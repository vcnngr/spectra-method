#!/usr/bin/env python3
"""Regression tests for SPECTRA scope-enforcer guardrails."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scope-enforcer.py"
SPEC = importlib.util.spec_from_file_location("scope_enforcer", SCRIPT)
scope_enforcer = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(scope_enforcer)


class ScopeEnforcerTests(unittest.TestCase):
    def setUp(self):
        self.engagement = {
            "id": "ENG-TEST-001",
            "type": "red-team",
            "status": "active",
            "authorization": {"timezone": "UTC"},
            "rules_of_engagement": {
                "testing_hours": "any",
                "social_engineering_allowed": False,
                "physical_access_allowed": False,
                "dos_testing_allowed": "none",
                "data_exfiltration_allowed": False,
                "production_systems": False,
                "max_impact_level": "high",
            },
            "scope": {
                "in_scope": {
                    "networks": ["10.10.10.0/24"],
                    "domains": ["example.com"],
                    "applications": [],
                    "cloud_accounts": [],
                    "users": [],
                    "notes": "",
                },
                "out_of_scope": {
                    "networks": ["10.10.10.200/32"],
                    "domains": ["blocked.example.com"],
                    "applications": [],
                    "critical_systems": [],
                    "users": [],
                    "notes": "",
                },
            },
        }

    def test_allows_in_scope_recon(self):
        result = scope_enforcer.run_check("example.com", self.engagement, "recon")
        self.assertEqual(result["verdict"], "IN_SCOPE")
        self.assertTrue(result["action_allowed"])

    def test_out_of_scope_precedence(self):
        result = scope_enforcer.run_check("blocked.example.com", self.engagement, "recon")
        self.assertEqual(result["verdict"], "OUT_OF_SCOPE")
        self.assertFalse(result["action_allowed"])

    def test_textual_none_denies_dos(self):
        result = scope_enforcer.run_check("example.com", self.engagement, "dos")
        self.assertEqual(result["verdict"], "AMBIGUOUS")
        self.assertFalse(result["action_allowed"])
        self.assertIn("dos_testing_allowed is false", result["restrictions"][0])

    def test_destructive_actions_are_hard_blocked(self):
        result = scope_enforcer.run_check(
            "example.com",
            self.engagement,
            "deploy ransomware payload",
        )
        self.assertEqual(result["verdict"], "AMBIGUOUS")
        self.assertFalse(result["action_allowed"])
        self.assertIn("destructive action hard-blocked", result["restrictions"][0])

    def test_summary_normalizes_textual_roe_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            engagement_path = Path(tmp) / "engagement.yaml"
            engagement_path.write_text(
                yaml.safe_dump({"engagement": self.engagement}, sort_keys=False),
                encoding="utf-8",
            )
            loaded = scope_enforcer.load_engagement(str(engagement_path))
            self.assertEqual(loaded["id"], "ENG-TEST-001")
            self.assertFalse(scope_enforcer._roe_allows(loaded["rules_of_engagement"]["dos_testing_allowed"]))
            self.assertTrue(scope_enforcer._roe_allows("light"))


if __name__ == "__main__":
    unittest.main()
