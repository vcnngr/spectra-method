#!/usr/bin/env python3
"""Regression tests for the SPECTRA Engagement Personas helper."""

from __future__ import annotations

import csv
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "engagement-personas.py"
REPO_ROOT = Path(__file__).resolve().parents[3]
AGENT_MANIFEST = REPO_ROOT / "_config" / "agent-manifest.csv"
SKILL_MANIFEST = REPO_ROOT / "_config" / "skill-manifest.csv"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ep = load_module("engagement_personas", SCRIPT)


SAMPLE_MANIFEST = """\
"name","displayName","title","icon","capabilities","role","identity","communicationStyle","principles","module","path","canonicalId"
"spectra-agent-red-lead","Viper","Red Team Lead","x","c","Red Team Lead","i","s","p","rtk","path","spectra-agent-red-lead"
"spectra-agent-blade","Blade","Quick Pentester","x","c","Quick Pentester","i","s","p","rtk","path","spectra-agent-blade"
"spectra-agent-recon","Ghost","Recon","x","c","Recon Specialist","i","s","p","rtk","path","spectra-agent-recon"
"spectra-agent-exploit","Razor","Exploit Dev","x","c","Exploit Developer","i","s","p","rtk","path","spectra-agent-exploit"
"spectra-agent-operator","Phantom","Operator","x","c","Attack Operator","i","s","p","rtk","path","spectra-agent-operator"
"spectra-agent-appsec","Forge","AppSec","x","c","AppSec Specialist","i","s","p","rtk","path","spectra-agent-appsec"
"spectra-agent-soc-manager","Commander","SOC Manager","x","c","SOC Manager","i","s","p","soc","path","spectra-agent-soc-manager"
"spectra-agent-specter","Specter","CISO","x","c","CISO","i","s","p","core","path","spectra-agent-specter"
"""


class EngagementPersonasTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.manifest = Path(self.tmp.name) / "agent-manifest.csv"
        self.manifest.write_text(SAMPLE_MANIFEST, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    # -- loading -----------------------------------------------------------

    def test_load_personas(self):
        personas = ep.load_personas(self.manifest)
        self.assertIn("spectra-agent-red-lead", personas)
        self.assertEqual(personas["spectra-agent-red-lead"]["displayName"], "Viper")
        self.assertEqual(personas["spectra-agent-red-lead"]["module"], "rtk")

    def test_missing_manifest_raises(self):
        with self.assertRaises(FileNotFoundError):
            ep.load_personas(Path(self.tmp.name) / "nope.csv")

    def test_load_personas_tolerates_utf8_bom(self):
        bom_manifest = Path(self.tmp.name) / "bom.csv"
        bom_manifest.write_text("﻿" + SAMPLE_MANIFEST, encoding="utf-8")
        personas = ep.load_personas(bom_manifest)
        # Without BOM tolerance the first column key would be "﻿name".
        self.assertIn("spectra-agent-red-lead", personas)

    def test_missing_required_column_raises(self):
        bad = Path(self.tmp.name) / "bad.csv"
        bad.write_text('"name","displayName","role"\n"x","X","r"\n', encoding="utf-8")
        with self.assertRaises(ValueError):
            ep.load_personas(bad)

    def test_build_catalog_groups_by_module_in_order(self):
        personas = ep.load_personas(self.manifest)
        catalog = ep.build_catalog(personas)
        # core must come before rtk/soc per the module order.
        keys = list(catalog.keys())
        self.assertLess(keys.index("core"), keys.index("rtk"))
        self.assertIn("spectra-agent-specter", [p["name"] for p in catalog["core"]])

    # -- recommendation ----------------------------------------------------

    def test_recommend_pentest(self):
        personas = ep.load_personas(self.manifest)
        rec = ep.recommend("pentest", personas)
        self.assertEqual(rec["lead"]["name"], "spectra-agent-red-lead")
        self.assertEqual(rec["solo"]["name"], "spectra-agent-blade")
        self.assertIn("spectra-external-recon", rec["workflows"])

    def test_recommend_unknown_type_raises(self):
        personas = ep.load_personas(self.manifest)
        with self.assertRaises(ValueError):
            ep.recommend("nonsense", personas)

    def test_recommend_missing_persona_raises(self):
        # The sample manifest lacks incident-response agents -> KeyError.
        personas = ep.load_personas(self.manifest)
        with self.assertRaises(KeyError):
            ep.recommend("incident-response", personas)

    # -- integrity against the REAL repo manifests -------------------------

    def test_profile_map_consistent_with_real_manifest(self):
        personas = ep.load_personas(AGENT_MANIFEST)
        missing = ep.validate_profile_map(personas)
        self.assertEqual(missing, [], f"PROFILE_MAP references unknown agents: {missing}")

    def test_every_engagement_type_recommends_cleanly(self):
        personas = ep.load_personas(AGENT_MANIFEST)
        for etype in ep.ENGAGEMENT_TYPES:
            rec = ep.recommend(etype, personas)
            self.assertTrue(rec["lead"]["displayName"])
            self.assertTrue(rec["solo"]["name"])
            self.assertTrue(rec["support"])

    def test_profile_map_workflows_exist_in_skill_manifest(self):
        # Every workflow a profile suggests must be a real registered skill that
        # is NOT an agent — so a reference cannot silently drift to an agent name.
        # (Core workflows like war-room live under /core/, not /workflows/, so we
        # key on the agent-vs-skill naming distinction rather than the path.)
        with SKILL_MANIFEST.open(encoding="utf-8-sig") as handle:
            known_workflows = {
                (r.get("name") or "").strip()
                for r in csv.DictReader(handle)
                if not (r.get("name") or "").strip().startswith("spectra-agent-")
            }
        referenced = set()
        for profile in ep.PROFILE_MAP.values():
            referenced.update(profile["workflows"])
        unknown = sorted(w for w in referenced if w not in known_workflows)
        self.assertEqual(unknown, [], f"PROFILE_MAP references unknown workflows: {unknown}")

    def test_engagement_types_match_schema_enum(self):
        # Three-way drift guard: schema enum == ENGAGEMENT_TYPES == PROFILE_MAP keys.
        import re
        schema = (REPO_ROOT / "core" / "schemas" / "engagement.schema.yaml").read_text(encoding="utf-8")
        # The type enum line, e.g.: enum: [pentest, red-team, ...]
        m = re.search(r"type:\s*\n\s*type:\s*string\s*\n\s*enum:\s*\[([^\]]+)\]", schema)
        self.assertIsNotNone(m, "Could not locate engagement type enum in schema")
        schema_types = {t.strip() for t in m.group(1).split(",")}
        self.assertEqual(schema_types, set(ep.ENGAGEMENT_TYPES),
                         "ENGAGEMENT_TYPES drifted from the schema enum")
        self.assertEqual(set(ep.PROFILE_MAP.keys()), set(ep.ENGAGEMENT_TYPES),
                         "PROFILE_MAP keys drifted from ENGAGEMENT_TYPES")

    def test_duplicate_agent_name_raises(self):
        dup = Path(self.tmp.name) / "dup.csv"
        dup.write_text(SAMPLE_MANIFEST + '"spectra-agent-red-lead","ViperDup","x","x","c","r","i","s","p","rtk","path","x"\n', encoding="utf-8")
        with self.assertRaises(ValueError):
            ep.load_personas(dup)

    def test_persona_includes_path(self):
        personas = ep.load_personas(AGENT_MANIFEST)
        red = personas["spectra-agent-red-lead"]
        self.assertIn("path", red)
        self.assertTrue(red["path"])

    def test_real_manifest_has_28_personas(self):
        personas = ep.load_personas(AGENT_MANIFEST)
        self.assertEqual(len(personas), 28)

    # -- CLI ---------------------------------------------------------------

    def test_cli_list(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ep.main(["--manifest", str(self.manifest), "list"])
        data = json.loads(buf.getvalue())
        self.assertEqual(data["persona_count"], 8)
        self.assertIn("by_module", data)

    def test_cli_recommend(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ep.main(["--manifest", str(self.manifest), "recommend", "--type", "pentest"])
        data = json.loads(buf.getvalue())
        self.assertEqual(data["lead"]["name"], "spectra-agent-red-lead")


if __name__ == "__main__":
    unittest.main()
