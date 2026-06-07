#!/usr/bin/env python3
"""Regression tests for the SPECTRA Exec Target (SSH, fingerprint-pinned)."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "exec-target.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


et = load_module("exec_target", SCRIPT)


PIN = "SHA256:TESTpinnedfingerprintAAAAAAAAAAAAAAAAAAAAAA"


def engagement(**overrides):
    target = {
        "host": "127.0.0.1", "port": 2222, "user": "operator",
        "pinned_fingerprint": PIN, "authorized": True,
    }
    target.update(overrides.pop("target", {}))
    eng = {
        "engagement": {
            "id": "E1", "type": "pentest",
            "scope": {"in_scope": {"networks": ["127.0.0.0/8"]}, "out_of_scope": {}},
            "exec_target": target,
        }
    }
    eng["engagement"].update(overrides)
    return eng


class ExecTargetValidationTests(unittest.TestCase):
    def test_absent_exec_target(self):
        v = et.validate_exec_target({"engagement": {"id": "E1"}})
        self.assertFalse(v["present"])
        self.assertFalse(v["allowed"])

    def test_valid_target_allowed(self):
        v = et.validate_exec_target(engagement())
        self.assertTrue(v["allowed"], v["errors"])

    def test_not_authorized_blocked(self):
        v = et.validate_exec_target(engagement(target={"authorized": False}))
        self.assertFalse(v["allowed"])
        self.assertTrue(any("authorized" in e for e in v["errors"]))

    def test_missing_host_blocked(self):
        v = et.validate_exec_target(engagement(target={"host": ""}))
        self.assertFalse(v["allowed"])

    def test_bad_fingerprint_format_blocked(self):
        v = et.validate_exec_target(engagement(target={"pinned_fingerprint": "deadbeef"}))
        self.assertFalse(v["allowed"])

    def test_out_of_scope_host_blocked(self):
        eng = engagement(target={"host": "8.8.8.8"})
        v = et.validate_exec_target(eng)
        self.assertFalse(v["allowed"])
        self.assertTrue(any("scope" in e for e in v["errors"]))

    def test_host_option_injection_blocked(self):
        # A host that looks like an ssh option must be refused.
        v = et.validate_exec_target(engagement(target={"host": "-oProxyCommand=touch /tmp/x"}))
        self.assertFalse(v["allowed"])
        self.assertTrue(any("host has an unsafe value" in e for e in v["errors"]))

    def test_user_option_injection_blocked(self):
        v = et.validate_exec_target(engagement(target={"user": "-oProxyCommand=x"}))
        self.assertFalse(v["allowed"])
        self.assertTrue(any("user has an unsafe value" in e for e in v["errors"]))

    def test_host_with_space_blocked(self):
        v = et.validate_exec_target(engagement(target={"host": "127.0.0.1 evil"}))
        self.assertFalse(v["allowed"])

    def test_invalid_port_blocked(self):
        for bad in (0, 70000, -1, True, "22"):
            v = et.validate_exec_target(engagement(target={"port": bad}))
            self.assertFalse(v["allowed"], f"port={bad!r}")


class ExecTargetSSHTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.eng_path = Path(self.tmp.name) / "e.yaml"
        import yaml
        self.eng_path.write_text(yaml.safe_dump(engagement()), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_build_ssh_argv_hardened_and_quoted(self):
        target = {"host": "127.0.0.1", "port": 2222, "user": "operator"}
        argv = et.build_ssh_argv(target, "/tmp/kh", ["nmap", "-sn", "127.0.0.1"])
        self.assertEqual(argv[0], "ssh")
        self.assertIn("BatchMode=yes", argv)
        self.assertIn("StrictHostKeyChecking=yes", argv)
        self.assertIn("UserKnownHostsFile=/tmp/kh", argv)
        self.assertIn("operator@127.0.0.1", argv)
        self.assertEqual(argv[-1], "nmap -sn 127.0.0.1")

    def test_build_ssh_argv_quotes_dangerous_token(self):
        target = {"host": "h", "port": 22, "user": "u"}
        argv = et.build_ssh_argv(target, "/tmp/kh", ["echo", "a; rm -rf /"])
        # The dangerous token is shlex-quoted into a single safe shell word.
        self.assertIn("'a; rm -rf /'", argv[-1])

    def test_run_remote_blocked_when_not_authorized(self):
        import yaml
        bad = Path(self.tmp.name) / "bad.yaml"
        bad.write_text(yaml.safe_dump(engagement(target={"authorized": False})), encoding="utf-8")
        with mock.patch.object(et, "verify_fingerprint") as vf:
            result = et.run_remote(str(bad), ["nmap", "-sn", "127.0.0.1"])
            self.assertEqual(result["status"], "blocked")
            vf.assert_not_called()  # never even reaches the network

    def test_run_remote_destructive_blocked(self):
        with mock.patch.object(et, "verify_fingerprint") as vf:
            # rm is not on the remote binary allowlist (also destructive).
            result = et.run_remote(str(self.eng_path), ["rm", "-rf", "/"])
            self.assertEqual(result["status"], "blocked")
            vf.assert_not_called()

    def test_run_remote_shell_wrapper_blocked(self):
        with mock.patch.object(et, "verify_fingerprint") as vf:
            result = et.run_remote(str(self.eng_path), ["sh", "-c", "rm -rf /"])
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("not allowed" in e for e in result["validation"]["errors"]))
            vf.assert_not_called()

    def test_run_remote_interpreter_blocked(self):
        with mock.patch.object(et, "verify_fingerprint") as vf:
            result = et.run_remote(str(self.eng_path), ["python3", "-c", "import os"])
            self.assertEqual(result["status"], "blocked")
            vf.assert_not_called()

    def test_run_remote_allowed_tool_passes_gate(self):
        # nmap is an allowlisted remote binary; should reach fingerprint stage.
        with mock.patch.object(et, "verify_fingerprint",
                               return_value={"matched": False, "reason": "x", "known_hosts_line": ""}) as vf:
            result = et.run_remote(str(self.eng_path), ["nmap", "-sn", "127.0.0.1"])
            self.assertEqual(result["status"], "fingerprint_mismatch")
            vf.assert_called_once()

    def test_verify_fingerprint_multiple_keys_one_matches(self):
        scan = ("[127.0.0.1]:2222 ssh-rsa AAAARSA\n"
                "[127.0.0.1]:2222 ssh-ed25519 AAAAED")
        def fake_fp(line):
            return PIN if "ed25519" in line else "SHA256:OTHER"
        with mock.patch.object(et, "scan_host_keys", return_value=scan), \
             mock.patch.object(et, "_fingerprint_of_line", side_effect=fake_fp):
            out = et.verify_fingerprint("127.0.0.1", 2222, PIN)
            self.assertTrue(out["matched"])
            self.assertIn("ed25519", out["known_hosts_line"])

    def test_run_remote_fingerprint_mismatch(self):
        with mock.patch.object(et, "verify_fingerprint",
                               return_value={"matched": False, "reason": "mismatch",
                                             "known_hosts_line": ""}):
            result = et.run_remote(str(self.eng_path), ["nmap", "-sn", "127.0.0.1"])
            self.assertEqual(result["status"], "fingerprint_mismatch")
            self.assertNotIn("execution", result)

    def test_run_remote_executes_on_match(self):
        with mock.patch.object(et, "verify_fingerprint",
                               return_value={"matched": True, "reason": "",
                                             "known_hosts_line": "[127.0.0.1]:2222 ssh-ed25519 AAAA"}), \
             mock.patch.object(et.tool_adapter, "execute",
                               return_value={"executed": True, "exit_code": 0,
                                             "stdout": "ok", "stderr": "", "timed_out": False}):
            result = et.run_remote(str(self.eng_path), ["nmap", "-sn", "127.0.0.1"])
            self.assertEqual(result["status"], "executed")
            self.assertEqual(result["execution"]["exit_code"], 0)

    def test_verify_fingerprint_matches(self):
        with mock.patch.object(et, "scan_host_keys",
                               return_value="[127.0.0.1]:2222 ssh-ed25519 AAAAKEY"), \
             mock.patch.object(et, "_fingerprint_of_line", return_value=PIN):
            out = et.verify_fingerprint("127.0.0.1", 2222, PIN)
            self.assertTrue(out["matched"])

    def test_verify_fingerprint_mismatch(self):
        with mock.patch.object(et, "scan_host_keys",
                               return_value="[127.0.0.1]:2222 ssh-ed25519 AAAAKEY"), \
             mock.patch.object(et, "_fingerprint_of_line", return_value="SHA256:OTHER"):
            out = et.verify_fingerprint("127.0.0.1", 2222, PIN)
            self.assertFalse(out["matched"])

    def test_verify_fingerprint_unreachable(self):
        with mock.patch.object(et, "scan_host_keys", return_value=""):
            out = et.verify_fingerprint("127.0.0.1", 2222, PIN)
            self.assertFalse(out["matched"])
            self.assertIn("could not retrieve", out["reason"])


if __name__ == "__main__":
    unittest.main()
