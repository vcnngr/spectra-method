#!/usr/bin/env python3
"""SPECTRA Noise-Budget Validator (Layer 3 — deterministic execution).

A SPECTRA engagement may declare a noise budget: the authorized timing and
footprint envelope for Red activity. This is planning and honest-measurement
only — it bounds how much signal an engagement may produce, never how to hide.
SPECTRA's
expected result is never "invisible Red"; it is an honest measurement of which
signals were produced, seen, and missed.

This validator checks that a declared noise budget is internally coherent before
Red activity begins, so an operator does not, for example, declare a low_footprint
profile while authorizing hundreds of actions per hour. It is read-only and
never throttles, schedules, or executes anything — it only reports.

Severity:
  FAIL  — the budget is invalid or self-contradictory (e.g. negative values).
  WARN  — the budget is internally inconsistent (e.g. low_footprint profile + a
          high rate); the operator should reconcile it but may proceed.
  INFO  — an advisory the operator may want to consider.

Absence of a noise budget is NOT an error — it is reported as budget_present=false
with status PASS, so existing engagements remain valid.

CLI:
  noise-budget.py check --engagement engagement.yaml
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only without pyyaml
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


# Profiles are named for measurable FOOTPRINT, not for evasion: SPECTRA models
# how much signal authorized activity produces, never how to hide it.
VALID_PROFILES = ("low_footprint", "balanced", "high_footprint")
VALID_TOLERANCE = ("low", "medium", "high")

# A "low_footprint" engagement authorizing more than this many actions/hour is
# almost certainly mislabeled — flagged as inconsistent, not blocked.
LOW_FOOTPRINT_RATE_CEILING = 30

# Non-negative integer fields (max_concurrent_actions has its own >=1 rule).
_NONNEG_INT_FIELDS = ("max_actions_per_hour", "min_action_interval_seconds")


def load_engagement(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Engagement file not found: {path}")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if "engagement" not in data:
        raise ValueError("Invalid engagement file: missing 'engagement' root key")
    return data


def _issue(severity: str, code: str, message: str) -> dict[str, str]:
    return {"severity": severity, "code": code, "message": message}


def _coerce_int(value: Any) -> int | None:
    if isinstance(value, bool):  # bool is an int subclass — reject explicitly
        return None
    if isinstance(value, int):
        return value
    return None


def validate_noise_budget(roe: dict[str, Any]) -> dict[str, Any]:
    """Validate the noise_budget block of a rules_of_engagement mapping."""
    budget = (roe or {}).get("noise_budget")
    if budget is None:
        return {"status": "PASS", "budget_present": False, "issues": []}
    if not isinstance(budget, dict):
        return {
            "status": "FAIL",
            "budget_present": True,
            "issues": [_issue("FAIL", "budget_type",
                              "noise_budget must be a mapping/object")],
        }

    issues: list[dict[str, str]] = []

    # A field present with an explicit null is a malformed budget — the schema
    # types reject null, so treat present-null as FAIL (distinct from absent).
    nullable_check = ("profile", "telemetry_tolerance", "max_actions_per_hour",
                      "min_action_interval_seconds", "max_concurrent_actions",
                      "abort_on_detection", "notes")
    for field in nullable_check:
        if field in budget and budget[field] is None:
            issues.append(_issue("FAIL", f"{field}_null",
                                 f"{field} is present but null; omit it or give a value"))

    profile = budget.get("profile")
    if profile is not None and profile not in VALID_PROFILES:
        issues.append(_issue("FAIL", "profile_invalid",
                             f"profile '{profile}' must be one of {', '.join(VALID_PROFILES)}"))

    tolerance = budget.get("telemetry_tolerance")
    if tolerance is not None and tolerance not in VALID_TOLERANCE:
        issues.append(_issue("FAIL", "tolerance_invalid",
                             f"telemetry_tolerance '{tolerance}' must be one of "
                             f"{', '.join(VALID_TOLERANCE)}"))

    # Numeric sanity.
    for field in _NONNEG_INT_FIELDS:
        if field in budget and budget[field] is not None:
            val = _coerce_int(budget[field])
            if val is None:
                issues.append(_issue("FAIL", f"{field}_type", f"{field} must be an integer"))
            elif val < 0:
                issues.append(_issue("FAIL", f"{field}_negative", f"{field} must be >= 0"))

    concurrent = budget.get("max_concurrent_actions")
    if concurrent is not None:
        cval = _coerce_int(concurrent)
        if cval is None:
            issues.append(_issue("FAIL", "max_concurrent_type",
                                 "max_concurrent_actions must be an integer"))
        elif cval < 1:
            issues.append(_issue("FAIL", "max_concurrent_invalid",
                                 "max_concurrent_actions must be >= 1"))

    abort = budget.get("abort_on_detection")
    if abort is not None and not isinstance(abort, bool):
        issues.append(_issue("FAIL", "abort_type", "abort_on_detection must be a boolean"))

    notes = budget.get("notes")
    if notes is not None and not isinstance(notes, str):
        issues.append(_issue("FAIL", "notes_type", "notes must be a string"))

    # --- Coherence (only when the relevant fields are valid) --------------
    rate = _coerce_int(budget.get("max_actions_per_hour"))
    interval = _coerce_int(budget.get("min_action_interval_seconds"))
    concurrent_val = _coerce_int(budget.get("max_concurrent_actions"))

    # Rate vs interval: a minimum spacing implies a maximum sustainable rate.
    if rate and interval and interval > 0:
        implied_max = 3600 // interval
        if rate > implied_max:
            issues.append(_issue(
                "WARN", "rate_exceeds_interval",
                f"max_actions_per_hour ({rate}) exceeds what "
                f"min_action_interval_seconds ({interval}s) permits (~{implied_max}/h)"))

    if profile == "low_footprint":
        if rate and rate > LOW_FOOTPRINT_RATE_CEILING:
            issues.append(_issue(
                "WARN", "low_footprint_high_rate",
                f"low_footprint profile with max_actions_per_hour={rate} "
                f"(> {LOW_FOOTPRINT_RATE_CEILING}) is inconsistent"))
        if tolerance == "high":
            issues.append(_issue(
                "WARN", "low_footprint_high_tolerance",
                "low_footprint profile with telemetry_tolerance=high is inconsistent"))
        if concurrent_val and concurrent_val > 1:
            issues.append(_issue(
                "WARN", "low_footprint_concurrency",
                f"low_footprint profile with max_concurrent_actions={concurrent_val} is inconsistent"))
        if budget.get("abort_on_detection") is not True:
            issues.append(_issue(
                "INFO", "low_footprint_no_abort",
                "low_footprint profile usually pairs with abort_on_detection=true"))

    if profile == "high_footprint" and tolerance == "low":
        issues.append(_issue(
            "WARN", "high_footprint_low_tolerance",
            "high_footprint profile with telemetry_tolerance=low is contradictory"))

    severities = {i["severity"] for i in issues}
    if "FAIL" in severities:
        status = "FAIL"
    elif "WARN" in severities:
        status = "WARN"
    else:
        status = "PASS"

    return {"status": status, "budget_present": True, "issues": issues}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_check(args: argparse.Namespace) -> None:
    try:
        doc = load_engagement(args.engagement)
    except (FileNotFoundError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)

    roe = (doc.get("engagement", {}) or {}).get("rules_of_engagement", {}) or {}
    result = validate_noise_budget(roe)
    result["engagement_id"] = (doc.get("engagement", {}) or {}).get("id", "")
    print(json.dumps(result, indent=2))
    # FAIL is the only blocking outcome by default; WARN/PASS exit 0 so it never
    # hard-stops an engagement over an advisory inconsistency. Pipelines that want
    # to treat inconsistencies as blocking can pass --fail-on-warn.
    blocking = result["status"] == "FAIL" or (args.fail_on_warn and result["status"] == "WARN")
    sys.exit(1 if blocking else 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="noise-budget.py",
        description="Validate a SPECTRA engagement noise budget for coherence (planning only).",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", help="Validate the noise_budget of an engagement")
    check.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    check.add_argument("--fail-on-warn", action="store_true",
                       help="Exit non-zero on WARN as well as FAIL")
    check.set_defaults(func=cmd_check)
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
