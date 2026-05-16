# Step 02 - Surface Map

## STEP GOAL

Build a testable map of application routes, APIs, roles, trust boundaries, and sensitive data flows.

## MANDATORY EXECUTION RULES

- Use provided documentation, OpenAPI specs, routes, screenshots, logs, or code references.
- Do not crawl or fuzz production unless explicitly allowed.
- Agent Autonomy Protocol: stop if discovery expands beyond approved hosts, tenants, or accounts.

## REQUIRED OUTPUT

Append:

- endpoint inventory
- role and permission model
- data classes and flows
- third-party integrations
- assumptions and unknowns

SUCCESS: Assessment surface is mapped to roles and data classes.

FAILURE: Routes or trust boundaries remain too vague for controlled testing.

## NEXT STEP

Read `./steps-c/step-03-auth-session-review.md`.
