---
name: spectra-help
description: 'Analyzes current state and user query to answer SPECTRA questions or recommend the next skill(s) to use. Use when user asks for help, spectra help, what to do next, or what to start with.'
---

# SPECTRA Help

## Overview

Help the user understand where they are in their SPECTRA workflow and what to do next. Answer SPECTRA questions when asked.

## On Activation

1. Read `skill-manifest.csv` to load the full skill catalog
2. Check for an active engagement in the engagement artifacts directory
3. Determine the user's current position in the workflow
4. Present contextually relevant recommendations

## Desired Outcomes

When this skill completes, the user should:

1. **Know where they are** — which module and phase they're in, whether an engagement is active, which kill chain phase is current
2. **Know what to do next** — the next recommended and/or required step, with clear reasoning
3. **Know how to invoke it** — skill name, menu code, action context, and any args that shortcut the conversation
4. **Get offered a quick start** — when a single skill is the clear next step, offer to run it for the user right now rather than just listing it
5. **Feel oriented, not overwhelmed** — surface only what's relevant to their current position; don't dump the entire catalog

## Data Sources

- **Catalog**: `{project-root}/_spectra/_config/skill-manifest.csv` — assembled manifest of all installed module skills
- **Config**: `config.yaml` files in `{project-root}/_spectra/` and its subfolders — resolve `output-location` variables, provide `communication_language` and engagement context
- **Active Engagement**: If an engagement is active, check `{engagement_artifacts}/{engagement_id}/engagement.yaml` for current state, scope, and kill chain progress
- **Agent Manifest**: `{project-root}/_spectra/_config/agent-manifest.csv` — available agents and their capabilities

## Skill Organization by Module

Present skills organized by security operations domain:

### CORE — Engagement Management & Coordination
Core skills for engagement lifecycle, multi-agent coordination, and cross-module operations.

### RTK — Red Team Toolkit
Offensive security skills: reconnaissance, exploitation, lateral movement, exfiltration. Red team agents and attack workflows.

### SOC — Security Operations Center
Defensive skills: alert triage, threat hunting, detection engineering. Blue team agents and monitoring workflows.

### IRT — Incident Response Team
Response skills: incident handling, digital forensics, malware analysis, threat intelligence. Response agents and investigation workflows.

### GRC — Governance, Risk & Compliance
Governance skills: risk assessment, compliance audit, policy lifecycle. GRC agents and audit workflows.

## CSV Interpretation

The catalog uses this format:

```
canonicalId,name,description,module,path,install_to_spectra
```

**Module grouping** determines skill organization:
- `core` — available regardless of engagement state
- `rtk` — red team / offensive skills
- `soc` — blue team / defensive skills
- `irt` — incident response skills
- `grc` — governance, risk & compliance skills

**Engagement State Detection:**
- If no active engagement → recommend `spectra-new-engagement` or `spectra-agent-specter`
- If engagement active → check kill chain status and recommend next phase skill
- If engagement complete → recommend `spectra-debrief` or `spectra-close-engagement`

## Response Format

For each recommended item, present:
- `[menu-code]` **Display name** — e.g., "[NE] New Engagement"
- Skill name in backticks — e.g., `spectra-new-engagement`
- For agent skills: agent invocation context — e.g., "talk to Specter for a rapid assessment"
- Description from CSV or your existing knowledge of the skill
- Module tag — e.g., `[CORE]`, `[RTK]`, `[SOC]`, `[IRT]`, `[GRC]`

**Ordering**: Show contextually relevant items first, then optional items. Make it clear which is the recommended next step.

## Quick Agent Reference

When the user asks "who can help with X", reference the agent manifest to suggest the right agent:

| Agent | Persona | Module | Best For |
|-------|---------|--------|----------|
| Specter | CISO / Quick Ops | CORE | Cross-domain assessment, strategic oversight |
| Viper | Red Team Lead | RTK | Attack strategy, engagement planning |
| Ghost | Recon Specialist | RTK | OSINT, reconnaissance |
| Razor | Exploit Developer | RTK | Vulnerability exploitation |
| Phantom | Attack Operator | RTK | Post-exploitation, lateral movement |
| Mirage | Social Engineer | RTK | Social engineering assessment |
| Blade | Quick Pentester | RTK | Rapid vulnerability assessment |
| Commander | SOC Manager | SOC | SOC operations, metrics |
| Watchdog | L1 Triage | SOC | Alert triage |
| Tracker | L2 Investigator | SOC | Incident investigation |
| Hawk | L3 Threat Hunter | SOC | Proactive threat hunting |
| Sentinel | Detection Engineer | SOC | Detection rule authoring |
| Shield | Quick SOC Analyst | SOC | Rapid alert analysis |
| Dispatch | Incident Handler | IRT | Incident coordination |
| Trace | Forensic Analyst | IRT | Digital forensics |
| Scalpel | Malware Analyst | IRT | Malware reverse engineering |
| Oracle | Threat Intel Analyst | IRT | Threat intelligence |
| Surge | Quick Responder | IRT | Rapid incident response |
| Arbiter | Risk Analyst | GRC | Risk assessment |
| Auditor | Compliance Auditor | GRC | Compliance assessment |
| Scribe | Policy Author | GRC | Policy documentation |

## Constraints

- Present all output in `{communication_language}`
- Recommend running each skill in a **fresh context window** when appropriate
- Match the user's tone — conversational when they're casual, structured when they want specifics
- If the active module is ambiguous, ask rather than guess
- If an engagement is active, always show its status summary before recommendations
