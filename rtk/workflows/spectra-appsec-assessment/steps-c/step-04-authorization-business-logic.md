# Step 04 - Authorization And Business Logic

## STEP GOAL

Evaluate object-level authorization, function-level authorization, tenant isolation, workflow integrity, and abuse cases.

## MANDATORY EXECUTION RULES

- Prefer role matrix review and controlled request comparison.
- Minimize data access; prove impact with metadata or synthetic records.
- Agent Autonomy Protocol: block mass enumeration, privilege escalation on real users, payment abuse, or irreversible workflow actions.
- **Token rule:** hold session tokens in process/shell variables re-acquired from a live login. NEVER read a token from a file you have marked for sanitization; a token `cat` from a shredded file yields an empty `Authorization: Bearer` header and turns every response into a misleading 401 (systematic false negative).
- **Target artifact rule:** every account, record, or item you create on the target is a residual until disposed of. Log it the moment you create it (see the Target Artifact Ledger below). A synthetic **privileged** artifact (e.g. an admin account from a mass-assignment/self-elevation test) must be flagged and prioritized for removal — never left to outlive the step.

## REQUIRED OUTPUT

Append:

- role-to-action matrix
- authorization test cases
- business rules tested (abuse cases: e.g. negative quantity, coupon/discount abuse, deprecated API paths)
- tenant/data isolation observations
- evidence and impact notes
- **Target Artifact Ledger** — every artifact created on the target with its disposition

## STEP CLOSE PROTOCOL (do not skip; order matters)

Closing this step is gated. Run these in order and only then mark it complete.

### 1. REQUIRED-OUTPUT self-audit (gate for completion)

Before writing `completed` to `stepsCompleted`, emit an explicit audit mapping **each** REQUIRED OUTPUT to the section that satisfies it:

| Required output | Produced? | Where |
|---|---|---|
| role-to-action matrix | yes/no | … |
| authorization test cases | yes/no | … |
| business rules tested (abuse cases) | yes/no | … |
| tenant/data isolation observations | yes/no | … |
| evidence and impact notes | yes/no | … |
| Target Artifact Ledger | yes/no | … |

- If any row is **no**, the step is **partial** — do NOT mark it `completed`. Execute the missing block (the business-logic/abuse-cases block is frequently the omitted one and often yields a real finding) or, if intentionally skipped, record it and ask the operator to confirm before closing.

### 2. Target Artifact Ledger disposition

List every artifact created on the target and set a final disposition:

| Artifact | Type | Privileged? | Disposition |
|---|---|---|---|
| e.g. user `qa+1@…` | synthetic account | no | removed |
| e.g. user `qa+admin@…` | synthetic account | **YES** | removed / **flag if residual** |

- Every **privileged** artifact must be removed (or explicitly, loudly flagged as a residual for teardown with operator sign-off). A synthetic admin account must never silently outlive the step.

### 3. Evidence consolidation, THEN sanitization (never the reverse)

1. Consolidate the redacted evidence into the assessment output first.
2. Verify the evidence files contain no secrets (e.g. `grep` for JWTs / password material) — tokens tied to a password-hash finding must be scrubbed.
3. **Only then** sanitize raw working material. Do NOT silence errors on destruction — run e.g. `shred -uv "$WD"/.tok* "$WD"/resp.json` **without** `2>/dev/null` so each file's outcome is visible and verifiable. Never shred a file whose output has not yet been consolidated. Sanitization applies ONLY to the agent's own local working files; never delete or alter target logs, audit trails, defender telemetry, or evidence of compromise.

SUCCESS: All REQUIRED OUTPUT present (self-audit clean), the artifact ledger has a disposition for every target artifact with no residual privileged account, and sanitization ran after evidence consolidation with visible outcomes.

FAILURE: Marking the step complete with missing REQUIRED OUTPUT; leaving a synthetic privileged artifact undocumented/active; shredding before evidence is consolidated; silencing cleanup errors; or reading tokens from files marked for destruction. Testing that changes real business state without approval is also FAILURE.

## NEXT STEP

Read `./steps-c/step-05-input-api-risk.md`.
