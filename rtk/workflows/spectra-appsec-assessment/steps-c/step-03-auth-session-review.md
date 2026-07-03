# Step 03 - Authentication And Session Review

## STEP GOAL

Assess authentication, session handling, MFA, password reset, token lifetime, and account recovery controls.

## MANDATORY EXECUTION RULES

- Use only approved test accounts and synthetic data.
- Capture evidence with secrets redacted.
- Agent Autonomy Protocol: do not attempt credential stuffing, MFA fatigue, real-user takeover, or token theft.

## TOKEN / JWT INSPECTION (do it safely and correctly)

When inspecting a JWT or other token, the command MUST be self-contained and
correct on its own — never rely on a `|| fallback` to hide a broken snippet.

- Prefer a minimal, correct decode. For a JWT payload — note the explicit
  base64url padding so it works for **any** token length (not just ones that
  happen to be already padded):
  ```bash
  python3 -c "import sys,base64,json; p=sys.argv[1].split('.')[1]; p+='='*(-len(p)%4); print(json.dumps(json.loads(base64.urlsafe_b64decode(p)),indent=2))" "$JWT"
  ```
- If you generate an inline Python one-liner, it must have **no undefined
  variables and no dead branches** (e.g. never `... if False else True`, never
  reference a name that was not assigned in that same command). Read the snippet
  back before running it.
- Base decisions on the **decoded claims you actually parsed** (alg, exp, iat,
  aud, iss, sub), not on a raw dump that only printed because a fallback ran.
- Redact signature material and any real subject identifiers in evidence.

## REQUIRED OUTPUT

Append:

- auth flows reviewed
- session controls
- reset and recovery behavior
- token and cookie properties
- gaps, evidence, and risk notes

SUCCESS: Auth/session risks are supported by safe evidence.

FAILURE: Findings rely on unapproved accounts, secrets, or speculative claims.

## NEXT STEP

Read `./steps-c/step-04-authorization-business-logic.md`.
