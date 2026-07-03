#!/usr/bin/env python3
"""Regression tests for SPECTRA evidence-logger multimodal/media support."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
import unittest.mock as mock
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "evidence-logger.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


el = load_module("evidence_logger", SCRIPT)


class MediaTypeTests(unittest.TestCase):
    def test_image_extensions(self):
        for name in ("a.png", "b.JPG", "c.jpeg", "d.gif", "e.webp", "diagram.svg"):
            self.assertEqual(el.detect_media_type(name), "image", name)

    def test_document_extensions(self):
        for name in ("r.pdf", "n.md", "x.txt", "d.docx"):
            self.assertEqual(el.detect_media_type(name), "document", name)

    def test_capture_and_binary(self):
        self.assertEqual(el.detect_media_type("net.pcap"), "capture")
        self.assertEqual(el.detect_media_type("mal.exe"), "binary")

    def test_unknown_is_other(self):
        self.assertEqual(el.detect_media_type("weird.xyz"), "other")
        self.assertEqual(el.detect_media_type("noext"), "other")

    def test_dotfile_and_path_edges(self):
        self.assertEqual(el.detect_media_type(".png"), "other")  # dotfile, no suffix
        self.assertEqual(el.detect_media_type("/tmp/dir.png/noext"), "other")

    def test_md_inline_neutralizes_injection(self):
        out = el._md_inline("line1\n## Injected\n```evil")
        self.assertNotIn("\n", out)
        self.assertNotIn("##", out.split(" ", 1)[0])  # heading not at line start
        self.assertNotIn("```", out)


class AcquireMediaIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.eng_dir = root / "engagements" / "ENG-M"
        self.eng_dir.mkdir(parents=True)
        self.eng = self.eng_dir / "engagement.yaml"
        self.eng.write_text("engagement: {id: \"ENG-M\", type: \"pentest\"}\n", encoding="utf-8")
        # A minimal PNG-ish file (bytes; content irrelevant to hashing).
        self.img = root / "screenshot.png"
        self.img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"spectra-test-image-bytes")

    def tearDown(self):
        self.tmp.cleanup()

    def _registry(self):
        import yaml
        reg = Path(self.tmp.name) / "evidence" / "ENG-M" / "evidence-registry.yaml"
        return yaml.safe_load(reg.read_text(encoding="utf-8"))["evidence_registry"]

    def test_acquire_image_records_media_and_analysis(self):
        argv = [
            "evidence-logger.py", "acquire",
            "--engagement", str(self.eng),
            "--description", "Login page screenshot",
            "--source", "browser",
            "--type", "screenshot",
            "--file", str(self.img),
            "--analysis", "Shows an exposed admin panel with a default-credentials banner.",
        ]
        with mock.patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
            el.main()
        items = self._registry()["items"]
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["media_type"], "image")
        self.assertIn("admin panel", item["visual_analysis"])
        # The image is hashed -> a visual conclusion is anchored to a verifiable file.
        self.assertTrue(item["hash_sha256"] and item["hash_sha256"] != "N/A")

    def _write_legacy_registry(self):
        # A registry whose item predates media_type/visual_analysis.
        import yaml
        reg_dir = Path(self.tmp.name) / "evidence" / "ENG-M"
        reg_dir.mkdir(parents=True, exist_ok=True)
        registry = {
            "evidence_registry": {
                "engagement_id": "ENG-M", "integrity_status": "UNVERIFIED",
                "item_count": 1, "items": [{
                    "id": "EV-ENG-M-001", "description": "legacy item",
                    "source_system": "old", "source_type": "document",
                    "hash_sha256": "abc", "status": "active",
                    "acquisition_timestamp": "2026-01-01T00:00:00Z",
                    "custody_log": [],
                }],
            }
        }
        (reg_dir / "evidence-registry.yaml").write_text(yaml.safe_dump(registry), encoding="utf-8")

    def test_export_legacy_registry_without_new_fields(self):
        # Backward compatibility: a registry missing the new fields must still
        # export and inventory without error.
        self._write_legacy_registry()
        report = Path(self.tmp.name) / "coc.md"
        commands = [
            ["evidence-logger.py", "inventory", "--engagement", str(self.eng)],
            ["evidence-logger.py", "export", "--engagement", str(self.eng),
             "--output", str(report)],
        ]
        for argv in commands:
            with mock.patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
                el.main()  # must not raise
        self.assertTrue(report.is_file())

    def test_export_analysis_markdown_injection_neutralized(self):
        # Acquire with a malicious analysis, then export; the custody table must
        # survive and no raw injected heading/fence may appear.
        argv = [
            "evidence-logger.py", "acquire",
            "--engagement", str(self.eng),
            "--description", "shot", "--source", "browser", "--type", "screenshot",
            "--file", str(self.img),
            "--analysis", "ok\n## INJECTED HEADING\n```\n| evil | table |",
        ]
        with mock.patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
            el.main()
        report = Path(self.tmp.name) / "coc.md"
        eargv = ["evidence-logger.py", "export", "--engagement", str(self.eng),
                 "--output", str(report)]
        with mock.patch.object(sys, "argv", eargv), redirect_stdout(io.StringIO()):
            el.main()
        text = report.read_text(encoding="utf-8")
        self.assertNotIn("\n## INJECTED HEADING", text)  # heading not on its own line
        self.assertIn("| # | Timestamp | Action", text)  # custody table intact

    def test_acquire_without_file_media_none(self):
        argv = [
            "evidence-logger.py", "acquire",
            "--engagement", str(self.eng),
            "--description", "Verbal note",
            "--source", "interview",
            "--type", "other",
        ]
        with mock.patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
            el.main()
        item = self._registry()["items"][0]
        self.assertEqual(item["media_type"], "none")
        self.assertEqual(item["visual_analysis"], "")


if __name__ == "__main__":
    unittest.main()
