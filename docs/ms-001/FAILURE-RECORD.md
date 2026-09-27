# MS-001 Stage 0 failure record

Every failed, aborted or non-converged attempt is preserved here rather than overwritten, as the provenance
requirements demand ([evidence policy §4](../evidence-policy.md#4-provenance-required-for-a-future-result-or-figure),
row "Failure record"; [MS-000 evidence policy §4](../ms-000/EVIDENCE-POLICY.md#4-provenance-requirements-for-any-eventual-result-or-figure)).
The private logs are kept unchanged and are identified here by SHA256. Local paths, host names and user names are
omitted from this public summary.

## F1. Geometry generator, attempt 1

This was a non-chemistry construction failure in a geometric builder. No engine ran, and no energy, force or
gradient was evaluated.

| Item | Record |
|---|---|
| Start (UTC) | 2026-09-26T19:16:24Z |
| Invocation | `python tools/build_ms001_geometries.py`, run from the repository root in the project-local environment (CPython 3.12.14, ASE 3.29.0, NumPy 2.5.3) |
| Exit code | 1 |
| Error class | `IndexError: list index out of range` |
| Failing location | Function `build_m1`, at the dimer-axis selection: line 103 of the script version that ran (`tools/build_ms001_geometries.py`), called from `main` at line 318 |
| Output | None. The script created the output directory `structures/ms-001/` before it failed and left it empty. It wrote no geometry file, record or other output |
| Script version that ran | Its SHA256 was not recorded before the script was edited [GAP]. The failing statement and the change are described below |
| Private log | Retained unchanged, SHA256 `4592247d4462cc61123bf616b9566909b55c3df38b0a75eab486755a202783ca` |

**Cause.** To find the dimer axis, the builder takes one top-layer atom of its finite lattice patch and looks up that
atom's two lattice neighbours in the virtual layer above. The version that ran used the first top-layer atom in the
patch. That atom lies on the patch edge, and only one of its two upper neighbours exists inside the finite patch, so
the lookup of the second neighbour raised `IndexError`.

**Change.** The reference atom is now the top-layer atom nearest the lateral centre of the patch, and an assertion
requires exactly two upper-layer neighbours before the axis is chosen. The corrected generator is reviewed before
any further run. Later attempts are numbered separately and never replace this record.

## F2. Geometry generator, attempt 2: completed run, superseded for a metadata defect

This entry records a defect in derived metadata, not a failed run. No engine ran, and no energy, force or gradient
was evaluated.

| Item | Record |
|---|---|
| Start (UTC) | 2026-09-26T19:24:15Z |
| Invocation | `python tools/build_ms001_geometries.py`, generator SHA256 `c7d14e03de21bdfbe68d805c63b0ce627a0fc7515952af17fafcdd4bd4e294ff`, reviewed before the run |
| Exit code | 0; seven output files written |
| Defect | In `geometry-record.json`, the P2 entry recorded `H-X-C_angle_deg` = `70.52877936550931`. Measured on the written P2 coordinates, all three H–Ge–Cα angles and all three H–Si–Cβ angles are 109.471° (the ideal tetrahedral angle, arccos(−1/3)). The coordinates are correct; the recorded derived value is wrong. The generator computed the supplement, 180° − 109.471°, beside the construction formula instead of measuring the angle at the heavy atom between the H direction and the bonded C direction |
| Scope of the defect | One derived number in `geometry-record.json`. The extxyz headers carry no numeric angle |
| What the digest agreement showed | All six file rows in `geometry-record.json` matched the SHA256 of the files on disk. That is an integrity check only, not a correctness check: a digest that agrees with a wrong value still agrees |
| Disposition | Attempt 2 is retained as a recorded attempt and superseded. Its run log and all seven output files are kept unchanged in the private record with the digests below. The generator is corrected to measure every reported distance and angle on the coordinates read back from the written files and to assert each declared value within declared tolerances (distances 1 × 10⁻⁶ Å, angles 1 × 10⁻⁴°). Regeneration is a separately numbered attempt 3, run only after review of the corrected generator |

Attempt-2 digests (SHA256), retained:

| File | SHA256 |
|---|---|
| `geometry-record.json` | `933392220e9ca809fe55b8d7d8610dd3bf62a496a3f0326232c084dfe382614e` |
| `M1-build-site.extxyz` | `ddc9867085919924dd73435755b1ece7d8b5cb644a33908cef2c6b4dbfdd1ee7` |
| `start-combined.extxyz` | `429d10eab9461d32a901fdc44ee06311bf6041bba22cb1e9bbc6cb7708133963` |
| `V1-separated-bodies.extxyz` | `2fe09b2ebd663dbe06762b6b082e27b2695ccd57f7e18786d81c18fdce644809` |
| `V2-contact-GeC-intact.extxyz` | `712a892d5514f3170ce33cf7d3f98b010b025153e5a061c8bdebe6c84a48c2de` |
| `V3-pendent-C2-GeC-broken.extxyz` | `ed74e66f68858fc5c1031145c7d164e71634a5dcd71fc7fedf2b7f38e7492e8d` |
| `P2-test-molecule-H3GeCCSiH3.extxyz` | `4d28620a0aff9cadaa8967e53c0ff7624f6c372ebbd48b5884f702c62be27a69` |
| Private run log | `db868255d9694b7a95870900eb375b8062624acfeefd5d518dd9745ecace5a44` |

The generator bytes that ran in attempt 2 are retained privately with the SHA256 above,
`c7d14e03de21bdfbe68d805c63b0ce627a0fc7515952af17fafcdd4bd4e294ff`.

**Attempt 3.** The corrected generator was reviewed and then run once, at 2026-09-26T19:39:02Z with exit code 0. Its
SHA256 is `bb1b2a99b352bc773c3e858d4aac3cd0596597b5cf87dedbc1182f933ee9ab13`. It regenerated all seven files, and
each header now carries that generator digest. The attempt-3 files and their digests are listed in
[structures/ms-001/README.md](../../structures/ms-001/README.md).

Measured on the written P2 file, all six H–X–C angles are 109.4712°, and the record carries the measured values.
Measuring constructed values against declared ideal values establishes the internal consistency of a geometric
construction. It is not physical validation, and it says nothing about chemistry, bonding or stability.
