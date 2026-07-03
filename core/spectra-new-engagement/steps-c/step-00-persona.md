# Step 0: Persona Selection

**Progress: Step 0 of 3** — Next: Engagement Initialization

## STEP GOAL:

Make the SPECTRA team discoverable before scope is defined. Determine the engagement type, present the recommended lead persona, a quick single-agent alternative, the supporting cast, and the workflows that team typically runs — all drawn from the agent roster — then let the operator choose who leads. This turns "28 agents somewhere in the framework" into an obvious, guided starting point.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Step-Specific Rules:

- 🎯 Focus only on persona orientation and engagement-type selection — no scope, no authorization, no testing content yet
- 🚫 FORBIDDEN to look ahead to future steps or assume knowledge from them
- 🧭 The persona catalog and recommendation are produced by the deterministic helper — do NOT invent personas, roles, or workflow names; present exactly what the helper returns
- 🙋 The operator may decline persona selection and continue with the current facilitator — that is always allowed

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 💡 If the operator's stated intent does not match the engagement type they pick, say so and PROPOSE the better-fitting type — then COMPLY with their choice

## EXECUTION PROTOCOLS:

- 🧰 Use the deterministic persona helper for all roster and recommendation data
- 🎯 Record the chosen engagement type and lead persona so Step 1 does not ask again
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md are available in memory
- Focus: Persona orientation and engagement-type capture only
- Helper: `{project-root}/_spectra/core/execution/engagement-personas.py`

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Determine the engagement type

Ask the operator what kind of engagement this is, presenting the supported types:

`pentest`, `red-team`, `purple-team`, `ctf`, `training`, `assessment`, `incident-response`, `compliance-audit`

If the operator describes intent in their own words instead of naming a type, map it to the closest supported type and confirm before proceeding.

**STOP and WAIT for the engagement type.**

### 2. Produce the team recommendation

Run the helper to get the recommended team for the chosen type:

```bash
python3 {project-root}/_spectra/core/execution/engagement-personas.py recommend --type {engagement_type}
```

Present the result to the operator as:

- **Lead persona** — `lead.displayName` (`lead.role`) — leads this engagement
- **Quick solo alternative** — `solo.displayName` (`solo.role`) — for a fast single-agent run
- **Supporting cast** — each of `support[]` as `displayName` (`role`)
- **Typical workflows** — `workflows[]`

Optionally, to show the full roster grouped by module:

```bash
python3 {project-root}/_spectra/core/execution/engagement-personas.py list
```

### 3. Let the operator choose who leads

Present a menu:

```
[L] Lead with {lead.displayName} (recommended)
[S] Solo / quick run with {solo.displayName}
[O] Other — choose any persona from the roster (show with the `list` helper)
[F] Continue with the current facilitator (no persona switch)
[C] Continue to engagement initialization
```

- A lead choice MUST be made before continuing. If the operator selects **C** without first choosing L/S/O/F, treat it as **F** (continue with the current facilitator) and state that explicitly — never proceed with an empty/unset lead.
- For **O (Other)**, run the `list` helper and ask the operator to provide the canonical agent name (e.g. `spectra-agent-l3-hunter`) from that output.
- If the operator picks **L**, **S**, or **O**, adopt that agent for the remainder of the engagement by its canonical name — load its persona from the agent's SKILL.md (the `path` field returned by the helper) and continue in that agent's name, identity, and communication style.
- If the operator picks **F** (or defaults to it via C), keep the current facilitator identity.
- Record `{engagement_type}` and the resolved lead persona in memory for Step 1.

**STOP and WAIT. Only proceed to the next step when the operator selects 'C' (with a lead resolved per the rule above).**

### 4. Continue

When the operator selects 'C', read fully and follow: `./step-01-init.md`

Carry the chosen `{engagement_type}` and lead persona forward so Step 1 confirms rather than re-asks them.

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Engagement type determined and confirmed with the operator
- Team recommendation produced by the deterministic helper and presented faithfully
- Lead persona chosen (lead, solo, other, or facilitator) and recorded for Step 1
- Engagement type carried forward so Step 1 confirms rather than re-asks
- Menu presented and user input handled correctly
- All output in `{communication_language}`

### ❌ SYSTEM FAILURE:

- Inventing personas, roles, or workflow names instead of using the helper output
- Proceeding without the operator confirming an engagement type
- Switching persona without operator selection
- Proceeding to Step 1 without the user selecting 'C'
- Not speaking in `{communication_language}`

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
