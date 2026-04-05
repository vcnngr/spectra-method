# Step 7: Cloud Privilege Escalation

**Progress: Step 7 of 10** — Next: Exploit Development & Technique Chaining

## STEP GOAL:

Execute cloud-specific privilege escalation techniques to elevate access within AWS, Azure, or GCP environments. Exploit IAM misconfigurations, metadata services, role chaining, managed identities, and cross-account trust relationships. Document all attempts with ATT&CK mapping.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify production cloud infrastructure without explicit operator authorization
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A POST-EXPLOITATION SPECIALIST executing authorized cloud privilege escalation
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Cloud escalation ONLY — local OS was 04-05, AD was 06
- ⚡ If step-01 classified cloud as N/A, perform brief applicability confirmation then proceed to [C]
- 📋 Every technique attempted must be logged: technique, cloud provider, result, artifacts
- ☁️ Identify the cloud provider FIRST — techniques are provider-specific
- 🔒 Cloud actions create extensive audit logs (CloudTrail, Activity Log, Audit Log) — assume ALL actions are logged
- 📊 Start with read-only enumeration, then escalate to write operations

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive actions ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  1. IAM policy modifications in cloud environments affect production infrastructure and are permanently logged in CloudTrail/Activity Log/Audit Log — every change is visible to defenders
  2. Metadata service abuse (IMDS) from compromised instances may trigger cloud-native detection services (GuardDuty, Defender for Cloud, SCC) — check if IMDS v2 enforcement is in place before attempting
  3. Cross-account pivoting may exceed the authorized engagement scope — verify with RoE that target accounts are in scope before assuming trust relationships
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present cloud escalation plan before beginning
- ⚠️ Present [A]/[W]/[C] menu after cloud escalation assessment complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Step-01 environment classification, step-03 cloud credentials, steps 04-05 local escalation (may provide instance-level access for metadata exploitation)
- Focus: Cloud IAM and service privilege escalation
- Limits: Stay within RoE cloud scope. Assume all actions are logged. Do NOT modify production infrastructure without explicit authorization.
- Dependencies: step-03-credential-discovery.md (cloud creds, tokens, keys), step-01 environment classification

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check

**Determine if cloud escalation applies to this engagement:**

- If NO cloud environment identified in step-01 → document "N/A — on-premise only" → proceed to Menu → [C]
- If cloud environment confirmed → identify provider(s) and current access:

| Field | Value |
|-------|-------|
| Cloud Provider(s) | {{AWS/Azure/GCP/Multi}} |
| Current Identity | {{ARN/UPN/ServiceAccount}} |
| Identity Type | {{User/Role/ServiceAccount/ManagedIdentity}} |
| Current Permissions | {{known permissions or "unknown — enum required"}} |
| Credential Source | {{step-03 finding / metadata / environment}} |
| MFA Required? | {{yes/no/unknown}} |

### 2. Cloud Permission Enumeration

**Before escalating, map current permissions — blind escalation wastes time and generates noise:**

**AWS:**

| Tool/Method | Command | Purpose |
|------------|---------|---------|
| AWS CLI | `aws sts get-caller-identity` | Verify current identity |
| AWS CLI | `aws iam list-attached-user-policies` | Attached policies |
| AWS CLI | `aws iam list-user-policies` | Inline policies |
| AWS CLI | `aws iam get-policy-version` | Policy details |
| Pacu | `run iam__enum_permissions` | Full permission enum |
| enumerate-iam | `enumerate-iam.py` | Brute-force permission enum |
| ScoutSuite | `scout aws` | Full AWS audit |

**Azure:**

| Tool/Method | Command | Purpose |
|------------|---------|---------|
| Az CLI | `az account show` | Current context |
| Az CLI | `az role assignment list` | RBAC assignments |
| Az CLI | `az ad user show` | User details |
| ROADtools | `roadrecon gather` | Full Azure AD enum |
| AzureHound | `azurehound` | BloodHound for Azure |
| Stormspotter | Full scope | Azure visualization |

**GCP:**

| Tool/Method | Command | Purpose |
|------------|---------|---------|
| gcloud | `gcloud auth list` | Active accounts |
| gcloud | `gcloud projects get-iam-policy PROJECT` | IAM bindings |
| gcloud | `gcloud iam roles describe ROLE` | Role permissions |
| ScoutSuite | `scout gcp` | Full GCP audit |

### 3. AWS Privilege Escalation (T1078.004, T1098.001, T1098.003)

**Known IAM escalation paths (Rhino Security Labs research — 21+ methods):**

| Category | Technique | Required Permission | Result |
|----------|-----------|-------------------|--------|
| Direct escalation | Attach admin policy | `iam:AttachUserPolicy` | Admin |
| Direct escalation | Create admin policy version | `iam:CreatePolicyVersion` | Admin |
| Direct escalation | Set default policy version | `iam:SetDefaultPolicyVersion` | Admin |
| Role assumption | PassRole + Lambda | `iam:PassRole` + `lambda:CreateFunction` + `lambda:InvokeFunction` | Admin via Lambda |
| Role assumption | PassRole + EC2 | `iam:PassRole` + `ec2:RunInstances` | Admin via instance |
| Role assumption | Direct role assumption | `sts:AssumeRole` on admin role | Admin |
| Credential exposure | Create access key | `iam:CreateAccessKey` on other user | Admin |
| Credential exposure | Create login profile | `iam:CreateLoginProfile` | Account access |
| Credential exposure | SSM secrets | `ssm:GetParameter` for secrets | Credential theft |
| Resource policy | Resource-based policy abuse | s3/sqs/sns/lambda resource policies | Data access |
| Cross-account | Cross-account role assumption | `sts:AssumeRole` on cross-account role | Lateral + escalation |

**Additional AWS vectors:**
- EC2 instance metadata (IMDS v1: `curl 169.254.169.254`) — steal instance role credentials
- SSM Parameter Store secrets
- Secrets Manager
- Lambda environment variables
- ECS task role credentials
- CloudFormation stack outputs with secrets
- Cognito identity pool misconfiguration

### 4. Azure Privilege Escalation (T1078.004, T1098.001, T1098.003)

| Category | Technique | Required Permission | Result |
|----------|-----------|-------------------|--------|
| RBAC abuse | User Access Administrator | Assign roles to self | Global Admin |
| Managed Identity | Exploit VM/App managed identity | Access to VM/App | Token theft |
| PIM abuse | Activate eligible role | PIM eligible assignment | Temporary admin |
| App registration | Create app + add credentials | `Application.ReadWrite.All` | App-based access |
| Service Principal | Add credentials to existing SP | Application owner | SP impersonation |
| Key Vault | Read secrets from Key Vault | Key Vault Secrets User | Credential access |
| Automation | Modify runbook with privileged identity | Automation Contributor | Code exec as identity |
| Function App | Modify function with managed identity | Website Contributor | Code exec as identity |
| Conditional Access | Bypass CA policies | Identify gaps in CA | Unrestricted access |

**Azure-specific vectors:**
- Azure AD Connect — extract sync credentials (DCSync equivalent for hybrid)
- Managed Identity token theft from IMDS (`169.254.169.254/metadata/identity/oauth2/token`)
- Azure Resource Manager API abuse
- Logic Apps with stored credentials
- Azure DevOps pipeline secrets

### 5. GCP Privilege Escalation (T1078.004, T1098.001)

| Category | Technique | Required Permission | Result |
|----------|-----------|-------------------|--------|
| IAM abuse | setIamPolicy on project | `resourcemanager.projects.setIamPolicy` | Admin |
| SA impersonation | actAs + compute create | `iam.serviceAccounts.actAs` + `compute.instances.create` | SA-level access |
| SA key creation | Create key for SA | `iam.serviceAccountKeys.create` | Persistent SA access |
| Token generation | signBlob/signJwt | `iam.serviceAccounts.signBlob` / `signJwt` | SA impersonation |
| Cloud Functions | Deploy function as SA | `cloudfunctions.functions.create` + `actAs` | Code exec as SA |
| Compute | setMetadata on instance | startup-script injection | Code exec on instance |
| Organization | orgpolicy.policy.set | Disable security constraints | Weaken controls |

**GCP-specific vectors:**
- Metadata server (`metadata.google.internal`) — project-level and instance-level metadata
- Default compute service account (often has Editor role)
- Workload Identity Federation misconfiguration
- Cloud Build with broad permissions
- GKE Workload Identity abuse

### 6. Metadata Service Exploitation (T1552.005)

**Cross-provider metadata service abuse — often the easiest path from instance to cloud identity:**

| Provider | Endpoint | Token Path | Protection |
|----------|----------|-----------|------------|
| AWS | `169.254.169.254` | `/latest/meta-data/iam/security-credentials/` | IMDSv2 (token required) |
| Azure | `169.254.169.254` | `/metadata/identity/oauth2/token` | Header: `Metadata:true` |
| GCP | `metadata.google.internal` | `/computeMetadata/v1/instance/service-accounts/default/token` | Header: `Metadata-Flavor:Google` |

**For each provider:**
- Check if metadata endpoint is accessible
- Check for IMDS v2 enforcement (AWS) or equivalent protections
- Extract temporary credentials
- Enumerate permissions of instance/VM/function identity
- Assess escalation potential of the cloud identity

**AWS IMDS exploitation sequence:**
1. Probe IMDSv1: `curl -s http://169.254.169.254/latest/meta-data/`
2. If blocked, attempt IMDSv2: `TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")` then `curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/`
3. Retrieve role name, then fetch `AccessKeyId`, `SecretAccessKey`, `Token`
4. Export credentials and verify with `aws sts get-caller-identity`

**Azure IMDS exploitation sequence:**
1. Probe: `curl -s -H "Metadata:true" "http://169.254.169.254/metadata/instance?api-version=2021-02-01"`
2. Request token: `curl -s -H "Metadata:true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"`
3. Use the `access_token` with Azure REST API or Az CLI
4. Check token scope and audience — different resources require different tokens

**GCP metadata exploitation sequence:**
1. Probe: `curl -s -H "Metadata-Flavor:Google" "http://metadata.google.internal/computeMetadata/v1/"`
2. List service accounts: `curl -s -H "Metadata-Flavor:Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/"`
3. Request token: `curl -s -H "Metadata-Flavor:Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"`
4. Use the `access_token` with gcloud API calls

**Document metadata exploitation results:**
```
| Provider | IMDS Version | Accessible | Identity Retrieved | Permissions | Escalation Potential |
|----------|-------------|------------|-------------------|-------------|---------------------|
```

### 7. Kubernetes & Container Orchestration

**If Kubernetes is in scope — container orchestration adds another escalation layer:**

| Vector | Condition | Method | Result |
|--------|----------|--------|--------|
| Service Account token | Pod access | `/var/run/secrets/kubernetes.io` | K8s API access |
| RBAC escalation | ClusterRole binding gaps | `kubectl auth can-i --list` | Elevated K8s access |
| Node access | Privileged pod | nsenter/chroot to host | Node-level access |
| Secret extraction | secrets read access | `kubectl get secrets` | Credential harvest |
| etcd access | Direct etcd access | `etcdctl get / --prefix` | Full cluster secrets |
| Kubelet API | Unauthenticated kubelet | `curl https://NODE:10250/pods` | Pod listing + exec |
| Cloud credential theft | Node IAM/SA | Cloud metadata from node | Cloud identity |

**K8s escalation sequence:**
1. Identify current context: `kubectl config current-context`
2. Enumerate permissions: `kubectl auth can-i --list --namespace=default`
3. List all namespaces: `kubectl get namespaces`
4. Check for privileged pods: `kubectl get pods -o json | grep privileged`
5. Check for mounted service account tokens with elevated RBAC
6. If node access achieved → pivot to cloud metadata service for cloud-level escalation

**Cloud-K8s integration vectors:**
- **EKS (AWS):** IRSA (IAM Roles for Service Accounts) — pods may have direct AWS IAM access
- **AKS (Azure):** AAD Pod Identity / Workload Identity — pods may hold Azure tokens
- **GKE (GCP):** Workload Identity — pods may impersonate GCP service accounts

### 8. Cross-Account & Cross-Tenant Pivoting

**Evaluate lateral movement across cloud boundaries — verify RoE scope before execution:**

**CRITICAL: Before attempting ANY cross-account/cross-tenant action, confirm with RoE that the target account/tenant is in scope. Unauthorized cross-boundary access is a scope violation.**

**AWS cross-account vectors:**
- `sts:AssumeRole` across account boundaries — check trust policies on roles in other accounts
- Resource-based policies granting cross-account access (S3 bucket policies, KMS key policies, SNS/SQS policies)
- AWS Organizations — if management account is compromised, child accounts may be accessible
- RAM (Resource Access Manager) shared resources between accounts

**Azure cross-tenant vectors:**
- Guest user access to other tenants via B2B collaboration
- Multi-tenant app registrations with broad consent
- Azure Lighthouse — delegated access across tenants
- Shared Azure AD applications with cross-tenant permissions

**GCP cross-project vectors:**
- Cross-project service account impersonation via `iam.serviceAccounts.actAs`
- Shared VPCs — network-level access across projects
- Organization-level IAM bindings granting project-spanning permissions
- Cross-project resource access via IAM policies

**Document cross-boundary findings:**
```
| Source Account/Tenant | Target Account/Tenant | Method | In RoE Scope? | Result |
|----------------------|----------------------|--------|---------------|--------|
```

### 9. Compile Cloud Escalation Results & Append Findings to Report

**Present results per provider:**

| Attempt | Provider | Technique | Identity | Result | Artifacts | Detection |
|---------|----------|-----------|----------|--------|-----------|-----------|
| CLD-001 | {{provider}} | {{technique}} | {{identity}} | Success/Fail | {{artifacts}} | {{events}} |

Write findings under `## Cloud Escalation Paths`:

```markdown
## Cloud Escalation Paths

### Summary
- Cloud provider(s): {{providers}}
- Techniques assessed: {{technique_count}}
- Successful escalations: {{success_count}}
- Metadata services exploited: {{metadata_status}}
- Cross-account pivoting: {{pivot_status}}
- Kubernetes vectors: {{k8s_status}}

### Permission Enumeration
{{permission_enum_results}}

### Provider-Specific Escalation
{{per_provider_results}}

### Metadata Service Exploitation
{{metadata_results}}

### Kubernetes & Container Orchestration
{{k8s_results}}

### Cross-Account Pivoting
{{cross_account_results}}

### Full Attempt Log
{{attempt_log_table}}
```

Update frontmatter:
- `cloud_environment` with provider(s) and escalation results
- Add technique metrics to frontmatter

### 10. Present MENU OPTIONS

"**Cloud privilege escalation assessment completed.**

Summary: {{technique_count}} techniques assessed across {{provider_count}} provider(s).
Successful escalations: {{success_count}} | Metadata: {{metadata_status}} | Cross-account: {{pivot_status}}
Kubernetes: {{k8s_status}} | All attempts logged with provider and detection events.

**Select an option:**
[A] Advanced Elicitation — Deep analysis of a specific cloud attack path
[W] War Room — Red (cross-account pivoting strategies) vs Blue (cloud-native detection: GuardDuty/Defender/SCC analysis)
[C] Continue — Proceed to Exploit Development & Technique Chaining (Step 8 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — explore specific cloud escalation paths in depth, analyze IAM policy chains, evaluate detection probability per technique, assess credential lifetime and rotation risks. Process insights, ask user if they want to refine approach, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: which escalation paths have highest success probability? What trust relationships can be chained? What credential lifetimes enable persistence? Blue Team perspective: what CloudTrail/Activity Log/Audit Log events are generated? What GuardDuty/Defender for Cloud/SCC findings would trigger? What anomaly baselines would detect these actions? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding step-07-cloud-escalation.md to stepsCompleted and updating cloud_environment, then read fully and follow: ./step-08-exploit-chaining.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and cloud_environment updated and Cloud Escalation Paths section populated], will you then read fully and follow: `./step-08-exploit-chaining.md` to begin exploit development and technique chaining.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Cloud provider identified and permissions enumerated before any escalation attempts
- All applicable provider-specific escalation paths assessed systematically
- Metadata services checked across all identified providers
- Cross-account pivoting evaluated with RoE scope verification
- Kubernetes and container orchestration vectors assessed if applicable
- Cloud-K8s integration vectors (IRSA/AAD Pod Identity/Workload Identity) evaluated
- Every attempt logged with provider, technique, identity, result, artifacts, and detection events
- Detection events (CloudTrail/Activity Log/Audit Log) documented per technique
- cloud_environment updated in frontmatter with provider(s) and escalation results
- Findings appended to report under `## Cloud Escalation Paths`
- Read-only enumeration completed before any write operations attempted

### FAILURE:

- Not enumerating permissions before attempting escalation — blind escalation generates noise
- Attempting write operations (IAM modifications, role creation) before understanding logging implications
- Cross-account pivoting without RoE verification — scope violation
- Not tracking cloud audit trail entries per technique — defenders will see every action
- Skipping metadata service checks when instance-level access exists — missed easy escalation path
- Not identifying the cloud provider before attempting provider-specific techniques
- Not documenting detection events generated by each escalation attempt
- Running automated tools (Pacu, ScoutSuite) without understanding their logging footprint
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every technique logged, every provider identified, every audit trail entry tracked.
