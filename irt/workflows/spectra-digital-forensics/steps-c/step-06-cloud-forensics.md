# Step 6: Cloud & SaaS Forensic Analysis

**Progress: Step 6 of 10** — Next: Timeline Reconstruction

## STEP GOAL:

Conduct comprehensive cloud and SaaS forensic analysis — cloud platform audit log analysis (AWS/Azure/GCP), identity and access event analysis, SaaS application forensics (M365/Google Workspace), and container/Kubernetes forensics where applicable. Cloud forensics reveals the management plane activity that disk and memory analysis cannot see — API calls, identity operations, resource modifications, and cross-service interactions that constitute the cloud attack surface.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify cloud resources or configurations during analysis — read-only operations exclusively
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST, not an autonomous analysis engine
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst conducting structured cloud forensic examination under ISO 27037 and NIST SP 800-86
- ✅ Cloud forensics is fundamentally different from endpoint forensics — there are no disk images, no memory dumps; everything is log-based and API-driven
- ✅ The management plane is the primary attack surface in cloud — IAM changes, API calls, resource creation, and cross-service operations reveal the attacker's cloud-native techniques
- ✅ Identity is the new perimeter — authentication logs, OAuth grants, service principal activity, and MFA bypass attempts are the cloud equivalent of process execution and network connections
- ✅ Cloud log retention varies by service and tier — some logs are available for 90 days, some for 7 days, some require explicit enablement

### Step-Specific Rules:

- 🎯 Focus exclusively on cloud and SaaS forensic analysis: platform audit logs, identity/access analysis, SaaS forensics, container forensics
- 🚫 FORBIDDEN to perform disk, memory, or network packet analysis — those were steps 3-5
- 🚫 FORBIDDEN to modify cloud resources, IAM policies, or configurations during analysis
- 💬 Approach: Systematic cloud log analysis per platform, cross-referencing with endpoint and network findings
- 📊 Every finding must cite: evidence ID (EVD-{case_id}-{NNN}), log source, API call/event details, and confidence level
- 🔒 Re-verify working copy hash before analysis begins

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Not analyzing IAM changes (role assignments, policy modifications, service account creation) during the incident window means you will miss the attacker's privilege escalation and persistence in the cloud — an attacker who creates a backdoor IAM role or adds an access key to a service account maintains access even after the initial entry point is remediated
  - Relying solely on CloudTrail/Activity Log without correlating with data plane logs (S3 access logs, storage analytics, database audit logs) means you see the management plane but miss the data plane — the attacker's API calls to modify infrastructure are visible, but their actual data access and exfiltration operations may only appear in service-specific data plane logs
  - Not checking for OAuth application consent grants and delegated permissions in M365/Google Workspace misses a common SaaS persistence technique — an attacker who registers a malicious OAuth app with broad permissions maintains access through the application even after the compromised user's password is changed and sessions are revoked
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Verify working copy integrity before beginning analysis
- 📋 Document log sources, time windows, and query parameters for all cloud analysis
- 🔒 Cite evidence IDs for every finding
- ⚠️ Present [A]/[W]/[C] menu after cloud forensic analysis is complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Case intake, forensic question, evidence inventory, all prior analysis findings (disk, memory, network)
- Focus: Cloud platform forensics, identity/access analysis, SaaS forensics, container forensics
- Limits: If cloud evidence was classified as N/A in step 2, document the N/A status and proceed to step 7. Only analyze acquired log exports (working copies).
- Dependencies: Cloud evidence acquired in step 2, findings from steps 3-5 for cross-reference

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check & Working Copy Verification

**If cloud evidence was classified as N/A in step 2:**

"**Cloud Forensics — Not Applicable**

No cloud platform logs, SaaS audit logs, or cloud evidence was acquired for this case. Reason: {{reason_from_step_2}}.

This step is documented as N/A. Cloud-specific artifacts cannot be analyzed."

Document N/A and proceed to menu with C option.

**If cloud evidence is available:**

Re-verify working copy integrity for all cloud evidence items.

### 2. AWS Forensic Analysis (If Applicable)

**CloudTrail Event Analysis:**

CloudTrail records all AWS API calls — the authoritative source for AWS management plane activity.

**Key Event Categories to Analyze:**

**Authentication & Access:**
- `ConsoleLogin` — Console sign-in events (source IP, MFA used, result)
- `AssumeRole` — Cross-account or role-based access (who assumed what role, from where)
- `GetSessionToken` / `GetFederationToken` — Temporary credential generation
- `SwitchRole` — Console role switching
- Failed authentication events — brute force indicators

**IAM Modifications (Persistence & Privilege Escalation):**
- `CreateUser`, `CreateAccessKey`, `CreateLoginProfile` — New identity creation
- `AttachUserPolicy`, `AttachRolePolicy`, `PutUserPolicy` — Permission expansion
- `CreateRole`, `UpdateAssumeRolePolicy` — Role creation/modification
- `CreateServiceAccount`, `AddUserToGroup` — Lateral access
- `DeleteTrail`, `StopLogging`, `UpdateTrail` — Anti-forensics (disabling audit)

**Data Access & Exfiltration:**
- S3: `GetObject`, `PutObject`, `ListBucket`, `CreateBucket`, `PutBucketPolicy`
- RDS: `DescribeDBInstances`, `CreateDBSnapshot`, `RestoreDBInstanceFromDBSnapshot`
- Secrets Manager: `GetSecretValue`, `ListSecrets`
- SSM: `SendCommand`, `StartSession` — Remote command execution

**Infrastructure Modification:**
- EC2: `RunInstances`, `CreateSecurityGroup`, `AuthorizeSecurityGroupIngress` — Instance creation, firewall modification
- Lambda: `CreateFunction`, `UpdateFunctionCode` — Serverless execution
- EBS: `CreateSnapshot`, `CopySnapshot` — Data staging

**VPC Flow Log Analysis:**
- Parse flow records for the forensic timeframe
- Identify: connections to/from suspicious IPs, unusual port usage, cross-VPC traffic, internet-bound traffic from internal resources

**GuardDuty Finding Correlation:**
- If GuardDuty findings were exported: correlate with CloudTrail events
- Finding types: reconnaissance, instance compromise, account compromise, data exfiltration

```
| # | Timestamp (UTC) | Event Name | Source IP | User/Role | Target Resource | Result | Anomaly | EVD ID |
|---|-----------------|------------|-----------|-----------|-----------------|--------|---------|--------|
| 1 | {{timestamp}} | {{event}} | {{ip}} | {{identity}} | {{resource}} | Success/Failure | {{anomaly}} | EVD-{case_id}-XXX |
```

### 3. Azure Forensic Analysis (If Applicable)

**Azure Activity Log (Management Plane):**
- Resource operations: VM creation/deletion, storage account operations, NSG modifications
- Administrative actions: role assignments, policy changes, subscription-level operations
- Diagnostic settings: logging configuration changes (anti-forensics indicator)

**Azure AD / Entra ID Sign-In & Audit Logs:**
- **Sign-in logs:** Authentication events with: user, app, IP, device, location, conditional access result, risk level, MFA status
  - Impossible travel detection: sign-ins from geographically distant locations within impossible timeframes
  - Anomalous sign-in patterns: unusual browsers, devices, or IP ranges
  - MFA bypass: sign-ins without MFA when policy requires it
- **Audit logs:** Directory changes with: actor, operation, target, result
  - Application registrations (OAuth app creation — persistence technique)
  - Consent grants (admin consent for broad permissions — data access)
  - User/group modifications
  - Role assignment changes (privilege escalation)
  - Conditional access policy modifications (defense weakening)

**NSG Flow Log Analysis:**
- Network Security Group flow records
- Identify: traffic patterns, blocked attempts, allowed connections to/from suspicious destinations

**Key Vault Audit:**
- Secret/key/certificate access events
- Who accessed what secrets, when, from where

### 4. GCP Forensic Analysis (If Applicable)

**Cloud Audit Logs:**
- **Admin Activity Logs:** Always enabled, 400-day retention. Resource creation, IAM changes, configuration modifications.
- **Data Access Logs:** Must be explicitly enabled. Read/write operations on data (GCS object access, BigQuery queries, Pub/Sub operations).
- **System Event Logs:** GCP-initiated actions (live migration, auto-scaling, maintenance).

**Key Analysis Targets:**
- IAM: `SetIamPolicy`, `CreateServiceAccount`, `CreateServiceAccountKey` — Identity persistence
- Compute: `instances.insert`, `instances.setMetadata` (startup scripts) — Code execution
- Storage: `objects.get`, `objects.list`, `buckets.setIamPolicy` — Data access/exfiltration
- GKE: Audit logs for pod creation, RBAC modifications, secret access

### 5. Identity & Access Analysis (Cross-Platform)

Regardless of specific cloud platform, analyze identity and access patterns:

**Authentication Analysis:**

```
| # | Timestamp | Identity | Platform | Source IP | Location | MFA | Result | Session Duration | Anomaly |
|---|-----------|----------|----------|-----------|----------|-----|--------|------------------|---------|
| 1 | {{timestamp}} | {{user/service}} | AWS/Azure/GCP/M365 | {{ip}} | {{geo}} | ✅/❌/N-A | Success/Failure | {{duration}} | {{anomaly}} |
```

**Anomaly Categories:**
- **Impossible travel:** Same identity authenticated from distant locations within physically impossible timeframes
- **MFA bypass:** Authentication without MFA when expected
- **Off-hours access:** Activity outside normal working hours for the identity
- **New device/browser:** First-time device or browser for established identity
- **IP anomaly:** Authentication from unusual IP range, VPN exit node, cloud provider IP, Tor exit node
- **Privilege anomaly:** Access to resources not previously accessed by this identity
- **Service account anomaly:** Interactive use of service accounts, service account used from unexpected source

**OAuth / Application Analysis:**
- List all OAuth applications and consent grants during the forensic timeframe
- Flag: new application registrations, admin consent grants, applications with broad permissions (Mail.ReadWrite, Files.ReadWrite.All, User.ReadWrite.All)
- Identify: applications granted permissions by compromised accounts, dormant applications suddenly active

**API Key / Access Key Usage:**
- Track all API key and access key usage during the forensic timeframe
- Flag: new keys created, keys used from unusual source IPs, keys for accounts not normally using programmatic access

**Cross-Account / Cross-Tenant Activity:**
- AWS: AssumeRole to external accounts, cross-account S3 access
- Azure: B2B collaboration, cross-tenant access
- GCP: Cross-project access, organization-level operations

### 6. SaaS Forensics

**Microsoft 365:**
- **Unified Audit Log:** Comprehensive audit of all M365 activities
  - Search: `Search-UnifiedAuditLog -StartDate -EndDate -Operations`
  - Key operations: FileAccessed, FileDownloaded, FileSynced, MailItemsAccessed, New-InboxRule, Set-Mailbox, Add-MailboxPermission
- **Exchange Message Trace:** Email delivery records
  - Track specific messages by sender, recipient, subject, date range
  - Identify: forwarding rules, delegate access, mail flow rules
- **SharePoint/OneDrive Activity:** File access, sharing, sync
  - Sensitive file access patterns, bulk downloads, external sharing
- **Teams Activity:** Message history, file sharing, meeting recordings
  - Data exfiltration via Teams file sharing

**Google Workspace:**
- **Admin Audit Log:** Administrative changes (user management, security settings, OAuth apps)
- **Drive Activity Log:** Document access, sharing, download, deletion
- **Gmail Log Events:** Message metadata, delegated access, forwarding rules
- **Login Audit Log:** Authentication events, suspicious login detection

**Other SaaS Platforms:**
- Slack: Workspace analytics, access logs, file sharing logs, integration activity
- Salesforce: Login history, setup audit trail, field history tracking
- GitHub/GitLab: Audit logs, access logs, repository events, secret scanning

### 7. Container / Kubernetes Forensics (If Applicable)

**Container Image Analysis:**
- Pull and analyze container images deployed during the forensic timeframe
- Layer analysis: identify modifications to base images
- Entrypoint/CMD analysis: detect malicious startup commands
- Embedded secrets: scan for hardcoded credentials, API keys, tokens

**Kubernetes Audit Logs:**
- API server audit logs: all requests to K8s API
- Key events: pod creation, RBAC modifications, secret access, configmap changes, namespace operations
- Flag: privileged pod creation, hostPath mounts, node shell access, kube-system namespace modifications

**Pod-to-Pod Communication:**
- Service mesh logs (Istio, Linkerd) if available
- Network policies: analyze for gaps allowing lateral movement
- DNS-based service discovery: CoreDNS logs

**Secret Access Patterns:**
- Kubernetes secrets access audit
- HashiCorp Vault audit log (if used)
- AWS Secrets Manager / Azure Key Vault / GCP Secret Manager audit

### 8. Cloud Forensics Findings Summary

Consolidate all cloud and SaaS forensic findings:

**Findings Table:**

```
| # | Finding | Category | Platform | Log Source | Identity/Resource | Timestamp | EVD ID | Severity | ATT&CK Technique | Confidence |
|---|---------|----------|----------|------------|-------------------|-----------|--------|----------|-------------------|------------|
| 1 | {{finding}} | Auth/IAM/Data/Config/Persistence | {{platform}} | {{source}} | {{identity}} | {{timestamp}} | EVD-{case_id}-XXX | Critical/High/Medium/Low/Info | {{T-code}} | Confirmed/Probable/Possible |
```

**Cloud Forensics Statistics:**
```
Cloud platforms analyzed: {{list}}
SaaS applications analyzed: {{list}}
Total log events analyzed: {{count}}
Authentication events analyzed: {{count}}
IAM modification events: {{count}}
Data access events: {{count}}
Anomalous identities identified: {{count}}
OAuth/application consent events: {{count}}
Cloud IOCs extracted: {{count}}
```

### 9. Append Findings to Report

Write all cloud forensic findings under `## Cloud Forensics` in the output file `{outputFile}`:

```markdown
## Cloud Forensics

### Cloud Platform Analysis
{{per_platform_analysis_results}}

### Identity & Access Analysis
{{authentication_analysis}}
{{oauth_application_analysis}}
{{cross_account_analysis}}

### SaaS Forensics
{{m365_analysis}}
{{google_workspace_analysis}}
{{other_saas_analysis}}

### Container/Kubernetes Forensics
{{container_analysis_if_applicable}}

### Cloud Forensics Findings Summary
{{consolidated_findings_table}}
{{statistics}}
```

Update frontmatter:
- Add this step name (`Cloud & SaaS Forensic Analysis`) to the end of `stepsCompleted`
- Set `analysis_types.cloud_forensics` to `true`
- Update `findings_count` and `findings_by_severity` with cloud forensic findings
- Update `iocs_extracted` with cloud IOCs
- Update `mitre_techniques` with cloud ATT&CK techniques

### 10. Present MENU OPTIONS

"**Cloud and SaaS forensic analysis complete.**

Cloud platforms analyzed: {{platforms}}
SaaS applications analyzed: {{saas_apps}}
Log events analyzed: {{event_count}}
Authentication anomalies: {{auth_anomaly_count}}
IAM modifications detected: {{iam_mod_count}}
OAuth consent events: {{oauth_count}}
Data access anomalies: {{data_anomaly_count}}
Cloud IOCs extracted: {{ioc_count}}

**Select an option:**
[A] Advanced Elicitation — Challenge cloud analysis completeness, identify log gaps, assess whether all cloud-native persistence mechanisms were detected
[W] War Room — Red (did I create a backdoor IAM role the analyst missed? did they find my OAuth app with delegated permissions? what about my cross-account trust I established for re-entry?) vs Blue (do we have complete audit log coverage? are there cloud services without logging enabled? could the attacker have disabled logging before acting? is our OAuth app inventory complete?)
[C] Continue — Proceed to Step 7: Timeline Reconstruction (Step 7 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — challenge the cloud analysis. Were all relevant cloud services analyzed? Are there log gaps (services without logging enabled, retention periods exceeded)? Were all IAM changes reviewed for persistence? Were OAuth consent grants fully audited? Were data plane logs analyzed alongside management plane logs? Could the attacker have disabled logging before acting (CloudTrail StopLogging, diagnostic settings modification)? Process insights, redisplay menu
- IF W: War Room — Red Team: did I disable CloudTrail before my main operations? Did the analyst find the service account key I created for persistent access? Did they detect my OAuth app with Mail.ReadWrite permissions? Did they notice I modified the conditional access policy to exempt my IP? Blue Team: is our cloud log retention sufficient? Did we check for logging gaps? Are all SaaS applications audited? Could the attacker be maintaining access through mechanisms we did not check (federated identity, SAML assertions, certificate-based auth)? Summarize insights, redisplay menu
- IF C: Verify frontmatter updated and this step added to stepsCompleted. Then read fully and follow: ./step-07-timeline.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, analysis_types.cloud_forensics set to true, findings counts updated, and Cloud Forensics section fully populated], will you then read fully and follow: `./step-07-timeline.md` to begin timeline reconstruction.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Working copy integrity verified before analysis began
- Cloud platform audit logs analyzed per platform (CloudTrail/Activity Log/Cloud Audit Logs)
- Identity and access analysis performed with authentication anomaly detection
- IAM modification events reviewed for persistence and privilege escalation
- OAuth/application consent grants audited for malicious applications
- SaaS forensics performed for relevant SaaS applications
- Container/K8s forensics performed if applicable
- Every finding cites evidence ID, log source, and confidence level
- Cloud forensics findings summary presented with severity and ATT&CK mapping
- Cross-reference performed with endpoint and network findings from steps 3-5
- Frontmatter updated with all relevant fields
- Findings appended to report under `## Cloud Forensics`

### ❌ SYSTEM FAILURE:

- Not analyzing IAM changes during the forensic timeframe
- Not checking for OAuth/application consent grants
- Not analyzing authentication logs for anomalies
- Analyzing only management plane logs without data plane logs (when available)
- Not checking whether logging was disabled or modified by the attacker
- Not correlating cloud findings with endpoint and network findings
- Modifying cloud resources or configurations during analysis
- Presenting findings without evidence ID citations
- Performing disk, memory, or network analysis during this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Cloud forensics reveals the management plane — identity changes, resource modifications, and data access that are invisible from the endpoint. Every API call is logged. Every identity change is tracked. The cloud audit trail is comprehensive but time-bounded — analyze it before retention expires.
