# Step 10: Reporting & Case Closure

**Progress: Step 10 of 10** — FINAL STEP

## STEP GOAL:

Complete the forensic investigation by validating report completeness, writing the executive summary for non-technical audiences, computing forensic metrics, performing a final chain of custody audit, establishing the evidence disposition plan, and formally closing the case. This is the capstone step — the investigation is only complete when the report is finalized, the evidence is secured, and the case is formally closed.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER finalize a report with incomplete sections — every section must be populated or explicitly marked N/A with reason
- 📖 CRITICAL: Read the complete step file before taking any action
- 📋 YOU ARE A DIGITAL FORENSIC ANALYST completing a court-admissible forensic report
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are a Digital Forensic Analyst finalizing a forensic investigation report under ISO 27037 and NIST SP 800-86
- ✅ The report IS the deliverable — a thorough investigation is worthless without a thorough report
- ✅ The executive summary must be understandable by non-technical readers (legal, executive, regulatory) while accurately representing the technical findings
- ✅ The chain of custody final audit is the last integrity check — it must confirm that every evidence item's chain of custody is complete and unbroken from receipt through analysis to storage
- ✅ Evidence disposition is a legal obligation — evidence under litigation hold cannot be destroyed; evidence without a hold must have a documented retention period and destruction plan

### Step-Specific Rules:

- 🎯 Focus exclusively on report validation, executive summary, metrics, chain of custody audit, evidence disposition, and case closure
- 🚫 FORBIDDEN to perform new analysis — all analysis is complete as of step 9
- 🚫 FORBIDDEN to modify evidence or chain of custody records — this is a read-only audit
- 💬 Approach: Systematic validation of every report section, then synthesis into executive summary
- 📊 Forensic metrics must be computed from actual investigation data, not estimated
- 🔒 Final chain of custody verification: re-hash all evidence items and confirm chain integrity

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Finalizing a report with sections marked as "to be completed" undermines the credibility of the entire report — a partially complete report suggests an incomplete investigation, and any reader (especially opposing counsel) will focus on what is missing rather than what is present
  - Not performing a final chain of custody audit before case closure means the investigation cannot be re-opened without re-verifying every evidence item — if a question arises about evidence integrity months later, the last verified state should be at case closure, not at the last individual analysis step
  - Destroying evidence without confirming litigation hold status risks sanctions and adverse inference — evidence destruction after a litigation hold has been issued (or should have been issued) is spoliation, which carries severe legal consequences including default judgment in some jurisdictions
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Validate every report section before finalizing
- 📋 Compute forensic metrics from actual investigation data
- 🔒 Perform final chain of custody audit — re-verify all evidence integrity
- ⚠️ Present final navigation menu after case closure
- 💾 Save finalized report to output file
- 📖 Update frontmatter with final status and this step added to stepsCompleted
- This is the FINAL step — no next step file to load

## CONTEXT BOUNDARIES:

- Available context: Complete forensic report from steps 1-9, all evidence items, chain of custody records
- Focus: Report validation, executive summary, metrics, chain of custody audit, evidence disposition, case closure
- Limits: Read-only — no new analysis, no evidence modification
- Dependencies: All previous steps completed

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Report Completeness Validation

Systematically validate that every section of the forensic report is populated:

**Section Validation Checklist:**

```
| Section | Status | Populated By | Notes |
|---------|--------|-------------|-------|
| Case Summary | ✅/❌/N-A | Step 1 | |
| Case Identification | ✅/❌/N-A | Step 1 | |
| Legal Context & Authority | ✅/❌/N-A | Step 1 | |
| Forensic Question | ✅/❌/N-A | Step 1 | |
| Scope Definition | ✅/❌/N-A | Step 1 | |
| Evidence Inventory & Chain of Custody | ✅/❌/N-A | Steps 1-2 | |
| Acquisition & Preservation | ✅/❌/N-A | Step 2 | |
| Disk Forensics | ✅/❌/N-A | Step 3 | |
| Memory Forensics | ✅/❌/N-A | Step 4 | |
| Network Forensics | ✅/❌/N-A | Step 5 | |
| Cloud Forensics | ✅/❌/N-A | Step 6 | |
| Timeline Reconstruction | ✅/❌/N-A | Step 7 | |
| Findings & Artifacts | ✅/❌/N-A | Step 8 | |
| IOC Summary | ✅/❌/N-A | Step 8 | |
| Expert Opinion | ✅/❌/N-A | Step 9 | |
| Legal Considerations | ✅/❌/N-A | Step 9 | |
| Recommendations | ✅/❌/N-A | Step 9 | |
| Executive Summary | ❌ (this step) | Step 10 | |
| Forensic Metrics | ❌ (this step) | Step 10 | |
| Appendices | ❌ (this step) | Step 10 | |
```

For any section marked N/A: verify that the N/A status is documented with a reason (e.g., "Memory Forensics — N/A: No memory dumps acquired for this case. Reason: all systems were powered off before investigation began.")

For any section marked ❌: this indicates an incomplete investigation. Flag to the operator:

"**Report Completeness Warning:** The following sections are incomplete:
- {{list of incomplete sections}}

This affects the report's credibility and completeness. Options:
1. Return to the relevant step to complete the section
2. Document the section as incomplete with a reason (investigation constraint, evidence limitation, time constraint)
3. Accept the report as-is with the incomplete sections noted"

### 2. Executive Summary

Write the executive summary for non-technical audiences. This section must be understandable by legal counsel, executives, board members, and regulators who may not have technical expertise.

**Investigation Overview (Non-Technical):**

"Between {{investigation_start}} and {{investigation_end}}, a digital forensic investigation was conducted in response to {{case_classification_description}}. The investigation examined {{evidence_item_count}} items of digital evidence from {{system_count}} systems, spanning {{timeline_duration}}.

The investigation was conducted under engagement {{engagement_id}} with authorization for forensic examination of the identified systems. {{Legal context summary — e.g., 'This investigation supports an active incident response' or 'This investigation was conducted under attorney-client privilege in support of pending litigation.'}}"

**Key Findings:**

"The investigation identified {{findings_count}} findings ({{critical}} critical, {{high}} high, {{medium}} medium):

1. **{{most_critical_finding_title}}**: {{one-sentence non-technical description}}
2. **{{second_finding_title}}**: {{one-sentence non-technical description}}
3. **{{third_finding_title}}**: {{one-sentence non-technical description}}
{{additional key findings as appropriate}}

**Answer to the Forensic Question:**
{{direct answer in non-technical language}}"

**Business Impact:**

"The investigation determined that:
- {{scope_summary — N systems, M accounts, data types at risk}}
- {{exfiltration_status — data was/was not/may have been removed from the organization}}
- {{operational_impact — impact on business operations}}
- {{regulatory_impact — frameworks triggered, notification requirements}}"

**Risk Assessment:**

"Based on the investigation findings:
- **Current risk level**: {{High/Medium/Low}} — {{justification}}
- **Residual risk after recommended actions**: {{High/Medium/Low}} — {{justification}}
- **Ongoing exposure**: {{description of any continuing risk}}"

**Recommended Actions (Non-Technical):**

"The investigation recommends the following priority actions:
1. **Immediate (0-72 hours)**: {{action summary}}
2. **Short-term (30 days)**: {{action summary}}
3. **Long-term (90 days)**: {{action summary}}

{{Regulatory notification requirements if applicable}}"

### 3. Forensic Metrics

Compute metrics from actual investigation data:

```
| Metric | Value |
|--------|-------|
| Case ID | {{case_id}} |
| Case Classification | {{classification}} |
| Investigation Start | {{start_timestamp}} |
| Investigation End | {{end_timestamp}} |
| Total Investigation Duration | {{duration}} |
| Evidence Items Received | {{received_count}} |
| Evidence Items Acquired | {{acquired_count}} |
| Evidence Items Analyzed | {{analyzed_count}} |
| Total Evidence Size | {{total_size}} |
| Artifacts Recovered | {{artifact_count}} |
| IOCs Extracted | {{ioc_count}} |
| Timeline Entries | {{timeline_count}} |
| Timeline Span | {{earliest}} to {{latest}} ({{duration}}) |
| Dwell Time | {{dwell_time}} |
| Findings (Total) | {{total}} |
| Findings (Critical) | {{critical}} |
| Findings (High) | {{high}} |
| Findings (Medium) | {{medium}} |
| Findings (Low) | {{low}} |
| Findings (Informational) | {{informational}} |
| ATT&CK Techniques Identified | {{technique_count}} |
| ATT&CK Tactics Covered | {{tactic_count}} / 14 |
| Systems Compromised (Confirmed) | {{confirmed_systems}} |
| Systems Compromised (Suspected) | {{suspected_systems}} |
| Accounts Compromised (Confirmed) | {{confirmed_accounts}} |
| Accounts Compromised (Suspected) | {{suspected_accounts}} |
| Data Exfiltration | {{confirmed/suspected/not detected}} |
| Anti-Forensics Detected | {{yes/no — types}} |
| Chain of Custody Status | {{intact/broken}} |
| Expert Opinion Confidence | {{confidence_level}} |
| Analysis Duration (Disk) | {{duration or N/A}} |
| Analysis Duration (Memory) | {{duration or N/A}} |
| Analysis Duration (Network) | {{duration or N/A}} |
| Analysis Duration (Cloud) | {{duration or N/A}} |
| Analysis Duration (Timeline) | {{duration}} |
```

### 4. Chain of Custody Final Audit

Perform the final integrity verification for all evidence items:

**Final Hash Verification:**

```
| EVD ID | Description | Master Hash (SHA-256) | Current Hash (SHA-256) | Match | Working Copy Hash | WC Match | Status |
|--------|-------------|----------------------|------------------------|-------|-------------------|----------|--------|
| EVD-{case_id}-001 | {{desc}} | {{master_hash}} | {{current_hash}} | ✅/❌ | {{wc_hash}} | ✅/❌ | {{Intact/ALERT}} |
```

**Chain of Custody Audit:**

```
| EVD ID | CoC Entries | All Transfers Documented | All Hashes Verified | Current Custodian | Storage Location | CoC Status |
|--------|-------------|-------------------------|---------------------|-------------------|------------------|------------|
| EVD-{case_id}-001 | {{count}} | ✅/❌ | ✅/❌ | {{custodian}} | {{location}} | {{Intact/Broken — detail}} |
```

**Final Audit Summary:**
```
Total evidence items: {{count}}
Chain of custody intact: {{count}} / {{total}}
Chain of custody broken: {{count}} — {{detail}}
All master hashes verified: {{yes / no — detail}}
All working copies verified: {{yes / no — detail}}
Evidence custodian: {{name, role}}
Evidence storage location: {{location}}
Encryption at rest: {{yes / no}}
Access logging enabled: {{yes / no}}
```

### 5. Evidence Disposition Plan

For each evidence item, determine the disposition:

**Disposition Categories:**
- **Retain (Litigation Hold)**: Evidence under active or anticipated legal proceedings — no destruction permitted
- **Retain (Regulatory)**: Evidence required for regulatory compliance — retain per regulatory timeframe
- **Retain (Case Policy)**: Evidence retained per organizational policy — retain per policy period
- **Return**: Evidence to be returned to the evidence owner/source
- **Destroy**: Evidence approved for secure destruction after retention period

```
| EVD ID | Description | Disposition | Basis | Retention Period | Retention Until | Destruction Method | Approved By |
|--------|-------------|-------------|-------|------------------|-----------------|-------------------|-------------|
| EVD-{case_id}-001 | {{desc}} | Retain/Return/Destroy | {{basis}} | {{period}} | {{date}} | {{method or N/A}} | {{approver}} |
```

**Disposition Notes:**
- Evidence under litigation hold: hold release must be explicitly confirmed by legal counsel before any disposition
- Evidence to be destroyed: use certified secure deletion (NIST SP 800-88 guidelines)
  - For digital media: overwrite (3+ passes), degauss, or physical destruction
  - For physical media: degauss and shred, or incineration
  - Document destruction: date, method, witness, certificate of destruction
- Evidence to be returned: document the return transfer in the chain of custody

### 6. Finalize Report

#### A. Populate Remaining Sections

Complete the remaining sections in the output file `{outputFile}`:

```markdown
## Executive Summary

### Investigation Overview (Non-Technical)
{{executive_overview}}

### Key Findings
{{key_findings_non_technical}}

### Business Impact
{{business_impact}}

### Risk Assessment
{{risk_assessment}}

### Recommended Actions
{{recommended_actions_non_technical}}

## Forensic Metrics
{{metrics_table}}

## Appendices

### Appendix A: Complete Evidence Index
{{evidence_inventory_with_hashes}}

### Appendix B: Full Chain of Custody Records
{{per_item_coc_records}}

### Appendix C: Complete IOC Feed (Machine-Readable)
{{ioc_list_in_machine_readable_format — STIX/CSV/JSON}}

### Appendix D: Tool Inventory & Versions
{{all_tools_used_with_versions_and_hashes}}

### Appendix E: Full YARA Rules
{{yara_rules_developed_or_used}}

### Appendix F: Forensic Image Verification Hashes
{{all_image_hashes}}

### Appendix G: Glossary of Forensic Terms
{{glossary_of_terms_used_in_report}}

### Appendix H: Regulatory Notification Records
{{notification_records_if_applicable}}

### Appendix I: Evidence Disposition Plan
{{disposition_plan}}
```

#### B. Update Frontmatter (Final)

Update frontmatter with final values:
- Add this step name (`Reporting & Case Closure`) to the end of `stepsCompleted`
- Set `case_status` to `'closed'`
- Verify ALL frontmatter fields are populated with final values:
  - `case_id`, `case_name`, `case_classification`, `legal_context`
  - `evidence_item_count`, `chain_of_custody_entries`, `integrity_verified`
  - `evidence_types`, `analysis_types`
  - `timeline_entries`, `artifacts_recovered`, `iocs_extracted`
  - `findings_count`, `findings_by_severity`
  - `expert_opinion_rendered`, `expert_opinion_confidence`
  - `root_cause`, `attack_vector`, `dwell_time`
  - `lateral_movement_detected`, `data_exfiltration_detected`
  - `persistence_mechanisms`, `anti_forensics_detected`

### 7. Present Case Closure Summary

"**Digital Forensic Investigation Complete**

{{user_name}}, the forensic investigation for case `{{case_id}}` is now complete.

**Case:** {{case_name}} (`{{case_id}}`)
**Classification:** {{case_classification}}
**Investigation Period:** {{start_date}} — {{end_date}} ({{duration}})

**Investigation Summary:**
- Evidence items: {{evidence_count}} received, {{acquired_count}} acquired, {{analyzed_count}} analyzed
- Total evidence size: {{total_size}}
- Timeline: {{timeline_entries}} events spanning {{timeline_span}}
- Dwell time: {{dwell_time}}
- Findings: {{findings_count}} ({{critical}} critical, {{high}} high, {{medium}} medium)
- IOCs: {{ioc_count}} unique indicators
- ATT&CK coverage: {{technique_count}} techniques across {{tactic_count}} tactics
- Scope: {{system_count}} systems, {{account_count}} accounts compromised
- Data exfiltration: {{exfil_status}}
- Expert opinion: rendered with {{confidence}} confidence

**Chain of Custody:** {{intact/broken}}
**Evidence Disposition:** Plan established for all {{evidence_count}} items
**Regulatory Notifications:** {{notification_status}}

**Report Location:** `{outputFile}`

**Forensic Question Answer:** {{one_sentence_answer}}

**Root Cause:** {{root_cause_one_liner}}

The forensic report is ready for delivery to the authorized recipients per the engagement terms."

### 8. Present FINAL NAVIGATION

"**Case `{{case_id}}` is closed. What would you like to do next?**

[W] War Room — Final adversarial review of the complete forensic investigation
[N] New Case — Start a new forensic investigation within the same engagement (`spectra-digital-forensics`)
[S] IRT Handoff — Transfer findings to incident handling for containment/eradication/recovery (`spectra-incident-handling`)
[D] Detection Engineering — Create detection rules based on IOCs and ATT&CK techniques found (`spectra-detection-lifecycle`)
[P] Purple Team — Run adversary simulation based on the attack chain to validate detection coverage
[I] Incident Handling Escalation — Escalate to full incident handling if not already initiated (`spectra-incident-handling`)"

#### Menu Handling Logic:

- IF W: Final War Room — comprehensive adversarial review of the entire investigation. Red Team reviews the report as if they were the attacker: is the timeline accurate? Did the analyst find everything? Are the conclusions correct? Blue Team reviews as the defense: is the report legally defensible? Are all findings evidenced? Are the recommendations actionable? Would this report survive independent peer review? Present findings, discuss with operator.
- IF N: Inform the operator that a new case can be initiated by running `spectra-digital-forensics` within the same engagement.
- IF S: Recommend `spectra-incident-handling` with a summary of key findings, IOCs, affected systems, and immediate actions for the incident handler.
- IF D: Recommend `spectra-detection-lifecycle` with the IOC feed, ATT&CK techniques, and behavioral indicators for detection rule creation.
- IF P: Recommend purple team engagement to validate detection coverage against the attack chain identified in this investigation.
- IF I: Recommend `spectra-incident-handling` for cases where the forensic investigation identified an active or unresolved incident requiring full incident response lifecycle management.
- IF user asks questions: Answer and present navigation again.

## CRITICAL STEP COMPLETION NOTE

This is the FINAL step. The case is closed when:
1. All report sections validated as complete or documented as N/A
2. Executive summary written for non-technical audience
3. Forensic metrics computed from actual investigation data
4. Chain of custody final audit completed with all evidence verified
5. Evidence disposition plan established
6. Frontmatter updated with `case_status: 'closed'` and this step added to `stepsCompleted`
7. Case closure summary presented to operator

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Report completeness validation performed for every section
- Executive summary written in non-technical language suitable for legal/executive/regulatory audiences
- Forensic question directly answered in executive summary
- Forensic metrics computed from actual investigation data (not estimated)
- Chain of custody final audit completed with all evidence items re-hashed and verified
- Evidence disposition plan established for every evidence item with retention basis and timeline
- Appendices populated with evidence index, CoC records, IOC feed, tool inventory, YARA rules, image hashes
- Report marked as complete with `case_status: 'closed'` in frontmatter
- All frontmatter fields populated with final values
- Case closure summary presented to operator with key metrics and forensic question answer
- Final navigation options presented for downstream workflows

### ❌ SYSTEM FAILURE:

- Finalizing report with incomplete or empty sections without N/A documentation
- Executive summary using technical jargon inappropriate for non-technical audience
- Not computing forensic metrics from actual data
- Not performing final chain of custody audit (last integrity check before case closure)
- Not establishing evidence disposition plan (evidence in legal/regulatory limbo)
- Not answering the forensic question in the executive summary
- Marking case as closed without operator acknowledgment
- Destroying evidence without confirming litigation hold status
- Not populating appendices with supporting data
- Performing new analysis during this step

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. This is the final step. The report is the deliverable. Every section must be complete or documented. The executive summary must be accessible. The chain of custody must verify. The evidence must be secured. The case is closed only when everything is in order.
