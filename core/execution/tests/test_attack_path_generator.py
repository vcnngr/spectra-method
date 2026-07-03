#!/usr/bin/env python3
"""Regression tests for the SPECTRA Attack-Path Generator."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "attack-path-generator.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


apg = load_module("attack_path_generator", SCRIPT)


ENGAGEMENT_YAML = """\
engagement:
  id: "ENG-TEST-001"
  type: "pentest"
  client_name: "Acme"
kill_chain:
  reconnaissance:
    status: "complete"
    agent: "spectra-agent-recon"
  weaponization:
    status: "pending"
    agent: ""
  delivery:
    status: "in-progress"
    agent: "spectra-agent-operator"
  exploitation:
    status: "complete"
    agent: "spectra-agent-exploit"
"""


FINDING_CRITICAL = """\
id: "F-001"
title: "Unauthenticated RCE on web app"
severity: "critical"
technique: "T1190"
phase: "exploitation"
evidence:
  - "EV-12"
  - "EV-13"
"""

# Medium severity, carries a technique but NO evidence -> unverified, not chained.
FINDING_MEDIUM_NOEV = """\
id: "F-002"
title: "Verbose error messages"
severity: "medium"
technique: "T1592"
phase: "reconnaissance"
"""

# High severity, no technique -> chained to impact, but excluded from detection ratio.
FINDING_HIGH_NOTECH = """\
id: "F-003"
title: "Weak password policy"
severity: "high"
"""


class AttackPathGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # report-adapters resolves evidence registry at <eng_dir>.parent.parent,
        # so nest the engagement a couple of levels deep like a real output tree.
        self.eng_dir = self.root / "engagements" / "ENG-TEST-001"
        self.findings_dir = self.eng_dir / "findings"
        self.findings_dir.mkdir(parents=True)
        self.engagement_path = self.eng_dir / "engagement.yaml"
        self.engagement_path.write_text(ENGAGEMENT_YAML, encoding="utf-8")
        (self.findings_dir / "f-001.yaml").write_text(FINDING_CRITICAL, encoding="utf-8")
        (self.findings_dir / "f-002.yaml").write_text(FINDING_MEDIUM_NOEV, encoding="utf-8")
        (self.findings_dir / "f-003.yaml").write_text(FINDING_HIGH_NOTECH, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _build(self, duel_ledger=None):
        return apg.build_attack_path(str(self.engagement_path), duel_ledger)

    # -- structure ---------------------------------------------------------

    def test_schema_and_core_nodes(self):
        graph = self._build()
        self.assertEqual(graph["schema"], "spectra.attack-path/v1")
        node_types = [n["type"] for n in graph["nodes"]]
        self.assertIn("entry", node_types)
        self.assertIn("impact", node_types)
        # Exactly one entry and one impact node.
        self.assertEqual(node_types.count("entry"), 1)
        self.assertEqual(node_types.count("impact"), 1)

    def test_only_active_phases_rendered(self):
        graph = self._build()
        phases = [n["phase"] for n in graph["nodes"] if n["type"] == "phase"]
        # weaponization is "pending" -> excluded; the rest are active.
        self.assertIn("reconnaissance", phases)
        self.assertIn("delivery", phases)
        self.assertIn("exploitation", phases)
        self.assertNotIn("weaponization", phases)

    def test_phases_in_canonical_order(self):
        graph = self._build()
        phases = [n["phase"] for n in graph["nodes"] if n["type"] == "phase"]
        self.assertEqual(phases, ["reconnaissance", "delivery", "exploitation"])

    def test_finding_attached_to_its_phase(self):
        graph = self._build()
        # F-001 belongs to exploitation -> an edge from phase:exploitation to it.
        edge = next(
            e for e in graph["edges"]
            if e["target"] == "finding:F-001" and e["type"] == "exploits"
        )
        self.assertEqual(edge["source"], "phase:exploitation")
        self.assertEqual(edge["label"], "T1190")

    def test_finding_without_phase_attaches_to_entry(self):
        graph = self._build()
        edge = next(
            e for e in graph["edges"]
            if e["target"] == "finding:F-003" and e["type"] == "exploits"
        )
        self.assertEqual(edge["source"], "entry")

    # -- evidence ----------------------------------------------------------

    def _write_registry(self, items, integrity_status="UNVERIFIED"):
        # report-adapters resolves the registry at <eng_dir>.parent.parent /
        # evidence / <eng_id> / evidence-registry.yaml.
        reg_dir = self.root / "evidence" / "ENG-TEST-001"
        reg_dir.mkdir(parents=True, exist_ok=True)
        registry = {
            "evidence_registry": {
                "engagement_id": "ENG-TEST-001",
                "integrity_status": integrity_status,
                "item_count": len(items),
                "last_verified": "2026-06-07T00:00:00Z",
                "items": items,
            }
        }
        import yaml  # report-adapters already depends on pyyaml
        (reg_dir / "evidence-registry.yaml").write_text(
            yaml.safe_dump(registry), encoding="utf-8",
        )

    def test_evidence_state_registry_missing(self):
        # No registry on disk: a finding that CLAIMS refs is registry_missing,
        # never "verified". Findings with no refs are no_reference.
        graph = self._build()
        by_id = {n["id"]: n for n in graph["nodes"]}
        self.assertEqual(by_id["finding:F-001"]["evidence_state"], "registry_missing")
        self.assertEqual(by_id["finding:F-001"]["evidence"]["claimed_refs"], ["EV-12", "EV-13"])
        self.assertEqual(by_id["finding:F-002"]["evidence_state"], "no_reference")
        self.assertEqual(by_id["finding:F-003"]["evidence_state"], "no_reference")
        self.assertFalse(graph["summary"]["evidence_registry"]["present"])
        self.assertEqual(graph["summary"]["evidence_backed_findings"], 0)

    def test_evidence_resolved_unverified(self):
        self._write_registry([{"id": "EV-12"}, {"id": "EV-13"}], "UNVERIFIED")
        graph = self._build()
        by_id = {n["id"]: n for n in graph["nodes"]}
        self.assertEqual(by_id["finding:F-001"]["evidence_state"], "resolved_unverified")
        self.assertEqual(by_id["finding:F-001"]["evidence"]["resolved_refs"], ["EV-12", "EV-13"])
        self.assertEqual(graph["summary"]["evidence_backed_findings"], 1)

    def test_evidence_integrity_verified(self):
        self._write_registry([{"id": "EV-12"}, {"id": "EV-13"}], "VERIFIED")
        graph = self._build()
        by_id = {n["id"]: n for n in graph["nodes"]}
        self.assertEqual(by_id["finding:F-001"]["evidence_state"], "integrity_verified")
        self.assertEqual(graph["summary"]["evidence_registry"]["integrity_status"], "VERIFIED")

    def test_evidence_integrity_failed(self):
        self._write_registry([{"id": "EV-12"}, {"id": "EV-13"}], "FAILED")
        graph = self._build()
        by_id = {n["id"]: n for n in graph["nodes"]}
        self.assertEqual(by_id["finding:F-001"]["evidence_state"], "resolved_integrity_failed")

    def test_evidence_partially_resolved(self):
        # Only one of F-001's two refs exists in the registry.
        self._write_registry([{"id": "EV-12"}], "VERIFIED")
        graph = self._build()
        by_id = {n["id"]: n for n in graph["nodes"]}
        node = by_id["finding:F-001"]
        self.assertEqual(node["evidence_state"], "partially_resolved")
        self.assertEqual(node["evidence"]["resolved_refs"], ["EV-12"])
        self.assertEqual(node["evidence"]["unresolved_refs"], ["EV-13"])

    def test_evidence_referenced_unresolved(self):
        # Registry exists but contains none of the claimed refs.
        self._write_registry([{"id": "EV-99"}], "UNVERIFIED")
        graph = self._build()
        by_id = {n["id"]: n for n in graph["nodes"]}
        self.assertEqual(by_id["finding:F-001"]["evidence_state"], "referenced_unresolved")

    def test_evidence_backlink_resolves_finding_without_refs(self):
        # A registry item that names a finding via finding_reference links it,
        # even though the finding carries no evidence field of its own.
        (self.findings_dir / "f-back.yaml").write_text(
            "id: \"F-BACK\"\ntitle: \"Backlinked finding\"\nseverity: \"low\"\n",
            encoding="utf-8",
        )
        self._write_registry(
            [{"id": "EV-50", "finding_reference": "F-BACK"}], "VERIFIED",
        )
        graph = self._build()
        by_id = {n["id"]: n for n in graph["nodes"]}
        node = by_id["finding:F-BACK"]
        self.assertEqual(node["evidence_state"], "integrity_verified")
        self.assertEqual(node["evidence"]["linked_items"], ["EV-50"])

    def test_evidence_breakdown_sums_to_finding_count(self):
        self._write_registry([{"id": "EV-12"}, {"id": "EV-13"}], "VERIFIED")
        graph = self._build()
        breakdown = graph["summary"]["evidence_breakdown"]
        self.assertEqual(sum(breakdown.values()), graph["summary"]["finding_count"])

    # -- impact chaining ---------------------------------------------------

    def test_high_and_critical_chain_to_impact(self):
        graph = self._build()
        escalate_sources = {
            e["source"] for e in graph["edges"] if e["type"] == "escalates"
        }
        self.assertIn("finding:F-001", escalate_sources)  # critical
        self.assertIn("finding:F-003", escalate_sources)  # high
        self.assertNotIn("finding:F-002", escalate_sources)  # medium
        self.assertEqual(graph["summary"]["chained_to_impact"], 2)

    def test_severity_counts(self):
        graph = self._build()
        counts = graph["summary"]["severity_counts"]
        self.assertEqual(counts["critical"], 1)
        self.assertEqual(counts["high"], 1)
        self.assertEqual(counts["medium"], 1)

    # -- detection overlay -------------------------------------------------

    def test_no_overlay_without_ledger(self):
        graph = self._build()
        self.assertFalse(graph["summary"]["detection_overlay"])
        self.assertNotIn("detection", graph["summary"])
        for node in graph["nodes"]:
            self.assertNotIn("detected", node)

    def test_detection_overlay_from_duel_ledger(self):
        ledger = self.root / "blue.jsonl"
        ledger.write_text(
            "\n".join([
                json.dumps({"role": "blue", "event_type": "detection", "technique": "T1190"}),
                json.dumps({"role": "blue", "event_type": "alert", "technique": "T9999"}),
                # Red's own event must NOT count as detection.
                json.dumps({"role": "red", "event_type": "detection", "technique": "T1592"}),
            ]),
            encoding="utf-8",
        )
        graph = self._build(duel_ledger=str(ledger))
        self.assertTrue(graph["summary"]["detection_overlay"])
        det = graph["summary"]["detection"]
        # F-001 (T1190) detected; F-002 (T1592) NOT detected (only red logged it).
        self.assertEqual(det["techniques_total"], 2)
        self.assertEqual(det["techniques_detected"], 1)
        self.assertEqual(det["techniques_missed"], 1)
        self.assertEqual(det["coverage_ratio"], 0.5)

        by_id = {n["id"]: n for n in graph["nodes"]}
        self.assertTrue(by_id["finding:F-001"]["detected"])
        self.assertFalse(by_id["finding:F-002"]["detected"])
        # F-003 has no technique -> no detected flag.
        self.assertNotIn("detected", by_id["finding:F-003"])

    def test_missing_duel_ledger_raises(self):
        with self.assertRaises(FileNotFoundError):
            self._build(duel_ledger=str(self.root / "nope.jsonl"))

    def test_malformed_ledger_lines_are_skipped(self):
        ledger = self.root / "blue.jsonl"
        ledger.write_text(
            "\n".join([
                "not json at all",
                "[1, 2, 3]",                 # valid JSON, not a dict
                '"a bare string"',           # valid JSON, not a dict
                "",                           # blank line
                json.dumps({"role": "blue", "event_type": "detection", "technique": "T1190"}),
            ]),
            encoding="utf-8",
        )
        graph = self._build(duel_ledger=str(ledger))  # must not raise
        self.assertEqual(graph["summary"]["detection"]["techniques_detected"], 1)

    def test_technique_match_is_case_insensitive(self):
        ledger = self.root / "blue.jsonl"
        # Ledger uses lowercase technique; finding F-001 uses upper-case "T1190".
        ledger.write_text(
            json.dumps({"role": "blue", "event_type": "alert", "technique": "t1190"}),
            encoding="utf-8",
        )
        graph = self._build(duel_ledger=str(ledger))
        by_id = {n["id"]: n for n in graph["nodes"]}
        self.assertTrue(by_id["finding:F-001"]["detected"])
        self.assertEqual(graph["summary"]["detection"]["techniques_detected"], 1)

    def test_duplicate_finding_ids_get_unique_nodes(self):
        # Two findings with the same id must not collapse into one node.
        (self.findings_dir / "f-001-dup.yaml").write_text(
            "id: \"F-001\"\ntitle: \"Duplicate id finding\"\nseverity: \"low\"\n",
            encoding="utf-8",
        )
        graph = self._build()
        finding_ids = [n["id"] for n in graph["nodes"] if n["type"] == "finding"]
        self.assertEqual(len(finding_ids), len(set(finding_ids)))  # all unique
        self.assertIn("finding:F-001", finding_ids)
        self.assertTrue(any(nid.startswith("finding:F-001#") for nid in finding_ids))

    def test_repeated_technique_counted_once(self):
        # A second finding reusing T1190 must not inflate techniques_total.
        (self.findings_dir / "f-004.yaml").write_text(
            "id: \"F-004\"\ntitle: \"Second RCE vector\"\nseverity: \"high\"\n"
            "technique: \"T1190\"\nphase: \"exploitation\"\n",
            encoding="utf-8",
        )
        ledger = self.root / "blue.jsonl"
        ledger.write_text(
            json.dumps({"role": "blue", "event_type": "detection", "technique": "T1190"}),
            encoding="utf-8",
        )
        graph = self._build(duel_ledger=str(ledger))
        det = graph["summary"]["detection"]
        # Unique techniques in path: T1190, T1592 -> total 2 (not 3).
        self.assertEqual(det["techniques_total"], 2)
        self.assertEqual(det["techniques_detected"], 1)

    def test_finding_in_excluded_phase_falls_back_to_entry(self):
        # A finding attributed to a PENDING (excluded) phase must not produce a
        # dangling edge to a non-existent phase node — it falls back to entry.
        (self.findings_dir / "f-weap.yaml").write_text(
            "id: \"F-WEAP\"\ntitle: \"Staged payload\"\nseverity: \"low\"\n"
            "phase: \"weaponization\"\n",  # weaponization is pending -> no node
            encoding="utf-8",
        )
        graph = self._build()
        node_ids = {n["id"] for n in graph["nodes"]}
        self.assertNotIn("phase:weaponization", node_ids)
        edge = next(e for e in graph["edges"] if e["target"] == "finding:F-WEAP")
        self.assertEqual(edge["source"], "entry")
        # No edge may reference a node that does not exist.
        for e in graph["edges"]:
            self.assertIn(e["source"], node_ids)
            self.assertIn(e["target"], node_ids)

    def test_no_impact_node_when_nothing_chains(self):
        # An engagement with only low/medium findings has no impact chain, so the
        # impact node must be omitted rather than left orphaned.
        for f in self.findings_dir.iterdir():
            f.unlink()
        (self.findings_dir / "f-low.yaml").write_text(
            "id: \"F-L\"\ntitle: \"Minor info leak\"\nseverity: \"low\"\n", encoding="utf-8",
        )
        graph = self._build()
        node_types = [n["type"] for n in graph["nodes"]]
        self.assertNotIn("impact", node_types)
        self.assertEqual(graph["summary"]["chained_to_impact"], 0)
        self.assertFalse(any(e["type"] == "escalates" for e in graph["edges"]))

    def test_mitigation_event_does_not_count_as_detection(self):
        ledger = self.root / "blue.jsonl"
        ledger.write_text(
            json.dumps({"role": "blue", "event_type": "mitigation", "technique": "T1190"}),
            encoding="utf-8",
        )
        graph = self._build(duel_ledger=str(ledger))
        # Mitigation is a response, not a detection — coverage stays 0.
        self.assertEqual(graph["summary"]["detection"]["techniques_detected"], 0)

    def test_plural_technique_field_counted(self):
        (self.findings_dir / "f-multi.yaml").write_text(
            "id: \"F-MULTI\"\ntitle: \"Chained abuse\"\nseverity: \"high\"\n"
            "techniques:\n  - \"T1078\"\n  - \"T1059\"\n",
            encoding="utf-8",
        )
        graph = self._build()
        node = next(n for n in graph["nodes"] if n["id"] == "finding:F-MULTI")
        self.assertEqual(node["techniques"], ["T1078", "T1059"])
        self.assertEqual(node["technique"], "T1078")  # primary

    def test_partial_multi_technique_detection_is_a_gap(self):
        (self.findings_dir / "f-multi.yaml").write_text(
            "id: \"F-MULTI\"\ntitle: \"Chained abuse\"\nseverity: \"high\"\n"
            "phase: \"exploitation\"\ntechniques:\n  - \"T1078\"\n  - \"T1059\"\n",
            encoding="utf-8",
        )
        ledger = self.root / "blue.jsonl"
        # Only one of the two techniques detected -> finding is NOT fully detected.
        ledger.write_text(
            json.dumps({"role": "blue", "event_type": "detection", "technique": "T1078"}),
            encoding="utf-8",
        )
        graph = self._build(duel_ledger=str(ledger))
        node = next(n for n in graph["nodes"] if n["id"] == "finding:F-MULTI")
        self.assertFalse(node["detected"])
        det = graph["summary"]["detection"]
        # Path techniques: T1190(F-001), T1592(F-002), T1078, T1059 -> 4 unique.
        self.assertEqual(det["techniques_total"], 4)
        self.assertEqual(det["techniques_detected"], 1)  # only T1078

    def test_adapter_loader_unresolvable_raises(self):
        import unittest.mock as mock
        # When importlib cannot build a spec, the loader must raise (not return None).
        with mock.patch.object(apg.importlib.util, "spec_from_file_location", return_value=None):
            with self.assertRaises(RuntimeError):
                apg._load_report_adapters()

    # -- mermaid -----------------------------------------------------------

    def test_mermaid_render(self):
        graph = self._build()
        mermaid = apg.render_mermaid(graph)
        self.assertTrue(mermaid.startswith("flowchart LR"))
        self.assertIn("Impact / Objective", mermaid)
        self.assertIn("Entry / Attacker", mermaid)

    def test_mermaid_ids_are_unique(self):
        graph = self._build()
        id_map = apg._mermaid_id_map(graph)
        # One id per node, all distinct, even for adversarial raw ids.
        self.assertEqual(len(id_map), len(graph["nodes"]))
        self.assertEqual(len(set(id_map.values())), len(graph["nodes"]))

    def test_mermaid_id_collision_safety(self):
        # Two raw ids that sanitize to the same string must stay distinct.
        graph = {"nodes": [{"id": "finding:a/b", "type": "finding", "label": "x"},
                           {"id": "finding:a:b", "type": "finding", "label": "y"}],
                 "edges": []}
        id_map = apg._mermaid_id_map(graph)
        self.assertEqual(len(set(id_map.values())), 2)

    def test_mermaid_handles_adversarial_labels(self):
        graph = {"nodes": [{"id": "n", "type": "finding", "label": 'evil"]|{(\\ end',
                            "severity": "low"}],
                 "edges": [{"source": "n", "target": "n", "label": 'a|b"c\\'}]}
        mermaid = apg.render_mermaid(graph)  # must not raise
        # Raw double-quote and pipe must not survive into the output verbatim.
        self.assertNotIn('"]|', mermaid)
        self.assertNotIn('a|b', mermaid)

    def test_mermaid_marks_missed_detection(self):
        ledger = self.root / "blue.jsonl"
        ledger.write_text(
            json.dumps({"role": "blue", "event_type": "detection", "technique": "T1190"}),
            encoding="utf-8",
        )
        graph = self._build(duel_ledger=str(ledger))
        mermaid = apg.render_mermaid(graph)
        self.assertIn("detected", mermaid)
        self.assertIn("MISSED", mermaid)  # T1592 was not detected


if __name__ == "__main__":
    unittest.main()
