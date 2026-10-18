"""Route-R2 control driver for job H2-A-01 (prospective; NOT_RUN; PROPOSED_NOT_AUTHORIZED; [AGENT]). Standard library
only; never imports an engine.

usage:
  h2_phase_a_r2_driver.py preflight --interpreter PATH --prefix PATH --runs-root PATH
  h2_phase_a_r2_driver.py code-provenance --out PATH
  h2_phase_a_r2_driver.py run --interpreter PATH --prefix PATH --runs-root PATH --authorization PATH

This driver composes the accepted Phase A driver instead of copying it. It reads ../phase-a/h2_phase_a_driver.py once
as bytes, checks them against the pinned SHA256 and executes exactly those bytes into a fresh module object; on a
mismatch or read failure it refuses (exit 2) without executing them. It reuses the accepted static checks, input
derivation, environment, command, launch, process-group cleanup, inventory and classification unchanged, and adds:
- the method-revision gate. R2_METHOD_DECISION binds the SHA256 of the method revision that a person approved and of
  the human approval record H2-R2-METHOD-HUMAN-APPROVAL.md. The gate passes only while both files on disk have exactly
  those digests, and no field of an authorization file can satisfy it. Were R2_METHOD_DECISION None, every launch
  would be refused with NETWORK_PREREQUISITE_UNRESOLVED. The accepted check network.prerequisite is replaced by this
  gate and is kept verbatim in the report under replaced_base_checks;
- the launch wrapper: the engine command runs under /usr/bin/sandbox-exec with the bound profile h2-r2-sandbox.sb,
  copied into the attempt, and with write parameters for the attempt's payload/ and scratch/ directories only;
- static re-checks of sandbox-exec and of the OS build against h2-r2-platform-identity.json, before launch,
  immediately before spawn and after the process ends;
- post-run observations of the write bound inside the attempt. They observe state; they detect no attempt. Each
  discrepancy is added as a reason to the accepted classification, which is applied unchanged.

The sandbox refuses covered operations; it does not detect them. A refusal that makes the engine fail is classified by
the accepted rules (FAILED, or STOP_BEFORE_ENERGY when the payload stops at a gate). This driver neither detects a
refused operation nor writes any record of it, and it reads no system log. The engine's stdout, stderr and output
files are kept and inventoried but not analysed for refusals; their silence does not show that no attempt was made.
The interlock checks bytes and fields only. It cannot show that a person authorized anything.

Exit codes as in the accepted driver: 0 completed (pending independent review), 2 BLOCK_LAUNCH, 3 STOP_BEFORE_ENERGY,
4 FAILED, 5 QUARANTINE, 64 usage error. Paths are relative to this file; there are no machine paths.
"""
import argparse
import base64
import hashlib
import json
import os
import plistlib
import re
import shlex
import shutil
import stat
import sys
import types

HERE = os.path.dirname(os.path.abspath(__file__))
ACCEPTED_DRIVER = os.path.join("..", "phase-a", "h2_phase_a_driver.py")
ACCEPTED_DRIVER_SHA256 = "6dcb4845e3b4b29f89dc4027274675e24c1152508828b1230857baac58b9aa7d"
# Route-R2 method decision: the SHA256 of the method revision a person approved (H2-R2-METHOD-REVISION.md) and of the
# human approval record (H2-R2-METHOD-HUMAN-APPROVAL.md), which binds the revision's digest and not this file's. The
# gate below requires both files on disk to have exactly these digests, and the authorization must carry equal values
# in bound_sha256.r2_method_revision and bound_sha256.method_revision_approval. None would fail the gate.
R2_METHOD_DECISION = {"method_revision_sha256": "9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc",
                      "approval_record_sha256": "e4897a80869bc04d6ece9a8be75673085e18ddb1b07df1df5e71fd4b76f10d7c"}
DECISION_KEYS = ("approval_record_sha256", "method_revision_sha256")
SANDBOX_EXEC = "/usr/bin/sandbox-exec"
SYSTEM_VERSION_PLIST = "/System/Library/CoreServices/SystemVersion.plist"
R2_BUNDLE = {"r2_driver": os.path.basename(__file__), "r2_profile": "h2-r2-sandbox.sb",
             "r2_platform_identity": "h2-r2-platform-identity.json", "r2_method_revision": "H2-R2-METHOD-REVISION.md",
             "r2_run_proposal": "H2-A-R2-RUN-PROPOSAL.md", "r2_decision_packet": "H2-A-R2-DECISION-PACKET.md",
             "method_revision_approval": "H2-R2-METHOD-HUMAN-APPROVAL.md"}
PROFILE_PARAMS = {"H2_PAYLOAD_DIR": "payload", "H2_SCRATCH_DIR": "scratch"}  # the only write parameters
REPLACED_BASE_CHECKS = ("network.prerequisite",)
AUTH_SCHEMA = "di-mechanosynthesis/h2-phase-a-r2-authorization/1"
# Code paths a run uses: both drivers execute, the payload runs in the engine process, the input, parameter file and
# static identity record determine what is run and checked, and the profile and platform identity record determine the
# sandbox the engine runs in.
PROVENANCE_KEYS = ("r2_driver", "driver", "payload", "input", "parameters", "static_identity", "r2_profile",
                   "r2_platform_identity")
ATTEMPT_ROOT_ENTRIES = ("bundle", "code-provenance.json", "engine.stderr", "engine.stdout", "launch-record.json",
                        "payload", "scratch")
A = None  # the accepted driver module, executed once from the pinned bytes by accepted()


class PinError(Exception):
    """The accepted driver's bytes could not be read or differ from the pinned digest; they were not executed."""


def accepted():
    """Read the accepted driver once, verify the pinned digest, then execute exactly those bytes into a new module."""
    global A
    if A is None:
        path = os.path.normpath(os.path.join(HERE, ACCEPTED_DRIVER))
        try:
            with open(path, "rb") as fh:
                data = fh.read()
        except OSError as exc:
            raise PinError(f"accepted driver unreadable: {exc.__class__.__name__}") from None
        got = hashlib.sha256(data).hexdigest()
        if got != ACCEPTED_DRIVER_SHA256:
            raise PinError(f"accepted driver SHA256 {got} differs from the pinned {ACCEPTED_DRIVER_SHA256}; "
                           "its bytes were not executed")
        mod = types.ModuleType("h2_phase_a_driver")
        mod.__file__ = path
        exec(compile(data, path, "exec", dont_inherit=True), mod.__dict__)
        A = mod
    return A


def r2_path(key):
    return os.path.join(HERE, R2_BUNDLE[key])


def is_hex64(v):
    return isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v) is not None


# ------------------------------------------------------------------------------------------ composed preflight

def observe_platform():
    """Static only: lstat and hash of sandbox-exec, and the OS version read from SystemVersion.plist."""
    st = os.lstat(SANDBOX_EXEC)
    regular = stat.S_ISREG(st.st_mode)
    obs = {"sandbox_exec_path": SANDBOX_EXEC, "sandbox_exec_regular_not_link": regular,
           "sandbox_exec_executable": regular and os.access(SANDBOX_EXEC, os.X_OK), "sandbox_exec_size": st.st_size,
           "sandbox_exec_sha256": A.sha256_file(SANDBOX_EXEC) if regular else None}
    with open(SYSTEM_VERSION_PLIST, "rb") as fh:
        pl = plistlib.load(fh)
    if not isinstance(pl, dict):
        raise ValueError(f"SystemVersion.plist top level is {type(pl).__name__}, not a dictionary")
    obs.update(os_product_version=pl.get("ProductVersion"), os_build_version=pl.get("ProductBuildVersion"))
    return obs


def decision_problem(digests):
    """None when the method-revision decision is set, well formed and binds the current method-revision and
    approval-record bytes."""
    d = R2_METHOD_DECISION
    if d is None:
        return ("NETWORK_PREREQUISITE_UNRESOLVED: the route-R2 method revision has not been decided by a person "
                "(R2_METHOD_DECISION is unset); no authorization field can satisfy this check")
    if not isinstance(d, dict) or sorted(d) != sorted(DECISION_KEYS) or not all(is_hex64(d[k]) for k in DECISION_KEYS):
        return "R2_METHOD_DECISION is malformed"
    if d["method_revision_sha256"] != digests.get("r2_method_revision"):
        return "R2_METHOD_DECISION binds method-revision bytes other than the current H2-R2-METHOD-REVISION.md"
    if digests.get("method_revision_approval") is None:
        return "the human approval record H2-R2-METHOD-HUMAN-APPROVAL.md is absent or unreadable"
    if d["approval_record_sha256"] != digests["method_revision_approval"]:
        return "R2_METHOD_DECISION binds approval-record bytes other than the current H2-R2-METHOD-HUMAN-APPROVAL.md"
    return None


def preflight(interpreter, prefix, runs_root, attempt_created=False):
    """The accepted static preflight with network.prerequisite replaced by the r2.* checks. Spawns no process."""
    rep = A.preflight(interpreter, prefix, runs_root, attempt_created)
    checks = [c for c in rep["checks"] if c["id"] not in REPLACED_BASE_CHECKS]
    replaced = [c for c in rep["checks"] if c["id"] in REPLACED_BASE_CHECKS]
    digests = dict(rep.get("digests", {}))
    ctx = {}

    def check(cid, ok, detail=""):
        checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "detail": detail})

    def guard(cid, fn):
        try:
            res = fn()
            check(cid, res is None, "" if res is None else str(res))
        except (A.Block, OSError, ValueError, KeyError, TypeError, AttributeError, plistlib.InvalidFileException) as exc:
            check(cid, False, f"{exc.__class__.__name__}: {exc}")

    guard("r2.accepted_driver_pin", lambda: None if digests.get("driver") == ACCEPTED_DRIVER_SHA256
          else "accepted driver bytes on disk differ from the pinned digest")
    for key in R2_BUNDLE:
        guard(f"r2.bundle.{key}", lambda key=key: digests.__setitem__(key, A.sha256_file(r2_path(key))))

    def platform():
        ctx["record"] = A.load_json(r2_path("r2_platform_identity"))
        ctx["obs"] = observe_platform()
    guard("r2.platform_identity.parse", platform)

    def sandbox_exec():
        if "obs" not in ctx:
            return "platform identity record or observation unavailable"
        want, obs = ctx["record"]["sandbox_exec"], ctx["obs"]
        if not (obs["sandbox_exec_regular_not_link"] and obs["sandbox_exec_executable"]):
            return "sandbox-exec is not an executable regular file"
        if want["path"] != SANDBOX_EXEC or want["size"] != obs["sandbox_exec_size"] or \
                want["sha256"] != obs["sandbox_exec_sha256"]:
            return "sandbox-exec path, size or SHA256 differs from the platform identity record"
        return None
    guard("r2.sandbox_exec", sandbox_exec)

    def os_build():
        if "obs" not in ctx:
            return "platform identity record or observation unavailable"
        want, obs = ctx["record"]["operating_system"], ctx["obs"]
        if (want["ProductVersion"], want["ProductBuildVersion"]) != (obs["os_product_version"], obs["os_build_version"]):
            return "OS version or build differs from the platform identity record"
        return None
    guard("r2.os_build", os_build)
    guard("r2.method_revision_decision", lambda: decision_problem(digests))
    if attempt_created is True:
        def bundle_fresh():
            attempt = os.path.join(rep["runs_root"], "H2-A-01")
            want = sorted([A.BUNDLE["payload"], A.BUNDLE["input"], R2_BUNDLE["r2_profile"]])
            return None if sorted(os.listdir(os.path.join(attempt, "bundle"))) == want \
                else "attempt bundle is not as created by this driver"
        guard("r2.attempt.bundle_fresh", bundle_fresh)
    rep.update(checks=checks, replaced_base_checks=replaced, digests=digests, r2_platform_observed=ctx.get("obs"),
               r2_method_decision=R2_METHOD_DECISION, ok=all(c["status"] == "PASS" for c in checks))
    return rep


# ------------------------------------------------------------------------------------------ code provenance

def provenance_path(key):
    return os.path.realpath(os.path.join(A.HERE, A.BUNDLE[key]) if key in A.BUNDLE else r2_path(key))


def build_provenance():
    """The accepted record's construction over the eight R2 code paths, with the accepted read-only Git functions."""
    root = A.repo_root(HERE)
    if not root:
        raise A.Block("code provenance unresolvable: no repository")
    rc, head = A.GIT_READ(root, "rev-parse", "--verify", "HEAD^{commit}")
    head = head.decode(errors="replace").strip()
    if rc != 0 or not re.fullmatch(r"[0-9a-f]{40}", head):
        raise A.Block("code provenance unresolvable: HEAD")
    files = []
    for key in PROVENANCE_KEYS:
        rel = os.path.relpath(provenance_path(key), root)
        with open(provenance_path(key), "rb") as fh:
            cur = fh.read()
        try:
            base = A.base_bytes(root, head, rel)
            diff = A.full_diff(rel, base, cur)
        except UnicodeDecodeError:
            raise A.Block(f"code provenance unresolvable: {rel} is not UTF-8 text")
        files.append({"key": key, "path": rel, "base_present": base is not None,
                      "base_blob_sha1": A.blob_id(base) if base is not None else None,
                      "current_sha256": hashlib.sha256(cur).hexdigest(), "current_size": len(cur),
                      "current_bytes_b64": base64.b64encode(cur).decode("ascii"), "diff_unified": diff,
                      "diff_sha256": hashlib.sha256(diff.encode()).hexdigest()})
    return {"schema": "di-mechanosynthesis/h2-phase-a-r2-code-provenance/1", "repository": root, "base_commit": head,
            "coverage": {"paths": [f["path"] for f in files],
                         "why": "the code paths a route-R2 run uses: both drivers execute, the payload runs in the engine "
                                "process, the input, parameter file and static identity record determine what is run and "
                                "checked, and the profile and platform identity record determine the sandbox",
                         "not_covered": "the driver interpreter and its standard library, the git program, sandbox-exec "
                                        "and the OS (bound by the platform identity record), the engine environment "
                                        "(bound by the static identity record), and every other repository file (the "
                                        "method revision, its approval record, proposals and decision packets are "
                                        "bound by SHA256 in the authorization)"},
            "files": files, "full_diff_sha256": hashlib.sha256("".join(f["diff_unified"] for f in files).encode()).hexdigest()}


def check_provenance(path, bound, digests):
    """BLOCK_LAUNCH unless the bound record exists, matches its digest and equals the record re-derived now."""
    if not (isinstance(path, str) and os.path.isfile(path)):
        raise A.Block("code provenance absent")
    if A.sha256_file(path) != bound:
        raise A.Block("code provenance digest differs from the authorization (bound_sha256.code_provenance)")
    try:
        rec = A.load_json(path)
    except ValueError:
        raise A.Block("code provenance malformed")
    fresh = build_provenance()
    if not isinstance(rec, dict) or rec != fresh:
        diff = sorted(k for k in set(fresh) | set(rec if isinstance(rec, dict) else {})
                      if not isinstance(rec, dict) or rec.get(k) != fresh.get(k))
        raise A.Block(f"code provenance mismatch: {diff}")
    for f in rec["files"]:
        if f["current_sha256"] != digests.get(f["key"]):
            raise A.Block(f"code provenance mismatch: {f['key']} differs from the bound digest")
    return rec


# ------------------------------------------------------------------------------------------ authorization interlock

def bound_keys():
    return sorted(list(A.BUNDLE) + list(R2_BUNDLE) + ["machine_binding", "code_provenance"])


def launched_argv(interpreter, attempt):
    """sandbox-exec with the attempt's profile copy and the two write parameters, then the accepted engine command."""
    params = []
    for name, sub in PROFILE_PARAMS.items():
        params += ["-D", f"{name}={os.path.join(attempt, sub)}"]
    return [SANDBOX_EXEC, "-f", os.path.join(attempt, "bundle", R2_BUNDLE["r2_profile"])] + params + \
        A.command_for(interpreter, attempt)


def check_authorization(auth_path, args, report):
    """Field and digest interlock. Raises Block on any mismatch. It does not prove that a person authorized anything."""
    auth = A.load_json(auth_path)
    bad = []
    if auth.get("schema") != AUTH_SCHEMA:
        bad.append("schema")
    if auth.get("job_id") != "H2-A-01" or auth.get("max_attempts") != 1:
        bad.append("job_id or max_attempts")
    for key in ("authorized_by", "authorized_utc", "statement"):
        if not isinstance(auth.get(key), str) or not auth[key].strip():
            bad.append(key)
    bound = auth.get("bound_sha256", {})
    if sorted(bound) != bound_keys():
        bad.append("bound_sha256 keys")
    for key in list(A.BUNDLE) + list(R2_BUNDLE):
        if bound.get(key) != report["digests"].get(key):
            bad.append(f"bound_sha256.{key}")
    if decision_problem(report["digests"]) is not None or \
            bound.get("method_revision_approval") != R2_METHOD_DECISION["approval_record_sha256"]:
        bad.append("bound_sha256.method_revision_approval")
    mb_path = auth.get("machine_binding_path", "")
    mb = {}
    if not (isinstance(mb_path, str) and os.path.isfile(mb_path) and A.sha256_file(mb_path) == bound.get("machine_binding")):
        bad.append("bound_sha256.machine_binding")
    else:
        mb = A.load_json(mb_path)
    for key, val in (("interpreter", args.interpreter), ("prefix", args.prefix), ("runs_root", args.runs_root)):
        if auth.get(key) != val or mb.get(key) != val:
            bad.append(key)
    ident = A.load_json(os.path.join(A.HERE, A.BUNDLE["static_identity"]))["preflight_expectations"]["sha256"]
    exp = auth.get("expected_static_sha256", {})
    if exp != ident or any(report["observed_sha256"].get(k) != v for k, v in exp.items()):
        bad.append("expected_static_sha256")
    attempt = os.path.join(report["runs_root"], "H2-A-01")
    env = A.build_environment(report["prefix_realpath"], os.path.join(attempt, "scratch"))
    declared = auth.get("environment", {})
    if any(k not in A.ALLOWED_ENV for k in declared):
        bad.append("environment: undeclared key")
    if declared != env:
        bad.append("environment")
    if mb.get("command") != shlex.join(launched_argv(args.interpreter, attempt)):
        bad.append("machine_binding.command")
    if bad:
        raise A.Block("authorization mismatch: " + ", ".join(bad))
    prov = check_provenance(auth.get("code_provenance_path"), bound.get("code_provenance"), report["digests"])
    return auth, env, prov


# ------------------------------------------------------------------------------------------ post-run observation

def attempt_observation(attempt, bound):
    """State of the attempt root and bundle/ after the process ended, and the attempt copies against their digests.
    This observes the write bound inside the attempt at one instant; it detects no attempt to write."""
    bad = []
    extra = sorted(set(os.listdir(attempt)) - set(ATTEMPT_ROOT_ENTRIES))
    if extra:
        bad.append(f"unexpected entries in the attempt root: {extra}")
    want = {os.path.basename(p) for p in bound if p.startswith("bundle" + os.sep)}
    extra = sorted(set(os.listdir(os.path.join(attempt, "bundle"))) - want)
    if extra:
        bad.append(f"unexpected entries in the attempt bundle: {extra}")
    for rel, digest in sorted(bound.items()):
        path = os.path.join(attempt, rel)
        if not (os.path.lexists(path) and stat.S_ISREG(os.lstat(path).st_mode) and A.sha256_file(path) == digest):
            bad.append(f"attempt copy missing or changed: {rel}")
    return bad


# ------------------------------------------------------------------------------------------ run

def run(args):
    try:
        first = preflight(args.interpreter, args.prefix, args.runs_root)
    except Exception as exc:  # noqa: BLE001 - an unexpected error before any attempt exists is a structured refusal
        return A.emit({"tier": "BLOCK_LAUNCH", "reasons": [f"preflight error: {exc.__class__.__name__}: {exc}"]}, 2)
    if not first["ok"]:
        return A.emit({"tier": "BLOCK_LAUNCH", "reasons": [c for c in first["checks"] if c["status"] == "FAIL"]}, 2)
    try:
        auth, env, prov = check_authorization(args.authorization, args, first)
    except (A.Block, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return A.emit({"tier": "BLOCK_LAUNCH", "reasons": [f"{exc.__class__.__name__}: {exc}"]}, 2)
    exp = A.derive_expected(A.load_json(os.path.join(A.HERE, A.BUNDLE["parameters"])))
    inp = A.load_json(os.path.join(A.HERE, A.BUNDLE["input"]))
    attempt = os.path.join(first["runs_root"], inp["job_id"])
    try:
        os.mkdir(attempt)  # exclusive: an existing attempt record for this job blocks any further launch
    except FileExistsError:
        return A.emit({"tier": "BLOCK_LAUNCH", "reasons": ["an attempt record for this job exists; zero retries"]}, 2)
    outcome = {"job_id": inp["job_id"], "attempt": attempt, "authorization_sha256": A.sha256_file(args.authorization),
               "preflight_initial": first, "free_bytes_before": first["free_bytes"], "route": "R2"}
    copies = {"payload": os.path.join(A.HERE, A.BUNDLE["payload"]), "input": os.path.join(A.HERE, A.BUNDLE["input"]),
              "r2_profile": r2_path("r2_profile")}
    bound_copies = {}
    try:
        for sub in ("bundle", "payload", "scratch"):
            os.mkdir(os.path.join(attempt, sub))
        for key, src_path in copies.items():
            rel = os.path.join("bundle", os.path.basename(src_path))
            with open(src_path, "rb") as src, open(os.path.join(attempt, rel), "xb") as out:
                out.write(src.read())
            if A.sha256_file(os.path.join(attempt, rel)) != auth["bound_sha256"][key]:
                raise A.Block(f"bundle copy of {key} differs from the bound digest")
            bound_copies[rel] = auth["bound_sha256"][key]
        prov_copy = os.path.join(attempt, "code-provenance.json")  # the bound record, preserved with the attempt
        with open(auth["code_provenance_path"], "rb") as src, open(prov_copy, "xb") as out:
            out.write(src.read())
        if A.sha256_file(prov_copy) != auth["bound_sha256"]["code_provenance"]:
            raise A.Block("preserved code-provenance copy differs from the bound digest")
        bound_copies["code-provenance.json"] = auth["bound_sha256"]["code_provenance"]
        final = preflight(args.interpreter, args.prefix, args.runs_root, attempt_created=True)
        outcome["preflight_final"] = final
        if not final["ok"] or final["digests"] != first["digests"] or final["observed_sha256"] != first["observed_sha256"] \
                or final["r2_platform_observed"] != first["r2_platform_observed"] \
                or sorted(os.listdir(attempt)) != ["bundle", "code-provenance.json", "payload", "scratch"]:
            raise A.Block("final preflight failed or changed")
        scratch = os.path.join(attempt, "scratch")
        cmd = A.command_for(args.interpreter, attempt)
        argv = launched_argv(args.interpreter, attempt)
        obs = final["r2_platform_observed"]
        launch_record = {
            "job_id": inp["job_id"], "utc": A.utc(), "command": cmd, "command_shell_form": shlex.join(cmd),
            "cwd": scratch, "environment": env, "allowed_environment": list(A.ALLOWED_ENV),
            "platform_injected": list(A.PLATFORM_INJECTED), "bound_sha256": auth["bound_sha256"],
            "expected_sha256": auth["expected_static_sha256"], "prefix_realpath": final["prefix_realpath"],
            "interpreter_realpath": os.path.realpath(args.interpreter), "nuclear_repulsion_abs_tol_hartree": exp["nr_tol"],
            "wall_bound_s": exp["wall_seconds"], "free_bytes_before": final["free_bytes"], "max_attempts": 1,
            "code_provenance": {"sha256": auth["bound_sha256"]["code_provenance"], "base_commit": prov["base_commit"],
                                "paths": prov["coverage"]["paths"], "full_diff_sha256": prov["full_diff_sha256"]},
            "sandbox_wrapper": {"program": SANDBOX_EXEC, "profile": os.path.join(attempt, "bundle", R2_BUNDLE["r2_profile"]),
                                "parameters": {k: os.path.join(attempt, v) for k, v in PROFILE_PARAMS.items()},
                                "note": "command is the engine command; launched_argv is what is spawned"},
            "launched_argv": argv, "launched_shell_form": shlex.join(argv),
            "r2_profile_sha256": auth["bound_sha256"]["r2_profile"],
            "r2_platform_identity_sha256": auth["bound_sha256"]["r2_platform_identity"],
            "sandbox_exec_sha256": obs["sandbox_exec_sha256"], "os_product_version": obs["os_product_version"],
            "os_build_version": obs["os_build_version"], "r2_method_decision": R2_METHOD_DECISION}
        A.write_exclusive(os.path.join(attempt, "launch-record.json"), launch_record)
        bound_copies["launch-record.json"] = A.sha256_file(os.path.join(attempt, "launch-record.json"))
    except (A.Block, OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        outcome.update({"tier": "BLOCK_LAUNCH", "reasons": [f"{exc.__class__.__name__}: {exc}"],
                        "note": "no engine process was launched; this attempt record still blocks any relaunch"})
        A.write_exclusive(os.path.join(attempt, "outcome.json"), outcome)
        return A.emit({"tier": "BLOCK_LAUNCH", "reasons": outcome["reasons"]}, 2)
    try:
        proc = A.launch(argv, env, scratch, attempt, exp["wall_seconds"])
    except Exception as exc:  # noqa: BLE001 - an outcome is written whatever happens after launch
        proc = {"spawn_error": f"driver error during launch: {exc.__class__.__name__}: {exc}"}
    outcome["process"] = proc
    after = []
    groups = tuple(g for g in A.POST_RUN_CHECK_GROUPS if g != "network") + ("r2",)
    try:
        outcome["free_bytes_after"] = shutil.disk_usage(attempt).free
        post = preflight(args.interpreter, args.prefix, args.runs_root, attempt_created=None)
        outcome["post_run_checks"] = post  # full check list, preserved
        for c in post["checks"]:
            if c["status"] == "FAIL" and c["id"].split(".")[0] in groups:
                after.append(f"post-run check failed: {c['id']}: {c['detail']}")
        changed = sorted(k for k in set(post["observed_sha256"]) | set(final["observed_sha256"])
                         if post["observed_sha256"].get(k) != final["observed_sha256"].get(k))
        if changed:
            after.append(f"prefix package records or bound files changed during the run: {changed}")
        if post["digests"] != final["digests"]:
            after.append("bundle files changed during the run")
        if post["r2_platform_observed"] != final["r2_platform_observed"]:
            after.append("sandbox-exec or OS version observation changed during the run")
    except Exception as exc:  # noqa: BLE001
        after.append(f"post-run checks could not be completed: {exc.__class__.__name__}: {exc}")
    try:
        after += attempt_observation(attempt, bound_copies)
    except Exception as exc:  # noqa: BLE001
        after.append(f"attempt observation could not be completed: {exc.__class__.__name__}: {exc}")
    try:
        files = A.inventory(attempt)
    except Exception as exc:  # noqa: BLE001
        files = []
        after.append(f"output inventory could not be completed: {exc.__class__.__name__}: {exc}")
    tier, reasons = A.classify(proc, attempt, inp, exp, after, launch_record, files)
    outcome.update({"tier": tier, "reasons": reasons, "files": files, "utc": A.utc(),
                    "rule": "stop, keep all output, mark remaining points NOT_RUN, change no setting",
                    "remaining_points": "none in Phase A; Phase B is NOT_RUN and needs a separate decision"})
    A.write_exclusive(os.path.join(attempt, "outcome.json"), outcome)
    return A.emit({"tier": tier, "reasons": reasons, "outcome": os.path.join(attempt, "outcome.json")}, A.EXIT[tier])


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"usage error: {message}", file=sys.stderr)
        sys.exit(64)


def main(argv=None):
    p = Parser(prog="h2_phase_a_r2_driver.py", description="H2-A-01 route-R2 control driver (no executable default)")
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
    try:
        accepted()
    except PinError as exc:
        print(json.dumps({"tier": "BLOCK_LAUNCH", "reasons": [f"PinError: {exc}"]}, indent=1, sort_keys=True))
        return 2
    if args.mode == "code-provenance":
        try:
            rec = build_provenance()
            with open(args.out, "x") as fh:
                json.dump(rec, fh, indent=1, sort_keys=True)
                fh.write("\n")
        except (A.Block, OSError) as exc:
            return A.emit({"code_provenance": "NOT_WRITTEN", "reason": f"{exc.__class__.__name__}: {exc}"}, 2)
        return A.emit({"code_provenance": "WRITTEN", "out": args.out, "sha256": A.sha256_file(args.out),
                       "base_commit": rec["base_commit"], "paths": rec["coverage"]["paths"]}, 0)
    if args.mode == "preflight":
        try:
            rep = preflight(args.interpreter, args.prefix, args.runs_root)
        except Exception as exc:  # noqa: BLE001 - structured refusal, as in run()
            return A.emit({"tier": "BLOCK_LAUNCH", "reasons": [f"preflight error: {exc.__class__.__name__}: {exc}"]}, 2)
        return A.emit({"tier": "PASS" if rep["ok"] else "BLOCK_LAUNCH", "report": rep}, 0 if rep["ok"] else 2)
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
