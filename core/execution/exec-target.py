#!/usr/bin/env python3
"""SPECTRA Exec Target (Layer 3 — deterministic execution).

Goal 5 makes SPECTRA executable against a real host in an authorized-only way.
An engagement may declare an `exec_target`: an operator-owned host where
RoE-authorized commands may be run over SSH. The authorization boundary is
explicit and layered:

  * authorized: the operator must set exec_target.authorized = true;
  * in scope: the exec host must be inside the engagement scope;
  * fingerprint pinned: the live host key must match exec_target.pinned_fingerprint
    (TOFU is refused) — connecting to an unexpected host is blocked, not trusted.

SSH is invoked with no shell on our side (argv list), strict host-key checking
against a temp known_hosts built from the *verified* key, BatchMode (no
interactive auth), and the remote command shlex-quoted so a token cannot break
out into the remote shell. Destructive remote commands are refused.

This module does not decide WHAT tool to run — that is gated by the tool adapter
(Goal 4). It decides WHERE and proves the where is the authorized, pinned host.

CLI:
  exec-target.py verify --engagement e.yaml
  exec-target.py run --engagement e.yaml -- nmap -sn 127.0.0.1
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shlex
import subprocess  # nosec B404 - argv list, no shell on our side
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


DEFAULT_PORT = 22
CONNECT_TIMEOUT = 10
DEFAULT_TIMEOUT_SECONDS = 300

# Host/user must never be interpretable as an ssh option (leading '-') or carry
# shell/option metacharacters. Hostnames and IPv4/IPv6 use alnum + . - : only.
_SAFE_HOST_RE = re.compile(r"^[A-Za-z0-9._:-]+$")
_SAFE_USER_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def _load_sibling(module_name: str, filename: str):
    script = Path(__file__).resolve().with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load {filename}: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope_enforcer = _load_sibling("scope_enforcer", "scope-enforcer.py")
tool_adapter = _load_sibling("tool_adapter", "tool-adapter.py")

# Remote commands are restricted to a fail-closed allowlist of READ-ONLY
# DIAGNOSTIC binaries only. This refuses shell/interpreter wrappers AND scanning
# tools (nmap/httpx/dig/whatweb): running a tool here would bypass the tool
# adapter's flag allowlist and per-target scope check (e.g. `nmap -iR <host>`
# would scan arbitrary out-of-scope hosts even though the exec host is in scope).
# Gated tool execution on a remote host must go through the tool adapter (which
# enforces flags + target scope), not this raw runner.
REMOTE_ALLOWED_BINARIES = {
    "id", "uname", "whoami", "hostname", "pwd", "uptime", "true", "echo",
}


def load_engagement(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Engagement file not found: {path}")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if "engagement" not in data:
        raise ValueError("Invalid engagement file: missing 'engagement' root key")
    return data


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_exec_target(engagement: dict[str, Any]) -> dict[str, Any]:
    """Validate the exec_target declaration against the authorization boundary."""
    errors: list[str] = []
    eng = engagement.get("engagement", {}) or {}
    target = eng.get("exec_target")

    if target is None:
        return {"present": False, "allowed": False,
                "errors": ["no exec_target declared (execution stays local)"]}
    if not isinstance(target, dict):
        return {"present": True, "allowed": False, "errors": ["exec_target must be a mapping"]}

    for field in ("host", "user", "pinned_fingerprint"):
        if not str(target.get(field, "")).strip():
            errors.append(f"exec_target.{field} is required")

    # Host/user must not be interpretable as ssh options or carry metacharacters.
    host_val = str(target.get("host", "")).strip()
    if host_val and (host_val.startswith("-") or not _SAFE_HOST_RE.match(host_val)):
        errors.append(f"exec_target.host has an unsafe value: {host_val!r}")
    user_val = str(target.get("user", "")).strip()
    if user_val and (user_val.startswith("-") or not _SAFE_USER_RE.match(user_val)):
        errors.append(f"exec_target.user has an unsafe value: {user_val!r}")

    if target.get("authorized") is not True:
        errors.append("exec_target.authorized must be true before remote execution")

    fp = str(target.get("pinned_fingerprint", "")).strip()
    if fp and not fp.startswith("SHA256:"):
        errors.append("exec_target.pinned_fingerprint must be a SHA256:... fingerprint")

    if "port" in target:
        port = target["port"]
        if isinstance(port, bool) or not isinstance(port, int) or not (1 <= port <= 65535):
            errors.append("exec_target.port must be an integer in 1..65535")

    key_path = str(target.get("key_path", "")).strip()
    if key_path and not Path(key_path).expanduser().is_file():
        errors.append(f"exec_target.key_path not found: {key_path}")

    # The exec host must be inside the engagement scope.
    host = str(target.get("host", "")).strip()
    if host:
        scope = eng.get("scope", {}) or {}
        in_scope = scope.get("in_scope", {}) or {}
        out_scope = scope.get("out_of_scope", {}) or {}
        ttype, normalized = scope_enforcer.classify_target(host)
        out_blocked, out_reason = scope_enforcer.check_out_of_scope(ttype, normalized, out_scope)
        if out_blocked:
            errors.append(f"exec_target.host is out of scope: {out_reason}")
        in_ok, _ = scope_enforcer.check_in_scope(ttype, normalized, in_scope)
        if not in_ok:
            errors.append(f"exec_target.host not in engagement scope: {host}")

    return {"present": True, "allowed": len(errors) == 0, "errors": errors, "target": target}


# ---------------------------------------------------------------------------
# Fingerprint pinning
# ---------------------------------------------------------------------------

def scan_host_keys(host: str, port: int) -> str:
    """Return ssh-keyscan output (known_hosts lines) for the host."""
    # '--' terminates option parsing so a crafted host cannot inject flags.
    result = tool_adapter.execute(["ssh-keyscan", "-p", str(port), "--", host], timeout=20)
    return result.get("stdout", "") or ""


def _fingerprint_of_line(known_hosts_line: str) -> str:
    """Compute the SHA256 fingerprint of a single known_hosts line."""
    # A valid known_hosts line is "host keytype base64key" — at least 3 fields.
    parts = known_hosts_line.split()
    if len(parts) < 3:
        return ""
    fh = tempfile.NamedTemporaryFile("w", suffix=".kh", delete=False)
    try:
        fh.write(known_hosts_line + "\n")
        fh.close()
        result = tool_adapter.execute(["ssh-keygen", "-lf", fh.name], timeout=10)
    finally:
        Path(fh.name).unlink(missing_ok=True)
    out = result.get("stdout", "") or ""
    for token in out.split():
        if token.startswith("SHA256:"):
            return token
    return ""


def verify_fingerprint(host: str, port: int, pinned: str) -> dict[str, Any]:
    """Confirm the live host key matches the pinned fingerprint.

    Returns the matching known_hosts line for strict pinning. A mismatch or an
    unreachable host is a hard failure — never trust-on-first-use.
    """
    scan = scan_host_keys(host, port)
    lines = [ln for ln in scan.splitlines() if ln.strip() and not ln.startswith("#")]
    if not lines:
        return {"matched": False, "reason": f"could not retrieve host key for {host}:{port}",
                "known_hosts_line": ""}
    for line in lines:
        if _fingerprint_of_line(line) == pinned:
            return {"matched": True, "reason": "", "known_hosts_line": line}
    return {"matched": False,
            "reason": f"live host key does not match pinned fingerprint {pinned}",
            "known_hosts_line": ""}


# ---------------------------------------------------------------------------
# Remote execution
# ---------------------------------------------------------------------------

def build_ssh_argv(target: dict[str, Any], known_hosts_file: str, remote_argv: list[str]) -> list[str]:
    """Build a hardened ssh argv. The remote command is shlex-quoted into one
    safe string so a token cannot break out into the remote shell."""
    port = int(target.get("port", DEFAULT_PORT))
    user = target["user"]
    host = target["host"]
    argv = [
        "ssh",
        "-F", "/dev/null",                 # ignore user SSH config for determinism
        "-p", str(port),
        "-o", "BatchMode=yes",
        "-o", "StrictHostKeyChecking=yes",
        "-o", f"UserKnownHostsFile={known_hosts_file}",
        "-o", f"ConnectTimeout={CONNECT_TIMEOUT}",
    ]
    key_path = str(target.get("key_path", "")).strip()
    if key_path:
        argv += ["-i", str(Path(key_path).expanduser())]
    argv.append(f"{user}@{host}")
    # The remote command is one shlex-quoted string; no post-destination '--'
    # (ssh would send it to the remote as literal command text).
    argv.append(" ".join(shlex.quote(tok) for tok in remote_argv))
    return argv


def run_remote(engagement_path: str, remote_argv: list[str],
               timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Validate, pin, and execute a remote command on the declared exec_target."""
    engagement = load_engagement(engagement_path)
    validation = validate_exec_target(engagement)
    result: dict[str, Any] = {"remote_argv": remote_argv, "validation": validation}

    if not validation["allowed"]:
        result["status"] = "blocked"
        return result

    # Fail-closed: the remote binary must be on the allowlist (no shell/interpreter
    # wrappers), and the command must not be destructive.
    if not remote_argv:
        result["status"] = "blocked"
        result["validation"]["errors"].append("empty remote command")
        return result
    # The binary must be a BARE allowlisted name. A path-qualified token (e.g.
    # /tmp/evil/id or ./id) whose basename is "id" would otherwise run an
    # arbitrary planted binary — so reject any '/' or '\' and match the whole
    # token. The remote shell resolves the bare name via PATH.
    remote_bin = remote_argv[0]
    if "/" in remote_bin or "\\" in remote_bin or remote_bin not in REMOTE_ALLOWED_BINARIES:
        result["status"] = "blocked"
        result["validation"]["errors"].append(
            f"remote binary not allowed: {remote_argv[0]!r} "
            f"(allowed bare names only: {', '.join(sorted(REMOTE_ALLOWED_BINARIES))})")
        return result
    ok, reason = tool_adapter.destructive_check(remote_argv)
    if not ok:
        result["status"] = "blocked"
        result["validation"]["errors"].append(reason)
        return result

    return _pin_and_ssh(validation["target"], remote_argv, result, timeout)


def run_remote_gated(engagement_path: str, remote_argv: list[str],
                     timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
    """Run a remote command that has ALREADY been gated by the tool adapter
    (tool allowlist + flag allowlist + target scope). Skips this module's
    diagnostics-only binary allowlist, but still enforces the exec_target
    authorization boundary (authorized + in-scope host + pinned fingerprint),
    rejects path-qualified binaries, and refuses destructive commands.

    This is the composition behind `tool-adapter.py run --via exec-target`.
    """
    engagement = load_engagement(engagement_path)
    validation = validate_exec_target(engagement)
    result: dict[str, Any] = {"remote_argv": remote_argv, "validation": validation}
    if not validation["allowed"]:
        result["status"] = "blocked"
        return result
    if not remote_argv:
        result["status"] = "blocked"
        result["validation"]["errors"].append("empty remote command")
        return result
    # Even though the caller gated the tool, never accept a path-qualified binary.
    if "/" in remote_argv[0] or "\\" in remote_argv[0]:
        result["status"] = "blocked"
        result["validation"]["errors"].append(
            f"remote binary may not be path-qualified: {remote_argv[0]!r}")
        return result
    ok, reason = tool_adapter.destructive_check(remote_argv)
    if not ok:
        result["status"] = "blocked"
        result["validation"]["errors"].append(reason)
        return result
    return _pin_and_ssh(validation["target"], remote_argv, result, timeout)


def _pin_and_ssh(target: dict[str, Any], remote_argv: list[str],
                 result: dict[str, Any], timeout: int) -> dict[str, Any]:
    """Verify the pinned fingerprint, then run the command over hardened SSH."""
    port = int(target.get("port", DEFAULT_PORT))
    pin = verify_fingerprint(target["host"], port, str(target["pinned_fingerprint"]).strip())
    result["fingerprint"] = {"matched": pin["matched"], "reason": pin["reason"]}
    if not pin["matched"]:
        result["status"] = "fingerprint_mismatch"
        return result
    kh = tempfile.NamedTemporaryFile("w", suffix=".known_hosts", delete=False)
    try:
        kh.write(pin["known_hosts_line"] + "\n")
        kh.close()
        Path(kh.name).chmod(0o600)
        ssh_argv = build_ssh_argv(target, kh.name, remote_argv)
        result["ssh_argv"] = ssh_argv
        result["execution"] = tool_adapter.execute(ssh_argv, timeout)
    finally:
        Path(kh.name).unlink(missing_ok=True)
    result["status"] = "executed"
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_verify(args: argparse.Namespace) -> None:
    try:
        engagement = load_engagement(args.engagement)
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    validation = validate_exec_target(engagement)
    out = {"validation": validation}
    if validation["allowed"]:
        target = validation["target"]
        port = int(target.get("port", DEFAULT_PORT))
        out["fingerprint"] = verify_fingerprint(
            target["host"], port, str(target["pinned_fingerprint"]).strip())
    print(json.dumps(out, indent=2))
    ok = validation["allowed"] and (out.get("fingerprint", {}).get("matched", False))
    sys.exit(0 if ok else 1)


def cmd_run(args: argparse.Namespace) -> None:
    if not args.remote:
        print(json.dumps({"error": "no remote command given (use -- <command>)"}), file=sys.stderr)
        sys.exit(3)
    try:
        result = run_remote(args.engagement, args.remote, timeout=args.timeout)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    print(json.dumps(result, indent=2))
    status = result["status"]
    if status == "blocked":
        sys.exit(1)
    if status == "fingerprint_mismatch":
        sys.exit(2)
    if status == "executed" and result["execution"].get("exit_code") not in (0, None):
        sys.exit(4)
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="exec-target.py",
        description="Run authorized commands on a declared, fingerprint-pinned SSH host.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_ver = sub.add_parser("verify", help="Validate exec_target and verify host fingerprint")
    p_ver.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_ver.set_defaults(func=cmd_verify)

    p_run = sub.add_parser("run", help="Run a remote command on the exec_target")
    p_run.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_run.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS)
    p_run.add_argument("remote", nargs=argparse.REMAINDER, help="Remote command after --")
    p_run.set_defaults(func=cmd_run)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    # argparse REMAINDER keeps a leading '--'; drop it.
    if getattr(args, "remote", None) and args.remote and args.remote[0] == "--":
        args.remote = args.remote[1:]
    args.func(args)


if __name__ == "__main__":
    main()
