# Step 1: Phishing Report Intake & Initialization

**Progress: Step 1 of 8** — Next: Header Analysis

## STEP GOAL:

Verify the active engagement, ingest the phishing email sample from the operator, extract initial email metadata (subject, sender, recipients, date, message-ID), preserve the raw email data verbatim, create the phishing report document from the template, and prepare the foundation for deep header analysis in the next step. This is the gateway step — no phishing investigation may begin without confirmed authorization, a valid email sample, and operator acknowledgment.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER proceed without verified engagement authorization
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC PHISHING ANALYST, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst conducting structured phishing investigation within an active security engagement
- ✅ Every action must be traceable to an authorized engagement and defined scope
- ✅ Email integrity is non-negotiable — raw email data must be preserved alongside normalized fields
- ✅ When in doubt about email legitimacy or scope, ASK. Never assume.
- ✅ Evidence chain integrity is non-negotiable from the very first step
- ✅ Phishing investigation follows a specific analytical flow: intake → headers → content → IOCs → scope → containment → detection → closure

### Step-Specific Rules:

- 🎯 Focus only on engagement verification, email sample ingestion, metadata extraction, and document creation — no header analysis or enrichment yet
- 🚫 FORBIDDEN to look ahead to future steps or assume knowledge from them
- 💬 Approach: Systematic intake with clear reporting to user
- 🚪 Detect existing workflow state and handle continuation properly
- 🔒 If engagement is missing or invalid: HARD STOP — no exceptions
- 📥 Phishing email sample is mandatory — cannot proceed without it
- 📧 Accept ALL input formats: EML, MSG, raw headers, forwarded text, screenshots, gateway alerts, user reports

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Processing an email without full headers significantly reduces analysis quality — header analysis (Step 2) requires Received chains, authentication results, and X-headers to trace the email's true origin and detect spoofing; without headers, the investigation proceeds on content alone, which limits confidence in attribution and infrastructure mapping
  - Screenshots lose all header data and embedded metadata — the investigation can still proceed on visual content (sender display name, subject, body, URLs, brand impersonation indicators), but header analysis will be severely limited and authentication verification (SPF/DKIM/DMARC) will be impossible; warn the operator but accept the screenshot if they confirm
  - Forwarded emails may have modified headers — when an email is forwarded, the original Received chain is typically preserved but new headers are prepended, and some mail clients strip or reformat headers; flag this to the operator so they understand that header analysis may contain artifacts from the forwarding process, not just the original delivery
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking any action
- 💾 Initialize document structure and update frontmatter appropriately
- Update frontmatter: add this step name to the end of the stepsCompleted array (it should be the first entry since this is step 1)
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md are available in memory, engagement.yaml is loaded, phishing email sample provided by operator
- Focus: Authorization verification, email sample ingestion, metadata extraction, and document creation only
- Limits: Don't assume knowledge from other steps or begin any header analysis, enrichment, or containment activity
- Dependencies: Configuration loaded from workflow.md initialization, engagement.yaml verified, phishing sample received from operator

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Check for Existing Workflow State

First, check if the output document already exists:

**Workflow State Detection:**

- Look for file at `{outputFile}`
- If exists, read the complete file including frontmatter
- If not exists, this is a fresh workflow

### 2. Handle Continuation (If Document Exists)

If the document exists and has frontmatter with `stepsCompleted` BUT `step-08-reporting.md` is NOT in the list, follow the Continuation Protocol since the document is incomplete:

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
| Email infrastructure in scope | Email systems or users within engagement scope | ✅/❌ |

**If ANY check fails:** HALT IMMEDIATELY.

"**AUTHORIZATION BLOCK**

The engagement does not meet the requirements for phishing response operations:
- {{list of failed checks}}

Required actions:
- If no engagement exists: run `spectra-new-engagement`
- If the engagement has expired: contact the engagement lead for renewal
- If scope is empty: update engagement.yaml with monitored assets
- If SOC operations are not authorized: request an engagement amendment
- If email infrastructure is not in scope: amend scope to include email systems

No phishing investigation will be executed without complete authorization."

**Do NOT proceed. This is a hard stop.**

### 4. Phishing Sample Ingestion

The operator has provided the phishing email sample (from workflow.md initialization). Parse and process based on the input format.

#### A. Detect Input Format

Identify the format of the incoming phishing sample:

**Full-fidelity formats (richest data — preferred):**
- **EML file** — RFC 5322 compliant email with full headers and MIME body
- **MSG file** — Microsoft Outlook proprietary format with full headers and body
- **Raw email source** — complete email source from "View Source" / "Show Original" including all headers

**Partial-fidelity formats (some data loss — acceptable with warnings):**
- **Raw headers only** — email headers without body content (header analysis possible, content analysis limited)
- **Forwarded email** — email forwarded by the reporter (headers may include forwarding artifacts)
- **Email gateway alert** — parsed metadata from secure email gateway (Proofpoint, Mimecast, Microsoft Defender for O365, Google Workspace Security)

**Low-fidelity formats (significant data loss — warn operator):**
- **Screenshot** — visual image of the email (no headers, no embedded metadata, no URL extraction from hyperlinks)
- **User report** — free-text description from the reporting user (no structured data, relies on user recall)
- **Chat/ticket excerpt** — excerpt from a helpdesk ticket or chat message describing the phishing email

Report the detected format to the operator:

"**Phishing sample format detected:** {{format_type}} ({{format_description}})
**Data fidelity:** {{Full / Partial / Low}}
**Parsing strategy:** {{full_parse / header_extraction / content_extraction / visual_analysis / manual_extraction}}
{{if Partial or Low: '⚠️ **Warning:** ' + specific_limitation_description}}"

#### B. Extract Initial Email Metadata

Extract and normalize the following fields from the phishing sample. For any field not present in the source data, mark as `[NOT PROVIDED]` and flag for operator review:

**Core Email Metadata:**
- **Incident ID**: Generate `PHISH-{{YYYYMMDD}}-{{HHMMSS}}` if none provided by the operator
- **Email Subject**: The subject line of the phishing email (preserve exactly, including any RE:/FW: prefixes)
- **Sender (From)**: Display name and email address from the From header (e.g., `"IT Support" <support@example.com>`)
- **Sender (Envelope)**: Return-Path / MAIL FROM address if available from headers
- **Reply-To**: Reply-To address if different from From (immediate red flag if mismatched)
- **Recipients (To)**: All To addresses — indicates targeted vs mass distribution
- **Recipients (CC)**: All CC addresses if present
- **Delivery Timestamp**: Date header value, converted to UTC
- **Message-ID**: Unique message identifier from headers
- **X-Mailer / User-Agent**: Email client or platform used to compose the message (if present in headers)

**Quick Triage Indicators (assess during intake):**
- **Reply-To mismatch**: Does Reply-To differ from From? (Yes/No/Not Present)
- **External sender**: Is the sender external to the organization? (Yes/No/Unknown)
- **Suspicious subject patterns**: Urgency keywords (urgent, immediate, action required, verify, confirm, suspended, locked)
- **Attachment present**: Are there attachments? (Yes/No — count and filenames if visible)
- **URLs present**: Are there URLs in the body? (Yes/No — count if visible)

Present the extracted metadata to the operator for validation:

"**Phishing Email Metadata — {{incident_id}}**

| Field | Value |
|-------|-------|
| Incident ID | {{incident_id}} |
| Subject | {{subject}} |
| From (Display) | {{from_display_name}} |
| From (Address) | {{from_address}} |
| Envelope From | {{return_path or '[NOT PROVIDED]'}} |
| Reply-To | {{reply_to or '[SAME AS FROM]'}} |
| To | {{to_addresses}} |
| CC | {{cc_addresses or '[NONE]'}} |
| Delivery Date (UTC) | {{delivery_timestamp}} |
| Message-ID | {{message_id or '[NOT PROVIDED]'}} |
| X-Mailer | {{x_mailer or '[NOT PROVIDED]'}} |

**Quick Triage Indicators:**

| Indicator | Value | Flag |
|-----------|-------|------|
| Reply-To Mismatch | {{Yes/No/Not Present}} | {{🔴 if Yes, 🟢 if No}} |
| External Sender | {{Yes/No/Unknown}} | {{🟡 if Yes}} |
| Urgency Language | {{detected keywords or 'None detected'}} | {{🔴 if detected}} |
| Attachments | {{count or 'None'}} | {{🟡 if > 0}} |
| URLs in Body | {{count or 'None'}} | {{🟡 if > 0}} |

**Fields marked [NOT PROVIDED]:** {{list of missing fields}}
**Data fidelity:** {{Full / Partial / Low}}

Please review and confirm accuracy, or provide corrections."

### 5. Raw Email Preservation

Preserve the raw email data verbatim for the audit trail. This is the original evidence and must never be modified.

**If full email source available (EML/MSG/raw source):**

"**Raw Email Source (Preserved Verbatim):**

```
{{complete raw email source — headers and body — exactly as received}}
```"

**If forwarded email text:**

"**Forwarded Email Text (Preserved Verbatim):**

⚠️ *Note: This email was forwarded by the reporter. Original headers may be modified or incomplete. Forwarding artifacts have been noted.*

```
{{forwarded email text — exactly as provided by the reporter}}
```"

**If screenshot:**

"**Screenshot Evidence:**

⚠️ *Note: Screenshot input — no header data available. Analysis limited to visual content.*

Screenshot file: {{file reference or inline description}}
Visual elements captured: {{sender display, subject, body text, visible URLs, branding elements}}"

**If user report / chat excerpt:**

"**User Report (Preserved Verbatim):**

⚠️ *Note: User-provided description — no structured email data. All metadata is as recalled by the reporter and should be verified against email gateway logs where possible.*

```
{{user report text — exactly as provided}}
```"

### 6. Create Document and Present Summary

#### A. Document Setup

- Copy the template from `../templates/phishing-report-template.md` to `{outputFile}`
- Populate frontmatter with:
  - `engagement_id`, `engagement_name` from engagement.yaml
  - `incident_id` from generated or operator-provided ID
  - `email_subject` from extracted metadata
  - `email_sender` from From address
  - `email_recipients` array with all To/CC addresses
  - `delivery_timestamp` from UTC delivery date
  - `urls_found` with initial count (if visible during intake)
  - `attachments_found` with initial count (if visible during intake)
- Initialize `stepsCompleted` as empty array

#### B. Populate Email Summary Section

Fill `## Email Summary` with:
- Extracted metadata table (from Section 4B above)
- Quick triage indicators table (from Section 4B above)
- Raw email data block (from Section 5 above — preserved verbatim in code fence)
- Input format and data fidelity notes
- Any missing fields flagged for downstream steps
- Data limitations based on input format

#### C. Present Summary to User

"Welcome {{user_name}}! I have verified the engagement authorization and completed phishing email intake.

**Engagement:** {{engagement_name}} (`{{engagement_id}}`)
**Status:** Active ✅

**Phishing Email Intake Summary:**
- **Incident ID:** {{incident_id}}
- **Subject:** {{email_subject}}
- **From:** {{from_display_name}} <{{from_address}}>
- **To:** {{to_addresses}}
- **Delivery Date:** {{delivery_timestamp}} UTC
- **Input Format:** {{format_type}} — Data Fidelity: {{Full/Partial/Low}}

**Quick Triage:**
- **Reply-To Mismatch:** {{Yes/No/Not Present}}
- **Attachments:** {{count or 'None detected'}}
- **URLs:** {{count or 'None detected'}}
- **Urgency Indicators:** {{keywords or 'None detected'}}

**Document created:** `{outputFile}`

The phishing email has been ingested and initial metadata extracted. The raw email has been preserved for the audit trail. Ready for deep header analysis in the next step."

### 7. Present MENU OPTIONS

Display menu after intake report:

"**Select an option:**
[A] Advanced Elicitation — Deep analysis of email metadata gaps, input quality assessment, and suggestions for obtaining higher-fidelity email data
[W] War Room — Red vs Blue discussion on initial phishing indicators and likely attacker objectives
[C] Continue — Proceed to Header Analysis (Step 2 of 8)"

#### Menu Handling Logic:

- IF A: Invoke deep analysis of email data quality — examine what intelligence is missing due to input format limitations, identify blind spots (missing headers, missing attachment data, missing URL metadata), suggest ways the operator could obtain higher-fidelity data (request EML from reporter, pull from email gateway, check mail flow logs). Process insights, ask user if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke War Room discussion — Red Team perspective on what the initial metadata reveals about the attacker's approach (targeted vs mass, infrastructure sophistication, social engineering technique), initial hypotheses about campaign type. Blue Team perspective on detection coverage for this type of phishing email, what the email gateway should have caught, and what initial response priorities should be. Summarize insights, ask user if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-02-header-analysis.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Email Summary section populated], will you then read fully and follow: `./step-02-header-analysis.md` to begin email header deep analysis.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Existing workflow detected and properly handed off to step-01b
- Engagement authorization fully verified with all checks passing (including SOC operations authorization and email infrastructure in scope)
- Phishing email sample received from operator and input format correctly identified with data fidelity assessment
- Email metadata extracted and normalized into structured fields with all available data captured
- Missing fields clearly flagged for operator review with specific impact notes
- Quick triage indicators assessed and presented (Reply-To mismatch, external sender, urgency language, attachments, URLs)
- Raw email data preserved verbatim in a code fence with format-specific preservation notes
- Fresh workflow initialized with template and proper frontmatter
- Email Summary section populated in output document with metadata table, quick triage indicators, and raw email
- User clearly informed of engagement status, email intake summary, and data quality assessment
- Input format warnings issued when appropriate (partial/low fidelity)
- Additional context validated before acceptance
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### SYSTEM FAILURE:

- Proceeding with phishing investigation without verified engagement authorization
- Processing emails outside the authorized scope or engagement boundaries
- Proceeding with fresh initialization when existing workflow exists
- Modifying raw email data instead of preserving it alongside normalized fields
- Not flagging missing critical fields or data fidelity limitations to the operator
- Not issuing appropriate warnings for partial/low fidelity input formats
- Not preserving the raw email source verbatim
- Not populating the Email Summary section of the output document
- Not reporting email intake summary and quick triage indicators to user clearly
- Allowing any header analysis, enrichment, or containment activity in this initialization step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No phishing investigation without authorization. No header analysis without confirmed email intake.
