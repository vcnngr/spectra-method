# Step 02 - Source Coverage

## STEP GOAL

Map available log sources to assets, identity systems, network paths, cloud services, applications, and ATT&CK coverage.

## MANDATORY EXECUTION RULES

- Separate expected sources from observed sources.
- Mark business-critical assets with missing logs.
- Agent Autonomy Protocol: do not infer visibility where no events exist.

## REQUIRED OUTPUT

Append coverage matrix: asset, source, collection method, coverage status, ATT&CK relevance, and owner.

SUCCESS: Coverage gaps are visible by asset and technique.

FAILURE: Review only lists sources without mapping them to detection needs.

## NEXT STEP

Read `./steps-c/step-03-schema-quality.md`.
