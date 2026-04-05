#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
SPECTRA Project Validator
Comprehensive structural, content, and consistency validation.

Usage:
  python validate-spectra.py --path <path_to_spectra> [--strict] [--json] [--fix-suggestions]
  python validate-spectra.py --path <path_to_spectra> --module rtk
  python validate-spectra.py --path <path_to_spectra> --summary
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import py_compile
import re
import sys
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: pyyaml required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

VERSION = "0.1.0"
MODULES = ("core", "rtk", "soc", "irt", "grc")

AGENT_CSV_COLUMNS = [
    "name", "displayName", "title", "icon", "capabilities", "role",
    "identity", "communicationStyle", "principles", "module", "path", "canonicalId",
]
SKILL_CSV_COLUMNS = [
    "canonicalId", "name", "description", "module", "path", "install_to_spectra",
]
CORE_CONFIG_REQUIRED = [
    "user_name", "communication_language", "document_output_language", "output_folder",
]

# Sections expected in agent SKILL.md files
AGENT_REQUIRED_SECTIONS = ["Overview", "On Activation"]
AGENT_IDENTITY_SECTIONS = ["Identity", "Communication Style", "Principles"]

# Path anti-patterns
ABSOLUTE_PATH_RE = re.compile(r'(?:^|[\s"`\'(])(/(?:Users|home|opt|var|tmp|etc|usr)/\S+)', re.MULTILINE)
PARENT_DIR_RE = re.compile(r'(?:^|[\s"`\'(])(\.\./\S+)', re.MULTILINE)


# ---------------------------------------------------------------------------
# Finding collector
# ---------------------------------------------------------------------------
class Findings:
    """Collect validation findings with severity and category."""

    def __init__(self):
        self._items: list[dict] = []
        self._passed = 0

    def add(self, code: str, severity: str, category: str, file: str,
            message: str, fix: str = "", line: int = 0):
        self._items.append({
            "code": code, "severity": severity, "category": category,
            "file": file, "message": message, "fix": fix, "line": line,
        })

    def passed(self, count: int = 1):
        self._passed += count

    @property
    def items(self) -> list[dict]:
        return self._items

    @property
    def total_checks(self) -> int:
        return self._passed + len(self._items)

    def summary(self) -> dict:
        counts = {"critical": 0, "warning": 0, "info": 0}
        for f in self._items:
            counts[f["severity"]] = counts.get(f["severity"], 0) + 1
        return {
            "total": self.total_checks,
            "passed": self._passed,
            "critical": counts["critical"],
            "warnings": counts["warning"],
            "info": counts["info"],
        }


# ---------------------------------------------------------------------------
# Tier 1 — Critical Structural Checks
# ---------------------------------------------------------------------------
def check_file_existence_agents(spectra: Path, agent_rows: list[dict], findings: Findings):
    """Check SKILL.md and bmad-skill-manifest.yaml for every agent."""
    for row in agent_rows:
        p = row.get("path", "").strip()
        if not p:
            continue
        agent_dir = spectra.parent / p
        skill_path = agent_dir / "SKILL.md"
        manifest_path = agent_dir / "bmad-skill-manifest.yaml"
        rel = p

        if skill_path.is_file():
            findings.passed()
        else:
            findings.add("FILE-001", "critical", "file_existence", rel,
                         f"Missing SKILL.md in agent directory",
                         f"Create SKILL.md at {rel}/SKILL.md")

        if manifest_path.is_file():
            findings.passed()
        else:
            findings.add("FILE-002", "critical", "file_existence", rel,
                         f"Missing bmad-skill-manifest.yaml in agent directory",
                         f"Create bmad-skill-manifest.yaml at {rel}/bmad-skill-manifest.yaml")


def check_file_existence_skills(spectra: Path, skill_rows: list[dict], findings: Findings):
    """Check SKILL.md for every skill-manifest entry."""
    for row in skill_rows:
        p = row.get("path", "").strip()
        if not p:
            continue
        skill_file = spectra.parent / p
        rel = p
        if skill_file.is_file():
            findings.passed()
        else:
            findings.add("FILE-003", "critical", "file_existence", rel,
                         f"Skill file does not exist at declared path",
                         f"Create file at {rel}")


def check_file_existence_workflows(spectra: Path, skill_rows: list[dict], findings: Findings):
    """Check workflow.md and steps-c/ for workflow entries."""
    for row in skill_rows:
        p = row.get("path", "").strip()
        cid = row.get("canonicalId", "")
        if not p:
            continue
        skill_dir = (spectra.parent / p).parent
        # Detect workflow: directory name does NOT contain 'agent' and is under workflows/
        if "/workflows/" not in p and "/spectra-agent-" not in p:
            # Core skills that are workflows have workflow.md
            wf = skill_dir / "workflow.md"
            if wf.is_file():
                findings.passed()
                _check_steps_dir(skill_dir, cid, findings)
            continue
        if "/workflows/" in p:
            wf = skill_dir / "workflow.md"
            if wf.is_file():
                findings.passed()
            else:
                findings.add("FILE-004", "critical", "file_existence",
                             str(skill_dir.relative_to(spectra.parent)),
                             f"Missing workflow.md for workflow {cid}",
                             f"Create workflow.md in {skill_dir.name}/")
            _check_steps_dir(skill_dir, cid, findings)


def _check_steps_dir(skill_dir: Path, cid: str, findings: Findings):
    """Validate steps-c/ directory and step numbering."""
    steps_dir = skill_dir / "steps-c"
    rel = str(skill_dir.name)
    if not steps_dir.is_dir():
        # Some core skills use 'steps' instead of 'steps-c'
        alt = skill_dir / "steps"
        if alt.is_dir():
            steps_dir = alt
        else:
            findings.add("FILE-005", "critical", "file_existence", rel,
                         f"Missing steps directory for workflow {cid}",
                         f"Create steps-c/ directory in {rel}/")
            return

    findings.passed()
    step_files = sorted(f for f in steps_dir.iterdir() if f.is_file() and f.suffix == ".md")
    if not step_files:
        findings.add("FILE-006", "critical", "file_existence", rel,
                     f"Steps directory is empty for workflow {cid}",
                     "Add step files (step-01-*.md, step-02-*.md, ...)")
        return

    findings.passed()
    # Check sequential numbering
    nums = []
    has_resume = False
    for sf in step_files:
        m = re.match(r'^step-(\d+)([a-z]?)-', sf.name)
        if m:
            n = int(m.group(1))
            suffix = m.group(2)
            if suffix == "b" and n == 1:
                has_resume = True
            elif not suffix:
                nums.append(n)

    if nums:
        nums.sort()
        expected = list(range(nums[0], nums[-1] + 1))
        gaps = set(expected) - set(nums)
        if gaps:
            findings.add("FILE-007", "warning", "file_existence", rel,
                         f"Step numbering gaps in {cid}: missing steps {sorted(gaps)}",
                         "Fill in missing step numbers for sequential flow")
        else:
            findings.passed()

    if has_resume:
        findings.passed()
    else:
        findings.add("FILE-008", "warning", "file_existence", rel,
                     f"No resume handler (step-01b-continue.md) for workflow {cid}",
                     "Create step-01b-continue.md for workflow resumption")


def check_manifest_integrity(spectra: Path, findings: Findings):
    """Validate CSV column counts, duplicates, and manifest.yaml structure."""
    agent_csv = spectra / "_config" / "agent-manifest.csv"
    skill_csv = spectra / "_config" / "skill-manifest.csv"
    manifest_yaml = spectra / "_config" / "manifest.yaml"
    agent_rows, skill_rows = [], []

    # --- agent-manifest.csv ---
    if agent_csv.is_file():
        text = agent_csv.read_text(encoding="utf-8")
        reader = csv.DictReader(StringIO(text))
        header = reader.fieldnames or []
        if header == AGENT_CSV_COLUMNS:
            findings.passed()
        else:
            missing = set(AGENT_CSV_COLUMNS) - set(header)
            extra = set(header) - set(AGENT_CSV_COLUMNS)
            detail = []
            if missing:
                detail.append(f"missing: {', '.join(sorted(missing))}")
            if extra:
                detail.append(f"extra: {', '.join(sorted(extra))}")
            findings.add("MANIFEST-001", "critical", "manifest_integrity",
                         "_spectra/_config/agent-manifest.csv",
                         f"Column mismatch — expected {len(AGENT_CSV_COLUMNS)}, got {len(header)}. {'; '.join(detail)}")

        agent_rows = list(reader)
        # Duplicate check on name (canonicalId may be empty for agents)
        names = [r.get("name", "") for r in agent_rows]
        dupes = {n for n in names if names.count(n) > 1 and n}
        if dupes:
            findings.add("MANIFEST-002", "critical", "manifest_integrity",
                         "_spectra/_config/agent-manifest.csv",
                         f"Duplicate agent names: {', '.join(sorted(dupes))}")
        else:
            findings.passed()
    else:
        findings.add("MANIFEST-003", "critical", "manifest_integrity",
                     "_spectra/_config/agent-manifest.csv", "File does not exist")

    # --- skill-manifest.csv ---
    if skill_csv.is_file():
        text = skill_csv.read_text(encoding="utf-8")
        reader = csv.DictReader(StringIO(text))
        header = reader.fieldnames or []
        if header == SKILL_CSV_COLUMNS:
            findings.passed()
        else:
            missing = set(SKILL_CSV_COLUMNS) - set(header)
            extra = set(header) - set(SKILL_CSV_COLUMNS)
            detail = []
            if missing:
                detail.append(f"missing: {', '.join(sorted(missing))}")
            if extra:
                detail.append(f"extra: {', '.join(sorted(extra))}")
            findings.add("MANIFEST-004", "critical", "manifest_integrity",
                         "_spectra/_config/skill-manifest.csv",
                         f"Column mismatch — expected {len(SKILL_CSV_COLUMNS)}, got {len(header)}. {'; '.join(detail)}")

        skill_rows = list(reader)
        cids = [r.get("canonicalId", "") for r in skill_rows]
        dupes = {c for c in cids if cids.count(c) > 1 and c}
        if dupes:
            findings.add("MANIFEST-005", "critical", "manifest_integrity",
                         "_spectra/_config/skill-manifest.csv",
                         f"Duplicate canonicalIds: {', '.join(sorted(dupes))}")
        else:
            findings.passed()
    else:
        findings.add("MANIFEST-006", "critical", "manifest_integrity",
                     "_spectra/_config/skill-manifest.csv", "File does not exist")

    # --- manifest.yaml ---
    if manifest_yaml.is_file():
        try:
            data = yaml.safe_load(manifest_yaml.read_text(encoding="utf-8"))
            for section in ("installation", "modules", "ides"):
                if section in data:
                    findings.passed()
                else:
                    findings.add("MANIFEST-007", "critical", "manifest_integrity",
                                 "_spectra/_config/manifest.yaml",
                                 f"Missing required section: {section}")
        except yaml.YAMLError as e:
            findings.add("MANIFEST-008", "critical", "manifest_integrity",
                         "_spectra/_config/manifest.yaml", f"Invalid YAML: {e}")
    else:
        findings.add("MANIFEST-009", "critical", "manifest_integrity",
                     "_spectra/_config/manifest.yaml", "File does not exist")

    return agent_rows, skill_rows


def check_config_validation(spectra: Path, findings: Findings, module_filter: str | None):
    """Validate core and module config.yaml files."""
    core_cfg = spectra / "core" / "config.yaml"
    if core_cfg.is_file():
        try:
            data = yaml.safe_load(core_cfg.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                data = {}
            for var in CORE_CONFIG_REQUIRED:
                if data.get(var):
                    findings.passed()
                else:
                    findings.add("CONFIG-001", "critical", "config_validation",
                                 "_spectra/core/config.yaml",
                                 f"Missing required core config variable: {var}")
        except yaml.YAMLError as e:
            findings.add("CONFIG-002", "critical", "config_validation",
                         "_spectra/core/config.yaml", f"Invalid YAML: {e}")
    else:
        findings.add("CONFIG-003", "critical", "config_validation",
                     "_spectra/core/config.yaml", "Core config.yaml does not exist")

    for mod in ("rtk", "soc", "irt", "grc"):
        if module_filter and mod != module_filter:
            continue
        cfg = spectra / mod / "config.yaml"
        if cfg.is_file():
            try:
                yaml.safe_load(cfg.read_text(encoding="utf-8"))
                findings.passed()
            except yaml.YAMLError as e:
                findings.add("CONFIG-004", "critical", "config_validation",
                             f"_spectra/{mod}/config.yaml", f"Invalid YAML: {e}")
        else:
            findings.add("CONFIG-005", "critical", "config_validation",
                         f"_spectra/{mod}/config.yaml", f"Module config.yaml missing for {mod}")


# ---------------------------------------------------------------------------
# Tier 2 — Content Quality Checks
# ---------------------------------------------------------------------------
def check_skill_frontmatter(spectra: Path, skill_rows: list[dict], findings: Findings,
                            module_filter: str | None):
    """Validate SKILL.md frontmatter for all skills."""
    for row in skill_rows:
        p = row.get("path", "").strip()
        mod = row.get("module", "").strip()
        if not p or (module_filter and mod != module_filter):
            continue
        skill_file = spectra.parent / p
        if not skill_file.is_file():
            continue

        content = skill_file.read_text(encoding="utf-8")
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match:
            findings.add("CONTENT-001", "warning", "content_quality", p,
                         "SKILL.md missing YAML frontmatter (--- delimiters)")
            continue
        findings.passed()

        try:
            fm = yaml.safe_load(fm_match.group(1))
            if not isinstance(fm, dict):
                fm = {}
        except yaml.YAMLError:
            findings.add("CONTENT-002", "warning", "content_quality", p,
                         "SKILL.md has invalid YAML frontmatter")
            continue

        if fm.get("name"):
            name = fm["name"]
            if name.startswith("spectra-"):
                findings.passed()
            else:
                findings.add("CONTENT-003", "warning", "content_quality", p,
                             f'Frontmatter name "{name}" does not follow spectra-* convention')
        else:
            findings.add("CONTENT-004", "warning", "content_quality", p,
                         "Frontmatter missing required 'name' field")

        if fm.get("description"):
            findings.passed()
        else:
            findings.add("CONTENT-005", "warning", "content_quality", p,
                         "Frontmatter missing required 'description' field")


def check_agent_sections(spectra: Path, agent_rows: list[dict], findings: Findings,
                         module_filter: str | None):
    """Check required sections in agent SKILL.md files."""
    for row in agent_rows:
        p = row.get("path", "").strip()
        mod = row.get("module", "").strip()
        if not p or (module_filter and mod != module_filter):
            continue
        skill_file = (spectra.parent / p) / "SKILL.md"
        if not skill_file.is_file():
            continue

        content = skill_file.read_text(encoding="utf-8")
        h2_titles = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        h2_clean = [t.strip() for t in h2_titles]

        for req in AGENT_REQUIRED_SECTIONS:
            if req in h2_clean:
                findings.passed()
            else:
                findings.add("CONTENT-006", "warning", "content_quality",
                             f"{p}/SKILL.md",
                             f"Missing required section: ## {req}")

        # At least one identity section
        has_identity = any(s in h2_clean for s in AGENT_IDENTITY_SECTIONS)
        if has_identity:
            findings.passed()
        else:
            findings.add("CONTENT-007", "warning", "content_quality",
                         f"{p}/SKILL.md",
                         f"Missing identity sections (need at least one of: {', '.join(AGENT_IDENTITY_SECTIONS)})")

        # Capabilities table
        if "Capabilities" in h2_clean or re.search(r'\|\s*Code\s*\|', content):
            findings.passed()
        else:
            findings.add("CONTENT-008", "warning", "content_quality",
                         f"{p}/SKILL.md",
                         "Missing ## Capabilities section or capabilities table")


def check_core_skill_sections(spectra: Path, findings: Findings):
    """Check required sections in core skill SKILL.md files (non-agent)."""
    core_dir = spectra / "core"
    for d in sorted(core_dir.iterdir()):
        if not d.is_dir() or d.name.startswith(".") or d.name in ("collaboration", "engagement",
                "execution", "frameworks", "reporting"):
            continue
        # Skip agents — they are checked separately
        if "agent" in d.name:
            continue

        skill_file = d / "SKILL.md"
        if not skill_file.is_file():
            continue

        content = skill_file.read_text(encoding="utf-8")
        h2_titles = [t.strip() for t in re.findall(r'^##\s+(.+)$', content, re.MULTILINE)]
        rel = f"_spectra/core/{d.name}/SKILL.md"

        for req in ("Overview", "On Activation"):
            if req in h2_titles:
                findings.passed()
            else:
                # Some core skills use different section names — check flexibly
                if req == "Overview" and any("overview" in t.lower() for t in h2_titles):
                    findings.passed()
                elif req == "On Activation" and any("activation" in t.lower() or
                        "on activation" in t.lower() for t in h2_titles):
                    findings.passed()
                else:
                    findings.add("CONTENT-009", "warning", "content_quality", rel,
                                 f"Missing required section: ## {req}")


def check_workflow_step_content(spectra: Path, skill_rows: list[dict], findings: Findings,
                                module_filter: str | None):
    """Check step files for required content patterns."""
    for row in skill_rows:
        p = row.get("path", "").strip()
        mod = row.get("module", "").strip()
        cid = row.get("canonicalId", "")
        if not p or (module_filter and mod != module_filter):
            continue
        skill_dir = (spectra.parent / p).parent

        # Only check workflows
        steps_dir = skill_dir / "steps-c"
        if not steps_dir.is_dir():
            steps_dir = skill_dir / "steps"
        if not steps_dir.is_dir():
            continue

        step_files = sorted(f for f in steps_dir.iterdir()
                            if f.is_file() and f.suffix == ".md" and re.match(r'^step-\d+', f.name))
        for sf in step_files:
            content = sf.read_text(encoding="utf-8")
            rel = f"{skill_dir.relative_to(spectra.parent)}/steps-c/{sf.name}"
            checks = [
                ("STEP GOAL", "STEP-001"),
                ("MANDATORY EXECUTION RULES", "STEP-002"),
                ("Agent Autonomy Protocol", "STEP-003"),
            ]
            for pattern, code in checks:
                if pattern.lower() in content.lower():
                    findings.passed()
                else:
                    findings.add(code, "warning", "content_quality", rel,
                                 f"Missing required section: {pattern}")

            # SUCCESS/FAILURE metrics
            has_success = bool(re.search(r'SUCCESS:', content, re.IGNORECASE))
            has_failure = bool(re.search(r'(?:SYSTEM\s+)?FAILURE:', content, re.IGNORECASE))
            if has_success and has_failure:
                findings.passed()
            elif has_success or has_failure:
                findings.passed()  # partial credit
            else:
                findings.add("STEP-004", "info", "content_quality", rel,
                             "Missing SUCCESS/FAILURE metrics section")


# ---------------------------------------------------------------------------
# Tier 3 — Cross-Reference Validation
# ---------------------------------------------------------------------------
def check_manifest_filesystem_sync(spectra: Path, agent_rows: list[dict],
                                   skill_rows: list[dict], findings: Findings,
                                   module_filter: str | None):
    """Check for orphan directories with no manifest entry and vice-versa."""
    # Build set of known paths from manifests
    known_agent_dirs = set()
    for row in agent_rows:
        p = row.get("path", "").strip()
        if p:
            known_agent_dirs.add(p.rstrip("/"))

    known_skill_paths = set()
    skill_dirs_from_manifest = set()
    for row in skill_rows:
        p = row.get("path", "").strip()
        if p:
            known_skill_paths.add(p)
            skill_dirs_from_manifest.add(str((spectra.parent / p).parent.relative_to(spectra.parent)))

    # Scan filesystem for agent directories
    for mod in MODULES:
        if module_filter and mod != module_filter and mod != "core":
            continue
        if mod == "core":
            # Core agents are at _spectra/core/spectra-agent-*
            core_dir = spectra / "core"
            if core_dir.is_dir():
                for d in core_dir.iterdir():
                    if d.is_dir() and "agent" in d.name:
                        rel = f"_spectra/core/{d.name}"
                        if rel in known_agent_dirs:
                            findings.passed()
                        else:
                            findings.add("XREF-001", "info", "cross_reference", rel,
                                         f"Agent directory exists but not in agent-manifest.csv")
        else:
            agents_dir = spectra / mod / "agents"
            if agents_dir.is_dir():
                for d in agents_dir.iterdir():
                    if d.is_dir():
                        rel = f"_spectra/{mod}/agents/{d.name}"
                        if rel in known_agent_dirs:
                            findings.passed()
                        else:
                            findings.add("XREF-001", "info", "cross_reference", rel,
                                         f"Agent directory exists but not in agent-manifest.csv")

    # Scan filesystem for workflow directories
    for mod in MODULES:
        if module_filter and mod != module_filter and mod != "core":
            continue
        if mod == "core":
            # Core skills at _spectra/core/spectra-*
            core_dir = spectra / "core"
            if core_dir.is_dir():
                for d in core_dir.iterdir():
                    if d.is_dir() and d.name.startswith("spectra-") and "agent" not in d.name:
                        rel = f"_spectra/core/{d.name}"
                        if rel in skill_dirs_from_manifest:
                            findings.passed()
                        else:
                            findings.add("XREF-002", "info", "cross_reference", rel,
                                         f"Skill directory exists but not in skill-manifest.csv")
        else:
            wf_dir = spectra / mod / "workflows"
            if wf_dir.is_dir():
                for d in wf_dir.iterdir():
                    if d.is_dir():
                        rel = f"_spectra/{mod}/workflows/{d.name}"
                        if rel in skill_dirs_from_manifest:
                            findings.passed()
                        else:
                            findings.add("XREF-002", "info", "cross_reference", rel,
                                         f"Workflow directory exists but not in skill-manifest.csv")

    # Module field consistency
    for row in skill_rows:
        p = row.get("path", "").strip()
        mod = row.get("module", "").strip()
        if not p or not mod:
            continue
        # Infer module from path
        parts = p.split("/")
        if len(parts) >= 2:
            path_mod = parts[1]  # _spectra/{module}/...
            if path_mod == mod:
                findings.passed()
            else:
                findings.add("XREF-003", "warning", "cross_reference", p,
                             f"Module field '{mod}' does not match path module '{path_mod}'")


def check_skill_cross_references(spectra: Path, skill_rows: list[dict],
                                 agent_rows: list[dict], findings: Findings,
                                 module_filter: str | None):
    """Check that references to other skills/agents in SKILL.md files exist."""
    known_skills = {r.get("canonicalId", "") for r in skill_rows}
    known_agents = {r.get("name", "") for r in agent_rows}
    known_all = known_skills | known_agents

    # Regex for spectra-* references
    ref_re = re.compile(r'\bspectra-[a-z0-9]+(?:-[a-z0-9]+)*\b')

    all_skills = list(skill_rows)
    for row in all_skills:
        p = row.get("path", "").strip()
        mod = row.get("module", "").strip()
        if not p or (module_filter and mod != module_filter):
            continue
        skill_file = spectra.parent / p
        if not skill_file.is_file():
            continue

        content = skill_file.read_text(encoding="utf-8")
        refs = set(ref_re.findall(content))
        for ref in refs:
            # Skip self-references and common prefixes
            if ref in known_all or ref.startswith("spectra-output"):
                findings.passed()
            else:
                # Only flag if it looks like a skill/agent reference (not a directory name)
                # Heuristic: if it appears after "invoke", "use", "call", "via", or as a capability link
                findings.add("XREF-004", "info", "cross_reference", p,
                             f'Reference to "{ref}" not found in any manifest')


# ---------------------------------------------------------------------------
# Tier 4 — Path & Language Standards, Framework Data, Execution Scripts
# ---------------------------------------------------------------------------
def check_path_standards(spectra: Path, skill_rows: list[dict], findings: Findings,
                         module_filter: str | None):
    """Check for absolute paths and parent directory references in SKILL.md files."""
    for row in skill_rows:
        p = row.get("path", "").strip()
        mod = row.get("module", "").strip()
        if not p or (module_filter and mod != module_filter):
            continue
        skill_file = spectra.parent / p
        if not skill_file.is_file():
            continue

        content = skill_file.read_text(encoding="utf-8")

        for m in ABSOLUTE_PATH_RE.finditer(content):
            line_num = content[:m.start()].count('\n') + 1
            findings.add("PATH-001", "warning", "path_standards", p,
                         f"Absolute path found: {m.group(1)[:80]}",
                         "Use {{project-root}} prefix instead", line_num)

        for m in PARENT_DIR_RE.finditer(content):
            line_num = content[:m.start()].count('\n') + 1
            findings.add("PATH-002", "warning", "path_standards", p,
                         f"Parent directory reference (../): {m.group(1)[:80]}",
                         "Use ./ for skill-internal or {{project-root}} for project-scope", line_num)

        findings.passed()


def check_framework_data(spectra: Path, findings: Findings):
    """Validate framework data directories have expected files."""
    frameworks = {
        "mitre-attack": (".json", "MITRE ATT&CK"),
        "nist": (".json", "NIST"),
        "sigma-rules": (".yaml", "Sigma Rules"),
        "owasp": (".json", "OWASP"),
    }
    fw_dir = spectra / "core" / "frameworks"
    if not fw_dir.is_dir():
        findings.add("FW-001", "critical", "framework_data",
                     "_spectra/core/frameworks/", "Frameworks directory does not exist")
        return

    for name, (ext, label) in frameworks.items():
        d = fw_dir / name
        if not d.is_dir():
            findings.add("FW-002", "warning", "framework_data",
                         f"_spectra/core/frameworks/{name}/",
                         f"{label} framework directory missing")
            continue

        matching = list(d.rglob(f"*{ext}"))
        if matching:
            findings.passed()
        else:
            findings.add("FW-003", "warning", "framework_data",
                         f"_spectra/core/frameworks/{name}/",
                         f"No {ext} files found in {label} directory")


def check_execution_scripts(spectra: Path, findings: Findings):
    """Validate execution scripts exist and have valid syntax."""
    exec_dir = spectra / "core" / "execution"
    if not exec_dir.is_dir():
        findings.add("EXEC-001", "critical", "execution_scripts",
                     "_spectra/core/execution/", "Execution directory does not exist")
        return

    required = {
        "scope-enforcer.py": "Scope enforcer script",
        "evidence-logger.py": "Evidence logger script",
        "tools-registry.yaml": "Tools registry",
    }

    for fname, label in required.items():
        fpath = exec_dir / fname
        if fpath.is_file():
            findings.passed()
            # Python syntax check
            if fname.endswith(".py"):
                try:
                    py_compile.compile(str(fpath), doraise=True)
                    findings.passed()
                except py_compile.PyCompileError as e:
                    findings.add("EXEC-002", "warning", "execution_scripts",
                                 f"_spectra/core/execution/{fname}",
                                 f"Python syntax error: {e}")
            # YAML validity check
            elif fname.endswith(".yaml"):
                try:
                    yaml.safe_load(fpath.read_text(encoding="utf-8"))
                    findings.passed()
                except yaml.YAMLError as e:
                    findings.add("EXEC-003", "warning", "execution_scripts",
                                 f"_spectra/core/execution/{fname}",
                                 f"Invalid YAML: {e}")
        else:
            findings.add("EXEC-004", "critical", "execution_scripts",
                         f"_spectra/core/execution/{fname}",
                         f"Missing required execution file: {label}")


# ---------------------------------------------------------------------------
# Output Formatters
# ---------------------------------------------------------------------------
SEVERITY_ORDER = {"critical": 0, "warning": 1, "info": 2}
SEVERITY_LABELS = {
    "critical": "\033[31m\u274c CRITICAL\033[0m",
    "warning": "\033[33m\u26a0\ufe0f  WARNING\033[0m",
    "info": "\033[36m\u2139\ufe0f  INFO\033[0m",
}
SEVERITY_LABELS_PLAIN = {
    "critical": "CRITICAL",
    "warning": "WARNING",
    "info": "INFO",
}


def format_text(findings: Findings, fix_suggestions: bool, no_color: bool) -> str:
    """Format findings as terminal output."""
    s = findings.summary()
    labels = SEVERITY_LABELS_PLAIN if no_color else SEVERITY_LABELS
    items = sorted(findings.items, key=lambda f: (SEVERITY_ORDER.get(f["severity"], 9), f["code"]))

    lines = []
    if no_color:
        lines.append("=" * 60)
        lines.append("          SPECTRA PROJECT VALIDATION REPORT")
        lines.append(f"          v{VERSION} -- {datetime.now().strftime('%Y-%m-%d')}")
        lines.append("=" * 60)
    else:
        lines.append("\033[1m\u2554" + "\u2550" * 58 + "\u2557\033[0m")
        lines.append("\033[1m\u2551          SPECTRA PROJECT VALIDATION REPORT" + " " * 15 + "\u2551\033[0m")
        lines.append(f"\033[1m\u2551          v{VERSION} -- {datetime.now().strftime('%Y-%m-%d')}" + " " * 27 + "\u2551\033[0m")
        lines.append("\033[1m\u255a" + "\u2550" * 58 + "\u255d\033[0m")

    lines.append("")
    p_mark = "PASSED" if no_color else "\033[32m\u2705\033[0m"
    w_mark = "WARNINGS" if no_color else "\033[33m\u26a0\ufe0f\033[0m"
    f_mark = "FAILED" if no_color else "\033[31m\u274c\033[0m"

    lines.append("SUMMARY")
    lines.append(f"   Total checks: {s['total']}")
    lines.append(f"   {p_mark} Passed:   {s['passed']}")
    lines.append(f"   {w_mark} Warnings: {s['warnings']}")
    lines.append(f"   {f_mark} Failed:   {s['critical']}")
    lines.append(f"   INFO:       {s['info']}")
    lines.append("")

    # Group by severity
    for sev in ("critical", "warning", "info"):
        sev_items = [f for f in items if f["severity"] == sev]
        if not sev_items:
            continue
        header_map = {"critical": "CRITICAL (Tier 1-2)", "warning": "WARNING (Tier 2-3)", "info": "INFO (Tier 3-4)"}
        lines.append(f"{labels[sev]}  ({len(sev_items)} findings)")
        lines.append("-" * 60)
        for f in sev_items:
            icon = {"critical": "X", "warning": "!", "info": "i"}[sev] if no_color else \
                   {"critical": "\u274c", "warning": "\u26a0\ufe0f", "info": "\u2139\ufe0f"}[sev]
            line_info = f" (line {f['line']})" if f.get("line") else ""
            lines.append(f"   {icon} [{f['code']}] {f['message']}")
            lines.append(f"     File: {f['file']}{line_info}")
            if f.get("fix") and fix_suggestions:
                lines.append(f"     Fix: {f['fix']}")
        lines.append("")

    if fix_suggestions and items:
        lines.append("FIX SUGGESTIONS")
        lines.append("-" * 60)
        seen = set()
        idx = 1
        for f in items:
            if f.get("fix") and f["fix"] not in seen:
                seen.add(f["fix"])
                lines.append(f"   {idx}. {f['fix']}")
                idx += 1
        lines.append("")

    return "\n".join(lines)


def format_json(findings: Findings) -> str:
    """Format findings as JSON."""
    s = findings.summary()
    return json.dumps({
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "summary": s,
        "findings": findings.items,
    }, indent=2)


def format_summary(findings: Findings, no_color: bool) -> str:
    """Format just the summary box."""
    s = findings.summary()
    lines = []
    if no_color:
        lines.append("=" * 60)
        lines.append("  SPECTRA VALIDATION SUMMARY")
        lines.append("=" * 60)
    else:
        lines.append("\033[1m\u2554" + "\u2550" * 40 + "\u2557\033[0m")
        lines.append("\033[1m\u2551  SPECTRA VALIDATION SUMMARY" + " " * 12 + "\u2551\033[0m")
        lines.append("\033[1m\u255a" + "\u2550" * 40 + "\u255d\033[0m")

    status_icon = "\033[32mPASS\033[0m" if s["critical"] == 0 else "\033[31mFAIL\033[0m"
    if no_color:
        status_icon = "PASS" if s["critical"] == 0 else "FAIL"

    lines.append(f"  Status:   {status_icon}")
    lines.append(f"  Checks:   {s['total']}")
    lines.append(f"  Passed:   {s['passed']}")
    lines.append(f"  Critical: {s['critical']}")
    lines.append(f"  Warnings: {s['warnings']}")
    lines.append(f"  Info:     {s['info']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------
def validate(spectra: Path, module_filter: str | None = None) -> Findings:
    """Run all validation tiers."""
    findings = Findings()

    # Tier 1 — Structural
    agent_rows, skill_rows = check_manifest_integrity(spectra, findings)
    check_config_validation(spectra, findings, module_filter)
    check_file_existence_agents(spectra, agent_rows, findings)
    check_file_existence_skills(spectra, skill_rows, findings)
    check_file_existence_workflows(spectra, skill_rows, findings)

    # Tier 2 — Content Quality
    check_skill_frontmatter(spectra, skill_rows, findings, module_filter)
    check_agent_sections(spectra, agent_rows, findings, module_filter)
    check_core_skill_sections(spectra, findings)
    check_workflow_step_content(spectra, skill_rows, findings, module_filter)

    # Tier 3 — Cross-References
    check_manifest_filesystem_sync(spectra, agent_rows, skill_rows, findings, module_filter)
    check_skill_cross_references(spectra, skill_rows, agent_rows, findings, module_filter)

    # Tier 4 — Path Standards, Frameworks, Execution
    check_path_standards(spectra, skill_rows, findings, module_filter)
    check_framework_data(spectra, findings)
    check_execution_scripts(spectra, findings)

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="SPECTRA Project Validator — structural, content, and consistency validation",
    )
    parser.add_argument("--path", required=True, type=Path,
                        help="Path to the _spectra/ directory")
    parser.add_argument("--module", default=None, choices=["rtk", "soc", "irt", "grc"],
                        help="Validate only a specific module")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output results as JSON")
    parser.add_argument("--summary", action="store_true",
                        help="Output only the summary box")
    parser.add_argument("--fix-suggestions", action="store_true",
                        help="Include fix suggestions in output")
    parser.add_argument("--strict", action="store_true",
                        help="Treat warnings as failures")
    parser.add_argument("--no-color", action="store_true",
                        help="Disable ANSI color codes in output")

    args = parser.parse_args()
    spectra = args.path.resolve()

    if not spectra.is_dir():
        print(f"Error: {spectra} is not a directory", file=sys.stderr)
        return 2

    # Auto-detect: if user passed the project root instead of _spectra/
    if (spectra / "_spectra").is_dir() and not (spectra / "_config").is_dir():
        spectra = spectra / "_spectra"

    findings = validate(spectra, module_filter=args.module)
    s = findings.summary()

    if args.json_output:
        print(format_json(findings))
    elif args.summary:
        print(format_summary(findings, args.no_color))
    else:
        print(format_text(findings, args.fix_suggestions, args.no_color))

    # Exit codes
    if s["critical"] > 0:
        return 2
    if args.strict and s["warnings"] > 0:
        return 1
    if s["warnings"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
