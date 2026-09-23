# Structures

Two **candidate** geometries of the benchmark's molecular tool, in its iodinated and activated forms.

> **Agent-proposed, unoptimized.** These are RDKit ETKDGv3 distance-geometry embeddings (seed `20260916`), with no
> force field, no quantum-chemical step and no relaxation. They are proposals built from literature identity
> statements, not measurements. They have not been compared against the benchmark authors' supplementary
> coordinates, which have not been obtained. They carry no stability, bonding or pathway claim.

| File | Atoms | Composition | Proposed charge / multiplicity | Notes |
|---|---|---|---|---|
| [`donor-precursor-EAOGe-C2I.extxyz`](donor-precursor-EAOGe-C2I.extxyz) | 49 | C17 H27 Ge I O3 | 0 / 1 | iodinated, closed-shell candidate |
| [`donor-activated-EAOGe-C2-radical.extxyz`](donor-activated-EAOGe-C2-radical.extxyz) | 48 | C17 H27 Ge O3 | 0 / 2 | de-iodinated candidate; `radical_electrons` = 1 on `D-Cb` |

## Format

Extended XYZ, coordinates in ångström, non-periodic (`pbc="F F F"`).

- **Per-atom columns:** `species`, `pos` (x y z), `atom_id` (stable ID, see
  [docs/donor-candidates.md](../docs/donor-candidates.md)), `map_num` (skeleton numbering; 0 for hydrogens) and
  `radical_electrons`.
- **Header keys:** record the origin (`agent-proposed/reconstructed`), the optimization status, `stability_claim=none`,
  `evidence_class=AGENT`, the generator name and SHA256, the RDKit and ASE versions, the ETKDG seed, a
  literature locator, and the proposed charge and multiplicity.

## Public adaptation (these are not the original hash-bound records)

Only line 2, the header, differs from the project's original records:
- **Removed:** an internal task identifier.
- **Changed:** in the literature locator, references to private cache file names were replaced by the public
  locator "Barrera et al. arXiv:2512.24431 SI p15".
- **Added:** `public_adaptation=` and `original_sha256=`. The latter records the SHA256 of the original file.

The atom count line and every atom line are byte-identical to the original. Source and export hashes are listed
in [provenance/EXPORT-MANIFEST.md](../provenance/EXPORT-MANIFEST.md).

The generator script is not published. It reads locally cached third-party supplementary text, which was
excluded from this export pending redistribution review. Surface-model coordinate files are also not published (see
[docs/donor-candidates.md](../docs/donor-candidates.md) §5).
