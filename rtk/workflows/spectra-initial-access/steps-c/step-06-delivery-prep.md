# Step 6: Delivery and Pretext Preparation

**Progress: Step 6 of 10** — Next: Pre-Execution RoE Gate

## STEP GOAL:

Prepare the complete delivery mechanism for the selected technique: pretext for social engineering, exploit chain for technical attack, or access procedure for credential-based, with optimized timing and targeting. At the end of this step, the entire operation must be ready for execution — only the final RoE verification remains.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER send phishing to targets outside the authorized scope — every recipient must be in the RoE
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INITIAL ACCESS SPECIALIST preparing authorized delivery mechanisms
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Initial Access Specialist conducting authorized offensive operations
- ✅ Delivery preparation transforms payloads into operational attack chains
- ✅ Social engineering pretexts must be credible but never cause emotional distress
- ✅ Every target must be verified against the authorized scope before inclusion
- ✅ A dry run validates the entire chain before live execution

### Step-Specific Rules:

- 🎯 Focus on delivery mechanism preparation, pretext design, targeting, and timing
- 🚫 FORBIDDEN to execute the delivery — this step is preparation only
- 🚫 FORBIDDEN to create pretexts that cause emotional distress or harm
- 💬 Approach: Build the complete operational package, verify every component, dry run
- 📊 Every target must include: identity, scope authorization, delivery method, and risk level
- 🔒 Only target entities explicitly authorized in the engagement RoE

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Pretexts causing emotional distress (fake firings, medical emergencies, false legal threats) may damage client relationships and raise ethical concerns — effective pretexts exploit work routines, not fears
  - Targeting people not in documented scope may have legal implications — every recipient must be explicitly authorized in the RoE
  - Untested exploits may crash production systems, causing denial of service or data corruption with legal and reputational consequences
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present delivery preparation plan before beginning
- ⚠️ Present [A]/[W]/[C] menu after preparation complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Selected technique, C2 infrastructure, developed payloads, defensive posture, attack surface, scope and RoE
- Focus: Delivery mechanism preparation, pretext design, targeting optimization, timing analysis
- Limits: Preparation only — do NOT execute delivery in this step
- Dependencies: Payloads from step-05, C2 infrastructure from step-04, technique from step-03, defenses from step-02

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Delivery Strategy per Technique

**Branch by `technique_selected.primary` to prepare the appropriate delivery mechanism:**

**T1566 (Phishing) — Social Engineering Delivery:**

**Email Design:**
- Subject line: target-specific, calibrated urgency (high for immediate action, medium for action within 24h)
- Body: professional tone, consistent with the selected pretext, no grammatical errors
- Sender persona: name, title, email address, full signature
- Call to action: clear and singular — one link or one attachment, never both

**Pretext Development — Select a credible scenario for the target's industry:**
- IT notification: password expiry, mandatory MFA configuration, system update
- Business context: invoice, contract, shipment confirmation, meeting invitation
- HR/corporate: benefit enrollment, policy update, mandatory training
- External: vendor communication, conference invitation, partnership request

**Sender Persona Construction:**
- Name and title consistent with the pretext (IT helpdesk, HR, external vendor)
- Email address: from controlled domain in step 4, similar to legitimate domain
- Professional email signature with name, title, phone, disclaimer
- Consistent LinkedIn presence (if pretext requires social validation)

**Landing Page (if link-based):**
- Clone of the legitimate page or custom industry-appropriate page
- Valid SSL on controlled domain
- URL construction: credible path, no suspicious visible parameters
- Credential harvesting with complete logging

**Attachment (if attachment-based):**
- Filename consistent with the pretext (e.g., "Invoice_Q4_2026.xlsx", not "payload.exe")
- Appropriate icon for the simulated file type
- Metadata cleaning: remove author, creation dates, comments, revision history
- Verify that the attachment passes the email gateway identified in step 2

**Document email template:**
```
From: {{sender_name}} <{{sender_email}}>
To: {{target_email}}
Subject: {{subject}}

{{body}}

{{signature}}
```

**T1190 (Exploit Public-Facing Application) — Technical Delivery:**

**Exploit Chain Validation:**
- Exploitation sequence documented step by step
- Each step with expected input, expected output, and success/failure indicators
- Timeout for each step — if not completed within the timeout, abort
- Exploit tested in lab environment matching the target configuration

**Rollback Procedure:**
- Procedure to restore the service if the exploit causes instability
- Specific commands for each failure scenario
- Emergency contact if the service does not restore

**Post-Exploit Immediate Actions:**
- Deploy C2 agent within 60 seconds of exploitation
- Establish persistence hook as the first post-access action
- Collect system info to confirm the target

**T1078/T1133 (Valid Accounts / External Remote Services) — Credential Delivery:**

**Credential Validation Procedure:**
- Test without triggering account lockout: verify lockout threshold from RoE or step 2 analysis
- Sequence: try 1 credential at a time, wait interval between attempts
- Validation with low-risk method: web portal > VPN > RDP > SSH (in order of stealth)

**Access Method Configuration:**
- VPN client configured with credentials ready
- Web portal URL and access procedure documented
- RDP/SSH connection string prepared
- Proxy chain configured for OPSEC (VPN → clean IP → target)

**Post-Authentication First Actions:**
- Deploy C2 agent as the first action after authentication
- Situational awareness: whoami, ipconfig, systeminfo, net group
- Scope verification: confirm that the accessed system is in-scope
- Enable local logging for evidence chain

### 2. Targeting Optimization

**Select and prioritize specific targets for the operation:**

**For Phishing:**
- Target list with: name, email, role, department, likelihood of interaction with the pretext
- Prioritize targets with privileged access (IT admin, finance, C-suite)
- Avoid targets with recent security awareness training (if known from OSINT)
- Sequencing: high-probability targets first, low-risk fallback after

**For Exploitation:**
- Target hosts with: IP, service, version, CVE, confidence of exploit success
- Prioritize targets with vulnerable service + no WAF
- Avoid high-visibility targets (e.g., main homepage) — prefer secondary services

**For Credentials:**
- Account list with: username, credential source (breach, OSINT, spray), validation status
- Prioritize accounts with VPN/RDP access + credentials from recent breach
- Avoid service accounts or admin accounts with elevated monitoring (if indicated by recon)

**Present targeting matrix:**
```
| # | Target | Type | Method | Success Probability | Detection Risk | Priority |
|---|--------|------|--------|---------------------|----------------|----------|
```

### 3. Timing Analysis

**Determine optimal execution window:**

**Timezone and Business Hours:**
- Target timezone from engagement.yaml and OSINT
- Standard business hours of the target (local culture, industry norms)
- Operator timezone vs target — calculate offset

**Optimal Window:**
- Phishing: Tuesday-Thursday, 9-11 AM target local time (peak email activity)
- Exploitation: outside business hours (less human monitoring) OR during business hours (more legitimate noise)
- Credentials: business hours (legitimate logins mask the attempt)

**Elements to Avoid:**
- National and local holidays of the target
- Known corporate events (earnings calls, all-hands, conferences)
- Scheduled maintenance windows (elevated IT visibility)
- Blackout periods defined in the RoE

**RoE Restrictions:**
- Verify authorized time windows in engagement.yaml
- Coordinate with internal contacts (if assumed breach scenario)
- Pre-execution notifications required by the RoE

**Delivery timeline:**
```
| Phase | When | Action | Notes |
|-------|------|--------|-------|
| Pre-execution | T-{{hours}} | Verify infrastructure, warm-up redirector | |
| Wave 1 | T+0 | Delivery to primary targets ({{count}} targets) | |
| Monitoring | T+0 → T+{{hours}} | Monitor callbacks, detection events | |
| Wave 2 (if needed) | T+{{hours}} | Delivery to secondary targets | Only if Wave 1 does not generate callback |
| Abort window | T+{{hours}} | Go/no-go decision for continuation | |
```

### 4. Pre-Flight Checklist

**Verify every operational component before proceeding to RoE Gate:**

**Payload Readiness:**
- [ ] Primary payload tested and functional (from step 5)
- [ ] Backup payload tested and functional (from step 5)
- [ ] Kill date set on all payloads
- [ ] Hashes recorded for tracking

**Infrastructure Readiness:**
- [ ] C2 framework operational and listening (from step 4)
- [ ] Redirector chain functional (traffic routing verified)
- [ ] Domains resolving correctly (DNS propagated)
- [ ] Valid SSL on all delivery domains
- [ ] Payload hosting accessible through the complete chain

**Delivery Readiness:**
- [ ] Email template prepared and verified (for phishing)
- [ ] Exploit chain validated in test environment (for exploitation)
- [ ] Credentials ready and procedure documented (for credential-based)
- [ ] Pretext coherent and credible
- [ ] Attachment metadata cleaned

**OPSEC Readiness:**
- [ ] VPN active on clean node (no personal IPs)
- [ ] Isolated VM for operations (no personal accounts logged in)
- [ ] Dedicated browser/tools without personal extensions
- [ ] DNS leak test completed

**Operational Readiness:**
- [ ] Logging enabled on all components (C2, redirector, hosting)
- [ ] Emergency procedures documented (abort, deconfliction, notification)
- [ ] Rollback plan prepared for each failure scenario
- [ ] Target list finalized and verified in-scope
- [ ] Timeline defined with abort windows

**If ANY check fails: DOCUMENT and RESOLVE before proceeding.**

### 5. Dry Run

**Validate the complete chain end-to-end — if possible:**

**For Phishing:**
- Send test email to internal control account (not to the target)
- Verify: email delivery → correct rendering → functional link/attachment → landing page/payload → C2 callback
- Check: email does not end up in spam, HTML renders correctly, links not rewritten unexpectedly
- Measure: time from click to C2 callback

**For Exploitation:**
- Execute exploit chain on lab replica of target environment
- Verify: connection → exploit → code execution → C2 callback
- Check: no service crash, no unexpected visible artifacts
- Measure: time from trigger to C2 callback

**For Credentials:**
- Test access procedure on non-production service (if available)
- Verify: authentication → access → C2 deploy → callback
- Check: no lockout triggered, no visible alert
- Measure: time from login to operational C2

**Document dry run results:**
```
| Phase | Expected Result | Observed Result | Time | Pass/Fail |
|-------|-----------------|-----------------|------|-----------|
```

**If the dry run fails:** identify the break point, fix, and re-execute. Do NOT proceed with a failed dry run.

### 6. Append Findings to Report

Write findings under `## Delivery Preparation`:

```markdown
## Delivery Preparation

### Summary
- Delivery method: {{delivery_method}}
- Technique: {{technique}} ({{tcode}})
- Selected targets: {{target_count}}
- Execution window: {{execution_window}}
- Dry run: {{pass/fail}}
- Pre-flight: {{passed_count}}/{{total_count}} checks passed

### Delivery Strategy
{{delivery_strategy_details}}

### Pretext / Exploit Chain / Access Procedure
{{technique_specific_delivery_details}}

### Target List
{{targeting_matrix}}

### Execution Timeline
{{delivery_timeline}}

### Pre-Flight Checklist
{{preflight_results}}

### Dry Run Results
{{dry_run_results}}
```

Update frontmatter:
- `delivery_method` with delivery mechanism type

### 7. Present MENU OPTIONS

"**Delivery preparation completed.**

Summary: {{delivery_method}} method prepared for {{target_count}} targets.
Pretext: {{pretext_summary}} | Timing: {{timing_window}} | Dry run: {{dry_run_status}}
Pre-flight: {{passed}}/{{total}} checks passed | Infrastructure: operational

**Select an option:**
[A] Advanced Elicitation — In-depth analysis of pretext credibility and interaction probability
[W] War Room — Red (delivery effectiveness, pretext realism) vs Blue (delivery detection probability, suspicious indicators)
[C] Continue — Proceed to Pre-Execution RoE Gate (Step 7 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge pretext credibility against target demographic, question timing assumptions against target behavior patterns, evaluate delivery mechanism against email gateway/WAF capabilities, identify weak points in the delivery chain. Process insights, ask user if they want to refine the delivery plan, if yes update and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: pretext realism assessment, target interaction probability, delivery chain reliability, what could go wrong? Blue Team perspective: email gateway detection probability, URL/attachment reputation scoring, SOC alert triggers from this delivery method, user reporting likelihood. Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted and updating delivery_method, then read fully and follow: ./step-07-roe-gate.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and delivery_method updated and Delivery Preparation section populated], will you then read fully and follow: `./step-07-roe-gate.md` to begin RoE gate verification.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Delivery strategy fully defined for selected technique with all components prepared
- Pretext developed without harmful or distressing content (for phishing)
- Exploit chain validated in test environment (for exploitation)
- Credential procedure documented with lockout avoidance (for credential-based)
- Targeting matrix built with every target verified against authorized scope
- Timing analysis completed with optimal execution window identified
- Pre-flight checklist completed with all checks passing
- Dry run executed successfully validating entire chain end-to-end
- delivery_method updated in frontmatter
- Findings appended to report under `## Delivery Preparation`

### ❌ SYSTEM FAILURE:

- Creating pretexts that cause emotional distress (fake firings, medical emergencies, legal threats)
- Including targets outside the authorized engagement scope
- Skipping exploit validation in test environment before production use
- Executing delivery in this step — this is preparation only
- Proceeding with failed pre-flight checks without resolution
- Proceeding with failed dry run without fixing the chain
- Not documenting the complete delivery plan for evidence chain
- Not building a timeline with abort windows
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Prepare everything, execute nothing — the RoE gate is next.
