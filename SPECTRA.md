# SPECTRA — Security Protocol Engineering for Cyber Threat Response & Assessment

> "Attack. Defend. Evolve."

## What is SPECTRA

Multi-agent framework for cybersecurity operations, modeled on BMAD architecture. 21 AI agents with full persona, organized into 4 operational modules + core. Each agent is a domain professional who DOES the work (writes exploits, creates detection rules, conducts forensics), not just plans it.

## Architecture

```
_spectra/
├── core/          Engagement framework, War Room, init, help, Specter (CISO), Chronicle (doc writer)
├── rtk/ 🔴        Red Team Kit — 6 offensive agents (Viper, Ghost, Razor, Phantom, Mirage, Blade)
├── soc/ 🔵        Security Operations — 6 defensive agents (Commander, Watchdog, Tracker, Hawk, Sentinel, Shield)
├── irt/ 🟠        Incident Response — 5 reactive agents (Dispatch, Trace, Scalpel, Oracle, Surge)
└── grc/ ⚪        Governance, Risk & Compliance — 3 strategic agents (Arbiter, Auditor, Scribe)
```

## Key Patterns

1. **Engagement Framework** — Every operation requires an engagement.yaml with scope, RoE, authorization. This context propagates to all agents.
2. **War Room** — Enhanced Party Mode with Disagreement Protocol (Red vs Blue adversarial).
3. **Context Budget System** — Adapts step granularity to model (Opus/Sonnet/Haiku).
4. **Kill Chain State Machine** — engagement-status.yaml tracks progress per ATT&CK phase.
5. **Agent Autonomy** — Agents HARD BLOCK destructive payloads only (ransomware, wipers). Everything else: WARN + COMPLY. The operator decides.
6. **Persona Carrythrough** — The persona stays active when invoking sub-skills.
7. **Step-File Architecture** — JIT loading, "read fully and follow", append-only, frontmatter state.

## Current Status (v0.1.0) — FEATURE COMPLETE

### Complete and operational:
- All 21 agents with SKILL.md + bmad-skill-manifest.yaml
- Complete manifests (agent-manifest.csv, skill-manifest.csv, manifest.yaml)
- Config per module with context budget (all configs set to English)
- Engagement template with kill chain + detection coverage
- Core: spectra-init, spectra-help, spectra-war-room (3 steps), spectra-new-engagement (3 steps), spectra-debrief
- Core: spectra-report-generator (~613 lines), spectra-evidence-chain (~525 lines), spectra-scope-check (~312 lines), spectra-close-engagement (~349 lines), spectra-executive-brief (~412 lines) — 5 core skills with embedded templates, schemas, and protocols
- Core: spectra_init.py (Python config loader, 4 subcommands: load/check/write/resolve-defaults, tested) + core-module.yaml
- Module definitions: rtk/module.yaml, soc/module.yaml, irt/module.yaml, grc/module.yaml (interactive config questions)
- Framework reference data: mitre-attack/techniques.json (14 tactics, 98 techniques), nist/800-53-controls.json (20 families, 54 controls), sigma-rules/templates/detection-templates.yaml (35 rules), owasp/top10.json (10 entries), cis/controls-v8.json (18 controls, 72 safeguards), cross-mapping/attack-nist-mapping.json (40 technique mappings)
- Execution scripts: scope-enforcer.py (259 lines, scope verification), evidence-logger.py (341 lines, chain of custody), tools-registry.yaml (361 lines, 44 tools in 9 categories)
- Validation framework: validate-spectra.py (968 lines, 1,459 checks across 4 severity tiers — 0 failures, 0 warnings)
- CLI installer: npx spectra-method install/validate/status/update (package.json, spectra-cli.js, installer.js)
- E2E integration testing: 8/8 tests passed (config loading, scripts, framework data, workflow continuity, cross-refs, manifests, CLI, validator)
- Distribution: package.json (spectra-method@0.1.0), README.md, LICENSE (MIT), CHANGELOG.md, .npmignore — npm pack ready (1.4 MB, 312 files)
- RTK: spectra-external-recon (10 steps, ~3,289 lines — flagship workflow)
- RTK: spectra-initial-access (10 steps, ~3,852 lines — full kill chain from recon to foothold)
- SOC: spectra-alert-triage (7 steps, ~2,687 lines — first Blue Team workflow, includes Purple Team bridge)
- SOC: spectra-detection-lifecycle (7 steps, ~3,523 lines — Red↔Blue bridge, Sigma/YARA rule authoring, test-driven detection engineering)
- SOC: spectra-phishing-response (8 steps, ~3,919 lines — full phishing incident response lifecycle: email intake, header analysis (SPF/DKIM/DMARC/ARC, Received chain, originating infrastructure), content & payload analysis (HTML/plaintext comparison, social engineering technique ID, URL detonation/redirect chain, attachment static/dynamic analysis, payload classification), IOC extraction & enrichment (multi-source TI, ATT&CK T1566.* mapping), scope & impact assessment (mail flow analysis, 5-tier user interaction funnel, endpoint assessment, campaign scope, regulatory notification), containment & eradication (email quarantine/purge, sender/domain/URL blocking, account lockdown with MFA/OAuth/mailbox rule audit, endpoint isolation), detection & prevention (gateway rules, Sigma/YARA/Suricata, awareness communications, Purple Team feedback), reporting & closure)
- SOC: spectra-threat-hunt (8 steps, ~3,455 lines — hypothesis-driven threat hunting lifecycle: hunt mission definition (6 trigger types), hypothesis development (ATT&CK-based, testability criteria, data source matrix, null hypothesis), data collection & preparation (SPL/KQL/EQL/Sigma queries, baseline establishment), automated analysis (frequency/stack ranking/time-series/clustering/long-tail), manual analysis (LOLBin detection, lateral movement traces, persistence, credential access, TTP matching), finding validation (evidence correlation, timeline reconstruction, 4-tier classification, hypothesis verdict), detection engineering (Sigma/YARA/Suricata, hunt playbooks, ATT&CK coverage delta, Purple Team), reporting with SQRRL maturity assessment). **SOC MODULE COMPLETE (4/4 workflows).**
- IRT: spectra-incident-handling (10 steps, ~6,874 lines — NIST 800-61 full lifecycle: intake, detection, triage, containment, evidence preservation, deep analysis, eradication, recovery, post-incident review, closure)
- IRT: spectra-digital-forensics (10 steps, ~5,324 lines — complete digital forensic investigation lifecycle: case intake & evidence receipt (EVD-NNN chain of custody, legal context, case classification), evidence acquisition & preservation (RFC 3227 order of volatility, disk imaging with write blockers, memory capture, cloud evidence, working copy creation), disk forensics (NTFS/ext4/APFS, $MFT/$UsnJrnl/ADS, Windows artifacts: Registry/EventLog/Prefetch/Amcache/ShimCache/SRUM/BAM, Linux/macOS artifacts, browser/email/messaging forensics, anti-forensics detection), memory forensics (Volatility 3, process analysis: pslist/psscan/pstree comparison, code injection detection: malfind/hollow process/reflective DLL, network from memory, credential extraction, kernel integrity: SSDT/drivers/rootkits, YARA scanning), network forensics (PCAP dissection, JA3/JA3S TLS fingerprinting, DNS tunneling/DGA detection, beaconing detection, lateral movement indicators, C2 identification), cloud forensics (AWS CloudTrail/VPC Flow/GuardDuty, Azure Activity/AD Sign-In/NSG Flow, GCP Audit, M365/Google Workspace, container/K8s), timeline reconstruction (super-timeline with Plaso, ATT&CK chain mapping, dwell time, threat actor behavioral profiling, Diamond Model), findings consolidation & IOC summary (TLP classification), expert opinion & legal considerations (ISO 27037/NIST SP 800-86/SWGDE, evidence admissibility, regulatory reporting), reporting & case closure)
- IRT: spectra-malware-analysis (10 steps, ~5,418 lines — complete malware analysis lifecycle: sample intake & safe handling (hash computation, encrypted storage, VirusTotal/MalwareBazaar triage), static analysis (PE headers/sections/imports/exports/Rich header/certificates/.NET, ELF/Mach-O, Office macros OLE/VBA/XLM, PDF analysis, script deobfuscation, string analysis with FLOSS, packing detection), sandbox detonation (Any.Run/Hybrid Analysis/Joe/Cape, process/filesystem/registry/network monitoring, evasion detection: VM/sandbox/anti-debug/sleep), manual dynamic analysis (FlareVM/REMnux, ProcMon/ProcExp/Regshot/Wireshark/API Monitor/x64dbg, anti-evasion countermeasures, multi-stage payload extraction, C2 protocol analysis), behavioral profile & capability mapping (9 ATT&CK capability categories, malware classification, sophistication assessment, configuration extraction), code analysis & reverse engineering (Ghidra/IDA/Binary Ninja, decryption routines, crypto analysis, code similarity: BinDiff/Diaphora, shellcode analysis), IOC extraction & detection signatures (YARA 3-tier rules, Sigma rules, Suricata rules, STIX 2.1 packaging), attribution & campaign assessment (Diamond Model, 4-level confidence framework, campaign context), remediation & Purple Team feedback, reporting & case closure)
- GRC: spectra-risk-assessment (7 steps, ~7,075 lines — NIST 800-30/FAIR hybrid: assessment scoping, Crown Jewels Analysis, threat identification (NIST D-2/E-2/E-3), vulnerability & predisposing conditions, risk calculation (qualitative + FAIR quantitative ALE), treatment planning with ROI, executive reporting & closure)
- RTK: spectra-privesc (10 steps, ~4,327 lines — full privilege escalation lifecycle: foothold assessment, local enumeration, credential discovery, Windows privesc (token abuse, UAC bypass, service exploitation, kernel), Linux privesc (SUID, sudo, capabilities, container escape), AD escalation (Kerberoasting, delegation, ADCS, DCSync), Cloud escalation (AWS/Azure/GCP IAM, metadata, K8s), exploit chaining with evasion integration, verification, and lateral movement handoff)
- RTK: spectra-lateral-movement (10 steps, ~7,853 lines — full lateral movement lifecycle: access ingestion & operational planning, internal network reconnaissance (passive/active scanning, service enumeration, trust mapping, target prioritization), credential operations (LSASS/SAM/NTDS extraction, PtH/PtT/OPtH, NTLM relay setup, credential→target mapping), Windows lateral (PsExec/WMI/WinRM/DCOM/RDP/scheduled tasks), Linux lateral (SSH/Ansible/Puppet/container pivoting/NFS), AD lateral (GPO deployment, Kerberos ticket forging, delegation abuse, trust hopping, ADCS, DCShadow), Cloud lateral (AWS/Azure/GCP cross-account, K8s pod-to-pod, multi-cloud pivoting), network pivoting & tunneling (SSH/SOCKS/chisel/ligolo/covert channels/C2 integration), access verification & persistence, reporting with exfiltration handoff)
- RTK: spectra-exfiltration (10 steps, ~9,618 lines — largest SPECTRA workflow. Full data exfiltration lifecycle: objective ingestion & exfiltration planning (explicit RoE authorization, data handling requirements, DLP posture assessment), target data discovery (file shares/databases/email/repos/secrets/cloud storage/backups with Varonis/DAM-aware OPSEC), data assessment & classification (L1-L4 sensitivity framework, GDPR/HIPAA/PCI/SOX regulatory mapping, RoE compliance matrix, feasibility analysis), data collection & staging (compression/encryption/chunking with AES-256/age/GPG, staging infrastructure), network exfiltration (HTTP/HTTPS/domain fronting, DNS tunneling, FTP/SFTP, email, C2 channels, ICMP/WebSocket), cloud exfiltration (S3/Blob/GCS, SaaS OneDrive/SharePoint/Google Drive, cross-account replication, serverless Lambda/Functions), covert channel exfiltration (steganography, protocol manipulation, dead drops, physical/USB/Bluetooth, air-gap bridging), DLP & monitoring evasion (content inspection bypass, protocol evasion, endpoint DLP bypass, CASB evasion, adaptive response), verification & cleanup (integrity verification, evidence chain EX-NNN, staging cleanup, persistence removal, OPSEC final assessment, secure data handling), reporting & engagement closure (DLP assessment report, cross-phase engagement summary, SOC Purple Team handoff, data handling commitment))

- IRT: spectra-threat-intel-workflow (8 steps, ~4,421 lines — structured threat intelligence production: intelligence requirements (PIRs/SIRs, Admiralty Scale), collection (7 source categories), threat actor profiling (Diamond Model attribution), Kill Chain & ATT&CK mapping (Navigator layer), intelligence assessment (ACH, red hat, confidence calibration), IOC packaging (STIX 2.1, Sigma/YARA/Suricata), dissemination (3-tier products)). **IRT MODULE COMPLETE (4/4 workflows).**
- GRC: spectra-compliance-audit (7 steps, ~4,064 lines — structured compliance audit: scope & methodology (8 frameworks), control mapping (SoA, cross-framework), evidence collection (4 types, 5-dimension quality), gap analysis (FIND-NNN, compliance scoring), remediation (phased roadmap, PDCA), cross-framework efficiency, reporting)
- GRC: spectra-policy-lifecycle (7 steps, ~4,267 lines — complete policy lifecycle: requirement & scope (policy/standard/procedure/guideline hierarchy), research & benchmarking, drafting (RFC 2119), stakeholder review (5 categories), approval & publication, enforcement & exceptions, review & maintenance). **GRC MODULE COMPLETE (3/3 workflows).**

**ALL 16 WORKFLOWS COMPLETE. ALL 4 MODULES COMPLETE.**

### To be completed:
- v0.1.0 COMPLETE AND VALIDATED. Future v0.2.0 targets: full ATT&CK matrix (1000+ techniques from MITRE STIX data), expanded NIST (all enhancements), production Sigma library (100+ rules from SigmaHQ), SIEM integration connectors, automated reporting pipeline

## How to Continue Development

1. Read this file for context
2. Read `_spectra/DEV-GUIDE.md` for exact file formats, patterns, and development principles
3. Read `_spectra/_config/skill-manifest.csv` for skill status
4. **ALL 16 WORKFLOWS COMPLETE.** RTK 5/5, SOC 4/4, IRT 4/4, GRC 3/3.
5. ~~**ALL 5 CORE SKILLS COMPLETE.**~~ DONE. report-generator, evidence-chain, scope-check, close-engagement, executive-brief
6. ~~**Execution scripts**~~ DONE. spectra_init.py, scope-enforcer.py, evidence-logger.py, tools-registry.yaml + module.yaml configs
7. ~~**Framework reference data**~~ DONE. ATT&CK (14 tactics, 98 techniques), NIST 800-53 (20 families, 54 controls), Sigma (35 rules), OWASP Top 10, CIS Controls v8 (18 controls, 72 safeguards), cross-mapping (40 technique mappings)
8. **v0.1.0 COMPLETE AND VALIDATED.** All integration tests pass, validator clean, npm pack ready. v0.2.0 targets: full ATT&CK matrix, expanded Sigma library, SIEM connectors, automated reporting
9. **Always run validator before committing**: python3 core/execution/validate-spectra.py --path _spectra/
10. Use spectra-external-recon, spectra-risk-assessment, or spectra-digital-forensics as reference for quality and depth

## Development Principles

- Replicate BMAD's winning patterns, not its numbers
- Every step file must be as complete as BMAD's (emoji rules, A/W/C menu, success/failure metrics)
- Agents HARD BLOCK destructive payloads only; WARN + COMPLY on everything else — the operator decides
- Agent Autonomy Protocol mandatory in every step file
- Chronicle (core) writes documentation for ALL modules
- The report IS the deliverable — an assessment without a report is just hacking
