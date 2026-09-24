# Donor candidates and model definitions

This document describes the two proposed donor geometries in [`../structures/`](../structures/README.md), the
method used to draw Figure 1 from one of them, and the surface models defined alongside them. Unless a statement is
marked otherwise, everything described here is agent-proposed (`[AGENT]`), reconstructed and unoptimized. The
donor geometries are proposals built from literature identity statements; they are neither measurements nor
relaxed structures. They have not been compared against the benchmark authors' supplementary coordinates, which
this project has not obtained. Numbered citations refer to [SOURCES.md](SOURCES.md), whose Section 4 lists the
structure-generation inputs.

## 1. The molecular tool

| Item | Value | Class and source |
|---|---|---|
| Common name | EAOGe-C2I | `[LIT]`; Cowie et al. [1], "Mechanosynthetic C2 donation" |
| Description | Germanium-substituted adamantane with a C2 group, an iodine cap and three OH-terminated legs | `[LIT]`; same locator |
| Systematic name, as recorded in the original reconstruction notes | 2,2′,2″-(1-(iodoethynyl)-1-germaadamantane-3,5,7-triyl)tris(ethan-1-ol) | Attributed by those notes to the supplementary information of Barrera et al. [2], p. 15; not verified against that source in the current review |
| Activated form | De-iodinated tool EAOGe-C2•, with the unpaired electron on the terminal carbon | The de-iodination event is `[LIT]` (Cowie et al. [1], "C2 donation mechanism"); the graph edit is `[AGENT]` |

The molecular graphs were generated with RDKit 2026.03.6.

| Item | Precursor (iodinated) | Activated (de-iodinated radical) |
|---|---|---|
| Formula | C17H27GeIO3, 49 atoms | C17H27GeO3, 48 atoms |
| Formal charge / unpaired electrons | 0 / 0 | 0 / 1 on `D-Cb` |
| InChIKey | `IJKSFCOUIXSZDJ-UHFFFAOYSA-N` | `PRAWODXJAOCADR-UHFFFAOYSA-N` |

The precursor input SMILES is given below, with atom-map numbers equal to the skeleton numbering. In the activated
form, `[C:12][I:13]` becomes `[C:12]`, a bracket atom with no hydrogens.

```text
[Ge:1]12([C:11]#[C:12][I:13])[CH2:2][C:3]3([CH2:14][CH2:15][OH:16])[CH2:4][C:5]([CH2:17][CH2:18][OH:19])([CH2:9]1)[CH2:6][C:7]([CH2:20][CH2:21][OH:22])([CH2:10]3)[CH2:8]2
```

The structure files carry stable atom identifiers. Hydrogen atoms are named after their parent, as in
`<parent>-H1` and `<parent>-H2`. The heavy atoms are listed below.

| Atom ID | Element | Role |
|---|---|---|
| `D-Ge1` | Ge | Cage position 1, bonded to `D-C2`, `D-C8`, `D-C9` and `D-Ca` |
| `D-C2`, `D-C8`, `D-C9` | C | Cage CH2 groups bonded to Ge |
| `D-C3`, `D-C5`, `D-C7` | C | Quaternary bridgeheads, each carrying one leg |
| `D-C4`, `D-C6`, `D-C10` | C | Cage CH2 groups between bridgeheads |
| `D-Ca` | C | Alkyne carbon bonded to Ge |
| `D-Cb` | C | Terminal alkyne carbon; the radical site after activation |
| `D-I1` | I | Iodine cap, precursor only |
| `D-L1a`, `D-L2a`, `D-L3a` | C | Leg CH2 groups on the bridgeheads |
| `D-L1b`, `D-L2b`, `D-L3b` | C | Leg CH2 groups bonded to O |
| `D-O1`, `D-O2`, `D-O3` | O | Hydroxyl feet (`D-O1-H1` and so on) |

## 2. Composition and electron bookkeeping

The counts below were re-derived directly from the structure files during the current review. They are
bookkeeping on file contents, not results of electronic-structure calculations.

| File | Atoms | Composition | Proposed charge / multiplicity | All-electron count | Parity check | Radical flag |
|---|---|---|---|---|---|---|
| Precursor | 49 | C17 H27 Ge I O3 | 0 / 1 | 238 (even) | Consistent with a singlet | None |
| Activated | 48 | C17 H27 Ge O3 | 0 / 2 | 185 (odd) | Consistent with a doublet | 1, on `D-Cb` |

The two compositions differ by exactly one iodine atom. With an effective core potential on iodine, the number of
electrons treated explicitly in the precursor is 238 − *n*<sub>core</sub>(I). When the E-01 attempt built the
selected basis with the installed Psi4 1.11, the engine reported *n*<sub>core</sub>(I) = 46 and 192 explicit
electrons for the precursor ([`../results/e01/raw/P-RKS-core.psi4.out`](../results/e01/raw/P-RKS-core.psi4.out)).
This is basis-construction output only; no SCF completed. The activated donor contains no iodine and needs no
effective core potential.

## 3. Generation of the coordinates

Only the donor candidates were embedded by RDKit ETKDGv3 distance geometry [13], with seed 20260916 and
coordinates in ångström. No force field, quantum-chemical step or relaxation followed, and no claim is made about
stability. Each file records the name and SHA256 of the generating script. The generator itself is not published,
because it reads locally cached third-party supplementary text for its consistency checks, and that text was
excluded from this export pending redistribution review. The leg conformation is a single ETKDG embedding. Other
seeds constitute a prospective sensitivity test that has not been run.

## 4. Figure 1: rendering method

Figure 1 of the README shows the 21 heavy atoms of the activated candidate. It is drawn by
[`../tools/render_donor_plate.py`](../tools/render_donor_plate.py), a deterministic script that uses the Python
standard library only.

The script reads all 48 atoms of the unchanged structure file. It reads the heavy-atom bonds from
[`../tools/activated-donor-bonds.tsv`](../tools/activated-donor-bonds.tsv), which transcribes the 23 heavy-atom
bonds of the SMILES above, without the C12–I13 bond, together with each atom's map number. Each hydrogen is bonded
to the parent named in its identifier. Before drawing, the script checks every map number against the `map_num`
column of the structure file, confirms that every atom is bonded, and requires each listed bond length to fall
within 0.9–2.10 Å (0.9–1.25 Å for bonds to hydrogen). It changes no coordinate and computes no chemistry.

The projection is orthographic:
- **Axes.** The vertical page axis follows the direction from `D-Ge1` to `D-Cb`. The reference horizontal axis
  follows the direction from `D-C7` to `D-C3`, orthogonalized against it.
- **View angles.** The azimuth about the vertical axis and the tilt about the horizontal axis are chosen from a
  fixed grid, of azimuths in 5° steps and tilts of 10° to 30° in 5° steps. The choice minimizes the summed overlap
  of projected heavy-atom discs, with ties going to the smallest azimuth and then the smallest tilt. For this
  structure the selected view has an azimuth of 10° and a tilt of 25°.
- **Drawing.** Hydrogen atoms are omitted. The atom discs use fixed display radii: 0.40 Å for Ge, 0.28 Å for C
  and 0.27 Å for O, in drawing units. These radii are graphic conventions chosen for legibility, not physical
  atomic radii. Bond strokes are clipped at the projected atom edges, and the triple bond is drawn as three
  parallel strokes.
- **Labels.** The labels map to atom identifiers as follows: Ge is `D-Ge1`, Cα is `D-Ca`, Cβ is `D-Cb`, and O1 to
  O3 are `D-O1` to `D-O3`.
- **Scale.** A scale bar of 2 Å is included.

The figure depicts the proposed input and not an optimized or validated structure. Rerunning
`python3 tools/render_donor_plate.py` from the repository root regenerates it.

## 5. Statements in the original reconstruction notes

The project's original reconstruction notes contain three claims about the donor's identity. They are reported
here so that the uncertainty in that identity remains visible. They are historical claims rather than newly
verified primary evidence, and none was checked against the cited sources in the current review.
- The notes state that the spectroscopic data they cite, ¹H integrals and ¹³C environments, are consistent with the
  name-derived graph.
- They state that the connectivity agrees with the tool scheme of Blue et al. [3] and with a text description in
  patent US11708384B2 [5].
- They record that a printed high-resolution mass-spectrometry formula in the cited source does not match the
  name-derived graph. The notes retain the name-derived graph and assert neither a typographical error nor a
  correction.

The identity of the donor therefore rests on literature statements as recorded in those notes, and it remains
unverified in the current review.

## 6. Surface model definitions

The reconstruction also defined three silicon models whose coordinate files are not published. They were not
generated by ETKDG. Each is built on an ASE `diamond100` silicon lattice [14] with a = 5.43 Å, with geometric
(2×1) dimer formation at a placeholder Si–Si distance, hydrogen caps along ideal tetrahedral directions and, for
the finite models, boundary pruning. All three are unoptimized.

| Model | Definition | Atoms | Role |
|---|---|---|---|
| (a) | H:Si(100)-(2×1) periodic slab with one inter-row dangling-bond pair; 4 dimer rows × 6 dimers × 6 layers | 430 | Build-site definition resembling the benchmark site |
| (c) | H:Si(100)-(2×1) finite cluster with the same pair rule; 6 rows × 5 dimers × 4 layers, hydrogen-capped | 440 | Finite build site resembling the benchmark site |
| (b) | Clean Si(100)-(2×1) finite comparator cluster with a C2 placeholder (C–C 1.52 Å, a placeholder value) | 384 | Comparator following the convention of MacLean et al. [4] (arXiv:2607.19488v1, as recorded in the reconstruction notes); not a benchmark reference |

The dangling-bond pair rule, the dimer geometry, the cap lengths, the extents and the constraint conventions are
`[AGENT]` choices. Each is paired with an alternative that forms a prospective sensitivity test. No coordinates
exist for a combined tool and surface or for an attached tool. The surface coordinate files are withheld, because
they are not inputs to the first calculation and their placeholder geometry could be mistaken for a model of the
benchmark.

## 7. Open questions

The benchmark authors' supplementary coordinates and input archives have not been obtained. Neither the donor
candidates nor the surface models have therefore been compared against them. Leg conformation, attachment mode and
the placement of the tool over the build site remain proposals with untested alternatives. The charge and
multiplicity assignments of Section 2 are consistent with electron-count parity. They are nevertheless hypotheses
rather than results of electronic-structure calculations.
