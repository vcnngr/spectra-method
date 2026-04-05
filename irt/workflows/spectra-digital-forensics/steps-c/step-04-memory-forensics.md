# Step 4: Memory Forensic Analysis

**Progress: Step 4 of 10** — Next: Network Forensic Analysis

## STEP GOAL:

Conduct comprehensive memory forensic analysis on acquired memory dumps — process enumeration and anomaly detection, code injection and hollowing identification, network connection reconstruction, credential extraction, kernel integrity verification, and YARA-based malware scanning. Memory forensics reveals the runtime state of the system at the moment of capture — active malware in its unpacked/decrypted state, network connections that no longer exist on disk, and injected code that never touched the file system.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER access or modify master evidence — analyze ONLY working copies of memory dumps
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous analysis engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst conducting structured memory forensic examination under ISO 27037 and NIST SP 800-86
- ✅ Memory is the only place where you can observe malware in its true form — on disk it is encrypted, packed, or obfuscated; in memory it is running, decoded, and exposed
- ✅ Process analysis is not just listing processes — it is comparing multiple enumeration methods to detect hiding techniques (pslist vs psscan vs pstree discrepancies reveal rootkits)
- ✅ Network connections from memory reveal C2 that has already been terminated — forensic gold that exists nowhere else
- ✅ Memory analysis requires the correct OS profile — an incorrect profile produces garbage output, not wrong answers

### Step-Specific Rules:

- 🎯 Focus exclusively on memory forensic analysis: process analysis, code injection detection, network reconstruction from memory, credential extraction, kernel analysis, and YARA scanning
- 🚫 FORBIDDEN to perform disk analysis — that was step 3
- 🚫 FORBIDDEN to perform network packet analysis — that is step 5
- 🚫 FORBIDDEN to modify memory dump working copies
- 💬 Approach: Systematic memory analysis using Volatility 3 (or equivalent) framework, with cross-reference to disk findings from step 3
- 📊 Every finding must cite: evidence ID (EVD-{case_id}-{NNN}), memory artifact source, process/address context, and confidence level
- 🔒 Re-verify working copy hash before analysis begins

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Skipping process comparison analysis (pslist vs psscan vs pstree) and relying on a single enumeration method means rootkits and hidden processes will not be detected — a sophisticated attacker using DKOM (Direct Kernel Object Manipulation) unlinks processes from the active process list, making them invisible to pslist but detectable by psscan which scans pool tags
  - Not running YARA scans across all process memory spaces misses malware that exists only in memory and never touches disk — fileless malware, reflectively loaded DLLs, and process-injected shellcode only exist in the memory address space of the host process and will not be found by disk analysis alone
  - Extracting credentials from memory (LSASS dump analysis) without documenting the legal authority and scope of credential analysis could create issues for litigation support or HR investigation cases — credential extraction is a powerful forensic technique but must be authorized and scoped appropriately
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Verify working copy integrity before beginning analysis
- ⚠️ Identify the correct OS profile before any Volatility analysis
- 📋 Document every Volatility plugin used with version and parameters
- 🔒 Cite evidence IDs for every finding
- ⚠️ Present [A]/[W]/[C] menu after memory forensic analysis is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of stepsCompleted and updating analysis_types, findings counts
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Case intake, forensic question, evidence inventory, acquisition records, disk forensics findings from step 3
- Focus: Memory forensic analysis — process analysis, injection detection, network from memory, credentials, kernel, YARA
- Limits: If memory evidence was classified as N/A in step 2, document the N/A status and proceed to step 5. Only analyze working copies.
- Dependencies: Evidence acquired in step 2, disk forensics findings from step 3 (for cross-reference)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check & Working Copy Verification

**If memory evidence was classified as N/A in step 2:**

"**Memory Forensics — Not Applicable**

No memory dumps or hibernation files were acquired for this case. Reason: {{reason_from_step_2}}.

This step is documented as N/A. Memory-specific artifacts (running processes, injected code, active network connections, in-memory credentials) cannot be analyzed. The investigation will rely on disk, network, and cloud evidence."

Document the N/A status in the report and proceed directly to the menu (instruction 9) with only the C option to advance.

**If memory evidence is available:**

Re-verify working copy integrity:

```
| EVD ID | Evidence Type | Working Copy Path | Master Hash (SHA-256) | Current Hash (SHA-256) | Match | Analyst | Verification Time |
|--------|---------------|-------------------|----------------------|------------------------|-------|---------|-------------------|
| EVD-{case_id}-XXX | Memory Dump | {{path}} | {{master_hash}} | {{current_hash}} | ✅/❌ | {{analyst}} | {{UTC timestamp}} |
```

### 2. Profile Identification

Before any Volatility analysis, identify the correct OS profile for the memory dump:

**Volatility 3 Profile Detection:**
- Volatility 3 uses ISF (Intermediate Symbol Format) files and auto-detects OS via `windows.info` / `linux.info` / `mac.info`
- Run: `vol3 -f memory.dump windows.info` (or linux.info / mac.info)
- If auto-detection fails: manually identify OS from disk forensics findings (step 3) and provide the correct symbol table

**Profile Information:**

```
| Field | Value |
|-------|-------|
| Memory Dump | EVD-{case_id}-XXX |
| Dump Format | {{raw/lime/elf/crash}} |
| Dump Size | {{bytes}} |
| Operating System | {{Windows 10 21H2 / Ubuntu 22.04 / macOS 13.0}} |
| Kernel Version | {{version}} |
| Architecture | {{x64/x86/ARM64}} |
| Symbol Table | {{ISF file or profile name}} |
| Build/Revision | {{build number}} |
| Profile Confidence | {{High — auto-detected / Medium — manual identification / Low — best guess}} |
```

### 3. Process Analysis

Enumerate processes using multiple methods to detect hidden/unlinked processes:

**Process Listing Comparison:**

Run three enumeration methods and compare results:

1. **pslist (linked list traversal):** Walks the `_EPROCESS` doubly-linked list from `PsActiveProcessHead`
   - `vol3 -f memory.dump windows.pslist`
   - Shows: PID, PPID, name, offset, threads, handles, session, start time
   - Limitation: DKOM can unlink processes from this list

2. **psscan (pool tag scanning):** Scans all memory for `_EPROCESS` pool tags regardless of list membership
   - `vol3 -f memory.dump windows.psscan`
   - Shows: PID, PPID, name, offset, time created, time exited
   - Advantage: Finds terminated processes AND processes hidden from pslist via DKOM

3. **pstree (parent-child hierarchy):** Displays process tree structure
   - `vol3 -f memory.dump windows.pstree`
   - Shows: hierarchical view with parent-child relationships
   - Advantage: Reveals unusual parentage (e.g., cmd.exe spawned by svchost.exe)

**Cross-Reference Analysis:**

```
| PID | Process Name | In pslist | In psscan | In pstree | Parent PID | Parent Name | Anomaly |
|-----|-------------|-----------|-----------|-----------|------------|-------------|---------|
| {{pid}} | {{name}} | ✅/❌ | ✅/❌ | ✅/❌ | {{ppid}} | {{parent}} | {{anomaly or 'None'}} |
```

**Anomaly Detection Criteria:**
- Process in psscan but NOT in pslist → hidden process (DKOM)
- Unusual parent-child relationships:
  - svchost.exe not spawned by services.exe → suspicious
  - cmd.exe or powershell.exe spawned by unusual parent (IIS, Office app, browser) → potential exploitation
  - lsass.exe not spawned by wininit.exe → suspicious
  - Multiple instances of processes that should be singleton (lsass.exe, csrss.exe, smss.exe)
- Processes with misspelled names: svchost.exe vs svch0st.exe, csrss.exe vs cssrs.exe
- Processes running from unusual paths: legitimate system processes should run from `C:\Windows\System32\`
- Processes with no associated user or session
- Terminated processes with recent exit times (attacker cleanup)

**Command Line Analysis:**
- `vol3 -f memory.dump windows.cmdline`
- Extract command lines for ALL processes
- Flag suspicious command lines:
  - PowerShell with encoded commands (`-enc`, `-e`, `-EncodedCommand`)
  - Download cradles (`IEX`, `Invoke-Expression`, `DownloadString`, `Net.WebClient`)
  - Credential tools (mimikatz, secretsdump, rubeus, SharpHound)
  - Reconnaissance commands (whoami, ipconfig, net group, systeminfo in rapid succession)
  - File transfer utilities (certutil, bitsadmin, curl with unusual destinations)

**Process Environment Variables:**
- `vol3 -f memory.dump windows.envars`
- Check for injected or modified environment variables
- Look for PATH modifications, proxy settings, temporary directory changes

**Handle Analysis:**
- `vol3 -f memory.dump windows.handles`
- For suspicious processes: enumerate files, registry keys, mutexes, events, network ports
- Mutexes are significant: many malware families create unique mutexes for single-instance checks
- File handles reveal what files a process has open (data access, log files, configuration)

### 4. Code Injection Detection

Scan for evidence of code injection, process hollowing, and reflective loading:

**Malfind Analysis:**
- `vol3 -f memory.dump windows.malfind`
- Scans for memory regions with suspicious characteristics:
  - PAGE_EXECUTE_READWRITE permissions (rarely used by legitimate software)
  - Memory regions not backed by any file on disk (MEM_MAPPED without a file)
  - MZ (PE) headers in non-module memory regions (injected executables)
- Per suspicious region: dump the first bytes, identify potential shellcode or PE headers

**Code Injection Techniques to Detect:**

| Technique | Detection Method | Volatility Plugin | Indicator |
|-----------|-----------------|-------------------|-----------|
| Classic DLL Injection | Loaded DLL not on disk, DLL in unusual path | dlllist + ldrmodules comparison | DLL in ldrmodules but not in InLoadOrderModuleList |
| Reflective DLL Injection | PE in executable memory, not loaded via standard loader | malfind | MZ header in VAD region without file backing |
| Process Hollowing | Legitimate process with replaced code section | malfind, procdump comparison | Process image on disk differs from process image in memory |
| Process Doppelganging | Process created from transacted file | psscan (process exists but image file does not) | No matching file on disk for process image |
| Thread Injection (CreateRemoteThread) | Thread in process not associated with loaded module | threads analysis | Thread start address outside any loaded module range |
| APC Injection | Queued APC pointing to injected code | threads analysis | APC pointing to non-module memory |
| Atom Bombing | Atom table manipulation | atoms plugin | Suspicious atom table entries with shellcode patterns |

**DLL Analysis:**
- `vol3 -f memory.dump windows.dlllist` — List DLLs loaded by each process
- `vol3 -f memory.dump windows.ldrmodules` — Cross-reference three loader lists
  - InLoadOrderModuleList, InMemoryOrderModuleList, InInitializationOrderModuleList
  - DLL in memory but missing from one or more lists → potentially injected/hidden
- Unlinked DLLs: present in memory but removed from loader lists

```
| PID | Process | DLL Path | In Load | In Memory | In Init | On Disk | Anomaly |
|-----|---------|----------|---------|-----------|---------|---------|---------|
| {{pid}} | {{process}} | {{dll_path}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{anomaly}} |
```

### 5. Network Analysis from Memory

Reconstruct network state at the time of memory capture:

**Active Network Connections:**
- `vol3 -f memory.dump windows.netscan` (Windows)
- `vol3 -f memory.dump linux.sockstat` (Linux)

```
| PID | Process | Protocol | Local Address | Local Port | Remote Address | Remote Port | State | Created |
|-----|---------|----------|---------------|------------|----------------|-------------|-------|---------|
| {{pid}} | {{process}} | TCP/UDP | {{local_addr}} | {{local_port}} | {{remote_addr}} | {{remote_port}} | {{state}} | {{timestamp}} |
```

**Anomaly Detection:**
- Connections to known malicious IPs/domains (cross-reference with disk IOCs from step 3)
- Connections on unusual ports (high-numbered ports, non-standard service ports)
- Processes that should not have network connections (notepad.exe, calc.exe, spoolsv.exe with outbound connections)
- Beaconing patterns (regular interval connections to same destination)
- DNS cache from memory: recently resolved domains

**Listening Ports:**
- Identify all listening ports and the processes bound to them
- Flag unexpected listeners (backdoor listeners, reverse shell listeners, proxy SOCKS listeners)

### 6. Credential Extraction

Extract credential material from memory (subject to legal authorization from case intake):

**LSASS Process Analysis:**
- Locate lsass.exe in process list
- Verify LSASS integrity (single instance, correct parent, correct path)
- If LSASS has been accessed by suspicious processes (Event ID 10 in Sysmon, or process handles to LSASS from non-system processes): this is a strong indicator of credential theft

**Credential Types Extractable from Memory:**
- **NTLM hashes:** From LSASS security packages (MSV1_0)
- **Kerberos tickets:** TGTs and TGS tickets from memory
  - Golden ticket indicators: TGT with unusually long lifetime, TGT for krbtgt account
  - Silver ticket indicators: TGS for specific service with anomalous properties
- **Cleartext passwords:** WDigest (if enabled — disabled by default on Windows 8.1+)
- **Cached credentials:** Domain cached credentials (MSCASH/MSCASH2)
- **SSP credentials:** Security Support Provider credentials
- **DPAPI keys:** Data Protection API master keys (used to decrypt user secrets)

**Credential Extraction Methods:**
- Volatility: `vol3 -f memory.dump windows.hashdump` (SAM hashes)
- Volatility: `vol3 -f memory.dump windows.lsadump` (LSA secrets)
- Mimikatz on memory dump: `sekurlsa::minidump`, `sekurlsa::logonpasswords`
- Tools: pypykatz (Python implementation of mimikatz for memory forensics)

**Present credential findings (redact actual values based on case sensitivity):**

```
| # | Account | Domain | Credential Type | Source | Hash/Ticket Present | Anomaly | EVD ID |
|---|---------|--------|-----------------|--------|---------------------|---------|--------|
| 1 | {{account}} | {{domain}} | NTLM/Kerberos/Cleartext/Cached | LSASS/SAM/LSA | Yes/No | {{anomaly}} | EVD-{case_id}-XXX |
```

**Security Note:** Credential extraction results are sensitive. Handle according to the legal context established in step 1. For litigation support cases, document that credentials were extractable but present only hashes, not cleartext values. For HR investigations, credential extraction may be out of scope.

### 7. Kernel Analysis

Analyze kernel integrity to detect rootkits and kernel-level manipulation:

**SSDT (System Service Descriptor Table) Analysis:**
- `vol3 -f memory.dump windows.ssdt`
- Every SSDT entry should point to ntoskrnl.exe or win32k.sys
- Entries pointing to other drivers: potentially hooked by a rootkit
- Present any SSDT anomalies with the hooking driver identified

**Driver Analysis:**
- `vol3 -f memory.dump windows.drvscan`
- `vol3 -f memory.dump windows.modules`
- List all loaded kernel drivers
- Cross-reference with known legitimate drivers
- Flag: unsigned drivers, drivers loaded from temp directories, drivers with recent load times, drivers not present on disk

```
| # | Driver | Path | Base Address | Size | Signed | On Disk | Anomaly | EVD ID |
|---|--------|------|-------------|------|--------|---------|---------|--------|
| 1 | {{driver}} | {{path}} | {{addr}} | {{size}} | ✅/❌/Unknown | ✅/❌ | {{anomaly}} | EVD-{case_id}-XXX |
```

**IRP (I/O Request Packet) Hook Detection:**
- Check major IRP function pointers for each driver
- Hooks redirect I/O operations: file hiding, process hiding, network hiding

**IDT (Interrupt Descriptor Table) Analysis:**
- Check IDT entries for unexpected handlers
- Rootkits may hook interrupts for execution redirection

### 8. YARA Scanning

Scan all process memory spaces with YARA rules for malware detection:

**YARA Rule Sources:**
- Public rule repositories: YARAify, YARA-Rules (GitHub), Malpedia
- Vendor-specific rules: CrowdStrike, Mandiant, Volexity
- Framework-specific signatures:
  - Cobalt Strike beacon signatures
  - Sliver implant signatures
  - Metasploit payload signatures
  - Mythic agent signatures
  - Brute Ratel C4 signatures
- Custom rules: IOC-based rules from this investigation

**Scanning Approach:**
- `vol3 -f memory.dump yarascan.YaraScan --yara-file rules.yar`
- Scan each process memory space individually for targeted detection
- Scan kernel memory for kernel-mode malware
- Scan all memory (process + kernel + unallocated) for comprehensive coverage

**YARA Match Results:**

```
| # | Rule Name | Process (PID) | Memory Address | Match Context | Rule Source | Confidence | EVD ID |
|---|-----------|---------------|----------------|---------------|-------------|------------|--------|
| 1 | {{rule}} | {{process (pid)}} | {{address}} | {{bytes matched}} | {{source}} | High/Medium/Low | EVD-{case_id}-XXX |
```

### 9. Linux Memory Analysis (If Applicable)

If the memory dump is from a Linux system:

**Linux-Specific Analysis:**
- `vol3 -f memory.dump linux.pslist` — Process listing
- `vol3 -f memory.dump linux.bash` — Bash history from memory (survives history file deletion)
- `vol3 -f memory.dump linux.check_afinfo` — Network protocol structure hooks
- `vol3 -f memory.dump linux.check_syscall` — Syscall table hooks (rootkit detection)
- `vol3 -f memory.dump linux.lsmod` — Loaded kernel modules
- `vol3 -f memory.dump linux.check_modules` — Hidden kernel module detection
- `vol3 -f memory.dump linux.tty_check` — TTY structure hooks
- `vol3 -f memory.dump linux.sockstat` — Network connections

**Linux-Specific Anomalies:**
- Hidden kernel modules (loaded but removed from module list)
- Syscall table hooks (redirected system calls)
- LD_PRELOAD injection (shared library preloading for function hooking)
- Rootkit detection: compare loaded modules with modules list, check for hook functions

### 10. Memory Forensics Findings Summary

Consolidate all memory forensic findings:

**Findings Table:**

```
| # | Finding | Category | Memory Artifact | Process/Address | Timestamp | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|----------|-----------------|-----------------|-----------|--------|----------|-------------------|------------|
| 1 | {{finding}} | Process/Injection/Network/Credential/Kernel/YARA | {{artifact}} | {{context}} | {{timestamp}} | EVD-{case_id}-XXX | Critical/High/Medium/Low/Info | {{T-code}} | Confirmed/Probable/Possible |
```

**Memory Forensics Statistics:**
```
Total processes enumerated: {{count}}
Hidden processes detected: {{count}}
Suspicious processes identified: {{count}}
Code injection instances detected: {{count}}
Active network connections: {{count}}
Suspicious network connections: {{count}}
Credentials extracted: {{count}} accounts
Kernel anomalies detected: {{count}}
YARA matches: {{count}}
IOCs extracted from memory analysis: {{count}}
```

### 11. Append Findings to Report

Write all memory forensic findings under `## Memory Forensics` in the output file `{outputFile}`:

```markdown
## Memory Forensics

### Process Analysis
{{process_listing_comparison_and_anomalies}}
{{command_line_analysis}}
{{handle_analysis}}

### Network Connections (from Memory)
{{active_connections_table}}
{{listening_ports}}
{{anomalous_connections}}

### Code Injection Detection
{{malfind_results}}
{{dll_analysis_cross_reference}}
{{injection_technique_detection}}

### Credential Extraction
{{credential_findings_table}}
{{security_notes}}

### Kernel Analysis
{{ssdt_analysis}}
{{driver_analysis}}
{{rootkit_detection_results}}

### YARA Scan Results
{{yara_match_table}}

### Memory Forensics Findings Summary
{{consolidated_findings_table}}
{{statistics}}
```

Update frontmatter:
- Add this step name (`Memory Forensic Analysis`) to the end of `stepsCompleted`
- Set `analysis_types.memory_forensics` to `true`
- Update `findings_count` and `findings_by_severity` with memory forensic findings
- Update `iocs_extracted` with IOCs found during memory analysis
- Update `mitre_techniques` with ATT&CK techniques identified from memory artifacts

### 12. Present MENU OPTIONS

"**Memory forensic analysis complete.**

Evidence items analyzed: {{analyzed_count}}
Processes enumerated: {{process_count}}
Hidden/suspicious processes: {{suspicious_count}}
Code injection instances: {{injection_count}}
Active network connections: {{connection_count}} ({{suspicious_connection_count}} suspicious)
Credentials extracted: {{credential_count}} accounts
Kernel anomalies: {{kernel_anomaly_count}}
YARA matches: {{yara_count}}
IOCs extracted: {{ioc_count}}

**Select an option:**
[A] Advanced Elicitation — Challenge memory analysis completeness, examine process anomalies in more detail, assess whether all injection techniques were detected
[W] War Room — Red (did I use in-memory-only techniques that survived this analysis? was my rootkit detected? did the analyst find my reflective DLL?) vs Blue (are there memory regions we did not scan? could the attacker have used kernel-mode techniques we did not check? is our YARA ruleset comprehensive enough?)
[C] Continue — Proceed to Step 5: Network Forensic Analysis (Step 5 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the memory analysis. Were all processes analyzed with command line inspection? Did the three-way process comparison (pslist/psscan/pstree) reveal any discrepancies? Were all memory regions with executable permissions scanned for injection? Were kernel integrity checks comprehensive? Is the YARA ruleset adequate for the suspected threat actor? Were credential extraction results correlated with disk findings (cached hashes, Kerberos ticket files)? Process insights, ask user if they want to expand analysis, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team: did my fileless payload survive detection? Did the analyst find my injected shellcode in the legitimate process? Did they detect my kernel driver rootkit? What about my reflective DLL that never touched disk? Did I clear my tracks from the process command line before the memory was captured? Blue Team: is our memory analysis comprehensive for the OS version? Are there Volatility plugins we did not run? Could the attacker have used anti-memory-forensics techniques (memory encryption, guard pages, pool tag manipulation)? Are our YARA rules current enough to detect modern malware variants? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated and this step added to stepsCompleted. Then read fully and follow: ./step-05-network-forensics.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, analysis_types.memory_forensics set to true, findings counts updated, and Memory Forensics section fully populated in the output document], will you then read fully and follow: `./step-05-network-forensics.md` to begin network forensic analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Working copy integrity verified before analysis began
- OS profile correctly identified for Volatility analysis
- Process analysis performed with three-way comparison (pslist/psscan/pstree) and anomaly detection
- Command line analysis extracted and reviewed for all processes
- Code injection detection performed (malfind, DLL cross-reference, injection technique identification)
- Network connections reconstructed from memory with anomaly flagging
- Credential extraction performed (within legal authorization scope) with results documented
- Kernel integrity analysis performed (SSDT, drivers, rootkit detection)
- YARA scanning performed across process and kernel memory spaces
- Every finding cites evidence ID, memory artifact, and confidence level
- Memory forensics findings summary presented with severity and ATT&CK mapping
- Cross-reference performed with disk forensics findings from step 3
- Frontmatter updated with analysis type, findings counts, IOCs, and techniques
- Findings appended to report under `## Memory Forensics`

### ❌ SYSTEM FAILURE:

- Analyzing master evidence instead of working copies
- Not verifying working copy integrity before analysis
- Not identifying the correct OS profile before Volatility analysis
- Using only one process enumeration method (missing hidden processes)
- Not running malfind or equivalent injection detection
- Not extracting network connections from memory
- Not scanning with YARA rules
- Presenting findings without evidence ID citations
- Not checking kernel integrity (SSDT, drivers)
- Performing disk or network packet analysis during this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Memory forensics reveals what disk forensics cannot — running malware, active connections, injected code, and extracted credentials. The correct profile is essential. Multiple enumeration methods are mandatory. Every finding must be sourced. Memory is volatile truth.
