# Step 02 - Ledger Integrity

## STEP GOAL

Validate imported Red and Blue ledger integrity before correlation.

## MANDATORY EXECUTION RULES

- Check event counts, role, session, timestamp order, schema versions, and hashes where available.
- Quarantine unknown fields rather than trusting them.
- Agent Autonomy Protocol: do not accept tampered, partial, or cross-session evidence silently.

## REQUIRED OUTPUT

Append integrity status, warnings, rejected events, schema notes, and evidence gaps.

SUCCESS: Ledgers are trustworthy enough to correlate.

FAILURE: Integrity errors make scoring unreliable.

## NEXT STEP

Read `./steps-c/step-03-timeline-correlation.md`.
