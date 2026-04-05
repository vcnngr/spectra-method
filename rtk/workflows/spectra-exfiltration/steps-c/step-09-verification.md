# Step 9: Exfiltration Verification & Cleanup

**Progress: Step 9 of 10** — Next: Documentation & Engagement Closure

## STEP GOAL:

Verify all exfiltrated data for integrity and completeness against the original target list, conduct comprehensive artifact cleanup across all compromised systems used during exfiltration (staging hosts, pivot infrastructure, deployed tools), remove all persistence mechanisms and staging infrastructure, verify cleanup completeness, prepare the evidence chain for the engagement report, and conduct a final OPSEC assessment before engagement closure. This step is the quality gate between operational execution and formal reporting — every claimed exfiltration must be verified, every artifact accounted for, and every trace addressed.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER attempt new exfiltration or lateral movement during verification — this is a confirmation and cleanup step
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN ATTACK OPERATOR verifying exfiltration results, cleaning artifacts, and preparing the evidence chain for reporting
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Verification and cleanup ONLY — no new exfiltration or lateral movement
- 🔐 Data integrity is non-negotiable — every exfiltrated file must match source checksums
- 🧹 Cleanup must be comprehensive — every artifact from steps 02-08 must be accounted for
- 📋 Evidence chain must be maintained for the engagement report — document what was taken, when, how, and through which channel
- ⚠️ Cleanup failures must be documented — if an artifact cannot be removed, report it with justification
- 🔒 Verify ALL data integrity BEFORE beginning cleanup — once access is removed, re-extraction is impossible

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Cleanup actions themselves generate logs (file deletion events, service removal events, scheduled task removal) that may alert defenders — pace cleanup deliberately and use low-noise deletion methods to avoid triggering incident response during the cleanup phase
  - Removing persistence mechanisms before verifying exfiltration completeness risks losing access if re-extraction is needed — verify ALL data integrity before beginning ANY cleanup operations
  - If the engagement requires proof of exfiltration (sample data retained on operator infrastructure), ensure data handling complies with RoE — encrypt at rest, apply strict access controls, and plan for secure deletion per engagement terms and timeline
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Verify all exfiltrated data integrity and completeness before any cleanup
- ⚠️ Present [A]/[W]/[C] menu after verification, cleanup, and OPSEC assessment complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: ALL prior step results (01-08), exfiltration targets, data staging locations, transfer records, DLP evasion results, all channels used
- Focus: Data integrity verification, artifact cleanup, evidence chain documentation, OPSEC assessment, secure data handling
- Limits: Do NOT attempt new exfiltration, lateral movement, or data access. This is verification and cleanup only. Read-only access to verify checksums — no new data collection.
- Dependencies: All steps 01-08 (especially steps 02-03 for target list, steps 04-07 for staging and transfer details, step 08 for DLP evasion artifacts)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Exfiltration Completeness Check

**Cross-reference exfiltrated data against the prioritized target list from step-03:**

| Target ID | Data Category | Source System | Source Path | Priority | Exfiltrated? | Volume Match? | Channel Used | Transfer Date | Notes |
|-----------|--------------|---------------|------------|----------|-------------|--------------|-------------|---------------|-------|
| DT-001 | {{PII/Financial/IP/Config}} | {{hostname}} | {{path}} | P1/P2/P3 | ✅/❌ | ✅/❌/Partial | {{network/cloud/covert/email}} | {{date}} | {{notes}} |
| DT-002 | {{category}} | {{host}} | {{path}} | {{priority}} | ✅/❌ | ✅/❌/Partial | {{channel}} | {{date}} | {{notes}} |

**Gap Analysis:**

For each target NOT exfiltrated or partially exfiltrated:

```
TARGET GAP: DT-{{NNN}} — {{data_category}} on {{system}}
Status: Not exfiltrated / Partially exfiltrated
Reason:
├── Access lost before transfer could complete
├── DLP blocked the transfer channel (step-08 evasion insufficient)
├── Volume too large for available bandwidth in engagement window
├── Data format incompatible with exfiltration method
├── Time constraints — engagement window closing
└── {{other_reason}}

Impact on engagement objectives:
{{Does this gap affect the engagement goals? Is the remaining exfiltrated data
sufficient to demonstrate the risk? Should we attempt re-extraction or accept the gap?}}
```

**Present Exfiltration Completeness Matrix:**

```
EXFILTRATION COMPLETENESS — {{engagement_name}}
Date: {{date}}

Total data targets identified (step-03): {{count}}
Successfully exfiltrated: {{count}} ({{percentage}}%)
Partially exfiltrated: {{count}}
Not exfiltrated: {{count}}
Total volume exfiltrated: {{size}}

Priority 1 targets: {{exfiltrated}}/{{total}} ({{percentage}}%)
Priority 2 targets: {{exfiltrated}}/{{total}} ({{percentage}}%)
Priority 3 targets: {{exfiltrated}}/{{total}} ({{percentage}}%)

Channels used: {{list of channels with volume per channel}}
```

### 2. Data Integrity Verification

**For EACH exfiltrated file or archive, verify integrity end-to-end:**

#### Checksum Verification

```bash
# Generate SHA-256 checksums on SOURCE system BEFORE cleanup
# This must be done while we still have access to source data

# Windows source
Get-FileHash -Algorithm SHA256 -Path "C:\path\to\original\file.xlsx" | Format-List

# Linux source
sha256sum /path/to/original/file.csv

# Compare with received file on operator system
sha256sum received_file.csv
# SHA-256 must match exactly — any mismatch = corrupted transfer
```

#### Decryption Verification

```bash
# Verify all encrypted archives can be decrypted
# For each encrypted archive used during exfiltration:

# 7-Zip encrypted archive
7z t -p"password" archive.7z
# "Everything is Ok" = integrity verified

# GPG encrypted file
gpg --batch --passphrase "password" -d encrypted_file.csv.gpg > /dev/null
echo $?  # 0 = success

# OpenSSL encrypted file
openssl enc -aes-256-cbc -d -pbkdf2 -in encrypted.bin -out /dev/null -pass pass:password
echo $?  # 0 = success

# age encrypted file
age -d -i key.txt encrypted.age > /dev/null
echo $?
```

#### Decompression Verification

```bash
# Verify all compressed files can be extracted completely

# 7z archive
7z t archive.7z  # Test integrity without extracting

# ZIP archive
unzip -t archive.zip

# TAR.GZ archive
tar -tzf archive.tar.gz > /dev/null
echo $?  # 0 = all files listed successfully

# Split files — verify reassembly
cat part_aa part_ab part_ac part_ad > reassembled.7z
sha256sum reassembled.7z  # Compare with original pre-split checksum
```

#### Content Spot-Check

```bash
# For each major data category, spot-check content completeness:

# Database dumps — verify row counts
wc -l exfiltrated_table.csv  # Compare with source row count
head -5 exfiltrated_table.csv  # Verify headers and sample data

# File archives — verify file count
tar -tzf archive.tar.gz | wc -l  # Compare with source file count
7z l archive.7z | grep "files"

# Documents — verify readable (not truncated)
file exfiltrated_document.docx  # Should show "Microsoft Word" not "data"
pdfinfo exfiltrated_report.pdf  # Should show page count matching source

# Credentials / config files — verify content is actionable
cat exfiltrated_config.yaml | head -20  # Verify structure and content
```

**Present Integrity Verification Results:**

| File/Archive | Source SHA-256 | Received SHA-256 | Match | Decryptable | Extractable | Content Verified | Status |
|-------------|---------------|------------------|-------|------------|------------|-----------------|--------|
| archive_001.7z | {{hash}} | {{hash}} | ✅/❌ | ✅/❌/N/A | ✅/❌ | ✅/❌ | Verified / Failed |
| db_export.csv.gpg | {{hash}} | {{hash}} | ✅/❌ | ✅/❌ | N/A | ✅/❌ | Verified / Failed |

**IF integrity check FAILS for any file:**

"⚠️ Integrity verification FAILED for {{filename}}.

Source SHA-256: {{source_hash}}
Received SHA-256: {{received_hash}}

Possible causes:
1. Transfer corruption — data damaged during network/cloud/covert channel transfer
2. Encoding/decoding error — multi-layer encoding introduced corruption
3. Truncation — transfer interrupted before completion
4. DLP modification — inline DLP modified the content during transfer (content quarantine/redaction)
5. Chunk reassembly error — split file chunks reassembled in wrong order

Action required:
├── If access to source is still available: re-transfer the file through verified channel
├── If access is lost: document as partial/corrupted exfiltration
└── Assess impact: is this file critical to engagement objectives?"

### 3. Evidence Chain Documentation

**Build the formal chain of custody for all exfiltrated data:**

For each exfiltrated dataset, document the complete lifecycle:

```
EVIDENCE CHAIN — EX-{{NNN}}
═══════════════════════════

Dataset: {{description — e.g., "Customer PII database from CRM system"}}
Classification: {{PII / PHI / PCI / Financial / IP / Credentials / Configuration}}
Risk Rating: {{Critical / High / Medium / Low}}

SOURCE:
├── System: {{hostname}} ({{ip}})
├── Path: {{full_path}}
├── Original filename: {{filename}}
├── Original size: {{bytes}}
├── Original SHA-256: {{hash}}
├── Original permissions: {{owner:group:mode}}
└── Last modified: {{timestamp}}

COLLECTION:
├── Date/Time: {{ISO 8601}}
├── Method: {{how data was collected — query, file copy, database dump, screen capture}}
├── Operator: {{user_name}}
├── Tool used: {{tool — e.g., mysqldump, robocopy, scp, aws s3 cp}}
├── Command: {{exact command used}}
└── Access credential: {{credential_type:identity used for access}}

STAGING:
├── Staging host: {{hostname}} ({{ip}})
├── Staging path: {{path on staging system}}
├── Encryption method: {{AES-256-7z / GPG / age / OpenSSL / none}}
├── Encryption password: {{reference — "stored in operator vault, ref: EX-NNN-KEY"}}
├── Compressed size: {{bytes after encryption/compression}}
├── Chunk count: {{N chunks if split, or 1 if single file}}
├── Chunk manifest: {{list of chunk filenames and checksums}}
└── Staging SHA-256: {{hash of encrypted/compressed file}}

TRANSFER:
├── Channel: {{network HTTPS / cloud S3 / DNS tunnel / email / covert channel}}
├── Transfer date/time: {{ISO 8601 start — ISO 8601 end}}
├── Source: {{staging_host:path}}
├── Destination: {{operator system or cloud storage}}
├── Transfer tool: {{curl, aws s3 cp, custom script, etc.}}
├── DLP evasion applied: {{technique(s) from step-08, or "none required"}}
├── Transfer duration: {{time}}
├── Transfer size: {{bytes transferred}}
└── Detection events: {{any alerts generated during this transfer}}

VERIFICATION:
├── Received SHA-256: {{hash — must match staging SHA-256}}
├── Integrity match: ✅/❌
├── Decryption verified: ✅/❌
├── Decompression verified: ✅/❌
├── Content spot-checked: ✅/❌
├── Row/file count match: ✅/❌
└── Verification date: {{ISO 8601}}
```

**Present Evidence Chain Summary Table:**

| ID | Dataset | Classification | Volume | Channel | Source → Staging → Destination | Integrity | Status |
|----|---------|---------------|--------|---------|-------------------------------|-----------|--------|
| EX-001 | {{description}} | {{class}} | {{size}} | {{channel}} | {{host}} → {{staging}} → {{dest}} | ✅/❌ | Verified |
| EX-002 | {{description}} | {{class}} | {{size}} | {{channel}} | {{host}} → {{staging}} → {{dest}} | ✅/❌ | Verified |

### 4. Staging Cleanup

**Remove ALL staged data from compromised systems — staging hosts are the highest-priority cleanup:**

#### Secure File Deletion

```bash
# Windows — secure deletion (overwrite before delete)
# SDelete (Sysinternals) — DOD-compliant secure delete
sdelete -p 3 C:\staging\encrypted_archive.7z
sdelete -p 3 -s C:\staging\chunks\  # Recursive directory delete

# If SDelete not available — cipher free-space wipe after standard delete
del /f /q C:\staging\encrypted_archive.7z
del /f /q /s C:\staging\chunks\*
cipher /w:C:\staging\  # Wipes free space — recovers nothing

# PowerShell secure overwrite
$file = "C:\staging\archive.7z"
$bytes = [System.IO.File]::ReadAllBytes($file)
$random = New-Object byte[] $bytes.Length
[System.Security.Cryptography.RNGCryptoServiceProvider]::Create().GetBytes($random)
[System.IO.File]::WriteAllBytes($file, $random)  # Overwrite with random data
Remove-Item $file -Force

# Linux — secure deletion
shred -vfz -n 3 /tmp/staging/encrypted_archive.7z
# -v verbose, -f force, -z zero fill final pass, -n 3 = 3 overwrite passes

# Alternative: srm (secure remove)
srm -vz /tmp/staging/encrypted_archive.7z

# Alternative: wipe
wipe -rfi /tmp/staging/

# Verify deletion
ls -la /tmp/staging/  # Should show empty or non-existent
stat /tmp/staging/encrypted_archive.7z 2>&1  # Should show "No such file"
```

#### Staging Directory Cleanup

```bash
# Remove ALL staging directories created during step-04

# Windows
rmdir /s /q C:\Windows\Temp\staging
rmdir /s /q C:\Users\Public\Documents\.cache
# Check Recycle Bin
rd /s /q C:\$Recycle.Bin\%SID%\  # Clear recycle bin for current user

# Linux
rm -rf /tmp/.staging /dev/shm/.cache /var/tmp/.data
# Verify
find / -name ".staging" -o -name ".exfil" -o -name ".cache" 2>/dev/null | head -20
```

#### Manifest and Metadata Cleanup

```bash
# Remove chunk manifests, file lists, checksums
# These are operational documents that reveal the exfiltration scope

# Windows
del /f /q C:\staging\manifest.txt C:\staging\checksums.sha256
del /f /q C:\staging\file_list.txt C:\staging\transfer_log.txt

# Linux
rm -f /tmp/staging/manifest.txt /tmp/staging/checksums.sha256
rm -f /tmp/staging/file_list.txt /tmp/staging/transfer_log.txt
```

**Present Staging Cleanup Checklist:**

| Staging Host | Path | File/Directory | Secure Delete Method | Verified Removed | Recycle Bin Cleared | Free Space Wiped | Status |
|-------------|------|---------------|---------------------|-----------------|--------------------|--------------------|--------|
| {{host}} | {{path}} | {{archive/chunks/manifests}} | shred/sdelete/cipher | ✅/❌ | ✅/❌/N/A | ✅/❌ | Clean / Residual |

### 5. Lateral Movement Artifact Cleanup

**Remove ALL tools and artifacts deployed during the lateral movement and exfiltration phases:**

#### Tool Removal

```bash
# Remove ALL offensive tools deployed to compromised systems
# Windows
del /f /q C:\Windows\Temp\chisel.exe
del /f /q C:\Windows\Temp\ligolo-agent.exe
del /f /q C:\Windows\Temp\nc.exe
del /f /q C:\Windows\Temp\mimikatz.exe
del /f /q C:\Users\Public\procdump.exe
# Check common drop locations
dir /s /b C:\Windows\Temp\*.exe C:\Users\Public\*.exe 2>nul

# Linux
rm -f /tmp/.chisel /dev/shm/.agent /var/tmp/.tunnel
rm -f /tmp/linpeas.sh /dev/shm/pspy
# Check common drop locations
find /tmp /dev/shm /var/tmp -type f -executable 2>/dev/null
```

#### Account and Group Cleanup

```bash
# Remove created accounts
# Windows
net user backdoor_account /delete
# Verify
net user backdoor_account 2>&1  # Should show "user name could not be found"

# Linux
userdel -r backdoor_account
# Verify
id backdoor_account 2>&1  # Should show "no such user"

# Remove group memberships added
# Windows
net localgroup Administrators added_user /delete
# AD
Remove-ADGroupMember -Identity "Domain Admins" -Members "added_user" -Confirm:$false

# Linux
gpasswd -d added_user sudo
gpasswd -d added_user wheel
```

#### Registry and Configuration Cleanup

```bash
# Windows — remove registry modifications
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "backdoor_name" /f
reg delete "HKCU\Software\Classes\CLSID\{hijacked_clsid}" /f
# Verify
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "backdoor_name" 2>&1

# Remove scheduled tasks
schtasks /delete /tn "task_name" /f
# Verify
schtasks /query /tn "task_name" 2>&1  # Should show "does not exist"

# Remove services
sc stop service_name
sc delete service_name
# Verify
sc query service_name 2>&1  # Should show "does not exist"

# Remove firewall rules added for pivoting
netsh advfirewall firewall delete rule name="pivot_rule_name"
# Linux
iptables -D INPUT -p tcp --dport pivot_port -j ACCEPT
```

#### History and Log Cleanup (if authorized by RoE)

```bash
# PowerShell history
Remove-Item (Get-PSReadlineOption).HistorySavePath -Force
# Or clear specific entries only

# Bash history
history -c && history -w
# Or remove specific entries
# Edit ~/.bash_history to remove only our commands

# Windows Event Log (requires SYSTEM — only if RoE-authorized)
wevtutil cl Security  # CAUTION: clears entire Security log
# Prefer selective clearing — remove specific events by ID range

# Note: Log clearing itself generates Event ID 1102 (audit log cleared)
# Consider whether clearing logs creates more forensic evidence than leaving them
```

#### Pivot Infrastructure Removal

```bash
# Terminate all active tunnels and proxies
# Chisel
taskkill /f /im chisel.exe  # Windows
pkill chisel  # Linux

# Ligolo-ng
# Disconnect agent from operator proxy
pkill ligolo  # Linux agent

# SSH tunnels
# Kill SSH tunnel processes
pkill -f "ssh.*-L\|ssh.*-R\|ssh.*-D"

# SOCKS proxies
# Kill proxychains/SOCKS processes
pkill -f "socks\|proxychains"

# Port forwards
# Remove iptables DNAT/SNAT rules
iptables -t nat -D PREROUTING -p tcp --dport forward_port -j DNAT --to-destination target:port
iptables -t nat -D POSTROUTING -j MASQUERADE

# Verify all tunnels terminated
netstat -tlnp | grep -E "chisel|ligolo|ssh.*tunnel|socks"  # Should show nothing
ss -tlnp | grep -E "LISTEN" | grep -E "pivot_ports"
```

**Present Lateral Movement Artifact Cleanup Table:**

| ID | System | Artifact Type | Artifact Detail | Cleanup Command | Verified Removed | Cleanup Evidence |
|----|--------|-------------|----------------|----------------|-----------------|-----------------|
| CLN-001 | {{host}} | Tool | chisel.exe in C:\Temp | `del /f /q C:\Temp\chisel.exe` | ✅/❌ | `dir C:\Temp\chisel.exe` → not found |
| CLN-002 | {{host}} | Account | backdoor_user | `net user backdoor_user /delete` | ✅/❌ | `net user backdoor_user` → not found |
| CLN-003 | {{host}} | Service | PSEXESVC | `sc delete PSEXESVC` | ✅/❌ | `sc query PSEXESVC` → not found |
| CLN-004 | {{host}} | Tunnel | SSH reverse tunnel on :8443 | `pkill -f "ssh.*-R 8443"` | ✅/❌ | `ss -tlnp` → port not listening |

### 6. Persistence Mechanism Removal

**Remove ALL persistence mechanisms deployed during the engagement:**

**CRITICAL: Verify all data integrity (section 2) BEFORE removing persistence. Once persistence is removed, re-access may be impossible.**

#### Windows Persistence Removal

```bash
# Scheduled Tasks
schtasks /delete /tn "SystemHealthCheck" /f
schtasks /delete /tn "WindowsUpdateAux" /f
# Verify: schtasks /query /tn "task_name" 2>&1

# Services
sc stop "WinUpdateSvc" && sc delete "WinUpdateSvc"
# Verify: sc query "WinUpdateSvc" 2>&1

# Registry Run Keys
reg delete "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "SecurityUpdate" /f
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SecurityUpdate" /f
# Verify: reg query path /v name 2>&1

# COM Object Hijacking
reg delete "HKCU\Software\Classes\CLSID\{hijacked_clsid}\InprocServer32" /f
del /f /q C:\Users\Public\legit.dll
# Verify: reg query and file existence check

# WMI Event Subscriptions
Get-WMIObject -Namespace root\Subscription -Class __EventFilter | Where-Object {$_.Name -eq "SystemCheck"} | Remove-WMIObject
Get-WMIObject -Namespace root\Subscription -Class CommandLineEventConsumer | Where-Object {$_.Name -eq "SystemCheckConsumer"} | Remove-WMIObject
Get-WMIObject -Namespace root\Subscription -Class __FilterToConsumerBinding | Remove-WMIObject
# Verify: Get-WMIObject queries return empty

# Startup Folder Items
del /f /q "C:\Users\user\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\backdoor.lnk"
# Verify: dir startup_path

# BITS Jobs
bitsadmin /cancel "job_name"
bitsadmin /list /allusers  # Verify our jobs are removed
```

#### Linux Persistence Removal

```bash
# Cron Jobs
crontab -r  # Remove user crontab (if entire crontab was ours)
# Or edit to remove specific entries
crontab -l | grep -v "exfil\|update\|backdoor" | crontab -
# System cron
rm -f /etc/cron.d/sys-update
# Verify: crontab -l, ls /etc/cron.d/

# Systemd Services
systemctl stop sys-update
systemctl disable sys-update
rm -f /etc/systemd/system/sys-update.service
systemctl daemon-reload
# Verify: systemctl status sys-update → not found

# SSH Authorized Keys
# Remove our key from authorized_keys (keep legitimate keys)
sed -i '/operator@c2/d' /root/.ssh/authorized_keys
sed -i '/operator@c2/d' /home/user/.ssh/authorized_keys
# Verify: grep "operator" authorized_keys → no output

# .bashrc/.profile Modifications
# Remove our additions (keep original content)
sed -i '/nohup.*update/d' /home/user/.bashrc
# Verify: cat .bashrc | grep update → no output

# PAM Backdoor (if deployed)
# Restore original pam_unix.so from backup
cp /lib/x86_64-linux-gnu/security/pam_unix.so.bak /lib/x86_64-linux-gnu/security/pam_unix.so
# Verify: sha256sum /lib/x86_64-linux-gnu/security/pam_unix.so → matches known good
```

#### AD Persistence Removal

```bash
# Golden/Silver Tickets — cannot "remove" from AD, but:
# Recommend client rotate krbtgt password TWICE (for Golden Ticket invalidation)
# Recommend client rotate service account passwords (for Silver Ticket invalidation)
# Document as cleanup recommendation — not operator-actionable

# RBCD (Resource-Based Constrained Delegation) Configuration
# Remove the msDS-AllowedToActOnBehalfOfOtherIdentity attribute
Set-ADComputer -Identity target_computer -Clear 'msDS-AllowedToActOnBehalfOfOtherIdentity'
# Verify: Get-ADComputer target -Properties msDS-AllowedToActOnBehalfOfOtherIdentity

# SID History (if added)
# Remove SID History entries added during engagement
Set-ADUser -Identity target_user -Remove @{SIDHistory='S-1-5-21-ATTACKER-SID'}
# Verify: Get-ADUser target -Properties SIDHistory

# AdminSDHolder ACL (if modified)
# Remove attacker ACE from AdminSDHolder
# Manual: ADSI Edit → CN=AdminSDHolder,CN=System,DC=domain,DC=local → Security → Remove attacker ACE
# Wait 60 minutes for SDProp to propagate (or manually trigger)

# ADCS Certificates (if issued)
# Revoke certificates issued during engagement
certutil -revoke certificate_serial_number 0
# Verify: certutil -view -restrict "serialnumber=serial" → shows revoked

# GPO Modifications (if made)
# Remove or revert GPO changes
# This requires client coordination — document changes for client action
```

#### Cloud Persistence Removal

```bash
# AWS — Remove additional IAM access keys
aws iam delete-access-key --access-key-id AKIA_ATTACKER_KEY --user-name compromised_user
# Verify: aws iam list-access-keys --user-name compromised_user

# AWS — Remove Lambda backdoor functions
aws lambda delete-function --function-name backdoor_function
# Verify: aws lambda get-function --function-name backdoor_function → not found

# AWS — Remove IAM policy attachments
aws iam detach-user-policy --user-name target --policy-arn arn:aws:iam::policy/backdoor_policy
aws iam delete-policy --policy-arn arn:aws:iam::policy/backdoor_policy

# Azure — Remove service principals
az ad sp delete --id service_principal_id
# Verify: az ad sp show --id service_principal_id → not found

# Azure — Remove role assignments
az role assignment delete --assignee attacker_id --role "Contributor"

# GCP — Remove service account keys
gcloud iam service-accounts keys delete key_id --iam-account sa@project.iam.gserviceaccount.com
# Verify: gcloud iam service-accounts keys list --iam-account sa
```

**Present Persistence Removal Checklist:**

| ID | System | Mechanism | T-Code | Removal Command | Verified Removed | Verification Evidence | Status |
|----|--------|-----------|--------|----------------|-----------------|----------------------|--------|
| P-001 | {{host}} | Scheduled Task | T1053.005 | `schtasks /delete /tn name /f` | ✅/❌ | `schtasks /query` → not found | Removed / Failed |
| P-002 | {{host}} | SSH Key | T1098.004 | `sed -i '/key/d' authorized_keys` | ✅/❌ | `grep key auth_keys` → empty | Removed / Failed |
| P-003 | DC01 | Golden Ticket | T1558.001 | Client: krbtgt rotation x2 | ⬜ Client Action | N/A — client responsibility | Documented |

### 7. Credential Cleanup

**Address all credentials used, created, or extracted during the engagement:**

```bash
# Credentials CREATED during engagement:
# - Additional IAM keys → delete (section 6)
# - Service principals → delete (section 6)
# - Local accounts → delete (section 5)
# - SSH keys → remove from authorized_keys (section 6)

# Kerberos tickets on target systems:
# Purge Kerberos ticket cache on compromised systems
klist purge  # Windows — purge current user's tickets
# Note: this only purges current session — tickets in LSASS persist until system reboot

# Cached credentials on operator system:
# Remove all target credentials from operator's working environment
rm -f *.ccache *.kirbi *.pfx *.key
shred -vfz -n 3 credentials.txt password_hashes.txt

# Credentials that CANNOT be cleaned by operator (require client action):
# - Compromised passwords → client must force rotation
# - Dumped NTLM hashes → client must rotate ALL compromised accounts
# - Kerberos tickets in LSASS → client must reboot affected systems
# - Cloud tokens → client must revoke and rotate
# - Certificates → client must revoke (section 6)
```

**Present Credential Cleanup Recommendations:**

| Credential Type | Identity | Scope | Operator Cleanup | Client Action Required | Priority |
|----------------|---------|-------|-----------------|----------------------|----------|
| Password (compromised) | {{user}} | {{domain/local}} | N/A | Force password rotation | Critical |
| NTLM Hash (dumped) | {{user}} | {{domain/local}} | Removed from operator sys | Rotate password + clear cached creds | Critical |
| Kerberos Ticket | {{user}} | {{domain}} | Purged local cache | Reboot affected systems | High |
| SSH Key (deployed) | {{user}} | {{system}} | Removed from authorized_keys | Verify removal, generate new host keys | Medium |
| Cloud Token | {{identity}} | {{provider}} | Deleted access keys | Rotate remaining credentials | Critical |
| Certificate (issued) | {{identity}} | {{CA}} | N/A | Revoke certificate | High |

### 8. OPSEC Final Assessment

**Comprehensive assessment of what remains after cleanup:**

#### Irremovable Artifacts

```
IRREMOVABLE ARTIFACTS — What we CANNOT clean up:

1. Authentication Events (Windows Security Log)
   - Every logon event (4624, 4625) from lateral movement is permanent audit trail
   - Every service creation (7045, 4697) logged
   - Kerberos ticket operations (4768, 4769, 4770) captured
   - Impact: Forensic timeline reconstruction is possible for ALL lateral movement

2. Cloud API Logs (CloudTrail / Azure Monitor / GCP Audit)
   - Every API call during cloud exfiltration is logged
   - Cannot be deleted by attacker (admin-only, or immutable)
   - Impact: Complete cloud exfiltration timeline is available to IR

3. Network Flow Data (NetFlow / Zeek / NTA)
   - Connection metadata for all exfiltration traffic is captured
   - Volume and timing patterns are recorded
   - Impact: Exfiltration channels can be reconstructed from flow data

4. SIEM Correlation Data
   - Alerts generated during engagement persist in SIEM
   - Correlation rules may have created case records
   - Impact: SOC has baseline for investigation if triggered

5. Endpoint Telemetry (EDR)
   - Process execution, file creation, network connections
   - Command-line arguments captured by EDR
   - Impact: Full process chain reconstruction is possible
```

#### Forensic Investigation Assessment

"If incident response is called NOW, post-cleanup, what would they find?"

| Forensic Domain | What Remains | Finding Probability | Impact |
|----------------|-------------|--------------------|---------| 
| Timeline Analysis | Authentication events, process creation timestamps | High | Can reconstruct lateral movement and exfiltration timeline |
| Memory Forensics | Minimal — tools removed, no persistent injection | Low | Volatile evidence dissipates after reboot |
| Disk Forensics | File deletion artifacts (MFT entries, journal), prefetch/shimcache | Medium | Deleted file names visible, execution evidence in prefetch |
| Network Forensics | Flow data, DNS queries, PCAP (if captured) | High | Exfiltration channels identifiable from connection metadata |
| Cloud Forensics | Complete API audit trail | Certain | Full cloud exfiltration timeline with exact operations |
| AD Forensics | Replication metadata, security descriptor changes | Medium | AD modifications visible in replication logs |

#### Post-Engagement Detection Risk

```
POST-ENGAGEMENT DETECTION RISK ASSESSMENT:

Probability of detection after cleanup:
├── Within 24 hours: {{Low/Medium/High}} — {{justification}}
├── Within 7 days: {{Low/Medium/High}} — {{justification}}
├── Within 30 days: {{Low/Medium/High}} — {{justification}}
└── During routine audit: {{Low/Medium/High}} — {{justification}}

Factors reducing detection risk:
├── {{factor_1 — e.g., All tools removed, no files on disk}}
├── {{factor_2 — e.g., Persistence mechanisms all removed}}
└── {{factor_3 — e.g., Exfiltration volume below NTA baseline}}

Factors increasing detection risk:
├── {{factor_1 — e.g., Authentication events in Security Log}}
├── {{factor_2 — e.g., Cloud API logs immutable}}
└── {{factor_3 — e.g., DLP alerts generated during step-08 testing}}

Overall assessment: {{Minimal / Moderate / Significant residual detection surface}}
```

**Present the complete OPSEC Final Assessment before proceeding.**

### 9. Secure Data Handling

**Document the handling of exfiltrated data on operator systems:**

```
SECURE DATA HANDLING — Exfiltrated Data

Data Location on Operator Systems:
├── Path: {{operator_system:path}}
├── Encryption: {{AES-256 at rest / full-disk encryption / both}}
├── Access control: {{who has access — operator only / team / restricted}}
└── Volume: {{total size of exfiltrated data}}

Data Retention Timeline:
├── Engagement active: {{start_date}} — {{end_date}}
├── Report delivery: {{expected_date}}
├── Data retention period: {{per RoE — typically 30-90 days post-report}}
├── Secure deletion deadline: {{date}}
└── Deletion method: {{shred / sdelete / crypto-erase / physical destruction}}

Secure Deletion Plan:
├── Step 1: Verify final report is delivered and accepted by client
├── Step 2: Confirm client does not require additional analysis of exfiltrated data
├── Step 3: Execute secure deletion using {{method}}
├── Step 4: Verify deletion (disk recovery attempt on sample)
├── Step 5: Document deletion with timestamp and method
└── Step 6: Notify client that exfiltrated data has been destroyed

Client Notification:
├── "All exfiltrated data is encrypted at rest on operator systems"
├── "Data access is restricted to {{operator/team}}"
├── "Data will be securely destroyed by {{date}} using {{method}}"
└── "Destruction confirmation will be provided to {{client_contact}}"
```

### 10. Document Findings

**Write findings under `## Exfiltration Verification & Cleanup Results`:**

```markdown
## Exfiltration Verification & Cleanup Results

### Summary
- Data targets identified: {{count}}
- Data targets exfiltrated: {{count}} ({{percentage}}%)
- Total volume exfiltrated: {{size}}
- Data integrity verified: {{count}}/{{count}} files ({{percentage}}% verified)
- Integrity failures: {{count}} ({{details}})
- Evidence chains documented: {{count}} (EX-001 through EX-{{NNN}})
- Artifacts cleaned: {{count}}/{{count}} ({{percentage}}%)
- Cleanup failures: {{count}} ({{details}})
- Persistence mechanisms removed: {{count}}/{{count}}
- Irremovable artifacts: {{count}} categories (authentication logs, cloud API logs, etc.)
- Post-engagement detection risk: {{minimal/moderate/significant}}

### Exfiltration Completeness Matrix
{{completeness_matrix}}

### Data Integrity Verification
{{integrity_results_table}}

### Evidence Chain Summary
{{evidence_chain_summary_table}}

### Staging Cleanup Results
{{staging_cleanup_checklist}}

### Artifact Cleanup Results
{{artifact_cleanup_table}}

### Persistence Removal Results
{{persistence_removal_checklist}}

### Credential Cleanup
{{credential_cleanup_table}}

### OPSEC Final Assessment
- Irremovable artifacts: {{count}} categories
- Forensic investigation findings: {{assessment}}
- Post-engagement detection risk: {{assessment}}

### Secure Data Handling
- Exfiltrated data encrypted at rest: ✅
- Data retention deadline: {{date}}
- Secure deletion scheduled: {{date}}
- Client notified of data handling: ✅/⬜
```

Update frontmatter metrics:
- `data_targets_exfiltrated` with count
- `total_volume_exfiltrated` with size
- `integrity_verified` with count and percentage
- `artifacts_cleaned` with count
- `persistence_removed` with count
- `cleanup_failures` with count
- `detection_risk_post_cleanup` with assessment

### 11. Present MENU OPTIONS

"**Exfiltration verification and cleanup completed.**

Data targets: {{identified}} identified | {{exfiltrated}} exfiltrated ({{percentage}}%)
Total volume: {{size}} across {{channel_count}} channels
Data integrity: {{verified}}/{{total}} verified ({{pass_rate}}% pass rate)
Evidence chains: {{count}} documented (EX-001 through EX-{{NNN}})
Artifacts cleaned: {{cleaned}}/{{total}} ({{percentage}}%)
Persistence removed: {{removed}}/{{total}}
Cleanup failures: {{count}}
Post-engagement detection risk: {{assessment}}
Data handling: Encrypted at rest, deletion scheduled {{date}}

**Select an option:**
[A] Advanced Elicitation — Deep review of a specific evidence chain, cleanup item, or integrity failure
[W] War Room — Red (was the cleanup sufficient? what would a forensic examiner find? which artifacts are most likely to trigger post-engagement investigation?) vs Blue (what detection opportunities did the exfiltration create? which irremovable artifacts are highest value for IR? what should the SOC prioritize in post-engagement monitoring?)
[C] Continue — Proceed to Documentation & Engagement Closure (Step 10 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — select a specific evidence chain by EX-ID, a cleanup item by CLN-ID, or an integrity failure and walk through the complete record: source data, collection method, staging details, transfer channel, DLP evasion applied, verification results, cleanup status. Challenge the documentation: is the evidence chain complete enough for the engagement report? Would a third-party reviewer accept this chain of custody? If the operator identifies gaps, iterate and complete. Redisplay menu.

- IF W: War Room — Red Team perspective: was the cleanup sufficient for operational security? If the SOC launches an investigation tomorrow, which artifacts would they find first? Which cleanup items are most likely to have failed silently (file not actually deleted, registry key not actually removed)? Was the data handling plan adequate for the sensitivity of the exfiltrated data? What would a forensic examiner find if they imaged the staging host NOW? Is the post-engagement detection risk assessment honest or optimistic? Blue Team perspective: which irremovable artifacts have the highest forensic value? What detection rules should be created based on the artifacts that remain? Which log sources should the SOC prioritize for post-engagement analysis? How would an IR team scope the full exfiltration from a single artifact? What retention policies should apply to the relevant log sources? What monitoring should continue post-engagement to confirm cleanup completeness? Summarize insights, redisplay menu.

- IF C: Update output file frontmatter adding this step name to stepsCompleted and updating verification and cleanup metrics, then read fully and follow: ./step-10-reporting.md

- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, data_targets_exfiltrated set, total_volume_exfiltrated set, integrity_verified set, artifacts_cleaned set, persistence_removed set, cleanup_failures set, and detection_risk_post_cleanup set], will you then read fully and follow: `./step-10-reporting.md` to proceed to the final documentation and engagement closure step.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Exfiltration completeness checked — every target from step-03 cross-referenced with actual exfiltration results
- Gap analysis performed for any targets not exfiltrated or partially exfiltrated, with reason and impact assessment
- Data integrity verified for EVERY exfiltrated file — SHA-256 checksum comparison, decryption verified, decompression verified, content spot-checked
- Integrity failures documented with cause analysis and impact assessment
- Evidence chain documented for every exfiltrated dataset (EX-001 through EX-NNN) with complete source → collection → staging → transfer → verification lifecycle
- Staging cleanup completed — all staged data securely deleted with verification, recycle bin cleared, free space wiped where possible
- Lateral movement artifacts cleaned — tools removed, accounts deleted, registry/config reverted, tunnels terminated, firewall rules removed
- Persistence mechanisms removed — every mechanism from the engagement documented, removal commands executed, removal verified
- Persistence that requires client action clearly documented (krbtgt rotation, certificate revocation, password rotation)
- Credential cleanup addressed — operator credentials purged, client credential rotation recommendations documented
- OPSEC final assessment completed — irremovable artifacts identified, forensic investigation assessment performed, post-engagement detection risk rated
- Secure data handling documented — encryption at rest, access controls, retention timeline, deletion plan, client notification
- Cleanup failures documented with justification — if an artifact cannot be removed, the report explains why
- Findings appended to report under `## Exfiltration Verification & Cleanup Results`
- Frontmatter updated with data_targets_exfiltrated, total_volume_exfiltrated, integrity_verified, artifacts_cleaned, persistence_removed, cleanup_failures, detection_risk_post_cleanup
- Menu presented and user choice respected before proceeding

### ❌ SYSTEM FAILURE:

- Beginning cleanup before verifying data integrity — once persistence/access is removed, re-extraction is impossible if data is corrupt
- Not verifying checksums for exfiltrated files — unverified data is unreliable evidence
- Not documenting evidence chains — exfiltration without chain of custody is not reportable
- Incomplete artifact cleanup — leaving tools, accounts, or persistence on client systems is a live security risk
- Not documenting cleanup failures — hidden cleanup failures are worse than known ones
- Not identifying irremovable artifacts — pretending logs don't exist undermines the OPSEC assessment
- Not addressing secure data handling — exfiltrated data without a destruction plan is a liability
- Not documenting credential cleanup recommendations for the client — compromised credentials that aren't rotated remain a risk
- Overstating cleanup effectiveness — claiming "no trace remains" when authentication logs and cloud API logs are immutable is dishonest
- Attempting new exfiltration or lateral movement during verification — this is a confirmation and cleanup step only
- Not performing the gap analysis for missing targets — the client needs to know what WAS and WASN'T exfiltrated
- Not pacing cleanup actions — rapid bulk deletion triggers more alerts than the original exfiltration
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Verification and cleanup are the bridge between operational execution and professional reporting. Every exfiltrated file must be verified, every artifact must be cleaned or documented, every evidence chain must be complete, and every credential must be addressed. The integrity of the engagement report depends entirely on the thoroughness of this step. Trust nothing, verify everything, clean everything, document everything.
