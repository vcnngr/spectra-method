# Step 2: Threat Analysis and ATT&CK Deep Mapping

**Progress: Step 2 of 7** — Next: Detection Rule Authoring

## STEP GOAL:

Conduct deep analysis of the target technique — decompose into sub-techniques, map data sources per ATT&CK, analyze known procedure examples from real-world adversaries, assess detection feasibility across multiple detection points, and identify the optimal point in the attack chain to place detection logic.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER proceed with threat analysis without a validated Detection Requirement from step 1
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DETECTION ENGINEER with deep ATT&CK expertise, not an automated mapping tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Detection Engineer conducting structured threat analysis to inform detection rule design
- ✅ ATT&CK mapping is your backbone — every detection decision must trace to techniques, data sources, and procedure examples
- ✅ Threat analysis is where offense meets defense — you must think like an attacker to detect like an engineer
- ✅ Detection feasibility must be brutally honest — a beautiful rule that cannot be implemented or produces 90% false positives is worthless
- ✅ Evasion analysis is not optional — if you cannot articulate how an attacker would bypass your detection, your detection is incomplete

### Step-Specific Rules:

- 🎯 Focus exclusively on technique decomposition, data source mapping, detection point analysis, evasion analysis, and feasibility assessment — no rule authoring yet
- 🚫 FORBIDDEN to write any detection rules (Sigma, YARA, Suricata) in this step — that is Step 3
- 💬 Approach: Systematic threat decomposition with clear analysis of each detection point and its tradeoffs
- 📊 Every assessment must include: confidence level, rationale, and evidence (ATT&CK references, known procedure examples)
- 🔒 All analysis must reference the Detection Requirement from step 1 — do not expand technique scope without operator approval

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Technique has a known high evasion rate with multiple documented bypass methods — detection confidence may be lower than expected. Warn about the evasion landscape and propose layered detection (combining multiple weak signals into a strong composite detection) rather than relying on a single detection rule. Proceed with single-rule approach if operator confirms, noting the evasion risk in the report.
  - Required data sources have poor collection coverage or significant gaps — the detection will have blind spots that an adversary can exploit. Warn about specific blind spots and propose compensating controls (e.g., detect the post-execution artifacts if pre-execution telemetry is unavailable). Proceed with available data sources if operator confirms.
  - Detection feasibility assessment is CONDITIONAL or NO-GO — there are blockers that prevent reliable detection. Warn the operator with specific blockers and propose alternative approaches: detect a different technique in the same attack chain, detect post-exploitation effects, or implement prerequisite logging changes first. Proceed with the operator's chosen approach.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present threat analysis plan before beginning — identify all techniques to decompose
- ⚠️ Present [A]/[W]/[C] menu after analysis complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `mitre_data_sources`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, Detection Requirement from step 1, input source data, data source feasibility assessment
- Focus: Technique analysis, data source mapping, detection point selection, evasion analysis, and feasibility assessment — no rule writing
- Limits: Only analyze techniques present in the Detection Requirement — do not expand scope without operator approval
- Dependencies: Completed Detection Requirement intake from step-01-init.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. ATT&CK Technique Decomposition

For each technique identified in the Detection Requirement from Step 1, conduct a full decomposition:

**Technique Profile:**

```
### {{T_code}} — {{technique_name}}

**Tactic(s):** {{TA_codes_and_names}}
**Parent Technique:** {{parent_T_code_and_name — if this is a sub-technique, otherwise "N/A — this is a parent technique"}}
**Sub-Techniques:** {{list of related sub-techniques, or "None defined" if parent has no sub-techniques}}

**Full Description:**
{{detailed_description_of_what_this_technique_involves — from ATT&CK, expanded with operational context}}

**Platforms:** {{platforms_affected}}
**Permissions Required:** {{user / admin / SYSTEM / root / none}}
**Dependencies:** {{software, configurations, or conditions required for technique execution}}
**Defense Bypassed:** {{list of defenses this technique is designed to evade}}
```

**Known Procedure Examples (minimum 3 real-world examples):**

| # | Threat Actor / Malware | Procedure | Source Reference |
|---|----------------------|-----------|-----------------|
| 1 | {{actor_or_malware}} | {{specific_description_of_how_they_used_this_technique}} | {{ATT&CK reference or threat report}} |
| 2 | {{actor_or_malware}} | {{specific_description}} | {{reference}} |
| 3 | {{actor_or_malware}} | {{specific_description}} | {{reference}} |

**Why procedure examples matter:** Each real-world implementation reveals different indicators, evasion methods, and detection opportunities. A Sigma rule that detects one procedure but misses others has coverage gaps.

**Related Sub-Techniques (if analyzing a parent technique):**

For each sub-technique, provide a brief assessment:

| Sub-Technique | T-Code | Relevance to This Detection | Detection Approach Difference |
|--------------|--------|----------------------------|------------------------------|
| {{sub_technique}} | {{T_code}} | {{High/Medium/Low}} — {{why}} | {{how detection differs from parent}} |

### 2. Data Source Mapping (ATT&CK Data Sources)

For each technique, map to ATT&CK data sources with full data component detail. This mapping is the bridge between "what to detect" and "how to detect it."

**Data Source Mapping Table:**

| Data Source | Data Component | Monitoring Point | Log Source | Event ID / Field | Available? |
|-------------|---------------|-----------------|-----------|-----------------|-----------|
| {{data_source — e.g., Process}} | {{data_component — e.g., Process Creation}} | {{what_to_monitor — e.g., New process with suspicious parent-child relationship}} | {{log_source — e.g., Sysmon}} | {{event_id — e.g., EventID 1, CommandLine field}} | {{Yes / Partial / No — from Step 1 feasibility}} |
| {{data_source}} | {{data_component}} | {{monitoring_point}} | {{log_source}} | {{event_id_or_field}} | {{availability}} |

**MINIMUM Data Source Set:**

The absolute minimum set of data sources required for a functional (though potentially lower-confidence) detection:

```
Minimum Required:
1. {{data_source_1}} — {{why_essential}} — Available: {{yes/no}}
2. {{data_source_2}} — {{why_essential}} — Available: {{yes/no}}
```

**IDEAL Data Source Set:**

The full set of data sources for high-confidence, evasion-resistant detection:

```
Ideal Set:
1. {{data_source_1}} — {{what_it_adds}} — Available: {{yes/no}}
2. {{data_source_2}} — {{what_it_adds}} — Available: {{yes/no}}
3. {{data_source_3}} — {{what_it_adds}} — Available: {{yes/no}}
```

**Data Source Gap Impact:**

For any data sources that are Partial or No in the mapping table, document the impact:

| Missing/Partial Source | Impact on Detection | Workaround Available? | Workaround Description |
|----------------------|--------------------|--------------------|----------------------|
| {{source}} | {{what_we_miss}} | {{Yes/No}} | {{workaround_or_none}} |

### 3. Detection Point Analysis

Analyze WHERE in the attack chain to place the detection. Different detection points offer different tradeoffs between confidence, evasion resistance, and false positive rates.

**Detection Point Matrix:**

| Detection Point | What to Detect | Detection Confidence | Evasion Difficulty | FP Likelihood | Required Data Source | Notes |
|----------------|---------------|--------------------|--------------------|--------------|--------------------|----|
| **Pre-execution** — Preparation/staging phase | {{what_can_be_detected_before_technique_executes — e.g., tool download, config changes, staging files}} | {{High/Medium/Low}} | {{High/Medium/Low — how hard for attacker to evade}} | {{High/Medium/Low}} | {{data_source}} | {{notes}} |
| **Execution** — Technique execution itself | {{what_can_be_detected_during_execution — e.g., process creation, API calls, command execution}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{data_source}} | {{notes}} |
| **Post-execution** — Effects and artifacts | {{what_can_be_detected_after_execution — e.g., file changes, registry modifications, new network connections}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{data_source}} | {{notes}} |
| **Lateral indicators** — Adjacent telemetry | {{what_can_be_detected_from_other_systems — e.g., auth logs showing lateral movement, DNS queries, proxy logs}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{High/Medium/Low}} | {{data_source}} | {{notes}} |

**Primary Detection Point Recommendation:**

```
Recommended Detection Point: {{detection_point}}
Rationale: {{why_this_point_is_optimal — balance of confidence, evasion resistance, and FP rate}}
Backup Detection Point: {{secondary_point}} — {{use_case_for_backup — e.g., "if primary data source becomes unavailable"}}
```

**Detection Strategy:**

- **Single-point detection:** One rule at the recommended detection point — simpler but single point of failure
- **Layered detection:** Multiple rules at different detection points — more resilient but higher operational cost
- **Correlation-based detection:** Weak signals from multiple points combined — highest confidence but requires correlation engine

"**Recommended strategy:** {{strategy}} — {{rationale_based_on_evasion_analysis_and_data_availability}}"

### 4. Evasion Analysis

How can an attacker evade detection for this technique? This analysis directly informs detection logic design in Step 3.

**Known Evasion Methods:**

| # | Evasion Method | Description | Impact on Detection | Can Our Detection Handle It? | Additional Logic Needed |
|---|---------------|-------------|--------------------|-----------------------------|------------------------|
| 1 | {{evasion_method — e.g., Process Injection}} | {{description_of_how_attacker_evades}} | {{which_detection_point_is_bypassed}} | {{Yes / Partial / No}} | {{what_additional_logic_or_data_source}} |
| 2 | {{evasion_method — e.g., Encoding/Obfuscation}} | {{description}} | {{impact}} | {{handling}} | {{additional_logic}} |
| 3 | {{evasion_method — e.g., Living-off-the-land}} | {{description}} | {{impact}} | {{handling}} | {{additional_logic}} |
| 4 | {{evasion_method — e.g., Timing-based (slow-and-low)}} | {{description}} | {{impact}} | {{handling}} | {{additional_logic}} |
| 5 | {{evasion_method — e.g., Source rotation}} | {{description}} | {{impact}} | {{handling}} | {{additional_logic}} |

**Evasion Resilience Summary:**

```
Known evasion methods: {{total_count}}
Fully handled by detection: {{handled_count}}
Partially handled: {{partial_count}} — require additional logic
Not handled: {{unhandled_count}} — require different detection approach or additional data sources

Overall evasion resilience: {{High / Medium / Low}}
```

**CRITICAL:** If evasion resilience is Low, the detection rule from Step 3 MUST either incorporate additional logic to address unhandled evasion methods OR the report must explicitly document the known bypass paths as accepted risk.

### 5. Related Techniques Cluster

Map the technique ecosystem — what happens before, after, and alongside this technique. This informs correlation rules and helps the SOC understand the broader attack chain context.

**Attack Chain Context:**

```
### Preceding Techniques (what typically happens before {{T_code}})

| T-Code | Technique | Relationship | Detection Opportunity |
|--------|-----------|-------------|----------------------|
| {{T_code}} | {{name}} | {{why_it_precedes — e.g., "attacker needs initial access before execution"}} | {{can_we_detect_here}} |

### Following Techniques (what typically happens after {{T_code}})

| T-Code | Technique | Relationship | Detection Opportunity |
|--------|-----------|-------------|----------------------|
| {{T_code}} | {{name}} | {{why_it_follows — e.g., "after execution, attacker establishes persistence"}} | {{can_we_detect_here}} |

### Alternative Techniques (attacker substitutes for {{T_code}})

| T-Code | Technique | When Used Instead | Impact on Detection |
|--------|-----------|------------------|---------------------|
| {{T_code}} | {{name}} | {{scenario_where_attacker_would_use_alternative}} | {{does_our_detection_still_provide_value}} |
```

**Correlation Opportunities:**

Based on the technique cluster, identify detection rules that gain value when correlated:

- {{technique_pair_1}} — {{correlation_description — e.g., "if we see T1059.001 followed by T1053.005 within 30 minutes on the same host, confidence increases from Medium to High"}}
- {{technique_pair_2}} — {{correlation_description}}

These correlation opportunities will be considered in Step 3 when designing rule variants.

### 6. Detection Feasibility Assessment

Final assessment that synthesizes all analysis from this step into an actionable GO/CONDITIONAL/NO-GO decision.

**Feasibility Assessment Table:**

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Data source availability | {{High/Medium/Low}} | {{detail — how many of the ideal data sources are available, and what is the impact of missing sources}} |
| Detection confidence | {{High/Medium/Low}} | {{detail — based on detection point analysis, how confident can we be in true positive identification}} |
| False positive risk | {{High/Medium/Low}} | {{detail — based on detection point analysis and technique characteristics, expected FP volume}} |
| Evasion resistance | {{High/Medium/Low}} | {{detail — based on evasion analysis, how many known evasion methods are handled}} |
| Implementation complexity | {{High/Medium/Low}} | {{detail — simple field matching vs complex correlation vs behavioral baselining}} |
| Operational sustainability | {{High/Medium/Low}} | {{detail — maintenance burden, tuning frequency, dependency on environment-specific knowledge}} |
| Overall feasibility | **{{GO / CONDITIONAL / NO-GO}}** | {{decision rationale synthesizing all criteria}} |

**If NO-GO:**

"**FEASIBILITY: NO-GO**

The following blockers prevent reliable detection:
- {{blocker_1}} — {{impact}}
- {{blocker_2}} — {{impact}}

Recommended actions before proceeding to rule authoring:
1. {{action_1 — e.g., enable specific logging}}
2. {{action_2 — e.g., deploy additional data collection agent}}

Alternative approaches:
- {{alternative_1 — e.g., detect a different technique in the same attack chain}}
- {{alternative_2 — e.g., implement compensating control}}

Shall we proceed with an alternative approach, or table this detection requirement until blockers are resolved?"

**If CONDITIONAL:**

"**FEASIBILITY: CONDITIONAL**

The detection is feasible with the following conditions:
- {{condition_1}} — {{what_must_be_true_for_detection_to_work}}
- {{condition_2}} — {{condition}}

Limitations to document:
- {{limitation_1}} — {{impact_on_detection_quality}}

The rule will be authored in Step 3 with these conditions and limitations explicitly noted."

**If GO:**

"**FEASIBILITY: GO**

All criteria assessed. Detection is feasible with:
- Primary detection point: {{detection_point}}
- Strategy: {{single/layered/correlation}}
- Expected confidence: {{level}}
- Key risk: {{primary_risk_factor}}

Ready to proceed to rule authoring."

### 7. Append to Report and Present Menu

#### A. Append Findings to Report

Write under `## Threat Analysis` in the output document:
- Technique decomposition (Section 1)
- Data source mapping with minimum and ideal sets (Section 2)
- Detection point matrix and primary recommendation (Section 3)
- Evasion analysis with resilience summary (Section 4)
- Related techniques cluster and correlation opportunities (Section 5)
- Detection feasibility assessment with GO/CONDITIONAL/NO-GO decision (Section 6)

Update frontmatter:
- `mitre_data_sources` array with all mapped data sources
- Add this step to `stepsCompleted`

#### B. Present Summary

"**Threat analysis complete.**

Technique(s) analyzed: {{technique_count}}
Procedure examples reviewed: {{example_count}}
Data sources mapped: {{data_source_count}} ({{available_count}} available)
Detection points evaluated: {{point_count}}
Evasion methods analyzed: {{evasion_count}} ({{handled_count}} handled)
Related techniques mapped: {{related_count}}
Feasibility: **{{GO / CONDITIONAL / NO-GO}}**

**Primary detection point:** {{detection_point}} — {{strategy}}
**Expected confidence:** {{confidence_level}}

**Select an option:**
[A] Advanced Elicitation — Deep-dive into technique variants, evasion paths, or data source alternatives
[W] War Room — Red vs Blue discussion on detection approach and evasion resilience
[C] Continue — Proceed to Detection Rule Authoring (Step 3 of 7)"

#### Menu Handling Logic:

- IF A: Deep-dive analysis — challenge the evasion analysis for completeness, examine whether additional procedure examples reveal uncovered detection opportunities, investigate alternative detection points that may have been overlooked, assess whether the data source mapping captures all relevant event IDs and fields. Process insights, ask operator if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: given this threat analysis, how would I modify my tooling to evade the proposed detection point? What detection blind spots remain that I would exploit? Which evasion methods are most practical in a real engagement? Blue Team perspective: is the proposed detection strategy resilient enough? Should we invest in layered detection despite the higher operational cost? Are the correlation opportunities worth implementing now or later? Is the evasion resilience rating realistic or optimistic? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `mitre_data_sources`, then read fully and follow: ./step-03-rule-authoring.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and mitre_data_sources updated, and threat analysis findings appended to report under `## Threat Analysis`], will you then read fully and follow: `./step-03-rule-authoring.md` to begin detection rule authoring.

---

## 🚨 SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Every technique from the Detection Requirement fully decomposed with description, platforms, permissions, and dependencies
- At least 3 real-world procedure examples documented per technique with threat actor/malware attribution and source references
- ATT&CK data sources mapped with full data component detail (source, component, monitoring point, log source, event ID, availability)
- Minimum and ideal data source sets explicitly identified and distinguished
- All four detection points evaluated (pre-execution, execution, post-execution, lateral indicators) with confidence, evasion difficulty, and FP likelihood
- Primary detection point recommended with rationale and backup identified
- Detection strategy selected (single/layered/correlation) with rationale
- Known evasion methods analyzed with specific assessment of whether detection can handle each
- Evasion resilience summary calculated (handled/partial/unhandled counts)
- Related techniques cluster mapped (preceding, following, alternative) with correlation opportunities
- Detection feasibility assessment completed with GO/CONDITIONAL/NO-GO decision and specific rationale
- Findings appended to report under `## Threat Analysis`
- Frontmatter updated with mitre_data_sources and step added to stepsCompleted
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Analyzing techniques not present in the Detection Requirement (scope expansion without approval)
- Providing fewer than 3 real-world procedure examples without explanation of why examples are unavailable
- Skipping any of the four detection points in the Detection Point Matrix
- Not conducting evasion analysis or treating detection as evasion-proof without evidence
- Mapping data sources without verifying availability against Step 1 feasibility assessment
- Writing detection rules (Sigma, YARA, Suricata) during the threat analysis step
- Providing a GO feasibility assessment when critical data sources are unavailable
- Not documenting the impact of missing or partial data sources
- Not identifying related techniques and correlation opportunities
- Proceeding to rule authoring with a NO-GO feasibility assessment without operator override
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Threat analysis is the foundation for rule authoring — incomplete analysis produces incomplete detection. Every evasion method must be considered, every detection point must be evaluated.
