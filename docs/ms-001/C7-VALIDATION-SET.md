# C7 validation set, P2 test molecule and Stage 2 checkpoint selectors

Status: MS-001 Stage 0, scope option B. Everything here is `[AGENT]` and declared before Stage 1. The configurations
are unrelaxed geometric inputs, not results. No calculation was run to build or select them.

## 1. Validation configurations

The configurations were built geometrically from the frozen model (B1) and the drive inputs (B3), as recorded in
[structures/ms-001](../../structures/ms-001/README.md). Their SHA256 digests are listed there and in the freeze
record.

| Member | File | Recipe (nominal name only; no bond state is claimed) |
|---|---|---|
| V1 | `V1-separated-bodies.extxyz` | The start of the approach branch, identical to `start-combined.extxyz` |
| V2 | `V2-contact-GeC-intact.extxyz` | The start tool rigidly translated so that `D-Cb` lies 1.87 Å from `S-L1-07-05`, along that site's nominal outward direction. `D-Ge1`–`D-Ca` is at its M2 distance, 1.8369 Å |
| V3 | `V3-pendent-C2-GeC-broken.extxyz` | V2 with `D-Ca` and `D-Cb` kept in place and the other 46 tool atoms translated by (0, 0, +1.50) Å. `D-Ge1`–`D-Ca` is 3.3368 Å |

The three members cover the constructed situations the branches are expected to pass through (spike §8.5): the
separated bodies, contact with the Ge–C distance at its tool value, and the C2 unit left at the site. That these
situations occur on the branches is a hypothesis, not a result.

## 2. Components tested by the finite-difference checks

Nine atoms are displaced, and every Cartesian component of each is tested (27 components per configuration) on V1,
V2 and V3. They include the boundary and link-host atoms of the declared partition
([B2 §2](B2-METHOD-DECLARATION.md#2-partition-embedding-and-cut-bonds)).

| Atom | Role in the scheme |
|---|---|
| `D-Cb`, `D-Ca` | Reaction atoms, in the high-level region |
| `D-Ge1` | Reaction atom, in the high-level region, and not a link host |
| `D-C2` | Link host of the cut bond `D-C2`–`D-C3`, in the high-level region |
| `D-C3` | Partner of that cut, in the low-level region only; enters E1 and E2 through the link-atom position |
| `S-L1-07-05` | Three-coordinate site and link host of `S-L1-07-05`–`S-L2-07-04` |
| `S-L2-07-04` | Partner of that cut |
| `S-L1-05-05` | Dimer partner of the site, host of `S-L1-05-05`–`S-L2-05-04` |
| `S-L2-05-04` | Partner of that cut |

- **Composite check.** Performed in full-system coordinates on all 27 components, so that displacing a partner
  moves its link atom and exercises the chain-rule term.
- **Constituent checks.** E3 (GFN0 on the full system) is checked on all 27 components. E1 and E2, evaluated on S+L,
  are checked on:
  - the components of the six listed atoms that are in S;
  - the link atoms on the `D-C2`–`D-C3` and `S-L1-07-05`–`S-L2-07-04` cuts, each treated as an ordinary atom of
    the subset.
- **Fixed-atom checks (N8).** Tested on V1, V2 and V3 with the fixed sets H_M1 and H_T of B3 §1, in the constrained
  GEO_OPT runs that C4 row 10 names. Retained components are not compared.

## 3. The P2 test molecule

| Item | Declaration |
|---|---|
| File | `structures/ms-001/P2-test-molecule-H3GeCCSiH3.extxyz`, 10 atoms, C2 H6 Ge Si |
| Why this molecule | It holds the elements Ge, C, Si and H and the Ge–C and C–Si pairs that the declared scheme treats at the ωB97X-D3 level. O and I are not exercised: O is in the low-level region only, and I is absent from every frozen configuration (B2 §7) |
| Charge and multiplicity | 0 and 1, restricted in both engines (declared) |
| Model chemistry | Identical in both engines, as N2 requires ([C4 §2](C4-TOLERANCES-AND-CONVERGENCE.md#2-numerical-convergence-protocol)): all-electron def2-TZVP; libxc `HYB_GGA_XC_WB97X_D3` with α = 1.0, β = −0.804272 and ω = 0.25; two-body D3 with zero damping, s6 = 1.0, sr6 = 1.281, s8 = 1.0, sr8 = 1.0 and α6 = 14. The dispersion-input contract to Psi4 is established from source (B2 §6). The open representation items (basis normalization, the unit of `OMEGA`, the s-dftd3 r⁻⁸ damping exponent, the D3 cutoff treatments, libxc versions) are listed in B2 §8 |
| Engines | CP2K 2026.2 (GAPW, B2 §4) and Psi4 1.11 (B2 §6) |
| Isolated-molecule treatment in the periodic engine | CP2K `SUBSYS/CELL/PERIODIC NONE`, `DFT/POISSON/PERIODIC NONE` and `POISSON_SOLVER WAVELET`, which is documented for 0D systems and requires that "the density goes to zero on the faces of the cell". `PREFERRED_FFT_LIBRARY FFTSG` is required by that solver [S0-cp2k-poisson]. The cell is an orthorhombic box enclosing the molecule plus 8.0 Å on every side (declared; 10 and 12 Å on ladder rungs 1 and 2). Psi4 treats the molecule as isolated by construction |

## 4. Stage 2 checkpoint selectors

The selectors are defined once, deterministically, in
[B3 §5](B3-DRIVE-PROTOCOL.md#5-checkpoints-declared-here-applied-in-stage-2): the geometric triggers T_A and T_R, the
trigger step k_b, the anchor a_b, the window W_b, and the boundary rules for early and missing triggers, short or
terminated branches and zero accepted steps. This record uses those definitions unchanged. The **selection** of
configurations and segments is geometric only. The **comparison** at checkpoint S is not: it compares the inherited
events E1–E4 under their full criteria in B3 §5. Those criteria include E1's N6-resolved energy decrease, E2's
persistent Si–C bond and intact Si–Si bonds at the anchoring Si, E3's pendent-state condition persisting over the
declared minimum span, and E4's bridging criterion. A match of geometric lists alone never releases a segment or a
branch, and neither does a match of isolated E3 hits.

| Checkpoint | Configuration or segment selected (B3 §5) | Rule applied there |
|---|---|---|
| Branch check, approach | Accepted step a_A: the step k_A at which the geometric trigger T_A first holds, or J_A if T_A never holds. It is not selected by event E1 | The constituent and composite N5 checks, repeated at that configuration, with direct envelopes re-measured by production-rung repeats and one tighter aligned rung (N3, N4). PASS releases the branch; a failed or indeterminate check quarantines the whole branch and every branch started from it |
| Branch check, retraction | Accepted step a_R: the step k_R at which the geometric trigger T_R first holds, that is `D-Ge1`–`D-Ca` non-bonded at all three multiples, or J_R if that never happens | As above. The check applies only if R was started under the retraction-eligibility rule |
| Energy-sign configurations | Every actual Stage 2 configuration used in an E1 or E5 energy difference, including both steps k − 1 and k wherever the E1 bond part holds at k, in the base scan and in both sensitivity re-runs | N6. If a required value is missing or N6 cannot resolve the sign, the sign, and E1 at that step, are INDETERMINATE (B3 §5) |
| Sensitivity checkpoint S | Window W_b on each branch, including its clipped forms. If W_b has fewer than three accepted steps, no re-run is made and S is INDETERMINATE | Coarse (0.20 Å, with a final 0.10 Å step when n_b is odd) and fine (0.05 Å) re-runs from step s_b, ending exactly at d(e_b). The ordered first occurrences of the inherited events E1, E2, E3 and E4, each under its full criterion in B3 §5, must be identical across the three runs. E3 counts only where its pendent-state condition persists over the declared minimum Δd_min = 0.20 Å of imposed d, and it is placed at the first step of that span (B3 §5, E3 persistence). An isolated E3 hit is not an occurrence and never contributes to a release. An event that is INDETERMINATE at any accepted step of any run in the interval, including an E1 sign that N6 cannot resolve or an E3 whose persistence cannot be established inside the interval, makes S INDETERMINATE. A match of geometric lists alone never releases the segment. A changed or INDETERMINATE order, or a terminated run, quarantines the span from s_b onward (spike §8.5) |
| Zero accepted steps | A branch with no accepted base step: on A, step 0 is not accepted; on R, the first retraction step is not accepted. No J_b, k_b, a_b or W_b exists, so no configuration or segment is selected | The branch check and checkpoint S for that branch are INDETERMINATE (blocking), and no sensitivity re-run is made. No dependent branch starts: if A has no accepted step, R is recorded as not started (approach has no accepted step). A restart happens only through the revision sequence |
