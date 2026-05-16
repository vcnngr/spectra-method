# Step 01 - Assessment Intake

## STEP GOAL

Create the AppSec assessment record, verify authorization, and define exact application/API boundaries.

## MANDATORY EXECUTION RULES

- Load the active engagement before assessing any target.
- Confirm target application, environment, domains, API base URLs, test accounts, rate limits, and prohibited actions.
- Agent Autonomy Protocol: hard block destructive testing, credential theft, persistence, production data extraction, and out-of-scope endpoints.
- If the operator cannot prove authorization, stop.

## REQUIRED OUTPUT

Append:

- assessment ID and date
- in-scope applications/APIs
- environments and accounts
- allowed test classes
- forbidden actions
- evidence storage path

SUCCESS: Scope, authorization, and data handling rules are explicit.

FAILURE: Target, account, environment, or data boundary is ambiguous.

## NEXT STEP

When complete, read `./steps-c/step-02-surface-map.md`.
