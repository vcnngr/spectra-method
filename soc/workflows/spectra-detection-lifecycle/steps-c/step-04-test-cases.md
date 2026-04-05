# Step 4: Test Case Design

**Progress: Step 4 of 7** — Next: Validation and Tuning

## STEP GOAL:

Design comprehensive test cases that validate the detection rule fires on true positives and does NOT fire on known false positive scenarios — following Sentinel's golden rule: "A detection rule without a test case is a hope, not a control."

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate test cases without a validated detection rule from Step 3 — test cases must be derived from actual rule logic, not hypothetical detection
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DETECTION ENGINEER, not an automated test generator — you facilitate structured test design with operator oversight
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Detection Engineer collaborating with an expert peer on test case design within an active security engagement
- ✅ Test cases are the contract between detection intent and detection reality — they prove the rule works as designed
- ✅ True positive tests alone create a false sense of security — false positive and evasion tests reveal the rule's actual operational profile
- ✅ Every test case must be reproducible — vague descriptions like "run the attack" are not test cases, they are wishes
- ✅ Evasion test cases are not optional luxuries — they define the boundaries of the detection and expose known gaps before adversaries do

### Step-Specific Rules:

- 🎯 Focus exclusively on test case design across all five categories: true positive, true negative, false positive, evasion, and edge case
- 🚫 FORBIDDEN to execute any test cases — design only, execution belongs to Step 5
- 🚫 FORBIDDEN to modify detection rule logic — if test design reveals rule issues, document them for Step 5 tuning
- 💬 Approach: Systematic derivation of test cases from rule logic, detection requirements, false positive documentation, and evasion analysis
- 📊 Every test case must include: unique ID, simulation method, expected result, prerequisites, and validation criteria
- 🔒 Test cases must reference specific rule fields and conditions — generic "attack simulation" is insufficient

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Test cases only cover the happy path (basic TP) without evasion or edge cases — warn about false sense of security; the rule passes easy tests but may miss real attacks that use encoding variants, alternative tools, or timing manipulation to bypass the exact conditions the rule checks
  - No true negative test cases defined — warn that without TN tests, the false positive rate is unknown until production deployment; FP storms destroy analyst trust faster than missed detections, and TN tests are the only pre-deployment safeguard against alert fatigue
  - Test prerequisites include data sources not currently available in the environment — warn that tests cannot be validated, rendering the entire test suite theoretical; recommend phased deployment where logging prerequisites are met first, or document the gap as an acceptance risk
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present test strategy overview before designing individual test cases
- ⚠️ Present [A]/[W]/[C] menu after all test categories are complete and summary is presented
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `test_cases_total` with the total number of test cases designed
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Detection requirement from Step 1, threat analysis and evasion techniques from Step 2, detection rule(s) with logic, fields, false positives, and metadata from Step 3
- Focus: Test case design across TP, TN, FP, evasion, and edge case categories — no test execution, no rule modification
- Limits: Only design tests for rules authored in Step 3 — do not invent rules or test hypothetical detections
- Dependencies: Completed detection rule(s) from step-03-rule-authoring.md with valid syntax and documented false positive patterns

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Test Strategy Definition

Review the detection rule(s) from Step 3 and define the test strategy. For each rule, extract the specific conditions, fields, thresholds, and false positive patterns that must be tested.

**Present the test strategy to the operator:**

```
Rule Under Test: {{rule_id}} — {{rule_title}}
Rule Format: {{sigma / yara / suricata}}
Detection Logic Summary: {{brief description of what the rule detects and how}}

Test Strategy:
┌─────────────────────────┬──────────┬──────────────────────────────────────────┐
│ Category                │ Target # │ Derivation Source                        │
├─────────────────────────┼──────────┼──────────────────────────────────────────┤
│ True Positive (TP)      │ ≥3       │ Rule conditions + technique variations   │
│ True Negative (TN)      │ ≥2       │ Normal operations resembling the attack  │
│ False Positive (FP)     │ ≥1 per   │ Rule falsepositives section              │
│                         │ FP entry │                                          │
│ Evasion                 │ ≥1 per   │ Step 2 evasion analysis                  │
│                         │ evasion  │                                          │
│ Edge Case               │ ≥2       │ Rule field types + boundary conditions   │
└─────────────────────────┴──────────┴──────────────────────────────────────────┘

ATT&CK Technique: {{T-code — technique_name}}
Primary Log Source: {{log_source}}
Platform: {{os / environment}}
```

**Key rule conditions to test:**
1. {{condition_1 — e.g., specific process name match}}
2. {{condition_2 — e.g., command line argument pattern}}
3. {{condition_3 — e.g., parent process relationship}}
4. {{additional conditions as applicable}}

**Documented false positive patterns to validate exclusions:**
1. {{fp_pattern_1 from rule falsepositives section}}
2. {{fp_pattern_2}}
3. {{additional FP patterns as applicable}}

**Known evasion techniques from Step 2:**
1. {{evasion_1 — e.g., command obfuscation}}
2. {{evasion_2 — e.g., alternative tool for same technique}}
3. {{additional evasions as applicable}}

"**Test strategy defined.** Proceeding to design individual test cases for each category."

### 2. True Positive Test Cases

For each detection rule, design at minimum 3 true positive test cases. These are the baseline: if ANY TP test fails during validation, the rule is broken.

**For each TP test case, present:**

```
┌──────────────────────┬─────────────────────────────────────────────────────┐
│ Test ID              │ TP-{{rule_id}}-{{NNN}}                             │
├──────────────────────┼─────────────────────────────────────────────────────┤
│ Test Name            │ {{descriptive_name}}                               │
│ Description          │ {{what this test validates — specific rule          │
│                      │ condition being exercised}}                        │
│ ATT&CK Technique     │ {{T-code — technique_name}}                        │
│ Simulation Method    │ {{exact command, tool invocation, or script to     │
│                      │ generate the event — must be reproducible}}        │
│ Expected Log Source  │ {{where the event appears — e.g., Sysmon EventID   │
│                      │ 1, Windows Security 4688, Zeek conn.log}}         │
│ Expected Log Fields  │ {{specific field:value pairs the rule matches}}    │
│ Expected Result      │ ALERT — rule fires with {{expected_severity}}      │
│ Platform             │ {{OS version / environment}}                       │
│ Prerequisites        │ {{logging config, agent version, permissions,      │
│                      │ required software}}                                │
│ Cleanup              │ {{post-test cleanup actions if needed}}            │
└──────────────────────┴─────────────────────────────────────────────────────┘
```

**Minimum TP test coverage:**

1. **Vanilla execution** — The technique executed in its most basic, textbook form. This is the "if this doesn't trigger, the rule is fundamentally broken" test.
2. **Common parameter variation** — The technique executed with commonly observed parameters, flags, or arguments that differ from the vanilla case but should still match the rule logic.
3. **Different target context** — The technique targeting a different asset type, user privilege level, or environment configuration (if applicable to the rule scope).

Present all TP test cases in sequence with full detail per case.

**TP Test Summary:**
```
Total TP tests designed: {{count}}
Rule conditions covered: {{list of conditions each test exercises}}
Uncovered conditions: {{any rule conditions not exercised by TP tests — flag for review}}
```

### 3. True Negative Test Cases

Design at minimum 2 true negative test cases. These represent normal, legitimate operations that resemble the attack pattern but are NOT malicious. If ANY TN test fires an alert, the rule is too broad.

**For each TN test case, present:**

```
┌──────────────────────┬─────────────────────────────────────────────────────┐
│ Test ID              │ TN-{{rule_id}}-{{NNN}}                             │
├──────────────────────┼─────────────────────────────────────────────────────┤
│ Test Name            │ {{descriptive_name}}                               │
│ Description          │ {{what legitimate activity this represents and     │
│                      │ why it resembles the attack pattern}}              │
│ ATT&CK Technique     │ N/A — legitimate activity                          │
│ Simulation Method    │ {{exact command or action to generate the          │
│                      │ legitimate event}}                                 │
│ Expected Log Source  │ {{same log source as the rule monitors}}           │
│ Expected Log Fields  │ {{field values — showing what differs from the     │
│                      │ malicious pattern}}                                │
│ Expected Result      │ NO ALERT — rule must NOT fire                      │
│ Key Differentiator   │ {{specific field or condition that distinguishes   │
│                      │ this from the malicious pattern}}                  │
│ Platform             │ {{OS version / environment}}                       │
│ Prerequisites        │ {{same logging config as TP tests}}               │
└──────────────────────┴─────────────────────────────────────────────────────┘
```

**TN test design rationale:**
- TN tests should use the SAME log source and SIMILAR process/activity patterns as the attack — they test the rule's specificity
- A rule that cannot distinguish between malicious and legitimate use of the same tools is operationally useless
- Focus on the most common legitimate activities that share characteristics with the detected technique

Present all TN test cases in sequence.

**TN Test Summary:**
```
Total TN tests designed: {{count}}
Legitimate patterns covered: {{list of normal activities tested}}
Risk assessment: {{how likely are these patterns in production — high/medium/low frequency}}
```

### 4. False Positive Test Cases

For each documented false positive in the rule's `falsepositives` section from Step 3, design a test case that validates the exclusion or filter works correctly. If ANY FP test fires an alert, the filter is broken.

**For each FP test case, present:**

```
┌──────────────────────┬─────────────────────────────────────────────────────┐
│ Test ID              │ FP-{{rule_id}}-{{NNN}}                             │
├──────────────────────┼─────────────────────────────────────────────────────┤
│ Test Name            │ {{descriptive_name}}                               │
│ Description          │ {{which documented false positive pattern this     │
│                      │ validates}}                                        │
│ ATT&CK Technique     │ N/A — known false positive pattern                 │
│ Simulation Method    │ {{exact command or action that triggers the        │
│                      │ documented FP pattern}}                            │
│ Expected Log Source  │ {{same log source as the rule monitors}}           │
│ Expected Log Fields  │ {{field values matching the FP pattern}}           │
│ Expected Result      │ NO ALERT — filter/exclusion should prevent firing  │
│ Filter Being Tested  │ {{specific exclusion condition in the rule that    │
│                      │ should suppress this pattern}}                     │
│ FP Source            │ {{reference to falsepositives entry in rule}}      │
│ Platform             │ {{OS version / environment}}                       │
│ Prerequisites        │ {{specific software or config that generates       │
│                      │ this FP pattern}}                                  │
│ Risk if Filter Fails │ {{impact — alert volume, analyst fatigue,          │
│                      │ trust degradation}}                                │
└──────────────────────┴─────────────────────────────────────────────────────┘
```

**Why this is a legitimate pattern:**
{{Detailed explanation of why this activity is benign and expected in production environments — e.g., "Administrative tools routinely invoke this process during scheduled maintenance, generating events that match the detection pattern but lack the malicious context."}}

Present all FP test cases in sequence.

**FP Test Summary:**
```
Total FP tests designed: {{count}}
Documented FP patterns covered: {{count}} of {{total_documented_FPs}}
Uncovered FP patterns: {{any documented FPs without test cases — flag as risk}}
```

### 5. Evasion Test Cases

For each evasion technique identified in Step 2's threat analysis, design a test case that attempts to bypass the detection rule. These tests define the rule's detection boundary — what it catches and what it misses.

**For each evasion test case, present:**

```
┌──────────────────────┬─────────────────────────────────────────────────────┐
│ Test ID              │ EV-{{rule_id}}-{{NNN}}                             │
├──────────────────────┼─────────────────────────────────────────────────────┤
│ Test Name            │ {{descriptive_name}}                               │
│ Description          │ {{what evasion method is being tested and how      │
│                      │ it attempts to bypass the rule}}                   │
│ ATT&CK Technique     │ {{T-code — technique_name (same as rule)}}         │
│ Evasion Method       │ {{name and description of evasion technique}}      │
│ Simulation Method    │ {{exact command or tool invocation using the       │
│                      │ evasion method — must be reproducible}}            │
│ Expected Log Source  │ {{where the evaded event would appear, if at all}} │
│ Expected Log Fields  │ {{field values as modified by the evasion}}        │
│ Expected Result      │ ALERT (rule catches despite evasion) /             │
│                      │ KNOWN GAP (evasion succeeds — rule does not fire)  │
│ Gap Justification    │ {{if KNOWN GAP: why the rule cannot catch this     │
│                      │ variant and what would be needed}}                 │
│ Compensating Control │ {{if KNOWN GAP: other detection that covers this   │
│                      │ evasion, or "NONE — gap exists"}}                  │
│ Platform             │ {{OS version / environment}}                       │
│ Prerequisites        │ {{evasion tool, encoding utility, permissions}}    │
└──────────────────────┴─────────────────────────────────────────────────────┘
```

**Evasion categories to consider:**

- **Command obfuscation** — environment variable substitution, caret insertion, string concatenation, encoding
- **Tool substitution** — same technique achieved via different binary, script, or living-off-the-land alternative
- **Process injection / indirect execution** — technique launched from unexpected parent process or via DLL sideloading
- **Timing manipulation** — slow execution, delayed staging, split across multiple sessions
- **Log evasion** — technique executed in a way that avoids generating the expected log event entirely
- **Encoding variants** — base64, hex, Unicode, double encoding of the detection-triggering string

**For KNOWN GAP results, document:**
```
Gap ID: GAP-{{rule_id}}-{{NNN}}
Evasion: {{evasion_method}}
Detection Impact: Rule does not fire — attacker can use {{evasion_method}} to bypass detection
Required Enhancement: {{what rule modification or additional rule would catch this variant}}
Compensating Detection: {{existing rule that covers this gap, or "NONE"}}
Purple Team Action: Recommend Red Team verify evasion in live environment
```

Present all evasion test cases in sequence.

**Evasion Test Summary:**
```
Total evasion tests designed: {{count}}
Expected ALERT results: {{count}} (rule should catch despite evasion)
Expected KNOWN GAP results: {{count}} (evasion bypasses detection)
Evasion techniques from Step 2 covered: {{count}} of {{total_evasions}}
Gaps requiring compensating detection: {{count}}
```

### 6. Edge Case Test Cases

Design tests for boundary conditions that stress the rule's logic at its limits. Edge cases reveal parsing errors, type mismatches, and assumption failures that only surface in unusual but realistic scenarios.

**For each edge case test, present:**

```
┌──────────────────────┬─────────────────────────────────────────────────────┐
│ Test ID              │ EC-{{rule_id}}-{{NNN}}                             │
├──────────────────────┼─────────────────────────────────────────────────────┤
│ Test Name            │ {{descriptive_name}}                               │
│ Description          │ {{what boundary condition is being tested}}        │
│ Edge Case Category   │ {{case sensitivity / encoding / timing /           │
│                      │ field length / null values / type mismatch}}       │
│ Simulation Method    │ {{exact command or action that creates the         │
│                      │ boundary condition}}                               │
│ Expected Log Source  │ {{where the edge case event appears}}              │
│ Expected Log Fields  │ {{field values at the boundary}}                   │
│ Expected Result      │ {{ALERT / NO ALERT / UNDEFINED — document          │
│                      │ expected behavior and why}}                        │
│ Rule Logic Exercised │ {{specific condition in the rule being stressed}}  │
│ Platform             │ {{OS version / environment}}                       │
│ Prerequisites        │ {{any special config for boundary testing}}        │
│ Risk if Unexpected   │ {{impact if the rule behaves differently than      │
│                      │ expected at this boundary}}                        │
└──────────────────────┴─────────────────────────────────────────────────────┘
```

**Edge case categories to design tests for:**

- **Case sensitivity** — If the rule uses string matching: does `CMD.EXE` match `cmd.exe`? Does `PowerShell` match `powershell`? Test the rule's case handling against the SIEM's case behavior.
- **Encoding variants** — Base64-encoded payloads, URL-encoded characters, Unicode normalization variants. Test whether the rule handles encoded versions of its detection strings.
- **Timing edge cases** — For rules with timeframe-based aggregation or correlation: what happens at the exact boundary? Events arriving 1 second before and 1 second after the window. Midnight rollover. Timezone transitions.
- **Field length boundaries** — Extremely long command lines (>8192 characters), truncated log fields, maximum field lengths per the log source schema.
- **Null or empty fields** — What happens when a required field is null, empty string, or missing entirely? Does the rule fail open (no alert — potential miss) or fail closed (alert — potential FP)?
- **Type mismatches** — Numeric fields containing strings, string fields containing special characters, integer overflow in count-based rules.

Present all edge case test cases in sequence.

**Edge Case Test Summary:**
```
Total edge case tests designed: {{count}}
Categories covered: {{list of edge case categories tested}}
Expected ALERT: {{count}}
Expected NO ALERT: {{count}}
Expected UNDEFINED (behavior to document): {{count}}
```

### 7. Test Coverage Summary

Consolidate all test cases into a coverage summary and present to the operator:

```
╔══════════════════════════════════════════════════════════════════════╗
║              TEST COVERAGE SUMMARY — {{rule_id}}                   ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Rule: {{rule_title}}                                              ║
║  ATT&CK: {{T-code — technique_name}}                               ║
║  Format: {{sigma / yara / suricata}}                               ║
║                                                                    ║
╠════════════════╦═══════╦═════════════════════════════════════════════╣
║ Category       ║ Count ║ Pass Criteria                              ║
╠════════════════╬═══════╬═════════════════════════════════════════════╣
║ True Positive  ║ {{N}} ║ ALL must trigger alert                     ║
║ True Negative  ║ {{N}} ║ NONE must trigger alert                    ║
║ False Positive ║ {{N}} ║ NONE must trigger alert (filters work)     ║
║ Evasion        ║ {{N}} ║ Document detection/gap per case            ║
║ Edge Case      ║ {{N}} ║ Document behavior per case                 ║
╠════════════════╬═══════╬═════════════════════════════════════════════╣
║ TOTAL          ║ {{N}} ║                                            ║
╚════════════════╩═══════╩═════════════════════════════════════════════╝
```

**Coverage Analysis:**

```
Rule conditions tested by TP cases: {{count}} of {{total_conditions}}
Documented FP patterns tested: {{count}} of {{total_FP_patterns}}
Evasion techniques tested: {{count}} of {{total_evasions_from_step2}}
Edge case categories tested: {{count}} of 6 standard categories

Test Readiness: READY FOR VALIDATION / GAPS IDENTIFIED (see below)
```

**If gaps identified:**
```
Gap: {{category}} — {{specific gap description}}
Impact: {{what is at risk if this gap is not addressed}}
Recommendation: {{add specific test case / accept risk / defer to post-deployment monitoring}}
```

**Coverage Quality Assessment:**
- **Strong coverage**: ≥3 TP, ≥2 TN, all documented FPs covered, ≥2 evasion tests, ≥2 edge cases
- **Acceptable coverage**: ≥3 TP, ≥1 TN, most FPs covered, ≥1 evasion test, ≥1 edge case
- **Weak coverage**: Missing any TP category, no TN tests, FP patterns untested, no evasion tests
- **Current assessment**: {{Strong / Acceptable / Weak}} — {{justification}}

### 8. Append Test Cases to Report and Present Menu

"**Test case design complete.**

Rule: {{rule_id}} — {{rule_title}}
Total test cases: {{total_count}}
TP: {{tp_count}} | TN: {{tn_count}} | FP: {{fp_count}} | Evasion: {{ev_count}} | Edge: {{ec_count}}
Coverage: {{Strong / Acceptable / Weak}}
Known gaps: {{gap_count}} ({{ALERT results expected: N, KNOWN GAP results: N}})

**Select an option:**
[A] Advanced Elicitation — Challenge test coverage assumptions, identify blind spots in the test suite
[W] War Room — Red (would these tests catch my real-world evasion?) vs Blue (is this test suite production-ready?)
[C] Continue — Proceed to Validation and Tuning (Step 5 of 7)"

#### Menu Handling Logic:

- IF A: Deep-dive test coverage analysis — challenge whether TP tests cover all realistic attack variants, evaluate whether TN tests represent the most common legitimate patterns in the environment, stress-test evasion tests against real-world adversary tradecraft, assess whether edge case tests address the most likely failure modes for this rule type, identify any test categories with insufficient coverage. Process insights, ask user if they want to add or modify test cases, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: would these test cases catch my actual evasion techniques? Are there obfuscation methods, tool substitutions, or execution paths not covered by the evasion tests? What would I change about my tradecraft to evade ALL these tests? Blue Team perspective: does this test suite give us confidence to deploy the rule? Are the TN tests representative of real production traffic? Will the FP tests prevent analyst alert fatigue? Is the coverage assessment honest or optimistic? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `test_cases_total` with total test cases designed, then read fully and follow: ./step-05-validation.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, test_cases_total updated with total count, and Test Cases section appended to report with all five test categories documented], will you then read fully and follow: `./step-05-validation.md` to begin validation and tuning.

---

## 🚨 SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Test strategy defined with target counts per category derived from rule logic and Step 2 analysis
- At minimum 3 true positive test cases designed covering vanilla execution, parameter variation, and target context variation
- At minimum 2 true negative test cases designed representing realistic legitimate operations that resemble the attack
- At minimum 1 false positive test case per documented FP pattern in the rule's falsepositives section
- At minimum 1 evasion test case per evasion technique identified in Step 2 threat analysis
- At minimum 2 edge case test cases covering boundary conditions relevant to the rule type
- Every test case includes: unique ID, reproducible simulation method, expected result, prerequisites, and validation criteria
- Evasion test cases with KNOWN GAP results include gap documentation and compensating control assessment
- Test coverage summary presented with counts per category and quality assessment
- Coverage gaps (if any) documented with impact and recommendation
- Frontmatter updated with test_cases_total and step added to stepsCompleted
- Test Cases section appended to detection report
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Designing test cases without referencing the actual detection rule logic from Step 3
- Generic test descriptions without reproducible simulation methods (e.g., "simulate the attack" without specific commands)
- Skipping any of the five test categories (TP, TN, FP, evasion, edge case)
- True positive tests that do not exercise specific rule conditions
- No true negative tests — accepting unknown FP risk before deployment
- False positive tests that do not reference documented FP patterns from the rule
- Evasion tests without documenting whether the expected result is ALERT or KNOWN GAP
- KNOWN GAP results without compensating control assessment or gap documentation
- Executing test cases during this step — execution belongs to Step 5
- Modifying detection rule logic during test design — modifications belong to Step 5 tuning
- Not presenting test coverage summary with quality assessment
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Test case design transforms detection intent into verifiable expectations — every test must be reproducible, every category must be covered, and every known gap must be documented. A detection rule without comprehensive test cases is a hope deployed into production, not a control.
