# Step 2: Attack Surface Analysis and Defensive Posture

**Progress: Step 2 of 10** — Next: Technique Selection

## STEP GOAL:

Classify the entire attack surface from the recon output and map the target's defensive posture to inform the selection of the initial access technique. This analysis transforms raw reconnaissance data into operational intelligence that determines which attack vectors are feasible and which defenses must be bypassed.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER classify defenses without evidence from recon data — assumptions kill operations
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INITIAL ACCESS SPECIALIST, not an autonomous exploit tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Initial Access Specialist conducting authorized offensive operations
- ✅ Attack surface analysis is the bridge between reconnaissance and technique selection
- ✅ Every classification must be grounded in recon data — never speculate without evidence
- ✅ Defensive posture assessment directly drives which TA0001 techniques are viable

### Step-Specific Rules:

- 🎯 Focus exclusively on attack surface classification and defensive posture mapping
- 🚫 FORBIDDEN to attempt exploitation or active probing — this is analysis of existing data
- 💬 Approach: Systematic categorization of recon findings into actionable attack surface intelligence
- 📊 Every finding must include: source data reference, confidence level, and impact on TA0001
- 🔒 All analysis must reference in-scope targets only — no speculation about unobserved assets

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Skipping defensive posture analysis means technique selection will be uninformed — without knowing the defenses, any technique choice is a blind shot that leads to detection and mission failure
  - Classifying defenses without evidence may lead to failed operations — overconfidence leads to detection, every classification must have a reference in the data
  - Ignoring credential leak data means missing potentially the fastest and stealthiest vector for initial access — not evaluating them means losing critical opportunities
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present your attack surface analysis plan before beginning classification
- ⚠️ Present [A]/[W]/[C] menu after analysis complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, RoE constraints, and full recon output from steps 1 (ingested)
- Focus: Attack surface categorization and defensive posture mapping — no active testing
- Limits: Only classify assets present in recon data — do not invent or assume unobserved assets
- Dependencies: Verified engagement and ingested recon output from step-01-init.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Attack Surface Classification

Parse all recon data into 5 attack surface categories. For each category, extract and classify every relevant finding:

**Category 1 — Network Perimeter:**
- Exposed services: VPN gateways, RDP endpoints, SSH servers, mail servers (SMTP/IMAP/POP3)
- High-risk ports: management interfaces, database ports, legacy protocols
- Obsolete services: EOL versions, deprecated protocols (FTP, Telnet, SMBv1)
- Gateways and proxies: reverse proxy, load balancer, WAF indicators from port scan behavior

**Category 2 — Human Targets:**
- Harvested emails: addresses collected from OSINT with format (first.last, flast, etc.)
- Org chart: organizational structure reconstructed from LinkedIn and public sources
- Key roles: IT administrator, C-suite, HR, finance — priority targets for social engineering
- Social media exposure: personal profiles with exploitable information for pretext

**Category 3 — Web Applications:**
- Applications with known vulnerabilities: CVEs mapped from identified versions
- API endpoints: exposed REST/GraphQL, public documentation, unauthenticated endpoints
- Exposed admin panels: CMS admin, phpMyAdmin, management consoles
- Vulnerable CMS: WordPress, Drupal, Joomla with outdated plugins/themes

**Category 4 — Cloud Infrastructure:**
- Exposed buckets/blobs: S3, Azure Blob, GCS with public permissions
- Misconfigured cloud services: instances with exposed metadata endpoint, permissive security groups
- Subdomain takeover candidates: dangling CNAMEs pointing to decommissioned cloud services
- Cloud-hosted applications: cloud services with potential misconfiguration

**Category 5 — Supply Chain:**
- Identified vendors: technology suppliers, managed services, outsourcers
- Third-party services: SaaS integrations, SSO federations, third-party APIs
- Software dependencies: libraries, frameworks, components with known vulnerabilities

**Present attack surface summary as:**
```
| Category | Asset Count | Max Risk | Potential Vector | Notes |
|----------|-------------|----------|-----------------|-------|
| Network Perimeter | {{count}} | Critical/High/Medium/Low | {{vector}} | {{note}} |
| Human Targets | {{count}} | Critical/High/Medium/Low | {{vector}} | {{note}} |
| Web Applications | {{count}} | Critical/High/Medium/Low | {{vector}} | {{note}} |
| Cloud Infrastructure | {{count}} | Critical/High/Medium/Low | {{vector}} | {{note}} |
| Supply Chain | {{count}} | Critical/High/Medium/Low | {{vector}} | {{note}} |
```

### 2. Defensive Posture Analysis

Map the target's defensive controls across 6 domains using evidence from recon data:

**Domain 1 — Email Security:**
- MX records analysis → identify email gateway vendor (Proofpoint, Mimecast, M365 Defender, Barracuda)
- DMARC enforcement level: `none` / `quarantine` / `reject` — parsed from TXT records
- DKIM presence and configuration — key length, selector patterns
- SPF record strictness: `~all` (softfail) vs `-all` (hardfail)
- Anti-phishing indicators: URL rewriting (Proofpoint URLDefense, Mimecast URL Protect)

**Domain 2 — Network Perimeter:**
- WAF presence and vendor: Cloudflare, Akamai, AWS WAF, F5 — from HTTP headers and behavior
- IDS/IPS indicators: rate limiting behavior, connection reset patterns, scan detection
- CDN/DDoS protection: Cloudflare, Akamai, AWS Shield indicators
- Firewall rules inferred: filtered vs closed ports, port scan response patterns, RST behavior

**Domain 3 — Endpoint Security:**
- EDR/AV indicators: job postings mentioning CrowdStrike, SentinelOne, Carbon Black, Defender
- Technology stack hints: endpoint management (SCCM, Intune, Jamf) from OSINT
- Patch cadence estimation: from service version currency across exposed services

**Domain 4 — Authentication:**
- MFA indicators: login pages with MFA prompts, Duo, Okta, Azure MFA references
- Password policy: complexity requirements from exposed login interfaces
- SSO/federation presence: SAML, OAuth endpoints, identity provider indicators (Azure AD, Okta, Ping)

**Domain 5 — Cloud Security:**
- Public bucket policies: ACL configuration, public access settings
- Cloud WAF: AWS WAF rules, Azure Front Door, GCP Cloud Armor indicators
- IAM indicators: role-based access patterns, service account exposure

**Domain 6 — Monitoring:**
- SOC indicators: job postings for SOC analysts, security operations mentions
- SIEM mentions: Splunk, Sentinel, QRadar, Elastic SIEM in job postings or technology references
- Logging posture: verbose headers, access logging indicators, audit trail evidence from exposed services

**Present defense matrix:**
```
| Defensive Domain | Identified Controls | Estimated Level | Impact on TA0001 | Evidence |
|------------------|---------------------|-----------------|------------------|----------|
| Email Security | {{controls}} | Strong/Medium/Weak/Unknown | {{impact}} | {{evidence}} |
| Network Perimeter | {{controls}} | Strong/Medium/Weak/Unknown | {{impact}} | {{evidence}} |
| Endpoint Security | {{controls}} | Strong/Medium/Weak/Unknown | {{impact}} | {{evidence}} |
| Authentication | {{controls}} | Strong/Medium/Weak/Unknown | {{impact}} | {{evidence}} |
| Cloud Security | {{controls}} | Strong/Medium/Weak/Unknown | {{impact}} | {{evidence}} |
| Monitoring | {{controls}} | Strong/Medium/Weak/Unknown | {{impact}} | {{evidence}} |
```

**CRITICAL:** `Unknown` is a valid and honest classification. Never upgrade `Unknown` to `Weak` without evidence — lack of information is NOT evidence of weakness.

### 3. Defense Impact on Techniques Matrix

Cross-reference defensive posture against TA0001 techniques to assess feasibility:

```
| Technique (T-Code) | Email Sec | Network Sec | Endpoint | Auth | Cloud | Feasibility |
|--------------------|-----------|-------------|----------|------|-------|-------------|
| T1566 Phishing | {{impact}} | - | {{impact}} | - | - | High/Medium/Low |
| T1190 Exploit Public-Facing App | - | {{impact}} | {{impact}} | - | - | High/Medium/Low |
| T1133 External Remote Services | - | {{impact}} | - | {{impact}} | - | High/Medium/Low |
| T1078 Valid Accounts | {{impact}} | - | - | {{impact}} | {{impact}} | High/Medium/Low |
| T1189 Drive-by Compromise | - | {{impact}} | {{impact}} | - | - | High/Medium/Low |
| T1199 Trusted Relationship | - | - | - | {{impact}} | {{impact}} | High/Medium/Low |
```

For each technique, explain the reasoning:
- Which defensive controls directly impact this technique?
- What is the aggregate effect on feasibility?
- Are there known bypasses for the identified controls?

### 4. Quick Win Identification

Identify targets with the highest reward-to-risk ratio:

**Quick Win Criteria:**
- Critical CVE + exposed service + no WAF detected = **quick win** (exploit path)
- Credential leaks + no MFA indicators = **quick win** (valid accounts path)
- Subdomain takeover candidate = **phishing infrastructure opportunity** (enables other techniques)
- Exposed admin panel + default/weak auth indicators = **quick win** (direct access)
- VPN/RDP exposed + credential leak for related accounts = **quick win** (remote services path)

**For each quick win identified, document:**
```
| # | Target | Vector | Defenses to Bypass | Detection Risk | Reward | Priority |
|---|--------|--------|-------------------|----------------|--------|----------|
```

**IMPORTANT:** Quick wins are opportunities, not guarantees. Each must be validated during technique selection and execution phases.

### 5. Summary and Preliminary Recommendation

Synthesize all analysis into actionable intelligence:

**Top 3 Attack Vectors — ranked by feasibility:**

For each vector, present:
```
| Rank | Attack Vector | T-Code | Identified Targets | Defensive Gaps | Success Prob. | Detection Risk | Estimated Effort |
|------|--------------|--------|-------------------|----------------|---------------|----------------|-----------------|
| 1 | {{vector}} | {{tcode}} | {{targets}} | {{gaps}} | High/Medium/Low | High/Medium/Low | {{estimate}} |
| 2 | {{vector}} | {{tcode}} | {{targets}} | {{gaps}} | High/Medium/Low | High/Medium/Low | {{estimate}} |
| 3 | {{vector}} | {{tcode}} | {{targets}} | {{gaps}} | High/Medium/Low | High/Medium/Low | {{estimate}} |
```

**Defensive Gap Summary:**
- Which defensive domains are weakest and why?
- Where are the blind spots in the target's monitoring?
- What attack vectors align with the identified gaps?
- Which gaps are confirmed vs inferred?

**Risk Assessment per Vector:**
- What happens if the technique fails? What evidence does a failed attempt leave?
- What is the detection signature? Which defensive controls would trigger?
- Can the operator pivot to an alternative without burning the engagement?
- What is the blast radius of detection — does it alert only to that vector or expose the entire operation?

### 6. Append Findings to Report

Write the consolidated attack surface analysis to the output document under `## Attack Surface Analysis`:

```markdown
## Attack Surface Analysis

### Attack Surface Classification
{{attack_surface_table — 5 categories with asset counts}}

### Defensive Posture
{{defense_matrix — 6 domains with evidence-based classifications}}

### Defense Impact on Techniques Matrix
{{technique_impact_matrix — techniques vs defenses}}

### Identified Quick Wins
{{quick_wins_table — targets with highest reward/risk ratio}}

### Preliminary Recommendation
{{top_3_vectors_ranked — with feasibility and risk assessment}}
```

### 7. Present MENU OPTIONS

"**Attack surface and defensive posture analysis complete.**

Summary: {{total_assets}} assets classified across 5 categories, {{defense_domains}} defensive domains analyzed.
Quick wins identified: {{quick_win_count}} | Top vector: {{top_vector}} | Overall defensive posture: {{overall_posture}}

**Select an option:**
[A] Advanced Elicitation — Deeper analysis of defensive posture gaps
[W] War Room — Red vs Blue discussion on the attack surface assessment
[C] Continue — Proceed to Technique Selection (Step 3 of 10)"

#### Menu Handling Logic:

- IF A: Deep-dive analysis of defensive posture gaps — challenge assumptions about defense classifications, explore edge cases in the impact matrix, identify potential false negatives in recon data that could affect surface analysis. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: which attack surface categories are most exploitable? What defensive blind spots are most dangerous? Blue Team perspective: are the defensive classifications fair? What additional controls might exist but not be visible from external recon? What would the SOC detect first? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-03-technique-selection.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and attack surface analysis appended to report], will you then read fully and follow: `./step-03-technique-selection.md` to begin technique selection.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- All 5 attack surface categories systematically analyzed with asset counts
- All 6 defensive domains assessed with evidence-based classifications
- Defense impact matrix cross-references techniques against controls
- Quick wins identified with reward-to-risk rationale
- Every classification includes source data reference from recon output
- Top 3 attack vectors ranked with feasibility justification
- `Unknown` used honestly where evidence is insufficient
- Findings appended to report under `## Attack Surface Analysis`
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted

### SYSTEM FAILURE:

- Classifying defensive posture without evidence from recon data
- Upgrading `Unknown` to `Weak` without supporting evidence
- Skipping credential leak analysis in attack surface classification
- Not cross-referencing defenses with TA0001 techniques in the impact matrix
- Performing active probing or exploitation during analysis
- Recording findings for out-of-scope assets
- Proceeding to technique selection without completing defensive analysis
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is ANALYSIS of existing data — no active testing. Every classification must have evidence.
