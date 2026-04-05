# Step 1: Intelligence Requirement & Collection Planning

**Progress: Step 1 of 8** — Next: Intelligence Collection

## STEP GOAL:

Verify the active engagement, intake the intelligence trigger from the operator (incident-driven, IOC-driven, advisory-driven, RFI-driven, proactive, or environmental), define Priority Intelligence Requirements (PIRs) and Standing Intelligence Requirements (SIRs), classify the intelligence type (tactical/operational/strategic), build a collection plan with source identification and Admiralty Scale reliability ratings, assign the intelligence ID, and create the intelligence report workspace. This is the gateway step — no intelligence production may begin without confirmed authorization, a validated intelligence requirement, a collection plan, and operator acknowledgment.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER proceed without verified engagement authorization
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST, not an autonomous data collection engine
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst producing finished intelligence products under NIST, Diamond Model, Kill Chain, and MITRE ATT&CK frameworks
- Every assessment must include a confidence level (high, moderate, low) and source attribution — unsourced claims are not intelligence
- Intelligence without context is just data. Every finding must answer: "So what? Who cares? What now?"
- When in doubt about scope, classification, or dissemination authority, ASK. Never assume permission
- Intelligence documentation is a decision-support artifact — accuracy, calibrated confidence, and analytic rigor are non-negotiable

### Step-Specific Rules:

- Focus only on engagement verification, intelligence trigger intake, PIR/SIR definition, intel type classification, collection planning, source reliability assessment, ID assignment, and workspace setup — no collection, analysis, or production activity yet
- FORBIDDEN to look ahead to future steps or assume knowledge from them
- Approach: Calm, methodical intelligence tradecraft with structured requirements elicitation and clear reporting to operator
- Detect existing workflow state and handle continuation properly
- If engagement is missing or invalid: HARD STOP — no exceptions
- Intelligence trigger data is mandatory — cannot proceed without at minimum a trigger source and initial requirement
- Record the intelligence requirement timestamp as the official start of the intelligence cycle

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Proceeding without clearly defined Priority Intelligence Requirements (PIRs) risks producing intelligence that answers no one's questions — unfocused collection wastes time and resources, and the resulting product will lack the precision that decision-makers need to act
  - Classifying intelligence type (tactical/operational/strategic) incorrectly misroutes the product to the wrong audience — tactical IOC feeds sent to executives are noise, and strategic assessments sent to SOC analysts lack the actionable specificity they need for detection engineering
  - Skipping source reliability assessment (Admiralty Scale) when multiple sources are available produces intelligence of unknown quality — without reliability ratings, the consumer cannot distinguish high-confidence findings from uncorroborated single-source claims, which directly undermines trust in the product
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Show your analysis of current state before taking any action
- Initialize document structure and update frontmatter appropriately
- Update frontmatter: add this step name to the end of the stepsCompleted array (it should be the first entry since this is step 1)
- Record the intelligence requirement timestamp as the official start of the intelligence cycle
- FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md are available in memory, engagement.yaml is loaded, prior analysis reports (incident-handling, forensics, malware, alert-triage, threat-hunt) may be available
- Focus: Authorization verification, intelligence trigger intake, PIR/SIR definition, intel type classification, collection planning, source reliability assessment, ID assignment, and workspace setup only
- Limits: Don't assume knowledge from other steps or begin any collection, processing, analysis, or production activity
- Dependencies: Configuration loaded from workflow.md initialization, engagement.yaml verified, operator provides intelligence trigger and requirements

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Check for Existing Workflow State

First, check if the output document already exists:

**Workflow State Detection:**

- Look for file at `{outputFile}`
- If exists, read the complete file including frontmatter
- If not exists, this is a fresh workflow — proceed to engagement verification

### 2. Handle Continuation (If Document Exists)

If the document exists and has frontmatter with `stepsCompleted` BUT `step-08-dissemination.md` is NOT in the list, follow the Continuation Protocol since the document is incomplete:

**Continuation Protocol:**

- **STOP immediately** and load `./step-01b-continue.md`
- Do not proceed with any initialization tasks
- Let step-01b handle all continuation logic
- This is an auto-proceed situation — no user choice needed

### 3. Verify Engagement Authorization (If Fresh Workflow)

If no document exists or no `stepsCompleted` in frontmatter:

#### A. Engagement File Verification

The engagement.yaml should already be loaded from workflow.md initialization. Verify the following and report:

**Authorization Checks:**

| Check | Requirement | Status |
|-------|------------|--------|
| File exists | engagement.yaml present | Pass/Fail |
| Status active | `status: active` | Pass/Fail |
| Dates valid | start_date <= today <= end_date | Pass/Fail |
| Intel authorized | Engagement permits intelligence operations (incident-response, blue-team, purple-team, or threat-intel) | Pass/Fail |
| External queries authorized | RoE permits querying external threat intelligence sources (OSINT, commercial feeds, ISACs) | Pass/Fail |
| Internal telemetry authorized | RoE permits accessing internal telemetry (SIEM, EDR, network logs) | Pass/Fail |
| Scope defined | At least one target system, network, or organizational unit in scope | Pass/Fail |

**If ANY of the first four checks fail:** HALT IMMEDIATELY.

"**AUTHORIZATION BLOCK**

The engagement does not meet the requirements for intelligence operations:
- {{list of failed checks}}

Required actions:
- If no engagement exists: run `spectra-new-engagement` to create an authorized engagement with threat intelligence scope
- If the engagement has expired: contact the engagement lead for renewal — intelligence production timelines depend on current authorization
- If scope is empty: update engagement.yaml with authorized systems and organizational units
- If intelligence operations are not authorized: the engagement type must permit incident-response, blue-team, purple-team, or threat-intel operations

No intelligence production activity will be executed without complete authorization."

**Do NOT proceed. This is a hard stop.**

#### B. Note Intelligence Restrictions (If Any)

If the engagement authorizes intelligence operations but restricts specific activities:

- Document each restriction clearly: e.g., "No dark web collection without CISO approval", "External sharing restricted to TLP:AMBER", "No commercial feed queries — budget not allocated"
- These restrictions will be enforced in step-02-collection.md and step-08-dissemination.md
- Present restrictions to the operator:

"**Intelligence Activity Restrictions Identified:**

| Restriction | Source (RoE Clause) | Impact on Collection/Dissemination |
|-------------|---------------------|-------------------------------------|
| {{restriction}} | {{roe_clause}} | {{how this affects intelligence production}} |

These restrictions will be enforced during collection and dissemination phases. Acknowledge?"

### 4. Intelligence Trigger Intake

This is the core of Step 1. Gather the intelligence trigger and requirements from the operator through structured elicitation. For each category, ask explicitly and wait for the operator's response.

#### A. Trigger Classification

Ask the operator to identify what triggered this intelligence production:

"**What triggered this intelligence requirement?** Select the primary trigger type:

1. **Incident-Driven** — Active or recent security incident requires threat intelligence context (actor profiling, campaign assessment, IOC enrichment)
2. **IOC-Driven** — New indicators of compromise received that need analysis, enrichment, and contextualization
3. **Advisory-Driven** — Government advisory (CISA, FBI, NSA, NCSC, ANSSI, BSI) or vendor report requires organizational impact assessment
4. **RFI-Driven** — Request for Information from stakeholder (CISO, board, legal, SOC, IR team) requires a specific intelligence product
5. **Proactive** — Standing intelligence requirement or scheduled landscape assessment (not triggered by a specific event)
6. **Environmental** — Change in threat landscape, geopolitical event, industry-specific threat, or supply chain concern requiring assessment

Which trigger, and provide details?"

Record: trigger type, trigger source (who/what initiated), trigger timestamp, urgency assessment, any reference IDs (incident ID, advisory ID, RFI ticket number).

#### B. Intelligence Trigger Details

Based on the trigger type selected, gather specific context:

**If Incident-Driven:**
"Provide the incident context:
- **Incident ID**: Reference to the incident handling report (if spectra-incident-handling was run)
- **Key IOCs**: IP addresses, domains, file hashes, email addresses, URLs from the incident
- **ATT&CK techniques observed**: Any MITRE techniques identified during incident response
- **Affected systems/data**: What was targeted or compromised
- **Timeline**: When did the incident start, when was it detected, current status
- **Specific questions**: What does the incident team need intelligence on? (actor identity, campaign scope, future actions, related targets)"

**If IOC-Driven:**
"Provide the indicator context:
- **IOC list**: All indicators with type classification (IP, domain, hash, URL, email, etc.)
- **Source of IOCs**: Where did these indicators come from? (ISAC feed, vendor alert, partner sharing, internal detection)
- **First seen / Last seen**: When were these indicators first and last observed
- **Context**: What activity were these indicators associated with? (C2 traffic, phishing, malware delivery, exfiltration)
- **Specific questions**: What needs to be determined? (Attribution, campaign scope, active/historical status, related infrastructure)"

**If Advisory-Driven:**
"Provide the advisory context:
- **Advisory ID**: e.g., CISA AA22-174A, FBI PIN, NCSC Advisory
- **Issuing authority**: Which organization published the advisory
- **Date published**: When was the advisory released
- **Threat actor / Campaign**: Who or what is the advisory about
- **Affected products / CVEs**: Any specific vulnerabilities or software referenced
- **Specific questions**: What does the organization need to know? (Are we targeted? Are we vulnerable? What defenses do we need?)"

**If RFI-Driven:**
"Provide the RFI context:
- **Requestor**: Who is asking? (CISO, board member, legal, SOC manager, IR lead, external partner)
- **RFI text**: What is the exact question or information need?
- **Deadline**: When is the response needed?
- **Classification**: What TLP level is appropriate for the response?
- **Audience**: Who will consume this intelligence product? (executive, technical, operational)
- **Decision**: What decision will this intelligence inform?"

**If Proactive:**
"Provide the proactive assessment context:
- **Focus area**: What threat category or actor group is the focus? (nation-state, ransomware, supply chain, sector-specific)
- **Standing requirement**: Is this fulfilling an existing SIR? Which one?
- **Assessment period**: What time window should this assessment cover?
- **Comparison baseline**: Is there a previous assessment to compare against?
- **Audience**: Who will consume this product?"

**If Environmental:**
"Provide the environmental context:
- **Environmental change**: What changed? (geopolitical event, new threat group, industry breach, supply chain compromise, regulatory change)
- **Relevance to organization**: Why does this change matter to us? (we use the affected technology, we operate in the affected region, our sector is being targeted)
- **Urgency**: Is this an emerging threat requiring immediate assessment or a strategic landscape shift?
- **Specific questions**: What do we need to assess? (exposure, risk, required defensive changes)"

Record all trigger details for downstream steps.

#### C. Cross-Module Context Loading

Check for existing analysis reports that provide pre-processed intelligence:

**Search and load (if available):**

| Source | Path | Data to Extract |
|--------|------|-----------------|
| Incident Handling | `{irt_artifacts}/incident-handling/` | IOCs, ATT&CK techniques, timeline, affected systems, root cause |
| Digital Forensics | `{irt_artifacts}/forensics/` | Forensic artifacts, malware indicators, timeline data, evidence |
| Malware Analysis | `{irt_artifacts}/malware/` | Malware capabilities, C2 infrastructure, YARA signatures, behavioral profile |
| Alert Triage | `{irt_artifacts}/../soc/` | Alert classification, enriched IOCs, initial ATT&CK mapping |
| Threat Hunt | `{irt_artifacts}/../soc/` | Hunt findings, hypothesis results, detection gaps |

**If reports found:**
"**Cross-Module Intelligence Sources Loaded:**

| Source Report | Type | Key Data | IOCs | ATT&CK Techniques |
|---------------|------|----------|------|---------------------|
| {{report_id}} | {{type}} | {{summary}} | {{ioc_count}} | {{technique_list}} |

This pre-processed data provides a warm start for intelligence production. Cross-references between reports have been flagged."

**If no reports found:**
"**No prior analysis reports found.** Intelligence production will proceed from cold start — you will provide the intelligence trigger and raw indicators directly. Loading completed analysis reports (incident-handling, forensics, malware-analysis, alert-triage, threat-hunt) provides pre-processed data that accelerates intelligence production."

Do NOT block on absence — allow the operator to proceed with cold-start intelligence production.

### 5. Priority Intelligence Requirements (PIRs)

Define the specific questions that this intelligence production must answer. PIRs are the backbone of focused intelligence — every collection action, every analysis, every assessment must trace back to a PIR.

"**Define Priority Intelligence Requirements (PIRs):**

PIRs are the specific questions this intelligence product must answer. They drive collection, focus analysis, and determine the success criteria for the finished product.

Based on the trigger context, I recommend the following PIRs. Confirm, modify, or add:

**Recommended PIRs:**

| # | PIR | Priority | Rationale |
|---|-----|----------|-----------|
| PIR-1 | {{recommended question based on trigger}} | Critical / High / Medium | {{why this question matters}} |
| PIR-2 | {{recommended question based on trigger}} | Critical / High / Medium | {{why this question matters}} |
| PIR-3 | {{recommended question based on trigger}} | Critical / High / Medium | {{why this question matters}} |

**Standard PIR Templates by Trigger Type:**

*Incident-Driven:*
- Who is the threat actor and what is their motivation?
- Is this incident part of a larger campaign targeting our sector?
- What additional TTPs should we expect from this actor?
- Are there indicators of pre-positioning or additional persistence we have not yet detected?

*IOC-Driven:*
- Are these IOCs associated with a known threat actor or campaign?
- Are these indicators currently active or historical?
- What is the broader infrastructure behind these indicators?
- Are other organizations in our sector being targeted by the same infrastructure?

*Advisory-Driven:*
- Is our organization exposed to the threat described in the advisory?
- Are the vulnerable technologies present in our environment?
- Have we observed any indicators from the advisory in our telemetry?
- What specific defensive actions must we take immediately?

*RFI-Driven:*
- {{Based on the specific RFI question}}

*Proactive:*
- What is the current threat landscape for our sector and geography?
- Which threat actors are most likely to target our organization?
- What emerging capabilities or TTPs should we prepare for?
- Where are our detection gaps relative to the most probable threats?

*Environmental:*
- How does this environmental change affect our risk posture?
- Are threat actors exploiting this change? Who and how?
- What immediate defensive adjustments are required?

Do you confirm these PIRs, or would you like to modify them?"

Wait for operator confirmation. Record all confirmed PIRs with priority assignments.

### 6. Standing Intelligence Requirements (SIRs)

"**Standing Intelligence Requirements (SIRs):**

SIRs are persistent intelligence needs that apply across multiple intelligence cycles. Check if any SIRs exist for this engagement:

- Search for existing SIRs in `{irt_intel}/` or engagement documentation
- If SIRs exist: present them and ask which are relevant to this production
- If no SIRs exist: recommend establishing baseline SIRs

**Recommended Baseline SIRs (modify as needed):**

| # | SIR | Category | Frequency |
|---|-----|----------|-----------|
| SIR-1 | Monitor for new threat actor activity targeting our sector | Threat Landscape | Continuous |
| SIR-2 | Track evolution of TTPs used against our technology stack | Technical | Weekly |
| SIR-3 | Monitor for compromised credentials or data related to our organization | Exposure | Continuous |
| SIR-4 | Assess new CVEs affecting our critical infrastructure | Vulnerability | As published |
| SIR-5 | Monitor dark web and underground forums for mentions of our organization | Exposure | Weekly |

Which SIRs are relevant to this production? Any additions or modifications?"

Record relevant SIRs.

### 7. Intelligence Type Classification

Based on the trigger, PIRs, and intended audience, classify the intelligence type:

"**Intelligence Type Classification:**

| Type | Audience | Format | Timeline | Focus |
|------|----------|--------|----------|-------|
| **Tactical** | SOC analysts, detection engineers, IR team | IOC feeds, detection rules, STIX bundles | Hours to days | Immediate action: detect, block, hunt |
| **Operational** | IR managers, hunt teams, security architects | Actor profiles, campaign assessments, TTP reports | Days to weeks | Operational decisions: containment strategy, hunt priorities, architecture hardening |
| **Strategic** | CISO, executives, board, risk committee | Landscape assessments, trend analysis, risk forecasts | Weeks to months | Strategic decisions: budget, program, policy, organizational risk |

Based on the trigger ({{trigger_type}}) and PIRs:

**Recommended Classification: {{type}}**

**Justification:** {{why this type matches the trigger and audience}}

**Note:** A single intelligence production can generate products at multiple levels. The primary classification determines the depth of analysis and the lead product format. Tactical and operational byproducts (IOC feeds, detection rules) are always generated when applicable.

Confirm or adjust?"

Wait for operator confirmation. Record intelligence type.

### 8. Collection Plan

Build the collection plan that maps each PIR to specific intelligence sources:

"**Collection Plan:**

For each PIR, identify the sources to query, the expected data, and the collection timeline:

| PIR | Source Category | Specific Sources | Expected Data | Reliability (Admiralty) | Priority | Timeline |
|-----|-----------------|------------------|---------------|------------------------|----------|----------|
| PIR-1 | OSINT | {{blogs, researcher feeds, paste sites}} | {{expected data}} | B-2 to C-3 | High | {{hours/days}} |
| PIR-1 | Commercial | {{Recorded Future, Mandiant, CrowdStrike}} | {{expected data}} | A-1 to B-2 | High | {{hours/days}} |
| PIR-1 | Internal | {{SIEM, EDR, SOC findings}} | {{expected data}} | A-1 to B-2 | High | {{hours/days}} |
| PIR-2 | ISAC/CERT | {{sector ISAC, national CERT}} | {{expected data}} | A-2 to B-2 | Medium | {{hours/days}} |
| ... | ... | ... | ... | ... | ... | ... |

**Source Reliability Assessment (Admiralty Scale):**

| Rating | Reliability | Description |
|--------|-------------|-------------|
| A | Completely reliable | Proven source with established track record, no history of inaccuracy |
| B | Usually reliable | Source has provided accurate intelligence in most cases |
| C | Fairly reliable | Source has provided accurate intelligence occasionally, some track record |
| D | Not usually reliable | Source has a history of providing inaccurate intelligence |
| E | Unreliable | Source has no track record or has consistently provided inaccurate intelligence |
| F | Cannot be judged | New source, reliability cannot be assessed |

| Rating | Credibility | Description |
|--------|-------------|-------------|
| 1 | Confirmed | Corroborated by independent sources |
| 2 | Probably true | Consistent with known information, logical, from reliable source |
| 3 | Possibly true | Not confirmed or denied, reasonable but unverified |
| 4 | Doubtfully true | Inconsistent with known information, questionable |
| 5 | Improbable | Contradicted by known information |
| 6 | Cannot be judged | Basis for evaluation does not exist |

**Collection Gaps (Known Before Collection Begins):**
- {{gap_1}}: e.g., No commercial TI subscription — limits enrichment depth
- {{gap_2}}: e.g., No dark web collection authorization — limits adversary infrastructure visibility
- {{gap_3}}: e.g., SIEM retention only 90 days — limits historical correlation

These gaps will be tracked through collection (step 2) and noted in the final product.

**Collection Timeline:**
- Start: {{now}}
- Target completion: {{based on urgency and PIR priorities}}
- Total estimated collection window: {{hours/days}}

Review and confirm the collection plan?"

Wait for operator confirmation. Record collection plan.

### 9. Intelligence ID Assignment

Generate the intelligence ID using the standard format:

**Format:** `INTEL-{engagement_id}-{YYYYMMDD}-{seq}`

- `{engagement_id}`: From engagement.yaml
- `{YYYYMMDD}`: Today's date (intelligence production registration date)
- `{seq}`: Sequential number starting at 001 — check for existing intelligence IDs in `{irt_intel}/` to avoid collisions

Example: `INTEL-ENG-2026-0001-20260405-001`

"**Intelligence ID Assigned:** `{{intel_id}}`

This ID will be used for all documentation, evidence tracking, dissemination records, and cross-module references throughout the intelligence production lifecycle."

Update frontmatter: `intel_id: '{{intel_id}}'`

### 10. Create Initial Document

#### A. Document Setup

- Copy the template from `../templates/intel-report-template.md` to `{outputFile}`
- Populate frontmatter with:
  - `engagement_id`, `engagement_name` from engagement.yaml
  - `intel_id` from step 9
  - `intel_name` from operator-provided summary
  - `intel_type` from step 7 (tactical/operational/strategic)
  - `trigger_source` from step 4A (who/what initiated)
  - `trigger_type` from step 4A (incident/IOC/advisory/RFI/proactive/environmental)
  - `priority_intelligence_requirements` from step 5 (array of PIR texts)
  - `standing_intelligence_requirements` from step 6 (array of relevant SIR texts)
  - `collection_sources` from step 8 (array of planned source categories)
  - `collection_gaps` from step 8 (array of known gaps)
  - `related_incident_id` from step 4B (if incident-driven)
  - `related_forensic_case` from step 4C (if forensic report loaded)
  - `related_malware_case` from step 4C (if malware report loaded)
  - `cross_module_references` from step 4C (array of loaded report IDs)
  - `tlp_classification` set to initial TLP based on engagement defaults
- Initialize `stepsCompleted` as empty array

#### B. Populate Intelligence Requirement Section

Fill `## Intelligence Requirement` with:

**### Intelligence Trigger**
- Trigger type, source, timestamp, urgency
- Trigger details (from step 4B structured intake)
- Cross-module context summary (from step 4C)

**### Priority Intelligence Requirements (PIRs)**
- All confirmed PIRs with priority assignments
- Rationale for each PIR

**### Standing Intelligence Requirements (SIRs)**
- Relevant SIRs with their status

**### Collection Plan**
- PIR-to-source mapping table
- Collection timeline
- Known collection gaps

**### Source Reliability Assessment**
- Admiralty Scale ratings for planned sources

### 11. Present Summary to Operator

"**Intelligence Production Initiated**

{{user_name}}, I have verified the engagement authorization and completed the intelligence requirement definition.

**Engagement:** {{engagement_name}} (`{{engagement_id}}`)
**Status:** Active
**Period:** {{start_date}} — {{end_date}}

**Intelligence Summary:**
- **Intelligence ID:** `{{intel_id}}`
- **Trigger:** {{trigger_type}} — {{trigger_source_summary}}
- **Intel Type:** {{tactical/operational/strategic}}
- **PIRs Defined:** {{pir_count}} priority intelligence requirements
- **SIRs Active:** {{sir_count}} standing intelligence requirements
- **Collection Sources Planned:** {{source_count}} sources across {{category_count}} categories
- **Known Collection Gaps:** {{gap_count}}
- **Collection Timeline:** {{estimated_timeline}}

**Cross-Module Context:** {{Loaded from N reports / Cold start — no prior analysis available}}

**Intelligence Restrictions:** {{restrictions_summary or 'None — full intelligence authority'}}

**Confidence Assessment:** At this stage, confidence is LOW — we have defined the questions but have not yet collected or analyzed evidence. Confidence will be calibrated at each subsequent step as evidence accumulates.

**Document created:** `{outputFile}`

The intelligence requirement has been registered and the collection plan is defined. We are ready to proceed to intelligence collection."

### 12. Present MENU OPTIONS

Display menu after requirement report:

"**Select an option:**
[A] Advanced Elicitation — Challenge PIR completeness, identify blind spots in the collection plan, probe for unstated assumptions about the threat, and refine source selection
[W] War Room — Red Team perspective: what intelligence would the adversary NOT want us to discover? Where are our analytic blind spots? Blue Team perspective: which PIRs matter most for immediate defense? Are we collecting from the right sources for the timeline pressure?
[C] Continue — Proceed to Step 2: Intelligence Collection & Processing (Step 2 of 8)"

#### Menu Handling Logic:

- IF A: Invoke deep analysis of intelligence requirement gaps — examine whether PIRs are truly answerable with available sources, identify analytic assumptions that could introduce bias, challenge whether the intelligence type classification matches the actual consumer need, probe for unstated requirements that decision-makers will expect but have not articulated. Process insights, ask operator if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke War Room discussion — Red Team perspective: based on the trigger type, what does the adversary's OPSEC look like? What would they have concealed that standard collection will miss? Are there deception indicators we should watch for? What intelligence would change the adversary's behavior if they knew we had it? Blue Team perspective: which PIRs have the shortest decision timelines — what intelligence is needed in hours vs days vs weeks? Are the collection sources sufficient for the urgency? What detection actions can we take NOW with what we already know, before intelligence production completes? Summarize insights, ask operator if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-02-collection.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, intel_id assigned, trigger_type set, priority_intelligence_requirements populated, collection_sources listed, and Intelligence Requirement section populated], will you then read fully and follow: `./step-02-collection.md` to begin intelligence collection.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Existing workflow detected and properly handed off to step-01b
- Engagement authorization fully verified with all checks passing (including intelligence operations and external query authorization)
- Intelligence restrictions documented if present
- Intelligence trigger intake completed with trigger type classified and details gathered
- Cross-module context loaded and parsed if available, or absence clearly communicated
- PIRs defined with priority assignments and rationale — each PIR is a specific, answerable question
- SIRs identified and relevance assessed
- Intelligence type classified (tactical/operational/strategic) with justification
- Collection plan built with PIR-to-source mapping, Admiralty Scale reliability ratings, and timeline
- Collection gaps identified before collection begins
- Intelligence ID generated in correct format with no collisions
- Fresh workflow initialized with template and proper frontmatter (intel_id, trigger_type, priority_intelligence_requirements, collection_sources all populated)
- Intelligence Requirement section fully populated in output document
- Operator clearly informed of engagement status, intelligence summary, and collection plan
- Confidence explicitly stated as LOW at this stage with explanation
- Additional context validated before acceptance
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### SYSTEM FAILURE:

- Proceeding with intelligence production without verified engagement authorization
- Processing intelligence requirements outside the authorized scope or engagement boundaries
- Proceeding with fresh initialization when existing incomplete workflow exists
- Not gathering intelligence trigger details before defining requirements
- Defining PIRs without operator confirmation — PIRs must be agreed upon, not assumed
- Not classifying intelligence type before building collection plan — type determines depth, format, and audience
- Building a collection plan without source reliability assessment (Admiralty Scale)
- Not identifying collection gaps before collection begins
- Not generating an intelligence ID before proceeding
- Ignoring available cross-module context (incident, forensic, malware, SOC reports) without informing the operator
- Not documenting intelligence restrictions from the engagement RoE
- Not populating the Intelligence Requirement section of the output document
- Not reporting intelligence summary, PIRs, and collection plan to operator clearly
- Stating confidence higher than LOW at this stage — no collection or analysis has occurred
- Allowing any collection, analysis, or production activity in this initialization step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted, intel_id, and trigger_type

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No intelligence operations without authorization. No analysis without defined requirements. Intelligence without requirements is just noise. The collection plan is the roadmap — without it, collection is unfocused and the product is unreliable.
