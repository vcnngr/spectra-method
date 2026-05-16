#!/usr/bin/env python3
"""SPECTRA Blue Live Adapter.

Read defensive telemetry from local log files and append normalized Blue events
to a Duel Mode ledger. The adapter is read-only: it does not modify logs,
services, firewall rules, or host configuration.
"""

from __future__ import annotations

import argparse
import glob
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SOURCE_TYPES = {
    "auth",
    "nginx_access",
    "nginx_error",
    "postfix",
    "dovecot",
    "fail2ban",
    "suricata",
    "suricata_eve",
    "wazuh",
    "zeek",
    "zeek_conn",
    "zeek_dns",
    "zeek_http",
}

MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


@dataclass
class Detection:
    event_type: str
    summary: str
    target: str = ""
    technique: str = ""
    source: str = ""
    confidence: str = "medium"
    severity: str = "medium"
    artifacts: list[str] | None = None

    def to_duel_args(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "summary": self.summary,
            "target": self.target,
            "technique": self.technique,
            "source": self.source,
            "confidence": self.confidence,
            "severity": self.severity,
            "artifacts": self.artifacts or [],
        }


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def duel_script_path() -> Path:
    return Path(__file__).resolve().with_name("duel-orchestrator.py")


def load_duel_module():
    spec = importlib.util.spec_from_file_location("duel_orchestrator_runtime", duel_script_path())
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["duel_orchestrator_runtime"] = module
    spec.loader.exec_module(module)
    return module


def parse_source(value: str) -> tuple[str, str]:
    if "=" not in value:
        raise ValueError("source must use type=path format")
    source_type, path = value.split("=", 1)
    source_type = source_type.strip()
    path = path.strip()
    if source_type not in SOURCE_TYPES:
        raise ValueError(f"unsupported source type: {source_type}; expected one of {sorted(SOURCE_TYPES)}")
    if not path:
        raise ValueError("source path cannot be empty")
    return source_type, path


def expand_paths(path_pattern: str) -> list[Path]:
    matches = [Path(p) for p in glob.glob(path_pattern)]
    if matches:
        return [p for p in matches if p.is_file()]
    p = Path(path_pattern)
    return [p] if p.is_file() else []


def parse_syslog_time(line: str, year: int | None = None) -> str:
    match = re.match(r"^([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d\d):(\d\d):(\d\d)", line)
    if not match:
        return now_utc()
    month, day, hour, minute, second = match.groups()
    current = datetime.now(timezone.utc)
    dt = datetime(
        year or current.year,
        MONTHS.get(month, current.month),
        int(day),
        int(hour),
        int(minute),
        int(second),
        tzinfo=timezone.utc,
    )
    return dt.isoformat()


def parse_auth_line(line: str, source_name: str) -> list[Detection]:
    detections: list[Detection] = []
    failed = re.search(r"Failed password for (invalid user )?(\S+) from ([0-9a-fA-F:.]+)", line)
    if failed:
        invalid, user, ip = failed.groups()
        detections.append(Detection(
            event_type="detection",
            summary=f"SSH failed password for {'invalid user ' if invalid else ''}{user} from {ip}.",
            target="sshd",
            technique="T1110.001",
            source=source_name,
            confidence="high",
            severity="medium",
        ))
    accepted = re.search(r"Accepted (password|publickey) for (\S+) from ([0-9a-fA-F:.]+)", line)
    if accepted:
        method, user, ip = accepted.groups()
        detections.append(Detection(
            event_type="detection",
            summary=f"SSH accepted {method} login for {user} from {ip}.",
            target="sshd",
            technique="T1078",
            source=source_name,
            confidence="high",
            severity="high" if user == "root" else "medium",
        ))
    if "Invalid user" in line:
        match = re.search(r"Invalid user (\S+) from ([0-9a-fA-F:.]+)", line)
        if match:
            user, ip = match.groups()
            detections.append(Detection(
                event_type="observation",
                summary=f"SSH invalid user probe for {user} from {ip}.",
                target="sshd",
                technique="T1589.002",
                source=source_name,
                confidence="medium",
                severity="low",
            ))
    return detections


def parse_nginx_access_line(line: str, source_name: str) -> list[Detection]:
    match = re.match(r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) (?P<proto>[^"]+)" (?P<status>\d{3}) (?P<size>\S+)', line)
    if not match:
        return []
    ip = match.group("ip")
    method = match.group("method")
    path = match.group("path")
    status = int(match.group("status"))
    path_lower = path.lower()
    detections: list[Detection] = []

    auth_paths = ("/login", "/phpmyadmin", "/remote/json.php", "/wp-login", "/admin")
    sensitive_paths = ("/.env", "/.git", "config.inc.php", "backup", ".sql", ".bak")
    if any(marker in path_lower for marker in auth_paths):
        detections.append(Detection(
            event_type="detection",
            summary=f"Web authentication surface touched: {method} {path} from {ip} returned {status}.",
            target=path.split("?")[0],
            technique="T1110.001" if status in {401, 403, 429} else "T1078",
            source=source_name,
            confidence="medium",
            severity="medium",
        ))
    if any(marker in path_lower for marker in sensitive_paths):
        detections.append(Detection(
            event_type="detection",
            summary=f"Sensitive path probe: {method} {path} from {ip} returned {status}.",
            target=path.split("?")[0],
            technique="T1595.003",
            source=source_name,
            confidence="high",
            severity="high" if status < 400 else "medium",
        ))
    if status == 429:
        detections.append(Detection(
            event_type="mitigation",
            summary=f"HTTP rate limiting observed for {ip} on {path}.",
            target=path.split("?")[0],
            technique="T1110.001",
            source=source_name,
            confidence="high",
            severity="medium",
        ))
    return detections


def parse_nginx_error_line(line: str, source_name: str) -> list[Detection]:
    if "client:" not in line:
        return []
    ip_match = re.search(r"client:\s*([0-9a-fA-F:.]+)", line)
    req_match = re.search(r'request:\s*"([^"]+)"', line)
    if "access forbidden" in line.lower() or "permission denied" in line.lower():
        return [Detection(
            event_type="detection",
            summary=f"Nginx access forbidden for {req_match.group(1) if req_match else 'request'} from {ip_match.group(1) if ip_match else 'unknown'}.",
            target="nginx",
            technique="T1595.003",
            source=source_name,
            confidence="medium",
            severity="medium",
        )]
    return []


def parse_postfix_line(line: str, source_name: str) -> list[Detection]:
    detections: list[Detection] = []
    sasl_failed = re.search(r"SASL .*authentication failed.*(?:\[(?P<ip>[0-9a-fA-F:.]+)\])?", line)
    if sasl_failed:
        ip = sasl_failed.group("ip") or "unknown"
        detections.append(Detection(
            event_type="detection",
            summary=f"Postfix SASL authentication failure from {ip}.",
            target="postfix",
            technique="T1110.001",
            source=source_name,
            confidence="high",
            severity="medium",
        ))
    if "NOQUEUE: reject:" in line:
        detections.append(Detection(
            event_type="mitigation",
            summary="Postfix rejected SMTP transaction by policy.",
            target="postfix",
            technique="T1589.002",
            source=source_name,
            confidence="medium",
            severity="low",
        ))
    return detections


def parse_dovecot_line(line: str, source_name: str) -> list[Detection]:
    if "auth failed" in line.lower() or "authentication failed" in line.lower():
        ip_match = re.search(r"rip=([0-9a-fA-F:.]+)", line)
        user_match = re.search(r"user=<([^>]+)>", line)
        return [Detection(
            event_type="detection",
            summary=f"Dovecot authentication failure for {user_match.group(1) if user_match else 'unknown user'} from {ip_match.group(1) if ip_match else 'unknown'}.",
            target="dovecot",
            technique="T1110.001",
            source=source_name,
            confidence="high",
            severity="medium",
        )]
    if "Login:" in line:
        ip_match = re.search(r"rip=([0-9a-fA-F:.]+)", line)
        user_match = re.search(r"user=<([^>]+)>", line)
        return [Detection(
            event_type="detection",
            summary=f"Dovecot successful login for {user_match.group(1) if user_match else 'unknown user'} from {ip_match.group(1) if ip_match else 'unknown'}.",
            target="dovecot",
            technique="T1078",
            source=source_name,
            confidence="high",
            severity="medium",
        )]
    return []


def parse_fail2ban_line(line: str, source_name: str) -> list[Detection]:
    if " Ban " in line or "NOTICE  [sshd] Ban" in line:
        ip_match = re.search(r"Ban\s+([0-9a-fA-F:.]+)", line)
        return [Detection(
            event_type="mitigation",
            summary=f"Fail2ban banned {ip_match.group(1) if ip_match else 'unknown source'}.",
            target="fail2ban",
            technique="T1110.001",
            source=source_name,
            confidence="high",
            severity="medium",
        )]
    return []


def json_object(line: str) -> dict[str, Any] | None:
    try:
        value = json.loads(line)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def first_text(*values: Any) -> str:
    for value in values:
        if value is not None:
            text = str(value).strip()
            if text:
                return text
    return ""


def lower_blob(*values: Any) -> str:
    return " ".join(str(value).lower() for value in values if value is not None)


def severity_from_suricata(value: Any) -> str:
    try:
        severity = int(value)
    except (TypeError, ValueError):
        return "medium"
    if severity <= 1:
        return "high"
    if severity == 2:
        return "medium"
    return "low"


def severity_from_wazuh(value: Any) -> str:
    try:
        level = int(value)
    except (TypeError, ValueError):
        return "medium"
    if level >= 12:
        return "high"
    if level >= 7:
        return "medium"
    return "low"


def scan_like(text: str) -> bool:
    markers = ("scan", "portscan", "sweep", "nmap", "recon", "probe")
    return any(marker in text for marker in markers)


def brute_or_login_like(text: str) -> bool:
    markers = ("brute", "password", "login", "logon", "authentication", "auth failure", "failed")
    return any(marker in text for marker in markers)


def malware_like(text: str) -> bool:
    markers = ("malware", "trojan", "virus", "ransomware", "backdoor", "worm")
    return any(marker in text for marker in markers)


def suspicious_http_path(path: str, status: Any) -> bool:
    path_lower = path.lower()
    markers = (
        "/.env",
        "/.git",
        "/wp-login",
        "/wp-admin",
        "/phpmyadmin",
        "/admin",
        "cmd=",
        "shell",
        "passwd",
        ".sql",
        ".bak",
    )
    if any(marker in path_lower for marker in markers):
        return True
    try:
        status_code = int(status)
    except (TypeError, ValueError):
        return False
    return status_code in {401, 403, 404, 429, 500}


def parse_suricata_eve_line(line: str, source_name: str) -> list[Detection]:
    data = json_object(line)
    if not data:
        return []
    alert = data.get("alert")
    if not isinstance(alert, dict):
        return []

    signature = first_text(alert.get("signature"), "Suricata alert")
    category = first_text(alert.get("category"))
    severity = severity_from_suricata(alert.get("severity"))
    src_ip = first_text(data.get("src_ip"), data.get("srcip"), "unknown")
    dest_ip = first_text(data.get("dest_ip"), data.get("dst_ip"), data.get("destip"), "unknown")
    proto = first_text(data.get("proto"))
    text = lower_blob(signature, category, proto)

    technique = "T1071"
    if scan_like(text):
        technique = "T1046"
    elif brute_or_login_like(text):
        technique = "T1110.001"

    details = f"{src_ip} -> {dest_ip}"
    if proto:
        details = f"{details} {proto}"
    if category:
        details = f"{details}; category={category}"
    return [Detection(
        event_type="detection",
        summary=f"Suricata alert: {signature} ({details}).",
        target=dest_ip,
        technique=technique,
        source=source_name,
        confidence="high",
        severity=severity,
        artifacts=[item for item in (src_ip, dest_ip, proto, category) if item],
    )]


def parse_wazuh_line(line: str, source_name: str) -> list[Detection]:
    data = json_object(line)
    if not data:
        return []
    rule = data.get("rule")
    rule = rule if isinstance(rule, dict) else {}
    agent = data.get("agent")
    agent = agent if isinstance(agent, dict) else {}
    alert_data = data.get("data")
    alert_data = alert_data if isinstance(alert_data, dict) else {}

    description = first_text(rule.get("description"))
    if not description:
        return []
    agent_name = first_text(agent.get("name"), "unknown-agent")
    src_ip = first_text(
        alert_data.get("srcip"),
        alert_data.get("src_ip"),
        data.get("srcip"),
        data.get("src_ip"),
        "unknown",
    )
    text = lower_blob(description, rule.get("groups"), rule.get("mitre"))

    technique = ""
    if brute_or_login_like(text):
        technique = "T1110.001"
    elif malware_like(text):
        technique = "T1204"
    elif scan_like(text):
        technique = "T1046"
    else:
        return []

    return [Detection(
        event_type="detection",
        summary=f"Wazuh alert on {agent_name}: {description} from {src_ip}.",
        target=agent_name,
        technique=technique,
        source=source_name,
        confidence="high",
        severity=severity_from_wazuh(rule.get("level")),
        artifacts=[item for item in (agent_name, src_ip) if item],
    )]


def parse_zeek_conn_line(line: str, source_name: str) -> list[Detection]:
    data = json_object(line)
    if not data:
        return []
    service = first_text(data.get("service"))
    history = first_text(data.get("history"))
    conn_state = first_text(data.get("conn_state"))
    proto = first_text(data.get("proto"))
    src_ip = first_text(data.get("id.orig_h"), data.get("src_ip"), data.get("srcip"), "unknown")
    dest_ip = first_text(data.get("id.resp_h"), data.get("dest_ip"), data.get("dst_ip"), "unknown")
    dest_port = first_text(data.get("id.resp_p"), data.get("dest_port"))
    text = lower_blob(service, history, conn_state, proto, data.get("note"))
    scan_state = conn_state in {"S0", "REJ", "RSTO", "RSTR"} or scan_like(text)
    low_payload = data.get("resp_bytes") in {0, "0"} and data.get("orig_bytes") in {0, "0", None}
    if not (scan_state or low_payload):
        return []
    target = f"{dest_ip}:{dest_port}" if dest_port else dest_ip
    return [Detection(
        event_type="detection",
        summary=f"Zeek conn scan-like connection: {src_ip} -> {target} {proto} state={conn_state or 'unknown'}.",
        target=target,
        technique="T1046",
        source=source_name,
        confidence="medium",
        severity="medium",
        artifacts=[item for item in (src_ip, dest_ip, dest_port, proto, conn_state) if item],
    )]


def parse_zeek_dns_line(line: str, source_name: str) -> list[Detection]:
    data = json_object(line)
    if not data:
        return []
    query = first_text(data.get("query"))
    if not query:
        return []
    src_ip = first_text(data.get("id.orig_h"), data.get("src_ip"), data.get("srcip"), "unknown")
    return [Detection(
        event_type="detection",
        summary=f"Zeek DNS query observed: {query} from {src_ip}.",
        target=query,
        technique="T1071.004",
        source=source_name,
        confidence="medium",
        severity="low",
        artifacts=[item for item in (src_ip, query) if item],
    )]


def parse_zeek_http_line(line: str, source_name: str) -> list[Detection]:
    data = json_object(line)
    if not data:
        return []
    uri = first_text(data.get("uri"))
    status = data.get("status_code")
    if not uri or not suspicious_http_path(uri, status):
        return []
    host = first_text(data.get("host"))
    method = first_text(data.get("method"))
    src_ip = first_text(data.get("id.orig_h"), data.get("src_ip"), data.get("srcip"), "unknown")
    target = f"{host}{uri}" if host else uri
    status_text = first_text(status, "unknown")
    return [Detection(
        event_type="detection",
        summary=f"Zeek HTTP suspicious request: {method or 'HTTP'} {target} from {src_ip} returned {status_text}.",
        target=target,
        technique="T1071.001",
        source=source_name,
        confidence="medium",
        severity="medium",
        artifacts=[item for item in (src_ip, host, uri, method, status_text) if item],
    )]


def parse_zeek_line(line: str, source_name: str) -> list[Detection]:
    data = json_object(line)
    if not data:
        return []
    path = first_text(data.get("_path"), data.get("path"), data.get("log_type")).lower()
    if path == "dns":
        return parse_zeek_dns_line(line, source_name)
    if path == "http":
        return parse_zeek_http_line(line, source_name)
    if path == "conn":
        return parse_zeek_conn_line(line, source_name)
    if data.get("query"):
        return parse_zeek_dns_line(line, source_name)
    if data.get("uri"):
        return parse_zeek_http_line(line, source_name)
    return parse_zeek_conn_line(line, source_name)


def parse_line(source_type: str, line: str, source_name: str) -> list[Detection]:
    if source_type == "auth":
        return parse_auth_line(line, source_name)
    if source_type == "nginx_access":
        return parse_nginx_access_line(line, source_name)
    if source_type == "nginx_error":
        return parse_nginx_error_line(line, source_name)
    if source_type == "postfix":
        return parse_postfix_line(line, source_name)
    if source_type == "dovecot":
        return parse_dovecot_line(line, source_name)
    if source_type == "fail2ban":
        return parse_fail2ban_line(line, source_name)
    if source_type in {"suricata", "suricata_eve"}:
        return parse_suricata_eve_line(line, source_name)
    if source_type == "wazuh":
        return parse_wazuh_line(line, source_name)
    if source_type == "zeek_conn":
        return parse_zeek_conn_line(line, source_name)
    if source_type == "zeek_dns":
        return parse_zeek_dns_line(line, source_name)
    if source_type == "zeek_http":
        return parse_zeek_http_line(line, source_name)
    if source_type == "zeek":
        return parse_zeek_line(line, source_name)
    return []


def checkpoint_key(source_type: str, path: Path) -> str:
    return f"{source_type}:{path.resolve()}"


def load_checkpoint(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {"version": 1, "sources": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"version": 1, "sources": {}}
    if not isinstance(data.get("sources"), dict):
        data["sources"] = {}
    data.setdefault("version", 1)
    return data


def save_checkpoint(path: Path, checkpoint: dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def tail_source_once(source_type: str, path: Path, checkpoint: dict[str, Any]) -> list[Detection]:
    key = checkpoint_key(source_type, path)
    stat = path.stat()
    sources = checkpoint.setdefault("sources", {})
    state = sources.get(key, {})
    stored_offset = state.get("offset", 0) if isinstance(state, dict) else 0
    offset = stored_offset if isinstance(stored_offset, int) and stored_offset <= stat.st_size else 0

    with path.open("rb") as handle:
        handle.seek(offset)
        chunk = handle.read()
        new_offset = handle.tell()

    detections: list[Detection] = []
    if chunk:
        source_name = f"{source_type}:{path}"
        text = chunk.decode("utf-8", errors="replace")
        for line in text.splitlines():
            detections.extend(parse_line(source_type, line, source_name))

    sources[key] = {
        "offset": new_offset,
        "size": stat.st_size,
        "mtime": stat.st_mtime,
        "source_type": source_type,
        "path": str(path),
        "updated_at": now_utc(),
    }
    return detections


def tail_once(
    sources: list[str],
    checkpoint_path: Path,
    output_root: Path | None = None,
    session_id: str | None = None,
    write_ledger: bool = True,
) -> dict[str, Any]:
    checkpoint = load_checkpoint(checkpoint_path)
    detections: list[Detection] = []
    tracked_paths = 0

    for raw_source in sources:
        source_type, pattern = parse_source(raw_source)
        for path in expand_paths(pattern):
            tracked_paths += 1
            detections.extend(tail_source_once(source_type, path, checkpoint))

    save_checkpoint(checkpoint_path, checkpoint)

    events: list[dict[str, Any]] = []
    if write_ledger and detections:
        if output_root is None or session_id is None:
            raise ValueError("output_root and session_id are required when write_ledger is enabled")
        events = write_duel_events(output_root, session_id, detections)

    return {
        "status": "tailed",
        "checkpoint": str(checkpoint_path),
        "tracked_paths": tracked_paths,
        "count": len(detections),
        "detections": [d.to_duel_args() for d in detections],
        "events": events,
    }


def ingest_sources(sources: list[str]) -> list[Detection]:
    detections: list[Detection] = []
    for raw_source in sources:
        source_type, pattern = parse_source(raw_source)
        paths = expand_paths(pattern)
        for path in paths:
            source_name = f"{source_type}:{path}"
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for line in handle:
                    detections.extend(parse_line(source_type, line.rstrip("\n"), source_name))
    return detections


def write_duel_events(output_root: Path, session_id: str, detections: list[Detection]) -> list[dict[str, Any]]:
    duel = load_duel_module()
    written: list[dict[str, Any]] = []
    duel.init_session(session_id, "blue", output_root)
    for detection in detections:
        written.append(duel.record_event(
            output_root=output_root,
            session_id=session_id,
            role="blue",
            event_type=detection.event_type,
            summary=detection.summary,
            target=detection.target,
            technique=detection.technique,
            source=detection.source,
            confidence=detection.confidence,
            severity=detection.severity,
            artifacts=detection.artifacts or [],
        )["event"])
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest defensive telemetry into SPECTRA Duel Mode Blue ledger.")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("ingest", help="Parse log sources and append Blue detections")
    ingest.add_argument("--session", required=True)
    ingest.add_argument("--output-root", type=Path, required=True)
    ingest.add_argument("--source", action="append", required=True, help="type=path or type=glob")
    ingest.add_argument("--dry-run", action="store_true")
    ingest.add_argument("--format", choices=("json", "jsonl"), default="json")

    tail = sub.add_parser("tail", help="Read new log bytes since checkpoint and append Blue detections")
    tail.add_argument("--session", required=True)
    tail.add_argument("--output-root", type=Path, required=True)
    tail.add_argument("--source", action="append", required=True, help="type=path or type=glob")
    tail.add_argument("--checkpoint", type=Path, required=True)
    tail.add_argument("--once", action="store_true", help="Run one bounded tail pass")
    tail.add_argument("--dry-run", action="store_true")
    tail.add_argument("--format", choices=("json", "jsonl"), default="json")

    args = parser.parse_args(argv)
    if args.command == "ingest":
        try:
            detections = ingest_sources(args.source)
            if args.dry_run:
                items = [d.to_duel_args() for d in detections]
                if args.format == "jsonl":
                    for item in items:
                        print(json.dumps(item, sort_keys=True))
                else:
                    print(json.dumps({"detections": items, "count": len(items)}, indent=2))
                return 0
            events = write_duel_events(args.output_root, args.session, detections)
            print(json.dumps({
                "status": "ingested",
                "session_id": args.session,
                "count": len(events),
                "events": events,
            }, indent=2))
            return 0
        except ValueError as exc:
            print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
            return 1
    if args.command == "tail":
        if not args.once:
            print(json.dumps({"error": "tail currently requires --once for bounded deterministic execution"}, indent=2), file=sys.stderr)
            return 1
        try:
            result = tail_once(
                sources=args.source,
                checkpoint_path=args.checkpoint,
                output_root=args.output_root,
                session_id=args.session,
                write_ledger=not args.dry_run,
            )
            if args.format == "jsonl":
                for item in result["detections"] if args.dry_run else result["events"]:
                    print(json.dumps(item, sort_keys=True))
            else:
                print(json.dumps(result, indent=2))
            return 0
        except ValueError as exc:
            print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
            return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
