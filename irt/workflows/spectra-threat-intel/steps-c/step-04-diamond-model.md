# Step 4: Diamond Model Analysis

**Progress: Step 4 of 8** — Next: Kill Chain & ATT&CK Mapping

## STEP GOAL:

Apply the Diamond Model of Intrusion Analysis to the collected intelligence and actor profile, constructing complete diamond events with all four core features (adversary, capability, infrastructure, victim) and meta-features (timestamp, phase, result, direction, methodology, resources). Group related events into activity threads, identify patterns across threads and historical activity, and conduct pivot analysis on shared infrastructure, capability overlaps, and victim commonalities to expand intelligence coverage and identify previously unknown relationships. The Diamond Model transforms discrete data points into a structured adversary operations model.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER construct a diamond event without all four core features populated (even if some are "unknown")
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST applying structured analytic frameworks, not filling templates
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst applying the Diamond Model of Intrusion Analysis (Caltagirone, Pendergast, Betz, 2013)
- The Diamond Model's power is in the relationships between features, not the features themselves — pivoting on shared features reveals connections invisible in flat IOC lists
- Every diamond event is a single adversary-capability-infrastructure-victim tuple — complex operations involve multiple events connected through activity threads
- Distinguish between the operator (the person or team conducting the operation) and the sponsor (the entity directing and resourcing the operation) — they may be different entities
- Meta-features provide temporal, methodological, and resource context that transforms events from snapshots into narratives

### Step-Specific Rules:

- Focus exclusively on Diamond Model event construction, meta-feature documentation, activity threading, and pivot analysis
- FORBIDDEN to begin Kill Chain mapping (step 5) or assessment (step 6) — those build on the Diamond Model
- FORBIDDEN to modify the actor profile from step 3 — Diamond Model analysis uses the profile as input
- Approach: Structured relationship modeling — each event is precise, each thread tells a story, each pivot reveals a connection
- Every event must cite evidence from the collection (step 2) and reference the actor profile (step 3)
- Unknown features must be explicitly marked as "Unknown" with notes on what would fill the gap

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Constructing diamond events with assumed features (filling in what "must be" rather than what evidence supports) produces a model that looks complete but is analytically hollow — unknown features should remain unknown until evidence fills them, because false completeness is more dangerous than acknowledged gaps
  - Treating activity threads as confirmed campaign narratives without evidence linking the events creates false pattern connections — temporal proximity alone does not establish thread membership. Events must be linked by shared features (same C2, same tool variant, same access vector) not just by timing
  - Not performing pivot analysis on shared infrastructure or capabilities wastes the Diamond Model's primary analytical power — the model was designed specifically for pivoting, and skipping pivots means treating the Diamond Model as a documentation format rather than an analytical tool
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Construct each diamond event individually with all four features and meta-features
- Group events into threads based on shared features (not assumptions)
- Perform pivots on every feature that has concrete values
- Update frontmatter: add this step name to the end of the stepsCompleted array
- FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Actor profile from step 3 (identity, capability, motivation, TTPs, attribution), processed intelligence from step 2 (IOC inventory, source findings, corroboration matrix), intelligence requirements from step 1 (PIRs)
- Focus: Diamond Model events, meta-features, activity threading, pivot analysis — no Kill Chain, no assessment, no detection content
- Limits: Diamond events are constructed from evidence — if evidence for a feature is missing, mark it unknown
- Dependencies: Threat actor profile from step-03-threat-actor.md, processed intelligence from step-02-collection.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Diamond Event Construction

For each distinct adversary action identified in the evidence, construct a diamond event. A single operation may involve multiple events (e.g., phishing email is event 1, malware execution is event 2, C2 callback is event 3, lateral movement is event 4).

"**Diamond Model Events:**

#### Event Construction Guidelines:
- Each event represents a single adversary-capability-infrastructure-victim interaction
- All four core features must be populated (use 'Unknown' with notes if evidence is insufficient)
- Each event gets a unique identifier: `DE-{{intel_id}}-{{seq}}`

#### Diamond Event Template:

```
                    ADVERSARY
                   {{operator}}
                   {{sponsor}}
                        |
                        |
    CAPABILITY ---------+--------- INFRASTRUCTURE
    {{tools/malware}}   |          {{C2/staging/hosting}}
    {{exploits}}        |          {{domains/IPs}}
    {{techniques}}      |          {{anonymization}}
                        |
                        |
                      VICTIM
                   {{org/sector}}
                   {{systems/data}}
```

For each identified event:

**Event DE-{{intel_id}}-001:**

| Feature | Value | Evidence | Confidence |
|---------|-------|----------|------------|
| **Adversary — Operator** | {{who conducted the operation}} | {{evidence}} | {{level}} |
| **Adversary — Sponsor** | {{who directed/resourced the operation}} | {{evidence}} | {{level}} |
| **Capability — Tools** | {{specific tools, malware, exploits used}} | {{evidence}} | {{level}} |
| **Capability — Techniques** | {{ATT&CK techniques employed}} | {{evidence}} | {{level}} |
| **Infrastructure — Type 1** | {{C2 servers}} — {{IP/domain}} | {{evidence}} | {{level}} |
| **Infrastructure — Type 2** | {{staging servers}} — {{IP/domain}} | {{evidence}} | {{level}} |
| **Infrastructure — Ownership** | {{dedicated / shared / compromised / leased}} | {{evidence}} | {{level}} |
| **Victim — Organization** | {{target organization}} | {{evidence}} | {{level}} |
| **Victim — Systems** | {{specific systems targeted}} | {{evidence}} | {{level}} |
| **Victim — Data** | {{data targeted or accessed}} | {{evidence}} | {{level}} |

**Event DE-{{intel_id}}-002:**
{{repeat for each event}}

**Event DE-{{intel_id}}-003:**
{{repeat for each event}}

**Total events constructed:** {{count}}"

### 2. Meta-Features Documentation

For each diamond event, document the meta-features that provide temporal, methodological, and resource context:

"**Meta-Features per Event:**

| Event ID | Timestamp | Phase | Result | Direction | Methodology | Resources |
|----------|-----------|-------|--------|-----------|-------------|-----------|
| DE-{{id}}-001 | {{UTC timestamp of the event}} | {{recon / weaponize / deliver / exploit / install / C2 / act}} | {{success / failure / unknown}} | {{adversary-to-victim / victim-to-adversary / bidirectional / infrastructure-to-infrastructure}} | {{social engineering / exploit / credential abuse / etc.}} | {{software / hardware / funds / knowledge / access}} |
| DE-{{id}}-002 | {{timestamp}} | {{phase}} | {{result}} | {{direction}} | {{methodology}} | {{resources}} |
| DE-{{id}}-003 | {{timestamp}} | {{phase}} | {{result}} | {{direction}} | {{methodology}} | {{resources}} |

**Meta-Feature Analysis:**

- **Temporal pattern:** Events span from {{earliest}} to {{latest}} ({{duration}}). The operational tempo suggests {{assessment of timing: rapid burst / methodical progression / slow and deliberate / sporadic}}.
- **Phase distribution:** {{count}} recon events, {{count}} delivery, {{count}} exploit, {{count}} install, {{count}} C2, {{count}} action. The phase concentration in {{dominant phase}} suggests {{assessment}}.
- **Result pattern:** {{success_count}} successful, {{failure_count}} failed, {{unknown_count}} unknown. The success rate suggests {{assessment of adversary competence / defender effectiveness}}.
- **Direction pattern:** {{assessment of unidirectional vs bidirectional communication patterns — indicator of C2 sophistication}}.
- **Methodology evolution:** {{whether the adversary changed methods within the operation — indicates adaptability}}."

### 3. Activity Threading

Group related diamond events into activity threads — sequences of events that represent coordinated operational phases:

"**Activity Threading:**

An activity thread is a group of diamond events connected by shared features (same adversary, same infrastructure, same capability, or same victim pathway) that represent a coherent operational sequence.

#### Thread Identification Criteria:
- Events sharing the SAME C2 infrastructure = same operational thread
- Events sharing the SAME tool/malware variant = same capability thread
- Events targeting the SAME victim system in sequence = same attack path thread
- Events with temporal proximity AND shared features = probable same thread

#### Thread T-{{intel_id}}-001: {{Thread Name}}

| Seq | Event ID | Timestamp | Phase | Description | Linking Feature |
|-----|----------|-----------|-------|-------------|----------------|
| 1 | DE-{{id}}-{{seq}} | {{timestamp}} | {{phase}} | {{description}} | — (thread origin) |
| 2 | DE-{{id}}-{{seq}} | {{timestamp}} | {{phase}} | {{description}} | {{shared feature linking to previous}} |
| 3 | DE-{{id}}-{{seq}} | {{timestamp}} | {{phase}} | {{description}} | {{shared feature linking to previous}} |

**Thread narrative:** {{one-paragraph description of what this thread represents operationally}}
**Thread confidence:** {{high/moderate/low — based on strength of linking features}}

#### Thread T-{{intel_id}}-002: {{Thread Name}}
{{repeat for each thread}}

**Threading Summary:**
- Total events: {{count}}
- Events in threads: {{count}} ({{percentage}}%)
- Unthreaded events: {{count}} ({{percentage}}%) — these may be isolated events or events lacking sufficient linking features
- Total threads: {{count}}
- Cross-thread connections: {{count}} — events or features that appear in multiple threads

**Historical Thread Links:**
If the actor has documented historical campaigns (from step 3), assess whether current threads connect to historical activity:

| Current Thread | Historical Campaign | Linking Feature | Confidence |
|----------------|-------------------|----------------|------------|
| T-{{id}}-001 | {{campaign}} | {{shared infra / tool / TTP}} | {{level}} |"

### 4. Pivot Analysis

The Diamond Model's primary analytical power is pivoting — using known features to discover unknown relationships. For each concrete feature value, pivot to discover connections:

"**Pivot Analysis:**

#### 4a. Infrastructure Pivots

For each infrastructure element (IP, domain, certificate, hosting provider), pivot to find related infrastructure and activity:

| Pivot Source | Pivot Type | Discovery | Relationship | Confidence | New IOC? |
|-------------|------------|-----------|--------------|------------|----------|
| {{IP address}} | Shared hosting / same ASN | {{other IPs on same host/ASN}} | {{related C2 / staging / unrelated}} | {{level}} | {{yes/no}} |
| {{domain}} | Passive DNS / WHOIS | {{other domains same registrant/nameserver}} | {{related infrastructure / coincidental}} | {{level}} | {{yes/no}} |
| {{SSL cert}} | Certificate transparency | {{other domains on same cert / cert chain}} | {{related infrastructure}} | {{level}} | {{yes/no}} |
| {{domain}} | Subdomain enumeration | {{subdomains / related domains}} | {{operational infrastructure}} | {{level}} | {{yes/no}} |
| {{IP address}} | Historical DNS resolution | {{domains that previously resolved here}} | {{prior operations / unrelated}} | {{level}} | {{yes/no}} |

**Infrastructure Pivot Summary:**
- Pivots performed: {{count}}
- New infrastructure discovered: {{count}} items
- New IOCs generated from pivots: {{count}}
- Connections to known campaigns: {{count}}

#### 4b. Capability Pivots

For each tool, malware sample, or exploit, pivot to find related capabilities:

| Pivot Source | Pivot Type | Discovery | Relationship | Confidence | New Intel? |
|-------------|------------|-----------|--------------|------------|-----------|
| {{malware hash}} | Code similarity (ssdeep/imphash) | {{related samples}} | {{same family / variant / unrelated}} | {{level}} | {{yes/no}} |
| {{tool name}} | YARA rule matching | {{other samples matching patterns}} | {{same build / same developer}} | {{level}} | {{yes/no}} |
| {{exploit CVE}} | Exploit DB / usage tracking | {{other actors using same exploit}} | {{shared tool / independent development}} | {{level}} | {{yes/no}} |
| {{C2 protocol}} | Beacon pattern analysis | {{other traffic matching C2 pattern}} | {{same C2 framework / generic pattern}} | {{level}} | {{yes/no}} |

**Capability Pivot Summary:**
- Pivots performed: {{count}}
- Related capabilities discovered: {{count}}
- Malware variants/family members identified: {{count}}
- Shared tooling with other actors: {{count}}

#### 4c. Victim Pivots

For each victim, pivot to find related targeting:

| Pivot Source | Pivot Type | Discovery | Relationship | Confidence |
|-------------|------------|-----------|--------------|------------|
| {{victim sector}} | Sector targeting intelligence | {{other orgs in same sector targeted}} | {{same campaign / parallel targeting}} | {{level}} |
| {{victim technology}} | Technology targeting | {{other orgs with same tech targeted}} | {{vulnerability exploitation campaign}} | {{level}} |
| {{victim geography}} | Geographic targeting | {{regional targeting patterns}} | {{geopolitical / opportunistic}} | {{level}} |

**Victim Pivot Summary:**
- Pivots performed: {{count}}
- Related targeting discovered: {{count}}
- Campaign scope expansion: {{broader than initially assessed / consistent with initial assessment}}

#### 4d. Adversary Pivots

For each adversary indicator, pivot to find related attribution:

| Pivot Source | Pivot Type | Discovery | Relationship | Confidence |
|-------------|------------|-----------|--------------|------------|
| {{actor alias}} | Cross-vendor tracking | {{additional campaigns attributed}} | {{confirms / contradicts attribution}} | {{level}} |
| {{operational pattern}} | Behavioral analysis | {{matching patterns in other ops}} | {{same operator / same training / coincidence}} | {{level}} |

**Adversary Pivot Summary:**
- Pivots performed: {{count}}
- Attribution evidence discovered: {{count}}
- Attribution confidence change: {{increased / decreased / unchanged}}"

### 5. Diamond Model Summary

"**Diamond Model Analysis Summary:**

| Metric | Value |
|--------|-------|
| Diamond events constructed | {{count}} |
| Events with all features known | {{count}} ({{percentage}}%) |
| Events with unknown features | {{count}} ({{percentage}}%) — {{which features most often unknown}} |
| Meta-features documented | {{count}} events fully documented |
| Activity threads identified | {{count}} |
| Events in threads | {{count}} / {{total}} ({{percentage}}%) |
| Historical thread links | {{count}} |
| Infrastructure pivots performed | {{count}} |
| Capability pivots performed | {{count}} |
| Victim pivots performed | {{count}} |
| Adversary pivots performed | {{count}} |
| New IOCs from pivots | {{count}} |
| New intelligence from pivots | {{count}} findings |
| Campaign scope: | {{expanded / consistent / narrowed}} from initial assessment |

**Key Findings from Diamond Model Analysis:**
1. {{finding 1 — most significant relationship discovered}}
2. {{finding 2 — most significant pattern across threads}}
3. {{finding 3 — most significant pivot discovery}}

**Remaining Unknowns:**
- {{unknown 1 — feature that remains unknown despite analysis, and what would fill it}}
- {{unknown 2 — relationship that could not be established, and why}}"

### 6. Update Frontmatter & Append to Report

**Update frontmatter:**
- Add this step name to the end of `stepsCompleted`
- `diamond_model_completed`: true
- `diamond_events`: total events constructed
- `activity_threads`: total threads identified
- `pivot_findings`: total new findings from pivot analysis
- `iocs_total`: update if new IOCs discovered from pivots
- `iocs_by_type`: update if new IOC types added

**Append to report under `## Diamond Model Analysis`:**
- Diamond Events (all events with four features and meta-features)
- Activity Threading (all threads with narratives)
- Pivot Analysis (infrastructure, capability, victim, adversary pivots)
- Infrastructure Analysis (patterns, geographic associations with caveats)

### 7. Present MENU OPTIONS

"**Diamond Model analysis complete.**

**Diamond Model Summary:**
- Events: {{event_count}} constructed ({{all_known_pct}}% with all features known)
- Activity threads: {{thread_count}} identified
- Pivots: {{total_pivot_count}} performed — {{new_ioc_count}} new IOCs, {{new_finding_count}} new findings
- Campaign scope: {{expanded / consistent / narrowed}}
- Historical links: {{link_count}} connections to prior campaigns
- Key discovery: {{most significant finding from the analysis}}

**So what:** {{what the Diamond Model reveals that was not visible from flat IOC analysis}}
**Who cares:** {{who benefits from the relationship mapping — IR team, hunt team, detection engineers}}
**What now:** {{specific actions enabled by the Diamond Model analysis — infrastructure blocking, expanded detection, hunt tasking}}

**Select an option:**
[A] Advanced Elicitation — Challenge the Diamond Model: are the activity threads supported by evidence or by narrative logic? Are the pivots finding genuine connections or coincidences? Are unknown features truly unknown or just unexamined? Could the adversary have deliberately created misleading feature relationships?
[W] War Room — Red Team: if a defender pivoted on my infrastructure, what would they find? Would I use shared hosting to create false connections? Would I embed false attribution indicators in my capabilities? Blue Team: which pivot discoveries should we operationalize immediately? Should new IOCs from pivots be pushed to detection before the full report is complete? Which activity threads suggest lateral movement paths we should hunt for?
[C] Continue — Proceed to Step 5: Kill Chain & ATT&CK Mapping (Step 5 of 8)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge every thread: is the linking feature strong enough? Could temporal proximity be coincidence? Are infrastructure pivots finding operational connections or just shared hosting? Are capability pivots matching code similarity or just common frameworks? Are there diamond events that should be in threads but are not? Are there unknown features that could be filled with additional collection? Process insights, ask operator if adjustments needed, if yes update and redisplay, if no redisplay
- IF W: War Room — Red Team perspective: the analysts mapped my operations with the Diamond Model. But did they find my backup infrastructure? Did they notice I rotated C2 between events? Would I use infrastructure that pivots cleanly to mislead analysts? Blue Team perspective: the pivots revealed new IOCs — should we deploy detection immediately or wait for confidence calibration? Which threads suggest the operation is broader than initially assessed? Should we task additional collection based on pivot findings? Summarize, redisplay menu
- IF C: Verify frontmatter updated with Diamond Model fields. Then read fully and follow: ./step-05-kill-chain.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, diamond_model_completed set to true, diamond_events, activity_threads, and pivot_findings all populated, and Diamond Model Analysis section fully populated in the output document], will you then read fully and follow: `./step-05-kill-chain.md` to begin Kill Chain and ATT&CK mapping.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Diamond events constructed for each identified adversary action with all four core features
- Unknown features explicitly marked as "Unknown" with notes on what evidence would fill them
- Adversary feature distinguishes operator from sponsor where evidence permits
- Meta-features documented for each event (timestamp, phase, result, direction, methodology, resources)
- Temporal patterns, phase distribution, and operational tempo analyzed from meta-features
- Activity threads constructed based on shared features (not assumptions or proximity alone)
- Thread narratives written as coherent operational stories
- Historical thread links assessed against prior campaigns from step 3
- Infrastructure pivots performed on IPs, domains, certificates, and hosting
- Capability pivots performed on malware, tools, and exploits
- Victim pivots performed on sector, technology, and geography
- Adversary pivots performed on attribution indicators
- New IOCs generated from pivot analysis documented and added to inventory
- Diamond Model summary with key findings and remaining unknowns
- "So what / Who cares / What now" explicitly answered
- Frontmatter updated with all Diamond Model fields
- Report section populated under Diamond Model Analysis
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Constructing diamond events with assumed features instead of marking unknowns
- Not distinguishing operator from sponsor in the adversary feature
- Not documenting meta-features — events without temporal and methodological context are snapshots, not intelligence
- Building activity threads from temporal proximity alone without shared feature evidence
- Not performing pivot analysis — this is the Diamond Model's primary analytical power
- Performing pivots but not assessing whether discoveries are genuine connections or coincidences
- Not updating the IOC inventory with new IOCs from pivots
- Not linking current threads to historical campaigns from step 3
- Not documenting remaining unknowns — unknowns inform collection gaps and confidence limits
- Treating the Diamond Model as a documentation exercise rather than an analytical tool
- Beginning Kill Chain mapping, assessment, or detection content during this step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with Diamond Model fields

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. The Diamond Model is an analytical framework, not a template to fill. Its power lies in the relationships between features and the discoveries that pivoting reveals. Treat it as a structured thinking tool, and it will reveal intelligence invisible in flat data. Treat it as a form to complete, and it adds no value.
