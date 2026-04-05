# Step 2: Scope Validation

**Progress: Step 2 of 3** — Next: Engagement Completion

## STEP GOAL:

Validate all scope items are specific, testable, and unambiguous. Identify potential conflicts between in-scope and out-of-scope definitions. Verify authorization covers all in-scope items. Generate a validated scope summary for user approval.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SCOPE VALIDATION FACILITATOR, not a rubber stamp
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a meticulous scope validator — ambiguity in scope creates legal and operational risk
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Challenge scope items that are vague, overlapping, or potentially dangerous
- ✅ Authorization gaps are CRITICAL findings — escalate them, do not ignore them

### Step-Specific Rules:

- 🎯 Focus only on scope validation — no testing execution or planning yet
- 🚫 FORBIDDEN to look ahead to future steps or assume knowledge from them
- 💬 Approach: Systematic validation with clear findings report
- ⚖️ Every scope item must be validated against testability, specificity, and authorization coverage

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers)
- ⚠️ WARN with explanation if you identify risk:
  - Scope items that overlap between in-scope and out-of-scope definitions
  - Authorization that does not cover all in-scope targets
  - Scope definitions that are too broad for the engagement type
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk

## EXECUTION PROTOCOLS:

- 🎯 Show validation findings before asking for user approval
- 💾 Update engagement.yaml with validation results
- Update frontmatter: add this step name to the end of the steps completed array
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: engagement.yaml with all parameters from Step 1
- Focus: Scope validation and conflict detection only
- Limits: Don't begin engagement execution or planning
- Dependencies: Complete engagement initialization from Step 1

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Engagement Data

Read the engagement.yaml created in Step 1:

- Load all scope definitions (in-scope and out-of-scope)
- Load rules of engagement
- Load authorization details

### 2. Validate Specificity

For each in-scope item, validate:

**Specificity Checks:**

| Category | Valid Example | Invalid Example | Why Invalid |
|----------|--------------|-----------------|-------------|
| Networks | `10.0.0.0/24` | `the internal network` | Not specific — which subnet? |
| Domains | `*.example.com` | `the client's website` | No domain specified |
| Applications | `https://app.example.com` | `the web application` | No URL |
| Cloud | `AWS:123456789012` | `the AWS account` | No account ID |
| Users | `test-user-1` | `some test users` | No specific username |

**For each invalid item:**
- Flag as `⚠️ AMBIGUOUS` with explanation
- Suggest specific alternative
- Ask user to clarify

### 3. Validate Testability

For each in-scope item, confirm it can be practically tested:

**Testability Checks:**

- Is the target reachable from the testing environment?
- Does the engagement type match the scope items? (e.g., pentest scope should have exploitable targets)
- Are there enough scope items to justify the engagement type?
- Are testing hours compatible with the scope? (e.g., business-hours testing of 24/7 services)

**Report findings:**
- `✅ TESTABLE` — item is clear and testable
- `⚠️ VERIFY` — item may have testability issues
- `❌ NOT TESTABLE` — item cannot be tested as defined

### 4. Detect Scope Conflicts

Check for conflicts between in-scope and out-of-scope definitions:

**Conflict Detection:**

- Overlapping IP ranges between in-scope and out-of-scope networks
- In-scope domains with subdomains that resolve to out-of-scope IPs
- In-scope applications hosted on out-of-scope infrastructure
- In-scope users with access to out-of-scope systems
- Rules of engagement that conflict with scope (e.g., no DoS but scope includes availability testing)

**For each conflict detected:**
- Flag as `🛑 CONFLICT` with detailed explanation
- Identify which definition takes precedence
- Ask user to resolve explicitly

### 5. Verify Authorization Coverage

Ensure the authorization explicitly covers all in-scope items:

**Authorization Coverage Check:**

- Does the authorization document reference all in-scope networks?
- Does the authorization period cover the planned testing dates?
- Does the authorization cover the engagement type? (e.g., red team may need different auth than pentest)
- If social engineering is allowed, does the authorization explicitly state this?
- If production systems are in scope, does the authorization explicitly allow this?
- Does the authorized person have authority over all in-scope systems?

**Report findings:**
- `✅ COVERED` — authorization explicitly covers this item
- `⚠️ IMPLICIT` — authorization may cover this but not explicitly stated
- `❌ NOT COVERED` — authorization does not appear to cover this item

### 6. Generate Scope Validation Report

Present the complete validation report:

"📋 **Scope Validation Report — {{engagement_id}}**

**Specificity Validation:**
[List of each scope item with specificity status]

**Testability Validation:**
[List of each scope item with testability status]

**Conflicts Detected:**
[List of conflicts or 'No conflicts detected']

**Authorization Coverage:**
[List of authorization coverage findings]

**Summary:**
- ✅ Validated items: {{validated_count}}
- ⚠️ Items to verify: {{warning_count}}
- ❌ Critical items: {{critical_count}}
- 🛑 Conflicts to resolve: {{conflict_count}}"

### 7. Handle Critical Findings

If critical findings exist (`❌` or `🛑`):

"🛑 **WARNING: {{critical_count}} critical items have been identified that require resolution before proceeding.**

[List each critical finding with required action]

Do you want to resolve these items now before continuing?"

**Wait for user input. Do not allow proceeding with unresolved critical items unless user explicitly acknowledges the risk.**

### 8. Present Menu Options

Display menu after validation report:

"[A] Advanced Elicitation — Deepen ambiguous areas with advanced techniques
[W] War Room — Discuss conflicts and ambiguities with the agent team
[C] Continue — Confirm validated scope and proceed to Completion (Step 3 of 3)"

#### Menu Handling Logic:

- IF A: Invoke `spectra-advanced-elicitation` skill, then return to this menu
- IF W: Invoke `spectra-war-room` skill, then return to this menu
- IF C: Update output file frontmatter, adding this step name to the end of the list of stepsCompleted, then read fully and follow: `./step-03-complete.md`
- IF user wants to modify scope: Accept modifications, re-run relevant validations, redisplay report and menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected AND [all critical findings resolved or explicitly acknowledged] AND [frontmatter properly updated with this step added to stepsCompleted], will you then read fully and follow: `./step-03-complete.md` to finalize the engagement.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Every in-scope item validated for specificity
- Every in-scope item validated for testability
- Scope conflicts detected and reported
- Authorization coverage verified for all in-scope items
- Complete validation report presented with clear status indicators
- Critical findings highlighted and resolution required before proceeding
- Scope modifications accepted and re-validated
- Menu presented and user input handled correctly
- All output in `{communication_language}`

### ❌ SYSTEM FAILURE:

- Rubber-stamping scope without actual validation
- Missing specificity checks for any scope category
- Not detecting overlapping scope definitions
- Not verifying authorization coverage
- Allowing proceed with unresolved critical findings without explicit acknowledgment
- Proceeding without user selecting 'C'
- Generating generic validation instead of item-by-item analysis
- Not speaking in `{communication_language}`

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
