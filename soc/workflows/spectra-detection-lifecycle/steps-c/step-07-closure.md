# Step 7: Coverage Assessment, Purple Team Feedback, and Closure

**Final Step — Workflow Complete**

## STEP GOAL:

Measure the detection coverage improvement, generate Purple Team feedback for Red Team and SOC operations, produce executive summary, and close the detection lifecycle with full traceability from threat finding to deployed rule.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- ✅ THIS IS A FINAL STEP — Workflow completion required
- 📖 CRITICAL: Read the complete step file before taking any action
- 🛑 NO new detection engineering operations — this is assessment, feedback, and closure
- 📋 FINALIZE document, generate coverage assessment, produce Purple Team feedback, update engagement status
- 💬 FOCUS on completion, coverage measurement, detection improvement feedback, and Purple Team handoff
- 🎯 UPDATE engagement status with detection lifecycle completion information
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Detection Engineer completing a structured detection lifecycle within an active security engagement
- ✅ The detection report must be a complete, standalone document tracing every decision from threat finding to deployed rule
- ✅ Every detection lifecycle feeds the Purple Team loop — skipping feedback means detection gaps remain invisible to Red Team and SOC operations
- ✅ Coverage assessment must be honest — inflating coverage percentages creates a false sense of security that adversaries will exploit
- ✅ The executive summary should serve both detection engineering teams and security leadership

### Step-Specific Rules:

- 🎯 Focus on report validation, coverage assessment, Purple Team feedback generation, executive summary, and engagement status update
- 🚫 FORBIDDEN to perform any new rule authoring, testing, validation, or deployment planning
- 🚫 FORBIDDEN to load additional workflow steps after this one
- 💬 Approach: Comprehensive closure with quantified coverage metrics, structured Purple Team feedback, and actionable next-step recommendations

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Closing the lifecycle with rules not yet deployed (validation passed but deployment still pending) — warn about coverage gap persistence; the rule exists in theory but provides zero operational protection until deployed; recommend tracking a deployment ticket with a deadline to ensure the rule reaches production
  - Purple Team feedback has no evasion tests — warn about unvalidated detection confidence; without Red Team verification of evasion gaps, the detection confidence is based on Blue Team self-assessment only; recommend at minimum 2 evasion verification requests for Red Team to validate the rule in realistic adversary conditions
  - Coverage assessment shows a critical tactic with 0% detection coverage — warn about strategic blind spot; the adversary can operate freely in this tactic without any detection; recommend immediate prioritization for the next detection lifecycle and consider whether interim monitoring (manual hunt queries) can provide temporary visibility
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show report completeness validation before any finalization action
- 💾 Update engagement status with detection lifecycle completion information
- 📖 Offer closure options and next workflow navigation
- 🚫 DO NOT load additional steps after this one

## TERMINATION STEP PROTOCOLS:

- This is a FINAL step — workflow completion required
- Update engagement status with detection lifecycle phase completion
- Suggest next operational workflows and validation options
- Mark workflow as complete in all tracking mechanisms

## CONTEXT BOUNDARIES:

- Available context: Complete detection report from all previous steps (1-6), engagement.yaml, all rule artifacts, test results, validation data, and deployment plan
- Focus: Report validation, coverage assessment, Purple Team feedback, executive summary, and closure
- Limits: No new detection engineering operations — assessment, feedback, and handoff only
- Dependencies: All previous steps completed; rule validated in Step 5; deployment planned in Step 6

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Validate Report Completeness

Before announcing completion, verify every section of the detection report is populated or explicitly marked N/A with justification:

```
REPORT COMPLETENESS VALIDATION
═══════════════════════════════

| Section | Step | Status | Expected Content |
|---------|------|--------|------------------|
| Detection Requirement | Step 1 | ✅/❌ | Normalized requirement, source classification, data source feasibility, rule ID |
| Threat Analysis | Step 2 | ✅/❌ | ATT&CK deep mapping, evasion techniques, detection surface analysis |
| Detection Rules | Step 3 | ✅/❌ | Rule(s) in Sigma/YARA/Suricata, metadata, false positive documentation |
| Test Cases | Step 4 | ✅/❌ | TP, TN, FP, evasion, edge case test cases with IDs and simulation methods |
| Validation Results | Step 5 | ✅/❌ | TP results, FP assessment, tuning log, evasion results, quality gate |
| Deployment Plan | Step 6 | ✅/❌ | Platform, alert config, monitoring baseline, schedule, rollback plan |
| Coverage Assessment | Step 7 | ⏳ | This section — populated below |
| Purple Team Feedback | Step 7 | ⏳ | This section — populated below |
```

**If any section shows incomplete:**

"The following sections are incomplete:
{{incomplete_sections_with_step_references}}

Would you like to return to the corresponding steps to complete them, or proceed with closure noting the missing sections?"

**If all sections complete:**
"**Report completeness validated.** All sections from Steps 1-6 populated. Proceeding to coverage assessment."

### 2. ATT&CK Coverage Assessment

Map the detection coverage improvement achieved by this lifecycle. Coverage must be honest — only count rules that are validated and deployed (or ready for deployment).

**Before this rule:**

```
ATT&CK COVERAGE — BEFORE
═════════════════════════

| Tactic | Techniques Covered | Total Techniques | Coverage % |
|--------|-------------------|-----------------|------------|
| {{TA0001}} Initial Access | {{N}} | {{total}} | {{%}} |
| {{TA0002}} Execution | {{N}} | {{total}} | {{%}} |
| {{TA0003}} Persistence | {{N}} | {{total}} | {{%}} |
| {{TA0004}} Privilege Escalation | {{N}} | {{total}} | {{%}} |
| {{TA0005}} Defense Evasion | {{N}} | {{total}} | {{%}} |
| {{TA0006}} Credential Access | {{N}} | {{total}} | {{%}} |
| {{TA0007}} Discovery | {{N}} | {{total}} | {{%}} |
| {{TA0008}} Lateral Movement | {{N}} | {{total}} | {{%}} |
| {{TA0009}} Collection | {{N}} | {{total}} | {{%}} |
| {{TA0011}} Command and Control | {{N}} | {{total}} | {{%}} |
| {{TA0010}} Exfiltration | {{N}} | {{total}} | {{%}} |
| {{TA0040}} Impact | {{N}} | {{total}} | {{%}} |
```

**After this rule:**

Same table structure with updated coverage numbers reflecting the new detection rule(s).

**Coverage Delta:**

```
COVERAGE DELTA
══════════════

Techniques newly covered by this lifecycle:
- {{T-code}} — {{technique_name}} (Tactic: {{tactic_name}})
- {{additional techniques if multi-rule lifecycle}}

Coverage improvement: +{{N}} technique(s), +{{delta}}% overall coverage

Remaining gaps in {{primary_tactic}}:
- {{T-code}} — {{technique_name}} — {{gap_reason: no data source / no rule / evasion-only coverage}}
- {{additional gaps}}

Priority gaps for next lifecycle (top 3):
1. {{T-code}} — {{technique_name}} — {{rationale for priority: frequency, impact, adversary usage}}
2. {{T-code}} — {{technique_name}} — {{rationale}}
3. {{T-code}} — {{technique_name}} — {{rationale}}
```

**ATT&CK Heatmap (text-based visualization):**

```
ATT&CK COVERAGE HEATMAP
════════════════════════

Legend: [███] = Covered | [▒▒▒] = Partial (evasion gaps) | [   ] = No coverage | [NEW] = This lifecycle

Reconnaissance    [   ][   ][   ][   ][   ]
Resource Dev      [   ][   ][   ][   ][   ]
Initial Access    [███][   ][NEW][   ][   ]
Execution         [███][▒▒▒][   ][   ][   ]
Persistence       [   ][   ][   ][   ][   ]
Priv Escalation   [███][   ][   ][   ][   ]
Defense Evasion   [   ][   ][   ][   ][   ]
Credential Access [   ][   ][   ][   ][   ]
Discovery         [███][   ][   ][   ][   ]
Lateral Movement  [   ][   ][   ][   ][   ]
Collection        [   ][   ][   ][   ][   ]
C2                [███][   ][   ][   ][   ]
Exfiltration      [   ][   ][   ][   ][   ]
Impact            [   ][   ][   ][   ][   ]
```

(Populate based on actual engagement coverage data — show which techniques have rules per tactic.)

### 3. Detection Coverage Score

Calculate engagement-level detection metrics for this lifecycle:

```
DETECTION COVERAGE SCORE
═════════════════════════
```

```
┌──────────────────────────────────────┬────────────┐
│ Metric                               │ Value      │
├──────────────────────────────────────┼────────────┤
│ Total ATT&CK techniques in scope     │ {{N}}      │
│ Techniques with detection rules      │ {{N}}      │
│ Techniques with validated rules      │ {{N}}      │
│ Techniques with deployed rules       │ {{N}}      │
│ Detection coverage % (authored)      │ {{%}}      │
│ Detection coverage % (validated)     │ {{%}}      │
│ Detection coverage % (deployed)      │ {{%}}      │
│ Rules authored this lifecycle        │ {{N}}      │
│ Rule formats used                    │ {{formats}}│
│ Test cases created                   │ {{N}}      │
│ Test cases passing                   │ {{N}}      │
│ Test cases failing                   │ {{N}}      │
│ FP rate (validated)                  │ {{%}}      │
│ Tuning iterations performed          │ {{N}}      │
│ Known evasion gaps                   │ {{N}}      │
│ Quality gate verdict                 │ {{verdict}}│
└──────────────────────────────────────┴────────────┘
```

**Coverage Quality Breakdown:**
- **Authored** coverage: Rules exist but may not be validated — this is detection INTENT
- **Validated** coverage: Rules passed quality gates — this is detection CAPABILITY
- **Deployed** coverage: Rules are live in production — this is detection REALITY
- **Gap between authored and deployed**: {{delta}} — represents rules in the pipeline that are not yet operational

### 4. Purple Team Feedback

Generate structured feedback for Red Team and SOC operations. This is the critical bridge that closes the Red-Blue feedback loop.

**For Red Team (attack verification):**

```yaml
purple_team_feedback:
  engagement_id: {{engagement_id}}
  rule_id: {{rule_id}}
  feedback_type: detection-deployed
  analyst: {{user_name}}
  date: {{date}}
  
  detection_deployed:
    technique: {{T-code — technique_name}}
    tactic: {{TA-code — tactic_name}}
    rule_name: {{rule_title}}
    rule_format: {{sigma / yara / suricata}}
    target_platform: {{deployment_target}}
    detection_point: {{pre-execution / execution / post-execution / lateral / network}}
    detection_confidence: {{high / medium / low — based on quality gate and evasion results}}
    fp_rate: {{percentage}}
    
  known_evasion_gaps:
    - evasion_technique: {{name}}
      evasion_description: {{how the attacker could bypass this detection}}
      detection_status: evaded — not detected by this rule
      compensating_detection: {{other rule ID or "NONE — gap exists"}}
      red_team_test: "Verify evasion works: {{specific test instruction for Red Team}}"
    - evasion_technique: {{name}}
      evasion_description: {{description}}
      detection_status: evaded
      compensating_detection: {{control or "NONE"}}
      red_team_test: "{{instruction}}"
    
  verification_requests:
    - test: "Attempt {{T-code}} with {{variation}} — verify detection fires within {{expected_latency}}"
      priority: {{critical / high / medium}}
    - test: "Attempt {{evasion_method}} — verify evasion status matches documented gap"
      priority: {{critical / high / medium}}
    - test: "Attempt {{related_technique}} — verify correlation rule fires if applicable"
      priority: {{medium / low}}
    
  coverage_after: {{percentage}}
  next_priority_gaps:
    - technique: {{T-code — technique_name}}
      tactic: {{tactic_name}}
      gap_reason: {{no data source / no rule authored / evasion-only coverage}}
      priority: {{critical / high / medium}}
    - technique: {{T-code — technique_name}}
      tactic: {{tactic_name}}
      gap_reason: {{reason}}
      priority: {{priority}}
```

**For SOC Operations (analyst guidance):**

```yaml
soc_operations_feedback:
  engagement_id: {{engagement_id}}
  date: {{date}}
  
  new_rules_deployed:
    - rule_name: {{name}}
      rule_id: {{id}}
      alert_name: {{alert_name_in_SIEM}}
      severity: {{level}}
      routing: {{L1 / L2 / L3}}
      known_fp_patterns:
        - "{{fp_pattern_1 — what it looks like and why it is benign}}"
        - "{{fp_pattern_2}}"
      triage_guidance: "{{what the analyst should check first when this alert fires — specific fields, context lookups, and decision criteria}}"
      escalation_criteria: "{{when to escalate — specific conditions that warrant L2/L3 involvement}}"
      runbook: {{link to runbook or "pending creation — outline in deployment plan"}}
      expected_volume: "{{expected daily alert count based on validation baseline}}"
      rollback_contact: "{{who to contact if alert is misbehaving — detection engineering team/lead}}"
```

### 5. Generate Executive Summary

Create a concise summary for the report header that serves both detection engineering teams and security leadership:

```
╔══════════════════════════════════════════════════════════════════════╗
║              DETECTION ENGINEERING SUMMARY                         ║
╠══════════════════════════════════════════════════════════════════════╣

Input: {{source_type — Red Team finding / alert triage recommendation /
       threat hunt / threat intelligence}} — {{source_reference}}

Technique: {{T-code — technique_name}} ({{tactic_name}})

Rules authored: {{N}} ({{formats — e.g., "1 Sigma, 1 YARA"}})

Test cases: {{total}} ({{passed}} passed, {{failed}} failed)
  TP: {{count}} | TN: {{count}} | FP: {{count}} |
  Evasion: {{count}} | Edge: {{count}}

Validation: {{PASSED / CONDITIONAL / FAILED}}
  FP rate: {{percentage}}%
  Tuning iterations: {{N}}

Deployment:
  Target: {{platform}} — {{deployment_mode}}
  Schedule: {{date or condition}}
  Rollback: Defined ({{trigger_count}} triggers)

Coverage impact: {{before}}% → {{after}}% (+{{delta}}%)
  Techniques newly covered: {{count}}
  Known evasion gaps: {{count}}

Purple Team items: {{N}} verification requests
  Red Team: {{red_team_item_count}} tests
  SOC Ops: {{soc_item_count}} guidance items

Time to complete: {{from intake to closure — duration}}

╚══════════════════════════════════════════════════════════════════════╝
```

### 6. Update Final Frontmatter

Update all frontmatter fields to reflect lifecycle completion:

```yaml
stepsCompleted: [..., "step-07-closure.md"]
workflowStatus: complete
completionDate: {{date}}
coverage_before: {{percentage}}
coverage_after: {{percentage}}
coverage_delta: +{{percentage}}
techniques_covered: [{{T-codes}}]
known_evasion_gaps: {{count}}
purple_team_items: {{count}}
soc_operations_items: {{count}}
```

Update the document header `**Status:**` from `In Progress` to `Completed`.

### 7. Recommend Next Actions

Based on the lifecycle results, recommend specific next actions:

**Recommend next actions to the operator:**

```
RECOMMENDED NEXT ACTIONS
═════════════════════════

1. Chronicle Documentation
   Recommend: spectra-agent-chronicle to write formal documentation for the detection rule
   Input: Detection report from this lifecycle
   Purpose: Formal detection catalog entry with operational documentation

2. Next Detection Priority
   Recommended rule: {{T-code — technique_name}}
   Rationale: {{why this is the next priority — from coverage gap analysis}}
   Source: Coverage assessment gap #1
   Action: Start new spectra-detection-lifecycle workflow

3. Red Team Verification
   Hand off: Purple Team feedback package to Red Team
   Items: {{count}} verification requests, {{count}} evasion tests
   Purpose: Validate detection effectiveness with adversary simulation
   Action: Package via spectra-war-room or direct Red Team handoff

4. SOC Training (if applicable)
   Required: {{yes / no — based on alert complexity and routing tier}}
   Scope: {{analyst briefing on new alert type, known FP patterns, triage guidance}}
   Audience: {{L1 / L2 / L3 — per routing from deployment plan}}

5. Tuning Backlog (if applicable)
   Rules requiring follow-up: {{count — rules with CONDITIONAL quality gate}}
   Items: {{specific tuning tasks deferred from Step 5}}
   Timeline: {{review date from deployment monitoring baseline}}
```

### 8. Present Navigation Menu

"**Detection Lifecycle Complete.** Select next action:"

"[W] War Room — Red vs Blue debrief on detection effectiveness and adversary response"
"[N] New Rule — Start new detection-lifecycle for next priority gap"
"[H] Handoff Red Team — Package Purple Team feedback for Red Team verification"
"[S] SOC Briefing — Package analyst guidance for SOC operations"
"[D] Document — Hand off to Chronicle for formal documentation"

#### Menu Handling Logic:

- IF W: Full War Room session — comprehensive Red vs Blue debrief on the entire detection lifecycle. Red Team perspective: does this new detection change my operational playbook? How would I adapt my tradecraft to evade this rule? Would I target the known evasion gaps immediately, or would I first probe the rule's boundaries to discover unknown gaps? Does the deployment configuration (throttling, routing) give me operational windows? How does the FP rate affect my ability to hide in the noise? Blue Team perspective: are we genuinely more secure after this lifecycle, or have we just created a checkbox? Is the coverage improvement meaningful against the actual threat we face? Are the evasion gaps acceptable or do they undermine the detection? Would this rule have caught the original Red Team finding that triggered this lifecycle? Grade the detection posture improvement. This is the capstone analytical discussion.
- IF N: Inform the user to start a fresh detection lifecycle. Provide engagement_id for reference. Recommend invoking `spectra-detection-lifecycle` to launch a new workflow from step-01-init.md with the next priority gap from the coverage assessment as input. The completed detection report remains at the current outputFile path.
- IF H: Package the Purple Team feedback from section 4 into a format suitable for Red Team consumption or `spectra-war-room`. Include: detection deployed details, known evasion gaps with specific test instructions, verification requests with priority, and coverage gaps for future exploitation testing. Each item should be actionable without requiring the Red Team to read the full detection report.
- IF S: Package the SOC operations feedback from section 4 into a standalone briefing suitable for analyst consumption. Include: new alert name and ID, severity and routing, known FP patterns with examples, triage guidance, escalation criteria, expected volume, and rollback contact. Ready for SOC team meeting or email distribution.
- IF D: Recommend invoking `spectra-agent-chronicle` for formal documentation. Provide the detection report path and key artifacts (rule file, test cases, validation results) as input for the documentation workflow.
- IF user asks questions: Answer and redisplay menu

### 9. Update Engagement Status

Append to engagement detection log:

```yaml
detection_lifecycle_log:
  - rule_id: {{rule_id}}
    technique: {{T-code — technique_name}}
    tactic: {{tactic_name}}
    status: {{deployed / conditional / blocked}}
    deployment_target: {{platform}}
    deployment_mode: {{alerting / detection-only / shadow}}
    fp_rate: {{percentage}}%
    quality_gate: {{READY / CONDITIONAL}}
    test_cases: {{total_count}} ({{passed}} passed)
    tuning_iterations: {{count}}
    known_evasion_gaps: {{count}}
    coverage_delta: +{{delta}}%
    completion_date: {{date}}
    analyst: {{user_name}}
    purple_team_items: {{count}}
    soc_operations_items: {{count}}
    next_priority: {{T-code — technique_name}}
    report_path: {{outputFile}}
```

---

## 🚨 SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Report completeness validated — all sections from Steps 1-6 populated or explicitly marked N/A with justification
- ATT&CK coverage assessment completed with before/after comparison showing coverage delta
- Coverage delta is honest — only counting validated and deployed/deployable rules
- Priority gaps identified for next lifecycle with rationale for prioritization
- ATT&CK heatmap visualization presented showing coverage distribution across tactics
- Detection coverage score calculated with authored/validated/deployed breakdown
- Purple Team feedback generated with specific evasion gaps, verification requests, and test instructions for Red Team
- SOC operations feedback generated with alert details, FP patterns, triage guidance, and escalation criteria
- Executive summary generated with quantified metrics covering the entire lifecycle
- Final frontmatter updated with workflowStatus: complete, completionDate, coverage metrics, and Purple Team item counts
- Document status changed from "In Progress" to "Completed"
- Next action recommendations provided (Chronicle, next rule, Red Team handoff, SOC training, tuning backlog)
- Engagement status updated with detection lifecycle completion data
- Navigation menu presented with correct options (W/N/H/S/D) and handling logic
- User understands deliverables, outcomes, and recommended next steps

### ❌ SYSTEM FAILURE:

- Not validating report completeness before announcing closure
- Coverage assessment that inflates numbers — counting unvalidated or undeployed rules as "covered"
- Coverage delta without before/after comparison — cannot measure improvement without a baseline
- ATT&CK heatmap that does not reflect actual coverage data
- Purple Team feedback without specific evasion tests — generic "test the detection" is not actionable
- Purple Team feedback without verification requests — Red Team cannot validate detection without specific test instructions
- SOC operations feedback without FP patterns or triage guidance — analysts will be unprepared for the new alert
- Executive summary without quantified metrics (test counts, FP rate, coverage percentages, timing)
- Not updating engagement status with lifecycle completion data
- Loading additional workflow steps after this terminal step
- Performing any new rule authoring, testing, validation, or deployment during closure
- Not providing clear next-action guidance via the navigation menu
- Closing without documenting all known evasion gaps — undisclosed gaps are undisclosed risks
- Not distinguishing between authored, validated, and deployed coverage percentages

**CRITICAL:** Reading only partial step file leads to incomplete understanding and poor decisions.
**CRITICAL:** Making decisions without complete understanding of step requirements and protocols.

## FINAL NOTE

The detection lifecycle report documents the complete engineering chain: from threat finding intake through rule authoring, test design, validation, deployment planning, and coverage assessment. Every decision is justified, every test is documented, every gap is disclosed. This report directly feeds the Purple Team loop through Red Team evasion verification and SOC operations guidance. The quality of this documentation determines how much the organization's detection posture actually improves from each lifecycle iteration.

**Detection lifecycle for {{rule_id}} is complete. The Purple Team feedback loop continues.**
