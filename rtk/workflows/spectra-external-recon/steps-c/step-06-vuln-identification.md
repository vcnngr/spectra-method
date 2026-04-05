# Step 6: Vulnerability Identification

**Progress: Step 6 of 10** — Next: Cloud and Infrastructure Enumeration

## STEP GOAL:

Identify potential vulnerabilities from all enumeration data collected in steps 2-5. This step correlates discovered services, versions, and configurations against known vulnerabilities (CVEs), misconfigurations, and security weaknesses — WITHOUT exploiting them.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER exploit vulnerabilities — identification and documentation only
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RECONNAISSANCE SPECIALIST performing vulnerability mapping
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Reconnaissance Specialist conducting authorized external reconnaissance
- ✅ Vulnerability identification is ANALYTICAL — correlate findings against known CVEs
- ✅ Some checks (SSL analysis, header analysis) send traffic — verify RoE compliance
- ✅ NEVER attempt proof-of-concept exploitation — only identify and document
- ✅ Rate findings by CVSS score and exploitability for prioritization

### Step-Specific Rules:

- 🎯 Focus on vulnerability correlation and security analysis
- 🚫 FORBIDDEN to run exploit code or attempt proof-of-concept
- 🚫 FORBIDDEN to attempt credential brute-forcing or default credential testing
- 💬 Approach: Systematic CVE correlation, misconfiguration checking, and security analysis
- 📊 Every vulnerability must include CVE reference (if applicable), CVSS score, and affected asset
- 🔒 Only assess vulnerabilities on in-scope assets

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Marking vulnerabilities as "confirmed" without supporting evidence — a vulnerability is only confirmed when corroborated by version data, CVE match, or observable misconfiguration
  - Skipping SSL/TLS analysis to save time — SSL/TLS weaknesses are among the most common and exploitable findings in external reconnaissance
  - Ignoring low-severity findings without documenting the decision and rationale — every finding must be recorded; triage is about prioritization, not omission
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present vulnerability assessment plan before beginning
- ⚠️ Present [A]/[W]/[C] menu after identification complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: All findings from steps 1-5 (scope, OSINT, subdomains, services, web apps)
- Focus: Vulnerability identification and correlation only — no exploitation
- Limits: Only assess in-scope assets with discovered service versions
- Dependencies: Service versions from step 4, technology stacks from step 5

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Compile Service Version Inventory

**Build assessment baseline from previous steps:**

From step 4 (Port & Service Discovery):
- All service name + version combinations
- Operating system versions

From step 5 (Web Enumeration):
- CMS versions (WordPress, Drupal, etc.)
- Framework versions (Spring, Laravel, etc.)
- JavaScript library versions
- Web server versions

"**Version Inventory for Vulnerability Analysis**

Services with identified version: {{versioned_service_count}}
Web applications with known stack: {{web_stack_count}}
Operating systems identified: {{os_count}}

Proceeding with CVE correlation and security analysis?"

### 2. CVE Correlation Against Discovered Services

**For each versioned service, search for known vulnerabilities:**

**CVE Lookup Sources:**
- NIST NVD (National Vulnerability Database)
- CVE Details / CVE.org
- Exploit-DB for public exploit availability
- Vulners.com for aggregated vulnerability data
- Vendor-specific security advisories

**For each service version:**
1. Search NVD for CVEs matching product + version
2. Filter by CVSS score >= 4.0 (Medium and above)
3. Check exploit availability (public exploit = higher risk)
4. Note if the vulnerability is in CISA KEV (Known Exploited Vulnerabilities)

**Document each vulnerability:**
```
| CVE ID | Service | Version | CVSS | Public Exploit | CISA KEV | Affected Assets |
|--------|---------|---------|------|----------------|----------|-----------------|
```

### 3. Known Misconfiguration Checking

**Check for common misconfigurations based on enumerated data:**

**Web Server Misconfigurations:**
- Directory listing enabled
- Server status/info pages exposed (Apache mod_status, Nginx status)
- Debug mode enabled (stack traces, verbose errors)
- Default installation pages present
- Backup files accessible (.bak, .old, .tmp, ~)

**Application Misconfigurations:**
- Exposed admin panels without IP restriction
- GraphQL introspection enabled in production
- Swagger/API documentation exposed in production
- CORS misconfiguration (Access-Control-Allow-Origin: *)
- Verbose error messages revealing internal paths

**Infrastructure Misconfigurations:**
- Open DNS resolver
- SNMP with default community strings (from UDP scan)
- Exposed management interfaces (Jenkins, Grafana without auth)
- Git repositories exposed (/.git/)
- Environment files exposed (/.env)

### 4. Default Credential Identification

**Identify services likely running with default credentials — do NOT attempt login:**

**Assessment approach (NO authentication attempts):**
- Check service version against known default credential databases
- Identify admin panels at default paths
- Note services with no visible authentication requirement
- Cross-reference with documentation for default accounts

**Common default credential scenarios:**
```
| Service | Path/Port | Known Default Account | Risk | Notes |
|---------|-----------|----------------------|------|-------|
```

**CRITICAL: Document for later exploitation phase — do NOT test now.**

### 5. SSL/TLS Configuration Analysis

**For each HTTPS service, analyze SSL/TLS security:**

**Tools:**
```bash
# testssl.sh for comprehensive analysis
testssl.sh --quiet --color 0 {{target}}:{{port}}

# sslscan for quick assessment
sslscan {{target}}:{{port}}

# nmap ssl scripts
nmap --script ssl-enum-ciphers,ssl-cert -p {{port}} {{target}}
```

**Check for:**
- Expired certificates
- Self-signed certificates
- Weak protocols (SSLv3, TLS 1.0, TLS 1.1)
- Weak cipher suites (RC4, DES, NULL, EXPORT)
- Known attacks: BEAST, POODLE, Heartbleed, ROBOT, DROWN
- Certificate chain issues (missing intermediates)
- Certificate CN/SAN mismatch
- HSTS not implemented or with short max-age
- Certificate pinning status

**Document per service:**
```
| Host:Port | Min Protocol | Weak Ciphers | SSL Vulnerabilities | Valid Certificate | HSTS |
|-----------|-------------|--------------|--------------------|--------------------|------|
```

### 6. Security Header Analysis

**For each web application, analyze HTTP security headers:**

**Headers to check:**
- `Strict-Transport-Security` (HSTS)
- `Content-Security-Policy` (CSP)
- `X-Frame-Options` / `frame-ancestors`
- `X-Content-Type-Options`
- `X-XSS-Protection` (legacy, but noted)
- `Referrer-Policy`
- `Permissions-Policy`
- `Cross-Origin-Opener-Policy` (COOP)
- `Cross-Origin-Resource-Policy` (CORP)
- `Cross-Origin-Embedder-Policy` (COEP)

**Rating per application:**
```
| Application | Headers Present | Headers Missing | Security Rating | Notes |
|-------------|----------------|-----------------|-----------------|-------|
```

### 7. Vulnerability Prioritization

**Prioritize all identified vulnerabilities:**

**Priority Matrix:**

| Priority | Criteria |
|----------|----------|
| CRITICAL | CVSS >= 9.0 OR public exploit + CISA KEV |
| HIGH | CVSS 7.0-8.9 OR public exploit available |
| MEDIUM | CVSS 4.0-6.9 OR misconfiguration with impact |
| LOW | CVSS < 4.0 OR informational findings |

**For each priority level, list:**
- Vulnerability count
- Most significant findings
- Affected assets
- Recommended exploitation order (for later phases)

### 8. Append Findings to Report

Write findings under `## Vulnerability Identification`:

```markdown
## Vulnerability Identification

### Summary
- CVE vulnerabilities identified: {{cve_count}}
- Misconfigurations: {{misconfig_count}}
- Services with known default credentials: {{default_cred_count}}
- SSL/TLS issues: {{ssl_issue_count}}
- Missing security headers: {{header_issue_count}}

### Distribution by Priority
- Critical: {{critical_count}}
- High: {{high_count}}
- Medium: {{medium_count}}
- Low: {{low_count}}

### CVE Vulnerabilities
{{cve_correlation_table}}

### Misconfigurations
{{misconfiguration_findings}}

### Default Credentials Identified
{{default_credential_table}}

### SSL/TLS Analysis
{{ssl_tls_analysis_table}}

### Security Header Analysis
{{security_header_table}}

### Priority Ranking
{{prioritized_vulnerability_list}}
```

Update frontmatter:
- `vulnerability_count` with total vulnerabilities identified
- `priority_targets.critical`, `.high`, `.medium`, `.low` with counts

### 9. Present MENU OPTIONS

"**Vulnerability identification complete.**

Summary: {{total_vuln_count}} vulnerabilities identified.
Critical: {{critical}} | High: {{high}} | Medium: {{medium}} | Low: {{low}}
CVE: {{cve_count}} | Misconfig: {{misconfig_count}} | SSL: {{ssl_count}} | Headers: {{header_count}}

**Select an option:**
[A] Advanced Elicitation — In-depth analysis of critical vulnerabilities
[W] War Room — Red vs Blue discussion on identified vulnerabilities
[C] Continue — Proceed to Cloud and Infrastructure Enumeration (Step 7 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — exploit chain potential (combining multiple vulns), lateral movement possibilities from external vulns, vulnerability age analysis (how long have these been exposed?). Redisplay menu
- IF W: War Room — Red: exploitation priority order? Which vulns enable initial access vs information gathering? Chaining potential? Blue: which CVEs should have been patched? Vulnerability management program assessment, compensating controls analysis. Summarize, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted and updating vulnerability_count and priority_targets, then read fully and follow: ./step-07-cloud-enum.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, vulnerability_count, and priority_targets updated], will you then read fully and follow: `./step-07-cloud-enum.md` to begin cloud and infrastructure enumeration.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Complete service version inventory compiled from previous steps
- CVE correlation performed for all versioned services
- Known misconfigurations checked systematically
- Default credential risks documented (without testing)
- SSL/TLS configuration analyzed for all HTTPS services
- Security headers analyzed for all web applications
- Vulnerabilities prioritized by CVSS and exploitability
- vulnerability_count and priority_targets updated in frontmatter

### ❌ SYSTEM FAILURE:

- Attempting ANY exploitation or proof-of-concept
- Testing default credentials against services
- Skipping CVE correlation for known service versions
- Not checking SSL/TLS configuration
- Not analyzing security headers
- Not prioritizing vulnerabilities by severity
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Identify, don't exploit.
