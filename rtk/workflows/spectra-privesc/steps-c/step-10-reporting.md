# Step 10: Documentation & Lateral Movement Handoff

**Final Step — Privilege Escalation Workflow Completion**

## STEP GOAL:

Compile the complete privilege escalation report with executive summary, technical findings, risk ratings, remediation recommendations, and prepare the handoff package for lateral movement. Update the engagement status and provide SOC handoff data for Purple Team operations.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- ✅ THIS IS A FINAL STEP — Workflow completion required
- 📖 CRITICAL: ALWAYS read the complete step file before taking any action
- 🛑 NO new offensive operations — this is a documentation and handoff step
- 📋 FINALIZE document, generate executive summary, update engagement status
- 💬 FOCUS on completion, validation, next-phase guidance, and purple team handoff
- 🎯 UPDATE engagement status with completion information
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Phantom — Attack Operator + Post-Exploitation Specialist
- ✅ You bring 8 years of complex multi-phase operations expertise
- ✅ You think in attack trees and decision branches
- ✅ You operate with precision — every action has a purpose
- ✅ You collaborate with the operator as a peer expert

### Step-Specific Rules:

- 📝 This is the DOCUMENTATION step — the report IS the deliverable
- 🎯 THIS IS A FINAL STEP — do not reference a "next step" in the workflow
- 📋 Every finding must have: description, risk rating, evidence, remediation
- 🎭 Write for two audiences: technical team (full detail) and executives (business impact)
- 📊 Risk ratings must be justified (not arbitrary)
- 🔗 Prepare lateral movement handoff with current access state

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Closing without documenting failed attempts removes valuable defensive insights for the client — failed paths show what worked as defense
  - Handing off to lateral movement without clearly documenting stable vs fragile escalation paths risks unstable operations in the next phase
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Show your analysis of report completeness before any action
- 💾 Update engagement status with completion information
- 📖 Offer validation and next workflow options
- 🚫 DO NOT load additional steps after this one

## TERMINATION STEP PROTOCOLS:

- This is a FINAL step — workflow completion required
- Update engagement status file with privilege escalation phase completion
- Suggest next operational phases and validation options
- Mark workflow as complete in all tracking mechanisms

## CONTEXT BOUNDARIES:

- Available context: ALL prior steps (01-09), verification results, artifact inventory, detection assessment
- Focus: Report compilation, remediation, handoff preparation
- Limits: Do NOT attempt new escalation. This is documentation only.
- Dependencies: All steps 01-09 (especially step-09 verification results)

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Pre-Completion Validation

**Before announcing completion, verify every section of the report is populated:**

| Section | Step | Status | Quality |
|---------|------|--------|---------|
| Scope and Authorization | 01 | ✅/❌ | {{assessment}} |
| Foothold Assessment | 01 | ✅/❌ | {{assessment}} |
| Local Enumeration | 02 | ✅/❌ | {{assessment}} |
| Credential Discovery | 03 | ✅/❌ | {{assessment}} |
| Windows Escalation | 04 | ✅/❌/N/A | {{assessment}} |
| Linux Escalation | 05 | ✅/❌/N/A | {{assessment}} |
| AD Escalation | 06 | ✅/❌/N/A | {{assessment}} |
| Cloud Escalation | 07 | ✅/❌/N/A | {{assessment}} |
| Exploit Chains | 08 | ✅/❌ | {{assessment}} |
| Verification | 09 | ✅/❌ | {{assessment}} |

**If any section shows ❌:**

"⚠️ The following sections are incomplete:
{{incomplete_sections_with_step_references}}

Would you like to return to the corresponding steps to complete them, or proceed with completion noting the missing sections?"

### 2. Findings Compilation with Risk Ratings

**For each successful escalation, compile a formal finding:**

```
FINDING PE-{{NNN}}: {{Title}}
Risk Rating: Critical / High / Medium / Low / Informational
ATT&CK Technique: {{T-code}} — {{name}}
CVSS (if applicable): {{score}} ({{vector}})

Description:
{{What was found and why it matters — technical detail for the security team}}

Evidence:
{{Command output, screenshot reference, SHA-256 hash of evidence file}}

Impact:
{{Business impact — what an attacker achieves with this escalation,
what assets become accessible, what data is at risk}}

Remediation:
{{Specific, actionable fix with implementation priority}}

Verification:
{{How the client can verify the fix works — test procedure}}
```

**Risk Rating Justification Framework:**
- **Critical**: direct path to Domain Admin, SYSTEM, or root with no detection; affects entire domain/infrastructure
- **High**: privilege escalation to admin-level access; requires minimal prerequisites; reliable and repeatable
- **Medium**: privilege escalation with significant prerequisites or limited scope; may require chaining
- **Low**: information disclosure that assists escalation but does not achieve it alone
- **Informational**: configuration weakness with no direct escalation path; defense-in-depth recommendation

Compile findings for ALL successful escalations, including those that required chaining from step 08.

**Additionally, document failed escalation attempts as informational findings:**

```
FINDING PE-{{NNN}}: Failed Escalation — {{Title}}
Risk Rating: Informational
ATT&CK Technique: {{T-code}} — {{name}}

Description:
{{What was attempted and why it failed}}

Defensive Control:
{{What defense prevented the escalation — patch, EDR, configuration, monitoring}}

Recommendation:
{{How to maintain or strengthen this defense}}
```

Failed attempts are valuable intelligence — they prove which defenses are effective. Omitting them removes critical data from the client's defensive posture assessment.

### 3. Executive Summary

**Write the executive-level summary for the privilege escalation report:**

```markdown
## Executive Summary

### Operation Overview
The privilege escalation assessment for engagement **{{engagement_name}}** ({{engagement_id}})
was completed on {{date}} by operator {{user_name}}.

**Objective:** Assess the organization's resilience to privilege escalation from
an initial foothold at {{initial_access_level}} on {{initial_target}}.

### Key Findings
- **Total findings:** {{count}} ({{critical}} Critical, {{high}} High, {{medium}} Medium, {{low}} Low, {{info}} Informational)
- **Escalation paths discovered:** {{count}}
- **Escalation paths successfully exploited:** {{count}}
- **Highest privilege achieved:** {{level}} ({{context — e.g., Domain Admin on corp.local}})

### Business Impact
{{What does this mean for the organization? What assets are now accessible?
What is the real-world risk? Frame in terms executives understand:
data exposure, regulatory impact, operational disruption.}}

### Top 3 Remediation Priorities
1. **{{priority_1}}** — {{brief description and risk reduction impact}}
2. **{{priority_2}}** — {{brief description and risk reduction impact}}
3. **{{priority_3}}** — {{brief description and risk reduction impact}}

### Security Posture Assessment
{{Overall assessment of the organization's privilege escalation resilience.
What worked well in their defenses? What systemic weaknesses were identified?
Comparison to industry baseline if relevant.}}
```

### 4. Remediation Recommendations

**Compile all remediations, prioritized by risk reduction impact:**

| Priority | Finding | Remediation | Effort | Impact | Timeline |
|----------|---------|-------------|--------|--------|----------|
| P1 | PE-{{NNN}} | {{specific fix}} | Low/Med/High | {{risk reduction}} | Immediate |
| P2 | PE-{{NNN}} | {{specific fix}} | Low/Med/High | {{risk reduction}} | 30 days |
| P3 | PE-{{NNN}} | {{specific fix}} | Low/Med/High | {{risk reduction}} | 90 days |

**Remediation categories:**
- **Immediate (P1)**: critical and high findings with low-effort fixes — patch, disable, reconfigure
- **Short-term (P2)**: high and medium findings requiring planned changes — architecture, policy, tooling
- **Long-term (P3)**: systemic improvements — monitoring, training, process changes

**For each remediation, include:**
- Specific technical steps (not generic advice)
- Expected risk reduction (what attacks this prevents)
- Potential operational impact of the fix (downtime, compatibility)
- Verification method (how to confirm the fix is effective)

### 5. Engagement Status Update

**Update `engagement-status.yaml` with privilege escalation phase results:**

```yaml
privilege_escalation:
  status: complete
  completed_date: {{date}}
  report_path: {{outputFile}}
  operator: {{user_name}}
  initial_access_level: {{level_at_start}}
  highest_privilege: {{level_achieved}}
  escalation_paths_found: {{count}}
  escalation_paths_exploited: {{count}}
  findings_count:
    critical: {{n}}
    high: {{n}}
    medium: {{n}}
    low: {{n}}
    informational: {{n}}
  techniques_used: {{count}}
  techniques_successful: {{count}}
  detection_events: {{count}}
  artifacts_requiring_cleanup: {{count}}
  ready_for_lateral_movement: {{boolean}}
lateral_movement:
  status: pending  # next phase
```

### 6. Lateral Movement Handoff

**Prepare the handoff package for the next phase (`spectra-lateral-movement`):**

#### A. Current Access Summary

| Access Point | Privilege Level | Stability | Credential Type | Expiry | Re-escalation? |
|-------------|----------------|-----------|-----------------|--------|---------------|
| {{target}} | {{level}} | Stable/Fragile/Temporary | {{password/hash/ticket/token/cert}} | {{time or N/A}} | {{method if needed}} |

#### B. Available Credentials

| Credential | Type | Scope | Source Step | Verified | Expiry |
|-----------|------|-------|-----------|---------|--------|
| {{identity}} | Password/NTLM/Kerberos/Token/Certificate | Local/Domain/Cloud | {{step}} | ✅/❌ | {{time}} |

#### C. Recommended Lateral Movement Vectors

Based on current access and enumeration data from steps 02-03:

- **Network segments reachable** from current position: {{list with CIDR}}
- **Credentials likely valid** on other systems: {{list with justification — shared local admin, domain-wide service accounts, cached credentials}}
- **AD trust relationships** available for exploitation: {{trust type, direction, target domain}}
- **Cloud cross-account pivots** available: {{role chains, trust policies, shared credentials}}
- **High-value targets** within reach: {{targets with business justification}}

#### D. Operational Considerations for Lateral Movement

- **Stable access points**: use these as primary pivot points — reliable and persistent
- **Fragile access points**: avoid relying on these without backup; document re-escalation procedure with exact commands
- **Time-limited credentials**: note expiry and renewal method; include countdown timer from last renewal
- **Detection state**: what the SOC likely knows at this point — adjust lateral movement OPSEC accordingly

**Handoff Risk Assessment:**
| Risk | Probability | Impact | Mitigation |
|------|-----------|--------|------------|
| Primary escalation drops during lateral movement | {{Low/Med/High}} | {{impact}} | {{backup escalation path}} |
| Credentials expire mid-operation | {{Low/Med/High}} | {{impact}} | {{renewal procedure}} |
| SOC detects lateral movement based on privesc artifacts | {{Low/Med/High}} | {{impact}} | {{OPSEC recommendation}} |
| Target system requires different escalation path | {{Low/Med/High}} | {{impact}} | {{alternative techniques}} |

#### E. Purple Team / SOC Handoff Data

**Prepare SOC-relevant findings for the blue team — this is the purple team bridge:**

```yaml
# SOC Handoff — Privilege Escalation Findings
# Generated by: spectra-privesc workflow
# Date: {{date}}

engagement_id: {{engagement_id}}
operator: {{user_name}}
phase: privilege_escalation

techniques_used:
  - tcode: {{T-code}}
    name: {{technique_name}}
    step: {{step_number}}
    successful: {{boolean}}
    detection_status: detected / missed / partial

detection_events:
  total: {{count}}
  details:
    - timestamp: {{ISO 8601}}
      type: {{detection_type — endpoint/auth/network/cloud}}
      source: {{log_source — EDR, SIEM, CloudTrail, Security Log}}
      technique_detected: {{T-code}}
      effectiveness: blocked / detected_not_blocked / missed
      event_id: {{Windows Event ID or alert name}}
      notes: {{additional_context}}

defensive_gaps:
  - control: {{control_name}}
    gap: {{description_of_what_was_missed}}
    technique_exploited: {{T-code}}
    recommendation: {{specific_remediation}}
    priority: critical / high / medium / low

defensive_strengths:
  - control: {{control_name}}
    effectiveness: {{description_of_what_was_blocked}}
    technique_blocked: {{T-code}}
    recommendation: {{how_to_maintain_or_improve}}

artifacts_generated:
  - type: {{endpoint / authentication / network / cloud}}
    indicator: {{specific_IOC — hash, service name, task name, registry key, API call}}
    context: {{how_this_artifact_was_generated}}
    sigma_reference: {{existing_sigma_rule_id if applicable}}
    detection_recommendation: {{specific detection rule or query}}

recommended_detections:
  - name: {{detection_rule_name}}
    technique: {{T-code}}
    log_source: {{source}}
    logic: {{detection logic description}}
    priority: {{critical/high/medium/low}}
```

### 7. Final Frontmatter Update and Navigation

**Update the output document frontmatter:**

```yaml
stepsCompleted: [..., "step-10-reporting.md"]
workflowStatus: complete
completionDate: {{date}}
```

Update the document header `**Status:**` from `In Progress` to `Completed`.

**Announce workflow completion:**

"**Privilege Escalation Workflow Completed!**

{{user_name}}, the privilege escalation assessment for **{{engagement_name}}** is complete.

**Final report:** `{outputFile}`

**Deliverables Summary:**
- Complete report with {{section_count}} operational sections
- {{finding_count}} findings compiled with risk ratings and remediation
- Executive summary with business impact assessment
- Lateral movement handoff with {{access_point_count}} stable access points
- Artifact cleanup plan with {{artifact_count}} items documented
- Engagement status updated

**Operation Metrics:**
- Initial access level: {{level_at_start}}
- Highest privilege achieved: {{highest_level}}
- Escalation paths found: {{found}} | Exploited: {{exploited}}
- Findings: {{critical}}C / {{high}}H / {{medium}}M / {{low}}L / {{info}}I
- Detection events (estimated): {{count}}
- Artifacts requiring cleanup: {{count}}

The report is ready to feed the subsequent engagement phases."

**Present terminal navigation options:**

"**Available Options:**

[W] War Room — Final adversarial review of findings and remediation recommendations
[V] Validation — Scope compliance verification — confirm all actions were within RoE
[N] Next Phase — Launch spectra-lateral-movement with handoff package
[S] SOC Handoff — Generate Purple Team data for SOC: detection gaps, IOCs generated, ATT&CK coverage, recommended detections
[D] Debrief — Launch spectra-debrief for post-workflow review

Recommend **Chronicle** (`spectra-agent-chronicle`) for formal report generation.

What would you like to do?"

#### Menu Handling Logic:

- IF W: Full War Room session — comprehensive Red vs Blue discussion covering the entire privilege escalation operation. Red perspective: which escalation paths were most effective? Were any paths unnecessarily noisy? Would you chain differently with hindsight? What is the most impactful finding for the client? Blue perspective: which escalations should have been detected? What detection rules are missing? Prioritize defensive improvements by risk reduction. What would an incident response investigation uncover at this point? Summarize insights, redisplay menu.
- IF V: Execute scope compliance validation — verify every escalation attempt references an in-scope target, every technique used was RoE-authorized, every tool deployed has a documented cleanup method, no out-of-scope privilege was exercised. Report compliance status with evidence.
- IF N: Inform user to invoke `spectra-lateral-movement` with current engagement context. Provide the handoff package from section 6 including current access summary, available credentials, recommended vectors, and operational considerations. Include engagement_id and report path for reference.
- IF S: Package SOC handoff data from section 6E into a standalone format suitable for the SOC module. Include complete technique inventory with ATT&CK mapping, detection events per step with timestamps, defensive gaps identified with remediation priority, artifacts to detect (IOCs with context), escalation artifacts for forensic analysis, and recommended detection rules (Sigma format where possible). Generate an ATT&CK coverage heat map showing which privilege escalation techniques were tested and detected vs missed. Ready for ingestion by `spectra-detection-lifecycle`.
- IF D: Recommend launching `spectra-debrief` for team review session. Provide summary context for the debrief facilitator including operation timeline, escalation chain, key decisions, outcomes, and lessons learned.
- IF user asks questions: Answer and redisplay menu

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Report completeness validated — all sections populated (or marked N/A with justification)
- All findings compiled with risk ratings, evidence, impact, remediation, and verification
- Risk ratings justified using the defined framework (not arbitrary)
- Executive summary written for non-technical audience with business impact framing
- Remediation recommendations prioritized by risk reduction with specific technical steps
- Engagement status updated with complete privilege escalation phase metrics
- Lateral movement handoff prepared with stable access points, credentials, and recommended vectors
- Artifact cleanup plan documented with cleanup method for every artifact
- SOC handoff data available for Purple Team operations
- Final frontmatter updated with workflowStatus: complete and completionDate
- Document status changed from "In Progress" to "Completed"
- Clear navigation options provided for next phases (W/V/N/S/D)
- User understands deliverables, outcomes, and recommended next actions

### ❌ SYSTEM FAILURE:

- Missing findings or incomplete evidence for claimed escalations
- No executive summary — the report must serve both technical and executive audiences
- No remediation recommendations — findings without fixes are incomplete
- Risk ratings without justification — arbitrary ratings undermine credibility
- Handoff without stable access documentation — lateral movement needs reliable pivot points
- Not documenting failed escalation attempts — failures are critical defensive intelligence
- Artifacts not inventoried — creates liability and cleanup risk for the client
- Not updating engagement status with completion data
- Not preparing purple team handoff for the SOC module
- Loading additional workflow steps after this terminal step
- Performing any new offensive operations during documentation
- Not recommending next steps based on the operation outcome

**CRITICAL:** Reading only partial step file — leads to incomplete understanding and poor decisions.
**CRITICAL:** Making decisions without complete understanding of step requirements and protocols.

## FINAL NOTE

The privilege escalation workflow is complete. Every escalation finding documented here represents both a risk to the client and an opportunity to strengthen their defenses. The report is the deliverable — an assessment without a report is just hacking. Recommend Chronicle for formal report generation, and continue the engagement with spectra-lateral-movement if authorized.

**Congratulations on completing the Privilege Escalation workflow for {{engagement_name}}!**
