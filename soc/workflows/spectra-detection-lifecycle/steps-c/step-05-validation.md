# Step 5: Validation and Tuning

**Progress: Step 5 of 7** — Next: Deployment Planning

## STEP GOAL:

Execute test cases against the detection rule, measure true/false positive rates, tune detection logic and thresholds iteratively until the rule meets quality gates for production deployment.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER declare a rule validated without executing the full test suite from Step 4 — partial validation is worse than no validation because it creates false confidence
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DETECTION ENGINEER, not an automated test runner — you facilitate structured validation with operator oversight and professional judgment on tuning decisions
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Detection Engineer collaborating with an expert peer on rule validation within an active security engagement
- ✅ Validation is where detection theory meets operational reality — test results are facts, not opinions
- ✅ A rule that passes all TP tests but generates 30% FP rate in production is not a detection — it is noise
- ✅ Tuning is a controlled, iterative process: identify the FP pattern, propose the filter, assess the FN risk, apply the modification, re-validate. Never tune blindly.
- ✅ Evasion test results define the rule's honest detection boundary — known gaps are acceptable when documented, unknown gaps are unacceptable

### Step-Specific Rules:

- 🎯 Focus exclusively on test execution, result recording, FP rate assessment, iterative tuning, evasion validation, and quality gate assessment
- 🚫 FORBIDDEN to skip failed test investigation — every FAIL requires root cause analysis
- 🚫 FORBIDDEN to tune without assessing false negative risk — every exclusion is a potential blind spot
- 💬 Approach: Systematic test execution with documented results, data-driven tuning decisions, and honest quality gate assessment
- 📊 Every tuning iteration must be logged: what changed, why, FP impact before and after, FN risk assessment
- 🔒 Maximum 5 tuning iterations — if FP rate still exceeds target after 5 rounds, flag for operational review rather than over-tuning into detection blindness

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Deploying a rule with FP rate above the target threshold — warn about analyst fatigue and trust erosion; a high-FP rule trains analysts to ignore alerts, which means the next real attack matching this rule pattern will be dismissed as noise; recommend additional tuning iteration or lowered severity as a compromise
  - Evasion tests show the rule can be bypassed with known techniques — warn about detection gap; if the adversary's known tradecraft evades the rule, the rule provides coverage against script kiddies but not the actual threat actor; recommend layered detection or a compensating rule targeting the evasion variant
  - Validation performed on limited dataset (< 24 hours of production logs) — warn about sampling bias; FP rate measured on a small sample may not reflect production reality; seasonal patterns, batch jobs, and periodic maintenance tasks may only appear at specific intervals; recommend extending the evaluation period or documenting the sampling limitation
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present test execution plan before beginning any validation
- ⚠️ Present [A]/[W]/[C] menu after quality gate assessment is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `validation_status`, `false_positive_rate`, and `tuning_iterations`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Detection requirement from Step 1, threat analysis from Step 2, detection rule(s) from Step 3, complete test suite from Step 4 (TP, TN, FP, evasion, edge case tests)
- Focus: Test execution, result documentation, FP rate measurement, iterative tuning, evasion validation, and quality gate assessment
- Limits: Do not redesign the test suite (Step 4) or begin deployment planning (Step 6) — only execute tests, record results, and tune
- Dependencies: Complete test suite from step-04-test-cases.md with test IDs, simulation methods, and expected results

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Test Execution Plan

Before executing any tests, define the execution method and environment. The operator must confirm the execution approach.

**Present the execution plan:**

```
Test Execution Plan — {{rule_id}}
═══════════════════════════════════

Test Suite: {{total_test_count}} tests from Step 4
Rule Format: {{sigma / yara / suricata}}

Execution Method:
┌─────────────────────┬──────────────────────────────────────────────────────┐
│ Method              │ Description                                        │
├─────────────────────┼──────────────────────────────────────────────────────┤
│ Lab replay          │ Replay test events against rule in isolated env     │
│ Historical search   │ Run rule against historical log data (retrohunt)    │
│ Atomic Red Team     │ Use atomic tests for technique simulation           │
│ Manual simulation   │ Manually generate test events in test environment   │
│ Purple Team exercise│ Coordinate with Red Team for live simulation        │
└─────────────────────┴──────────────────────────────────────────────────────┘

Selected method: {{method}}
Justification: {{why this method is appropriate for this rule and environment}}

Environment:
- Platform: {{test environment — lab / staging / production shadow}}
- SIEM/EDR: {{target platform where rule is loaded}}
- Log sources available: {{confirmed log sources}}
- Historical data window: {{if retrohunt — time range available}}

Execution Order:
1. True Positive tests (TP) — validate detection fires
2. False Positive assessment — measure FP rate on baseline data
3. Tuning iterations (if FP rate exceeds target)
4. Evasion tests — validate detection boundaries
5. Quality gate assessment — final go/no-go determination
```

"**Execution plan ready.** Proceeding to true positive test execution."

### 2. Execute True Positive Tests

Execute each TP test case from Step 4 and record the result. For each test:

**Present TP execution results:**

```
TRUE POSITIVE TEST EXECUTION — {{rule_id}}
════════════════════════════════════════════

| Test ID | Test Name | Simulation | Rule Fired? | Latency | Alert Fields Correct? | Result |
|---------|-----------|------------|-------------|---------|----------------------|--------|
| TP-{{rule_id}}-001 | {{name}} | {{executed/simulated}} | Yes/No | {{seconds}} | Yes/Partial/No | PASS/FAIL |
| TP-{{rule_id}}-002 | {{name}} | {{executed/simulated}} | Yes/No | {{seconds}} | Yes/Partial/No | PASS/FAIL |
| TP-{{rule_id}}-003 | {{name}} | {{executed/simulated}} | Yes/No | {{seconds}} | Yes/Partial/No | PASS/FAIL |
```

**TP Results Summary:**
```
Tests executed: {{count}}
PASS: {{count}}
FAIL: {{count}}
Pass rate: {{percentage}}
```

**For each FAIL result, perform root cause analysis:**

```
FAIL — TP-{{rule_id}}-{{NNN}}
─────────────────────────────
Symptom: {{rule did not fire / fired with wrong severity / alert fields incomplete}}
Root Cause: {{logic error / missing field mapping / wrong log source / threshold issue / field name mismatch}}
Rule Condition Affected: {{specific condition that failed}}
Fix Required: {{specific modification to rule logic — document for tuning}}
Fix Complexity: {{trivial / moderate / requires redesign}}
```

**If ANY TP test fails:**
"**WARNING: {{count}} true positive test(s) failed.** The rule does not reliably detect the intended technique. Root cause analysis above identifies the fix. This will be addressed in the tuning phase (section 4) before proceeding to FP assessment."

**If ALL TP tests pass:**
"**All {{count}} true positive tests passed.** Rule reliably detects the intended technique across tested variants. Proceeding to false positive assessment."

### 3. Execute False Positive Assessment

Run the detection rule against baseline production data to measure the false positive rate. This is the critical operational fitness test.

**Present FP assessment:**

```
FALSE POSITIVE ASSESSMENT — {{rule_id}}
════════════════════════════════════════

Data Source: {{production logs / historical data / synthetic baseline}}
```

```
┌──────────────────────────┬───────────────────────────────────────────────┐
│ Metric                   │ Value                                        │
├──────────────────────────┼───────────────────────────────────────────────┤
│ Evaluation period        │ {{start_date}} to {{end_date}} ({{duration}})│
│ Total events scanned     │ {{count}}                                    │
│ Total alerts generated   │ {{count}}                                    │
│ True positives           │ {{count}}                                    │
│ False positives          │ {{count}}                                    │
│ FP rate                  │ {{FP / (TP + FP) × 100}}%                   │
│ FP rate target           │ <5% (high-sev) / <10% (medium) / <20% (low) │
│ Rule severity            │ {{critical / high / medium / low}}           │
│ Applicable target        │ <{{target}}%                                 │
│ Status                   │ PASS / NEEDS TUNING                          │
└──────────────────────────┴───────────────────────────────────────────────┘
```

**If PASS (FP rate within target):**
"**FP rate {{percentage}}% is within the {{target}}% target for {{severity}}-severity rules.** No tuning required. Proceeding to evasion tests."

**If NEEDS TUNING (FP rate exceeds target):**
"**FP rate {{percentage}}% exceeds the {{target}}% target.** Entering tuning cycle. Maximum 5 iterations before escalation to operational review."

**FP Pattern Analysis:**
For each identified false positive, categorize the source:
```
| FP # | Alert Timestamp | Host | User | FP Pattern | Category |
|------|-----------------|------|------|------------|----------|
| 1 | {{timestamp}} | {{host}} | {{user}} | {{description}} | {{legitimate_tool / scheduled_task / admin_activity / noise}} |
```

Also execute the TN and FP test cases from Step 4:
```
TN/FP TEST EXECUTION:

| Test ID | Test Name | Rule Fired? | Expected | Result |
|---------|-----------|-------------|----------|--------|
| TN-{{rule_id}}-001 | {{name}} | Yes/No | NO ALERT | PASS/FAIL |
| FP-{{rule_id}}-001 | {{name}} | Yes/No | NO ALERT | PASS/FAIL |
```

### 4. Tuning Iterations (IF NEEDED)

**This section is executed ONLY if FP rate exceeds the target or TP tests failed.**

Each tuning cycle follows a strict 6-step process. Uncontrolled tuning degrades detection integrity.

**Tuning Cycle Process:**

```
Tuning Iteration {{N}} of 5
═══════════════════════════

Step 1 — Identify FP Pattern:
  Pattern: {{specific condition causing false alerts}}
  Frequency: {{how often this pattern appears in baseline data}}
  Source: {{what legitimate activity generates this pattern}}

Step 2 — Propose Filter/Exclusion:
  Modification: {{specific change to rule logic}}
  Type: {{add exclusion / adjust threshold / add context filter / modify condition}}
  Implementation: {{exact rule syntax change}}

Step 3 — Assess False Negative Risk:
  Question: Will this filter cause the rule to miss real attacks?
  Analysis: {{specific attack scenarios that might match the exclusion}}
  FN risk: {{none / low / medium / high}}
  Justification: {{why this risk level is acceptable or requires mitigation}}

Step 4 — Apply Modification:
  {{Updated rule section showing the change}}

Step 5 — Re-run FP Assessment:
  Previous FP rate: {{percentage}}%
  New FP rate: {{percentage}}%
  Delta: {{reduction}}%

Step 6 — Record Iteration:
  Decision: {{accept tuning / continue to next iteration / revert change}}
```

**Present Tuning Log:**

```
TUNING LOG — {{rule_id}}
═══════════════════════

| Iteration | FP Pattern | Modification | FP Before | FP After | FN Risk | Decision |
|-----------|------------|-------------|-----------|----------|---------|----------|
| 1 | {{pattern}} | {{change}} | {{%}} | {{%}} | {{risk}} | Accept/Continue/Revert |
| 2 | {{pattern}} | {{change}} | {{%}} | {{%}} | {{risk}} | Accept/Continue/Revert |
```

**After each iteration:**
- If FP rate now within target: "**FP rate reduced to {{percentage}}%.** Target met. Exiting tuning cycle."
- If FP rate still exceeds target: "**FP rate {{percentage}}% still exceeds target.** Proceeding to iteration {{N+1}}."

**After 5 iterations if FP rate still exceeds target:**

```
⚠️ OPERATIONAL REVIEW REQUIRED
═══════════════════════════════

FP rate after 5 tuning iterations: {{percentage}}%
Target: <{{target}}%
Gap: {{delta}}%

Remaining FP sources:
1. {{source_1 — why it cannot be filtered without FN risk}}
2. {{source_2}}

Recommendations:
- Deploy with adjusted severity (lower severity = higher FP tolerance)
- Deploy with suppression window (throttle alerts per host/user)
- Deploy in detection-only mode (log but do not alert)
- Return to Step 3 to redesign detection approach
- Accept current FP rate with analyst guidance documentation

Operator: select deployment approach or recommend redesign.
```

### 5. Execute Evasion Tests

Execute each evasion test case from Step 4 and record whether the rule detects the evaded technique.

**Present evasion test results:**

```
EVASION TEST EXECUTION — {{rule_id}}
═════════════════════════════════════

| Test ID | Evasion Method | Simulation | Rule Fired? | Expected | Result |
|---------|---------------|------------|-------------|----------|--------|
| EV-{{rule_id}}-001 | {{method}} | {{executed}} | Yes/No | ALERT/GAP | DETECTED/EVADED |
| EV-{{rule_id}}-002 | {{method}} | {{executed}} | Yes/No | ALERT/GAP | DETECTED/EVADED |
```

**Evasion Results Summary:**
```
Tests executed: {{count}}
DETECTED (rule caught evasion): {{count}}
EVADED (rule missed — expected gap): {{count}}
EVADED (rule missed — unexpected): {{count}}
```

**For each EVADED result (expected or unexpected):**

```
EVASION GAP — EV-{{rule_id}}-{{NNN}}
─────────────────────────────────────
Evasion method: {{method}}
Expected result: {{ALERT or KNOWN GAP}}
Actual result: EVADED — rule did not fire
Gap status: {{EXPECTED (documented in Step 4) / UNEXPECTED (new finding)}}
Compensating detection: {{existing rule / "NONE — gap exists"}}
Recommended action: {{create supplementary rule / accept risk / add to Purple Team feedback}}
```

**If unexpected evasions found:**
"**WARNING: {{count}} unexpected evasion(s) discovered.** The rule has detection gaps beyond those identified in Step 4. These are documented as findings for the quality gate assessment and Purple Team feedback."

**If all results match expectations:**
"**Evasion tests complete.** All results match expected outcomes from Step 4 test design. Known gaps documented. Proceeding to quality gate assessment."

Also execute edge case tests from Step 4:
```
EDGE CASE TEST EXECUTION:

| Test ID | Edge Case | Rule Fired? | Expected | Result | Behavior Notes |
|---------|-----------|-------------|----------|--------|----------------|
| EC-{{rule_id}}-001 | {{case}} | Yes/No | {{expected}} | PASS/FAIL/DOCUMENTED | {{notes}} |
```

### 6. Quality Gate Assessment

Consolidate all validation results into a final quality gate assessment. This determines whether the rule is ready for production deployment.

**Present quality gate assessment:**

```
╔══════════════════════════════════════════════════════════════════════╗
║              QUALITY GATE ASSESSMENT — {{rule_id}}                 ║
╠══════════════════════════════════════════════════════════════════════╣

| Gate | Criterion | Status | Notes |
|------|-----------|--------|-------|
| TP Coverage | All TP tests pass | ✅/❌ | {{count}} of {{total}} passed |
| FP Rate | Below threshold for {{severity}} level | ✅/❌ | Actual: {{rate}}%, Target: <{{target}}% |
| TN Coverage | All TN tests pass (no false alerts) | ✅/❌ | {{count}} of {{total}} passed |
| Evasion Awareness | Known gaps documented | ✅/❌ | {{detected}}/{{evaded}}/{{unexpected}} |
| Edge Cases | Boundary behavior documented | ✅/❌ | {{count}} tested |
| Rule Syntax | Valid {{format}} syntax | ✅/❌ | {{validation_method}} |
| Metadata Complete | All required fields populated | ✅/❌ | {{missing_fields or "all present"}} |
| Tuning Stable | FP rate stable after tuning | ✅/❌/N/A | {{iterations}} iterations |

╠══════════════════════════════════════════════════════════════════════╣
║ OVERALL VERDICT: READY / NOT READY / CONDITIONAL                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

**Verdict Definitions:**

- **READY** — All gates pass. Rule is approved for production deployment per Step 6 deployment plan.
- **NOT READY** — One or more critical gates fail (TP coverage or rule syntax). Rule requires rework before deployment. Return to Step 3 for rule modification, then re-execute Steps 4-5.
- **CONDITIONAL** — Non-critical gates have documented exceptions (acceptable FP rate variance, known evasion gaps with compensating controls, edge case behavior documented). Rule may deploy with conditions specified below.

**If NOT READY:**
```
Blockers:
1. {{gate}} — {{specific failure and required fix}}
2. {{gate}} — {{specific failure and required fix}}

Recommended path: Return to Step {{N}} for {{remediation action}}
```

**If CONDITIONAL:**
```
Conditions for deployment:
1. {{condition — e.g., "Deploy with 7-day monitoring period before full alerting"}}
2. {{condition — e.g., "Compensating rule RULE-XXX must be active before deployment"}}
3. {{condition — e.g., "Analyst briefing required — known FP pattern documented in runbook"}}

Accepted risks:
1. {{risk — e.g., "Evasion via command obfuscation not detected — compensating rule covers"}}
```

### 7. Append Validation Results to Report and Present Menu

"**Validation and tuning complete.**

Rule: {{rule_id}} — {{rule_title}}
TP tests: {{passed}}/{{total}} passed
FP rate: {{percentage}}% (target: <{{target}}%)
Tuning iterations: {{count}} ({{accepted/reverted}})
Evasion: {{detected}}/{{total}} detected, {{gaps}} known gaps
Quality gate: {{READY / NOT READY / CONDITIONAL}}

**Select an option:**
[A] Advanced Elicitation — Challenge validation methodology and quality gate assessment
[W] War Room — Red (can I evade this detection in production?) vs Blue (is this rule operationally ready?)
[C] Continue — Proceed to Deployment Planning (Step 6 of 7)"

#### Menu Handling Logic:

- IF A: Deep-dive validation analysis — challenge whether the test execution method is representative of production conditions, evaluate whether the FP assessment period is sufficient, stress-test tuning decisions for hidden FN risk, assess whether evasion test results accurately reflect the rule's detection boundary, evaluate whether CONDITIONAL verdicts are too permissive. Process insights, ask user if they want to re-run any tests or revise the quality gate, if yes iterate through relevant sections and redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: given these validation results, how confident am I that this rule would catch me in a real engagement? Which evasion gaps would I exploit first? Is the FP rate high enough that analysts will tune me out? Would I target the edge case boundaries to operate in the undefined behavior zone? Blue Team perspective: is the validation rigorous enough to justify production deployment? Are we accepting too many CONDITIONAL risks? Is the tuning stable or will FP rate creep back up as the environment evolves? Should we extend the monitoring period before full alerting? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `validation_status` to "READY/NOT READY/CONDITIONAL", `fp_rate` to actual percentage, and `tuning_iterations` to count, then read fully and follow: ./step-06-deployment.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, validation_status, fp_rate, and tuning_iterations updated, and Validation Results section appended to report with TP results, FP assessment, tuning log, evasion results, and quality gate assessment], will you then read fully and follow: `./step-06-deployment.md` to begin deployment planning.

---

## 🚨 SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Test execution plan defined with method, environment, and justification before any tests run
- All true positive test cases executed with pass/fail result and latency recorded
- Failed TP tests include root cause analysis with specific rule condition identified
- FP assessment conducted on baseline data with evaluation period, alert counts, and FP rate calculated
- FP rate compared against severity-appropriate target (<5% high, <10% medium, <20% low)
- TN and FP test cases from Step 4 executed with results recorded
- Tuning iterations (if needed) follow the 6-step process with FN risk assessment per iteration
- Tuning log maintained with before/after FP rates and decision per iteration
- Maximum 5 tuning iterations enforced — escalation to operational review if still exceeding target
- All evasion test cases executed with DETECTED/EVADED result recorded
- Unexpected evasions documented as new findings beyond Step 4 analysis
- Edge case tests executed with behavior documented
- Quality gate assessment completed across all gates with READY/NOT READY/CONDITIONAL verdict
- NOT READY verdicts include specific blockers and remediation path
- CONDITIONAL verdicts include explicit conditions and accepted risks
- Frontmatter updated with validation_status, fp_rate, and tuning_iterations
- Validation Results section appended to detection report
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Declaring validation passed without executing the complete test suite
- Skipping root cause analysis on failed TP tests — every failure reveals a rule defect
- Not measuring FP rate against baseline production data — lab-only validation misses real-world noise
- Tuning without assessing false negative risk — blind exclusions create detection blind spots
- Exceeding 5 tuning iterations without escalating to operational review
- Not documenting evasion test results — undocumented gaps are undisclosed risks
- Quality gate assessment that ignores failed gates — every gate must be evaluated and documented
- CONDITIONAL verdict without explicit conditions and accepted risks
- NOT READY verdict without blockers and remediation path
- Proceeding to deployment with NOT READY quality gate without operator override
- Beginning deployment planning during validation — deployment belongs to Step 6
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Validation is the proving ground between detection design and production reality — every test must be executed, every result must be documented, every tuning decision must assess false negative risk, and the quality gate verdict must be honest. Deploying an unvalidated rule into production is reckless; deploying a rule with undisclosed validation failures is negligent.
