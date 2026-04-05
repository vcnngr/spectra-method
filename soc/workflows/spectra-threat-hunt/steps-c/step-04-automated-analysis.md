# Step 4: Hunt Execution — Automated Analysis

**Progress: Step 4 of 8** — Next: Manual Analysis

## STEP GOAL:

Execute all queries from the hunt execution plan systematically, apply pattern detection techniques to the results, perform automated triage to categorize findings as known-good, known-bad, or unknown, and produce an intermediate findings table that prioritizes items for manual deep-dive analysis. This is the first execution step — transform prepared queries into raw results, then distill those results into actionable leads.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify queries during execution without documenting the change and reason
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A THREAT HUNTER executing a systematic hunt plan, not an alert correlation engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Threat Hunter executing the hunt plan methodically — resist the urge to chase rabbit holes during automated analysis
- ✅ Document every query execution: what was run, what was returned, what was excluded
- ✅ Automated analysis identifies leads — it does not classify findings. Classification happens in step 6 after manual analysis confirms or denies
- ✅ Cross-data-source correlation is a force multiplier — the same entity appearing in multiple query results dramatically increases suspicion
- ✅ The goal is to reduce the haystack, not to find the needle — manual analysis finds the needle

### Step-Specific Rules:

- 🎯 Focus exclusively on query execution, pattern detection, automated triage, and intermediate findings documentation
- 🚫 FORBIDDEN to perform deep manual investigation of individual findings — that is step 5
- 🚫 FORBIDDEN to classify findings as confirmed malicious — automated analysis produces leads, not verdicts
- 💬 Approach: Systematic, phased execution with checkpoint documentation after each phase
- 📊 Every query execution must be documented with: results count, time range covered, data volume, performance metrics
- 🔒 Follow the execution plan from step 3 — do not add queries without operator approval

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Finding a known-bad indicator (exact IOC match) during automated analysis is urgent but should not derail the systematic hunt — document it, flag it for immediate manual analysis in step 5, but continue executing remaining queries. Abandoning the plan to chase a single finding may cause you to miss broader compromise indicators that would only appear in later queries.
  - Queries returning zero results may indicate a clean environment OR a logging gap — before accepting zero results as "hypothesis not supported," verify that the data source was actually logging during the hunt time window and that the query syntax correctly matches the field schema. Silent failures are the most dangerous outcome.
  - High-volume results (thousands of events) from a single query may indicate the query is too broad rather than indicating widespread malicious activity — review the query logic and baseline before concluding the environment is compromised. Apply frequency analysis and stack ranking to distinguish signal from noise.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Execute queries in the planned order from step 3, documenting results per query
- ⚠️ Checkpoint after each phase — save intermediate results before proceeding
- ⚠️ Present [A]/[W]/[C] menu after all automated analysis complete
- 💾 ONLY save to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to stepsCompleted and updating `queries_executed`, `data_volume_analyzed`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Hunt mission, hypotheses, all queries and baselines from steps 1-3, execution plan
- Focus: Query execution, pattern detection, automated triage, and intermediate findings — no deep manual analysis or final classification
- Limits: Only execute queries from the step 3 plan — do not add new queries without approval
- Dependencies: Completed data collection preparation from step-03-data-collection.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Execution Preparation

Confirm readiness before executing queries:

"**Hunt Execution — Pre-flight Check:**

| Check | Status |
|-------|--------|
| Execution plan loaded from step 3 | ✅/❌ |
| Total queries to execute | {{count}} |
| Execution phases planned | {{phase_count}} |
| Data sources confirmed accessible | {{count}} / {{total}} |
| Baselines loaded | {{count}} |
| Estimated total runtime | {{time}} |
| Operator confirmed ready to begin | Awaiting confirmation |

**Note:** Query execution begins once the operator confirms. Results will be documented per query with checkpoints between phases."

Wait for operator confirmation before proceeding with query execution.

### 2. Systematic Query Execution

Execute each query from the step 3 execution plan in the planned order. Document results per query:

"**Phase {{N}} Execution — {{phase description}}:**

---

**Query {{query_id}}: {{query purpose}}**

| Execution Detail | Value |
|-----------------|-------|
| Hypothesis | {{hypothesis_id}}: {{hypothesis_name}} |
| Data Source | {{specific log source}} |
| Time Range Covered | {{actual time range searched}} |
| Query Syntax Used | {{platform — Splunk/KQL/EQL/EDR}} |
| Events Returned | {{count}} |
| Data Volume Scanned | {{volume — e.g., "2.3 GB across 4.7M events"}} |
| Query Duration | {{seconds/minutes}} |
| Performance Impact | {{none observed / minor / moderate / significant}} |

**Raw Results Summary:**
```
{{Summary of results — top entries, distribution, key patterns. NOT full raw output unless small.}}
{{For large result sets: show statistical summary and top-N most interesting entries}}
```

**Baseline Comparison:**
- Expected baseline: {{normal range from step 3 baseline}}
- Actual observed: {{what was found}}
- Deviation: {{within baseline / slight deviation / significant deviation / extreme deviation}}

**Automated Triage:**
- Known-good (matches whitelist/baseline): {{count}} events → excluded
- Known-bad (matches IOC/signature): {{count}} events → **FLAGGED for immediate manual analysis**
- Unknown (no match either way): {{count}} events → queued for manual analysis

---

**Query {{next_query_id}}: {{query purpose}}**
{{Repeat per-query documentation}}

---

**Phase {{N}} Checkpoint:**
- Queries executed: {{count}} / {{phase_total}}
- Total events returned: {{count}}
- Known-good excluded: {{count}}
- Known-bad flagged: {{count}}
- Unknown queued: {{count}}
- Hypothesis status: {{trending toward confirmation / trending toward refutation / insufficient data / mixed signals}}

Save intermediate results to report."

### 3. Pattern Detection Techniques

Apply systematic pattern detection to the query results:

"**Pattern Detection Analysis:**

#### A. Frequency Analysis
Identify rare events — items occurring at unusually low frequency compared to baseline:

| Finding | Frequency | Baseline Frequency | Deviation | Hosts/Users Affected | Suspicion Level |
|---------|-----------|-------------------|-----------|---------------------|----------------|
| {{event/entity}} | {{count}} | {{baseline count}} | {{% deviation}} | {{list}} | {{High/Medium/Low}} |

**Rare event summary:** {{count}} events below the {{threshold}} percentile threshold.

#### B. Stack Ranking
Rank results by occurrence count — least frequent items are most interesting:

| Rank | Entity | Type | Count | % of Total | Notes |
|------|--------|------|-------|-----------|-------|
| 1 (rarest) | {{entity}} | {{process/domain/IP/hash}} | {{count}} | {{%}} | {{why this is interesting}} |
| 2 | ... | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

**Long-tail findings:** {{count}} entities appeared only once (unique occurrences warrant investigation).

#### C. Time-Series Analysis
Identify temporal patterns in the results:

| Pattern Type | Finding | Time Window | Affected Entities | Suspicion Level |
|-------------|---------|-------------|-------------------|----------------|
| Activity spike | {{description}} | {{when}} | {{hosts/users}} | {{High/Medium/Low}} |
| Off-hours activity | {{description}} | {{when}} | {{hosts/users}} | {{High/Medium/Low}} |
| Periodic pattern (automation) | {{description}} | {{interval}} | {{hosts/users}} | {{High/Medium/Low}} |
| Burst-then-silent | {{description}} | {{when}} | {{hosts/users}} | {{High/Medium/Low}} |

**Temporal anomaly summary:** {{count}} temporal anomalies identified across {{time_range}}.

#### D. Baseline Deviation Analysis
Compare current period results against established baselines from step 3:

| Metric | Baseline (Normal) | Current Period | Deviation | Statistical Significance | Suspicion Level |
|--------|-------------------|---------------|-----------|------------------------|----------------|
| {{metric}} | {{mean ± std_dev}} | {{current_value}} | {{+/-N std_dev}} | {{p-value or qualitative}} | {{High/Medium/Low}} |

**Baseline deviation summary:** {{count}} metrics outside 2 standard deviations from baseline.

#### E. Clustering Analysis
Group similar events and identify anomalous clusters:

| Cluster | Common Attributes | Event Count | Anomalous? | Reason |
|---------|-------------------|-------------|-----------|--------|
| C1 | {{shared attributes — same source, same dest, same process}} | {{count}} | ✅/❌ | {{why anomalous or normal}} |
| C2 | ... | ... | ... | ... |

**Cluster summary:** {{count}} clusters identified, {{anomalous_count}} flagged as anomalous.

#### F. Cross-Data-Source Correlation
Identify entities appearing across multiple query results from different data sources:

| Entity | Type | Appeared In | Query Results | Correlation Significance |
|--------|------|-------------|--------------|------------------------|
| {{entity — IP, hostname, username}} | {{type}} | {{list of data sources}} | {{list of query IDs}} | {{High — multi-source correlation / Medium — two sources / Low — single source}} |

**Cross-correlation summary:** {{count}} entities appeared in results from multiple data sources. Multi-source correlation dramatically increases confidence in findings."

### 4. Automated Triage Summary

Consolidate all automated findings into a prioritized table:

"**Automated Triage Results — Consolidated:**

| # | Finding ID | Source Query | Entity | Type | Category | Suspicion Level | Data Sources | Notes |
|---|-----------|-------------|--------|------|----------|----------------|-------------|-------|
| 1 | AF-001 | {{query_id}} | {{entity}} | {{process/IP/domain/hash/behavior}} | 🔴 Known-bad | Critical | {{count}} sources | {{brief note}} |
| 2 | AF-002 | {{query_id}} | {{entity}} | {{type}} | 🟡 Unknown | High | {{count}} sources | {{brief note}} |
| 3 | AF-003 | {{query_id}} | {{entity}} | {{type}} | 🟡 Unknown | Medium | {{count}} sources | {{brief note}} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Legend:**
- 🔴 **Known-bad:** Matches IOC, signature, or known malicious pattern — immediate manual analysis required
- 🟡 **Unknown:** No match to known-good or known-bad — requires manual investigation to classify
- 🟢 **Known-good:** Matches whitelist/baseline — excluded from further analysis (documented for audit)

**Triage Statistics:**
```
Total events analyzed: {{count}}
├── Known-good (excluded): {{count}} ({{%}})
├── Known-bad (flagged): {{count}} ({{%}})
└── Unknown (queued): {{count}} ({{%}})

Findings requiring manual analysis: {{count}}
├── Critical (known-bad): {{count}}
├── High suspicion (unknown, multi-source): {{count}}
├── Medium suspicion (unknown, single source): {{count}}
└── Low suspicion (unknown, weak indicator): {{count}}

Cross-data-source correlations: {{count}}
Timeline clusters identified: {{count}}
```"

### 5. Intermediate Hypothesis Assessment

Assess each hypothesis based on automated analysis results:

"**Hypothesis Status — Post-Automated Analysis:**

| Hypothesis | Status | Evidence Strength | Key Findings | Recommendation |
|-----------|--------|-------------------|-------------|----------------|
| H1: {{name}} | 🔴 Trending Confirmed / 🟡 Mixed Signals / 🟢 Trending Refuted / ⚪ Insufficient Data | {{Strong / Moderate / Weak / None}} | {{brief summary of relevant findings}} | {{Deep dive in step 5 / Deprioritize / Requires additional data}} |
| H2: {{name}} | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

**CRITICAL:** These are interim assessments. No hypothesis is confirmed or refuted until after manual analysis in step 5 and validation in step 6. Automated analysis identifies patterns — human analysis confirms meaning."

### 6. Execution Metrics

"**Automated Analysis Metrics:**

| Metric | Value |
|--------|-------|
| Queries executed | {{count}} / {{planned}} |
| Queries with results | {{count}} |
| Queries with zero results | {{count}} (verified: {{count}} confirmed clean, {{count}} potential logging gap) |
| Total events scanned | {{count}} |
| Total data volume | {{volume}} |
| Total execution time | {{duration}} |
| Findings for manual analysis | {{count}} |
| Phases completed | {{count}} / {{total}} |"

### 7. Present MENU OPTIONS

"**Automated analysis complete.**

Summary: {{queries_executed}} queries executed, {{events_scanned}} events analyzed, {{findings_count}} findings for manual analysis.
Known-bad: {{known_bad_count}} | Unknown: {{unknown_count}} | Known-good excluded: {{known_good_count}}
Cross-correlations: {{correlation_count}} | Temporal anomalies: {{temporal_count}}
Hypothesis trend: {{count}} trending confirmed | {{count}} mixed | {{count}} trending refuted | {{count}} insufficient data

**Select an option:**
[A] Advanced Elicitation — Deep review of automated findings, challenge triage decisions, identify missed patterns
[W] War Room — Red vs Blue discussion on automated findings and adversary implications
[C] Continue — Proceed to Manual Analysis (Step 5 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive automated results — challenge the known-good exclusions (could an adversary blend into normal activity?), examine zero-result queries for logging gaps, review cross-correlations for hidden patterns, assess whether the frequency analysis thresholds are appropriate, identify queries that should be modified and re-run based on initial results. Process insights, ask user if they want to re-run or add queries, if yes execute and update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: looking at these results, which findings would concern me most as an attacker? Which of my activities might have been caught? Which findings are noise that would distract the hunter? If the automated analysis missed me, what queries would I worry about in manual analysis? Blue Team perspective: are our triage thresholds appropriate? Are we excluding too aggressively (missing low-and-slow attacks)? Are the cross-correlations meaningful or coincidental? What additional queries would strengthen the weak hypotheses? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `queries_executed`, `data_volume_analyzed`. Append automated analysis results to report under `## Automated Analysis Results`. Then read fully and follow: ./step-05-manual-analysis.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and queries_executed and data_volume_analyzed updated, and automated analysis results appended to report under `## Automated Analysis Results`], will you then read fully and follow: `./step-05-manual-analysis.md` to begin manual deep-dive analysis.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All planned queries executed in the defined order with per-query documentation
- Checkpoints saved between execution phases with intermediate results
- Pattern detection techniques applied systematically: frequency analysis, stack ranking, time-series, baseline deviation, clustering, cross-data-source correlation
- Automated triage performed on all results: known-good excluded, known-bad flagged, unknown queued
- Findings prioritized by suspicion level with cross-data-source correlation highlighted
- Zero-result queries verified for logging gaps vs genuine absence of activity
- Intermediate hypothesis assessment presented with evidence strength and recommendation
- Execution metrics documented (queries, events, volume, duration, findings)
- All automated analysis results appended to report under `## Automated Analysis Results`
- Frontmatter updated with queries_executed, data_volume_analyzed, and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Executing queries out of the planned order without documenting the change
- Not documenting per-query execution results (events returned, time range, volume, performance)
- Classifying findings as "confirmed malicious" during automated analysis (automated produces leads, not verdicts)
- Accepting zero results without verifying data source health and query syntax
- Not applying pattern detection techniques (just reporting raw query results is not analysis)
- Not performing cross-data-source correlation (individual query results without correlation miss multi-source patterns)
- Abandoning the execution plan to chase individual findings (document and flag, but continue systematic execution)
- Not saving checkpoint data between execution phases
- Deep-diving into individual findings (that's step 5's job)
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Automated analysis is systematic and documented. It produces prioritized leads for manual investigation, not final conclusions. Every query executed, every result documented, every finding triaged.
