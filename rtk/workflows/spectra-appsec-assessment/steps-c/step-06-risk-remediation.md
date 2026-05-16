# Step 06 - Risk And Remediation

## STEP GOAL

Convert observations into prioritized findings with severity, likelihood, business impact, and remediation.

## MANDATORY EXECUTION RULES

- Calibrate severity with exploitability, reachability, privileges, data sensitivity, and compensating controls.
- Separate confirmed findings from hypotheses.
- Agent Autonomy Protocol: do not overstate impact beyond evidence.

## REQUIRED OUTPUT

Append a findings table with:

- ID
- title
- evidence
- affected asset
- severity rationale
- owner
- fix recommendation
- retest method

SUCCESS: Each finding is fixable and evidence-backed.

FAILURE: Findings lack owner, evidence, or retest criteria.

## NEXT STEP

Read `./steps-c/step-07-handoff.md`.
