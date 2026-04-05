# Step 1B: Workflow Resumption

## STEP GOAL:

Resume the threat intelligence production workflow from where it was left off, ensuring smooth continuation with full context restoration including engagement scope, intelligence trigger, PIR status, collection progress, analysis findings, IOC state, and all prior intelligence production findings.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER generate content without user input
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST resuming authorized intelligence production
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst resuming structured intelligence production within an active engagement
- Resume workflow from exact point where it was interrupted
- Re-verify that the engagement is still active and dates are still valid
- All prior findings and intelligence state remain valid unless scope has changed or intelligence has become stale
- Intelligence currency matters — assess whether time gap has degraded intelligence validity

### Step-Specific Rules:

- FOCUS on understanding where we left off and continuing appropriately
- FORBIDDEN to modify content completed in previous steps
- Reload engagement.yaml to re-verify authorization
- If engagement has expired since last session: HARD STOP
- If scope has been amended since last session: flag changes to operator
- If significant time has passed, assess intelligence currency — IOCs decay, campaigns evolve, threat actors adapt

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Resuming a workflow on an expired or deactivated engagement invalidates all prior authorization — re-verification is essential before any intelligence production continues
  - Resuming intelligence production after a significant time gap (>48 hours) may mean IOCs have decayed, campaigns have evolved, or threat actors have changed infrastructure — indicators have a half-life, and stale IOCs in a finished product undermine consumer trust and may generate false positives if operationalized
  - Skipping to a future step without verifying document state consistency may produce intelligence with gaps in the analytic chain — the consumer cannot assess confidence if intermediate analysis steps are missing or corrupted
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Show your analysis of current state before taking action
- Update frontmatter: add this step name to the end of the stepsCompleted array
- Reload engagement.yaml and verify it is still active
- FORBIDDEN to begin new intelligence production activities during continuation setup

## CONTEXT BOUNDARIES:

- Available context: Current document and frontmatter are already loaded
- Focus: Workflow state analysis, intelligence currency assessment, and continuation logic only
- Limits: Don't assume knowledge beyond what's in the document and engagement.yaml
- Dependencies: Existing workflow state from previous session

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Re-verify Engagement Authorization

**Before anything else:**

- Reload `engagement.yaml`
- Verify `status` is still `active`
- Verify dates: `start_date <= today <= end_date`
- Verify intelligence operations are still authorized in the engagement
- If engagement has expired or been deactivated:

"**BLOCK — Engagement no longer active.**

Engagement {{engagement_id}} is now {{expired/deactivated}} since your last session.
No intelligence production activity may continue.
Contact the engagement lead for renewal."

**HARD STOP — Do not proceed.**

### 2. Analyze Current State

**State Assessment:**

Review the frontmatter to understand:

- `stepsCompleted`: Array of completed step filenames (last element = most recently completed)
- `engagement_id`, `engagement_name`: Engagement context
- `intel_id`, `intel_name`: Intelligence product identity
- `intel_type`: Intelligence classification (tactical/operational/strategic)
- `trigger_source`, `trigger_type`: What initiated this intelligence production
- `priority_intelligence_requirements`: PIRs defined
- `standing_intelligence_requirements`: Active SIRs
- `collection_sources`: Planned collection sources
- `collection_gaps`: Known gaps in collection
- `source_count`, `raw_data_items`, `processed_items`: Collection progress
- `threat_actors_identified`, `threat_actor_count`: Actor identification state
- `attribution_confidence`: Current attribution confidence
- `diamond_model_completed`: Whether Diamond Model analysis is done
- `diamond_events`, `activity_threads`, `pivot_findings`: Diamond Model metrics
- `kill_chain_mapped`: Whether Kill Chain mapping is done
- `kill_chain_phases_covered`: Kill Chain coverage
- `mitre_techniques`, `mitre_technique_count`: ATT&CK mapping state
- `campaigns_identified`, `campaign_count`: Campaign identification state
- `ach_hypotheses_evaluated`, `ach_leading_hypothesis`: Assessment state
- `assessment_confidence`: Overall assessment confidence
- `iocs_total`, `iocs_by_type`: IOC inventory
- `stix_bundle_created`: Whether STIX packaging is done
- `sigma_rules_created`, `yara_rules_created`, `suricata_rules_created`: Detection content state
- `tlp_classification`: TLP marking
- `dissemination_targets`, `dissemination_count`: Dissemination state
- `products_tactical`, `products_operational`, `products_strategic`: Finished product count

**Intelligence Currency Assessment:**

Calculate time elapsed since the intelligence trigger and last workflow activity:

- Determine when the intelligence trigger was first recorded
- Determine when the last step was completed (estimate from document modification time or context)
- Calculate the time gap

**Currency Assessment Matrix:**

| Time Gap | IOC Currency | Campaign Currency | Actor Currency | Recommended Action |
|----------|--------------|-------------------|----------------|--------------------|
| < 24 hours | Current | Current | Current | Continue normally |
| 24-48 hours | Likely current | Current | Current | Continue, note time gap |
| 48-72 hours | May be stale | Likely current | Current | Re-validate active IOCs in step 2 |
| 3-7 days | Probably stale | May have evolved | Current | Re-run collection for active IOCs, check for campaign updates |
| 7-14 days | Stale | May have evolved | Likely current | Significant re-collection needed, campaigns may have shifted |
| > 14 days | Expired | Likely evolved | May have changed | Consider restarting from step 2 with fresh collection |

**If time gap > 48 hours:**

"**NOTICE — Intelligence currency assessment required.**

The intelligence production was last active approximately {{elapsed_time}} ago.

**Currency Impact Assessment:**

| Intelligence Element | Status | Risk |
|---------------------|--------|------|
| IOCs (IPs, domains) | {{current/stale/expired}} | {{IOC infrastructure has a median lifespan of ~30 days; adversaries rotate}} |
| Campaign activity | {{current/may have evolved}} | {{campaigns adapt in response to detection and public reporting}} |
| Threat actor TTPs | {{current/likely current}} | {{TTPs evolve slowly but major shifts occur after public exposure}} |
| Detection rules | {{still valid/may need update}} | {{if IOCs are stale, detection rules based on them need refresh}} |
| Advisory context | {{current/may have updates}} | {{check for updated advisories, new CVEs, vendor patches since last session}} |

**Recommended actions:**
- {{specific actions based on the time gap and what steps have been completed}}

Proceed with continuation, or would you like to adjust the approach?"

### 3. Determine Next Step

**Step Sequence Lookup:**

Use the following ordered sequence to determine the next step from the last completed step:

| Last Completed | Next Step | Next Step Title |
|---|---|---|
| step-01-init.md | step-02-collection.md | Intelligence Collection & Processing |
| step-02-collection.md | step-03-threat-actor.md | Threat Actor Profiling |
| step-03-threat-actor.md | step-04-diamond-model.md | Diamond Model Analysis |
| step-04-diamond-model.md | step-05-kill-chain.md | Kill Chain & ATT&CK Mapping |
| step-05-kill-chain.md | step-06-assessment.md | Intelligence Assessment & Analytic Products |
| step-06-assessment.md | step-07-ioc-packaging.md | IOC Packaging & Detection Content |
| step-07-ioc-packaging.md | step-08-dissemination.md | Dissemination & Reporting |

1. Get the last element from the `stepsCompleted` array
2. Look it up in the table above to find the next step
3. That's the next step to load

**Example:**
- If `stepsCompleted = ["step-01-init.md", "step-02-collection.md", "step-03-threat-actor.md"]`
- Last element is `"step-03-threat-actor.md"`
- Table lookup: next step is `./step-04-diamond-model.md`

### 4. Handle Workflow Completion

**If `stepsCompleted` array contains `"step-08-dissemination.md"`:**

"The threat intelligence production workflow for {{intel_id}} in engagement {{engagement_name}} has already been completed.

The final intelligence report is available at `{outputFile}` with all sections completed.

**Final Intelligence Product Summary:**
- **Intel ID:** {{intel_id}} | **Type:** {{intel_type}}
- **Trigger:** {{trigger_type}} — {{trigger_source}}
- **PIRs Defined:** {{priority_intelligence_requirements count}} | **PIRs Answered:** {{pirs_answered}} | **Unanswered:** {{pirs_unanswered}}
- **Sources Consulted:** {{source_count}}
- **Threat Actors Identified:** {{threat_actor_count}} | Attribution: {{attribution_confidence}} confidence
- **Diamond Events:** {{diamond_events}} | Activity Threads: {{activity_threads}}
- **ATT&CK Techniques:** {{mitre_technique_count}} mapped
- **Campaigns Identified:** {{campaign_count}}
- **Assessment Confidence:** {{assessment_confidence}}
- **IOCs Total:** {{iocs_total}} ({{iocs_active}} active, {{iocs_historical}} historical)
- **STIX Bundle:** {{stix_bundle_created}} ({{stix_objects}} objects)
- **Detection Content:** Sigma: {{sigma_rules_created}} | YARA: {{yara_rules_created}} | Suricata: {{suricata_rules_created}} | SIEM: {{siem_queries_created}}
- **TLP:** {{tlp_classification}}
- **Dissemination:** {{dissemination_count}} products to {{dissemination_targets count}} targets
- **Intelligence Gaps:** {{intelligence_gaps count}} remaining

Would you like me to:
- Review the intelligence report with you
- Discuss the intelligence gaps and what additional collection could fill them
- Launch a War Room session to stress-test the findings
- Begin a new intelligence production for a different requirement within the same engagement
- Route products to downstream workflows: SOC (spectra-alert-triage), IR (spectra-incident-handling), Hunt (spectra-threat-hunt), Detection (spectra-detection-lifecycle), Forensics (spectra-digital-forensics), Malware Analysis (spectra-malware-analysis)

How would you like to proceed?"

### 5. Present Current Progress

**If workflow not complete:**

"Welcome back {{user_name}}. Resuming the threat intelligence production workflow for {{engagement_name}}.

**Engagement:** {{engagement_id}} — Still active
**Remaining period:** until {{end_date}}

**Intelligence Product Under Production:**
- **Intel ID:** {{intel_id}} | **Type:** {{intel_type}}
- **Trigger:** {{trigger_type}} — {{trigger_source}}
- **TLP:** {{tlp_classification}}

**Priority Intelligence Requirements:**
| # | PIR | Status |
|---|-----|--------|
| PIR-1 | {{pir_text}} | {{Answered / In Progress / Not Started}} |
| PIR-2 | {{pir_text}} | {{Answered / In Progress / Not Started}} |
| ... | ... | ... |

**Intelligence Production Progress:**
- Last step completed: {{last step filename from stepsCompleted array}}
- Next step: {{next step from lookup table}} ({{next step title}})
- Sources consulted: {{source_count}}
- Raw data items: {{raw_data_items}} | Processed: {{processed_items}}
- Threat actors identified: {{threat_actor_count}} (attribution: {{attribution_confidence}})
- Diamond Model: {{diamond_model_completed}} | Events: {{diamond_events}}
- Kill Chain mapped: {{kill_chain_mapped}} | ATT&CK techniques: {{mitre_technique_count}}
- Campaigns: {{campaign_count}}
- Assessment confidence: {{assessment_confidence or 'Not yet assessed'}}
- IOCs total: {{iocs_total}} | Detection rules: {{sigma_rules_created + yara_rules_created + suricata_rules_created + siem_queries_created}}

**Completed report sections:**
{{list of completed sections based on stepsCompleted}}

**Intelligence Currency:** {{assessment from step 2}}

Everything correct? Would you like to make adjustments before continuing?"

### 6. Present MENU OPTIONS

Display: "**Select an option:** [C] Continue to {{next step name}} ({{next step title}})"

#### Menu Handling Logic:

- IF C: Read fully and follow the next step determined from the lookup table in step 3
- IF Any other comments or queries: respond and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [current state confirmed, engagement re-verified, and intelligence currency assessed], will you then read fully and follow the next step (from the lookup table) to resume the workflow.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Engagement re-verified as still active with valid dates and intelligence operations still authorized
- All previous workflow state accurately analyzed and presented with intelligence production metrics
- Intelligence currency assessed based on time gap with specific impact per intelligence element
- Recommended actions provided for stale intelligence elements
- PIR status presented (answered, in progress, not started)
- Correct next step identified from the lookup table
- User confirms understanding of progress before continuation

### SYSTEM FAILURE:

- Not re-verifying engagement authorization before continuing
- Continuing work on an expired or deactivated engagement
- Continuing when intelligence operations authorization has been revoked from the engagement
- Not assessing intelligence currency when significant time has passed — stale IOCs in a finished product are worse than no IOCs
- Modifying content from already completed steps
- Failing to determine the next step from the lookup table
- Not presenting PIR status so the operator can assess what questions remain unanswered
- Proceeding without user confirmation of current state
- Beginning intelligence production activities during continuation setup

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No intelligence operations on expired engagements. Intelligence has a shelf life — always assess currency before resuming production.
