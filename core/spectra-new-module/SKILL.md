---
name: spectra-new-module
description: 'Scaffold a new SPECTRA domain module (agent + workflow + config) with a valid structure. Includes an OT/ICS preset. Use to extend SPECTRA into a new domain.'
---

# SPECTRA New Module

## Overview

SPECTRA's five modules (Core, RTK, SOC, IRT, GRC) all share the same shape: a `module.yaml`, a `config.yaml`, an `agents/` directory, and a `workflows/` directory. This skill makes that shape repeatable so extending SPECTRA into a new domain is a deterministic scaffold, not hand-copied boilerplate — the extensibility flywheel that lets the framework grow without drifting.

It generates a valid module skeleton and prints the manifest rows you should add to register it. Registration is deliberately a reviewed step: the scaffold never edits the live manifests for you.

A built-in **`ot-ics` preset** demonstrates a domain extension — an OT/ICS security specialist agent and an `ot-assessment` workflow — with SPECTRA's safety boundary baked into the generated content: **OT/ICS work is assessment and modeling only**. The generated agent and workflow state explicitly that they never issue destructive controller/PLC commands and never disrupt safety-instrumented systems.

## Deterministic runtime (Layer 3)

Generate a module (created under `<dest>/<code>/`):

```bash
python3 {project-root}/_spectra/core/execution/scaffold-module.py create \
  --code ot --name "OT/ICS Security" --dest "{project-root}/_spectra" --preset ot-ics
```

A generic module:

```bash
python3 {project-root}/_spectra/core/execution/scaffold-module.py create \
  --code mymod --name "My Module" --dest "{project-root}/_spectra"
```

The command prints the created files plus `suggested_agent_manifest_row` and `suggested_skill_manifest_row`. Module code must be lowercase letters/digits/underscore (2–16 chars). It refuses to overwrite an existing module unless `--force`.

You must fully embody this persona so the user gets the best experience and help they need, therefore its important to remember you must not break character until the user dismisses this persona.

When you are in this persona and the user calls a skill, this persona must carry through and remain active.

## On Activation

1. **Load config via spectra-init skill** — store config vars.
2. **Confirm the module** — code, human-readable name, and whether to use the `ot-ics` preset or a generic skeleton.
3. **Generate** the module with the runtime above.
4. **Register (reviewed)** — add the printed rows to `_config/agent-manifest.csv` and `_config/skill-manifest.csv`, then run `npm run build:skill-index` and `npm run validate`.
5. **Fill in the domain content** — replace the stub identity/steps with real domain knowledge and framework mappings (e.g. ICS ATT&CK + IEC 62443 for OT).

## Boundary

The scaffold generates structure, not authorization to act. Generated modules inherit SPECTRA's safety boundary; domain presets that touch sensitive environments (like OT/ICS) generate assessment-only agents that never manipulate live control systems. The operator reviews and registers — nothing is wired into the live framework automatically.
