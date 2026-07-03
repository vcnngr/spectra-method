#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
SPECTRA Engagement State Machine

Deterministic validation, workflow gating, and state transitions for SPECTRA
engagement files.

Usage:
  python engagement-state.py validate --engagement engagement.yaml
  python engagement-state.py status --engagement engagement.yaml
  python engagement-state.py gate --engagement engagement.yaml --workflow spectra-external-recon [--target example.com]
  python engagement-state.py transition --engagement engagement.yaml --workflow spectra-external-recon --to in-progress

Exit codes:
  0 - allowed / valid / transition applied
  1 - blocked by engagement gate or invalid transition
  2 - validation warnings only
  3 - invalid input, missing file, bad YAML
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


VERSION = "0.2.0"

VALID_ENGAGEMENT_STATUSES = {"planning", "active", "paused", "complete", "archived"}
VALID_WORKFLOW_STATUSES = {"pending", "in-progress", "blocked", "complete", "skipped"}

# LLM agents naturally write "completed"/"in progress" when closing a workflow,
# but the canonical enum values are "complete"/"in-progress". Accept the common
# natural-language spellings and canonicalize them, so an engagement.yaml never
# needs a manual edit to validate or transition (see GitHub issue #2).
STATUS_ALIASES = {
    "completed": "complete",
    "complete": "complete",
    "in progress": "in-progress",
    "in_progress": "in-progress",
    "inprogress": "in-progress",
    "in-progress": "in-progress",
}


def canonical_status(value: Any) -> str:
    """Map a status value to its canonical spelling (lowercased, trimmed)."""
    s = str(value or "").strip().lower()
    return STATUS_ALIASES.get(s, s)
VALID_TRANSITIONS = {
    "pending": {"in-progress", "blocked", "skipped"},
    "in-progress": {"complete", "blocked"},
    "blocked": {"in-progress", "skipped"},
    "skipped": {"in-progress"},
    "complete": set(),
}

WORKFLOWS = {
    "spectra-external-recon": {
        "state_key": "external_recon",
        "kill_chain": "reconnaissance",
        "action": "recon",
        "allowed_types": {"pentest", "red-team", "purple-team", "ctf", "training", "assessment"},
    },
    "external-recon": {
        "state_key": "external_recon",
        "kill_chain": "reconnaissance",
        "action": "recon",
        "allowed_types": {"pentest", "red-team", "purple-team", "ctf", "training", "assessment"},
    },
    "spectra-initial-access": {
        "state_key": "initial_access",
        "kill_chain": "exploitation",
        "action": "initial-access",
        "allowed_types": {"pentest", "red-team", "purple-team", "ctf", "training", "assessment"},
    },
    "initial-access": {
        "state_key": "initial_access",
        "kill_chain": "exploitation",
        "action": "initial-access",
        "allowed_types": {"pentest", "red-team", "purple-team", "ctf", "training", "assessment"},
    },
    "spectra-privesc": {
        "state_key": "privilege_escalation",
        "kill_chain": "installation",
        "action": "privilege-escalation",
        "allowed_types": {"pentest", "red-team", "purple-team", "ctf", "training"},
    },
    "privesc": {
        "state_key": "privilege_escalation",
        "kill_chain": "installation",
        "action": "privilege-escalation",
        "allowed_types": {"pentest", "red-team", "purple-team", "ctf", "training"},
    },
    "spectra-lateral-movement": {
        "state_key": "lateral_movement",
        "kill_chain": "command_and_control",
        "action": "lateral-movement",
        "allowed_types": {"pentest", "red-team", "purple-team", "training"},
    },
    "lateral-movement": {
        "state_key": "lateral_movement",
        "kill_chain": "command_and_control",
        "action": "lateral-movement",
        "allowed_types": {"pentest", "red-team", "purple-team", "training"},
    },
    "spectra-exfiltration": {
        "state_key": "exfiltration",
        "kill_chain": "actions_on_objectives",
        "action": "exfiltration",
        "allowed_types": {"pentest", "red-team", "purple-team", "training"},
        "requires_roe": "data_exfiltration_allowed",
    },
    "exfiltration": {
        "state_key": "exfiltration",
        "kill_chain": "actions_on_objectives",
        "action": "exfiltration",
        "allowed_types": {"pentest", "red-team", "purple-team", "training"},
        "requires_roe": "data_exfiltration_allowed",
    },
}


def _load_scope_enforcer():
    script = Path(__file__).resolve().with_name("scope-enforcer.py")
    spec = importlib.util.spec_from_file_location("scope_enforcer", script)
    if not spec or not spec.loader:
        _die(f"Cannot load scope enforcer: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope_enforcer = _load_scope_enforcer()


def _load_noise_budget():
    script = Path(__file__).resolve().with_name("noise-budget.py")
    spec = importlib.util.spec_from_file_location("noise_budget", script)
    if not spec or not spec.loader:
        _die(f"Cannot load noise budget validator: {script}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


noise_budget = _load_noise_budget()


def load_document(path: str) -> tuple[dict[str, Any], Path]:
    p = Path(path)
    if not p.exists():
        _die(f"Engagement file not found: {path}")
    try:
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        _die(f"Invalid engagement YAML: {exc}")
    if not isinstance(data, dict) or "engagement" not in data:
        _die("Invalid engagement file: missing 'engagement' root key")
    if not isinstance(data["engagement"], dict):
        _die("Invalid engagement file: 'engagement' must be an object")
    return data, p


def save_document(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=False), encoding="utf-8")


def normalize_workflow(name: str) -> dict[str, Any]:
    workflow = WORKFLOWS.get(name.strip().lower())
    if not workflow:
        valid = ", ".join(sorted(k for k in WORKFLOWS if k.startswith("spectra-")))
        _die(f"Unknown workflow '{name}'. Valid workflows: {valid}")
    return workflow


def _list_count(section: dict[str, Any], skip_notes: bool = True) -> int:
    total = 0
    for key, value in (section or {}).items():
        if skip_notes and key == "notes":
            continue
        if isinstance(value, list):
            total += len(value)
    return total


def _parse_iso_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(raw).date()
    except ValueError:
        try:
            return date.fromisoformat(raw)
        except ValueError:
            return None


def _today_for_engagement(eng: dict[str, Any]) -> date:
    tz_name = (eng.get("authorization") or {}).get("timezone") or ""
    if tz_name:
        try:
            from zoneinfo import ZoneInfo

            return datetime.now(ZoneInfo(tz_name)).date()
        except Exception:
            pass
    return date.today()


def _scope_counts(eng: dict[str, Any]) -> dict[str, int]:
    scope = eng.get("scope") or {}
    return {
        "in_scope": _list_count(scope.get("in_scope") or {}),
        "out_of_scope": _list_count(scope.get("out_of_scope") or {}),
    }


def validate_document(data: dict[str, Any], strict: bool = False) -> dict[str, Any]:
    eng = data.get("engagement") or {}
    errors: list[str] = []
    warnings: list[str] = []

    required_strings = ["id", "name", "type", "status"]
    for key in required_strings:
        if not str(eng.get(key) or "").strip():
            errors.append(f"engagement.{key} is required")

    status = canonical_status(eng.get("status"))
    if status and status not in VALID_ENGAGEMENT_STATUSES:
        errors.append(f"engagement.status must be one of {sorted(VALID_ENGAGEMENT_STATUSES)}")

    auth = eng.get("authorization") or {}
    for key in ["client", "authorized_by", "authorization_document", "start_date", "end_date", "timezone"]:
        if not str(auth.get(key) or "").strip():
            errors.append(f"engagement.authorization.{key} is required")

    start_date = _parse_iso_date(auth.get("start_date"))
    end_date = _parse_iso_date(auth.get("end_date"))
    if auth.get("start_date") and not start_date:
        errors.append("engagement.authorization.start_date must be ISO-8601 date or datetime")
    if auth.get("end_date") and not end_date:
        errors.append("engagement.authorization.end_date must be ISO-8601 date or datetime")
    if start_date and end_date and start_date > end_date:
        errors.append("engagement.authorization.start_date must be before or equal to end_date")

    scope_counts = _scope_counts(eng)
    if scope_counts["in_scope"] == 0:
        errors.append("engagement.scope.in_scope must contain at least one target")
    if scope_counts["out_of_scope"] == 0:
        warnings.append("engagement.scope.out_of_scope is empty; explicit exclusions are recommended")

    roe = eng.get("rules_of_engagement") or {}
    for key in [
        "testing_hours",
        "notify_before_exploit",
        "notify_on_critical",
        "social_engineering_allowed",
        "physical_access_allowed",
        "dos_testing_allowed",
        "data_exfiltration_allowed",
        "production_systems",
        "max_impact_level",
    ]:
        if key not in roe:
            errors.append(f"engagement.rules_of_engagement.{key} is required")

    max_impact = str(roe.get("max_impact_level") or "").strip()
    if max_impact and max_impact not in {"low", "medium", "high", "critical"}:
        errors.append("engagement.rules_of_engagement.max_impact_level must be low, medium, high, or critical")

    workflow_state = data.get("workflow_state")
    if workflow_state is not None and not isinstance(workflow_state, dict):
        errors.append("workflow_state must be an object")
    if isinstance(workflow_state, dict):
        for key, state in workflow_state.items():
            if not isinstance(state, dict):
                errors.append(f"workflow_state.{key} must be an object")
                continue
            wf_status = canonical_status(state.get("status") or "pending")
            if wf_status not in VALID_WORKFLOW_STATUSES:
                errors.append(f"workflow_state.{key}.status must be one of {sorted(VALID_WORKFLOW_STATUSES)}")

    if strict and "workflow_state" not in data:
        warnings.append("workflow_state missing; engagement-state can initialize it during transition")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "scope_counts": scope_counts,
    }


def gate_document(data: dict[str, Any], workflow_name: str, target: str | None, action: str | None) -> dict[str, Any]:
    eng = data["engagement"]
    workflow = normalize_workflow(workflow_name)
    errors: list[str] = []
    warnings: list[str] = []

    validation = validate_document(data, strict=True)
    errors.extend(validation["errors"])
    warnings.extend(validation["warnings"])

    if canonical_status(eng.get("status")) != "active":
        errors.append("engagement.status must be active before running RTK workflows")

    engagement_type = str(eng.get("type") or "").strip()
    if engagement_type and engagement_type not in workflow["allowed_types"]:
        errors.append(f"engagement.type '{engagement_type}' does not permit workflow {workflow_name}")

    auth = eng.get("authorization") or {}
    today = _today_for_engagement(eng)
    start_date = _parse_iso_date(auth.get("start_date"))
    end_date = _parse_iso_date(auth.get("end_date"))
    if start_date and today < start_date:
        errors.append(f"engagement has not started: today={today.isoformat()} start_date={start_date.isoformat()}")
    if end_date and today > end_date:
        errors.append(f"engagement has expired: today={today.isoformat()} end_date={end_date.isoformat()}")

    roe = eng.get("rules_of_engagement") or {}
    required_roe = workflow.get("requires_roe")
    if required_roe and not scope_enforcer._roe_allows(roe.get(required_roe, False)):
        errors.append(f"{required_roe} must be explicitly allowed before workflow {workflow_name}")

    # A declared noise budget must be coherent before activity opens. Only a FAIL
    # (invalid/contradictory budget) blocks; WARN/INFO are advisory. An absent
    # budget is fine — existing engagements without one are unaffected.
    nb_result = noise_budget.validate_noise_budget(roe)
    if nb_result["status"] == "FAIL":
        for issue in nb_result["issues"]:
            if issue["severity"] == "FAIL":
                errors.append(f"noise_budget: {issue['message']}")

    if workflow["state_key"] == "exfiltration":
        data_handling = eng.get("data_handling") or {}
        if not data_handling:
            errors.append("engagement.data_handling is required before exfiltration")
        for field in ["authorized_data_types", "retention_period", "destruction_procedure"]:
            value = data_handling.get(field)
            if isinstance(value, list):
                missing = len(value) == 0
            else:
                missing = not str(value or "").strip()
            if missing:
                errors.append(f"engagement.data_handling.{field} is required before exfiltration")
        if not scope_enforcer._roe_allows(data_handling.get("encryption_required", False)):
            errors.append("engagement.data_handling.encryption_required must be true before exfiltration")

    effective_action = action or workflow["action"]
    action_ok, restrictions = scope_enforcer.check_action_restrictions(effective_action, roe)
    if not action_ok:
        errors.extend(restrictions)

    target_result = None
    if target:
        target_result = scope_enforcer.run_check(target, eng, effective_action)
        if target_result["verdict"] != "IN_SCOPE":
            errors.append(f"target gate failed: {target_result['verdict']} - {target_result['reason']}")
        if not target_result.get("action_allowed", True):
            errors.extend(target_result.get("restrictions", []))
        if not target_result.get("timing_ok", True):
            errors.extend(target_result.get("restrictions", []))

    state = get_workflow_state(data, workflow["state_key"], workflow)

    return {
        "allowed": len(errors) == 0,
        "workflow": workflow_name,
        "state_key": workflow["state_key"],
        "kill_chain": workflow["kill_chain"],
        "action": effective_action,
        "engagement_id": eng.get("id"),
        "engagement_status": eng.get("status"),
        "workflow_status": state.get("status", "pending"),
        "scope_counts": validation["scope_counts"],
        "target_result": target_result,
        "errors": errors,
        "warnings": warnings,
    }


def default_workflow_state(workflow: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "pending",
        "phase": workflow["kill_chain"],
        "agent": "",
        "started": "",
        "completed": "",
        "findings_count": 0,
        "artifacts": [],
    }


def get_workflow_state(data: dict[str, Any], state_key: str, workflow: dict[str, Any]) -> dict[str, Any]:
    workflow_state = data.setdefault("workflow_state", {})
    if state_key not in workflow_state or not isinstance(workflow_state[state_key], dict):
        workflow_state[state_key] = default_workflow_state(workflow)
    return workflow_state[state_key]


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def transition_document(data: dict[str, Any], workflow_name: str, to_status: str, args: argparse.Namespace) -> dict[str, Any]:
    to_status = canonical_status(to_status)
    if to_status not in VALID_WORKFLOW_STATUSES:
        return {
            "transitioned": False,
            "errors": [f"target status must be one of {sorted(VALID_WORKFLOW_STATUSES)}"],
        }

    workflow = normalize_workflow(workflow_name)
    state = get_workflow_state(data, workflow["state_key"], workflow)
    from_status = canonical_status(state.get("status") or "pending")
    allowed_next = VALID_TRANSITIONS.get(from_status, set())
    if to_status not in allowed_next and not args.force:
        return {
            "transitioned": False,
            "workflow": workflow_name,
            "from": from_status,
            "to": to_status,
            "errors": [f"invalid transition: {from_status} -> {to_status}"],
        }

    state["status"] = to_status
    if args.agent is not None:
        state["agent"] = args.agent
    if args.findings_count is not None:
        state["findings_count"] = args.findings_count
    if args.artifact:
        artifacts = state.setdefault("artifacts", [])
        for artifact in args.artifact:
            if artifact not in artifacts:
                artifacts.append(artifact)
    if to_status == "in-progress" and not state.get("started"):
        state["started"] = now_iso()
    if to_status in {"complete", "skipped", "blocked"}:
        state["completed"] = now_iso()
    if to_status == "in-progress":
        state["completed"] = ""

    kill_chain = data.setdefault("kill_chain", {})
    phase = kill_chain.setdefault(workflow["kill_chain"], {})
    phase["status"] = to_status
    if state.get("agent"):
        phase["agent"] = state["agent"]
    if state.get("started"):
        phase["started"] = state["started"]
    if state.get("completed"):
        phase["completed"] = state["completed"]
    if "findings_count" in phase or state.get("findings_count"):
        phase["findings_count"] = state.get("findings_count", 0)
    phase["artifacts"] = deepcopy(state.get("artifacts", []))

    return {
        "transitioned": True,
        "workflow": workflow_name,
        "state_key": workflow["state_key"],
        "from": from_status,
        "to": to_status,
        "state": state,
        "errors": [],
    }


def cmd_validate(args: argparse.Namespace) -> None:
    data, _ = load_document(args.engagement)
    result = validate_document(data, strict=args.strict)
    print(json.dumps(result, indent=2))
    if result["errors"]:
        sys.exit(1)
    if result["warnings"]:
        sys.exit(2)
    sys.exit(0)


def cmd_status(args: argparse.Namespace) -> None:
    data, _ = load_document(args.engagement)
    result = validate_document(data, strict=False)
    workflow_state = data.get("workflow_state") or {}
    print(json.dumps({
        "engagement_id": data["engagement"].get("id"),
        "engagement_status": data["engagement"].get("status"),
        "valid": result["valid"],
        "errors": result["errors"],
        "warnings": result["warnings"],
        "workflow_state": workflow_state,
        "kill_chain": data.get("kill_chain") or {},
    }, indent=2))
    sys.exit(0 if result["valid"] else 1)


def cmd_gate(args: argparse.Namespace) -> None:
    data, _ = load_document(args.engagement)
    result = gate_document(data, args.workflow, args.target, args.action)
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["allowed"] else 1)


def cmd_transition(args: argparse.Namespace) -> None:
    data, path = load_document(args.engagement)
    gate = gate_document(data, args.workflow, args.target, args.action)
    if not gate["allowed"] and not args.force and args.to_status != "blocked":
        print(json.dumps({
            "transitioned": False,
            "gate": gate,
            "errors": ["workflow gate failed; transition blocked"],
        }, indent=2))
        sys.exit(1)

    result = transition_document(data, args.workflow, args.to_status, args)
    if not gate["allowed"]:
        result["gate"] = gate
    print(json.dumps(result, indent=2))
    if not result["transitioned"]:
        sys.exit(1)
    if not args.dry_run:
        save_document(path, data)
    sys.exit(0)


def _die(msg: str) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(3)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="engagement-state",
        description="SPECTRA deterministic engagement state machine",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_validate = sub.add_parser("validate", help="Validate engagement.yaml")
    p_validate.add_argument("--engagement", required=True)
    p_validate.add_argument("--strict", action="store_true")
    p_validate.set_defaults(func=cmd_validate)

    p_status = sub.add_parser("status", help="Print engagement status")
    p_status.add_argument("--engagement", required=True)
    p_status.set_defaults(func=cmd_status)

    p_gate = sub.add_parser("gate", help="Run deterministic workflow gate")
    p_gate.add_argument("--engagement", required=True)
    p_gate.add_argument("--workflow", required=True)
    p_gate.add_argument("--target")
    p_gate.add_argument("--action")
    p_gate.set_defaults(func=cmd_gate)

    p_transition = sub.add_parser("transition", help="Apply deterministic workflow state transition")
    p_transition.add_argument("--engagement", required=True)
    p_transition.add_argument("--workflow", required=True)
    p_transition.add_argument("--to", dest="to_status", required=True)
    p_transition.add_argument("--target")
    p_transition.add_argument("--action")
    p_transition.add_argument("--agent")
    p_transition.add_argument("--artifact", action="append")
    p_transition.add_argument("--findings-count", type=int)
    p_transition.add_argument("--force", action="store_true")
    p_transition.add_argument("--dry-run", action="store_true")
    p_transition.set_defaults(func=cmd_transition)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
