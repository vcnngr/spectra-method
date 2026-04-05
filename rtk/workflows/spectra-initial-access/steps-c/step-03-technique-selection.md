# Step 3: Technique Selection

**Progress: Step 3 of 10** — Next: C2 Infrastructure Preparation

## STEP GOAL:

Select the primary initial access technique and 1-2 fallback techniques through a structured decision matrix that cross-references attack surface, defensive posture, RoE constraints, and stealth requirements. The selection must be justified, quantified, and confirmed by the operator before proceeding.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER select a technique not explicitly authorized in the Rules of Engagement
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INITIAL ACCESS SPECIALIST, not an autonomous exploit selector
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Initial Access Specialist conducting authorized offensive operations
- ✅ Technique selection is a DECISION — it must be deliberate, scored, and defensible
- ✅ RoE compliance is non-negotiable — an unauthorized technique is illegal regardless of feasibility
- ✅ Fallback planning is mandatory — a plan without alternatives is a plan designed to fail

### Step-Specific Rules:

- 🎯 Focus exclusively on technique evaluation, scoring, and selection
- 🚫 FORBIDDEN to begin execution, payload development, or infrastructure setup — that is later steps
- 💬 Approach: Structured decision matrix with transparent scoring methodology
- 📊 Every technique must be scored on all dimensions — no partial evaluations
- 🔒 RoE authorization check is the FIRST filter — unauthorized techniques are eliminated immediately

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Selecting a technique not documented in RoE may have legal implications — even if technically feasible, without authorization it compromises the entire engagement
  - Operating without a fallback plan means failure on primary technique ends the operation — a plan without alternatives is a fragile plan that fails at the first unexpected obstacle
  - Choosing the "easiest" technique while ignoring the engagement's stealth requirements risks detection, which equals mission failure — ease alone is not a sufficient criterion
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present technique inventory before scoring — get user confirmation on RoE-authorized techniques
- ⚠️ Present [A]/[W]/[C] menu after selection finalized
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, RoE constraints, recon output, and attack surface analysis from steps 1-2
- Focus: Technique evaluation and selection only — no execution, infrastructure, or payload planning
- Limits: Only evaluate techniques within MITRE ATT&CK TA0001 that are RoE-authorized
- Dependencies: Attack surface classification and defensive posture mapping from step-02-attack-surface.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Available Technique Inventory

Present all MITRE ATT&CK TA0001 techniques with their authorization status from the Rules of Engagement:

```
| T-Code | Technique | Sub-Technique | RoE Authorized? | Feasibility (from Step 2) | Stealth Level | Complexity | Estimated Time |
|--------|-----------|---------------|-----------------|--------------------------|---------------|------------|----------------|
| T1566 | Phishing | - | ✅/❌/⚠️ | High/Medium/Low | Medium | Medium | 2-5 days |
| T1566.001 | | Spearphishing Attachment | ✅/❌/⚠️ | | | | |
| T1566.002 | | Spearphishing Link | ✅/❌/⚠️ | | | | |
| T1566.003 | | Spearphishing via Service | ✅/❌/⚠️ | | | | |
| T1190 | Exploit Public-Facing Application | - | ✅/❌/⚠️ | | | | |
| T1133 | External Remote Services | - | ✅/❌/⚠️ | | | | |
| T1078 | Valid Accounts | - | ✅/❌/⚠️ | | | | |
| T1078.001 | | Default Accounts | ✅/❌/⚠️ | | | | |
| T1078.002 | | Domain Accounts | ✅/❌/⚠️ | | | | |
| T1078.003 | | Local Accounts | ✅/❌/⚠️ | | | | |
| T1078.004 | | Cloud Accounts | ✅/❌/⚠️ | | | | |
| T1189 | Drive-by Compromise | - | ✅/❌/⚠️ | | | | |
| T1199 | Trusted Relationship | - | ✅/❌/⚠️ | | | | |
| T1200 | Hardware Additions | - | ✅/❌/⚠️ | | | | |
| T1091 | Replication Through Removable Media | - | ✅/❌/⚠️ | | | | |
```

**Authorization Legend:**
- ✅ Explicitly authorized in RoE
- ⚠️ Partially authorized (with constraints — document constraints)
- ❌ NOT authorized — **ELIMINATE IMMEDIATELY from further evaluation**

"**TA0001 technique inventory compiled.**

Authorized techniques: {{authorized_count}}
Constrained techniques: {{constrained_count}}
Excluded techniques (not authorized): {{excluded_count}}

Do you confirm the inventory before proceeding with scoring?"

**WAIT for user confirmation before scoring.**

### 2. Decision Matrix Scoring

For each RoE-authorized technique, apply a weighted multi-criteria decision matrix:

**Scoring Criteria (1-5 scale):**

| Criterion | Weight | Description | 1 (Worst) | 5 (Best) |
|-----------|--------|-------------|-----------|----------|
| Feasibility | 0.25 | Available attack surface for the technique | No suitable targets | Multiple highly exposed targets |
| Success Probability | 0.30 | Considering target's defensive posture | Strong defenses, bypass unlikely | Weak or absent defenses for this vector |
| Stealth | 0.20 | Likelihood of evading detection during and after | Detection nearly certain | Indistinguishable from legitimate traffic |
| RoE Compliance | 0.15 | Alignment with engagement constraints | Significant constraints limit effectiveness | Fully aligned, no constraints |
| Time/Resources | 0.10 | Effort required vs available timeline | Exceeds available timeline | Executable in days with current resources |

**Weighted Formula:**
```
Score = (Feasibility x 0.25) + (Success Prob. x 0.30) + (Stealth x 0.20) + (Compliance x 0.15) + (Time x 0.10)
```

**Present scored results ranked by total score:**
```
| Rank | T-Code | Technique | Feas. | Prob. | Stealth | Comp. | Time | Total Score |
|------|--------|-----------|-------|-------|---------|-------|------|-------------|
| 1 | {{tcode}} | {{name}} | {{/5}} | {{/5}} | {{/5}} | {{/5}} | {{/5}} | {{weighted}} |
| 2 | {{tcode}} | {{name}} | {{/5}} | {{/5}} | {{/5}} | {{/5}} | {{/5}} | {{weighted}} |
| ... | | | | | | | | |
```

For each score, provide a brief justification referencing step 2 analysis data.

### 3. Primary + Fallback Selection

Based on scoring, present the recommended selection for user approval:

**Primary Technique** — Highest scored, confirmed by user:
- T-code and name
- Targets selected for this technique (specific assets/people from recon)
- **Attack narrative**: step-by-step from delivery/exploit to callback
- Required infrastructure (overview — detailed in step 4)
- Required payloads (overview — developed in step 5)
- Estimated timeline
- Detection risk assessment: which defensive controls must be bypassed
- **Trigger for switching to fallback**: specific conditions indicating failure

**Fallback 1** — Second option if primary fails:
- Same structure as primary
- Must be a different technique (not a sub-technique of the primary)
- Activation trigger: what must happen to switch to this fallback

**Fallback 2** — Third option (different attack vector category):
- Same structure
- MUST belong to a different category (e.g., if primary is phishing, fallback 2 cannot be phishing)
- Represents the last resort plan

"Do you confirm the selection? You can modify primary and fallback before proceeding."

**WAIT for user confirmation of all three selections.**

### 4. ATT&CK Chain Mapping

Map the complete kill chain for the selected primary technique, showing how initial access connects to the broader operation:

**Primary Technique Chain:**
```
Reconnaissance (TA0043) → Resource Development (TA0042) → Initial Access (TA0001) → Execution (TA0002)
{{recon_technique}}     → {{resource_technique}}       → {{selected_technique}} → {{execution_technique}}
```

**Detailed chain for primary:**
- **Pre-conditions**: What must be true before execution (infrastructure ready, payload tested, pretext crafted)
- **Execution**: The initial access action itself
- **Post-conditions**: Expected state after successful execution (shell, credentials, session)
- **Next phase handoff**: How this connects to execution (TA0002) and persistence (TA0003)

**Fallback chain mappings** (abbreviated — same structure):
- Fallback 1: `{{recon}} → {{resource}} → {{fallback1}} → {{execution}}`
- Fallback 2: `{{recon}} → {{resource}} → {{fallback2}} → {{execution}}`

**Detection Surface Mapping for Primary:**
- Which telemetry sources would detect this technique? (email logs, EDR, network IDS, SIEM)
- What is the expected detection timeline? (immediate, hours, days)
- What TTPs in the chain have known detection signatures?
- Which parts of the chain are most likely to trigger alerts?

### 5. Presentation and Confirmation

Present the complete technique selection package for final operator approval:

"**Technique Selection Summary:**

**Primary:** {{T-code}} — {{technique_name}}
- Target: {{target_summary}}
- Score: {{weighted_score}}/5.00
- Stealth: {{stealth_assessment}}
- Timeline: {{estimated_timeline}}

**Fallback 1:** {{T-code}} — {{technique_name}}
- Trigger: {{switch_trigger}}
- Score: {{weighted_score}}/5.00

**Fallback 2:** {{T-code}} — {{technique_name}}
- Trigger: {{switch_trigger}}
- Score: {{weighted_score}}/5.00

**Kill Chain:** {{primary_chain_summary}}

Do you confirm the complete selection to proceed to infrastructure preparation?"

### 6. Append Findings to Report

Write the technique selection to the output document under `## Technique Selection`:

```markdown
## Technique Selection

### TA0001 Technique Inventory
{{technique_inventory_table — all techniques with RoE status}}

### Decision Matrix
{{scored_matrix — all authorized techniques with weighted scores}}

### Primary Technique
- T-Code: {{tcode}}
- Name: {{technique_name}}
- Target: {{target_summary}}
- Attack Narrative: {{step_by_step_narrative}}
- Fallback Trigger: {{switch_conditions}}

### Fallback 1
{{fallback_1_details}}

### Fallback 2
{{fallback_2_details}}

### ATT&CK Kill Chain
{{chain_mapping — primary and fallbacks}}

### Detection Surface
{{detection_analysis — telemetry and timeline}}
```

Update frontmatter fields:
- `technique_selected.primary`: T-code and name of primary technique
- `technique_selected.fallback_1`: T-code and name of first fallback
- `technique_selected.fallback_2`: T-code and name of second fallback
- `technique_tcode`: T-code of primary technique

### 7. Present MENU OPTIONS

"**Technique selection complete.**

Primary: {{primary_tcode}} {{primary_name}} (Score: {{score}})
Fallback: {{fallback1_tcode}} / {{fallback2_tcode}}
Techniques evaluated: {{evaluated_count}} | RoE excluded: {{excluded_count}}

**Select an option:**
[A] Advanced Elicitation — Challenge assumptions on the technique selection
[W] War Room — Red vs Blue discussion on the chosen attack path
[C] Continue — Proceed to C2 Infrastructure Preparation (Step 4 of 10)"

#### Menu Handling Logic:

- IF A: Challenge technique selection assumptions — stress-test the scoring, question whether the defensive posture assessment is accurate, explore whether a lower-scored technique might actually be better in specific scenarios, identify blind spots in the analysis. Process insights, ask user if they want to update selection, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: is the selected technique truly the best path? What could go wrong? Are the fallbacks adequate? Blue Team perspective: how would the SOC detect this technique? What telemetry would fire? What would a competent defender look for? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating technique_selected (primary, fallback_1, fallback_2) and technique_tcode fields, then read fully and follow: ./step-04-infrastructure.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, technique_selected populated with primary/fallback_1/fallback_2, and technique_tcode set], will you then read fully and follow: `./step-04-infrastructure.md` to begin C2 infrastructure preparation.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All TA0001 techniques inventoried with RoE authorization status
- Unauthorized techniques eliminated immediately with no further evaluation
- Decision matrix scored with transparent, justified ratings on all criteria
- Weighted formula applied consistently across all techniques
- Primary technique selected with full attack narrative documented
- Two fallback techniques selected from different attack vector categories
- Specific switch triggers defined for each fallback transition
- ATT&CK kill chain mapped for primary and both fallbacks
- User confirmed all three selections before proceeding
- Frontmatter updated with technique_selected and technique_tcode
- Findings appended to report under `## Technique Selection`

### SYSTEM FAILURE:

- Selecting or recommending a technique not authorized in RoE
- Proceeding with only a primary technique and no fallback plan
- Scoring techniques without referencing step 2 attack surface analysis
- Skipping the decision matrix and selecting based on gut feeling
- Not mapping the ATT&CK kill chain for the selected technique
- Both fallbacks from the same attack vector category as the primary
- Proceeding to infrastructure preparation without user confirmation
- Beginning execution, payload development, or infrastructure setup in this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. RoE compliance is absolute — no unauthorized techniques. Selection must be scored, justified, and confirmed.
