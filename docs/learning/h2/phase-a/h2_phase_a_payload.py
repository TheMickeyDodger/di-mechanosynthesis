"""Engine-side payload for job H2-A-01 (prospective; NOT_RUN; [AGENT]).

Executed only by the authorized interpreter, launched by h2_phase_a_driver.py after a person's separate, exact-byte
authorization. This file authorizes nothing. The module top level imports only the standard library; the engine is
imported inside run() so that tests can load the pure check functions without any engine.

Gated stages; a failed gate writes its own record and a stop record, and no later stage starts:
  P0 before `import psi4`: argv, interpreter and environment recorded; the bound prefix files re-hashed.
  import: loads the engine extension and its libraries and runs the package's import-time initialization.
  I1 loaded identity, before any engine call other than attribute reads and the data-directory accessor:
     version string, module and extension paths, loaded-image paths and on-disk digests of those files.
  I2 explicit settings and molecule: output file, threads, memory, options, molecule; all read back.
  I3 basis resolution, basis-file digest, basis-function count and nuclear repulsion against 1/R.
  energy: the single SCF energy call; then the reported total energy, reported nuclear repulsion, iteration count
     and convergence state are recorded separately, with no other energy derived, by exclusive creation.
What this ordering proves and does not prove: static bound files are checked by the driver before launch and
re-hashed here before import; loaded observations are validated after import and before the payload's explicit
settings, molecule, basis, nuclear-repulsion and energy API calls. Not proved: what the import and start-up of the
engine and its native libraries do (their native side effects are not observed), the correspondence between
in-memory code and on-disk bytes, and source-to-binary correspondence.

usage (by the driver only): <interpreter> -I -B h2_phase_a_payload.py <input.json> <attempt-dir>
Every engine API used here is located in the Psi4 v1.11 tagged source; see H2-A-01-RUN-PROPOSAL.md section 6.
"""
import datetime
import hashlib
import json
import math
import os
import re
import sys

STOP_BEFORE_ENERGY_EXIT = 3
ENERGY_FAILED_EXIT = 4
SCF_KEYS = ["reference", "basis", "guess", "scf_type", "df_scf_guess", "e_convergence", "d_convergence",
            "maxiter", "fail_on_maxiter"]
GLOBAL_READBACK = {"basis", "scf_type"}  # read by the v1.11 driver with core.get_global_option
CORE_REL = "lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so"
MODULE_REL = "lib/python3.14/site-packages/psi4/__init__.py"
REHASH = ["bin/python3.14", CORE_REL, "lib/libint2.dylib", "include/libint2/shell.h", "share/psi4/basis/sto-3g.gbs"]
RESULT_FIELDS = ["job_id", "reported_total_energy_hartree", "reported_nuclear_repulsion_hartree",
                 "scf_iterations", "converged", "engine_version", "post_energy_readback",
                 "banner_preserved_after_energy", "output_files"]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_exclusive(path, obj):
    with open(path, "x") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True, allow_nan=True)
        fh.write("\n")


def inside(prefix_real, path):
    real = os.path.realpath(path)
    return real == prefix_real or real.startswith(prefix_real + os.sep)


# ---------------------------------------------------------------- pure checks (no engine; tested on dicts)

def expected_scf_options(inp):
    """Expected read-back values in the engine's representation (upper-case strings, booleans as 0/1)."""
    out = {}
    for k in SCF_KEYS:
        v = inp["engine_options"][k]
        out[k] = v.upper() if isinstance(v, str) else (int(v) if isinstance(v, bool) else v)
    return out


def check_environment(observed, launch_env, platform_injected):
    """Observed os.environ before import: exactly the launcher's names and values, plus declared platform names."""
    problems = []
    for k, v in launch_env.items():
        if observed.get(k) != v:
            problems.append(f"environment: {k} missing or differs from the launcher record")
    for k in sorted(set(observed) - set(launch_env) - set(platform_injected)):
        problems.append(f"environment: undeclared name {k}")
    return problems


def check_interpreter(obs, launch):
    problems = []
    if obs.get("isolated") != 1:
        problems.append("interpreter: not started in isolated mode (-I)")
    if obs.get("dont_write_bytecode") != 1:
        problems.append("interpreter: bytecode writing not disabled (-B)")
    if obs.get("executable_realpath") != launch["interpreter_realpath"]:
        problems.append("interpreter: sys.executable differs from the launched interpreter")
    if obs.get("prefix_realpath") != launch["prefix_realpath"]:
        problems.append("interpreter: sys.prefix differs from the bound prefix")
    return problems


def check_static_rehash(launch):
    """P0: re-hash the bound prefix files before import. Returns (problems, observed digests)."""
    problems, seen = [], {}
    pre = launch["prefix_realpath"]
    exp = launch.get("expected_sha256") or {}
    for rel in REHASH:
        if rel not in exp:
            problems.append(f"static: no bound digest for {rel}")
            continue
        real = os.path.realpath(os.path.join(pre, rel))
        if not inside(pre, real):
            problems.append(f"static: {rel} resolves outside the bound prefix")
            continue
        try:
            seen[rel] = sha256_file(real)
        except OSError as exc:
            problems.append(f"static: {rel} unreadable ({exc.__class__.__name__})")
            continue
        if seen[rel] != exp[rel]:
            problems.append(f"static: {rel} digest differs from the launch binding")
    return problems, seen


def check_engine_identity(obs, inp, launch):
    """Version string, module files, data directory and loaded images (layer ii observations)."""
    problems = []
    pre = launch["prefix_realpath"]
    exp = launch["expected_sha256"]
    if obs.get("version") != inp["expected_engine_version"]:
        problems.append("identity: engine version string differs")
    for key in ("module_file", "core_file"):
        if not obs.get(key) or not inside(pre, obs[key]):
            problems.append(f"identity: {key} not inside the bound prefix")
    core_rel = CORE_REL
    if obs.get("core_file") and os.path.realpath(obs["core_file"]) != os.path.join(pre, core_rel):
        problems.append("identity: engine core library is not the bound prefix file")
    if obs.get("module_file") and os.path.realpath(obs["module_file"]) != os.path.join(pre, MODULE_REL):
        problems.append("identity: engine package module is not the bound prefix file")
    if obs.get("datadir_realpath") != os.path.join(pre, "share", "psi4"):
        problems.append("identity: engine data directory is not <PREFIX>/share/psi4")
    images = obs.get("loaded_images")
    if not isinstance(images, list) or not images:
        problems.append("identity: loaded-image list unavailable")
        return problems
    libint = [i for i in images if os.path.basename(i["path"]).startswith("libint2")]
    want = os.path.join(pre, "lib", "libint2.dylib")
    if not libint:
        problems.append("identity: no Libint library among loaded images")
    for i in libint:
        if i.get("realpath") != want:
            problems.append("identity: a loaded Libint library is not <PREFIX>/lib/libint2.dylib")
        elif i.get("sha256") != exp["lib/libint2.dylib"]:
            problems.append("identity: loaded Libint library digest differs")
    cores = [i for i in images if i.get("realpath") == os.path.join(pre, core_rel)]
    if not cores:
        problems.append("identity: engine core library not among loaded images")
    elif cores[0].get("sha256") != exp[core_rel]:
        problems.append("identity: loaded core library digest differs")
    return problems


def check_basis(obs, inp, launch):
    problems = []
    want = os.path.join(launch["prefix_realpath"], "share", "psi4", "basis", "sto-3g.gbs")
    if obs.get("basis_file_realpath") != want:
        problems.append("basis: file used is not <PREFIX>/share/psi4/basis/sto-3g.gbs")
    elif obs.get("basis_file_sha256") != launch["expected_sha256"]["share/psi4/basis/sto-3g.gbs"]:
        problems.append("basis: file digest differs")
    if obs.get("cwd_gbs_files"):
        problems.append("basis: .gbs files present in the working directory")
    if obs.get("nbf") != 2:
        problems.append("basis: basis-function count is not 2")
    return problems


def check_molecule(obs, inp):
    problems = []
    mol = inp["molecule"]
    tol = inp["readback_tolerances"]["coordinate_abs_bohr"]
    if obs.get("natom") != len(mol["atoms"]):
        problems.append("molecule: atom count differs")
        return problems
    if obs.get("molecular_charge") != mol["charge"]:
        problems.append("molecule: charge differs")
    if obs.get("multiplicity") != mol["multiplicity"]:
        problems.append("molecule: multiplicity differs")
    if obs.get("electrons") != mol["electrons"]:
        problems.append("molecule: electron count differs")
    if obs.get("units") != "Bohr":
        problems.append("molecule: units are not Bohr")
    if str(obs.get("point_group")).lower() != inp["molecule_options"]["symmetry"]:
        problems.append("molecule: point group differs")
    if obs.get("com_fixed") is not inp["molecule_options"]["no_com"]:
        problems.append("molecule: centre-of-mass setting differs")
    if obs.get("orientation_fixed") is not inp["molecule_options"]["no_reorient"]:
        problems.append("molecule: orientation setting differs")
    for i, atom in enumerate(mol["atoms"]):
        got = obs["atoms"][i] if i < len(obs.get("atoms", [])) else {}
        if got.get("label") != atom["label"].upper() or got.get("symbol") != atom["element"].upper():
            problems.append(f"molecule: atom {i} label or element differs")
        xyz = got.get("xyz_bohr")
        if not xyz or any(not math.isfinite(a) or abs(a - b) > tol for a, b in zip(xyz, atom["xyz_bohr"])):
            problems.append(f"molecule: atom {i} coordinates differ")
    return problems


def check_nuclear_repulsion(value, inp, tol):
    """Geometry and unit integrity check only: |V_NN - 1/R| <= tol (hartree, R in bohr)."""
    if value is None:
        return ["nuclear repulsion: missing"]
    if not isinstance(value, (int, float)) or not math.isfinite(value):
        return ["nuclear repulsion: nonfinite"]
    if abs(value - 1.0 / inp["molecule"]["R_bohr"]) > tol:
        return ["nuclear repulsion: differs from 1/R beyond tolerance"]
    return []


def check_settings(obs, inp):
    problems = []
    exp = expected_scf_options(inp)
    for k, v in exp.items():
        got = obs.get("options", {}).get(k)
        if got != v:
            problems.append(f"setting: {k} read back differs")
        if obs.get("changed", {}).get(k) is not True:
            problems.append(f"setting: {k} not marked as changed by the user")
    if obs.get("threads") != inp["threads"]:
        problems.append("setting: thread count read back differs")
    want = inp["readback_tolerances"]["memory_bytes"]
    if obs.get("memory_set_bytes") != want or obs.get("memory_bytes") != want:
        problems.append("setting: engine memory read back differs")
    return problems


def sizeof_fmt(num):
    """Memory text as the v1.11 banner prints it (psi4/header.py 82-87, used at line 94)."""
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return "%3.1f %sB" % (num, unit)
        num /= 1024.0
    return "%.1f YiB" % num


def check_banner(text, inp, launch):
    """Printed banner (v1.11 psi4/header.py 89-140, printed by set_output_file, extras.py 310-314)."""
    if not text:
        return ["banner: missing"]
    problems = []
    lines = [ln.strip() for ln in text.splitlines()]
    if "Psi4: An Open-Source Ab Initio Electronic Structure Package" not in lines:
        problems.append("banner: program line missing")
    vers = [m.group(1) for ln in lines for m in [re.fullmatch(r"Psi4 (\S+)(?: \S+)?", ln)] if m]
    if vers != [inp["expected_engine_version"]]:
        problems.append("banner: version line missing or differs")
    fields = {}
    for ln in lines:
        m = re.fullmatch(r"(PSIDATADIR|Threads|Memory):\s+(.+)", ln)
        if m:
            fields.setdefault(m.group(1), []).append(m.group(2))
    dd = fields.get("PSIDATADIR", [])
    if len(dd) != 1 or os.path.realpath(dd[0]) != os.path.join(launch["prefix_realpath"], "share", "psi4"):
        problems.append("banner: PSIDATADIR missing or not <PREFIX>/share/psi4")
    if fields.get("Threads") != [str(inp["threads"])]:
        problems.append("banner: thread line missing or differs")
    if fields.get("Memory") != [sizeof_fmt(inp["readback_tolerances"]["memory_bytes"])]:
        problems.append("banner: memory line missing or differs")
    return problems


def build_molrec(inp):
    """Molecule record for psi4.core.Molecule.from_dict (v1.11 psi4/src/export_mints.cc 228-328)."""
    mol, con = inp["molecule"], inp["construction"]
    opts = inp["molecule_options"]
    atoms = mol["atoms"]
    geom = [c for a in atoms for c in a["xyz_bohr"]]
    return {
        "name": inp["job_id"], "units": "Bohr" if opts["units"] == mol["units"] == "bohr" else "INVALID",
        "fix_com": opts["no_com"], "fix_orientation": opts["no_reorient"], "fix_symmetry": opts["symmetry"],
        "elem": [a["element"] for a in atoms], "elbl": [a["label"][len(a["element"]):] for a in atoms],
        "elez": [1.0 for _ in atoms], "elea": [con["mass_number"][a["element"]] for a in atoms],
        "real": [True for _ in atoms], "mass": [con["mass_amu"][a["element"]] for a in atoms],
        "geom": geom, "fragment_separators": [], "fragment_charges": [float(mol["charge"])],
        "fragment_multiplicities": [mol["multiplicity"]], "molecular_charge": float(mol["charge"]),
        "molecular_multiplicity": mol["multiplicity"], "provenance": dict(con["molrec_provenance"]),
    }


# ---------------------------------------------------------------- engine-side observation (future authorized run)

def loaded_images(prefix_real):
    """Loaded Mach-O images of this process through the dyld image API, an operating-system interface outside the
    engine source (see the proposal's gap list). Files under the prefix are hashed statically; others by name."""
    import ctypes
    lib = ctypes.CDLL(None)
    count = lib._dyld_image_count
    count.restype = ctypes.c_uint32
    name = lib._dyld_get_image_name
    name.restype = ctypes.c_char_p
    name.argtypes = [ctypes.c_uint32]
    out = []
    for i in range(count()):
        raw = name(i)
        path = raw.decode("utf-8", "replace") if raw else ""
        real = os.path.realpath(path) if path else ""
        rec = {"path": path, "realpath": real}
        if path and inside(prefix_real, path) and os.path.isfile(real):
            rec["sha256"] = sha256_file(real)
        out.append(rec)
    return out


def observe_identity(psi4, launch):
    """I1: attribute reads, the data-directory accessor (core.get_datadir, v1.11 psi4/src/core.cc 1256-1257, set at
    import by psi4/__init__.py 82) and the loaded-image list. No setting, molecule, basis or SCF call."""
    return {"version": psi4.__version__, "module_file": psi4.__file__, "core_file": psi4.core.__file__,
            "datadir_realpath": os.path.realpath(psi4.core.get_datadir()),
            "loaded_images": loaded_images(launch["prefix_realpath"])}


def observe_configuration(psi4, mol):
    """I2: read-back of the explicit settings and of the molecule built from the input."""
    core = psi4.core
    return {
        "options": {k: (core.get_global_option(k.upper()) if k in GLOBAL_READBACK else core.get_option("SCF", k.upper()))
                    for k in SCF_KEYS},
        "changed": {k: bool(core.has_global_option_changed(k.upper()) if k in GLOBAL_READBACK
                            else core.has_option_changed("SCF", k.upper())) for k in SCF_KEYS},
        "threads": core.get_num_threads(), "memory_bytes": core.get_memory(),
        "natom": mol.natom(), "molecular_charge": mol.molecular_charge(), "multiplicity": mol.multiplicity(),
        "electrons": int(round(sum(mol.Z(i) for i in range(mol.natom())))) - mol.molecular_charge(),
        "units": mol.units(), "point_group": mol.schoenflies_symbol(), "com_fixed": mol.com_fixed(),
        "orientation_fixed": mol.orientation_fixed(),
        "atoms": [{"label": mol.label(i), "symbol": mol.symbol(i), "xyz_bohr": [mol.x(i), mol.y(i), mol.z(i)]}
                  for i in range(mol.natom())],
    }


def observe_basis_geometry(psi4, inp, mol):
    """I3: basis file the v1.11 search order resolves (cwd, PSIPATH, datadir/basis: libmintsbasisset.py 803-805,
    916-925), its digest, the basis-function count and the molecule's nuclear repulsion."""
    _, bsdict = psi4.driver.qcdb.BasisSet.pyconstruct(mol.to_dict(quiet=True), "BASIS", inp["engine_options"]["basis"],
                                                      "ORBITAL", None, return_dict=True)
    m = re.search(r"file (.+?\.gbs)", bsdict.get("message", ""))
    return {"basis_message": bsdict.get("message", ""),
            "basis_file_realpath": os.path.realpath(m.group(1)) if m else None,
            "basis_file_sha256": sha256_file(m.group(1)) if m else None,
            "cwd_gbs_files": sorted(f for f in os.listdir(".") if f.endswith(".gbs")),
            "nbf": psi4.core.BasisSet.build(mol, "ORBITAL", inp["engine_options"]["basis"], quiet=True).nbf(),
            "nuclear_repulsion_hartree": mol.nuclear_repulsion_energy()}


def run(argv):
    if len(argv) != 3:
        print(__doc__, file=sys.stderr)
        return 64
    input_path, attempt = argv[1], argv[2]
    out = os.path.join(attempt, "payload")
    launch = json.load(open(os.path.join(attempt, "launch-record.json")))
    inp = json.load(open(input_path))

    def stop(stage, problems, extra=None):
        rec = {"stage": stage, "tier": "STOP_BEFORE_ENERGY", "utc": utc(), "problems": problems, "energy_called": False}
        rec.update(extra or {})
        write_exclusive(os.path.join(out, "stop-before-energy.json"), rec)
        return STOP_BEFORE_ENERGY_EXIT

    def gate(stage, name, obs, problems):
        obs.update({"stage": stage, "utc": utc(), "problems": problems})
        write_exclusive(os.path.join(out, name), obs)
        return stop(stage, problems) if problems else None

    # P0: before the engine import.
    pre = {"argv": list(argv), "sys_version": sys.version, "sys_executable": sys.executable, "sys_path": list(sys.path),
           "environ": dict(os.environ), "cwd": os.getcwd(), "pid": os.getpid(), "isolated": sys.flags.isolated,
           "dont_write_bytecode": sys.flags.dont_write_bytecode,
           "executable_realpath": os.path.realpath(sys.executable), "prefix_realpath": os.path.realpath(sys.prefix),
           "engine_modules_loaded_before_import": sorted(m for m in sys.modules if m == "psi4" or m.startswith("psi4."))}
    static_problems, pre["static_sha256"] = check_static_rehash(launch)
    problems = (check_environment(pre["environ"], launch["environment"], launch["platform_injected"])
                + check_interpreter(pre, launch) + static_problems
                + (["engine module loaded before import"] if pre["engine_modules_loaded_before_import"] else []))
    if gate("P0-pre-import", "pre-import.json", pre, problems):
        return STOP_BEFORE_ENERGY_EXIT
    try:
        import psi4  # the engine is imported only here; import-time initialization is not observed
    except BaseException as exc:  # noqa: BLE001 - every import failure is recorded, nothing is retried
        return stop("import", [f"import failed: {exc.__class__.__name__}: {exc}"])

    # I1: loaded identity, before any setting, molecule, basis or SCF call.
    try:
        ident = observe_identity(psi4, launch)
    except BaseException as exc:  # noqa: BLE001
        return stop("I1-loaded-identity", [f"observation failed: {exc.__class__.__name__}: {exc}"])
    if gate("I1-loaded-identity", "i1-identity.json", ident, check_engine_identity(ident, inp, launch)):
        return STOP_BEFORE_ENERGY_EXIT

    # I2: explicit settings, printed banner and molecule, read back. Threads and memory are set first so that the
    # banner, requested explicitly, reports the bound settings; core.print_out flushes (v1.11 core.cc 558-563).
    conf = {}
    output = os.path.join(out, "psi4-output.dat")
    try:
        psi4.set_num_threads(inp["threads"])
        conf["memory_set_bytes"] = psi4.set_memory(inp["memory"])
        psi4.set_output_file(output, False, print_header=True)
        with open(output, "rb") as fh:
            banner = fh.read()
        conf.update({"banner_text": banner.decode("utf-8", "replace"), "banner_bytes": len(banner),
                     "banner_sha256": hashlib.sha256(banner).hexdigest()})
        psi4.set_options(dict(inp["engine_options"]))
        mol = psi4.core.Molecule.from_dict(build_molrec(inp))
        conf.update(observe_configuration(psi4, mol))
    except BaseException as exc:  # noqa: BLE001
        return stop("I2-configuration", [f"observation failed: {exc.__class__.__name__}: {exc}"], {"observations": conf})
    if gate("I2-configuration", "i2-configuration.json", conf, check_banner(conf["banner_text"], inp, launch)
            + check_settings(conf, inp) + check_molecule(conf, inp)):
        return STOP_BEFORE_ENERGY_EXIT

    # I3: basis and geometry integrity.
    try:
        geo = observe_basis_geometry(psi4, inp, mol)
    except BaseException as exc:  # noqa: BLE001
        return stop("I3-basis-geometry", [f"observation failed: {exc.__class__.__name__}: {exc}"])
    tol = launch["nuclear_repulsion_abs_tol_hartree"]
    if gate("I3-basis-geometry", "i3-basis-geometry.json", geo,
            check_basis(geo, inp, launch) + check_nuclear_repulsion(geo.get("nuclear_repulsion_hartree"), inp, tol)):
        return STOP_BEFORE_ENERGY_EXIT

    result = {"stage": "energy", "job_id": inp["job_id"], "engine_version": ident["version"], "energy_called": True,
              "energy_call_utc": utc()}
    try:
        energy, wfn = psi4.energy(inp["method_call"], molecule=mol, return_wfn=True)
    except psi4.driver.p4util.exceptions.SCFConvergenceError as exc:
        result.update({"converged": False, "failure": f"SCFConvergenceError: {exc}", "utc": utc()})
        write_exclusive(os.path.join(out, "energy-failed.json"), result)
        return ENERGY_FAILED_EXIT
    except BaseException as exc:  # noqa: BLE001
        result.update({"converged": None, "failure": f"{exc.__class__.__name__}: {exc}", "utc": utc()})
        write_exclusive(os.path.join(out, "energy-failed.json"), result)
        return ENERGY_FAILED_EXIT
    result["energy_return_utc"] = utc()
    result["reported_total_energy_hartree"] = energy
    result["reported_total_energy_source"] = "return value of psi4.energy (core variable CURRENT ENERGY)"
    result["converged"] = True
    result["converged_basis"] = "no SCFConvergenceError with FAIL_ON_MAXITER true (v1.11 scf_iterator.py 85-97, 608-609)"
    try:  # a failure here leaves fields missing, which the driver classifies as QUARANTINE
        result["reported_nuclear_repulsion_hartree"] = (wfn.variable("NUCLEAR REPULSION ENERGY")
                                                        if wfn.has_variable("NUCLEAR REPULSION ENERGY") else None)
        # Scalar variables are stored and returned as doubles (v1.11 psi4/driver/p4util/python_helpers.py 1330;
        # psi4/src/psi4/libmints/wavefunction.h 246, 666). The raw value is kept; the count is recorded as an integer
        # only when that double is finite and integral, otherwise as null (which the driver quarantines).
        raw = wfn.variable("SCF ITERATIONS") if wfn.has_variable("SCF ITERATIONS") else None
        result["scf_iterations_raw"] = raw
        result["scf_iterations"] = (int(raw) if isinstance(raw, (int, float)) and not isinstance(raw, bool)
                                    and math.isfinite(raw) and float(raw).is_integer() else None)
        wmol = wfn.molecule()
        result["post_energy_readback"] = {
            "wavefunction_class": type(wfn).__name__, "nbf": wfn.basisset().nbf(), "nalpha": wfn.nalpha(),
            "nbeta": wfn.nbeta(), "natom": wmol.natom(),
            "atoms": [{"label": wmol.label(i), "xyz_bohr": [wmol.x(i), wmol.y(i), wmol.z(i)]} for i in range(wmol.natom())],
            "options": {k: (psi4.core.get_global_option(k.upper()) if k in GLOBAL_READBACK
                            else psi4.core.get_option("SCF", k.upper())) for k in SCF_KEYS},
        }
        with open(output, "rb") as fh:
            result["banner_preserved_after_energy"] = fh.read().startswith(banner)
        result["output_files"] = sorted(os.listdir(out))
    except BaseException as exc:  # noqa: BLE001
        result["post_energy_error"] = f"{exc.__class__.__name__}: {exc}"
    result["utc"] = utc()
    write_exclusive(os.path.join(out, "result.json"), result)
    return 0


if __name__ == "__main__":
    sys.exit(run(sys.argv))
