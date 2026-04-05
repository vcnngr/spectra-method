# Step 1: Engagement Initialization

**Progress: Step 1 of 3** — Next: Scope Validation

## STEP GOAL:

Initialize a new security engagement by collecting engagement type, client authorization, scope, rules of engagement, and deconfliction contacts. Generate a unique engagement ID and create the engagement.yaml from template.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a security engagement facilitator ensuring complete operational coverage
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Every engagement parameter must be explicitly confirmed by the user — never assume
- ✅ Authorization and scope are CRITICAL — incomplete information here causes operational risk

### Step-Specific Rules:

- 🎯 Focus only on engagement initialization — no testing or execution content yet
- 🚫 FORBIDDEN to look ahead to future steps or assume knowledge from them
- 💬 Approach: Systematic elicitation of engagement parameters with clear confirmation
- 🚪 Every question must be answered before proceeding — no optional fields in this step
- ⚖️ Rules of engagement MUST be explicit — ambiguity creates legal and operational risk

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers)
- ⚠️ WARN with explanation if you identify risk:
  - Scope definitions that are dangerously broad or ambiguous
  - Authorization gaps that could create legal exposure
  - Rules of engagement that conflict with scope or engagement type
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk

## EXECUTION PROTOCOLS:

- 🎯 Show collected information summary before finalizing
- 💾 Initialize engagement.yaml structure and update frontmatter appropriately
- Update frontmatter: add this step name to the end of the steps completed array
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md are available in memory
- Focus: Engagement initialization and parameter collection only
- Limits: Don't assume knowledge from other steps or begin scope validation yet
- Dependencies: Configuration loaded from workflow.md initialization
- Template: `{project-root}/_spectra/core/engagement/engagement-template.yaml`

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Check for Existing Engagement State

First, check if an engagement document already exists:

**Engagement State Detection:**

- Look for any existing `engagement.yaml` files in `{engagement_artifacts}/`
- If user specified an engagement ID, check for that specific engagement
- If active engagements exist, inform the user and ask if they want to create a new one or resume an existing one

### 2. Engagement Type Selection

Ask the user to select the engagement type:

"Welcome {{user_name}}! Let's start creating a new security engagement.

**Select the engagement type:**

| # | Type | Description |
|---|------|-------------|
| 1 | **Pentest** | Standard penetration test — vulnerability discovery and exploitation |
| 2 | **Red Team** | Advanced attack simulation with specific objectives |
| 3 | **Purple Team** | Collaborative Red + Blue exercise with real-time feedback |
| 4 | **CTF** | Capture The Flag — controlled competition environment |
| 5 | **Training** | Training session with security scenarios |
| 6 | **Assessment** | Security assessment without active exploitation |
| 7 | **Incident Response** | Response to an ongoing security incident |
| 8 | **Compliance Audit** | Regulatory or framework compliance audit |

Which engagement type do you want to create?"

**Wait for user input.**

### 3. Client and Authorization

After engagement type is confirmed, collect authorization details:

"**Client information and authorization:**

1. **Client name:** Who is the engagement sponsor?
2. **Authorized by:** Name and title of the person who authorized the test (e.g., 'John Smith, CISO')
3. **Authorization document:** Path or reference to the signed authorization document (SOW, contract, authorization letter)
4. **Start date:** Planned start date (ISO-8601 format: YYYY-MM-DD)
5. **End date:** Planned end date
6. **Timezone:** Reference timezone (e.g., Europe/Rome)"

**Wait for user input. Collect all fields before proceeding.**

### 4. Scope Definition — In Scope

Collect in-scope items:

"**Scope definition — IN SCOPE elements:**

Specify all elements that fall within the testing perimeter:

1. **Networks:** Subnets and IP ranges (e.g., `10.0.0.0/24`, `192.168.1.0/24`)
2. **Domains:** Domains and subdomains (e.g., `example.com`, `*.example.com`)
3. **Applications:** Application URLs or identifiers (e.g., `https://app.example.com`)
4. **Cloud accounts:** Cloud accounts in scope (e.g., `AWS:123456789012`)
5. **Users:** Test user accounts (e.g., `test-user-1`)
6. **Notes:** Additional scope information

For each category, list elements separated by comma. If a category is not applicable, indicate so."

**Wait for user input.**

### 5. Scope Definition — Out of Scope and Critical Exclusions

Collect out-of-scope items:

"**Scope definition — OUT OF SCOPE elements and critical exclusions:**

⚠️ **WARNING: Exclusions are just as important as scope. Elements not explicitly excluded may be considered testable.**

1. **Excluded networks:** Subnets and IP ranges NOT to test
2. **Excluded domains:** Domains and subdomains NOT to test
3. **Excluded applications:** Applications NOT to test
4. **Critical systems:** Systems that must NOT be touched under any circumstances (e.g., `DC01`, `SCADA-controller`, critical production systems)
5. **Excluded users:** User accounts NOT to use or impersonate (e.g., `CEO`, `board-members`)
6. **Notes:** Specific exclusions or particular constraints"

**Wait for user input.**

### 6. Rules of Engagement

Collect rules of engagement:

"**Rules of Engagement:**

Define the operational parameters of the engagement:

| # | Parameter | Options | Default |
|---|-----------|---------|---------|
| 1 | **Testing hours** | any / business-hours / after-hours / custom | any |
| 2 | **Notify before exploit** | yes / no | no |
| 3 | **Notify on critical finding** | yes / no | yes |
| 4 | **Social engineering allowed** | yes / no | no |
| 5 | **Physical access allowed** | yes / no | no |
| 6 | **DoS testing allowed** | yes / no | no |
| 7 | **Data exfiltration allowed** | yes / no (proof of access only) | no |
| 8 | **Production systems** | yes / no | no |
| 9 | **Maximum impact level** | low / medium / high / critical | high |

Confirm or modify each parameter. If hours are 'custom', specify the time window."

**Wait for user input.**

### 7. Deconfliction Contacts

Collect deconfliction information:

"**Deconfliction Contacts:**

🛑 **CRITICAL: Without deconfliction contacts, an engagement cannot proceed safely.**

1. **Primary contact:** Name
2. **Primary phone:** Direct number
3. **Primary email:** Email address
4. **Secondary contact:** Name (backup)
5. **Secondary phone:** Direct number
6. **Emergency stop procedure:** How to immediately halt all testing (e.g., 'Call number X and say codeword Y')
7. **Deconfliction channel:** Dedicated communication channel (e.g., `Slack #red-team-deconflict`)"

**Wait for user input.**

### 8. Generate Engagement ID

Generate a unique engagement ID in the format `ENG-YYYY-NNN`:

- `YYYY` = current year
- `NNN` = sequential number, zero-padded (check existing engagements in `{engagement_artifacts}/` to determine next number)

Example: `ENG-2026-001`, `ENG-2026-002`

### 9. Create Engagement File

- Copy the template from `{project-root}/_spectra/core/engagement/engagement-template.yaml`
- Fill in all collected parameters
- Create directory: `{engagement_artifacts}/{engagement_id}/`
- Write to: `{engagement_artifacts}/{engagement_id}/engagement.yaml`

### 10. Present Initialization Summary

"**Engagement Summary — {{engagement_id}}**

| Field | Value |
|-------|-------|
| **ID** | {{engagement_id}} |
| **Type** | {{engagement_type}} |
| **Client** | {{client_name}} |
| **Authorized by** | {{authorized_by}} |
| **Period** | {{start_date}} → {{end_date}} |
| **Scope in** | {{in_scope_summary}} |
| **Scope out** | {{out_scope_summary}} |
| **Social eng.** | {{social_eng}} |
| **DoS** | {{dos_allowed}} |
| **Max impact** | {{max_impact}} |
| **Deconfliction** | {{primary_contact}} / {{secondary_contact}} |

File created: `{engagement_artifacts}/{{engagement_id}}/engagement.yaml`"

### 11. Present Menu Options

Display menu after initialization summary:

"[A] Advanced Elicitation — Deepen the parameters with advanced elicitation techniques
[W] War Room — Discuss scope and rules with the agent team
[C] Continue — Save and proceed to Scope Validation (Step 2 of 3)"

#### Menu Handling Logic:

- IF A: Invoke `spectra-advanced-elicitation` skill, then return to this menu
- IF W: Invoke `spectra-war-room` skill, then return to this menu
- IF C: Update output file frontmatter, adding this step name to the end of the list of stepsCompleted, then read fully and follow: `./step-02-scope-validation.md`
- IF user asks questions: Answer and redisplay menu
- IF user wants to modify a field: Accept modification, update engagement.yaml, redisplay summary and menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected AND [engagement.yaml properly created with all collected parameters] AND [frontmatter properly updated with this step added to stepsCompleted], will you then read fully and follow: `./step-02-scope-validation.md` to begin scope validation.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Engagement type selected and confirmed
- Client authorization details complete (client, authorized_by, document, dates, timezone)
- In-scope items explicitly defined across all applicable categories
- Out-of-scope items and critical exclusions explicitly defined
- Rules of engagement confirmed parameter by parameter
- Deconfliction contacts complete with emergency stop procedure
- Unique engagement ID generated in ENG-YYYY-NNN format
- engagement.yaml created from template with all parameters filled
- Engagement directory created at `{engagement_artifacts}/{engagement_id}/`
- Initialization summary presented clearly
- Menu presented and user input handled correctly
- All output in `{communication_language}`

### ❌ SYSTEM FAILURE:

- Proceeding with incomplete authorization (missing authorized_by or dates)
- Scope left ambiguous or undefined
- Rules of engagement not explicitly confirmed
- Missing deconfliction contacts or emergency stop procedure
- Engagement ID not following ENG-YYYY-NNN format
- engagement.yaml not created or missing fields
- Proceeding without user selecting 'C'
- Assuming values for any field without user confirmation
- Not speaking in `{communication_language}`

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
