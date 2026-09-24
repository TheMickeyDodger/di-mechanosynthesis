# MS-000 ASE smoke and environment record

Status: public adaptation of the MS-000 smoke-test record.

This test checked that ASE 3.29.0 could be imported and that selected structure metadata survived an extxyz
write/read round trip on one macOS arm64 environment. It performed no electronic-structure calculation and
produced no evidence about energy, force, bonding, stability, reaction pathways, or the Cowie benchmark.

## Environment

| Item | Recorded value |
|---|---|
| Date | 2026-09-16 UTC |
| Operating system | macOS 15.6, Darwin 24.6.0, arm64 |
| Python | CPython 3.12.14 |
| uv | 0.12.5 |
| ASE | 3.29.0 |
| NumPy | 2.5.3 |
| External chemistry engines | `xtb`, `cp2k`, `cp2k.psmp`, and `cp2k.ssmp` were not present |

The virtual environment, package caches, and temporary files were confined to a private isolated workspace. No
global or system package was installed. Local paths and the host name have been omitted from this public record.

## Attempts

The first attempt failed before package installation or testing because its run script called the GNU `timeout`
utility, which was absent on the host. Both the install and smoke commands returned exit 127. The final marker in
that log was only an end-of-script marker and did not indicate a successful test.

The second attempt replaced `timeout` with a Perl alarm wrapper. The cap mechanism was first checked with a two
second busy loop and ended by `SIGALRM` as expected (`cap_test_exit=142`). The isolated environment was created,
ASE 3.29.0 and its resolved dependencies were installed, and the test completed with these exit codes:

| Step | Exit code |
|---|---:|
| Create environment | 0 |
| Install packages | 0 |
| Record resolved packages | 0 |
| Run smoke test | 0 |

The complete second attempt, including environment creation and installation, took 35 seconds. The smoke-test
program itself took 7.01 seconds.

## Test and result

The test created an eight-atom placeholder containing Si, H, C, Ge, O, and I in a 10 by 10 by 15 angstrom cell.
The coordinates were arbitrary and have no physical meaning. The object carried periodic-boundary flags, integer
atom tags, a `FixAtoms` constraint on atoms 0 and 1, and an `info` value. ASE wrote it as extxyz and read it back.

All nine comparisons passed:

1. atom count
2. element symbols
3. positions under NumPy `allclose` with relative tolerance `1e-5` and absolute tolerance `1e-8` angstrom
4. cell vectors under NumPy `allclose` with relative tolerance `1e-5` and absolute tolerance `1e-8` angstrom
5. periodic-boundary flags
6. atom tags
7. presence of the `FixAtoms` constraint
8. constrained atom indices
9. the selected `info` value

An independent replay used the unchanged program and the same resolved environment. It returned exit 0, passed
the same nine checks, and produced the same extxyz digest. The replay record is retained privately with SHA256
`7999a3851a852c5a959dd49c1358628ce53cdbf8e5a27c3eed446b579f3fa4db`.

## Resolved packages

```text
ase==3.29.0
contourpy==1.4.0
cycler==0.12.1
fonttools==4.65.0
kiwisolver==1.5.1
matplotlib==3.11.2
numpy==2.5.3
packaging==26.3
pillow==12.3.0
pyparsing==3.3.2
python-dateutil==2.9.0.post0
scipy==1.18.1
six==1.17.0
typing-extensions==4.16.0
```

## Tested program

The following is the exact program used in the completed attempt and independent replay. Its SHA256 is
`728aa687b0939780b60016487ada4c5c3ff6fbe0484e171709a26911209e4645`.

```python
"""ASE import + extxyz round-trip smoke test.

Evidence label: TOY IMPORT/IO SMOKE TEST. Not chemistry evidence, not benchmark
reproduction, no energies, no forces, no calculator. The atoms below are a
placeholder geometry with no physical meaning.
"""
import hashlib
import sys
import time

t0 = time.time()
import numpy as np  # noqa: E402
import ase  # noqa: E402
from ase import Atoms  # noqa: E402
from ase.constraints import FixAtoms  # noqa: E402
from ase.io import read, write  # noqa: E402

print("ase.__version__ =", ase.__version__)
print("numpy.__version__ =", np.__version__)
print("python =", sys.version.split()[0])

# Placeholder atoms (NOT a Cowie geometry; NOT physically meaningful).
symbols = ["Si", "Si", "H", "C", "C", "Ge", "O", "I"]
positions = np.array([[0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [0.0, 1.5, 0.0],
                      [0.0, 0.0, 3.0], [0.0, 0.0, 4.2], [0.0, 0.0, 6.0],
                      [1.5, 0.0, 6.5], [0.0, 0.0, 8.0]])
atoms = Atoms(symbols=symbols, positions=positions, cell=[10.0, 10.0, 15.0], pbc=[True, True, False])
atoms.set_constraint(FixAtoms(indices=[0, 1]))
atoms.info["evidence_class"] = "smoke-placeholder-not-chemistry"
atoms.set_tags(list(range(len(atoms))))  # atom identity tags survive round-trip?

path = "roundtrip.extxyz"
write(path, atoms, format="extxyz")
back = read(path, format="extxyz")

checks = {
    "n_atoms": len(back) == len(atoms),
    "symbols": back.get_chemical_symbols() == symbols,
    "positions_close": bool(np.allclose(back.get_positions(), positions, atol=1e-8)),
    "cell_close": bool(np.allclose(back.get_cell()[:], atoms.get_cell()[:], atol=1e-8)),
    "pbc": list(back.get_pbc()) == [True, True, False],
    "tags": list(back.get_tags()) == list(range(len(atoms))),
    "fixatoms_constraint_present": any(isinstance(c, FixAtoms) for c in back.constraints),
    "fixatoms_indices": any(isinstance(c, FixAtoms) and sorted(c.index.tolist()) == [0, 1] for c in back.constraints),
    "info_key": back.info.get("evidence_class") == "smoke-placeholder-not-chemistry",
}
for k, v in checks.items():
    print(f"check {k}: {'PASS' if v else 'FAIL'}")
digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
print("roundtrip.extxyz sha256 =", digest)
print("elapsed_s =", round(time.time() - t0, 3))
print("RESULT:", "ALL_PASS" if all(checks.values()) else "SOME_FAIL")
print("LABEL: toy import/IO smoke test; NOT chemistry evidence; NOT benchmark reproduction")
sys.exit(0 if all(checks.values()) else 1)
```

## Private raw-record digests

| Record | SHA256 | Interpretation |
|---|---|---|
| Failed-attempt log | `6dcd9bbcd51bbccff8b656c776bca1bedc39c86d39caf425c2be004e6b953557` | Exit 127 before installation or test |
| Failed-attempt script | `4953f2a6035c2511e6a3aea60b7367ab9e5746c938e0d4b767856caa5469ca0f` | Script that used unavailable `timeout` |
| Completed-attempt log | `5868200023632e6b30cb7c9c1d406405f004d29eb7609aa980229f3a4c9e9693` | Environment, package resolution, and nine passing checks |
| Completed-attempt script | `774b8ae98b488a1783300724f1fac81563a347bf856c2e353b42054f79af0764` | Isolated runner with Perl alarm caps |
| Test program | `728aa687b0939780b60016487ada4c5c3ff6fbe0484e171709a26911209e4645` | Exact copy above |
| Round-trip extxyz | `24b77f580634c3548e965275dfe5907f6095b881c51421f085b4c4a8c4e867c1` | Identical in completed run and replay |

The raw records remain private because they contain local paths and a host name. The digest table permits the
public summary to be checked against the retained records without publishing those identifiers.
