# Step 4: IOC Extraction & Enrichment

**Progress: Step 4 of 8** — Next: Scope & Impact Assessment

## STEP GOAL:

Extract ALL Indicators of Compromise (IOCs) from headers, content, and attachments analyzed in previous steps, systematically enrich each IOC against threat intelligence sources, map all identified techniques to the MITRE ATT&CK framework (specifically Initial Access and Execution tactics), assess whether this phishing email is part of a known campaign or threat actor operation, and produce a comprehensive enrichment report that informs the scope and impact assessment in the next step.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER enrich IOCs without first verifying they were extracted from previous steps
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC PHISHING ANALYST, not an autonomous threat intelligence platform
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst conducting structured phishing investigation
- ✅ IOC enrichment transforms raw observables into intelligence — this step is the foundation for scope assessment and containment decisions
- ✅ Every enrichment finding must cite the source and confidence level — unsupported claims degrade investigation quality
- ✅ Enrichment informs but does not replace analyst judgment — a clean IOC can still be malicious (novel infrastructure, targeted operations)
- ✅ Phishing-specific ATT&CK mapping is critical — T1566 sub-techniques and T1204 User Execution must be explicitly mapped

### Step-Specific Rules:

- 🎯 Focus exclusively on IOC extraction, enrichment, ATT&CK mapping, and campaign assessment
- 🚫 FORBIDDEN to begin scope assessment, containment, or any active defensive action — this is intelligence gathering
- 💬 Approach: Systematic extraction and enrichment of each IOC category against multiple sources with cross-referencing
- 📊 Every IOC must include: source queried, result, confidence level, and relevance to the phishing investigation
- 🔒 All IOCs must originate from data analyzed in steps 1-3 — do not fabricate indicators

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Querying public enrichment services with IOCs from a sensitive engagement may expose investigation indicators to third parties — domains, IPs, and hashes submitted to VirusTotal become public and searchable; if the phishing campaign is targeted (spearphishing), the attacker may monitor VT submissions to detect investigation activity; consider whether private/internal-only enrichment is appropriate for high-sensitivity engagements
  - Enrichment results from a single source may be incomplete or outdated — phishing infrastructure is ephemeral, with domains and IPs often rotated every 24-72 hours; cross-referencing multiple sources improves confidence, and absence of intelligence does not mean absence of threat
  - ATT&CK mapping should reflect the FULL kill chain implied by the phishing email, not just the delivery technique — if the payload is a loader that downloads Cobalt Strike, the ATT&CK mapping should include not just T1566 (Phishing) but also T1059 (Command and Scripting Interpreter), T1105 (Ingress Tool Transfer), and downstream techniques; limiting mapping to T1566 alone underrepresents the threat
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present IOC extraction inventory and enrichment plan before beginning queries — get user confirmation on sources to use
- ⚠️ Present [A]/[W]/[C] menu after enrichment complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `iocs_extracted`, `iocs_enriched`, `mitre_techniques`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, phishing email sample, extracted metadata, header analysis, content analysis from steps 1-3
- Focus: IOC extraction, enrichment, ATT&CK mapping, campaign assessment
- Limits: Only enrich IOCs present in the steps 1-3 analysis — do not invent indicators
- Dependencies: Completed email intake (step 1), header analysis (step 2), content analysis (step 3)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. IOC Extraction from All Sources

Systematically extract ALL IOCs from the analysis performed in steps 1-3. Categorize by type and source step.

**IOC Extraction — Headers (Step 2):**

| # | IOC | Type | Source | Context |
|---|-----|------|--------|---------|
| H1 | {{sender_email}} | Email Address | From header | Sender identity |
| H2 | {{reply_to_email}} | Email Address | Reply-To header | Reply destination (if different from From) |
| H3 | {{return_path}} | Email Address | Return-Path header | Envelope sender |
| H4 | {{origin_ip}} | IP Address | First Received header | True origin server |
| H5 | {{relay_ips}} | IP Address | Received chain | Intermediate relay servers |
| H6 | {{sender_domain}} | Domain | From address | Sender domain |
| H7 | {{dkim_domain}} | Domain | DKIM d= | DKIM signing domain |
| H8 | {{x_originating_ip}} | IP Address | X-Originating-IP | Client IP of sender |
| ... | ... | ... | ... | ... |

**IOC Extraction — Content (Step 3):**

| # | IOC | Type | Source | Context |
|---|-----|------|--------|---------|
| C1 | {{url_1_defanged}} | URL | Body/HTML href | {{link destination}} |
| C2 | {{url_2_defanged}} | URL | Redirect chain | {{intermediate redirect}} |
| C3 | {{final_landing_url}} | URL | Redirect resolution | {{final destination}} |
| C4 | {{url_domain_1}} | Domain | URL extraction | {{domain from URL}} |
| C5 | {{tracking_pixel_url}} | URL | Embedded image | {{tracking/beacon}} |
| ... | ... | ... | ... | ... |

**IOC Extraction — Attachments (Step 3):**

| # | IOC | Type | Source | Context |
|---|-----|------|--------|---------|
| A1 | {{md5_hash}} | File Hash (MD5) | Attachment hash | {{filename}} |
| A2 | {{sha1_hash}} | File Hash (SHA1) | Attachment hash | {{filename}} |
| A3 | {{sha256_hash}} | File Hash (SHA256) | Attachment hash | {{filename}} |
| A4 | {{embedded_url}} | URL | Macro/script content | {{C2 or download URL from attachment}} |
| A5 | {{embedded_ip}} | IP Address | Macro/script content | {{C2 IP from attachment}} |
| ... | ... | ... | ... | ... |

**IOC Extraction Summary:**

```
Total IOCs Extracted: {{total_count}}
- IP Addresses: {{count}}
- Domains: {{count}}
- URLs: {{count}}
- File Hashes: {{count}} ({{unique_files}} unique files × 3 hash types)
- Email Addresses: {{count}}
- Other (user agents, sender infrastructure): {{count}}

Sources:
- From headers (Step 2): {{count}} IOCs
- From content (Step 3): {{count}} IOCs
- From attachments (Step 3): {{count}} IOCs
```

"**IOC inventory extracted: {{total_count}} indicators across {{category_count}} categories.**

Ready to begin enrichment. Confirm to proceed, or specify any IOCs to exclude from public lookups (e.g., for OPSEC reasons in a sensitive engagement)."

**WAIT for user confirmation before querying sources.**

### 2. Enrichment per IOC Type

For each IOC category, query appropriate threat intelligence sources and present results:

#### A. IP Address Enrichment

For each extracted IP address:

- **VirusTotal**: Detection ratio, community score, last analysis date, associated malware samples
- **AbuseIPDB**: Confidence score, total reports, abuse categories, last reported date
- **GreyNoise**: Classification (benign/malicious/unknown), noise vs targeted, actor tags, bot activity
- **Shodan**: Open ports, running services, HTTP headers, SSL certificates, organization, ASN
- **Geolocation**: Country, city, ISP, ASN name, hosting provider
- **Reverse DNS**: PTR record — does it match the expected hostname?

**IP Risk Indicators** (flag if any apply):
- IP belongs to a known bulletproof hosting provider (FlokiNET, Shinjiru, etc.)
- IP is a Tor exit node, known VPN endpoint, or open proxy
- IP has been recently allocated or changed ownership (new allocation = no reputation history)
- IP shares ASN with other known malicious infrastructure from enrichment
- Reverse DNS points to suspicious or auto-generated hostnames (e.g., random-string.vps-provider.com)
- IP runs mail services inconsistent with the claimed sender (e.g., residential IP running SMTP)

Present per-IP enrichment:

```
| IP | VT Score | AbuseIPDB Conf. | GreyNoise Class | Geo / ASN | Services | Verdict |
|----|----------|----------------|-----------------|-----------|----------|---------|
| {{ip}} | {{detections}}/{{total}} | {{score}}% ({{reports}} reports) | {{class}} | {{country}} / AS{{num}} {{org}} | {{ports/services}} | Malicious/Suspicious/Clean/Unknown |
```

#### B. Domain Enrichment

For each extracted domain:

- **VirusTotal**: Detection ratio, assigned categories, community votes, subdomains
- **WHOIS**: Registration date, registrar, registrant info, name servers
- **Domain age**: Days since registration (< 30 days = suspicious flag, < 7 days = high risk)
- **Passive DNS**: Historical IP resolutions, sibling domains on same infrastructure, DNS record changes
- **URLScan.io**: Page screenshot (if domain hosts a page), redirect chain, embedded resources, contacted IPs

**Domain Risk Indicators** (flag if any apply):
- Domain registered within last 30 days (newly registered domain — common phishing infrastructure)
- Domain uses privacy-protected WHOIS registration (not inherently malicious but common in phishing)
- Domain mimics a legitimate brand (typosquatting: microsofft.com, homoglyph: rnicrosоft.com with Cyrillic о)
- Domain resolves to multiple IPs in short timeframe (fast-flux behavior)
- Domain name matches known DGA patterns (high entropy, random character sequences)
- Domain registered at same registrar as known phishing domains from threat intel
- Domain uses free DNS hosting (afraid.org, freedns) or free TLS (Let's Encrypt) — not malicious alone but common in commodity phishing

Present per-domain enrichment:

```
| Domain | VT Score | Domain Age | WHOIS Registrar | PDNS (Recent IPs) | Risk Indicators | Verdict |
|--------|----------|-----------|-----------------|-------------------|-----------------|---------|
| {{domain}} | {{detections}}/{{total}} | {{age}} days | {{registrar}} | {{ip_list}} | {{indicators}} | Malicious/Suspicious/Clean/Unknown |
```

#### C. URL Enrichment

For each extracted URL:

- **VirusTotal**: Detection ratio, scan date, category, community votes
- **PhishTank**: Known phishing URL? Reported date, target brand
- **Google Safe Browsing**: Classification (phishing, malware, unwanted software, social engineering)
- **URLhaus**: Known malware distribution URL? Associated payloads, first seen, last seen
- **URLScan.io**: Live scan results (if safe to submit), redirect chain, final page content

Present per-URL enrichment:

```
| URL (defanged) | VT Score | PhishTank | Safe Browsing | URLhaus | Category | Verdict |
|---------------|----------|-----------|---------------|---------|----------|---------|
| {{url}} | {{detections}}/{{total}} | {{listed/not_listed}} | {{clean/flagged}} | {{listed/not_listed}} | {{phishing/malware/clean/unknown}} | Malicious/Suspicious/Clean/Unknown |
```

#### D. File Hash Enrichment

For each file hash (prefer SHA256, supplement with MD5/SHA1):

- **VirusTotal**: AV detection ratio, malware family names, first seen/last seen dates, behavioral analysis summary
- **MalwareBazaar**: Malware tags, YARA rule matches, associated campaigns, delivery method
- **Hybrid Analysis**: Behavioral summary, contacted IPs/domains, dropped files, process execution chain

Present per-hash enrichment:

```
| Hash (SHA256) | Filename | VT Detections | Malware Family | First Seen | Campaign | Verdict |
|--------------|----------|---------------|---------------|------------|----------|---------|
| {{hash}} | {{filename}} | {{detections}}/{{total}} | {{family or 'Unknown'}} | {{date}} | {{campaign or 'None'}} | Malicious/Suspicious/Clean/Unknown |
```

#### E. Email Address Enrichment

For each extracted email address:

- **Domain reputation**: Apply domain enrichment (above) to the email domain
- **Known campaign association**: Check against threat intel feeds for sender involvement in reported phishing campaigns
- **Disposable/temporary email check**: Flag throwaway domains (mailinator, guerrillamail, tempmail, yopmail, sharklasers, etc.)
- **Email address pattern**: Is the local part auto-generated (random strings) or human-readable?
- **Breach database presence**: Has this email appeared in known data breaches (indicates compromised account vs purpose-built)?

Present per-email enrichment:

```
| Email / Domain | Domain VT Score | Domain Age | Disposable? | Campaign Match | Pattern | Verdict |
|----------------|----------------|-----------|-------------|----------------|---------|---------|
| {{email}} | {{score}} | {{age}} | Yes/No | {{campaign or 'None'}} | {{human/auto-generated}} | Malicious/Suspicious/Clean/Unknown |
```

### 3. Enrichment Summary

Consolidate all enrichment results into a unified summary:

**Enrichment Statistics:**
```
Total IOCs Enriched: {{total}}
- Malicious: {{count}} ({{percent}}%)
- Suspicious: {{count}} ({{percent}}%)
- Clean: {{count}} ({{percent}}%)
- Unknown (no data): {{count}} ({{percent}}%)

Cross-reference hits: {{count}} IOCs appeared in multiple threat intel sources
Single-source only: {{count}} IOCs had results from only one source
Zero-hit IOCs: {{count}} IOCs had no results from any source (potential novel infrastructure)
```

**Consolidated IOC Table:**

```
| # | IOC | Type | Reputation | Threat Label | Confidence | Key Finding |
|---|-----|------|------------|-------------|------------|-------------|
| 1 | {{ioc}} | {{type}} | Malicious/Suspicious/Clean/Unknown | {{label or 'None'}} | High/Medium/Low | {{finding}} |
```

### 4. MITRE ATT&CK Mapping

Map all identified techniques to the ATT&CK framework. Phishing investigations MUST map the delivery technique AND the implied post-delivery techniques based on payload analysis.

**Phishing-Specific ATT&CK Techniques:**

| Technique ID | Technique Name | Evidence | Confidence |
|-------------|---------------|----------|------------|
| **T1566.001** | Spearphishing Attachment | {{attachment present with malicious indicators? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1566.002** | Spearphishing Link | {{malicious URL in body? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1566.003** | Spearphishing via Service | {{delivered via social media, messaging, or non-email service? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1566.004** | Spearphishing Voice (Vishing) | {{phone number provided for callback? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1204.001** | User Execution: Malicious Link | {{user must click URL for attack to succeed? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1204.002** | User Execution: Malicious File | {{user must open attachment for attack to succeed? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1598** | Phishing for Information | {{email requests sensitive information without technical payload? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1598.002** | Phishing for Info: Spearphishing Attachment | {{attachment designed to collect info (form, survey)? Evidence.}} | {{High/Medium/Low/N/A}} |
| **T1598.003** | Phishing for Info: Spearphishing Link | {{link leads to info collection page? Evidence.}} | {{High/Medium/Low/N/A}} |

**Implied Post-Delivery Techniques (based on payload analysis from Step 3):**

| Technique ID | Technique Name | Evidence | Confidence |
|-------------|---------------|----------|------------|
| T1059.001 | PowerShell | {{macro executes PowerShell? Script content indicates PS execution?}} | {{H/M/L/N/A}} |
| T1059.003 | Windows Command Shell | {{payload executes cmd.exe commands?}} | {{H/M/L/N/A}} |
| T1059.005 | Visual Basic | {{VBA macros in Office document?}} | {{H/M/L/N/A}} |
| T1059.007 | JavaScript | {{.js attachment or HTML with JS execution?}} | {{H/M/L/N/A}} |
| T1105 | Ingress Tool Transfer | {{payload downloads additional files from C2?}} | {{H/M/L/N/A}} |
| T1078 | Valid Accounts | {{credential harvesting page — stolen creds enable account access?}} | {{H/M/L/N/A}} |
| T1071.001 | Web Protocols | {{payload communicates via HTTP/HTTPS?}} | {{H/M/L/N/A}} |
| T1218.* | System Binary Proxy Execution | {{payload uses mshta, rundll32, regsvr32, etc.?}} | {{H/M/L/N/A}} |
| T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys | {{payload establishes persistence via Run keys?}} | {{H/M/L/N/A}} |
| {{additional}} | {{additional techniques based on specific payload behavior}} | {{evidence}} | {{confidence}} |

**ATT&CK Summary:**
```
Primary Tactic: Initial Access (TA0001)
Primary Technique: {{T1566.00X — specific sub-technique}}
Secondary Tactics: {{Execution (TA0002), Persistence (TA0003), etc. — based on payload}}
Total Techniques Mapped: {{count}}
Kill Chain Coverage: {{tactics covered}}
```

### 5. Campaign and Threat Actor Assessment

Based on enrichment results and ATT&CK mapping, assess whether this phishing email is part of a known campaign or threat actor operation:

**Known Threat Actor / Campaign Association:**
- Do any IOCs map to known APT groups, cybercrime operations, or named campaigns?
- Are there shared infrastructure indicators (overlapping IPs, domains, or hashes across known threat actor profiles)?
- Does the phishing technique match known playbooks (e.g., Emotet's invoice theme, QakBot's reply-chain hijacking, BazarLoader's Google Docs lure)?

**Known Malware Family:**
- Did hash lookups identify a specific malware family?
- What are the known capabilities of this malware family (loader, RAT, infostealer, ransomware precursor)?
- What is the typical kill chain for this malware family after initial delivery?

**Infrastructure Pattern Analysis:**
- Bulletproof hosting, Tor, VPN, cloud hosting?
- Newly registered domains, DGA patterns?
- Shared hosting with other known phishing infrastructure?
- Infrastructure reuse from previous campaigns?

**Novel / Unknown Indicators:**
- IOCs with zero hits across all sources — potentially targeted/custom tooling
- Recently provisioned infrastructure (domains < 30 days, IPs with no history)
- Unique social engineering approach not matching known templates

**Campaign Assessment:**
```
Campaign Type: {{Known campaign / Likely part of known campaign / Unknown campaign / Novel/Targeted / Commodity phishing}}
Threat Actor: {{named actor or 'Unattributed'}}
Malware Family: {{identified family or 'Not identified'}}
Campaign Scale: {{mass / semi-targeted / spearphishing / whaling}}
Infrastructure Sophistication: {{commodity (free services) / moderate (registered domains, basic OPSEC) / advanced (dedicated infrastructure, authentication configured, OPSEC-aware)}}
Enrichment Confidence: {{High (multi-source corroboration) / Medium (limited sources) / Low (mostly unknown)}}
```

### 6. Present Enrichment Results to User

"**IOC Enrichment Complete — {{incident_id}}**

**Enrichment Summary:** {{total_enriched}} IOCs enriched across {{category_count}} categories.
- Malicious: {{malicious_count}} | Suspicious: {{suspicious_count}} | Clean: {{clean_count}} | Unknown: {{unknown_count}}

**ATT&CK Mapping:** {{total_techniques}} techniques mapped
- Primary: {{primary_technique}} ({{tactic}})
- Kill chain depth: {{tactics covered}}

**Campaign Assessment:**
- Campaign type: {{assessment}}
- Threat actor: {{actor or 'Unattributed'}}
- Malware family: {{family or 'Not identified'}}
- Confidence: {{confidence}}

**Key Findings:**
1. {{most significant enrichment finding}}
2. {{second most significant}}
3. {{third most significant}}"

### 7. Present MENU OPTIONS

"**Select an option:**
[A] Advanced Elicitation — Deep-dive into specific IOC enrichment findings, challenge assumptions about clean/unknown IOCs, explore infrastructure connections
[W] War Room — Red vs Blue discussion on enrichment implications — what do the IOCs reveal about attacker infrastructure and capability?
[C] Continue — Proceed to Scope & Impact Assessment (Step 5 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive enrichment analysis — challenge assumptions about clean/unknown IOCs, explore potential false negatives in threat intel coverage, investigate whether IOCs with low confidence could be higher risk than assessed, examine cross-references between IOCs that may reveal hidden patterns, look for infrastructure overlaps. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: if I were the attacker, which IOCs would I ensure stay clean? What infrastructure would evade these enrichment sources? Which IOCs are decoys vs operational? How would I rotate infrastructure to stay ahead of enrichment databases? Blue Team perspective: are we over-relying on reputation scores? What do the unknown IOCs tell us? How do we handle novel threats with zero intel hits? Should we submit IOCs to sandbox services for behavioral analysis? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `iocs_extracted`, `iocs_enriched`, `mitre_techniques`, then read fully and follow: ./step-05-scope-impact.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and iocs_extracted, iocs_enriched, mitre_techniques updated, and enrichment results appended to report under `## IOC Enrichment Results`], will you then read fully and follow: `./step-05-scope-impact.md` to begin scope and impact assessment.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All IOCs extracted from steps 1-3 (headers, content, attachments) categorized by type and source step
- IOC inventory presented and confirmed by operator before enrichment begins
- Multiple threat intelligence sources queried per IOC type for cross-referencing
- Per-IOC enrichment tables presented with source, score, and verdict for each category
- Consolidated enrichment summary with statistics (malicious/suspicious/clean/unknown counts)
- MITRE ATT&CK mapping covers both delivery techniques (T1566.*) AND implied post-delivery techniques
- Campaign and threat actor assessment addresses: actor association, malware family, infrastructure patterns, novel indicators
- Clean/unknown IOCs explicitly noted as not necessarily benign
- All URLs remain defanged throughout the enrichment report
- Enrichment results appended to report under `## IOC Enrichment Results`
- Frontmatter updated with iocs_extracted, iocs_enriched, mitre_techniques and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Enriching IOCs not extracted from steps 1-3 (fabricating indicators)
- Relying on a single threat intelligence source without cross-referencing
- Treating "clean" reputation as definitive proof of benign intent
- Treating "unknown" as "clean" — absence of evidence is not evidence of absence
- Mapping only T1566 without considering implied post-delivery techniques from payload analysis
- Skipping any IOC category present in the extraction
- Not defanging URLs in enrichment results
- Beginning scope assessment, containment, or any active response during enrichment
- Not presenting enrichment statistics with malicious/suspicious/clean/unknown breakdown
- Proceeding to scope assessment without completing enrichment for all extracted IOCs
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with IOC counts, ATT&CK techniques, and stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every IOC must be enriched against appropriate sources. Enrichment informs scope assessment — it does not replace analyst judgment.
