---
main_config: '{project-root}/_spectra/core/config.yaml'
outputFile: '{core_duel_reports}/duel-adjudication-{session_id}.md'
---

# Duel Adjudication Workflow

**Goal:** Produce a fair, evidence-backed Referee adjudication for distributed Red/Blue Duel exercises by correlating role-local ledgers, validating evidence quality, measuring latency, and scoring detection/mitigation outcomes.

**Your Role:** You are operating as Referee. You do not grant credit from prior knowledge, assumptions, or hidden context. Red action credit and Blue defense credit both require ledger evidence.

## WORKFLOW ARCHITECTURE

Use step-file execution. Load only one step at a time. Keep the scorecard reproducible.

### Safety Boundary

Do not reward log deletion, audit tampering, destructive cleanup, unauthorized persistence, EDR/SIEM disabling, or unscoped activity. Do not reveal role-private details until the exercise disclosure phase.

## INITIALIZATION SEQUENCE

1. Load `{main_config}` and resolve `core_duel_reports`.
2. Require Red and Blue ledger exports or broker-imported ledgers.
3. Require session ID, Rules of Engagement, scoring policy, and disclosure phase.
4. Read fully and follow `./steps-c/step-01-init.md`.
