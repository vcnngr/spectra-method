# Step 8: Recovery & Restoration

**Progress: Step 8 of 10** — Next: Post-Incident Review & Lessons Learned

## STEP GOAL:

Execute a controlled recovery process to restore affected systems and services to full production operation with enhanced monitoring, ensuring no re-compromise occurs and business operations resume safely following verified eradication.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INCIDENT RESPONSE COORDINATOR, not an autonomous response tool
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Incident Response Coordinator managing the recovery phase of an active security incident under NIST 800-61
- ✅ Recovery is where the organization transitions from incident response back to normal operations — it must be controlled, phased, and monitored
- ✅ A rushed recovery undoes the work of containment and eradication — the attacker may have left dormant access that activates when systems return to production
- ✅ Enhanced monitoring is not optional during recovery — it is the early warning system that validates eradication was successful
- ✅ Every restored system must be validated before and after reconnection to the production environment
- ✅ Business owners must confirm service restoration — technical recovery is necessary but not sufficient
- ✅ Data integrity is paramount — restoring corrupted or tampered data into production can cause cascading failures

### Step-Specific Rules:

- 🎯 Focus only on recovery planning, phased restoration execution, monitoring deployment, and validation — no post-incident review yet
- 🚫 FORBIDDEN to look ahead to future steps or begin post-incident analysis
- 🚫 FORBIDDEN to begin recovery on any system where eradication verification failed (check step 7 results)
- 🚫 FORBIDDEN to skip observation periods between recovery phases — these are detection windows for re-compromise
- 📝 Log every recovery action with timestamp, executor, validation result, and business owner confirmation
- ⏱️ Track recovery time per system and per service — this data feeds into post-incident metrics
- 🔍 Enhanced monitoring must be deployed BEFORE systems are returned to production, not after
- 📊 Recovery is measured by business service restoration, not just technical system availability

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Restoring from backups without verifying they are pre-compromise risks re-introducing the attacker's persistence into the clean environment — backup integrity must be confirmed against the incident timeline before restoration
  - Skipping the observation period between recovery phases to accelerate business restoration risks missing re-compromise indicators that only manifest under production load and real user activity patterns
  - Not deploying enhanced monitoring before returning systems to production means you have no early warning if eradication was incomplete — the observation period is meaningless without the instrumentation to observe
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of current state before taking any action
- 💾 Update document structure and frontmatter appropriately
- Update frontmatter: add this step name to the end of the stepsCompleted array
- Update frontmatter: `recovery_status` as work progresses ('in-progress' at start, 'complete' or 'in_progress' at end)
- Update frontmatter: `recovery_timestamp` when recovery is verified complete
- Update frontmatter: `incident_status` to 'recovered' when all systems restored
- ⏱️ Record all recovery actions with precise timestamps and business owner confirmations
- 🔗 Cross-reference recovery actions with eradication verification results from step 7
- 🚫 FORBIDDEN to load next step until user selects 'C' (Continue)
- 🚫 FORBIDDEN to declare recovery complete without business owner validation

## CONTEXT BOUNDARIES:

- Available context: Eradication verification results (step 7), containment actions (step 4), evidence inventory (step 5), deep analysis findings (step 6), full incident timeline, affected systems inventory, IOC inventory, MITRE ATT&CK mapping, credential reset status, infrastructure modification reversal status
- Focus: Controlled system restoration with enhanced monitoring, phased rollout, validation, and business acceptance
- Limits: Do not begin post-incident review or lessons learned — that is step 9. Do not restore systems that failed eradication verification. Do not skip observation periods.
- Dependencies: Step 7 (eradication) must be verified complete for all systems being recovered. Enhanced monitoring infrastructure must be deployable. Backup integrity must be verified.

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Recovery Readiness Assessment

Before any system is restored to production, verify that all prerequisites are met. This is the gate between eradication and recovery — no exceptions, no shortcuts.

**Pre-Recovery Checklist:**

```
| # | Requirement | Verification Method | Status | Verified By | Notes |
|---|-------------|--------------------|--------|-------------|-------|
| 1 | Eradication verified complete (all systems clean per step 7) | Review step 7 verification checklist — all systems must show ✅ Clean | ✅/❌ | {{handler}} | {{notes}} |
| 2 | Root cause addressed (vulnerability patched, misconfiguration fixed, initial access vector closed) | Verify patch/fix applied on all systems in scope | ✅/❌ | {{handler}} | {{notes}} |
| 3 | Credential resets confirmed effective (no authentication with old credentials) | Review step 7 credential verification results | ✅/❌ | {{handler}} | {{notes}} |
| 4 | No active C2 communications detected (monitoring period passed clean) | Review network monitoring from step 7 verification | ✅/❌ | {{handler}} | {{notes}} |
| 5 | Backup integrity verified (pre-compromise backups identified and tested) | Test restore of selected backups, verify data integrity | ✅/❌ | {{handler}} | {{notes}} |
| 6 | Enhanced monitoring ready for deployment (rules, alerts, dashboards prepared) | Verify monitoring infrastructure operational | ✅/❌ | {{handler}} | {{notes}} |
| 7 | Recovery plan approved by incident lead and business owners | Documented approval with stakeholder sign-off | ✅/❌ | {{approver}} | {{notes}} |
| 8 | Rollback plan prepared (if recovery introduces issues) | Document rollback procedures per system | ✅/❌ | {{handler}} | {{notes}} |
```

**Root Cause Remediation Verification:**

The initial access vector and root cause must be addressed before recovery, otherwise restored systems are immediately vulnerable to the same attack:

- **Vulnerability-based initial access:**
  - Patch applied to all affected systems? Version verified?
  - Compensating controls in place for systems that cannot be immediately patched?
  - External-facing instances of the vulnerability identified and patched?

- **Credential-based initial access:**
  - Compromised credentials reset (covered in step 7)?
  - MFA enforced on the access path used by the attacker?
  - Access controls tightened to prevent credential reuse?

- **Misconfiguration-based initial access:**
  - Misconfiguration corrected on all instances?
  - Configuration baseline updated to prevent recurrence?
  - Configuration monitoring in place to detect future drift?

- **Supply chain / third-party initial access:**
  - Compromised software/update removed?
  - Vendor notified and response confirmed?
  - Alternative supply chain controls implemented?

- **Social engineering initial access:**
  - Targeted users briefed on the specific social engineering technique used?
  - Additional email/web filtering rules deployed?
  - Awareness training scheduled for the affected team/organization?

**Backup Integrity Verification:**

Backups are the foundation of recovery. A compromised backup reintroduces the attacker.

- Identify the last known clean backup for each system (backup date must be BEFORE the earliest confirmed compromise date from the incident timeline)
- Test restore of selected backups in an isolated environment
- Scan restored data for known IOCs from this incident
- Verify database integrity (consistency checks, referential integrity)
- Verify file integrity against known-good checksums where available
- If no pre-compromise backup exists: document the gap and plan for data reconstruction

```
| System | Last Clean Backup Date | Incident Compromise Date | Backup Verified Clean | Test Restore Successful | Data Loss Window | Notes |
|--------|----------------------|-------------------------|----------------------|------------------------|-----------------|-------|
| {{host}} | {{backup_date}} | {{compromise_date}} | ✅/❌ | ✅/❌ | {{days/hours}} | {{notes}} |
| ... | ... | ... | ... | ... | ... | ... |
```

**If ANY pre-recovery check fails:**

"**RECOVERY BLOCKED — Prerequisites not met.**

Failed checks:
{{list of failed checks with details}}

Required actions before recovery can proceed:
{{specific actions needed to resolve each failed check}}

Recovery cannot begin until all prerequisites are satisfied. This protects the organization from re-compromise and ensures restored systems are secure."

**HALT — Do not proceed to recovery planning until all checks pass or the operator explicitly accepts the risk with documented justification.**

If the operator chooses to proceed with known gaps, document:
- Which check(s) are being accepted as incomplete
- The risk this introduces
- The operator's justification for accepting the risk
- Compensating controls that will be applied

### 2. Recovery Prioritization

Not all systems recover simultaneously. Prioritization ensures critical business operations resume first, with each tier serving as a validation gate for the next.

**Recovery Tier Classification:**

Classify each affected system into recovery tiers based on business criticality:

**Tier 1 — Critical (Restore First):**
- Core business operations and revenue-generating systems
- Safety-critical systems (SCADA, medical devices, life safety)
- Authentication infrastructure (domain controllers, identity providers, MFA systems)
- Core network services (DNS, DHCP, core routing)
- Customer-facing systems with SLA obligations
- **Recovery target:** Within 4-8 hours of recovery start
- **Observation period:** Minimum 4 hours before proceeding to Tier 2

**Tier 2 — Important (Restore Second):**
- Business support systems (ERP, CRM, HR systems)
- Email and collaboration platforms
- Internal communication systems
- Secondary authentication services
- Monitoring and logging infrastructure (needed for observing recovery)
- **Recovery target:** Within 12-24 hours of recovery start
- **Observation period:** Minimum 2 hours before proceeding to Tier 3

**Tier 3 — Standard (Restore Third):**
- Development and staging environments
- Non-critical internal tools and utilities
- Backup and archive systems
- Training and test environments
- **Recovery target:** Within 48-72 hours of recovery start
- **Observation period:** Standard monitoring, no mandatory hold

**Tier 4 — Deferred (Schedule for Later):**
- Low-priority systems that can wait for scheduled maintenance
- Systems being decommissioned or replaced
- Redundant systems where primary is already restored
- Systems requiring hardware procurement or extended rebuild
- **Recovery target:** Scheduled during next maintenance window

**Per-System Recovery Plan:**

```
| System | Business Service | Tier | Recovery Method | Data Source | Backup Date | Owner/Contact | Dependencies | ETA | Rollback Plan |
|--------|-----------------|------|-----------------|-------------|-------------|---------------|-------------|-----|---------------|
| {{host}} | {{service}} | 1 | Restore from backup / Rebuild from IaC / Redeploy from source / Patch and return | {{source}} | {{date}} | {{owner}} | {{deps}} | {{hours}} | {{rollback}} |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

**Recovery Methods Explained:**

- **Restore from verified clean backup:** Restore full system image or data from a verified pre-compromise backup. Use when: system was rebuilt in eradication phase and needs data restored, or system can be reverted to backup state.

- **Rebuild from IaC/golden image + restore data only:** Rebuild the system from infrastructure-as-code templates or verified golden images, then restore only data (not system binaries or configurations) from backup. Use when: system binaries may have been modified, highest confidence approach.

- **Redeploy from source control:** Rebuild application layer from source code repository (verified clean branch). Use when: application servers where code integrity is critical, containerized workloads.

- **Patch and return:** Apply security patches and configuration fixes to the existing system (which was surgically cleaned in step 7). Use when: system was surgically cleaned with high confidence, rebuild is not feasible, system cannot be taken offline for rebuild.

Present the recovery plan to the operator:

"**Recovery Plan Summary:**

| Tier | Systems | Recovery Method | Estimated Timeline |
|------|---------|-----------------|-------------------|
| Tier 1 (Critical) | {{count}} systems | {{methods}} | {{timeline}} |
| Tier 2 (Important) | {{count}} systems | {{methods}} | {{timeline}} |
| Tier 3 (Standard) | {{count}} systems | {{methods}} | {{timeline}} |
| Tier 4 (Deferred) | {{count}} systems | {{methods}} | Scheduled: {{date}} |

**Total estimated recovery timeline:** {{hours/days}}
**Expected business impact during recovery:** {{summary}}
**Data loss window:** {{earliest backup date}} to {{incident detection date}}

Approve the recovery plan to begin phased restoration?"

Wait for operator confirmation before proceeding.

### 3. Data Restoration Planning

Data restoration requires careful handling to avoid reintroducing compromised data or losing data integrity.

**Backup Selection & Verification:**

For each system requiring data restoration:

1. **Identify candidate backups:**
   - List all available backups with dates
   - Identify the last backup BEFORE the confirmed compromise date (from incident timeline)
   - If compromise date is uncertain, use the earliest possible compromise date with safety margin

2. **Verify backup integrity:**
   - Check backup checksums/hashes against backup catalog
   - Perform test restore in an isolated environment (NOT on production systems)
   - Scan restored data for known IOCs from this incident (file hashes, malware signatures, attacker artifacts)
   - Verify database consistency (run DBCC CHECKDB for SQL Server, pg_dump --check for PostgreSQL, mysqlcheck for MySQL)
   - Verify application data integrity (referential integrity, data validation checks)

3. **Assess data loss window:**
   - Calculate the time between the selected backup and the incident detection time
   - Identify what data was created/modified during this gap period
   - Determine if any of the gap data can be recovered from:
     - Transaction logs (database point-in-time recovery)
     - Replication partners (if not also compromised)
     - User-side copies (local caches, email attachments, exported reports)
     - Cloud sync services (OneDrive, SharePoint, Google Drive — verify clean)
   - Document the data loss for business owner acknowledgment

4. **Data tampering assessment:**
   - Did the attacker modify data (not just steal it)?
   - If data tampering is suspected, compare restored data against known-good references
   - If tampered data was propagated to downstream systems, those systems also need data correction
   - Flag any data integrity concerns for business owner review

Present the data restoration plan:

```
| System | Database/Data Store | Backup Selected | Backup Date | Data Loss Window | IOC Scan Result | Integrity Check | Gap Recovery Method | Business Owner Acknowledged |
|--------|--------------------|-----------------|----|-----------------|-----------------|-----------------|--------------------|-----------------------------|
| {{host}} | {{datastore}} | {{backup_id}} | {{date}} | {{window}} | Clean/Failed | Pass/Fail | {{method or 'N/A'}} | Pending |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

"**Data Restoration Plan:**

**Total data loss window:** {{earliest gap}} to {{incident detection}}
**Systems requiring data restoration:** {{count}}
**Gap recovery possible for:** {{count}} systems (via {{methods}})
**Unrecoverable data loss:** {{count}} systems — {{summary of lost data}}

Business owners must acknowledge data loss before restoration proceeds. Confirm the data restoration plan?"

### 4. Phased Restoration Execution

Recovery proceeds in phases, with mandatory observation periods between each phase. Each phase serves as a validation gate — issues detected in one phase are resolved before the next phase begins.

**Pre-Phase Preparation (Before All Phases):**

- Deploy enhanced monitoring infrastructure (if not already in place from step 7)
- Configure alerting thresholds for recovered systems (lower thresholds = higher sensitivity during recovery)
- Prepare communication templates for stakeholder status updates
- Assign monitoring responsibilities for each phase
- Establish escalation criteria: what conditions trigger a recovery halt?

**Recovery Escalation Criteria (Apply to ALL Phases):**

If ANY of the following occur during a recovery phase, HALT the phase immediately:

- C2 beaconing detected from any recovered system
- Authentication with pre-reset (compromised) credentials detected
- New malware or persistence mechanism detected on a recovered system
- Anomalous outbound network traffic from recovered systems
- Unauthorized configuration changes on recovered systems
- Evidence of data exfiltration activity
- Unexpected service behavior inconsistent with normal operations

"**If escalation criteria are triggered:** HALT recovery immediately. Do NOT restore additional systems. Re-enter eradication (step 7) for the affected system(s). Notify the operator with full details."

---

**Phase 1: Critical Systems (Tier 1)**

Execute Tier 1 system recovery:

1. **Deploy enhanced monitoring** for Tier 1 systems BEFORE restoration begins
   - SIEM alert rules for incident-specific IOCs
   - EDR enhanced monitoring mode (increased telemetry)
   - Network monitoring for C2 indicators at the segment level
   - Authentication monitoring for compromised account patterns
   - File integrity monitoring on critical system files

2. **Restore Tier 1 systems** following the per-system recovery plan:
   - Execute the selected recovery method (backup restore, IaC rebuild, source redeploy, patch and return)
   - Apply all current security patches before network reconnection
   - Verify system configuration matches hardened baseline
   - Reconnect to network with enhanced monitoring active

3. **Validate Tier 1 functionality:**
   - Verify core service availability (application responds, database accessible, authentication functional)
   - Run integration tests if available
   - Verify network connectivity to required dependencies
   - Confirm DNS resolution and service discovery
   - Verify backup and recovery services for the restored systems

4. **Monitor Tier 1 systems:**
   - **Minimum observation period: 4 hours**
   - Check monitoring dashboards every 15 minutes during the first hour
   - Check monitoring dashboards every 30 minutes for the remaining 3 hours
   - Review all alerts generated during the observation period
   - Verify no escalation criteria have been triggered

5. **Tier 1 phase gate:**
   - All Tier 1 systems operational? ✅/❌
   - Enhanced monitoring active and generating expected telemetry? ✅/❌
   - No escalation criteria triggered? ✅/❌
   - No anomalous activity detected? ✅/❌
   - Business owners confirm service availability? ✅/❌

Phase 1 execution log:

```
| Seq | System | Recovery Action | Method | Executed By | Timestamp | Monitoring Active | Functionality Verified | Business Owner Confirmed | Issues | Status |
|-----|--------|----------------|--------|-------------|-----------|-------------------|----------------------|------------------------|--------|--------|
| 1 | {{host}} | {{action}} | {{method}} | {{handler}} | {{ts}} | ✅/❌ | ✅/❌ | ✅/❌ | {{issues}} | Complete/Failed |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

"**Phase 1 (Critical Systems) {{Complete/In-Progress}}**

Systems restored: {{count}} of {{total Tier 1}}
Observation period: {{elapsed}} of 4 hours minimum
Escalation criteria triggered: {{Yes/No}}
Anomalous activity: {{None / Details}}
Business owner confirmations: {{count}} of {{total}}

{{If all clear:}} Phase 1 gate passed. Ready to proceed to Phase 2.
{{If issues:}} Phase 1 gate BLOCKED. Issues requiring resolution: {{details}}"

Wait for operator confirmation before proceeding to Phase 2.

---

**Phase 2: Important Systems (Tier 2)**

Execute Tier 2 system recovery:

1. **Extend enhanced monitoring** to cover Tier 2 systems
   - Apply the same monitoring configuration as Phase 1
   - Ensure monitoring covers integration points between Tier 1 and Tier 2 systems

2. **Restore Tier 2 systems** following the per-system recovery plan:
   - Execute selected recovery method
   - Apply all current security patches
   - Verify system configuration matches hardened baseline
   - Reconnect to network with enhanced monitoring active

3. **Validate Tier 2 functionality:**
   - Verify service availability
   - Verify integration with restored Tier 1 systems (data flows, authentication, API connectivity)
   - Run integration tests if available
   - Verify email flow if email systems are in Tier 2
   - Confirm collaboration tools are operational if in Tier 2

4. **Monitor Tier 2 systems:**
   - **Minimum observation period: 2 hours**
   - Check monitoring dashboards every 30 minutes
   - Review all alerts generated during observation
   - Verify no escalation criteria triggered
   - Verify Tier 1 systems remain stable with Tier 2 systems reconnected

5. **Tier 2 phase gate:**
   - All Tier 2 systems operational? ✅/❌
   - Integration with Tier 1 systems verified? ✅/❌
   - Enhanced monitoring active and generating expected telemetry? ✅/❌
   - No escalation criteria triggered? ✅/❌
   - Tier 1 systems remain stable? ✅/❌
   - Business owners confirm service availability? ✅/❌

Phase 2 execution log:

```
| Seq | System | Recovery Action | Method | Executed By | Timestamp | Monitoring Active | Functionality Verified | Integration Verified | Business Owner Confirmed | Issues | Status |
|-----|--------|----------------|--------|-------------|-----------|-------------------|----------------------|---------------------|------------------------|--------|--------|
| 1 | {{host}} | {{action}} | {{method}} | {{handler}} | {{ts}} | ✅/❌ | ✅/❌ | ✅/❌ | ✅/❌ | {{issues}} | Complete/Failed |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

"**Phase 2 (Important Systems) {{Complete/In-Progress}}**

Systems restored: {{count}} of {{total Tier 2}}
Observation period: {{elapsed}} of 2 hours minimum
Tier 1 systems stable: ✅/❌
Escalation criteria triggered: {{Yes/No}}
Business owner confirmations: {{count}} of {{total}}

{{If all clear:}} Phase 2 gate passed. Ready to proceed to Phase 3.
{{If issues:}} Phase 2 gate BLOCKED. Issues requiring resolution: {{details}}"

Wait for operator confirmation before proceeding to Phase 3.

---

**Phase 3: Standard & Deferred Systems (Tiers 3 & 4)**

Execute Tier 3 system recovery (Tier 4 systems are scheduled for later):

1. **Extend enhanced monitoring** to cover Tier 3 systems
   - Standard monitoring configuration with incident-specific detection rules

2. **Restore Tier 3 systems** following the per-system recovery plan:
   - Execute selected recovery method
   - Apply all current security patches
   - Verify system configuration matches hardened baseline
   - Reconnect to network

3. **Validate Tier 3 functionality:**
   - Verify service availability
   - Full integration testing with Tier 1 and Tier 2 systems
   - Verify development and staging environments are functional
   - Confirm data integrity in restored environments

4. **Monitor Tier 3 systems:**
   - Standard monitoring with enhanced alerting for incident-specific indicators
   - No mandatory observation hold — but continue monitoring

5. **Schedule Tier 4 systems:**
   - Document the scheduled recovery date for each Tier 4 system
   - Assign owners responsible for the deferred recovery
   - Set calendar reminders for follow-up
   - Document any interim compensating controls for deferred systems

Phase 3 execution log:

```
| Seq | System | Tier | Recovery Action | Method | Executed By | Timestamp | Functionality Verified | Integration Verified | Status |
|-----|--------|------|----------------|--------|-------------|-----------|----------------------|---------------------|--------|
| 1 | {{host}} | 3 | {{action}} | {{method}} | {{handler}} | {{ts}} | ✅/❌ | ✅/❌ | Complete/Deferred |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
```

"**Phase 3 (Standard Systems) {{Complete/In-Progress}}**

Tier 3 systems restored: {{count}} of {{total Tier 3}}
Tier 4 systems deferred: {{count}} — scheduled for {{dates}}
All tiers integrated: ✅/❌
Enhanced monitoring active across all tiers: ✅/❌"

### 5. Enhanced Monitoring Deployment

Enhanced monitoring is the safety net that validates eradication was successful. It must be comprehensive, tuned to this specific incident, and maintained for a defined period.

**Monitoring Enhancements — Deploy for ALL Recovered Systems:**

**A. Incident-Specific Detection Rules:**

- SIEM rules based on all IOCs from this incident:
  - Network IOCs: C2 IPs, domains, URLs — alert on any connection attempt
  - Host IOCs: file hashes, file paths, registry keys, process names — alert on any match
  - Behavioral IOCs: specific command-line patterns, PowerShell scripts, lateral movement techniques
  
- Sigma rules created or adapted for the MITRE ATT&CK techniques observed:
  - Detection rules for each technique in the attack chain
  - Detection rules for the specific tools used by the attacker
  - Detection rules for the persistence mechanisms that were eradicated

- YARA rules for malware families identified in the incident:
  - Scan all file writes on recovered systems against incident-specific YARA rules
  - Deploy YARA scanning on network perimeter for file transfers

**B. Enhanced Logging Configuration:**

- Increase logging verbosity on recovered systems temporarily:
  - Windows: enable PowerShell Script Block Logging, Module Logging, and Transcription
  - Windows: enable command-line process auditing (Event ID 4688)
  - Windows: enable WMI activity logging
  - Linux: enable auditd with comprehensive syscall monitoring
  - Network: enable full packet capture on segments with recovered systems (if capacity allows)
  - Cloud: ensure CloudTrail/audit logging covers all recovered services with no gaps
  
- Centralize all logs from recovered systems to SIEM with priority ingestion
- Set log retention for recovery period: minimum 90 days for incident-related logs

**C. Network Monitoring:**

- Monitor for C2 indicators specific to this incident at network perimeter
- Deploy network-based detection (IDS/IPS signatures) for attacker tools and malware
- Monitor DNS queries from recovered systems for known malicious domains
- Monitor for anomalous outbound traffic patterns (beaconing, data exfiltration indicators)
- Monitor for lateral movement indicators between recovered systems
- If applicable: deploy network traffic analysis (NTA) for encrypted traffic anomaly detection

**D. Authentication Monitoring:**

- Monitor for authentication with pre-reset credentials (should be impossible — any success is a critical alert)
- Monitor for pass-the-hash / pass-the-ticket activity patterns
- Monitor for Kerberos anomalies (unusual ticket requests, golden/silver ticket indicators)
- Monitor for authentication from unusual source IPs or locations
- Monitor for authentication to accounts that were disabled during eradication
- Monitor for privilege escalation patterns observed during the incident

**E. File Integrity Monitoring (FIM):**

- Deploy FIM on all recovered systems covering:
  - System binaries and DLLs
  - Configuration files
  - Web application directories (if web shells were found)
  - Startup locations (startup folder, registry run keys, cron directories)
  - Scheduled task definitions
  - SSH authorized_keys files
- Alert on ANY file change in monitored locations during recovery period

**F. Endpoint Detection & Response (EDR) Enhancements:**

- Set EDR to enhanced detection mode on recovered systems
- Create custom detection rules for attacker TTPs specific to this incident
- Enable memory scanning on recovered endpoints
- Set alerting threshold to low/verbose for recovery period
- Ensure EDR agent is operational on ALL recovered systems (verify agent health)

**Monitoring Duration & Reduction Schedule:**

```
| Monitoring Type | Recovery Period (0-14 days) | Extended Period (14-30 days) | Steady State (30+ days) | Review Date |
|-----------------|---------------------------|-----------------------------|-----------------------|-------------|
| Incident-specific IOC alerts | Active — all IOCs | Active — all IOCs | Retain top indicators | Day 30 |
| Enhanced logging verbosity | Full verbosity | Reduce to critical events | Standard + incident rules | Day 14 |
| Network monitoring (C2 patterns) | Active — all patterns | Active — key patterns | Integrate into standard | Day 30 |
| Authentication monitoring | Active — all pre-reset creds | Active — anomaly-based | Standard + incident patterns | Day 30 |
| File integrity monitoring | Active — all locations | Active — critical locations | Standard FIM | Day 14 |
| EDR enhanced mode | Enhanced — all endpoints | Enhanced — recovered only | Standard + custom rules | Day 14 |
| Threat hunting cadence | Twice weekly | Weekly | Monthly | Day 30 |
| Monitoring review meetings | Daily | Twice weekly | As needed | Day 14 |
```

**Active Threat Hunting Schedule:**

- **Week 1-2:** Twice-weekly targeted threat hunts on recovered systems
  - Hunt for IOCs from this incident
  - Hunt for attacker TTPs on adjacent systems
  - Hunt for new persistence mechanisms
  - Hunt for data staging or exfiltration activity

- **Week 3-4:** Weekly threat hunts
  - Broader scope: include systems not directly affected
  - Focus on detection gaps identified during the incident
  - Hunt for campaign-related indicators from threat intelligence

- **Month 2-3:** Monthly threat hunts
  - Standard threat hunting cadence with incident-informed hunt hypotheses
  - Review and update detection rules based on hunt findings
  - Transition incident-specific hunts into standard hunting program

Present the monitoring plan:

"**Enhanced Monitoring Plan:**

| Monitoring Category | Coverage | Duration | Responsible Party | First Review |
|--------------------|---------|----------|-------------------|-------------|
| IOC-based detection | {{count}} IOCs across {{count}} systems | 30 days minimum | {{team}} | Day 7 |
| Enhanced logging | {{count}} systems at full verbosity | 14 days, then reduce | {{team}} | Day 14 |
| Network monitoring | {{count}} C2 patterns monitored | 30 days minimum | {{team}} | Day 7 |
| Authentication monitoring | All recovered accounts | 30 days minimum | {{team}} | Day 7 |
| File integrity monitoring | {{count}} systems, {{count}} paths | 14 days full, then reduce | {{team}} | Day 14 |
| EDR enhanced mode | {{count}} endpoints | 14 days full, then reduce | {{team}} | Day 14 |
| Threat hunting | Twice weekly → weekly → monthly | 3 months | {{team}} | Week 1 |

Confirm the monitoring plan, or adjust coverage and duration?"

### 6. Validation & Acceptance

Recovery is not complete until both technical validation and business acceptance are confirmed.

**Technical Validation Checklist:**

```
| # | Validation Item | Method | Status | Verified By | Timestamp |
|---|----------------|--------|--------|-------------|-----------|
| 1 | All Tier 1 systems operational and monitored | Service checks + monitoring telemetry | ✅/❌ | {{handler}} | {{ts}} |
| 2 | All Tier 2 systems operational and integrated with Tier 1 | Integration tests + service checks | ✅/❌ | {{handler}} | {{ts}} |
| 3 | All Tier 3 systems restored or scheduled (Tier 4) | Inventory reconciliation | ✅/❌ | {{handler}} | {{ts}} |
| 4 | No anomalous activity during observation periods | Monitoring review | ✅/❌ | {{handler}} | {{ts}} |
| 5 | No escalation criteria triggered during any phase | Alert review | ✅/❌ | {{handler}} | {{ts}} |
| 6 | Enhanced monitoring active and generating expected telemetry | Monitoring dashboard check | ✅/❌ | {{handler}} | {{ts}} |
| 7 | No re-compromise indicators detected | Threat hunt + monitoring review | ✅/❌ | {{handler}} | {{ts}} |
| 8 | Root cause vulnerability remediated on all systems | Patch verification scan | ✅/❌ | {{handler}} | {{ts}} |
| 9 | Credential resets holding (no pre-reset credential auth) | Authentication monitoring review | ✅/❌ | {{handler}} | {{ts}} |
| 10 | Data integrity confirmed on restored systems | Integrity checks per system | ✅/❌ | {{handler}} | {{ts}} |
```

**Business Acceptance Checklist:**

```
| # | Business Validation Item | Owner | Status | Confirmed By | Timestamp |
|---|------------------------|-------|--------|-------------|-----------|
| 1 | Service level targets met (response time, availability, throughput) | {{service_owner}} | ✅/❌ | {{name}} | {{ts}} |
| 2 | Data integrity confirmed by business owners (no data corruption, no missing records beyond documented loss window) | {{data_owner}} | ✅/❌ | {{name}} | {{ts}} |
| 3 | User access restored appropriately (correct permissions, no excess access) | {{access_owner}} | ✅/❌ | {{name}} | {{ts}} |
| 4 | Performance within acceptable parameters (no degradation vs pre-incident baseline) | {{ops_owner}} | ✅/❌ | {{name}} | {{ts}} |
| 5 | Customer-facing services confirmed operational (if applicable) | {{customer_ops}} | ✅/❌ | {{name}} | {{ts}} |
| 6 | Business workflows functional end-to-end (order processing, data pipelines, reporting, etc.) | {{business_ops}} | ✅/❌ | {{name}} | {{ts}} |
| 7 | Communication to stakeholders: recovery complete notification sent | {{comms_lead}} | ✅/❌ | {{name}} | {{ts}} |
| 8 | Data loss acknowledged by affected business units | {{business_units}} | ✅/❌ | {{name}} | {{ts}} |
```

"**Validation & Acceptance Summary:**

**Technical validation:** {{count}}/10 checks passed
**Business acceptance:** {{count}}/8 checks confirmed

{{If all passed:}}
Recovery validated and accepted. All systems are operational, monitored, and confirmed by business owners.

{{If any failed:}}
Outstanding items:
{{list of failed items with remediation plan}}

These items must be resolved or accepted as known gaps before recovery can be declared complete."

### 7. Recovery Situation Report

Compile the final recovery status for stakeholder communication and incident documentation:

"**RECOVERY SITUATION REPORT**

**Incident:** {{incident_id}} — {{incident_category}}
**Severity:** {{incident_severity}}
**Recovery Status:** {{Complete / In-Progress}}
**Report Date:** {{current_date}}

---

**Systems Recovered:**
| Tier | Total | Recovered | Pending | Deferred |
|------|-------|-----------|---------|----------|
| Tier 1 (Critical) | {{count}} | {{count}} | {{count}} | {{count}} |
| Tier 2 (Important) | {{count}} | {{count}} | {{count}} | {{count}} |
| Tier 3 (Standard) | {{count}} | {{count}} | {{count}} | {{count}} |
| Tier 4 (Deferred) | {{count}} | {{count}} | {{count}} | {{count}} |
| **Total** | **{{count}}** | **{{count}}** | **{{count}}** | **{{count}}** |

**Data Loss Window:** {{earliest gap start}} to {{incident detection date}} ({{duration}})
- Data recoverable: {{count}} systems via {{methods}}
- Data unrecoverable: {{count}} systems — {{summary}}

**Business Impact Duration:**
| Service | Outage Start | Service Restored | Total Outage | SLA Impact |
|---------|-------------|------------------|-------------|------------|
| {{service}} | {{start}} | {{restored}} | {{duration}} | {{within/exceeded}} SLA |
| ... | ... | ... | ... | ... |

**Key Recovery Metrics:**
- Time from detection to recovery complete: {{duration}}
- Time from eradication to recovery complete: {{duration}}
- Systems requiring rebuild vs surgical recovery: {{rebuild_count}} / {{surgical_count}}
- Recovery phases completed: {{count}} of 3
- Escalation criteria triggered during recovery: {{count}} ({{details or 'None'}})
- Business owner acceptances received: {{count}} of {{total}}

**Remaining Items:**
- Deferred systems: {{list with scheduled dates}}
- Enhanced monitoring: active for {{duration}} remaining
- Threat hunting: {{schedule}}
- Outstanding business acceptance items: {{list or 'None'}}

**Residual Risk:**
{{Document any known residual risk from recovery decisions}}
- Systems returned with accepted gaps: {{list or 'None'}}
- Data integrity concerns pending resolution: {{list or 'None'}}
- Monitoring coverage gaps: {{list or 'None'}}

**Next Phase:** Post-Incident Review & Lessons Learned (Step 9)"

### 8. Update Frontmatter

Update the output file frontmatter with recovery results:

- `recovery_status`: 'complete' (if all validation passed and business acceptance received) or 'in_progress' (if deferred items remain)
- `recovery_timestamp`: timestamp when recovery validation was completed
- `incident_status`: 'recovered' (if recovery is complete) — this reflects the incident lifecycle status transition
- Add `step-08-recovery.md` to `stepsCompleted` array

### 9. Append to Report

Write the recovery findings under the `## Recovery & Restoration` section of `{outputFile}`:

**### Recovery Strategy**
- Recovery readiness assessment results
- Root cause remediation verification
- Recovery tier classification and prioritization
- Per-system recovery method selection with justification

**### System Restoration Priority**
- Tier classification table with all affected systems
- Recovery dependencies and sequencing

**### Restoration Actions**
- Phase 1, 2, 3 execution logs with timestamps and verification
- Per-system recovery actions and results
- Issues encountered and resolutions

**### Service Re-enablement Log**
- Business services restored with timestamps
- Business owner confirmations
- SLA impact assessment

**### Monitoring Enhancement During Recovery**
- Enhanced monitoring plan with all six categories
- Detection rules deployed (IOC-based, behavioral, YARA, Sigma)
- Monitoring duration schedule
- Threat hunting schedule

**### Recovery Verification & Testing**
- Technical validation checklist results
- Business acceptance checklist results
- Residual risk documentation

**### Recovery Timeline**
- Chronological log of all recovery actions with timestamps
- Phase gate results
- Total recovery duration

### 10. Present MENU OPTIONS

"**Recovery phase {{complete/in-progress}}.**

{{If complete:}}
All systems have been restored to production operation with enhanced monitoring active. Business owners have confirmed service restoration. The environment is operating normally with heightened detection capability. The active incident response is operationally complete — the next step transitions to post-incident review and lessons learned.

{{If in-progress:}}
Recovery is in progress. Tier 1-3 systems are {{status}}, with {{count}} Tier 4 systems deferred. Enhanced monitoring is active. {{Any outstanding items.}}

**Select an option:**
[A] Advanced Elicitation — Challenge the recovery completeness: probe for systems that may have been missed in the recovery plan, data integrity concerns, monitoring gaps, business services not yet validated, or residual risks that have not been documented
[W] War Room — Red vs Blue discussion: Red Team perspective on how an attacker would test whether their access survived eradication and recovery, what dormant persistence mechanisms look like from the outside, and what the attacker's next move would be if they still have a foothold vs Blue Team perspective on monitoring confidence levels, detection gaps that remain even with enhanced monitoring, the adequacy of the observation periods, and whether the recovery plan addressed the root cause sufficiently
[C] Continue — Proceed to Step 9: Post-Incident Review & Lessons Learned (Step 9 of 10)"

#### Menu Handling Logic:

- IF A: Invoke deep analysis of recovery completeness — probe for systems that may not have been included in the recovery plan, data integrity concerns that were not fully addressed, monitoring coverage gaps (are there network segments or system types not covered?), business services that depend on recovered systems but were not explicitly validated, residual risks from recovery decisions that were not documented, rollback plans that were not tested. Challenge each recovery phase: was the observation period sufficient? Were the right things being monitored? Is the monitoring plan sustainable for 30 days? Process insights, ask operator if they accept adjustments, if yes update document then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke War Room discussion — Red Team perspective: if my persistence survived eradication, what would I do during recovery? I would stay dormant during the observation period and activate only after enhanced monitoring is reduced. I would test my access with minimal footprint — a single DNS query, a single HTTP request to a legitimate service I control. I would have multiple persistence mechanisms and only use the most stealthy one. I would check if my credential access still works by authenticating from a legitimate-looking source. Blue Team perspective: what is our detection confidence for dormant persistence? How effective is our monitoring against an attacker who knows we are watching? Are we monitoring the right indicators or just the ones we already know about? Is the 30-day monitoring period sufficient, or should certain detections be permanent? What detection gaps existed before the incident that allowed it to happen — have those been closed? Summarize insights, ask operator if they want to note anything, redisplay menu
- IF C: Verify recovery_status — if 'in_progress', inform the operator that recovery is not complete and confirm they want to proceed to post-incident review with recovery still ongoing. If operator confirms, document the decision. Update output file frontmatter adding this step name to the end of stepsCompleted array, then read fully and follow: ./step-09-post-incident.md
- IF user provides additional context: Validate and incorporate, update document, redisplay menu
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, recovery_status set, recovery_timestamp recorded if complete, incident_status updated to 'recovered' if applicable, and Recovery & Restoration section populated], will you then read fully and follow: `./step-09-post-incident.md` to begin post-incident review and lessons learned.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Pre-recovery checklist completed with all eight checks verified (or risk acceptance documented for accepted gaps)
- Root cause remediation verified before recovery began
- Backup integrity verified for all systems requiring data restoration (pre-compromise date confirmed, IOC scan clean, test restore successful)
- Recovery tier classification applied to all affected systems with business justification
- Per-system recovery plan documented with method, data source, owner, dependencies, and rollback plan
- Data loss window calculated and communicated to business owners with acknowledgment
- Phased restoration executed in correct sequence (Tier 1 → Tier 2 → Tier 3, Tier 4 deferred)
- Mandatory observation periods observed between phases (4 hours for Phase 1, 2 hours for Phase 2)
- Enhanced monitoring deployed BEFORE systems returned to production
- All six monitoring categories configured (IOC alerts, enhanced logging, network monitoring, authentication monitoring, FIM, EDR)
- Monitoring duration schedule established with review dates
- Threat hunting schedule established (twice weekly → weekly → monthly)
- Technical validation checklist completed (10 items)
- Business acceptance checklist completed (8 items) with business owner confirmations
- Recovery situation report compiled with metrics and residual risk documentation
- Per-phase execution logs maintained with timestamps and verification
- Frontmatter updated with recovery_status, recovery_timestamp, incident_status
- Recovery & Restoration section fully populated in output document
- Operator informed and confirmed at every decision point and phase gate
- Menu presented and user input handled correctly

### ❌ SYSTEM FAILURE:

- Beginning recovery without verified eradication completion
- Restoring from backups without verifying they are pre-compromise
- Skipping mandatory observation periods between recovery phases
- Not deploying enhanced monitoring before returning systems to production
- Not verifying root cause remediation before recovery
- Not obtaining business owner confirmation of service restoration
- Ignoring escalation criteria during recovery phases (C2 detection, credential reuse, new malware)
- Not calculating or communicating data loss windows to business owners
- Not preparing rollback plans before restoration
- Declaring recovery complete without both technical validation and business acceptance
- Generating recovery content without operator input and confirmation
- Skipping recovery tiers or restoring all systems simultaneously without phase gates
- Not maintaining per-phase execution logs with timestamps
- Not establishing an enhanced monitoring duration and reduction schedule
- Not scheduling post-recovery threat hunting
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with recovery_status, recovery_timestamp, and incident_status

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Recovery must be phased, monitored, and validated — a premature return to production without enhanced monitoring is indistinguishable from no eradication at all. Business acceptance is required, not optional. Evidence of successful recovery is the absence of re-compromise over a monitored observation period.
