# Step 3: Disk Forensic Analysis

**Progress: Step 3 of 10** — Next: Memory Forensic Analysis

## STEP GOAL:

Conduct comprehensive disk forensic analysis on acquired forensic images — file system analysis, operating system artifact extraction, application artifact recovery, deleted file recovery, and anti-forensics detection. Every finding is documented with evidence ID, artifact source, timestamp, and confidence level. Analysis is performed exclusively on working copies; master evidence is never accessed.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER access or modify master evidence — analyze ONLY working copies
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous analysis engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst conducting structured disk forensic examination under ISO 27037 and NIST SP 800-86
- ✅ Disk forensics is the workhorse of digital investigation — file system artifacts survive reboots, log clearing, and most anti-forensics techniques
- ✅ Every artifact has a story to tell — timestamps reveal sequences, metadata reveals actors, deleted files reveal intent
- ✅ The $MFT is the ground truth for NTFS — it records every file that ever existed, even after deletion
- ✅ Anti-forensics detection is as important as artifact recovery — what the attacker tried to hide tells you what they valued

### Step-Specific Rules:

- 🎯 Focus exclusively on disk forensic analysis: file system examination, OS artifact extraction, application artifact recovery, deleted file carving, and anti-forensics detection
- 🚫 FORBIDDEN to perform memory analysis — that is step 4
- 🚫 FORBIDDEN to perform network analysis — that is step 5
- 🚫 FORBIDDEN to modify working copies — mount read-only, analyze with forensic tools
- 💬 Approach: Systematic artifact extraction across all evidence types, cross-referencing findings with the forensic question
- 📊 Every finding must cite: evidence ID (EVD-{case_id}-{NNN}), artifact source, file path, timestamp, and confidence level
- 🔒 Re-verify working copy hash before analysis begins — confirm integrity since acquisition

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Relying solely on file system timestamps without cross-referencing $MFT $STANDARD_INFORMATION vs $FILENAME timestamps risks missing timestomping — attackers routinely modify $SI timestamps (visible to dir/ls) while $FN timestamps (in $MFT) preserve the original values, and the discrepancy is the detection signal
  - Skipping deleted file recovery and unallocated space carving when investigating data theft or destruction means you are analyzing only what the attacker left visible — the deleted artifacts often contain the most incriminating evidence (staged files, tools, exfiltration scripts) that the attacker specifically tried to remove
  - Not checking for Alternate Data Streams (NTFS ADS) when investigating malware or data hiding misses a well-known concealment technique — ADS can store executable payloads, stolen data, or configuration files that are invisible to standard directory listings and most file explorers
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Verify working copy integrity before beginning analysis
- ⚠️ Mount all forensic images read-only — no write operations permitted
- 📋 Document every forensic tool used with name, version, and parameters
- 🔒 Cite evidence IDs for every finding
- ⚠️ Present [A]/[W]/[C] menu after disk forensic analysis is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of stepsCompleted and updating analysis_types, artifacts_recovered, and findings counts
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Case intake, forensic question, evidence inventory, acquisition records, evidence type classification (from step 2)
- Focus: Disk forensic analysis — file systems, OS artifacts, application artifacts, deleted files, anti-forensics
- Limits: If disk evidence was classified as N/A in step 2, document the N/A status and proceed to step 4. Only analyze working copies from `{irt_evidence_chain}/{case_id}/working/`
- Dependencies: Evidence acquired and preserved in step-02-acquisition.md, working copies created and verified

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check & Working Copy Verification

**If disk evidence was classified as N/A in step 2:**

"**Disk Forensics — Not Applicable**

No disk images or file system evidence was acquired for this case. Reason: {{reason_from_step_2}}.

This step is documented as N/A. The forensic question will be addressed using other evidence types (memory, network, cloud) in subsequent steps."

Document the N/A status in the report and proceed directly to the menu (instruction 8) with only the C option to advance.

**If disk evidence is available:**

Before any analysis, re-verify working copy integrity:

```
| EVD ID | Evidence Type | Working Copy Path | Master Hash (SHA-256) | Current Hash (SHA-256) | Match | Analyst | Verification Time |
|--------|---------------|-------------------|----------------------|------------------------|-------|---------|-------------------|
| EVD-{case_id}-XXX | Disk Image | {{path}} | {{master_hash}} | {{current_hash}} | ✅/❌ | {{analyst}} | {{UTC timestamp}} |
```

If ANY hash mismatch: STOP. The working copy may have been modified since creation. Investigate the cause. Create a new working copy from master if needed. Do NOT proceed with analysis on a working copy that fails integrity verification.

### 2. File System Analysis

For each disk image, identify and analyze the file system structure:

**File System Identification:**

| Disk Image | EVD ID | File System | Partition Table | Partitions | Total Size | Allocated | Unallocated |
|------------|--------|-------------|-----------------|------------|------------|-----------|-------------|
| {{image}} | EVD-{case_id}-XXX | NTFS/ext4/APFS/FAT32/HFS+/XFS | MBR/GPT | {{count}} | {{size}} | {{size}} | {{size}} |

**Per-Partition Analysis:**
- Partition type, offset, size, file system type
- Volume label, serial number
- File count, directory count
- Free space, unallocated clusters

**File System Artifacts:**

**NTFS-Specific Artifacts:**
- **$MFT (Master File Table):** Parse complete $MFT for all file entries (active and deleted)
  - Tools: analyzeMFT, MFTECmd (Eric Zimmerman), Autopsy
  - Extract: filename, parent directory, $STANDARD_INFORMATION timestamps, $FILENAME timestamps, file size, flags (deleted, directory, hidden, system)
  - Compare $SI timestamps vs $FN timestamps for every file of interest — discrepancies indicate timestomping
- **$UsnJrnl (USN Journal / Change Journal):** File system change log
  - Tools: MFTECmd, usnjrnl.py
  - Records: file creation, deletion, rename, data write, close, security change
  - Survives log clearing — attackers rarely scrub the USN Journal
- **$LogFile (NTFS Transaction Log):** File system transaction recovery
  - Tools: LogFileParser
  - Useful for recovering recently deleted or modified file operations
- **Alternate Data Streams (ADS):**
  - Scan for ADS on all files: `dir /r` equivalent via forensic tool
  - Tools: Autopsy ADS module, ADS Detector, streams.exe (Sysinternals)
  - Common attacker use: storing payloads, configs, or exfiltrated data in ADS
  - Zone.Identifier ADS: indicates file was downloaded from the internet

**ext4/Linux-Specific Artifacts:**
- Inode analysis: timestamps (atime, mtime, ctime, crtime for ext4)
- Journal analysis: ext4 journal for file system operations
- Deleted inode recovery: extundelete, ext4magic
- Extended attributes: security contexts, ACLs

**APFS/macOS-Specific Artifacts:**
- APFS snapshot analysis: time-stamped point-in-time snapshots
- Spotlight metadata: .Spotlight-V100 indexes with file content and metadata
- Quarantine events: com.apple.quarantine extended attribute (downloaded files)
- FSEvents: file system event log (/.fseventsd/)
- KnowledgeC.db: user activity knowledge database

**File Signature Analysis (Magic Bytes):**
- Scan all files for extension vs magic byte mismatch
- Tools: file command, TrID, Autopsy file type module
- Common mismatches: .jpg containing .exe, .doc containing .ps1, .txt containing encoded payload
- Present mismatches:

```
| # | File Path | Expected Type (Extension) | Actual Type (Magic Bytes) | EVD ID | Suspicious |
|---|-----------|---------------------------|---------------------------|--------|------------|
| 1 | {{path}} | {{extension_type}} | {{magic_type}} | EVD-{case_id}-XXX | ✅/❌ |
```

**Deleted File Recovery:**
- **File carving (unallocated space):**
  - Tools: Autopsy (PhotoRec engine), Scalpel, foremost, bulk_extractor
  - Carve by file signature: executables, documents, archives, images, scripts
- **$MFT deleted entries:**
  - Recover file metadata for deleted files (timestamps, size, parent directory)
  - If file data clusters are not overwritten: full file recovery is possible
- **Slack space analysis:**
  - File slack (between end of file data and end of cluster): may contain remnants of previous files
  - Volume slack (between end of volume and end of partition)
  - Tools: Autopsy, EnCase, Sleuth Kit (blkstat, blkcat)

### 3. Operating System Artifact Extraction

Extract and analyze OS-specific artifacts relevant to the forensic question:

**Windows Artifacts:**

**Registry Analysis:**
- **SAM (Security Accounts Manager):**
  - Local user accounts, RIDs, account creation dates, last login dates
  - Password hint values, account lockout status
  - Tools: RegRipper, Registry Explorer (Eric Zimmerman), Autopsy
- **SYSTEM:**
  - Computer name, timezone, mounted devices (USBs, external drives)
  - Services (current control set): persistence via service creation
  - Network interface configurations
- **SOFTWARE:**
  - Installed programs (Uninstall keys), program execution (MUICache)
  - Network profiles (connected networks with dates)
  - Windows version, installation date
- **NTUSER.DAT (per user):**
  - Run/RunOnce keys (persistence)
  - TypedPaths, TypedURLs (user-typed paths and URLs)
  - RecentDocs MRU (recently opened documents)
  - UserAssist (ROT13 encoded program execution with run count and timestamps)
  - Shellbags (folder access history with timestamps — survives folder deletion)
  - ComDlg32 (Open/Save dialog history)
  - Software\Microsoft\Windows\CurrentVersion\Explorer\Map Network Drive MRU
- **UsrClass.dat (per user):**
  - Additional Shellbag data
  - COM class registrations
  - Virtualized registry for sandboxed applications

**Windows Event Logs (from disk):**
- Security.evtx: 4624 (logon), 4625 (failed logon), 4648 (explicit credentials), 4672 (special privileges), 4688 (process creation), 4698 (scheduled task created), 4720 (account created), 7045 (service installed)
- System.evtx: 7034 (service crashed), 7036 (service started/stopped), 7040 (start type changed)
- Microsoft-Windows-PowerShell/Operational.evtx: 4103 (module logging), 4104 (script block logging)
- Microsoft-Windows-Sysmon/Operational.evtx (if deployed): 1 (process create), 3 (network connection), 7 (image loaded), 8 (CreateRemoteThread), 10 (process access), 11 (file create), 12/13 (registry), 22 (DNS query), 23 (file delete)
- Microsoft-Windows-TerminalServices-RemoteConnectionManager/Operational.evtx: RDP connection events
- Microsoft-Windows-TaskScheduler/Operational.evtx: Task creation/execution/deletion
- Tools: EvtxECmd (Eric Zimmerman), python-evtx, Event Log Explorer, Chainsaw

**Execution Artifacts:**
- **Prefetch:** `C:\Windows\Prefetch\*.pf` — program execution with timestamps, run count, files/directories accessed
  - Tools: PECmd (Eric Zimmerman), WinPrefetchView
  - CRITICAL: Prefetch records execution even if the executable has been deleted
- **Amcache.hve:** `C:\Windows\appcompat\Programs\Amcache.hve` — program execution with SHA-1 hash, path, publisher, first execution time
  - Tools: AmcacheParser (Eric Zimmerman)
  - CRITICAL: Contains SHA-1 hash of executed files — even if the file is deleted, you have the hash for IOC matching
- **ShimCache (AppCompatCache):** Program execution evidence from `SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache`
  - Tools: ShimCacheParser, AppCompatCacheParser (Eric Zimmerman)
  - Records: file path, file size, last modified time (on disk), execution flag (Windows 7 only)
- **SRUM (System Resource Usage Monitor):** `C:\Windows\System32\sru\SRUDB.dat`
  - Per-application: network bytes sent/received, CPU time, foreground/background time
  - Tools: SrumECmd (Eric Zimmerman), srum-dump
  - CRITICAL: Proves application execution AND quantifies network usage — survives most cleanup
- **BAM/DAM (Background Activity Moderator):** `SYSTEM\CurrentControlSet\Services\bam\State\UserSettings\{SID}`
  - Last execution time for executables on Windows 10 1709+
  - Tools: Registry Explorer
- **Jump Lists:** `%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations\` and `CustomDestinations\`
  - Recent files per application, with timestamps
  - Tools: JLECmd (Eric Zimmerman)
- **LNK Files:** `%APPDATA%\Microsoft\Windows\Recent\`
  - Target path, target creation/modification/access times, volume serial number, MAC address
  - Tools: LECmd (Eric Zimmerman)

**Linux Artifacts:**
- `/var/log/auth.log` or `/var/log/secure`: Authentication events, sudo usage, SSH sessions
- `/var/log/syslog` or `/var/log/messages`: System events
- `~/.bash_history`, `~/.zsh_history`: Command history per user (may be cleared by attacker)
- `/var/log/wtmp` (parsed with `last`): Successful logins
- `/var/log/btmp` (parsed with `lastb`): Failed logins
- `/var/log/lastlog`: Last login per user
- Crontab files: `/var/spool/cron/crontabs/`, `/etc/cron.d/`, `/etc/crontab`
- systemd journals: `/var/log/journal/` — structured logging with rich metadata
- Package management: `/var/log/dpkg.log`, `/var/log/yum.log`, `/var/log/apt/history.log`
- Audit logs: `/var/log/audit/audit.log` (if auditd configured)
- `/tmp/` and `/var/tmp/`: Temporary files (attacker tools, staged data)
- SSH authorized_keys: `~/.ssh/authorized_keys` (persistence via added keys)
- SSH known_hosts: `~/.ssh/known_hosts` (lateral movement targets)

**macOS Artifacts:**
- Unified Logs: `log show --predicate 'eventMessage contains ...'` — comprehensive system logging
- FSEvents: `/.fseventsd/` — file system change journal (creation, deletion, modification, rename)
- Spotlight metadata: `.Spotlight-V100/` — indexed file content and metadata
- Quarantine events: `~/Library/Preferences/com.apple.LaunchServices.QuarantineEventsV2` — downloaded files with URL source
- KnowledgeC.db: `~/Library/Application Support/Knowledge/knowledgeC.db` — app usage, device activity, media playback
- TCC.db: `~/Library/Application Support/com.apple.TCC/TCC.db` — privacy permission grants (camera, microphone, screen recording, full disk access)
- Launch items: `~/Library/LaunchAgents/`, `/Library/LaunchAgents/`, `/Library/LaunchDaemons/` — persistence

### 4. Application Artifact Analysis

**Browser Forensics (Chrome/Firefox/Edge/Safari):**

| Browser | Profile Path | History DB | Downloads | Cache | Cookies | Extensions |
|---------|-------------|------------|-----------|-------|---------|------------|
| Chrome | `%LOCALAPPDATA%\Google\Chrome\User Data\Default\` | History (SQLite) | History (downloads table) | Cache/ | Cookies (SQLite) | Extensions/ |
| Firefox | `%APPDATA%\Mozilla\Firefox\Profiles\` | places.sqlite | places.sqlite (moz_downloads) | cache2/ | cookies.sqlite | extensions/ |
| Edge | `%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\` | History (SQLite) | History (downloads table) | Cache/ | Cookies (SQLite) | Extensions/ |
| Safari | `~/Library/Safari/` | History.db | Downloads.plist | ~/Library/Caches/com.apple.Safari/ | Cookies.binarycookies | Extensions/ |

- Tools: Hindsight (Chrome), KAPE with browser module, DB Browser for SQLite, Autopsy browser module
- Extract: URL history with timestamps, download history with source URL and save path, search terms, bookmarks, autofill data, saved passwords (encrypted), extension list with permissions
- **IndexedDB:** Modern web applications store data in IndexedDB — check for webmail, cloud storage, and messaging app data

**Email Client Artifacts:**
- Outlook: PST/OST files (`%LOCALAPPDATA%\Microsoft\Outlook\`) — full email, calendar, contacts
- Thunderbird: mbox format in profile directory
- Tools: Kernel PST Viewer, pst-utils, Autopsy email module

**Messaging & Collaboration:**
- Microsoft Teams: `%APPDATA%\Microsoft\Teams\` — IndexedDB, local storage, cached files
- Slack: `%APPDATA%\Slack\` — IndexedDB with message history
- Discord: `%APPDATA%\discord\` — local storage, cache

**Remote Access Tools:**
- RDP: Bitmap cache (`%LOCALAPPDATA%\Microsoft\Terminal Server Client\Cache\`) — reconstruct screen images from RDP sessions
- TeamViewer: `%APPDATA%\TeamViewer\` — connection logs with timestamps, partner IDs, connection duration
- AnyDesk: `%APPDATA%\AnyDesk\` — connection traces, ad.trace log file

**Cloud Sync Clients:**
- OneDrive: `%LOCALAPPDATA%\Microsoft\OneDrive\` — sync logs, file metadata
- Dropbox: `%APPDATA%\Dropbox\` — sync database, file cache
- Google Drive: `%LOCALAPPDATA%\Google\DriveFS\` — content cache, metadata

### 5. Anti-Forensics Detection

Actively look for evidence of anti-forensic techniques:

**Timestamp Manipulation (Timestomping):**
- Compare $STANDARD_INFORMATION timestamps with $FILENAME timestamps in $MFT
  - $SI is modifiable by user-space tools (SetFileTime API, timestomp.exe, PowerShell)
  - $FN is set by the kernel and not modifiable by standard user-space tools
  - If $SI creation time is BEFORE $FN creation time → timestomping detected
  - If $SI timestamps are suspiciously round (00:00:00) or match system dates → suspicious
- Tools: MFTECmd with timestamp comparison, Autopsy timeline module
- Present timestomping detections:

```
| # | File Path | $SI Created | $FN Created | $SI Modified | $FN Modified | Discrepancy | EVD ID |
|---|-----------|-------------|-------------|--------------|--------------|-------------|--------|
| 1 | {{path}} | {{si_created}} | {{fn_created}} | {{si_modified}} | {{fn_modified}} | {{description}} | EVD-{case_id}-XXX |
```

**Secure Deletion Evidence:**
- Artifacts of secure deletion tools: Eraser, sdelete (Sysinternals), shred, srm, BleachBit
  - Prefetch entries for deletion tools
  - USN Journal entries showing file deletion patterns (rapid sequential deletion of many files)
  - Registry entries for deletion tool installation/configuration
- Large gaps in $MFT sequence numbers (bulk deletion)
- Overwritten file slack containing non-random data patterns (zero-fill, random-fill signatures)

**Log Clearing:**
- Event Log clearing evidence:
  - Event ID 1102 (Security log cleared) — ironically, this event is logged AFTER the clear
  - Event ID 104 (System log cleared)
  - Gaps in Event Log sequence numbers
  - Event Log files with recent creation dates but no historical events
- Journal vacuuming (Linux): `journalctl --vacuum-time` evidence
- Syslog gaps or truncation

**Data Hiding:**
- Encrypted containers: TrueCrypt/VeraCrypt volumes (check for container files, mounted volume artifacts)
- Hidden partitions: analyze partition table for gaps, HPA (Host Protected Area), DCO (Device Configuration Overlay)
- Steganography: statistical analysis on image files for embedded data (tools: StegDetect, zsteg)
- Hidden ADS (Alternate Data Streams) on NTFS

**Anti-Forensics Summary:**

```
| # | Technique | Evidence Found | Affected Files/Systems | Impact on Investigation | EVD ID | Confidence |
|---|-----------|----------------|------------------------|------------------------|--------|------------|
| 1 | {{technique}} | {{evidence}} | {{files/systems}} | {{impact}} | EVD-{case_id}-XXX | Confirmed/Probable/Possible |
```

### 6. Disk Forensics Findings Summary

Consolidate all disk forensic findings into a structured summary:

**Findings Table:**

```
| # | Finding | Category | Artifact Source | File Path | Timestamp | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|----------|-----------------|-----------|-----------|--------|----------|-------------------|------------|
| 1 | {{finding}} | OS/App/FS/AntiForensics | {{source}} | {{path}} | {{timestamp}} | EVD-{case_id}-XXX | Critical/High/Medium/Low/Info | {{T-code}} | Confirmed/Probable/Possible |
```

**Disk Forensics Statistics:**
```
Total artifacts examined: {{count}}
Artifacts with forensic significance: {{count}}
Deleted files recovered: {{count}}
File signature mismatches detected: {{count}}
Anti-forensics indicators detected: {{count}}
Timestomping instances detected: {{count}}
Unique executables identified: {{count}}
Persistence mechanisms (disk-based): {{count}}
IOCs extracted from disk analysis: {{count}}
```

### 7. Append Findings to Report

Write all disk forensic findings under `## Disk Forensics` in the output file `{outputFile}`:

```markdown
## Disk Forensics

### File System Analysis
{{file_system_identification_and_partition_analysis}}
{{file_signature_analysis_results}}
{{deleted_file_recovery_results}}

### Operating System Artifacts
{{windows_or_linux_or_macos_artifact_analysis}}
{{execution_artifacts_summary}}
{{registry_analysis_summary}}

### Application Artifacts
{{browser_forensics_results}}
{{email_and_messaging_results}}
{{remote_access_and_cloud_sync_results}}

### Anti-Forensics Detection
{{timestomping_detection_results}}
{{secure_deletion_evidence}}
{{log_clearing_evidence}}
{{data_hiding_detection}}

### Disk Forensics Findings Summary
{{consolidated_findings_table}}
{{statistics}}
```

Update frontmatter:
- Add this step name (`Disk Forensic Analysis`) to the end of `stepsCompleted`
- Set `analysis_types.disk_forensics` to `true`
- Update `artifacts_recovered` with the count of artifacts with forensic significance
- Update `anti_forensics_detected` to `true` if any anti-forensics indicators were found
- Update `findings_count` and `findings_by_severity` with disk forensic findings
- Update `iocs_extracted` with IOCs found during disk analysis
- Update `mitre_techniques` with ATT&CK techniques identified from disk artifacts

### 8. Present MENU OPTIONS

"**Disk forensic analysis complete.**

Evidence items analyzed: {{analyzed_count}}
Artifacts with forensic significance: {{significant_count}}
Deleted files recovered: {{deleted_count}}
Anti-forensics indicators: {{anti_forensics_count}}
Timestomping detected: {{timestomping_count}} instances
Persistence mechanisms found: {{persistence_count}}
IOCs extracted: {{ioc_count}}
ATT&CK techniques mapped: {{technique_count}}

**Select an option:**
[A] Advanced Elicitation — Challenge disk forensic findings, identify artifacts that should have been present but were not found, assess whether anti-forensics may have obscured additional evidence
[W] War Room — Red (what artifacts did I leave that the analyst found? what did I successfully destroy? what hiding techniques would defeat this analysis?) vs Blue (are there disk artifacts we have not examined that are relevant to the forensic question? did we detect all anti-forensic activity? what would a second examiner find that we missed?)
[C] Continue — Proceed to Step 4: Memory Forensic Analysis (Step 4 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the disk forensic analysis. Were all relevant artifacts examined for the forensic question? Are there OS artifacts that should contain entries but do not (indicating deletion or tampering)? Are the anti-forensics detections complete, or could more sophisticated techniques have evaded detection? Are there file system artifacts in unallocated space that have not been carved? Is the execution artifact evidence consistent with the user activity timeline? Process insights, ask user if they want to expand analysis, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: the analyst found my tools via Prefetch and Amcache — but did they check SRUM for my network usage? Did they find my encrypted container in the hidden partition? Did my timestomping survive the $SI vs $FN comparison? Did they check Shellbags for the directories I browsed? Blue Team perspective: is our artifact coverage complete for the OS on this system? Are there forensic artifacts we did not extract that could provide additional evidence? Are the timestamps consistent across artifact sources? Could the attacker have planted false artifacts? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated with analysis_types.disk_forensics, artifacts_recovered, findings counts, and this step added to stepsCompleted. Then read fully and follow: ./step-04-memory-forensics.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, analysis_types.disk_forensics set to true, artifacts_recovered updated, findings counts updated, and Disk Forensics section fully populated in the output document], will you then read fully and follow: `./step-04-memory-forensics.md` to begin memory forensic analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Working copy integrity verified before analysis began (hash match confirmed)
- File system identified and partition structure analyzed for each disk image
- $MFT parsed for NTFS volumes with full file entry extraction
- OS artifacts extracted per platform (registry, event logs, execution artifacts for Windows; logs, history, journals for Linux; unified logs, FSEvents for macOS)
- Application artifacts examined (browsers, email, messaging, remote access, cloud sync)
- Deleted file recovery attempted via file carving and $MFT deleted entries
- File signature analysis performed (extension vs magic byte comparison)
- Anti-forensics detection performed (timestomping, secure deletion, log clearing, data hiding)
- Every finding cites evidence ID, artifact source, timestamp, and confidence level
- Disk forensics findings summary table presented with severity and ATT&CK mapping
- Frontmatter updated with analysis type, artifact count, findings counts, IOCs, and techniques
- Findings appended to report under `## Disk Forensics`
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Analyzing master evidence instead of working copies
- Not verifying working copy integrity before analysis
- Mounting forensic images with write access
- Not parsing $MFT on NTFS volumes (primary source of file system truth)
- Not checking for timestomping ($SI vs $FN comparison)
- Not examining execution artifacts (Prefetch, Amcache, ShimCache, SRUM)
- Not attempting deleted file recovery when relevant to the forensic question
- Not checking for anti-forensics indicators
- Presenting findings without evidence ID citations
- Not extracting OS artifacts appropriate to the operating system
- Performing memory or network analysis during this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Disk forensics is the backbone of most investigations — file system artifacts are persistent, rich, and often survive attacker cleanup. Every artifact source must be examined. Every finding must be sourced. Anti-forensics detection is not optional — what the attacker hid tells you what matters.
