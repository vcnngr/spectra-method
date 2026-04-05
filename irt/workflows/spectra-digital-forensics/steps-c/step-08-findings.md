# Step 8: Findings Consolidation & IOC Summary

**Progress: Step 8 of 10** — Next: Expert Opinion & Legal Considerations

## STEP GOAL:

Consolidate findings from ALL analysis phases into a unified findings set classified by severity, cross-referenced by attack chain, and supported by evidence citations. Compile all IOCs extracted across all phases into a categorized, TLP-classified IOC summary. Perform root cause analysis to identify the fundamental weakness that enabled the attack. Determine the complete scope of compromise — affected systems, accounts, and data. This step transforms analysis outputs into actionable intelligence.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER present a finding without evidence citation — every finding must reference specific EVD IDs
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous analysis engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst consolidating investigation findings under ISO 27037 and NIST SP 800-86
- ✅ Findings consolidation is where the investigation's conclusions take shape — individual artifacts become coherent findings, and findings chain together into the complete attack narrative
- ✅ Every finding must be defensible — if you cannot cite the evidence, it is an opinion, not a finding; opinions belong in step 9
- ✅ IOC compilation serves two purposes: immediate detection (feed to SIEM/EDR) and intelligence sharing (feed to ISACs/FIRST)
- ✅ Root cause analysis goes deeper than "how did they get in" — it identifies the systemic weakness that must be fixed

### Step-Specific Rules:

- 🎯 Focus exclusively on findings consolidation, IOC compilation, root cause analysis, and scope determination
- 🚫 FORBIDDEN to perform new forensic analysis — work only with findings from steps 3-7
- 🚫 FORBIDDEN to render expert opinions — that is step 9
- 💬 Approach: Systematic consolidation with severity classification, evidence cross-referencing, and IOC categorization
- 📊 Every finding must have: description, evidence sources (EVD IDs), confidence level, ATT&CK technique, timeline position, impact
- 🔒 IOCs must be categorized by type, tagged with TLP classification, and include context

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Classifying a finding as "Informational" when it demonstrates active compromise (code injection, credential theft, C2 communication) understates the severity and may cause downstream responders to deprioritize critical remediation — severity should reflect actual impact, not comfort level
  - Not linking related findings into attack chains produces a list of isolated observations rather than a coherent narrative — the value of findings consolidation is showing how individual artifacts connect to form the complete attack story; isolated findings cannot answer the forensic question
  - Publishing IOCs without TLP classification risks inappropriate dissemination — IOCs extracted from a privileged investigation may contain information that identifies the victim, the investigation, or sensitive technical details; TLP classification ensures IOCs are shared only to appropriate audiences
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Review ALL findings from steps 3-7 before beginning consolidation
- 📋 Classify every finding by severity with documented justification
- 🔒 Cite evidence IDs for every finding — no unsupported claims
- ⚠️ Present [A]/[W]/[C] menu after consolidation is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to stepsCompleted and updating all findings/IOC counters
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: ALL findings from steps 3-7, timeline, ATT&CK mapping, evidence inventory, case intake data
- Focus: Findings consolidation, IOC compilation, root cause analysis, scope determination
- Limits: Work with existing findings only. Expert opinions and legal analysis belong in step 9.
- Dependencies: Completed analysis from steps 3-7 and timeline from step 7

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Findings Consolidation

Merge findings from ALL analysis phases, classify by severity, and cross-reference into attack chains.

**Severity Classification Criteria:**

| Severity | Criteria | Examples |
|----------|----------|----------|
| **Critical** | Active compromise with confirmed data exfiltration, credential theft of privileged accounts, rootkit or kernel compromise, active C2 with attacker control | Confirmed exfiltration of customer PII, Domain Admin credentials stolen, kernel rootkit installed, live C2 channel active |
| **High** | Confirmed unauthorized access, malware execution, persistence established, lateral movement achieved, unprivileged credential theft | Attacker has shell access, malware executing, persistence via scheduled task, moved to 3+ systems, standard user credentials stolen |
| **Medium** | Suspicious activity with probable compromise, policy violations with security impact, evidence of reconnaissance or preparation | Suspicious process execution, unauthorized tool installation, enumeration activity, policy violation enabling attack |
| **Low** | Minor security issues, incomplete attack attempts, indicators without confirmed compromise | Failed exploitation attempts, incomplete reconnaissance, minor misconfigurations |
| **Informational** | Contextual observations, normal activity of interest, baseline deviations without security impact | Unusual but authorized activity, system changes within normal operations, environmental observations |

**Per-Finding Record:**

```
| Field | Value |
|-------|-------|
| Finding ID | FND-{case_id}-{NNN} |
| Title | {{concise finding title}} |
| Severity | Critical/High/Medium/Low/Informational |
| Description | {{detailed description of what was found}} |
| Evidence Sources | EVD-{case_id}-{list of relevant EVD IDs} |
| Analysis Phase | Disk/Memory/Network/Cloud/Timeline |
| Confidence | Confirmed/Probable/Possible |
| ATT&CK Technique | {{T-code(s) and name(s)}} |
| Timeline Position | {{timestamp or range from master timeline}} |
| Affected Systems | {{system list}} |
| Affected Accounts | {{account list}} |
| Impact | {{specific impact of this finding}} |
| Related Findings | FND-{case_id}-{related FND IDs} |
```

**Consolidated Findings Table:**

```
| # | FND ID | Title | Severity | Evidence Sources | Confidence | ATT&CK | Timeline | Impact |
|---|--------|-------|----------|------------------|------------|--------|----------|--------|
| 1 | FND-{case_id}-001 | {{title}} | {{severity}} | EVD-{case_id}-XXX | {{confidence}} | {{T-code}} | {{timestamp}} | {{impact}} |
```

**Attack Chain Cross-Reference:**

Link related findings into coherent attack chains:

```
Attack Chain 1: {{chain name — e.g., "Initial Access through Data Exfiltration"}}
  FND-{case_id}-001 → FND-{case_id}-003 → FND-{case_id}-007 → FND-{case_id}-012 → FND-{case_id}-018
  
  {{narrative connecting the findings in causal sequence}}
```

Present findings by attack chain (grouped) AND by severity (sorted):

**Findings by Severity:**
```
Critical: {{count}} findings
High: {{count}} findings
Medium: {{count}} findings
Low: {{count}} findings
Informational: {{count}} findings
Total: {{count}} findings
```

### 2. IOC Summary

Compile all IOCs extracted across ALL analysis phases into a categorized summary:

**File Hash IOCs:**

```
| # | Hash Type | Hash Value | Filename | Context | First Seen | Last Seen | Source Phase | EVD ID | Confidence | TLP |
|---|-----------|------------|----------|---------|------------|-----------|-------------|--------|------------|-----|
| 1 | MD5/SHA-256/SHA-1 | {{hash}} | {{filename}} | {{where and why this file matters}} | {{timestamp}} | {{timestamp}} | Disk/Memory | EVD-{case_id}-XXX | {{confidence}} | {{TLP:CLEAR/GREEN/AMBER/AMBER+STRICT/RED}} |
```

**IP Address IOCs:**

```
| # | IP Address | Port(s) | Direction | Context | First Seen | Last Seen | Source Phase | EVD ID | Confidence | TLP |
|---|------------|---------|-----------|---------|------------|-----------|-------------|--------|------------|-----|
| 1 | {{ip}} | {{ports}} | Inbound/Outbound/Both | {{C2/exfil/scanning/lateral}} | {{timestamp}} | {{timestamp}} | Network/Cloud | EVD-{case_id}-XXX | {{confidence}} | {{TLP}} |
```

**Domain IOCs:**

```
| # | Domain | Resolution(s) | Context | First Seen | Last Seen | Registration | Source Phase | EVD ID | Confidence | TLP |
|---|--------|---------------|---------|------------|-----------|--------------|-------------|--------|------------|-----|
| 1 | {{domain}} | {{IPs}} | {{C2/phishing/exfil/DGA}} | {{timestamp}} | {{timestamp}} | {{reg_date}} | Network/DNS | EVD-{case_id}-XXX | {{confidence}} | {{TLP}} |
```

**URL IOCs:**

```
| # | URL | Context | First Seen | Last Seen | Source Phase | EVD ID | Confidence | TLP |
|---|-----|---------|------------|-----------|-------------|--------|------------|-----|
| 1 | {{url}} | {{download/C2/exfil/phishing}} | {{timestamp}} | {{timestamp}} | Network/Proxy | EVD-{case_id}-XXX | {{confidence}} | {{TLP}} |
```

**Email Address IOCs:**

```
| # | Email | Context | First Seen | Source Phase | EVD ID | Confidence | TLP |
|---|-------|---------|------------|-------------|--------|------------|-----|
| 1 | {{email}} | {{phishing sender/attacker account}} | {{timestamp}} | Disk/Cloud | EVD-{case_id}-XXX | {{confidence}} | {{TLP}} |
```

**Registry Key IOCs (Windows):**

```
| # | Registry Path | Value | Context | First Seen | Source Phase | EVD ID | Confidence | TLP |
|---|---------------|-------|---------|------------|-------------|--------|------------|-----|
| 1 | {{path}} | {{value}} | {{persistence/configuration}} | {{timestamp}} | Disk | EVD-{case_id}-XXX | {{confidence}} | {{TLP}} |
```

**Mutex/Event IOCs:**

```
| # | Name | Type | Context | Process | Source Phase | EVD ID | Confidence | TLP |
|---|------|------|---------|---------|-------------|--------|------------|-----|
| 1 | {{name}} | Mutex/Event/Named Pipe | {{malware identifier/C2}} | {{process}} | Memory | EVD-{case_id}-XXX | {{confidence}} | {{TLP}} |
```

**YARA Signatures:**
- Include any custom YARA rules developed during the investigation
- Reference existing YARA rules that matched during analysis

**Behavioral IOCs:**

```
| # | Behavior | Description | ATT&CK Technique | Detection Logic (Sigma/YARA/Custom) | Confidence | TLP |
|---|----------|-------------|-------------------|--------------------------------------|------------|-----|
| 1 | {{behavior}} | {{description}} | {{T-code}} | {{detection_logic}} | {{confidence}} | {{TLP}} |
```

**IOC Summary Statistics:**
```
Total unique IOCs: {{count}}
  File hashes: {{count}}
  IP addresses: {{count}}
  Domains: {{count}}
  URLs: {{count}}
  Email addresses: {{count}}
  Registry keys: {{count}}
  Mutexes/events: {{count}}
  YARA signatures: {{count}}
  Behavioral indicators: {{count}}
TLP distribution:
  TLP:RED: {{count}} (restricted to investigation team)
  TLP:AMBER+STRICT: {{count}} (organization only)
  TLP:AMBER: {{count}} (organization + clients)
  TLP:GREEN: {{count}} (community sharing)
  TLP:CLEAR: {{count}} (public)
```

### 3. Root Cause Analysis

Determine the initial compromise vector and the fundamental weakness:

**Initial Access Vector:**
- What was the first confirmed attacker activity in the timeline?
- What entry point was used? (cite specific evidence)
- Was there reconnaissance activity preceding initial access?

**Enabling Vulnerability:**
- What specific weakness was exploited?
  - Software vulnerability: CVE, affected software, patch status
  - Configuration weakness: misconfiguration details, secure configuration standard
  - Credential weakness: weak password, reuse, no MFA, exposed
  - Human factor: social engineering, policy violation, insufficient training
  - Process gap: missing patching, inadequate access review

**Root Cause Chain:**

```
Proximate Cause: {{the immediate action — e.g., phishing email clicked, vulnerability exploited}}
    ↓ enabled by
Intermediate Cause: {{the condition — e.g., no email filtering, unpatched software, weak password}}
    ↓ enabled by
Root Cause: {{the fundamental weakness — e.g., no patch management program, no MFA enforcement, no security awareness training}}
```

**Contributing Factors:**
- What other conditions made the attack possible or easier?
- Were compensating controls absent, misconfigured, or bypassed?
- Was this a known risk that was accepted?

**Prevention Assessment:**
- What security control would have prevented the initial access?
- What detection control would have caught the attack earlier?
- What response capability would have limited the scope?

### 4. Scope Determination

Using the consolidated findings and timeline, determine the complete blast radius:

**Affected Systems:**

```
| # | System | Hostname | IP | OS | Role | Compromise Type | First Activity | Last Activity | Findings | Confidence |
|---|--------|----------|-----|-----|------|-----------------|----------------|---------------|----------|------------|
| 1 | {{system}} | {{host}} | {{ip}} | {{os}} | {{role}} | Initial Access/Lateral/C2/Persistence | {{timestamp}} | {{timestamp}} | FND-{case_id}-XXX | Confirmed/Suspected |
```

**Compromised Accounts:**

```
| # | Account | Type | Privilege | Compromise Method | First Misuse | Last Misuse | Findings | Confidence |
|---|---------|------|-----------|-------------------|--------------|-------------|----------|------------|
| 1 | {{account}} | User/Service/Admin/Machine | {{level}} | {{method}} | {{timestamp}} | {{timestamp}} | FND-{case_id}-XXX | Confirmed/Suspected |
```

**Data Exposure Assessment:**

```
| # | Data Repository | Type | Classification | Access Type | Volume | Exfiltration Evidence | Findings | Confidence |
|---|----------------|------|----------------|-------------|--------|----------------------|----------|------------|
| 1 | {{repo}} | File Share/DB/Email/Cloud | {{PII/PHI/PCI/IP/Financial}} | Read/Write/Delete/Exfiltrate | {{volume}} | {{yes/no/unknown}} | FND-{case_id}-XXX | Confirmed/Suspected |
```

**Scope Summary:**
```
Systems confirmed compromised: {{count}}
Systems suspected compromised: {{count}}
Accounts confirmed compromised: {{count}}
Accounts suspected compromised: {{count}}
Data repositories accessed: {{count}}
Data confirmed exfiltrated: {{yes/no/suspected}}
Data volume at risk: {{volume}}
Regulatory data affected: {{yes — list frameworks / no}}
```

### 5. Append Findings to Report

Write all consolidated findings under `## Findings & Artifacts` and `## IOC Summary` in the output file `{outputFile}`:

```markdown
## Findings & Artifacts

### Consolidated Findings
{{findings_table_by_severity}}

### Attack Chain Reconstruction
{{attack_chains_with_finding_references}}

### Root Cause Analysis
{{root_cause_chain}}
{{contributing_factors}}
{{prevention_assessment}}

### Scope Determination
#### Affected Systems
{{systems_table}}

#### Compromised Accounts
{{accounts_table}}

#### Data Exposure Assessment
{{data_exposure_table}}

## IOC Summary

### File Hash IOCs
{{hash_iocs_table}}

### Network IOCs
{{ip_domain_url_tables}}

### Host IOCs
{{registry_mutex_tables}}

### Behavioral IOCs
{{behavioral_iocs_table}}
```

Update frontmatter:
- Add this step name (`Findings Consolidation & IOC Summary`) to the end of `stepsCompleted`
- Set `findings_count` to total findings
- Update `findings_by_severity` with counts per severity
- Set `iocs_extracted` to total unique IOC count
- Update `iocs_by_type` with per-type counts
- Set `root_cause` to one-line root cause summary
- Set `attack_vector` to initial access technique
- Update `persistence_mechanisms` count
- Update `lateral_movement_detected` and `data_exfiltration_detected` from scope determination

### 6. Present MENU OPTIONS

"**Findings consolidation and IOC compilation complete.**

Findings: {{total_count}} ({{critical}} critical, {{high}} high, {{medium}} medium, {{low}} low, {{info}} informational)
Attack chains identified: {{chain_count}}
Root cause: {{root_cause_one_liner}}
IOCs compiled: {{ioc_total}} ({{hash_count}} hashes, {{ip_count}} IPs, {{domain_count}} domains, {{url_count}} URLs, {{behavioral_count}} behavioral)
Systems compromised: {{system_count}} ({{confirmed}} confirmed, {{suspected}} suspected)
Accounts compromised: {{account_count}} ({{confirmed}} confirmed, {{suspected}} suspected)
Data exfiltration: {{exfil_status}}

**Select an option:**
[A] Advanced Elicitation — Challenge findings severity classifications, question root cause depth, identify missing IOCs, stress-test scope completeness
[W] War Room — Red (are the findings accurate? did the analyst miss any of my activities? is the scope determination complete or did I compromise systems they have not found? are all my IOCs in their list?) vs Blue (are the findings defensible under cross-examination? is the root cause truly the root cause or just the most visible failure? are we confident the scope is complete? will our IOC list enable detection of related future attacks?)
[C] Continue — Proceed to Step 9: Expert Opinion & Legal Considerations (Step 9 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the consolidation. Are severity classifications consistent and justified? Is the root cause analysis deep enough, or does it stop at the proximate cause? Are there IOCs that should have been extracted but were missed? Is the scope determination complete or could the attacker have accessed systems without leaving detectable traces? Are the attack chains complete or are there gaps in the causal logic? Process insights, redisplay menu
- IF W: War Room — Red Team: the findings list captures most of my activities, but did they find my dormant backdoor? Did they identify all the accounts I compromised, including the service account I created? Is their IOC list complete enough to detect me if I attack again with different infrastructure but same TTPs? Blue Team: are these findings court-ready? Can every finding withstand "show me the evidence"? Is the root cause actionable? Will the scope determination survive independent verification? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated and this step added to stepsCompleted. Then read fully and follow: ./step-09-expert-opinion.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, findings_count, findings_by_severity, iocs_extracted, iocs_by_type, root_cause, attack_vector all updated, and Findings & Artifacts and IOC Summary sections populated], will you then read fully and follow: `./step-09-expert-opinion.md` to formulate expert opinion and address legal considerations.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Findings merged from ALL analysis phases (disk, memory, network, cloud, timeline)
- Every finding classified by severity with documented justification
- Every finding cites specific evidence sources (EVD IDs) and confidence level
- Related findings cross-referenced into attack chains with narrative
- IOCs compiled from ALL phases, categorized by type, with context and TLP classification
- Root cause identified as a chain from proximate to fundamental weakness with evidence
- Complete scope determination: systems, accounts, and data repositories affected
- Data exfiltration status determined (confirmed/suspected/not detected)
- Finding IDs (FND-{case_id}-{NNN}) assigned for traceability
- Frontmatter updated with all findings and IOC counters
- Findings and IOC Summary sections populated in output document

### ❌ SYSTEM FAILURE:

- Presenting findings without evidence citations
- Not classifying findings by severity
- Not linking related findings into attack chains
- Not compiling IOCs from ALL analysis phases
- IOCs without TLP classification
- Root cause analysis stopping at proximate cause without identifying fundamental weakness
- Scope determination missing systems, accounts, or data repositories identified in analysis
- Rendering expert opinions in this step (belongs to step 9)
- Performing new forensic analysis during this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Findings consolidation is where analysis becomes actionable. Every finding must be evidenced. Every IOC must be categorized. Root cause must be fundamental. Scope must be complete. This is the foundation for expert opinion and the forensic report.
