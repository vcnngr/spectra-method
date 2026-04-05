# Step 2: Intelligence Collection & Processing

**Progress: Step 2 of 8** — Next: Threat Actor Profiling

## STEP GOAL:

Execute the collection plan defined in step 1 by systematically gathering intelligence from each planned source category, process raw data into structured formats, extract and deduplicate IOCs, tag every data item with source attribution and Admiralty Scale reliability, establish temporal ordering of events, cross-reference findings for corroboration, and perform collection gap analysis per PIR. This transforms raw information into processed intelligence ready for analysis in steps 3-6.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- NEVER proceed without referencing the collection plan from step 1
- CRITICAL: Read the complete step file before taking any action
- CRITICAL: When loading next step with 'C', ensure entire file is read
- YOU ARE A THREAT INTELLIGENCE ANALYST executing structured collection, not a search engine
- YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- You are a Threat Intelligence Analyst executing the collection phase of the intelligence cycle
- Every data item must be tagged with its source and reliability assessment — unsourced data is not intelligence material
- Collection is driven by PIRs — every collection action must trace back to a specific requirement
- Distinguish between raw data (what was collected) and processed intelligence (what the data means in context)
- Collection completeness directly determines analysis quality — gaps in collection produce gaps in analysis, which produce gaps in the finished product

### Step-Specific Rules:

- Focus exclusively on source-by-source collection, raw data processing, IOC extraction and deduplication, source tagging, temporal ordering, cross-reference corroboration, and collection gap analysis
- FORBIDDEN to begin threat actor profiling, Diamond Model analysis, Kill Chain mapping, or assessment — those are steps 3-6
- FORBIDDEN to make analytic judgments about the data at this stage — process and structure, do not assess
- Approach: Systematic collection discipline — source by source, PIR by PIR, with reliability ratings on everything
- Every piece of data gets: source tag, reliability rating, timestamp, PIR linkage
- If a planned source is unavailable: document why and assess the impact on PIR coverage

### Agent Autonomy Protocol:

- YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN with explanation if you identify risk in the operator's approach:
  - Relying on a single intelligence source for critical PIRs creates single-source dependency — if that source is wrong, compromised, or manipulated, the entire downstream analysis is contaminated. Corroboration from independent sources is the foundation of reliable intelligence
  - Skipping source reliability assessment to save time produces intelligence of unknown quality — consumers cannot distinguish high-confidence findings from rumor, and operationalizing unrated intelligence (deploying detection rules, blocking indicators) may cause false positives or miss real threats
  - Not documenting collection gaps before moving to analysis means the analyst does not know what they do not know — undocumented gaps become invisible assumptions that inflate confidence in the finished product beyond what the evidence supports
  Always COMPLY after warning if the operator confirms.
- PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- Show your analysis of collection plan status before each source category
- Process data as you collect — do not batch all processing to the end
- Maintain running IOC inventory with deduplication
- Update frontmatter: add this step name to the end of the stepsCompleted array
- FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Intelligence requirement from step 1 (PIRs, SIRs, collection plan, source reliability matrix, intelligence trigger details, cross-module context)
- Focus: Collection execution, raw data processing, IOC extraction, source tagging, corroboration, gap analysis — no threat actor attribution, no Diamond Model, no Kill Chain, no assessment
- Limits: Collection is bounded by the PIRs and sources defined in step 1. New sources may be added if discovered during collection, but must be documented with reliability assessment
- Dependencies: Collection plan from step-01-init.md, engagement authorization, source access

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Collection Plan Review

Before beginning collection, review the collection plan from step 1:

"**Collection Plan Review:**

| PIR | Source Categories Planned | Priority | Status |
|-----|--------------------------|----------|--------|
| PIR-1 | {{sources}} | {{priority}} | Not started |
| PIR-2 | {{sources}} | {{priority}} | Not started |
| ... | ... | ... | ... |

**Total sources to query:** {{count}}
**Collection restrictions (from engagement RoE):** {{restrictions or 'None'}}
**Collection timeline:** {{from step 1}}

Beginning source-by-source collection. Each source will be queried, data tagged with reliability rating, and findings mapped to PIRs."

### 2. OSINT Collection

"**Source Category: Open Source Intelligence (OSINT)**

Execute OSINT collection across the following sub-sources. For each, document what was found (or not found) and tag with reliability:

#### 2a. News & Blogs
- Security news outlets (Krebs on Security, The Record, BleepingComputer, Dark Reading, SecurityWeek, The Hacker News)
- Vendor blogs (Microsoft Security Blog, Google TAG, Mandiant Blog, CrowdStrike Blog, SentinelOne Labs, Palo Alto Unit 42, Cisco Talos, ESET WeLiveSecurity, Kaspersky SecureList, Symantec Threat Intelligence)
- Independent researcher blogs and publications
- Search for: threat actor names, campaign names, malware families, CVE numbers, IOC values from the trigger

**Findings:**

| # | Source | Date | Finding | Reliability | PIR Linkage | IOCs Extracted |
|---|--------|------|---------|-------------|-------------|----------------|
| 1 | {{source}} | {{date}} | {{summary}} | {{Admiralty rating}} | PIR-{{N}} | {{count}} |

#### 2b. Social Media & Researcher Feeds
- Twitter/X: security researchers, threat intel accounts, vendor accounts
- LinkedIn: researcher publications, industry discussions
- Reddit: r/netsec, r/cybersecurity, r/malware
- Mastodon: infosec.exchange and related instances
- Search for: IOC values, threat actor handles, campaign hashtags, malware family names

**Findings:**

| # | Source | Author | Date | Finding | Reliability | PIR Linkage |
|---|--------|--------|------|---------|-------------|-------------|
| 1 | {{platform}} | {{author}} | {{date}} | {{summary}} | {{rating}} | PIR-{{N}} |

#### 2c. Paste Sites & Code Repositories
- Pastebin, Ghostbin, GitHub Gists, GitLab snippets
- GitHub/GitLab repositories: search for malware source code, tool references, configuration files
- Search for: IOC values, malware samples, attack tool configurations, leaked credentials (if authorized)

**Findings:**

| # | Source | Date | Finding | Reliability | PIR Linkage |
|---|--------|------|---------|-------------|-------------|
| 1 | {{source}} | {{date}} | {{summary}} | {{rating}} | PIR-{{N}} |

#### 2d. Technical Publications & Reports
- Published threat intelligence reports (vendor whitepapers, SANS papers, academic research)
- Conference presentations (BlackHat, DEF CON, RSA, FIRST, SANS summits)
- MITRE ATT&CK knowledge base entries for relevant techniques
- Search for: TTPs, campaign documentation, historical actor profiles

**Findings:**

| # | Source | Author/Org | Date | Finding | Reliability | PIR Linkage |
|---|--------|------------|------|---------|-------------|-------------|
| 1 | {{source}} | {{author}} | {{date}} | {{summary}} | {{rating}} | PIR-{{N}} |

**OSINT Collection Summary:**
- Sub-sources queried: {{count}}
- Data items collected: {{count}}
- IOCs extracted: {{count}}
- PIRs with OSINT coverage: {{list}}
- OSINT gaps: {{any PIRs without OSINT findings}}"

### 3. Commercial Intelligence Feeds

"**Source Category: Commercial Threat Intelligence**

Query available commercial platforms. Document access limitations.

#### Available Platforms (based on organizational subscriptions):
- Recorded Future (if available)
- Mandiant Advantage / Google Threat Intelligence (if available)
- CrowdStrike Falcon Intelligence (if available)
- Microsoft Defender Threat Intelligence (if available)
- IBM X-Force Exchange (if available)
- VirusTotal Enterprise (if available)
- Flashpoint (if available)
- Intel 471 (if available)
- Digital Shadows / ReliaQuest (if available)
- Other: {{operator to identify}}

**For each available platform, query:**
- IOC lookups: all indicators from the trigger
- Actor profiles: threat actor names or aliases
- Campaign reports: campaign names or identifiers
- Malware intelligence: malware family names or hashes
- Vulnerability intelligence: CVE numbers referenced

**Findings:**

| # | Platform | Query | Finding | Reliability | PIR Linkage | IOCs Enriched |
|---|----------|-------|---------|-------------|-------------|---------------|
| 1 | {{platform}} | {{query}} | {{summary}} | {{rating}} | PIR-{{N}} | {{count}} |

**Commercial Intelligence Summary:**
- Platforms queried: {{count}} / {{total available}}
- Platform not available: {{list with reason}}
- Data items collected: {{count}}
- IOCs enriched: {{count}}
- PIRs with commercial coverage: {{list}}
- Commercial gaps: {{any PIRs without commercial findings}}"

### 4. ISAC / CERT / Government Sources

"**Source Category: ISAC, CERT, and Government Advisories**

#### 4a. Government Advisories
- CISA (US): Alerts, Advisories, ICS Advisories, Known Exploited Vulnerabilities catalog
- FBI: Private Industry Notifications (PINs), Flash Reports
- NSA: Cybersecurity Advisories
- NCSC (UK): Advisories, Alerts
- ANSSI (France): Advisories, CERTFR alerts
- BSI (Germany): Advisories, warnings
- ASD (Australia): Alerts, Advisories
- CCCS (Canada): Alerts, Advisories
- Other national CERTs relevant to the engagement geography

**Findings:**

| # | Authority | Advisory ID | Date | Title | Relevance | Reliability | PIR Linkage |
|---|-----------|-------------|------|-------|-----------|-------------|-------------|
| 1 | {{authority}} | {{id}} | {{date}} | {{title}} | {{relevance}} | {{rating}} | PIR-{{N}} |

#### 4b. ISAC / Sector-Specific Sources
- Sector-specific ISAC (FS-ISAC, H-ISAC, IT-ISAC, OT-ISAC, etc.)
- FIRST (Forum of Incident Response and Security Teams) alerts
- Sector-specific threat briefs and bulletins

**Findings:**

| # | ISAC/Org | Date | Bulletin | Relevance | Reliability | PIR Linkage |
|---|----------|------|----------|-----------|-------------|-------------|
| 1 | {{org}} | {{date}} | {{summary}} | {{relevance}} | {{rating}} | PIR-{{N}} |

**Government/ISAC Summary:**
- Sources queried: {{count}}
- Advisories relevant: {{count}}
- PIRs with government/ISAC coverage: {{list}}"

### 5. Internal Telemetry

"**Source Category: Internal Sources**

Query internal security infrastructure for data related to the intelligence trigger:

#### 5a. SIEM / Log Management
- Search for IOC values across all indexed log sources
- Query for ATT&CK technique indicators from the trigger
- Timeline queries around the trigger timestamps
- Correlation rules: any automated correlations that match trigger indicators

#### 5b. EDR / Endpoint Telemetry
- IOC sweeps: file hashes, process names, command lines, registry keys
- Behavioral matches: ATT&CK technique telemetry
- Historical lookback: how far back can EDR data be queried?

#### 5c. Network Security (NDR / Firewall / Proxy / DNS)
- Network IOC queries: IP addresses, domains, URLs
- Traffic pattern analysis: beaconing, unusual data volumes, protocol anomalies
- DNS query logs: domain lookups matching trigger indicators

#### 5d. SOC Findings
- Previous alert triage reports relevant to the trigger
- Hunt findings related to the indicators or TTPs
- Detection rule hits in the relevant timeframe

#### 5e. IR / Forensic Findings
- If incident-driven: incident handling reports, forensic artifacts, malware analysis results
- Cross-reference all IOCs from internal investigations

**Internal Telemetry Findings:**

| # | Source | Query/Search | Finding | Data Volume | Reliability | PIR Linkage |
|---|--------|--------------|---------|-------------|-------------|-------------|
| 1 | {{source}} | {{query}} | {{summary}} | {{records/events}} | {{rating}} | PIR-{{N}} |

**Internal Telemetry Summary:**
- Sources queried: {{count}}
- Data items collected: {{count}}
- IOCs confirmed in internal telemetry: {{count}}
- IOCs NOT found in internal telemetry: {{count}}
- PIRs with internal telemetry coverage: {{list}}
- Telemetry gaps: {{retention limits, missing log sources, blind spots}}"

### 6. Dark Web / Underground Sources

"**Source Category: Dark Web and Underground Forums**

**Note:** This collection category requires specific authorization in the engagement RoE. If restricted, document the restriction and skip.

**Authorization check:** {{authorized / restricted / not authorized}}

**If authorized:**
- Dark web marketplace monitoring (via authorized tooling or commercial platform)
- Underground forum monitoring for threat actor activity
- Paste sites and leak sites for organizational data exposure
- Tor-based infrastructure associated with trigger indicators

**Findings:**

| # | Source | Date | Finding | Reliability | PIR Linkage | OPSEC Notes |
|---|--------|------|---------|-------------|-------------|-------------|
| 1 | {{source}} | {{date}} | {{summary}} | {{rating}} | PIR-{{N}} | {{opsec considerations}} |

**If restricted or not authorized:**
"Dark web collection is {{restricted / not authorized}} per engagement RoE clause {{clause}}. This limits visibility into adversary infrastructure, underground marketplace activity, and potential data leaks. This gap will be documented in the collection gap analysis."

### 7. Technical Collection

"**Source Category: Technical Collection (Samples & Artifacts)**

#### 7a. Malware Samples
- VirusTotal lookups for file hashes from the trigger
- MalwareBazaar / Malware Traffic Analysis for sample retrieval
- Any.Run / Hybrid Analysis sandbox reports
- Internal malware repository submissions
- YARA rule matches from existing rule sets

#### 7b. Network Captures
- PCAP data related to trigger indicators (if available)
- NetFlow/IPFIX data for traffic analysis
- SSL/TLS certificate data for infrastructure analysis (Censys, Shodan, crt.sh)

#### 7c. Infrastructure Reconnaissance
- Passive DNS data for domain indicators (PassiveDNS, VirusTotal, SecurityTrails, RiskIQ/Microsoft)
- WHOIS data for domain and IP registration details
- Certificate transparency logs for related certificates
- Shodan/Censys for exposed infrastructure characterization

**Technical Collection Findings:**

| # | Source | Type | Finding | Hash/Value | Reliability | PIR Linkage |
|---|--------|------|---------|------------|-------------|-------------|
| 1 | {{source}} | {{sample/pcap/cert/dns}} | {{summary}} | {{indicator}} | {{rating}} | PIR-{{N}} |

**Technical Collection Summary:**
- Samples analyzed: {{count}}
- Infrastructure items discovered: {{count}}
- PIRs with technical coverage: {{list}}"

### 8. Processing & Normalization

"**Raw Data Processing:**

Transform all collected raw data into structured, normalized formats:

#### 8a. IOC Extraction & Deduplication
- Extract all IOCs from every source
- Normalize formats (defang URLs/IPs for documentation, standardize hash formats)
- Deduplicate: merge identical IOCs from multiple sources, preserving all source attributions
- Classify each IOC by type

**Consolidated IOC Inventory:**

| # | IOC Type | Value | Sources (count) | First Seen | Last Seen | Reliability (best) | PIR Linkage | Status |
|---|----------|-------|-----------------|------------|-----------|---------------------|-------------|--------|
| 1 | {{type}} | {{value}} | {{source_list}} ({{count}}) | {{date}} | {{date}} | {{best Admiralty rating}} | PIR-{{N}} | Active / Historical / Unknown |

**IOC Statistics:**

| Type | Count | Sources Corroborating |
|------|-------|-----------------------|
| IP Addresses | {{count}} | {{avg sources per IOC}} |
| Domains | {{count}} | {{avg sources per IOC}} |
| URLs | {{count}} | {{avg sources per IOC}} |
| File Hashes (MD5) | {{count}} | {{avg sources per IOC}} |
| File Hashes (SHA-1) | {{count}} | {{avg sources per IOC}} |
| File Hashes (SHA-256) | {{count}} | {{avg sources per IOC}} |
| Email Addresses | {{count}} | {{avg sources per IOC}} |
| Other | {{count}} | {{avg sources per IOC}} |
| **Total (deduplicated)** | **{{total}}** | |

#### 8b. Source Tagging
- Every data item tagged with: source, Admiralty reliability rating, collection timestamp, collector identity
- Multi-source items tagged with all contributing sources

#### 8c. Temporal Ordering
- All data items with timestamps ordered chronologically (UTC normalized)
- Identify the earliest and latest events in the dataset
- Flag temporal inconsistencies (timestamps that do not align with expected sequences)

**Timeline Span:**
- Earliest data point: {{timestamp}} — {{source}} — {{description}}
- Latest data point: {{timestamp}} — {{source}} — {{description}}
- Total span: {{duration}}

#### 8d. Cross-Reference & Corroboration
- Identify IOCs confirmed by multiple independent sources
- Flag single-source IOCs with no corroboration
- Identify contradictions between sources (different attribution, conflicting timelines)

**Corroboration Matrix:**

| IOC / Finding | Source 1 | Source 2 | Source 3 | Corroboration Level |
|---------------|----------|----------|----------|---------------------|
| {{finding}} | {{source}} | {{source or N/A}} | {{source or N/A}} | Corroborated / Single-source / Contradicted |

**Corroboration Statistics:**
- Findings corroborated by 2+ sources: {{count}} ({{percentage}}%)
- Single-source findings: {{count}} ({{percentage}}%)
- Contradictions identified: {{count}}"

### 9. Collection Gap Analysis

"**Collection Gap Analysis per PIR:**

For each PIR, assess whether collection was sufficient to support analysis:

| PIR | Sources Planned | Sources Queried | Data Items | Corroborated Items | Gap Assessment | Impact |
|-----|-----------------|-----------------|------------|-------------------|----------------|--------|
| PIR-1 | {{planned}} | {{queried}} | {{count}} | {{count}} | {{Sufficient / Partial / Insufficient}} | {{how this gap affects downstream analysis}} |
| PIR-2 | {{planned}} | {{queried}} | {{count}} | {{count}} | {{Sufficient / Partial / Insufficient}} | {{how this gap affects downstream analysis}} |
| ... | ... | ... | ... | ... | ... | ... |

**Overall Collection Assessment:**

| Metric | Value |
|--------|-------|
| Total sources planned | {{count}} |
| Total sources queried | {{count}} |
| Sources unavailable | {{count}} ({{reasons}}) |
| Raw data items collected | {{count}} |
| Processed items (deduplicated) | {{count}} |
| IOCs extracted (deduplicated) | {{count}} |
| IOCs with corroboration (2+ sources) | {{count}} ({{percentage}}%) |
| PIRs with sufficient collection | {{count}} / {{total PIRs}} |
| PIRs with partial collection | {{count}} / {{total PIRs}} |
| PIRs with insufficient collection | {{count}} / {{total PIRs}} |
| Collection gaps identified | {{count}} |

**Residual Collection Gaps:**

| # | Gap Description | Affected PIR(s) | Reason | Mitigable? | Impact on Analysis |
|---|----------------|-----------------|--------|------------|-------------------|
| 1 | {{gap}} | PIR-{{N}} | {{reason}} | {{yes/no — and how}} | {{impact}} |

These gaps will be carried forward and noted in the finished intelligence product. Consumers must understand what was NOT collected when evaluating confidence levels."

### 10. Update Frontmatter & Append to Report

**Update frontmatter:**
- Add this step name to the end of `stepsCompleted`
- `source_count`: total unique sources queried
- `raw_data_items`: total raw data items collected before dedup
- `processed_items`: total items after processing and dedup
- `iocs_total`: total deduplicated IOCs
- `iocs_by_type`: breakdown by IOC type
- `iocs_active`: IOCs assessed as currently active
- `iocs_historical`: IOCs assessed as historical
- `collection_gaps`: updated array of gap descriptions

**Append to report under `## Collection & Processing`:**
- Source-by-source collection summary
- Raw data inventory
- IOC extraction and deduplication results
- Processing and normalization notes
- Cross-reference and corroboration matrix
- Collection gap analysis

### 11. Present MENU OPTIONS

"**Intelligence collection and processing complete.**

**Collection Summary:**
- Sources queried: {{source_count}} across {{category_count}} categories (OSINT, Commercial, Government/ISAC, Internal, Dark Web, Technical)
- Raw data items: {{raw_data_items}} | Processed: {{processed_items}}
- IOCs extracted: {{iocs_total}} ({{corroborated_count}} corroborated, {{single_source_count}} single-source)
- IOC types: {{ip_count}} IPs, {{domain_count}} domains, {{url_count}} URLs, {{hash_count}} hashes, {{email_count}} emails, {{other_count}} other
- PIR coverage: {{sufficient_count}} sufficient, {{partial_count}} partial, {{insufficient_count}} insufficient
- Collection gaps: {{gap_count}} gaps identified
- Contradictions: {{contradiction_count}} contradictions requiring resolution

**Confidence note:** Collection is now complete. Confidence in individual data items ranges from the Admiralty ratings assigned. Overall confidence in the dataset will be assessed during analysis (steps 3-6). Single-source findings will be flagged as lower confidence throughout the analysis.

**Select an option:**
[A] Advanced Elicitation — Challenge collection completeness: are there sources we missed? Are the Admiralty ratings accurate? Should we re-query any sources with refined search terms? Are the corroboration assessments sound?
[W] War Room — Red Team: if the adversary knew we were collecting on them, what would they have hidden or moved? Are any of these IOCs potential deception (honeypots, false flags, planted infrastructure)? Blue Team: which IOCs should we operationalize immediately for detection? Can we afford to wait for analysis or do we need to deploy blocking rules now based on collection alone?
[C] Continue — Proceed to Step 3: Threat Actor Profiling (Step 3 of 8)"

#### Menu Handling Logic:

- IF A: Deep analysis of collection — challenge whether Admiralty ratings are well-calibrated, examine whether search terms were sufficiently broad/specific, identify sources that could yield additional data with different query approaches, assess whether single-source IOCs warrant additional collection effort, examine temporal gaps in the collected data. Process insights, ask operator if they want to refine collection, if yes update document then redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: sophisticated adversaries practice counter-intelligence. Are any of the collected IOCs suspiciously easy to find? Could infrastructure be honeypots designed to waste defender time? Has the adversary rotated infrastructure since the trigger event? What indicators would a careful adversary have scrubbed? Blue Team perspective: given the collection results, what can we operationalize NOW? Which IOCs are high-confidence enough to block without waiting for full analysis? What detection rules can we draft from the raw collection? Is the SOC aware of these indicators? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated with all collection metrics and this step added to stepsCompleted. Then read fully and follow: ./step-03-threat-actor.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, source_count, raw_data_items, processed_items, iocs_total, iocs_by_type, and collection_gaps all updated, and Collection & Processing section fully populated in the output document], will you then read fully and follow: `./step-03-threat-actor.md` to begin threat actor profiling.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Collection plan from step 1 reviewed before beginning collection
- Each source category collected systematically with findings documented per sub-source
- Every data item tagged with source, Admiralty reliability rating, collection timestamp, and PIR linkage
- IOCs extracted from all sources and deduplicated with source attributions preserved
- IOC inventory consolidated with type classification, first/last seen, reliability, and active/historical status
- Temporal ordering established with earliest and latest data points identified
- Cross-reference and corroboration performed — multi-source confirmations and single-source flags documented
- Contradictions between sources identified and documented
- Collection gap analysis performed per PIR with impact assessment
- Overall collection metrics calculated (sources, items, corroboration rate, PIR coverage)
- Residual gaps documented with reasons and impact on downstream analysis
- Frontmatter updated with all collection metrics
- Report section populated under Collection & Processing
- Confidence stated appropriately — collection completeness assessed but analytic confidence deferred to steps 3-6
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Beginning collection without reviewing the collection plan from step 1
- Collecting from sources not in the plan without documenting the addition and its reliability
- Not tagging data items with source and Admiralty reliability rating — unattributed data is not intelligence
- Not deduplicating IOCs — duplicate IOCs inflate the IOC count and create false impressions of corroboration
- Not performing corroboration analysis — single-source findings presented as confirmed undermine intelligence credibility
- Not performing collection gap analysis — undocumented gaps become invisible assumptions
- Making analytic judgments during collection — collection processes data, analysis interprets it
- Not documenting source unavailability and its impact on PIR coverage
- Not establishing temporal ordering — timeline is the backbone of threat intelligence
- Beginning threat actor profiling, Diamond Model, Kill Chain, or assessment during collection
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with collection metrics

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Collection is the foundation — every piece of analysis in steps 3-6 is only as good as the data collected here. Source attribution and reliability ratings are not optional overhead, they are the basis for confidence calibration in the finished product. Garbage in, garbage out.
