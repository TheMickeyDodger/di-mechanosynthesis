# C4 tolerances, acceptance budgets and numerical-convergence protocol

Status: MS-001 Stage 0, scope option B. This record instantiates every row of the spike's §8.6 table, the
numerical-convergence protocol N1–N8 and the revision sequence, with a concrete declared value or a documented
default cited for the exact version.

- **Approval.** The roles are those of spike §8.6. The values are proposed by the method author (this package,
  `[AGENT]`), are checked by the independent reviewer and are approved by a person. The independent review checked
  and approved the package, and final Lead acceptance is recorded. **Approval by a person is still PENDING**: no
  value here is approved by a person yet, and nothing here authorizes Stage 1 or claims readiness, parity or any
  physical result.
- **Freezing.** No value is chosen or adjusted from a result of this program. Every value is frozen before Stage 1.

Three terms are used exactly as the spike defines them (§8.6):
- A **stopping criterion**, such as an SCF or optimizer threshold, ends an iteration. It is not an accuracy bound.
- An **empirical stability envelope** is the observed spread of a quantity under declared perturbations. It is not a
  rigorous error bound.
- An **acceptance budget** is a declared tolerance, frozen and reviewed. It is a proposal, not a validated
  uncertainty, and results are reported against it.

No value below is presented as physically justified. No rigorous error bound is claimed anywhere.

## 1. Tolerance table (spike §8.6), instantiated

| # | Quantity | Declared value or cited default | Pass/fail rule (unchanged from the spike) |
|---|---|---|---|
| 1 | Force convergence per accepted step | The CP2K 2026.2 `GEO_OPT` defaults [S0-cp2k-geo-opt]: `MAX_FORCE 4.5e-4` hartree/bohr, `RMS_FORCE 3.0e-4` hartree/bohr, `MAX_DR 3.0e-3` bohr, `RMS_DR 1.5e-3` bohr (optimizer BFGS, `MAX_ITER 200`). These are stopping criteria and not accuracy bounds. The step-size sensitivity check never selects them; it can only trigger the revision sequence | A step is accepted only if the reported maximum residual force is at or below 4.5e-4 hartree/bohr, together with CP2K's other three criteria (B3 §3) |
| 2 | SCF energy convergence | ωB97X-D3 (E1): `EPS_SCF 1.0e-5`, the CP2K 2026.2 default [S0-cp2k-scf], set explicitly and used for energies and forces alike (B2 §4). GFN0-xTB (E2, E3): not applicable, because CP2K's internal GFN0 "has no SCC variables" [S0-cp2k-xtb], so no SCC iteration is performed. P2 in Psi4 1.11: `SCF E_CONVERGENCE 1.0e-8` and `D_CONVERGENCE 1.0e-8`, set explicitly for energies and gradients alike. The v1.11 driver would itself set 1e-6 for energies and 1e-8 for analytic gradients, but only when the user has not changed these options [S0-psi4-driver-util, lines 40–86], so explicit values are the effective ones (B2 §6). All are stopping criteria and not accuracy bounds on the converged energy or forces | A step is rejected if an SCF did not converge to the recorded value |
| 3 | Energy-sign criteria (E1, E5) | No budget and no physical threshold. Rule N6 is applied to direct composite-energy measurements at each actual Stage 2 configuration used in the sign. Event E1 is observed only when its Si–C bond part (row 4) and an N6-resolved energy decrease hold at the same accepted step. Step 0, an unavailable energy and an unresolved sign are handled as B3 §5 states. The geometric trigger T_A of B3 §5 controls the scan and never substitutes for this sign. Through E1, the sign also enters the checkpoint S comparison (row 11) | A sign is reported only under N6; otherwise it is indeterminate |
| 4 | Bond/no-bond cutoff per element pair (E1, E2, E3, E4, E6; the geometric triggers T_A and T_R of B3 §5) | Tabulation: `ase.data.covalent_radii` of ASE 3.29.0, which cites Cordero et al. 2008 [S0-ase-src-data, lines 436–442]: H 0.31 (line 447), C 0.76 (452), O 0.66 (454), Si 1.11 (460) and Ge 1.20 Å (478). Cutoff for a pair A–B: m·(r_A + r_B), with base multiple m = 1.20 and sensitivity multiples 1.10 and 1.30 | An observation counts as observed only if it holds at all three multiples; otherwise it is indeterminate |
| 5 | E3(i) proximity | `D-Ge1` to `D-Ca` at or below 2.00·(r_Ge + r_C) = 3.92 Å, the same covalent-radius rule with a declared multiple of 2.00. In the E3 compared at checkpoint S (B3 §5), this proximity, together with the connectivity condition, must persist over the declared minimum **Δd_min = 0.20 Å** of imposed d. That value is an `[AGENT]` declaration, not a physical threshold | A proximity claim only |
| 6 | E3(ii) radical character | Scheme: the Mulliken spin population printed by CP2K `DFT/PRINT/MULLIKEN` [S0-cp2k-mulliken] from the ωB97X-D3 sub-force_eval E1, the only hybrid-DFT density in the scheme. Sites: the pendent C2 (`D-Ca` + `D-Cb`, summed) and `D-Ge1`. Threshold: an absolute summed spin population of at least 0.50 on a site group. If the scheme does not produce spin populations for E1 inside `MIXED`, E3(ii) is reported indeterminate | A radical-character claim only, and only if the threshold is met on every accepted step in the range. It never supports E3(iii) |
| 7 | E3(iii) interaction and stabilization | **Retained INDETERMINATE by declaration under this scheme; no reference is computed.** Spike §8.6 requires the fragment reference "at the same z". In B3 the imposed drive value is d, the translation of H_M1. The reported quantity is D − z0, where D is the H_T-to-H_M1 separation. The EAOGe fragment contains the tool handle H_T, so separating it (for example by +10 Å along z) leaves d unchanged but changes the reported D, and so D − z0, by the same amount. No reference in this model keeps both d and D − z0 fixed while separating the fragments, so the same-z requirement cannot be met as the spike states it. The threshold that would have applied (−0.10 eV) is not used | E3(iii) is reported INDETERMINATE on every step. No stabilization claim is made. E3(i) and E3(ii) are unaffected |
| 8 | P2 cross-engine agreement | Budgets B_E = 1.0e-4 hartree for the energy difference and B_F = 1.0e-4 hartree/bohr per force component. These are declarations, not derived or validated uncertainties | N7: pass, fail or indeterminate per comparison. P2 is established only if every comparison passes. A common representation or regime that cannot be demonstrated is blocking |
| 9 | Finite-difference checks, constituent levels and composite coupled gradient | Budget B = 5.0e-4 hartree/bohr per gradient component. Steps h = 0.02 bohr, h/2 = 0.01 bohr and h/4 = 0.005 bohr. Regime interval for q: [3.0, 5.0]. The tested components are listed in [C7 §2](C7-VALIDATION-SET.md#2-components-tested-by-the-finite-difference-checks) | N5: PASS is required at every tested component of every validation configuration. The scheme is accepted for Stage 2 only if the composite check passes. FAIL returns the route to Stage 0; INDETERMINATE is blocking |
| 10 | Constraint projection | **N8 is BLOCKED pending definition.** N8 compares two recorded quantities: (i) the projected gradient that GEO_OPT uses, and (ii) the analytic composite gradient after the constraints are applied. The record that carries (i) in CP2K 2026.2 is not identified in the retrieved documentation (`UNVERIFIED`). For (ii), `FORCE_EVAL/PRINT/FORCES` has an `NDIGITS` keyword (default 8 [S0-cp2k-print-forces]), but the printed representation (numeric format, units as printed, rounding or truncation) is not established. The combined formatting allowance r = r_(i) + r_(ii) therefore cannot be defined for both records. The budget B_P = 1.0e-6 hartree/bohr is declared and kept | N8 is not run and has no outcome until both representations and r are defined from version-matched source, before Stage 1 begins (a prerequisite to starting Stage 1, through the revision sequence). Until then every consumer of N8 is blocked |
| 11 | Step-size sensitivity | No numeric tolerance. Steps 0.20 Å and 0.05 Å against the base 0.10 Å. The deterministic window W_b of [B3 §5](B3-DRIVE-PROTOCOL.md#5-checkpoints-declared-here-applied-in-stage-2) applies. It is anchored on the geometric triggers T_A and T_R, never on event E1, with the rules for early and missing triggers, short or terminated branches, endpoints and retraction eligibility. **Zero accepted steps:** if step 0 of A, or the first step of R, is not accepted, no J_b, anchor or window exists; the branch check and checkpoint S for that branch are INDETERMINATE (blocking); no sensitivity re-run is made; and no dependent branch starts (R is recorded as not started when A has no accepted step) | At checkpoint S, the window is released only if the ordered first occurrences of the inherited events E1, E2, E3 and E4 are identical across the three runs, each event judged under its full criterion in B3 §5: E1 with its N6-resolved energy sign (row 3), and E2 with its persistent Si–C bond and intact Si–Si bonds at the anchoring Si. E3 counts only where its pendent-state condition persists over Δd_min = 0.20 Å (row 5), and it is placed at the first step of that span; an isolated E3 hit is not an occurrence. A match of geometric lists alone never releases it, and neither does a match of isolated E3 hits. S is changed or INDETERMINATE, and quarantines from s_b onward as spike §8.5 defines, if any of these occurs: a changed order; a terminated re-run; a window of fewer than three accepted steps; or a compared event that is INDETERMINATE at any step of any run. Such an event can come from an indeterminate cutoff judgement, a missing energy or N6 value, an E1 sign that N6 cannot resolve, or an E3 whose persistence cannot be established inside the interval |

Which CP2K output records the projected gradient used by GEO_OPT, and therefore the recorded values that N8
compares, is `UNVERIFIED`. If no such record exists, N8 is indeterminate and blocking.

## 2. Numerical-convergence protocol

Every item here is declared in Stage 0, which runs no calculation. The calibration runs form Stage 1a. The checks
that consume them (Stage 1b) start only after those outputs are recorded.

**N1, refinement ladders.** Each ladder has three rungs. Rung 0 is production. Only numerical controls defined in
the version-matched documentation change along a ladder. The basis, core treatment, functional, dispersion form and
parameters, geometry, charge and multiplicity never change.

| Object | Rung 0 (production) | Rung 1 | Rung 2 |
|---|---|---|---|
| E1, ωB97X-D3 in CP2K (GAPW) | `EPS_SCF 1e-5`, `CUTOFF 600` Ry, `REL_CUTOFF 60` Ry, `EPS_DEFAULT 1e-10`, `EPS_SCHWARZ 1e-10`, `LEBEDEV_GRID 50`, `RADIAL_GRID 50`, D3 `EPS_CN 1e-6` and `R_CUTOFF 25` Å, cell margin 8 Å | `1e-6`, 800, 70, `1e-12`, `1e-12`, 80, 80, `1e-8`, 30 Å, 10 Å | `1e-7`, 1000, 80, `1e-14`, `1e-14`, 110, 110, `1e-10`, 35 Å, 12 Å |
| E2 and E3, GFN0-xTB in CP2K | `EPS_PAIRPOTENTIAL 1e-10`, `EPS_DEFAULT 1e-10`, cell margin 8 Å | `1e-12`, `1e-12`, 10 Å | `1e-14`, `1e-14`, 12 Å |
| Composite (aligned) | At composite rung k, E1, E2 and E3 each use rung k, and the frozen mapping, link and composition rules produce the actual coupled energy and mapped analytic gradient. Constituent and composite values are both recorded, and a constituent envelope never substitutes for a composite one | | |
| P2 in Psi4 1.11 | `SCF E_CONVERGENCE 1e-8`, `D_CONVERGENCE 1e-8` (set explicitly), grid 75 × 302, `INTS_TOLERANCE 1e-12` | `1e-9`, `1e-9`, 99 × 590, `1e-14` | `1e-10`, `1e-10`, 150 × 974, `1e-16` |
| P2 in CP2K | The E1 ladder | | |

The documented defaults are cited in B2 §4 and §6. Whether each engine accepts these exact grid sizes, or rounds
them to its nearest supported grid, is `UNVERIFIED`. The grid actually used is taken from the output and recorded.

**N2, same representation.** Compared values use:
- identical atoms and coordinates from the frozen files, by digest;
- charge 0; multiplicity 2 (unrestricted) for the combined configurations, and 1 (restricted) for P2;
- def2-TZVP, all-electron, subject to the normalization item in B2 §6;
- α = 1.0, β = −0.804272 and ω = 0.25;
- two-body D3 with zero damping, s6 = 1.0, sr6 = 1.281, s8 = 1.0, sr8 = 1.0 and α6 = 14.

**Electronic-state comparison rule (operational, frozen).** Two computed values A and B are treated as the same
electronic state only if all of the following hold. Values can differ by rung, repeat, displaced point or engine.
1. **Convergence.** Both records report SCF convergence to the declared criterion. For GFN0 constituents, which
   perform no SCC iteration, this item is replaced by a normal engine termination.
2. **Charge and multiplicity.** Both records show the declared charge and multiplicity: 0 and 2, unrestricted, for
   the combined configurations and S+L; 0 and 1, restricted, for P2. The numbers of α and β electrons printed by the
   engine are consistent with them.
3. **Spin populations (open-shell ωB97X-D3 records, E1 only).** For each declared site group (row 6: `D-Ca` + `D-Cb`,
   and `D-Ge1`), the summed Mulliken spin populations of A and B differ by at most 0.10 e, and the two values have
   the same sign whenever either magnitude is 0.10 e or more. This threshold is declared `[AGENT]`; it is a
   state-matching criterion, not an accuracy bound. The reference for a ladder or repeat set is the first
   production-rung repeat.
4. **Closed-shell P2.** Items 1 and 2 only, with the restricted reference in both engines.

**Missing diagnostic.** If a diagnostic required by items 1 to 3 is absent from either record, the pair does not
satisfy N2. Examples are a missing convergence flag, missing electron counts, or no Mulliken spin populations for E1
inside `MIXED`. The comparison is not used, and every check that consumes it (N3, N4, N5, N6, N7) is INDETERMINATE
and blocking for that object. It is never passed. A pair that fails items 1 to 3 on the recorded values is likewise
not used, and the difference is reported as a change of electronic state, not as noise.

**N3, energy calibration (Stage 1a).**
- **Coverage.** On each validation configuration, every constituent energy (E1, E2, E3) and the actual composite
  energy are computed at every rung. The P2 energy is computed at every rung in both engines.
- **Repeats.** Each production rung is repeated three times from different initial guesses:
  - CP2K: `SCF_GUESS ATOMIC`, `CORE` and `EHT` [S0-cp2k-scf];
  - Psi4: `GUESS SAD` (the production run), `CORE` and `GWH` [S0-psi4-read-options, line 1505], every run with
    `DF_SCF_GUESS false`, and the SAD repeat with `SAD_SCF_TYPE DIRECT`, so that the Python driver requests no
    fitting basis. Whether the compiled SCF and gradient steps use one is `UNVERIFIED` and is a prerequisite to
    starting Stage 1 (B2 §6 and §8).

  No random guess is used, so every repeat's random seed is recorded as "none". For GFN0, which performs no SCC
  iteration, the repeats test run-to-run reproducibility only.
- **Envelope.** ε_X is the largest absolute difference among X's production-rung repeats and between the production
  rung and each tighter rung.
- **Regime.** A convergence regime is shown for X when the magnitude of the difference between successive rungs does
  not increase along the ladder. Without it, X is unusable, and every check that consumes it is blocked.

**N4, force calibration (Stage 1a).** The same direct procedure applies to every analytic force component of each
constituent, and to every component of the actual composite mapped gradient, including the link-host and
chain-rule terms. It gives an object-specific envelope φ_X. A constituent force envelope is never used for the
composite gradient.

**N5, finite-difference checks (Stage 1b).** For a tested component of object X,
D(s) = [E_X(x + s) − E_X(x − s)]/(2s) at s = 0.02, 0.01 and 0.005 bohr, with every displaced point satisfying N2.
- **Richardson estimate and truncation.** R = [4D(h/2) − D(h)]/3 and T = |D(h) − D(h/2)|/3.
- **Noise.** N = 3ε/h. The regime is indicated when q = [D(h) − D(h/2)]/[D(h/2) − D(h/4)] lies in [3.0, 5.0] and
  |D(h/2) − D(h/4)| exceeds 6ε/h.
- **Allowance.** U = T + N + φ, with G the analytic gradient component.
- **Rule:**
  - PASS if the regime is indicated and |G − R| + U ≤ B = 5.0e-4 hartree/bohr.
  - FAIL if the regime is indicated and |G − R| − U > B.
  - INDETERMINATE in every other case, including a vanishing leading s² coefficient, an unresolved denominator or a
    ratio that indicates a different leading order.

A constituent check uses that constituent's direct ε and φ; the composite check uses the composite's.

**N6, energy signs (E1, E5).** Each actual Stage 2 configuration a or b used in an energy-sign claim receives three
direct composite-energy production-rung repeats and one tighter aligned composite rung (rung 1). ε_a or ε_b follows
N3. The sign of the composite ΔE is reported only if |ΔE| > ε_a + ε_b; otherwise it is indeterminate. No
constituent envelope, validation-configuration transfer or budget is used.

**N7, P2 agreement.** The model chemistry is identical in both engines (N2). The periodic engine uses the declared
isolated-molecule treatment (B2 §5; C7 §3).
- **Energy.** PASS if |ΔE| + ε_1 + ε_2 ≤ B_E = 1.0e-4 hartree; FAIL if |ΔE| − (ε_1 + ε_2) > B_E; otherwise
  INDETERMINATE.
- **Forces.** Each force component is judged the same way, with φ_1, φ_2 and B_F = 1.0e-4 hartree/bohr.
- **Outcome.** P2 is established only if every comparison passes. A pass establishes internal consistency only: two
  engines that share a definitional error would still agree.

**N8, constraint projection. BLOCKED pending definition (row 10).** The rule below is frozen, but it cannot be
applied until the representations of both compared records, and the combined formatting allowance r, are defined
from version-matched CP2K source:
- **Fixed atoms.** Fixed-atom coordinates must be identical in the recorded output before and after a constrained
  step, and the components the constraints remove must be zero in the recorded projected gradient; otherwise the
  check fails.
- **Retained components.** These are compared with the analytic gradient after the constraints are applied. With
  difference Δ, r = r_(i) + r_(ii) (undefined until row 10 is resolved) and B_P = 1.0e-6 hartree/bohr: PASS if
  |Δ| + r ≤ B_P; FAIL if |Δ| − r > B_P; otherwise INDETERMINATE, which is blocking.

While r is undefined, N8 has no outcome, and C6 (which requires N8) cannot be met.

Where a quantity cannot be resolved, the outcome is INDETERMINATE and blocking, never a pass. That covers a missing
regime or common representation, a noise-limited difference and an unresolvable recorded precision.

## 3. Revision sequence (binding)

After freezing, a value or definition changes only through this sequence (spike §8.6):

1. A recorded reason that does not refer to agreement with the paper. A validation tolerance or budget is never
   relaxed to turn a recorded failure or indeterminate result into a pass. A demonstrated error in its recorded
   basis is corrected with the failure retained.
2. Fresh approval by the same roles as the original selection.
3. Revalidation of everything the old value governed. Every Stage 1 check and every accepted step whose outcome used
   it is repeated. A changed per-step criterion invalidates the rest of the branch, which is re-run from its first
   step together with its sensitivity segments.
4. Superseded results are retained, and both outcomes are reported.

- **Stage 2 quarantine.** A quarantine at a Stage 2 checkpoint (B3 §5; spike §8.5) is the declared trigger on which
  the force criterion, the production settings or the z step may be tightened through this sequence.
- **Stage 1 failure.** A frozen definition that fails in Stage 1, such as the coupling route failing its
  demonstration (C2 §5), returns to Stage 0 under the same sequence.
- **Diagnostic runs.** Runs under spike §8.8 are additional and never replace a frozen-setup result.
