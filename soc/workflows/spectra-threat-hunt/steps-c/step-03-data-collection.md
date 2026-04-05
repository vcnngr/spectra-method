# Step 3: Data Collection & Preparation

**Progress: Step 3 of 8** — Next: Automated Analysis

## STEP GOAL:

Verify access to all required data sources, construct detection queries per hypothesis, establish behavioral baselines for the target environment, and produce a complete hunt execution plan with queries ready to run. This step bridges hypothesis (what to look for) with execution (how to find it) — every query must trace back to a hypothesis, and every hypothesis must have at least one query.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute queries in this step — this is preparation only
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A THREAT HUNTER preparing a systematic hunt execution plan
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Threat Hunter preparing the operational infrastructure for a systematic hunt
- ✅ Every query must be purpose-built for a specific hypothesis — no exploratory fishing expeditions
- ✅ Baseline establishment is essential — without knowing "normal," you cannot identify "abnormal"
- ✅ Query performance matters — poorly optimized queries against large datasets waste time and impact production systems
- ✅ Multiple query formats increase portability — Sigma for sharing, platform-native for execution, regex for ad-hoc

### Step-Specific Rules:

- 🎯 Focus exclusively on data source verification, query construction, baseline establishment, and execution planning
- 🚫 FORBIDDEN to execute any queries or analyze any results — this is preparation, not execution
- 💬 Approach: Methodical preparation with attention to query quality, performance, and traceability
- 📊 Every query must include: purpose, hypothesis link, data source, expected results, and performance estimate
- 🔒 All queries must trace to hypotheses from step 2 — do not construct queries unrelated to defined hypotheses

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Queries with broad time ranges and no field filters against high-volume data sources (e.g., full Sysmon EventID 1 scan across 90 days) may time out, exhaust search quotas, or degrade SIEM performance for other analysts — use progressive refinement: start narrow (specific process names, specific hosts), then broaden if initial results warrant it.
  - Constructing queries without first verifying field names and log format can lead to zero-result false negatives — field names vary across SIEM platforms (e.g., `process_name` vs `Image` vs `process.executable`), and format changes after upgrades can silently break queries. Verify field schemas before execution.
  - Skipping baseline establishment means every anomaly found in step 4 will require ad-hoc baselining, which is slower and less rigorous — invest time now in understanding "normal" to make anomaly detection in the next step faster and more confident.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present data source verification results before constructing queries
- ⚠️ Present [A]/[W]/[C] menu after all queries constructed and execution plan finalized
- 💾 ONLY save to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of stepsCompleted and updating `data_sources_queried`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Hunt mission, hypotheses, ATT&CK mappings, data source requirements, success criteria from steps 1-2
- Focus: Data source verification, query construction, baseline establishment, and execution planning — no query execution or result analysis
- Limits: Only construct queries for hypotheses defined in step 2 — do not add new hypotheses without operator approval
- Dependencies: Completed hypothesis development from step-02-hypothesis.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Data Source Inventory and Access Verification

For each data source identified in step 2's requirements matrix, verify actual access and data health:

"**Data Source Access Verification:**

| # | Data Source | Required By | Access Status | Health Check | Field Schema Verified | Retention Confirmed |
|---|-------------|-------------|--------------|-------------|----------------------|-------------------|
| 1 | {{source}} | H1, H3 | ✅ Accessible / ⚠️ Restricted / ❌ Inaccessible | ✅ Logging active, no gaps / ⚠️ {{gap description}} / ❌ Source offline | ✅ / ❌ | ✅ {{days}} / ❌ {{actual vs required}} |
| 2 | ... | ... | ... | ... | ... | ... |

**Log Source Health Checks:**
- **Gap detection:** Are there any time periods within the lookback window where logging stopped? (Gaps in logging during key periods could mean an adversary disabled logging — this is itself a finding worth investigating.)
- **Delay assessment:** Is there ingestion delay between event generation and SIEM availability? (Important for near-real-time monitoring window.)
- **Format consistency:** Has the log format changed during the lookback window? (Schema changes can break queries silently.)

**Data Source Readiness Summary:**
- Sources fully available: {{count}} ({{list}})
- Sources with limitations: {{count}} ({{list with limitation details}})
- Sources unavailable: {{count}} ({{list — note impact on which hypotheses}})

**Impact Assessment:**
{{For each unavailable or limited source, explain the impact on hypothesis testability and recommend mitigation — alternative data source, adjusted scope, or hypothesis marked as inconclusive.}}"

### 2. Query Construction per Hypothesis

For each hypothesis, construct detection queries in multiple formats. Organize by hypothesis:

#### Query Format Reference

Provide queries in the formats most relevant to the target SIEM/EDR platform, plus Sigma for portability:

"**Query Library — Organized by Hypothesis:**

---

**Hypothesis H1: {{descriptive name}}**
**ATT&CK Technique:** {{T-code}}: {{technique_name}}

**Query H1-Q1: {{query purpose}}**

| Attribute | Value |
|-----------|-------|
| Purpose | {{what this query detects and why}} |
| Hypothesis Link | H1 — {{specific observable this query targets}} |
| Data Source | {{specific log source}} |
| Time Range | {{lookback window for this query}} |
| Expected Results | {{what a positive result looks like — volume, pattern}} |
| Expected Volume | {{estimated event count based on environment size}} |
| Performance Estimate | {{fast: <30s / medium: 30s-5min / slow: 5-30min / heavy: >30min}} |

**Sigma Rule:**
```yaml
title: {{descriptive title}}
id: {{UUID}}
status: experimental
description: {{what this rule detects}}
references:
  - {{ATT&CK URL}}
  - {{trigger source URL if applicable}}
author: {{user_name}} via SPECTRA threat hunt {{hunt_id}}
date: {{YYYY/MM/DD}}
tags:
  - attack.{{tactic}}
  - attack.{{T-code}}
logsource:
  category: {{category}}
  product: {{product}}
detection:
  selection:
    {{field}}: {{value}}
  condition: selection
  {{additional conditions as needed}}
falsepositives:
  - {{known FP scenario 1}}
  - {{known FP scenario 2}}
level: {{informational / low / medium / high / critical}}
```

**Splunk SPL:**
```spl
index={{index}} sourcetype={{sourcetype}}
| where {{condition}}
| stats count by {{fields}}
| where count {{threshold}}
| table {{output_fields}}
```

**Microsoft KQL (Sentinel / Defender):**
```kql
{{table}}
| where TimeGenerated between (ago({{lookback}}) .. now())
| where {{condition}}
| summarize count() by {{fields}}
| where count_ {{threshold}}
| project {{output_fields}}
```

**Elastic EQL/KQL:**
```eql
{{query_type}} where {{condition}}
```

**EDR Query ({{platform}}):**
```
{{platform-specific query syntax}}
```

**Network Query (Zeek/Suricata):**
```
{{network-specific query}}
```

---

**Query H1-Q2: {{next query purpose}}**
{{Repeat query structure for additional queries under H1}}

---

**Hypothesis H2: {{descriptive name}}**
{{Repeat entire query structure for H2}}

---

{{Continue for all hypotheses}}

**Query Summary:**
| Hypothesis | Queries | Data Sources | Est. Total Runtime | Priority |
|-----------|---------|-------------|-------------------|----------|
| H1 | {{count}} | {{sources}} | {{time}} | {{priority}} |
| H2 | {{count}} | {{sources}} | {{time}} | {{priority}} |
| ... | ... | ... | ... | ... |
| **Total** | **{{total queries}}** | **{{unique sources}}** | **{{total time}}** | — |"

### 3. Baseline Establishment

Define "normal" for the target environment and each technique being hunted:

"**Baseline Definitions:**

---

**Baseline B1: {{technique/behavior being baselined}}**
**Purpose:** Establish what normal looks like for {{specific activity}} so deviations can be identified in automated analysis

**Statistical Baseline:**

| Metric | Normal Range | Measurement Period | Source |
|--------|-------------|-------------------|--------|
| {{metric — e.g., "PowerShell execution count per host per day"}} | {{range — e.g., "5-25 events"}} | {{period — e.g., "last 30 days"}} | {{data source}} |
| {{metric — e.g., "Unique external DNS destinations per host per day"}} | {{range — e.g., "50-200"}} | {{period}} | {{data source}} |
| {{metric — e.g., "Off-hours logon events"}} | {{range — e.g., "0-3 per night"}} | {{period}} | {{data source}} |

**Behavioral Baseline:**

| Behavior | Normal Pattern | Abnormal Pattern (Hunt Target) |
|----------|---------------|-------------------------------|
| Process parent-child | {{e.g., "explorer.exe → chrome.exe, outlook.exe → winword.exe"}} | {{e.g., "winword.exe → cmd.exe → powershell.exe"}} |
| Network destinations | {{e.g., "Internal DNS, CDN, known SaaS"}} | {{e.g., "Newly registered domains, bulletproof hosting, Tor"}} |
| User activity hours | {{e.g., "08:00-18:00 local time"}} | {{e.g., "02:00-04:00 activity from non-shift workers"}} |
| Service account behavior | {{e.g., "Fixed set of hosts, predictable operations"}} | {{e.g., "Lateral access to new hosts, interactive logon"}} |

**Whitelist Strategy:**

| Category | Known-Good Items | Source of Truth |
|----------|-----------------|----------------|
| Authorized admin tools | {{list — e.g., "SCCM, Ansible, Intune"}} | {{IT approved tool list}} |
| Authorized remote access | {{list — e.g., "VPN IPs, jump box IPs"}} | {{network diagram}} |
| Scheduled tasks | {{list — e.g., "backup jobs, patch cycles"}} | {{change management}} |
| Service accounts | {{list — e.g., "svc-backup, svc-monitor"}} | {{AD service account inventory}} |

---

**Baseline B2: {{next technique/behavior}}**
{{Repeat baseline structure}}

---"

### 4. Hunt Execution Plan

"**Hunt Execution Plan:**

| Execution Order | Query ID | Hypothesis | Data Source | Est. Runtime | Invasiveness | Dependency |
|----------------|----------|-----------|-------------|-------------|-------------|------------|
| 1 | H1-Q1 | H1 | {{source}} | {{time}} | Low | None |
| 2 | H1-Q2 | H1 | {{source}} | {{time}} | Low | None |
| 3 | H2-Q1 | H2 | {{source}} | {{time}} | Medium | H1-Q1 results |
| ... | ... | ... | ... | ... | ... | ... |

**Execution Strategy:**
- **Phase 1 — Low-impact queries:** {{queries that scan indexed/aggregated data — minimal system impact}}
- **Phase 2 — Medium-impact queries:** {{queries against raw logs, broader time ranges, cross-data-source joins}}
- **Phase 3 — High-impact queries:** {{resource-intensive queries — full-text search, statistical analysis, large exports}}

**Parallel Execution Opportunities:**
- Queries that can run simultaneously: {{list — e.g., H1-Q1 and H2-Q1 target different data sources}}
- Queries that must be sequential: {{list — e.g., H2-Q2 depends on H1-Q1 results to narrow scope}}

**Checkpoint Strategy:**
- Save intermediate results after each phase
- After Phase 1: assess whether any hypothesis is trending strongly → may adjust Phase 2 priorities
- After Phase 2: assess whether Phase 3 is necessary or if sufficient evidence exists
- Each checkpoint updates the hunt report with current findings

**Performance Impact Mitigation:**
- Schedule heavy queries during {{low-activity period}} if possible
- Set query timeouts at {{threshold}} to prevent runaway queries
- Monitor SIEM/EDR performance during execution — pause if {{threshold}} is reached
- Use sampling for initial sweeps, then drill down on interesting results

**Estimated Total Execution Time:** {{total time for all phases}}
**Estimated Data Volume to Scan:** {{total volume across all queries}}"

### 5. Data Collection Readiness Matrix

"**Data Collection Readiness — Final Assessment:**

| Hypothesis | Queries Ready | Data Sources Verified | Baseline Defined | Execution Phase | Testability |
|-----------|--------------|---------------------|-----------------|----------------|------------|
| H1 | {{count}} / {{planned}} | ✅ / ⚠️ / ❌ | ✅ / ❌ | Phase {{1/2/3}} | {{High/Medium/Low}} |
| H2 | {{count}} / {{planned}} | ✅ / ⚠️ / ❌ | ✅ / ❌ | Phase {{1/2/3}} | {{High/Medium/Low}} |
| ... | ... | ... | ... | ... | ... |

**Overall Readiness:**
- Total queries constructed: {{count}}
- Data sources verified: {{count}} / {{total required}}
- Baselines defined: {{count}} / {{total needed}}
- Execution plan validated: ✅ / ❌
- Estimated total runtime: {{time}}

**Blockers (if any):**
{{List any issues that could prevent successful execution — missing access, insufficient retention, performance concerns}}

**Recommendation:** {{Ready to execute / Execute with caveats / Requires remediation before proceeding}}"

### 6. Present MENU OPTIONS

"**Data collection preparation complete.**

Summary: {{query_count}} queries constructed across {{hypothesis_count}} hypotheses targeting {{source_count}} data sources.
Execution plan: {{phase_count}} phases, estimated {{total_time}} total runtime.
Baselines: {{baseline_count}} behavioral baselines defined.

**Select an option:**
[A] Advanced Elicitation — Review query quality, optimize performance, identify missing detection angles
[W] War Room — Red vs Blue discussion on query evasion and detection blind spots
[C] Continue — Proceed to Automated Analysis / Hunt Execution (Step 4 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive query review — examine each query for potential false negative scenarios (what would an adversary do to avoid triggering this query?), optimize query performance (can filters be added to reduce scan volume?), identify missing queries (are there observables from the hypothesis that don't have a corresponding query?), review baseline completeness (are there legitimate activities not whitelisted that could create noise?). Process insights, ask user if they want to update queries, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: if I saw these queries, which would I worry about most? Which could I trivially evade by modifying my tradecraft? Are there simpler detection approaches that would be harder to evade? What about the queries' time ranges — could I operate in gaps between baseline periods? Blue Team perspective: are our queries robust against technique variations? Do we have sufficient baseline coverage? Are our whitelists too permissive? What's our contingency if Phase 1 yields overwhelming results? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `data_sources_queried` array and `queries_executed` count (set to 0, will be updated during execution). Append data collection details to report under `## Data Sources & Collection`. Then read fully and follow: ./step-04-automated-analysis.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and data_sources_queried populated, and data collection details appended to report under `## Data Sources & Collection`], will you then read fully and follow: `./step-04-automated-analysis.md` to begin automated hunt execution.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All required data sources verified for access, health, field schema, and retention
- Data source limitations documented with impact on hypothesis testability
- Detection queries constructed for every hypothesis with multiple format options (Sigma + platform-native)
- Every query includes: purpose, hypothesis link, data source, expected results, and performance estimate
- Behavioral baselines defined for target environment covering normal patterns per technique
- Whitelist strategy documented with source of truth per category
- Hunt execution plan defined with phased approach, parallel opportunities, checkpoint strategy, and performance mitigation
- Data collection readiness matrix confirms overall readiness
- All data collection details appended to report under `## Data Sources & Collection`
- Frontmatter updated with data_sources_queried and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Constructing queries without verifying data source access and field schemas
- Queries that don't trace to a specific hypothesis (fishing expeditions)
- Not establishing baselines before proceeding to analysis (every anomaly will require ad-hoc investigation)
- Not assessing query performance impact on production systems
- Executing queries during this preparation step (step 3 is planning only)
- Not documenting data source limitations and their impact on hypothesis testability
- Not providing multiple query formats for portability and platform flexibility
- Not defining a phased execution plan with checkpoints
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every query must trace to a hypothesis. Every hypothesis must have queries ready. Every baseline must be defined before hunting begins. Preparation prevents wasted execution time.
