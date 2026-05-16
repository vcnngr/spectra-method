# Step 03 - Blast Radius

## STEP GOAL

Assess affected identities, workloads, storage, network paths, secrets, data classes, and cross-account impact.

## MANDATORY EXECUTION RULES

- Use read-only resource graph, IAM, network, and audit evidence.
- Mark assumptions and unknowns.
- Agent Autonomy Protocol: do not enumerate outside authorized accounts, tenants, projects, or clusters.

## REQUIRED OUTPUT

Append resource graph summary, likely access path, affected data stores, identities, regions, and confidence.

SUCCESS: Incident impact is bounded enough for containment planning.

FAILURE: Containment would be blind or over-broad.

## NEXT STEP

Read `./steps-c/step-04-containment-plan.md`.
