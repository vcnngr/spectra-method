#!/usr/bin/env python3
"""SPECTRA Posture Diff (Layer 3).

An engagement is usually a one-shot. But security is a moving target: the same
scope re-assessed weeks later has new findings, resolved ones, and a different
activity footprint. This module makes an engagement *repeatable over time* by
capturing a deterministic posture snapshot and diffing two snapshots into a
scored delta — did the posture improve or regress?

It is SPECTRA-native, not a vulnerability-management platform: a snapshot is
built only from the engagement's own artifacts (its `findings/` directory, its
scope, its run log), and the delta is a deterministic score the Referee can
build on — not a live dashboard.

Snapshots live under `<engagement_dir>/posture/<timestamp>.json` (append-only
history). `diff` compares the two most recent by default.

CLI:
  posture-diff.py snapshot --engagement E
  posture-diff.py diff     --engagement E [--from A.json --to B.json]
  posture-diff.py list     --engagement E
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Severity weights: higher = worse. Resolving a critical improves posture more
# than resolving an info; introducing a critical regresses it more.
SEVERITY_WEIGHT = {"critical": 5, "high": 4, "medium": 3, "low": 2,
                   "informational": 1, "info": 1}


def _load_sibling(module_name: str, file_name: str):
    """Import a hyphenated sibling execution module by file path."""
    script = Path(__file__).resolve().with_name(file_name)
    spec = importlib.util.spec_from_file_location(module_name, script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load {file_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _utc_now_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _norm_sev(sev: Any) -> str:
    s = str(sev or "informational").lower()
    return "informational" if s == "info" else s


def posture_dir(engagement_path: str) -> Path:
    return Path(engagement_path).resolve().parent / "posture"


def build_snapshot(engagement_path: str, now: str | None = None) -> dict[str, Any]:
    """Build a deterministic posture snapshot from the engagement's artifacts."""
    ra = _load_sibling("report_adapters", "report-adapters.py")
    racc = _load_sibling("run_accounting", "run-accounting.py")

    fsum = ra.findings_summary(engagement_path)
    # Keep only the stable, comparable fields — a snapshot must be reproducible.
    findings = [
        {
            "id": str(f.get("id")),
            "title": f.get("title", f.get("name", f.get("id"))),
            "severity": _norm_sev(f.get("severity")),
            "status": str(f.get("status", "open")).lower(),
        }
        for f in fsum.get("findings", [])
    ]
    runs = racc.summarize(engagement_path, limit=0)
    eng = ra.load_engagement_document(engagement_path)["engagement"]
    return {
        "ts": now or _utc_now_compact(),
        "engagement_id": eng.get("id"),
        "findings": findings,
        "severity_counts": fsum.get("severity_counts", {}),
        "open_count": sum(1 for f in findings if f["status"] != "resolved"),
        "runs": {"total": runs.get("total", 0),
                 "executed": runs.get("executed", 0),
                 "blocked": runs.get("blocked", 0)},
    }


def take_snapshot(engagement_path: str, now: str | None = None) -> Path:
    """Build a snapshot and persist it to the posture history."""
    snap = build_snapshot(engagement_path, now=now)
    pdir = posture_dir(engagement_path)
    pdir.mkdir(parents=True, exist_ok=True)
    out = pdir / f"{snap['ts']}.json"
    out.write_text(json.dumps(snap, indent=2) + "\n", encoding="utf-8")
    return out


def list_snapshots(engagement_path: str) -> list[Path]:
    pdir = posture_dir(engagement_path)
    if not pdir.is_dir():
        return []
    return sorted(p for p in pdir.iterdir()
                  if p.is_file() and p.suffix == ".json")


def _snapshot_findings(snap: dict[str, Any]) -> list[dict[str, Any]]:
    """Defensively extract findings: a hand-edited or truncated snapshot may
    hold a non-list or null entries; accounting must not crash on it."""
    raw = snap.get("findings") if isinstance(snap, dict) else None
    if not isinstance(raw, list):
        return []
    return [f for f in raw if isinstance(f, dict) and f.get("id") is not None]


def _index(findings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(f["id"]): f for f in findings}


def _is_resolved(f: dict[str, Any]) -> bool:
    return str(f.get("status", "open")).lower() == "resolved"


def _effective_weight(f: dict[str, Any] | None) -> int:
    """A finding's weight on the posture. A resolved or absent finding weighs 0,
    so closing it in-place (status -> resolved) improves the score just like
    deleting its file does."""
    if f is None or _is_resolved(f):
        return 0
    return SEVERITY_WEIGHT.get(f["severity"], 1)


def diff_snapshots(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    """Compare two snapshots by finding id and score the posture delta.

    Buckets are computed over *active* (non-resolved) findings; the score is the
    sum of per-id weight reductions, so resolving (or downgrading) a worse
    finding is positive and adding (or escalating) one is negative."""
    before = before if isinstance(before, dict) else {}
    after = after if isinstance(after, dict) else {}
    a_all, b_all = _index(_snapshot_findings(before)), _index(_snapshot_findings(after))
    a_act = {i for i, f in a_all.items() if not _is_resolved(f)}
    b_act = {i for i, f in b_all.items() if not _is_resolved(f)}

    added = [b_all[i] for i in sorted(b_act - a_act)]
    resolved = [a_all[i] for i in sorted(a_act - b_act)]
    persisting, escalations = [], []
    for i in sorted(a_act & b_act):
        persisting.append(b_all[i])
        if SEVERITY_WEIGHT.get(b_all[i]["severity"], 1) > SEVERITY_WEIGHT.get(a_all[i]["severity"], 1):
            escalations.append({"id": i, "from": a_all[i]["severity"], "to": b_all[i]["severity"]})

    # Per-id weight reduction across every finding seen in either snapshot.
    score = sum(_effective_weight(a_all.get(i)) - _effective_weight(b_all.get(i))
                for i in (a_all.keys() | b_all.keys()))
    verdict = "improved" if score > 0 else "regressed" if score < 0 else "unchanged"
    return {
        "from_ts": before.get("ts"),
        "to_ts": after.get("ts"),
        "added": added,
        "resolved": resolved,
        "persisting": sorted(persisting, key=lambda f: f["id"]),
        "escalations": escalations,
        "counts": {"added": len(added), "resolved": len(resolved),
                   "persisting": len(persisting), "escalations": len(escalations)},
        "score": score,
        "verdict": verdict,
    }


def _read_snapshot(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"snapshot is not a JSON object: {path}")
    return data


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cmd_snapshot(args: argparse.Namespace) -> None:
    try:
        out = take_snapshot(args.engagement)
    except (FileNotFoundError, ValueError, KeyError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    print(json.dumps({"snapshot": str(out)}, indent=2))
    sys.exit(0)


def cmd_diff(args: argparse.Namespace) -> None:
    try:
        if args.from_snap and args.to_snap:
            before, after = _read_snapshot(Path(args.from_snap)), _read_snapshot(Path(args.to_snap))
        else:
            snaps = list_snapshots(args.engagement)
            if len(snaps) < 2:
                print(json.dumps({"error": "need at least two snapshots to diff; "
                                           "run 'snapshot' on separate occasions"}),
                      file=sys.stderr)
                sys.exit(3)
            before, after = _read_snapshot(snaps[-2]), _read_snapshot(snaps[-1])
        result = diff_snapshots(before, after)
    except (FileNotFoundError, ValueError, KeyError, TypeError,
            AttributeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    print(json.dumps(result, indent=2))
    sys.exit(0)


def cmd_list(args: argparse.Namespace) -> None:
    print(json.dumps({"snapshots": [str(p) for p in list_snapshots(args.engagement)]}, indent=2))
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="posture-diff.py",
        description="Snapshot an engagement's posture and diff snapshots over time.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_s = sub.add_parser("snapshot", help="Capture a posture snapshot now")
    p_s.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_s.set_defaults(func=cmd_snapshot)

    p_d = sub.add_parser("diff", help="Diff two snapshots (default: two most recent)")
    p_d.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_d.add_argument("--from", dest="from_snap", help="Older snapshot JSON path")
    p_d.add_argument("--to", dest="to_snap", help="Newer snapshot JSON path")
    p_d.set_defaults(func=cmd_diff)

    p_l = sub.add_parser("list", help="List posture snapshots for an engagement")
    p_l.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_l.set_defaults(func=cmd_list)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
