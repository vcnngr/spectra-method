# Step 8: Reporting & Closure

**Final Step — Workflow Complete**

## STEP GOAL:

Finalize the phishing analysis report with executive summary and quantified metrics, validate report completeness across all 8 sections, generate lessons learned, update engagement status with incident completion data, and close the phishing response workflow — producing a complete, standalone phishing investigation report that serves as both an operational record and input to the detection improvement cycle.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- ✅ THIS IS A FINAL STEP — Workflow completion required
- 📖 CRITICAL: Read the complete step file before taking any action
- 🛑 NO new investigation or response operations — this is documentation and closure
- 📋 FINALIZE document, generate executive summary, update engagement status
- 💬 FOCUS on completion, validation, metrics, lessons learned, and handoff
- 🎯 UPDATE engagement status with phishing incident completion information
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst completing an authorized phishing investigation
- ✅ The phishing report must be a complete, standalone document with full evidence chain, blast radius assessment, and containment record
- ✅ Every phishing investigation feeds the detection improvement cycle — skipping lessons learned or Purple Team feedback means defense gaps remain unaddressed
- ✅ The executive summary should serve both SOC operators and non-technical stakeholders
- ✅ Metrics quantify the incident — they are the foundation for trending, benchmarking, and improvement

### Step-Specific Rules:

- 🎯 Focus on report finalization, executive summary, lessons learned, metrics, and engagement status update
- 🚫 FORBIDDEN to perform any new investigation, enrichment, or response operations
- 🚫 FORBIDDEN to load additional workflow steps after this one
- 💬 Approach: Comprehensive documentation with quantified metrics and actionable improvement recommendations

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Closing a phishing investigation without documenting the blast radius and user interaction funnel metrics reduces the report's value for future trending — the ratio of received:clicked:compromised is the most important metric for measuring phishing resilience over time; without it, the organization cannot track whether awareness training and detection improvements are actually reducing click rates
  - Skipping the lessons learned section means organizational learning from this incident is lost — every phishing investigation should answer: what worked, what failed, what would we do differently, and what systemic improvements are needed; these findings feed directly into security program improvement
  - Closing without verifying that containment actions are complete (or explicitly documenting exceptions) may leave the organization partially exposed — verify the containment action matrix from Step 6 before marking the investigation as complete
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show report completeness validation before any finalization action
- 💾 Update engagement status with phishing incident completion information
- 📖 Offer closure options and next workflow navigation
- 🚫 DO NOT load additional steps after this one

## TERMINATION STEP PROTOCOLS:

- This is a FINAL step — workflow completion required
- Update engagement status with phishing investigation completion
- Suggest next operational workflows and validation options
- Mark workflow as complete in all tracking mechanisms

## CONTEXT BOUNDARIES:

- Available context: Complete phishing investigation report from all previous steps (1-7), engagement.yaml, all enrichment, scope, containment, and detection data
- Focus: Report validation, executive summary, lessons learned, metrics, and closure
- Limits: No new investigation operations — documentation and handoff only
- Dependencies: All previous steps completed; containment actions recommended (step 6); detection improvements created (step 7)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Validate Report Completeness

Before announcing completion, verify every section of the report is populated:

**Report Completeness Validation:**

| Section | Step | Status | Expected Content |
|---------|------|--------|------------------|
| Email Summary | Step 1 | ✅/❌ | Extracted metadata, quick triage indicators, raw email preserved |
| Header Analysis | Step 2 | ✅/❌ | Received chain, SPF/DKIM/DMARC, infrastructure mapping, anomalies |
| Content & Payload Analysis | Step 3 | ✅/❌ | Body analysis, social engineering, URLs, attachments, payload classification |
| IOC Enrichment Results | Step 4 | ✅/❌ | Enrichment tables, ATT&CK mapping, campaign assessment |
| Scope & Impact Assessment | Step 5 | ✅/❌ | User interaction funnel, blast radius, business impact, regulatory assessment |
| Containment & Eradication | Step 6 | ✅/❌ | Containment action matrix, email/account/endpoint/infra actions |
| Detection & Prevention | Step 7 | ✅/❌ | Detection rules, gateway rules, user communications, Purple Team feedback |

**If any section shows incomplete:**

"The following sections are incomplete:
{{incomplete_sections_with_step_references}}

Would you like to return to the corresponding steps to complete them, or proceed with completion noting the missing sections?"

### 2. Containment Status Verification

Before closing, verify the containment status from Step 6:

**Containment Action Matrix — Final Status:**

| Category | Total Actions | Complete | Pending | Deferred |
|----------|--------------|---------|---------|----------|
| Email | {{count}} | {{count}} | {{count}} | {{count}} |
| Account | {{count}} | {{count}} | {{count}} | {{count}} |
| Endpoint | {{count}} | {{count}} | {{count}} | {{count}} |
| Infrastructure | {{count}} | {{count}} | {{count}} | {{count}} |
| **Total** | {{total}} | {{complete}} | {{pending}} | {{deferred}} |

**If actions are still pending:**

"⚠️ **Containment Not Fully Complete**

{{pending_count}} containment actions are still pending:
{{list of pending actions}}

Options:
1. Update the containment status before closing (recommended)
2. Close with pending actions documented as outstanding items
3. Return to Step 6 to update the containment plan"

### 3. Generate Executive Summary

Populate the `## Executive Summary` section of the output document:

```markdown
## Executive Summary

### Phishing Incident Overview
Phishing incident {{incident_id}} investigated on {{date}} by {{user_name}} within engagement {{engagement_name}} ({{engagement_id}}).

### Email Details
- **Subject:** {{email_subject}}
- **Sender:** {{email_sender}} ({{sender_infrastructure_type — legitimate/spoofed/compromised}})
- **Delivery Date:** {{delivery_timestamp}} UTC
- **Authentication:** SPF: {{spf_result}} | DKIM: {{dkim_result}} | DMARC: {{dmarc_result}}
- **Header Verdict:** {{header_verdict — FORGED/SPOOFED/COMPROMISED/SUSPICIOUS/LEGITIMATE INFRASTRUCTURE}}

### Payload & Attack Mechanism
- **Payload Type:** {{payload_type}} — {{1-sentence description of attack mechanism}}
- **URLs Found:** {{urls_found}} (Malicious: {{count}}, Suspicious: {{count}})
- **Attachments Found:** {{attachments_found}} (Malicious: {{count}})
- **Social Engineering:** {{primary technique}} ({{secondary techniques}})
- **Brand Impersonation:** {{brand or 'None detected'}}

### Blast Radius
- **Total recipients:** {{users_received}}
- **Opened/previewed:** {{users_opened}}
- **Clicked URL/opened attachment:** {{users_clicked}}
- **Submitted credentials:** {{users_submitted_creds}}
- **Confirmed account compromise:** {{accounts_compromised}}
- **Confirmed endpoint compromise:** {{endpoints_compromised}}
- **Click rate:** {{users_clicked / users_received * 100}}%
- **Compromise rate:** {{(users_submitted_creds + endpoints_compromised) / users_received * 100}}%

### MITRE ATT&CK
- **Techniques:** {{mitre_techniques}}
- **Kill Chain Coverage:** {{tactics covered}}
- **Campaign Assessment:** {{campaign type — known/unknown/novel}}

### Classification & Severity
- **Classification:** {{classification}}
- **Severity:** {{severity}}
- **Campaign Type:** {{targeted/semi-targeted/mass}}

### Response Summary
- **Containment actions:** {{containment_actions}} (Complete: {{complete}}, Pending: {{pending}})
- **Emails purged:** {{count}} from {{mailbox_count}} mailboxes
- **Accounts secured:** {{count}} (password reset + session revocation + MFA reset)
- **Endpoints contained:** {{count}} (isolated + cleaned)
- **Infrastructure blocked:** {{count}} IPs, {{count}} domains

### Detection Improvements
- **Detection rules created:** {{detection_rules_created}} (Sigma: {{count}}, YARA: {{count}}, Suricata: {{count}})
- **Email gateway rules:** {{count}}
- **Purple Team items:** {{purple_team_items}}

### Key Findings
1. {{finding_1 — most significant discovery from the investigation}}
2. {{finding_2 — second most significant}}
3. {{finding_3 — third most significant}}

### Regulatory Impact
- {{regulatory_notification_required or 'No regulatory notification required'}}
- {{if required: deadline, responsible party, current status}}
```

### 4. Metrics

Calculate and document key phishing response metrics:

**Phishing Response Metrics:**

| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| **Time to detection** | {{delivery_timestamp → first_report_timestamp}} | < 1 hour (good), 1-4h (acceptable), > 4h (needs improvement) | {{assessment}} |
| **Time to containment** | {{first_report → containment_complete}} | < 4 hours (good), 4-24h (acceptable), > 24h (needs improvement) | {{assessment}} |
| **Time to full scope** | {{first_report → scope_assessment_complete}} | < 2 hours (good), 2-8h (acceptable), > 8h (needs improvement) | {{assessment}} |
| **Email gateway catch rate** | {{emails_blocked / total_emails * 100}}% | > 90% (good), 50-90% (needs improvement), < 50% (poor) | {{assessment}} |
| **User click rate** | {{users_clicked / users_received * 100}}% | < 5% (good), 5-15% (average), > 15% (needs improvement) | {{assessment}} |
| **User report rate** | {{users_reported / users_received * 100}}% | > 20% (good), 5-20% (average), < 5% (needs improvement) | {{assessment}} |
| **Compromise rate** | {{(creds_submitted + endpoints_compromised) / users_received * 100}}% | < 1% (good), 1-5% (concerning), > 5% (critical) | {{assessment}} |
| **IOCs analyzed** | {{iocs_enriched}} of {{iocs_extracted}} extracted | 100% enrichment target | {{assessment}} |
| **Detection rules created** | {{detection_rules_created}} | N/A — every investigation should produce rules | {{assessment}} |
| **Purple Team items** | {{purple_team_items}} | N/A — every investigation should produce PT items | {{assessment}} |

**User Interaction Funnel:**
```
Received:              {{users_received}} ██████████████████████████████  100%
Opened/Previewed:      {{users_opened}}   ████████████████████░░░░░░░░░░  {{%}}
Clicked/Opened:        {{users_clicked}}  ████████████░░░░░░░░░░░░░░░░░░  {{%}}
Submitted Credentials: {{users_submitted_creds}} ████░░░░░░░░░░░░░░░░░░░░░░░░░░  {{%}}
Account Compromised:   {{accounts_compromised}} ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░  {{%}}
Endpoint Compromised:  {{endpoints_compromised}} █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  {{%}}
```

### 5. Lessons Learned

Populate the `## Lessons Learned` section:

**Lessons Learned — {{incident_id}}:**

#### What Worked Well
- {{what_worked_1 — e.g., "Email gateway caught 80% of deliveries via URL inspection"}}
- {{what_worked_2 — e.g., "User reported the phishing email within 15 minutes of delivery"}}
- {{what_worked_3 — e.g., "EDR detected and alerted on macro execution within seconds"}}

#### What Failed or Was Suboptimal
- {{what_failed_1 — e.g., "Email gateway did not detect the phishing email because the URL was not in any block list (newly registered domain)"}}
- {{what_failed_2 — e.g., "DMARC policy is set to p=none, so spoofed emails are not blocked"}}
- {{what_failed_3 — e.g., "No automated email purge capability — manual process took 4 hours"}}

#### What Would We Do Differently
- {{improvement_1 — e.g., "Implement automated email purge via Security Orchestration platform"}}
- {{improvement_2 — e.g., "Move DMARC policy from p=none to p=quarantine (phased rollout)"}}
- {{improvement_3 — e.g., "Add newly-registered-domain detection rule to email gateway"}}

#### Systemic Improvements Needed
- {{systemic_1 — e.g., "Security awareness training should include phishing simulation exercises quarterly"}}
- {{systemic_2 — e.g., "Implement URL click tracking in email security platform for faster scope assessment"}}
- {{systemic_3 — e.g., "Establish automated credential compromise detection (impossible travel, suspicious login patterns)"}}

#### Phishing-Specific Defense Gaps
| Gap | Current State | Recommended State | Priority | Owner |
|-----|--------------|-------------------|----------|-------|
| {{gap_1}} | {{current}} | {{recommended}} | {{P1/P2/P3}} | {{team}} |
| {{gap_2}} | {{current}} | {{recommended}} | {{P1/P2/P3}} | {{team}} |
| {{gap_3}} | {{current}} | {{recommended}} | {{P1/P2/P3}} | {{team}} |

### 6. Update Engagement Status

Update the engagement tracking with phishing incident completion data:

```yaml
engagement_id: {{engagement_id}}
last_updated: {{date}}
phishing_log:
  - incident_id: {{incident_id}}
    email_subject: {{email_subject}}
    email_sender: {{email_sender}}
    payload_type: {{payload_type}}
    severity: {{severity}}
    classification: {{classification}}
    mitre_techniques: {{T-codes}}
    blast_radius:
      received: {{users_received}}
      opened: {{users_opened}}
      clicked: {{users_clicked}}
      submitted_creds: {{users_submitted_creds}}
      accounts_compromised: {{accounts_compromised}}
      endpoints_compromised: {{endpoints_compromised}}
    containment_actions: {{containment_actions}}
    detection_rules_created: {{detection_rules_created}}
    purple_team_items: {{purple_team_items}}
    timestamp: {{date}}
    analyst: {{user_name}}
    time_to_detection: {{duration}}
    time_to_containment: {{duration}}
    regulatory_notification: {{required/not_required}}
```

### 7. Final Frontmatter Update and Completion Announcement

**Update the output document frontmatter:**

```yaml
stepsCompleted: [..., "step-08-reporting.md"]
workflowStatus: complete
completionDate: {{date}}
classification: {{classification}}
severity: {{severity}}
detection_rules_created: {{count}}
purple_team_items: {{count}}
```

Update the document header `**Status:**` from `In Progress` to `Completed`.

**Announce workflow completion:**

"**Phishing Response Workflow Completed!**

{{user_name}}, the phishing investigation for incident **{{incident_id}}** is complete.

**Final report:** `{outputFile}`

**Incident Summary:**
- **Email:** \"{{email_subject}}\" from {{email_sender}}
- **Payload:** {{payload_type}} ({{severity}} severity)
- **Authentication:** SPF: {{spf_result}} | DKIM: {{dkim_result}} | DMARC: {{dmarc_result}}

**Blast Radius:**
- Received: {{users_received}} | Clicked: {{users_clicked}} | Compromised: {{accounts_compromised + endpoints_compromised}}
- Click rate: {{click_rate}}% | Compromise rate: {{compromise_rate}}%

**Response:**
- Containment actions: {{containment_actions}} (Complete: {{complete_count}})
- Detection rules: {{detection_rules_created}}
- Purple Team items: {{purple_team_items}}

**Deliverables:**
- Complete phishing analysis report with {{section_count}} sections
- Evidence chain from intake through containment
- Executive summary with quantified metrics
- Detection rules: Sigma ({{count}}), YARA ({{count}}), Suricata ({{count}})
- Email gateway rules: {{count}}
- User communication templates: {{count}}
- Purple Team test scenarios: {{count}}
- Lessons learned and defense gap analysis

**Key Metrics:**
- Time to detection: {{duration}}
- Time to containment: {{duration}}
- Gateway catch rate: {{rate}}%
- User click rate: {{rate}}%

The phishing investigation report is ready to feed the detection improvement cycle and Purple Team operations."

### 8. Final Navigation Options

"**Available Options:**

[W] War Room — Red vs Blue debrief on the entire phishing investigation
[N] New Phishing — Start a new phishing investigation (fresh step-01-init.md)
[S] SOC Handoff — Package for L2/L3/IRT with full investigation context
[D] Detection Engineering — Hand off detection rules to Sentinel (`spectra-agent-detection-eng`)
[P] Purple Team — Hand off feedback to Red Team via `spectra-war-room`
[I] Incident Handling — Escalate to full incident response via Dispatch (`spectra-incident-handling`)

What would you like to do?"

#### Menu Handling Logic:

- IF W: Full War Room session — comprehensive Red vs Blue debrief on the entire phishing investigation. Red Team perspective: how effective was this phishing campaign? What would I improve as the attacker? How would I evade the new detection rules? What does the click rate tell me about the organization's susceptibility? How would I use the compromised accounts for the next stage? Blue Team perspective: was our response timeline adequate? Did we have the right data at the right time? Where were our visibility gaps? How does this phishing compare to industry benchmarks? What would we do differently in the next phishing incident? Grade the organization's phishing defense posture. This is the capstone analytical discussion.
- IF N: Inform the user to start a fresh phishing investigation. Provide engagement_id for reference. Recommend invoking `spectra-phishing-response` to launch a new workflow from step-01-init.md. The completed report remains at the current outputFile path.
- IF S: Package the phishing investigation findings into a standalone handoff format suitable for L2, L3, or IRT consumption. Include: executive summary, email details, blast radius, containment status, outstanding actions, evidence locations, and recommended next investigation steps. Ready for direct ingestion by the receiving team.
- IF D: Package the detection rules and email gateway recommendations from Step 7 into a format suitable for the detection engineering team or `spectra-agent-detection-eng`. Include: all Sigma/YARA/Suricata rules, email gateway rule specifications, DMARC enforcement recommendations. Each item actionable without requiring the detection engineer to re-read the full report.
- IF P: Package the Purple Team feedback from Step 7 into a format suitable for `spectra-war-room` or direct Red Team consumption. Include: gateway effectiveness assessment, SOC detection gaps, Red Team test scenarios, evasion variants. This is the bridge that closes the Red-Blue feedback loop for phishing defense.
- IF I: If the phishing investigation revealed significant compromise (Tier 4-5 users, lateral movement, data exposure), recommend escalation to full incident handling. Package the phishing investigation findings as the incident intake data for `spectra-incident-handling`. Include: incident timeline, compromised assets, containment status, and investigation findings.
- IF user asks questions: Answer and redisplay menu

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Report completeness validated — all 7 investigation sections populated (or gaps documented with justification)
- Containment status verified — pending actions documented
- Executive summary generated with all quantified metrics (blast radius, authentication results, response timeline, detection improvements)
- User interaction funnel presented with counts and percentages
- Key phishing response metrics calculated (time to detection, time to containment, click rate, compromise rate, gateway catch rate)
- Lessons learned documented: what worked, what failed, what to improve, systemic gaps
- Engagement status updated with phishing incident completion data
- Final frontmatter updated with workflowStatus: complete, completionDate, and all metrics
- Document status changed from "In Progress" to "Completed"
- Clear navigation options provided for next actions (W/N/S/D/P/I)
- User understands deliverables, outcomes, and recommended next actions

### SYSTEM FAILURE:

- Not validating report completeness before announcing completion
- Not verifying containment action status before closing
- Generating executive summary without quantified blast radius metrics
- Not calculating phishing-specific metrics (click rate, compromise rate, gateway catch rate)
- Skipping lessons learned — every phishing investigation must feed organizational learning
- Not updating engagement status with incident completion data
- Not providing clear next-action guidance via the navigation menu
- Loading additional workflow steps after this terminal step
- Performing any new investigation or response operations during completion
- Closing without documenting the user interaction funnel
- Not documenting regulatory notification status (required or not required)

**CRITICAL:** Reading only partial step file leads to incomplete understanding and poor decisions.
**CRITICAL:** Making decisions without complete understanding of step requirements and protocols.

## FINAL NOTE

The phishing analysis report documents the entire investigation chain: from email intake through header forensics, content analysis, IOC enrichment, scope assessment, containment, and detection improvement. Every finding is evidenced, every metric is quantified, every recommendation is specific. This report directly feeds the detection improvement cycle through Purple Team feedback and detection rules, and provides the organizational learning foundation through lessons learned and defense gap analysis.

**Phishing investigation for {{incident_id}} is complete. The detection improvement cycle continues.**
