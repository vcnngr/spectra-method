# Step 4: C2 Infrastructure Preparation

**Progress: Step 4 of 10** — Next: Payload Development

## STEP GOAL:

Plan and document the command and control (C2) infrastructure required for the selected technique, including domains, redirectors, servers, communication profiles, and OPSEC controls. The infrastructure must be designed for resilience, stealth, and compliance with the rules of engagement.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER deploy infrastructure shared across engagements — cross-contamination is a legal risk
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INITIAL ACCESS SPECIALIST, not an autonomous infrastructure deployer
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Initial Access Specialist conducting authorized offensive operations
- ✅ Infrastructure planning must match the selected technique from step 3
- ✅ OPSEC is paramount — the infrastructure IS the operation's stealth layer
- ✅ Every component must be dedicated to this engagement and traceable

### Step-Specific Rules:

- 🎯 Focus exclusively on infrastructure planning and OPSEC design
- 🚫 FORBIDDEN to deploy, purchase, or configure live infrastructure — this is PLANNING and DOCUMENTATION
- 💬 Approach: Systematic infrastructure design matching technique requirements and OPSEC constraints
- 📊 Every component must include: purpose, protocol, provider recommendation, and OPSEC consideration
- 🔒 All infrastructure must be dedicated to this engagement — no shared resources

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Using shared infrastructure risks cross-engagement contamination — shared infrastructure means legal risk that can invalidate the entire assessment
  - Skipping domain reputation checks may lead to immediate detection — burned or blacklisted domains mean detection before the operation even begins
  - Configuring C2 without a target-specific communication profile makes generic C2 traffic easily identifiable by any competent SOC with traffic baseline
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present infrastructure requirements based on selected technique before detailed planning
- ⚠️ Present [A]/[W]/[C] menu after infrastructure plan complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, RoE, recon output, attack surface analysis, and selected techniques from steps 1-3
- Focus: Infrastructure planning and OPSEC design only — no live deployment or payload development
- Limits: Plan must align with selected primary technique and support fallback techniques where possible
- Dependencies: Technique selection (primary + fallbacks) from step-03-technique-selection.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Infrastructure Requirements per Technique

Based on the selected primary technique, define all required infrastructure components:

**For T1566 (Phishing) — Full infrastructure:**
- Sending domain + mail server (SMTP relay) for email delivery
- Landing page / credential harvesting server for spearphishing link
- Payload hosting server for spearphishing attachment
- C2 callback server for post-exploitation communication
- Redirectors: SMTP redirector (for email delivery) + HTTPS redirector (for callbacks)

**For T1190 (Exploit Public-Facing Application) — Reduced infrastructure:**
- C2 callback server for post-exploitation
- HTTPS redirector for callback obfuscation
- Staging server for webshell/payload delivery if needed

**For T1078/T1133 (Valid Accounts / External Remote Services) — Minimal infrastructure:**
- C2 callback server for post-access operations
- VPN/proxy chain for OPSEC during access
- Minimal infrastructure — access through target's legitimate channels

**For T1189 (Drive-by Compromise) — Web infrastructure:**
- Watering hole / exploit hosting server
- C2 callback server
- HTTPS redirector
- Domain with appropriate categorization

**Present requirements table for the selected primary technique:**
```
| Component | Role | Protocol | Recommended Provider | Status |
|-----------|------|----------|---------------------|--------|
| {{component}} | {{role}} | {{protocol}} | {{provider}} | To configure |
```

**Additional components for fallback support:**
- Document which infrastructure components are shared between primary and fallbacks
- Document which components need to be technique-specific

### 2. Domain Strategy

Plan the domain acquisition and configuration strategy:

**Domain Selection Criteria:**
- **Categorization**: domain must fall within non-suspicious categories (health, technology, business, finance — aligned with the target's sector)
- **Domain aging**: ideally 30+ days old, minimum 14 days — freshly registered domains are an immediate flag
- **TLD selection**: .com, .net, .org preferred — exotic TLDs (.xyz, .top) are more suspicious
- **Naming convention**: must appear plausible for the target's sector

**DNS Configuration for sending domains:**
- A record → mail server IP
- MX record → mail server hostname
- SPF record: `v=spf1 ip4:{{mail_server_ip}} -all`
- DKIM: generate keypair, publish TXT record
- DMARC: `v=DMARC1; p=quarantine; rua=mailto:{{report_email}}`

**SSL/TLS Configuration:**
- Let's Encrypt for automation (free, ACME)
- Purchased certificates for domains requiring specific categorization
- Wildcard where possible for flexibility

**Reputation Check Procedure:**
- VirusTotal domain lookup
- Google Safe Browsing check
- Sender Score (for sending domains)
- Domain categorization check (Bluecoat, Fortiguard, Palo Alto)
- MXToolbox blacklist check

**Present domain plan:**
```
| Domain | Purpose | Category | Age | SSL | Reputation | Status |
|--------|---------|----------|-----|-----|------------|--------|
| {{domain}} | Sending/C2/Redirect | {{category}} | {{age}} | ✅/❌ | Clean/Flagged/Unknown | To acquire/Available |
```

### 3. C2 Framework Selection

Evaluate and select the C2 framework based on engagement requirements and target environment:

**Framework Comparison Matrix:**
```
| Framework | Pros | Cons | Suited For |
|-----------|------|------|-----------|
| Cobalt Strike | Mature, malleable C2 profiles, teamserver, OPSEC features | Expensive, signatures heavily monitored by EDR | Enterprise targets with EDR — requires custom profiles |
| Sliver | Open source, implant diversity (HTTP/HTTPS/mTLS/DNS/WG), good OPSEC | Less mature, smaller community | Budget-conscious, diverse protocols, cost-constrained engagements |
| Mythic | Modular, multiple agents (Apollo, Poseidon, Medusa), modern UI | Complex setup, resource intensive | Multi-operator, long engagements, need for custom agents |
| Havoc | Modern, evasion-focused, Demon agent | Newer, less documentation | Targets with modern EDR, advanced evasion needs |
| Brute Ratel | Sleep obfuscation, syscall evasion, badger flexibility | Expensive, restrictive licensing | Targets with advanced enterprise EDR (CrowdStrike, SentinelOne) |
```

**For the selected framework, document:**
- **Framework chosen**: name and version
- **Justification**: why this framework for this engagement
- **Communication protocol**: HTTP / HTTPS / DNS / SMB / named pipes
- **Callback intervals**: sleep time + jitter percentage (e.g., 60s sleep, 20% jitter)
- **User-Agent**: configured to match target's legitimate traffic
- **Malleable Profile / Communication Profile**: key characteristics
  - URI patterns mimicking legitimate traffic (e.g., `/api/v2/status`, `/cdn/assets/`)
  - HTTP headers matching services used by the target
  - POST body encoding (base64, custom, encrypted)
  - Certificate pinning considerations

### 4. Redirector Architecture

Design the traffic flow architecture to protect the C2 server:

**Base Architecture:**
```
[Target Endpoint] → [Redirector Layer] → [C2 Server]
                          ↓ (non-matching traffic)
                    [Legitimate Site / 404]
```

**HTTPS Redirectors — Options:**
- Apache `mod_rewrite` with filtering rules
- Nginx reverse proxy with location matching
- Cloud functions (AWS Lambda, Azure Functions, GCP Cloud Functions)
- CDN-based (AWS CloudFront, Azure CDN) — hides C2 IP behind CDN

**SMTP Redirectors (for phishing delivery):**
- Postfix/sendmail relay with header manipulation
- Cloud email services (AWS SES, SendGrid) — note ToS and reputation concerns
- Dedicated SMTP relay on separate VPS

**DNS Redirectors (for DNS-based C2):**
- Authoritative DNS server as frontend
- DNS-over-HTTPS proxy for obfuscation

**Filtering Rules for redirector:**
- Block known sandbox and scanner user-agents (wget, curl, Python-urllib, sandbox UA)
- Geo-restriction: only traffic from target's country/region
- Time-based filtering: only during target's working hours
- Header validation: verify presence of expected headers
- TLS fingerprint: JA3/JA3S filtering to block automated tools
- Rate limiting: block anomalous connections

**Present architecture diagram:**
```
[Target] ─── HTTPS ──→ [CDN/Cloud Redirector] ─── HTTPS ──→ [C2 Server]
                              │
                              │ (non-matching traffic)
                              ▼
                        [Legitimate Website Clone]

[Target] ←── Email ──── [SMTP Redirector] ←── SMTP ──── [Mail Server]
                              │
                              │ (bounce/error)
                              ▼
                        [Null Route]
```

### 5. OPSEC Checklist

Verify operational security across all infrastructure components:

**Network Infrastructure:**
- [ ] VPN chain configured (no direct connection to operational infrastructure)
- [ ] Kill switch configured (emergency teardown procedure documented)
- [ ] DNS leak protection active on all operational connections

**Operational Isolation:**
- [ ] Dedicated VMs for the engagement (no personal accounts)
- [ ] Isolated browser profiles (no personal cookies, history, extensions)
- [ ] Dedicated SSH keys for engagement infrastructure
- [ ] Dedicated provider accounts (not traceable to other operations)

**Reputation and Detection:**
- [ ] No uploads to VirusTotal (use private scanners: antiscan.me, nodistribute)
- [ ] Domains/IPs not present in threat intelligence feeds
- [ ] Domain categorization verified on all major vendors
- [ ] SMTP reputation verified (Sender Score, blacklist check)

**Logging and Accountability:**
- [ ] Logging enabled on all infrastructure components
- [ ] Timestamps synchronized (NTP) for evidence chain
- [ ] Infrastructure configuration backup documented
- [ ] Evidence retention policy aligned with engagement terms

**Emergency Procedures:**
- [ ] Kill switch procedure: exact teardown sequence for each component
- [ ] Burn notice: procedure if infrastructure is compromised or identified
- [ ] Communication plan: how to notify the client in case of incident

### 6. Validation and Deployment Plan

Present the deployment timeline and action items:

**Deployment Plan:**
```
| Component | Required Action | Responsible | Deadline | Dependencies | Status |
|-----------|----------------|-------------|----------|--------------|--------|
| Domains | Purchase and DNS configuration | {{operator}} | D-14 | None | To do |
| SSL/TLS | Certificate generation | {{operator}} | D-13 | Domains registered | To do |
| C2 Server | Deploy and configure framework | {{operator}} | D-10 | None | To do |
| Redirectors | Deploy and configure rules | {{operator}} | D-7 | C2 server active | To do |
| Mail Server | SMTP configuration + auth records | {{operator}} | D-7 | Domains DNS ready | To do |
| Reputation | Verify reputation of all components | {{operator}} | D-3 | All deployed | To do |
| OPSEC | Execute complete checklist | {{operator}} | D-1 | All deployed | To do |
| E2E Test | End-to-end test of complete flow | {{operator}} | D-1 | All verified | To do |
```

**D-notation:** D = day of operation execution. D-14 = 14 days before execution.

**Pre-deployment Validation:**
- Connectivity test: C2 → redirector → C2 server
- Filtering test: verify redirector rules work (scanner blocking, geo-restrict)
- Reputation test: final scan of all domains/IPs
- Callback test: simulate callback from target's network range (if possible)
- Kill switch test: verify teardown procedure works

"**Infrastructure plan complete.**

Do you confirm the deployment plan? Any modifications to components, providers, or timeline?"

### 7. Present MENU OPTIONS

"**C2 infrastructure preparation complete.**

Planned components: {{component_count}} | C2 Framework: {{framework_name}}
Domains: {{domain_count}} | Redirectors: {{redirector_count}} | OPSEC checklist: {{checklist_status}}

**Select an option:**
[A] Advanced Elicitation — Challenge OPSEC assumptions and infrastructure resilience
[W] War Room — Red vs Blue discussion on C2 detection and infrastructure resilience
[C] Continue — Proceed to Payload Development (Step 5 of 10)"

#### Menu Handling Logic:

- IF A: Challenge OPSEC assumptions — stress-test the redirector filtering rules, question domain categorization longevity, explore what happens if a component is burned mid-operation, evaluate whether the callback profile truly blends with target traffic. Process insights, ask user if they want to update the plan, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: is the infrastructure resilient enough? What single point of failure exists? How quickly can we pivot if a component is burned? Blue Team perspective: what would a SOC look for to identify this C2? Which threat intel feeds would catch these domains? What JA3 fingerprints would the C2 framework produce? How would network monitoring detect the callback pattern? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-05-payload-dev.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and infrastructure plan appended to report], will you then read fully and follow: `./step-05-payload-dev.md` to begin payload development.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Infrastructure requirements mapped to selected technique from step 3
- All required components identified with role, protocol, and provider
- Domain strategy includes categorization, aging, DNS records, and reputation checks
- C2 framework selected with justified comparison against alternatives
- Communication profile designed to match target traffic patterns
- Redirector architecture designed with filtering rules documented
- OPSEC checklist completed with all items addressed
- Deployment timeline with dependencies and responsibilities documented
- Kill switch and emergency procedures defined
- Findings appended to report under `## C2 Infrastructure`
- Frontmatter updated with this step name added to stepsCompleted

### SYSTEM FAILURE:

- Using shared or non-dedicated infrastructure for the engagement
- Skipping domain reputation verification in the planning phase
- Designing C2 communication without a profile specific to the target environment
- No redirector layer between target and C2 server
- Incomplete OPSEC checklist with unaddressed items
- No kill switch or emergency teardown procedure
- Deploying, purchasing, or configuring live infrastructure in this step (this is PLANNING)
- Not linking infrastructure plan to the technique selected in step 3
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is PLANNING — no live deployment. Every component must be dedicated, documented, and OPSEC-verified.
