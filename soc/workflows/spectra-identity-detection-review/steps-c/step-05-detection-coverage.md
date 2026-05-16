# Step 05 - Detection Coverage

## STEP GOAL

Map identity risks to detections, log sources, alert rules, playbooks, and response actions.

## MANDATORY EXECUTION RULES

- Map each risk to ATT&CK and required event fields.
- Distinguish missing telemetry from weak detection logic.
- Agent Autonomy Protocol: no auto-response recommendation without human gate and rollback path.

## REQUIRED OUTPUT

Append coverage matrix: risk, data source, event fields, current detection, gap, owner, and next action.

SUCCESS: Identity detection gaps are actionable.

FAILURE: Gap list cannot drive detection engineering.

## NEXT STEP

Read `./steps-c/step-06-response-readiness.md`.
