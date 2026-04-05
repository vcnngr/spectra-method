# Step 2: Email Header Deep Analysis

**Progress: Step 2 of 8** — Next: Content & Payload Analysis

## STEP GOAL:

Perform comprehensive analysis of the email headers to trace the email's true origin, verify authentication mechanisms (SPF, DKIM, DMARC, ARC), map the originating infrastructure, detect header anomalies and spoofing indicators, and assess sender reputation — producing a structured header analysis that establishes whether the email is forged, spoofed, or originates from legitimate-but-compromised infrastructure.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER modify raw email headers — analyze alongside the preserved original
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC PHISHING ANALYST, not an autonomous email gateway
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst conducting structured phishing investigation
- ✅ Header analysis is the forensic backbone of phishing investigation — it reveals the true origin, delivery path, and authenticity of the email
- ✅ Every authentication check must cite the specific header value and result — unsupported claims about email authenticity degrade investigation quality
- ✅ Headers can be forged too — a PASS result on SPF/DKIM/DMARC does not guarantee the email is legitimate; it means the sending infrastructure was configured correctly for that domain
- ✅ If headers are unavailable (screenshot/user report input), document the limitation clearly and skip to available analysis

### Step-Specific Rules:

- 🎯 Focus exclusively on email header forensics — Received chain, authentication, infrastructure, anomalies
- 🚫 FORBIDDEN to begin content analysis, URL investigation, or any containment activity — this is header forensics only
- 💬 Approach: Systematic header-by-header analysis with structured findings
- 📊 Every finding must cite the specific header name and value
- 🔒 All analysis must reference headers from the preserved email in step 1 — do not fabricate header data
- ⚠️ If the input format from step 1 has no headers (screenshot, user report): document this limitation, extract whatever sender information is available from the visual/textual input, and note that header analysis is incomplete

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - SPF/DKIM/DMARC all passing does NOT mean the email is legitimate — a threat actor who compromised a legitimate email account, or who properly configured a lookalike domain with valid DNS records, will pass all authentication checks; authentication proves the email was sent by the claimed infrastructure, not that the infrastructure is trustworthy
  - A single Received header (or very few hops) may indicate the email was injected directly into the mail server, bypassing normal internet routing — this is common in compromised account scenarios and internal phishing; it does not automatically mean the email is benign
  - Display name spoofing combined with a legitimate-looking domain is one of the most effective phishing techniques — the From display name shows "CEO Name" but the actual address is from an unrelated domain; always compare display name against actual email domain and organizational directory
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present header analysis plan before beginning — acknowledge any limitations from input format
- ⚠️ Present [A]/[W]/[C] menu after analysis complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `spf_result`, `dkim_result`, `dmarc_result`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Engagement scope, phishing email sample, extracted metadata, raw email source from step 1
- Focus: Email header forensics — authentication, infrastructure, anomalies
- Limits: Only analyze headers present in the step 1 preserved email — do not fabricate header data
- Dependencies: Completed email intake and metadata extraction from step-01-init.md

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Header Availability Assessment

Before beginning analysis, assess what header data is available based on the input format from step 1:

**Header Data Assessment:**

| Data Category | Available? | Source |
|---------------|-----------|--------|
| Received chain | Yes/No/Partial | {{EML/MSG/raw headers/forwarded}} |
| Authentication-Results | Yes/No | {{header present?}} |
| SPF record reference | Yes/No | {{Received-SPF or Authentication-Results}} |
| DKIM-Signature | Yes/No | {{DKIM-Signature header present?}} |
| DMARC policy | Yes/No | {{Authentication-Results or DNS lookup needed}} |
| ARC headers | Yes/No | {{ARC-Seal, ARC-Message-Signature, ARC-Authentication-Results}} |
| X-headers | Yes/No/Partial | {{X-Originating-IP, X-Mailer, X-MS-Exchange-*, etc.}} |
| Return-Path | Yes/No | {{Return-Path header present?}} |
| Reply-To | Yes/No | {{Reply-To header present?}} |

**If NO headers available (screenshot/user report):**

"⚠️ **Header Analysis Limitation**

The phishing sample was provided as {{format_type}}, which contains no email header data. Header-based analysis (Received chain tracing, authentication verification, infrastructure mapping) cannot be performed.

**Available analysis with current data:**
- Sender display name and visible address (from visual/textual content)
- Reply-To information (if visible in the email client)
- General sender legitimacy assessment based on domain name

**Recommendation:** Request the original email headers from the email gateway or mail server logs. This will enable complete header forensics.

Proceeding with available data."

**If PARTIAL headers (forwarded email, gateway alert):**

"⚠️ **Header Analysis — Partial Data**

The phishing sample was provided as {{format_type}}. Some headers may have been modified during forwarding or parsing. Findings are noted with confidence levels.

Proceeding with available headers."

### 2. Received Chain Analysis

Trace the email's delivery path hop by hop, starting from the BOTTOM Received header (first hop) to the TOP (last hop before delivery).

**For each Received header, extract:**

| Hop # | From (Sending MTA) | By (Receiving MTA) | Protocol | Timestamp (UTC) | Delay | Notes |
|-------|--------------------|--------------------|----------|-----------------|-------|-------|
| 1 (origin) | {{sending server hostname/IP}} | {{receiving server hostname/IP}} | {{SMTP/ESMTP/ESMTPS/ESMTPSA}} | {{timestamp converted to UTC}} | — | {{first hop — true origin}} |
| 2 | {{next hop}} | {{next hop}} | {{protocol}} | {{timestamp}} | {{delta from previous hop}} | {{internal relay? external gateway?}} |
| ... | ... | ... | ... | ... | ... | ... |
| N (delivery) | {{last sending server}} | {{recipient's mail server}} | {{protocol}} | {{timestamp}} | {{delta}} | {{final delivery to mailbox}} |

**Received Chain Analysis:**

- **Total hops:** {{count}}
- **Total transit time:** {{time from first Received to last Received}}
- **Origin server:** {{hostname/IP from the first (bottom) Received header}}
- **Delivery server:** {{hostname/IP from the last (top) Received header}}

**Received Chain Anomaly Detection:**

| Anomaly | Detection Method | Finding |
|---------|-----------------|---------|
| Timestamp inconsistency | Hop N+1 timestamp < Hop N timestamp | {{Found/Not Found — detail if found}} |
| Excessive delay | Any single hop > 30 minutes | {{Found/Not Found — which hop, how long}} |
| Missing hops | Gap in relay chain or direct injection | {{Found/Not Found — detail}} |
| Internal-only routing | No external hops, email appears injected | {{Found/Not Found — could indicate compromised internal account}} |
| Unknown relay | MTA hostname not matching known infrastructure | {{Found/Not Found — detail}} |
| Protocol downgrade | ESMTPS → ESMTP (TLS dropped during transit) | {{Found/Not Found — which hop}} |
| Suspicious with clause | "with" clause indicates unusual protocol or auth method | {{Found/Not Found — detail}} |

### 3. Authentication Verification

Verify all email authentication mechanisms. Check both the Authentication-Results header (if present) and perform independent verification where possible.

#### A. SPF (Sender Policy Framework) Verification

**SPF Check:**

| Component | Value |
|-----------|-------|
| Sender (MAIL FROM / Return-Path) | {{envelope_sender_address}} |
| Sender Domain | {{domain from envelope sender}} |
| Sending IP | {{IP from first Received header or Received-SPF header}} |
| SPF Record | {{TXT record for sender domain, e.g., "v=spf1 include:_spf.google.com ~all"}} |
| SPF Result | {{pass / fail / softfail / neutral / none / temperror / permerror}} |
| Alignment | {{strict (exact domain match) / relaxed (organizational domain match) / none}} |

**SPF Result Interpretation:**
- **pass**: Sending IP is authorized by the domain's SPF record — does NOT mean email is legitimate, only that the infrastructure is authorized
- **fail**: Sending IP is NOT authorized — strong indicator of spoofing
- **softfail (~all)**: Domain owner suspects this IP is unauthorized but does not hard-reject — common in misconfigured or transitional SPF
- **neutral (?all)**: Domain makes no assertion — SPF provides no signal
- **none**: No SPF record published — domain does not implement SPF
- **temperror/permerror**: DNS lookup failed or SPF record is malformed

#### B. DKIM (DomainKeys Identified Mail) Verification

**DKIM Check:**

| Component | Value |
|-----------|-------|
| DKIM-Signature Present | Yes/No |
| Signing Domain (d=) | {{domain that signed the email}} |
| Selector (s=) | {{DKIM selector used}} |
| Algorithm (a=) | {{rsa-sha256 / rsa-sha1 / ed25519-sha256}} |
| Header Fields Signed (h=) | {{list of signed headers}} |
| Body Hash (bh=) | {{base64 body hash}} |
| DKIM Result | {{pass / fail / none / temperror / permerror}} |
| Key Length | {{key bit length from DNS selector record, e.g., 2048-bit RSA}} |
| From Alignment | {{DKIM d= domain matches From domain? strict/relaxed/mismatch}} |

**DKIM Result Interpretation:**
- **pass**: Email body and signed headers have not been modified since signing — the email was sent by infrastructure authorized to sign for the d= domain
- **fail**: Email has been modified in transit, or the DKIM key is invalid — possible tampering or misconfiguration
- **none**: No DKIM-Signature header present — the sending domain does not sign emails with DKIM
- **Multiple signatures**: Some emails carry multiple DKIM signatures (e.g., original sender + mailing list). Evaluate each independently.

**DKIM Signing Domain Analysis:**
- Does d= match the From address domain? (alignment check)
- If d= is a different domain (e.g., d=sendgrid.net for an email From: ceo@company.com), this indicates the email was sent through a third-party service — determine if this is expected for the claimed sender

#### C. DMARC (Domain-based Message Authentication, Reporting, and Conformance) Verification

**DMARC Check:**

| Component | Value |
|-----------|-------|
| DMARC Record | {{_dmarc.domain TXT record, e.g., "v=DMARC1; p=reject; rua=..."}} |
| Policy (p=) | {{none / quarantine / reject}} |
| Subdomain Policy (sp=) | {{none / quarantine / reject / [inherits from p=]}} |
| Alignment Mode (adkim=) | {{strict (s) / relaxed (r)}} |
| Alignment Mode (aspf=) | {{strict (s) / relaxed (r)}} |
| Percentage (pct=) | {{percentage of messages subject to policy, default 100}} |
| SPF Alignment | {{pass / fail}} — SPF domain aligns with From domain? |
| DKIM Alignment | {{pass / fail}} — DKIM d= domain aligns with From domain? |
| DMARC Result | {{pass (at least one alignment passes) / fail (neither aligns)}} |

**DMARC Policy Impact:**
- **p=none**: Domain monitors but does not enforce — even a DMARC fail will not cause rejection (weak posture, common during DMARC rollout)
- **p=quarantine**: Failing emails should be quarantined — indicates the domain has moderate DMARC enforcement
- **p=reject**: Failing emails should be rejected outright — indicates strong DMARC enforcement; if the phishing email still reached the mailbox despite DMARC reject, the receiving gateway may not enforce DMARC, or the email passed DMARC

**CRITICAL NOTE:** DMARC pass means the email was sent by infrastructure authorized for the From domain. It does NOT mean the sender is who they claim to be. A threat actor who registers `company-support.com` and properly configures SPF, DKIM, and DMARC will pass all checks. Always evaluate the From domain itself, not just the authentication results.

#### D. ARC (Authenticated Received Chain) Verification

If ARC headers are present (common when email passes through mailing lists, forwarding services, or cloud email gateways):

**ARC Check:**

| Component | Value |
|-----------|-------|
| ARC-Seal Present | Yes/No |
| ARC Instance (i=) | {{instance number — indicates how many ARC-aware intermediaries handled the email}} |
| ARC-Authentication-Results | {{authentication results as seen by each ARC intermediary}} |
| ARC Validation | {{pass / fail / none}} |
| ARC Chain Integrity | {{valid (all seals verify) / broken (seal verification failed) / none (no ARC)}} |

**ARC Significance:** ARC preserves authentication results across forwarding hops. If SPF/DKIM fail due to legitimate forwarding but ARC chain is valid, the original authentication results (before forwarding broke them) can be trusted.

### 4. Originating Infrastructure Mapping

Identify the true origin of the phishing email by analyzing the first Received header and correlating with authentication data.

**Origin Infrastructure:**

| Component | Value |
|-----------|-------|
| True Origin IP | {{IP from first Received header or X-Originating-IP}} |
| Reverse DNS (PTR) | {{rDNS result for origin IP}} |
| ASN | {{AS number and organization name}} |
| ISP / Hosting Provider | {{ISP or hosting company}} |
| Geolocation | {{Country, City}} |
| Mail Service Identification | {{known service or unknown}} |

**Known Mail Service Detection:**

| Service Pattern | Detection Method | Identified? |
|-----------------|-----------------|-------------|
| Gmail / Google Workspace | Received: from mail-*.google.com, DKIM d=*.gserviceaccount.com | {{Yes/No}} |
| Microsoft 365 / Exchange Online | Received: from *.protection.outlook.com, X-MS-Exchange-* headers | {{Yes/No}} |
| Amazon SES | Received: from *.amazonses.com, DKIM d=amazonses.com | {{Yes/No}} |
| SendGrid | Received: from *.sendgrid.net, DKIM d=sendgrid.net | {{Yes/No}} |
| Mailchimp / Mandrill | Received: from *.mandrillapp.com or *.rsgsv.net | {{Yes/No}} |
| Proofpoint | Received: from *.pphosted.com | {{Yes/No}} |
| Mimecast | Received: from *.mimecast.com | {{Yes/No}} |
| Barracuda | Received: from *.barracuda.com | {{Yes/No}} |
| Custom / self-hosted | No known service pattern — check PTR, WHOIS | {{Yes/No}} |
| Bulletproof hosting | IP in known bulletproof ASN ranges | {{Yes/No}} |
| Compromised infrastructure | Legitimate service + anomalous sending patterns | {{Assessment}} |

**Infrastructure Assessment:**
- **Sending platform**: {{identified service or 'Unknown/Custom'}}
- **Infrastructure legitimacy**: {{Legitimate service (potentially compromised account) / Purpose-built attacker infrastructure / Free-tier abuse / Compromised server / Unknown}}
- **Geographic consistency**: Does the sending location match the claimed sender's expected location? {{Yes/No/Cannot determine}}

### 5. Header Anomaly Detection

Systematically check for header-based indicators of phishing, spoofing, and manipulation.

**Anomaly Detection Matrix:**

| Anomaly Category | Check | Finding | Severity |
|-----------------|-------|---------|----------|
| **Reply-To Mismatch** | Reply-To header differs from From address | {{detail or 'Not present'}} | {{🔴 High / 🟡 Medium / 🟢 Clean}} |
| **Return-Path Mismatch** | Return-Path / envelope sender differs from From address | {{detail or 'Aligned'}} | {{🔴/🟡/🟢}} |
| **Display Name Spoofing** | From display name impersonates known entity but email domain differs | {{detail or 'Not detected'}} | {{🔴/🟡/🟢}} |
| **Homoglyph Domain** | From domain uses lookalike characters (e.g., rn→m, l→1, 0→O) | {{detail or 'Not detected'}} | {{🔴/🟡/🟢}} |
| **Cousin Domain** | From domain is a lookalike registration (e.g., company-support.com, companyy.com) | {{detail or 'Not detected'}} | {{🔴/🟡/🟢}} |
| **Subdomain Spoofing** | From domain uses brand as subdomain (e.g., microsoft.attacker.com) | {{detail or 'Not detected'}} | {{🔴/🟡/🟢}} |
| **X-Originating-IP** | Reveals true sender IP (common in webmail) | {{IP or 'Not present'}} | {{Informational}} |
| **X-Mailer Anomaly** | Unusual or suspicious email client identifier | {{detail or 'Normal/Not present'}} | {{🟡/🟢}} |
| **X-PHP-Script** | Indicates email sent via PHP script (webshell, compromised website) | {{detail or 'Not present'}} | {{🔴 if present}} |
| **Timestamp Inconsistency** | Date header vs Received timestamps are significantly different | {{detail or 'Consistent'}} | {{🟡/🟢}} |
| **Missing Standard Headers** | Expected headers absent (Message-ID, Date, MIME-Version) | {{list or 'All present'}} | {{🟡/🟢}} |
| **Encoding Anomalies** | Unusual Content-Transfer-Encoding or charset in headers | {{detail or 'Normal'}} | {{🟡/🟢}} |
| **Precedence / Priority** | Bulk or list headers on a supposedly personal email | {{detail or 'Not present'}} | {{🟡/🟢}} |
| **List-Unsubscribe** | Unsubscribe header on targeted/personal email (mass mailer indicator) | {{present/absent}} | {{🟡 if present on targeted email}} |

### 6. Sender Reputation Assessment

Consolidate all header findings into a sender reputation assessment:

**Sender Reputation Summary:**

```
Sender Address: {{from_address}}
Sender Domain: {{from_domain}}
Envelope Sender: {{return_path_address}}
Sending Infrastructure: {{identified platform/IP}}

Authentication Summary:
- SPF: {{result}} ({{detail}})
- DKIM: {{result}} (d={{signing_domain}})
- DMARC: {{result}} (p={{policy}})
- ARC: {{result or 'N/A'}}

Infrastructure Assessment:
- Origin IP: {{ip}} ({{country}}, AS{{asn}} {{org}})
- rDNS: {{ptr_record}}
- Service: {{identified_service or 'Unknown'}}
- Infrastructure type: {{legitimate/attacker-controlled/compromised/unknown}}

Anomalies Detected: {{count}}
- Critical (🔴): {{count}} — {{summary}}
- Warning (🟡): {{count}} — {{summary}}
- Clean (🟢): {{count}}

Header Analysis Verdict:
{{FORGED — authentication fails, headers indicate spoofing}}
{{SPOOFED — display name/domain impersonation with separate infrastructure}}
{{COMPROMISED — legitimate account/infrastructure sending malicious content}}
{{SUSPICIOUS — anomalies detected but no definitive spoofing indicator}}
{{LEGITIMATE INFRASTRUCTURE — authentication passes, infrastructure matches claimed sender, but content may still be malicious}}
{{INSUFFICIENT DATA — not enough header data to make a determination}}

Confidence: {{High / Medium / Low}}
```

### 7. Present Header Analysis to User

"**Header Analysis Complete — {{incident_id}}**

**Authentication Results:**
| Protocol | Result | Detail |
|----------|--------|--------|
| SPF | {{result}} | {{sender_ip}} {{authorized/unauthorized}} for {{domain}} |
| DKIM | {{result}} | Signed by {{d= domain}}, alignment: {{aligned/misaligned}} |
| DMARC | {{result}} | Policy: {{p= value}}, alignment: {{pass/fail}} |
| ARC | {{result or 'N/A'}} | {{detail}} |

**Origin Infrastructure:**
- **Sending IP:** {{origin_ip}} ({{country}}, {{isp}})
- **Mail Service:** {{identified_service or 'Unknown/Custom'}}
- **Infrastructure Type:** {{legitimate/attacker/compromised/unknown}}

**Anomalies Detected:** {{total_count}}
- 🔴 Critical: {{count}} — {{list}}
- 🟡 Warning: {{count}} — {{list}}

**Header Verdict:** {{FORGED / SPOOFED / COMPROMISED / SUSPICIOUS / LEGITIMATE INFRASTRUCTURE / INSUFFICIENT DATA}}
**Confidence:** {{High / Medium / Low}}"

### 8. Present MENU OPTIONS

"**Select an option:**
[A] Advanced Elicitation — Deep-dive into specific header findings, challenge authentication assumptions, investigate infrastructure further
[W] War Room — Red vs Blue discussion on header analysis implications — how would an attacker set up this infrastructure? What should the email gateway have caught?
[C] Continue — Proceed to Content & Payload Analysis (Step 3 of 8)"

#### Menu Handling Logic:

- IF A: Deep-dive header analysis — investigate specific anomalies further, query DNS records for the sender domain, examine X-headers in more detail, challenge assumptions about authentication results (e.g., SPF pass does not mean legitimate), explore whether the sending infrastructure is part of a known campaign. Process insights, ask user if they want to update findings, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: how would I set up this sending infrastructure? Is this a free-tier abuse, compromised account, or purpose-built domain? How sophisticated is the email authentication setup? What does the infrastructure tell us about the attacker's resources? Blue Team perspective: what should our email gateway have caught? Are our SPF/DKIM/DMARC policies adequate? Would this email have been caught by a stricter DMARC policy? What header-based detection rules could catch this pattern? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `spf_result`, `dkim_result`, `dmarc_result`, then read fully and follow: ./step-03-content-analysis.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and spf_result, dkim_result, dmarc_result updated, and header analysis results appended to report under `## Header Analysis`], will you then read fully and follow: `./step-03-content-analysis.md` to begin content and payload analysis.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Header data availability assessed and limitations documented
- Received chain analyzed hop by hop with timestamps, delays, and anomalies
- All authentication mechanisms checked (SPF, DKIM, DMARC, ARC) with specific header values cited
- Originating infrastructure mapped (IP, rDNS, ASN, geolocation, mail service identification)
- Header anomaly detection matrix completed for all anomaly categories
- Sender reputation assessment consolidates all findings into a structured verdict
- Authentication results correctly interpreted (pass ≠ legitimate)
- Header analysis appended to report under `## Header Analysis`
- Frontmatter updated with spf_result, dkim_result, dmarc_result and step added to stepsCompleted
- If headers unavailable: limitation clearly documented, available analysis performed, recommendation to obtain headers issued
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Fabricating header data not present in the preserved email from step 1
- Treating SPF/DKIM/DMARC pass as proof of email legitimacy
- Not analyzing the full Received chain when headers are available
- Not detecting Reply-To / Return-Path / display name mismatches when they exist in the headers
- Skipping authentication verification for any available protocol
- Not mapping the originating infrastructure when the origin IP is available
- Beginning content analysis, URL investigation, or containment during header analysis
- Not documenting limitations when headers are unavailable or partial
- Proceeding to content analysis without completing all available header checks
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with authentication results and stepsCompleted

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every available header must be analyzed. Authentication pass does not equal legitimacy.
