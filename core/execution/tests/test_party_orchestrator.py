#!/usr/bin/env python3
"""Regression tests for Party Mode sub-agent planner."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "party-orchestrator.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


party_orchestrator = load_module("party_orchestrator", SCRIPT)


class PartyOrchestratorTests(unittest.TestCase):
    def test_adversarial_plan_has_red_blue_purple_and_gates(self):
        plan = party_orchestrator.build_plan(
            topic="lateral movement detection gap review",
            mode="adversarial",
            agents_per_team=1,
        )
        teams = {agent["team"] for agent in plan["sub_agents"]}
        self.assertIn("red", teams)
        self.assertIn("blue", teams)
        self.assertIn("purple", teams)
        self.assertTrue(plan["safety_contract"]["requires_engagement_scope"])
        self.assertIn("engagement-state gate", plan["safety_contract"]["rtk_execution_requires"])

    def test_incident_plan_prioritizes_defense_and_response(self):
        plan = party_orchestrator.build_plan(
            topic="ransomware incident containment and executive update",
            mode="incident",
            agents_per_team=1,
        )
        teams = {agent["team"] for agent in plan["sub_agents"]}
        self.assertIn("blue", teams)
        self.assertIn("purple", teams)
        self.assertNotIn("red", teams)
        self.assertEqual(plan["rounds"][1]["id"], "triage")

    def test_markdown_render_includes_model_profiles(self):
        plan = party_orchestrator.build_plan(
            topic="cloud detection engineering",
            mode="purple",
            agents_per_team=1,
        )
        content = party_orchestrator.render_markdown(plan)
        self.assertIn("SPECTRA Party Plan", content)
        self.assertIn("Model profile", content)

    def test_modules_filter_prevents_uninstalled_agent_selection(self):
        plan = party_orchestrator.build_plan(
            topic="red blue detection review",
            mode="adversarial",
            agents_per_team=1,
            modules=["core"],
        )
        modules = {agent["module"] for agent in plan["sub_agents"]}
        self.assertEqual(modules, {"core"})

    def test_party_v2_emits_lane_contracts_and_quality_gates(self):
        plan = party_orchestrator.build_plan(
            topic="distributed red blue incident readiness",
            mode="purple",
            agents_per_team=1,
            lanes=["red", "blue", "irt", "grc", "core"],
        )
        self.assertEqual(plan["schema_version"], "0.2")
        lanes = {agent["lane"] for agent in plan["sub_agents"]}
        self.assertIn("red", lanes)
        self.assertIn("blue", lanes)
        self.assertIn("irt", lanes)
        self.assertIn("grc", lanes)
        self.assertIn("coordinator", lanes)
        self.assertTrue(plan["quality_gates"])
        for agent in plan["sub_agents"]:
            self.assertIn("input_contract", agent)
            self.assertIn("output_contract", agent)
            self.assertIn("required_json_keys", agent["output_contract"])
            self.assertIn("done_criteria", agent["task_contract"])
        self.assertEqual(len(plan["spawn_manifest"]), len(plan["sub_agents"]))

    def test_lane_override_limits_spawn_manifest(self):
        plan = party_orchestrator.build_plan(
            topic="telemetry detection review",
            mode="collaborative",
            agents_per_team=1,
            lanes=["blue", "irt"],
        )
        lanes = {item["lane"] for item in plan["spawn_manifest"]}
        self.assertEqual(lanes, {"blue", "irt"})


if __name__ == "__main__":
    unittest.main()
