# Step 8: Reporting & Closure

**Final Step — Workflow Complete**

## STEP GOAL:

Finalize the hunt report with executive summary and quantified metrics, assess hunt maturity, document lessons learned, generate future hunt recommendations, update engagement status, and close the threat hunt workflow. This is the terminal step — no further steps exist. The hunt report must be a complete, standalone document that communicates findings, detection improvements, and organizational risk posture changes to both technical and non-technical stakeholders.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- ✅ THIS IS A FINAL STEP — Workflow completion required
- 📖 CRITICAL: Read the complete step file before taking any action
- 🛑 NO new hunting, analysis, or detection engineering — this is documentation and closure
- 📋 FINALIZE document, generate executive summary, update engagement status
- 💬 FOCUS on completion, validation, metrics, maturity assessment, and handoff
- 🎯 UPDATE engagement status with hunt completion information
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Threat Hunter completing an authorized hunt operation and producing a comprehensive hunt report
- ✅ The hunt report must be a complete, standalone document — another analyst should understand what was hunted, what was found, and what was improved
- ✅ Metrics quantify hunt effectiveness — without metrics, the hunt program cannot mature
- ✅ Lessons learned feed the next hunt — skip this section and institutional knowledge is lost
- ✅ The executive summary must serve both the SOC team (technical detail) and leadership (business impact)

### Step-Specific Rules:

- 🎯 Focus on report finalization, executive summary, hunt metrics, maturity assessment, lessons learned, future hunt recommendations, and engagement status update
- 🚫 FORBIDDEN to perform any new hunting, analysis, or detection engineering operations
- 🚫 FORBIDDEN to load additional workflow steps after this one
- 💬 Approach: Comprehensive documentation with quantified metrics, actionable recommendations, and clear handoff guidance

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Closing a hunt without documenting lessons learned forfeits institutional knowledge that would improve future hunts — the lessons learned section is how the hunt program matures over time. Even "everything went smoothly" hunts have lessons: what worked well should be replicated, and process improvements should be captured.
  - Closing a hunt with confirmed malicious findings without verifying that incident response has been notified creates a gap between discovery and action — if active adversary presence was confirmed, verify that the incident response team has been engaged before marking this hunt as complete.
  - An executive summary without quantified metrics (finding counts, data volume, technique coverage, detection improvement delta) reduces the hunt's value to leadership and makes it harder to justify continued investment in the hunt program — always include specific numbers, not qualitative assessments.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show report completeness validation before any finalization action
- 💾 Update engagement status with hunt completion information
- 📖 Offer closure options and next workflow navigation
- 🚫 DO NOT load additional steps after this one

## TERMINATION STEP PROTOCOLS:

- This is a FINAL step — workflow completion required
- Update engagement status with hunt phase completion
- Suggest next operational workflows and validation options
- Mark workflow as complete in all tracking mechanisms

## CONTEXT BOUNDARIES:

- Available context: Complete hunt report from all previous steps (1-7), engagement.yaml, all findings, detection engineering output
- Focus: Report validation, executive summary, metrics, maturity, lessons learned, and closure
- Limits: No new hunting operations — documentation and handoff only
- Dependencies: All previous steps completed; findings validated in step 6; detection engineering complete in step 7

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Validate Report Completeness

Before announcing completion, verify every section of the report is populated:

"**Report Completeness Validation:**

| Section | Step | Status | Expected Content |
|---------|------|--------|------------------|
| Hunt Mission | Step 1 | ✅/❌ | Trigger classification, scope definition, intelligence, hunt ID |
| Hypothesis Development | Step 2 | ✅/❌ | ATT&CK mapping, hypotheses, data source requirements, success criteria |
| Data Sources & Collection | Step 3 | ✅/❌ | Source verification, query library, baselines, execution plan |
| Automated Analysis Results | Step 4 | ✅/❌ | Query execution results, pattern detection, automated triage, checkpoint data |
| Manual Analysis Results | Step 5 | ✅/❌ | Behavioral analysis, LOLBin/lateral/persistence/credential analysis, TTP matching |
| Validated Findings | Step 6 | ✅/❌ | Evidence chains, classifications, ATT&CK mapping, impact, hypothesis verdicts |
| Detection Engineering | Step 7 | ✅/❌ | Detection rules, hunt playbooks, gap analysis, surface reduction, Purple Team |

**If any section shows incomplete:**

"The following sections are incomplete:
{{incomplete_sections_with_step_references}}

Would you like to return to the corresponding steps to complete them, or proceed with closure noting the missing sections?""

### 2. Generate Executive Summary

Populate the `## Executive Summary` section of the output document:

"**Executive Summary:**

### Hunt Overview
Hunt {{hunt_id}} ("{{hunt_name}}") executed within engagement {{engagement_name}} on {{date}} by {{user_name}}.

### Mission
- **Trigger:** {{trigger_type}} — {{trigger_source}}
- **Hunt Classification:** {{Tactical / Strategic / Hybrid}}
- **Target Environment:** {{scope summary}}
- **Lookback Window:** {{historical period}} + {{live monitoring period}}
- **Hypotheses Tested:** {{count}}

### Key Findings

| # | Finding | Classification | Confidence | ATT&CK | Business Impact |
|---|---------|---------------|-----------|--------|----------------|
| 1 | {{finding 1 — most significant}} | {{classification}} | {{confidence}} | {{T-codes}} | {{impact}} |
| 2 | {{finding 2}} | {{classification}} | {{confidence}} | {{T-codes}} | {{impact}} |
| 3 | {{finding 3}} | {{classification}} | {{confidence}} | {{T-codes}} | {{impact}} |

{{If no findings (all hypotheses refuted):}}
**No malicious activity detected.** All hypotheses were systematically tested against {{data_source_count}} data sources over {{time_period}}. While no adversary presence was confirmed, this hunt produced {{rule_count}} detection rules, {{playbook_count}} hunt playbooks, and identified {{gap_count}} detection gaps for remediation. The absence of findings, combined with verified data source coverage, provides reasonable assurance that the targeted techniques were not active during the hunt window.

### Detection Improvement
- **Detection rules created:** {{count}} ({{types}})
- **Hunt playbooks created:** {{count}}
- **Detection gaps identified:** {{count}}
- **ATT&CK coverage delta:** {{before}}% → {{after}}% ({{techniques added}} techniques)
- **Attack surface reduction items:** {{count}}

### Threat Posture Assessment
{{1-3 sentences assessing the organization's security posture based on hunt findings:}}
{{If malicious: "Active adversary presence was confirmed with {{technique_count}} techniques observed across {{tactic_count}} tactics. Immediate incident response engagement is recommended. The adversary demonstrated {{sophistication_level}} sophistication, and {{count}} detection gaps were identified that could allow further undetected activity."}}
{{If suspicious but unconfirmed: "Suspicious activity was identified that warrants continued monitoring. While definitive malicious attribution was not possible, the observed behaviors are inconsistent with normal operations and should be treated as potential compromise indicators."}}
{{If clean: "No adversary activity was detected during this hunt. Detection coverage has been improved with {{rule_count}} new rules. {{gap_count}} detection gaps remain that should be addressed to improve future detection capability."}}"

### 3. Hunt Metrics

"**Hunt Metrics:**

| Metric | Value |
|--------|-------|
| **Hunt ID** | {{hunt_id}} |
| **Hunt Name** | {{hunt_name}} |
| **Hunt Type** | {{Tactical / Strategic / Hybrid}} |
| **Start Time** | {{hunt_start_time}} |
| **End Time** | {{hunt_end_time (now)}} |
| **Duration** | {{total duration}} |
| **Trigger Type** | {{trigger_type}} |

**Data Metrics:**

| Metric | Value |
|--------|-------|
| Data sources queried | {{count}} ({{list}}) |
| Data volume analyzed | {{volume — e.g., "47.3 GB across 12.4M events"}} |
| Queries executed | {{count}} |
| Query phases completed | {{count}} |

**Hypothesis Metrics:**

| Metric | Value |
|--------|-------|
| Hypotheses developed | {{count}} |
| Hypotheses tested | {{count}} |
| Hypotheses confirmed | {{count}} |
| Hypotheses refuted | {{count}} |
| Hypotheses inconclusive | {{count}} |
| Unexpected findings | {{count}} |

**Finding Metrics:**

| Metric | Value |
|--------|-------|
| Total findings | {{count}} |
| Confirmed malicious | {{count}} |
| Suspicious | {{count}} |
| Benign anomaly | {{count}} |
| False positive | {{count}} |
| ATT&CK techniques confirmed | {{count}} |
| ATT&CK tactics observed | {{count}} |
| Evidence chains constructed | {{count}} |

**Detection Engineering Metrics:**

| Metric | Value |
|--------|-------|
| Detection rules created | {{count}} |
| ├── Sigma rules | {{count}} |
| ├── YARA rules | {{count}} |
| ├── Suricata rules | {{count}} |
| └── Platform-native rules | {{count}} |
| Hunt playbooks created | {{count}} |
| Detection gaps identified | {{count}} |
| Attack surface reduction items | {{count}} |
| Purple Team items | {{count}} |
| ATT&CK coverage improvement | {{before}}% → {{after}}% |"

### 4. Hunt Maturity Assessment

"**Hunt Maturity Assessment (SQRRL Hunting Maturity Model):**

| Level | Description | This Hunt |
|-------|-------------|-----------|
| **HMM0 — Initial** | Relies primarily on automated alerting (SIEM, IDS). No regular data collection beyond alerts. No routine hunting. | {{Yes/No}} |
| **HMM1 — Minimal** | Incorporates threat intelligence indicator searches (IOC sweeps). Routine data collection from key sources. | {{Yes/No}} |
| **HMM2 — Procedural** | Follows defined hunt procedures and playbooks. Hunting is a regular activity. Some data analysis techniques applied. | {{Yes/No}} |
| **HMM3 — Innovative** | Creates new hunt procedures. Uses data analysis tools and techniques creatively. Threat modeling drives hunts. | {{Yes/No}} |
| **HMM4 — Leading** | Automates successful hunt procedures into continuous detection. Hunting drives detection engineering cycle. Original research produces new techniques. | {{Yes/No}} |

**This hunt operated at Level: {{0-4}}**

**Justification:** {{Why this level — reference specific aspects of the hunt that support the assessment}}

**Automation Potential:**

| Hunt Component | Automation Feasibility | Effort | Value |
|---------------|----------------------|--------|-------|
| {{component — e.g., "H1 IOC sweep queries"}} | {{High — ready for scheduled search / Medium — needs query tuning / Low — requires human judgment}} | {{effort estimate}} | {{time saved per execution}} |
| ... | ... | ... | ... |

**Repeatability Score:**

| Criterion | Score (1-5) | Notes |
|-----------|------------|-------|
| Query documentation | {{1-5}} | {{all queries documented with context}} |
| Baseline availability | {{1-5}} | {{baselines established for comparison}} |
| Playbook completeness | {{1-5}} | {{investigation guidance documented}} |
| Data source stability | {{1-5}} | {{data sources likely to remain available}} |
| Analyst skill requirement | {{1-5}} | {{1=expert only, 5=any L1 can execute}} |
| **Overall Repeatability** | **{{average}}/5** | {{summary}} |"

### 5. Lessons Learned

"**Lessons Learned:**

#### What Worked Well
| # | Lesson | Detail | Recommendation |
|---|--------|--------|---------------|
| 1 | {{what worked}} | {{specific detail}} | {{replicate in future hunts}} |
| 2 | ... | ... | ... |

#### What Could Be Improved
| # | Lesson | Detail | Recommendation |
|---|--------|--------|---------------|
| 1 | {{what could improve}} | {{specific detail}} | {{specific improvement action}} |
| 2 | ... | ... | ... |

#### Unexpected Discoveries
| # | Discovery | Impact | Action |
|---|-----------|--------|--------|
| 1 | {{unexpected finding or insight}} | {{how it affects operations}} | {{what to do about it}} |
| 2 | ... | ... | ... |

#### Process Improvements
| # | Current Process | Recommended Change | Expected Impact |
|---|----------------|-------------------|----------------|
| 1 | {{current approach}} | {{recommended change}} | {{expected improvement}} |
| 2 | ... | ... | ... |"

### 6. Future Hunt Recommendations

"**Future Hunt Recommendations:**

| # | Hunt Topic | Trigger | ATT&CK Focus | Priority | Rationale |
|---|-----------|---------|-------------|----------|-----------|
| 1 | {{recommended hunt — e.g., "Hunt for lateral movement via WMI in cloud-connected endpoints"}} | {{what triggers this hunt — gap discovered, technique not tested, new intelligence}} | {{T-codes}} | {{Critical/High/Medium/Low}} | {{why this hunt is needed — references this hunt's gaps or findings}} |
| 2 | {{recommended hunt}} | {{trigger}} | {{T-codes}} | {{priority}} | {{rationale}} |
| 3 | {{recommended hunt}} | {{trigger}} | {{T-codes}} | {{priority}} | {{rationale}} |
| ... | ... | ... | ... | ... | ... |

**Hunt Cadence Recommendation:**
- Hypotheses confirmed in this hunt: Re-hunt {{frequency}} to verify detection rules catch future variants
- Inconclusive hypotheses: Re-hunt when {{data source gap}} is resolved
- Refuted hypotheses: Re-hunt {{frequency}} with updated intelligence or after significant environment changes
- New hypotheses from unexpected findings: Prioritize for next hunt cycle"

### 7. Update Engagement Status

Update the engagement tracking with hunt completion data:

```yaml
engagement_id: {{engagement_id}}
last_updated: {{date}}
hunt_log:
  - hunt_id: {{hunt_id}}
    hunt_name: {{hunt_name}}
    hunt_type: {{Tactical / Strategic / Hybrid}}
    trigger_type: {{trigger_type}}
    timestamp: {{date}}
    hunter: {{user_name}}
    duration: {{total_duration}}
    hypotheses_tested: {{count}}
    hypotheses_confirmed: {{count}}
    hypotheses_refuted: {{count}}
    hypotheses_inconclusive: {{count}}
    findings_total: {{count}}
    findings_confirmed_malicious: {{count}}
    findings_suspicious: {{count}}
    detection_rules_created: {{count}}
    detection_gaps_identified: {{count}}
    hunt_playbooks_created: {{count}}
    purple_team_items: {{count}}
    attack_surface_reduction_items: {{count}}
    hunt_maturity_level: {{0-4}}
    data_sources_queried: {{count}}
    data_volume_analyzed: {{volume}}
    queries_executed: {{count}}
```

### 8. Final Frontmatter Update and Completion Announcement

**Update the output document frontmatter:**

```yaml
stepsCompleted: [..., "step-08-reporting.md"]
workflowStatus: complete
completionDate: {{date}}
hunt_end_time: {{date}}
hunt_duration: {{duration}}
hunt_maturity_level: {{0-4}}
```

Update the document header `**Status:**` from `In Progress` to `Completed`.

Populate the `## Lessons Learned & Future Hunts` section with content from sections 5 and 6 above.

**Announce workflow completion:**

"**Threat Hunt Workflow Completed!**

{{user_name}}, the threat hunt **{{hunt_id}}** ("{{hunt_name}}") is complete.

**Final report:** `{outputFile}`

**Hunt Summary:**
- **Trigger:** {{trigger_type}} — {{trigger_source}}
- **Classification:** {{Tactical / Strategic / Hybrid}}
- **Duration:** {{total_duration}}
- **Scope:** {{brief scope summary}}

**Findings:**
- Hypotheses tested: {{count}} — Confirmed: {{confirmed}} | Refuted: {{refuted}} | Inconclusive: {{inconclusive}}
- Total findings: {{count}} — Confirmed Malicious: {{count}} | Suspicious: {{count}} | Benign: {{count}} | FP: {{count}}
- ATT&CK techniques confirmed: {{count}} across {{count}} tactics

**Detection Improvements:**
- Detection rules created: {{count}} (Sigma: {{count}}, YARA: {{count}}, Suricata: {{count}}, Native: {{count}})
- Hunt playbooks created: {{count}}
- Detection gaps identified: {{count}}
- Attack surface reduction items: {{count}}
- ATT&CK coverage: {{before}}% → {{after}}% (+{{delta}} techniques)
- Purple Team items: {{count}}

**Hunt Maturity Level:** {{level}} ({{level_name}})
**Repeatability Score:** {{score}}/5

{{If confirmed malicious: "**IMPORTANT:** Confirmed malicious activity was detected. Ensure incident response has been notified and containment actions are in progress. Consider launching spectra-incident-handling for full incident lifecycle management."}}
{{If suspicious: "Suspicious activity warrants continued monitoring. Consider enhanced detection rules and periodic re-hunting to resolve ambiguity."}}
{{If clean: "No adversary activity detected — detection posture has been strengthened with new rules and playbooks. The hunt reduced uncertainty about the targeted techniques in this environment."}}

The hunt report is ready to feed the detection improvement cycle and Purple Team operations."

### 9. Final Navigation Options

"**Available Options:**

[W] War Room — Red vs Blue debrief on the entire hunt operation
[N] New Hunt — Start a new threat hunt workflow (fresh step-01-init.md)
[S] SOC Handoff — Package hunt findings for SOC team with monitoring guidance
[D] Detection Engineering — Hand off rules and gap analysis to Sentinel (`spectra-agent-detection-eng`)
[P] Purple Team — Hand off feedback to Red Team via `spectra-war-room`
[T] Triage Handoff — If confirmed malicious finding needs immediate triage response (`spectra-alert-triage`)

What would you like to do?"

#### Menu Handling Logic:

- IF W: Full War Room session — comprehensive Red vs Blue debrief on the entire hunt operation. Red Team perspective: was this hunt something I would fear as an adversary? Which findings show strong detection capability? Where are the remaining blind spots I would exploit? What does this hunt tell me about the organization's detection maturity? If I were planning the next operation, how would I adjust my tradecraft based on these new detection rules? Blue Team perspective: was our hunt process efficient? Did we have the right data at the right time? Where were we slow? What data sources were missing? How would we execute this hunt differently next time? What's the realistic detection improvement from this hunt? Are our new rules operationally maintainable? Grade the organization's hunting posture. This is the capstone analytical discussion.
- IF N: Inform the user to start a fresh hunt. Provide engagement_id for reference. Recommend invoking `spectra-threat-hunt` to launch a new workflow from step-01-init.md. The completed hunt report remains at the current outputFile path.
- IF S: Package the hunt findings into a standalone SOC handoff format — monitoring guidance for confirmed/suspicious findings, new detection rules to deploy, baseline data for the SOC to maintain, and key indicators to watch for. Include enough context for SOC L1/L2 to understand what was found and what to monitor without requiring the full hunt report.
- IF D: Package the detection engineering output from step 7 into a format suitable for `spectra-agent-detection-eng` or the detection engineering team. Include: all detection rules (Sigma/YARA/Suricata/native), test cases, gap analysis, and recommended deployment priority. Each deliverable should be actionable without requiring the detection engineer to re-read the full hunt report.
- IF P: Package the Purple Team feedback from step 7 into a format suitable for `spectra-war-room` or direct Red Team consumption. Include: detection tests to run, evasion variants to test, gaps to exploit, hunt findings that inform attack planning, and blind spots to leverage. This is the bridge that closes the Red-Blue feedback loop.
- IF T: If confirmed malicious findings require immediate triage response, package the relevant findings with evidence chains, affected systems/users, ATT&CK mapping, and recommended containment actions into a format suitable for `spectra-alert-triage` or `spectra-incident-handling`. Flag the urgency level based on adversary activity state (active vs historical).
- IF user asks questions: Answer and redisplay menu

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Report completeness validated — all sections populated (or marked N/A with justification)
- Executive summary generated with quantified metrics, key findings table, detection improvement summary, and threat posture assessment
- Executive summary tailored for both technical and non-technical audiences
- Hunt metrics comprehensive: timing, data, hypotheses, findings, detection engineering, maturity
- Hunt maturity assessment performed using SQRRL model with justification
- Automation potential and repeatability score assessed for future hunt optimization
- Lessons learned documented with what worked, improvements needed, unexpected discoveries, and process changes
- Future hunt recommendations provided with trigger conditions, ATT&CK focus, and rationale
- Engagement status updated with hunt completion data
- Final frontmatter updated with workflowStatus: complete, completionDate, hunt_end_time, hunt_duration, hunt_maturity_level
- Document status changed from "In Progress" to "Completed"
- Lessons Learned & Future Hunts section populated in output document
- Clear navigation options provided for next actions (W/N/S/D/P/T)
- User understands deliverables, outcomes, and recommended next actions

### SYSTEM FAILURE:

- Not validating report completeness before announcing completion
- Generating executive summary without quantified metrics (qualitative-only summaries undervalue the hunt)
- Not assessing hunt maturity level (prevents program improvement tracking)
- Skipping lessons learned (institutional knowledge lost)
- Not providing future hunt recommendations (hunt program stagnates)
- Closing with confirmed malicious findings without verifying incident response notification
- Not updating engagement status with hunt completion data
- Not providing clear next-action guidance via the navigation menu
- Loading additional workflow steps after this terminal step
- Performing any new hunting or analysis during completion
- Not distinguishing between confirmed malicious, suspicious, benign, and FP in summary
- Not calculating detection improvement delta (ATT&CK coverage before vs after)

**CRITICAL:** Reading only partial step file leads to incomplete understanding and poor decisions.
**CRITICAL:** Making decisions without complete understanding of step requirements and protocols.

## FINAL NOTE

The hunt report documents the complete analytical journey: from trigger intelligence through hypothesis development, data collection, systematic analysis, finding validation, and detection engineering. Every decision is justified, every finding is classified with evidence chains, every detection improvement is tested and documented. This report directly feeds the detection improvement cycle through new rules, playbooks, gap analysis, and Purple Team feedback. The quality of this documentation determines how much the organization learns from this hunt — and how much stronger its defenses become.

**Hunt {{hunt_id}} is complete. The detection improvement cycle continues. Happy hunting.**
