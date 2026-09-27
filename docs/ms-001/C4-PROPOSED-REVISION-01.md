# C4 proposed revision 01: the definition of N8

Date: 2026-09-27. Status: **PROPOSED. Options for a human decision under C4 §3. Not applied and not approved.**

This document sets out options for a decision on N8 under the binding revision sequence of
[C4](C4-TOLERANCES-AND-CONVERGENCE.md) ([C4 §3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding)). It
follows from the findings of the [source resolution record](SOURCE-RESOLUTION.md) of the same date. It is written by
the method author of this package, and its content is `[AGENT]`.

What it does not do:
- **C4 is unchanged.** C4 stays byte-identical at SHA256
  `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`, as approved by a person on 2026-09-27
  ([approval record](C4-HUMAN-APPROVAL.md)). Nothing here is in force.
- **Only step 1 of the sequence is taken.** This document records a reason. Fresh approval by the same roles as the
  original selection (step 2) has not occurred, and revalidation (step 3) has not occurred. Nothing that N8 governs
  has run, so no result has yet been governed by the old definition.
- **No budget is relaxed, and N8 has no outcome.** No tolerance, budget or rule is relaxed to turn a recorded failure
  or indeterminate result into a pass. N8 has not been run, and this document gives it no outcome.
- **No option is chosen.** The final design may stay pending.
- **No authorization.** Stage 1 remains BLOCKED and is not authorized.

## 1. Recorded reason (C4 §3, step 1)

Version-matched CP2K 2026.2 source ([source resolution §7](SOURCE-RESOLUTION.md#7-n8-the-two-compared-representations))
establishes, under the declared settings:
- **No direct record.** CP2K writes no separate, direct record of the gradient array that `GEO_OPT` uses.
- **One array.** In memory that gradient is the exact negation of the constrained composite force array. The printed
  force records are decimal renderings of that array.
- **Rounding.** The printed digits are fixed by source. The rounding of formatted output is left to the compiler and
  run-time library.

C4 row 10 does not say whether a negated force record can serve as N8's record (i) (Section 2). Under either reading,
source reading alone cannot give N8 an outcome:
- **Under reading A.** Records exist, but the allowance r is not defined from version-matched source, and the
  retained-component comparison would compare renderings of one array.
- **Under reading B.** Record (i) does not exist.

Row 10 makes the definition of both representations and r a prerequisite to starting Stage 1 "through the revision
sequence". A decision under §3 is therefore needed before N8 can have an outcome. Its content is not fixed by the
source and is set out as options in Section 4.

The reason does not refer to agreement with the benchmark paper, and it corrects no recorded result.

## 2. The definitional ambiguity

Row 10, third column, states:

> N8 compares two recorded quantities: (i) the projected gradient that GEO_OPT uses, and (ii) the analytic composite gradient after the constraints are applied.

The paragraph after the tolerance table states:

> Which CP2K output records the projected gradient used by GEO_OPT, and therefore the recorded values that N8 compares, is `UNVERIFIED`. If no such record exists, N8 is indeterminate and blocking.

C4 states no requirement that the two records be independent, and none that record (i) be written by the optimizer.

**Reading A: a negated force record can carry (i).**
- **The claim.** By source the optimizer's gradient is the exact negation of the constrained force array in memory.
  A rendering of that array, negated, therefore records the gradient the optimizer uses, to within formatting.
- **Records.** Both (i) and (ii) have records, and "if no such record exists" does not apply.
- **For r.** r must bound the difference between two renderings of one array, and the source does not fix the
  rounding. So r is not defined from version-matched source, and row 10 keeps N8 from being run.
- **For N8's value as a check.** The retained-component difference reflects formatting only, and it is zero by
  construction if one record serves for both. A fault in how the constraint acts on retained components would appear
  identically in both records, so the comparison could not detect it. The fixed-atom clause keeps its value.

**Reading B: record (i) must be the optimizer's own record of the gradient.**
- **Records.** Record (i) does not exist, so the paragraph applies, and N8 is classed as indeterminate and blocking.
  That class is a status of the definition, not an executed outcome.
- **For r.** r_(i) has nothing to bound.
- **For N8's value as a check.** N8 cannot be applied at all.

**Proposed reading (`[AGENT]`).** Reading A is proposed as the literal reading, because C4 states no independence
requirement and the source establishes the exact in-memory relation. The proposal is made together with its
consequence: under reading A, the retained-component comparison would carry no information about the projection. The
choice of reading belongs to the approval roles.

## 3. Audit of the affected clauses

Each quotation below is exact apart from line wrapping. Table cells are quoted without their column separators. The
audit covers every clause that the findings touch, including those that need no change.

**A1. Row 10 of the tolerance table, third column ("Declared value or cited default").**

> **N8 is BLOCKED pending definition.** N8 compares two recorded quantities: (i) the projected gradient that GEO_OPT uses, and (ii) the analytic composite gradient after the constraints are applied. The record that carries (i) in CP2K 2026.2 is not identified in the retrieved documentation (`UNVERIFIED`). For (ii), `FORCE_EVAL/PRINT/FORCES` has an `NDIGITS` keyword (default 8 [S0-cp2k-print-forces]), but the printed representation (numeric format, units as printed, rounding or truncation) is not established. The combined formatting allowance r = r_(i) + r_(ii) therefore cannot be defined for both records. The budget B_P = 1.0e-6 hartree/bohr is declared and kept

- **Finding.**
  - No separate, direct record of the optimizer's gradient exists. Whether a force record serves as (i) depends on
    the reading (Section 2).
  - (ii) is printed as forces, not gradients: in `ES(n+7).n` in `FORCE_UNIT` to standard output, or in `F(n+6).n`
    in a.u. to a named file.
  - The rounding is left to the compiler and run-time library.
- **Change needed.** A change is needed for N8 to have an outcome under either reading. Its content is a decision
  (Section 4).

**A2. Row 10, fourth column ("Pass/fail rule").**

> N8 is not run and has no outcome until both representations and r are defined from version-matched source, before Stage 1 begins (a prerequisite to starting Stage 1, through the revision sequence). Until then every consumer of N8 is blocked

- **Finding.**
  - Under reading A the representations are characterized from source, but r cannot be defined from it.
  - Under reading B record (i) does not exist.
  - Under both, the condition is not met by source reading, and N8 is not run and has no outcome.
- **Change needed.** As for A1.

**A3. The paragraph that follows the tolerance table** (after row 11).

> Which CP2K output records the projected gradient used by GEO_OPT, and therefore the recorded values that N8 compares, is `UNVERIFIED`. If no such record exists, N8 is indeterminate and blocking.

- **Finding.**
  - Under reading B its condition holds, and N8 is classed as indeterminate and blocking as a status of the
    definition.
  - Under reading A its condition does not hold.
  - The `UNVERIFIED` question is answered by the source fact above. The reading remains a question of definition.
- **Change needed.** As for A1.

**A4. N8 in §2, its heading sentence and rule.**

> **N8, constraint projection. BLOCKED pending definition (row 10).** The rule below is frozen, but it cannot be applied until the representations of both compared records, and the combined formatting allowance r, are defined from version-matched CP2K source:

> - **Fixed atoms.** Fixed-atom coordinates must be identical in the recorded output before and after a constrained step, and the components the constraints remove must be zero in the recorded projected gradient; otherwise the check fails.

> - **Retained components.** These are compared with the analytic gradient after the constraints are applied. With difference Δ, r = r_(i) + r_(ii) (undefined until row 10 is resolved) and B_P = 1.0e-6 hartree/bohr: PASS if |Δ| + r ≤ B_P; FAIL if |Δ| − r > B_P; otherwise INDETERMINATE, which is blocking.

- **Finding.**
  - *Fixed atoms.* The clause could be applied to a force record and to the optimizer's coordinate records. That
    rests on a premise not established from CP2K source: that a component set to exactly 0.0 is rendered as zero.
  - *Retained components, reading A.* The comparison could be made but would carry no information about the
    projection.
  - *Retained components, reading B.* No record (i) exists.
- **Change needed.** As for A1.

**A5. The sentence after the N8 rule.**

> While r is undefined, N8 has no outcome, and C6 (which requires N8) cannot be met.

- **Finding.** Under both readings r cannot be defined from version-matched source. As long as this rule and the
  declared stock CP2K 2026.2 route stay as they are, N8 has no outcome and C6 cannot be met. A different route, such
  as the out-of-scope instrumentation of option O4, could change what can be recorded.
- **Change needed.** As for A1.

**A6. The closing paragraph of §2.**

> Where a quantity cannot be resolved, the outcome is INDETERMINATE and blocking, never a pass. That covers a missing regime or common representation, a noise-limited difference and an unresolvable recorded precision.

- **Finding.** This paragraph is consistent with every option below and governs a missing or unparseable record.
- **Change needed.** No.

**A7. The N2 normalization qualification.**

> - def2-TZVP, all-electron, subject to the normalization item in B2 §6;

- **Finding.** CP2K's normalization is established from source. The Psi4 integral path is established only at Libint
  v2.8.1, which no build is shown to link (source resolution §6).
- **Change needed.** No. The qualification remains correct and continues to govern N2.

**A8. The N3 compiled-basis prerequisite** (the Psi4 repeats of N3).

> - Psi4: `GUESS SAD` (the production run), `CORE` and `GWH` [S0-psi4-read-options, line 1505], every run with `DF_SCF_GUESS false`, and the SAD repeat with `SAD_SCF_TYPE DIRECT`, so that the Python driver requests no fitting basis. Whether the compiled SCF and gradient steps use one is `UNVERIFIED` and is a prerequisite to starting Stage 1 (B2 §6 and §8).

- **Finding.** The Psi4 v1.11 tagged source constructs no fitting basis in the compiled steps under these settings.
  The installed binary's build provenance and runtime conformance are not established (source resolution §8).
- **Change needed.** No change to the definition. The sentence is a status statement within approved bytes. The
  source resolution record supersedes it for status; the statement is not edited.

**A9. §3, the revision sequence, step 1.**

> 1. A recorded reason that does not refer to agreement with the paper. A validation tolerance or budget is never relaxed to turn a recorded failure or indeterminate result into a pass. A demonstrated error in its recorded basis is corrected with the failure retained.

- **Finding.** This document follows step 1. Steps 2 and 3 are outstanding. Options O1 and O2 change what N8 checks.
  That is a change of coverage, stated for decision, and not a relaxation applied to any recorded result.
- **Change needed.** No change to §3.

**A10. Row 1, the pass/fail rule on the reported maximum residual force.** Row 1 accepts a step on the aggregate
maximum residual force that `GEO_OPT` reports. By source that aggregate is computed over the same in-memory gradient.
- **Change needed.** No. It is not a component-wise record and is not offered as one.

## 4. Options for the decision

The options are listed for the roles of the original selection. The method author proposes; the independent reviewer
checks; a person decides. None is preferred by this document except where marked.

| Option | What changes | What N8 then checks | What it gives up or needs |
|---|---|---|---|
| O0. No change | Nothing | Nothing. N8 stays BLOCKED, C6 cannot be met, and the Stage 1 prerequisite of row 10 stays unmet | Progress on N8 and C6 |
| O1. Reading A with a declared r | Records (i) and (ii) are declared as renderings of the constrained force array, and an allowance r is declared and justified through §3, for example one unit in the last printed place with its unit and exponent treatment defined | The fixed-atom clause, and a retained-component comparison that can be run | The retained-component comparison carries no information about the projection. r rests on a declared, not a source-defined, rounding bound |
| O2. Fixed-atom checks only (candidate text in Section 5) | The retained-component comparison is removed. Records are declared for the fixed-atom clause | Zero fixed components in the force record, and unchanged fixed-atom coordinates | Retained-component coverage at run time. That the constraint leaves retained components unchanged would rest on source reading of `fix_atom_control` alone. This trade-off is for decision, not a conclusion |
| O3. Reconstruction within one evaluation | (ii) is taken as the unconstrained composite forces reconstructed from the sub-force_eval force records of the same evaluation, through the frozen mapping and the `GENMIX` derivative | The full rule, with an independent second record | The derivative values used at run time are not printed, and the link-atom force mapping is an undocumented route capability ([C2 §5](C2-COUPLING-ROUTE.md#5-what-the-official-documentation-does-not-establish), items 1 and 3). It stays BLOCKED until those Stage 1 dependencies are settled, and it needs an allowance for two records and the reconstruction |
| O4. Instrumented build (outside this task's scope) | A separately authorized code change records the optimizer's gradient vector and the composite force array before the constraint, with the projection declared prospectively and full provenance of the changed code | The full rule, with direct records of both quantities | A code change, its own authorization, review and provenance. It departs from the stock CP2K 2026.2 route. No instrumentation, code change or engine run is authorized here |

A comparison against a separate evaluation of the same geometry without constraints is not listed. Its difference
would include SCF convergence noise between two evaluations, which B_P does not bound.

## 5. Candidate text for option O2

This text is a candidate only. It applies if O2 is chosen and steps 2 and 3 are completed. The number of printed
digits n is left to be declared with the approval.

**P1. Row 10, third column.**

> **N8 checks the fixed-atom constraint on the records that exist.** In CP2K 2026.2 the gradient that GEO_OPT uses is, by source, the exact negation of the constrained composite force array in memory, and no separate record of it is written. N8 uses the constrained-force record of the top-level `MIXED` force_eval, `FORCE_EVAL/PRINT/FORCES` written to standard output in `ES(n+7).n` with `FORCE_UNIT hartree/bohr` and n declared, which is a decimal rendering of that array, and the optimizer's coordinate records, `MOTION/PRINT/TRAJECTORY` in its default format. That the constraint leaves the retained components unchanged is source-defined behaviour and is not tested at run time. The budget B_P = 1.0e-6 hartree/bohr is not used by this rule.

**P2. Row 10, fourth column.**

> N8 is applied at every accepted step: PASS if both of its checks pass, FAIL if either fails, otherwise INDETERMINATE, which is blocking.

**P3. The paragraph after the tolerance table.**

> In CP2K 2026.2 no output records the optimizer's gradient array directly; it is, by source, the exact negation of the constrained composite force array in memory, which `FORCE_EVAL/PRINT/FORCES` renders in decimal form (source resolution record, §7). N8 is defined on that rendering and on the coordinate records.

**P4. N8 in §2.**

> **N8, constraint projection.** Applied at every accepted step:
> - **Fixed components.** In the constrained-force record of row 10, every component of every fixed atom must print with a zero significand. A non-zero significand fails the check.
> - **Fixed coordinates.** The coordinates of every fixed atom must print identically in the coordinate records before and after the step. A difference fails the check. The check resolves differences only down to the printed precision.
> - **Missing or unreadable records.** A record that is missing, unparseable, non-finite or overflowed makes N8 INDETERMINATE, which is blocking.
>
> No retained-component comparison is made.

**P5. The sentence after the N8 rule.**

> C6 requires N8 to PASS on every accepted step of the validation configurations and branches it covers.

**Premises that the candidate does not establish.** P4 relies on how Fortran formatted output renders values: a
component that is exactly 0.0 prints with a zero significand, a non-zero component does not, and equal coordinates
print identically. None of these is established from CP2K source. No compiled formatting test was run. Their
confirmation belongs to Stage 1 under its own authorization.

**Consequential record.** B3 §3 refers constraint projection to "N8 (C4 §3)". N8 is in C4 §2. B3 is a frozen record.
A matching editorial correction of B3 would follow the same sequence, and none is made here.

## 6. Status

| Step of C4 §3 | State |
|---|---|
| 1. Recorded reason | Recorded here, 2026-09-27, with the ambiguity of Section 2 and the options of Section 4 |
| 2. Fresh approval by the same roles | Not occurred. No option is chosen |
| 3. Revalidation of everything the old value governed | Not occurred. Nothing governed by N8 has run |
| 4. Retention of superseded results | Not applicable. No N8 result exists |

Until step 2 is completed, C4 as approved on 2026-09-27 is the definition in force. Under it, N8 is BLOCKED and has
not been run. Stage 1 remains BLOCKED and is not authorized.
