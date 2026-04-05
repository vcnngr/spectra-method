<p align="center">
  <img src="https://img.shields.io/npm/v/spectra-method.svg?style=flat-square&color=red" alt="npm version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License: MIT">
  <img src="https://img.shields.io/badge/agents-21-blue?style=flat-square" alt="21 agents">
  <img src="https://img.shields.io/badge/workflows-16-orange?style=flat-square" alt="16 workflows">
  <img src="https://img.shields.io/badge/lines-80K%2B-green?style=flat-square" alt="80K+ lines">
</p>

<h1 align="center">S P E C T R A</h1>

<p align="center">
  <strong>Security Protocol Engineering for Cyber Threat Response & Assessment</strong>
</p>

<p align="center">
  <em>"Attack. Defend. Evolve."</em>
</p>

<p align="center">
  21 AI agents. 16 structured workflows. 80,000+ lines of operational security knowledge.<br>
  A complete cybersecurity team — instantly available in your AI IDE.
</p>

---

## What is SPECTRA?

SPECTRA is a **multi-agent operating system for cybersecurity operations**. Not a chatbot. Not a wrapper for existing tools. A full team of specialized professionals — each with their own identity, expertise, and opinions.

When **Viper** (Red Team Lead) and **Commander** (SOC Manager) look at the same target, they see different things. Put them in a **War Room** together, and they *clash* — producing insights neither would reach alone.

```bash
npx spectra-method install --tools claude-code -y
```

## Modules

| Module | | Agents | Workflows | Focus |
|--------|---|--------|-----------|-------|
| **RTK** | :red_circle: | 6 | 5 | Red Team — recon, exploitation, lateral movement, exfiltration |
| **SOC** | :large_blue_circle: | 6 | 4 | Security Operations — triage, hunting, detection engineering |
| **IRT** | :orange_circle: | 5 | 4 | Incident Response — forensics, malware analysis, threat intel |
| **GRC** | :white_circle: | 3 | 3 | Governance, Risk & Compliance — risk, audit, policy |
| **Core** | :zap: | 2 | 10 skills | Engagement framework, War Room, reporting |

---

## Quick Start

```bash
# Full install
npx spectra-method install \
  --tools claude-code \
  --user-name "YourName" \
  --communication-language "English" \
  -y

# Then in your AI IDE:
/spectra-help                    # See what's available
/spectra-new-engagement          # Create a scoped engagement
/spectra-agent-red-lead          # Talk to Viper
/spectra-war-room                # Launch Red vs Blue debate
```

---

## The Agents

### Core :zap:

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Specter** | CISO | Cross-domain oversight, strategic coordination |
| **Chronicle** | Documentation Specialist | Writes reports for ALL modules with full context |

### RTK :red_circle: Red Team Kit

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Viper** | Red Team Lead | Attack strategy, engagement planning |
| **Ghost** | Recon Specialist | OSINT, passive/active reconnaissance |
| **Razor** | Exploit Developer | Vulnerability research, exploit chains |
| **Phantom** | Attack Operator | Post-exploitation, lateral movement, evasion |
| **Mirage** | Social Engineer | Phishing, pretexting, awareness testing |
| **Blade** | Quick Pentester | Rapid vulnerability assessment |

### SOC :large_blue_circle: Security Operations

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Commander** | SOC Manager | Operations, metrics, escalation management |
| **Watchdog** | L1 Triage | Alert classification, IOC enrichment |
| **Tracker** | L2 Investigator | Event correlation, phishing response |
| **Hawk** | L3 Threat Hunter | Hypothesis-driven hunting, ATT&CK mapping |
| **Sentinel** | Detection Engineer | Sigma/YARA/Suricata rule authoring |
| **Shield** | Quick SOC Analyst | Rapid triage and investigation |

### IRT :orange_circle: Incident Response

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Dispatch** | Incident Handler | NIST 800-61 lifecycle coordination |
| **Trace** | Forensic Analyst | Disk/memory/network/cloud forensics |
| **Scalpel** | Malware Analyst | Static/dynamic analysis, reverse engineering |
| **Oracle** | Threat Intel Analyst | Diamond Model, attribution, STIX 2.1 |
| **Surge** | Quick Responder | Emergency triage and containment |

### GRC :white_circle: Governance, Risk & Compliance

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Arbiter** | Risk Analyst | NIST 800-30, FAIR, risk quantification |
| **Auditor** | Compliance Auditor | ISO 27001, SOC 2, PCI DSS, HIPAA, GDPR |
| **Scribe** | Policy Author | Policy lifecycle, RFC 2119 |

---

## Workflows

### RTK :red_circle: Kill Chain (50 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-external-recon` | 10 | OSINT, DNS, WHOIS, Shodan, port scanning |
| `spectra-initial-access` | 10 | Phishing, exploitation, credential attacks |
| `spectra-privesc` | 10 | Windows/Linux/AD/Cloud escalation |
| `spectra-lateral-movement` | 10 | PsExec, WMI, Kerberos, cloud pivoting |
| `spectra-exfiltration` | 10 | HTTP, DNS tunnel, steganography, DLP evasion |

### SOC :large_blue_circle: Detection & Response (30 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-alert-triage` | 7 | Classification, investigation, Purple Team bridge |
| `spectra-detection-lifecycle` | 7 | ATT&CK mapping, Sigma/YARA authoring |
| `spectra-phishing-response` | 8 | Header/payload analysis, IOC extraction |
| `spectra-threat-hunt` | 8 | Hypothesis-driven hunting, finding validation |

### IRT :orange_circle: Investigation (38 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-incident-handling` | 10 | NIST 800-61 full lifecycle |
| `spectra-digital-forensics` | 10 | Disk, memory, network, cloud forensics |
| `spectra-malware-analysis` | 10 | Static, dynamic, sandbox, reverse engineering |
| `spectra-threat-intel-workflow` | 8 | Diamond Model, ATT&CK, STIX 2.1 |

### GRC :white_circle: Governance (21 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-risk-assessment` | 7 | NIST 800-30/FAIR, Crown Jewels Analysis |
| `spectra-compliance-audit` | 7 | 8 frameworks, gap analysis, remediation |
| `spectra-policy-lifecycle` | 7 | Drafting, review, enforcement, exceptions |

---

## Framework Data

| Framework | Content |
|-----------|---------|
| MITRE ATT&CK | 98 techniques, 14 tactics |
| NIST 800-53 Rev 5 | 54 controls, 20 families |
| Sigma Rules | 35 detection templates |
| OWASP Top 10 | 2021 edition |
| CIS Controls v8 | 18 controls, 72 safeguards |
| Cross-mapping | 40 ATT&CK-to-NIST mappings |

---

## CLI

```
npx spectra-method install [options]

  -d, --directory <path>               Target directory (default: ".")
  -m, --modules <modules>              Module IDs: rtk,soc,irt,grc
  --tools <tools>                      IDE: claude-code (default)
  --user-name <name>                   Name for agents
  --communication-language <lang>      Agent language (default: English)
  --document-output-language <lang>    Document language (default: English)
  --output-folder <path>               Output folder (default: _spectra-output)
  -y, --yes                            Accept all defaults
  -f, --force                          Force reinstall

npx spectra-method validate            Verify installation
npx spectra-method status              Show version and modules
npx spectra-method update              Update (preserves configs)
```

---

## Architecture

```
project/
├── .claude/skills/       48 skills as slash commands
├── _spectra/             Framework: agents, workflows, configs
│   ├── core/             Engagement framework, skills, scripts
│   ├── rtk/              Red Team Kit
│   ├── soc/              Security Operations
│   ├── irt/              Incident Response
│   ├── grc/              Governance, Risk & Compliance
│   └── _config/          Manifests
└── _spectra-output/      Engagement artifacts
    ├── engagements/
    ├── reports/
    └── evidence/
```

**Agent Autonomy Protocol**: HARD BLOCK destructive payloads only (ransomware, wipers). Everything else: WARN + COMPLY. The operator decides.

---

## Requirements

- **AI IDE**: Claude Code, Cursor, or compatible
- **Python**: 3.10+
- **Node.js**: 18+

## License

MIT

---

<p align="center"><em>Built for operators. By operators.</em></p>
