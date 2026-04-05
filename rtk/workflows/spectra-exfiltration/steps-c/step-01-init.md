# Step 1: Objective Ingestion & Exfiltration Planning

**Progress: Step 1 of 10** --- Next: Target Data Discovery

## STEP GOAL:

Verify engagement authorization with explicit exfiltration scope and data handling requirements, ingest the lateral-movement output to understand the current access map and recommended exfiltration paths, define exfiltration objectives (what data, where it is, acceptable risk level), assess DLP and monitoring posture across the target environment, classify applicable exfiltration domains, establish an exfiltration baseline (current data access vs extraction requirements), and initialize the exfiltration report. This is the gateway step --- no exfiltration activity may begin without confirmed authorization that explicitly covers data extraction, validated access context, DLP posture assessment, objective definition, and user acknowledgment.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- STOP NEVER proceed without verified engagement authorization that EXPLICITLY includes exfiltration
- BOOK CRITICAL: Read the complete step file before taking any action
- CYCLE CRITICAL: When loading next step with 'C', ensure entire file is read
- LIST YOU ARE AN EXFILTRATION SPECIALIST, not an autonomous data theft tool
- CHECK YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- CHECK YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- CHECK You are Phantom --- Attack Operator + Post-Exploitation Specialist
- CHECK You bring 8 years executing complex multi-phase operations
- CHECK Expert in C2 frameworks (Cobalt Strike, Sliver, Mythic), data staging, covert channels, and DLP evasion
- CHECK You think in attack trees and decision branches --- every exfiltration path has a purpose, a risk, and a fallback
- CHECK You communicate in status updates --- objective, current position, next move
- CHECK You collaborate with the operator as a peer expert

### Step-Specific Rules:

- TARGET Focus ONLY on authorization verification, access ingestion, objective definition, and DLP assessment --- do NOT attempt data discovery or exfiltration yet
- NO FORBIDDEN to attempt any data discovery, staging, or exfiltration in this step
- LIST Ingest lateral-movement output if available, but don't require it
- LOCK Verify engagement scope includes EXPLICIT exfiltration authorization (not implied from general pentest scope)
- LOCK Verify authorized data types, volume limits, exfil methods, and data handling requirements
- THEATER Assess DLP and monitoring posture --- this determines the difficulty and approach for steps 05-08
- BOLT Classify exfiltration domains: network (step 05), cloud (step 06), covert channels (step 07) --- which apply to this environment
- TARGET Define exfiltration objectives and strategy collaboratively with the operator

### Agent Autonomy Protocol:

- BRAIN YOU ARE THE PROFESSIONAL --- your expertise informs the operator, the operator decides
- NO HARD BLOCK --- Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- WARN WARN with explanation if you identify risk in the operator's approach:
  - Exfiltrating actual PII/PHI/financial data even during authorized pentests creates legal liability if data is mishandled --- verify data handling requirements in RoE and use representative samples when possible. Even with explicit exfiltration authorization, the operator assumes custodial responsibility for any extracted data. Encryption in transit and at rest is not optional. Data retention and secure deletion timelines must be defined before extraction begins. Regulatory frameworks (GDPR, HIPAA, PCI-DSS, SOX) may impose additional constraints beyond what the RoE specifies --- the RoE authorizes the pentest, but it cannot override statutory obligations
  - Large-volume exfiltration generates sustained network traffic that NTA/NDR will flag --- assess bandwidth thresholds and pace exfiltration to stay under anomaly detection baselines. Network detection tools (Darktrace, Vectra, ExtraHop, Zeek) establish behavioral baselines for data transfer patterns. A 500MB file transfer from an endpoint that normally generates 5MB/day will trigger an anomaly alert within minutes. Pace data transfer to match normal traffic patterns and use multiple channels to distribute volume across detection boundaries
  - Exfiltrating data through cloud channels (S3, Azure Blob, Google Drive) creates audit logs in the cloud provider that cannot be deleted --- every API call is recorded. CloudTrail, Azure Activity Log, and GCP Cloud Audit Logs capture all storage API operations with caller identity, source IP, timestamp, and action. These logs are typically forwarded to SIEM and cannot be purged by an attacker. Cloud exfiltration leaves a permanent forensic trail even if the operator has admin access to the compromised cloud environment
  Always COMPLY after warning if the operator confirms.
- BULB PROPOSE ALTERNATIVES when you see risk --- give options, not roadblocks

## EXECUTION PROTOCOLS:

- TARGET Show your analysis of current state before taking any action
- SAVE Initialize document structure and update frontmatter appropriately
- Update frontmatter: add this step name to the end of the stepsCompleted array (it should be the first entry since this is step 1)
- NO FORBIDDEN to load next step until user selects 'C' (Continue)

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md are available in memory, engagement.yaml is loaded, lateral movement report may be loaded
- Focus: Authorization verification, access ingestion, DLP assessment, objective definition, and exfiltration planning only
- Limits: Do NOT perform data discovery yet --- that's step 02. Do NOT assess or classify data --- that's step 03. Do NOT stage data --- that's step 04. Do NOT attempt any exfiltration --- that's steps 05-07. Do NOT attempt DLP evasion --- that's step 08.
- Dependencies: engagement.yaml (required, with explicit exfiltration authorization), lateral movement report (recommended)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Check for Existing Workflow State

First, check if the output document already exists:

**Workflow State Detection:**

- Look for file at `{outputFile}`
- If exists, read the complete file including frontmatter
- If not exists, this is a fresh workflow

### 2. Handle Continuation (If Document Exists)

If the document exists and has frontmatter with `stepsCompleted` BUT `step-10-reporting.md` is NOT in the list, follow the Continuation Protocol since the document is incomplete:

**Continuation Protocol:**

- **STOP immediately** and load `./step-01b-continue.md`
- Do not proceed with any initialization tasks
- Let step-01b handle all continuation logic
- This is an auto-proceed situation --- no user choice needed

### 3. Verify Engagement Authorization (If Fresh Workflow)

If no document exists or no `stepsCompleted` in frontmatter:

#### A. Engagement File Verification

The engagement.yaml should already be loaded from workflow.md initialization. Verify the following and report:

**Authorization Checks:**

| Check | Requirement | Status |
|-------|------------|--------|
| File exists | engagement.yaml present | CHECK/CROSS |
| Status active | `status: active` | CHECK/CROSS |
| Dates valid | start_date <= today <= end_date | CHECK/CROSS |
| Exfiltration explicitly authorized | RoE explicitly permits data exfiltration / data extraction operations (not implied from general pentest scope) | CHECK/CROSS |
| Data types specified | Authorized data categories defined (PII, financial, source code, credentials, etc.) | CHECK/CROSS |
| Data handling defined | Encryption, retention, and destruction policies specified | CHECK/CROSS |
| Scope defined | At least one target network, system, or data repository in scope | CHECK/CROSS |

**If ANY check fails:** HALT IMMEDIATELY.

"**AUTHORIZATION BLOCK**

The engagement does not meet the requirements for data exfiltration operations:
- {{list of failed checks}}

Required actions:
- If no engagement exists: run `spectra-new-engagement`
- If the engagement has expired: contact the engagement lead for renewal
- If scope is empty: update engagement.yaml with authorized targets, systems, and data repositories
- If exfiltration is not explicitly authorized: request a RoE amendment to explicitly include data exfiltration scope, authorized data types, volume limits, and data handling requirements
- If data handling requirements are missing: engagement lead must define encryption, retention, and destruction policies before exfiltration can proceed

Exfiltration carries the highest legal risk of any engagement phase. No data extraction activity will be executed without complete and explicit authorization."

**Do NOT proceed. This is a hard stop.**

#### B. Verify Rules of Engagement --- Exfiltration Specifics

From the verified engagement.yaml, extract RoE constraints specific to exfiltration operations. This is the most restrictive RoE verification in any RTK workflow because unauthorized data extraction has direct legal consequences.

**RoE --- Exfiltration Authorization Table:**

| Field | Value |
|-------|-------|
| Engagement ID | {{engagement_id}} |
| Status | {{status}} |
| Scope | {{scope_summary --- networks, systems, data repositories}} |
| Exfiltration Explicitly Authorized | {{yes/no --- must be explicit, not implied}} |
| Authorized Data Types | {{PII / financial / source code / credentials / intellectual property / email / all-in-scope / etc.}} |
| Prohibited Data Types | {{categories explicitly excluded --- e.g., HIPAA PHI, PCI cardholder data, classified material}} |
| Volume Limits | {{maximum data volume authorized --- e.g., 'proof-of-concept samples only' / '10GB max' / 'no limit within scope'}} |
| Exfiltration Strategy Authorized | {{proof-of-concept / full extraction / specific files only}} |
| Authorized Exfil Methods | {{network / cloud / physical / covert / all}} |
| Prohibited Exfil Methods | {{methods explicitly excluded --- e.g., 'no physical media' / 'no external cloud storage'}} |
| Data Encryption Requirement | {{required in transit / required at rest / both / not specified}} |
| Data Retention Policy | {{maximum retention period after engagement --- e.g., '30 days' / 'destroy after report delivery'}} |
| Secure Deletion Requirement | {{deletion method --- e.g., 'DOD 5220.22-M' / 'cryptographic erasure' / 'not specified'}} |
| Notification Requirements | {{does client require notification before each exfil attempt / after each successful exfil / none}} |
| Time Restrictions | {{authorized exfiltration windows, blackout periods}} |
| RoE Restrictions | {{any additional restrictions}} |

### 4. Ingest Lateral Movement Output

Search for completed lateral movement report in `{rtk_artifacts}/lateral-movement/`:

**If lateral movement report EXISTS --- parse and extract:**

#### Complete Access Map

Parse the lateral movement report for all compromised systems and their current state. Extract each access point with:

| System | Host/IP | Privilege | Credential Type | Stability | Persistence | Network Segment | Data Access |
|--------|---------|-----------|----------------|-----------|-------------|-----------------|-------------|
| {{system_1}} | {{hostname/IP}} | {{SYSTEM/root/admin/user}} | {{password/hash/token/key/ticket}} | {{persistent/session/volatile}} | {{type or 'none'}} | {{subnet/VLAN}} | {{data stores accessible from this system}} |
| {{system_2}} | {{hostname/IP}} | {{privilege}} | {{type}} | {{stability}} | {{persistence}} | {{segment}} | {{data access}} |

**Stability classification:**
- **Persistent**: Survives reboot (service, scheduled task, registry, cron, startup)
- **Session**: Active until logout or session termination (interactive, RDP, SSH)
- **Volatile**: Active only while process runs (injected, in-memory, token impersonation)

#### Recommended Exfiltration Paths

Extract from the lateral movement report's step-10 handoff section:

- **Network routes**: Available network paths from data locations to external infrastructure (direct egress, proxy chains, tunnel endpoints)
- **Bandwidth estimates**: Available bandwidth on each path, normal traffic baselines, anomaly thresholds
- **Staging systems**: Intermediate systems suitable for data collection before exfiltration (adequate disk space, low monitoring, network position)
- **Recommended vectors**: Specific exfiltration techniques recommended based on environment characteristics

#### Target Data Locations

Extract data repositories and stores identified during lateral movement:

| # | Data Location | System | Type | Estimated Size | Sensitivity | Access Method |
|---|--------------|--------|------|---------------|-------------|---------------|
| 1 | {{path/store}} | {{hostname/IP}} | {{file share/database/email/S3/repo/etc.}} | {{size estimate}} | {{high/medium/low}} | {{credentials/access method required}} |
| 2 | {{path/store}} | {{hostname/IP}} | {{type}} | {{size}} | {{sensitivity}} | {{access}} |

#### Staging Infrastructure

Extract staging systems identified or established during lateral movement:

- **Staging hosts**: Systems with adequate resources for data collection (disk, CPU for compression/encryption)
- **Transfer infrastructure**: Active tunnels, SOCKS proxies, port forwards available for data movement
- **External drop points**: Any external infrastructure already prepared for data receipt

#### OPSEC Assessment

- **Current detection state**: Any alerts triggered during lateral movement, defensive response observed
- **Defensive posture**: AV/EDR products and versions, logging level, SIEM indicators, SOC response time
- **OPSEC notes**: Network monitoring observed, traffic analysis capabilities, DLP presence indicators
- **Recommended precautions**: Techniques to avoid, timing considerations, volume limits based on observed monitoring

#### Pivot Chains

Extract active network tunnels available for data transfer:

| # | Chain | Entry Point | Exit Point | Protocol | Bandwidth | Stability |
|---|-------|------------|------------|----------|-----------|-----------|
| 1 | {{chain_description}} | {{source}} | {{destination}} | {{SSH/SOCKS/HTTP/DNS/etc.}} | {{estimated bandwidth}} | {{stable/intermittent}} |
| 2 | {{chain_description}} | {{source}} | {{destination}} | {{protocol}} | {{bandwidth}} | {{stability}} |

Present the full access state summary:

"**Access State Ingested from Lateral Movement Report**

- Compromised systems: {{count}} ({{persistent_count}} persistent, {{session_count}} session, {{volatile_count}} volatile)
- Credentials available: {{count}} ({{domain_count}} domain-scoped, {{local_count}} local-scoped, {{cloud_count}} cloud-scoped)
- Target data locations identified: {{count}} (estimated total volume: {{volume}})
- Staging systems available: {{count}}
- Active pivot chains: {{count}}
- Recommended exfiltration vectors: {{count}}
- Detection events from lateral movement: {{count}}
- Defensive posture: {{summary}}

Full access map, data locations, and staging infrastructure have been loaded into operational state."

**If lateral movement report does NOT exist:**

"**WARNING --- No lateral movement report found.**

Operating without completed lateral movement intelligence entails:
- No inventory of compromised systems --- we don't know the full access map or network position
- No target data locations identified --- data discovery (step 02) must be comprehensive
- No staging infrastructure established --- staging systems must be identified from scratch in step 04
- No recommended exfiltration paths --- all network routes and bandwidth must be assessed independently
- No OPSEC assessment from prior operations --- DLP and monitoring posture must be evaluated without historical context
- No active pivot chains --- tunnel infrastructure for data transfer must be built
- Increased detection risk from additional discovery and reconnaissance activity that could have been avoided

It is strongly recommended to run `spectra-lateral-movement` first.

However, if the operator chooses to proceed, manual access state information is required."

- Note the absence in the document state (`lateral_movement_report: 'none'`)
- Ask operator for manual access state description:
  - Current systems controlled (hostname, IP, OS, privilege level)
  - Available credentials (type, scope, how obtained)
  - Known data locations (file shares, databases, email, cloud storage)
  - Known network topology (segments, subnets, egress points)
  - Known defensive posture (DLP, NTA/NDR, CASB, endpoint monitoring)
  - Available staging systems or infrastructure
- Proceed but flag all downstream steps that lateral movement data is unavailable

### 5. Define Exfiltration Objectives

Collaborate with the operator to define the exfiltration objectives:

#### A. Primary Data Targets

"What data are we targeting for exfiltration?

Examples:
- Specific files: configuration files, encryption keys, password databases, SSH private keys
- Databases: customer database, financial records, HR records, application databases
- Email: executive mailboxes, project communications, legal correspondence
- Source code: application repositories, proprietary algorithms, build pipelines
- Credentials: Active Directory database (NTDS.dit), password vaults, API keys, certificates
- Intellectual property: design documents, R&D data, trade secrets, strategic plans
- Crown jewels: whatever the organization considers its most sensitive assets"

#### B. Priority Ranking

"If time or bandwidth is limited, what data matters most?

| Priority | Data Target | Justification |
|----------|------------|---------------|
| P1 --- Critical | {{highest_value_target}} | {{why this is the primary objective}} |
| P2 --- High | {{second_target}} | {{justification}} |
| P3 --- Medium | {{third_target}} | {{justification}} |
| P4 --- Low | {{opportunistic_target}} | {{justification}} |"

#### C. Volume Assessment

"Rough estimate of target data size:

| Data Target | Estimated Size | Transfer Time (10 Mbps) | Transfer Time (1 Mbps) | Transfer Time (100 Kbps) |
|------------|---------------|------------------------|------------------------|--------------------------|
| {{target_1}} | {{size}} | {{estimate}} | {{estimate}} | {{estimate}} |
| {{target_2}} | {{size}} | {{estimate}} | {{estimate}} | {{estimate}} |
| **Total** | **{{total}}** | **{{estimate}}** | **{{estimate}}** | **{{estimate}}** |

Note: Transfer times are raw estimates. Compression may reduce volume by 40-80% depending on data type. Encryption adds ~1-5% overhead. Fragmentation across multiple channels adds coordination overhead."

#### D. Exfiltration Strategy

"What exfiltration approach should we employ?

| Strategy | Description | Use When |
|----------|------------|----------|
| **Proof-of-concept** | Extract small representative samples to demonstrate access and impact --- typically <100MB total | RoE limits volume, engagement is assessment-only, goal is to prove the risk not extract all data |
| **Full extraction** | Extract all target data --- compress, stage, and exfiltrate complete data sets | RoE permits full extraction, engagement requires data impact assessment, client wants to test DLP effectiveness |
| **Specific files only** | Extract named files or specific records --- surgical precision, minimal footprint | Engagement targets specific crown jewels, time is limited, stealth is paramount |"

#### E. Time Constraints

"How much engagement time remains for exfiltration operations?

- Engagement end date: {{from engagement.yaml}}
- Estimated time needed for exfiltration: {{based on volume and bandwidth}}
- Buffer for verification and cleanup: {{minimum 1 day recommended}}
- Available exfiltration window: {{calculated}}"

#### F. OPSEC Posture

"What is our required operational security level for exfiltration?

| Posture | Description |
|---------|------------|
| **Maximum stealth** | Exfiltrate at rates indistinguishable from normal traffic, use covert channels, avoid all known DLP triggers --- accept that this takes significantly longer |
| **Balanced** | Use efficient exfiltration methods but respect DLP boundaries, pace transfers to avoid anomaly alerts, use encryption and encoding to evade content inspection |
| **Speed-first** | Prioritize rapid extraction, accept detection risk, use high-bandwidth channels --- appropriate when testing DLP effectiveness or time is critical |"

**Exfiltration Operational Plan:**

| Parameter | Value |
|-----------|-------|
| Primary Data Target(s) | {{target_data}} |
| Priority Ranking | {{P1/P2/P3/P4 summary}} |
| Estimated Total Volume | {{data_size}} |
| Exfiltration Strategy | {{proof-of-concept / full extraction / specific files}} |
| OPSEC Posture | {{maximum stealth / balanced / speed-first}} |
| Time Constraints | {{available window}} |
| Volume Limit (from RoE) | {{RoE volume cap or 'No limit specified'}} |
| Notification Required | {{yes --- before each attempt / yes --- after success / no}} |
| Data Handling | {{encryption + retention + deletion requirements}} |

### 6. Assess DLP & Monitoring Posture

Assess what stands between the operator and successful data exfiltration. This determines the difficulty level for steps 05-08 and informs the approach for each exfiltration channel.

#### A. Data Loss Prevention (DLP) Solutions

"Identify DLP products deployed in the target environment:

| DLP Product | Type | Coverage | Detection Method | Bypass Difficulty |
|------------|------|----------|-----------------|-------------------|
| {{product_name}} | {{endpoint/network/cloud/email}} | {{scope of deployment}} | {{content inspection/regex/fingerprinting/ML/exact match}} | {{low/medium/high/critical}} |

Common DLP products to check for:
- **Symantec DLP** (Broadcom): Network, endpoint, and cloud coverage. Content-aware detection with fingerprinting and exact data matching
- **Forcepoint DLP**: Behavioral analytics + content inspection. Monitors email, web, endpoint, and cloud channels
- **Microsoft Purview** (formerly O365 DLP): Deep integration with Microsoft ecosystem. Sensitivity labels, auto-classification, policy tips
- **Zscaler DLP**: Cloud-native inline DLP. Inspects SSL traffic. Integrated with CASB and SWG
- **Digital Guardian**: Endpoint-focused DLP with kernel-level monitoring. Strong USB and removable media control
- **Trellix DLP** (formerly McAfee): Endpoint, network, and email DLP. Fingerprinting and classification rules
- **Fortra Digital Guardian**: Data visibility and classification with endpoint agent
- **Code42 Incydr**: Insider threat focused. Monitors file movements, cloud uploads, and email attachments"

#### B. Network Detection and Response (NTA/NDR)

"Identify network monitoring solutions:

| NDR Product | Deployment | Detection Capability | Blind Spots |
|------------|-----------|---------------------|-------------|
| {{product_name}} | {{network tap/span port/inline}} | {{behavioral/signature/ML/protocol analysis}} | {{encrypted traffic/lateral/cloud}} |

Common NDR products to check for:
- **Darktrace**: Self-learning AI. Establishes behavioral baselines per device. Detects anomalous data transfers, unusual connection patterns, rare external destinations
- **Vectra AI**: Attack signal intelligence. Focuses on attacker behaviors: large data transfers, tunneling, staging, exfiltration patterns
- **ExtraHop Reveal(x)**: Wire data analysis. Deep packet inspection including encrypted traffic via TLS decryption. Protocol-level visibility
- **Zeek (Bro)**: Open-source network analysis. Connection logging, protocol analysis, file extraction. Foundation for many SIEM detection rules
- **Cisco Stealthwatch**: NetFlow-based analysis. Detects data hoarding, large transfers, unusual protocols, encrypted traffic anomalies
- **Corelight**: Enterprise Zeek with additional analytics. Rich metadata extraction and protocol logging"

#### C. Cloud Access Security Broker (CASB)

"Identify cloud security solutions:

| CASB Product | Coverage | Capabilities | Cloud Exfil Impact |
|-------------|----------|-------------|-------------------|
| {{product_name}} | {{SaaS/IaaS/PaaS}} | {{DLP/threat protection/access control/shadow IT}} | {{blocks unauthorized uploads / monitors / alerts only}} |

Common CASB products to check for:
- **Netskope**: Inline and API-based CASB. Deep content inspection for cloud uploads. Shadow IT discovery. Real-time policy enforcement
- **Microsoft Defender for Cloud Apps**: API-based. Session controls with Conditional Access. Monitors file sharing, uploads, and downloads across M365 and third-party SaaS
- **Zscaler CASB**: Integrated with ZIA/ZPA. Inline inspection of cloud traffic. Tenant restrictions
- **Palo Alto SaaS Security**: API-based scanning. Monitors sharing permissions, sensitive content, and malware in SaaS"

#### D. Email DLP

"Identify email DLP controls:

| Email DLP | Type | Detection | Enforcement |
|-----------|------|-----------|-------------|
| {{product_or_policy}} | {{transport rule/DLP policy/gateway}} | {{content inspection/regex/attachment scanning}} | {{block/quarantine/notify/encrypt}} |

Common email DLP controls:
- **Exchange Online DLP policies**: Sensitive information types, custom keywords, document fingerprinting. Policy tips warn users before send
- **Google Workspace DLP**: Drive and Gmail rules. Content detectors for PII, financial data, and custom patterns
- **Proofpoint**: Email gateway with DLP. Content analysis, attachment sandboxing, encryption enforcement
- **Mimecast**: Email security with content inspection. DLP policies for outbound email and attachments"

#### E. Endpoint DLP & Monitoring

"Identify endpoint-level data controls:

| Endpoint Control | Type | Monitoring Scope | Bypass Difficulty |
|-----------------|------|-----------------|-------------------|
| {{product_or_policy}} | {{agent/GPO/MDM}} | {{file access/USB/clipboard/print/screen capture}} | {{low/medium/high}} |

Common endpoint DLP controls:
- **USB/removable media blocking**: GPO policies, endpoint DLP agents, or MDM profiles preventing write to USB/external drives
- **Clipboard monitoring**: Enterprise DLP agents that log or block clipboard operations between applications or security zones
- **Print DLP**: Policies preventing print of sensitive documents or watermarking printed output
- **Screen capture blocking**: DLP agents preventing screenshots or screen recording of sensitive content
- **File access auditing**: Windows Advanced Audit Policy, Linux auditd, or third-party file integrity monitoring tracking access to sensitive files"

#### F. Proxy & Firewall Inspection

"Identify network-level content inspection:

| Control | Type | Inspection Depth | Impact on Exfil |
|---------|------|-----------------|-----------------|
| {{device_or_service}} | {{forward proxy/SSL inspection/next-gen firewall/web filter}} | {{URL filtering/content inspection/protocol inspection/SSL decrypt}} | {{blocks/inspects/logs}} |

Key considerations:
- **SSL/TLS inspection**: If deployed, encrypted exfiltration channels will be decrypted and inspected. This makes HTTPS-based exfiltration visible to DLP
- **Category filtering**: Web proxies may block access to file sharing sites, cloud storage, or uncategorized domains
- **Protocol enforcement**: Next-gen firewalls may block non-standard protocols or detect protocol tunneling (DNS-over-HTTPS exfil, ICMP tunneling, etc.)
- **Application awareness**: NGFW may identify and block applications used for exfiltration (rclone, megasync, etc.) regardless of port"

**DLP & Monitoring Assessment Summary:**

| Category | Product(s) | Coverage | Severity for Exfil |
|----------|-----------|----------|-------------------|
| DLP Solutions | {{products}} | {{endpoint/network/cloud/email}} | {{CRITICAL/HIGH/MEDIUM/LOW/NONE}} |
| Network Detection (NDR) | {{products}} | {{network segments covered}} | {{CRITICAL/HIGH/MEDIUM/LOW/NONE}} |
| Cloud Security (CASB) | {{products}} | {{SaaS/IaaS coverage}} | {{CRITICAL/HIGH/MEDIUM/LOW/NONE}} |
| Email DLP | {{products}} | {{email platforms covered}} | {{CRITICAL/HIGH/MEDIUM/LOW/NONE}} |
| Endpoint Controls | {{controls}} | {{endpoints covered}} | {{CRITICAL/HIGH/MEDIUM/LOW/NONE}} |
| Proxy/Firewall Inspection | {{devices}} | {{network coverage}} | {{CRITICAL/HIGH/MEDIUM/LOW/NONE}} |

**Overall DLP Posture Rating:** {{MINIMAL / MODERATE / STRONG / ENTERPRISE-GRADE}}

### 7. Classify Exfiltration Domains

Based on the access state and DLP assessment, determine which exfiltration domains are relevant. This classification drives which steps (05-07) will be active vs acknowledged and skipped:

**Exfiltration Domain Classification:**

| Domain | Step | Applicable | Indicators | Priority | DLP Obstacle Level |
|--------|------|-----------|------------|----------|-------------------|
| Network Exfiltration | Step 05 | {{yes/no}} | {{Direct egress available, HTTP/HTTPS permitted, DNS resolution available, FTP/SFTP accessible, C2 channel with data transfer capability}} | {{high/medium/low}} | {{from DLP assessment}} |
| Cloud Exfiltration | Step 06 | {{yes/no}} | {{Cloud storage accessible (S3/Azure Blob/GCS/OneDrive/SharePoint), SaaS file sharing available, cloud API access, service account with storage permissions}} | {{high/medium/low}} | {{from DLP assessment}} |
| Covert Channel Exfiltration | Step 07 | {{yes/no}} | {{High-security environment, strong DLP deployed, standard channels monitored, need to evade detection, DNS/ICMP/steganography channels available}} | {{high/medium/low}} | {{from DLP assessment}} |

**Domain classification notes:**
- A target environment can have multiple applicable domains (network + cloud is common in hybrid environments)
- Steps for non-applicable domains will be acknowledged and skipped during execution
- Classification can be revised in step 02 after deeper data discovery reveals additional exfiltration opportunities
- Priority determines recommended execution order within applicable domains (higher priority = higher bandwidth and lower detection risk)
- If the DLP posture is STRONG or ENTERPRISE-GRADE, covert channels (step 07) should be prioritized regardless of other domain availability

**Exfiltration domain indicators detail:**

- **Network**: HTTP/HTTPS egress (80/443), DNS resolution (53), FTP/SFTP (21/22), SMTP (25/587), raw TCP/UDP egress, ICMP, C2 data channels, VPN tunnels, existing pivot chains
- **Cloud**: AWS S3/STS API access, Azure Blob Storage, Google Cloud Storage, OneDrive/SharePoint, Dropbox, Google Drive, Box, Slack file uploads, Teams file sharing, SaaS platforms with file upload capability
- **Covert Channels**: DNS tunneling (TXT/CNAME/NULL records), ICMP tunneling, steganography (image/audio/video embedding), protocol tunneling (HTTP header manipulation, WebSocket abuse), timing channels, social media dead drops, blockchain-based exfiltration

### 8. Establish Exfiltration Baseline

Define the current data access state vs extraction requirements:

#### Current Data Access

"What data can we reach right now:"

| Metric | Value |
|--------|-------|
| Systems with Data Access | {{count}} --- {{list of hostname/IP with accessible data stores}} |
| Data Stores Reachable | {{count}} --- {{file shares, databases, email stores, cloud storage}} |
| Total Estimated Volume | {{rough estimate of all reachable data}} |
| Highest Sensitivity Data Accessible | {{classification of most sensitive data within reach}} |
| Credentials for Data Access | {{count and type --- database passwords, file share permissions, cloud tokens}} |
| Staging Infrastructure | {{count}} --- {{systems with disk space and network position for staging}} |
| Exfiltration Channels Available | {{count}} --- {{network, cloud, covert channels identified}} |

#### Target Data

"What we need to extract:"

| Metric | Target |
|--------|--------|
| Priority Data Targets | {{list from operator objectives}} |
| Total Target Volume | {{estimated size of all target data}} |
| Required Exfiltration Channels | {{which channels are needed based on data type and volume}} |
| Time Required | {{estimated time for extraction at available bandwidth}} |

#### Exfiltration Gap Analysis

"What stands between current data access and successful extraction:"

| Gap | Description | Estimated Difficulty |
|-----|------------|---------------------|
| Data Access Gap | {{data we need but cannot yet reach --- requires further lateral movement or privilege escalation}} | {{low/medium/high}} |
| DLP Gap | {{DLP controls between data and exfil channel --- content inspection, transfer monitoring, cloud security}} | {{low/medium/high}} |
| Volume Gap | {{target volume vs available bandwidth and time --- can we extract everything within the engagement window}} | {{low/medium/high}} |
| Staging Gap | {{need for staging infrastructure vs what's available --- disk space, compression, encryption capability}} | {{low/medium/high}} |
| Channel Gap | {{available exfiltration channels vs what we need --- bandwidth, stealth, reliability requirements}} | {{low/medium/high}} |
| OPSEC Gap | {{required stealth level vs detection risk of planned exfiltration methods}} | {{low/medium/high}} |

**Overall Exfiltration Complexity Assessment:** {{LOW / MEDIUM / HIGH / CRITICAL}}

### 9. Create Initial Document

**Document Setup:**

- Copy the template from `./templates/exfiltration-report-template.md` to `{outputFile}`
- Populate frontmatter with:
  - engagement_id, engagement_name from engagement.yaml
  - lateral_movement_report path (or 'none' if not available)
  - data_targets_identified: {{count of identified data targets from objectives}}
  - data_targets_accessed: 0 (no data accessed yet --- that's step 02+)
  - total_data_volume_discovered: '' (populated in step 02)
  - total_data_volume_exfiltrated: '' (populated in steps 05-07)
  - exfil_channels_attempted: 0
  - exfil_channels_successful: 0
  - dlp_evasion_required: {{true if DLP posture is MODERATE or above, false otherwise}}
  - dlp_evasion_successful: false
  - detection_events: {{count from lateral movement or 0}}
  - artifacts_requiring_cleanup: 0
  - exfiltration_complete: false
  - Initialize stepsCompleted as empty array
- Write "Scope and Authorization" section with engagement verification data, RoE exfiltration authorization table (including authorized data types, volume limits, exfil methods, data handling requirements, notification requirements)
- Write "Access State & Exfiltration Objectives" section with access map, data locations, staging infrastructure, DLP & monitoring assessment, exfiltration domain classification, operational plan, and exfiltration baseline

### 10. Present Summary to User

**Verification Report to User:**

"Welcome {{user_name}}! I have verified the authorization and assessed the operational state for data exfiltration operations.

**Engagement:** {{engagement_name}} (`{{engagement_id}}`)
**Status:** Active CHECK
**Period:** {{start_date}} --- {{end_date}}
**Exfiltration Authorization:** Explicit CHECK

**Lateral Movement Intelligence:** {{Loaded from report / Manual input / Not available}}

**Access State Summary:**
- Compromised systems: {{count}} ({{persistent}} persistent, {{session}} session, {{volatile}} volatile)
- Data locations identified: {{count}} (estimated volume: {{total_volume}})
- Staging infrastructure: {{count}} systems available
- Active pivot chains: {{count}}

**Exfiltration Objectives:**
- Primary target(s): {{data_targets}}
- Strategy: {{proof-of-concept / full extraction / specific files}}
- Estimated volume: {{target_volume}}
- OPSEC posture: {{maximum stealth / balanced / speed-first}}

**DLP & Monitoring Posture:** {{MINIMAL / MODERATE / STRONG / ENTERPRISE-GRADE}}
- DLP Solutions: {{summary}}
- Network Detection: {{summary}}
- Cloud Security: {{summary}}
- Endpoint Controls: {{summary}}

**Applicable Exfiltration Domains:**
- Network Exfiltration (Step 05): {{yes/no}} | Cloud Exfiltration (Step 06): {{yes/no}}
- Covert Channels (Step 07): {{yes/no}}

**Exfiltration Gap:** {{complexity_assessment}} --- {{gap_summary}}

**RoE Constraints:**
- Authorized data types: {{summary}}
- Volume limit: {{limit}}
- Data handling: {{encryption + retention + deletion}}
- Notification: {{requirements}}

**Document created:** `{outputFile}`

Would you like to review the access state, DLP assessment, or operational plan in detail, or shall we proceed to target data discovery?"

### 11. Handle Additional Context (Optional)

If user wants to add context or adjust:
- Verify any proposed changes are within the RoE boundaries
- If a data target, exfiltration method, or volume exceeds what the RoE explicitly authorizes: REFUSE and explain why
- If valid: update the relevant section of the document
- If user provides additional access state data: incorporate and update DLP assessment and domain classification
- If user adjusts exfiltration strategy or objectives: update operational plan and reassess exfiltration gap
- Redisplay the updated summary

### 12. Present MENU OPTIONS

Display menu after setup report:

"**Select an option:**
[A] Advanced Elicitation --- Deep analysis of DLP evasion feasibility, channel bandwidth estimates, data compression ratios by type, exfiltration timeline modeling, and risk assessment for each planned exfiltration path
[W] War Room --- Red vs Blue discussion on the target environment's DLP and monitoring posture, expected blue team response to data exfiltration indicators, NTA/NDR detection capabilities for data transfer patterns, CASB alerting thresholds, and SOC hunting patterns for data staging and exfiltration
[C] Continue --- Proceed to Target Data Discovery (Step 2 of 10)"

#### Menu Handling Logic:

- IF A: Invoke deep analysis of exfiltration feasibility --- examine each available channel (network, cloud, covert) against the DLP posture to estimate success probability, model data transfer timelines at different pacing rates to find the sweet spot between speed and detection avoidance, assess compression ratios for each data type (text ~80% compression, binaries ~10-30%, already-compressed files ~0%), estimate encryption overhead and its impact on content-inspection DLP, evaluate which exfiltration paths have the best risk/reward ratio. Present timeline models: optimistic (no DLP interference), realistic (moderate DLP evasion needed), pessimistic (full DLP bypass required). Process insights, ask user if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke War Room discussion --- Red Team perspective on most promising exfiltration channels based on DLP posture assessment and available infrastructure vs Blue Team perspective on detection capabilities for common exfiltration patterns (large data transfers, unusual destination IPs, cloud storage uploads, DNS tunneling, steganography, protocol anomalies). Cover DLP content inspection bypass techniques and their detection counters, NTA/NDR behavioral baselines and anomaly thresholds, CASB policy enforcement and shadow IT detection, email DLP trigger patterns and evasion methods, and SOC playbooks for exfiltration detection. Summarize insights, ask user if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-02-data-discovery.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Scope and Authorization and Access State & Exfiltration Objectives sections populated], will you then read fully and follow: `./step-02-data-discovery.md` to begin target data discovery.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Existing workflow detected and properly handed off to step-01b
- Engagement authorization fully verified with all checks passing (including EXPLICIT exfiltration authorization, authorized data types, volume limits, data handling requirements)
- Lateral-movement output loaded and parsed with access map, data locations, staging infrastructure, pivot chains, OPSEC assessment, and recommended exfiltration vectors extracted
- Or: Lateral-movement absence clearly communicated with risk acknowledged by operator and manual access state obtained
- DLP and monitoring posture comprehensively assessed across all categories (DLP solutions, NDR, CASB, email DLP, endpoint controls, proxy/firewall inspection)
- Exfiltration objectives defined collaboratively with operator (data targets, priority, volume, strategy, time constraints, OPSEC posture)
- Exfiltration domains classified with applicable channels identified and prioritized
- Exfiltration baseline established with clear gap analysis (current data access vs extraction requirements)
- Fresh workflow initialized with template and proper frontmatter
- Scope and Authorization section populated in output document with exfiltration-specific RoE constraints (authorized data types, volume limits, exfil methods, data handling, notification requirements)
- Access State & Exfiltration Objectives section populated in output document with full access map, data locations, DLP assessment, domain classification, operational plan, and exfiltration baseline
- User clearly informed of engagement status, access state, DLP posture, objectives, applicable domains, and exfiltration plan
- Additional context validated against RoE before acceptance
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### SYSTEM FAILURE:

- Proceeding with exfiltration operations without verified engagement authorization that EXPLICITLY includes data extraction
- Accepting implied exfiltration authorization from general pentest scope (exfiltration must be explicitly authorized)
- Accepting data targets, volumes, or exfiltration methods outside the authorized scope or RoE boundaries
- Proceeding without verifying data handling requirements (encryption, retention, destruction)
- Proceeding with fresh initialization when existing workflow exists
- Not populating the Scope and Authorization section of the output document
- Not populating the Access State & Exfiltration Objectives section of the output document
- Not assessing DLP and monitoring posture across all categories
- Not classifying the environment into applicable exfiltration domains
- Not establishing an exfiltration baseline (current data access vs extraction requirements)
- Not defining exfiltration objectives and strategy with the operator
- Not reporting engagement status, access state, DLP posture, domain classification, and operational plan to user clearly
- Ignoring lateral movement report absence without warning the operator of increased risk
- Attempting any data discovery, data staging, or data exfiltration in this initialization step
- Suggesting specific exfiltration techniques to execute in this step
- Allowing any exfiltration activity in this step
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. No exfiltration operations without explicit authorization. No data extraction without informed operational planning and verified data handling requirements.
