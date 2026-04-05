# Step 7: Timeline Reconstruction

**Progress: Step 7 of 10** — Next: Findings Consolidation & IOC Summary

## STEP GOAL:

Construct a unified super-timeline by merging artifacts from ALL forensic analysis phases (disk, memory, network, cloud) into a single chronological sequence normalized to UTC. Apply timeline analysis techniques to identify pivot points, activity clusters, gaps, and dwell time. Map the complete attack narrative to ATT&CK. Build a threat actor behavioral profile. The timeline is the factual backbone of the investigation — it transforms individual artifacts into a coherent story with causal relationships.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER fabricate timeline entries — every event must be sourced from collected evidence with an EVD ID
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous timeline generator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst reconstructing the complete forensic timeline under ISO 27037 and NIST SP 800-86
- ✅ The timeline is the single most important deliverable of a forensic investigation — it tells the story of what happened, when, by whom, and in what sequence
- ✅ Every timeline entry MUST be sourced to specific evidence — unsourced entries are speculation, not forensics
- ✅ Confidence levels are mandatory — Confirmed (corroborated by 2+ sources), Probable (one strong source), Possible (circumstantial)
- ✅ Gaps in the timeline are as significant as events — they may indicate anti-forensics, evidence gaps, or periods of attacker dormancy

### Step-Specific Rules:

- 🎯 Focus exclusively on timeline construction, analysis, ATT&CK chain mapping, and threat actor behavioral profiling
- 🚫 FORBIDDEN to perform new forensic analysis — work only with findings from steps 3-6
- 🚫 FORBIDDEN to fabricate events or fill gaps with speculation — document gaps as gaps
- 💬 Approach: Systematic integration of all forensic findings into chronological order, then analytical techniques applied
- 📊 Every timeline entry must cite: evidence ID, source artifact type, timestamp (UTC), confidence level
- ⏱️ ALL timestamps normalized to UTC — mixed timezones create false ordering

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Declaring the timeline "complete" without analyzing gaps is forensically irresponsible — gaps may represent anti-forensic activity (log clearing, timestomping), evidence that was not collected, or periods where the attacker was dormant; each possibility has different implications for the investigation scope and findings
  - Not normalizing all timestamps to a single timezone (UTC) before merging creates false event ordering — a 14:00 EST event and a 14:00 UTC event are 5 hours apart, and incorrect ordering leads to false causal relationships that will be challenged by opposing counsel
  - Building the ATT&CK chain from assumed behavior rather than evidenced artifacts produces a plausible-looking narrative that may be wrong — every technique mapping must cite specific evidence; techniques that are "likely" but not evidenced should be marked as "suspected" with an explanation of why evidence is absent
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Merge ALL findings from steps 3-6 into a unified timeline before analysis
- ⚠️ Normalize ALL timestamps to UTC before merging
- 📋 Tag every timeline entry with evidence source type and EVD ID
- 🔒 Mark confidence level for every timeline entry
- ⚠️ Present [A]/[W]/[C] menu after timeline reconstruction is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to stepsCompleted and updating timeline_entries, dwell_time, mitre_techniques
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: ALL findings from steps 3-6 (disk, memory, network, cloud), case intake data, forensic question, evidence inventory
- Focus: Timeline construction, gap analysis, ATT&CK mapping, dwell time calculation, threat actor profiling
- Limits: Work only with existing findings — do not perform new forensic analysis. Source every entry.
- Dependencies: Completed analysis phases from steps 3-6

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Super-Timeline Construction

Merge artifacts from ALL completed forensic analysis phases into a unified timeline.

**Source Integration Matrix:**

| Source Phase | Artifact Types to Extract | Timestamp Source | Example Events |
|--------------|--------------------------|------------------|----------------|
| Disk (Step 3) | $MFT entries, event logs, registry timestamps, prefetch, amcache, shimcache, SRUM, USN journal, browser history, LNK files, shellbags | File system timestamps, log timestamps, registry timestamps | File creation, program execution, registry modification, web access |
| Memory (Step 4) | Process creation times, network connections, kernel module load times, credential access events | Process timestamps, connection timestamps | Process start, network connection established, credential extracted |
| Network (Step 5) | PCAP timestamps, flow records, firewall logs, proxy logs, DNS queries, IDS alerts | Packet timestamps, flow timestamps, log timestamps | Network connection, DNS query, data transfer, C2 beacon |
| Cloud (Step 6) | CloudTrail events, Azure Activity Log, GCP Audit Log, M365 UAL, sign-in logs | API call timestamps, log event timestamps | API call, authentication, resource modification, data access |

**Timeline Construction Process:**

1. **Extract events from each forensic phase:**
   - Review each finding from steps 3-6
   - For each finding with a timestamp: create a timeline entry
   - For findings that span a time range: create entries for start and end

2. **Normalize all timestamps to UTC:**
   - Identify the timezone of each artifact source
   - Convert all timestamps to UTC
   - Document the original timezone for reference
   - **Common timezone sources:**
     - Windows: Registry `SYSTEM\CurrentControlSet\Control\TimeZoneInformation`
     - Linux: `/etc/timezone` or `timedatectl`
     - Cloud logs: typically already UTC
     - Network captures: typically UTC (check capture tool configuration)

3. **Merge into unified timeline sorted by UTC timestamp**

4. **De-duplicate events:**
   - Same event from multiple sources (e.g., login event in Windows Security Log AND in Azure AD sign-in log)
   - Keep both entries but mark as corroborated — this INCREASES confidence
   - Assign: Confirmed confidence (2+ sources agree)

5. **Tag every entry:**
   - Evidence ID (EVD-{case_id}-{NNN})
   - Source phase (Disk/Memory/Network/Cloud)
   - Source artifact type (event log, prefetch, PCAP, CloudTrail, etc.)
   - Confidence level (Confirmed/Probable/Possible)

6. **Identify gaps:**
   - Time periods where no events are recorded despite expected activity
   - Document each gap with: start time, end time, duration, possible explanations
   - Gap explanations: log clearing (anti-forensics), log retention expired, evidence not collected, monitoring gap, attacker dormancy, legitimate off-hours

**Present Master Timeline:**

```
| # | Timestamp (UTC) | Source Phase | Artifact Type | EVD ID | Event Description | System | Actor | ATT&CK Technique | Confidence |
|---|-----------------|-------------|---------------|--------|-------------------|--------|-------|-------------------|------------|
| 1 | {{timestamp}} | Disk/Memory/Network/Cloud | {{type}} | EVD-{case_id}-XXX | {{description}} | {{hostname/IP}} | {{user/process}} | {{T-code or N/A}} | Confirmed/Probable/Possible |
```

**Timeline Statistics:**
```
Total events in timeline: {{count}}
Time span: {{earliest_event}} to {{latest_event}} ({{duration}})
Events by source phase:
  - Disk artifacts: {{count}} ({{percentage}}%)
  - Memory artifacts: {{count}} ({{percentage}}%)
  - Network artifacts: {{count}} ({{percentage}}%)
  - Cloud artifacts: {{count}} ({{percentage}}%)
Confidence distribution:
  - Confirmed: {{count}} ({{percentage}}%)
  - Probable: {{count}} ({{percentage}}%)
  - Possible: {{count}} ({{percentage}}%)
Timeline gaps identified: {{count}}
Corroborated events (2+ sources): {{count}}
```

### 2. Timeline Analysis Techniques

Apply analytical techniques to extract meaning from the raw timeline:

**Pivot Point Identification:**
- Identify key events that changed the course of the investigation:
  - Initial access (first attacker activity)
  - Privilege escalation (transition from standard to elevated access)
  - Lateral movement initiation (first movement to a new system)
  - Persistence establishment (first persistence mechanism deployed)
  - Data access (first access to sensitive data)
  - Exfiltration initiation (first data transfer out of the environment)
  - Detection (first alert or anomaly that led to investigation)

**Activity Clustering:**
- Group related events by:
  - Time proximity (events within minutes of each other)
  - System affinity (events on the same system)
  - Actor affinity (events by the same user or process)
  - Technique affinity (events using the same ATT&CK technique)
- Clusters represent operational sessions — the attacker working toward a specific objective

**Gap Analysis:**

```
| # | Gap Start (UTC) | Gap End (UTC) | Duration | Systems Affected | Possible Explanation | Impact on Investigation | Confidence |
|---|-----------------|---------------|----------|------------------|---------------------|------------------------|------------|
| 1 | {{start}} | {{end}} | {{duration}} | {{systems}} | {{explanation}} | {{impact}} | High/Medium/Low |
```

**Dwell Time Calculation:**

```
First known attacker activity: {{timestamp}} ({{event_description}})
   Evidence: EVD-{case_id}-{{NNN}} — Source: {{artifact_type}} — Confidence: {{level}}

Detection date: {{timestamp}} ({{detection_source}})
   Evidence: EVD-{case_id}-{{NNN}} — Source: {{artifact_type}}

Dwell Time: {{days}} days, {{hours}} hours, {{minutes}} minutes

Time to contain (from detection): {{hours}} hours, {{minutes}} minutes
Time from initial access to first data access: {{duration}}
Time from initial access to first exfiltration: {{duration or 'N/A'}}
Time from detection to containment: {{duration}}
```

**Dwell Time Context:**
- Industry median dwell time (reference Mandiant M-Trends, CrowdStrike Threat Report, IBM X-Force):
  - Global median: ~16 days (varies by year and report)
  - With internal detection: ~13 days
  - With external notification: ~28 days
- Is this dwell time consistent with the attack complexity observed?
- Given the dwell time, does the scope of compromise match expected attacker capability?

### 3. ATT&CK Chain Reconstruction

Map every timeline event to ATT&CK techniques where applicable, building the complete kill chain:

**For each ATT&CK tactic, document observed techniques with evidence:**

| Tactic | Techniques Observed | Timeline Events | Systems Affected | Evidence IDs | Confidence |
|--------|---------------------|-----------------|------------------|-------------|------------|
| TA0043 Reconnaissance | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0042 Resource Development | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0001 Initial Access | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0002 Execution | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0003 Persistence | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0004 Privilege Escalation | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0005 Defense Evasion | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0006 Credential Access | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0007 Discovery | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0008 Lateral Movement | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0009 Collection | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0011 Command & Control | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0010 Exfiltration | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |
| TA0040 Impact | {{T-codes}} | Events #{{list}} | {{systems}} | EVD-{case_id}-XXX | {{level}} |

**Kill Chain Coverage:**
```
Tactics with confirmed activity: {{count}} / 14
Tactics with probable activity: {{count}} / 14
Tactics with no detected activity: {{count}} / 14 — {{list of undetected tactics}}
```

**For undetected tactics:** Document whether the absence is because:
- The tactic was not relevant to this attack (e.g., no Impact for espionage)
- The tactic occurred but evidence was not available (e.g., Reconnaissance is typically invisible to victim-side monitoring)
- The tactic may have occurred but was concealed by defense evasion

### 4. Threat Actor Behavioral Profile

Build a behavioral profile of the threat actor based on timeline patterns:

**Working Hours Analysis:**
- Plot attacker activity by hour of day (UTC and estimated local time)
- Identify consistent work patterns — suggests a human operator with a regular schedule
- Estimate operator timezone based on activity concentration
- Weekend/holiday activity patterns
- Session duration analysis: how long are attacker operational sessions?

**Tool Preference & Proficiency:**
- What tools did the attacker use? (living off the land vs custom tools vs commodity malware)
- Tool sophistication: basic scripts, intermediate frameworks, advanced custom tooling
- Operational speed: how quickly did the attacker progress through the kill chain?
- Error recovery: did the attacker make mistakes and correct them? (indicates human operator vs automated)

**Operational Security Assessment:**
- Anti-forensics employed: log clearing, timestomping, secure deletion, encrypted tools
- Proxy/anonymization: VPN, Tor, compromised infrastructure for C2
- Credential hygiene: did the attacker rotate access methods, or reuse the same credentials?
- Cleanup behavior: did the attacker remove tools after use?

**Objective Indicators:**
- **Espionage:** Targeted data access, selective exfiltration, long dwell time, stealth priority
- **Financial:** Ransomware staging, banking trojan deployment, BEC activity, cryptocurrency mining
- **Destruction:** Wiper deployment, data deletion, service disruption
- **Hacktivism:** Defacement, data leak staging, public communications
- **Insider Threat:** Authorized access misuse, policy violations, data theft before departure

**Diamond Model Summary:**
```
ADVERSARY: {{known group / unknown / suspected — with confidence level}}
   |
CAPABILITY: {{custom / commodity / living-off-the-land / mixed — with sophistication assessment}}
   |
INFRASTRUCTURE: {{dedicated / shared / compromised / cloud-hosted — with details}}
   |
VICTIM: {{organization, sector, size, geography — from engagement context}}
```

### 5. Append Findings to Report

Write all timeline reconstruction findings under `## Timeline Reconstruction` in the output file `{outputFile}`:

```markdown
## Timeline Reconstruction

### Super-Timeline Construction Methodology
{{methodology_description}}
{{source_integration_matrix}}
{{timestamp_normalization_notes}}

### Master Timeline
{{chronological_timeline_table}}
{{timeline_statistics}}

### ATT&CK Chain Reconstruction
{{per_tactic_analysis}}
{{kill_chain_coverage}}

### Threat Actor Behavioral Profile
{{working_hours_analysis}}
{{tool_preferences}}
{{opsec_assessment}}
{{diamond_model}}

### Timeline Gaps & Analysis
{{gap_table}}
{{dwell_time_calculation}}
{{activity_clustering_summary}}
{{pivot_point_identification}}
```

Update frontmatter:
- Add this step name (`Timeline Reconstruction`) to the end of `stepsCompleted`
- Set `timeline_entries` to the total event count
- Update `dwell_time` with the calculated dwell time as text
- Update `mitre_techniques` with the complete list of all ATT&CK T-codes observed
- Update `lateral_movement_detected` if TA0008 was confirmed
- Update `data_exfiltration_detected` if TA0010 was confirmed

### 6. Present MENU OPTIONS

"**Timeline reconstruction complete.**

Timeline events: {{event_count}} events spanning {{duration}}
Events by source: Disk {{disk_count}} | Memory {{memory_count}} | Network {{network_count}} | Cloud {{cloud_count}}
Confidence: {{confirmed_count}} confirmed | {{probable_count}} probable | {{possible_count}} possible
Corroborated events: {{corroborated_count}}
Timeline gaps: {{gap_count}}
ATT&CK coverage: {{tactics_count}} tactics, {{techniques_count}} techniques
Dwell time: {{dwell_time}}
Threat actor: {{attribution_summary}} ({{confidence}} confidence)
Estimated operator timezone: {{timezone_estimate}}

**Select an option:**
[A] Advanced Elicitation — Challenge timeline completeness, examine gaps, stress-test the ATT&CK chain for missing techniques, validate the threat actor profile
[W] War Room — Red (does the timeline accurately reflect what I did? are there activities the analyst missed? did my anti-forensics create convincing gaps? is the behavioral profile accurate or did I successfully misdirect?) vs Blue (is the timeline complete enough to support findings? are the gaps explainable? is the ATT&CK chain continuous or are there logical gaps that suggest missing techniques? would this timeline withstand cross-examination?)
[C] Continue — Proceed to Step 8: Findings Consolidation & IOC Summary (Step 8 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the timeline. Are there events that should exist based on the ATT&CK chain but are missing? Are the gaps truly gaps or could they be filled by evidence we did not collect? Is the dwell time calculation based on the true first activity or could earlier activity have been missed? Is the threat actor profile supported by evidence or is it speculative? Could the attacker have manipulated timestamps to create a false narrative? Process insights, redisplay menu
- IF W: War Room — Red Team: the timeline shows my main operational sessions, but did the analyst find my early reconnaissance? Did they detect my backup C2 that I barely used? Are there activities I performed during the "gaps" that anti-forensics successfully concealed? Is the behavioral profile accurate or was I successful in disguising my timezone and tools? Blue Team: is this timeline legally defensible? Would a competent opposing expert find inconsistencies? Are all confidence levels justified? Is the ATT&CK mapping evidence-based or assumption-based? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated and this step added to stepsCompleted. Then read fully and follow: ./step-08-findings.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, timeline_entries counted, dwell_time calculated, mitre_techniques complete, and Timeline Reconstruction section fully populated], will you then read fully and follow: `./step-08-findings.md` to begin findings consolidation and IOC summary.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Super-timeline constructed from ALL completed analysis phases (disk, memory, network, cloud)
- All timestamps normalized to UTC before merging
- Every timeline entry sourced with evidence ID, artifact type, and confidence level
- De-duplication performed with corroborated events marked as Confirmed
- Timeline gaps identified and documented with duration, systems affected, and possible explanations
- Dwell time calculated with first activity, detection date, and industry benchmark comparison
- ATT&CK chain mapped across all 14 tactics with evidence citations
- Undetected tactics documented with explanation of why (not relevant, evidence unavailable, or concealed)
- Threat actor behavioral profile built from timeline patterns (working hours, tools, OPSEC, objectives)
- Diamond Model analysis completed
- Activity clusters and pivot points identified
- Frontmatter updated with timeline_entries, dwell_time, mitre_techniques
- Findings appended to report under `## Timeline Reconstruction`

### ❌ SYSTEM FAILURE:

- Creating timeline entries without evidence citations (fabricated events)
- Not normalizing timestamps to UTC (mixed timezone ordering errors)
- Not analyzing timeline gaps (gaps are findings, not blank spaces)
- Not calculating dwell time
- Mapping ATT&CK techniques without evidence support
- Not de-duplicating events from multiple sources
- Not marking confidence levels for timeline entries
- Building threat actor profile from speculation rather than evidence patterns
- Performing new forensic analysis during this step (work with existing findings only)
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. The timeline is the investigation's story told in evidence. Every event must be sourced. Every gap must be explained. Every technique must be evidenced. The timeline transforms artifacts into narrative — but only if every entry is grounded in fact.
