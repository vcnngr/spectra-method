# Step 02 - Data Exposure Analysis

## STEP GOAL

Classify potentially affected data, subjects, systems, volumes, and exposure confidence.

## MANDATORY EXECUTION RULES

- Minimize personal data copied into the artifact.
- Use counts, classes, and references where possible.
- Agent Autonomy Protocol: do not request or expose raw sensitive data unless strictly necessary and authorized.

## REQUIRED OUTPUT

Append data class, subject type, estimated volume, exposure vector, evidence reference, and confidence.

SUCCESS: Exposure is classified without unnecessary data replication.

FAILURE: Artifact stores raw personal data or unclear estimates.

## NEXT STEP

Read `./steps-c/step-03-jurisdiction-clock.md`.
