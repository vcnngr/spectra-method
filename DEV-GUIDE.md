# SPECTRA Development Guide

> This guide is for the AI context that continues to develop SPECTRA. It is not user documentation.

## How to Resume Development

Suggested prompt for the user:
```
/coordinator
Continue building SPECTRA. Read _spectra/SPECTRA.md for context and _spectra/DEV-GUIDE.md for development patterns. The next natural step is [whatever is needed].
```

## Reference Patterns

SPECTRA replicates BMAD patterns. To understand them, the primary reference is the work already done:

### Internal reference (READ THESE):
- **Complete recon workflow**: `_spectra/rtk/workflows/spectra-external-recon/` — 10 steps, workflow.md, template, resume handler. THIS is the quality benchmark.
- **Agent SKILL.md**: `_spectra/rtk/agents/spectra-agent-red-lead/SKILL.md` — standard agent format
- **War Room**: `_spectra/core/spectra-war-room/workflow.md` — multi-agent adversarial pattern
- **New Engagement**: `_spectra/core/spectra-new-engagement/` — core workflow with 3 steps

### BMAD reference (if needed to understand the original pattern):
- Agent format: `_bmad/bmm/3-solutioning/bmad-agent-architect/SKILL.md`
- Workflow format: `_bmad/bmm/2-plan-workflows/bmad-create-prd/workflow.md`
- Step files: `_bmad/bmm/2-plan-workflows/bmad-create-prd/steps-c/`
- Party mode: `_bmad/core/bmad-party-mode/workflow.md`

## Exact File Formats

### Agent SKILL.md
```markdown
---
name: spectra-agent-{name}
description: "{description}"
---

# {DisplayName}

## Overview
{2-3 sentences}

## Identity
{From agent-manifest.csv, verbatim}

## Communication Style
{From agent-manifest.csv, verbatim}

## Principles
{From agent-manifest.csv, verbatim}

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## Capabilities

| Code | Description | Skill |
|------|-------------|-------|
| XX | Description | spectra-skill-name |

## On Activation

1. **Load config via spectra-init skill** — Store all returned vars
2. **Load engagement context** — Search for active engagement.yaml
   - If NO engagement found: inform user, recommend `spectra-new-engagement`
   - If engagement found: load scope, verify status is "active"
3. **Greet and present capabilities** — Greet `{user_name}` in `{communication_language}`
4. Present capabilities table

**STOP and WAIT for user input**

**CRITICAL:** When user responds with a code, invoke the corresponding skill by its exact registered name.
```

### Workflow SKILL.md (redirect)
```markdown
---
name: spectra-{workflow-name}
description: '{description}'
---

Follow the instructions in ./workflow.md.
```

### workflow.md
```markdown
---
main_config: '{project-root}/_spectra/{module}/config.yaml'
outputFile: '{artifact_path}/output-file.md'
---

# {Workflow Title}

**Goal:** {Single sentence}

**Your Role:** {Role description during the workflow}

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## WORKFLOW ARCHITECTURE

This uses **step-file architecture** for disciplined execution:

### Core Principles
- **Micro-file Design**: Each step is self-contained
- **Just-In-Time Loading**: Only the current step file is in memory
- **Sequential Enforcement**: Must follow exact order, no skipping
- **State Tracking**: Document progress in output file frontmatter using `stepsCompleted`
- **Append-Only Building**: Build documents by appending content

### Step Processing Rules
1. **READ COMPLETELY**: Read entire step file before acting
2. **FOLLOW SEQUENCE**: Execute sections in order
3. **WAIT FOR INPUT**: Halt at menus and wait
4. **CHECK CONTINUATION**: Only proceed on explicit [C]
5. **SAVE STATE**: Update stepsCompleted before loading next
6. **LOAD NEXT**: "Read fully and follow" the next step

### Critical Rules (NO EXCEPTIONS)
- 🛑 **NEVER** load multiple step files simultaneously
- 📖 **ALWAYS** read entire step file before execution
- 🚫 **NEVER** skip steps or optimize the sequence
- 💾 **ALWAYS** update frontmatter when writing final output
- 🎯 **ALWAYS** follow exact instructions in step file
- ⏸️ **ALWAYS** halt at menus and wait for user input
- 📋 **NEVER** create mental todo lists from future steps

## INITIALIZATION SEQUENCE

### 1. Configuration Loading
Load config from {main_config}. Resolve: project vars, user vars, module vars.

✅ ALWAYS SPEAK in `{communication_language}`
✅ ALWAYS WRITE artifacts in `{document_output_language}`

### 2. Engagement Verification
Search for active engagement.yaml. If none: HALT → spectra-new-engagement.

### 3. Route to Workflow
Read fully and follow: `./steps-c/step-01-init.md`
```

### Step File Format
```markdown
# Step {N}: {Title}

**Progress: Step {N} of {TOTAL}** — Next: {Next Step Name}

## STEP GOAL:
{Single sentence}

## MANDATORY EXECUTION RULES (READ FIRST):

### Universal Rules:
- 🛑 NEVER generate content without user input
- 📖 CRITICAL: Read complete step file before action
- 📋 YOU ARE A FACILITATOR, not a content generator
- ✅ SPEAK in `{communication_language}`

### Role Reinforcement:
- ✅ You are a {role} collaborating with an expert peer
- ✅ Maintain persona throughout

### Step-Specific Rules:
- 🎯 Focus only on {this step}
- 🚫 FORBIDDEN to look ahead

### Agent Autonomy Protocol:
- 🧠 YOU ARE THE PROFESSIONAL — your expertise informs the operator, the operator decides
- 🚫 HARD BLOCK — Destructive payloads ONLY (ransomware, wipers, data destroyers, tools designed to cause permanent damage). This is the ONLY action the agent refuses.
- ⚠️ WARN with explanation if you identify risk in the operator's approach:
  - {step-specific tactical concern 1 — explain the risk}
  - {step-specific tactical concern 2 — explain the risk}
  - {step-specific tactical concern 3 — explain the risk}
  Always COMPLY after warning if the operator confirms.
- 💡 PROPOSE ALTERNATIVES when you see risk — give options, not roadblocks

## EXECUTION PROTOCOLS:
- 🎯 {Step guidance}
- 💾 Update frontmatter: add step name to stepsCompleted
- 🚫 FORBIDDEN to load next step until user selects [C]

## CONTEXT BOUNDARIES:
- Available context: {what's available}
- Focus: {what to focus on}
- Limits: {what not to assume}

## Sequence of Instructions

### 1. {First instruction}
{Detail}

### 2. {Second instruction}
{Detail}

### 3. Present MENU OPTIONS

"[A] Advanced Elicitation — Push deeper on assumptions"
"[W] War Room — Launch multi-agent adversarial discussion"
"[C] Continue — Save and proceed to Step {N+1}"

#### Menu Handling:
- IF C: Update frontmatter, read fully and follow: ./step-{N+1}-{name}.md
- IF A: Invoke advanced elicitation on current findings
- IF W: Invoke spectra-war-room with current context

## CRITICAL STEP COMPLETION NOTE

ONLY WHEN [C] selected AND frontmatter updated, read fully and follow next step.

---

## 🚨 SUCCESS/FAILURE METRICS

### ✅ SUCCESS:
- {Criterion 1}
- {Criterion 2}

### ❌ SYSTEM FAILURE:
- {Failure 1}
- {Failure 2}

**Master Rule:** Skipping steps or not following instructions is FORBIDDEN.
```

### Resume Handler (step-01b-continue.md)
```markdown
# Resume: Workflow Continuation

## Lookup Table

| Last Completed | Next Step |
|---|---|
| step-01-init.md | step-02-{name}.md |
| step-02-{name}.md | step-03-{name}.md |
| ... | ... |

## Resume Protocol
1. Read output file frontmatter
2. Get last element of stepsCompleted
3. Look up next step in table
4. Present progress summary
5. Wait for user confirmation
6. Load next step
```

### Template Format
```markdown
---
stepsCompleted: []
inputDocuments: []
workflowType: '{type}'
engagement_id: '{{engagement_id}}'
---

# {Report Title} — {{engagement_id}}

**Engagement:** {{engagement_name}}
**Analyst:** {{user_name}}
**Date:** {{date}}

## {Section per step}
```

## Manifest CSV Formats

### agent-manifest.csv (12 columns)
```
name,displayName,title,icon,capabilities,role,identity,communicationStyle,principles,module,path,canonicalId
```

### skill-manifest.csv (6 columns)
```
canonicalId,name,description,module,path,install_to_spectra
```

## Suggested Development Order

### Next workflows to build (priority):

1. ~~**spectra-initial-access** (RTK)~~ — **DONE.** 10 steps, ~3,852 lines. Full kill chain from recon to foothold.

2. ~~**spectra-alert-triage** (SOC)~~ — **DONE.** 7 steps, ~2,687 lines. First blue team workflow with Purple Team bridge.

3. ~~**spectra-detection-lifecycle** (SOC)~~ — **DONE.** 7 steps, ~3,523 lines. Red↔Blue bridge: requirement intake (4 sources), ATT&CK deep mapping, Sigma/YARA/Suricata authoring, test-driven validation, deployment planning, coverage measurement, Purple Team feedback loop. Owned by Sentinel.

4. ~~**spectra-incident-handling** (IRT)~~ — **DONE.** 10 steps, ~6,874 lines. NIST 800-61 full lifecycle: incident intake, detection source analysis, severity triage, containment strategy, evidence preservation (chain of custody), deep analysis (full ATT&CK chain, timeline reconstruction, root cause), eradication (credential reset, persistence removal), recovery (phased restoration, enhanced monitoring), post-incident review (PIR with SMART recommendations), reporting & closure. Owned by Dispatch.

5. ~~**spectra-risk-assessment** (GRC)~~ — **DONE.** 7 steps, ~7,075 lines. NIST 800-30 Rev.1 / FAIR hybrid: assessment scoping & methodology, Crown Jewels Analysis (MITRE CJA, 3-tier system), threat identification (NIST D-2/E-2/E-3, ATT&CK cross-ref), vulnerability & predisposing conditions (NIST F taxonomy, FAIR TCAP/CS), risk calculation (Tables G-2→G-5→H-3→I-2 + FAIR 4-stage LEF×LM=ALE), treatment planning (Accept/Mitigate/Transfer/Avoid with ROI, residual risk, phased roadmap), executive reporting & closure (NIST Appendix K structure, confidence levels, communication plan, maintenance triggers). Owned by Arbiter.

6. ~~**spectra-privesc** (RTK)~~ — **DONE.** 10 steps, ~4,327 lines. Full privilege escalation lifecycle: foothold assessment, local enumeration (winPEAS/linPEAS), credential discovery, Windows privesc (token manipulation, UAC bypass, service exploitation, kernel), Linux privesc (SUID/SGID, sudo, capabilities, cron, container escape), AD escalation (Kerberoasting, delegation abuse, ADCS ESC1-10, DCSync, ticket forging), Cloud escalation (AWS/Azure/GCP IAM, metadata services, K8s), exploit chaining with defense evasion (AMSI/ETW/EDR bypass), verification & stability, reporting with lateral movement handoff. Owned by Phantom.

7. ~~**spectra-lateral-movement** (RTK)~~ — **DONE.** 10 steps, ~7,853 lines. Full lateral movement lifecycle: access ingestion & operational planning (privesc handoff ingestion, movement domain classification, objective definition), internal network reconnaissance (passive discovery, active scanning with stealth profiles, service enumeration, trust mapping, target prioritization by business value), credential operations (LSASS/SAM/NTDS extraction with 9 evasion variants, PtH/PtT/OPtH, Golden/Silver/Diamond tickets, NTLM relay setup with PetitPotam/PrinterBug/DFSCoerce, credential→target mapping), Windows lateral movement (PsExec/WMI/WinRM/DCOM/RDP/scheduled tasks/named pipes with per-technique OPSEC and Event IDs), Linux lateral movement (SSH with agent forwarding/ControlMaster, Ansible/Puppet/Chef/Salt abuse, Docker/K8s container pivoting, NFS/database exploitation), AD lateral movement (GPO deployment, Kerberos ticket forging, unconstrained/constrained/RBCD delegation, trust hopping, ADCS ESC1-8, SID History, DCShadow), Cloud lateral movement (AWS cross-account/SSM/Lambda/EKS, Azure managed identity/Automation/Function Apps, GCP SA impersonation/GKE, multi-cloud pivoting), network pivoting & tunneling (SSH tunnels/chisel/ligolo-ng/SOCKS, C2 pivot integration with Cobalt Strike/Sliver/Mythic, covert channels: DNS/ICMP/domain fronting), access verification & persistence (RAG status system, per-platform persistence mechanisms, OPSEC review, exfiltration readiness), reporting with exfiltration handoff & Purple Team SOC data. Owned by Phantom.

8. ~~**spectra-exfiltration** (RTK)~~ — **DONE.** 10 steps, ~9,618 lines. Largest SPECTRA workflow. Full data exfiltration lifecycle: objective ingestion & exfiltration planning (explicit RoE authorization with data type/volume/method constraints, data handling requirements, comprehensive DLP/NDR/CASB/endpoint assessment), target data discovery (SMB/NFS/DFS/SharePoint shares, MSSQL/MySQL/PostgreSQL/Oracle/MongoDB databases, Exchange/O365/Gmail/Slack/Teams comms, Git/CI-CD repos, HashiCorp Vault/AWS SM/Azure KV secrets, S3/Blob/GCS/SaaS cloud storage, backup/archive systems — Varonis/DAM-aware OPSEC), data assessment & classification (L1-L4 sensitivity framework, GDPR/HIPAA/PCI/SOX regulatory mapping, RoE compliance matrix with INCLUDE/RESTRICT/EXCLUDE, feasibility analysis with bandwidth modeling), data collection & staging (per-platform extraction commands, compression 7z/gzip/zstd, encryption AES-256/age/GPG, chunking per channel capacity, SHA-256 manifest), network exfiltration (HTTP/HTTPS/domain fronting/HTTP2, DNS dnscat2/iodine/dns2tcp/DoH, FTP/SFTP/SCP, email SMTP/EWS/Graph API, C2 Cobalt Strike/Sliver/Mythic/Metasploit, ICMP/SMB/RDP clipboard/WebSocket), cloud exfiltration (AWS S3/presigned URL/cross-account replication/Lambda, Azure Blob/SAS/Functions/Logic Apps, GCP gsutil/signed URL/Cloud Functions/Transfer Service, SaaS OneDrive/Google Drive/Slack, cloud-to-cloud, serverless SNS/SQS/EventBridge), covert channel exfiltration (steganography image/audio/document/video, protocol manipulation DNS-DoH/ICMP/HTTP headers/TCP-IP/NTP, dead drops paste sites/code repos/social media, physical USB/print/Bluetooth/QR/mobile hotspot, air-gap bridging), DLP & monitoring evasion (content inspection bypass encoding/encryption/file type manipulation/homoglyph, protocol-level HTTPS/cert pinning/domain fronting/WebSocket/QUIC, network-level traffic blending/throttling/fragmentation/timing jitter, endpoint DLP process injection/ADS/memory-only/DLL sideload, CASB personal cloud/unmanaged SaaS/API direct/shadow IT, adaptive response playbook), verification & cleanup (integrity SHA-256, evidence chain EX-NNN custody, secure deletion shred/sdelete/cipher, lateral movement artifact removal, persistence mechanism removal per-platform, credential cleanup, OPSEC final assessment, secure data handling), reporting & engagement closure (DLP assessment report, cross-phase engagement summary recon→exfil, SOC Purple Team handoff, data handling commitment with retention/deletion timeline). Owned by Phantom. **RTK MODULE COMPLETE (5/5 workflows).**

9. ~~**spectra-phishing-response** (SOC)~~ — **DONE.** 8 steps, ~3,919 lines. Full phishing incident response lifecycle: email intake & sample collection (EML/MSG/headers/forwarded/screenshot), header analysis (Received chain hop-by-hop, SPF/DKIM/DMARC/ARC verification, originating infrastructure mapping, 14-point header anomaly detection), content & payload analysis (HTML/plaintext comparison, social engineering technique ID via Cialdini/NIST, brand impersonation, URL detonation/redirect chains, attachment static/dynamic analysis per file type, polyglot detection, payload classification matrix), IOC extraction & enrichment (multi-source TI per IOC type, ATT&CK T1566.* mapping, campaign assessment), scope & impact assessment (mail flow analysis with M365/Google Workspace/Proofpoint guidance, 5-tier user interaction funnel: received/opened/clicked/submitted/compromised, endpoint assessment for Tiers 3-5, credential compromise assessment, campaign scope, regulatory notification GDPR/HIPAA/PCI), containment & eradication (email quarantine/purge with platform-specific commands, sender/domain/URL/hash blocking, 10-point account containment per user, endpoint isolation, infrastructure blocking), detection & prevention (email gateway rules, Sigma/YARA/Suricata rules, phased DMARC rollout, 4-audience awareness communications, Purple Team feedback), reporting & closure. Owned by Tracker.

10. ~~**spectra-threat-hunt** (SOC)~~ — **DONE.** 8 steps, ~3,455 lines. Hypothesis-driven threat hunting lifecycle: hunt mission definition (6 trigger types: intel/incident/detection-gap/anomaly/hypothesis/environmental-driven, hunt scope, tactical vs strategic classification), hypothesis development (ATT&CK-based construction, threat actor profiling, hypothesis formulation framework with null hypothesis, data source availability matrix, success criteria with confidence levels), data collection & preparation (multi-SIEM query construction SPL/KQL/EQL/Sigma/EDR, log source health check, baseline establishment: statistical/behavioral/whitelisting, hunt execution plan), automated analysis (systematic query execution, 6 pattern detection techniques: frequency/stack ranking/time-series/baseline deviation/clustering/long-tail, automated triage known-good/known-bad/unknown, cross-data-source correlation), manual analysis (deep dive on automated findings, behavioral analysis: LOLBin detection with 8 tool families, lateral movement traces 5 methods, persistence 6 mechanisms, credential access 4 indicators, data staging/exfiltration, threat actor TTP matching), finding analysis & validation (evidence correlation, timeline reconstruction, 4-tier classification: confirmed malicious/suspicious/benign anomaly/FP, ATT&CK procedure-level mapping, hypothesis verdict: confirmed/refuted/inconclusive), detection engineering (Sigma/YARA/Suricata rule creation with full metadata, hunt playbook creation, ATT&CK coverage delta, attack surface reduction, Purple Team feedback), reporting with SQRRL maturity assessment and repeatability scoring. Owned by Hawk. **SOC MODULE COMPLETE (4/4 workflows).**

11. ~~**spectra-digital-forensics** (IRT)~~ — **DONE.** 10 steps, ~5,324 lines. Complete digital forensic investigation lifecycle: case intake & evidence receipt (EVD-NNN chain of custody, legal context, case classification, evidence inventory with hashing), evidence acquisition & preservation (RFC 3227 order of volatility, disk imaging with write blockers, memory capture with LiME/WinPmem/DumpIt, cloud evidence AWS/Azure/GCP, network capture, working copy creation with integrity verification), disk forensics (NTFS $MFT/$UsnJrnl/ADS, Windows: Registry/EventLog/Prefetch/Amcache/ShimCache/SRUM/BAM, Linux: auth.log/journal/bash_history, macOS: Unified Logs/FSEvents/KnowledgeC, browser/email/messaging/remote access forensics, anti-forensics detection: timestomping/$SI vs $FN comparison/secure deletion/log clearing), memory forensics (Volatility 3: pslist/psscan/pstree comparison for hidden processes, code injection: malfind/hollow process/reflective DLL, network from memory: netscan/DNS cache, credential extraction: LSASS/Kerberos/NTLM, kernel integrity: SSDT hooks/driver analysis/rootkit detection, YARA scanning), network forensics (PCAP dissection, JA3/JA3S TLS fingerprinting, DNS tunneling/DGA detection, beaconing detection, flow analysis, lateral movement indicators: SMB/RDP/WinRM/SSH, C2 identification: Cobalt Strike/Sliver/Metasploit/Mythic), cloud forensics (AWS CloudTrail/VPC Flow/GuardDuty, Azure Activity/AD Sign-In/NSG Flow, GCP Audit, M365/Google Workspace eDiscovery, container/K8s), timeline reconstruction (super-timeline with Plaso/log2timeline, UTC normalization, gap analysis, dwell time, ATT&CK chain mapping across 14 tactics, threat actor behavioral profiling: working hours/tools/OPSEC, Diamond Model), findings consolidation & IOC summary (severity classification, attack chain cross-referencing, 9-category IOC compilation with TLP, root cause analysis), expert opinion & legal considerations (ISO 27037/NIST SP 800-86/SWGDE compliance, evidence admissibility, expert witness preparation, GDPR/HIPAA/PCI/SEC regulatory reporting), reporting & case closure (evidence disposition plan). Owned by Trace.

12. ~~**spectra-malware-analysis** (IRT)~~ — **DONE.** 10 steps, ~5,418 lines. Complete malware analysis lifecycle: sample intake & safe handling (hash computation MD5/SHA1/SHA256/ssdeep, encrypted storage, controlled environment verification, VirusTotal/MalwareBazaar initial triage), static analysis (PE: headers/sections/imports/exports/Rich header/Authenticode/PDB/.NET, ELF/Mach-O, Office: OLE/VBA macros/XLM/DDE, PDF: pdf-parser/pdfid, scripts: deobfuscation/download cradle ID, archives: ISO/IMG/VHD MotW bypass, string analysis with FLOSS, packing/entropy detection), sandbox detonation (Any.Run/Hybrid Analysis/Joe/Cape, process/filesystem/registry/network monitoring, 5-category evasion detection: VM/sandbox/anti-debug/sleep/environment), manual dynamic analysis (FlareVM/REMnux, INetSim/FakeNet-NG, ProcMon/ProcExp/Regshot/Wireshark/API Monitor/x64dbg, anti-evasion countermeasures, multi-stage payload extraction, C2 protocol analysis), behavioral profile & capability mapping (9 ATT&CK capability categories: recon through impact, malware type classification, sophistication assessment, configuration extraction), code analysis & reverse engineering (Ghidra/IDA/Binary Ninja/radare2, decryption routines, cryptographic analysis, code similarity: BinDiff/Diaphora/SSDC, shellcode analysis), IOC extraction & detection signatures (comprehensive IOC compilation, YARA 3-tier: hash/string/structural, Sigma rules for host indicators, Suricata rules for network, STIX 2.1 packaging), attribution & campaign assessment (Diamond Model, 4-level confidence framework, campaign context, geographic/sector targeting), remediation & Purple Team feedback (detection deployment, evasion techniques handoff, TI dissemination), reporting & case closure. Owned by Scalpel.

13. ~~**spectra-threat-intel-workflow** (IRT)~~ — **DONE.** 8 steps, ~4,421 lines. Structured threat intelligence production lifecycle: intelligence requirement definition (PIRs/SIRs, 5 trigger types: incident/IOC/advisory/RFI/proactive, Admiralty Scale A-F/1-6 source reliability, tactical/operational/strategic classification), collection & processing (7 source categories: OSINT news/blogs/social/paste/repos, commercial feeds Recorded Future/Mandiant/CrowdStrike/Microsoft, ISAC/CERT, government CISA/FBI/NSA/NCSC/ANSSI/BSI, internal SIEM/EDR/SOC/IR/forensics, dark web/underground, technical samples/pcaps/logs — processing with normalization/dedup/source tagging/temporal ordering/cross-reference), threat actor profiling (vendor naming cross-reference APT29=Cozy Bear=Nobelium=Midnight Blizzard, profile: motivation/capability/intent/history/TTPs ATT&CK mapped/infrastructure/victimology, attribution confidence with alternative hypotheses), Diamond Model analysis (adversary operator vs sponsor/capability/infrastructure/victim, meta-features: timestamp/phase/result/direction/methodology/resources, activity threading, pivot analysis: infrastructure/capability/victim pivots), Kill Chain & ATT&CK mapping (Lockheed Martin 7-phase + Unified Kill Chain 18-phase, per-technique mapping with Navigator layer JSON, campaign analysis: timeline/targeting/evolution/links), intelligence assessment (ACH Analysis of Competing Hypotheses, key assumptions check, indicators & warnings, red hat analysis, confidence calibration High/Moderate/Low, predictive assessment with impact scenarios, actionable intelligence "so what/who cares/what now"), IOC packaging (STIX 2.1 bundle: Threat Actor/Campaign/Indicator/Malware/Attack Pattern/Relationship/Sighting objects, Sigma/YARA/Suricata/KQL/SPL detection content, TLP WHITE/GREEN/AMBER/RED classification), dissemination with 3-tier products tactical/operational/strategic per audience. Owned by Oracle. **IRT MODULE COMPLETE (4/4 workflows).**

14. ~~**spectra-compliance-audit** (GRC)~~ — **DONE.** 7 steps, ~4,064 lines. Structured compliance audit lifecycle: audit scope & methodology (6 audit types: certification/regulatory/internal/M&A/incident-driven/client request, 8 frameworks: ISO 27001:2022/SOC 2 TSC/PCI DSS v4.0/HIPAA Security Rule/GDPR/NIST CSF 2.0/NIST 800-53 Rev 5/CIS Controls v8, assessment approach: full/focused/gap/readiness, evidence requirements, sampling methodology), control mapping & applicability (framework-specific enumeration: ISO 93 Annex A controls/SOC 2 CC1-CC9+criteria/PCI 12 requirements/HIPAA Administrative-Physical-Technical safeguards/NIST 800-53 20 families/NIST CSF 6 functions/CIS 18 controls with IG1-3, Statement of Applicability, cross-framework mapping table, shared responsibility model for cloud), evidence collection & validation (4 evidence types: documentary/technical/interview/observation, 5-dimension quality assessment: currency/completeness/accuracy/relevance/sufficiency, evidence catalog with gap tracking, technical validation: CIS benchmarks/vuln scans/pen test/access reviews), gap analysis & finding classification (per-control C/PC/NC/N-A assessment, finding classification Critical/High/Medium/Low/Informational, FIND-NNN documentation, compliance scoring with trend analysis and peer benchmarking), remediation planning (per-finding: immediate/short 0-90d/medium 90-180d/long 180+d, compensating controls with sunset dates, phased roadmap P0-P3 with RACI, continuous compliance PDCA/KPIs/automated monitoring), cross-framework analysis (unified control matrix, efficiency: overlap %/evidence reuse %/effort reduction, gap reconciliation, multi-framework dashboard), reporting & audit closure. Owned by Auditor.

15. ~~**spectra-policy-lifecycle** (GRC)~~ — **DONE.** 7 steps, ~4,267 lines. Complete security policy lifecycle: policy requirement & scope (6 triggers: new/review/gap/regulatory/org-change/framework, policy type hierarchy: Policy=high-level mandatory/Standard=specific requirements/Procedure=step-by-step/Guideline=recommended, scope: departments/systems/audience/jurisdictional, framework alignment to ISO 27001/NIST 800-53/SOC 2/PCI DSS, stakeholder identification: owner/author/reviewers/approver), research & benchmarking (5 domains: existing landscape/industry SANS-NIST-CIS-ISO 27002/regulatory per jurisdiction/threat landscape/technology context), policy drafting (10-section structure, RFC 2119 language framework SHALL/SHOULD/MAY, plain language Flesch 60-70, active voice, specific & measurable, enforceable only, technology-neutral), stakeholder review (5 categories: technical/legal/business/HR/usability, review package/assignments/tracking/sign-off, conflict resolution), approval & publication (version management major.minor, publication/distribution, awareness & training per audience, acknowledgment tracking, implementation support with technical enforcement), enforcement & exception management (automated: DLP/IAM/CASB/endpoint, manual/detective/corrective controls, compliance KPIs, exception lifecycle with risk assessment/time-limited/compensating controls, violation handling: inadvertent/negligent/willful with HR partnership), review & maintenance (annual + 10 trigger events, minor/major/emergency/retirement processes, policy metrics). Owned by Scribe. **GRC MODULE COMPLETE (3/3 workflows).**

**ALL 16 WORKFLOWS COMPLETE. ALL 4 MODULES COMPLETE (RTK 5/5, SOC 4/4, IRT 4/4, GRC 3/3).** v0.1.0 FEATURE COMPLETE.

### Things to build after workflows:

7. ~~**spectra_init.py**~~ — **DONE.** Python config loader with 4 subcommands: load/check/write/resolve-defaults. Tested. Includes core-module.yaml + module.yaml for rtk/soc/irt/grc.

8. ~~**Framework reference data**~~ — **DONE.** JSON/YAML in core/frameworks/:
   - mitre-attack/techniques.json (14 tactics, 28 techniques)
   - nist/800-53-controls.json (8 families, 18 controls)
   - owasp/top10.json (10 entries)
   - sigma-rules/templates/detection-templates.yaml (10 rules)

9. ~~**Execution scripts**~~ — **DONE.** Python in core/execution/:
   - scope-enforcer.py (259 lines, scope verification)
   - evidence-logger.py (341 lines, chain of custody)
   - tools-registry.yaml (361 lines, 44 tools in 9 categories)

**v0.1.0 FEATURE COMPLETE.** All workflows, core skills, execution scripts, and framework reference data built.

## Non-Negotiable Principles

1. **Agent Autonomy Protocol** mandatory in EVERY step file — agents are the operator's instrument, not gatekeepers. REFUSE only for destructive payloads (ransomware, wipers, data destroyers). WARN + COMPLY for everything else (technique choices, scope questions, tactical decisions). The operator is the professional who decides. The agent advises, never blocks (except destructive payloads). Always propose alternatives when warning.
2. **Engagement context** mandatory — no operation without authorization. RoE is a documentation and accountability tool, not a blocking mechanism. It records decisions and provides audit trail, but does not prevent the operator from executing.
3. **Quality = BMAD level** — if the recon has 3196 lines and 10 steps, new workflows must be comparable
4. **Manifest consistency** — every skill in the CSV must have a SKILL.md. Verify after every batch
5. **A/W/C menu** (not A/P/C like BMAD) — Advanced / War Room / Continue
6. **Communication language is configurable via config.yaml** — set `communication_language` and `document_output_language` in module configs
7. **"Read fully and follow"** — mandatory pattern for every step transition
8. **Append-only** — documents built by appending, never rewriting
9. **Frontmatter as state** — stepsCompleted, inputDocuments, engagement_id
10. **Chronicle writes for all** — after every workflow, recommend Chronicle for documentation
