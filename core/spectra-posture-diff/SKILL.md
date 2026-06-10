---
name: spectra-posture-diff
description: 'Make an engagement repeatable over time: snapshot its security posture and diff two snapshots into a scored delta (improved / regressed). Use to re-assess the same scope and measure change.'
---

# SPECTRA Posture Diff

## Overview

A penetration test is usually a one-shot photograph; security is a moving picture. SPECTRA closes that gap on its own terms — without becoming a vulnerability-management platform. A **posture snapshot** is built only from the engagement's own artifacts (its `findings/` directory, its scope, its run log), and two snapshots diff into a deterministic, severity-weighted delta: what was resolved, what is new, what persists, and what escalated.

This is the SPECTRA-native answer to "are we better or worse than last time?" — a scored verdict the Referee and the report can build on, not a live dashboard. Recurring engagements become a trend line instead of disconnected reports.

## Deterministic runtime (Layer 3)

Capture a snapshot of the current posture (run it again on a later occasion):

```bash
python3 {project-root}/_spectra/core/execution/posture-diff.py snapshot \
  --engagement "{engagement_yaml}"
```

Diff the two most recent snapshots (or pass explicit `--from`/`--to`):

```bash
python3 {project-root}/_spectra/core/execution/posture-diff.py diff \
  --engagement "{engagement_yaml}"
```

Snapshots are append-only under `<engagement_dir>/posture/<timestamp>.json`. The diff reports `added`, `resolved`, `persisting`, and `escalations`, plus a `score` (positive = improved) and a `verdict` of `improved` / `regressed` / `unchanged`. Severity weights: critical 5, high 4, medium 3, low 2, informational 1 — resolving a critical improves posture more than resolving an info; introducing or escalating one regresses it.

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — store `{engagement_artifacts}` and other config vars.
2. **Detect the active engagement** and confirm findings exist under its `findings/` directory.
3. **Snapshot** the current posture; on a later re-assessment, snapshot again.
4. **Diff** the snapshots, present the scored delta, and feed it into the report or a Referee comparison.

## Boundary

This skill only reads an engagement's own artifacts and writes posture snapshots beside it. It does not scan, execute, or reach across engagements; it is a deterministic comparison, never a continuous-monitoring service. Findings remain the source of truth — the posture score is a summary of them, not a replacement.
