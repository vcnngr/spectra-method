#!/usr/bin/env python3
"""SPECTRA Engagement Personas (Layer 3 — deterministic execution).

SPECTRA ships 28 specialized agents, but at engagement start an operator should
not have to know all 28 names to pick the right team. This helper makes the
roster discoverable: given an engagement type, it recommends a lead persona, a
fast single-agent alternative, a supporting cast, and the workflows that team
typically runs — all resolved from the agent manifest so names never drift.

This is SPECTRA-native, not a generic "profile picker": the recommendations map
onto SPECTRA's own agents and workflows, and the agent manifest
(_config/agent-manifest.csv) is the single source of truth for every persona's
display name, role, and module. If a mapping points at an agent that does not
exist in the manifest, that is an error surfaced here, not a silent mislabel.

Read-only. Emits JSON for the spectra-new-engagement directive layer to present.

CLI:
  engagement-personas.py list                      # full roster grouped by module
  engagement-personas.py recommend --type pentest  # team recommendation for a type
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Any


# Engagement types mirror core/schemas/engagement.schema.yaml's enum.
ENGAGEMENT_TYPES = (
    "pentest",
    "red-team",
    "purple-team",
    "ctf",
    "training",
    "assessment",
    "incident-response",
    "compliance-audit",
)

# Deterministic engagement-type -> SPECTRA team mapping. Every agent name here is
# validated against the manifest at runtime. "solo" names a quick single-agent
# alternative (SPECTRA's Blade/Shield/Surge/Specter quick-ops agents) for fast
# engagements where standing up a full cast is overkill.
PROFILE_MAP: dict[str, dict[str, Any]] = {
    "pentest": {
        "lead": "spectra-agent-red-lead",
        "solo": "spectra-agent-blade",
        "support": [
            "spectra-agent-recon",
            "spectra-agent-exploit",
            "spectra-agent-operator",
            "spectra-agent-appsec",
        ],
        "workflows": [
            "spectra-external-recon",
            "spectra-initial-access",
            "spectra-privesc",
            "spectra-lateral-movement",
            "spectra-exfiltration",
        ],
    },
    "red-team": {
        "lead": "spectra-agent-red-lead",
        "solo": "spectra-agent-blade",
        "support": [
            "spectra-agent-recon",
            "spectra-agent-exploit",
            "spectra-agent-operator",
            "spectra-agent-social-eng",
            "spectra-agent-referee",
        ],
        "workflows": [
            "spectra-external-recon",
            "spectra-initial-access",
            "spectra-privesc",
            "spectra-lateral-movement",
            "spectra-exfiltration",
        ],
    },
    "purple-team": {
        "lead": "spectra-agent-referee",
        "solo": "spectra-agent-specter",
        "support": [
            "spectra-agent-red-lead",
            "spectra-agent-soc-manager",
            "spectra-agent-detection-eng",
            "spectra-agent-telemetry",
        ],
        "workflows": [
            "spectra-war-room",
            "spectra-duel-adjudication",
            "spectra-detection-lifecycle",
            "spectra-attack-path",
        ],
    },
    "ctf": {
        "lead": "spectra-agent-exploit",
        "solo": "spectra-agent-blade",
        "support": [
            "spectra-agent-recon",
            "spectra-agent-appsec",
            "spectra-agent-operator",
        ],
        "workflows": [
            "spectra-appsec-assessment",
            "spectra-initial-access",
            "spectra-privesc",
        ],
    },
    "training": {
        "lead": "spectra-agent-specter",
        "solo": "spectra-agent-specter",
        "support": [
            "spectra-agent-chronicle",
            "spectra-agent-red-lead",
            "spectra-agent-soc-manager",
        ],
        "workflows": [
            "spectra-war-room",
        ],
    },
    "assessment": {
        "lead": "spectra-agent-blade",
        "solo": "spectra-agent-blade",
        "support": [
            "spectra-agent-recon",
            "spectra-agent-appsec",
            "spectra-agent-identity",
        ],
        "workflows": [
            "spectra-external-recon",
            "spectra-appsec-assessment",
        ],
    },
    "incident-response": {
        "lead": "spectra-agent-handler",
        "solo": "spectra-agent-surge",
        "support": [
            "spectra-agent-forensics",
            "spectra-agent-malware",
            "spectra-agent-threat-intel",
            "spectra-agent-cloud",
        ],
        "workflows": [
            "spectra-incident-handling",
            "spectra-digital-forensics",
            "spectra-malware-analysis",
            "spectra-threat-intel-workflow",
            "spectra-cloud-incident-response",
        ],
    },
    "compliance-audit": {
        "lead": "spectra-agent-compliance",
        "solo": "spectra-agent-specter",
        "support": [
            "spectra-agent-risk",
            "spectra-agent-policy",
            "spectra-agent-privacy",
        ],
        "workflows": [
            "spectra-compliance-audit",
            "spectra-risk-assessment",
            "spectra-policy-lifecycle",
            "spectra-privacy-breach-assessment",
        ],
    },
}


# ---------------------------------------------------------------------------
# Manifest loading
# ---------------------------------------------------------------------------

def _default_manifest_path(spectra_root: str | None) -> Path:
    """Resolve _config/agent-manifest.csv in source or installed layout.

    Resolution order: explicit --spectra-root, then the SPECTRA_ROOT environment
    variable (robust when the package layout is flattened by an installer), then
    the source-tree location relative to this file.
    """
    root_hint = spectra_root or os.environ.get("SPECTRA_ROOT")
    if root_hint:
        root = Path(root_hint)
        for candidate in (root / "_config" / "agent-manifest.csv",
                           root / "_spectra" / "_config" / "agent-manifest.csv"):
            if candidate.is_file():
                return candidate
        return root / "_config" / "agent-manifest.csv"
    # core/execution/<this file> -> repo root is parents[2].
    return Path(__file__).resolve().parents[2] / "_config" / "agent-manifest.csv"


REQUIRED_MANIFEST_COLUMNS = ("name", "displayName", "role", "module")


def load_personas(manifest_path: str | Path) -> dict[str, dict[str, str]]:
    """Load all agent personas from the manifest, keyed by canonical agent name."""
    path = Path(manifest_path)
    if not path.is_file():
        raise FileNotFoundError(f"Agent manifest not found: {path}")
    personas: dict[str, dict[str, str]] = {}
    # utf-8-sig tolerates a UTF-8 BOM (common when a CSV is edited in Excel).
    with path.open(encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        missing_cols = [c for c in REQUIRED_MANIFEST_COLUMNS
                        if c not in (reader.fieldnames or [])]
        if missing_cols:
            raise ValueError(
                f"Agent manifest {path} is missing required column(s): "
                f"{', '.join(missing_cols)}"
            )
        for line_no, row in enumerate(reader, start=2):  # row 1 is the header
            name = (row.get("name") or "").strip()
            if not name:
                continue
            if name in personas:
                raise ValueError(
                    f"Duplicate agent name '{name}' in {path} (row {line_no}); "
                    f"canonical agent names must be unique."
                )
            personas[name] = {
                "name": name,
                "displayName": (row.get("displayName") or "").strip(),
                "title": (row.get("title") or "").strip(),
                "role": (row.get("role") or "").strip(),
                "module": (row.get("module") or "").strip(),
                "path": (row.get("path") or "").strip(),
            }
    return personas


# ---------------------------------------------------------------------------
# Catalog + recommendation
# ---------------------------------------------------------------------------

def build_catalog(personas: dict[str, dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    """Group personas by module, ordered for stable presentation."""
    module_order = ["core", "rtk", "soc", "irt", "grc"]

    def sort_key(persona: dict[str, str]) -> tuple[str, str]:
        # Stable ordering with a canonical-name tie-breaker.
        return (persona["displayName"] or persona["name"], persona["name"])

    catalog: dict[str, list[dict[str, str]]] = {}
    for module in module_order:
        members = [p for p in personas.values() if p["module"] == module]
        if members:
            catalog[module] = sorted(members, key=sort_key)
    # Any module not in the predefined order (defensive — keeps unknowns visible),
    # in deterministic module-name order with sorted members.
    unknown_modules = sorted(
        {p["module"] for p in personas.values() if p["module"] not in module_order}
    )
    for module in unknown_modules:
        members = [p for p in personas.values() if p["module"] == module]
        catalog[module] = sorted(members, key=sort_key)
    return catalog


def _resolve(name: str, personas: dict[str, dict[str, str]]) -> dict[str, str]:
    persona = personas.get(name)
    if persona is None:
        raise KeyError(
            f"Persona '{name}' referenced in PROFILE_MAP is missing from the agent "
            f"manifest. The mapping and the manifest are out of sync."
        )
    return persona


def recommend(engagement_type: str, personas: dict[str, dict[str, str]]) -> dict[str, Any]:
    """Recommend a SPECTRA team for an engagement type."""
    profile = PROFILE_MAP.get(engagement_type)
    if profile is None:
        raise ValueError(
            f"Unknown engagement type '{engagement_type}'. "
            f"Expected one of: {', '.join(ENGAGEMENT_TYPES)}"
        )
    return {
        "engagement_type": engagement_type,
        "lead": _resolve(profile["lead"], personas),
        "solo": _resolve(profile["solo"], personas),
        "support": [_resolve(n, personas) for n in profile["support"]],
        "workflows": list(profile["workflows"]),
    }


def validate_profile_map(personas: dict[str, dict[str, str]]) -> list[str]:
    """Return a list of agent names referenced in PROFILE_MAP but absent from the
    manifest. An empty list means the mapping is fully consistent."""
    referenced: set[str] = set()
    for profile in PROFILE_MAP.values():
        referenced.add(profile["lead"])
        referenced.add(profile["solo"])
        referenced.update(profile["support"])
    return sorted(name for name in referenced if name not in personas)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_list(args: argparse.Namespace) -> None:
    personas = load_personas(args.manifest or _default_manifest_path(args.spectra_root))
    catalog = build_catalog(personas)
    print(json.dumps({"persona_count": len(personas), "by_module": catalog}, indent=2))


def cmd_recommend(args: argparse.Namespace) -> None:
    personas = load_personas(args.manifest or _default_manifest_path(args.spectra_root))
    try:
        result = recommend(args.type, personas)
    except (ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    print(json.dumps(result, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="engagement-personas.py",
        description="Discoverable SPECTRA persona catalog and team recommendations.",
    )
    parser.add_argument("--manifest", help="Path to agent-manifest.csv (overrides default)")
    parser.add_argument("--spectra-root", help="SPECTRA root for manifest resolution")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List the full persona roster grouped by module")
    p_list.set_defaults(func=cmd_list)

    p_rec = sub.add_parser("recommend", help="Recommend a team for an engagement type")
    p_rec.add_argument("--type", required=True, choices=ENGAGEMENT_TYPES, help="Engagement type")
    p_rec.set_defaults(func=cmd_recommend)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
