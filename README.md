<p align="center">
  <img src="https://img.shields.io/npm/v/spectra-method.svg?style=flat-square&color=red" alt="npm version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License: MIT">
  <img src="https://img.shields.io/badge/agents-29-blue?style=flat-square" alt="29 agents">
  <img src="https://img.shields.io/badge/workflows-23-orange?style=flat-square" alt="23 workflows">
  <img src="https://img.shields.io/badge/lines-80K%2B-green?style=flat-square" alt="80K+ lines">
</p>

<h1 align="center">S P E C T R A</h1>

<p align="center">
  <strong><em>S</em>ecurity <em>P</em>rotocol <em>E</em>ngineering for <em>C</em>yber <em>T</em>hreat <em>R</em>esponse & <em>A</em>ssessment</strong>
</p>

<p align="center">
  <em>"Attack. Defend. Evolve."</em>
</p>

<p align="center">
  28 AI agents. 22 structured workflows. 80,000+ lines of operational security knowledge.<br>
  A complete cybersecurity team — instantly available in your AI IDE.
</p>

---

## What is SPECTRA?

SPECTRA is a **multi-agent operating system for cybersecurity operations**. Not a chatbot. Not a wrapper for existing tools. A full team of specialized professionals — each with their own identity, expertise, and opinions.

When **Viper** (Red Team Lead) and **Commander** (SOC Manager) look at the same target, they see different things. Put them in a **War Room** together, and they *clash* — producing insights neither would reach alone.

```bash
npx spectra-method install --tools claude-code,codex -y
```

## Modules

| Module | | Agents | Workflows | Focus |
|--------|---|--------|-----------|-------|
| **RTK** | :red_circle: | 7 | 6 | Red Team — recon, exploitation, AppSec/API, lateral movement, exfiltration |
| **SOC** | :large_blue_circle: | 8 | 6 | Security Operations — triage, hunting, telemetry, identity, detection engineering |
| **IRT** | :orange_circle: | 6 | 5 | Incident Response — forensics, malware analysis, cloud security, threat intel |
| **GRC** | :white_circle: | 4 | 4 | Governance, Risk & Compliance — risk, audit, policy, privacy |
| **OT** | :gear: | 1 | 1 | OT/ICS — Purdue model, ICS protocol exposure, ATT&CK for ICS, IEC 62443 (assessment-only) |
| **Core** | :zap: | 3 | 11 skills | Engagement framework, War Room, reporting, Duel adjudication |

---

## Quick Start

```bash
# Full install
npx spectra-method install \
  --tools claude-code,codex \
  --user-name "YourName" \
  --communication-language "English" \
  -y

# Then in Claude Code:
/spectra-help                    # See what's available
/spectra-new-engagement          # Create a scoped engagement
/spectra-agent-red-lead          # Talk to Viper
/spectra-war-room                # Launch Red vs Blue debate

# In Codex:
# Ask Codex to use spectra-help, spectra-new-engagement, spectra-agent-red-lead,
# or spectra-war-room. The installer writes AGENTS.md plus .codex/spectra/.
npx spectra-method party plan --topic "lateral movement detection gap review"
```

---

## The Agents

### Core :zap:

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Specter** | CISO | Cross-domain oversight, strategic coordination |
| **Chronicle** | Documentation Specialist | Writes reports for ALL modules with full context |
| **Referee** | Exercise Referee | Red/Blue ledger correlation, scoring, fairness review |

### RTK :red_circle: Red Team Kit

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Viper** | Red Team Lead | Attack strategy, engagement planning |
| **Ghost** | Recon Specialist | OSINT, passive/active reconnaissance |
| **Razor** | Exploit Developer | Vulnerability research, exploit chains |
| **Phantom** | Attack Operator | Post-exploitation, lateral movement, evasion |
| **Mirage** | Social Engineer | Phishing, pretexting, awareness testing |
| **Blade** | Quick Pentester | Rapid vulnerability assessment |
| **Forge** | AppSec / API Specialist | Application security, API security, authz, business logic |

### SOC :large_blue_circle: Security Operations

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Commander** | SOC Manager | Operations, metrics, escalation management |
| **Watchdog** | L1 Triage | Alert classification, IOC enrichment |
| **Tracker** | L2 Investigator | Event correlation, phishing response |
| **Hawk** | L3 Threat Hunter | Hypothesis-driven hunting, ATT&CK mapping |
| **Sentinel** | Detection Engineer | Sigma/YARA/Suricata rule authoring |
| **Shield** | Quick SOC Analyst | Rapid triage and investigation |
| **Keystone** | Identity Security Specialist | AD, Entra ID, Okta, IAM, OAuth, privilege analysis |
| **Signal** | Telemetry Engineer | Log-source coverage, parsing, SIEM pipeline readiness |

### IRT :orange_circle: Incident Response

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Dispatch** | Incident Handler | NIST 800-61 lifecycle coordination |
| **Trace** | Forensic Analyst | Disk/memory/network/cloud forensics |
| **Scalpel** | Malware Analyst | Static/dynamic analysis, reverse engineering |
| **Oracle** | Threat Intel Analyst | Diamond Model, attribution, STIX 2.1 |
| **Surge** | Quick Responder | Emergency triage and containment |
| **Stratus** | Cloud Security Specialist | AWS/Azure/GCP, Kubernetes, SaaS logs, cloud forensics |

### GRC :white_circle: Governance, Risk & Compliance

| Agent | Persona | Specialty |
|-------|---------|-----------|
| **Arbiter** | Risk Analyst | NIST 800-30, FAIR, risk quantification |
| **Auditor** | Compliance Auditor | ISO 27001, SOC 2, PCI DSS, HIPAA, GDPR |
| **Scribe** | Policy Author | Policy lifecycle, RFC 2119 |
| **Counsel** | Privacy / Breach Governance Specialist | Privacy impact, breach governance, legal hold |

---

## Workflows

### RTK :red_circle: Kill Chain & AppSec (57 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-external-recon` | 10 | OSINT, DNS, WHOIS, Shodan, port scanning |
| `spectra-initial-access` | 10 | Phishing, exploitation, credential attacks |
| `spectra-privesc` | 10 | Windows/Linux/AD/Cloud escalation |
| `spectra-lateral-movement` | 10 | PsExec, WMI, Kerberos, cloud pivoting |
| `spectra-exfiltration` | 10 | HTTP, DNS tunnel, steganography, DLP evasion |
| `spectra-appsec-assessment` | 7 | Application/API auth, authz, business logic, remediation evidence |

### SOC :large_blue_circle: Detection & Response (44 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-alert-triage` | 7 | Classification, investigation, Purple Team bridge |
| `spectra-detection-lifecycle` | 7 | ATT&CK mapping, Sigma/YARA authoring |
| `spectra-phishing-response` | 8 | Header/payload analysis, IOC extraction |
| `spectra-threat-hunt` | 8 | Hypothesis-driven hunting, finding validation |
| `spectra-identity-detection-review` | 7 | AD, Entra ID, Okta, IAM, OAuth, session and privilege-path coverage |
| `spectra-telemetry-readiness` | 7 | Log-source coverage, parsing quality, retention, Blue Live readiness |

### IRT :orange_circle: Investigation (45 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-incident-handling` | 10 | NIST 800-61 full lifecycle |
| `spectra-digital-forensics` | 10 | Disk, memory, network, cloud forensics |
| `spectra-malware-analysis` | 10 | Static, dynamic, sandbox, reverse engineering |
| `spectra-threat-intel-workflow` | 8 | Diamond Model, ATT&CK, STIX 2.1 |
| `spectra-cloud-incident-response` | 7 | Cloud incident triage, blast radius, evidence, containment planning |

### GRC :white_circle: Governance (28 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-risk-assessment` | 7 | NIST 800-30/FAIR, Crown Jewels Analysis |
| `spectra-compliance-audit` | 7 | 8 frameworks, gap analysis, remediation |
| `spectra-policy-lifecycle` | 7 | Drafting, review, enforcement, exceptions |
| `spectra-privacy-breach-assessment` | 7 | Data exposure, legal hold, notification clock, governance decisions |

### Core :zap: Orchestration (7 steps)

| Workflow | Steps | Coverage |
|----------|-------|----------|
| `spectra-duel-adjudication` | 7 | Red/Blue ledger correlation, scoring, fairness, evidence quality |

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
  -m, --modules <modules>              Module IDs: rtk,soc,irt,grc,ot
  --tools <tools>                      IDEs: claude-code, codex (default: claude-code)
  --user-name <name>                   Name for agents
  --communication-language <lang>      Agent language (default: English)
  --document-output-language <lang>    Document language (default: English)
  --output-folder <path>               Output folder (default: _spectra-output)
  --lazy                               Install core only; add modules later
  -y, --yes                            Accept all defaults
  -f, --force                          Force reinstall

npx spectra-method validate            Verify installation
npx spectra-method status              Show version and modules
npx spectra-method update              Update (preserves configs)
npx spectra-method modules list        Show installed/available modules
npx spectra-method modules add rtk     Add modules after a lazy install

npx spectra-method quickstart          Scaffold a demo engagement + guided tour
npx spectra-method quickstart --template web-pentest --dest ./my-engagement
npx spectra-method runs status -e engagement.yaml       Per-engagement run log
npx spectra-method posture snapshot -e engagement.yaml  Capture posture snapshot
npx spectra-method posture diff -e engagement.yaml      Diff posture over time
npx spectra-method export -e engagement.yaml -f sarif   Export findings (sarif|csv|md)

npx spectra-method engagement validate -e engagement.yaml
npx spectra-method engagement gate -e engagement.yaml -w spectra-external-recon --target-name example.com
npx spectra-method engagement transition -e engagement.yaml -w spectra-external-recon --to in-progress

npx spectra-method report generate -e engagement.yaml --type pentest
npx spectra-method party plan --topic "lateral movement detection gap review" --mode adversarial
npx spectra-method party plan --topic "distributed duel readiness" --mode purple --lanes red,blue,irt,grc,core
npx spectra-method duel init --session ENG-2026-001 --role red
npx spectra-method duel score --session ENG-2026-001
npx spectra-method blue ingest --session ENG-2026-001 --source auth=/var/log/auth.log
npx spectra-method blue tail --session ENG-2026-001 --source auth=/var/log/auth.log --once
npx spectra-method broker export --session ENG-2026-001 --role red --bundle red-bundle.json
npx spectra-method broker import --session ENG-2026-001 --role red --bundle red-bundle.json
```

Party Mode generates deterministic sub-agent plans for Red, Blue, IRT, GRC, coordinator, and scribe lanes. The plan includes input contracts, output contracts, done criteria, model profile classes, quality gates, safety gates, spawn manifest, merge contract, and debate rounds. It is plan-first: RTK execution still requires engagement state and scope checks before any offensive workflow action.

Duel Mode separates Red, Blue, and Referee views for exercises run across different machines. Red and Blue write role-local JSONL ledgers; the Referee scorecard correlates Red actions with Blue detections or mitigations. Red OPSEC is modeled as noise and footprint constraints, while log deletion, audit tampering, destructive cleanup, and security-tool disabling are blocked by policy.

Blue Live Adapter ingests defensive telemetry read-only into the Blue ledger. Supported source types: `auth`, `nginx_access`, `nginx_error`, `postfix`, `dovecot`, `fail2ban`, `suricata_eve`, `wazuh`, `zeek_conn`, `zeek_dns`, and `zeek_http`. `blue tail --once` reads only new bytes since the stored checkpoint, so repeated runs do not duplicate old detections. Partial trailing log lines are held until a newline arrives, which prevents truncated detections.

Red/Blue Broker supports separated machines without requiring shared filesystem access. Each side exports a signed JSON bundle from its local ledger; the Referee imports Red and Blue bundles, deduplicates events, then runs `duel score`. Imports verify the bundle checksum, event count, role/session, bundle schema, and event schema, then retain only known event fields. The broker is offline and file-based: it does not open sockets, deploy agents, or modify remote hosts.

Development background:

- [red-blue-team origin](docs/development/red-blue-team-origin.md)
- [distributed Red/Blue Duel](docs/development/distributed-red-blue-duel.md)

---

## Architecture

```
project/
├── .claude/skills/       60 skills as Claude Code slash commands
├── .codex/spectra/       Codex skill index and routing instructions
├── AGENTS.md             Codex repo-native SPECTRA adapter block
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

- **AI IDE**: Claude Code, Codex, Cursor, or compatible
- **Python**: 3.10+
- **Node.js**: 18+

## License

MIT

---

<p align="center"><em>Built for operators. By operators.</em></p>
