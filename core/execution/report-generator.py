#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Structured SPECTRA report generator."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VERSION = "0.3.0"


def _load_adapters():
    script = Path(__file__).resolve().with_name("report-adapters.py")
    spec = importlib.util.spec_from_file_location("report_adapters", script)
    if not spec or not spec.loader:
        raise RuntimeError(f"Cannot load report adapters: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


adapters = _load_adapters()


def _default_output_path(engagement_path: str, report_type: str, engagement_id: str) -> Path:
    eng_dir = Path(engagement_path).resolve().parent
    output_root = eng_dir.parent.parent
    return output_root / "reports" / engagement_id / f"{report_type}-report.md"


def _safe(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _list_lines(items: list[Any]) -> list[str]:
    if not items:
        return ["- None documented"]
    return [f"- {_safe(item)}" for item in items]


def _scope_section(title: str, section: dict[str, Any]) -> list[str]:
    lines = [f"### {title}", ""]
    for key, value in section.items():
        if key == "notes":
            continue
        if isinstance(value, list) and value:
            lines.append(f"**{key.replace('_', ' ').title()}:**")
            lines.extend(_list_lines(value))
            lines.append("")
    notes = section.get("notes")
    if notes:
        lines.extend(["**Notes:**", _safe(notes), ""])
    if len(lines) == 2:
        lines.append("- None documented")
        lines.append("")
    return lines


def _risk_rating(counts: dict[str, int]) -> str:
    if counts.get("critical", 0):
        return "Critical"
    if counts.get("high", 0):
        return "High"
    if counts.get("medium", 0):
        return "Moderate"
    if counts.get("low", 0):
        return "Low"
    return "Informational"


def render_markdown(bundle: dict[str, Any], report_type: str) -> str:
    engagement = bundle["engagement"]
    auth = engagement.get("authorization") or {}
    findings = bundle["findings"]
    counts = findings["severity_counts"]
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    engagement_id = engagement.get("id", "unknown")
    title_type = report_type.replace("-", " ").title()

    lines: list[str] = [
        "---",
        f"report_type: {report_type}",
        f"engagement_id: {engagement_id}",
        f"generated: {generated}",
        "generator: SPECTRA report-generator.py",
        f"generator_version: {VERSION}",
        "---",
        "",
        f"# {title_type} Report - {engagement_id}",
        "",
        f"**Client:** {_safe(auth.get('client'), 'unknown')}",
        f"**Engagement Type:** {_safe(engagement.get('type'), 'unknown')}",
        f"**Status:** {_safe(engagement.get('status'), 'unknown')}",
        f"**Period:** {_safe(auth.get('start_date'), 'unknown')} -> {_safe(auth.get('end_date'), 'unknown')}",
        f"**Generated:** {generated}",
        "",
        "## 1. Executive Summary",
        "",
        f"Overall risk rating: **{_risk_rating(counts)}**.",
        f"Total findings: **{findings['total']}** "
        f"(Critical: {counts['critical']} | High: {counts['high']} | Medium: {counts['medium']} | "
        f"Low: {counts['low']} | Informational: {counts['informational']}).",
        f"Evidence items indexed: **{bundle['evidence']['item_count']}** "
        f"(integrity: {bundle['evidence']['integrity_status']}).",
        "",
        "## 2. Scope And Authorization",
        "",
    ]

    scope = bundle["scope"]
    lines.extend(_scope_section("In Scope", scope["in_scope"]))
    lines.extend(_scope_section("Out Of Scope", scope["out_of_scope"]))

    roe = scope["rules_of_engagement"]
    lines.extend([
        "### Rules Of Engagement",
        "",
        f"- Testing hours: {_safe(roe.get('testing_hours'), 'unknown')}",
        f"- Max impact level: {_safe(roe.get('max_impact_level'), 'unknown')}",
        f"- Social engineering allowed: {_safe(roe.get('social_engineering_allowed'), 'false')}",
        f"- Physical access allowed: {_safe(roe.get('physical_access_allowed'), 'false')}",
        f"- DoS testing allowed: {_safe(roe.get('dos_testing_allowed'), 'false')}",
        f"- Data exfiltration allowed: {_safe(roe.get('data_exfiltration_allowed'), 'false')}",
        "",
        "## 3. Workflow State",
        "",
        "| Workflow | Status | Agent | Started | Completed | Artifacts |",
        "|----------|--------|-------|---------|-----------|-----------|",
    ])
    for key, state in (bundle.get("workflow_state") or {}).items():
        artifacts = ", ".join(state.get("artifacts") or [])
        lines.append(
            f"| {key} | {state.get('status', 'pending')} | {state.get('agent', '')} | "
            f"{state.get('started', '')} | {state.get('completed', '')} | {artifacts} |"
        )
    if not bundle.get("workflow_state"):
        lines.append("| None | pending | | | | |")

    lines.extend([
        "",
        "## 4. Findings Summary",
        "",
        "| ID | Title | Severity | CVSS | Status | Source |",
        "|----|-------|----------|------|--------|--------|",
    ])
    for finding in findings["findings"]:
        lines.append(
            f"| {finding.get('id', '')} | {finding.get('title', '')} | "
            f"{finding.get('severity', 'informational')} | {finding.get('cvss', finding.get('cvss_score', ''))} | "
            f"{finding.get('status', '')} | {finding.get('source_path', '')} |"
        )
    if not findings["findings"]:
        lines.append("| None | No findings documented | informational | | | |")

    evidence = bundle["evidence"]
    lines.extend([
        "",
        "## 5. Evidence Index",
        "",
        f"Registry: `{evidence['registry_path']}`",
        "",
        "| Evidence ID | Description | Type | Status | SHA-256 |",
        "|-------------|-------------|------|--------|---------|",
    ])
    for item in evidence["items"]:
        sha = _safe(item.get("hash_sha256"), "N/A")
        if len(sha) > 18:
            sha = f"{sha[:18]}..."
        lines.append(
            f"| {item.get('id', '')} | {item.get('description', '')} | "
            f"{item.get('source_type', '')} | {item.get('status', '')} | {sha} |"
        )
    if not evidence["items"]:
        lines.append("| None | No evidence registered | | | |")

    tools = bundle["tools"]
    lines.extend([
        "",
        "## 6. Tool Registry Snapshot",
        "",
        f"Tools registered: **{tools['tool_count']}** across **{tools['category_count']}** categories.",
        "",
        "| Tool | Category | Type | License |",
        "|------|----------|------|---------|",
    ])
    for tool in tools["tools"][:25]:
        lines.append(
            f"| {tool.get('name', '')} | {tool.get('category', '')} | "
            f"{tool.get('type', '')} | {tool.get('license', '')} |"
        )
    if tools["tool_count"] > 25:
        lines.append(f"| ... | {tools['tool_count'] - 25} additional tools omitted from snapshot | | |")

    lines.extend([
        "",
        "## 7. Adapter Metadata",
        "",
        f"- Engagement path: `{bundle['engagement_path']}`",
        f"- Findings directory: `{findings['findings_dir']}`",
        f"- Evidence registry exists: {evidence['exists']}",
        f"- Tool registry exists: {tools['exists']}",
        "",
    ])
    return "\n".join(lines)


def cmd_generate(args: argparse.Namespace) -> None:
    try:
        bundle = adapters.build_report_bundle(args.engagement, args.spectra_root)
        engagement_id = bundle["engagement"].get("id", "unknown")
        output = Path(args.output) if args.output else _default_output_path(args.engagement, args.type, engagement_id)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render_markdown(bundle, args.type), encoding="utf-8")
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    print(json.dumps({
        "status": "generated",
        "report_type": args.type,
        "engagement_id": engagement_id,
        "output": str(output.resolve()),
        "findings": bundle["findings"]["total"],
        "evidence_items": bundle["evidence"]["item_count"],
    }, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="report-generator")
    sub = parser.add_subparsers(dest="command", required=True)
    p_generate = sub.add_parser("generate", help="Generate structured report")
    p_generate.add_argument("--engagement", required=True)
    p_generate.add_argument("--type", default="pentest")
    p_generate.add_argument("--output")
    p_generate.add_argument("--spectra-root")
    p_generate.set_defaults(func=cmd_generate)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
