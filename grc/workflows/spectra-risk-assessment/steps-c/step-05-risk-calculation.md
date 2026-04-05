# Step 5: Risk Calculation — NIST 800-30 + FAIR

**Progress: Step 5 of 7** — Next: Risk Treatment Planning

## STEP GOAL:

Calculate risk for all identified threat-vulnerability pairs using NIST 800-30 qualitative/semi-quantitative method (likelihood x impact via matrices), then conduct FAIR quantitative analysis for High/Very High risks affecting Crown Jewels to produce Annual Loss Expectancy (ALE) in dollar terms. Produce the risk register and heat map. This is the analytical engine of the entire assessment — every rating must be defensible, every number traceable, every assumption documented.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER produce risk ratings without evidence traceability — a risk score without evidence is an opinion, not an assessment
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RISK ANALYST, not an autonomous scoring engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Arbiter, the risk quantification expert — CRISC/CISSP/FAIR certified — this step is your core competency
- ✅ "High risk" without numbers is just an opinion — quantify everything possible
- ✅ NIST 800-30 provides the structure, FAIR provides the precision — use both where applicable
- ✅ Every risk score must be traceable to evidence from prior steps — untraceable ratings are not assessments, they are guesses
- ✅ Confidence levels must accompany every rating — acknowledge uncertainty rather than hide it
- ✅ Risk calculation is a two-framework process: NIST 800-30 qualitative matrices establish the baseline, FAIR quantitative analysis adds financial precision for the highest risks
- ✅ The risk register produced here is the single source of truth that drives all treatment decisions in step 6 and the executive summary in step 7

### Step-Specific Rules:

- 🎯 Focus exclusively on risk calculation using data gathered in steps 2-4: asset valuations, threat characterization, vulnerability severity, control effectiveness, threat-vulnerability mapping
- 🚫 FORBIDDEN to propose treatment strategies, mitigations, or remediation actions in this step — that is step-06. Risk calculation informs treatment decisions; this step does not make them
- 🚫 FORBIDDEN to write executive summary language or risk appetite comparisons — that is step-07. Calculate the numbers; interpretation for leadership comes later
- 💬 Approach: Systematic, evidence-based scoring using NIST 800-30 matrices for all scenarios, then FAIR quantitative deep-dive for H/VH scenarios affecting Crown Jewels
- 📊 Every likelihood and impact rating must cite the specific evidence source from prior steps (asset tier, threat characterization, vulnerability severity score, control effectiveness rating)
- 🔄 Reference `assessment_approach` from step-01 to determine which method(s) apply:
  - If `qualitative`: NIST 800-30 matrices only (sections 1-9, 11-12)
  - If `hybrid`: NIST 800-30 matrices for all + FAIR for H/VH Crown Jewel scenarios (all sections)
  - If `fair`: FAIR analysis for all scenarios (all sections, FAIR primary)
- 🔒 All calculations must be reproducible — document formulas, inputs, and intermediate results so any qualified analyst can verify the work

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your quantification expertise is paramount here. Risk calculation is where analytical rigor meets professional judgment, and you are the subject matter expert.
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Operator wants to rate ALL risks as High/VH — explain that risk inflation dilutes urgency and makes prioritization impossible. If everything is high priority, nothing is high priority. The purpose of risk assessment is differentiation, and uniform ratings defeat that purpose. Ask the operator to re-examine evidence supporting each rating.
  - Likelihood/impact ratings contradict evidence from prior steps — explain the evidence-rating gap. If step-03 characterized a threat source as low capability with no known targeting, but the operator rates initiation likelihood as VH, the rating is not supported by the evidence. Either the evidence needs to be updated or the rating needs to be revised.
  - FAIR analysis attempted without sufficient data — explain garbage-in-garbage-out risk. FAIR requires calibrated inputs (TEF, Vulnerability, Loss Magnitude), and if the data from prior steps is insufficient to calibrate these inputs, the FAIR output will have a false precision that is worse than no number at all. Recommend qualitative fallback with documented data gaps.
  - Risk register has obvious duplicates or overlapping scenarios — explain double-counting risk. If "Phishing leads to credential theft on Email Server" and "Social engineering leads to account compromise on Email Server" are essentially the same scenario, counting both inflates the risk profile and distorts the heat map. Deduplicate or merge with operator approval.
  - Semi-quantitative scores used without understanding the scale — explain that NIST 800-30 semi-quantitative values (0-100) are ordinal, not cardinal. A score of 80 is not "twice as risky" as 40. The numbers enable matrix lookup, not arithmetic comparison.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks. If the operator disagrees with your assessment, document both perspectives in the risk register with a note on the disagreement.

## EXECUTION PROTOCOLS:

- 🎯 Load output document and verify `step-04-vulnerability-assessment.md` (or equivalent) in `stepsCompleted`
- 🎯 Load ALL prior data: assets and Crown Jewels with valuations (step-02), threat characterization and sources (step-03), vulnerabilities with severity scores, control effectiveness ratings, and threat-vulnerability mapping (step-04)
- 🎯 Verify FAIR-specific data availability if assessment_approach is 'hybrid' or 'fair': TCAP scores, CS scores, contact frequency estimates, loss magnitude inputs from Crown Jewel valuations
- ⚠️ Present data completeness summary before beginning calculation — if critical data is missing, flag gaps and ask operator how to proceed
- 📋 Work through scenarios systematically: define scenarios first, then score each through the NIST pipeline (likelihood step A → step B → overall likelihood → impact → risk determination) before moving to FAIR
- ⚠️ Present [A]/[W]/[C] menu after full risk register and heat map are complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of `stepsCompleted` and updating:
  - `total_risks_calculated`: total number of risk scenarios scored
  - `risks_very_high`: count of VH risk scenarios
  - `risks_high`: count of H risk scenarios
  - `risks_moderate`: count of M risk scenarios
  - `risks_low`: count of L risk scenarios
  - `risks_very_low`: count of VL risk scenarios
  - `fair_analyses_completed`: count of FAIR analyses performed (0 if qualitative only)
  - `total_ale`: aggregate ALE across all FAIR-analyzed scenarios (null if qualitative only)
  - `risk_register_populated`: true
  - `heat_map_generated`: true
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Complete data from steps 1-4: assessment scope and approach (step-01), asset inventory with Crown Jewel designations and dollar valuations (step-02), threat characterization with sources, capabilities, intents, and targeting profiles (step-03), vulnerability inventory with severity scores, control effectiveness ratings, FAIR TCAP/CS scores if hybrid, and threat-vulnerability mapping (step-04)
- Focus: Risk scenario definition, likelihood determination (two-step NIST process), impact assessment (five harm categories), risk matrix calculation, risk register population, heat map generation, FAIR quantitative analysis for H/VH Crown Jewel scenarios, ALE calculation
- Limits: Do NOT propose treatment strategies, mitigations, or remediation actions (step-06). Do NOT write executive summary language, risk appetite comparisons, or board-level reporting (step-07). Calculate the numbers; everything else comes later.
- Dependencies: Threat-vulnerability mapping from step-04, Crown Jewel valuations from step-02, FAIR TCAP/CS data from step-04 (if hybrid/fair approach)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load & Validate Prior Data

Load the output document and all prior section data. This step depends entirely on the quality and completeness of data gathered in steps 2-4 — verify everything before beginning calculation.

**Load and verify the following data sets:**

**From Step 01 — Scope Definition:**
- `assessment_approach`: qualitative / hybrid / fair — this determines which calculation methods are required
- `risk_model`: the risk model selected (NIST 800-30 default)
- Assessment scope boundaries — which systems, business processes, and data flows are in scope

**From Step 02 — Asset Inventory & Crown Jewels:**
- Complete asset inventory with tier assignments (Crown Jewel / Tier 2 / Tier 3)
- Crown Jewel Analysis (CJA) with dollar valuations:
  - Asset replacement cost
  - Revenue dependency (revenue at risk if asset is unavailable)
  - Regulatory exposure (fines, penalties if asset data is breached)
  - Competitive advantage value
  - Total asset value (aggregated valuation)
- Business Impact Analysis (BIA) data: RTO, RPO, MTPD for critical assets
- Data classification for assets containing sensitive data

**From Step 03 — Threat Identification:**
- Threat source catalog with characterization:
  - Adversarial: capability level, intent, targeting profile
  - Non-adversarial: range of effects, likelihood modifiers
- Threat event catalog mapped to NIST 800-30 Appendix E threat events
- Threat relevance determination (relevant / not relevant / unknown)

**From Step 04 — Vulnerability & Control Assessment:**
- Vulnerability inventory with severity scores (CVSS or qualitative severity)
- Control effectiveness ratings per vulnerability (fully effective / mostly effective / partially effective / minimally effective / not effective)
- Threat-vulnerability mapping: which threat events exploit which vulnerabilities on which assets
- Predisposing conditions that increase susceptibility
- If hybrid/fair approach:
  - Threat Capability (TCAP) scores per threat-vulnerability pair
  - Control Strength (CS) scores per vulnerability-control combination
  - Contact frequency estimates where available

**Data Completeness Verification:**

Present the following summary to the operator before proceeding:

```
DATA COMPLETENESS CHECK — Risk Calculation Readiness

Assets inventoried: {{count}} ({{crown_jewel_count}} Crown Jewels, {{t2_count}} Tier 2, {{t3_count}} Tier 3)
Crown Jewels with dollar valuations: {{count}} / {{crown_jewel_count}} — {{complete/incomplete}}
Threat sources characterized: {{count}} ({{adversarial_count}} adversarial, {{non_adversarial_count}} non-adversarial)
Threat events cataloged: {{count}} ({{relevant_count}} relevant)
Vulnerabilities inventoried: {{count}} with severity scores
Controls assessed: {{count}} with effectiveness ratings
Threat-vulnerability pairs mapped: {{count}} — these become risk scenarios

Assessment approach: {{approach}}
FAIR data availability (if hybrid/fair):
  - TCAP scores: {{count}} / {{required}} — {{complete/incomplete}}
  - CS scores: {{count}} / {{required}} — {{complete/incomplete}}
  - Contact frequency estimates: {{count}} / {{required}} — {{complete/incomplete}}
  - Crown Jewel loss magnitude inputs: {{count}} / {{required}} — {{complete/incomplete}}

DATA GAPS (if any):
{{list_missing_data_with_impact_on_calculation}}

READINESS: {{READY / READY WITH GAPS / NOT READY}}
```

**If critical data is missing:**
- Flag specific gaps and their impact on calculation accuracy
- Ask operator: proceed with available data (document limitations) or return to prior step to fill gaps?
- If proceeding with gaps: document each gap and its effect on confidence levels throughout the calculation

### 2. Define Risk Scenarios

Each unique (Threat Event x Vulnerability x Affected Asset) triple constitutes one risk scenario. Build the complete scenario list from the threat-vulnerability mapping produced in step-04.

**Scenario Construction Rules:**
- One scenario per unique threat-event / vulnerability / asset combination
- If a single threat event exploits the same vulnerability across multiple assets, create separate scenarios for each asset (impact may differ by asset value)
- If multiple threat events exploit the same vulnerability on the same asset, create separate scenarios (likelihood may differ by threat source)
- Group scenarios by asset tier: Crown Jewels first, then Tier 2, then Tier 3
- Assign sequential scenario IDs: RS-001, RS-002, RS-003, etc.
- Include the threat source type (adversarial/non-adversarial) — this determines which likelihood table applies in section 3

**Deduplication Check:**
- Review scenario list for effective duplicates — scenarios where the same real-world event is described in slightly different terms
- If duplicates found: flag to operator, recommend merge, document decision
- Example duplicate: "APT group exploits unpatched Exchange CVE-2024-XXXX" and "Nation-state actor exploits Exchange RCE vulnerability" — if these describe the same threat source and vulnerability, they are one scenario

**Present the risk scenario inventory:**

```
RISK SCENARIO INVENTORY — {{count}} scenarios identified

CROWN JEWEL SCENARIOS ({{count}}):
| RS-# | Scenario Description | Threat Event | Threat Source | Type | Vulnerability | Affected Asset | Asset Tier |
|------|---------------------|-------------|--------------|------|--------------|---------------|-----------|
| RS-001 | {{description}} | {{threat_event}} | {{source}} | Adv/Non-Adv | {{vuln}} | {{asset}} | Crown Jewel |

TIER 2 SCENARIOS ({{count}}):
| RS-# | Scenario Description | Threat Event | Threat Source | Type | Vulnerability | Affected Asset | Asset Tier |
|------|---------------------|-------------|--------------|------|--------------|---------------|-----------|
| RS-0XX | {{description}} | {{threat_event}} | {{source}} | Adv/Non-Adv | {{vuln}} | {{asset}} | Tier 2 |

TIER 3 SCENARIOS ({{count}}):
| RS-# | Scenario Description | Threat Event | Threat Source | Type | Vulnerability | Affected Asset | Asset Tier |
|------|---------------------|-------------|--------------|------|--------------|---------------|-----------|
| RS-0XX | {{description}} | {{threat_event}} | {{source}} | Adv/Non-Adv | {{vuln}} | {{asset}} | Tier 3 |

Total scenarios: {{total}}
  Crown Jewel scenarios: {{count}} (scored first, FAIR eligible)
  Tier 2 scenarios: {{count}}
  Tier 3 scenarios: {{count}}
  Adversarial scenarios: {{count}} (use Table G-2)
  Non-adversarial scenarios: {{count}} (use Table G-3)
```

Confirm scenario list with operator before proceeding to scoring.

### 3. NIST 800-30 Likelihood Determination — Step A: Threat Event Initiation/Occurrence

For each risk scenario, assess the likelihood that the threat event is initiated (adversarial threats) or occurs (non-adversarial threats). This is the FIRST of two likelihood assessments — it evaluates whether the threat event happens at all, regardless of whether it succeeds.

**Use the appropriate table based on threat source type:**

**NIST 800-30 Table G-2 — Likelihood of Threat Event Initiation (ADVERSARIAL):**

This table assesses the probability that an adversary initiates the threat event, based on their capability, intent, and targeting profile as characterized in step-03.

| Qualitative Level | Semi-Quantitative Value | Description | Rating Criteria |
|-------------------|------------------------|-------------|-----------------|
| Very High (VH) | 96-100 | Adversary is almost certain to initiate the threat event. | Capability: very high — the adversary has advanced tools, techniques, and resources (e.g., nation-state, organized crime with technical division). Intent: strong and demonstrated — the adversary has attacked similar targets or explicitly targeted this organization. Targeting: focused — the adversary specifically targets this organization, sector, or asset class. |
| High (H) | 80-95 | Adversary is highly likely to initiate the threat event. | Capability: high — the adversary has sophisticated but not cutting-edge tools. Intent: strong — the adversary has motivation and has attacked similar organizations. Targeting: broad but relevant — the adversary targets this sector or region. |
| Moderate (M) | 21-79 | Adversary is somewhat likely to initiate the threat event. | Capability: moderate — the adversary has standard tools and some technical skill. Intent: present but opportunistic — the adversary is not specifically targeting this organization but would exploit opportunities. Targeting: opportunistic — scanning, mass exploitation, or spray-and-pray approaches. |
| Low (L) | 5-20 | Adversary is unlikely to initiate the threat event. | Capability: low — the adversary has limited tools and skill. Intent: weak or theoretical — no demonstrated interest in this target type. Targeting: untargeted or random — no evidence of specific interest. |
| Very Low (VL) | 0-4 | Adversary is highly unlikely to initiate the threat event. | Capability: negligible — the adversary lacks meaningful tools or skill. Intent: none demonstrated. Targeting: none — the adversary has no known interest in this target, sector, or asset class. |

**Evidence Mapping for Table G-2 Ratings:**
- Capability rating: reference threat source characterization from step-03 (capability level assessment)
- Intent rating: reference threat source characterization from step-03 (intent assessment, known campaigns)
- Targeting rating: reference threat source characterization from step-03 (targeting profile, whether this organization/sector is in the crosshairs)
- Historical data: reference any threat intelligence on frequency of similar attacks against the sector

**NIST 800-30 Table G-3 — Likelihood of Threat Event Occurrence (NON-ADVERSARIAL):**

This table assesses the probability that a non-adversarial event occurs, based on historical frequency, environmental conditions, and predisposing conditions.

| Qualitative Level | Semi-Quantitative Value | Description | Rating Criteria |
|-------------------|------------------------|-------------|-----------------|
| Very High (VH) | 96-100 | Error, accident, or environmental event is almost certain to occur within the assessment timeframe. | Historical frequency: multiple occurrences per year or continuous exposure. Predisposing conditions: environment strongly favors occurrence (aging infrastructure, high-complexity systems, geographic exposure to natural hazards). Trend: increasing frequency or severity. |
| High (H) | 80-95 | Highly likely to occur within the assessment timeframe. | Historical frequency: has occurred within the past 1-2 years. Predisposing conditions: significant factors favoring occurrence. Trend: stable or increasing. |
| Moderate (M) | 21-79 | Somewhat likely to occur within the assessment timeframe. | Historical frequency: has occurred within the past 3-5 years or occurs in comparable organizations. Predisposing conditions: some factors present. Trend: stable. |
| Low (L) | 5-20 | Unlikely to occur within the assessment timeframe. | Historical frequency: rare — has not occurred in 5+ years but is plausible. Predisposing conditions: few factors present. Trend: stable or decreasing. |
| Very Low (VL) | 0-4 | Highly unlikely to occur within the assessment timeframe. | Historical frequency: no known occurrence in this or comparable organizations. Predisposing conditions: negligible. Trend: decreasing or non-existent. |

**Evidence Mapping for Table G-3 Ratings:**
- Historical frequency: reference organizational incident history, sector statistics, vendor advisories
- Predisposing conditions: reference vulnerability assessment from step-04 (system age, complexity, configuration drift, geographic/environmental exposure)
- Trend data: reference threat landscape analysis from step-03

**For each scenario, record:**

```
| RS-# | Threat Event | Source Type | Initiation/Occurrence Likelihood | Semi-Quant | Evidence Reference | Confidence |
|------|-------------|------------|----------------------------------|------------|-------------------|------------|
| RS-001 | {{event}} | Adversarial (G-2) | {{VL/L/M/H/VH}} | {{0-100}} | Step-03: {{source_char}}, Step-04: {{vuln_data}} | High/Medium/Low |
```

**Confidence Level Criteria:**
- **High**: rating supported by multiple evidence sources from prior steps, consistent with historical data and threat intelligence
- **Medium**: rating supported by primary evidence but with some uncertainty or incomplete data
- **Low**: rating based on limited evidence, significant assumptions, or extrapolation from insufficient data — document specific assumptions

### 4. NIST 800-30 Likelihood Determination — Step B: Adverse Impact Probability

For each risk scenario, assess the likelihood that IF the threat event is initiated/occurs, it RESULTS in adverse impact to the organization. This considers the effectiveness of existing security controls and the severity of the vulnerability being exploited.

This is distinct from Step A: Step A asks "Does the threat event happen?" Step B asks "If it happens, does it cause harm?" A highly likely threat event may have low adverse impact probability if controls are strong. Conversely, a rare threat event may have very high adverse impact probability if it bypasses all controls.

**NIST 800-30 Table G-4 — Likelihood Threat Event Results in Adverse Impact:**

| Qualitative Level | Semi-Quantitative Value | Description | Rating Criteria |
|-------------------|------------------------|-------------|-----------------|
| Very High (VH) | 96-100 | If the threat event is initiated or occurs, it is almost certain to result in adverse impact. | Vulnerability severity: critical — the vulnerability provides direct, unmitigated access to the asset or its data. Control effectiveness: absent or completely ineffective — no controls address this threat-vulnerability pair, or existing controls have been demonstrated to be ineffective. Predisposing conditions: strongly favor successful exploitation. |
| High (H) | 80-95 | If the threat event is initiated or occurs, it is highly likely to result in adverse impact. | Vulnerability severity: high — the vulnerability provides significant access or disruption capability. Control effectiveness: weak — controls exist but are significantly deficient (outdated signatures, misconfigured rules, insufficient coverage). Predisposing conditions: favor successful exploitation. |
| Moderate (M) | 21-79 | If the threat event is initiated or occurs, it is somewhat likely to result in adverse impact. | Vulnerability severity: moderate — the vulnerability provides partial access or requires additional steps for full exploitation. Control effectiveness: partially effective — controls address some aspects of the threat but leave gaps. Predisposing conditions: neutral — neither strongly favor nor prevent exploitation. |
| Low (L) | 5-20 | If the threat event is initiated or occurs, it is unlikely to result in adverse impact. | Vulnerability severity: low — the vulnerability provides minimal access and requires significant effort to exploit. Control effectiveness: mostly effective — controls address the primary attack vector with minor gaps. Predisposing conditions: do not favor exploitation. |
| Very Low (VL) | 0-4 | If the threat event is initiated or occurs, it is highly unlikely to result in adverse impact. | Vulnerability severity: informational or negligible — the vulnerability provides no meaningful access. Control effectiveness: comprehensive and verified — multiple layers of controls address this threat-vulnerability pair, and controls have been tested/validated. Predisposing conditions: actively prevent exploitation. |

**Evidence Mapping for Table G-4 Ratings — CRITICAL: these must reference step-04 data:**
- Vulnerability severity: reference severity score from step-04 vulnerability inventory (CVSS base score or qualitative severity)
- Control effectiveness: reference control effectiveness rating from step-04 (fully effective / mostly effective / partially effective / minimally effective / not effective)
- Predisposing conditions: reference predisposing conditions from step-04 (system architecture, exposure, configuration, age, complexity)
- If hybrid/fair approach: reference TCAP vs CS comparison from step-04:
  - If TCAP >> CS: adverse impact probability skews VH/H (controls are outmatched)
  - If CS >> TCAP: adverse impact probability skews L/VL (controls are adequate)
  - If TCAP ≈ CS: adverse impact probability is M (uncertain outcome)

**For each scenario, record:**

```
| RS-# | Vulnerability | Severity | Control Effectiveness | Adverse Impact Likelihood | Semi-Quant | Evidence Reference | Confidence |
|------|--------------|----------|----------------------|---------------------------|------------|-------------------|------------|
| RS-001 | {{vuln}} | {{severity}} | {{effectiveness}} | {{VL/L/M/H/VH}} | {{0-100}} | Step-04: {{vuln_id}}, {{control_id}} | High/Medium/Low |
```

### 5. NIST 800-30 Overall Likelihood Determination (Table G-5)

Combine the Step A rating (threat event initiation/occurrence) with the Step B rating (adverse impact probability) to determine the overall likelihood for each risk scenario.

**NIST 800-30 Table G-5 — Overall Likelihood Assessment Matrix:**

The overall likelihood represents the combined probability that (1) the threat event occurs AND (2) it results in adverse impact. This two-step decomposition prevents the common error of conflating threat frequency with threat success rate.

```
                          Likelihood Threat Event Results in Adverse Impact
                     VL          L           M           H           VH
               +----------+----------+----------+----------+----------+
          VH   |    L     |    M     |    H     |   VH     |   VH     |
               +----------+----------+----------+----------+----------+
Likeli-   H    |    L     |    M     |    M     |    H     |   VH     |
hood of        +----------+----------+----------+----------+----------+
Threat    M    |    L     |    L     |    M     |    M     |    H     |
Event          +----------+----------+----------+----------+----------+
Init/     L    |   VL     |    L     |    L     |    M     |    M     |
Occur          +----------+----------+----------+----------+----------+
          VL   |   VL     |   VL     |    L     |    L     |    L     |
               +----------+----------+----------+----------+----------+
```

**Semi-Quantitative Combination:**
For semi-quantitative values, multiply the two semi-quantitative scores and normalize to 0-100:
- Overall Semi-Quant = (Step A Semi-Quant x Step B Semi-Quant) / 100
- Then map the result back to the qualitative scale:
  - 96-100 = VH
  - 80-95 = H
  - 21-79 = M
  - 5-20 = L
  - 0-4 = VL

**For each scenario, record the overall likelihood:**

```
OVERALL LIKELIHOOD DETERMINATION

| RS-# | Step A: Initiation/Occurrence | Step B: Adverse Impact | Overall Likelihood (G-5) | Semi-Quant | Rationale |
|------|-------------------------------|------------------------|--------------------------|------------|-----------|
| RS-001 | {{VL/L/M/H/VH}} | {{VL/L/M/H/VH}} | {{VL/L/M/H/VH}} | {{0-100}} | {{brief_justification}} |
```

**Sanity Check:**
After completing overall likelihood for all scenarios, review the distribution:
- Are the ratings differentiated, or are they clustered at one level?
- If clustered: revisit evidence — are we failing to distinguish between scenarios, or is the evidence genuinely similar?
- If all scenarios are H/VH: warn operator about risk inflation (per autonomy protocol)
- If all scenarios are L/VL: verify this is evidence-based and not a result of optimism bias

### 6. Impact Determination (NIST 800-30, Table H-3)

For each risk scenario, assess the impact (adverse consequence) if the threat event succeeds. Impact is assessed across FIVE NIST 800-30 harm categories. This multi-dimensional assessment prevents the common error of evaluating impact only in terms of financial loss or only in terms of operational disruption.

**NIST 800-30 Table H-3 — Impact Assessment Scale:**

**Category 1: Damage to Operations (Mission Capability)**

| Level | Semi-Quant | Description |
|-------|------------|-------------|
| VH | 96-100 | Multiple severe or catastrophic adverse effects on organizational operations, mission capability, or mission effectiveness. Organization cannot perform one or more primary functions. Multiple critical business processes are disrupted beyond recovery in acceptable timeframes. Cascading failures affect dependent systems and processes. |
| H | 80-95 | Severe adverse effect on organizational operations. Significant degradation in mission capability to the extent that the organization can perform its primary functions but effectiveness is significantly reduced. Critical business processes are severely degraded. |
| M | 21-79 | Serious adverse effect on organizational operations. Significant degradation in mission capability but the organization can still perform all primary functions with reduced effectiveness. Important but non-critical business processes are disrupted. |
| L | 5-20 | Limited adverse effect on organizational operations. Minor degradation in mission capability. Non-critical business processes experience minor delays or reduced quality. Organization can perform all functions with minimal impact. |
| VL | 0-4 | Negligible adverse effect on organizational operations. No discernible degradation in mission capability. Business processes continue normally or with imperceptible delays. |

**Category 2: Damage to Organizational Assets (Financial/Physical)**

| Level | Semi-Quant | Description |
|-------|------------|-------------|
| VH | 96-100 | Major damage to organizational assets or financial loss. Loss exceeds the organization's ability to absorb without external assistance. Physical assets destroyed or rendered permanently unusable. Financial loss threatens organizational viability. |
| H | 80-95 | Significant damage to organizational assets or financial loss. Loss is substantial and requires significant budget reallocation or emergency funding. Physical assets significantly damaged. Financial loss impacts strategic initiatives. |
| M | 21-79 | Moderate damage to organizational assets or financial loss. Loss is material but absorbable within existing budgets with reprioritization. Physical assets damaged but repairable. Financial loss impacts operational budgets. |
| L | 5-20 | Minor damage to organizational assets or financial loss. Loss is minor and within normal operating variance. Physical assets experience superficial damage. Financial loss is within discretionary spending authority. |
| VL | 0-4 | Negligible damage to organizational assets or negligible financial loss. No meaningful impact on asset value or organizational finances. |

**Category 3: Harm to Individuals**

| Level | Semi-Quant | Description |
|-------|------------|-------------|
| VH | 96-100 | Severe harm to individuals — loss of life, serious life-threatening injuries, or severe long-term consequences. Large-scale exposure of highly sensitive personal data (medical records, financial accounts, identity documents) affecting thousands or more individuals. Potential for identity theft, financial ruin, or physical danger to affected persons. |
| H | 80-95 | Significant harm to individuals — serious injury, significant financial loss, or substantial privacy violation. Exposure of sensitive personal data affecting hundreds of individuals. Significant risk of identity theft or financial harm. |
| M | 21-79 | Moderate harm to individuals — financial loss requiring significant effort to recover, moderate privacy violation, emotional distress. Exposure of personal data affecting dozens of individuals. Moderate risk of identity theft or financial harm. |
| L | 5-20 | Minor harm to individuals — inconvenience, minor financial loss easily recovered, limited privacy violation affecting few individuals. Low risk of further harm. |
| VL | 0-4 | Negligible harm to individuals — no meaningful impact on personal well-being, finances, or privacy. |

**Category 4: Harm to Other Organizations**

| Level | Semi-Quant | Description |
|-------|------------|-------------|
| VH | 96-100 | Severe harm to other organizations — the incident causes cascading failures affecting critical infrastructure partners, supply chain disruption affecting multiple downstream organizations, or breach of interconnected systems exposing partner data. |
| H | 80-95 | Significant harm to other organizations — substantial disruption to partner operations, significant partner data exposure, or supply chain impact affecting key partners. |
| M | 21-79 | Moderate harm to other organizations — noticeable disruption to partner operations, moderate partner data exposure, or supply chain delays affecting some partners. |
| L | 5-20 | Minor harm to other organizations — minimal disruption to partner operations, minor or no partner data exposure, negligible supply chain impact. |
| VL | 0-4 | Negligible harm to other organizations — no meaningful impact on any external entity. |

**Category 5: Harm to the Nation (National Security / Critical Infrastructure)**

| Level | Semi-Quant | Description |
|-------|------------|-------------|
| VH | 96-100 | Severe damage to national security interests — compromise of classified information, disruption of critical national infrastructure (power grid, water, financial systems, communications), or enabling of attacks against national defense capabilities. |
| H | 80-95 | Significant damage to national security interests — compromise of sensitive but unclassified government information, significant disruption of critical infrastructure serving large populations, or degradation of national defense supply chain. |
| M | 21-79 | Moderate damage to national security interests — limited compromise of government information, moderate disruption of critical infrastructure, or moderate impact on defense supply chain. |
| L | 5-20 | Minor damage to national security interests — minimal or indirect impact on government operations, minor disruption of regional infrastructure, negligible defense supply chain impact. |
| VL | 0-4 | Negligible damage to national security interests — no meaningful impact. Note: most private-sector organizations will rate this category VL unless they are part of critical infrastructure or government supply chain. |

**Impact Determination Process:**

For EACH risk scenario:
1. Rate impact across all 5 categories independently, citing evidence
2. Determine the OVERALL impact level:
   - Default: the HIGHEST individual category rating becomes the overall impact
   - Exception: operator may adjust downward with documented justification (e.g., Category 5 is VH but the organization is not critical infrastructure and the scenario does not realistically affect national security — the operator may override based on organizational context)
3. For Crown Jewel scenarios: cross-reference dollar valuations from step-02 to calibrate the Category 2 (Assets/Financial) rating:
   - If Crown Jewel total value > $10M: VH for Category 2 is justified if the scenario threatens the full asset value
   - If Crown Jewel total value $1M-$10M: H for Category 2 is typical
   - Calibrate based on what percentage of the asset value is at risk in this specific scenario

**Record impact determination per scenario:**

```
IMPACT DETERMINATION

| RS-# | Cat 1: Operations | Cat 2: Assets | Cat 3: Individuals | Cat 4: Other Orgs | Cat 5: Nation | Overall Impact | Semi-Quant | Crown Jewel $ Reference | Evidence |
|------|-------------------|---------------|--------------------|--------------------|---------------|----------------|------------|------------------------|----------|
| RS-001 | {{level}} | {{level}} | {{level}} | {{level}} | {{level}} | {{level}} | {{0-100}} | {{if CJ: $value}} | Step-02: {{ref}}, Step-04: {{ref}} |
```

### 7. Risk Determination (NIST 800-30, Table I-2)

Combine the overall likelihood (from section 5) with the overall impact (from section 6) using the NIST 800-30 risk determination matrix to produce the final risk level for each scenario.

**NIST 800-30 Table I-2 — Risk Determination Matrix:**

This matrix produces the authoritative risk level for each scenario. The risk level directly determines treatment priority in step-06.

```
                              LEVEL OF IMPACT
                     VL          L           M           H           VH
               +----------+----------+----------+----------+----------+
          VH   |   VL     |    L     |    M     |    H     |   VH     |
               +----------+----------+----------+----------+----------+
Overall   H    |   VL     |    L     |    M     |    H     |   VH     |
Likeli-        +----------+----------+----------+----------+----------+
hood      M    |   VL     |    L     |    M     |    M     |    H     |
               +----------+----------+----------+----------+----------+
          L    |   VL     |    L     |    L     |    L     |    M     |
               +----------+----------+----------+----------+----------+
          VL   |   VL     |   VL     |   VL     |    L     |    L     |
               +----------+----------+----------+----------+----------+
```

**Semi-Quantitative Risk Calculation:**
- Risk Semi-Quant = (Overall Likelihood Semi-Quant x Overall Impact Semi-Quant) / 100
- Map to qualitative:
  - 96-100 = VH (Very High)
  - 80-95 = H (High)
  - 21-79 = M (Moderate)
  - 5-20 = L (Low)
  - 0-4 = VL (Very Low)

**For each scenario, record the risk determination:**

```
RISK DETERMINATION

| RS-# | Scenario | Overall Likelihood | Overall Impact | Risk Level (I-2) | Semi-Quant | Confidence |
|------|----------|-------------------|----------------|------------------|------------|------------|
| RS-001 | {{scenario}} | {{VL/L/M/H/VH}} | {{VL/L/M/H/VH}} | {{VL/L/M/H/VH}} | {{0-100}} | High/Med/Low |
```

**Post-Determination Validation:**
- Review the risk determination results for internal consistency:
  - Are scenarios with similar evidence receiving similar risk levels?
  - Are Crown Jewel scenarios appropriately differentiated from Tier 3 scenarios?
  - Does the distribution make sense given the organization's threat landscape?
- If anomalies are found: investigate and document whether the anomaly reflects genuine risk differentiation or a rating error
- Present risk level distribution to operator:

```
RISK LEVEL DISTRIBUTION

Very High (VH): {{count}} scenarios ({{percentage}}%)
High (H):       {{count}} scenarios ({{percentage}}%)
Moderate (M):   {{count}} scenarios ({{percentage}}%)
Low (L):        {{count}} scenarios ({{percentage}}%)
Very Low (VL):  {{count}} scenarios ({{percentage}}%)

Total: {{count}} scenarios
```

### 8. Risk Register Population (NIST 800-30 Table I-5 Format)

Compile the master risk register — the single authoritative artifact that captures all risk calculation results. The risk register must contain sufficient detail for any qualified analyst to understand, verify, and defend every rating.

**Risk Register Schema — 17 columns minimum:**

```
| # | RS-ID | Risk Scenario Description | Threat Event (NIST Appendix E) | Threat Source | Source Type | Capability | Intent | Targeting | Relevance | Vulnerability | Vuln Severity | Predisposing Conditions | Controls & Effectiveness | Initiation Likelihood (G-2/G-3) | Adverse Impact Likelihood (G-4) | Overall Likelihood (G-5) | Impact: Operations | Impact: Assets | Impact: Individuals | Impact: Other Orgs | Impact: Nation | Overall Impact (H-3) | Risk Level (I-2) | Semi-Quant Score | Confidence | Evidence References | Notes |
```

**Due to table width constraints, present the risk register in two parts:**

**Part A — Threat & Vulnerability Context:**

```
RISK REGISTER — Part A: Threat & Vulnerability Context

| # | RS-ID | Scenario | Threat Event | Threat Source | Type | Capability | Intent | Targeting | Relevance | Vulnerability | Severity | Predisposing Conditions | Controls | Control Effectiveness |
|---|-------|----------|-------------|--------------|------|-----------|--------|-----------|-----------|--------------|----------|------------------------|----------|---------------------|
```

**Part B — Risk Scoring:**

```
RISK REGISTER — Part B: Risk Scoring & Determination

| # | RS-ID | Init/Occur Likelihood | Adverse Impact Likelihood | Overall Likelihood | Impact: Ops | Impact: Assets | Impact: Individuals | Impact: Other Orgs | Impact: Nation | Overall Impact | RISK LEVEL | Semi-Quant | Confidence | Evidence References |
|---|-------|-----------------------|---------------------------|-------------------|-------------|---------------|--------------------|--------------------|---------------|----------------|------------|------------|------------|---------------------|
```

**Risk Register Ordering:**
1. Sort by Risk Level descending: VH first, then H, M, L, VL
2. Within each risk level: sort by Semi-Quantitative score descending
3. Within the same score: Crown Jewel scenarios listed before Tier 2 before Tier 3

**Risk Register Summary Statistics:**

```
RISK REGISTER SUMMARY

Total risk scenarios: {{count}}
  Very High: {{count}} — require immediate action, FAIR analysis if hybrid approach
  High: {{count}} — require urgent treatment planning within 30 days
  Moderate: {{count}} — require treatment planning within 90 days
  Low: {{count}} — accept or batch with low priority
  Very Low: {{count}} — accept with documentation

Crown Jewel scenarios at H/VH: {{count}} / {{crown_jewel_total}} — FAIR analysis candidates
Average confidence: {{high_count}} High / {{med_count}} Medium / {{low_count}} Low
Highest risk scenario: RS-{{id}} — {{description}} — {{risk_level}}
```

### 9. Risk Heat Map Generation

Generate the 5x5 risk heat map showing the distribution of all risk scenarios across the likelihood-impact matrix. The heat map provides an immediate visual summary of the organization's risk posture.

**Heat Map Template:**

```
                                    I M P A C T
                    VL          L           M           H           VH
               +----------+----------+----------+----------+----------+
          VH   |          |          |          |          |          |
               |          |          |          |          |          |
               +----------+----------+----------+----------+----------+
  O       H    |          |          |          |          |          |
  V            |          |          |          |          |          |
  E            +----------+----------+----------+----------+----------+
  R       M    |          |          |          |          |          |
  A            |          |          |          |          |          |
  L            +----------+----------+----------+----------+----------+
  L       L    |          |          |          |          |          |
               |          |          |          |          |          |
  L            +----------+----------+----------+----------+----------+
  I       VL   |          |          |          |          |          |
  K            |          |          |          |          |          |
  E            +----------+----------+----------+----------+----------+
  L
  I
  H
  O
  O
  D
```

**Populate the heat map:**
- Place each risk scenario ID (RS-###) in the appropriate cell based on its overall likelihood (row) and overall impact (column)
- Multiple scenarios in the same cell: list all IDs separated by commas
- Crown Jewel scenarios: mark with asterisk (*) for visual distinction

**Color Zone Definitions (NIST-aligned):**

```
RISK ZONE LEGEND

Zone        | Cells                              | Risk Level | Treatment Urgency
------------|------------------------------------|-----------|---------
RED         | (VH,H), (VH,VH), (H,VH), (M,VH)  | VH        | Immediate action required — unacceptable risk
ORANGE      | (VH,M), (H,H), (M,H), (VH,L)      | H         | Urgent — plan treatment within 30 days
YELLOW      | (H,M), (M,M), (L,VH), (VL,VH),    | M         | Monitor — plan treatment within 90 days
            | (L,H), (VL,H)                      |           |
GREEN       | All remaining cells                 | L/VL      | Accept or batch with low priority
```

**Heat Map Statistics:**

```
HEAT MAP DISTRIBUTION

RED zone (VH risk):     {{count}} scenarios ({{percentage}}%) — IMMEDIATE ACTION
ORANGE zone (H risk):   {{count}} scenarios ({{percentage}}%) — URGENT (30 days)
YELLOW zone (M risk):   {{count}} scenarios ({{percentage}}%) — MONITOR (90 days)
GREEN zone (L/VL risk): {{count}} scenarios ({{percentage}}%) — ACCEPT/BATCH

Risk concentration: {{observation about where risks cluster — e.g., "majority of risks cluster in the H-likelihood / M-impact region, indicating a threat landscape with frequent but moderate-consequence events"}}
Crown Jewel exposure: {{count}} Crown Jewel scenarios in RED/ORANGE zones
```

### 10. FAIR Quantitative Deep-Dive (for H/VH Risks on Crown Jewels)

**Applicability Check:**
- If `assessment_approach` is `qualitative`: SKIP this section entirely. Proceed to section 11.
- If `assessment_approach` is `hybrid`: perform FAIR analysis ONLY for scenarios that are (1) rated H or VH in the NIST risk determination AND (2) affect a Crown Jewel asset.
- If `assessment_approach` is `fair`: perform FAIR analysis for ALL scenarios (Crown Jewels first, then other tiers).

**FAIR (Factor Analysis of Information Risk) provides what NIST 800-30 qualitative matrices cannot: dollar-denominated risk quantification with calibrated confidence ranges.** While the NIST matrix tells you a risk is "High," FAIR tells you it has a most likely annual cost of $2.3M with a 90% confidence range of $800K to $5.1M. This precision enables cost-benefit analysis for treatment decisions in step-06.

**For EACH qualifying scenario, execute the complete FAIR analysis:**

---

#### Stage 1 — Scenario Confirmation & Scoping

Before running FAIR numbers, confirm the scenario is well-defined and the data inputs are available.

```
FAIR ANALYSIS — RS-{{id}}: {{scenario_description}}

Asset: {{crown_jewel_name}} (from step-02 CJA)
Asset Value: ${{total_value}} (replacement: ${{repl}}, revenue dependency: ${{rev}}, regulatory exposure: ${{reg}})
Threat Community: {{threat_source}} (from step-03)
Threat Type: {{adversarial/non-adversarial}}
Effect: {{Confidentiality / Integrity / Availability}} breach
Vulnerability Exploited: {{vulnerability}} (from step-04)
NIST Risk Level: {{H/VH}} (from section 7)
```

**Data Sufficiency Check:**
- Are TCAP and CS scores available from step-04? Yes/No
- Is contact frequency estimable from threat characterization in step-03? Yes/No
- Are loss magnitude inputs available from Crown Jewel valuation in step-02? Yes/No
- If any critical input is missing: document the gap, use conservative estimates with wider confidence ranges, and flag the assumption

---

#### Stage 2 — Loss Event Frequency (LEF) Calculation

LEF answers: "How often does this loss event actually occur?"

**Step 2a — Threat Event Frequency (TEF):**

TEF = Contact Frequency x Probability of Action

- **Contact Frequency (CF)**: How often does the threat agent come into contact with (encounter, interact with, or have access to) this asset?
  - Sources: threat intelligence reports, industry benchmarks, organizational telemetry (e.g., number of phishing emails received per year, number of exploit attempts detected per year, number of insider access events per year)
  - Express as: events per year
  - Range: (min, likely, max) — e.g., (50, 200, 500) phishing emails per year targeting finance team

- **Probability of Action (PoA)**: Given contact, what is the probability the threat agent takes action (attempts exploitation)?
  - For adversarial threats: derived from intent and targeting (step-03)
    - Targeted attack: PoA approaches 1.0
    - Opportunistic: PoA typically 0.1-0.5
    - Untargeted/mass: PoA typically 0.01-0.1
  - For non-adversarial threats: PoA = 1.0 (errors, accidents, and environmental events do not "choose" to act — if contact occurs, the event occurs)
  - Express as: probability 0.0-1.0
  - Range: (min, likely, max)

- **TEF = CF x PoA** (events per year)
  - Calculate min, likely, max
  - Example: CF(50, 200, 500) x PoA(0.05, 0.10, 0.20) = TEF(2.5, 20, 100) threat events per year

**Step 2b — Vulnerability (FAIR Definition):**

FAIR Vulnerability is NOT the same as a CVE or technical vulnerability. In FAIR, Vulnerability is the probability that a threat event results in a loss event — it measures the gap between threat capability and control strength.

- **Threat Capability (TCAP)**: from step-04 FAIR data
  - Expressed as: percentile (0-100) representing where the threat agent falls on the capability spectrum
  - Sources: threat characterization from step-03, calibrated during step-04

- **Control Strength (CS)**: from step-04 FAIR data
  - Expressed as: percentile (0-100) representing where the control environment falls on the strength spectrum
  - Sources: control effectiveness assessment from step-04

- **FAIR Vulnerability Derivation:**
  - If TCAP > CS: Vulnerability approaches 1.0 — the threat agent is more capable than the controls can handle
  - If CS > TCAP: Vulnerability approaches 0.0 — the controls are stronger than the threat agent's capability
  - If TCAP ≈ CS: Vulnerability ≈ 0.5 — uncertain outcome, could go either way
  - Precise calculation: Vulnerability = probability that TCAP exceeds CS, accounting for uncertainty in both estimates
  - Express as: probability 0.0-1.0
  - Range: (min, likely, max)

- **LEF = TEF x Vulnerability** (loss events per year)
  - Calculate min, likely, max
  - Example: TEF(2.5, 20, 100) x Vuln(0.05, 0.15, 0.30) = LEF(0.125, 3.0, 30.0) loss events per year
  - Interpretation: "We estimate between 0.1 and 30 loss events per year from this scenario, with a most likely frequency of 3 events per year"

---

#### Stage 3 — Loss Magnitude (LM) Estimation

LM answers: "When a loss event occurs, how much does it cost?"

Reference Crown Jewel valuations from step-02 for calibration. All values expressed in dollars with (min, likely, max) ranges at 90% confidence.

**Primary Loss (direct, immediate costs incurred by the organization):**

| Loss Category | Description | Estimation Method | Min ($) | Likely ($) | Max ($) |
|---------------|-------------|-------------------|---------|------------|---------|
| **Productivity Loss** | Lost revenue or productivity during downtime/degradation | $/hour downtime x estimated hours of impact. Reference RTO/RPO from step-02 BIA. Include staff idle time, missed SLAs, delayed deliverables. | {{min}} | {{likely}} | {{max}} |
| **Response Cost** | Cost of incident response, investigation, forensics, legal counsel, PR/communications | Internal IR team hours + external retainer costs + legal counsel rates + forensic investigation fees + crisis communications. Reference industry benchmarks if no organizational data. | {{min}} | {{likely}} | {{max}} |
| **Replacement Cost** | Cost to rebuild, restore, or replace the affected asset | Rebuild from backup time + reconfiguration + validation + data re-entry if lost. Reference asset replacement cost from step-02 CJA. | {{min}} | {{likely}} | {{max}} |

**Primary Loss Total** = Productivity + Response + Replacement
- Range: (${{min}}, ${{likely}}, ${{max}})

**Secondary Loss (consequential losses that may or may not materialize):**

Secondary losses are contingent — they depend on whether external stakeholders (regulators, customers, partners, media) learn about and respond to the incident. Therefore, secondary loss is calculated as: Secondary LEF x Secondary Loss Magnitude.

- **Secondary Loss Event Frequency (SLEF)**: probability that secondary stakeholders become aware and respond
  - Factors: regulatory notification requirements, media attention likelihood, customer notification obligations, partner contractual obligations
  - Express as: probability 0.0-1.0
  - If regulatory notification is mandatory (e.g., GDPR, HIPAA, PCI): SLEF approaches 1.0 for regulatory component
  - If media attention is likely (large breach, public company, sensitive sector): SLEF approaches 1.0 for reputational component
  - Range: (min, likely, max)

| Secondary Loss Category | Description | SLEF | Min ($) | Likely ($) | Max ($) |
|------------------------|-------------|------|---------|------------|---------|
| **Fines & Judgments** | Regulatory penalties, legal settlements, contractual penalties | {{0.0-1.0}} | {{min}} | {{likely}} | {{max}} |
| **Competitive Advantage Loss** | Loss of intellectual property value, market position erosion, contract losses to competitors | {{0.0-1.0}} | {{min}} | {{likely}} | {{max}} |
| **Reputation Damage** | Customer churn, brand value erosion, increased customer acquisition cost, stock price impact | {{0.0-1.0}} | {{min}} | {{likely}} | {{max}} |

**Secondary Loss Total** = Sum of (SLEF x Secondary Loss Magnitude) per category
- Range: (${{min}}, ${{likely}}, ${{max}})

**Total Loss Magnitude (LM)** = Primary Loss + Secondary Loss
- Range: (${{min}}, ${{likely}}, ${{max}})

---

#### Stage 4 — Annual Loss Expectancy (ALE) Calculation

ALE is the bottom line: the expected annual financial exposure from this risk scenario.

**ALE = LEF x LM**

Calculate across the full range:
- ALE_min = LEF_min x LM_min
- ALE_likely = LEF_likely x LM_likely
- ALE_max = LEF_max x LM_max

**Present as calibrated statement:**
```
ANNUAL LOSS EXPECTANCY — RS-{{id}}: {{scenario}}

LEF: {{min}} to {{max}} loss events/year (most likely: {{likely}})
LM:  ${{min}} to ${{max}} per event (most likely: ${{likely}})
ALE: ${{min}} to ${{max}} per year (most likely: ${{likely}})

"There is a 90% probability that annual losses from this scenario will fall between
${{ale_min}} and ${{ale_max}}, with a most likely value of ${{ale_likely}}."
```

**Sensitivity Analysis:**
For each FAIR-analyzed scenario, identify the input variable with the greatest influence on ALE:
- If LEF dominates: risk reduction should focus on reducing threat event frequency or improving control strength
- If LM dominates: risk reduction should focus on limiting blast radius, improving response capability, or transferring financial impact
- Document which variable drives the most uncertainty in the ALE range

---

#### FAIR Analysis Summary

After completing FAIR analysis for all qualifying scenarios, present the consolidated summary:

```
FAIR QUANTITATIVE ANALYSIS SUMMARY

| # | RS-ID | Scenario | Crown Jewel | TEF (likely) | Vuln (likely) | LEF (likely) | LM Range ($) | ALE Range ($) | ALE Most Likely ($) | Key Driver |
|---|-------|----------|------------|--------------|---------------|-------------|--------------|--------------|--------------------|-----------| 
| 1 | RS-{{id}} | {{scenario}} | {{asset}} | {{tef}} | {{vuln}} | {{lef}} | {{min}}-{{max}} | {{min}}-{{max}} | {{likely}} | LEF/LM |

AGGREGATE ALE (all FAIR-analyzed scenarios):
  Total ALE (most likely): ${{total_likely}}
  Total ALE range (90% confidence): ${{total_min}} to ${{total_max}}
  
  Top 3 scenarios by ALE:
  1. RS-{{id}}: ${{ale}} — {{scenario}}
  2. RS-{{id}}: ${{ale}} — {{scenario}}
  3. RS-{{id}}: ${{ale}} — {{scenario}}

  Note: ALE values across scenarios should NOT be simply summed if scenarios are correlated
  (e.g., same threat source attacking multiple assets). Correlation between scenarios means
  the aggregate ALE may be lower than the arithmetic sum. Document known correlations.
```

**FAIR Data Quality Indicator:**

```
FAIR INPUT QUALITY

| Input | Scenarios with High-Quality Data | Scenarios with Estimated Data | Scenarios with Insufficient Data |
|-------|----------------------------------|-------------------------------|----------------------------------|
| Contact Frequency | {{count}} | {{count}} | {{count}} |
| Probability of Action | {{count}} | {{count}} | {{count}} |
| TCAP | {{count}} | {{count}} | {{count}} |
| CS | {{count}} | {{count}} | {{count}} |
| Primary Loss Components | {{count}} | {{count}} | {{count}} |
| Secondary Loss Components | {{count}} | {{count}} | {{count}} |

Overall FAIR confidence: {{High / Medium / Low}}
```

### 11. Write Section 5 to Output Document

Populate Section 5 (Risk Determination) of the output document with all calculation results. This section must be self-contained — a reader who skips directly to Section 5 must be able to understand the risk posture without reading the entire document.

**Section 5 Structure:**

```markdown
## 5. Risk Determination

### 5.1 Risk Scenario Inventory
{{scenario inventory table from section 2}}
{{total count and tier breakdown}}

### 5.2 Likelihood Analysis
#### 5.2.1 Threat Event Initiation/Occurrence (NIST Table G-2/G-3)
{{initiation/occurrence ratings from section 3 with evidence references}}

#### 5.2.2 Adverse Impact Probability (NIST Table G-4)
{{adverse impact ratings from section 4 with evidence references}}

#### 5.2.3 Overall Likelihood Determination (NIST Table G-5)
{{overall likelihood ratings from section 5 with matrix reference}}

### 5.3 Impact Analysis (NIST Table H-3)
{{impact ratings across 5 categories per scenario from section 6}}
{{overall impact determination with justification}}

### 5.4 Risk Matrix — NIST 800-30 (Table I-2)
{{completed risk determination from section 7}}
{{risk level distribution statistics}}

### 5.5 Risk Register
{{full risk register from section 8 — both Part A and Part B}}
{{risk register summary statistics}}

### 5.6 Risk Heat Map
{{5x5 heat map from section 9 with scenario placement}}
{{heat map statistics and zone distribution}}
{{risk concentration observations}}

### 5.7 FAIR Quantitative Analysis
{{if applicable: complete FAIR analysis from section 10}}
{{FAIR summary table with ALE values}}
{{aggregate ALE with confidence range}}
{{FAIR data quality indicator}}
{{if not applicable: "FAIR analysis not performed — assessment approach is qualitative only"}}

### 5.8 Annual Loss Expectancy Summary
{{if applicable: ALE ranking by scenario}}
{{top risks by financial exposure}}
{{aggregate annual financial risk exposure with confidence range}}
{{if not applicable: "ALE not calculated — assessment approach is qualitative only"}}

### 5.9 Risk Calculation Methodology Notes
{{assessment approach used}}
{{key assumptions documented}}
{{data gaps and their impact on confidence}}
{{known limitations of the analysis}}
```

**Update frontmatter with all calculated values:**

```yaml
total_risks_calculated: {{count}}
risks_very_high: {{count}}
risks_high: {{count}}
risks_moderate: {{count}}
risks_low: {{count}}
risks_very_low: {{count}}
fair_analyses_completed: {{count}} # 0 if qualitative only
total_ale: {{dollar_amount}} # null if qualitative only
risk_register_populated: true
heat_map_generated: true
```

### 12. Present MENU OPTIONS

"**Risk calculation complete.**

Risk scenarios calculated: {{total_count}}
  Very High: {{vh_count}} — immediate action required
  High: {{h_count}} — urgent treatment within 30 days
  Moderate: {{m_count}} — treatment within 90 days
  Low: {{l_count}} — accept or batch
  Very Low: {{vl_count}} — accept with documentation

Heat map: {{count}} scenarios in RED zone, {{count}} in ORANGE, {{count}} in YELLOW, {{count}} in GREEN
Crown Jewel exposure: {{count}} Crown Jewel scenarios at H/VH

{{if FAIR performed:}}
FAIR analyses completed: {{count}}
Total ALE (most likely): ${{total_ale}}
Total ALE range (90% confidence): ${{ale_min}} — ${{ale_max}}
Highest ALE scenario: RS-{{id}} — ${{ale}} — {{scenario}}
{{end if}}

Confidence: {{high_count}} High / {{med_count}} Medium / {{low_count}} Low ratings
Highest risk: RS-{{id}} — {{scenario}} — {{risk_level}}

**Select an option:**
[A] Advanced Elicitation — Challenge risk ratings and quantification assumptions
[W] War Room — Red Team challenges likelihood ratings with adversary perspective; Blue Team challenges impact assessments with defender realities; Arbiter defends quantification methodology
[C] Continue — Save and proceed to Step 6: Risk Treatment Planning"

#### Menu Handling Logic:

- **IF A (Advanced Elicitation):** Challenge risk ratings from multiple angles using Socratic questioning:
  - **Likelihood challenges:** "RS-{{id}} is rated {{level}} likelihood — what would change that rating? What evidence would move it up or down one level? Are we anchoring on the most available information rather than the most relevant?"
  - **Impact challenges:** "RS-{{id}} impact is rated {{level}} — but have we considered second-order effects? If this Crown Jewel is compromised, what cascade effects impact other assets not in this scenario?"
  - **FAIR challenges (if applicable):** "The ALE for RS-{{id}} is ${{ale}} — but the contact frequency estimate of {{cf}} per year is based on {{source}}. How reliable is that source? If CF is 2x higher, ALE becomes ${{revised_ale}}. Does that change our priorities?"
  - **Distribution challenges:** "{{percentage}}% of scenarios are rated {{level}}. Is this distribution realistic, or are we suffering from {{anchoring/inflation/deflation}} bias?"
  - **Confidence challenges:** "{{count}} ratings have Low confidence. Should we invest more effort in data gathering before finalizing, or are these low-confidence ratings in low-risk scenarios where precision does not matter?"
  Process operator responses, adjust ratings if justified (document the change and rationale), redisplay menu.

- **IF W (War Room):** Invoke spectra-war-room with risk register as context:
  - **Red Team perspective:** "Your risk register says RS-{{id}} is {{level}} likelihood. I am the threat actor described in step-03. Here is why your likelihood rating is wrong: you underestimate my capability because {{reason}}. You underestimate my intent because {{reason}}. Your controls that you rated {{effectiveness}} are actually {{weaker_assessment}} because {{reason}}. The real risk level for this scenario is {{higher_level}}."
  - **Blue Team perspective:** "Your impact assessment for RS-{{id}} assumes {{assumption}}. But our actual recovery capability is {{capability}}, and our incident response maturity is {{level}}. The real impact would be {{assessment}} because {{reason}}. Also, you missed this cascading effect: {{cascade}}."
  - **Arbiter defense:** Defend the quantification methodology against both challenges. Where challenges are valid, propose specific rating adjustments. Where challenges are unfounded, explain why the current rating is evidence-based.
  Summarize insights from all three perspectives, propose any rating adjustments, redisplay menu.

- **IF C (Continue):** Verify:
  1. Section 5 is fully populated in the output document (all subsections 5.1-5.9)
  2. Frontmatter updated with all fields (total_risks_calculated, risks per level, fair_analyses_completed, total_ale, risk_register_populated, heat_map_generated)
  3. `step-05-risk-calculation.md` added to `stepsCompleted` array
  Then read fully and follow: `./step-06-treatment.md`

- **IF user asks questions:** Answer the question using risk register data, NIST methodology, or FAIR methodology as appropriate. Redisplay menu.

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, total_risks_calculated, risks_very_high, risks_high, risks_moderate, risks_low, risks_very_low, fair_analyses_completed, total_ale, risk_register_populated, and heat_map_generated all updated, and Section 5 (Risk Determination) fully populated in the output document with subsections 5.1 through 5.9], will you then read fully and follow: `./step-06-treatment.md` to begin risk treatment planning.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All risk scenarios defined from threat-vulnerability mapping with unique (Threat Event x Vulnerability x Asset) triples
- Likelihood assessed using TWO-STEP NIST decomposition: Step A (initiation/occurrence via G-2/G-3) AND Step B (adverse impact via G-4), combined via G-5 matrix — NOT a single-step "how likely is this bad thing" assessment
- Impact assessed across ALL FIVE NIST 800-30 harm categories (Operations, Assets, Individuals, Other Organizations, Nation) per scenario — NOT a single-dimension "how bad is it" assessment
- Overall risk determined using Table I-2 matrix with both qualitative levels and semi-quantitative scores
- Risk register populated with 17+ columns per entry, sorted by risk level, with evidence references and confidence levels
- Heat map generated with risk scenario placement, color zone definitions, and distribution statistics
- FAIR quantitative analysis completed for all H/VH Crown Jewel scenarios (if assessment_approach is hybrid or fair):
  - LEF calculated from TEF (CF x PoA) and FAIR Vulnerability (TCAP vs CS)
  - LM calculated with Primary Loss (productivity, response, replacement) and Secondary Loss (SLEF x fines, competitive loss, reputation)
  - ALE calculated as LEF x LM with calibrated ranges (min, likely, max) at 90% confidence
  - Sensitivity analysis performed identifying key ALE drivers
- All ratings traceable to evidence from prior steps (step-02 asset valuations, step-03 threat characterizations, step-04 vulnerability severities and control effectiveness ratings)
- Confidence levels documented for every rating (High/Medium/Low) with criteria applied consistently
- Data gaps acknowledged with their impact on calculation confidence
- Section 5 populated in output document (subsections 5.1-5.9)
- Frontmatter updated (total_risks_calculated, risks per level, fair_analyses_completed, total_ale, risk_register_populated, heat_map_generated)
- Menu presented and user input handled correctly
- No treatment strategies proposed (reserved for step-06)
- No executive summary language written (reserved for step-07)

### SYSTEM FAILURE:

- Risk ratings without evidence traceability — a score is not an assessment if it cannot be traced to evidence. "I think this is High" is not analysis; "This is High because step-03 characterizes the threat source as high-capability (APT group) with demonstrated intent (targeted this sector 3 times in 12 months) and step-04 rates control effectiveness as minimally effective (legacy firewall with no IDS)" is analysis.
- Single-step likelihood assessment — skipping the initiation/occurrence x adverse impact decomposition produces a single "gut feel" likelihood that conflates threat frequency with control effectiveness. The two-step process is mandatory.
- Impact assessed in a single dimension — rating impact as "High" without distinguishing whether it is high for operations, assets, individuals, other organizations, or national security. A data breach with VH impact to individuals but VL impact to operations is very different from a DDoS with VH impact to operations but VL impact to individuals. The five-category assessment is mandatory.
- No risk register or incomplete register — the risk register is the deliverable of this step. Without a complete, structured register, subsequent steps have no authoritative data source.
- No heat map — the heat map is required for visual risk communication. Without it, step-07 executive summary cannot effectively communicate risk posture to leadership.
- FAIR analysis attempted without sufficient data and without documenting data quality — if FAIR inputs are guesses without confidence ranges, the output has false precision that is worse than no number. Either document data quality and confidence ranges, or fall back to qualitative.
- ALE calculated without calibrated ranges — a point estimate ALE (e.g., "$2.3M per year") without a confidence range is misleading. Always provide (min, likely, max) with stated confidence level.
- Treatment proposed in this step — risk calculation informs treatment decisions but does not make them. Proposing "we should implement MFA" or "we should patch this vulnerability" is step-06's job. This step says "the risk is High and the ALE is $2.3M." Treatment is someone else's problem, for now.
- Content generated without operator input — the operator must confirm the scenario list, review risk ratings, and make informed decisions at the menu. Autonomous risk calculation without human judgment is not a risk assessment.
- Frontmatter not updated — if the frontmatter is not updated, subsequent steps will not have accurate context about the risk calculation results.
- Proceeding without user selecting 'C' (Continue) — the operator must explicitly approve the risk calculation results before treatment planning begins.

**Master Rule:** Risk calculation is the heart of this assessment. Every rating must be defensible — traceable to evidence, calibrated with confidence levels, and documented with methodology. A risk register built on opinion is a liability, not an asset. A risk register built on evidence is the foundation for every security investment decision the organization will make. This step must be the most rigorous, most documented, and most defensible step in the entire workflow. Thoroughness here is not optional — it is the entire point.
