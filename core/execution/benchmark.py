#!/usr/bin/env python3
"""SPECTRA Benchmark Harness (Layer 3 — deterministic execution).

Turns SPECTRA's "it works" claim into reproducible, evidence-backed proof. A
benchmark SUITE declares cases with ground truth: a target, an allowlisted tool,
optional args, and the expected observations (markers the tool output should
contain). The harness runs each case through the scope+RoE-gated tool adapter,
scores the actual output against the expected markers, and produces a
deterministic scorecard with a grade.

SPECTRA-native and honest:

  * Reproducible. Scoring is deterministic marker matching, not LLM judgement.
    Same suite + same target -> same scorecard. Run logs are the evidence.
  * Authorized-only. Every case runs through the tool adapter, so scope, RoE,
    the flag allowlist, and the destructive HARD BLOCK all apply — a benchmark
    cannot scan out of scope.
  * No inflation. A missed expectation is a gap, reported as such; a blocked or
    unavailable case is reported honestly, never silently counted as a pass.

It does not execute anything itself — it composes the tool adapter (Goal 4),
which composes scope-enforcer. Use --dry-run to gate and preview without running.

CLI:
  benchmark.py run --suite suite.yaml --engagement e.yaml [--dry-run] [--output report.json]
"""

from __future__ import annotations

import argparse
import contextlib
import importlib.util
import json
import re
import signal
import sys
from pathlib import Path
from typing import Any

REGEX_TIMEOUT_SECONDS = 2


@contextlib.contextmanager
def _regex_time_limit(seconds: int):
    """Best-effort ReDoS guard. Uses SIGALRM on the Unix main thread; on other
    platforms or worker threads it yields without a limit (graceful fallback)."""
    try:
        previous = signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError()))
    except (ValueError, AttributeError):
        yield  # not the main thread, or no SIGALRM (e.g. Windows)
        return
    prior_remaining = signal.alarm(seconds)  # returns any pending alarm's seconds
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
        if prior_remaining > 0:  # restore a pre-existing alarm we interrupted
            signal.alarm(prior_remaining)

try:
    import yaml
except ImportError:  # pragma: no cover
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)


def _load_tool_adapter():
    script = Path(__file__).resolve().with_name("tool-adapter.py")
    spec = importlib.util.spec_from_file_location("tool_adapter", script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load tool adapter: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tool_adapter = _load_tool_adapter()


# ---------------------------------------------------------------------------
# Suite loading
# ---------------------------------------------------------------------------

def load_suite(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Benchmark suite not found: {path}")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Invalid suite: 'cases' must be a non-empty list")
    seen_ids: set[str] = set()
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise ValueError(f"Invalid suite: case[{index}] must be a mapping")
        cid = str(case.get("id", "")).strip()
        if not cid:
            raise ValueError(f"Invalid suite: case[{index}] is missing a non-empty 'id'")
        if cid in seen_ids:
            raise ValueError(f"Invalid suite: duplicate case id {cid!r}")
        seen_ids.add(cid)
        if not str(case.get("tool", "")).strip():
            raise ValueError(f"Invalid suite: {cid} is missing 'tool'")
        if not str(case.get("target", "")).strip():
            raise ValueError(f"Invalid suite: {cid} is missing 'target'")
        args = case.get("args")
        if args is not None and not (isinstance(args, list)
                                     and all(isinstance(a, (str, int, float)) for a in args)):
            raise ValueError(f"Invalid suite: {cid} 'args' must be a list of scalars")
        expect = case.get("expect")
        if not isinstance(expect, list) or not expect:
            raise ValueError(f"Invalid suite: {cid} must have a non-empty 'expect' list")
        for exp in expect:
            if not isinstance(exp, dict) or not str(exp.get("match", "")).strip():
                raise ValueError(f"Invalid suite: {cid} each 'expect' entry needs a non-empty 'match'")
            if "name" in exp and not isinstance(exp["name"], str):
                raise ValueError(f"Invalid suite: {cid} 'expect.name' must be a string")
    return data


# ---------------------------------------------------------------------------
# Scoring (pure — independent of execution)
# ---------------------------------------------------------------------------

def _marker_matches(match: str, text: str) -> bool:
    """A marker matches by substring, or by regex when prefixed with 're:'.

    Regex markers come from the (operator-authored) suite; a ReDoS guard bounds
    catastrophic backtracking so a bad pattern cannot hang the harness.
    """
    if match.startswith("re:"):
        try:
            with _regex_time_limit(REGEX_TIMEOUT_SECONDS):
                return re.search(match[3:], text) is not None
        except (re.error, TimeoutError):
            return False
    return match in text


def score_case(case: dict[str, Any], actual_text: str) -> dict[str, Any]:
    """Score one case's expected markers against captured output."""
    expectations = case.get("expect", []) or []
    matched: list[str] = []
    missed: list[str] = []
    for exp in expectations:
        name = str(exp.get("name", exp.get("match", "")))
        match = str(exp.get("match", ""))
        if match and _marker_matches(match, actual_text):
            matched.append(name)
        else:
            missed.append(name)
    total = len(expectations)
    return {
        "expected_count": total,
        "matched": matched,
        "missed": missed,
        "passed": total > 0 and not missed,
    }


def grade_suite(scorecards: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate scored cases into a deterministic grade.

    Pass rate is over SCORABLE cases (executed and scored); blocked/unavailable
    cases are reported separately and never count as passes.
    """
    scorable = [s for s in scorecards if s["status"] == "scored"]
    passed = [s for s in scorable if s["score"]["passed"]]
    not_scored = [s for s in scorecards if s["status"] != "scored"]
    # Grade on the RAW rate; round only for display so a rounded value cannot
    # inflate a case across a threshold.
    raw_rate = (len(passed) / len(scorable)) * 100 if scorable else 0.0
    pass_rate = round(raw_rate, 2)

    if not scorable:
        grade, rationale = "N/A", "No scorable cases (all blocked, unavailable, or planned)."
    elif raw_rate >= 90.0:
        grade, rationale = "A", "Strong coverage: expectations met across the suite."
    elif raw_rate >= 75.0:
        grade, rationale = "B", "Good coverage: most expectations met."
    elif raw_rate >= 50.0:
        grade, rationale = "C", "Partial coverage: at least half of expectations met."
    elif passed:
        grade, rationale = "D", "Limited coverage: some expectations met."
    else:
        grade, rationale = "F", "No expectations met."

    return {
        "cases_total": len(scorecards),
        "cases_scored": len(scorable),
        "cases_passed": len(passed),
        "cases_not_scored": len(not_scored),
        "pass_rate_percent": pass_rate,
        "grade": grade,
        "rationale": rationale,
    }


# ---------------------------------------------------------------------------
# Running
# ---------------------------------------------------------------------------

def run_case(case: dict[str, Any], engagement_path: str, dry_run: bool,
             timeout: int) -> dict[str, Any]:
    """Run one case through the gated tool adapter and score it."""
    case_id = str(case.get("id", "case"))
    tool = str(case.get("tool", ""))
    target = str(case.get("target", ""))
    args = [str(a) for a in (case.get("args") or [])]

    record: dict[str, Any] = {"id": case_id, "tool": tool, "target": target}
    try:
        result = tool_adapter.run(engagement_path, tool, target,
                                  extra_args=args, dry_run=dry_run, timeout=timeout)
    except (KeyError, FileNotFoundError, ValueError, RuntimeError) as exc:
        record["status"] = "error"
        record["error"] = str(exc)
        return record

    adapter_status = result.get("status")
    record["adapter_status"] = adapter_status

    if adapter_status == "planned":
        record["status"] = "planned"
    elif adapter_status == "blocked":
        record["status"] = "blocked"
        record["errors"] = result.get("gate", {}).get("errors", [])
    elif adapter_status == "unavailable":
        record["status"] = "unavailable"
        record["error"] = result.get("error", "")
    elif adapter_status == "executed":
        execution = result.get("execution", {}) or {}
        # A tool that timed out or exited non-zero did not produce a trustworthy
        # result — it is an error, not a (possibly false) pass.
        if execution.get("timed_out") or execution.get("exit_code") not in (0, None):
            record["status"] = "error"
            record["error"] = (f"tool exit_code={execution.get('exit_code')} "
                               f"timed_out={execution.get('timed_out')}")
            record["stderr"] = (execution.get("stderr", "") or "")[:500]
        else:
            actual = execution.get("stdout", "") or ""
            record["status"] = "scored"
            record["score"] = score_case(case, actual)
    else:
        record["status"] = "error"
        record["error"] = f"unexpected adapter status: {adapter_status}"
    return record


def run_suite(suite_path: str, engagement_path: str, dry_run: bool = False,
              timeout: int = 300) -> dict[str, Any]:
    suite = load_suite(suite_path)
    cards = [run_case(c, engagement_path, dry_run, timeout) for c in suite["cases"]]
    return {
        "suite": suite.get("suite", Path(suite_path).stem),
        "engagement": engagement_path,
        "dry_run": dry_run,
        "cases": cards,
        "summary": grade_suite(cards),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_run(args: argparse.Namespace) -> None:
    try:
        report = run_suite(args.suite, args.engagement, dry_run=args.dry_run, timeout=args.timeout)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps({"status": "written", "output": str(out.resolve()),
                          "summary": report["summary"]}, indent=2))
    else:
        print(json.dumps(report, indent=2))
    # Exit non-zero if any scored case failed OR any case errored (CI gating).
    failed = any(
        c["status"] == "error" or (c["status"] == "scored" and not c["score"]["passed"])
        for c in report["cases"]
    )
    sys.exit(1 if failed else 0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="benchmark.py",
        description="Run a reproducible SPECTRA capability benchmark (scope+RoE gated).",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p_run = sub.add_parser("run", help="Run a benchmark suite against an engagement")
    p_run.add_argument("--suite", required=True, help="Path to the benchmark suite YAML")
    p_run.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_run.add_argument("--dry-run", action="store_true", help="Gate and preview; execute nothing")
    p_run.add_argument("--timeout", type=int, default=300)
    p_run.add_argument("--output", help="Write the scorecard JSON here")
    p_run.set_defaults(func=cmd_run)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
