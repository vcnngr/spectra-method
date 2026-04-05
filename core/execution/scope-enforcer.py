#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
SPECTRA Scope Enforcer
Programmatic scope verification for engagement targets.
Called by SPECTRA agents before any target interaction.

Usage:
  python scope-enforcer.py check --target <target> --engagement <path/to/engagement.yaml> [--action <type>]
  python scope-enforcer.py bulk --targets <file_with_targets> --engagement <path/to/engagement.yaml>
  python scope-enforcer.py summary --engagement <path/to/engagement.yaml>

Exit codes:
  0 — IN_SCOPE (all targets verified)
  1 — OUT_OF_SCOPE (at least one target denied)
  2 — AMBIGUOUS (at least one target unresolved)
  3 — Error (invalid input, missing file, bad YAML)
"""

import argparse
import ipaddress
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

import yaml


# ---------------------------------------------------------------------------
# Engagement loader
# ---------------------------------------------------------------------------

def load_engagement(path: str) -> dict:
    """Load and validate an engagement YAML file."""
    p = Path(path)
    if not p.exists():
        _die(f"Engagement file not found: {path}")
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or "engagement" not in data:
        _die("Invalid engagement file: missing 'engagement' root key")
    eng = data["engagement"]
    scope = eng.get("scope", {})
    in_scope = scope.get("in_scope", {})
    out_scope = scope.get("out_of_scope", {})
    # Verify scope is populated
    if _is_scope_empty(in_scope) and _is_scope_empty(out_scope):
        _die("Engagement scope is empty. Populate scope fields before running scope checks.")
    return eng


def _is_scope_empty(scope_section: dict) -> bool:
    """Return True if every list in the scope section is empty or absent."""
    if not scope_section:
        return True
    for key, val in scope_section.items():
        if key == "notes":
            continue
        if isinstance(val, list) and len(val) > 0:
            return False
    return True


# ---------------------------------------------------------------------------
# Target classification & normalization
# ---------------------------------------------------------------------------

def classify_target(raw: str) -> tuple[str, str]:
    """
    Classify a raw target string and return (type, normalized_value).
    Types: ipv4, cidr, domain, subdomain, url, hostname, cloud_account, username, action
    """
    target = raw.strip()

    # URL — contains ://
    if "://" in target:
        parsed = urlparse(target)
        domain = parsed.hostname or ""
        return "url", domain.lower()

    # Cloud account — provider:id pattern (e.g. AWS:123456789012)
    if ":" in target and not target.startswith("["):
        parts = target.split(":", 1)
        if parts[0].isalpha() and parts[1].strip():
            return "cloud_account", target

    # CIDR — contains /
    if "/" in target:
        try:
            net = ipaddress.ip_network(target, strict=False)
            return "cidr", str(net)
        except ValueError:
            pass

    # IPv4
    try:
        addr = ipaddress.ip_address(target)
        return "ipv4", str(addr)
    except ValueError:
        pass

    # Domain / subdomain — contains a dot and looks like a hostname
    if "." in target and not target.startswith('"'):
        normalized = target.lower().rstrip(".")
        labels = normalized.split(".")
        if len(labels) > 2:
            return "subdomain", normalized
        return "domain", normalized

    # Action description — quoted or long free-text
    if target.startswith('"') or " " in target:
        return "action", target.strip('"')

    # Fallback — treat as hostname (short label without dots)
    return "hostname", target


# ---------------------------------------------------------------------------
# Matching helpers
# ---------------------------------------------------------------------------

def _ip_in_network(ip_str: str, network_str: str) -> bool:
    """Check if an IP address is contained within a CIDR network."""
    try:
        return ipaddress.ip_address(ip_str) in ipaddress.ip_network(network_str, strict=False)
    except ValueError:
        return False


def _cidr_overlaps(cidr_a: str, cidr_b: str) -> bool:
    """Check if two CIDR ranges overlap."""
    try:
        return ipaddress.ip_network(cidr_a, strict=False).overlaps(
            ipaddress.ip_network(cidr_b, strict=False)
        )
    except ValueError:
        return False


def _domain_matches(target_domain: str, scope_domain: str) -> bool:
    """
    Check domain match including wildcards.
    - Exact: example.com == example.com
    - Wildcard: *.example.com matches sub.example.com (but NOT example.com itself)
    - Parent inclusion: if example.com is in scope, sub.example.com is implicitly in scope
    """
    td = target_domain.lower().rstrip(".")
    sd = scope_domain.lower().rstrip(".")

    # Exact match
    if td == sd:
        return True

    # Wildcard match (*.example.com)
    if sd.startswith("*."):
        parent = sd[2:]
        if td.endswith("." + parent) and td != parent:
            return True
        return False

    # Parent domain inclusion — if scope has example.com, sub.example.com matches
    if td.endswith("." + sd):
        return True

    return False


def _case_insensitive_match(target: str, scope_entry: str) -> bool:
    """Case-insensitive exact match."""
    return target.strip().lower() == scope_entry.strip().lower()


# ---------------------------------------------------------------------------
# Core scope check
# ---------------------------------------------------------------------------

def check_out_of_scope(target_type: str, normalized: str, out_scope: dict) -> tuple[bool, str]:
    """
    Check if target matches any out-of-scope entry.
    Returns (matched: bool, matched_entry: str).
    """
    # Networks
    for i, net in enumerate(out_scope.get("networks", []) or []):
        if target_type in ("ipv4",) and _ip_in_network(normalized, net):
            return True, f"scope.out_of_scope.networks[{i}]: {net}"
        if target_type == "cidr" and _cidr_overlaps(normalized, net):
            return True, f"scope.out_of_scope.networks[{i}]: {net}"

    # Domains
    for i, dom in enumerate(out_scope.get("domains", []) or []):
        if target_type in ("domain", "subdomain", "url") and _domain_matches(normalized, dom):
            return True, f"scope.out_of_scope.domains[{i}]: {dom}"

    # Applications
    for i, app in enumerate(out_scope.get("applications", []) or []):
        if target_type == "url" and _case_insensitive_match(normalized, urlparse(app).hostname or app):
            return True, f"scope.out_of_scope.applications[{i}]: {app}"

    # Critical systems
    for i, cs in enumerate(out_scope.get("critical_systems", []) or []):
        if target_type == "hostname" and _case_insensitive_match(normalized, cs):
            return True, f"scope.out_of_scope.critical_systems[{i}]: {cs}"
        # Also check IP-resolved hostnames against critical systems
        if target_type in ("ipv4", "domain", "subdomain") and _case_insensitive_match(normalized, cs):
            return True, f"scope.out_of_scope.critical_systems[{i}]: {cs}"

    # Users
    for i, usr in enumerate(out_scope.get("users", []) or []):
        if _case_insensitive_match(normalized, usr):
            return True, f"scope.out_of_scope.users[{i}]: {usr}"

    return False, ""


def check_in_scope(target_type: str, normalized: str, in_scope: dict) -> tuple[bool, str]:
    """
    Check if target matches any in-scope entry.
    Returns (matched: bool, matched_entry: str).
    """
    # Networks
    for i, net in enumerate(in_scope.get("networks", []) or []):
        if target_type == "ipv4" and _ip_in_network(normalized, net):
            return True, f"scope.in_scope.networks[{i}]: {net}"
        if target_type == "cidr" and _cidr_overlaps(normalized, net):
            return True, f"scope.in_scope.networks[{i}]: {net}"

    # Domains
    for i, dom in enumerate(in_scope.get("domains", []) or []):
        if target_type in ("domain", "subdomain", "url") and _domain_matches(normalized, dom):
            return True, f"scope.in_scope.domains[{i}]: {dom}"

    # Applications
    for i, app in enumerate(in_scope.get("applications", []) or []):
        if target_type == "url" and _case_insensitive_match(normalized, urlparse(app).hostname or app):
            return True, f"scope.in_scope.applications[{i}]: {app}"

    # Cloud accounts
    for i, ca in enumerate(in_scope.get("cloud_accounts", []) or []):
        if target_type == "cloud_account" and _case_insensitive_match(normalized, ca):
            return True, f"scope.in_scope.cloud_accounts[{i}]: {ca}"

    # Users
    for i, usr in enumerate(in_scope.get("users", []) or []):
        if _case_insensitive_match(normalized, usr):
            return True, f"scope.in_scope.users[{i}]: {usr}"

    return False, ""


def check_action_restrictions(action: str | None, roe: dict) -> tuple[bool, list[str]]:
    """
    Validate an action type against rules of engagement.
    Returns (allowed: bool, restriction_messages: list).
    """
    if not action:
        return True, []

    restrictions = []
    action_lower = action.lower()

    action_map = {
        "dos":              "dos_testing_allowed",
        "stress":           "dos_testing_allowed",
        "social-engineering": "social_engineering_allowed",
        "phishing":         "social_engineering_allowed",
        "physical":         "physical_access_allowed",
        "exfiltration":     "data_exfiltration_allowed",
        "exfil":            "data_exfiltration_allowed",
    }

    for keyword, field in action_map.items():
        if keyword in action_lower and not roe.get(field, False):
            restrictions.append(f"{field} is false — {action} not permitted by RoE")

    # Production systems check
    if "production" in action_lower and not roe.get("production_systems", False):
        restrictions.append("production_systems is false — production access not permitted")

    # Max impact level check
    impact_order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    max_impact = roe.get("max_impact_level", "high")
    if "critical" in action_lower and impact_order.get(max_impact, 3) < 4:
        restrictions.append(f"max_impact_level is '{max_impact}' — critical-impact actions not permitted")

    allowed = len(restrictions) == 0
    return allowed, restrictions


def check_timing(roe: dict, timezone: str) -> tuple[bool, str]:
    """
    Check if current time falls within authorized testing hours.
    Returns (within_window: bool, message: str).
    """
    testing_hours = roe.get("testing_hours", "any")
    if testing_hours == "any":
        return True, ""

    # Import datetime here — only needed for timing checks
    from datetime import datetime

    try:
        import zoneinfo
        tz = zoneinfo.ZoneInfo(timezone) if timezone else None
    except Exception:
        tz = None

    now = datetime.now(tz)
    hour = now.hour

    if testing_hours == "business-hours":
        if 9 <= hour < 17:
            return True, ""
        return False, f"Outside business hours (09:00-17:00). Current: {now.strftime('%H:%M')}"

    if testing_hours == "after-hours":
        if hour < 9 or hour >= 17:
            return True, ""
        return False, f"Within business hours — after-hours testing only. Current: {now.strftime('%H:%M')}"

    if testing_hours == "custom":
        custom = roe.get("custom_hours", "")
        # Attempt to parse "HH:MM-HH:MM" format
        if custom and "-" in custom:
            try:
                start_str, end_str = custom.split("-", 1)
                sh, sm = map(int, start_str.strip().split(":"))
                eh, em = map(int, end_str.strip().split(":"))
                start_min = sh * 60 + sm
                end_min = eh * 60 + em
                cur_min = hour * 60 + now.minute
                if start_min <= cur_min < end_min:
                    return True, ""
                return False, f"Outside custom window ({custom}). Current: {now.strftime('%H:%M')}"
            except ValueError:
                pass
        return True, f"Custom hours defined but could not parse: '{custom}'"

    return True, ""


def run_check(target: str, engagement: dict, action: str | None = None) -> dict:
    """
    Run a full scope check on a single target.
    Returns a result dict with verdict, matched_entry, restrictions, etc.
    """
    scope = engagement.get("scope", {})
    in_scope = scope.get("in_scope", {})
    out_scope = scope.get("out_of_scope", {})
    roe = engagement.get("rules_of_engagement", {})
    tz = engagement.get("authorization", {}).get("timezone", "")

    target_type, normalized = classify_target(target)

    result = {
        "target": target,
        "target_type": target_type,
        "normalized": normalized,
        "verdict": "AMBIGUOUS",
        "matched_entry": "",
        "restrictions": [],
        "action_allowed": True,
        "timing_ok": True,
        "reason": "",
    }

    # --- Action-only targets (free-text descriptions) ---
    if target_type == "action":
        action_ok, action_restrictions = check_action_restrictions(normalized, roe)
        result["action_allowed"] = action_ok
        result["restrictions"] = action_restrictions
        result["verdict"] = "IN_SCOPE" if action_ok else "AMBIGUOUS"
        result["reason"] = "Action checked against RoE" if action_ok else "Action conflicts with RoE"
        result["matched_entry"] = "rules_of_engagement"
        return result

    # --- Step 1: Out-of-scope check (precedence) ---
    oos_match, oos_entry = check_out_of_scope(target_type, normalized, out_scope)
    if oos_match:
        result["verdict"] = "OUT_OF_SCOPE"
        result["matched_entry"] = oos_entry
        result["reason"] = f"Target {normalized} matches out-of-scope entry"
        result["action_allowed"] = False
        return result

    # --- Step 2: In-scope check ---
    is_match, is_entry = check_in_scope(target_type, normalized, in_scope)
    if is_match:
        result["verdict"] = "IN_SCOPE"
        result["matched_entry"] = is_entry
        result["reason"] = f"Target {normalized} matches in-scope entry"

        # Check action restrictions
        if action:
            action_ok, action_restrictions = check_action_restrictions(action, roe)
            result["action_allowed"] = action_ok
            result["restrictions"].extend(action_restrictions)
            if not action_ok:
                result["verdict"] = "AMBIGUOUS"
                result["reason"] += " but action restricted by RoE"

        # Check timing
        timing_ok, timing_msg = check_timing(roe, tz)
        result["timing_ok"] = timing_ok
        if not timing_ok:
            result["restrictions"].append(timing_msg)

        return result

    # --- Step 3: No match — AMBIGUOUS ---
    result["verdict"] = "AMBIGUOUS"
    result["reason"] = f"Target {normalized} not found in any scope definition"
    return result


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_check(args: argparse.Namespace) -> None:
    """Single target scope check."""
    eng = load_engagement(args.engagement)
    result = run_check(args.target, eng, args.action)
    print(json.dumps(result, indent=2))
    _exit_for_verdict(result["verdict"])


def cmd_bulk(args: argparse.Namespace) -> None:
    """Bulk scope check from a file of targets."""
    eng = load_engagement(args.engagement)
    targets_path = Path(args.targets)
    if not targets_path.exists():
        _die(f"Targets file not found: {args.targets}")

    with open(targets_path, "r", encoding="utf-8") as f:
        targets = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    results = []
    for t in targets:
        results.append(run_check(t, eng))

    print(json.dumps(results, indent=2))

    # Exit code: worst verdict wins
    verdicts = {r["verdict"] for r in results}
    if "OUT_OF_SCOPE" in verdicts:
        sys.exit(1)
    elif "AMBIGUOUS" in verdicts:
        sys.exit(2)
    sys.exit(0)


def cmd_summary(args: argparse.Namespace) -> None:
    """Print engagement scope summary."""
    eng = load_engagement(args.engagement)
    scope = eng.get("scope", {})
    in_s = scope.get("in_scope", {})
    out_s = scope.get("out_of_scope", {})
    roe = eng.get("rules_of_engagement", {})

    def _count(section: dict) -> int:
        total = 0
        for k, v in section.items():
            if k == "notes":
                continue
            if isinstance(v, list):
                total += len(v)
        return total

    restrictions = []
    if not roe.get("social_engineering_allowed", False):
        restrictions.append("social_engineering: denied")
    if not roe.get("physical_access_allowed", False):
        restrictions.append("physical_access: denied")
    if not roe.get("dos_testing_allowed", False):
        restrictions.append("dos_testing: denied")
    if not roe.get("data_exfiltration_allowed", False):
        restrictions.append("data_exfiltration: denied")
    if not roe.get("production_systems", False):
        restrictions.append("production_systems: denied")

    summary = {
        "engagement_id": eng.get("id", "unknown"),
        "engagement_type": eng.get("type", "unknown"),
        "status": eng.get("status", "unknown"),
        "in_scope_count": _count(in_s),
        "out_of_scope_count": _count(out_s),
        "testing_hours": roe.get("testing_hours", "any"),
        "max_impact_level": roe.get("max_impact_level", "high"),
        "restrictions": restrictions,
        "in_scope_breakdown": {
            k: len(v) if isinstance(v, list) else 0
            for k, v in in_s.items() if k != "notes"
        },
        "out_of_scope_breakdown": {
            k: len(v) if isinstance(v, list) else 0
            for k, v in out_s.items() if k != "notes"
        },
    }
    print(json.dumps(summary, indent=2))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _die(msg: str) -> None:
    """Print error JSON and exit with code 3."""
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(3)


def _exit_for_verdict(verdict: str) -> None:
    """Map verdict string to process exit code."""
    code = {"IN_SCOPE": 0, "OUT_OF_SCOPE": 1, "AMBIGUOUS": 2}.get(verdict, 3)
    sys.exit(code)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="scope-enforcer",
        description="SPECTRA Scope Enforcer — programmatic scope verification",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- check --
    p_check = sub.add_parser("check", help="Check a single target against engagement scope")
    p_check.add_argument("--target", required=True, help="Target to verify (IP, domain, URL, etc.)")
    p_check.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_check.add_argument("--action", default=None, help="Action type (recon, scanning, exploitation, etc.)")

    # -- bulk --
    p_bulk = sub.add_parser("bulk", help="Bulk-check targets from a file")
    p_bulk.add_argument("--targets", required=True, help="Path to file with one target per line")
    p_bulk.add_argument("--engagement", required=True, help="Path to engagement.yaml")

    # -- summary --
    p_summary = sub.add_parser("summary", help="Print engagement scope summary")
    p_summary.add_argument("--engagement", required=True, help="Path to engagement.yaml")

    args = parser.parse_args()

    dispatch = {
        "check": cmd_check,
        "bulk": cmd_bulk,
        "summary": cmd_summary,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
