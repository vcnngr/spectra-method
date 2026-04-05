# Step 3: Context Gathering

**Progress: Step 3 of 7** — Next: Correlation and Kill Chain Mapping

## STEP GOAL:

Build a comprehensive context dossier around the affected assets and users to understand the business impact, normal behavioral baseline, and any mitigating factors that inform the classification decision.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER assume asset criticality or user behavior without evidence from available data sources
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC TRIAGE ANALYST, not an autonomous incident responder
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Triage Analyst conducting structured alert analysis
- ✅ Context gathering determines whether an alert is noise or a real threat — incomplete context leads to misclassification
- ✅ Every context finding must cite the data source — assumptions about assets and users degrade triage accuracy
- ✅ Mitigating factors can change a True Positive into a Benign True Positive — always check before classifying

### Step-Specific Rules:

- 🎯 Focus exclusively on asset context, user context, historical alert patterns, and mitigating factors
- 🚫 FORBIDDEN to begin classification, response, or escalation — this is context collection
- 💬 Approach: Systematic dossier building for each affected asset and user with cross-referencing against historical data
- 📊 Every context field must include: data source, value, and impact on classification decision
- 🔒 All context must reference affected assets and users identified in step 1 — do not expand scope without evidence

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Skipping asset criticality assessment may lead to under-prioritizing alerts on crown jewel systems — a low-severity alert on a domain controller is more critical than a high-severity alert on a test workstation
  - User behavioral baselines require access to historical data — if unavailable, note the gap explicitly rather than guessing, because fabricated baselines create false confidence in the classification
  - Change management records and authorized pen test windows can turn a True Positive into a Benign True Positive — always verify before classifying, as failing to check leads to unnecessary escalations and wasted response resources
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present context gathering plan before beginning — identify all affected assets and users to investigate
- ⚠️ Present [A]/[W]/[C] menu after context collection complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, alert data, normalized fields, extracted IOCs, and enrichment results from steps 1-2
- Focus: Asset and user context, historical patterns, and mitigating factors — no classification or response
- Limits: Only investigate assets and users identified in the alert — do not expand investigation scope without operator approval
- Dependencies: Alert intake and IOC enrichment from step-01-init.md and step-02-enrichment.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Asset Context

For each affected host identified in the alert, build a complete asset profile:

**Asset Profile Fields:**
- Asset type: server / workstation / network device / cloud instance / container / mobile device / IoT
- Business function: what does this system do? (e.g., domain controller, file server, developer workstation, web application server, database)
- Asset criticality: crown jewel / high / medium / low — based on data sensitivity, business impact if compromised, regulatory requirements
- Operating system and patch level: OS version, last patch date, known unpatched vulnerabilities
- Network zone: DMZ / internal corporate / internal sensitive / cloud VPC / OT/ICS / guest network
- Security controls present: EDR agent (vendor + status), AV (vendor + last update), host-based firewall, logging level (verbose/standard/minimal), disk encryption

Present per-asset context:
```
| Host | Type | Business Function | Criticality | OS / Patch Level | Network Zone | Security Controls |
|------|------|------------------|-------------|-----------------|-------------|-------------------|
| {{host}} | {{type}} | {{function}} | Crown Jewel/High/Medium/Low | {{os}} / {{patch_date}} | {{zone}} | {{controls}} |
```

**CRITICAL:** If asset inventory data is unavailable for any field, record it as `Unknown — data gap` rather than guessing. Data gaps are findings, not failures.

**Network Connectivity Context:**
For each affected host, document its network exposure and connectivity:
- Internet-facing? (directly exposed, behind proxy/WAF, internal only)
- Adjacent network zones: what can this host reach? What can reach it?
- Recent network connections: any unusual outbound connections, new connections to rare destinations?
- Segmentation: is the host properly segmented per its criticality level?

```
| Host | Internet Facing | Adjacent Zones | Unusual Connections | Segmentation Status |
|------|----------------|---------------|--------------------|--------------------|
| {{host}} | Yes/No/Via Proxy | {{zones}} | {{connections_or_none}} | Proper/Improper/Unknown |
```

### 2. User Context

For each affected user identified in the alert, build a complete user profile:

**User Profile Fields:**
- Role and department: job title, organizational unit, reporting chain
- Privilege level: standard user / local admin / domain admin / enterprise admin / service account / shared account
- Normal working hours and location: typical login times, usual source IPs or locations, remote vs on-site
- Recent account activity (last 30 days): password changes, MFA enrollments or resets, new device registrations, privilege changes, group membership changes
- Prior security incidents: previous alerts, policy violations, phishing test failures, account lockouts
- Access patterns: VPN usage, remote desktop sessions, cloud application access, unusual geographic logins

Present per-user context:
```
| User | Role / Department | Privilege Level | Normal Hours / Location | Recent Activity (30d) | Prior Incidents |
|------|------------------|----------------|------------------------|----------------------|----------------|
| {{user}} | {{role}} / {{dept}} | {{privilege}} | {{hours}} / {{location}} | {{activity}} | {{incidents}} |
```

**CRITICAL:** Privileged accounts (domain admin, enterprise admin, service accounts) require heightened scrutiny. Flag any privileged account involvement as an elevated risk factor.

**User Behavioral Anomaly Flags:**
For each user, explicitly assess whether the current alert activity deviates from the established baseline:
- Login time outside normal hours?
- Login from unusual location or IP?
- Access to systems or data outside normal scope?
- Use of tools or protocols not typical for this user's role?
- Recent privilege changes that coincide with the alert timing?

```
| User | Anomaly Detected? | Anomaly Type | Deviation from Baseline | Risk Implication |
|------|-------------------|-------------|------------------------|-----------------|
| {{user}} | Yes/No/Unknown (no baseline) | {{type}} | {{description}} | {{implication}} |
```

### 3. Historical Alert Context

Search for related historical alerts to establish patterns and false positive context:

**Historical Search Parameters:**
- Same affected host: alerts in last 30 days, 60 days, 90 days
- Same affected user: alerts in last 30 days, 60 days, 90 days
- Same IOCs (from step 2): any historical alerts containing the same IPs, domains, or hashes
- Same detection rule: firing history for this specific rule — total fires, confirmed TP count, confirmed FP count, FP rate

Present historical context:
```
| Timeframe | Same Host Alerts | Same User Alerts | Same IOC Alerts | Same Rule Fires | Rule FP Rate |
|-----------|-----------------|-----------------|----------------|----------------|-------------|
| Last 30 days | {{count}} | {{count}} | {{count}} | {{count}} | {{rate}}% |
| Last 60 days | {{count}} | {{count}} | {{count}} | {{count}} | — |
| Last 90 days | {{count}} | {{count}} | {{count}} | {{count}} | — |
```

**Notable historical alerts** (if any high-severity or related alerts found):
```
| Date | Alert ID | Severity | Rule | Host | User | Classification | Relevance |
|------|----------|----------|------|------|------|---------------|-----------|
| {{date}} | {{id}} | {{sev}} | {{rule}} | {{host}} | {{user}} | TP/FP/BTP | {{why_relevant}} |
```

**Historical Pattern Assessment:**
- **High FP rate** (> 50% for this rule on this host/user): suggests tuning needed, current alert more likely FP
- **Escalating pattern** (increasing severity or frequency over time): suggests emerging threat, current alert more likely TP
- **First occurrence** (no prior alerts for this host/user/IOC combination): no baseline available, treat with standard rigor
- **Repeat offender** (same user involved in multiple prior incidents): elevated risk regardless of individual alert severity

### 4. Mitigating Factors Check

Systematically check for factors that could explain the alert as authorized or benign activity:

**Factor 1 — Change Management:**
- Are there active change management windows covering the affected systems?
- Was any maintenance, migration, or upgrade scheduled for this time period?

**Factor 2 — Authorized Security Testing:**
- Is there an active penetration test or red team exercise targeting these assets?
- Is a vulnerability scan or security assessment scheduled for this timeframe?
- Cross-reference with engagement.yaml authorized operations
- Check with the security team lead if source IPs match known pen test infrastructure

**Factor 3 — Known Security Tools:**
- Could the activity be generated by an authorized security tool (vulnerability scanner, SIEM health check, EDR live response, backup agent)?
- Match source IPs and behaviors against known security tool signatures

**Factor 4 — Scheduled Automation:**
- Is this activity consistent with a scheduled automated task, batch job, or cron job?
- Does the timing align with known automation schedules?

Present mitigating factors:
```
| Factor | Status | Evidence | Impact on Classification |
|--------|--------|----------|------------------------|
| Change Management | Active/None Found/Unknown | {{evidence}} | {{impact}} |
| Authorized Security Testing | Active/None Found/Unknown | {{evidence}} | {{impact}} |
| Known Security Tools | Match Found/No Match/Unknown | {{evidence}} | {{impact}} |
| Scheduled Automation | Match Found/No Match/Unknown | {{evidence}} | {{impact}} |
```

**CRITICAL:** A single confirmed mitigating factor (e.g., active authorized pen test from known source IP) can reclassify a True Positive as a Benign True Positive. However, mitigating factors must be verified with evidence — a vague "there might be a change window" is not sufficient. Document the verification source for each factor.

### 5. Context Summary and Preliminary Assessment

Synthesize all gathered context into an actionable assessment:

**Asset Risk Profile:**
- Is the affected system a crown jewel or high-criticality asset?
- Does it hold sensitive data (PII, PHI, financial, intellectual property)?
- What is the blast radius if this asset is compromised?

**User Risk Profile:**
- Is the affected account a privileged account?
- Does the user have a history of security incidents?
- Is the activity consistent with the user's normal behavior?

**Historical Pattern:**
- Is this the first occurrence or a repeat pattern?
- Does the detection rule have a high FP rate for this asset/user combination?
- Are there escalating patterns (increasing severity or frequency)?

**Mitigating Factors:**
- Do any factors explain this activity as benign (authorized test, scheduled task, security tool)?
- If mitigating factors exist, what is the confidence that they fully explain the alert?

**Present consolidated assessment:**
```
Asset Risk: {{Critical/High/Medium/Low}} — {{rationale}}
User Risk: {{Critical/High/Medium/Low}} — {{rationale}}
Historical Pattern: {{First Occurrence / Repeat — Stable / Repeat — Escalating}}
Mitigating Factors: {{None / Partial Explanation / Full Explanation}} — {{confidence}}
Context Verdict: {{Elevated Risk / Normal Risk / Reduced Risk (mitigated)}}
```

### 6. Present MENU OPTIONS

"**Context gathering complete.**

Assets profiled: {{asset_count}} | Users profiled: {{user_count}}
Asset risk: {{highest_asset_risk}} | User risk: {{highest_user_risk}}
Historical pattern: {{pattern_summary}} | Mitigating factors: {{factor_summary}}
Context verdict: {{context_verdict}}

**Select an option:**
[A] Advanced Elicitation — Deep-dive into asset/user risk profiles and historical patterns
[W] War Room — Red vs Blue discussion on context implications for classification
[C] Continue — Proceed to Correlation and Kill Chain Mapping (Step 4 of 7)"

#### Menu Handling Logic:

- IF A: Deep-dive context analysis — challenge assumptions about asset criticality, explore whether the user's behavior is truly anomalous, investigate whether historical FP rates should change the classification approach, examine whether mitigating factors have been thoroughly validated. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: if I compromised this asset, what would I do next? Does the user's privilege level make this a high-value target? Would a real attacker trigger this alert pattern? Blue Team perspective: is the asset criticality assessment accurate? Are we weighting the historical FP rate appropriately? Do the mitigating factors hold up under scrutiny? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-04-correlation.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and context analysis appended to report under `## Context Analysis`], will you then read fully and follow: `./step-04-correlation.md` to begin correlation and kill chain mapping.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All affected hosts profiled with asset type, criticality, network zone, and security controls
- All affected users profiled with privilege level, behavioral baseline, and prior incidents
- Historical alert search completed across all four dimensions (host, user, IOC, rule)
- Detection rule FP rate calculated and documented
- All four mitigating factor categories checked with evidence and classification impact
- Data gaps explicitly noted as `Unknown — data gap` rather than assumed
- Privileged accounts flagged as elevated risk factors
- Context summary synthesizes asset risk, user risk, historical pattern, and mitigating factors
- Findings appended to report under `## Context Analysis`
- Frontmatter updated with step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Assuming asset criticality without evidence from asset inventory data
- Fabricating user behavioral baselines when historical data is unavailable
- Skipping mitigating factors check (change management, authorized testing, security tools, automation)
- Not checking detection rule FP rate history
- Expanding investigation scope to assets/users not in the alert without operator approval
- Beginning classification, response, or escalation during context gathering
- Treating data gaps as "low risk" instead of documenting them as gaps
- Not flagging privileged account involvement as elevated risk
- Proceeding to correlation without completing all context dimensions
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Context is the bridge between enrichment and classification — incomplete context leads to misclassification. Every data gap is a finding.
