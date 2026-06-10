#!/usr/bin/env python3
"""Regression tests for SPECTRA Quickstart scaffolding."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "quickstart.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


qs = load_module("quickstart", SCRIPT)


class TemplateListingTests(unittest.TestCase):
    def test_demo_and_scenarios_present(self):
        names = qs.list_templates()
        self.assertIn("demo", names)
        for scenario in ("web-pentest", "cloud-ir", "ot-assessment"):
            self.assertIn(scenario, names)

    def test_shipped_template_files_exist(self):
        for scenario in ("web-pentest", "cloud-ir", "ot-assessment"):
            self.assertTrue((qs.TEMPLATES_DIR / f"{scenario}.engagement.yaml").is_file())

    def test_demo_assets_shipped(self):
        self.assertTrue((qs.DEMO_DIR / "engagement.yaml").is_file())
        self.assertTrue((qs.DEMO_DIR / "war-room-debrief.md").is_file())
        self.assertTrue(list((qs.DEMO_DIR / "findings").glob("*.yaml")))


class ScaffoldTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dest = Path(self.tmp.name) / "ws"

    def tearDown(self):
        self.tmp.cleanup()

    def test_scaffold_demo_copies_findings_and_debrief(self):
        m = qs.scaffold("demo", str(self.dest))
        self.assertEqual(m["template"], "demo")
        self.assertTrue((self.dest / "engagement.yaml").is_file())
        self.assertTrue((self.dest / "war-room-debrief.md").is_file())
        self.assertTrue(list((self.dest / "findings").glob("*.yaml")))
        self.assertIn("engagement.yaml", m["files"])

    def test_scaffold_scenario_copies_engagement_only(self):
        m = qs.scaffold("web-pentest", str(self.dest))
        self.assertEqual(m["files"], ["engagement.yaml"])
        self.assertIn("Web Application", (self.dest / "engagement.yaml").read_text())

    def test_scaffold_demo_excludes_runtime_artifacts(self):
        m = qs.scaffold("demo", str(self.dest))
        # a clean quickstart never ships a stray run log or posture history
        self.assertFalse((self.dest / "run-log.jsonl").exists())
        self.assertNotIn("run-log.jsonl", m["files"])
        self.assertFalse((self.dest / "posture").exists())

    def test_scaffold_unknown_template_raises(self):
        with self.assertRaises(ValueError):
            qs.scaffold("nope", str(self.dest))

    def test_scaffold_refuses_overwrite_without_force(self):
        qs.scaffold("demo", str(self.dest))
        with self.assertRaises(FileExistsError):
            qs.scaffold("web-pentest", str(self.dest))

    def test_scaffold_force_overwrites(self):
        qs.scaffold("demo", str(self.dest))
        m = qs.scaffold("web-pentest", str(self.dest), force=True)
        self.assertEqual(m["template"], "web-pentest")

    def test_demo_refuses_clobber_of_any_file(self):
        # Pre-create a demo sub-file but NOT engagement.yaml; copy must still refuse.
        (self.dest / "findings").mkdir(parents=True)
        (self.dest / "war-room-debrief.md").write_text("mine", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            qs.scaffold("demo", str(self.dest))
        # the pre-existing file is untouched
        self.assertEqual((self.dest / "war-room-debrief.md").read_text(), "mine")

    def test_demo_refuses_symlink_escape(self):
        # A pre-existing findings/ symlink pointing outside dest must not let the
        # copy write through it.
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir()
        self.dest.mkdir(parents=True)
        (self.dest / "findings").symlink_to(outside, target_is_directory=True)
        with self.assertRaises((ValueError, FileExistsError)):
            qs.scaffold("demo", str(self.dest), force=True)
        # nothing was written into the outside directory
        self.assertEqual(list(outside.iterdir()), [])

    def test_force_refuses_file_symlink_escape(self):
        # A target FILE that is itself a symlink out of dest must be refused even
        # with --force (which skips the existence/clash check).
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir()
        secret = outside / "secret.yaml"
        secret.write_text("original", encoding="utf-8")
        self.dest.mkdir(parents=True)
        (self.dest / "engagement.yaml").symlink_to(secret)
        with self.assertRaises(ValueError):
            qs.scaffold("web-pentest", str(self.dest), force=True)
        self.assertEqual(secret.read_text(), "original")  # untouched

    def test_force_refuses_demo_file_symlink_escape(self):
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir()
        secret = outside / "war-room-debrief.md"
        secret.write_text("original", encoding="utf-8")
        self.dest.mkdir(parents=True)
        (self.dest / "war-room-debrief.md").symlink_to(secret)
        with self.assertRaises(ValueError):
            qs.scaffold("demo", str(self.dest), force=True)
        self.assertEqual(secret.read_text(), "original")

    def test_force_does_not_modify_hardlinked_outside_file(self):
        # A target hardlinked to an outside file must NOT be written through:
        # copy onto an existing inode would modify the outside file even with
        # --force. The scaffold unlinks first, leaving the outside file intact.
        import os
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir()
        secret = outside / "secret.yaml"
        secret.write_text("original-secret", encoding="utf-8")
        self.dest.mkdir(parents=True)
        os.link(secret, self.dest / "engagement.yaml")   # hardlink (same inode)
        qs.scaffold("web-pentest", str(self.dest), force=True)
        self.assertEqual(secret.read_text(), "original-secret")        # untouched
        self.assertIn("Web Application", (self.dest / "engagement.yaml").read_text())
        self.assertNotEqual((self.dest / "engagement.yaml").stat().st_ino, secret.stat().st_ino)

    def test_cli_init_bad_dest_exits_3(self):
        import io
        from contextlib import redirect_stdout
        afile = Path(self.tmp.name) / "afile"
        afile.write_text("x", encoding="utf-8")
        bad = afile / "child"   # parent is a file -> NotADirectoryError
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            qs.main(["init", "--template", "demo", "--dest", str(bad)])
        self.assertEqual(cm.exception.code, 3)

    def test_tour_uses_absolute_debrief_path(self):
        m = qs.scaffold("demo", str(self.dest))
        steps = qs.tour(m)
        debrief_step = next(s for s in steps if "war-room-debrief.md" in s)
        self.assertIn(str(self.dest.resolve()), debrief_step)

    def test_tour_demo_mentions_war_room(self):
        m = qs.scaffold("demo", str(self.dest))
        steps = " ".join(qs.tour(m))
        self.assertIn("war-room", steps.lower())
        self.assertIn("posture", steps.lower())

    def test_cli_init_emits_manifest_and_tour(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stdout(buf):
            qs.main(["init", "--template", "demo", "--dest", str(self.dest)])
        self.assertEqual(cm.exception.code, 0)
        out = json.loads(buf.getvalue())
        self.assertEqual(out["template"], "demo")
        self.assertTrue(out["tour"])


class DemoValidatesTests(unittest.TestCase):
    """The shipped demo engagement must pass SPECTRA's own validator."""

    def test_demo_engagement_validates(self):
        import yaml
        es_path = Path(__file__).resolve().parents[1] / "engagement-state.py"
        es = load_module("engagement_state", es_path)
        data = yaml.safe_load((qs.DEMO_DIR / "engagement.yaml").read_text(encoding="utf-8"))
        result = es.validate_document(data)
        self.assertEqual(result.get("errors", []), [],
                         f"demo engagement has validation errors: {result.get('errors')}")

    def test_scenario_templates_structurally_valid(self):
        # Templates carry CAPS placeholders (so they aren't 'active'), but their
        # structure/keys must be present so a filled copy validates.
        import yaml
        for scenario in ("web-pentest", "cloud-ir", "ot-assessment"):
            data = yaml.safe_load(
                (qs.TEMPLATES_DIR / f"{scenario}.engagement.yaml").read_text(encoding="utf-8"))
            eng = data["engagement"]
            self.assertIn("authorization", eng)
            self.assertIn("rules_of_engagement", eng)
            self.assertIn("scope", eng)


if __name__ == "__main__":
    unittest.main()
