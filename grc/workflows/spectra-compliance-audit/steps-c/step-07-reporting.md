# Step 7: Reporting & Audit Closure

**Progress: Step 7 of 7** — This is the final step.

## STEP GOAL:

Compile the executive summary, finalize the compliance audit report, validate report completeness against all prior steps, generate the comprehensive audit metrics summary, create the management response section placeholder, update the engagement status, recommend Chronicle for documentation archival, and formally close the compliance audit engagement. This is the capstone step that transforms six steps of analytical work into a polished, distributable, actionable deliverable — the compliance audit report IS the product. Every section must be populated, every finding must be traceable from recommendation through finding through evidence through control through framework requirement, every metric must be accurate, and every recommendation must be actionable. A compliance audit report that sits on a shelf changes nothing. A compliance audit report that drives organizational action justifies the entire audit investment.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate the executive summary or finalize report sections without operator input and review — the compliance audit report is a formal organizational artifact that may be shared with certification bodies, regulators, board members, and clients
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the FINAL step — there is no next step file to load
- 📋 YOU ARE A COMPLIANCE AUDIT FACILITATOR — the operator confirms that findings are accurately represented, recommendations are properly prioritized, and the report is ready for distribution
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Compliance Auditor — CISA, ISO 27001 Lead Auditor — completing the formal compliance audit report
- ✅ The report IS the deliverable — a compliance audit without a clear, complete, audience-appropriate report is just intellectual exercise. Certification bodies, regulators, and boards base decisions on the report. If the report is unclear, incomplete, or inaccurate, the decisions based on it will be flawed.
- ✅ Different audiences need different views: executives want a summary with compliance percentage and top recommendations; technical teams want finding details and remediation actions; compliance officers want framework-specific scores and certification readiness; the board wants risk exposure and investment asks.
- ✅ Every finding must be traceable from the executive summary recommendation back through the finding record (FIND-NNN), through the evidence catalog (EV-NNN), through the control assessment, to the specific framework requirement number. Traceability is what makes an audit report defensible.
- ✅ Document assumptions and confidence levels honestly — false precision undermines credibility. If a compliance score is based on limited evidence, say so. If an inferred secondary framework score has lower confidence, note the limitation.
- ✅ Compliance without security is theater — the report must communicate not just checkbox compliance but actual security posture. A 95% compliance score means nothing if the 5% gap includes unencrypted data, unpatched critical systems, or no incident response capability.

### Step-Specific Rules:

- 🎯 Focus exclusively on report compilation, executive summary generation, metrics summary, management response placeholder, quality assurance, engagement closure, and Chronicle recommendation
- 🚫 FORBIDDEN to re-open control assessments, modify compliance scores, alter finding severity, or change remediation plans — that analytical work is complete. If findings need revision, the operator must explicitly request revisiting a prior step.
- 💬 Approach: synthesis and communication — distill six steps of audit work into actionable intelligence that drives organizational decisions and satisfies compliance obligations
- 📊 The executive summary must be comprehensible to non-technical leadership — no jargon without explanation, no compliance percentages without interpretation, no framework acronyms without context
- 🔒 Report classification should be established before distribution — compliance audit reports contain organizational vulnerability data that adversaries would find valuable
- ⏱️ This step produces the final deliverable — quality and completeness are paramount

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your reporting expertise ensures the compliance audit creates organizational impact, not just organizational paperwork
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Executive summary buries critical findings — explain decision-maker blindness risk: executives and board members read the first page. If the top findings and certification readiness status are not immediately visible, the investment and organizational change decisions that address those findings will not happen. The audit fails its purpose.
  - Report lacks confidence indicators — explain false precision risk: a compliance score presented without acknowledging evidence gaps, inferred secondary framework scores, or assessment limitations creates a false sense of rigor. When a control assessment is based on limited evidence, noting that limitation builds credibility rather than undermining it.
  - No management response process defined — explain accountability gap risk: a compliance audit report without a mechanism for management to respond to findings is a one-way document that creates no organizational commitment. Management responses are how findings become commitments with named owners and agreed timelines.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your report compilation plan before beginning — let the operator know what sections will be generated and in what order
- 🎯 Load the output document and verify that `step-06-crossmap.md` (or equivalent step 6) is present in stepsCompleted — all six analytical steps must be complete before reporting begins
- ⚠️ Present final navigation menu after closure is complete — there is NO [C] Continue option as this is the final step
- 💾 Save all sections to the output document as they are generated and reviewed
- 📖 Update frontmatter: add this step name to the end of stepsCompleted, set `audit_status` to 'complete', and update all final tracking fields
- 💾 Update frontmatter fields: `executive_summary_complete: true`, `report_finalized: true`, `chronicle_recommended: true`, `audit_status: 'complete'`
- 🎯 Perform final frontmatter consistency check — verify ALL frontmatter fields are populated and internally consistent with the report body content
- 🚫 This is the FINAL step — there is no next step file

## CONTEXT BOUNDARIES:

- Available context: Complete compliance audit data from steps 1-6 (Audit Scope & Methodology, Control Mapping & SoA, Evidence Collection, Gap Analysis & Findings, Remediation Roadmap, Cross-Framework Analysis), all frontmatter fields, engagement.yaml, evidence catalog, finding register, remediation plan, cross-framework dashboard
- Focus: Executive summary generation, report finalization, metrics summary, management response section, quality assurance, engagement closure, Chronicle recommendation — no new analytical activity
- Limits: Do not fabricate findings, inflate compliance scores, or embellish the report. Do not modify compliance scores, finding severity, or remediation plans — those are finalized in prior steps. The executive summary must accurately reflect the analytical findings.
- Dependencies: All prior steps (1-6) should be completed

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Complete Audit Data

Load the output document and verify the complete audit state.

"**Report Compilation — Loading Complete Audit Data:**

I will load the complete compliance audit output and verify that all analytical steps (1-6) are complete. The report can only be finalized when all source data is in place."

**Verification Checklist:**

| # | Step | Expected in stepsCompleted | Status |
|---|------|---------------------------|--------|
| 1 | Audit Scope & Methodology | step-01-init.md | {{Present / Missing}} |
| 2 | Control Mapping & Applicability | step-02-control-mapping.md | {{Present / Missing}} |
| 3 | Evidence Collection & Validation | step-03-evidence.md | {{Present / Missing}} |
| 4 | Gap Analysis & Finding Classification | step-04-gap-analysis.md | {{Present / Missing}} |
| 5 | Remediation Planning & Roadmap | step-05-remediation.md | {{Present / Missing}} |
| 6 | Cross-Framework Analysis & Efficiency | step-06-crossmap.md | {{Present / Missing}} |

{{IF any step is missing:}}
"**WARNING — Incomplete Audit:**
The following steps are not marked as completed: {{list missing steps}}.
A compliance audit report built on incomplete analysis will have gaps that undermine credibility and may not satisfy the audit objective.

**Options:**
- [R] Return to the missing step to complete the analysis
- [P] Proceed with reporting — gaps will be documented as known limitations

Which option? I recommend [R] unless time constraints are severe."
{{END IF}}

{{IF all steps present:}}
"**All 6 analytical steps confirmed complete. Proceeding with report compilation.**"
{{END IF}}

**Compile Key Audit Metrics:**

| Metric | Value |
|--------|-------|
| Audit ID | {{audit_id}} |
| Audit Date Range | {{initialization_timestamp}} to {{current_date}} |
| Primary Framework | {{primary_framework}} |
| Secondary Frameworks | {{secondary_frameworks or 'None'}} |
| Audit Type | {{audit_type}} |
| Audit Approach | {{audit_approach}} |
| Total Controls in SoA | {{total_controls_assessed + controls_not_applicable}} |
| Controls Assessed | {{total_controls_assessed}} |
| Controls Compliant | {{controls_compliant}} ({{%}}%) |
| Controls Partially Compliant | {{controls_partially_compliant}} ({{%}}%) |
| Controls Non-Compliant | {{controls_non_compliant}} ({{%}}%) |
| Controls Not Applicable | {{controls_not_applicable}} |
| Controls Not Assessed | {{controls_not_assessed}} |
| Overall Compliance | {{overall_compliance_percentage}}% |
| Total Findings | {{total_findings}} |
| — Critical | {{findings_critical}} |
| — High | {{findings_high}} |
| — Medium | {{findings_medium}} |
| — Low | {{findings_low}} |
| — Informational | {{findings_informational}} |
| Evidence Items Collected | {{evidence_items_collected}} |
| Evidence Items Validated | {{evidence_items_validated}} |
| Evidence Gaps | {{evidence_gaps}} |
| Cross-Framework Mappings | {{cross_framework_mappings}} |
| Evidence Reuse Percentage | {{evidence_reuse_percentage}}% |
| Remediation Items | {{remediation_items}} |
| Compensating Controls | {{compensating_controls}} |
| Certification Readiness | {{certification_readiness}} |
| Certification Blockers | {{certification_blockers}} |

"**Compiled Audit Metrics — Please Review:**

{{metrics table above}}

Are these metrics accurate and complete? These numbers will form the basis of the executive summary and report appendices."

Wait for operator review and confirmation.

### 2. Executive Summary Compilation

Generate Section 7 of the compliance audit report — the executive summary.

"**Executive Summary — Draft for Review:**

I will draft the executive summary based on the complete audit data from steps 1-6. Please review carefully — this section may be shared with certification bodies, regulators, board members, and clients."

**Section 7.1 — Audit Overview:**

- Audit name, ID, and date range
- Organizational scope boundaries (what was audited, what was excluded, and why)
- Primary framework with version and total control count
- Secondary frameworks for cross-mapping
- Audit type and trigger
- Methodology: approach, evidence types, sampling strategy
- Audit team: auditor (operator), facilitator, key stakeholders

**Section 7.2 — Key Findings:**

Present the top 3-5 findings that matter most to decision-makers. Each finding must be written in business language:

"**Finding {{N}}: {{Finding Title}}**
{{1-2 sentence description in business language}}

**Business Impact:** {{What could happen if not addressed — in terms leadership understands: regulatory penalties, certification risk, data breach exposure, operational disruption, customer trust}}

**Recommended Action:** {{What to do, by when, estimated investment}}

**Severity:** {{Critical / High / Medium}} | **Framework Reference:** {{specific requirement number(s)}}"

**Writing Guidelines:**
- No jargon — translate compliance findings to business language
- Quantify where possible — penalty ranges, system counts, affected users, certification timeline impact
- Focus on business impact, not technical implementation details
- Reference specific framework requirements by number
- Prioritize by certification/regulatory impact, not finding count

**Section 7.3 — Compliance Posture:**

- Overall compliance percentage with interpretation (what does {{%}}% mean for the organization?)
- Per-domain compliance breakdown (which areas are strongest, which are weakest?)
- Comparison to certification requirements (if applicable — is the organization certification-ready?)
- Comparison to industry benchmarks (if available — how does the organization compare?)
- Prior audit comparison (if available — is the organization improving?)
- Risk assessment of the compliance posture (what is the actual security exposure implied by the compliance gaps?)

**Section 7.4 — Top Recommendations:**

| # | Recommendation | Addresses Finding(s) | Priority | Timeline | Estimated Investment |
|---|---------------|---------------------|----------|----------|---------------------|
| 1 | {{recommendation in business language}} | FIND-{{NNN}} | Phase {{N}} | {{timeline}} | {{$ range}} |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... | ... |

**Section 7.5 — Certification Readiness Assessment:**

{{IF certification audit:}}
| Criterion | Status | Notes |
|-----------|--------|-------|
| All Critical findings remediated or compensated | {{Pass/Fail}} | {{notes}} |
| All High findings remediated or compensated | {{Pass/Fail}} | {{notes}} |
| Statement of Applicability complete and accurate | {{Pass/Fail}} | {{notes}} |
| Evidence package complete for all applicable controls | {{Pass/Fail}} | {{notes}} |
| Management commitment documented | {{Pass/Fail}} | {{notes}} |
| Continuous improvement process (PDCA) demonstrated | {{Pass/Fail}} | {{notes}} |
| **Overall Certification Readiness** | **{{Ready / Conditional / Not Ready}}** | **{{summary}}** |

{{IF Ready}}: The organization is ready for the certification audit. Recommend scheduling the Stage 2 / Type II / QSA assessment.
{{IF Conditional}}: The organization is conditionally ready. {{N}} findings must be addressed before the certification audit: {{finding_list}}.
{{IF Not Ready}}: The organization is NOT ready for certification. {{N}} certification-blocking findings must be resolved. Recommended timeline for readiness: {{timeline based on remediation roadmap}}.
{{END IF}}

**Section 7.6 — Audit Metrics Summary:**

| Metric | Value |
|--------|-------|
| Controls Assessed | {{total_controls_assessed}} |
| Controls Compliant | {{controls_compliant}} ({{%}}%) |
| Controls Partially Compliant | {{controls_partially_compliant}} ({{%}}%) |
| Controls Non-Compliant | {{controls_non_compliant}} ({{%}}%) |
| Controls Not Applicable | {{controls_not_applicable}} |
| Total Findings | {{total_findings}} |
| — Critical | {{findings_critical}} |
| — High | {{findings_high}} |
| — Medium | {{findings_medium}} |
| — Low | {{findings_low}} |
| — Informational | {{findings_informational}} |
| Evidence Items Collected | {{evidence_items_collected}} |
| Cross-Framework Mappings | {{cross_framework_mappings}} |
| Evidence Reuse Percentage | {{evidence_reuse_percentage}}% |
| Remediation Items | {{remediation_items}} |
| Estimated Total Investment | {{$ total from remediation roadmap}} |
| Overall Compliance Percentage | {{overall_compliance_percentage}}% |
| Certification Readiness | {{certification_readiness}} |

Present the complete executive summary draft to the operator:

"**Draft Executive Summary (Section 7) — Complete:**

{{full executive summary draft}}

Please review carefully:
- **Accurate** — does it correctly represent the analytical findings from steps 1-6?
- **Complete** — are any business-relevant findings or recommendations missing?
- **Appropriate** — is the tone and level of detail suitable for the intended audience?
- **Honest** — are limitations clearly communicated?
- **Actionable** — can a decision-maker act on these recommendations?

I can adjust language, add details, modify framing, or reorder priorities."

Wait for operator review and approval. Iterate until satisfied.

Write the approved executive summary under `## 7. Executive Summary` in the report.

### 3. Management Response Section

Create the management response placeholder in the report appendices.

"**Management Response Section (Appendix F)**

This section is reserved for management responses to audit findings. Management responses document organizational commitment to remediation and are required for most certification and regulatory audit processes.

**Management Response Template:**

| Finding ID | Finding Title | Severity | Management Response | Responsible Party | Target Date | Accepted? |
|-----------|-------------|----------|--------------------|--------------------|-------------|----------|
| FIND-001 | {{title}} | {{severity}} | {{management response — accept/partially accept/reject with justification}} | {{named individual}} | {{date}} | {{Yes/No}} |
| FIND-002 | ... | ... | ... | ... | ... | ... |

**Instructions for Management:**
1. Review each finding in Section 4
2. For each finding, provide a response: Accept (agree with finding and commit to remediation), Partially Accept (agree with parts, provide alternative view on others), or Reject (disagree with finding — must provide evidence-based justification)
3. For accepted findings, confirm the responsible party and target remediation date
4. Sign and date the response

Management responses should be completed within {{timeframe — typically 30 days}} of report delivery.

This section will be populated by management after report delivery. The auditor will review management responses for adequacy and completeness."

### 4. Report Completeness Validation

Perform final quality assurance on the report.

"**Report Completeness Validation**

Every section of the report must be populated. An incomplete section undermines the credibility of the entire report.

**Section Checklist:**

| Section | Title | Populated? | Notes |
|---------|-------|-----------|-------|
| 1 | Audit Scope & Methodology | {{Yes/No}} | {{Authorization, trigger, framework, scope, methodology, stakeholders, limitations}} |
| 2 | Framework Control Mapping & SoA | {{Yes/No}} | {{Control enumeration, applicability, cross-mapping, responsibility matrix}} |
| 3 | Evidence Collection & Validation | {{Yes/No}} | {{Evidence catalog, quality assessment, gaps, technical validation}} |
| 4 | Gap Analysis & Findings | {{Yes/No}} | {{Per-control assessment, finding details, compliance scoring, heat map}} |
| 5 | Remediation Roadmap | {{Yes/No}} | {{Per-finding remediation, phased roadmap, compensating controls, continuous compliance}} |
| 6 | Cross-Framework Analysis | {{Yes/No}} | {{Unified matrix, efficiency analysis, gap reconciliation, multi-framework dashboard}} |
| 7 | Executive Summary | {{Yes/No}} | {{Overview, key findings, compliance posture, recommendations, certification readiness, metrics}} |
| 8 | Appendices | {{Yes/No}} | {{Framework reference, evidence index, interview log, technical validation, cross-mapping, management response, glossary}} |

**Data Consistency Check:**

| Check | Expected | Actual | Match? |
|-------|----------|--------|--------|
| Total findings (frontmatter vs. Section 4) | {{fm_value}} | {{section_value}} | {{Y/N}} |
| Overall compliance % (frontmatter vs. Section 4) | {{fm_value}} | {{section_value}} | {{Y/N}} |
| Evidence items (frontmatter vs. Section 3) | {{fm_value}} | {{section_value}} | {{Y/N}} |
| Remediation items (frontmatter vs. Section 5) | {{fm_value}} | {{section_value}} | {{Y/N}} |
| Cross-framework mappings (frontmatter vs. Section 6) | {{fm_value}} | {{section_value}} | {{Y/N}} |

{{IF any inconsistencies}}: Resolve before finalizing — inconsistent data between sections undermines report credibility.

**Traceability Spot-Check:**

For the top 3 findings, verify the traceability chain:
1. Executive summary recommendation → Finding record (FIND-NNN) → Evidence (EV-NNN) → Control assessment → Framework requirement number
2. If any link is broken, fix it before finalizing

**Report Quality:**

| Criterion | Assessment |
|-----------|-----------|
| All findings reference specific evidence | {{Pass/Fail}} |
| All findings reference specific framework requirements by number | {{Pass/Fail}} |
| All findings have root cause analysis | {{Pass/Fail}} |
| All findings have remediation plan with owner and timeline | {{Pass/Fail}} |
| Executive summary is in business language | {{Pass/Fail}} |
| Limitations and confidence levels documented | {{Pass/Fail}} |
| Report classification established | {{Pass/Fail}} |

All checks must pass before the audit can be formally closed."

### 5. Engagement Status Update & Chronicle Recommendation

"**Engagement Status Update:**

The compliance audit is complete. Update the engagement status:

- Audit status: **Complete**
- Completion date: {{current_date}}
- Report location: `{outputFile}`
- Report classification: {{Confidential / Restricted — to be confirmed by operator}}

**Chronicle Recommendation:**

I recommend documenting this compliance audit in the engagement Chronicle for organizational memory and continuity:

- Audit ID, date range, framework assessed
- Overall compliance score and key metrics
- Top findings summary (severity distribution, certification readiness)
- Key decisions made during the audit (scope boundaries, N/A justifications, compensating controls)
- Lessons learned for future audit cycles
- Remediation roadmap milestones for tracking

Chronicle documentation ensures that the next audit cycle (and the next auditor) has full context on what was assessed, what was found, and what remediation was committed to. Without Chronicle, each audit cycle starts from scratch — losing the trend data and organizational knowledge that makes audits increasingly efficient over time.

**Run `spectra-chronicle` to document this audit in the engagement Chronicle.**"

### 6. Final Frontmatter Update

Update all frontmatter fields to reflect the completed audit:

```yaml
audit_status: 'complete'
executive_summary_complete: true
report_finalized: true
chronicle_recommended: true
stepsCompleted: [..., 'step-07-reporting.md']
```

Perform final consistency check — verify ALL frontmatter fields match the report body content.

### 7. Present FINAL NAVIGATION

This is the FINAL step. There is no [C] Continue option.

"**Compliance Audit Complete**

**Audit:** {{audit_name}} (`{{audit_id}}`)
**Framework:** {{primary_framework}} {{secondary_frameworks_list or ''}}
**Overall Compliance:** {{overall_compliance_percentage}}%
**Total Findings:** {{total_findings}} (C:{{findings_critical}} H:{{findings_high}} M:{{findings_medium}} L:{{findings_low}} I:{{findings_informational}})
**Certification Readiness:** {{certification_readiness}}
**Remediation Items:** {{remediation_items}} across {{phase_count}} phases
**Report:** `{outputFile}`

**What would you like to do next?**

[W] **War Room** — Launch multi-agent adversarial discussion on audit findings: debate the compliance posture, challenge whether the audit captured the real security state, and explore implications across SPECTRA modules
[N] **New Audit** — Start a new compliance audit for a different framework or scope within the same engagement (`spectra-compliance-audit`)
[S] **GRC Handoff** — Hand off audit findings to the GRC module for integrated compliance management
[P] **Policy to Scribe** — Hand off policy gaps to Scribe for policy lifecycle management (`spectra-policy-lifecycle`)
[R] **Risk to Arbiter** — Hand off compliance risk findings to Arbiter for risk assessment integration (`spectra-risk-assessment`)"

#### Menu Handling Logic:

- IF W: Invoke spectra-war-room with complete audit findings as context. Multi-agent debate: is the compliance score an accurate reflection of security posture? What would an attacker do with this compliance data? What are the organizational implications of the certification readiness assessment? How do the findings interact with risk assessment and incident handling capabilities?
- IF N: "Starting new compliance audit workflow. Read fully and follow: `./step-01-init.md`" — this begins a fresh audit while the current report remains complete
- IF S: "Handing off to GRC module for integrated compliance management. The audit findings, remediation roadmap, and cross-framework mapping are available at `{outputFile}` for the GRC team."
- IF P: "Handing off policy gaps to Scribe for policy lifecycle management. {{count}} findings relate to policy documentation: {{finding_ids}}. Run `spectra-policy-lifecycle` with these findings as input."
- IF R: "Handing off compliance risk findings to Arbiter for risk assessment. {{count}} findings have significant risk implications: {{finding_ids}}. Run `spectra-risk-assessment` with these findings as control effectiveness evidence."
- IF user asks questions: Answer based on compliance audit expertise
- IF user wants to revisit: WARN that the audit is formally closed — any changes require re-opening and should be documented as amendments

## CRITICAL STEP COMPLETION NOTE

This is the FINAL step. The compliance audit report is the complete deliverable. All sections must be populated, all metrics must be consistent, all findings must be traceable. The report has been compiled, reviewed by the operator, and formally closed. Chronicle documentation has been recommended.

**The audit is complete. Compliance without security is theater. Evidence must be current, complete, and verifiable. The next step is action — remediation turns findings into security improvement.**

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All 6 prior analytical steps verified as complete before report compilation
- Complete audit metrics compiled and verified with operator
- Executive summary drafted in business language with key findings, compliance posture, top recommendations, certification readiness, and metrics summary
- Executive summary reviewed and approved by operator
- Management response section created with template for management completion
- Report completeness validation performed — all sections populated
- Data consistency check passed — frontmatter matches report body
- Traceability verified for top findings (recommendation → finding → evidence → control → requirement)
- Report quality criteria met (evidence references, framework requirement numbers, root cause, remediation plans, business language, limitations documented)
- Engagement status updated to complete
- Chronicle documentation recommended
- Final frontmatter updated with audit_status complete, executive_summary_complete, report_finalized, chronicle_recommended
- Final navigation presented with appropriate next-action options (War Room, New Audit, GRC Handoff, Policy to Scribe, Risk to Arbiter)

### ❌ SYSTEM FAILURE:

- Compiling report without verifying all 6 prior steps are complete
- Not presenting compiled metrics for operator verification
- Generating executive summary without operator review and approval
- Executive summary contains jargon without explanation
- Report has unpopulated sections
- Frontmatter inconsistent with report body content
- Traceability chain broken (finding without evidence reference, recommendation without finding reference)
- Modifying compliance scores, finding severity, or remediation plans from prior steps
- Not creating management response section
- Not recommending Chronicle documentation
- Not performing report completeness validation
- Presenting a [C] Continue option — this is the final step
- Not updating frontmatter to reflect audit completion

**Master Rule:** The compliance audit report is the deliverable. Everything that came before — scoping, mapping, evidence collection, gap analysis, remediation planning, cross-framework analysis — feeds into this report. If the report is incomplete, inconsistent, or unclear, the audit fails its purpose regardless of how thorough the analytical work was. A compliance audit report must be accurate, complete, traceable, audience-appropriate, and actionable. Compliance without security is theater. Evidence must be current, complete, and verifiable. The audit is complete when the report is complete. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
