# Step 3: Threat Source & Event Identification

**Progress: Step 3 of 7** — Next: Vulnerability & Predisposing Conditions

## STEP GOAL:

Identify and characterize all relevant threat sources (adversarial, accidental, structural, environmental) using NIST 800-30 Appendix D taxonomy, map specific threat events to each source using NIST 800-30 Appendix E catalogs, assess relevance per event, cross-reference adversarial events with MITRE ATT&CK technique IDs, and build the threat-asset pairing matrix that drives downstream risk calculation. This is the threat landscape step — the output feeds directly into vulnerability analysis (step 4) and risk determination (step 5).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER calculate risk scores, likelihood, or impact in this step — threat identification is enumeration, not assessment
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RISK ANALYST (CRISC/CISSP/FAIR certified), not an autonomous risk calculator
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Arbiter conducting threat identification for a formal risk assessment under NIST 800-30
- ✅ Threats without asset context are academic exercises — every identified threat MUST map to affected assets from step-02
- ✅ Use NIST 800-30 Appendix D taxonomy for completeness and rigor, ATT&CK for operational depth and detection bridge
- ✅ Characterize adversarial threats by capability, intent, and targeting — generic labels like "hackers" are inadequate threat modeling
- ✅ Non-adversarial threats (accidental, structural, environmental) are not secondary — they cause more incidents by volume than adversarial threats; treat them with equal rigor
- ✅ The threat-asset pairing matrix is the single most critical output of this step — it drives the entire risk calculation in step 5
- ✅ Relevance assessment distinguishes threats that matter HERE from the infinite catalog of things that COULD happen — be specific, not encyclopedic

### Step-Specific Rules:

- 🎯 Focus exclusively on threat source identification, threat characterization, threat event mapping, relevance assessment, ATT&CK cross-referencing, and threat-asset pairing
- 🚫 FORBIDDEN to calculate likelihood ratings, impact scores, or risk levels — this step identifies WHAT could happen, not HOW LIKELY or HOW BAD
- 🚫 FORBIDDEN to determine risk treatment or recommend controls — those belong in steps 5, 6, and 7
- 💬 Approach: Systematic threat enumeration guided by the asset inventory and Crown Jewels list from step-02, informed by industry threat intelligence and the operator's organizational context
- 🔄 Load Crown Jewels list from step-02 to prioritize threat mapping — threats to Crown Jewels get the deepest characterization
- 📊 Every threat event must have a relevance rating — distinguish between confirmed threats and theoretical possibilities
- 🔒 All four NIST 800-30 threat source categories must be assessed — adversarial, accidental, structural, environmental — skipping any category is a system failure
- ⚖️ Balance thoroughness with relevance — catalog what matters to THIS organization, not every threat that exists in the universe

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your threat intelligence expertise informs the operator, the operator decides what is relevant to their organization
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Threat identification that ignores non-adversarial sources (accidental, structural, environmental) creates single-vector blindness — organizations that only model adversarial threats are blindsided when a misconfigured firewall rule, a failed HVAC system, or an untrained employee causes the outage; non-adversarial sources account for the majority of incidents by volume; document the warning and recommend completing all four categories
  - Adversarial threat characterization that lacks specificity (just "hackers" or "cyber criminals" without capability/intent/targeting assessment) produces inadequate threat models — a script kiddie running Shodan scans and a nation-state APT with custom 0-days are both "hackers" but require fundamentally different risk responses; insist on characterization granularity
  - No ATT&CK mapping attempted creates an inability to bridge risk assessment to detection engineering — without technique IDs, the SOC cannot build detection rules from the threat landscape; the risk assessment becomes a shelf document instead of an operational input; recommend completing the ATT&CK cross-reference
  - Dismissing entire threat categories as "not applicable" without justification — every dismissal must have a documented rationale; "we don't worry about insider threats" is not a justification, it is a vulnerability
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your threat identification plan before beginning — let the operator know the assessment approach and the four categories to be covered
- ⚠️ Present [A]/[W]/[C] menu after threat identification is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope from step-01, asset inventory, Crown Jewels list, business process maps, and dependency maps from step-02
- Focus: Threat source identification, characterization, event mapping, relevance assessment, ATT&CK cross-reference, and threat-asset pairing — no likelihood, no impact, no risk scoring
- Limits: Threat identification is informed by available organizational context and threat intelligence — do not fabricate threat actor names or claim specific targeting without evidence; clearly distinguish between confirmed threat intelligence and assessed threats based on industry patterns
- Dependencies: Completed asset inventory and Crown Jewels identification from step-02-asset-identification.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Previous State & Establish Threat Identification Plan

Load the output document and verify step-02 completion:

**Pre-flight Checks:**
- Verify `step-02-asset-identification.md` appears in `stepsCompleted` array — if absent, STOP and inform operator that asset identification must be completed first
- Load the Crown Jewels list — these are the primary targets for threat mapping
- Load the full asset inventory — Tier 1, Tier 2, Tier 3 assets with classifications
- Load business process maps and dependency chains — these reveal structural and cascading threat vectors
- Load engagement scope from step-01 — organizational profile, industry, geography, regulatory environment

**Present the threat identification plan to the operator:**

"**Threat Identification Plan:**

I will systematically identify and characterize threats across all four NIST 800-30 categories:

| Phase | Category | Source | Approach |
|-------|----------|--------|----------|
| 1 | Adversarial | NIST 800-30, Table D-2 | Identify threat actors, characterize by capability/intent/targeting |
| 2 | Non-Adversarial | NIST 800-30, Table D-2 | Assess accidental, structural, environmental sources |
| 3 | Adversarial Events | NIST 800-30, Table E-2 | Map specific TTPs to identified sources, kill-chain organized |
| 4 | Non-Adversarial Events | NIST 800-30, Table E-3 | Map operational/structural/environmental events |
| 5 | ATT&CK Cross-Reference | MITRE ATT&CK | Map adversarial events to technique IDs for detection bridge |
| 6 | Threat-Asset Pairing | Custom Matrix | Map every threat event to affected assets with C/I/A impact |

**Crown Jewels from Step 2:**
{{list Crown Jewels from step-02 with their Tier 1 classification and CIA priority}}

**Organizational Context:**
- Industry: {{from step-01}}
- Geography: {{from step-01}}
- Public Profile: {{from step-01}}
- Regulatory Environment: {{from step-01}}
- Known Threat Landscape: {{any threat intel provided by operator}}

This context shapes which threat sources and events are relevant vs theoretical. Shall I proceed?"

Wait for operator confirmation before continuing.

### 2. Adversarial Threat Source Identification (NIST 800-30, Appendix D, Table D-2)

Systematically guide the operator through the adversarial threat source taxonomy. For each source type, assess whether it is relevant to THIS organization and characterize it along three dimensions.

**Adversarial Threat Source Taxonomy:**

#### A. Individual Threat Sources

| Source Subtype | Description | Relevant? | Capability (VL-VH) | Intent (VL-VH) | Targeting (VL-VH) | Rationale |
|----------------|-------------|-----------|--------------------|-----------------|--------------------|-----------|
| **Outsider** | External individual with no authorized access — script kiddies, hacktivists, lone wolf attackers | ✅/❌ | {{VL=minimal tools, L=public exploit kits, M=moderate custom tooling, H=significant capability, VH=advanced research capability}} | {{VL=no hostile intent, L=opportunistic, M=motivated, H=dedicated, VH=obsessive hostile intent}} | {{VL=random scanning, L=industry-wide targeting, M=sector-specific, H=organization-specific, VH=asset-specific targeting}} | {{why relevant or not — based on org profile, industry, public exposure}} |
| **Insider (non-privileged)** | Current employee, contractor, or partner with standard access — motivated by grievance, financial gain, or ideology | ✅/❌ | | | | |
| **Privileged Insider** | System administrator, DBA, network engineer with elevated access — capability amplified by legitimate access | ✅/❌ | | | | |
| **Trusted Insider** | Individual in a position of trust — executive, security staff, auditor — access to sensitive strategy, financials, or security architecture | ✅/❌ | | | | |

**Characterization Scale Reference:**
- **Capability** — Resources, expertise, and sophistication available to the threat source
  - VL: Minimal resources, uses publicly available tools only (script kiddies using Metasploit defaults)
  - L: Limited resources, can modify public tools and follow tutorials (low-skill but motivated attackers)
  - M: Moderate resources, can develop custom tools, understands defense evasion (organized criminal groups)
  - H: Significant resources, employs specialists, purchases 0-days, has operational security (well-funded criminal enterprises)
  - VH: Extensive resources, dedicated teams, custom toolchains, state-level infrastructure (nation-state APTs, tier-1 criminal syndicates)

- **Intent** — Degree of hostile motivation toward the target
  - VL: No hostile intent; actions are unintentional or incidental
  - L: Opportunistic; will exploit easy targets but won't invest effort
  - M: Motivated; has a reason to target but will move on if difficult
  - H: Dedicated; persistent motivation with willingness to invest significant effort
  - VH: Obsessive; single-minded focus on the target, will not be deterred

- **Targeting** — Degree to which the threat source specifically targets THIS organization
  - VL: Non-specific; targets of opportunity via automated scanning or mass campaigns
  - L: Semi-targeted; targets specific industries or geographies but not individual organizations
  - M: Targeted; selects specific organizations within a sector but without deep reconnaissance
  - H: Specifically targeted; conducts reconnaissance against this organization, tailors TTPs
  - VH: Surgically targeted; detailed knowledge of target's infrastructure, people, and defenses; custom operations

**Ask the operator:**
"Which individual-level adversarial sources are relevant to your organization? Consider:
- External attack surface (internet-facing services, public web presence, cloud footprint)
- Employee population (size, turnover rate, contractor ratio, remote workforce)
- Privileged access holders (how many admins, DBAs, security staff?)
- Insider threat indicators (industry with high IP value, defense/government contracts, recent layoffs, known grievances)
- Public profile (media presence, executive visibility, controversial operations)"

#### B. Group Threat Sources

| Source Subtype | Description | Relevant? | Capability (VL-VH) | Intent (VL-VH) | Targeting (VL-VH) | Rationale |
|----------------|-------------|-----------|--------------------|-----------------|--------------------|-----------|
| **Ad Hoc Group** | Loosely affiliated individuals with shared motivation — hacktivists (Anonymous-style), protest-driven groups, ideologically motivated collectives | ✅/❌ | | | | |
| **Established Group** | Organized criminal groups, ransomware affiliates, persistent threat groups with defined structure, funding, and specialization | ✅/❌ | | | | |

**Ask the operator:**
"Are there known threat groups that target your industry, geography, or organization type? Consider:
- Ransomware groups known to target your sector (e.g., healthcare: Hive, Royal; finance: Cl0p, LockBit; manufacturing: BlackBasta)
- Hacktivist groups with ideological opposition to your industry or operations
- Criminal groups known to operate in your geography or supply chain"

#### C. Organization Threat Sources

| Source Subtype | Description | Relevant? | Capability (VL-VH) | Intent (VL-VH) | Targeting (VL-VH) | Rationale |
|----------------|-------------|-----------|--------------------|-----------------|--------------------|-----------|
| **Competitor** | Business competitor seeking competitive advantage through espionage, sabotage, or IP theft | ✅/❌ | | | | |
| **Supplier/Vendor** | Supply chain entity with access to systems, data, or infrastructure — risk amplified by trust relationships | ✅/❌ | | | | |
| **Partner** | Business partner, joint venture participant, or consortium member with shared access or data exchange | ✅/❌ | | | | |
| **Customer** | Customer entity with access to customer-facing systems, APIs, or portals — risk of abuse or unauthorized access | ✅/❌ | | | | |
| **Nation-State** | State-sponsored or state-directed entities with geopolitical motivation — espionage, disruption, pre-positioning for conflict | ✅/❌ | | | | |

**Ask the operator:**
"Which organizational-level adversarial sources are relevant? Consider:
- Competitive landscape (high-value IP, market position, M&A activity)
- Supply chain exposure (number of vendors with system access, SaaS dependencies, managed service providers)
- Nation-state interest (critical infrastructure designation, defense contracts, geopolitical sensitivity, data of national interest)
- Customer-facing attack surface (APIs, portals, B2B integrations)"

**Compile the adversarial threat source summary:**

"**Adversarial Threat Source Summary:**

| # | Source | Subtype | Capability | Intent | Targeting | Threat Level | Key Concern |
|---|--------|---------|------------|--------|-----------|-------------|-------------|
| A1 | {{source}} | {{subtype}} | {{VL-VH}} | {{VL-VH}} | {{VL-VH}} | {{composite assessment}} | {{primary concern for this org}} |
| A2 | ... | ... | ... | ... | ... | ... | ... |

**Total Adversarial Sources Identified:** {{count}}
**Highest Threat Level Sources:** {{list sources rated H or VH on any dimension}}"

Update running count: `adversarial_sources: {{count}}`

### 3. Non-Adversarial Threat Source Identification (NIST 800-30, Table D-2)

Systematically assess non-adversarial threat sources. These are not intentionally hostile but can cause incidents equal to or exceeding adversarial impact.

#### A. Accidental Threat Sources

| Source Subtype | Description | Relevant? | Range of Effects (VL-VH) | Historical Precedent | Rationale |
|----------------|-------------|-----------|------------------------|---------------------|-----------|
| **User (non-privileged)** | Standard employees making mistakes — clicking phishing links, misconfiguring applications, mishandling data, shadow IT, lost devices | ✅/❌ | {{VL=minor data exposure, L=limited service disruption, M=significant data loss or service impact, H=critical system failure or major data breach, VH=catastrophic cascading failure}} | {{any known incidents in the organization?}} | {{why relevant — workforce size, remote work, training maturity, BYOD policy}} |
| **Privileged User/Admin** | System administrators, DBAs, network engineers making mistakes — misconfigurations, accidental deletions, failed patches, untested changes | ✅/❌ | | | |

**Ask the operator:**
"What is the accidental threat profile for your organization? Consider:
- Workforce maturity (security awareness training frequency, phishing simulation results, shadow IT prevalence)
- Change management discipline (are privileged changes peer-reviewed? Is there a CAB process? How often do changes cause outages?)
- Historical incidents (have accidental actions caused past incidents? What types?)
- Remote workforce (BYOD risk, home network security, physical security of devices)"

#### B. Structural Threat Sources

| Source Subtype | Description | Relevant? | Range of Effects (VL-VH) | Age/Condition | Rationale |
|----------------|-------------|-----------|------------------------|---------------|-----------|
| **IT Equipment — Storage** | SAN/NAS failures, disk failures, RAID degradation, backup media failures | ✅/❌ | | {{age, maintenance status, redundancy level}} | |
| **IT Equipment — Processing** | Server hardware failures, CPU failures, memory errors, motherboard failures | ✅/❌ | | | |
| **IT Equipment — Communications** | Network switch failures, router failures, firewall hardware failures, cable plant degradation, ISP outages | ✅/❌ | | | |
| **Environmental Controls** | HVAC failures in data centers, fire suppression system failures, UPS/generator failures, physical security system failures | ✅/❌ | | | |
| **Software — OS** | Operating system bugs, kernel panics, unpatched vulnerabilities, driver incompatibilities, end-of-life OS in production | ✅/❌ | | {{patch currency, EOL status}} | |
| **Software — Networking** | DNS failures, DHCP exhaustion, routing table corruption, certificate expiration, load balancer failures | ✅/❌ | | | |
| **Software — Mission-Specific** | Application bugs, database corruption, middleware failures, integration breakdowns, batch job failures | ✅/❌ | | | |

**Ask the operator:**
"What is the structural health of your infrastructure? Consider:
- Hardware lifecycle (average age of servers, switches, storage; replacement cadence; single points of failure)
- Software currency (patch cadence, number of EOL systems, technical debt level)
- Redundancy and failover (N+1, active-active, DR capability, tested failover procedures)
- Environmental controls (data center tier, maintenance contracts, monitoring maturity)"

#### C. Environmental Threat Sources

| Source Subtype | Description | Relevant? | Range of Effects (VL-VH) | Geographic Risk | Rationale |
|----------------|-------------|-----------|------------------------|----------------|-----------|
| **Fire** | Data center fire, office fire, wildfire proximity | ✅/❌ | | {{geographic fire risk, suppression systems}} | |
| **Flood** | Fluvial flooding, pluvial flooding, coastal flooding, pipe burst, sprinkler malfunction | ✅/❌ | | {{flood zone designation, floor level, historical floods}} | |
| **Earthquake** | Seismic activity affecting facilities and infrastructure | ✅/❌ | | {{seismic zone, building code compliance}} | |
| **Hurricane/Tornado** | High-wind events affecting facilities, power, and communications | ✅/❌ | | {{geographic wind risk, building construction}} | |
| **Power Failure** | Grid instability, prolonged outage, regional blackout | ✅/❌ | | {{grid reliability, UPS/generator capacity, fuel reserves}} | |
| **Telecommunications Failure** | ISP outage, last-mile failure, regional fiber cut, cloud provider outage | ✅/❌ | | {{ISP diversity, carrier redundancy, cloud region diversity}} | |

**Ask the operator:**
"What is the environmental threat profile for your facilities? Consider:
- Geographic location (natural disaster risk zones, climate patterns, historical events)
- Facility type (owned vs leased, data center tier, construction age and standards)
- Utility reliability (power grid stability, backup power capacity, ISP diversity)
- Cloud dependency (single-region vs multi-region, provider diversity, geographic distribution of cloud resources)"

**Compile the non-adversarial threat source summary:**

"**Non-Adversarial Threat Source Summary:**

| # | Source Category | Subtype | Range of Effects | Historical Precedent | Key Concern |
|---|---------------|---------|-----------------|---------------------|-------------|
| N1 | Accidental | {{subtype}} | {{VL-VH}} | {{yes/no — details}} | {{primary concern}} |
| N2 | Structural | {{subtype}} | {{VL-VH}} | {{yes/no — details}} | {{primary concern}} |
| N3 | Environmental | {{subtype}} | {{VL-VH}} | {{yes/no — details}} | {{primary concern}} |
| ... | ... | ... | ... | ... | ... |

**Total Non-Adversarial Sources Identified:** {{count}}
**Highest-Effect Sources:** {{list sources rated H or VH}}"

Update running count: `non_adversarial_sources: {{count}}`

### 4. Threat Event Mapping — Adversarial (NIST 800-30, Appendix E, Table E-2)

Map specific adversarial threat events to the identified threat sources. Organize by kill-chain phase to maintain operational structure. For each event, assess relevance to THIS organization and identify affected assets.

**Relevance Rating Scale:**

| Rating | Definition | Criteria |
|--------|-----------|----------|
| **Confirmed** | Observed in this environment | Threat intelligence, incident history, or active indicators confirm this event has occurred or is occurring |
| **Expected** | High probability based on specific threat intel | Sector-specific threat intelligence, similar organizations breached, active campaigns targeting this industry |
| **Anticipated** | Assessed likely based on industry data | Industry breach reports, DBIR statistics, regulatory findings indicate this event type is common in similar environments |
| **Predicted** | Possible based on general trends | General cybersecurity trends, emerging TTPs, new vulnerability disclosures suggest this event could occur |
| **Possible** | Cannot be ruled out | No specific indicators but the attack vector exists and cannot be excluded |

#### A. Reconnaissance & Resource Development

| # | Threat Event | Applicable Source(s) | Relevance | Affected Assets | Notes |
|---|-------------|---------------------|-----------|----------------|-------|
| E-A1 | Perform network scanning and reconnaissance (port scanning, service enumeration, vulnerability scanning) | {{from section 2}} | {{Confirmed/Expected/Anticipated/Predicted/Possible}} | {{from step-02 asset inventory}} | {{organizational context — internet-facing assets, exposure level}} |
| E-A2 | Perform host discovery and OS fingerprinting across exposed infrastructure | | | | |
| E-A3 | Social engineering to gather organizational information (OSINT, pretexting, vishing) | | | | |
| E-A4 | Perform reconnaissance of employee information via social media and public sources | | | | |
| E-A5 | Acquire infrastructure for attack staging (domains, VPS, C2 infrastructure) | | | | |
| E-A6 | Develop or acquire custom exploit tooling targeting organization's technology stack | | | | |

#### B. Initial Access & Weaponization

| # | Threat Event | Applicable Source(s) | Relevance | Affected Assets | Notes |
|---|-------------|---------------------|-----------|----------------|-------|
| E-B1 | Craft and deliver spear-phishing attacks targeting employees (email, social media, messaging) | | | | |
| E-B2 | Create counterfeit/spoofed websites to harvest credentials or deliver malware | | | | |
| E-B3 | Deliver known malware to internal systems via email attachments, web downloads, or removable media | | | | |
| E-B4 | Deliver modified/custom malware designed to evade current defensive controls | | | | |
| E-B5 | Deliver zero-day exploits against internet-facing services or client applications | | | | |
| E-B6 | Exploit public-facing application vulnerabilities (SQLi, RCE, SSRF, auth bypass) | | | | |
| E-B7 | Compromise supply chain to gain initial access (software supply chain, hardware supply chain, MSP compromise) | | | | |
| E-B8 | Exploit trusted third-party relationships for initial access (VPN, partner portals, API integrations) | | | | |
| E-B9 | Exploit valid credentials obtained through credential stuffing, password spraying, or dark web purchases | | | | |

#### C. Execution & Persistence

| # | Threat Event | Applicable Source(s) | Relevance | Affected Assets | Notes |
|---|-------------|---------------------|-----------|----------------|-------|
| E-C1 | Install persistent access mechanisms (backdoors, web shells, implants) on compromised systems | | | | |
| E-C2 | Install rootkits or bootkits to maintain stealthy persistent access below OS visibility | | | | |
| E-C3 | Install keyloggers, screen capture tools, or credential harvesting tools | | | | |
| E-C4 | Establish persistence via scheduled tasks, services, registry run keys, or startup items | | | | |
| E-C5 | Hijack legitimate software update mechanisms for persistence or delivery | | | | |
| E-C6 | Modify system configurations to weaken security controls (disable logging, modify firewall rules, disable AV) | | | | |

#### D. Privilege Escalation & Credential Access

| # | Threat Event | Applicable Source(s) | Relevance | Affected Assets | Notes |
|---|-------------|---------------------|-----------|----------------|-------|
| E-D1 | Exploit vulnerabilities in internal systems to escalate privileges (kernel exploits, service exploits, misconfigurations) | | | | |
| E-D2 | Conduct credential harvesting from memory (Mimikatz, LSASS dump, token theft) | | | | |
| E-D3 | Perform Kerberoasting, AS-REP roasting, or other Active Directory credential attacks | | | | |
| E-D4 | Exploit split tunneling or VPN misconfigurations to access internal resources | | | | |
| E-D5 | Abuse misconfigured permissions to escalate privileges (RBAC bypass, IAM policy exploitation, group policy abuse) | | | | |

#### E. Lateral Movement & Discovery

| # | Threat Event | Applicable Source(s) | Relevance | Affected Assets | Notes |
|---|-------------|---------------------|-----------|----------------|-------|
| E-E1 | Perform lateral movement using compromised credentials (RDP, SSH, SMB, WinRM, PsExec) | | | | |
| E-E2 | Enumerate internal network to identify additional targets, trust relationships, and high-value systems | | | | |
| E-E3 | Exploit trust relationships between systems (AD trusts, SSH key reuse, service account pivoting) | | | | |
| E-E4 | Move laterally through cloud environments (cross-account pivoting, service principal abuse, metadata service exploitation) | | | | |

#### F. Command & Control

| # | Threat Event | Applicable Source(s) | Relevance | Affected Assets | Notes |
|---|-------------|---------------------|-----------|----------------|-------|
| E-F1 | Establish C2 channels via encrypted external network connections (HTTPS, DNS tunneling, cloud services) | | | | |
| E-F2 | Communicate through covert channels or steganography to evade network monitoring | | | | |
| E-F3 | Use legitimate cloud services for C2 (Slack, Teams, Google Drive, Azure Blob, AWS S3) | | | | |
| E-F4 | Communicate via removable media or air-gap bridging techniques (for isolated networks) | | | | |

#### G. Actions on Objectives

| # | Threat Event | Applicable Source(s) | Relevance | Affected Assets | Notes |
|---|-------------|---------------------|-----------|----------------|-------|
| E-G1 | Exfiltrate sensitive data via network channels (HTTPS, DNS, cloud storage, email) | | | | |
| E-G2 | Exfiltrate data via physical means (USB, printed documents, photographed screens) | | | | |
| E-G3 | Modify or delete critical information/data to disrupt operations or destroy evidence | | | | |
| E-G4 | Disrupt mission/business operations through service degradation, denial of service, or system destruction | | | | |
| E-G5 | Deploy ransomware or destructive malware to extort or destroy | | | | |
| E-G6 | Obtain unauthorized access to systems to establish long-term strategic presence (espionage) | | | | |
| E-G7 | Manipulate business processes through compromised systems (fraud, transaction manipulation, supply chain manipulation) | | | | |

**Ask the operator for each phase:**
"Review the adversarial threat events mapped above. For each phase:
1. Are the relevance ratings accurate for your organization?
2. Are there specific threat events I should add based on your knowledge of past incidents or current threat intelligence?
3. Are any events marked as relevant that you believe should be downgraded? (If so, provide justification — I will warn if the downgrade removes coverage for a significant attack vector.)"

**Compile the adversarial event summary:**

"**Adversarial Threat Event Summary:**

| Phase | Events Mapped | Confirmed | Expected | Anticipated | Predicted | Possible |
|-------|-------------|-----------|----------|------------|-----------|----------|
| Reconnaissance & Resource Dev | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Initial Access & Weaponization | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Execution & Persistence | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Priv Escalation & Cred Access | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Lateral Movement & Discovery | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Command & Control | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Actions on Objectives | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| **TOTAL** | **{{total}}** | **{{total}}** | **{{total}}** | **{{total}}** | **{{total}}** | **{{total}}** |

**Top Relevance Events (Confirmed + Expected):** {{list the highest-relevance events that demand priority attention}}"

### 5. Threat Event Mapping — Non-Adversarial (NIST 800-30, Appendix E, Table E-3)

Map non-adversarial threat events to the sources identified in section 3. These events are not intentionally malicious but their impact can match or exceed adversarial events.

#### A. Accidental Threat Events

| # | Threat Event | Source Subtype | Relevance | Affected Assets | Notes |
|---|-------------|---------------|-----------|----------------|-------|
| E-NA1 | Spill of sensitive information (accidental email to wrong recipient, misconfigured sharing permissions, public S3 bucket, exposed API key in public repo) | User / Privileged User | {{relevance}} | {{assets}} | {{organizational context — data handling maturity, DLP controls}} |
| E-NA2 | Mishandling of critical and/or sensitive information (improper classification, storage in unauthorized location, transmission via insecure channel) | User / Privileged User | | | |
| E-NA3 | Incorrect privilege settings (over-permissioned accounts, misconfigured RBAC, stale access after role change, orphaned service accounts) | Privileged User/Admin | | | |
| E-NA4 | Accidental deletion or modification of critical data (unintended database operations, misconfigured scripts, fat-finger errors on production systems) | User / Privileged User | | | |
| E-NA5 | Misconfiguration of security controls (firewall rules, WAF bypass, disabled logging, incorrect encryption settings, permissive CORS) | Privileged User/Admin | | | |
| E-NA6 | Failed or untested changes deployed to production (patch breaks functionality, configuration change causes outage, migration corrupts data) | Privileged User/Admin | | | |
| E-NA7 | Introduction of vulnerable software through shadow IT (unapproved SaaS, personal devices, unauthorized development tools) | User | | | |

#### B. Structural Threat Events

| # | Threat Event | Source Subtype | Relevance | Affected Assets | Notes |
|---|-------------|---------------|-----------|----------------|-------|
| E-NS1 | Disk failure / storage array degradation / backup media failure | IT Equipment — Storage | | | |
| E-NS2 | Server hardware failure (CPU, memory, motherboard, power supply) | IT Equipment — Processing | | | |
| E-NS3 | Network communications contention / bandwidth exhaustion / routing failure | IT Equipment — Comms | | | |
| E-NS4 | Network device failure (switch, router, firewall, load balancer) | IT Equipment — Comms | | | |
| E-NS5 | HVAC failure leading to thermal shutdown of data center equipment | Environmental Controls | | | |
| E-NS6 | UPS/generator failure during power event | Environmental Controls | | | |
| E-NS7 | Fire suppression system malfunction (false trigger or failure to activate) | Environmental Controls | | | |
| E-NS8 | Operating system crash / kernel panic / unrecoverable software error | Software — OS | | | |
| E-NS9 | DNS/DHCP/certificate infrastructure failure (expired certificates, DNS resolution failure, DHCP exhaustion) | Software — Networking | | | |
| E-NS10 | Application software bug causing data corruption, service failure, or cascading dependency failure | Software — Mission-Specific | | | |
| E-NS11 | Database corruption or consistency failure | Software — Mission-Specific | | | |
| E-NS12 | Integration / middleware failure causing inter-system communication breakdown | Software — Mission-Specific | | | |

#### C. Environmental Threat Events

| # | Threat Event | Source Subtype | Relevance | Affected Assets | Notes |
|---|-------------|---------------|-----------|----------------|-------|
| E-NE1 | Earthquake causing facility damage, equipment displacement, or structural failure | Earthquake | | | |
| E-NE2 | Fire (natural or accidental) causing facility damage or data center loss | Fire | | | |
| E-NE3 | Flood (external flooding, pipe burst, sprinkler malfunction) causing water damage to equipment | Flood | | | |
| E-NE4 | Hurricane/tornado causing facility damage, prolonged power loss, or communications disruption | Hurricane/Tornado | | | |
| E-NE5 | Prolonged power outage exceeding UPS/generator capacity | Power Failure | | | |
| E-NE6 | Telecommunications infrastructure failure (ISP outage, fiber cut, regional network disruption) | Telecom Failure | | | |
| E-NE7 | Cloud provider regional outage affecting hosted services and data | Telecom Failure / Structural | | | |

**Ask the operator:**
"Review the non-adversarial threat events above:
1. Have any of these events occurred in your environment in the past 3-5 years?
2. Are there known structural weaknesses (aging infrastructure, single points of failure, deferred maintenance) that increase the relevance of structural events?
3. Are there geographic or facility-specific factors that affect environmental event relevance?
4. Are there additional non-adversarial events specific to your technology stack that should be added?"

**Compile the non-adversarial event summary:**

"**Non-Adversarial Threat Event Summary:**

| Category | Events Mapped | Confirmed | Expected | Anticipated | Predicted | Possible |
|----------|-------------|-----------|----------|------------|-----------|----------|
| Accidental | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Structural | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Environmental | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| **TOTAL** | **{{total}}** | **{{total}}** | **{{total}}** | **{{total}}** | **{{total}}** | **{{total}}** |

**Top Relevance Events (Confirmed + Expected):** {{list the highest-relevance non-adversarial events}}"

### 6. MITRE ATT&CK Cross-Reference

For each adversarial threat event identified in section 4, map to specific MITRE ATT&CK technique IDs. This cross-reference bridges the risk assessment to detection engineering — these technique IDs feed directly into SOC detection rules and Purple Team exercises.

**ATT&CK Mapping Table:**

| Threat Event ID | Threat Event Description | ATT&CK Tactic | ATT&CK Technique ID | Technique Name | Sub-technique(s) | Known Groups Using | Detection Data Source |
|----------------|------------------------|---------------|---------------------|---------------|------------------|-------------------|---------------------|
| E-A1 | Network scanning and reconnaissance | Reconnaissance | T1595 | Active Scanning | T1595.001 (Scanning IP Blocks), T1595.002 (Vulnerability Scanning) | {{groups relevant to org's sector}} | Network Traffic: Network Traffic Flow |
| E-A3 | Social engineering for information gathering | Reconnaissance | T1598 | Phishing for Information | T1598.001 (Spearphishing Service), T1598.002 (Spearphishing Attachment), T1598.003 (Spearphishing Link) | | Application Log: Email |
| E-B1 | Spear-phishing attacks | Initial Access | T1566 | Phishing | T1566.001 (Attachment), T1566.002 (Link), T1566.003 (Service) | | Application Log: Email, Network Traffic |
| E-B6 | Public-facing application exploitation | Initial Access | T1190 | Exploit Public-Facing Application | — | | Application Log, Network Traffic |
| E-B7 | Supply chain compromise | Initial Access | T1195 | Supply Chain Compromise | T1195.001 (Software), T1195.002 (Hardware) | | File Monitoring |
| E-B9 | Valid credential exploitation | Initial Access | T1078 | Valid Accounts | T1078.001 (Default), T1078.002 (Domain), T1078.003 (Local), T1078.004 (Cloud) | | Logon Session |
| E-C1 | Persistent access mechanisms | Persistence | T1505 | Server Software Component | T1505.003 (Web Shell) | | Process, File, Network |
| E-C4 | Scheduled task persistence | Persistence | T1053 | Scheduled Task/Job | T1053.005 (Scheduled Task) | | Process, Command |
| E-C6 | Security control modification | Defense Evasion | T1562 | Impair Defenses | T1562.001 (Disable/Modify Tools), T1562.004 (Disable/Modify Firewall) | | Process, Windows Registry |
| E-D1 | Internal privilege escalation | Privilege Escalation | T1068 | Exploitation for Privilege Escalation | — | | Process, Application Log |
| E-D2 | Credential harvesting from memory | Credential Access | T1003 | OS Credential Dumping | T1003.001 (LSASS Memory), T1003.003 (NTDS) | | Process, Command |
| E-D3 | AD credential attacks | Credential Access | T1558 | Steal or Forge Kerberos Tickets | T1558.003 (Kerberoasting), T1558.004 (AS-REP Roasting) | | Active Directory |
| E-E1 | Lateral movement via credentials | Lateral Movement | T1021 | Remote Services | T1021.001 (RDP), T1021.002 (SMB), T1021.004 (SSH) | | Logon Session, Network Traffic |
| E-E3 | Trust relationship exploitation | Lateral Movement | T1550 | Use Alternate Authentication Material | T1550.002 (Pass the Hash), T1550.003 (Pass the Ticket) | | Active Directory, Logon Session |
| E-F1 | C2 via external network | Command and Control | T1071 | Application Layer Protocol | T1071.001 (Web), T1071.004 (DNS) | | Network Traffic |
| E-F3 | C2 via cloud services | Command and Control | T1102 | Web Service | T1102.002 (Bidirectional) | | Network Traffic |
| E-G1 | Data exfiltration via network | Exfiltration | T1041 | Exfiltration Over C2 Channel | — | | Network Traffic |
| E-G3 | Data destruction/modification | Impact | T1485 | Data Destruction | — | | File, Process |
| E-G4 | Service disruption | Impact | T1499 | Endpoint Denial of Service | T1499.001-T1499.004 | | Network Traffic, Sensor Health |
| E-G5 | Ransomware deployment | Impact | T1486 | Data Encrypted for Impact | — | | File, Process |
| ... | {{continue for all adversarial events}} | ... | ... | ... | ... | ... | ... |

**IMPORTANT:** This table is the starter mapping. Expand it to cover ALL adversarial threat events identified in section 4. Events without ATT&CK mappings should be noted — they may represent novel TTPs or organizational-specific threat events not yet cataloged by MITRE.

**Ask the operator:**
"Review the ATT&CK mapping. Are there specific technique IDs or threat groups that your threat intelligence team has flagged as particularly relevant? Are there any techniques your SOC currently has detection rules for? (This helps identify coverage gaps.)"

**Compile the ATT&CK summary:**

"**MITRE ATT&CK Cross-Reference Summary:**

| Tactic | Techniques Mapped | Sub-techniques | Coverage |
|--------|-----------------|----------------|----------|
| Reconnaissance | {{count}} | {{count}} | {{mapped/total events in phase}} |
| Initial Access | {{count}} | {{count}} | |
| Execution | {{count}} | {{count}} | |
| Persistence | {{count}} | {{count}} | |
| Privilege Escalation | {{count}} | {{count}} | |
| Defense Evasion | {{count}} | {{count}} | |
| Credential Access | {{count}} | {{count}} | |
| Discovery | {{count}} | {{count}} | |
| Lateral Movement | {{count}} | {{count}} | |
| Collection | {{count}} | {{count}} | |
| Command and Control | {{count}} | {{count}} | |
| Exfiltration | {{count}} | {{count}} | |
| Impact | {{count}} | {{count}} | |
| **TOTAL** | **{{total}}** | **{{total}}** | **{{total mapped}}/{{total adversarial events}}** |

**Unmapped Events:** {{list any adversarial events without ATT&CK technique IDs — these are gaps}}
**Top Groups Relevant to Organization:** {{list threat groups most relevant to org's sector and geography}}"

Update running count: `mitre_techniques_mapped: {{count}}`

### 7. Threat-Asset Pairing Matrix

Build the critical mapping of which threat events target which assets. This matrix is the primary input for risk calculation in step 5 — every cell with a pairing generates a risk scenario that must be assessed.

**Matrix Structure:**

Use Crown Jewels (Tier 1) as primary columns, then Tier 2 critical assets. Tier 3 assets are grouped by category unless specific pairing is relevant.

| Threat Event | {{Crown Jewel 1}} | {{Crown Jewel 2}} | {{Crown Jewel 3}} | {{Tier 2 Asset A}} | {{Tier 2 Asset B}} | {{Tier 2 Asset C}} | {{Tier 3 (grouped)}} |
|-------------|-------------------|-------------------|-------------------|-------------------|-------------------|-------------------|---------------------|
| **Adversarial Events** | | | | | | | |
| E-A1: Network reconnaissance | | | | ✅ (C) | ✅ (C) | | ✅ (C) |
| E-B1: Spear-phishing | ✅ (C,I) | ✅ (C) | | ✅ (C) | | | |
| E-B6: Public app exploitation | ✅ (C,I,A) | | ✅ (C,I,A) | ✅ (C,I,A) | | | |
| E-B9: Valid credential abuse | ✅ (C,I) | ✅ (C,I) | ✅ (C,I) | ✅ (C,I) | ✅ (C,I) | | |
| E-C1: Persistent access | ✅ (C,I) | ✅ (C,I) | | ✅ (C,I) | | | |
| E-D2: Credential harvesting | ✅ (C) | ✅ (C) | ✅ (C) | ✅ (C) | ✅ (C) | ✅ (C) | ✅ (C) |
| E-E1: Lateral movement | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | | |
| E-G1: Data exfiltration | ✅ (C) | ✅ (C) | ✅ (C) | | | | |
| E-G4: Service disruption | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) |
| E-G5: Ransomware | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) |
| **Non-Adversarial Events** | | | | | | | |
| E-NA1: Sensitive data spill | ✅ (C) | ✅ (C) | | | | | |
| E-NA4: Accidental data deletion | ✅ (I,A) | ✅ (I,A) | ✅ (I,A) | | | | |
| E-NA5: Misconfigured controls | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | ✅ (C,I,A) | | |
| E-NS1: Storage failure | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | | | |
| E-NS3: Network contention | | | | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) |
| E-NS10: Application bug | ✅ (I,A) | | ✅ (I,A) | ✅ (I,A) | | | |
| E-NE5: Prolonged power outage | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) |
| E-NE7: Cloud provider outage | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | ✅ (A) | | |
| ... | {{complete for ALL events from sections 4 and 5}} | | | | | | |

**CIA Impact Key:**
- **C** = Confidentiality — unauthorized disclosure of information
- **I** = Integrity — unauthorized modification or destruction of information
- **A** = Availability — disruption of access to or use of information or systems

**Matrix Completion Rules:**
- Every threat event from sections 4 and 5 must appear in the matrix — no orphaned events
- Every Crown Jewel must have at least one pairing — an unpaired Crown Jewel means either the threat identification is incomplete or the asset classification is wrong
- CIA impact types must be specified per pairing — "this threat affects this asset" is insufficient; specify HOW it affects it
- Empty cells are valid and meaningful — they indicate a threat event does not apply to that specific asset

**Ask the operator:**
"Review the threat-asset pairing matrix:
1. Are there pairings I've missed? (Threats that could affect assets not marked)
2. Are there pairings I've included that you believe are not realistic? (If so, justify — I will warn if removing a pairing creates a blind spot)
3. Are the CIA impact types accurate for each pairing?
4. Which Crown Jewel has the most threat pairings? This asset requires the deepest vulnerability analysis in step 4."

**Compile the pairing matrix summary:**

"**Threat-Asset Pairing Matrix Summary:**

| Asset | Total Threat Pairings | Adversarial | Non-Adversarial | CIA Distribution |
|-------|---------------------|-------------|----------------|-----------------|
| {{Crown Jewel 1}} | {{count}} | {{count}} | {{count}} | C:{{count}} I:{{count}} A:{{count}} |
| {{Crown Jewel 2}} | {{count}} | {{count}} | {{count}} | C:{{count}} I:{{count}} A:{{count}} |
| ... | ... | ... | ... | ... |

**Most-Targeted Asset:** {{asset with most pairings}} — {{count}} threat pairings
**Most Common CIA Impact:** {{C, I, or A}} across all pairings
**Total Risk Scenarios Generated:** {{total non-empty cells}} — each feeds into risk calculation in step 5"

### 8. Threat Landscape Summary

Compile the comprehensive threat landscape summary that consolidates all findings from this step:

"**Threat Landscape Summary — Step 3 Complete**

### Threat Source Totals

| Category | Sources Identified | Highest-Rated Source |
|----------|-------------------|---------------------|
| Adversarial — Individual | {{count}} | {{source with highest composite rating}} |
| Adversarial — Group | {{count}} | {{source}} |
| Adversarial — Organization | {{count}} | {{source}} |
| Accidental | {{count}} | {{source}} |
| Structural | {{count}} | {{source}} |
| Environmental | {{count}} | {{source}} |
| **TOTAL** | **{{total_sources}}** | |

### Threat Event Totals

| Category | Events Mapped | Confirmed | Expected | Anticipated | Predicted | Possible |
|----------|-------------|-----------|----------|------------|-----------|----------|
| Adversarial | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| Non-Adversarial | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} | {{count}} |
| **TOTAL** | **{{total_events}}** | | | | | |

### Top Threats by Relevance

| Rank | Threat Event | Relevance | Source(s) | Affected Crown Jewels | CIA Impact |
|------|-------------|-----------|----------|---------------------|-----------|
| 1 | {{event}} | {{rating}} | {{source}} | {{assets}} | {{C/I/A}} |
| 2 | ... | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... |

### Most-Targeted Assets

| Rank | Asset | Total Threat Pairings | Top Threat | Primary CIA Concern |
|------|-------|---------------------|-----------|-------------------|
| 1 | {{asset}} | {{count}} | {{highest-relevance threat targeting this asset}} | {{C, I, or A}} |
| 2 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

### ATT&CK Coverage

| Metric | Value |
|--------|-------|
| Total Techniques Mapped | {{count}} |
| Total Sub-techniques | {{count}} |
| Tactics Covered | {{count}}/14 |
| Unmapped Adversarial Events | {{count}} |
| Top Relevant Threat Group | {{group}} |

### Coverage Gaps Identified

| Gap | Description | Risk | Recommendation |
|-----|-------------|------|---------------|
| {{gap}} | {{description of uncovered area}} | {{what could be missed}} | {{how to address in subsequent steps}} |

**Key Findings:**
1. {{most critical insight from the threat landscape analysis}}
2. {{second most critical insight}}
3. {{third most critical insight}}"

### 9. Write Section 3 to Output Document

Populate Section 3 (Threat Landscape) in the output document with the following structure:

```markdown
## 3. Threat Landscape

### 3.1 Threat Source Identification
{{Complete threat source taxonomy from sections 2 and 3 — all adversarial and non-adversarial sources with characterization}}

### 3.2 Adversarial Threat Characterization
{{Detailed characterization of each adversarial source — capability, intent, targeting ratings with rationale}}
{{Include group/organization-level sources with sector-specific context}}

### 3.3 Non-Adversarial Threat Sources
{{Accidental, structural, and environmental sources with range of effects and historical precedent}}
{{Include facility-specific and technology-stack-specific context}}

### 3.4 Threat Event Mapping
{{All adversarial events from section 4, organized by kill-chain phase, with relevance ratings}}
{{All non-adversarial events from section 5, organized by source category, with relevance ratings}}

### 3.5 MITRE ATT&CK Cross-Reference
{{ATT&CK mapping table from section 6 — technique IDs, sub-techniques, relevant groups, detection data sources}}
{{ATT&CK coverage summary}}

### 3.6 Threat-Asset Pairing Matrix
{{Complete threat-asset matrix from section 7 with CIA impact types}}
{{Pairing summary statistics}}
{{Risk scenario count that feeds into step 5}}
```

**Frontmatter Updates:**

Update the following frontmatter fields in the output document:

```yaml
threat_sources_identified: {{total count of all threat sources across all 4 categories}}
threat_events_mapped: {{total count of all threat events (adversarial + non-adversarial)}}
adversarial_sources: {{count of adversarial threat sources}}
non_adversarial_sources: {{count of non-adversarial threat sources}}
mitre_techniques_mapped: {{count of unique ATT&CK technique IDs mapped}}
relevance_ratings_complete: true
threat_asset_pairings: {{count of non-empty cells in the pairing matrix}}
risk_scenarios_generated: {{count of threat-asset pairings that feed into step 5}}
```

### 10. Present MENU OPTIONS

"**Threat source and event identification complete.**

**Threat Landscape Summary:**
- **Threat Sources:** {{total_sources}} identified ({{adversarial_count}} adversarial, {{non_adversarial_count}} non-adversarial)
- **Threat Events:** {{total_events}} mapped ({{adversarial_events}} adversarial, {{non_adversarial_events}} non-adversarial)
- **Relevance Distribution:** {{confirmed}} Confirmed, {{expected}} Expected, {{anticipated}} Anticipated, {{predicted}} Predicted, {{possible}} Possible
- **ATT&CK Techniques Mapped:** {{technique_count}} techniques across {{tactic_count}} tactics
- **Threat-Asset Pairings:** {{pairing_count}} risk scenarios identified for step 5
- **Most-Targeted Asset:** {{asset_name}} with {{count}} threat pairings
- **Top Threat Event:** {{event_name}} ({{relevance}}) affecting {{affected_asset_count}} assets
- **Coverage Gaps:** {{gap_count}} identified — {{brief description}}

**Select an option:**
[A] Advanced Elicitation — Challenge threat completeness, characterization accuracy, and relevance ratings; stress-test the threat landscape for blind spots
[W] War Room — Red Team validates threat realism and identifies missing attack paths; Blue Team assesses detection coverage for identified threats and identifies telemetry gaps
[C] Continue — Save and proceed to Step 4: Vulnerability & Predisposing Conditions (Step 4 of 7)"

#### Menu Handling Logic:

- IF A: Advanced Elicitation on threat landscape completeness — challenge whether the threat source characterization is granular enough (are "outsiders" differentiated by motivation and capability?), stress-test relevance ratings (is "Possible" being used to avoid the work of proper threat assessment?), question whether the ATT&CK mapping covers the full kill chain or has tactical gaps, examine whether non-adversarial threats received the same rigor as adversarial threats, challenge the threat-asset pairings for completeness and accuracy. Process insights, ask operator if they want to update findings, if yes update then redisplay menu, if no redisplay menu.

- IF W: War Room discussion — **Red Team perspective:** Given the identified adversarial threat sources and their characterization, what attack paths are most realistic? Are there missing adversarial events that a skilled attacker would use against THIS specific organization? Are the capability/intent/targeting ratings accurate or are we underestimating specific threat actors? What would a dedicated adversary target first based on the asset inventory? Are there supply chain or trust relationship attack vectors we haven't considered? **Blue Team perspective:** For the identified adversarial events, what detection coverage exists today? Which ATT&CK techniques have detection rules and which are blind spots? Are there non-adversarial events where monitoring is insufficient (e.g., no alerting on misconfigurations, no hardware health monitoring, no environmental sensors)? What telemetry would need to be in place to detect the top-relevance threat events? Where are the biggest detection gaps relative to the highest-relevance threats? Summarize insights, redisplay menu.

- IF C: Update output file frontmatter adding `step-03-threat-identification.md` to the end of the `stepsCompleted` array and updating all threat identification fields (threat_sources_identified, threat_events_mapped, adversarial_sources, non_adversarial_sources, mitre_techniques_mapped, relevance_ratings_complete, threat_asset_pairings, risk_scenarios_generated), then read fully and follow: `./step-04-vulnerability-assessment.md`

- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, threat_sources_identified populated, threat_events_mapped populated, adversarial_sources and non_adversarial_sources counted, mitre_techniques_mapped counted, relevance_ratings_complete set to true, threat_asset_pairings counted, and Section 3 (Threat Landscape) fully populated in the report with all six subsections], will you then read fully and follow: `./step-04-vulnerability-assessment.md` to begin vulnerability and predisposing condition analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All four NIST 800-30 threat source categories assessed (adversarial, accidental, structural, environmental) — no category skipped
- Adversarial threat sources characterized by capability, intent, and targeting on the VL-VH scale with documented rationale
- Non-adversarial threat sources assessed for range of effects with historical precedent consideration
- Adversarial threat events mapped from NIST 800-30 Appendix E, Table E-2, organized by kill-chain phase
- Non-adversarial threat events mapped from NIST 800-30 Appendix E, Table E-3, organized by source category
- Relevance ratings assigned to every threat event using the five-level scale (Confirmed/Expected/Anticipated/Predicted/Possible)
- MITRE ATT&CK cross-reference completed for adversarial events with technique IDs, sub-techniques, and detection data sources
- Threat-asset pairing matrix completed with CIA impact types for every non-empty cell
- Every Crown Jewel from step-02 has at least one threat pairing
- No orphaned threat events (events without asset pairings)
- Threat landscape summary compiled with coverage gap analysis
- Section 3 of output document populated with all six subsections (3.1 through 3.6)
- Frontmatter updated with all threat identification counts (sources, events, techniques, pairings, scenarios)
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### ❌ SYSTEM FAILURE:

- Only adversarial threats considered — non-adversarial sources (accidental, structural, environmental) ignored or dismissed without justification
- Threat sources identified without characterization — listing "insider threat" without capability/intent/targeting assessment is useless for risk calculation
- Generic threat labels used without specificity — "hackers" is not a threat source characterization; it is a word
- No relevance assessment — every threat event assigned the same rating, or ratings assigned without organizational context
- Threats not mapped to specific assets — a threat landscape disconnected from the asset inventory produces a shelf document, not a risk assessment
- ATT&CK cross-reference skipped — without technique IDs, the bridge to detection engineering is broken
- CIA impact types not specified in threat-asset pairings — "this threat affects this asset" without C/I/A specificity is insufficient for risk calculation
- Likelihood, impact, or risk scores calculated in this step — this step identifies WHAT, not HOW LIKELY or HOW BAD
- Risk treatment or control recommendations made in this step — those belong in steps 5, 6, and 7
- Content generated without operator input — the operator provides the organizational context that makes the threat landscape specific
- Frontmatter not updated with all threat identification metrics before proceeding
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted and all threat identification results

**Master Rule:** A threat without context is noise. Every threat source must be characterized. Every threat event must be rated for relevance. Every threat must be mapped to affected assets with CIA impact types. Every adversarial threat must be connected to observable TTPs via ATT&CK technique IDs. The threat landscape is not a catalog of everything bad that could happen — it is a structured, organization-specific inventory of what matters HERE, rated by relevance, mapped to what it threatens, and connected to how it can be detected.
