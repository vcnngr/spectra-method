---
name: spectra-tool-run
description: 'Run a vetted security tool against an in-scope target, gated by engagement scope and Rules of Engagement. Use when an agent needs to actually execute recon/scanning tooling, not just plan it.'
---

# SPECTRA Tool Run

## Overview

Planning a scan and running it are different acts, and the gap between them is where unauthorized activity hides. SPECTRA closes that gap on its own terms: tools run only through a deterministic adapter that enforces the engagement scope, the Rules of Engagement, and the destructive HARD BLOCK on every invocation. There is no "the agent shelled out to whatever it wanted" — the binary is fixed per tool, there is no shell, and the target must be in scope.

This skill is how an agent moves from a recommended command to an executed, evidence-producing result without leaving the authorized envelope. It wraps the Layer-3 tool adapter, which:

- runs only **allowlisted** tools (the binary is never taken from input);
- uses **no shell** (argv list, `shell=False`) — no injection surface;
- **scope-gates** the target with the same `scope-enforcer` the workflows use;
- **RoE-gates** the action (e.g. a DoS tool needs `dos_testing_allowed`);
- enforces the **destructive HARD BLOCK** (ransomware/wipers/data-destroyers and obviously destructive shell constructs are refused outright);
- defaults to a **dry run** mindset: preview the gated command before executing.

Execution defaults to the local host. Remote execution against a declared, in-scope, fingerprint-pinned host is handled by the exec-target capability and composed with this adapter.

## Deterministic runtime (Layer 3)

List allowlisted tools and whether each binary is installed:

```bash
python3 {project-root}/_spectra/core/execution/tool-adapter.py list
```

Preview a gated command without executing anything (always do this first):

```bash
python3 {project-root}/_spectra/core/execution/tool-adapter.py run \
  --engagement "{engagement_yaml}" --tool nmap --target "{target}" --dry-run
```

Execute the gated command:

```bash
python3 {project-root}/_spectra/core/execution/tool-adapter.py run \
  --engagement "{engagement_yaml}" --tool nmap --target "{target}" -- -sV
```

Status values: `planned` (dry run), `executed`, `blocked` (failed scope/RoE/HARD BLOCK — see `gate.errors`), `unavailable` (binary not installed). Exit codes: 0 ok/planned, 1 blocked, 2 unavailable, 4 tool exited non-zero.

### Remote execution: `--via exec-target`

The same gated command can run on the engagement's declared, in-scope, fingerprint-pinned host instead of locally:

```bash
python3 {project-root}/_spectra/core/execution/tool-adapter.py run \
  --engagement "{engagement_yaml}" --tool nmap --target "{target}" --via exec-target -- -sV
```

The order of trust is layered and fail-closed: this adapter gates the tool, the flag allowlist, and the target scope **first**; only then does the command cross to `spectra-exec-target`, which adds the authorized-host check, the SSH fingerprint pin, the path-qualified-binary refusal, and the destructive HARD BLOCK. Neither layer trusts the other's input. Remote status values: `executed_remote`, `fingerprint_mismatch`, or `blocked` (see `remote.validation.errors`); the remote detail is returned under `result["remote"]`. A `--dry-run` always wins and never reaches the host.

### Fail-closed flag allowlist

Tool flags are **allowlisted per tool**, not denylisted: only explicitly vetted, read-only flags are permitted, and the target is validated as data (never a flag). This structurally refuses flags that would read or write arbitrary files (`-oN`, `-iL`, `--resume`), run code (nmap `--script`), or override the gated target with other hosts (nmap `-iR`). `nuclei` is intentionally not included — its templates can execute code, which flag-gating alone cannot make safe. Adding a tool or flag is a security decision made in `tool-adapter.py`'s `ADAPTERS`, not at call time.

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — store `{user_name}`, `{communication_language}`, `{document_output_language}`, `{engagement_artifacts}`, `{evidence_artifacts}`, and any other config vars.
2. **Detect the active engagement** — find an `engagement.yaml` with `status: "active"` under `{engagement_artifacts}`. If none, halt and recommend `spectra-new-engagement`.
3. **Confirm the target and tool** with the operator.
4. **Dry-run first** — run with `--dry-run`, show the exact `argv` and the gate result, and confirm before executing.
5. **Execute** — run for real; report status, exit code, and captured output.
6. **Preserve evidence** — register meaningful output with `spectra-evidence-chain` so findings derived from it can resolve to verified evidence (see `spectra-attack-path`).

## Boundary

This skill never runs a tool the adapter does not allowlist, never uses a shell, never targets anything outside engagement scope, and never executes a destructive construct — those are refused before execution, not after. Read-only recon is the default posture; anything louder is gated by the engagement noise budget and Rules of Engagement, and the operator decides within them.
