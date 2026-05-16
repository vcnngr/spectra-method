# Step 05 - Blue Live Adapter Fit

## STEP GOAL

Determine whether sources can feed Blue Live Adapter or need parser/adapter work.

## MANDATORY EXECUTION RULES

- Compare source format to supported Blue Live source types.
- Identify required parser changes as engineering work, not manual workaround.
- Agent Autonomy Protocol: do not open sockets, deploy agents, or modify remote hosts from this workflow.

## REQUIRED OUTPUT

Append source-to-adapter mapping, unsupported formats, sample lines, parser needs, and test commands.

SUCCESS: Blue Live readiness is explicit.

FAILURE: Unsupported source is treated as ingest-ready.

## NEXT STEP

Read `./steps-c/step-06-detection-gap-map.md`.
