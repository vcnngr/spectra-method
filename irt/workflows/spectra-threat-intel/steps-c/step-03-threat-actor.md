# Step 3: Threat Actor Profiling

**Progress: Step 3 of 8** — Next: Diamond Model Analysis

## STEP GOAL:

Identify and profile the threat actor(s) behind the intelligence trigger using all collected data from step 2. This includes: known group attribution with vendor naming cross-references, characterization of unknown actors, profiling motivation, capability, intent, and historical campaigns, mapping known TTPs to MITRE ATT&CK, documenting infrastructure patterns and geographic associations (with explicit caveats), analyzing victimology, and providing an evidence-based attribution confidence assessment with alternative hypotheses. The actor profile is the adversary model that drives all downstream analysis — Diamond Model, Kill Chain, assessment, and detection content.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER present attribution as certain — all attribution carries confidence levels (high, moderate, low) with explicit justification
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST performing adversary profiling, not a database lookup engine
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst building an adversary model that will drive all downstream analysis and detection
- Attribution is one of the hardest problems in intelligence — be rigorous, cite evidence, acknowledge alternative explanations
- Threat actors use shared tooling, false flags, and deliberate misdirection — never assume attribution from a single indicator
- Geographic associations are NOT attribution — infrastructure hosted in a country does not mean the actor is from that country
- Vendor naming conventions differ — the same actor has multiple names across vendors. Always cross-reference
- Historical campaigns inform but do not determine current activity — actors evolve their TTPs

### Step-Specific Rules:

- Focus exclusively on actor identification, profiling, TTP mapping, attribution confidence, and alternative hypothesis generation
- FORBIDDEN to perform Diamond Model analysis (step 4), Kill Chain mapping (step 5), or assessment (step 6) — those build on this profile
- FORBIDDEN to state attribution without confidence level and supporting evidence
- FORBIDDEN to dismiss alternative hypotheses without evidence
- Approach: Evidence-based adversary modeling with explicit confidence calibration and intellectual humility
- Every attribution claim must cite specific evidence from the collection (step 2) and specify the Admiralty reliability of the source

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Attributing activity to a specific threat actor based on a single indicator (e.g., a single malware hash or C2 domain) is analytically unsound — commodity malware is used by dozens of groups, infrastructure is frequently shared or compromised, and sophisticated actors deliberately plant false attribution indicators. Premature attribution narrows the investigation and may cause the team to miss the real adversary
  - Dismissing the possibility of an unknown or new threat actor because the TTPs partially match a known group ignores the reality that new groups emerge constantly, known groups evolve, and copycat operations deliberately mimic known actors — always maintain "unknown actor" as a live hypothesis until evidence overwhelmingly favors attribution
  - Treating geographic hosting of infrastructure as evidence of actor nationality conflates infrastructure with identity — adversaries routinely use VPNs, compromised hosts, bulletproof hosting in jurisdictions unrelated to their origin, and cloud infrastructure that spans regions. Geographic associations should be noted as infrastructure facts, never as attribution evidence
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Build the profile from evidence upward, not from a hypothesis downward — avoid confirmation bias
- Present all evidence for AND against each attribution hypothesis
- Maintain alternative hypotheses until overwhelming evidence favors one
- Update frontmatter: add this step name to the end of the stepsCompleted array
- FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: All collected and processed data from step 2 (IOC inventory, source-by-source findings, corroboration matrix, temporal ordering), intelligence requirements from step 1 (PIRs, trigger details)
- Focus: Actor identification, profiling, TTP mapping, attribution confidence, alternative hypotheses — no Diamond Model, no Kill Chain, no assessment
- Limits: Attribution is limited by the collected evidence. If evidence is insufficient for attribution, say so explicitly — "insufficient evidence for attribution" is a valid and important analytic finding
- Dependencies: Processed intelligence from step-02-collection.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Actor Identification

Begin by examining the collected evidence for indicators that point to a specific threat actor or actor category:

"**Actor Identification — Evidence Review:**

#### 1a. Known Group Indicators
Search the collected evidence for matches against known threat actor databases:

| Evidence Type | Value | Matched Actor(s) | Source | Reliability | Match Type |
|---------------|-------|-------------------|--------|-------------|------------|
| Malware hash | {{hash}} | {{actor(s)}} | {{source}} | {{rating}} | Exact / Behavioral / Family |
| C2 infrastructure | {{IP/domain}} | {{actor(s)}} | {{source}} | {{rating}} | Exact / Historical / Shared |
| TTP pattern | {{technique}} | {{actor(s)}} | {{source}} | {{rating}} | Signature / Common / Widespread |
| Email address | {{email}} | {{actor(s)}} | {{source}} | {{rating}} | Registration / Phishing / Attribution |
| Tool usage | {{tool}} | {{actor(s)}} | {{source}} | {{rating}} | Custom / Modified commodity / Commodity |

**Match Analysis:**
- Indicators matching a single known group: {{count}}
- Indicators matching multiple groups: {{count}}
- Indicators with no known group match: {{count}}
- Custom tooling indicators (strongest attribution signal): {{count}}
- Commodity tooling indicators (weak attribution signal): {{count}}

#### 1b. Actor Category Classification
Based on the evidence, classify the actor category:

| Category | Indicators For | Indicators Against | Assessment |
|----------|---------------|-------------------|------------|
| **Nation-State / APT** | {{indicators}} | {{counter-indicators}} | {{likely/possible/unlikely}} |
| **Cybercrime (Organized)** | {{indicators}} | {{counter-indicators}} | {{likely/possible/unlikely}} |
| **Cybercrime (Opportunistic)** | {{indicators}} | {{counter-indicators}} | {{likely/possible/unlikely}} |
| **Hacktivist** | {{indicators}} | {{counter-indicators}} | {{likely/possible/unlikely}} |
| **Insider Threat** | {{indicators}} | {{counter-indicators}} | {{likely/possible/unlikely}} |
| **Unknown / New Actor** | {{indicators}} | {{counter-indicators}} | {{likely/possible/unlikely}} |

**Leading category assessment:** {{category}} — Confidence: {{high/moderate/low}}
**Evidence basis:** {{specific evidence justifying the category}}"

### 2. Vendor Naming Cross-Reference

If the evidence points to a known group, cross-reference naming conventions across vendors:

"**Vendor Naming Cross-Reference:**

Threat actors are tracked under different names by different vendors. The same actor group may have 5-10+ different designations.

| Vendor | Name | Aliases | Source |
|--------|------|---------|--------|
| MITRE ATT&CK | {{group_id}} — {{name}} | {{aliases}} | attack.mitre.org |
| Microsoft | {{name}} | | Microsoft Threat Intelligence |
| CrowdStrike | {{name}} | | CrowdStrike Falcon Intelligence |
| Mandiant / Google | {{name}} | | Mandiant Threat Intelligence |
| Unit 42 / Palo Alto | {{name}} | | Unit 42 |
| Cisco Talos | {{name}} | | Cisco Talos Intelligence |
| ESET | {{name}} | | ESET Research |
| Kaspersky | {{name}} | | Kaspersky GReAT |
| Symantec / Broadcom | {{name}} | | Symantec Threat Intelligence |
| Secureworks | {{name}} | | Secureworks CTU |
| Other vendors | {{name}} | | {{source}} |

**Common name for this report:** {{selected name}} (with aliases listed for cross-reference)

**Note:** If vendor attributions conflict (different vendors attribute the same indicators to different groups), document the conflict explicitly. Vendor disagreement is important context for the consumer."

### 3. Actor Profile

Build the comprehensive threat actor profile:

"**Threat Actor Profile: {{actor_name or 'UNKNOWN-{{intel_id}}'}}**

#### 3a. Motivation Assessment

| Motivation | Evidence | Confidence |
|-----------|----------|------------|
| **Financial gain** | {{evidence or 'No indicators'}} | {{high/moderate/low/none}} |
| **Espionage (state-sponsored)** | {{evidence or 'No indicators'}} | {{high/moderate/low/none}} |
| **Espionage (corporate/competitive)** | {{evidence or 'No indicators'}} | {{high/moderate/low/none}} |
| **Hacktivism / Ideological** | {{evidence or 'No indicators'}} | {{high/moderate/low/none}} |
| **Destructive / Sabotage** | {{evidence or 'No indicators'}} | {{high/moderate/low/none}} |
| **Access brokering** | {{evidence or 'No indicators'}} | {{high/moderate/low/none}} |
| **Unknown** | {{evidence supporting uncertainty}} | |

**Leading motivation assessment:** {{motivation}} — Confidence: {{level}}
**So what:** {{what this motivation means for the organization — what the actor wants and why it matters}}

#### 3b. Capability Assessment

| Capability Dimension | Assessment | Evidence |
|---------------------|------------|----------|
| **Custom tooling** | {{yes/no — describe tools}} | {{evidence}} |
| **Exploit development** | {{zero-day / n-day / commodity only}} | {{evidence}} |
| **Infrastructure sophistication** | {{dedicated / shared / compromised / cloud}} | {{evidence}} |
| **OPSEC discipline** | {{high / moderate / low}} | {{evidence}} |
| **Persistence sophistication** | {{advanced / moderate / basic}} | {{evidence}} |
| **Evasion capability** | {{advanced / moderate / basic}} | {{evidence}} |
| **Data exfiltration capability** | {{demonstrated / suspected / unknown}} | {{evidence}} |
| **Destructive capability** | {{demonstrated / suspected / unknown}} | {{evidence}} |

**Overall capability level:** {{sophisticated / moderate / basic / unknown}}
**Who cares:** {{who in the organization should be concerned based on this capability level}}

#### 3c. Intent Assessment

Based on motivation, capability, and observed behavior:

- **Immediate intent:** What is the actor trying to accomplish RIGHT NOW based on observed activity?
- **Probable objectives:** What are the likely end-state goals based on the actor profile?
- **Alternative objectives:** What other goals are consistent with the observed behavior?
- **Timeline assessment:** Is this a quick hit (days) or a long-term operation (weeks/months)?

**What now:** {{specific actions the organization should take based on the intent assessment}}"

### 4. Historical Campaigns

Research and document the actor's historical campaign activity:

"**Historical Campaigns (if known actor):**

| # | Campaign | Timeframe | Targets (Sector/Geo) | TTPs | Tools | Outcome | Source |
|---|----------|-----------|----------------------|------|-------|---------|--------|
| 1 | {{name}} | {{dates}} | {{targets}} | {{key TTPs}} | {{tools}} | {{public outcome}} | {{source}} |
| 2 | {{name}} | {{dates}} | {{targets}} | {{key TTPs}} | {{tools}} | {{public outcome}} | {{source}} |

**Campaign Pattern Analysis:**
- **Target consistency:** Does this actor consistently target our sector/geography? (high/moderate/low consistency)
- **TTP evolution:** How have the actor's TTPs changed over time? (stable / evolving / rapidly changing)
- **Tool evolution:** Has the actor upgraded tools between campaigns? (same tools / new variants / entirely new tooling)
- **Operational tempo:** How frequently does this actor launch campaigns? (continuous / periodic / sporadic)
- **Relationship to current activity:** How does the current trigger activity compare to historical campaigns? (consistent / deviation / evolution)

**If unknown actor:**
"No historical campaigns can be attributed to this actor with the current evidence. The actor is characterized as UNKNOWN-{{intel_id}} for tracking purposes. Any future intelligence that correlates to the indicators in this report should be cross-referenced for potential campaign linkage."

### 5. Known TTPs — ATT&CK Mapping

Map all observed and historically documented TTPs to MITRE ATT&CK:

"**ATT&CK TTP Mapping for {{actor_name}}:**

#### Observed in Current Activity (from collected evidence):

| ATT&CK ID | Technique | Tactic | Procedure Detail | Evidence | Source | Confidence |
|------------|-----------|--------|------------------|----------|--------|------------|
| {{T-code}} | {{name}} | {{tactic}} | {{how this actor uses this technique}} | {{specific evidence}} | {{source}} | {{high/moderate/low}} |

#### Historically Documented (from threat intelligence):

| ATT&CK ID | Technique | Tactic | Procedure Detail | Campaign | Source | Last Observed |
|------------|-----------|--------|------------------|----------|--------|---------------|
| {{T-code}} | {{name}} | {{tactic}} | {{how this actor uses this technique}} | {{campaign}} | {{source}} | {{date}} |

#### Expected but NOT Observed:
Based on the actor profile and historical TTPs, the following techniques are expected but were NOT detected in the current activity:

| ATT&CK ID | Technique | Tactic | Why Expected | Possible Explanations |
|------------|-----------|--------|--------------|----------------------|
| {{T-code}} | {{name}} | {{tactic}} | {{why we expect this}} | {{not used / not detected / evasion / not yet deployed}} |

**TTP Coverage:**
- Techniques observed in current activity: {{count}}
- Techniques documented historically: {{count}}
- Techniques expected but not observed: {{count}} — **these are detection blind spots or techniques not yet deployed**
- Total ATT&CK techniques associated: {{count}}"

### 6. Infrastructure Patterns

"**Infrastructure Analysis:**

#### Known Infrastructure Patterns:
| Pattern | Current Activity | Historical Pattern | Consistency |
|---------|-----------------|-------------------|-------------|
| **Hosting providers** | {{providers}} | {{historical providers}} | {{consistent/different}} |
| **Domain registration** | {{registrar, privacy service}} | {{historical pattern}} | {{consistent/different}} |
| **SSL/TLS certificates** | {{cert patterns}} | {{historical pattern}} | {{consistent/different}} |
| **C2 protocols** | {{protocols}} | {{historical protocols}} | {{consistent/different}} |
| **IP ranges / ASNs** | {{ranges}} | {{historical ranges}} | {{consistent/different}} |
| **DNS patterns** | {{DNS behavior}} | {{historical DNS}} | {{consistent/different}} |

#### Geographic Associations (WITH CAVEATS):

| Infrastructure Element | Geographic Location | Confidence | Caveat |
|----------------------|---------------------|------------|--------|
| {{element}} | {{country/region}} | {{level}} | {{e.g., 'VPN egress — does NOT indicate actor nationality'}} |

**CRITICAL CAVEAT:** Geographic associations describe WHERE infrastructure is located, NOT where the actor is from. Adversaries deliberately use infrastructure in multiple jurisdictions to complicate attribution. Geographic data is an infrastructure fact, not an identity indicator."

### 7. Victimology

"**Victimology Analysis:**

Who does this actor target? Understanding victimology helps assess whether our organization is a primary, secondary, or incidental target.

| Dimension | Pattern | Evidence | Our Organization |
|-----------|---------|----------|-----------------|
| **Sector targeting** | {{sectors targeted}} | {{source}} | {{match/no match}} |
| **Geographic targeting** | {{regions/countries}} | {{source}} | {{match/no match}} |
| **Organization size** | {{large/medium/small/all}} | {{source}} | {{match/no match}} |
| **Technology targeting** | {{specific technologies}} | {{source}} | {{match/no match}} |
| **Data targeting** | {{what data they pursue}} | {{source}} | {{match/no match}} |
| **Supply chain targeting** | {{upstream/downstream targeting}} | {{source}} | {{match/no match}} |

**Victimology Assessment:**
- Match score: {{count matches}} / {{total dimensions}}
- Our organization as a target: {{primary target / secondary target / target of opportunity / unlikely target}}
- **So what:** {{what this means for our risk posture}}"

### 8. Attribution Confidence Assessment

"**Attribution Confidence Assessment:**

This is the rigorous assessment of how confident we are in the actor identification.

#### Evidence Summary for Attribution:

| Evidence Category | Count | Quality (Admiralty) | Attribution Weight |
|-------------------|-------|--------------------|--------------------|
| Custom tooling matches | {{count}} | {{range}} | HIGH — custom tools are the strongest attribution indicator |
| Infrastructure overlaps | {{count}} | {{range}} | MEDIUM — infrastructure can be shared or compromised |
| TTP consistency | {{count}} | {{range}} | MEDIUM — TTPs can be copied |
| Victimology consistency | {{count}} | {{range}} | LOW-MEDIUM — many actors target same sectors |
| Malware family matches | {{count}} | {{range}} | MEDIUM — malware can be shared, sold, or leaked |
| Operational patterns | {{count}} | {{range}} | MEDIUM — working hours, language artifacts, etc. |
| Direct statements | {{count}} | {{range}} | VARIABLE — claims may be false, misdirection |

#### Attribution Confidence Level:

**HIGH confidence** requires:
- Multiple independent evidence categories converging on the same actor
- At least one category with strong indicators (custom tooling, unique infrastructure, actor-specific procedures)
- No significant evidence contradicting the attribution
- Corroboration from multiple reliable sources (Admiralty A-B)

**MODERATE confidence** requires:
- Several evidence categories pointing to the same actor
- Some indicators are shared with other actors
- Alternative explanations exist but are less consistent with the evidence
- Mix of reliable and less reliable sources

**LOW confidence** means:
- Limited evidence categories
- Indicators are largely commodity (shared tools, common infrastructure)
- Multiple actors could be responsible
- Primarily single-source or low-reliability sources

**Current attribution confidence: {{HIGH / MODERATE / LOW / INSUFFICIENT}}**

**Justification:** {{detailed justification citing specific evidence and source reliability}}

#### Alternative Hypotheses:

| # | Hypothesis | Supporting Evidence | Contradicting Evidence | Plausibility |
|---|-----------|---------------------|----------------------|--------------|
| 1 | {{actor_name}} (leading) | {{evidence}} | {{counter-evidence}} | {{high/moderate/low}} |
| 2 | {{alternative actor}} | {{evidence}} | {{counter-evidence}} | {{high/moderate/low}} |
| 3 | Unknown / New actor | {{evidence}} | {{counter-evidence}} | {{high/moderate/low}} |

#### What Would Change Confidence:

| To Increase Confidence | To Decrease Confidence |
|----------------------|----------------------|
| {{evidence that would strengthen attribution}} | {{evidence that would weaken attribution}} |
| {{e.g., identifying custom tool source code overlap}} | {{e.g., discovering the malware is publicly available}} |
| {{e.g., HUMINT corroboration from government partner}} | {{e.g., another actor claiming responsibility with proof}} |"

### 9. Update Frontmatter & Append to Report

**Update frontmatter:**
- Add this step name to the end of `stepsCompleted`
- `threat_actors_identified`: array of identified actor names/IDs
- `threat_actor_count`: number of actors identified
- `attribution_confidence`: current confidence level (high/moderate/low/insufficient)
- `actor_motivation`: leading motivation assessment
- `actor_capability`: overall capability level
- `mitre_techniques`: updated array with all ATT&CK T-codes from this step
- `mitre_technique_count`: total unique techniques

**Append to report under `## Threat Actor Profile`:**
- Actor Identification (evidence review, category classification)
- Actor Profile (motivation, capability, intent)
- Historical Campaigns
- Known TTPs (ATT&CK mapping table)
- Attribution Assessment (confidence, alternative hypotheses, what would change confidence)

### 10. Present MENU OPTIONS

"**Threat actor profiling complete.**

**Actor Summary:**
- Identified actor: {{actor_name or 'UNKNOWN-' + intel_id}}
- Category: {{nation-state / cybercrime-organized / cybercrime-opportunistic / hacktivist / insider / unknown}}
- Motivation: {{motivation}} ({{confidence}} confidence)
- Capability: {{sophisticated / moderate / basic / unknown}}
- Attribution confidence: {{HIGH / MODERATE / LOW / INSUFFICIENT}}
- Alternative hypotheses: {{count}} maintained
- ATT&CK techniques: {{count}} observed, {{count}} historical, {{count}} expected but not observed
- Victimology match: {{count}} / {{total dimensions}}
- Our organization: {{primary / secondary / opportunistic / unlikely}} target

**So what:** {{one-sentence summary of what this means for the organization}}
**Who cares:** {{who needs to know — CISO? SOC? IR team? Legal?}}
**What now:** {{specific recommended actions based on the actor profile}}

**Select an option:**
[A] Advanced Elicitation — Challenge attribution: is the evidence truly converging or are we anchoring on the first match? Are the alternative hypotheses given fair weight? Are we confusing infrastructure geography with actor identity? Is the capability assessment calibrated or assumed?
[W] War Room — Red Team: if I were this actor, would my profile match what the analyst described? What would I do differently to evade profiling? Would I plant false attribution indicators? Blue Team: given this actor profile, what are our immediate detection priorities? Which of their historical TTPs are we NOT detecting? Where should we focus hunting?
[C] Continue — Proceed to Step 4: Diamond Model Analysis (Step 4 of 8)"

#### Menu Handling Logic:

- IF A: Deep analysis — systematically challenge the attribution. Is the evidence base diverse enough or concentrated in one category? Could confirmation bias be at work (did we find what we expected)? Are the alternative hypotheses truly alternative or just minor variations of the leading hypothesis? Is the capability assessment based on observed evidence or assumed from the actor's reputation? Are there deception indicators in the collected data? Process insights, ask operator if adjustments are warranted, if yes update and redisplay, if no redisplay
- IF W: War Room — Red Team perspective: the analyst thinks they know who I am. Do they? Would I use my best tools against this target or save them? Would I plant indicators pointing to another group? How would I adapt if I knew this intelligence product was being created? Blue Team perspective: given the actor profile, what are the highest-priority detection gaps? Which historical TTPs should we search for immediately? What containment strategy matches this actor's capability level? Should we brief the SOC on this actor's patterns? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated with actor identification and attribution confidence. Then read fully and follow: ./step-04-diamond-model.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, threat_actors_identified, threat_actor_count, attribution_confidence, actor_motivation, actor_capability, and mitre_techniques all updated, and Threat Actor Profile section fully populated in the output document], will you then read fully and follow: `./step-04-diamond-model.md` to begin Diamond Model analysis.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Collected evidence systematically reviewed for actor identification indicators
- Known group matches identified with vendor naming cross-reference
- Actor category classified (nation-state, cybercrime, hacktivist, insider, unknown) with evidence basis
- Comprehensive actor profile built: motivation, capability, intent — each with confidence levels
- Historical campaigns documented with TTP evolution analysis
- Full ATT&CK mapping: observed techniques, historical techniques, and expected-but-not-observed techniques
- Infrastructure patterns documented with geographic caveats
- Victimology analysis performed with organizational match assessment
- Attribution confidence explicitly calibrated (high/moderate/low/insufficient) with detailed justification
- Alternative hypotheses maintained and documented with supporting/contradicting evidence
- "What would change confidence" documented for both directions
- Every attribution claim cites specific evidence with source reliability
- "So what / Who cares / What now" explicitly answered
- Frontmatter updated with all actor identification fields
- Report section populated under Threat Actor Profile
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Stating attribution without confidence level — attribution without confidence is assertion, not intelligence
- Dismissing alternative hypotheses without evidence — intellectual honesty requires maintaining alternatives
- Treating infrastructure geography as actor nationality — this is analytically unsound
- Using commodity tooling as strong attribution evidence — shared tools are weak indicators
- Not cross-referencing vendor naming conventions — consumers use different naming systems
- Not mapping ATT&CK techniques for the actor — TTP mapping drives detection engineering
- Not identifying expected-but-not-observed techniques — these are critical detection blind spots
- Not performing victimology analysis — understanding targeting patterns informs organizational risk
- Not answering "So what / Who cares / What now" — intelligence without actionable context is just data
- Building the profile from hypothesis downward instead of evidence upward (confirmation bias)
- Beginning Diamond Model analysis, Kill Chain mapping, or assessment during this step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with actor identification fields

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Attribution is one of the hardest problems in threat intelligence. Intellectual honesty, evidence rigor, and calibrated confidence are not optional — they are what separates intelligence from speculation. The actor profile drives everything downstream: Diamond Model, Kill Chain, assessment, and detection. Get it wrong here, and every subsequent step builds on a flawed foundation.
