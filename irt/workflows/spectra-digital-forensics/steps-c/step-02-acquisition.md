# Step 2: Evidence Acquisition & Preservation

**Progress: Step 2 of 10** — Next: Disk Forensic Analysis

## STEP GOAL:

Plan and execute (or document) the forensic acquisition of all evidence items, ensuring every acquisition follows forensic best practices — write blockers for disk imaging, proper tools for memory capture, validated export methods for logs and network data, and API-based collection for cloud evidence. Every acquisition produces a forensic copy with verified integrity, and the original evidence is never modified. Working copies are created for analysis; master copies are preserved untouched.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify, access, or write to original evidence — all operations produce forensic copies
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous acquisition tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst planning and documenting forensic acquisition methodology under ISO 27037 and NIST SP 800-86
- ✅ Acquisition is the foundation — if evidence is acquired improperly, every analysis step downstream is compromised
- ✅ Write blockers are mandatory for physical disk access — no exceptions, no shortcuts, no "I'll be careful"
- ✅ The order of volatility (RFC 3227) governs acquisition priority — most volatile evidence first
- ✅ Every acquisition must be reproducible — document the exact tool, version, parameters, and procedure so another examiner can verify

### Step-Specific Rules:

- 🎯 Focus exclusively on acquisition planning, forensic imaging methodology, preservation protocols, working copy creation, and integrity verification of acquired evidence
- 🚫 FORBIDDEN to analyze evidence content — that begins in steps 3-6. This step acquires and preserves; analysis comes later
- 🚫 FORBIDDEN to access original evidence without write protection
- 🚫 FORBIDDEN to skip integrity verification for any acquired evidence item
- 💬 Approach: Systematic acquisition following order of volatility, with documentation at every stage
- 📊 Every acquired evidence item must include: acquisition method, tool details, write protection method, hash at acquisition, hash verification of copy, and storage location
- 🔒 Chain of custody must be updated for every acquisition operation

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Imaging a disk without a hardware or software write blocker risks modifying the original evidence with every read operation — even mounting a filesystem updates access timestamps, and NTFS journals update on mount, creating detectable modifications that opposing counsel will identify and exploit
  - Capturing memory by writing the dump to the evidence system itself overwrites memory pages with the dump file, destroying the very evidence you are trying to capture — always write memory dumps to external media or a network share, never to the local disk of the system being acquired
  - Acquiring disk images before memory dumps on a running system permanently loses volatile evidence — once the system is powered off for disk imaging, all running processes, network connections, decryption keys, and in-memory malware artifacts are gone forever and cannot be recovered from the disk image
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present acquisition plan before beginning any acquisition activity
- ⚠️ Follow order of volatility strictly — most volatile evidence first
- 📋 Update chain of custody for EVERY acquisition operation
- 🔒 Hash EVERY acquired evidence item immediately after acquisition (SHA-256 minimum, MD5 + SHA-256 standard)
- ⚠️ Present [A]/[W]/[C] menu after acquisition planning and documentation is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `acquisition_methods`, `evidence_items`, `evidence_types`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Case intake data, evidence inventory, chain of custody records, forensic question, scope definition, legal context, incident handling cross-reference
- Focus: Acquisition planning, forensic imaging methodology, memory capture, log collection, network capture, cloud evidence collection, preservation protocols, working copy creation, and integrity verification
- Limits: Only acquire evidence from systems within the engagement scope — acquisition from third-party systems requires separate authorization. Do not analyze evidence content.
- Dependencies: Case intake and evidence receipt completed in step-01-init.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Acquisition Planning — Order of Volatility

Based on the case scope, evidence inventory, and forensic question, develop a comprehensive acquisition plan. Follow the order of volatility from RFC 3227 — the most volatile evidence is acquired first because it disappears first.

**Evidence Acquisition Priority Matrix:**

**Priority 1 — Volatile Evidence (exists only in live/running state):**

1. **CPU Registers, Cache:**
   - Captured implicitly in memory dumps — no separate acquisition
   - Note for completeness in the acquisition plan

2. **Routing Table, ARP Cache, Process Table, Kernel Statistics:**
   - Windows: `route print`, `arp -a`, `tasklist /v /fo csv`, `netstat -anob`, `systeminfo`, `ipconfig /all`, `net session`, `net use`
   - Linux: `ip route`, `arp -a`, `ps auxwww`, `ss -tulnp`, `uname -a`, `cat /proc/meminfo`, `lsmod`, `who`
   - macOS: `netstat -rn`, `arp -a`, `ps auxwww`, `lsof -i`, `system_profiler`
   - **Collection method:** Run commands, redirect output to external media with timestamps
   - **CRITICAL:** These are point-in-time snapshots — record exact collection timestamp for each

3. **Memory Contents (RAM):**
   - **Windows acquisition tools:**
     - WinPmem (open-source, kernel driver, raw format): `winpmem_mini_x64.exe output.raw`
     - DumpIt (Comae, single executable, simple): `DumpIt.exe`
     - Belkasoft RAM Capturer (free, minimal footprint)
     - Magnet RAM Capture (free, user-friendly)
     - FTK Imager (memory capture mode, widely accepted in courts)
   - **Linux acquisition tools:**
     - LiME (Loadable Kernel Module): `insmod lime-$(uname -r).ko "path=/mnt/evidence/mem.lime format=lime"`
     - /proc/kcore (limited, does not capture all memory regions)
     - crash utility (for kernel debugging)
   - **macOS acquisition tools:**
     - osxpmem (requires SIP disable or kext approval)
     - MacQuisition (commercial, full acquisition suite)
   - **Hibernation/pagefile:**
     - Windows: `hiberfil.sys` (hibernation data), `pagefile.sys` (paged memory), `swapfile.sys`
     - Linux: swap partition or swap file
     - These contain memory pages written to disk — acquire as part of disk imaging
   - **Cloud VM memory:**
     - AWS: Create forensic AMI snapshot, or use SSM to run memory capture tool
     - Azure: Disk snapshot captures committed memory; or use VM extension for live capture
     - GCP: Machine image captures instance state
   - **Timing considerations:**
     - Memory MUST be captured before any containment action that changes system state
     - Memory MUST be captured before powering off the system for disk imaging
     - Order: volatile data collection → memory capture → disk imaging
   - **Output destination:** ALWAYS to external media or network share — NEVER to the evidence system
   - **Verification:** Hash immediately after capture, verify file size matches system RAM (± tool overhead)

4. **Temporary File Systems:**
   - Collected as part of disk imaging (Priority 1.5 — bridge between volatile and persistent)
   - Windows: `%TEMP%`, `%TMP%`, `C:\Windows\Temp\`, `%APPDATA%\Local\Temp\`
   - Linux: `/tmp/`, `/var/tmp/`, swap partitions
   - macOS: `/tmp/`, `/private/var/folders/`
   - If live acquisition: capture directory listings and file metadata before imaging

**Priority 2 — Semi-Volatile Evidence (persists but may be overwritten or rotated):**

5. **Disk Data (full forensic image):**
   - **Physical acquisition (preferred for evidentiary purposes):**
     - Power down system, remove disk, connect via write blocker
     - Tools: dc3dd, FTK Imager, Guymager, ewfacquire
     - Hardware write blockers: Tableau T35689iu, CRU WiebeTech, Wiebetech UltraDock
     - Software write blockers: Linux `mount -o ro,noexec,noatime`, Windows Registry forensic boot
   - **Live acquisition (when system cannot be powered down):**
     - F-Response (enterprise remote forensic imaging)
     - GRR Rapid Response (Google's incident response framework)
     - Velociraptor (open-source endpoint monitoring and forensic collection)
     - FTK Imager CLI (live disk imaging)
   - **Image formats:**
     - E01 (EnCase/Expert Witness): compressed, embedded hashes, case metadata, industry standard
     - AFF4 (Advanced Forensic Format): modern, supports compression and encryption, open standard
     - Raw/dd: universal compatibility, no compression, largest file size, no embedded metadata
   - **Write blocker verification:**
     - Before imaging: verify write blocker is functioning — attempt a test write and confirm it is blocked
     - Document: write blocker make/model/serial, firmware version, verification test result
   - **Imaging procedure:**
     1. Connect source disk via write blocker
     2. Hash source disk before imaging (if accessible): `sha256sum /dev/sdX`
     3. Execute imaging: `dc3dd if=/dev/sdX of=/path/to/image.dd hash=sha256 log=imaging.log`
     4. Or for E01: `ewfacquire /dev/sdX -t /path/to/image -f encase6 -c best -S 2G`
     5. Hash the completed image
     6. Verify: source hash == image hash (bit-for-bit identical)
     7. If hash mismatch: re-image; if persistent mismatch, document bad sectors/hardware issues
     8. Create working copy from master image (never analyze master)
     9. Hash working copy and verify against master

6. **Remote Logging & Monitoring Data:**
   - **Time window:** Forensic question timeframe ± 72 hours minimum buffer (± 30 days for APT/advanced threats)
   - **SIEM exports:**
     - Splunk: `| outputcsv` or REST API export
     - Elastic/Kibana: Kibana CSV export or Elasticsearch scroll API
     - Sentinel: Log Analytics query export or Azure CLI
     - QRadar: ARIEL query export
   - **EDR telemetry:**
     - CrowdStrike: RTR session data, detection details, process timeline
     - SentinelOne: Deep Visibility queries, threat details
     - Microsoft Defender: Advanced Hunting queries, device timeline
     - Carbon Black: process search, binary analysis, watchlist hits
   - **Windows Event Logs:**
     - Security (4624/4625/4648/4672/4688/4698/4720/7045)
     - System (7034/7036/7040/7045)
     - PowerShell (4103/4104)
     - Sysmon (if deployed: 1/3/7/8/10/11/12/13/22/23)
     - Terminal Services (21/22/23/24/25)
     - TaskScheduler (106/140/141/200/201)
   - **Network device logs:**
     - Firewall: allowed/denied connections, NAT translations, VPN sessions
     - Proxy/SWG: HTTP/HTTPS requests, URL categories, user agents
     - DNS server: query logs with source IP, queried domain, response
     - IDS/IPS: triggered signatures with packet captures
   - **Cloud logs:**
     - AWS: `aws cloudtrail lookup-events --start-time --end-time`, S3 server access logs, VPC Flow Logs, GuardDuty findings
     - Azure: `az monitor activity-log list`, Azure AD sign-in logs, NSG Flow Logs, Key Vault audit
     - GCP: `gcloud logging read`, Cloud Audit Logs (Admin Activity, Data Access), VPC Flow Logs
     - M365: Unified Audit Log (Search-UnifiedAuditLog), Exchange message trace, SharePoint access logs
     - Google Workspace: Admin Audit, Drive activity, Gmail logs, Login audit
   - **Email logs:** Mail transport logs, message tracking, DLP alerts, mail rule audit
   - **Authentication logs:** Windows Security (logon events), Kerberos, RADIUS/TACACS, SSO/SAML, MFA events

7. **Network Capture Data:**
   - **Full packet capture (PCAP):**
     - Live capture: `tcpdump -i ethX -w capture.pcap -G 3600 -W 24`
     - NSM historical: check Security Onion, Zeek, Arkime (Moloch), NetworkMiner
     - SPAN/TAP: mirror traffic from affected network segments
   - **Flow data:**
     - NetFlow v5/v9/IPFIX from routers, switches, firewalls
     - sFlow from switches
   - **DNS query logs from DNS servers or security tools (Umbrella, Infoblox, Pi-hole)**
   - **Proxy/firewall logs (see item 6 above)**

8. **Physical Configuration & Network Topology:**
   - Network device running configs (switches, routers, firewalls)
   - VLAN assignments, port security configurations
   - DNS zone files, DHCP lease tables
   - Cloud security group / NSG rules
   - Load balancer, reverse proxy configurations

**Priority 3 — Non-Volatile Evidence (persistent, stable):**

9. **Archival & Reference Data:**
   - Backup snapshots from before the incident window (for clean-state comparison)
   - Previous forensic images from related cases
   - Archived logs beyond active retention
   - Configuration management database (CMDB) records
   - Change management records for the incident window

**Present as acquisition plan matrix:**

```
| # | Evidence Type | Priority | Source System(s) | Acquisition Method | Tool | Write Protection | Assigned Collector | Estimated Size | Status |
|---|---------------|----------|------------------|--------------------|------|------------------|--------------------|----------------|--------|
| 1 | {{type}} | P1/P2/P3 | {{system}} | {{method}} | {{tool}} | {{write_blocker}} | {{collector}} | {{size}} | Pending/Acquired/Failed/N-A |
```

**Acquisition Scope Decision:**

Present the plan and ask the operator to confirm scope:

"**Acquisition Plan Ready.**

Total acquisition items: {{count}}
- Priority 1 (Volatile): {{p1_count}} items
- Priority 2 (Semi-Volatile): {{p2_count}} items
- Priority 3 (Non-Volatile): {{p3_count}} items
- Estimated total size: {{total_size}}

Not all evidence types are needed for every investigation. The forensic question drives what is relevant. For items marked N/A: the exclusion rationale is documented.

Confirm, modify, or refine this acquisition plan."

### 2. Preservation Protocols

For all acquired evidence, establish and document preservation protocols:

**Master Copy vs Working Copy:**
- **Master copy**: The original forensic acquisition — NEVER analyzed, NEVER modified, stored securely with access logging
- **Working copy**: A verified duplicate of the master — this is what gets analyzed in steps 3-6
- **Verification**: Working copy hash MUST match master copy hash before any analysis begins

**Working Copy Creation Procedure:**
1. Hash the master copy (should already have hash from acquisition)
2. Create a bit-for-bit copy: `dc3dd if=master.E01 of=working.E01 hash=sha256`
3. Hash the working copy
4. Compare: master hash == working copy hash
5. If match: working copy is verified — proceed to analysis
6. If mismatch: re-copy; investigate storage medium for errors

**Storage Security:**
- Encrypted storage: All evidence storage must be encrypted at rest (LUKS, BitLocker, FileVault, or encrypted container)
- Access control: Restrict to authorized forensic personnel only
- Access logging: Every access to evidence storage must be logged
- Physical security: If on physical media, store in locked evidence locker
- Append-only: Evidence storage is append-only — new items added, existing items never modified or deleted

**Storage Directory Structure:**
```
{irt_evidence_chain}/
  {case_id}/
    manifest.md                          — Master evidence inventory with hashes
    integrity-log.md                     — Hash verification log with timestamps
    chain-of-custody/
      EVD-{case_id}-001-coc.md           — Per-item chain of custody
    master/
      memory/
        EVD-{case_id}-XXX-hostname.lime  — Master memory dumps
      disk-images/
        EVD-{case_id}-XXX-hostname.E01   — Master forensic disk images
      logs/
        EVD-{case_id}-XXX-source.json    — Master log exports
      network/
        EVD-{case_id}-XXX-capture.pcap   — Master network captures
      cloud/
        EVD-{case_id}-XXX-service.json   — Master cloud log exports
      volatile/
        EVD-{case_id}-XXX-processes.txt  — Volatile data captures
    working/
      (mirrors master/ structure — these are analyzed)
```

**Chain of Custody Update:**
For every acquisition operation, add a chain of custody entry:
```
| Transfer # | Date/Time (UTC) | Released By | Received By | Purpose | Location Before | Location After | Hash Verified |
|------------|-----------------|-------------|-------------|---------|-----------------|----------------|---------------|
| {{seq}} | {{timestamp}} | {{source}} | {{analyst}} | Forensic acquisition | {{source_system}} | {{storage_path}} | Yes — {{hash}} |
```

### 3. Mobile Evidence Acquisition (If Applicable)

If mobile devices are in scope:

**Mobile Acquisition Methods:**
- **Physical acquisition** (full bit-for-bit image): Cellebrite UFED, GrayKey, Oxygen Forensic Detective
- **Logical acquisition** (file-level copy): iTunes backup (iOS), ADB backup (Android), Cellebrite logical
- **Cloud acquisition** (associated cloud accounts): iCloud, Google Account, Samsung Cloud
- **Manual acquisition** (screenshots, photos): For locked devices or as supplement

**Mobile-Specific Considerations:**
- Airplane mode immediately upon seizure (prevent remote wipe, new data, or location tracking)
- Faraday bag if airplane mode cannot be enabled
- Do NOT attempt passcode guesses — may trigger lockout or data destruction
- Document device state: powered on/off, locked/unlocked, airplane mode status, battery level
- Preserve SIM card separately with chain of custody

### 4. Acquisition Execution & Verification

For each evidence item in the acquisition plan, document the acquisition execution:

**Per-Item Acquisition Record:**
```
| Field | Value |
|-------|-------|
| Evidence ID | EVD-{case_id}-{NNN} |
| Acquisition Start | {{UTC timestamp}} |
| Acquisition End | {{UTC timestamp}} |
| Duration | {{HH:MM:SS}} |
| Tool | {{name, version}} |
| Tool Hash (SHA-256) | {{hash of the tool binary — proves tool integrity}} |
| Parameters | {{exact command line or configuration}} |
| Write Protection | {{hardware write blocker model/serial OR software method}} |
| Source Hash (before acquisition) | {{hash if accessible}} |
| Acquisition Hash (SHA-256) | {{hash of acquired image}} |
| Acquisition Hash (MD5) | {{hash of acquired image}} |
| File Size | {{bytes}} |
| Master Copy Location | {{path}} |
| Working Copy Created | {{yes/no}} |
| Working Copy Hash Match | {{yes — verified / no — ALERT}} |
| Working Copy Location | {{path}} |
| Errors/Anomalies | {{any issues during acquisition}} |
| Chain of Custody Updated | {{yes — entry #}} |
```

**Present final acquisition inventory:**

```
| # | EVD ID | Description | Source | Method | Tool | Hash (SHA-256) | Size | Working Copy | Status |
|---|--------|-------------|--------|--------|------|----------------|------|--------------|--------|
| 1 | EVD-{case_id}-001 | {{desc}} | {{source}} | {{method}} | {{tool}} | {{hash}} | {{size}} | ✅/❌ | Acquired/Failed/N-A |
```

**Acquisition Summary:**
```
Total acquisition items planned: {{planned_count}}
Total items acquired: {{acquired_count}}
Total items failed: {{failed_count}} — {{reasons}}
Total items N/A: {{na_count}} — {{reasons}}
Total evidence size (master): {{master_size}}
Total evidence size (working): {{working_size}}
All master hashes verified: {{Yes / No — detail}}
All working copies verified: {{Yes / No — detail}}
Chain of custody entries added: {{coc_count}}
Write blockers used: {{count}} / {{required_count}}
```

### 5. Evidence Type Classification for Downstream Analysis

Based on the acquired evidence, determine which analysis phases (steps 3-6) are applicable:

**Analysis Applicability Matrix:**

```
| Analysis Phase | Step | Applicable | Evidence Available | EVD IDs |
|----------------|------|------------|-------------------|---------|
| Disk Forensics | Step 3 | ✅/❌/Partial | {{disk images, file system exports}} | EVD-{case_id}-XXX |
| Memory Forensics | Step 4 | ✅/❌/Partial | {{memory dumps, hibernation files}} | EVD-{case_id}-XXX |
| Network Forensics | Step 5 | ✅/❌/Partial | {{PCAPs, flow data, network logs}} | EVD-{case_id}-XXX |
| Cloud Forensics | Step 6 | ✅/❌/Partial | {{cloud logs, SaaS audit logs}} | EVD-{case_id}-XXX |
```

- **Applicable**: Sufficient evidence exists for meaningful analysis
- **Partial**: Some evidence exists but coverage is incomplete — analysis will have documented gaps
- **Not Applicable**: No evidence of this type was acquired — step will be documented as N/A with reason

### 6. Append Findings to Report

Write all acquisition and preservation findings under `## Acquisition & Preservation` in the output file `{outputFile}`:

```markdown
## Acquisition & Preservation

### Acquisition Plan
{{acquisition_plan_matrix_from_instruction_1}}

### Acquisition Methodology Per Evidence Type
{{per_type_methodology_documentation}}

### Working Copy Verification
{{master_vs_working_copy_hash_verification_table}}

### Storage & Security
{{storage_directory_structure_and_security_measures}}
```

Update Evidence Inventory section with any new evidence items acquired in this step.

Update frontmatter:
- Add this step name (`Evidence Acquisition & Preservation`) to the end of the `stepsCompleted` array
- Update `acquisition_methods` with the list of acquisition tools used
- Update `evidence_items` array with any new EVD IDs
- Update `evidence_item_count` with the total count
- Update `evidence_types` booleans (disk, memory, network, cloud, mobile)
- Update `chain_of_custody_entries` with the current total
- Set `integrity_verified` to `true` if all hashes match, `false` if any discrepancies

### 7. Present MENU OPTIONS

"**Evidence acquisition and preservation complete.**

Evidence items acquired: {{acquired_count}} / {{planned_count}} planned
Evidence failed/unavailable: {{failed_count}}
Total evidence size: {{total_size}}
Chain of custody: {{intact / broken — detail}}
Hash verification: {{all passed / {{failed_count}} failures}}
Working copies: {{all verified / {{failed_count}} failures}}
Write blockers: {{count}} used / {{required_count}} required

**Analysis Applicability:**
- Disk Forensics (Step 3): {{applicable / partial / N-A}}
- Memory Forensics (Step 4): {{applicable / partial / N-A}}
- Network Forensics (Step 5): {{applicable / partial / N-A}}
- Cloud Forensics (Step 6): {{applicable / partial / N-A}}

**Select an option:**
[A] Advanced Elicitation — Challenge acquisition completeness, identify collection gaps, assess whether evidence is sufficient to answer the forensic question
[W] War Room — Red (what evidence did the attacker destroy before we acquired it? what anti-forensic techniques would defeat our acquisition?) vs Blue (is our evidence set forensically sound? will it withstand legal challenge? are there additional sources we should acquire?)
[C] Continue — Proceed to Step 3: Disk Forensic Analysis (Step 3 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the acquisition plan and execution. Is the evidence set sufficient to answer the forensic question? Are there systems that should have been imaged but were not? Are there log sources with gaps in coverage or retention? Was the order of volatility followed correctly? Could any acquisition method have inadvertently modified evidence? Are there additional evidence sources that would strengthen the investigation? Is the chain of custody documentation complete enough for the legal context? Process insights, ask user if they want to acquire additional evidence, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: before the forensic analyst acquired evidence, what did I have time to destroy? Did I run secure deletion tools? Did I clear event logs and scrub the USN journal? Did I corrupt memory before it was dumped? Did I plant false evidence to misdirect? Are there systems I compromised that the analyst did not acquire? Blue Team perspective: is every evidence item acquired with write protection? Do all hashes verify? Is the chain of custody legally defensible? Could opposing counsel challenge any acquisition methodology? Are there gaps in our evidence that the attacker could have exploited? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated with acquisition_methods, evidence_items, evidence_types, chain_of_custody_entries, integrity_verified, and this step added to stepsCompleted. Then read fully and follow: ./step-03-disk-forensics.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, acquisition_methods populated, evidence_items updated, evidence_types set, chain_of_custody_entries counted, integrity_verified set, and Acquisition & Preservation section fully populated in the output document], will you then read fully and follow: `./step-03-disk-forensics.md` to begin disk forensic analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Acquisition plan developed following order of volatility (RFC 3227) with priority, source, method, tool, write protection, and assigned collector for each item
- Forensic acquisition methodology documented per evidence type with tool, procedure, and verification steps
- Write blockers used (or documented as not applicable with reason) for all physical disk access
- Memory acquisition documented with output to external media and hash verification
- Disk imaging completed with write blocker verification and bit-for-bit hash verification
- Log collection documented with defined time window, export method, and hash at collection
- Cloud evidence collection documented with API method, time window, and hash at export
- Working copies created for all master evidence items with hash verification
- Chain of custody updated for every acquisition operation
- Evidence type classification completed for downstream analysis routing (steps 3-6)
- Acquisition summary presented with counts, sizes, and verification status
- Storage directory structure established with encryption and access controls
- Frontmatter updated with acquisition_methods, evidence_items, evidence_types, chain_of_custody_entries, integrity_verified
- Findings appended to report under `## Acquisition & Preservation`
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Acquiring disk images without write blockers
- Writing memory dumps to the evidence system itself
- Not following order of volatility (imaging disk before capturing memory on a running system)
- Not hashing evidence at the point of acquisition
- Not creating working copies (analyzing master evidence directly)
- Working copy hash not verified against master
- Not documenting acquisition tool name, version, and parameters
- Chain of custody not updated for every acquisition operation
- Analyzing evidence content during this step (analysis belongs to steps 3-6)
- Declaring acquisition complete without verifying all planned items are accounted for (acquired, failed with reason, or N/A with reason)
- Not classifying evidence types for downstream analysis routing
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Evidence acquisition is irreversible — you get one chance to do it right. Write blockers are mandatory. Hash everything. Document everything. The original evidence is sacred. Forensic integrity is non-negotiable.
