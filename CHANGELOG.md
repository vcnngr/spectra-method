# SPECTRA Changelog

## v0.2.0 (2026-05-16)

### Added

- Deterministic engagement state machine in `core/execution/engagement-state.py`.
- JSON and YAML engagement schemas in `core/schemas/`.
- CLI bridge: `spectra engagement validate|status|gate|transition`.
- `workflow_state` section in the engagement template for RTK phase tracking.
- `data_handling` section in the engagement template for exfiltration authorization controls.
- Installer smoke tests now verify schema/script installation and exercise the Node engagement command.

### Changed

- RTK workflows now require `engagement-state.py gate` before workflow execution.
- RTK workflows now require `scope-enforcer.py check` before every target-specific action.
- Validator now checks the engagement state script and schema files.
- Version metadata updated to `0.2.0`.

### Security

- Exfiltration workflow gate now requires explicit `data_exfiltration_allowed` authorization.
- Exfiltration workflow gate now requires data type, retention, destruction, and encryption controls.
- Failed deterministic gates are hard stops and cannot be overridden by manual workflow interpretation.

## v0.1.1 (2026-05-16)

### Fixed

- Validator now supports both npm source layout and installed `_spectra/` layout.
- Validator now supports partial installs such as `--modules rtk` without false missing-module failures.
- CLI `validate` no longer requires `DEV-GUIDE.md`, which is intentionally excluded from installed projects.
- Scope enforcer now normalizes textual RoE values such as `"none"`, `"false"`, `"light"`, and `"full"`.
- Scope enforcer now hard-blocks destructive action descriptions at the deterministic layer.
- Corrected RTK lateral-movement and exfiltration workflow text from `NO HARD BLOCK` to `HARD BLOCK`.

### Changed

- CI and npm publish workflows now run the full SPECTRA validator.
- CI now runs full and partial install smoke tests before accepting changes.
- CLI `validate --deep` now runs the full Python validator against an installed project.
- Added reusable npm scripts for validator, scope guardrail tests, and install smoke tests.

### Added

- Regression tests for scope enforcement, RoE normalization, out-of-scope precedence, and destructive-action blocking.

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
