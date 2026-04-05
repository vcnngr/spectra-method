# Step 3: Engagement Completion

**Progress: Step 3 of 3** — Final Step

## STEP GOAL:

Finalize the engagement by writing the final engagement.yaml with all validated parameters, creating the engagement directory structure, presenting a comprehensive engagement summary, and recommending next operational steps.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input for final confirmation
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A FACILITATOR finalizing a security engagement — precision is mandatory
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a security engagement coordinator completing the operational setup
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ The engagement.yaml produced here propagates to ALL agents — accuracy is critical
- ✅ Recommended next steps should be tailored to the engagement type

### Step-Specific Rules:

- 🎯 Focus on finalization, directory creation, and next-step recommendations
- 🚫 FORBIDDEN to begin any testing or execution activities
- 💬 Approach: Final verification, structured output, clear next steps
- 💾 The engagement.yaml must be complete, correct, and ready for agent consumption

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers)
- ⚠️ WARN with explanation if you identify risk:
  - Engagement parameters that may cause operational issues downstream
  - Directory structures that conflict with existing data
  - Recommended next steps that may not be appropriate for the engagement type
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk

## EXECUTION PROTOCOLS:

- 🎯 Present final engagement summary before writing
- 💾 Write final engagement.yaml with all validated parameters
- 📖 Create engagement directory structure
- Update frontmatter: add this step name to the end of the steps completed array
- 🚫 FORBIDDEN to close without user confirmation

## CONTEXT BOUNDARIES:

- Available context: Complete engagement.yaml with validated scope from Steps 1-2
- Focus: Finalization, directory creation, recommendations only
- Limits: Don't begin testing, reconnaissance, or any execution
- Dependencies: All parameters validated in Step 2

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Validated Engagement Data

Read the engagement.yaml with all parameters from Steps 1-2:

- Verify all required fields are populated
- Verify scope validation status (all items should be `✅ VALIDATED` or explicitly acknowledged)
- Verify authorization coverage is complete

### 2. Write Final engagement.yaml

Write the definitive engagement.yaml to `{engagement_artifacts}/{{engagement_id}}/engagement.yaml`:

- Set `engagement.status: "planning"` (will change to "active" when testing begins)
- Include all collected and validated parameters
- Include scope validation metadata
- Timestamp the creation: `created_at: {{date}}`

### 3. Create Engagement Directory Structure

Create the operational directory structure:

```
{engagement_artifacts}/{{engagement_id}}/
├── engagement.yaml          # Engagement configuration (already created)
├── reconnaissance/          # Recon findings and OSINT data
├── exploitation/            # Exploit artifacts, PoCs, payloads
├── evidence/                # Screenshots, logs, recordings
│   ├── chain-of-custody/    # Evidence custody tracking
│   └── raw/                 # Unprocessed evidence files
├── findings/                # Individual finding write-ups
├── reports/                 # Generated reports
│   ├── technical/           # Technical report artifacts
│   └── executive/           # Executive summary artifacts
├── debrief/                 # Post-engagement debrief artifacts
└── logs/                    # Engagement operational logs
```

Confirm directory creation to user.

### 4. Present Final Engagement Summary

"✅ **Engagement {{engagement_id}} — Final Summary**

**General Information:**
| Field | Value |
|-------|-------|
| ID | {{engagement_id}} |
| Type | {{engagement_type}} |
| Status | Planning |
| Client | {{client_name}} |
| Authorized by | {{authorized_by}} |
| Period | {{start_date}} → {{end_date}} |

**Validated Scope:**
- In-scope: {{in_scope_count}} validated items
- Out-of-scope: {{out_scope_count}} defined exclusions
- Critical systems excluded: {{critical_exclusions_count}}

**Rules of Engagement:**
- Hours: {{testing_hours}}
- Social engineering: {{social_eng}}
- DoS: {{dos_allowed}}
- Exfiltration: {{exfil_allowed}}
- Maximum impact: {{max_impact}}

**Deconfliction:**
- Primary contact: {{primary_contact}} ({{primary_phone}})
- Stop procedure: {{emergency_stop}}

**Directory structure created:** `{engagement_artifacts}/{{engagement_id}}/`

**Configuration file:** `{engagement_artifacts}/{{engagement_id}}/engagement.yaml`"

### 5. Generate Engagement-Specific Recommendations

Based on engagement type, recommend the optimal next steps:

**For Pentest:**
"**Recommended next steps:**
1. 👻 **Ghost** (`spectra-external-recon`) — Start external reconnaissance
2. ⚔️ **Blade** (`spectra-agent-blade`) — For an initial quick assessment
3. 🐍 **Viper** (`spectra-agent-red-lead`) — To plan the attack strategy"

**For Red Team:**
"**Recommended next steps:**
1. 🐍 **Viper** (`spectra-agent-red-lead`) — Campaign planning
2. 👻 **Ghost** (`spectra-external-recon`) — Reconnaissance and target package
3. 🪞 **Mirage** (`spectra-agent-social-eng`) — If social engineering is allowed"

**For Purple Team:**
"**Recommended next steps:**
1. ⚔️ **War Room** (`spectra-war-room`) — Adversarial Red vs Blue session for the plan
2. 🐍 **Viper** + 🎖️ **Commander** — Simultaneous Red/Blue coordination
3. 🛡️ **Sentinel** (`spectra-agent-detection-eng`) — Detection baseline preparation"

**For Incident Response:**
"**Recommended next steps:**
1. 📡 **Dispatch** (`spectra-agent-handler`) — Incident response coordination
2. ⚡ **Surge** (`spectra-agent-surge`) — Rapid triage if urgent
3. 🔬 **Trace** (`spectra-agent-forensics`) — Evidence acquisition"

**For Compliance Audit:**
"**Recommended next steps:**
1. 📋 **Auditor** (`spectra-agent-compliance`) — Start compliance audit
2. ⚖️ **Arbiter** (`spectra-agent-risk`) — Preliminary risk assessment
3. 📝 **Scribe** (`spectra-agent-policy`) — Review existing policies"

**For CTF / Training / Assessment:**
"**Recommended next steps:**
1. 👁️ **Specter** (`spectra-agent-specter`) — Rapid assessment and coordination
2. ⚔️ **War Room** (`spectra-war-room`) — Collaborative discussion on the plan
3. Specific skills based on the exercise objectives"

### 6. Present Final Confirmation

"Engagement **{{engagement_id}}** has been created successfully and the operational structure is ready.

**All SPECTRA agents can now operate within the context of this engagement.**

Would you like to start one of the recommended next steps, or do you need to modify anything?"

### 7. Complete Workflow Exit

**Frontmatter Update:**

```yaml
---
stepsCompleted: [step-01-init, step-02-scope-validation, step-03-complete]
engagement_id: '{{engagement_id}}'
engagement_type: '{{engagement_type}}'
status: 'planning'
workflow_completed: true
---
```

**State:**

- Mark engagement creation workflow as completed
- Engagement is now available to all SPECTRA agents via `{engagement_artifacts}/{{engagement_id}}/engagement.yaml`

---

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [final engagement.yaml written] AND [directory structure created] AND [engagement summary presented] AND [next steps recommended] AND [frontmatter updated with workflow_completed: true] is this workflow complete.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Final engagement.yaml complete with all validated parameters
- Engagement directory structure fully created
- Comprehensive engagement summary presented
- Engagement-specific next step recommendations generated
- Kill chain status initialized as "pending" for all phases
- Detection coverage initialized at 0 for all ATT&CK tactics
- File paths and engagement ID clearly communicated to user
- Workflow frontmatter properly updated
- All output in `{communication_language}`

### ❌ SYSTEM FAILURE:

- engagement.yaml missing required fields
- Directory structure incomplete or not created
- Generic next steps not tailored to engagement type
- Not presenting engagement summary before closing
- Not marking workflow as completed
- Beginning any testing or execution activities
- Not speaking in `{communication_language}`

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
