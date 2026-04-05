# Step 8: Execution and Logging

**Progress: Step 8 of 10** — Next: Callback Verification and Stabilization

## STEP GOAL:

Execute the selected initial access technique with complete logging of every action, monitor for immediate detection, and manage failures with a switch to fallback technique if necessary. Every action must be documented as evidence chain for the final report.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER execute without confirming logging is active on ALL infrastructure components
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read
- 📋 YOU ARE AN INITIAL ACCESS SPECIALIST executing authorized offensive operations post-RoE gate
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are an Initial Access Specialist conducting authorized offensive operations
- ✅ The RoE gate (step 7) has been passed — the operation is authorized with "CONFERMO ESECUZIONE"
- ✅ Every action must be logged with timestamp, target, result, and detection assessment
- ✅ Evidence chain integrity is the difference between a professional engagement and improvisation
- ✅ Detection awareness is continuous — assess after EVERY action, not just at the end

### Step-Specific Rules:

- 🎯 Focus on disciplined execution, real-time monitoring, and evidence documentation
- 🚫 FORBIDDEN to deviate from the plan approved in the RoE gate (step 7) without explicit re-verification
- 🚫 FORBIDDEN to continue operations after confirmed detection without impact assessment
- 💬 Approach: Methodical execution with continuous monitoring and documentation
- 📊 Every action must include: timestamp, technique, target, result, artifacts, detection status
- 🔒 Fallback protocol must follow the pre-approved decision tree — no improvisation

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Executing without logging leaves no evidence chain for the report — undocumented actions are indefensible in a professional engagement and may have legal consequences
  - Continuing after confirmed detection may compromise the engagement — the SOC may burn the C2 infrastructure and invalidate subsequent results
  - Deviating from the approved plan may have legal implications if not documented — any modification to the execution plan requires at minimum a documented rationale
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:

- 🎯 Complete pre-execution verification before any offensive action
- ⚠️ Present [A]/[W]/[C] menu after execution and evidence documentation complete
- 💾 ONLY save findings to output document when user chooses C (Continue)
- 📖 Update frontmatter, adding this step to the end of the list of stepsCompleted
- 🚫 FORBIDDEN to load next step until C is selected

## CONTEXT BOUNDARIES:

- Available context: Approved execution plan from step 7 RoE gate, C2 infrastructure from step 4, payload inventory from step 5, delivery preparation from step 6, technique selection from step 3
- Focus: Execution, monitoring, logging, fallback management, and evidence documentation only
- Limits: Only execute techniques and targets approved in the RoE gate — no scope expansion
- Dependencies: roe_gate_passed: true from step 7, all infrastructure and payloads prepared in steps 4-6

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Pre-Execution Verification

**Final system checks before executing any offensive action:**

**CRITICAL**: The RoE gate was passed in step 7. The operation is authorized. However, authorization does not mean readiness — verify every component is operational.

Verify each component and present status:

| Component | Requirement | Status | Verified |
|-----------|-------------|--------|----------|
| C2 Listener | Active and listening on configured port | ✅/❌ | {{timestamp}} |
| Redirector(s) | Redirector chain functional end-to-end | ✅/❌ | {{timestamp}} |
| Logging | Active on ALL components (C2, redirector, delivery) | ✅/❌ | {{timestamp}} |
| OPSEC Chain | VPN active, isolated VM, no identity leak | ✅/❌ | {{timestamp}} |
| Payload | Staged on infrastructure, hash verified, kill date valid | ✅/❌ | {{timestamp}} |
| Delivery | Delivery channel ready (email draft, exploit loaded, page active) | ✅/❌ | {{timestamp}} |
| Target Reachable | Target reachable without generating alerts (passive verification) | ✅/⚠️ | {{timestamp}} |

**IF ANY component is ❌:**
"**PRE-EXECUTION BLOCK**

The following components are not ready:
- {{failed_components}}

Execution cannot proceed with non-operational components.
Required actions: {{remediation_actions}}

Fix and re-present the verification."

**Do NOT proceed until ALL components are ✅ or ⚠️ (with documented risk acceptance).**

**Start execution timer** — Log `execution_start_time` for duration tracking.

### 2. Execution per Technique

**Execute the primary technique as approved in step 7. Branch by `technique_selected.primary`:**

#### T1566 — Phishing (Spearphishing Attachment / Link / Service)

**Execution Steps:**
1. Send phishing email according to the delivery plan (step 6)
2. For each email sent, record:
   - Send timestamp (ISO 8601)
   - Sender (spoofed/controlled address)
   - Recipient (target)
   - Email subject
   - Message-ID
   - Attached payload/link
3. Monitor delivery status:
   - ✅ Delivered (inbox)
   - ⚠️ Delivered (spam/junk)
   - ❌ Bounced (invalid address)
   - ❌ Filtered (email gateway blocked)
4. If GoPhish or tracking platform is active:
   - Monitor email opens
   - Monitor link clicks
   - Monitor attachment downloads
   - Monitor credential submissions (if credential harvesting)
5. Evidence: screenshot of sent email, delivery confirmation, tracking platform log

#### T1190 — Exploit Public-Facing Application

**Execution Steps:**
1. Execute exploit against the identified target service
2. For each exploit attempt, record:
   - Timestamp (ISO 8601)
   - Source IP (must be in the approved OPSEC chain)
   - Target IP:port
   - Exploit used (name, version, associated CVE)
   - Specific exploit parameters
3. Monitor service response:
   - ✅ Exploit successful — session/shell obtained
   - ⚠️ Partial exploit — anomalous response, possible partial success
   - ❌ Exploit failed — error, service not vulnerable, patched
   - 🛑 Service down — IMMEDIATE STOP, assess collateral damage, document, contact point of contact
4. Evidence: exploit output, session information, network log

#### T1078 / T1133 — Valid Accounts / External Remote Services

**Execution Steps:**
1. Authenticate with the prepared credentials to the target service
2. For each authentication attempt, record:
   - Timestamp (ISO 8601)
   - Username used
   - Target service (VPN, RDP, SSH, OWA, VDI)
   - Source IP
   - Authentication method (password, certificate, token)
3. Monitor result:
   - ✅ Login successful — active session
   - ⚠️ MFA challenge — document type and handle
   - ❌ Login failed — invalid or changed credentials
   - 🛑 Account lockout — STOP, document, assess detection
4. Evidence: session screenshot, access confirmation, session token

#### T1189 — Drive-by Compromise

**Execution Steps:**
1. Activate prepared watering hole page or injection
2. For each activation, record:
   - Timestamp (ISO 8601)
   - Target URL injected/activated
   - Injection method
   - Configured exploit kit
3. Monitor traffic:
   - ✅ Target visitor triggered exploit
   - ⚠️ Non-target traffic received — verify targeting
   - ❌ No visitors after time window
4. Evidence: access log, trigger confirmation, visitor fingerprint

### 3. Real-Time Monitoring Dashboard

**Track every action and its outcome during execution:**

| # | Timestamp | Action | Technique (T-Code) | Target | Result | Detection? | Artifacts | Notes |
|---|-----------|--------|---------------------|--------|--------|------------|-----------|-------|
| 1 | {{ISO 8601}} | {{action}} | {{T-code}} | {{target}} | ✅/⚠️/❌/🛑 | None/Possible/Confirmed | {{artifacts}} | {{notes}} |

**Continuously monitor for:**

- **C2 callback received?** → Document, proceed to step 9 with [C]
- **Target service went down?** → 🛑 IMMEDIATE STOP — assess collateral damage, document, contact point of contact
- **Account locked?** → 🛑 STOP — document, assess detection, switch to fallback
- **Email bounced/filtered?** → Annotate, send to next target if available
- **Contact from blue team?** → 🛑 IMMEDIATE STOP — activate deconfliction protocol (reference deconfliction procedure in the RoE)

### 4. Detection Assessment

**After EACH action, assess whether the SOC detected the activity:**

**Detection Indicators:**
- IP blocked or rate-limited (verify connectivity from redirector)
- Account disabled or password changed (verify with subsequent attempt)
- Email quarantined or removed from mailbox (verify tracking)
- Direct contact from the security team or engagement point of contact
- Sudden changes in defensive posture (new firewall rules, DNS modifications)

**Classification per action:**

| # | Action | Detection Indicators | Classification | Operational Impact |
|---|--------|---------------------|----------------|-------------------|
| {{n}} | {{action}} | {{indicators_observed}} | No Detection / Possible Detection / Confirmed Detection | {{impact_assessment}} |

**Confirmed Detection — Response Protocol:**
1. IMMEDIATE STOP of all ongoing actions
2. Document: what was detected, how we know, timestamp
3. Assess impact: is the C2 infrastructure burned? Was the payload analyzed? Is the operation compromised?
4. Decide: full abort, pause and reassess, or switch to completely different vector
5. Notify the operator with explicit recommendation

### 5. Fallback Protocol

**If the primary technique fails, follow the pre-approved fallback decision tree:**

```
Primary failed → Retry (max 2 attempts) → Fallback 1 → Retry (max 2) → Fallback 2 → Retry (max 2) → Document failure
```

**For each level of the fallback chain:**

1. **Document the failure:**
   - What happened — detailed error description
   - Why it failed — root cause analysis (defenses, technical error, target not vulnerable)
   - Evidence — screenshots, logs, error output

2. **Assess failure type:**
   - **Temporary** (retry possible): timeout, network error, rate limiting → wait, slightly modify the approach, retry (max 2 retries)
   - **Permanent** (switch necessary): patch applied, account disabled, email systematically filtered → switch to fallback technique

3. **If switching to fallback:**
   - Document decision rationale for the switch
   - Verify that the fallback technique is still usable (infrastructure active, payload valid)
   - The fallback technique is already pre-approved in the RoE gate of step 7
   - Load fallback payload/delivery from step 5/6 preparation
   - Execute following the same procedure as section 2
   - Update the monitoring dashboard (section 3)

4. **If ALL techniques exhausted:**
   - Document every attempt and every failure
   - Calculate metrics: total attempts, time spent, detection events
   - Proceed to step 10 for reporting with `callback_status: "failed"`
   - Note: a failed initial access is NOT a failed engagement — information about which defenses worked is a valuable deliverable

**Decision Log:**
```
| # | Technique | Attempt | Result | Decision | Rationale |
|---|-----------|---------|--------|----------|-----------|
| 1 | {{primary}} | 1/3 | ❌ Failed | Retry | {{reason}} |
| 2 | {{primary}} | 2/3 | ❌ Failed | Switch FB1 | {{reason}} |
| 3 | {{fallback_1}} | 1/3 | ... | ... | ... |
```

### 6. Evidence Chain Documentation

**For EVERY action taken during execution, document the complete evidence record:**

```markdown
### Action #{{n}}
- **Timestamp**: {{ISO 8601}}
- **Technique**: {{T-code}} — {{technique_name}}
- **Target**: {{IP/email/URL}}
- **Action**: {{detailed_description}}
- **Result**: Success / Failure / Partial
- **Artifacts**: {{screenshots, logs, hashes, packet captures}}
- **Detection**: None / Possible / Confirmed
- **Notes**: {{additional_context}}
```

**Evidence Integrity:**
- Every screenshot must include a visible timestamp
- Every log must be preserved in its original form
- SHA256 hash of every artifact for chain of custody
- Action chronology must be consistent with no temporal gaps

**Execution Summary:**
```
Total execution duration: {{execution_duration}}
Total actions: {{action_count}}
Primary technique: {{primary}} — {{success/failed}}
Fallbacks used: {{fallback_count}} ({{which}})
Total attempts: {{total_attempts}}
Detection events: {{detection_count}}
Callback received: Yes/No
```

### 7. Append Findings to Report

Write findings under `## Execution Log`:

```markdown
## Execution Log

### Execution Summary
- Primary technique: {{technique_selected.primary}} ({{technique_tcode}})
- Primary result: {{success/failed}}
- Fallbacks used: {{fallback_count}}
- Total attempts: {{targets_attempted}}
- Callback received: {{yes/no}}
- Detection events: {{detection_events}}
- Execution duration: {{duration}}

### Pre-Execution Verification
{{pre_execution_status_table}}

### Monitoring Dashboard
{{real_time_monitoring_table}}

### Detection Assessment
{{detection_assessment_table}}

### Fallback Decision Log
{{fallback_decision_log — if applicable}}

### Evidence Chain
{{per_action_evidence_documentation}}

### Execution Summary
{{execution_summary_block}}
```

Update frontmatter:
- `targets_attempted` with total number of targets attempted
- `detection_events` with count of detection events
- `callback_status` — set to `"failed"` if no callback received and all techniques exhausted; leave as `"pending"` if callback received (step 9 will update to `"verified"`)

### 8. Present MENU OPTIONS

"**Execution completed.**

Technique: {{primary_tcode}} {{primary_name}} — Result: {{result}}
Attempts: {{targets_attempted}} | Detection: {{detection_events}} events
Callback: {{received/not_received}} | Fallbacks used: {{fallback_count}}
Duration: {{execution_duration}}

**Select an option:**
[A] Advanced Elicitation — In-depth analysis of execution results and unexplored alternatives
[W] War Room — Red (what worked/failed, lessons learned) vs Blue (what was detected, detection gaps)
[C] Continue — Proceed to Callback Verification and Stabilization (Step 9 of 10)"

#### Menu Handling Logic:

- IF A: Deep analysis — examine execution results, analyze why specific actions succeeded or failed, explore alternative approaches that could have been taken, assess whether the detection assessment is accurate, evaluate OPSEC posture after execution. Process insights, ask user if they want to note anything, if yes update document then redisplay menu, if no redisplay menu
- IF W: War Room — Red Team perspective: which actions were most effective? What surprised us? Were fallbacks adequate? Would a different approach sequence have been better? Blue Team perspective: what telemetry was likely generated? What log sources captured the activity? What would a competent SOC analyst see in the SIEM right now? Estimate time to detection. Summarize insights, redisplay menu
- IF C (callback received): Update output file frontmatter adding this step name to stepsCompleted and updating targets_attempted and detection_events, then read fully and follow: ./step-09-callback.md
- IF C (NO callback, all techniques exhausted): Update output file frontmatter adding this step name to stepsCompleted, updating targets_attempted, detection_events, and setting callback_status to "failed", then read fully and follow: ./step-10-complete.md — skip step 9 entirely since there is no callback to verify
- IF user asks questions: Answer and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, targets_attempted and detection_events updated, and callback_status set to "failed" if applicable], will you then:
- **If callback received**: read fully and follow: `./step-09-callback.md` to verify callback and stabilize foothold
- **If NO callback and all techniques exhausted**: read fully and follow: `./step-10-complete.md` to document and close the engagement with callback_status "failed"

---

## 🚨 SYSTEM SUCCESS/FAILURE METRICS

### ✅ SUCCESS:

- Pre-execution verification completed with all components confirmed operational
- Execution timer started and duration tracked
- Technique executed following the exact plan approved in RoE gate (step 7)
- Every action logged with timestamp, technique, target, result, artifacts, and detection status
- Real-time monitoring dashboard maintained throughout execution
- Detection assessed after EVERY action with classification and impact analysis
- Fallback protocol followed correctly when primary technique failed
- Evidence chain documented for every action with SHA256 hashes and timestamps
- targets_attempted and detection_events updated in frontmatter
- callback_status set to "failed" if no callback received and all techniques exhausted
- Execution Log section populated in output document

### ❌ SYSTEM FAILURE:

- Executing any offensive action without confirming logging is active
- Continuing after confirmed detection without impact assessment
- Deviating from the plan approved in the RoE gate without re-verification
- Not logging actions with complete evidence records (timestamp, target, result, artifacts)
- Not assessing detection after every action
- Not following the fallback decision tree when primary technique fails
- Improvising techniques not pre-approved in step 7
- Missing evidence documentation (screenshots, logs, hashes)
- Not tracking execution duration and action count
- Proceeding without user selecting 'C' (Continue)

**Master Rule:** Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE. Every action logged, every detection assessed, every evidence preserved. Undocumented execution is unacceptable.
