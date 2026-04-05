# SPECTRA -- Security Protocol Engineering for Cyber Threat Response & Assessment

> "Attack. Defend. Evolve."

Multi-agent cybersecurity framework for AI-assisted security operations. 21 specialized agents organized into 4 operational modules plus a core framework -- covering red team, blue team, incident response, and governance.

## Quick Start

### Install via npx

```bash
npx spectra-method install
```

### Install specific modules

```bash
npx spectra-method install --modules rtk,soc
```

### Validate installation

```bash
npx spectra-method validate
```

### Check installation status

```bash
npx spectra-method status
```

### Update to latest version

```bash
npx spectra-method update
```

## What is SPECTRA?

SPECTRA is a multi-agent framework designed for cybersecurity operations within AI IDE environments (Claude Code, Cursor, and similar). It provides 21 purpose-built agents, each with deep domain expertise, structured workflows, and deterministic execution scripts.

The framework operates through engagements -- scoped security assessments with defined rules of engagement, evidence chains, and reporting pipelines.

## Modules

| Module | Icon | Focus | Agents | Workflows |
|--------|------|-------|--------|-----------|
| **RTK** | Red | Red Team Kit | 6 | 5 |
| **SOC** | Blue | Security Operations Center | 6 | 4 |
| **IRT** | Orange | Incident Response Team | 5 | 4 |
| **GRC** | White | Governance, Risk & Compliance | 3 | 3 |
| **Core** | Bolt | Framework + Documentation | 2 | 10 skills |

## Agents

### Core (2)

| Agent | Persona | Specialty |
|-------|---------|-----------|
| Specter | CISO / Quick Ops | Cross-domain assessment, rapid triage, strategic oversight |
| Chronicle | Documentation Specialist | Pentest reports, incident reports, executive briefs |

### RTK -- Red Team Kit (6)

| Agent | Persona | Specialty |
|-------|---------|-----------|
| Viper | Red Team Lead | Engagement planning, attack strategy, team coordination |
| Ghost | Recon & OSINT | Passive/active recon, subdomain enumeration, credential leaks |
| Razor | Exploit Developer | Vulnerability analysis, exploit chains, PoC development |
| Phantom | Attack Operator | C2 management, persistence, lateral movement, evasion |
| Mirage | Social Engineer | Phishing campaigns, pretext development, awareness testing |
| Blade | Quick Pentester | Rapid vulnerability assessment, automated scanning |

### SOC -- Security Operations Center (6)

| Agent | Persona | Specialty |
|-------|---------|-----------|
| Commander | SOC Manager | Metrics, KPIs, escalation management, executive reporting |
| Watchdog | L1 Triage Analyst | Alert triage, IOC enrichment, false positive identification |
| Tracker | L2 Investigator | Event correlation, timeline construction, scope determination |
| Hawk | L3 Threat Hunter | Hypothesis-driven hunting, behavioral analysis, ATT&CK mapping |
| Sentinel | Detection Engineer | Sigma/YARA rules, detection tuning, coverage mapping |
| Shield | Quick Analyst | Rapid triage + investigation + detection in one flow |

### IRT -- Incident Response Team (5)

| Agent | Persona | Specialty |
|-------|---------|-----------|
| Dispatch | Incident Handler | Coordination, timeline tracking, stakeholder communication |
| Trace | Forensic Analyst | Disk/memory/network forensics, evidence preservation |
| Scalpel | Malware Analyst | Static/dynamic analysis, reverse engineering, IOC extraction |
| Oracle | Threat Intel Analyst | Campaign tracking, attribution, Diamond Model analysis |
| Surge | Quick Responder | Rapid triage, containment, emergency response |

### GRC -- Governance, Risk & Compliance (3)

| Agent | Persona | Specialty |
|-------|---------|-----------|
| Arbiter | Risk Analyst | FAIR methodology, risk quantification, business impact analysis |
| Auditor | Compliance Auditor | ISO 27001, SOC 2, PCI DSS, gap analysis, control mapping |
| Scribe | Policy Author | Policy drafting, ISMS documentation, procedure standards |

## Getting Started

1. **Install SPECTRA** -- `npx spectra-method install`
2. **Configure** -- Run the `spectra-init` skill to set project variables
3. **Create an engagement** -- Use `spectra-new-engagement` to define scope and rules
4. **Invoke agents** -- Talk to them by name:
   - "Talk to Viper" -- Red team lead
   - "Talk to Commander" -- SOC manager
   - "Talk to Dispatch" -- Incident handler
   - "Talk to Arbiter" -- Risk analyst

## CLI Commands

| Command | Description |
|---------|-------------|
| `npx spectra-method install` | Install SPECTRA into current project |
| `npx spectra-method install --modules rtk,soc` | Install specific modules |
| `npx spectra-method install --target ./path` | Install into a specific directory |
| `npx spectra-method install --force` | Force reinstall (overwrites framework files) |
| `npx spectra-method validate` | Validate installation structure |
| `npx spectra-method status` | Show version, modules, and config status |
| `npx spectra-method update` | Update framework files (preserves configs) |

## Requirements

- **AI IDE**: Claude Code, Cursor, or compatible AI IDE environment
- **Python**: 3.10+ (for init and validation scripts)
- **Node.js**: 18+ (for CLI installer -- optional if installing manually)

## Architecture

SPECTRA follows a 3-layer architecture:

- **Directives** -- Skills (SKILL.md files) define what each agent does
- **Orchestration** -- The AI IDE reads directives and routes between agents
- **Execution** -- Python scripts handle deterministic operations (evidence logging, scope enforcement, config management)

All engagement data is written to `_spectra-output/` (never committed). Framework files live in `_spectra/`. User configuration is stored in per-module `config.yaml` files that persist across updates.

## License

MIT
