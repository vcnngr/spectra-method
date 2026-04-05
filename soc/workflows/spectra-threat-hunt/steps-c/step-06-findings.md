# Step 6: Finding Analysis & Validation

**Progress: Step 6 of 8** — Next: Detection Engineering

## STEP GOAL:

Correlate all findings from automated (step 4) and manual (step 5) analysis, build evidence chains for each finding, assign final classification (Confirmed Malicious, Suspicious, Benign Anomaly, False Positive) with confidence levels, map validated findings to ATT&CK techniques at the procedure level, assess business impact, and validate or refute each hypothesis. This is the judgment step — all analysis converges here into validated, classified findings with full evidence chains.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER classify a finding without documented evidence chain and reasoning
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A THREAT HUNTER rendering final analytical judgment on hunt findings
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Threat Hunter validating findings — this is where hypotheses are confirmed, refuted, or declared inconclusive
- ✅ Every classification must be backed by an evidence chain — correlation across data sources increases confidence, single-source evidence decreases it
- ✅ "Confirmed Malicious" requires corroboration from multiple independent data sources with alternative explanations eliminated
- ✅ "Not Found" is a valid and valuable outcome — a well-executed hunt that finds nothing has still reduced uncertainty
- ✅ Unexpected findings (things discovered outside any hypothesis) are often the most valuable — document them with the same rigor as hypothesis-driven findings

### Step-Specific Rules:

- 🎯 Focus exclusively on evidence correlation, finding classification, ATT&CK mapping, impact assessment, and hypothesis validation
- 🚫 FORBIDDEN to perform new queries or additional data collection — use only the evidence already gathered in steps 4-5
- 🚫 FORBIDDEN to begin detection engineering or rule creation — that is step 7
- 💬 Approach: Rigorous evidence-based classification with explicit confidence levels and alternative explanation assessment
- 📊 Every finding must have: evidence chain, classification, confidence level, ATT&CK mapping, and reasoning
- 🔒 Classifications must be defensible — would another analyst reach the same conclusion from this evidence?

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Classifying a finding as "Confirmed Malicious" based on a single data source without corroboration creates risk of false attribution — single-source evidence should be classified as "Suspicious" at most unless the evidence is unambiguous (e.g., known C2 beacon with matching JA3 hash, process injection into lsass.exe with known Mimikatz patterns). Recommend seeking corroboration before confirming.
  - Classifying all "Not Found" hypotheses as "refuted" without verifying data source completeness conflates absence of evidence with evidence of absence — verify that logging was active, retention was sufficient, and queries were syntactically correct before accepting refutation. If any of these conditions are not met, classify as "Inconclusive" instead.
  - Reporting confirmed malicious findings without immediate notification to incident response may allow adversary activity to continue during the time between finding validation and report delivery — if confirmed malicious activity is found, recommend immediate parallel notification to the incident response team while continuing the hunt workflow.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present evidence correlation before assigning classifications
- ⚠️ Present [A]/[W]/[C] menu after all findings validated and hypotheses assessed
- 💾 ONLY save to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to stepsCompleted and updating findings counts, hypothesis counts
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Hunt mission, hypotheses, automated findings, manual analysis assessments, baselines from steps 1-5
- Focus: Evidence correlation, finding classification, ATT&CK mapping, impact assessment, hypothesis validation — no new data collection or detection engineering
- Limits: Only classify findings already investigated in steps 4-5 — do not introduce new entities
- Dependencies: Completed manual analysis from step-05-manual-analysis.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Evidence Correlation

Cross-reference all findings from automated (step 4) and manual (step 5) analysis:

"**Evidence Correlation Matrix:**

#### A. Finding-to-Finding Correlation

| Finding A | Finding B | Correlation Type | Shared Element | Temporal Proximity | Significance |
|-----------|-----------|-----------------|---------------|-------------------|-------------|
| AF-001 | AF-003 | Same host | {{hostname}} | {{minutes/hours apart}} | {{Strong — same attack chain / Moderate — possible relation / Weak — coincidental}} |
| AF-002 | AF-005 | Same user | {{username}} | {{time difference}} | {{significance}} |
| AF-001 | AF-004 | Same time window | {{overlapping period}} | {{concurrent}} | {{significance}} |
| ... | ... | ... | ... | ... | ... |

**Correlation clusters:**
- **Cluster 1:** {{findings that correlate — e.g., AF-001 + AF-003 + AF-006 form an attack chain on HOST-A}}
- **Cluster 2:** {{findings that correlate — e.g., AF-002 + AF-005 involve USER-B across multiple hosts}}
- **Uncorrelated findings:** {{findings with no cross-references — investigate whether isolation is itself significant}}

#### B. Evidence Chain Construction

For each cluster or significant finding, construct the evidence chain:

"**Evidence Chain EC-1: {{descriptive name}}**

```
Timeline:
{{timestamp_1}} — [{{data_source_1}}] {{finding_description_1}} (AF-001)
    └─ Evidence: {{specific log entry, process event, network connection}}
{{timestamp_2}} — [{{data_source_2}}] {{finding_description_2}} (AF-003)
    └─ Evidence: {{specific log entry, process event, network connection}}
{{timestamp_3}} — [{{data_source_3}}] {{finding_description_3}} (AF-006)
    └─ Evidence: {{specific log entry, process event, network connection}}

Data source corroboration: {{count}} independent sources confirm this chain
Alternative explanation: {{what legitimate scenario could produce this same chain?}}
Alternative probability: {{High (likely legitimate) / Low (unlikely to be coincidental) / None (no legitimate explanation)}}
```"

### 2. Finding Classification

For each finding (or finding cluster), assign the final classification:

"**Finding Classification:**

---

**Finding F-001: {{descriptive name}}**

| Classification Field | Detail |
|---------------------|--------|
| **Finding ID** | F-001 (composed of automated findings: {{AF-xxx, AF-yyy}}) |
| **Classification** | 🔴 Confirmed Malicious / 🟠 Suspicious / 🟡 Benign Anomaly / ⚪ False Positive |
| **Confidence Level** | **High** (corroborated by {{count}} independent data sources, alternative explanations eliminated) / **Medium** (single strong data source, strong indicators, some alternatives remain) / **Low** (circumstantial, requires further investigation) |
| **Evidence Chain** | EC-{{n}} — {{brief chain summary}} |
| **Data Sources** | {{list of data sources contributing evidence}} |
| **Corroboration** | {{count}} independent sources confirm — {{list sources}} |
| **Alternative Explanations** | {{list considered alternatives and why they were accepted/rejected}} |
| **First Activity** | {{earliest timestamp in chain}} |
| **Last Activity** | {{latest timestamp in chain}} |
| **Duration** | {{time span of activity}} |
| **Affected Systems** | {{hosts, IPs, endpoints}} |
| **Affected Users** | {{usernames, accounts}} |
| **Hypothesis Link** | {{which hypothesis this finding supports/refutes}} |

**Classification Reasoning:**
{{Detailed explanation of why this classification was assigned. This is the intellectual output — another analyst should be able to follow this reasoning and reach the same conclusion.}}

---

**Finding F-002: {{descriptive name}}**
{{Repeat classification structure for each finding}}

---"

### 3. ATT&CK Technique Mapping (for Confirmed/Suspicious findings)

"**ATT&CK Mapping — Validated Findings:**

| Finding | Technique ID | Technique Name | Tactic | Sub-technique | Platform | Procedure Detail |
|---------|-------------|---------------|--------|---------------|----------|-----------------|
| F-001 | {{T-code}} | {{name}} | {{tactic}} | {{sub-technique or N/A}} | {{platform}} | {{how specifically was this technique executed — tool, command, method}} |
| F-001 | {{T-code}} | {{name}} | {{tactic}} | {{sub-technique}} | {{platform}} | {{procedure detail}} |
| F-002 | {{T-code}} | {{name}} | {{tactic}} | {{sub-technique}} | {{platform}} | {{procedure detail}} |
| ... | ... | ... | ... | ... | ... | ... |

**Kill Chain Coverage:**
```
{{Map findings across the kill chain:}}

Reconnaissance    → [{{covered/gap}}] {{findings if any}}
Resource Dev      → [{{covered/gap}}] {{findings if any}}
Initial Access    → [{{covered/gap}}] {{findings if any}}
Execution         → [{{covered/gap}}] {{findings if any}}
Persistence       → [{{covered/gap}}] {{findings if any}}
Priv Escalation   → [{{covered/gap}}] {{findings if any}}
Defense Evasion   → [{{covered/gap}}] {{findings if any}}
Credential Access → [{{covered/gap}}] {{findings if any}}
Discovery         → [{{covered/gap}}] {{findings if any}}
Lateral Movement  → [{{covered/gap}}] {{findings if any}}
Collection        → [{{covered/gap}}] {{findings if any}}
C2                → [{{covered/gap}}] {{findings if any}}
Exfiltration      → [{{covered/gap}}] {{findings if any}}
Impact            → [{{covered/gap}}] {{findings if any}}
```

**Techniques confirmed present:** {{count}} techniques across {{count}} tactics
**Kill chain stages observed:** {{count}} / 14 tactics
**Deepest penetration:** {{furthest tactic in the chain — indicates adversary progress}}"

### 4. Impact Assessment (for Confirmed Malicious findings)

"**Impact Assessment:**

| Impact Dimension | Assessment | Detail |
|-----------------|-----------|--------|
| **Affected systems** | {{count}} systems | {{list with criticality ratings}} |
| **Affected users** | {{count}} accounts | {{list with privilege levels}} |
| **Data exposure risk** | {{None / Low / Medium / High / Critical}} | {{what data was accessible or potentially exfiltrated}} |
| **Lateral movement extent** | {{None / Limited / Moderate / Widespread}} | {{how far the adversary moved in the network}} |
| **Persistence established** | {{None / Single mechanism / Multiple mechanisms}} | {{what persistence was found and where}} |
| **Credential compromise** | {{None / Local accounts / Domain accounts / Privileged accounts}} | {{what credentials are at risk}} |
| **Business impact** | {{None / Low / Medium / High / Critical}} | {{impact on business operations, data integrity, reputation}} |
| **Containment urgency** | {{Immediate / Soon (24h) / Planned / Monitoring only}} | {{recommended urgency based on adversary activity state}} |

**Recommended Immediate Actions (if confirmed malicious):**
1. {{action 1 — e.g., "Isolate HOST-A from network — confirmed C2 communication"}}
2. {{action 2 — e.g., "Reset credentials for USER-B — confirmed credential access"}}
3. {{action 3 — e.g., "Block outbound to IP X.X.X.X — confirmed exfiltration destination"}}
4. {{action 4 — e.g., "Notify incident response team — handoff to spectra-incident-handling"}}

**CRITICAL:** If confirmed malicious activity with ongoing risk is found, recommend immediate notification to incident response IN PARALLEL with continuing this hunt workflow. Do not wait for hunt completion to escalate active threats."

### 5. Hypothesis Validation

For each hypothesis from step 2, present the final verdict:

"**Hypothesis Validation:**

---

**Hypothesis H1: {{descriptive name}}**

| Verdict Field | Detail |
|--------------|--------|
| **Hypothesis** | "If {{threat actor/technique}} is present in {{environment}}, then we expect to observe {{observable}} in {{data source}}" |
| **Verdict** | ✅ Confirmed / ❌ Refuted / ⚠️ Inconclusive |
| **Supporting Findings** | {{list of findings that support or refute}} |
| **Evidence Strength** | {{Strong (multi-source) / Moderate (single strong source) / Weak (circumstantial) / None}} |
| **Data Source Completeness** | {{All required sources available / Some gaps / Critical gaps}} |
| **Reasoning** | {{Why this verdict — what evidence confirmed/refuted, or what data was missing for inconclusive}} |

**{{If Confirmed:}}** The hypothesis is supported by findings {{list}} with {{confidence}} confidence. This indicates {{interpretation of what confirmed presence means for the organization}}.

**{{If Refuted:}}** The hypothesis was tested against {{count}} data sources over {{time period}} with {{count}} queries. No evidence was found supporting the presence of {{technique/actor}}. Data source completeness was verified as {{complete/partial}}. {{If complete: This provides reasonable assurance that this specific technique was not active during the hunt window. If partial: The refutation is qualified by data gaps — see Inconclusive recommendations.}}

**{{If Inconclusive:}}** The hypothesis could not be fully tested due to: {{list of gaps — missing data source, insufficient retention, ambiguous results}}. To resolve, the following would be needed: {{specific remediation — add data source, extend retention, deploy additional logging}}.

---

**Hypothesis H2: {{descriptive name}}**
{{Repeat validation structure}}

---

**Unexpected Findings:**
{{Findings discovered during the hunt that were not part of any predefined hypothesis — these are often the most valuable}}

| Finding | Description | Relevance | Recommended Action |
|---------|-------------|-----------|-------------------|
| UF-001 | {{what was found outside hypothesis scope}} | {{why it matters}} | {{investigate further / create new hypothesis / monitor / escalate}} |

---

**Hypothesis Validation Summary:**

| Hypothesis | Verdict | Confidence | Key Finding(s) |
|-----------|---------|-----------|---------------|
| H1 | ✅ / ❌ / ⚠️ | {{High/Medium/Low}} | {{brief}} |
| H2 | ✅ / ❌ / ⚠️ | {{High/Medium/Low}} | {{brief}} |
| ... | ... | ... | ... |

Total hypotheses: {{count}}
├── Confirmed: {{count}}
├── Refuted: {{count}}
└── Inconclusive: {{count}}

Unexpected findings: {{count}}"

### 6. Validated Findings Summary

"**Validated Findings — Final Summary:**

| # | Finding ID | Description | Classification | Confidence | ATT&CK | Impact | Evidence Sources |
|---|-----------|-------------|---------------|-----------|--------|--------|-----------------|
| 1 | F-001 | {{brief description}} | 🔴 Confirmed Malicious | {{High/Medium/Low}} | {{T-codes}} | {{impact}} | {{count}} sources |
| 2 | F-002 | {{brief description}} | 🟠 Suspicious | {{High/Medium/Low}} | {{T-codes}} | {{potential impact}} | {{count}} sources |
| 3 | F-003 | {{brief description}} | 🟡 Benign Anomaly | {{High/Medium/Low}} | N/A | None | {{count}} sources |
| 4 | F-004 | {{brief description}} | ⚪ False Positive | {{High/Medium/Low}} | N/A | None | {{count}} sources |
| ... | ... | ... | ... | ... | ... | ... | ... |

**Finding Statistics:**
```
Total findings validated: {{count}}
├── Confirmed Malicious: {{count}}
├── Suspicious: {{count}}
├── Benign Anomaly: {{count}}
└── False Positive: {{count}}

ATT&CK techniques confirmed: {{count}} across {{count}} tactics
Evidence chains constructed: {{count}}
Cross-source corroborations: {{count}}
Immediate actions recommended: {{count}}
```"

### 7. Present MENU OPTIONS

"**Finding analysis and validation complete.**

Summary: {{findings_total}} findings validated — {{confirmed}} confirmed malicious, {{suspicious}} suspicious, {{benign}} benign, {{fp}} false positive.
Hypotheses: {{confirmed_count}} confirmed, {{refuted_count}} refuted, {{inconclusive_count}} inconclusive.
ATT&CK coverage: {{technique_count}} techniques across {{tactic_count}} tactics confirmed.
{{If confirmed malicious: **ALERT:** Confirmed malicious activity found — recommend immediate incident response notification.}}

**Select an option:**
[A] Advanced Elicitation — Challenge classifications, explore alternative evidence interpretations, strengthen evidence chains
[W] War Room — Red vs Blue discussion on validated findings and organizational impact
[C] Continue — Proceed to Detection Engineering (Step 7 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive validation — challenge "Confirmed Malicious" classifications (is the evidence truly unambiguous?), challenge "Refuted" hypotheses (could the adversary have evaded our detection?), explore whether "Suspicious" findings could be elevated with additional context from the operator, identify correlations between unexpected findings and hypotheses that may have been missed. Process insights, ask user if they want to update classifications, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: looking at these validated findings, how would I assess the adversary's skill level? If my operation was partially detected, what's my next move? Which "refuted" hypotheses would I test differently? What detection improvements from this hunt would most impact future Red Team operations? Blue Team perspective: are our classifications defensible? Would another analyst reach the same conclusion? What's the organizational risk if the "suspicious" findings are actually malicious? How do we handle the "inconclusive" hypotheses — accept risk or invest in capability? What detection rules would have caught these findings earlier? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `findings_total`, `findings_confirmed_malicious`, `findings_suspicious`, `findings_benign`, `false_positives_identified`, `hypotheses_confirmed`, `hypotheses_refuted`, `hypotheses_inconclusive`. Append validated findings to report under `## Validated Findings`. Then read fully and follow: ./step-07-detection-engineering.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and all finding/hypothesis counts updated, and validated findings appended to report under `## Validated Findings`], will you then read fully and follow: `./step-07-detection-engineering.md` to begin detection engineering.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Evidence correlation performed across all findings with cross-reference matrix
- Evidence chains constructed for all significant findings with timeline, data sources, and alternative explanations
- Every finding classified with documented evidence chain, confidence level, and reasoning
- Classifications defensible — another analyst could reach the same conclusion from the documented evidence
- ATT&CK mapping completed at procedure level for all confirmed/suspicious findings
- Kill chain coverage mapped showing observed and gap stages
- Impact assessment performed for confirmed malicious findings with affected systems, users, data exposure, and recommended actions
- Every hypothesis validated with verdict (Confirmed/Refuted/Inconclusive) and supporting evidence
- "Not Found" and "Inconclusive" properly distinguished based on data source completeness
- Unexpected findings documented with same rigor as hypothesis-driven findings
- Validated findings summary table produced with all findings, classifications, and statistics
- All validated findings appended to report under `## Validated Findings`
- Frontmatter updated with all finding/hypothesis counts and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Classifying findings without documented evidence chains and reasoning
- "Confirmed Malicious" classification based on single data source without corroboration
- Confusing "Not Found" (evidence of absence) with "Inconclusive" (absence of evidence)
- Not mapping confirmed/suspicious findings to ATT&CK at procedure level
- Not assessing business impact for confirmed malicious findings
- Not recommending immediate actions for confirmed active threats
- Not validating every hypothesis with explicit verdict
- Ignoring unexpected findings discovered outside hypothesis scope
- Performing new data collection or queries during validation
- Beginning detection rule creation during this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every finding must be classified with evidence. Every hypothesis must be validated with a verdict. The distinction between "Not Found" and "Inconclusive" is non-negotiable. Classification reasoning is the primary intellectual output of this step.
