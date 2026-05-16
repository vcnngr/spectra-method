# red-blue-team Origin

## Purpose

The `red-blue-team` directory is the incubation workspace from which `spectra-method` emerged. It is not the public package, it is not the canonical installable source, and it should not be treated as a stable runtime. It is a corpus of analysis, prototypes, architecture experiments, and reference material used to define the SPECTRA model.

Its main value is historical and architectural:

- it preserves early decisions about agents, workflows, modules, and operating style.
- it shows how BMAD patterns were studied and adapted.
- it contains useful examples for understanding why SPECTRA separates Red, Blue, IRT, GRC, and Core.
- it provides a comparison point when evaluating whether a new feature still fits the original intent.

## Relationship With BMAD

SPECTRA was created by reusing multi-agent orchestration concepts already present in BMAD, not by copying the BMAD domain. From BMAD, SPECTRA mainly borrowed structural patterns:

- agents with declared identity, role, principles, and capabilities.
- step-based workflows with progressive loading.
- Party Mode as a multi-perspective conversation pattern.
- manifests and registries that make agents and skills discoverable.
- separation between coordination, execution, output, and validation.

SPECTRA adapts these patterns to authorized cybersecurity operations. The primary transformation is from generic orchestration to orchestration constrained by engagement, scope, Rules of Engagement, evidence, and operational accountability.

In SPECTRA, Red, Blue, IRT, and GRC are not decorative personas. They are distinct work domains:

- Red evaluates attack paths within scope and Rules of Engagement.
- Blue analyzes telemetry, controls, detections, and mitigations.
- IRT handles triage, containment, forensics, malware, and recovery.
- GRC translates technical risk into governance, audit, policy, and business decisions.
- Core maintains engagement state, evidence chain, reporting, and coordination.

## Relationship With spectra-method

`spectra-method` is the productized version of the work that started in `red-blue-team`. It is the versioned npm/GitHub package: installable, validated, and release-managed. It should be considered the source of truth for:

- distributable framework structure.
- CLI and installation behavior.
- public manifests and configuration.
- workflows and skills installed into consumer projects.
- support runtimes such as Party Mode, Duel Mode, and Blue Live Adapter.
- tests, validation, and package compatibility.

`red-blue-team` remains a reference corpus. It can explain intent, but it must not override what `spectra-method` has already consolidated in package code, tests, and CLI behavior. When there is a divergence, the versioned package behavior wins; the origin corpus helps determine whether the divergence is intentional or design debt.

## Relationship With spectra-playground

`spectra-playground` is a consumer example and testbed. It represents an installation that uses SPECTRA in a practical context, with engagements, operating guides, and test data. It is not the framework source of truth.

Use it to:

- verify installation and usage ergonomics.
- test end-to-end flows.
- observe how a consumer project structures engagements and outputs.
- collect feedback on documentation and CLI behavior.

Do not use it to:

- define canonical APIs.
- change manifest contracts.
- decide global safety policies.
- replace package tests or validation.

## Current Architecture Concepts

### Party Mode

Party Mode is the multi-agent planner. It produces deterministic plans for SPECTRA agents to work in parallel or in controlled disagreement. It does not automatically execute offensive actions; it assigns lanes, task contracts, expected outputs, model profiles, and safety gates.

Its primary function is to turn a complex question into coordinated work across Red, Blue, and Purple perspectives. Every plan must remain tied to engagement, authorization, scope, and Rules of Engagement.

### Duel Mode

Duel Mode models distributed Red/Blue exercises. Red, Blue, and Referee have separate views and local ledgers. Red records intent, planned actions, observations, and handoffs. Blue records observations, detections, mitigations, misses, and handoffs. Referee correlates ledgers and produces scorecards.

The key point is separation: Red and Blue do not share all state. Referee is responsible for correlating evidence and measuring whether Blue detected or mitigated Red activity within acceptable time and coverage.

### Blue Live And Blue Tail

Blue Live Adapter imports defensive telemetry in read-only mode and normalizes it into Blue events. Blue Tail uses checkpoints to read only new bytes from already-seen logs, avoiding duplicates across repeated runs.

These components do not modify logs, services, firewalls, hosts, or configurations. They are ingestion and normalization tools for feeding the Blue ledger.

### Ledger-Only Separation

Duel Mode and Blue Live are ledger-only. The framework records events and correlations; it does not provide procedures to alter artifacts, delete traces, or manipulate controls. Red/Blue separation lives in ledgers and visibility contracts, not in anti-forensics techniques.

### Scorecard

Scorecards measure the exercise. Typical metrics:

- detection latency.
- severity coverage.
- misses by technique.
- observed mitigations.
- final outcome grade.

The scorecard is not free-form narrative judgment. It must derive from ledger events, timestamps, technique, target, severity, confidence, and explicit correlations.

### Scope Guardrails

Every SPECTRA operation starts from engagement and scope. Red must not act outside the Rules of Engagement. Blue and IRT must distinguish in-scope systems, related systems, and excluded systems. GRC must avoid policy or audit work outside the authorized perimeter.

Guardrails are not bureaucracy: they are the boundary that makes the operation authorized, repeatable, and defensible.

## Safety Boundary

SPECTRA should model Red behavior as OPSEC, noise, and footprint measurement, not destructive anti-forensics.

Forbidden:

- deleting or altering logs.
- tampering with audit trails.
- destructive cleanup.
- disabling EDR, SIEM, auditd, Sysmon, Defender, or logging.
- unauthorized persistence.
- instructions for hiding evidence from Blue or IRT.

Allowed within an authorized engagement:

- low-and-slow planning within Rules of Engagement.
- measurement of generated footprint.
- noise budget tracking.
- attribution challenges.
- defensive telemetry analysis.
- detection engineering.
- Blue mitigation and recommendation work.
- Referee correlation and scorecards.

The principle is simple: Red can produce measurable signals; Blue must be able to observe, detect, or mitigate them; Referee must be able to correlate them. No part of the framework should normalize evidence deletion or weakening of security controls.
