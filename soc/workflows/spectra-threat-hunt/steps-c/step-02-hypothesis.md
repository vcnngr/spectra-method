# Step 2: Hypothesis Development

**Progress: Step 2 of 8** — Next: Data Collection & Preparation

## STEP GOAL:

Develop structured, testable hunting hypotheses grounded in the trigger intelligence from step 1. Map hypotheses to specific ATT&CK techniques, identify required data sources per hypothesis, define success criteria and confidence levels, and produce a hypothesis development table that drives all subsequent data collection and analysis. The hypothesis is the intellectual foundation of the hunt — without a rigorous hypothesis, hunting degenerates into aimless searching.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER develop hypotheses without verified hunt trigger from step 1
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A THREAT HUNTER, not an automated correlation engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Threat Hunter developing hypotheses grounded in threat intelligence and adversary tradecraft
- ✅ Every hypothesis must be falsifiable — if you can't define what "not found" looks like, the hypothesis is untestable
- ✅ Think in ATT&CK procedures, not just techniques — the same technique can be executed dozens of different ways
- ✅ The absence of evidence is not evidence of absence — if data sources are insufficient, the hypothesis is inconclusive, not refuted
- ✅ Hypotheses must account for adversary evasion — sophisticated threat actors specifically avoid common detection patterns

### Step-Specific Rules:

- 🎯 Focus exclusively on hypothesis development, ATT&CK mapping, data source identification, and success criteria definition
- 🚫 FORBIDDEN to execute any queries or collect any data — this is planning, not execution
- 💬 Approach: Strategic and inquisitive — challenge assumptions, consider alternative explanations, define what "not found" means
- 📊 Every hypothesis must include: ATT&CK mapping, required data sources, testability assessment, and expected observables
- 🔒 All hypotheses must reference intelligence from step 1 — do not fabricate threat context

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Hypotheses that rely on a single data source create a single point of failure — if that source has gaps, blind spots, or is evaded, the entire hypothesis becomes untestable. Recommend requiring corroborating data sources where possible to increase confidence in both positive and negative results.
  - Overly broad hypotheses (e.g., "APT is present in the network") are unfalsifiable and lead to unbounded investigation — narrow the hypothesis to specific techniques, specific environments, and specific observables to make the hunt tractable and the results actionable.
  - Hypotheses based solely on IOCs without behavioral components will miss adversaries who have rotated their infrastructure — consider adding behavioral hypotheses that detect the technique regardless of the specific indicators used, especially for strategic hunts.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present hypothesis development plan before constructing hypotheses — get user input on approach
- ⚠️ Present [A]/[W]/[C] menu after hypothesis development complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `hypotheses_tested`, `mitre_techniques_targeted`, `mitre_tactics_targeted`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, hunt trigger data, extracted intelligence, hunt scope definition, hunt classification from step 1
- Focus: Hypothesis development, ATT&CK mapping, data source planning, and success criteria — no data collection or analysis
- Limits: Only develop hypotheses grounded in step 1 trigger intelligence — do not invent unrelated threats
- Dependencies: Completed hunt mission definition and scope from step-01-init.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Review Hunt Mission Context

Load the Hunt Mission section from step 1 output. Summarize the key inputs for hypothesis development:

"**Hypothesis Development — Input Summary:**

| Input | Value |
|-------|-------|
| Hunt ID | {{hunt_id}} |
| Trigger Type | {{trigger_type}} |
| Hunt Classification | {{Tactical / Strategic / Hybrid}} |
| Threat Actor(s) | {{actors or 'Not attributed'}} |
| ATT&CK Techniques (from trigger) | {{T-codes or 'None provided'}} |
| Target Environment | {{scope summary}} |
| Historical Lookback | {{lookback window}} |
| Data Sources Available | {{count available}} / {{count total assessed}} |

Ready to develop hunting hypotheses from this trigger intelligence."

### 2. ATT&CK-Based Hypothesis Construction

#### A. Technique Mapping

Map the hunt trigger to specific ATT&CK techniques. For each technique, provide full detail:

"**ATT&CK Technique Mapping:**

| # | Technique ID | Technique Name | Tactic | Sub-technique | Platforms | Data Sources Required |
|---|-------------|---------------|--------|---------------|-----------|----------------------|
| 1 | {{T-code}} | {{name}} | {{tactic}} | {{sub-technique or 'N/A'}} | {{Windows/Linux/macOS/Cloud}} | {{specific data sources}} |
| 2 | ... | ... | ... | ... | ... | ... |

**Total techniques mapped:** {{count}}
**Tactics covered:** {{list of unique tactics in order of kill chain position}}"

#### B. Tactic Chain Analysis

Identify the expected tactic chain — how would an adversary using these techniques progress through the kill chain?

"**Expected Tactic Chain:**

```
{{Tactic 1}} → {{Tactic 2}} → {{Tactic 3}} → ... → {{Final Tactic}}
  └─ {{T-code}}: {{technique_name}}  └─ {{T-code}}: {{technique_name}}  └─ {{T-code}}: {{technique_name}}
```

**Chain assessment:**
- **Entry point:** {{where the adversary enters — initial access technique and vector}}
- **Progression path:** {{how the adversary moves through tactics — what enables each step}}
- **Objective:** {{what the adversary is trying to achieve — data theft, persistence, disruption}}
- **Gaps in chain:** {{tactics in the chain where we have no techniques mapped — these are blind spots}}"

#### C. Threat Actor Profiling (if intel-driven)

If the trigger references known threat actors, profile their tradecraft:

"**Threat Actor Profile:**

| Attribute | Detail |
|-----------|--------|
| Actor Name | {{name or alias}} |
| Attribution Confidence | {{High / Medium / Low / Unconfirmed}} |
| Motivation | {{espionage / financial / hacktivism / sabotage / unknown}} |
| Known TTPs | {{list of ATT&CK techniques historically attributed}} |
| Preferred Tools | {{malware families, frameworks, custom tools}} |
| Target Profile | {{industries, geographies, organization sizes}} |
| Recent Activity | {{most recent campaign, date, summary}} |
| Evasion Sophistication | {{Low (commodity tools) / Medium (custom tools, basic evasion) / High (living-off-the-land, custom C2, advanced evasion)}} |

**Environmental applicability:** {{Does the target environment match this actor's historical target profile? Are the preconditions for their techniques present?}}"

#### D. Environmental Applicability Assessment

For each mapped technique, assess whether the target environment has the preconditions:

"**Environmental Applicability Matrix:**

| Technique | Precondition | Present in Environment? | Notes |
|-----------|-------------|------------------------|-------|
| {{T-code}}: {{name}} | {{precondition — e.g., "Windows hosts with PowerShell enabled"}} | ✅/❌/⚠️ | {{e.g., "90% of endpoints run Windows 10/11"}} |
| {{T-code}}: {{name}} | {{precondition — e.g., "Cloud workloads with IAM roles"}} | ✅/❌/⚠️ | {{e.g., "3 AWS accounts with 47 IAM roles"}} |
| ... | ... | ... | ... |

**Techniques with missing preconditions:** {{list — these techniques can be deprioritized in hypothesis development}}
**Techniques with confirmed preconditions:** {{list — these are the primary hypothesis candidates}}"

### 3. Hypothesis Formulation

For each viable technique (preconditions confirmed), formulate a structured hypothesis:

#### A. Hypothesis Structure

Each hypothesis follows this framework:
- **Structure:** "If [threat actor/technique] is present in [environment], then we expect to observe [observable behavior] in [data source]"
- **Primary hypothesis** — the main claim to test
- **Alternative hypotheses** — legitimate explanations for the same observables
- **Null hypothesis** — what "not found" looks like vs "can't detect" (critical distinction)

#### B. Hypothesis Development Table

"**Hunt Hypotheses:**

---

**Hypothesis H1: {{descriptive name}}**

| Field | Detail |
|-------|--------|
| **Statement** | If {{threat actor/technique}} is present in {{environment}}, then we expect to observe {{observable behavior}} in {{data source}} |
| **ATT&CK Technique** | {{T-code}}: {{technique name}} ({{tactic}}) |
| **ATT&CK Procedure** | {{specific procedure — how the technique is executed, not just the technique category}} |
| **Target Environment** | {{specific systems/network segment/cloud tenant}} |
| **Expected Observables** | {{specific artifacts, log entries, behavioral patterns}} |
| **Primary Data Source** | {{main data source for this hypothesis}} |
| **Corroborating Sources** | {{additional data sources that could confirm or deny}} |
| **Alternative Explanations** | {{legitimate activity that could produce similar observables}} |
| **Null Hypothesis** | {{what the data looks like if the threat is NOT present — vs — what it looks like if we can't detect it}} |
| **Testability** | {{High (data sources available, clear observables) / Medium (partial data, ambiguous observables) / Low (missing data sources, noisy observables)}} |
| **Priority** | {{Critical / High / Medium / Low — based on threat severity and testability}} |

**Expected Evidence Patterns:**
```
{{Specific log entries, process chains, network patterns, or file artifacts that would confirm this hypothesis}}
Example:
- Sysmon EventID 1: powershell.exe spawned by winword.exe with encoded command
- Windows Security 4688: cmd.exe with /c certutil -urlcache -split -f http://{{domain}}
- Zeek DNS: query for {{domain}} from {{internal IP}} with no prior history
```

**False Positive Baseline:**
```
{{What legitimate activity looks like that could resemble this technique}}
Example:
- IT admin using PowerShell with encoded commands for scheduled maintenance
- SCCM deploying software via certutil
- DNS queries to CDN domains that are newly observed but legitimate
```

---

**Hypothesis H2: {{descriptive name}}**
{{Repeat the same structure}}

---

**Hypothesis H3: {{descriptive name}}**
{{Repeat the same structure — develop at minimum 2-4 hypotheses depending on trigger complexity}}

---"

### 4. Data Source Requirements per Hypothesis

Consolidate all data source requirements across hypotheses:

"**Data Source Requirements Matrix:**

| Data Source | Required By | Available? | Retention | Gaps/Limitations |
|-------------|-------------|-----------|-----------|-----------------|
| {{source}} | H1, H3 | ✅/⚠️/❌ | {{days}} | {{specific limitations}} |
| {{source}} | H2 | ✅/⚠️/❌ | {{days}} | {{specific limitations}} |
| ... | ... | ... | ... | ... |

**Coverage Assessment:**
- Hypotheses fully testable (all data sources available): {{list}}
- Hypotheses partially testable (some data sources missing): {{list — note which sources are missing}}
- Hypotheses untestable (critical data sources missing): {{list — note what would need to change}}

**Recommendation:** {{Proceed with testable hypotheses / Request additional data source access / Adjust scope}}"

### 5. Success Criteria Definition

Define clear success and failure criteria for the hunt:

"**Hunt Success Criteria:**

| Finding Type | Definition | Required Evidence |
|-------------|------------|-------------------|
| **Confirmed** (direct evidence) | Direct evidence of attacker activity — C2 communication, tool deployment, data staging, credential theft | Corroborated by 2+ independent data sources, timeline consistent, alternative explanations eliminated |
| **Probable** (strong circumstantial) | Strong circumstantial evidence — behavioral match to hypothesis, anomalous activity inconsistent with baseline, but not conclusive | Single strong data source with behavioral match, alternative explanations not fully eliminated |
| **Possible** (weak indicators) | Weak indicators that warrant further investigation — statistical anomaly, partial pattern match, unusual but explainable | Statistical deviation from baseline, partial indicator match, requires additional data or analysis |
| **Not Found** (hypothesis refuted) | Sufficient investigation completed with adequate data sources — no evidence found, hypothesis rejected for this environment and time window | All planned queries executed, data sources confirmed healthy, baseline established — absence of evidence with sufficient detection capability constitutes evidence of absence |
| **Inconclusive** (untestable) | Insufficient data to confirm or refute — critical data source missing, retention too short, logging gaps | Data source gap documented, required remediation identified, hypothesis marked for re-testing when data is available |

**CRITICAL:** 'Not Found' and 'Inconclusive' are fundamentally different outcomes. 'Not Found' means we looked and didn't see it. 'Inconclusive' means we couldn't look properly. The distinction determines whether we re-hunt or remediate data sources."

### 6. Hypothesis Prioritization and Hunt Plan

"**Hypothesis Priority and Execution Order:**

| Priority | Hypothesis | Testability | Estimated Effort | Execution Order |
|----------|-----------|-------------|-----------------|----------------|
| {{Critical/High/Medium/Low}} | H1: {{name}} | {{High/Medium/Low}} | {{time estimate}} | {{1/2/3/...}} |
| ... | ... | ... | ... | ... |

**Execution strategy:**
- {{If hybrid hunt: IOC sweep first (quick wins), then behavioral analysis (deeper investigation)}}
- {{Dependency chain: hypothesis X depends on results of hypothesis Y}}
- {{Parallel vs sequential: hypotheses that can be investigated simultaneously vs those that build on each other}}
- {{Time allocation: estimated hours per hypothesis based on complexity and data volume}}"

### 7. Present MENU OPTIONS

"**Hypothesis development complete.**

Summary: {{hypothesis_count}} hypotheses developed across {{technique_count}} ATT&CK techniques.
Testability: {{testable_count}} fully testable | {{partial_count}} partially testable | {{untestable_count}} untestable
Priority: {{critical_count}} critical | {{high_count}} high | {{medium_count}} medium | {{low_count}} low

**Select an option:**
[A] Advanced Elicitation — Challenge hypotheses, identify blind spots, refine testability
[W] War Room — Red vs Blue discussion on hypothesis quality and adversary evasion strategies
[C] Continue — Proceed to Data Collection & Preparation (Step 3 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive hypothesis analysis — challenge the assumptions underlying each hypothesis, identify what an adversary would do to evade detection of these specific observables, propose additional hypotheses based on adjacent ATT&CK techniques, assess whether the null hypothesis is genuinely distinguishable from the positive hypothesis given available data sources. Process insights, ask user if they want to update hypotheses, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: which of these hypotheses would I be most concerned about as the attacker? Which are easy to evade? What techniques would I add to my playbook that these hypotheses don't cover? If I knew this hunt was coming, what would I change about my operations? Blue Team perspective: are our hypotheses testable with the available data? Are we relying too heavily on known TTPs and missing novel approaches? How do we handle the "inconclusive" hypotheses — accept the risk or invest in data source improvement? What is the detection engineering value if we find nothing? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `hypotheses_tested` count, `mitre_techniques_targeted` array, `mitre_tactics_targeted` array. Append hypothesis development to report under `## Hypothesis Development`. Then read fully and follow: ./step-03-data-collection.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and hypotheses_tested count updated, and hypothesis development appended to report under `## Hypothesis Development`], will you then read fully and follow: `./step-03-data-collection.md` to begin data collection and preparation.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All ATT&CK techniques from trigger mapped with full detail (ID, name, tactic, sub-technique, platforms, data sources)
- Tactic chain analyzed with entry point, progression path, objective, and gaps identified
- Threat actor profiled (if intel-driven) with tradecraft, tools, and evasion sophistication
- Environmental applicability assessed per technique with precondition verification
- At least 2-4 hypotheses developed, each with: structured statement, ATT&CK mapping, expected observables, alternative explanations, null hypothesis, testability assessment, and priority
- Data source requirements consolidated across all hypotheses with availability assessment
- Success criteria defined with clear distinction between "Not Found" and "Inconclusive"
- Hypotheses prioritized and execution order determined
- Hypothesis Development section populated in output document
- Frontmatter updated with hypotheses_tested, mitre_techniques_targeted, mitre_tactics_targeted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Developing hypotheses without grounding in step 1 trigger intelligence
- Hypotheses that are not falsifiable (no clear "not found" definition)
- Not mapping hypotheses to specific ATT&CK techniques with full detail
- Not assessing environmental applicability (hunting for techniques with missing preconditions)
- Not identifying data source requirements per hypothesis
- Not distinguishing between "Not Found" and "Inconclusive" in success criteria
- Treating all hypotheses as equal priority without testability and severity assessment
- Beginning data collection or query execution during hypothesis development
- Not accounting for adversary evasion in hypothesis construction
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every hypothesis must be grounded in intelligence, mapped to ATT&CK, and testable against available data sources. The hypothesis is the hunt — without it, you're just searching.
