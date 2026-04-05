# Step 5: Web Application Enumeration

**Progress: Step 5 of 10** — Next: Vulnerability Identification

## STEP GOAL:

Map the web application attack surface across all discovered HTTP/HTTPS services. This step identifies directories, technologies, API endpoints, authentication mechanisms, and input points that will feed vulnerability identification in step 6.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER attempt exploitation or authentication bypass — enumeration only
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A RECONNAISSANCE SPECIALIST, not a penetration tester (yet)
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Reconnaissance Specialist conducting authorized external reconnaissance
- ✅ Web enumeration is ACTIVE — it sends HTTP requests to target web applications
- ✅ Stay within RoE bounds — no injection attempts, no authentication testing
- ✅ Aggressive directory brute-forcing can cause denial of service — respect rate limits
- ✅ Document all discovered entry points for downstream exploitation planning

### Step-Specific Rules:

- 🎯 Focus on web application surface mapping — directories, tech, APIs, inputs
- 🚫 FORBIDDEN to attempt SQL injection, XSS, or any exploitation technique
- 🚫 FORBIDDEN to attempt login with credentials (even default ones — that's later)
- 💬 Approach: Systematic enumeration of every HTTP/HTTPS service from step 4
- 📊 Map every web application to its technology stack, endpoints, and input points
- 🔒 Only enumerate applications on in-scope hosts

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers). This is the ONLY action the agent refuses. Note: in recon context, destructive actions are unlikely but the principle stands.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Brute-forcing directories on production systems if the RoE disallows aggressive enumeration — aggressive dir busting can cause service degradation or denial of service
  - Testing authentication mechanisms without explicit authorization — credential testing is an exploitation activity, not enumeration, and requires separate RoE approval
  - Skipping technology fingerprinting to save time — knowing the exact tech stack is essential for accurate vulnerability identification in the next step
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present enumeration plan before beginning
- ⚠️ Present [A]/[W]/[C] menu after enumeration complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Scope, OSINT, subdomain inventory, and service map from steps 1-4
- Focus: Web application enumeration only — no vulnerability exploitation
- Limits: Only enumerate HTTP/HTTPS services discovered in step 4
- Dependencies: Service map from step-04-port-scanning.md identifies web services

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Identify Web Application Targets

**From step 4 service map, extract all HTTP/HTTPS services:**

- All hosts with ports 80, 443, 8080, 8443, and any other identified HTTP services
- Include non-standard ports running web servers
- Include API gateways and reverse proxies

"**Web Enumeration Targets**

HTTP/HTTPS services identified: {{web_service_count}}

{{for each web_service}}
- {{hostname}}:{{port}} ({{service_version}})
{{/for}}

Would you like to proceed with full enumeration, or focus on specific targets?"

### 2. Directory and File Brute-Forcing

**For each web application, discover hidden paths:**

**Tool Configuration:**
```bash
# gobuster directory mode
gobuster dir -u https://{{target}} -w /path/to/SecLists/Discovery/Web-Content/directory-list-2.3-medium.txt -t 50 -o dirs_{{target}}.txt

# ffuf for flexible fuzzing
ffuf -u https://{{target}}/FUZZ -w /path/to/wordlist.txt -mc 200,301,302,403 -o ffuf_{{target}}.json

# feroxbuster for recursive discovery
feroxbuster -u https://{{target}} -w /path/to/wordlist.txt --depth 3 -o ferox_{{target}}.txt
```

**High-value paths to check:**
```
/admin, /administrator, /login, /wp-admin, /wp-login.php,
/api, /api/v1, /api/v2, /swagger, /swagger-ui, /api-docs,
/graphql, /graphiql, /.well-known, /robots.txt, /sitemap.xml,
/.git, /.env, /.htaccess, /backup, /config, /debug,
/phpinfo.php, /server-status, /server-info, /elmah.axd,
/trace.axd, /actuator, /actuator/health, /metrics,
/console, /shell, /dashboard, /panel, /manage
```

**For each discovered path, document:**
- URL path
- HTTP response code
- Content type
- Size (for anomaly detection)
- Redirect target (if 3xx)

### 3. Technology Fingerprinting

**Active technology identification for each web application:**

**HTTP Response Analysis:**
- Server header (Apache, Nginx, IIS, etc.)
- X-Powered-By header
- Set-Cookie patterns (PHPSESSID, JSESSIONID, ASP.NET_SessionId)
- Custom headers revealing framework/version

**CMS Detection:**
- WordPress: `/wp-content/`, `/wp-includes/`, `/wp-json/`
- Drupal: `/sites/default/`, `/core/misc/drupal.js`
- Joomla: `/administrator/`, `/components/`, `/modules/`
- SharePoint: `/_layouts/`, `/_catalogs/`

**Framework Fingerprinting:**
- JavaScript frameworks from source analysis (React, Angular, Vue)
- Backend framework indicators (Rails, Django, Laravel, Spring)
- API framework detection (Express, FastAPI, Flask)

**Document per application:**
```
| Application | Server | CMS/Framework | Language | Version | Confidence |
|-------------|--------|---------------|----------|---------|------------|
```

### 4. API Endpoint Discovery

**For applications with API indicators:**

**Discovery Techniques:**
- Swagger/OpenAPI documentation: `/swagger.json`, `/api-docs`, `/openapi.yaml`
- GraphQL introspection: POST to `/graphql` with introspection query
- WADL/WSDL for SOAP services
- JavaScript source analysis for API endpoint references
- Mobile app API endpoints (if in scope)

**For each discovered API:**
- Base URL and version
- Authentication type (API key, OAuth, JWT, Basic)
- Discovered endpoints and methods (GET, POST, PUT, DELETE)
- Request/response content types
- Rate limiting indicators

### 5. Authentication Mechanism Identification

**Map authentication surfaces — do NOT test credentials:**

**For each login/auth endpoint:**
- Authentication type (form-based, Basic Auth, OAuth, SAML, LDAP)
- Multi-factor authentication indicators
- Account lockout behavior indicators (from response headers/messages)
- Password policy indicators (client-side validation)
- Session management (cookie flags, token type)
- SSO/federation indicators

**Document:**
```
| Endpoint | Auth Type | MFA | Session Mgmt | Notes |
|----------|----------|-----|-------------|-------|
```

### 6. Input Point Mapping

**Identify all user-input entry points:**

**For each web application, map:**
- Forms (login, search, contact, registration, file upload)
- URL parameters (query strings)
- POST body parameters
- HTTP headers accepting user input (Referer, User-Agent, X-Forwarded-For)
- Cookie values that appear user-controllable
- File upload endpoints
- WebSocket endpoints
- Server-Sent Events (SSE) endpoints

**Classify each input point by potential attack relevance:**
```
| Application | Input Point | Type | Parameters | Attack Potential |
|-------------|------------|------|------------|-----------------|
```

### 7. Consolidate Web Application Map

**Build comprehensive web application inventory:**

**Per-Application Summary:**
```
### {{application_url}}
- Technology: {{tech_stack}}
- CMS/Framework: {{cms_framework}}
- Interesting directories: {{interesting_dirs_count}}
- API endpoints: {{api_endpoint_count}}
- Auth mechanism: {{auth_type}}
- Input points: {{input_point_count}}
- Exposed files: {{exposed_files}}
- Notes: {{observations}}
```

**Web Attack Surface Statistics:**
- Total web applications: {{web_app_count}}
- Total unique directories/paths discovered: {{path_count}}
- API endpoints discovered: {{api_count}}
- Authentication surfaces: {{auth_surface_count}}
- Input points mapped: {{input_count}}
- Potentially sensitive files exposed: {{sensitive_file_count}}

### 8. Append Findings to Report

Write findings under `## Web Application Enumeration`:

```markdown
## Web Application Enumeration

### Summary
- Web applications analyzed: {{web_app_count}}
- Directories/paths discovered: {{path_count}}
- API endpoints: {{api_count}}
- Authentication surfaces: {{auth_surface_count}}
- Input points mapped: {{input_count}}

### Application Inventory
{{per_application_summaries}}

### Technology Stacks
{{technology_fingerprinting_table}}

### Discovered APIs
{{api_endpoint_details}}

### Authentication Mechanisms
{{auth_mechanism_table}}

### Input Point Map
{{input_point_map}}

### Sensitive Files and Directories
{{sensitive_files_and_dirs}}
```

### 9. Present MENU OPTIONS

"**Web application enumeration complete.**

Summary: {{web_app_count}} applications analyzed.
Directories: {{path_count}} | APIs: {{api_count}} | Auth surfaces: {{auth_surface_count}} | Input points: {{input_count}}

**Select an option:**
[A] Advanced Elicitation — Push deeper on web application surface
[W] War Room — Launch multi-agent adversarial discussion on web applications
[C] Continue — Save and proceed to Vulnerability Identification (Step 6 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — technology correlation vulnerabilities, API security posture assessment, authentication weakness indicators, input point risk ranking. Redisplay menu
- IF W: War Room — Red: most promising web attack vectors? Authentication bypass potential? API abuse scenarios? Blue: WAF effectiveness assessment, web application monitoring gaps, recommended detection rules for enumeration patterns observed. Summarize, redisplay menu
- IF C: Update output file frontmatter adding this step name to stepsCompleted, then read fully and follow: ./step-06-vuln-identification.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and web enumeration findings appended to report], will you then read fully and follow: `./step-06-vuln-identification.md` to begin vulnerability identification.

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- All HTTP/HTTPS services from step 4 targeted for enumeration
- Directory brute-forcing performed with appropriate wordlists
- Technology stack fingerprinted for each web application
- API endpoints discovered and documented with auth types
- Authentication mechanisms mapped without testing credentials
- Input points systematically mapped per application
- RoE rate limits respected during enumeration
- Complete web application inventory built and documented

### ❌ SYSTEM FAILURE:

- Attempting ANY exploitation (SQL injection, XSS, etc.)
- Testing credentials against authentication surfaces
- Enumerating applications on out-of-scope hosts
- Causing denial of service through aggressive brute-forcing
- Not mapping input points for downstream exploitation planning
- Skipping technology fingerprinting
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Enumerate, don't exploit.
