#!/usr/bin/env python3
"""Regression tests for the SPECTRA Benchmark Harness."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "benchmark.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


bm = load_module("benchmark", SCRIPT)


ENGAGEMENT = """\
engagement:
  id: "ENG-B"
  type: "pentest"
  rules_of_engagement: {}
  scope:
    in_scope: {networks: ["127.0.0.0/8"]}
    out_of_scope: {}
"""

SUITE = """\
suite: "echo-baseline"
cases:
  - id: "marker-present"
    tool: "_bench_echo"
    target: "127.0.0.1"
    expect:
      - {name: "target echoed", match: "127.0.0.1"}
  - id: "marker-missing"
    tool: "_bench_echo"
    target: "127.0.0.1"
    expect:
      - {name: "absent marker", match: "THIS-IS-NOT-PRESENT"}
  - id: "out-of-scope"
    tool: "_bench_echo"
    target: "8.8.8.8"
    expect:
      - {name: "x", match: "8.8.8.8"}
"""


class ScoreTests(unittest.TestCase):
    def test_marker_substring(self):
        self.assertTrue(bm._marker_matches("open", "port 22 open"))
        self.assertFalse(bm._marker_matches("closed", "port 22 open"))

    def test_marker_regex(self):
        self.assertTrue(bm._marker_matches(r"re:\d+/tcp open", "2222/tcp open"))
        self.assertFalse(bm._marker_matches(r"re:\d+/tcp closed", "2222/tcp open"))

    def test_score_case_all_matched(self):
        case = {"expect": [{"name": "a", "match": "foo"}, {"name": "b", "match": "bar"}]}
        s = bm.score_case(case, "foo and bar here")
        self.assertTrue(s["passed"])
        self.assertEqual(s["missed"], [])

    def test_score_case_partial(self):
        case = {"expect": [{"name": "a", "match": "foo"}, {"name": "b", "match": "bar"}]}
        s = bm.score_case(case, "only foo")
        self.assertFalse(s["passed"])
        self.assertEqual(s["missed"], ["b"])

    def test_score_case_no_expectations_not_passed(self):
        s = bm.score_case({"expect": []}, "anything")
        self.assertFalse(s["passed"])  # nothing to prove -> not a pass

    def test_grade_bands(self):
        def cards(passed, total):
            out = [{"status": "scored", "score": {"passed": True}} for _ in range(passed)]
            out += [{"status": "scored", "score": {"passed": False}} for _ in range(total - passed)]
            return out
        self.assertEqual(bm.grade_suite(cards(10, 10))["grade"], "A")
        self.assertEqual(bm.grade_suite(cards(8, 10))["grade"], "B")
        self.assertEqual(bm.grade_suite(cards(5, 10))["grade"], "C")
        self.assertEqual(bm.grade_suite(cards(1, 10))["grade"], "D")
        self.assertEqual(bm.grade_suite(cards(0, 10))["grade"], "F")

    def test_grade_excludes_unscored(self):
        cards = [
            {"status": "scored", "score": {"passed": True}},
            {"status": "blocked"},
            {"status": "unavailable"},
        ]
        g = bm.grade_suite(cards)
        self.assertEqual(g["cases_scored"], 1)
        self.assertEqual(g["cases_passed"], 1)
        self.assertEqual(g["cases_not_scored"], 2)
        self.assertEqual(g["pass_rate_percent"], 100.0)


class RunSuiteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.eng = root / "e.yaml"
        self.eng.write_text(ENGAGEMENT, encoding="utf-8")
        self.suite = root / "suite.yaml"
        self.suite.write_text(SUITE, encoding="utf-8")
        # Register a temporary echo-backed tool so cases really execute.
        bm.tool_adapter.ADAPTERS["_bench_echo"] = {
            "binary": "echo", "action": "recon", "read_only": True,
            "allowed_flags": set(), "value_flags": set(), "allowed_values": set(),
        }

    def tearDown(self):
        bm.tool_adapter.ADAPTERS.pop("_bench_echo", None)
        self.tmp.cleanup()

    def test_run_suite_scores_and_grades(self):
        report = bm.run_suite(str(self.suite), str(self.eng))
        by_id = {c["id"]: c for c in report["cases"]}
        # marker present -> scored + passed
        self.assertEqual(by_id["marker-present"]["status"], "scored")
        self.assertTrue(by_id["marker-present"]["score"]["passed"])
        # marker missing -> scored + failed
        self.assertEqual(by_id["marker-missing"]["status"], "scored")
        self.assertFalse(by_id["marker-missing"]["score"]["passed"])
        # out of scope -> blocked, never scored
        self.assertEqual(by_id["out-of-scope"]["status"], "blocked")
        # summary: 2 scored, 1 passed, 1 not scored
        self.assertEqual(report["summary"]["cases_scored"], 2)
        self.assertEqual(report["summary"]["cases_passed"], 1)
        self.assertEqual(report["summary"]["cases_not_scored"], 1)

    def test_run_suite_dry_run_does_not_score(self):
        report = bm.run_suite(str(self.suite), str(self.eng), dry_run=True)
        statuses = {c["status"] for c in report["cases"]}
        # in-scope cases are planned (not executed/scored); out-of-scope blocked.
        self.assertIn("planned", statuses)
        self.assertNotIn("scored", statuses)

    def test_missing_suite_raises(self):
        with self.assertRaises(FileNotFoundError):
            bm.load_suite(str(Path(self.tmp.name) / "nope.yaml"))

    def test_invalid_suite_raises(self):
        bad = Path(self.tmp.name) / "bad.yaml"
        bad.write_text("suite: x\ncases: []\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            bm.load_suite(str(bad))

    def test_suite_missing_tool_raises(self):
        bad = Path(self.tmp.name) / "b.yaml"
        bad.write_text("cases:\n  - {id: x, target: '127.0.0.1', expect: [{match: a}]}\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            bm.load_suite(str(bad))

    def test_suite_empty_expect_raises(self):
        bad = Path(self.tmp.name) / "b.yaml"
        bad.write_text("cases:\n  - {id: x, tool: nmap, target: '127.0.0.1', expect: []}\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            bm.load_suite(str(bad))

    def test_bad_regex_marker_is_missed_not_crash(self):
        # An invalid regex must not raise; it just fails to match.
        self.assertFalse(bm._marker_matches("re:(", "anything"))

    def test_all_unscorable_grade_na(self):
        cards = [{"status": "blocked"}, {"status": "unavailable"}]
        g = bm.grade_suite(cards)
        self.assertEqual(g["grade"], "N/A")

    def test_suite_string_expect_entry_raises(self):
        bad = Path(self.tmp.name) / "b.yaml"
        bad.write_text("cases:\n  - {id: x, tool: nmap, target: '127.0.0.1', expect: ['justastring']}\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            bm.load_suite(str(bad))

    def test_suite_duplicate_id_raises(self):
        bad = Path(self.tmp.name) / "b.yaml"
        bad.write_text(
            "cases:\n"
            "  - {id: dup, tool: nmap, target: '127.0.0.1', expect: [{match: a}]}\n"
            "  - {id: dup, tool: nmap, target: '127.0.0.1', expect: [{match: b}]}\n",
            encoding="utf-8")
        with self.assertRaises(ValueError):
            bm.load_suite(str(bad))

    def test_suite_scalar_args_raises(self):
        bad = Path(self.tmp.name) / "b.yaml"
        bad.write_text("cases:\n  - {id: x, tool: nmap, target: '127.0.0.1', args: '-sn', expect: [{match: a}]}\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            bm.load_suite(str(bad))

    def test_nonzero_exit_is_error_not_scored(self):
        # `false` exits 1 -> the case must be an error, never a (false) pass.
        bm.tool_adapter.ADAPTERS["_bench_false"] = {
            "binary": "false", "action": "recon", "read_only": True,
            "allowed_flags": set(), "value_flags": set(), "allowed_values": set(),
        }
        suite = Path(self.tmp.name) / "fail.yaml"
        suite.write_text(
            "cases:\n  - {id: f, tool: _bench_false, target: '127.0.0.1', expect: [{match: ''}]}\n"
            .replace("match: ''", "match: x"), encoding="utf-8")
        try:
            report = bm.run_suite(str(suite), str(self.eng))
            self.assertEqual(report["cases"][0]["status"], "error")
        finally:
            bm.tool_adapter.ADAPTERS.pop("_bench_false", None)

    def test_grade_low_nonzero_is_d_not_f(self):
        cards = [{"status": "scored", "score": {"passed": True}}]
        cards += [{"status": "scored", "score": {"passed": False}} for _ in range(199)]
        self.assertEqual(bm.grade_suite(cards)["grade"], "D")  # 0.5% -> D, not F

    def test_cli_failed_case_exits_1(self):
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            bm.main(["run", "--suite", str(self.suite), "--engagement", str(self.eng)])
        self.assertEqual(cm.exception.code, 1)  # marker-missing fails

    def test_cli_writes_output_file(self):
        out = Path(self.tmp.name) / "score.json"
        with self.assertRaises(SystemExit), redirect_stdout(io.StringIO()):
            bm.main(["run", "--suite", str(self.suite), "--engagement", str(self.eng),
                     "--output", str(out)])
        import json
        self.assertTrue(out.is_file())
        data = json.loads(out.read_text())
        self.assertIn("summary", data)

    def test_cli_run_emits_report(self):
        buf = io.StringIO()
        with self.assertRaises(SystemExit), redirect_stdout(buf):
            bm.main(["run", "--suite", str(self.suite), "--engagement", str(self.eng)])
        import json
        data = json.loads(buf.getvalue())
        self.assertIn("summary", data)
        self.assertEqual(data["summary"]["cases_scored"], 2)


if __name__ == "__main__":
    unittest.main()
