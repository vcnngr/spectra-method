#!/usr/bin/env python3
"""Regression tests for report adapters and generator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

import yaml


ADAPTERS_SCRIPT = Path(__file__).resolve().parents[1] / "report-adapters.py"
GENERATOR_SCRIPT = Path(__file__).resolve().parents[1] / "report-generator.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


report_adapters = load_module("report_adapters", ADAPTERS_SCRIPT)
report_generator = load_module("report_generator", GENERATOR_SCRIPT)


class ReportPipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.eng_dir = self.root / "_spectra-output" / "engagements" / "ENG-REPORT-001"
        self.eng_dir.mkdir(parents=True)
        today = date.today()
        self.engagement_path = self.eng_dir / "engagement.yaml"
        self.engagement_path.write_text(yaml.safe_dump({
            "engagement": {
                "id": "ENG-REPORT-001",
                "name": "Report test",
                "type": "pentest",
                "status": "complete",
                "authorization": {
                    "client": "Example Corp",
                    "authorized_by": "CISO",
                    "authorization_document": "sow.pdf",
                    "start_date": (today - timedelta(days=5)).isoformat(),
                    "end_date": today.isoformat(),
                    "timezone": "UTC",
                },
                "rules_of_engagement": {
                    "testing_hours": "any",
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
                        "networks": ["10.0.0.0/24"],
                        "domains": ["example.com"],
                        "applications": [],
                        "cloud_accounts": [],
                        "users": [],
                        "notes": "",
                    },
                    "out_of_scope": {
                        "networks": [],
                        "domains": ["blocked.example.com"],
                        "applications": [],
                        "critical_systems": [],
                        "users": [],
                        "notes": "",
                    },
                },
            },
            "workflow_state": {
                "external_recon": {
                    "status": "complete",
                    "agent": "Ghost",
                    "started": "2026-05-16T10:00:00",
                    "completed": "2026-05-16T11:00:00",
                    "artifacts": ["recon-report.md"],
                }
            },
            "kill_chain": {},
        }, sort_keys=False), encoding="utf-8")

        findings_dir = self.eng_dir / "findings"
        findings_dir.mkdir()
        (findings_dir / "FIND-001.yaml").write_text(yaml.safe_dump({
            "id": "FIND-001",
            "title": "Exposed admin panel",
            "severity": "high",
            "cvss": 8.1,
            "status": "confirmed",
        }, sort_keys=False), encoding="utf-8")

        evidence_dir = self.root / "_spectra-output" / "evidence" / "ENG-REPORT-001"
        evidence_dir.mkdir(parents=True)
        (evidence_dir / "evidence-registry.yaml").write_text(yaml.safe_dump({
            "evidence_registry": {
                "engagement_id": "ENG-REPORT-001",
                "item_count": 1,
                "integrity_status": "VERIFIED",
                "last_verified": "2026-05-16T11:00:00Z",
                "items": [{
                    "id": "EV-ENG-REPORT-001-001",
                    "description": "Screenshot",
                    "source_type": "screenshot",
                    "status": "active",
                    "hash_sha256": "a" * 64,
                }],
            }
        }, sort_keys=False), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_adapters_build_bundle(self):
        bundle = report_adapters.build_report_bundle(str(self.engagement_path))
        self.assertEqual(bundle["engagement"]["id"], "ENG-REPORT-001")
        self.assertEqual(bundle["scope"]["counts"]["in_scope"], 2)
        self.assertEqual(bundle["findings"]["total"], 1)
        self.assertEqual(bundle["evidence"]["item_count"], 1)
        self.assertGreater(bundle["tools"]["tool_count"], 0)

    def test_generator_writes_structured_report(self):
        bundle = report_adapters.build_report_bundle(str(self.engagement_path))
        content = report_generator.render_markdown(bundle, "pentest")
        self.assertIn("# Pentest Report - ENG-REPORT-001", content)
        self.assertIn("Exposed admin panel", content)
        self.assertIn("Evidence Index", content)


if __name__ == "__main__":
    unittest.main()
