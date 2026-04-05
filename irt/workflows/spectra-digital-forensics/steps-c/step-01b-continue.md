# Step 1B: Workflow Resumption

## STEP GOAL:

Resume the digital forensics workflow from where it was left off, ensuring smooth continuation with full context restoration including engagement scope, case data, evidence inventory, chain of custody status, analysis progress, findings, and all prior forensic work. Re-verify engagement authorization and evidence integrity before resuming.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST resuming authorized work
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst resuming a structured forensic examination within an active security engagement
- ✅ Resume workflow from the exact point where it was interrupted
- ✅ Re-verify that the engagement is still active and dates are still valid
- ✅ Re-verify evidence integrity — hash working copies to confirm they have not been modified during the interruption
- ✅ All prior findings and forensic state remain valid unless evidence integrity has been compromised
- ✅ Time gaps in forensic investigations have specific concerns: evidence retention, legal deadlines, evidence degradation

### Step-Specific Rules:

- 💬 FOCUS on understanding where we left off and continuing appropriately
- 🚫 FORBIDDEN to modify content completed in previous steps
- 📖 Reload engagement.yaml to re-verify authorization
- 🔒 If engagement has expired since last session: HARD STOP
- 🔒 If evidence integrity cannot be verified: WARN and assess impact
- ⏰ If significant time has passed, warn about evidence retention, legal deadlines, and potential evidence degradation

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Resuming a workflow on an expired or deactivated engagement invalidates all prior authorization — re-verification is essential before any forensic activity continues, as forensic work without authorization has no legal standing and may itself constitute unauthorized access to evidence
  - Resuming analysis after a significant time gap without re-verifying evidence integrity means you cannot guarantee that working copies have not been modified during the interruption — if hash verification fails upon resume, the analysis performed on that working copy after the gap may be unreliable
  - Time gaps in forensic investigations with pending regulatory notifications may have caused notification deadline violations — GDPR requires DPA notification within 72 hours of breach awareness, and a workflow pause during that window may have exceeded the deadline
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking action
- Update frontmatter: add this step name to the end of the stepsCompleted array
- 📖 Reload engagement.yaml and verify it is still active
- 🔐 Re-verify evidence integrity by checking working copy hashes
- 🚫 FORBIDDEN to begin new forensic activities during continuation setup

## CONTEXT BOUNDARIES:

- Available context: Current document and frontmatter are already loaded
- Focus: Workflow state analysis, engagement re-verification, evidence integrity re-verification, and continuation logic only
- Limits: Don't assume knowledge beyond what's in the document and engagement.yaml
- Dependencies: Existing workflow state from previous session

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Re-verify Engagement Authorization

**Before anything else:**

- Reload `engagement.yaml`
- Verify `status` is still `active`
- Verify dates: `start_date <= today <= end_date`
- Verify forensic investigation operations are still authorized in the engagement
- If engagement has expired or been deactivated:

"**BLOCK — Engagement no longer active.**

Engagement {{engagement_id}} is now {{expired/deactivated}} since your last session.
No forensic activity may continue.
Contact the engagement lead for renewal.

**Evidence Status:** All evidence items remain in `{irt_evidence_chain}/{case_id}/` with chain of custody intact as of last session. Evidence preservation continues regardless of engagement status."

**HARD STOP — Do not proceed.**

### 2. Analyze Current State

**State Assessment:**

Review the frontmatter to understand:

- `stepsCompleted`: Array of completed step filenames (last element = most recently completed)
- `engagement_id`, `engagement_name`: Engagement context
- `case_id`, `case_name`, `case_classification`: Case identity
- `legal_context`, `legal_hold_status`: Legal framework
- `forensic_question`: The question driving the investigation
- `evidence_items`: List of EVD IDs
- `evidence_item_count`: Total evidence items
- `chain_of_custody_entries`: CoC entry count
- `integrity_verified`: Whether all hashes verified at last check
- `evidence_types`: Which evidence types are present (disk, memory, network, cloud, mobile)
- `analysis_types`: Which analysis phases have been completed
- `timeline_entries`: Timeline event count (if step 7+)
- `artifacts_recovered`: Artifacts found during analysis
- `iocs_extracted`: IOC count
- `mitre_techniques`: ATT&CK techniques identified
- `findings_count`, `findings_by_severity`: Findings status (if step 8+)
- `expert_opinion_rendered`: Whether expert opinion is complete (if step 9+)
- `root_cause`, `attack_vector`, `dwell_time`: Key investigation findings
- `case_status`: Current case status

### 3. Evidence Integrity Re-Verification

**CRITICAL — Re-verify evidence integrity before resuming analysis.**

For each evidence working copy:
1. Read the expected hash from the evidence manifest / chain of custody records
2. Compute the current hash of the working copy
3. Compare: expected hash == current hash

```
| EVD ID | Evidence Type | Expected Hash (SHA-256) | Current Hash (SHA-256) | Match | Status |
|--------|---------------|------------------------|------------------------|-------|--------|
| EVD-{case_id}-XXX | {{type}} | {{expected_hash}} | {{current_hash}} | ✅/❌ | Verified/ALERT |
```

**If ALL hashes match:** Evidence integrity is confirmed. Analysis can safely resume.

**If ANY hash mismatch:** 

"**EVIDENCE INTEGRITY ALERT**

Working copy hash mismatch detected for:
- EVD-{{case_id}}-{{NNN}}: Expected {{expected_hash}}, computed {{current_hash}}

Possible explanations:
1. Working copy was accidentally modified during the interruption
2. Storage media error or corruption
3. Unauthorized access to evidence storage

**Impact Assessment:** Analysis findings from previous steps that relied on this evidence item may need to be re-evaluated.

**Recommended Actions:**
1. Create a new working copy from the master evidence (verify master hash first)
2. Re-run analysis on the new working copy for affected steps
3. Document the integrity break in the chain of custody

Proceed with new working copy, or halt for investigation?"

### 4. Time Gap Assessment

**Calculate time elapsed since last workflow activity:**

- Determine the timestamp of the last step completion (from document content or file modification time)
- Calculate elapsed time

**Forensic-Specific Time Gap Concerns:**

```
| Concern | Threshold | Current Status | Action Required |
|---------|-----------|----------------|-----------------|
| Evidence retention | Cloud logs may have rotated if > 30 days | {{elapsed}} since last activity | {{Check cloud log availability}} |
| Legal deadlines | GDPR 72h, PCI 72h, SEC 4 business days | {{elapsed}} since case intake | {{Check notification compliance}} |
| Memory dump freshness | Memory represents system state at capture time only | N/A (static evidence) | None |
| Live evidence | Any live system evidence may have changed | {{elapsed}} since acquisition | {{Re-acquire if systems are still running}} |
| Threat actor activity | Attacker may have continued operations during gap | {{elapsed}} since containment | {{Verify containment still holds}} |
| Witness availability | Witness memory degrades over time | {{elapsed}} since case intake | {{Schedule interviews if needed}} |
```

**If more than 72 hours have elapsed:**

"**NOTICE — Significant time gap detected.**

The case was last active at {{last_activity_timestamp}} UTC ({{elapsed_time}} ago).

Forensic-specific concerns:
- **Regulatory notifications:** If breach notification deadlines apply (GDPR 72h, PCI 72h), verify compliance
- **Evidence retention:** Cloud logs with short retention may have rotated — check availability before relying on them
- **Containment status:** If this case is part of an active incident, verify containment is still holding
- **Threat actor activity:** If the threat actor was not contained, additional compromise may have occurred during the gap

Recommend addressing these concerns before resuming analysis."

### 5. Determine Next Step

**Step Sequence Lookup:**

Use the following ordered sequence to determine the next step from the last completed step:

| Last Completed | Next Step |
|---|---|
| step-01-init.md | step-02-acquisition.md |
| step-02-acquisition.md | step-03-disk-forensics.md |
| step-03-disk-forensics.md | step-04-memory-forensics.md |
| step-04-memory-forensics.md | step-05-network-forensics.md |
| step-05-network-forensics.md | step-06-cloud-forensics.md |
| step-06-cloud-forensics.md | step-07-timeline.md |
| step-07-timeline.md | step-08-findings.md |
| step-08-findings.md | step-09-expert-opinion.md |
| step-09-expert-opinion.md | step-10-reporting.md |

1. Get the last element from the `stepsCompleted` array
2. Look it up in the table above to find the next step
3. That's the next step to load!

**Example:**
- If `stepsCompleted = ["step-01-init.md", "step-02-acquisition.md", "step-03-disk-forensics.md"]`
- Last element is `"step-03-disk-forensics.md"`
- Table lookup → next step is `./step-04-memory-forensics.md`

### 6. Handle Workflow Completion

**If `stepsCompleted` array contains `"step-10-reporting.md"`:**

"The forensic investigation for case {{case_id}} in engagement {{engagement_name}} has already been completed.

The final forensic report is available at `{outputFile}` with all sections completed.

**Final Results:**
- Case ID: {{case_id}} | Classification: {{case_classification}}
- Forensic Question: {{forensic_question}}
- Evidence Items: {{evidence_item_count}} | Artifacts: {{artifacts_recovered}}
- Timeline Events: {{timeline_entries}} | Dwell Time: {{dwell_time}}
- Findings: {{findings_count}} ({{critical}} critical, {{high}} high)
- IOCs: {{iocs_extracted}} | ATT&CK Techniques: {{technique_count}}
- Root Cause: {{root_cause}}
- Expert Opinion: {{expert_opinion_confidence}} confidence
- Case Status: {{case_status}}
- Chain of Custody: {{integrity_status}}

Would you like me to:
- Review the forensic report with you
- Suggest the next workflow (Incident Handling via `spectra-incident-handling`, Detection Lifecycle via `spectra-detection-lifecycle`, or Malware Analysis via `spectra-malware-analysis`)
- Launch a War Room session to discuss the investigation findings
- Begin a new forensic investigation for a different case within the same engagement

How would you like to proceed?"

### 7. Present Current Progress

**If workflow not complete:**

"Welcome back {{user_name}}! Resuming the digital forensics workflow for {{engagement_name}}.

**Engagement:** {{engagement_id}} — Still active ✅
**Remaining period:** until {{end_date}}

**Case Under Investigation:**
- Case ID: {{case_id}} | Name: {{case_name}}
- Classification: {{case_classification}}
- Legal Context: {{legal_context}}
- Forensic Question: {{forensic_question}}

**Evidence Status:**
- Evidence items: {{evidence_item_count}}
- Evidence types: {{evidence_types_present}}
- Integrity: {{all_verified / issues_detected}}
- Chain of custody: {{intact / broken}}

**Current Progress:**
- Last step completed: {{last_step_name}}
- Next step: {{next_step_name}}
- Analysis completed: {{analysis_types_completed}}
- Analysis remaining: {{analysis_types_remaining}}

**Investigation Metrics (so far):**
- Artifacts recovered: {{artifacts_recovered}}
- IOCs extracted: {{iocs_extracted}}
- Timeline entries: {{timeline_entries or 'Not yet constructed'}}
- Findings: {{findings_count or 'Not yet consolidated'}}
- ATT&CK techniques: {{technique_count or 'Not yet mapped'}}
- Dwell time: {{dwell_time or 'Not yet calculated'}}
- Root cause: {{root_cause or 'Not yet determined'}}

**Time Gap:** {{elapsed_time}} since last session
**Time Gap Concerns:** {{concerns_if_any or 'None identified'}}

**Completed Report Sections:**
{{list of completed sections based on stepsCompleted}}

Everything correct? Would you like to make adjustments before continuing?"

### 8. Present MENU OPTIONS

Display: "**Select an option:** [C] Continue to {{next step name}}"

#### Menu Handling Logic:

- IF C: Read fully and follow the next step determined from the lookup table in step 5
- IF Any other comments or queries: respond and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [current state confirmed, engagement re-verified, and evidence integrity verified], will you then read fully and follow the next step (from the lookup table) to resume the workflow.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Engagement re-verified as still active with valid dates and forensic operations still authorized
- Evidence integrity re-verified by checking working copy hashes against expected values
- All previous workflow state accurately analyzed and presented with forensic metrics
- Time gap assessed with forensic-specific concerns (regulatory deadlines, evidence retention, containment status, threat actor activity)
- Correct next step identified from the lookup table
- Hash mismatches detected and flagged with remediation options
- User confirms understanding of progress before continuation
- Regulatory deadline compliance checked during time gap assessment

### ❌ SYSTEM FAILURE:

- Not re-verifying engagement authorization before continuing
- Continuing work on an expired or deactivated engagement
- Not re-verifying evidence integrity (working copy hashes) before resuming analysis
- Continuing analysis on working copies with failed hash verification
- Not assessing time gap implications for evidence retention and legal deadlines
- Modifying content from already completed steps
- Failing to determine the next step from the lookup table
- Not flagging significant time gaps and their forensic implications
- Proceeding without user confirmation of current state
- Beginning forensic activities during continuation setup

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No forensic operations on expired engagements. Evidence integrity must be re-verified before resuming analysis. Time gaps have forensic consequences that must be assessed.
