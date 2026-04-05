# Resume: Privilege Escalation Workflow Continuation

## STEP GOAL:

Resume the privilege escalation workflow from where it was left off, ensuring smooth continuation with full context restoration including engagement scope, foothold data, escalation progress, technique state, and all prior operational findings.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A PRIVILEGE ESCALATION SPECIALIST resuming authorized work
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom --- Attack Operator + Post-Exploitation Specialist
- ✅ Resume workflow from exact point where it was interrupted
- ✅ Re-verify that the engagement is still active and dates are still valid
- ✅ All prior findings and operational state remain valid unless scope has changed

### Step-Specific Rules:

- 💬 FOCUS on understanding where we left off and continuing appropriately
- 🚫 FORBIDDEN to modify content completed in previous steps
- 📖 Reload engagement.yaml to re-verify authorization
- 🔒 If engagement has expired since last session: HARD STOP
- 🔒 If RoE has been amended since last session: flag changes to operator

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL --- your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK --- Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Resuming a workflow on an expired or deactivated engagement invalidates all prior authorization --- re-verification is essential
  - Skipping engagement re-verification and jumping straight to operations risks operating under changed conditions since the previous session
  - Skipping to a future step without verifying document state consistency may lead to unreliable operations based on corrupted or incomplete state
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk --- give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking action
- Update frontmatter: add this step name to the end of the stepsCompleted array
- 📖 Reload engagement.yaml and verify it is still active
- 🚫 FORBIDDEN to begin new escalation activities during continuation setup

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
- Verify privilege escalation is still authorized in RoE
- If engagement has expired or been deactivated:

"**BLOCK --- Engagement no longer active.**

Engagement {{engagement_id}} is now {{expired/deactivated}} since your last session.
No escalation activity may continue.
Contact the engagement lead for renewal."

**HARD STOP --- Do not proceed.**

### 2. Analyze Current State

**State Assessment:**

Review the frontmatter to understand:

- `stepsCompleted`: Array of completed step filenames (last element = most recently completed)
- `engagement_id`, `engagement_name`: Engagement context
- `initial_access_report`: Whether initial-access data was available
- `current_privilege_level`: Privilege level at workflow start
- `highest_privilege_achieved`: Highest privilege obtained so far
- `os_environment`: Target operating system
- `ad_environment`: Whether Active Directory is in play
- `cloud_environment`: Whether cloud escalation applies
- `escalation_paths_identified`: Number of escalation vectors discovered
- `escalation_paths_successful`: Number of successful escalations
- `techniques_attempted`: Total techniques tried
- `techniques_successful`: Total techniques that succeeded
- `detection_events`: Number of times escalation activity was detected

### 3. Determine Next Step

**Step Sequence Lookup:**

Use the following ordered sequence to determine the next step from the last completed step:

| Last Completed | Next Step |
|---|---|
| step-01-init.md | step-02-local-enum.md |
| step-02-local-enum.md | step-03-credential-discovery.md |
| step-03-credential-discovery.md | step-04-windows-privesc.md |
| step-04-windows-privesc.md | step-05-linux-privesc.md |
| step-05-linux-privesc.md | step-06-ad-escalation.md |
| step-06-ad-escalation.md | step-07-cloud-escalation.md |
| step-07-cloud-escalation.md | step-08-exploit-chaining.md |
| step-08-exploit-chaining.md | step-09-verification.md |
| step-09-verification.md | step-10-reporting.md |

1. Get the last element from the `stepsCompleted` array
2. Look it up in the table above to find the next step
3. That's the next step to load!

**Example:**
- If `stepsCompleted = ["step-01-init.md", "step-02-local-enum.md", "step-03-credential-discovery.md"]`
- Last element is `"step-03-credential-discovery.md"`
- Table lookup -> next step is `./step-04-windows-privesc.md`

### 4. Handle Workflow Completion

**If `stepsCompleted` array contains `"step-10-reporting.md"`:**

"Great news! The privilege escalation workflow for {{engagement_name}} has already been completed.

The final report is available at `{outputFile}` with all sections completed.

**Final Results:**
- Escalation paths identified: {{escalation_paths_identified}}
- Escalation paths successful: {{escalation_paths_successful}}
- Techniques attempted: {{techniques_attempted}}
- Techniques successful: {{techniques_successful}}
- Highest privilege achieved: {{highest_privilege_achieved}}
- Detection events: {{detection_events}}

Would you like me to:
- Review the privilege escalation report with you
- Suggest the next workflow (Lateral Movement via `spectra-lateral-movement` or Persistence via `spectra-persistence`)
- Launch a War Room session to discuss the Red vs Blue findings
- Begin a new escalation cycle for different targets within the same engagement

How would you like to proceed?"

### 5. Present Current Progress

**If workflow not complete:**

"Welcome back {{user_name}}! Resuming the privilege escalation workflow for {{engagement_name}}.

**Engagement:** {{engagement_id}} --- Still active ✅
**Remaining period:** until {{end_date}}

**Current Progress:**
- Last step completed: {{last step filename from stepsCompleted array}}
- Next step: {{next step from lookup table}}
- Initial access data: {{loaded / not available}}
- Current privilege level: {{current_privilege_level}}
- Highest privilege achieved: {{highest_privilege_achieved}}
- Escalation paths identified: {{escalation_paths_identified}} | Successful: {{escalation_paths_successful}}
- Techniques attempted: {{techniques_attempted}} | Successful: {{techniques_successful}}
- Detection events: {{detection_events}}

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

- Engagement re-verified as still active with valid dates and privilege escalation still authorized
- All previous workflow state accurately analyzed and presented with operational metrics
- Correct next step identified from the lookup table
- User confirms understanding of progress before continuation

### SYSTEM FAILURE:

- Not re-verifying engagement authorization before continuing
- Continuing work on an expired or deactivated engagement
- Continuing when privilege escalation authorization has been revoked from RoE
- Modifying content from already completed steps
- Failing to determine the next step from the lookup table
- Proceeding without user confirmation of current state
- Beginning escalation activities during continuation setup

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No escalation operations on expired engagements.
