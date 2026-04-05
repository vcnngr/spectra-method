# Step 6: Cross-Framework Analysis & Efficiency

**Progress: Step 6 of 7** — Next: Reporting & Audit Closure

## STEP GOAL:

Perform comprehensive cross-framework analysis using the control mappings established in Step 2 combined with the compliance assessments from Step 4, build a unified control matrix that consolidates overlapping controls across all assessed frameworks, calculate efficiency metrics (overlap percentage, evidence reuse percentage, effort reduction), reconcile gaps across frameworks identifying framework-unique controls and conflicting requirements, generate a multi-framework compliance dashboard showing per-framework compliance scores and a unified organizational compliance posture, and produce a heat map visualizing compliance across all frameworks. This step transforms individual framework assessments into a holistic view of the organization's compliance posture — the efficiency gains from cross-framework mapping are what make multi-framework compliance manageable rather than multiplicative.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate cross-framework mappings without reference to the actual control mapping from Step 2 — cross-framework analysis must be grounded in the established mappings, not generated from scratch
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read — "read fully and follow"
- 📋 YOU ARE A COMPLIANCE AUDIT FACILITATOR — you perform the cross-framework analysis, the operator confirms that the efficiency opportunities and conflicting requirements are accurately identified
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Compliance Auditor — CISA, ISO 27001 Lead Auditor — with cross-framework expertise spanning ISO 27001, SOC 2, PCI DSS, HIPAA, GDPR, NIST CSF, NIST 800-53, and CIS Controls
- ✅ Cross-framework mapping is not academic — it is the efficiency engine that reduces organizational compliance burden. Without it, every framework is a separate audit with separate evidence collection, separate assessments, and separate remediation tracks.
- ✅ Framework conflicts exist — PCI DSS requires specific encryption standards, GDPR requires data minimization, HIPAA has specific retention requirements, and ISO 27001 is risk-based rather than prescriptive. Identifying where frameworks conflict is as important as identifying where they overlap.
- ✅ The unified control matrix is the primary deliverable of this step — it consolidates N frameworks worth of controls into a single operational view that the organization can manage as one compliance program rather than N separate programs
- ✅ Evidence reuse is the biggest efficiency gain — quantify it. If 150 evidence items were collected for ISO 27001, and 80% of those also satisfy SOC 2 controls, the organization saved 120 evidence collection activities

### Step-Specific Rules:

- 🎯 Focus exclusively on cross-framework analysis, unified control matrix, efficiency metrics, gap reconciliation, multi-framework dashboard, and compliance heat map
- 🚫 FORBIDDEN to modify individual control assessments from Step 4 — the per-framework compliance status is finalized. This step ANALYZES the cross-framework implications, it does not reassess.
- 🚫 FORBIDDEN to modify the remediation roadmap from Step 5 — remediation planning is complete. This step may IDENTIFY additional remediation opportunities from cross-framework gaps, but does not modify existing plans.
- 🚫 FORBIDDEN to write the executive summary — that is step 07
- 💬 Approach: analytical synthesis — combine individual framework assessments into a holistic compliance view
- 📊 If only one framework was assessed (no secondary frameworks), this step is abbreviated — produce a single-framework compliance dashboard and note that cross-framework analysis is not applicable

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your cross-framework expertise identifies efficiency opportunities that reduce organizational compliance burden
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Conflicting framework requirements not resolved — explain compliance collision risk: when two frameworks have conflicting requirements for the same control domain (e.g., PCI DSS mandates specific encryption algorithms while GDPR focuses on "appropriate" encryption without prescribing algorithms), the organization must choose which requirement to prioritize. Ignoring the conflict means one framework's requirements are met while the other's are not. Document the conflict and the resolution decision.
  - Evidence reuse assumed without validation — explain mapping accuracy risk: not all cross-framework control mappings are exact equivalences. ISO 27001 A.5.15 (Access control) and PCI DSS 7.2 (Access control) address similar concepts but have different evidence requirements. ISO 27001 requires a risk-based access control policy; PCI DSS requires specific access control configurations for cardholder data. Evidence that satisfies one may not fully satisfy the other without supplementation.
  - Single-framework assessment presented as multi-framework compliance — explain false coverage risk: an ISO 27001 audit does not automatically satisfy SOC 2, PCI DSS, or HIPAA requirements. Cross-framework mapping identifies areas of overlap but also identifies gaps where additional assessment is needed. Do not claim multi-framework compliance based on a single-framework audit.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Load output document and verify `step-05-remediation.md` in `stepsCompleted`
- 🎯 Load all data from steps 2 and 4: cross-framework mapping (step 02), per-control compliance assessments (step 04), finding register (step 04), evidence catalog (step 03)
- ⚠️ If no secondary frameworks were selected — produce abbreviated output (single-framework dashboard only) and note that cross-framework analysis is not applicable
- ⚠️ Present [A]/[W]/[C] menu after cross-framework analysis is complete
- 💾 ONLY save to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of `stepsCompleted` and updating:
  - `crossmap_complete: true`
  - `evidence_reuse_percentage`: calculated from actual evidence reuse
  - `cross_framework_mappings`: confirmed count from detailed mapping
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Complete data from steps 1-5: audit scope, framework selection, cross-framework control mapping (step 02), evidence catalog with cross-framework references (step 03), per-control compliance assessments (step 04), finding register (step 04), remediation roadmap (step 05)
- Focus: Unified control matrix, efficiency metrics, gap reconciliation, multi-framework dashboard, compliance heat map
- Limits: Do NOT modify individual control assessments (step 04). Do NOT modify remediation roadmap (step 05). Do NOT write executive summary (step 07). Analyze cross-framework implications only.
- Dependencies: Cross-framework mapping from step 02, compliance assessments from step 04

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Cross-Framework Data

Load the output document and verify step-05 is complete. Extract cross-framework mapping from step 02 and compliance assessments from step 04.

**Single-Framework Check:**

If no secondary frameworks were selected in Step 1:

"**Cross-Framework Analysis: Single Framework Only**

This audit assessed only {{primary_framework}} with no secondary frameworks for cross-mapping. Cross-framework analysis is not applicable.

I will generate a single-framework compliance dashboard and proceed to the reporting step.

**{{primary_framework}} Compliance Dashboard:**

| Domain/Theme | Total | Compliant | Partial | Non-Compliant | N/A | Not Assessed | Score |
|-------------|-------|-----------|---------|---------------|-----|-------------|-------|
| {{domain}} | {{t}} | {{c}} | {{p}} | {{nc}} | {{na}} | {{nas}} | {{%}}% |
| **Overall** | **{{t}}** | **{{c}}** | **{{p}}** | **{{nc}}** | **{{na}}** | **{{nas}}** | **{{%}}%** |

The full compliance analysis is already documented in Step 4. Proceeding to the reporting step for final report compilation.

**Single-Framework Improvement Recommendations:**

Even without cross-framework mapping, consider the following efficiency recommendations:

| # | Recommendation | Benefit |
|---|---------------|---------|
| 1 | Map primary framework controls to NIST CSF 2.0 as a maturity overlay | Provides a maturity-based view of the compliance posture for executive communication |
| 2 | Map primary framework controls to CIS Controls v8 for prioritized implementation | CIS Implementation Groups provide a practical roadmap for remediation prioritization |
| 3 | Consider adding secondary frameworks in the next audit cycle | Cross-framework mapping reduces the incremental effort of additional frameworks by 30-60% |
| 4 | Document the single-framework assessment as a baseline for future cross-mapping | The current assessment provides evidence artifacts that can be reused when secondary frameworks are added |

These are recommendations for future audit cycles — they do not affect the current audit."

Skip to section 7 (MENU OPTIONS) for single-framework audits.

**Multi-Framework Check:**

"**Cross-Framework Analysis — Loading Data:**

I will load the cross-framework control mapping from Step 2 and the per-control compliance assessments from Step 4 to build the unified control matrix and efficiency analysis."

**Present Cross-Framework Context:**

```
CROSS-FRAMEWORK ANALYSIS CONTEXT
Primary Framework: {{primary_framework}} — {{applicable_controls}} controls assessed
Secondary Frameworks: {{secondary_frameworks_list}}
Cross-Framework Mappings: {{mapping_count}} established in Step 2
Evidence Items: {{evidence_items_collected}} with cross-framework references
Findings: {{total_findings}} classified in Step 4
```

### 2. Unified Control Matrix

Build the unified control matrix that consolidates controls across all assessed frameworks.

"**Unified Control Matrix**

The unified control matrix maps every applicable control from the primary framework to its equivalent(s) in secondary frameworks. This creates a single operational view of the organization's compliance obligations.

**Matrix Structure:**

| Unified Control Area | Description | {{Primary Framework}} | Status | {{Secondary 1}} | Mapping | {{Secondary 2}} | Mapping | Evidence Reuse |
|---------------------|-------------|----------------------|--------|-----------------|---------|-----------------|---------|---------------|
| Access Control — Policy | Define and enforce access control policy | {{primary_id}} | {{status}} | {{sec1_id}} | {{Direct/Partial/Unique}} | {{sec2_id}} | {{Direct/Partial/Unique}} | {{EV-ids}} |
| Access Control — Provisioning | User provisioning and deprovisioning | {{primary_id}} | {{status}} | {{sec1_id}} | {{Direct/Partial/Unique}} | {{sec2_id}} | {{Direct/Partial/Unique}} | {{EV-ids}} |
| Access Control — Reviews | Periodic access reviews | {{primary_id}} | {{status}} | {{sec1_id}} | {{Direct/Partial/Unique}} | {{sec2_id}} | {{Direct/Partial/Unique}} | {{EV-ids}} |
| Access Control — Privileged | Privileged access management | {{primary_id}} | {{status}} | {{sec1_id}} | {{Direct/Partial/Unique}} | {{sec2_id}} | {{Direct/Partial/Unique}} | {{EV-ids}} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Unified Control Area Categories:**

| Category | Control Areas | Primary Controls | Secondary Controls |
|----------|-------------|-----------------|-------------------|
| Governance & Risk | Risk management, compliance, management commitment | {{count}} | {{count}} |
| Access Control | Identity, authentication, authorization, access reviews | {{count}} | {{count}} |
| Change Management | Change control, configuration management, release management | {{count}} | {{count}} |
| Incident Management | Detection, response, recovery, lessons learned | {{count}} | {{count}} |
| Data Protection | Classification, encryption, retention, disposal | {{count}} | {{count}} |
| People Security | Background checks, awareness, training, competency | {{count}} | {{count}} |
| Physical Security | Data center, media, environmental controls | {{count}} | {{count}} |
| Operations Security | Monitoring, logging, vulnerability management, backup | {{count}} | {{count}} |
| Third-Party Management | Vendor assessment, supply chain, cloud provider | {{count}} | {{count}} |
| Business Continuity | BCP, DR, testing, recovery | {{count}} | {{count}} |
| Compliance & Audit | Legal requirements, independent review, compliance monitoring | {{count}} | {{count}} |

The unified matrix consolidates {{total_primary}} primary controls and {{total_secondary}} secondary controls into {{unified_count}} unified control areas."

### 3. Efficiency Analysis

Calculate the efficiency gains from cross-framework mapping.

"**Cross-Framework Efficiency Analysis**

**Overlap & Deduplication:**

| Metric | Value |
|--------|-------|
| Total controls across ALL frameworks (raw) | {{total_raw}} |
| Unique controls (after deduplication via mapping) | {{unique}} |
| Overlap percentage | {{(total_raw - unique) / total_raw × 100}}% |
| Duplicate controls eliminated | {{total_raw - unique}} |

**Evidence Reuse:**

| Metric | Value |
|--------|-------|
| Total evidence items collected | {{evidence_items_collected}} |
| Evidence items mapped to multiple frameworks | {{multi_framework_evidence}} |
| Evidence items used by only one framework | {{single_framework_evidence}} |
| Evidence reuse percentage | {{multi / total × 100}}% |
| Equivalent evidence items saved via reuse | {{saved_count}} |
| Estimated effort reduction (evidence collection) | {{%}} |

**Assessment Effort Reduction:**

| Metric | Value |
|--------|-------|
| Controls assessed (primary) | {{primary_count}} |
| Equivalent secondary controls satisfied via mapping | {{satisfied_count}} |
| Additional secondary controls requiring unique assessment | {{unique_secondary}} |
| Effort saved via cross-framework mapping | {{%}} |

**Without Cross-Framework Mapping (Hypothetical):**

| Framework | Controls | Evidence Required | Assessment Effort |
|-----------|---------|-------------------|-------------------|
| {{primary}} | {{count}} | {{estimate}} | {{estimate}} |
| {{secondary_1}} | {{count}} | {{estimate}} | {{estimate}} |
| {{secondary_2}} | {{count}} | {{estimate}} | {{estimate}} |
| **Total (independent)** | **{{total}}** | **{{total_estimate}}** | **{{total_effort}}** |

**With Cross-Framework Mapping (Actual):**

| Metric | Independent | With Mapping | Savings |
|--------|------------|-------------|---------|
| Controls assessed | {{independent}} | {{actual}} | {{saved}} ({{%}}) |
| Evidence items | {{independent}} | {{actual}} | {{saved}} ({{%}}) |
| Assessment effort | {{independent}} | {{actual}} | {{saved}} ({{%}}) |

**Efficiency Recommendation:**

Based on the cross-framework analysis, the organization can manage its compliance obligations as {{unified_count}} unified control areas instead of {{total_raw}} separate framework controls. This reduces ongoing compliance management effort by approximately {{%}}%.

**Efficiency Breakdown by Control Area:**

| Unified Control Area | Primary Controls | Secondary Controls (Mapped) | Evidence Items (Collected Once) | Effort Saved |
|---------------------|-----------------|---------------------------|-------------------------------|-------------|
| Access Control | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Change Management | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Incident Management | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Data Protection | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Governance & Risk | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| People Security | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Operations Security | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Third-Party Management | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Business Continuity | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Physical Security | {{count}} | {{count}} | {{count}} | {{hours/days}} |
| Compliance & Audit | {{count}} | {{count}} | {{count}} | {{hours/days}} |

Control areas with the highest evidence reuse are the highest-efficiency areas — these are where the cross-framework mapping pays for itself."

### 4. Gap Reconciliation

Identify framework-unique controls and conflicting requirements.

"**Gap Reconciliation — Cross-Framework**

**Framework-Unique Controls:**

Controls that exist in one framework with no equivalent in the others require independent assessment and evidence.

| Framework | Unique Control ID | Control Title | Status | Why Unique |
|-----------|------------------|--------------|--------|-----------|
| {{framework}} | {{control_id}} | {{title}} | {{status from assessment}} | {{explanation — e.g., "PCI DSS data retention rules have no ISO 27001 equivalent"}} |

**Unique Control Summary:**

| Framework | Total Applicable | Mapped to Other Framework(s) | Unique (No Mapping) | Unique % |
|-----------|-----------------|-----------------------------|--------------------|---------|
| {{framework}} | {{total}} | {{mapped}} | {{unique}} | {{%}} |

**Conflicting Requirements:**

Where frameworks have conflicting or inconsistent requirements for the same control area:

| Control Area | Framework A Requirement | Framework B Requirement | Conflict Type | Resolution |
|-------------|------------------------|------------------------|--------------|-----------|
| {{area}} | {{requirement_A}} | {{requirement_B}} | {{Prescriptive vs. Risk-based / Stricter vs. Lenient / Contradictory}} | {{how the organization resolves — typically implement the stricter requirement}} |

**Common Conflict Areas:**

| Conflict Area | Frameworks | Nature of Conflict |
|-------------|-----------|-------------------|
| Encryption standards | PCI DSS (specific algorithms) vs. GDPR ("appropriate") vs. ISO 27001 (risk-based) | PCI DSS is most prescriptive — implementing PCI DSS standards generally satisfies others |
| Data retention | GDPR (minimize) vs. HIPAA (6 years) vs. PCI DSS (1 year) vs. SOX (7 years) | Retention schedule must address each framework's minimum and maximum |
| Incident notification | GDPR (72 hours) vs. HIPAA (60 days) vs. NIS2 (24 hours initial) | Implement the shortest timeline to satisfy all |
| Risk assessment | NIST 800-53 (annual) vs. ISO 27001 (when significant changes) vs. PCI DSS (annual) | Annual minimum with trigger-based reassessment satisfies all |
| Access reviews | SOC 2 (period of audit) vs. ISO 27001 (at defined intervals) vs. PCI DSS (every 6 months) | Every 6 months satisfies all |

Any conflicting requirements that need resolution? The general principle is to implement the strictest requirement, which satisfies all frameworks simultaneously."

### 5. Multi-Framework Compliance Dashboard

Generate the multi-framework compliance dashboard.

"**Multi-Framework Compliance Dashboard**

**Per-Framework Compliance:**

| Framework | Total Controls | Compliant | Partial | Non-Compliant | N/A | Not Assessed | Compliance % |
|-----------|---------------|-----------|---------|---------------|-----|-------------|-------------|
| {{primary}} | {{total}} | {{c}} | {{p}} | {{nc}} | {{na}} | {{nas}} | {{%}}% |
| {{secondary_1}} (inferred) | {{total}} | {{c}} | {{p}} | {{nc}} | {{na}} | {{nas}} | {{%}}% |
| {{secondary_2}} (inferred) | {{total}} | {{c}} | {{p}} | {{nc}} | {{na}} | {{nas}} | {{%}}% |

**Note on Secondary Framework Scores:**
Secondary framework compliance is INFERRED from the primary framework assessment via cross-framework mapping. Controls with direct mapping inherit the primary assessment. Controls with partial mapping receive a reduced confidence assessment. Framework-unique controls may require independent assessment for a definitive score.

**Unified Compliance Posture:**

| Metric | Value |
|--------|-------|
| Unified control areas | {{count}} |
| Compliant (all mapped controls) | {{count}} ({{%}}%) |
| Partial (at least one mapped control partial) | {{count}} ({{%}}%) |
| Non-compliant (at least one mapped control non-compliant) | {{count}} ({{%}}%) |
| Unified compliance percentage | {{%}}% |

**Compliance Heat Map — All Frameworks:**

```
MULTI-FRAMEWORK COMPLIANCE HEAT MAP
Legend: ██ Compliant  ▓▓ Partial  ░░ Non-Compliant  ·· N/A  ?? Not Assessed

{{primary_framework}}:
  {{domain_1}} ({{score}}%): ██ ██ ▓▓ ░░ ██ ██ ██ ▓▓ ██
  {{domain_2}} ({{score}}%): ██ ██ ██ ██ ██ ██ ·· ██ ██
  {{domain_3}} ({{score}}%): ▓▓ ░░ ██ ██ ██ ▓▓ ██ ░░ ██

{{secondary_1}} (inferred):
  {{domain_1}} ({{score}}%): ██ ██ ▓▓ ░░ ██ ██
  {{domain_2}} ({{score}}%): ██ ██ ██ ██ ██ ██
  {{domain_3}} ({{score}}%): ▓▓ ░░ ██ ██ ??

{{secondary_2}} (inferred):
  {{domain_1}} ({{score}}%): ██ ▓▓ ██ ██ ██
  {{domain_2}} ({{score}}%): ██ ██ ░░ ██ ██
```

Each block represents one control within the domain. Red areas indicate compliance gaps that affect multiple frameworks — these are the highest-priority remediation targets because one fix improves compliance across all mapped frameworks."

### 6. Efficiency Recommendations

Provide recommendations for ongoing multi-framework compliance management.

"**Cross-Framework Efficiency Recommendations**

Based on the analysis, the following recommendations optimize ongoing compliance management:

| # | Recommendation | Impact | Effort |
|---|---------------|--------|--------|
| 1 | Adopt unified control framework (use the unified matrix as the operational compliance control set) | Reduces ongoing management from {{N}} framework tracks to 1 unified track | Medium — requires GRC platform configuration |
| 2 | Implement evidence-once-use-many collection process | Reduces evidence collection effort by {{%}}% | Low — process change, no tooling |
| 3 | Consolidate audit schedules (single audit covers multiple frameworks) | Reduces audit frequency and disruption | Medium — requires auditor coordination |
| 4 | Address framework-unique controls in dedicated mini-audits | Ensures unique requirements are not missed | Low — focused assessment |
| 5 | Resolve conflicting requirements once and document the resolution | Eliminates recurring conflict resolution | Low — one-time decision documentation |
| 6 | Use the unified control matrix as the basis for GRC platform configuration | Enables automated cross-framework reporting | Medium — GRC platform setup |

**Estimated Annual Compliance Effort Reduction:** {{%}}% (based on evidence reuse and unified management approach)

These recommendations apply to the ongoing compliance program, not just this audit cycle."

### 7. Present MENU OPTIONS

Display menu after cross-framework analysis summary:

"**Select an option:**
[A] Advanced Elicitation — Push deeper on cross-framework mapping accuracy, challenge efficiency calculations, probe conflicting requirement resolutions, and stress-test the unified control matrix against each framework's specific requirements
[W] War Room — Launch multi-agent adversarial discussion on cross-framework compliance: challenge whether inferred secondary scores are reliable, whether the efficiency gains are realistic, whether the unified control matrix captures all unique requirements, and whether the conflicting requirement resolutions satisfy each framework independently
[C] Continue — Save and proceed to Step 7: Reporting & Audit Closure (FINAL STEP — Step 7 of 7)"

#### Menu Handling Logic:

- IF A: Invoke advanced elicitation on cross-framework analysis. Challenge mapping accuracy (are partial mappings actually equivalent?), probe efficiency calculations (are the effort reduction numbers realistic?), test conflicting requirement resolutions (does implementing the stricter requirement truly satisfy the lenient one?). Process insights, ask operator if they accept adjustments, if yes update analysis then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke spectra-war-room with cross-framework analysis as context. Auditor perspective: would each framework's certification body accept the inferred scores? Are the unique controls adequately covered? Red perspective: does the unified matrix create blind spots where framework-specific requirements are lost? Blue perspective: can the organization operationalize the unified control matrix? Summarize insights, ask operator if they want to adjust anything, redisplay menu
- IF C: Update output file frontmatter adding `step-06-crossmap.md` to the end of `stepsCompleted` array and updating `crossmap_complete`, `evidence_reuse_percentage`, `cross_framework_mappings` fields, then read fully and follow: `./step-07-reporting.md`
- IF user provides additional context: Validate, adjust analysis, redisplay menu
- IF user asks questions: Answer based on cross-framework expertise and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, crossmap_complete set to true, evidence_reuse_percentage calculated, cross_framework_mappings confirmed, and Section 6 (Cross-Framework Analysis) fully populated with unified control matrix, efficiency analysis, gap reconciliation, multi-framework dashboard, and compliance heat map], will you then read fully and follow: `./step-07-reporting.md` to begin executive reporting and audit closure.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Cross-framework mapping data loaded from Steps 2 and 4
- Single-framework audits handled with abbreviated output (dashboard only)
- Unified control matrix built consolidating all frameworks into unified control areas
- Efficiency analysis calculated with overlap, evidence reuse, and effort reduction metrics
- Gap reconciliation completed — framework-unique controls identified, conflicting requirements documented with resolutions
- Multi-framework compliance dashboard generated with per-framework and unified scores
- Compliance heat map generated for all frameworks
- Efficiency recommendations provided for ongoing compliance management
- Frontmatter updated with crossmap completion, evidence reuse percentage, and mapping count

### ❌ SYSTEM FAILURE:

- Modifying individual control assessments from Step 4
- Modifying the remediation roadmap from Step 5
- Writing executive summary content (step 07)
- Generating cross-framework mappings from scratch instead of using Step 2 mappings
- Claiming multi-framework compliance without acknowledging inferred scores and unique controls
- Not identifying conflicting requirements between frameworks
- Not calculating efficiency metrics
- Not producing the multi-framework dashboard
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with crossmap completion status

**Master Rule:** Cross-framework analysis transforms separate compliance silos into a unified compliance program. Without this analysis, organizations managing multiple frameworks duplicate effort, miss conflicting requirements, and cannot quantify the efficiency of cross-framework management. The unified control matrix is not just an audit artifact — it is the blueprint for an efficient, sustainable compliance program. Get the mappings right, quantify the efficiency, resolve the conflicts. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
