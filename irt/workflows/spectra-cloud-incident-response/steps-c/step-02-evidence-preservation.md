# Step 02 - Evidence Preservation

## STEP GOAL

Preserve cloud evidence sources before volatile data expires or containment changes state.

## MANDATORY EXECUTION RULES

- Identify logs, snapshots, flow records, audit events, SaaS audit trails, and Kubernetes events.
- Prefer immutable export or documented snapshot procedure.
- Agent Autonomy Protocol: do not delete, rewrite, or suppress audit trails.

## REQUIRED OUTPUT

Append evidence source, retention window, export method, hash/checksum if available, owner, and gaps.

SUCCESS: Critical cloud evidence has a preservation plan.

FAILURE: Volatile evidence may expire without documented action.

## NEXT STEP

Read `./steps-c/step-03-blast-radius.md`.
