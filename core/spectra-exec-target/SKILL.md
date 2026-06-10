---
name: spectra-exec-target
description: 'Run authorized commands on an operator-declared host over SSH, pinned to its host fingerprint and gated by engagement scope. Use to execute against a real in-scope target host.'
---

# SPECTRA Exec Target

## Overview

To make an engagement executable against a real host without leaving the authorized envelope, SPECTRA runs remote commands only on a host the operator has explicitly declared, that is inside the engagement scope, and whose live SSH host key matches a pinned fingerprint. That triple — **authorized + in-scope + fingerprint-pinned** — is the authorization boundary. Connecting to an unexpected host is refused, never trusted on first use.

The remote execution is hardened: SSH runs as an argv list (no shell on our side), with `BatchMode=yes` (no interactive auth), `StrictHostKeyChecking=yes` against a known_hosts built from the *verified* key, and the remote command shlex-quoted so no token can break out into the remote shell. Destructive remote commands are refused even on an authorized host.

This skill decides **where** a command runs and proves the where is the pinned, authorized host. It does not decide **what** runs — the tool and its flags are gated by `spectra-tool-run` (the tool adapter). Compose them: gate the command locally, then execute it on the declared target.

## Engagement declaration

Add an `exec_target` block to the engagement (see `engagement-template.yaml`):

```yaml
engagement:
  exec_target:
    host: "10.0.0.5"          # must be inside engagement scope
    port: 22
    user: "operator"
    key_path: "~/.ssh/engagement_key"
    pinned_fingerprint: "SHA256:..."   # the expected host key fingerprint
    authorized: true          # the operator's explicit go-ahead
```

Get the fingerprint to pin with: `ssh-keyscan -p <port> <host> | ssh-keygen -lf -`.

## Deterministic runtime (Layer 3)

Validate the declaration and confirm the live host matches the pinned fingerprint:

```bash
python3 {project-root}/_spectra/core/execution/exec-target.py verify --engagement "{engagement_yaml}"
```

Run an authorized read-only diagnostic on the declared host:

```bash
python3 {project-root}/_spectra/core/execution/exec-target.py run --engagement "{engagement_yaml}" -- uname -a
```

The raw remote runner accepts **read-only diagnostics only** (`id`, `uname`, `whoami`, `hostname`, `pwd`, `uptime`). It deliberately refuses scanning tools (nmap, httpx, dig, whatweb): running them here would bypass the tool adapter's flag allowlist and per-target scope check (for example, `nmap -iR <host>` would scan arbitrary out-of-scope hosts even though the exec host itself is in scope). Gated tool execution against a remote host goes through `spectra-tool-run`, which enforces the flag allowlist and target scope before dispatch.

### Composed entrypoint: `tool-run --via exec-target`

The supported way to run a *scanning tool* on the declared host is not the raw runner above but `spectra-tool-run` with `--via exec-target`. That path calls this module's **gated** runner, which skips the diagnostics-only binary allowlist (the tool adapter has already gated the tool, its flags, and the target scope) while still enforcing every authorization control here: authorized + in-scope host, fingerprint pin, refusal of any path-qualified binary (a bare name is required; a planted path like `./nmap` or a directory-qualified token is rejected), and the destructive HARD BLOCK. The two layers never trust each other's input — each re-checks what it owns.

Status values: `executed`, `blocked` (not authorized / out of scope / not an allowed remote binary / destructive — see `validation.errors`), `fingerprint_mismatch` (live host key does not match the pin — execution refused). Exit codes: 0 ok, 1 blocked, 2 fingerprint mismatch, 4 remote command non-zero.

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — store `{user_name}`, `{communication_language}`, `{document_output_language}`, `{engagement_artifacts}`, and any other config vars.
2. **Detect the active engagement** with an `exec_target` block. If none, halt and explain that remote execution requires a declared, authorized exec_target.
3. **Verify first** — always run `verify` and confirm the fingerprint matches before running any command. If it mismatches, STOP and surface it: the host is not the expected one.
4. **Gate the command** with `spectra-tool-run` (scope/RoE/flag allowlist) before sending it to the host.
5. **Run and report** — execute, report status, exit code, and captured output. Preserve meaningful output with `spectra-evidence-chain`.

## Boundary

This skill never executes on a host that is not declared, in scope, and fingerprint-pinned; never trusts an unknown host key; never uses a shell on the SPECTRA side; and refuses destructive remote commands. The pin plus the scope plus the explicit authorization are what make remote execution defensible.
