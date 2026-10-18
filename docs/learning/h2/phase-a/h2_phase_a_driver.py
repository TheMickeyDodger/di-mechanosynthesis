"""Control driver for job H2-A-01 (prospective; NOT_RUN; [AGENT]). Standard library only; never imports an engine.

usage:
  h2_phase_a_driver.py preflight --interpreter PATH --prefix PATH --runs-root PATH
  h2_phase_a_driver.py code-provenance --out PATH
  h2_phase_a_driver.py run --interpreter PATH --prefix PATH --runs-root PATH --authorization PATH

There is no executable default. No arguments, unknown arguments or a missing binding give a usage error (exit 64)
with no process spawned and nothing written. `preflight` is static: it spawns no process, imports no engine and
writes nothing. `code-provenance` writes one detached code-provenance record (exclusive creation) using read-only Git
queries. `run` launches at most one engine process, and only when an authorization file binds the exact digests of
every bound file and of a code-provenance record that the driver re-derives from Git and the current bytes. The interlock checks bytes and fields only. It cannot show that a person authorized
anything; that is established, if at all, by the human decision record outside this program.

Exit codes: 0 completed (result recorded, pending independent review), 2 BLOCK_LAUNCH, 3 STOP_BEFORE_ENERGY,
4 FAILED, 5 QUARANTINE, 64 usage error. Paths in the bundle are relative to this file; there are no machine paths.
"""
import argparse
import base64
import datetime
import difflib
import hashlib
import json
import math
import os
import re
import shlex
import shutil
import signal
import stat
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BUNDLE = {"driver": os.path.basename(__file__), "payload": "h2_phase_a_payload.py", "input": "h2-a-01-input.json",
          "parameters": os.path.join("..", "h2-method-parameters.json"),
          "static_identity": "h2-a-01-static-identity.json", "run_proposal": "H2-A-01-RUN-PROPOSAL.md",
          "decision_packet": "H2-A-01-DECISION-PACKET.md"}
BOUND_KEYS = sorted(list(BUNDLE) + ["machine_binding", "code_provenance"])
# Code paths a run uses (evidence policy section 4, "Code identity"): the driver executes, the payload runs in the
# engine process, and the input, parameter file and static identity record determine what is run and checked.
PROVENANCE_KEYS = ("driver", "payload", "input", "parameters", "static_identity")
GIT_ALLOWED = ("rev-parse", "ls-tree", "cat-file")  # read-only queries only; never index, history or remote writes
ALLOWED_ENV = ("LC_ALL", "OMP_NUM_THREADS", "PATH", "PSI_SCRATCH", "TMPDIR")  # [AGENT] allow-list, nothing inherited
PLATFORM_INJECTED = ("__CF_USER_TEXT_ENCODING",)  # recorded if present in the engine process, never scrubbed
FREE_SPACE_FLOOR_BYTES = 2 * 1024 ** 3  # [AGENT] floor on the runs-root file system
TERM_GRACE_S = 5.0  # [AGENT] SIGTERM-to-SIGKILL grace for the process group
POLL_S = 0.05
SCF_KEYS = ("reference", "basis", "guess", "scf_type", "df_scf_guess", "e_convergence", "d_convergence",
            "maxiter", "fail_on_maxiter")
MOL_KEYS = ("units", "symmetry", "no_reorient", "no_com")
STAGE_RECORDS = ("pre-import", "i1-identity", "i2-configuration", "i3-basis-geometry")  # payload gates, in order
EXPECTED_OUTPUTS = ("launch-record.json", "code-provenance.json", "engine.stdout", "engine.stderr",
                    "bundle/h2_phase_a_payload.py", "bundle/h2-a-01-input.json", "payload/pre-import.json",
                    "payload/i1-identity.json", "payload/i2-configuration.json", "payload/i3-basis-geometry.json",
                    "payload/result.json", "payload/psi4-output.dat", "payload/psi4-output.log")
RESULT_FIELDS = ("job_id", "reported_total_energy_hartree", "reported_nuclear_repulsion_hartree", "scf_iterations",
                 "converged", "engine_version", "post_energy_readback", "banner_preserved_after_energy", "output_files")
# No-network prerequisite (accepted stop condition "any network access or installation attempt"). No offline check or
# sandbox with established semantics exists in this package (proposal section 8.5), so no observer is configured and
# every launch is refused with NETWORK_PREREQUISITE_UNRESOLVED. A future reviewed revision may supply an observer: a
# function the driver itself calls before launch and after the process ends, returning {"offline": bool, ...}. A
# field in the authorization file cannot satisfy this gate.
NETWORK_OBSERVER = None
POST_RUN_CHECK_GROUPS = ("bundle", "input", "prefix", "interpreter", "package", "sha256", "network")
EXIT = {"COMPLETED_PENDING_REVIEW": 0, "BLOCK_LAUNCH": 2, "STOP_BEFORE_ENERGY": 3, "FAILED": 4, "QUARANTINE": 5}


class Block(Exception):
    """Launch refused before any engine process exists."""


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    with open(path) as fh:
        return json.load(fh)


def under(root, path):
    return path == root or path.startswith(root + os.sep)


# ------------------------------------------------------------------------------------------ input against parameters

def derive_expected(params):
    """Phase A expectations derived from the accepted parameter file, not restated."""
    jobs = params["phases"]["A"]["job_sequence"]
    if len(jobs) != 1 or params["resource_bounds"]["phase_A_max_jobs"] != 1:
        raise ValueError("Phase A must have exactly one job")
    r = jobs[0]["R_bohr"]
    atoms = []
    for a in params["system"]["atoms"]:
        m = re.fullmatch(r"\(0, 0, ([+-])R/2\)", a["position_bohr"])
        if not m:
            raise ValueError("unrecognized atom position form")
        atoms.append({"label": a["label"], "element": a["element"],
                      "xyz_bohr": [0.0, 0.0, (r / 2.0) * (1.0 if m.group(1) == "+" else -1.0)]})
    opts = params["proposed_engine_options"]
    tols = [float(m.group(1)) for s in params["stop_conditions"]
            for m in [re.search(r"by more than ([0-9.eE+-]+) hartree", s)] if m]
    if len(tols) != 1:
        raise ValueError("nuclear-repulsion tolerance not found exactly once")
    return {
        "job_id": jobs[0]["job_id"], "R_bohr": r, "atoms": atoms,
        "charge": params["system"]["charge"], "multiplicity": params["system"]["multiplicity"],
        "electrons": params["system"]["electrons"], "coordinate_unit": params["system"]["coordinate_unit"],
        "engine_options": {k: opts[k]["value"] for k in SCF_KEYS},
        "molecule_options": {k: opts[k]["value"] for k in MOL_KEYS},
        "threads": opts["threads"]["value"], "memory": opts["memory"]["value"],
        "wall_seconds": params["resource_bounds"]["wall_seconds_per_job"],
        "retries": params["resource_bounds"]["automatic_retries"], "nr_tol": tols[0],
        "method": params["electronic_model"]["method"], "basis_functions": params["electronic_model"]["basis_functions_expected"],
    }


def check_input(inp, exp, params):
    bad = []
    mol = inp["molecule"]
    pairs = [("job_id", inp["job_id"], exp["job_id"]), ("R_bohr", mol["R_bohr"], exp["R_bohr"]),
             ("atoms", mol["atoms"], exp["atoms"]), ("charge", mol["charge"], exp["charge"]),
             ("multiplicity", mol["multiplicity"], exp["multiplicity"]), ("electrons", mol["electrons"], exp["electrons"]),
             ("units", mol["units"], exp["coordinate_unit"]), ("engine_options", inp["engine_options"], exp["engine_options"]),
             ("molecule_options", inp["molecule_options"], exp["molecule_options"]), ("threads", inp["threads"], exp["threads"]),
             ("memory", inp["memory"], exp["memory"]), ("method", inp["engine_options"]["reference"].upper(), exp["method"]),
             ("threads_bound", inp["threads"], params["resource_bounds"]["threads"])]
    for name, got, want in pairs:
        if got != want or type(got) is not type(want):
            bad.append(f"input {name} differs from the accepted parameters")
    m = re.fullmatch(r"(\d+) MiB", exp["memory"])
    if not m or int(m.group(1)) != params["resource_bounds"]["engine_memory_mib"] or \
            inp["readback_tolerances"]["memory_bytes"] != int(m.group(1)) * 1024 ** 2:
        bad.append("input memory bytes differ from the accepted engine memory setting")
    if exp["retries"] != 0:
        bad.append("accepted parameters do not set zero retries")
    return bad


# ------------------------------------------------------------------------------------------ static preflight

def resolve_inside(path, prefix_real, hops=8):
    """Follow a symlink chain without leaving the prefix; return the final real path or raise Block."""
    cur = os.path.abspath(path)
    for _ in range(hops):
        if not under(prefix_real, os.path.realpath(os.path.dirname(cur))) or not under(prefix_real, cur):
            raise Block(f"path leaves the prefix: {os.path.basename(path)}")
        st = os.lstat(cur)
        if not stat.S_ISLNK(st.st_mode):
            if not under(prefix_real, os.path.realpath(cur)):
                raise Block(f"path leaves the prefix: {os.path.basename(path)}")
            return os.path.realpath(cur)
        cur = os.path.normpath(os.path.join(os.path.dirname(cur), os.readlink(cur)))
    raise Block(f"too many symbolic links: {os.path.basename(path)}")


def repo_root(start):
    cur = start
    while True:
        if os.path.lexists(os.path.join(cur, ".git")):
            return cur
        nxt = os.path.dirname(cur)
        if nxt == cur:
            return None
        cur = nxt


# ------------------------------------------------------------------------------------------ code provenance

def git_read(repo, *args):
    """Read-only Git query against the repository that holds this driver. Only rev-parse, ls-tree and cat-file are
    permitted, with --no-optional-locks; nothing is written to any index, history or remote."""
    if not args or args[0] not in GIT_ALLOWED:
        raise Block(f"git command not permitted: {args[:1]}")
    git = shutil.which("git")
    if not git:
        return 127, b""
    try:
        res = subprocess.run([git, "--no-optional-locks", "-C", repo] + list(args), capture_output=True,
                             stdin=subprocess.DEVNULL, timeout=60,
                             env={"PATH": os.environ.get("PATH", ""), "LC_ALL": "C", "GIT_OPTIONAL_LOCKS": "0"})
    except (OSError, subprocess.SubprocessError):
        return 126, b""
    return res.returncode, res.stdout


GIT_READ = git_read  # the tests substitute a fixture reader; no test creates or changes a Git repository


def blob_id(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def full_diff(rel, base, cur):
    """Unified diff from the base bytes (None: absent at the base commit) to the current bytes."""
    a = [] if base is None else base.decode("utf-8").splitlines(keepends=True)
    return "".join(difflib.unified_diff(a, cur.decode("utf-8").splitlines(keepends=True),
                                        "/dev/null" if base is None else "a/" + rel, "b/" + rel))


def base_bytes(root, commit, rel):
    rc, out = GIT_READ(root, "ls-tree", "-z", commit, "--", rel)
    if rc != 0:
        raise Block(f"code provenance unresolvable: ls-tree {rel}")
    if not out:
        return None
    meta, _, name = out.rstrip(b"\0").partition(b"\t")
    parts = meta.split()
    if name.decode() != rel or len(parts) != 3 or parts[1] != b"blob":
        raise Block(f"code provenance unresolvable: tree entry {rel}")
    rc, data = GIT_READ(root, "cat-file", "blob", parts[2].decode())
    if rc != 0 or blob_id(data) != parts[2].decode():
        raise Block(f"code provenance unresolvable: base blob of {rel}")
    return data


def build_provenance():
    """Derive the code-provenance record from read-only Git queries and the current bytes. Raises Block if it cannot."""
    root = repo_root(HERE)
    if not root:
        raise Block("code provenance unresolvable: no repository")
    rc, head = GIT_READ(root, "rev-parse", "--verify", "HEAD^{commit}")
    head = head.decode(errors="replace").strip()
    if rc != 0 or not re.fullmatch(r"[0-9a-f]{40}", head):
        raise Block("code provenance unresolvable: HEAD")
    files = []
    for key in PROVENANCE_KEYS:
        path = os.path.realpath(os.path.join(HERE, BUNDLE[key]))
        rel = os.path.relpath(path, root)
        with open(path, "rb") as fh:
            cur = fh.read()
        try:
            base = base_bytes(root, head, rel)
            diff = full_diff(rel, base, cur)
        except UnicodeDecodeError:
            raise Block(f"code provenance unresolvable: {rel} is not UTF-8 text")
        files.append({"key": key, "path": rel, "base_present": base is not None,
                      "base_blob_sha1": blob_id(base) if base is not None else None,
                      "current_sha256": hashlib.sha256(cur).hexdigest(), "current_size": len(cur),
                      "current_bytes_b64": base64.b64encode(cur).decode("ascii"), "diff_unified": diff,
                      "diff_sha256": hashlib.sha256(diff.encode()).hexdigest()})
    return {"schema": "di-mechanosynthesis/h2-phase-a-code-provenance/1", "repository": root, "base_commit": head,
            "coverage": {"paths": [f["path"] for f in files],
                         "why": "the code paths a run uses: the driver executes, the payload runs in the engine process, "
                                "and the input, parameter file and static identity record determine what is run and checked",
                         "not_covered": "the driver interpreter and its standard library, the git program, the engine "
                                        "environment (bound by the static identity record), and every other repository file "
                                        "(the proposal and decision packet are bound by SHA256 in the authorization)"},
            "files": files, "full_diff_sha256": hashlib.sha256("".join(f["diff_unified"] for f in files).encode()).hexdigest()}


def check_provenance(path, bound, digests):
    """BLOCK_LAUNCH unless the bound record exists, matches its digest and equals the record re-derived now."""
    if not (isinstance(path, str) and os.path.isfile(path)):
        raise Block("code provenance absent")
    if sha256_file(path) != bound:
        raise Block("code provenance digest differs from the authorization (bound_sha256.code_provenance)")
    try:
        rec = load_json(path)
    except ValueError:
        raise Block("code provenance malformed")
    fresh = build_provenance()
    if not isinstance(rec, dict) or rec != fresh:
        diff = sorted(k for k in set(fresh) | set(rec if isinstance(rec, dict) else {})
                      if not isinstance(rec, dict) or rec.get(k) != fresh.get(k))
        raise Block(f"code provenance mismatch: {diff}")
    for f in rec["files"]:
        if f["current_sha256"] != digests.get(f["key"]):
            raise Block(f"code provenance mismatch: {f['key']} differs from the bound digest")
    return rec


def network_gate():
    """Driver-performed gate. Returns (ok, reason, observation)."""
    if NETWORK_OBSERVER is None:
        return False, "NETWORK_PREREQUISITE_UNRESOLVED", None
    obs = NETWORK_OBSERVER()
    if not isinstance(obs, dict) or obs.get("offline") is not True:
        return False, "HOST_NOT_OFFLINE", obs
    return True, None, obs


def preflight(interpreter, prefix, runs_root, attempt_created=False):
    """Static checks only. Returns a report; report['ok'] is False on any failure. Spawns no process."""
    checks, digests = [], {}

    def check(cid, ok, detail=""):
        checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "detail": detail})
        return ok

    def guard(cid, fn):
        try:
            res = fn()
            return check(cid, res is None or res is True, "" if res in (None, True) else str(res))
        except (Block, OSError, ValueError, KeyError, TypeError) as exc:
            return check(cid, False, f"{exc.__class__.__name__}: {exc}")

    for key, rel in BUNDLE.items():
        guard(f"bundle.{key}", lambda rel=rel, key=key: digests.__setitem__(key, sha256_file(os.path.join(HERE, rel))))
    ctx = {}

    def load_bundle():
        ctx["params"] = load_json(os.path.join(HERE, BUNDLE["parameters"]))
        ctx["inp"] = load_json(os.path.join(HERE, BUNDLE["input"]))
        ctx["ident"] = load_json(os.path.join(HERE, BUNDLE["static_identity"]))
        ctx["exp"] = derive_expected(ctx["params"])
    if not guard("bundle.parse", load_bundle):
        return {"ok": False, "checks": checks, "digests": digests, "utc": utc()}
    guard("input.matches_parameters", lambda: "; ".join(check_input(ctx["inp"], ctx["exp"], ctx["params"])) or None)
    pexp = ctx["ident"]["preflight_expectations"]
    prefix_real = os.path.realpath(prefix)
    ok_prefix = check("prefix.absolute_normalized", os.path.isabs(prefix) and prefix_real == prefix
                      and os.path.isdir(prefix_real), "prefix must be an absolute, canonical, link-free directory path")
    observed = {}

    def prefix_file(rel):
        real = resolve_inside(os.path.join(prefix_real, rel), prefix_real)
        observed[rel] = sha256_file(real)
        return observed[rel]

    if ok_prefix:
        def interp():
            if os.path.normpath(interpreter) != os.path.join(prefix_real, pexp["interpreter"]) and \
                    os.path.realpath(interpreter) != os.path.join(prefix_real, pexp["interpreter"]):
                return "interpreter is not the bound prefix interpreter"
            real = resolve_inside(interpreter, prefix_real)
            observed[pexp["interpreter"]] = sha256_file(real)
            return None if os.access(real, os.X_OK) else "interpreter not executable"
        guard("interpreter.inside_prefix", interp)
        for pkg, fields in pexp["package_records"].items():
            def rec(pkg=pkg, fields=fields):
                name = f"{fields['name']}-{fields['version']}-{fields['build']}.json"
                real = resolve_inside(os.path.join(prefix_real, "conda-meta", name), prefix_real)
                observed["conda-meta/" + name] = sha256_file(real)  # full-file digest, compared before and after a run
                got = load_json(real)
                diff = [k for k in ("name", "version", "build", "build_number", "channel", "subdir", "sha256")
                        if got.get(k) != fields[k]]
                return f"package record {pkg} differs in {diff}" if diff else None
            guard(f"package.{pkg}", rec)

        def names():
            observed["conda-meta/"] = sorted(os.listdir(resolve_inside(os.path.join(prefix_real, "conda-meta"), prefix_real)))
        guard("package.record_names", names)
        for rel, want in pexp["sha256"].items():
            if rel == pexp["interpreter"]:
                guard(f"sha256.{rel}", lambda rel=rel, want=want: None if observed.get(rel) == want
                      else "interpreter digest differs from the static identity record")
            else:
                guard(f"sha256.{rel}", lambda rel=rel, want=want: None if prefix_file(rel) == want
                      else "digest differs from the static identity record")
    runs_real = os.path.realpath(runs_root)

    def runs():
        if not (os.path.isabs(runs_root) and runs_real == runs_root and os.path.isdir(runs_real)):
            return "runs root must be an existing absolute, canonical, link-free directory"
        if ok_prefix and under(prefix_real, runs_real):
            return "runs root is inside the prefix"
        root = repo_root(HERE)
        if root and under(root, runs_real) and not under(os.path.join(root, ".herd"), runs_real):
            return "runs root is inside the repository's public tree"
        return None
    guard("runs_root.location", runs)
    attempt = os.path.join(runs_real, ctx["inp"]["job_id"])
    if attempt_created is None:
        pass  # post-run state observation: the attempt directory exists by design
    elif attempt_created:
        guard("attempt.fresh", lambda: None if sorted(os.listdir(attempt)) == ["bundle", "code-provenance.json", "payload", "scratch"]
              and os.listdir(os.path.join(attempt, "scratch")) == [] and os.listdir(os.path.join(attempt, "payload")) == []
              else "attempt directory or scratch is not as created by this driver")
    else:
        guard("attempt.absent", lambda: None if not os.path.lexists(attempt)
              else "an attempt record for this job exists; zero retries")
    free = {}

    def space():
        free["bytes"] = shutil.disk_usage(runs_real).free
        return None if free["bytes"] >= FREE_SPACE_FLOOR_BYTES else "free space below the declared floor"
    guard("free_space.floor", space)
    net = {}

    def network():
        ok, reason, net["observation"] = network_gate()
        return None if ok else reason
    guard("network.prerequisite", network)
    return {"ok": all(c["status"] == "PASS" for c in checks), "checks": checks, "digests": digests,
            "observed_sha256": observed, "free_bytes": free.get("bytes"), "network": net.get("observation"), "utc": utc(),
            "interpreter": interpreter, "prefix_realpath": prefix_real, "runs_root": runs_real}


# ------------------------------------------------------------------------------------------ authorization interlock

def build_environment(prefix_real, scratch):
    """The engine environment, built from the allow-list only; nothing is inherited from the caller."""
    env = {"LC_ALL": "C", "OMP_NUM_THREADS": "1", "PATH": os.pathsep.join([os.path.join(prefix_real, "bin"), "/usr/bin", "/bin"]),
           "PSI_SCRATCH": scratch, "TMPDIR": scratch}
    assert sorted(env) == sorted(ALLOWED_ENV)
    return env


def command_for(interpreter, attempt):
    # -I: isolated mode; -B: no bytecode written (keeps the prefix unmodified). Flag semantics are CPython's, not
    # located in a cached source here (proposal section 6).
    return [interpreter, "-I", "-B", os.path.join(attempt, "bundle", BUNDLE["payload"]),
            os.path.join(attempt, "bundle", BUNDLE["input"]), attempt]


def check_authorization(auth_path, args, report):
    """Field and digest interlock. Raises Block on any mismatch. It does not prove that a person authorized anything."""
    auth = load_json(auth_path)
    bad = []
    if auth.get("schema") != "di-mechanosynthesis/h2-phase-a-authorization/1":
        bad.append("schema")
    if auth.get("job_id") != "H2-A-01" or auth.get("max_attempts") != 1:
        bad.append("job_id or max_attempts")
    for key in ("authorized_by", "authorized_utc", "statement"):
        if not isinstance(auth.get(key), str) or not auth[key].strip():
            bad.append(key)
    bound = auth.get("bound_sha256", {})
    if sorted(bound) != BOUND_KEYS:
        bad.append("bound_sha256 keys")
    for key in BUNDLE:
        if bound.get(key) != report["digests"].get(key):
            bad.append(f"bound_sha256.{key}")
    mb_path = auth.get("machine_binding_path", "")
    mb = {}
    if not (isinstance(mb_path, str) and os.path.isfile(mb_path) and sha256_file(mb_path) == bound.get("machine_binding")):
        bad.append("bound_sha256.machine_binding")
    else:
        mb = load_json(mb_path)
    for key, val in (("interpreter", args.interpreter), ("prefix", args.prefix), ("runs_root", args.runs_root)):
        if auth.get(key) != val or mb.get(key) != val:
            bad.append(key)
    ident = load_json(os.path.join(HERE, BUNDLE["static_identity"]))["preflight_expectations"]["sha256"]
    exp = auth.get("expected_static_sha256", {})
    if exp != ident or any(report["observed_sha256"].get(k) != v for k, v in exp.items()):  # digests only
        bad.append("expected_static_sha256")
    attempt = os.path.join(report["runs_root"], "H2-A-01")
    env = build_environment(report["prefix_realpath"], os.path.join(attempt, "scratch"))
    declared = auth.get("environment", {})
    if any(k not in ALLOWED_ENV for k in declared):
        bad.append("environment: undeclared key")
    if declared != env:
        bad.append("environment")
    if mb.get("command") != shlex.join(command_for(args.interpreter, attempt)):
        bad.append("machine_binding.command")
    if bad:
        raise Block("authorization mismatch: " + ", ".join(bad))
    prov = check_provenance(auth.get("code_provenance_path"), bound.get("code_provenance"), report["digests"])
    return auth, env, prov


# ------------------------------------------------------------------------------------------ launch and bound

def group_alive(pgid):
    try:
        os.killpg(pgid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def stop_group(pgid, record, reap):
    """SIGTERM to the group, grace, SIGKILL, then verify that no member of the group remains. `reap` collects the
    direct child's status while waiting, so that an unreaped child is not mistaken for a surviving member."""
    for sig in (signal.SIGTERM, signal.SIGKILL):
        reap()
        if not group_alive(pgid):
            break
        try:
            os.killpg(pgid, sig)
            record.setdefault("signals_sent", []).append({"signal": sig.name, "utc": utc()})
        except ProcessLookupError:
            break
        end = time.monotonic() + TERM_GRACE_S
        while time.monotonic() < end:
            reap()
            if not group_alive(pgid):
                break
            time.sleep(POLL_S)
    record["group_absent_after_cleanup"] = not group_alive(pgid)


def launch(cmd, env, scratch, attempt, wall_s):
    rec = {"command": cmd, "wall_bound_s": wall_s}
    out_fd = os.open(os.path.join(attempt, "engine.stdout"), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    err_fd = os.open(os.path.join(attempt, "engine.stderr"), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    rec["start_utc"] = utc()
    t0 = time.monotonic()
    try:
        proc = subprocess.Popen(cmd, cwd=scratch, env=env, stdin=subprocess.DEVNULL, stdout=out_fd, stderr=err_fd,
                                start_new_session=True, close_fds=True)
    except OSError as exc:
        rec.update({"spawn_error": f"{exc.__class__.__name__}: {exc}", "end_utc": utc()})
        return rec
    finally:
        os.close(out_fd)
        os.close(err_fd)
    pgid = proc.pid  # start_new_session makes the child a session and process-group leader
    rec.update({"pid": proc.pid, "pgid": pgid, "timed_out": False})
    done = {}

    def reap(block=False):
        if "status" not in done:
            pid, st, ru = os.wait4(proc.pid, 0 if block else os.WNOHANG)
            if pid == proc.pid:
                done.update(status=st, rusage=ru, elapsed=time.monotonic() - t0, end_utc=utc())

    while "status" not in done:
        reap()
        if "status" not in done and time.monotonic() - t0 >= wall_s:
            rec["timed_out"] = True
            stop_group(pgid, rec, reap)
            reap(block=True)
        elif "status" not in done:
            time.sleep(POLL_S)
    proc.returncode = os.waitstatus_to_exitcode(done["status"])  # reaped here; Popen must not wait again
    rec.update({"elapsed_s": done["elapsed"], "end_utc": done["end_utc"]})
    if os.WIFSIGNALED(done["status"]):
        rec["signal"] = os.WTERMSIG(done["status"])
    else:
        rec["exit_code"] = os.WEXITSTATUS(done["status"])
    rec["peak_child_rss_raw"] = done["rusage"].ru_maxrss
    rec["peak_child_rss_note"] = "ru_maxrss of the direct child from wait4; an observation only, unit platform-defined"
    if not rec["timed_out"]:
        rec["group_members_after_exit"] = group_alive(pgid)
        if rec["group_members_after_exit"]:
            stop_group(pgid, rec, reap)
    return rec


def inventory(attempt):
    rows = []
    for dirpath, dirnames, filenames in os.walk(attempt, followlinks=False):
        dirnames.sort()
        for name in sorted(filenames) + [d for d in dirnames if os.path.islink(os.path.join(dirpath, d))]:
            path = os.path.join(dirpath, name)
            st = os.lstat(path)
            row = {"path": os.path.relpath(path, attempt), "size": st.st_size}
            if stat.S_ISLNK(st.st_mode):
                row["readlink"] = os.readlink(path)
            elif stat.S_ISREG(st.st_mode):
                row["sha256"] = sha256_file(path)
            rows.append(row)
    return rows


# ------------------------------------------------------------------------------------------ classification

def read_record(payload_dir, name):
    path = os.path.join(payload_dir, name)
    if not os.path.isfile(path):
        return None
    try:
        rec = load_json(path)
    except (OSError, ValueError):
        return {"__malformed__": "unparseable"}
    return rec if isinstance(rec, dict) else {"__malformed__": f"top level is {type(rec).__name__}"}


def is_int(v):
    return isinstance(v, int) and not isinstance(v, bool)


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def is_hex64(v):
    return isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) is not None


TYPES = {"str": lambda v: isinstance(v, str), "int": is_int, "num": is_num, "bool": lambda v: isinstance(v, bool),
         "list": lambda v: isinstance(v, list), "dict": lambda v: isinstance(v, dict), "hex64": is_hex64}
CORE_REL = "lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so"
MODULE_REL = "lib/python3.14/site-packages/psi4/__init__.py"
LIBINT_REL = "lib/libint2.dylib"
BASIS_REL = "share/psi4/basis/sto-3g.gbs"
REHASH = ("bin/python3.14", CORE_REL, LIBINT_REL, "include/libint2/shell.h", BASIS_REL)  # the payload's P0 set
STAGE_SPEC = {
    "pre-import": ("P0-pre-import", {"argv": "list", "environ": "dict", "isolated": "int", "dont_write_bytecode": "int",
                                     "static_sha256": "dict", "executable_realpath": "str", "prefix_realpath": "str",
                                     "cwd": "str", "engine_modules_loaded_before_import": "list"}),
    "i1-identity": ("I1-loaded-identity", {"version": "str", "module_file": "str", "core_file": "str",
                                           "datadir_realpath": "str", "loaded_images": "list"}),
    "i2-configuration": ("I2-configuration", {"banner_text": "str", "banner_sha256": "hex64", "banner_bytes": "int",
                                              "options": "dict", "changed": "dict", "threads": "int", "memory_bytes": "int",
                                              "memory_set_bytes": "int", "natom": "int", "atoms": "list",
                                              "molecular_charge": "int", "multiplicity": "int", "electrons": "int",
                                              "units": "str", "point_group": "str", "com_fixed": "bool",
                                              "orientation_fixed": "bool"}),
    "i3-basis-geometry": ("I3-basis-geometry", {"basis_file_realpath": "str", "basis_file_sha256": "hex64", "nbf": "int",
                                                "cwd_gbs_files": "list", "nuclear_repulsion_hartree": "num"}),
}
RESULT_SPEC = {"job_id": "str", "stage": "str", "energy_called": "bool", "engine_version": "str", "converged": "bool",
               "post_energy_readback": "dict", "banner_preserved_after_energy": "bool", "output_files": "list",
               "energy_call_utc": "str", "energy_return_utc": "str"}
READBACK_SPEC = {"wavefunction_class": "str", "nbf": "int", "nalpha": "int", "nbeta": "int", "natom": "int",
                 "atoms": "list", "options": "dict"}
STOP_STAGES = (("P0-pre-import", "pre-import"), ("import", None), ("I1-loaded-identity", "i1-identity"),
               ("I2-configuration", "i2-configuration"), ("I3-basis-geometry", "i3-basis-geometry"))


def shape(rec, spec, where):
    if not isinstance(rec, dict) or "__malformed__" in rec:
        return [f"malformed {where}"]
    return [f"missing or mistyped {where} field: {k}" for k, t in spec.items() if k not in rec or not TYPES[t](rec[k])]


def scf_options(exp):
    return {k: (v.upper() if isinstance(v, str) else (int(v) if isinstance(v, bool) else v))
            for k, v in exp["engine_options"].items()}


def atoms_ok(atoms, exp, tol, need_symbol=False):
    if not isinstance(atoms, list) or len(atoms) != len(exp["atoms"]):
        return False
    for got, want in zip(atoms, exp["atoms"]):
        xyz = got.get("xyz_bohr") if isinstance(got, dict) else None
        if not isinstance(got, dict) or got.get("label") != want["label"].upper() or \
                (need_symbol and got.get("symbol") != want["element"].upper()) or not isinstance(xyz, list) or \
                len(xyz) != 3 or not all(is_num(a) and math.isfinite(a) and abs(a - b) <= tol for a, b in zip(xyz, want["xyz_bohr"])):
            return False
    return True


def sizeof_fmt(num):
    """Memory text as the v1.11 banner prints it (psi4/header.py 82-87)."""
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f %sB" % (num, unit)
        num /= 1024.0
    return "%.1f YiB" % num


def banner_problems(text, inp, exp, pre):
    """The driver's own re-check of the banner text (v1.11 psi4/header.py 89-140)."""
    lines = [ln.strip() for ln in text.splitlines()]
    bad = []
    if "Psi4: An Open-Source Ab Initio Electronic Structure Package" not in lines:
        bad.append("i2-configuration: banner program line missing")
    if [m.group(1) for ln in lines for m in [re.fullmatch(r"Psi4 (\S+)(?: \S+)?", ln)] if m] != [inp["expected_engine_version"]]:
        bad.append("i2-configuration: banner version line missing or differs")
    fields = {}
    for ln in lines:
        m = re.fullmatch(r"(PSIDATADIR|Threads|Memory):\s+(.+)", ln)
        if m:
            fields.setdefault(m.group(1), []).append(m.group(2))
    dd = fields.get("PSIDATADIR", [])
    if len(dd) != 1 or os.path.realpath(dd[0]) != os.path.join(pre, "share", "psi4"):
        bad.append("i2-configuration: banner PSIDATADIR missing or not <PREFIX>/share/psi4")
    if fields.get("Threads") != [str(exp["threads"])]:
        bad.append("i2-configuration: banner thread line missing or differs")
    if fields.get("Memory") != [sizeof_fmt(inp["readback_tolerances"]["memory_bytes"])]:
        bad.append("i2-configuration: banner memory line missing or differs")
    return bad


def check_p0(rec, launch):
    bad = []
    env, inj = launch.get("environment"), launch.get("platform_injected") or []
    if not isinstance(env, dict):
        return ["pre-import: launch record lacks the environment binding"]
    got = rec["environ"]
    for label, names in (("environment names missing", set(env) - set(got)),
                         ("undeclared environment names", set(got) - set(env) - set(inj)),
                         ("environment values differ", {k for k in env if k in got and got[k] != env[k]})):
        if names:
            bad.append(f"pre-import: {label}: {sorted(names)}")
    if rec["argv"] != list(launch.get("command") or [])[3:]:
        bad.append("pre-import: argv differs from the bound command")
    if rec["executable_realpath"] != launch.get("interpreter_realpath"):
        bad.append("pre-import: executable realpath differs from the bound interpreter")
    if rec["prefix_realpath"] != launch.get("prefix_realpath"):
        bad.append("pre-import: prefix realpath differs from the bound prefix")
    if not isinstance(launch.get("cwd"), str) or os.path.realpath(rec["cwd"]) != os.path.realpath(launch["cwd"]):
        bad.append("pre-import: working directory differs from the bound scratch")
    if rec["isolated"] != 1 or rec["dont_write_bytecode"] != 1:
        bad.append("pre-import: interpreter not started with -I -B")
    if rec["engine_modules_loaded_before_import"] != []:
        bad.append("pre-import: engine module loaded before import")
    want = launch.get("expected_sha256") if isinstance(launch.get("expected_sha256"), dict) else {}
    st = rec["static_sha256"]
    if sorted(st) != sorted(REHASH) or any(st.get(k) != want.get(k) for k in REHASH):
        bad.append("pre-import: static re-hash differs from the launch binding")
    return bad


def check_i1(rec, inp, launch):
    bad = []
    pre = launch.get("prefix_realpath") or ""
    want = launch.get("expected_sha256") if isinstance(launch.get("expected_sha256"), dict) else {}
    if rec["version"] != inp["expected_engine_version"]:
        bad.append("i1-identity: version differs")
    for field, rel in (("module_file", MODULE_REL), ("core_file", CORE_REL), ("datadir_realpath", "share/psi4")):
        if not pre or os.path.realpath(rec[field]) != os.path.join(pre, rel):
            bad.append(f"i1-identity: {field} is not <PREFIX>/{rel}")
    images = rec["loaded_images"]
    if not images:
        return bad + ["i1-identity: loaded-image list empty"]
    if not all(isinstance(i, dict) and isinstance(i.get("path"), str) and isinstance(i.get("realpath"), str)
               and ("sha256" not in i or is_hex64(i["sha256"])) for i in images):
        return bad + ["i1-identity: malformed loaded-image entry"]
    cores = [i for i in images if i["realpath"] == os.path.join(pre, CORE_REL)]
    if not cores:
        bad.append("i1-identity: core extension not among loaded images")
    elif any(i.get("sha256") != want.get(CORE_REL) for i in cores):
        bad.append("i1-identity: loaded core extension digest differs")
    libint = [i for i in images if any(os.path.basename(i[k]).startswith("libint2") for k in ("path", "realpath"))]
    if not libint:
        bad.append("i1-identity: no Libint library among loaded images")
    elif any(i["realpath"] != os.path.join(pre, LIBINT_REL) for i in libint):
        bad.append("i1-identity: a loaded Libint library is not <PREFIX>/lib/libint2.dylib")
    elif any(i.get("sha256") != want.get(LIBINT_REL) for i in libint):
        bad.append("i1-identity: loaded Libint library digest differs")
    return bad


def check_i2(rec, inp, exp, launch):
    bad = []
    tol = inp["readback_tolerances"]["coordinate_abs_bohr"]
    mem = inp["readback_tolerances"]["memory_bytes"]
    if rec["threads"] != exp["threads"] or rec["memory_bytes"] != mem or rec["memory_set_bytes"] != mem:
        bad.append("i2-configuration: threads or memory differ")
    if rec["options"] != scf_options(exp):
        bad.append("i2-configuration: options differ")
    if sorted(rec["changed"]) != sorted(SCF_KEYS) or any(v is not True for v in rec["changed"].values()):
        bad.append("i2-configuration: an option is not marked as changed by the user")
    banner = rec["banner_text"].encode("utf-8")
    if hashlib.sha256(banner).hexdigest() != rec["banner_sha256"] or rec["banner_bytes"] != len(banner):
        bad.append("i2-configuration: banner digest or byte length differs")
    bad += banner_problems(rec["banner_text"], inp, exp, launch.get("prefix_realpath") or "")
    mo = exp["molecule_options"]
    for field, want in (("molecular_charge", exp["charge"]), ("multiplicity", exp["multiplicity"]),
                        ("electrons", exp["electrons"]), ("natom", len(exp["atoms"])),
                        ("units", {"bohr": "Bohr"}.get(exp["coordinate_unit"])), ("com_fixed", mo["no_com"]),
                        ("orientation_fixed", mo["no_reorient"])):
        if rec[field] != want or type(rec[field]) is not type(want):
            bad.append(f"i2-configuration: {field} differs")
    if rec["point_group"].lower() != mo["symmetry"]:
        bad.append("i2-configuration: point_group differs")
    if not atoms_ok(rec["atoms"], exp, tol, need_symbol=True):
        bad.append("i2-configuration: atoms differ")
    return bad


def check_i3(rec, exp, launch):
    bad = []
    pre = launch.get("prefix_realpath") or ""
    want = launch.get("expected_sha256") if isinstance(launch.get("expected_sha256"), dict) else {}
    if not pre or rec["basis_file_realpath"] != os.path.join(pre, BASIS_REL):
        bad.append("i3-basis-geometry: basis file is not <PREFIX>/share/psi4/basis/sto-3g.gbs")
    if rec["basis_file_sha256"] != want.get(BASIS_REL):
        bad.append("i3-basis-geometry: basis file digest differs")
    if rec["cwd_gbs_files"] != []:
        bad.append("i3-basis-geometry: .gbs files present in the working directory")
    if rec["nbf"] != exp["basis_functions"]:
        bad.append("i3-basis-geometry: basis-function count differs")
    nr = rec["nuclear_repulsion_hartree"]
    if not math.isfinite(nr) or abs(nr - 1.0 / exp["R_bohr"]) > exp["nr_tol"]:
        bad.append("i3-basis-geometry: nuclear repulsion differs from 1/R")
    return bad


def validate_stages(recs, inp, exp, launch):
    """Every stage record: shape and types, a passed gate, and each gate-defining value compared with the launch or
    input binding (see the proposal's re-check table for the fields that are recorded but not re-checked)."""
    bad = []
    launch = launch if isinstance(launch, dict) else {}
    for name, (stage, spec) in STAGE_SPEC.items():
        rec = recs.get(name)
        if rec is None:
            bad.append(f"missing provenance: {name} record")
            continue
        problems = shape(rec, spec, name)
        if not problems and (rec.get("stage") != stage or rec.get("problems") != []):
            problems.append(f"{name} record not a passed {stage} gate")
        if not problems:
            problems = {"pre-import": lambda: check_p0(rec, launch), "i1-identity": lambda: check_i1(rec, inp, launch),
                        "i2-configuration": lambda: check_i2(rec, inp, exp, launch),
                        "i3-basis-geometry": lambda: check_i3(rec, exp, launch)}[name]()
        bad += problems
    return bad


def stop_consistent(stop, recs):
    """A stop record must name a known stage; every earlier stage record must be a passed gate; the stopping stage's
    record, if written, must carry the same problems; no later stage record may exist."""
    names = [s for s, _ in STOP_STAGES]
    if stop["stage"] not in names:
        return False
    k = names.index(stop["stage"])
    for i, (stage, rec_name) in enumerate(STOP_STAGES):
        if rec_name is None:
            continue
        rec = recs.get(rec_name)
        if i < k and not (isinstance(rec, dict) and rec.get("stage") == stage and rec.get("problems") == []):
            return False
        if i == k and rec is not None and not (isinstance(rec, dict) and rec.get("problems") == stop["problems"]):
            return False
        if i > k and rec is not None:
            return False
    return True


def _classify(proc, attempt, inp, exp, after, launch, files):
    payload_dir = os.path.join(attempt, "payload")
    failed, quarantine = [], list(after)
    recs = {n: read_record(payload_dir, n + ".json") for n in ("stop-before-energy", "energy-failed", "result") + STAGE_RECORDS}
    if proc.get("group_members_after_exit") or proc.get("group_absent_after_cleanup") is False:
        quarantine.append("process-group members remained after the engine process ended")
    if "spawn_error" in proc:
        return "FAILED", ["spawn failed: " + str(proc["spawn_error"])] + quarantine
    if proc.get("timed_out"):
        return "FAILED", ["timeout"] + quarantine
    if "signal" in proc:
        return "FAILED", [f"terminated by signal {proc['signal']}"] + quarantine
    code = proc.get("exit_code")
    if code == EXIT["STOP_BEFORE_ENERGY"]:
        stop = recs["stop-before-energy"]
        if not shape(stop, {"tier": "str", "stage": "str", "energy_called": "bool", "problems": "list"}, "stop") and \
                stop["tier"] == "STOP_BEFORE_ENERGY" and stop["energy_called"] is False and \
                recs["result"] is None and recs["energy-failed"] is None and stop_consistent(stop, recs):
            return "STOP_BEFORE_ENERGY", [f"stopped at {stop['stage']}"] + [str(x) for x in stop["problems"]] + quarantine
        return "FAILED", ["stop exit code without a valid stop record consistent with the stage records"] + quarantine
    if code == EXIT["FAILED"]:
        ef = recs["energy-failed"] if isinstance(recs["energy-failed"], dict) else {}
        return "FAILED", ["energy call failed: " + str(ef.get("failure", "no failure record"))] + quarantine
    if code != 0:
        return "FAILED", [f"nonzero exit {code}"] + quarantine
    res = recs["result"]
    if res is None or "__malformed__" in res:
        return "QUARANTINE", ["missing provenance: result record " + ("absent" if res is None else res["__malformed__"])] + quarantine
    present = {f.get("path") for f in files if isinstance(f, dict) and is_hex64(f.get("sha256")) and is_int(f.get("size"))}
    quarantine += [f"missing expected output: {o}" for o in EXPECTED_OUTPUTS if o not in present]
    quarantine += validate_stages(recs, inp, exp, launch)
    result_shape = shape(res, RESULT_SPEC, "result")
    quarantine += result_shape
    if "post_energy_error" in res:
        quarantine.append("post-energy read-back incomplete: " + str(res["post_energy_error"]))
    if res.get("job_id") != exp["job_id"] or res.get("stage") != "energy" or res.get("energy_called") is not True:
        quarantine.append("result record does not describe the energy call of this job")
    e = res.get("reported_total_energy_hartree")
    if not is_num(e):
        quarantine.append("missing provenance: reported total energy")
    elif not math.isfinite(e):
        failed.append("nonfinite energy")
    if res.get("converged") is not True:
        failed.append("SCF not converged")
    # The iteration limit is evaluated independently of the raw-consistency check, and both reasons are kept. Fail
    # closed: a finite raw reported value at or above the limit also counts as reaching it, whatever the recorded count.
    it = res.get("scf_iterations")
    raw = res.get("scf_iterations_raw")
    maxiter = inp["engine_options"]["maxiter"]
    count_ok = is_int(it) and it >= 1
    raw_ok = is_num(raw) and math.isfinite(raw)
    if not count_ok:
        quarantine.append("missing provenance: scf_iterations is not a positive integer")
    elif not raw_ok or raw != it:
        quarantine.append("scf_iterations is not consistent with the raw reported value")
    if count_ok and it >= maxiter:
        failed.append("iteration limit reached")
    elif raw_ok and raw >= maxiter:
        failed.append("iteration limit reached by the raw reported value")
    try:
        t_call = datetime.datetime.fromisoformat(res.get("energy_call_utc"))
        t_ret = datetime.datetime.fromisoformat(res.get("energy_return_utc"))
        if t_ret < t_call:
            quarantine.append("energy return time precedes the energy call time")
    except (TypeError, ValueError):
        quarantine.append("missing provenance: energy call or return time")
    nr = res.get("reported_nuclear_repulsion_hartree")
    if nr is None:
        quarantine.append("missing reported nuclear repulsion")
    elif not is_num(nr) or not math.isfinite(nr):
        quarantine.append("nonfinite reported nuclear repulsion")
    elif abs(nr - 1.0 / exp["R_bohr"]) > exp["nr_tol"]:
        quarantine.append("reported nuclear repulsion differs from 1/R beyond tolerance")
    if res.get("engine_version") != inp["expected_engine_version"]:
        quarantine.append("post-energy identity mismatch: engine version")
    post = res.get("post_energy_readback")
    problems = shape(post, READBACK_SPEC, "post-energy read-back")
    quarantine += problems
    if not problems:
        tol = inp["readback_tolerances"]["coordinate_abs_bohr"]
        if post["wavefunction_class"] != exp["method"]:
            quarantine.append("post-energy identity mismatch: reference")
        if post["nbf"] != exp["basis_functions"]:
            quarantine.append("post-energy identity mismatch: basis-function count")
        if post["nalpha"] + post["nbeta"] != exp["electrons"] or (exp["multiplicity"] == 1 and post["nalpha"] != post["nbeta"]):
            quarantine.append("post-energy identity mismatch: electron count or spin")
        if post["natom"] != len(exp["atoms"]) or not atoms_ok(post["atoms"], exp, tol):
            quarantine.append("post-energy identity mismatch: atom count, coordinates or atom labels")
        if post["options"] != scf_options(exp):
            quarantine.append("post-energy identity mismatch: options")
    outs = res.get("output_files")
    if not isinstance(outs, list) or not {"psi4-output.dat", "psi4-output.log"} <= {o for o in outs if isinstance(o, str)}:
        quarantine.append("result record does not list the engine output and log files")
    i2 = recs["i2-configuration"] if isinstance(recs["i2-configuration"], dict) else {}
    banner = i2.get("banner_text").encode("utf-8") if isinstance(i2.get("banner_text"), str) else b""
    try:
        with open(os.path.join(payload_dir, "psi4-output.dat"), "rb") as fh:
            final = fh.read()
    except OSError:
        final = b""
    if res.get("banner_preserved_after_energy") is not True or not banner or not final.startswith(banner):
        quarantine.append("printed banner absent, truncated or inconsistent after the energy call")
    if failed and not result_shape:  # FAILED only on a well-formed result that reports failure
        return "FAILED", failed + quarantine
    if quarantine or failed:
        return "QUARANTINE", quarantine + failed
    return "COMPLETED_PENDING_REVIEW", []


def classify(proc, attempt, inp, exp, after=(), launch=None, files=()):
    """Independent post-run classification from the records. `after` holds driver-observed post-run problems. It never
    raises: any unexpected shape or error gives QUARANTINE with the reason preserved. Returns (tier, reasons)."""
    try:
        return _classify(proc, attempt, inp, exp, list(after), launch, list(files))
    except Exception as exc:  # noqa: BLE001 - classification must always produce a preserved outcome
        return "QUARANTINE", [f"classification error: {exc.__class__.__name__}: {exc}"] + list(after)


# ------------------------------------------------------------------------------------------ run

def write_exclusive(path, obj):
    with open(path, "x") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)
        fh.write("\n")


def emit(obj, code):
    print(json.dumps(obj, indent=1, sort_keys=True))
    return code


def run(args):
    first = preflight(args.interpreter, args.prefix, args.runs_root)
    if not first["ok"]:
        return emit({"tier": "BLOCK_LAUNCH", "reasons": [c for c in first["checks"] if c["status"] == "FAIL"]}, 2)
    try:
        auth, env, prov = check_authorization(args.authorization, args, first)
    except (Block, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return emit({"tier": "BLOCK_LAUNCH", "reasons": [f"{exc.__class__.__name__}: {exc}"]}, 2)
    exp = derive_expected(load_json(os.path.join(HERE, BUNDLE["parameters"])))
    inp = load_json(os.path.join(HERE, BUNDLE["input"]))
    attempt = os.path.join(first["runs_root"], inp["job_id"])
    try:
        os.mkdir(attempt)  # exclusive: an existing attempt record for this job blocks any further launch
    except FileExistsError:
        return emit({"tier": "BLOCK_LAUNCH", "reasons": ["an attempt record for this job exists; zero retries"]}, 2)
    outcome = {"job_id": inp["job_id"], "attempt": attempt, "authorization_sha256": sha256_file(args.authorization),
               "preflight_initial": first, "free_bytes_before": first["free_bytes"]}
    try:
        for sub in ("bundle", "payload", "scratch"):
            os.mkdir(os.path.join(attempt, sub))
        for key in ("payload", "input"):
            dst = os.path.join(attempt, "bundle", BUNDLE[key])
            with open(os.path.join(HERE, BUNDLE[key]), "rb") as src, open(dst, "xb") as out:
                out.write(src.read())
            if sha256_file(dst) != auth["bound_sha256"][key]:
                raise Block(f"bundle copy of {key} differs from the bound digest")
        prov_copy = os.path.join(attempt, "code-provenance.json")  # the bound record, preserved with the attempt
        with open(auth["code_provenance_path"], "rb") as src, open(prov_copy, "xb") as out:
            out.write(src.read())
        if sha256_file(prov_copy) != auth["bound_sha256"]["code_provenance"]:
            raise Block("preserved code-provenance copy differs from the bound digest")
        final = preflight(args.interpreter, args.prefix, args.runs_root, attempt_created=True)
        outcome["preflight_final"] = final
        if not final["ok"] or final["digests"] != first["digests"] or final["observed_sha256"] != first["observed_sha256"] \
                or sorted(os.listdir(attempt)) != ["bundle", "code-provenance.json", "payload", "scratch"]:
            raise Block("final preflight failed or changed")
        scratch = os.path.join(attempt, "scratch")
        cmd = command_for(args.interpreter, attempt)
        launch_record = {
            "job_id": inp["job_id"], "utc": utc(), "command": cmd, "command_shell_form": shlex.join(cmd),
            "cwd": scratch, "environment": env, "allowed_environment": list(ALLOWED_ENV),
            "platform_injected": list(PLATFORM_INJECTED), "bound_sha256": auth["bound_sha256"],
            "expected_sha256": auth["expected_static_sha256"], "prefix_realpath": final["prefix_realpath"],
            "interpreter_realpath": os.path.realpath(args.interpreter), "nuclear_repulsion_abs_tol_hartree": exp["nr_tol"],
            "wall_bound_s": exp["wall_seconds"], "free_bytes_before": final["free_bytes"], "max_attempts": 1,
            "code_provenance": {"sha256": auth["bound_sha256"]["code_provenance"], "base_commit": prov["base_commit"],
                                "paths": prov["coverage"]["paths"], "full_diff_sha256": prov["full_diff_sha256"]}}
        write_exclusive(os.path.join(attempt, "launch-record.json"), launch_record)
    except (Block, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        outcome.update({"tier": "BLOCK_LAUNCH", "reasons": [f"{exc.__class__.__name__}: {exc}"],
                        "note": "no engine process was launched; this attempt record still blocks any relaunch"})
        write_exclusive(os.path.join(attempt, "outcome.json"), outcome)
        return emit({"tier": "BLOCK_LAUNCH", "reasons": outcome["reasons"]}, 2)
    try:
        proc = launch(cmd, env, scratch, attempt, exp["wall_seconds"])
    except Exception as exc:  # noqa: BLE001 - an outcome is written whatever happens after launch
        proc = {"spawn_error": f"driver error during launch: {exc.__class__.__name__}: {exc}"}
    outcome["process"] = proc
    after = []
    try:
        outcome["free_bytes_after"] = shutil.disk_usage(attempt).free
        post = preflight(args.interpreter, args.prefix, args.runs_root, attempt_created=None)
        outcome["post_run_checks"] = post  # full check list, preserved
        for c in post["checks"]:
            if c["status"] == "FAIL" and c["id"].split(".")[0] in POST_RUN_CHECK_GROUPS:
                after.append(f"post-run check failed: {c['id']}: {c['detail']}")
        changed = sorted(k for k in set(post["observed_sha256"]) | set(final["observed_sha256"])
                         if post["observed_sha256"].get(k) != final["observed_sha256"].get(k))
        if changed:
            after.append(f"prefix package records or bound files changed during the run: {changed}")
        if post["digests"] != final["digests"]:
            after.append("bundle files changed during the run")
    except Exception as exc:  # noqa: BLE001
        after.append(f"post-run checks could not be completed: {exc.__class__.__name__}: {exc}")
    try:
        files = inventory(attempt)
    except Exception as exc:  # noqa: BLE001
        files = []
        after.append(f"output inventory could not be completed: {exc.__class__.__name__}: {exc}")
    tier, reasons = classify(proc, attempt, inp, exp, after, launch_record, files)
    outcome.update({"tier": tier, "reasons": reasons, "files": files, "utc": utc(),
                    "rule": "stop, keep all output, mark remaining points NOT_RUN, change no setting",
                    "remaining_points": "none in Phase A; Phase B is NOT_RUN and needs a separate decision"})
    write_exclusive(os.path.join(attempt, "outcome.json"), outcome)
    return emit({"tier": tier, "reasons": reasons, "outcome": os.path.join(attempt, "outcome.json")}, EXIT[tier])


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"usage error: {message}", file=sys.stderr)
        sys.exit(64)


def main(argv=None):
    p = Parser(prog="h2_phase_a_driver.py", description="H2-A-01 control driver (no executable default)")
    sub = p.add_subparsers(dest="mode", required=True)
    cp = sub.add_parser("code-provenance")
    cp.add_argument("--out", required=True)
    for mode in ("preflight", "run"):
        s = sub.add_parser(mode)
        s.add_argument("--interpreter", required=True)
        s.add_argument("--prefix", required=True)
        s.add_argument("--runs-root", required=True)
        if mode == "run":
            s.add_argument("--authorization", required=True)
    args = p.parse_args(argv)
    if args.mode == "code-provenance":
        try:
            rec = build_provenance()
            with open(args.out, "x") as fh:
                json.dump(rec, fh, indent=1, sort_keys=True)
                fh.write("\n")
        except (Block, OSError) as exc:
            return emit({"code_provenance": "NOT_WRITTEN", "reason": f"{exc.__class__.__name__}: {exc}"}, 2)
        return emit({"code_provenance": "WRITTEN", "out": args.out, "sha256": sha256_file(args.out),
                     "base_commit": rec["base_commit"], "paths": rec["coverage"]["paths"]}, 0)
    if args.mode == "preflight":
        rep = preflight(args.interpreter, args.prefix, args.runs_root)
        return emit({"tier": "PASS" if rep["ok"] else "BLOCK_LAUNCH", "report": rep}, 0 if rep["ok"] else 2)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
