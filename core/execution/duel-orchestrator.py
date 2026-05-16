#!/usr/bin/env python3
"""SPECTRA Duel Mode runtime.

Duel Mode separates Red, Blue, and Referee views for Red/Blue exercises. It
records role-local JSONL ledgers and scores Red activity against Blue detection
or mitigation events. The runtime is intentionally plan/ledger based: it does
not provide log deletion, audit tampering, or destructive cleanup procedures.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


ROLES = {"red", "blue", "referee"}
RED_EVENT_TYPES = {"planned_action", "action", "observation", "handoff"}
BLUE_EVENT_TYPES = {"observation", "detection", "mitigation", "miss", "handoff"}
REFEREE_EVENT_TYPES = {"checkpoint", "correlation", "decision", "score"}

SAFETY_CONTRACT = {
    "mode": "ledger_only",
    "requires_engagement_scope": True,
    "red_allowed": [
        "low-and-slow activity planning within RoE",
        "telemetry footprint measurement",
        "attribution challenge design",
        "noise budget tracking",
    ],
    "red_forbidden": [
        "log deletion",
        "audit trail tampering",
        "destructive cleanup",
        "unauthorized persistence",
        "EDR/SIEM disabling instructions",
    ],
    "blue_allowed": [
        "live telemetry ingestion",
        "detection validation",
        "mitigation recommendation",
        "authorized active defense",
    ],
}

FORBIDDEN_PATTERNS = [
    r"\b(clear|delete|erase|wipe|remove)\s+(the\s+)?(logs?|audit|history|events?)\b",
    r"\b(log|audit|event)\s+(tamper|tampering|deletion|wiping)\b",
    r"\bdisable\s+(edr|siem|auditd|logging|sysmon|defender)\b",
    r"\bturn\s+off\s+(edr|siem|auditd|logging|sysmon|defender)\b",
    r"\bkill\s+(edr|siem|auditd|sysmon|defender)\b",
]


@dataclass
class DuelEvent:
    id: str
    session_id: str
    role: str
    event_type: str
    summary: str
    timestamp: str
    target: str = ""
    technique: str = ""
    source: str = ""
    confidence: str = "medium"
    severity: str = "medium"
    red_event_id: str = ""
    artifacts: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "role": self.role,
            "event_type": self.event_type,
            "summary": self.summary,
            "timestamp": self.timestamp,
            "target": self.target,
            "technique": self.technique,
            "source": self.source,
            "confidence": self.confidence,
            "severity": self.severity,
            "red_event_id": self.red_event_id,
            "artifacts": self.artifacts or [],
        }


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_output_root(project_root: Path | None = None) -> Path:
    root = project_root or Path.cwd()
    return root / "_spectra-output" / "duel"


def role_event_types(role: str) -> set[str]:
    if role == "red":
        return RED_EVENT_TYPES
    if role == "blue":
        return BLUE_EVENT_TYPES
    if role == "referee":
        return REFEREE_EVENT_TYPES
    return set()


def role_dir(output_root: Path, session_id: str, role: str) -> Path:
    return output_root / session_id / role


def ledger_path(output_root: Path, session_id: str, role: str) -> Path:
    suffix = {
        "red": "red-events.jsonl",
        "blue": "blue-events.jsonl",
        "referee": "referee-ledger.jsonl",
    }[role]
    return role_dir(output_root, session_id, role) / suffix


def validate_role(role: str):
    if role not in ROLES:
        raise ValueError(f"invalid role: {role}; expected one of {sorted(ROLES)}")


def validate_event_type(role: str, event_type: str):
    allowed = role_event_types(role)
    if event_type not in allowed:
        raise ValueError(f"invalid {role} event type: {event_type}; expected one of {sorted(allowed)}")


def check_red_safety(summary: str, event_type: str):
    text = f"{event_type} {summary}".lower()
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, text):
            raise ValueError(
                "Duel Mode blocks log deletion, audit tampering, destructive cleanup, and security-tool disabling. "
                "Record OPSEC goals as noise/footprint constraints instead."
            )


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.is_file() or yaml is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def write_yaml(path: Path, data: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    if yaml is not None:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    else:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def init_session(session_id: str, role: str, output_root: Path, engagement: str = "") -> dict[str, Any]:
    validate_role(role)
    rdir = role_dir(output_root, session_id, role)
    rdir.mkdir(parents=True, exist_ok=True)
    ledger = ledger_path(output_root, session_id, role)
    if not ledger.exists():
        ledger.write_text("", encoding="utf-8")
    state = {
        "schema_version": "0.1",
        "session_id": session_id,
        "role": role,
        "engagement": engagement,
        "created_at": now_utc(),
        "ledger": str(ledger),
        "safety_contract": SAFETY_CONTRACT,
        "visibility": {
            "red": "Red sees own plan/actions and shared engagement scope only.",
            "blue": "Blue sees telemetry, alerts, controls, and own detections only.",
            "referee": "Referee may ingest both ledgers and produce scorecards.",
        }[role],
    }
    write_yaml(rdir / "duel-session.yaml", state)
    return state


def next_event_id(output_root: Path, session_id: str, role: str) -> str:
    prefix = {"red": "RED", "blue": "BLUE", "referee": "REF"}[role]
    count = len(load_events(ledger_path(output_root, session_id, role))) + 1
    return f"{prefix}-{count:04d}"


def append_event(output_root: Path, event: DuelEvent) -> dict[str, Any]:
    validate_role(event.role)
    validate_event_type(event.role, event.event_type)
    if event.role == "red":
        check_red_safety(event.summary, event.event_type)
    path = ledger_path(output_root, event.session_id, event.role)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")
    return {"status": "recorded", "ledger": str(path), "event": event.to_dict()}


def record_event(
    output_root: Path,
    session_id: str,
    role: str,
    event_type: str,
    summary: str,
    target: str = "",
    technique: str = "",
    source: str = "",
    confidence: str = "medium",
    severity: str = "medium",
    red_event_id: str = "",
    artifacts: list[str] | None = None,
) -> dict[str, Any]:
    event = DuelEvent(
        id=next_event_id(output_root, session_id, role),
        session_id=session_id,
        role=role,
        event_type=event_type,
        summary=summary,
        timestamp=now_utc(),
        target=target,
        technique=technique,
        source=source,
        confidence=confidence,
        severity=severity,
        red_event_id=red_event_id,
        artifacts=artifacts or [],
    )
    return append_event(output_root, event)


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        events.append(json.loads(line))
    return events


def parse_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def normalize_severity(value: str) -> str:
    severity = (value or "medium").strip().lower()
    if severity in {"critical", "high", "medium", "low", "info"}:
        return severity
    return "medium"


def calculate_average(values: list[int]) -> float | None:
    if not values:
        return None
    return round(sum(values) / len(values), 2)


def summarize_missed_by_technique(missed: list[dict[str, Any]]) -> dict[str, int]:
    summary: dict[str, int] = {}
    for item in missed:
        technique = item.get("technique") or "no-technique"
        summary[technique] = summary.get(technique, 0) + 1
    return dict(sorted(summary.items()))


def calculate_severity_coverage(
    red_actions: list[dict[str, Any]],
    matched_red_ids: set[str],
) -> dict[str, dict[str, float | int]]:
    coverage: dict[str, dict[str, float | int]] = {}
    for red in red_actions:
        severity = normalize_severity(red.get("severity", "medium"))
        bucket = coverage.setdefault(severity, {"total": 0, "detected": 0, "coverage_percent": 0.0})
        bucket["total"] = int(bucket["total"]) + 1
        if red.get("id") in matched_red_ids:
            bucket["detected"] = int(bucket["detected"]) + 1

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    for bucket in coverage.values():
        total = int(bucket["total"])
        detected = int(bucket["detected"])
        bucket["coverage_percent"] = round((detected / total) * 100, 2) if total else 0.0
    return dict(sorted(coverage.items(), key=lambda item: order.get(item[0], 99)))


def calculate_outcome_grade(
    detection_rate: float,
    mitigation_rate: float,
    missed: list[dict[str, Any]],
    average_latency_seconds: float | None,
) -> dict[str, str]:
    missed_severities = {normalize_severity(item.get("severity", "medium")) for item in missed}
    has_critical_miss = "critical" in missed_severities
    has_high_miss = "high" in missed_severities
    if detection_rate >= 90 and mitigation_rate >= 50 and not has_critical_miss and not has_high_miss:
        grade = "A"
        rationale = "Strong detection coverage with meaningful mitigation and no high-severity misses."
    elif detection_rate >= 75 and not has_critical_miss:
        grade = "B"
        rationale = "Good detection coverage with no critical misses."
    elif detection_rate >= 50:
        grade = "C"
        rationale = "Partial coverage; Blue saw at least half of Red actions."
    elif detection_rate > 0:
        grade = "D"
        rationale = "Limited coverage; Blue saw some Red activity but missed most actions."
    else:
        grade = "F"
        rationale = "No Red actions were detected or mitigated."

    if average_latency_seconds is None:
        latency_note = "No latency baseline available."
    else:
        latency_note = f"Average detection latency was {average_latency_seconds} seconds."
    return {"grade": grade, "rationale": f"{rationale} {latency_note}"}


def events_match(red: dict[str, Any], blue: dict[str, Any]) -> bool:
    if blue.get("red_event_id") and blue.get("red_event_id") == red.get("id"):
        return True
    red_tech = (red.get("technique") or "").lower()
    blue_tech = (blue.get("technique") or "").lower()
    red_target = (red.get("target") or "").lower()
    blue_target = (blue.get("target") or "").lower()
    if red_tech and blue_tech and red_tech == blue_tech:
        if not red_target or not blue_target or red_target == blue_target:
            return True
    return False


def score_duel(red_events: list[dict[str, Any]], blue_events: list[dict[str, Any]]) -> dict[str, Any]:
    red_actions = [e for e in red_events if e.get("event_type") in {"planned_action", "action"}]
    blue_detections = [e for e in blue_events if e.get("event_type") in {"detection", "mitigation"}]
    matched: list[dict[str, Any]] = []
    missed: list[dict[str, Any]] = []

    for red in red_actions:
        matches = [blue for blue in blue_detections if events_match(red, blue)]
        if matches:
            first = sorted(matches, key=lambda e: e.get("timestamp", ""))[0]
            latency_seconds = None
            rt = parse_time(red.get("timestamp", ""))
            bt = parse_time(first.get("timestamp", ""))
            if rt and bt:
                latency_seconds = max(0, int((bt - rt).total_seconds()))
            matched.append({
                "red_event_id": red.get("id"),
                "blue_event_id": first.get("id"),
                "technique": red.get("technique"),
                "target": red.get("target"),
                "severity": normalize_severity(red.get("severity", "medium")),
                "blue_event_type": first.get("event_type"),
                "latency_seconds": latency_seconds,
            })
        else:
            missed.append({
                "red_event_id": red.get("id"),
                "technique": red.get("technique"),
                "target": red.get("target"),
                "severity": normalize_severity(red.get("severity", "medium")),
                "summary": red.get("summary"),
            })

    total = len(red_actions)
    detected = len(matched)
    mitigated = len([m for m in matched if m.get("blue_event_type") == "mitigation"])
    detection_rate = round((detected / total) * 100, 2) if total else 0.0
    mitigation_rate = round((mitigated / total) * 100, 2) if total else 0.0
    latency_values = [m["latency_seconds"] for m in matched if isinstance(m.get("latency_seconds"), int)]
    first_detection_latency = min(latency_values) if latency_values else None
    average_detection_latency = calculate_average(latency_values)
    matched_red_ids = {str(m.get("red_event_id")) for m in matched if m.get("red_event_id")}
    severity_coverage = calculate_severity_coverage(red_actions, matched_red_ids)
    missed_by_technique = summarize_missed_by_technique(missed)
    outcome = calculate_outcome_grade(detection_rate, mitigation_rate, missed, average_detection_latency)
    return {
        "schema_version": "0.1",
        "generated_at": now_utc(),
        "summary": {
            "red_actions": total,
            "blue_detections_or_mitigations": detected,
            "blue_mitigations": mitigated,
            "missed": len(missed),
            "detection_rate_percent": detection_rate,
            "mitigation_rate_percent": mitigation_rate,
            "first_detection_latency_seconds": first_detection_latency,
            "average_detection_latency_seconds": average_detection_latency,
            "outcome_grade": outcome["grade"],
        },
        "severity_coverage": severity_coverage,
        "missed_by_technique": missed_by_technique,
        "outcome": outcome,
        "matched": matched,
        "missed": missed,
    }


def render_scorecard(score: dict[str, Any]) -> str:
    s = score["summary"]
    lines = [
        "# SPECTRA Duel Scorecard",
        "",
        f"Generated: {score['generated_at']}",
        "",
        "## Summary",
        "",
        f"- Red actions: {s['red_actions']}",
        f"- Blue detections/mitigations: {s['blue_detections_or_mitigations']}",
        f"- Blue mitigations: {s['blue_mitigations']}",
        f"- Missed actions: {s['missed']}",
        f"- Detection rate: {s['detection_rate_percent']}%",
        f"- Mitigation rate: {s['mitigation_rate_percent']}%",
        f"- First detection latency: {s.get('first_detection_latency_seconds')}",
        f"- Average detection latency: {s.get('average_detection_latency_seconds')}",
        f"- Outcome grade: {s.get('outcome_grade')}",
        "",
        "## Severity Coverage",
        "",
    ]
    for severity, data in score.get("severity_coverage", {}).items():
        lines.append(
            f"- {severity}: {data.get('detected', 0)}/{data.get('total', 0)} "
            f"({data.get('coverage_percent', 0.0)}%)"
        )
    if not score.get("severity_coverage"):
        lines.append("- None")
    lines.extend([
        "",
        "## Missed By Technique",
        "",
    ])
    for technique, count in score.get("missed_by_technique", {}).items():
        lines.append(f"- {technique}: {count}")
    if not score.get("missed_by_technique"):
        lines.append("- None")
    lines.extend([
        "",
        "## Matched",
        "",
    ])
    for item in score["matched"]:
        lines.append(
            f"- {item['red_event_id']} -> {item['blue_event_id']} "
            f"({item.get('technique') or 'no-technique'}, {item.get('target') or 'no-target'}, "
            f"latency={item.get('latency_seconds')})"
        )
    if not score["matched"]:
        lines.append("- None")
    lines.extend(["", "## Missed", ""])
    for item in score["missed"]:
        lines.append(
            f"- {item['red_event_id']} ({item.get('technique') or 'no-technique'}, "
            f"{item.get('target') or 'no-target'}): {item.get('summary')}"
        )
    if not score["missed"]:
        lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def build_status(output_root: Path, session_id: str) -> dict[str, Any]:
    status = {"session_id": session_id, "roles": {}}
    for role in sorted(ROLES):
        ledger = ledger_path(output_root, session_id, role)
        state = role_dir(output_root, session_id, role) / "duel-session.yaml"
        status["roles"][role] = {
            "initialized": state.is_file(),
            "ledger": str(ledger),
            "events": len(load_events(ledger)),
        }
    return status


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run SPECTRA Duel Mode session, ledger, and scoring commands.")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Initialize a role-local Duel Mode session")
    init_cmd.add_argument("--session", required=True)
    init_cmd.add_argument("--role", choices=sorted(ROLES), required=True)
    init_cmd.add_argument("--output-root", type=Path, required=True)
    init_cmd.add_argument("--engagement", default="")

    record_cmd = sub.add_parser("record", help="Append an event to a role-local Duel Mode ledger")
    record_cmd.add_argument("--session", required=True)
    record_cmd.add_argument("--role", choices=sorted(ROLES), required=True)
    record_cmd.add_argument("--event-type", required=True)
    record_cmd.add_argument("--summary", required=True)
    record_cmd.add_argument("--output-root", type=Path, required=True)
    record_cmd.add_argument("--target", default="")
    record_cmd.add_argument("--technique", default="")
    record_cmd.add_argument("--source", default="")
    record_cmd.add_argument("--confidence", default="medium")
    record_cmd.add_argument("--severity", default="medium")
    record_cmd.add_argument("--red-event-id", default="")
    record_cmd.add_argument("--artifact", action="append", default=[])

    score_cmd = sub.add_parser("score", help="Score Red events against Blue detection/mitigation events")
    score_cmd.add_argument("--session", default="")
    score_cmd.add_argument("--red", type=Path, required=True)
    score_cmd.add_argument("--blue", type=Path, required=True)
    score_cmd.add_argument("--format", choices=("json", "markdown"), default="markdown")
    score_cmd.add_argument("--output", type=Path, default=None)

    status_cmd = sub.add_parser("status", help="Show Duel Mode role initialization and event counts")
    status_cmd.add_argument("--session", required=True)
    status_cmd.add_argument("--output-root", type=Path, required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = init_session(args.session, args.role, args.output_root, args.engagement)
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "record":
            result = record_event(
                output_root=args.output_root,
                session_id=args.session,
                role=args.role,
                event_type=args.event_type,
                summary=args.summary,
                target=args.target,
                technique=args.technique,
                source=args.source,
                confidence=args.confidence,
                severity=args.severity,
                red_event_id=args.red_event_id,
                artifacts=args.artifact,
            )
            print(json.dumps(result, indent=2))
            return 0
        if args.command == "score":
            score = score_duel(load_events(args.red), load_events(args.blue))
            content = json.dumps(score, indent=2) if args.format == "json" else render_scorecard(score)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(content + "\n", encoding="utf-8")
            else:
                print(content)
            return 0
        if args.command == "status":
            print(json.dumps(build_status(args.output_root, args.session), indent=2))
            return 0
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
