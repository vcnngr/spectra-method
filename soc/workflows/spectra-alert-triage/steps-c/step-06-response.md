# Step 6: Response Recommendation and Escalation

**Progress: Step 6 of 7** — Next: Documentation and Purple Team Feedback

## STEP GOAL:

Determine the appropriate response tier, generate specific containment actions, identify evidence to preserve, and route to the correct escalation target with full context — converting the classification decision into actionable response. This step is ONLY reached for True Positive and Benign True Positive classifications. False Positive alerts skip directly to step 7.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute containment actions autonomously — recommend and document, operator executes
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC TRIAGE ANALYST conducting structured alert analysis
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Triage Analyst conducting structured alert analysis within an active security engagement
- ✅ This step converts the classification into action — every recommendation must be specific, measurable, and tied to the alert context
- ✅ Evidence preservation BEFORE containment is non-negotiable — containment actions destroy volatile evidence
- ✅ Escalation without sufficient context forces the next tier to re-triage from scratch, wasting critical response time
- ✅ Containment actions on production systems carry business impact — the operator must understand the trade-off before executing

### Step-Specific Rules:

- 🎯 Focus on response tier determination, evidence preservation, containment recommendations, and escalation packaging
- 🚫 FORBIDDEN to reclassify the alert — classification was finalized in step 5
- 🚫 FORBIDDEN to execute containment actions directly — recommend and document only, operator decides and executes
- 💬 Approach: Structured response planning with explicit impact assessment for every recommended action
- 📊 Every containment action must include: target, expected impact, urgency, and business disruption risk

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Containment actions on production systems may cause business disruption — ensure the operator understands the impact before executing; isolating a critical server or disabling a privileged account can have cascading effects beyond the security incident
  - Escalating without sufficient context forces the next tier to re-triage — always include full enrichment and classification rationale so the receiving analyst can act immediately rather than starting over
  - Preserving forensic evidence before containment is critical — containment actions such as host isolation, account disable, or process termination may destroy volatile evidence (memory, active sessions, network connections) that is irreplaceable once lost
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Determine response tier before recommending any specific actions
- ⚠️ Present [A]/[W]/[C] menu after response plan is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `escalation_target` and `containment_actions`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Classification (TP or BTP), confidence level, priority (P1-P4), all enrichment and correlation findings from steps 1-5, asset criticality, user privilege level, kill chain position
- Focus: Response tier, evidence preservation, containment actions, escalation packaging, and notification decisions
- Limits: Do not reclassify, do not execute actions directly, do not begin documentation/closure (step 7)
- Dependencies: Completed classification from step-05-classification.md with classification != "FP"

## CRITICAL PREREQUISITE:

**This step is executed ONLY for TP and BTP classifications.**

If the alert was classified as False Positive in step 5, this step is skipped entirely — the transition to step 7 is managed in the step 5 menu. If you arrived here, the classification is TP or BTP.

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Response Tier Determination

Based on the classification and priority from step 5, determine the appropriate response tier:

| Priority | Response Tier | Target | Action |
|----------|--------------|--------|--------|
| P1 Critical | IRT Activation | Incident Response Team | Full incident declaration, all-hands response, management notification |
| P2 High | L2/L3 Escalation | Senior Analyst + Management | Deep investigation, coordinated containment, stakeholder notification |
| P3 Medium | L2 Escalation | L2 Investigator (Tracker) | Deeper analysis, scoped containment, standard escalation |
| P4 Low | L1 Handles | Current Analyst (Watchdog) | Standard playbook, document and close |

Present the tier determination:

"**Response Tier: {{tier_name}}**

Classification: {{TP / BTP}} ({{confidence}} confidence)
Priority: {{P1 / P2 / P3 / P4}}
Target: {{IRT / L2-L3 / L2 / L1}}
Action: {{action_summary}}
SLA: {{response_time_target}}"

### 2. Evidence Preservation

**CRITICAL: Evidence preservation MUST be planned BEFORE any containment action.**

Containment actions such as host isolation, account disabling, and process termination can destroy volatile evidence that is irreplaceable once lost.

#### A. Volatile Evidence (capture first — lost on reboot, isolation, or process termination):

| Evidence | Collection Method | Priority | Status |
|----------|-------------------|----------|--------|
| Running processes and process tree | `tasklist /v` / `ps auxf` or EDR process snapshot | Critical | Pending |
| Active network connections | `netstat -ano` / `ss -tulpn` or NDR snapshot | Critical | Pending |
| Memory state (RAM dump) | EDR memory capture / WinPmem / LiME | High | Pending |
| Logged-in sessions and active tokens | `query user` / `w` / OAuth session listing | High | Pending |
| DNS cache | `ipconfig /displaydns` / `systemd-resolve --statistics` | Medium | Pending |
| Clipboard contents | If relevant to data exfiltration | Low | Pending |

#### B. Non-Volatile Evidence (stable — capture before containment alters state):

| Evidence | Collection Method | Priority | Status |
|----------|-------------------|----------|--------|
| Log files (SIEM, EDR, OS) | Export from source platform, preserve timestamps | Critical | Pending |
| Disk image or triage package | EDR forensic package / `dd` / FTK Imager | High | Pending |
| Registry hives (Windows) | REG export / EDR registry snapshot | Medium | Pending |
| Email headers and body | Email gateway export, preserve full MIME | Medium (if email-based) | Pending |
| File system artifacts | Prefetch, Amcache, ShimCache, $MFT | Medium | Pending |
| Browser artifacts | History, downloads, cached pages | Low | Pending |

#### C. Chain of Custody

"**Evidence preservation plan:**

For every artifact collected, record:
- Timestamp of collection (UTC)
- Analyst name: {{user_name}}
- Collection method and tool used
- Hash of collected artifact (SHA256)
- Storage location

**Evidence collection priority:**
1. Volatile evidence FIRST — this is lost when containment actions execute
2. Non-volatile evidence SECOND — stable but should be captured before host state changes
3. Begin containment ONLY after critical evidence is preserved or operator accepts the risk"

### 3. Containment Actions

Based on the alert type and kill chain position, recommend specific containment actions. Present recommendations grouped by alert category.

#### Network-Based Containment (suspicious IP, C2 communication, lateral movement):

| # | Action | Target | Impact | Urgency | Business Risk |
|---|--------|--------|--------|---------|---------------|
| 1 | Block source IP at perimeter firewall | {{src_ip}} | Stops inbound malicious traffic | {{P-level}} | Low — external IP only |
| 2 | Add domain to DNS sinkhole | {{domain}} | Prevents DNS resolution of C2 | {{P-level}} | Low — targeted domain |
| 3 | Block URL at web proxy | {{url}} | Prevents access to malicious resource | {{P-level}} | Low — targeted URL |
| 4 | Add IOCs to EDR blocklist | {{ioc_list}} | Blocks known indicators across fleet | {{P-level}} | Low — indicator-specific |
| 5 | Block at network segmentation point | {{segment}} | Prevents lateral spread | {{P-level}} | Medium — may affect legitimate cross-segment traffic |

#### Endpoint-Based Containment (malware, suspicious process, persistence):

| # | Action | Target | Impact | Urgency | Business Risk |
|---|--------|--------|--------|---------|---------------|
| 1 | Isolate host via EDR (network quarantine) | {{hostname}} | Host remains online but network-disconnected | {{P-level}} | High — user loses network access |
| 2 | Kill malicious process | PID {{pid}} — {{process_name}} | Terminates active malicious execution | {{P-level}} | Low — targeted process |
| 3 | Quarantine suspicious file | {{file_path}} | Prevents file execution | {{P-level}} | Low — targeted file |
| 4 | Disable persistence mechanism | {{persistence_type}} at {{location}} | Prevents reactivation on reboot | {{P-level}} | Low — targeted mechanism |

#### Identity-Based Containment (compromised account, credential theft):

| # | Action | Target | Impact | Urgency | Business Risk |
|---|--------|--------|--------|---------|---------------|
| 1 | Disable / lock compromised account | {{username}} | Prevents further unauthorized access | {{P-level}} | High — user loses all access |
| 2 | Revoke active sessions and tokens | {{username}} sessions | Terminates all active authenticated sessions | {{P-level}} | High — user is logged out everywhere |
| 3 | Force password reset | {{username}} | Invalidates potentially stolen credentials | {{P-level}} | Medium — user must re-authenticate |
| 4 | Check and remove mail forwarding rules | {{username}} mailbox | Removes attacker persistence in email | {{P-level}} | Low — targeted mailbox setting |
| 5 | Revoke OAuth app grants | {{username}} OAuth apps | Removes unauthorized API access | {{P-level}} | Medium — may revoke legitimate apps |
| 6 | Review recent account activity | {{username}} audit log | Identifies lateral actions from compromised account | {{P-level}} | None — read-only |

#### Email-Based Containment (phishing, malicious attachment):

| # | Action | Target | Impact | Urgency | Business Risk |
|---|--------|--------|--------|---------|---------------|
| 1 | Search and purge from all mailboxes | Message ID / subject / sender | Removes malicious email before more users interact | {{P-level}} | Low — targeted message |
| 2 | Block sender domain | {{sender_domain}} | Prevents future emails from same source | {{P-level}} | Low — unless legitimate domain spoofed |
| 3 | Check email gateway for clicks/submissions | {{url_in_email}} | Identifies users who interacted with phish | {{P-level}} | None — read-only |
| 4 | If credentials submitted → identity containment | See identity-based actions above | Full identity compromise response | {{P-level}} | See identity section |

**Select applicable categories and present the consolidated action plan:**

"**Containment Action Plan — {{alert_id}}**

| # | Action | Target | Impact | Urgency | Business Risk | Executed? |
|---|--------|--------|--------|---------|---------------|-----------|
| {{for each applicable action from the categories above}} |

**Total actions recommended:** {{count}}
**Highest business risk action:** {{action_description}} — {{risk_description}}

Operator: review the action plan and confirm which actions to execute. Evidence preservation should be completed before containment unless time pressure requires immediate action."

### 4. Escalation Package

If the response tier requires escalation (P1, P2, or P3), prepare a complete escalation package for the receiving team:

"**Escalation Package — {{alert_id}}**

**Executive Summary:**
Alert {{alert_id}} from {{alert_source}} classified as {{classification}} ({{confidence}} confidence) with priority {{priority}}. {{1-2 sentence summary of what happened, what was found, and why it matters.}}

**Classification:**
- Result: {{TP / BTP}}
- Confidence: {{High / Medium / Low}}
- Priority: {{P1 / P2 / P3 / P4}}
- Justification: {{decision_tree_summary}}

**Key Enrichment Findings:**
- IOCs analyzed: {{iocs_enriched}} — Malicious: {{count}}, Suspicious: {{count}}
- Threat profile: {{threat_profile}}
- Campaign association: {{campaign_or_none}}
- Malware family: {{family_or_none}}

**Kill Chain Position:**
- MITRE ATT&CK: {{mitre_techniques}} ({{tactic_names}})
- Kill chain coverage: {{tactics_detected}}
- Campaign assessment: {{isolated / related / campaign}}

**Scope:**
- Affected hosts: {{affected_hosts}}
- Affected users: {{affected_users}}
- Blast radius: {{assessment}}

**Actions Taken:**
- Evidence preserved: {{list_or_pending}}
- Containment actions executed: {{list_or_pending}}

**Recommended Next Steps:**
1. {{investigation_step_1}}
2. {{investigation_step_2}}
3. {{investigation_step_3}}

**Evidence Locations:**
- Triage report: {{outputFile}}
- Preserved artifacts: {{locations}}
- Relevant log queries: {{SIEM_query_references}}"

If the response tier is P4 (L1 handles), skip the escalation package:

"**No escalation required** — P4 alert handled at L1 (current analyst). Actions documented for audit trail."

### 5. Notification Decisions

Determine who needs to be notified based on the response tier and impact:

| Notification Target | When Required | Channel | Information to Include | Information to Withhold |
|---------------------|---------------|---------|----------------------|------------------------|
| SOC Manager | P1, P2, or any BTP | Incident bridge / phone | Classification, priority, scope, actions taken | Detailed IOCs (provide in report) |
| CISO / Security Leadership | P1 only, or P2 with regulated data | Phone / encrypted email | Executive summary, business impact, response status | Technical details |
| Affected Business Unit | When user/host containment affects operations | Email / Teams-Slack | What is affected, expected duration, workaround | Attack details, IOCs |
| Legal / Compliance | When regulated data (PII/PHI/PCI) is involved | Encrypted email | Data type potentially exposed, timeline, containment status | Technical attack details |
| External (CERT/LE) | P1 with confirmed data breach or critical infrastructure | Per regulatory requirement | As required by regulation | Limit to regulatory minimum |
| IT Operations | When containment requires infrastructure changes | Incident bridge / ticket | Specific changes needed, urgency, rollback plan | Full attack narrative |

Present notification plan:

"**Notification Plan:**

| # | Target | Channel | Timing | Status |
|---|--------|---------|--------|--------|
| {{for each required notification}} |

**Note:** Notification content should be appropriate for the audience — technical detail for technical teams, business impact for leadership, regulatory requirements for legal."

### 6. Present MENU OPTIONS

"**Response plan complete.**

Alert: {{alert_id}} — {{classification}} ({{priority}})
Response tier: {{tier}} — Target: {{escalation_target}}
Containment actions: {{count}} recommended
Evidence preservation: {{status}}
Notifications: {{count}} required

**Select an option:**
[A] Advanced Elicitation — Deep analysis of containment trade-offs and response alternatives
[W] War Room — Red (how would the attacker respond to these containment actions?) vs Blue (are we containing fast enough? What are we missing?)
[C] Continue — Proceed to Documentation and Purple Team Feedback (Step 7 of 7)"

#### Menu Handling Logic:

- IF A: Deep analysis — evaluate containment action effectiveness, explore alternative containment strategies, assess whether containment scope is sufficient or excessive, analyze potential attacker response to containment (will they pivot? escalate? go dormant?), review evidence preservation completeness. Process insights, ask user if they want to revise the response plan, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: how would the attacker detect these containment actions? What would they do in the time between detection and containment? Are there backup channels we are not addressing? Would they abandon this operation or escalate? Blue Team perspective: are we containing the right things? Is the scope too narrow (missing attacker persistence) or too broad (disrupting business unnecessarily)? Is our evidence preservation adequate for forensics and potential legal proceedings? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `escalation_target` and `containment_actions` count, then read fully and follow: ./step-07-complete.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and escalation_target and containment_actions updated, and Response and Escalation section populated in output document], will you then read fully and follow: `./step-07-complete.md` to complete the workflow with documentation and Purple Team feedback.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Response tier correctly determined from classification and priority
- Evidence preservation plan created with volatile evidence prioritized before containment
- Chain of custody requirements documented for all evidence artifacts
- Containment actions recommended with specific targets, impact assessment, and business risk
- Applicable containment categories selected based on alert type (network, endpoint, identity, email)
- Escalation package prepared with complete context for receiving team (if escalation required)
- Notification decisions documented with audience-appropriate information boundaries
- Response and Escalation section populated in output document
- Frontmatter updated with escalation_target and containment_actions count
- Operator informed of all recommendations with business impact clearly communicated

### SYSTEM FAILURE:

- Executing containment actions autonomously without operator confirmation
- Recommending containment before planning evidence preservation
- Escalating without sufficient context (forcing the next tier to re-triage)
- Not assessing business impact of containment actions on production systems
- Reclassifying the alert (classification was finalized in step 5)
- Arriving at this step with an FP classification (FP alerts skip to step 7)
- Not documenting which containment actions were executed vs recommended
- Omitting notification decisions for alerts involving regulated data or critical infrastructure
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Response planning converts analysis into action — every recommendation must be specific, impact-assessed, and documented. Evidence preservation before containment is non-negotiable.
