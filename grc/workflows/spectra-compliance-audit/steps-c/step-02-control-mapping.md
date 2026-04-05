# Step 2: Control Mapping & Applicability

**Progress: Step 2 of 7** — Next: Evidence Collection & Validation

## STEP GOAL:

Enumerate the complete control set for the primary framework, determine applicability for each control (applicable or not-applicable with documented justification), build the formal Statement of Applicability (SoA), establish cross-framework mappings between the primary and all secondary frameworks to identify overlapping controls and evidence reuse opportunities, create the responsibility matrix assigning control owners/implementers/assessors, and document shared responsibility for cloud-hosted controls. This step transforms the abstract framework selection from Step 1 into a concrete, actionable audit work plan — every control that will be assessed, every control that is excluded, every cross-framework mapping that reduces duplicate effort, and every control owner who will be interviewed.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate control applicability determinations without operator input — applicability is an organizational decision, not an auditor decision
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read — "read fully and follow"
- 📋 YOU ARE A COMPLIANCE AUDIT FACILITATOR — you enumerate the controls and present the framework structure, the operator determines applicability based on organizational context
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Compliance Auditor — CISA, ISO 27001 Lead Auditor — you know every control in every major framework by number
- ✅ Reference framework requirements BY NUMBER — "ISO 27001:2022 Annex A 5.1 Policies for information security" not "the policy control"
- ✅ For ISO 27001:2022: You know the 93 Annex A controls organized into 4 themes (Organizational 5.1-5.37, People 6.1-6.8, Physical 7.1-7.14, Technological 8.1-8.34)
- ✅ For SOC 2: You know the Trust Service Criteria (CC1-CC9 Common Criteria, plus A1 Availability, C1 Confidentiality, PI1 Processing Integrity, P1 Privacy) with points of focus
- ✅ For PCI DSS v4.0: You know the 12 requirements and their sub-requirements, including the new v4.0 requirements with future-dated applicability
- ✅ For HIPAA: You know Administrative Safeguards (§164.308), Physical Safeguards (§164.310), Technical Safeguards (§164.312), and Organizational Requirements (§164.314)
- ✅ For NIST 800-53 Rev 5: You know the 20 control families (AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SC, SI, SR) and their control baselines (Low/Moderate/High)
- ✅ For NIST CSF 2.0: You know the 6 Functions (Govern, Identify, Protect, Detect, Respond, Recover) with their Categories and Subcategories
- ✅ For CIS Controls v8: You know the 18 controls and the Implementation Group model (IG1/IG2/IG3)
- ✅ The Statement of Applicability is a formal audit artifact — for ISO 27001, it is a mandatory certification document (Clause 6.1.3d). For PCI DSS, scope documentation is required by Requirement 12.5.2. Treat it with the rigor it deserves.

### Step-Specific Rules:

- 🎯 Focus exclusively on control enumeration, applicability determination, cross-framework mapping, and responsibility assignment — do NOT collect evidence, assess compliance, or identify gaps
- 🚫 FORBIDDEN to assess whether controls are compliant, partially compliant, or non-compliant in this step — that is step 04. This step determines WHAT will be assessed, not HOW controls are performing.
- 🚫 FORBIDDEN to collect or reference specific evidence artifacts — that is step 03. This step identifies which controls need evidence, not the evidence itself.
- 💬 Approach: systematic framework enumeration followed by collaborative applicability review — work through each control domain/theme with the operator
- 📊 For frameworks with large control sets (NIST 800-53: 1000+ controls, PCI DSS: 250+ sub-requirements), work at the domain/family level first to establish applicability boundaries, then detail individual controls within applicable domains
- 🔗 Cross-framework mapping is not optional when secondary frameworks are selected — it is the efficiency engine that justifies multi-framework audits

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your framework expertise drives the enumeration, the operator provides the organizational context for applicability
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Marking too many controls as N/A without adequate justification — explain certification risk: for ISO 27001:2022, Clause 6.1.3d requires that N/A determinations be justified and that the justification demonstrates why the control is not needed. Certification bodies will challenge broad N/A claims, especially for Technological controls (8.x) that apply to virtually all organizations with IT systems. A control marked N/A that later proves applicable creates a non-conformity.
  - Excluding controls related to in-scope data or processes — explain scope integrity risk: if the organization processes payment card data but marks PCI DSS Requirement 3 (Protect Stored Account Data) as N/A, the scope is inconsistent. Controls that apply to in-scope data flows cannot be excluded without removing the data flow from scope.
  - No cross-framework mapping when multiple frameworks are selected — explain efficiency loss risk: without mapping, the evidence collection in Step 3 will duplicate effort. The same access review evidence satisfies ISO 27001:2022 A.5.18, SOC 2 CC6.1, PCI DSS 7.2, HIPAA §164.312(a)(1), and NIST 800-53 AC-2/AC-3. Without mapping, you collect the same evidence five times.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Load output document and verify `step-01-init.md` in `stepsCompleted`
- 🎯 Load all scope data from Step 1: primary framework, secondary frameworks, scope systems, scope processes, scope locations, scope exclusions, audit type, audit approach
- ⚠️ Present [A]/[W]/[C] menu after SoA, cross-framework mapping, and responsibility matrix are all complete
- 💾 ONLY save to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of `stepsCompleted` and updating:
  - `total_controls_assessed`: total controls determined to be applicable (will be assessed in steps 3-4)
  - `controls_not_applicable`: count of controls marked N/A
  - `statement_of_applicability_complete: true`
  - `control_mapping_complete: true` (if secondary frameworks exist, includes cross-mapping)
  - `cross_framework_mappings`: count of cross-framework control mappings established
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Complete data from step 1: primary framework with version, secondary frameworks with versions, audit type, audit approach, scope systems, scope processes, scope locations, scope exclusions, audit limitations, engagement authorization boundaries
- Focus: Framework control enumeration, applicability determination (applicable/N-A with justification), Statement of Applicability creation, cross-framework mapping, responsibility matrix, shared responsibility model for cloud
- Limits: Do NOT assess compliance status (compliant/non-compliant — step 04), do NOT collect evidence (step 03), do NOT identify gaps or classify findings (step 04). This step builds the PLAN for what will be assessed.
- Dependencies: Primary and secondary framework selections from step 01, scope definition from step 01

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Audit Context

Load the output document and verify that step-01-init.md is in the stepsCompleted array. Extract all scope and framework data from Section 1.

"**Control Mapping — Loading Audit Context:**

I will load the audit scope and framework selection from Step 1 to build the control mapping work plan."

**Present Framework Summary:**

```
FRAMEWORK CONFIGURATION
Primary Framework: {{primary_framework}} ({{version}})
Secondary Frameworks: {{secondary_frameworks_list or 'None'}}
Audit Type: {{audit_type}}
Audit Approach: {{audit_approach}}

SCOPE SUMMARY
Systems: {{scope_systems_summary}}
Processes: {{scope_processes_summary}}
Locations: {{scope_locations_summary}}
Exclusions: {{scope_exclusions_summary}}
```

**Determine Control Set Size:**

Based on the primary framework, present the expected control set:

| Framework | Expected Control Set |
|-----------|---------------------|
| ISO 27001:2022 | 93 Annex A controls in 4 themes |
| SOC 2 TSC | CC1-CC9 + applicable category criteria (A1/C1/PI1/P1) with points of focus |
| PCI DSS v4.0 | 12 requirements, ~250 sub-requirements (varies by SAQ type for merchants) |
| HIPAA Security Rule | ~42 standards and implementation specifications across 3 safeguard categories |
| GDPR | ~40 auditable requirements across Articles 5-49 + Chapter V |
| NIST CSF 2.0 | 6 Functions, 22 Categories, 106 Subcategories |
| NIST 800-53 Rev 5 | 20 families, controls vary by baseline (Low ~130, Moderate ~325, High ~420) |
| CIS Controls v8 | 18 controls, 153 safeguards (IG1: 56, IG2: 74, IG3: 23 additional) |

"Based on {{primary_framework}}, we will enumerate {{expected_count}} controls. For large control sets, I will work at the domain/family level first and then detail individual controls within applicable domains.

Ready to begin control enumeration?"

### 2. Primary Framework Control Enumeration

Enumerate the complete control set for the primary framework. Work through each domain/theme/family systematically.

**Framework-Specific Enumeration Approach:**

#### IF ISO 27001:2022:

"**ISO 27001:2022 Annex A Control Enumeration**

The 93 Annex A controls are organized into 4 themes. We will work through each theme to determine applicability.

**Theme 1: Organizational Controls (A.5.1 — A.5.37) — 37 controls**

| Control ID | Control Title | Applicable? | Justification (if N/A) |
|-----------|--------------|-------------|----------------------|
| A.5.1 | Policies for information security | | |
| A.5.2 | Information security roles and responsibilities | | |
| A.5.3 | Segregation of duties | | |
| A.5.4 | Management responsibilities | | |
| A.5.5 | Contact with authorities | | |
| A.5.6 | Contact with special interest groups | | |
| A.5.7 | Threat intelligence | | |
| A.5.8 | Information security in project management | | |
| A.5.9 | Inventory of information and other associated assets | | |
| A.5.10 | Acceptable use of information and other associated assets | | |
| A.5.11 | Return of assets | | |
| A.5.12 | Classification of information | | |
| A.5.13 | Labelling of information | | |
| A.5.14 | Information transfer | | |
| A.5.15 | Access control | | |
| A.5.16 | Identity management | | |
| A.5.17 | Authentication information | | |
| A.5.18 | Access rights | | |
| A.5.19 | Information security in supplier relationships | | |
| A.5.20 | Addressing information security within supplier agreements | | |
| A.5.21 | Managing information security in the ICT supply chain | | |
| A.5.22 | Monitoring, review and change management of supplier services | | |
| A.5.23 | Information security for use of cloud services | | |
| A.5.24 | Information security incident management planning and preparation | | |
| A.5.25 | Assessment and decision on information security events | | |
| A.5.26 | Response to information security incidents | | |
| A.5.27 | Learning from information security incidents | | |
| A.5.28 | Collection of evidence | | |
| A.5.29 | Information security during disruption | | |
| A.5.30 | ICT readiness for business continuity | | |
| A.5.31 | Legal, statutory, regulatory and contractual requirements | | |
| A.5.32 | Intellectual property rights | | |
| A.5.33 | Protection of records | | |
| A.5.34 | Privacy and protection of PII | | |
| A.5.35 | Independent review of information security | | |
| A.5.36 | Compliance with policies, rules and standards for information security | | |
| A.5.37 | Documented operating procedures | | |

Let's review these Organizational controls. For each, determine:
- **Applicable**: The control is relevant to your ISMS scope
- **N/A**: The control is not applicable — you MUST provide justification per ISO 27001:2022 Clause 6.1.3d

We can work through these in batches. Which controls are clearly applicable, which are clearly N/A, and which need discussion?"

Continue with Theme 2 (People A.6.1-6.8), Theme 3 (Physical A.7.1-7.14), Theme 4 (Technological A.8.1-8.34) using the same format.

#### IF SOC 2 TSC:

"**SOC 2 Trust Service Criteria Enumeration**

SOC 2 uses Trust Service Criteria organized into Common Criteria (CC) and category-specific criteria. Determine which TSC categories are in scope based on the service and client requirements.

**Category Selection:**

| Category | Criteria | In Scope? | Rationale |
|----------|---------|-----------|-----------|
| **Security** (CC) | CC1-CC9 | Mandatory for all SOC 2 | Always in scope — CC1 (Control Environment), CC2 (Communication & Information), CC3 (Risk Assessment), CC4 (Monitoring), CC5 (Control Activities), CC6 (Logical & Physical Access), CC7 (System Operations), CC8 (Change Management), CC9 (Risk Mitigation) |
| **Availability** (A) | A1.1-A1.3 | | Include if availability commitments exist in SLAs |
| **Confidentiality** (C) | C1.1-C1.2 | | Include if confidential information is processed |
| **Processing Integrity** (PI) | PI1.1-PI1.5 | | Include if data processing accuracy matters |
| **Privacy** (P) | P1.0-P8.1 | | Include if personal information is processed |

Which categories are in scope? Then we will enumerate the specific criteria and points of focus for each."

Continue with criteria and points of focus enumeration.

#### IF PCI DSS v4.0:

Present the 12 requirements at the requirement level, then expand to sub-requirements for applicable requirements. Note future-dated requirements (those with effective dates after the current date).

#### IF HIPAA Security Rule:

Present Administrative (§164.308), Physical (§164.310), Technical (§164.312) safeguards with each standard and implementation specification marked as Required (R) or Addressable (A).

#### IF NIST 800-53 Rev 5:

Work at the family level first (20 families), determine which families are applicable, then enumerate individual controls within applicable families at the appropriate baseline (Low/Moderate/High).

#### IF NIST CSF 2.0:

Present the 6 Functions with Categories and Subcategories.

#### IF CIS Controls v8:

Present the 18 controls and determine the Implementation Group (IG1/IG2/IG3) based on organizational maturity. Enumerate safeguards for the selected IG.

#### IF GDPR:

Present the auditable articles with specific requirements.

**For ALL frameworks — work iteratively with the operator:**
- Present controls in manageable batches (by domain/theme/family)
- For each batch, ask the operator to confirm applicability
- For N/A determinations, require justification
- Flag any N/A determinations that seem inconsistent with the defined scope
- Continue until all controls are classified

### 3. Statement of Applicability

Once all controls are classified, compile the formal Statement of Applicability:

"**Statement of Applicability (SoA) — {{primary_framework}}**

**Summary:**

| Category | Count | Percentage |
|----------|-------|-----------|
| Total Controls | {{total}} | 100% |
| Applicable | {{applicable}} | {{%}} |
| Not Applicable | {{na}} | {{%}} |

**N/A Controls with Justification:**

| Control ID | Control Title | Justification | Risk Acceptance Required? |
|-----------|--------------|---------------|-------------------------|
| {{id}} | {{title}} | {{justification per framework requirements}} | {{Yes/No}} |

{{IF ISO 27001:2022}}: Per Clause 6.1.3d, every N/A determination must include a justification demonstrating that the control is not needed and that no applicable risk requires the control. Controls excluded must be documented in the SoA.
{{IF PCI DSS v4.0}}: Per Requirement 12.5.2, scope documentation must be reviewed and confirmed every 12 months and upon significant changes.
{{IF HIPAA}}: Addressable implementation specifications (A) must include a risk-based decision: implement as specified, implement an equivalent alternative, or document why the specification is not reasonable and appropriate.

Does this Statement of Applicability accurately reflect your organization's compliance scope? Any adjustments needed before we finalize?"

Wait for operator confirmation.

### 4. Cross-Framework Mapping

**If secondary frameworks were selected in Step 1:**

Build the cross-framework mapping between the primary framework and each secondary framework.

"**Cross-Framework Control Mapping**

Mapping {{primary_framework}} controls to {{secondary_frameworks_list}}. This mapping identifies:
1. **Direct mappings** — controls that have a clear one-to-one or one-to-many equivalent across frameworks
2. **Partial mappings** — controls that overlap but do not fully satisfy each other
3. **Unique controls** — controls in one framework with no equivalent in the other

**Mapping Table:**

| Primary: {{primary}} Control ID | Primary Control Title | {{Secondary 1}} Control | Mapping Type | Notes |
|-------------------------------|---------------------|------------------------|-------------|-------|
| {{id}} | {{title}} | {{secondary_id}} | Direct / Partial / Unique | {{mapping notes}} |

**Cross-Framework Mapping Summary:**

| Mapping Metric | Value |
|---------------|-------|
| Total primary controls (applicable) | {{count}} |
| Controls with direct secondary mapping | {{count}} ({{%}}) |
| Controls with partial secondary mapping | {{count}} ({{%}}) |
| Controls unique to primary (no secondary equivalent) | {{count}} ({{%}}) |
| Secondary controls unique (no primary equivalent) | {{count}} ({{%}}) |
| Total cross-framework mappings | {{count}} |
| Estimated evidence reuse potential | {{%}} |

**Evidence Reuse Opportunities:**

The following evidence artifacts can satisfy requirements across multiple frameworks simultaneously:

| Evidence Type | Primary Control(s) | Secondary Control(s) | Frameworks Satisfied |
|--------------|-------------------|---------------------|---------------------|
| Access control policy | {{primary_ids}} | {{secondary_ids}} | {{framework_list}} |
| Change management procedure | {{primary_ids}} | {{secondary_ids}} | {{framework_list}} |
| Incident response plan | {{primary_ids}} | {{secondary_ids}} | {{framework_list}} |
| Vulnerability scan results | {{primary_ids}} | {{secondary_ids}} | {{framework_list}} |
| ... | ... | ... | ... |

This mapping will be used in Step 3 to optimize evidence collection — one evidence artifact can be collected once and mapped to multiple controls across frameworks."

**If NO secondary frameworks were selected:**

"**Cross-Framework Mapping: Not Applicable**

No secondary frameworks were selected in Step 1. Cross-framework mapping is not required for single-framework audits. If the operator wants to add cross-mapping later, secondary frameworks can be added and this section revisited."

### 5. Responsibility Matrix

Build the responsibility matrix assigning control owners, implementers, and assessors for each applicable control.

"**Control Responsibility Matrix**

For each applicable control, identify:
- **Control Owner**: Person or role responsible for the control's existence and effectiveness
- **Implementer**: Person or team responsible for operating the control day-to-day
- **Assessor**: Person who will be interviewed or who provides evidence for the control assessment
- **Shared Responsibility Notes**: For cloud-hosted controls, who is responsible — the Cloud Service Provider (CSP) or the customer?

| Control ID | Control Title | Owner | Implementer | Assessor | Shared Responsibility |
|-----------|--------------|-------|-------------|---------|----------------------|
| {{id}} | {{title}} | {{owner}} | {{implementer}} | {{assessor}} | {{CSP/Customer/Shared/N-A}} |

**Cloud Shared Responsibility Model:**

{{IF cloud platforms in scope:}}

For controls implemented on cloud platforms ({{cloud_platforms_from_scope}}), the shared responsibility model applies:

| Control Area | IaaS (Customer Responsibility) | PaaS (Shared) | SaaS (CSP Responsibility) |
|-------------|-------------------------------|---------------|--------------------------|
| Physical security | CSP | CSP | CSP |
| Network infrastructure | CSP | CSP | CSP |
| Virtualization/hypervisor | CSP | CSP | CSP |
| Operating system | Customer | Shared (CSP patches, customer configures) | CSP |
| Application | Customer | Customer | CSP |
| Data classification & encryption | Customer | Customer | Customer |
| Identity & access management | Customer | Customer | Shared |
| Security monitoring | Customer | Shared | Shared |
| Compliance configuration | Customer | Customer | Customer |

For each control hosted in cloud:
- If CSP-managed: request CSP's SOC 2 Type II report, ISO 27001 certificate, or other independent attestation as evidence
- If customer-managed: evidence must come from the organization's own configuration and operations
- If shared: evidence from both CSP attestation AND customer configuration is required

Let's walk through the responsibility assignments for your applicable controls. We can work by domain/theme to be efficient."

Wait for operator input on ownership assignments. Iterate until complete.

### 6. Control Mapping Summary & Work Plan

Present the complete control mapping summary and the audit work plan derived from it:

"**Control Mapping Complete — Audit Work Plan**

**Statement of Applicability Summary:**

| Metric | Value |
|--------|-------|
| Primary Framework | {{primary_framework}} |
| Total Controls | {{total}} |
| Applicable Controls | {{applicable}} |
| Not Applicable (with justification) | {{na}} |
| Cross-Framework Mappings | {{mappings_count}} |
| Evidence Reuse Opportunities | {{reuse_count}} |
| Control Owners Identified | {{unique_owners}} |

**Audit Work Plan — Evidence Collection Preview:**

Based on the applicable controls and responsibility matrix, the evidence collection in Step 3 will require:

| Evidence Category | Estimated Items | Control Coverage |
|-------------------|-----------------|-----------------|
| Documentary (policies, procedures, records) | {{estimate}} | {{control_count}} controls |
| Technical (configs, scans, logs, reports) | {{estimate}} | {{control_count}} controls |
| Interview (control owners, process owners) | {{estimate}} interviewees | {{control_count}} controls |
| Observation (walkthroughs, process observation) | {{estimate}} observations | {{control_count}} controls |

**Total evidence items to collect (estimated):** {{total_estimate}}
**Evidence items reusable across frameworks:** {{reuse_estimate}} ({{reuse_percentage}}% reduction in collection effort)

**Key Control Owners to Engage:**

| Owner/Role | Controls Owned | Interview Priority |
|-----------|---------------|-------------------|
| {{owner}} | {{count}} controls | {{High/Medium/Low}} |

This establishes the audit work plan. We are ready to proceed to evidence collection where we will systematically collect, catalog, and validate evidence against every applicable control."

### 7. Present MENU OPTIONS

Display menu after control mapping summary:

"**Select an option:**
[A] Advanced Elicitation — Push deeper on N/A justifications, cross-framework mapping completeness, responsibility assignments, and shared responsibility model accuracy
[W] War Room — Launch multi-agent adversarial discussion on the Statement of Applicability: challenge N/A determinations, probe for missing cross-framework mappings, stress-test ownership assignments against certification body expectations
[C] Continue — Save and proceed to Step 3: Evidence Collection & Validation (Step 3 of 7)"

#### Menu Handling Logic:

- IF A: Invoke advanced elicitation on SoA, cross-framework mapping, and responsibility matrix. Challenge N/A determinations (would a certification body accept this justification?), probe cross-framework mapping for missed overlaps, verify responsibility assignments (is the named owner actually accountable?), test shared responsibility model against cloud platform documentation. Process insights, ask operator if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke spectra-war-room with SoA and control mapping as context. Auditor perspective: which N/A determinations would a certification auditor challenge? Where are the weakest justifications? Red perspective: which excluded controls create exploitable gaps? Blue perspective: is the responsibility matrix realistic — will the named owners actually be available for interviews and evidence provision? Summarize insights, ask operator if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding `step-02-control-mapping.md` to the end of `stepsCompleted` array and updating `total_controls_assessed`, `controls_not_applicable`, `statement_of_applicability_complete`, `control_mapping_complete`, `cross_framework_mappings` fields, then read fully and follow: `./step-03-evidence.md`
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer based on framework expertise and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, total_controls_assessed populated, controls_not_applicable counted, statement_of_applicability_complete set to true, control_mapping_complete set to true, cross_framework_mappings counted, and Section 2 (Framework Control Mapping & Statement of Applicability) fully populated with SoA, cross-framework mapping, and responsibility matrix], will you then read fully and follow: `./step-03-evidence.md` to begin evidence collection and validation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Audit context loaded from Step 1 with framework and scope data verified
- Complete control set enumerated for the primary framework with correct version-specific controls
- Applicability determination completed for every control with operator input
- N/A determinations include documented justification per framework requirements (ISO 27001 Clause 6.1.3d, PCI DSS 12.5.2, etc.)
- Statement of Applicability formally compiled with summary statistics
- Cross-framework mapping completed (if secondary frameworks selected) with direct/partial/unique classification
- Evidence reuse opportunities identified from cross-framework mapping
- Responsibility matrix completed with owner/implementer/assessor for every applicable control
- Shared responsibility model documented for cloud-hosted controls
- Audit work plan derived from control mapping with evidence collection estimates
- Frontmatter updated with control counts, SoA status, mapping status, and cross-framework mapping count
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Assessing compliance status (compliant/non-compliant) during control mapping — that is step 04
- Collecting evidence or referencing specific evidence artifacts — that is step 03
- Generating applicability determinations without operator input
- Accepting N/A determinations without justification
- Not enumerating the complete control set for the primary framework
- Missing cross-framework mapping when secondary frameworks were selected
- Not building the responsibility matrix with ownership assignments
- Not documenting shared responsibility for cloud-hosted controls
- Proceeding to evidence collection with an incomplete or unconfirmed SoA
- Not updating frontmatter with control counts and SoA/mapping completion status
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** The Statement of Applicability is the foundation of the compliance audit — it defines what will be assessed and what is excluded. An incomplete SoA produces an incomplete audit. An SoA without justified N/A determinations will be challenged by certification bodies. A control mapping without cross-framework efficiency analysis wastes organizational time and budget. Get the map right before starting the journey. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
