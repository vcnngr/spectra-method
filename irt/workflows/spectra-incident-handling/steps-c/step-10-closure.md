# Step 10: Reporting & Engagement Closure

**Progress: Step 10 of 10** — This is the final step.

## STEP GOAL:

Generate the final incident handling report with executive summary, compile the complete timeline of events across all phases, consolidate the IOC summary for sharing, finalize prioritized recommendations, conduct report quality assurance, establish a distribution plan with TLP classification, complete the incident closure checklist, and formally close the incident within the engagement. This is the capstone step that transforms the operational incident data into a polished, distributable deliverable and ensures no loose ends remain.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate the executive summary or final report sections without operator input and review — the final report is a formal organizational artifact
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: This is the FINAL step — there is no next step file to load
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator completing the formal closure of a security incident under NIST 800-61
- ✅ The final report is a legal, regulatory, and organizational artifact — accuracy, completeness, and appropriate classification are non-negotiable
- ✅ The executive summary is written for non-technical leadership — translate all technical findings into business language
- ✅ IOC distribution requires TLP classification — uncontrolled dissemination of incident details creates risk
- ✅ Incident closure is not the end of activity — follow-up reviews (30/60/90 days), monitoring, and recommendation tracking continue
- ✅ Every section of the report must be populated — an incomplete report undermines the credibility of the entire incident response effort

### Step-Specific Rules:

- 🎯 Focus exclusively on executive summary generation, timeline compilation, IOC consolidation, recommendation finalization, report quality assurance, distribution planning, and closure checklist completion
- 🚫 FORBIDDEN to begin new investigation, containment, eradication, or recovery activity — this is documentation and closure
- 💬 Approach: Precise, formal, quality-focused — this is the final product that stakeholders, regulators, and leadership will reference
- 📊 The executive summary must be comprehensible to non-technical readers — no jargon without explanation
- 🔒 TLP classification is mandatory for every distribution channel — default to TLP:AMBER if uncertain
- ⏱️ Closure does not mean abandonment — enhanced monitoring, follow-up reviews, and recommendation tracking are part of closure
- 📝 The report completeness checklist is a hard gate — every section must be populated before closure

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Closing an incident without completing the post-incident review (step 9) wastes the most valuable improvement opportunity — if step 9 was marked incomplete or skipped, strongly recommend completing it before closure
  - Distributing a report without TLP classification risks uncontrolled dissemination of sensitive incident details — incident reports contain IOCs, vulnerability information, and organizational weaknesses that adversaries can exploit if leaked
  - Not scheduling follow-up reviews (30/60/90 days) means recommendations will not be tracked and the same incident pattern may recur — closure without follow-up is organizational amnesia
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your report finalization plan before beginning — let the operator know what sections will be generated and in what order
- ⚠️ Present [A]/[W]/[D] menu after closure is complete — there is NO [C] Continue option as this is the final step
- 💾 Save all sections to the output document as they are generated and reviewed
- 📖 Update frontmatter: add this step name to the end of stepsCompleted, set `incident_status` to the final status, and update all final tracking fields
- 🚫 This is the FINAL step — there is no next step file

## CONTEXT BOUNDARIES:

- Available context: Complete incident handling report with data from steps 1-9 (intake, detection, triage, containment, evidence, deep analysis, eradication, recovery, post-incident review), all frontmatter fields, engagement.yaml, PIR findings and recommendations
- Focus: Executive summary generation, timeline compilation, IOC consolidation, recommendation finalization, report QA, distribution planning, and formal closure — no new operational activity
- Limits: Do not fabricate findings or embellish the report — accuracy is paramount. The executive summary must accurately reflect the technical findings, not oversimplify to the point of misrepresentation
- Dependencies: All prior steps (1-9) should be completed. If step 9 (PIR) was not completed, WARN the operator before proceeding with closure

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Executive Summary Generation

Generate the executive summary for non-technical leadership. This is typically the only section that C-suite, board members, and regulators will read — it must be accurate, concise, and free of jargon.

"**Executive Summary — Draft for Review:**

I will draft the executive summary based on the complete incident data from steps 1-9. Please review carefully — this section will be the primary reference for leadership and may be shared with regulators."

**Executive Summary Structure:**

**Incident Overview** (2-3 sentences):
- What happened at a high level — type of incident, scope, and impact
- When it was detected and how long the adversary was active
- Current status

**Business Impact**:
- Operational disruption: services affected, duration of disruption, workarounds required
- Financial impact: estimated direct costs (response, recovery, remediation) and indirect costs (business disruption, reputational risk)
- Data exposure: what data was at risk, whether exfiltration was confirmed or suspected, number of records affected
- Regulatory implications: which regulatory frameworks apply (GDPR, HIPAA, PCI DSS, SEC, NIS2), whether notification obligations were triggered, notification status
- Reputational risk: customer impact, public disclosure requirements, media exposure risk

**Response Summary**:
- Key actions taken: containment approach, eradication steps, recovery timeline
- Response effectiveness: what went well in the response
- Timeline: detection to containment to eradication to recovery with durations

**Current Status**:
- Incident status: resolved / monitoring / ongoing with conditions
- Enhanced monitoring: what is being monitored and for how long
- Open actions: any remaining remediation work

**Key Findings**:
- Root cause: how the attacker gained access, what vulnerability or weakness was exploited
- Scope: total systems affected, users affected, data at risk
- Dwell time: how long the adversary was active before detection
- Attack sophistication: assessment of adversary capability and resources

**Recommendations for Leadership** (top 3-5):
- The most critical recommendations from the PIR, translated to business language
- Each recommendation should include: what needs to happen, why it matters (business risk), and the requested investment (time, budget, resources)
- Prioritized by business risk, not technical severity

**Writing Guidelines:**
- No jargon — translate technical findings to business language. "Lateral movement via Pass-the-Hash" becomes "the attacker used stolen credentials to access additional systems"
- Quantify where possible — systems affected, hours of disruption, data records at risk, estimated cost
- Focus on risk and business impact, not technical implementation details
- Be honest about what is known vs suspected vs unknown — clearly label uncertainties
- Include "what we did well" — leadership needs to know the investment in security capabilities paid off
- Keep the total executive summary under 2 pages when rendered

Present the draft executive summary to the operator:

"**Draft Executive Summary:**

{{draft executive summary}}

Please review this summary carefully. Is it:
- Accurate — does it correctly represent the technical findings?
- Complete — are any business-relevant findings missing?
- Appropriate — is the tone and level of detail suitable for the intended audience?
- Honest — are uncertainties clearly communicated?

I can adjust language, add details, or modify the framing before we finalize."

Wait for operator review and approval. Iterate until the operator is satisfied.

Write the approved executive summary under `## Executive Summary` in the report.

### 2. Complete Timeline of Events

Compile the master timeline from all steps into a single, chronologically ordered sequence. This timeline is the definitive record of both attacker and defender actions.

**Timeline Compilation:**

Gather timeline data from:
- Step 1: Detection timestamp, prior actions taken
- Step 2: Detection timeline, earliest indicators, dwell time estimate
- Step 3: Triage timeline, severity adjustments
- Step 4: Containment actions with timestamps
- Step 5: Evidence collection timeline, chain of custody entries
- Step 6: Deep analysis timeline — refined attack chain, root cause, scope determination
- Step 7: Eradication actions with timestamps and verification results
- Step 8: Recovery actions with timestamps and validation results

**Master Timeline Format:**

```
| # | Timestamp (UTC) | Phase | Event | System/Actor | Source | Confidence |
|---|-----------------|-------|-------|-------------|--------|------------|
```

**Timeline Phases** (for the Phase column):
- **Pre-Incident** — Attacker preparation, reconnaissance, infrastructure setup (if known from threat intel or forensic analysis)
- **Initial Compromise** — The moment of initial access — the first successful exploitation or credential use
- **Post-Compromise** — All adversary activity after initial access: persistence, privilege escalation, discovery, lateral movement, collection, staging, exfiltration
- **Detection** — The moment the incident was detected and the alert/report that triggered the response
- **Response Initiation** — IR team engagement, incident intake, initial classification
- **Containment** — All containment actions: isolation, lockout, quarantine, blocking
- **Evidence Collection** — Forensic imaging, memory capture, log collection, evidence chain entries
- **Analysis** — Key analysis milestones: root cause identification, scope determination, attack chain reconstruction
- **Eradication** — All eradication actions: malware removal, persistence cleanup, credential rotation, patch deployment
- **Recovery** — All recovery actions: system restoration, service re-enablement, validation, monitoring
- **Post-Incident** — PIR activities, recommendation generation, report finalization

**Timeline Quality Requirements:**
- Chronologically ordered — every entry must be in time order
- Both attacker actions AND defender actions in the same timeline — this shows the race between offense and defense
- Timestamps in UTC — convert any local timestamps to UTC with notation
- Confidence level for each entry — Confirmed (evidence-based), Probable (strong inference), Possible (weak inference), Estimated (timeline reconstruction)
- No gaps without explanation — if there are periods with no events, note whether this is adversary dormancy, visibility gap, or evidence destruction

Present the compiled timeline to the operator:

"**Master Timeline of Events — {{event_count}} entries across {{phase_count}} phases:**

{{timeline table}}

**Timeline Statistics:**
- Total timeline span: {{first event}} to {{last event}} = {{total duration}}
- Attacker actions: {{count}} events
- Defender actions: {{count}} events
- Pre-detection activity: {{count}} events (dwell time coverage)
- Post-detection activity: {{count}} events (response coverage)
- Timeline gaps: {{count}} unexplained gaps

Is this timeline complete and accurate? Are there any events that should be added, corrected, or removed?"

Wait for operator review. Integrate corrections.

Write under `## Timeline of Events` in the report.

### 3. IOC Summary

Consolidate all indicators of compromise from the entire incident into a structured, shareable format.

**IOC Compilation:**

Gather IOCs from:
- Step 1: Initial indicators from intake
- Step 2: Enriched IOCs with threat intel context
- Step 6: Additional IOCs discovered during deep analysis
- Step 7: IOCs related to persistence mechanisms and eradication

**IOC Summary Structure:**

"**Consolidated IOC Summary:**

### Network IOCs

| # | Type | Value | Context | First Seen | Last Seen | Confidence | TLP |
|---|------|-------|---------|-----------|----------|------------|-----|
| 1 | IP Address | {{ip}} | {{role in attack — C2, exfil, staging}} | {{timestamp}} | {{timestamp}} | High/Medium/Low | {{TLP}} |
| 2 | Domain | {{domain}} | {{role in attack}} | {{timestamp}} | {{timestamp}} | High/Medium/Low | {{TLP}} |
| 3 | URL | {{url}} | {{role in attack}} | {{timestamp}} | {{timestamp}} | High/Medium/Low | {{TLP}} |

### Host IOCs

| # | Type | Value | Context | System | Confidence | TLP |
|---|------|-------|---------|--------|------------|-----|
| 1 | File Hash (SHA256) | {{hash}} | {{malware family, tool name}} | {{affected host}} | High/Medium/Low | {{TLP}} |
| 2 | File Path | {{path}} | {{purpose — persistence, staging, tool}} | {{affected host}} | High/Medium/Low | {{TLP}} |
| 3 | Registry Key | {{key}} | {{purpose — persistence, config}} | {{affected host}} | High/Medium/Low | {{TLP}} |
| 4 | Service Name | {{service}} | {{purpose — persistence, backdoor}} | {{affected host}} | High/Medium/Low | {{TLP}} |
| 5 | Scheduled Task | {{task}} | {{purpose — persistence, execution}} | {{affected host}} | High/Medium/Low | {{TLP}} |

### Email IOCs

| # | Type | Value | Context | Confidence | TLP |
|---|------|-------|---------|------------|-----|
| 1 | Sender Address | {{email}} | {{role — phishing, social engineering}} | High/Medium/Low | {{TLP}} |
| 2 | Subject Line | {{subject}} | {{campaign context}} | High/Medium/Low | {{TLP}} |
| 3 | Attachment Hash | {{hash}} | {{payload type}} | High/Medium/Low | {{TLP}} |

### Behavioral IOCs

| # | ATT&CK Technique | Behavior Description | Detection Method | Confidence | TLP |
|---|-----------------|---------------------|-----------------|------------|-----|
| 1 | {{T-code}} | {{specific behavior observed}} | {{how to detect this behavior}} | High/Medium/Low | {{TLP}} |
| 2 | ... | ... | ... | ... | ... |

**IOC Statistics:**
- Total IOCs: {{count}}
- Network IOCs: {{count}} (IPs: {{count}}, Domains: {{count}}, URLs: {{count}})
- Host IOCs: {{count}} (Hashes: {{count}}, Paths: {{count}}, Registry: {{count}}, Services: {{count}}, Tasks: {{count}})
- Email IOCs: {{count}}
- Behavioral IOCs: {{count}}
- Deduplicated: {{original count}} → {{final count}} ({{removed}} duplicates removed)"

**IOC Sharing Considerations:**

"**IOC Sharing Assessment:**

| Consideration | Assessment |
|--------------|-----------|
| TLP Classification (default) | {{TLP:WHITE / TLP:GREEN / TLP:AMBER / TLP:RED}} |
| Rationale | {{why this TLP level}} |
| STIX/TAXII format | Recommended for automated sharing — structured IOC package |
| Sharing partners | {{ISACs, sector CERTs, law enforcement, peer organizations}} |
| Sharing restrictions | {{any IOCs that must NOT be shared — e.g., internal IPs, sensitive file paths}} |
| Expiration | {{recommended IOC expiration date — infrastructure IOCs typically 90 days, hash IOCs longer}} |

**Cross-Module Recommendation:**
- **Oracle** (`spectra-threat-intel-workflow`): Recommend invoking Oracle to produce a formal threat intelligence product from these IOCs — structured for sharing with ISACs, sector CERTs, and peer organizations. Oracle can package the IOCs in STIX format with proper TLP markings and contextual narrative."

Wait for operator review. Adjust TLP classifications and sharing decisions as directed.

Write under `## IOC Summary` in the report.

### 4. Final Recommendations — Consolidated & Prioritized

Compile recommendations from all steps into a single, prioritized list organized by implementation timeline.

**Recommendation Compilation:**

Gather recommendations from:
- Step 3: Triage recommendations (if any)
- Step 4: Containment lessons and recommendations
- Step 6: Deep analysis findings and recommendations
- Step 7: Eradication recommendations for hardening
- Step 8: Recovery recommendations for resilience
- Step 9: Full PIR recommendation set (primary source)

**Consolidated Recommendations by Priority:**

"**Final Recommendations — Consolidated from All Steps:**

### Immediate (0-30 days)

Critical actions that must be completed NOW to prevent recurrence or address remaining risk:

| # | Recommendation | Category | Owner | Deadline | Status | Source Step |
|---|---------------|----------|-------|----------|--------|------------|
| I-1 | {{critical action}} | {{Detection/Response/Prevention/Process/Training}} | {{owner}} | {{date}} | Pending | Step {{N}} |
| I-2 | ... | ... | ... | ... | ... | ... |

### Short-term (30-90 days)

Infrastructure and process improvements based on root cause analysis:

| # | Recommendation | Category | Owner | Deadline | Status | Source Step |
|---|---------------|----------|-------|----------|--------|------------|
| S-1 | {{improvement action}} | {{category}} | {{owner}} | {{date}} | Pending | Step {{N}} |
| S-2 | ... | ... | ... | ... | ... | ... |

### Long-term (90-365 days)

Strategic investments and organizational changes for lasting improvement:

| # | Recommendation | Category | Owner | Deadline | Status | Source Step |
|---|---------------|----------|-------|----------|--------|------------|
| L-1 | {{strategic action}} | {{category}} | {{owner}} | {{date}} | Pending | Step {{N}} |
| L-2 | ... | ... | ... | ... | ... | ... |

**Recommendation Summary:**
- Immediate actions: {{count}} (Critical priority)
- Short-term actions: {{count}} (High priority)
- Long-term actions: {{count}} (Medium priority)
- Total recommendations: {{count}}
- Recommendations with assigned owners: {{count}} / {{total}}
- Recommendations with deadlines: {{count}} / {{total}}"

"Are these recommendations complete, properly prioritized, and accurately attributed? Any additions or modifications?"

Wait for operator review.

Write under `## Recommendations` in the report.

### 5. Report Finalization — Quality Assurance

Conduct a systematic quality check on the complete report. This is a hard gate — every section must pass before the incident can be closed.

**Report Completeness Checklist:**

"**Report Completeness Audit:**

| # | Section | Status | Notes |
|---|---------|--------|-------|
| 1 | Incident Intake & Classification | {{Populated / Missing / Incomplete}} | {{details}} |
| 2 | Detection Source Analysis | {{Populated / Missing / Incomplete}} | {{details}} |
| 3 | Initial Analysis & Triage | {{Populated / Missing / Incomplete}} | {{details}} |
| 4 | Containment Strategy & Execution | {{Populated / Missing / Incomplete}} | {{details}} |
| 5 | Evidence Preservation | {{Populated / Missing / Incomplete}} | {{details}} |
| 6 | Deep Analysis & Scope Determination | {{Populated / Missing / Incomplete}} | {{details}} |
| 7 | Eradication Plan | {{Populated / Missing / Incomplete}} | {{details}} |
| 8 | Recovery & Restoration | {{Populated / Missing / Incomplete}} | {{details}} |
| 9 | Post-Incident Review | {{Populated / Missing / Incomplete}} | {{details}} |
| 10 | Executive Summary | {{Populated / Missing / Incomplete}} | {{details}} |
| 11 | Timeline of Events | {{Populated / Missing / Incomplete}} | {{details}} |
| 12 | IOC Summary | {{Populated / Missing / Incomplete}} | {{details}} |
| 13 | Recommendations | {{Populated / Missing / Incomplete}} | {{details}} |

**Quality Checks:**

| # | Quality Criterion | Status | Notes |
|---|------------------|--------|-------|
| 1 | All sections have substantive content (no empty/placeholder sections) | {{Pass / Fail}} | {{details}} |
| 2 | Timeline is chronologically ordered | {{Pass / Fail}} | {{details}} |
| 3 | IOCs are deduplicated | {{Pass / Fail}} | {{details}} |
| 4 | Recommendations are SMART (Specific, Measurable, Assigned, Realistic, Time-bound) | {{Pass / Fail}} | {{details}} |
| 5 | Executive summary is non-technical and business-focused | {{Pass / Fail}} | {{details}} |
| 6 | All findings have evidence references | {{Pass / Fail}} | {{details}} |
| 7 | Sensitive information appropriately classified/marked | {{Pass / Fail}} | {{details}} |
| 8 | Frontmatter fields are complete and accurate | {{Pass / Fail}} | {{details}} |
| 9 | Incident ID is consistent throughout the report | {{Pass / Fail}} | {{details}} |
| 10 | Timestamps are in UTC format consistently | {{Pass / Fail}} | {{details}} |
| 11 | ATT&CK techniques use correct T-codes | {{Pass / Fail}} | {{details}} |
| 12 | Evidence chain references are intact | {{Pass / Fail}} | {{details}} |

**Overall Report Status:** {{PASS — ready for distribution / FAIL — requires remediation}}

{{IF any section is Missing or Incomplete:}}
**ACTION REQUIRED:** The following sections need attention before the report can be finalized:
{{list of incomplete sections with what's missing}}

Would you like to address these gaps now, or note them as known limitations in the report?
{{END IF}}

{{IF any quality check fails:}}
**QUALITY ISSUES:** The following quality criteria were not met:
{{list of failed checks with remediation guidance}}

Would you like to remediate these issues now?
{{END IF}}"

Wait for operator to address any issues or accept the report as-is with noted limitations.

### 6. Report Distribution Plan

Establish who receives the report and at what classification level.

"**Report Distribution Plan:**

| # | Recipient | Distribution Type | Content | TLP | Method | Timing |
|---|-----------|------------------|---------|-----|--------|--------|
| 1 | IR Team | Full Report | Complete report with all technical details | TLP:RED | Secure file share | Immediate |
| 2 | CISO / Security Leadership | Full Report | Complete report | TLP:RED | Secure file share | Immediate |
| 3 | Executive Leadership / C-Suite | Executive Summary Only | Executive summary + recommendations | TLP:AMBER | Email / briefing | Within 24h |
| 4 | Legal Counsel | Full Report | Complete report for legal review | TLP:RED | Secure file share | Immediate |
| 5 | Regulators (if required) | Regulatory Notification | Notification format per regulatory requirements | TLP:AMBER | Regulatory portal / certified mail | Per regulatory timeline |
| 6 | Law Enforcement (if applicable) | Investigation Package | Timeline, IOCs, evidence references | TLP:AMBER | Law enforcement liaison | Per LE timeline |
| 7 | Board of Directors (if required) | Board Summary | High-level summary + business impact + key recommendations | TLP:RED | Board presentation | Next board meeting |
| 8 | Insurance (if applicable) | Claims Documentation | Incident details per policy requirements | TLP:RED | Insurance liaison | Per policy requirements |
| 9 | Affected Customers (if required) | Customer Notification | Impact description + protective actions | TLP:WHITE | Customer communication channel | Per notification timeline |
| 10 | Industry Partners / ISAC | IOC Package | Sanitized IOCs + TTP summary | TLP:GREEN | ISAC sharing portal / STIX/TAXII | After internal distribution |

**Distribution Guidelines:**
- **TLP:RED** — Restricted to named recipients only. No further sharing without explicit permission.
- **TLP:AMBER** — Limited distribution within the recipient's organization. Need-to-know basis.
- **TLP:GREEN** — May be shared within the recipient's community (sector, ISAC). Not for public disclosure.
- **TLP:WHITE** — May be shared freely. Ensure no sensitive details remain before classifying as WHITE.

**Cross-Module Recommendations:**
- **Chronicle** (`spectra-agent-chronicle`): Invoke Chronicle to produce a polished, presentation-ready version of the full incident report — formatted for executive consumption with visualizations and narrative flow.
- **spectra-executive-brief**: Invoke for a board-level summary that distills the incident to a 1-2 page executive brief with business impact focus and strategic recommendations.

Which recipients apply to this incident? Adjust the distribution list as needed."

Wait for operator input. Adjust distribution plan based on the operator's direction.

### 7. Incident Closure Checklist

Systematically verify all closure requirements are met.

"**Incident Closure Checklist — Incident {{incident_id}}:**

### Operational Closure

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 1 | All containment actions documented with timestamps | {{Complete / Incomplete}} | {{details}} |
| 2 | All evidence preserved with chain of custody intact | {{Complete / Incomplete}} | {{evidence_chain_intact status}} |
| 3 | All eradication actions verified and documented | {{Complete / Incomplete}} | {{eradication_status}} |
| 4 | All systems recovered, validated, and returned to service | {{Complete / Incomplete}} | {{recovery_status}} |
| 5 | Post-incident review completed with lessons learned | {{Complete / Incomplete}} | {{post_incident_completed status}} |
| 6 | All recommendations documented with SMART criteria | {{Complete / Incomplete}} | {{recommendation count}} |
| 7 | Report finalized and quality-checked | {{Complete / Incomplete}} | {{report QA status}} |
| 8 | Report distributed to appropriate recipients | {{Complete / Incomplete}} | {{distribution status}} |

### Monitoring & Follow-up

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 9 | Enhanced monitoring active (30-day minimum) | {{Active / Not Started / Not Required}} | {{monitoring details}} |
| 10 | Follow-up review scheduled — 30 days | {{Scheduled / Not Scheduled}} | {{date if scheduled}} |
| 11 | Follow-up review scheduled — 60 days | {{Scheduled / Not Scheduled}} | {{date if scheduled}} |
| 12 | Follow-up review scheduled — 90 days | {{Scheduled / Not Scheduled}} | {{date if scheduled}} |
| 13 | Recommendation tracking mechanism established | {{Established / Not Established}} | {{tracking method}} |

### Legal & Regulatory

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 14 | Legal review of report completed (if required) | {{Complete / Not Required / Pending}} | {{details}} |
| 15 | Regulatory notification obligations addressed | {{Complete / Not Required / Pending}} | {{regulatory frameworks, notification dates}} |
| 16 | Law enforcement coordination complete (if applicable) | {{Complete / Not Required / Pending}} | {{details}} |
| 17 | Evidence retention plan established | {{Established / Not Established}} | {{retention period, storage location}} |
| 18 | Insurance notification complete (if applicable) | {{Complete / Not Required / Pending}} | {{details}} |

### Knowledge Management

| # | Requirement | Status | Notes |
|---|------------|--------|-------|
| 19 | IOCs shared with threat intel team / database | {{Complete / Pending}} | {{sharing status}} |
| 20 | Detection rules updated based on findings | {{Complete / Pending / Tracked as Recommendation}} | {{details}} |
| 21 | IR playbook updated based on lessons learned | {{Complete / Pending / Tracked as Recommendation}} | {{details}} |
| 22 | Knowledge base entry created | {{Complete / Pending}} | {{details}} |

**Closure Determination:**

Based on the checklist above:
- **If ALL items are Complete or Not Required:** Incident Status → **CLOSED**
- **If enhanced monitoring is still active (item 9):** Incident Status → **MONITORING** — incident will close automatically after the monitoring period ends. Schedule a review at the end of the monitoring period.
- **If recommendations are pending but operational closure is complete:** Incident Status → **CLOSED WITH OPEN ACTIONS** — operational incident is resolved but improvement actions are tracked separately through the recommendation tracking mechanism.

**Recommended Status:** {{CLOSED / MONITORING / CLOSED WITH OPEN ACTIONS}}

Do you confirm this status?"

Wait for operator to confirm or adjust the incident status.

### 8. Update Frontmatter — Final State

Update the incident handling report frontmatter with all final values:

- `incident_status`: Set to the confirmed status from section 7 ('closed', 'monitoring', or 'closed-with-open-actions')
- Add `step-10-closure.md` to stepsCompleted array
- `closure_timestamp`: Current timestamp in UTC
- `report_finalized`: true
- `total_duration`: Calculate from detection_timestamp to closure_timestamp
- `total_recommendations`: Count of all recommendations
- `total_iocs`: Count of all deduplicated IOCs
- `total_evidence_items`: Count from evidence chain
- `total_timeline_events`: Count from master timeline
- `distribution_tlp`: Default TLP classification for the report
- `monitoring_end_date`: If status is 'monitoring', set the monitoring end date (30 days from closure by default)
- `follow_up_30_day`: Date for 30-day follow-up review
- `follow_up_60_day`: Date for 60-day follow-up review
- `follow_up_90_day`: Date for 90-day follow-up review

### 9. Append Final Sections to Report

Write the executive summary, timeline, IOC summary, and recommendations sections to the output document. These are the sections generated in steps 1-4 of this step file.

Verify the complete report structure:

```markdown
---
(frontmatter with all final values)
---

# Incident Handling Report — {{incident_id}}

## Executive Summary
{{from section 1 of this step}}

## Incident Intake & Classification
{{from step-01-init.md}}

## Detection Source Analysis
{{from step-02-detection.md}}

## Initial Analysis & Triage
{{from step-03-triage.md}}

## Containment Strategy & Execution
{{from step-04-containment.md}}

## Evidence Preservation
{{from step-05-evidence.md}}

## Deep Analysis & Scope Determination
{{from step-06-deep-analysis.md}}

## Eradication Plan
{{from step-07-eradication.md}}

## Recovery & Restoration
{{from step-08-recovery.md}}

## Post-Incident Review
{{from step-09-post-incident.md}}

## Timeline of Events
{{from section 2 of this step}}

## IOC Summary
{{from section 3 of this step}}

## Recommendations
{{from section 4 of this step}}
```

### 10. Final Message to Operator

Present the formal incident closure communication:

"**INCIDENT {{incident_id}} — CLOSURE REPORT**

{{user_name}}, the incident handling workflow for {{engagement_name}} is now complete.

**Incident Summary:**
- **Severity:** {{incident_severity}}
- **Category:** {{incident_category}}
- **Duration:** {{total_duration}}
- **Dwell Time:** {{dwell_time}}
- **Systems Affected:** {{affected_systems}}
- **Users Affected:** {{affected_users}}
- **Root Cause:** {{root_cause}}
- **Status:** {{incident_status}}

**Key Metrics:**
- MTTD: {{mttd}} | MTTR: {{mttr}} | MTTC: {{mttc}}
- Evidence items: {{total_evidence_items}} | Evidence chain: {{evidence_chain_intact}}
- IOCs identified: {{total_iocs}} | ATT&CK techniques: {{mitre_techniques count}}

**Report:** `{outputFile}`
- Sections: {{section count}} / 13 populated
- Recommendations: {{total_recommendations}} (Immediate: {{count}} | Short-term: {{count}} | Long-term: {{count}})

**Follow-up Schedule:**
- Enhanced monitoring ends: {{monitoring_end_date}}
- 30-day review: {{follow_up_30_day}}
- 60-day review: {{follow_up_60_day}}
- 90-day review: {{follow_up_90_day}}

**Recommended Next Steps:**
- For polished report: invoke Chronicle (`spectra-agent-chronicle`)
- For executive brief: invoke `spectra-executive-brief`
- For detection rules: invoke Sentinel (`spectra-detection-lifecycle`)
- For threat intelligence product: invoke Oracle (`spectra-threat-intel-workflow`)
- For lessons learned implementation: invoke `spectra-debrief`
- For engagement closure: invoke `spectra-close-engagement`"

### 11. Present FINAL MENU OPTIONS

This is the FINAL step. There is NO [C] Continue option. The workflow completes here.

"**Incident handling workflow complete.**

**Select an option:**
[A] Advanced Elicitation — Deep review of any report section for additional insights, challenge completeness, probe for overlooked findings
[W] War Room — Full team retrospective on the incident response: Handler, Forensics, Threat Intel, SOC, Management — all perspectives on what this incident means for the organization
[D] Done — Mark workflow as complete and finalize

**Additional options:**
[CH] Invoke Chronicle for polished final report
[EB] Invoke spectra-executive-brief for board summary
[DL] Invoke spectra-detection-lifecycle for new detection rules
[TI] Invoke spectra-threat-intel-workflow for intelligence product
[DB] Invoke spectra-debrief for formal lessons learned session"

#### Menu Handling Logic:

- IF A: Deep analysis of any selected section — operator chooses which section to examine. Challenge the executive summary for accuracy and appropriate language, probe the timeline for missing events, verify IOC completeness, stress-test recommendations for SMART compliance, question whether the closure checklist is honestly assessed. Process insights, ask operator if they want to update the report, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room — Full team retrospective with all agent perspectives: Handler perspective: was the coordination model effective? Were 10-step workflows the right granularity? What would you change about the workflow? Forensics perspective: was evidence handling adequate throughout? Were chain of custody protocols followed? Was analysis depth sufficient? Threat Intel perspective: what does this incident tell us about the threat landscape? Is this actor likely to return? Are there related campaigns we should be watching? SOC perspective: what detection improvements are most urgent? Were the detection rules that fired reliable? What new telemetry would have helped? Management perspective: was communication adequate? Were resource allocation decisions sound? What organizational changes would improve future response? Summarize all perspectives, redisplay menu
- IF D: Confirm workflow completion to operator: "Incident handling workflow for {{incident_id}} is now marked as complete. The final report is available at `{outputFile}`. Thank you for your leadership through this incident, {{user_name}}." — end workflow
- IF CH: Recommend operator invoke `spectra-agent-chronicle` for polished report generation. Provide context: incident_id, report path, key findings summary for Chronicle to work with. Redisplay menu
- IF EB: Recommend operator invoke `spectra-executive-brief` for board-level summary. Provide context: incident_id, executive summary section, key metrics, top recommendations. Redisplay menu
- IF DL: Recommend operator invoke `spectra-detection-lifecycle` for detection rule development. Provide context: IOC list, ATT&CK mapping, detection gaps identified in PIR. Redisplay menu
- IF TI: Recommend operator invoke `spectra-threat-intel-workflow` for formal intelligence product. Provide context: IOC package, threat actor indicators, campaign context from deep analysis. Redisplay menu
- IF DB: Recommend operator invoke `spectra-debrief` for formal lessons learned implementation session. Provide context: PIR findings, recommendation list, gap analysis from step 9. Redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- [D] Done is the ONLY option that ends the workflow — all other options return to this menu
- Do NOT auto-close the workflow — the operator must explicitly select [D] Done

## CRITICAL STEP COMPLETION NOTE

This is the FINAL step. When the operator selects [D] Done, the workflow is complete. The frontmatter should already be updated with this step added to stepsCompleted and incident_status set to the final status. No further step files will be loaded. The incident handling report at `{outputFile}` is the final deliverable.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Executive summary generated in non-technical business language, reviewed and approved by operator
- Executive summary accurately represents technical findings without jargon — quantified impact where possible
- Complete timeline compiled from all steps (1-9) with chronological ordering, both attacker and defender actions
- Timeline includes phase classification, source references, and confidence levels for every entry
- IOC summary consolidated, deduplicated, and organized by type (Network, Host, Email, Behavioral)
- TLP classification assigned to each IOC set with rationale
- IOC sharing considerations documented (partners, format, restrictions, expiration)
- Recommendations consolidated from all steps, organized by timeline (Immediate/Short-term/Long-term)
- All recommendations verified as SMART with owner, deadline, and success metric
- Report completeness audit conducted — all 13 sections checked
- Report quality checks passed — timeline order, IOC deduplication, SMART compliance, non-technical executive summary, evidence references, sensitive data marking
- Report distribution plan established with TLP classification for each recipient
- Incident closure checklist completed with all 22 items assessed
- Incident status determined and confirmed by operator (CLOSED / MONITORING / CLOSED WITH OPEN ACTIONS)
- Enhanced monitoring confirmed active with end date
- Follow-up reviews scheduled (30/60/90 days)
- Evidence retention plan established
- Frontmatter updated with all final values (status, closure timestamp, total counts, follow-up dates)
- All final sections written to report (Executive Summary, Timeline, IOC Summary, Recommendations)
- Final closure message presented to operator with complete summary and next-step recommendations
- Menu presented with correct options (A/W/D + CH/EB/DL/TI/DB) — NO [C] Continue option
- Workflow terminates only when operator selects [D] Done

### ❌ SYSTEM FAILURE:

- Generating an executive summary with technical jargon that non-technical leadership cannot understand
- Generating an executive summary that misrepresents or oversimplifies the technical findings
- Not compiling a complete timeline from all steps — omitting attacker actions, defender actions, or entire phases
- Timeline entries without timestamps or out of chronological order
- IOCs not deduplicated — duplicate entries indicate sloppy compilation
- IOC summary without TLP classification — distributing IOCs without TLP creates uncontrolled dissemination risk
- Recommendations not organized by implementation timeline (Immediate/Short-term/Long-term)
- Recommendations that fail SMART criteria (vague, unassigned, no deadline)
- Report sections left empty or with placeholder content
- Not conducting the report completeness audit — skipping quality assurance
- Not establishing a report distribution plan with TLP classification
- Not completing the incident closure checklist
- Closing the incident without scheduling follow-up reviews (30/60/90 days)
- Closing the incident without establishing evidence retention plan
- Not setting the correct incident status based on closure checklist results
- Including a [C] Continue option in the menu — this is the FINAL step
- Auto-closing the workflow without operator selecting [D] Done
- Initiating new investigation, containment, or response activity in this closure step
- Proceeding without operator review and approval of the executive summary
- Not presenting cross-module recommendations (Chronicle, Executive Brief, Sentinel, Oracle, Debrief)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is the capstone step — the quality of the final report reflects the quality of the entire incident response effort. Every section must be populated. The executive summary must be non-technical. IOCs must have TLP classification. Recommendations must be SMART. The incident is not closed until the operator says it is closed.
