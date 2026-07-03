#!/usr/bin/env python3
"""SPECTRA Quickstart (Layer 3).

The fastest way to understand a method is to run it once. This scaffolds a
ready-to-use engagement into the operator's workspace — either the self-contained
**demo** (a fictional, loopback-only engagement with sample findings and a worked
War Room debrief) or a **scenario template** (web pentest, cloud IR, OT/ICS) — and
prints a guided tour so value lands in minutes without hand-writing YAML.

Everything it copies is shipped with SPECTRA; it writes nothing but the chosen
files into the destination. No network, no execution.

CLI:
  quickstart.py list
  quickstart.py init --template demo --dest ./spectra-quickstart [--force]
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

_CORE = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = _CORE / "templates" / "engagements"
DEMO_DIR = _CORE / "examples" / "demo-engagement"
TEMPLATE_SUFFIX = ".engagement.yaml"


def list_templates() -> list[str]:
    """Available scenario templates, plus the always-present 'demo'."""
    names = ["demo"]
    if TEMPLATES_DIR.is_dir():
        names += sorted(p.name[: -len(TEMPLATE_SUFFIX)]
                        for p in TEMPLATES_DIR.iterdir()
                        if p.name.endswith(TEMPLATE_SUFFIX))
    return names


def _assert_within(dest_real: str, target: Path) -> None:
    """Refuse to write through a symlink that escapes the destination. Guards
    both a symlinked parent dir (`dest/findings -> /tmp/outside`) and a
    symlinked target file (`dest/engagement.yaml -> /tmp/outside/x`) — the latter
    matters because --force skips the existence check, and shutil.copy2 would
    otherwise follow the link and write outside --dest."""
    if target.is_symlink():
        raise ValueError(f"refusing to write through a symlink: {target}")
    real_parent = os.path.realpath(target.parent)
    if real_parent != dest_real and not real_parent.startswith(dest_real + os.sep):
        raise ValueError(f"refusing to write outside destination: {target}")


def _prepare_target(dest_real: str, target: Path) -> None:
    """Validate containment, then remove any existing target before copying.

    Unlinking first breaks a hardlink: shutil.copy2 onto an existing path writes
    *through* the inode, so a `dest/engagement.yaml` hardlinked to an outside
    file would otherwise be modified even with --force. Removing the link first
    (it only decrements the outside file's link count) makes the copy create a
    fresh, independent file inside --dest."""
    _assert_within(dest_real, target)
    if target.exists():
        target.unlink()


def _copy_demo(dest: Path, force: bool = False) -> list[str]:
    """Copy the full demo engagement (engagement.yaml + findings + debrief).

    Refuses to clobber ANY existing demo file unless force — not just
    engagement.yaml — so a partially-populated destination is never silently
    overwritten, and never follows a symlink out of the destination."""
    if not (DEMO_DIR / "engagement.yaml").is_file():
        raise FileNotFoundError(f"demo engagement assets missing: {DEMO_DIR}")
    # Copy only the demo's authored assets, never runtime artifacts that may have
    # accumulated in the source (run logs, posture snapshots) — so a fresh
    # quickstart is always clean regardless of prior local runs.
    sources = [s for s in sorted(DEMO_DIR.rglob("*"))
               if s.is_file() and s.name != "run-log.jsonl"
               and "posture" not in s.relative_to(DEMO_DIR).parts]
    dest_real = os.path.realpath(dest)
    if not force:
        clashes = [str(s.relative_to(DEMO_DIR)) for s in sources
                   if (dest / s.relative_to(DEMO_DIR)).exists()]
        if clashes:
            raise FileExistsError(
                f"these files already exist in {dest} (pass --force to overwrite): "
                f"{', '.join(clashes)}")
    written: list[str] = []
    for src in sources:
        rel = src.relative_to(DEMO_DIR)
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        _prepare_target(dest_real, out)
        shutil.copy2(src, out)
        written.append(str(rel))
    return written


def scaffold(template: str, dest: str, force: bool = False) -> dict[str, Any]:
    """Scaffold the chosen template/demo into dest. Returns a manifest."""
    available = list_templates()
    if template not in available:
        raise ValueError(f"unknown template {template!r}; choose from {', '.join(available)}")

    dest_path = Path(dest)
    eng = dest_path / "engagement.yaml"
    if eng.exists() and not force:
        raise FileExistsError(f"{eng} already exists; pass --force to overwrite")
    dest_path.mkdir(parents=True, exist_ok=True)

    if template == "demo":
        written = _copy_demo(dest_path, force=force)
    else:
        src = TEMPLATES_DIR / f"{template}{TEMPLATE_SUFFIX}"
        if not src.is_file():
            raise FileNotFoundError(f"template not found: {src}")
        _prepare_target(os.path.realpath(dest_path), eng)
        shutil.copy2(src, eng)
        written = ["engagement.yaml"]

    return {
        "template": template,
        "dest": str(dest_path.resolve()),
        "engagement": str(eng.resolve()),
        "files": written,
    }


def tour(manifest: dict[str, Any]) -> list[str]:
    """Guided next steps after scaffolding — the 5-minute tour."""
    eng = manifest["engagement"]
    dest = manifest["dest"]
    is_demo = manifest["template"] == "demo"
    steps = [
        f"Engagement scaffolded at: {eng}",
        f"Validate it:        spectra engagement validate --engagement {eng}",
    ]
    if is_demo:
        steps += [
            "Preview a gated scan (nothing runs): a dry-run on 127.0.0.1 is "
            "in scope and plans; 8.8.8.8 is refused as out of scope",
            f"Snapshot the posture:   spectra posture snapshot --engagement {eng}",
            f"Export the findings:    spectra export --engagement {eng} --format md",
            f"See the flagship:       open {dest}/war-room-debrief.md, then run "
            f"the 'spectra-war-room' skill on this engagement in Claude Code or Codex",
        ]
    else:
        steps += [
            "Fill the CAPS placeholders (client, dates, scope) and set status: active",
            "Then re-validate, and start the recommended workflow noted at the top of the file",
        ]
    return steps


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def cmd_list(args: argparse.Namespace) -> None:
    print(json.dumps({"templates": list_templates()}, indent=2))
    sys.exit(0)


def cmd_init(args: argparse.Namespace) -> None:
    try:
        manifest = scaffold(args.template, args.dest, force=args.force)
    except (ValueError, FileExistsError, FileNotFoundError, NotADirectoryError,
            PermissionError, OSError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(3)
    manifest["tour"] = tour(manifest)
    print(json.dumps(manifest, indent=2))
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quickstart.py",
        description="Scaffold a demo or scenario engagement and print a guided tour.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_l = sub.add_parser("list", help="List available templates (incl. demo)")
    p_l.set_defaults(func=cmd_list)

    p_i = sub.add_parser("init", help="Scaffold a template/demo into a directory")
    p_i.add_argument("--template", default="demo", help="demo, web-pentest, cloud-ir, ot-assessment")
    p_i.add_argument("--dest", default="./spectra-quickstart", help="Destination directory")
    p_i.add_argument("--force", action="store_true", help="Overwrite an existing engagement.yaml")
    p_i.set_defaults(func=cmd_init)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
