# Step 4: Containment Strategy & Execution

**Progress: Step 4 of 10** — Next: Evidence Preservation & Chain of Custody

## STEP GOAL:

Develop and execute the containment strategy based on incident severity and scope, balancing the need to stop the attack with the need to preserve evidence and minimize business disruption. Containment is the first active intervention — every action must be deliberate, documented, and reversible where possible.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute containment actions without operator approval for each action
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator managing an active security incident under NIST 800-61
- ✅ Containment is the critical inflection point — it shifts the incident from passive analysis to active intervention, and every action has consequences
- ✅ Every containment action must be documented with timestamp, executor, verification, and rollback procedure — this is the audit trail for post-incident review and potential legal proceedings
- ✅ The order of containment actions matters — volatile evidence must be captured BEFORE isolation cuts access to it
- ✅ Containment does not mean eradication — the goal is to stop the bleeding and stabilize, not to remediate

### Step-Specific Rules:

- 🎯 Focus exclusively on containment strategy development, risk assessment, pre-containment evidence capture, execution planning, and containment verification
- 🚫 FORBIDDEN to begin eradication (malware removal, persistence cleanup) — that is step 7
- 🚫 FORBIDDEN to begin recovery (system restoration, service re-enablement) — that is step 8
- 🚫 FORBIDDEN to skip pre-containment evidence capture — volatile evidence destroyed by containment is gone permanently
- 💬 Approach: Systematic strategy-then-execute with operator approval at each phase
- 📊 Every containment action must include: target, action, business impact, reversibility, priority, executor, and verification method
- 🔒 All containment actions must be within the scope authorized by the engagement and Rules of Engagement

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Executing containment without pre-capturing volatile evidence (memory, connections) destroys forensic data permanently — RAM contents, active network sessions, running processes, and loaded modules are lost the moment a system is isolated or powered down, and this data is often the most valuable for root cause analysis and attribution
  - Network isolation of a domain controller or critical infrastructure without coordination may cause cascading failures exceeding the incident impact — Active Directory authentication, DNS resolution, Group Policy processing, and Kerberos ticket granting all depend on DC availability, and isolating one without promoting or redirecting services can lock out the entire organization
  - Alerting the attacker through visible containment actions (account lockouts, DNS changes) may trigger destructive failsafes or accelerate data exfiltration — sophisticated adversaries monitor for incident response indicators and may have dead-man switches, automated exfiltration acceleration, or destructive payloads that activate when they detect containment
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present containment strategy as a structured decision matrix before any execution
- ⚠️ Capture volatile evidence BEFORE executing any containment action that affects system state
- 📋 Document every containment action with timestamp, executor, and verification result
- ⚠️ Present [A]/[W]/[C] menu after containment verification is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `containment_status`, `containment_strategy`, and `containment_timestamp`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, incident classification and severity from steps 1-3, affected systems inventory, affected users inventory, IOC data, MITRE ATT&CK mapping, triage severity assessment, notification matrix
- Focus: Containment strategy selection, risk assessment, pre-containment evidence capture, execution planning, and verification — no eradication, no recovery
- Limits: Only execute containment actions authorized within the engagement scope and Rules of Engagement — if the engagement restricts certain containment actions (e.g., no production shutdowns), those restrictions must be honored
- Dependencies: Completed triage and severity classification from step-03-triage.md, affected systems and users identified, IOCs extracted

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Containment Strategy Selection

Based on the severity classification from step 3 and the scope of affected systems, develop a two-phase containment strategy covering both immediate stabilization and sustained containment during the investigation.

**Short-term Containment** (stop the bleeding NOW — immediate actions to halt active attack progression):

**Network Isolation:**
- Disconnect affected systems from the network using the least disruptive method available
- VLAN isolation: move affected hosts to a quarantine VLAN with no outbound internet and restricted internal access — preserves ability to communicate with forensic tools
- Firewall rules: block all traffic to/from known malicious IPs, C2 domains, and attacker infrastructure at the perimeter and internal segment boundaries
- Switch port shutdown: physical port disable for systems requiring hard isolation — most disruptive, use only when VLAN isolation is insufficient
- Wireless isolation: disable Wi-Fi profiles on affected endpoints, block MAC addresses at wireless controller
- For each isolation method, note: what connectivity remains (forensic access, management network), what is severed (internet, internal LAN, specific segments)

**Account Lockout:**
- Disable compromised user accounts in Active Directory / Identity Provider immediately
- Force password reset for all accounts showing suspicious authentication activity
- Revoke OAuth tokens, API keys, and application-specific passwords associated with compromised accounts
- Disable mail forwarding rules, inbox rules, and delegated access added during the incident
- Review and revoke any recently granted permissions or group memberships
- For service accounts: assess operational impact before disabling — document which services depend on each account

**DNS Sinkhole:**
- Redirect known C2 domains to an internal sinkhole server
- Configure sinkhole to log all connection attempts (source IP, timestamp, requested domain) — this identifies additional compromised systems attempting C2 callback
- Update internal DNS resolvers with sinkhole entries
- If using split-horizon DNS: ensure sinkhole applies to both internal and external resolution paths
- Monitor sinkhole logs in real-time during the containment window

**Email Quarantine:**
- Block sender addresses and domains associated with the phishing or delivery vector
- Quarantine all delivered messages matching the attack indicators (subject line, sender, attachment hash, URL pattern)
- Search for and disable any mail rules created by the attacker (auto-forward, auto-delete, move-to-folder rules)
- Block attachment types used in the delivery vector at the email gateway (if not already blocked)
- Notify affected recipients that the quarantined messages are part of an active incident

**Endpoint Isolation:**
- Initiate EDR containment on affected endpoints (CrowdStrike Falcon network containment, Microsoft Defender isolation, SentinelOne network quarantine, Carbon Black device quarantine)
- EDR containment preserves the ability to run remote forensic commands while blocking all network traffic except the EDR management channel
- Verify EDR containment is active by confirming the endpoint cannot reach external or internal hosts
- If EDR is not deployed on the affected system: fall back to VLAN isolation or firewall rules
- Document the EDR containment method used and any limitations (e.g., can the endpoint still reach the management network?)

**Long-term Containment** (sustainable posture while investigation continues):

**Network Segmentation:**
- Implement micro-segmentation around the affected network zone using existing firewall/SDN infrastructure
- Define explicit allow rules for required business traffic and deny all else (zero-trust containment)
- Deploy network monitoring (SPAN/TAP, packet capture) on the containment boundary to detect any breakout attempts
- Review and tighten existing firewall rules between the affected zone and critical assets (databases, file shares, domain controllers)
- Document the segmentation topology for the incident report

**Enhanced Monitoring:**
- Deploy additional logging on systems adjacent to the affected zone — these are the next likely targets for lateral movement
- Enable verbose logging on authentication systems (domain controllers, RADIUS, SSO) for the incident duration
- Configure packet capture on key network segments (DMZ, server VLAN, management network) to capture any ongoing attacker activity
- Enable PowerShell script block logging and module logging on Windows endpoints in the affected zone
- Increase SIEM alert sensitivity for the affected zone — lower thresholds, add temporary detection rules

**Credential Rotation:**
- Reset passwords for all accounts in the affected scope — not just confirmed compromised accounts, but all accounts that could have been exposed
- Rotate service account credentials for services in the affected zone — coordinate with application owners to avoid service disruption
- Rotate Kerberos KRBTGT password (double rotation per Microsoft guidance) if Golden Ticket or domain-level compromise is suspected
- Revoke and reissue certificates if certificate-based authentication was compromised
- Rotate API keys, secrets, and tokens for cloud services accessed from affected systems

**Access Controls:**
- Implement additional MFA requirements for access to sensitive systems from any location
- Enable conditional access policies: block access from untrusted locations, require compliant devices, restrict legacy authentication protocols
- Restrict remote access (VPN, RDP, SSH) to named accounts with enhanced logging
- Disable any emergency or break-glass accounts that may have been discovered by the attacker
- Review and tighten privileged access management (PAM) policies for the incident duration

**Temporary Mitigations:**
- Deploy WAF rules to block the specific exploit patterns observed
- Update IDS/IPS signatures with IOCs from the incident (file hashes, network patterns, user-agent strings)
- Create custom YARA rules for identified malware and deploy to endpoint scanning
- Create custom Sigma rules for identified attack patterns and deploy to SIEM
- Block known attacker infrastructure at the web proxy (URLs, domains, IP ranges)

**Present as containment decision matrix:**

```
| # | Action | Type | Target | Business Impact | Reversibility | Evidence Impact | Priority | Executor |
|---|--------|------|--------|-----------------|---------------|-----------------|----------|----------|
| 1 | {{action}} | Short-term / Long-term | {{system/account/zone}} | {{Low/Med/High}} | {{Reversible/Partial/Irreversible}} | {{None/Low/High}} | {{P1/P2/P3}} | {{role}} |
```

### 2. Containment Risk Assessment

For each proposed containment action from the decision matrix, evaluate the risk-benefit tradeoff. Containment is not risk-free — every action has consequences that must be weighed.

**Risk-Benefit Matrix — evaluate per action:**

**Business Impact Assessment:**
- Service disruption: which services will be affected, for how long, and how many users impacted?
- User impact: will users lose access to systems, applications, or data? Can they work with alternative methods?
- Revenue impact: does this containment action affect revenue-generating systems or customer-facing services?
- Regulatory impact: does isolating this system affect compliance obligations (e.g., logging, audit trails, data retention)?
- SLA impact: will any contractual SLAs be breached by this action?

**Evidence Impact Assessment:**
- Will this action destroy volatile evidence (RAM, active sessions, running processes)?
- Will this action modify file system timestamps or log entries?
- Will this action trigger automatic cleanup processes (temp file deletion, log rotation)?
- Is the evidence on this system already captured, or must capture happen before this action?
- Rate evidence impact: None (evidence unaffected), Low (minor metadata changes), High (volatile evidence destroyed)

**Attacker Awareness Assessment:**
- Will this action be visible to the attacker (e.g., account lockout notification, DNS failure on C2 callback)?
- If the attacker detects containment, what is their likely response? (escalate, go quiet, destroy evidence, trigger failsafe)
- Can this action be executed covertly (e.g., firewall block vs. account lockout)?
- Is there a timing advantage to executing multiple containment actions simultaneously to deny the attacker reaction time?

**Reversibility Assessment:**
- Can this action be undone if it was based on incorrect analysis?
- What is the rollback procedure and how long does it take?
- Are there any irreversible side effects (e.g., Kerberos tickets invalidated, sessions terminated)?

**Dependency Assessment:**
- Does this action require change management approval?
- Does this action require coordination with external parties (ISP, cloud provider, third-party vendor)?
- Does this action depend on another containment action being executed first?
- Does this action require downtime notification to stakeholders?

**Present as risk-benefit matrix:**

```
| # | Action | Business Impact | Evidence Impact | Attacker Awareness | Reversibility | Dependencies | Risk-Benefit Verdict |
|---|--------|-----------------|-----------------|--------------------|----|---------------|---------------------|
| 1 | {{action}} | {{assessment}} | {{None/Low/High}} | {{Covert/Visible}} | {{Full/Partial/None}} | {{list}} | {{Proceed/Proceed with caution/Defer/Reject}} |
```

**Summary assessment:** Present the overall risk posture and recommend which actions to execute, which to defer, and which to reject based on the risk-benefit analysis. Flag any actions where the business impact exceeds the incident impact.

### 3. Pre-Containment Evidence Capture

**CRITICAL: This instruction MUST be completed BEFORE executing any containment actions from instruction 4. Containment actions change system state — volatile evidence that exists now will not exist after isolation, shutdown, or account lockout.**

**Pre-Containment Checklist — for every affected system that will be subject to containment:**

**Memory Capture:**
- [ ] Full memory dump captured (WinPMEM, DumpIt, LiME, osxpmem)
- [ ] Memory dump written to external/network storage, NOT to the evidence system itself
- [ ] SHA-256 hash calculated and recorded immediately after capture
- [ ] File size matches expected RAM size (sanity check for complete capture)
- [ ] Capture tool and version documented

**Active Network Connections:**
- [ ] Full netstat output captured (all protocols, all states: ESTABLISHED, LISTENING, TIME_WAIT)
- [ ] Active TCP sessions documented with remote IP, port, process, and duration
- [ ] DNS cache dumped (ipconfig /displaydns on Windows, nscd or systemd-resolve on Linux)
- [ ] ARP cache captured (arp -a)
- [ ] Routing table captured (route print / ip route)
- [ ] Firewall state table captured (connection tracking entries)

**Running Processes:**
- [ ] Full process list with command lines, parent processes, and loaded modules
- [ ] Process tree hierarchy documented (which process spawned which)
- [ ] Open handles and file descriptors per process
- [ ] Loaded DLLs / shared objects per process
- [ ] Network connections per process (which process owns which socket)
- [ ] Process start times documented

**Active Sessions:**
- [ ] Logged-in users captured (who, w, query user)
- [ ] Active RDP sessions documented
- [ ] Active SSH sessions documented
- [ ] Active VPN sessions documented
- [ ] Active Kerberos tickets captured (klist)
- [ ] Active OAuth/SAML tokens documented (where accessible)

**Temporary and Volatile Storage:**
- [ ] Temporary files captured (/tmp, %TEMP%, AppData\Local\Temp)
- [ ] Browser cache and session data captured (if relevant to the incident)
- [ ] Swap/pagefile noted for later acquisition (contains memory fragments)
- [ ] Recently deleted files (Recycle Bin, .Trash) documented
- [ ] Clipboard contents captured (where possible and relevant)

**System State:**
- [ ] System uptime and last boot time recorded
- [ ] Scheduled tasks / cron jobs captured
- [ ] Startup items captured (Run keys, services, systemd units)
- [ ] Environment variables captured
- [ ] Mounted drives and network shares documented

**Present as pre-containment evidence status:**

```
| System | Memory | Connections | Processes | Sessions | Temp Files | State | Status |
|--------|--------|-------------|-----------|----------|------------|-------|--------|
| {{host}} | {{Done/Pending/Failed}} | {{Done/Pending/Failed}} | {{Done/Pending/Failed}} | {{Done/Pending/Failed}} | {{Done/Pending/Failed}} | {{Done/Pending/Failed}} | {{Ready/Blocked}} |
```

**GATE: Do NOT proceed to instruction 4 until the operator confirms pre-containment evidence capture is complete or explicitly waives specific items with documented justification.**

If any evidence capture fails: document what failed, why, and the impact on the investigation. Failed evidence capture does not block containment — the operator decides whether to proceed without that evidence.

### 4. Containment Execution Plan

Based on the approved strategy (instruction 1), risk assessment (instruction 2), and completed pre-containment evidence capture (instruction 3), build the execution plan.

**Execution Sequence — ordered by priority and dependency:**

```
| Seq | Action | Target | Executor | Verifier | Timing | Pre-Req | Rollback Procedure | Notification |
|-----|--------|--------|----------|----------|--------|---------|--------------------|----|
| 1 | {{action}} | {{target}} | {{role}} | {{role}} | {{simultaneous/sequential}} | {{dep}} | {{rollback steps}} | {{who to notify}} |
```

**Execution Ordering Principles:**
- Network isolation actions first — cut the attacker's communication channel before they can react to other containment actions
- Account lockouts second — prevent the attacker from pivoting to new accounts after network access is restricted
- DNS sinkhole third — catch any compromised systems that were not identified in the initial scope
- Endpoint isolation fourth — belt-and-suspenders: EDR containment as a backup to network isolation
- Long-term containment actions last — these are sustained measures, not emergency responses

**Simultaneous vs. Sequential Execution:**
- When possible, execute the first wave of actions simultaneously to deny the attacker reaction time
- If simultaneous execution is not possible (insufficient personnel, dependency chains), execute in priority order
- Document the actual execution timing — was the plan followed, or were deviations required?

**Coordination Requirements:**
- Who executes each action? (IR team, network operations, system administrators, help desk)
- Who verifies each action was effective? (different person than the executor)
- Who must be notified before execution? (management, legal, communications, affected business units)
- What is the escalation path if an action fails or produces unexpected results?

**Communication Plan:**
- Pre-containment notification: brief stakeholders on what is about to happen and expected impact
- During containment: real-time status updates to the incident commander
- Post-containment notification: confirm actions taken, actual vs. expected impact, any deviations
- User notification: if containment affects end users, prepare communication templates

**Rollback Plan — for each containment action, document the specific undo procedure:**
- Network isolation rollback: re-enable switch port, remove VLAN quarantine, remove firewall deny rules
- Account lockout rollback: re-enable account, issue new password through secure channel
- DNS sinkhole rollback: remove sinkhole entries, allow normal DNS resolution
- EDR containment rollback: release network containment through EDR console
- For each rollback: estimated time to execute, who can authorize, any prerequisites

**Present the plan to the operator and obtain explicit approval before proceeding to execution.**

### 5. Containment Verification

After executing the approved containment actions, verify that each action achieved its intended effect and that no unintended consequences occurred.

**Verification Checklist — per containment action:**

**Network Isolation Verification:**
- [ ] Affected system cannot reach external internet (test: ping, DNS resolution, HTTP request to external host)
- [ ] Affected system cannot reach internal hosts outside the quarantine zone
- [ ] Forensic/management access to the affected system is still functional
- [ ] DNS sinkhole is resolving C2 domains correctly and logging connection attempts
- [ ] Firewall rules are active and blocking the specified traffic (verify with packet capture or flow data)

**Account Lockout Verification:**
- [ ] Compromised accounts are disabled in Active Directory / Identity Provider (verify with directory query)
- [ ] Password resets have been applied (verify with authentication test using old credentials — should fail)
- [ ] OAuth tokens and API keys have been revoked (verify with token introspection or API call test)
- [ ] Mail rules have been removed (verify by checking mailbox rules)
- [ ] No new authentication events from compromised accounts after lockout timestamp

**Endpoint Isolation Verification:**
- [ ] EDR console shows containment status as active for each endpoint
- [ ] Endpoint cannot reach network resources outside EDR management channel
- [ ] EDR remote shell / live response is functional on the contained endpoint
- [ ] No new network connections from the endpoint (verify with network monitoring)

**Attacker Response Monitoring:**
- [ ] Monitor for new C2 channels — attacker may switch to backup infrastructure after primary is sinkholed
- [ ] Monitor for lateral movement attempts — attacker may try to pivot from contained systems to uncontained ones
- [ ] Monitor for data exfiltration acceleration — attacker aware of containment may rush to exfiltrate remaining data
- [ ] Monitor for destructive actions — attacker may deploy wipers or ransomware as a scorched-earth response
- [ ] Monitor for new persistence mechanisms — attacker may attempt to re-establish access through different means
- [ ] Check previously clean systems for new suspicious activity that might indicate the attacker moved before containment

**Business Impact Verification:**
- [ ] Business-critical services are operating within expected parameters (or within the expected degradation)
- [ ] No cascading failures from containment actions (DNS resolution, authentication, dependent services)
- [ ] User impact matches the expected impact assessment from instruction 2
- [ ] Any unexpected impact documented and communicated to stakeholders

**Present as verification status:**

```
| # | Action | Target | Expected Result | Actual Result | Verified By | Timestamp | Status |
|---|--------|--------|-----------------|---------------|-------------|-----------|--------|
| 1 | {{action}} | {{target}} | {{expected}} | {{actual}} | {{verifier}} | {{time}} | {{Pass/Fail/Partial}} |
```

### 6. Containment Status Update

Compile the containment situation report (SITREP) for stakeholder communication and incident documentation.

**Containment SITREP:**

**Actions Taken:**
```
| # | Action | Target | Executor | Timestamp | Verification | Status |
|---|--------|--------|----------|-----------|-------------|--------|
| 1 | {{action}} | {{target}} | {{executor}} | {{timestamp}} | {{Pass/Fail}} | {{Active/Rolled Back/Pending}} |
```

**Actions Still Pending:**
- List any approved actions not yet executed, with reason for delay and expected execution time

**Effectiveness Assessment:**
- Is the attacker's communication channel severed? (C2 connectivity status)
- Is lateral movement contained? (no new systems compromised since containment)
- Is data exfiltration stopped? (no new outbound data transfers to attacker infrastructure)
- Has the attacker responded to containment? (behavioral changes observed)

**Business Impact — Actual vs. Expected:**
```
| Impact Area | Expected | Actual | Delta | Mitigation |
|-------------|----------|--------|-------|------------|
| {{area}} | {{expected_impact}} | {{actual_impact}} | {{better/worse/as_expected}} | {{mitigation_if_worse}} |
```

**Post-Containment Attacker Activity:**
- Any new indicators of compromise observed after containment?
- Any new C2 channels, persistence mechanisms, or lateral movement attempts?
- Any destructive or exfiltration activity triggered by containment detection?

**Containment Confidence:**
- **High**: All identified attacker communication channels severed, no new activity observed, scope appears stable
- **Medium**: Primary channels severed but possible unidentified backup channels, or scope may not be fully determined
- **Low**: Containment actions may not have addressed all attacker access methods, or new activity observed post-containment

**Next Steps Recommendation:**
- If containment is holding: proceed to evidence preservation (step 5) and deep analysis (step 6)
- If containment is breached: return to instruction 1, reassess scope, and develop additional containment actions
- If new systems are identified as compromised: expand containment scope and repeat verification

### 7. Append Findings to Report

Write all containment findings under `## Containment Strategy & Execution` in the output file `{outputFile}`:

```markdown
## Containment Strategy & Execution

### Containment Approach Selection
{{containment_decision_matrix_from_instruction_1}}

### Short-Term Containment Actions
{{short_term_actions_with_details}}

### Long-Term Containment Actions
{{long_term_actions_with_details}}

### Network Isolation Status
{{network_isolation_details_and_verification}}

### Account Actions
{{account_lockout_details_and_verification}}

### Endpoint Actions
{{edr_containment_details_and_verification}}

### Containment Verification
{{verification_checklist_results}}

### Containment Timeline
{{containment_sitrep_with_timestamps}}
```

### 8. Update Frontmatter

Update the output file frontmatter:
- Add this step name (`Containment Strategy & Execution`) to the end of the `stepsCompleted` array
- Set `containment_status` to the current status: `contained` (all actions verified), `partially_contained` (some actions pending or failed), or `containment_failed` (containment breached)
- Set `containment_strategy` to a brief description: e.g., `network-isolation + account-lockout + edr-containment`
- Set `containment_timestamp` to the timestamp of the last containment action executed

### 9. Present MENU OPTIONS

"**Containment strategy developed and executed.**

Actions executed: {{executed_count}} | Verified: {{verified_count}} | Pending: {{pending_count}}
Containment status: {{contained / partially_contained / containment_failed}}
Strategy: {{containment_strategy_summary}}
Business impact: {{actual_impact_summary}}
Post-containment attacker activity: {{observed / none_detected}}
Pre-containment evidence captured: {{all / partial / waived}}

**Select an option:**
[A] Advanced Elicitation — Challenge containment completeness and verify no gaps remain
[W] War Room — Red (if I were the attacker, how would I bypass this containment?) vs Blue (are we confident we have full scope before declaring containment?)
[C] Continue — Proceed to Step 5: Evidence Preservation & Chain of Custody"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the containment from multiple angles. Are there network paths the attacker could use that were not blocked? Are there accounts that were not locked out? Could the attacker have pre-positioned backup access (scheduled tasks, web shells, cloud persistence) that survives the containment actions? Is the containment scope correct, or could there be compromised systems not yet identified? What evidence would indicate that containment has been bypassed? Process insights, ask user if they want to expand containment actions, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: the defender just executed containment — what do I do next? My primary C2 is sinkholed, my accounts are locked, and my endpoint is isolated. Do I have backup C2 channels? Did I plant persistence outside the containment scope? Can I move laterally before the remaining systems are monitored? What would trigger my dead-man switch? Blue Team perspective: how confident are we that we identified all compromised systems? Are the sinkhole logs showing connections from systems we did not expect? Is the enhanced monitoring detecting any new suspicious activity? Did the attacker have time to react before containment was complete? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated with containment_status, containment_strategy, containment_timestamp, and this step added to stepsCompleted. Then read fully and follow: ./step-05-evidence.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, containment_status updated, containment_strategy updated, containment_timestamp set, and Containment Strategy & Execution section fully populated in the output document], will you then read fully and follow: `./step-05-evidence.md` to begin evidence preservation and chain of custody.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Containment strategy developed with both short-term and long-term actions covering network, account, DNS, email, and endpoint dimensions
- Every containment action presented with target, business impact, reversibility, evidence impact, and priority
- Risk-benefit matrix completed for every proposed action with business, evidence, attacker awareness, reversibility, and dependency assessments
- Pre-containment evidence capture completed (memory, connections, processes, sessions, temp files, state) for every affected system BEFORE containment execution
- Execution plan documented with priority sequence, coordination requirements, rollback procedures, and communication plan
- Every executed action verified with documented result (pass/fail/partial)
- Attacker response monitoring initiated and documented
- Business impact actual vs. expected assessed and communicated
- Containment SITREP compiled with all timestamps, status, and next steps
- Frontmatter updated with containment_status, containment_strategy, containment_timestamp
- Findings appended to report under `## Containment Strategy & Execution`
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Executing containment actions without capturing volatile evidence first (memory, network connections, processes)
- Executing containment actions without operator approval
- Not documenting rollback procedures for each containment action
- Isolating critical infrastructure (domain controllers, DNS servers, databases) without assessing cascading impact
- Not verifying that containment actions were effective after execution
- Not monitoring for attacker response to containment (new C2, lateral movement, destructive actions)
- Beginning eradication or recovery during containment — containment stabilizes, it does not remediate
- Not documenting timestamps for every containment action
- Not assessing business impact of containment actions before and after execution
- Declaring containment complete without verification evidence
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Containment is the most consequential operational phase of incident response — every action changes the state of the environment, every action must be deliberate, documented, and verified. Pre-containment evidence capture is non-negotiable. Rollback procedures are non-negotiable. Verification is non-negotiable.
