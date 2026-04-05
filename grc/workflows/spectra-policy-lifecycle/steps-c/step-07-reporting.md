# Step 7: Review, Maintenance & Closure

**Progress: Step 7 of 7** — This is the final step.

## STEP GOAL:

Compile the complete policy lifecycle report — finalized policy document with all sections complete, document control verified, cross-framework mapping validated, review schedule established with trigger events, maintenance plan with version control and update processes, policy metrics summary (requirements, controls, enforcement mechanisms, exceptions, framework coverage), engagement status update, Chronicle recommendation — and formally close the policy lifecycle engagement. This is the capstone step that transforms six steps of policy development into a complete, published, maintained governance document that will protect the organization for years if managed according to the maintenance plan.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER finalize the policy lifecycle report or close the engagement without operator review and confirmation
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the FINAL step — there is no next step file to load
- 📋 YOU ARE A POLICY LIFECYCLE COMPLETION FACILITATOR — the operator confirms that the policy is complete, the lifecycle documentation is accurate, and the engagement can be closed
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Scribe, a Policy Author completing the policy lifecycle and establishing the maintenance plan
- ✅ The policy document IS the deliverable — a policy without maintenance is a snapshot that decays into irrelevance. The maintenance plan is what gives the policy longevity.
- ✅ "A policy nobody reads protects nobody" — and a policy nobody maintains becomes a liability. Outdated policies create false confidence, mislead auditors, and fail to address current threats.
- ✅ Every section of the policy must be populated — an incomplete policy undermines the credibility of the entire governance program and may fail regulatory scrutiny
- ✅ The lifecycle report provides the evidence trail: what was done, why, by whom, and how the policy will be maintained going forward. This is what auditors review.

### Step-Specific Rules:

- 🎯 Focus exclusively on policy document finalization, cross-framework validation, review schedule establishment, maintenance plan creation, metrics compilation, and engagement closure
- 🚫 FORBIDDEN to re-open drafting, modify requirements, alter enforcement mechanisms, or change approval decisions — those were finalized in prior steps. If changes are needed, the operator must explicitly request revisiting a prior step.
- 💬 Approach: synthesis and closure — compile the complete lifecycle record, verify completeness, establish the maintenance framework, and close the engagement cleanly
- 📊 The policy metrics summary must be comprehensive — it is the executive-level view of what the policy lifecycle produced
- 🔒 Final document classification and distribution restrictions must be confirmed
- ⏱️ This step produces the final deliverable and closes the engagement — quality and completeness are paramount

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your lifecycle management expertise ensures the policy will be maintained, reviewed, and updated as the organization evolves
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - No review schedule set — explain assessment decay risk: a policy is a point-in-time document. Without defined review triggers and a scheduled review date, the policy will silently become outdated as regulations change, threats evolve, and the organization transforms. Within 18 months, an unreviewed policy will contain requirements that are either impossible, irrelevant, or insufficient. Every framework (ISO 27001, NIST, SOC 2) requires periodic policy review.
  - No maintenance owner assigned — explain orphan policy risk: a policy without a designated maintenance owner has no one accountable for keeping it current. When the annual review date arrives, no one initiates the review. When an incident reveals a gap, no one updates the policy. The policy becomes a zombie document — technically alive but functionally dead.
  - Engagement closure without confirming all deliverables — explain incomplete handover risk: closing the engagement without verifying that the policy is published, awareness is scheduled, enforcement is configured, and the exception process is operational means some post-lifecycle activities may never happen. The engagement closure checklist exists to prevent this.
  - Policy metrics not compiled — explain institutional knowledge loss risk: the metrics summary captures what was built, how many requirements, which frameworks, how many reviewers, what enforcement mechanisms. Without this, the next review cycle starts from scratch and the organization cannot measure policy program maturity over time.
  - No Chronicle recommendation — explain continuity risk: recording the policy lifecycle engagement in Chronicle provides organizational memory across engagement boundaries. Future assessments, audits, and policy reviews can reference this engagement's decisions and rationale.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks. The operator decides, you facilitate.

## EXECUTION PROTOCOLS:

- 🎯 Load output document and verify that `step-06-enforcement.md` is present in the `stepsCompleted` array — all six prior steps must be complete before lifecycle closure
- ⚠️ Present [A]/[W] menu plus final navigation options after closure — there is NO [C] Continue option as this is the final step
- 💾 Save all finalization content to the output document
- 📖 Update frontmatter: add this step name to the end of stepsCompleted, set `policy_status` to final status, and update all final tracking fields
- 💾 Update frontmatter fields: `review_schedule_set: true`, `maintenance_plan_created: true`, `lifecycle_report_complete: true`, `chronicle_recommended: true`, `policy_status: 'published'`
- 🎯 Perform final frontmatter consistency check — verify ALL frontmatter fields are populated and internally consistent with the document body
- 🚫 This is the FINAL step — there is no next step file

## CONTEXT BOUNDARIES:

- Available context: Complete policy lifecycle data from steps 1-6 (Requirement & Scope, Research & Benchmarking, Policy Drafting, Stakeholder Review, Approval & Publication, Enforcement & Exceptions), all frontmatter fields, engagement.yaml, complete policy document
- Focus: Policy document finalization, cross-framework validation, review schedule, maintenance plan, metrics compilation, engagement closure — no new content creation
- Limits: Do not fabricate requirements, inflate coverage, or embellish the policy. Do not modify requirements, enforcement mechanisms, or approval decisions — those are finalized in prior steps. Do not create new policy content — only compile, validate, and plan for maintenance.
- Dependencies: All prior steps (1-6) should be completed. If any step was not completed, WARN the operator before proceeding.

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Complete Policy State

Load the output document and verify all six prior steps are complete:

"**Policy Lifecycle Closure — Loading Complete Policy State**

I will verify that all analytical and governance steps are complete before finalizing the policy lifecycle."

**Verification Checklist:**

| # | Step | Expected in stepsCompleted | Status |
|---|------|---------------------------|--------|
| 1 | Requirement & Scope | step-01-init.md | {{Present / Missing}} |
| 2 | Research & Benchmarking | step-02-research.md | {{Present / Missing}} |
| 3 | Policy Drafting | step-03-drafting.md | {{Present / Missing}} |
| 4 | Stakeholder Review | step-04-review.md | {{Present / Missing}} |
| 5 | Approval & Publication | step-05-approval.md | {{Present / Missing}} |
| 6 | Enforcement & Exceptions | step-06-enforcement.md | {{Present / Missing}} |

{{IF any step is missing:}}
**WARNING — Incomplete Policy Lifecycle:**
The following steps are not marked as completed: {{list missing steps}}. A policy published without completing all lifecycle steps will have gaps.

**Options:**
- [R] Return to the missing step to complete the work
- [P] Proceed with closure — gaps will be documented as known limitations

Which option?
{{END IF}}

{{IF all steps present:}}
**All 6 lifecycle steps confirmed complete. Proceeding with final closure.**
{{END IF}}

### 2. Policy Document Finalization

Verify every section of the policy document is complete and consistent:

"**Policy Document — Section Completeness Check**

| # | Section | Status | Items | Quality Check |
|---|---------|--------|-------|--------------|
| 0 | Document Control | {{Complete/Incomplete}} | Version, change log, review history, distribution | {{issues}} |
| 1 | Purpose & Scope | {{Complete/Incomplete}} | Purpose statement, scope tables, hierarchy, framework alignment | {{issues}} |
| 2 | Policy Statements | {{Complete/Incomplete}} | {{count}} PS-## statements | {{issues}} |
| 3 | Standards & Requirements | {{Complete/Incomplete}} | {{count}} STD-## requirements | {{issues}} |
| 4 | Procedures | {{Complete/Incomplete}} | {{count}} PRC-## procedures | {{issues}} |
| 5 | Roles & Responsibilities | {{Complete/Incomplete}} | RACI matrix, role definitions | {{issues}} |
| 6 | Compliance & Enforcement | {{Complete/Incomplete}} | {{count}} mechanisms, KPIs, violation framework | {{issues}} |
| 7 | Exceptions Process | {{Complete/Incomplete}} | Workflow, register, approval authority | {{issues}} |
| 8 | Related Documents | {{Complete/Incomplete}} | Cross-references | {{issues}} |
| 9 | Definitions & Glossary | {{Complete/Incomplete}} | {{count}} terms | {{issues}} |
| 10 | Review & Maintenance | {{Complete/Incomplete}} | Schedule, triggers, maintenance classification | {{issues}} |
| A | Appendix A: Framework Mapping | {{Complete/Incomplete}} | Cross-framework control table | {{issues}} |
| B | Appendix B: Implementation Checklist | {{Complete/Incomplete}} | Action items with owners and deadlines | {{issues}} |
| C | Appendix C: Awareness & Training Plan | {{Complete/Incomplete}} | Training matrix, acknowledgment plan | {{issues}} |
| D | Appendix D: Quick Reference Card | {{Complete/Incomplete}} | DOs, DON'Ts, help contacts | {{issues}} |

**Cross-Reference Validation:**

| Check | Result |
|-------|--------|
| Every PS-## statement has at least one STD-## implementing it | {{Pass/Fail}} |
| Every STD-## maps to at least one framework control | {{Pass/Fail}} |
| Every STD-## has at least one enforcement mechanism | {{Pass/Fail}} |
| RACI matrix covers all policy activities | {{Pass/Fail}} |
| Exception approval authorities match enforcement section | {{Pass/Fail}} |
| Violation classifications match enforcement section | {{Pass/Fail}} |
| Related documents list is current | {{Pass/Fail}} |
| All terms in the document are defined in the glossary | {{Pass/Fail}} |

{{IF any issues found:}}
**Issues to Resolve:**
| # | Issue | Section | Resolution |
|---|-------|---------|-----------|
| 1 | {{issue}} | {{section}} | {{fix}} |

Shall I address these issues now?"

Wait for operator decision. Fix any issues identified.

### 3. Cross-Framework Mapping Validation

"**Cross-Framework Control Mapping — Final Validation**

Verify that Appendix A is complete and accurate:

**Appendix A: Framework Control Mapping**

| Policy Requirement | ISO 27001:2022 | NIST 800-53 Rev. 5 | CIS Controls v8 | SOC 2 TSC | PCI DSS v4.0 | Other |
|-------------------|---------------|--------------------|--------------------|-----------|-------------|-------|
| PS-01 / STD-01 | {{control}} | {{control}} | {{control}} | {{criteria}} | {{req}} | {{other}} |
| PS-02 / STD-02 | | | | | | |
| PS-03 / STD-03 | | | | | | |

**Framework Coverage Summary:**

| Framework | Total Controls Mapped | Coverage | Gaps |
|-----------|---------------------|----------|------|
| ISO 27001:2022 | {{count}} | {{coverage %}} | {{gaps}} |
| NIST 800-53 Rev. 5 | {{count}} | {{coverage %}} | {{gaps}} |
| CIS Controls v8 | {{count}} | {{coverage %}} | {{gaps}} |
| SOC 2 TSC | {{count}} | {{coverage %}} | {{gaps}} |
| PCI DSS v4.0 | {{count}} | {{coverage %}} | {{gaps}} |

Any framework control gaps to address?"

Wait for operator validation.

### 4. Review Schedule & Trigger Events

"**Review Schedule — Final Configuration**

**Scheduled Review:**

| Field | Value |
|-------|-------|
| **Review frequency** | {{frequency — annual minimum for policies, semi-annual for standards}} |
| **Next review date** | {{calculated from effective_date + frequency}} |
| **Review owner** | {{policy_owner}} |
| **Review process** | {{minor: owner review + update / major: full Steps 3-5 cycle}} |
| **Review duration** | {{estimated calendar days for review cycle}} |

**Trigger Events for Unscheduled Review:**

| # | Trigger Event | Detection Method | Response Time | Process |
|---|-------------|-----------------|---------------|---------|
| 1 | **Regulatory change** affecting this domain | Regulatory monitoring, legal team notification | 30 days assessment | Assess impact → minor or major update |
| 2 | **Security incident** revealing a policy gap | Post-incident review (PIR), lessons learned | 14 days assessment | Gap analysis → emergency or major update |
| 3 | **Organizational restructuring** affecting scope | HR/business notification | 60 days assessment | Scope review → minor or major update |
| 4 | **Technology change** affecting enforceability | IT change management, architecture review | 30 days assessment | Enforcement review → minor or major update |
| 5 | **Audit finding** related to this policy | Internal/external audit report | Per audit timeline | Finding remediation → minor or major update |
| 6 | **Framework update** (new version released) | Framework monitoring, GRC team | 90 days assessment | Gap analysis → major update |
| 7 | **Risk assessment finding** in this domain | Risk assessment output | Per risk treatment timeline | Requirement review → minor or major update |
| 8 | **Executive/board request** | Direct request | As specified | Scoped review per request |
| 9 | **Significant non-compliance trend** | Compliance KPI monitoring | 30 days assessment | Root cause → enforcement or policy change |
| 10 | **Third-party/supply chain change** | Vendor management, procurement | 60 days assessment | Scope and requirement review |

**Review Checklist for Future Reviewers:**

| # | Check Item | How to Verify |
|---|-----------|---------------|
| 1 | Are all regulatory requirements still current? | Cross-reference regulatory tracking service |
| 2 | Are framework controls still mapped correctly? | Verify against latest framework version |
| 3 | Are enforcement mechanisms still operational? | Test automated controls, verify manual processes |
| 4 | Is the target audience still accurately defined? | Review organizational structure changes |
| 5 | Are exception registers current? | Review active exceptions, expired exceptions |
| 6 | Are compliance KPIs meeting targets? | Review dashboard metrics |
| 7 | Have related policies changed? | Cross-reference related document list |
| 8 | Are procedures still operationally valid? | Validate with operational staff |
| 9 | Is the glossary still accurate? | Review terms against current usage |
| 10 | Does the Quick Reference Card reflect current requirements? | Compare against Section 2-3 |

Review the maintenance schedule and trigger events. Adjustments needed?"

Wait for operator input.

### 5. Maintenance Plan

"**Maintenance Plan**

**Version Control Process:**

| Update Type | Version Change | Process | Approval | Communication |
|-------------|---------------|---------|----------|---------------|
| **Minor** (clarifications, formatting, contacts) | X.Y → X.(Y+1) | Author updates, owner reviews | Policy Owner | Notification to stakeholders |
| **Major** (new requirements, scope changes) | X.Y → (X+1).0 | Full review cycle (Steps 3-5) | Original approval authority | Full awareness and training cycle |
| **Emergency** (critical gap, active incident) | X.Y → X.(Y+1)-EM | 48-hour expedited review | CISO + Policy Owner | Immediate notification, training within 7 days |
| **Retirement** (policy no longer needed) | N/A → Retired | Sunset review | Original approval authority | Notification with replacement reference |

**Retirement/Sunset Process:**
1. Identify reason for retirement (superseded, domain no longer applicable, consolidated)
2. Verify no orphan dependencies (standards, procedures, guidelines that reference this policy)
3. Notify all stakeholders of retirement date and replacement document (if any)
4. Archive the document with full change history
5. Update all cross-references in related documents
6. Remove from active policy repository
7. Retain in archive per record retention requirements

**Archive Requirements:**

| Field | Value |
|-------|-------|
| **Archive location** | {{archive path}} |
| **Retention period** | {{per organizational retention policy and regulatory requirements}} |
| **Access** | {{who can access archived versions}} |
| **Format** | {{PDF/Markdown/both — immutable format for audit trail}} |

Confirm the maintenance plan."

Wait for operator input.

### 6. Policy Metrics Summary

"**Policy Lifecycle Metrics Summary**

This is the executive-level view of what the policy lifecycle produced:

**Document Metrics:**

| Metric | Value |
|--------|-------|
| **Policy ID** | {{policy_id}} |
| **Policy Name** | {{policy_name}} |
| **Document Type** | {{policy_type}} |
| **Version** | {{policy_version}} |
| **Status** | {{policy_status}} |
| **Effective Date** | {{effective_date}} |
| **Next Review** | {{next_review_date}} |
| **Classification** | {{classification}} |

**Content Metrics:**

| Metric | Count |
|--------|-------|
| Policy statements (PS-##) | {{count}} |
| Standards/requirements (STD-##) | {{count}} |
| Procedures (PRC-##) | {{count}} |
| Roles defined | {{count}} |
| Definitions in glossary | {{count}} |

**Framework Coverage:**

| Metric | Count |
|--------|-------|
| Frameworks aligned | {{count}} |
| Specific controls addressed | {{count}} |
| Regulatory requirements satisfied | {{count}} |

**Stakeholder Engagement:**

| Metric | Count |
|--------|-------|
| Reviewers engaged | {{reviewers_total}} |
| Reviewers signed off | {{reviewers_signed_off}} |
| Review cycles completed | {{review_cycles_completed}} |
| Approval authority | {{approver}} |

**Enforcement Coverage:**

| Metric | Count |
|--------|-------|
| Total enforcement mechanisms | {{enforcement_mechanisms}} |
| Automated controls | {{automated_controls}} |
| Manual controls | {{manual_controls}} |
| Detective controls | {{detective_controls}} |
| Corrective controls | {{corrective_controls}} |
| Compliance KPIs | {{compliance_kpis}} |
| Exception process defined | {{exception_process_defined}} |
| Violation framework defined | {{violation_framework_defined}} |

**Awareness & Training:**

| Metric | Value |
|--------|-------|
| Awareness plan created | {{awareness_plan_created}} |
| Training requirements | {{training_requirements}} |
| Acknowledgment tracking | {{acknowledgment_tracking}} |

**Lifecycle Status:**

| Metric | Value |
|--------|-------|
| Lifecycle start | {{initialization_timestamp}} |
| Lifecycle end | {{current_date}} |
| Total lifecycle duration | {{duration}} |
| Steps completed | 7/7 |
| Review schedule set | {{review_schedule_set}} |
| Maintenance plan created | {{maintenance_plan_created}} |

Review the metrics summary. Accurate?"

Wait for operator confirmation.

### 7. Engagement Status Update

"**Engagement Status Update**

The policy lifecycle engagement for **{{policy_name}}** is ready for closure:

**Engagement Summary:**

| Field | Value |
|-------|-------|
| **Engagement** | {{engagement_name}} (`{{engagement_id}}`) |
| **Deliverable** | {{policy_name}} (`{{policy_id}}`) |
| **Document Type** | {{policy_type}} |
| **Final Status** | Published |
| **Output Location** | `{outputFile}` |
| **Effective Date** | {{effective_date}} |
| **Next Review** | {{next_review_date}} |

**Post-Lifecycle Actions:**

| # | Action | Responsible | Timeline | Status |
|---|--------|------------|----------|--------|
| 1 | Publish document to {{publication_location}} | {{owner}} | Immediate | Pending |
| 2 | Distribute to {{target_audience}} | {{author}} | Within {{days}} days | Pending |
| 3 | Schedule awareness communications | {{training_coordinator}} | Per awareness plan | Pending |
| 4 | Configure automated enforcement controls | {{IT/security team}} | Per implementation plan | Pending |
| 5 | Initialize exception register | {{policy_owner}} | At publication | Pending |
| 6 | Configure compliance monitoring/KPIs | {{compliance_team}} | Within {{days}} days | Pending |
| 7 | Schedule next review | {{policy_owner}} | {{next_review_date}} | Pending |

**Chronicle Recommendation:**
I recommend recording this policy lifecycle engagement in Chronicle to maintain organizational memory. Future engagements — compliance audits, risk assessments, policy reviews, and incident investigations — can reference the decisions, rationale, and framework mappings from this engagement.

Would you like to initiate a Chronicle entry for this engagement?"

Wait for operator response.

### 8. Final Frontmatter Update

Update all frontmatter fields to final state:
- `policy_status: 'published'`
- `review_schedule_set: true`
- `maintenance_plan_created: true`
- `lifecycle_report_complete: true`
- `chronicle_recommended: true`
- Add `step-07-reporting.md` to `stepsCompleted` array
- Verify ALL frontmatter fields are populated and consistent with document body

### 9. Present Final Navigation

"**Policy Lifecycle Complete**

**{{policy_name}}** (`{{policy_id}}`) has been successfully developed, reviewed, approved, published, and equipped with enforcement mechanisms, exception management, and a maintenance plan.

**Document:** `{outputFile}`

**Select an option:**
[A] Advanced Elicitation — Final quality review: challenge completeness, probe maintenance plan robustness, stress-test enforcement coverage
[W] War Room — Launch multi-agent adversarial discussion on the final policy: Red stress-tests enforceability and identifies loopholes, Blue validates framework coverage and operational readiness
[N] New Policy — Launch a new `spectra-policy-lifecycle` engagement for another policy, standard, procedure, or guideline within the same engagement
[C] Compliance Audit — Hand off to Auditor agent via `spectra-compliance-audit` to verify this policy against framework requirements
[R] Risk Assessment — Hand off to Arbiter agent via `spectra-risk-assessment` to evaluate the risks this policy addresses"

#### Menu Handling Logic:

- IF A: Invoke advanced elicitation on final policy quality. Challenge completeness (any sections still thin?), probe maintenance plan (will the review actually happen?), stress-test enforcement (are all mechanisms implementable?), verify metrics accuracy. Process insights, update if needed, redisplay menu
- IF W: Invoke spectra-war-room with final policy as context. Red perspective: where are the loopholes? Which requirements will be circumvented first? What enforcement blind spots exist? Blue perspective: is the framework coverage defensible under audit? Is the maintenance plan realistic? Is the awareness plan sufficient? Summarize insights, redisplay menu
- IF N: Inform operator to invoke `spectra-policy-lifecycle` to start a new policy lifecycle engagement
- IF C: Inform operator to invoke `spectra-compliance-audit` to audit this policy against framework requirements
- IF R: Inform operator to invoke `spectra-risk-assessment` to assess risks in this policy's domain
- IF user asks questions: Answer based on policy lifecycle expertise and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting navigation options
- This is the FINAL step — there is no [C] Continue option to a next step

## CRITICAL STEP COMPLETION NOTE

This is the FINAL step. When the operator selects a navigation option, the policy lifecycle engagement is complete. The output document at `{outputFile}` contains the complete, approved, published policy with enforcement mechanisms, exception management, and a maintenance plan. The frontmatter must reflect `policy_status: 'published'`, `lifecycle_report_complete: true`, and all 7 steps in the `stepsCompleted` array.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All 6 prior steps verified as complete before closure
- Policy document finalized with all sections complete and consistent
- Cross-reference validation passed (statements → requirements → enforcement → framework)
- Cross-framework control mapping validated in Appendix A
- Review schedule established with frequency, trigger events, and reviewer checklist
- Maintenance plan created with version control, update processes, and retirement/sunset process
- Policy lifecycle metrics compiled and presented to operator
- Engagement status updated with post-lifecycle action items
- Chronicle recommendation made for organizational memory
- Final frontmatter updated with all fields populated and consistent
- Final navigation options presented (A/W/N/C/R)
- Operator confirmed metrics accuracy and engagement closure

### SYSTEM FAILURE:

- Proceeding without verifying all 6 prior steps are complete
- Not finalizing the policy document (leaving sections incomplete or inconsistent)
- Not validating cross-framework mapping
- Not establishing a review schedule (assessment decay guarantee)
- Not creating a maintenance plan (orphan policy guarantee)
- Not compiling policy lifecycle metrics (institutional knowledge loss)
- Not recommending Chronicle for organizational memory
- Re-opening drafting, modifying requirements, or changing enforcement at this stage
- Not updating frontmatter to final state
- Not presenting final navigation options
- Presenting a [C] Continue option — this is the FINAL step

**Master Rule:** This step closes the loop on the entire policy lifecycle. A policy without a maintenance plan will decay into irrelevance. A policy without metrics cannot demonstrate program maturity. A policy without a review schedule will silently become outdated. The lifecycle report and maintenance plan are what give the policy longevity beyond this engagement. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
