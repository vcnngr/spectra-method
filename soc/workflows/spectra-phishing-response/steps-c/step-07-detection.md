# Step 7: Detection & Prevention

**Progress: Step 7 of 8** — Next: Reporting & Closure

## STEP GOAL:

Create detection rules and prevention improvements based on the phishing analysis — email gateway rules for sender/domain/subject/attachment patterns, Sigma/YARA/Suricata detection rules for email-delivered IOCs and post-exploitation behavior, user awareness communications, and Purple Team feedback that bridges the Blue Team findings to Red Team testing — producing actionable detection improvements that strengthen the organization's defenses against this and similar phishing campaigns.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER deploy detection rules directly — all rules are RECOMMENDATIONS for the detection engineering team
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE A SOC PHISHING ANALYST creating detection improvements — NOT deploying them to production
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a SOC Phishing Analyst creating detection and prevention improvements based on phishing investigation findings
- ✅ Every detection rule must include: description, logic, ATT&CK mapping, test case, and false positive assessment
- ✅ Detection rules should target behavior patterns, not just IOCs — IOCs rotate, behaviors persist
- ✅ Purple Team feedback must include specific tests for the Red Team to execute
- ✅ User awareness communications should be informative without causing panic

### Step-Specific Rules:

- 🎯 Focus on detection rule creation, prevention improvement recommendations, user communications, and Purple Team feedback
- 🚫 FORBIDDEN to deploy any rules to production — recommendations only
- 💬 Approach: Systematic detection improvement across email gateway, SIEM, network, and endpoint layers
- 📊 Every rule must include test case and FP assessment
- 🔒 Rules must be based on findings from steps 1-6 — do not create rules for hypothetical scenarios

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Detection rules based solely on static IOCs (specific IPs, domains, hashes) provide short-term protection but become ineffective as soon as the attacker rotates infrastructure — complement IOC-based rules with behavioral rules (e.g., detect login page impersonation patterns, macro execution chains, or email authentication failures) for durable detection
  - Sending a user awareness notification that is too specific about the phishing email content may inadvertently teach users to recognize only this exact phishing template while creating a false sense of security — awareness communications should describe the general technique (urgency, brand impersonation, credential harvesting) and reinforce reporting behavior, not just describe this one email
  - DMARC enforcement recommendations must be phased carefully — moving from p=none to p=reject without a monitoring period (p=quarantine with pct=10, then pct=50, then pct=100, then p=reject) may block legitimate email from third-party senders not yet included in the SPF record; aggressive DMARC rollout without monitoring causes business disruption
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Present detection improvement plan before beginning rule creation
- ⚠️ Present [A]/[W]/[C] menu after detection improvements are complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted and updating `detection_rules_created`, `purple_team_items`
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Complete phishing analysis (steps 1-4), blast radius (step 5), containment plan (step 6)
- Focus: Detection rules, prevention improvements, user communications, Purple Team feedback
- Limits: Rules are recommendations — not deployed. Based on actual investigation findings, not hypotheticals.
- Dependencies: Completed phishing analysis and containment planning from steps 1-6

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Email Gateway Rules

Create email gateway detection and blocking rules based on the phishing email characteristics:

**Email Gateway Rule Recommendations:**

#### A. Sender/Domain Rules

| Rule # | Rule Name | Type | Logic | Scope | Expected FP Rate | Notes |
|--------|-----------|------|-------|-------|------------------|-------|
| EG-01 | Block sender address | Sender block | From = {{sender_address}} | Organization-wide | None | Exact match — attacker may change address |
| EG-02 | Block sender domain | Domain block | From domain = {{sender_domain}} | Organization-wide | {{FP risk if legitimate domain}} | Only if domain is purpose-built for phishing |
| EG-03 | Subject pattern match | Content filter | Subject contains "{{pattern}}" | Organization-wide | {{FP assessment}} | Temporary — review after 30 days |
| EG-04 | Reply-To mismatch + pattern | Anomaly rule | Reply-To domain ≠ From domain AND subject matches pattern | Organization-wide | Low-Medium | Catches reply-to spoofing variants |

#### B. Attachment Rules

| Rule # | Rule Name | Type | Logic | Scope | Expected FP Rate | Notes |
|--------|-----------|------|-------|-------|------------------|-------|
| EG-05 | Block attachment by hash | Hash block | SHA256 = {{attachment_hash}} | Organization-wide | None | Exact match — attacker may modify file |
| EG-06 | Block attachment by name pattern | Filename filter | Filename matches "{{pattern}}" | Organization-wide | {{FP assessment}} | {{justification}} |
| EG-07 | Block macro-enabled attachments from external | Macro policy | External sender + attachment has macros | External senders | Medium — legitimate macros exist | Reduces macro-based phishing surface |

#### C. URL Rewriting and Safe Links

| Rule # | Rule Name | Type | Logic | Scope | Expected FP Rate | Notes |
|--------|-----------|------|-------|-------|------------------|-------|
| EG-08 | Block phishing URL | URL block | URL matches {{defanged_url_pattern}} | Organization-wide | None | Exact match |
| EG-09 | Block phishing domain | URL domain block | URL domain = {{malicious_domain}} | Organization-wide | {{FP assessment}} | Block entire domain in URL filter |
| EG-10 | Safe Links / URL rewriting | URL policy | Enable real-time URL scanning for all inbound email | Organization-wide | Low | Catches new URLs not yet in block lists |

#### D. Authentication Enforcement

**SPF/DKIM/DMARC Enforcement Recommendations:**

| Recommendation | Current State | Recommended State | Implementation Guidance |
|---------------|--------------|-------------------|------------------------|
| SPF enforcement | {{current policy}} | Hard fail reject (-all) | Ensure all legitimate sending IPs are in SPF record before enforcing |
| DKIM verification | {{current state}} | Require DKIM pass for external mail | Enable DKIM checking on email gateway |
| DMARC policy (own domain) | {{current p= value}} | p=reject (phased rollout) | Phase: p=none → p=quarantine pct=10 → pct=50 → pct=100 → p=reject |
| DMARC enforcement (inbound) | {{current enforcement}} | Honor sender DMARC policy | Configure gateway to reject/quarantine based on sender's DMARC |
| External sender tagging | {{current state}} | Tag all external emails | Add [EXTERNAL] tag or banner to all external emails |

### 2. Detection Rule Creation

Create formal detection rules for the phishing campaign IOCs and behaviors:

#### A. Sigma Rules — Email IOCs

**Sigma Rule — Phishing Email IOC Detection:**

```yaml
title: "Phishing Campaign IOC — {{incident_id}} — Email Infrastructure"
id: {{generate UUID}}
status: experimental
description: |
  Detects network communication with infrastructure associated with phishing campaign {{incident_id}}.
  Sender: {{sender_address}}
  Campaign type: {{payload_type}}
  ATT&CK: {{primary_technique}}
references:
  - "Internal: Phishing Report {{incident_id}}"
author: "{{user_name}} via SPECTRA spectra-phishing-response"
date: {{date}}
tags:
  - attack.initial_access
  - attack.{{technique_id_dotted}}
logsource:
  category: proxy
  # Alternative: dns, firewall, web
detection:
  selection_domain:
    c-uri|contains:
      - '{{malicious_domain_1}}'
      - '{{malicious_domain_2}}'
  selection_ip:
    dst_ip:
      - '{{malicious_ip_1}}'
      - '{{malicious_ip_2}}'
  condition: selection_domain or selection_ip
falsepositives:
  - "{{FP assessment — e.g., 'None expected — domains are purpose-built phishing infrastructure'}}"
  - "{{Additional FP scenario if applicable}}"
level: high
```

#### B. Sigma Rules — Post-Exploitation (if payload was executed)

**Sigma Rule — Phishing Payload Execution Behavior:**

```yaml
title: "Phishing Payload Execution — {{incident_id}} — Process Chain"
id: {{generate UUID}}
status: experimental
description: |
  Detects process execution patterns associated with the payload delivered in phishing campaign {{incident_id}}.
  Payload type: {{payload_type}}
  Malware family: {{malware_family or 'Unknown'}}
references:
  - "Internal: Phishing Report {{incident_id}}"
author: "{{user_name}} via SPECTRA spectra-phishing-response"
date: {{date}}
tags:
  - attack.execution
  - attack.{{relevant_technique_id}}
logsource:
  category: process_creation
  product: windows
detection:
  selection_parent:
    ParentImage|endswith:
      - '\\OUTLOOK.EXE'
      - '\\WINWORD.EXE'
      - '\\EXCEL.EXE'
      - '\\POWERPNT.EXE'
  selection_child:
    Image|endswith:
      - '\\cmd.exe'
      - '\\powershell.exe'
      - '\\wscript.exe'
      - '\\cscript.exe'
      - '\\mshta.exe'
      - '\\rundll32.exe'
      - '\\regsvr32.exe'
      - '\\certutil.exe'
  condition: selection_parent and selection_child
falsepositives:
  - "Legitimate Office macros that spawn command-line tools — validate against allowlisted macros"
  - "IT administrative tools triggered from Outlook links"
level: high
```

#### C. YARA Rule (if malware sample available)

**YARA Rule — Phishing Attachment:**

```yara
rule phishing_attachment_{{incident_id}} {
    meta:
        description = "Detects attachment from phishing campaign {{incident_id}}"
        author = "{{user_name}} via SPECTRA"
        date = "{{date}}"
        reference = "Phishing Report {{incident_id}}"
        hash = "{{sha256_hash}}"
        malware_family = "{{family or 'Unknown'}}"
        mitre_attack = "{{technique_id}}"
        
    strings:
        {{$s1 = "unique string from static analysis" ascii wide}}
        {{$s2 = "another unique string" ascii wide}}
        {{$s3 = { hex bytes pattern from file } }}
        
    condition:
        {{file_magic_check}} and
        ({{string_combination}}) and
        filesize < {{max_size}}
}
```

#### D. Suricata/Snort Rule (Network IOCs)

**Suricata Rule — Phishing C2 Communication:**

```
# Detect DNS query for phishing domain
alert dns $HOME_NET any -> any 53 (msg:"SPECTRA — Phishing campaign {{incident_id}} — DNS query for malicious domain"; dns.query; content:"{{malicious_domain}}"; nocase; classtype:trojan-activity; sid:{{sid}}; rev:1; metadata:mitre_technique_id {{technique_id}}, created_at {{date}}, updated_at {{date}};)

# Detect HTTP/TLS connection to phishing infrastructure
alert tls $HOME_NET any -> $EXTERNAL_NET any (msg:"SPECTRA — Phishing campaign {{incident_id}} — TLS to malicious domain"; tls.sni; content:"{{malicious_domain}}"; nocase; classtype:trojan-activity; sid:{{sid+1}}; rev:1;)

# Detect connection to phishing IP
alert ip $HOME_NET any -> {{malicious_ip}} any (msg:"SPECTRA — Phishing campaign {{incident_id}} — Connection to phishing IP"; classtype:trojan-activity; sid:{{sid+2}}; rev:1;)
```

#### E. Detection Rule Summary

| Rule # | Type | Target | ATT&CK | FP Rate | Test Case | Status |
|--------|------|--------|--------|---------|-----------|--------|
| SIGMA-01 | Sigma (proxy/DNS) | Phishing infrastructure IOCs | T1566.00X | {{rate}} | Query for malicious domain from test host | Recommendation |
| SIGMA-02 | Sigma (process) | Post-exploitation process chain | T1059.00X | {{rate}} | Simulate Office → cmd/PS execution | Recommendation |
| YARA-01 | YARA | Phishing attachment detection | T1566.001 | {{rate}} | Scan with sample hash | Recommendation |
| SURI-01 | Suricata | DNS/network IOC detection | T1071.001 | {{rate}} | DNS query for test domain | Recommendation |
| EG-01–10 | Email gateway | Email-layer blocking | T1566.00X | {{rate}} | Send test email matching rule | Recommendation |

**Detection Rule Output:**
- Save Sigma rules to: `{soc_detection_rules}/sigma/phishing-{{incident_id}}-*.yml`
- Save YARA rules to: `{soc_detection_rules}/yara/phishing-{{incident_id}}.yar`
- Save Suricata rules to: `{soc_detection_rules}/suricata/phishing-{{incident_id}}.rules`

### 3. Awareness & Communication

#### A. User Notification (Recipients Who Received But Did Not Interact)

**Phishing Alert — User Notification Template:**

```
Subject: Security Alert — Phishing Email Detected — Action Required

To: [affected users — Tier 1 and Tier 2]
From: [IT Security / SOC Team]

Dear colleague,

Our security team has identified a phishing email that was delivered to your inbox. 
The email has been [removed / will be removed shortly].

**What to look for:**
- Subject line containing: "{{subject_pattern}}"
- Sender appearing as: {{sender_display_name}}
- Email requesting: {{general_action — e.g., "you to click a link and enter your credentials"}}

**What you should do:**
1. Do NOT click any links or open any attachments in this email
2. Do NOT reply to the email
3. If you have already interacted with the email (clicked a link, opened an attachment, 
   or entered any information), contact the IT Security team IMMEDIATELY at [contact info]
4. Delete the email from your inbox and trash

**How to report suspicious emails in the future:**
- [Organization-specific reporting mechanism — e.g., "Click the Report Phishing button in Outlook"]
- [Or forward to phishing@company.com]

Thank you for your vigilance.

[IT Security Team]
```

#### B. Security Awareness Reminder

**Security Awareness Reminder Template:**

```
Subject: Security Awareness Reminder — How to Spot Phishing Emails

Key indicators of phishing emails:
1. Urgency or threats — "Your account will be suspended", "Immediate action required"
2. Sender address doesn't match the claimed organization
3. Links that don't go where they appear to — hover before clicking
4. Unexpected attachments, especially Office documents with macros
5. Requests for credentials, personal information, or financial transactions
6. Generic greetings when the sender should know your name

When in doubt:
- Don't click, don't open, don't reply
- Report the email using [organization's reporting mechanism]
- Contact IT Security at [contact info]
```

#### C. IT/Helpdesk Notification

**IT/Helpdesk Brief:**

```
Subject: PHISHING CAMPAIGN ACTIVE — {{incident_id}} — Helpdesk Brief

Priority: {{severity}}
Date: {{date}}

SITUATION:
A phishing campaign targeting our organization has been identified. 
{{blast_radius_summary}}

WHAT TO EXPECT:
- Users may contact helpdesk reporting suspicious email matching:
  Subject: "{{subject_pattern}}"
  Sender: {{sender_display_name}} <{{sender_address}}>
- Users who clicked the link may report being unable to access their accounts 
  (due to password reset as part of containment)
- {{additional expected user contacts}}

HELPDESK ACTIONS:
1. Log all user reports as related to incident {{incident_id}}
2. If user ONLY received the email: reassure them, confirm email will be purged
3. If user CLICKED a link: escalate to SOC team at [contact] — mark URGENT
4. If user OPENED an attachment: escalate to SOC team at [contact] — mark CRITICAL
5. If user ENTERED credentials: escalate to SOC team at [contact] — mark CRITICAL
6. Do NOT attempt to remediate independently — SOC team is coordinating response

SOC CONTACT: [contact info]
```

#### D. Executive Notification (If High/Critical Severity)

**Executive Brief:**

```
Subject: Security Incident — Phishing Campaign — {{incident_id}}

Severity: {{severity}}
Date: {{date}}

SUMMARY:
A phishing campaign has been detected targeting {{count}} employees.
{{1-2 sentence description of the attack and its impact}}

IMPACT:
- {{users_received}} employees received the phishing email
- {{users_clicked}} employees clicked the link/opened the attachment
- {{accounts_compromised}} accounts potentially compromised
- {{endpoints_compromised}} endpoints potentially compromised
- Regulatory notification: {{required/not required}} — {{detail if required}}

ACTIONS TAKEN:
- {{containment_summary}}
- {{detection_summary}}

CURRENT STATUS: {{Contained / Partially Contained / Under Investigation}}

NEXT STEPS:
1. {{next_step_1}}
2. {{next_step_2}}

RISK ASSESSMENT:
- Data exposure: {{level}}
- Financial risk: {{level}}
- Reputational risk: {{level}}

Contact: [SOC team contact]
```

### 4. Purple Team Feedback

Create Purple Team feedback items that bridge Blue Team phishing investigation findings to Red Team testing:

**Purple Team Feedback — Phishing Response {{incident_id}}:**

```yaml
# Purple Team Feedback — Phishing Response
# Generated by: spectra-phishing-response workflow
# Date: {{date}}

engagement_id: {{engagement_id}}
incident_id: {{incident_id}}
analyst: {{user_name}}
classification: {{payload_type}}
severity: {{severity}}
mitre_techniques: {{mitre_techniques}}
```

#### A. Email Gateway Assessment

```yaml
# What the email gateway caught vs missed
gateway_assessment:
  caught:
    - action: "{{what was blocked/quarantined}}"
      mechanism: "{{which gateway feature caught it — SPF check, URL filter, sandbox, etc.}}"
  missed:
    - action: "{{what was NOT caught — email delivered to inbox}}"
      gap: "{{why it was missed — authentication passed, URL not in block list, new domain, etc.}}"
      
  # Gateway effectiveness score
  effectiveness: "{{emails_blocked}} of {{total_emails}} blocked ({{%}}) — {{assessment}}"
```

#### B. SOC Detection Assessment

```yaml
# What the SOC detected vs missed
soc_assessment:
  detection_source: "{{how was the phishing discovered — user report, gateway alert, automated detection, threat intel feed}}"
  time_to_detection: "{{time from delivery to first detection/report}}"
  detection_gaps:
    - gap: "{{what should have been detected but wasn't}}"
      root_cause: "{{why — missing rule, missing log source, rule logic flaw}}"
      fix: "{{proposed detection improvement}}"
```

#### C. Red Team Testing Recommendations

```yaml
# Red Team should test these scenarios
red_team_tests:
  # Test 1: Can Red Team reproduce this campaign?
  - test_id: PT-{{incident_id}}-01
    description: "Reproduce the phishing campaign technique against the organization"
    technique: "{{T1566.00X}} — {{technique_name}}"
    scenario: |
      Send a phishing email using the same technique ({{payload_type}}) but with 
      different IOCs (new domain, new sender, new payload hash) to test whether 
      the organization's defenses detect the TECHNIQUE, not just the IOCs.
    expected_result: "Email gateway should detect/block based on behavioral analysis, not IOC matching"
    priority: high

  # Test 2: Test authentication bypass
  - test_id: PT-{{incident_id}}-02
    description: "Test email authentication enforcement"
    technique: "SPF/DKIM/DMARC bypass"
    scenario: |
      Send emails with various authentication failure modes:
      - SPF fail with valid DKIM (should DMARC pass or fail?)
      - DKIM fail with SPF pass (alignment test)
      - Display name spoofing with valid authentication from lookalike domain
      - Subdomain spoofing ({{brand}}.attacker.com)
    expected_result: "Gateway should enforce DMARC policy and flag display name spoofing"
    priority: high

  # Test 3: Test payload detection
  - test_id: PT-{{incident_id}}-03
    description: "Test payload detection with evasion variants"
    technique: "{{payload_technique}}"
    scenario: |
      Deliver similar payload using evasion techniques:
      {{if credential_harvester: "- Different credential harvesting page template
      - HTTPS with valid certificate on newly registered domain
      - URL shortener / redirect chain to evade URL inspection"}}
      {{if malware_dropper: "- Modified attachment to evade hash-based detection
      - Password-protected archive delivery
      - ISO/VHD/IMG container to bypass Mark of the Web
      - Macro obfuscation variants (VBA stomping, XLM macros, document templates)"}}
    expected_result: "Detection should trigger on behavioral pattern, not just IOC match"
    priority: high

  # Test 4: Test detection gaps identified in this investigation
  - test_id: PT-{{incident_id}}-04
    description: "Exploit specific detection gaps found in this investigation"
    gaps:
      {{for each gap from soc_assessment.detection_gaps:}}
      - gap: "{{gap_description}}"
        exploit: "{{how Red Team should exploit this gap}}"
        expected_result: "{{what detection SHOULD trigger after gap is fixed}}"
    priority: medium
```

#### D. Evasion Variants to Test

```yaml
# Evasion variants for Red Team to test
evasion_variants:
  email_evasion:
    - variant: "Homoglyph domain — {{lookalike_domain}}"
      test: "Register domain with Cyrillic/Unicode lookalike characters"
    - variant: "Subdomain abuse — {{brand}}.attacker-domain.com"
      test: "Use legitimate brand as subdomain of attacker-controlled domain"
    - variant: "Compromised account relay"
      test: "Send phishing from a compromised legitimate email account (bypasses SPF/DKIM/DMARC)"
    - variant: "Reply chain hijacking"
      test: "Inject phishing into an existing email thread (QakBot/Emotet technique)"
      
  payload_evasion:
    - variant: "HTML smuggling"
      test: "Deliver payload via JavaScript-assembled blob in HTML email"
    - variant: "QR code phishing"
      test: "Replace URL with QR code — bypasses URL inspection"
    - variant: "OneNote/PDF lure"
      test: "Embed payload in non-macro-enabled format"
    - variant: "Cloud storage link"
      test: "Host payload on legitimate cloud service (SharePoint, OneDrive, Google Drive)"
```

### 5. Detection Improvement Summary

Present the complete detection improvement package:

"**Detection & Prevention Improvements — {{incident_id}}**

**Email Gateway Rules:** {{count}} rules recommended
- Sender/domain blocks: {{count}}
- Attachment rules: {{count}}
- URL rules: {{count}}
- Authentication enforcement: {{count}} recommendations

**Detection Rules Created:** {{count}}
- Sigma rules: {{count}} (IOC-based: {{count}}, behavioral: {{count}})
- YARA rules: {{count}}
- Suricata rules: {{count}}
- Rule output location: `{soc_detection_rules}/`

**User Communications:** {{count}} templates created
- User notification (Tier 1-2 recipients)
- Security awareness reminder
- IT/Helpdesk brief
- Executive notification (if severity warrants)

**Purple Team Feedback:** {{count}} test items
- Gateway effectiveness assessment
- SOC detection gap analysis
- Red Team test scenarios: {{count}}
- Evasion variants to test: {{count}}"

### 6. Present MENU OPTIONS

"**Select an option:**
[A] Advanced Elicitation — Deep-dive into specific detection rules, challenge rule logic, identify additional detection gaps
[W] War Room — Red vs Blue discussion on detection effectiveness — how would the attacker evade these new rules? Are there detection gaps we haven't addressed?
[C] Continue — Proceed to Reporting & Closure (Step 8 of 8 — Final Step)"

#### Menu Handling Logic:

- IF A: Deep-dive detection analysis — review specific rule logic for gaps, challenge false positive assessments, identify additional detection scenarios not covered, explore whether behavioral rules are sufficient or need refinement, examine whether user communications are appropriate for the audience. Process insights, ask user if they want to update, if yes update then redisplay menu, if no redisplay menu
- IF W: War Room discussion — Red Team perspective: which of these new detection rules can I bypass? What evasion techniques would I use against the email gateway improvements? How quickly can I adapt my phishing campaign to evade these signatures? Blue Team perspective: are our detection rules durable or will they need constant updating? Is our DMARC enforcement adequate? Do we have the right logging and visibility to detect the next variant of this campaign? Summarize insights, redisplay menu
- IF C: Update output file frontmatter adding this step name to the end of stepsCompleted array and updating `detection_rules_created`, `purple_team_items`, then read fully and follow: ./step-08-reporting.md
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted and detection_rules_created, purple_team_items updated, and detection improvements appended to report under `## Detection & Prevention` and Purple Team feedback appended under `## Purple Team Feedback`], will you then read fully and follow: `./step-08-reporting.md` to begin reporting and closure.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Email gateway rules created covering sender, domain, attachment, URL, and authentication layers
- Each gateway rule includes scope, FP assessment, and implementation guidance
- Authentication enforcement recommendations include phased DMARC rollout guidance
- Formal detection rules created (Sigma, YARA, Suricata) with description, logic, ATT&CK mapping, test case, and FP assessment
- Rules target both IOCs (short-term) and behaviors (durable detection)
- Detection rules saved to appropriate output directories
- User communication templates created for all audience levels (users, helpdesk, executives)
- Purple Team feedback includes: gateway assessment, SOC detection gaps, Red Team test scenarios, evasion variants
- Purple Team tests are specific and actionable (not vague "test phishing detection")
- Detection improvements appended to report under `## Detection & Prevention`
- Purple Team feedback appended under `## Purple Team Feedback`
- Frontmatter updated with detection_rules_created, purple_team_items and step added to stepsCompleted
- Menu presented and user input handled correctly

### SYSTEM FAILURE:

- Creating detection rules without test cases or FP assessments
- Creating only IOC-based rules without behavioral rules (IOCs rotate, behaviors persist)
- Deploying rules to production instead of recommending them
- Not creating DMARC enforcement recommendations when authentication gaps were identified
- Not providing user communication templates
- Purple Team feedback without specific Red Team test scenarios
- Skipping evasion variant analysis
- Detection rules that don't reference ATT&CK techniques
- Awareness communications that cause panic or are too technical for end users
- Beginning reporting or closure activities during detection improvement
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with detection and Purple Team metrics

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Detection rules must be both IOC-based (immediate) and behavioral (durable). Purple Team feedback closes the Red-Blue loop.
