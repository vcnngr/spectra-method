# Step 1B: Workflow Resumption

## STEP GOAL:

Resume the policy lifecycle workflow from where it was left off, ensuring smooth continuation with full context restoration including engagement scope, policy requirement, document type, scope definition, framework alignment, stakeholder register, drafting progress, review status, approval state, and all prior lifecycle findings.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A POLICY AUTHOR resuming authorized work
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Scribe, a Policy Author with 8 years of security policy experience, resuming an active policy lifecycle engagement
- ✅ Resume workflow from exact point where it was interrupted
- ✅ Re-verify that the engagement is still active and dates are still valid
- ✅ All prior findings and document state remain valid unless scope has changed
- ✅ Policy timeliness matters — flag if significant time has passed since last activity (regulatory deadlines, audit timelines, stakeholder availability may have shifted)

### Step-Specific Rules:

- 💬 FOCUS on understanding where we left off and continuing appropriately
- 🚫 FORBIDDEN to modify content completed in previous steps
- 📖 Reload engagement.yaml to re-verify authorization
- 🔒 If engagement has expired since last session: HARD STOP
- 🔒 If scope has been amended since last session: flag changes to operator
- ⏰ If significant delay has occurred, warn the operator about potential impacts:
  - Regulatory deadlines may have shifted or passed
  - Stakeholder availability may have changed
  - Organizational changes may affect scope
  - Framework versions may have been updated
  - Related policies may have been modified by others

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Resuming a workflow on an expired or deactivated engagement invalidates all prior authorization — re-verification is essential before any policy lifecycle activity continues
  - Resuming after a significant time gap may mean regulatory requirements have changed — new regulations, updated frameworks, or revised compliance deadlines may affect the policy content drafted so far
  - Skipping to a future step without verifying document state consistency may lead to a policy with gaps between sections — for example, requirements drafted in step 03 that no longer align with the scope defined in step 01 because organizational changes occurred during the gap
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking action
- Update frontmatter: add this step name to the end of the stepsCompleted array
- 📖 Reload engagement.yaml and verify it is still active
- 🚫 FORBIDDEN to begin new policy lifecycle activities during continuation setup

## CONTEXT BOUNDARIES:

- Available context: Current document and frontmatter are already loaded
- Focus: Workflow state analysis and continuation logic only
- Limits: Don't assume knowledge beyond what's in the document and engagement.yaml
- Dependencies: Existing workflow state from previous session

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Re-verify Engagement Authorization

**Before anything else:**

- Reload `engagement.yaml`
- Verify `status` is still `active`
- Verify dates: `start_date <= today <= end_date`
- Verify GRC operations are still authorized in the engagement
- If engagement has expired or been deactivated:

"**BLOCK — Engagement no longer active.**

Engagement {{engagement_id}} is now {{expired/deactivated}} since your last session.
No policy lifecycle activity may continue.
Contact the engagement lead for renewal."

**HARD STOP — Do not proceed.**

### 2. Analyze Current State

**State Assessment:**

Review the frontmatter to understand the complete workflow state:

**Identity & Classification Fields:**
- `stepsCompleted`: Array of completed step filenames (last element = most recently completed)
- `engagement_id`, `engagement_name`: Engagement context
- `policy_id`, `policy_name`: Policy identity
- `policy_type`: Document type (policy/standard/procedure/guideline)
- `policy_version`, `policy_status`: Version and lifecycle status
- `classification`: Document classification level (public/internal/confidential/restricted)

**Stakeholder Fields:**
- `owner`, `author`, `approver`: Core stakeholder assignments
- `reviewers_signed_off`: Count of reviewer approvals obtained
- `reviewers_total`: Total reviewers identified for the review cycle

**Scope & Alignment Fields:**
- `framework_alignment`: Mapped frameworks (array — ISO 27001, NIST 800-53, CIS, SOC 2, PCI DSS, etc.)
- `controls_addressed`: Specific controls (array — individual control IDs)
- `scope_departments`, `scope_systems`: Scope boundaries
- `target_audience`: Who must comply with this document
- `policy_trigger`: What drove this lifecycle engagement (new/review/gap/regulatory/org-change/framework)
- `regulatory_drivers`: Applicable regulations (array)
- `related_policies`: Policy landscape (array — parent, child, sibling documents)

**Lifecycle Progress Fields:**
- `research_complete`: Whether research phase completed (boolean)
- `drafting_complete`: Whether drafting phase completed (boolean)
- `review_cycles_completed`: Number of review iterations completed
- `approval_status`: Current approval state (pending/conditional/approved/rejected)
- `approval_date`: When approved (if applicable)
- `effective_date`: When policy becomes enforceable (if set)
- `publication_date`: When published (if applicable)
- `next_review_date`: When next review is due (if set)

**Enforcement & Governance Fields:**
- `awareness_plan_created`: Whether awareness plan exists (boolean)
- `training_requirements`: Count of training items defined
- `acknowledgment_tracking`: Whether acknowledgment tracking is configured (boolean)
- `enforcement_mechanisms`: Count of enforcement mechanisms defined
- `automated_controls`: Count of automated enforcement mechanisms
- `manual_controls`: Count of manual enforcement mechanisms
- `detective_controls`: Count of detective mechanisms
- `corrective_controls`: Count of corrective mechanisms
- `compliance_kpis`: Count of KPIs defined
- `exception_process_defined`: Whether exception process exists (boolean)
- `violation_framework_defined`: Whether violation handling exists (boolean)
- `review_schedule_set`: Whether review schedule is established (boolean)
- `maintenance_plan_created`: Whether maintenance plan exists (boolean)
- `lifecycle_report_complete`: Whether the final lifecycle report has been generated (boolean)

**Time Gap Assessment:**

- Calculate time elapsed since last activity (use the most recent stepsCompleted entry timestamp or change_log entry)
- If more than 7 days have passed since last activity, warn:

"**NOTICE — Time gap detected since last policy lifecycle activity.**

Last activity was approximately {{elapsed_time}} ago.

**Potential impacts of the time gap:**

| Area | Concern | Action Needed |
|------|---------|---------------|
| **Regulatory deadlines** | {{regulation}} deadline may have shifted | Verify compliance timeline |
| **Stakeholder availability** | Reviewers/approvers may have changed roles or availability | Re-confirm stakeholder register |
| **Organizational changes** | Restructuring, system changes, or process changes may affect scope | Verify scope is still accurate |
| **Framework updates** | Control frameworks or regulatory guidance may have been updated | Check for framework version changes |
| **Related policies** | Other policy documents may have been created or modified | Check for conflicts or dependencies |
| **Threat landscape** | New incidents or vulnerabilities may inform policy requirements | Review recent incident data |

Consider whether any of these factors require revisiting completed steps before continuing.

For each concern area, recommend a specific validation action:
- **Regulatory deadlines**: Check the `regulatory_drivers` array against current regulatory calendars
- **Stakeholder availability**: Confirm that `owner`, `approver`, and reviewers in the stakeholder register are still in their roles
- **Organizational changes**: Verify that `scope_departments` and `scope_systems` still reflect organizational reality
- **Framework updates**: Check whether any framework in `framework_alignment` has released a new version since last activity
- **Related policies**: Verify that documents in `related_policies` have not been modified or retired"

- If more than 30 days have passed, escalate the warning:

"**WARNING — Significant delay detected ({{elapsed_time}}).**

A policy lifecycle engagement inactive for more than 30 days has a high probability of scope drift. Strongly recommend re-validating:
1. Policy scope still reflects organizational reality
2. Stakeholders are still available and engaged
3. Regulatory deadlines have not passed
4. Framework requirements have not changed
5. Related policies have not created conflicts

Proceed with caution, or consider restarting specific steps if significant changes are identified."

### 3. Determine Next Step

**Step Sequence Lookup:**

Use the following ordered sequence to determine the next step from the last completed step:

| Last Completed | Next Step | Next Step Description |
|---|---|---|
| step-01-init.md | step-02-research.md | Research & Benchmarking |
| step-02-research.md | step-03-drafting.md | Policy Drafting |
| step-03-drafting.md | step-04-review.md | Stakeholder Review & Iteration |
| step-04-review.md | step-05-approval.md | Approval, Publication & Awareness |
| step-05-approval.md | step-06-enforcement.md | Enforcement & Exception Management |
| step-06-enforcement.md | step-07-reporting.md | Review, Maintenance & Closure |

1. Get the last element from the `stepsCompleted` array
2. Look it up in the table above to find the next step
3. That's the next step to load

**Example:**
- If `stepsCompleted = ["step-01-init.md", "step-02-research.md", "step-03-drafting.md"]`
- Last element is `"step-03-drafting.md"`
- Table lookup: next step is `./step-04-review.md`

### 4. Handle Workflow Completion

**If `stepsCompleted` array contains `"step-07-reporting.md"`:**

"The policy lifecycle workflow for **{{policy_name}}** (`{{policy_id}}`) in engagement **{{engagement_name}}** has already been completed.

The final policy document is available at `{outputFile}` with all sections completed.

**Final Results:**

| Field | Value |
|-------|-------|
| **Policy ID** | {{policy_id}} |
| **Policy Name** | {{policy_name}} |
| **Document Type** | {{policy_type}} |
| **Version** | {{policy_version}} |
| **Status** | {{policy_status}} |
| **Effective Date** | {{effective_date}} |
| **Next Review** | {{next_review_date}} |
| **Owner** | {{owner}} |
| **Approver** | {{approver}} |
| **Framework Alignment** | {{framework_alignment}} |
| **Controls Addressed** | {{controls_addressed count}} |
| **Enforcement Mechanisms** | {{enforcement_mechanisms}} |
| **Exception Process** | {{exception_process_defined}} |
| **Review Schedule** | {{review_schedule_set}} |

Would you like to:
- Review the policy document with you
- Start a new policy within the same engagement (launch a fresh `spectra-policy-lifecycle`)
- Launch a compliance audit to verify this policy against framework requirements (via `spectra-compliance-audit`)
- Launch a risk assessment to evaluate risks this policy addresses (via `spectra-risk-assessment`)
- Launch a War Room session to stress-test the policy with Red vs Blue perspectives

How would you like to proceed?"

### 5. Present Current Progress

**If workflow not complete:**

"Welcome back {{user_name}}! Resuming the policy lifecycle workflow for **{{engagement_name}}**.

**Engagement:** {{engagement_id}} — Still active
**Remaining period:** until {{end_date}}

**Policy Under Development:**

| Field | Value |
|-------|-------|
| **Policy ID** | {{policy_id}} |
| **Policy Name** | {{policy_name}} |
| **Document Type** | {{policy_type}} |
| **Version** | {{policy_version}} |
| **Status** | {{policy_status}} |
| **Owner** | {{owner}} |
| **Approver** | {{approver}} |

**Scope:**
- Departments: {{scope_departments}}
- Systems: {{scope_systems}}
- Target Audience: {{target_audience}}

**Framework Alignment:** {{framework_alignment}}
**Regulatory Drivers:** {{regulatory_drivers or 'None identified'}}

**Current Progress:**

| Step | Description | Status |
|------|-------------|--------|
| Step 1: Initialization | Policy Requirement & Scope | {{Completed/Pending}} |
| Step 2: Research | Research & Benchmarking | {{Completed/Pending}} |
| Step 3: Drafting | Policy Drafting | {{Completed/Pending}} |
| Step 4: Review | Stakeholder Review | {{Completed/Pending}} |
| Step 5: Approval | Approval & Publication | {{Completed/Pending}} |
| Step 6: Enforcement | Enforcement & Exceptions | {{Completed/Pending}} |
| Step 7: Reporting | Review & Closure | {{Completed/Pending}} |

**Last step completed:** {{last step filename from stepsCompleted array}}
**Next step:** {{next step from lookup table}} — {{next step description}}

**Key Metrics:**
- Research complete: {{research_complete}}
- Drafting complete: {{drafting_complete}}
- Review cycles: {{review_cycles_completed}}
- Reviewers signed off: {{reviewers_signed_off}} / {{reviewers_total}}
- Approval status: {{approval_status}}
- Enforcement mechanisms: {{enforcement_mechanisms}}
- Exception process: {{exception_process_defined}}

**Completed document sections:**

| Step Completed | Document Sections Populated |
|---|---|
| step-01-init.md | Document Control, Purpose & Scope (Section 1), Document Hierarchy, Initial Framework Alignment |
| step-02-research.md | Research & Benchmarking Summary, Policy Coverage Matrix, Regulatory Mapping |
| step-03-drafting.md | Policy Statements (Section 2), Standards & Requirements (Section 3), Procedures (Section 4), Roles & Responsibilities (Section 5), Compliance & Enforcement framework (Section 6), Exceptions Process (Section 7), Related Documents (Section 8), Definitions (Section 9), Review & Maintenance (Section 10) |
| step-04-review.md | Review History updated, feedback tracked, sign-offs recorded |
| step-05-approval.md | Approval record, Distribution table, Appendix B (Implementation), Appendix C (Awareness), Appendix D (Quick Reference) |
| step-06-enforcement.md | Enforcement mechanisms detailed in Section 6, Exception register structure in Section 7, Compliance KPIs |

**Sections populated based on completed steps:**
{{list only sections for steps that appear in stepsCompleted}}

Everything correct? Would you like to make adjustments before continuing?"

### 6. Present MENU OPTIONS

Display: "**Select an option:** [C] Continue to {{next step name}} ({{next step description}})"

#### Menu Handling Logic:

- IF C: Read fully and follow the next step determined from the lookup table in step 3
- IF Any other comments or queries: respond and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [current state confirmed and engagement re-verified], will you then read fully and follow the next step (from the lookup table) to resume the workflow.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Engagement re-verified as still active with valid dates and GRC operations still authorized
- All previous workflow state accurately analyzed and presented with policy lifecycle metrics
- Time gap assessed and operator warned if scope drift, regulatory changes, or stakeholder shifts may have occurred
- Correct next step identified from the lookup table
- Completed workflow detected and appropriate options presented (new policy, compliance audit, risk assessment, war room)
- User confirms understanding of progress before continuation

### SYSTEM FAILURE:

- Not re-verifying engagement authorization before continuing
- Continuing work on an expired or deactivated engagement
- Continuing when GRC operations authorization has been revoked from the engagement
- Modifying content from already completed steps
- Failing to determine the next step from the lookup table
- Not flagging significant time gaps that may affect policy currency, regulatory compliance, or stakeholder availability
- Proceeding without user confirmation of current state
- Beginning policy lifecycle activities during continuation setup
- Not detecting a completed workflow (step-07-reporting.md in stepsCompleted)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No policy lifecycle operations on expired engagements.
