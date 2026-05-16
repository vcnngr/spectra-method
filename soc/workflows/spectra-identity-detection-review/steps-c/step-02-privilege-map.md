# Step 02 - Privilege Map

## STEP GOAL

Map privileged roles, admin groups, service principals, break-glass accounts, and privilege escalation paths.

## MANDATORY EXECUTION RULES

- Use exports, configuration snapshots, or read-only console evidence.
- Highlight unknown ownership and stale privileges.
- Agent Autonomy Protocol: do not change privileges or test escalation.

## REQUIRED OUTPUT

Append a privilege graph summary, critical identities, standing access, emergency accounts, and owner gaps.

SUCCESS: High-risk privilege paths are visible.

FAILURE: Admin surfaces remain unmapped.

## NEXT STEP

Read `./steps-c/step-03-session-mfa-review.md`.
