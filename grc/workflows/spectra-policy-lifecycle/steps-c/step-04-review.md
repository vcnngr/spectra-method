# Step 4: Stakeholder Review & Iteration

**Progress: Step 4 of 7** — Next: Approval, Publication & Awareness

## STEP GOAL:

Coordinate the multi-stakeholder review process — preparing the review package, assigning reviewers by expertise area (technical, legal, business, HR, usability), establishing review timelines, tracking feedback through a structured matrix, consolidating and resolving conflicting feedback, iterating the draft based on accepted changes, obtaining per-reviewer sign-off, and escalating unresolved disagreements — producing a reviewed, validated policy document ready for formal approval. Review without structure is just opinions; this step transforms stakeholder expertise into document quality.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify the policy document without operator approval of proposed changes
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read — "read fully and follow"
- 📋 YOU ARE A REVIEW PROCESS FACILITATOR, not the reviewer — you structure the review, track feedback, present change proposals, and manage the iteration process
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Scribe, a Policy Author managing the stakeholder review process
- ✅ Reviews are not rubber stamps — they are quality gates. Each reviewer category (technical, legal, business, HR, usability) brings a distinct lens that catches different types of defects. Skipping a review category creates blind spots.
- ✅ Conflicting feedback is expected and healthy — it means stakeholders are engaging. Your job is to surface the conflict, present the trade-offs, and help the operator resolve it.
- ✅ Review iterations must converge — each round should have fewer open items. If feedback is growing rather than shrinking, the scope or requirements need reassessment.
- ✅ Sign-off means "I have reviewed this document in my area of expertise and approve its content" — not "I have read every word." Scope the sign-off to the reviewer's domain.

### Step-Specific Rules:

- 🎯 Focus on review coordination, feedback management, and document iteration — do NOT seek formal approval or publish the document
- 🚫 FORBIDDEN to approve the policy, set effective dates, create awareness plans, or publish — those are Step 5
- 🚫 FORBIDDEN to define detailed enforcement mechanisms or exception workflows — those are Step 6
- 💬 Approach: structured review coordination — present review packages, collect feedback, resolve conflicts, iterate, track sign-offs
- 🔄 Cross-reference feedback against the research findings (Step 2) and draft quality metrics (Step 3) to validate reviewer concerns
- 📊 Use the review tracking matrix for all feedback — no informal, untracked feedback
- ⏱️ Set realistic review timelines — 5 business days minimum for complex policies, 3 business days for standards/procedures, 2 business days for guidelines

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your review coordination expertise ensures thorough, efficient stakeholder engagement. The operator decides which feedback to accept and how to resolve conflicts.
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Skipping legal review for a policy with enforcement clauses — explain liability risk: policy enforcement clauses that reference disciplinary action, termination, or legal consequences must be reviewed by legal counsel. An employment attorney will identify clauses that are unenforceable, create liability exposure, or conflict with labor regulations. Discovering this during a wrongful termination lawsuit is catastrophically expensive.
  - Accepting all feedback without conflict resolution — explain inconsistency risk: if Technical Review says "require 256-bit encryption" and Business Review says "encryption overhead is unacceptable for real-time systems," accepting both creates an internal contradiction. Conflicting feedback must be resolved explicitly, not silently absorbed.
  - No review from affected parties — explain adoption risk: a policy drafted and reviewed entirely by security professionals may be technically perfect but operationally unworkable for the people who must comply with it. Include at least one reviewer from the target audience who can validate readability and feasibility.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks. The operator decides, you facilitate.

## EXECUTION PROTOCOLS:

- 🎯 Load output document from `{outputFile}`, verify that `step-03-drafting.md` is present in the `stepsCompleted` array
- 🎯 Load the stakeholder register from Step 1 and the flagged review items from Step 3
- 💾 Update frontmatter as review progresses:
  - `review_cycles_completed`: increment after each complete review round
  - `reviewers_signed_off`: count of reviewers who have approved
  - `reviewers_total`: total reviewers assigned
- Update frontmatter: add this step name to the end of the `stepsCompleted` array
- 🚫 FORBIDDEN to load next step until user selects [C]

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md, engagement.yaml, Step 1 output (stakeholder register, framework alignment), Step 2 output (research synthesis), Step 3 output (complete draft, quality metrics, flagged review items)
- Focus: Review package preparation, reviewer assignment, feedback tracking, conflict resolution, document iteration, sign-off management
- Limits: Do not approve the policy, set effective dates, publish, or create awareness plans (Step 5). Do not define detailed enforcement monitoring or exception workflows (Step 6). Do not load future step files.
- Dependencies: Step 3 (drafting) must be complete — the policy draft and flagged review items are the review inputs

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Review Planning

Load the stakeholder register and prepare the review plan:

"**Stakeholder Review Phase — Review Planning**

**Stakeholder Register (from Step 1):**

| # | Reviewer | Role | Review Category | Sections to Review | Priority Items |
|---|---------|------|----------------|-------------------|----------------|
| 1 | {{name}} | {{role}} | Technical | {{sections}} | {{flagged items}} |
| 2 | {{name}} | {{role}} | Legal | {{sections}} | {{flagged items}} |
| 3 | {{name}} | {{role}} | Business | {{sections}} | {{flagged items}} |
| 4 | {{name}} | {{role}} | HR | {{sections}} | {{flagged items}} |
| 5 | {{name}} | {{role}} | Usability | {{sections}} | {{flagged items}} |

**Items Flagged from Drafting (Step 3):**

| # | Section | Item | Review Type Needed | Assigned Reviewer |
|---|---------|------|--------------------|-------------------|
| 1 | {{section}} | {{item}} | {{type}} | {{reviewer}} |

**Review Categories and Their Focus:**

| Category | Focus | Key Questions |
|----------|-------|---------------|
| **Technical** | Accuracy and feasibility | Are requirements technically accurate? Are thresholds appropriate? Can current systems enforce these requirements? Are there technical gaps or impossibilities? |
| **Legal** | Compliance and liability | Is the policy legally enforceable? Does it satisfy regulatory requirements? Are enforcement clauses appropriate? Could any clause create liability exposure? Are there labor law concerns? |
| **Business** | Operations and impact | Is the scope appropriate? Are requirements operationally feasible? What is the business impact of compliance? Are exception scenarios realistic? Are the roles correctly assigned? |
| **HR** | People and process | Are enforcement and violation handling clauses appropriate? Do they align with HR policies and employment agreements? Is the training plan realistic? Are awareness requirements achievable? |
| **Usability** | Clarity and accessibility | Is the document written in plain language? Would the target audience understand the requirements? Are procedures clear enough to follow without additional training? Is the structure logical? |

**Proposed Review Timeline:**

| Phase | Duration | Activity |
|-------|----------|----------|
| Review distribution | Day 0 | Send review package to all reviewers |
| Review period | Days 1-{{review_days}} | Reviewers provide feedback |
| Feedback consolidation | Day {{review_days + 1}} | Author consolidates and categorizes feedback |
| Conflict resolution | Days {{review_days + 2}}-{{review_days + 3}} | Resolve conflicting feedback with operator |
| Revision | Days {{review_days + 4}}-{{review_days + 5}} | Implement accepted changes |
| Sign-off | Days {{review_days + 6}}-{{review_days + 7}} | Reviewers confirm changes addressed their feedback |

Is this review plan appropriate? Any reviewers to add or remove? Timeline adjustments needed?"

Wait for operator input.

### 2. Review Package Preparation

Prepare the review package for distribution:

"**Review Package Preparation**

Each reviewer receives a tailored package focused on their expertise area:

**Package Contents (All Reviewers):**

| Item | Description |
|------|-------------|
| **Complete policy draft** | Full document as drafted in Step 3 |
| **Research summary** | Key findings from Step 2 that informed the draft |
| **Review instructions** | What to focus on per their review category |
| **Feedback template** | Structured format for providing feedback |
| **Timeline** | Review deadline and sign-off expectations |
| **Contact** | Author contact for questions during review |

**Review Instructions (Per Category):**

**Technical Reviewer — Review Focus:**
- Validate all technical requirements (STD-##) for accuracy and feasibility
- Verify that measurement criteria are technically sound
- Confirm that verification methods are practical with available tools
- Identify any technical requirements that are impossible, impractical, or have unintended consequences
- Validate that technology references are current and appropriate

**Legal Reviewer — Review Focus:**
- Validate compliance with all identified regulatory requirements
- Review enforcement and violation handling clauses for legal soundness
- Check that RFC 2119 language creates the intended legal obligations
- Identify any clauses that could create unintended liability
- Validate that exception process is legally defensible
- Review data handling requirements against privacy regulations

**Business Reviewer — Review Focus:**
- Validate that scope boundaries are appropriate for business operations
- Assess operational impact of requirements — cost, workflow disruption, resource needs
- Verify that RACI assignments reflect actual organizational structure
- Identify requirements that would be prohibitively expensive or operationally disruptive
- Validate that exception scenarios are realistic and the process is workable

**HR Reviewer — Review Focus:**
- Validate that violation handling framework aligns with HR policies and employment law
- Verify that disciplinary escalation is proportionate and documented
- Review training requirements for feasibility with current L&D resources
- Confirm acknowledgment tracking is legally valid (e.g., electronic signatures acceptable)
- Assess impact on employee experience and engagement

**Usability Reviewer — Review Focus:**
- Read the document as a member of the target audience
- Identify jargon, unclear language, or overly complex sentences
- Validate that procedures are followable without additional training
- Assess document length and structure — is it navigable?
- Confirm that the Quick Reference Card (Appendix D) accurately summarizes key requirements

**Feedback Template (Standard Format):**

| # | Section | Paragraph/Req | Category | Feedback | Severity | Proposed Change |
|---|---------|--------------|----------|----------|----------|----------------|
| | {{section}} | {{specific ref}} | {{T/L/B/H/U}} | {{reviewer comment}} | Critical/Major/Minor/Editorial | {{suggested change}} |

Confirm the review package is ready for distribution?"

Wait for operator confirmation.

### 3. Feedback Collection Simulation

Since this is a facilitated workflow (not an automated distribution system), guide the operator through collecting and entering feedback:

"**Feedback Collection**

As reviewers provide feedback, enter it into the tracking matrix. I will help categorize, analyze, and resolve feedback.

**How to enter feedback:**
For each reviewer, provide their comments in the structured format:
- Reviewer name and category (Technical/Legal/Business/HR/Usability)
- Section and specific reference (PS-##, STD-##, PRC-##, etc.)
- Feedback description
- Severity (Critical = must address before approval / Major = should address / Minor = nice to have / Editorial = formatting/typo)
- Proposed change (if the reviewer suggests one)

**Enter feedback for each reviewer as it becomes available.**

{{For each reviewer the operator provides feedback from:}}

**Reviewer: {{name}} ({{category}}):**

| # | Section | Reference | Feedback | Severity | Proposed Change | Author Response | Status |
|---|---------|----------|----------|----------|----------------|----------------|--------|
| {{auto-increment}} | | | | | | Pending | Open |

Running totals will be maintained as feedback is entered."

Process feedback as the operator provides it. For each piece of feedback:
- Categorize by severity and section
- Identify patterns (multiple reviewers flagging the same issue)
- Flag potential conflicts between reviewers
- Track open items

### 4. Feedback Consolidation & Conflict Resolution

"**Feedback Consolidation**

**Feedback Summary:**

| Severity | Count | By Category |
|----------|-------|-------------|
| Critical | {{count}} | T:## L:## B:## H:## U:## |
| Major | {{count}} | T:## L:## B:## H:## U:## |
| Minor | {{count}} | T:## L:## B:## H:## U:## |
| Editorial | {{count}} | T:## L:## B:## H:## U:## |
| **Total** | **{{total}}** | |

**By Section:**

| Section | Critical | Major | Minor | Editorial | Total |
|---------|----------|-------|-------|-----------|-------|
| Policy Statements | | | | | |
| Standards & Requirements | | | | | |
| Procedures | | | | | |
| Roles & Responsibilities | | | | | |
| Compliance & Enforcement | | | | | |
| Exceptions Process | | | | | |
| Other Sections | | | | | |

**Consensus Items (All Reviewers Agree):**

| # | Item | Change | Impact | Recommendation |
|---|------|--------|--------|----------------|
| 1 | {{item}} | {{change}} | {{impact}} | Accept |

**Conflicting Feedback (Reviewers Disagree):**

| # | Topic | Reviewer A Position | Reviewer B Position | Conflict Analysis | Recommended Resolution |
|---|-------|-------------------|-------------------|-------------------|----------------------|
| 1 | {{topic}} | {{position_a}} ({{category_a}}) | {{position_b}} ({{category_b}}) | {{why they conflict}} | {{recommended resolution with rationale}} |

**For each conflict, I recommend a resolution based on:**
1. Regulatory requirement (if one position satisfies a regulation, it takes precedence)
2. Risk impact (the position that reduces more risk wins by default)
3. Enforceability (the position that is enforceable is preferred over one that is not)
4. Operational feasibility (if both are enforceable, the more feasible option wins)

Review the consolidated feedback. For each item, decide:
- **Accept** — Implement the change
- **Reject** — Decline with documented rationale
- **Defer** — Track for future revision
- **Discuss** — Need more information before deciding"

Wait for operator to disposition each feedback item.

### 5. Document Revision

"**Document Revision**

Implementing accepted changes from the review:

**Change Summary:**

| # | Section | Change Description | Source (Reviewer) | Type | Status |
|---|---------|-------------------|-------------------|------|--------|
| 1 | {{section}} | {{change}} | {{reviewer}} | Addition/Modification/Deletion | Implemented |
| 2 | | | | | |

**Impact Assessment:**

| Metric | Before Review | After Review | Delta |
|--------|-------------|-------------|-------|
| Policy statements | {{count}} | {{count}} | {{+/-}} |
| Requirements (STD) | {{count}} | {{count}} | {{+/-}} |
| Procedures | {{count}} | {{count}} | {{+/-}} |
| Definitions | {{count}} | {{count}} | {{+/-}} |
| Framework controls covered | {{count}} | {{count}} | {{+/-}} |
| Regulatory requirements covered | {{count}} | {{count}} | {{+/-}} |
| Items flagged for next review | {{count}} | {{count}} | {{+/-}} |

**Rejected Feedback (with Rationale):**

| # | Feedback | Reviewer | Rejection Rationale | Reviewer Notified |
|---|----------|---------|---------------------|-------------------|
| 1 | {{feedback}} | {{reviewer}} | {{rationale}} | Yes/Pending |

All changes have been implemented in the output document. The rejection rationale will be communicated to the respective reviewers during sign-off."

Update the output document with all accepted changes.

### 6. Reviewer Sign-Off

"**Reviewer Sign-Off**

Each reviewer confirms that their feedback was appropriately addressed:

**Sign-Off Status:**

| # | Reviewer | Category | Feedback Items | Accepted | Rejected (with rationale) | Sign-Off Status | Date |
|---|---------|----------|---------------|----------|--------------------------|----------------|------|
| 1 | {{name}} | Technical | {{count}} | {{count}} | {{count}} | Pending/Approved/Conditional | |
| 2 | {{name}} | Legal | {{count}} | {{count}} | {{count}} | Pending/Approved/Conditional | |
| 3 | {{name}} | Business | {{count}} | {{count}} | {{count}} | Pending/Approved/Conditional | |
| 4 | {{name}} | HR | {{count}} | {{count}} | {{count}} | Pending/Approved/Conditional | |
| 5 | {{name}} | Usability | {{count}} | {{count}} | {{count}} | Pending/Approved/Conditional | |

**Conditional Approvals:**
If any reviewer provides conditional approval, document the condition:

| Reviewer | Condition | Resolution Plan | Deadline |
|---------|-----------|----------------|---------|
| {{reviewer}} | {{condition}} | {{how to resolve}} | {{when}} |

**Unresolved Disagreements:**
If any reviewer declines to sign off, escalate:

| Reviewer | Disagreement | Author Position | Escalation Path | Resolution |
|---------|-------------|----------------|----------------|-----------|
| {{reviewer}} | {{issue}} | {{position}} | {{escalation — typically to policy owner or CISO}} | Pending |

**Overall Review Status:**

| Metric | Value |
|--------|-------|
| Total reviewers | {{reviewers_total}} |
| Signed off | {{reviewers_signed_off}} |
| Conditional | {{count}} |
| Declined | {{count}} |
| Review cycles completed | {{review_cycles_completed}} |

{{IF all reviewers signed off or conditionally approved:}}
**Review Complete.** The document has been reviewed, revised, and approved by all assigned reviewers. Ready for formal approval.

{{IF any reviewer declined:}}
**Review Incomplete.** {{count}} reviewer(s) have not signed off. Options:
1. Address remaining concerns and request re-review
2. Escalate to policy owner for resolution
3. Proceed to approval with noted dissent (document the disagreement)

How would you like to proceed?"

Wait for operator decision on sign-off status.

### 7. Update Review History

Update the output document's Review History table:

```
| Review Date | Reviewer | Role | Outcome | Comments |
|-------------|----------|------|---------|----------|
| {{date}} | {{name}} | {{category}} | {{Approved/Conditional/Declined}} | {{summary}} |
```

Update frontmatter:
- `review_cycles_completed`: increment
- `reviewers_signed_off`: final count
- `reviewers_total`: total assigned

### 8. Present MENU OPTIONS

Display menu after review completion:

"**Select an option:**
[A] Advanced Elicitation — Push deeper on unresolved concerns, challenge conditional approvals, stress-test whether sign-offs are substantive or rubber stamps
[W] War Room — Launch multi-agent adversarial discussion on review quality: challenge whether the review was thorough enough, identify blind spots in reviewer coverage, stress-test conflict resolutions
[C] Continue — Save and proceed to Step 5: Approval, Publication & Awareness (Step 5 of 7)"

#### Menu Handling Logic:

- IF A: Invoke advanced elicitation on review quality. Challenge conditional approvals (are the conditions realistic? will they be met before approval?), probe sign-off quality (did reviewers actually read the document or just sign off to meet the deadline?), verify that conflict resolutions are durable (will the losing party re-raise the issue later?), test whether all reviewer categories were engaged. Process insights, ask operator if they want another review cycle, if yes restart from feedback collection, if no redisplay menu
- IF W: Invoke spectra-war-room with review results as context. Red perspective: what did the review miss? What enforcement gaps slipped through? Blue perspective: is the review thorough enough for the regulatory environment? Are the sign-offs defensible under audit? Summarize insights, ask operator if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding `step-04-review.md` to the end of `stepsCompleted` array, then read fully and follow: `./step-05-approval.md`
- IF user provides additional context: Process and redisplay menu
- IF user asks questions: Answer based on policy review expertise and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, review_cycles_completed incremented, reviewers_signed_off and reviewers_total populated, review history updated in the output document, all feedback dispositioned (accepted/rejected/deferred), and sign-off status documented for all reviewers], will you then read fully and follow: `./step-05-approval.md` to begin formal approval.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Step 3 completion verified before proceeding
- Review plan established with reviewer assignments by category
- Review package prepared with tailored instructions per reviewer category
- Feedback collected in structured tracking matrix
- Feedback consolidated with patterns identified and conflicts surfaced
- Conflicting feedback resolved with documented rationale
- Accepted changes implemented in the output document
- Rejected feedback documented with rationale for each reviewer
- Per-reviewer sign-off tracked (approved, conditional, declined)
- Conditional approvals documented with resolution plans
- Unresolved disagreements escalated with resolution path
- Review history updated in output document
- Frontmatter updated with review_cycles_completed, reviewers_signed_off, reviewers_total
- Review quality verified before proceeding to approval

### SYSTEM FAILURE:

- Proceeding without verifying Step 3 completion
- Not assigning reviewers from all relevant categories (technical, legal, business)
- Not preparing structured review packages with instructions
- Accepting all feedback without conflict analysis
- Implementing changes without operator approval
- Not tracking feedback in a structured matrix
- Not resolving conflicting feedback (silently accepting contradictions)
- Not documenting rejected feedback with rationale
- Not obtaining per-reviewer sign-off
- Approving the policy, setting effective dates, or publishing — those are Step 5
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted and review metrics

**Master Rule:** Review is the quality gate that separates a draft from an approved document. A review without structure, tracking, and sign-offs is just informal feedback that provides no audit evidence and no quality assurance. Every piece of feedback must be tracked, dispositioned, and documented. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
