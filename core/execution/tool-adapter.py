#!/usr/bin/env python3
"""SPECTRA Tool Adapter (Layer 3 — deterministic execution).

Closes the plan->do gap in a SPECTRA-native, authorized-only way: it lets an
engagement actually RUN a vetted security tool against an in-scope target, with
every invocation gated by engagement scope and Rules of Engagement, and the
destructive HARD BLOCK enforced. It is the disciplined alternative to "an agent
shells out to whatever it wants".

Guarantees:

  * Allowlist only. Only tools in ADAPTERS run. There is no arbitrary command
    execution — the binary is fixed per logical tool and never taken from input.
  * No shell. Commands run as an argv list via subprocess (shell=False), so there
    is no shell-injection surface from target or extra args.
  * Scope-gated. The target must pass the engagement scope check (in-scope, not
    out-of-scope) — reusing scope-enforcer, the same gate the workflows use.
  * RoE-gated. The action implied by the tool is checked against Rules of
    Engagement (e.g. a DoS tool needs dos_testing_allowed).
  * HARD BLOCK. Destructive intent (ransomware/wipers/data-destroyers and
    obviously destructive shell constructs) is refused outright — defense in
    depth on top of scope-enforcer's destructive keyword block.
  * Honest by default. --dry-run builds and gates the command and shows exactly
    what WOULD run, executing nothing.

Execution defaults to the local host. Remote execution against a declared,
in-scope, fingerprint-pinned exec_target is handled by exec-target.py (Goal 5)
and composed by this adapter via --via exec-target.

CLI:
  tool-adapter.py run --engagement e.yaml --tool nmap --target 10.0.0.5 [-- -sV]
  tool-adapter.py run --engagement e.yaml --tool nmap --target 10.0.0.5 --dry-run
  tool-adapter.py list
"""

from __future__ import annotations

import argparse
import importlib.util
import ipaddress
import json
import re
import shutil
import subprocess  # nosec B404 - we run only allowlisted binaries, never a shell
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------------------
# Tool allowlist (FAIL-CLOSED)
# ---------------------------------------------------------------------------
# Each adapter fixes the BINARY (never taken from user input) plus a
# *case-sensitive* allowlist of safe flags. Anything not on the allowlist is
# refused. This is deliberately fail-closed: a denylist of dangerous flags is
# whack-a-mole — e.g. nmap -iR scans random hosts and overrides the gated
# target; nmap --script and nuclei -t execute code; -oN/-iL/--resume read or
# write files. Only explicitly vetted, read-only flags are permitted. Flags
# taking a value are in value_flags; bare values must be in allowed_values;
# values are charset-restricted (no file paths). target_flag, when set, precedes
# the target argument.
#
# Adding a tool or flag here is a SECURITY decision: each flag must be unable to
# read/write arbitrary files, run code, or override the target/scope. nuclei is
# intentionally excluded — its templates (-t) can execute code, which flag-gating
# alone cannot make safe.
ADAPTERS: dict[str, dict[str, Any]] = {
    "nmap": {
        "binary": "nmap", "action": "recon", "read_only": True,
        "identity": {"probe": ["--version"], "expect": "nmap"},
        "allowed_flags": {
            "-sV", "-sn", "-sS", "-sT", "-sU", "-Pn", "-n", "-F", "-O",
            "-v", "-vv", "-4", "-6", "--open", "-p", "--top-ports",
            "--min-rate", "--max-rate",
            "-T0", "-T1", "-T2", "-T3", "-T4", "-T5",
        },
        "value_flags": {"-p", "--top-ports", "--min-rate", "--max-rate"},
        "allowed_values": set(),
    },
    "httpx": {
        "binary": "httpx", "action": "recon", "read_only": True,
        "target_flag": "-u",
        # Pin identity to ProjectDiscovery httpx — the bare name collides with
        # the Python `httpx` HTTP client (different, mutating flags).
        "identity": {"probe": ["-version"], "expect": "projectdiscovery"},
        "allowed_flags": {
            "-silent", "-sc", "-status-code", "-title", "-td", "-tech-detect",
            "-fr", "-follow-redirects", "-json", "-ip", "-cdn", "-cname",
            "-location", "-server", "-web-server", "-cl", "-content-length",
            "-nc", "-no-color", "-p", "-ports", "-t", "-threads",
            "-timeout", "-rl", "-rate-limit",
        },
        # -method is intentionally excluded: a non-GET method (PUT/DELETE/POST)
        # could mutate the target, breaking the read-only recon posture.
        "value_flags": {"-p", "-ports", "-t", "-threads", "-timeout",
                        "-rl", "-rate-limit"},
        "allowed_values": set(),
    },
    "dig": {
        "binary": "dig", "action": "recon", "read_only": True,
        "identity": {"probe": ["-v"], "expect": "dig"},
        "allowed_flags": {
            "+short", "+noall", "+answer", "+trace", "+tcp",
            "+nocomments", "+nostats", "-x", "-t", "-4", "-6",
        },
        "value_flags": {"-t"},
        "allowed_values": {
            "A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR",
            "SRV", "CAA", "ANY", "DNSKEY", "DS",
        },
    },
    "whatweb": {
        "binary": "whatweb", "action": "recon", "read_only": True,
        "identity": {"probe": ["--version"], "expect": "whatweb"},
        "allowed_flags": {
            "-a", "--aggression", "-v", "--verbose", "--no-errors",
            "-t", "--max-threads", "--open-timeout", "--read-timeout",
        },
        "value_flags": {"-a", "--aggression", "-t", "--max-threads",
                        "--open-timeout", "--read-timeout"},
        "allowed_values": set(),
    },
}

# Defense-in-depth command-level denylist: obviously destructive shell
# constructs that must never run, regardless of tool or RoE. This complements
# (does not replace) scope-enforcer.check_action_restrictions, which separately
# blocks destructive keywords like "ransomware"/"wiper" at the action level.
DESTRUCTIVE_PATTERNS = [
    re.compile(r"\brm\b.*(?:-rf|-fr|-r\b.*-f|--recursive|--force)", re.IGNORECASE),
    re.compile(r"\bmkfs(\.\w+)?\b", re.IGNORECASE),
    re.compile(r"\bdd\b[^\n]*\bof=", re.IGNORECASE),
    re.compile(r"\b(wipefs|shred|fdisk|parted)\b", re.IGNORECASE),
    re.compile(r"\b(shutdown|reboot|halt|poweroff)\b", re.IGNORECASE),
    re.compile(r">\s*/dev/sd[a-z]", re.IGNORECASE),
    re.compile(r":\(\)\s*\{", re.IGNORECASE),            # fork bomb
]

# A safe value token: alphanumerics plus a small set of punctuation used by port
# specs, timing, rates, and DNS record types. No slash (so no file paths), no
# whitespace, no leading dash.
_SAFE_VALUE_RE = re.compile(r"^[A-Za-z0-9_.,:+%@-]+$")

DEFAULT_TIMEOUT_SECONDS = 300
# Cap captured output so a large scan cannot return an unbounded blob.
MAX_OUTPUT_CHARS = 2_000_000


# ---------------------------------------------------------------------------
# Engagement + scope-enforcer loading
# ---------------------------------------------------------------------------

def _load_scope_enforcer():
    script = Path(__file__).resolve().with_name("scope-enforcer.py")
    spec = importlib.util.spec_from_file_location("scope_enforcer", script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load scope enforcer: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope_enforcer = _load_scope_enforcer()


def load_engagement(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Engagement file not found: {path}")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if "engagement" not in data:
        raise ValueError("Invalid engagement file: missing 'engagement' root key")
    return data


# ---------------------------------------------------------------------------
# Command building + gating
# ---------------------------------------------------------------------------

def resolve_tool(tool: str) -> dict[str, Any]:
    adapter = ADAPTERS.get(tool)
    if adapter is None:
        raise KeyError(f"Unknown tool '{tool}'. Allowlisted: {', '.join(sorted(ADAPTERS))}")
    return adapter


def build_argv(adapter: dict[str, Any], target: str, extra_args: list[str] | None) -> list[str]:
    """Build the argv list. The binary is fixed; the target and extra args are data."""
    argv = [adapter["binary"]]
    if extra_args:
        argv.extend(extra_args)
    if target:
        if adapter.get("target_flag"):
            argv.append(adapter["target_flag"])
        argv.append(target)
    return argv


def destructive_check(argv: list[str]) -> tuple[bool, str]:
    """Return (ok, reason). ok=False means a destructive construct was found."""
    joined = " ".join(argv)
    for pattern in DESTRUCTIVE_PATTERNS:
        if pattern.search(joined):
            return False, f"destructive construct hard-blocked: matches /{pattern.pattern}/"
    return True, ""


def _safe_value(value: str) -> bool:
    """A value token must be a restricted scalar — no file paths, no traversal."""
    return bool(_SAFE_VALUE_RE.match(value)) and ".." not in value


def _url_in_scope(target_url: str, in_scope: dict[str, Any]) -> bool:
    """Path-aware URL scope check.

    scope-enforcer treats a URL as in-scope when only its HOSTNAME matches an
    in-scope application, ignoring the path — so an app declared as
    https://host/app would also admit https://host/admin. For execution we
    require either (a) the host matches an in-scope DOMAIN (host-level scope), or
    (b) the URL falls under an in-scope APPLICATION's path prefix.
    """
    parsed = urlparse(target_url)
    host = (parsed.hostname or "").lower()
    if not host:
        return False
    path = parsed.path or "/"

    for dom in in_scope.get("domains", []) or []:
        if scope_enforcer._domain_matches(host, str(dom)):
            return True

    for app in in_scope.get("applications", []) or []:
        app_parsed = urlparse(str(app))
        app_host = (app_parsed.hostname or "").lower()
        if app_host != host:
            continue
        app_path = (app_parsed.path or "").rstrip("/")
        if not app_path:  # application declared host-only -> whole host in scope
            return True
        if path == app_path or path.startswith(app_path + "/"):
            return True
    return False


def _cidr_contained(target_cidr: str, in_scope_networks: list[str]) -> bool:
    """True only if the whole target CIDR sits inside an in-scope network.

    scope-enforcer treats a CIDR target as in-scope when it merely OVERLAPS an
    in-scope network, so a broad target like 0.0.0.0/0 would pass. For actually
    executing a tool we require full containment, closing that scope bypass.
    """
    try:
        target_net = ipaddress.ip_network(target_cidr, strict=False)
    except ValueError:
        return False
    for net in in_scope_networks or []:
        try:
            scope_net = ipaddress.ip_network(str(net), strict=False)
        except ValueError:
            continue
        if target_net.version == scope_net.version and target_net.subnet_of(scope_net):
            return True
    return False


def validate_target(target: str) -> tuple[bool, str]:
    """Targets are data, never flags: reject anything that could be misread as
    an option or carry shell/control characters."""
    if not target:
        return False, "empty target"
    if "\x00" in target:
        return False, "target contains a null byte"
    if target.startswith("-"):
        return False, f"target may not start with '-': {target!r}"
    if any(c.isspace() for c in target):
        return False, f"target may not contain whitespace: {target!r}"
    return True, ""


def validate_extra_args(adapter: dict[str, Any], extra_args: list[str] | None) -> tuple[bool, str]:
    """Fail-closed allowlist check of extra args (case-sensitive flags).

    Each flag token must be in the adapter's allowed_flags; values must follow a
    value_flag or be in allowed_values, and must be restricted scalars (no paths).
    """
    allowed_flags = adapter.get("allowed_flags", set())
    value_flags = adapter.get("value_flags", set())
    allowed_values = adapter.get("allowed_values", set())

    expect_value = False
    for arg in extra_args or []:
        if "\x00" in arg or any(c.isspace() for c in arg):
            return False, f"argument has whitespace or null byte: {arg!r}"

        if arg.startswith("-") or arg.startswith("+"):  # '+' covers dig flags
            token = arg.split("=", 1)[0]
            if token not in allowed_flags:
                return False, (f"flag not on allowlist for this tool: {arg!r} "
                               f"(allowed: {', '.join(sorted(allowed_flags))})")
            if "=" in arg:
                value = arg.split("=", 1)[1]
                if not _safe_value(value):
                    return False, f"unsafe value for {token}: {value!r}"
                expect_value = False
            else:
                expect_value = token in value_flags
        else:
            # A bare value: only valid right after a value-flag, or if explicitly
            # allowed (e.g. a DNS record type). Never a filesystem path.
            if expect_value:
                if not _safe_value(arg):
                    return False, f"unsafe value: {arg!r}"
                expect_value = False
            elif arg in allowed_values:
                continue
            else:
                return False, f"unexpected argument (not a flag or allowed value): {arg!r}"
    return True, ""


def gate(engagement: dict[str, Any], adapter: dict[str, Any], target: str,
         argv: list[str], extra_args: list[str] | None = None) -> dict[str, Any]:
    """Gate a tool invocation against scope, RoE, and the destructive HARD BLOCK."""
    errors: list[str] = []
    eng = engagement.get("engagement", {}) or {}
    scope = eng.get("scope", {}) or {}
    in_scope = scope.get("in_scope", {}) or {}
    out_scope = scope.get("out_of_scope", {}) or {}
    roe = eng.get("rules_of_engagement", {}) or {}

    # 1. Destructive HARD BLOCK (command level) — first, unconditional.
    ok, reason = destructive_check(argv)
    if not ok:
        errors.append(reason)

    # 1b. Target must be data, not a flag or control string.
    target_ok, target_reason = validate_target(target)
    if not target_ok:
        errors.append(f"invalid target: {target_reason}")

    # 1c. Extra args must pass the fail-closed per-tool flag allowlist.
    args_ok, args_reason = validate_extra_args(adapter, extra_args)
    if not args_ok:
        errors.append(args_reason)

    # 2. Scope: target must be classified, in-scope, and not out-of-scope.
    target_type, normalized = scope_enforcer.classify_target(target)
    out_blocked, out_reason = scope_enforcer.check_out_of_scope(target_type, normalized, out_scope)
    if out_blocked:
        errors.append(f"target out of scope: {out_reason}")
    in_ok, in_reason = scope_enforcer.check_in_scope(target_type, normalized, in_scope)
    if not in_ok:
        errors.append(f"target not in engagement scope: {target}")
    elif target_type == "cidr" and not _cidr_contained(normalized, in_scope.get("networks", [])):
        # Overlap is not enough for execution: the whole range must be in scope.
        errors.append(f"CIDR target not fully contained in an in-scope network: {target}")
    elif target_type == "url" and not _url_in_scope(target, in_scope):
        # Hostname match is not enough: the URL must fall under an in-scope
        # domain or application path, not just share a host with one.
        errors.append(f"URL not within an in-scope domain or application path: {target}")

    # 3. RoE / action restrictions (also re-checks destructive keywords).
    action_string = f"{adapter.get('action', '')} {' '.join(argv)}"
    action_ok, restrictions = scope_enforcer.check_action_restrictions(action_string, roe)
    if not action_ok:
        errors.extend(restrictions)

    return {
        "allowed": len(errors) == 0,
        "errors": errors,
        "target_type": target_type,
        "normalized_target": normalized,
        "scope_reason": in_reason if in_ok else "",
    }


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def execute(argv: list[str], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Run argv with no shell, capturing output. Never raises on tool failure."""
    try:
        proc = subprocess.run(  # nosec B603 - argv is allowlisted binary, shell=False
            argv,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
    except subprocess.TimeoutExpired:
        return {"executed": True, "timed_out": True, "exit_code": None,
                "stdout": "", "stderr": f"timed out after {timeout}s", "truncated": False}

    def _cap(text: str) -> tuple[str, bool]:
        if text and len(text) > MAX_OUTPUT_CHARS:
            return text[:MAX_OUTPUT_CHARS] + "\n...[truncated]", True
        return text, False

    stdout, t1 = _cap(proc.stdout or "")
    stderr, t2 = _cap(proc.stderr or "")
    return {
        "executed": True,
        "timed_out": False,
        "exit_code": proc.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "truncated": t1 or t2,
    }


def verify_identity(resolved_path: str, adapter: dict[str, Any]) -> tuple[bool, str]:
    """Confirm the resolved binary really is the expected tool.

    `shutil.which("httpx")` may resolve to the Python `httpx` HTTP client rather
    than ProjectDiscovery httpx — a different tool with mutating flags. A short
    probe (e.g. --version) must contain the expected marker before we trust the
    flag allowlist. Adapters without an `identity` block skip the check.
    """
    identity = adapter.get("identity")
    if not identity:
        return True, ""
    probe = [resolved_path] + list(identity.get("probe", []))
    expect = str(identity.get("expect", "")).lower()
    result = execute(probe, timeout=15)
    blob = ((result.get("stdout") or "") + " " + (result.get("stderr") or "")).lower()
    if expect and expect in blob:
        return True, ""
    return False, (f"resolved binary at {resolved_path} is not the expected "
                   f"'{adapter['binary']}' (identity marker '{expect}' not found)")


def _load_exec_target():
    # Lazy import (avoids a load-time cycle with exec-target.py).
    script = Path(__file__).resolve().with_name("exec-target.py")
    spec = importlib.util.spec_from_file_location("exec_target", script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load exec target: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _load_run_accounting():
    # Lazy import of the hyphenated run-accounting.py module.
    script = Path(__file__).resolve().with_name("run-accounting.py")
    spec = importlib.util.spec_from_file_location("run_accounting", script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load run accounting: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(engagement_path: str, tool: str, target: str, extra_args: list[str] | None = None,
        dry_run: bool = False, timeout: int = DEFAULT_TIMEOUT_SECONDS,
        via: str | None = None) -> dict[str, Any]:
    """Resolve, gate, and (unless dry_run) execute a vetted tool invocation.

    via="exec-target" runs the *gated* command on the engagement's declared,
    fingerprint-pinned exec_target host instead of locally — the tool adapter
    enforces tool/flag/target scope, exec-target enforces the authorized host.
    """
    adapter = resolve_tool(tool)
    engagement = load_engagement(engagement_path)
    argv = build_argv(adapter, target, extra_args)
    gate_result = gate(engagement, adapter, target, argv, extra_args)

    result: dict[str, Any] = {
        "tool": tool,
        "target": target,
        "argv": argv,
        "dry_run": dry_run,
        "via": via or "local",
        "gate": gate_result,
    }

    if not gate_result["allowed"]:
        result["status"] = "blocked"
        return result

    # A dry run shows the gated plan without needing the tool installed.
    if dry_run:
        result["status"] = "planned"
        return result

    # Remote execution on the declared exec_target: the command is already
    # tool/flag/scope gated above; exec-target adds the authorized+pinned host.
    if via == "exec-target":
        remote = _load_exec_target().run_remote_gated(engagement_path, argv, timeout)
        result["remote"] = remote
        result["status"] = "executed_remote" if remote.get("status") == "executed" else remote.get("status", "error")
        return result

    # The binary must be installed to actually run. Resolve to an absolute path
    # and execute that exact path (avoids a TOCTOU/PATH-reresolution window).
    resolved = shutil.which(adapter["binary"])
    if resolved is None:
        result["status"] = "unavailable"
        result["error"] = f"binary '{adapter['binary']}' not found on PATH"
        return result

    # Confirm the resolved binary is actually the expected tool before trusting
    # the flag allowlist (guards the httpx name collision).
    id_ok, id_reason = verify_identity(resolved, adapter)
    if not id_ok:
        result["status"] = "unavailable"
        result["error"] = id_reason
        return result

    exec_argv = [resolved] + argv[1:]
    result["execution"] = execute(exec_argv, timeout)
    result["status"] = "executed"
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> None:
    catalog = {
        name: {"binary": a["binary"], "action": a["action"],
               "read_only": a.get("read_only", False),
               "available": shutil.which(a["binary"]) is not None}
        for name, a in sorted(ADAPTERS.items())
    }
    print(json.dumps({"tools": catalog}, indent=2))


def cmd_run(args: argparse.Namespace) -> None:
    try:
        result = run(args.engagement, args.tool, args.target,
                     extra_args=args.extra, dry_run=args.dry_run, timeout=args.timeout,
                     via=args.via)
    except (FileNotFoundError, ValueError, KeyError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)

    # Best-effort run accounting: record what ran so the engagement keeps an
    # operational activity log. Never let an accounting failure affect the run
    # outcome or exit code.
    if not args.no_log:
        try:
            _load_run_accounting().record(args.engagement, result)
        except Exception:  # nosec B110 - accounting is advisory, never fatal
            pass

    print(json.dumps(result, indent=2))
    # Exit codes: 0 ok/planned, 1 blocked, 2 unavailable/fingerprint, 4 nonzero exit.
    status = result["status"]
    if status == "blocked":
        sys.exit(1)
    if status in ("unavailable", "fingerprint_mismatch"):
        sys.exit(2)
    if status == "executed" and result["execution"].get("exit_code") not in (0, None):
        sys.exit(4)
    if status == "executed_remote" and result["remote"].get("execution", {}).get("exit_code") not in (0, None):
        sys.exit(4)
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tool-adapter.py",
        description="Run a vetted security tool, gated by engagement scope and RoE.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List allowlisted tools and availability")
    p_list.set_defaults(func=cmd_list)

    p_run = sub.add_parser("run", help="Run a vetted tool against an in-scope target")
    p_run.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_run.add_argument("--tool", required=True, help="Allowlisted tool name (see 'list')")
    p_run.add_argument("--target", required=True, help="Target (must be in engagement scope)")
    p_run.add_argument("--dry-run", action="store_true", help="Gate and show the command; execute nothing")
    p_run.add_argument("--via", choices=["exec-target"], default=None,
                       help="Run the gated command on the engagement's declared exec_target host")
    p_run.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS, help="Execution timeout (s)")
    p_run.add_argument("--no-log", action="store_true", help="Do not append this run to the engagement run log")
    p_run.add_argument("extra", nargs="*", help="Extra tool args (after --)")
    p_run.set_defaults(func=cmd_run)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
