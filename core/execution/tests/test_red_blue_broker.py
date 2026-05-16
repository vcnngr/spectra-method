#!/usr/bin/env python3
"""Regression tests for Red/Blue ledger broker."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


BROKER_SCRIPT = Path(__file__).resolve().parents[1] / "red-blue-broker.py"
DUEL_SCRIPT = Path(__file__).resolve().parents[1] / "duel-orchestrator.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


broker = load_module("red_blue_broker", BROKER_SCRIPT)
duel = load_module("duel_for_broker_tests", DUEL_SCRIPT)


class RedBlueBrokerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.red_root = self.root / "red" / "_spectra-output" / "duel"
        self.referee_root = self.root / "referee" / "_spectra-output" / "duel"
        self.session = "ENG-BROKER-001"

    def tearDown(self):
        self.tmp.cleanup()

    def test_export_import_and_deduplicate_role_ledger(self):
        duel.init_session(self.session, "red", self.red_root, "engagement.yaml")
        duel.record_event(
            self.red_root,
            self.session,
            "red",
            "action",
            "Credential pressure within authorized noise budget.",
            target="app.example.test",
            technique="T1110.001",
        )
        bundle = self.root / "exchange" / "red-bundle.json"

        exported = broker.export_bundle(self.red_root, self.session, "red", bundle)
        self.assertEqual(exported["event_count"], 1)
        self.assertTrue(bundle.is_file())

        imported = broker.import_bundle(self.referee_root, self.session, "red", bundle)
        self.assertEqual(imported["imported"], 1)
        self.assertEqual(imported["skipped_duplicates"], 0)

        duplicate = broker.import_bundle(self.referee_root, self.session, "red", bundle)
        self.assertEqual(duplicate["imported"], 0)
        self.assertEqual(duplicate["skipped_duplicates"], 1)

        events = broker.load_events(broker.ledger_path(self.referee_root, self.session, "red"))
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["id"], "RED-0001")

    def test_import_rejects_tampered_bundle(self):
        duel.init_session(self.session, "blue", self.red_root, "engagement.yaml")
        duel.record_event(
            self.red_root,
            self.session,
            "blue",
            "detection",
            "Detected authentication failures.",
            target="app.example.test",
            technique="T1110.001",
        )
        bundle = self.root / "blue-bundle.json"
        broker.export_bundle(self.red_root, self.session, "blue", bundle)

        data = json.loads(bundle.read_text(encoding="utf-8"))
        data["events"][0]["summary"] = "Tampered summary."
        bundle.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(ValueError):
            broker.import_bundle(self.referee_root, self.session, "blue", bundle)

    def test_import_rejects_event_count_mismatch(self):
        duel.init_session(self.session, "blue", self.red_root, "engagement.yaml")
        duel.record_event(
            self.red_root,
            self.session,
            "blue",
            "detection",
            "Detected authentication failures.",
            target="app.example.test",
            technique="T1110.001",
        )
        bundle = self.root / "blue-count-bundle.json"
        broker.export_bundle(self.red_root, self.session, "blue", bundle)

        data = json.loads(bundle.read_text(encoding="utf-8"))
        data["event_count"] = 99
        bundle.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(ValueError):
            broker.import_bundle(self.referee_root, self.session, "blue", bundle)

    def test_import_strips_unknown_event_keys_and_uses_hash_marker(self):
        duel.init_session(self.session, "blue", self.red_root, "engagement.yaml")
        duel.record_event(
            self.red_root,
            self.session,
            "blue",
            "detection",
            "Detected authentication failures.",
            target="app.example.test",
            technique="T1110.001",
        )
        bundle = self.root / "blue-extra-bundle.json"
        broker.export_bundle(self.red_root, self.session, "blue", bundle)

        data = json.loads(bundle.read_text(encoding="utf-8"))
        data["events"][0]["html_payload"] = "<script>alert(1)</script>"
        data["events_sha256"] = broker.events_hash(data["events"])
        bundle.write_text(json.dumps(data), encoding="utf-8")

        imported = broker.import_bundle(self.referee_root, self.session, "blue", bundle)
        self.assertEqual(imported["imported"], 1)
        events = broker.load_events(broker.ledger_path(self.referee_root, self.session, "blue"))
        self.assertNotIn("html_payload", events[0])
        markers = list((self.referee_root / self.session / "imports").glob("blue-*-blue-extra-bundle.json"))
        self.assertEqual(len(markers), 1)

    def test_import_rejects_role_mismatch(self):
        duel.init_session(self.session, "red", self.red_root, "engagement.yaml")
        duel.record_event(
            self.red_root,
            self.session,
            "red",
            "action",
            "Authorized scan planning.",
            target="app.example.test",
            technique="T1046",
        )
        bundle = self.root / "red-bundle.json"
        broker.export_bundle(self.red_root, self.session, "red", bundle)

        with self.assertRaises(ValueError):
            broker.import_bundle(self.referee_root, self.session, "blue", bundle)


if __name__ == "__main__":
    unittest.main()
