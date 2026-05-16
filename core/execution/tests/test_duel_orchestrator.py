#!/usr/bin/env python3
"""Regression tests for Duel Mode runtime."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "duel-orchestrator.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


duel_orchestrator = load_module("duel_orchestrator", SCRIPT)


class DuelOrchestratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.output_root = self.root / "_spectra-output" / "duel"
        self.session = "ENG-DUEL-001"

    def tearDown(self):
        self.tmp.cleanup()

    def test_init_record_and_score(self):
        duel_orchestrator.init_session(self.session, "red", self.output_root, "engagement.yaml")
        duel_orchestrator.init_session(self.session, "blue", self.output_root, "engagement.yaml")
        red = duel_orchestrator.record_event(
            self.output_root,
            self.session,
            "red",
            "action",
            "Low-and-slow authentication pressure within credential attempt budget.",
            target="antilia.blackhole.global:8081",
            technique="T1110.001",
        )["event"]
        duel_orchestrator.record_event(
            self.output_root,
            self.session,
            "blue",
            "detection",
            "Detected repeated phpMyAdmin login failures from same source over extended window.",
            target="antilia.blackhole.global:8081",
            technique="T1110.001",
            red_event_id=red["id"],
        )
        score = duel_orchestrator.score_duel(
            duel_orchestrator.load_events(duel_orchestrator.ledger_path(self.output_root, self.session, "red")),
            duel_orchestrator.load_events(duel_orchestrator.ledger_path(self.output_root, self.session, "blue")),
        )
        self.assertEqual(score["summary"]["red_actions"], 1)
        self.assertEqual(score["summary"]["blue_detections_or_mitigations"], 1)
        self.assertEqual(score["summary"]["detection_rate_percent"], 100.0)

    def test_red_event_blocks_log_tampering_language(self):
        duel_orchestrator.init_session(self.session, "red", self.output_root, "engagement.yaml")
        with self.assertRaises(ValueError):
            duel_orchestrator.record_event(
                self.output_root,
                self.session,
                "red",
                "action",
                "Delete logs after authentication testing.",
                target="host",
                technique="cleanup",
            )

    def test_status_counts_role_events(self):
        duel_orchestrator.init_session(self.session, "referee", self.output_root, "engagement.yaml")
        duel_orchestrator.record_event(
            self.output_root,
            self.session,
            "referee",
            "checkpoint",
            "Exercise start checkpoint.",
        )
        status = duel_orchestrator.build_status(self.output_root, self.session)
        self.assertTrue(status["roles"]["referee"]["initialized"])
        self.assertEqual(status["roles"]["referee"]["events"], 1)

    def test_score_tracks_detection_latency_and_severity_coverage(self):
        red_events = [
            {
                "id": "RED-0001",
                "event_type": "action",
                "summary": "Credential pressure within attempt budget.",
                "timestamp": "2026-05-16T10:00:00+00:00",
                "target": "app.example.test",
                "technique": "T1110.001",
                "severity": "high",
            },
            {
                "id": "RED-0002",
                "event_type": "action",
                "summary": "Web enumeration within rate budget.",
                "timestamp": "2026-05-16T10:05:00+00:00",
                "target": "app.example.test",
                "technique": "T1595.003",
                "severity": "medium",
            },
        ]
        blue_events = [
            {
                "id": "BLUE-0001",
                "event_type": "detection",
                "summary": "Detected auth failures.",
                "timestamp": "2026-05-16T10:02:00+00:00",
                "target": "app.example.test",
                "technique": "T1110.001",
                "red_event_id": "RED-0001",
            },
            {
                "id": "BLUE-0002",
                "event_type": "mitigation",
                "summary": "Rate limited enumeration source.",
                "timestamp": "2026-05-16T10:08:00+00:00",
                "target": "app.example.test",
                "technique": "T1595.003",
                "red_event_id": "RED-0002",
            },
        ]

        score = duel_orchestrator.score_duel(red_events, blue_events)

        self.assertEqual(score["summary"]["first_detection_latency_seconds"], 120)
        self.assertEqual(score["summary"]["average_detection_latency_seconds"], 150.0)
        self.assertEqual(score["severity_coverage"]["high"]["coverage_percent"], 100.0)
        self.assertEqual(score["severity_coverage"]["medium"]["coverage_percent"], 100.0)
        self.assertEqual(score["summary"]["outcome_grade"], "A")

    def test_score_groups_missed_actions_by_technique(self):
        red_events = [
            {
                "id": "RED-0001",
                "event_type": "action",
                "summary": "Credential pressure within attempt budget.",
                "timestamp": "2026-05-16T10:00:00+00:00",
                "target": "app.example.test",
                "technique": "T1110.001",
                "severity": "high",
            },
            {
                "id": "RED-0002",
                "event_type": "action",
                "summary": "Second credential pressure window.",
                "timestamp": "2026-05-16T10:10:00+00:00",
                "target": "app.example.test",
                "technique": "T1110.001",
                "severity": "high",
            },
            {
                "id": "RED-0003",
                "event_type": "action",
                "summary": "Web enumeration within rate budget.",
                "timestamp": "2026-05-16T10:20:00+00:00",
                "target": "app.example.test",
                "technique": "T1595.003",
                "severity": "medium",
            },
        ]
        blue_events = [
            {
                "id": "BLUE-0001",
                "event_type": "detection",
                "summary": "Detected enumeration.",
                "timestamp": "2026-05-16T10:25:00+00:00",
                "target": "app.example.test",
                "technique": "T1595.003",
                "red_event_id": "RED-0003",
            },
        ]

        score = duel_orchestrator.score_duel(red_events, blue_events)

        self.assertEqual(score["missed_by_technique"], {"T1110.001": 2})
        self.assertEqual(score["severity_coverage"]["high"]["detected"], 0)
        self.assertEqual(score["severity_coverage"]["high"]["total"], 2)
        self.assertEqual(score["summary"]["outcome_grade"], "D")


if __name__ == "__main__":
    unittest.main()
