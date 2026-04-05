# Step 5: Kill Chain & ATT&CK Mapping

**Progress: Step 5 of 8** — Next: Intelligence Assessment

## STEP GOAL:

Reconstruct the complete attack lifecycle using both the Lockheed Martin Cyber Kill Chain (7 phases) and the Unified Kill Chain, then perform deep ATT&CK mapping at sub-technique granularity with procedure-level detail, generate an ATT&CK Navigator layer, analyze campaign context (is this part of a larger campaign?), identify detection gaps (what data sources detected activity vs what missed it), and differentiate from similar unrelated campaigns. This step transforms the actor profile and Diamond Model into a complete operational picture of the adversary's attack methodology.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER map ATT&CK techniques without citing specific evidence — speculative technique mapping produces misleading intelligence
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST reconstructing adversary operations, not generating a generic ATT&CK matrix
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst mapping the adversary's operational methodology to structured kill chain and ATT&CK frameworks
- Kill Chain reconstruction tells the story of HOW the attack unfolded — it must be evidence-based and temporally accurate
- ATT&CK mapping must be at sub-technique granularity where evidence supports it — T1059 is less useful than T1059.001 (PowerShell)
- Every technique mapped must include the specific procedure (how THIS adversary used THIS technique) — generic descriptions add no intelligence value
- Detection gap analysis is as important as detection coverage — what was MISSED tells you where to invest in detection engineering
- Campaign analysis extends the lens beyond this single operation — is this one battle in a larger war?

### Step-Specific Rules:

- Focus exclusively on Kill Chain reconstruction, ATT&CK deep mapping, Navigator layer generation, campaign analysis, and detection gap assessment
- FORBIDDEN to begin intelligence assessment (step 6), IOC packaging (step 7), or dissemination (step 8) — those build on this mapping
- FORBIDDEN to map techniques speculatively — if there is no evidence of a technique, do not map it. Note it as "not detected" instead
- Approach: Evidence-based operational reconstruction with granular technique mapping and honest gap assessment
- Reference the Diamond Model events (step 4) and actor profile (step 3) for context, but base the mapping on collected evidence (step 2)

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Mapping ATT&CK techniques based on what the actor "usually does" rather than what evidence shows they did in THIS operation conflates historical capability with current activity — the actor may have used different techniques, adapted to your environment, or been limited by your defenses. Map what you observe, not what you expect
  - Not identifying detection gaps alongside detection coverage creates a false sense of security — knowing which techniques were detected is only half the picture. The techniques that were NOT detected represent current blind spots that the adversary can exploit again, and the detection engineering team needs this gap analysis to prioritize rule development
  - Treating every related activity as part of the same campaign without evidence of coordination inflates campaign scope and may trigger disproportionate response — campaigns are defined by shared objectives, coordinated timing, and operational infrastructure linkage, not just similar IOCs or TTPs
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Build Kill Chain from evidence, then validate against the Diamond Model timeline
- Map ATT&CK techniques with evidence citations for each
- Identify gaps between expected and observed techniques
- Update frontmatter: add this step name to the end of the stepsCompleted array
- FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Diamond Model events and threads (step 4), actor profile with historical TTPs (step 3), processed intelligence and IOC inventory (step 2), PIRs (step 1)
- Focus: Kill Chain reconstruction, ATT&CK mapping, Navigator layer, campaign analysis, detection gaps — no assessment, no IOC packaging, no dissemination
- Limits: Mapping is limited to evidence-supported techniques. Expected-but-not-observed techniques are documented as gaps, not as confirmed activity
- Dependencies: Diamond Model from step-04-diamond-model.md, actor profile from step-03-threat-actor.md, evidence from step-02-collection.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Lockheed Martin Kill Chain Reconstruction

Reconstruct the attack through the 7 phases of the Lockheed Martin Cyber Kill Chain, using evidence from the collection and Diamond Model:

"**Lockheed Martin Cyber Kill Chain Reconstruction:**

#### Phase 1: Reconnaissance
- **What the adversary learned before acting:**
- Evidence: {{specific evidence of reconnaissance activity or 'Not directly observed — reconnaissance typically occurs outside victim visibility'}}
- Sources: {{data sources that would detect reconnaissance}}
- Diamond Events: {{DE-{{id}}-{{seq}} if applicable}}
- Assessment: {{what can be inferred about reconnaissance from the nature of the attack}}

#### Phase 2: Weaponization
- **What the adversary prepared:**
- Evidence: {{specific evidence of weaponization — malware compilation timestamps, document creation dates, exploit packaging}}
- Tools created/modified: {{tool inventory with evidence}}
- Infrastructure prepared: {{staging, C2, exfil infrastructure with evidence}}
- Diamond Events: {{DE-{{id}}-{{seq}} if applicable}}
- Assessment: {{level of preparation suggests {{sophistication assessment}}}

#### Phase 3: Delivery
- **How the adversary delivered the weapon:**
- Delivery method: {{email / web / USB / supply chain / watering hole / other}}
- Evidence: {{specific evidence — email headers, web logs, infection vector artifacts}}
- Timeline: {{delivery timestamp(s)}}
- Diamond Events: {{DE-{{id}}-{{seq}}}}
- Success/Failure: {{delivery attempts: {{success_count}} succeeded, {{failure_count}} failed}}

#### Phase 4: Exploitation
- **How the adversary gained execution:**
- Vulnerability exploited: {{CVE if applicable, or technique — social engineering, credential abuse, etc.}}
- Evidence: {{exploitation artifacts — process creation, vulnerability trigger logs, user action}}
- Timeline: {{exploitation timestamp(s)}}
- Diamond Events: {{DE-{{id}}-{{seq}}}}
- Assessment: {{exploitation sophistication}}

#### Phase 5: Installation
- **How the adversary established persistence:**
- Persistence mechanisms: {{registry keys, scheduled tasks, services, web shells, implants, cron jobs}}
- Evidence: {{specific artifacts for each mechanism}}
- Timeline: {{installation timestamp(s)}}
- Diamond Events: {{DE-{{id}}-{{seq}}}}
- Assessment: {{persistence sophistication and redundancy}}

#### Phase 6: Command & Control
- **How the adversary maintained communication:**
- C2 channels: {{protocols, destinations, beacon intervals, encryption}}
- Evidence: {{network traffic, DNS queries, process behavior}}
- Timeline: {{C2 establishment and duration}}
- Diamond Events: {{DE-{{id}}-{{seq}}}}
- Assessment: {{C2 sophistication — custom vs commodity, evasion techniques}}

#### Phase 7: Actions on Objectives
- **What the adversary accomplished (or attempted):**
- Objectives achieved: {{data access, data theft, lateral movement, privilege escalation, destruction, etc.}}
- Evidence: {{specific evidence of objective completion or attempt}}
- Timeline: {{action timestamps}}
- Diamond Events: {{DE-{{id}}-{{seq}}}}
- Assessment: {{objective completion status — achieved / partially achieved / attempted but failed}}

**Kill Chain Coverage:**

| Phase | Status | Evidence Strength | Detection Source |
|-------|--------|-------------------|-----------------|
| Reconnaissance | {{Observed / Inferred / Not detected}} | {{Strong / Moderate / Weak / None}} | {{what detected it}} |
| Weaponization | {{Observed / Inferred / Not detected}} | {{level}} | {{source}} |
| Delivery | {{Observed / Inferred / Not detected}} | {{level}} | {{source}} |
| Exploitation | {{Observed / Inferred / Not detected}} | {{level}} | {{source}} |
| Installation | {{Observed / Inferred / Not detected}} | {{level}} | {{source}} |
| Command & Control | {{Observed / Inferred / Not detected}} | {{level}} | {{source}} |
| Actions on Objectives | {{Observed / Inferred / Not detected}} | {{level}} | {{source}} |

**Phases with strong evidence:** {{count}} / 7
**Phases inferred:** {{count}} / 7
**Phases not detected:** {{count}} / 7"

### 2. Unified Kill Chain Mapping

Map to the extended Unified Kill Chain (18 phases) for more granular coverage:

"**Unified Kill Chain Mapping:**

The Unified Kill Chain extends the Lockheed Martin model with specific phases for network propagation and action on objectives:

#### Initial Foothold Phases:
| Phase | Activity | Evidence | Diamond Event |
|-------|----------|----------|---------------|
| Reconnaissance | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Weaponization | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Social Engineering | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Exploitation | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Persistence | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Defense Evasion | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Command & Control | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |

#### Network Propagation Phases:
| Phase | Activity | Evidence | Diamond Event |
|-------|----------|----------|---------------|
| Pivoting | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Discovery | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Privilege Escalation | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Execution | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Credential Access | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Lateral Movement | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |

#### Action on Objectives Phases:
| Phase | Activity | Evidence | Diamond Event |
|-------|----------|----------|---------------|
| Collection | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Exfiltration | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Impact | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |
| Objectives | {{activity}} | {{evidence or 'Not observed'}} | {{event ID}} |

**Unified Kill Chain Coverage:** {{observed_phases}} / 18 phases with evidence"

### 3. ATT&CK Deep Mapping

Map every observed technique to MITRE ATT&CK at sub-technique granularity:

"**MITRE ATT&CK Deep Mapping:**

For each technique observed in the evidence, document at procedure level:

| # | ATT&CK ID | Technique | Sub-Technique | Tactic | Procedure (How THIS Actor Used It) | Evidence | Data Source That Detected | Confidence |
|---|-----------|-----------|---------------|--------|-----------------------------------|----------|--------------------------|------------|
| 1 | {{T-code}} | {{name}} | {{sub-technique or N/A}} | {{tactic(s)}} | {{specific procedure — command lines, tool parameters, behavioral pattern}} | {{evidence citation}} | {{SIEM / EDR / NDR / logs / forensic artifact}} | {{high/moderate/low}} |
| 2 | {{T-code}} | {{name}} | {{sub-technique or N/A}} | {{tactic(s)}} | {{specific procedure}} | {{evidence}} | {{data source}} | {{confidence}} |

**ATT&CK Mapping Statistics:**

| Tactic | Techniques Observed | Sub-Techniques | Confidence Distribution |
|--------|--------------------|-----------------|-----------------------|
| Reconnaissance (TA0043) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Resource Development (TA0042) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Initial Access (TA0001) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Execution (TA0002) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Persistence (TA0003) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Privilege Escalation (TA0004) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Defense Evasion (TA0005) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Credential Access (TA0006) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Discovery (TA0007) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Lateral Movement (TA0008) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Collection (TA0009) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Command and Control (TA0011) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Exfiltration (TA0010) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| Impact (TA0040) | {{count}} | {{count}} | H:{{n}} M:{{n}} L:{{n}} |
| **TOTAL** | **{{total}}** | **{{total}}** | |

**Technique Confidence Summary:**
- High confidence techniques: {{count}} ({{percentage}}%) — corroborated by multiple evidence sources
- Moderate confidence techniques: {{count}} ({{percentage}}%) — supported by single strong source
- Low confidence techniques: {{count}} ({{percentage}}%) — inferred or circumstantial evidence"

### 4. ATT&CK Navigator Layer

Generate an ATT&CK Navigator layer JSON for visual representation:

"**ATT&CK Navigator Layer:**

```json
{
  \"name\": \"{{intel_id}} — {{actor_name}} Technique Coverage\",
  \"versions\": {
    \"attack\": \"15\",
    \"navigator\": \"5.0\",
    \"layer\": \"4.5\"
  },
  \"domain\": \"enterprise-attack\",
  \"description\": \"ATT&CK techniques observed in {{intel_id}} attributed to {{actor_name}} ({{attribution_confidence}} confidence)\",
  \"filters\": {
    \"platforms\": [\"Windows\", \"Linux\", \"macOS\", \"Azure AD\", \"Office 365\", \"Google Workspace\", \"SaaS\", \"IaaS\", \"Network\", \"Containers\"]
  },
  \"sorting\": 0,
  \"layout\": {
    \"layout\": \"side\",
    \"aggregateFunction\": \"average\",
    \"showID\": true,
    \"showName\": true,
    \"showAggregateScores\": false,
    \"countUnscored\": false
  },
  \"hideDisabled\": false,
  \"techniques\": [
    {
      \"techniqueID\": \"{{T-code}}\",
      \"tactic\": \"{{tactic-slug}}\",
      \"color\": \"{{#ff6666 for high confidence / #ffcc66 for moderate / #ffff66 for low}}\",
      \"comment\": \"{{procedure description — how the actor used this technique}}\",
      \"enabled\": true,
      \"metadata\": [
        {\"name\": \"evidence\", \"value\": \"{{evidence summary}}\"},
        {\"name\": \"confidence\", \"value\": \"{{high/moderate/low}}\"},
        {\"name\": \"data_source\", \"value\": \"{{what detected it}}\"}
      ],
      \"links\": [],
      \"showSubtechniques\": true
    }
  ],
  \"gradient\": {
    \"colors\": [\"#ffff66\", \"#ffcc66\", \"#ff6666\"],
    \"minValue\": 1,
    \"maxValue\": 3
  },
  \"legendItems\": [
    {\"label\": \"High Confidence\", \"color\": \"#ff6666\"},
    {\"label\": \"Moderate Confidence\", \"color\": \"#ffcc66\"},
    {\"label\": \"Low Confidence\", \"color\": \"#ffff66\"}
  ],
  \"metadata\": [
    {\"name\": \"intel_id\", \"value\": \"{{intel_id}}\"},
    {\"name\": \"actor\", \"value\": \"{{actor_name}}\"},
    {\"name\": \"attribution_confidence\", \"value\": \"{{confidence}}\"},
    {\"name\": \"created\", \"value\": \"{{date}}\"}
  ],
  \"showTacticRowBackground\": true,
  \"tacticRowBackground\": \"#dddddd\",
  \"selectTechniquesAcrossTactics\": true,
  \"selectSubtechniquesWithParent\": false,
  \"selectVisibleTechniques\": false
}
```

**Layer Usage Notes:**
- Import this JSON into the MITRE ATT&CK Navigator (https://mitre-attack.github.io/attack-navigator/)
- Color coding: Red = high confidence, Orange = moderate, Yellow = low
- Comments contain procedure details for each technique
- This layer can be overlaid with the organization's detection coverage layer to identify gaps"

### 5. Detection Gap Assessment

Identify what was detected versus what was missed:

"**Detection Gap Assessment:**

#### Data Sources That Detected Activity:

| Data Source | Techniques Detected | Detection Method | Latency |
|-------------|-------------------|------------------|---------|
| {{SIEM}} | {{T-codes}} | {{rule/alert/correlation}} | {{time from activity to detection}} |
| {{EDR}} | {{T-codes}} | {{behavioral/signature}} | {{latency}} |
| {{NDR}} | {{T-codes}} | {{traffic analysis/signature}} | {{latency}} |
| {{Other}} | {{T-codes}} | {{method}} | {{latency}} |

#### Data Sources That MISSED Activity:

| ATT&CK Technique | Expected Data Source | Why It Was Missed | Impact | Recommendation |
|-------------------|---------------------|-------------------|--------|----------------|
| {{T-code}} | {{data source}} | {{not deployed / misconfigured / evasion / log gap / insufficient coverage}} | {{technique went undetected for {{duration}}}} | {{specific recommendation to close the gap}} |

#### Techniques Not Detected at All:
Based on the actor profile (step 3) and historical TTPs, these techniques are EXPECTED for this actor but were NOT detected in any data source:

| ATT&CK ID | Technique | Why Expected | Possible Explanations | Priority for Detection |
|------------|-----------|--------------|----------------------|----------------------|
| {{T-code}} | {{name}} | {{actor historically uses this}} | {{not used / detection gap / evasion}} | {{critical / high / medium}} |

**Detection Gap Summary:**

| Category | Count |
|----------|-------|
| Techniques detected by at least one source | {{count}} |
| Techniques detected by multiple sources | {{count}} |
| Techniques detected by ONLY one source | {{count}} — {{single point of detection failure risk}} |
| Techniques NOT detected by any source | {{count}} — {{critical blind spots}} |
| Expected techniques not observed | {{count}} — {{may indicate evasion or gap}} |"

### 6. Campaign Analysis

"**Campaign Analysis:**

#### Is This Part of a Larger Campaign?

A campaign is a coordinated series of intrusion activities with shared objectives, infrastructure, and timing. Assess whether the current activity is an isolated operation or part of a broader campaign:

**Campaign Indicators:**

| Indicator | Evidence For | Evidence Against | Assessment |
|-----------|-------------|------------------|------------|
| **Shared infrastructure** with other operations | {{evidence}} | {{counter-evidence}} | {{supports / does not support campaign}} |
| **Shared tooling** across operations | {{evidence}} | {{counter-evidence}} | {{supports / does not support}} |
| **Coordinated timing** with other incidents | {{evidence}} | {{counter-evidence}} | {{supports / does not support}} |
| **Common targeting** pattern (sector/geography) | {{evidence}} | {{counter-evidence}} | {{supports / does not support}} |
| **Consistent objectives** across operations | {{evidence}} | {{counter-evidence}} | {{supports / does not support}} |
| **Operational continuity** (progressive escalation) | {{evidence}} | {{counter-evidence}} | {{supports / does not support}} |

**Campaign Assessment:**
- **Conclusion:** {{This IS part of a campaign / This MAY be part of a campaign / This appears to be an isolated operation}}
- **Confidence:** {{high/moderate/low}}
- **Evidence basis:** {{summary of key evidence supporting the conclusion}}

#### If Campaign Identified:

**Campaign Profile:**

| Attribute | Assessment | Evidence |
|-----------|------------|----------|
| Campaign name/ID | {{name or assign provisional ID}} | — |
| Campaign timeframe | {{start — ongoing/end}} | {{temporal evidence}} |
| Campaign scope | {{number of targets / sectors / regions}} | {{targeting evidence}} |
| Campaign objectives | {{strategic / financial / espionage / destructive}} | {{objective evidence}} |
| Campaign evolution | {{stable / escalating / de-escalating / adapting}} | {{evolution evidence}} |
| Our position in campaign | {{early target / recent target / target of opportunity}} | {{timing evidence}} |

**Campaign Timeline:**

| Date/Period | Activity | Target | Relation to Our Operation |
|-------------|----------|--------|--------------------------|
| {{date}} | {{activity}} | {{target}} | {{how it relates}} |

#### Differentiation from Similar Unrelated Campaigns:

| Similar Campaign | Similarities | Key Differences | Why Unrelated |
|-----------------|-------------|-----------------|---------------|
| {{campaign}} | {{what looks similar}} | {{what is different}} | {{why we assess it as separate}} |"

### 7. Update Frontmatter & Append to Report

**Update frontmatter:**
- Add this step name to the end of `stepsCompleted`
- `kill_chain_mapped`: true
- `kill_chain_phases_covered`: number of phases with evidence (out of 7 for LM, out of 18 for UKC)
- `mitre_techniques`: updated complete array of all T-codes
- `mitre_technique_count`: total unique techniques mapped
- `attack_pattern_gaps`: array of expected-but-not-detected technique IDs
- `campaigns_identified`: array of campaign names/IDs
- `campaign_count`: number of campaigns identified
- `campaign_timespan`: start-to-end of identified campaign

**Append to report under `## Kill Chain & ATT&CK Mapping`:**
- Kill Chain Reconstruction (LM 7-phase and UKC 18-phase)
- ATT&CK Deep Mapping (full technique table with procedures)
- ATT&CK Navigator Layer (JSON)
- Campaign Analysis
- Detection Gap Assessment

### 8. Present MENU OPTIONS

"**Kill Chain and ATT&CK mapping complete.**

**Mapping Summary:**
- Kill Chain (Lockheed Martin): {{observed_phases}} / 7 phases with evidence
- Kill Chain (Unified): {{observed_phases}} / 18 phases with evidence
- ATT&CK techniques mapped: {{total_count}} ({{high_count}} high, {{moderate_count}} moderate, {{low_count}} low confidence)
- Sub-techniques: {{sub_count}} at sub-technique granularity
- Detection coverage: {{detected_count}} techniques detected | {{missed_count}} missed | {{expected_not_observed}} expected but not observed
- Campaign assessment: {{campaign / possible campaign / isolated operation}} ({{confidence}} confidence)
- Navigator layer: generated for import

**So what:** {{what the Kill Chain and ATT&CK mapping reveals about the adversary's operational capability and our detection posture}}
**Who cares:** {{detection engineers need the gap assessment, hunt teams need the expected-but-not-observed techniques, IR teams need the Kill Chain reconstruction}}
**What now:** {{specific actions — gap remediation priorities, hunt task generation, detection rule development targets}}

**Select an option:**
[A] Advanced Elicitation — Challenge the mapping: are techniques mapped based on evidence or inference? Is the Kill Chain reconstruction complete or are there phases built on assumption? Could the campaign assessment be wrong — are we seeing a pattern that is not there, or missing a pattern that is?
[W] War Room — Red Team: the defenders mapped my Kill Chain — but did they find my fallback delivery mechanism? Did they notice the phase I deliberately made noisy to distract from the quiet one? If my campaign is broader than they think, what else should they be looking for? Blue Team: given the detection gaps, what is the quickest path to closing the most critical blind spots? Which techniques should we build detection rules for FIRST? Should we task a threat hunt based on the expected-but-not-observed techniques?
[C] Continue — Proceed to Step 6: Intelligence Assessment & Analytic Products (Step 6 of 8)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge each technique mapping: is the evidence strong enough? Are any techniques mapped from a single weak source? Is the Kill Chain reconstruction supported by the timeline or does it have temporal gaps? Is the campaign assessment based on genuine coordination indicators or surface-level similarity? Are the detection gaps real gaps or artifact of collection limitations? Process insights, update if needed, redisplay menu
- IF W: War Room — Red Team perspective: the defenders think they found my full Kill Chain. But did they find my reconnaissance? Do they know my full C2 infrastructure? Is my "Actions on Objectives" phase complete or am I still executing? If I know they are building detection for my techniques, what would I change? Blue Team perspective: given the detection gap assessment, what are the quick wins? Which Sigma/YARA rules can we build from the procedure details? Should we overlay the Navigator layer with our existing detection coverage? What hunt hypotheses emerge from the expected-but-not-observed techniques? Summarize, redisplay menu
- IF C: Verify frontmatter updated with Kill Chain and ATT&CK fields. Then read fully and follow: ./step-06-assessment.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, kill_chain_mapped set to true, kill_chain_phases_covered, mitre_techniques, mitre_technique_count, attack_pattern_gaps, campaigns_identified, campaign_count, and campaign_timespan all updated, and Kill Chain & ATT&CK Mapping section fully populated in the output document], will you then read fully and follow: `./step-06-assessment.md` to begin intelligence assessment.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Lockheed Martin Kill Chain reconstructed across all 7 phases with evidence citations for observed phases
- Unified Kill Chain mapped across 18 phases for granular coverage
- Each Kill Chain phase documented with evidence, timeline, Diamond Event references, and detection sources
- ATT&CK mapping at sub-technique granularity with procedure-level detail for each technique
- Every mapped technique cites specific evidence and identifies the data source that detected it
- ATT&CK statistics calculated per tactic with confidence distribution
- ATT&CK Navigator layer JSON generated with confidence color coding and procedure comments
- Detection gap assessment performed: what was detected vs what was missed vs what was expected but not observed
- Single-point-of-detection-failure techniques identified (detected by only one source)
- Campaign analysis performed with evidence-based assessment (campaign / possible campaign / isolated)
- Campaign differentiated from similar unrelated campaigns where applicable
- "So what / Who cares / What now" explicitly answered with specific actions
- Frontmatter updated with all Kill Chain and ATT&CK fields
- Report section populated under Kill Chain & ATT&CK Mapping
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Mapping ATT&CK techniques without evidence citations — speculative mapping produces misleading intelligence
- Mapping at technique level when sub-technique evidence exists — T1059 is less useful than T1059.001
- Not providing procedure details — generic technique descriptions add no intelligence value for detection engineering
- Not identifying detection gaps — detection coverage without gap analysis gives false confidence
- Not documenting expected-but-not-observed techniques — these are the most critical gaps
- Not generating the Navigator layer — visual representation is essential for stakeholder communication
- Not performing campaign analysis — isolated operations have different response implications than campaigns
- Conflating similar activity with coordinated campaigns without evidence of coordination
- Building Kill Chain from assumption rather than evidence — inferred phases must be marked as inferred
- Beginning intelligence assessment, IOC packaging, or dissemination during this step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with Kill Chain and ATT&CK fields

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. The Kill Chain and ATT&CK mapping are the operational blueprint of the adversary's methodology. Every technique must be evidence-based. Every gap must be acknowledged. This mapping drives detection engineering, hunt tasking, and defensive prioritization — it must be accurate, granular, and honest about what we know versus what we do not know.
