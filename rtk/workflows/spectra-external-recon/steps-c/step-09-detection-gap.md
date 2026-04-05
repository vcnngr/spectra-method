# Step 9: Detection Gap Analysis (Purple Team Hook)

**Progress: Step 9 of 10** — Next: Workflow Completion

## STEP GOAL:

Analyze what the target SOC should detect from this reconnaissance activity. This is the critical purple team bridge — connecting Red Team Kit (RTK) output to SOC module input. For every recon technique used, assess detection likelihood and recommend Sigma rules for gaps.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER skip detection analysis for any technique used — completeness is critical
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RECONNAISSANCE SPECIALIST with purple team awareness
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Reconnaissance Specialist with deep understanding of both attack and defense
- ✅ This step is the purple team handoff — your output feeds directly into SOC module
- ✅ Be honest about detection gaps — the goal is to improve defensive posture
- ✅ Sigma rules should be actionable and implementable by the SOC
- ✅ ATT&CK data sources and detection references are your foundation

### Step-Specific Rules:

- 🎯 Focus on detection analysis, gap identification, and Sigma rule recommendations
- 🚫 FORBIDDEN to perform any new reconnaissance or scanning
- 💬 Approach: For each technique used, assess blue team detection capability
- 📊 Every technique must have: detection assessment, confidence, and recommendation
- 🔗 This step's output is designed as direct input for SPECTRA SOC module

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Skipping this step even if the operator says "just red team, no blue" — detection gap analysis is what separates professional red teaming from adversary simulation theater; purple team awareness is mandatory
  - Assessing detection capabilities without the ATT&CK mapping from step 08 — detection analysis requires technique-to-datasource correlation, which is impossible without structured ATT&CK data
  - Marking detection as "adequate" without evidence from log source analysis — detection adequacy claims must be backed by specific data source availability and rule coverage assessment
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present detection analysis plan before beginning
- ⚠️ Present [A]/[W]/[C] menu after analysis complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Complete target package and ATT&CK mapping from step 8
- Focus: Detection analysis and Sigma rule recommendations only
- Limits: Work with techniques already documented — no new recon
- Dependencies: ATT&CK technique mapping from step-08-target-package.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Compile Technique Inventory

**From step 8 ATT&CK mapping, list ALL techniques used during this engagement:**

"**Reconnaissance Technique Inventory**

ATT&CK techniques used in this engagement:

| # | T-Code | Technique | Step Used | Activity Description |
|---|--------|-----------|-----------|---------------------|
{{for each technique}}
| {{n}} | {{T_code}} | {{technique_name}} | Step {{step_number}} | {{activity_description}} |
{{/for}}

Total techniques: {{technique_count}}

Proceeding with detection analysis for each technique?"

### 2. Detection Assessment per Technique

**For EACH technique in the inventory, assess SOC detection capability:**

**Assessment Framework:**

For each T-code, evaluate:

1. **Data Sources Required** — What log sources would detect this technique?
   - Network traffic logs (firewall, IDS/IPS, NetFlow)
   - DNS query logs
   - Web server/application logs
   - Cloud provider logs (CloudTrail, Azure Activity Log)
   - Endpoint detection logs
   - Email gateway logs

2. **Detection Likelihood** — Would a typical SOC detect this?
   - **High**: Standard SIEM rules would trigger (e.g., port scan detection)
   - **Medium**: Requires tuned rules or correlation (e.g., subdomain brute-force)
   - **Low**: Requires specialized monitoring (e.g., passive OSINT — no target-side logs)
   - **None**: No target-side artifact generated (e.g., whois lookup, CT log query)

3. **Evasion Potential** — How easy is it to evade detection?
   - Rate limiting to stay below thresholds
   - Source IP rotation
   - Legitimate-looking user agents
   - Encrypted channels
   - Time-based evasion (slow scanning)

**Document per technique:**
```
### {{T_code}} — {{technique_name}}

**Activity performed:** {{activity_description}}
**Required data sources:** {{required_data_sources}}
**Estimated detection:** {{High/Medium/Low/None}}
**Assessment confidence:** {{confidence_level}}
**Evasion potential:** {{evasion_assessment}}
**Target-side artifacts:** {{target_side_artifacts}}
```

### 3. Detection Gap Identification

**Identify gaps where the SOC likely WOULD NOT detect the recon:**

**Classify gaps:**

| Gap Type | Description | Impact |
|----------|-------------|--------|
| **Blind** | No log generated on target side | SOC cannot detect with any configuration |
| **Unmonitored** | Logs available but typically not collected | Requires new data source in SIEM |
| **Uncorrelated** | Logs collected but no correlation rule | Requires new SIEM/Sigma rule |
| **Threshold** | Activity below alerting threshold | Requires threshold tuning |
| **Context** | Activity blends into legitimate traffic | Requires advanced behavioral analysis |

**Gap Summary:**
```
| T-Code | Technique | Gap Type | Severity | Recommendation |
|--------|-----------|----------|----------|----------------|
```

### 4. Sigma Rule Recommendations

**For each identified gap (non-blind), recommend a Sigma rule:**

**Sigma Rule Template:**
```yaml
title: {{rule_title}}
id: {{uuid}}
status: experimental
description: {{description}}
references:
  - https://attack.mitre.org/techniques/{{T_code}}/
author: SPECTRA RTK
date: {{date}}
tags:
  - attack.reconnaissance
  - attack.{{T_code_lowercase}}
logsource:
  category: {{log_category}}
  product: {{product}}
detection:
  selection:
    {{detection_logic}}
  condition: selection
  timeframe: {{timeframe}}
falsepositives:
  - {{false_positive_description}}
level: {{low/medium/high/critical}}
```

**For each gap, provide:**
- Sigma rule in proper format
- Required log source
- Expected false positive rate
- Tuning recommendations
- Implementation priority

### 5. SOC Module Handoff Package

**Prepare the structured handoff for SPECTRA SOC module:**

**Handoff Data:**
```yaml
engagement_id: {{engagement_id}}
recon_techniques_used:
  {{for each technique}}
  - t_code: {{T_code}}
    technique: {{name}}
    detection_status: {{detected/gap}}
    gap_type: {{gap_type if applicable}}
    sigma_rule_id: {{sigma_rule_id if recommended}}
  {{/for}}
detection_gaps:
  total: {{gap_count}}
  blind: {{blind_count}}
  actionable: {{actionable_count}}
  sigma_rules_recommended: {{sigma_count}}
recommended_data_sources:
  {{list of data sources needed to close gaps}}
```

### 6. Detection Coverage Score

**Calculate overall detection coverage:**

```
Total techniques used: {{total_techniques}}
Detectable techniques (High/Medium): {{detectable_count}}
Detection gaps: {{gap_count}}
Blind gaps (non-remediable): {{blind_count}}
Actionable gaps: {{actionable_count}}

**Coverage Score: {{detectable_count / total_techniques * 100}}%**
**Post-remediation Score: {{(detectable_count + actionable_count) / total_techniques * 100}}%**
```

### 7. Append Findings to Report

Write under `## Detection Gap Analysis`:

```markdown
## Detection Gap Analysis

### Summary
- Reconnaissance techniques used: {{technique_count}}
- Techniques detectable by SOC: {{detectable_count}}
- Detection gaps identified: {{gap_count}}
  - Blind gaps: {{blind_count}}
  - Actionable gaps: {{actionable_count}}
- Sigma rules recommended: {{sigma_count}}
- Current coverage score: {{coverage_score}}%
- Post-remediation coverage score: {{post_remediation_score}}%

### Detection Assessment per Technique
{{per_technique_detection_assessment}}

### Detection Gaps
{{gap_identification_table}}

### Recommended Sigma Rules
{{sigma_rules}}

### Detection Coverage Score
{{coverage_calculation}}

### SOC Module Handoff Package
{{soc_handoff_yaml}}

### Priority Recommendations for SOC
1. {{priority_recommendation_1}}
2. {{priority_recommendation_2}}
3. {{priority_recommendation_3}}
...
```

Update frontmatter:
- `detection_gaps_identified` with total gap count

### 8. Present MENU OPTIONS

"**Detection gap analysis complete.**

Current coverage: {{coverage_score}}% | Post-remediation: {{post_remediation_score}}%
Total gaps: {{gap_count}} ({{blind_count}} blind, {{actionable_count}} actionable)
Sigma rules recommended: {{sigma_count}}

**This output is ready to be consumed by the SPECTRA SOC module.**

**Select an option:**
[A] Advanced Elicitation — In-depth analysis of critical gaps
[W] War Room — Red vs Blue discussion on detection coverage
[C] Continue — Proceed to Workflow Completion (Step 10 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — detection evasion strategy assessment, Sigma rule efficacy prediction, false positive impact analysis, detection engineering maturity assessment of the target SOC. Redisplay menu
- IF W: War Room — This is the ULTIMATE War Room moment. Red: which gaps would you exploit for persistence? How would you modify techniques to avoid the detectable ones? Blue: prioritization of Sigma rule deployment, data source acquisition roadmap, detection engineering sprint planning. This discussion should be rich and detailed. Summarize, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted and updating detection_gaps_identified, then read fully and follow: ./step-10-complete.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and detection_gaps_identified updated], will you then read fully and follow: `./step-10-complete.md` to complete the workflow.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Complete technique inventory compiled from ATT&CK mapping
- Every technique assessed for SOC detection likelihood
- Detection gaps classified by type (blind, unmonitored, uncorrelated, threshold, context)
- Sigma rules recommended for all actionable gaps
- SOC module handoff package prepared in structured format
- Detection coverage score calculated (current and post-remediation)
- Prioritized recommendations provided for SOC improvement
- detection_gaps_identified updated in frontmatter

### ❌ SYSTEM FAILURE:

- Skipping detection assessment for any technique used
- Not providing Sigma rules for actionable gaps
- Not preparing SOC module handoff package
- Not calculating detection coverage scores
- Performing any new reconnaissance during analysis
- Not classifying gaps by type
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every technique needs a detection assessment — no exceptions.
