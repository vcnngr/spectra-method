---
name: spectra-remediation-export
description: 'Export an engagement''s findings into remediation-ready, tool-agnostic formats — SARIF, CSV, or a Markdown ticket pack. Use to hand findings to engineering, CI, or a tracker.'
---

# SPECTRA Remediation Export

## Overview

A finding is only useful when engineering can act on it. SPECTRA turns an engagement's findings into remediation-ready, tool-agnostic artifacts — and stops there, on purpose. This is a deterministic **export**, not a live integration: no network, no credentials, no third-party API. You take the output and feed it to whatever system you already run.

Three formats cover the common destinations:

- **SARIF** (2.1.0) — for code-scanning dashboards and CI gates; one result per finding, severity mapped to error/warning/note.
- **CSV** — for spreadsheets and issue trackers; one row per finding with id, title, severity, status, CVSS, source.
- **Markdown ticket pack** — one paste-ready section per finding, with description and remediation.

Keeping this an export (not an integration) is what keeps SPECTRA a method rather than a ticketing platform.

## Deterministic runtime (Layer 3)

```bash
python3 {project-root}/_spectra/core/execution/remediation-export.py export \
  --engagement "{engagement_yaml}" --format sarif --out findings.sarif
```

Formats: `sarif`, `csv`, `md`. With no `--out`, the export is written to stdout. Findings are read from the engagement's `findings/` directory (the same source the report generator uses), so the export always matches the report.

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — store config vars.
2. **Detect the active engagement** and confirm findings exist under its `findings/` directory.
3. **Confirm the destination** with the operator (CI/SARIF, tracker/CSV, or a ticket pack/Markdown).
4. **Export** in the chosen format; hand the file to the downstream system.

## Boundary

This skill only reads the engagement's findings and writes an export file. It never contacts an external system, never carries credentials, and never modifies findings. The operator owns the handoff to any tracker or pipeline.
