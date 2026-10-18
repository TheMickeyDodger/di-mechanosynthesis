"""Tests of h2_phase_a_r2_driver.py. Standard library unittest; run with python3 -I -B and a private TMPDIR, e.g.:
  TMPDIR=<private temp> python3 -I -B -m unittest discover -s <this directory> -t <this directory> -v

Every test works in a temporary tree built by the accepted test module's Case (a copy of the accepted bundle, a fake
prefix whose interpreter is the accepted fixture-fake-interpreter.py, a runs root) extended with a copy of the route-R2
files. No engine is imported or executed and no real prefix or runs root is touched. The default case exercises the
shipped R2_METHOD_DECISION unchanged: the real approved method revision and the real human approval record are copied
into the case tree, and the run proposal and decision packet are placeholders. Only the unset-gate and fixture-patch
negatives replace R2_METHOD_DECISION inside the test process. Every authorization in these tests is a FIXTURE, not an
authorization. Tests marked "real sandbox" run /usr/bin/sandbox-exec with the R2 profile around fake processes only;
their only network destinations are an AF_UNIX socket and the literal address 127.0.0.1 on ephemeral ports, owned by
the test. Observations that are recorded rather than asserted are printed to stderr as OBSERVATION lines.
"""
import contextlib
import hashlib
import importlib.util
import json
import os
import plistlib
import shlex
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock

TESTS = os.path.dirname(os.path.abspath(__file__))
R2 = os.path.dirname(TESTS)
H2 = os.path.dirname(R2)
PHASE_A = os.path.join(H2, "phase-a")
MARK = "FIXTURE - test value, not a scientific value"
FIXTURE_APPROVAL = "fa11" * 16  # FIXTURE digest that is the digest of no approval record
METHOD_SHA256 = "9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc"  # approved method revision
PACKET_SHA256 = "5ce61f7c97be6db8e332d296d3f54335acb04552296d33eb230ce40cbd9c4083"  # approved decision packet
APPROVAL = "H2-R2-METHOD-HUMAN-APPROVAL.md"
APPROVAL_DIFFERS = f"R2_METHOD_DECISION binds approval-record bytes other than the current {APPROVAL}"
REAL_SANDBOX_EXEC = "/usr/bin/sandbox-exec"
REAL_PLIST = "/System/Library/CoreServices/SystemVersion.plist"
PIDS = []  # every fixture process id recorded by a test; none may remain at the end of the suite
H2_TREE_BEFORE = {}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


acc = load_module("h2_phase_a_accepted_test_driver", os.path.join(PHASE_A, "tests", "test_driver.py"))
sha, jload, jdump, tree_digest = acc.sha, acc.jload, acc.jdump, acc.tree_digest


def observe(name, obj):
    print(f"OBSERVATION {name}: {json.dumps(obj, sort_keys=True)}", file=sys.stderr)


def shipped_driver():
    """The shipped route-R2 driver module, loaded without calling accepted(), so that no accepted bytes execute."""
    return load_module(f"r2_shipped_{time.monotonic_ns()}", os.path.join(R2, "h2_phase_a_r2_driver.py"))


def h2_tree():
    out = {}
    for d, dirs, files in os.walk(H2):
        for n in files + [x for x in dirs if x == "__pycache__"]:
            p = os.path.join(d, n)
            out[os.path.relpath(p, H2)] = sha(p) if os.path.isfile(p) else "DIRECTORY"
    return out


def setUpModule():
    H2_TREE_BEFORE.update(h2_tree())


def host_platform_identity():
    st = os.lstat(REAL_SANDBOX_EXEC)
    with open(REAL_PLIST, "rb") as fh:
        pl = plistlib.load(fh)
    return {"schema": "di-mechanosynthesis/h2-r2-platform-identity/1", "fixture": MARK,
            "sandbox_exec": {"path": REAL_SANDBOX_EXEC, "size": st.st_size, "sha256": sha(REAL_SANDBOX_EXEC)},
            "operating_system": {"ProductVersion": pl["ProductVersion"], "ProductBuildVersion": pl["ProductBuildVersion"]}}


class Case(acc.Case):
    """The accepted test Case, extended with the route-R2 files; self.drv is the R2 driver module. decision=False
    replaces the shipped R2_METHOD_DECISION with None inside the test process (the unset gate); otherwise the shipped
    constant is used unchanged."""

    def __init__(self, tmp, mode="complete", wall=None, probe=False, decision=True):
        super().__init__(tmp, mode, wall)
        self.r2dir = os.path.join(self.root, "docs", "learning", "h2", "phase-a-r2")
        os.makedirs(self.r2dir)
        for name in ("h2_phase_a_r2_driver.py", "h2-r2-sandbox.sb", "H2-R2-METHOD-REVISION.md", APPROVAL):
            shutil.copyfile(os.path.join(R2, name), os.path.join(self.r2dir, name))
        for name in ("H2-A-R2-RUN-PROPOSAL.md", "H2-A-R2-DECISION-PACKET.md"):
            with open(os.path.join(self.r2dir, name), "w") as fh:
                fh.write(f"{MARK}: placeholder for {name}\n")
        jdump(host_platform_identity(), os.path.join(self.r2dir, "h2-r2-platform-identity.json"))
        if probe:
            with open(self.interp, "w") as fh, open(os.path.join(TESTS, "fixture-r2-probe.py")) as src:
                fh.write(f"#!{sys.executable} -I\n" + src.read())
            ipath = os.path.join(self.bundle, "h2-a-01-static-identity.json")
            ident = jload(ipath)
            ident["preflight_expectations"]["sha256"]["bin/python3.14"] = sha(self.interp)
            jdump(ident, ipath)
        self.drv = self.r2 = self.load_r2(decision)

    def load_r2(self, decision=True):
        mod = load_module(f"r2_{id(self)}_{time.monotonic_ns()}", os.path.join(self.r2dir, "h2_phase_a_r2_driver.py"))
        mod.accepted()
        mod.A.GIT_READ = acc.fixture_git()
        if not decision:
            mod.R2_METHOD_DECISION = None
        return mod

    def provenance(self, record=None):
        os.makedirs(os.path.join(self.root, ".herd", "auth"), exist_ok=True)
        path = os.path.join(self.root, ".herd", "auth", "code-provenance.json")
        with open(path, "w") as fh:
            json.dump(record if record is not None else self.r2.build_provenance(), fh, indent=1, sort_keys=True)
        return path

    def authorization(self, mutate=None, provenance=None):
        A = self.r2.A
        auth_dir = os.path.join(self.root, ".herd", "auth")
        os.makedirs(auth_dir, exist_ok=True)
        prov_path = provenance or self.provenance()
        mb_path = os.path.join(auth_dir, "machine-binding.json")
        mb = {"interpreter": self.interp, "prefix": self.prefix, "runs_root": self.runs, "fixture": MARK,
              "command": shlex.join(self.r2.launched_argv(self.interp, self.attempt))}
        if mutate:
            mutate(None, mb)
        jdump(mb, mb_path)
        digests = {k: sha(os.path.join(self.bundle, rel)) for k, rel in A.BUNDLE.items()}
        digests.update({k: sha(os.path.join(self.r2dir, rel)) for k, rel in self.r2.R2_BUNDLE.items()})
        digests.update(machine_binding=sha(mb_path), code_provenance=sha(prov_path))
        auth = {"schema": self.r2.AUTH_SCHEMA, "job_id": "H2-A-01", "max_attempts": 1, "authorized_by": MARK,
                "authorized_utc": MARK, "statement": MARK + " - this is not an authorization", "bound_sha256": digests,
                "machine_binding_path": mb_path, "code_provenance_path": prov_path, "interpreter": self.interp,
                "prefix": self.prefix, "runs_root": self.runs,
                "expected_static_sha256": jload(os.path.join(self.bundle, "h2-a-01-static-identity.json"))
                ["preflight_expectations"]["sha256"],
                "environment": A.build_environment(os.path.realpath(self.prefix), os.path.join(self.attempt, "scratch"))}
        if mutate:
            mutate(auth, None)
        path = os.path.join(auth_dir, "authorization.json")
        jdump(auth, path)
        return path

    def cli(self, args, driver=None):
        return subprocess.run([sys.executable, "-I", "-B", driver or os.path.join(self.r2dir, "h2_phase_a_r2_driver.py")]
                              + args, capture_output=True, text=True, timeout=120)

    def probe_config(self, listeners, nested=True):
        jdump({"fixture": MARK, "case_root": self.root, "unix_socket": listeners.unix_path, "tcp_port": listeners.tcp_port,
               "udp_port": listeners.udp_port, "nested": nested}, os.path.join(self.prefix, "FIXTURE-PROBE.json"))

    def probe_records(self):
        payload = os.path.join(self.attempt, "payload")
        return {n[len("probe-"):-len(".json")]: jload(os.path.join(payload, n))
                for n in os.listdir(payload) if n.startswith("probe-")}


class Listeners:
    """Test-owned listeners: an AF_UNIX stream socket in the case's private .herd directory (bound by a relative path,
    the macOS socket path limit), and a TCP and a UDP socket on the literal address 127.0.0.1 with ephemeral ports."""

    def __init__(self, case):
        self.received, self.stop = [], False
        self.unix_path = os.path.join(case.root, ".herd", "l.sock")
        here = os.getcwd()
        os.chdir(os.path.dirname(self.unix_path))
        try:
            self.unix = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self.unix.bind("l.sock")
        finally:
            os.chdir(here)
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.bind(("127.0.0.1", 0))
        self.tcp_port = self.tcp.getsockname()[1]
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.bind(("127.0.0.1", 0))
        self.udp_port = self.udp.getsockname()[1]
        self.threads = [threading.Thread(target=self.accept_loop, args=(s,), daemon=True) for s in (self.unix, self.tcp)]
        self.threads.append(threading.Thread(target=self.udp_loop, daemon=True))
        for s in (self.unix, self.tcp):
            s.listen(8)
            s.settimeout(0.2)
        self.udp.settimeout(0.2)
        for t in self.threads:
            t.start()

    def accept_loop(self, sock):
        while not self.stop:
            try:
                conn, _ = sock.accept()
            except (socket.timeout, OSError):
                continue
            with conn:
                conn.settimeout(2)
                try:
                    self.received.append(conn.recv(64).decode("ascii", "replace"))
                except OSError as exc:
                    self.received.append(f"recv error {exc}")

    def udp_loop(self):
        while not self.stop:
            try:
                self.received.append(self.udp.recv(64).decode("ascii", "replace"))
            except (socket.timeout, OSError):
                continue

    def close(self):
        time.sleep(0.5)
        self.stop = True
        for t in self.threads:
            t.join(timeout=5)
        for s in (self.unix, self.tcp, self.udp):
            s.close()
        os.unlink(self.unix_path)
        return [t.is_alive() for t in self.threads]


class Base(unittest.TestCase):
    maxDiff = None  # full assertion messages, so that a failure shows the reason that was or was not produced

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = self._tmp.name
        self.addCleanup(self._tmp.cleanup)

    def failed(self, report):
        return {c["id"]: c["detail"] for c in report["checks"] if c["status"] == "FAIL"}

    def case(self, **kw):
        """A fresh Case in its own directory, so that every negative case is independent of the others."""
        return Case(tempfile.mkdtemp(dir=self.tmp), **kw)

    def no_spawn(self, case, argv=None, mutate=None):
        """main() for a run whose launch and Popen fail the test if called; nothing may be written to the runs root."""
        def boom(*a, **k):
            raise AssertionError("a process was spawned on a refused launch")
        with mock.patch.object(case.r2.A, "launch", boom), mock.patch.object(subprocess, "Popen", boom):
            code, out = case.main(argv) if argv else case.run(mutate)
        self.assertEqual(os.listdir(case.runs), [], "nothing may be written on BLOCK_LAUNCH")
        return code, out

    def refused_checks(self, case, expected, argv=None, mutate=None):
        """The run is refused at its first preflight with exactly the expected failing checks {id: detail}."""
        code, out = self.no_spawn(case, argv, mutate)
        self.assertEqual((code, out), (2, {"tier": "BLOCK_LAUNCH", "reasons": [
            {"id": cid, "status": "FAIL", "detail": detail} for cid, detail in expected.items()]}))


# ------------------------------------------------------------------------------------------ shipped gate (AC2)

class TestShippedGate(Base):
    def test_usage_errors_exit_64_and_write_nothing(self):
        case = Case(self.tmp)
        before = tree_digest(case.root), tree_digest(case.prefix)
        for args in ([], ["frobnicate"], case.base() + ["--unknown"], case.base("run"),
                     ["run", "--interpreter", case.interp, "--authorization", "x"], ["code-provenance"]):
            res = case.cli(args)
            self.assertEqual((res.returncode, res.stdout), (64, ""), args)
        self.assertEqual((tree_digest(case.root), tree_digest(case.prefix)), before)
        self.assertEqual(os.listdir(case.runs), [])

    def test_shipped_constant_binds_the_approved_method_and_the_actual_approval_record(self):
        shipped = shipped_driver()
        self.assertIsNone(shipped.A)  # loading the module executed no accepted bytes
        approval, method = os.path.join(R2, APPROVAL), os.path.join(R2, "H2-R2-METHOD-REVISION.md")
        self.assertEqual(shipped.R2_METHOD_DECISION, {"method_revision_sha256": sha(method),
                                                      "approval_record_sha256": sha(approval)})
        self.assertEqual(shipped.R2_METHOD_DECISION["method_revision_sha256"], METHOD_SHA256)
        self.assertEqual(sha(os.path.join(R2, "H2-A-R2-DECISION-PACKET.md")), PACKET_SHA256)
        self.assertEqual(shipped.R2_BUNDLE.get("method_revision_approval"), APPROVAL)
        with open(approval) as fh:
            text = fh.read()
        self.assertIn(METHOD_SHA256, text)
        self.assertIn(PACKET_SHA256, text)
        for name in ("h2_phase_a_r2_driver.py", "H2-A-R2-RUN-PROPOSAL-02.md", "H2-A-R2-RUN-DECISION-PACKET.md",
                     os.path.join("tests", "test_r2_driver.py")):  # no digest of a file that binds the record
            self.assertNotIn(sha(os.path.join(R2, name)), text, name)
        self.assertEqual(Case(self.tmp).r2.R2_METHOD_DECISION, shipped.R2_METHOD_DECISION)  # default case unpatched

    def test_unset_gate_refuses_and_the_accepted_driver_still_refuses(self):
        case = Case(self.tmp, decision=False)
        auth = case.authorization()
        self.refused_checks(case, {"r2.method_revision_decision": (
            "NETWORK_PREREQUISITE_UNRESOLVED: the route-R2 method revision has not been decided by a person "
            "(R2_METHOD_DECISION is unset); no authorization field can satisfy this check")},
            case.base("run") + ["--authorization", auth])  # every other check passes
        res = case.cli(case.base("run") + ["--authorization", auth], os.path.join(case.bundle, "h2_phase_a_driver.py"))
        self.assertEqual(res.returncode, 2)
        self.assertIn("NETWORK_PREREQUISITE_UNRESOLVED", res.stdout)
        self.assertEqual(os.listdir(case.runs), [])

    def test_replaced_check_is_kept_verbatim_and_no_authorization_field_satisfies_the_gate(self):
        case = Case(self.tmp, decision=False)
        rep = case.r2.preflight(case.interp, case.prefix, case.runs)
        self.assertEqual(list(self.failed(rep)), ["r2.method_revision_decision"])
        base = case.r2.A.preflight(case.interp, case.prefix, case.runs)
        self.assertEqual(rep["replaced_base_checks"], [c for c in base["checks"] if c["id"] == "network.prerequisite"])
        self.assertEqual(rep["replaced_base_checks"][0]["detail"], "NETWORK_PREREQUISITE_UNRESOLVED")
        self.assertNotIn("network.prerequisite", [c["id"] for c in rep["checks"]])
        self.assertIsNone(case.r2.A.NETWORK_OBSERVER)
        shipped = shipped_driver().R2_METHOD_DECISION

        def add(a, m):  # even the shipped values, carried in the authorization, do not satisfy the unset gate
            if a:
                a.update(r2_method_decision=shipped, R2_METHOD_DECISION=shipped, network_prerequisite="RESOLVED",
                         offline=True)
        code, out = self.no_spawn(case, mutate=add)
        self.assertEqual((code, [c["id"] for c in out["reasons"]]), (2, ["r2.method_revision_decision"]))

    def test_authorization_file_negatives(self):
        def template(name):
            with open(os.path.join(R2, name)) as fh:
                return fh.read().split("```json\n", 1)[1].split("```", 1)[0]
        mismatch = None
        for name, content in (("absent", None), ("invalid JSON", "FIXTURE not JSON\n"), ("list", '["FIXTURE"]\n'),
                              ("approved packet template", template("H2-A-R2-DECISION-PACKET.md")),
                              ("run-decision packet template", template("H2-A-R2-RUN-DECISION-PACKET.md"))):
            with self.subTest(name=name):
                case = self.case()
                path = os.path.join(case.root, ".herd", "FIXTURE-authorization.json")
                if content is not None:
                    with open(path, "w") as fh:
                        fh.write(content)
                code, out = self.no_spawn(case, case.base("run") + ["--authorization", path])
                if name == "absent":
                    want = [f"FileNotFoundError: [Errno 2] No such file or directory: {path!r}"]
                elif name == "invalid JSON":
                    want = ["JSONDecodeError: Expecting value: line 1 column 1 (char 0)"]
                elif name == "list":
                    want = ["AttributeError: 'list' object has no attribute 'get'"]
                else:
                    self.assertEqual(sorted(json.loads(content)["bound_sha256"]), case.r2.bound_keys())
                    mismatch = mismatch or ", ".join(
                        ["schema"] + [f"bound_sha256.{k}" for k in list(case.r2.A.BUNDLE) + list(case.r2.R2_BUNDLE)]
                        + ["bound_sha256.method_revision_approval", "bound_sha256.machine_binding", "interpreter",
                           "prefix", "runs_root", "expected_static_sha256", "environment: undeclared key",
                           "environment", "machine_binding.command"])
                    want = ["Block: authorization mismatch: " + mismatch]
                self.assertEqual((code, out), (2, {"tier": "BLOCK_LAUNCH", "reasons": want}))


# ------------------------------------------------------------------------------------------ method decision (enabling)

class TestMethodDecision(Base):
    """The approval-bytes binding and the decision negatives; each subtest uses a fresh case."""

    def test_approval_record_absent_unreadable_altered_or_replaced(self):
        def flip(path):
            with open(path, "rb") as fh:
                data = bytearray(fh.read())
            data[len(data) // 2] ^= 0x01  # one byte altered, the length unchanged
            with open(path, "wb") as fh:
                fh.write(bytes(data))

        def replace(path):
            with open(path, "w") as fh:
                fh.write(f"{MARK}: other bytes in place of the approval record\n")

        def unreadable(path):
            os.chmod(path, 0)
            self.addCleanup(os.chmod, path, 0o644)
        for name, change in (("absent", os.unlink), ("unreadable", unreadable), ("one byte altered", flip),
                             ("replaced", replace)):
            with self.subTest(name=name):
                case = self.case()
                auth = case.authorization()  # bound to the real record's bytes before the change
                path = os.path.join(case.r2dir, APPROVAL)
                change(path)
                expected = {"r2.method_revision_decision": APPROVAL_DIFFERS}
                if name in ("absent", "unreadable"):
                    error = "FileNotFoundError: [Errno 2] No such file or directory" if name == "absent" \
                        else "PermissionError: [Errno 13] Permission denied"
                    expected = {"r2.bundle.method_revision_approval": f"{error}: {path!r}", "r2.method_revision_decision":
                                f"the human approval record {APPROVAL} is absent or unreadable"}
                self.refused_checks(case, expected, case.base("run") + ["--authorization", auth])

    def test_authorization_approval_value_or_key(self):
        for name, mutate, want in (
                ("differs from the file and the constant",
                 lambda a, m: a and a["bound_sha256"].__setitem__("method_revision_approval", FIXTURE_APPROVAL),
                 "bound_sha256.method_revision_approval, bound_sha256.method_revision_approval"),
                ("key missing", lambda a, m: a and a["bound_sha256"].pop("method_revision_approval"),
                 "bound_sha256 keys, bound_sha256.method_revision_approval, bound_sha256.method_revision_approval")):
            with self.subTest(name=name):
                code, out = self.no_spawn(self.case(), mutate=mutate)
                self.assertEqual((code, out), (2, {"tier": "BLOCK_LAUNCH", "reasons": [
                    "Block: authorization mismatch: " + want]}))

    def test_decision_differs_from_the_case_files_or_is_malformed(self):
        good = {"method_revision_sha256": METHOD_SHA256, "approval_record_sha256": sha(os.path.join(R2, APPROVAL))}
        with self.subTest(case="constant approval digest differs from the record on disk (FIXTURE patch)"):
            case = self.case()
            case.r2.R2_METHOD_DECISION = dict(good, approval_record_sha256=FIXTURE_APPROVAL)
            self.refused_checks(case, {"r2.method_revision_decision": APPROVAL_DIFFERS})
        with self.subTest(case="method revision on disk differs from the shipped constant"):
            case = self.case()
            with open(os.path.join(case.r2dir, "H2-R2-METHOD-REVISION.md"), "a") as fh:
                fh.write(f"{MARK}: one appended line\n")
            self.refused_checks(case, {"r2.method_revision_decision": (
                "R2_METHOD_DECISION binds method-revision bytes other than the current H2-R2-METHOD-REVISION.md")})
        for value in ({"method_revision_sha256": METHOD_SHA256}, "FIXTURE",
                      dict(good, approval_record_sha256="FIXTURE"), dict(good, extra=FIXTURE_APPROVAL), list(good.values())):
            with self.subTest(case="malformed", value=value):
                case = self.case()
                case.r2.R2_METHOD_DECISION = value
                self.refused_checks(case, {"r2.method_revision_decision": "R2_METHOD_DECISION is malformed"})


# ------------------------------------------------------------------------------------------ accepted-driver pin (AC3)

class TestAcceptedDriverPin(Base):
    def test_altered_accepted_driver_is_refused_before_its_bytes_execute(self):
        case = Case(self.tmp)
        marker = os.path.join(self.tmp, "FIXTURE-executed-marker")
        path = os.path.join(case.bundle, "h2_phase_a_driver.py")
        with open(path) as fh:
            text = fh.read()
        with open(path, "w") as fh:  # the altered bytes would create the marker if they were ever executed
            fh.write(f"open({marker!r}, 'x').close()  # FIXTURE alteration\n" + text)
        for args in (case.base(), ["code-provenance", "--out", os.path.join(self.tmp, "never.json")],
                     case.base("run") + ["--authorization", os.path.join(self.tmp, "absent.json")]):
            res = case.cli(args)
            self.assertEqual(res.returncode, 2, args)
            self.assertIn("PinError", res.stdout)
            self.assertFalse(os.path.exists(marker))
        fresh = load_module(f"r2_pin_{id(self)}", os.path.join(case.r2dir, "h2_phase_a_r2_driver.py"))
        with self.assertRaises(fresh.PinError):
            fresh.accepted()
        self.assertIsNone(fresh.A)
        self.assertFalse(os.path.exists(marker))
        self.assertEqual(os.listdir(case.runs), [])
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "never.json")))
        os.unlink(path)
        res = case.cli(case.base())
        self.assertEqual(res.returncode, 2)
        self.assertIn("accepted driver unreadable", res.stdout)

    def test_pinned_bytes_are_read_once_and_executed_into_a_fresh_module(self):
        case = Case(self.tmp, decision=False)
        fresh = load_module(f"r2_once_{id(self)}", os.path.join(case.r2dir, "h2_phase_a_r2_driver.py"))
        target = os.path.join(case.bundle, "h2_phase_a_driver.py")
        real_open, opened = open, []

        def counting_open(file, *a, **k):
            if isinstance(file, str) and os.path.realpath(file) == os.path.realpath(target):
                opened.append(a[:1])
            return real_open(file, *a, **k)
        with mock.patch("builtins.open", counting_open):
            mod = fresh.accepted()
            again = fresh.accepted()
        self.assertIs(mod, again)
        self.assertEqual(opened, [("rb",)])
        self.assertEqual(mod.__file__, os.path.normpath(target))
        self.assertEqual(mod.launch.__code__.co_filename, os.path.normpath(target))
        self.assertNotIn(mod.__name__, sys.modules)
        self.assertIsNone(mod.NETWORK_OBSERVER)
        self.assertEqual(mod.HERE, case.bundle)


# ------------------------------------------------------------------------------------------ binding negatives (AC4)

class TestBindingNegatives(Base):
    def blocked(self, case, needle, mutate=None, provenance=None):
        def boom(*a, **k):
            raise AssertionError("a process was spawned on a refused launch")
        with mock.patch.object(case.r2.A, "launch", boom), mock.patch.object(subprocess, "Popen", boom):
            code, out = case.run(mutate, provenance)
        self.assertEqual((code, out["tier"]), (2, "BLOCK_LAUNCH"), out)
        self.assertIn(needle, json.dumps(out))
        self.assertEqual(os.listdir(case.runs), [], "nothing may be written on BLOCK_LAUNCH")
        return out

    def test_each_bound_key_and_the_approval_binding(self):
        keys = self.case().r2.bound_keys()
        self.assertEqual(keys, ["code_provenance", "decision_packet", "driver", "input", "machine_binding",
                                "method_revision_approval", "parameters", "payload", "r2_decision_packet", "r2_driver",
                                "r2_method_revision", "r2_platform_identity", "r2_profile", "r2_run_proposal",
                                "run_proposal", "static_identity"])  # sixteen, each once
        for key in keys:
            with self.subTest(key=key):
                self.blocked(self.case(), f"bound_sha256.{key}" if key != "code_provenance"
                             else "code provenance digest differs",
                             lambda a, m, key=key: a and a["bound_sha256"].__setitem__(key, "0" * 64))

    def test_changed_r2_files_after_authorization(self):
        for name, needle in (("h2-r2-sandbox.sb", "bound_sha256.r2_profile"),
                             ("h2-r2-platform-identity.json", "bound_sha256.r2_platform_identity"),
                             ("H2-A-R2-DECISION-PACKET.md", "bound_sha256.r2_decision_packet"),
                             (APPROVAL, APPROVAL_DIFFERS)):  # the method gate refuses before the interlock
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp)
                auth = case.authorization()
                path = os.path.join(case.r2dir, name)
                with open(path, "a") as fh:
                    fh.write(" " if name.endswith(".json") else "; FIXTURE change\n")
                code, out = case.main(case.base("run") + ["--authorization", auth])
                self.assertEqual(code, 2)
                self.assertIn(needle, json.dumps(out))
                self.assertEqual(os.listdir(case.runs), [])

    def test_platform_identity_negatives(self):
        fake = os.path.join(self.tmp, "fake-sandbox-exec")
        with open(fake, "w") as fh:
            fh.write("#!/bin/sh\nexit 99  # FIXTURE: not sandbox-exec\n")
        os.chmod(fake, 0o755)
        link = os.path.join(self.tmp, "link-sandbox-exec")
        os.symlink(REAL_SANDBOX_EXEC, link)
        noexec = os.path.join(self.tmp, "noexec-sandbox-exec")
        shutil.copyfile(REAL_SANDBOX_EXEC, noexec)
        os.chmod(noexec, 0o644)
        plist = os.path.join(self.tmp, "SystemVersion.plist")
        with open(plist, "wb") as fh:
            plistlib.dump(dict(host_platform_identity()["operating_system"], ProductBuildVersion="FIXTURE0"), fh)
        bad_plist = os.path.join(self.tmp, "bad.plist")
        with open(bad_plist, "w") as fh:
            fh.write("FIXTURE not a plist")
        for const, value, check in (("SANDBOX_EXEC", fake, "r2.sandbox_exec"), ("SANDBOX_EXEC", link, "r2.sandbox_exec"),
                                    ("SANDBOX_EXEC", noexec, "r2.sandbox_exec"),
                                    ("SANDBOX_EXEC", self.tmp, "r2.sandbox_exec"),
                                    ("SYSTEM_VERSION_PLIST", plist, "r2.os_build"),
                                    ("SYSTEM_VERSION_PLIST", bad_plist, "r2.platform_identity.parse")):
            with self.subTest(const=const, value=os.path.basename(value)):
                case = self.case()
                with mock.patch.object(case.r2, const, value):
                    out = self.blocked(case, check)
                self.assertIn(check, [c["id"] for c in out["reasons"]])
        with self.subTest(case="record digest differs from the host"):
            case = self.case()
            ident = jload(os.path.join(case.r2dir, "h2-r2-platform-identity.json"))
            ident["sandbox_exec"]["sha256"] = "0" * 64
            jdump(ident, os.path.join(case.r2dir, "h2-r2-platform-identity.json"))
            self.blocked(case, "r2.sandbox_exec")

    def refusal(self, case, mode, patches):
        """main() for preflight or run under the given patches; an escaping exception is a test failure, not an error."""
        argv = case.base(mode) + (["--authorization", case.authorization()] if mode == "run" else [])
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(case.r2.A, "launch", mock.Mock(side_effect=AssertionError("spawned"))))
            for obj, name, value in patches:
                stack.enter_context(mock.patch.object(obj, name, value))
            try:
                code, out = case.main(argv)
            except Exception as exc:  # noqa: BLE001
                self.fail(f"{mode} raised {exc.__class__.__name__} instead of a structured BLOCK_LAUNCH: {exc}")
        self.assertEqual(os.listdir(case.runs), [])
        return code, out

    def test_wrong_shaped_plist_is_a_structured_refusal(self):
        for shape, value in (("array", ["FIXTURE"]), ("string", "FIXTURE")):
            plist = os.path.join(self.tmp, f"{shape}.plist")
            with open(plist, "wb") as fh:
                plistlib.dump(value, fh)
            for mode in ("preflight", "run"):
                with self.subTest(shape=shape, mode=mode):
                    case = self.case()
                    code, out = self.refusal(case, mode, [(case.r2, "SYSTEM_VERSION_PLIST", plist)])
                    checks = out["report"]["checks"] if mode == "preflight" else out["reasons"]
                    failed = {c["id"]: c["detail"] for c in checks if c["status"] == "FAIL"}
                    self.assertIn(f"SystemVersion.plist top level is {type(value).__name__}, not a dictionary",
                                  failed.get("r2.platform_identity.parse", ""))
                    self.assertEqual((code, out["tier"]), (2, "BLOCK_LAUNCH"), out)

    def test_unexpected_preflight_error_is_a_structured_refusal(self):
        for mode in ("preflight", "run"):
            with self.subTest(mode=mode):
                case = self.case()
                code, out = self.refusal(case, mode, [(case.r2, "observe_platform",
                                                      mock.Mock(side_effect=RuntimeError("FIXTURE unexpected")))])
                self.assertEqual((code, out), (2, {"tier": "BLOCK_LAUNCH",
                                                   "reasons": ["preflight error: RuntimeError: FIXTURE unexpected"]}))

    def test_machine_binding_command_must_be_the_wrapped_command(self):
        case = Case(self.tmp)
        A = case.r2.A
        wrapped = case.r2.launched_argv(case.interp, case.attempt)
        self.assertEqual(wrapped[:3], [REAL_SANDBOX_EXEC, "-f", os.path.join(case.attempt, "bundle", "h2-r2-sandbox.sb")])
        self.assertEqual(wrapped[3:7], ["-D", "H2_PAYLOAD_DIR=" + os.path.join(case.attempt, "payload"),
                                        "-D", "H2_SCRATCH_DIR=" + os.path.join(case.attempt, "scratch")])
        self.assertEqual(wrapped[7:], A.command_for(case.interp, case.attempt))
        variants = {"no wrapper": lambda c, w: c.r2.A.command_for(c.interp, c.attempt),
                    "payload parameter widened to the attempt": lambda c, w: w[:4] + ["H2_PAYLOAD_DIR=" + c.attempt] + w[5:],
                    "scratch parameter dropped": lambda c, w: w[:5] + w[7:],
                    "profile from the repository": lambda c, w: w[:2] + [os.path.join(c.r2dir, "h2-r2-sandbox.sb")] + w[3:],
                    "inline profile": lambda c, w: [REAL_SANDBOX_EXEC, "-p", "(version 1)(allow default)"] + w[7:]}
        for name, make in variants.items():
            with self.subTest(name=name):
                c = self.case()
                argv = make(c, c.r2.launched_argv(c.interp, c.attempt))
                self.blocked(c, "machine_binding.command", lambda a, m, argv=argv: m and m.__setitem__("command", shlex.join(argv)))

    def test_accepted_interlock_rules_carry_over(self):
        for field, value, needle in (("schema", "di-mechanosynthesis/h2-phase-a-authorization/1", "schema"),
                                     ("max_attempts", 2, "max_attempts"), ("job_id", "H2-B-01", "job_id"),
                                     ("statement", " ", "statement"), ("interpreter", "/elsewhere", "interpreter"),
                                     ("runs_root", "/elsewhere", "runs_root")):
            with self.subTest(field=field):
                self.blocked(self.case(), needle, lambda a, m, f=field, v=value: a and a.__setitem__(f, v))
        for name, needle, mutate in (
                ("environment value", "environment", lambda a, m: a and a["environment"].__setitem__("OMP_NUM_THREADS", "4")),
                ("environment key", "environment: undeclared key",
                 lambda a, m: a and a["environment"].__setitem__("PSIPATH", "/x")),
                ("static digest", "expected_static_sha256",
                 lambda a, m: a and a["expected_static_sha256"].__setitem__("lib/libint2.dylib", "0" * 64))):
            with self.subTest(case=name):
                self.blocked(self.case(), needle, mutate)

    def test_code_provenance_absent_mismatched_stale_or_unresolvable(self):
        with self.subTest(case="absent"):
            self.blocked(self.case(), "code provenance absent", lambda a, m: a and a.pop("code_provenance_path"))
        with self.subTest(case="tampered diff"):
            case = self.case()
            rec = case.r2.build_provenance()
            rec["files"][-1]["diff_unified"] += "+FIXTURE tampered line\n"
            self.blocked(case, "code provenance mismatch", provenance=case.provenance(rec))
        with self.subTest(case="accepted five-path record"):
            case = self.case()
            self.blocked(case, "code provenance mismatch", provenance=case.provenance(case.r2.A.build_provenance()))
        with self.subTest(case="stale after a profile change"):
            case = self.case()
            stale = case.provenance(case.r2.build_provenance())
            with open(os.path.join(case.r2dir, "h2-r2-sandbox.sb"), "a") as fh:
                fh.write("; FIXTURE change after the provenance record\n")
            self.blocked(case, "code provenance mismatch", provenance=stale)
        for name, reader, needle in (("HEAD moved", acc.fixture_git(head="dead" * 10), "code provenance mismatch"),
                                     ("ls-tree fails", acc.fixture_git(fail="ls-tree"), "unresolvable: ls-tree")):
            with self.subTest(case=name):
                case = self.case()
                prov = case.provenance()
                case.r2.A.GIT_READ = reader  # FIXTURE: the Git state differs from the one the record was made from
                self.blocked(case, needle, provenance=prov)


# ------------------------------------------------------------------------------------------ real sandbox (AC5)

class TestRealSandboxPrevention(Base):
    """real sandbox: the probe and its descendants run under /usr/bin/sandbox-exec through the R2 run path."""
    REFUSED_WRITES = ("prefix_existing_file", "prefix_new_file", "conda_meta_new_record", "attempt_bundle",
                      "attempt_root", "runs_root", "repository_tree")
    ALLOWED_WRITES = ("inside_payload", "inside_scratch")
    NETWORK = ("unix_connect", "unix_bind", "tcp_connect_127", "udp_send_127")
    ROLES = ("process", "child", "grandchild", "setsid_grandchild")

    def run_probe(self, case, sandboxed):
        listeners = Listeners(case)
        case.probe_config(listeners)
        self.prefix_before = tree_digest(case.prefix)  # after the probe configuration is written
        try:
            if sandboxed:
                code, out = case.run()
                self.assertTrue(os.path.isdir(os.path.join(case.attempt, "payload")), out)  # the run reached launch
            else:  # unsandboxed control: the same probe, launched directly with the same layout and environment
                for sub in ("bundle", "payload", "scratch"):
                    os.makedirs(os.path.join(case.attempt, sub))
                env = case.r2.A.build_environment(os.path.realpath(case.prefix), os.path.join(case.attempt, "scratch"))
                cmd = case.r2.A.command_for(case.interp, case.attempt)
                with open(os.path.join(case.attempt, "engine.stdout"), "x") as so, \
                        open(os.path.join(case.attempt, "engine.stderr"), "x") as se:
                    code = subprocess.run(cmd, cwd=os.path.join(case.attempt, "scratch"), env=env,
                                          stdin=subprocess.DEVNULL, stdout=so, stderr=se, timeout=120).returncode
                out = None
        finally:
            alive = listeners.close()
        self.assertEqual(alive, [False, False, False])
        recs = case.probe_records()
        for rec in recs.values():
            PIDS.append(rec["pid"])
        return code, out, recs, listeners.received

    def test_sandboxed_probe_and_descendants_are_refused(self):
        case = Case(self.tmp, probe=True)
        docs_before = tree_digest(os.path.join(case.root, "docs"))
        code, out, recs, received = self.run_probe(case, sandboxed=True)
        self.assertLessEqual(set(self.ROLES + ("process_after_nested",)), set(recs))
        self.assertLessEqual(set(recs), set(self.ROLES + ("process_after_nested", "nested")))
        for role, rec in recs.items():
            for op in self.REFUSED_WRITES:
                self.assertEqual((role, op, rec["writes"][op]["ok"], rec["writes"][op].get("errno")), (role, op, False, 1))
            for op in self.ALLOWED_WRITES:
                self.assertEqual((role, op, rec["writes"][op]["ok"]), (role, op, True))
            for op in self.NETWORK:
                self.assertEqual((role, op, rec["network"][op]["ok"], rec["network"][op].get("errno")), (role, op, False, 1))
        self.assertEqual(received, [])  # the owned listeners received nothing
        self.assertEqual((code, out["tier"], out["reasons"]), (5, "QUARANTINE", ["missing provenance: result record absent"]))
        proc, gc, sgc = recs["process"], recs["grandchild"], recs["setsid_grandchild"]
        self.assertEqual((gc["pgid"], gc["sid"]), (proc["pgid"], proc["sid"]))
        self.assertNotEqual(sgc["pgid"], proc["pgid"])
        self.assertNotEqual(sgc["sid"], proc["sid"])
        o = case.outcome()
        self.assertEqual(o["process"]["command"], case.r2.launched_argv(case.interp, case.attempt))
        with open(os.path.join(case.attempt, "engine.stdout")) as fh:
            stdout = fh.read()
        with open(os.path.join(case.attempt, "engine.stderr")) as fh:
            stderr = fh.read()
        for role in self.ROLES:
            self.assertIn(f"FIXTURE-STDOUT-{role}", stdout)
            self.assertIn(f"FIXTURE-STDERR-{role}", stderr)
        self.assertEqual(tree_digest(case.prefix), self.prefix_before)
        self.assertEqual(tree_digest(os.path.join(case.root, "docs")), docs_before)
        self.assertEqual(sorted(os.listdir(case.runs)), ["H2-A-01"])
        self.assertEqual(sorted(os.listdir(os.path.join(case.attempt, "bundle"))),
                         ["h2-a-01-input.json", "h2-r2-sandbox.sb", "h2_phase_a_payload.py"])
        self.assertFalse([n for n in os.listdir(case.attempt) if n.startswith("fixture-")])
        nested = proc["nested_sandbox_exec"]
        observe("nested_sandbox_exec_inside_sandbox", nested)
        observe("probe_environ_names_sandboxed", proc["environ_names"])
        observe("nested_probe_ran", "nested" in recs)  # whatever happened; if it ran, the loop above checked its refusals
        self.assertLessEqual(set(proc["environ_names"]),
                             set(case.r2.A.ALLOWED_ENV) | set(case.r2.A.PLATFORM_INJECTED))

    def test_unsandboxed_control_of_the_same_probe_succeeds(self):
        case = Case(self.tmp, probe=True)
        code, _, recs, received = self.run_probe(case, sandboxed=False)
        self.assertEqual(code, 0)
        for role in self.ROLES + ("process_after_nested",):
            rec = recs[role]
            for op in self.REFUSED_WRITES + self.ALLOWED_WRITES:
                self.assertTrue(rec["writes"][op]["ok"], (role, op, rec["writes"][op]))
            for op in self.NETWORK:
                self.assertTrue(rec["network"][op]["ok"], (role, op, rec["network"][op]))
        for role in self.ROLES:
            for kind in ("unix", "tcp", "udp"):
                self.assertIn(f"FIXTURE-{role}-{kind}", received)
        observe("nested_sandbox_exec_unsandboxed_control", recs["process"]["nested_sandbox_exec"])
        observe("probe_environ_names_control", recs["process"]["environ_names"])


# ------------------------------------------------------------------------------------------ preserved behaviour (AC6)

class TestPreservedBehaviour(Base):
    """real sandbox: the accepted fake interpreter, unchanged, launched through the R2 wrapper."""

    def test_complete_run_and_launch_record(self):
        case = Case(self.tmp, mode="env_dump")
        os.environ["FIXTURE_LEAK_CHECK"] = MARK
        self.addCleanup(os.environ.pop, "FIXTURE_LEAK_CHECK", None)
        code, out = case.run()
        self.assertEqual((code, out["tier"], out["reasons"]), (0, "COMPLETED_PENDING_REVIEW", []))
        o = case.outcome()
        A = case.r2.A
        launch = jload(os.path.join(case.attempt, "launch-record.json"))
        argv = case.r2.launched_argv(case.interp, case.attempt)
        self.assertEqual(launch["command"], A.command_for(case.interp, case.attempt))
        self.assertEqual((launch["launched_argv"], launch["launched_shell_form"]), (argv, shlex.join(argv)))
        self.assertEqual(launch["launched_shell_form"], jload(os.path.join(case.root, ".herd", "auth",
                                                                          "machine-binding.json"))["command"])
        self.assertEqual(o["process"]["command"], argv)
        self.assertEqual(launch["sandbox_exec_sha256"], sha(REAL_SANDBOX_EXEC))
        self.assertEqual(sha(os.path.join(case.attempt, "bundle", "h2-r2-sandbox.sb")), launch["r2_profile_sha256"])
        shipped = shipped_driver().R2_METHOD_DECISION
        self.assertEqual((case.r2.R2_METHOD_DECISION, launch["r2_method_decision"]), (shipped, shipped))
        env = jload(os.path.join(case.attempt, "payload", "fixture-env.json"))
        observe("accepted_fake_environ_names_under_wrapper", env["names"])
        self.assertLessEqual(set(env["names"]), set(A.ALLOWED_ENV) | set(A.PLATFORM_INJECTED))
        self.assertNotIn("FIXTURE_LEAK_CHECK", env["names"])
        for rep in ("preflight_initial", "preflight_final", "post_run_checks"):
            self.assertTrue(all(c["status"] == "PASS" for c in o[rep]["checks"]), rep)
            self.assertLessEqual({"r2.method_revision_decision", "r2.bundle.method_revision_approval"},
                                 {c["id"] for c in o[rep]["checks"]}, rep)
            self.assertEqual(o[rep]["r2_method_decision"], shipped, rep)
            self.assertEqual([c["id"] for c in o[rep]["replaced_base_checks"]], ["network.prerequisite"])
        self.assertIn("r2.sandbox_exec", [c["id"] for c in o["post_run_checks"]["checks"]])
        files = {f["path"] for f in o["files"]}
        self.assertLessEqual(set(A.EXPECTED_OUTPUTS) | {"bundle/h2-r2-sandbox.sb"}, files)

    def test_second_run_blocks_and_nothing_is_overwritten(self):
        case = Case(self.tmp)
        code, out = case.run()
        self.assertEqual(code, 0, out)
        before = tree_digest(case.attempt)
        code, out = case.run()
        self.assertEqual((code, out), (2, {"tier": "BLOCK_LAUNCH", "reasons": [  # the accepted preflight check blocks first
            {"id": "attempt.absent", "status": "FAIL", "detail": "an attempt record for this job exists; zero retries"}]}))
        self.assertEqual(tree_digest(case.attempt), before)

    def wait_gone(self, pid, seconds=10):
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return True
            time.sleep(0.1)
        return False

    def test_timeout_kills_the_group_through_the_wrapper(self):
        case = Case(self.tmp, mode="hang", wall=2)
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (4, "FAILED"), out)
        self.assertIn("timeout", out["reasons"])
        proc = case.outcome()["process"]
        self.assertEqual([s["signal"] for s in proc["signals_sent"]], ["SIGTERM", "SIGKILL"])
        self.assertTrue(proc["group_absent_after_cleanup"])
        self.assertEqual(proc.get("signal"), signal.SIGKILL)
        grandchild = jload(os.path.join(case.attempt, "payload", "fixture-grandchild.json"))["pid"]
        PIDS.append(grandchild)
        self.assertTrue(self.wait_gone(grandchild))

    def test_group_member_left_after_exit_is_quarantined(self):
        case = Case(self.tmp, mode="leftover")
        code, out = case.run()
        self.assertEqual((code, out["tier"]), (5, "QUARANTINE"), out)
        self.assertIn("process-group members remained after the engine process ended", out["reasons"])
        grandchild = jload(os.path.join(case.attempt, "payload", "fixture-grandchild.json"))["pid"]
        PIDS.append(grandchild)
        self.assertTrue(self.wait_gone(grandchild))

    def test_refused_prefix_write_that_breaks_the_fake_is_failed(self):
        case = Case(self.tmp, mode="modify_prefix")
        before = tree_digest(case.prefix)
        code, out = case.run()
        self.assertEqual((code, out["tier"], out["reasons"]), (4, "FAILED", ["nonzero exit 1"]))
        self.assertEqual(tree_digest(case.prefix), before)
        with open(os.path.join(case.attempt, "engine.stderr")) as fh:
            self.assertIn("PermissionError", fh.read())

    def test_prefix_change_outside_the_sandbox_during_the_run_is_quarantined(self):
        case = Case(self.tmp)
        real_launch = case.r2.A.launch

        def unsandboxed_actor(*a, **k):  # the test process, which is not sandboxed, changes the prefix mid-run
            meta = os.path.join(case.prefix, "conda-meta")
            name = [n for n in os.listdir(meta) if n.startswith("psi4-")][0]
            rec = jload(os.path.join(meta, name))
            jdump(dict(rec, build_number=rec["build_number"] + 1), os.path.join(meta, name))
            jdump({"fixture": MARK}, os.path.join(meta, "fixture-installed-0.0-0.json"))
            return real_launch(*a, **k)
        with mock.patch.object(case.r2.A, "launch", unsandboxed_actor):
            code, out = case.run()
        self.assertIn("post-run check failed: package.psi4: package record psi4 differs in ['build_number']", out["reasons"])
        self.assertIn("prefix package records or bound files changed during the run: "
                      "['conda-meta/', 'conda-meta/psi4-1.11-py314h53d0584_1.json']", out["reasons"])
        self.assertEqual((code, out["tier"]), (5, "QUARANTINE"), out)

    def test_iteration_limit_malformed_record_and_stop_tiers(self):
        limit, mismatch = "iteration limit reached", "scf_iterations is not consistent with the raw reported value"
        for mode, code, tier, check in (("iter_50_raw49", 4, "FAILED", lambda r: r == [limit, mismatch]),
                                        ("result_list", 5, "QUARANTINE", lambda r: "result record top level is list" in r[0]),
                                        ("stop", 3, "STOP_BEFORE_ENERGY",
                                         lambda r: r[:2] == ["stopped at I1-loaded-identity", "FIXTURE identity problem"])):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp, mode=mode)
                got, out = case.run()
                self.assertEqual((got, out["tier"]), (code, tier), out)
                self.assertTrue(check(out["reasons"]), out["reasons"])
                self.assertEqual(case.outcome()["tier"], tier)


# ------------------------------------------------------------------------------------------ post-run observation (AC6)

class TestPostRunObservation(Base):
    """real sandbox: an unsandboxed actor (the test process) changes state while the driver is in its launch step."""

    def run_with_actor(self, case, actor):
        real_launch = case.r2.A.launch

        def wrapped(*a, **k):
            actor(case)
            return real_launch(*a, **k)
        with mock.patch.object(case.r2.A, "launch", wrapped):
            return case.run()

    def test_unexpected_entries_and_altered_copies_are_quarantined(self):
        def put(path, mode, data):
            with open(path, mode) as fh:
                fh.write(data)

        def write(rel):
            return lambda case: put(os.path.join(case.attempt, rel), "x", "FIXTURE extra\n")

        def append(rel):
            return lambda case: put(os.path.join(case.attempt, rel), "a", "; FIXTURE altered\n")
        cases = {"root entry": (write("FIXTURE-extra"), "unexpected entries in the attempt root: ['FIXTURE-extra']"),
                 "bundle entry": (write("bundle/FIXTURE-extra"),
                                  "unexpected entries in the attempt bundle: ['FIXTURE-extra']"),
                 "profile copy": (append("bundle/h2-r2-sandbox.sb"),
                                  "attempt copy missing or changed: bundle/h2-r2-sandbox.sb"),
                 "payload copy": (append("bundle/h2_phase_a_payload.py"),
                                  "attempt copy missing or changed: bundle/h2_phase_a_payload.py"),
                 "provenance copy": (lambda case: os.unlink(os.path.join(case.attempt, "code-provenance.json")),
                                     "attempt copy missing or changed: code-provenance.json"),
                 "repository profile": (lambda case: put(os.path.join(case.r2dir, "h2-r2-sandbox.sb"), "a", "; FIXTURE\n"),
                                        "bundle files changed during the run"),
                 "OS build": (lambda case: setattr(case.r2, "SYSTEM_VERSION_PLIST", case.alt_plist),
                              "post-run check failed: r2.os_build: OS version or build differs from the platform identity "
                              "record")}
        for name, (actor, needle) in cases.items():
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                case = Case(tmp)
                case.alt_plist = os.path.join(tmp, "SystemVersion.plist")
                with open(case.alt_plist, "wb") as fh:
                    plistlib.dump({"ProductVersion": "FIXTURE", "ProductBuildVersion": "FIXTURE0"}, fh)
                code, out = self.run_with_actor(case, actor)
                self.assertIn(needle, out["reasons"])  # the exact reason, so that a failure names the missing check
                self.assertEqual((code, out["tier"]), (5, "QUARANTINE"), out)
                self.assertEqual(case.outcome()["reasons"], out["reasons"])

    def test_approval_record_changed_during_the_run_is_quarantined(self):
        case = Case(self.tmp)

        def actor(case):
            with open(os.path.join(case.r2dir, APPROVAL), "a") as fh:
                fh.write(f"{MARK}: changed during the run\n")
        code, out = self.run_with_actor(case, actor)
        reasons = [f"post-run check failed: r2.method_revision_decision: {APPROVAL_DIFFERS}",
                   "bundle files changed during the run"]
        self.assertEqual((code, out["tier"], out["reasons"]), (5, "QUARANTINE", reasons))
        o = case.outcome()
        self.assertEqual(o["reasons"], reasons)
        self.assertNotEqual(o["post_run_checks"]["digests"]["method_revision_approval"],
                            o["preflight_final"]["digests"]["method_revision_approval"])


# ------------------------------------------------------------------------------------------ code provenance (AC7)

class TestCodeProvenance(Base):
    def test_record_covers_the_eight_paths(self):
        case = Case(self.tmp)
        base = b"FIXTURE base text\n"
        rel_profile = os.path.relpath(os.path.join(case.r2dir, "h2-r2-sandbox.sb"), case.root)
        case.r2.A.GIT_READ = acc.fixture_git(tree={rel_profile: base})
        rec = case.r2.build_provenance()
        self.assertEqual(rec["schema"], "di-mechanosynthesis/h2-phase-a-r2-code-provenance/1")
        self.assertEqual([f["key"] for f in rec["files"]], list(case.r2.PROVENANCE_KEYS))
        self.assertEqual(rec["coverage"]["paths"], [
            "docs/learning/h2/phase-a-r2/h2_phase_a_r2_driver.py", "docs/learning/h2/phase-a/h2_phase_a_driver.py",
            "docs/learning/h2/phase-a/h2_phase_a_payload.py", "docs/learning/h2/phase-a/h2-a-01-input.json",
            "docs/learning/h2/h2-method-parameters.json", "docs/learning/h2/phase-a/h2-a-01-static-identity.json",
            "docs/learning/h2/phase-a-r2/h2-r2-sandbox.sb", "docs/learning/h2/phase-a-r2/h2-r2-platform-identity.json"])
        for f in rec["files"]:
            with open(os.path.join(case.root, f["path"]), "rb") as fh:
                cur = fh.read()
            self.assertEqual(f["current_sha256"], hashlib.sha256(cur).hexdigest())
            self.assertEqual(f["diff_sha256"], hashlib.sha256(f["diff_unified"].encode()).hexdigest())
            self.assertEqual(f["base_present"], f["path"] == rel_profile)
            if f["path"] == rel_profile:
                self.assertEqual(f["base_blob_sha1"], acc.git_blob_id(base))
                self.assertTrue(f["diff_unified"].startswith("--- a/" + rel_profile))
        digests = {f["key"]: f["current_sha256"] for f in rec["files"]}
        path = case.provenance(rec)
        self.assertEqual(case.r2.check_provenance(path, sha(path), digests), rec)

    def test_code_provenance_mode_writes_exclusively_or_not_at_all(self):
        case = Case(self.tmp)
        out_path = os.path.join(self.tmp, "prov.json")
        code, out = case.main(["code-provenance", "--out", out_path])
        self.assertEqual((code, out["code_provenance"], out["sha256"]), (0, "WRITTEN", sha(out_path)))
        self.assertEqual(len(out["paths"]), 8)
        code, out = case.main(["code-provenance", "--out", out_path])
        self.assertEqual((code, out["code_provenance"]), (2, "NOT_WRITTEN"))
        case.r2.A.GIT_READ = acc.fixture_git(fail="rev-parse")
        code, out = case.main(["code-provenance", "--out", os.path.join(self.tmp, "never.json")])
        self.assertEqual((code, out["code_provenance"]), (2, "NOT_WRITTEN"))
        self.assertFalse(os.path.exists(os.path.join(self.tmp, "never.json")))


# ------------------------------------------------------------------------------------------ suite end (AC13)

class TestZZSuiteEnd(Base):
    def test_no_repository_writes_bytecode_or_leftover_processes(self):
        self.assertEqual(h2_tree(), H2_TREE_BEFORE)
        self.assertFalse([k for k in h2_tree() if "__pycache__" in k])
        if not PIDS:
            self.skipTest("no fixture process id was recorded in this test selection")
        alive = []
        for pid in PIDS:
            try:
                os.kill(pid, 0)
                alive.append(pid)
            except ProcessLookupError:
                pass
        self.assertEqual(alive, [])
        observe("fixture_pids_checked", len(PIDS))


if __name__ == "__main__":
    unittest.main()
