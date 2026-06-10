#!/usr/bin/env python3
"""Regression tests for SPECTRA Run Accounting (per-engagement run log)."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "run-accounting.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ra = load_module("run_accounting", SCRIPT)

TS = "2026-06-10T00:00:00Z"


class BuildRecordTests(unittest.TestCase):
    def test_executed_local_exit_code(self):
        result = {"tool": "nmap", "target": "10.0.0.5", "status": "executed",
                  "via": "local", "dry_run": False,
                  "execution": {"exit_code": 0}}
        rec = ra.build_record(result, now=TS)
        self.assertEqual(rec["ts"], TS)
        self.assertEqual(rec["tool"], "nmap")
        self.assertEqual(rec["status"], "executed")
        self.assertEqual(rec["exit_code"], 0)
        self.assertEqual(rec["via"], "local")
        self.assertFalse(rec["dry_run"])

    def test_executed_remote_exit_code(self):
        result = {"tool": "nmap", "target": "10.0.0.5", "status": "executed_remote",
                  "via": "exec-target",
                  "remote": {"execution": {"exit_code": 2}}}
        rec = ra.build_record(result, now=TS)
        self.assertEqual(rec["exit_code"], 2)
        self.assertEqual(rec["via"], "exec-target")

    def test_blocked_has_no_exit_code(self):
        rec = ra.build_record({"tool": "nmap", "target": "8.8.8.8",
                               "status": "blocked"}, now=TS)
        self.assertIsNone(rec["exit_code"])

    def test_planned_dry_run(self):
        rec = ra.build_record({"tool": "nmap", "target": "10.0.0.5",
                               "status": "planned", "dry_run": True}, now=TS)
        self.assertTrue(rec["dry_run"])
        self.assertIsNone(rec["exit_code"])

    def test_error_field_carried(self):
        rec = ra.build_record({"tool": "httpx", "target": "x", "status": "unavailable",
                               "error": "binary not found"}, now=TS)
        self.assertEqual(rec["error"], "binary not found")

    def test_default_now_is_utc_z(self):
        rec = ra.build_record({"tool": "dig", "target": "x", "status": "blocked"})
        self.assertTrue(rec["ts"].endswith("Z"))


class LogIOTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.eng = Path(self.tmp.name) / "engagement.yaml"
        self.eng.write_text("engagement: {}\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_log_path_beside_engagement(self):
        self.assertEqual(ra.run_log_path(str(self.eng)),
                         Path(self.tmp.name).resolve() / "run-log.jsonl")

    def test_record_appends_and_reads_back(self):
        ra.record(str(self.eng), {"tool": "nmap", "target": "10.0.0.5",
                                  "status": "executed", "execution": {"exit_code": 0}}, now=TS)
        ra.record(str(self.eng), {"tool": "dig", "target": "10.0.0.6",
                                  "status": "blocked"}, now=TS)
        recs = ra.read_log(str(self.eng))
        self.assertEqual(len(recs), 2)
        self.assertEqual(recs[0]["tool"], "nmap")
        self.assertEqual(recs[1]["status"], "blocked")

    def test_read_log_missing_is_empty(self):
        self.assertEqual(ra.read_log(str(self.eng)), [])

    def test_read_log_skips_blank_and_corrupt(self):
        log = ra.run_log_path(str(self.eng))
        log.write_text(json.dumps({"tool": "nmap", "status": "executed",
                                   "exit_code": 0}) + "\n\nnot-json\n"
                       + json.dumps({"tool": "dig", "status": "blocked"}) + "\n",
                       encoding="utf-8")
        recs = ra.read_log(str(self.eng))
        self.assertEqual(len(recs), 2)

    def test_summarize_counts(self):
        for r in [
            {"tool": "nmap", "target": "a", "status": "executed", "execution": {"exit_code": 0}},
            {"tool": "nmap", "target": "b", "status": "executed", "execution": {"exit_code": 4}},
            {"tool": "dig", "target": "c", "status": "blocked"},
            {"tool": "httpx", "target": "d", "status": "planned", "dry_run": True},
            {"tool": "nmap", "target": "e", "status": "executed_remote",
             "via": "exec-target", "remote": {"execution": {"exit_code": 0}}},
        ]:
            ra.record(str(self.eng), r, now=TS)
        s = ra.summarize(str(self.eng))
        self.assertEqual(s["total"], 5)
        self.assertEqual(s["executed"], 3)        # 2 local + 1 remote
        self.assertEqual(s["blocked"], 1)
        self.assertEqual(s["planned"], 1)
        self.assertEqual(s["nonzero_exit"], 1)    # the exit_code 4
        self.assertEqual(s["by_tool"]["nmap"], 3)
        self.assertEqual(s["first_ts"], TS)

    def test_summarize_recent_is_reverse_and_limited(self):
        for i in range(5):
            ra.record(str(self.eng), {"tool": f"t{i}", "target": "x",
                                      "status": "blocked"}, now=TS)
        s = ra.summarize(str(self.eng), limit=2)
        self.assertEqual(len(s["recent"]), 2)
        self.assertEqual(s["recent"][0]["tool"], "t4")  # most recent first
        self.assertEqual(s["recent"][1]["tool"], "t3")

    def test_read_log_skips_valid_json_non_objects(self):
        # Valid JSON that is not an object (scalar/array) is corrupt for our
        # purposes and must never reach the summarizer.
        log = ra.run_log_path(str(self.eng))
        log.write_text("1\n\"str\"\n[1,2]\n"
                       + json.dumps({"tool": "nmap", "status": "blocked"}) + "\n",
                       encoding="utf-8")
        recs = ra.read_log(str(self.eng))
        self.assertEqual(len(recs), 1)
        # And summarize must not crash on the surrounding noise.
        self.assertEqual(ra.summarize(str(self.eng))["total"], 1)

    def test_summarize_record_without_ts_does_not_crash(self):
        log = ra.run_log_path(str(self.eng))
        log.write_text(json.dumps({"tool": "nmap", "status": "blocked"}) + "\n",
                       encoding="utf-8")
        s = ra.summarize(str(self.eng))
        self.assertEqual(s["total"], 1)
        self.assertIsNone(s["first_ts"])

    def test_summarize_empty(self):
        s = ra.summarize(str(self.eng))
        self.assertEqual(s["total"], 0)
        self.assertIsNone(s["first_ts"])
        self.assertEqual(s["recent"], [])


if __name__ == "__main__":
    unittest.main()
