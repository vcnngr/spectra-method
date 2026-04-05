# Step 1B: Workflow Resumption

## STEP GOAL:

Resume the threat hunt workflow from where it was left off, ensuring smooth continuation with full context restoration including engagement scope, hunt mission, hypothesis state, data collection progress, analysis findings, and all prior hunting output.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A THREAT HUNTER resuming authorized work
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Threat Hunter conducting proactive, hypothesis-driven hunting within an active security engagement
- ✅ Resume workflow from exact point where it was interrupted
- ✅ Re-verify that the engagement is still active and dates are still valid
- ✅ All prior findings and hunting state remain valid unless scope has changed
- ✅ Hunt time sensitivity is generally lower than alert triage, but data retention limits may be a factor — if the lookback window has shifted since the last session, flag this to the operator

### Step-Specific Rules:

- 💬 FOCUS on understanding where we left off and continuing appropriately
- 🚫 FORBIDDEN to modify content completed in previous steps
- 📖 Reload engagement.yaml to re-verify authorization
- 🔒 If engagement has expired since last session: HARD STOP
- 🔒 If scope has been amended since last session: flag changes to operator
- ⏰ If significant time has passed, assess data retention impact on remaining hunt activities

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Resuming a workflow on an expired or deactivated engagement invalidates all prior authorization — re-verification is essential before any hunting activity continues
  - Resuming a hunt after a significant time gap may mean data retention windows have shifted — logs that were available when the hunt started may have been rotated out. Check retention against the original lookback window and flag any data loss before continuing.
  - Skipping to a future step without verifying document state consistency may lead to unreliable findings based on corrupted or incomplete state — verify that previous step outputs are intact before proceeding
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking action
- Update frontmatter: add this step name to the end of the stepsCompleted array
- 📖 Reload engagement.yaml and verify it is still active
- 🚫 FORBIDDEN to begin new hunting activities during continuation setup

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
No hunting activity may continue.
Contact the engagement lead for renewal."

**HARD STOP — Do not proceed.**

### 2. Analyze Current State

**State Assessment:**

Review the frontmatter to understand:

- `stepsCompleted`: Array of completed step filenames (last element = most recently completed)
- `engagement_id`, `engagement_name`: Engagement context
- `hunt_id`, `hunt_name`, `hunt_type`: Hunt identity and classification
- `hypothesis`: Primary hypothesis (if step 2+)
- `mitre_techniques_targeted`: ATT&CK techniques being hunted (if step 2+)
- `mitre_tactics_targeted`: ATT&CK tactics being hunted (if step 2+)
- `data_sources_queried`: Data sources used (if step 3+)
- `data_volume_analyzed`: Volume processed (if step 4+)
- `queries_executed`: Query count (if step 4+)
- `hypotheses_tested`, `hypotheses_confirmed`, `hypotheses_refuted`, `hypotheses_inconclusive`: Hypothesis metrics (if step 6+)
- `findings_total`, `findings_confirmed_malicious`, `findings_suspicious`, `findings_benign`: Finding metrics (if step 6+)
- `false_positives_identified`: FP count (if step 6+)
- `detection_rules_created`: Rules created (if step 7+)
- `detection_gaps_identified`: Gaps found (if step 7+)
- `hunt_playbooks_created`: Playbooks created (if step 7+)
- `purple_team_items`: PT feedback items (if step 7+)
- `attack_surface_reduction_items`: ASR items (if step 7+)
- `hunt_start_time`: When the hunt began
- `hunt_maturity_level`: Maturity assessment (if step 8)

**Time Gap Assessment:**

- Calculate time elapsed since `hunt_start_time`
- Assess data retention impact:

"**NOTICE — Time gap assessment.**

The hunt was started at {{hunt_start_time}} ({{elapsed_time}} ago).

**Data retention impact:**
| Data Source | Original Retention | Data Still Available? | Impact |
|-------------|-------------------|---------------------|--------|
| {{source}} | {{days}} | ✅ / ⚠️ / ❌ | {{impact on remaining queries}} |
| ... | ... | ... | ... |

{{If any data has rotated out:}}
**WARNING:** Some data sources may have rotated logs since the hunt began. The original lookback window of {{lookback}} may be partially unavailable. Remaining hunt activities should account for this:
- If in steps 1-3 (pre-execution): Adjust the lookback window in the execution plan
- If in steps 4-5 (execution): Verify previously executed queries are not affected; re-run if needed for the current data window
- If in steps 6-8 (post-execution): All analysis was performed on available data — results remain valid for the period analyzed

{{If no data has rotated:}}
Data retention is sufficient — all original data sources remain available for the lookback window."

### 3. Determine Next Step

**Step Sequence Lookup:**

Use the following ordered sequence to determine the next step from the last completed step:

| Last Completed | Next Step |
|---|---|
| step-01-init.md | step-02-hypothesis.md |
| step-02-hypothesis.md | step-03-data-collection.md |
| step-03-data-collection.md | step-04-automated-analysis.md |
| step-04-automated-analysis.md | step-05-manual-analysis.md |
| step-05-manual-analysis.md | step-06-findings.md |
| step-06-findings.md | step-07-detection-engineering.md |
| step-07-detection-engineering.md | step-08-reporting.md |

1. Get the last element from the `stepsCompleted` array
2. Look it up in the table above to find the next step
3. That's the next step to load!

**Example:**
- If `stepsCompleted = ["step-01-init.md", "step-02-hypothesis.md", "step-03-data-collection.md"]`
- Last element is `"step-03-data-collection.md"`
- Table lookup → next step is `./step-04-automated-analysis.md`

### 4. Handle Workflow Completion

**If `stepsCompleted` array contains `"step-08-reporting.md"`:**

"The threat hunt workflow for {{hunt_id}} ("{{hunt_name}}") in engagement {{engagement_name}} has already been completed.

The final hunt report is available at `{outputFile}` with all sections completed.

**Final Results:**
- Hunt ID: {{hunt_id}} | Type: {{hunt_type}}
- Trigger: {{hunt trigger summary}}
- Hypotheses: {{hypotheses_tested}} tested — {{hypotheses_confirmed}} confirmed, {{hypotheses_refuted}} refuted, {{hypotheses_inconclusive}} inconclusive
- Findings: {{findings_total}} total — {{findings_confirmed_malicious}} malicious, {{findings_suspicious}} suspicious, {{findings_benign}} benign, {{false_positives_identified}} FP
- ATT&CK techniques confirmed: {{count from mitre_techniques_targeted}}
- Detection rules created: {{detection_rules_created}}
- Detection gaps identified: {{detection_gaps_identified}}
- Hunt playbooks created: {{hunt_playbooks_created}}
- Purple Team items: {{purple_team_items}}
- Attack surface reduction items: {{attack_surface_reduction_items}}
- Hunt maturity level: {{hunt_maturity_level}}

Would you like me to:
- Review the hunt report with you
- Suggest the next workflow (new hunt via `spectra-threat-hunt`, detection lifecycle via `spectra-detection-lifecycle`, or incident handling via `spectra-incident-handling` if malicious findings require response)
- Launch a War Room session to discuss Red vs Blue implications of the hunt findings
- Begin a new hunt within the same engagement

How would you like to proceed?"

### 5. Present Current Progress

**If workflow not complete:**

"Welcome back {{user_name}}! Resuming the threat hunt workflow for {{engagement_name}}.

**Engagement:** {{engagement_id}} — Still active ✅
**Remaining period:** until {{end_date}}

**Hunt Under Execution:**
- Hunt ID: {{hunt_id}} | Name: {{hunt_name}}
- Type: {{hunt_type}}
- Started: {{hunt_start_time}} ({{elapsed_time}} ago)
- Target: {{brief scope summary}}

**Current Progress:**
- Last step completed: {{last step filename from stepsCompleted array}}
- Next step: {{next step from lookup table}}

**Hunt Metrics So Far:**
- Hypotheses developed: {{hypotheses_tested or 'Not yet'}}
- Data sources queried: {{data_sources_queried count or 'Not yet'}}
- Queries executed: {{queries_executed or 'Not yet'}}
- Data volume analyzed: {{data_volume_analyzed or 'Not yet'}}
- Findings total: {{findings_total or 'Not yet'}}
- Confirmed malicious: {{findings_confirmed_malicious or 'Not yet'}}
- Detection rules created: {{detection_rules_created or 'Not yet'}}

**Completed report sections:**
{{list of completed sections based on stepsCompleted}}

**Data retention status:** {{summary — all sources available / some sources have rotated / data gap detected}}

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
- All previous workflow state accurately analyzed and presented with hunt-specific metrics
- Time gap assessed with data retention impact analysis per data source
- Correct next step identified from the lookup table
- Data retention warnings provided if lookback window has been affected
- User confirms understanding of progress before continuation
- Already-completed workflow detected and handled gracefully with results summary

### SYSTEM FAILURE:

- Not re-verifying engagement authorization before continuing
- Continuing work on an expired or deactivated engagement
- Continuing when SOC operations authorization has been revoked from the engagement
- Modifying content from already completed steps
- Failing to determine the next step from the lookup table
- Not assessing data retention impact of time gaps on the hunt
- Proceeding without user confirmation of current state
- Beginning hunting activities during continuation setup
- Not flagging scope changes since last session

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No hunting operations on expired engagements. Data retention impacts must be assessed before resuming.
