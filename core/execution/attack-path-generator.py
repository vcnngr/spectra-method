#!/usr/bin/env python3
"""SPECTRA Attack-Path Generator (Layer 3 — deterministic execution).

Builds an evidence-anchored attack-path graph from data SPECTRA already tracks:
the engagement kill_chain, the findings registry, the evidence registry, and —
when present — a Duel Mode Blue ledger used to overlay honest detection status.

SPECTRA principles enforced here (not a generic graph tool):

  * Evidence over assumption. Every finding node carries its evidence references;
    a finding with no linked evidence is marked ``evidence_state: "unverified"``
    rather than silently trusted.
  * Honest measurement, not "invisible Red". When a Blue ledger is supplied,
    edges carrying an ATT&CK technique are labelled detected / missed based on
    Blue telemetry — never on prior knowledge of the Red plan. This feeds
    detection-gap design and Referee adjudication.
  * Modeling only. This script MODELS authorized attack paths from recorded
    results. It never connects to a target, never executes a payload, and never
    modifies any host. It is read-only over engagement artifacts.

Outputs:

  * ``attack-path.json`` — nodes + edges + summary (the serializable artifact).
  * an optional Mermaid ``flowchart LR`` render for embedding in reports.

The CLI mirrors the other Layer-3 tools (report-generator.py, duel-orchestrator.py).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Canonical Lockheed-Martin-style kill-chain order used by SPECTRA engagements.
# Phases are rendered in this order when present; unknown phases keep their
# insertion order after the known ones.
CANONICAL_PHASE_ORDER = [
    "reconnaissance",
    "weaponization",
    "delivery",
    "exploitation",
    "installation",
    "command_and_control",
    "actions_on_objectives",
]

# Phase statuses that represent real activity worth placing on the graph.
ACTIVE_PHASE_STATUSES = {"in-progress", "in_progress", "complete", "completed"}

# Shared with report-adapters; duplicated locally to keep this module importable
# even if the adapter cannot be loaded.
SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "informational": 4,
    "info": 4,
}

# Findings at or above this rank (lower number = more severe) are wired to the
# terminal impact node as a chained outcome.
IMPACT_SEVERITY_MAX_RANK = SEVERITY_ORDER["high"]


# ---------------------------------------------------------------------------
# Adapter loading (report-adapters.py has a hyphen, so import it by path)
# ---------------------------------------------------------------------------

def _load_report_adapters():
    """Load the sibling report-adapters module by file path.

    Mirrors the loader convention used by report-generator.py. Works in both the
    source repo layout and the installed _spectra layout, because the adapter
    always sits next to this file.
    """
    script = Path(__file__).resolve().with_name("report-adapters.py")
    spec = importlib.util.spec_from_file_location("report_adapters", script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load report adapters: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _severity_of(finding: dict[str, Any]) -> str:
    sev = str(finding.get("severity", "informational")).lower()
    if sev == "info":
        sev = "informational"
    return sev if sev in SEVERITY_ORDER else "informational"


def _severity_rank(severity: str) -> int:
    return SEVERITY_ORDER.get(severity, 4)


def _finding_phase(finding: dict[str, Any], known_phases: list[str]) -> str | None:
    """Resolve which kill-chain phase a finding belongs to.

    Honors an explicit ``phase`` / ``kill_chain_phase`` field, normalizing it to
    a known phase key. Returns None when the finding cannot be attributed.
    """
    raw = finding.get("phase") or finding.get("kill_chain_phase") or ""
    norm = str(raw).strip().lower().replace(" ", "_").replace("-", "_")
    if not norm:
        return None
    if norm in known_phases:
        return norm
    # Tolerate close aliases (e.g. "c2" -> "command_and_control").
    aliases = {
        "c2": "command_and_control",
        "recon": "reconnaissance",
        "exploit": "exploitation",
        "objectives": "actions_on_objectives",
        "actions": "actions_on_objectives",
    }
    return aliases.get(norm) if aliases.get(norm) in known_phases else None


def _techniques_of(finding: dict[str, Any]) -> list[str]:
    """Extract all ATT&CK technique labels from a finding, de-duplicated.

    Honors both singular fields (technique, attack_technique, ...) and plural
    list fields (techniques, mitre_techniques, ...). Order is preserved so the
    first technique is a stable "primary" for display; the full list feeds
    unique-technique coverage so multi-technique findings are never undercounted.
    """
    singular_keys = ("technique", "attack_technique", "mitre_technique", "tcode", "t_code")
    plural_keys = ("techniques", "attack_techniques", "mitre_techniques")

    collected: list[str] = []
    for key in singular_keys:
        value = finding.get(key)
        if value:
            collected.append(str(value).strip())
    for key in plural_keys:
        value = finding.get(key)
        if isinstance(value, (list, tuple)):
            collected.extend(str(v).strip() for v in value if v)
        elif value:
            collected.append(str(value).strip())

    seen: set[str] = set()
    ordered: list[str] = []
    for technique in collected:
        if technique and technique.upper() not in seen:
            seen.add(technique.upper())
            ordered.append(technique)
    return ordered


def _evidence_refs(finding: dict[str, Any]) -> list[str]:
    refs = finding.get("evidence") or finding.get("evidence_refs") or finding.get("evidence_ids")
    if refs is None:
        return []
    if isinstance(refs, str):
        return [refs]
    if isinstance(refs, (list, tuple)):
        return [str(r) for r in refs if r]
    return []


def _ordered_phases(kill_chain: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """Return (phase_key, phase_data) for ACTIVE phases, in canonical order."""
    items: list[tuple[str, dict[str, Any]]] = []
    seen: set[str] = set()
    for key in CANONICAL_PHASE_ORDER:
        if key in kill_chain:
            seen.add(key)
            data = kill_chain[key] if isinstance(kill_chain[key], dict) else {}
            items.append((key, data))
    # Append any non-canonical phases in their original order.
    for key, data in kill_chain.items():
        if key not in seen:
            items.append((key, data if isinstance(data, dict) else {}))

    active = []
    for key, data in items:
        status = str(data.get("status", "")).strip().lower()
        if status in ACTIVE_PHASE_STATUSES:
            active.append((key, data))
    return active


def _blue_detected_techniques(duel_ledger_path: str | None) -> set[str]:
    """Collect ATT&CK techniques Blue evidenced as detected, from a duel ledger.

    The ledger is JSONL; Blue detection events carry a ``technique`` field. Only
    blue-role detection-type events count — Red's own techniques do not. Returned
    techniques are upper-cased so matching against findings is case-insensitive.
    """
    if not duel_ledger_path:
        return set()
    path = Path(duel_ledger_path)
    if not path.is_file():
        raise FileNotFoundError(f"Duel ledger not found: {duel_ledger_path}")

    detected: set[str] = set()
    # Stream the ledger line-by-line so a large file is never fully buffered.
    with path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            role = str(event.get("role", "")).strip().lower()
            etype = str(event.get("event_type", "")).strip().lower()
            technique = str(event.get("technique", "")).strip()
            # Only detection/alert events count as DETECTION. Mitigation is a
            # response, not a detection signal — conflating them would inflate
            # detection coverage. Referee credits mitigation separately.
            if role == "blue" and technique and ("detect" in etype or "alert" in etype):
                detected.add(technique.upper())
    return detected


# ---------------------------------------------------------------------------
# Graph construction
# ---------------------------------------------------------------------------

def build_attack_path(
    engagement_path: str,
    duel_ledger_path: str | None = None,
    spectra_root: str | None = None,
) -> dict[str, Any]:
    """Build the attack-path graph dict from engagement artifacts."""
    adapters = _load_report_adapters()
    bundle = adapters.build_report_bundle(engagement_path, spectra_root)

    engagement = bundle.get("engagement", {}) or {}
    kill_chain = bundle.get("kill_chain", {}) or {}
    findings = (bundle.get("findings", {}) or {}).get("findings", []) or []

    detected_techniques = _blue_detected_techniques(duel_ledger_path)
    detection_overlay = duel_ledger_path is not None

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    # --- Entry node -------------------------------------------------------
    entry_id = "entry"
    nodes.append({
        "id": entry_id,
        "type": "entry",
        "label": "Entry / Attacker",
    })

    # --- Phase nodes (active kill-chain phases, canonical order) ----------
    active_phases = _ordered_phases(kill_chain)
    known_phases = list(kill_chain.keys())
    phase_node_ids: dict[str, str] = {}
    prev_id = entry_id
    for key, data in active_phases:
        node_id = f"phase:{key}"
        phase_node_ids[key] = node_id
        nodes.append({
            "id": node_id,
            "type": "phase",
            "label": key.replace("_", " ").title(),
            "phase": key,
            "status": str(data.get("status", "")).strip().lower(),
            "agent": data.get("agent", ""),
        })
        edges.append({
            "source": prev_id,
            "target": node_id,
            "type": "progression",
            "label": "advances to",
        })
        prev_id = node_id

    # The terminal impact node is emitted only if something actually chains into
    # it (see below), so an engagement with no high/critical finding does not
    # leave a misleading orphan "Impact" node on the graph.
    impact_id = "impact"

    # --- Finding nodes + edges -------------------------------------------
    chained_to_impact = 0
    impact_edges: list[dict[str, Any]] = []
    # Detection coverage is measured over UNIQUE techniques observed in the path,
    # not per finding, so repeated techniques don't inflate the ratio.
    path_techniques: set[str] = set()
    detected_path_techniques: set[str] = set()
    seen_node_ids: set[str] = set()

    for index, finding in enumerate(findings):
        fid = str(finding.get("id") or f"finding-{index}")
        node_id = f"finding:{fid}"
        # Disambiguate duplicate finding ids so node ids stay unique.
        if node_id in seen_node_ids:
            suffix = 1
            while f"{node_id}#{suffix}" in seen_node_ids:
                suffix += 1
            node_id = f"{node_id}#{suffix}"
        seen_node_ids.add(node_id)

        severity = _severity_of(finding)
        techniques = _techniques_of(finding)
        primary_technique = techniques[0] if techniques else ""
        evidence = _evidence_refs(finding)
        evidence_state = "verified" if evidence else "unverified"

        node: dict[str, Any] = {
            "id": node_id,
            "type": "finding",
            "label": str(finding.get("title") or finding.get("name") or fid),
            "finding_id": fid,
            "severity": severity,
            "technique": primary_technique,
            "techniques": techniques,
            "evidence_state": evidence_state,
            "evidence_refs": evidence,
            "source_path": finding.get("source_path", ""),
        }

        # Detection overlay applies to findings that carry at least one technique.
        # A finding counts as detected only if ALL of its techniques were
        # evidenced by Blue — a partially-detected finding still surfaces a gap.
        detected: bool | None = None
        if detection_overlay and techniques:
            keys = [t.upper() for t in techniques]
            path_techniques.update(keys)
            detected_here = [k for k in keys if k in detected_techniques]
            detected_path_techniques.update(detected_here)
            detected = len(detected_here) == len(keys)
            node["detected"] = detected

        nodes.append(node)

        # Attach finding to its kill-chain phase if attributable, else to entry.
        phase_key = _finding_phase(finding, known_phases)
        attach_to = phase_node_ids.get(phase_key) if phase_key else None
        source_id = attach_to or entry_id
        edge_label = primary_technique or "yields"
        edge: dict[str, Any] = {
            "source": source_id,
            "target": node_id,
            "type": "exploits",
            "label": edge_label,
            "severity": severity,
        }
        if detected is not None:
            edge["detected"] = detected
        edges.append(edge)

        # High/critical findings chain into the terminal impact node.
        if _severity_rank(severity) <= IMPACT_SEVERITY_MAX_RANK:
            chained_to_impact += 1
            impact_edge: dict[str, Any] = {
                "source": node_id,
                "target": impact_id,
                "type": "escalates",
                "label": f"{severity} impact",
                "severity": severity,
            }
            if detected is not None:
                impact_edge["detected"] = detected
            impact_edges.append(impact_edge)

    # Emit the impact node (and its inbound edges) only when something reaches it.
    if chained_to_impact:
        nodes.append({
            "id": impact_id,
            "type": "impact",
            "label": "Impact / Objective",
        })
        edges.extend(impact_edges)

    # --- Summary ----------------------------------------------------------
    severity_counts = {k: 0 for k in ("critical", "high", "medium", "low", "informational")}
    unverified = 0
    for finding in findings:
        sev = _severity_of(finding)
        severity_counts[sev] += 1
        if not _evidence_refs(finding):
            unverified += 1

    summary: dict[str, Any] = {
        "engagement_id": engagement.get("id", ""),
        "engagement_type": engagement.get("type", ""),
        "active_phases": [k for k, _ in active_phases],
        "node_count": len(nodes),
        "edge_count": len(edges),
        "finding_count": len(findings),
        "severity_counts": severity_counts,
        "chained_to_impact": chained_to_impact,
        "unverified_findings": unverified,
        "detection_overlay": detection_overlay,
    }
    if detection_overlay:
        techniques_total = len(path_techniques)
        techniques_detected = len(detected_path_techniques)
        coverage = (techniques_detected / techniques_total) if techniques_total else 0.0
        summary["detection"] = {
            "techniques_total": techniques_total,
            "techniques_detected": techniques_detected,
            "techniques_missed": techniques_total - techniques_detected,
            "coverage_ratio": round(coverage, 4),
        }

    return {
        "schema": "spectra.attack-path/v1",
        "engagement_path": str(Path(engagement_path).resolve()),
        "summary": summary,
        "nodes": nodes,
        "edges": edges,
    }


# ---------------------------------------------------------------------------
# Mermaid rendering
# ---------------------------------------------------------------------------

_MERMAID_SHAPE = {
    "entry": ("([", "])"),       # stadium
    "phase": ("[", "]"),          # rectangle
    "finding": ("{{", "}}"),     # hexagon
    "impact": ("[/", "/]"),      # parallelogram
}


def _mermaid_id_map(graph: dict[str, Any]) -> dict[str, str]:
    """Assign a collision-free Mermaid id to each node, by insertion order.

    Sanitizing the raw node id alone is not bijective (``finding:a/b`` and
    ``finding:a:b`` would collapse), so ids are issued sequentially. A sanitized
    fragment is appended purely for human readability of the rendered source.
    """
    id_map: dict[str, str] = {}
    for index, node in enumerate(graph.get("nodes", [])):
        raw = node["id"]
        readable = "".join(c if c.isalnum() else "_" for c in raw)[:40]
        id_map[raw] = f"n{index}_{readable}"
    return id_map


def _mermaid_escape(text: str) -> str:
    # Escape backslashes first so a trailing "\" cannot escape the closing quote,
    # then neutralize quotes, newlines, and the Mermaid edge-label delimiter "|".
    return (
        str(text)
        .replace("\\", "\\\\")
        .replace('"', "'")
        .replace("\n", " ")
        .replace("|", "/")
    )


def render_mermaid(graph: dict[str, Any]) -> str:
    """Render the attack-path graph as a Mermaid flowchart (left-to-right)."""
    lines = ["flowchart LR"]
    id_map = _mermaid_id_map(graph)

    for node in graph.get("nodes", []):
        nid = id_map[node["id"]]
        open_b, close_b = _MERMAID_SHAPE.get(node.get("type", "phase"), ("[", "]"))
        label = _mermaid_escape(node.get("label", node["id"]))
        if node.get("type") == "finding" and node.get("severity"):
            label = f"{label} ({node['severity']})"
        lines.append(f'    {nid}{open_b}"{label}"{close_b}')

    for edge in graph.get("edges", []):
        # Edges only ever reference emitted nodes, but guard defensively so a
        # stray edge can never crash the render.
        if edge["source"] not in id_map or edge["target"] not in id_map:
            continue
        src = id_map[edge["source"]]
        dst = id_map[edge["target"]]
        label = _mermaid_escape(edge.get("label", ""))
        detected = edge.get("detected")
        if detected is True:
            label = f"{label} [detected]" if label else "detected"
            connector = "-->"
        elif detected is False:
            label = f"{label} [MISSED]" if label else "MISSED"
            connector = "-.->"
        else:
            connector = "-->"
        if label:
            lines.append(f'    {src} {connector}|"{label}"| {dst}')
        else:
            lines.append(f"    {src} {connector} {dst}")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_generate(args: argparse.Namespace) -> None:
    try:
        graph = build_attack_path(args.engagement, args.duel_ledger, args.spectra_root)
    except Exception as exc:  # noqa: BLE001 — surface a clean JSON error to callers
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(graph, indent=2), encoding="utf-8")

    if args.mermaid:
        mmd = Path(args.mermaid)
        mmd.parent.mkdir(parents=True, exist_ok=True)
        mmd.write_text(render_mermaid(graph), encoding="utf-8")

    if args.output or args.mermaid:
        result = {"status": "written", "summary": graph["summary"]}
        if args.output:
            result["output"] = str(Path(args.output).resolve())
        if args.mermaid:
            result["mermaid"] = str(Path(args.mermaid).resolve())
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(graph, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="attack-path-generator.py",
        description="Generate an evidence-anchored SPECTRA attack-path graph (modeling only).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate the attack-path graph from an engagement")
    gen.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    gen.add_argument("--duel-ledger", help="Optional Duel Mode Blue ledger (JSONL) for detection overlay")
    gen.add_argument("--output", help="Write attack-path.json here")
    gen.add_argument("--mermaid", help="Write a Mermaid flowchart render here")
    gen.add_argument("--spectra-root", help="SPECTRA root for tool/framework resolution")
    gen.set_defaults(func=cmd_generate)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
