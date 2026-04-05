```
  ███████╗██████╗ ███████╗ ██████╗████████╗██████╗  █████╗ 
  ██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝██��══██╗██╔══██╗
  ███████╗██████╔╝█████╗  ██║        ██║   ██████╔��███████║
  ╚════██��██╔═══╝ ██╔══╝  █��║        ██║   ██╔══██╗██╔══██║
  █��█████║██║     ███████╗╚██████╗   ██║   ██║  ██║██║  ██║
  ╚══════��╚═╝     ╚═���════╝ ╚═════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝
```

# Security Protocol Engineering for Cyber Threat Response & Assessment

> *"Attack. Defend. Evolve."*

[![npm version](https://img.shields.io/npm/v/spectra-method.svg)](https://www.npmjs.com/package/spectra-method)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/github/stars/vcnngr/spectra-method?style=social)](https://github.com/vcnngr/spectra-method)

**21 AI agents. 16 structured workflows. 80,000+ lines of operational security knowledge.**

A complete cybersecurity team — Red Team, Blue Team, Incident Response, Forensics, Risk, Compliance — available instantly in your AI IDE.

```bash
npx spectra-method install --tools claude-code -y
```

---

## What is SPECTRA?

SPECTRA is not a chatbot that answers security questions. It's a **multi-agent operating system for cybersecurity operations** where each agent is a specialist with their own identity, expertise, and opinions.

When you talk to **Viper** (Red Team Lead), he thinks like an attacker. When you switch to **Commander** (SOC Manager), he sees the same data from a defender's perspective. Put them in the same **War Room**, and they *clash* — producing insights neither would reach alone.

| Module | | Agents | Workflows | Focus |
|--------|---|--------|-----------|-------|
| **RTK** | 🔴 | 6 | 5 | Red Team — recon, exploitation, lateral movement, exfiltration |
| **SOC** | 🔵 | 6 | 4 | Security Operations — triage, hunting, detection engineering |
| **IRT** | 🟠 | 5 | 4 | Incident Response — forensics, malware analysis, threat intel |
| **GRC** | ⚪ | 3 | 3 | Governance, Risk & Compliance — risk, audit, policy |
| **Core** | ⚡ | 2 | 10 skills | Engagement framework, War Room, reporting |

---

## Quick Start

```bash
# Install with full options
npx spectra-method install \
  --tools claude-code \
  --user-name "YourName" \
  --communication-language "English" \
  --document-output-language "English" \
  -y

# Validate installation
npx spectra-method validate

# Check status
npx spectra-method status
```

Then in your AI IDE:

```
/spectra-help                    — See what's available
/spectra-new-engagement          — Create a scoped engagement
/spectra-agent-red-lead          — Talk to Viper (Red Team Lead)
/spectra-agent-soc-manager       ��� Talk to Commander (SOC Manager)
/spectra-war-room                — Launch Red vs Blue debate
```

---

## The Agents

### Core ⚡

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Specter** 👁️ | CISO | Cross-domain oversight, rapid assessment, strategic coordination |
| **Chronicle** 📖 | Documentation Specialist | Writes reports for ALL modules with full engagement context |

### RTK 🔴 Red Team Kit

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Viper** 🐍 | Red Team Lead | Attack strategy, engagement planning, team coordination |
| **Ghost** 👻 | Recon Specialist | OSINT, passive/active reconnaissance, attack surface mapping |
| **Razor** 🔪 | Exploit Developer | Vulnerability research, exploit chains, PoC development |
| **Phantom** 👤 | Attack Operator | Post-exploitation, lateral movement, persistence, evasion |
| **Mirage** 🎭 | Social Engineer | Phishing campaigns, pretexting, awareness testing |
| **Blade** ⚔️ | Quick Pentester | Rapid vulnerability assessment |

### SOC 🔵 Security Operations

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Commander** 🎖️ | SOC Manager | Operations coordination, metrics, escalation management |
| **Watchdog** 🐕 | L1 Triage | Alert classification, IOC enrichment, false positive ID |
| **Tracker** 🔍 | L2 Investigator | Event correlation, timeline reconstruction, phishing response |
| **Hawk** 🦅 | L3 Threat Hunter | Hypothesis-driven hunting, behavioral analysis, ATT&CK mapping |
| **Sentinel** 🛡️ | Detection Engineer | Sigma/YARA/Suricata rules, detection tuning, coverage mapping |
| **Shield** ⚡ | Quick SOC Analyst | Rapid triage and investigation |

### IRT 🟠 Incident Response

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Dispatch** 📡 | Incident Handler | NIST 800-61 lifecycle, coordination, stakeholder communication |
| **Trace** 🔬 | Forensic Analyst | Disk/memory/network/cloud forensics, timeline reconstruction |
| **Scalpel** 🔭 | Malware Analyst | Static/dynamic analysis, reverse engineering, YARA/STIX |
| **Oracle** 🔮 | Threat Intel Analyst | Diamond Model, ATT&CK mapping, campaign tracking, attribution |
| **Surge** ⚡ | Quick Responder | Emergency triage and containment |

### GRC ⚪ Governance, Risk & Compliance

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Arbiter** ⚖️ | Risk Analyst | NIST 800-30, FAIR, Crown Jewels Analysis, risk quantification |
| **Auditor** 📋 | Compliance Auditor | ISO 27001, SOC 2, PCI DSS, HIPAA, GDPR, NIST CSF, CIS Controls |
| **Scribe** 📜 | Policy Author | Policy lifecycle, RFC 2119, stakeholder review, enforcement |

---

## Workflows

### RTK 🔴 Kill Chain (50 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-external-recon` | 10 | OSINT, DNS, WHOIS, Shodan, port scanning, fingerprinting |
| `spectra-initial-access` | 10 | Phishing, exploitation, credential attacks, web attacks |
| `spectra-privesc` | 10 | Windows/Linux/AD/Cloud privilege escalation |
| `spectra-lateral-movement` | 10 | PsExec, WMI, SSH, Kerberos, NTLM relay, cloud pivoting |
| `spectra-exfiltration` | 10 | HTTP, DNS tunnel, cloud, steganography, DLP evasion |

### SOC 🔵 Detection & Response (30 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-alert-triage` | 7 | Classification, investigation, escalation, Purple Team bridge |
| `spectra-detection-lifecycle` | 7 | ATT&CK mapping, Sigma/YARA authoring, test-driven validation |
| `spectra-phishing-response` | 8 | Header analysis, payload analysis, IOC extraction, containment |
| `spectra-threat-hunt` | 8 | Hypothesis-driven hunting, behavioral analysis, finding validation |

### IRT 🟠 Investigation (38 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-incident-handling` | 10 | NIST 800-61 full lifecycle |
| `spectra-digital-forensics` | 10 | Disk, memory, network, cloud forensics with chain of custody |
| `spectra-malware-analysis` | 10 | Static, dynamic, sandbox, reverse engineering |
| `spectra-threat-intel-workflow` | 8 | Collection, Diamond Model, ATT&CK, STIX 2.1, dissemination |

### GRC ⚪ Governance (21 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-risk-assessment` | 7 | NIST 800-30/FAIR hybrid, Crown Jewels, risk quantification |
| `spectra-compliance-audit` | 7 | Multi-framework audit (8 frameworks), gap analysis, remediation |
| `spectra-policy-lifecycle` | 7 | Drafting, review, approval, enforcement, exception management |

---

## Framework Reference Data

| Framework | Content |
|-----------|---------|
| MITRE ATT&CK | 98 techniques across 14 tactics |
| NIST 800-53 Rev 5 | 54 controls across 20 families |
| Sigma Rules | 35 detection rule templates |
| OWASP Top 10 | 2021 edition, complete |
| CIS Controls v8 | 18 controls, 72 safeguards |
| Cross-mapping | 40 ATT&CK-to-NIST mappings |

---

## CLI Reference

```bash
npx spectra-method install [options]

Options:
  -d, --directory <path>               Installation directory (default: ".")
  -m, --modules <modules>              Comma-separated module IDs (e.g., "rtk,soc")
  --tools <tools>                      IDE targets (e.g., "claude-code"). Use "none" to skip.
  --user-name <name>                   Name for agents to use
  --communication-language <lang>      Language for agent communication (default: "English")
  --document-output-language <lang>    Language for document output (default: "English")
  --output-folder <path>               Output folder relative to project root
  --action <type>                      install | update | quick-update
  -y, --yes                            Accept all defaults
  -f, --force                          Force reinstall

npx spectra-method validate            Verify installation integrity
npx spectra-method status              Show version, modules, IDE support
npx spectra-method update              Update framework (preserves configs)
```

---

## Architecture

```
project/
├── .claude/skills/       ← 48 skills registered as slash commands
├── _spectra/             ← Framework (agents, workflows, configs)
│   ├── core/             ← Engagement framework, 10 skills, execution scripts
│   ├── rtk/ 🔴           ← Red Team Kit
│   ├── soc/ 🔵           ← Security Operations Center
│   ├── irt/ 🟠           ← Incident Response Team
│   ├── grc/ ⚪           ← Governance, Risk & Compliance
│   └── _config/          ← Manifests (agents, skills, installation)
└── _spectra-output/      ← Engagement artifacts (never committed)
    ├── engagements/
    ├── reports/
    └── evidence/
```

**Agent Autonomy Protocol**: Agents HARD BLOCK destructive payloads only (ransomware, wipers). Everything else: WARN + COMPLY — the operator decides.

---

## Requirements

- **AI IDE**: Claude Code, Cursor, or compatible environment
- **Python**: 3.10+ (for config and execution scripts)
- **Node.js**: 18+ (for CLI installer)

## License

MIT

---

*Built for operators. By operators.*
