"""Control-boundary tests for h2_phase_a_driver.py. Standard library unittest; run with python3 -I -B (no bytecode
written into the repository tree), for example:
  TMPDIR=<private temp> python3 -I -B -m unittest discover -s <this directory> -t <this directory> -v

Every test works in a temporary tree: a copy of the bundle, a fake prefix whose "interpreter" is the fixture script
fixture-fake-interpreter.py, and a runs root. No engine is imported or executed, no real prefix is touched, and every
record a fake writes carries a FIXTURE marker and non-physical sentinel numbers. The network gate is satisfied only by
patching the module's observer with a fixture inside the test process; the shipped driver has no observer.
"""
import base64
import contextlib
import hashlib
import importlib.util
import io
import json
import os
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

TESTS = os.path.dirname(os.path.abspath(__file__))
PHASE_A = os.path.dirname(TESTS)
H2 = os.path.dirname(PHASE_A)
MARK = "FIXTURE - test value, not a scientific value"
SP = "lib/python3.14/site-packages/"
PREFIX_FILES = {"include/libint2/shell.h": b"FIXTURE shell.h\n", "share/psi4/basis/sto-3g.gbs": b"FIXTURE basis\n",
                "lib/libint2.dylib": b"FIXTURE libint\n", SP + "psi4/core.cpython-314-darwin.so": b"FIXTURE core\n"}


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tree_digest(root):
    out = {}
    for d, _, files in os.walk(root):
        for f in files:
            p = os.path.join(d, f)
            out[os.path.relpath(p, root)] = sha(p)
    return out


def jload(path):
    with open(path) as fh:
        return json.load(fh)


def jdump(obj, path):
    with open(path, "w") as fh:
        json.dump(obj, fh)


def offline():
    return {"offline": True, "fixture": MARK}


FIXTURE_COMMIT = "fa11" * 10  # FIXTURE commit id (hex only): not a commit of any repository


def git_blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def fixture_git(head=FIXTURE_COMMIT, fail=None, tree=None, bad_blob=False):
    """FIXTURE stand-in for the driver's read-only Git reader. No repository is read, created or changed."""
    tree = tree or {}

    def reader(repo, *args):
        assert args[0] in ("rev-parse", "ls-tree", "cat-file"), args
        if fail == args[0]:
            return 128, b""
        if args[0] == "rev-parse":
            return 0, (head + "\n").encode()
        if args[0] == "ls-tree":
            rel = args[-1]
            return (0, f"100644 blob {git_blob_id(tree[rel])}\t{rel}\0".encode()) if rel in tree else (0, b"")
        for data in tree.values():
            if git_blob_id(data) == args[-1]:
                return 0, (data + b"FIXTURE altered") if bad_blob else data
        return 128, b""
    return reader


class Case:
    def __init__(self, tmp, mode="complete", wall=None):
        self.tmp = tmp
        self.root = os.path.join(tmp, "case")
        os.makedirs(os.path.join(self.root, ".git"))  # marks the copied tree as a repository for the runs-root rule
        self.bundle = os.path.join(self.root, "docs", "learning", "h2", "phase-a")
        os.makedirs(self.bundle)
        params = os.path.join(self.root, "docs", "learning", "h2", "h2-method-parameters.json")
        if wall is None:
            shutil.copyfile(os.path.join(H2, "h2-method-parameters.json"), params)
        else:
            p = jload(os.path.join(H2, "h2-method-parameters.json"))
            p["resource_bounds"]["wall_seconds_per_job"] = wall
            p["fixture"] = MARK
            jdump(p, params)
        for name in ("h2_phase_a_driver.py", "h2_phase_a_payload.py", "h2-a-01-input.json"):
            shutil.copyfile(os.path.join(PHASE_A, name), os.path.join(self.bundle, name))
        for name in ("H2-A-01-RUN-PROPOSAL.md", "H2-A-01-DECISION-PACKET.md"):
            with open(os.path.join(self.bundle, name), "w") as fh:
                fh.write(f"{MARK}: placeholder for {name}\n")
        self.prefix = os.path.join(tmp, "prefix")
        for rel, data in PREFIX_FILES.items():
            os.makedirs(os.path.dirname(os.path.join(self.prefix, rel)), exist_ok=True)
            with open(os.path.join(self.prefix, rel), "wb") as fh:
                fh.write(data)
        os.makedirs(os.path.join(self.prefix, "bin"))
        self.interp = os.path.join(self.prefix, "bin", "python3.14")
        with open(self.interp, "w") as fh:
            with open(os.path.join(TESTS, "fixture-fake-interpreter.py")) as src:
                fh.write(f"#!{sys.executable} -I\n" + src.read())
        os.chmod(self.interp, 0o755)
        os.symlink("python3.14", os.path.join(self.prefix, "bin", "python3"))
        real_ident = jload(os.path.join(PHASE_A, "h2-a-01-static-identity.json"))
        os.makedirs(os.path.join(self.prefix, "conda-meta"))
        for fields in real_ident["preflight_expectations"]["package_records"].values():
            rec = dict(fields, fixture=MARK)
            jdump(rec, os.path.join(self.prefix, "conda-meta",
                                    f"{fields['name']}-{fields['version']}-{fields['build']}.json"))
        self.set_mode(mode)
        ident = dict(real_ident, fixture=MARK)
        ident["preflight_expectations"] = dict(real_ident["preflight_expectations"])
        ident["preflight_expectations"]["sha256"] = {rel: sha(os.path.join(self.prefix, rel))
                                                     for rel in list(PREFIX_FILES) + ["bin/python3.14"]}
        jdump(ident, os.path.join(self.bundle, "h2-a-01-static-identity.json"))
        self.runs = os.path.join(self.root, ".herd", "runs")
        os.makedirs(self.runs)
        self.attempt = os.path.join(self.runs, "H2-A-01")
        self.drv = self.load()

    def set_mode(self, mode):
        with open(os.path.join(self.prefix, "FIXTURE-MODE"), "w") as fh:
            fh.write(mode)

    def load(self, observer=offline):
        spec = importlib.util.spec_from_file_location(f"drv_{id(self)}", os.path.join(self.bundle, "h2_phase_a_driver.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.NETWORK_OBSERVER = observer
        mod.GIT_READ = fixture_git()
        return mod

    def base(self, mode="preflight"):
        return [mode, "--interpreter", self.interp, "--prefix", self.prefix, "--runs-root", self.runs]

    def provenance(self, record=None):
        os.makedirs(os.path.join(self.root, ".herd", "auth"), exist_ok=True)
        path = os.path.join(self.root, ".herd", "auth", "code-provenance.json")
        with open(path, "w") as fh:
            json.dump(record if record is not None else self.drv.build_provenance(), fh, indent=1, sort_keys=True)
        return path

    def authorization(self, mutate=None, provenance=None):
        os.makedirs(os.path.join(self.root, ".herd", "auth"), exist_ok=True)
        prov_path = provenance or self.provenance()
        mb_path = os.path.join(self.root, ".herd", "auth", "machine-binding.json")
        cmd = shlex.join(self.drv.command_for(self.interp, self.attempt))
        mb = {"interpreter": self.interp, "prefix": self.prefix, "runs_root": self.runs, "command": cmd, "fixture": MARK}
        if mutate:
            mutate(None, mb)
        with open(mb_path, "w") as fh:
            json.dump(mb, fh)
        digests = {k: sha(os.path.join(self.bundle, rel)) for k, rel in self.drv.BUNDLE.items()}
        digests["machine_binding"] = sha(mb_path)
        digests["code_provenance"] = sha(prov_path)
        auth = {"schema": "di-mechanosynthesis/h2-phase-a-authorization/1", "job_id": "H2-A-01", "max_attempts": 1,
                "authorized_by": MARK, "authorized_utc": MARK, "statement": MARK + " - this is not an authorization",
                "bound_sha256": digests, "machine_binding_path": mb_path, "code_provenance_path": prov_path,
                "interpreter": self.interp,
                "prefix": self.prefix, "runs_root": self.runs,
                "expected_static_sha256": jload(os.path.join(self.bundle, "h2-a-01-static-identity.json"))
                ["preflight_expectations"]["sha256"],
                "environment": self.drv.build_environment(os.path.realpath(self.prefix), os.path.join(self.attempt, "scratch"))}
        if mutate:
            mutate(auth, None)
        path = os.path.join(self.root, ".herd", "auth", "authorization.json")
        with open(path, "w") as fh:
            json.dump(auth, fh)
        return path

    def main(self, argv, drv=None):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = (drv or self.drv).main(argv)
        return code, json.loads(buf.getvalue())

    def run(self, mutate=None, provenance=None):
        return self.main(self.base("run") + ["--authorization", self.authorization(mutate, provenance)])

    def outcome(self):
        return jload(os.path.join(self.attempt, "outcome.json"))


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def failed_checks(self, out):
        return {c["id"]: c["detail"] for c in out["report"]["checks"] if c["status"] == "FAIL"}


class TestUsage(Base):
    def cli(self, case, args):
        return subprocess.run([sys.executable, "-I", os.path.join(case.bundle, "h2_phase_a_driver.py")] + args,
                              capture_output=True, text=True, timeout=60)

    def test_no_arguments_unknown_and_missing_binding_are_usage_errors(self):
        case = Case(self.tmp)
        before = tree_digest(case.root), tree_digest(case.prefix)
        for args in ([], ["frobnicate"], case.base() + ["--unknown"], case.base("run"),
                     ["run", "--interpreter", case.interp, "--authorization", "x"]):
            res = self.cli(case, args)
            self.assertEqual(res.returncode, 64, args)
            self.assertEqual(res.stdout, "", args)
        self.assertEqual((tree_digest(case.root), tree_digest(case.prefix)), before)
        self.assertEqual(os.listdir(case.runs), [])

    def test_shipped_driver_blocks_on_unresolved_network_prerequisite(self):
        case = Case(self.tmp)
        res = self.cli(case, case.base("run") + ["--authorization", case.authorization()])
        self.assertEqual(res.returncode, 2)
        out = json.loads(res.stdout)
        self.assertEqual(out["tier"], "BLOCK_LAUNCH")
        self.assertIn("NETWORK_PREREQUISITE_UNRESOLVED", json.dumps(out))
        self.assertEqual(os.listdir(case.runs), [])


class TestPreflight(Base):
    def test_preflight_passes_on_fixture_and_spawns_no_process_or_file(self):
        case = Case(self.tmp)
        before = tree_digest(case.root)

        def boom(*a, **k):
            raise AssertionError("preflight attempted to spawn a process")
        names = ["fork", "forkpty", "posix_spawn", "posix_spawnp", "system", "popen", "execv", "execve", "spawnv",
                 "spawnve"]
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(subprocess, "Popen", boom))
            for n in names:
                if hasattr(os, n):
                    stack.enter_context(mock.patch.object(os, n, boom))
            code, out = case.main(case.base())
        self.assertEqual(code, 0, self.failed_checks(out))
        self.assertEqual(out["tier"], "PASS")
        self.assertEqual(tree_digest(case.root), before)

    def test_network_gate_logic(self):
        case = Case(self.tmp)
        for observer, reason in ((None, "NETWORK_PREREQUISITE_UNRESOLVED"),
                                 (lambda: {"offline": False, "fixture": MARK}, "HOST_NOT_OFFLINE"),
                                 (lambda: "offline", "HOST_NOT_OFFLINE")):
            code, out = case.main(case.base(), case.load(observer))
            self.assertEqual(code, 2)
            self.assertEqual(self.failed_checks(out), {"network.prerequisite": reason})
        self.assertEqual(case.main(case.base(), case.load(offline))[0], 0)

    def check_fails(self, case, check_id, argv=None):
        code, out = case.main(argv or case.base())
        self.assertEqual(code, 2)
        self.assertEqual(out["tier"], "BLOCK_LAUNCH")
        self.assertIn(check_id, self.failed_checks(out))
        return out

    def test_each_static_digest_mismatch_blocks(self):
        for rel in list(PREFIX_FILES) + ["bin/python3.14"]:
            with self.subTest(rel=rel), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp)
                with open(os.path.join(case.prefix, rel), "ab") as fh:
                    fh.write(b"FIXTURE changed\n")
                self.check_fails(case, f"sha256.{rel}")

    def test_package_record_mismatches_block(self):
        for pkg, field, value in (("psi4", "build_number", 2), ("psi4", "sha256", "0" * 64), ("libint", "version", "2.8.1"),
                                  ("libint", "channel", "FIXTURE-other"), ("psi4", "subdir", "osx-64")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp)
                name = [n for n in os.listdir(os.path.join(case.prefix, "conda-meta")) if n.startswith(pkg + "-")][0]
                path = os.path.join(case.prefix, "conda-meta", name)
                rec = jload(path)
                rec[field] = value
                jdump(rec, path)
                self.check_fails(case, f"package.{pkg}")

    def test_links_leaving_the_prefix_block(self):
        case = Case(self.tmp)
        outside = os.path.join(self.tmp, "outside.dylib")
        shutil.move(os.path.join(case.prefix, "lib/libint2.dylib"), outside)
        os.symlink(outside, os.path.join(case.prefix, "lib/libint2.dylib"))
        self.check_fails(case, "sha256.lib/libint2.dylib")
        case2 = Case(os.path.join(self.tmp, "b"))
        os.unlink(case2.interp)
        os.symlink(sys.executable, case2.interp)
        self.check_fails(case2, "interpreter.inside_prefix")

    def test_interpreter_must_be_the_bound_one(self):
        case = Case(self.tmp)
        other = os.path.join(case.prefix, "bin", "python-other")
        shutil.copyfile(case.interp, other)
        argv = case.base()
        argv[argv.index("--interpreter") + 1] = other
        self.check_fails(case, "interpreter.inside_prefix", argv)

    def test_input_inconsistent_with_parameters_blocks(self):
        for path, value in ((("molecule", "R_bohr"), 1.5), (("engine_options", "maxiter"), 51),
                            (("engine_options", "df_scf_guess"), True), (("molecule", "charge"), 1),
                            (("molecule_options", "no_com"), False), (("memory",), "600 MiB")):
            with self.subTest(path=path), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp)
                p = os.path.join(case.bundle, "h2-a-01-input.json")
                inp = jload(p)
                tgt = inp
                for k in path[:-1]:
                    tgt = tgt[k]
                tgt[path[-1]] = value
                jdump(inp, p)
                self.check_fails(case, "input.matches_parameters")

    def test_location_attempt_and_space_checks(self):
        case = Case(self.tmp)
        public = os.path.join(case.root, "results")
        os.makedirs(public)
        argv = case.base()
        argv[argv.index("--runs-root") + 1] = public
        self.check_fails(case, "runs_root.location", argv)
        inside = os.path.join(case.prefix, "runs")
        os.makedirs(inside)
        argv[argv.index("--runs-root") + 1] = inside
        self.check_fails(case, "runs_root.location", argv)
        argv = case.base()
        argv[argv.index("--prefix") + 1] = case.prefix + "/bin/.."
        self.check_fails(case, "prefix.absolute_normalized", argv)
        with mock.patch.object(shutil, "disk_usage", lambda p: shutil._ntuple_diskusage(10, 10, 1024)):
            self.check_fails(case, "free_space.floor")
        os.mkdir(case.attempt)
        self.check_fails(case, "attempt.absent")


class TestAuthorization(Base):
    def blocked(self, case, mutate, needle):
        code, out = case.run(mutate)
        self.assertEqual(code, 2, out)
        self.assertEqual(out["tier"], "BLOCK_LAUNCH")
        self.assertIn(needle, json.dumps(out))
        self.assertEqual(os.listdir(case.runs), [], "nothing may be written on BLOCK_LAUNCH")

    def test_each_binding_mismatch_blocks(self):
        case = Case(self.tmp)
        keys = sorted(case.drv.BOUND_KEYS)
        for key in keys:
            with self.subTest(key=key):
                self.blocked(case, lambda a, m, key=key: a and a["bound_sha256"].__setitem__(key, "0" * 64),
                             f"bound_sha256.{key}")

        def drop(a, m):
            if a:
                del a["bound_sha256"]["decision_packet"]
        self.blocked(case, drop, "bound_sha256 keys")
        for field, value, needle in (("job_id", "H2-B-01", "job_id"), ("max_attempts", 2, "max_attempts"),
                                     ("statement", " ", "statement"), ("schema", "x", "schema"),
                                     ("interpreter", "/elsewhere", "interpreter"), ("prefix", "/elsewhere", "prefix"),
                                     ("runs_root", "/elsewhere", "runs_root")):
            with self.subTest(field=field):
                self.blocked(case, lambda a, m, f=field, v=value: a and a.__setitem__(f, v), needle)

    def test_static_digest_environment_and_command_bindings(self):
        case = Case(self.tmp)
        self.blocked(case, lambda a, m: a and a["expected_static_sha256"].__setitem__("lib/libint2.dylib", "0" * 64),
                     "expected_static_sha256")
        self.blocked(case, lambda a, m: a and a["environment"].__setitem__("PSIPATH", "/elsewhere"),
                     "environment: undeclared key")
        self.blocked(case, lambda a, m: a and a["environment"].__setitem__("OMP_NUM_THREADS", "4"), "environment")
        self.blocked(case, lambda a, m: m and m.__setitem__("command", "FIXTURE other command"),
                     "machine_binding.command")
        self.blocked(case, lambda a, m: a and a.__setitem__("machine_binding_path", "/nonexistent"),
                     "bound_sha256.machine_binding")


class TestCodeProvenance(Base):
    def blocked(self, case, needle, mutate=None, provenance=None):
        code, out = case.run(mutate, provenance)
        self.assertEqual((code, out["tier"]), (2, "BLOCK_LAUNCH"), out)
        self.assertIn(needle, json.dumps(out))
        self.assertEqual(os.listdir(case.runs), [], "nothing may be written on BLOCK_LAUNCH")

    def test_record_covers_the_run_code_paths_with_resolvable_diffs(self):
        case = Case(self.tmp)
        base = b"FIXTURE base text\n"
        rel_payload = os.path.relpath(os.path.join(case.bundle, "h2_phase_a_payload.py"), case.root)
        case.drv.GIT_READ = fixture_git(tree={rel_payload: base})
        rec = case.drv.build_provenance()
        self.assertEqual(rec["base_commit"], FIXTURE_COMMIT)
        self.assertEqual([f["key"] for f in rec["files"]], list(case.drv.PROVENANCE_KEYS))
        self.assertEqual(rec["coverage"]["paths"], [f["path"] for f in rec["files"]])
        for f in rec["files"]:
            with open(os.path.join(case.root, f["path"]), "rb") as fh:
                cur = fh.read()
            self.assertEqual(f["current_sha256"], hashlib.sha256(cur).hexdigest())
            self.assertEqual(base64.b64decode(f["current_bytes_b64"]), cur)
            self.assertEqual(f["diff_sha256"], hashlib.sha256(f["diff_unified"].encode()).hexdigest())
            if f["path"] == rel_payload:
                self.assertTrue(f["base_present"])
                self.assertEqual(f["base_blob_sha1"], git_blob_id(base))
                self.assertTrue(f["diff_unified"].startswith("--- a/" + rel_payload))
            else:
                self.assertFalse(f["base_present"])
                self.assertTrue(f["diff_unified"].startswith("--- /dev/null"))
        self.assertEqual(case.drv.check_provenance(case.provenance(rec), sha(case.provenance(rec)),
                                                   {f["key"]: f["current_sha256"] for f in rec["files"]}), rec)

    def test_absent_provenance_blocks(self):
        case = Case(self.tmp)
        self.blocked(case, "code provenance absent", lambda a, m: a and a.pop("code_provenance_path"))
        self.blocked(case, "code provenance absent", lambda a, m: a and a.__setitem__("code_provenance_path", "/nonexistent"))

    def test_mismatched_provenance_blocks(self):
        case = Case(self.tmp)
        self.blocked(case, "code provenance digest differs",
                     lambda a, m: a and a["bound_sha256"].__setitem__("code_provenance", "0" * 64))
        rec = case.drv.build_provenance()
        rec["files"][1]["diff_unified"] += "+FIXTURE tampered line\n"
        self.blocked(case, "code provenance mismatch", provenance=case.provenance(rec))
        rec = case.drv.build_provenance()
        rec["files"][0]["base_blob_sha1"] = "0" * 40
        self.blocked(case, "code provenance mismatch", provenance=case.provenance(rec))
        stale = case.provenance(case.drv.build_provenance())
        case.drv.GIT_READ = fixture_git(head="dead" * 10)  # FIXTURE: HEAD moved after the record was made
        self.blocked(case, "code provenance mismatch", provenance=stale)

    def test_record_stale_after_code_change_blocks(self):
        case = Case(self.tmp)
        stale = case.provenance(case.drv.build_provenance())
        with open(os.path.join(case.bundle, "h2_phase_a_payload.py"), "a") as fh:
            fh.write("# FIXTURE change after the provenance record\n")
        self.blocked(case, "code provenance mismatch", provenance=stale)

    def test_unresolvable_provenance_blocks(self):
        case = Case(self.tmp)
        rel_payload = os.path.relpath(os.path.join(case.bundle, "h2_phase_a_payload.py"), case.root)
        prov = case.provenance(case.drv.build_provenance())
        for reader, needle in ((fixture_git(fail="rev-parse"), "unresolvable: HEAD"),
                               (fixture_git(fail="ls-tree"), "unresolvable: ls-tree"),
                               (fixture_git(tree={rel_payload: b"FIXTURE base\n"}, bad_blob=True), "unresolvable: base blob")):
            with self.subTest(needle=needle):
                case.drv.GIT_READ = reader
                self.blocked(case, needle, provenance=prov)
        case.drv.GIT_READ = fixture_git(fail="rev-parse")
        code, out = case.main(["code-provenance", "--out", os.path.join(self.tmp, "never-written.json")])
        self.assertEqual((code, out["code_provenance"]), (2, "NOT_WRITTEN"))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "never-written.json")))

    def test_real_git_reader_is_read_only(self):
        case = Case(self.tmp)
        with self.assertRaises(case.drv.Block):
            case.drv.git_read(case.root, "commit", "-m", "FIXTURE")  # refused before any process starts
        with self.assertRaises(case.drv.Block):
            case.drv.git_read(case.root, "update-index", "--refresh")
        real = case.drv.repo_root(TESTS)  # the repository holding these tests: read-only queries only
        if real is None or not shutil.which("git"):
            self.skipTest("no repository or git available")
        rc, head = case.drv.git_read(real, "rev-parse", "--verify", "HEAD^{commit}")
        self.assertEqual(rc, 0)
        rc, entry = case.drv.git_read(real, "ls-tree", "-z", head.decode().strip(), "--", "README.md")
        self.assertEqual(rc, 0)
        sha1 = entry.split(b"\t")[0].split()[2].decode()
        rc, data = case.drv.git_read(real, "cat-file", "blob", sha1)
        self.assertEqual((rc, case.drv.blob_id(data)), (0, sha1))


class TestLaunch(Base):
    def test_successful_fake_launch_records_everything(self):
        case = Case(self.tmp)
        os.environ["FIXTURE_LEAK_CHECK"] = MARK
        self.addCleanup(os.environ.pop, "FIXTURE_LEAK_CHECK", None)
        case.set_mode("env_dump")
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (0, "COMPLETED_PENDING_REVIEW"), out)
        o = case.outcome()
        proc = o["process"]
        for key in ("pid", "pgid", "start_utc", "end_utc", "elapsed_s", "peak_child_rss_raw"):
            self.assertIn(key, proc)
        self.assertEqual(proc["exit_code"], 0)
        self.assertFalse(proc["timed_out"])
        self.assertFalse(proc["group_members_after_exit"])
        self.assertIsInstance(o["free_bytes_before"], int)
        self.assertIsInstance(o["free_bytes_after"], int)
        files = {f["path"]: f for f in o["files"]}
        for rel in ("launch-record.json", "engine.stdout", "engine.stderr", "payload/result.json",
                    "payload/psi4-output.dat", "bundle/h2_phase_a_payload.py", "bundle/h2-a-01-input.json"):
            self.assertIn(rel, files)
            self.assertEqual(files[rel]["sha256"], sha(os.path.join(case.attempt, rel)))
        env = jload(os.path.join(case.attempt, "payload", "fixture-env.json"))
        self.assertLessEqual(set(env["names"]), set(case.drv.ALLOWED_ENV) | set(case.drv.PLATFORM_INJECTED))
        self.assertNotIn("FIXTURE_LEAK_CHECK", env["names"])
        self.assertEqual(os.path.realpath(env["cwd"]), os.path.realpath(os.path.join(case.attempt, "scratch")))
        launch = jload(os.path.join(case.attempt, "launch-record.json"))
        self.assertEqual(sorted(launch["environment"]), sorted(case.drv.ALLOWED_ENV))
        self.assertEqual(launch["command"][1:3], ["-I", "-B"])
        bound = jload(os.path.join(case.root, ".herd", "auth", "authorization.json"))["bound_sha256"]["code_provenance"]
        self.assertEqual(sha(os.path.join(case.attempt, "code-provenance.json")), bound)
        self.assertEqual(launch["code_provenance"]["sha256"], bound)
        self.assertEqual(launch["code_provenance"]["base_commit"], FIXTURE_COMMIT)
        for rel in case.drv.EXPECTED_OUTPUTS:
            self.assertIn(rel, files)
        self.assertEqual(o["reasons"], [])
        self.assertTrue(all(c["status"] == "PASS" for c in o["post_run_checks"]["checks"]))
        self.assertEqual(jload(os.path.join(case.attempt, "payload", "result.json"))["fixture"].split(" ")[0], "FIXTURE")

    def test_existing_attempt_blocks_relaunch_and_nothing_is_overwritten(self):
        case = Case(self.tmp)
        self.assertEqual(case.run()[0], 0)
        before = tree_digest(case.attempt)
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (2, "BLOCK_LAUNCH"))
        self.assertIn("attempt record", json.dumps(out))
        self.assertEqual(tree_digest(case.attempt), before)
        with self.assertRaises(FileExistsError):
            case.drv.write_exclusive(os.path.join(case.attempt, "outcome.json"), {"fixture": MARK})

    def test_tiers_from_fake_outcomes(self):
        expect = {"nonzero": ("FAILED", "nonzero exit 17"), "energy_failed": ("FAILED", "energy call failed"),
                  "stop": ("STOP_BEFORE_ENERGY", "FIXTURE identity problem"),
                  "stop_without_record": ("FAILED", "without a valid stop record"),
                  "nonfinite_energy": ("FAILED", "nonfinite energy"),
                  "missing_field": ("QUARANTINE", "scf_iterations is not a positive integer"),
                  "missing_nr": ("QUARANTINE", "missing reported nuclear repulsion"),
                  "nonfinite_nr": ("QUARANTINE", "nonfinite reported nuclear repulsion"),
                  "mismatch_nr": ("QUARANTINE", "differs from 1/R"),
                  "banner_lost": ("QUARANTINE", "printed banner"),
                  "modify_prefix": ("QUARANTINE", "prefix package records or bound files changed"),
                  "modify_record_build_number": ("QUARANTINE", "post-run check failed: package.psi4"),
                  "iterations_null": ("QUARANTINE", "scf_iterations is not a positive integer"),
                  "iterations_float": ("QUARANTINE", "scf_iterations is not a positive integer"),
                  "missing_log": ("QUARANTINE", "missing expected output: payload/psi4-output.log"),
                  "missing_output": ("QUARANTINE", "missing expected output: payload/psi4-output.dat"),
                  "stage_problems_only": ("QUARANTINE", "missing or mistyped i3-basis-geometry field"),
                  "result_list": ("QUARANTINE", "result record top level is list"),
                  "readback_string": ("QUARANTINE", "malformed post-energy read-back"),
                  "atoms_malformed": ("QUARANTINE", "atom count, coordinates or atom labels"),
                  "post_energy_error": ("QUARANTINE", "post-energy read-back incomplete"),
                  "stage_gate_failed": ("QUARANTINE", "i1-identity record not a passed I1-loaded-identity gate"),
                  "stop_inconsistent": ("FAILED", "consistent with the stage records")}
        for mode, (tier, needle) in expect.items():
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp, mode=mode)
                code, out = case.run()
                self.assertEqual(out["tier"], tier, out)
                self.assertEqual(code, case.drv.EXIT[tier])
                self.assertTrue(any(needle in r for r in out["reasons"]), out["reasons"])
                self.assertEqual(case.outcome()["tier"], tier)

    def test_stage_value_negatives_quarantine(self):
        """Each gate-defining stage value contradicting the launch or input binding gives QUARANTINE (preserved)."""
        expect = {
            "images_empty": "i1-identity: loaded-image list empty",
            "images_missing": "missing or mistyped i1-identity field: loaded_images",
            "image_entry_malformed": "i1-identity: malformed loaded-image entry",
            "core_image_absent": "i1-identity: core extension not among loaded images",
            "core_image_outside": "i1-identity: core extension not among loaded images",
            "core_image_digest_wrong": "i1-identity: loaded core extension digest differs",
            "libint_image_absent": "i1-identity: no Libint library among loaded images",
            "libint_image_outside": "i1-identity: a loaded Libint library is not <PREFIX>/lib/libint2.dylib",
            "libint_image_digest_wrong": "i1-identity: loaded Libint library digest differs",
            "module_outside": "i1-identity: module_file is not <PREFIX>/",
            "core_file_outside": "i1-identity: core_file is not <PREFIX>/",
            "datadir_outside": "i1-identity: datadir_realpath is not <PREFIX>/share/psi4",
            "env_value_changed": "pre-import: environment values differ: ['OMP_NUM_THREADS']",
            "env_key_added": "pre-import: undeclared environment names: ['PSIPATH']",
            "env_key_removed": "pre-import: environment names missing: ['TMPDIR']",
            "argv_wrong": "pre-import: argv differs from the bound command",
            "executable_mismatch": "pre-import: executable realpath differs from the bound interpreter",
            "prefix_mismatch": "pre-import: prefix realpath differs from the bound prefix",
            "cwd_wrong": "pre-import: working directory differs from the bound scratch",
            "modules_loaded_before_import": "pre-import: engine module loaded before import",
            "static_rehash_key_missing": "pre-import: static re-hash differs from the launch binding",
            "pre_import_digest_wrong": "pre-import: static re-hash differs from the launch binding",
            "charge_wrong": "i2-configuration: molecular_charge differs",
            "multiplicity_wrong": "i2-configuration: multiplicity differs",
            "electrons_wrong": "i2-configuration: electrons differs",
            "units_wrong": "i2-configuration: units differs",
            "point_group_wrong": "i2-configuration: point_group differs",
            "com_wrong": "i2-configuration: com_fixed differs",
            "orientation_wrong": "i2-configuration: orientation_fixed differs",
            "changed_flag_false": "i2-configuration: an option is not marked as changed by the user",
            "banner_bytes_wrong": "i2-configuration: banner digest or byte length differs",
            "banner_version_wrong": "i2-configuration: banner version line missing or differs",
            "banner_datadir_wrong": "i2-configuration: banner PSIDATADIR missing or not <PREFIX>/share/psi4",
            "i2_threads_wrong": "i2-configuration: threads or memory differ",
            "basis_path_outside": "i3-basis-geometry: basis file is not <PREFIX>/share/psi4/basis/sto-3g.gbs",
            "cwd_gbs_nonempty": "i3-basis-geometry: .gbs files present in the working directory",
            "nalpha_nbeta_unequal": "post-energy identity mismatch: electron count or spin",
            "iterations_raw_mismatch": "scf_iterations is not consistent with the raw reported value",
            "energy_utc_order_wrong": "energy return time precedes the energy call time",
        }
        for mode, needle in expect.items():
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp, mode=mode)
                code, out = case.run()
                self.assertEqual((code, out["tier"]), (5, "QUARANTINE"), out)
                self.assertTrue(any(needle in r for r in out["reasons"]), out["reasons"])
                o = case.outcome()
                self.assertEqual(o["tier"], "QUARANTINE")
                self.assertTrue(any(needle in r for r in o["reasons"]))

    def test_iteration_limit_boundaries(self):
        """The limit (maxiter 50) is evaluated independently of the raw-consistency check; both reasons are kept."""
        limit, mismatch = "iteration limit reached", "scf_iterations is not consistent with the raw reported value"
        raw_limit = "iteration limit reached by the raw reported value"
        expect = {"iter_49_match": (0, "COMPLETED_PENDING_REVIEW", []),
                  "iter_49_raw48": (5, "QUARANTINE", [mismatch]),
                  "iter_49_raw50": (4, "FAILED", [raw_limit, mismatch]),
                  "iter_50_match": (4, "FAILED", [limit]),
                  "iter_50_raw49": (4, "FAILED", [limit, mismatch]),
                  "iter_51_match": (4, "FAILED", [limit]),
                  "iter_51_raw49": (4, "FAILED", [limit, mismatch])}
        for mode, (code, tier, reasons) in expect.items():
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp, mode=mode)
                got_code, out = case.run()
                self.assertEqual((got_code, out["tier"], out["reasons"]), (code, tier, reasons))
                o = case.outcome()
                self.assertEqual((o["tier"], o["reasons"]), (tier, reasons))

    def test_stop_record_reports_its_stage(self):
        case = Case(self.tmp, mode="stop")
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (3, "STOP_BEFORE_ENERGY"), out)
        self.assertEqual(out["reasons"][:2], ["stopped at I1-loaded-identity", "FIXTURE identity problem"])

    def test_record_content_change_is_detected_and_checks_preserved(self):
        case = Case(self.tmp, mode="modify_record_build_number")
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (5, "QUARANTINE"), out)
        o = case.outcome()
        failed = {c["id"] for c in o["post_run_checks"]["checks"] if c["status"] == "FAIL"}
        self.assertEqual(failed, {"package.psi4"})
        self.assertTrue(any("conda-meta/psi4-1.11-py314h53d0584_1.json" in r for r in o["reasons"]), o["reasons"])

    def test_classification_never_raises(self):
        case = Case(self.tmp)
        exp = case.drv.derive_expected(jload(os.path.join(H2, "h2-method-parameters.json")))
        inp = jload(os.path.join(case.bundle, "h2-a-01-input.json"))
        attempt = os.path.join(self.tmp, "attempt")
        os.makedirs(os.path.join(attempt, "payload"))
        bodies = ['["FIXTURE"]', '"FIXTURE"', '{"stage": 5}', "FIXTURE not json", '{"post_energy_readback": [1]}',
                  '{"scf_iterations": "7", "output_files": "FIXTURE", "reported_total_energy_hartree": "x"}']
        for body in bodies:
            with self.subTest(body=body):
                with open(os.path.join(attempt, "payload", "result.json"), "w") as fh:
                    fh.write(body)
                for name in ("pre-import.json", "i2-configuration.json"):
                    with open(os.path.join(attempt, "payload", name), "w") as fh:
                        fh.write(body)
                tier, reasons = case.drv.classify({"exit_code": 0}, attempt, inp, exp, [], {"expected_sha256": "x"},
                                                  [{"path": 1}, "FIXTURE"])
                self.assertEqual(tier, "QUARANTINE")
                self.assertTrue(reasons)
        tier, reasons = case.drv.classify(None, attempt, inp, exp)
        self.assertEqual(tier, "QUARANTINE")
        self.assertIn("classification error", reasons[0])

    def wait_gone(self, pid, seconds=10):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return True
            time.sleep(0.1)
        return False

    def test_timeout_kills_group_including_term_ignoring_grandchild(self):
        case = Case(self.tmp, mode="hang", wall=2)
        t0 = time.monotonic()
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (4, "FAILED"), out)
        self.assertIn("timeout", out["reasons"])
        proc = case.outcome()["process"]
        self.assertTrue(proc["timed_out"])
        self.assertEqual([s["signal"] for s in proc["signals_sent"]], ["SIGTERM", "SIGKILL"])
        self.assertTrue(proc["group_absent_after_cleanup"])
        self.assertEqual(proc.get("signal"), signal.SIGKILL)
        grandchild = jload(os.path.join(case.attempt, "payload", "fixture-grandchild.json"))["pid"]
        self.assertTrue(self.wait_gone(grandchild))
        with self.assertRaises(ProcessLookupError):
            os.killpg(proc["pgid"], 0)
        self.assertLess(time.monotonic() - t0, 2 + 2 * case.drv.TERM_GRACE_S + 10)

    def test_group_member_left_after_exit_is_cleaned_and_quarantined(self):
        case = Case(self.tmp, mode="leftover")
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (5, "QUARANTINE"), out)
        self.assertIn("process-group members remained after the engine process ended", out["reasons"])
        proc = case.outcome()["process"]
        self.assertTrue(proc["group_members_after_exit"])
        self.assertTrue(proc["group_absent_after_cleanup"])
        grandchild = jload(os.path.join(case.attempt, "payload", "fixture-grandchild.json"))["pid"]
        self.assertTrue(self.wait_gone(grandchild))


if __name__ == "__main__":
    unittest.main()
