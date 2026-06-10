#!/usr/bin/env python3
"""SPECTRA Remediation Export (Layer 3).

A finding is only useful when engineering can act on it. This module exports an
engagement's findings into remediation-ready, tool-agnostic formats — SARIF (for
code-scanning dashboards and CI), CSV (for trackers and spreadsheets), and a
Markdown ticket pack (one section per finding, ready to paste).

It is a deterministic *export*, not a live integration: SPECTRA stays a method,
not a ticketing platform. No network, no credentials, no third-party API — you
take the output and feed it to whatever system you already run.

CLI:
  remediation-export.py export --engagement E --format sarif|csv|md [--out FILE]
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import io
import json
import sys
from pathlib import Path
from typing import Any

# SARIF severity → result level. SARIF has only error/warning/note.
SARIF_LEVEL = {"critical": "error", "high": "error", "medium": "warning",
               "low": "warning", "informational": "note", "info": "note"}
CSV_COLUMNS = ["id", "title", "severity", "status", "cvss", "remediation", "source_path"]


def _csv_safe(value: Any) -> str:
    """Neutralize spreadsheet formula injection: a cell beginning with a formula
    trigger (=, +, -, @) or a leading control char (tab, CR, LF) is prefixed
    with a single quote so Excel/Sheets treat it as text, not a formula."""
    s = "" if value is None else str(value)
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r", "\n"):
        return "'" + s
    return s


def _load_report_adapters():
    script = Path(__file__).resolve().with_name("report-adapters.py")
    spec = importlib.util.spec_from_file_location("report_adapters", script)
    if not spec or not spec.loader:
        raise RuntimeError("Cannot load report-adapters.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_findings(engagement_path: str) -> list[dict[str, Any]]:
    ra = _load_report_adapters()
    # Validate the engagement exists and is well-formed first; otherwise a bad
    # path would silently export an empty set (findings_summary tolerates a
    # missing findings/ dir) instead of failing loudly.
    ra.load_engagement_document(engagement_path)
    return ra.findings_summary(engagement_path).get("findings", [])


def _norm_sev(sev: Any) -> str:
    s = str(sev or "informational").lower()
    return "informational" if s == "info" else s


def to_sarif(findings: list[dict[str, Any]]) -> str:
    """Minimal valid SARIF 2.1.0 with one result per finding."""
    rules, results = [], []
    seen_rules: set[str] = set()
    for f in findings:
        fid = str(f.get("id"))
        sev = _norm_sev(f.get("severity"))
        title = f.get("title", f.get("name", fid))
        if fid not in seen_rules:
            seen_rules.add(fid)
            rules.append({
                "id": fid,
                "name": str(title),
                "shortDescription": {"text": str(title)},
                "properties": {"security-severity": str(f.get("cvss", f.get("cvss_score", "")))
                               or "0", "severity": sev},
            })
        result: dict[str, Any] = {
            "ruleId": fid,
            "level": SARIF_LEVEL.get(sev, "note"),
            "message": {"text": str(f.get("description", title))},
            "properties": {"severity": sev, "status": str(f.get("status", "open")).lower()},
        }
        # A location makes the finding actionable in code-scanning dashboards.
        src = f.get("source_path") or f.get("location") or f.get("file")
        if src:
            result["locations"] = [{
                "physicalLocation": {"artifactLocation": {"uri": str(src)}}
            }]
        results.append(result)
    doc = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": "SPECTRA", "informationUri": "https://spectramethod.dev",
                                "rules": rules}},
            "results": results,
        }],
    }
    return json.dumps(doc, indent=2)


def to_csv(findings: list[dict[str, Any]]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=CSV_COLUMNS, extrasaction="ignore")
    writer.writeheader()
    for f in findings:
        writer.writerow({
            "id": _csv_safe(f.get("id")),
            "title": _csv_safe(f.get("title", f.get("name", f.get("id")))),
            "severity": _csv_safe(_norm_sev(f.get("severity"))),
            "status": _csv_safe(str(f.get("status", "open")).lower()),
            "cvss": _csv_safe(f.get("cvss", f.get("cvss_score", ""))),
            "remediation": _csv_safe(f.get("remediation", f.get("recommendation", ""))),
            "source_path": _csv_safe(f.get("source_path", "")),
        })
    return buf.getvalue()


def to_markdown(findings: list[dict[str, Any]]) -> str:
    if not findings:
        return "# Remediation\n\n_No findings to export._\n"
    lines = ["# Remediation Pack\n",
             f"{len(findings)} finding(s). One section per item — ready to paste into a tracker.\n"]
    for f in findings:
        fid = f.get("id")
        sev = _norm_sev(f.get("severity")).upper()
        title = f.get("title", f.get("name", fid))
        lines.append(f"\n## [{sev}] {title}  \n`{fid}`\n")
        if f.get("cvss") or f.get("cvss_score"):
            lines.append(f"- **CVSS:** {f.get('cvss', f.get('cvss_score'))}")
        lines.append(f"- **Status:** {str(f.get('status', 'open')).lower()}")
        if f.get("description"):
            lines.append(f"\n**Description**\n\n{f['description']}\n")
        if f.get("remediation") or f.get("recommendation"):
            lines.append(f"\n**Remediation**\n\n{f.get('remediation', f.get('recommendation'))}\n")
    return "\n".join(lines) + "\n"


EXPORTERS = {"sarif": to_sarif, "csv": to_csv, "md": to_markdown}


def export(engagement_path: str, fmt: str) -> str:
    if fmt not in EXPORTERS:
        raise ValueError(f"unknown format {fmt!r}; choose from {', '.join(sorted(EXPORTERS))}")
    return EXPORTERS[fmt](load_findings(engagement_path))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cmd_export(args: argparse.Namespace) -> None:
    try:
        out = export(args.engagement, args.format)
        if args.out:
            Path(args.out).write_text(out, encoding="utf-8")
    except (FileNotFoundError, IsADirectoryError, PermissionError, OSError,
            ValueError, KeyError, RuntimeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    if args.out:
        print(json.dumps({"written": str(Path(args.out).resolve()), "format": args.format}))
    else:
        sys.stdout.write(out if out.endswith("\n") else out + "\n")
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="remediation-export.py",
        description="Export engagement findings into remediation-ready formats.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("export", help="Export findings as sarif, csv, or md")
    p.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p.add_argument("--format", required=True, choices=sorted(EXPORTERS),
                   help="Output format")
    p.add_argument("--out", help="Write to file instead of stdout")
    p.set_defaults(func=cmd_export)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
