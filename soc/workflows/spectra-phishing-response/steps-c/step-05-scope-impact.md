# Step 5: Scope & Impact Assessment

**Progress: Step 5 of 8** — Next: Containment & Eradication

## STEP GOAL:

Determine the full blast radius of the phishing campaign by analyzing mail flow data, categorizing user impact into tiers based on interaction level (received → opened → clicked → submitted credentials → executed malware), assessing endpoint compromise for high-interaction users, determining campaign scope (targeted vs mass, single vs multi-organization), and evaluating business impact including regulatory notification requirements — producing a structured scope assessment that directly informs containment priorities in the next step.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER perform containment actions during scope assessment — this is intelligence gathering to INFORM containment
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC PHISHING ANALYST assessing the blast radius of a phishing incident
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst conducting structured phishing investigation
- ✅ Scope assessment determines WHO is affected and HOW DEEPLY — this directly drives containment urgency and resource allocation
- ✅ The user interaction funnel (received → opened → clicked → compromised) is the key metric for phishing incident severity
- ✅ Not all recipients are equally affected — tiered assessment is critical for proportional response
- ✅ Regulatory notification requirements (GDPR 72h, HIPAA, state breach laws) may impose hard deadlines that override other priorities

### Step-Specific Rules:

- 🎯 Focus exclusively on scope and impact assessment — mail flow analysis, user categorization, endpoint assessment, campaign scope, business impact
- 🚫 FORBIDDEN to begin containment, blocking, account disabling, or any remediation — scope assessment only
- 💬 Approach: Systematic scope expansion from the single known phishing email to the full blast radius
- 📊 All user counts must be tracked across the interaction funnel tiers
- 🔒 Scope assessment is based on data from steps 1-4 plus mail flow / security platform data provided by or queried with the operator

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Scope assessment based solely on the single reported email may dramatically underestimate the blast radius — phishing campaigns typically target multiple recipients, and the first report is rarely the first delivery; always query mail flow logs to identify ALL recipients before determining scope
  - Users who clicked a credential harvesting link but claim they "didn't enter anything" should still be treated as potentially compromised — auto-fill, browser credential managers, and SSO tokens can expose credentials without explicit user submission; the safe assumption is compromise until proven otherwise
  - Endpoint compromise assessment for Tier 5 users (malware execution) requires EDR telemetry that may not be available through the SOC analyst's normal access — if EDR data is needed, coordinate with the endpoint team rather than assuming the absence of alerts means the endpoint is clean
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present scope assessment plan before beginning — acknowledge what data sources are available
- ⚠️ Present [A]/[W]/[C] menu after assessment complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `affected_users_total`, `users_received`, `users_opened`, `users_clicked`, `users_submitted_creds`, `accounts_compromised`, `severity`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, phishing email analysis, header analysis, content analysis, IOC enrichment from steps 1-4
- Focus: Scope and impact assessment — mail flow, user categorization, endpoint assessment, campaign scope, business impact
- Limits: Scope assessment only — do not begin any containment or remediation actions
- Dependencies: Completed email analysis (steps 1-3) and IOC enrichment (step 4)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Mail Flow Analysis

Guide the operator through querying mail flow data to identify the full scope of the phishing campaign.

#### A. Mail Server / Gateway Query Guidance

Provide platform-specific query guidance based on the organization's email platform:

**Microsoft Exchange / Microsoft 365:**
```
# Exchange Online — Message Trace (Security & Compliance Center)
# Search by sender address
Get-MessageTrace -SenderAddress "{{sender_address}}" -StartDate "{{delivery_date - 7 days}}" -EndDate "{{delivery_date + 1 day}}"

# Search by subject line
Get-MessageTrace -Subject "{{email_subject}}" -StartDate "{{delivery_date - 7 days}}" -EndDate "{{delivery_date + 1 day}}"

# Threat Explorer (Microsoft Defender for O365)
# Filter: Sender = {{sender_address}} OR Subject contains "{{email_subject}}"
# Date range: {{delivery_date - 7 days}} to {{delivery_date + 1 day}}

# Compliance Search — for purge operations (Step 6)
New-ComplianceSearch -Name "Phishing-{{incident_id}}" -ExchangeLocation All -ContentMatchQuery 'from:"{{sender_address}}" AND subject:"{{email_subject}}"'
```

**Google Workspace:**
```
# Google Admin Console → Reporting → Email Log Search
# Sender: {{sender_address}}
# Date range: {{delivery_date - 7 days}} to {{delivery_date + 1 day}}

# Gmail Security Investigation Tool (Enterprise)
# Search: from:{{sender_address}} OR subject:"{{email_subject}}"
# Actions available: view headers, view message, delete message

# BigQuery (if logging enabled)
SELECT timestamp, sender, recipient, subject, message_id, delivery_status
FROM `project.dataset.gmail_logs`
WHERE sender = '{{sender_address}}'
AND timestamp BETWEEN '{{delivery_date - 7 days}}' AND '{{delivery_date + 1 day}}'
```

**Proofpoint / Mimecast / Barracuda / Other Gateway:**
```
# Proofpoint TAP — Smart Search
# Sender: {{sender_address}}
# Subject: "{{email_subject}}"
# Threat type: All
# Date range: {{delivery_date - 7 days}} to {{delivery_date + 1 day}}

# Mimecast — Message Tracking
# Search by sender: {{sender_address}}
# Search by subject: {{email_subject}}

# Generic SIEM query (Splunk/Elastic/Sentinel)
index=email sourcetype=email_gateway
(sender="{{sender_address}}" OR subject="{{email_subject}}")
| stats count by recipient, delivery_status, action_taken
```

"**Please provide mail flow data** using the queries above (adapted to your platform) to identify all recipients of this phishing campaign. I need:
1. Total recipients who received the email
2. Delivery status for each recipient (delivered, quarantined, bounced, filtered)
3. Any click tracking data (if available from email security platform or proxy logs)
4. Any credential submission indicators (authentication logs showing logins from known-malicious infrastructure)

If you cannot query mail flow data directly, provide your best estimate based on available information."

**WAIT for operator to provide mail flow data before proceeding.**

#### B. Delivery Scope Summary

Based on mail flow data provided by the operator:

**Delivery Scope:**

| Delivery Status | Count | Percentage | Recipients |
|----------------|-------|------------|------------|
| Delivered to inbox | {{count}} | {{%}} | {{list or 'See detailed list below'}} |
| Quarantined by gateway | {{count}} | {{%}} | {{list}} |
| Blocked/rejected | {{count}} | {{%}} | {{list}} |
| Bounced (invalid recipient) | {{count}} | {{%}} | {{list}} |
| Filtered to spam/junk | {{count}} | {{%}} | {{list}} |
| **Total sent** | {{total}} | 100% | — |

**Delivery Analysis:**
- **Gateway effectiveness:** {{quarantined + blocked}} of {{total}} ({{%}}) were caught by the email gateway
- **Inbox delivery rate:** {{delivered}} of {{total}} ({{%}}) reached the inbox
- **Delivery timeline:** First delivery: {{earliest timestamp}} — Last delivery: {{latest timestamp}}
- **Internal forwarding:** {{count or 'None detected'}} — Did any recipient forward the phishing email internally?

### 2. User Impact Categorization

Categorize all recipients by their level of interaction with the phishing email. This is the core of the blast radius assessment.

**User Interaction Funnel:**

| Tier | Description | Exposure Level | Count | Action Required |
|------|-------------|---------------|-------|-----------------|
| **Tier 1** | Received only — no interaction | Minimal — email in mailbox but not opened | {{count}} | Email purge, awareness notification |
| **Tier 2** | Opened / previewed | Low-Medium — potential tracking pixel exposure, email content viewed | {{count}} | Email purge, awareness notification, check for tracking pixel data exfil |
| **Tier 3** | Clicked URL | Medium-High — exposed to landing page, potential credential/malware exposure | {{count}} | Password reset if credential harvester, endpoint scan, proxy log review |
| **Tier 4** | Submitted credentials | High — confirmed credential compromise | {{count}} | Immediate: disable account, force password reset, revoke sessions, MFA reset |
| **Tier 5** | Executed attachment / malware | Critical — confirmed endpoint compromise | {{count}} | Immediate: network isolation, malware removal, full incident response |

**Data Sources for Tier Classification:**

| Data Source | Tiers Informed | Query Method |
|------------|----------------|-------------|
| Email gateway logs | Tier 1 (delivery confirmation) | Message trace by sender/subject |
| Email open tracking | Tier 2 (open/preview detection) | Email security platform analytics, tracking pixel callbacks |
| Proxy / web filter logs | Tier 3 (URL click detection) | URL filter logs for phishing URL hits |
| URL click tracking | Tier 3 (click confirmation) | Safe Links / URL rewriting click reports |
| Authentication logs | Tier 4 (credential use detection) | Login attempts from malicious infrastructure IPs |
| Password change logs | Tier 4 (post-compromise activity) | Unusual password changes following phishing delivery |
| EDR telemetry | Tier 5 (execution detection) | Process creation, file writes, network connections from attachment |
| SIEM correlation | Tiers 3-5 | Correlated alerts for phishing recipients |

"**Please provide interaction data** to classify users by tier. At minimum I need:
- Proxy/web filter logs for URL clicks from the phishing email
- Authentication logs for the period since email delivery (to detect credential use from suspicious IPs)
- EDR alerts for any recipients who opened attachments

Any tier data you can provide improves the accuracy of the blast radius assessment."

**Present tier classification as data becomes available. Update as new data arrives.**

#### Detailed Per-Tier User Lists

For each non-empty tier, present the detailed user list:

**Tier {{N}} Users — {{tier_description}}:**

| # | User | Email | Department | Device | Interaction Time | Status | Notes |
|---|------|-------|------------|--------|-----------------|--------|-------|
| 1 | {{name}} | {{email}} | {{dept}} | {{hostname}} | {{timestamp}} | {{active/contained}} | {{specific notes}} |

### 3. Endpoint Assessment (Tier 3-5 Users)

For users in Tiers 3-5 (clicked URL, submitted credentials, or executed malware), guide the operator through endpoint assessment.

#### A. Tier 3 — URL Click Assessment

For each user who clicked a URL:

**Assessment Checklist:**

| Check | Data Source | Finding |
|-------|-----------|---------|
| URL destination type | Proxy logs | {{credential harvester / malware download / redirect chain / benign}} |
| Time on page | Proxy logs | {{duration — longer exposure = higher risk}} |
| Download triggered | Proxy logs / endpoint | {{file downloaded? filename, hash}} |
| Browser exploit potential | Patch status | {{browser version, known vulns for that version}} |
| Post-click network activity | EDR / firewall | {{suspicious outbound connections?}} |
| Post-click process activity | EDR | {{new processes spawned after browser activity?}} |

**Tier 3 Risk Assessment:**
- If URL was credential harvester → **escalate to Tier 4 assessment** (user may have submitted credentials even if they deny it)
- If URL triggered download → **escalate to Tier 5 assessment** (malware may have executed)
- If URL was tracking/benign → remain Tier 3, document exposure

#### B. Tier 4 — Credential Compromise Assessment

For each user suspected or confirmed to have submitted credentials:

**Credential Compromise Assessment:**

| Check | Data Source | Finding |
|-------|-----------|---------|
| Credential type exposed | Landing page analysis (Step 3) | {{email/password, O365, Google, VPN, internal app}} |
| Post-compromise logins | Authentication logs | {{logins from suspicious IPs since exposure time}} |
| MFA status at time of compromise | IAM platform | {{MFA enabled? Type? Could attacker bypass?}} |
| OAuth app consents | Azure AD / Google Admin | {{new app consents since compromise?}} |
| Mailbox rules created | Exchange/Gmail admin | {{auto-forwarding rules added?}} |
| Email access from suspicious IPs | Sign-in logs | {{mailbox accessed from phishing infrastructure?}} |
| Lateral movement indicators | SIEM | {{authenticated to other systems using compromised creds?}} |
| MFA device enrollment | IAM platform | {{new MFA devices registered since compromise?}} |
| Delegate/shared access changes | Exchange/Gmail admin | {{new delegates added? Shared mailbox access granted?}} |

**Credential Compromise Verdict:**
```
User: {{username}}
Credential Type Compromised: {{type}}
Confirmed Unauthorized Access: {{Yes/No/Unknown}}
Post-Compromise Actions Detected: {{list or 'None detected'}}
MFA Bypass Possible: {{Yes/No/Unknown}}
Lateral Movement Risk: {{High/Medium/Low}}
```

#### C. Tier 5 — Endpoint Compromise Assessment

For each user who executed a malicious attachment:

**Endpoint Compromise Assessment:**

| Check | Data Source | Finding |
|-------|-----------|---------|
| Process execution chain | EDR | {{parent → child process tree from attachment open}} |
| Network connections | EDR / firewall | {{C2 callbacks, data exfiltration, lateral movement}} |
| File system changes | EDR | {{dropped files, modified files, new executables}} |
| Registry modifications | EDR | {{persistence mechanisms, Run keys, services}} |
| Scheduled tasks | EDR | {{new scheduled tasks created}} |
| Credential access | EDR | {{LSASS access, SAM dump, credential harvesting tools}} |
| Privilege escalation | EDR | {{UAC bypass, token manipulation, exploit execution}} |
| Lateral movement | EDR / SIEM | {{RDP, PsExec, WMI, WinRM to other hosts}} |
| Data staging / exfiltration | EDR / DLP | {{file collection, archive creation, outbound transfer}} |

**Endpoint Compromise Verdict:**
```
Host: {{hostname}}
User: {{username}}
Malware Executed: {{Yes/No/Unknown}}
Malware Family: {{from Step 4 enrichment or 'Unknown'}}
Persistence Established: {{Yes/No/Unknown}}
C2 Communication: {{Active/Historical/None detected}}
Lateral Movement: {{Detected/Not detected/Unknown}}
Data Exposure: {{Detected/Not detected/Unknown}}
Containment Priority: {{IMMEDIATE / HIGH / MEDIUM}}
```

### 4. Campaign Scope Determination

Assess the broader scope of the phishing campaign:

**Campaign Scope Assessment:**

| Dimension | Assessment | Evidence |
|-----------|-----------|----------|
| **Target type** | {{Targeted spearphish / Semi-targeted (department/role) / Mass campaign / BEC/Whaling}} | {{evidence for classification}} |
| **Organization scope** | {{Single organization / Multiple organizations / Unknown}} | {{evidence — other orgs reporting same campaign?}} |
| **Campaign duration** | {{Single wave / Multiple waves / Ongoing}} | {{delivery timestamps, related emails}} |
| **Related emails** | {{count}} — same sender infrastructure, similar content | {{evidence}} |
| **Volume** | {{1-5 recipients (targeted) / 5-50 (semi-targeted) / 50+ (mass)}} | {{delivery data}} |
| **Personalization** | {{Generic / Role-based / Name-personalized / Context-personalized}} | {{evidence from email content}} |

**Campaign Timeline:**

| Event | Timestamp | Description |
|-------|-----------|-------------|
| First known delivery | {{timestamp}} | {{earliest delivery in mail flow data}} |
| Last known delivery | {{timestamp}} | {{latest delivery}} |
| First user interaction | {{timestamp}} | {{first click/open}} |
| First report | {{timestamp}} | {{when was the phishing reported}} |
| Investigation start | {{timestamp}} | {{when did this workflow begin}} |

### 5. Business Impact Assessment

Evaluate the business impact of the phishing incident:

**Business Impact Matrix:**

| Impact Category | Assessment | Detail |
|----------------|-----------|--------|
| **Data exposure** | {{None / Low / Medium / High / Critical}} | {{what data could have been exposed? PII, credentials, financial, IP}} |
| **Account compromise** | {{count}} accounts confirmed/suspected compromised | {{which accounts, privilege level}} |
| **System compromise** | {{count}} endpoints confirmed/suspected compromised | {{which systems, criticality}} |
| **Financial risk** | {{None / Low / Medium / High}} | {{BEC wire transfer? Ransomware deployment risk? Fraud?}} |
| **Operational impact** | {{None / Low / Medium / High}} | {{disruption to business operations}} |
| **Reputational risk** | {{None / Low / Medium / High}} | {{customer-facing impact, brand damage}} |

**Regulatory Notification Assessment:**

| Regulation | Applicable? | Threshold Met? | Deadline | Action Required |
|-----------|-------------|---------------|----------|-----------------|
| GDPR (Article 33) | {{Yes/No/Unknown}} | {{personal data breach confirmed?}} | 72 hours from awareness | {{notify DPA}} |
| GDPR (Article 34) | {{Yes/No/Unknown}} | {{high risk to individuals?}} | Without undue delay | {{notify affected individuals}} |
| HIPAA | {{Yes/No/Unknown}} | {{PHI exposed?}} | 60 days (to HHS), without unreasonable delay (to individuals) | {{notify HHS + individuals}} |
| PCI DSS | {{Yes/No/Unknown}} | {{cardholder data exposed?}} | Per acquirer agreement | {{notify payment brands + acquirer}} |
| SOX | {{Yes/No/Unknown}} | {{financial reporting integrity affected?}} | Varies | {{notify audit committee}} |
| State breach laws | {{Yes/No/Unknown}} | {{PII of state residents exposed?}} | {{varies by state — typically 30-60 days}} | {{per-state notification}} |
| Industry-specific | {{sector regulation}} | {{threshold}} | {{deadline}} | {{action}} |

**CRITICAL:** If any regulatory notification deadline applies, flag it prominently:

"⚠️ **REGULATORY NOTIFICATION DEADLINE**
{{regulation}}: Notification required within {{deadline}} of breach awareness.
Awareness timestamp: {{when the breach/compromise was confirmed}}
Deadline: {{calculated deadline}}
Time remaining: {{hours/days remaining}}
Responsible party: {{who in the organization must be notified to initiate regulatory reporting}}"

### 6. Severity Classification

Based on the full scope assessment, classify the incident severity:

**Severity Classification:**

| Criteria | Finding | Score |
|----------|---------|-------|
| Users received | {{count}} | {{1-5: Low, 5-50: Medium, 50+: High}} |
| Users clicked/interacted | {{count}} | {{0: Low, 1-5: Medium, 5+: High}} |
| Credentials compromised | {{count}} | {{0: Low, 1-3: High, 3+: Critical}} |
| Endpoints compromised | {{count}} | {{0: Low, 1: High, 2+: Critical}} |
| Data exposure confirmed | {{type}} | {{None: Low, PII: High, Sensitive/Financial: Critical}} |
| Regulatory notification required | {{Yes/No}} | {{No: Neutral, Yes: +1 severity level}} |
| Campaign ongoing | {{Yes/No}} | {{No: Neutral, Yes: +1 urgency}} |

**Overall Severity:** {{Low / Medium / High / Critical}}
**Urgency:** {{Standard / Elevated / Immediate}}

### 7. Present Blast Radius Visualization

"**Blast Radius Assessment — {{incident_id}}**

**User Interaction Funnel:**
```
Tier 1 — Received only:        {{count}} users  ████████████████████░░░░░
Tier 2 — Opened/previewed:     {{count}} users  ██████████████░░░░░░░░░░░
Tier 3 — Clicked URL:          {{count}} users  ████████░░░░░░░░░░░░░░░░░
Tier 4 — Submitted credentials: {{count}} users  ████░░░░░░░░░░░░░░░░░░░░░
Tier 5 — Executed malware:     {{count}} users  ██░░░░░░░░░░░░░░░░░░░░░░░
```

**Severity:** {{severity}} | **Urgency:** {{urgency}}
**Campaign type:** {{type}} | **Scope:** {{scope}}
**Accounts compromised:** {{count}} | **Endpoints compromised:** {{count}}
**Regulatory notifications:** {{required/not required}}

**Containment Priorities (for Step 6):**
1. {{highest priority — Tier 5 users / immediate isolation needed?}}
2. {{second priority — Tier 4 users / credential reset needed?}}
3. {{third priority — Tier 3 users / assessment needed?}}
4. {{fourth priority — Tier 1-2 users / email purge and notification}}"

### 8. Present MENU OPTIONS

"**Select an option:**
[A] Advanced Elicitation — Deep-dive into specific scope findings, challenge assumptions about user interaction tiers, investigate edge cases
[W] War Room — Red vs Blue discussion on blast radius implications — what would the attacker do next with this access? How should we prioritize containment?
[C] Continue — Proceed to Containment & Eradication (Step 6 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive scope analysis — challenge tier classifications (are Tier 3 users really not Tier 4?), investigate whether mail flow data is complete, assess whether internal forwarding expanded the blast radius, examine whether the attacker has already leveraged compromised credentials for lateral movement. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: with these compromised credentials, what would I do next? How quickly can I move laterally before containment catches up? Where are the high-value targets accessible from these compromised accounts? Blue Team perspective: is our containment timeline realistic given the blast radius? Are we tracking all the right data sources? What are we missing in the scope assessment? Should we escalate to full incident response? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `affected_users_total`, `users_received`, `users_opened`, `users_clicked`, `users_submitted_creds`, `accounts_compromised`, `severity`, then read fully and follow: ./step-06-containment.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and all scope metrics updated, and scope assessment results appended to report under `## Scope & Impact Assessment`], will you then read fully and follow: `./step-06-containment.md` to begin containment and eradication planning.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Mail flow query guidance provided for the operator's email platform
- Delivery scope documented with counts per status (delivered, quarantined, blocked, bounced, filtered)
- User interaction funnel populated across all 5 tiers with counts and user lists
- Endpoint assessment guidance provided for Tier 3-5 users with platform-specific checklists
- Credential compromise assessment completed for Tier 4 users (post-compromise access, MFA, mailbox rules, OAuth)
- Endpoint compromise assessment completed for Tier 5 users (process chains, network, persistence, lateral movement)
- Campaign scope determined (targeted vs mass, single vs multi-org, duration, volume)
- Campaign timeline documented with key events
- Business impact assessed across all categories (data, accounts, systems, financial, operational, reputational)
- Regulatory notification requirements assessed with specific deadlines flagged
- Severity classified based on quantified criteria
- Blast radius visualization presented with clear containment priorities
- Scope assessment appended to report under `## Scope & Impact Assessment`
- Frontmatter updated with all scope metrics and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Assessing scope based only on the single reported email without querying mail flow data
- Not categorizing users into interaction tiers
- Treating all recipients as equally affected without tiered assessment
- Assuming Tier 3 users (clicked URL) are not compromised without endpoint/credential assessment
- Assuming users who "didn't enter anything" on a credential page are not compromised
- Not assessing regulatory notification requirements when data exposure is possible
- Beginning containment, blocking, or account disabling during scope assessment
- Not providing platform-specific query guidance for the operator
- Not flagging regulatory notification deadlines prominently when they apply
- Proceeding to containment without completed scope assessment
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with scope metrics and stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. The blast radius must be fully assessed before containment begins. Scope assessment drives containment priorities.
