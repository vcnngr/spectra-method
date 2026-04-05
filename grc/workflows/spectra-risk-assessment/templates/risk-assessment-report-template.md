---
stepsCompleted: []
inputDocuments: []
workflowType: 'risk-assessment'
engagement_id: '{{engagement_id}}'
engagement_name: '{{engagement_name}}'
assessment_id: ''
assessment_status: 'open'
assessment_approach: ''
risk_model: ''
risk_appetite: ''
assessment_scope: ''
stakeholders_identified: 0
total_assets_inventoried: 0
crown_jewels_identified: 0
asset_tiers: ''
dependency_maps_created: 0
total_asset_value: ''
threat_sources_identified: 0
threat_events_mapped: 0
adversarial_sources: 0
non_adversarial_sources: 0
mitre_techniques_mapped: []
relevance_ratings_complete: false
vulnerabilities_identified: 0
predisposing_conditions: 0
controls_assessed: 0
control_gaps_identified: 0
total_risks_calculated: 0
risks_very_high: 0
risks_high: 0
risks_moderate: 0
risks_low: 0
risks_very_low: 0
fair_analyses_completed: 0
total_ale: ''
risk_register_populated: false
heat_map_generated: false
risks_with_treatment: 0
treatment_accept: 0
treatment_mitigate: 0
treatment_transfer: 0
treatment_avoid: 0
residual_risks_calculated: false
treatment_roadmap_created: false
executive_summary_complete: false
report_finalized: false
chronicle_recommended: false
---

# Risk Assessment Report — {{engagement_id}}

**Engagement:** {{engagement_name}}
**Risk Analyst:** {{user_name}}
**Date:** {{date}}
**Status:** In Progress
**Frameworks:** NIST SP 800-30 Rev. 1 (Process) | FAIR (Quantification)

---

## 1. Assessment Scope & Methodology

### 1.1 Purpose & Objectives

*What is this assessment intended to achieve? What decisions will it inform?*

**Purpose:**

> {{purpose_statement}}

**Objectives:**

1. {{objective_1}}
2. {{objective_2}}
3. {{objective_3}}

**Triggering Event:** {{triggering_event — regulatory requirement, M&A activity, new system deployment, periodic review, incident response, etc.}}

### 1.2 Scope Definition

**In-Scope Systems & Business Processes:**

| System / Process | Type | Owner | Business Function | Included Assets |
|------------------|------|-------|-------------------|-----------------|
| | | | | |

**Out-of-Scope (Explicit Exclusions):**

| Exclusion | Reason | Risk of Exclusion |
|-----------|--------|-------------------|
| | | |

**Organizational Boundaries:**

- **Business Units:** {{business_units_in_scope}}
- **Geographic Scope:** {{geographic_scope}}
- **Data Types:** {{data_types_in_scope}}
- **Regulatory Regimes:** {{applicable_regulations}}

### 1.3 Assessment Approach & Risk Model

**Assessment Approach:**

- [ ] Quantitative (FAIR-only)
- [ ] Qualitative (NIST 800-30-only)
- [ ] Hybrid (NIST 800-30 process + FAIR for critical risks) — **RECOMMENDED**

**Risk Model Selected:** {{risk_model — threat-source/threat-event/vulnerability/impact per NIST 800-30 Table D-1}}

**FAIR Trigger Criteria:** FAIR quantitative analysis is applied when:
- NIST 800-30 qualitative rating is High or Very High, AND
- The affected asset is classified as a Crown Jewel (Tier 1), OR
- Stakeholder explicitly requests dollar-value quantification

**Assessment Scale References:**
- Likelihood: NIST 800-30 Table G-3 (VL/L/M/H/VH)
- Impact: NIST 800-30 Table H-3 (VL/L/M/H/VH)
- Risk: NIST 800-30 Table I-2 (5x5 matrix)

### 1.4 Stakeholders & Risk Appetite

**Stakeholder Register:**

| Stakeholder | Role | Interest | Influence | Risk Appetite | Briefing Cadence |
|-------------|------|----------|-----------|---------------|------------------|
| | | | | | |

**Organizational Risk Appetite:**

- **Risk Appetite Statement:** {{risk_appetite_statement}}
- **Risk Tolerance Thresholds:**
  - Very High Risk: {{tolerance_vh — e.g., "Unacceptable — immediate treatment required"}}
  - High Risk: {{tolerance_h — e.g., "Requires executive-approved treatment plan within 30 days"}}
  - Moderate Risk: {{tolerance_m — e.g., "Treatment plan within 90 days, may accept with justification"}}
  - Low Risk: {{tolerance_l — e.g., "Accept with monitoring"}}
  - Very Low Risk: {{tolerance_vl — e.g., "Accept"}}
- **Maximum Acceptable ALE:** {{max_ale — dollar threshold for single-loss acceptability}}

### 1.5 Assumptions & Constraints

**Assumptions:**

| # | Assumption | Impact if Invalid | Confidence |
|---|-----------|-------------------|------------|
| A1 | | | |
| A2 | | | |
| A3 | | | |

**Constraints:**

| # | Constraint | Impact on Assessment | Mitigation |
|---|-----------|---------------------|------------|
| C1 | | | |
| C2 | | | |
| C3 | | | |

**Data Sources & Confidence:**

| Source | Type | Last Updated | Confidence | Notes |
|--------|------|-------------|------------|-------|
| | | | | |

---

## 2. Asset Inventory & Crown Jewels Analysis

### 2.1 Asset Inventory

| Asset | Type | Owner | Classification | Criticality | Dependencies |
|-------|------|-------|---------------|-------------|--------------|
| | | | | | |

**Asset Type Legend:**
- **HW** — Hardware (servers, endpoints, network devices, IoT)
- **SW** — Software (applications, databases, middleware, OS)
- **DATA** — Data stores (databases, file shares, cloud storage, backups)
- **SVC** — Services (cloud services, SaaS, APIs, third-party integrations)
- **PPL** — People (key personnel, teams, external contractors)
- **PROC** — Processes (business processes, workflows, procedures)

**Classification Legend:**
- **Public** — No confidentiality requirement
- **Internal** — Organization-internal, limited business impact if disclosed
- **Confidential** — Significant business impact if disclosed
- **Restricted** — Severe business impact if disclosed, regulatory implications

**Criticality Legend:**
- **Critical** — Business cannot operate without this asset
- **High** — Significant degradation of business operations
- **Medium** — Moderate impact, workarounds available
- **Low** — Minimal operational impact

**Total Assets Inventoried:** {{total_assets_inventoried}}

### 2.2 Crown Jewels Identification

*Crown Jewels are the assets whose compromise would cause catastrophic business impact. These receive the highest scrutiny and FAIR quantification.*

| Asset | Business Function | Impact if Compromised | Tier | Dollar Value Range |
|-------|-------------------|----------------------|------|--------------------|
| | | | | |

**Tiering Criteria:**
- **Tier 1 (Crown Jewels):** Catastrophic impact — existential threat to the organization, regulatory sanctions, massive financial loss. Always receives FAIR analysis.
- **Tier 2 (High Value):** Severe impact — significant financial loss, reputational damage, operational disruption. Receives FAIR analysis if rated H/VH.
- **Tier 3 (Standard):** Moderate impact — manageable financial loss, limited operational disruption. NIST 800-30 qualitative analysis only.

**Crown Jewels Identified:** {{crown_jewels_identified}}

### 2.3 Dependency Mapping

*Upstream and downstream dependencies for Crown Jewel and Tier 2 assets. A dependency failure is a threat event.*

**Dependency Map — Crown Jewel Assets:**

| Crown Jewel | Depends On | Dependency Type | Failure Impact | Redundancy |
|-------------|-----------|-----------------|----------------|------------|
| | | | | |

**Dependency Type Legend:**
- **HARD** — Complete failure if dependency is unavailable
- **SOFT** — Degraded operation if dependency is unavailable
- **DATA** — Data flow dependency (integrity/availability)
- **AUTH** — Authentication/authorization dependency

**Dependency Maps Created:** {{dependency_maps_created}}

### 2.4 Asset Valuation Summary

| Tier | Count | Estimated Value Range | Notes |
|------|-------|-----------------------|-------|
| Tier 1 (Crown Jewels) | | | |
| Tier 2 (High Value) | | | |
| Tier 3 (Standard) | | | |
| **Total** | | | |

**Total Estimated Asset Value:** {{total_asset_value}}

---

## 3. Threat Landscape

### 3.1 Threat Source Identification

| Source | Type | Capability | Intent | Targeting | Relevance |
|--------|------|-----------|--------|-----------|-----------|
| | | | | | |

**Type Legend (per NIST 800-30 Table D-2):**
- **ADV** — Adversarial (individuals, groups, organizations, nation-states)
- **ACC** — Accidental (user errors, administrative mistakes)
- **STR** — Structural (equipment failures, software defects, environmental)
- **ENV** — Environmental (natural disasters, infrastructure failures)

**Capability Scale (Adversarial only):**
- **Very High** — Possesses or can develop sophisticated capabilities, extensive resources, nation-state level
- **High** — Advanced technical skills, significant resources, organized criminal or APT level
- **Moderate** — Moderate technical skills, some specialized tools, hacktivist or organized group
- **Low** — Basic technical skills, widely available tools, opportunistic attacker

**Intent Scale (Adversarial only):**
- **Very High** — Actively targeting the organization, demonstrated past attacks
- **High** — Targeting the sector/industry, organization is in the target set
- **Moderate** — Opportunistic, would attack if opportunity presented
- **Low** — No known interest, theoretical threat only

**Relevance Scale (per NIST 800-30 Table E-4):**
- **Confirmed** — Threat source has been observed targeting the organization or its sector
- **Expected** — High confidence the threat source will target the organization based on TTPs and targeting history
- **Anticipated** — Moderate confidence based on general threat landscape and organizational profile
- **Predicted** — Low confidence, theoretical but plausible
- **N/A** — Not applicable to the organization's threat profile

### 3.2 Adversarial Threat Characterization

*Detailed characterization for each adversarial threat source with Relevance rating of Confirmed, Expected, or Anticipated.*

**Threat Source: {{threat_source_name}}**

- **Type:** {{type — e.g., Nation-State, Organized Crime, Hacktivist, Insider, Competitor}}
- **Capability:** {{capability_rating}}
- **Intent:** {{intent_rating}}
- **Targeting:** {{targeting_description}}
- **Known TTPs:** {{known_ttps}}
- **Historical Activity:** {{historical_activity_relevant_to_org}}
- **MITRE ATT&CK Groups:** {{mitre_groups — e.g., APT28, FIN7}}
- **Relevance:** {{relevance_rating}}

*(Repeat block for each adversarial threat source)*

### 3.3 Non-Adversarial Threat Sources

*Accidental, structural, and environmental threat sources per NIST 800-30 Table D-4.*

| Source | Type | Range of Effects | Likelihood Factors | Relevance |
|--------|------|------------------|-------------------|-----------|
| | | | | |

**Adversarial Sources:** {{adversarial_sources}}
**Non-Adversarial Sources:** {{non_adversarial_sources}}
**Total Threat Sources Identified:** {{threat_sources_identified}}

### 3.4 Threat Event Mapping

| Event | Source | TTP | Relevance | Affected Assets |
|-------|--------|-----|-----------|-----------------|
| | | | | |

**Threat Event Relevance (per NIST 800-30 Table E-4):**
- Map each threat event to the threat source(s) that could initiate it
- Rate relevance based on the combination of source capability/intent and event complexity
- Link each event to the specific assets it would affect

**Total Threat Events Mapped:** {{threat_events_mapped}}

### 3.5 MITRE ATT&CK Cross-Reference

*Map identified threat events to MITRE ATT&CK techniques for standardized threat communication.*

| Technique ID | Technique Name | Tactic | Mapped Threat Events | Detection Coverage |
|-------------|----------------|--------|---------------------|-------------------|
| | | | | |

**MITRE Techniques Mapped:** {{mitre_techniques_mapped}}

### 3.6 Threat-Asset Pairing Matrix

*Matrix showing which threat events affect which Crown Jewel and Tier 2 assets. This drives the risk determination phase.*

| Threat Event | Asset 1 | Asset 2 | Asset 3 | Asset 4 | Asset 5 |
|-------------|---------|---------|---------|---------|---------|
| | | | | | |

*Cell values: **X** = directly affected, **D** = affected via dependency, **—** = not affected*

---

## 4. Vulnerability & Control Assessment

### 4.1 Vulnerability Identification

| Vuln ID | Vulnerability | Type | Severity | Affected Asset | Exploitability |
|---------|--------------|------|----------|----------------|----------------|
| | | | | | |

**Type Legend:**
- **TECH** — Technical vulnerability (CVE, misconfiguration, design flaw)
- **PROC** — Process vulnerability (missing procedure, inadequate workflow)
- **PPL** — People vulnerability (lack of training, social engineering susceptibility)
- **PHYS** — Physical vulnerability (access control weakness, environmental exposure)
- **ARCH** — Architectural vulnerability (single point of failure, missing segmentation)

**Severity Scale (per NIST 800-30 Table F-2):**
- **Very High** — Easily exploitable, no compensating controls, direct path to Crown Jewel
- **High** — Exploitable with moderate effort, limited compensating controls
- **Moderate** — Exploitable with significant effort or requires chaining
- **Low** — Difficult to exploit, strong compensating controls in place
- **Very Low** — Theoretical, not practically exploitable in current environment

**Exploitability Scale:**
- **Weaponized** — Public exploit code available, actively exploited in the wild
- **PoC Available** — Proof-of-concept exists, not yet weaponized
- **Theoretical** — Vulnerability confirmed but no known exploitation method
- **Mitigated** — Vulnerability exists but compensating controls reduce exploitability

**Total Vulnerabilities Identified:** {{vulnerabilities_identified}}

### 4.2 Predisposing Conditions

*Organizational conditions that increase susceptibility to threat events (per NIST 800-30 Table F-3).*

| Condition | Category | Severity | Affected Assets | Compounding Factors |
|-----------|----------|----------|-----------------|-------------------|
| | | | | |

**Category Legend:**
- **TECH** — Technical (legacy systems, end-of-life software, technical debt)
- **ORG** — Organizational (understaffing, budget constraints, competing priorities)
- **OPS** — Operational (change management gaps, patching delays, monitoring blind spots)
- **GOV** — Governance (missing policies, unclear ownership, inadequate risk culture)
- **3RD** — Third-party (supply chain dependencies, vendor concentration, shared infrastructure)

**Predisposing Conditions Identified:** {{predisposing_conditions}}

### 4.3 Control Effectiveness

| Control ID | Control | Type | Coverage | Effectiveness | Gaps |
|-----------|---------|------|----------|---------------|------|
| | | | | | |

**Type Legend:**
- **PREV** — Preventive (blocks the threat event from occurring)
- **DET** — Detective (identifies the threat event during or after occurrence)
- **CORR** — Corrective (reduces impact after the threat event occurs)
- **COMP** — Compensating (alternative control when primary is infeasible)
- **DETER** — Deterrent (discourages the threat event initiation)

**Effectiveness Scale:**
- **Very High (VH)** — Control consistently prevents/detects the threat event, regularly tested, fully implemented
- **High (H)** — Control is effective in most scenarios, occasionally bypassed in edge cases
- **Moderate (M)** — Control provides partial protection, significant scenarios where it fails
- **Low (L)** — Control is largely ineffective, easily bypassed or circumvented
- **Very Low (VL)** — Control exists on paper but is not operational or is trivially bypassed

**Controls Assessed:** {{controls_assessed}}

### 4.4 Control Gaps

*Identified gaps where controls are missing, ineffective, or incomplete.*

| Gap ID | Description | Affected Vulnerability | Affected Asset | Risk Increase | Recommended Control |
|--------|------------|----------------------|----------------|---------------|-------------------|
| | | | | | |

**Control Gaps Identified:** {{control_gaps_identified}}

### 4.5 Threat-Vulnerability Mapping

*Map threat events to the vulnerabilities they exploit and the controls that address them.*

| Threat Event | Exploited Vulnerability | Predisposing Condition | Existing Controls | Control Effectiveness | Net Exposure |
|-------------|------------------------|----------------------|-------------------|--------------------|-------------|
| | | | | | |

---

## 5. Risk Determination

### 5.1 Likelihood Analysis

*Two-step likelihood determination per NIST 800-30 (Table G-3 & G-4):*

**Step 1 — Likelihood of Threat Event Initiation (adversarial) or Occurrence (non-adversarial):**

| Threat Event | Source Characteristics | Relevance | Initiation Likelihood |
|-------------|----------------------|-----------|----------------------|
| | | | |

**Step 2 — Likelihood of Threat Event Resulting in Adverse Impact (given initiation):**

| Threat Event | Vulnerability Severity | Predisposing Conditions | Control Effectiveness | Impact Likelihood |
|-------------|----------------------|------------------------|--------------------|------------------|
| | | | | |

**Overall Likelihood (per NIST 800-30 Table G-5):**

| Threat Event | Initiation Likelihood | Impact Likelihood | Overall Likelihood |
|-------------|----------------------|------------------|-------------------|
| | | | |

**Likelihood Scale (NIST 800-30 Table G-3):**
- **Very High (VH):** Adversary is highly motivated and sufficiently capable, and controls to prevent the threat event are ineffective — near certainty of initiation and impact
- **High (H):** Adversary is motivated and capable, and controls may not prevent the threat event — highly likely
- **Moderate (M):** Adversary is motivated but controls may impede — possible
- **Low (L):** Adversary lacks motivation or capability, or controls are likely to prevent — unlikely
- **Very Low (VL):** Adversary lacks motivation and capability, or controls are fully effective — highly unlikely

### 5.2 Impact Analysis

*Impact assessment across five harm categories per NIST 800-30 (Table H-2):*

| Threat Event | Harm to Operations | Harm to Assets | Harm to Individuals | Harm to Other Orgs | Harm to Nation |
|-------------|-------------------|----------------|--------------------|--------------------|---------------|
| | | | | | |

**Overall Impact (highest harm category per NIST 800-30 Table H-4):**

| Threat Event | Max Harm Category | Overall Impact |
|-------------|------------------|----------------|
| | | |

**Impact Scale (NIST 800-30 Table H-3):**
- **Very High (VH):** Multiple severe or catastrophic adverse effects — existential threat, regulatory sanctions, massive data breach, extended operational shutdown
- **High (H):** Severe adverse effect on operations, assets, or individuals — significant financial loss, major reputational damage, extended partial outage
- **Moderate (M):** Serious adverse effect — noticeable financial loss, moderate reputational damage, temporary operational disruption
- **Low (L):** Limited adverse effect — minor financial loss, contained reputational impact, brief disruption
- **Very Low (VL):** Negligible adverse effect — no meaningful operational, financial, or reputational impact

### 5.3 Risk Matrix — NIST 800-30

*5x5 qualitative risk matrix per NIST 800-30 Table I-2:*

|  | **VL Impact** | **L Impact** | **M Impact** | **H Impact** | **VH Impact** |
|---|---|---|---|---|---|
| **VH Likelihood** | Low | Moderate | High | Very High | Very High |
| **H Likelihood** | Low | Moderate | High | High | Very High |
| **M Likelihood** | Low | Low | Moderate | High | High |
| **L Likelihood** | Very Low | Low | Low | Moderate | Moderate |
| **VL Likelihood** | Very Low | Very Low | Low | Low | Moderate |

### 5.4 Risk Register

*Comprehensive risk register per NIST 800-30 Table I-5:*

| Risk ID | Threat Source | Threat Event | Vulnerability | Affected Asset | Likelihood | Impact | Risk Level | FAIR ALE | Risk Owner | Treatment | Status |
|---------|-------------|-------------|---------------|----------------|-----------|--------|-----------|----------|-----------|-----------|--------|
| | | | | | | | | | | | |

**Risk Determination Summary:**
- **Total Risks Calculated:** {{total_risks_calculated}}
- **Very High:** {{risks_very_high}}
- **High:** {{risks_high}}
- **Moderate:** {{risks_moderate}}
- **Low:** {{risks_low}}
- **Very Low:** {{risks_very_low}}

### 5.5 Risk Heat Map

*Visual representation of risk distribution across likelihood and impact dimensions.*

```
RISK HEAT MAP

Impact →    VL        L         M         H         VH
          ┌─────────┬─────────┬─────────┬─────────┬─────────┐
VH Lklhd  │         │         │         │         │         │
          ├─────────┼─────────┼─────────┼─────────┼─────────┤
H  Lklhd  │         │         │         │         │         │
          ├─────────┼─────────┼─────────┼─────────┼─────────┤
M  Lklhd  │         │         │         │         │         │
          ├─────────┼─────────┼─────────┼─────────┼─────────┤
L  Lklhd  │         │         │         │         │         │
          ├─────────┼─────────┼─────────┼─────────┼─────────┤
VL Lklhd  │         │         │         │         │         │
          └─────────┴─────────┴─────────┴─────────┴─────────┘

Legend: [count] = number of risks in cell
        VH/H cells trigger FAIR analysis for Crown Jewel assets
```

**Heat Map Generated:** {{heat_map_generated}}

### 5.6 FAIR Quantitative Analysis

*FAIR analysis is conducted for risks rated High or Very High that affect Crown Jewel assets. Each analysis produces an Annual Loss Expectancy (ALE) expressed as a range.*

**FAIR Analysis: {{risk_id}} — {{risk_description}}**

**Loss Event Frequency (LEF):**

| Factor | Min | Most Likely | Max | Confidence | Rationale |
|--------|-----|-------------|-----|------------|-----------|
| Threat Event Frequency (TEF) | | | | | |
| Vulnerability (Prob of Action) | | | | | |
| **LEF = TEF x Vulnerability** | | | | | |

**Loss Magnitude (LM):**

| Loss Form | Min | Most Likely | Max | Confidence | Rationale |
|-----------|-----|-------------|-----|------------|-----------|
| Productivity Loss | | | | | |
| Response Cost | | | | | |
| Replacement Cost | | | | | |
| Fines & Judgments | | | | | |
| Competitive Advantage Loss | | | | | |
| Reputation Damage | | | | | |
| **Total Loss Magnitude** | | | | | |

**Annual Loss Expectancy (ALE):**

| Metric | Min | Most Likely | Max |
|--------|-----|-------------|-----|
| LEF (events/year) | | | |
| LM (per event) | | | |
| **ALE = LEF x LM** | | | |

**Confidence Level:** {{confidence — Low/Medium/High}}
**Data Quality:** {{data_quality — Measured/Estimated/Expert Opinion/Industry Benchmark}}

*(Repeat FAIR analysis block for each qualifying risk)*

**FAIR Analyses Completed:** {{fair_analyses_completed}}

### 5.7 Annual Loss Expectancy Summary

| Risk ID | Risk Description | NIST Rating | ALE (Most Likely) | ALE (Max) | Crown Jewel |
|---------|-----------------|-------------|-------------------|-----------|-------------|
| | | | | | |

**Total ALE (Most Likely):** {{total_ale}}
**Total ALE (Maximum):** {{total_ale_max}}

---

## 6. Risk Treatment Plan

### 6.1 Treatment Strategy Decisions

| Risk ID | Risk Level | ALE | Strategy | Justification |
|---------|-----------|-----|----------|---------------|
| | | | | |

**Treatment Strategy Options:**
- **Mitigate** — Implement controls to reduce likelihood and/or impact
- **Transfer** — Shift risk to third party (insurance, outsourcing, contractual)
- **Avoid** — Eliminate the risk by removing the threat source or vulnerability (change business process, retire system)
- **Accept** — Acknowledge the risk and monitor (must be within risk appetite and formally approved)

### 6.2 Mitigation Controls & Actions

*For each risk with strategy = Mitigate:*

| Risk ID | Proposed Control | Control Type | Expected Risk Reduction | Cost Estimate | Implementation Timeline | Owner |
|---------|-----------------|-------------|------------------------|---------------|------------------------|-------|
| | | | | | | |

**Control Implementation Priority:**
1. {{priority_1_control — highest risk reduction per dollar}}
2. {{priority_2_control}}
3. {{priority_3_control}}

### 6.3 Risk Transfer Mechanisms

*For each risk with strategy = Transfer:*

| Risk ID | Transfer Mechanism | Transfer Party | Coverage | Annual Cost | Residual Retention | Gap |
|---------|-------------------|---------------|----------|-------------|-------------------|-----|
| | | | | | | |

**Transfer Types:**
- **Insurance** — Cyber insurance, business interruption, D&O
- **Contractual** — SLA guarantees, liability clauses, indemnification
- **Outsource** — Managed security services, cloud provider shared responsibility

### 6.4 Risk Acceptance Documentation

*For each risk with strategy = Accept:*

| Risk ID | Risk Level | ALE | Accepting Authority | Acceptance Rationale | Review Date | Conditions |
|---------|-----------|-----|--------------------|--------------------|-------------|-----------|
| | | | | | | |

**Acceptance Criteria:**
- Risk level must be within organizational risk appetite
- Accepting authority must have appropriate delegation of authority
- Acceptance must include explicit review date (maximum 12 months)
- Conditions for revocation must be documented

### 6.5 Residual Risk Assessment

*Residual risk after treatment is applied:*

| Risk ID | Inherent Risk | Treatment Strategy | Expected Control Effect | Residual Likelihood | Residual Impact | Residual Risk Level | Residual ALE |
|---------|--------------|-------------------|------------------------|--------------------|-----------------|--------------------|-------------|
| | | | | | | | |

**Residual Risk Summary:**
- **Risks Remaining Very High:** {{residual_vh}}
- **Risks Remaining High:** {{residual_h}}
- **Risks Remaining Moderate:** {{residual_m}}
- **Risks Remaining Low:** {{residual_l}}
- **Risks Remaining Very Low:** {{residual_vl}}

**Residual Risks Calculated:** {{residual_risks_calculated}}

### 6.6 Treatment Prioritization & ROI

| Priority | Risk ID | Treatment | Cost | Risk Reduction | ALE Reduction | ROI | Quick Win |
|----------|---------|-----------|------|----------------|---------------|-----|-----------|
| | | | | | | | |

**ROI Calculation:**
- ROI = (ALE Reduction - Treatment Cost) / Treatment Cost
- Quick Win = Treatment cost < ${{threshold}} AND implementation < {{days}} days AND risk reduction >= 1 level

### 6.7 Treatment Roadmap

| Phase | Timeline | Risk IDs | Actions | Budget | Dependencies | Milestone |
|-------|----------|----------|---------|--------|-------------|-----------|
| Immediate (0-30 days) | | | | | | |
| Short-Term (30-90 days) | | | | | | |
| Medium-Term (90-180 days) | | | | | | |
| Long-Term (180-365 days) | | | | | | |

**Treatment Roadmap Created:** {{treatment_roadmap_created}}

**Treatment Summary:**
- **Risks with Treatment:** {{risks_with_treatment}}
- **Mitigate:** {{treatment_mitigate}}
- **Transfer:** {{treatment_transfer}}
- **Accept:** {{treatment_accept}}
- **Avoid:** {{treatment_avoid}}

---

## 7. Executive Summary

### 7.1 Assessment Overview

**Assessment ID:** {{assessment_id}}
**Assessment Date:** {{date}}
**Assessment Approach:** {{assessment_approach}}
**Scope:** {{assessment_scope_summary}}
**Risk Model:** NIST SP 800-30 Rev. 1 (qualitative) + FAIR (quantitative for critical risks)

### 7.2 Key Findings

1. {{key_finding_1}}
2. {{key_finding_2}}
3. {{key_finding_3}}
4. {{key_finding_4}}
5. {{key_finding_5}}

### 7.3 Risk Landscape Summary

| Metric | Value |
|--------|-------|
| Total Assets Assessed | {{total_assets_inventoried}} |
| Crown Jewels Identified | {{crown_jewels_identified}} |
| Threat Sources Identified | {{threat_sources_identified}} |
| Vulnerabilities Identified | {{vulnerabilities_identified}} |
| Control Gaps Identified | {{control_gaps_identified}} |
| Total Risks Calculated | {{total_risks_calculated}} |
| Very High Risks | {{risks_very_high}} |
| High Risks | {{risks_high}} |
| Moderate Risks | {{risks_moderate}} |
| Low / Very Low Risks | {{risks_low}} + {{risks_very_low}} |
| Total Annual Loss Expectancy | {{total_ale}} |
| FAIR Analyses Completed | {{fair_analyses_completed}} |

### 7.4 Top Risks

| Rank | Risk ID | Description | Risk Level | ALE | Treatment | Owner |
|------|---------|------------|-----------|-----|-----------|-------|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

### 7.5 Strategic Recommendations

1. **{{recommendation_1_title}}:** {{recommendation_1_detail}}
2. **{{recommendation_2_title}}:** {{recommendation_2_detail}}
3. **{{recommendation_3_title}}:** {{recommendation_3_detail}}

### 7.6 Investment Priorities

| Priority | Investment | Cost Range | Expected ALE Reduction | Risks Addressed | Payback Period |
|----------|-----------|-----------|----------------------|-----------------|---------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

**Executive Summary Complete:** {{executive_summary_complete}}

---

## 8. Appendices

### Appendix A: Methodology Reference

**NIST SP 800-30 Rev. 1 — Guide for Conducting Risk Assessments**

The assessment follows the NIST SP 800-30 Rev. 1 four-step risk assessment process:

1. **Prepare for Assessment** — Establish context, scope, assumptions, and constraints
2. **Conduct Assessment** — Identify threat sources, threat events, vulnerabilities; determine likelihood and impact; calculate risk
3. **Communicate Results** — Present risk determination results to stakeholders; provide risk treatment recommendations
4. **Maintain Assessment** — Track risk changes, treatment effectiveness, and trigger reassessment criteria

**FAIR — Factor Analysis of Information Risk**

FAIR provides a quantitative risk analysis framework that decomposes risk into measurable factors:

- **Loss Event Frequency (LEF)** = Threat Event Frequency (TEF) x Vulnerability (probability the threat event becomes a loss event)
- **Loss Magnitude (LM)** = Sum of primary and secondary loss forms (productivity, response, replacement, fines, competitive advantage, reputation)
- **Risk (ALE)** = LEF x LM, expressed as an annualized dollar range

**Hybrid Integration:**
- NIST 800-30 provides the systematic identification and qualitative rating for ALL risks
- FAIR provides dollar-value quantification for HIGH and VERY HIGH risks affecting Crown Jewel assets
- This hybrid approach ensures comprehensive coverage (NIST) with decision-grade financial data (FAIR) where it matters most

### Appendix B: NIST 800-30 Assessment Scales

**Table B-1: Likelihood of Threat Event Initiation (Adversarial)**

| Qualitative Value | Semi-Quantitative Value | Description |
|-------------------|------------------------|-------------|
| Very High | 96-100 / 10 | Adversary is almost certain to initiate the threat event |
| High | 80-95 / 8 | Adversary is highly likely to initiate the threat event |
| Moderate | 21-79 / 5 | Adversary is somewhat likely to initiate the threat event |
| Low | 5-20 / 2 | Adversary is unlikely to initiate the threat event |
| Very Low | 0-4 / 0 | Adversary is highly unlikely to initiate the threat event |

**Table B-2: Likelihood of Threat Event Resulting in Adverse Impact**

| Qualitative Value | Semi-Quantitative Value | Description |
|-------------------|------------------------|-------------|
| Very High | 96-100 / 10 | If the threat event is initiated, it is almost certain to result in adverse impact |
| High | 80-95 / 8 | If the threat event is initiated, it is highly likely to result in adverse impact |
| Moderate | 21-79 / 5 | If the threat event is initiated, it is somewhat likely to result in adverse impact |
| Low | 5-20 / 2 | If the threat event is initiated, it is unlikely to result in adverse impact |
| Very Low | 0-4 / 0 | If the threat event is initiated, it is highly unlikely to result in adverse impact |

**Table B-3: Overall Likelihood**

| Likelihood of Initiation | Likelihood of Impact |||||
|---|---|---|---|---|---|
| | **VH** | **H** | **M** | **L** | **VL** |
| **VH** | VH | VH | H | M | L |
| **H** | VH | H | M | L | VL |
| **M** | H | M | M | L | VL |
| **L** | M | L | L | L | VL |
| **VL** | L | L | VL | VL | VL |

**Table B-4: Impact Scale**

| Qualitative Value | Semi-Quantitative Value | Description |
|-------------------|------------------------|-------------|
| Very High | 96-100 / 10 | Multiple severe or catastrophic adverse effects on operations, assets, individuals, other orgs, or the nation |
| High | 80-95 / 8 | Severe adverse effect on operations, assets, individuals, other orgs, or the nation |
| Moderate | 21-79 / 5 | Serious adverse effect on operations, assets, individuals, other orgs, or the nation |
| Low | 5-20 / 2 | Limited adverse effect on operations, assets, individuals, other orgs, or the nation |
| Very Low | 0-4 / 0 | Negligible adverse effect on operations, assets, individuals, other orgs, or the nation |

**Table B-5: Risk Determination Matrix (Level of Risk)**

| Likelihood | Impact |||||
|---|---|---|---|---|---|
| | **VH** | **H** | **M** | **L** | **VL** |
| **VH** | VH | VH | H | M | L |
| **H** | VH | H | H | M | L |
| **M** | H | H | M | L | L |
| **L** | M | M | L | L | VL |
| **VL** | M | L | L | VL | VL |

### Appendix C: FAIR Analysis Details

*Detailed FAIR model decomposition trees and Monte Carlo simulation parameters for each analyzed risk.*

**FAIR Ontology Reference:**

```
Risk
├── Loss Event Frequency (LEF)
│   ├── Threat Event Frequency (TEF)
│   │   ├── Contact Frequency
│   │   └── Probability of Action
│   └── Vulnerability (Vuln)
│       ├── Control Strength
│       └── Threat Capability
└── Loss Magnitude (LM)
    ├── Primary Loss
    │   ├── Productivity Loss
    │   ├── Response Cost
    │   └── Replacement Cost
    └── Secondary Loss
        ├── Fines & Judgments
        ├── Competitive Advantage Loss
        └── Reputation Damage
```

*(Detailed analysis worksheets appended per risk)*

### Appendix D: Complete Risk Register (Exportable)

*Full risk register in tabular format for export to GRC tools.*

| Risk ID | Threat Source | Threat Event | Vuln ID | Asset | Likelihood | Impact | Risk Level | FAIR ALE (Min) | FAIR ALE (ML) | FAIR ALE (Max) | Treatment | Residual Risk | Owner | Status | Last Updated |
|---------|-------------|-------------|---------|-------|-----------|--------|-----------|---------------|--------------|--------------|-----------|--------------|-------|--------|-------------|
| | | | | | | | | | | | | | | | |

### Appendix E: Control Mapping

*Mapping of controls to risks, vulnerabilities, and frameworks.*

| Control ID | Control Description | Type | Maps to Risk(s) | Maps to Vuln(s) | NIST CSF | ISO 27001 | Effectiveness |
|-----------|-------------------|------|-----------------|-----------------|----------|-----------|---------------|
| | | | | | | | |

### Appendix F: Assumptions & Confidence Levels

*Comprehensive list of all assumptions made during the assessment with confidence ratings and impact analysis.*

| Assumption ID | Assumption | Category | Confidence | Impact if Invalid | Validation Method |
|--------------|-----------|----------|------------|-------------------|------------------|
| | | | | | |

**Overall Assessment Confidence:**
- **Data Quality:** {{overall_data_quality — Measured/Estimated/Expert Opinion/Mixed}}
- **Coverage:** {{coverage — Complete/Partial/Limited}}
- **Confidence Level:** {{confidence_level — High/Medium/Low}}
- **Key Uncertainty Factors:** {{key_uncertainties}}

### Appendix G: Glossary

| Term | Definition |
|------|-----------|
| ALE | Annual Loss Expectancy — the expected monetary loss for an asset due to a risk over a one-year period |
| Crown Jewel | An asset whose compromise would cause catastrophic business impact; Tier 1 classification |
| FAIR | Factor Analysis of Information Risk — a quantitative risk analysis framework |
| LEF | Loss Event Frequency — the probable frequency with which a loss event will occur within a given timeframe |
| LM | Loss Magnitude — the probable magnitude of primary and secondary loss resulting from a loss event |
| NIST 800-30 | NIST Special Publication 800-30 Rev. 1 — Guide for Conducting Risk Assessments |
| Predisposing Condition | An existing condition within an organization that affects the likelihood of a threat event |
| Residual Risk | Risk remaining after risk treatment has been applied |
| Risk Appetite | The amount of risk an organization is willing to accept in pursuit of its objectives |
| Risk Register | A structured record of identified risks with their ratings, owners, and treatment status |
| TEF | Threat Event Frequency — the probable frequency with which a threat agent will act against an asset |
| Threat Event | An event or situation initiated by a threat source that has the potential to cause adverse impact |
| Threat Source | The intent and method targeted at the intentional exploitation of a vulnerability, or the situation and method that may accidentally trigger a vulnerability |
| Vulnerability | A weakness in an information system, system security procedures, internal controls, or implementation that could be exploited by a threat source |

---

**Report Finalized:** {{report_finalized}}
**Chronicle Recommended:** {{chronicle_recommended}}
