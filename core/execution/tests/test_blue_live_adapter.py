#!/usr/bin/env python3
"""Regression tests for Blue Live Adapter."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "blue-live-adapter.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


blue_live_adapter = load_module("blue_live_adapter", SCRIPT)


class BlueLiveAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_log(self, name: str, content: str) -> Path:
        path = self.root / name
        path.write_text(content, encoding="utf-8")
        return path

    def append_log(self, path: Path, content: str):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(content)

    def test_auth_parser_detects_ssh_password_pressure(self):
        log = self.write_log(
            "auth.log",
            "May 16 10:00:00 host sshd[100]: Failed password for invalid user admin from 203.0.113.10 port 53222 ssh2\n",
        )
        detections = blue_live_adapter.ingest_sources([f"auth={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1110.001")
        self.assertEqual(detections[0].event_type, "detection")

    def test_nginx_parser_detects_sensitive_path_probe(self):
        log = self.write_log(
            "access.log",
            '203.0.113.10 - - [16/May/2026:10:00:00 +0000] "GET /.env HTTP/1.1" 403 153 "-" "curl/8"\n',
        )
        detections = blue_live_adapter.ingest_sources([f"nginx_access={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1595.003")

    def test_fail2ban_parser_records_mitigation(self):
        log = self.write_log(
            "fail2ban.log",
            "2026-05-16 10:00:00,000 fail2ban.actions [1]: NOTICE  [sshd] Ban 203.0.113.10\n",
        )
        detections = blue_live_adapter.ingest_sources([f"fail2ban={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].event_type, "mitigation")

    def test_suricata_eve_parser_maps_scan_alert(self):
        log = self.write_log(
            "eve.json",
            json.dumps({
                "event_type": "alert",
                "src_ip": "203.0.113.10",
                "dest_ip": "198.51.100.20",
                "proto": "TCP",
                "alert": {
                    "signature": "ET SCAN Nmap Scripting Engine User-Agent Detected",
                    "category": "Attempted Information Leak",
                    "severity": 2,
                },
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"suricata_eve={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1046")
        self.assertEqual(detections[0].severity, "medium")
        self.assertIn("Suricata alert", detections[0].summary)

    def test_suricata_eve_parser_defaults_network_alert_to_c2_channel(self):
        log = self.write_log(
            "eve-c2.json",
            json.dumps({
                "event_type": "alert",
                "src_ip": "203.0.113.10",
                "dest_ip": "198.51.100.20",
                "proto": "TCP",
                "alert": {
                    "signature": "ET POLICY Suspicious outbound connection",
                    "category": "Potential Corporate Privacy Violation",
                    "severity": 1,
                },
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"suricata={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1071")
        self.assertEqual(detections[0].severity, "high")

    def test_wazuh_parser_maps_brute_force_alert(self):
        log = self.write_log(
            "alerts.json",
            json.dumps({
                "rule": {
                    "description": "sshd: brute force trying to get access to the system",
                    "level": 10,
                },
                "agent": {"name": "web-01"},
                "data": {"srcip": "203.0.113.10"},
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"wazuh={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1110.001")
        self.assertEqual(detections[0].target, "web-01")

    def test_wazuh_parser_maps_malware_alert(self):
        log = self.write_log(
            "malware-alerts.json",
            json.dumps({
                "rule": {
                    "description": "Malware detected during endpoint scan",
                    "level": 13,
                },
                "agent": {"name": "workstation-07"},
                "srcip": "203.0.113.11",
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"wazuh={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1204")
        self.assertEqual(detections[0].severity, "high")

    def test_wazuh_parser_maps_network_scan_alert(self):
        log = self.write_log(
            "scan-alerts.json",
            json.dumps({
                "rule": {
                    "description": "Network scan from external source",
                    "level": 8,
                },
                "agent": {"name": "ids-01"},
                "data": {"src_ip": "203.0.113.12"},
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"wazuh={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1046")
        self.assertEqual(detections[0].severity, "medium")

    def test_zeek_dns_parser_maps_query(self):
        log = self.write_log(
            "dns.log",
            json.dumps({
                "id.orig_h": "10.0.0.15",
                "query": "beacon.example.test",
                "qtype_name": "A",
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"zeek_dns={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1071.004")
        self.assertEqual(detections[0].target, "beacon.example.test")

    def test_zeek_http_parser_maps_suspicious_request(self):
        log = self.write_log(
            "http.log",
            json.dumps({
                "id.orig_h": "10.0.0.15",
                "host": "app.example.test",
                "method": "GET",
                "uri": "/.env",
                "status_code": 403,
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"zeek_http={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1071.001")
        self.assertIn("/.env", detections[0].summary)

    def test_zeek_conn_parser_maps_scan_like_connection(self):
        log = self.write_log(
            "conn.log",
            json.dumps({
                "id.orig_h": "10.0.0.15",
                "id.resp_h": "198.51.100.20",
                "id.resp_p": 22,
                "proto": "tcp",
                "conn_state": "S0",
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"zeek_conn={log}"])
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0].technique, "T1046")
        self.assertEqual(detections[0].target, "198.51.100.20:22")

    def test_write_duel_events_appends_blue_ledger(self):
        log = self.write_log(
            "mail.log",
            "May 16 10:00:00 host postfix/smtpd[100]: warning: unknown[203.0.113.10]: SASL LOGIN authentication failed\n",
        )
        output_root = self.root / "_spectra-output" / "duel"
        detections = blue_live_adapter.ingest_sources([f"postfix={log}"])
        events = blue_live_adapter.write_duel_events(output_root, "ENG-BLUE-001", detections)
        self.assertEqual(len(events), 1)
        ledger = output_root / "ENG-BLUE-001" / "blue" / "blue-events.jsonl"
        self.assertTrue(ledger.is_file())
        self.assertIn("Postfix SASL", ledger.read_text(encoding="utf-8"))
        self.assertIn("203.0.113.10", ledger.read_text(encoding="utf-8"))

    def test_suricata_parser_ignores_non_alert_event_with_alert_metadata(self):
        log = self.write_log(
            "eve-flow.json",
            json.dumps({
                "event_type": "flow",
                "src_ip": "203.0.113.10",
                "dest_ip": "198.51.100.20",
                "alert": {"signature": "Prior alert metadata", "severity": 2},
            }) + "\n",
        )
        detections = blue_live_adapter.ingest_sources([f"suricata_eve={log}"])
        self.assertEqual(detections, [])

    def test_tail_once_checkpoint_prevents_duplicate_ingest(self):
        log = self.write_log(
            "auth.log",
            "May 16 10:00:00 host sshd[100]: Failed password for invalid user admin from 203.0.113.10 port 53222 ssh2\n",
        )
        output_root = self.root / "_spectra-output" / "duel"
        checkpoint = self.root / "blue-tail.checkpoint.json"

        first = blue_live_adapter.tail_once(
            sources=[f"auth={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-001",
        )
        second = blue_live_adapter.tail_once(
            sources=[f"auth={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-001",
        )

        self.assertEqual(first["count"], 1)
        self.assertEqual(second["count"], 0)
        ledger = output_root / "ENG-BLUE-TAIL-001" / "blue" / "blue-events.jsonl"
        self.assertEqual(len(ledger.read_text(encoding="utf-8").splitlines()), 1)

        state = json.loads(checkpoint.read_text(encoding="utf-8"))
        key = blue_live_adapter.checkpoint_key("auth", log)
        self.assertEqual(state["sources"][key]["offset"], log.stat().st_size)

    def test_tail_once_appends_only_new_lines_after_checkpoint(self):
        log = self.write_log(
            "access.log",
            '203.0.113.10 - - [16/May/2026:10:00:00 +0000] "GET /health HTTP/1.1" 200 2 "-" "curl/8"\n',
        )
        output_root = self.root / "_spectra-output" / "duel"
        checkpoint = self.root / "blue-tail.checkpoint.json"

        first = blue_live_adapter.tail_once(
            sources=[f"nginx_access={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-002",
        )
        self.append_log(
            log,
            '203.0.113.10 - - [16/May/2026:10:01:00 +0000] "GET /.env HTTP/1.1" 403 153 "-" "curl/8"\n',
        )
        second = blue_live_adapter.tail_once(
            sources=[f"nginx_access={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-002",
        )

        self.assertEqual(first["count"], 0)
        self.assertEqual(second["count"], 1)
        self.assertEqual(second["detections"][0]["technique"], "T1595.003")
        ledger = output_root / "ENG-BLUE-TAIL-002" / "blue" / "blue-events.jsonl"
        lines = ledger.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        self.assertIn("/.env", lines[0])

    def test_tail_once_keeps_partial_line_until_newline(self):
        log = self.write_log(
            "partial-auth.log",
            "May 16 10:00:00 host sshd[100]: Failed password for invalid user admin from 203.0.113.10",
        )
        output_root = self.root / "_spectra-output" / "duel"
        checkpoint = self.root / "blue-tail-partial.checkpoint.json"

        first = blue_live_adapter.tail_once(
            sources=[f"auth={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-003",
        )
        self.append_log(log, " port 53222 ssh2\n")
        second = blue_live_adapter.tail_once(
            sources=[f"auth={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-003",
        )

        self.assertEqual(first["count"], 0)
        self.assertEqual(second["count"], 1)
        self.assertIn("admin", second["detections"][0]["summary"])

    def test_tail_once_resets_offset_when_inode_changes(self):
        log = self.write_log(
            "rotate-auth.log",
            "May 16 10:00:00 host sshd[100]: Failed password for invalid user admin from 203.0.113.10 port 53222 ssh2\n",
        )
        output_root = self.root / "_spectra-output" / "duel"
        checkpoint = self.root / "blue-tail-rotate.checkpoint.json"

        first = blue_live_adapter.tail_once(
            sources=[f"auth={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-004",
        )
        rotated = log.with_suffix(".log.1")
        log.rename(rotated)
        log.write_text(
            "May 16 10:01:00 host sshd[101]: Failed password for invalid user deploy from 203.0.113.11 port 53223 ssh2\n",
            encoding="utf-8",
        )
        second = blue_live_adapter.tail_once(
            sources=[f"auth={log}"],
            checkpoint_path=checkpoint,
            output_root=output_root,
            session_id="ENG-BLUE-TAIL-004",
        )

        self.assertEqual(first["count"], 1)
        self.assertEqual(second["count"], 1)
        self.assertIn("deploy", second["detections"][0]["summary"])


if __name__ == "__main__":
    unittest.main()
