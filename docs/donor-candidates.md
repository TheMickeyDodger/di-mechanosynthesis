# Donor candidates and model definitions

**Everything on this page is `[AGENT]` — proposed, reconstructed and unoptimized — unless marked otherwise.**
The two donor-candidate files in [`../structures/`](../structures/README.md) are proposals built from literature
identity statements. They are not measurements, not relaxed structures, and have not been compared against the
benchmark authors' supplementary coordinates, which this project has not obtained. Structure-generation inputs
and their sources are indexed in [SOURCES.md](SOURCES.md) §4.

## 1. The molecular tool

| Item | Value | Class |
|---|---|---|
| Common name | EAOGe-C2I | `[LIT]` ([Cowie et al.](https://arxiv.org/abs/2605.27250), "Mechanosynthetic C2 donation") |
| Description | Ge-substituted adamantane, C2 group with iodine cap, three OH-terminated legs | `[LIT]` (same) |
| Systematic name (as recorded in the original reconstruction notes) | 2,2′,2″-(1-(iodoethynyl)-1-germaadamantane-3,5,7-triyl)tris(ethan-1-ol) | Attributed by those notes to the supplementary information of [Barrera et al.](https://arxiv.org/abs/2512.24431), p. 15. **Not verified against that source in the current review.** |
| Activated form | De-iodinated tool EAOGe-C2•, with the unpaired electron on the terminal carbon | Event `[LIT]` (Cowie et al., "C2 donation mechanism"); graph edit `[AGENT]` |

### Molecular graph (generated with RDKit 2026.03.6)

| Item | Precursor (iodinated) | Activated (de-iodinated radical) |
|---|---|---|
| Formula | C17H27GeIO3, 49 atoms | C17H27GeO3, 48 atoms |
| Formal charge / unpaired electrons | 0 / 0 | 0 / 1 on `D-Cb` |
| InChIKey | `IJKSFCOUIXSZDJ-UHFFFAOYSA-N` | `PRAWODXJAOCADR-UHFFFAOYSA-N` |

Precursor input SMILES, with atom maps equal to the skeleton numbering. For the activated form, `[C:12][I:13]`
becomes `[C:12]`, a bracket atom with no hydrogens.

```text
[Ge:1]12([C:11]#[C:12][I:13])[CH2:2][C:3]3([CH2:14][CH2:15][OH:16])[CH2:4][C:5]([CH2:17][CH2:18][OH:19])([CH2:9]1)[CH2:6][C:7]([CH2:20][CH2:21][OH:22])([CH2:10]3)[CH2:8]2
```

### Stable atom IDs (heavy atoms; hydrogens are `<parent>-H1`, `<parent>-H2`)

| Atom ID | Element | Role |
|---|---|---|
| `D-Ge1` | Ge | cage position 1, bonded to `D-C2`, `D-C8`, `D-C9`, `D-Ca` |
| `D-C2`, `D-C8`, `D-C9` | C | cage CH2 bonded to Ge |
| `D-C3`, `D-C5`, `D-C7` | C | quaternary bridgeheads, each carrying one leg |
| `D-C4`, `D-C6`, `D-C10` | C | cage CH2 between bridgeheads |
| `D-Ca` | C | alkyne carbon bonded to Ge |
| `D-Cb` | C | terminal alkyne carbon; radical site after activation |
| `D-I1` | I | iodine cap (precursor only) |
| `D-L1a`, `D-L2a`, `D-L3a` | C | leg CH2 on the bridgeheads |
| `D-L1b`, `D-L2b`, `D-L3b` | C | leg CH2 bonded to O |
| `D-O1`, `D-O2`, `D-O3` | O | hydroxyl feet (`D-O1-H1`, …) |

## 2. Composition and electron bookkeeping

These counts were re-derived directly from the structure files during the current review. They are bookkeeping on
file contents, not electronic-structure results.

| File | Atoms | Composition | Charge / multiplicity (proposed) | Electrons (all-electron) | Parity check | Radical flag |
|---|---|---|---|---|---|---|
| precursor | 49 | C17 H27 Ge I O3 | 0 / 1 | 238 (even) | consistent with a singlet | none |
| activated | 48 | C17 H27 Ge O3 | 0 / 2 | 185 (odd) | consistent with a doublet | 1, on `D-Cb` |

The two compositions differ by exactly one iodine atom. With an effective core potential on iodine, the
explicitly treated electron count of the precursor is 238 − *n*<sub>core</sub>(I). The value of *n*<sub>core</sub>
for the selected basis is **`UNVERIFIED`** from project sources and must come from the installed engine's basis
library or output. The activated donor contains no iodine, so it needs no effective core potential.

## 3. How the coordinates were generated

- **Donor candidates only:** RDKit ETKDGv3 distance-geometry embedding, seed `20260916`, units Å.
- **No force field, no quantum-chemical step, no relaxation, no stability claim.**
- **Headers:** each file records the generator's name and SHA256. The generator is **not published**. It reads
  locally cached third-party supplementary text for its consistency checks, and that text was excluded from this
  export pending redistribution review.
- **Conformation:** the leg conformation is one ETKDG embedding. Other seeds are a prospective sensitivity test,
  not run.

## 4. What the original reconstruction notes state (historical claims; not verified in the current review)

The following are claims recorded in the project's original reconstruction notes. They are reported here so that
the uncertainty in the donor's identity stays visible. They are **not** newly verified primary evidence, and none
was checked against the cited sources in the current review.

- **Graph vs name and spectra:** the notes state that the spectroscopic data they cite (¹H integrals and ¹³C
  environments) are consistent with the name-derived graph.
- **Graph vs other sources:** the notes state that the connectivity is consistent with the tool scheme in
  [Blue et al.](https://arxiv.org/abs/2606.13876) and with a text description in patent US11708384B2.
- **Mass-spectrometry mismatch:** the notes record that a printed high-resolution mass-spectrometry formula in the
  cited source does **not** match the name-derived graph. They keep the name-derived graph and assert neither a
  typo nor a correction.

The donor identity therefore rests on literature statements as recorded in those notes, and it remains
**unverified** in the current review.

## 5. Surface model definitions (defined; coordinate files not published)

The reconstruction also defined three silicon models. **They were not built with ETKDG.** They use an ASE
`diamond100` Si lattice (a = 5.43 Å) with geometric (2×1) dimer formation at a placeholder Si–Si distance,
hydrogen caps along ideal tetrahedral directions, and boundary pruning for the finite models. All are unoptimized.

| Model | Definition | Atoms | Role |
|---|---|---|---|
| (a) | H:Si(100)-(2×1) periodic slab with one inter-row dangling-bond pair; 4 dimer rows × 6 dimers × 6 layers | 430 | build-site definition (Cowie-like) |
| (c) | H:Si(100)-(2×1) finite cluster with the same pair rule; 6 rows × 5 dimers × 4 layers, H-capped | 440 | finite Cowie-like build site |
| (b) | clean Si(100)-(2×1) finite comparator cluster with a C2 placeholder (C–C 1.52 Å, a placeholder value) | 384 | comparator after the MacLean preprint (arXiv:2607.19488v1, as recorded by the reconstruction); **not** a benchmark reference |

- **Choices, not sourced facts:** the dangling-bond pair rule, dimer geometry, cap lengths, extents and
  constraint conventions are `[AGENT]` choices. Each has a stated alternative as a prospective sensitivity test.
- **Not built:** no combined tool-over-surface or attached coordinates exist.
- **Why the coordinate files are not published:** they are not inputs to the first experiment, and they contain
  placeholder geometry that is easy to mistake for a model of the benchmark.

## 6. Open questions

- **No primary coordinates:** the benchmark authors' supplementary coordinates and input archives have not been
  obtained, so neither the donor candidates nor the surface models have been compared against them.
- **Conformation unexplored:** leg conformation, attachment mode and tool placement over the build site are
  proposals with untested alternatives.
- **Charge and spin are hypotheses:** the assignments in §2 are consistent with electron-count parity, but they
  are not electronic-structure results.
