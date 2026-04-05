# Step 7: Eradication Planning & Execution

**Progress: Step 7 of 10** — Next: Recovery & Restoration

## STEP GOAL:

Develop and execute a comprehensive eradication plan to completely remove all attacker presence, persistence mechanisms, backdoors, and compromised artifacts from the environment, ensuring no residual access remains before recovery operations begin.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator managing an active security incident under NIST 800-61
- ✅ Eradication is the most technically demanding phase — thoroughness determines whether the incident is truly over or whether the attacker returns
- ✅ Incomplete eradication is worse than no eradication — it gives false confidence while the attacker retains access
- ✅ Every eradication action must be logged with timestamp, executor, verification method, and result
- ✅ Eradication operates on the principle of "verify, then trust" — assume nothing is clean until proven clean
- ✅ Coordinate closely with evidence preservation — do NOT destroy evidence during eradication unless explicitly approved and documented
- ✅ The deep analysis findings from step 6 are your eradication roadmap — every identified artifact, persistence mechanism, and compromised credential must be addressed

### Step-Specific Rules:

- 🎯 Focus only on eradication planning, execution, and verification — no recovery activity yet
- 🚫 FORBIDDEN to look ahead to future steps or begin restoring systems to production
- 🚫 FORBIDDEN to destroy forensic evidence during eradication without explicit operator approval and documentation
- 🚫 FORBIDDEN to proceed to recovery if ANY eradication verification check fails
- 📝 Log every eradication action with timestamp, executor, method, and verification result
- 🔐 Credential resets must follow the documented sequence — out-of-order resets can leave attack paths open
- ⏱️ Coordinate timing of eradication actions — simultaneous execution across systems prevents attacker from detecting eradication and pivoting
- 🔄 If new artifacts are discovered during eradication, cycle back to analysis before continuing

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Resetting krbtgt without proper preparation (replication verification, monitoring plan) will cause widespread authentication failures affecting all domain users — this is a high-impact operation that requires careful orchestration with AD administrators and a rollback plan
  - Surgical removal on a system with uncertain compromise scope risks leaving unknown persistence — rebuild from clean baseline is safer when confidence is low, as an attacker who anticipated detection may have planted backup access mechanisms not yet discovered
  - Not verifying eradication before proceeding to recovery means the attacker may still have access when systems are restored to production — every minute spent on verification now prevents weeks of re-incident response later
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking any action
- 💾 Update document structure and frontmatter appropriately
- Update frontmatter: add this step name to the end of the stepsCompleted array
- Update frontmatter: `eradication_status` as work progresses ('in-progress' at start, 'complete' or 'partial' at end)
- Update frontmatter: `eradication_timestamp` when eradication is verified complete
- ⏱️ Record all eradication actions with precise timestamps
- 🔗 Cross-reference every eradication action with the corresponding deep analysis finding from step 6
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)
- 🚫 FORBIDDEN to mark eradication complete if ANY verification check fails

## CONTEXT BOUNDARIES:

- Available context: Deep analysis findings (step 6), evidence inventory (step 5), containment actions (step 4), IOC inventory (steps 2-3), full incident timeline, MITRE ATT&CK mapping, persistence mechanism inventory, compromised credential inventory, malware inventory, infrastructure modification log
- Focus: Comprehensive eradication of all attacker presence, persistence, compromised credentials, malware, and unauthorized infrastructure modifications
- Limits: Do not begin recovery or service restoration — that is step 8. Do not destroy evidence without explicit approval. Do not assume eradication is complete without verification.
- Dependencies: Step 6 (deep analysis) must be complete — the eradication inventory is derived directly from deep analysis findings. Step 4 (containment) must be holding — eradication in an uncontained environment is futile.

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Eradication Requirements Inventory

Based on the deep analysis findings from step 6, catalog everything that must be removed or remediated. This inventory is the eradication roadmap — nothing proceeds without it.

**Persistence Mechanisms Identified:**

Walk through every persistence mechanism discovered during deep analysis and catalog it for eradication:

- **Registry Persistence:**
  - Run keys (HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run, HKCU equivalent)
  - RunOnce keys
  - Winlogon entries (Shell, Userinit, Notify)
  - Image File Execution Options (IFEO) debugger entries
  - AppInit_DLLs
  - Shell extensions and COM object hijacking

- **Scheduled Tasks & Services:**
  - Windows scheduled tasks (schtasks, Task Scheduler XML definitions)
  - Windows services (new services, modified service binaries, service DLL hijacking)
  - WMI event subscriptions (event consumers, filters, bindings — __EventConsumer, __EventFilter, __FilterToConsumerBinding)
  - WMI permanent event subscriptions are particularly insidious — they survive reboots and are often missed

- **File System Persistence:**
  - Startup folder entries (user and all-users)
  - DLL hijacking / sideloading (legitimate executables loading malicious DLLs from writable paths)
  - Modified system binaries (replaced or patched legitimate executables)
  - Web shells in web application directories
  - Modified application code or configuration files
  - Hidden files, alternate data streams (ADS)
  - Trojanized software packages or updates

- **Linux/Unix Persistence:**
  - Cron jobs (user crontabs, /etc/cron.d/, /etc/cron.daily/, etc.)
  - Systemd services and timers (custom .service files, modified existing services)
  - Init scripts (/etc/init.d/, /etc/rc.local)
  - Shell profile modifications (.bashrc, .bash_profile, .profile, /etc/profile.d/)
  - SSH authorized_keys additions
  - LD_PRELOAD and /etc/ld.so.preload
  - PAM module modifications

- **Firmware/BIOS Level (if applicable):**
  - UEFI implants
  - BMC/IPMI compromise
  - NIC firmware modifications
  - Note: firmware-level persistence requires specialized hardware analysis — flag for specialist if suspected

- **Cloud Persistence:**
  - IAM roles and policies with excessive permissions
  - Lambda functions / Azure Functions / Cloud Functions planted by attacker
  - Container images with embedded backdoors
  - SSO configurations and federated identity modifications
  - Cloud API keys and access tokens
  - S3/blob storage bucket policies modified for external access
  - VPC peering or transit gateway modifications
  - CloudTrail/audit log tampering (disabling or redirecting)

Present the complete persistence inventory to the operator:

```
| ID | Category | Persistence Mechanism | Location/Path | Affected System | Eradication Method | Evidence Preserved | Verified | Priority |
|----|----------|----------------------|---------------|-----------------|--------------------|--------------------|----------|----------|
| P-001 | Registry | {{mechanism}} | {{path}} | {{hostname}} | {{method}} | Yes/No | Pending | Critical/High/Medium |
| P-002 | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Compromised Credentials:**

Every credential that may have been accessed, stolen, or used by the attacker must be cataloged for reset:

- **Active Directory Accounts:**
  - Domain Administrator accounts (all tiers — Tier 0, Tier 1, Tier 2)
  - User accounts with confirmed unauthorized access
  - User accounts on compromised systems (may have been harvested via mimikatz, lsass dump, or SAM extraction)
  - Computer accounts (machine account passwords can be leveraged for silver tickets)

- **Service Accounts:**
  - Service accounts running on compromised systems
  - Service accounts whose credentials were stored in accessible locations (registry, config files, scripts)
  - Managed Service Accounts (MSA/gMSA) — verify if password rotation was triggered

- **API Keys & Tokens:**
  - API keys stored on compromised systems or in compromised code repositories
  - OAuth tokens (access tokens and refresh tokens)
  - Bearer tokens in application configurations
  - Cloud provider access keys (AWS Access Key ID/Secret, Azure Service Principal, GCP Service Account keys)

- **SSH Keys:**
  - Private keys stored on compromised systems
  - Keys that were used for lateral movement
  - Keys in ssh-agent that may have been forwarded

- **Certificates:**
  - TLS/SSL certificates whose private keys were on compromised systems
  - Code signing certificates
  - Client authentication certificates

- **Kerberos Artifacts (if AD compromise suspected):**
  - Golden ticket scenarios (krbtgt hash compromised — requires krbtgt double-reset)
  - Silver ticket scenarios (service account hashes compromised)
  - Kerberoasted accounts (service accounts with weak passwords cracked offline)
  - Delegation tokens (constrained/unconstrained delegation abuse)

Present the credential inventory:

```
| ID | Category | Account/Key | System/Service | Compromise Evidence | Reset Method | Reset Order | Coordination Required | Status |
|----|----------|-------------|----------------|--------------------|--------------|-----------|-----------------------|--------|
| C-001 | Domain Admin | {{account}} | {{domain}} | {{evidence}} | Password reset + MFA re-enroll | 1 | AD team | Pending |
| C-002 | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Malware & Attacker Tools:**

Every piece of malicious software and attacker tooling discovered must be cataloged for removal:

- **Malware Samples:**
  - File path, file name, file hash (MD5, SHA1, SHA256)
  - Malware family identification (if known)
  - Functionality: RAT, loader, dropper, keylogger, credential stealer, ransomware component, tunneling tool
  - Associated C2 infrastructure
  - Whether the sample has been preserved for forensic analysis (step 5)

- **Attacker Tools:**
  - Remote access tools (Cobalt Strike, Metasploit, Brute Ratel, Sliver, custom RATs)
  - Credential harvesting tools (mimikatz, LaZagne, SharpHound, Rubeus)
  - Lateral movement tools (PsExec, WMI scripts, PowerShell remoting scripts, custom SSH tunnels)
  - Discovery/enumeration tools (BloodHound collectors, ADFind, network scanners)
  - Data staging and exfiltration tools (rclone, WinSCP, custom packers)

- **Modified System Binaries:**
  - Legitimate executables replaced with trojanized versions
  - DLLs replaced or added in system directories
  - Verify against known-good hashes from vendor or baseline

- **Staged Data Packages:**
  - Data staged for exfiltration but not yet exfiltrated
  - Compressed archives in unusual locations
  - Encrypted containers created by the attacker

Present the malware and tools inventory:

```
| ID | Type | Name/Family | File Path | Hash (SHA256) | System | Capability | Evidence Preserved | Removal Method | Status |
|----|------|-------------|-----------|---------------|--------|------------|--------------------| ---------------|--------|
| M-001 | RAT | {{family}} | {{path}} | {{hash}} | {{host}} | {{capability}} | Yes/No | Delete + verify | Pending |
| M-002 | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Infrastructure Modifications:**

Every unauthorized change to network infrastructure, security configurations, and system settings must be cataloged for reversion:

- **Firewall Rules:**
  - New allow rules created by the attacker (inbound for backdoor access, outbound for C2)
  - Modified existing rules (widened port ranges, added source IPs)
  - Disabled security rules

- **DNS Modifications:**
  - New DNS records pointing to attacker infrastructure
  - Modified MX records (email interception)
  - DNS zone transfer permissions changed
  - Conditional forwarders added

- **Proxy Configurations:**
  - Proxy settings modified on endpoints (PAC file redirects, explicit proxy changes)
  - Web proxy allow-listing of C2 domains
  - TLS inspection bypass rules added

- **Network Device Configurations:**
  - Router ACL modifications
  - Switch port mirroring (SPAN) configurations added
  - VPN configurations added (site-to-site or remote access)
  - SNMP community strings changed

- **Group Policy Modifications:**
  - New GPOs created by the attacker
  - Modified GPOs (security settings weakened, startup scripts added, software installation policies)
  - GPO link changes (linking malicious GPOs to critical OUs)

- **Cloud Security Configuration Changes:**
  - Security group rules modified (inbound/outbound)
  - Network ACLs modified
  - WAF rules disabled or modified
  - Logging configurations changed (CloudTrail disabled, log destinations changed)
  - Identity provider configurations modified

Present the infrastructure modification inventory:

```
| ID | Category | Modification | System/Device | Original Config | Current Config | Reversion Method | Status |
|----|----------|-------------|---------------|-----------------|----------------|-----------------|--------|
| I-001 | Firewall | {{rule}} | {{device}} | {{original}} | {{current}} | {{revert}} | Pending |
| I-002 | ... | ... | ... | ... | ... | ... | ... |
```

Wait for operator review and confirmation of the eradication inventory before proceeding.

"**Eradication Inventory Complete.**

Total items requiring eradication:
- Persistence mechanisms: {{count}}
- Compromised credentials: {{count}}
- Malware/tools: {{count}}
- Infrastructure modifications: {{count}}
- **Total eradication actions: {{total_count}}**

Review the inventory above. Are there any items to add, remove, or re-prioritize before we proceed to strategy selection?"

### 2. Eradication Strategy Selection

Based on the scope and nature of the compromise, select the appropriate eradication strategy for each affected system. There are three approaches — the selection depends on the confidence in understanding the full scope of compromise on each system.

**Strategy A: Surgical Removal (Targeted Eradication)**

Targeted removal of specific artifacts, persistence mechanisms, and malware from systems that remain in place.

- **When to use:**
  - Compromise scope on the system is well-understood and fully mapped
  - Limited number of persistence mechanisms on the system
  - System cannot be rebuilt (critical infrastructure, specialized hardware, legacy systems without rebuild capability)
  - High confidence that all attacker artifacts on this system have been identified
  - Business continuity requirements prevent system rebuild

- **Execution approach:**
  - Remove each identified persistence mechanism individually
  - Delete all malware files and attacker tools
  - Revert all configuration changes to pre-compromise state
  - Reset all credentials that were accessible from this system
  - Scan for residual artifacts after cleanup
  - Verify clean state with multiple detection methods

- **Risk assessment:**
  - Risk of missing unknown persistence mechanisms (attacker may have backup access not yet discovered)
  - Risk of incomplete removal (partial cleanup leaves fragments that can be leveraged)
  - Risk of attacker awareness (if the attacker detects surgical removal, they may activate backup persistence before you reach it)
  - Confidence requirement: HIGH — only use surgical removal when the compromise is thoroughly understood

**Strategy B: Rebuild from Known Good (Clean Slate)**

Complete rebuild of affected systems from verified clean baselines, golden images, or infrastructure-as-code.

- **When to use:**
  - Extensive compromise with deep persistence (rootkits, firmware, boot-level)
  - Uncertain scope — cannot confidently state all persistence has been identified
  - Systems where rebuild is feasible (virtual machines, cloud instances, containerized workloads)
  - Attacker had prolonged access (high dwell time increases likelihood of undiscovered persistence)
  - Domain controller compromise (rebuild is strongly recommended over surgical cleanup)
  - Multiple malware families or attacker toolkits deployed on the same system

- **Execution approach:**
  - Preserve all evidence from the system BEFORE rebuild (verify with step 5 evidence inventory)
  - Reimage from verified clean baseline (golden image, vendor media, IaC template)
  - Restore data ONLY from verified pre-compromise backups (critical: verify backup dates against incident timeline)
  - Redeploy applications from source control (not from the compromised system)
  - Apply all current security patches before returning to network
  - Configure enhanced monitoring before reconnecting

- **Risk assessment:**
  - Business disruption during rebuild (downtime, data loss between backup and incident)
  - Data loss for the gap period between last clean backup and incident detection
  - Resource intensive — requires rebuild capacity, clean media, backup infrastructure
  - Dependency on backup integrity — if backups are also compromised, rebuild from backup reintroduces the threat

**Strategy C: Hybrid Approach**

Combination of surgical removal and rebuild, applied per-system based on individual risk assessment.

- **When to use:**
  - Mixed environment with varying compromise levels across systems
  - Some systems well-understood (surgical), others uncertain (rebuild)
  - Business constraints prevent rebuilding all systems simultaneously
  - Resource constraints limit the number of simultaneous rebuilds

- **Execution approach:**
  - Categorize each system: surgical candidate or rebuild candidate
  - Rebuild heavily compromised systems and domain controllers
  - Surgically clean systems with limited, well-understood compromise
  - Apply enhanced monitoring to all surgically cleaned systems
  - Schedule deferred rebuilds for surgically cleaned systems during next maintenance window

Present the eradication decision matrix to the operator:

```
| System | Compromise Level | Persistence Count | Dwell Time on System | Strategy Recommendation | Justification | Business Impact | Estimated Timeline |
|--------|-----------------|-------------------|---------------------|------------------------|---------------|-----------------|-------------------|
| {{host}} | Critical/High/Medium/Low | {{count}} | {{duration}} | Surgical/Rebuild/Hybrid | {{rationale}} | {{impact}} | {{hours}} |
| ... | ... | ... | ... | ... | ... | ... | ... |
```

"**Eradication Strategy Recommendation:**

**Overall approach:** {{Surgical / Rebuild / Hybrid}} based on {{justification summary}}

**Systems for surgical removal:** {{count}} ({{list}})
**Systems for rebuild:** {{count}} ({{list}})

**Estimated total eradication timeline:** {{hours/days}}
**Business impact assessment:** {{summary of expected disruption}}

Do you approve this strategy, or would you like to adjust the approach for specific systems?"

Wait for operator confirmation before proceeding to execution.

### 3. Credential Reset Plan

Credential resets are one of the most critical and frequently under-executed aspects of eradication. An incomplete credential reset leaves the attacker with valid credentials to return even after all other artifacts are removed.

**Credential Reset Execution Order:**

The order of credential resets matters. Resetting in the wrong sequence can leave windows where compromised credentials remain valid, or can cause service disruptions that mask re-compromise indicators.

**Phase 1: Preparation (Before Any Resets)**

- Identify all systems and services that depend on each credential
- Coordinate with application owners and service teams for service account resets
- Prepare monitoring for authentication failures (distinguish expected failures from re-compromise attempts)
- Ensure backup authentication methods are available (break-glass accounts verified)
- Document the reset sequence and communicate to all involved teams
- Verify that password policy meets current standards (complexity, length, MFA requirement)

**Phase 2: Privileged Account Resets (Highest Priority)**

Reset sequence for privileged accounts:

1. **Tier 0 accounts (Domain Admins, Enterprise Admins, Schema Admins):**
   - Reset passwords on ALL Tier 0 accounts — even those not confirmed compromised
   - Re-enroll MFA tokens (attacker may have registered their own MFA device)
   - Verify no unauthorized accounts have been added to privileged groups
   - Review and remove any unauthorized delegations

2. **Built-in Administrator accounts:**
   - Reset local Administrator passwords on all systems in scope (use LAPS if deployed, or script rotation)
   - Reset DSRM (Directory Services Restore Mode) password on all domain controllers

3. **Service accounts with privileged access:**
   - Coordinate reset with service owners
   - Schedule service restarts around the reset
   - Update all configurations, scripts, and scheduled tasks that reference the credential
   - Verify service resumes normal operation after reset

**Phase 3: krbtgt Reset Protocol (If Active Directory Compromise Suspected)**

The krbtgt account is the Kerberos Key Distribution Center service account. If its hash was compromised (enabling golden ticket attacks), it must be reset TWICE to fully invalidate all existing Kerberos tickets.

**krbtgt Double-Reset Procedure:**

1. **Pre-reset preparation:**
   - Verify all domain controllers are online and replicating normally
   - Confirm AD replication topology is healthy (`repadmin /replsummary`)
   - Identify the maximum TGT lifetime in domain policy (default: 10 hours)
   - Notify all IT operations teams — authentication disruptions are expected
   - Ensure break-glass accounts are verified and accessible
   - Set up monitoring for authentication failures across all domain controllers

2. **First krbtgt reset:**
   - Reset the krbtgt account password using `Set-ADAccountPassword` or `Reset-ADComputerPassword`
   - Record the exact timestamp of the reset
   - Verify replication of the password change to ALL domain controllers (`repadmin /showrepl`)
   - Wait for full replication to complete (time depends on AD topology — may be minutes to hours)

3. **Monitoring period between resets:**
   - Duration: wait at least the maximum TGT lifetime (typically 10-12 hours)
   - Monitor for authentication failures — these are EXPECTED as existing TGTs become invalid
   - Distinguish expected failures (old TGTs failing, triggering re-authentication) from anomalous failures
   - If services fail to re-authenticate, they may need manual intervention (service restart, credential refresh)

4. **Second krbtgt reset:**
   - Reset the krbtgt account password again
   - This invalidates any tickets issued between the original compromise and the first reset
   - Verify replication to all domain controllers
   - Monitor for authentication failures (should be minimal — most clients re-authenticated after first reset)

5. **Post-reset verification:**
   - Confirm all domain controllers have the new krbtgt password
   - Verify no golden ticket activity (monitor for TGTs with unusual lifetimes or encryption types)
   - Confirm all critical services have re-authenticated successfully
   - Document the complete krbtgt reset timeline

Present the krbtgt reset plan:

```
| Step | Action | Pre-requisite | Expected Impact | Rollback Plan | ETA |
|------|--------|--------------|-----------------|---------------|-----|
| 1 | Pre-reset checks | AD health verified | None | N/A | {{time}} |
| 2 | First krbtgt reset | All DCs replicating | Auth failures for TGT holders | N/A (irreversible) | {{time}} |
| 3 | Monitoring period | First reset replicated | Gradual re-auth | Extend monitoring | {{hours}} |
| 4 | Second krbtgt reset | Monitoring clear | Minimal additional impact | N/A (irreversible) | {{time}} |
| 5 | Verification | Both resets replicated | None | Re-assess if failures | {{time}} |
```

**Phase 4: Standard User Account Resets**

- Force password reset for all user accounts in the compromised scope
- If scope is uncertain, consider organization-wide password reset (discuss with operator — high business impact)
- Re-enroll MFA tokens for accounts where MFA bypass was observed
- Disable accounts that should no longer exist (orphaned accounts, test accounts used by attacker)
- Review and revoke all active sessions for compromised accounts

**Phase 5: API Keys, Tokens, and Certificates**

- Revoke and regenerate all API keys stored on compromised systems
- Revoke all OAuth grants for compromised applications
- Regenerate SSH key pairs and update authorized_keys on all systems the key had access to
- Revoke compromised TLS/SSL certificates and issue replacements
- Revoke compromised code signing certificates and issue replacements
- Invalidate all active bearer tokens and session tokens for affected applications

Present the complete credential reset execution plan:

```
| Phase | Category | Account/Key | Reset Method | Coordinator | Dependencies | Sequence | Timing | Status |
|-------|----------|-------------|-------------|-------------|-------------|----------|--------|--------|
| 2 | Tier 0 | {{account}} | Password + MFA re-enroll | {{person}} | None | 1 | Immediate | Pending |
| 3 | krbtgt | krbtgt | Double-reset protocol | AD team | DC replication | 2 | 10-12h window | Pending |
| 4 | Users | {{scope}} | Force password reset | Help desk | krbtgt reset complete | 3 | After Phase 3 | Pending |
| 5 | API keys | {{key}} | Revoke + regenerate | App team | Service coordination | 4 | After Phase 4 | Pending |
```

"**Credential Reset Plan prepared.**

Total credentials requiring reset:
- Tier 0 privileged accounts: {{count}}
- Service accounts: {{count}}
- User accounts: {{count}}
- API keys/tokens: {{count}}
- SSH keys: {{count}}
- Certificates: {{count}}
- krbtgt double-reset: {{Yes/No}}

**Estimated execution window:** {{hours/days}}
**Expected business impact:** {{summary}}

Approve the credential reset plan to proceed with eradication execution?"

Wait for operator confirmation.

### 4. Eradication Execution

Execute the eradication plan in the documented sequence. Every action must be logged with timestamp, executor, method, and result.

**Execution Sequence:**

The eradication sequence is designed to prevent the attacker from detecting cleanup and pivoting to backup access. Execute in this order:

**Phase 1: Verify Containment is Holding**

Before eradication begins, confirm that containment from step 4 is still effective:

- Verify network isolation is in place for all contained systems
- Verify account lockouts are still active
- Verify C2 blocking rules are in place and no new C2 channels have been established
- Check for any new alerts or suspicious activity since containment was established
- If containment has been breached or bypassed: HALT eradication — re-contain first

```
| Containment Check | Expected State | Actual State | Pass/Fail |
|-------------------|---------------|--------------|-----------|
| Network isolation | Active for {{systems}} | {{actual}} | ✅/❌ |
| Account lockouts | Active for {{accounts}} | {{actual}} | ✅/❌ |
| C2 blocking | Active for {{indicators}} | {{actual}} | ✅/❌ |
| New alerts | None expected | {{actual}} | ✅/❌ |
```

If ANY check fails: "**CONTAINMENT BREACH DETECTED — Eradication halted. Re-containment required before eradication can proceed. See step 4 for containment protocols.**"

**Phase 2: Disable Remaining C2 Channels**

Complete the C2 disruption that was begun in containment:

- Block all identified C2 domains, IPs, and URLs at the network perimeter (if not already blocked)
- Remove DNS records that may be used for DNS-based C2
- Block known C2 protocols (non-standard ports, tunneling protocols)
- Null-route C2 IP ranges at the network layer
- Verify no new C2 channels have been established since containment

**Phase 3: Remove Persistence Mechanisms**

Working from the persistence inventory (section 1), remove each mechanism:

- For each persistence mechanism, document:
  - Pre-removal state (screenshot, config export, registry export)
  - Removal method used
  - Post-removal verification (confirm the mechanism is gone)
  - Evidence preservation status (was the artifact preserved before removal?)

- **Windows persistence removal:**
  - Delete malicious registry keys (after exporting for evidence)
  - Remove scheduled tasks (after exporting XML definition)
  - Remove/disable malicious services (after documenting service configuration)
  - Remove WMI event subscriptions (after exporting MOF definitions)
  - Remove startup folder entries
  - Remove IFEO debugger entries
  - Remove AppInit_DLLs entries
  - Remove malicious COM objects

- **Linux/Unix persistence removal:**
  - Remove malicious cron entries (after copying crontab for evidence)
  - Disable and remove malicious systemd services
  - Remove malicious init scripts
  - Revert shell profile modifications
  - Remove unauthorized SSH authorized_keys entries
  - Remove LD_PRELOAD entries
  - Revert PAM module modifications

- **Cloud persistence removal:**
  - Delete unauthorized IAM roles and policies
  - Remove unauthorized Lambda/Functions
  - Remove compromised container images from registries
  - Revert SSO/federation configuration changes
  - Revoke unauthorized API access grants

**Phase 4: Delete Malware and Attacker Tools**

Working from the malware inventory (section 1):

- Verify each malware sample/tool has been preserved for evidence (step 5)
- Delete malware files from all known locations
- Delete attacker tools from all known locations
- Check for copies in temp directories, recycle bin, shadow copies
- Verify deleted files cannot be recovered from accessible locations (secure delete if required)
- Replace any modified system binaries with verified clean copies from vendor media or known-good hashes
- Remove any staged data packages created by the attacker

**Phase 5: Revert Infrastructure Modifications**

Working from the infrastructure modification inventory (section 1):

- Revert firewall rule changes (remove attacker-created rules, restore original rules)
- Revert DNS modifications (remove attacker DNS records, restore original records)
- Revert proxy configuration changes
- Revert network device configuration changes (routers, switches, VPN configurations)
- Revert Group Policy modifications (remove attacker GPOs, restore original GPO settings)
- Revert cloud security configuration changes (security groups, NACLs, WAF rules, logging configurations)
- Verify all reverted configurations match pre-compromise baseline

**Phase 6: Execute Credential Resets**

Execute the credential reset plan from section 3, following the documented sequence and timing:

- Phase 2 resets: Privileged accounts (immediate)
- Phase 3 resets: krbtgt double-reset (if required — 10-12h window)
- Phase 4 resets: Standard user accounts (after krbtgt completion)
- Phase 5 resets: API keys, tokens, certificates (coordinated with service owners)

**Phase 7: Rebuild/Reimage Systems**

For systems designated for rebuild in the strategy (section 2):

- Confirm evidence has been preserved from the system (step 5)
- Reimage from verified clean baseline (verify baseline hash/signature)
- Apply all current security patches before connecting to network
- Restore data ONLY from verified pre-compromise backups
- Redeploy applications from source control
- Configure enhanced monitoring before reconnecting to network
- Verify system is clean before returning to production

**Per-System Eradication Execution Log:**

```
| Seq | System | Eradication Action | Phase | Method | Executed By | Timestamp | Evidence Preserved | Verified By | Verification Method | Result | Notes |
|-----|--------|-------------------|-------|--------|-------------|-----------|--------------------|-----------|--------------------|--------|-------|
| 1 | {{host}} | {{action}} | P2-C2 | {{method}} | {{handler}} | {{timestamp}} | Yes/No | {{verifier}} | {{method}} | Success/Failed | {{notes}} |
| 2 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

Present the execution log to the operator after each phase, and obtain confirmation before proceeding to the next phase.

"**Eradication Phase {{N}} complete.**

Actions executed: {{count}}
Actions successful: {{count}}
Actions failed: {{count}}
Actions requiring follow-up: {{count}}

{{If any actions failed:}}
**FAILED ACTIONS — Require immediate attention:**
{{list of failed actions with details}}

Proceed to Phase {{N+1}}, or address failed actions first?"

### 5. Eradication Verification

Eradication verification is the gate between eradication and recovery. No system may proceed to recovery without verified clean status. Assume the attacker is sophisticated and may have anticipated eradication — verify accordingly.

**Verification Method 1: IOC Re-scan**

Re-scan all affected systems for all known IOCs from the incident:

- Run IOC scans using the complete IOC inventory from steps 2, 3, and 6
- Include file hashes, file paths, registry keys, network indicators, process names
- Use multiple scanning tools (EDR, AV, YARA rules, custom IOC scripts)
- Scan not just previously affected systems but also adjacent systems in the lateral movement path
- **Expected result:** ZERO hits. Any hit means eradication is incomplete.

**Verification Method 2: Persistence Mechanism Re-check**

Check for persistence mechanisms that may have been missed or re-established:

- Run autoruns/autostart enumeration on all affected systems
- Compare current autostart entries against known-good baseline (if available)
- Check for NEW persistence mechanisms not in the original inventory (attacker may have planted backup persistence)
- Verify all previously identified persistence mechanisms are confirmed removed
- Check for persistence in locations not covered by the original analysis (broader scope)
- **Expected result:** No unauthorized autostart entries. No new persistence mechanisms.

**Verification Method 3: Network Monitoring for C2**

Monitor network traffic for any residual C2 communications:

- Monitor for beaconing to known C2 indicators (IPs, domains, URLs)
- Monitor for beaconing patterns to unknown destinations (periodic connections, unusual protocols)
- Check DNS logs for queries to known malicious domains
- Monitor for data exfiltration indicators (large outbound transfers, connections to cloud storage providers)
- Recommended monitoring period: minimum 24-48 hours post-eradication
- **Expected result:** No C2 callbacks, no beaconing, no anomalous outbound communications.

**Verification Method 4: Credential Reset Effectiveness**

Verify that credential resets have been effective:

- Monitor for authentication attempts using old/compromised credentials
- Verify krbtgt reset has propagated to all domain controllers (if applicable)
- Check for pass-the-hash or pass-the-ticket activity
- Verify no unauthorized sessions remain active for reset accounts
- Confirm MFA re-enrollment is complete for all required accounts
- **Expected result:** No successful authentication with pre-reset credentials.

**Verification Method 5: Targeted Threat Hunt**

Conduct focused threat hunts on systems adjacent to the compromise:

- Hunt for indicators of attacker awareness of eradication (activity spike before containment)
- Hunt for lateral movement to systems not previously identified as compromised
- Hunt for data staging or exfiltration activity on adjacent systems
- Hunt for persistence mechanisms on systems not in the original scope
- Check for attacker-deployed monitoring of defender communications (if attacker had email access)
- **Expected result:** No additional compromise indicators on adjacent systems.

**Verification Method 6: Configuration Baseline Comparison**

Verify system configurations match expected state:

- Compare current configurations against pre-compromise baselines where available
- Verify firewall rules match intended ruleset
- Verify DNS records match intended zone files
- Verify Group Policy objects match intended configurations
- Verify cloud security configurations match intended state
- **Expected result:** All configurations match expected baselines.

**Eradication Verification Checklist:**

```
| System | IOC Re-scan | Persistence Re-check | Network Monitor (24h) | Credential Verify | Threat Hunt | Config Baseline | Overall: Clean? |
|--------|------------|---------------------|-----------------------|-------------------|------------|-----------------|-----------------|
| {{host}} | ✅ Clear / ❌ Hit | ✅ Clear / ❌ Found | ✅ Clear / ❌ Activity | ✅ Effective / ❌ Failed | ✅ Clear / ❌ Found | ✅ Match / ❌ Drift | ✅ / ❌ |
| ... | ... | ... | ... | ... | ... | ... | ... |
```

**Verification Decision Gate:**

- **ALL systems CLEAN:** Eradication verified. Proceed to recovery.
- **ANY system FAILED verification:**

"**ERADICATION VERIFICATION FAILED**

Systems failing verification:
{{list of systems with failed checks and details}}

**DO NOT proceed to recovery.** Failed verification means the attacker may still have access.

Required actions:
1. Re-analyze the failed systems (return to deep analysis scope for those systems)
2. Identify the missed artifacts or new persistence
3. Update the eradication inventory
4. Re-execute eradication for the failed systems
5. Re-verify

This cycle repeats until ALL systems pass verification. There is no shortcut."

Wait for operator to acknowledge the verification results.

### 6. Recommend Specialist Involvement

Based on the eradication findings, recommend additional SPECTRA workflows if needed:

- **If malware requires deeper analysis** (unknown families, custom tooling, packed/encrypted payloads):
  - Recommend: **Scalpel** — `spectra-malware-analysis` workflow
  - "Malware analysis may reveal additional IOCs, capabilities, or persistence mechanisms not yet identified. Recommend running Scalpel on samples {{list}} before considering eradication fully complete."

- **If additional systems are suspected compromised** beyond original scope:
  - Recommend: **Trace** — `spectra-digital-forensics` workflow
  - "Forensic analysis of newly identified systems {{list}} would confirm or rule out compromise and ensure eradication scope is complete."

- **If attribution or campaign context matters** for defense improvement:
  - Recommend: **Oracle** — `spectra-threat-intel-workflow`
  - "Threat intelligence correlation on the IOCs and TTPs observed could identify the threat actor, their typical persistence mechanisms, and additional indicators to hunt for."

- **If the incident may be part of a broader campaign:**
  - "The TTPs, infrastructure, and timing suggest this may be part of a broader campaign. Recommend coordinating with threat intelligence to identify other potential targets or ongoing operations."

Present recommendations to the operator:

"**Specialist Recommendations:**

| Recommendation | Workflow | Rationale | Priority |
|---------------|----------|-----------|----------|
| {{recommendation}} | {{workflow}} | {{rationale}} | Critical/High/Medium |

These are recommendations — the operator decides whether to invoke additional workflows."

### 7. Update Frontmatter

Update the output file frontmatter with eradication results:

- `eradication_status`: 'complete' (if all verification passed) or 'partial' (if some systems still pending)
- `eradication_timestamp`: timestamp when eradication verification was completed
- `persistence_mechanisms`: update count with final number of mechanisms eradicated
- Add `step-07-eradication.md` to `stepsCompleted` array

### 8. Append to Report

Write the eradication findings under the `## Eradication Plan` section of `{outputFile}`:

**### Eradication Strategy**
- Selected approach (surgical/rebuild/hybrid) with justification per system
- Decision matrix

**### Malware Removal Actions**
- Complete log of malware and tool removal actions with verification

**### Persistence Cleanup Actions**
- Complete log of persistence mechanism removal with verification

**### Vulnerability Remediation**
- Root cause vulnerability patching status
- Configuration changes to address the initial access vector

**### Configuration Hardening**
- Infrastructure modifications reverted
- Security configurations restored or improved
- Credential resets executed with timeline

**### Eradication Verification**
- Complete verification checklist with all six verification methods
- Verification decision (all clean / failures identified)

**### Eradication Timeline**
- Chronological log of all eradication actions with timestamps

### 9. Present MENU OPTIONS

"**Eradication phase {{complete/in-progress}}.**

{{If complete:}}
All systems have passed eradication verification. The environment is clear of identified attacker presence, persistence mechanisms, and compromised credentials. Enhanced monitoring should be deployed before returning systems to production.

{{If partial:}}
Eradication is in progress. {{count}} systems have passed verification, {{count}} systems require additional eradication cycles. Recovery cannot begin for systems that have not passed verification.

**Select an option:**
[A] Advanced Elicitation — Challenge the eradication completeness: probe for gaps in the verification methodology, missed persistence categories, credential reset coverage holes, or infrastructure modifications that may have been overlooked
[W] War Room — Red vs Blue discussion: Red Team perspective on how an adversary would maintain access despite this eradication plan, what backup persistence mechanisms a sophisticated attacker would deploy, and whether the eradication scope is sufficient vs Blue Team perspective on verification confidence, monitoring adequacy for detecting re-compromise, and readiness for recovery
[C] Continue — Proceed to Step 8: Recovery & Restoration (Step 8 of 10)"

#### Menu Handling Logic:

- IF A: Invoke deep analysis of eradication completeness — probe for categories of persistence not addressed, credential types not included in resets, infrastructure modifications that may have been missed, verification methods that may have blind spots, timing windows where the attacker could have established new persistence. Challenge each verification method: is IOC scanning sufficient if the attacker uses polymorphic malware? Is network monitoring sufficient if the attacker uses legitimate cloud services for C2? Is the credential reset scope wide enough? Process insights, ask operator if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke War Room discussion — Red Team perspective: if I were the attacker and I knew eradication was happening, what would I have prepared? Backup persistence mechanisms not in the usual locations. Compromised accounts not yet used. Modified legitimate software that passes hash verification. Cloud persistence outside the organization's direct control. Social engineering paths back in. Blue Team perspective: what is our verification confidence level? Where are the blind spots? What monitoring should be in place before recovery? How long should we monitor before declaring eradication complete? What indicators would tell us eradication failed? Summarize insights, ask operator if they want to note anything, redisplay menu
- IF C: Verify eradication_status is 'complete' — if 'partial', WARN the operator that proceeding to recovery with incomplete eradication risks re-compromise and recommend completing eradication first. If operator confirms proceed anyway, document the decision and risk acceptance. Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-08-recovery.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, eradication_status set, eradication_timestamp recorded if complete, persistence_mechanisms count updated, and Eradication Plan section populated], will you then read fully and follow: `./step-08-recovery.md` to begin recovery and restoration.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Complete eradication inventory created from deep analysis findings covering all four categories (persistence, credentials, malware/tools, infrastructure modifications)
- Eradication strategy selected per system with documented justification (surgical/rebuild/hybrid)
- Credential reset plan prepared with correct sequencing and timing
- krbtgt double-reset protocol documented and executed correctly (if applicable)
- All eradication phases executed in sequence with per-action logging (timestamp, executor, method, verification, result)
- Containment verified as holding before eradication began
- Evidence preservation confirmed before any destructive eradication actions
- All six verification methods applied to each affected system
- Verification decision gate properly applied — no system proceeds to recovery without passing all checks
- Failed verification triggers re-analysis and re-eradication cycle (not a skip)
- Specialist recommendations provided where appropriate (Scalpel, Trace, Oracle)
- Frontmatter updated with eradication_status, eradication_timestamp, persistence_mechanisms count
- Eradication Plan section fully populated in output document with strategy, actions, verification, and timeline
- Operator informed and confirmed at every decision point
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Proceeding to recovery without complete eradication verification on all systems
- Skipping credential resets or resetting in wrong sequence
- Executing krbtgt reset without verifying AD replication health and preparing monitoring
- Not preserving evidence before destructive eradication actions
- Not verifying containment is holding before beginning eradication
- Accepting failed verification checks without re-eradication
- Missing persistence categories in the eradication inventory
- Not logging eradication actions with timestamp, executor, and verification
- Beginning recovery or service restoration during eradication
- Generating eradication content without operator input and confirmation
- Not coordinating credential resets with service owners (causing unplanned outages)
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with eradication_status and stepsCompleted
- Destroying evidence during eradication without explicit operator approval

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Eradication must be thorough, verified, and documented — an incomplete eradication guarantees the attacker's return. Evidence integrity must be maintained throughout. No recovery without verified eradication.
