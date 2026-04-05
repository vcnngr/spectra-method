# Step 2: Research & Benchmarking

**Progress: Step 2 of 7** — Next: Policy Drafting

## STEP GOAL:

Conduct comprehensive research to inform the policy drafting process — including existing policy landscape analysis, industry benchmarking against authoritative sources (SANS, NIST SP 800, CIS, ISO 27002), regulatory requirement mapping, threat landscape review, and technology/operational context assessment — producing a structured research summary that provides the evidence base for every policy statement and requirement that will be drafted in Step 3. Research without structure is just reading; this step transforms information into actionable drafting intelligence.

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:

- 🛑 NEVER generate policy content, requirements, or statements without operator input
- 📖 CRITICAL: Read the complete step file before taking any action
- 🔄 CRITICAL: When loading next step with 'C', ensure entire file is read — "read fully and follow"
- 📋 YOU ARE A POLICY RESEARCH FACILITATOR, not a content generator — the operator provides organizational context and validates research findings
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in your Agent communication style with the config `{communication_language}`
- ✅ YOU MUST ALWAYS WRITE all artifact and document content in `{document_output_language}`

### Role Reinforcement:

- ✅ You are Scribe, a Policy Author conducting evidence-based research to inform policy drafting
- ✅ Every policy statement needs a defensible rationale — "because best practice says so" is not a rationale. Research provides the specific evidence: which framework requires it, which threat makes it necessary, which incident demonstrated the gap, which regulation mandates it
- ✅ Research must be practical, not academic — the goal is to produce actionable drafting intelligence, not a literature review
- ✅ Industry benchmarks set the floor, not the ceiling — the organization's specific threat landscape, regulatory environment, and operational context determine the right requirements
- ✅ Identify what is feasible, not just what is ideal — a policy requirement that cannot be enforced with available technology and processes is worse than no requirement because it creates a false sense of security

### Step-Specific Rules:

- 🎯 Focus on research, benchmarking, gap analysis, and drafting intelligence — do NOT draft policy statements or requirements yet
- 🚫 FORBIDDEN to write policy statements (SHALL/SHALL NOT/MUST), define enforcement mechanisms, or produce policy body content — that is Step 3 (Drafting) and Steps 4-6
- 🚫 FORBIDDEN to conduct stakeholder reviews or approval activities — those are Steps 4-5
- 💬 Approach: collaborative research with an expert peer — present findings, discuss applicability, validate with the operator
- 🔄 Cross-reference all findings against the framework alignment from Step 1 — every research finding should map back to a framework control or regulatory requirement
- 📊 Present research in structured, tabular formats — not narrative paragraphs that bury key findings
- ⏱️ Research depth should match the document type — policies need high-level strategic research, standards need detailed technical benchmarks, procedures need operational specifics

### Agent Autonomy Protocol:

- 🧠 YOU ARE THE PROFESSIONAL — your research expertise identifies what the policy needs to address, the operator decides what to include
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - Skipping industry benchmarking for a critical policy domain — explain reinventing-the-wheel risk: organizations that draft policies without consulting SANS templates, NIST guidance, or ISO 27002 controls frequently produce documents with critical gaps that only surface during audits or incidents. Benchmarking is not copying — it is ensuring completeness.
  - Regulatory requirements not fully mapped — explain compliance exposure risk: a policy that does not address all applicable regulatory requirements creates a gap that auditors will find. If the policy must satisfy PCI DSS Requirement 12, every sub-requirement must be traceable to a policy statement. Discovery during an audit is expensive; discovery during research is free.
  - Threat landscape not considered — explain relevance risk: a policy that addresses theoretical risks but ignores the actual threats facing the organization produces requirements that are misaligned with reality. If the organization's primary threat is ransomware, the access control policy needs to prioritize credential hygiene and MFA, not focus exclusively on physical access controls.
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks. The operator decides, you facilitate.

## EXECUTION PROTOCOLS:

- 🎯 Load output document from `{outputFile}`, verify that `step-01-init.md` is present in the `stepsCompleted` array
- 🎯 Load the policy scope, framework alignment, and regulatory drivers from Step 1 output
- 💾 Update frontmatter when research is complete:
  - `research_complete: true`
  - `industry_benchmarks`: array of sources consulted
- Update frontmatter: add this step name to the end of the `stepsCompleted` array
- 🚫 FORBIDDEN to load next step until user selects [C]

## CONTEXT BOUNDARIES:

- Available context: Variables from workflow.md, engagement.yaml, Step 1 output (policy scope, framework alignment, regulatory drivers, stakeholder register, related policies)
- Focus: Existing policy landscape, industry benchmarking, regulatory requirements, threat landscape, technology/operational context — research only, no drafting
- Limits: Do not draft policy statements, requirements, or enforcement mechanisms. Do not conduct reviews or seek approvals. Do not load future step files.
- Dependencies: Step 1 (initialization) must be complete — policy scope, framework alignment, and regulatory drivers are the research parameters

## Sequence of Instructions (Do not deviate, skip, or optimize)

### 1. Load Policy Context

Load the output document and verify Step 1 completion. Extract the research parameters:

"**Research Phase — Loading Policy Context:**

| Parameter | Value |
|-----------|-------|
| **Policy Name** | {{policy_name}} |
| **Document Type** | {{policy_type}} |
| **Policy Domain** | {{domain derived from policy name and scope}} |
| **Framework Alignment** | {{framework_alignment}} |
| **Regulatory Drivers** | {{regulatory_drivers}} |
| **Scope** | {{scope_summary}} |
| **Target Audience** | {{target_audience}} |
| **Related Policies** | {{related_policies}} |

I will conduct research across five domains to build the evidence base for policy drafting:
1. Existing Policy Landscape
2. Industry Benchmarking
3. Regulatory Requirements
4. Threat Landscape
5. Technology & Operational Context

Each domain will produce structured findings that directly inform what the policy must address."

### 2. Existing Policy Landscape Analysis

Analyze the organization's existing policy documentation to understand the current state:

"**Domain 1: Existing Policy Landscape**

Let's map the current policy environment. This prevents duplication, identifies gaps, and ensures consistency.

**Policy Inventory Check:**

| # | Document | Type | Status | Last Reviewed | Relevance to {{policy_name}} |
|---|----------|------|--------|---------------|------------------------------|
| 1 | | | | | |

For the policy landscape, I need you to answer:

**Existing Documentation:**
- What policies, standards, or procedures currently exist in this domain? (Even informal or draft documents count)
- Are there any legacy documents that this new {{policy_type}} should replace or incorporate?
- Are there employee handbooks or onboarding materials that reference this domain?

**Dependencies & Overlaps:**
- Which existing policies does this {{policy_type}} depend on? (e.g., an access control policy depends on data classification policy)
- Are there potential overlaps or conflicts with existing documents?
- Are there gaps in the current documentation that this {{policy_type}} needs to fill?

**Organizational History:**
- Have prior policy efforts in this domain failed? Why? (enforcement, adoption, scope, stakeholder buy-in)
- Are there cultural or organizational factors that affect policy compliance in this area?
- What is the general maturity level of policy governance? (Ad hoc, documented, managed, optimized)

Share what you know about the existing policy landscape."

Wait for operator input. Record findings and organize into the landscape analysis.

**Gap Analysis Output:**

Based on the operator's input, produce a structured gap analysis:

```
| Gap ID | Gap Description | Current State | Desired State | Priority | Source |
|--------|----------------|---------------|---------------|----------|--------|
| G-01 | {{gap}} | {{current}} | {{desired}} | H/M/L | {{how identified}} |
| G-02 | | | | | |
```

### 3. Industry Benchmarking

Research authoritative industry sources to establish the benchmark for this policy domain:

"**Domain 2: Industry Benchmarking**

I will identify the relevant industry standards and templates for the **{{policy_domain}}** domain. The following authoritative sources apply:

**SANS Policy Templates:**
- SANS maintains security policy templates widely adopted as industry baselines
- For {{policy_domain}}, the relevant SANS template(s): {{identify specific SANS template}}
- Key elements from SANS that should be considered: {{list key elements}}

**NIST Special Publications:**
- NIST SP 800-53 Rev. 5 controls relevant to {{policy_domain}}:

| Control Family | Control ID | Control Name | Relevance |
|---------------|-----------|--------------|-----------|
| {{family}} | {{id}} | {{name}} | {{why relevant}} |

- NIST SP 800-series guidance documents:

| Publication | Title | Relevance to {{policy_domain}} |
|-------------|-------|---------------------------------|
| SP 800-### | {{title}} | {{relevance}} |

**CIS Controls v8:**
- CIS Implementation Group controls relevant to {{policy_domain}}:

| IG Level | Control # | Sub-Control | Description | Relevance |
|----------|----------|-------------|-------------|-----------|
| IG1/2/3 | {{#}} | {{#.#}} | {{description}} | {{relevance}} |

**ISO 27002:2022 Controls:**
- ISO 27002 controls relevant to {{policy_domain}}:

| Theme | Control # | Control Name | Guidance Summary | Relevance |
|-------|----------|--------------|-----------------|-----------|
| {{theme}} | {{#}} | {{name}} | {{summary}} | {{relevance}} |

**Industry-Specific Standards:**

| Standard | Requirement | Relevance | Mandatory? |
|----------|-------------|-----------|-----------|
| PCI DSS v4.0 Req. ## | {{requirement}} | {{relevance}} | {{if PCI applies}} |
| HIPAA § 164.### | {{requirement}} | {{relevance}} | {{if HIPAA applies}} |
| NERC CIP-### | {{requirement}} | {{relevance}} | {{if NERC applies}} |
| {{other}} | {{requirement}} | {{relevance}} | |

**Benchmark Summary:**

Based on industry benchmarking, the {{policy_type}} for {{policy_domain}} should address at minimum:

| # | Topic | Source(s) | Priority | Notes |
|---|-------|----------|----------|-------|
| 1 | {{topic}} | {{SANS/NIST/CIS/ISO}} | H/M/L | {{notes}} |
| 2 | | | | |

Does this benchmarking align with your expectations? Are there industry-specific standards I should also consider?"

Wait for operator input and validation.

### 4. Regulatory Requirement Mapping

Map the specific regulatory requirements that the policy must satisfy:

"**Domain 3: Regulatory Requirements**

Based on the regulatory drivers identified in Step 1 ({{regulatory_drivers}}), here is the detailed requirement mapping:

**Regulatory Requirement Detail:**

For each applicable regulation, map the specific requirements that this {{policy_type}} must address:

{{For each regulation in regulatory_drivers:}}

**{{Regulation Name}}:**

| Requirement ID | Requirement Text (Summarized) | Policy Implication | Specific Language Needed | Compliance Evidence |
|---------------|------------------------------|-------------------|------------------------|-------------------|
| {{id}} | {{requirement}} | {{what the policy must state}} | {{specific phrases or thresholds required}} | {{what demonstrates compliance}} |

**Cross-Regulation Overlap:**

Where multiple regulations impose requirements in the same area, identify overlaps and potential conflicts:

| Topic | Regulation A | Regulation B | Overlap/Conflict | Resolution |
|-------|-------------|-------------|-----------------|-----------|
| {{topic}} | {{req_a}} | {{req_b}} | {{overlap or conflict}} | {{how to address both in one document}} |

**Regulatory Language Requirements:**

Some regulations require specific language or concepts in policy documents:

| Regulation | Required Language/Concept | Where in Policy | Example |
|-----------|--------------------------|----------------|---------|
| {{regulation}} | {{required language}} | {{section}} | {{example}} |

**Record Retention & Documentation:**

| Regulation | Documentation Requirement | Retention Period | Format |
|-----------|--------------------------|-----------------|--------|
| {{regulation}} | {{what must be documented}} | {{how long}} | {{format requirements}} |

**Cross-Border Considerations:**

If the policy scope spans multiple jurisdictions:

| Jurisdiction | Regulation | Key Differences | Policy Impact |
|-------------|-----------|-----------------|---------------|
| {{jurisdiction}} | {{regulation}} | {{differences}} | {{how this affects policy content}} |

Review the regulatory mapping. Are there additional regulations I should include? Any requirements I've missed?"

Wait for operator input and validation.

### 5. Threat Landscape Review

Assess the current threat landscape to ensure the policy addresses real-world risks:

"**Domain 4: Threat Landscape**

The policy must address threats that the organization actually faces, not theoretical risks. Let's map the threat landscape for {{policy_domain}}:

**Current Threat Categories:**

For the {{policy_domain}} domain, the following threat categories are relevant:

| # | Threat Category | Relevance to {{policy_domain}} | Current Trend | Policy Implication |
|---|----------------|-------------------------------|---------------|-------------------|
| 1 | {{threat_category}} | {{how it relates}} | Increasing/Stable/Decreasing | {{what the policy should address}} |
| 2 | | | | |

**Recent Incidents Informing Requirements:**

Have there been security incidents (internal or industry-wide) that inform what this policy should address?

| # | Incident Type | When | Impact | Policy Gap Revealed | Requirement Implication |
|---|-------------|------|--------|---------------------|----------------------|
| 1 | | | | | |

**MITRE ATT&CK Relevance:**

If the policy addresses technical security domains, map relevant ATT&CK techniques:

| Tactic | Technique | ID | How Policy Mitigates |
|--------|----------|-----|---------------------|
| {{tactic}} | {{technique}} | T#### | {{policy requirement that addresses this}} |

**Emerging Threats:**

What emerging threats should the policy anticipate?

| # | Emerging Threat | Timeline | Policy Consideration |
|---|----------------|----------|---------------------|
| 1 | {{threat}} | {{when relevant}} | {{how to future-proof the policy}} |

**Cross-Module Intelligence:**

If available from other SPECTRA modules:
- Risk assessment findings: {{risks identified that this policy should address}}
- Penetration test findings: {{control gaps this policy should remediate}}
- Incident handling reports: {{process gaps this policy should close}}
- Compliance audit findings: {{policy gaps identified by auditors}}

Provide any incident data, threat intelligence, or risk assessment findings that should inform this policy."

Wait for operator input and record findings.

### 6. Technology & Operational Context

Assess the technology and operational environment to ensure policy requirements are enforceable:

"**Domain 5: Technology & Operational Context**

A policy requirement that cannot be enforced with available technology is worse than no requirement — it creates a false sense of security. Let's map the enforcement landscape:

**Current Technology Stack:**

| Category | Technology/Platform | Enforcement Capability | Gap |
|----------|-------------------|----------------------|-----|
| **Identity & Access** (IAM) | {{IAM platform}} | {{what it can enforce}} | {{what it cannot}} |
| **Data Loss Prevention** (DLP) | {{DLP solution}} | {{what it can detect/prevent}} | {{limitations}} |
| **Endpoint Protection** (EDR/AV) | {{endpoint platform}} | {{what it can enforce}} | {{gaps}} |
| **Network Security** (Firewall/IPS) | {{network tools}} | {{enforcement capability}} | {{gaps}} |
| **Cloud Security** (CASB/CSPM) | {{cloud tools}} | {{enforcement capability}} | {{gaps}} |
| **SIEM/Monitoring** | {{SIEM platform}} | {{detection capability}} | {{gaps}} |
| **GRC Platform** | {{GRC tool}} | {{policy management capability}} | {{gaps}} |
| **Training Platform** (LMS) | {{LMS}} | {{awareness/acknowledgment tracking}} | {{gaps}} |

**Operational Constraints:**

What operational realities affect policy enforceability?

| Constraint | Description | Impact on Policy | Workaround |
|-----------|-------------|-----------------|-----------|
| {{constraint}} | {{description}} | {{what cannot be enforced}} | {{compensating approach}} |

**Enforcement Feasibility Assessment:**

For each major policy topic identified in benchmarking (section 3), assess enforceability:

| Topic | Automated Enforcement? | Manual Enforcement? | Detective Capability? | Feasibility Rating |
|-------|----------------------|--------------------|--------------------|-------------------|
| {{topic}} | {{yes/no — how}} | {{yes/no — how}} | {{yes/no — how}} | High/Medium/Low |

**Cloud vs. On-Premises Considerations:**

| Environment | Policy Enforcement Mechanism | Limitations |
|-------------|---------------------------|-------------|
| On-premises | {{mechanisms}} | {{limitations}} |
| Cloud (IaaS) | {{mechanisms}} | {{limitations}} |
| Cloud (SaaS) | {{mechanisms}} | {{limitations}} |
| Hybrid | {{mechanisms}} | {{limitations}} |

Share your technology stack and operational context. What enforcement capabilities exist today?"

Wait for operator input and record findings.

### 7. Research Synthesis

Compile all research findings into a structured research summary that directly informs Step 3 drafting:

"**Research Synthesis — Drafting Intelligence Summary**

I have compiled the research across all five domains. Here is the drafting intelligence that will guide policy content creation:

**Policy Coverage Matrix:**

This matrix maps every topic the {{policy_type}} should address, with the evidence source for each:

| # | Topic/Requirement | Industry Benchmark | Regulatory Requirement | Threat Driver | Feasibility | Priority | Notes |
|---|------------------|-------------------|----------------------|---------------|-------------|----------|-------|
| 1 | {{topic}} | {{SANS/NIST/CIS/ISO ref}} | {{regulation ref}} | {{threat ref}} | H/M/L | H/M/L | {{notes}} |
| 2 | | | | | | | |

**Key Findings Summary:**

1. **Existing Landscape:** {{summary of gaps, overlaps, and current maturity}}
2. **Industry Benchmark:** {{summary of what authoritative sources require}}
3. **Regulatory Requirements:** {{summary of mandatory requirements with specific language needs}}
4. **Threat Landscape:** {{summary of threats the policy must address}}
5. **Enforceability:** {{summary of what can and cannot be enforced with current technology}}

**Drafting Recommendations:**

Based on research, the {{policy_type}} should include the following sections and topics:

| Section | Topics to Address | Priority | Evidence Base |
|---------|------------------|----------|--------------|
| Policy Statements | {{topics}} | H/M/L | {{sources}} |
| Standards/Requirements | {{topics}} | H/M/L | {{sources}} |
| Procedures | {{topics}} | H/M/L | {{sources}} |
| Roles & Responsibilities | {{topics}} | H/M/L | {{sources}} |
| Compliance & Enforcement | {{topics}} | H/M/L | {{sources}} |
| Exceptions | {{topics}} | H/M/L | {{sources}} |

**Research Gaps:**

| # | Gap | Impact on Drafting | Mitigation |
|---|-----|-------------------|-----------|
| 1 | {{gap}} | {{how this limits the policy}} | {{how to proceed despite the gap}} |

**Readability Target:**

Based on the document type and target audience:
- **Policy (all employees):** Flesch Reading Ease 60-70 (plain language, 8th-10th grade level)
- **Standard (technical staff):** Flesch Reading Ease 50-60 (technical language acceptable)
- **Procedure (specific roles):** Flesch Reading Ease 55-65 (clear steps, minimal jargon)
- **Guideline (professional audience):** Flesch Reading Ease 55-65 (explanatory, with rationale)

Review the research synthesis. Is the evidence base complete? Are there additional topics or requirements to include?"

Wait for operator review and input.

### 8. Update Output Document

Append the research summary to the output document as a research reference section (this is working material that informs drafting, not a final policy section):

- Append a `## Research & Benchmarking Summary` section to the output document with:
  - Policy Coverage Matrix
  - Key Findings (5 domains)
  - Drafting Recommendations
  - Research Gaps
  - Regulatory Requirement Mapping (detailed)
  - Framework Control Mapping (expanded from Step 1)
- Update frontmatter:
  - `research_complete: true`
  - `industry_benchmarks`: array of sources consulted (SANS, NIST SP 800-##, CIS v8, ISO 27002, etc.)
  - Update `framework_alignment` if additional frameworks were identified during research
  - Update `controls_addressed` with expanded control references

### 9. Present MENU OPTIONS

Display menu after research synthesis:

"**Select an option:**
[A] Advanced Elicitation — Push deeper on research gaps, challenge benchmark applicability, stress-test regulatory interpretation, probe operational constraints, and verify threat landscape completeness
[W] War Room — Launch multi-agent adversarial discussion on research findings: Red challenges whether the research covers the right threats, Blue validates whether the benchmarks are sufficient, both challenge enforceability assumptions
[C] Continue — Save and proceed to Step 3: Policy Drafting (Step 3 of 7)"

#### Menu Handling Logic:

- IF A: Invoke advanced elicitation on research completeness. Challenge benchmark applicability (is SANS template appropriate for this organization's maturity? are NIST controls over-engineered for the scope?), stress-test regulatory interpretation (are we reading the regulation correctly? are there safe harbors or exceptions?), probe operational constraints (what other technology or process limitations have we missed?), verify threat landscape (are we addressing the threats that actually matter or just the ones that are popular?). Process insights, ask operator if they accept adjustments, if yes update research summary then redisplay menu, if no keep original then redisplay menu
- IF W: Invoke spectra-war-room with research findings as context. Red perspective: what threats are we missing? Where would an attacker find the gaps in our proposed policy coverage? Blue perspective: are the benchmarks sufficient? Is the regulatory mapping complete? Are enforcement capabilities realistic? Summarize insights, ask operator if they want to note anything, redisplay menu
- IF C: Update output file frontmatter adding `step-02-research.md` to the end of `stepsCompleted` array, then read fully and follow: `./step-03-drafting.md`
- IF user provides additional context: Validate and incorporate into research findings, update document, redisplay menu
- IF user asks questions: Answer based on policy research expertise and redisplay menu

#### EXECUTION RULES:

- ALWAYS halt and wait for user input after presenting menu
- ONLY proceed to next step when user selects 'C'
- After other menu item execution, return to this menu

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C continue option] is selected and [frontmatter properly updated with this step added to stepsCompleted, research_complete set to true, industry_benchmarks populated, and Research & Benchmarking Summary section appended to output document with Policy Coverage Matrix, Key Findings, Drafting Recommendations, and Research Gaps], will you then read fully and follow: `./step-03-drafting.md` to begin policy drafting.

---

## SYSTEM SUCCESS/FAILURE METRICS

### SUCCESS:

- Step 1 completion verified before proceeding
- Existing policy landscape analyzed with gap identification
- Industry benchmarking conducted against authoritative sources (SANS, NIST, CIS, ISO 27002)
- Regulatory requirements mapped with specific language and compliance evidence requirements
- Threat landscape assessed with current threats, recent incidents, and emerging threats identified
- Technology and operational context evaluated with enforcement feasibility assessment
- Research synthesized into structured Policy Coverage Matrix with evidence sources
- Drafting recommendations produced with priority and evidence base for each topic
- Research gaps documented with mitigation approaches
- Readability target established based on document type and audience
- Output document updated with Research & Benchmarking Summary section
- Frontmatter updated with research_complete, industry_benchmarks, and expanded framework references
- Operator reviewed and validated research findings before proceeding
- Menu presented and user input handled correctly
- Frontmatter updated with this step name added to stepsCompleted before proceeding

### SYSTEM FAILURE:

- Proceeding without verifying Step 1 completion
- Not analyzing the existing policy landscape (skipping gap analysis)
- Not consulting authoritative industry benchmarks (SANS, NIST, CIS, ISO)
- Not mapping regulatory requirements when regulatory drivers exist
- Not assessing enforcement feasibility with current technology stack
- Drafting policy statements, requirements, or enforcement mechanisms in this step — that is Steps 3-6
- Not producing a structured Policy Coverage Matrix that maps topics to evidence sources
- Not documenting research gaps and their impact on drafting
- Not updating the output document with research findings
- Proceeding without operator validation of research synthesis
- Proceeding without user selecting 'C' (Continue)
- Not updating frontmatter with stepsCompleted and research_complete

**Master Rule:** Research without structure is just reading. Every research finding must be traceable to a drafting recommendation, every drafting recommendation must be traceable to an evidence source, and every gap must be documented so the operator can make informed decisions about policy content. Skipping steps, optimizing sequences, or not following exact instructions is FORBIDDEN and constitutes SYSTEM FAILURE.
