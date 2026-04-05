# Step 6: Active Directory Privilege Escalation

**Progress: Step 6 of 10** — Next: Cloud Privilege Escalation

## STEP GOAL:

Execute Active Directory-specific privilege escalation techniques to move from domain user to Domain Admin or equivalent. Exploit Kerberos weaknesses, ACL misconfigurations, delegation abuse, certificate services, and AD-specific attack paths. Document all attempts with full ATT&CK mapping.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify AD schema or Group Policy Objects without explicit operator authorization
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN ATTACK OPERATOR executing authorized Active Directory escalation
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Active Directory escalation ONLY — local OS was steps 04-05, cloud is step-07
- ⚡ If step-01 classified AD as N/A (not domain-joined), perform brief applicability confirmation then proceed to [C]
- 📋 Every technique attempted must be logged: technique, T-code, result, artifacts
- 🩸 BloodHound collection is RECOMMENDED as first action — maps all attack paths
- 🔄 Start with credential-based attacks (Kerberoast, AS-REP), then move to ACL/delegation abuse
- 🎯 Target: Domain Admin, Enterprise Admin, or equivalent high-privilege AD group

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive actions ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - DCSync (T1003.006) triggers alerts on most mature SOCs — assess detection capability and consider whether you need this technique vs alternatives before executing
  - Kerberoasting at scale generates detectable Kerberos TGS-REQ traffic patterns — request tickets for specific high-value SPNs rather than bulk requesting
  - ADCS certificate abuse may issue certificates with long validity that persist well beyond engagement timeline — track all certificates issued for post-engagement revocation
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present AD escalation plan before beginning
- ⚠️ Present [A]/[W]/[C] menu after all AD escalation techniques are assessed
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Step-02 enumeration (domain info, users, groups), step-03 credentials (domain creds, hashes, tickets), steps 04-05 escalation results (local admin achieved?)
- Focus: AD domain privilege escalation — moving from domain user toward Domain Admin
- Limits: Stay within RoE for AD scope. Do NOT modify GPOs or AD schema without explicit authorization. Log all domain modifications.
- Dependencies: step-02-local-enum.md, step-03-credential-discovery.md; local admin from step-04/05 is helpful but not required

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check

**Determine if Active Directory escalation applies to this engagement:**

- IF NOT domain-joined environment → document "N/A — standalone/workgroup host, no AD attack surface" → proceed to Menu → [C]
- IF domain-joined → assess current domain context and populate:

| Field | Value |
|-------|-------|
| Domain Name | {{domain}} |
| Domain Controller(s) | {{DCs}} |
| Current Domain User | {{user}} |
| Domain Groups (current user) | {{groups}} |
| Local Admin on Current Host? | {{yes/no}} |
| Local Admin on DC? | {{yes/no}} |
| Domain Functional Level | {{level}} |
| Trust Relationships | {{trusts}} |
| Credentials Available | {{creds_summary — plaintext/hashes/tickets from step-03}} |

**Current access assessment:**
- What domain privileges do we have right now?
- What is the shortest theoretical path from current access to Domain Admin?
- Which attack categories are viable given current credentials?

### 2. AD Enumeration & BloodHound Collection

**BloodHound/SharpHound collection (RECOMMENDED first action):**

Collection methods and detection risk:

| Method | Data Collected | Detection Risk | Use When |
|--------|---------------|----------------|----------|
| All | Full domain data | HIGH — queries every object, generates significant LDAP traffic | Lab/low-maturity SOC |
| DCOnly | Users, groups, GPOs, trusts from DC | MEDIUM — DC-focused queries | Prefer over All in monitored environments |
| Session | Logged-on sessions | MEDIUM — NetSessionEnum calls across hosts | Need session data for lateral paths |
| LoggedOn | Logged-on users via registry | HIGH — requires local admin on targets | When you have widespread local admin |

**After collection, identify and prioritize:**
1. Shortest path to Domain Admin
2. Kerberoastable accounts (accounts with SPNs)
3. AS-REP roastable accounts (no preauth required)
4. Unconstrained delegation hosts
5. Constrained delegation services
6. ACL abuse paths (GenericAll, WriteDACL, WriteOwner, etc.)
7. ADCS vulnerable certificate templates
8. Cross-domain trust relationships for pivoting

**Manual enumeration alternatives (if BloodHound collection not viable):**

| Target | Tool/Command | Purpose |
|--------|-------------|---------|
| Domain users/groups | PowerView Get-DomainUser / Get-DomainGroup | Map accounts and memberships |
| SPNs | PowerView Get-DomainUser -SPN | Identify Kerberoast targets |
| No preauth | PowerView Get-DomainUser -PreauthNotRequired | Identify AS-REP roast targets |
| Delegation | PowerView Get-DomainComputer -Unconstrained | Find unconstrained delegation hosts |
| Constrained delegation | PowerView Get-DomainComputer -TrustedToAuth | Find constrained delegation services |
| ACLs | PowerView Get-DomainObjectAcl -ResolveGUIDs | Permission analysis on key objects |
| GPOs | PowerView Get-DomainGPO | GPO abuse targets |
| Trusts | nltest /domain_trusts, Get-DomainTrust | Cross-domain pivoting opportunities |
| ADCS | Certify find / certipy find | Certificate template vulnerability analysis |
| LAPS | PowerView Get-DomainComputer -Properties ms-Mcs-AdmPwd | LAPS password retrieval |
| gMSA | PowerView Get-DomainObject -LDAPFilter '(objectClass=msDS-GroupManagedServiceAccount)' | gMSA password extraction targets |

**Present enumeration summary:**
```
| Category | Count | High-Value Targets | Notes |
|----------|-------|-------------------|-------|
```

### 3. Kerberoasting (T1558.003)

Attack Kerberos TGS by requesting service tickets for SPN-registered accounts and cracking them offline:

**Process:**
1. Identify accounts with SPNs (from BloodHound or manual enumeration)
2. Prioritize targets: service accounts with admin group membership, accounts with weak password policies, accounts with old password last set dates
3. Request TGS tickets: `Rubeus kerberoast` / `GetUserSPNs.py`
4. Extract ticket hashes
5. Offline cracking with hashcat (mode 13100 for RC4, mode 19700 for AES) or john

**Targeted vs Bulk approach:**
- TARGETED (preferred): request tickets for specific high-value accounts — service accounts with admin access, accounts with old passwords, accounts with weak policy
- BULK: request all available TGS — higher detection risk, generates significant Kerberos traffic

| SPN Account | Service | Password Last Set | Admin Groups | Ticket Hash (preview) | Crackable? | Cracked Password |
|-------------|---------|-------------------|--------------|----------------------|------------|-----------------|
| {{account}} | {{svc}} | {{date}} | {{groups}} | {{hash_first_32}} | {{yes/no/pending}} | {{password_or_N/A}} |

**Evasion considerations:**
- Use AES encryption type requests instead of RC4 where possible (less anomalous)
- Space out ticket requests to avoid burst detection
- Target specific SPNs rather than wildcard queries

### 4. AS-REP Roasting (T1558.004)

Attack accounts without Kerberos pre-authentication required:

**Process:**
1. Identify accounts with DONT_REQUIRE_PREAUTH flag set (from enumeration)
2. Request AS-REP: `Rubeus asreproast` / `GetNPUsers.py`
3. Extract AS-REP hashes
4. Offline cracking with hashcat (mode 18200) or john

| Account | DONT_REQUIRE_PREAUTH | AS-REP Hash (preview) | Crackable? | Cracked Password | Domain Groups |
|---------|---------------------|----------------------|------------|-----------------|---------------|
| {{account}} | {{yes}} | {{hash_first_32}} | {{yes/no/pending}} | {{password_or_N/A}} | {{groups}} |

**Note:** AS-REP roasting is lower detection risk than Kerberoasting — no TGS request, just standard AS-REQ without preauth data.

### 5. Delegation Abuse

**5a. Unconstrained Delegation**

Hosts with unconstrained delegation store the TGT of any user who authenticates to them:

- **Discovery:** Find computers with `TRUSTED_FOR_DELEGATION` flag
- **Attack:** Coerce authentication from a high-value target (DC, admin) → capture their TGT → use TGT for impersonation
- **Coercion methods:**
  - PrinterBug / SpoolSample — trigger Print Spooler callback
  - PetitPotam — trigger LSARPC EfsRpcOpenFileRaw callback
  - DFSCoerce — trigger DFS-based callback
- **Execution:** `Rubeus monitor /interval:5` to capture incoming TGTs → `Rubeus ptt` to inject
- **Escalation path:** Coerce DC authentication → capture DC$ TGT → DCSync

**5b. Constrained Delegation**

Services configured with `msDS-AllowedToDelegateTo`:

- **Discovery:** Find accounts/computers with constrained delegation configured
- **Attack:** Use S4U2Self + S4U2Proxy to impersonate any user to the allowed target service
- **Execution:**
  - `Rubeus s4u /impersonateuser:Administrator /msdsspn:{{target_spn}} /user:{{delegation_account}}`
  - `getST.py -spn {{target_spn}} -impersonate Administrator {{domain}}/{{account}}`
- **Key insight:** If protocol transition is enabled (TRUSTED_TO_AUTH_FOR_DELEGATION), you can impersonate ANY user without their interaction

**5c. Resource-Based Constrained Delegation (RBCD)**

Write to `msDS-AllowedToActOnBehalfOfOtherIdentity` on a target computer:

- **Prerequisites:** WriteDACL, GenericWrite, or GenericAll on target computer object
- **Attack sequence:**
  1. Create or use existing machine account (default: MachineAccountQuota = 10)
  2. Write RBCD attribute on target computer pointing to controlled machine account
  3. S4U2Self + S4U2Proxy from controlled machine account → impersonate admin to target
- **Tools:** `Rubeus`, `PowerView Set-DomainObject`, `Impacket rbcd.py + getST.py`
- **Detection:** Modification of `msDS-AllowedToActOnBehalfOfOtherIdentity` generates event 5136 (Directory Service Changes)

| Delegation Type | Target | Account/Host | Attack Path | Result | Artifacts |
|----------------|--------|-------------|-------------|--------|-----------|
| {{type}} | {{target}} | {{account}} | {{path}} | {{result}} | {{artifacts}} |

### 6. ACL Abuse

Based on BloodHound ACL analysis or manual enumeration, identify and exploit abusable permissions:

| Permission | On Object | Attack | Result |
|-----------|-----------|--------|--------|
| GenericAll | User | Reset password / set SPN → targeted Kerberoast | Account takeover |
| GenericAll | Group | Add self to group | Privilege elevation |
| GenericAll | Computer | RBCD attack / LAPS password read | Computer admin |
| GenericWrite | User | Set SPN → targeted Kerberoast, modify logon script | Credential/code exec |
| GenericWrite | Computer | Write msDS-AllowedToActOnBehalfOfOtherIdentity → RBCD | Computer admin |
| WriteDACL | Any object | Grant self GenericAll → full control | Full control |
| WriteOwner | Any object | Take ownership → WriteDACL → GenericAll | Full control |
| ForceChangePassword | User | Reset password without knowing current | Account takeover |
| AddMember | Group | Add controlled user to privileged group | Group membership |
| AllExtendedRights | Domain | DCSync (Replicating Directory Changes) | Full credential dump |
| AllExtendedRights | User | Read LAPS password / change password | Account takeover |
| ReadGMSAPassword | gMSA | Read gMSA password blob | Service account takeover |

**For each abusable ACL found:**
```
### ACL-{{num}}: {{permission}} on {{object}}
- Source principal: {{who has the permission}}
- Target object: {{what it applies to}}
- Attack: {{technique to exploit}}
- Execution: {{exact command/tool}}
- Result: {{what was achieved}}
- Artifacts: {{logs, events, modifications made}}
```

**ACL chain attacks:** Multiple ACL abuses can be chained — e.g., GenericWrite on User A → Set SPN → Kerberoast → crack → User A has WriteDACL on Group B → add self → Group B has DCSync rights.

### 7. ADCS Certificate Abuse (T1649)

If Active Directory Certificate Services (ADCS) exists in the environment:

**Discovery:** `Certify find` / `certipy find -u {{user}} -p {{pass}} -dc-ip {{dc_ip}}`

| ESC | Vulnerability | Condition | Exploitation | Tool |
|-----|--------------|-----------|-------------|------|
| ESC1 | Client auth template allows SAN, enrollee supplies SAN | Template: Client Auth EKU + CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT + enrollment rights | Request cert with SAN of DA → authenticate as DA | Certify/Certipy |
| ESC2 | Template with Any Purpose or SubCA EKU | Template: Any Purpose/SubCA EKU + enrollment rights | Request cert → use for client auth as any principal | Certify |
| ESC3 | Enrollment agent template | Template: Certificate Request Agent EKU | Enroll as agent → co-sign cert request for DA | Certify chain |
| ESC4 | Vulnerable template ACLs | WriteDACL/Owner on certificate template | Modify template → enable ESC1 conditions → exploit | Certify + template modify |
| ESC6 | EDITF_ATTRIBUTESUBJECTALTNAME2 flag | CA-level flag set on the CA | Any template request can specify SAN → request as DA | Certify |
| ESC7 | Vulnerable CA ACLs | ManageCA or ManageCertificates permission | Approve pending requests / enable SubCA | Certipy |
| ESC8 | NTLM relay to HTTP enrollment | Web enrollment endpoint enabled | Coerce auth → relay to enrollment → get cert as target | ntlmrelayx + PetitPotam |
| ESC9 | No security extension (szOID_NTDS_CA_SECURITY_EXT) | StrongCertificateBindingEnforcement = 0 or 1 | GenericWrite on user → change UPN → request cert → authenticate | Certipy |
| ESC10 | Weak certificate mapping | CertificateMappingMethods includes UPN mapping | Similar to ESC9 — change UPN → request → auth | Certipy |

**For each finding:**
```
| Template/CA | ESC Type | Vulnerability | Exploitation Steps | Certificate Obtained | Impersonation Target | Cert Validity |
|-------------|----------|--------------|-------------------|---------------------|---------------------|---------------|
```

**CRITICAL:** Track ALL certificates issued during ADCS exploitation for post-engagement revocation. Certificates persist beyond password changes and can provide long-term unauthorized access if not revoked.

### 8. DCSync (T1003.006)

**Prerequisites:** Account must have Replicating Directory Changes + Replicating Directory Changes All permissions (typically Domain Admins, Enterprise Admins, DC computer accounts, or accounts granted these via ACL abuse).

**Before executing DCSync, confirm:**
- [ ] Lower-detection techniques have been attempted first (Kerberoast, AS-REP, delegation, ACL)
- [ ] Detection risk has been assessed with operator
- [ ] Current account actually has the required replication permissions

**Execution:**
- `secretsdump.py -just-dc {{domain}}/{{user}}:{{pass}}@{{dc_ip}}`
- `mimikatz lsadump::dcsync /domain:{{domain}} /user:{{target_user}}`

**Priority extraction targets:**
1. `krbtgt` — enables Golden Ticket creation
2. Domain Admin accounts — direct high-privilege access
3. Service accounts — lateral movement, persistence
4. KRBTGT history — assess if krbtgt has been rotated recently

**Detection:** VERY HIGH — most mature SOCs alert on DRS-Replication events (Event ID 4662 with GUID for DS-Replication-Get-Changes). Microsoft Defender for Identity (MDI) specifically detects DCSync.

| Target Account | NTLM Hash (preview) | Hash Type | Purpose | Extracted |
|---------------|---------------------|-----------|---------|-----------|
| {{account}} | {{hash_first_16}}... | {{NT/LM/AES}} | {{golden_ticket/impersonation/lateral}} | {{yes/no}} |

### 9. Ticket Forging

**Silver Ticket (T1558.002):**
- **Requires:** Service account NTLM hash + domain SID
- **Creates:** Forged TGS for a specific service — no DC interaction required
- **Use case:** Access specific services (CIFS, HTTP, MSSQL, LDAP) without touching DC
- **Duration:** Default 10 hours (can be set to any value)
- **Detection:** Lower than Golden Ticket — no DC interaction, but event 4624 with unusual ticket fields
- **Execution:** `Rubeus silver /service:{{spn}} /rc4:{{hash}} /user:Administrator /domain:{{domain}} /sid:{{sid}}`

**Golden Ticket (T1558.001):**
- **Requires:** krbtgt NTLM hash + domain SID
- **Creates:** Forged TGT — impersonate ANY user including non-existent users
- **Duration:** Up to 10 years by default
- **Detection:** HIGH — ticket lifetime anomalies, domain controller validation mismatches, Event 4769 with unusual encryption types
- **WARN:** Creates long-lived persistence artifact — track for post-engagement cleanup
- **Execution:** `Rubeus golden /rc4:{{krbtgt_hash}} /user:Administrator /domain:{{domain}} /sid:{{sid}} /id:500`

**Diamond Ticket (variation):**
- **Requires:** krbtgt AES key
- **Creates:** Legitimate TGT that is modified — harder to detect than Golden Ticket
- **Advantage:** Passes KDC validation checks that catch traditional Golden Tickets
- **Execution:** `Rubeus diamond /krbkey:{{aes256_key}} /user:{{user}} /password:{{pass}} /enctype:aes /domain:{{domain}}`

| Ticket Type | Target | Key Material | Duration Set | Impersonated User | Result |
|------------|--------|-------------|-------------|-------------------|--------|
| {{type}} | {{service_or_domain}} | {{hash_type}} | {{duration}} | {{user}} | {{success/fail}} |

### 10. GPO Abuse

**If current user has GPO modification rights (identified via BloodHound GPC/GPO edge analysis):**

| GPO Attack | Method | Impact | Detection |
|-----------|--------|--------|-----------|
| Immediate Scheduled Task | Deploy task via GPO Immediate Scheduled Task | Code execution on all hosts in GPO scope | Event 4698 (task creation), Group Policy refresh events |
| Startup/Logon Script | Add script to GPO User/Computer configuration | Code execution at next logon/startup | Group Policy Application events, script execution events |
| Software Installation | Deploy MSI via GPO Software Installation | Arbitrary software deployment | Event 1033/1034 (Software Installation), MSI logs |
| Restricted Groups | Modify Restricted Groups to add user to local Admins | Local admin on all GPO-scoped hosts | Event 4732 (member added to group), GPO modification events |
| Security Settings | Modify security policy (audit, firewall, etc.) | Weaken defenses across GPO scope | GPO version change, security policy events |

**Tools:** `SharpGPOAbuse`, `PowerView New-GPOImmediateTask`, `pyGPOAbuse`

**CRITICAL:** GPO modifications affect all hosts/users in the GPO's scope. Confirm scope before execution. Log all GPO changes for post-engagement rollback.

### 11. Compile Escalation Results & Present Menu

**Present AD attack path summary:**

| Attempt | Technique | T-Code | Target | Result | Artifacts | Detection Risk |
|---------|-----------|--------|--------|--------|-----------|---------------|
| AD-001 | {{technique}} | T{{code}} | {{target}} | Success/Fail | {{artifacts}} | {{events_generated}} |
| AD-002 | {{technique}} | T{{code}} | {{target}} | Success/Fail | {{artifacts}} | {{events_generated}} |

**AD escalation path diagram** (present as text):
```
domain_user → [technique_1] → intermediate_access → [technique_2] → Domain Admin
  Example: domain_user → [Kerberoast svc_sql] → svc_sql → [GenericAll on DA group] → Domain Admin
```

**Highest privilege achieved:**
- Account: {{account}}
- Domain groups: {{groups}}
- Equivalent to Domain Admin: {{yes/no}}
- Persistence established: {{yes/no — via tickets, certificates, etc.}}

**Certificates issued (for post-engagement tracking):**

| Certificate | Template | Issued For | Valid Until | Revocation Needed |
|-------------|----------|-----------|-------------|-------------------|
| {{cert_thumbprint}} | {{template}} | {{subject}} | {{expiry}} | {{yes/no}} |

**Write findings under `## Active Directory Escalation`:**

```markdown
## Active Directory Escalation

### Summary
- Domain: {{domain}}
- Starting access: {{initial_domain_user}}
- Highest privilege achieved: {{final_access}}
- Techniques attempted: {{technique_count}}
- Successful techniques: {{success_count}}
- Attack path chain: {{path_diagram}}
- Certificates issued: {{cert_count}} (tracked for revocation)

### Domain Context
{{domain_context_table}}

### Enumeration Results
{{enumeration_summary}}

### Kerberos Attacks
{{kerberoast_and_asrep_tables}}

### Delegation Abuse
{{delegation_results}}

### ACL Abuse
{{acl_abuse_results}}

### ADCS Exploitation
{{adcs_results_and_certificate_tracking}}

### DCSync / Credential Extraction
{{dcsync_results}}

### Ticket Forging
{{ticket_results}}

### GPO Abuse
{{gpo_results}}

### Full Attack Path
{{attack_path_diagram_and_chain}}

### Artifacts & IOCs Generated
{{detection_events_and_artifacts}}
```

Update frontmatter metrics.

### 12. Present MENU OPTIONS

"**Active Directory escalation completed.**

Summary: {{technique_count}} techniques assessed, {{success_count}} successful.
Starting access: {{initial_access}} | Highest achieved: {{final_access}}
Attack path: {{path_summary}}
Certificates tracked: {{cert_count}} for post-engagement revocation

**Select an option:**
[A] Advanced Elicitation — Deep analysis of a specific AD attack path (alternative chains, missed paths, persistence implications)
[W] War Room — Red (alternative AD escalation chains, unexploited paths, persistence options) vs Blue (AD-specific detection analysis — ATA/MDI alerts, Event IDs 4662/4769/4768, LDAP query anomalies, Kerberos encryption downgrades)
[C] Continue — Proceed to Cloud Privilege Escalation (Step 7 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the chosen attack path. Were there shorter paths? Did BloodHound reveal chains we didn't exploit? Are there alternative paths if the primary is burned? Analyze persistence quality — are forged tickets detectable? Will certificate abuse survive krbtgt rotation? Assess OPSEC — what artifacts were left, what events were generated, what would MDI flag? Process insights, ask user if they want to refine approach, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: what alternative escalation chains exist? What paths weren't attempted and why? Can we achieve the same result with lower detection risk? What persistence mechanisms survive remediation (password reset, krbtgt rotation, cert revocation)? Blue Team perspective: which Event IDs would fire (4662, 4769, 4768, 4724, 5136, 4732)? What would MDI/ATA flag (DCSync, Kerberoast, suspicious replication, unusual LDAP queries)? What Sigma/YARA rules would catch this? What forensic artifacts persist on domain controllers? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted, then read fully and follow: ./step-07-cloud-escalation.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Active Directory Escalation section populated], will you then read fully and follow: `./step-07-cloud-escalation.md` to begin cloud privilege escalation.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- BloodHound collection completed (or manual enumeration equivalent performed)
- All applicable AD attack paths assessed systematically
- Kerberos attacks (Kerberoast, AS-REP) attempted before ACL/delegation abuse
- DCSync attempted ONLY after lower-detection techniques
- Every technique logged with T-code, result, and artifacts
- Attack path chains documented with full escalation diagram
- All certificates issued during ADCS exploitation tracked for post-engagement revocation
- Domain context table populated
- Findings appended to report under `## Active Directory Escalation`
- stepsCompleted updated in frontmatter

### SYSTEM FAILURE:

- Attempting DCSync before exhausting lower-detection methods (Kerberoast, AS-REP, delegation, ACL)
- Bulk Kerberoasting without targeting high-value SPNs first
- Not tracking certificates issued during ADCS exploitation
- Skipping applicability check for non-domain-joined environments
- Not documenting the full attack chain from initial access to highest privilege
- Modifying GPOs or AD schema without explicit operator authorization
- Not logging technique, T-code, result, and artifacts for every attempt
- Proceeding without user selecting 'C' (Continue)
- Not assessing detection risk before high-noise techniques

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every technique logged, every certificate tracked, every attack path documented. Credential-based attacks before modification-based attacks. Always.