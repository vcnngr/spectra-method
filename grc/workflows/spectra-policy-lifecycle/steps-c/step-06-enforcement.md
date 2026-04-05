# Step 6: Enforcement & Exception Management

**Progress: Step 6 of 7** — Next: Review, Maintenance & Closure

## STEP GOAL:

Design and document the complete enforcement ecosystem for the approved policy — automated controls (DLP, firewall, IAM, CASB, endpoint), manual controls (periodic reviews, certifications, audits), detective controls (monitoring, alerting, reporting), corrective controls (incident response for violations), compliance monitoring with KPIs and dashboards, the exception management lifecycle (request, risk assessment, approval, monitoring, renewal), and the violation handling framework (classification, response, HR partnership, documentation, lessons learned). Enforcement without design is ad hoc; enforcement without measurement is invisible. This step ensures every policy requirement has a compliance path and every deviation has a response path.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER define enforcement actions or violation responses without operator input and validation
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read — "read fully and follow"
- 📋 YOU ARE AN ENFORCEMENT DESIGN FACILITATOR, not an enforcement authority — the operator defines acceptable enforcement mechanisms, the organization's HR policies govern violation handling, and you provide the structured framework
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Scribe, a Policy Author designing the enforcement and exception management framework
- ✅ Enforcement is the credibility test — a policy with no enforcement mechanism is a suggestion, and the organization will treat it as one. Every requirement must have at least one enforcement mechanism.
- ✅ Automated enforcement is preferred over manual enforcement — humans forget, skip steps, and get busy. Automated controls are consistent, tireless, and auditable.
- ✅ Exception management is not a loophole — it is a pressure valve that prevents shadow compliance (informal workarounds that are invisible and unmanaged). A well-designed exception process with risk assessment, compensating controls, and time limits is better governance than rigid rules that everyone circumvents.
- ✅ Violation handling must be proportionate, documented, and consistent — disproportionate responses create resentment and avoidance, inconsistent responses create legal liability, and undocumented responses create audit exposure.
- ✅ Enforcement must be designed with HR — disciplinary action clauses must align with employment law, HR policies, and collective bargaining agreements

### Step-Specific Rules:

- 🎯 Focus on enforcement mechanism design, compliance monitoring, exception management, and violation handling
- 🚫 FORBIDDEN to modify policy requirements, standards, or procedures — those were finalized in Steps 3-5
- 🚫 FORBIDDEN to finalize the lifecycle report, set review schedules, or close the engagement — those are Step 7
- 💬 Approach: structured enforcement design with operator collaboration — present enforcement options, assess feasibility with available technology, design monitoring, build exception workflows
- 🔄 Cross-reference the technology context from Step 2 (enforcement feasibility) and the requirements from Step 3 (what must be enforced)
- 📊 Every enforcement mechanism must map to a specific policy requirement — no orphan controls and no unmonitored requirements
- ⏱️ Enforcement mechanisms must be implementable within the timeline established in Step 5

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your enforcement design expertise ensures every requirement has a compliance path. The operator decides what is feasible, proportionate, and appropriate for their organization.
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Requirements with no enforcement mechanism assigned — explain paper tiger risk: every requirement without an enforcement mechanism is a requirement that exists only on paper. When auditors ask "how do you enforce Requirement X?" the answer cannot be "we hope people comply." Without enforcement, compliance rates will decline steadily over time as organizational attention shifts.
  - Enforcement relies entirely on manual processes — explain enforcement fatigue risk: manual enforcement (quarterly access reviews, manual log reviews, periodic certifications) depends on human discipline, which erodes over time. Start with automated enforcement where possible, use manual processes for what cannot be automated, and plan a roadmap to automate manual processes.
  - Exception process has no time limit — explain permanent exception risk: exceptions without expiration dates become permanent deviations that are never revisited. Every exception must have a maximum duration and a mandatory renewal review. Organizations that allow permanent exceptions accumulate risk silently.
  - Violation response is disproportionate — explain organizational trust risk: if the response to a first-time inadvertent violation is the same as the response to willful circumvention, the enforcement framework is perceived as punitive rather than educational. Proportionate response builds trust and encourages self-reporting.
  - No compliance metrics defined — explain invisible enforcement risk: if you cannot measure compliance, you cannot demonstrate it. Auditors, regulators, and executives need evidence that the policy is being followed. Compliance without metrics is faith-based governance.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks. The operator decides, you facilitate.

## EXECUTION PROTOCOLS:

- 🎯 Load output document from `{outputFile}`, verify that `step-05-approval.md` is present in the `stepsCompleted` array
- 🎯 Load the policy requirements (Step 3), enforcement feasibility assessment (Step 2), and technology context (Step 2)
- 💾 Update output document Section 6 (Compliance & Enforcement) and Section 7 (Exceptions Process) with detailed content
- 💾 Update frontmatter when enforcement design is complete:
  - `enforcement_mechanisms`: total count of enforcement mechanisms defined
  - `automated_controls`: count of automated enforcement mechanisms
  - `manual_controls`: count of manual enforcement mechanisms
  - `detective_controls`: count of detective mechanisms
  - `corrective_controls`: count of corrective mechanisms
  - `compliance_kpis`: count of KPIs defined
  - `exception_process_defined: true`
  - `violation_framework_defined: true`
- Update frontmatter: add this step name to the end of the `stepsCompleted` array
- 🚫 FORBIDDEN to load next step until user selects [C]

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md, engagement.yaml, Steps 1-5 output (policy scope, research findings including enforcement feasibility, complete policy draft, review results, approval record, awareness plan)
- Focus: Enforcement mechanism design, compliance monitoring with KPIs, exception management lifecycle, violation handling framework, HR partnership for disciplinary action
- Limits: Do not modify policy requirements (Steps 3-5). Do not finalize lifecycle reporting, set review schedules, or close the engagement (Step 7). Do not load future step files.
- Dependencies: Step 5 (approval) must be complete — the approved policy with its requirements is the input. Step 2 (research) provides the enforcement feasibility context.

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Enforcement Mapping

Map every policy requirement to enforcement mechanisms:

"**Enforcement Design Phase — Requirement Mapping**

Every requirement in the approved {{policy_type}} must have at least one enforcement mechanism. Let's map them:

**Requirement-to-Enforcement Matrix:**

| Req ID | Requirement Summary | Automated? | Manual? | Detective? | Corrective? | Current Coverage | Gap |
|--------|-------------------|-----------|---------|-----------|------------|-----------------|-----|
| PS-01 | {{statement}} | {{Y/N — tool}} | {{Y/N — process}} | {{Y/N — monitoring}} | {{Y/N — response}} | Full/Partial/None | {{gap}} |
| STD-01 | {{requirement}} | | | | | | |
| STD-02 | {{requirement}} | | | | | | |
| PRC-01 | {{procedure}} | | | | | | |

**Enforcement Coverage Summary:**

| Category | Count | Percentage |
|----------|-------|-----------|
| Fully enforced (automated + detective) | {{count}} | {{%}} |
| Partially enforced (manual or detective only) | {{count}} | {{%}} |
| Not yet enforced | {{count}} | {{%}} |
| **Total requirements** | **{{total}}** | **100%** |

Requirements with no enforcement mechanism are the highest priority for this step.

Review the requirement-to-enforcement mapping. Is the coverage assessment accurate?"

Wait for operator input.

### 2. Automated Enforcement Mechanisms

"**Automated Enforcement Design**

Automated controls are the gold standard — consistent, tireless, auditable. For each requirement that can be automated:

**Automated Control Inventory:**

| # | Requirement | Control Type | Technology/Tool | Configuration | Owner | Implementation Status |
|---|------------|-------------|----------------|---------------|-------|--------------------|
| 1 | STD-## | Preventive | {{tool — e.g., IAM, DLP, Firewall}} | {{specific config — e.g., MFA required for all admin accounts}} | {{owner}} | Planned/In Progress/Active |
| 2 | STD-## | Detective | {{tool — e.g., SIEM, EDR, CASB}} | {{specific config — e.g., alert on privilege escalation}} | {{owner}} | |
| 3 | STD-## | Corrective | {{tool — e.g., SOAR, automated response}} | {{specific config — e.g., auto-lock after 5 failed attempts}} | {{owner}} | |

**Automated Control Categories:**

| Category | Purpose | Examples | Policy Applicability |
|----------|---------|---------|---------------------|
| **Identity & Access Management (IAM)** | Enforce access controls | MFA enforcement, RBAC, privileged access, session timeout, password policies | Access control, authentication requirements |
| **Data Loss Prevention (DLP)** | Prevent unauthorized data movement | Content inspection, endpoint DLP, cloud DLP, email DLP | Data handling, classification, transfer requirements |
| **Firewall/IPS** | Network-level enforcement | Allow/deny rules, IPS signatures, geo-blocking | Network security requirements |
| **CASB** | Cloud application control | Shadow IT detection, sanctioned app enforcement, DLP for SaaS | Cloud security, SaaS governance |
| **Endpoint Protection (EDR)** | Endpoint-level enforcement | Application control, device control, encryption enforcement | Endpoint security, device management |
| **Email Security** | Communication enforcement | Phishing protection, attachment filtering, encryption enforcement | Email security, communication requirements |
| **Configuration Management** | Baseline enforcement | Hardening standards, patch management, compliance scanning | System configuration, hardening requirements |

For each automated control, provide:
1. The specific tool/platform that will enforce it
2. The exact configuration needed
3. Who owns the configuration
4. Timeline for implementation (if not already active)

Share your automated enforcement capabilities for the requirements identified."

Wait for operator input. Record automated controls.

### 3. Manual & Detective Controls

"**Manual & Detective Control Design**

For requirements that cannot be fully automated, design manual and detective controls:

**Manual Controls:**

| # | Requirement | Control Activity | Frequency | Responsible | Evidence/Artifact | Time Estimate |
|---|------------|-----------------|-----------|-------------|-------------------|--------------|
| 1 | STD-## | {{activity — e.g., quarterly access review}} | {{frequency}} | {{role}} | {{evidence — e.g., signed review form}} | {{hours per cycle}} |
| 2 | STD-## | {{activity — e.g., annual policy acknowledgment}} | | | | |
| 3 | STD-## | {{activity — e.g., configuration audit}} | | | | |

**Detective Controls:**

| # | Requirement | Monitoring Method | Tool | Alert Condition | Response | Owner |
|---|------------|-------------------|------|----------------|----------|-------|
| 1 | STD-## | {{method — e.g., SIEM correlation rule}} | {{SIEM/EDR/CASB}} | {{what triggers alert}} | {{initial response}} | {{owner}} |
| 2 | STD-## | {{method — e.g., periodic compliance scan}} | {{scanner}} | {{threshold for alert}} | {{response}} | {{owner}} |
| 3 | STD-## | {{method — e.g., user behavior analytics}} | {{UBA tool}} | {{anomaly threshold}} | {{response}} | {{owner}} |

**Manual-to-Automated Roadmap:**

For manual controls, identify opportunities to automate in the future:

| # | Current Manual Control | Automation Opportunity | Tool Required | Estimated Timeline | Priority |
|---|----------------------|----------------------|---------------|-------------------|----------|
| 1 | {{manual control}} | {{how to automate}} | {{tool}} | {{timeline}} | H/M/L |

Review the manual and detective controls. Are these operationally feasible?"

Wait for operator input.

### 4. Compliance Monitoring & KPIs

"**Compliance Monitoring Design**

If you cannot measure compliance, you cannot demonstrate it. Define the key performance indicators for this {{policy_type}}:

**Compliance KPIs:**

| # | KPI | Target | Measurement Method | Data Source | Frequency | Owner | Dashboard |
|---|-----|--------|-------------------|-------------|-----------|-------|-----------|
| 1 | **Compliance rate** | {{target — e.g., 95%}} | {{how measured}} | {{data source}} | {{frequency}} | {{owner}} | {{yes/no}} |
| 2 | **Exception rate** | {{target — e.g., <5%}} | Active exceptions / total in scope | Exception register | Monthly | Policy Owner | Yes |
| 3 | **Violation rate** | {{target — e.g., <2%}} | Violations detected / total in scope | Enforcement tools + reports | Monthly | Compliance Monitor | Yes |
| 4 | **Training completion** | {{target — e.g., 100% within 30 days}} | Completed / assigned | LMS | Quarterly | Training Coordinator | Yes |
| 5 | **Acknowledgment rate** | {{target — e.g., 100% within 14 days}} | Acknowledged / distributed | LMS / GRC tool | Monthly | Policy Author | Yes |
| 6 | **Time to remediate** | {{target — e.g., <30 days for major}} | Days from detection to resolution | Incident tracking | Quarterly | Compliance Monitor | Yes |
| 7 | **Audit finding rate** | {{target — e.g., 0 critical findings}} | Findings per audit cycle | Audit reports | Per audit | Policy Owner | Yes |

**Non-Compliance Escalation:**

| Threshold | Trigger | Escalation | Action |
|-----------|---------|-----------|--------|
| Compliance rate < {{threshold_1}} | Monthly KPI review | Policy Owner | Investigation, remediation plan |
| Compliance rate < {{threshold_2}} | Monthly KPI review | CISO | Root cause analysis, executive briefing |
| Exception rate > {{threshold}} | Monthly KPI review | Policy Owner | Exception review, process assessment |
| Repeat violation | Per occurrence | Manager + HR | Progressive discipline per violation framework |
| Systematic non-compliance | Pattern analysis | CISO + Business Unit Head | Organizational intervention, training, control redesign |

**Compliance Dashboard:**

| Section | Content | Audience | Refresh |
|---------|---------|----------|---------|
| Executive summary | Overall compliance rate, trend, top issues | CISO / Board | Monthly |
| Department breakdown | Per-department compliance metrics | Department heads | Monthly |
| Exception register | Active exceptions, expiring soon, overdue | Policy Owner | Weekly |
| Violation log | Recent violations, trends, repeat offenders | Compliance Monitor | Real-time |
| Audit status | Upcoming audits, recent findings, remediation | Compliance team | Quarterly |

Review the compliance monitoring framework. Are the KPI targets appropriate? Any metrics to add or adjust?"

Wait for operator input and iterate.

### 5. Exception Management Design

"**Exception Management Lifecycle**

The exception process must be formal, risk-assessed, time-limited, and auditable. Informal exceptions are invisible risks.

**Exception Request Workflow:**

```
Requestor identifies need for exception
    |
    v
Submit exception request (Section 7 template)
    |
    v
Policy Owner / Delegate reviews request
    |
    v
Risk assessment of exception
    ├── Risk Level: Low → Policy Owner approves (max 12 months)
    ├── Risk Level: Medium → Policy Owner + Security review (max 6 months)
    ├── Risk Level: High → CISO approves (max 3 months)
    └── Risk Level: Critical → CISO + Board notification (max 1 month)
    |
    v
Compensating controls validated
    |
    v
Exception registered with:
    - Exception ID (EXC-{policy_id}-{sequence})
    - Requestor, approver, risk level
    - Compensating controls
    - Expiry date
    - Renewal requirements
    |
    v
Monitoring: compensating controls verified periodically
    |
    v
Before expiry:
    ├── Renewed (new risk assessment required)
    └── Closed (return to compliance or risk accepted)
```

**Exception Register Structure:**

| Field | Description | Required? |
|-------|-------------|-----------|
| Exception ID | EXC-{policy_id}-{NNN} | Auto-generated |
| Requestor | Name, role, department | Yes |
| Request Date | Date of submission | Auto-generated |
| Requirement | Specific REQ-##/STD-## | Yes |
| Business Justification | Why exception is needed | Yes |
| Risk Assessment | Risk level (L/M/H/C) with rationale | Yes |
| Compensating Controls | Alternative controls in place | Yes |
| Approval Authority | Who approved | Yes |
| Approval Date | When approved | Yes |
| Expiry Date | When exception expires | Yes |
| Renewal Review Date | 30 days before expiry | Auto-calculated |
| Monitoring Frequency | How often compensating controls are verified | Based on risk level |
| Status | Active / Expired / Renewed / Closed | Tracked |

**Exception Metrics:**

| Metric | Target | Purpose |
|--------|--------|---------|
| Active exceptions | < {{threshold}} | Indicates policy feasibility |
| Average exception duration | < {{threshold}} months | Indicates permanent deviation risk |
| Exception renewal rate | < {{threshold}}% | Indicates systemic issues |
| Exceptions by requirement | Distribution analysis | Identifies problematic requirements |
| Compensating control effectiveness | 100% verified | Validates risk management |

Review the exception management design. Is the workflow appropriate? Are the approval authorities correct?"

Wait for operator input and iterate.

### 6. Violation Handling Framework

"**Violation Handling Framework**

Violations must be classified, investigated, and responded to proportionately. This framework must align with HR policies and employment law.

**Violation Classification:**

| Category | Description | Examples | Typical Response | HR Involvement |
|----------|-------------|---------|-----------------|----------------|
| **Inadvertent** | Unintentional non-compliance, first occurrence, no malicious intent | Forgot to lock screen, sent unencrypted email by mistake, used personal device for one meeting | Education and awareness — verbal counseling, targeted training | Notification only |
| **Negligent** | Non-compliance due to carelessness, repeated minor violations, or failure to complete required training | Repeatedly failed to patch systems, skipped access reviews, ignored training deadlines | Written warning, mandatory training, increased monitoring | HR consulted |
| **Willful** | Deliberate circumvention of known policy requirements for convenience or expediency | Shared credentials to avoid MFA, disabled security controls, used unauthorized cloud services intentionally | Formal disciplinary action per HR policy, access review, monitoring | HR partnership required |
| **Malicious** | Intentional violation with harmful intent to the organization or others | Data theft, sabotage, unauthorized access for personal gain, deliberate destruction | Immediate access suspension, investigation, potential termination, legal action | HR + Legal + Management |

**Violation Response Process:**

```
Violation detected (automated alert, manual report, audit finding)
    |
    v
Initial classification (inadvertent/negligent/willful/malicious)
    |
    v
Investigation (scope, impact, intent, history)
    |
    v
Response determination (per classification above)
    |
    v
Documentation (violation record, investigation notes, response taken)
    |
    v
Remediation (close the gap that allowed the violation)
    |
    v
Follow-up (verify remediation, monitor for recurrence)
    |
    v
Lessons learned (update training, controls, or policy if systemic)
```

**Repeat Offender Management:**

| Occurrence | Classification | Escalated Response |
|-----------|---------------|-------------------|
| 1st | Inadvertent | Education and counseling |
| 2nd | Negligent (pattern) | Written warning, mandatory training |
| 3rd | Negligent (persistent) | Formal disciplinary action, access review |
| 4th+ | Willful (demonstrated disregard) | Severe disciplinary action per HR policy |

**Documentation Requirements:**

Every violation must be documented with:
- Date and time of detection
- How detected (automated/manual/audit/report)
- Description of the violation and affected requirement
- Classification with rationale
- Investigation summary
- Response taken
- Remediation actions
- Follow-up verification

**HR Partnership:**

| Violation Category | HR Role | Manager Role | Security Role |
|-------------------|---------|-------------|--------------|
| Inadvertent | Notified | Counsels employee | Provides context |
| Negligent | Consulted, reviews response | Delivers warning | Recommends training |
| Willful | Partners on disciplinary | Delivers action | Provides evidence |
| Malicious | Leads HR process | Supports investigation | Leads technical investigation |

**Legal Considerations:**
- All violation responses must be consistent across similar circumstances (avoid discrimination claims)
- Documentation must be factual and objective (avoid subjective characterizations)
- Employee rights must be respected (right to respond, union representation if applicable)
- Privacy laws must be observed during investigation (data protection, monitoring laws)

Review the violation handling framework. Does it align with your HR policies and organizational culture?"

Wait for operator input and iterate.

### 7. Update Output Document

Update the output document with detailed enforcement content:

- Expand Section 6 (Compliance & Enforcement) with:
  - Requirement-to-enforcement matrix
  - Automated, manual, and detective control details
  - Compliance KPIs with targets
  - Non-compliance escalation framework
  - Violation classification and response process
- Expand Section 7 (Exceptions Process) with:
  - Complete exception request workflow
  - Exception register structure
  - Exception metrics

Update frontmatter:
- `enforcement_mechanisms`: total count
- `automated_controls`: count
- `manual_controls`: count
- `detective_controls`: count
- `corrective_controls`: count
- `compliance_kpis`: count
- `exception_process_defined: true`
- `violation_framework_defined: true`

### 8. Present MENU OPTIONS

Display menu after enforcement design:

"**Select an option:**
[A] Advanced Elicitation — Push deeper on enforcement gaps, exception process robustness, violation proportionality, and KPI coverage
[W] War Room — Launch multi-agent adversarial discussion on enforcement design: Red challenges enforcement gaps and circumvention vectors, Blue validates monitoring coverage and response adequacy
[C] Continue — Save and proceed to Step 7: Review, Maintenance & Closure (Final Step)"

#### Menu Handling Logic:

- IF A: Invoke advanced elicitation on enforcement completeness. Challenge enforcement gaps (which requirements still have no mechanism?), probe exception process (can it be gamed? are compensating controls validated?), test violation proportionality (would employees perceive this as fair?), verify KPI coverage (can every metric be measured with available tools?). Process insights, update design if accepted, redisplay menu
- IF W: Invoke spectra-war-room with enforcement design as context. Red perspective: how would someone circumvent each enforcement mechanism? Where are the blind spots? Which exceptions would accumulate into permanent risk? Blue perspective: is the monitoring comprehensive? Are the KPIs actionable? Is the violation framework legally defensible? Summarize insights, ask operator if they want to adjust, redisplay menu
- IF C: Update output file frontmatter adding `step-06-enforcement.md` to the end of `stepsCompleted` array, then read fully and follow: `./step-07-reporting.md`
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer based on enforcement design expertise and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, enforcement_mechanisms populated, automated_controls counted, manual_controls counted, detective_controls counted, corrective_controls counted, compliance_kpis defined, exception_process_defined set to true, violation_framework_defined set to true, and output document Sections 6 and 7 fully expanded with enforcement details], will you then read fully and follow: `./step-07-reporting.md` to begin review, maintenance, and closure.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Step 5 completion verified before proceeding
- Every policy requirement mapped to at least one enforcement mechanism
- Automated controls designed with specific tools, configurations, and owners
- Manual controls designed with frequency, evidence, and time estimates
- Detective controls designed with monitoring methods, alert conditions, and responses
- Compliance KPIs defined with targets, measurement methods, and owners
- Non-compliance escalation framework established with thresholds
- Exception management lifecycle designed with workflow, register, and metrics
- Violation classification created with proportionate responses per category
- Repeat offender management defined with escalation path
- HR partnership roles defined for each violation category
- Documentation requirements established for violations
- Output document Sections 6 and 7 fully expanded
- Frontmatter updated with all enforcement counts and flags

### SYSTEM FAILURE:

- Proceeding without verifying Step 5 completion
- Leaving any requirement without an enforcement mechanism
- Defining enforcement actions without operator validation
- Not designing compliance KPIs (invisible enforcement)
- Not creating a formal exception process (forcing shadow compliance)
- Creating disproportionate violation responses
- Not involving HR in violation handling framework design
- Modifying policy requirements at this stage (return to Steps 3-5 for changes)
- Finalizing lifecycle reporting or closing the engagement — that is Step 7
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with enforcement counts and process flags

**Master Rule:** Enforcement is where policy meets reality. A policy without enforcement is a suggestion. A policy with disproportionate enforcement is resented. A policy with invisible enforcement is untestable. Design enforcement that is automated where possible, proportionate always, and measured consistently. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
