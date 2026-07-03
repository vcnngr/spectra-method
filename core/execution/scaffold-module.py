#!/usr/bin/env python3
"""SPECTRA Module Scaffold (Layer 3 — deterministic execution).

SPECTRA ships five modules (Core, RTK, SOC, IRT, GRC) that all share the same
shape: a module.yaml, a config.yaml, an agents/ dir, and a workflows/ dir. This
generator makes that shape repeatable, so extending SPECTRA into a new domain is
a deterministic scaffold rather than hand-copied boilerplate — the extensibility
flywheel the framework needs to grow without drifting.

It writes a valid module skeleton to a target directory and prints the manifest
rows an operator should add to register it. Registration is intentionally NOT
automatic: adding agents/skills to the live manifests is a reviewed step.

A built-in `ot-ics` preset demonstrates a domain extension — an OT/ICS security
specialist agent and an ot-assessment workflow — with SPECTRA's safety boundary
baked in: OT/ICS work is modeling and assessment only. The generated content
states explicitly that it never issues destructive controller/PLC commands and
never disrupts safety-instrumented systems.

CLI:
  scaffold-module.py create --code ot --name "OT/ICS Security" --dest ./ --preset ot-ics
  scaffold-module.py create --code mymod --name "My Module" --dest /tmp/out
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

# Hyphen-free lowercase so generated agent/workflow ids (spectra-<code>-...) stay
# valid; '_' would break the validator's spectra-* id regex.
CODE_RE = re.compile(r"^[a-z][a-z0-9]{1,15}$")
# Canonical modules must never be overwritten by the scaffold.
RESERVED_CODES = {"core", "rtk", "soc", "irt", "grc"}
# Names embed into YAML scalars and single-quoted frontmatter, so disallow
# quotes, newlines, and backslashes that would break the generated files.
NAME_RE = re.compile(r"^[A-Za-z0-9 /&.,()+\-]{1,60}$")


def _csv_row(fields: list[str]) -> str:
    """Build one CSV row with proper quoting (handles commas/quotes in fields)."""
    buf = io.StringIO()
    csv.writer(buf, quoting=csv.QUOTE_ALL).writerow(fields)
    return buf.getvalue().strip("\r\n")


# ---------------------------------------------------------------------------
# Presets
# ---------------------------------------------------------------------------

def _generic_preset(code: str, name: str) -> dict[str, Any]:
    agent_slug = f"spectra-agent-{code}-lead"
    wf_slug = f"spectra-{code}-assessment"
    return {
        "agent": {
            "slug": agent_slug,
            "displayName": name.split()[0].title() if name.split() else "Lead",
            "title": f"{name} Specialist",
            "role": f"{name} Specialist + Module Lead",
            "capabilities": f"{name} assessment, planning, reporting, and handoff",
            "extra_sections": "",
            "boundary": (f"This agent operates within engagement scope and Rules of Engagement. "
                         f"It supports authorized {name} work only."),
        },
        "workflow": {
            "slug": wf_slug,
            "title": f"{name} Assessment",
            "goal": f"Plan and conduct an authorized {name} assessment, producing evidence-backed findings.",
        },
    }


def _ot_ics_preset(code: str, name: str) -> dict[str, Any]:
    agent_slug = f"spectra-agent-{code}-ics"
    wf_slug = f"spectra-{code}-assessment"
    return {
        "agent": {
            "slug": agent_slug,
            "displayName": "Relay",
            "title": "OT/ICS Security Specialist",
            "role": "OT/ICS Security Specialist + Industrial Assessment Lead",
            "capabilities": ("OT/ICS architecture review, Purdue-model segmentation analysis, "
                             "ICS protocol exposure assessment (Modbus, DNP3, S7, EtherNet/IP), "
                             "ICS ATT&CK technique mapping, IEC 62443 control assessment, "
                             "safety-instrumented-system risk review"),
            "extra_sections": (
                "## OT/ICS Domain Notes\n\n"
                "- Map activity to the ICS ATT&CK matrix and IEC 62443 zones/conduits and SR/CR controls.\n"
                "- Reason in the Purdue model (levels 0-5); flag flat networks and IT/OT bridges.\n"
                "- Treat availability and safety as paramount — in OT they outrank confidentiality.\n"
            ),
            "boundary": (
                "OT/ICS work in SPECTRA is ASSESSMENT and MODELING only. This agent NEVER issues "
                "destructive or state-changing controller/PLC commands, NEVER writes to industrial "
                "control points, and NEVER disrupts or disables safety-instrumented systems (SIS). "
                "It documents exposure, segmentation, and detection gaps so defenders can fix them — "
                "it does not manipulate live process control. Any active testing requires explicit, "
                "written authorization and an isolated/lab environment."
            ),
        },
        "workflow": {
            "slug": wf_slug,
            "title": "OT/ICS Assessment",
            "goal": ("Conduct an authorized, ASSESSMENT-ONLY OT/ICS review: enumerate the industrial "
                     "architecture and exposure, map to ICS ATT&CK and IEC 62443, and produce "
                     "evidence-backed segmentation and detection-gap findings — never manipulating "
                     "live process control or safety systems."),
        },
    }


PRESETS = {"generic": _generic_preset, "ot-ics": _ot_ics_preset}


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

def _module_yaml(code: str, name: str) -> str:
    return (
        f"code: {code}\n"
        f"name: \"SPECTRA {name} Kit\"\n"
        f"description: \"{name} module generated by spectra-new-module\"\n"
        f"module_version: 0.1.0\n"
        f"default_selected: false\n\n"
        f"header: \"{name} Configuration\"\n"
        f"subheader: \"Configure the {name} module.\"\n\n"
        f"{code}_artifacts:\n"
        f"  prompt: \"Where should {name} engagement artifacts be stored?\"\n"
        f"  default: \"{{output_folder}}/engagements/{{engagement_id}}/{code}\"\n"
        f"  result: \"{{project-root}}/{{value}}\"\n\n"
        f"{code}_reports:\n"
        f"  prompt: \"Where should {name} reports be stored?\"\n"
        f"  default: \"{{output_folder}}/engagements/{{engagement_id}}/{code}/reports\"\n"
        f"  result: \"{{project-root}}/{{value}}\"\n\n"
        f"directories:\n"
        f"  - \"{{output_folder}}/engagements/{{engagement_id}}/{code}\"\n"
        f"  - \"{{output_folder}}/engagements/{{engagement_id}}/{code}/reports\"\n"
    )


def _config_yaml(code: str, name: str) -> str:
    return (
        f"# {name} Module Configuration\n"
        f"# Version: 0.1.0\n\n"
        f"# Inherited from core\n"
        f"user_name: Operator\n"
        f"communication_language: English\n"
        f"document_output_language: English\n"
        f"output_folder: _spectra-output\n\n"
        f"# {code}-specific\n"
        f"{code}_artifacts: \"{{project-root}}/_spectra-output/engagements/{{engagement_id}}/{code}\"\n"
        f"{code}_reports: \"{{project-root}}/_spectra-output/engagements/{{engagement_id}}/{code}/reports\"\n"
    )


def _agent_skill_md(agent: dict[str, Any]) -> str:
    extra = agent.get("extra_sections", "")
    extra_block = f"\n{extra}\n" if extra else ""
    return (
        f"---\n"
        f"name: {agent['slug']}\n"
        f"description: '{agent['title']}. {agent['capabilities']}.'\n"
        f"---\n\n"
        f"# {agent['displayName']} — {agent['title']}\n\n"
        f"## Overview\n\n"
        f"{agent['role']}. {agent['capabilities']}.\n\n"
        f"You must fully embody this persona so the user gets the best experience and help they "
        f"need, therefore its important to remember you must not break character until the user "
        f"dismisses this persona.\n\n"
        f"## Identity\n\n"
        f"{agent['role']} operating within authorized engagements.\n\n"
        f"## Communication Style\n\n"
        f"Evidence-driven, precise, and scope-aware. Separates observation from interpretation.\n\n"
        f"## Principles\n\n"
        f"Evidence over assumption. Authorized scope and Rules of Engagement bound every action. "
        f"The report is the deliverable.\n"
        f"{extra_block}\n"
        f"## On Activation\n\n"
        f"1. Load config via spectra-init skill and store config vars.\n"
        f"2. Detect the active engagement; if none, recommend spectra-new-engagement.\n"
        f"3. Confirm scope and objectives with the operator before acting.\n\n"
        f"## Boundary\n\n"
        f"{agent['boundary']}\n"
    )


def _workflow_skill_md(wf: dict[str, Any]) -> str:
    return (
        f"---\n"
        f"name: {wf['slug']}\n"
        f"description: '{wf['title']} workflow. {wf['goal']}'\n"
        f"---\n\n"
        f"# {wf['title']}\n\n"
        f"## Overview\n\n"
        f"{wf['goal']}\n\n"
        f"You must fully embody this persona so the user gets the best experience and help they "
        f"need, therefore its important to remember you must not break character until the user "
        f"dismisses this persona.\n\n"
        f"## On Activation\n\n"
        f"1. Load config via spectra-init skill and store config vars.\n"
        f"2. Detect the active engagement scoped to this assessment.\n"
        f"3. Follow the assessment steps, producing evidence-backed findings.\n\n"
        f"## Boundary\n\n"
        f"Operates within engagement scope and Rules of Engagement; authorized assessment only.\n"
    )


def _workflow_md(wf: dict[str, Any]) -> str:
    return (
        f"---\n"
        f"main_config: '{{project-root}}/_spectra/core/config.yaml'\n"
        f"---\n\n"
        f"# {wf['title']} Workflow\n\n"
        f"**Goal:** {wf['goal']}\n\n"
        f"This workflow uses step-file architecture. Load only the current step file; "
        f"execute steps in order; halt at menus and wait for user input.\n\n"
        f"## Route\n\n"
        f"Read fully and follow: `./steps-c/step-01-init.md`\n"
    )


def _step_01_md(wf: dict[str, Any]) -> str:
    return (
        f"# Step 1: Initialization\n\n"
        f"**Progress: Step 1 of 1**\n\n"
        f"## STEP GOAL\n\n"
        f"{wf['goal']}\n\n"
        f"## Sequence of Instructions (Do not deviate, skip, or optimize)\n\n"
        f"1. Load config via spectra-init skill and store config vars.\n"
        f"2. Detect the active engagement scoped to this assessment.\n"
        f"3. Conduct the assessment within scope and Rules of Engagement, producing "
        f"evidence-backed findings.\n\n"
        f"## 🚨 SYSTEM SUCCESS/FAILURE METRICS\n\n"
        f"### ✅ SUCCESS:\n\n"
        f"- Engagement detected and scope confirmed\n"
        f"- Assessment conducted within scope and Rules of Engagement\n"
        f"- Evidence-backed findings produced\n"
        f"- All output in `{{communication_language}}`\n\n"
        f"### ❌ SYSTEM FAILURE:\n\n"
        f"- Acting outside engagement scope or Rules of Engagement\n"
        f"- Producing findings without evidence\n"
        f"- Not speaking in `{{communication_language}}`\n\n"
        f"**Master Rule:** Skipping steps or acting outside scope is FORBIDDEN and "
        f"constitutes SYSTEM FAILURE.\n"
    )


def _skill_manifest(kind: str) -> str:
    return f"type: {kind}\n"


def _readme(code: str, name: str, agent_slug: str, wf_slug: str) -> str:
    return (
        f"# SPECTRA {name} Kit (`{code}`)\n\n"
        f"Generated by `spectra-new-module`.\n\n"
        f"## Contents\n\n"
        f"- `agents/{agent_slug}/` — module agent\n"
        f"- `workflows/{wf_slug}/` — module workflow\n"
        f"- `module.yaml`, `config.yaml` — module metadata and configuration\n\n"
        f"## Registering this module\n\n"
        f"Add the agent and workflow rows printed by the scaffold to "
        f"`_config/agent-manifest.csv` and `_config/skill-manifest.csv`, then run "
        f"`npm run build:skill-index` and `npm run validate`.\n"
    )


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def generate(code: str, name: str, dest: str, preset: str = "generic",
             force: bool = False) -> dict[str, Any]:
    """Write a module skeleton under dest/<code>/ and return the created files +
    suggested manifest rows. Refuses to overwrite an existing module unless force."""
    if not CODE_RE.match(code):
        raise ValueError(f"Invalid module code {code!r}: use lowercase letters/digits, 2-16 chars")
    if code in RESERVED_CODES:
        raise ValueError(f"Module code {code!r} is reserved (a canonical SPECTRA module)")
    if not NAME_RE.match(name):
        raise ValueError(f"Invalid module name {name!r}: letters/digits/spaces and / & . , ( ) + - only")
    if ".." in Path(dest).parts:
        raise ValueError(f"Invalid dest {dest!r}: '..' path components are not allowed")
    if preset not in PRESETS:
        raise ValueError(f"Unknown preset {preset!r}. Available: {', '.join(sorted(PRESETS))}")

    spec = PRESETS[preset](code, name)
    agent = spec["agent"]
    wf = spec["workflow"]

    dest_path = Path(dest)
    module_dir = dest_path / code
    if module_dir.exists() and not force:
        raise FileExistsError(f"Module directory already exists: {module_dir} (use --force to overwrite)")

    agent_rel = f"agents/{agent['slug']}"
    wf_rel = f"workflows/{wf['slug']}"
    # Relative path within the module -> content. A generated workflow includes
    # workflow.md + a steps-c/ step so it satisfies the SPECTRA validator.
    rel_files: dict[str, str] = {
        "module.yaml": _module_yaml(code, name),
        "config.yaml": _config_yaml(code, name),
        "README.md": _readme(code, name, agent["slug"], wf["slug"]),
        f"{agent_rel}/SKILL.md": _agent_skill_md(agent),
        f"{agent_rel}/spectra-skill-manifest.yaml": _skill_manifest("agent"),
        f"{wf_rel}/SKILL.md": _workflow_skill_md(wf),
        f"{wf_rel}/spectra-skill-manifest.yaml": _skill_manifest("skill"),
        f"{wf_rel}/workflow.md": _workflow_md(wf),
        f"{wf_rel}/steps-c/step-01-init.md": _step_01_md(wf),
    }

    # Write into a temp sibling dir, then atomically swap it into place so a
    # mid-write failure never leaves a partial module and --force never leaves
    # stale files behind.
    tmp_dir = dest_path / f".{code}.scaffold.tmp"
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    try:
        for rel, content in rel_files.items():
            target = tmp_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        if module_dir.exists():
            shutil.rmtree(module_dir)
        tmp_dir.replace(module_dir)
    except Exception:
        if tmp_dir.exists():
            shutil.rmtree(tmp_dir, ignore_errors=True)
        raise

    files = {str(module_dir / rel): content for rel, content in rel_files.items()}

    # Suggested manifest rows (CSV) — printed for the operator to review, not
    # auto-appended (registration is a reviewed step). Built with csv.writer so
    # any commas/quotes in fields are escaped correctly. The agent path is a
    # DIRECTORY (matching agent-manifest.csv); the skill path is the SKILL.md.
    agent_row = _csv_row([
        agent["slug"], agent["displayName"], agent["title"], "🛠",
        agent["capabilities"], agent["role"],
        "[FILL_IN_IDENTITY]", "[FILL_IN_COMMUNICATION_STYLE]", "[FILL_IN_PRINCIPLES]",
        code, f"_spectra/{code}/agents/{agent['slug']}", agent["slug"],
    ])
    skill_row = _csv_row([
        wf["slug"], wf["slug"], f"{wf['title']} workflow. {wf['goal']}",
        code, f"_spectra/{code}/workflows/{wf['slug']}/SKILL.md", "true",
    ])

    return {
        "module_code": code,
        "module_dir": str(module_dir),
        "preset": preset,
        "files_created": sorted(files.keys()),
        "agent": agent["slug"],
        "workflow": wf["slug"],
        "suggested_agent_manifest_row": agent_row,
        "suggested_skill_manifest_row": skill_row,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_create(args: argparse.Namespace) -> None:
    try:
        result = generate(args.code, args.name, args.dest, preset=args.preset, force=args.force)
    except (ValueError, FileExistsError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    print(json.dumps(result, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="scaffold-module.py",
        description="Generate a valid SPECTRA module skeleton.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create", help="Create a new module skeleton")
    p.add_argument("--code", required=True, help="Module code (lowercase, e.g. 'ot')")
    p.add_argument("--name", required=True, help="Human-readable module name")
    p.add_argument("--dest", required=True, help="Destination directory (module created under <dest>/<code>/)")
    p.add_argument("--preset", default="generic", choices=sorted(PRESETS), help="Content preset")
    p.add_argument("--force", action="store_true", help="Overwrite an existing module directory")
    p.set_defaults(func=cmd_create)
    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
