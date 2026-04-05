# Step 8: Target Package Assembly

**Progress: Step 8 of 10** — Next: Detection Gap Analysis

## STEP GOAL:

Organize ALL findings from steps 2-7 into a structured, prioritized target package. This is the operational output that feeds directly into exploitation planning (Initial Access phase). Every target is prioritized by attack potential and mapped to MITRE ATT&CK techniques.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER introduce findings not already documented in previous steps
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RECONNAISSANCE SPECIALIST assembling an actionable target package
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Reconnaissance Specialist conducting authorized external reconnaissance
- ✅ The target package is the bridge between recon and exploitation
- ✅ Prioritization must be data-driven, based on actual findings
- ✅ ATT&CK mapping provides common language for Red/Blue team handoff
- ✅ Every recommended attack vector must trace back to specific findings

### Step-Specific Rules:

- 🎯 Focus on synthesis, prioritization, and ATT&CK mapping
- 🚫 FORBIDDEN to perform any new reconnaissance or scanning
- 💬 Approach: Analytical assembly of existing findings into operational intelligence
- 📊 Every target must have: priority rating, attack vectors, ATT&CK mapping
- 🔒 All findings must reference only in-scope assets

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Presenting findings without MITRE ATT&CK mapping — ATT&CK provides the common language for Red/Blue team handoff and is non-negotiable for operational target packages
  - Prioritizing targets based on operator preference alone rather than evidence — priority must be driven by CVSS scores, exploit availability, and attack surface data, not subjective opinion
  - Omitting low-priority targets from the package — the target package must be comprehensive; even low-priority targets can become high-priority through chaining or changed conditions
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present assembly plan before beginning synthesis
- ⚠️ Present [A]/[W]/[C] menu after package complete
- 💾 ONLY save target package to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: All findings from steps 1-7 are in the report
- Focus: Synthesis, prioritization, and ATT&CK mapping only
- Limits: No new reconnaissance — work only with existing data
- Dependencies: All previous step outputs feed into this synthesis

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Review All Previous Findings

**Read the complete output document to build a mental model:**

From each section, extract:
- **OSINT (Step 2):** Email addresses, credential leaks, technology intelligence, exposed documents
- **Subdomains (Step 3):** Live subdomains, takeover candidates, infrastructure distribution
- **Services (Step 4):** Open ports, service versions, OS fingerprints, high-exposure hosts
- **Web Apps (Step 5):** Technologies, API endpoints, auth mechanisms, input points
- **Vulnerabilities (Step 6):** CVEs, misconfigurations, SSL issues, missing headers
- **Cloud (Step 7):** Cloud resources, storage exposure, CDN/WAF configuration

"**Findings Review Complete**

Preparing target package from collected data:
- Passive OSINT: {{osint_finding_count}} findings
- Subdomains: {{subdomain_count}} unique ({{alive_count}} active)
- Services: {{service_count}} across {{host_count}} hosts
- Web applications: {{web_app_count}}
- Vulnerabilities: {{vuln_count}} ({{critical}} critical, {{high}} high)
- Cloud: {{cloud_resource_count}} resources

Proceeding with prioritization and ATT&CK mapping?"

### 2. Target Prioritization

**Assign priority to each target based on attack potential:**

**Priority Criteria Matrix:**

| Priority | Criteria | Examples |
|----------|----------|----------|
| **CRITICAL** | Critical CVE with public exploit + exposed service, or direct unauthenticated access to sensitive data | RCE on web service, public S3 storage with data, subdomain takeover on primary domain |
| **HIGH** | High CVE or multiple medium CVEs + broad attack surface, or recent leaked credentials | Exposed admin panel + credential leak, unauthenticated API + sensitive data, vulnerable SSL + critical service |
| **MEDIUM** | Medium CVE or significant misconfigurations, or attack vector requiring chaining | Missing security headers + input points, default credentials identified, enumerable cloud storage |
| **LOW** | Informational findings, missing hardening without direct impact | Version disclosure, banner information, DNS zone info |

**For each target (host/application), calculate:**
1. Highest severity vulnerability associated
2. Number of distinct attack vectors available
3. Potential business impact (based on service type and data exposure)
4. Exploitability (public exploit? authentication required? complexity?)

### 3. ATT&CK Technique Mapping

**Map ALL reconnaissance findings to MITRE ATT&CK techniques:**

**Reconnaissance Phase (TA0043):**
- T1595 — Active Scanning (port scanning, service enumeration)
- T1595.001 — Scanning IP Blocks
- T1595.002 — Vulnerability Scanning
- T1595.003 — Wordlist Scanning
- T1592 — Gather Victim Host Information
- T1592.002 — Software (technology stack identification)
- T1592.004 — Client Configurations
- T1593 — Search Open Websites/Domains
- T1593.001 — Social Media
- T1593.002 — Search Engines (Google dorking)
- T1593.003 — Code Repositories
- T1594 — Search Victim-Owned Websites
- T1596 — Search Open Technical Databases
- T1596.001 — DNS/Passive DNS
- T1596.002 — WHOIS
- T1596.003 — Digital Certificates (CT logs)
- T1596.005 — Scan Databases (Shodan, Censys)
- T1589 — Gather Victim Identity Information
- T1589.001 — Credentials (credential leak checking)
- T1589.002 — Email Addresses
- T1590 — Gather Victim Network Information
- T1590.001 — Domain Properties
- T1590.002 — DNS
- T1590.004 — Network Topology
- T1590.005 — IP Addresses

**Potential Initial Access Techniques (TA0001) — based on findings:**
- T1190 — Exploit Public-Facing Application (from CVEs found)
- T1133 — External Remote Services (VPN, RDP, SSH exposure)
- T1078 — Valid Accounts (from credential leaks)
- T1199 — Trusted Relationship (cloud service connections)

**Map each target to applicable T-codes:**
```
| Target | Recon Techniques Used | Potential Initial Access Techniques | T-Codes |
|--------|----------------------|-----------------------------------|---------|
```

### 4. Create Target Summary Table

**Master Target Table — the core of the target package:**

```
| # | IP | Hostname | Services | Vulnerabilities | Attack Vectors | Priority | T-Codes |
|---|-----|----------|----------|-----------------|----------------|----------|---------|
```

**Sort by priority (CRITICAL first, then HIGH, MEDIUM, LOW).**

### 5. Recommended Attack Vectors

**For each CRITICAL and HIGH priority target, detail the recommended attack approach:**

```
### Target #{{n}}: {{hostname}} ({{ip}}) — Priority: {{priority}}

**Exposed services:** {{services}}
**Key vulnerabilities:** {{key_vulns}}

**Recommended attack vector:**
1. {{step_1_description}} — {{technique_and_tool}}
2. {{step_2_description}} — {{technique_and_tool}}
3. {{step_3_description}} — {{technique_and_tool}}

**ATT&CK Chain:** {{T-code sequence}}
**Success likelihood:** {{high/medium/low}}
**Prerequisites:** {{prerequisites}}
**Risks:** {{detection_risk, collateral_damage_risk}}
```

### 6. Attack Path Visualization

**Identify multi-step attack chains:**

- Chain credential leaks → valid accounts → exposed admin panel
- Chain subdomain takeover → phishing infrastructure → initial access
- Chain cloud storage exposure → data exfiltration path
- Chain vulnerability → RCE → lateral movement opportunity

"**Attack Paths Identified:**

{{for each attack_path}}
**Path {{n}}:** {{path_description}}
Complexity: {{complexity}} | Likelihood: {{likelihood}} | Impact: {{impact}}
{{steps_in_chain}}
{{/for}}"

### 7. Append Target Package to Report

Write under `## Target Package`:

```markdown
## Target Package

### Target Summary
- Total targets: {{total_targets}}
- Critical priority: {{critical_count}}
- High priority: {{high_count}}
- Medium priority: {{medium_count}}
- Low priority: {{low_count}}
- ATT&CK techniques mapped: {{technique_count}}

### Master Target Table
{{master_target_table}}

### Recommended Attack Vectors
{{per_target_attack_vectors — CRITICAL and HIGH only}}

### Multi-Step Attack Paths
{{attack_path_chains}}

### MITRE ATT&CK Mapping
#### Reconnaissance Techniques Used
{{recon_techniques_used_with_T_codes}}
#### Potential Initial Access Techniques
{{initial_access_techniques_with_T_codes}}

### Target Package Statistics
{{comprehensive_statistics}}
```

Update frontmatter:
- `priority_targets` with updated counts per priority
- `attack_techniques_mapped` with list of all T-codes used

### 8. Present MENU OPTIONS

"**Target package assembled.**

Summary: {{total_targets}} prioritized targets. {{critical_count}} critical, {{high_count}} high.
ATT&CK techniques mapped: {{technique_count}} | Attack paths: {{path_count}}

**Select an option:**
[A] Advanced Elicitation — In-depth analysis of attack paths
[W] War Room — Red vs Blue discussion on the complete target package
[C] Continue — Proceed to Detection Gap Analysis (Step 9 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — overlooked attack combinations, alternative attack paths, risk-adjusted prioritization review, comparison with common real-world attack patterns. Redisplay menu
- IF W: War Room — Red: prioritization agreement? Missing attack vectors? Exploitation timeline estimate? Blue: which attack paths are most likely to succeed undetected? Priority defensive hardening recommendations? Incident response preparation for likely attack vectors. Summarize, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted and updating priority_targets and attack_techniques_mapped, then read fully and follow: ./step-09-detection-gap.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, priority_targets and attack_techniques_mapped updated], will you then read fully and follow: `./step-09-detection-gap.md` to begin detection gap analysis.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All findings from steps 2-7 reviewed and synthesized
- Every target assigned a data-driven priority rating
- ATT&CK techniques mapped to all findings (recon + potential initial access)
- Master target table created with IP, hostname, services, vulns, priority, T-codes
- Recommended attack vectors detailed for CRITICAL and HIGH targets
- Multi-step attack paths identified and documented
- priority_targets and attack_techniques_mapped updated in frontmatter

### ❌ SYSTEM FAILURE:

- Introducing new findings not documented in previous steps
- Performing any new scanning or reconnaissance
- Not mapping findings to ATT&CK techniques
- Prioritizing based on assumptions rather than actual findings
- Missing attack path chains that are visible in the data
- Not providing recommended attack vectors for high-priority targets
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Synthesize, prioritize, and map — no new recon.
