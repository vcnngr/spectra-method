#!/usr/bin/env python3
"""Regression tests for SPECTRA Remediation Export."""

from __future__ import annotations

import csv
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "remediation-export.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


rx = load_module("remediation_export", SCRIPT)

FINDINGS = [
    {"id": "F1", "title": "SQL Injection", "severity": "critical", "status": "open",
     "cvss": 9.8, "description": "param id is injectable", "remediation": "parametrize",
     "source_path": "/x/F1.yaml"},
    {"id": "F2", "title": "Verbose errors", "severity": "info", "status": "resolved"},
]


class FormatterTests(unittest.TestCase):
    def test_sarif_is_valid_json_210(self):
        doc = json.loads(rx.to_sarif(FINDINGS))
        self.assertEqual(doc["version"], "2.1.0")
        run = doc["runs"][0]
        self.assertEqual(run["tool"]["driver"]["name"], "SPECTRA")
        self.assertEqual(len(run["results"]), 2)
        self.assertEqual(run["results"][0]["ruleId"], "F1")
        self.assertEqual(run["results"][0]["level"], "error")   # critical -> error
        self.assertEqual(run["results"][1]["level"], "note")    # info -> note

    def test_csv_has_header_and_rows(self):
        rows = list(csv.DictReader(io.StringIO(rx.to_csv(FINDINGS))))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["id"], "F1")
        self.assertEqual(rows[0]["severity"], "critical")
        self.assertEqual(rows[1]["severity"], "informational")  # info normalized

    def test_sarif_result_has_location(self):
        doc = json.loads(rx.to_sarif(FINDINGS))
        res0 = doc["runs"][0]["results"][0]
        self.assertEqual(res0["locations"][0]["physicalLocation"]["artifactLocation"]["uri"],
                         "/x/F1.yaml")
        # F2 has no source -> no locations key (not an empty/invalid one)
        self.assertNotIn("locations", doc["runs"][0]["results"][1])

    def test_csv_formula_injection_neutralized(self):
        rows = list(csv.reader(io.StringIO(
            rx.to_csv([{"id": "F3", "title": "=cmd|' /c calc'!A1",
                        "severity": "low", "status": "open"}]))))
        # title cell is prefixed with a quote so it is treated as text
        self.assertTrue(rows[1][1].startswith("'="))

    def test_csv_has_remediation_column(self):
        self.assertIn("remediation", rx.CSV_COLUMNS)
        rows = list(csv.DictReader(io.StringIO(rx.to_csv(FINDINGS))))
        self.assertEqual(rows[0]["remediation"], "parametrize")

    def test_csv_injection_neutralized_in_all_text_fields(self):
        # severity/status are also escaped if a finding smuggles a formula there
        rows = list(csv.reader(io.StringIO(
            rx.to_csv([{"id": "=A", "title": "ok", "severity": "+evil",
                        "status": "=cmd", "remediation": "@x"}]))))
        r = rows[1]
        self.assertTrue(r[0].startswith("'="))   # id
        self.assertTrue(r[2].startswith("'+"))   # severity
        self.assertTrue(r[3].startswith("'="))   # status
        self.assertTrue(r[5].startswith("'@"))   # remediation

    def test_markdown_sections(self):
        md = rx.to_markdown(FINDINGS)
        self.assertIn("## [CRITICAL] SQL Injection", md)
        self.assertIn("`F1`", md)
        self.assertIn("**Remediation**", md)
        self.assertIn("parametrize", md)

    def test_markdown_empty(self):
        self.assertIn("No findings", rx.to_markdown([]))

    def test_export_unknown_format_raises(self):
        with tempfile.TemporaryDirectory() as d:
            eng = Path(d) / "engagement.yaml"
            eng.write_text("engagement:\n  id: ENG-T\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                rx.export(str(eng), "nope")


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.eng = self.dir / "engagement.yaml"
        self.eng.write_text("engagement:\n  id: ENG-T\n", encoding="utf-8")
        fdir = self.dir / "findings"
        fdir.mkdir()
        (fdir / "F1.yaml").write_text(
            "id: F1\ntitle: SQLi\nseverity: critical\ncvss: 9.8\n"
            "description: injectable\nremediation: parametrize\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_cli_export_sarif_to_file(self):
        out = self.dir / "out.sarif"
        with self.assertRaises(SystemExit) as cm, io.StringIO() as buf:
            from contextlib import redirect_stdout
            with redirect_stdout(buf):
                rx.main(["export", "--engagement", str(self.eng),
                         "--format", "sarif", "--out", str(out)])
        self.assertEqual(cm.exception.code, 0)
        doc = json.loads(out.read_text())
        self.assertEqual(doc["runs"][0]["results"][0]["ruleId"], "F1")

    def test_cli_export_bad_out_path_exits_3(self):
        import io as _io
        from contextlib import redirect_stdout
        bad = self.dir / "no-such-dir" / "out.sarif"
        with self.assertRaises(SystemExit) as cm, redirect_stdout(_io.StringIO()):
            rx.main(["export", "--engagement", str(self.eng),
                     "--format", "sarif", "--out", str(bad)])
        self.assertEqual(cm.exception.code, 3)

    def test_cli_export_csv_stdout(self):
        import io as _io
        from contextlib import redirect_stdout
        buf = _io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stdout(buf):
            rx.main(["export", "--engagement", str(self.eng), "--format", "csv"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("F1", buf.getvalue())
        self.assertIn("critical", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
