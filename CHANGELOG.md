# SPECTRA Changelog

## v0.1.0 (2026-04-05)

### Initial Release

**Framework:**
- 21 AI agents across 5 modules (Core, RTK, SOC, IRT, GRC)
- 16 complete workflows (~80,000+ lines)
- 10 core skills with embedded templates and protocols
- Step-file architecture with JIT loading
- Agent Autonomy Protocol (HARD BLOCK destructive only)
- War Room multi-agent adversarial discussions
- Context Budget System (Opus/Sonnet/Haiku profiles)

**Modules:**
- 🔴 RTK (Red Team Kit): external-recon, initial-access, privesc, lateral-movement, exfiltration
- 🔵 SOC (Security Operations): alert-triage, detection-lifecycle, phishing-response, threat-hunt
- 🟠 IRT (Incident Response): incident-handling, digital-forensics, malware-analysis, threat-intel
- ⚪ GRC (Governance, Risk & Compliance): risk-assessment, compliance-audit, policy-lifecycle

**Infrastructure:**
- spectra_init.py configuration system (4 subcommands)
- Engagement framework with scope, RoE, kill chain tracking
- Framework reference data (ATT&CK, NIST 800-53, Sigma, OWASP, CIS Controls v8)
- Execution scripts (scope-enforcer, evidence-logger, tools-registry)
- Project validator (1,459 checks across 4 severity tiers)
- CLI installer (npx spectra-method install/validate/status/update)
