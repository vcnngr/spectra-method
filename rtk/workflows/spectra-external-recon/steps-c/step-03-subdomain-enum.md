# Step 3: Active Subdomain Enumeration

**Progress: Step 3 of 10** — Next: Port and Service Discovery

## STEP GOAL:

Comprehensive subdomain discovery through active enumeration techniques. This step builds on the passive subdomain findings from Step 2 by adding DNS brute-forcing, active certificate analysis, virtual host discovery, and validation of all discovered subdomains.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER enumerate subdomains outside the authorized scope
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RECONNAISSANCE SPECIALIST, not an autonomous scanner
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Reconnaissance Specialist conducting authorized external reconnaissance
- ✅ Active enumeration sends traffic to DNS infrastructure — verify RoE allows this
- ✅ Respect rate limits defined in engagement RoE
- ✅ Document every technique used for reproducibility and detection analysis

### Step-Specific Rules:

- 🎯 Focus on comprehensive subdomain discovery and validation
- 🚫 FORBIDDEN to perform port scanning or service enumeration (that's step 4)
- 💬 Approach: Systematic enumeration with multiple complementary techniques
- 📊 Merge results with passive findings from step 2 — deduplicate
- 🔒 Check RoE for DNS enumeration rate limits before beginning

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers). This is the ONLY action the agent refuses. Note: in recon context, destructive actions are unlikely but the principle stands.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Brute-forcing with aggressive wordlists without confirming the RoE explicitly allows it — aggressive DNS enumeration can trigger alerts and violate RoE
  - Skipping wildcard detection before brute-forcing — wildcard DNS causes massive false positives downstream that corrupt the entire target inventory
  - Enumerating domains not listed in the authorized scope — out-of-scope enumeration is unauthorized reconnaissance regardless of intent
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your enumeration plan before beginning active techniques
- ⚠️ Present [A]/[W]/[C] menu after enumeration complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Scope and passive OSINT findings from steps 1-2 are in memory
- Focus: Subdomain enumeration only — no port scanning or web app testing
- Limits: Only enumerate subdomains of in-scope root domains
- Dependencies: Passive subdomain list from step-02-passive-osint.md serves as baseline

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Review Passive Baseline and RoE

Before active enumeration, establish context:

**Review passive subdomain findings from Step 2:**
- Count of subdomains already discovered passively
- Identify gaps in passive coverage (domains with few passive results)

**Review RoE constraints for active enumeration:**
- DNS query rate limits
- Time-of-day restrictions
- Required notification before active scanning

"**Active Subdomain Enumeration Plan**

Passive baseline: {{passive_subdomain_count}} subdomains already identified
In-scope root domains: {{domain_list}}

Planned techniques:
1. DNS brute-force with curated wordlists
2. Active Certificate Transparency analysis
3. Virtual host discovery
4. Wildcard DNS detection
5. Validation and resolution of all subdomains

RoE — DNS rate limit: {{rate_limit}}
RoE — Time restrictions: {{time_restrictions}}

Would you like to proceed with the full plan?"

### 2. Wildcard Detection

**Before brute-forcing, check for wildcard DNS:**

For each in-scope root domain:
- Query a random, non-existent subdomain (e.g., `asdkjh2398sdf.{{domain}}`)
- If it resolves: wildcard DNS is active
- Document wildcard behavior (what IP/CNAME it resolves to)
- Adjust brute-force strategy to filter wildcard responses

"**Wildcard Detection:**
{{for each domain}}
- `{{domain}}`: {{wildcard_detected ? 'Wildcard ACTIVE — filter enabled' : 'No wildcard detected'}}"

### 3. DNS Brute-Force Enumeration

**Wordlist-based subdomain discovery:**

Recommended approach and tools:
- **Wordlists:** SecLists DNS wordlists, Assetnote wordlists, custom industry-specific wordlists
- **Tools:** `gobuster dns`, `ffuf`, `amass enum -brute`, `puredns`
- **Strategy:** Start with common subdomains (top 1000), then expand to comprehensive lists

**Common high-value subdomain patterns to enumerate:**
```
www, mail, ftp, vpn, remote, dev, staging, test, api, admin,
portal, webmail, owa, autodiscover, cpanel, whm, ns1, ns2,
mx, smtp, pop, imap, db, database, sql, backup, git, svn,
jenkins, jira, confluence, wiki, docs, cdn, assets, static,
monitoring, grafana, kibana, elastic, prometheus, sentry,
vault, pki, ca, ldap, ad, dc, sso, auth, login, id
```

**For each valid result:**
- Record subdomain, resolved IP, CNAME chain if applicable
- Check if IP falls within in-scope network ranges
- Flag subdomains resolving to cloud providers (AWS, Azure, GCP)

### 4. Active Certificate Transparency Analysis

**Deeper CT log analysis beyond passive step 2:**

- Query multiple CT log aggregators in real-time
- Cross-reference with Censys certificate search
- Identify recently issued certificates (indicates active infrastructure)
- Look for internal/staging subdomains exposed in certificate SANs
- Identify certificate patterns (issuer, validity periods, key sizes)

### 5. Virtual Host Discovery

**Identify subdomains sharing IP addresses:**

- Group all resolved IPs from discovered subdomains
- For shared IPs, probe for virtual host routing differences
- Use Host header manipulation to discover hidden vhosts
- Tools: `gobuster vhost`, `ffuf` with Host header fuzzing

**Document vhost mapping:**
```
| IP | Hosted Subdomains | Provider | Notes |
|----|-------------------|----------|-------|
```

### 6. Subdomain Validation and Resolution

**Validate ALL discovered subdomains (passive + active):**

For each unique subdomain:
- DNS resolution check (A, AAAA, CNAME records)
- HTTP/HTTPS reachability probe (status code only, no deep crawling)
- Classify status: `alive`, `dead`, `redirect`, `filtered`
- Identify subdomain takeover candidates (CNAME pointing to unclaimed resources)

**Subdomain Takeover Check:**
- CNAME to decommissioned cloud services (S3, Azure, Heroku, GitHub Pages)
- NXDOMAIN responses with dangling CNAME records
- Services with expired registrations

### 7. Consolidate and Deduplicate

**Merge passive (step 2) and active findings:**

**Master Subdomain Table:**
```
| Subdomain | IP | Record Type | Status | Source | Takeover Risk |
|-----------|-----|------------|--------|--------|--------------|
```

**Statistics:**
- Total unique subdomains: {{total}} ({{passive_count}} passive + {{active_new}} new from active)
- Live subdomains: {{alive_count}}
- Potential takeover candidates: {{takeover_count}}
- Cloud-hosted subdomains: {{cloud_count}}
- Subdomains with virtual hosting: {{vhost_count}}

### 8. Append Findings to Report

Write consolidated subdomain findings to the output document under `## Subdomain Enumeration`:

```markdown
## Subdomain Enumeration

### Summary
- Total unique subdomains: {{total}}
- Live subdomains: {{alive_count}}
- New from active enumeration: {{active_new_count}}
- Subdomain takeover candidates: {{takeover_count}}
- Wildcard DNS detected: {{wildcard_domains}}

### Wildcard Detection
{{wildcard_findings}}

### Master Subdomain Table
{{master_subdomain_table}}

### Subdomain Takeover Candidates
{{takeover_candidates}}

### Virtual Host Mapping
{{vhost_mapping}}

### Infrastructure Distribution
{{infrastructure_distribution — cloud vs on-prem breakdown}}
```

Update frontmatter `target_count` with total unique live subdomains/IPs.

### 9. Present MENU OPTIONS

"**Subdomain enumeration complete.**

Summary: {{total_unique}} unique subdomains found ({{alive_count}} live).
New from active: {{active_new}} | Takeover candidates: {{takeover_count}} | Wildcard: {{wildcard_domains}}

**Select an option:**
[A] Advanced Elicitation — Push deeper on subdomain patterns
[W] War Room — Launch multi-agent adversarial discussion on subdomain attack surface
[C] Continue — Save and proceed to Port and Service Discovery (Step 4 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — naming convention patterns, infrastructure topology inference, subdomain age analysis, potential shadow IT identification. Process insights, ask user if they want to update findings, redisplay menu
- IF W: War Room — Red: which subdomains are the most promising attack vectors? Subdomain takeover exploitation value? Blue: subdomain sprawl monitoring recommendations, DNS monitoring rules. Summarize, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating target_count, then read fully and follow: ./step-04-port-scanning.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and subdomain findings appended to report], will you then read fully and follow: `./step-04-port-scanning.md` to begin port and service discovery.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Wildcard DNS detected and handled before brute-forcing
- DNS brute-force performed with appropriate wordlists
- Active CT log analysis adds findings beyond passive step
- Virtual host discovery maps IP-to-subdomain relationships
- All subdomains validated (alive/dead/redirect/filtered)
- Subdomain takeover candidates identified and documented
- Passive and active findings merged and deduplicated
- Findings appended to report with proper structure
- target_count updated in frontmatter

### ❌ SYSTEM FAILURE:

- Enumerating subdomains outside authorized scope
- Performing port scanning or service enumeration (that's step 4)
- Not checking for wildcard DNS before brute-forcing
- Not merging with passive findings from step 2
- Not validating discovered subdomains for liveness
- Missing subdomain takeover candidate detection
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Subdomain enumeration only — no port scanning.
