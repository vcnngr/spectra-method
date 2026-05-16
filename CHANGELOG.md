# SPECTRA Changelog

## Unreleased

### Added

- Party Mode v2 plan schema with explicit Red, Blue, IRT, GRC, core/coordinator, and scribe lanes.
- Sub-agent input contracts, output contracts, done criteria, quality gates, spawn manifest, and merge contract.
- CLI lane override: `spectra party plan --lanes red,blue,irt,grc,core`.

## v0.3.1 (2026-05-16)

### Added

- Party Mode sub-agent planner in `core/execution/party-orchestrator.py`.
- CLI bridge: `spectra party plan --topic "..."`
- Duel Mode runtime in `core/execution/duel-orchestrator.py`.
- CLI bridge: `spectra duel init|record|status|score`.
- Blue Live Adapter in `core/execution/blue-live-adapter.py`.
- CLI bridge: `spectra blue ingest --session ENG --source auth=/var/log/auth.log`.
- Blue Tail Mode with checkpointed `spectra blue tail --once`.
- Blue telemetry parsers for Suricata/EVE JSONL, Wazuh JSON alerts, and Zeek conn/dns/http JSONL.
- Red/Blue Broker in `core/execution/red-blue-broker.py`.
- CLI bridge: `spectra broker export|import --session ENG --role red|blue --bundle bundle.json`.
- LLM routing profile classes in `core/config.yaml` for coordinator, Red, Blue, Purple, and scribe lanes.
- Separated Red/Blue/Referee ledgers with scorecard generation.
- Referee scorecard metrics for detection latency, severity coverage, misses by technique, and outcome grade.
- Party Mode regression tests and installer smoke coverage.
- Development docs for the `red-blue-team` origin directory and distributed Duel Mode.

### Changed

- War Room workflow now documents plan-first sub-agent orchestration before parallel or multi-LLM execution.
- Duel scorecards now include richer low-and-slow exercise metrics while preserving existing JSON fields.
- Validator and CI now check Party Mode, Duel Mode, Blue adapter, and broker execution scripts.

### Security

- Duel Mode blocks Red ledger events that attempt log deletion, audit tampering, destructive cleanup, or security-tool disabling instructions.
- Blue Live Adapter is read-only and only parses telemetry into Blue ledger events.
- Red/Blue Broker is offline and file-based. It signs exported event payloads with SHA256 and imports with deduplication; it does not create a network listener or control remote hosts.

## v0.3.0 (2026-05-16)

### Added

- Compact `_config/skill-index.json` generated from `skill-manifest.csv`.
- `scripts/build-skill-index.mjs` for deterministic skill index rebuilds.
- Lazy install mode: `spectra install --lazy` installs core only.
- Lazy module loading commands: `spectra modules list` and `spectra modules add <modules>`.
- Report adapter runtime in `core/execution/report-adapters.py`.
- Structured report generator runtime in `core/execution/report-generator.py`.
- CLI report bridge: `spectra report generate -e engagement.yaml --type pentest`.
- Report pipeline regression tests and smoke coverage.

### Changed

- Skill registration now reads compact `skill-index.json` first and falls back to CSV.
- Installer manifest now records `availableModules`.
- Validator now checks report adapter and report generator scripts.
- Report generator skill now documents the deterministic runtime path.
- Version metadata updated to `0.3.0`.

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
