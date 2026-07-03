#!/usr/bin/env python3
"""Regression tests for SPECTRA engagement state gates."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "engagement-state.py"
SPEC = importlib.util.spec_from_file_location("engagement_state", SCRIPT)
engagement_state = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(engagement_state)


class EngagementStateTests(unittest.TestCase):
    def setUp(self):
        today = date.today()
        self.doc = {
            "engagement": {
                "id": "ENG-TEST-002",
                "name": "State machine test",
                "type": "red-team",
                "status": "active",
                "authorization": {
                    "client": "Example Corp",
                    "authorized_by": "CISO",
                    "authorization_document": "sow.pdf",
                    "start_date": (today - timedelta(days=1)).isoformat(),
                    "end_date": (today + timedelta(days=7)).isoformat(),
                    "timezone": "UTC",
                },
                "rules_of_engagement": {
                    "testing_hours": "any",
                    "custom_hours": "",
                    "notify_before_exploit": False,
                    "notify_on_critical": True,
                    "social_engineering_allowed": False,
                    "physical_access_allowed": False,
                    "dos_testing_allowed": False,
                    "data_exfiltration_allowed": False,
                    "production_systems": False,
                    "max_impact_level": "high",
                },
                "scope": {
                    "in_scope": {
                        "networks": ["10.20.30.0/24"],
                        "domains": ["example.com"],
                        "applications": [],
                        "cloud_accounts": [],
                        "users": [],
                        "notes": "",
                    },
                    "out_of_scope": {
                        "networks": ["10.20.30.200/32"],
                        "domains": ["blocked.example.com"],
                        "applications": [],
                        "critical_systems": [],
                        "users": [],
                        "notes": "",
                    },
                },
            },
            "workflow_state": {},
            "kill_chain": {},
        }

    def test_valid_engagement_passes_recon_gate(self):
        result = engagement_state.gate_document(
            self.doc,
            "spectra-external-recon",
            "example.com",
            None,
        )
        self.assertTrue(result["allowed"], result["errors"])

    # -- issue #2: 'completed' vs 'complete' tolerance ---------------------

    def test_canonical_status_maps_natural_spellings(self):
        self.assertEqual(engagement_state.canonical_status("completed"), "complete")
        self.assertEqual(engagement_state.canonical_status("in progress"), "in-progress")
        self.assertEqual(engagement_state.canonical_status("in_progress"), "in-progress")
        self.assertEqual(engagement_state.canonical_status("COMPLETE"), "complete")
        self.assertEqual(engagement_state.canonical_status("active"), "active")

    def test_workflow_status_completed_validates(self):
        # An agent that wrote "completed" (not the canonical "complete") must not
        # break validation — no manual edit required.
        self.doc["workflow_state"] = {"external_recon": {"status": "completed"}}
        result = engagement_state.validate_document(self.doc)
        self.assertTrue(result["valid"], result["errors"])

    def test_engagement_status_completed_validates(self):
        self.doc["engagement"]["status"] = "completed"
        result = engagement_state.validate_document(self.doc)
        self.assertTrue(result["valid"], result["errors"])

    def test_transition_accepts_and_canonicalizes_completed(self):
        # Move to in-progress first, then transition target "completed" must be
        # accepted and written as the canonical "complete".
        self.doc["workflow_state"] = {"external_recon": {"status": "in-progress"}}
        args = SimpleNamespace(force=False, agent=None, findings_count=None, artifact=[])
        result = engagement_state.transition_document(
            self.doc, "spectra-external-recon", "completed", args)
        self.assertTrue(result["transitioned"], result.get("errors"))
        self.assertEqual(
            self.doc["workflow_state"]["external_recon"]["status"], "complete")

    def test_transition_from_completed_state_maps_correctly(self):
        # Prior state persisted as "completed" must canonicalize to "complete"
        # for the transition lookup rather than dead-ending on an unknown status.
        self.doc["workflow_state"] = {"external_recon": {"status": "completed"}}
        args = SimpleNamespace(force=False, agent=None, findings_count=None, artifact=[])
        result = engagement_state.transition_document(
            self.doc, "spectra-external-recon", "in-progress", args)
        self.assertEqual(result["from"], "complete")

    def test_gate_blocks_out_of_scope_target(self):
        result = engagement_state.gate_document(
            self.doc,
            "spectra-external-recon",
            "blocked.example.com",
            None,
        )
        self.assertFalse(result["allowed"])
        self.assertIn("target gate failed: OUT_OF_SCOPE", result["errors"][0])

    def test_gate_blocks_exfil_without_explicit_roe(self):
        result = engagement_state.gate_document(
            self.doc,
            "spectra-exfiltration",
            "example.com",
            None,
        )
        self.assertFalse(result["allowed"])
        self.assertTrue(any("data_exfiltration_allowed" in err for err in result["errors"]))

    def test_gate_blocks_exfil_without_data_handling(self):
        self.doc["engagement"]["rules_of_engagement"]["data_exfiltration_allowed"] = True
        result = engagement_state.gate_document(
            self.doc,
            "spectra-exfiltration",
            "example.com",
            None,
        )
        self.assertFalse(result["allowed"])
        self.assertTrue(any("data_handling" in err for err in result["errors"]))

    def test_transition_updates_workflow_state_and_kill_chain(self):
        args = SimpleNamespace(
            force=False,
            agent="Viper",
            findings_count=3,
            artifact=["recon-report.md"],
        )
        result = engagement_state.transition_document(
            self.doc,
            "spectra-external-recon",
            "in-progress",
            args,
        )
        self.assertTrue(result["transitioned"], result["errors"])
        self.assertEqual(self.doc["workflow_state"]["external_recon"]["status"], "in-progress")
        self.assertEqual(self.doc["kill_chain"]["reconnaissance"]["status"], "in-progress")
        self.assertEqual(self.doc["kill_chain"]["reconnaissance"]["agent"], "Viper")

    def test_invalid_transition_is_rejected(self):
        args = SimpleNamespace(force=False, agent=None, findings_count=None, artifact=[])
        result = engagement_state.transition_document(
            self.doc,
            "spectra-external-recon",
            "complete",
            args,
        )
        self.assertFalse(result["transitioned"])
        self.assertIn("invalid transition", result["errors"][0])

    def test_cli_transition_writes_yaml(self):
        with tempfile.TemporaryDirectory() as tmp:
            engagement_path = Path(tmp) / "engagement.yaml"
            engagement_path.write_text(yaml.safe_dump(self.doc, sort_keys=False), encoding="utf-8")
            loaded, path = engagement_state.load_document(str(engagement_path))
            args = SimpleNamespace(
                force=False,
                agent=None,
                findings_count=None,
                artifact=[],
            )
            result = engagement_state.transition_document(
                loaded,
                "spectra-external-recon",
                "in-progress",
                args,
            )
            self.assertTrue(result["transitioned"])
            engagement_state.save_document(path, loaded)
            reloaded = yaml.safe_load(engagement_path.read_text(encoding="utf-8"))
            self.assertEqual(reloaded["workflow_state"]["external_recon"]["status"], "in-progress")


if __name__ == "__main__":
    unittest.main()
