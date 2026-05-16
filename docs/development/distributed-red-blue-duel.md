# Distributed Red/Blue Duel

## Purpose

Distributed Red/Blue Duel describes how SPECTRA supports Red/Blue exercises across separate machines, sessions, or operators. The model measures detection, mitigation, and coordination without blurring role boundaries or turning the exercise into anti-forensics.

The design is intentionally ledger-first:

- Red records activity and intent in its own ledger.
- Blue records telemetry, detections, mitigations, and misses in its own ledger.
- Referee imports both ledgers, correlates events, and produces the scorecard.
- No role retroactively modifies another role's ledger.

## Roles

### Red

Red operates as an authorized adversary emulator. It must stay within the engagement, scope, and Rules of Engagement. Duel Mode does not give Red permission to delete traces or disable defenses; it models OPSEC as noise reduction, footprint control, and measurable choices of timing or technique.

Typical events:

- `planned_action`: planned action or operational hypothesis.
- `action`: action performed within scope.
- `observation`: outcome observed by Red.
- `handoff`: information handed to Referee or a later phase.

### Blue

Blue operates as the defender. It observes telemetry, validates detections, proposes mitigations, and records misses when a signal is not detected. Blue Live Adapter can feed the ledger from local logs in read-only mode.

Typical events:

- `observation`: observed signal or context.
- `detection`: detection with technique, target, source, and confidence.
- `mitigation`: control or response applied.
- `miss`: Red activity that was not detected or was detected late.
- `handoff`: handoff to IRT, GRC, or Referee.

### Referee

Referee keeps the correlation view. It does not replace Red or Blue; it compares events, timestamps, targets, and techniques to produce a scorecard.

Typical events:

- `checkpoint`: exercise state.
- `correlation`: mapping between a Red event and a Blue event.
- `decision`: scoring or interpretation decision.
- `score`: interim or final result.

## Separate Visibility

Separation is part of the model. Red sees its own plan, actions, and shared scope. Blue sees telemetry, alerts, controls, and its own detections. Referee can read both sides for scoring.

This separation avoids two common errors:

- Blue detecting activity because it has artificial knowledge of the Red plan.
- Red optimizing against Blue details that would not be available in a realistic exercise.

The ledger-only format keeps the separation inspectable: each event has a role, type, summary, timestamp, target, technique, source, confidence, severity, and artifacts.

## Operating Flow

1. Create or verify an authorized engagement.
2. Initialize Duel sessions for Red, Blue, and Referee with the same `session_id`.
3. Generate a Party Mode v2 plan with explicit lanes when the work needs multiple perspectives:

```bash
spectra party plan --topic "distributed duel readiness" --mode purple --lanes red,blue,irt,grc,core
```

4. Have Red record planned or observed activity within the Rules of Engagement.
5. Have Blue record observations, detections, mitigations, and misses.
6. Use Blue Live or Blue Tail, when useful, for read-only defensive log ingestion.
7. Export local ledgers with Red/Blue Broker when roles run on different machines.
8. Import bundles into the Referee workspace.
9. Have Referee produce correlations and a scorecard.
10. Move results into reporting, detection backlog, mitigation planning, or IRT/GRC follow-up.

Party Mode v2 does not execute actions. It produces work contracts for sub-agents: required inputs, mandatory outputs, completion criteria, quality gates, and merge contracts. This makes each lane's deliverables explicit before Referee or Chronicle produce synthesis and reports.

## Blue Live And Blue Tail

Blue Live Adapter reads local defensive sources and normalizes Blue events. Current runtime source types include `auth`, `nginx_access`, `nginx_error`, `postfix`, `dovecot`, `fail2ban`, `suricata_eve`, `wazuh`, `zeek_conn`, `zeek_dns`, and `zeek_http`.

Blue Tail adds checkpointing. In tail mode, it reads only the new portion of files already processed. This allows repeated runs without duplicating old detections. Incomplete trailing lines remain pending until a newline arrives, so the ledger does not contain truncated detections.

Important constraint: Blue Live and Blue Tail are read-only. They do not delete, rotate, rewrite, or repair logs. They do not apply firewall rules, restart services, or modify hosts.

## Red/Blue Broker

Red/Blue Broker supports offline ledger exchange across separated machines. Each role exports a JSON bundle from its local ledger:

```bash
spectra broker export --session ENG-2026-001 --role red --bundle red-bundle.json
spectra broker export --session ENG-2026-001 --role blue --bundle blue-bundle.json
```

Referee imports the bundles into its workspace:

```bash
spectra broker import --session ENG-2026-001 --role red --bundle red-bundle.json
spectra broker import --session ENG-2026-001 --role blue --bundle blue-bundle.json
spectra duel score --session ENG-2026-001 --output scorecard.md
```

Each bundle contains type, bundle schema version, event schema version, session, role, export timestamp, events, and a SHA256 checksum of the event payload. Import verifies checksum, event count, session, role, bundle schema, event schema, and minimum event fields. Unknown event fields are stripped before writing the ledger, then already-present events are deduplicated.

The broker does not open sockets, run listeners, install remote agents, or control hosts. It is an explicit file exchange mechanism suitable for truly separated Red and Blue workspaces.

## Scorecard

The scorecard must remain explainable. Every score must trace back to ledger events.

Recommended metrics:

- detection latency: time between Red action and correlated Blue detection.
- severity coverage: share of Red events detected by severity.
- technique misses: techniques not detected or detected with low confidence.
- mitigation coverage: events with a response or applied control.
- outcome grade: final summary derived from metrics, not impressions.

When a correlation is missing, Referee must distinguish between:

- no telemetry available.
- telemetry available but not analyzed.
- detection absent.
- detection present but not mapped to the correct technique.
- mitigation present but late or incomplete.

## Scope Guardrails

Duel Mode does not weaken SPECTRA controls. Every Red event must remain within scope and Rules of Engagement. Every Blue event must identify its source and observed target. Referee must flag any mismatch between ledger and scope.

Examples of violations:

- Red records action against an excluded target.
- Red proposes a technique not authorized by the Rules of Engagement.
- Blue imports logs from unauthorized systems without context.
- Referee assigns a score without a correlatable event.

## Safety Boundary

The model allows OPSEC as measurement, not as evidence deletion.

Forbidden behaviors:

- deleting, altering, or hiding logs.
- tampering with audit trails.
- disabling EDR, SIEM, auditd, Sysmon, Defender, or logging.
- destructive cleanup.
- removing artifacts to prevent detection.
- creating unauthorized persistence.

Allowed behaviors within authorization:

- planning low-and-slow activity.
- measuring how much noise a technique produces.
- comparing techniques for detection coverage.
- recording footprint and telemetry sources.
- validating detection rules.
- proposing mitigations.
- producing scorecards and improvement backlogs.

The expected result is not "invisible Red." The expected result is an honest measurement: which signals were produced, which signals Blue saw, which signals were missed, which controls worked, and which controls need improvement.
