# Step 06 - Risk And Remediation

## STEP GOAL

Convert observations into prioritized findings with severity, likelihood, business impact, and remediation.

## MANDATORY EXECUTION RULES

- Calibrate severity with exploitability, reachability, privileges, data sensitivity, and compensating controls.
- Separate confirmed findings from hypotheses.
- Agent Autonomy Protocol: do not overstate impact beyond evidence.

## FINDING INTEGRITY (proven vs hypothesized — enforced, not optional)

Over-claiming distorts risk and destroys report credibility. Every finding MUST make the proven/hypothesized boundary **structural**, not a matter of prose:

- **Mandatory "Proven / Not established" split.** Each finding carries two explicit sections:
  - **WHAT WAS PROVEN (only this):** the exact observed evidence (request → response, status code, artifact). Nothing else.
  - **NOT ESTABLISHED / NOT TESTED:** every capability that was hypothesized but not demonstrated (e.g. SSTI, deserialization, RCE), stated plainly as not observed or not attempted.
- **Severity is assigned to what is DEMONSTRATED**, never to the worst-case potential of a hypothesized sink. Malformed JSON accepted with HTTP 200 (a schema/contract gap) is **Low** until injection is actually shown.
- **OWASP/class must match the evidence.** A contract/validation gap is **A08**, not **A03 (Injection)**, until injection is demonstrated. Do not label a field a "template/deserialization/eval sink" without evidence that it is one.
- **Language guard.** Never write "exploit chain withheld", "deliberately not exploited", or "capability held back" unless a working (even if unexecuted) PoC is attached that demonstrates the exploit is *available*. Restraint language is only for exploits you have shown to exist. Absent a PoC, the correct phrasing is "not tested / unverified" — restraint means not *running* a demonstrated exploit, never implying one exists when it was never shown.

## REQUIRED OUTPUT

Append a findings table with:

- ID
- title
- **WHAT WAS PROVEN (only this)** — observed evidence
- **NOT ESTABLISHED / NOT TESTED** — hypothesized-but-undemonstrated capabilities
- affected asset
- OWASP class (matched to the proven evidence)
- severity (anchored to what is proven)
- severity rationale (why this severity follows from the proven evidence)
- owner
- fix recommendation
- retest method

SUCCESS: Each finding is fixable and evidence-backed; proven and hypothesized are structurally separated; severity and OWASP class follow the proven evidence; no exploit is claimed or "withheld" without an attached PoC.

FAILURE: Findings lack owner, evidence, or retest criteria; severity or class reflects a hypothesized (undemonstrated) capability; "withheld exploit"/restraint language used without a PoC; proven and hypothesized blurred into one claim.

## NEXT STEP

Read `./steps-c/step-07-handoff.md`.
