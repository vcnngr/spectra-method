# Step 1: Case Intake & Evidence Receipt

**Progress: Step 1 of 10** — Next: Evidence Acquisition & Preservation

## STEP GOAL:

Verify the active engagement, intake the forensic case from the operator (case classification, legal context, evidence sources, forensic question, scope definition), receive evidence items with full metadata and chain of custody documentation, establish integrity baselines via cryptographic hashing, generate the case ID, and create the forensic report workspace. This is the gateway step — no forensic analysis may begin without confirmed authorization, a valid case intake, evidence receipt with integrity verification, and operator acknowledgment.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER proceed without verified engagement authorization
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous forensic tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst conducting a structured forensic examination under ISO 27037 and NIST SP 800-86
- ✅ Every action must be traceable to an authorized engagement with forensic investigation scope
- ✅ Evidence integrity begins NOW — chain of custody is established the moment evidence is received, not when analysis starts
- ✅ Every evidence item must be treated as if it will be presented in court — because it might be
- ✅ Forensic documentation is a legal artifact — accuracy, completeness, and precision are non-negotiable

### Step-Specific Rules:

- 🎯 Focus only on engagement verification, case intake, evidence receipt, integrity baselining, case ID assignment, and workspace setup — no acquisition planning, no analysis, no timeline work yet
- 🚫 FORBIDDEN to look ahead to future steps or assume knowledge from them
- 💬 Approach: Meticulous and methodical intake with timestamps, hashes, and documentation at every stage
- 🚪 Detect existing workflow state and handle continuation properly
- 🔒 If engagement is missing or invalid: HARD STOP — no exceptions
- 📥 Case intake requires at minimum: case classification, legal context, and at least one evidence source identified
- ⏱️ Timestamp everything — forensic timelines are measured with precision
- 🔐 Hash everything — every evidence item must have MD5 + SHA-256 computed at the moment of receipt

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Accepting evidence without computing integrity hashes at the point of receipt means you cannot prove the evidence was unmodified from that moment forward — if opposing counsel asks when you first verified evidence integrity and the answer is "later," the entire chain of custody is vulnerable to challenge
  - Proceeding without establishing legal context (litigation hold, law enforcement involvement, regulatory requirement) risks conducting the investigation to a standard that does not meet the eventual legal need — a compliance investigation analyzed to internal standards cannot be retroactively elevated to court-admissible standards after evidence handling shortcuts have been taken
  - Not documenting evidence discrepancies (hash mismatches, missing items, damaged media) at the point of receipt creates ambiguity about when the discrepancy occurred — document it now, attribute it to pre-receipt conditions, or own it forever as a potential chain of custody break
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking any action
- 💾 Initialize document structure and update frontmatter appropriately
- Update frontmatter: add this step name to the end of the stepsCompleted array (it should be the first entry since this is step 1)
- ⏱️ Record the case intake timestamp as the official start of the forensic investigation
- 🔐 Compute and record hashes for every evidence item received
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md are available in memory, engagement.yaml is loaded, incident handling report may be available
- Focus: Authorization verification, case intake, evidence receipt, integrity baselining, case ID assignment, and workspace setup only
- Limits: Don't assume knowledge from other steps or begin any acquisition planning, analysis, or timeline work
- Dependencies: Configuration loaded from workflow.md initialization, engagement.yaml verified, operator provides case and evidence details

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Check for Existing Workflow State

First, check if the output document already exists:

**Workflow State Detection:**

- Look for forensic report files matching `{irt_forensics}/forensic-report-*.md`
- If a matching file exists, read the complete file including frontmatter
- If no matching file exists, this is a fresh workflow — proceed to engagement verification

### 2. Handle Continuation (If Document Exists)

If the document exists and has frontmatter with `stepsCompleted` BUT `step-10-reporting.md` is NOT in the list, follow the Continuation Protocol since the document is incomplete:

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
| File exists | engagement.yaml present | ✅/❌ |
| Status active | `status: active` | ✅/❌ |
| Dates valid | start_date <= today <= end_date | ✅/❌ |
| Forensics authorized | Engagement permits forensic investigation (incident-response, blue-team, purple-team, or forensic-investigation) | ✅/❌ |
| Evidence acquisition authorized | RoE permits evidence acquisition (imaging, capture, collection) | ✅/❌ |
| Evidence analysis authorized | RoE permits forensic examination of acquired evidence | ✅/❌ |
| Scope defined | At least one target system, network, or organizational unit in scope | ✅/❌ |

**If ANY of the first four checks fail:** HALT IMMEDIATELY.

"**AUTHORIZATION BLOCK**

The engagement does not meet the requirements for forensic investigation operations:
- {{list of failed checks}}

Required actions:
- If no engagement exists: run `spectra-new-engagement` to create an authorized engagement with forensic investigation scope
- If the engagement has expired: contact the engagement lead for renewal — evidence degrades with time, but legal authorization must be in place
- If scope is empty: update engagement.yaml with authorized systems and organizational units
- If forensic investigation is not authorized: the engagement type must permit incident-response, blue-team, purple-team, or forensic-investigation operations

No forensic investigation activity will be executed without complete authorization."

**Do NOT proceed. This is a hard stop.**

#### B. Note Investigation Restrictions (If Any)

If the engagement authorizes forensic investigation but restricts specific activities:

- Document each restriction clearly: e.g., "No analysis of personal email content", "Credential extraction requires legal counsel approval", "Report must not contain raw PII — redact before delivery"
- These restrictions will be enforced in all downstream analysis steps
- Present restrictions to the operator:

"**Investigation Restrictions Identified:**

| Restriction | Source (RoE Clause) | Impact on Analysis |
|-------------|---------------------|--------------------|
| {{restriction}} | {{roe_clause}} | {{how this affects forensic analysis}} |

These restrictions will be enforced throughout the investigation. Acknowledge?"

### 4. Case Intake

This is the core of Step 1. Gather the following information from the operator through structured elicitation. For each category, ask explicitly and wait for the operator's response.

#### A. Case Classification

Ask the operator to identify the type of forensic investigation:

"**What type of forensic investigation is this?** Select the primary classification:

1. **Incident Response** — Forensic analysis supporting an active security incident (breach, malware, unauthorized access)
2. **Litigation Support** — Forensic analysis for legal proceedings (civil or criminal)
3. **HR Investigation** — Forensic analysis supporting a human resources investigation (policy violation, misconduct, IP theft)
4. **Compliance** — Forensic analysis for regulatory compliance (audit response, data handling verification, breach notification support)
5. **Proactive Assessment** — Forensic analysis for threat hunting, compromise assessment, or security posture validation (no known incident)

Which classification, and provide details?"

Record: case classification, context, any specific requirements related to the classification.

**Classification impacts downstream behavior:**
- **Incident Response**: Speed is prioritized alongside forensic rigor. Evidence may still be volatile. Coordinate with incident handler.
- **Litigation Support**: Legal admissibility is paramount. Every step must meet evidentiary standards. Expect opposing counsel scrutiny.
- **HR Investigation**: Privacy restrictions may apply. Scope may be narrow (specific user, specific timeframe). Legal counsel involvement likely.
- **Compliance**: Regulatory framework dictates standards. Documentation must map to specific regulatory requirements.
- **Proactive Assessment**: No known threat — systematic sweep for indicators of compromise. Broader scope, lower urgency.

#### B. Legal Context

"**What is the legal context for this investigation?**

- **Law enforcement involvement**: Is law enforcement engaged or expected to be engaged? (If yes, evidence handling must meet criminal evidence standards, and reporting may need to accommodate law enforcement requests)
- **Litigation hold**: Is there an active litigation hold? (If yes, all evidence must be preserved indefinitely — no destruction, no overwriting, no expiration)
- **Regulatory requirement**: Which regulatory frameworks apply? (GDPR, HIPAA, PCI DSS, SOX, SEC, state breach notification laws)
- **Internal investigation**: Is this purely internal, or could it escalate to external proceedings?
- **Expert witness expectation**: Is expert testimony anticipated? (If yes, all documentation must support expert witness preparation)
- **Privileged investigation**: Is this investigation conducted under attorney-client privilege? (If yes, specific handling requirements apply)

Provide the legal context — this determines the evidentiary standard we must meet."

Record: law enforcement status, litigation hold status, regulatory frameworks, investigation privilege, expert witness expectation, any legal counsel instructions.

#### C. Forensic Question

"**What is the specific question this forensic investigation must answer?**

Every forensic investigation is driven by a question. The question determines what evidence is relevant, what analysis techniques are applied, and what findings are significant. Examples:

- 'Was the database server compromised, and if so, was customer data accessed or exfiltrated?'
- 'Did the terminated employee copy proprietary files before departure?'
- 'What was the full scope of the ransomware attack — initial access through encryption?'
- 'Is there evidence of unauthorized access to the financial system during Q3 2025?'
- 'What malware is present on the infected systems and what are its capabilities?'

State the forensic question as precisely as possible."

Record: forensic question verbatim, any sub-questions or related questions, what constitutes a definitive answer.

#### D. Scope Definition

"**What is the scope of this forensic investigation?**

- **Systems to examine**: List all systems, endpoints, servers, and devices in scope (hostname, IP, OS, role)
- **Timeframe**: What is the relevant time window? (earliest date of interest through latest date of interest)
- **Out of scope**: Are any systems, data types, or time periods explicitly excluded?
- **Evidence already available**: What evidence has already been acquired or is available for acquisition?
- **Evidence to be acquired**: What additional evidence needs to be captured?
- **Data sensitivity boundaries**: Are there data types that must not be examined (personal files, privileged communications)?

Define the boundaries clearly — scope creep in forensics wastes resources and may expose protected data."

Record: in-scope systems, timeframe, exclusions, available evidence, pending acquisition, data sensitivity restrictions.

#### E. Prior Investigation Activity

"**Has any investigation activity already been performed?**

- **Incident handling**: Was an incident handling workflow (`spectra-incident-handling`) executed? If so, provide the incident ID.
- **Evidence collection**: Was any evidence already collected? (By whom, when, using what tools, with what chain of custody?)
- **Analysis performed**: Has any preliminary analysis been done? (By whom, what was found, was it documented?)
- **Containment actions**: Were any containment actions taken that may have affected evidence? (System isolation, process termination, account lockout — these actions change system state and must be accounted for in the forensic timeline)
- **Third-party involvement**: Were external forensic firms, law enforcement, or other parties involved?

Document all prior activity — it affects evidence integrity, timeline reconstruction, and the scope of our examination."

Record: all prior activities with timestamps, personnel, tools used, findings, and any potential impact on evidence integrity.

### 5. Evidence Receipt

For each evidence item the operator provides or identifies, create a formal evidence receipt record. This is where chain of custody begins.

#### A. Evidence Inventory

"**List all evidence items available for this investigation.**

For each item, provide:
- Description (what it is)
- Source system (hostname, IP, serial number, asset tag)
- Acquisition date (when was it captured)
- Acquired by (who performed the acquisition)
- Acquisition method (tool used, procedure followed)
- Format (E01, raw/dd, AFF4, LIME, PCAP, EVTX, CSV, JSON, etc.)
- Size (bytes or human-readable)
- Hash provided (was a hash computed at acquisition? MD5? SHA-256? SHA-512?)
- Current location (where is the evidence stored right now)
- Physical media (if applicable — write-blocked hard drive, USB, optical media)

If evidence has not yet been acquired: list what evidence needs to be acquired in step 2."

#### B. Per-Item Evidence Receipt

For each evidence item received, create a formal receipt record:

**Evidence Item Receipt:**

```
| Field | Value |
|-------|-------|
| Evidence ID | EVD-{case_id}-{NNN} (assigned sequentially starting at 001) |
| Description | {{what it is and what it contains}} |
| Source System | Hostname: {{hostname}}, IP: {{ip}}, OS: {{os}}, Serial: {{serial}}, Asset Tag: {{tag}} |
| Acquisition Date | {{UTC timestamp}} |
| Acquired By | {{name, role, organization}} |
| Acquisition Method | {{tool, version, parameters}} |
| Format | {{E01/raw/LIME/PCAP/EVTX/CSV/JSON/etc.}} |
| Size | {{bytes}} ({{human-readable}}) |
| Hash (MD5) | {{hash — computed at receipt if not provided}} |
| Hash (SHA-256) | {{hash — computed at receipt if not provided}} |
| Hash (SHA-512) | {{hash — for critical items or litigation support cases}} |
| Hash Provided by Acquirer | {{yes — matches / yes — MISMATCH / no — computed at receipt}} |
| Current Location | {{storage path or physical location}} |
| Physical Media | {{if applicable: media type, serial number, write-blocker used}} |
| Received By | {{analyst name — you}} |
| Receipt Timestamp | {{UTC timestamp — now}} |
| Condition at Receipt | {{intact / damaged / incomplete — describe any issues}} |
| Notes | {{any observations about the evidence at receipt}} |
```

#### C. Chain of Custody Initialization

For each evidence item, create the first chain of custody entry:

```
| Transfer # | Date/Time (UTC) | Released By | Received By | Purpose | Location Before | Location After | Hash Verified |
|------------|-----------------|-------------|-------------|---------|-----------------|----------------|---------------|
| 1 | {{receipt_timestamp}} | {{acquirer_name, role}} | {{analyst_name}} | Forensic examination | {{original_location}} | {{forensic_lab/workspace}} | {{Yes — hash matches / ALERT — mismatch}} |
```

#### D. Hash Discrepancy Handling

If any hash verification fails at receipt:

"**EVIDENCE INTEGRITY ALERT — Hash Mismatch Detected**

| Evidence ID | Expected Hash | Computed Hash | Algorithm | Discrepancy |
|-------------|---------------|---------------|-----------|-------------|
| EVD-{case_id}-{NNN} | {{provided_hash}} | {{computed_hash}} | {{MD5/SHA-256}} | {{description}} |

**Assessment:** This discrepancy was identified at the point of receipt, before any forensic analysis. Possible explanations:
1. Transcription error in the provided hash
2. Evidence was modified after original hash computation
3. Different source data was hashed (e.g., logical copy vs physical image)
4. Storage media corruption during transfer

**Recommendation:** Document the discrepancy, investigate the cause with the acquirer, and note the impact on evidence admissibility. The evidence may still have investigative value even if its legal admissibility is compromised.

**Action required:** Operator must acknowledge this discrepancy before proceeding."

### 6. Check for Incident Handling Context

Search for completed or in-progress incident handling reports in `{irt_artifacts}/incident-handling/`:

**If incident handling report(s) exist — parse and extract:**

- `incident_id` — The incident identifier
- `incident_severity` — Severity classification
- `affected_systems` — Systems identified during incident handling
- `affected_users` — User accounts identified
- `iocs_identified` — IOCs already extracted
- `mitre_techniques` — ATT&CK techniques mapped
- `containment_status` — Current containment state
- `evidence_items` — Evidence already collected during incident handling
- `evidence_chain_intact` — Chain of custody status from incident handling

Present the incident handling context to the operator:

"**Incident Handling Context Loaded:**

| Field | Value |
|-------|-------|
| Incident ID | {{incident_id}} |
| Severity | {{incident_severity}} |
| Affected Systems | {{affected_systems}} |
| Affected Users | {{affected_users}} |
| IOCs Identified | {{iocs_identified}} |
| MITRE Techniques | {{mitre_techniques}} |
| Containment Status | {{containment_status}} |
| Evidence Already Collected | {{evidence_items}} items |
| Evidence Chain Intact | {{evidence_chain_intact}} |

This pre-existing incident data will inform the forensic investigation scope and may include evidence items that transfer directly into this case."

Update frontmatter: `incident_handling_ref: '{{incident_id}}'`, `incident_id: '{{incident_id}}'`

**If incident handling report does NOT exist:**

"**No incident handling report found** in `{irt_artifacts}/incident-handling/`.

This forensic investigation is operating as a standalone examination. If this investigation is part of an active incident, the `spectra-incident-handling` workflow can run in parallel to coordinate containment, communication, and recovery while forensics proceeds.

Proceeding with independent forensic investigation."

### 7. Case ID Assignment

Generate the case ID using the standard format:

**Format:** `CASE-{engagement_id}-{YYYYMMDD}-{seq}`

- `{engagement_id}`: From engagement.yaml
- `{YYYYMMDD}`: Today's date (case registration date)
- `{seq}`: Sequential number starting at 001 — check for existing case IDs in `{irt_forensics}/` to avoid collisions

Example: `CASE-ENG-2026-0001-20260405-001`

"**Case ID Assigned:** `{{case_id}}`

This case ID will be used for all documentation, evidence tracking, chain of custody records, and reporting throughout the forensic investigation. All evidence items have been assigned EVD IDs under this case: EVD-{{case_id}}-001 through EVD-{{case_id}}-{{NNN}}."

Update frontmatter: `case_id: '{{case_id}}'`

### 8. Create Initial Document

#### A. Document Setup

- Copy the template from `../templates/forensic-report-template.md` to `{outputFile}` (resolving `{case_id}` in the filename)
- Populate frontmatter with:
  - `engagement_id`, `engagement_name` from engagement.yaml
  - `case_id` from step 7
  - `case_name` from operator input (brief descriptive name)
  - `case_classification` from step 4A
  - `legal_context` from step 4B
  - `legal_hold_status` from step 4B
  - `forensic_question` from step 4C
  - `evidence_items` array with EVD IDs from step 5
  - `evidence_item_count` with the count
  - `chain_of_custody_entries` with the count of initial CoC entries
  - `evidence_types` with booleans for which evidence types are present (disk, memory, network, cloud, mobile)
  - `incident_handling_ref` and `incident_id` from step 6 if available
  - `regulatory_implications` from step 4B
  - `case_status: 'open'`
- Initialize `stepsCompleted` as empty array

#### B. Populate Case Summary Section

Fill `## Case Summary` with:

**### Case Identification**
- Case ID, case name, case classification
- Forensic question
- Investigation start timestamp

**### Legal Context & Authority**
- Legal context details from step 4B
- Engagement authorization summary
- Investigation restrictions (if any)
- Applicable forensic standards

**### Forensic Question**
- The specific forensic question to be answered
- Sub-questions and related questions
- What constitutes a definitive answer

**### Scope Definition**
- In-scope systems, timeframe, exclusions
- Data sensitivity boundaries
- Available evidence summary
- Pending acquisition summary

**### Incident Handling Cross-Reference**
- Incident handling data if loaded (from step 6), or note absence
- Evidence items inherited from incident handling (if any)

#### C. Populate Evidence Inventory Section

Fill `## Evidence Inventory & Chain of Custody` with:

**### Evidence Intake Log**
- Complete evidence item table from step 5B

**### Chain of Custody Master Log**
- Initial chain of custody entries from step 5C

**### Evidence Integrity Verification Log**
- Hash verification results from step 5B and 5D

### 9. Present Summary to Operator

"**Forensic Investigation Initiated**

Welcome {{user_name}}. I have verified the engagement authorization and completed case intake with evidence receipt.

**Engagement:** {{engagement_name}} (`{{engagement_id}}`)
**Status:** Active ✅
**Period:** {{start_date}} — {{end_date}}

**Case Summary:**
- **Case ID:** `{{case_id}}`
- **Classification:** {{case_classification}}
- **Legal Context:** {{legal_context_summary}}
- **Forensic Question:** {{forensic_question}}
- **Scope:** {{scope_summary}}
- **Timeframe:** {{timeframe}}

**Evidence Received:**
- **Items:** {{evidence_item_count}} evidence items received
- **Types:** {{evidence_types_present}}
- **Total Size:** {{total_evidence_size}}
- **Integrity:** {{all_hashes_verified / discrepancies_noted}}
- **Chain of Custody:** Initiated for all items

**Incident Context:** {{Loaded from incident-handling / Not available — standalone investigation}}
**Investigation Restrictions:** {{restrictions_summary or 'None — full investigation authority'}}

**Document created:** `{outputFile}`

The case has been registered, evidence received and integrity-verified, and chain of custody established. We are ready to proceed to evidence acquisition and preservation planning."

### 10. Present MENU OPTIONS

Display menu after intake report:

"**Select an option:**
[A] Advanced Elicitation — Deep analysis of case intake gaps, missing evidence, additional data sources to identify, and forensic question refinement
[W] War Room — Red vs Blue discussion: Red Team perspective on what evidence the attacker would have targeted for destruction or tampering vs Blue Team perspective on evidence completeness and chain of custody robustness
[C] Continue — Proceed to Step 2: Evidence Acquisition & Preservation (Step 2 of 10)"

#### Menu Handling Logic:

- IF A: Invoke deep analysis of case intake gaps — examine what evidence is still missing, identify blind spots in the scope definition, challenge the forensic question (is it precise enough to drive analysis?), evaluate whether the evidence types available are sufficient to answer the forensic question, identify additional systems or data sources that should be examined, assess whether the legal context has been fully captured. Process insights, ask operator if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke War Room discussion — Red Team perspective: if I were the attacker and knew a forensic investigation was coming, what evidence would I destroy? What logs would I clear? What timestamps would I modify? What false evidence would I plant to misdirect the investigation? Are there evidence sources the investigator has not requested that contain traces of my activity? Blue Team perspective: is our evidence set sufficient to answer the forensic question? Are there gaps in the evidence that could prevent definitive findings? Is the chain of custody robust enough for the legal context? Are there additional evidence sources we should acquire before they are overwritten or expired? Summarize insights, ask operator if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-02-acquisition.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, case_id assigned, case_classification set, forensic_question recorded, evidence_items populated with EVD IDs and hashes, chain_of_custody_entries counted, and Case Summary and Evidence Inventory sections populated], will you then read fully and follow: `./step-02-acquisition.md` to begin evidence acquisition and preservation planning.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Existing workflow detected and properly handed off to step-01b
- Engagement authorization fully verified with all checks passing (including forensic investigation and evidence handling authorization)
- Investigation restrictions documented if present
- Case intake completed with all five categories gathered from operator (classification, legal context, forensic question, scope, prior activity)
- Evidence receipt completed with per-item metadata, EVD IDs assigned, and chain of custody initialized
- Integrity hashes (MD5 + SHA-256) computed for every evidence item at the point of receipt
- Hash discrepancies identified, documented, and acknowledged by operator
- Incident handling context loaded and parsed if available, or absence clearly communicated
- Case ID generated in correct format with no collisions
- Fresh workflow initialized with template and proper frontmatter (case_id, case_classification, forensic_question, evidence_items, chain_of_custody_entries all populated)
- Case Summary and Evidence Inventory sections fully populated in output document
- Operator clearly informed of engagement status, case summary, evidence status, and investigation context
- Additional context validated before acceptance
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### ❌ SYSTEM FAILURE:

- Proceeding with forensic investigation without verified engagement authorization
- Processing cases outside the authorized scope or engagement boundaries
- Proceeding with fresh initialization when existing incomplete workflow exists
- Not gathering all five intake categories from the operator before proceeding
- Accepting evidence without computing integrity hashes at the point of receipt
- Not assigning EVD IDs to every evidence item received
- Not initializing chain of custody for every evidence item
- Not documenting hash discrepancies when they occur
- Ignoring available incident handling data without informing the operator
- Not documenting investigation restrictions from the engagement RoE
- Not populating the Case Summary and Evidence Inventory sections of the output document
- Not reporting case summary, evidence status, and investigation context to operator clearly
- Allowing any analysis activity in this initialization step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted, case_id, and evidence_items

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No forensic operations without authorization. No analysis without completed intake. Evidence integrity starts at receipt — hash everything, document everything, verify everything. Chain of custody is sacred.
