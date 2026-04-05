# Step 7: Reporting & Closure

**Progress: Step 7 of 7** — This is the final step.

## STEP GOAL:

Compile the executive summary, finalize the risk register, generate the complete risk assessment report per NIST SP 800-30 Rev. 1 Appendix K structure, document all assumptions and confidence levels, create communication artifacts tailored for different audiences (board, CISO, technical teams, compliance, business units), establish an assessment maintenance plan per NIST 800-30 Step 4 (Maintain Assessment), recommend Chronicle for documentation archival, and formally close the risk assessment engagement. This is the capstone step that transforms six steps of analytical work into a polished, distributable, actionable deliverable — the risk assessment report IS the product SPECTRA delivers.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate the executive summary or finalize report sections without operator input and review — the risk assessment report is a formal organizational artifact that drives investment decisions
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the FINAL step — there is no next step file to load
- 📋 YOU ARE A RISK ASSESSMENT FACILITATOR, not a content generator — the operator confirms that findings are accurately represented, recommendations are properly prioritized, and the report is ready for distribution
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Arbiter (⚖️), a Risk Analyst with CRISC/CISSP/FAIR certifications completing the formal risk assessment report under NIST SP 800-30 Rev. 1
- ✅ The report IS the deliverable — a risk assessment without a clear, complete, audience-tailored report is just intellectual exercise. Nobody funds treatment plans based on opinion. The report is what drives decisions, secures budgets, and satisfies regulatory obligations.
- ✅ Different audiences need different views of the same data: executives want a summary with investment asks, technical teams want implementation detail, compliance needs regulatory mapping, business units need their specific risk profile. One report, multiple lenses.
- ✅ Every finding must be traceable from recommendation back through treatment decision, through risk rating, through threat-vulnerability pairing, to the original evidence. Traceability is what makes a risk assessment defensible under audit.
- ✅ Document assumptions and confidence levels honestly — false precision undermines credibility more than acknowledged uncertainty. A risk assessment that claims 95% confidence in every rating is a risk assessment that nobody should trust.
- ✅ Every section of the report must be populated — an incomplete report undermines the credibility of the entire risk assessment effort and may fail regulatory scrutiny

### Step-Specific Rules:

- 🎯 Focus exclusively on report compilation, executive summary generation, appendix creation, quality assurance, confidence documentation, communication planning, maintenance planning, and formal closure
- 🚫 FORBIDDEN to re-open risk calculations, modify risk ratings, alter likelihood or impact scores, or change treatment decisions — that analytical work is complete. If findings need revision, the operator must explicitly request revisiting a prior step.
- 💬 Approach: synthesis and communication — distill six steps of analytical work into actionable intelligence that drives organizational decisions. The quality of the report determines whether the assessment creates impact or gathers dust.
- 📊 The executive summary must be comprehensible to non-technical leadership — no jargon without explanation, no risk matrices without interpretation, no technical acronyms without context
- 🔒 Report classification should be established before distribution — risk assessments contain organizational vulnerability data that adversaries would find extremely valuable
- ⏱️ This step produces the final deliverable — quality and completeness are paramount. A rushed final step undermines all prior work.
- 📝 The report quality assurance checklist is a hard gate — every check must pass before the assessment can be formally closed

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your reporting expertise ensures the risk assessment creates organizational impact, not just organizational paperwork
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Executive summary buries critical findings beneath methodology descriptions or qualifications — explain decision-maker blindness risk: executives read the first page and the recommendations. If the top 3 risks are not immediately visible, the investment decisions that address those risks will not be made. The assessment fails its primary purpose.
  - Report lacks confidence levels for assessment areas — explain false precision risk: a risk register that rates every entry without acknowledging the uncertainty behind those ratings creates a false sense of analytical rigor. When a likelihood rating is based on limited threat intelligence, saying so is not weakness — it is intellectual honesty that builds credibility. Auditors specifically look for assumption documentation.
  - No communication plan for stakeholders — explain report-sits-on-shelf risk: a risk assessment that exists only as a PDF on a shared drive creates zero organizational change. Without a deliberate plan to deliver findings to the right people in the right format at the right time, the assessment is a sunk cost. Define who gets what, when, and how.
  - Residual risks exceed risk appetite but no formal acceptance documented — explain accountability gap risk: if the organization is knowingly operating above its stated risk appetite, that decision must be formally documented with a named decision-maker. Implicit risk acceptance is a governance failure.
  - Report does not include maintenance triggers — explain assessment decay risk: a risk assessment is a point-in-time snapshot. Without defined triggers for reassessment (new threats, major changes, incidents, regulatory shifts), the assessment loses relevance within months. NIST 800-30 Step 4 (Maintain Assessment) exists for this reason.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks. The operator decides, you facilitate.

## EXECUTION PROTOCOLS:

- 🎯 Present your report compilation plan before beginning — let the operator know what sections will be generated and in what order
- 🎯 Load the output document and verify that `step-06-treatment.md` (or equivalent step 6) is present in stepsCompleted — all six analytical steps must be complete before reporting begins
- ⚠️ Present [A]/[W]/[F] menu after closure is complete — there is NO [C] Continue option as this is the final step
- 💾 Save all sections to the output document as they are generated and reviewed
- 📖 Update frontmatter: add this step name to the end of stepsCompleted, set `assessment_status` to the final status, and update all final tracking fields
- 💾 Update frontmatter fields: `executive_summary_complete: true`, `report_finalized: true`, `chronicle_recommended: true`, `assessment_status: 'complete'`
- 🎯 Perform final frontmatter consistency check — verify ALL frontmatter fields are populated and internally consistent with the report body content
- 🚫 This is the FINAL step — there is no next step file

## CONTEXT BOUNDARIES:

- Available context: Complete risk assessment data from steps 1-6 (Scope & Initialization, Asset Discovery & Crown Jewels, Threat Identification, Vulnerability & Control Assessment, Risk Calculation & Analysis, Treatment Planning), all frontmatter fields, engagement.yaml, risk register, treatment plan, FAIR analyses
- Focus: Executive summary generation, report finalization, appendix compilation, quality assurance, confidence documentation, communication planning, maintenance planning, and formal closure — no new analytical activity
- Limits: Do not fabricate findings, inflate risk ratings, or embellish the report — accuracy is paramount. Do not modify risk ratings, likelihood/impact scores, or treatment decisions — those are finalized in prior steps. The executive summary must accurately reflect the analytical findings, not oversimplify to the point of misrepresentation.
- Dependencies: All prior steps (1-6) should be completed. If any step was not completed, WARN the operator before proceeding with reporting — an incomplete assessment produces an incomplete report.

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Complete Assessment Data

Load the output document and verify the complete assessment state. All six prior steps must be completed before the report can be finalized.

"**Report Compilation — Loading Assessment Data:**

I will load the complete risk assessment output and verify that all analytical steps (1-6) are complete. The report can only be finalized when all source data is in place."

**Verification Checklist:**

| # | Step | Expected in stepsCompleted | Status |
|---|------|---------------------------|--------|
| 1 | Initialization & Scoping | step-01-init.md | {{Present / Missing}} |
| 2 | Asset Discovery & Crown Jewels | step-02-assets.md | {{Present / Missing}} |
| 3 | Threat Identification | step-03-threats.md | {{Present / Missing}} |
| 4 | Vulnerability & Control Assessment | step-04-vulns.md | {{Present / Missing}} |
| 5 | Risk Calculation & Analysis | step-05-risk.md | {{Present / Missing}} |
| 6 | Treatment Planning | step-06-treatment.md | {{Present / Missing}} |

{{IF any step is missing:}}
**⚠️ WARNING — Incomplete Assessment:**
The following steps are not marked as completed: {{list missing steps}}. A risk assessment report built on incomplete analysis will have gaps that undermine credibility and may fail regulatory scrutiny.

**Options:**
- [R] Return to the missing step to complete the analysis
- [P] Proceed with reporting — gaps will be documented as known limitations in the report

Which option? I recommend [R] unless time constraints are severe.
{{END IF}}

{{IF all steps present:}}
**✅ All 6 analytical steps confirmed complete. Proceeding with report compilation.**
{{END IF}}

**Compile Key Assessment Metrics from the complete dataset:**

| Metric | Value |
|--------|-------|
| Assessment ID | {{assessment_id}} |
| Assessment Date Range | {{start_date}} to {{current_date}} |
| Scope | {{assessment_scope summary}} |
| Methodology | {{risk_model — e.g., NIST 800-30 + FAIR hybrid}} |
| Total Assets Inventoried | {{count}} |
| Crown Jewels Identified | {{crown_jewels_count}} |
| Total Threat Sources Identified | {{count}} |
| Total Threat Events Analyzed | {{count}} |
| Total Vulnerabilities Identified | {{count}} |
| Control Gaps Identified | {{count}} |
| Existing Controls Evaluated | {{count}} |
| Total Risks in Register | {{count}} |
| Risk Distribution — Very High | {{count}} ({{percentage}}%) |
| Risk Distribution — High | {{count}} ({{percentage}}%) |
| Risk Distribution — Moderate | {{count}} ({{percentage}}%) |
| Risk Distribution — Low | {{count}} ({{percentage}}%) |
| Risk Distribution — Very Low | {{count}} ({{percentage}}%) |
| Risks Exceeding Risk Appetite | {{count}} |
| FAIR ALE — Total Annualized Loss Exposure | {{total_ale if hybrid model}} |
| Treatment Decisions — Mitigate | {{count}} |
| Treatment Decisions — Transfer | {{count}} |
| Treatment Decisions — Avoid | {{count}} |
| Treatment Decisions — Accept | {{count}} |
| Residual Risks Within Appetite | {{count}} / {{total}} |
| Residual Risks Still Exceeding Appetite | {{count}} (formally accepted) |

Present these compiled metrics to the operator:

"**Assessment Metrics Summary — Compiled from Steps 1-6:**

{{metrics table above}}

Are these metrics accurate and complete? These numbers will form the basis of the executive summary and report appendices. Any discrepancy should be corrected now before the report is finalized."

Wait for operator review and confirmation of metrics accuracy.

### 2. Executive Summary Compilation

Generate Section 7 of the risk assessment report — the executive summary. This is typically the only section that board members, audit committees, and executive leadership will read. It must be accurate, concise, business-focused, and free of technical jargon.

"**Executive Summary — Draft for Review:**

I will draft the executive summary based on the complete assessment data from steps 1-6. Please review carefully — this section will be the primary reference for leadership, may be shared with the audit committee, and may be referenced by regulators."

**Section 7.1 — Assessment Overview:**

- Assessment name, ID, and date range
- Organizational scope boundaries (what was assessed, what was excluded, and why)
- Methodology: NIST SP 800-30 Rev. 1 systematic risk assessment process with FAIR quantitative enrichment for critical risks (if hybrid model selected)
- Assessment team: facilitator (Arbiter), operator, identified stakeholders
- Assessment trigger: regulatory requirement, compliance cycle, incident-driven, new system, merger/acquisition, or proactive risk management
- Regulatory drivers: which frameworks this assessment supports (SOX 404, HIPAA, PCI DSS, NIST CSF, ISO 27001, NIS2, etc.)

**Section 7.2 — Key Findings:**

The top 3-5 findings that matter most to decision-makers. Each finding must answer three questions:

1. **What?** — The finding in plain business language
2. **Why does it matter?** — The business impact if not addressed (quantified where possible)
3. **What should we do?** — The recommended action in business terms

**Finding Format:**

"**Finding {{N}}: {{Finding Title}}**
{{1-2 sentence description in business language — no jargon}}

**Business Impact:** {{What could happen, how likely, how severe — in terms leadership understands: revenue, reputation, regulatory penalty, operational disruption}}

**Recommended Action:** {{What to do, by when, estimated investment}}

**Risk Level:** {{Very High / High / Moderate}} | **Estimated Annual Exposure:** {{ALE if quantified}}"

**Writing Guidelines for Findings:**
- No jargon — translate technical findings to business language. "Unpatched CVE-2024-XXXX on internet-facing server" becomes "a known vulnerability in our customer-facing web platform that attackers are actively exploiting across the industry"
- Quantify where possible — dollar ranges, system counts, affected users, regulatory penalty ranges
- Focus on business risk, not technical implementation details
- Be honest about what is known vs estimated vs assumed — clearly label uncertainties
- Prioritize by business impact, not CVSS score

**Section 7.3 — Risk Landscape Summary:**

- Aggregate risk profile: how many risks at each level (Very High through Very Low)
- Risk heat map reference: point to the risk heat map in the appendices for visual representation
- Comparison to risk appetite: how many risks exceed the organization's stated risk appetite? Are these formally accepted or pending treatment?
- Risk concentration: are risks clustered around specific assets, threat sources, or business functions? What does this concentration tell us?
- Trend indicators: if a prior assessment exists, how has the risk profile changed? More risks? Fewer? Higher severity? Lower? New categories?
- Overall risk posture assessment: one-paragraph professional opinion on the organization's current risk posture

**Section 7.4 — Top Risks:**

| Rank | Risk ID | Risk Description | Level | ALE (if FAIR) | Treatment Strategy | Risk Owner | Implementation Timeline |
|------|---------|-----------------|-------|--------------|-------------------|------------|------------------------|
| 1 | {{risk_id}} | {{plain language description}} | {{VH/H/M}} | {{$X,XXX - $XX,XXX}} | {{Mitigate/Transfer/Avoid/Accept}} | {{named owner}} | {{timeline}} |
| 2 | ... | ... | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... | ... |

Top 5-10 risks by severity. This table is what the board sees. Every entry must be understandable to a non-technical reader. Include only Very High and High risks unless the total risk count is low.

**Section 7.5 — Strategic Recommendations:**

Organize recommendations by implementation priority and timeline:

"**Priority 1 — Immediate Actions (0-30 days):**

These actions address Very High risks or risks that are actively being exploited. Delay increases exposure.

| # | Recommendation | Addresses Risk(s) | Expected Risk Reduction | Estimated Cost | Owner |
|---|---------------|-------------------|------------------------|---------------|-------|
| P1-1 | {{action in business language}} | {{risk_id(s)}} | {{VH→H or H→M}} | {{$range}} | {{owner}} |
| P1-2 | ... | ... | ... | ... | ... |

**Priority 2 — Short-term Actions (30-90 days):**

These actions address High risks and foundational control gaps. They require planning and resource allocation.

| # | Recommendation | Addresses Risk(s) | Expected Risk Reduction | Estimated Cost | Owner |
|---|---------------|-------------------|------------------------|---------------|-------|
| P2-1 | {{action}} | {{risk_id(s)}} | {{level change}} | {{$range}} | {{owner}} |
| P2-2 | ... | ... | ... | ... | ... |

**Priority 3 — Medium-term Actions (90-180 days):**

These actions address Moderate risks and strategic improvements. They require budget cycles and project planning.

| # | Recommendation | Addresses Risk(s) | Expected Risk Reduction | Estimated Cost | Owner |
|---|---------------|-------------------|------------------------|---------------|-------|
| P3-1 | {{action}} | {{risk_id(s)}} | {{level change}} | {{$range}} | {{owner}} |
| P3-2 | ... | ... | ... | ... | ... |"

**Section 7.6 — Investment Priorities:**

For FAIR-quantified risks, present the business case for treatment investment:

"**Investment Analysis — Risk Treatment ROI:**

| # | Treatment | ALE Without Treatment | Treatment Cost (Annual) | ALE After Treatment | Net Annual Benefit | ROI |
|---|-----------|----------------------|------------------------|--------------------|--------------------|-----|
| 1 | {{treatment name}} | {{$current_ale}} | {{$treatment_cost}} | {{$residual_ale}} | {{$benefit}} | {{percentage}}% |
| 2 | ... | ... | ... | ... | ... | ... |

**Aggregate Investment Summary:**
- **Cost of inaction:** Total aggregate ALE without treatment = {{$total_current_ale}} per year
- **Cost of treatment:** Total annual treatment investment = {{$total_treatment_cost}} per year
- **Expected ALE after treatment:** {{$total_residual_ale}} per year
- **Net annual risk reduction:** {{$total_benefit}} per year
- **Overall ROI:** {{$total_benefit / $total_treatment_cost * 100}}%

**Budget Recommendation:**
{{1-2 paragraph business justification for the recommended investment level, citing specific risks, regulatory obligations, and potential consequences of inaction. Frame in terms leadership understands: protecting revenue, avoiding regulatory penalties, maintaining customer trust, supporting business objectives.}}"

{{IF purely qualitative model — no FAIR quantification:}}
"**Note:** This assessment used a qualitative methodology. Investment priorities are based on risk severity rankings rather than quantified financial exposure. For future assessments, consider hybrid NIST 800-30 + FAIR approach to enable ROI-based investment decisions for critical risks."
{{END IF}}

Present the complete executive summary draft to the operator:

"**Draft Executive Summary (Section 7) — Complete:**

{{full executive summary draft — sections 7.1 through 7.6}}

Please review this summary carefully:
- **Accurate** — does it correctly represent the analytical findings from steps 1-6?
- **Complete** — are any business-relevant findings or recommendations missing?
- **Appropriate** — is the tone and level of detail suitable for executive and board audiences?
- **Honest** — are uncertainties clearly communicated without undermining credibility?
- **Actionable** — can a decision-maker act on these recommendations without additional analysis?

I can adjust language, add details, modify framing, or reorder priorities before we finalize."

Wait for operator review and approval. Iterate until the operator is satisfied.

Write the approved executive summary under `## Section 7: Executive Summary` in the report.

### 3. Appendices Compilation

Compile Section 8 — Appendices. These provide the detailed reference material that supports the executive summary findings.

"**Compiling Report Appendices — Section 8:**

The appendices provide the detailed evidence, methodology, and reference material that supports every finding in the executive summary. These are the sections that technical teams, auditors, and compliance reviewers will reference."

**Appendix A — Methodology Reference:**

"**A. Methodology Reference**

**Primary Framework:** NIST SP 800-30 Rev. 1 — Guide for Conducting Risk Assessments
**Quantitative Enrichment:** {{FAIR (Factor Analysis of Information Risk) for critical risks / Not used — qualitative only}}

**Process Steps:**
1. **Prepare for Assessment** (Step 1) — Defined scope, methodology, stakeholders, risk appetite
2. **Conduct Assessment** (Steps 2-5):
   - Identify threat sources and threat events (Step 3)
   - Identify vulnerabilities and predisposing conditions (Step 4)
   - Determine likelihood of occurrence (Step 5)
   - Determine magnitude of impact (Step 5)
   - Determine risk (Step 5)
3. **Communicate Results** (Steps 6-7) — Treatment planning, executive reporting
4. **Maintain Assessment** (Step 7) — Maintenance plan, reassessment triggers

**Risk Model:** {{Qualitative / Semi-Quantitative / Hybrid (Qualitative + FAIR)}}
**Assessment Scales:** See Appendix B for all scales used
**FAIR Parameters:** See Appendix C for quantitative analysis details"

**Appendix B — NIST 800-30 Assessment Scales:**

"**B. Assessment Scales**

**Likelihood Scale (NIST 800-30 Table H-3):**

| Level | Score | Description | Frequency Guidance |
|-------|-------|-------------|-------------------|
| Very High | 10 | Almost certain to occur | Multiple times per year |
| High | 8 | Highly likely to occur | Once per year |
| Moderate | 5 | Somewhat likely to occur | Once every 2-3 years |
| Low | 2 | Unlikely but possible | Once every 5-10 years |
| Very Low | 0 | Highly unlikely | Less than once per 10 years |

**Impact Scale (NIST 800-30 Table H-4):**

| Level | Score | Description | Business Impact Guidance |
|-------|-------|-------------|------------------------|
| Very High | 10 | Catastrophic adverse effect | Existential threat to mission, massive financial loss, severe regulatory penalty |
| High | 8 | Severe adverse effect | Major mission degradation, significant financial loss, regulatory action |
| Moderate | 5 | Serious adverse effect | Noticeable mission impact, moderate financial loss, compliance findings |
| Low | 2 | Limited adverse effect | Minor mission impact, minimal financial loss, audit observations |
| Very Low | 0 | Negligible adverse effect | No noticeable mission impact, trivial financial loss |

**Risk Level Matrix (NIST 800-30 Table I-2):**

| Likelihood ↓ / Impact → | Very Low (0) | Low (2) | Moderate (5) | High (8) | Very High (10) |
|--------------------------|-------------|---------|-------------|----------|---------------|
| Very High (10) | Very Low | Low | Moderate | High | Very High |
| High (8) | Very Low | Low | Moderate | High | Very High |
| Moderate (5) | Very Low | Low | Moderate | Moderate | High |
| Low (2) | Very Low | Low | Low | Low | Moderate |
| Very Low (0) | Very Low | Very Low | Very Low | Low | Low |

**Risk Severity Classification:**

| Level | Score Range | Response Requirement |
|-------|-----------|---------------------|
| Very High | 96-100 | Immediate executive action required — unacceptable risk |
| High | 80-95 | Senior management attention required — treatment plan mandatory |
| Moderate | 21-79 | Management attention required — treatment plan recommended |
| Low | 5-20 | Routine procedures — monitor and accept |
| Very Low | 0-4 | No action required — accept and document |"

**Appendix C — FAIR Analysis Details:**

{{IF hybrid model with FAIR quantification:}}
"**C. FAIR Analysis Details**

For each risk analyzed using FAIR quantification:

**Risk {{risk_id}}: {{risk_name}}**

| FAIR Parameter | Value | Basis / Source |
|---------------|-------|---------------|
| Loss Event Frequency (LEF) | {{range}} | {{basis for estimate}} |
| — Threat Event Frequency (TEF) | {{range}} | {{threat intel / incident history / industry data}} |
| — Vulnerability (Vuln) | {{percentage}} | {{control effectiveness assessment}} |
| Loss Magnitude (LM) | {{$range}} | {{basis for estimate}} |
| — Primary Loss | {{$range}} | {{response costs, replacement costs, fines}} |
| — Secondary Loss | {{$range}} | {{reputation, competitive advantage, litigation}} |
| — Secondary Loss Event Frequency | {{percentage}} | {{likelihood of secondary effects}} |
| Annualized Loss Exposure (ALE) | {{$range}} | {{LEF x LM}} |
| Confidence Level | {{percentage}} | {{data quality assessment}} |
| Key Assumptions | {{list}} | {{what was assumed and impact if wrong}} |

{{Repeat for each FAIR-quantified risk}}

**FAIR Aggregation:**
- Total ALE across all quantified risks: {{$total_ale_range}}
- Risks quantified: {{count}} of {{total_risks}} ({{percentage}}%)
- Average confidence level: {{percentage}}%
- Note: ALE ranges represent 80% confidence intervals — there is a 10% chance actual losses exceed the upper bound"
{{END IF}}

{{IF qualitative only:}}
"**C. FAIR Analysis Details**

FAIR quantitative analysis was not performed for this assessment. The assessment used qualitative/semi-quantitative methodology exclusively per the agreed scope. For future assessments where investment ROI analysis is required, recommend hybrid NIST 800-30 + FAIR approach for critical risks."
{{END IF}}

**Appendix D — Complete Risk Register:**

"**D. Complete Risk Register**

The complete risk register in exportable format. All columns from the risk calculation and treatment steps:

| # | Risk ID | Threat Source | Threat Event | Vulnerability / Predisposing Condition | Affected Asset(s) | Asset Criticality | Likelihood | Impact | Inherent Risk Level | Inherent Risk Score | Existing Controls | Control Effectiveness | Treatment Strategy | Planned Controls | Residual Likelihood | Residual Impact | Residual Risk Level | Residual Risk Score | Risk Owner | Implementation Timeline | Status |
|---|---------|--------------|-------------|--------------------------------------|-------------------|------------------|-----------|--------|-------------------|--------------------|--------------------|----------------------|-------------------|-----------------|--------------------|-----------------|--------------------|-----------------------|------------|------------------------|--------|
| 1 | {{id}} | {{source}} | {{event}} | {{vuln}} | {{asset}} | {{criticality}} | {{L}} | {{I}} | {{level}} | {{score}} | {{controls}} | {{effectiveness}} | {{strategy}} | {{planned}} | {{res_L}} | {{res_I}} | {{res_level}} | {{res_score}} | {{owner}} | {{timeline}} | {{status}} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Register Statistics:**
- Total entries: {{count}}
- By inherent risk level: VH={{count}}, H={{count}}, M={{count}}, L={{count}}, VL={{count}}
- By residual risk level: VH={{count}}, H={{count}}, M={{count}}, L={{count}}, VL={{count}}
- By treatment strategy: Mitigate={{count}}, Transfer={{count}}, Avoid={{count}}, Accept={{count}}
- With assigned owner: {{count}} / {{total}} ({{percentage}}%)
- With implementation timeline: {{count}} / {{total}} ({{percentage}}%)"

**Appendix E — Control Mapping:**

"**E. Control Mapping**

Mapping of identified controls and control gaps to established framework references:

| # | Control / Gap | Status | NIST 800-53 Rev. 5 | CIS Controls v8 | ISO 27001:2022 | Risk(s) Addressed |
|---|-------------|--------|--------------------|-----------------|--------------------|-------------------|
| 1 | {{control name}} | {{Implemented / Partial / Planned / Gap}} | {{control family and number}} | {{CIS control number}} | {{Annex A control}} | {{risk_id(s)}} |
| 2 | ... | ... | ... | ... | ... | ... |

**Control Coverage Summary:**
- Total controls evaluated: {{count}}
- Implemented (effective): {{count}} ({{percentage}}%)
- Implemented (partially effective): {{count}} ({{percentage}}%)
- Planned (in treatment plan): {{count}} ({{percentage}}%)
- Gaps (no control): {{count}} ({{percentage}}%)
- Framework coverage: NIST 800-53 = {{percentage}}% mapped, CIS = {{percentage}}% mapped, ISO 27001 = {{percentage}}% mapped"

**Appendix F — Assumptions & Confidence Levels:**

"**F. Assumptions & Confidence Levels**

Every risk assessment is built on assumptions. Documenting them is not a weakness — it is intellectual honesty that makes the assessment defensible and maintainable.

**Assessment-Wide Assumptions:**

| # | Assumption | Assessment Area | Impact if Wrong | Mitigation |
|---|-----------|----------------|----------------|-----------|
| 1 | {{assumption statement}} | {{Scope / Threats / Vulns / Likelihood / Impact / Treatment}} | {{what changes in the assessment if this assumption is invalid}} | {{how to validate or monitor this assumption}} |
| 2 | ... | ... | ... | ... |

**Confidence Levels by Assessment Area:**

See Section 5 of this step for the detailed confidence level table.

**Data Quality Assessment:**

| Data Source | Quality | Completeness | Notes |
|------------|---------|-------------|-------|
| Asset inventory | {{High / Medium / Low}} | {{percentage}}% estimated coverage | {{basis for quality assessment}} |
| Threat intelligence | {{High / Medium / Low}} | {{scope of threat landscape covered}} | {{sources used}} |
| Vulnerability data | {{High / Medium / Low}} | {{scan coverage, manual assessment coverage}} | {{tools and methods used}} |
| Control documentation | {{High / Medium / Low}} | {{percentage}}% controls with evidence of effectiveness | {{assessment method}} |
| Impact estimates | {{High / Medium / Low}} | {{basis — BIA, financial data, stakeholder input}} | {{confidence in estimates}} |
| Incident history | {{High / Medium / Low}} | {{years of history, completeness of records}} | {{data source}} |"

**Appendix G — Glossary:**

"**G. Glossary**

Key terms used in this risk assessment report:

| Term | Definition |
|------|-----------|
| ALE | Annualized Loss Exposure — the expected annual financial loss from a specific risk (FAIR) |
| Crown Jewel | A critical asset whose compromise would have catastrophic impact on the organization |
| FAIR | Factor Analysis of Information Risk — a quantitative risk analysis methodology |
| Inherent Risk | The level of risk before any controls or treatments are applied |
| LEF | Loss Event Frequency — how often a loss event is expected to occur per year (FAIR) |
| Likelihood | The probability that a given threat source will exercise a vulnerability |
| NIST 800-30 | NIST Special Publication 800-30 Rev. 1 — Guide for Conducting Risk Assessments |
| Predisposing Condition | An existing condition that increases or decreases the likelihood of a threat event |
| Residual Risk | The level of risk remaining after controls and treatments are applied |
| Risk Appetite | The amount and type of risk an organization is willing to accept in pursuit of its objectives |
| Risk Register | The comprehensive catalog of identified risks with ratings, owners, and treatment decisions |
| Risk Tolerance | The acceptable deviation from the risk appetite — how much variance is permissible |
| TEF | Threat Event Frequency — how often a threat agent acts against an asset per year (FAIR) |
| Threat Event | An event or situation that has the potential for causing undesirable consequences |
| Threat Source | The intent and method targeted at the exploitation of a vulnerability |
| Treatment | An action taken to modify risk — mitigate, transfer, avoid, or accept |
| Vulnerability | A weakness in a system, procedure, or control that could be exploited by a threat source |"

Present the compiled appendices to the operator:

"**Appendices (Section 8) — Draft Complete:**

{{list all appendices A through G with brief description of each}}

Are the appendices complete and accurate? Are there any additional reference materials that should be included? Any appendix that needs adjustment before finalization?"

Wait for operator review and confirmation.

Write the approved appendices under `## Section 8: Appendices` in the report.

### 4. Report Quality Assurance

Conduct a systematic quality check on the complete report. This is a hard gate — every section must pass and every quality criterion must be met before the assessment can be formally closed.

"**Report Quality Assurance — Comprehensive Audit:**

I will conduct a systematic review of the complete risk assessment report to verify completeness, consistency, and quality. This is a hard gate — all checks must pass before the assessment can be closed."

**Section Completeness Audit:**

| # | Section | Status | Content Assessment | Notes |
|---|---------|--------|-------------------|-------|
| 1 | Section 1: Scope & Methodology | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |
| 2 | Section 2: Asset Inventory & Crown Jewels | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |
| 3 | Section 3: Threat Identification | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |
| 4 | Section 4: Vulnerability & Control Assessment | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |
| 5 | Section 5: Risk Calculation & Analysis | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |
| 6 | Section 6: Treatment Plan | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |
| 7 | Section 7: Executive Summary | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |
| 8 | Section 8: Appendices (A-G) | {{Populated / Missing / Incomplete}} | {{substantive content check}} | {{details}} |

**Quality Criteria Audit:**

| # | Quality Criterion | Status | Notes |
|---|------------------|--------|-------|
| 1 | All 8 sections have substantive content (no empty or placeholder sections) | {{Pass / Fail}} | {{details}} |
| 2 | Executive summary reflects actual findings from steps 1-6 — no contradictions | {{Pass / Fail}} | {{details}} |
| 3 | Executive summary is non-technical and business-focused — comprehensible to board audience | {{Pass / Fail}} | {{details}} |
| 4 | Risk ratings are consistent across all sections — register matches analysis, treatment matches register | {{Pass / Fail}} | {{details}} |
| 5 | Treatment plan aligns with risk register — every treated risk has a corresponding treatment entry | {{Pass / Fail}} | {{details}} |
| 6 | Residual risks are within stated risk appetite — or formally accepted with documented rationale | {{Pass / Fail}} | {{details}} |
| 7 | All assumptions are documented in Appendix F | {{Pass / Fail}} | {{details}} |
| 8 | Confidence levels are stated for all assessment areas | {{Pass / Fail}} | {{details}} |
| 9 | Traceability: every recommendation traces back to a risk, which traces back to evidence | {{Pass / Fail}} | {{details}} |
| 10 | No dangling references, empty tables, or placeholder content ({{...}} patterns) | {{Pass / Fail}} | {{details}} |
| 11 | Frontmatter fields are complete and consistent with report body content | {{Pass / Fail}} | {{details}} |
| 12 | Assessment ID is consistent throughout the report | {{Pass / Fail}} | {{details}} |
| 13 | Risk owner assigned to every risk in the register | {{Pass / Fail}} | {{details}} |
| 14 | Implementation timelines assigned to all treatment actions | {{Pass / Fail}} | {{details}} |
| 15 | FAIR calculations are mathematically consistent (if hybrid model) | {{Pass / Fail}} | {{details}} |
| 16 | Control mapping references valid framework control IDs | {{Pass / Fail}} | {{details}} |
| 17 | Glossary includes all domain-specific terms used in the report | {{Pass / Fail}} | {{details}} |

**Overall Report Status:** {{PASS — ready for finalization / FAIL — requires remediation}}

{{IF any section is Missing or Incomplete:}}
**ACTION REQUIRED:** The following sections need attention before the report can be finalized:
{{list of incomplete sections with what is missing}}

Would you like to address these gaps now, or note them as known limitations in the report?
{{END IF}}

{{IF any quality criterion fails:}}
**QUALITY ISSUES:** The following quality criteria were not met:
{{list of failed checks with specific remediation guidance}}

Would you like to remediate these issues now? I can provide specific guidance for each failed criterion.
{{END IF}}

{{IF all checks pass:}}
**✅ REPORT QUALITY ASSURANCE PASSED — All sections populated, all quality criteria met. The report is ready for finalization.**
{{END IF}}

Wait for operator to address any issues or accept the report with noted limitations.

### 5. Confidence Level Documentation

For each major assessment area, document the confidence level, basis for that confidence, key assumptions, and what changes in the assessment if those assumptions are wrong. This is intellectual honesty that makes the assessment defensible and maintainable.

"**Confidence Level Assessment — By Assessment Area:**

Documenting confidence levels is not a weakness — it is the mark of a rigorous, professional assessment. Every stakeholder should understand where the assessment is strongest and where uncertainty remains."

| # | Assessment Area | Confidence | Basis for Confidence | Key Assumptions | If Wrong — Impact on Assessment |
|---|----------------|------------|---------------------|----------------|-------------------------------|
| 1 | Asset inventory completeness | {{High / Medium / Low}} | {{automated discovery + manual validation / manual inventory only / partial coverage}} | {{e.g., CMDB is current and complete, shadow IT is minimal}} | {{undiscovered assets may harbor unassessed risks — overall risk posture could be understated}} |
| 2 | Threat identification coverage | {{High / Medium / Low}} | {{multiple threat intel sources + industry reports / single source / general knowledge only}} | {{e.g., threat landscape is adequately represented by available intelligence}} | {{unidentified threat sources could exploit vulnerabilities not covered by treatment plan}} |
| 3 | Vulnerability assessment accuracy | {{High / Medium / Low}} | {{authenticated scan + manual review / unauthenticated scan only / documentation review only}} | {{e.g., scan results are current, configuration baselines are accurate}} | {{undiscovered vulnerabilities change likelihood ratings — some risks may be underrated}} |
| 4 | Control effectiveness ratings | {{High / Medium / Low}} | {{control testing + evidence review / documentation review only / self-attestation}} | {{e.g., controls operate as documented, no degradation since last test}} | {{overrated control effectiveness means residual risk is higher than reported}} |
| 5 | Likelihood ratings | {{High / Medium / Low}} | {{incident data + threat intel + industry benchmarks / expert judgment only}} | {{e.g., historical patterns predict future frequency, threat landscape is stable}} | {{underrated likelihood means risk levels are understated — treatment urgency may be higher}} |
| 6 | Impact ratings | {{High / Medium / Low}} | {{BIA data + financial analysis + stakeholder input / estimate without BIA / general assessment}} | {{e.g., impact estimates account for cascading effects, regulatory penalties are correctly estimated}} | {{underrated impact means risk levels are understated — investment justification may be insufficient}} |
| 7 | FAIR quantification precision | {{High / Medium / Low / N/A}} | {{calibrated estimates with industry data / expert estimates without calibration / N/A — qualitative only}} | {{e.g., frequency and magnitude ranges are reasonable, loss distributions are appropriate}} | {{ALE ranges may not bracket actual losses — investment ROI calculations may be misleading}} |
| 8 | Treatment effectiveness projections | {{High / Medium / Low}} | {{based on vendor claims + industry benchmarks + organizational experience / vendor claims only / assumption}} | {{e.g., planned controls will be implemented as designed, control effectiveness will match projections}} | {{actual residual risk may be higher than projected — treatment plan may be insufficient}} |

**Overall Assessment Confidence:** {{High / Medium / Low}}
**Confidence Rationale:** {{1-2 sentence overall assessment of data quality and analytical rigor}}

"**Confidence Assessment — Complete:**

{{confidence table above}}

**Key Takeaway for Stakeholders:**
{{1-2 sentences summarizing where the assessment is strongest, where uncertainty remains, and what actions would improve confidence in future assessments}}

Is this confidence assessment honest and accurate? Any areas where you believe the confidence is over- or under-stated?"

Wait for operator review.

Write the confidence assessment to Appendix F in the report.

### 6. Communication Plan

Define how the risk assessment report reaches each audience in the appropriate format with the right key messages. A risk assessment that sits on a shared drive unread creates zero organizational change.

"**Communication Plan — Report Distribution:**

Different stakeholders need different views of the same assessment data. The communication plan ensures the right people receive the right information in the right format at the right time."

| # | Audience | Deliverable | Format | Key Messages | Delivery Method | Timeline |
|---|----------|------------|--------|-------------|----------------|----------|
| 1 | Board / Audit Committee | Executive Summary (Section 7) | Presentation deck / 1-2 page brief | Top risks, risk appetite compliance, investment ask, regulatory exposure | Board presentation / secure distribution | Within 1 week of finalization |
| 2 | CISO / CTO / Security Leadership | Full Report (all sections) | Complete document | Risk landscape, treatment roadmap, budget requirements, maintenance plan | Direct delivery — secure file share | Immediate upon finalization |
| 3 | Technical Teams (IT, Security Ops, Engineering) | Relevant sections + Appendices D & E | Technical detail — risk register + control mapping | Specific control implementations, remediation guidance, implementation timelines, success criteria | Team briefing + document distribution | Within 2 weeks |
| 4 | Compliance / Legal / Internal Audit | Risk Register + Treatment Plan + Control Mapping | Compliance view — sections 4, 5, 6 + Appendices D & E | Regulatory risk exposure, control gaps mapped to frameworks, treatment coverage, residual risk formal acceptance | Compliance team briefing | Within 1 week |
| 5 | Business Unit Owners | Risk summaries per BU | Tailored excerpts from risk register | Their specific risks, their risk ownership responsibilities, treatment actions assigned to their teams, timelines | 1:1 briefings with each BU owner | Within 2 weeks |
| 6 | Risk Committee (if exists) | Full Report + Confidence Assessment | Complete document with emphasis on Appendix F | Overall risk posture, confidence levels, assumptions, maintenance plan, comparison to appetite | Committee presentation | Next scheduled meeting |
| 7 | External Auditors (if applicable) | Full Report + Appendices | Complete document per audit requirements | Methodology compliance, control mapping, evidence of systematic process | Audit portal / secure transmission | Per audit schedule |

**Communication Guidelines:**
- **Classification:** The risk assessment report contains organizational vulnerability data — classify as Confidential or equivalent organizational classification. Do not distribute via unencrypted email.
- **Tailoring:** Each audience receives only what they need. Sending a 50-page technical report to the board is as ineffective as sending a 2-page summary to the implementation team.
- **Feedback loop:** Each communication should include a mechanism for the audience to ask questions, challenge findings, or provide additional context. The assessment improves with organizational input.
- **Tracking:** Track which stakeholders have received and acknowledged the report. Unread reports create zero risk reduction.

"**Communication Plan — Complete:**

{{communication table above}}

Which audiences apply to this assessment? Do any need to be added, removed, or adjusted? Are the delivery timelines realistic for your organization?"

Wait for operator review and confirmation.

### 7. Assessment Maintenance Plan

Document how the risk assessment stays current over time. A risk assessment is a point-in-time snapshot — without a maintenance plan, it begins losing relevance immediately. This implements NIST 800-30 Step 4: Maintain Assessment.

"**Assessment Maintenance Plan — NIST 800-30 Step 4:**

A risk assessment that is never updated is a risk assessment that creates a false sense of security. The maintenance plan defines when and how this assessment is refreshed."

**Reassessment Triggers:**

| # | Trigger | Action Required | Scope of Reassessment | Frequency / Timing | Responsible Party |
|---|---------|----------------|----------------------|-------------------|-------------------|
| 1 | Scheduled annual review | Full reassessment — complete steps 1-7 | All assets, threats, vulnerabilities | Annual (12 months from assessment date) | CISO / Risk Manager |
| 2 | Significant security incident | Targeted reassessment — focus on affected assets and threat vectors | Assets and threats related to the incident | Event-driven — within 30 days of incident closure | IR Team + Risk Manager |
| 3 | Major system or infrastructure change | Scope update + delta assessment — new assets, changed threat surface | New and modified systems | Change-driven — as part of change management process | Change Advisory Board |
| 4 | New threat intelligence | Threat and likelihood update — new threat sources, revised frequencies | Threat landscape and likelihood ratings | Quarterly review of threat intel feeds | Threat Intelligence Team |
| 5 | Regulatory or compliance change | Compliance impact analysis — new requirements, changed controls | Regulatory-driven scope | Event-driven — within 60 days of regulatory change effective date | Compliance Team |
| 6 | Control implementation milestone | Residual risk recalculation — verify control effectiveness, update residual ratings | Specific risks addressed by the implemented control | Milestone-driven — upon control deployment and validation | Risk Owner |
| 7 | Merger, acquisition, or divestiture | Full reassessment with expanded scope | New organizational boundaries and assets | Event-driven — as part of M&A due diligence | Executive Sponsor + CISO |
| 8 | Risk appetite change | Re-evaluate all risks against new appetite thresholds | All risks — new appetite comparison | Event-driven — when board approves new appetite statement | Risk Committee |
| 9 | Treatment plan failure or delay | Re-evaluate affected risks — original risk ratings may need to persist | Risks whose treatment is delayed or failed | Event-driven — when treatment milestones are missed | Risk Owner + CISO |
| 10 | Business strategy change | Strategic risk reassessment — new assets, new threats aligned to new objectives | Strategy-driven scope | Event-driven — when strategic plan is updated | Executive Leadership + CISO |

**Monitoring Between Assessments:**

| # | Monitoring Activity | Frequency | Responsible Party | Output |
|---|-------------------|-----------|-------------------|--------|
| 1 | Track treatment implementation status | Monthly | Risk owners (report to CISO) | Treatment status dashboard |
| 2 | Review new vulnerabilities against assessed assets | Continuous | Vulnerability Management Team | Updated vulnerability data |
| 3 | Monitor threat intelligence for relevant changes | Continuous | Threat Intelligence Team | Threat landscape update |
| 4 | Track incident data for likelihood validation | Quarterly | IR Team | Incident trend analysis |
| 5 | Validate risk appetite alignment | Semi-annual | Risk Committee | Appetite compliance report |

**Assessment Version Control:**

| Field | Value |
|-------|-------|
| Current version | {{version — e.g., 1.0}} |
| Next scheduled reassessment | {{date — 12 months from assessment date}} |
| Version history location | {{organizational knowledge base / GRC tool}} |
| Change log requirement | All modifications to the risk register between formal assessments must be logged with date, author, and rationale |

"**Maintenance Plan — Complete:**

{{maintenance tables above}}

Are these triggers and monitoring activities appropriate for your organization? Any triggers that should be added or modified? Is the annual reassessment cycle realistic, or should it be more frequent given your risk environment?"

Wait for operator review and confirmation.

### 8. Chronicle Documentation Recommendation

Recommend invoking Chronicle (SPECTRA's core documentation agent) to archive the risk assessment and create organizational knowledge management artifacts.

"**Chronicle Documentation Recommendation:**

The risk assessment report is now complete. I recommend invoking **Chronicle** (`spectra-agent-chronicle`) to:

1. **Archive the risk assessment report** in the organizational knowledge base — this ensures the assessment is discoverable, version-controlled, and available for future reference by any SPECTRA workflow or organizational process
2. **Create a summary record** for the SPECTRA engagement — a concise entry that captures the assessment scope, key findings, top risks, and treatment decisions for the engagement log
3. **Generate a debrief template** for the engagement closure — structured for a stakeholder debrief session that reviews assessment findings and confirms next steps

**Why Chronicle?**
The report IS the deliverable — this is what SPECTRA produces. Chronicle ensures the deliverable is properly archived, indexed, and accessible. Without archival, the assessment exists only as a local file that will be lost, forgotten, or impossible to find when the next assessment cycle begins or when an auditor asks for the prior assessment.

**Context for Chronicle:**
- Assessment ID: {{assessment_id}}
- Report path: `{outputFile}`
- Key findings: {{top 3 findings from executive summary}}
- Risk count: {{total_risks}} risks assessed, {{count}} exceeding appetite
- Treatment coverage: {{percentage}}% of risks have treatment plans
- Maintenance trigger: next reassessment due {{next_assessment_date}}

Note: Chronicle invocation is a recommendation — the operator decides whether to invoke it now, later, or not at all."

### 9. Close Assessment

Formally close the risk assessment engagement by updating all final tracking fields and presenting the closure summary.

"**Assessment Closure — Finalizing:**

Setting all final fields and preparing the closure summary."

**Update Frontmatter — Final State:**

- `assessment_status`: Set to 'complete'
- `report_finalized`: true
- `executive_summary_complete`: true
- `chronicle_recommended`: true
- `closure_timestamp`: Current timestamp in UTC
- `total_duration`: Calculate from assessment initialization timestamp to closure timestamp
- `total_assets`: Count from asset inventory
- `crown_jewels_count`: Count from Crown Jewels analysis
- `total_threat_sources`: Count from threat identification
- `total_threat_events`: Count from threat identification
- `total_vulnerabilities`: Count from vulnerability assessment
- `total_control_gaps`: Count from control assessment
- `total_risks`: Count from risk register
- `risks_very_high`: Count
- `risks_high`: Count
- `risks_moderate`: Count
- `risks_low`: Count
- `risks_very_low`: Count
- `risks_exceeding_appetite`: Count
- `total_ale`: Total ALE if FAIR quantification was used
- `treatments_mitigate`: Count
- `treatments_transfer`: Count
- `treatments_avoid`: Count
- `treatments_accept`: Count
- `residual_within_appetite`: Count
- `residual_exceeding_appetite`: Count (formally accepted)
- `next_reassessment_date`: 12 months from assessment date (or per maintenance plan)
- Add `step-07-reporting.md` to stepsCompleted array

**Final Frontmatter Consistency Check:**

Verify ALL frontmatter fields are populated and consistent with the report body:

| Check | Status |
|-------|--------|
| assessment_id matches throughout report | {{Pass / Fail}} |
| assessment_status = 'complete' | {{Pass / Fail}} |
| report_finalized = true | {{Pass / Fail}} |
| stepsCompleted contains all 7 steps | {{Pass / Fail}} |
| Risk counts match risk register | {{Pass / Fail}} |
| Treatment counts match treatment plan | {{Pass / Fail}} |
| All date fields populated | {{Pass / Fail}} |
| All count fields populated | {{Pass / Fail}} |
| No empty or placeholder frontmatter values | {{Pass / Fail}} |

**Present Final Assessment Summary:**

"**RISK ASSESSMENT {{assessment_id}} — CLOSURE REPORT**

{{user_name}}, the risk assessment workflow for {{engagement_name}} is now complete.

**Assessment Summary:**
- **Scope:** {{assessment_scope}}
- **Methodology:** {{risk_model}}
- **Duration:** {{total_duration}}
- **Assets Assessed:** {{total_assets}} (Crown Jewels: {{crown_jewels_count}})
- **Threats Identified:** {{total_threat_sources}} sources, {{total_threat_events}} events
- **Vulnerabilities Identified:** {{total_vulnerabilities}} (Control Gaps: {{total_control_gaps}})
- **Total Risks:** {{total_risks}}

**Risk Profile:**
- Very High: {{risks_very_high}} | High: {{risks_high}} | Moderate: {{risks_moderate}} | Low: {{risks_low}} | Very Low: {{risks_very_low}}
- Risks exceeding appetite: {{risks_exceeding_appetite}}
- FAIR Total ALE: {{total_ale if hybrid}} {{or 'N/A — qualitative model' if not}}

**Treatment Coverage:**
- Mitigate: {{treatments_mitigate}} | Transfer: {{treatments_transfer}} | Avoid: {{treatments_avoid}} | Accept: {{treatments_accept}}
- Residual risks within appetite: {{residual_within_appetite}} / {{total_risks}}
- Residual risks formally accepted above appetite: {{residual_exceeding_appetite}}

**Report:**
- File: `{outputFile}`
- Sections: 8 / 8 populated (7 body sections + appendices)
- Appendices: 7 (A-G)
- Quality assurance: {{PASS / PASS WITH NOTED LIMITATIONS}}

**Next Reassessment:** {{next_reassessment_date}}

**Recommended Next Steps:**
Based on the assessment findings, the following SPECTRA workflows are recommended:

{{IF regulatory or compliance gaps identified:}}
- **spectra-compliance-audit** — Conduct a formal compliance audit for {{identified frameworks}} to address regulatory control gaps identified in this assessment
{{END IF}}

{{IF threat detection gaps identified:}}
- **spectra-detection-lifecycle** — Build or improve detection rules for the threat events and ATT&CK techniques identified in this assessment. Current detection coverage may not address: {{specific gaps}}
{{END IF}}

{{IF active threat indicators identified:}}
- **spectra-threat-hunt** — Proactively hunt for the threat sources and TTPs identified in this assessment. Recommended hunt hypotheses: {{specific hypotheses based on identified threats}}
{{END IF}}

- **spectra-close-engagement** — Formally close the SPECTRA engagement and archive all artifacts

**Chronicle Recommendation:** Invoke Chronicle (`spectra-agent-chronicle`) to archive the risk assessment report in the organizational knowledge base and create the engagement record."

### 10. Present FINAL MENU OPTIONS

This is the FINAL step. There is NO [C] Continue option. The workflow completes here.

"**Risk assessment workflow complete.**

**Select an option:**
[A] Advanced Elicitation — Deep review of report quality, completeness, and analytical rigor. Challenge the executive summary, probe confidence levels, stress-test the traceability of recommendations to evidence.
[W] War Room — Full adversarial review of the entire risk assessment. Red challenges risk ratings and assumptions. Blue validates treatment plan effectiveness. Auditor checks methodology compliance and regulatory alignment. Arbiter defends analytical decisions.
[F] Finalize — Mark the risk assessment as complete and close the engagement (no more changes).

**Additional options:**
[CH] Invoke Chronicle for documentation archival and engagement record
[CA] Invoke spectra-compliance-audit for identified regulatory gaps
[DL] Invoke spectra-detection-lifecycle for threat detection rules
[TH] Invoke spectra-threat-hunt for proactive threat hunting"

#### Menu Handling Logic:

- IF A: Advanced elicitation on the complete report. Probe the operator's satisfaction with each major area:
  - Executive summary: Does it accurately represent findings? Is it compelling enough to drive action? Will leadership understand it? Are investment asks clear?
  - Risk register: Are risk ratings defensible? Are there any ratings that feel inflated or deflated? Any risks that were missed?
  - Treatment plan: Are treatment strategies realistic? Are timelines achievable? Are cost estimates reasonable? Is there organizational capacity to execute?
  - Confidence levels: Are they honest? Where is the assessment weakest? What additional data would improve confidence?
  - Assumptions: Are any assumptions fragile? Which assumptions, if wrong, would most change the assessment conclusions?
  Process insights, offer to update the report, then redisplay menu.

- IF W: War Room — invoke `spectra-war-room` with full assessment context. This is the most rigorous quality check available:
  - **Red Team perspective:** Challenge every risk rating. Are likelihood estimates supported by evidence or just gut feel? Are impact ratings consistent with actual organizational exposure? Are there threat sources that were overlooked? Are vulnerabilities understated?
  - **Blue Team perspective:** Validate the treatment plan. Are the proposed controls sufficient? Are there cheaper alternatives? Will the implementation timelines actually be met? Is the residual risk calculation realistic or optimistic?
  - **Auditor perspective:** Check methodology compliance. Does the assessment follow NIST 800-30 faithfully? Are all required documentation elements present? Would this assessment satisfy a regulatory examination? Are assumptions documented per professional standards?
  - **Arbiter perspective (you):** Defend the analytical methodology. Explain rating decisions. Justify the confidence levels. Defend the treatment recommendations.
  Summarize all perspectives with any identified issues. Offer to update the report based on War Room findings. Redisplay menu.

- IF F: **FINALIZE THE ASSESSMENT.** This is the terminal action.
  - Verify ALL frontmatter fields are populated and consistent
  - Set `assessment_status: 'complete'` (confirm it is set)
  - Set `report_finalized: true` (confirm it is set)
  - Present final completion message:

  "**RISK ASSESSMENT {{assessment_id}} — FINALIZED**

  The risk assessment for {{engagement_name}} is now formally complete.

  **Final Metrics:**
  - {{total_risks}} risks assessed across {{total_assets}} assets
  - {{risks_very_high}} Very High, {{risks_high}} High, {{risks_moderate}} Moderate risks identified
  - {{total_ale if FAIR}} total annualized loss exposure quantified
  - {{treatments_mitigate + treatments_transfer + treatments_avoid}} risks with active treatment plans
  - {{treatments_accept}} risks formally accepted
  - Report quality assurance: PASSED
  - Confidence levels: documented for {{count}} assessment areas

  **Report delivered at:** `{outputFile}`

  **Next reassessment due:** {{next_reassessment_date}}

  **Recommended next:**
  - Invoke **Chronicle** to archive the report and create the engagement record
  - Invoke **spectra-close-engagement** to formally close the SPECTRA engagement
  {{additional workflow recommendations based on findings}}

  Thank you for your partnership in this assessment, {{user_name}}. The risk register is now the organization's decision tool — monitor treatment implementation, track risk evolution, and reassess per the maintenance plan."

  — End workflow.

- IF CH: Recommend operator invoke `spectra-agent-chronicle` for documentation archival. Provide context: assessment_id, report path, key findings summary, risk counts, treatment summary. Redisplay menu.
- IF CA: Recommend operator invoke `spectra-compliance-audit` for regulatory gap closure. Provide context: identified regulatory frameworks, control gaps mapped to specific requirements, compliance risks from the assessment. Redisplay menu.
- IF DL: Recommend operator invoke `spectra-detection-lifecycle` for detection rule development. Provide context: identified threat events, ATT&CK techniques, detection gaps, recommended detection approaches from the assessment. Redisplay menu.
- IF TH: Recommend operator invoke `spectra-threat-hunt` for proactive threat hunting. Provide context: identified threat sources, TTPs, hunt hypotheses derived from the risk assessment findings. Redisplay menu.
- IF user asks questions: Answer the question thoroughly with reference to the assessment data, then redisplay menu.

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- [F] Finalize is the ONLY option that ends the workflow — all other options return to this menu
- Do NOT auto-close the workflow — the operator must explicitly select [F] Finalize
- Do NOT present a [C] Continue option — this is the final step. There is no step 8.

## CRITICAL STEP COMPLETION NOTE

This is the FINAL step. When the operator selects [F] Finalize, the workflow is complete. The frontmatter should already be updated with this step added to stepsCompleted and assessment_status set to 'complete'. No further step files will be loaded. The risk assessment report at `{outputFile}` is the final deliverable.

The report is what SPECTRA delivers. It is what drives investment decisions, satisfies regulatory requirements, and improves the organization's security posture. Every finding must be traceable. Every recommendation must be actionable. Every assumption must be transparent. The quality of this report reflects the quality of the entire risk assessment effort.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Complete assessment data loaded and verified — all 6 prior steps confirmed in stepsCompleted
- Key assessment metrics compiled and verified with operator — asset counts, risk distribution, treatment coverage, FAIR ALE totals
- Executive summary (Section 7) generated in non-technical business language, reviewed and approved by operator
- Executive summary includes all 6 subsections: Assessment Overview (7.1), Key Findings (7.2), Risk Landscape Summary (7.3), Top Risks (7.4), Strategic Recommendations (7.5), Investment Priorities (7.6)
- Key findings translated to business language — quantified impact where possible, no jargon without explanation
- Top risks table populated with risk level, ALE (if FAIR), treatment strategy, owner, and timeline
- Strategic recommendations organized by priority tier (0-30 days, 30-90 days, 90-180 days) with expected risk reduction and cost
- Investment priorities include ROI analysis for FAIR-quantified risks with cost of inaction and treatment ROI
- All 7 appendices compiled (A: Methodology, B: Scales, C: FAIR Details, D: Risk Register, E: Control Mapping, F: Assumptions & Confidence, G: Glossary)
- Risk register in complete exportable format with all 21+ columns
- Control mapping references valid NIST 800-53, CIS Controls, and ISO 27001 control IDs
- Report quality assurance conducted — all sections checked for completeness, all quality criteria evaluated
- Section completeness audit passed — all 8 sections populated with substantive content
- Quality criteria audit passed — 17 criteria evaluated including consistency, traceability, accuracy, and completeness
- Confidence levels documented for all 8 assessment areas with basis, assumptions, and impact-if-wrong
- Overall assessment confidence level stated with rationale
- Communication plan defined for all stakeholder audiences with format, key messages, delivery method, and timeline
- Assessment maintenance plan established per NIST 800-30 Step 4 — 10 reassessment triggers defined with scope, timing, and responsible party
- Monitoring activities between assessments defined with frequency and ownership
- Chronicle documentation recommended with full context for archival
- Assessment formally closed with all frontmatter fields populated and consistent
- Final frontmatter consistency check passed — all fields verified against report body
- Closure summary presented with complete assessment metrics
- Next steps recommended based on specific assessment findings (compliance audit, detection lifecycle, threat hunt)
- Menu presented with correct options ([A]/[W]/[F] + [CH]/[CA]/[DL]/[TH]) — NO [C] Continue option
- Workflow terminates only when operator selects [F] Finalize

### ❌ SYSTEM FAILURE:

- Proceeding with reporting when prior steps are incomplete without warning the operator
- Generating an executive summary with technical jargon that non-technical leadership cannot understand
- Generating an executive summary that misrepresents, oversimplifies, or contradicts the analytical findings
- Key findings that are not traceable back through risk ratings to evidence
- Top risks table missing risk level, treatment strategy, owner, or timeline for any entry
- Strategic recommendations not organized by implementation priority (Immediate / Short-term / Medium-term)
- Investment priorities without ROI analysis when FAIR quantification was performed
- Appendices missing or incomplete — all 7 appendices (A-G) must be populated
- Risk register with missing columns or incomplete entries
- Control mapping with invalid or missing framework references
- Report sections left empty or with placeholder content ({{...}} patterns in the final document)
- Not conducting the report quality assurance audit — skipping the hard gate
- Quality criteria audit skipped or conducted superficially without checking each criterion
- Confidence levels not documented — presenting risk ratings without acknowledging uncertainty
- No communication plan — report exists but no plan to deliver it to stakeholders
- No maintenance plan — assessment is point-in-time with no plan for ongoing relevance
- Maintenance plan without defined triggers, timing, and responsible parties
- Re-opening risk calculations or modifying risk ratings in this step — analytical work is finalized in prior steps
- Changing treatment decisions in this step — treatment planning is finalized in step 6
- Closing the assessment with incomplete or inconsistent frontmatter
- Not recommending Chronicle for documentation archival
- Including a [C] Continue option in the menu — this is the FINAL step, there is no step 8
- Auto-closing the workflow without operator selecting [F] Finalize
- Proceeding without operator review and approval of the executive summary
- Not presenting cross-module recommendations (compliance audit, detection lifecycle, threat hunt) when findings warrant them
- Generating report content without operator input — the operator confirms, you facilitate

**Master Rule:** The report is the deliverable. An assessment without a clear, actionable, audience-tailored report is just intellectual exercise. Nobody funds treatment plans based on opinion — they fund them based on a defensible, well-documented risk assessment report that translates risk into business language, quantifies exposure where possible, acknowledges uncertainty honestly, and provides traceable recommendations with clear ownership and timelines. Make every finding traceable, every recommendation actionable, every assumption transparent. The quality of this report determines whether the assessment creates organizational impact or gathers dust. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
