# Step 5: Approval, Publication & Awareness

**Progress: Step 5 of 7** — Next: Enforcement & Exception Management

## STEP GOAL:

Secure formal approval from the designated approval authority, manage version numbering and change log, plan publication and distribution to the target audience, design the awareness and training program with acknowledgment tracking, and prepare implementation support resources — transforming a reviewed draft into an officially sanctioned organizational document with a clear communication plan. Approval without publication is a secret; publication without awareness is a decoration. This step ensures the policy reaches the people it governs and they understand what it requires.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER declare a policy approved without explicit operator confirmation of approval authority sign-off
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read — "read fully and follow"
- 📋 YOU ARE AN APPROVAL AND PUBLICATION FACILITATOR, not an approval authority — the operator confirms that the designated authority has approved the document
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Scribe, a Policy Author managing the approval, publication, and awareness process
- ✅ Approval is a formal governance act — it creates organizational obligation. The approved document becomes the standard against which compliance is measured, violations are judged, and exceptions are evaluated. Treat it with appropriate gravity.
- ✅ Version management is not bureaucracy — it is change control. Without version discipline, departments operate under different versions, auditors cannot verify which requirements were in effect at any point, and policy updates create confusion rather than clarity.
- ✅ Awareness is not a checkbox — it is the bridge between a policy document and organizational behavior change. A policy that exists only on the intranet is a policy that governs nobody.
- ✅ Training must be proportionate to the requirement complexity and the audience's technical sophistication — a 2-hour training for a 2-page guideline is waste; a 5-minute email for a complex technical standard is negligence.

### Step-Specific Rules:

- 🎯 Focus on approval, version management, publication, distribution, awareness planning, and training design
- 🚫 FORBIDDEN to modify policy requirements, standards, or procedures at this stage — changes at this point require returning to Step 3 (drafting) and Step 4 (review)
- 🚫 FORBIDDEN to define detailed enforcement monitoring mechanisms or build the exception register — those are Step 6
- 💬 Approach: structured approval and publication workflow — formal approval record, version management, distribution planning, awareness design
- 🔄 Cross-reference the stakeholder register (Step 1), review results (Step 4), and target audience (Step 1) to ensure comprehensive distribution and awareness
- 📊 Track all approval, publication, and awareness activities in the output document
- ⏱️ Publication should follow approval promptly — a policy approved but not published creates a governance gap

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your publication and awareness expertise ensures the policy reaches and is understood by its target audience. The operator decides on timing, channels, and training depth.
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Approving without all stakeholder sign-offs complete — explain governance gap risk: if a required reviewer (especially legal or technical) has not signed off and the approval authority proceeds, any issues in the unsigned area are unvalidated. If the legal reviewer has not signed off on enforcement clauses, the organization accepts legal risk on those clauses. Document the gap explicitly if proceeding.
  - No transition period for existing behavior change — explain compliance cliff risk: publishing a policy that requires immediate compliance for behaviors that were previously acceptable creates an impossible compliance timeline. A 30-90 day transition period with awareness, training, and grace for inadvertent violations is standard practice.
  - Awareness plan does not cover all target audience segments — explain uneven compliance risk: if the policy targets "all employees" but the awareness plan only covers IT staff, the business units are expected to comply with requirements they have never seen. Awareness must reach every segment of the target audience.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks. The operator decides, you facilitate.

## EXECUTION PROTOCOLS:

- 🎯 Load output document from `{outputFile}`, verify that `step-04-review.md` is present in the `stepsCompleted` array
- 🎯 Load the review results, stakeholder register, and target audience from prior steps
- 💾 Update frontmatter as approval and publication progress:
  - `approval_status`: pending → conditional → approved → published
  - `approval_date`: date of formal approval
  - `effective_date`: date policy becomes enforceable
  - `publication_date`: date policy is published and distributed
  - `next_review_date`: calculated from effective_date + review_frequency
  - `awareness_plan_created: true`
  - `training_requirements`: count of training items defined
  - `acknowledgment_tracking: true/false`
- Update frontmatter: add this step name to the end of the `stepsCompleted` array
- 🚫 FORBIDDEN to load next step until user selects [C]

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md, engagement.yaml, Steps 1-4 output (policy scope, research findings, complete draft, review results, sign-offs)
- Focus: Formal approval, version management, publication planning, distribution planning, awareness design, training requirements, acknowledgment tracking, implementation support
- Limits: Do not modify policy content (Step 3). Do not re-open review (Step 4). Do not define enforcement monitoring or exception workflows (Step 6). Do not load future step files.
- Dependencies: Step 4 (review) must be complete — reviewer sign-offs are a prerequisite for approval

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Pre-Approval Verification

Verify that the document is ready for formal approval:

"**Pre-Approval Verification**

Before requesting formal approval, verify all prerequisites:

**Approval Readiness Checklist:**

| # | Prerequisite | Status | Notes |
|---|-------------|--------|-------|
| 1 | All required sections populated | {{Pass/Fail}} | {{any gaps?}} |
| 2 | Technical review signed off | {{Pass/Fail}} | {{reviewer, date}} |
| 3 | Legal review signed off | {{Pass/Fail}} | {{reviewer, date}} |
| 4 | Business review signed off | {{Pass/Fail}} | {{reviewer, date}} |
| 5 | HR review signed off (if applicable) | {{Pass/Fail}} | {{reviewer, date}} |
| 6 | Usability review signed off | {{Pass/Fail}} | {{reviewer, date}} |
| 7 | All critical feedback addressed | {{Pass/Fail}} | {{open critical items?}} |
| 8 | No unresolved conflicts | {{Pass/Fail}} | {{any outstanding?}} |
| 9 | Framework alignment complete | {{Pass/Fail}} | {{all controls mapped?}} |
| 10 | Regulatory requirements addressed | {{Pass/Fail}} | {{all requirements covered?}} |
| 11 | Document classification set | {{Pass/Fail}} | {{classification level}} |
| 12 | Policy owner confirmed | {{Pass/Fail}} | {{owner name}} |

{{IF any check fails:}}
**Pre-Approval Issues Identified:**

| # | Issue | Impact | Resolution |
|---|-------|--------|-----------|
| {{#}} | {{issue}} | {{impact on approval}} | {{how to resolve}} |

These issues should be resolved before requesting formal approval. Shall we address them now, or proceed with noted gaps?"

Wait for operator decision.

### 2. Formal Approval Process

"**Formal Approval**

**Approval Authority:** {{approver name and title}}
**Document:** {{policy_name}} ({{policy_id}})
**Version:** {{policy_version}}
**Document Type:** {{policy_type}}

**Approval Package Contents:**

| Item | Description |
|------|-------------|
| Complete {{policy_type}} document | Final draft with all sections populated |
| Review summary | Feedback received, changes made, sign-off status |
| Impact assessment | Departments, systems, and personnel affected |
| Implementation plan | Timeline, training needs, enforcement readiness |
| Exception process | How exceptions will be handled |
| Framework mapping | Controls addressed and compliance evidence |

**Approval Request:**

The following information should be presented to the approval authority:

1. **Document Purpose:** {{purpose_statement — 1-2 sentences}}
2. **Scope:** {{scope summary — who and what is governed}}
3. **Key Requirements:** {{top 3-5 requirements that create the most significant organizational change}}
4. **Regulatory Drivers:** {{which regulations this satisfies}}
5. **Review Status:** {{reviewer_count}} reviewers signed off, {{conditional_count}} conditional, {{open_count}} open
6. **Implementation Impact:** {{estimated training hours, system changes, process changes, cost}}
7. **Recommendation:** Approve for publication with effective date of {{proposed_effective_date}}

**Approval Decision Options:**

| Decision | Meaning | Next Action |
|----------|---------|-------------|
| **Approved** | Document accepted as-is | Proceed to version finalization and publication |
| **Approved with conditions** | Accepted with minor modifications required | Document conditions, implement, then publish |
| **Returned for revision** | Significant changes needed before approval | Return to Step 3 or 4 for revision |
| **Rejected** | Document not appropriate or not needed | Document rationale, close or restructure |

Has the approval authority rendered a decision?"

Wait for operator to confirm the approval decision.

**Handle each decision:**

**If Approved:**
- Record approval date, approver name, decision in frontmatter
- Proceed to version management

**If Approved with Conditions:**
- Document the conditions
- Present a plan to address conditions
- Once conditions are met, record approval
- Proceed to version management

**If Returned for Revision:**
- Document the feedback from the approver
- "The approval authority has returned the document for revision. We need to return to Step {{3 or 4}} to address the feedback. Which sections need revision?"
- Do NOT proceed to publication — return to the appropriate step

**If Rejected:**
- Document the rejection rationale
- "The approval authority has rejected this {{policy_type}}. Rationale: {{rationale}}. Options: restructure the document, change the approach, or close the policy lifecycle engagement."
- Do NOT proceed

### 3. Version Management

"**Version Management**

**Version Numbering Convention:**
- Major versions: X.0 — New document, new requirements, scope changes, enforcement changes
- Minor versions: X.Y — Clarifications, formatting, contact updates, non-substantive changes
- This is Version **{{policy_version}}** (initial publication)

**Change Log Update:**

| Version | Date | Author | Description | Approved By |
|---------|------|--------|-------------|-------------|
| {{version}} | {{approval_date}} | {{author}} | {{description}} | {{approver}} |

**Previous Version Handling:**

{{IF this supersedes an existing document:}}
- Previous document: {{supersedes}}
- Previous version archived at: {{archive_location}}
- Transition period: {{transition_period}} days
- During transition: both versions available, new version takes precedence
- After transition: previous version marked as 'retired' with redirect to new document

{{IF this is a new document:}}
- No previous version exists
- Effective date: {{effective_date}}

**Version Control Record:**

| Field | Value |
|-------|-------|
| **Document ID** | {{policy_id}} |
| **Version** | {{policy_version}} |
| **Effective Date** | {{effective_date}} |
| **Approved By** | {{approver}} |
| **Approval Date** | {{approval_date}} |
| **Next Review** | {{next_review_date}} |
| **Archive Location** | {{archive_path}} |

Version record confirmed?"

Wait for operator confirmation.

### 4. Publication & Distribution Planning

"**Publication & Distribution Plan**

**Publication Locations:**

| # | Location | Type | Audience | Access Control | Owner |
|---|----------|------|----------|---------------|-------|
| 1 | {{intranet/SharePoint/DMS}} | Primary repository | All authorized personnel | {{access control}} | {{owner}} |
| 2 | {{GRC tool/policy portal}} | Policy management system | Compliance team | {{access control}} | {{owner}} |
| 3 | {{HR portal/employee handbook}} | Reference copy | All employees | {{access control}} | {{owner}} |
| 4 | {{external portal}} (if applicable) | Customer/partner access | External parties | {{access control}} | {{owner}} |

**Distribution Plan:**

| # | Audience Segment | Distribution Method | Timeline | Acknowledgment Required | Follow-Up |
|---|-----------------|-------------------|----------|------------------------|-----------|
| 1 | {{segment_1 — e.g., IT Department}} | {{email/portal/meeting}} | {{when}} | Yes/No | {{follow-up plan}} |
| 2 | {{segment_2 — e.g., All Employees}} | {{email/intranet/LMS}} | {{when}} | Yes/No | {{follow-up plan}} |
| 3 | {{segment_3 — e.g., Contractors}} | {{vendor portal/contract amendment}} | {{when}} | Yes/No | {{follow-up plan}} |
| 4 | {{segment_4 — e.g., Executive Leadership}} | {{briefing/email}} | {{when}} | No | {{follow-up plan}} |

**Classification & Marking:**
- Document classification: {{classification}}
- Classification marking: {{how marked — header/footer/watermark}}
- Distribution restriction: {{who can and cannot share this document externally}}

Review the publication and distribution plan. Any audiences missing? Channels to adjust?"

Wait for operator input.

### 5. Awareness & Training Design

"**Awareness & Training Plan**

Policy awareness is the bridge between a document and behavior change. Different audiences need different awareness approaches.

**Awareness Communications:**

| # | Audience | Message Focus | Channel | Timing | Sender | Tone |
|---|---------|--------------|---------|--------|--------|------|
| 1 | **Executive Leadership** | Strategic impact, regulatory compliance, governance posture | Executive briefing / summary memo | Before publication | CISO/CIO | Strategic |
| 2 | **Management** | Team implications, enforcement responsibilities, exception handling | Management meeting / email | At publication | Policy Owner | Operational |
| 3 | **{{target_audience}} (General)** | What changed, what is required, where to find help | All-staff email / intranet announcement | At publication | CISO + HR | Clear, supportive |
| 4 | **IT/Technical Staff** | Technical requirements, enforcement mechanisms, implementation timeline | Technical briefing / wiki | Before publication | Security Team | Technical |

**Training Requirements:**

| # | Audience | Training Type | Content | Delivery | Duration | Frequency | Mandatory? | Tracking |
|---|---------|-------------|---------|----------|----------|-----------|-----------|----------|
| 1 | {{audience}} | {{type — e.g., CBT, workshop, briefing}} | {{content focus}} | {{LMS/in-person/webinar}} | {{duration}} | {{one-time/annual/on change}} | Yes/No | {{LMS/sign-off sheet}} |
| 2 | | | | | | | | |

**Acknowledgment Tracking:**

| Requirement | Details |
|-------------|---------|
| **Acknowledgment method** | {{electronic signature via LMS / wet signature / email reply}} |
| **Legal validity** | {{confirm with legal that the acknowledgment method is legally defensible}} |
| **Tracking system** | {{LMS / GRC tool / spreadsheet}} |
| **Deadline** | {{days from publication for initial acknowledgment}} |
| **Non-acknowledgment escalation** | {{what happens if someone does not acknowledge — reminder cadence, manager notification, escalation}} |
| **New hire process** | {{when new hires must acknowledge — e.g., first week, onboarding}} |
| **Re-acknowledgment trigger** | {{on major version updates}} |

**Quick Reference Card (Appendix D):**

The Quick Reference Card provides a one-page summary for day-to-day reference:

| What You Must Do | What You Must Not Do | Where to Get Help |
|-----------------|---------------------|-------------------|
| {{top 5-7 DOs from requirements}} | {{top 5-7 DON'Ts from requirements}} | {{help desk / policy owner / wiki}} |

**FAQs:**

| # | Question | Answer |
|---|---------|--------|
| 1 | {{anticipated FAQ}} | {{answer}} |
| 2 | {{anticipated FAQ}} | {{answer}} |
| 3 | {{anticipated FAQ}} | {{answer}} |
| 4 | {{anticipated FAQ}} | {{answer}} |
| 5 | {{anticipated FAQ}} | {{answer}} |

Review the awareness and training plan. Are the audiences, channels, and training requirements appropriate?"

Wait for operator input and iterate.

### 6. Implementation Support

"**Implementation Support**

Beyond awareness, some requirements need active implementation support:

**Technical Controls to Configure:**

| # | Requirement | Control | System/Tool | Configuration | Responsible | Timeline |
|---|------------|---------|-------------|---------------|-------------|----------|
| 1 | STD-## | {{control}} | {{system}} | {{what to configure}} | {{who}} | {{when}} |

**Process Changes:**

| # | Current Process | New Process | Affected Team | Training Needed | Timeline |
|---|---------------|------------|---------------|----------------|----------|
| 1 | {{current}} | {{new}} | {{team}} | Yes/No | {{when}} |

**Transition Period:**

| Phase | Duration | What Applies | Enforcement Level |
|-------|----------|-------------|-------------------|
| **Grace Period** | {{days}} from publication | New policy published, awareness ongoing | Educational — no penalties for inadvertent violations |
| **Transition** | {{days}} after grace | Full requirements in effect, exceptions available | Progressive — minor violations counseled, major violations escalated |
| **Full Enforcement** | After transition | All requirements fully enforceable | Full enforcement per Section 6 |

Review the implementation support plan. Any additional technical or process changes needed?"

Wait for operator input.

### 7. Update Output Document

Update the output document with:
- Approval record in Document Control section
- Updated change log
- Distribution table populated
- Awareness & Training Plan in Appendix C
- Quick Reference Card in Appendix D
- Implementation Checklist in Appendix B
- FAQs appended

Update frontmatter:
- `approval_status: 'approved'` (or 'conditional' if conditions remain)
- `approval_date: '{{date}}'`
- `effective_date: '{{date}}'`
- `publication_date: '{{date}}'`
- `next_review_date: '{{calculated_date}}'`
- `policy_status: 'approved'` (or 'published' if publication is immediate)
- `awareness_plan_created: true`
- `training_requirements: {{count}}`
- `acknowledgment_tracking: true`

### 8. Present MENU OPTIONS

Display menu after approval and publication planning:

"**Select an option:**
[A] Advanced Elicitation — Push deeper on awareness plan coverage, training adequacy, transition period appropriateness, and implementation readiness
[W] War Room — Launch multi-agent adversarial discussion on publication strategy: Red challenges whether awareness will actually reach the audience, Blue validates whether training is sufficient for compliance
[C] Continue — Save and proceed to Step 6: Enforcement & Exception Management (Step 6 of 7)"

#### Menu Handling Logic:

- IF A: Invoke advanced elicitation on publication readiness. Challenge awareness plan coverage (does it reach all audience segments?), probe training adequacy (is the depth sufficient for the complexity?), test transition period (is it long enough for behavior change but short enough for governance?), verify implementation readiness (are technical controls ready? are process changes feasible?). Process insights, update plans if accepted, redisplay menu
- IF W: Invoke spectra-war-room with publication plan as context. Red perspective: how would people avoid or circumvent the awareness program? What enforcement gaps exist during transition? Blue perspective: is the training sufficient? Is the acknowledgment legally defensible? Are the distribution channels comprehensive? Summarize insights, ask operator if they want to adjust, redisplay menu
- IF C: Update output file frontmatter adding `step-05-approval.md` to the end of `stepsCompleted` array, then read fully and follow: `./step-06-enforcement.md`
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer based on policy publication expertise and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, approval_status set, approval_date recorded, effective_date set, publication_date set, next_review_date calculated, awareness_plan_created set to true, training_requirements populated, acknowledgment_tracking set, and output document updated with approval record, distribution table, awareness plan, quick reference card, and implementation checklist], will you then read fully and follow: `./step-06-enforcement.md` to begin enforcement and exception management design.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Step 4 completion verified before proceeding
- Pre-approval verification completed with all prerequisites checked
- Approval package prepared with complete information for the approval authority
- Formal approval decision recorded with approver name, date, and conditions (if any)
- Version management applied with change log updated and previous version archived (if applicable)
- Publication locations identified with access control
- Distribution plan designed covering all audience segments
- Awareness communications planned for each audience with appropriate channel and timing
- Training requirements defined with content, delivery method, duration, and tracking
- Acknowledgment tracking designed with legally defensible method
- Quick Reference Card drafted for day-to-day reference
- FAQs developed anticipating common questions
- Implementation support planned (technical controls, process changes, transition period)
- Output document updated with approval record, distribution, awareness, and implementation details
- Frontmatter updated with approval_status, dates, awareness_plan_created, training_requirements

### SYSTEM FAILURE:

- Proceeding without verifying Step 4 completion
- Declaring approval without operator confirmation of approval authority sign-off
- Modifying policy requirements at this stage without returning to Step 3/4
- Not preparing a formal approval package for the approval authority
- Not recording the approval decision with date, approver, and conditions
- Not applying version management (version number, change log, effective date)
- Not planning publication and distribution to all target audience segments
- Not designing an awareness and training program proportionate to the requirements
- Not establishing acknowledgment tracking for compliance evidence
- Not planning a transition period for behavior change
- Defining enforcement monitoring mechanisms or building the exception register — those are Step 6
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted and approval/publication fields

**Master Rule:** Approval without publication is a secret. Publication without awareness is decoration. Awareness without training is negligence. The entire purpose of Steps 1-4 is to produce a document that changes organizational behavior — this step is where that transformation from document to practice begins. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
