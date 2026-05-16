# Step 01 - Adjudication Intake

## STEP GOAL

Open the Duel adjudication record and verify session, ledgers, RoE, and scoring policy.

## MANDATORY EXECUTION RULES

- Require Red and Blue evidence sources.
- Verify session IDs and event schema compatibility.
- Agent Autonomy Protocol: block scoring for out-of-scope or destructive actions.

## REQUIRED OUTPUT

Append session ID, ledger sources, schema versions, RoE reference, scoring model, and disclosure state.

SUCCESS: Adjudication inputs are complete.

FAILURE: Session, ledger, or RoE mismatch is unresolved.

## NEXT STEP

Read `./steps-c/step-02-ledger-integrity.md`.
