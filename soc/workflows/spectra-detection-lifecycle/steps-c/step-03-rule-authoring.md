# Step 3: Detection Rule Authoring

**Progress: Step 3 of 7** — Next: Test Case Development

## STEP GOAL:

Write production-quality detection rules in the appropriate format (Sigma primary, YARA for file-based, Suricata for network-based), with complete metadata, optimized detection logic based on the threat analysis from Step 2, anticipated false positive handling, and rule quality validation — producing rules ready for testing in Step 4.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER author detection rules without completed threat analysis from Step 2 — rules without threat context are blind guesses
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DETECTION ENGINEER crafting production-grade detection content, not a rule template filler
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Detection Engineer authoring detection rules that will be deployed in a production SOC environment
- ✅ Every rule must detect BEHAVIOR, not artifacts — artifacts change with every tool recompile, behaviors persist across tooling generations
- ✅ False positive management is not an afterthought — it is a core design principle. A rule with a 50% FP rate will be disabled by analysts within a week.
- ✅ Rule quality is non-negotiable — every field, every tag, every filter has a purpose. Incomplete rules create operational risk.
- ✅ Detection logic must be informed by the evasion analysis from Step 2 — if you know how an attacker evades, design around it

### Step-Specific Rules:

- 🎯 Focus exclusively on rule authoring, false positive filtering, quality validation, and variant generation — no testing or deployment yet
- 🚫 FORBIDDEN to test rules against live data or deploy to any SIEM in this step — that is Steps 4-6
- 💬 Approach: Methodical rule construction with detection logic design principles, followed by rigorous quality validation
- 📊 Every rule must include: complete metadata, detection logic, false positive filters, specific FP scenarios, and level justification
- 🔒 All detection logic must trace back to the Detection Point recommendation from Step 2 — do not arbitrarily change the detection approach without documenting the reason
- ✍️ Rule syntax must be valid and parseable — broken rules cannot be tested

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Rule uses artifact-based detection (specific hash, IP address, filename, or static string) instead of behavioral detection — warn about evasion risk since artifacts are trivially changed by adversaries (hash changes with one-byte modification, IPs rotate, filenames are arbitrary). Propose a behavioral alternative that detects the technique's observable behavior rather than the specific tool instance. Proceed with artifact-based detection if operator confirms, but document the expected shelf life and recommended review date.
  - Rule has no false positive filters (no `filter_*` conditions in Sigma, no negative conditions) — warn about analyst fatigue. A rule without exclusions will fire on every instance of the monitored behavior, including legitimate usage. Recommend adding exclusions for known legitimate patterns specific to the environment. Proceed without filters if operator confirms, noting that tuning will be required post-deployment.
  - Rule detection level set to critical or high without sufficient confidence from the Step 2 feasibility assessment — warn about alert priority inflation. If the detection confidence is Medium but the rule level is critical, analysts will lose trust in critical alerts. Recommend matching the rule level to the actual detection confidence, adjusted by technique severity. Proceed with elevated level if operator confirms with justification.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present rule authoring plan before beginning — format selection, detection logic approach, and expected rule count
- ⚠️ Present [A]/[W]/[C] menu after all rules authored and quality-checked
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `rules_authored` and `rules_format`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Detection Requirement from Step 1, Threat Analysis from Step 2 (technique decomposition, data source mapping, detection point recommendation, evasion analysis, feasibility assessment)
- Focus: Rule authoring, FP management, quality validation, and variant generation — no testing or deployment
- Limits: Author rules based on the recommended detection point and strategy from Step 2 — do not change approach without documenting the reason and getting operator acknowledgment
- Dependencies: Completed threat analysis from step-02-threat-analysis.md with GO or CONDITIONAL feasibility

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Rule Format Selection

Based on the Step 2 analysis and the detection type from the Detection Requirement, confirm the rule format(s) to author.

**Format Decision:**

| Criterion | Assessment | Selected Format |
|-----------|-----------|----------------|
| Detection point | {{detection_point_from_step_2}} | {{format_implication}} |
| Observable type | {{behavioral / file-based / network-based}} | {{Sigma / YARA / Suricata}} |
| Data source | {{primary_data_source}} | {{format_compatibility}} |
| Detection strategy | {{single / layered / correlation}} | {{single_rule / multi-rule_set}} |

**Format(s) to author:**

- **Primary:** {{Sigma / YARA / Suricata}} — {{rationale}}
- **Secondary:** {{additional_format_or_none}} — {{rationale_if_applicable}}

**Rule count estimate:**

- Primary rule: 1
- Variant rules: {{count — based on evasion paths from Step 2}}
- Correlation rules: {{count — based on technique cluster from Step 2}}
- **Total expected:** {{total}}

If multiple formats are needed, author the primary format first, then secondary formats. Each rule follows the same quality checklist.

### 2. Sigma Rule Authoring (PRIMARY PATH)

Write a complete, production-quality Sigma rule. Every field is mandatory — no placeholders, no "TODO" values.

**Sentinel's Detection Logic Design Principles:**

Before writing the rule, internalize these principles:

1. **Detect BEHAVIOR not artifacts** — Artifacts change (hashes, IPs, filenames). Behaviors persist (process creation patterns, API call sequences, registry modification patterns). Target the technique, not the tool.
2. **Use field-level conditions** — Match on specific log fields (ParentImage, CommandLine, TargetFilename), not just keyword searches. Field-level conditions are precise; keyword searches are noisy.
3. **Include negative conditions upfront** — `filter_legitimate` conditions reduce FPs from day one. Don't ship a rule that fires on svchost.exe doing its job.
4. **Use modifiers strategically** — `|contains`, `|startswith`, `|endswith`, `|re`, `|base64offset` are powerful when used correctly. Prefer `|contains` over exact match when the value may appear in a longer string. Use `|re` only when simpler modifiers cannot express the pattern.
5. **Prefer `selection AND NOT filter` pattern** — Cleaner logic, easier to tune. Each filter condition has a clear purpose that can be documented.
6. **Consider timeframe for correlation** — If the detection relies on multiple events within a window, specify `timeframe`. Without it, the correlation engine may match events hours apart.
7. **Level must match confidence** — A `critical` rule that fires on Medium-confidence detection erodes analyst trust in all critical alerts.

**Complete Sigma Rule:**

```yaml
title: {{descriptive_title — concise but specific enough to understand what it detects without reading the description}}
id: {{uuid-v4 — generate a real UUID}}
related:
  - id: {{related_rule_id — from Step 1 if tuning existing rule, or related community rule}}
    type: {{derived | obsoletes | merged | renamed | similar}}
status: experimental
description: |
  {{detailed_description — what this rule detects, why it matters, and what behavior indicates compromise}}
  {{include technique description from Step 2 — what the attacker does}}
  {{include observable behavior from Detection Requirement — what is visible in logs}}
  {{note any limitations or conditions from feasibility assessment}}
references:
  - https://attack.mitre.org/techniques/{{T_code}}/
  - {{additional_references — threat reports, blog posts, vendor advisories that describe this technique}}
  - {{procedure_example_references_from_step_2}}
author: SPECTRA SOC — {user_name}
date: {{date}}
modified: {{date}}
tags:
  - attack.{{tactic_name_lowercase_with_underscores — e.g., attack.execution}}
  - attack.{{T_code_lowercase — e.g., attack.t1059.001}}
  - detection.{{engagement_id}}
logsource:
  category: {{category — process_creation | network_connection | file_event | registry_event | dns_query | image_load | pipe_created | driver_load | file_access | etc.}}
  product: {{product — windows | linux | macos | aws | azure | gcp | etc.}}
  service: {{service — sysmon | security | system | powershell | etc. — omit if not applicable}}
  definition: >
    {{additional_requirements — e.g., "Requires Sysmon with configuration that logs process creation with command line (EventID 1)" or "Requires Windows Security audit policy: Audit Process Creation with command line logging enabled (GPO)"}}
detection:
  selection:
    {{field_1}}: {{value_or_pattern}}
    {{field_2}}:
      - {{value_1}}
      - {{value_2}}
    {{field_3|modifier}}: {{pattern}}
  filter_legitimate_{{description_1}}:
    {{field}}: {{known_legitimate_value_or_pattern}}
  filter_legitimate_{{description_2}}:
    {{field}}:
      - {{legitimate_value_1}}
      - {{legitimate_value_2}}
  condition: selection and not 1 of filter_legitimate_*
  timeframe: {{timeframe_if_applicable — e.g., 5m for correlation, omit for single-event detection}}
falsepositives:
  - >
    {{specific_false_positive_scenario_1 — NOT "legitimate use" — describe the exact scenario,
    e.g., "System administrators using PowerShell remoting (Enter-PSSession) to managed servers
    from approved jump hosts during change management windows"}}
  - >
    {{specific_false_positive_scenario_2 — e.g., "Configuration management tools (Ansible, SCCM)
    executing PowerShell scripts on endpoints during scheduled deployment windows"}}
  - >
    {{specific_false_positive_scenario_3 — e.g., "Security tools (EDR live response, vulnerability
    scanners) executing commands that match the detection pattern during authorized scans"}}
level: {{informational | low | medium | high | critical — justified by detection confidence from Step 2 and technique severity}}
```

**Detection Logic Walkthrough:**

After writing the rule, explain the logic decisions:

```
Selection Logic:
- {{field_1}}: {{value}} — why this field and value were chosen
- {{field_2}}: {{value}} — what behavior this captures
- {{modifier used}}: {{why this modifier over alternatives}}

Filter Logic:
- filter_legitimate_{{name}}: {{what legitimate behavior this excludes and why}}

Condition Design:
- Why "selection and not filter" pattern was chosen
- Why timeframe is/isn't included
- What the expected true positive to false positive ratio is

Level Justification:
- Detection confidence from Step 2: {{level}}
- Technique severity: {{level}}
- Combined assessment: {{rule_level}} — {{rationale}}
```

### 3. YARA Rule Authoring (IF FILE-BASED DETECTION)

If the Detection Requirement specifies file-based detection (malware samples, suspicious binaries, document analysis), write a complete YARA rule.

**Complete YARA Rule:**

```
rule {{rule_name}} : {{space_separated_tags}} {
    meta:
        description = "{{detailed_description_of_what_this_rule_detects}}"
        author = "SPECTRA SOC — {user_name}"
        date = "{{date}}"
        reference = "https://attack.mitre.org/techniques/{{T_code}}/"
        engagement_id = "{{engagement_id}}"
        rule_id = "{{rule_id}}"
        tlp = "amber"
        severity = "{{critical | high | medium | low}}"
        hash_sample_1 = "{{sha256_of_reference_sample_if_available}}"
        
    strings:
        $s1 = {{string_or_hex_pattern}} {{ascii | wide | nocase | fullword}}
        $s2 = {{string_or_hex_pattern}}
        $h1 = { {{hex_pattern_with_wildcards}} }
        
    condition:
        {{condition — e.g., uint16(0) == 0x5A4D and filesize < 500KB and 2 of ($s*) and $h1}}
}
```

**YARA Logic Walkthrough:**

```
String Selection:
- $s1: {{what_this_string_identifies — e.g., "unique string from malware config parser"}}
- $s2: {{what_this_string_identifies}}
- $h1: {{what_this_hex_pattern_captures — e.g., "opcode sequence for custom encryption routine"}}

Condition Design:
- File type check: {{why — e.g., "PE header check to limit scope to executables"}}
- File size constraint: {{why — e.g., "reference samples are all under 500KB"}}
- String threshold: {{why — e.g., "2 of 3 strings for resilience against minor recompilation"}}

Evasion Considerations:
- {{what_changes_would_evade_this_rule — e.g., "UPX packing would hide strings"}}
- {{mitigation — e.g., "added hex pattern for opcodes that survive packing"}}
```

### 4. Suricata Rule Authoring (IF NETWORK-BASED DETECTION)

If the Detection Requirement specifies network-based detection (traffic patterns, protocol anomalies, payload signatures), write a complete Suricata rule.

**Complete Suricata Rule:**

```
alert {{protocol}} {{src_ip}} {{src_port}} -> {{dst_ip}} {{dst_port}} (
    msg:"SPECTRA {{rule_id}} — {{descriptive_message}}";
    {{content/pcre/flow/threshold options}};
    reference:url,attack.mitre.org/techniques/{{T_code}}/;
    classtype:{{classtype}};
    sid:{{sid — unique numeric ID}};
    rev:1;
    metadata: created_by SPECTRA, engagement_id {{engagement_id}}, attack_technique {{T_code}};
)
```

**Suricata Logic Walkthrough:**

```
Traffic Matching:
- Protocol and direction: {{rationale}}
- Content match: {{what_is_matched_and_why}}
- Flow conditions: {{established/to_server/etc — why}}

Performance Considerations:
- Content ordering for fast_pattern: {{rationale}}
- Threshold to prevent alert flooding: {{if_applicable}}
```

### 5. Rule Quality Checklist

Walk through every quality check for each authored rule. ALL checks must pass before proceeding.

**Quality Checklist:**

| # | Check | Status | Notes |
|---|-------|--------|-------|
| 1 | ATT&CK technique mapped in tags | ✅/❌ | {{detail — T-code and tactic present in tags array}} |
| 2 | Detection logic targets behavior not artifacts | ✅/❌ | {{detail — what behavior is detected, confirm no hash/IP-only matching}} |
| 3 | False positive filters included | ✅/❌ | {{detail — number of filter conditions, what they exclude}} |
| 4 | Specific FP scenarios documented (not generic "legitimate use") | ✅/❌ | {{detail — each FP scenario describes a real operational situation}} |
| 5 | Log source requirements fully specified | ✅/❌ | {{detail — category, product, service, and definition all populated}} |
| 6 | Rule level matches detection confidence | ✅/❌ | {{detail — level justified by Step 2 confidence assessment}} |
| 7 | References include ATT&CK URL | ✅/❌ | {{detail}} |
| 8 | References include threat report or procedure example source | ✅/❌ | {{detail}} |
| 9 | UUID generated for rule ID | ✅/❌ | {{detail — valid UUID v4 format}} |
| 10 | Status set to experimental | ✅/❌ | {{detail — new rules always start as experimental}} |
| 11 | Tags include both tactic and technique | ✅/❌ | {{detail}} |
| 12 | Author and date set correctly | ✅/❌ | {{detail}} |
| 13 | Description is specific and actionable | ✅/❌ | {{detail — description explains what, why, and observable behavior}} |
| 14 | Log source definition specifies prerequisites | ✅/❌ | {{detail — what must be enabled/configured for this rule to work}} |
| 15 | Detection logic uses field-level conditions | ✅/❌ | {{detail — no keyword-only matching}} |
| 16 | Modifiers used correctly | ✅/❌ | {{detail — appropriate use of contains/startswith/endswith/re}} |
| 17 | Rule syntax is valid and parseable | ✅/❌ | {{detail — YAML syntax valid, no broken indentation or missing fields}} |

**Quality Gate:**

```
Checks passed: {{passed_count}} / 17
Checks failed: {{failed_count}}
```

**If ANY check fails:** Fix the rule before proceeding. Document what was changed and why. Re-run the checklist after fixing.

**Do NOT proceed past this section with any failed quality checks.**

### 6. Rule Variants (Evasion Coverage)

If the evasion analysis from Step 2 identified evasion methods that the primary rule cannot handle, author variant rules to cover those paths.

**Variant Assessment:**

| Evasion Method (from Step 2) | Primary Rule Handles? | Variant Needed? | Variant Description |
|-----------------------------|----------------------|----------------|---------------------|
| {{evasion_1}} | {{Yes/No/Partial}} | {{Yes/No}} | {{what the variant detects differently}} |
| {{evasion_2}} | {{Yes/No/Partial}} | {{Yes/No}} | {{description}} |

**For each variant needed:**

Author a complete rule following the same format as Section 2/3/4 (depending on format). Each variant:
- Gets its own UUID
- References the primary rule via the `related` field with type `similar`
- Has its own quality checklist validation
- Documents what specific evasion path it covers

**Correlation Rule (if applicable):**

If the detection strategy from Step 2 recommends correlation-based detection, author a correlation rule that combines signals from multiple detection points:

```yaml
title: {{correlation_title — describes the combined detection}}
id: {{uuid-v4}}
related:
  - id: {{primary_rule_id}}
    type: derived
status: experimental
description: |
  Correlation rule that combines {{signal_1}} and {{signal_2}} to detect {{technique}}
  with higher confidence than individual signals. Requires both conditions to occur
  on the same host within {{timeframe}}.
# ... (complete Sigma rule following same format as Section 2)
detection:
  selection_signal_1:
    {{first_signal_conditions}}
  selection_signal_2:
    {{second_signal_conditions}}
  condition: selection_signal_1 and selection_signal_2
  timeframe: {{correlation_window — e.g., 30m}}
```

**Variant Summary:**

```
Primary rule: {{rule_id}} — {{title}}
Variant rules: {{variant_count}}
Correlation rules: {{correlation_count}}
Total rules authored: {{total}}

Evasion paths covered by primary: {{primary_coverage_count}} / {{total_evasion_paths}}
Evasion paths covered by variants: {{variant_coverage_count}} / {{total_evasion_paths}}
Remaining uncovered evasion paths: {{uncovered_count}} — {{accepted_risk_rationale}}
```

### 7. Append Rules to Report and Present Menu

#### A. Append Findings to Report

Write under `## Detection Rules` in the output document:
- Format selection rationale (Section 1)
- Complete primary rule with detection logic walkthrough (Section 2/3/4)
- Quality checklist results (Section 5)
- Variant rules with individual quality checklists (Section 6, if applicable)
- Correlation rules (Section 6, if applicable)
- Variant summary with evasion coverage assessment

Update frontmatter:
- `rules_authored` with total rule count (primary + variants + correlation)
- `rules_format` array with formats used
- Add this step to `stepsCompleted`

#### B. Present Summary

"**Detection rule authoring complete.**

Rules authored: {{total_rules}}
- Primary: {{primary_count}} ({{format}})
- Variants: {{variant_count}} (evasion coverage)
- Correlation: {{correlation_count}} (multi-signal)

Quality checklist: {{passed_count}}/{{total_checks}} passed across all rules
Evasion coverage: {{covered_paths}}/{{total_paths}} known evasion paths addressed

Primary rule: `{{rule_id}}` — {{title}}
Detection point: {{detection_point}}
Level: {{level}} | Confidence: {{confidence}}
False positive filters: {{filter_count}}

All rules are ready for testing in the next step.

**Select an option:**
[A] Advanced Elicitation — Deep-dive into detection logic design, FP filter completeness, or rule optimization
[W] War Room — Red vs Blue discussion on rule evasion resilience and detection coverage
[C] Continue — Proceed to Test Case Development (Step 4 of 7)"

#### Menu Handling Logic:

- IF A: Deep-dive rule analysis — challenge the detection logic for completeness, examine whether FP filters cover all known legitimate patterns in the environment, investigate whether modifiers are optimal, assess whether the rule level is correctly calibrated, explore whether additional variant rules would improve coverage. Process insights, ask operator if they want to update rules, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: given this Sigma/YARA/Suricata rule, how would I evade it? What field values would I change? What alternative tools achieve the same technique without matching this detection logic? Can I trigger the FP filters intentionally to hide my activity? Blue Team perspective: is the detection logic tight enough to avoid FP flooding? Are the filter conditions too broad (letting real attacks through) or too narrow (not filtering enough FPs)? Should we add environment-specific filters now or wait for tuning data from testing? Is the rule level appropriate for the SOC's alert volume? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `rules_authored` and `rules_format`, then read fully and follow: ./step-04-test-cases.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and rules_authored count and rules_format updated, and detection rules appended to report under `## Detection Rules`], will you then read fully and follow: `./step-04-test-cases.md` to begin test case development.

---

## 🚨 SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Rule format(s) selected with documented rationale tracing back to Step 2 analysis
- Primary rule authored with ALL mandatory fields populated — no placeholders, no TODOs
- Detection logic follows behavioral detection principles — targets technique behavior, not specific tool artifacts
- False positive filters included with specific, operational FP scenarios (not generic "legitimate use")
- Rule level justified by detection confidence from Step 2 feasibility assessment
- Log source definition specifies prerequisite configurations (what must be enabled for the rule to work)
- Quality checklist completed for every rule with all 17 checks passing
- Failed quality checks fixed and re-validated before proceeding
- Variant rules authored for evasion paths identified in Step 2 that the primary rule cannot handle
- Correlation rules authored if the detection strategy from Step 2 recommends multi-signal detection
- Detection logic walkthrough documents the reasoning behind every selection, filter, and modifier choice
- Evasion coverage summary shows which evasion paths are addressed and which are accepted risk
- All rules appended to report under `## Detection Rules` with quality checklists
- Frontmatter updated with rules_authored count, rules_format, and step added to stepsCompleted
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Authoring rules without completed threat analysis from Step 2
- Writing detection logic based on artifacts (hashes, IPs, static strings) without warning about evasion risk
- Shipping rules without false positive filters — rules without exclusions will be disabled by analysts
- Using generic FP descriptions ("legitimate use", "normal activity") instead of specific operational scenarios
- Setting rule level to critical/high without confidence justification from Step 2
- Failing quality checklist checks and proceeding anyway
- Not generating a valid UUID for each rule
- Leaving rule status as anything other than "experimental" for new rules
- Not specifying log source prerequisites in the definition field
- Ignoring evasion paths from Step 2 without variant rules or documented accepted risk
- Testing rules against live data or deploying to SIEM during the authoring step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Detection rules are the operational output of this workflow — they must be production-quality, behaviorally grounded, FP-resilient, and fully validated against the quality checklist before advancing to testing.
