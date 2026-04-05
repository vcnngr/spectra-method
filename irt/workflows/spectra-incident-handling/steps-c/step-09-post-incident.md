# Step 9: Post-Incident Review & Lessons Learned

**Progress: Step 9 of 10** — Next: Reporting & Engagement Closure

## STEP GOAL:

Conduct a thorough post-incident review (PIR) following NIST 800-61 Section 3.4 guidelines to extract lessons learned, quantify detection and response metrics, identify process improvements, and generate actionable SMART recommendations that strengthen the organization's security posture. This is the MOST IMPORTANT step from an organizational improvement perspective — NIST 800-61 emphasizes that post-incident activity is what prevents the NEXT incident. Every minute invested here pays compound dividends in future incident prevention, detection speed, and response efficiency.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate post-incident findings without operator input — the PIR is a collaborative exercise, not an autonomous report
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator facilitating a structured post-incident review under NIST 800-61 Section 3.4
- ✅ The PIR is a blameless learning exercise — your role is facilitator, not judge. Focus on systems and processes, not individuals
- ✅ Every finding must reference specific incident data — no speculation, no assumptions, only evidence-based observations
- ✅ Recommendations without owners and deadlines are wishes, not action items — every recommendation must be SMART
- ✅ The PIR bridges this incident to organizational improvement — it is the mechanism by which one incident prevents the next ten
- ✅ Document both successes and failures with equal rigor — reinforcing what worked is as important as fixing what didn't

### Step-Specific Rules:

- 🎯 Focus exclusively on post-incident review facilitation, metric calculation, gap analysis, root cause analysis, and recommendation generation — no new containment, eradication, or recovery activity
- 🚫 FORBIDDEN to look ahead to step 10 or begin report finalization
- 💬 Approach: Facilitative, blameless, evidence-based — guide the operator through structured reflection with probing questions
- 📊 All metrics must be calculated from documented timestamps — never estimate when actual data exists
- 🔒 PIR findings are sensitive — they reveal organizational weaknesses. Handle with appropriate confidentiality
- ⏱️ The PIR should be conducted while events are fresh — ideally within 1-2 weeks of incident closure (NIST 800-61 recommendation)
- 📝 Recommendations must be specific enough to implement without further clarification — vague recommendations are organizational debt

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Skipping the PIR or rushing through it because "the incident is over" wastes the most valuable learning opportunity — NIST 800-61 emphasizes this is where organizational improvement happens. An unreviewed incident is a wasted incident — the organization paid the cost but refused the lesson
  - Allowing blame-oriented discussion instead of blameless review creates a culture where incidents are hidden rather than reported, degrading future detection and response — blame suppresses the candid information sharing that is essential for accurate root cause analysis
  - Not assigning specific owners and deadlines to recommendations means they will never be implemented — an unimplemented lesson learned is a lesson wasted. Studies show that recommendations without accountability have less than 10% implementation rates
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your PIR facilitation plan before beginning — let the operator know the structure and time expectations
- ⚠️ Present [A]/[W]/[C] menu after PIR is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter: add this step name to the end of stepsCompleted, set `post_incident_completed: true`
- 🚫 FORBIDDEN to load next step until C is selected
- 📊 Calculate all metrics from documented incident data — cross-reference timestamps from steps 1-8

## CONTEXT BOUNDARIES:

- Available context: Complete incident handling report with data from steps 1-8 (intake, detection analysis, triage, containment, evidence, deep analysis, eradication, recovery), all frontmatter fields, engagement.yaml
- Focus: Post-incident review facilitation, metric calculation, gap analysis, root cause analysis of process failures, recommendation generation, detection engineering handoff, and knowledge base updates — no new operational response actions
- Limits: Do not fabricate metrics or findings — every data point must reference documented incident data. Do not assume organizational context beyond what was gathered during the incident
- Dependencies: All prior steps (1-8) must be completed — the PIR synthesizes the entire incident lifecycle. Recovery must be complete or in monitoring phase before conducting a meaningful PIR

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Post-Incident Review Meeting Facilitation

Before diving into analysis, structure the PIR session and set expectations with the operator. This is a facilitated discussion, not an autonomous report.

**PIR Session Setup:**

"**Post-Incident Review (PIR) — Incident {{incident_id}}**

We are now entering the most important phase of incident response from an organizational improvement perspective. NIST 800-61 Section 3.4 designates post-incident activity as the mechanism that transforms a single incident response into lasting security improvement.

**PIR Agenda:**

| # | Topic | Duration | Purpose |
|---|-------|----------|---------|
| 1 | Incident Overview | 5 min | What happened — timeline summary, scope, impact |
| 2 | Detection Effectiveness | 10 min | How was it detected? How could detection be faster? |
| 3 | Response Effectiveness | 15 min | What went well? What didn't? Bottlenecks? |
| 4 | Communication Effectiveness | 10 min | Were stakeholders informed? Timely? Accurately? |
| 5 | Technical Analysis | 15 min | Root cause, attack chain, scope accuracy |
| 6 | Process Gaps | 10 min | What procedures were missing or inadequate? |
| 7 | Improvement Actions | 15 min | Specific, measurable, assigned, time-bound |
| 8 | Final Summary | 5 min | Key takeaways and next steps |

**PIR Ground Rules:**
- **Blameless culture** — We focus on systems and processes, not individuals. The question is never 'who failed?' but 'what system allowed this failure?'
- **Evidence-based** — Every finding must reference incident data. No speculation, no assumptions.
- **Forward-looking** — The goal is improvement, not punishment. Every finding should lead to an action.
- **Inclusive** — All responders should contribute. I recommend using the War Room option [W] for multi-perspective analysis.
- **Honest** — Understating failures and overstating successes undermines the entire exercise. Candor is the currency of effective PIR.

Shall we begin? I will guide you through each agenda item with structured questions."

Wait for operator acknowledgment before proceeding. If the operator wants to skip or abbreviate, WARN about the cost of incomplete PIR but COMPLY after warning.

### 2. Incident Overview Recap

Present a concise summary of the incident compiled from steps 1-8 to establish shared context:

"**Incident Overview Recap:**

| Attribute | Value |
|-----------|-------|
| Incident ID | {{incident_id}} |
| Severity | {{incident_severity}} |
| Category | {{incident_category}} |
| Detection Source | {{detection_source}} |
| Detection Timestamp | {{detection_timestamp}} UTC |
| Root Cause | {{root_cause}} |
| Attack Vector | {{attack_vector}} |
| Affected Systems | {{affected_systems}} |
| Affected Users | {{affected_users}} |
| Data at Risk | {{affected_data}} |
| Containment Strategy | {{containment_strategy}} |
| Containment Achieved | {{containment_timestamp}} UTC |
| Eradication Completed | {{eradication_timestamp}} UTC |
| Recovery Completed | {{recovery_timestamp}} UTC |
| Current Status | {{incident_status}} |
| MITRE Techniques | {{mitre_techniques}} |
| Dwell Time | {{dwell_time}} |

**Incident Narrative:**
{{2-3 paragraph narrative of the incident lifecycle compiled from report sections — what happened, how it was detected, how it was contained, eradicated, and recovered from}}

Does this summary accurately capture the incident? Are there any corrections or additions before we proceed to the detailed review?"

Wait for operator confirmation. Integrate any corrections.

### 3. Detection & Response Metrics

Calculate quantitative metrics from documented timestamps. These metrics are the foundation for benchmarking and improvement tracking.

**Key Time-Based Metrics:**

Calculate each metric from the documented timestamps in the incident report:

- **MTTD (Mean Time to Detect):** Time from first attacker activity (earliest IOC timestamp or estimated initial compromise) to the moment the incident was detected. Source: earliest indicator timestamp from step 2 detection timeline vs detection_timestamp from step 1 intake.

- **MTTR (Mean Time to Respond):** Time from detection to the initiation of response actions. Source: detection_timestamp vs first containment action timestamp from step 4.

- **MTTC (Mean Time to Contain):** Time from detection to full containment achieved. Source: detection_timestamp vs containment_timestamp from step 4 frontmatter.

- **MTTE (Mean Time to Eradicate):** Time from containment achieved to eradication complete. Source: containment_timestamp vs eradication_timestamp from step 7 frontmatter.

- **MTTRec (Mean Time to Recover):** Time from eradication complete to full recovery. Source: eradication_timestamp vs recovery_timestamp from step 8 frontmatter.

- **Total Incident Duration:** Time from first attacker activity to recovery complete. Source: earliest indicator timestamp vs recovery_timestamp.

- **Dwell Time:** Time from first attacker activity to detection — this is the adversary's undetected operational window. Source: dwell_time from step 6 deep analysis (most accurate) or step 2 estimate.

Present metrics as structured table:

"**Detection & Response Metrics:**

| Metric | Value | Calculation | Benchmark | Assessment |
|--------|-------|-------------|-----------|------------|
| MTTD (Time to Detect) | {{calculated}} | First activity → Detection | Industry median ~16 days (Mandiant M-Trends) | {{above/below/at benchmark}} |
| MTTR (Time to Respond) | {{calculated}} | Detection → Response initiation | SLA target: {{org SLA or 'not defined'}} | {{assessment}} |
| MTTC (Time to Contain) | {{calculated}} | Detection → Full containment | SLA target: {{org SLA or 'not defined'}} | {{assessment}} |
| MTTE (Time to Eradicate) | {{calculated}} | Containment → Eradication complete | Depends on scope | {{assessment}} |
| MTTRec (Time to Recover) | {{calculated}} | Eradication → Recovery complete | Depends on scope | {{assessment}} |
| Total Duration | {{calculated}} | First activity → Recovery | — | {{assessment}} |
| Dwell Time | {{calculated}} | First activity → Detection | Median ~16 days (external), ~9 days (internal detection) | {{assessment}} |

**Benchmark Context:**
- Mandiant M-Trends report: median dwell time for externally notified incidents is ~16 days, internally detected ~9 days
- For ransomware incidents: median dwell time before encryption is typically 5-7 days
- Compare MTTR and MTTC against organizational SLA targets if defined
- Compare against organization's historical incidents if baseline data exists

How do these metrics compare to your expectations and organizational targets?"

Wait for operator input on metric context and organizational benchmarks.

**Process Metrics:**

"**Process Metrics Assessment:**

| Metric | Value | Impact |
|--------|-------|--------|
| Escalation count | {{number of escalations during incident}} | {{did escalation work smoothly or cause delays?}} |
| False starts / misdirections | {{count of investigative dead ends}} | {{time wasted on incorrect hypotheses}} |
| Communication delays | {{gaps between detection and stakeholder notification}} | {{did delays affect business decisions?}} |
| Tool gaps | {{tools needed but unavailable during response}} | {{what capability was missing?}} |
| Staff availability issues | {{any staffing gaps during response}} | {{did staffing affect response speed?}} |
| Evidence collection issues | {{any evidence that was unavailable or compromised}} | {{did evidence gaps affect analysis accuracy?}} |
| Playbook adequacy | {{was there a playbook for this incident type?}} | {{did the playbook cover the actual scenario?}} |

Were there additional process issues not captured here?"

Wait for operator input.

### 4. What Worked Well

Document positive outcomes with equal rigor as failures. Reinforcing effective practices is as important as fixing gaps — what gets recognized gets repeated.

"**What Worked Well — Structured Assessment:**

I will propose findings based on the incident data. Please confirm, correct, or add to each category.

**Category: Detection Capabilities**
- What detection mechanisms fired correctly and in a timely manner?
- Was the initial alert accurate (true positive)?
- Did enrichment and correlation produce actionable intelligence?

**Category: Response Procedures**
- Which response procedures were effective and followed correctly?
- Were containment actions timely and successful?
- Was evidence preservation handled properly?

**Category: Communication**
- Were stakeholder notifications timely and accurate?
- Was the escalation path clear and functional?
- Did executive communication meet expectations?

**Category: Tools & Technology**
- Which tools performed as expected during the incident?
- Did EDR/SIEM/NDR provide the visibility needed?
- Were forensic tools adequate for evidence collection?

**Category: Team Coordination**
- Was workstream coordination effective?
- Were roles and responsibilities clear?
- Did handoffs between shifts/teams work smoothly?

**Category: Decision Making**
- Which decisions were correct in hindsight?
- Was the severity classification accurate?
- Was the containment strategy appropriate?

For each positive finding, I will document:
1. What happened — the specific positive outcome
2. Why it worked — the underlying process, tool, or capability that enabled it
3. How to sustain it — what to do to ensure this continues to work in future incidents"

Guide the operator through each category, asking probing questions. Document each finding as a structured entry:

```
| # | Category | What Worked | Why It Worked | How to Sustain |
|---|----------|-------------|---------------|----------------|
```

### 5. What Needs Improvement

Document gaps and failures with evidence-based specificity. The goal is not blame but precise identification of improvement targets.

"**What Needs Improvement — Structured Assessment:**

I will walk through each category systematically. For each gap identified, we will document the evidence and impact.

**Category: Detection Gaps**
- What indicators were missed or detected late?
- Were there IOCs that should have been caught by existing rules?
- What was the dwell time, and what could have shortened it?
- Were there blind spots in log collection or telemetry?

**Category: Response Gaps**
- Were there procedures that were missing for this incident type?
- Were existing procedures unclear, outdated, or inadequate?
- Were there delays in decision-making that affected outcomes?
- Were containment actions timely, or were there bottlenecks?

**Category: Communication Gaps**
- Were there delays in stakeholder notification?
- Were any required notifications missed entirely?
- Was the escalation path unclear at any point?
- Were executive updates timely and at the right level of detail?

**Category: Tool Gaps**
- Were any tools unavailable when needed?
- Did any tools underperform or produce unreliable results?
- Were there capabilities needed that no tool in the stack provides?
- Were tool integrations (SIEM-to-EDR, EDR-to-SOAR) working?

**Category: Knowledge Gaps**
- Were there skills or knowledge that were lacking during the response?
- Was the team familiar with the attack techniques encountered?
- Were there analysis tasks that required expertise not available?
- Was institutional knowledge about the environment sufficient?

**Category: Process Gaps**
- Were there procedures that don't exist but should?
- Were existing procedures not followed? If so, why?
- Were approval processes too slow for the urgency level?
- Were there ambiguities in roles and responsibilities?

**Category: Documentation Gaps**
- Were runbooks outdated or missing for this incident type?
- Was asset inventory accurate enough for scope determination?
- Were network diagrams current and useful during the response?
- Were contact lists and escalation matrices up to date?"

Guide the operator through each category. For each gap identified, document:

```
| # | Category | Gap Description | Evidence | Impact | Root Cause |
|---|----------|----------------|----------|--------|------------|
```

### 6. Root Cause Analysis of Process Failures

For each significant gap identified in section 5, go deeper than symptoms to identify root causes. Use the 5 Whys technique to trace each gap to its underlying systemic cause.

"**Root Cause Analysis — 5 Whys Method:**

For each significant process failure, we will trace the chain of causation to the root. This is where we move from 'what happened' to 'why the system allowed it to happen.'

Let me walk through the most impactful gaps identified above."

For each significant gap, conduct the 5 Whys:

**5 Whys Template:**

"**Gap:** {{gap description from section 5}}

| Level | Question | Answer |
|-------|----------|--------|
| Why 1 | Why did {{gap}} happen? | {{answer}} |
| Why 2 | Why did {{why 1 answer}} happen? | {{answer}} |
| Why 3 | Why did {{why 2 answer}} happen? | {{answer}} |
| Why 4 | Why did {{why 3 answer}} happen? | {{answer}} |
| Why 5 | Why did {{why 4 answer}} happen? | {{answer — this is typically the root cause}} |

**Root Cause Classification:** {{People / Process / Technology / Organizational}}
**Systemic or Isolated:** {{Is this a systemic issue affecting multiple incidents, or isolated to this incident?}}"

Guide the operator through 5 Whys for each significant gap. Not every gap needs 5 levels — stop when the root cause is reached.

**Contributing Factors Assessment:**

After individual root cause analyses, assess the broader contributing factors:

"**Contributing Factors Assessment:**

| Factor | Assessment | Impact on This Incident |
|--------|-----------|------------------------|
| Staffing levels during incident | {{adequate / insufficient / critical gaps}} | {{how staffing affected response speed and quality}} |
| Training and preparation state | {{well-prepared / partially prepared / unprepared}} | {{how training gaps affected response}} |
| Playbook/runbook availability | {{available and current / available but outdated / missing}} | {{how playbook state affected response}} |
| Tool availability and effectiveness | {{all tools available / partial gaps / critical gaps}} | {{how tool availability affected response}} |
| Management support and decision speed | {{fast and supportive / adequate / slow or absent}} | {{how management engagement affected response}} |
| Cross-team coordination | {{smooth / functional with friction / dysfunctional}} | {{how coordination affected response}} |
| Pre-existing security posture | {{strong / adequate / weak}} | {{how baseline security affected the incident}} |
| Threat intelligence readiness | {{proactive / reactive / absent}} | {{how threat intel influenced detection and response}} |

Which of these factors had the most significant impact on the incident outcome?"

Wait for operator input.

### 7. Actionable Recommendations — SMART Format

Generate recommendations that are Specific, Measurable, Assigned, Realistic, and Time-bound. Each recommendation must trace back to a specific finding from sections 4-6.

"**Actionable Recommendations:**

Based on our PIR findings, I will propose recommendations in five categories. For each recommendation, we need to assign an owner and deadline. Recommendations without accountability have less than 10% implementation rates.

**Category: Detection Improvements**

| # | Recommendation | Priority | Owner | Deadline | Success Metric | Source Finding |
|---|---------------|----------|-------|----------|----------------|----------------|
| D-1 | {{specific detection improvement}} | Critical/High/Medium/Low | {{assigned owner}} | {{date}} | {{how to verify implementation}} | {{gap # from section 5}} |
| D-2 | ... | ... | ... | ... | ... | ... |

**Category: Response Improvements**

| # | Recommendation | Priority | Owner | Deadline | Success Metric | Source Finding |
|---|---------------|----------|-------|----------|----------------|----------------|
| R-1 | {{specific response improvement}} | Critical/High/Medium/Low | {{assigned owner}} | {{date}} | {{how to verify implementation}} | {{gap # from section 5}} |
| R-2 | ... | ... | ... | ... | ... | ... |

**Category: Prevention Improvements**

| # | Recommendation | Priority | Owner | Deadline | Success Metric | Source Finding |
|---|---------------|----------|-------|----------|----------------|----------------|
| P-1 | {{specific prevention improvement}} | Critical/High/Medium/Low | {{assigned owner}} | {{date}} | {{how to verify implementation}} | {{gap # from section 5}} |
| P-2 | ... | ... | ... | ... | ... | ... |

**Category: Process & Documentation**

| # | Recommendation | Priority | Owner | Deadline | Success Metric | Source Finding |
|---|---------------|----------|-------|----------|----------------|----------------|
| PD-1 | {{specific process/doc improvement}} | Critical/High/Medium/Low | {{assigned owner}} | {{date}} | {{how to verify implementation}} | {{gap # from section 5}} |
| PD-2 | ... | ... | ... | ... | ... | ... |

**Category: Training & Awareness**

| # | Recommendation | Priority | Owner | Deadline | Success Metric | Source Finding |
|---|---------------|----------|-------|----------|----------------|----------------|
| T-1 | {{specific training improvement}} | Critical/High/Medium/Low | {{assigned owner}} | {{date}} | {{how to verify implementation}} | {{gap # from section 5}} |
| T-2 | ... | ... | ... | ... | ... | ... |"

**Recommendation Quality Checklist:**

For each recommendation, verify it meets SMART criteria:
- **Specific** — Is it clear enough to implement without further clarification? Could someone unfamiliar with the incident understand what needs to be done?
- **Measurable** — Is there a concrete success metric? How will we know it's done?
- **Assigned** — Is there a named owner? (Person or team, not "someone should...")
- **Realistic** — Is it achievable given organizational constraints, budget, and staffing?
- **Time-bound** — Is there a deadline? Not "ASAP" or "when possible" — an actual date.

"Do you want to adjust any recommendations? Add owners or deadlines? Modify priority levels?"

Wait for operator input. Iterate until the operator is satisfied with the recommendation set.

### 8. Detection Engineering Recommendations

Bridge the PIR findings to the detection engineering function. This is where lessons learned become concrete detection improvements.

"**Detection Engineering Handoff:**

Based on the incident IOCs, attack techniques, and detection gaps identified in this PIR, the following detection engineering actions are recommended:

**New Detection Rules Needed:**

| # | Rule Type | Description | ATT&CK Technique | Source IOC/Behavior | Priority |
|---|-----------|-------------|-------------------|---------------------|----------|
| 1 | {{Sigma/YARA/Snort/Custom}} | {{what the rule should detect}} | {{T-code}} | {{specific IOC or behavior from this incident}} | {{priority}} |
| 2 | ... | ... | ... | ... | ... |

**Existing Rules Requiring Tuning:**

| # | Rule ID/Name | Current State | Required Tuning | Reason |
|---|-------------|---------------|-----------------|--------|
| 1 | {{rule identifier}} | {{current behavior}} | {{what needs to change}} | {{why — reference incident data}} |
| 2 | ... | ... | ... | ... |

**Detection Gap Coverage:**

| # | Gap Description | Required Data Source | Detection Approach | Complexity |
|---|----------------|--------------------|--------------------|------------|
| 1 | {{what we cannot currently detect}} | {{log source or telemetry needed}} | {{how to detect it}} | High/Medium/Low |
| 2 | ... | ... | ... | ... |

**Cross-Module Recommendations:**
- **Sentinel** (`spectra-detection-lifecycle`): Recommend invoking Sentinel for formal Sigma/YARA rule development based on the IOCs and techniques documented in this incident. Sentinel can take the ATT&CK mapping and IOC list and produce validated, tested detection rules.
- **Hawk** (`spectra-threat-hunting`): Recommend proactive threat hunting sweeps using the behavioral indicators from this incident to validate that similar activity is not occurring elsewhere in the environment. Hawk can design and execute hypothesis-driven hunts based on the ATT&CK techniques mapped.
- **Oracle** (`spectra-threat-intel-workflow`): Recommend formal threat intelligence analysis to determine if this incident is part of a broader campaign targeting the organization or sector.

Would you like to refine these detection engineering recommendations?"

Wait for operator input.

### 9. Knowledge Base Update Recommendations

Capture institutional knowledge so this incident's lessons persist beyond the PIR.

"**Knowledge Base Update Checklist:**

The following knowledge base updates are recommended to capture institutional learning from this incident:

| # | Update Type | Description | Owner | Status |
|---|-----------|-------------|-------|--------|
| 1 | Incident Pattern Documentation | Document the attack pattern (initial access → persistence → lateral movement → objective) as a reference case for future incidents of this type | {{owner}} | Pending |
| 2 | IR Playbook Update | Update (or create) the IR playbook for {{incident_category}} incidents based on lessons learned — incorporate the effective procedures and close the gaps identified | {{owner}} | Pending |
| 3 | IOC Database Update | Add all validated IOCs from this incident to the organization's threat intel database with context, confidence levels, and expiration dates | {{owner}} | Pending |
| 4 | Asset Inventory Update | Update asset inventory if new systems, services, or network segments were discovered during scope determination that were not previously documented | {{owner}} | Pending |
| 5 | Contact List Update | Update IR contact lists and escalation matrices if any contacts were incorrect, missing, or unreachable during the incident | {{owner}} | Pending |
| 6 | Network Documentation Update | Update network diagrams if the incident revealed undocumented network paths, segments, or connections | {{owner}} | Pending |
| 7 | Threat Actor Profile | If a specific threat actor was attributed, create or update the threat actor profile with TTPs observed in this incident | {{owner}} | Pending |

**Cross-Module Recommendation:**
- **Chronicle** (`spectra-agent-chronicle`): Recommend invoking Chronicle for formal incident documentation write-up — Chronicle produces polished, structured incident reports suitable for the knowledge base and organizational record.

Which knowledge base updates are applicable? Assign owners for each."

Wait for operator input.

### 10. Update Frontmatter

Update the incident handling report frontmatter:

- Set `post_incident_completed: true`
- Add PIR completion timestamp
- Record total recommendation count
- Record metric values calculated in section 3

### 11. Append Findings to Report

Write all PIR findings to the output document under `## Post-Incident Review`:

```markdown
## Post-Incident Review

### PIR Meeting Summary
{{PIR session context — date, participants, ground rules}}

### Incident Overview
{{Concise incident recap from section 2}}

### Detection & Response Metrics
{{Metrics table from section 3 — MTTD, MTTR, MTTC, MTTE, MTTRec, Total Duration, Dwell Time}}
{{Benchmark comparisons}}
{{Process metrics table}}

### What Worked Well
{{Structured findings table from section 4 — category, finding, why it worked, how to sustain}}

### What Needs Improvement
{{Structured findings table from section 5 — category, gap, evidence, impact, root cause}}

### Root Cause Analysis
{{5 Whys analysis for each significant gap from section 6}}
{{Contributing factors assessment}}

### Recommendations
{{SMART recommendations by category from section 7}}
{{Detection, Response, Prevention, Process & Documentation, Training & Awareness}}

### Detection Engineering Handoff
{{New rules, tuning requirements, gap coverage from section 8}}

### Knowledge Base Updates
{{Checklist from section 9}}
```

### 12. Present MENU OPTIONS

"**Post-incident review complete.**

**PIR Summary:**
- **Metrics calculated:** MTTD: {{mttd}} | MTTR: {{mttr}} | MTTC: {{mttc}} | Dwell Time: {{dwell_time}}
- **What worked well:** {{count}} findings documented
- **Gaps identified:** {{count}} process gaps with root cause analysis
- **Recommendations generated:** {{count}} SMART recommendations across 5 categories
- **Detection engineering actions:** {{count}} new rules + {{count}} tuning actions
- **Knowledge base updates:** {{count}} items identified

This PIR captures the organizational learning from incident {{incident_id}}. The next step finalizes the incident report with executive summary, complete timeline, IOC summary, and formal closure.

**Select an option:**
[A] Advanced Elicitation — Deep challenge of PIR findings: stress-test the root cause analysis, question whether recommendations are truly SMART, probe for overlooked gaps, challenge the metric calculations
[W] War Room — Full team debrief — all perspectives: Handler (coordination effectiveness), Forensics (evidence and analysis quality), Threat Intel (intelligence gaps), SOC (detection effectiveness), Management (communication and decision speed)
[C] Continue — Proceed to Step 10: Reporting & Engagement Closure (Step 10 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis of PIR findings — challenge the root cause analysis for completeness (are we stopping at symptoms instead of root causes?), stress-test whether recommendations are truly SMART (or are they vague aspirations?), probe for gaps the PIR may have overlooked (what about supply chain? what about insider risk? what about cloud-specific issues?), verify metric calculations against documented timestamps, question whether the "what worked well" section is honest or self-congratulatory. Process insights, ask operator if they want to update findings, if yes update document then redisplay menu, if no redisplay menu
- IF W: War Room — Full team debrief with all agent perspectives: Handler perspective: was coordination effective? Were workstreams managed well? Were decisions made at the right time? Forensics perspective: was evidence handling adequate? Were forensic tools sufficient? Was analysis thorough enough? Threat Intel perspective: did we have the intelligence we needed? Were there campaign indicators we missed? Is this actor likely to return? SOC perspective: did detection rules fire as expected? What telemetry gaps exist? Are the proposed detection improvements sufficient? Management perspective: was communication timely? Were executive updates actionable? Were resource allocation decisions sound? Summarize all perspectives, ask operator if they want to incorporate insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, set `post_incident_completed: true`, then read fully and follow: ./step-10-closure.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, post_incident_completed set to true, detection and response metrics documented, recommendations generated in SMART format with owners and deadlines, and Post-Incident Review section populated in the report], will you then read fully and follow: `./step-10-closure.md` to begin reporting and engagement closure.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- PIR session structured with clear agenda, ground rules, and blameless culture established before beginning
- Incident overview recap presented and confirmed by operator before proceeding to detailed review
- All time-based metrics calculated from documented timestamps (MTTD, MTTR, MTTC, MTTE, MTTRec, Total Duration, Dwell Time)
- Metrics compared against industry benchmarks (Mandiant M-Trends) and organizational targets where available
- Process metrics documented (escalation count, false starts, communication delays, tool gaps, staffing issues)
- "What worked well" documented with structured entries across all applicable categories (detection, response, communication, tools, coordination, decisions)
- "What needs improvement" documented with evidence-based gap entries across all applicable categories (detection, response, communication, tools, knowledge, process, documentation)
- Root cause analysis conducted using 5 Whys for each significant process gap
- Root causes classified as People / Process / Technology / Organizational
- Contributing factors assessed (staffing, training, playbooks, tools, management, coordination, security posture, threat intel)
- Recommendations generated in SMART format with specific owner, deadline, success metric, and source finding reference for each
- Recommendations organized across five categories: Detection, Response, Prevention, Process & Documentation, Training & Awareness
- Detection engineering handoff documented with new rules needed, existing rules requiring tuning, and detection gap coverage
- Cross-module recommendations made for Sentinel, Hawk, Oracle, and Chronicle where applicable
- Knowledge base update checklist generated with owners assigned
- PIR findings appended to report under `## Post-Incident Review` with all sub-sections populated
- Frontmatter updated with post_incident_completed: true and this step added to stepsCompleted
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Skipping the PIR or generating findings without operator participation — the PIR is a collaborative exercise, not an automated report
- Conducting a blame-oriented review that focuses on individual failures instead of systemic issues
- Fabricating metrics or findings that are not supported by documented incident data
- Calculating metrics from estimated timestamps when actual timestamps are documented in the report
- Not calculating dwell time or key response metrics (MTTD, MTTR, MTTC)
- Generating recommendations that are vague, unassigned, or without deadlines — every recommendation must be SMART
- Not conducting root cause analysis on significant gaps — treating symptoms instead of causes
- Not documenting "what worked well" — reinforcing effective practices is as important as fixing failures
- Generating detection engineering recommendations without referencing specific incident IOCs or ATT&CK techniques
- Not providing cross-module recommendations for detection lifecycle, threat hunting, or threat intelligence workflows
- Initiating any new containment, eradication, or recovery actions during the PIR
- Proceeding to step 10 without completing the full PIR exercise
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted and post_incident_completed

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. The PIR is the mechanism that transforms one incident into organizational improvement. Every finding must have evidence. Every recommendation must be SMART. Blameless culture is non-negotiable. This is where the investment in incident response pays long-term dividends.
