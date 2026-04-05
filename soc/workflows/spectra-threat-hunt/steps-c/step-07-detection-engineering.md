# Step 7: Detection Engineering

**Progress: Step 7 of 8** — Next: Reporting & Closure

## STEP GOAL:

Convert validated hunt findings into lasting detection improvements — create detection rules (Sigma, YARA, Suricata, platform-native), build reusable hunt playbooks, analyze detection coverage gaps against ATT&CK, generate attack surface reduction recommendations, and produce Purple Team feedback that bridges hunting findings to Red Team testing and detection validation. This is the lasting value step — every hunt, regardless of findings, must produce detection engineering output.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER create detection rules without linking them to validated findings from step 6
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A THREAT HUNTER converting findings into engineering deliverables
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Threat Hunter who understands that the hunt's lasting value is measured by detection improvements, not just findings
- ✅ Every confirmed/suspicious finding must produce at least one detection rule — findings without rules are wasted intelligence
- ✅ Detection rules must be tested — an untested rule is a liability, not an asset
- ✅ Hunt playbooks ensure institutional knowledge survives analyst turnover — the next hunter should be able to re-run this hunt without reinventing it
- ✅ Even a hunt with zero findings produces value: refuted hypotheses reduce uncertainty, and the queries become reusable playbook content

### Step-Specific Rules:

- 🎯 Focus exclusively on detection rule creation, hunt playbook development, detection gap analysis, attack surface reduction, and Purple Team feedback
- 🚫 FORBIDDEN to perform additional hunting, data collection, or finding classification — that is complete
- 💬 Approach: Engineering precision — every rule must have correct syntax, test cases, false positive assessment, and ATT&CK mapping
- 📊 Every detection rule must include: name, ATT&CK mapping, detection logic, log source requirements, FP assessment, test case, severity
- 🔒 Rules must be grounded in actual findings — do not create speculative rules for techniques not observed

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Detection rules based solely on specific IOCs (IP addresses, domains, hashes) have a short shelf life as adversaries rotate infrastructure — always pair IOC-based rules with behavioral detection rules that detect the technique regardless of the specific indicators. IOC rules provide immediate value; behavioral rules provide lasting value.
  - Detection rules without documented false positive exclusions and test cases will degrade over time as the environment changes — every rule must include at least one known FP scenario and a test procedure to validate the rule triggers correctly. Untested rules are technical debt.
  - Closing a hunt without creating detection rules for confirmed findings means the same adversary activity could occur again without detection — the detection engineering output is the primary return on investment for the hunt operation. Even "not found" hunts should produce gap analysis and playbook content.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Create detection rules for all confirmed/suspicious findings, then develop hunt playbooks, then gap analysis
- ⚠️ Present [A]/[W]/[C] menu after all detection engineering complete
- 💾 ONLY save to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to stepsCompleted and updating `detection_rules_created`, `detection_gaps_identified`, `hunt_playbooks_created`, `purple_team_items`, `attack_surface_reduction_items`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: All hunt findings, classifications, evidence chains, ATT&CK mappings, hypotheses from steps 1-6
- Focus: Detection engineering deliverables — rules, playbooks, gap analysis, surface reduction, Purple Team feedback
- Limits: Only create rules for findings from this hunt — do not expand scope to unrelated techniques
- Dependencies: Completed finding validation from step-06-findings.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Detection Rule Creation

For each confirmed or suspicious finding, create detection rules:

"**Detection Rules — Derived from Hunt Findings:**

---

**Rule DR-001: {{descriptive rule name}}**

| Rule Field | Detail |
|-----------|--------|
| **Rule Name** | {{hunt_id}}_{{technique_shortname}}_{{descriptor}} |
| **Source Finding** | F-{{nnn}} — {{finding description}} |
| **ATT&CK Mapping** | {{T-code}}: {{technique_name}} ({{tactic}}) |
| **Detection Logic** | {{human-readable description of what the rule detects}} |
| **Log Source** | {{specific log source required}} |
| **Severity** | {{informational / low / medium / high / critical}} |
| **Confidence** | {{low / medium / high}} — based on finding validation confidence |
| **False Positive Assessment** | {{known FP scenarios and how to distinguish from true positive}} |

**Sigma Rule:**
```yaml
title: '{{Descriptive title — Technique Name via Specific Method}}'
id: {{UUID — generate unique}}
status: experimental
description: |
  Detects {{specific behavior}} as observed during threat hunt {{hunt_id}}.
  {{Additional context about why this detection matters.}}
references:
  - 'https://attack.mitre.org/techniques/{{T-code}}/'
  - '{{additional reference — threat report, blog post, advisory}}'
author: '{{user_name}} via SPECTRA threat hunt {{hunt_id}}'
date: {{YYYY/MM/DD}}
modified: {{YYYY/MM/DD}}
tags:
  - attack.{{tactic_lowercase}}
  - attack.{{T-code_lowercase}}
logsource:
  category: {{category — process_creation, network_connection, file_event, etc.}}
  product: {{product — windows, linux, etc.}}
  service: {{service — sysmon, security, etc.}}
detection:
  selection:
    {{field_1}}: '{{value_1}}'
    {{field_2}}:
      - '{{value_2a}}'
      - '{{value_2b}}'
  filter_legitimate:
    {{filter_field}}: '{{legitimate_value_to_exclude}}'
  condition: selection and not filter_legitimate
falsepositives:
  - '{{FP scenario 1 — e.g., "IT administrators using PowerShell for scheduled maintenance"}}'
  - '{{FP scenario 2 — e.g., "SCCM software deployment via certutil"}}'
level: {{informational / low / medium / high / critical}}
```

**YARA Rule (if file-based indicator found):**
```yara
rule {{hunt_id}}_{{descriptor}} {
    meta:
        description = "{{what this rule detects}}"
        author = "{{user_name}} via SPECTRA {{hunt_id}}"
        date = "{{YYYY-MM-DD}}"
        reference = "{{reference URL}}"
        hash = "{{sample hash if available}}"
        mitre_attack = "{{T-code}}"
    
    strings:
        $s1 = {{string or hex pattern}} {{modifiers}}
        $s2 = {{string or hex pattern}} {{modifiers}}
    
    condition:
        {{condition — e.g., "uint16(0) == 0x5A4D and any of ($s*)"}}
}
```

**Suricata/Snort Rule (if network indicator found):**
```
alert {{protocol}} {{src}} {{src_port}} -> {{dst}} {{dst_port}} (
    msg:"SPECTRA {{hunt_id}} — {{description}}";
    {{content/pcre/flowbits/threshold options}};
    classtype:{{classtype}};
    sid:{{SID}};
    rev:1;
    metadata:
        mitre_attack {{T-code}},
        created_at {{YYYY_MM_DD}},
        hunt_id {{hunt_id}};
)
```

**Platform-Specific Query (KQL / SPL / EQL):**
```
{{Platform-native detection query optimized for deployment as a scheduled search/analytics rule}}
```

**Test Case:**
```
Test ID: TC-DR-001
Purpose: Validate that rule DR-001 triggers correctly
Method:
  1. {{Specific steps to trigger the detection — simulate the technique}}
  2. {{Expected log generation}}
  3. {{Verify rule triggers and generates alert}}
Expected Result: Alert fires with severity {{level}} within {{timeframe}}
False Negative Test:
  1. {{Specific steps to test a technique variation}}
  2. {{Verify rule still triggers — or document the evasion if it doesn't}}
```

---

**Rule DR-002: {{next rule}}**
{{Repeat rule structure for each finding requiring a detection rule}}

---

**Detection Rules Summary:**

| Rule ID | Finding | ATT&CK | Type | Severity | FP Risk | Test Status |
|---------|---------|--------|------|----------|---------|-------------|
| DR-001 | F-001 | {{T-code}} | Sigma + {{others}} | {{level}} | {{Low/Medium/High}} | Ready for testing |
| DR-002 | F-002 | {{T-code}} | Sigma + {{others}} | {{level}} | {{Low/Medium/High}} | Ready for testing |
| ... | ... | ... | ... | ... | ... | ... |

**Total rules created:** {{count}} ({{sigma_count}} Sigma, {{yara_count}} YARA, {{suricata_count}} Suricata, {{platform_count}} platform-native)"

### 2. Hunt Playbook Creation

For each hypothesis tested, create a reusable hunt playbook:

"**Hunt Playbooks — Reusable Hunt Procedures:**

---

**Playbook HP-001: {{descriptive name — e.g., "Hunt for Cobalt Strike Beacon Activity"}}**

| Playbook Field | Detail |
|---------------|--------|
| **Playbook ID** | HP-001 |
| **Hunt Type** | {{Tactical / Strategic / Hybrid}} |
| **ATT&CK Coverage** | {{T-codes covered}} |
| **Trigger Conditions** | {{When should this hunt be re-run? — e.g., "When new Cobalt Strike C2 infrastructure is identified", "Quarterly proactive hunt", "After Purple Team exercise"}} |
| **Required Data Sources** | {{list of required data sources with minimum retention}} |
| **Estimated Duration** | {{time to execute the full playbook}} |
| **Skill Level Required** | {{L1 / L2 / L3 — minimum analyst level}} |
| **Last Executed** | {{this hunt's date}} |
| **Last Result** | {{brief summary of this hunt's findings}} |

**Query Library:**
```
{{All queries from this hunt related to this hypothesis, refined based on what worked and what didn't:}}

Query 1: {{query_id}} — {{purpose}}
- Platform: {{SIEM/EDR}}
- Status: {{Effective — produced actionable results / Refined — modified based on hunt experience / Deprecated — did not produce useful results}}
- Query: {{actual query}}
- Notes: {{what was learned about this query during the hunt}}

Query 2: {{query_id}} — {{purpose}}
...
```

**Investigation Guidance:**
```
When executing this playbook:
1. {{First investigation step — what to look for in results}}
2. {{Second investigation step — how to triage results}}
3. {{Third investigation step — when to escalate}}
4. {{Known false positives specific to this hunt}}
5. {{Expected baseline values from this hunt (for future comparison)}}
```

**Previous Results Baseline:**
```
Hunt {{hunt_id}} ({{date}}):
- Events analyzed: {{count}}
- Findings: {{summary}}
- Hypothesis verdict: {{Confirmed / Refuted / Inconclusive}}
- Note: {{any relevant context for future hunters}}
```

---

**Playbook HP-002: {{next playbook}}**
{{Repeat playbook structure}}

---

**Playbook Summary:**

| Playbook ID | Name | ATT&CK | Re-run Trigger | Queries | Last Result |
|------------|------|--------|---------------|---------|-------------|
| HP-001 | {{name}} | {{T-codes}} | {{trigger}} | {{count}} | {{result}} |
| HP-002 | {{name}} | {{T-codes}} | {{trigger}} | {{count}} | {{result}} |
| ... | ... | ... | ... | ... | ... |

**Total playbooks created:** {{count}}"

### 3. Detection Gap Analysis

"**Detection Gap Analysis:**

#### A. ATT&CK Coverage Assessment

| Tactic | Techniques Huntable | Techniques Detectable (automated rule) | Gap | Recommendation |
|--------|-------------------|--------------------------------------|-----|---------------|
| {{tactic}} | {{count huntable}} | {{count with automated detection}} | {{count gap}} | {{recommendation}} |
| ... | ... | ... | ... | ... |

**Coverage before this hunt:** {{estimated technique coverage percentage}}
**Coverage after this hunt (with new rules):** {{updated coverage percentage}}
**Net improvement:** {{delta — count of new techniques now detectable}}

#### B. Data Source Gap Analysis

| Missing/Limited Data Source | Techniques Affected | Impact on Detection | Remediation Effort | Recommendation |
|---------------------------|--------------------|--------------------|-------------------|---------------|
| {{data source}} | {{T-codes}} | {{what cannot be detected without this source}} | {{Low/Medium/High/Very High}} | {{specific recommendation}} |
| ... | ... | ... | ... | ... |

#### C. Techniques Huntable but Not Detectable

| Technique | Why Not Automatically Detectable | Hunt Frequency Needed | Automation Potential |
|-----------|--------------------------------|---------------------|-------------------|
| {{T-code}}: {{name}} | {{reason — too noisy for automated rule, requires context, needs human judgment}} | {{monthly / quarterly / semi-annually}} | {{Low — manual only / Medium — semi-automated / High — could be automated with ML/UEBA}} |

**Gap Analysis Summary:**
```
Detection rules created this hunt: {{count}}
Detection gaps identified: {{count}}
├── Data source gaps: {{count}} (require infrastructure changes)
├── Rule gaps: {{count}} (require detection engineering)
└── Capability gaps: {{count}} (require technology investment)

Techniques that remain hunt-only (no automated detection possible): {{count}}
Recommended next investment: {{highest-impact gap to close}}
```"

### 4. Attack Surface Reduction Recommendations

"**Attack Surface Reduction — Based on Hunt Findings:**

| # | Recommendation | Category | Finding Link | Effort | Impact | Priority |
|---|---------------|----------|-------------|--------|--------|----------|
| 1 | {{specific recommendation — e.g., "Disable PowerShell v2 on all endpoints to prevent downgrade attacks"}} | Configuration hardening | F-{{nnn}} | {{Low/Medium/High}} | {{impact description}} | {{Critical/High/Medium/Low}} |
| 2 | {{recommendation — e.g., "Restrict outbound DNS to corporate resolvers only to prevent DNS tunneling"}} | Network segmentation | F-{{nnn}} | {{Low/Medium/High}} | {{impact}} | {{priority}} |
| 3 | {{recommendation — e.g., "Implement LAPS to eliminate shared local admin passwords"}} | Privilege reduction | F-{{nnn}} | {{Low/Medium/High}} | {{impact}} | {{priority}} |
| 4 | {{recommendation — e.g., "Block certutil.exe for non-admin users via AppLocker/WDAC"}} | Unnecessary service reduction | F-{{nnn}} | {{Low/Medium/High}} | {{impact}} | {{priority}} |
| 5 | {{recommendation — e.g., "Enable Credential Guard on all domain-joined endpoints"}} | Configuration hardening | F-{{nnn}} | {{Low/Medium/High}} | {{impact}} | {{priority}} |
| ... | ... | ... | ... | ... | ... | ... |

**Attack surface reduction categories:**
```
Configuration hardening: {{count}} recommendations
Network segmentation: {{count}} recommendations
Privilege reduction: {{count}} recommendations
Unnecessary service/port reduction: {{count}} recommendations
Total: {{count}} recommendations
```"

### 5. Purple Team Feedback

"**Purple Team Feedback — Hunt Findings to Red/Blue Action Items:**

```yaml
# Purple Team Feedback — Threat Hunt
# Generated by: spectra-threat-hunt workflow
# Date: {{date}}

engagement_id: {{engagement_id}}
hunt_id: {{hunt_id}}
hunter: {{user_name}}
hypotheses_tested: {{count}}
hypotheses_confirmed: {{count}}
findings_confirmed_malicious: {{count}}
findings_suspicious: {{count}}
```

#### A. Red Team Testing Recommendations

```yaml
# Detection rules created — Red Team should test these
detection_tests:
  - rule_id: DR-001
    rule_name: '{{rule name}}'
    technique: '{{T-code — technique_name}}'
    test: 'Execute {{technique}} using {{alternative method}} to verify detection triggers'
    expected_result: 'Rule should fire — if it does not, the evasion variant must be documented'
    priority: {{critical / high / medium / low}}
  
  - rule_id: DR-002
    rule_name: '{{rule name}}'
    technique: '{{T-code — technique_name}}'
    test: 'Execute {{technique}} with {{specific evasion}} to test rule resilience'
    expected_result: 'Rule should still trigger despite evasion — verify detection boundary'
    priority: {{priority}}

# Evasion variants to test — will new rules survive technique variation?
evasion_tests:
  - technique: '{{T-code}}'
    current_detection: '{{what the new rule detects}}'
    evasion_variant: '{{specific alternative method that might bypass the rule}}'
    test: 'Attempt {{technique}} using {{evasion_variant}} and verify whether detection triggers'
    expected_result: '{{Detection should/should not trigger — document the boundary}}'
    priority: {{priority}}

# Detection gaps for Red Team to exploit in future assessments
detection_gaps:
  - tactic: '{{TA00XX — tactic_name}}'
    technique: '{{T-code — technique_name}}'
    gap: '{{what is not detected and why}}'
    red_team_action: 'Exploit this gap in next assessment to demonstrate risk'
    priority: {{priority}}
```

#### B. Hunt Findings for Red Team Attack Planning

```yaml
# Findings that inform Red Team operations
attack_planning_intel:
  - finding: '{{description of environmental weakness discovered during hunt}}'
    implication: '{{how a Red Team could leverage this}}'
    technique: '{{T-code}}'
    priority: {{priority}}

# Confirmed blind spots — areas where hunting could not detect
blind_spots:
  - area: '{{specific blind spot — e.g., "No visibility into container-to-container traffic"}}'
    impact: '{{what adversary activity could occur undetected}}'
    remediation: '{{what would be needed to close this blind spot}}'
```

#### C. Blue Team Action Items

```yaml
# Detection engineering backlog
detection_backlog:
  - item: '{{rule to create/tune}}'
    priority: {{priority}}
    estimated_effort: '{{hours}}'
    technique: '{{T-code}}'
  
# Data source improvements needed
data_source_improvements:
  - source: '{{data source name}}'
    current_state: '{{what is available now}}'
    desired_state: '{{what is needed}}'
    impact: '{{what detection capability this enables}}'
    priority: {{priority}}

# Hunt program recommendations
hunt_program:
  - recommendation: '{{periodic re-hunt recommendation}}'
    frequency: '{{monthly / quarterly / semi-annually}}'
    playbook: 'HP-{{nnn}}'
    trigger: '{{what should trigger this hunt}}'
```"

### 6. Present MENU OPTIONS

"**Detection engineering complete.**

Summary:
- Detection rules created: {{count}} ({{sigma}} Sigma, {{yara}} YARA, {{suricata}} Suricata, {{native}} platform-native)
- Hunt playbooks created: {{count}}
- Detection gaps identified: {{count}}
- Attack surface reduction items: {{count}}
- Purple Team items: {{count}}
- ATT&CK coverage improvement: {{before}}% → {{after}}%

**Select an option:**
[A] Advanced Elicitation — Review rule quality, test case coverage, gap analysis completeness
[W] War Room — Red vs Blue discussion on detection improvements and residual risk
[C] Continue — Proceed to Reporting & Closure (Step 8 of 8 — FINAL)"

#### Menu Handling Logic:

- IF A: Deep-dive detection engineering — review each rule for evasion resistance, examine test cases for completeness, challenge whether gap analysis covers all relevant techniques, assess whether attack surface reduction recommendations are actionable and properly prioritized, verify hunt playbooks are detailed enough for a different analyst to execute. Process insights, ask user if they want to update rules or analysis, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: which of these new detection rules would concern me most? Which can I trivially bypass? Are the evasion tests comprehensive enough or am I holding back my best techniques? What detection gaps remain that I would prioritize exploiting? If I were planning the next operation against this organization, what would I change based on this hunt's detection improvements? Blue Team perspective: are these rules production-ready or do they need tuning? What is the expected FP rate in our environment? Do we have the infrastructure to deploy all recommended rules? What's the priority order for detection gap remediation? How do we maintain these rules over time? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `detection_rules_created`, `detection_gaps_identified`, `hunt_playbooks_created`, `purple_team_items`, `attack_surface_reduction_items`. Append detection engineering to report under `## Detection Engineering`. Then read fully and follow: ./step-08-reporting.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and all detection engineering counts updated, and detection engineering details appended to report under `## Detection Engineering`], will you then read fully and follow: `./step-08-reporting.md` for final reporting and workflow closure.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Detection rules created for all confirmed/suspicious findings with Sigma as baseline format
- Each rule includes: name, ATT&CK mapping, detection logic explanation, log source requirements, FP assessment, test case, severity
- Additional rule formats provided where relevant (YARA for files, Suricata for network, platform-native for deployment)
- Hunt playbooks created for each hypothesis with: trigger conditions, query library, investigation guidance, previous results
- Detection gap analysis performed with ATT&CK coverage before/after assessment
- Data source gaps documented with remediation recommendations
- Attack surface reduction recommendations provided with finding links, effort, and priority
- Purple Team feedback includes: detection tests, evasion variants, gap exploitation recommendations, hunt program recommendations
- All detection engineering content appended to report under `## Detection Engineering`
- Frontmatter updated with all detection engineering counts and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Creating detection rules without linking to validated findings
- Rules without false positive assessment or test cases (untested rules are liabilities)
- IOC-only rules without behavioral alternatives (short shelf life)
- Not creating hunt playbooks (institutional knowledge lost)
- Not performing detection gap analysis (missed improvement opportunities)
- Not providing Purple Team feedback (breaking the Red-Blue feedback loop)
- Rules with incorrect Sigma syntax or invalid field names
- Performing additional hunting or data collection during detection engineering
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every confirmed finding must produce a detection rule. Every hypothesis must produce a hunt playbook. Every hunt must produce detection gap analysis. The detection engineering output is the hunt's lasting return on investment.
