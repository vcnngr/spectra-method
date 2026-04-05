# Step 4: Correlation and Kill Chain Mapping

**Progress: Step 4 of 7** — Next: Classification and Priority Assignment

## STEP GOAL:

Identify related alerts and events, map all activity to MITRE ATT&CK techniques, plot on the kill chain to determine attack stage and scope, and assess whether this is an isolated event or part of a coordinated campaign.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER correlate alerts without evidence linking them — each connection must be justified
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC TRIAGE ANALYST, not an automated correlation engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Triage Analyst conducting structured alert analysis
- ✅ Correlation reveals what a single alert cannot — whether the activity is isolated or part of a larger operation
- ✅ Every correlation must cite the evidence connecting the alerts — unsubstantiated connections create false campaign narratives
- ✅ ATT&CK mapping must be based on observed behavior, not speculation about what an attacker might do next

### Step-Specific Rules:

- 🎯 Focus exclusively on alert correlation, ATT&CK mapping, and kill chain analysis
- 🚫 FORBIDDEN to begin containment, response, or escalation — this is analytical correlation
- 💬 Approach: Systematic search for related signals followed by structured ATT&CK mapping and campaign assessment
- 📊 Every correlated alert must include: relationship type, evidence for the connection, and confidence level
- 🔒 Only correlate alerts within the monitored environment — do not assume activity on unmonitored assets

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Limiting correlation to a narrow time window may miss slow-and-low attacks that span days or weeks — adversaries deliberately space their activity to avoid triggering time-based correlation rules
  - Absence of correlated alerts does not mean absence of attack — the adversary may have only triggered one detection while operating across multiple hosts undetected
  - Over-correlating unrelated alerts can create false campaign narratives that misdirect response efforts — require specific evidence (shared IOCs, same user, same host, temporal proximity) for each connection
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present correlation search plan before beginning — identify search dimensions and time windows
- ⚠️ Present [A]/[W]/[C] menu after correlation and mapping complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `mitre_techniques`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, alert data, normalized fields, enriched IOCs, and asset/user context from steps 1-3
- Focus: Alert correlation, ATT&CK technique mapping, kill chain plotting, and campaign assessment — no response actions
- Limits: Only correlate alerts present in the monitoring environment — do not assume undetected activity without evidence
- Dependencies: Alert intake, IOC enrichment, and context gathering from steps 1-3

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Related Alert Search

Search for related signals across multiple correlation dimensions. For each dimension, specify the search scope and time windows:

**Dimension 1 — Same Affected Host:**
- Search for all alerts on the same host(s) in: last 24 hours, last 7 days, last 30 days
- Include: SIEM alerts, EDR detections, firewall logs, authentication events

**Dimension 2 — Same Affected User:**
- Search for all alerts involving the same user account(s) in: last 24 hours, last 7 days, last 30 days
- Include: authentication anomalies, policy violations, privilege escalation attempts, data access alerts

**Dimension 3 — Same Source IP:**
- Search for any alerts across the entire environment involving the same source IP(s)
- No time limit — any historical match is relevant for infrastructure analysis

**Dimension 4 — Same IOCs:**
- Search for any alerts containing the same enriched IOCs (IPs, domains, hashes) from step 2
- Cross-reference: same hash on different hosts, same C2 domain from different users, same IP contacting multiple assets

**Dimension 5 — Same MITRE Technique:**
- Search for other hosts or users showing the same ATT&CK technique behavior
- This reveals whether the attack pattern is targeting multiple assets simultaneously

Present correlated alerts:
```
| # | Alert ID | Timestamp | Source | Technique | Host | User | Severity | Relationship | Evidence |
|---|----------|-----------|--------|-----------|------|------|----------|-------------|----------|
| 1 | {{id}} | {{time}} | {{source}} | {{technique}} | {{host}} | {{user}} | {{sev}} | Same Host/User/IP/IOC/Technique | {{evidence}} |
```

**Correlation Statistics:**
```
Total Related Alerts Found: {{total}}
- Same Host: {{count}}
- Same User: {{count}}
- Same Source IP: {{count}}
- Same IOCs: {{count}}
- Same Technique (other assets): {{count}}
Unique hosts involved: {{count}}
Unique users involved: {{count}}
Time span of correlated activity: {{earliest}} to {{latest}}
```

### 2. ATT&CK Technique Mapping

Map ALL alerts (the original alert plus every correlated alert) to MITRE ATT&CK techniques:

**For each alert, determine:**
- The observed behavior that triggered the alert
- The ATT&CK technique(s) that best describe the behavior
- The tactic (kill chain phase) the technique belongs to
- The expected data source for this technique (per ATT&CK documentation) — validate that the detection aligns
- Confidence in the mapping: High (behavior is textbook match), Medium (behavior is consistent but ambiguous), Low (best guess based on limited data)

Present ATT&CK mapping:
```
| # | Alert / Event | Observed Behavior | ATT&CK Technique | Tactic | Data Source | Mapping Confidence |
|---|--------------|-------------------|-------------------|--------|-------------|-------------------|
| 1 | {{alert}} | {{behavior}} | {{T-code}} {{name}} | {{tactic}} | {{source}} | High/Medium/Low |
```

**Technique Summary:**
```
Unique techniques identified: {{count}}
Unique tactics covered: {{count}}
Techniques mapped with high confidence: {{count}}
Techniques mapped with medium/low confidence: {{count}}
```

### 3. Kill Chain Plot

Visualize the full MITRE ATT&CK kill chain and mark which tactics have detected activity:

```
[  ] TA0043 Reconnaissance
[  ] TA0042 Resource Development
[  ] TA0001 Initial Access
[  ] TA0002 Execution
[  ] TA0003 Persistence
[  ] TA0004 Privilege Escalation
[  ] TA0005 Defense Evasion
[  ] TA0006 Credential Access
[  ] TA0007 Discovery
[  ] TA0008 Lateral Movement
[  ] TA0009 Collection
[  ] TA0011 Command and Control
[  ] TA0010 Exfiltration
[  ] TA0040 Impact
```

Mark each tactic: `[X]` for detected activity, `[?]` for suspected but unconfirmed, `[ ]` for no detection.

**Kill Chain Analysis:**

**Earliest detected stage:** {{tactic_id}} {{tactic_name}} — {{evidence}}
**Latest detected stage:** {{tactic_id}} {{tactic_name}} — {{evidence}}

**Gap Analysis:**
- Identify gaps between detected stages — these represent potential undetected adversary activity
- For each gap: what would the attacker need to do between the detected stages? What telemetry sources would capture it? Is the absence of detection a coverage gap or evidence the attacker has not progressed?

```
| Gap | Expected Activity | Telemetry Source | Detection Coverage | Assessment |
|-----|-------------------|-----------------|-------------------|------------|
| {{tactic_A}} → {{tactic_B}} | {{expected}} | {{source}} | Covered/Partial/Blind Spot | Gap likely real / Gap likely coverage issue |
```

**Attack Progression Assessment:**
- **Linear progression** (sequential tactics): suggests methodical, potentially automated or playbook-driven attack
- **Scattered tactics** (non-sequential): suggests opportunistic attacker or multiple unrelated events incorrectly correlated
- **Late-stage only** (C2, exfil, impact without early stages): suggests the early stages were missed or the attacker had prior access
- **Early-stage only** (recon, initial access): suggests the attack is in progress or was stopped early

### 4. Campaign Assessment

Evaluate whether this represents an isolated event or a coordinated campaign:

**Assessment Criteria:**

**Scope Analysis:**
- Single host or multiple hosts affected?
- Single user or multiple users affected?
- Single network zone or cross-zone activity?

**Temporal Analysis:**
- All activity within a short window (minutes/hours) or spread over days/weeks?
- Is there a pattern to the timing (working hours, after hours, regular intervals)?

**IOC Overlap:**
- Do the correlated alerts share IOCs with the original alert?
- Do the IOCs map to known threat actor infrastructure or malware families (from step 2)?
- Is there shared C2 infrastructure across multiple hosts?

**Behavioral Consistency:**
- Do the correlated alerts show a consistent attack methodology?
- Is there evidence of the same toolset across multiple alerts (same JA3 hash, same process chain, same file names)?

**Campaign Verdict:**

| Verdict | Criteria | Confidence |
|---------|----------|------------|
| **Isolated Event** | Single alert, no correlated activity, no shared IOCs | High/Medium/Low |
| **Related Activity** | Multiple alerts sharing IOCs or host/user, but no clear attack progression | High/Medium/Low |
| **Suspected Campaign** | Multiple alerts across hosts/users showing kill chain progression with shared infrastructure | High/Medium/Low |
| **Confirmed Campaign** | Clear multi-stage attack with shared IOCs, kill chain coverage across multiple tactics, and known threat actor association | High/Medium/Low |

Select the appropriate verdict and justify with specific evidence.

**Adversary Objective Assessment:**
Based on kill chain position, what is the likely adversary objective?
- **Reconnaissance / Foothold**: early-stage activity, attacker is still establishing access
- **Expansion**: lateral movement, privilege escalation, credential harvesting in progress
- **Objective execution**: collection, exfiltration, or impact activity detected
- **Unknown**: insufficient data to determine objective

### 5. Correlation Summary

Synthesize all correlation findings into actionable intelligence:

**Present consolidated summary:**
```
Total Correlated Alerts: {{count}}
Kill Chain Coverage: {{tactics_detected}} of 14 tactics ({{tactic_list}})
Scope: Single Host / Multiple Hosts ({{count}}) / Organization-Wide
Campaign Assessment: {{verdict}} ({{confidence}} confidence)
Adversary Objective: {{objective}}
Time Span: {{earliest_alert}} to {{latest_alert}} ({{duration}})
```

**Key Correlation Finding:**
What does the correlation tell us that the individual alert from step 1 did not? Present the single most important insight gained through correlation analysis — this finding should directly influence the classification decision in step 5.

### 6. Present MENU OPTIONS

"**Correlation and kill chain mapping complete.**

Correlated alerts: {{correlated_count}} | Unique techniques: {{technique_count}} | Tactics covered: {{tactic_count}}/14
Scope: {{scope_summary}} | Campaign: {{campaign_verdict}} ({{confidence}})
Kill chain: {{earliest_tactic}} through {{latest_tactic}} | Objective: {{objective}}

**Select an option:**
[A] Advanced Elicitation — Challenge correlation assumptions and kill chain gaps
[W] War Room — Red vs Blue discussion on campaign assessment and adversary intent
[C] Continue — Proceed to Classification and Priority Assignment (Step 5 of 7)"

#### Menu Handling Logic:

- IF A: Deep-dive correlation analysis — challenge whether correlated alerts are truly related or coincidentally similar, investigate kill chain gaps for potential undetected activity, stress-test the campaign verdict by examining alternative explanations, evaluate whether the adversary objective assessment is supported by evidence or assumption. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: if I were the attacker, would this correlation reveal my full operation or just the tip? What am I doing that is NOT being detected? Are the kill chain gaps where I am operating undetected? Blue Team perspective: are we over-correlating unrelated events? Is the campaign verdict premature? Do the kill chain gaps represent real blind spots or is the attacker simply not at those stages? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `mitre_techniques` with all mapped technique T-codes, then read fully and follow: ./step-05-classification.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, mitre_techniques updated with all mapped T-codes, and correlation analysis appended to report under `## Correlation and Kill Chain`], will you then read fully and follow: `./step-05-classification.md` to begin classification and priority assignment.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All five correlation dimensions searched (host, user, source IP, IOCs, technique)
- Related alerts presented with relationship type, evidence, and confidence for each connection
- All alerts (original + correlated) mapped to ATT&CK techniques with tactic and confidence level
- Kill chain plotted with detected tactics clearly marked
- Gap analysis completed identifying potential undetected activity between detected stages
- Attack progression type assessed (linear, scattered, late-stage, early-stage)
- Campaign verdict selected with specific evidence justification
- Adversary objective assessed based on kill chain position
- Key correlation finding articulated — what correlation revealed beyond the individual alert
- Frontmatter updated with mitre_techniques array and step added to stepsCompleted
- Findings appended to report under `## Correlation and Kill Chain`
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Correlating alerts without evidence linking them (shared IOC, host, user, or temporal proximity)
- Over-correlating unrelated alerts into a false campaign narrative
- Mapping ATT&CK techniques based on speculation rather than observed behavior
- Skipping kill chain gap analysis — gaps are critical for understanding detection blind spots
- Treating absence of correlated alerts as proof the event is isolated
- Assigning a campaign verdict without supporting evidence
- Beginning containment, response, or escalation during correlation analysis
- Not updating mitre_techniques in frontmatter with all mapped T-codes
- Proceeding to classification without completing kill chain mapping
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Correlation transforms individual alerts into operational intelligence — every connection must be evidence-based, every gap must be analyzed, and the campaign assessment must be justified.
