# Step 6: Deep Analysis & Scope Determination

**Progress: Step 6 of 10** — Next: Eradication Planning & Execution

## STEP GOAL:

Conduct comprehensive technical analysis of all collected evidence to determine the full scope of the incident, reconstruct the complete attack timeline, identify root cause, and map the full ATT&CK chain. This is where the evidence collected in step 5 is transformed into actionable intelligence that drives eradication and recovery decisions.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER declare scope "complete" without cross-referencing multiple evidence sources — single-source analysis produces single-source blind spots
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous analysis engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator performing deep forensic analysis to determine the full truth of the incident under NIST 800-61
- ✅ Deep analysis separates what you know from what you assume — every finding must be grounded in evidence, and every gap must be acknowledged
- ✅ The scope determination directly controls the eradication plan — if you miss a compromised system here, it survives eradication and the attacker retains access
- ✅ Timeline reconstruction is the backbone of the investigation — it tells the story of the attack from initial access to detection, and every event must be sourced
- ✅ Root cause is not the same as initial access — root cause is the fundamental weakness that enabled the attack, and addressing it prevents recurrence

### Step-Specific Rules:

- 🎯 Focus exclusively on timeline reconstruction, root cause analysis, ATT&CK chain mapping, scope determination, dwell time calculation, and threat actor assessment
- 🚫 FORBIDDEN to begin eradication or remediation — that is step 7. Analysis informs the plan; this step does not execute the plan
- 🚫 FORBIDDEN to declare scope complete based on a single evidence source — cross-reference forensic artifacts, logs, network data, and endpoint telemetry
- 💬 Approach: Systematic analysis of all evidence sources, building from timeline to root cause to full scope
- 📊 Every finding must cite the specific evidence source, evidence ID, and confidence level (confirmed/probable/possible)
- 🔒 Analyze working copies of evidence only — NEVER modify the master evidence items in `{irt_evidence_chain}/`

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Declaring scope "contained" based on known IOCs alone ignores the possibility of unknown persistence mechanisms or additional compromised systems — a sophisticated attacker uses multiple persistence techniques across multiple systems, and the IOCs you found may only represent one access method while others remain undetected
  - Not involving threat intelligence (Oracle agent) when indicators suggest a known threat actor wastes attribution context that informs eradication completeness — known threat actors have documented TTPs, and understanding which TTPs you have NOT detected tells you where to look for what you missed
  - Relying solely on log-based timeline when logs may have been tampered with — cross-reference with forensic artifacts (file system timestamps, registry modifications, prefetch entries, browser history) for validation, as attackers routinely clear event logs but rarely scrub all forensic artifacts
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Build the timeline before any other analysis — the timeline is the foundation for everything else
- ⚠️ Cross-reference every critical finding across at least two independent evidence sources
- 📋 Cite evidence IDs (EVD-{incident_id}-{seq}) for every finding
- ⚠️ Present [A]/[W]/[C] menu after full analysis is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating severity, scope, and analysis fields
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Complete evidence set from step 5, chain of custody manifest, containment status from step 4, initial triage from steps 1-3, IOCs, MITRE ATT&CK mapping from initial classification
- Focus: Evidence analysis, timeline reconstruction, root cause identification, ATT&CK chain mapping, scope determination, dwell time calculation, threat actor assessment — no eradication, no recovery
- Limits: Analysis is limited to the collected evidence — gaps in evidence collection (documented in step 5) are gaps in analysis. Acknowledge what you cannot determine due to missing evidence.
- Dependencies: Evidence collected and preserved in step-05-evidence.md, containment holding from step-04-containment.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Full Timeline Reconstruction

Build the master timeline by merging ALL evidence sources into a single chronological sequence. The timeline is the factual backbone of the investigation — every event must be sourced and every claim must be evidenced.

**Timeline Sources — extract events from each evidence category:**

**File System Artifacts:**
- MAC times (Modified, Accessed, Created/Changed) for files associated with the incident
- NTFS: $MFT entries, $UsnJrnl (USN Journal) for file creation/modification/deletion/rename events
- NTFS: $LogFile for file system transaction recovery
- Ext4/XFS: inode timestamps, journal entries
- File creation in suspicious directories (Temp, AppData, ProgramData, hidden directories)
- Executable files: compilation timestamps (PE header), first-seen on the system

**Windows Artifacts:**
- Event Logs: Security (4624/4625/4648/4672/4688/4698/4720/7045), System, PowerShell (4103/4104), Sysmon (if deployed), TaskScheduler, Terminal Services
- Prefetch: program execution with timestamps and execution count (.pf files in C:\Windows\Prefetch)
- Amcache: program execution evidence including file hash, path, publisher, and first execution time (Amcache.hve)
- ShimCache (AppCompatCache): program execution evidence from the Application Compatibility Cache
- SRUM (System Resource Usage Monitor): per-application network usage, CPU time, and energy data — proves execution even if other artifacts are cleaned
- USN Journal: file system changes with timestamps — survives log clearing
- Jump Lists: recent documents and application usage per user
- LNK files: shortcut files with target path, creation time, access time, and volume information
- BAM/DAM (Background Activity Moderator): last execution time for executables on Windows 10+
- UserAssist: program execution with run count and last run time (ROT13 encoded in registry)
- MRU (Most Recently Used): recently accessed files, typed paths, run dialog entries

**Linux Artifacts:**
- auth.log / secure: authentication events, sudo usage, SSH sessions
- bash_history / zsh_history: command history per user (may be cleared by attacker)
- wtmp / btmp: login records (successful and failed)
- lastlog: last login per user
- cron logs: scheduled task execution
- systemd journal: comprehensive system log with structured fields
- Package manager logs: recently installed packages (apt, yum, dpkg)
- Audit logs: if auditd is configured, detailed system call and file access logging

**Registry Artifacts (Windows):**
- Run/RunOnce keys: persistence mechanisms (HKLM and HKCU)
- Services: newly created or modified services (HKLM\SYSTEM\CurrentControlSet\Services)
- UserAssist: encoded program execution evidence
- MRU lists: recently accessed files, typed URLs, search terms
- Network profiles: recently connected networks with timestamps
- Shellbags: folder access evidence with timestamps
- TypedPaths / TypedURLs: URLs and paths manually entered by the user

**Network Artifacts:**
- Firewall logs: allowed and denied connections with source, destination, port, protocol
- Proxy logs: HTTP/HTTPS requests with URL, user agent, response code, bytes transferred
- DNS query logs: domain resolution requests with source IP, queried domain, response
- NetFlow/IPFIX: network flow summaries (source, destination, port, bytes, duration)
- IDS/IPS alerts: triggered signatures with timestamps and payload snippets
- VPN logs: remote access sessions with user, source IP, duration

**Authentication Artifacts:**
- Kerberos ticket events: TGT/TGS requests, ticket renewals, failed authentication
- NTLM authentication events: legacy authentication (often used in pass-the-hash)
- OAuth/SAML events: token issuance, consent grants, application access
- SSO/federation logs: identity provider authentication events
- MFA events: challenge/response, bypass, enrollment changes
- Azure AD / Entra ID sign-in logs: conditional access evaluation, risk events, token issuance

**Cloud Artifacts:**
- AWS CloudTrail: API calls with caller identity, source IP, parameters, and response
- Azure Activity Log: resource operations, administrative actions
- Azure AD Audit Log: directory changes, application registrations, role assignments
- GCP Audit Log: admin activity, data access, system events
- Cloud storage access logs: object reads, writes, permission changes
- Cloud compute logs: instance creation, modification, deletion, console access

**Email Artifacts:**
- Email headers: routing information, authentication results (SPF/DKIM/DMARC), timestamps
- Delivery logs: message tracking from send to delivery
- Mail rules: auto-forward rules, inbox rules, transport rules created/modified during incident window
- DLP alerts: data loss prevention triggers related to the incident

**Timeline Construction Method:**

1. **Normalize all timestamps to UTC** — mixed timezones in the timeline create false ordering and analytical errors
2. **Extract events from every evidence source** listed above that is available in the collected evidence set
3. **Merge into a single unified timeline** sorted by UTC timestamp
4. **De-duplicate** events that appear in multiple sources (e.g., same login in SIEM and Windows Event Log) — keep both entries but mark them as corroborated
5. **Identify gaps** — time periods where no events are recorded, despite expected activity. Gaps may indicate:
   - Log clearing by the attacker
   - Log rotation that predates the collection window
   - Systems not being monitored
   - Evidence that was not collected or was unavailable
6. **Mark confidence level** for each event:
   - **Confirmed**: corroborated by 2+ independent evidence sources
   - **Probable**: supported by one strong evidence source with consistent context
   - **Possible**: inferred from circumstantial evidence or single weak source

**Present as chronological timeline table:**

```
| # | Timestamp (UTC) | Source | Evidence ID | Event Description | System | Actor | ATT&CK Technique | Confidence |
|---|-----------------|--------|-------------|-------------------|--------|-------|------------------|------------|
| 1 | {{timestamp}} | {{source_type}} | EVD-{id}-{{seq}} | {{description}} | {{hostname/IP}} | {{user/process}} | {{T-code or N/A}} | Confirmed/Probable/Possible |
```

**Timeline Statistics:**
```
Total events in timeline: {{count}}
Time span: {{earliest_event}} to {{latest_event}} ({{duration}})
Confirmed events: {{count}} ({{percentage}}%)
Probable events: {{count}} ({{percentage}}%)
Possible events: {{count}} ({{percentage}}%)
Evidence sources contributing: {{count}} sources
Timeline gaps identified: {{count}} — {{gap_descriptions}}
```

### 2. Root Cause Analysis

Determine the initial compromise vector and the fundamental weakness that enabled the attack. Root cause goes deeper than "how did they get in" — it answers "why were they able to get in."

**Initial Access Vector Determination:**
- What was the first confirmed attacker activity in the timeline?
- What was the entry point: phishing email, exploited vulnerability, compromised credentials, supply chain, insider?
- What evidence confirms the initial access vector? (cite evidence IDs)
- Were there earlier reconnaissance activities that preceded the initial access?

**Enabling Vulnerability Identification:**
- What specific weakness was exploited?
  - Software vulnerability: CVE number, affected software, patch availability, patch status at time of incident
  - Configuration weakness: what was misconfigured, what the secure configuration should be, why it was not applied
  - Credential weakness: weak password, password reuse, no MFA, exposed credentials, default credentials
  - Human factor: social engineering success, policy violation, insufficient training
  - Process gap: missing patch management, inadequate access review, no change management

**Contributing Factors:**
- What other conditions made the attack possible or easier?
- Were there compensating controls that should have caught the attack but did not?
- Were there policy violations or process failures that contributed?
- Was there a chain of failures, or was a single failure sufficient?

**Prevention Gap Analysis:**
- What security control was absent, misconfigured, or bypassed?
- Was this a known risk that was accepted, or an unknown risk?
- Was there a detection opportunity that was missed?
- Was there a prevention opportunity that was not implemented?

**Present as root cause chain (proximate to root):**

```
Proximate Cause: {{the immediate action that caused the incident}}
    ↓ enabled by
Intermediate Cause: {{the condition that allowed the proximate cause}}
    ↓ enabled by
Root Cause: {{the fundamental weakness — the thing that, if fixed, would have prevented the entire incident}}
```

**Root Cause Classification:**
| Category | Subcategory | Description | Evidence |
|----------|-------------|-------------|----------|
| Technical / Process / Human | {{specific}} | {{detail}} | EVD-{id}-{{seq}} |

### 3. Full ATT&CK Chain Mapping

Map the complete attack narrative to the MITRE ATT&CK framework, using the timeline as the factual basis. For each tactic, identify the specific techniques observed, the evidence supporting the mapping, and the affected systems.

**For each ATT&CK tactic, evaluate and document:**

**TA0043 — Reconnaissance:**
- What did the attacker learn before the attack? (open-source intelligence, scanning, social engineering)
- Evidence: DNS logs showing zone transfer attempts, web server logs showing directory enumeration, LinkedIn scraping indicators, email header analysis showing target validation
- Techniques observed: {{T-codes with evidence}}
- If no evidence: note whether reconnaissance would have been visible to our monitoring

**TA0042 — Resource Development:**
- What infrastructure, tools, or accounts did the attacker prepare?
- Evidence: C2 domain registration dates, SSL certificate creation dates, compromised account acquisition timeline
- Techniques observed: {{T-codes with evidence}}
- If no evidence: note whether resource development is typically invisible to victim-side monitoring

**TA0001 — Initial Access:**
- How did the attacker enter the environment?
- Evidence: phishing email, exploit logs, credential abuse, supply chain artifact
- Techniques observed: {{T-codes with evidence}}
- This should align with the root cause analysis from instruction 2

**TA0002 — Execution:**
- What did the attacker run on the compromised systems?
- Evidence: process execution logs, Prefetch, Amcache, PowerShell script block logs, command history
- Techniques observed: {{T-codes with evidence}}
- Document: command lines, scripts, binaries, and their purpose in the attack chain

**TA0003 — Persistence:**
- How did the attacker maintain access across reboots, credential changes, and containment?
- Evidence: registry modifications (Run keys, services), scheduled tasks, cron jobs, web shells, implant files, startup items, account creation
- Techniques observed: {{T-codes with evidence}}
- **CRITICAL for eradication:** every persistence mechanism found here must be removed in step 7

**TA0004 — Privilege Escalation:**
- How did the attacker obtain elevated access?
- Evidence: privilege escalation exploits, token manipulation, UAC bypass artifacts, sudo abuse, SUID binary exploitation
- Techniques observed: {{T-codes with evidence}}
- Document: from what privilege level to what privilege level, on which systems

**TA0005 — Defense Evasion:**
- How did the attacker hide from detection and analysis?
- Evidence: log clearing events (1102), timestomping artifacts (MAC time inconsistencies), process injection artifacts, AV/EDR tampering, obfuscated scripts
- Techniques observed: {{T-codes with evidence}}
- Note: defense evasion artifacts may explain gaps in the timeline

**TA0006 — Credential Access:**
- What credentials did the attacker harvest, and how?
- Evidence: LSASS access events, credential dumping tool artifacts (Mimikatz, secretsdump), Kerberoasting events (TGS requests for service accounts), password spray patterns, keylogger artifacts
- Techniques observed: {{T-codes with evidence}}
- **CRITICAL for eradication:** every compromised credential must be rotated in step 7

**TA0007 — Discovery:**
- What did the attacker enumerate within the environment?
- Evidence: Active Directory enumeration queries (BloodHound, PowerView, net commands), network scanning artifacts, share enumeration, file system browsing patterns
- Techniques observed: {{T-codes with evidence}}
- The scope of discovery tells you the scope of the attacker's knowledge about your environment

**TA0008 — Lateral Movement:**
- How did the attacker move between systems?
- Evidence: remote logon events (type 3, 10), PsExec/WMI/WinRM artifacts, RDP session logs, SSH session logs, pass-the-hash/pass-the-ticket events, remote service creation
- Techniques observed: {{T-codes with evidence}}
- Map the exact path: system A → system B → system C, with timestamps and credentials used

**TA0009 — Collection:**
- What data did the attacker gather?
- Evidence: file access logs, data staging artifacts (compressed archives in temp directories), clipboard access, email collection (mailbox export, rule creation), database query logs
- Techniques observed: {{T-codes with evidence}}
- Identify what data was targeted and whether it includes sensitive/regulated data

**TA0011 — Command and Control:**
- How did the attacker communicate with the compromised environment?
- Evidence: C2 callback network traffic, DNS tunneling patterns, beaconing behavior (regular interval connections), encrypted channels, proxy usage, protocol tunneling
- Techniques observed: {{T-codes with evidence}}
- Document: C2 infrastructure (IPs, domains, ports, protocols), beacon intervals, data encoding

**TA0010 — Exfiltration:**
- Did the attacker remove data from the environment?
- Evidence: large outbound transfers to external IPs, DNS exfiltration patterns, cloud storage uploads, email-based exfiltration, removable media artifacts
- Techniques observed: {{T-codes with evidence}}
- **CRITICAL for regulatory notification:** if data exfiltration is confirmed, this triggers notification obligations

**TA0040 — Impact:**
- Did the attacker cause direct damage?
- Evidence: file encryption artifacts, service disruption logs, data deletion artifacts, defacement, resource hijacking (cryptomining)
- Techniques observed: {{T-codes with evidence}}
- Assess: was the impact intentional (objective) or collateral (side effect of other activity)?

**Present ATT&CK summary:**

```
| Tactic | Techniques Observed | Systems Affected | Evidence IDs | Confidence |
|--------|---------------------|------------------|-------------|------------|
| TA0043 Reconnaissance | {{T-codes}} | {{systems}} | EVD-{id}-{{seq}} | {{level}} |
| TA0042 Resource Development | {{T-codes}} | {{systems}} | EVD-{id}-{{seq}} | {{level}} |
...
| TA0040 Impact | {{T-codes}} | {{systems}} | EVD-{id}-{{seq}} | {{level}} |
```

**Kill Chain Coverage:**
```
Tactics with confirmed activity: {{count}} / 14
Tactics with probable activity: {{count}} / 14
Tactics with no detected activity: {{count}} / 14
```

### 4. Complete Scope Determination

Using the timeline, root cause, and ATT&CK mapping, determine the full blast radius of the incident. This is the definitive answer on what was compromised.

**Compromised Systems — Complete Inventory:**

```
| # | System | Hostname | IP | Role | Compromise Type | First Activity | Last Activity | Evidence | Confidence |
|---|--------|----------|-----|------|-----------------|----------------|---------------|----------|------------|
| 1 | {{system}} | {{host}} | {{ip}} | {{role}} | Initial Access / Lateral Movement / C2 / Persistence | {{timestamp}} | {{timestamp}} | EVD-{id}-{{seq}} | Confirmed/Suspected |
```

**Compromised Accounts — Complete Inventory:**

```
| # | Account | Type | Privilege Level | Compromise Method | First Misuse | Last Misuse | Evidence | Confidence |
|---|---------|------|-----------------|-------------------|--------------|-------------|----------|------------|
| 1 | {{account}} | User / Service / Admin / Machine | {{level}} | {{method}} | {{timestamp}} | {{timestamp}} | EVD-{id}-{{seq}} | Confirmed/Suspected |
```

**Accessed Data Repositories:**

```
| # | Repository | Type | Data Classification | Access Type | Data Volume | Exfiltration Evidence | Evidence | Confidence |
|---|------------|------|--------------------|----|-------------|----------------------|----------|------------|
| 1 | {{repo}} | File Share / Database / Email / Cloud Storage | {{classification}} | Read / Write / Delete / Exfiltrate | {{volume}} | {{yes/no/unknown}} | EVD-{id}-{{seq}} | Confirmed/Suspected |
```

**Network Segments with Attacker Presence:**
- List every network segment where attacker activity was detected
- Note the duration of presence in each segment
- Identify any segments where the attacker had presence but is now contained

**Cloud Resources Accessed/Modified:**
- Cloud accounts, subscriptions, projects accessed
- Resources created, modified, or deleted by the attacker
- IAM changes (roles, permissions, policies) made by the attacker
- Cloud storage objects accessed or exfiltrated

**Lateral Movement Map:**
- Reconstruct the exact path the attacker took through the environment
- Document: source system → destination system, method used, credentials used, timestamp
- Present as a directed graph description (text-based)

**Data Exfiltration Assessment:**
- Confirmed exfiltration: what data, how much, to where, when
- Suspected exfiltration: what data may have been exfiltrated based on access patterns without confirmed outbound transfer
- Not exfiltrated: data repositories that were not accessed or where access was read-only with no outbound transfer evidence

### 5. Dwell Time Calculation

Calculate the time between first attacker activity and detection. Dwell time is one of the most important incident metrics — it determines how much damage the attacker could have accomplished.

**Calculation:**

```
First known attacker activity: {{timestamp}} ({{event_description}})
   Evidence: EVD-{id}-{{seq}} — Confidence: {{level}}

Detection date: {{timestamp}} ({{detection_source}})
   Evidence: EVD-{id}-{{seq}}

Dwell Time: {{days}} days, {{hours}} hours

Containment date: {{timestamp}}
Time to contain (from detection): {{hours}} hours
```

**Dwell Time Context:**
- Industry benchmark comparison: median dwell time by sector (reference current year statistics from Mandiant M-Trends, CrowdStrike threat report, or IBM X-Force)
- Is this dwell time consistent with the observed attack complexity?
- Given the dwell time, what could the attacker have accomplished?
  - Days 1-7: initial access, execution, basic persistence, local discovery
  - Days 8-30: privilege escalation, credential access, lateral movement, deeper persistence
  - Days 31-90: extensive discovery, data collection staging, C2 infrastructure maturation
  - Days 90+: complete environment compromise, data exfiltration, potential impact preparation
- Does the observed scope match the expected scope for this dwell time, or is it larger/smaller than expected?

### 6. Threat Actor Assessment

If attribution is possible or relevant, assess the threat actor behind the incident. Attribution is NOT required for effective incident response — but understanding the adversary informs eradication completeness.

**Indicator-Based Assessment:**
- Do any IOCs (malware hashes, C2 infrastructure, email addresses) match known threat actor databases?
- Do the TTPs (techniques, tactics, procedures) match documented threat actor profiles?
- Is the malware a known family associated with a specific threat group?
- Does the C2 infrastructure overlap with previously attributed campaigns?

**Diamond Model Analysis:**

```
ADVERSARY: {{known group / unknown / suspected}}
   ↕
CAPABILITY: {{custom tooling / commodity malware / living-off-the-land / mixed}}
   ↕
INFRASTRUCTURE: {{dedicated / shared / compromised third-party / cloud-hosted}}
   ↕
VICTIM: {{organization name, sector, size, geography}}
```

**Motivation Assessment:**
- **Financial**: ransomware preparation, cryptocurrency mining, banking trojan, business email compromise
- **Espionage**: intellectual property theft, state-sponsored intelligence collection, competitive intelligence
- **Hacktivism**: defacement, data leak, service disruption for ideological purposes
- **Insider Threat**: disgruntled employee, departing employee data theft, policy violation
- **Unknown**: insufficient evidence for motivation determination

**Attribution Confidence:**
- **High**: multiple independent indicators pointing to the same known threat actor, consistent with their documented TTPs and targeting profile
- **Medium**: some indicators match a known group, but alternative explanations exist (shared tooling, false flag)
- **Low**: limited indicators, could match multiple groups or an unknown actor
- **No Attribution**: insufficient evidence for meaningful attribution

**Oracle (Threat Intelligence) Recommendation:**
- If indicators suggest a known threat actor or APT group: recommend invoking `spectra-threat-intel` workflow with the Oracle agent for deeper analysis
- If malware samples are available: recommend invoking `spectra-malware-analysis` for detailed capability assessment
- If attribution is uncertain: recommend presenting IOCs to threat intelligence sharing communities (ISAC, FIRST) for collaborative analysis
- Document the recommendation and whether the operator approves further intelligence analysis

### 7. Update Severity & Frontmatter

Based on the complete analysis, provide the final severity assessment and update all relevant frontmatter fields.

**Severity Comparison:**

```
| Assessment Point | Severity | Basis |
|------------------|----------|-------|
| Step 1 (Intake) | {{initial_severity}} | {{initial_basis}} |
| Step 3 (Triage) | {{triage_severity}} | {{triage_basis}} |
| Step 6 (Analysis) | {{final_severity}} | {{analysis_basis}} |
| Change? | {{Yes — escalated/de-escalated / No — confirmed}} | {{justification}} |
```

If severity changed: document the specific evidence that justified the change.

**Update frontmatter:**
- Add this step name (`Deep Analysis & Scope Determination`) to the end of the `stepsCompleted` array
- `incident_severity`: final severity assessment
- `affected_systems`: total count of confirmed + suspected compromised systems
- `affected_users`: total count of confirmed + suspected compromised user accounts
- `affected_data`: summary of data repositories accessed/exfiltrated
- `iocs_identified`: total count of unique IOCs identified across all evidence
- `mitre_techniques`: complete list of all ATT&CK technique T-codes observed
- `dwell_time`: calculated dwell time as text (e.g., "14 days 6 hours")
- `root_cause`: one-line root cause summary
- `attack_vector`: initial access technique (T-code and name)
- `lateral_movement_detected`: true/false based on TA0008 findings
- `data_exfiltration_detected`: true/false based on TA0010 findings
- `persistence_mechanisms`: count of persistence mechanisms identified

### 8. Append Findings to Report

Write all deep analysis findings under `## Deep Analysis & Scope Determination` in the output file `{outputFile}`:

```markdown
## Deep Analysis & Scope Determination

### Root Cause Analysis
{{root_cause_chain_from_instruction_2}}

### Attack Vector Reconstruction
{{initial_access_details_and_evidence}}

### Kill Chain / Attack Flow
{{full_att&ck_chain_mapping_from_instruction_3}}

### Lateral Movement Analysis
{{lateral_movement_map_and_paths}}

### Persistence Mechanism Inventory
{{all_persistence_mechanisms_from_TA0003}}

### Data Access & Exfiltration Assessment
{{data_repositories_accessed_and_exfiltration_evidence}}

### Dwell Time Calculation
{{dwell_time_calculation_from_instruction_5}}

### Full Scope Determination
{{compromised_systems_accounts_data_from_instruction_4}}

### IOC Correlation & Enrichment
{{ioc_summary_with_threat_actor_context}}
```

### 9. Present MENU OPTIONS

"**Deep analysis and scope determination complete.**

Timeline events: {{event_count}} events spanning {{duration}}
Root cause: {{root_cause_one_liner}}
ATT&CK coverage: {{tactics_count}} tactics, {{techniques_count}} techniques
Compromised systems: {{system_count}} ({{confirmed_count}} confirmed, {{suspected_count}} suspected)
Compromised accounts: {{account_count}} ({{confirmed_count}} confirmed, {{suspected_count}} suspected)
Data exfiltration: {{confirmed / suspected / not detected}}
Dwell time: {{dwell_time}}
Persistence mechanisms: {{persistence_count}}
Threat actor: {{attribution_summary}} ({{confidence}} confidence)
Severity: {{final_severity}} ({{changed_or_confirmed}} from triage)

**Select an option:**
[A] Advanced Elicitation — Challenge scope completeness and analysis assumptions
[W] War Room — Red Team: based on the attacker's current position, what would the next move be? What have the defenders not found yet? Blue Team: what detection gaps allowed this dwell time? Are we confident we found all persistence before eradication?
[C] Continue — Proceed to Step 7: Eradication Planning & Execution"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the analysis from multiple angles. Is the scope truly complete or could there be compromised systems without indicators? Is the root cause the real root cause, or just the most visible failure? Are there ATT&CK techniques that should be present based on the attack pattern but were not detected — does that mean they did not happen or that we lack visibility? Is the dwell time accurate, or could earlier activity be hiding before the timeline start? Could the attacker have planted false evidence to misdirect the investigation? Process insights, ask user if they want to expand analysis, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: the defenders think they found everything. What did they miss? Based on my TTPs, where would I have hidden persistence that survives their eradication plan? Did they find my backup C2 channel? Did they find the secondary account I compromised for re-entry? What would I do next to re-establish access after eradication? Blue Team perspective: are we confident the timeline is complete? Did the attacker clear logs that we cannot recover? Are there systems in the scope that we do not have evidence for? Is our persistence inventory complete enough to drive eradication? What detection improvements would have caught this earlier? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated with all fields from instruction 7 and this step added to stepsCompleted. Then read fully and follow: ./step-07-eradication.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, incident_severity, affected_systems, affected_users, affected_data, iocs_identified, mitre_techniques, dwell_time, root_cause, attack_vector, lateral_movement_detected, data_exfiltration_detected, and persistence_mechanisms all updated, and Deep Analysis & Scope Determination section fully populated in the output document], will you then read fully and follow: `./step-07-eradication.md` to begin eradication planning and execution.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Master timeline reconstructed from ALL available evidence sources with events normalized to UTC, merged, de-duplicated, and confidence-rated
- Timeline gaps identified and documented with potential explanations (log clearing, retention, monitoring gaps)
- Root cause identified as a chain from proximate cause through intermediate to fundamental root cause, with evidence citations
- Full ATT&CK chain mapped across all 14 tactics with specific techniques, evidence IDs, affected systems, and confidence levels for each
- Kill chain coverage statistics calculated (confirmed, probable, not detected per tactic)
- Complete scope determination with inventories of compromised systems, accounts, data repositories, network segments, and cloud resources
- Lateral movement paths reconstructed with source, destination, method, credentials, and timestamps
- Data exfiltration assessed as confirmed, suspected, or not detected with supporting evidence
- Dwell time calculated with first attacker activity, detection date, and industry benchmark comparison
- Threat actor assessed using Diamond Model with motivation and attribution confidence
- Severity compared across intake, triage, and analysis with documented justification for any change
- All frontmatter fields updated (incident_severity, affected_systems, affected_users, affected_data, iocs_identified, mitre_techniques, dwell_time, root_cause, attack_vector, lateral_movement_detected, data_exfiltration_detected, persistence_mechanisms)
- Findings appended to report under `## Deep Analysis & Scope Determination`
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Declaring scope complete based on a single evidence source without cross-referencing
- Building timeline from logs alone without forensic artifact validation (attackers clear logs)
- Not citing evidence IDs for analysis findings — unsubstantiated claims are not analysis
- Mapping ATT&CK techniques based on speculation rather than observed evidence
- Declaring "no lateral movement" without analyzing authentication logs, remote service events, and network traffic
- Declaring "no exfiltration" without analyzing outbound network traffic, DNS logs, and cloud storage access
- Not identifying persistence mechanisms — this directly causes eradication failure
- Not calculating dwell time — it is a key incident metric required for post-incident review and regulatory reporting
- Beginning eradication or remediation actions during analysis — this step informs the plan, it does not execute it
- Not acknowledging analysis gaps caused by missing evidence (documented in step 5)
- Not recommending threat intelligence analysis (Oracle) when indicators suggest a known threat actor
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Deep analysis is where evidence becomes intelligence. Every finding must be sourced. Every gap must be acknowledged. The scope determination drives the entire eradication and recovery plan — if the scope is wrong, eradication is incomplete and the attacker retains access. Thoroughness here prevents failure downstream.
