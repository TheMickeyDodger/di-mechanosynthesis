"""Tests for h2_phase_a_payload.py without any engine. Standard library unittest; run with python3 -I -B.

The pure check functions are exercised on synthetic, fixture-marked observation dictionaries. The ordering tests run
the payload's run() in a subprocess against a fixture stand-in named psi4 that exists only in the test's temporary
directory; they fail closed unless that name resolves there. No value here is a scientific value.
"""
import hashlib
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

TESTS = os.path.dirname(os.path.abspath(__file__))
PHASE_A = os.path.dirname(TESTS)
MARK = "FIXTURE"
spec = importlib.util.spec_from_file_location("h2_phase_a_payload", os.path.join(PHASE_A, "h2_phase_a_payload.py"))
P = importlib.util.module_from_spec(spec)
spec.loader.exec_module(P)
with open(os.path.join(PHASE_A, "h2-a-01-input.json")) as _fh:
    INP = json.load(_fh)
PRE = "/FIXTURE/prefix"
CORE = os.path.join(PRE, P.CORE_REL)
LIBINT = os.path.join(PRE, "lib", "libint2.dylib")
LAUNCH = {"prefix_realpath": PRE, "interpreter_realpath": PRE + "/bin/python3.14",
          "expected_sha256": {P.CORE_REL: "c" * 64, "lib/libint2.dylib": "d" * 64,
                              "share/psi4/basis/sto-3g.gbs": "e" * 64}}


def identity_obs(**over):
    obs = {"version": INP["expected_engine_version"], "module_file": PRE + "/lib/python3.14/site-packages/psi4/__init__.py",
           "core_file": CORE, "datadir_realpath": PRE + "/share/psi4",
           "loaded_images": [{"path": "/usr/lib/FIXTURE.dylib", "realpath": "/usr/lib/FIXTURE.dylib"},
                             {"path": CORE, "realpath": CORE, "sha256": "c" * 64},
                             {"path": "@rpath/libint2.dylib", "realpath": LIBINT, "sha256": "d" * 64}]}
    obs.update(over)
    return obs


def molecule_obs():
    return {"natom": 2, "molecular_charge": 0, "multiplicity": 1, "electrons": 2, "units": "Bohr", "point_group": "c1",
            "com_fixed": True, "orientation_fixed": True,
            "atoms": [{"label": "H1", "symbol": "H", "xyz_bohr": [0.0, 0.0, -0.7]},
                      {"label": "H2", "symbol": "H", "xyz_bohr": [0.0, 0.0, 0.7]}]}


def settings_obs():
    return {"options": P.expected_scf_options(INP), "changed": {k: True for k in P.SCF_KEYS}, "threads": 1,
            "memory_bytes": 524288000, "memory_set_bytes": 524288000}


def banner(**over):
    f = {"program": "Psi4: An Open-Source Ab Initio Electronic Structure Package",
         "version": "Psi4 " + INP["expected_engine_version"] + " FIXTURE-release", "PSIDATADIR": PRE + "/share/psi4",
         "Memory": "500.0 MiB", "Threads": "1"}
    f.update(over)
    lines = ["    FIXTURE banner text, synthetic", "      " + f["program"], "            " + f["version"], ""]
    lines += [f"    {k}: {v}" for k, v in f.items() if k in ("PSIDATADIR", "Memory", "Threads") and v is not None]
    return "\n".join(lines) + "\n"


class TestPureChecks(unittest.TestCase):
    def test_environment(self):
        launch_env = {"PATH": "FIXTURE", "TMPDIR": "FIXTURE"}
        self.assertEqual(P.check_environment(dict(launch_env, __CF_USER_TEXT_ENCODING="FIXTURE"), launch_env,
                                             ["__CF_USER_TEXT_ENCODING"]), [])
        self.assertIn("environment: undeclared name PSIPATH",
                      P.check_environment(dict(launch_env, PSIPATH="FIXTURE"), launch_env, ["__CF_USER_TEXT_ENCODING"]))
        self.assertTrue(P.check_environment({"PATH": "FIXTURE"}, launch_env, []))
        self.assertTrue(P.check_environment({"PATH": "other", "TMPDIR": "FIXTURE"}, launch_env, []))

    def test_interpreter(self):
        ok = {"isolated": 1, "dont_write_bytecode": 1, "executable_realpath": LAUNCH["interpreter_realpath"],
              "prefix_realpath": PRE}
        self.assertEqual(P.check_interpreter(ok, LAUNCH), [])
        for key, val in (("isolated", 0), ("dont_write_bytecode", 0), ("executable_realpath", "/usr/bin/FIXTURE"),
                         ("prefix_realpath", "/FIXTURE/x")):
            self.assertTrue(P.check_interpreter(dict(ok, **{key: val}), LAUNCH), key)

    def test_static_rehash(self):
        with tempfile.TemporaryDirectory() as tmp:
            pre = os.path.realpath(tmp)
            exp = {}
            for rel in P.REHASH:
                os.makedirs(os.path.dirname(os.path.join(pre, rel)), exist_ok=True)
                with open(os.path.join(pre, rel), "wb") as fh:
                    fh.write(b"FIXTURE " + rel.encode())
                exp[rel] = hashlib.sha256(b"FIXTURE " + rel.encode()).hexdigest()
            launch = {"prefix_realpath": pre, "expected_sha256": exp}
            self.assertEqual(P.check_static_rehash(launch)[0], [])
            with open(os.path.join(pre, "lib/libint2.dylib"), "ab") as fh:
                fh.write(b"changed")
            self.assertEqual(P.check_static_rehash(launch)[0], ["static: lib/libint2.dylib digest differs from the launch binding"])
            os.unlink(os.path.join(pre, "lib/libint2.dylib"))
            os.symlink(os.path.join(TESTS, "test_payload.py"), os.path.join(pre, "lib/libint2.dylib"))
            self.assertIn("static: lib/libint2.dylib resolves outside the bound prefix", P.check_static_rehash(launch)[0])
            del exp[P.CORE_REL]
            self.assertIn(f"static: no bound digest for {P.CORE_REL}", P.check_static_rehash(launch)[0])

    def test_engine_identity(self):
        self.assertEqual(P.check_engine_identity(identity_obs(), INP, LAUNCH), [])
        cases = {
            "version": identity_obs(version="FIXTURE-other"),
            "libint outside": identity_obs(loaded_images=[{"path": CORE, "realpath": CORE, "sha256": "c" * 64},
                                                          {"path": "/opt/FIXTURE/libint2.dylib", "realpath": "/opt/FIXTURE/libint2.dylib"}]),
            "no libint": identity_obs(loaded_images=[{"path": CORE, "realpath": CORE, "sha256": "c" * 64}]),
            "libint digest": identity_obs(loaded_images=[{"path": CORE, "realpath": CORE, "sha256": "c" * 64},
                                                         {"path": LIBINT, "realpath": LIBINT, "sha256": "0" * 64}]),
            "core digest": identity_obs(loaded_images=[{"path": CORE, "realpath": CORE, "sha256": "0" * 64},
                                                       {"path": LIBINT, "realpath": LIBINT, "sha256": "d" * 64}]),
            "no images": identity_obs(loaded_images=[]),
            "module outside": identity_obs(module_file="/FIXTURE/elsewhere/psi4/__init__.py"),
            "module inside but not the package file": identity_obs(module_file=PRE + "/lib/python3.14/site-packages/psi4/FIXTURE.py"),
            "datadir": identity_obs(datadir_realpath="/FIXTURE/other/share/psi4"),
        }
        for name, obs in cases.items():
            self.assertTrue(P.check_engine_identity(obs, INP, LAUNCH), name)

    def test_settings_molecule_basis_and_nuclear_repulsion(self):
        self.assertEqual(P.check_settings(settings_obs(), INP), [])
        bad = settings_obs()
        bad["options"]["guess"] = "SAD"
        self.assertIn("setting: guess read back differs", P.check_settings(bad, INP))
        bad = settings_obs()
        bad["changed"]["maxiter"] = False
        self.assertTrue(P.check_settings(bad, INP))
        self.assertTrue(P.check_settings(dict(settings_obs(), memory_bytes=1), INP))
        self.assertEqual(P.check_molecule(molecule_obs(), INP), [])
        for key, val in (("units", "Angstrom"), ("point_group", "d2h"), ("com_fixed", False), ("multiplicity", 3),
                         ("molecular_charge", 1), ("electrons", 1), ("natom", 3)):
            self.assertTrue(P.check_molecule(dict(molecule_obs(), **{key: val}), INP), key)
        moved = molecule_obs()
        moved["atoms"][1]["xyz_bohr"] = [0.0, 0.0, 0.70001]
        self.assertTrue(P.check_molecule(moved, INP))
        swapped = molecule_obs()
        swapped["atoms"][0]["label"] = "H2"
        self.assertTrue(P.check_molecule(swapped, INP))
        base = {"basis_file_realpath": PRE + "/share/psi4/basis/sto-3g.gbs", "basis_file_sha256": "e" * 64,
                "cwd_gbs_files": [], "nbf": 2}
        self.assertEqual(P.check_basis(base, INP, LAUNCH), [])
        for key, val in (("basis_file_realpath", "/FIXTURE/cwd/sto-3g.gbs"), ("basis_file_sha256", "0" * 64),
                         ("cwd_gbs_files", ["sto-3g.gbs"]), ("nbf", 3)):
            self.assertTrue(P.check_basis(dict(base, **{key: val}), INP, LAUNCH), key)
        tol = 1e-10
        self.assertEqual(P.check_nuclear_repulsion(1.0 / 1.4, INP, tol), [])  # the geometric identity 1/R, not an engine value
        self.assertEqual(P.check_nuclear_repulsion(None, INP, tol), ["nuclear repulsion: missing"])
        self.assertEqual(P.check_nuclear_repulsion(math.nan, INP, tol), ["nuclear repulsion: nonfinite"])
        self.assertEqual(P.check_nuclear_repulsion(1.0 / 1.4 + 2e-10, INP, tol),
                         ["nuclear repulsion: differs from 1/R beyond tolerance"])

    def test_banner(self):
        self.assertEqual(P.check_banner(banner(), INP, LAUNCH), [])
        self.assertEqual(P.check_banner("", INP, LAUNCH), ["banner: missing"])
        self.assertIn("banner: version line missing or differs",
                      P.check_banner(banner(version="Psi4 FIXTURE-0.0"), INP, LAUNCH))
        self.assertIn("banner: program line missing", P.check_banner(banner(program="FIXTURE other program"), INP, LAUNCH))
        self.assertIn("banner: PSIDATADIR missing or not <PREFIX>/share/psi4",
                      P.check_banner(banner(PSIDATADIR="/FIXTURE/elsewhere"), INP, LAUNCH))
        self.assertIn("banner: thread line missing or differs", P.check_banner(banner(Threads="4"), INP, LAUNCH))
        self.assertIn("banner: memory line missing or differs", P.check_banner(banner(Memory=None), INP, LAUNCH))
        self.assertEqual(P.sizeof_fmt(524288000), "500.0 MiB")

    def test_molrec_from_input(self):
        rec = P.build_molrec(INP)
        self.assertEqual([e + l for e, l in zip(rec["elem"], rec["elbl"])], ["H1", "H2"])
        self.assertEqual(rec["geom"], [0.0, 0.0, -0.7, 0.0, 0.0, 0.7])
        self.assertEqual((rec["units"], rec["fix_com"], rec["fix_orientation"], rec["fix_symmetry"]), ("Bohr", True, True, "c1"))
        self.assertEqual((rec["molecular_charge"], rec["molecular_multiplicity"]), (0.0, 1))
        self.assertEqual(P.expected_scf_options(INP)["df_scf_guess"], 0)
        self.assertEqual(P.expected_scf_options(INP)["basis"], "STO-3G")


class TestOrderingWithFixtureStandIn(unittest.TestCase):
    """The payload stops at I1 on a loaded-identity problem before any setting, molecule, basis or energy call."""

    def setUp(self):
        self.assertIsNone(importlib.util.find_spec("psi4"), "a psi4 module is importable by the test interpreter")
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        tmp = os.path.realpath(self._tmp.name)
        self.fixture_root = os.path.join(tmp, "fixture-modules")
        os.makedirs(os.path.join(self.fixture_root, "psi4"))
        shutil.copyfile(os.path.join(TESTS, "fixture-fake-psi4-init.py"),
                        os.path.join(self.fixture_root, "psi4", "__init__.py"))
        self.prefix = os.path.join(tmp, "fake-prefix")
        expected = {}
        for rel in P.REHASH:
            os.makedirs(os.path.dirname(os.path.join(self.prefix, rel)), exist_ok=True)
            with open(os.path.join(self.prefix, rel), "wb") as fh:
                fh.write(b"FIXTURE " + rel.encode())
            expected[rel] = hashlib.sha256(b"FIXTURE " + rel.encode()).hexdigest()
        self.attempt = os.path.join(tmp, "attempt")
        os.makedirs(os.path.join(self.attempt, "payload"))
        self.log = os.path.join(tmp, "calls.jsonl")
        inp = dict(INP, expected_engine_version="FIXTURE-1.11", fixture=MARK)
        self.input = os.path.join(tmp, "input.json")
        with open(self.input, "w") as fh:
            json.dump(inp, fh)
        self.env = {"LC_ALL": "C", "FIXTURE_CALL_LOG": self.log}
        self.launch = {"prefix_realpath": self.prefix, "interpreter_realpath": os.path.realpath(sys.executable),
                       "expected_sha256": expected, "platform_injected": ["__CF_USER_TEXT_ENCODING"],
                       "nuclear_repulsion_abs_tol_hartree": 1e-10, "fixture": MARK}

    def run_payload(self, mode):
        env = dict(self.env, FIXTURE_PSI4_MODE=mode)
        with open(os.path.join(self.attempt, "launch-record.json"), "w") as fh:
            json.dump(dict(self.launch, environment=env), fh)
        res = subprocess.run([sys.executable, "-I", "-B", os.path.join(TESTS, "fixture-ordering-harness.py"), self.fixture_root,
                              os.path.join(PHASE_A, "h2_phase_a_payload.py"), self.input, self.attempt, self.prefix],
                             env=env, capture_output=True, text=True, timeout=60)
        self.assertNotIn(res.returncode, (97, 98), "fixture isolation check failed; payload not run")
        with open(self.log) as fh:
            events = [json.loads(line)["event"] for line in fh]
        return res, events

    def assert_stopped_at_i1(self, res, events, needle):
        self.assertEqual(res.returncode, P.STOP_BEFORE_ENERGY_EXIT, res.stderr)
        out = os.path.join(self.attempt, "payload")
        with open(os.path.join(out, "stop-before-energy.json")) as fh:
            stop = json.load(fh)
        self.assertEqual(stop["stage"], "I1-loaded-identity")
        self.assertFalse(stop["energy_called"])
        self.assertTrue(any(needle in p for p in stop["problems"]), stop["problems"])
        self.assertEqual(sorted(os.listdir(out)), ["i1-identity.json", "pre-import.json", "stop-before-energy.json"])
        with open(os.path.join(out, "pre-import.json")) as fh:
            self.assertEqual(json.load(fh)["problems"], [])
        self.assertEqual(events[0], "import")
        self.assertEqual([e for e in events if e.startswith("CALLED:")], [])
        self.assertLessEqual(set(events), {"import", "get_datadir"})

    def test_version_mismatch_stops_at_i1(self):
        res, events = self.run_payload("version_mismatch")
        self.assert_stopped_at_i1(res, events, "identity: engine version string differs")

    def test_missing_libint_image_stops_at_i1(self):
        res, events = self.run_payload("version_match")
        self.assert_stopped_at_i1(res, events, "identity: no Libint library among loaded images")
        with open(os.path.join(self.attempt, "payload", "stop-before-energy.json")) as fh:
            self.assertNotIn("identity: engine version string differs", json.load(fh)["problems"])


if __name__ == "__main__":
    unittest.main()
