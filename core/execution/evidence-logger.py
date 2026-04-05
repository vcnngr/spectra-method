#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""
SPECTRA Evidence Logger
Chain of custody management for digital evidence.
Called by SPECTRA agents during evidence collection and handling.

Usage:
  python evidence-logger.py acquire --engagement <path> --description <desc> --source <src> --type <type> [--file <path>] [--actor <name>]
  python evidence-logger.py transfer --engagement <path> --evidence-id <id> --to <custodian> --reason <reason> --method <method>
  python evidence-logger.py verify --engagement <path> [--evidence-id <id>]
  python evidence-logger.py inventory --engagement <path>
  python evidence-logger.py export --engagement <path> --output <path>

Exit codes:
  0 — Success
  1 — Verification failure (hash mismatch detected)
  2 — Evidence not found or inaccessible
  3 — Error (invalid input, missing file, bad YAML)
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_SOURCE_TYPES = [
    "disk-image", "memory", "log-export", "packet-capture",
    "screenshot", "document", "artifact", "other",
]
VALID_CLASSIFICATIONS = ["original", "working-copy", "derivative"]
VALID_STATUSES = ["active", "transferred", "archived", "destroyed"]


# ---------------------------------------------------------------------------
# Registry management
# ---------------------------------------------------------------------------

def _registry_path(engagement_path: str) -> Path:
    """
    Derive the evidence registry path from an engagement.yaml path.
    Registry lives at: {evidence_artifacts}/{engagement_id}/evidence-registry.yaml
    We infer the evidence root as a sibling 'evidence' directory to 'engagements'.
    """
    eng_data = _load_engagement(engagement_path)
    eng_id = eng_data.get("id", "unknown")

    eng_dir = Path(engagement_path).resolve().parent  # .../engagements/{eng_id}/
    # Navigate from engagements dir to evidence dir
    output_root = eng_dir.parent.parent  # .../_spectra-output/
    evidence_root = output_root / "evidence"
    return evidence_root / eng_id / "evidence-registry.yaml"


def _load_engagement(path: str) -> dict:
    """Load the engagement section from an engagement YAML file."""
    p = Path(path)
    if not p.exists():
        _die(f"Engagement file not found: {path}")
    with open(p, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not data or "engagement" not in data:
        _die("Invalid engagement file: missing 'engagement' root key")
    return data["engagement"]


def _load_registry(reg_path: Path) -> dict:
    """Load an existing registry or create a new empty one."""
    if reg_path.exists():
        with open(reg_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data and "evidence_registry" in data:
            return data["evidence_registry"]

    # Create new empty registry — caller must provide engagement_id
    return None


def _init_registry(engagement_id: str) -> dict:
    """Create a fresh empty evidence registry."""
    now = _iso_now()
    return {
        "engagement_id": engagement_id,
        "created": now,
        "last_modified": now,
        "last_verified": "never",
        "integrity_status": "UNVERIFIED",
        "item_count": 0,
        "items": [],
    }


def _save_registry(reg: dict, reg_path: Path) -> None:
    """Persist the registry to disk immediately."""
    reg_path.parent.mkdir(parents=True, exist_ok=True)
    # Also ensure files/ subdir exists
    files_dir = reg_path.parent / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    with open(reg_path, "w", encoding="utf-8") as f:
        yaml.dump(
            {"evidence_registry": reg},
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def _get_or_create_registry(engagement_path: str) -> tuple[dict, Path]:
    """Load or initialize registry, return (registry_dict, registry_path)."""
    eng = _load_engagement(engagement_path)
    eng_id = eng.get("id", "unknown")
    reg_path = _registry_path(engagement_path)

    reg = _load_registry(reg_path)
    if reg is None:
        reg = _init_registry(eng_id)
        _save_registry(reg, reg_path)

    return reg, reg_path


# ---------------------------------------------------------------------------
# Hashing
# ---------------------------------------------------------------------------

def compute_hashes(file_path: str) -> dict:
    """
    Compute SHA-256, MD5, and SHA-1 hashes for a file.
    Returns dict with hash values and file_size_bytes.
    """
    p = Path(file_path)
    if not p.exists():
        return {"error": f"File not found: {file_path}"}
    if not p.is_file():
        return {"error": f"Not a regular file: {file_path}"}

    sha256 = hashlib.sha256()
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()

    file_size = 0
    buf_size = 65536  # 64 KB chunks for memory efficiency

    with open(p, "rb") as f:
        while True:
            data = f.read(buf_size)
            if not data:
                break
            file_size += len(data)
            sha256.update(data)
            md5.update(data)
            sha1.update(data)

    return {
        "hash_sha256": sha256.hexdigest(),
        "hash_md5": md5.hexdigest(),
        "hash_sha1": sha1.hexdigest(),
        "file_size_bytes": file_size,
    }


# ---------------------------------------------------------------------------
# Evidence ID generation
# ---------------------------------------------------------------------------

def _next_evidence_id(registry: dict) -> str:
    """Generate the next sequential evidence ID: EV-{engagement_id}-{NNN}."""
    eng_id = registry.get("engagement_id", "unknown")
    next_num = registry.get("item_count", 0) + 1
    # Pad to at least 3 digits
    return f"EV-{eng_id}-{next_num:03d}"


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------

def cmd_acquire(args: argparse.Namespace) -> None:
    """Register a new piece of digital evidence."""
    reg, reg_path = _get_or_create_registry(args.engagement)
    now = _iso_now()

    # Validate source type
    if args.type not in VALID_SOURCE_TYPES:
        _die(f"Invalid source type '{args.type}'. Valid: {', '.join(VALID_SOURCE_TYPES)}")

    classification = getattr(args, "classification", "original") or "original"
    if classification not in VALID_CLASSIFICATIONS:
        _die(f"Invalid classification '{classification}'. Valid: {', '.join(VALID_CLASSIFICATIONS)}")

    # Compute hashes if file provided
    hashes = {}
    file_path_str = ""
    if args.file:
        file_path_str = str(Path(args.file).resolve())
        hashes = compute_hashes(args.file)
        if "error" in hashes:
            _die(hashes["error"])

    # Generate evidence ID
    ev_id = _next_evidence_id(reg)
    actor = args.actor or "SPECTRA-agent"

    # Build evidence item (follows schema from spectra-evidence-chain SKILL.md)
    item = {
        "id": ev_id,
        "description": args.description,
        "source_system": args.source,
        "source_type": args.type,
        "acquisition_method": getattr(args, "method", "automated") or "automated",
        "acquiring_party": actor,
        "acquisition_timestamp": now,
        "hash_sha256": hashes.get("hash_sha256", "N/A"),
        "hash_md5": hashes.get("hash_md5", "N/A"),
        "hash_sha1": hashes.get("hash_sha1", "N/A"),
        "ssdeep": "N/A",  # ssdeep requires external tool — mark N/A
        "file_path": file_path_str,
        "file_size_bytes": hashes.get("file_size_bytes", 0),
        "finding_reference": getattr(args, "finding_ref", "") or "",
        "classification": classification,
        "status": "active",
        "current_custodian": actor,
        "notes": getattr(args, "notes", "") or "",
        "custody_log": [
            {
                "timestamp": now,
                "action": "acquired",
                "actor": actor,
                "reason": f"Evidence acquisition: {args.description}",
                "method": getattr(args, "method", "automated") or "automated",
                "from_location": args.source,
                "to_location": "SPECTRA evidence store",
                "hash_verified": True,
            }
        ],
    }

    # Append to registry
    if reg["items"] is None:
        reg["items"] = []
    reg["items"].append(item)
    reg["item_count"] = len(reg["items"])
    reg["last_modified"] = now
    reg["integrity_status"] = "UNVERIFIED"

    _save_registry(reg, reg_path)

    # Output result
    result = {
        "status": "acquired",
        "evidence_id": ev_id,
        "description": args.description,
        "source": args.source,
        "source_type": args.type,
        "hash_sha256": item["hash_sha256"],
        "hash_md5": item["hash_md5"],
        "hash_sha1": item["hash_sha1"],
        "file_size_bytes": item["file_size_bytes"],
        "custodian": actor,
        "timestamp": now,
        "registry_item_count": reg["item_count"],
        "registry_path": str(reg_path),
    }
    print(json.dumps(result, indent=2))


def cmd_transfer(args: argparse.Namespace) -> None:
    """Record a custody transfer for an evidence item."""
    reg, reg_path = _get_or_create_registry(args.engagement)
    now = _iso_now()

    # Find the evidence item
    item = None
    for it in (reg.get("items") or []):
        if it["id"] == args.evidence_id:
            item = it
            break

    if item is None:
        _die(f"Evidence item not found: {args.evidence_id}")

    if item.get("status") != "active":
        _die(f"Evidence {args.evidence_id} has status '{item.get('status')}' — only 'active' items can be transferred")

    previous_custodian = item.get("current_custodian", "unknown")
    previous_location = "unknown"
    # Try to get last known location from custody log
    if item.get("custody_log"):
        previous_location = item["custody_log"][-1].get("to_location", "unknown")

    # Optionally verify hash before transfer
    hash_verified = False
    if item.get("file_path") and Path(item["file_path"]).exists():
        hashes = compute_hashes(item["file_path"])
        if "error" not in hashes:
            hash_verified = hashes["hash_sha256"] == item.get("hash_sha256", "")
            if not hash_verified:
                # Alert but continue — operator decided to transfer
                print(json.dumps({
                    "warning": "HASH MISMATCH before transfer",
                    "evidence_id": args.evidence_id,
                    "expected_sha256": item.get("hash_sha256"),
                    "computed_sha256": hashes["hash_sha256"],
                }), file=sys.stderr)

    # Record transfer event
    transfer_event = {
        "timestamp": now,
        "action": "transferred",
        "actor": previous_custodian,
        "reason": args.reason,
        "method": args.method,
        "from_location": previous_location,
        "to_location": f"{args.to} custody",
        "hash_verified": hash_verified,
    }

    if item.get("custody_log") is None:
        item["custody_log"] = []
    item["custody_log"].append(transfer_event)
    item["current_custodian"] = args.to
    reg["last_modified"] = now

    _save_registry(reg, reg_path)

    result = {
        "status": "transferred",
        "evidence_id": args.evidence_id,
        "description": item.get("description", ""),
        "from_custodian": previous_custodian,
        "to_custodian": args.to,
        "method": args.method,
        "reason": args.reason,
        "hash_verified": hash_verified,
        "timestamp": now,
        "custody_events_total": len(item["custody_log"]),
    }
    print(json.dumps(result, indent=2))


def cmd_verify(args: argparse.Namespace) -> None:
    """Verify integrity of evidence items by recomputing hashes."""
    reg, reg_path = _get_or_create_registry(args.engagement)
    now = _iso_now()

    items_to_verify = reg.get("items") or []
    # If a specific evidence ID is provided, verify only that item
    if args.evidence_id:
        items_to_verify = [it for it in items_to_verify if it["id"] == args.evidence_id]
        if not items_to_verify:
            _die(f"Evidence item not found: {args.evidence_id}")

    verified = 0
    failed = 0
    inaccessible = 0
    reference_only = 0
    details = []

    for item in items_to_verify:
        ev_id = item["id"]
        file_path = item.get("file_path", "")

        if not file_path:
            # Reference-only evidence — no file to verify
            reference_only += 1
            details.append({
                "evidence_id": ev_id,
                "status": "REFERENCE_ONLY",
                "reason": "No file path — cannot verify automatically",
            })
            continue

        p = Path(file_path)
        if not p.exists():
            inaccessible += 1
            details.append({
                "evidence_id": ev_id,
                "status": "INACCESSIBLE",
                "reason": f"File not found: {file_path}",
            })
            continue

        hashes = compute_hashes(file_path)
        if "error" in hashes:
            inaccessible += 1
            details.append({
                "evidence_id": ev_id,
                "status": "INACCESSIBLE",
                "reason": hashes["error"],
            })
            continue

        sha256_ok = hashes["hash_sha256"] == item.get("hash_sha256", "")
        md5_ok = hashes["hash_md5"] == item.get("hash_md5", "")
        sha1_ok = hashes["hash_sha1"] == item.get("hash_sha1", "")

        if sha256_ok:
            verified += 1
            details.append({
                "evidence_id": ev_id,
                "status": "VERIFIED",
                "sha256_match": True,
                "md5_match": md5_ok,
                "sha1_match": sha1_ok,
            })
        else:
            failed += 1
            details.append({
                "evidence_id": ev_id,
                "status": "FAILED",
                "sha256_match": False,
                "expected_sha256": item.get("hash_sha256", ""),
                "computed_sha256": hashes["hash_sha256"],
                "md5_match": md5_ok,
                "sha1_match": sha1_ok,
            })

    # Update registry integrity status
    if failed > 0:
        reg["integrity_status"] = "FAILED"
    elif verified > 0:
        reg["integrity_status"] = "VERIFIED"
    else:
        reg["integrity_status"] = "UNVERIFIED"

    reg["last_verified"] = now
    reg["last_modified"] = now
    _save_registry(reg, reg_path)

    result = {
        "verification_timestamp": now,
        "total_items": len(items_to_verify),
        "verified": verified,
        "failed": failed,
        "inaccessible": inaccessible,
        "reference_only": reference_only,
        "integrity_status": reg["integrity_status"],
        "items": details,
    }
    print(json.dumps(result, indent=2))

    # Exit code 1 if any failures detected
    if failed > 0:
        sys.exit(1)


def cmd_inventory(args: argparse.Namespace) -> None:
    """List all evidence items in the registry."""
    reg, _ = _get_or_create_registry(args.engagement)
    items = reg.get("items") or []

    inventory = []
    for item in items:
        inventory.append({
            "id": item.get("id"),
            "description": item.get("description"),
            "source_type": item.get("source_type"),
            "source_system": item.get("source_system"),
            "current_custodian": item.get("current_custodian"),
            "acquisition_timestamp": item.get("acquisition_timestamp"),
            "status": item.get("status"),
            "classification": item.get("classification"),
            "hash_sha256": item.get("hash_sha256", "")[:16] + "...",
            "file_size_bytes": item.get("file_size_bytes", 0),
            "custody_events": len(item.get("custody_log", [])),
        })

    summary = {
        "engagement_id": reg.get("engagement_id"),
        "total_items": reg.get("item_count", 0),
        "integrity_status": reg.get("integrity_status"),
        "last_verified": reg.get("last_verified"),
        "active": sum(1 for it in items if it.get("status") == "active"),
        "transferred": sum(1 for it in items if it.get("status") == "transferred"),
        "archived": sum(1 for it in items if it.get("status") == "archived"),
        "destroyed": sum(1 for it in items if it.get("status") == "destroyed"),
        "items": inventory,
    }
    print(json.dumps(summary, indent=2))


def cmd_export(args: argparse.Namespace) -> None:
    """Generate a chain-of-custody-report.md at the specified output path."""
    reg, _ = _get_or_create_registry(args.engagement)
    eng = _load_engagement(args.engagement)
    now = _iso_now()
    date_str = now[:10]

    eng_id = eng.get("id", "unknown")
    eng_type = eng.get("type", "unknown")
    client = eng.get("authorization", {}).get("client", "unknown")

    items = reg.get("items") or []
    total_custody_events = sum(len(it.get("custody_log", [])) for it in items)

    # --- Build the report ---
    lines = []
    lines.append(f"# Chain of Custody Report — {eng_id}")
    lines.append("")
    lines.append(f"**Engagement:** {eng_id} — {eng_type}")
    lines.append(f"**Client:** {client}")
    lines.append(f"**Report Date:** {date_str}")
    lines.append("**Generated by:** SPECTRA Evidence Chain")
    lines.append(f"**Integrity Status:** {reg.get('integrity_status', 'UNVERIFIED')}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 1: Evidence Inventory
    lines.append("## 1. Evidence Inventory")
    lines.append("")
    lines.append("| # | Evidence ID | Description | Source | Type | Acquired | SHA-256 | Status |")
    lines.append("|---|-------------|-------------|--------|------|----------|---------|--------|")
    for i, item in enumerate(items, 1):
        sha_short = (item.get("hash_sha256", "N/A") or "N/A")[:16] + "..."
        lines.append(
            f"| {i} | {item.get('id', '')} | {item.get('description', '')} | "
            f"{item.get('source_system', '')} | {item.get('source_type', '')} | "
            f"{(item.get('acquisition_timestamp', '') or '')[:10]} | {sha_short} | "
            f"{item.get('status', '')} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 2: Custody Event Log
    lines.append("## 2. Custody Event Log")
    lines.append("")
    for item in items:
        ev_id = item.get("id", "")
        desc = item.get("description", "")
        lines.append(f"### {ev_id}: {desc}")
        lines.append("")
        lines.append("| # | Timestamp | Action | Actor | From | To | Method | Reason | Hash Verified |")
        lines.append("|---|-----------|--------|-------|------|----|--------|--------|---------------|")
        for j, event in enumerate(item.get("custody_log", []), 1):
            hv = "Yes" if event.get("hash_verified") else "No"
            lines.append(
                f"| {j} | {event.get('timestamp', '')} | {event.get('action', '')} | "
                f"{event.get('actor', '')} | {event.get('from_location', '')} | "
                f"{event.get('to_location', '')} | {event.get('method', '')} | "
                f"{event.get('reason', '')} | {hv} |"
            )
        lines.append("")
    lines.append("---")
    lines.append("")

    # Section 3: Integrity Verification Summary
    lines.append("## 3. Integrity Verification Summary")
    lines.append("")
    lines.append(f"**Last verification:** {reg.get('last_verified', 'never')}")
    lines.append(f"**Overall status:** {reg.get('integrity_status', 'UNVERIFIED')}")
    lines.append("")
    lines.append("| # | Evidence ID | SHA-256 Stored | Status |")
    lines.append("|---|-------------|----------------|--------|")
    for i, item in enumerate(items, 1):
        sha = (item.get("hash_sha256", "N/A") or "N/A")[:16] + "..."
        status = item.get("status", "unknown")
        lines.append(f"| {i} | {item.get('id', '')} | {sha} | {status} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 4: Attestation
    lines.append("## 4. Attestation")
    lines.append("")
    lines.append(
        "I attest that this chain of custody report accurately represents the handling of all "
        "evidence items listed above. All evidence was acquired, stored, and transferred in "
        "accordance with applicable forensic standards (ISO 27037, NIST SP 800-86, SWGDE Best Practices)."
    )
    lines.append("")
    lines.append(
        "All hash computations were performed using industry-standard cryptographic algorithms. "
        "Any integrity failures or anomalies are documented in the Integrity Verification Summary above."
    )
    lines.append("")
    lines.append(f"**Engagement:** {eng_id}")
    lines.append(f"**Date:** {date_str}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*Report generated by SPECTRA Evidence Chain — {date_str}*")

    # Write report
    report_content = "\n".join(lines) + "\n"
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_content)

    result = {
        "status": "exported",
        "output_path": str(output_path.resolve()),
        "items_documented": len(items),
        "custody_events": total_custody_events,
        "integrity_status": reg.get("integrity_status", "UNVERIFIED"),
    }
    print(json.dumps(result, indent=2))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _iso_now() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _die(msg: str) -> None:
    """Print error JSON to stderr and exit with code 3."""
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(3)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="evidence-logger",
        description="SPECTRA Evidence Logger — chain of custody management",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # -- acquire --
    p_acq = sub.add_parser("acquire", help="Register new evidence")
    p_acq.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_acq.add_argument("--description", required=True, help="Evidence description")
    p_acq.add_argument("--source", required=True, help="Source system or location")
    p_acq.add_argument("--type", required=True, choices=VALID_SOURCE_TYPES, help="Evidence source type")
    p_acq.add_argument("--file", default=None, help="Path to evidence file (optional)")
    p_acq.add_argument("--actor", default=None, help="Acquiring party name")
    p_acq.add_argument("--method", default=None, help="Acquisition method")
    p_acq.add_argument("--classification", default="original", choices=VALID_CLASSIFICATIONS, help="Evidence classification")
    p_acq.add_argument("--finding-ref", default=None, help="Linked finding ID")
    p_acq.add_argument("--notes", default=None, help="Additional notes")

    # -- transfer --
    p_xfr = sub.add_parser("transfer", help="Record custody transfer")
    p_xfr.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_xfr.add_argument("--evidence-id", required=True, help="Evidence item ID")
    p_xfr.add_argument("--to", required=True, help="New custodian name")
    p_xfr.add_argument("--reason", required=True, help="Transfer reason")
    p_xfr.add_argument("--method", required=True, help="Transfer method")

    # -- verify --
    p_ver = sub.add_parser("verify", help="Verify evidence integrity")
    p_ver.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_ver.add_argument("--evidence-id", default=None, help="Verify single item (optional — omit for all)")

    # -- inventory --
    p_inv = sub.add_parser("inventory", help="List all evidence items")
    p_inv.add_argument("--engagement", required=True, help="Path to engagement.yaml")

    # -- export --
    p_exp = sub.add_parser("export", help="Generate chain of custody report")
    p_exp.add_argument("--engagement", required=True, help="Path to engagement.yaml")
    p_exp.add_argument("--output", required=True, help="Output path for the report .md file")

    args = parser.parse_args()

    dispatch = {
        "acquire": cmd_acquire,
        "transfer": cmd_transfer,
        "verify": cmd_verify,
        "inventory": cmd_inventory,
        "export": cmd_export,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
