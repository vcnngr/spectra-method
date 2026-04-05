# Step 3: Data Assessment & Classification

**Progress: Step 3 of 10** — Next: Data Collection & Staging

## STEP GOAL:

Assess and classify all discovered data targets from the step-02 data map. Estimate data volumes with precision, classify sensitivity levels against regulatory and business impact frameworks, verify RoE compliance for each data category, prioritize targets by engagement objectives and operational feasibility, and produce the final authoritative exfiltration target list that drives collection, staging, and channel selection in subsequent steps.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER collect, stage, or transfer data during assessment — this step evaluates and prioritizes, it does not move data
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN EXFILTRATION SPECIALIST conducting data assessment, not an autonomous data extraction tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Assessment ONLY — do not collect or transfer data (that is step-04)
- 📋 EVERY data target must be checked against RoE authorized data types — no exceptions
- 📏 Volume estimation drives exfiltration channel selection — accuracy matters
- ⚖️ Prioritization considers BOTH business value AND operational risk (DLP, monitoring, bandwidth)
- 🚫 Any data target that fails RoE check must be EXCLUDED from the exfiltration target list

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Opening/reading files to assess content generates file access audit logs that Varonis DatAdvantage, DLP endpoint agents (Symantec, Forcepoint, Digital Guardian), and CASB solutions track per-file — use metadata inspection (file size, type, modified date, file header bytes) for assessment where possible, minimize full file reads
  - Sampling database content to verify sensitivity may trigger database activity monitoring (DAM) solutions (Imperva, IBM Guardium, Oracle Audit Vault) — use COUNT/schema queries and column-name analysis before executing SELECT queries on actual data
  - Assessing email content requires opening individual messages which generates per-message audit entries in Exchange/O365 Unified Audit Log — use search metadata (subject, sender, date range, attachment indicators) for initial assessment rather than opening messages
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your assessment plan before beginning classification
- ⚠️ Present [A]/[W]/[C] menu after assessment complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, RoE from step-01, comprehensive data map from step-02, access credentials, network topology
- Focus: Data assessment, classification, RoE verification, and prioritization ONLY
- Limits: Do NOT collect, copy, stage, or transfer data — assessment and classification only
- Dependencies: step-02-data-discovery.md (data map with all source locations, access methods, preliminary volume estimates)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Data Inventory Compilation

Consolidate all discoveries from step-02 into a single master inventory for systematic assessment. Every data source must be assigned a unique identifier and tracked through the assessment pipeline.

**Master Data Inventory (initial — pre-assessment):**
```
| Source ID | Category | Type | Location | Access Method | Credentials | Volume (Est.) | Sensitivity (TBD) | RoE Status (TBD) | Priority (TBD) |
|-----------|----------|------|----------|---------------|-------------|---------------|--------------------|-------------------|----------------|
| FS-001 | File Share | SMB | \\{{host}}\{{share}} | SMB auth | CRED-{{n}} | {{size}} | — | — | — |
| DB-001 | Database | MSSQL | {{host}}:1433 | SQL auth | CRED-{{n}} | {{size}} | — | — | — |
| EM-001 | Email | O365 | {{tenant}} | Graph API | CRED-{{n}} | {{size}} | — | — | — |
| SC-001 | Source Code | GitLab | {{host}} | API token | CRED-{{n}} | {{size}} | — | — | — |
| SEC-001 | Secrets | Vault | {{host}}:8200 | Vault token | CRED-{{n}} | {{size}} | — | — | — |
| CS-001 | Cloud Storage | S3 | s3://{{bucket}} | IAM role | CRED-{{n}} | {{size}} | — | — | — |
| BK-001 | Backup | DB Backup | {{path}} | File access | CRED-{{n}} | {{size}} | — | — | — |
```

**Verify completeness:** Cross-reference against step-02 data map. Confirm no discovered sources are missing from the inventory. Flag any sources that were discovered but could not be enumerated (access denied, network issues).

### 2. Volume Estimation

Precise volume estimation is critical — it determines exfiltration channel selection, time requirements, and bandwidth allocation. Inaccurate estimates lead to failed exfiltration or blown timelines.

#### 2a. File Share Volume Assessment (T1083 — File and Directory Discovery)

**Windows PowerShell:**
```
# Total share size
Get-ChildItem -Path "\\{{target}}\{{share}}" -Recurse -ErrorAction SilentlyContinue |
  Measure-Object -Property Length -Sum |
  Select-Object @{N='TotalSize_GB';E={[math]::Round($_.Sum/1GB,2)}}, Count

# Size by file extension (understand data composition)
Get-ChildItem -Path "\\{{target}}\{{share}}" -Recurse -File -ErrorAction SilentlyContinue |
  Group-Object Extension |
  Select-Object @{N='Extension';E={$_.Name}}, Count, @{N='TotalSize_MB';E={[math]::Round(($_.Group | Measure-Object Length -Sum).Sum/1MB,2)}} |
  Sort-Object TotalSize_MB -Descending | Select-Object -First 20

# Size of sensitive files only (targeted volume)
Get-ChildItem -Path "\\{{target}}\{{share}}" -Recurse -Include *.kdbx,*.pfx,*.pem,*.key,*.sql,*.bak,*.conf -ErrorAction SilentlyContinue |
  Measure-Object -Property Length -Sum |
  Select-Object @{N='SensitiveSize_MB';E={[math]::Round($_.Sum/1MB,2)}}, Count
```

**Linux:**
```
# Total directory size
du -sh /mnt/{{share}}/

# Size by directory (top-level breakdown)
du -sh /mnt/{{share}}/* 2>/dev/null | sort -rh | head -20

# File count and size by extension
find /mnt/{{share}} -type f -printf '%s %f\n' 2>/dev/null |
  awk -F. '{ext=$NF; size+=$1; count++} END {for(e in ext) printf "%s\t%d files\t%.2f MB\n", e, count[e], size[e]/1048576}' |
  sort -t$'\t' -k3 -rn | head -20
```

OPSEC: Recursive `Get-ChildItem` and `du` generate significant I/O on storage systems. Varonis and Stealthbits will flag bulk enumeration. If step-02 already captured directory listings, reuse that data rather than re-enumerating.

#### 2b. Database Volume Assessment

```
# MSSQL — database and table sizes
sqlcmd -S {{target}} -U {{user}} -P {{pass}} -Q "
  SELECT DB_NAME(database_id) AS DatabaseName,
    CAST(SUM(size * 8.0 / 1024) AS DECIMAL(10,2)) AS SizeMB
  FROM sys.master_files
  GROUP BY database_id
  ORDER BY SizeMB DESC"

# MSSQL — specific table sizes
sqlcmd -S {{target}} -U {{user}} -P {{pass}} -d {{database}} -Q "
  SELECT t.NAME AS TableName,
    p.rows AS RowCounts,
    CAST(ROUND(SUM(a.total_pages) * 8.0 / 1024, 2) AS DECIMAL(10,2)) AS TotalSpaceMB,
    CAST(ROUND(SUM(a.used_pages) * 8.0 / 1024, 2) AS DECIMAL(10,2)) AS UsedSpaceMB
  FROM sys.tables t
  INNER JOIN sys.indexes i ON t.object_id = i.object_id
  INNER JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
  INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
  WHERE t.is_ms_shipped = 0
  GROUP BY t.NAME, p.rows
  ORDER BY TotalSpaceMB DESC"

# MySQL — database sizes
mysql -h {{target}} -u {{user}} -p'{{pass}}' -e "
  SELECT table_schema AS 'Database',
    ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS 'Size_MB',
    SUM(table_rows) AS 'Total_Rows'
  FROM information_schema.tables
  GROUP BY table_schema
  ORDER BY Size_MB DESC"

# PostgreSQL — database sizes
psql -h {{target}} -U {{user}} -c "
  SELECT datname, pg_size_pretty(pg_database_size(datname)) AS size
  FROM pg_database
  WHERE datistemplate = false
  ORDER BY pg_database_size(datname) DESC"

# PostgreSQL — table sizes within database
psql -h {{target}} -U {{user}} -d {{database}} -c "
  SELECT schemaname, tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    n_live_tup AS row_count
  FROM pg_stat_user_tables
  ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
  LIMIT 30"

# MongoDB — collection sizes
mongosh --host {{target}} -u {{user}} -p {{pass}} {{database}} --eval "
  db.getCollectionNames().forEach(function(c) {
    var stats = db.getCollection(c).stats();
    print(c + ': ' + stats.count + ' docs, ' + Math.round(stats.storageSize/1024/1024) + ' MB storage, ' + Math.round(stats.size/1024/1024) + ' MB data');
  })"
```

OPSEC: Size queries on system tables (sys.master_files, information_schema.tables, pg_database_size) are metadata-only operations with minimal detection risk. They do not touch actual data.

#### 2c. Email Volume Assessment

```
# Exchange/O365 — mailbox sizes via Graph API
GET https://graph.microsoft.com/v1.0/users?$select=displayName,mail&$expand=mailboxSettings

# Exchange PowerShell (if admin)
Get-Mailbox -ResultSize Unlimited |
  Get-MailboxStatistics |
  Select-Object DisplayName,TotalItemSize,ItemCount |
  Sort-Object TotalItemSize -Descending | Select-Object -First 50

# Gmail — mailbox usage via Admin SDK
GET https://admin.googleapis.com/admin/reports/v1/usage/users?date={{date}}&parameters=accounts:gmail_used_quota_in_mb
```

#### 2d. Cloud Storage Volume Assessment

```
# AWS S3 — bucket size via CloudWatch metrics
aws cloudwatch get-metric-statistics --namespace AWS/S3 --metric-name BucketSizeBytes \
  --dimensions Name=BucketName,Value={{bucket}} Name=StorageType,Value=StandardStorage \
  --start-time {{start}} --end-time {{end}} --period 86400 --statistics Average

# AWS S3 — direct size calculation
aws s3 ls s3://{{bucket}} --recursive --summarize | tail -2

# Azure Blob — container metrics
az storage blob list --container-name {{container}} --account-name {{account}} --query "[].{name:name, size:properties.contentLength}" --output table

# GCS — bucket size
gsutil du -s gs://{{bucket}}
```

**Present Volume Assessment table:**
```
| Source ID | Category | Location | Raw Volume | Sensitive Data Volume | Compressed Est. (70%) | Exfil Time @10Mbps | Exfil Time @1Mbps | Feasibility |
|-----------|----------|----------|------------|----------------------|-----------------------|--------------------|-------------------|-------------|
| FS-001 | File Share | \\{{host}}\{{share}} | {{raw}} | {{sensitive}} | {{compressed}} | {{time}} | {{time}} | High/Med/Low |
| DB-001 | Database | {{host}}:1433 | {{raw}} | {{sensitive}} | {{compressed}} | {{time}} | {{time}} | {{feasibility}} |
| EM-001 | Email | {{tenant}} | {{raw}} | {{sensitive}} | {{compressed}} | {{time}} | {{time}} | {{feasibility}} |
| CS-001 | Cloud | s3://{{bucket}} | {{raw}} | {{sensitive}} | {{compressed}} | {{time}} | {{time}} | {{feasibility}} |
| BK-001 | Backup | {{path}} | {{raw}} | {{raw}} (backup=full) | {{compressed}} | {{time}} | {{time}} | {{feasibility}} |
| **TOTAL** | — | — | **{{total_raw}}** | **{{total_sensitive}}** | **{{total_compressed}}** | **{{total_time}}** | **{{total_time}}** | — |
```

**Bandwidth feasibility calculation:**
```
Total Sensitive Volume: {{total_volume}}
Estimated Compression Ratio: ~70% (varies by data type)
Compressed Volume: {{compressed_volume}}
Available Bandwidth (estimated): {{bandwidth}}
Available Time Window: {{time_window}}
Maximum Transferable: {{max_transfer}} (bandwidth × time)
Feasibility: {{FEASIBLE / EXCEEDS CAPACITY — requires prioritization or multiple sessions}}
```

### 3. Sensitivity Classification

Classify every data target by sensitivity level using a standardized framework that maps to regulatory, business impact, and operational risk categories.

#### 3a. Classification Framework

| Level | Classification | Definition | Regulatory Exposure | Business Impact | Examples |
|-------|---------------|------------|--------------------| ----------------|---------|
| **L4** | **Critical** | Data whose exposure creates material regulatory, legal, or existential business risk | GDPR Art. 83 (up to 4% global revenue), HIPAA (up to $1.5M/violation), PCI DSS (fines + card brand penalties) | Existential — lawsuits, regulatory action, loss of customer trust, stock impact | PII/PHI with regulatory coverage, production credentials (DA hashes, CA private keys), M&A documents pre-announcement, source code of security products |
| **L3** | **High** | Data whose exposure creates significant operational or competitive damage | SOX (financial reporting), industry-specific (GLBA, FERPA) | Severe — competitive disadvantage, operational disruption, significant financial loss | Financial records, employee databases, customer lists with contact info, strategic plans, internal security assessments, vulnerability reports |
| **L2** | **Medium** | Data whose exposure creates moderate operational or reputational risk | Contractual obligations (NDA violations), privacy policies | Moderate — embarrassment, minor financial impact, limited competitive exposure | General business documents, internal communications, non-sensitive source code, operational procedures, meeting minutes |
| **L1** | **Low** | Data whose exposure creates minimal impact | None | Minimal — public-facing content or easily reconstructable information | Marketing materials, public documentation, general reference materials, obsolete data |

#### 3b. Classify Each Data Source

**For each source in the master inventory, apply the classification framework:**

```
| Source ID | Location | Data Contents (Assessed) | Sensitivity Level | Classification Justification | Regulatory Framework |
|-----------|----------|-------------------------|-------------------|------------------------------|---------------------|
| FS-001 | \\{{host}}\{{share}} | {{description}} | L4/L3/L2/L1 | {{justification}} | {{GDPR/HIPAA/PCI/SOX/None}} |
| DB-001 | {{host}}:1433 | {{description}} | L4/L3/L2/L1 | {{justification}} | {{framework}} |
| EM-001 | {{tenant}} | {{description}} | L4/L3/L2/L1 | {{justification}} | {{framework}} |
```

**Assessment techniques by data category:**

| Category | Metadata Assessment (Low OPSEC) | Content Sampling (Higher OPSEC) |
|----------|--------------------------------|---------------------------------|
| File Shares | File names, extensions, directory structure, file sizes, modified dates | Open file headers, first 100 bytes, keyword grep |
| Databases | Table/column names, row counts, data types | SELECT TOP 5 from tables with sensitive column names |
| Email | Subject lines, sender/recipient, attachment metadata | Open specific messages matching keyword search |
| Source Code | Repository names, README files, directory structure | Search for hardcoded credentials, API keys |
| Cloud Storage | Object names, sizes, metadata tags | Download sample objects |
| Backups | Backup job names, sizes, timestamps | Restore and inspect (high OPSEC cost) |

OPSEC: Metadata-based assessment (column names, file names, sizes) generates minimal detection events. Content sampling (opening files, SELECT queries) generates audit log entries. Always prefer metadata assessment. Only escalate to content sampling when metadata is insufficient to determine sensitivity.

### 4. RoE Compliance Check

**CRITICAL: This is non-negotiable. Every data target MUST be verified against the engagement Rules of Engagement before inclusion in the exfiltration target list.**

#### 4a. RoE Authorization Matrix

**Review step-01 RoE parameters and apply to each data source:**

```
| RoE Parameter | Authorized | Restricted | Excluded |
|--------------|-----------|------------|----------|
| Data Types | {{authorized_types}} | {{restricted_types}} | {{excluded_types}} |
| Volume Limits | {{volume_limit — e.g., "proof-of-concept only" or "full extraction authorized"}} | — | — |
| Handling Requirements | {{requirements — e.g., "AES-256 encryption required", "secure deletion after report"}} | — | — |
| Prohibited Targets | — | — | {{prohibited — e.g., "no patient records", "no payment card data"}} |
| Time Restrictions | {{window — e.g., "business hours only" or "weekends preferred"}} | — | — |
| Notification Requirements | {{notify — e.g., "notify client CISO if PII discovered"}} | — | — |
```

#### 4b. Per-Source RoE Compliance Assessment

**Apply RoE checks to every data source:**

```
| Source ID | Data Type | RoE Authorization | Volume Compliance | Handling Compliance | Decision | Notes |
|-----------|-----------|-------------------|-------------------|--------------------| ---------|-------|
| FS-001 | {{type}} | ✅ Authorized / ⚠️ Restricted / ❌ Excluded | ✅ Within limits / ⚠️ Requires PoC scope | ✅ Can comply / ❌ Cannot comply | INCLUDE / EXCLUDE / RESTRICT | {{notes}} |
| DB-001 | {{type}} | {{status}} | {{status}} | {{status}} | {{decision}} | {{notes}} |
| EM-001 | {{type}} | {{status}} | {{status}} | {{status}} | {{decision}} | {{notes}} |
```

**RoE Decision Logic:**
- **INCLUDE**: Data type authorized, volume within limits, handling requirements achievable
- **RESTRICT**: Data type authorized but volume must be limited to proof-of-concept, or specific handling required
- **EXCLUDE**: Data type explicitly prohibited by RoE, or handling requirements cannot be met

**⚠️ Any source marked EXCLUDE must be removed from all subsequent steps. Document the exclusion reason for the engagement report.**

**Present RoE Compliance Summary:**
```
Total data sources assessed: {{total}}
INCLUDE (fully authorized): {{include_count}}
RESTRICT (authorized with limitations): {{restrict_count}}
EXCLUDE (RoE prohibited): {{exclude_count}}

Excluded sources:
{{excluded_list_with_reasons}}
```

### 5. Exfiltration Feasibility Assessment

For each authorized data target (INCLUDE or RESTRICT), assess operational feasibility across multiple dimensions.

#### 5a. Access Reliability Assessment

```
| Source ID | Access Method | Credential Status | Connection Stability | Access Windows | Reliability Score |
|-----------|--------------|-------------------|---------------------|---------------|-------------------|
| FS-001 | SMB | CRED-{{n}} (Verified) | Persistent share access | 24/7 | High |
| DB-001 | SQL auth | CRED-{{n}} (Verified) | Stable connection | Business hours (locked after) | Medium |
| EM-001 | Graph API | Token (expires {{time}}) | API rate limits | Token lifetime | Medium |
| CS-001 | IAM role | Session (12h max) | Stable | Session duration | Medium |
| BK-001 | File access | CRED-{{n}} (Local admin) | Direct disk | 24/7 | High |
```

#### 5b. Transfer Feasibility Assessment

For each source, assess which exfiltration channels are viable based on volume and network position:

```
| Source ID | Volume | Network Exfil (HTTPS) | Cloud Exfil (S3/Blob) | Covert Channel (DNS/ICMP) | Physical | Recommended Channel |
|-----------|--------|----------------------|----------------------|--------------------------|----------|---------------------|
| FS-001 | {{size}} | ✅ ({{time}}) | ✅ ({{time}}) | ❌ (too large) | ❌ | HTTPS |
| DB-001 | {{size}} | ✅ ({{time}}) | ✅ ({{time}}) | ⚠️ (slow) | ❌ | Cloud upload |
| SEC-001 | {{size}} | ✅ (seconds) | ✅ (seconds) | ✅ (small enough) | ❌ | Covert (max stealth) |
| BK-001 | {{size}} | ⚠️ ({{time}}) | ✅ ({{time}}) | ❌ | ⚠️ (if physical access) | Cloud upload |
```

**Channel capacity reference:**
| Channel | Bandwidth | Max Practical Volume | Stealth Level | Detection Surface |
|---------|-----------|---------------------|---------------|-------------------|
| HTTPS (direct) | 1-100 Mbps | Unlimited (bandwidth-limited) | Medium | Web proxy logs, SSL inspection, DLP |
| HTTPS (C2 tunnel) | 100 Kbps-10 Mbps | GB range | Medium-High | C2 traffic patterns, beaconing detection |
| DNS tunneling | 10-50 Kbps | KB-MB range | High | DNS query volume anomaly, TXT record size |
| ICMP tunneling | 10-100 Kbps | MB range | High | ICMP payload inspection, volume anomaly |
| Cloud API (S3/Blob/GCS) | 10-1000 Mbps | Unlimited | Medium | CloudTrail/Monitor logs, unusual API patterns |
| Cloud sync (OneDrive/GDrive) | 1-50 Mbps | GB-TB range | Low-Medium | Sync agent logs, unusual volume |
| Email attachment | Variable | MB per message | Low | DLP email scanning, attachment inspection |
| Physical (USB) | N/A | Unlimited | Varies | USB device audit, endpoint DLP |

#### 5c. DLP & Monitoring Risk Assessment

**For each data source, assess the monitoring and DLP coverage:**

```
| Source ID | Location | DLP Coverage | Storage Monitoring | Network Monitoring | CASB Coverage | Overall Detection Risk |
|-----------|----------|-------------|-------------------|-------------------|---------------|----------------------|
| FS-001 | On-prem file share | Endpoint DLP ({{product}}) | Varonis/Netwrix ({{status}}) | Proxy/IDS ({{status}}) | N/A | Medium-High |
| DB-001 | On-prem database | DAM ({{product}}) | — | Proxy/IDS | N/A | Medium |
| EM-001 | O365 cloud | O365 DLP policies | — | — | CASB ({{product}}) | High |
| CS-001 | AWS S3 | — | CloudTrail | — | CASB ({{status}}) | Medium |
| BK-001 | Backup storage | None (typically) | None (typically) | Proxy/IDS | N/A | **Low** |
```

**DLP evasion considerations per data type:**
| Data Type | Common DLP Signatures | Evasion Approach |
|-----------|----------------------|------------------|
| PII (SSN, CC#) | Regex patterns (###-##-####, credit card checksums) | Encrypt before transfer, split across channels |
| Source code | File extension rules, keyword rules | Compress + encrypt, rename extensions |
| Documents (Office) | Content inspection, classification labels | Remove metadata/labels, compress + encrypt |
| Database exports | File type inspection, volume thresholds | Encrypt to generic binary, chunk to sub-threshold sizes |
| Email archives (PST) | File type blocking | Encrypt, rename extension, embed in allowed container |

#### 5d. Time Requirement Assessment

```
| Source ID | Volume (Compressed) | Channel | Est. Bandwidth | Transfer Time | Collection Time | Total Time | Schedule |
|-----------|--------------------| --------|-----------------|---------------|-----------------|------------|----------|
| FS-001 | {{size}} | HTTPS | {{bw}} | {{time}} | {{collection}} | {{total}} | {{window}} |
| DB-001 | {{size}} | Cloud | {{bw}} | {{time}} | {{extraction}} | {{total}} | {{window}} |
| EM-001 | {{size}} | HTTPS | {{bw}} | {{time}} | {{download}} | {{total}} | {{window}} |
| **TOTAL** | **{{total_size}}** | — | — | **{{total_transfer}}** | **{{total_collection}}** | **{{grand_total}}** | — |
```

### 6. Prioritization

Rank all authorized targets using a weighted multi-factor scoring model that balances engagement value against operational risk and time efficiency.

#### 6a. Scoring Matrix

| Factor | Weight | High (3) | Medium (2) | Low (1) |
|--------|--------|----------|------------|---------|
| Objective Alignment | 30% | Directly proves primary engagement objective | Supports secondary objectives | Tangential to engagement goals |
| Business Impact Proof | 25% | Material risk proof (regulatory fine, stock impact, competitive damage) | Significant impact demonstration | Minor impact proof |
| Operational Feasibility | 25% | Reliable access, proven channel, low DLP risk | Some uncertainty in access or channel | Requires new capabilities or high DLP risk |
| Time Efficiency | 20% | High value per hour of effort (small volume, high sensitivity) | Moderate value-to-time ratio | Large volume, moderate value, long extraction time |

#### 6b. Scored Target List

```
| Rank | Source ID | Location | Description | Objective Align. | Business Impact | Feasibility | Time Efficiency | Total Score | Decision |
|------|-----------|----------|-------------|------------------|----------------|-------------|-----------------|-------------|----------|
| 1 | {{id}} | {{location}} | {{desc}} | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{total}}/3.0 | Full extract |
| 2 | {{id}} | {{location}} | {{desc}} | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{total}}/3.0 | Full extract |
| 3 | {{id}} | {{location}} | {{desc}} | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{total}}/3.0 | PoC sample |
| 4 | {{id}} | {{location}} | {{desc}} | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{score}}/3 | {{total}}/3.0 | PoC sample |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Decision categories:**
- **Full extract**: Complete exfiltration of the data source — justified by engagement objectives and feasibility
- **PoC sample**: Proof-of-concept extraction only — representative sample sufficient for report findings
- **Defer**: Not prioritized for current operational window — available for follow-up if time permits
- **Exclude**: Failed RoE check or infeasible — removed from target list

**Present the FINAL Prioritized Exfiltration Target List — this is the authoritative document for steps 04-10:**

```
=== PRIORITIZED EXFILTRATION TARGET LIST ===
Date: {{date}}
Operator: {{operator}}
Total targets: {{count}}
Total volume (compressed): {{volume}}
Estimated total time: {{time}}

[FULL EXTRACT TARGETS]
1. {{source_id}} — {{location}} — {{volume}} — {{channel}} — {{justification}}
2. {{source_id}} — {{location}} — {{volume}} — {{channel}} — {{justification}}
3. ...

[PROOF-OF-CONCEPT TARGETS]
1. {{source_id}} — {{location}} — {{sample_size}} of {{total}} — {{channel}} — {{justification}}
2. ...

[DEFERRED TARGETS]
1. {{source_id}} — {{reason_for_deferral}}
2. ...

[EXCLUDED TARGETS (RoE)]
1. {{source_id}} — {{exclusion_reason}}
2. ...
```

### 7. Exfiltration Strategy Recommendation

Based on the assessment results, present the recommended exfiltration strategy that will guide steps 04-10.

#### 7a. Per-Target Strategy

```
| Rank | Source ID | Extract Type | Collection Method | Staging Location | Exfil Channel | Estimated Time | Sequence Order |
|------|-----------|-------------|-------------------|-----------------|---------------|----------------|----------------|
| 1 | {{id}} | Full / PoC | {{method}} | {{staging_host}} | HTTPS/Cloud/DNS/Covert | {{time}} | Phase 1 |
| 2 | {{id}} | Full / PoC | {{method}} | {{staging_host}} | {{channel}} | {{time}} | Phase 1 |
| 3 | {{id}} | Full / PoC | {{method}} | {{staging_host}} | {{channel}} | {{time}} | Phase 2 |
```

#### 7b. Exfiltration Phasing Strategy

```
Phase 1 — Quick Wins ({{time_estimate}}):
- Small, high-value targets that prove engagement objectives with minimal risk
- Targets: {{list}}
- Channel: {{primary_channel}}
- Goal: Establish exfiltration capability and deliver initial proof

Phase 2 — Primary Extraction ({{time_estimate}}):
- Main engagement targets requiring larger transfers
- Targets: {{list}}
- Channel: {{primary_channel}} + {{backup_channel}}
- Goal: Complete primary objective exfiltration

Phase 3 — Extended Operations ({{time_estimate}} — if time permits):
- Additional targets and deferred items
- Targets: {{list}}
- Channel: {{channel}}
- Goal: Maximum coverage within operational window
```

#### 7c. Resource Requirements Summary

```
| Resource | Requirement | Available | Status |
|----------|------------|-----------|--------|
| Staging disk space | {{total_staging_size}} | {{available}} | ✅/❌ |
| Encryption tools | AES-256 capable tool on staging hosts | {{available_tools}} | ✅/❌ |
| Compression tools | 7z/gzip/zstd on staging hosts | {{available_tools}} | ✅/❌ |
| Network bandwidth | {{required_bw}} for {{duration}} | {{available_bw}} | ✅/❌ |
| Exfil infrastructure | {{channel_infrastructure}} | {{status}} | ✅/❌ |
| Time window | {{total_time_needed}} | {{available_window}} | ✅/❌ |
```

### 8. Document Findings

**Write consolidated assessment findings to the output document under `## Data Assessment & Classification`:**

```markdown
## Data Assessment & Classification

### Master Data Inventory
{{master_inventory — all sources with assessment fields populated}}

### Volume Assessment
{{volume_table — per-source and total with compression estimates and bandwidth calculations}}

### Sensitivity Classification
{{classification_table — every source with level, justification, regulatory framework}}

### RoE Compliance Matrix
{{roe_matrix — authorization status, restrictions, exclusions with reasons}}

### Feasibility Assessment
{{feasibility_tables — access reliability, transfer feasibility, DLP risk, time requirements}}

### Prioritized Exfiltration Target List
{{prioritized_list — ranked targets with scores, decisions, and justifications}}

### Exfiltration Strategy Recommendation
{{strategy — phasing, per-target approach, resource requirements}}

### Assessment OPSEC Log
{{opsec_log — all detection events generated during assessment}}
```

### 9. Present MENU OPTIONS

"**Data assessment and classification complete.**

Summary: {{total_sources}} data sources assessed — {{include_count}} authorized (INCLUDE), {{restrict_count}} restricted (PoC only), {{exclude_count}} excluded (RoE). Total exfiltration volume: {{total_volume}} (compressed: {{compressed}}). Estimated total time: {{total_time}}.
Priority sequence: {{phase1_targets}} (quick wins) → {{phase2_targets}} (primary) → {{phase3_targets}} (extended). Recommended channels: {{channels}}.

**Select an option:**
[A] Advanced Elicitation — Deep dive into classification decisions (challenge sensitivity levels, question RoE interpretations, explore alternative prioritization, reassess feasibility for borderline targets)
[W] War Room — Red (exfiltration efficiency optimization, monitoring blind spot exploitation, multi-channel parallelization, backup target strategy) vs Blue (DLP coverage gap analysis, monitoring detection capabilities per target, data classification accuracy, RoE enforcement verification)
[C] Continue — Proceed to Step 4: Data Collection & Staging"

#### Menu Handling Logic:

- IF A: Deep-dive analysis of assessment decisions — challenge sensitivity classifications (is L3 data actually L4?), question RoE interpretations for borderline cases, explore alternative prioritization weights, reassess feasibility for targets near the include/exclude boundary, investigate whether PoC targets should be upgraded to full extract or vice versa. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: is the exfiltration phasing optimal? Can multiple channels be used in parallel to reduce total time? Are backup targets being undervalued as low-monitoring alternatives? Can cloud storage exfiltration bypass on-prem DLP entirely? Blue Team perspective: which data sources have inadequate DLP coverage? Are sensitivity classifications accurate based on the discovery? What monitoring improvements would detect this assessment activity? How should RoE controls be verified in real engagements? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-04-staging.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and assessment findings appended to report], will you then read fully and follow: `./step-04-staging.md` to begin data collection and staging.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All discovered data sources from step-02 compiled into master inventory with unique identifiers
- Volume estimation completed for every data source with per-source and total calculations including compression estimates
- Sensitivity classification applied to every source using L1-L4 framework with justification and regulatory mapping
- RoE compliance check performed for EVERY data source — no source reaches step-04 without authorization verification
- Excluded sources documented with clear RoE prohibition reasons
- Feasibility assessment completed across all dimensions: access reliability, transfer feasibility, DLP/monitoring risk, time requirements
- Prioritized exfiltration target list produced with weighted multi-factor scoring and clear decisions (full/PoC/defer/exclude)
- Exfiltration strategy recommendation presented with phasing, per-target channel selection, and resource requirements
- Bandwidth feasibility calculated — total volume vs. available bandwidth vs. time window
- Assessment OPSEC events documented
- Findings appended to report under `## Data Assessment & Classification`
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted

### ❌ SYSTEM FAILURE:

- Not assessing every data source from the step-02 inventory (cherry-picking targets without systematic assessment)
- Skipping RoE compliance check for any data source — ALL sources must be verified
- Including RoE-excluded data in the exfiltration target list
- Not estimating volumes (volume drives channel selection and is required for steps 05-07)
- Not classifying sensitivity (classification drives prioritization and report findings)
- Not assessing DLP/monitoring risk per source (risk assessment drives evasion strategy in step-08)
- Collecting, staging, or transferring data during assessment (that is step-04 and beyond)
- Producing a target list without weighted scoring and justification
- Not calculating bandwidth feasibility (failed exfiltration due to bandwidth exceeding time window)
- Proceeding without user selecting 'C' (Continue)
- Not documenting assessment OPSEC events
- Not recommending exfiltration phasing strategy (phases drive operational sequencing)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is DATA ASSESSMENT — no collection, no staging, no exfiltration. Every data source must be assessed, classified, RoE-verified, and prioritized before any data movement begins.
