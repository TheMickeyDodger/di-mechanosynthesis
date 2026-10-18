# FIXTURE ONLY. A stand-in "engine interpreter" for the driver tests. It is copied into a fake prefix inside a test
# temporary directory with a shebang line naming the test's own Python, and the driver launches it exactly as it would
# launch the engine interpreter. It imports no engine, ignores the payload file it is given, and writes fixture-marked
# records into <attempt>/payload that are consistent with the fixture launch binding (fake-prefix paths and digests),
# with deliberately non-physical sentinel numbers. Its behaviour is chosen by the file FIXTURE-MODE at the root of the
# fake prefix; the MUTATIONS table turns the consistent records into one negative case each. Nothing it writes is a
# scientific value.
import datetime
import hashlib
import json
import math
import os
import re
import signal
import subprocess
import sys
import time

MARK = "FIXTURE - synthetic test record, not engine output, not a scientific value"
SENTINEL_ENERGY = 424242.0  # deliberately non-physical
PREFIX = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = "lib/python3.14/site-packages/psi4/"


def write(path, obj):
    with open(path, "x") as fh:
        json.dump(obj, fh, allow_nan=True)


def scf_options(inp):
    return {k: (v.upper() if isinstance(v, str) else (int(v) if isinstance(v, bool) else v))
            for k, v in inp["engine_options"].items()}


def setp(rec, key, value):
    rec[key] = value


def delp(rec, key):
    del rec[key]


# mode -> (record, mutation); each negative case changes exactly one thing in otherwise consistent records
MUTATIONS = {
    "images_empty": ("i1-identity", lambda r, L: setp(r, "loaded_images", [])),
    "images_missing": ("i1-identity", lambda r, L: delp(r, "loaded_images")),
    "image_entry_malformed": ("i1-identity", lambda r, L: r["loaded_images"].append({"path": 7})),
    "core_image_absent": ("i1-identity", lambda r, L: setp(r, "loaded_images", [i for i in r["loaded_images"] if not i["path"].endswith(".so")])),
    "core_image_outside": ("i1-identity", lambda r, L: [i.update(realpath="/FIXTURE/outside/core.cpython-314-darwin.so") for i in r["loaded_images"] if i["path"].endswith(".so")]),
    "core_image_digest_wrong": ("i1-identity", lambda r, L: [i.update(sha256="0" * 64) for i in r["loaded_images"] if i["path"].endswith(".so")]),
    "libint_image_absent": ("i1-identity", lambda r, L: setp(r, "loaded_images", [i for i in r["loaded_images"] if "libint2" not in i["path"]])),
    "libint_image_outside": ("i1-identity", lambda r, L: [i.update(realpath="/FIXTURE/outside/libint2.dylib") for i in r["loaded_images"] if "libint2" in i["path"]]),
    "libint_image_digest_wrong": ("i1-identity", lambda r, L: [i.update(sha256="0" * 64) for i in r["loaded_images"] if "libint2" in i["path"]]),
    "module_outside": ("i1-identity", lambda r, L: setp(r, "module_file", "/FIXTURE/outside/psi4/__init__.py")),
    "core_file_outside": ("i1-identity", lambda r, L: setp(r, "core_file", "/FIXTURE/outside/core.cpython-314-darwin.so")),
    "datadir_outside": ("i1-identity", lambda r, L: setp(r, "datadir_realpath", "/FIXTURE/outside/share/psi4")),
    "env_value_changed": ("pre-import", lambda r, L: r["environ"].update(OMP_NUM_THREADS="4")),
    "env_key_added": ("pre-import", lambda r, L: r["environ"].update(PSIPATH="/FIXTURE/elsewhere")),
    "env_key_removed": ("pre-import", lambda r, L: r["environ"].pop("TMPDIR")),
    "argv_wrong": ("pre-import", lambda r, L: setp(r, "argv", r["argv"][:-1] + ["/FIXTURE/other-attempt"])),
    "executable_mismatch": ("pre-import", lambda r, L: setp(r, "executable_realpath", "/FIXTURE/other/python3.14")),
    "prefix_mismatch": ("pre-import", lambda r, L: setp(r, "prefix_realpath", "/FIXTURE/other-prefix")),
    "cwd_wrong": ("pre-import", lambda r, L: setp(r, "cwd", "/FIXTURE/other-scratch")),
    "modules_loaded_before_import": ("pre-import", lambda r, L: setp(r, "engine_modules_loaded_before_import", ["psi4"])),
    "static_rehash_key_missing": ("pre-import", lambda r, L: r["static_sha256"].pop("include/libint2/shell.h")),
    "charge_wrong": ("i2-configuration", lambda r, L: setp(r, "molecular_charge", 1)),
    "multiplicity_wrong": ("i2-configuration", lambda r, L: setp(r, "multiplicity", 3)),
    "electrons_wrong": ("i2-configuration", lambda r, L: setp(r, "electrons", 1)),
    "units_wrong": ("i2-configuration", lambda r, L: setp(r, "units", "Angstrom")),
    "point_group_wrong": ("i2-configuration", lambda r, L: setp(r, "point_group", "d2h")),
    "com_wrong": ("i2-configuration", lambda r, L: setp(r, "com_fixed", False)),
    "orientation_wrong": ("i2-configuration", lambda r, L: setp(r, "orientation_fixed", False)),
    "changed_flag_false": ("i2-configuration", lambda r, L: r["changed"].update(guess=False)),
    "banner_bytes_wrong": ("i2-configuration", lambda r, L: setp(r, "banner_bytes", r["banner_bytes"] + 1)),
    "i2_threads_wrong": ("i2-configuration", lambda r, L: setp(r, "threads", 4)),
    "basis_path_outside": ("i3-basis-geometry", lambda r, L: setp(r, "basis_file_realpath", "/FIXTURE/cwd/sto-3g.gbs")),
    "cwd_gbs_nonempty": ("i3-basis-geometry", lambda r, L: setp(r, "cwd_gbs_files", ["sto-3g.gbs"])),
    "stage_problems_only": ("i3-basis-geometry", lambda r, L: [r.pop(k) for k in list(r) if k not in ("stage", "problems")]),
    "pre_import_digest_wrong": ("pre-import", lambda r, L: setp(r, "static_sha256", {k: "0" * 64 for k in r["static_sha256"]})),
    "stage_gate_failed": ("i1-identity", lambda r, L: setp(r, "problems", ["FIXTURE identity problem recorded but not stopped"])),
}
BANNER_VARIANTS = {"banner_version_wrong": ("Psi4 1.11 FIXTURE-release", "Psi4 FIXTURE-0.0 FIXTURE-release"),
                   "banner_datadir_wrong": ("PSIDATADIR: {pre}/share/psi4", "PSIDATADIR: /FIXTURE/elsewhere/share/psi4")}


def banner_text(mode, inp):
    lines = ["    FIXTURE BANNER - synthetic text, not engine output",
             "      Psi4: An Open-Source Ab Initio Electronic Structure Package",
             "            Psi4 1.11 FIXTURE-release".replace("1.11", inp["expected_engine_version"]),
             "    PSIDATADIR: {pre}/share/psi4", "    Memory:     500.0 MiB", "    Threads:    1", ""]
    text = "\n".join(lines)
    if mode in BANNER_VARIANTS:
        old, new = BANNER_VARIANTS[mode]
        text = text.replace(old.replace("1.11", inp["expected_engine_version"]), new)
    return text.replace("{pre}", PREFIX_REAL)


PREFIX_REAL = os.path.realpath(PREFIX)


def main():
    payload, input_path, attempt = sys.argv[-3:]  # argv: -I -B <payload> <input> <attempt>
    mode = open(os.path.join(PREFIX, "FIXTURE-MODE")).read().strip()
    out = os.path.join(attempt, "payload")
    with open(input_path) as fh:
        inp = json.load(fh)
    with open(os.path.join(attempt, "launch-record.json")) as fh:
        launch = json.load(fh)
    r = inp["molecule"]["R_bohr"]
    pre = launch["prefix_realpath"]
    want = launch["expected_sha256"]
    atoms = [{"label": a["label"].upper(), "symbol": a["element"].upper(), "xyz_bohr": a["xyz_bohr"]}
             for a in inp["molecule"]["atoms"]]
    if mode == "env_dump":
        write(os.path.join(out, "fixture-env.json"), {"fixture": MARK, "names": sorted(os.environ), "cwd": os.getcwd()})
    if mode == "nonzero":
        return 17
    if mode in ("hang", "leftover"):
        code = "import signal, time\nsignal.signal(signal.SIGTERM, signal.SIG_IGN)\nwhile True: time.sleep(0.2)\n"
        child = subprocess.Popen([sys.executable, "-I", "-c", code], stdin=subprocess.DEVNULL)  # same process group
        write(os.path.join(out, "fixture-grandchild.json"), {"fixture": MARK, "pid": child.pid})
        if mode == "hang":
            signal.signal(signal.SIGTERM, signal.SIG_IGN)
            while True:
                time.sleep(0.2)
    if mode == "modify_prefix":
        with open(os.path.join(PREFIX, "conda-meta", "fixture-installed-0.0-0.json"), "x") as fh:
            fh.write("{}")
    if mode == "modify_record_build_number":  # change a field inside an existing record without renaming it
        name = [n for n in os.listdir(os.path.join(PREFIX, "conda-meta")) if n.startswith("psi4-")][0]
        path = os.path.join(PREFIX, "conda-meta", name)
        with open(path) as fh:
            rec = json.load(fh)
        rec["build_number"] = rec["build_number"] + 1
        with open(path, "w") as fh:
            json.dump(rec, fh)
    banner = banner_text(mode, inp)
    images = [{"path": "/FIXTURE/system/libSystem.B.dylib", "realpath": "/FIXTURE/system/libSystem.B.dylib", "fixture": MARK},
              {"path": os.path.join(pre, SP + "core.cpython-314-darwin.so"), "realpath": os.path.join(pre, SP + "core.cpython-314-darwin.so"),
               "sha256": want[SP + "core.cpython-314-darwin.so"], "fixture": MARK},
              {"path": "@rpath/libint2.dylib", "realpath": os.path.join(pre, "lib/libint2.dylib"),
               "sha256": want["lib/libint2.dylib"], "fixture": MARK}]
    stages = {
        "pre-import": {"argv": list(launch["command"][3:]), "environ": dict(os.environ), "isolated": 1,
                       "dont_write_bytecode": 1, "static_sha256": dict(want),
                       "executable_realpath": launch["interpreter_realpath"], "prefix_realpath": pre,
                       "cwd": os.getcwd(), "engine_modules_loaded_before_import": [], "stage": "P0-pre-import"},
        "i1-identity": {"version": inp["expected_engine_version"], "module_file": os.path.join(pre, SP + "__init__.py"),
                        "core_file": os.path.join(pre, SP + "core.cpython-314-darwin.so"),
                        "datadir_realpath": os.path.join(pre, "share/psi4"), "loaded_images": images,
                        "stage": "I1-loaded-identity"},
        "i2-configuration": {"banner_text": banner, "banner_sha256": hashlib.sha256(banner.encode()).hexdigest(),
                             "banner_bytes": len(banner.encode()), "options": scf_options(inp),
                             "changed": {k: True for k in inp["engine_options"]}, "threads": inp["threads"],
                             "memory_bytes": inp["readback_tolerances"]["memory_bytes"],
                             "memory_set_bytes": inp["readback_tolerances"]["memory_bytes"], "natom": len(atoms),
                             "atoms": atoms, "molecular_charge": inp["molecule"]["charge"],
                             "multiplicity": inp["molecule"]["multiplicity"], "electrons": inp["molecule"]["electrons"],
                             "units": "Bohr", "point_group": inp["molecule_options"]["symmetry"],
                             "com_fixed": inp["molecule_options"]["no_com"],
                             "orientation_fixed": inp["molecule_options"]["no_reorient"], "stage": "I2-configuration"},
        # 1/R is the geometric identity the driver checks, not an engine value
        "i3-basis-geometry": {"basis_file_realpath": os.path.join(pre, "share/psi4/basis/sto-3g.gbs"),
                              "basis_file_sha256": want["share/psi4/basis/sto-3g.gbs"], "nbf": 2, "cwd_gbs_files": [],
                              "nuclear_repulsion_hartree": 1.0 / r, "basis_message": "FIXTURE", "stage": "I3-basis-geometry"},
    }
    for rec in stages.values():
        rec.update(fixture=MARK, problems=[])
    if mode in ("stop", "stop_inconsistent"):
        # stop: a consistent stop at I1. stop_inconsistent: the stop record names I2 although I1 did not pass.
        write(os.path.join(out, "pre-import.json"), stages["pre-import"])
        write(os.path.join(out, "i1-identity.json"), dict(stages["i1-identity"], problems=["FIXTURE identity problem"]))
        stage, problems = "I1-loaded-identity", ["FIXTURE identity problem"]
        if mode == "stop_inconsistent":
            problems = ["FIXTURE configuration problem"]
            write(os.path.join(out, "i2-configuration.json"), dict(stages["i2-configuration"], problems=problems))
            stage = "I2-configuration"
        write(os.path.join(out, "stop-before-energy.json"), {"fixture": MARK, "tier": "STOP_BEFORE_ENERGY", "stage": stage,
                                                            "energy_called": False, "problems": problems})
        return 3
    for name, rec in stages.items():
        if mode in MUTATIONS and MUTATIONS[mode][0] == name:
            MUTATIONS[mode][1](rec, launch)
        write(os.path.join(out, name + ".json"), rec)
    if mode != "missing_output":
        with open(os.path.join(out, "psi4-output.dat"), "x") as fh:
            fh.write((banner if mode != "banner_lost" else "FIXTURE truncated\n") + "FIXTURE body\n")
    if mode != "missing_log":
        with open(os.path.join(out, "psi4-output.log"), "x") as fh:
            fh.write("FIXTURE log\n")
    if mode == "stop_without_record":
        return 3
    if mode == "energy_failed":
        write(os.path.join(out, "energy-failed.json"), {"fixture": MARK, "failure": "FIXTURE convergence failure"})
        return 4
    t0 = datetime.datetime.now(datetime.timezone.utc)
    result = {
        "fixture": MARK, "job_id": inp["job_id"], "stage": "energy", "energy_called": True,
        "engine_version": inp["expected_engine_version"], "energy_call_utc": t0.isoformat(),
        "energy_return_utc": (t0 - datetime.timedelta(seconds=5) if mode == "energy_utc_order_wrong"
                              else t0 + datetime.timedelta(seconds=1)).isoformat(),
        "reported_total_energy_hartree": math.nan if mode == "nonfinite_energy" else SENTINEL_ENERGY,
        "reported_nuclear_repulsion_hartree": {"nonfinite_nr": math.inf, "mismatch_nr": 1.0 / r + 1e-6}.get(mode, 1.0 / r),
        "scf_iterations": {"iterations_null": None, "iterations_float": 7.0}.get(mode, 7),
        "scf_iterations_raw": {"iterations_raw_mismatch": 8.0}.get(mode, 7.0),
        "converged": True, "banner_preserved_after_energy": True,
        "output_files": ["i1-identity.json", "i2-configuration.json", "i3-basis-geometry.json", "pre-import.json",
                         "psi4-output.dat", "psi4-output.log"],
        "post_energy_readback": {
            "wavefunction_class": "RHF", "nbf": 2, "nalpha": 1, "nbeta": 1, "natom": 2,
            "atoms": [{"label": a["label"], "xyz_bohr": a["xyz_bohr"]} for a in atoms], "options": scf_options(inp),
        },
    }
    m = re.fullmatch(r"iter_(\d+)_(match|raw(\d+))", mode)  # boundary cases around the iteration limit
    if m:
        result["scf_iterations"] = int(m.group(1))
        result["scf_iterations_raw"] = float(m.group(1)) if m.group(2) == "match" else float(m.group(3))
    if mode == "nalpha_nbeta_unequal":
        result["post_energy_readback"].update(nalpha=2, nbeta=0)
    if mode == "missing_nr":
        result["reported_nuclear_repulsion_hartree"] = None
    if mode == "missing_field":
        del result["scf_iterations"]
    if mode == "readback_string":
        result["post_energy_readback"] = "FIXTURE not an object"
    if mode == "atoms_malformed":
        result["post_energy_readback"]["atoms"] = ["FIXTURE", "FIXTURE"]
    if mode == "post_energy_error":
        result["post_energy_error"] = "FIXTURE read-back error"
    if mode == "result_list":
        result = ["FIXTURE", "not an object"]
    write(os.path.join(out, "result.json"), result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
