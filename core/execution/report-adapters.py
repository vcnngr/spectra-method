#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
SPECTRA Report Adapters

Normalizes engagement, scope, evidence, findings, and tool registry data into a
stable bundle consumed by report-generator.py and future integrations.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "informational": 4, "info": 4}


def _to_float(value: Any) -> float:
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc


def load_engagement_document(engagement_path: str) -> dict[str, Any]:
    path = Path(engagement_path)
    if not path.exists():
        raise FileNotFoundError(f"Engagement file not found: {engagement_path}")
    data = load_yaml(path)
    if "engagement" not in data:
        raise ValueError("Invalid engagement file: missing 'engagement' root key")
    return data


def scope_summary(engagement: dict[str, Any]) -> dict[str, Any]:
    scope = engagement.get("scope") or {}
    in_scope = scope.get("in_scope") or {}
    out_scope = scope.get("out_of_scope") or {}

    def section_counts(section: dict[str, Any]) -> dict[str, int]:
        return {
            key: len(value)
            for key, value in section.items()
            if key != "notes" and isinstance(value, list)
        }

    return {
        "in_scope": in_scope,
        "out_of_scope": out_scope,
        "counts": {
            "in_scope": sum(section_counts(in_scope).values()),
            "out_of_scope": sum(section_counts(out_scope).values()),
            "in_scope_breakdown": section_counts(in_scope),
            "out_of_scope_breakdown": section_counts(out_scope),
        },
        "rules_of_engagement": engagement.get("rules_of_engagement") or {},
        "data_handling": engagement.get("data_handling") or {},
    }


def evidence_registry_path(engagement_path: str) -> Path:
    eng_doc = load_engagement_document(engagement_path)
    eng_id = eng_doc["engagement"].get("id", "unknown")
    eng_dir = Path(engagement_path).resolve().parent
    output_root = eng_dir.parent.parent
    return output_root / "evidence" / eng_id / "evidence-registry.yaml"


def evidence_summary(engagement_path: str) -> dict[str, Any]:
    reg_path = evidence_registry_path(engagement_path)
    data = load_yaml(reg_path)
    registry = data.get("evidence_registry") or {}
    items = registry.get("items") or []
    return {
        "registry_path": str(reg_path),
        "exists": reg_path.exists(),
        "engagement_id": registry.get("engagement_id"),
        "item_count": registry.get("item_count", len(items)),
        "integrity_status": registry.get("integrity_status", "UNVERIFIED"),
        "last_verified": registry.get("last_verified", "never"),
        "items": items,
    }


def _flatten_tools(node: Any, category: str, subcategory: str = "") -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    if isinstance(node, list):
        for item in node:
            if isinstance(item, dict):
                normalized = dict(item)
                normalized["category"] = category
                normalized["subcategory"] = subcategory
                tools.append(normalized)
    elif isinstance(node, dict):
        for key, value in node.items():
            tools.extend(_flatten_tools(value, category, key))
    return tools


def tools_summary(spectra_root: str | None = None) -> dict[str, Any]:
    root = Path(spectra_root) if spectra_root else Path(__file__).resolve().parents[2]
    registry_path = root / "core" / "execution" / "tools-registry.yaml"
    data = load_yaml(registry_path)
    registry = data.get("registry") or {}
    categories = registry.get("categories") or {}
    tools: list[dict[str, Any]] = []
    for category, value in categories.items():
        tools.extend(_flatten_tools(value, category))
    return {
        "registry_path": str(registry_path),
        "exists": registry_path.exists(),
        "version": registry.get("version"),
        "tool_count": len(tools),
        "category_count": len(categories),
        "tools": tools,
    }


def _load_markdown_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {"id": path.stem, "title": path.stem, "source_path": str(path)}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {"id": path.stem, "title": path.stem, "source_path": str(path)}
    meta = yaml.safe_load(parts[1]) or {}
    if not isinstance(meta, dict):
        meta = {}
    meta.setdefault("id", path.stem)
    meta.setdefault("title", path.stem)
    meta["source_path"] = str(path)
    return meta


def findings_summary(engagement_path: str) -> dict[str, Any]:
    eng_dir = Path(engagement_path).resolve().parent
    findings_dir = eng_dir / "findings"
    findings: list[dict[str, Any]] = []
    if findings_dir.exists():
        for path in sorted(findings_dir.iterdir()):
            if path.suffix.lower() in {".yaml", ".yml"}:
                finding = load_yaml(path)
            elif path.suffix.lower() == ".json":
                finding = load_json(path)
            elif path.suffix.lower() == ".md":
                finding = _load_markdown_frontmatter(path)
            else:
                continue
            if finding:
                finding.setdefault("id", path.stem)
                finding.setdefault("title", finding.get("name", path.stem))
                finding.setdefault("severity", "informational")
                finding["source_path"] = str(path)
                findings.append(finding)

    findings.sort(key=lambda f: (
        SEVERITY_ORDER.get(str(f.get("severity", "informational")).lower(), 4),
        -_to_float(f.get("cvss", f.get("cvss_score", 0))),
        str(f.get("id", "")),
    ))

    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "informational": 0}
    for finding in findings:
        sev = str(finding.get("severity", "informational")).lower()
        if sev == "info":
            sev = "informational"
        counts[sev if sev in counts else "informational"] += 1

    return {
        "findings_dir": str(findings_dir),
        "exists": findings_dir.exists(),
        "total": len(findings),
        "severity_counts": counts,
        "findings": findings,
    }


def build_report_bundle(engagement_path: str, spectra_root: str | None = None) -> dict[str, Any]:
    doc = load_engagement_document(engagement_path)
    engagement = doc["engagement"]
    return {
        "engagement_path": str(Path(engagement_path).resolve()),
        "engagement": engagement,
        "workflow_state": doc.get("workflow_state") or {},
        "kill_chain": doc.get("kill_chain") or {},
        "scope": scope_summary(engagement),
        "evidence": evidence_summary(engagement_path),
        "findings": findings_summary(engagement_path),
        "tools": tools_summary(spectra_root),
    }


def cmd_bundle(args: argparse.Namespace) -> None:
    try:
        bundle = build_report_bundle(args.engagement, args.spectra_root)
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    if args.output:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(bundle, indent=2), encoding="utf-8")
        print(json.dumps({"status": "written", "output": str(output.resolve())}, indent=2))
    else:
        print(json.dumps(bundle, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="report-adapters")
    sub = parser.add_subparsers(dest="command", required=True)
    p_bundle = sub.add_parser("bundle", help="Build normalized report data bundle")
    p_bundle.add_argument("--engagement", required=True)
    p_bundle.add_argument("--spectra-root")
    p_bundle.add_argument("--output")
    p_bundle.set_defaults(func=cmd_bundle)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
