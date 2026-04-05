# Step 1: Alert Intake and Initialization

**Progress: Step 1 of 7** — Next: IOC Enrichment

## STEP GOAL:

Verify the active engagement, ingest the raw alert from the operator, normalize it into a structured format, and extract all observables (IOCs) for enrichment in the next step. This is the gateway step — no triage activity may begin without confirmed authorization, a valid alert source, and operator acknowledgment.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER proceed without verified engagement authorization
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC TRIAGE ANALYST, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Triage Analyst conducting structured alert analysis within an active security engagement
- ✅ Every action must be traceable to an authorized engagement and defined scope
- ✅ Alert integrity is non-negotiable — raw data must be preserved alongside normalized fields
- ✅ When in doubt about alert legitimacy or scope, ASK. Never assume.
- ✅ Evidence chain integrity is non-negotiable from the very first step

### Step-Specific Rules:

- 🎯 Focus only on engagement verification, alert ingestion, normalization, and IOC extraction — no enrichment or classification yet
- 🚫 FORBIDDEN to look ahead to future steps or assume knowledge from them
- 💬 Approach: Systematic intake with clear reporting to user
- 🚪 Detect existing workflow state and handle continuation properly
- 🔒 If engagement is missing or invalid: HARD STOP — no exceptions
- 📥 Raw alert data is mandatory — cannot proceed without it

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Processing an alert from a source not configured in the SIEM may indicate a rogue or test alert — verify the source legitimacy with the operator before proceeding, but do not block if the operator confirms
  - Normalizing an alert with missing critical fields (no timestamp, no affected host, no source IP) reduces triage reliability — flag the gaps so the operator can supplement manually, but continue with available data if the operator accepts the risk
  - Extracting IOCs from unstructured or free-text alerts may produce false extractions — present all extracted observables for operator validation before recording them as confirmed IOCs
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking any action
- 💾 Initialize document structure and update frontmatter appropriately
- Update frontmatter: add this step name to the end of the stepsCompleted array (it should be the first entry since this is step 1)
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md are available in memory, engagement.yaml is loaded, raw alert data provided by operator
- Focus: Authorization verification, alert ingestion, normalization, and IOC extraction only
- Limits: Don't assume knowledge from other steps or begin any enrichment, classification, or response activity
- Dependencies: Configuration loaded from workflow.md initialization, engagement.yaml verified, alert data received from operator

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Check for Existing Workflow State

First, check if the output document already exists:

**Workflow State Detection:**

- Look for file at `{outputFile}`
- If exists, read the complete file including frontmatter
- If not exists, this is a fresh workflow

### 2. Handle Continuation (If Document Exists)

If the document exists and has frontmatter with `stepsCompleted` BUT `step-07-complete.md` is NOT in the list, follow the Continuation Protocol since the document is incomplete:

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
| SOC operations authorized | Engagement permits SOC triage operations | ✅/❌ |
| Scope defined | At least one monitored asset in scope | ✅/❌ |
| Alert source in scope | Alert originates from a monitored source within scope | ✅/❌ |

**If ANY check fails:** HALT IMMEDIATELY.

"**AUTHORIZATION BLOCK**

The engagement does not meet the requirements for SOC triage operations:
- {{list of failed checks}}

Required actions:
- If no engagement exists: run `spectra-new-engagement`
- If the engagement has expired: contact the engagement lead for renewal
- If scope is empty: update engagement.yaml with monitored assets
- If SOC operations are not authorized: request an engagement amendment

No triage activity will be executed without complete authorization."

**Do NOT proceed. This is a hard stop.**

### 4. Alert Ingestion and Normalization

The operator has provided the raw alert data (from workflow.md initialization). Parse and normalize into a structured format.

#### A. Detect Input Format

Identify the format of the incoming alert data:

**Structured formats (parse directly):**
- JSON (SIEM export, API response, cloud security finding)
- CEF (Common Event Format — ArcSight, QRadar, etc.)
- OCSF (Open Cybersecurity Schema Framework)
- LEEF (Log Event Extended Format)
- Syslog with structured payload

**Semi-structured formats (extract key-value pairs):**
- SIEM alert with labeled fields (Splunk notable, Elastic alert, Sentinel incident)
- EDR detection summary (CrowdStrike, SentinelOne, Defender)
- Email gateway notification with parsed headers
- Tabular output (CSV, TSV)

**Unstructured formats (extract observables manually):**
- Free-text description from an analyst or operator
- Screenshot of an alert console
- Chat/email notification without structured fields
- Verbatim log lines without parsing

Report the detected format to the operator:

"**Alert format detected:** {{format_type}} ({{source_description}})
Parsing strategy: {{direct_parse / key_value_extraction / manual_extraction}}"

#### B. Normalize Alert Fields

Extract and normalize the following fields from the raw alert data. For any field not present in the source data, mark as `[NOT PROVIDED]` and flag for operator review:

**Core Alert Metadata:**
- **Alert ID**: Unique identifier from the source system (or generate `TRIAGE-{{YYYYMMDD}}-{{HHMMSS}}` if none provided)
- **Timestamp (UTC)**: When the alert fired, converted to UTC
- **Source Platform**: The system that generated the alert (e.g., Splunk, CrowdStrike, Sentinel)
- **Rule Name**: The detection rule or signature that triggered
- **Severity**: Original severity from source system (critical/high/medium/low/informational)
- **Confidence Score**: If the source provides a confidence metric

**MITRE ATT&CK Mapping:**
- **Technique(s)**: If the alert is pre-tagged with ATT&CK technique IDs (e.g., T1566.001)
- **Tactic(s)**: The corresponding tactic(s) (e.g., Initial Access, Execution)
- If not tagged: note for manual mapping in Step 4 (Correlation)

**Affected Assets:**
- **Host(s)**: Hostname, IP address, OS, asset criticality if known
- **User(s)**: Username, email, role/privilege level, department if known

**Network Observables:**
- **Source IP**: Origin of the suspicious activity
- **Destination IP**: Target of the suspicious activity
- **Source Port / Destination Port**: If available
- **Protocol**: TCP, UDP, ICMP, HTTP, DNS, etc.

**Alert Content:**
- **Raw log/event data**: Verbatim from the source — preserve exactly as received
- **Alert description**: Human-readable summary from the detection system

Present the normalized alert to the operator for validation:

"**Normalized Alert — {{alert_id}}**

| Field | Value |
|-------|-------|
| Alert ID | {{alert_id}} |
| Timestamp (UTC) | {{timestamp}} |
| Source Platform | {{source_platform}} |
| Rule Name | {{rule_name}} |
| Severity | {{severity}} |
| Confidence | {{confidence}} |
| MITRE Technique(s) | {{techniques or 'Not tagged — manual mapping in Step 4'}} |
| Affected Host(s) | {{hosts}} |
| Affected User(s) | {{users}} |
| Source IP | {{src_ip}} |
| Destination IP | {{dst_ip}} |
| Protocol | {{protocol}} |

**Fields marked [NOT PROVIDED]:** {{list of missing fields}}

Please review and confirm accuracy, or provide corrections."

### 5. IOC Extraction

Extract all observables (Indicators of Compromise) from the alert data — both from structured fields and from raw log/event content.

#### A. Observable Types to Extract

Systematically scan for the following observable types:

- **IP Addresses**: IPv4 and IPv6, both source and destination, plus any referenced in logs
- **Domains**: FQDNs, subdomains, any DNS references in the alert
- **URLs**: Full URLs including paths and query parameters
- **File Hashes**: MD5, SHA1, SHA256 — from file references, payload hashes, attachment hashes
- **Email Addresses**: Sender, recipient, references in headers or body
- **User Agents**: HTTP user agent strings from web traffic or proxy logs
- **JA3/JA3S Hashes**: TLS fingerprints if available from network inspection
- **Process Names**: Executable names, service names, parent-child process relationships
- **Command Lines**: Full command-line strings from EDR or Sysmon events
- **Registry Keys**: Windows registry paths if applicable (modifications, persistence keys)
- **File Paths**: Local file paths referenced in the alert

#### B. Present Extracted IOCs

Present the IOC extraction results in a structured table for operator validation:

"**Extracted IOCs — {{alert_id}}**

| # | IOC | Type | Context | Source Field |
|---|-----|------|---------|--------------|
| 1 | {{ioc_value}} | {{type}} | {{where/why this IOC appears}} | {{which alert field it came from}} |
| 2 | ... | ... | ... | ... |

**Total IOCs extracted:** {{count}}

**Extraction notes:**
- {{any ambiguities, potential false extractions, or items needing operator judgment}}

Please review and confirm the IOC list. Flag any false extractions or add any IOCs I may have missed."

Wait for operator confirmation before proceeding. If the operator flags false extractions, remove them. If the operator adds IOCs, incorporate them.

### 6. Create Document and Present Summary

#### A. Document Setup

- Copy the template from `../templates/triage-report-template.md` to `{outputFile}`
- Populate frontmatter with:
  - `engagement_id`, `engagement_name` from engagement.yaml
  - `alert_id` from normalized alert
  - `alert_source` from source platform
  - `alert_severity` from original severity
  - `alert_timestamp` from UTC timestamp
  - `iocs_extracted` with the confirmed count
  - `affected_hosts` array with identified hostnames/IPs
  - `affected_users` array with identified usernames
  - `mitre_techniques` array if auto-tagged by the source system
- Initialize `stepsCompleted` as empty array

#### B. Populate Alert Summary Section

Fill `## Alert Summary` with:
- Normalized alert table (from Section 4B above)
- Raw alert data block (preserved verbatim in a code fence)
- Confirmed IOC table (from Section 5B above)
- Input format and parsing notes
- Any missing fields flagged for downstream steps

#### C. Present Summary to User

"Welcome {{user_name}}! I have verified the engagement authorization and completed alert intake.

**Engagement:** {{engagement_name}} (`{{engagement_id}}`)
**Status:** Active ✅

**Alert Intake Summary:**
- **Alert ID:** {{alert_id}}
- **Source:** {{source_platform}} — {{rule_name}}
- **Severity:** {{severity}} | **Confidence:** {{confidence}}
- **Timestamp:** {{timestamp}} UTC
- **Affected Host(s):** {{hosts}}
- **Affected User(s):** {{users}}
- **MITRE Technique(s):** {{techniques or 'Pending manual mapping in Step 4'}}

**IOC Extraction:**
- **Total IOCs extracted:** {{count}}
- **Types:** {{summary of IOC types, e.g., '3 IPs, 2 domains, 1 hash'}}

**Document created:** `{outputFile}`

The alert has been ingested and normalized. All extracted IOCs are ready for enrichment in the next step."

### 7. Present MENU OPTIONS

Display menu after intake report:

"**Select an option:**
[A] Advanced Elicitation — Deep analysis of alert context gaps and additional intelligence needs
[W] War Room — Red vs Blue discussion on initial alert assessment and likely attacker intent
[C] Continue — Proceed to IOC Enrichment (Step 2 of 7)"

#### Menu Handling Logic:

- IF A: Invoke deep analysis of alert context gaps — examine what intelligence is missing, identify blind spots in the alert data, suggest additional data sources to query. Process insights, ask user if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke War Room discussion — Red Team perspective on what this alert pattern suggests about attacker TTPs vs Blue Team perspective on detection coverage and potential evasion. Summarize insights, ask user if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-02-enrichment.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Alert Summary section populated], will you then read fully and follow: `./step-02-enrichment.md` to begin IOC enrichment.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Existing workflow detected and properly handed off to step-01b
- Engagement authorization fully verified with all checks passing (including SOC operations authorization)
- Raw alert data received from operator and input format correctly identified
- Alert normalized into structured fields with all available data extracted
- Missing fields clearly flagged for operator review
- All IOCs extracted, presented in structured table, and validated by operator
- Fresh workflow initialized with template and proper frontmatter
- Alert Summary section populated in output document with normalized data, raw alert, and IOC table
- User clearly informed of engagement status, alert intake summary, and IOC extraction results
- Additional context validated before acceptance
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### SYSTEM FAILURE:

- Proceeding with triage operations without verified engagement authorization
- Processing alerts outside the authorized scope or engagement boundaries
- Proceeding with fresh initialization when existing workflow exists
- Modifying raw alert data instead of preserving it alongside normalized fields
- Not flagging missing critical fields to the operator
- Recording IOCs without operator validation
- Not populating the Alert Summary section of the output document
- Not reporting alert intake summary and IOC extraction results to user clearly
- Allowing any enrichment, classification, or response activity in this initialization step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No triage operations without authorization. No enrichment without confirmed alert intake.
