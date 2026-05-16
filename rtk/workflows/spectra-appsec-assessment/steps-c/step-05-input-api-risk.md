# Step 05 - Input And API Risk

## STEP GOAL

Review input validation, API schema enforcement, upload handling, SSRF exposure, injection risk, and error handling.

## MANDATORY EXECUTION RULES

- Use benign probes and static evidence unless active testing is authorized.
- Keep payloads non-destructive and non-persistent.
- Agent Autonomy Protocol: do not provide exploit chains, shell payloads, destructive injection, or blind exfiltration techniques.

## REQUIRED OUTPUT

Append:

- API contract gaps
- validation failures
- upload and parser risks
- error leakage
- recommended safe retest method

SUCCESS: Input/API risks are classified with safe validation evidence.

FAILURE: Testing creates uncontrolled execution, data loss, or service instability.

## NEXT STEP

Read `./steps-c/step-06-risk-remediation.md`.
