# Structures

This directory contains two candidate geometries of the benchmark's molecular tool, in its iodinated and
activated forms. Both are agent-proposed and unoptimized. They are RDKit ETKDGv3 distance-geometry embeddings with
seed `20260916`, obtained without a force field, a quantum-chemical step or relaxation. They are proposals built
from literature identity statements, not measurements, and carry no claim about stability, bonding or pathways.
They have not been compared with the benchmark authors' supplementary coordinates, which have not been obtained.

| File | Atoms | Composition | Proposed charge / multiplicity | Notes |
|---|---|---|---|---|
| [`donor-precursor-EAOGe-C2I.extxyz`](donor-precursor-EAOGe-C2I.extxyz) | 49 | C17 H27 Ge I O3 | 0 / 1 | Iodinated, closed-shell candidate |
| [`donor-activated-EAOGe-C2-radical.extxyz`](donor-activated-EAOGe-C2-radical.extxyz) | 48 | C17 H27 Ge O3 | 0 / 2 | De-iodinated candidate; `radical_electrons` = 1 on `D-Cb` |

## Format

The files use the extended XYZ format, with coordinates in ångström and no periodicity (`pbc="F F F"`). Each atom
line records the columns `species`, `pos` (x, y and z), the stable identifier `atom_id` described in
[docs/donor-candidates.md](../docs/donor-candidates.md), the skeleton number `map_num` (0 for hydrogens) and
`radical_electrons`. The header keys record:
- the origin (`agent-proposed/reconstructed`) and the optimization status
- `stability_claim=none` and `evidence_class=AGENT`
- the name and SHA256 of the generator
- the RDKit and ASE versions and the ETKDG seed
- a literature locator
- the proposed charge and multiplicity

## Public adaptation

These files are not the original hash-bound records. Only the second line, the header, differs from the originals:
- An internal task identifier was removed.
- In the literature locator, references to private cache file names were replaced by the public locator "Barrera
  et al. arXiv:2512.24431 SI p15".
- The keys `public_adaptation=` and `original_sha256=` were added. The latter records the SHA256 of the original
  file.

The atom-count line and every atom line are byte-identical to the original records. Source and export hashes are
listed in [provenance/EXPORT-MANIFEST.md](../provenance/EXPORT-MANIFEST.md).

The generating script is not published. It reads locally cached third-party supplementary text, which was excluded
from this export pending redistribution review. The coordinate files of the surface models are also not published,
for the reasons given in [docs/donor-candidates.md](../docs/donor-candidates.md), Section 6. Figure 1 of the
README is rendered from the activated file by [`tools/render_donor_plate.py`](../tools/render_donor_plate.py),
which reads the file without modifying it.
