# SPECTRA Changelog

## v0.7.0 (2026-07-03)

### Added

- **OT/ICS module** (6th module): agent **Relay** (OT/ICS Security Specialist) and the `spectra-ot-assessment` 6-step workflow — Purdue-model architecture, ICS protocol exposure, MITRE ATT&CK for ICS, and IEC 62443 zones/conduits + SR/CR controls. Assessment-only boundary at every layer (no control/PLC commands, no writes, no SIS interaction). Agent count 28 → 29.
- **Quickstart onboarding** — `spectra quickstart` scaffolds a shipped, loopback-only demo engagement (sample findings + a worked War Room debrief) or a scenario template (`web-pentest`, `cloud-ir`, `ot-assessment`) and prints a guided tour. Copy-only, symlink/hardlink-escape guarded.
- **Posture diff** — `spectra posture` (skill `spectra-posture-diff`): snapshot an engagement's posture (findings/scope/run-log) and diff two snapshots into a status-aware, severity-weighted delta (improved/regressed/unchanged). Makes recurring engagements a trend line.
- **Remediation export** — `spectra export` (skill `spectra-remediation-export`): export findings to SARIF 2.1.0 (with locations), CSV (formula-injection escaped), or a Markdown ticket pack. Deterministic export, no network.
- **Run accounting** — `spectra runs` + `run-accounting.py`: append-only per-engagement `run-log.jsonl` of every gated tool run (including dry-run and blocked), with a status/tool summary. `--no-log` opts out.
- **`tool-run --via exec-target`** — run a gated tool command on the engagement's declared, in-scope, SSH-fingerprint-pinned host; the tool adapter gates tool/flags/scope and exec-target adds the authorized-host boundary.
- Growth execution layer: attack-path graph generator, persona-first engagement entry, RoE noise budget, fail-closed tool adapter, fingerprint-pinned exec-target, reproducible Referee benchmark, multimodal (screenshot) evidence, and a custom-module scaffold.

### Fixed

- #2 — engagement state machine now tolerates the natural spellings `completed`/`in progress` and canonicalizes them to `complete`/`in-progress`, so a workflow's status no longer fails the next gate or needs a manual edit.
- #3 — AppSec token/JWT inspection guidance: self-contained, correct commands (no `|| fallback` masking, no undefined vars or dead branches); robust base64url decode with explicit padding.
- #4 — external-recon verifies which spec a Swagger/OpenAPI UI loads before rating severity (default petstore spec → Low; target's own API → Medium), avoiding an inflated false positive.
- #5 — AppSec step close is gated by a REQUIRED-OUTPUT self-audit; a step cannot be marked complete with missing outputs.
- #6 — canonical step-close order (consolidate evidence → verify no secrets → then sanitize), no error-silencing on destruction, and a token-hygiene rule; sanitization scoped to the agent's own files only.
- #7 — Target Artifact Ledger tracks artifacts created on the target with a disposition; privileged synthetic artifacts (e.g. admin accounts) must be removed or flagged, never left silently active.
- #1 — CI prepared for the GitHub Actions Node.js 24 runtime (compat smoke + test on Node 24).

### Changed

- Validator module set and persona-count test extended for the OT module (validator 2040 checks, execution suite 330 tests).

### Security

- Migrated npm publish workflow to npm Trusted Publishers (OIDC). Removed dependency on long-lived `NPM_TOKEN` secret; npm now authenticates via GitHub Actions OIDC identity claims (org `vcnngr`, repo `spectra-method`, workflow `publish.yml`).
- Pinned npm CLI upgrade step (`npm install -g npm@latest`) to satisfy Trusted Publishers minimum (npm >= 11.5.1).
- Provenance attestations continue to be generated automatically on publish.
- Recommended hardening (manual, post-migration): enable "Require two-factor authentication and disallow tokens" on the `spectra-method` npm package and delete the legacy `NPM_TOKEN` GitHub secret.

## v0.6.0 (2026-05-16)

### Added

- Codex IDE adapter via `spectra install --tools codex`.
- Generated project `AGENTS.md` managed block for Codex repo-native SPECTRA routing.
- Generated `.codex/spectra/skill-index.json` and `.codex/spectra/instructions.md`.
- `_config/ides/codex.yaml` to document Codex install behavior alongside Claude Code.
- Smoke coverage for combined Claude Code + Codex installs and Codex lazy module add.

### Changed

- CLI `--tools` validation now accepts `codex` in addition to `claude-code`.
- Install/status/validate output now reports Codex adapter state.
- README now documents Claude Code slash-command usage and Codex repo-native usage.
- Version metadata updated to `0.6.0`.

## v0.5.0 (2026-05-16)

### Added

- Six workflow brains for the agents introduced in v0.4.0:
  - `spectra-appsec-assessment` for Forge: AppSec/API assessment, auth/session review, authorization, business logic, input/API risk, remediation, and handoff.
  - `spectra-identity-detection-review` for Keystone: identity privilege maps, MFA/session review, OAuth and persistence surfaces, detection coverage, and response readiness.
  - `spectra-telemetry-readiness` for Signal: source coverage, parser/schema quality, retention/integrity, Blue Live fit, and detection gap mapping.
  - `spectra-cloud-incident-response` for Stratus: cloud incident intake, evidence preservation, blast radius, containment planning, recovery, governance gates, and reporting.
  - `spectra-privacy-breach-assessment` for Counsel: data exposure, jurisdiction/clock map, legal hold, notification decision support, and governance remediation.
  - `spectra-duel-adjudication` for Referee: ledger integrity, timeline correlation, scoring, fairness review, gap analysis, and final scorecard.

### Changed

- Workflow coverage increased from 16 to 22 structured workflows.
- Skill registration increased from 54 to 60 skills.
- README workflow tables updated for RTK, SOC, IRT, GRC, and Core orchestration.
- Version metadata updated to `0.5.0`.

## v0.4.0 (2026-05-16)

### Added

- Party Mode v2 plan schema with explicit Red, Blue, IRT, GRC, core/coordinator, and scribe lanes.
- Sub-agent input contracts, output contracts, done criteria, quality gates, spawn manifest, and merge contract.
- CLI lane override: `spectra party plan --lanes red,blue,irt,grc,core`.
- Six additional agents prepared for the next patch/minor release:
  - Referee, Exercise Referee for Red/Blue ledger correlation and scoring.
  - Forge, AppSec/API Specialist for application and API security assessment.
  - Keystone, Identity Security Specialist for AD, Entra ID, Okta, IAM, OAuth, and privilege analysis.
  - Signal, Telemetry Engineer for log-source coverage, parser quality, SIEM readiness, and Blue Live source validation.
  - Stratus, Cloud Security Specialist for AWS, Azure, GCP, Kubernetes, SaaS logs, cloud forensics, and cloud incident response.
  - Counsel, Privacy/Breach Governance Specialist for privacy impact, breach governance, legal hold, and regulatory exposure.

### Changed

- Renamed legacy `bmad-skill-manifest.yaml` files to `spectra-skill-manifest.yaml`.
- Validator now requires `spectra-skill-manifest.yaml` and reports legacy BMAD manifest names as warnings.
- Version metadata updated to `0.4.0`.

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
