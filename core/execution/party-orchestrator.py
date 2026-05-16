#!/usr/bin/env python3
"""SPECTRA Party Mode planner.

Builds deterministic multi-agent task plans from the agent manifest. The script
does not call external LLM providers. It emits a machine-readable plan that an
IDE, runner, or human operator can use to spawn sub-agents with clear roles,
outputs, and safety gates.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - validator installs pyyaml
    yaml = None


TEAM_BY_MODULE = {
    "rtk": "red",
    "soc": "blue",
    "irt": "purple",
    "grc": "purple",
    "core": "purple",
}

DEFAULT_MODEL_PROFILES = {
    "coordinator": {
        "class": "balanced-reasoning",
        "latency": "medium",
        "use_for": "round control, synthesis, conflict resolution",
    },
    "red": {
        "class": "deep-reasoning",
        "latency": "medium",
        "use_for": "attack-path analysis, feasibility review, risk discovery",
    },
    "blue": {
        "class": "fast-analytical",
        "latency": "low",
        "use_for": "detection mapping, log questions, control validation",
    },
    "purple": {
        "class": "deep-synthesis",
        "latency": "medium",
        "use_for": "risk arbitration, evidence synthesis, executive framing",
    },
    "scribe": {
        "class": "long-context-writing",
        "latency": "medium",
        "use_for": "reporting, decision log, action register",
    },
}

MODE_ROUNDS = {
    "adversarial": [
        ("frame", "Coordinator frames objective, scope, assumptions, and evidence needs."),
        ("red-position", "Red sub-agent identifies plausible attack paths and constraints."),
        ("blue-counter", "Blue sub-agent maps detections, controls, telemetry, and response gaps."),
        ("purple-arbitration", "Purple sub-agent scores risk, resolves disagreement, and records decisions."),
        ("action-register", "Scribe converts outcome into tasks, owners, evidence, and follow-up workflows."),
    ],
    "collaborative": [
        ("frame", "Coordinator frames objective, scope, assumptions, and evidence needs."),
        ("parallel-analysis", "Specialist sub-agents work in parallel on their assigned lanes."),
        ("merge", "Coordinator merges compatible findings and flags conflicts."),
        ("action-register", "Scribe converts outcome into tasks, owners, evidence, and follow-up workflows."),
    ],
    "purple": [
        ("frame", "Coordinator frames objective, scope, assumptions, and evidence needs."),
        ("emulate", "Red sub-agent proposes bounded adversary hypotheses."),
        ("detect", "Blue sub-agent maps detection and response coverage."),
        ("validate", "Purple sub-agent converts both sides into validation tests and measurable controls."),
        ("action-register", "Scribe converts outcome into tasks, owners, evidence, and follow-up workflows."),
    ],
    "incident": [
        ("frame", "Coordinator states incident objective, severity, timeline, and containment constraints."),
        ("triage", "SOC/IRT sub-agents split triage, timeline, forensics, malware, and threat intel lanes."),
        ("containment-review", "Blue/Purple sub-agents compare containment options and business impact."),
        ("executive-sync", "Coordinator and scribe prepare status, decisions, and communications."),
    ],
}

TASK_BY_TEAM = {
    "red": {
        "objective": "Find attacker-view gaps and plausible attack paths within scope.",
        "default_outputs": ["attack_paths", "assumptions", "required_evidence", "detection_questions"],
    },
    "blue": {
        "objective": "Map controls, telemetry, detections, response paths, and blind spots.",
        "default_outputs": ["coverage_map", "control_gaps", "queries_needed", "response_actions"],
    },
    "purple": {
        "objective": "Arbitrate risk, preserve evidence quality, and convert disagreement into decisions.",
        "default_outputs": ["risk_decisions", "evidence_requirements", "owners", "next_workflows"],
    },
}

SAFETY_CONTRACT = {
    "requires_engagement_scope": True,
    "requires_authorization": True,
    "hard_blocks": [
        "destructive payload generation",
        "ransomware or wiper instructions",
        "unauthorized target execution",
    ],
    "rtk_execution_requires": [
        "engagement-state gate",
        "scope-enforcer check",
        "rules of engagement confirmation",
    ],
}


@dataclass
class Agent:
    name: str
    display_name: str
    title: str
    capabilities: str
    role: str
    principles: str
    module: str
    path: str

    @property
    def team(self) -> str:
        return TEAM_BY_MODULE.get(self.module, "purple")

    @property
    def searchable(self) -> str:
        return " ".join([
            self.name,
            self.display_name,
            self.title,
            self.capabilities,
            self.role,
            self.principles,
        ]).lower()


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[2]


def default_manifest_path() -> Path:
    return repo_root_from_script() / "_config" / "agent-manifest.csv"


def load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.is_file() or yaml is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def load_model_profiles(config_path: Path | None = None) -> dict[str, Any]:
    profiles = dict(DEFAULT_MODEL_PROFILES)
    if config_path:
        config = load_yaml_file(config_path)
    else:
        config = load_yaml_file(repo_root_from_script() / "core" / "config.yaml")
    configured = config.get("llm_routing", {}).get("profiles", {})
    if isinstance(configured, dict):
        for key, value in configured.items():
            if isinstance(value, dict):
                profiles[key] = {**profiles.get(key, {}), **value}
    return profiles


def load_agents(manifest_path: Path) -> list[Agent]:
    if not manifest_path.is_file():
        raise FileNotFoundError(f"agent manifest not found: {manifest_path}")
    rows: list[Agent] = []
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            rows.append(Agent(
                name=row.get("name", "").strip(),
                display_name=row.get("displayName", "").strip(),
                title=row.get("title", "").strip(),
                capabilities=row.get("capabilities", "").strip(),
                role=row.get("role", "").strip(),
                principles=row.get("principles", "").strip(),
                module=row.get("module", "").strip(),
                path=row.get("path", "").strip(),
            ))
    return rows


def topic_terms(topic: str) -> list[str]:
    words = re.findall(r"[a-z0-9][a-z0-9_-]{2,}", topic.lower())
    stop = {"and", "the", "for", "with", "from", "into", "team", "mode", "party"}
    return [w for w in words if w not in stop]


def score_agent(agent: Agent, terms: list[str], preferred_team: str | None = None) -> int:
    text = agent.searchable
    score = 0
    for term in terms:
        if term in text:
            score += 3
        if term in agent.capabilities.lower():
            score += 2
        if term in agent.title.lower():
            score += 1
    if preferred_team and agent.team == preferred_team:
        score += 2
    if agent.module == "core":
        score += 1
    return score


def select_agents(agents: list[Agent], topic: str, mode: str, agents_per_team: int) -> list[Agent]:
    terms = topic_terms(topic)
    by_team = {
        team: [a for a in agents if a.team == team]
        for team in ("red", "blue", "purple")
    }

    selected: list[Agent] = []
    if mode == "collaborative":
        pool = sorted(agents, key=lambda a: score_agent(a, terms), reverse=True)
        return pool[: max(3, agents_per_team * 2)]

    required = {
        "adversarial": ("red", "blue", "purple"),
        "purple": ("red", "blue", "purple"),
        "incident": ("blue", "purple"),
    }.get(mode, ("red", "blue", "purple"))

    for team in required:
        ranked = sorted(by_team[team], key=lambda a: score_agent(a, terms, team), reverse=True)
        selected.extend(ranked[:agents_per_team])

    # Prefer a core coordinator if one exists, without increasing the team size.
    core = next((a for a in agents if a.module == "core" and a.name == "spectra-agent-specter"), None)
    if core and core not in selected:
        for i, agent in enumerate(selected):
            if agent.team == "purple":
                selected[i] = core
                break
        else:
            selected.insert(0, core)

    # Stable de-duplication.
    seen: set[str] = set()
    unique: list[Agent] = []
    for agent in selected:
        if agent.name not in seen:
            unique.append(agent)
            seen.add(agent.name)
    return unique


def model_profile_for(agent: Agent, profiles: dict[str, Any]) -> dict[str, Any]:
    key = agent.team
    if agent.name == "spectra-agent-chronicle":
        key = "scribe"
    if agent.name == "spectra-agent-specter":
        key = "coordinator"
    return {"profile": key, **profiles.get(key, {})}


def build_sub_agent(agent: Agent, topic: str, profiles: dict[str, Any], index: int) -> dict[str, Any]:
    task = TASK_BY_TEAM[agent.team]
    return {
        "id": f"subagent-{index:02d}-{agent.display_name.lower().replace(' ', '-')}",
        "source_agent": agent.name,
        "display_name": agent.display_name,
        "title": agent.title,
        "team": agent.team,
        "module": agent.module,
        "model_routing": model_profile_for(agent, profiles),
        "task_contract": {
            "topic": topic,
            "objective": task["objective"],
            "stay_in_role": True,
            "respect_scope": True,
            "outputs": task["default_outputs"],
            "handoff_format": "markdown+json-summary",
        },
        "prompt_contract": [
            f"Act as {agent.display_name}, {agent.title}.",
            "Use the SPECTRA engagement scope and rules of engagement as hard constraints.",
            "Return evidence-backed findings, assumptions, blockers, and next actions.",
            "Do not produce destructive payloads or unauthorized execution instructions.",
        ],
    }


def build_plan(
    topic: str,
    mode: str,
    manifest_path: Path | None = None,
    config_path: Path | None = None,
    agents_per_team: int = 1,
    modules: list[str] | None = None,
) -> dict[str, Any]:
    manifest = manifest_path or default_manifest_path()
    agents = load_agents(manifest)
    if modules:
        allowed_modules = set(modules)
        agents = [agent for agent in agents if agent.module in allowed_modules]
    profiles = load_model_profiles(config_path)
    selected = select_agents(agents, topic, mode, agents_per_team)
    sub_agents = [
        build_sub_agent(agent, topic, profiles, index)
        for index, agent in enumerate(selected, start=1)
    ]
    return {
        "schema_version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "topic": topic,
        "mode": mode,
        "safety_contract": SAFETY_CONTRACT,
        "coordinator": {
            "model_routing": profiles["coordinator"],
            "responsibilities": [
                "load engagement context",
                "spawn or simulate sub-agents",
                "enforce scope gates",
                "merge outputs",
                "resolve conflicts",
            ],
        },
        "sub_agents": sub_agents,
        "rounds": [
            {"id": rid, "objective": objective}
            for rid, objective in MODE_ROUNDS.get(mode, MODE_ROUNDS["adversarial"])
        ],
        "execution_notes": [
            "Spawn sub-agents only after engagement scope is loaded.",
            "Give each sub-agent the same engagement ID and artifact root.",
            "Merge final outputs through Specter or Chronicle before reporting.",
        ],
    }


def render_markdown(plan: dict[str, Any]) -> str:
    lines = [
        f"# SPECTRA Party Plan - {plan['mode']}",
        "",
        f"Topic: {plan['topic']}",
        f"Generated: {plan['generated_at']}",
        "",
        "## Safety Gates",
    ]
    for block in plan["safety_contract"]["hard_blocks"]:
        lines.append(f"- Hard block: {block}")
    lines.extend(["", "## Sub-Agents"])
    for agent in plan["sub_agents"]:
        routing = agent["model_routing"]
        lines.extend([
            f"- {agent['display_name']} ({agent['team']}, {agent['title']})",
            f"  - Model profile: {routing.get('profile')} / {routing.get('class')}",
            f"  - Objective: {agent['task_contract']['objective']}",
        ])
    lines.extend(["", "## Rounds"])
    for round_item in plan["rounds"]:
        lines.append(f"- {round_item['id']}: {round_item['objective']}")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic SPECTRA Party Mode sub-agent plan.")
    sub = parser.add_subparsers(dest="command", required=True)

    plan_cmd = sub.add_parser("plan", help="Generate a sub-agent Party Mode plan")
    plan_cmd.add_argument("--topic", required=True, help="Discussion or task topic")
    plan_cmd.add_argument("--mode", choices=sorted(MODE_ROUNDS), default="adversarial")
    plan_cmd.add_argument("--agents-per-team", type=int, default=1)
    plan_cmd.add_argument("--manifest", type=Path, default=None)
    plan_cmd.add_argument("--config", type=Path, default=None)
    plan_cmd.add_argument("--modules", default="", help="Comma-separated installed modules to allow")
    plan_cmd.add_argument("--format", choices=("json", "markdown"), default="json")
    plan_cmd.add_argument("--output", type=Path, default=None)

    args = parser.parse_args(argv)
    if args.command == "plan":
        plan = build_plan(
            topic=args.topic,
            mode=args.mode,
            manifest_path=args.manifest,
            config_path=args.config,
            agents_per_team=max(1, args.agents_per_team),
            modules=[m.strip() for m in args.modules.split(",") if m.strip()],
        )
        content = json.dumps(plan, indent=2) if args.format == "json" else render_markdown(plan)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(content + "\n", encoding="utf-8")
        else:
            print(content)
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())
