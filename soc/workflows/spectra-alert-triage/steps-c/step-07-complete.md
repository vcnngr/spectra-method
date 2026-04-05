# Step 7: Documentation, Closure, and Purple Team Feedback

**Final Step — Workflow Complete**

## STEP GOAL:

Finalize the triage report with executive summary and quantified metrics, generate detection tuning recommendations, create Purple Team feedback items that bridge Blue to Red, update engagement status, and close the triage workflow. This is the terminal step — no further steps exist.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- ✅ THIS IS A FINAL STEP — Workflow completion required
- 📖 CRITICAL: Read the complete step file before taking any action
- 🛑 NO new triage or response operations — this is documentation and closure
- 📋 FINALIZE document, generate executive summary, update engagement status
- 💬 FOCUS on completion, validation, detection improvement, and Purple Team handoff
- 🎯 UPDATE engagement status with triage completion information
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Triage Analyst completing an authorized triage operation
- ✅ The triage report must be a complete, standalone document with full evidence chain and classification rationale
- ✅ Every triage feeds the detection improvement cycle — skipping Purple Team feedback means detection gaps remain unaddressed
- ✅ Detection tuning recommendations must be specific enough to be actionable — vague suggestions waste detection engineering time
- ✅ The executive summary should serve both SOC operators and non-technical stakeholders

### Step-Specific Rules:

- 🎯 Focus on report finalization, executive summary, detection tuning, Purple Team feedback, and engagement status update
- 🚫 FORBIDDEN to perform any new triage, enrichment, or response operations
- 🚫 FORBIDDEN to load additional workflow steps after this one
- 💬 Approach: Comprehensive documentation with quantified metrics and actionable improvement recommendations

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Closing a triage without documenting the classification rationale reduces the value for future analysts and detection tuning — the classification justification is the primary intellectual output of the triage; without it, the report is just raw data
  - Skipping the Purple Team feedback loop means detection gaps remain unaddressed — every triage, whether TP, FP, or BTP, produces intelligence that should feed the detection improvement cycle
  - Detection tuning recommendations without specific rule modifications are too vague to be actionable — include the rule name, current logic, proposed change, expected impact, and false negative risk
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show report completeness validation before any finalization action
- 💾 Update engagement status with triage completion information
- 📖 Offer closure options and next workflow navigation
- 🚫 DO NOT load additional steps after this one

## TERMINATION STEP PROTOCOLS:

- This is a FINAL step — workflow completion required
- Update engagement status with triage phase completion
- Suggest next operational workflows and validation options
- Mark workflow as complete in all tracking mechanisms

## CONTEXT BOUNDARIES:

- Available context: Complete triage report from all previous steps (1-6 or 1-5 for FP path), engagement.yaml, all enrichment and correlation data
- Focus: Report validation, executive summary, detection tuning, Purple Team feedback, and closure
- Limits: No new triage operations — documentation and handoff only
- Dependencies: All previous steps completed; classification finalized in step 5; response finalized in step 6 (if TP/BTP) or skipped (if FP)

## THREE COMPLETION PATHS:

This step handles three distinct paths based on the classification from step 5:

- **TP (True Positive) path**: Full report with response actions, detection gap analysis, and Purple Team feedback for Red Team testing
- **FP (False Positive) path**: Report focused on detection tuning and FP reduction — no response section, Purple Team feedback focuses on verification after tuning
- **BTP (Benign True Positive) path**: Report with authorization documentation, exception scoping, and detection refinement to reduce noise

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Validate Report Completeness

Before announcing completion, verify every section of the report is populated:

| Section | Step | Status | Expected Content |
|---------|------|--------|------------------|
| Alert Summary | Step 1 | ✅/❌ | Normalized alert, raw data, extracted IOCs |
| IOC Enrichment Results | Step 2 | ✅/❌ | Enrichment tables, threat assessment, statistics |
| Context Analysis | Step 3 | ✅/❌ | Asset/user context, historical alerts, mitigating factors |
| Correlation and Kill Chain | Step 4 | ✅/❌ | Related alerts, ATT&CK mapping, campaign assessment |
| Classification and Priority | Step 5 | ✅/❌ | Decision tree, classification, confidence, priority |
| Response and Escalation | Step 6 | ✅/❌ or N/A | Containment plan, escalation package (N/A if FP) |

**If any section shows incomplete:**

"The following sections are incomplete:
{{incomplete_sections_with_step_references}}

Would you like to return to the corresponding steps to complete them, or proceed with completion noting the missing sections?"

### 2. Generate Executive Summary

Populate the `## Executive Summary` section of the output document:

```markdown
## Executive Summary

### Alert Overview
Alert {{alert_id}} from {{alert_source}} triaged on {{date}} by {{user_name}}.

### Classification
- Result: {{classification}} ({{classification_confidence}} confidence)
- Priority: {{priority}}
- MITRE ATT&CK: {{mitre_techniques}}
- Decision path: Q1 ({{verdict}}) → Q2 ({{verdict}}) → Q3 ({{confidence}})

### Scope
- Affected hosts: {{count}} ({{list}})
- Affected users: {{count}} ({{list}})
- Correlated alerts: {{count}}
- Kill chain coverage: {{tactics_detected}}
- Campaign assessment: {{isolated / related / campaign}}

### Actions Taken
- Containment actions: {{count}} ({{summary}}) — or "N/A — False Positive, no response required"
- Escalation: {{target or "handled at L1" or "N/A — False Positive"}}
- Evidence preserved: {{summary or "N/A"}}

### Key Findings
1. {{finding_1 — most significant discovery}}
2. {{finding_2 — second most significant}}
3. {{finding_3 — third most significant}}

### Metrics
- Time to triage: {{duration from alert_timestamp to completion}}
- IOCs analyzed: {{iocs_enriched}} of {{iocs_extracted}} extracted
- Enrichment verdict: Malicious {{count}} / Suspicious {{count}} / Clean {{count}} / Unknown {{count}}
- Detection tuning items: {{count}}
- Purple Team items: {{count}}
```

### 3. Detection Tuning Recommendations

Populate the `## Detection Tuning Recommendations` section based on the classification path:

#### If FALSE POSITIVE — Focus on FP reduction:

"**Root Cause Analysis:**

What caused the false positive?
- Rule logic issue: {{too_broad_condition / missing_exclusion / threshold_too_low / field_parsing_error}}
- Data quality issue: {{log_format_change / field_normalization_error / timestamp_mismatch}}
- Context gap: {{legitimate_activity_not_allowlisted / authorized_tool_not_excluded}}

**Specific Rule Modification:**

```
Rule: {{rule_name}}
Source: {{detection_platform — Sigma / Splunk / Sentinel / CrowdStrike / custom}}
Current logic: {{description_of_current_detection_logic}}
Trigger condition: {{what_specifically_triggered_this_FP}}
Recommended change: {{add exclusion / adjust threshold / modify condition / add context filter}}
Proposed modification: {{specific_change — e.g., 'Add exclusion for process_name=authorized_tool.exe when parent_process=scheduler.exe'}}
Expected impact: Reduce FP rate by approximately {{estimate}} for this rule
False negative risk: {{assessment — does this change create a blind spot for real attacks?}}
Testing required: {{how_to_validate_the_tuning — replay malicious samples, verify detection still triggers}}
```

**FP Pattern Assessment:**
- Is this a recurring FP? {{yes_with_count / first_occurrence}}
- Broader rule family affected? {{other_rules_with_same_logic_flaw}}
- Recommended review scope: {{single_rule / rule_family / detection_category}}"

#### If TRUE POSITIVE — Focus on detection gaps:

"**Detection Effectiveness Assessment:**

What was detected:
- Rule that fired: {{rule_name}} — {{what_it_caught}}
- ATT&CK coverage: {{techniques_detected}} / {{total_techniques_in_kill_chain}}

What was NOT detected (gaps in kill chain coverage):
| Gap # | ATT&CK Technique | Tactic | Why Not Detected | Data Source Required |
|-------|-----------------|--------|------------------|---------------------|
| 1 | {{T-code — technique_name}} | {{tactic}} | {{missing_rule / missing_log_source / evasion}} | {{log_source}} |

**Recommended New Detection Rules:**

```
Gap: {{ATT&CK technique not detected — T-code and name}}
Rule concept: {{what the rule should detect — behavior, indicator, pattern}}
Suggested format: Sigma / YARA / platform-specific
Data source required: {{log_source — Sysmon EventID, Windows Security, network flow, etc.}}
Priority: {{critical / high / medium / low}}
Reference: {{existing Sigma rule ID or community detection reference if applicable}}
```

**Detection Improvement Roadmap:**
1. {{highest_priority_detection_gap}}
2. {{second_priority}}
3. {{third_priority}}"

#### If BENIGN TRUE POSITIVE — Focus on exception scoping:

"**Exception Recommendation:**

The detected activity is legitimate and authorized. To prevent recurring alerts:

```
Activity: {{description_of_authorized_activity}}
Authorization: {{pen_test_id / change_ticket / tool_authorization}}
Exception scope: {{NARROW — specific user + specific host + specific time window}}
  - User: {{specific_username or group}}
  - Host: {{specific_hostname or range}}
  - Time: {{specific_window or permanent with review date}}
  - Process: {{specific_process_name}}
Exception type: {{allowlist / suppress / threshold_adjust}}
Review date: {{when this exception should be re-evaluated}}
```

**Warning:** Exception must be scoped as narrowly as possible. Blanket exceptions create blind spots. Every exception should have a review date."

### 4. Purple Team Feedback

Populate the `## Purple Team Feedback` section. This is the critical bridge between Blue Team triage and Red Team operations:

```yaml
# Purple Team Feedback — Alert Triage
# Generated by: spectra-alert-triage workflow
# Date: {{date}}

engagement_id: {{engagement_id}}
alert_id: {{alert_id}}
analyst: {{user_name}}
classification: {{TP / FP / BTP}}
priority: {{priority}}
mitre_techniques: {{mitre_techniques}}
```

#### For TRUE POSITIVE — Red Team should test variations:

```yaml
# Detection that worked — what was caught
detected_technique: {{T-code — technique_name}}
detection_rule: {{rule_name}}
detection_data_source: {{what_log_source_triggered_the_detection}}
detection_latency: {{time_from_activity_to_alert}}

# Detection gaps — Red Team should exploit these
detection_gaps:
  - tactic: {{TA00XX — tactic_name}}
    technique: {{T-code — technique_name}}
    gap: {{what_was_not_detected_and_why}}
    red_team_test: "Test whether {{specific_variation_or_evasion}} evades current detection"
    priority: {{critical / high / medium / low}}

# Evasion testing — Red Team should verify detection robustness
evasion_tests:
  - detected_technique: {{T-code}}
    test: "Attempt {{technique_name}} using {{alternative_tool_or_method}} to test detection coverage"
    expected_result: "Detection should still trigger if rule logic is sound"

# Kill chain gaps for Red Team to exploit in future operations
uncovered_stages:
  - tactic: {{TA00XX — tactic_name}}
    assessment: "No detection coverage for this tactic — Red Team can operate freely here"
```

#### For FALSE POSITIVE — Red Team should verify tuning:

```yaml
# Tuning applied — verify it does not create blind spots
tuning_applied: {{specific_rule_change_from_section_3}}
tuning_risk: {{false_negative_risk_assessment}}

# Verification needed from Red Team
verification_tests:
  - test: "Confirm {{original_malicious_pattern}} still triggers detection after tuning"
    method: "Execute {{specific_attack_variation}} matching the original rule intent"
    expected_result: "Alert should fire for malicious variant despite FP tuning"

# Detection integrity check
original_rule_intent: {{what_the_rule_was_designed_to_catch}}
tuning_narrows_to: {{what_the_rule_now_catches_after_exclusion}}
potential_blind_spot: {{what_an_attacker_could_do_to_exploit_the_exclusion}}
```

#### For BENIGN TRUE POSITIVE — Red Team should test exception boundaries:

```yaml
# Exception created — verify it cannot be abused
exception_scope: {{exception_details_from_section_3}}

# Abuse testing needed from Red Team
abuse_tests:
  - test: "Attempt to perform malicious activity that matches the exception criteria"
    scenario: "If exception allows {{tool}} for {{user}}, test whether attacker using same {{tool}} from different context triggers detection"
    expected_result: "Exception should NOT cover attacker activity — only the specific authorized scenario"
```

### 5. Update Engagement Status

Update the engagement tracking with triage completion data:

```yaml
engagement_id: {{engagement_id}}
last_updated: {{date}}
triage_log:
  - alert_id: {{alert_id}}
    classification: {{TP / FP / BTP}}
    priority: {{P1 / P2 / P3 / P4 or N/A}}
    confidence: {{High / Medium / Low}}
    mitre_techniques: {{T-codes}}
    timestamp: {{date}}
    analyst: {{user_name}}
    escalation: {{target or "L1 handled" or "N/A — FP"}}
    containment_actions: {{count or 0}}
    detection_tuning_items: {{count}}
    purple_team_items: {{count}}
    time_to_triage: {{duration}}
```

### 6. Final Frontmatter Update and Completion Announcement

**Update the output document frontmatter:**

```yaml
stepsCompleted: [..., "step-07-complete.md"]
workflowStatus: complete
completionDate: {{date}}
detection_tuning_recommendations: {{count}}
purple_team_items: {{count}}
```

Update the document header `**Status:**` from `In Progress` to `Completed`.

**Announce workflow completion:**

"**Alert Triage Workflow Completed!**

{{user_name}}, the triage for alert **{{alert_id}}** is complete.

**Final report:** `{outputFile}`

**Classification:** {{classification}} ({{classification_confidence}} confidence)
**Priority:** {{priority or 'N/A'}}

**Deliverables Summary:**
- Complete triage report with {{section_count}} sections
- Evidence chain documented from intake through classification
- Executive summary with quantified metrics
- Detection tuning recommendations: {{count}} items
- Purple Team feedback items: {{count}} items
- Engagement status updated

**Triage Metrics:**
- Alert source: {{alert_source}}
- MITRE ATT&CK: {{mitre_techniques}}
- IOCs analyzed: {{iocs_enriched}} of {{iocs_extracted}}
- Containment actions: {{count or 'N/A'}}
- Escalation: {{escalation_target or 'N/A'}}
- Time to triage: {{duration}}

{{if TP: The alert has been classified as a True Positive and response actions are documented. Escalation package is ready for the receiving team.}}
{{if FP: The alert has been classified as a False Positive. Detection tuning recommendations are ready for implementation to reduce future false positive rate.}}
{{if BTP: The alert has been classified as a Benign True Positive. Exception documentation and scope are ready for implementation.}}

The triage report is ready to feed the detection improvement cycle and Purple Team operations."

### 7. Final Navigation Options

"**Available Options:**

[W] War Room — Red vs Blue debrief on the entire triage operation
[N] New Alert — Start a new triage workflow (fresh step-01-init.md)
[S] SOC Handoff — Package for L2/L3/IRT with full triage context
[D] Detection Engineering — Hand off tuning recommendations to Sentinel (`spectra-agent-detection-eng`)
[P] Purple Team — Hand off feedback to Red Team via `spectra-war-room`

What would you like to do?"

#### Menu Handling Logic:

- IF W: Full War Room session — comprehensive Red vs Blue debrief on the entire triage. Red Team perspective: was this alert something I would worry about as an attacker? How would I avoid this detection next time? What would I do differently in the time between activity and detection? What does this triage tell me about SOC maturity? Blue Team perspective: was our triage process efficient? Did we have the right data at the right time? Where were we slow? What data sources were missing? How would we handle this alert differently next time? Grade the organization's detection posture based on this triage. This is the capstone analytical discussion.
- IF N: Inform the user to start a fresh triage. Provide engagement_id for reference. Recommend invoking `spectra-alert-triage` to launch a new workflow from step-01-init.md. The completed triage report remains at the current outputFile path.
- IF S: Package the triage findings into a standalone escalation/handoff format suitable for L2, L3, or IRT consumption. Include: executive summary, classification with full justification, enrichment highlights, kill chain position, containment actions taken and pending, evidence locations, and recommended next investigation steps. Ready for direct ingestion by the receiving team.
- IF D: Package the detection tuning recommendations from section 3 into a format suitable for the detection engineering team or `spectra-agent-detection-eng`. Include: specific rule modifications (FP path), new rule recommendations (TP path), or exception configurations (BTP path). Each recommendation should be actionable without requiring the detection engineer to re-read the full triage report.
- IF P: Package the Purple Team feedback from section 4 into a format suitable for `spectra-war-room` or direct Red Team consumption. Include: detection gaps to exploit, evasion tests to run, tuning verification tests, and kill chain coverage analysis. This is the bridge that closes the Red-Blue feedback loop.
- IF user asks questions: Answer and redisplay menu

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Report completeness validated — all sections populated (or marked N/A with justification)
- Executive summary generated with quantified metrics for all three classification paths (TP, FP, BTP)
- Detection tuning recommendations are specific and actionable (rule name, current logic, proposed change, expected impact, false negative risk)
- Purple Team feedback includes specific detection gaps, evasion tests, and verification items
- Purple Team feedback correctly tailored to classification path (TP gaps, FP tuning verification, BTP exception abuse testing)
- Engagement status updated with triage completion data
- Final frontmatter updated with workflowStatus: complete, completionDate, detection_tuning_recommendations, and purple_team_items
- Document status changed from "In Progress" to "Completed"
- Clear navigation options provided for next actions (W/N/S/D/P)
- User understands deliverables, outcomes, and recommended next actions

### SYSTEM FAILURE:

- Not validating report completeness before announcing completion
- Generating executive summary without quantified metrics (IOC counts, timing, action counts)
- Detection tuning recommendations without specific rule modifications (vague "improve detection" is not actionable)
- Skipping Purple Team feedback — every triage must feed the improvement cycle regardless of classification
- Purple Team feedback that does not include specific tests for Red Team to execute
- Not updating engagement status with triage completion data
- Not providing clear next-action guidance via the navigation menu
- Loading additional workflow steps after this terminal step
- Performing any new triage or response operations during completion
- Closing without documenting the classification rationale
- Not distinguishing between TP, FP, and BTP paths in documentation and recommendations

**CRITICAL:** Reading only partial step file leads to incomplete understanding and poor decisions.
**CRITICAL:** Making decisions without complete understanding of step requirements and protocols.

## FINAL NOTE

The triage report documents the entire analytical chain: from alert intake through classification to response and closure. Every decision is justified, every IOC is enriched, every recommendation is specific. This report directly feeds the detection improvement cycle through Purple Team feedback and detection tuning recommendations. The quality of this documentation determines how much the organization learns from this alert.

**Alert triage for {{alert_id}} is complete. The detection improvement cycle continues.**
