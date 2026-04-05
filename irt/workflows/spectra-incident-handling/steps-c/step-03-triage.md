# Step 3: Initial Analysis & Severity Triage

**Progress: Step 3 of 10** — Next: Containment Strategy & Execution

## STEP GOAL:

Perform initial technical analysis to determine the full incident scope, validate or adjust the severity classification based on new evidence, conduct a formal business impact assessment, make the containment urgency decision, and establish the stakeholder notification matrix. This is the critical decision gate — the output of this step directly determines how aggressively and quickly we contain.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER downgrade severity without documented evidence — under-classification benefits the adversary
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator managing an active security incident under NIST 800-61
- ✅ Triage is the pivotal decision point — everything before this was information gathering, everything after this is action
- ✅ Scope determination drives resource allocation — underestimate and you're under-resourced, overestimate and you waste capacity
- ✅ Business impact assessment is not optional — it determines notification obligations, resource priority, and executive involvement
- ✅ The containment urgency decision is the single most consequential output of this step — get it wrong and you either lose evidence waiting or disrupt business unnecessarily

### Step-Specific Rules:

- 🎯 Focus exclusively on scope assessment, technical triage, severity re-assessment, business impact analysis, containment urgency decision, and stakeholder notification planning
- 🚫 FORBIDDEN to execute containment actions — this step DECIDES the containment strategy, step 4 EXECUTES it
- 💬 Approach: Evidence-driven analysis that translates technical findings into business risk and actionable containment decisions
- 📊 Every scope assessment must include a confidence level — distinguish between confirmed and suspected scope
- 🔒 Severity can be upgraded or downgraded, but EVERY change must be documented with specific evidence justifying the change
- ⚖️ Balance urgency with accuracy — a wrong containment decision is worse than a slightly delayed correct one

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Downgrading severity under business pressure risks inadequate response to a real incident — if the evidence supports a higher severity, the classification must reflect reality regardless of how inconvenient it is; document the pressure and the evidence-based recommendation separately
  - Delaying containment to gather more data while active exfiltration is occurring prioritizes analysis over damage control — if there is evidence of active data movement, containment takes precedence over perfect information; you can investigate after the bleeding stops
  - Not documenting business impact assessment creates legal exposure if regulatory notification is required — regulators expect documented risk assessment contemporaneous with the incident, not reconstructed after the fact; document now
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your triage analysis plan before beginning — let the operator know the assessment approach
- ⚠️ Present [A]/[W]/[C] menu after triage complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, incident intake data from step 1, enriched IOCs and detection analysis from step 2 (NIST classification, ATT&CK mapping, detection timeline, dwell time estimate)
- Focus: Scope determination, severity validation, business impact, containment urgency, and stakeholder notification planning — no containment execution
- Limits: Scope assessment is based on currently available data — do not claim certainty where evidence only supports suspicion; clearly distinguish confirmed vs suspected
- Dependencies: Completed detection source analysis, IOC enrichment, NIST classification, ATT&CK mapping, and detection timeline from step-02-detection.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Scope Assessment — Determine the Blast Radius

Systematically assess the scope of the incident across five domains. For each domain, distinguish between **confirmed** (evidence-backed) and **suspected** (inferred from indicators) scope.

#### A. Affected Systems Inventory

Identify all systems involved in or affected by the incident:

**Confirmed Systems** (direct evidence of compromise or impact):

| System | Type | Role | Evidence of Compromise | Criticality | Status |
|--------|------|------|----------------------|-------------|--------|
| {{hostname/IP}} | Server/Endpoint/Network Device/Cloud Resource | {{business function}} | {{specific evidence — IOC match, suspicious process, unauthorized access}} | Critical/High/Medium/Low | Compromised/Impacted/Under Investigation |

**Suspected Systems** (indirect indicators or proximity-based suspicion):

| System | Type | Suspicion Basis | Investigation Priority |
|--------|------|----------------|----------------------|
| {{hostname/IP}} | {{type}} | {{why this system is suspected — same subnet, same credentials, similar traffic pattern}} | High/Medium/Low |

**Network Segments:**
- Which VLANs/subnets contain confirmed affected systems?
- Are there network segments that share trust relationships with affected segments?
- Is there evidence of cross-segment activity (lateral movement indicators)?
- Which network boundaries have been crossed?

#### B. Affected Users

Identify all user accounts involved:

**Confirmed Compromised Accounts:**

| Account | Type | Privilege Level | Evidence | Impact |
|---------|------|-----------------|----------|--------|
| {{username}} | Domain/Local/Cloud/Service | Standard/Admin/Domain Admin/Root | {{evidence — credential theft, unauthorized login, pass-the-hash}} | {{what the attacker can do with this account}} |

**Suspected Compromised Accounts:**

| Account | Suspicion Basis | Investigation Priority |
|---------|----------------|----------------------|
| {{username}} | {{why suspected — same password, MFA bypass attempt, related activity}} | High/Medium/Low |

**Privileged Account Assessment:**
- Are any domain admin, root, or service accounts compromised?
- Are any cloud admin (Azure Global Admin, AWS root, GCP org admin) accounts compromised?
- What is the blast radius if the most privileged compromised account is fully exploited?

#### C. Affected Data Assessment

Classify the data at risk:

| Data Category | Classification | Regulatory Framework | Location | Exposure Risk |
|---------------|---------------|---------------------|----------|--------------|
| PII (Personal Identifiable Information) | {{Confidential/Internal/Public}} | GDPR, CCPA | {{systems/databases}} | {{confirmed accessed / suspected accessible / no evidence of access}} |
| PHI (Protected Health Information) | {{classification}} | HIPAA | {{location}} | {{exposure risk}} |
| PCI (Payment Card Data) | {{classification}} | PCI DSS | {{location}} | {{exposure risk}} |
| Intellectual Property | {{classification}} | Trade secret/NDA | {{location}} | {{exposure risk}} |
| Financial Data | {{classification}} | SOX, SEC | {{location}} | {{exposure risk}} |
| Credentials/Secrets | {{classification}} | Internal | {{location}} | {{exposure risk}} |

**Data Access Evidence:**
- Is there evidence the adversary accessed sensitive data stores?
- Are there data staging indicators (compression, encryption, collection)?
- Are there data exfiltration indicators (unusual outbound traffic, large transfers)?

Update frontmatter: `data_exfiltration_detected: {{true/false}}`

#### D. Network Propagation Assessment

Evaluate lateral movement and C2 activity:

- **Lateral movement indicators**: Pass-the-hash, RDP from compromised hosts, WMI/PSExec execution, SMB file shares accessed from anomalous sources
- **C2 beaconing patterns**: Regular interval connections, DNS tunneling, HTTP(S) callbacks, encoded/encrypted channels
- **Infrastructure compromise**: Are network devices (firewalls, routers, switches) compromised?
- **Trust exploitation**: Are trust relationships (Active Directory trusts, SSH keys, service account credentials) being leveraged?

Update frontmatter: `lateral_movement_detected: {{true/false}}`

#### E. Cloud/SaaS Impact Assessment

- **OAuth tokens**: Are any OAuth tokens compromised? What applications do they grant access to?
- **API keys**: Are any API keys exposed or used by the adversary?
- **Cloud resources**: Are cloud compute, storage, or networking resources compromised?
- **SaaS access**: Are any SaaS applications (M365, Google Workspace, Salesforce, Slack) compromised?
- **Identity federation**: If SSO/SAML is compromised, what is the downstream impact on federated applications?

**Present the complete scope matrix to the operator:**

"**Incident Scope Assessment:**

| Domain | Confirmed | Suspected | Confidence | Notes |
|--------|-----------|-----------|------------|-------|
| Systems | {{confirmed_count}} | {{suspected_count}} | High/Medium/Low | {{key note}} |
| User Accounts | {{confirmed_count}} | {{suspected_count}} | High/Medium/Low | {{key note}} |
| Data Categories | {{at_risk_count}} categories | - | High/Medium/Low | {{most sensitive data at risk}} |
| Network Segments | {{affected_count}} | {{adjacent_count}} | High/Medium/Low | {{lateral movement status}} |
| Cloud/SaaS | {{affected_count}} | {{suspected_count}} | High/Medium/Low | {{federation impact}} |

**Scope Summary:** {{narrative summary of the blast radius — what is the worst-case scenario if all suspected scope is confirmed?}}"

Update frontmatter: `affected_systems: {{confirmed_count}}`, `affected_users: {{confirmed_user_count}}`

### 2. Technical Triage Analysis

Conduct focused technical analysis across available data sources to validate scope and uncover additional indicators. The depth of analysis depends on what data sources are available.

#### A. Log Analysis (SIEM)

If SIEM access is available or logs are provided:
- Query for all events related to confirmed IOCs across a ±24h window from the first indicator
- Search for related user accounts across all authentication logs
- Search for related systems across all endpoint and network logs
- Identify any events that extend the timeline earlier than the current first indicator
- Identify any events that expand the scope to systems not yet identified
- Document query syntax and results for reproducibility

#### B. Endpoint Analysis (EDR)

If EDR telemetry is available:
- Process tree analysis for all suspicious processes on confirmed affected endpoints
- File system changes: created, modified, deleted files — especially in temp directories, startup locations, and system directories
- Registry modifications: run keys, scheduled tasks, WMI subscriptions, services
- Scheduled tasks and cron jobs: newly created or modified
- Network connections: all outbound connections from affected endpoints, especially to non-standard ports
- Memory artifacts: if memory capture is available or EDR provides in-memory detection

#### C. Network Analysis (NDR/PCAP)

If network detection or packet captures are available:
- Traffic patterns to/from confirmed malicious IPs and domains
- DNS queries from affected systems — especially for non-standard TLDs, high-entropy domains, or known C2 domains
- Connection volumes and durations — persistent connections suggest C2
- Data transfer volumes — large outbound transfers suggest exfiltration
- Protocol anomalies — HTTP on non-standard ports, DNS with unusual record types, encrypted traffic to unknown endpoints

#### D. Authentication Analysis

Review authentication events across all available sources:
- Failed and successful logins for compromised accounts across all systems
- Impossible travel analysis: same account authenticating from geographically distant locations within impossible timeframes
- MFA bypass attempts: MFA fatigue, SIM swap, token theft
- Service account activity: service accounts performing interactive logins or accessing systems outside their normal scope
- Kerberos: golden ticket, silver ticket, or Kerberoasting indicators
- Cloud authentication: Azure AD sign-in logs, AWS CloudTrail, GCP audit logs

#### E. Email Analysis (If Email-Borne)

If the incident involves email-based attack:
- Email header analysis: sender authentication (SPF, DKIM, DMARC results), routing headers, originating IP
- Attachment analysis: file type, hash, macro presence, embedded content
- Recipient scope: how many users received the malicious email?
- Click tracking: if URL-based, how many users clicked? Which users?
- Mail flow rules: are there new mail flow rules forwarding emails externally?

**Present triage findings:**

"**Technical Triage Results:**

| Data Source | Analyzed | Key Findings | Scope Impact |
|-------------|----------|--------------|-------------|
| SIEM Logs | ✅/❌/Partial | {{summary}} | {{did this expand or confirm scope?}} |
| EDR Telemetry | ✅/❌/Partial | {{summary}} | {{did this expand or confirm scope?}} |
| Network Data | ✅/❌/Partial | {{summary}} | {{did this expand or confirm scope?}} |
| Authentication Logs | ✅/❌/Partial | {{summary}} | {{did this expand or confirm scope?}} |
| Email Analysis | ✅/❌/N/A | {{summary}} | {{did this expand or confirm scope?}} |

**New Findings from Triage:**
- {{any new IOCs discovered}}
- {{any new affected systems discovered}}
- {{any new compromised accounts discovered}}
- {{any timeline extensions (earlier start or wider activity window)}}
- {{any technique changes (new ATT&CK mappings)}}"

### 3. Severity Re-assessment

With the enriched scope data and technical triage results, re-evaluate the incident severity:

**Original Severity from Step 1:** `{incident_severity}` — `{initial_classification}` (Confidence: `{initial_classification_confidence}`)

**Re-assessment Based on New Evidence:**

| Factor | Step 1 Assessment | Step 3 Assessment | Change | Evidence |
|--------|------------------|-------------------|--------|----------|
| Scope (systems) | {{original count}} | {{updated count}} | {{expanded/same/reduced}} | {{evidence}} |
| Scope (users) | {{original count}} | {{updated count}} | {{expanded/same/reduced}} | {{evidence}} |
| Data sensitivity | {{original}} | {{updated}} | {{escalated/same/reduced}} | {{evidence}} |
| Active threat | {{original}} | {{updated}} | {{confirmed/same/reduced}} | {{evidence}} |
| Lateral movement | {{original}} | {{updated}} | {{confirmed/not detected}} | {{evidence}} |
| Data exfiltration | {{original}} | {{updated}} | {{confirmed/not detected}} | {{evidence}} |

**NIST Functional Impact Assessment:**
- **None**: No effect on the organization's ability to provide services
- **Low**: Minimal effect; the organization can still provide critical services
- **Medium**: Organization has lost the ability to provide a critical service to a subset of users
- **High**: Organization can no longer provide critical services to any users

**Functional Impact:** {{None/Low/Medium/High}} — {{justification}}

**NIST Information Impact Assessment:**
- **None**: No information was exfiltrated, changed, deleted, or compromised
- **Privacy Breach**: Sensitive PII accessed or exfiltrated
- **Proprietary Breach**: Unclassified proprietary information accessed or exfiltrated
- **Integrity Loss**: Sensitive or proprietary information changed or deleted

**Information Impact:** {{None/Privacy Breach/Proprietary Breach/Integrity Loss}} — {{justification}}

**NIST Recoverability Assessment:**
- **Regular**: Time to recovery is predictable with existing resources
- **Supplemented**: Time to recovery is predictable with additional resources
- **Extended**: Time to recovery is unpredictable; additional resources and outside help needed
- **Not Recoverable**: Recovery from the incident is not possible (e.g., sensitive data exfiltrated and posted publicly)

**Recoverability:** {{Regular/Supplemented/Extended/Not Recoverable}} — {{justification}}

**Severity Decision:**

"**Severity Re-assessment:**

| Attribute | Value |
|-----------|-------|
| Original Severity (Step 1) | CAT-{{N}} ({{label}}) |
| Adjusted Severity (Step 3) | CAT-{{N}} ({{label}}) |
| Change | {{Upgraded/Maintained/Downgraded}} |
| Functional Impact | {{level}} |
| Information Impact | {{level}} |
| Recoverability | {{level}} |

**Justification for {{Upgrade/Maintenance/Downgrade}}:**
{{detailed narrative explaining the severity decision, referencing specific new evidence from scope assessment and triage analysis}}

Do you confirm the severity {{adjustment/maintenance}}, or would you like to override?"

If severity is upgraded to CAT-1 or CAT-2: immediately flag notification requirements (see section 6).
If the operator overrides the recommended severity, document both the recommended and actual classification with the operator's reasoning.

Update frontmatter: `incident_severity: 'CAT-{{N}}'` (updated if changed)

### 4. Business Impact Assessment

Translate technical findings into business risk:

#### A. Operational Impact

| Service/System | Impact Level | Current Status | Recovery Estimate |
|---------------|-------------|---------------|-------------------|
| {{business_service}} | Critical/High/Medium/Low/None | Degraded/Offline/Functional | {{estimate}} |

- What business processes are disrupted?
- What is the cost per hour of the disruption?
- Are there workarounds available?

#### B. Financial Impact Estimate

| Cost Category | Estimate | Confidence | Notes |
|--------------|----------|------------|-------|
| Business interruption | {{estimate}} | High/Medium/Low | {{basis}} |
| Incident response costs | {{estimate}} | High/Medium/Low | {{internal + external}} |
| Regulatory fines (potential) | {{estimate}} | High/Medium/Low | {{applicable regulations}} |
| Legal costs | {{estimate}} | High/Medium/Low | {{litigation risk}} |
| Reputational damage | {{estimate}} | Low | {{difficult to quantify}} |
| Remediation costs | {{estimate}} | High/Medium/Low | {{systems, controls, training}} |

#### C. Reputational Impact

- Is customer data involved? If yes, how many customers?
- Are public-facing systems compromised? Could customers be directly affected?
- Is there media risk? (publicly traded company, high-profile organization, critical infrastructure)
- Has the breach been publicly disclosed (by the adversary or third parties)?

#### D. Regulatory Notification Obligations

Based on the data at risk and applicable jurisdictions:

| Regulation | Applicable? | Notification Timeline | Trigger Condition | Status |
|-----------|-------------|----------------------|-------------------|--------|
| GDPR (EU) | ✅/❌ | 72 hours from awareness | Personal data breach | {{not triggered / clock started at {{timestamp}}}} |
| PCI DSS | ✅/❌ | Immediate to acquirer | Cardholder data compromise | {{status}} |
| HIPAA (US) | ✅/❌ | 60 days (individual), immediate (HHS if >500) | PHI breach | {{status}} |
| SEC (US) | ✅/❌ | 4 business days (8-K filing) | Material cybersecurity incident | {{status}} |
| NIS2 (EU) | ✅/❌ | 24h early warning, 72h full notification | Significant incident | {{status}} |
| State breach notification | ✅/❌ | Varies by state | PII breach | {{status}} |
| Sector-specific | ✅/❌ | {{varies}} | {{sector requirements}} | {{status}} |

**CRITICAL:** If any notification clock has started, document the start time and calculate the deadline. Notification deadlines do not pause for investigation — they run from the moment of awareness.

#### E. Legal Implications

- Evidence preservation requirements: are there legal hold obligations?
- Law enforcement notification: is the incident criminal in nature? (ransomware, theft, espionage)
- Insurance notification: does the cyber insurance policy require notification within a specific timeframe?
- Attorney-client privilege: should legal counsel be engaged to protect investigation communications?

**Present the Business Impact Matrix:**

"**Business Impact Assessment:**

| Dimension | Impact Level | Key Concern |
|-----------|-------------|------------|
| Operational | Critical/High/Medium/Low | {{primary operational concern}} |
| Financial (estimated) | {{total estimate range}} | {{largest cost category}} |
| Reputational | High/Medium/Low | {{primary reputational concern}} |
| Regulatory | {{number of triggered obligations}} active | {{most urgent deadline}} |
| Legal | {{assessment}} | {{primary legal concern}} |

**Most Urgent Regulatory Deadline:** {{regulation}} — {{deadline timestamp}} ({{hours remaining}})"

### 5. Containment Urgency Decision

Based on all analysis — scope, triage, severity, and business impact — make the containment urgency recommendation:

**Containment Urgency Levels:**

| Level | Criteria | Timeline | Action |
|-------|----------|----------|--------|
| **IMMEDIATE** (CAT-1) | Active data exfiltration, spreading malware, ransomware in progress, critical system compromise, active insider threat | Contain NOW — minutes matter | Execute emergency containment immediately in step 4; accept potential evidence loss to stop the bleeding |
| **URGENT** (CAT-2) | Confirmed compromise, attacker has persistent access, privilege escalation achieved, C2 active but no active exfiltration | Contain within hours | Plan containment in step 4 with evidence preservation in mind; coordinate with forensics |
| **PLANNED** (CAT-3) | Suspicious activity confirmed but scope limited, no active exfiltration, no lateral movement confirmed | Contain after thorough analysis | Use steps 4-6 for careful, planned containment that maximizes evidence preservation |
| **MONITOR** (CAT-4) | Low confidence indicators, possible false positive, no confirmed compromise | Monitor and gather more data | Enhanced monitoring before containment; may not need containment if investigation disproves compromise |

**Decision Factors:**

| Factor | Finding | Urgency Impact |
|--------|---------|---------------|
| Active exfiltration | {{yes/no/unknown}} | {{HIGH if yes}} |
| Spreading/propagating | {{yes/no/unknown}} | {{HIGH if yes}} |
| Privileged access compromised | {{yes/no/unknown}} | {{HIGH if yes}} |
| C2 active | {{yes/no/unknown}} | {{MEDIUM if yes}} |
| Lateral movement | {{confirmed/suspected/none}} | {{based on finding}} |
| Data sensitivity | {{classification}} | {{based on sensitivity}} |
| Regulatory clock running | {{yes/no}} | {{HIGH if yes}} |
| Evidence at risk | {{yes/no}} | {{affects approach, not urgency}} |

**Present the containment urgency decision:**

"**Containment Urgency Recommendation:**

| Attribute | Value |
|-----------|-------|
| Recommended Urgency | {{IMMEDIATE / URGENT / PLANNED / MONITOR}} |
| Severity | CAT-{{N}} |
| Active Threat | {{assessment}} |
| Evidence Preservation | {{can we preserve before containing?}} |
| Engagement Containment Restrictions | {{restrictions from step 1, if any}} |

**Justification:**
{{detailed narrative explaining why this urgency level is recommended, referencing specific findings from scope, triage, severity, and business impact}}

**Containment Approach Preview:**
- {{high-level containment actions to expect in step 4, tailored to the urgency level}}

Do you confirm the containment urgency level? The next step will execute the containment strategy based on this decision."

Wait for operator confirmation.

Update frontmatter: `containment_status: '{{urgency level decided}}'`

### 6. Stakeholder Notification Matrix

Based on severity and business impact, determine who needs to be notified and when:

**Notification Matrix:**

| Stakeholder | Role | Notification Trigger | Urgency | Channel | Status |
|-------------|------|---------------------|---------|---------|--------|
| CISO / Security Leadership | Incident oversight | CAT-1: Immediate, CAT-2: Within 1 hour | {{urgency}} | {{phone/email/incident channel}} | {{notified/pending/not required}} |
| CTO / IT Leadership | Technical response coordination | CAT-1/CAT-2: Immediate | {{urgency}} | {{channel}} | {{status}} |
| Legal Counsel | Regulatory compliance, privilege protection | Data breach suspected or confirmed | {{urgency}} | {{channel}} | {{status}} |
| CEO / Executive Leadership | Business decision authority | CAT-1: Immediate, CAT-2: Within 4 hours | {{urgency}} | {{channel}} | {{status}} |
| PR / Communications | External messaging | Public-facing impact or media risk | {{urgency}} | {{channel}} | {{status}} |
| HR | Employee-related incidents | Insider threat or employee data breach | {{urgency}} | {{channel}} | {{status}} |
| Law Enforcement | Criminal investigation | Ransomware, theft, espionage, fraud | {{urgency}} | {{channel}} | {{status}} |
| Cyber Insurance | Claims and coverage | Per policy notification requirements | {{urgency}} | {{channel}} | {{status}} |
| Regulators | Compliance obligations | Per regulatory framework timelines | {{urgency}} | {{channel}} | {{status}} |
| Business System Owners | Affected system management | Their systems are impacted | {{urgency}} | {{channel}} | {{status}} |
| External IR Firm | Augmented response capability | Internal resources insufficient | {{urgency}} | {{channel}} | {{status}} |
| Customers / Data Subjects | Notification obligations | Per regulatory requirements | {{urgency}} | {{channel}} | {{status}} |

"**Stakeholder Notification Summary:**

**Immediate notifications required:** {{count}} stakeholders
**Notifications within 4 hours:** {{count}} stakeholders
**Notifications pending investigation:** {{count}} stakeholders

The notification matrix will be tracked in the Stakeholder Communication Log throughout the incident lifecycle."

Update frontmatter: `stakeholder_notifications: {{count of required notifications}}`

### 7. Append Findings to Report

Write the consolidated triage analysis to the output document under `## Initial Analysis & Triage`:

```markdown
## Initial Analysis & Triage

### Severity Classification
{{severity re-assessment from section 3 — original, adjusted, NIST functional/information/recoverability impacts}}

### Impact Assessment
{{business impact matrix from section 4 — operational, financial, reputational, regulatory, legal}}

### Affected Systems Inventory
{{confirmed and suspected systems from section 1A}}

### Affected Users Inventory
{{confirmed and suspected accounts from section 1B}}

### Affected Data Assessment
{{data classification and exposure risk from section 1C}}

### Escalation Decision
{{containment urgency decision from section 5 — level, justification, approach preview}}

### Notification Matrix
{{stakeholder notification matrix from section 6}}
```

Update frontmatter fields:
- `incident_severity`: updated if severity changed
- `affected_systems`: updated count
- `affected_users`: updated count
- `affected_data`: updated classification
- `lateral_movement_detected`: true/false
- `data_exfiltration_detected`: true/false
- `containment_status`: urgency level decided
- `stakeholder_notifications`: count of required notifications
- `regulatory_notifications`: count of triggered regulatory obligations

### 8. Present MENU OPTIONS

"**Initial analysis and severity triage complete.**

**Triage Summary:**
- **Severity:** CAT-{{N}} ({{label}}) — {{Maintained/Upgraded/Downgraded}} from Step 1
- **Scope:** {{system_count}} confirmed systems, {{user_count}} confirmed accounts, {{data_categories}} data categories at risk
- **Functional Impact:** {{level}} | **Information Impact:** {{level}} | **Recoverability:** {{level}}
- **Business Impact:** {{highest dimension}} is the primary concern
- **Containment Urgency:** {{IMMEDIATE/URGENT/PLANNED/MONITOR}}
- **Notifications Required:** {{count}} stakeholders, {{regulatory_count}} regulatory obligations
- **Active Threat Assessment:** {{summary}}

**Select an option:**
[A] Advanced Elicitation — Challenge the severity classification, stress-test the scope assessment, explore alternative containment urgency levels
[W] War Room — Red Team perspective: what would the attacker do next based on their current position? What capabilities do they have that we haven't accounted for? Blue Team perspective: what detection gaps exist that might mean the scope is larger than we think? What evidence should we preserve before containment potentially alerts the adversary?
[C] Continue — Proceed to Step 4: Containment Strategy & Execution (Step 4 of 10)"

#### Menu Handling Logic:

- IF A: Challenge triage conclusions — stress-test the severity classification by examining whether the evidence truly supports the assigned level, question whether the scope might be larger than assessed, explore what happens if containment is delayed vs executed immediately, challenge the business impact estimates with alternative scenarios. Process insights, ask operator if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: given the attacker's confirmed position (compromised accounts, accessed systems, mapped techniques), what is the most dangerous next move? Are they likely to escalate (exfiltrate, deploy ransomware, establish deeper persistence)? What would a competent adversary prioritize? Blue Team perspective: are we confident we've found everything? What telemetry gaps mean the scope could be larger? What evidence might we lose when we begin containment? Should we deploy additional sensors before containing? What's the risk of the adversary detecting our investigation? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating all affected fields (incident_severity, affected_systems, affected_users, affected_data, lateral_movement_detected, data_exfiltration_detected, containment_status, stakeholder_notifications, regulatory_notifications), then read fully and follow: ./step-04-containment.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, incident_severity confirmed or updated, scope counts updated, containment_status set to urgency level, stakeholder_notifications count set, and Initial Analysis & Triage section fully populated in the report], will you then read fully and follow: `./step-04-containment.md` to begin containment strategy and execution.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Scope assessed across all five domains (systems, users, data, network, cloud) with confirmed vs suspected distinction
- Technical triage conducted across all available data sources (SIEM, EDR, NDR, auth logs, email)
- Severity re-assessed with NIST functional impact, information impact, and recoverability ratings
- Severity change (if any) documented with specific evidence justification
- Operator confirmed or overrode severity with rationale recorded
- Business impact assessed across all dimensions (operational, financial, reputational, regulatory, legal)
- Regulatory notification obligations identified with deadlines and clock-start timestamps
- Containment urgency decision made with documented justification and operator confirmation
- Stakeholder notification matrix established with urgency and status for each stakeholder
- All findings appended to report under `## Initial Analysis & Triage`
- Frontmatter updated with all affected fields (severity, scope counts, containment status, notifications)
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### ❌ SYSTEM FAILURE:

- Downgrading severity without specific evidence — "it doesn't seem that bad" is not evidence
- Not distinguishing between confirmed and suspected scope — mixing certainty with suspicion corrupts decision-making
- Skipping the business impact assessment — technical triage without business context produces incomplete decisions
- Not identifying regulatory notification obligations when sensitive data is at risk
- Making the containment urgency decision without referencing scope, severity, and business impact
- Executing containment actions in this step — this step DECIDES, step 4 EXECUTES
- Not documenting the severity change justification when upgrading or downgrading
- Proceeding to containment without operator confirmation of urgency level
- Not establishing the stakeholder notification matrix
- Ignoring containment restrictions from the engagement RoE
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted and all triage results

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This step DECIDES the containment approach — it does not EXECUTE containment. Every severity change must have evidence. Every urgency decision must have documented justification. Business impact is not optional.
