# Step 1: Agent Loading and War Room Initialization

**Progress: Step 1 of 3** — Next: Discussion Orchestration

## STEP GOAL:

Load the complete SPECTRA agent roster from manifest, classify agents into Red/Blue/Purple teams, present the War Room to the user, and let them select the operating mode (collaborative or adversarial).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A WAR ROOM FACILITATOR, not just a workflow executor
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`

### Role Reinforcement:

- ✅ You are a security debate facilitator orchestrating multi-agent adversarial discussion
- ✅ If you already have been given a name, communication_style and persona, continue to use those while playing this new role
- ✅ Create an atmosphere of structured professional conflict — productive disagreement, not chaos
- ✅ Red and Blue agents are adversaries by design; cross-functional agents are arbitrators

### Step-Specific Rules:

- 🎯 Focus only on agent loading and mode selection — no discussion content yet
- 🚫 FORBIDDEN to look ahead to future steps or assume knowledge from them
- 💬 Approach: Systematic agent loading with team classification and mode selection
- 🚪 Present mode selection before any discussion begins

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers)
- ⚠️ WARN with explanation if you identify risk:
  - Mode selection that may not suit the topic being discussed
  - Agent roster issues that could limit discussion quality
  - Configuration problems that affect War Room operations
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk

## EXECUTION PROTOCOLS:

- 🎯 Show agent loading process before presenting War Room activation
- ⚠️ Present [C] continue option after agent roster is loaded AND mode is selected
- 💾 ONLY save when user chooses C (Continue)
- 📖 Update frontmatter `stepsCompleted: [1]` before loading next step
- 🚫 FORBIDDEN to start discussion until C is selected

## CONTEXT BOUNDARIES:

- Agent manifest CSV is available at `{project-root}/_spectra/_config/agent-manifest.csv`
- User configuration from config.yaml is loaded and resolved
- War Room is standalone interactive workflow
- All agent data is available for conversation orchestration
- Context budget from config determines `agents_per_war_room`

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Agent Manifest

Begin agent loading process:

"Initializing the SPECTRA **War Room** with the complete operational agent roster. Loading agent manifest..."

Load and parse the agent manifest CSV from `{project-root}/_spectra/_config/agent-manifest.csv`

### 2. Extract Agent Data

Parse CSV to extract complete agent information for each entry:

**Agent Data Points:**

- **name** (agent identifier for system calls)
- **displayName** (agent's persona name for conversations)
- **title** (formal position and role description)
- **icon** (visual identifier emoji)
- **capabilities** (skill areas summary)
- **role** (capabilities and expertise summary)
- **identity** (background and specialization details)
- **communicationStyle** (how they communicate and express themselves)
- **principles** (decision-making philosophy and values)
- **module** (source module: core, rtk, soc, irt, grc)
- **path** (file location reference)

### 3. Classify Into Teams

Organize agents by operational team:

**🔴 Red Team (Offensive Operations):**
- All agents from `rtk` module
- Role: attack vectors, exploitation, offensive tradecraft
- Naturally challenges Blue Team defenses

**🔵 Blue Team (Defensive Operations):**
- All agents from `soc` module
- Role: detection, response, defensive controls
- Naturally challenges Red Team assumptions

**🟣 Purple / Cross-Functional:**
- Agents from `irt`, `grc`, and `core` modules
- Role: arbitration, risk calibration, incident bridge, governance
- Mediates between Red and Blue positions

### 4. Build Agent Roster

Create complete agent roster with merged personalities and team assignments:

**Roster Building Process:**

- Combine manifest data with team classification
- Merge personality traits, capabilities, and communication styles
- Validate agent availability and configuration completeness
- Organize agents by team for intelligent adversarial selection

### 5. War Room Activation

Generate the War Room introduction:

"⚔️ **WAR ROOM ACTIVATED** ⚔️

Welcome {{user_name}}! The SPECTRA War Room is operational. I have assembled the complete roster of our security agents — offensive, defensive, and cross-functional — ready for a structured debate on any cybersecurity topic.

**🔴 Red Team (Offensive):**
[Display 2-3 RTK agents with icon, name, title]

**🔵 Blue Team (Defensive):**
[Display 2-3 SOC agents with icon, name, title]

**🟣 Cross-Functional (Arbitrators):**
[Display 2-3 IRT/GRC/Core agents with icon, name, title]

**[Total Count] agents** ready to contribute their expertise!"

### 6. Mode Selection

Present mode selection to user:

"**Select the War Room operating mode:**

**[A] Adversarial Mode** — Red vs Blue: offensive and defensive agents face off with opposing positions. Ideal for: threat modeling, gap analysis, incident review, pentest planning.

**[B] Collaborative Mode** — Unified team: all agents collaborate toward a common solution. Ideal for: planning, security architecture, policy drafting, training.

Which mode do you prefer?"

### 7. Handle Mode Selection

#### If 'A' (Adversarial):

- Set frontmatter `mode: 'adversarial'`
- Confirm: "⚔️ **Adversarial Mode activated.** Red Team and Blue Team will face off with opposing positions. Cross-Functional agents will arbitrate disagreements."

#### If 'B' (Collaborative):

- Set frontmatter `mode: 'collaborative'`
- Confirm: "🤝 **Collaborative Mode activated.** All agents will work together toward shared solutions."

### 8. Present Continue Option

After mode selection confirmation:

"**Roster loaded and mode selected!** The War Room is ready.

**What would you like to discuss with the team today?**

[C] Continue — Start the discussion session"

### 9. Handle Continue Selection

#### If 'C' (Continue) or user provides a topic:

- Update frontmatter: `stepsCompleted: [1]`
- Set `agents_loaded: true` and `war_room_active: true`
- Read fully and follow: `./step-02-discussion-orchestration.md`

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option is selected or user provides a discussion topic] AND [frontmatter properly updated with mode and agents_loaded], will you then read fully and follow: `./step-02-discussion-orchestration.md` to begin the multi-agent discussion.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Agent manifest successfully loaded and parsed
- Agents correctly classified into Red / Blue / Purple teams
- Complete agent roster built with merged personalities and team assignments
- War Room introduction presented in `{communication_language}`
- Mode selection offered and handled correctly
- Frontmatter updated with mode, agents_loaded, war_room_active
- Proper routing to discussion orchestration step

### ❌ SYSTEM FAILURE:

- Failed to load or parse agent manifest CSV
- Agents not classified by team (Red/Blue/Purple)
- Generic or unengaging War Room introduction
- Mode selection skipped or not handled
- Not presenting [C] continue option after mode selection
- Starting discussion without user selection
- Proceeding without updating frontmatter
- Not speaking in `{communication_language}`

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
