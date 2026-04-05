# Step 7: Cloud and Infrastructure Enumeration

**Progress: Step 7 of 10** — Next: Target Package Assembly

## STEP GOAL:

Discover cloud exposure across AWS, Azure, GCP, and other cloud providers. Identify misconfigured cloud resources, exposed storage, CDN/WAF configurations, and cloud-specific attack surface that may not have been covered by traditional network reconnaissance.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER access data in discovered storage buckets — enumeration only
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RECONNAISSANCE SPECIALIST mapping cloud attack surface
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Reconnaissance Specialist conducting authorized external reconnaissance
- ✅ Cloud enumeration requires understanding of multi-cloud architectures
- ✅ Some cloud resources may be shared infrastructure — verify scope carefully
- ✅ Bucket/blob enumeration is legal for public listing, but accessing private data is NOT
- ✅ Document cloud provider, region, and service type for each finding

### Step-Specific Rules:

- 🎯 Focus on cloud resource discovery and exposure assessment
- 🚫 FORBIDDEN to access contents of discovered storage (even if publicly listable)
- 🚫 FORBIDDEN to modify any cloud resource or configuration
- 💬 Approach: Systematic cloud provider identification and resource enumeration
- 📊 Map cloud services to potential attack vectors
- 🔒 Distinguish between target-owned cloud resources and shared services

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Accessing cloud resources outside the authorized scope — cloud infrastructure often involves shared tenancy and unauthorized access has legal implications beyond the engagement
  - Skipping bucket/blob enumeration even if the operator claims "there is no cloud" — cloud presence must be verified through evidence, not assumptions, as shadow IT frequently operates cloud services unknown to stakeholders
  - Interacting with cloud metadata endpoints without explicit Rules of Engagement authorization — metadata service access (e.g., 169.254.169.254) can escalate privilege and crosses the line from enumeration to exploitation
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present cloud enumeration plan before beginning
- ⚠️ Present [A]/[W]/[C] menu after enumeration complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: All findings from steps 1-6 (scope through vulnerabilities)
- Focus: Cloud infrastructure discovery and exposure assessment
- Limits: Only enumerate cloud resources associated with in-scope targets
- Dependencies: DNS records, IP ranges, technology stacks from previous steps

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Cloud Service Provider Identification

**Determine which cloud providers the target uses:**

**Detection Methods:**

**From DNS records (already collected):**
- CNAME to `*.amazonaws.com` → AWS
- CNAME to `*.azure.net`, `*.azurewebsites.net` → Azure
- CNAME to `*.googleapis.com`, `*.appspot.com` → GCP
- CNAME to `*.cloudflare.com` → Cloudflare
- CNAME to `*.fastly.net` → Fastly

**From IP range analysis:**
- Cross-reference discovered IPs with cloud provider IP ranges
- AWS: ip-ranges.json
- Azure: Published IP ranges
- GCP: Published IP ranges

**From HTTP headers and response patterns:**
- `x-amz-*` headers → AWS
- `x-ms-*` headers → Azure
- `x-goog-*` headers → GCP
- Server: `AmazonS3`, `Windows-Azure`, `Google Frontend`

**From technology stack (step 5):**
- CloudFront distributions
- Azure CDN endpoints
- Cloud Load Balancing signatures

"**Cloud Provider Identification**

{{for each provider detected}}
- **{{provider}}**: Detected via {{detection_method}}
  - Services identified: {{service_list}}
{{/for}}

Providers not detected: {{undetected_providers}}

Proceeding with provider-specific enumeration?"

### 2. AWS Enumeration

**If AWS is detected:**

**S3 Bucket Enumeration:**
- Derive potential bucket names from:
  - Company name variations (company, company-prod, company-dev, company-backup)
  - Domain-based names (www.company.com → www-company-com, company-com)
  - Known naming patterns (assets, uploads, media, static, logs, backups)
- Check bucket existence: `aws s3 ls s3://{{bucket_name}} --no-sign-request`
- Check for public listing (do NOT download contents)

**Other AWS Services:**
- CloudFront distribution analysis
- Elastic Beanstalk environment detection
- EC2 instance metadata indicators
- RDS/database endpoint exposure
- Lambda function URLs
- API Gateway endpoints

**Tools:**
- `cloud_enum` for automated cloud resource enumeration
- `S3Scanner` for bucket discovery
- `aws` CLI with `--no-sign-request` for public resource checking

### 3. Azure Enumeration

**If Azure is detected:**

**Blob Storage Enumeration:**
- Derive storage account names from company/domain patterns
- Check blob container listing: `https://{{account}}.blob.core.windows.net/{{container}}?restype=container&comp=list`
- Check for anonymous access

**Other Azure Services:**
- Azure App Service enumeration
- Azure Functions endpoints
- Azure DevOps exposure (dev.azure.com)
- Azure AD tenant information
- Azure Key Vault exposure indicators

### 4. GCP Enumeration

**If GCP is detected:**

**Cloud Storage Enumeration:**
- Derive bucket names from company/project patterns
- Check bucket existence and listing permissions
- Check for public access

**Other GCP Services:**
- App Engine application detection
- Cloud Functions endpoints
- Firebase database exposure
- GCP project ID discovery

### 5. CDN and WAF Detection

**Identify content delivery and security layers:**

**CDN Detection:**
- Cloudflare (check via DNS, HTTP headers, challenge pages)
- AWS CloudFront (x-amz-cf-id, x-amz-cf-pop headers)
- Akamai (X-Akamai-* headers)
- Fastly (x-served-by, x-cache headers)
- Azure CDN (x-ms-ref header)

**WAF Detection:**
- Cloudflare WAF (cf-ray header, challenge pages)
- AWS WAF (x-amzn-waf-* headers)
- ModSecurity (detection through response patterns)
- Imperva/Incapsula (incap_ses cookies, X-CDN header)
- F5 BIG-IP ASM (detection through cookie patterns)

**For each detected layer:**
```
| Target | CDN | WAF | Bypass Potential | Notes |
|--------|-----|-----|-----------------|-------|
```

### 6. DNS-Based Cloud Service Discovery

**Advanced DNS analysis for cloud resources:**

- SRV records revealing cloud services
- TXT records with cloud service verification tokens
- MX records pointing to cloud email services (O365, Google Workspace)
- Autodiscover records for Exchange/O365
- SPF records revealing email infrastructure

**Cloud service mapping:**
```
| DNS Record | Cloud Provider | Service | Implications |
|------------|---------------|---------|-------------|
```

### 7. Cloud Metadata and Configuration Analysis

**Analyze cloud-specific exposure:**

- Public AMI/VM image exposure
- Cloud formation template exposure
- Terraform state file exposure
- Docker image registry exposure (ECR, ACR, GCR)
- Kubernetes API server exposure
- Cloud monitoring dashboard exposure (CloudWatch, Azure Monitor)

### 8. Consolidate Cloud Findings

**Build comprehensive cloud exposure inventory:**

**Per-Provider Summary:**
```
### {{Provider}}
- Resources discovered: {{resource_count}}
- Exposed storage: {{storage_count}}
- Services with public access: {{public_service_count}}
- Overall risk: {{risk_level}}
```

**Cloud Attack Surface Statistics:**
- Cloud providers identified: {{provider_count}}
- Storage resources discovered: {{storage_count}}
- CDN/WAF layers detected: {{cdn_waf_count}}
- Cloud services with public exposure: {{public_count}}
- Potential misconfigurations: {{misconfig_count}}

### 9. Append Findings to Report

Write findings under `## Cloud and Infrastructure`:

```markdown
## Cloud and Infrastructure

### Summary
- Cloud providers identified: {{provider_count}}
- Storage resources discovered: {{storage_count}}
- Publicly exposed services: {{public_count}}
- CDN detected: {{cdn_list}}
- WAF detected: {{waf_list}}
- Cloud misconfigurations: {{misconfig_count}}

### Cloud Provider Mapping
{{provider_detection_details}}

### Storage Enumeration
#### AWS S3
{{s3_findings}}
#### Azure Blob
{{blob_findings}}
#### GCP Storage
{{gcs_findings}}

### CDN and WAF
{{cdn_waf_detection_table}}

### Exposed Cloud Services
{{cloud_service_exposure}}

### DNS Cloud Discovery
{{dns_cloud_service_mapping}}

### Configuration and Metadata
{{cloud_config_findings}}
```

### 10. Present MENU OPTIONS

"**Cloud and infrastructure enumeration complete.**

Summary: {{provider_count}} cloud providers, {{storage_count}} storage resources, {{public_count}} exposed services.
CDN: {{cdn_list}} | WAF: {{waf_list}} | Cloud misconfigs: {{misconfig_count}}

**Select an option:**
[A] Advanced Elicitation — In-depth analysis of cloud exposure
[W] War Room — Red vs Blue discussion on cloud infrastructure
[C] Continue — Proceed to Target Package Assembly (Step 8 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — cloud-specific attack paths, storage misconfiguration exploitation potential, WAF bypass assessment, multi-cloud complexity risks. Redisplay menu
- IF W: War Room — Red: cloud-first attack vectors? Storage as data exfiltration path? Metadata service exploitation potential? Blue: cloud security posture assessment, CSPM recommendations, cloud-native detection capabilities. Summarize, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted, then read fully and follow: ./step-08-target-package.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and cloud findings appended to report], will you then read fully and follow: `./step-08-target-package.md` to begin target package assembly.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Cloud providers identified from DNS, IP, header, and tech stack analysis
- Storage enumeration performed per provider (S3, Blob, GCS)
- CDN and WAF layers detected and documented
- DNS-based cloud service discovery completed
- Cloud metadata and configuration exposure checked
- All findings restricted to in-scope targets
- Storage contents NOT accessed (enumeration only)
- Comprehensive cloud exposure inventory built

### ❌ SYSTEM FAILURE:

- Accessing contents of discovered storage resources
- Modifying any cloud resource or configuration
- Enumerating cloud resources not associated with in-scope targets
- Not checking for all major cloud providers
- Not detecting CDN/WAF layers (affects exploitation planning)
- Skipping DNS-based cloud service discovery
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Enumerate cloud exposure, don't access data.
