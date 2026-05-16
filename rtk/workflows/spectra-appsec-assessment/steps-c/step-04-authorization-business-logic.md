# Step 04 - Authorization And Business Logic

## STEP GOAL

Evaluate object-level authorization, function-level authorization, tenant isolation, workflow integrity, and abuse cases.

## MANDATORY EXECUTION RULES

- Prefer role matrix review and controlled request comparison.
- Minimize data access; prove impact with metadata or synthetic records.
- Agent Autonomy Protocol: block mass enumeration, privilege escalation on real users, payment abuse, or irreversible workflow actions.

## REQUIRED OUTPUT

Append:

- role-to-action matrix
- authorization test cases
- business rules tested
- tenant/data isolation observations
- evidence and impact notes

SUCCESS: Authorization and logic risks have reproducible safe cases.

FAILURE: Testing changes real business state without approval.

## NEXT STEP

Read `./steps-c/step-05-input-api-risk.md`.
