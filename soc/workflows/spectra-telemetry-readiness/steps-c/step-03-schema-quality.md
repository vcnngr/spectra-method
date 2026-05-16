# Step 03 - Schema And Parser Quality

## STEP GOAL

Evaluate whether events are parsed, normalized, timestamped, and field-complete enough for detection and investigation.

## MANDATORY EXECUTION RULES

- Use representative samples.
- Preserve raw examples with sensitive values redacted.
- Agent Autonomy Protocol: no parser changes in production without change control.

## REQUIRED OUTPUT

Append parsing status, required fields, missing fields, timestamp accuracy, normalization issues, and sample evidence.

SUCCESS: Parser quality is measurable.

FAILURE: Field gaps are hidden behind generic "logs exist" statements.

## NEXT STEP

Read `./steps-c/step-04-retention-integrity.md`.
