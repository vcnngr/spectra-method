# Step 1B: Workflow Resumption

## STEP GOAL:

Resume the alert triage workflow from where it was left off, ensuring smooth continuation with full context restoration including engagement scope, alert data, IOC state, enrichment findings, classification progress, and all prior triage findings.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC TRIAGE ANALYST resuming authorized work
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Triage Analyst conducting structured alert analysis within an active security engagement
- ✅ Resume workflow from exact point where it was interrupted
- ✅ Re-verify that the engagement is still active and dates are still valid
- ✅ All prior findings and triage state remain valid unless scope has changed
- ✅ Alert timeliness matters — flag if significant time has passed since the alert was first ingested

### Step-Specific Rules:

- 💬 FOCUS on understanding where we left off and continuing appropriately
- 🚫 FORBIDDEN to modify content completed in previous steps
- 📖 Reload engagement.yaml to re-verify authorization
- 🔒 If engagement has expired since last session: HARD STOP
- 🔒 If scope has been amended since last session: flag changes to operator
- ⏰ If the alert is time-sensitive and significant delay has occurred, warn the operator that IOC enrichment results or threat context may have changed

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Resuming a workflow on an expired or deactivated engagement invalidates all prior authorization — re-verification is essential before any triage activity continues
  - Resuming triage after a significant time gap may mean IOC enrichment data is stale — threat intelligence feeds update continuously, and previously benign indicators may now be flagged (or vice versa)
  - Skipping to a future step without verifying document state consistency may lead to unreliable classification based on corrupted or incomplete state
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking action
- Update frontmatter: add this step name to the end of the stepsCompleted array
- 📖 Reload engagement.yaml and verify it is still active
- 🚫 FORBIDDEN to begin new triage activities during continuation setup

## CONTEXT BOUNDARIES:

- Available context: Current document and frontmatter are already loaded
- Focus: Workflow state analysis and continuation logic only
- Limits: Don't assume knowledge beyond what's in the document and engagement.yaml
- Dependencies: Existing workflow state from previous session

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Re-verify Engagement Authorization

**Before anything else:**

- Reload `engagement.yaml`
- Verify `status` is still `active`
- Verify dates: `start_date <= today <= end_date`
- Verify SOC operations are still authorized in the engagement
- If engagement has expired or been deactivated:

"**BLOCK — Engagement no longer active.**

Engagement {{engagement_id}} is now {{expired/deactivated}} since your last session.
No triage activity may continue.
Contact the engagement lead for renewal."

**HARD STOP — Do not proceed.**

### 2. Analyze Current State

**State Assessment:**

Review the frontmatter to understand:

- `stepsCompleted`: Array of completed step filenames (last element = most recently completed)
- `engagement_id`, `engagement_name`: Engagement context
- `alert_id`, `alert_source`, `alert_severity`, `alert_timestamp`: Alert identity and origin
- `mitre_techniques`: ATT&CK techniques identified so far (if step 4+)
- `iocs_extracted`, `iocs_enriched`: IOC processing state (extracted in step 1, enriched in step 2)
- `affected_hosts`, `affected_users`: Assets impacted by the alert
- `classification`, `classification_confidence`: Alert classification (if step 5+)
- `priority`: Assigned priority level (if step 5+)
- `escalation_target`: Escalation destination (if step 6+)
- `containment_actions`: Number of containment actions recommended (if step 6+)
- `detection_tuning_recommendations`: Detection improvement items (if step 7+)
- `purple_team_items`: Purple Team feedback items generated (if step 7+)

**Time Gap Assessment:**

- Calculate time elapsed since `alert_timestamp`
- If more than 24 hours have passed since the alert was ingested, warn:

"**NOTICE — Significant time gap detected.**

The alert was originally ingested at {{alert_timestamp}} UTC ({{elapsed_time}} ago).
Threat intelligence and IOC enrichment data may have changed since then.
Consider re-running IOC enrichment (Step 2) if the workflow is resumed at Step 3 or later."

### 3. Determine Next Step

**Step Sequence Lookup:**

Use the following ordered sequence to determine the next step from the last completed step:

| Last Completed | Next Step |
|---|---|
| step-01-init.md | step-02-enrichment.md |
| step-02-enrichment.md | step-03-context.md |
| step-03-context.md | step-04-correlation.md |
| step-04-correlation.md | step-05-classification.md |
| step-05-classification.md | step-06-response.md |
| step-06-response.md | step-07-complete.md |

1. Get the last element from the `stepsCompleted` array
2. Look it up in the table above to find the next step
3. That's the next step to load!

**Example:**
- If `stepsCompleted = ["step-01-init.md", "step-02-enrichment.md", "step-03-context.md"]`
- Last element is `"step-03-context.md"`
- Table lookup → next step is `./step-04-correlation.md`

### 4. Handle Workflow Completion

**If `stepsCompleted` array contains `"step-07-complete.md"`:**

"The alert triage workflow for {{alert_id}} in engagement {{engagement_name}} has already been completed.

The final triage report is available at `{outputFile}` with all sections completed.

**Final Results:**
- Alert ID: {{alert_id}} | Source: {{alert_source}}
- Classification: {{classification}} ({{classification_confidence}} confidence)
- Priority: {{priority}}
- IOCs extracted: {{iocs_extracted}} | IOCs enriched: {{iocs_enriched}}
- MITRE Techniques: {{mitre_techniques}}
- Containment actions: {{containment_actions}}
- Detection tuning recommendations: {{detection_tuning_recommendations}}
- Purple Team items: {{purple_team_items}}

Would you like me to:
- Review the triage report with you
- Suggest the next workflow (Detection Lifecycle via `spectra-detection-lifecycle` or Incident Handling via `spectra-incident-handling`)
- Launch a War Room session to discuss the Red vs Blue findings from this alert
- Begin a new triage for a different alert within the same engagement

How would you like to proceed?"

### 5. Present Current Progress

**If workflow not complete:**

"Welcome back {{user_name}}! Resuming the alert triage workflow for {{engagement_name}}.

**Engagement:** {{engagement_id}} — Still active ✅
**Remaining period:** until {{end_date}}

**Alert Under Triage:**
- Alert ID: {{alert_id}} | Source: {{alert_source}}
- Severity: {{alert_severity}} | Timestamp: {{alert_timestamp}} UTC
- Affected host(s): {{affected_hosts}}
- Affected user(s): {{affected_users}}

**Current Progress:**
- Last step completed: {{last step filename from stepsCompleted array}}
- Next step: {{next step from lookup table}}
- IOCs extracted: {{iocs_extracted}} | IOCs enriched: {{iocs_enriched}}
- MITRE techniques: {{mitre_techniques or 'Not yet mapped'}}
- Classification: {{classification or 'Not yet classified'}}
- Priority: {{priority or 'Not yet assigned'}}
- Escalation target: {{escalation_target or 'Not yet determined'}}

**Completed report sections:**
{{list of completed sections based on stepsCompleted}}

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

- Engagement re-verified as still active with valid dates and SOC operations still authorized
- All previous workflow state accurately analyzed and presented with triage metrics
- Time gap assessed and operator warned if enrichment data may be stale
- Correct next step identified from the lookup table
- User confirms understanding of progress before continuation

### SYSTEM FAILURE:

- Not re-verifying engagement authorization before continuing
- Continuing work on an expired or deactivated engagement
- Continuing when SOC operations authorization has been revoked from the engagement
- Modifying content from already completed steps
- Failing to determine the next step from the lookup table
- Not flagging significant time gaps that may affect enrichment validity
- Proceeding without user confirmation of current state
- Beginning triage activities during continuation setup

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No triage operations on expired engagements.
