#!/usr/bin/env python3
"""Regression tests for the SPECTRA Tool Adapter (fail-closed flag allowlist)."""

from __future__ import annotations

import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "tool-adapter.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


ta = load_module("tool_adapter", SCRIPT)


ENGAGEMENT = """\
engagement:
  id: "ENG-T"
  type: "pentest"
  rules_of_engagement:
    dos_testing_allowed: false
    data_exfiltration_allowed: false
    production_systems: false
  scope:
    in_scope:
      networks: ["127.0.0.0/8"]
      domains: ["lab.example.com"]
    out_of_scope:
      networks: ["10.9.9.0/24"]
"""


class ToolAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.eng = Path(self.tmp.name) / "engagement.yaml"
        self.eng.write_text(ENGAGEMENT, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    # -- resolve / build ---------------------------------------------------

    def test_unknown_tool_raises(self):
        with self.assertRaises(KeyError):
            ta.resolve_tool("definitely-not-a-tool")

    def test_nuclei_is_not_allowlisted(self):
        # nuclei was removed: its templates can execute code.
        with self.assertRaises(KeyError):
            ta.resolve_tool("nuclei")

    def test_build_argv_plain(self):
        argv = ta.build_argv(ta.ADAPTERS["nmap"], "127.0.0.1", ["-sV"])
        self.assertEqual(argv, ["nmap", "-sV", "127.0.0.1"])

    def test_build_argv_target_flag(self):
        argv = ta.build_argv(ta.ADAPTERS["httpx"], "http://lab.example.com", None)
        self.assertEqual(argv, ["httpx", "-u", "http://lab.example.com"])

    # -- destructive HARD BLOCK -------------------------------------------

    def test_destructive_rm_blocked(self):
        ok, reason = ta.destructive_check(["nmap", "; rm -rf /"])
        self.assertFalse(ok)
        self.assertIn("destructive", reason)

    def test_destructive_rm_variants_blocked(self):
        for variant in ("; rm -r -f /", "rm --recursive --force /", "rm -fr /"):
            ok, _ = ta.destructive_check([variant])
            self.assertFalse(ok, variant)

    def test_benign_passes_destructive_check(self):
        ok, _ = ta.destructive_check(["nmap", "-sV", "127.0.0.1"])
        self.assertTrue(ok)

    def test_ransomware_word_blocked_at_gate(self):
        # ransomware/wiper are blocked at the action level (scope-enforcer).
        g = self._gate("127.0.0.1", ["nmap", "127.0.0.1"], extra=["ransomware"])
        self.assertFalse(g["allowed"])

    # -- target validation -------------------------------------------------

    def test_target_starting_with_dash_rejected(self):
        ok, _ = ta.validate_target("-iR")
        self.assertFalse(ok)

    def test_target_with_whitespace_rejected(self):
        ok, _ = ta.validate_target("127.0.0.1 10.0.0.1")
        self.assertFalse(ok)

    def test_target_with_null_byte_rejected(self):
        ok, _ = ta.validate_target("127.0.0.1\x00rm")
        self.assertFalse(ok)

    def test_valid_target_accepted(self):
        ok, _ = ta.validate_target("127.0.0.1")
        self.assertTrue(ok)

    # -- fail-closed flag allowlist ---------------------------------------

    def _va(self, tool, extra):
        return ta.validate_extra_args(ta.ADAPTERS[tool], extra)

    def test_safe_flags_pass(self):
        ok, _ = self._va("nmap", ["-sV", "-p", "1-1000", "-T4"])
        self.assertTrue(ok)

    def test_output_flag_blocked(self):
        ok, _ = self._va("nmap", ["-oN", "/etc/passwd"])
        self.assertFalse(ok)

    def test_concatenated_output_flag_blocked(self):
        # -oN/tmp/x as a single token is not on the allowlist -> blocked.
        ok, _ = self._va("nmap", ["-oN/tmp/x"])
        self.assertFalse(ok)

    def test_equals_output_flag_blocked(self):
        ok, _ = self._va("nmap", ["--output=/tmp/x"])
        self.assertFalse(ok)

    def test_nmap_iR_blocked(self):
        # -iR overrides the gated target with random hosts -> must be refused.
        ok, _ = self._va("nmap", ["-iR", "1000"])
        self.assertFalse(ok)

    def test_nmap_resume_blocked(self):
        ok, _ = self._va("nmap", ["--resume", "/etc/passwd"])
        self.assertFalse(ok)

    def test_nmap_script_blocked(self):
        ok, _ = self._va("nmap", ["--script", "http-vuln"])
        self.assertFalse(ok)

    def test_httpx_store_response_blocked(self):
        ok, _ = self._va("httpx", ["-sr"])
        self.assertFalse(ok)

    def test_dig_batch_file_blocked(self):
        ok, _ = self._va("dig", ["-f", "/etc/hosts"])
        self.assertFalse(ok)

    def test_dig_record_type_value_allowed(self):
        ok, _ = self._va("dig", ["+short", "A"])
        self.assertTrue(ok)

    def test_value_with_path_blocked(self):
        # A value following a value-flag must not be a filesystem path.
        ok, _ = self._va("nmap", ["-p", "/etc/passwd"])
        self.assertFalse(ok)

    def test_unexpected_bare_value_blocked(self):
        ok, _ = self._va("nmap", ["randomthing"])
        self.assertFalse(ok)

    # -- gating ------------------------------------------------------------

    def _gate(self, target, argv, extra=None, adapter="nmap"):
        import yaml
        eng = yaml.safe_load(self.eng.read_text())
        return ta.gate(eng, ta.ADAPTERS[adapter], target, argv, extra)

    def test_in_scope_allowed(self):
        g = self._gate("127.0.0.1", ["nmap", "127.0.0.1"], extra=["-sV"])
        self.assertTrue(g["allowed"], g["errors"])

    def test_out_of_scope_blocked(self):
        g = self._gate("10.9.9.5", ["nmap", "10.9.9.5"])
        self.assertFalse(g["allowed"])
        self.assertTrue(any("out of scope" in e for e in g["errors"]))

    def test_not_in_scope_blocked(self):
        g = self._gate("8.8.8.8", ["nmap", "8.8.8.8"])
        self.assertFalse(g["allowed"])
        self.assertTrue(any("not in engagement scope" in e for e in g["errors"]))

    def test_gate_blocks_iR_even_in_scope(self):
        # Confirmed scope bypass: -iR with an in-scope target must still block.
        g = self._gate("127.0.0.1", ["nmap", "-iR", "1000", "127.0.0.1"],
                       extra=["-iR", "1000"])
        self.assertFalse(g["allowed"])

    def test_gate_blocks_output_flag_in_scope(self):
        g = self._gate("127.0.0.1", ["nmap", "-oN", "/etc/passwd", "127.0.0.1"],
                       extra=["-oN", "/etc/passwd"])
        self.assertFalse(g["allowed"])

    def test_roe_action_blocked(self):
        g = self._gate("127.0.0.1", ["nmap", "127.0.0.1"], extra=["exfil"])
        self.assertFalse(g["allowed"])

    def test_cidr_contained_allowed(self):
        # 127.0.0.0/24 is fully inside the in-scope 127.0.0.0/8.
        g = self._gate("127.0.0.0/24", ["nmap", "127.0.0.0/24"])
        self.assertTrue(g["allowed"], g["errors"])

    def test_cidr_overlap_not_contained_blocked(self):
        # 0.0.0.0/0 merely OVERLAPS the in-scope net — must be blocked.
        g = self._gate("0.0.0.0/0", ["nmap", "0.0.0.0/0"])
        self.assertFalse(g["allowed"])
        self.assertTrue(any("not fully contained" in e for e in g["errors"]))

    def test_httpx_method_flag_blocked(self):
        # -method could send mutating HTTP verbs; not on the allowlist.
        ok, _ = self._va("httpx", ["-method", "DELETE"])
        self.assertFalse(ok)

    # -- URL path-aware scope ---------------------------------------------

    def test_url_application_path_prefix(self):
        scope = {"applications": ["https://lab.example.com/app"]}
        self.assertTrue(ta._url_in_scope("https://lab.example.com/app", scope))
        self.assertTrue(ta._url_in_scope("https://lab.example.com/app/x", scope))
        # Same host, different path -> NOT in scope (the bypass being closed).
        self.assertFalse(ta._url_in_scope("https://lab.example.com/admin", scope))

    def test_url_host_only_application_allows_any_path(self):
        scope = {"applications": ["https://lab.example.com"]}
        self.assertTrue(ta._url_in_scope("https://lab.example.com/anything", scope))

    def test_url_domain_scope_allows_any_path(self):
        scope = {"domains": ["lab.example.com"]}
        self.assertTrue(ta._url_in_scope("https://lab.example.com/admin", scope))

    def test_url_other_host_blocked(self):
        scope = {"applications": ["https://lab.example.com/app"]}
        self.assertFalse(ta._url_in_scope("https://evil.example.com/app", scope))

    # -- binary identity pinning ------------------------------------------

    def test_verify_identity_match(self):
        echo = shutil.which("echo")
        adapter = {"binary": "echo", "identity": {"probe": ["SPECTRA"], "expect": "spectra"}}
        ok, _ = ta.verify_identity(echo, adapter)
        self.assertTrue(ok)

    def test_verify_identity_mismatch(self):
        echo = shutil.which("echo")
        adapter = {"binary": "echo", "identity": {"probe": ["SPECTRA"], "expect": "projectdiscovery"}}
        ok, reason = ta.verify_identity(echo, adapter)
        self.assertFalse(ok)
        self.assertIn("not the expected", reason)

    def test_verify_identity_skipped_without_block(self):
        ok, _ = ta.verify_identity("/bin/echo", {"binary": "echo"})
        self.assertTrue(ok)

    def test_run_identity_mismatch_marks_unavailable(self):
        ta.ADAPTERS["_test_id"] = {
            "binary": "echo", "action": "recon", "read_only": True,
            "allowed_flags": set(), "value_flags": set(), "allowed_values": set(),
            "identity": {"probe": ["x"], "expect": "projectdiscovery"},
        }
        try:
            result = ta.run(str(self.eng), "_test_id", "127.0.0.1")
            self.assertEqual(result["status"], "unavailable")
        finally:
            del ta.ADAPTERS["_test_id"]

    # -- run orchestration -------------------------------------------------

    def test_run_blocked_does_not_execute(self):
        result = ta.run(str(self.eng), "nmap", "8.8.8.8")
        self.assertEqual(result["status"], "blocked")
        self.assertNotIn("execution", result)

    def test_run_dry_run_plans_without_binary(self):
        result = ta.run(str(self.eng), "nmap", "127.0.0.1", extra_args=["-sV"], dry_run=True)
        self.assertEqual(result["status"], "planned")
        self.assertEqual(result["argv"], ["nmap", "-sV", "127.0.0.1"])

    def test_run_real_execution_with_echo(self):
        ta.ADAPTERS["_test_echo"] = {
            "binary": "echo", "action": "recon", "read_only": True,
            "allowed_flags": set(), "value_flags": set(), "allowed_values": set(),
        }
        try:
            result = ta.run(str(self.eng), "_test_echo", "127.0.0.1")
            self.assertEqual(result["status"], "executed")
            self.assertEqual(result["execution"]["exit_code"], 0)
            self.assertIn("127.0.0.1", result["execution"]["stdout"])
        finally:
            del ta.ADAPTERS["_test_echo"]

    def test_execute_captures_output(self):
        out = ta.execute(["echo", "spectra-ok"])
        self.assertEqual(out["exit_code"], 0)
        self.assertIn("spectra-ok", out["stdout"])
        self.assertFalse(out["timed_out"])
        self.assertFalse(out["truncated"])

    # -- CLI ---------------------------------------------------------------

    def test_cli_list(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ta.main(["list"])
        import json
        data = json.loads(buf.getvalue())
        self.assertIn("nmap", data["tools"])
        self.assertNotIn("nuclei", data["tools"])

    def test_cli_run_blocked_exits_1(self):
        with self.assertRaises(SystemExit) as cm, redirect_stdout(io.StringIO()):
            ta.main(["run", "--engagement", str(self.eng), "--tool", "nmap",
                     "--target", "8.8.8.8"])
        self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
