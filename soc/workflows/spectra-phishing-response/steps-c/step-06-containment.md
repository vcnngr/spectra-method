# Step 6: Containment & Eradication

**Progress: Step 6 of 8** — Next: Detection & Prevention

## STEP GOAL:

Plan and coordinate comprehensive containment and eradication actions across all affected layers — email (message purge, sender blocking), accounts (password reset, session revocation, MFA reset, mailbox rule audit), endpoints (network isolation, malware removal, persistence cleanup), and infrastructure (firewall rules, DNS sinkhole, proxy blocks) — producing a structured containment action matrix that tracks each action's status and ensures no affected user or system is left uncontained.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute containment actions autonomously — ALL actions are RECOMMENDATIONS for the operator to execute
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC PHISHING ANALYST recommending and tracking containment actions — the OPERATOR executes them
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst coordinating phishing incident containment within an active security engagement
- ✅ Containment actions are RECOMMENDATIONS — the operator decides what to execute and when
- ✅ Every containment action must be tracked with status (Pending / In Progress / Complete / Deferred / Not Applicable)
- ✅ Containment prioritization follows the tier model from Step 5 — highest-interaction users first
- ✅ Eradication means removing all traces of the phishing campaign from the environment — emails, credentials, malware, persistence, attacker access

### Step-Specific Rules:

- 🎯 Focus on containment planning, action recommendations, and status tracking
- 🚫 FORBIDDEN to execute containment actions directly — the agent recommends, the operator executes
- 💬 Approach: Prioritized containment plan with specific actionable commands/procedures per action
- 📊 Every action tracked in the containment action matrix with status, owner, and timestamp
- 🔒 Containment scope is limited to assets and users identified in the Step 5 blast radius assessment
- ⚠️ Business continuity must be considered — containment actions that disrupt operations should be flagged with impact assessment

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Disabling a compromised account without first auditing mailbox rules and OAuth app consents may leave attacker persistence in place — auto-forwarding rules created by the attacker will continue to exfiltrate email even after the password is reset, and OAuth tokens remain valid until explicitly revoked; always audit before or simultaneously with password reset
  - Purging phishing emails from all mailboxes without preserving a forensic copy removes evidence that may be needed for regulatory reporting, legal proceedings, or further investigation — always ensure at least one complete copy (including headers) is preserved in the investigation file before initiating mass purge
  - Blocking a sending domain at the email gateway without verifying whether it is a legitimate compromised domain (vs a purpose-built phishing domain) may block legitimate business email — if the phishing came from a compromised account at a legitimate organization, blocking the entire domain could disrupt business communications; use targeted sender blocking (specific address) rather than domain blocking in these cases
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present containment plan organized by priority (Tier 5 → Tier 4 → Tier 3 → Tier 1-2)
- ⚠️ Present [A]/[W]/[C] menu after containment plan is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `containment_actions`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Complete phishing analysis (steps 1-4) and blast radius assessment (step 5)
- Focus: Containment and eradication actions — email, account, endpoint, infrastructure
- Limits: Actions are recommendations only — operator executes. Scope limited to blast radius from step 5.
- Dependencies: Completed scope assessment (step 5) with tier classifications and blast radius

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Containment Priority Assessment

Based on the blast radius from Step 5, establish containment priorities:

**Containment Priority Order:**

| Priority | Target | Urgency | Rationale |
|----------|--------|---------|-----------|
| P0 — IMMEDIATE | Tier 5 users (malware execution) | Within minutes | Active endpoint compromise — attacker may be pivoting |
| P1 — URGENT | Tier 4 users (credential submission) | Within 1 hour | Compromised credentials — attacker may be accessing accounts |
| P2 — HIGH | Tier 3 users (URL click) | Within 4 hours | Potential exposure — assess and contain as needed |
| P3 — STANDARD | Email purge (all tiers) | Within 8 hours | Remove phishing email from all mailboxes |
| P4 — STANDARD | Infrastructure blocking | Within 8 hours | Block attacker infrastructure at network perimeter |
| P5 — SCHEDULED | Tier 1-2 users (awareness) | Within 24 hours | Notification and awareness for low-interaction users |

### 2. Email Containment

#### A. Email Forensic Preservation

**BEFORE any purge operation, ensure forensic preservation:**

"⚠️ **PRESERVATION REQUIRED BEFORE PURGE**

Verify that a complete forensic copy of the phishing email (including full headers) is preserved:
- Location: This investigation's report file contains the raw email source (preserved in Step 1)
- Additional: If regulatory reporting may be required, preserve a separate copy in the evidence repository

Confirmation required before proceeding with email purge."

#### B. Message Search and Purge

**Email Purge Recommendations:**

**Microsoft 365 / Exchange Online:**
```powershell
# Step 1: Create compliance search
New-ComplianceSearch -Name "Phishing-{{incident_id}}" `
  -ExchangeLocation All `
  -ContentMatchQuery 'from:"{{sender_address}}" AND subject:"{{email_subject}}" AND received:{{delivery_date}}'

# Step 2: Start the search
Start-ComplianceSearch -Identity "Phishing-{{incident_id}}"

# Step 3: Review results (verify correct emails targeted)
Get-ComplianceSearch -Identity "Phishing-{{incident_id}}" | FL Items, Size

# Step 4: Purge (soft delete — recoverable from Deleted Items)
New-ComplianceSearchAction -SearchName "Phishing-{{incident_id}}" -Purge -PurgeType SoftDelete

# Step 4 (alternative): Hard delete (permanent — use only if soft delete is insufficient)
New-ComplianceSearchAction -SearchName "Phishing-{{incident_id}}" -Purge -PurgeType HardDelete

# Threat Explorer alternative (GUI):
# Security Center → Threat Explorer → Filter by sender/subject → Select all → Purge
```

**Google Workspace:**
```
# Google Admin Console → Security Investigation Tool
# Search: from:{{sender_address}} subject:"{{email_subject}}"
# Action: Delete messages from search results

# Gmail API alternative (for automation):
# Use Admin SDK → Gmail API → users.messages.trash() or users.messages.delete()
```

**Email Purge Status:**

| Action | Scope | Command/Method | Status | Verified |
|--------|-------|---------------|--------|----------|
| Search for phishing emails | All mailboxes | {{search method}} | {{Pending/Complete}} | {{count found}} |
| Soft delete phishing emails | {{count}} mailboxes | {{purge method}} | {{Pending/Complete}} | {{count deleted}} |
| Verify purge completion | All affected mailboxes | {{verification}} | {{Pending/Complete}} | {{confirmed?}} |

#### C. Sender Blocking

**Sender Block Recommendations:**

| Block Type | Target | Implementation | Scope | Notes |
|-----------|--------|---------------|-------|-------|
| Sender address block | {{sender_address}} | Transport rule / blocked sender list | Organization-wide | Blocks this specific address |
| Sender domain block | {{sender_domain}} | Transport rule / domain block | Organization-wide | ⚠️ Only if domain is purpose-built for phishing — NOT if legitimate domain was compromised |
| Reply-To address block | {{reply_to_address}} | Transport rule | Organization-wide | If Reply-To differs from From |
| Subject pattern block | "{{subject_pattern}}" | Transport rule | Organization-wide | Temporary — remove after campaign subsides |

**Microsoft 365 Transport Rule:**
```powershell
# Block sender address
New-TransportRule -Name "Block-Phishing-{{incident_id}}" `
  -From "{{sender_address}}" `
  -DeleteMessage $true `
  -Comments "Phishing containment — {{incident_id}}"

# Block sender domain (only for malicious domains)
New-TransportRule -Name "Block-Domain-{{sender_domain}}" `
  -SenderDomainIs "{{sender_domain}}" `
  -DeleteMessage $true `
  -Comments "Phishing containment — {{incident_id}}"
```

#### D. URL and Attachment Blocking (Email Gateway)

**Email Gateway Block Recommendations:**

| Block Type | Target | Implementation | Status |
|-----------|--------|---------------|--------|
| URL block | {{phishing_url_defanged}} | Email gateway URL filter / Safe Links policy | {{Pending/Complete}} |
| Attachment hash block | SHA256: {{hash}} | Email gateway hash-based blocking | {{Pending/Complete}} |
| Attachment name block | {{filename_pattern}} | Email gateway filename rule | {{Pending/Complete}} |
| Attachment extension block | {{extension if unusual}} | Email gateway extension policy | {{Pending/Complete}} |

### 3. Account Containment (Tier 4-5 Users)

For each user in Tier 4 (credential submission) and Tier 5 (malware execution), perform comprehensive account containment.

**Account Containment Checklist — Per User:**

For each compromised user, track the following actions:

**User: {{username}} — Tier {{tier}}**

| # | Action | Priority | Command/Method | Status | Notes |
|---|--------|----------|---------------|--------|-------|
| 1 | **Disable account / Force password reset** | IMMEDIATE | {{platform-specific command}} | {{Pending/Complete}} | Prevents attacker from using stolen credentials |
| 2 | **Revoke all active sessions** | IMMEDIATE | {{platform-specific command}} | {{Pending/Complete}} | Terminates any active attacker sessions |
| 3 | **Revoke all refresh tokens** | IMMEDIATE | {{platform-specific command}} | {{Pending/Complete}} | Prevents session restoration via cached tokens |
| 4 | **MFA reset** | HIGH | {{platform-specific command}} | {{Pending/Complete}} | If attacker may have enrolled their own MFA device |
| 5 | **OAuth/app consent review** | HIGH | {{platform-specific command}} | {{Pending/Complete}} | Revoke any suspicious app permissions granted post-compromise |
| 6 | **Mailbox rule audit** | HIGH | {{platform-specific command}} | {{Pending/Complete}} | Check for auto-forwarding rules created by attacker |
| 7 | **Delegate access review** | HIGH | {{platform-specific command}} | {{Pending/Complete}} | Check for delegated access grants |
| 8 | **Mobile device management** | MEDIUM | {{platform-specific command}} | {{Pending/Complete}} | Check for new device enrollments |
| 9 | **Sign-in log review** | MEDIUM | {{platform-specific command}} | {{Pending/Complete}} | Identify all post-compromise access from attacker IPs |
| 10 | **Connected applications review** | MEDIUM | {{platform-specific command}} | {{Pending/Complete}} | Check IMAP/POP/SMTP/ActiveSync connections |

**Platform-Specific Commands:**

**Microsoft 365 / Azure AD:**
```powershell
# 1. Force password reset
Set-MsolUserPassword -UserPrincipalName "{{user_upn}}" -ForceChangePassword $true

# 2. Revoke sessions (Azure AD)
Revoke-AzureADUserAllRefreshToken -ObjectId "{{user_object_id}}"

# 3. Revoke sessions (M365)
Revoke-MgUserSignInSession -UserId "{{user_upn}}"

# 4. Check MFA methods
Get-MgUserAuthenticationMethod -UserId "{{user_upn}}"

# 5. Check OAuth consents
Get-AzureADUserOAuth2PermissionGrant -ObjectId "{{user_object_id}}"

# 6. Check mailbox rules (including forwarding)
Get-InboxRule -Mailbox "{{user_upn}}" | Where {$_.ForwardTo -or $_.ForwardAsAttachmentTo -or $_.RedirectTo}
Get-Mailbox "{{user_upn}}" | FL ForwardingAddress, ForwardingSmtpAddress, DeliverToMailboxAndForward

# 7. Check delegates
Get-MailboxPermission "{{user_upn}}" | Where {$_.User -ne "NT AUTHORITY\SELF"}
Get-RecipientPermission "{{user_upn}}"

# 8. Check mobile devices
Get-MobileDevice -Mailbox "{{user_upn}}"

# 9. Sign-in logs (Azure AD Audit)
Get-AzureADAuditSignInLogs -Filter "userPrincipalName eq '{{user_upn}}'"
```

**Google Workspace:**
```
# Admin Console → Directory → Users → {{user}} → Security
# 1. Reset password (require change on next login)
# 2. Sign out user from all sessions
# 3. Review 2-Step Verification enrollment
# 4. Review third-party app access
# 5. Check email forwarding settings
# 6. Review delegated accounts
# 7. Check recently used devices
# 8. Review login activity
```

### 4. Endpoint Containment (Tier 5 Users)

For each user in Tier 5 (malware execution), coordinate endpoint containment.

**Endpoint Containment Checklist — Per Host:**

**Host: {{hostname}} — User: {{username}}**

| # | Action | Priority | Method | Status | Notes |
|---|--------|----------|--------|--------|-------|
| 1 | **Network isolation** | IMMEDIATE | EDR isolation / VLAN change / firewall rule | {{Pending/Complete}} | Prevents lateral movement and C2 communication |
| 2 | **Forensic image** | HIGH | EDR memory capture / disk image | {{Pending/Complete}} | Preserve evidence before remediation |
| 3 | **Malware quarantine** | HIGH | EDR quarantine / manual removal | {{Pending/Complete}} | Quarantine identified malware samples |
| 4 | **Persistence removal** | HIGH | Registry cleanup, scheduled task removal, service removal | {{Pending/Complete}} | Remove all identified persistence mechanisms |
| 5 | **Full endpoint scan** | MEDIUM | EDR full scan / secondary AV scan | {{Pending/Complete}} | Verify no additional malware present |
| 6 | **Credential assessment** | MEDIUM | Check for credential dumping indicators | {{Pending/Complete}} | Were credentials harvested from this endpoint? |
| 7 | **Network isolation verification** | MEDIUM | Confirm no outbound C2 | {{Pending/Complete}} | Verify isolation is effective |
| 8 | **Restoration assessment** | LOW | Determine if reimage required vs cleanup | {{Pending/Complete}} | Full reimage for critical compromise, cleanup for contained malware |

**EDR Platform Commands:**

| Platform | Network Isolation | Full Scan | Quarantine |
|----------|------------------|-----------|-----------|
| CrowdStrike | `Contain host` in Falcon console | `Scan host` / RTR `runscript` | Automatic on detection |
| SentinelOne | `Disconnect from network` in console | `Initiate scan` | `Quarantine` in Threats |
| Microsoft Defender for Endpoint | `Isolate machine` in Security Center | `Run antivirus scan` | `Stop and Quarantine` |
| Carbon Black | `Quarantine device` in CBC | `Background scan` | `Ban hash` |

### 5. Infrastructure Blocking

Block attacker infrastructure at the network perimeter:

**Infrastructure Block Recommendations:**

| # | Block Type | Target | Implementation | Status |
|---|-----------|--------|---------------|--------|
| 1 | Firewall IP block | {{C2 IPs from IOC enrichment}} | Outbound deny rule on perimeter firewall | {{Pending/Complete}} |
| 2 | DNS sinkhole | {{malicious domains}} | DNS resolver sinkhole / RPZ entry | {{Pending/Complete}} |
| 3 | Proxy URL block | {{phishing URLs, defanged}} | Web proxy / CASB URL category override | {{Pending/Complete}} |
| 4 | Proxy domain block | {{malicious domains}} | Web proxy domain block list | {{Pending/Complete}} |
| 5 | IDS/IPS signature | {{network IOCs}} | Suricata/Snort rule for C2 traffic pattern | {{Pending/Complete}} |
| 6 | TLS inspection | {{malicious domains}} | TLS decrypt for monitoring if needed | {{Pending/Complete}} |

**Firewall Rule Example:**
```
# Block outbound to phishing infrastructure
iptables -A OUTPUT -d {{c2_ip}} -j DROP
# Or firewall appliance equivalent
deny ip any host {{c2_ip}} log

# DNS sinkhole
# Add to RPZ or DNS block list:
{{malicious_domain}}. CNAME sinkhole.local.
*.{{malicious_domain}}. CNAME sinkhole.local.
```

### 6. Containment Action Matrix — Master Tracker

Consolidate ALL containment actions into a single tracking matrix:

**Containment Action Matrix — {{incident_id}}**

| # | Category | Action | Target | Priority | Status | Owner | Timestamp | Notes |
|---|----------|--------|--------|----------|--------|-------|-----------|-------|
| 1 | Email | Forensic preservation | Investigation file | P0 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 2 | Email | Email purge | {{count}} mailboxes | P3 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 3 | Email | Sender block | {{sender}} | P3 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 4 | Email | URL block (gateway) | {{urls}} | P3 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 5 | Account | Password reset | {{user}} | P1 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 6 | Account | Session revocation | {{user}} | P1 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 7 | Account | MFA reset | {{user}} | P1 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 8 | Account | Mailbox rule audit | {{user}} | P1 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 9 | Account | OAuth consent review | {{user}} | P1 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 10 | Endpoint | Network isolation | {{host}} | P0 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 11 | Endpoint | Malware quarantine | {{host}} | P0 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 12 | Endpoint | Persistence removal | {{host}} | P0 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 13 | Infra | Firewall IP block | {{IPs}} | P4 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 14 | Infra | DNS sinkhole | {{domains}} | P4 | {{status}} | {{who}} | {{when}} | {{notes}} |
| 15 | Infra | Proxy URL block | {{URLs}} | P4 | {{status}} | {{who}} | {{when}} | {{notes}} |

**Containment Statistics:**
```
Total Actions: {{count}}
- Complete: {{count}} ({{%}})
- In Progress: {{count}} ({{%}})
- Pending: {{count}} ({{%}})
- Deferred: {{count}} ({{%}})
- N/A: {{count}} ({{%}})

Categories:
- Email: {{count}} actions
- Account: {{count}} actions ({{users_affected}} users)
- Endpoint: {{count}} actions ({{hosts_affected}} hosts)
- Infrastructure: {{count}} actions
```

### 7. Present Containment Summary to User

"**Containment Plan Complete — {{incident_id}}**

**Containment Status:**
- Total actions recommended: {{count}}
- Actions by priority: P0 (IMMEDIATE): {{count}} | P1 (URGENT): {{count}} | P2-P5: {{count}}

**Email Containment:**
- Emails to purge: {{count}} across {{mailbox_count}} mailboxes
- Sender blocks: {{count}} (address: {{count}}, domain: {{count}})
- URL/attachment blocks: {{count}}

**Account Containment:**
- Accounts requiring password reset: {{count}}
- Accounts requiring session revocation: {{count}}
- Accounts requiring MFA reset: {{count}}
- Mailbox rules to audit: {{count}}

**Endpoint Containment:**
- Hosts requiring network isolation: {{count}}
- Hosts requiring malware removal: {{count}}
- Hosts requiring full reimage: {{count}}

**Infrastructure Blocking:**
- IPs to block: {{count}}
- Domains to sinkhole: {{count}}
- URLs to block at proxy: {{count}}

All actions are documented in the Containment Action Matrix. Please execute the actions in priority order and update the status as each is completed."

### 8. Present MENU OPTIONS

"**Select an option:**
[A] Advanced Elicitation — Deep-dive into specific containment actions, review platform-specific commands, assess containment gaps
[W] War Room — Red vs Blue discussion on containment effectiveness — would this containment plan stop the attacker? What gaps remain?
[C] Continue — Proceed to Detection & Prevention (Step 7 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive containment planning — review specific actions in detail, provide additional platform-specific commands, assess whether containment scope is adequate, identify potential gaps (e.g., mobile devices, VPN access, partner portals), verify forensic preservation is complete. Process insights, ask user if they want to update the plan, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: if I were the attacker, what would I do in the time between detection and containment? Which persistence mechanisms would I use that this containment plan doesn't address? How would I maintain access despite password resets? Blue Team perspective: is our containment plan sequenced correctly? Are we blocking at the right layers? What would we miss? How do we verify containment is effective? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `containment_actions`, then read fully and follow: ./step-07-detection.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and containment_actions count updated, and containment plan appended to report under `## Containment & Eradication`], will you then read fully and follow: `./step-07-detection.md` to begin detection and prevention improvement.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Containment priorities established based on Step 5 tier classifications
- Forensic preservation verified before any purge operations recommended
- Email containment plan includes: search/purge, sender blocking, URL blocking, attachment blocking
- Account containment plan includes: password reset, session revocation, MFA reset, mailbox rule audit, OAuth review, delegate review
- Endpoint containment plan includes: network isolation, malware quarantine, persistence removal, full scan
- Infrastructure blocking plan includes: firewall rules, DNS sinkhole, proxy blocks
- Platform-specific commands provided for each action
- All actions tracked in the master containment action matrix with status, owner, and timestamp
- Containment statistics summarized (total, complete, pending, by category)
- All containment actions are RECOMMENDATIONS — operator executes
- Business continuity impact considered for disruptive actions
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Executing containment actions autonomously instead of recommending them to the operator
- Recommending email purge before verifying forensic preservation
- Blocking a legitimate domain that was compromised (instead of blocking the specific sender address)
- Not providing platform-specific commands for containment actions
- Not tracking containment actions in the master matrix
- Missing any containment layer (email, account, endpoint, infrastructure)
- Not prioritizing containment based on user interaction tiers
- Beginning detection engineering or reporting during containment planning
- Recommending account containment without mailbox rule and OAuth audit
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with containment_actions count and stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Containment actions are recommendations — the operator executes. Forensic preservation before purge. Every layer must be addressed.
