#!/usr/bin/env python3
"""Regression tests for SPECTRA Posture Diff."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "posture-diff.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


pd = load_module("posture_diff", SCRIPT)


def _snap(ts, findings):
    return {"ts": ts, "engagement_id": "ENG-T", "findings": findings}


def _f(fid, sev, status="open"):
    return {"id": fid, "title": f"finding {fid}", "severity": sev, "status": status}


class DiffScoringTests(unittest.TestCase):
    def test_resolved_high_is_improved(self):
        before = _snap("t1", [_f("F1", "high")])
        after = _snap("t2", [])
        d = pd.diff_snapshots(before, after)
        self.assertEqual(d["counts"]["resolved"], 1)
        self.assertEqual(d["score"], 4)        # high weight
        self.assertEqual(d["verdict"], "improved")

    def test_added_critical_is_regressed(self):
        d = pd.diff_snapshots(_snap("t1", []), _snap("t2", [_f("F9", "critical")]))
        self.assertEqual(d["counts"]["added"], 1)
        self.assertEqual(d["score"], -5)
        self.assertEqual(d["verdict"], "regressed")

    def test_persisting_finding_no_score(self):
        f = [_f("F1", "medium")]
        d = pd.diff_snapshots(_snap("t1", f), _snap("t2", f))
        self.assertEqual(d["counts"]["persisting"], 1)
        self.assertEqual(d["counts"]["added"], 0)
        self.assertEqual(d["counts"]["resolved"], 0)
        self.assertEqual(d["score"], 0)
        self.assertEqual(d["verdict"], "unchanged")

    def test_escalation_counts_against(self):
        before = _snap("t1", [_f("F1", "low")])
        after = _snap("t2", [_f("F1", "critical")])
        d = pd.diff_snapshots(before, after)
        self.assertEqual(d["counts"]["escalations"], 1)
        self.assertEqual(d["escalations"][0]["from"], "low")
        self.assertEqual(d["escalations"][0]["to"], "critical")
        self.assertEqual(d["score"], -(5 - 2))   # crit - low
        self.assertEqual(d["verdict"], "regressed")

    def test_in_place_resolve_is_improved(self):
        # Finding stays in the snapshot but its status flips to resolved.
        before = _snap("t1", [_f("F1", "high", status="open")])
        after = _snap("t2", [_f("F1", "high", status="resolved")])
        d = pd.diff_snapshots(before, after)
        self.assertEqual(d["counts"]["resolved"], 1)
        self.assertEqual(d["score"], 4)
        self.assertEqual(d["verdict"], "improved")

    def test_de_escalation_is_improved(self):
        before = _snap("t1", [_f("F1", "critical")])
        after = _snap("t2", [_f("F1", "low")])
        d = pd.diff_snapshots(before, after)
        self.assertEqual(d["score"], 5 - 2)   # critical -> low weight reduction
        self.assertEqual(d["verdict"], "improved")

    def test_mixed_net_score(self):
        before = _snap("t1", [_f("F1", "high"), _f("F2", "low")])
        after = _snap("t2", [_f("F2", "low"), _f("F3", "medium")])
        # resolved F1(high=4) +4, added F3(medium=3) -3 => +1 improved
        d = pd.diff_snapshots(before, after)
        self.assertEqual(d["score"], 1)
        self.assertEqual(d["verdict"], "improved")


class SnapshotIOTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.eng = self.dir / "engagement.yaml"
        self.eng.write_text("engagement:\n  id: ENG-T\n  scope:\n    in_scope: {}\n",
                            encoding="utf-8")
        fdir = self.dir / "findings"
        fdir.mkdir()
        (fdir / "F1.yaml").write_text("id: F1\ntitle: SQLi\nseverity: high\nstatus: open\n",
                                      encoding="utf-8")
        (fdir / "F2.yaml").write_text("id: F2\nname: Info leak\nseverity: info\n",
                                      encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_snapshot_normalizes(self):
        snap = pd.build_snapshot(str(self.eng), now="20260610T000000Z")
        self.assertEqual(snap["engagement_id"], "ENG-T")
        ids = {f["id"]: f for f in snap["findings"]}
        self.assertEqual(ids["F1"]["severity"], "high")
        self.assertEqual(ids["F2"]["severity"], "informational")  # info -> informational
        self.assertEqual(ids["F2"]["status"], "open")             # defaulted
        self.assertEqual(snap["runs"]["total"], 0)                # no run log yet

    def test_take_and_list_snapshots(self):
        pd.take_snapshot(str(self.eng), now="20260610T000000Z")
        pd.take_snapshot(str(self.eng), now="20260611T000000Z")
        snaps = pd.list_snapshots(str(self.eng))
        self.assertEqual(len(snaps), 2)
        self.assertTrue(str(snaps[-1]).endswith("20260611T000000Z.json"))

    def test_cli_diff_two_recent(self):
        import io
        from contextlib import redirect_stdout
        # snapshot 1: one finding; snapshot 2: resolved (remove findings dir contents)
        pd.take_snapshot(str(self.eng), now="20260610T000000Z")
        for p in (self.dir / "findings").iterdir():
            p.unlink()
        pd.take_snapshot(str(self.eng), now="20260611T000000Z")
        buf = io.StringIO()
        with self.assertRaises(SystemExit) as cm, redirect_stdout(buf):
            pd.main(["diff", "--engagement", str(self.eng)])
        self.assertEqual(cm.exception.code, 0)
        out = json.loads(buf.getvalue())
        self.assertEqual(out["counts"]["resolved"], 2)
        self.assertEqual(out["verdict"], "improved")

    def test_diff_tolerates_shape_invalid_snapshots(self):
        # list instead of object, and null/garbage finding entries
        self.assertEqual(pd.diff_snapshots([], {"findings": [None, 1, {"id": "F1", "severity": "low"}]})["counts"]["added"], 1)
        self.assertEqual(pd.diff_snapshots({"findings": "nope"}, {})["counts"]["added"], 0)

    def test_cli_diff_malformed_snapshot_exits_3(self):
        import io
        from contextlib import redirect_stdout
        pdir = self.dir / "posture"
        pdir.mkdir()
        (pdir / "20260610T000000Z.json").write_text("[]", encoding="utf-8")
        (pdir / "20260611T000000Z.json").write_text("{\"findings\": [null]}", encoding="utf-8")
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            pd.main(["diff", "--engagement", str(self.eng)])
        # [] top-level is rejected as a non-object snapshot (exit 3), not a crash
        self.assertEqual(cm.exception.code, 3)

    def test_cli_diff_needs_two_snapshots(self):
        import io
        from contextlib import redirect_stdout
        pd.take_snapshot(str(self.eng), now="20260610T000000Z")
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            pd.main(["diff", "--engagement", str(self.eng)])
        self.assertEqual(cm.exception.code, 3)


if __name__ == "__main__":
    unittest.main()
