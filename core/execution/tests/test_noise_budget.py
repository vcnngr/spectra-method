#!/usr/bin/env python3
"""Regression tests for the SPECTRA Noise-Budget Validator."""

from __future__ import annotations

import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "noise-budget.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


nb = load_module("noise_budget", SCRIPT)


def roe(**budget):
    return {"noise_budget": budget} if budget else {}


class NoiseBudgetTests(unittest.TestCase):
    def codes(self, result):
        return {i["code"] for i in result["issues"]}

    # -- presence ----------------------------------------------------------

    def test_absent_budget_is_pass(self):
        result = nb.validate_noise_budget({})
        self.assertEqual(result["status"], "PASS")
        self.assertFalse(result["budget_present"])
        self.assertEqual(result["issues"], [])

    def test_non_dict_budget_fails(self):
        result = nb.validate_noise_budget({"noise_budget": "not-a-dict"})
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("budget_type", self.codes(result))

    def test_well_formed_balanced_budget_passes(self):
        result = nb.validate_noise_budget(roe(
            profile="balanced", max_actions_per_hour=20,
            min_action_interval_seconds=60, max_concurrent_actions=2,
            telemetry_tolerance="medium", abort_on_detection=False,
        ))
        self.assertEqual(result["status"], "PASS", result["issues"])
        self.assertTrue(result["budget_present"])

    # -- type / range validation -------------------------------------------

    def test_invalid_profile_fails(self):
        result = nb.validate_noise_budget(roe(profile="ninja"))
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("profile_invalid", self.codes(result))

    def test_invalid_tolerance_fails(self):
        result = nb.validate_noise_budget(roe(telemetry_tolerance="silent"))
        self.assertIn("tolerance_invalid", self.codes(result))

    def test_negative_rate_fails(self):
        result = nb.validate_noise_budget(roe(max_actions_per_hour=-5))
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("max_actions_per_hour_negative", self.codes(result))

    def test_zero_concurrent_fails(self):
        result = nb.validate_noise_budget(roe(max_concurrent_actions=0))
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("max_concurrent_invalid", self.codes(result))

    def test_bool_for_int_field_fails(self):
        # True must not be silently accepted as an integer rate.
        result = nb.validate_noise_budget(roe(max_actions_per_hour=True))
        self.assertIn("max_actions_per_hour_type", self.codes(result))

    def test_non_bool_abort_fails(self):
        result = nb.validate_noise_budget(roe(abort_on_detection="yes"))
        self.assertIn("abort_type", self.codes(result))

    # -- coherence ---------------------------------------------------------

    def test_rate_exceeds_interval_warns(self):
        # 30s spacing permits ~120/h; 600/h exceeds it.
        result = nb.validate_noise_budget(roe(
            max_actions_per_hour=600, min_action_interval_seconds=30))
        self.assertEqual(result["status"], "WARN")
        self.assertIn("rate_exceeds_interval", self.codes(result))

    def test_low_footprint_high_rate_warns(self):
        result = nb.validate_noise_budget(roe(profile="low_footprint", max_actions_per_hour=500))
        self.assertEqual(result["status"], "WARN")
        self.assertIn("low_footprint_high_rate", self.codes(result))

    def test_low_footprint_high_tolerance_warns(self):
        result = nb.validate_noise_budget(roe(profile="low_footprint", telemetry_tolerance="high"))
        self.assertIn("low_footprint_high_tolerance", self.codes(result))

    def test_low_footprint_concurrency_warns(self):
        result = nb.validate_noise_budget(roe(profile="low_footprint", max_concurrent_actions=4))
        self.assertIn("low_footprint_concurrency", self.codes(result))

    def test_low_footprint_no_abort_is_info_only(self):
        result = nb.validate_noise_budget(roe(profile="low_footprint", abort_on_detection=False))
        self.assertEqual(result["status"], "PASS")  # INFO does not downgrade
        self.assertIn("low_footprint_no_abort", self.codes(result))

    def test_low_footprint_abort_omitted_is_info(self):
        # Nudge fires when abort_on_detection is unset (not just when False).
        result = nb.validate_noise_budget(roe(profile="low_footprint"))
        self.assertEqual(result["status"], "PASS")
        self.assertIn("low_footprint_no_abort", self.codes(result))

    def test_low_footprint_abort_true_no_nudge(self):
        result = nb.validate_noise_budget(roe(profile="low_footprint", abort_on_detection=True))
        self.assertNotIn("low_footprint_no_abort", self.codes(result))

    def test_high_footprint_low_tolerance_warns(self):
        result = nb.validate_noise_budget(roe(profile="high_footprint", telemetry_tolerance="low"))
        self.assertEqual(result["status"], "WARN")
        self.assertIn("high_footprint_low_tolerance", self.codes(result))

    def test_fail_dominates_warn(self):
        result = nb.validate_noise_budget(roe(
            profile="low_footprint", max_actions_per_hour=500, max_concurrent_actions=0))
        self.assertEqual(result["status"], "FAIL")

    # -- loading -----------------------------------------------------------

    def test_load_missing_engagement_raises(self):
        with self.assertRaises(FileNotFoundError):
            nb.load_engagement("/nonexistent/engagement.yaml")

    def test_load_invalid_engagement_raises(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "e.yaml"
            p.write_text("not_engagement: true\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                nb.load_engagement(str(p))

    # -- null / type edge cases -------------------------------------------

    def test_present_null_field_fails(self):
        # A key present with explicit null is malformed (schema rejects null).
        result = nb.validate_noise_budget(roe(profile=None))
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("profile_null", self.codes(result))

    def test_float_for_int_field_fails(self):
        result = nb.validate_noise_budget(roe(max_actions_per_hour=10.5))
        self.assertIn("max_actions_per_hour_type", self.codes(result))

    def test_negative_interval_fails(self):
        result = nb.validate_noise_budget(roe(min_action_interval_seconds=-1))
        self.assertEqual(result["status"], "FAIL")
        self.assertIn("min_action_interval_seconds_negative", self.codes(result))

    def test_bool_concurrent_fails(self):
        result = nb.validate_noise_budget(roe(max_concurrent_actions=True))
        self.assertIn("max_concurrent_type", self.codes(result))

    def test_non_string_notes_fails(self):
        result = nb.validate_noise_budget(roe(notes=123))
        self.assertIn("notes_type", self.codes(result))

    # -- CLI exit codes ----------------------------------------------------

    def _write_engagement(self, tmp, **budget):
        p = Path(tmp) / "e.yaml"
        import yaml
        doc = {"engagement": {"id": "E1", "rules_of_engagement": {"noise_budget": budget}}}
        p.write_text(yaml.safe_dump(doc), encoding="utf-8")
        return str(p)

    def test_cli_fail_exits_1(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = self._write_engagement(d, max_concurrent_actions=0)
            with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
                nb.main(["check", "--engagement", path])
            self.assertEqual(cm.exception.code, 1)

    def test_cli_warn_exits_0_by_default(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = self._write_engagement(d, profile="low_footprint", max_actions_per_hour=500)
            with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
                nb.main(["check", "--engagement", path])
            self.assertEqual(cm.exception.code, 0)

    def test_cli_warn_exits_1_with_fail_on_warn(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            path = self._write_engagement(d, profile="low_footprint", max_actions_per_hour=500)
            with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
                nb.main(["check", "--engagement", path, "--fail-on-warn"])
            self.assertEqual(cm.exception.code, 1)

    # -- gate integration --------------------------------------------------

    def test_gate_blocks_on_fail_budget(self):
        # The engagement-state gate must block a workflow when the noise budget
        # is invalid (FAIL), and allow it when the budget is merely WARN/absent.
        es = load_module("engagement_state",
                         Path(__file__).resolve().parents[1] / "engagement-state.py")
        base = {
            "engagement": {
                "id": "E1", "name": "n", "type": "red-team", "status": "active",
                "rules_of_engagement": {},
            }
        }
        # FAIL budget -> gate blocks.
        bad = {"engagement": dict(base["engagement"],
                                  rules_of_engagement={"noise_budget": {"max_concurrent_actions": 0}})}
        result = es.gate_document(bad, "spectra-external-recon", None, None)
        self.assertFalse(result["allowed"])
        self.assertTrue(any("noise_budget" in e for e in result["errors"]))


if __name__ == "__main__":
    unittest.main()
