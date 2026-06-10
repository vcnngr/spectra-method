#!/usr/bin/env python3
"""SPECTRA Run Accounting (Layer 3).

Every gated tool invocation produces an operational record — what ran, against
what, with what outcome. This module maintains an append-only run log per
engagement and summarizes it, so an operator (or a report) can answer "what did
this engagement actually do?" without trawling shell history.

It is deliberately separate from the evidence chain: evidence is the *findings*
you stand behind; the run log is the *activity* you performed. The two serve
different audiences (the report reader vs. the engagement auditor).

Design:
  * Append-only JSONL next to engagement.yaml (`run-log.jsonl`).
  * A record is derived from a tool-adapter result dict, never from free input.
  * No shell, no network. Pure file accounting.

CLI:
  run-accounting.py record --engagement E [--result FILE]   # FILE or stdin
  run-accounting.py status --engagement E [--limit N]
  run-accounting.py path   --engagement E
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_NAME = "run-log.jsonl"


def run_log_path(engagement_path: str) -> Path:
    """The run log lives beside the engagement.yaml it accounts for."""
    return Path(engagement_path).resolve().parent / LOG_NAME


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _exit_code(result: dict[str, Any]) -> int | None:
    """Pull the process exit code out of a local or remote tool-adapter result."""
    status = result.get("status")
    if status == "executed":
        return result.get("execution", {}).get("exit_code")
    if status == "executed_remote":
        return result.get("remote", {}).get("execution", {}).get("exit_code")
    return None


def build_record(result: dict[str, Any], now: str | None = None) -> dict[str, Any]:
    """Reduce a tool-adapter result to a compact, stable accounting record."""
    rec: dict[str, Any] = {
        "ts": now or _utc_now_iso(),
        "tool": result.get("tool"),
        "target": result.get("target"),
        "status": result.get("status"),
        "via": result.get("via", "local"),
        "dry_run": bool(result.get("dry_run", False)),
        "exit_code": _exit_code(result),
    }
    if result.get("error"):
        rec["error"] = result["error"]
    return rec


def record(engagement_path: str, result: dict[str, Any],
           now: str | None = None) -> dict[str, Any]:
    """Append one run record for the engagement and return it."""
    rec = build_record(result, now=now)
    log = run_log_path(engagement_path)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")
    return rec


def read_log(engagement_path: str) -> list[dict[str, Any]]:
    """Read all records; silently skip blank or corrupt lines (append-only logs
    can be truncated mid-write — accounting should never crash on that)."""
    log = run_log_path(engagement_path)
    if not log.is_file():
        return []
    out: list[dict[str, Any]] = []
    for line in log.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        # Only accept object records; a valid-JSON scalar/array is corrupt for
        # our purposes and must not reach the summarizer's dict access.
        if isinstance(rec, dict):
            out.append(rec)
    return out


def summarize(engagement_path: str, limit: int = 10) -> dict[str, Any]:
    """Aggregate the run log into operational accounting."""
    records = read_log(engagement_path)
    by_status = Counter(r.get("status") for r in records)
    by_tool = Counter(r.get("tool") for r in records)
    executed = by_status.get("executed", 0) + by_status.get("executed_remote", 0)
    nonzero = sum(1 for r in records
                  if r.get("status") in ("executed", "executed_remote")
                  and r.get("exit_code") not in (0, None))
    return {
        "engagement": str(Path(engagement_path).resolve()),
        "log": str(run_log_path(engagement_path)),
        "total": len(records),
        "executed": executed,
        "blocked": by_status.get("blocked", 0),
        "planned": by_status.get("planned", 0),
        "nonzero_exit": nonzero,
        "by_status": dict(by_status),
        "by_tool": dict(by_tool),
        "first_ts": records[0].get("ts") if records else None,
        "last_ts": records[-1].get("ts") if records else None,
        "recent": records[-limit:][::-1] if limit > 0 else [],
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cmd_record(args: argparse.Namespace) -> None:
    raw = Path(args.result).read_text(encoding="utf-8") if args.result else sys.stdin.read()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"invalid result JSON: {exc}"}), file=sys.stderr)
        sys.exit(3)
    if not isinstance(result, dict):
        print(json.dumps({"error": "result must be a JSON object"}), file=sys.stderr)
        sys.exit(3)
    rec = record(args.engagement, result)
    print(json.dumps(rec, indent=2))
    sys.exit(0)


def cmd_status(args: argparse.Namespace) -> None:
    print(json.dumps(summarize(args.engagement, limit=args.limit), indent=2))
    sys.exit(0)


def cmd_path(args: argparse.Namespace) -> None:
    print(str(run_log_path(args.engagement)))
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="run-accounting.py",
        description="Per-engagement run log: record gated tool runs and summarize activity.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_rec = sub.add_parser("record", help="Append a run record from a tool-adapter result")
    p_rec.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_rec.add_argument("--result", help="Path to a result JSON file (default: read stdin)")
    p_rec.set_defaults(func=cmd_record)

    p_st = sub.add_parser("status", help="Summarize the engagement run log")
    p_st.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_st.add_argument("--limit", type=int, default=10, help="How many recent runs to include")
    p_st.set_defaults(func=cmd_status)

    p_pa = sub.add_parser("path", help="Print the run log path for an engagement")
    p_pa.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_pa.set_defaults(func=cmd_path)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
