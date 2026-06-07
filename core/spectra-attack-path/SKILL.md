---
name: spectra-attack-path
description: 'Generate an evidence-anchored attack-path graph from engagement kill-chain and findings, with optional Blue detection overlay. Use to visualize how findings chain into impact and where detection gaps are.'
---

# SPECTRA Attack-Path Graph

## Overview

A list of findings is not an attack. Attackers do not exploit vulnerabilities in isolation — they chain them: a low-severity information leak feeds a medium-severity misconfiguration, which enables a critical remote code execution, which reaches the objective. A flat findings table hides that story. The attack-path graph tells it.

This skill turns data SPECTRA already tracks — the engagement `kill_chain`, the findings registry, and the evidence registry — into a serializable attack-path graph: nodes for the entry point, the active kill-chain phases, each finding, and the terminal impact; edges that show how exploitation progresses and how findings escalate toward impact. When a Duel Mode Blue ledger is supplied, the graph is overlaid with **honest detection status**: which techniques Blue actually evidenced detecting, and which it missed.

This is a SPECTRA-native artifact, not a generic diagram:

- **Evidence over assumption.** Verification is a property of the evidence registry (`spectra-evidence-chain` / `evidence-logger.py`), never of a finding field. The graph resolves each finding's claimed evidence references against the real `evidence-registry.yaml` — in both directions (finding → registry item id, and registry `finding_reference` → finding) — and reports an honest `evidence_state`. It only reaches `integrity_verified` when references resolve **and** the registry integrity status is `VERIFIED`. A finding whose references do not resolve is surfaced, never silently trusted. A path without resolved evidence is a hypothesis, and the graph says so.
- **Honest measurement, not "invisible Red".** Detection status comes only from Blue telemetry in the duel ledger, never from prior knowledge of the Red plan. Missed techniques are the point: they are the detection-gap backlog.
- **Modeling only.** This skill MODELS authorized attack paths from recorded results. It never connects to a target, never executes anything, and never modifies a host. It is read-only over engagement artifacts and fully respects the SPECTRA safety boundary.

The graph is consumed by Chronicle (`spectra-agent-chronicle`) for reporting, by Referee (`spectra-agent-referee`) to credit chained Red outcomes and quantify detection coverage during Duel adjudication, and by Specter (`spectra-agent-specter`) for rapid cross-domain impact framing.

## Deterministic runtime (Layer 3)

Mechanical graph assembly is handled by a deterministic generator. Use it directly:

```bash
python3 {project-root}/_spectra/core/execution/attack-path-generator.py generate \
  --engagement "{engagement_yaml}" \
  --output "{attack_path_json}" \
  --mermaid "{attack_path_mmd}"
```

Add a detection overlay from a Duel Mode Blue ledger:

```bash
python3 {project-root}/_spectra/core/execution/attack-path-generator.py generate \
  --engagement "{engagement_yaml}" \
  --duel-ledger "{blue_ledger_jsonl}" \
  --output "{attack_path_json}" \
  --mermaid "{attack_path_mmd}"
```

The generator emits `attack-path.json` (schema `spectra.attack-path/v1`: `summary`, `nodes`, `edges`) and an optional Mermaid `flowchart LR` render suitable for embedding in a report. With no `--output`/`--mermaid` it prints the full graph JSON to stdout; otherwise it prints a summary.

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — Store all returned vars for use:
   - Use `{user_name}` from config for greeting
   - Use `{communication_language}` from config for all communications
   - Use `{document_output_language}` from config for all document content
   - Use `{engagement_artifacts}` for locating engagement files
   - Use `{evidence_artifacts}` for evidence registry paths
   - Use `{report_artifacts}` for graph output paths
   - Store any other config variables as `{var-name}` and use appropriately

2. **Detect active or completed engagement:**
   - Search `{engagement_artifacts}/*/engagement.yaml` for engagements with `status: "active"` or `status: "complete"`
   - If multiple found, present the list and ask the user to select one
   - If none found, halt and recommend: "No engagements found. Use `spectra-new-engagement` to create one before building an attack-path graph."
   - Load the selected `engagement.yaml` as operational context

3. **Offer a detection overlay (optional):**
   - If a Duel Mode session exists for this engagement, ask whether to overlay Blue detection status from its ledger
   - If yes, locate the Blue ledger (JSONL) and pass it as `--duel-ledger`

4. **Generate the graph:**
   - Run the Layer-3 generator with `--output` and `--mermaid` pointed at `{report_artifacts}`
   - Report the summary: node/edge counts, findings chained to impact, unverified findings, and — when overlaid — detection coverage and missed techniques

## Reading the graph

Each finding node carries an honest `evidence_state` (weakest → strongest):

| `evidence_state` | Meaning |
|---|---|
| `no_reference` | Nothing links this finding to any evidence. |
| `registry_missing` | The finding claims references but `evidence-registry.yaml` is absent. |
| `referenced_unresolved` | References exist but none resolve to a registry item. |
| `partially_resolved` | Some references resolve to registry items; others dangle. |
| `resolved_unverified` | All references resolve, but registry integrity is `UNVERIFIED`. |
| `resolved_integrity_failed` | References resolve, but registry integrity is `FAILED`. |
| `integrity_verified` | All references resolve **and** registry integrity is `VERIFIED`. |

Only `resolved_unverified` and `integrity_verified` count toward `evidence_backed_findings`; everything else is counted in `unsupported_findings` and flagged `[unverified]` in the Mermaid render.

- **`unsupported_findings` / the `evidence_breakdown`** — claims not backed by resolved evidence. Treat them as hypotheses; resolve, verify, or downgrade before they appear in a client deliverable. Run `spectra-evidence-chain` to register and verify the underlying artifacts.
- **`chained_to_impact`** — high/critical findings that reach the objective. These are the paths to lead with.
- **Missed techniques (`detected: false`)** — the detection-gap backlog. Hand these to the detection engineer (`spectra-agent-detection-eng`) via `spectra-detection-lifecycle`.
- **Coverage ratio** — detected techniques over techniques observed in the path. This is an honest exercise metric, not a Red success/failure score.

## Boundary

This skill never executes attack steps. It documents and visualizes authorized, already-recorded activity. It does not delete, alter, or hide any data, and it does not weaken any control. The graph exists to improve the next exercise — to show which paths worked, which were evidenced, and which signals defenders need to add.
