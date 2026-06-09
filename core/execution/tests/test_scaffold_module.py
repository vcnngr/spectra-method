#!/usr/bin/env python3
"""Regression tests for the SPECTRA Module Scaffold."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scaffold-module.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


sm = load_module("scaffold_module", SCRIPT)


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dest = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    # -- validation --------------------------------------------------------

    def test_invalid_code_raises(self):
        for bad in ("OT", "1mod", "with-dash", "x", "toolongmodulename123"):
            with self.assertRaises(ValueError, msg=bad):
                sm.generate(bad, "X", str(self.dest))

    def test_unknown_preset_raises(self):
        with self.assertRaises(ValueError):
            sm.generate("mod", "Mod", str(self.dest), preset="nope")

    def test_reserved_code_rejected(self):
        for code in ("core", "rtk", "soc", "irt", "grc"):
            with self.assertRaises(ValueError, msg=code):
                sm.generate(code, "X", str(self.dest))
            with self.assertRaises(ValueError, msg=code):  # even with force
                sm.generate(code, "X", str(self.dest), force=True)

    def test_underscore_code_rejected(self):
        with self.assertRaises(ValueError):
            sm.generate("with_underscore", "X", str(self.dest))

    def test_dest_traversal_rejected(self):
        with self.assertRaises(ValueError):
            sm.generate("mod", "X", "../../etc")

    def test_generated_workflow_is_validator_shaped(self):
        result = sm.generate("mymod", "My Module", str(self.dest))
        wf_dir = self.dest / "mymod" / "workflows" / result["workflow"]
        self.assertTrue((wf_dir / "workflow.md").is_file())
        step = wf_dir / "steps-c" / "step-01-init.md"
        self.assertTrue(step.is_file())
        text = step.read_text()
        self.assertIn("SUCCESS", text)
        self.assertIn("FAILURE", text)

    def test_force_replaces_stale_files(self):
        sm.generate("mymod", "My Module", str(self.dest))
        stale = self.dest / "mymod" / "agents" / "stale-extra.txt"
        stale.write_text("leftover", encoding="utf-8")
        sm.generate("mymod", "My Module", str(self.dest), force=True)
        self.assertFalse(stale.exists())  # temp-dir swap removed the stale file

    def test_name_injection_rejected(self):
        for bad in ('My "Kit"', "Line\nBreak", "back\\slash", "quote'd"):
            with self.assertRaises(ValueError, msg=bad):
                sm.generate("mod", bad, str(self.dest))

    def test_generated_module_yaml_valid_with_special_name(self):
        import yaml
        sm.generate("mod", "OT/ICS Security & Safety", str(self.dest))
        meta = yaml.safe_load((self.dest / "mod" / "module.yaml").read_text())
        self.assertEqual(meta["code"], "mod")
        self.assertIn("OT/ICS Security", meta["name"])

    def test_refuse_overwrite_without_force(self):
        sm.generate("mod", "Mod", str(self.dest))
        with self.assertRaises(FileExistsError):
            sm.generate("mod", "Mod", str(self.dest))
        # force succeeds
        sm.generate("mod", "Mod", str(self.dest), force=True)

    # -- generic generation ------------------------------------------------

    def test_generic_structure(self):
        result = sm.generate("mymod", "My Module", str(self.dest))
        mod = self.dest / "mymod"
        self.assertTrue((mod / "module.yaml").is_file())
        self.assertTrue((mod / "config.yaml").is_file())
        self.assertTrue((mod / "README.md").is_file())
        agent_skill = mod / "agents" / result["agent"] / "SKILL.md"
        wf_skill = mod / "workflows" / result["workflow"] / "SKILL.md"
        self.assertTrue(agent_skill.is_file())
        self.assertTrue(wf_skill.is_file())
        self.assertTrue((agent_skill.parent / "spectra-skill-manifest.yaml").is_file())

    def test_generated_yaml_is_valid(self):
        import yaml
        sm.generate("mymod", "My Module", str(self.dest))
        mod = self.dest / "mymod"
        module_meta = yaml.safe_load((mod / "module.yaml").read_text())
        self.assertEqual(module_meta["code"], "mymod")
        # manifests parse
        for mf in mod.rglob("spectra-skill-manifest.yaml"):
            data = yaml.safe_load(mf.read_text())
            self.assertIn(data["type"], ("agent", "skill"))

    def test_agent_skill_has_required_sections(self):
        # The validator requires these sections for agent SKILL.md files.
        result = sm.generate("mymod", "My Module", str(self.dest))
        text = (self.dest / "mymod" / "agents" / result["agent"] / "SKILL.md").read_text()
        for section in ("## Overview", "## On Activation", "## Identity",
                        "## Communication Style", "## Principles"):
            self.assertIn(section, text, section)
        self.assertTrue(text.startswith("---\nname: "))

    def test_manifest_rows_returned(self):
        import csv as _csv
        result = sm.generate("mymod", "My Module", str(self.dest))
        self.assertIn(result["agent"], result["suggested_agent_manifest_row"])
        self.assertIn("_spectra/mymod/agents/", result["suggested_agent_manifest_row"])
        self.assertIn(result["workflow"], result["suggested_skill_manifest_row"])
        # Agent path column is a DIRECTORY (no /SKILL.md), matching agent-manifest.csv.
        agent_fields = next(_csv.reader([result["suggested_agent_manifest_row"]]))
        self.assertEqual(len(agent_fields), 12)
        self.assertEqual(agent_fields[10], "_spectra/mymod/agents/" + result["agent"])
        self.assertNotIn("SKILL.md", agent_fields[10])
        # Skill row path IS the SKILL.md file.
        skill_fields = next(_csv.reader([result["suggested_skill_manifest_row"]]))
        self.assertTrue(skill_fields[4].endswith("/SKILL.md"))

    # -- ot-ics preset + safety boundary -----------------------------------

    def test_ot_ics_preset_content(self):
        result = sm.generate("ot", "OT/ICS Security", str(self.dest), preset="ot-ics")
        self.assertEqual(result["agent"], "spectra-agent-ot-ics")
        self.assertEqual(result["workflow"], "spectra-ot-assessment")
        agent_text = (self.dest / "ot" / "agents" / result["agent"] / "SKILL.md").read_text()
        self.assertIn("IEC 62443", agent_text)
        self.assertIn("ICS ATT&CK", agent_text)
        self.assertIn("Purdue", agent_text)

    def test_ot_ics_safety_boundary_present(self):
        result = sm.generate("ot", "OT/ICS Security", str(self.dest), preset="ot-ics")
        agent_text = (self.dest / "ot" / "agents" / result["agent"] / "SKILL.md").read_text()
        wf_text = (self.dest / "ot" / "workflows" / result["workflow"] / "SKILL.md").read_text()
        # Assessment-only boundary: never destructive PLC manipulation.
        self.assertIn("ASSESSMENT", agent_text)
        self.assertIn("NEVER", agent_text)
        self.assertIn("safety-instrumented systems", agent_text)
        self.assertIn("ASSESSMENT-ONLY", wf_text)

    # -- CLI ---------------------------------------------------------------

    def test_cli_create(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            sm.main(["create", "--code", "ot", "--name", "OT/ICS Security",
                     "--dest", str(self.dest), "--preset", "ot-ics"])
        import json
        data = json.loads(buf.getvalue())
        self.assertEqual(data["module_code"], "ot")
        self.assertEqual(data["preset"], "ot-ics")


if __name__ == "__main__":
    unittest.main()
