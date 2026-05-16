# Step 01 - Cloud Incident Intake

## STEP GOAL

Create the cloud incident record and define platform, assets, authority, severity, and initial evidence.

## MANDATORY EXECUTION RULES

- Verify incident authorization and cloud account boundaries.
- Preserve original alerts, timestamps, account IDs, regions, and resource IDs.
- Agent Autonomy Protocol: block unapproved containment, key rotation, deletion, or workload shutdown.

## REQUIRED OUTPUT

Append incident ID, cloud scope, affected assets, initial indicators, severity, stakeholders, and evidence path.

SUCCESS: Incident scope and authority are clear.

FAILURE: Cloud account, tenant, or authorization is uncertain.

## NEXT STEP

Read `./steps-c/step-02-evidence-preservation.md`.
