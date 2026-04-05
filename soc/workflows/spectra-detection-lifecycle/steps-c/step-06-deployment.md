# Step 6: Deployment Planning

**Progress: Step 6 of 7** — Next: Coverage Assessment, Purple Team Feedback, and Closure

## STEP GOAL:

Create a complete deployment plan for the validated detection rule — target platform selection, alert routing, severity mapping, runbook linkage, monitoring baselines, and rollback criteria — converting the validated rule into an operational detection deployed with full operational readiness.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER deploy a rule without a validated quality gate from Step 5 — deployment without validation is operational negligence
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DETECTION ENGINEER, not an automated deployment tool — you plan deployments with operator oversight and operational awareness
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Detection Engineer collaborating with an expert peer on deployment planning within an active security engagement
- ✅ A validated detection rule is useless until it is deployed, configured, and monitored in the production environment — deployment planning is the bridge between validation and value
- ✅ Alert configuration is not just "turn it on" — severity, throttling, grouping, enrichment, routing, and runbook linkage determine whether analysts can act on the alert or drown in noise
- ✅ Every deployment must have a rollback plan — rules that misbehave in production must be disabled quickly and safely without requiring emergency debugging
- ✅ Monitoring baselines define "normal" for the rule — without baselines, anomalous rule behavior (FP spikes, volume surges) goes undetected

### Step-Specific Rules:

- 🎯 Focus exclusively on platform selection, rule conversion, alert configuration, monitoring baselines, deployment scheduling, and rollback planning
- 🚫 FORBIDDEN to re-validate the rule — validation was completed in Step 5
- 🚫 FORBIDDEN to execute the deployment — this step produces the deployment PLAN, the operator or change management process executes it
- 💬 Approach: Structured deployment planning with explicit platform compatibility assessment, alert configuration rationale, and operational readiness checklist
- 📊 Every alert configuration setting must include rationale — arbitrary severity, throttling, or routing decisions create operational confusion
- 🔒 Rollback criteria must be specific and measurable — "disable if it causes problems" is not a rollback plan

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Deploying directly to full alerting without a shadow or detection-only period — warn about unknown production FP rate variance; validation was performed on a limited dataset, and production traffic patterns may trigger false positives not seen during testing; recommend staged deployment with a detection-only period before enabling alerting
  - No rollback criteria defined — warn about operational risk if the rule misbehaves in production; without pre-defined auto-disable thresholds, a runaway rule can flood the SOC queue for hours before someone notices and manually disables it; propose automatic rollback triggers based on alert volume and FP rate
  - Alert routing to L1 for a high-complexity detection requiring deep forensic analysis — warn about analyst capability mismatch; L1 analysts may not have the skills or tools to properly triage this alert type, leading to misclassification or unnecessary escalation; recommend L2/L3 routing with L1 triage guidance as a fallback
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present platform assessment before any configuration planning
- ⚠️ Present [A]/[W]/[C] menu after deployment plan is complete with rollback criteria
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `deployment_target`, `deployment_mode`, and `rollback_defined`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Detection requirement from Step 1, threat analysis from Step 2, detection rule(s) from Step 3, test cases from Step 4, validation results and quality gate from Step 5
- Focus: Platform compatibility, rule conversion, alert configuration, monitoring baselines, deployment scheduling, and rollback planning
- Limits: Do not re-validate, do not execute deployment, do not begin coverage assessment (Step 7)
- Dependencies: Quality gate assessment from step-05-validation.md with verdict of READY or CONDITIONAL (NOT READY blocks deployment)

## CRITICAL PREREQUISITE:

**This step is executed ONLY for rules with READY or CONDITIONAL quality gate verdict from Step 5.**

If the quality gate verdict was NOT READY, deployment planning is blocked. The workflow should return to Step 3 for rule rework. If you arrived here, the quality gate is READY or CONDITIONAL.

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Target Platform Assessment

Evaluate the detection rule against the organization's security platform stack. Not every rule format runs natively on every platform — conversion may be required.

**Present platform compatibility assessment:**

```
TARGET PLATFORM ASSESSMENT — {{rule_id}}
═════════════════════════════════════════

Rule format: {{sigma / yara / suricata}}
Quality gate: {{READY / CONDITIONAL}}
```

```
| Platform | Type | Compatibility | Conversion Needed | Limitations | Status |
|----------|------|--------------|-------------------|-------------|--------|
| {{platform_1}} | SIEM | Native / Requires conversion | {{converter / manual}} | {{field mapping, unsupported features}} | Primary / Secondary / N/A |
| {{platform_2}} | EDR | Native / Requires conversion | {{converter / manual}} | {{limitations}} | Primary / Secondary / N/A |
| {{platform_3}} | Network | Native / Requires conversion | {{converter / manual}} | {{limitations}} | Primary / Secondary / N/A |
```

**Common platform targets:**

| Category | Platforms |
|----------|-----------|
| SIEM | Splunk, Microsoft Sentinel, Elastic Security, IBM QRadar, Google Chronicle, Sumo Logic |
| EDR | CrowdStrike Falcon, Microsoft Defender for Endpoint, SentinelOne, Carbon Black, Cortex XDR |
| Network Security | Suricata, Snort, Zeek |
| Cloud Security | AWS GuardDuty, Azure Defender, GCP Security Command Center |

**Selected deployment target(s):**
```
Primary target: {{platform}} — {{justification}}
Secondary target: {{platform or "N/A"}} — {{justification}}
```

### 2. Rule Conversion (IF NEEDED)

If the detection rule format does not natively run on the target platform, perform format conversion and document any detection logic changes.

**Present conversion details:**

```
RULE CONVERSION — {{rule_id}}
═════════════════════════════

Source format: {{sigma / yara / suricata}}
Target format: {{SPL / KQL / EQL / Lucene / platform-specific}}
Conversion method: {{sigma-cli / manual / sigmac / uncoder.io / custom converter}}
```

**Converted Rule:**
```
{{converted rule in target platform syntax}}
```

**Conversion Fidelity Assessment:**

```
┌─────────────────────────┬───────────────────────────────────────────────┐
│ Logic Element           │ Fidelity                                     │
├─────────────────────────┼───────────────────────────────────────────────┤
│ Selection conditions    │ Preserved / Modified — {{detail}}            │
│ Field mappings          │ Preserved / Modified — {{field changes}}     │
│ Logical operators       │ Preserved / Modified — {{AND/OR/NOT changes}}│
│ Aggregation/timeframe   │ Preserved / Modified / LOST — {{detail}}     │
│ Regular expressions     │ Preserved / Modified / LOST — {{detail}}     │
│ Negation/exclusions     │ Preserved / Modified — {{detail}}            │
└─────────────────────────┴───────────────────────────────────────────────┘
```

**If any logic was MODIFIED or LOST:**
```
⚠️ CONVERSION LOGIC CHANGE
Element: {{what changed}}
Impact: {{what attacks may be missed or what FPs may increase}}
Recommendation: {{re-validate with platform-specific tests / accept with documentation / redesign for target platform}}
```

**If conversion is not needed (native format):**
"**No conversion required.** Rule format {{format}} runs natively on {{platform}}. Proceeding to alert configuration."

### 3. Alert Configuration

Define the complete alert configuration for the deployed rule. Every setting must include a rationale — arbitrary configuration creates operational confusion when analysts need to understand why the alert behaves as it does.

**Present alert configuration:**

```
ALERT CONFIGURATION — {{rule_id}}
══════════════════════════════════
```

```
┌──────────────────┬───────────────────────────────────────┬──────────────────────────────────┐
│ Setting          │ Value                                │ Rationale                        │
├──────────────────┼───────────────────────────────────────┼──────────────────────────────────┤
│ Alert name       │ {{descriptive_name — must be unique  │ Clear identification in SOC      │
│                  │ and immediately informative}}        │ queue                            │
│ Alert ID         │ {{rule_id from Step 1}}              │ Traceability to detection        │
│                  │                                      │ lifecycle                        │
│ Severity         │ {{Critical/High/Medium/Low/Info}}    │ Matches rule level from Step 3   │
│                  │                                      │ — {{justification}}              │
│ Throttling       │ {{time_window — e.g., 1 alert per   │ Prevents alert flood during      │
│                  │ host per 15 min}}                    │ sustained attack or noisy period │
│ Grouping         │ {{by host / by user / by source IP / │ Groups related alerts to reduce  │
│                  │ by technique}}                       │ analyst context-switching        │
│ Enrichment       │ {{auto-enrich fields — GeoIP,       │ Pre-populates context so analyst │
│                  │ asset lookup, user context, threat   │ does not need manual lookups     │
│                  │ intel}}                              │                                  │
│ Routing          │ {{queue / team — L1 triage, L2       │ Based on alert complexity and    │
│                  │ investigation, L3 hunt}}             │ severity                         │
│ Notification     │ {{email / Slack / PagerDuty /        │ Based on severity — critical     │
│                  │ SOAR / none}}                        │ requires immediate notification  │
│ Runbook          │ {{link to response procedure or      │ Analyst guidance for triage and  │
│                  │ "CREATE NEW" with outline}}          │ response                         │
│ Tags             │ {{MITRE tactic, technique, data      │ Enables filtering and reporting  │
│                  │ source, campaign if applicable}}     │                                  │
│ Correlation      │ {{link to related rules for          │ Enables multi-rule correlation   │
│                  │ multi-stage detection, or "N/A"}}    │ in SIEM                          │
└──────────────────┴───────────────────────────────────────┴──────────────────────────────────┘
```

**Throttling Design:**
- Purpose: Prevent alert storms during sustained adversary activity or recurring FP patterns
- Window: {{time_period}} — selected because {{justification based on technique speed and expected frequency}}
- Grouping field: {{field}} — alerts grouped by this field share the same context and should be reviewed together
- Risk: Throttling may suppress alerts if the attacker pivots to a different host/user within the throttle window — accepted risk with {{mitigation}}

**Runbook Outline (if CREATE NEW):**
```
Runbook: {{rule_name}} — Triage Guide
1. Initial Assessment: {{what to check first when this alert fires}}
2. Context Gathering: {{what additional data to pull — user activity, host baseline, related alerts}}
3. True/False Positive Determination: {{specific criteria to distinguish TP from FP for this rule}}
4. Known FP Patterns: {{list from Step 3 falsepositives section — analyst should check these first}}
5. Escalation Criteria: {{when to escalate and to whom}}
6. Containment Actions: {{if TP confirmed — immediate actions per alert type}}
7. Evidence Preservation: {{what to capture before containment}}
```

### 4. Monitoring Baseline

Define what "normal" looks like for this rule post-deployment. Without baselines, anomalous rule behavior goes undetected until it causes visible damage (analyst fatigue, missed alerts, or SOC queue flooding).

**Present monitoring baseline:**

```
MONITORING BASELINE — {{rule_id}}
══════════════════════════════════
```

```
┌───────────────────────────┬────────────────────────┬────────────────────────┬─────────────────────────────────────┐
│ Metric                    │ Expected Baseline      │ Alert Threshold        │ Action When Exceeded               │
├───────────────────────────┼────────────────────────┼────────────────────────┼─────────────────────────────────────┤
│ Daily alert volume        │ {{expected_count}}     │ >{{N}}x baseline       │ Review for FP spike or active       │
│                           │                        │                        │ campaign — if FP: initiate tuning   │
│ FP rate (weekly review)   │ <{{target}}%           │ >{{threshold}}%        │ Initiate tuning cycle — return to   │
│                           │                        │                        │ Step 5 process                      │
│ Mean time to triage       │ <{{minutes}} min       │ >{{threshold}} min     │ Review alert quality and runbook    │
│                           │                        │                        │ — may need enrichment or context    │
│ Unique hosts triggering   │ {{expected_count}}     │ >{{N}} in {{timeframe}}│ Possible campaign — escalate to     │
│                           │                        │                        │ hunt team for investigation         │
│ Unique users triggering   │ {{expected_count}}     │ >{{N}} in {{timeframe}}│ Possible credential compromise      │
│                           │                        │                        │ campaign — escalate                 │
│ Analyst feedback (monthly)│ Useful / Actionable    │ "Noise" / "Ignore"     │ Immediate tuning review — analyst   │
│                           │                        │                        │ trust erosion detected              │
└───────────────────────────┴────────────────────────┴────────────────────────┴─────────────────────────────────────┘
```

**Baseline Derivation:**
- Daily volume estimate based on: {{validation data from Step 5 / environment size / technique prevalence}}
- FP rate baseline: {{actual rate from Step 5 validation}}
- Triage time estimate: {{based on alert complexity and runbook availability}}
- Host/user trigger expectations: {{based on environment profile and technique scope}}

**Baseline Review Schedule:**
- Week 1: Daily review of alert volume and FP rate (new rule stabilization)
- Weeks 2-4: Bi-weekly review
- Month 2+: Monthly review aligned with detection health reporting cycle
- Event-triggered: Immediate review on any threshold breach

### 5. Deployment Schedule

Recommend the deployment approach based on the quality gate verdict and operational context.

**Present deployment schedule:**

```
DEPLOYMENT SCHEDULE — {{rule_id}}
══════════════════════════════════
```

**Deployment Approach Options:**

```
┌─────────────┬──────────────────────────────────────────────────────────────┐
│ Approach    │ When to Use                                                │
├─────────────┼──────────────────────────────────────────────────────────────┤
│ Immediate   │ Critical detection gap, no alternative coverage, rule is   │
│             │ READY with high confidence                                 │
│ Staged      │ Deploy in detection-only mode (log but don't alert) for N  │
│             │ days, then enable alerting after confirming production FP   │
│             │ rate matches validation                                    │
│ Scheduled   │ Deploy during next maintenance window — non-urgent gap,    │
│             │ change management required                                 │
│ Conditional │ Deployment blocked on prerequisite — data source not yet   │
│             │ enabled, platform upgrade required, dependent rule needed  │
└─────────────┴──────────────────────────────────────────────────────────────┘
```

**Selected approach: {{approach}}**

```
┌──────────────────────┬─────────────────────────────────────────────────────┐
│ Deployment Detail    │ Value                                              │
├──────────────────────┼─────────────────────────────────────────────────────┤
│ Deployment date      │ {{date or "upon prerequisite completion"}}         │
│ Deployment window    │ {{time window — e.g., "next change window" or      │
│                      │ "immediately"}}                                    │
│ Initial mode         │ {{alerting / detection-only / shadow}}             │
│ Monitoring period    │ {{N days in detection-only before full alerting}}  │
│ Full enablement date │ {{date or "after monitoring period confirms        │
│                      │ baseline"}}                                        │
│ Approval required    │ {{SOC manager / detection engineering lead /       │
│                      │ change advisory board / none}}                     │
│ Deployment owner     │ {{who executes the deployment}}                    │
│ Notification         │ {{who is notified when rule goes live}}            │
│ Prerequisites        │ {{data sources, platform version, dependent        │
│                      │ rules, runbook completion}}                        │
└──────────────────────┴─────────────────────────────────────────────────────┘
```

**If CONDITIONAL quality gate (from Step 5):**
```
⚠️ CONDITIONAL DEPLOYMENT REQUIREMENTS:
{{List conditions from Step 5 quality gate that must be met or monitored during deployment}}

1. {{condition_1 — with how it will be verified during deployment}}
2. {{condition_2 — with monitoring approach}}
```

### 6. Rollback Plan

Define specific, measurable rollback triggers and procedures. Rollback must be executable without requiring root cause analysis — disable first, investigate after.

**Present rollback plan:**

```
ROLLBACK PLAN — {{rule_id}}
════════════════════════════
```

**Automatic Rollback Triggers (rule should be auto-disabled if ANY trigger fires):**

```
┌─────────────────────────────────────────────────┬──────────────────────────┐
│ Trigger                                         │ Threshold                │
├─────────────────────────────────────────────────┼──────────────────────────┤
│ FP rate exceeds target by 2x                    │ >{{2 × target}}%        │
│ Alert volume exceeds baseline by {{N}}x          │ >{{N}}x daily baseline  │
│                                                 │ sustained for {{hours}}  │
│ SIEM performance impact detected                │ Query time >{{threshold}}│
│ Analyst override: rule marked "useless" by      │ {{N}} analysts in        │
│ multiple analysts                               │ {{timeframe}}            │
└─────────────────────────────────────────────────┴──────────────────────────┘
```

**Manual Rollback Triggers:**
- SOC manager decision based on analyst feedback
- Detection engineering team review identifies logic flaw
- Change in environment renders rule obsolete (e.g., monitored application decommissioned)
- Platform migration renders rule incompatible

**Rollback Procedure:**
```
1. DISABLE rule on {{platform}} — {{specific disable procedure or API call}}
2. NOTIFY: {{SOC team / detection engineering / management}} — "Rule {{rule_id}} disabled due to {{trigger}}"
3. DOCUMENT: Open tuning ticket with trigger details, alert samples, and impact assessment
4. INVESTIGATE: Root cause analysis of rollback trigger
5. REMEDIATE: Apply fix per root cause
6. RE-VALIDATE: Return to Step 5 — execute full validation cycle on modified rule
7. RE-DEPLOY: Follow Step 6 deployment schedule for re-deployment
```

**Recovery Time Objective:**
- Rule disable: <{{minutes}} minutes from trigger detection
- Team notification: <{{minutes}} minutes from disable
- Tuning ticket opened: <{{hours}} hours from disable
- Root cause analysis: <{{days}} business days
- Re-validation and re-deployment: Per Steps 5-6 standard timeline

### 7. Append Deployment Plan to Report and Present Menu

"**Deployment planning complete.**

Rule: {{rule_id}} — {{rule_title}}
Target platform: {{platform}} ({{native / converted}})
Deployment mode: {{alerting / detection-only / shadow}}
Deployment date: {{date or condition}}
Alert routing: {{L1/L2/L3}} via {{notification_channel}}
Monitoring period: {{N}} days
Rollback triggers: {{count}} automatic, {{count}} manual
Runbook: {{link or "CREATE NEW — outline provided"}}

**Select an option:**
[A] Advanced Elicitation — Challenge deployment assumptions, alert configuration, and rollback readiness
[W] War Room — Red (how would I exploit this deployment window?) vs Blue (is the SOC ready for this alert?)
[C] Continue — Proceed to Coverage Assessment, Purple Team Feedback, and Closure (Step 7 of 7)"

#### Menu Handling Logic:

- IF A: Deep-dive deployment analysis — challenge whether the alert configuration settings are appropriate for the environment (is severity too high/low? is throttling too aggressive/permissive?), evaluate whether the monitoring baseline is realistic or optimistic, stress-test rollback triggers for completeness (what scenario is NOT covered?), assess whether the deployment schedule allows adequate monitoring before full enablement, evaluate whether the runbook is detailed enough for the routing tier. Process insights, ask user if they want to revise the deployment plan, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: how would I exploit the detection-only monitoring period to operate freely? Would I notice this new rule deploying (alert name in the environment, behavioral change in SOC response)? Can I trigger the rollback by intentionally flooding FPs to get the rule auto-disabled? What would I do in the window between rule disable and re-deployment? Blue Team perspective: is the SOC team briefed on this new alert? Will L1 analysts know what to do when it fires? Is the monitoring baseline conservative enough to catch real anomalies? Does the rollback plan leave us blind during the recovery period, and if so, what compensating visibility do we have? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `deployment_target` to platform name, `deployment_mode` to selected mode, and `rollback_defined` to true, then read fully and follow: ./step-07-closure.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, deployment_target, deployment_mode, and rollback_defined updated, and Deployment Plan section appended to report with platform assessment, alert configuration, monitoring baseline, deployment schedule, and rollback plan], will you then read fully and follow: `./step-07-closure.md` to complete the workflow with coverage assessment, Purple Team feedback, and closure.

---

## 🚨 SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Target platform assessed for compatibility with rule format and conversion needs documented
- Rule conversion (if needed) includes fidelity assessment with any logic changes flagged
- Alert configuration includes all required settings (name, severity, throttling, grouping, enrichment, routing, notification, runbook, tags)
- Every alert configuration setting includes rationale — no arbitrary values
- Monitoring baseline defined with expected values, alert thresholds, and actions when exceeded
- Baseline review schedule defined (daily during stabilization, weekly, monthly)
- Deployment approach selected with justification (immediate, staged, scheduled, conditional)
- Deployment schedule includes date, mode, monitoring period, approval, and prerequisites
- CONDITIONAL quality gate conditions carried forward into deployment requirements
- Rollback triggers defined with specific, measurable thresholds (not vague "if it causes problems")
- Rollback procedure documented with disable steps, notification targets, and recovery timeline
- Runbook provided or outlined for analyst guidance
- Frontmatter updated with deployment_target, deployment_mode, and rollback_defined
- Deployment Plan section appended to detection report
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Planning deployment for a rule with NOT READY quality gate — deployment is blocked until rework
- Deploying directly to alerting without assessing whether staged/detection-only deployment is more appropriate
- Alert configuration without rationale — arbitrary severity, throttling, or routing is operationally opaque
- No monitoring baseline — without expected values, anomalous rule behavior is invisible
- No rollback plan — rules without rollback criteria leave the SOC vulnerable to runaway alerts
- Rollback triggers that are vague or immeasurable (e.g., "disable if analysts complain")
- Not assessing platform compatibility or conversion fidelity — deploying a converted rule without checking for logic loss
- Executing the deployment during this step — deployment planning produces the PLAN, not the action
- Beginning coverage assessment or closure during deployment planning — that is Step 7
- Not carrying CONDITIONAL quality gate conditions into deployment requirements
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Deployment planning converts a validated detection rule into an operational asset — every configuration must be justified, every baseline must be defined, every rollback trigger must be measurable, and the deployment approach must match the operational risk profile. A rule without a deployment plan is validated but valueless; a rule with a bad deployment plan is a liability disguised as a control.
