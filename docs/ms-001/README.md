# MS-001 Stage 0 package (scope option B)

This package holds the Stage 0 definitions of MS-001 under scope option B, the declared-deviation prospective study
([MS-000 compute spike §5](../ms-000/MS-000-COMPUTE-SPIKE.md#5-reproduction-readiness-and-scope-options)). Stage 0
defines and freezes the model, the method scheme, the drive, the tolerances and the validation set. It runs no
chemistry: the only execution was a provenance wiring test on a trivial job that adds two integers.

**What this package does not establish.**
- **Only Stage 0 of option B is authorized** ([C1](C1-AUTHORIZATION.md)).
- **Faithful reproduction is still blocked.** Option A remains BLOCKED on missing benchmark inputs and missing
  parity and coupling evidence.
- **Parity is unknown.** Parity with the benchmark is unknown for every item.
- **No coupling route has been demonstrated.** No composition of GFN0-xTB with ωB97X-D3 has been demonstrated
  through any route (P3b is open). The six capability and validation gaps of the selected route, listed in
  [C2 §5](C2-COUPLING-ROUTE.md#5-what-the-official-documentation-does-not-establish), all stay open:
  1. link atoms in `MIXED`;
  2. different methods per sub-force_eval;
  3. the numerical mixing derivative;
  4. GFN0 under open-shell settings;
  5. ωB97X-D3 with exact exchange in GAPW;
  6. validation of the composite coupled energy and gradient (C6).
- **Approval of C4 is not validation.** The corrected definitions have independent review approval and Lead
  acceptance, and on 2026-09-27 a person approved C4, bound to its exact SHA256, as the prospective numerical
  protocol of Stage 0 ([approval record](C4-HUMAN-APPROVAL.md)). Stage 0 is therefore closed as a set of frozen
  prospective definitions. Neither the acceptance, the approval nor the closure is readiness or physical validation,
  and none upgrades an evidence label; E3's minimum persistence Δd_min = 0.20 Å, for example, remains an arbitrary
  `[AGENT]` declaration without physical validation.
- **Stage 1 is BLOCKED and not authorized.** It needs a separate authorization and its prerequisites below.

The package contains no energy, force, gradient, optimized structure or other physical result. Every model,
setting and threshold in it is `[AGENT]`, a declared deviation.

## Records

| Item | Record | What it contains |
|---|---|---|
| C1 | [C1-AUTHORIZATION.md](C1-AUTHORIZATION.md) | The authorization of option B, Stage 0 only, dated and kept separate from the MS-000 gate |
| B1, C7 geometries | [structures/ms-001](../../structures/ms-001/README.md) | Model M1, the start configuration, validation configurations V1–V3 and the P2 molecule, all built geometrically with no relaxation; M2 reused by digest; every `[AGENT]` choice listed |
| C3 | [C3-PROVENANCE-WIRING.md](C3-PROVENANCE-WIRING.md) | ASE and AiiDA data-model review, the frozen provenance field set, one trivial job and a coverage table (2 fields demonstrated on the job, 5 by surrogate, 4 not demonstrated) |
| C2 | [C2-COUPLING-ROUTE.md](C2-COUPLING-ROUTE.md) | Comparison of the three coupling candidates against the declared partition; selection of CP2K `MIXED`/`GENMIX` and its specification; what the documentation does not establish |
| B2 | [B2-METHOD-DECLARATION.md](B2-METHOD-DECLARATION.md) | Partition by atom id, cut bonds and link atoms, charge and spin, the GFN0 selector with its provenance requirement, ωB97X-D3 parameters and D3 form, basis and core treatment for H, C, O, Si, Ge and I, and engine numerics |
| B3 | [B3-DRIVE-PROTOCOL.md](B3-DRIVE-PROTOCOL.md) | Fixed atom sets by id, rigid displacement, the base, coarser and finer steps, branches, per-step relaxation, bookkeeping and checkpoint selectors; NEB excluded as a substitute |
| C4 | [C4-TOLERANCES-AND-CONVERGENCE.md](C4-TOLERANCES-AND-CONVERGENCE.md) | Every row of the spike's §8.6 tolerance table instantiated, the protocol N1–N8, and the binding revision sequence |
| C4 approval | [C4-HUMAN-APPROVAL.md](C4-HUMAN-APPROVAL.md) | The human approval of C4 on 2026-09-27, bound to path, commit and SHA256, with its scope, the limits that stand and the qualification of C4's frozen opening bullet |
| C7 | [C7-VALIDATION-SET.md](C7-VALIDATION-SET.md) | Validation configurations, the components tested by the finite-difference checks, the P2 test molecule and its isolated-molecule treatment, and the Stage 2 checkpoint selectors |
| Failures | [FAILURE-RECORD.md](FAILURE-RECORD.md) | Geometry attempt 1 (failed before writing anything) and attempt 2 (superseded for a metadata defect), both retained |
| Sources | [SOURCE-LEDGER.md](SOURCE-LEDGER.md) | Every source used, with URL, version, locator, access time and the digest of the retrieved bytes |
| Freeze | [STAGE0-FREEZE-RECORD.md](STAGE0-FREEZE-RECORD.md) | Path, SHA256 and evidence label of every frozen artifact |

## Open items, by when they must be settled

None of these is claimed. The categories match the
[freeze record](STAGE0-FREEZE-RECORD.md#1-disposition).

- **Prerequisites to starting Stage 1.**
  - A separate Stage 1 authorization. Independent review approval and Lead acceptance of the corrected Stage 0
    items, and the human approval of C4, are recorded; they authorize nothing.
  - The C3 blockers: identity-chain survival, the remaining provenance extensions, and the login-shell environment
    gap ([C3 §5](C3-PROVENANCE-WIRING.md#5-coverage-table)).
  - Five definitions to settle from version-matched source: GFN0 parameter provenance through CP2K (G4), CP2K's unit
    for `OMEGA`, the normalization of single-primitive basis coefficients, the printed representations that N8
    compares, and whether the compiled Psi4 SCF and gradient steps use any fitting basis under the declared settings
    (B2 §6). N8 is BLOCKED until both compared representations, and with them the combined formatting allowance r,
    are defined (C4 row 10).
- **Dependencies within Stage 1.**
  - CP2K installation and build identity, including its libxc version.
  - The five route capabilities of C2 §5, items 1 to 5.
  - Mulliken spin populations for E1 inside `MIXED`.
  - The remaining N2 representation checks.
- **Stage 2 gates.**
  - C5, which includes P2's check against the defining ωB97X-D3 reference, not obtained `[GAP]`.
  - C6, which needs N5 and N8.
  - B4: parity unknown.

Two declared items stand without a pending test. CP2K's hard-coded D3 sr8 = 1.0 is declared as a deviation. E3(iii)
is INDETERMINATE by declaration (C4, row 7).
