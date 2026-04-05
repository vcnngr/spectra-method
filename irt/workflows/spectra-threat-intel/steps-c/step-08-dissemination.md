# Step 8: Dissemination & Reporting (FINAL STEP)

**Progress: Step 8 of 8** — Final Step

## STEP GOAL:

Produce finished intelligence products tailored to each stakeholder audience (tactical for SOC, operational for IR/Hunt, strategic for CISO/Executives), create the formal dissemination record documenting who receives what, when, and how with TLP compliance verification, calculate intelligence production metrics (PIRs answered, sources consulted, IOCs produced, detection rules created, confidence levels, gaps, time to product), validate report completeness, and update the engagement status. This is the capstone of the intelligence cycle — where finished intelligence reaches the consumers who need it to make decisions and take action.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER disseminate intelligence without TLP compliance verification
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST delivering finished intelligence products, not dumping raw data
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst completing the intelligence cycle by delivering finished products to consumers
- Dissemination is not just sending files — it is matching the RIGHT product to the RIGHT audience in the RIGHT format at the RIGHT time
- A brilliant assessment that reaches the wrong audience, in the wrong format, or too late, has zero operational impact
- The intelligence cycle does not end with dissemination — feedback from consumers drives the next cycle
- Intelligence production metrics provide accountability and continuous improvement data
- Every finished product must answer the consumer's question, not just the analyst's interest

### Step-Specific Rules:

- Focus exclusively on finished product creation, dissemination planning, TLP compliance, intelligence metrics, report validation, and engagement status update
- Approach: Consumer-focused delivery — each product tailored to its audience's needs, classification level, and decision timeline
- Every product must be self-contained — the consumer should not need to read the full report to get their product
- TLP compliance must be verified before any dissemination record is created
- Feedback collection plan must be established — intelligence without feedback does not improve

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Disseminating the full intelligence report to all stakeholders instead of tailored products overwhelms consumers with irrelevant detail — a SOC analyst needs IOCs and detection rules, not the ACH matrix; a CISO needs the risk assessment and recommended actions, not Sigma rule syntax. Untailored dissemination reduces the probability that any consumer will act on the intelligence
  - Not verifying TLP compliance before sharing risks unauthorized disclosure — sharing a TLP:AMBER indicator in a TLP:GREEN product violates the source's trust and may result in loss of intelligence access. TLP compliance must be checked at the indicator level, not just the document level
  - Skipping the feedback collection plan means the intelligence team has no mechanism to assess product quality, relevance, or timeliness — without consumer feedback, the next intelligence cycle will repeat the same mistakes and the intelligence program cannot mature
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Produce each finished product separately, tailored to audience
- Verify TLP compliance before documenting any dissemination record
- Calculate all intelligence production metrics
- Validate report completeness against template
- Update frontmatter: add this step name to the end of the stepsCompleted array
- Update engagement status
- Present final navigation options

## CONTEXT BOUNDARIES:

- Available context: ALL preceding steps — this step synthesizes the entire intelligence production
- Focus: Finished products, dissemination, metrics, validation, closure — no new analysis, no new collection
- Limits: Products are derived from existing analysis — do not introduce new findings at this stage
- Dependencies: IOC packaging (step 7), intelligence assessment (step 6), all preceding steps

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Finished Intelligence Products

Create three audience-tailored products from the intelligence production:

"**Finished Intelligence Products:**

#### Product 1: Tactical Intelligence Product

**Audience:** SOC analysts, detection engineers, security operations
**Purpose:** Immediate detection and response — what to look for and what to do
**Format:** IOC feed + detection rules + quick reference

**Tactical Product Contents:**

| Component | Content | Format |
|-----------|---------|--------|
| **Executive IOC Summary** | Top-priority active IOCs with context | Table |
| **Active IOC Feed** | All active IOCs in machine-readable format | CSV / JSON |
| **Detection Rules** | Sigma, YARA, Suricata rules from step 7 | Rule files |
| **SIEM Queries** | KQL and SPL queries from step 7 | Query text |
| **STIX Bundle** | Machine-readable intelligence package | JSON |
| **ATT&CK Techniques** | Techniques to detect with procedure details | Table |
| **Quick Reference Card** | One-page summary: actor, IOCs, rules, actions | Markdown |

**Quick Reference Card:**

```
THREAT INTELLIGENCE QUICK REFERENCE — {{intel_id}}
Date: {{date}} | TLP: {{tactical_product_TLP}} | Confidence: {{overall_confidence}}

THREAT ACTOR: {{actor_name}} ({{category}})
MOTIVATION: {{motivation}} | CAPABILITY: {{capability_level}}
CAMPAIGN: {{campaign_name or 'Isolated operation'}}

PRIORITY IOCs (deploy immediately):
{{top 10-15 active, high-confidence IOCs with type and context}}

ATT&CK TECHNIQUES (detection priorities):
{{top techniques with T-codes and detection guidance}}

IMMEDIATE ACTIONS:
1. {{action 1 — e.g., deploy Sigma rules to SIEM}}
2. {{action 2 — e.g., sweep endpoints for IOC hashes}}
3. {{action 3 — e.g., block C2 domains at proxy/DNS}}
4. {{action 4 — e.g., hunt for lateral movement patterns}}

DETECTION RULES AVAILABLE: {{sigma_count}} Sigma | {{yara_count}} YARA | {{suricata_count}} Suricata | {{siem_count}} SIEM queries
```

#### Product 2: Operational Intelligence Product

**Audience:** IR managers, threat hunt teams, security architects
**Purpose:** Operational decision-making — understand the adversary to plan response
**Format:** Actor profile + campaign assessment + TTP report

**Operational Product Contents:**

| Component | Content | Format |
|-----------|---------|--------|
| **Threat Actor Profile** | Full actor profile from step 3 | Narrative + tables |
| **Campaign Assessment** | Campaign analysis from step 5 | Narrative + timeline |
| **TTP Deep Dive** | ATT&CK mapping with procedures from step 5 | Tables + Navigator layer |
| **Diamond Model Summary** | Key relationships and pivots from step 4 | Diagrams + tables |
| **Kill Chain Reconstruction** | Full Kill Chain from step 5 | Timeline + tables |
| **Predictive Assessment** | Likely next actions from step 6 | Scenarios + indicators |
| **Detection Gap Analysis** | What was missed from step 5 | Tables |
| **Hunt Hypotheses** | Hypotheses for threat hunting based on gaps | Structured list |

**Hunt Hypotheses (for Hawk / threat hunt teams):**

| # | Hypothesis | Based On | ATT&CK | Data Sources | Expected Evidence |
|---|-----------|----------|--------|--------------|-------------------|
| 1 | {{hypothesis — e.g., 'The actor used T1053.005 for persistence on additional systems beyond those already identified'}} | {{step 5 gap analysis — technique expected but not observed}} | {{T-code}} | {{where to hunt}} | {{what finding would confirm}} |
| 2 | {{hypothesis}} | {{basis}} | {{T-code}} | {{sources}} | {{evidence}} |

#### Product 3: Strategic Intelligence Product

**Audience:** CISO, executive leadership, board risk committee, legal/compliance
**Purpose:** Strategic decisions — what does this mean for our risk and what do we need to invest in
**Format:** Executive assessment + risk implications + recommended investments

**Strategic Product Contents:**

| Component | Content | Format |
|-----------|---------|--------|
| **Executive Summary** | 1-page threat assessment in plain language | Narrative |
| **Risk Implications** | Impact on organizational risk posture | Table + narrative |
| **Threat Landscape Context** | Where this threat fits in the broader landscape | Narrative |
| **Recommended Actions** | Strategic investments and program changes | Prioritized list |
| **Metrics** | Intelligence production metrics | Table |
| **Confidence Statement** | Overall confidence with plain-language explanation | Narrative |

**Executive Summary (plain language, no jargon):**

```
EXECUTIVE THREAT INTELLIGENCE BRIEF — {{intel_id}}
Date: {{date}} | Classification: {{tlp for executives}}

SITUATION:
{{2-3 sentences describing what happened and why it matters, in business terms}}

THREAT ACTOR:
{{1-2 sentences on who is behind this — name, motivation, capability in plain language}}
Attribution confidence: {{level}} — {{plain language explanation}}

RISK TO ORGANIZATION:
{{2-3 sentences on what this means for the organization's security posture}}

KEY FINDINGS:
1. {{finding in business terms}}
2. {{finding in business terms}}
3. {{finding in business terms}}

RECOMMENDED ACTIONS:
1. {{action — business language, not technical}} — Priority: {{level}} — Timeline: {{when}}
2. {{action}} — Priority: {{level}} — Timeline: {{when}}
3. {{action}} — Priority: {{level}} — Timeline: {{when}}

WHAT HAPPENS IF WE DO NOTHING:
{{consequence assessment in business terms}}

CONFIDENCE: {{overall confidence}} — {{plain language: what this means for decision-making}}
```"

### 2. Dissemination Record

"**Dissemination Record:**

Document exactly who receives what, when, and how:

#### Distribution Log:

| # | Recipient | Role | Product(s) | TLP | Format | Delivery Method | Date | Acknowledged |
|---|----------|------|-----------|-----|--------|-----------------|------|-------------|
| 1 | {{name/team}} | {{role}} | {{product type}} | {{TLP}} | {{PDF/email/STIX/API}} | {{secure email/portal/API/in-person}} | {{date}} | {{yes/no/pending}} |
| 2 | {{name/team}} | {{role}} | {{product}} | {{TLP}} | {{format}} | {{method}} | {{date}} | {{status}} |

#### Dissemination Matrix (Product-to-Consumer):

| Consumer | Tactical | Operational | Strategic | IOC Feed | STIX Bundle | Detection Rules |
|----------|----------|-------------|-----------|----------|-------------|----------------|
| SOC (Commander) | Yes | Summary | No | Yes | Yes | Yes |
| Hunt Team (Hawk) | Yes | Yes | No | Yes | Yes | Yes |
| Detection Eng (Sentinel) | Rules only | TTP section | No | Yes | Yes | Yes |
| IR Team (Dispatch) | Yes | Yes | Summary | Yes | Yes | Yes |
| Forensics (Trace) | IOC list | Full | No | Yes | Yes | No |
| Malware Analysis (Scalpel) | Samples | Full | No | Yes | Yes | YARA only |
| CISO | Summary | Summary | Full | No | No | No |
| Legal/Compliance | No | No | Risk section | No | No | No |
| ISAC | IOC list | Summary | No | TLP-compliant | TLP-compliant | TLP-compliant |

#### TLP Compliance Verification:

| Product | TLP | Contains RED Indicators? | Contains AMBER+STRICT? | Verification |
|---------|-----|------------------------|----------------------|-------------|
| {{product}} | {{TLP}} | {{yes/no}} | {{yes/no}} | {{PASS — no TLP violations / FAIL — {{issue}}}} |

**TLP Compliance Status:** {{ALL PASS / FAILURES IDENTIFIED — {{details}}}

If any TLP violations detected: resolve before recording dissemination.

#### Feedback Collection Plan:

| Consumer | Feedback Type | Collection Method | Timeline | Responsible |
|----------|--------------|-------------------|----------|-------------|
| SOC | Did IOCs generate true positives? Detection rule quality? | Post-deployment report | 7 days | SOC Manager |
| Hunt Team | Did hunt hypotheses yield findings? | Hunt debrief | 14 days | Hunt Lead |
| IR Team | Was operational intel useful for response decisions? | Post-incident review | Case closure | IR Lead |
| CISO | Was strategic product actionable for decisions? | 1:1 feedback | 30 days | Analyst |
| ISAC | Did shared indicators match partner observations? | ISAC feedback loop | 30 days | ISAC coordinator |"

### 3. Intelligence Metrics

"**Intelligence Production Metrics:**

| Metric | Value |
|--------|-------|
| **Intelligence ID** | {{intel_id}} |
| **Intelligence Type** | {{tactical/operational/strategic}} |
| **Trigger Type** | {{incident/IOC/advisory/RFI/proactive/environmental}} |
| **PIRs Defined** | {{count}} |
| **PIRs Answered** | {{count}} ({{percentage}}%) |
| **PIRs Unanswered** | {{count}} — {{reasons}} |
| **SIRs Addressed** | {{count}} |
| **Sources Consulted** | {{count}} across {{category_count}} categories |
| **Raw Data Items Collected** | {{count}} |
| **Processed Items** | {{count}} |
| **IOCs Produced** | {{total}} ({{active}} active, {{historical}} historical, {{expired}} expired) |
| **IOC Corroboration Rate** | {{percentage}}% corroborated by 2+ sources |
| **Threat Actors Identified** | {{count}} |
| **Attribution Confidence** | {{level}} |
| **Diamond Events** | {{count}} |
| **Activity Threads** | {{count}} |
| **Pivot Findings** | {{count}} |
| **ATT&CK Techniques Mapped** | {{count}} |
| **Detection Rules Created** | Sigma: {{n}}, YARA: {{n}}, Suricata: {{n}}, SIEM: {{n}} |
| **STIX Objects** | {{count}} |
| **ACH Hypotheses Evaluated** | {{count}} |
| **Key Assumptions Identified** | {{count}} ({{linchpin}} linchpin) |
| **Predictive Scenarios** | {{count}} |
| **Confidence Levels Achieved** | {{overall}} (H:{{n}} M:{{n}} L:{{n}} per assessment) |
| **Collection Gaps** | {{count}} |
| **Intelligence Gaps** | {{count}} |
| **TLP Distribution** | RED:{{n}} AMBER+STRICT:{{n}} AMBER:{{n}} GREEN:{{n}} CLEAR:{{n}} |
| **Products Delivered** | Tactical:{{n}} Operational:{{n}} Strategic:{{n}} |
| **Dissemination Targets** | {{count}} |
| **Time: Requirement to Product** | {{duration}} |

**Quality Assessment:**

| Quality Dimension | Assessment | Notes |
|-------------------|-----------|-------|
| **Timeliness** | {{met deadline / delayed by {{time}}}} | {{context}} |
| **Relevance** | {{directly answers PIRs / partially relevant / tangential}} | {{which PIRs answered}} |
| **Accuracy** | {{to be validated by consumer feedback}} | {{confidence distribution}} |
| **Completeness** | {{all PIRs addressed / gaps remain}} | {{unanswered PIRs}} |
| **Clarity** | {{products tailored to audiences}} | {{format appropriateness}} |
| **Actionability** | {{specific actions recommended / general guidance only}} | {{action count}} |"

### 4. Report Completeness Validation

"**Report Completeness Validation:**

Verify that all sections of the intelligence report are populated:

| Section | Status | Notes |
|---------|--------|-------|
| Frontmatter | {{Complete / Incomplete — {{missing fields}}}} | All fields populated |
| Intelligence Requirement | {{Complete / Incomplete}} | Trigger, PIRs, SIRs, collection plan |
| Collection & Processing | {{Complete / Incomplete}} | Source-by-source, IOC inventory, gaps |
| Threat Actor Profile | {{Complete / Incomplete}} | ID, profile, campaigns, TTPs, attribution |
| Diamond Model Analysis | {{Complete / Incomplete}} | Events, meta-features, threads, pivots |
| Kill Chain & ATT&CK Mapping | {{Complete / Incomplete}} | LM/UKC, deep mapping, Navigator, campaign |
| Intelligence Assessment | {{Complete / Incomplete}} | ACH, assumptions, I&W, red hat, predictions |
| IOC & Indicator Summary | {{Complete / Incomplete}} | Consolidation, lifecycle, STIX, detection |
| Finished Intelligence Products | {{Complete / Incomplete}} | Tactical, operational, strategic |
| Dissemination Record | {{Complete / Incomplete}} | Distribution, TLP compliance, feedback plan |
| Intelligence Metrics | {{Complete / Incomplete}} | All metrics populated |
| Appendices | {{Complete / Incomplete}} | IOC feed, STIX JSON, Navigator layer, detection rules |

**Validation Result:** {{ALL COMPLETE / INCOMPLETE — {{sections needing attention}}}}

**Engagement Status Update:**
- Update frontmatter: `Status: Complete`
- Record completion timestamp
- Note any follow-up intelligence cycles recommended"

### 5. Present Final Summary and Navigation

"**Intelligence Production Complete**

{{user_name}}, the threat intelligence production workflow for {{intel_id}} is complete.

**Final Product Summary:**

| Dimension | Result |
|-----------|--------|
| **Intelligence ID** | {{intel_id}} |
| **Actor** | {{actor_name}} — {{category}} ({{attribution_confidence}} confidence) |
| **Campaign** | {{campaign or 'Isolated operation'}} |
| **PIRs** | {{answered}}/{{total}} answered |
| **IOCs** | {{total}} produced ({{active}} active) |
| **Detection** | {{total_rules}} rules across Sigma/YARA/Suricata/SIEM |
| **STIX** | {{stix_objects}} objects in STIX 2.1 bundle |
| **Assessment** | {{overall_confidence}} confidence |
| **Products** | {{tactical_count}} tactical, {{operational_count}} operational, {{strategic_count}} strategic |
| **Dissemination** | {{dissemination_count}} products to {{target_count}} targets |
| **Time** | {{requirement_to_product_duration}} |

**Intelligence Gaps (for next cycle):**
{{numbered list of remaining intelligence gaps and what would fill them}}

**Recommended Follow-Up:**
{{specific recommendations for the next intelligence cycle — additional collection, monitoring, re-assessment timeline}}

**Report saved to:** `{outputFile}`

---

**Select next action:**
[W] War Room — Final adversarial review of the complete intelligence product
[N] New Intel — Begin a new intelligence production within this engagement
[S] SOC to Commander — Hand off tactical product to SOC workflow (spectra-alert-triage)
[D] Detection to Sentinel — Hand off detection rules to detection lifecycle (spectra-detection-lifecycle)
[H] Hunt to Hawk — Hand off hunt hypotheses to threat hunt workflow (spectra-threat-hunt)
[I] IR to Dispatch — Hand off operational product to incident handling (spectra-incident-handling)
[F] Forensics to Trace — Hand off IOCs/indicators to digital forensics (spectra-digital-forensics)
[M] Malware to Scalpel — Hand off samples/indicators to malware analysis (spectra-malware-analysis)"

#### Menu Handling Logic:

- IF W: War Room — Final adversarial review of the complete product. Red Team: does this intelligence product accurately describe what I did, or does it miss critical aspects? Would this product stop me from succeeding again? What would I change based on reading this? Blue Team: is this product actionable enough? Can the SOC deploy these rules tomorrow? Can the CISO make a budget decision from the strategic product? Summarize and redisplay menu
- IF N: "Starting a new intelligence production within the same engagement. This will create a new intel ID and a fresh intelligence report. Read fully and follow: ./step-01-init.md"
- IF S: "Tactical product ready for SOC Commander. The operator should invoke `spectra-alert-triage` or `spectra-detection-lifecycle` for the SOC module. Key handoff data: IOC feed, detection rules, ATT&CK techniques."
- IF D: "Detection content ready for Sentinel. The operator should invoke `spectra-detection-lifecycle` with the detection rules and ATT&CK mapping from this intelligence product."
- IF H: "Hunt hypotheses ready for Hawk. The operator should invoke `spectra-threat-hunt` with the hunt hypotheses generated from the detection gap analysis."
- IF I: "Operational product ready for Dispatch. The operator should invoke `spectra-incident-handling` if this intelligence relates to an active or potential incident."
- IF F: "IOC and indicator data ready for Trace. The operator should invoke `spectra-digital-forensics` if forensic investigation is needed."
- IF M: "Malware samples and indicators ready for Scalpel. The operator should invoke `spectra-malware-analysis` for deep malware reverse engineering."

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting the final navigation
- Cross-module handoffs provide the relevant data subset, not the full report
- New intel production starts fresh with step-01-init.md

## CRITICAL STEP COMPLETION NOTE

This is the FINAL STEP. The intelligence production workflow is complete when:
- All three finished products (tactical, operational, strategic) are created
- Dissemination record is documented with TLP compliance verified
- Intelligence metrics are calculated and recorded
- Report completeness validation passes
- Engagement status is updated
- Frontmatter is fully updated with all final fields including this step in stepsCompleted
- Final navigation options are presented to the operator

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Three finished intelligence products created: tactical (SOC), operational (IR/Hunt), strategic (CISO/Exec)
- Each product tailored to its audience's needs, classification level, and format requirements
- Quick reference card created for tactical product with priority IOCs and immediate actions
- Executive summary created for strategic product in plain business language
- Hunt hypotheses generated for operational product based on detection gap analysis
- Dissemination record created with who/what/when/how for every distribution
- Dissemination matrix shows which consumers receive which products
- TLP compliance verified for every product before dissemination record creation
- Feedback collection plan established with specific metrics, methods, and timelines per consumer
- Intelligence production metrics calculated comprehensively
- Quality assessment performed across timeliness, relevance, accuracy, completeness, clarity, actionability
- Report completeness validated against template — all sections populated
- Engagement status updated
- Intelligence gaps documented for next cycle
- Follow-up recommendations provided
- Final navigation options presented with cross-module handoff guidance
- Frontmatter fully updated with all final fields

### SYSTEM FAILURE:

- Not creating all three product types (tactical, operational, strategic)
- Not tailoring products to audience — sending the full report to everyone
- Not creating the quick reference card — SOC analysts need the one-page summary
- Not creating the executive summary in business language — executives cannot consume technical intelligence
- Not verifying TLP compliance before documenting dissemination — unauthorized disclosure risk
- Not establishing a feedback collection plan — intelligence without feedback cannot improve
- Not calculating intelligence metrics — accountability and improvement require measurement
- Not validating report completeness — incomplete reports undermine consumer trust
- Not documenting intelligence gaps — gaps inform the next intelligence cycle
- Not updating engagement status — future workflows need accurate state
- Not presenting cross-module navigation options — intelligence must flow to consumers
- Introducing new analysis findings at this stage — this step packages and delivers, it does not analyze

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Dissemination is where intelligence creates value. A brilliant analysis that never reaches the right consumer has zero impact. Every product must be tailored, every dissemination must be TLP-compliant, every metric must be recorded, and every gap must inform the next cycle. Intelligence is a cycle, not a line — this ending is the beginning of the next requirement.
