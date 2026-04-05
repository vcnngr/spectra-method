# Step 3: Content & Payload Analysis

**Progress: Step 3 of 8** — Next: IOC Extraction & Enrichment

## STEP GOAL:

Perform comprehensive analysis of the email body content (HTML and plaintext), identify social engineering techniques, detect brand impersonation, extract and analyze all URLs (including redirect chains and credential harvesting detection), analyze all attachments (file metadata, hash computation, static analysis, sandbox recommendations), and classify the payload type — producing a structured content analysis that reveals the attack mechanism and enables targeted IOC extraction in the next step.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute or detonate payloads — analysis only, no active interaction with live malicious content
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC PHISHING ANALYST performing forensic content analysis
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst conducting structured phishing investigation
- ✅ Content analysis reveals the attack mechanism — what the attacker wants the victim to DO
- ✅ URLs must be defanged before documentation (hxxps://, [.] instead of .) to prevent accidental navigation
- ✅ Attachment analysis is static only at this stage — dynamic analysis (sandbox detonation) is a recommendation, not an action
- ✅ Social engineering techniques should be mapped to known frameworks (Cialdini's principles, NIST phishing categories)

### Step-Specific Rules:

- 🎯 Focus exclusively on email body content, URL analysis, and attachment analysis
- 🚫 FORBIDDEN to begin IOC enrichment, scope assessment, or any containment activity — this is content forensics only
- 💬 Approach: Systematic content examination with structured findings for each component (body, URLs, attachments)
- 📊 Every URL must be defanged before recording in the report
- 🔒 All analysis must reference content from the preserved email in step 1 — do not fabricate content
- 🔬 Attachment analysis is STATIC only — recommend sandbox detonation, do not execute

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - URLs in phishing emails frequently use multi-stage redirect chains — the visible URL, the href URL, and the final landing page may all be different; analyzing only the visible URL text without examining the HTML href attribute and tracing the redirect chain will miss the true destination and may lead to incomplete containment
  - Attachments with double extensions (e.g., invoice.pdf.exe), password-protected archives, or polyglot files are designed to bypass both email gateway scanning and analyst expectations — flag these as high-risk and recommend sandbox detonation before any manual interaction; never open suspicious attachments directly
  - BEC (Business Email Compromise) and social engineering-only phishing emails have NO technical payload — no malicious URLs, no malicious attachments; the attack is the content itself (a request for wire transfer, credential sharing, or sensitive data); dismissing an email as "clean" because it lacks technical indicators is a critical analysis error
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present content analysis plan before beginning — acknowledge what content types are present
- ⚠️ Present [A]/[W]/[C] menu after analysis complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `urls_found`, `attachments_found`, `payload_type`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, phishing email sample, extracted metadata, raw email source, header analysis from steps 1-2
- Focus: Email body content analysis, URL analysis, attachment analysis, payload classification
- Limits: Only analyze content present in the preserved email from step 1 — do not fabricate content or interact with live URLs
- Dependencies: Completed email intake (step 1) and header analysis (step 2)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Content Inventory

Before detailed analysis, inventory all content components present in the email:

**Content Inventory:**

| Component | Present? | Count | Details |
|-----------|---------|-------|---------|
| Plaintext body | Yes/No | — | {{character count, language}} |
| HTML body | Yes/No | — | {{approximate complexity, inline styles, external resources}} |
| Embedded images | Yes/No | {{count}} | {{inline vs linked, CID references}} |
| URLs (visible) | Yes/No | {{count}} | {{in body text}} |
| URLs (HTML href) | Yes/No | {{count}} | {{in hyperlinks, may differ from visible text}} |
| Attachments | Yes/No | {{count}} | {{filenames, approximate sizes}} |
| Embedded objects | Yes/No | {{count}} | {{OLE objects, embedded PDFs, etc.}} |
| Tracking pixels | Yes/No | {{count}} | {{1x1 images, web beacons}} |

### 2. Email Body Analysis

#### A. HTML vs Plaintext Comparison

If both HTML and plaintext versions exist, compare them for discrepancies:

**Body Comparison:**

| Aspect | Plaintext Version | HTML Version | Discrepancy? |
|--------|-------------------|-------------|-------------|
| Visible text content | {{summary}} | {{summary}} | {{Yes/No — detail}} |
| URLs visible to user | {{list}} | {{list}} | {{Yes/No — hidden URLs?}} |
| Formatting emphasis | {{none}} | {{bold, color, sizing}} | {{urgency enhanced in HTML?}} |
| Hidden content | N/A | {{hidden divs, display:none, white text, zero-width chars}} | {{Found/Not Found}} |

**Hidden Content Detection:**
- **display:none / visibility:hidden**: CSS-hidden content that may contain tracking or obfuscation
- **White text on white background**: Text invisible to the user but visible to email scanners (anti-detection technique)
- **Zero-width characters**: Unicode zero-width spaces (U+200B), zero-width joiners (U+200D), zero-width non-joiners (U+200C) — used for fingerprinting, tracking, or obfuscating text
- **Font-size: 0**: Text rendered at zero size — invisible but present in the DOM
- **HTML comments**: `<!-- -->` containing metadata, tracking IDs, or campaign identifiers

#### B. Social Engineering Technique Identification

Analyze the email content for social engineering techniques using established frameworks:

**Cialdini's Principles of Influence:**

| Principle | Detected? | Evidence | Severity |
|-----------|----------|----------|----------|
| **Urgency/Scarcity** | Yes/No | "Your account will be suspended in 24 hours", "Limited time offer" | {{🔴/🟡/🟢}} |
| **Authority** | Yes/No | Impersonating CEO, IT department, legal, bank, government | {{🔴/🟡/🟢}} |
| **Fear/Threat** | Yes/No | "Unauthorized access detected", "Legal action pending" | {{🔴/🟡/🟢}} |
| **Curiosity** | Yes/No | "You have a new voicemail", "Someone shared a document with you" | {{🔴/🟡/🟢}} |
| **Reward/Greed** | Yes/No | "You've won", "Refund pending", "Bonus available" | {{🔴/🟡/🟢}} |
| **Social Proof** | Yes/No | "Other employees have already completed this", "Company-wide requirement" | {{🔴/🟡/🟢}} |
| **Reciprocity** | Yes/No | "As a valued customer", "Because you're a premium member" | {{🔴/🟡/🟢}} |
| **Trust/Familiarity** | Yes/No | Using first name, referencing internal projects, mimicking normal communication | {{🔴/🟡/🟢}} |

**NIST Phishing Category Classification:**

| Category | Match? | Description |
|----------|--------|-------------|
| Credential Harvesting | Yes/No | Email directs user to fake login page to steal credentials |
| Malware Delivery | Yes/No | Email delivers malicious attachment or links to malware download |
| BEC / Impersonation | Yes/No | Email impersonates executive/authority to request action (wire transfer, data disclosure) |
| Tech Support Scam | Yes/No | Email claims technical issue, provides phone number or remote access instructions |
| Advance Fee / 419 | Yes/No | Email promises reward in exchange for upfront payment or personal information |
| Sextortion / Extortion | Yes/No | Email threatens to release compromising information unless payment is made |
| Reconnaissance | Yes/No | Email designed to confirm email validity (tracking pixel) or gather intelligence |

#### C. Brand Impersonation Detection

If the email appears to impersonate a known brand or organization:

**Brand Impersonation Analysis:**

| Element | Analysis | Finding |
|---------|----------|---------|
| Logo usage | Is a brand logo present? Official or copied/modified? | {{detail}} |
| Color scheme | Does the email use the brand's official color palette? | {{detail}} |
| Template matching | Does the layout match known templates from this brand? | {{detail}} |
| Footer content | Copyright notices, unsubscribe links, legal disclaimers — authentic? | {{detail}} |
| Sender alignment | Does the sender domain match the impersonated brand? | {{detail}} |
| Language/tone | Does the writing style match typical communications from this brand? | {{detail}} |
| Call-to-action | What action does the email request? Consistent with brand communication? | {{detail}} |

#### D. Language Analysis

**Language Quality Assessment:**

| Indicator | Finding |
|-----------|---------|
| Grammar quality | {{native quality / minor errors / significant errors / machine translation artifacts}} |
| Spelling accuracy | {{accurate / typos present / systematic misspellings}} |
| Localization | {{properly localized for target audience / generic / wrong locale}} |
| Translation artifacts | {{detected machine translation patterns / none}} |
| Tone consistency | {{consistent with claimed sender / inconsistent / multiple styles}} |
| Technical accuracy | {{correct terminology / incorrect technical terms}} |

### 3. URL Analysis

For EACH URL found in the email (both visible text URLs and HTML href attribute URLs), perform the following analysis.

**CRITICAL: Defang all URLs before recording.**
- `http://` → `hxxp://`
- `https://` → `hxxps://`
- `.` in domains → `[.]`
- Example: `https://login.microsoft.com` → `hxxps://login[.]microsoft[.]com`

#### A. URL Extraction

Extract URLs from ALL sources within the email:

**URL Extraction Matrix:**

| # | Visible Text | HTML href (actual destination) | Match? | Source Location |
|---|-------------|-------------------------------|--------|-----------------|
| 1 | {{what user sees, defanged}} | {{actual href destination, defanged}} | {{Yes/No — MISMATCH = HIGH RISK}} | {{body / button / image / signature}} |
| 2 | ... | ... | ... | ... |

**URL Mismatch Detection:**
- If the visible text shows one URL but the HTML href points to a different domain → **HIGH RISK** — this is a classic phishing technique (displaying `microsoft.com` but linking to `evil-site.com`)
- Document EVERY mismatch explicitly

#### B. Per-URL Analysis

For each unique URL destination (deduplicated by actual href):

**URL Analysis — URL #{{N}}: {{defanged_url}}**

| Component | Value |
|-----------|-------|
| Full URL (defanged) | {{hxxps://domain[.]com/path?params}} |
| Domain | {{domain[.]com}} |
| TLD | {{.com / .net / .xyz / .ru / etc.}} |
| Path | {{/path/to/page}} |
| Query Parameters | {{param1=value1&param2=value2 or 'None'}} |
| Fragment | {{#section or 'None'}} |
| URL Shortener | {{Yes (bit[.]ly, tinyurl[.]com, etc.) / No}} |
| Resolved Destination | {{final destination if shortener resolved, defanged}} |

**Redirect Chain Analysis (if applicable):**

| Hop | URL (defanged) | Status Code | Method |
|-----|---------------|-------------|--------|
| 1 (initial) | {{first URL}} | — | Direct link |
| 2 | {{redirect target}} | 301/302 | HTTP redirect |
| 3 | {{next redirect}} | 302 | Meta refresh / JS redirect |
| N (final) | {{landing page}} | 200 | Final destination |

**Landing Page Assessment (based on URL structure and domain analysis):**

| Assessment | Finding |
|------------|---------|
| Domain age | {{known domain / newly registered / cannot determine}} |
| Domain reputation | {{legitimate / suspicious / known malicious / unknown}} |
| Login form present | {{Yes — credential harvesting likely / No}} |
| File download triggered | {{Yes — malware delivery likely / No}} |
| Brand impersonation | {{Mimics known brand login page / No}} |
| SSL certificate | {{Valid from known CA / Self-signed / Let's Encrypt (common in phishing) / No HTTPS}} |
| URL categorization | {{Phishing / Malware / C2 / Legitimate / Suspicious / Unknown}} |

#### C. URL Summary Table

**All URLs — Summary:**

| # | URL (defanged) | Type | Category | Risk Level |
|---|---------------|------|----------|------------|
| 1 | {{url}} | {{visible link / hidden href / redirect / embedded}} | {{Phishing / Malware / C2 / Benign / Tracking / Unknown}} | {{🔴 Critical / 🟡 Suspicious / 🟢 Clean / ⚪ Unknown}} |
| 2 | ... | ... | ... | ... |

### 4. Attachment Analysis

For EACH attachment found in the email, perform static analysis.

**CRITICAL:** Do NOT execute, open, or detonate any attachment. All analysis is static (metadata, hashes, signature detection). Dynamic analysis (sandbox detonation) is a RECOMMENDATION only.

#### A. Attachment Inventory

**Attachments Found:**

| # | Filename | Extension | MIME Type | Size | File Magic | Match? |
|---|----------|-----------|-----------|------|-----------|--------|
| 1 | {{filename.ext}} | {{.ext}} | {{application/...}} | {{bytes/KB/MB}} | {{magic bytes identification}} | {{MIME matches magic? Yes/No — MISMATCH = suspicious}} |
| 2 | ... | ... | ... | ... | ... | ... |

**Attachment Risk Indicators (immediate flags):**

| Risk Indicator | Detected? | Detail |
|---------------|----------|--------|
| Double extension | Yes/No | {{e.g., invoice.pdf.exe — high risk}} |
| Executable extension | Yes/No | {{.exe, .scr, .bat, .cmd, .ps1, .vbs, .js, .wsf, .msi, .dll}} |
| Macro-enabled format | Yes/No | {{.docm, .xlsm, .pptm, .dotm, .xltm}} |
| Archive/container | Yes/No | {{.zip, .rar, .7z, .tar.gz, .iso, .img, .vhd}} |
| Password-protected | Yes/No | {{password in email body? "Password: 1234"}} |
| MIME/magic mismatch | Yes/No | {{MIME says PDF but magic bytes say PE executable}} |
| Oversized attachment | Yes/No | {{unusually large for claimed content type}} |
| Zero-byte file | Yes/No | {{empty attachment — possible test or broken payload}} |

#### B. Per-Attachment Static Analysis

For each attachment:

**Attachment Analysis — {{filename}}**

**Hash Computation:**

| Algorithm | Hash Value |
|-----------|-----------|
| MD5 | {{hash}} |
| SHA1 | {{hash}} |
| SHA256 | {{hash}} |

**Static Analysis Results:**

| Analysis Type | Applicable? | Finding |
|--------------|------------|---------|
| **VBA Macro Detection** | {{Yes for Office docs}} | {{macros present / auto-execute macros / obfuscated VBA / no macros}} |
| **XLM Macro Detection** | {{Yes for Excel}} | {{Excel 4.0 macros / no XLM macros}} |
| **Embedded Objects (OLE)** | {{Yes for Office/RTF}} | {{OLE objects found / none — list embedded objects if found}} |
| **PE Analysis** | {{Yes for executables}} | {{imports, sections, packer detection, compiler info}} |
| **Script Content** | {{Yes for .js/.vbs/.ps1}} | {{obfuscated / download cradle / embedded payload / clean}} |
| **PDF Analysis** | {{Yes for PDFs}} | {{JavaScript actions / URI actions / embedded files / launch actions / form fields}} |
| **Archive Contents** | {{Yes for archives}} | {{file listing, nested archives, executable content inside}} |
| **RTF Analysis** | {{Yes for RTF}} | {{OLE objects / equation editor exploit (CVE-2017-11882) / embedded objects}} |
| **HTML/HTA Analysis** | {{Yes for .html/.hta}} | {{JavaScript execution / external resource loading / VBScript}} |
| **LNK (Shortcut) Analysis** | {{Yes for .lnk}} | {{target path / command line arguments / icon location — often used to execute PowerShell}} |
| **ISO/IMG/VHD Analysis** | {{Yes for disk images}} | {{contains executables? DLLs? LNK files? Used to bypass Mark of the Web}} |

**Dynamic Analysis Recommendation:**

"Recommended sandbox detonation for: {{filename}}
- Suggested platforms: ANY.RUN, Hybrid Analysis, Joe Sandbox, Triage (Hatching)
- Configuration: {{Windows 10/11 target, Office version matching org, network monitoring enabled}}
- Analysis focus: {{process execution chain, network callouts, file system modifications, registry changes, persistence mechanisms}}
- Time recommendation: {{minimum 5-minute analysis window for delayed execution payloads}}"

#### C. Polyglot File Detection

Check for files that are valid in multiple formats simultaneously:

**Polyglot Assessment:**

| Check | Finding |
|-------|---------|
| File magic matches claimed type | {{Yes/No — if No, file may be interpreted differently by different parsers}} |
| Multiple valid interpretations | {{e.g., file is valid as both PDF and ZIP, or both HTML and JavaScript}} |
| Fat/thin headers | {{file begins with one type's header but contains another type's payload}} |

### 5. Payload Classification

Based on all content analysis (body, URLs, attachments), classify the overall payload:

**Payload Classification Matrix:**

| Classification | Indicators Present | Confidence |
|---------------|-------------------|------------|
| **Credential Harvester** | URL leads to fake login page, form fields detected, brand impersonation | {{High/Medium/Low/None}} |
| **Malware Dropper** | Malicious attachment delivers executable payload directly | {{High/Medium/Low/None}} |
| **Loader / Downloader** | Attachment or URL downloads next-stage payload from C2 | {{High/Medium/Low/None}} |
| **BEC / Impersonation** | No technical payload, social engineering only, requests action | {{High/Medium/Low/None}} |
| **Reconnaissance** | Tracking pixel, read receipt, no malicious content | {{High/Medium/Low/None}} |
| **Hybrid** | Multiple payload types present (e.g., credential harvester + malware) | {{High/Medium/Low/None}} |

**Primary Payload Classification:** {{type with highest confidence}}
**Secondary Payload (if hybrid):** {{type or 'None'}}

**Payload Summary:**
```
Primary Payload: {{classification}}
Confidence: {{High/Medium/Low}}
Attack Mechanism: {{1-2 sentence description of how the attack works}}
Victim Action Required: {{what the victim must do for the attack to succeed}}
Indicators: {{key indicators that support this classification}}
```

### 6. Present Content Analysis to User

"**Content & Payload Analysis Complete — {{incident_id}}**

**Email Body:**
- Social engineering techniques: {{count}} detected ({{primary technique}})
- Brand impersonation: {{detected brand or 'None detected'}}
- Hidden content: {{found/not found}}
- Language quality: {{assessment}}

**URLs Found:** {{total_count}}
- 🔴 Malicious/Phishing: {{count}}
- 🟡 Suspicious: {{count}}
- 🟢 Clean/Legitimate: {{count}}
- ⚪ Unknown: {{count}}
- URL mismatches (visible ≠ href): {{count}}

**Attachments Found:** {{total_count}}
- 🔴 Malicious indicators: {{count}}
- 🟡 Suspicious: {{count}}
- Hashes computed: {{count}} (MD5 + SHA1 + SHA256 per file)
- Sandbox detonation recommended: {{yes/no — which files}}

**Payload Classification:** {{primary_type}} ({{confidence}} confidence)
{{if hybrid: 'Secondary: ' + secondary_type}}
**Attack Mechanism:** {{description}}"

### 7. Present MENU OPTIONS

"**Select an option:**
[A] Advanced Elicitation — Deep-dive into specific content findings, URL redirect chains, attachment internals, social engineering analysis
[W] War Room — Red vs Blue discussion on payload design and delivery technique — how sophisticated is this attack? What detection gaps does it exploit?
[C] Continue — Proceed to IOC Extraction & Enrichment (Step 4 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive content analysis — examine specific URLs in more detail, analyze attachment internals more thoroughly, challenge the payload classification, investigate social engineering techniques for sophistication indicators, examine whether the content has been reused from known campaigns. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: how would I craft this email to maximize click rate? What evasion techniques are used (URL obfuscation, attachment wrapping, sandbox evasion)? How sophisticated is the payload design? Is this a commodity attack or targeted? Blue Team perspective: what content-based detection rules could catch this? Are our email gateway policies adequate for this payload type? What user training would help against this social engineering technique? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `urls_found`, `attachments_found`, `payload_type`, then read fully and follow: ./step-04-ioc-enrichment.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and urls_found, attachments_found, payload_type updated, and content analysis results appended to report under `## Content & Payload Analysis`], will you then read fully and follow: `./step-04-ioc-enrichment.md` to begin IOC extraction and enrichment.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Content inventory completed identifying all components (body, HTML, URLs, attachments, embedded objects, tracking pixels)
- HTML vs plaintext comparison performed when both versions are present
- Hidden content detection completed (display:none, white text, zero-width characters)
- Social engineering techniques identified using Cialdini's principles and NIST phishing categories
- Brand impersonation analysis performed when applicable
- Language quality assessed for translation artifacts and grammar indicators
- Every URL extracted, defanged, and analyzed (including mismatch detection between visible text and href)
- URL redirect chains traced where applicable
- Every attachment inventoried with file metadata, risk indicators, and hash computation
- Static analysis performed per attachment type (macros, OLE, PE, scripts, PDF actions, etc.)
- Sandbox detonation recommended for suspicious attachments with platform and configuration guidance
- Polyglot file detection performed where applicable
- Payload classified using the classification matrix with confidence levels
- Content analysis appended to report under `## Content & Payload Analysis`
- Frontmatter updated with urls_found, attachments_found, payload_type and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Fabricating content not present in the preserved email from step 1
- Executing, opening, or detonating any attachment (all analysis must be static)
- Not defanging URLs before recording in the report
- Missing URL mismatches between visible text and HTML href attributes
- Not computing hashes for every attachment
- Treating absence of technical payload as "clean" (BEC/social engineering attacks have no technical payload)
- Not classifying the payload type
- Beginning IOC enrichment, scope assessment, or containment during content analysis
- Skipping social engineering technique identification
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with content analysis metrics and stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every content component must be analyzed. Absence of technical payload does not mean absence of threat.
