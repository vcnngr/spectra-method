#!/usr/bin/env python3
"""SPECTRA Red/Blue ledger broker.

The broker moves Duel Mode ledgers between separated machines through explicit
JSON bundles. It is intentionally offline and file based: no daemon, no network
listener, no direct host control.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROLES = {"red", "blue", "referee"}
BUNDLE_TYPE = "spectra-duel-ledger"
SCHEMA_VERSION = "0.1"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
        if not isinstance(item, dict):
            raise ValueError(f"invalid event at {path}:{line_number}: expected object")
        events.append(item)
    return events


def write_events(path: Path, events: list[dict[str, Any]]):
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "".join(json.dumps(event, sort_keys=True) + "\n" for event in events)
    path.write_text(content, encoding="utf-8")


def canonical_events(events: list[dict[str, Any]]) -> str:
    return json.dumps(events, sort_keys=True, separators=(",", ":"))


def events_hash(events: list[dict[str, Any]]) -> str:
    return hashlib.sha256(canonical_events(events).encode("utf-8")).hexdigest()


def validate_event(event: dict[str, Any], session_id: str, role: str):
    if event.get("session_id") != session_id:
        raise ValueError(
            f"event {event.get('id', '<unknown>')} session mismatch: "
            f"{event.get('session_id')} != {session_id}"
        )
    if event.get("role") != role:
        raise ValueError(
            f"event {event.get('id', '<unknown>')} role mismatch: {event.get('role')} != {role}"
        )
    if not event.get("id") or not event.get("event_type") or not event.get("summary"):
        raise ValueError(f"event missing required fields: {event}")


def event_key(event: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(event.get("role", "")),
        str(event.get("id", "")),
        str(event.get("timestamp", "")),
        str(event.get("summary", "")),
    )


def export_bundle(output_root: Path, session_id: str, role: str, bundle_path: Path) -> dict[str, Any]:
    validate_role(role)
    ledger = ledger_path(output_root, session_id, role)
    events = load_events(ledger)
    for event in events:
        validate_event(event, session_id, role)

    bundle = {
        "schema_version": SCHEMA_VERSION,
        "bundle_type": BUNDLE_TYPE,
        "session_id": session_id,
        "role": role,
        "exported_at": now_utc(),
        "source_ledger": str(ledger),
        "event_count": len(events),
        "events_sha256": events_hash(events),
        "events": events,
    }
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "status": "exported",
        "bundle": str(bundle_path),
        "session_id": session_id,
        "role": role,
        "event_count": len(events),
        "events_sha256": bundle["events_sha256"],
    }


def load_bundle(bundle_path: Path) -> dict[str, Any]:
    try:
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid bundle JSON: {exc}") from exc
    if not isinstance(bundle, dict):
        raise ValueError("invalid bundle: expected object")
    if bundle.get("bundle_type") != BUNDLE_TYPE:
        raise ValueError(f"invalid bundle_type: {bundle.get('bundle_type')}")
    if bundle.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(f"unsupported schema_version: {bundle.get('schema_version')}")
    events = bundle.get("events")
    if not isinstance(events, list):
        raise ValueError("invalid bundle: events must be a list")
    if bundle.get("events_sha256") != events_hash(events):
        raise ValueError("invalid bundle: events_sha256 mismatch")
    if bundle.get("event_count") != len(events):
        raise ValueError("invalid bundle: event_count mismatch")
    return bundle


def import_bundle(output_root: Path, session_id: str, role: str, bundle_path: Path) -> dict[str, Any]:
    validate_role(role)
    bundle = load_bundle(bundle_path)
    if bundle.get("session_id") != session_id:
        raise ValueError(f"bundle session mismatch: {bundle.get('session_id')} != {session_id}")
    if bundle.get("role") != role:
        raise ValueError(f"bundle role mismatch: {bundle.get('role')} != {role}")

    incoming = bundle["events"]
    for event in incoming:
        validate_event(event, session_id, role)

    ledger = ledger_path(output_root, session_id, role)
    existing = load_events(ledger)
    existing_keys = {event_key(event) for event in existing}
    imported = [event for event in incoming if event_key(event) not in existing_keys]
    merged = existing + imported
    write_events(ledger, merged)

    imports_dir = output_root / session_id / "imports"
    imports_dir.mkdir(parents=True, exist_ok=True)
    marker = imports_dir / f"{role}-{bundle_path.name}"
    marker.write_text(json.dumps(bundle, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return {
        "status": "imported",
        "bundle": str(bundle_path),
        "ledger": str(ledger),
        "session_id": session_id,
        "role": role,
        "imported": len(imported),
        "skipped_duplicates": len(incoming) - len(imported),
        "total_events": len(merged),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export/import SPECTRA Duel Mode ledgers as offline bundles.")
    sub = parser.add_subparsers(dest="command", required=True)

    export_cmd = sub.add_parser("export", help="Export a role ledger to a JSON bundle")
    export_cmd.add_argument("--session", required=True)
    export_cmd.add_argument("--role", choices=sorted(ROLES), required=True)
    export_cmd.add_argument("--output-root", type=Path, required=True)
    export_cmd.add_argument("--bundle", type=Path, required=True)

    import_cmd = sub.add_parser("import", help="Import a JSON bundle into a role ledger")
    import_cmd.add_argument("--session", required=True)
    import_cmd.add_argument("--role", choices=sorted(ROLES), required=True)
    import_cmd.add_argument("--output-root", type=Path, required=True)
    import_cmd.add_argument("--bundle", type=Path, required=True)

    args = parser.parse_args(argv)
    try:
        if args.command == "export":
            result = export_bundle(args.output_root, args.session, args.role, args.bundle)
        else:
            result = import_bundle(args.output_root, args.session, args.role, args.bundle)
        print(json.dumps(result, indent=2))
        return 0
    except ValueError as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
