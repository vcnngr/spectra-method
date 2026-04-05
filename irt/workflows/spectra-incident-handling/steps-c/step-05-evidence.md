# Step 5: Evidence Preservation & Chain of Custody

**Progress: Step 5 of 10** — Next: Deep Analysis & Scope Determination

## STEP GOAL:

Establish a forensically sound evidence collection process with documented chain of custody for all digital evidence, ensuring admissibility in legal proceedings and regulatory compliance. Every piece of evidence must be acquired with integrity, hashed at collection, documented with custody records, and stored securely.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify, overwrite, or delete original evidence — all evidence operations are acquisition-only
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous forensic tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator ensuring forensic integrity of all digital evidence under NIST 800-61
- ✅ Evidence preservation is what separates professional incident response from ad-hoc firefighting — without proper chain of custody, evidence has no legal standing and investigation findings are challengeable
- ✅ Every evidence item must be treated as if it will be presented in court — because it might be, and you will not get a second chance to collect it properly
- ✅ The order of collection matters — volatile evidence must be collected before non-volatile, and the order of volatility (RFC 3227) must be followed
- ✅ Hash everything, document everything, assume nothing about future use of this evidence

### Step-Specific Rules:

- 🎯 Focus exclusively on evidence collection planning, forensic acquisition, chain of custody documentation, integrity verification, and secure storage
- 🚫 FORBIDDEN to analyze evidence in depth — that is step 6 (Deep Analysis). This step collects and preserves; analysis comes next
- 🚫 FORBIDDEN to modify original evidence in any way — forensic images, not direct access
- 🚫 FORBIDDEN to skip chain of custody documentation for any evidence item, regardless of perceived importance
- 💬 Approach: Systematic collection following order of volatility, with documentation at every stage
- 📊 Every evidence item must include: unique ID, description, source system, collection method, collector identity, timestamp, SHA-256 hash, and storage location
- 🔒 All evidence must be stored in `{irt_evidence_chain}/` with access controls and integrity verification

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Collecting evidence without write-blockers or forensic tools risks modifying the original evidence, rendering it inadmissible — even mounting a disk without write protection changes access timestamps, and these changes are detectable and will be challenged by opposing counsel
  - Not documenting chain of custody for every evidence transfer creates legal exposure and may invalidate the entire evidence set — if you cannot prove who had the evidence, when, and what they did with it, the evidence chain is broken and a competent attorney will exploit that gap
  - Prioritizing disk imaging over memory capture on running systems loses volatile evidence that is irretrievable after power-off or containment — memory contains decryption keys, active malware in its unpacked/decrypted state, network connections, and process trees that do not exist on disk
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present evidence collection plan before beginning any acquisition
- ⚠️ Follow order of volatility strictly — most volatile evidence first
- 📋 Document chain of custody for EVERY evidence item at the moment of collection
- 🔒 Hash EVERY evidence item at the moment of collection (SHA-256 minimum)
- ⚠️ Present [A]/[W]/[C] menu after evidence collection and documentation is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `evidence_items`, `evidence_chain_intact`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, incident classification and severity, affected systems inventory, containment status and actions from step 4, pre-containment evidence captured in step 4, IOC data, MITRE ATT&CK mapping
- Focus: Evidence collection planning, forensic acquisition methodology, chain of custody documentation, integrity verification, and secure storage — no analysis of evidence content
- Limits: Only collect evidence from systems within the engagement scope and authorized by the Rules of Engagement — collection from third-party systems requires separate authorization
- Dependencies: Containment completed in step-04-containment.md, pre-containment volatile evidence captured in step 4

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Evidence Collection Planning

Based on the incident scope, affected systems, and containment status, develop a comprehensive evidence collection plan. The plan must follow the order of volatility from RFC 3227 — the most volatile evidence is collected first because it disappears first.

**Evidence Categories & Priority (Order of Volatility — MOST volatile first):**

**Priority 1 — Volatile Evidence (collected first, exists only in live/running state):**

1. **Registers, Cache** — Almost never captured manually in incident response; captured implicitly in memory dumps. Note for completeness but do not attempt separate capture.

2. **Routing Table, ARP Cache, Process Table, Kernel Statistics:**
   - Routing table: `route print` (Windows), `ip route` (Linux), `netstat -rn` (macOS)
   - ARP cache: `arp -a` (all platforms)
   - Process table: `tasklist /v` (Windows), `ps auxwww` (Linux/macOS)
   - Kernel statistics: `sysinfo` (Windows), `uname -a && cat /proc/meminfo` (Linux)
   - Network statistics: `netstat -anob` (Windows), `ss -tulnp` (Linux)
   - **NOTE:** If these were already captured in step 4 pre-containment evidence capture, verify the captures are intact and do not re-capture unless the system state has changed

3. **Memory Contents (RAM Dump):**
   - Windows: WinPMEM, DumpIt, Belkasoft RAM Capturer, FTK Imager (memory capture mode)
   - Linux: LiME (Linux Memory Extractor) — kernel module for live acquisition
   - macOS: osxpmem (requires SIP disable or kext approval)
   - Cloud VMs: API-based memory snapshot (AWS: create forensic AMI; Azure: disk snapshot; GCP: machine image)
   - **CRITICAL:** Write memory dump to external media or network share — NEVER to the evidence system itself (this overwrites evidence)
   - **CRITICAL:** Hash the memory dump immediately after capture — file size should match system RAM
   - **NOTE:** If memory was already captured in step 4 pre-containment, verify the existing capture. Only re-capture if the system has been running since containment and new memory contents may be relevant

4. **Temporary File Systems:**
   - Windows: `%TEMP%`, `%TMP%`, `C:\Windows\Temp`, `AppData\Local\Temp`
   - Linux: `/tmp`, `/var/tmp`, swap partitions
   - macOS: `/tmp`, `/private/var/folders/`
   - Browser caches and session storage
   - Application temporary files (Office recovery, download caches)

5. **Disk Data (captured as forensic image — see instruction 2):**
   - Full disk image, not logical file copy
   - Includes unallocated space, file slack, deleted files
   - This bridges volatile and non-volatile — disk is persistent but may be modified by continued operation

**Priority 2 — Semi-Volatile Evidence (persists but may be overwritten or rotated):**

6. **Remote Logging and Monitoring Data:**
   - SIEM: export all relevant logs for the incident time window with buffer (incident window ± 72 hours minimum)
   - Syslog: centralized syslog server exports
   - EDR telemetry: full event history for affected endpoints
   - Network monitoring: NetFlow/IPFIX, DNS query logs, proxy logs, firewall logs
   - Cloud logs: AWS CloudTrail, Azure Activity Log, Azure AD Sign-in logs, GCP Audit Log, GCP Cloud Logging
   - Email logs: mail transport logs, message tracking, DLP alerts
   - Authentication logs: Windows Security Event Log (logon events 4624/4625/4648/4672), Kerberos ticket events, RADIUS/TACACS, SSO/SAML assertion logs
   - **CRITICAL:** Verify log retention — some logs are rotated on short cycles (24-72 hours). Export before they expire.
   - **CRITICAL:** Export raw logs, not just filtered views — analysis may require events not matching current IOCs

7. **Physical Configuration, Network Topology:**
   - Network device configurations (switch, router, firewall — running config and startup config)
   - VLAN configuration and port assignments
   - DNS zone files
   - DHCP lease tables
   - Load balancer and reverse proxy configurations
   - SDN/cloud network security group rules

**Priority 3 — Non-Volatile Evidence (persistent, stable, collected after volatile):**

8. **Archival Media:**
   - Backup tapes or snapshots from before the incident (for comparison with current state)
   - Previous forensic images from related incidents
   - Archived logs beyond the active retention window
   - Historical configuration backups

**Present as evidence collection matrix:**

```
| # | Evidence Type | Priority | Source System(s) | Collection Method | Tool | Assigned Collector | Estimated Size | Status |
|---|---------------|----------|------------------|-------------------|------|-------------------|----------------|--------|
| 1 | {{type}} | P1/P2/P3 | {{system}} | {{method}} | {{tool}} | {{collector}} | {{size}} | Pending/Captured/Failed/N-A |
```

**Collection Scope Decision:**
- Present the collection plan and ask the operator to confirm scope — not every evidence type is needed for every incident
- For lower-severity incidents: prioritize memory, disk images, and logs directly related to the attack path
- For higher-severity incidents (regulatory, legal, suspected data breach): collect comprehensively across all priority levels
- For any evidence type marked N/A: document why it was excluded (not relevant, not accessible, already captured, out of scope)

### 2. Forensic Acquisition Methodology

For each evidence type in the collection plan, define the specific acquisition methodology. The methodology must ensure forensic soundness — the original evidence is never modified, and the acquisition process is documented and reproducible.

**Memory Acquisition:**

**Procedure:**
1. Prepare external storage media (USB drive, network share) — format and verify empty before use
2. Select acquisition tool based on target OS:
   - Windows: WinPMEM (open-source, kernel driver), DumpIt (commandline, single executable), FTK Imager (GUI, CLI available)
   - Linux: LiME (kernel module — `insmod lime.ko "path=/mnt/evidence/mem.lime format=lime"`)
   - macOS: osxpmem (requires System Integrity Protection configuration)
   - VMware: `.vmem` file or snapshot memory from hypervisor level
   - Hyper-V: checkpoint with memory export
3. Execute capture — output to external media, NOT to the evidence system
4. Record: tool name, tool version, tool hash (verify the tool itself is clean), start time, end time
5. Calculate SHA-256 hash of the memory dump immediately after capture
6. Verify file size: compare to system RAM size (should match or be slightly larger due to metadata)
7. Copy the memory dump to a second location for redundancy
8. Hash the second copy and verify it matches the first

**Disk Imaging:**

**Procedure:**
1. If possible, power down the system and remove the disk for imaging — eliminates any risk of write operations
2. If live imaging is required (system cannot be powered down): use a forensic imaging tool that operates in read-only mode
3. **Write-blocker is MANDATORY for physical disk access** — hardware write-blocker preferred (Tableau, CRU), software write-blocker acceptable if hardware is unavailable
4. Select imaging tool:
   - FTK Imager: E01 format (Expert Witness, compressed, with embedded hashes), or raw/dd format
   - dc3dd: enhanced dd with built-in hashing and progress indication
   - ewfacquire: EWF/E01 format with compression and hash verification
   - dd: raw format — use `if=/dev/sdX of=/path/to/image.dd bs=64K conv=noerror,sync status=progress`
5. Image format selection:
   - E01 (Expert Witness): recommended — compressed, includes embedded hash, supports case metadata
   - AFF4: modern forensic format, supports compression and encryption
   - Raw (dd): universal compatibility, no compression, largest file size
6. Calculate source disk hash BEFORE imaging (if accessible via write-blocker)
7. Execute imaging — record start time, tool, parameters
8. Calculate image hash after imaging completes
9. Verify: source hash == image hash (bit-for-bit identical)
10. If hash mismatch: re-image. If persistent mismatch: document the discrepancy with potential causes (bad sectors, hardware failure) and note affected regions
11. Create a second copy of the forensic image for working analysis (never analyze the master copy)

**Log Collection:**

**Procedure:**
1. Define the time window: incident start (earliest known attacker activity) minus 72 hours through current time
2. Export in native format where possible (EVTX for Windows Event Logs, raw syslog, JSON for cloud logs)
3. Also export in a universal format for cross-source analysis (CSV, JSON-lines)
4. For SIEM exports: export both raw events and any correlation/aggregation data
5. For cloud logs: use the provider's API for bulk export — console downloads may be truncated
   - AWS: `aws cloudtrail lookup-events` or S3 bucket export
   - Azure: `az monitor activity-log list` or Log Analytics export
   - GCP: `gcloud logging read` or BigQuery export
6. Hash every log export file after collection
7. Document: source system, time window, export method, file format, record count, file size, hash
8. If logs are not available (already rotated, not enabled, retention expired): document the gap and the impact on the investigation

**Network Capture:**

**Procedure:**
1. Full packet capture (PCAP): if a network TAP or SPAN is available, capture all traffic on the affected network segment
2. Historical PCAP: check if NSM (Network Security Monitoring) tools have stored packet captures from the incident window
3. NetFlow/IPFIX: export flow data for the incident time window from routers, switches, and firewalls
4. DNS query logs: export from DNS servers or DNS security tools (Infoblox, Pi-hole, Umbrella)
5. Proxy/web filter logs: export from web proxy or secure web gateway
6. Hash all capture files after collection
7. Document: capture point (which network segment), time window, file format, file size, hash

### 3. Chain of Custody Documentation

For EVERY piece of evidence collected, create a chain of custody record. This is not optional. This is not a formality. This is the legal foundation that makes the evidence admissible.

**Evidence ID Convention:**
- Format: `EVD-{incident_id}-{sequential_number}`
- Example: `EVD-INC-2026-0042-001`, `EVD-INC-2026-0042-002`
- Sequential numbers assigned in collection order
- Once assigned, an evidence ID is permanent — never reuse or reassign

**Chain of Custody Record — per evidence item:**

```
| Field | Value |
|-------|-------|
| Evidence ID | EVD-{incident_id}-{seq} |
| Description | {{what it is and what it contains}} |
| Relevance | {{why it was collected — what incident aspect it relates to}} |
| Source System | Hostname: {{hostname}}, IP: {{ip}}, Serial: {{serial}}, Asset Tag: {{tag}} |
| Source Location | {{file path, disk, memory, network segment}} |
| Collection Method | {{tool used, parameters, procedure followed}} |
| Collection Tool | {{tool name, version, hash of the tool binary}} |
| Collector | {{name, role, contact}} |
| Collection Timestamp | {{UTC timestamp — start and end of acquisition}} |
| Integrity Hash (SHA-256) | {{hash computed at collection}} |
| File Size | {{bytes}} |
| File Format | {{E01, raw, EVTX, PCAP, CSV, etc.}} |
| Storage Location | {{path within {irt_evidence_chain}/}} |
| Access Control | {{who has access to this evidence}} |
| Notes | {{any anomalies, deviations from procedure, or special handling requirements}} |
```

**Chain of Custody Transfer Log — per evidence item:**

Every time evidence changes hands (physically or logically), a transfer record is created:

```
| Transfer # | Date/Time (UTC) | Released By | Received By | Purpose | Location Before | Location After | Hash Verified |
|------------|-----------------|-------------|-------------|---------|-----------------|----------------|---------------|
| 1 | {{timestamp}} | {{name, role}} | {{name, role}} | {{purpose}} | {{from}} | {{to}} | {{Yes — hash matches / No — ALERT}} |
```

**Present the master chain of custody table:**

```
| Evidence ID | Description | Source | Collector | Timestamp | SHA-256 | Size | Format | Storage | CoC Status |
|-------------|-------------|--------|-----------|-----------|---------|------|--------|---------|------------|
| EVD-{id}-001 | {{desc}} | {{source}} | {{collector}} | {{time}} | {{hash}} | {{size}} | {{format}} | {{path}} | {{Intact/Broken}} |
```

### 4. Evidence Integrity Verification

After all evidence is collected and documented, verify the integrity of every evidence item. This is the final gate before evidence is stored and the investigation proceeds to analysis.

**Integrity Verification Procedure:**

1. **Re-hash every evidence item** at its storage location
2. **Compare the storage hash to the collection hash** — they MUST match
3. **If hash matches:** mark as verified, record verification timestamp and verifier
4. **If hash mismatch:** ALERT — evidence may have been modified or corrupted
   - Do NOT discard the evidence — it may still have investigative value even if legally compromised
   - Document: which evidence, expected hash vs actual hash, when the discrepancy was discovered, potential causes
   - Assess impact: does this invalidate the evidence for legal proceedings? Does it affect investigative conclusions?
   - Attempt to determine cause: storage media error, transfer corruption, unintended modification
   - If possible: re-acquire from source (if source is still available and unchanged)

**Hash Integrity Log:**

```
| Evidence ID | Collection Hash (SHA-256) | Verification Hash (SHA-256) | Match | Verified By | Verification Time | Notes |
|-------------|--------------------------|----------------------------|-------|-------------|-------------------|-------|
| EVD-{id}-001 | {{hash}} | {{hash}} | {{Yes/NO — ALERT}} | {{verifier}} | {{timestamp}} | {{notes}} |
```

**For high-profile cases (regulatory investigation, legal proceedings, law enforcement involvement):**
- Consider implementing a hash chain: each evidence item's hash includes the previous item's hash, creating a tamper-evident sequence
- Consider using a trusted timestamp authority (TSA) to cryptographically prove when evidence was collected
- Consider creating a notarized evidence manifest signed by the lead investigator

### 5. Evidence Storage & Security

All evidence must be stored securely with access controls, encryption, and audit logging.

**Storage Location:** `{irt_evidence_chain}/` directory structure:

```
{irt_evidence_chain}/
  manifest.md                    — Master evidence inventory with hashes
  integrity-log.md               — Hash verification log with timestamps
  chain-of-custody/
    EVD-{id}-001-coc.md          — Chain of custody for each evidence item
    EVD-{id}-002-coc.md
  memory/
    EVD-{id}-001-hostname.lime   — Memory dumps
  disk-images/
    EVD-{id}-002-hostname.E01    — Forensic disk images
  logs/
    EVD-{id}-003-siem-export.json — Log exports
    EVD-{id}-004-cloudtrail.json
  network/
    EVD-{id}-005-capture.pcap    — Network captures
  volatile/
    EVD-{id}-006-processes.txt   — Volatile data captures from pre-containment
    EVD-{id}-007-connections.txt
```

**Storage Security Requirements:**
- Encryption at rest: all evidence storage must be encrypted (full-disk encryption or encrypted container)
- Access control: restrict access to authorized incident response personnel only
- Access logging: every access to evidence storage must be logged (who, when, what, purpose)
- Physical security: if evidence is on physical media (USB, hard drive), store in a locked, access-controlled location
- No modification: evidence storage is append-only — new evidence can be added, existing evidence is never modified or deleted

**Backup Requirements:**
- At least one verified copy of every evidence item in a separate storage location
- Backup hash must match the primary hash
- Backup storage must have equivalent access controls
- Document backup locations in the evidence manifest

**Retention Policy:**
- Determine retention period based on:
  - Legal requirements (litigation hold, regulatory mandate, law enforcement request)
  - Organizational policy (standard evidence retention period)
  - Case duration (retain at least until post-incident review is complete and all action items are closed)
- Document the retention decision and the basis for it
- Set a review date for evidence disposal

### 6. Evidence Collection Execution

Execute the evidence collection per the plan from instruction 1, using the methodologies from instruction 2, with chain of custody documentation from instruction 3.

**Execution Sequence:**
- Follow the order of volatility — Priority 1 evidence first, then Priority 2, then Priority 3
- For each evidence item collected:
  1. Execute acquisition using the documented methodology
  2. Hash the evidence immediately after collection
  3. Create the chain of custody record
  4. Transfer to secure storage
  5. Verify hash at storage location
  6. Update the evidence manifest

**Document any deviations from the plan:**
- Evidence that could not be collected: what, why, and the impact on the investigation
- Evidence collection that deviated from the planned methodology: what changed and why
- Evidence contamination events: any accidental modification of evidence, with assessment of impact
- Additional evidence discovered during collection: items not in the original plan that were identified during acquisition

**Present final evidence inventory:**

```
| # | Evidence ID | Description | Source | Priority | Method | Collector | Hash (SHA-256) | Size | Status |
|---|-------------|-------------|--------|----------|--------|-----------|----------------|------|--------|
| 1 | EVD-{id}-001 | {{desc}} | {{source}} | P1/P2/P3 | {{method}} | {{collector}} | {{hash}} | {{size}} | Collected/Failed/N-A |
```

**Evidence Collection Summary:**
```
Total evidence items planned: {{planned_count}}
Total evidence items collected: {{collected_count}}
Total evidence items failed: {{failed_count}} — {{reasons}}
Total evidence items N/A: {{na_count}} — {{reasons}}
Total evidence size: {{total_size}}
Chain of custody intact: {{Yes / No — detail}}
All hashes verified: {{Yes / No — detail}}
```

### 7. Append Findings to Report

Write all evidence preservation findings under `## Evidence Preservation` in the output file `{outputFile}`:

```markdown
## Evidence Preservation

### Evidence Collection Plan
{{evidence_collection_matrix_from_instruction_1}}

### Evidence Inventory
{{final_evidence_inventory_from_instruction_6}}

### Chain of Custody Log
{{master_chain_of_custody_table_from_instruction_3}}

### Hash Verification
{{hash_integrity_log_from_instruction_4}}

### Evidence Storage & Handling
{{storage_location_and_security_details_from_instruction_5}}

### Forensic Image Status
{{disk_imaging_details_and_verification}}
```

Update frontmatter:
- Add this step name (`Evidence Preservation & Chain of Custody`) to the end of the `stepsCompleted` array
- Set `evidence_items` to the total number of evidence items collected
- Set `evidence_chain_intact` to `true` if all hashes verified and no chain of custody breaks, `false` otherwise (with explanation in the notes)

### 8. Present MENU OPTIONS

"**Evidence preservation and chain of custody documentation complete.**

Evidence items collected: {{collected_count}} / {{planned_count}} planned
Evidence failed/unavailable: {{failed_count}}
Total evidence size: {{total_size}}
Chain of custody: {{intact / broken — detail}}
Hash verification: {{all passed / {{failed_count}} failures}}
Storage: `{irt_evidence_chain}/`
Volatile evidence: {{captured / partial / not captured}}
Forensic images: {{count}} created and verified

**Select an option:**
[A] Advanced Elicitation — Challenge evidence completeness and identify collection gaps
[W] War Room — Red (what evidence did the attacker destroy or tamper with before we got to it?) vs Blue (is our evidence set sufficient for root cause analysis and legal proceedings?)
[C] Continue — Proceed to Step 6: Deep Analysis & Scope Determination"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the evidence collection. Is the evidence set sufficient to reconstruct the full attack timeline? Are there systems that should have been imaged but were not? Are there log sources that are missing or have gaps? Could the attacker have tampered with any evidence before collection? Is the chain of custody robust enough for legal proceedings? What additional evidence would strengthen the investigation? Process insights, ask user if they want to collect additional evidence, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: before the defenders collected evidence, what did I have time to destroy? Did I clear event logs? Did I timestomp my malware? Did I corrupt the MFT? Did I plant false evidence to misdirect the investigation? Are there systems where I operated that the defenders have not collected evidence from? Blue Team perspective: do we trust the evidence we collected? Have we verified that logs were not tampered with? Do we have corroborating evidence from independent sources for critical events? Is our evidence chain legally defensible? What would a forensic examiner challenge in our methodology? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated with evidence_items, evidence_chain_intact, and this step added to stepsCompleted. Then read fully and follow: ./step-06-deep-analysis.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, evidence_items set to the collected count, evidence_chain_intact set correctly, and Evidence Preservation section fully populated in the output document], will you then read fully and follow: `./step-06-deep-analysis.md` to begin deep analysis and scope determination.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Evidence collection plan developed following order of volatility (RFC 3227) with priority, source, method, tool, and assigned collector for each item
- Forensic acquisition methodology defined per evidence type (memory, disk, logs, network) with tool, procedure, and verification steps
- Memory acquisition completed with hash verification and size sanity check
- Disk imaging completed with write-blocker and bit-for-bit hash verification (source hash == image hash)
- Log collection completed with defined time window, native format export, and hash at collection
- Chain of custody record created for EVERY evidence item with all required fields (ID, description, source, method, collector, timestamp, hash, storage)
- Every evidence item hashed at collection (SHA-256) and re-hashed at storage with documented match
- Hash integrity log complete with verification timestamp and verifier identity
- Evidence stored securely in `{irt_evidence_chain}/` with access controls and encryption
- Any failed or unavailable evidence documented with reason and investigation impact
- Evidence collection summary presented with counts, sizes, and status
- Frontmatter updated with evidence_items count and evidence_chain_intact status
- Findings appended to report under `## Evidence Preservation`
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Collecting evidence without documenting chain of custody for every item
- Not hashing evidence at the point of collection
- Writing memory dumps to the evidence system itself (destroys evidence by overwriting)
- Imaging disks without write-blockers (modifies original evidence)
- Not following order of volatility (capturing disk before memory on a live system)
- Analyzing evidence content during this step (analysis belongs to step 6)
- Modifying, overwriting, or deleting any original evidence
- Not documenting evidence that could not be collected (gaps must be recorded)
- Storing evidence without access controls or encryption
- Declaring chain of custody intact when any hash verification failed
- Not creating a second copy of critical evidence (forensic images, memory dumps)
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Evidence preservation is the legal foundation of the entire incident response — every item hashed, every transfer documented, every gap recorded. There is no second chance to collect evidence that has been modified, overwritten, or lost. Forensic integrity is non-negotiable.
