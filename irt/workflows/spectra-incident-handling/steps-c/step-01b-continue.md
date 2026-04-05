# Step 1B: Workflow Resumption

## STEP GOAL:

Resume the incident handling workflow from where it was left off, ensuring smooth continuation with full context restoration including engagement scope, incident classification, containment status, evidence chain integrity, affected systems inventory, and all prior operational findings. Incident response is time-critical — fast, accurate resumption directly impacts business outcomes.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE AN INCIDENT RESPONSE COORDINATOR resuming active incident management
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are an Incident Response Coordinator managing an active security incident under NIST 800-61
- Resume workflow from exact point where it was interrupted
- Re-verify that the engagement is still active and dates are still valid
- Re-verify that incident response authorization has not been revoked or modified
- All prior findings, containment actions, and operational state remain valid unless scope has changed
- Evidence chain integrity must be confirmed — any gap in custody since last session must be flagged
- Containment actions taken in prior sessions remain in effect unless explicitly reversed
- If the incident has escalated or de-escalated since last session, the severity classification may need updating

### Step-Specific Rules:

- FOCUS on understanding where we left off and continuing appropriately
- FORBIDDEN to modify content completed in previous steps
- Reload engagement.yaml to re-verify authorization
- If engagement has expired since last session: HARD STOP
- If RoE has been amended since last session: flag changes to operator
- If containment actions from prior session have been reversed or failed: flag immediately
- If new IOCs have been reported since last session: note for downstream integration
- Time-sensitive context: calculate elapsed time since last session — during an active incident, gaps matter

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive actions ONLY (ransomware deployment, intentional data destruction, wipers, tools designed to cause permanent damage to victim systems). This is the ONLY action the agent refuses. Incident response is defensive — there is no scenario where these are appropriate.
- WARN with explanation if you identify risk in the operator's approach:
  - Resuming a workflow on an expired or deactivated engagement invalidates all prior authorization — re-verification is essential
  - Skipping engagement re-verification and jumping straight to operations risks operating under changed conditions since the previous session
  - Skipping to a future step without verifying document state consistency may lead to unreliable operations based on corrupted or incomplete state
  - Skipping containment verification when resuming mid-incident risks operating on assumptions about containment that may no longer be valid — an attacker may have evaded containment during the session gap
  - Jumping directly to eradication or recovery without confirming containment is holding risks incomplete removal and reinfection
  - Proceeding with evidence collection without re-verifying chain of custody integrity risks evidence admissibility and forensic soundness
  - Resuming stakeholder communications without checking for new developments risks sending outdated information to executives or regulators
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Show your analysis of current state before taking action
- Update frontmatter: add this step name to the end of the stepsCompleted array
- Reload engagement.yaml and verify it is still active
- FORBIDDEN to begin new containment, eradication, or recovery actions during continuation setup
- FORBIDDEN to modify evidence chain records during continuation setup
- Calculate time elapsed since last session and flag if critical thresholds have been exceeded

## CONTEXT BOUNDARIES:

- Available context: Current document and frontmatter are already loaded
- Focus: Workflow state analysis and continuation logic only
- Limits: Don't assume knowledge beyond what's in the document and engagement.yaml
- Dependencies: Existing workflow state from previous session
- Time sensitivity: Incident response has time-critical dependencies — session gaps affect containment effectiveness and evidence freshness

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Re-verify Engagement Authorization

**Before anything else:**

- Reload `engagement.yaml`
- Verify `status` is still `active`
- Verify dates: `start_date <= today <= end_date`
- Verify incident response operations are still authorized in the engagement scope
- Check for any RoE amendments since the last session — compare engagement.yaml modification timestamp against last stepsCompleted timestamp if available
- If engagement has expired or been deactivated:

"**BLOCK — Engagement no longer active.**

Engagement {{engagement_id}} is now {{expired/deactivated}} since your last session.
No incident response activity may continue under this authorization.

**CRITICAL:** If the incident is still active, this is a procedural gap — the engagement must be renewed before response operations can resume. Contact the engagement lead immediately.

Active containment measures remain in place but cannot be modified without re-authorization."

**HARD STOP — Do not proceed.**

### 2. Analyze Current State

**State Assessment:**

Review the frontmatter to understand:

- `stepsCompleted`: Array of completed step filenames (last element = most recently completed)
- `engagement_id`, `engagement_name`: Engagement context
- `incident_id`: The unique incident identifier assigned during intake
- `incident_severity`: Current severity classification (Critical / High / Medium / Low)
- `incident_category`: Incident category (malware, unauthorized-access, data-breach, denial-of-service, insider-threat, supply-chain, other)
- `incident_status`: Current incident lifecycle status (open / contained / eradicated / recovered / closed)
- `detection_source`: Where the incident was first detected (SOC alert, user report, automated detection, threat intel, third-party notification)
- `detection_timestamp`: When the incident was first detected — use this to calculate current incident duration
- `initial_classification`, `initial_classification_confidence`: How the incident was first classified and confidence level
- `mitre_techniques`: Array of identified MITRE ATT&CK techniques
- `containment_status`: Current containment state (pending / partial / full / failed / bypassed)
- `containment_strategy`: The containment approach selected (isolation, segmentation, monitoring, hybrid)
- `containment_timestamp`: When containment was achieved — use this to calculate time-to-contain
- `eradication_status`: Current eradication state (pending / in-progress / complete / failed)
- `eradication_timestamp`: When eradication was completed
- `recovery_status`: Current recovery state (pending / in-progress / complete / failed)
- `recovery_timestamp`: When recovery was completed
- `affected_systems`: Count of systems identified as affected
- `affected_users`: Count of users identified as affected
- `affected_data`: Description of data types affected (PII, financial, intellectual property, credentials, etc.)
- `iocs_identified`, `iocs_enriched`: IOC counts — identified vs enriched with threat intelligence
- `evidence_items`: Count of evidence items collected
- `evidence_chain_intact`: Boolean — whether chain of custody is unbroken
- `root_cause`: Identified root cause (if deep analysis completed)
- `attack_vector`: How the attacker gained initial access
- `dwell_time`: Calculated time between initial compromise and detection
- `lateral_movement_detected`: Boolean — whether lateral movement was observed
- `data_exfiltration_detected`: Boolean — whether data exfiltration was observed
- `persistence_mechanisms`: Count of identified persistence mechanisms
- `stakeholder_notifications`: Count of stakeholder notifications sent
- `regulatory_notifications`: Count of regulatory notifications sent
- `post_incident_completed`: Boolean — whether post-incident review has been done
- `soc_triage_loaded`: Whether SOC alert-triage data was loaded during intake
- `soc_alert_id`: The SOC alert ID that triggered escalation (if applicable)
- `forensics_launched`: Whether digital forensics workflow was invoked
- `malware_analysis_launched`: Whether malware analysis workflow was invoked
- `threat_intel_launched`: Whether threat intelligence workflow was invoked

**Time-Critical Calculations:**
- Calculate elapsed time since `detection_timestamp` (total incident duration)
- Calculate elapsed time since `containment_timestamp` (time in containment)
- Calculate elapsed time since last session (session gap)
- Flag if session gap exceeds 4 hours for Critical severity incidents
- Flag if session gap exceeds 12 hours for High severity incidents
- Flag if session gap exceeds 24 hours for Medium/Low severity incidents

### 3. Determine Next Step

**Step Sequence Lookup:**

Use the following ordered sequence to determine the next step from the last completed step:

| Last Completed | Next Step |
|---|---|
| step-01-init.md | step-02-detection.md |
| step-02-detection.md | step-03-triage.md |
| step-03-triage.md | step-04-containment.md |
| step-04-containment.md | step-05-evidence.md |
| step-05-evidence.md | step-06-deep-analysis.md |
| step-06-deep-analysis.md | step-07-eradication.md |
| step-07-eradication.md | step-08-recovery.md |
| step-08-recovery.md | step-09-post-incident.md |
| step-09-post-incident.md | step-10-closure.md |

1. Get the last element from the `stepsCompleted` array
2. Look it up in the table above to find the next step
3. That's the next step to load!

**Example:**
- If `stepsCompleted = ["step-01-init.md", "step-02-detection.md", "step-03-triage.md", "step-04-containment.md"]`
- Last element is `"step-04-containment.md"`
- Table lookup -> next step is `./step-05-evidence.md`

**Phase Awareness:**
When presenting the next step, also indicate the NIST 800-61 phase transition if applicable:
- Steps 01-03: Detection & Analysis phase
- Step 04-05: Containment phase
- Step 06: Deep Analysis phase (iterative with Containment)
- Step 07: Eradication phase
- Step 08: Recovery phase
- Steps 09-10: Post-Incident Activity phase

### 4. Handle Workflow Completion

**If `stepsCompleted` array contains `"step-10-closure.md"`:**

"The incident handling workflow for {{engagement_name}} has been completed.

The final report is available at `{outputFile}` with all sections completed.

**Incident Summary:**
- Incident ID: {{incident_id}}
- Severity: {{incident_severity}}
- Category: {{incident_category}}
- Status: {{incident_status}}
- Detection source: {{detection_source}}
- Dwell time: {{dwell_time}}
- Root cause: {{root_cause}}

**Response Metrics:**
- Affected systems: {{affected_systems}}
- Affected users: {{affected_users}}
- IOCs identified: {{iocs_identified}}
- Evidence items collected: {{evidence_items}}
- Evidence chain intact: {{evidence_chain_intact}}
- Persistence mechanisms found: {{persistence_mechanisms}}
- Lateral movement detected: {{lateral_movement_detected}}
- Data exfiltration detected: {{data_exfiltration_detected}}

**Containment & Recovery:**
- Containment status: {{containment_status}}
- Eradication status: {{eradication_status}}
- Recovery status: {{recovery_status}}

**Post-Incident:**
- Lessons learned documented: {{lessons_learned}}
- Detection improvements proposed: {{detection_improvements}}
- Stakeholder notifications sent: {{stakeholder_notifications}}
- Regulatory notifications sent: {{regulatory_notifications}}

Would you like me to:
- Review the incident handling report in detail
- Suggest the next workflow (Digital Forensics via `spectra-digital-forensics` for deeper analysis, or Threat Intel via `spectra-threat-intel` for campaign correlation)
- Launch a War Room session to discuss Blue vs Red findings and detection improvements
- Generate a Purple Team feedback loop based on the incident findings
- Export the IOC summary for integration into detection infrastructure

How would you like to proceed?"

### 5. Present Current Progress

**If workflow not complete:**

"Welcome back {{user_name}}. Resuming incident handling for {{engagement_name}}.

**Engagement:** {{engagement_id}} — Still active
**Remaining period:** until {{end_date}}

**Incident Context:**
- Incident ID: {{incident_id}}
- Severity: {{incident_severity}}
- Category: {{incident_category}}
- Status: {{incident_status}}
- Detection source: {{detection_source}}
- Total incident duration: {{calculated from detection_timestamp}}
- Session gap: {{calculated elapsed time since last session}}

**Current Progress:**
- Last step completed: {{last step filename from stepsCompleted array}}
- Next step: {{next step from lookup table}} (NIST Phase: {{phase name}})
- SOC triage loaded: {{soc_triage_loaded}}
- SOC alert ID: {{soc_alert_id or 'N/A — cold start'}}

**Containment & Eradication Status:**
- Containment: {{containment_status}} (strategy: {{containment_strategy or 'not yet selected'}})
- Eradication: {{eradication_status}}
- Recovery: {{recovery_status}}

**Scope & Impact:**
- Affected systems: {{affected_systems}} | Users: {{affected_users}}
- IOCs identified: {{iocs_identified}} | Enriched: {{iocs_enriched}}
- Evidence items: {{evidence_items}} | Chain intact: {{evidence_chain_intact}}
- MITRE techniques: {{mitre_techniques or 'not yet mapped'}}
- Lateral movement: {{lateral_movement_detected}}
- Data exfiltration: {{data_exfiltration_detected}}
- Persistence mechanisms: {{persistence_mechanisms}}

**Workstream Status:**
- Forensics: {{forensics_launched or 'not launched'}}
- Malware analysis: {{malware_analysis_launched or 'not launched'}}
- Threat intelligence: {{threat_intel_launched or 'not launched'}}

**Communication:**
- Stakeholder notifications: {{stakeholder_notifications}}
- Regulatory notifications: {{regulatory_notifications}}

**Completed report sections:**
{{list of completed sections based on stepsCompleted}}

{{IF session gap exceeds threshold for current severity:}}
**TIME GAP ALERT:** {{session gap duration}} have elapsed since the last session. For a {{incident_severity}} severity incident, this exceeds the recommended maximum session gap. Verify that:
1. Containment actions are still holding
2. No new IOCs or alerts have been generated during the gap
3. Stakeholders have been kept informed during the gap
{{END IF}}

Everything correct? Would you like to make adjustments before continuing?"

### 6. Present MENU OPTIONS

Display: "**Select an option:** [C] Continue to {{next step name}}"

#### Menu Handling Logic:

- IF C: Read fully and follow the next step determined from the lookup table in step 3
- IF Any other comments or queries: respond and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [current state confirmed and engagement re-verified], will you then read fully and follow the next step (from the lookup table) to resume the workflow.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Engagement re-verified as still active with valid dates and incident response still authorized
- All previous workflow state accurately analyzed and presented with incident-specific metrics
- Incident severity, containment status, and evidence chain integrity correctly reported
- Time-critical calculations performed (incident duration, session gap, time-to-contain)
- Session gap alerts raised when thresholds are exceeded for the incident severity level
- Correct next step identified from the lookup table with NIST 800-61 phase context
- User confirms understanding of progress before continuation
- No containment, eradication, or recovery actions taken during continuation setup

### SYSTEM FAILURE:

- Not re-verifying engagement authorization before continuing
- Continuing work on an expired or deactivated engagement
- Continuing when incident response authorization has been revoked from the engagement scope
- Modifying content from already completed steps
- Failing to determine the next step from the lookup table
- Proceeding without user confirmation of current state
- Beginning containment, eradication, or recovery actions during continuation setup
- Failing to calculate or report incident duration and session gap
- Not flagging session gap threshold violations for the incident severity level
- Not verifying evidence chain integrity status on resumption
- Not reporting containment status — a failed or bypassed containment is an escalation trigger
- Modifying evidence chain records during continuation setup
- Presenting outdated severity classification without checking for reclassification indicators

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Incident response operates under time pressure — accurate resumption is critical. Evidence integrity is non-negotiable. No incident response operations on expired engagements.
