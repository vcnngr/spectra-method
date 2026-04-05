# Step 7: IOC Packaging & Detection Content

**Progress: Step 7 of 8** — Next: Dissemination & Reporting

## STEP GOAL:

Consolidate all indicators of compromise from collection, analysis, and pivot findings into a comprehensive IOC inventory with lifecycle assessment, package them into a STIX 2.1 bundle with properly structured objects and relationships, create actionable detection content (Sigma rules, YARA rules, Suricata/Snort rules, KQL/SPL queries) each mapped to ATT&CK with confidence and false positive assessments, and apply TLP classification with handling instructions per indicator. This step transforms intelligence assessments into operationally deployable detection and response content.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER create detection rules without specifying confidence and false positive risk
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST producing detection-grade intelligence, not generic rule templates
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst packaging intelligence into operationally deployable formats
- IOCs without context are just strings — every indicator must carry its story (source, confidence, lifecycle status, TLP, ATT&CK mapping)
- STIX 2.1 is the interoperability standard — properly structured STIX enables machine-readable intelligence sharing
- Detection rules must be tuned for the consumer's environment — generic rules produce false positives that erode analyst trust
- TLP classification is not optional — it determines who can receive each indicator and how it can be shared
- Every detection rule must specify what it detects, what it misses, and what false positives to expect

### Step-Specific Rules:

- Focus exclusively on IOC consolidation, STIX packaging, detection content creation, and TLP classification
- FORBIDDEN to begin dissemination (step 8) — that step handles who receives what and how
- FORBIDDEN to create detection rules without ATT&CK technique mapping and false positive assessment
- Approach: Production-quality detection content that a SOC analyst can deploy with confidence
- Every IOC must be assessed for lifecycle status (active/historical/expired)
- Every detection rule must be tested conceptually against known-good patterns to assess FP risk

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Deploying IOCs without lifecycle assessment risks blocking legitimate infrastructure — IP addresses get reassigned, domains expire and are re-registered, and threat actors abandon infrastructure. An IOC that was malicious 6 months ago may now point to a legitimate CDN or a parked domain. Blocking it creates a false positive that disrupts business operations
  - Creating detection rules without false positive assessment produces rules that SOC analysts will disable within days — a rule that fires 500 times a day on legitimate activity is not detection, it is noise. Every rule must include expected FP rate and tuning guidance so the SOC can deploy with confidence
  - Not applying TLP classification per indicator risks unauthorized disclosure — some indicators may come from sensitive sources (government partners, ISACs, classified feeds) that restrict sharing. Sharing a TLP:RED indicator publicly is a trust violation that can cut off future intelligence sharing from that source
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Consolidate IOCs from ALL steps (collection, actor profiling, Diamond Model pivots, Kill Chain mapping)
- Assess each IOC for lifecycle status before packaging
- Create STIX objects with proper relationships
- Write detection rules with full metadata
- Apply TLP per indicator, not just per document
- Update frontmatter: add this step name to the end of the stepsCompleted array
- FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Intelligence assessment (step 6), Kill Chain and ATT&CK mapping (step 5), Diamond Model (step 4), actor profile (step 3), processed intelligence and IOC inventory (step 2), PIRs (step 1)
- Focus: IOC consolidation, lifecycle assessment, STIX 2.1 packaging, detection content creation, TLP classification — no dissemination, no stakeholder communication
- Limits: Detection rules are intelligence-informed, not environment-tuned. Environment-specific tuning is the responsibility of the detection engineering team (Sentinel) after receiving the rules
- Dependencies: All preceding steps — IOC packaging synthesizes the entire intelligence production

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. IOC Consolidation

Compile all IOCs from every step into a single comprehensive inventory:

"**IOC Consolidation:**

Merge IOCs from:
- Step 2 (Collection & Processing): original extracted IOCs
- Step 3 (Actor Profiling): IOCs from historical campaign research
- Step 4 (Diamond Model): new IOCs from pivot analysis
- Step 5 (Kill Chain): IOCs mapped to specific Kill Chain phases

**Comprehensive IOC Inventory:**

| # | IOC Type | Value | Context | First Seen | Last Seen | Confidence | Source Count | Source (Best) | ATT&CK Technique | Kill Chain Phase | TLP | Lifecycle | Notes |
|---|----------|-------|---------|------------|-----------|------------|--------------|---------------|-------------------|-----------------|-----|-----------|-------|
| 1 | {{type}} | {{value}} | {{what this IOC represents}} | {{date}} | {{date}} | {{H/M/L}} | {{count}} | {{best source}} | {{T-code}} | {{phase}} | {{TLP}} | {{active/historical/expired}} | {{context}} |
| 2 | {{type}} | {{value}} | {{context}} | {{date}} | {{date}} | {{level}} | {{count}} | {{source}} | {{T-code}} | {{phase}} | {{TLP}} | {{status}} | {{notes}} |

**IOC Statistics:**

| IOC Type | Total | Active | Historical | Expired | High Conf | Moderate Conf | Low Conf |
|----------|-------|--------|------------|---------|-----------|---------------|----------|
| IP Addresses | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Domains | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| URLs | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| File Hashes (SHA-256) | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| File Hashes (SHA-1) | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| File Hashes (MD5) | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Email Addresses | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| Other | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} | {{n}} |
| **TOTAL** | **{{n}}** | **{{n}}** | **{{n}}** | **{{n}}** | **{{n}}** | **{{n}}** | **{{n}}** |"

### 2. IOC Lifecycle Assessment

For each IOC, assess whether it is still operationally relevant:

"**IOC Lifecycle Assessment:**

IOC lifecycle status determines operational utility:

| Status | Meaning | Operational Use |
|--------|---------|-----------------|
| **Active** | IOC is currently in use by the threat actor | Block, detect, alert — highest priority for deployment |
| **Historical** | IOC was used but is no longer active (infrastructure rotated, campaign ended) | Retrospective hunt, historical correlation, trend analysis — do NOT block |
| **Expired** | IOC has been reassigned, re-registered, or is no longer attributable to the threat | Remove from blocklists, retain for historical reference only |

**Lifecycle Assessment Criteria:**

| Factor | Active Indicators | Historical Indicators | Expired Indicators |
|--------|-------------------|----------------------|-------------------|
| Last observed | Within 30 days | 30-180 days ago | >180 days ago or reassigned |
| Infrastructure status | Resolving, responsive | Down, parked, or sinkholed | Re-registered, new owner |
| Threat actor behavior | Actor still using | Actor has rotated | Actor has abandoned |
| TI feed status | Still flagged malicious | Mixed signals | Clean / not flagged |

**Lifecycle Assessment Results:**

| IOC | Current Status | Assessment Basis | Recommended Action |
|-----|---------------|-----------------|-------------------|
| {{value}} | {{Active}} | {{last seen {{date}}, still resolving, still flagged by {{sources}}}} | Deploy to detection and blocking |
| {{value}} | {{Historical}} | {{last seen {{date}}, infrastructure sinkholed}} | Hunt retroactively, do not block |
| {{value}} | {{Expired}} | {{domain re-registered by {{entity}}, no longer attributable}} | Remove from any existing blocklists |

**Lifecycle Summary:**
- IOCs recommended for active deployment: {{count}}
- IOCs recommended for historical hunting only: {{count}}
- IOCs recommended for removal from blocklists: {{count}} (if previously deployed)"

### 3. STIX 2.1 Bundle

Package intelligence into STIX 2.1 format for machine-readable sharing:

"**STIX 2.1 Bundle:**

Generate the following STIX Domain Objects (SDOs) and Relationship Objects (SROs):

#### STIX Objects Inventory:

| Object Type | Count | Description |
|-------------|-------|-------------|
| `threat-actor` | {{n}} | Threat actor profile(s) from step 3 |
| `campaign` | {{n}} | Campaign(s) identified in step 5 |
| `indicator` | {{n}} | IOCs with STIX patterns |
| `malware` | {{n}} | Malware families identified |
| `tool` | {{n}} | Legitimate tools used maliciously |
| `attack-pattern` | {{n}} | ATT&CK techniques mapped in step 5 |
| `vulnerability` | {{n}} | CVEs exploited (if applicable) |
| `infrastructure` | {{n}} | Adversary infrastructure from Diamond Model |
| `identity` | {{n}} | Victim organization(s) |
| `report` | 1 | This intelligence report as a STIX report |
| `relationship` | {{n}} | Links between all objects |
| `sighting` | {{n}} | Where indicators were observed |
| **TOTAL** | **{{n}}** | |

#### STIX Bundle Structure:

```json
{
  \"type\": \"bundle\",
  \"id\": \"bundle--{{uuid}}\",
  \"objects\": [
    {
      \"type\": \"threat-actor\",
      \"id\": \"threat-actor--{{uuid}}\",
      \"spec_version\": \"2.1\",
      \"created\": \"{{timestamp}}\",
      \"modified\": \"{{timestamp}}\",
      \"name\": \"{{actor_name}}\",
      \"description\": \"{{actor_description}}\",
      \"threat_actor_types\": [\"{{nation-state / crime-syndicate / criminal / hacktivist / insider-threat / unknown}}\"],
      \"aliases\": [\"{{alias1}}\", \"{{alias2}}\"],
      \"roles\": [\"{{agent / director / independent / infrastructure-operator / malware-author / sponsor}}\"],
      \"goals\": [\"{{goal1}}\", \"{{goal2}}\"],
      \"sophistication\": \"{{none / minimal / intermediate / advanced / expert / innovator / strategic}}\",
      \"resource_level\": \"{{individual / club / contest / team / organization / government}}\",
      \"primary_motivation\": \"{{accidental / coercion / dominance / ideology / notoriety / organizational-gain / personal-gain / personal-satisfaction / revenge / unpredictable}}\",
      \"confidence\": {{0-100}}
    },
    {
      \"type\": \"indicator\",
      \"id\": \"indicator--{{uuid}}\",
      \"spec_version\": \"2.1\",
      \"created\": \"{{timestamp}}\",
      \"modified\": \"{{timestamp}}\",
      \"name\": \"{{indicator_name}}\",
      \"description\": \"{{context — what this indicator represents}}\",
      \"indicator_types\": [\"{{anomalous-activity / anonymization / benign / compromised / malicious-activity / attribution}}\"],
      \"pattern\": \"{{STIX pattern — e.g., [ipv4-addr:value = '203.0.113.1']}}\",
      \"pattern_type\": \"stix\",
      \"pattern_version\": \"2.1\",
      \"valid_from\": \"{{first_seen_timestamp}}\",
      \"valid_until\": \"{{expiry_timestamp_if_applicable}}\",
      \"kill_chain_phases\": [{\"kill_chain_name\": \"mitre-attack\", \"phase_name\": \"{{tactic}}\"}],
      \"confidence\": {{0-100}}
    },
    {
      \"type\": \"relationship\",
      \"id\": \"relationship--{{uuid}}\",
      \"spec_version\": \"2.1\",
      \"relationship_type\": \"{{indicates / uses / targets / attributed-to / related-to}}\",
      \"source_ref\": \"{{source_object_id}}\",
      \"target_ref\": \"{{target_object_id}}\",
      \"confidence\": {{0-100}}
    }
  ]
}
```

**STIX Relationship Map:**
- `threat-actor` --uses--> `malware`, `tool`, `attack-pattern`
- `threat-actor` --attributed-to--> `campaign`
- `campaign` --uses--> `malware`, `tool`, `attack-pattern`, `infrastructure`
- `campaign` --targets--> `identity`, `vulnerability`
- `indicator` --indicates--> `malware`, `threat-actor`, `campaign`
- `malware` --uses--> `attack-pattern`
- `sighting` --observed--> `indicator` (at `identity`)

**Note:** The full STIX bundle JSON will be placed in Appendix B of the report."

### 4. Detection Content

Create detection rules from the intelligence:

"**Detection Content:**

#### 4a. Sigma Rules

For each detection-worthy pattern, create a Sigma rule:

```yaml
title: {{Descriptive title — actor name + behavior}}
id: {{uuid}}
status: experimental
description: >
  Detects {{specific behavior}} associated with {{actor_name}} ({{intel_id}}).
  {{procedure detail from ATT&CK mapping.}}
references:
  - {{intelligence report reference}}
  - {{MITRE ATT&CK URL}}
author: Oracle (SPECTRA Threat Intelligence) — {{intel_id}}
date: {{date}}
modified: {{date}}
tags:
  - attack.{{tactic}}
  - attack.{{T-code}}
  - {{actor_tag}}
logsource:
  category: {{process_creation / network_connection / file_event / registry_event / dns_query / etc.}}
  product: {{windows / linux / etc.}}
detection:
  selection:
    {{field}}: {{value or pattern}}
  condition: selection
falsepositives:
  - {{known FP scenario 1}}
  - {{known FP scenario 2}}
level: {{critical / high / medium / low / informational}}
```

**Sigma Rules Created:**

| # | Rule Title | ATT&CK | Log Source | Level | FP Risk | Confidence |
|---|-----------|--------|-----------|-------|---------|------------|
| 1 | {{title}} | {{T-code}} | {{source}} | {{level}} | {{low/medium/high}} | {{H/M/L}} |
| 2 | {{title}} | {{T-code}} | {{source}} | {{level}} | {{FP risk}} | {{confidence}} |

#### 4b. YARA Rules

For each malware sample or file-based indicator:

```yara
rule {{RuleName}} : {{tags}} {
    meta:
        description = \"{{Detects malware/tool associated with actor_name (intel_id)}}\"
        author = \"Oracle (SPECTRA Threat Intelligence)\"
        reference = \"{{intel_id}}\"
        date = \"{{date}}\"
        hash = \"{{sample_hash}}\"
        tlp = \"{{TLP level}}\"
        mitre_attack = \"{{T-code}}\"
        confidence = \"{{high/moderate/low}}\"
        
    strings:
        $s1 = {{string or hex pattern}} {{nocase/wide/ascii}}
        $s2 = {{string or hex pattern}}
        $h1 = { {{hex pattern with wildcards}} }
        
    condition:
        {{condition — e.g., uint16(0) == 0x5A4D and filesize < 1MB and (2 of ($s*) or $h1)}}
}
```

**YARA Rules Created:**

| # | Rule Name | Target | Strings | Confidence | FP Risk |
|---|----------|--------|---------|------------|---------|
| 1 | {{name}} | {{what it detects}} | {{count}} | {{H/M/L}} | {{low/medium/high}} |

#### 4c. Suricata / Snort Rules

For each network-based indicator:

```
alert {{protocol}} {{src}} {{src_port}} -> {{dst}} {{dst_port}} (
    msg:\"SPECTRA {{intel_id}} — {{description}}\";
    {{content / dns.query / tls.sni / http.uri / etc.}};
    reference:url,{{reference}};
    classtype:{{trojan-activity / attempted-admin / etc.}};
    sid:{{unique_id}};
    rev:1;
    metadata: mitre_technique_id {{T-code}}, confidence {{level}}, tlp {{TLP}}, created_at {{date}};
)
```

**Suricata Rules Created:**

| # | SID | Description | Protocol | Direction | Confidence | FP Risk |
|---|-----|-------------|----------|-----------|------------|---------|
| 1 | {{sid}} | {{description}} | {{TCP/UDP/HTTP/DNS/TLS}} | {{direction}} | {{H/M/L}} | {{risk}} |

#### 4d. SIEM Queries (KQL / SPL)

For each detection pattern, provide SIEM-ready queries:

**KQL (Microsoft Sentinel / Defender):**

```kql
// {{Description}} — {{intel_id}} — {{T-code}}
// Confidence: {{level}} | FP Risk: {{risk}}
{{KQL query}}
```

**SPL (Splunk):**

```spl
// {{Description}} — {{intel_id}} — {{T-code}}
// Confidence: {{level}} | FP Risk: {{risk}}
{{SPL query}}
```

**SIEM Queries Created:**

| # | Description | ATT&CK | Language | Confidence | FP Risk |
|---|-------------|--------|----------|------------|---------|
| 1 | {{description}} | {{T-code}} | KQL | {{H/M/L}} | {{risk}} |
| 2 | {{description}} | {{T-code}} | SPL | {{H/M/L}} | {{risk}} |"

### 5. TLP Classification & Handling

"**TLP Classification:**

Apply Traffic Light Protocol (TLP) classification per indicator and per product:

**TLP Definitions (TLP 2.0):**

| TLP Level | Sharing | Use Case |
|-----------|---------|----------|
| **TLP:RED** | Named recipients only, no further sharing | Sensitive source intelligence, classified feeds, named individuals only |
| **TLP:AMBER+STRICT** | Organization only, no sharing beyond | Internal detection and response, not for partners or ISACs |
| **TLP:AMBER** | Organization and clients/partners on need-to-know | Shared with trusted partners, ISACs, sector peers |
| **TLP:GREEN** | Community sharing permitted | Broad sharing within security community, ISACs, peer organizations |
| **TLP:CLEAR** | Unlimited, public disclosure permitted | Public IOC feeds, blog posts, advisories |

**Per-Indicator TLP Assignment:**

| IOC | TLP | Rationale | Handling Instructions |
|-----|-----|-----------|---------------------|
| {{value}} | {{TLP:level}} | {{why this TLP — source restrictions, sensitivity, operational impact}} | {{specific handling — e.g., 'Do not share externally', 'OK for ISAC sharing', 'May be published'}} |

**Per-Product TLP Assignment:**

| Product | TLP | Rationale |
|---------|-----|-----------|
| Full intelligence report | {{TLP}} | {{rationale}} |
| IOC feed (active indicators) | {{TLP}} | {{rationale}} |
| STIX bundle | {{TLP}} | {{rationale}} |
| Detection rules (Sigma/YARA/Suricata) | {{TLP}} | {{rationale}} |
| SIEM queries | {{TLP}} | {{rationale}} |
| Executive summary | {{TLP}} | {{rationale}} |

**TLP Distribution Summary:**

| TLP Level | Indicators | Products |
|-----------|-----------|----------|
| TLP:RED | {{count}} | {{count}} |
| TLP:AMBER+STRICT | {{count}} | {{count}} |
| TLP:AMBER | {{count}} | {{count}} |
| TLP:GREEN | {{count}} | {{count}} |
| TLP:CLEAR | {{count}} | {{count}} |"

### 6. Update Frontmatter & Append to Report

**Update frontmatter:**
- Add this step name to the end of `stepsCompleted`
- `iocs_total`: final consolidated count
- `iocs_by_type`: final breakdown by type
- `iocs_active`: count of active IOCs
- `iocs_historical`: count of historical IOCs
- `stix_bundle_created`: true
- `stix_objects`: total STIX objects in bundle
- `sigma_rules_created`: count
- `yara_rules_created`: count
- `suricata_rules_created`: count
- `siem_queries_created`: count
- `tlp_classification`: overall report TLP
- `tlp_distribution`: counts per TLP level

**Append to report under `## IOC & Indicator Summary`:**
- IOC Consolidation (full inventory table)
- IOC Lifecycle Assessment
- STIX 2.1 Bundle (summary + JSON in Appendix B)
- Detection Content (Sigma, YARA, Suricata, SIEM queries)
- TLP Classification & Handling

### 7. Present MENU OPTIONS

"**IOC packaging and detection content complete.**

**Packaging Summary:**
- IOCs consolidated: {{iocs_total}} total ({{iocs_active}} active, {{iocs_historical}} historical, {{expired_count}} expired)
- IOC types: {{ip_count}} IPs, {{domain_count}} domains, {{url_count}} URLs, {{hash_count}} hashes, {{email_count}} emails
- STIX 2.1 bundle: {{stix_objects}} objects ({{threat_actor_count}} actors, {{campaign_count}} campaigns, {{indicator_count}} indicators, {{relationship_count}} relationships)
- Sigma rules: {{sigma_count}} ({{high_conf_count}} high confidence)
- YARA rules: {{yara_count}}
- Suricata rules: {{suricata_count}}
- SIEM queries: {{siem_count}} (KQL + SPL)
- TLP distribution: {{red_count}} RED, {{amber_strict_count}} AMBER+STRICT, {{amber_count}} AMBER, {{green_count}} GREEN, {{clear_count}} CLEAR

**Detection Content Quality:**
- Rules with high confidence: {{count}} / {{total}}
- Rules with low FP risk: {{count}} / {{total}}
- ATT&CK technique coverage: {{covered_count}} / {{total_techniques}} techniques have detection rules

**Select an option:**
[A] Advanced Elicitation — Review detection content quality: are the Sigma rules specific enough to avoid FPs? Are the YARA rules resilient to minor malware variants? Are the Suricata rules testing on the right protocol fields? Are TLP classifications consistent and appropriate?
[W] War Room — Red Team: if I saw these detection rules, how would I evade them? Which rules would I trigger deliberately to create noise? What detection gaps remain that I would exploit? Blue Team: which rules should we deploy first? What is the expected alert volume? How do we tune for our specific environment? Should we deploy in detect-only mode first?
[C] Continue — Proceed to Step 8: Dissemination & Reporting (FINAL STEP — Step 8 of 8)"

#### Menu Handling Logic:

- IF A: Deep analysis — review each detection rule for specificity, resilience, and FP risk. Are Sigma rules too broad (matching legitimate admin tools)? Are YARA rules too narrow (matching only one sample variant)? Are Suricata rules matching on the right fields? Is the STIX bundle properly structured with correct relationships? Are TLP classifications consistent with source restrictions? Process insights, update if needed, redisplay menu
- IF W: War Room — Red Team perspective: these detection rules target my current TTPs. But what if I change tools? Which rules are based on volatile IOCs I can rotate overnight? Which rules detect behavior that I cannot easily change? Blue Team perspective: deployment prioritization — which rules give us the best coverage-to-FP ratio? How do we integrate the STIX bundle into our TIP? Which SIEM queries can we schedule as recurring searches? Summarize, redisplay menu
- IF C: Verify frontmatter updated with all IOC and detection content fields. Then read fully and follow: ./step-08-dissemination.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, iocs_total, iocs_by_type, iocs_active, iocs_historical, stix_bundle_created, stix_objects, sigma_rules_created, yara_rules_created, suricata_rules_created, siem_queries_created, tlp_classification, and tlp_distribution all updated, and IOC & Indicator Summary section fully populated in the output document], will you then read fully and follow: `./step-08-dissemination.md` to begin dissemination and reporting.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- IOCs consolidated from ALL steps (collection, actor profiling, Diamond Model pivots, Kill Chain mapping) into single inventory
- Every IOC carries context (source, confidence, lifecycle status, TLP, ATT&CK mapping, Kill Chain phase)
- IOC lifecycle assessment performed — active, historical, and expired IOCs distinguished with recommended actions
- STIX 2.1 bundle created with proper SDOs (threat-actor, campaign, indicator, malware, tool, attack-pattern, vulnerability, infrastructure, identity, report) and SROs (relationship, sighting)
- STIX patterns correctly formatted for each indicator type
- STIX relationships properly map actor-to-campaign, campaign-to-infrastructure, indicator-to-malware, etc.
- Sigma rules created with full metadata (tags, ATT&CK mapping, falsepositives, level)
- YARA rules created with proper conditions, string matching, and metadata
- Suricata rules created with protocol-specific detection and proper metadata
- KQL and SPL queries provided for SIEM deployment
- Every detection rule includes confidence level, FP risk assessment, and ATT&CK mapping
- TLP classification applied per indicator AND per product
- TLP handling instructions documented
- Frontmatter updated with all IOC and detection content fields
- Report section populated under IOC & Indicator Summary
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Not consolidating IOCs from all steps — missing IOCs from pivot analysis or Kill Chain mapping
- Not assessing IOC lifecycle — deploying expired IOCs blocks legitimate infrastructure
- Creating STIX objects without proper relationships — unlinked STIX objects lose analytic context
- Creating detection rules without ATT&CK mapping — unmapped rules cannot be correlated to threat coverage
- Creating detection rules without FP assessment — untested rules create alert fatigue
- Creating YARA rules that only match exact samples without variant resilience
- Not providing both KQL and SPL queries — organizations use different SIEM platforms
- Not applying TLP per indicator — bulk TLP misses source-specific restrictions
- Not distinguishing active from historical IOCs in the output — consumers need to know what to block vs what to hunt
- Beginning dissemination before IOC packaging is complete
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with IOC and detection content fields

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. IOC packaging is where intelligence becomes operationally deployable. Every indicator must be contextualized, every detection rule must be assessed for quality, every sharing decision must be TLP-compliant. The SOC analysts and detection engineers who receive these products will use them to protect the organization — production quality is not optional.
