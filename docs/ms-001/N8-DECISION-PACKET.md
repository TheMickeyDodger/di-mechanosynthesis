# N8 decision packet

Date: 2026-09-27. MS-001 scope option B, before Stage 1. Status: **decision support for a person. One option is
recommended as an `[AGENT]` proposal. No option is chosen, approved or applied.**

This packet turns the options of [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md) into a decision that a
person can take on exact terms. It recommends one option, states what that option gains and loses, gives exact
candidate text, and maps every frozen record that a future, authorized application would have to change.

What this packet is not:
- **Not the decision.** How N8 is defined is a method-author decision. It is reserved to the roles of the original
  selection under [C4 §3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding): the method author proposes,
  the independent reviewer checks, and a person decides. Reviewing, accepting or publishing this packet as a
  document is not that decision and cannot stand in for step 2 of the sequence. No source fact decides it either.
- **Not a change.** [C4](C4-TOLERANCES-AND-CONVERGENCE.md) stays byte-identical at SHA256
  `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`. Every record bound in the
  [freeze record](STAGE0-FREEZE-RECORD.md#2-frozen-artifacts) is unchanged, and so is the freeze record itself. Until a
  person decides otherwise, C4 as approved on 2026-09-27 is the definition in force, and under it N8 is BLOCKED.
- **Not an outcome.** N8 has not been run and has no outcome. Nothing here reports a force, a coordinate or a
  gradient.
- **Not authorization.** Stage 1 remains BLOCKED and is not authorized. This packet authorizes no calculation,
  installation, instrumentation or engine run.

## 1. Source facts and decisions kept apart

**Source facts.** They are read from the CP2K 2026.2 release archive, whose identity is given in the
[source resolution record, §2](SOURCE-RESOLUTION.md#2-method-and-source-identity). Each file is identified by SHA256 in
the [pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md). Each fact states what the source text defines: `[LIT]`
provenance, with no chemistry class and nothing about a build or a run.

| # | Fact | Locator (CP2K 2026.2) |
|---|---|---|
| S1 | In each evaluation the top-level force_eval runs the fixed-atom control after the sub-force_evals (`force_env_methods.F` 361–369). For `COMPONENTS_TO_FIX XYZ` that control copies each locally held particle force into a scratch array set to `0.0_dp` (`constraint_fxd.F` 130–147). It sets the three components of every fixed atom to `0.0_dp` (221–225), sums the array over MPI ranks and writes it back to the particle forces (232–242). Components of atoms that are not fixed are copied without change | `src/force_env_methods.F`; `src/constraint_fxd.F` |
| S2 | The optimizer's gradient is the particle force array packed with scale factor −1. In memory it is therefore the exact negation of the constrained array F_c. No routine that receives the gradient writes its components | [Source resolution §7](SOURCE-RESOLUTION.md#7-n8-the-two-compared-representations), steps 5 and 6 |
| S3 | `FORCE_EVAL/PRINT/FORCES` of the top-level force_eval writes F_c under the label `Atomic` (`force_env_methods.F` 410–442). The print key is created at high print level with default file name `__STD_OUT__`, and it has `NDIGITS` and `FORCE_UNIT` keywords (`input_cp2k_force_eval.F` 322–335). Written to the main output, each row carries the atom index (`force_env_utils.F` 509–513) and three components plus the norm in `ES(n+7).n` (486–490), after multiplication by the conversion factor of `FORCE_UNIT` (503). The header names the unit (504–506). n is `NDIGITS` clamped to 1…20 (482). The record carries no iteration number | `src/force_env_methods.F`; `src/input_cp2k_force_eval.F`; `src/force_env_utils.F` |
| S4 | Written to a named file, the same record uses `F(n+6).n` in atomic units, with no conversion | `src/force_env_utils.F` 574–582, 590–606 |
| S5 | `MOTION/PRINT/TRAJECTORY` is created at low print level (`input_cp2k_motion_print.F` 73–75), and its `FORMAT` keyword defaults to `XMOL` (319–323). Its unit is read from its `UNIT` keyword (`motion_utils.F` 380–382); this record does not establish that keyword's default. In `XMOL` format each frame's title reads ` i = ` followed by the iteration number in `I8` and the energy (`motion_utils.F` 419–423). Each atom line gives the element symbol and three coordinates in `F20.10` after multiplication by the unit factor, in particle order, with no atom index (`particle_methods.F` 269–295) | `src/input_cp2k_motion_print.F`; `src/motion_utils.F`; `src/particle_methods.F` |
| S6 | Print keys have an `EACH` subsection, `ADD_LAST` and `FILENAME` keywords, and the file name `__STD_OUT__` selects the main output | `src/input/cp_output_handling.F` 221, 262, 292–294, 766–772 |
| S7 | Within `GEO_OPT` BFGS, the initial evaluation (`bfgs_optimizer.F` 290) is followed by the iteration-0 cycle report (304) from `gopt_f_io_init`, which writes no trajectory frame (`gopt_f_methods.F` 176–250). Each later iteration evaluates at the new geometry (`bfgs_optimizer.F` 409–410) and then calls `gopt_f_io` (427–428). That routine calls `geo_opt_io` and then writes the cycle report (`gopt_f_methods.F` 321–336). `geo_opt_io` writes the frame for that iteration through `write_geo_traj` (1048–1088, the call at 1072), which writes the `TRAJECTORY` print key (920–941). Every cycle report prints `OPT| Step number` with the iteration number (482–486). Convergence is reported by the banner `GEOMETRY OPTIMIZATION COMPLETED` (769–774). On convergence the counter is incremented and the energy is reevaluated at the minimum (banner at 899–900). That call passes the energy output but no gradient (902–903), and a frame is written with the incremented number (904), with no further cycle report | `src/motion/bfgs_optimizer.F`; `src/motion/gopt_f_methods.F` |
| S7a | The final reevaluation computes no forces and prints no force block. For minimization, `cp_eval_at` requests forces only when its gradient argument is present (`gopt_f77_methods.F` 131–135). The force environment takes that request as its `calculate_forces` flag (`force_env_methods.F` 260), and it writes the `Atomic` force block only when the flag is true (411–413 and 439). The initial and per-iteration evaluations pass the gradient (`bfgs_optimizer.F` 290, 409–410), so they print a force block when the print key is on | `src/motion/gopt_f77_methods.F`; `src/force_env_methods.F`; `src/motion/bfgs_optimizer.F` |
| S8 | How a value is rounded to the printed digits is left to the compiler and run-time library. CP2K source fixes the digits but not the rounding | [Source resolution §7](SOURCE-RESOLUTION.md#7-n8-the-two-compared-representations), "Rounding" |

**Project inferences from these facts.** Each can be checked against the cited lines.
- **One array, one rendering.** A stock force record is a rendering of F_c. A second stock record of the same
  evaluation is a second rendering of the same array. **No stock rendering carries information about how the
  constraint acts on the retained components.**
- **No starting frame.** In the reading of S7, `GEO_OPT` writes no trajectory frame for its starting geometry. A
  comparison between frames can therefore not see the first optimizer move. The reference for fixed coordinates has
  to be the run's input coordinates.
- **What a printed value can show.** Equality at printed precision does not prove equality in memory, because
  distinct values can print identically and the rounding is not fixed by source (S8). A printed difference between
  two renderings of values produced in the same way does indicate a difference. No threshold is claimed below which
  every change would be invisible: a change of any size can cross a rounding boundary and alter the last printed
  digit.
- **What `ES` editing shows.** Under the Fortran definition of `ES` editing a finite non-zero value is printed with a
  non-zero significand, because the exponent absorbs the magnitude. A zero significand therefore shows, at most,
  that the value printed as zero. Whether a given build conforms is a run-time property (S8). `F` editing gives no
  such assurance, because an `F(n+6).n` field prints small values as zero.

**Decisions that source cannot make.** Each needs a person under C4 §3:
- which option to adopt, and so whether N8 keeps a retained-component comparison;
- which records N8 uses, with their digits, units and selectors;
- which runs and which evaluations N8 is applied to;
- how iterations, identity and fixed-set membership are established;
- how record integrity is judged, and how FAIL and INDETERMINATE combine.

## 2. Options and recommendation

The options are those of [C4-PROPOSED-REVISION-01.md §4](C4-PROPOSED-REVISION-01.md#4-options-for-the-decision),
where they are described in full.

| Option | N8 can have an outcome on the stock CP2K 2026.2 route | Run-time coverage of the fixed-atom clause | Run-time coverage of retained components | Additional authorization or design needed |
|---|---|---|---|---|
| O0, no change | No | None | None | None, but N8 and C6 stay unmeetable |
| O1, reading A with a declared r | Yes, once r is declared | Yes | Nominal only: both records render F_c, so the difference reflects formatting | A declared r, justified without a source-defined rounding bound |
| O2, fixed-atom checks only | Yes, subject to the Stage 1 observations of Section 5 | Yes | None, stated as a loss | None beyond the decision and the Stage 1 observations of Section 5 |
| O3, reconstruction in one evaluation | Not before Stage 1 route dependencies are settled | Yes | Yes, against a reconstructed unconstrained composite | C2 §5 items 1 and 3 settled in Stage 1; an allowance for two records and the reconstruction |
| O4, instrumented build | Yes, on a changed build | Yes | Yes, with direct records of both quantities | A code change with its own authorization, review and provenance; departs from the stock route |

**Recommendation (`[AGENT]`): O2, fixed-atom checks only.** The reasons:
1. **It gives up no coverage the stock route could provide.** On the stock route every retained-component comparison
   compares renderings of one array (S2, S3). O1 would keep a comparison that cannot detect a projection error, and
   it would rest on a declared rounding bound where CP2K source defines none (S8). O2 drops that comparison and says
   so.
2. **It needs no allowance r.** Its tests are a zero-significand test on `ES` fields and a character-identity test
   against declared input strings. Both are stated as tests of printed values.
3. **O3 is not available before Stage 1.** It depends on route capabilities that only Stage 1 can settle.
4. **O4 departs from the declared stock route.** It needs a code change and an authorization outside this decision.
   It remains available later, as a separate proposal, if run-time retained-component coverage is judged necessary.
5. **O0 leaves C6 unmeetable** on the declared route.

The recommendation is a proposal. A person may choose any option, including O0, or ask for a different one.

## 3. What O2 gains and loses

**Gained.**
- N8 can have an outcome on the stock route, once the Stage 1 observations of Section 5 are made, without an
  undefined allowance.
- The fixed-atom clause of the frozen rule is kept in substance and made exact. Every evaluation's fixed components
  are tested at every force-bearing evaluation, on the record whose format keeps non-zero values non-zero. Every
  frame's fixed coordinates are tested against the run's input, so the first optimizer move and the final frame are
  covered.
- Iteration association, completeness, identity binding, record integrity and outcome precedence are declared before
  any run.

**Lost, stated for the decision.**
- **Retained-component coverage at run time.** That the constraint leaves every retained component unchanged would
  rest on the source reading of `fix_atom_control` alone (S1). No run-time record would test it. N8 would not detect
  a fault in how a build applies the constraint to retained components. Such a fault could show only indirectly,
  through other checks, and none of them is designed for it.
- **The budget B_P** = 1.0e-6 hartree/bohr would no longer be used by N8. It is not relaxed: no recorded result
  exists, and N8 governs nothing that has run. The change is a change of coverage, stated for decision.
- **Printed values, not values in memory.**
  - A fixed component that prints with a zero significand has printed as zero. Given a conforming `ES` formatter,
    that is consistent only with a zero value (Section 1).
  - Fixed coordinates that print identically to their input strings are equal at the printed precision of
    `F20.10` ångström. That does not prove that they are equal in memory.
  - **This is the fixed-coordinate precision limit.** It limits what the printed output can evidence. It is not a
    statement about which changes can occur.

## 4. Exact candidate text for O2

The texts below would replace the clauses named in Section 6.1. Each is a candidate only. It takes effect only if a
person chooses O2 and the rest of the C4 §3 sequence is completed.

**C1. Row 10, third column** (replacing the current cell):

> **N8 checks the fixed-atom constraint on the records that exist.** In CP2K 2026.2 the gradient that GEO_OPT uses is, by source, the exact negation of the constrained composite force array in memory, and no separate record of it is written. N8 uses four records of each run it covers. (a) The force record: `FORCE_EVAL/PRINT/FORCES` of the top-level `MIXED` force_eval, switched on, with `FILENAME __STD_OUT__`, `NDIGITS 8`, `FORCE_UNIT hartree/bohr` and `EACH/GEO_OPT 1`, so that every component is printed in `ES15.8` in the main output; `PRINT/FORCES` is not enabled in any sub-force_eval. (b) The coordinate record: `MOTION/PRINT/TRAJECTORY`, switched on, with `FORMAT XMOL`, `UNIT angstrom` and `EACH/GEO_OPT 1`, so that every coordinate is printed in `F20.10`. (c) The iteration record: the optimizer's `OPT| Step number` reports in the main output. (d) The input record: the run's retained input coordinates, written in ångström with exactly ten decimal places, in the atom order that every frozen combined file shares, with the `atom_id` of every atom in the run's identity sidecar (C3, F4). That the constraint leaves the retained components unchanged is source-defined behaviour and is not tested at run time. The budget B_P = 1.0e-6 hartree/bohr is not used by N8.

**C2. Row 10, fourth column** (replacing the current cell):

> N8 is applied to the constrained GEO_OPT runs of C7 §2: one run from each of V1, V2 and V3, with the fixed sets H_M1 and H_T of B3 §1 and the settings of B3 §3. The outcome of a run is FAIL if any check of the §2 rule fails on a judged record; otherwise INDETERMINATE if any part of the run is INDETERMINATE; otherwise PASS. INDETERMINATE is blocking.

**C3. The paragraph after the tolerance table** (replacing the current paragraph):

> In CP2K 2026.2 no output records the optimizer's gradient array directly. By source it is the exact negation of the constrained composite force array in memory, which `FORCE_EVAL/PRINT/FORCES` renders in decimal form (source resolution record, §7). N8 is defined on that rendering and on the other records of row 10, and it compares no two records of the gradient.

**C4. N8 in §2** (replacing the heading sentence, both bullets and the sentence after the rule):

> **N8, constraint projection: fixed-atom checks.** Applied to each run named in row 10, on the records of row 10.
> - **Iterations.** The `OPT| Step number` reports define the run's iterations. Their numbers must run 0, 1, …, K without gap or repetition, with K ≥ 1. The run must have reported convergence and ended normally; otherwise the run is INDETERMINATE.
>   - *Force-bearing evaluations.* A top-level `Atomic` force block that precedes the report of iteration 0 belongs to iteration 0. One that lies between the reports of iterations k − 1 and k belongs to iteration k. Every iteration 0 to K must have at least one force block. More than one is allowed, and every block is judged.
>   - *The final reevaluation.* The energy-only reevaluation after convergence prints no force block. None is required after the report of K, and one that appears there makes the run INDETERMINATE.
>   - *Coordinate frames.* A frame belongs to the iteration named in its title. Exactly one frame is required for each iteration 1 to K, exactly one for K + 1, the frame written after the final reevaluation, and none for iteration 0.
>   - *Completeness.* A missing force block for iterations 0 to K, or a missing, unexpected or repeated frame, makes the run INDETERMINATE. Because K ≥ 1 and convergence are required, every run that can pass has at least two frames. A run with no frame or a single frame cannot pass.
> - **Identity and fixed set.** The fixed set is H_M1 and H_T of B3 §1, 141 atoms, taken by `atom_id` from the run's identity sidecar. The input record binds each position in the shared atom order to one `atom_id`. N8 relies on the correspondence that the i-th input atom is the atom printed with index i in the force record and on the i-th line of every coordinate frame. Stage 1 must establish that correspondence for the build and input form used. Until it has, identity cannot be established, and the run is INDETERMINATE. Agreement of atom counts, element sequences and printed indices is a necessary consistency check. It is never proof of identity: it cannot detect an exchange of atoms of the same element.
> - **Fixed components.** In every judged force block, each of the x, y and z fields of every fixed atom must parse as a finite number with a zero significand, printed `0.00000000E+00` with either sign. A field that parses as a finite number with a non-zero significand fails the check. The check concerns the printed value only.
> - **Fixed coordinates.** In every judged frame, each of the three coordinates of every fixed atom must be character-identical to that atom's ten-decimal input string. A difference fails the check. This comparison is judged only on a build for which Stage 1 has shown that a coordinate that does not change prints identically to its ten-decimal input string. Otherwise the fixed-coordinate check is INDETERMINATE. Equality of printed strings does not prove equality in memory.
> - **Record integrity.** A record, block or frame that is empty, unparseable, non-finite, overflowed or inconsistent with the atom order is INDETERMINATE, and its content is not judged.
> - **Outcome.** FAIL if any check on a judged record fails; otherwise INDETERMINATE if any part of the run is INDETERMINATE; otherwise PASS. INDETERMINATE is blocking.
>
> No retained-component comparison is made. C6 requires N8 to PASS on each run named in row 10.

How the candidate meets the required declarations:

| Required declaration | Where the candidate makes it |
|---|---|
| Print digits, units and output selector | C1 (a) and (b): `ES15.8` in `hartree/bohr` in the main output, top-level force_eval only; `F20.10` in ångström |
| Iteration and evaluation association | C4, "Iterations": an index from the optimizer's own reports, independent of the force and coordinate records. It covers initial, per-iteration, duplicate and missing cases. It separates the force-bearing evaluations from the energy-only final reevaluation (S7, S7a), and its completeness rule excludes zero frames and a single frame |
| Identity and fixed-set mapping | C4, "Identity and fixed set": the input record and sidecar bind index to `atom_id`; the correspondence is a named Stage 1 observation; consistency checks are not identity |
| Failure and indeterminate precedence | C2 and C4, "Outcome": FAIL, then INDETERMINATE, then PASS; integrity failures are not judged |
| Rendered versus mathematical equality | C4, "Fixed components" and "Fixed coordinates", and Section 3 of this packet |

**Where N8 applies.** The candidate keeps N8's scope where C7 §2 already puts it: V1, V2 and V3 with the fixed
sets. Applying N8 also to every accepted step of the drive branches of B3 would extend its scope. That would be a
further decision, and it is not proposed here.

## 5. Stage 1 observations the candidate depends on

These are observations to be made on the build that Stage 1 installs, under its own authorization. **None of them is
a current observation.**
1. **Zero components.** A component that is `0.0_dp` in memory prints with a zero significand in the force record,
   with either sign accepted.
2. **Non-zero components.** A non-zero component prints with a non-zero significand, including the
   three-digit-exponent form that `ES` editing uses without the letter `E`.
3. **Non-finite values.** Non-finite values print in a form that the parser rejects.
4. **Unchanged coordinates.** A coordinate that does not change prints identically to its ten-decimal input string.
5. **Atom correspondence.** The i-th input atom is the atom printed with index i in the force record and on the i-th
   line of each frame.
6. **The iteration structure of S7 and S7a.** Force blocks, cycle reports and frames appear as S7 and S7a describe,
   including the absence of a force block after the final reevaluation. The top-level `Atomic` force block is
   distinguishable from any other force block in the main output.

If an observation fails or cannot be made, N8 is INDETERMINATE on that build until the definition is revised through
C4 §3.

## 6. Consequential frozen-record edit map

This map lists, by record and clause, every change that a future authorized application of O2 would require. It
covers every reference in the independent audit of this packet. For each one it gives either exact proposed text or
the reason for no change. **Every record in this map stays unchanged in this task.**

Three kinds of text are kept apart:
- *historical statements*, which were accurate on their dates and are never rewritten;
- *current-state statements*, which a future application would supersede, in place or by a dated update;
- *future freeze bindings*, which would change only after an approved revision.

**Placeholders.** Text in the form `[human-resolved: …]` is left open deliberately and is filled in only when a
person decides. It names what is missing: the decision date, or the file name of the new approval record.

**Independent items.** Two items are not consequences of O2:
- **C4-j**, the optional rewrite of C4's opening Approval bullet;
- **B3-b**, the editorial correction of a cross-reference in B3.

Each can be accepted or declined on its own. Accepting O2 does not require either of them, and neither requires O2.
Every other change in this map is a consequence of O2 and belongs with it.

### 6.1 C4 (`docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md`)

| Ref | Clause | Disposition |
|---|---|---|
| C4-a | Row 10, third column (`N8 is BLOCKED pending definition…`) | With O2: replace with candidate C1 |
| C4-b | Row 10, fourth column (`N8 is not run and has no outcome until…`) | With O2: replace with candidate C2 |
| C4-c | Paragraph after the table (lines 39–40, `Which CP2K output records…`) | With O2: replace with candidate C3 |
| C4-d | §2, N8 heading sentence (`N8, constraint projection. BLOCKED pending definition (row 10)…`) | With O2: replace with the heading sentence of candidate C4 |
| C4-e | §2, the fixed-atoms bullet | With O2: replace with the bullets of candidate C4 from "Iterations" to "Outcome". The frozen clause's substance, zero removed components and unchanged fixed coordinates in the recorded output, is kept and made exact |
| C4-f | §2, the retained-components bullet | With O2: remove it. Candidate C4 says "No retained-component comparison is made." |
| C4-g | §2, the sentence after the rule (`While r is undefined, N8 has no outcome, and C6 … cannot be met.`) | With O2: replace with the closing sentence of candidate C4 |
| C4-h | §2, closing paragraph (`Where a quantity cannot be resolved…`) | No change. It is consistent with the candidate and still governs any unresolvable quantity |
| C4-i | Row 10, second column (`Constraint projection`) | No change. The row keeps the spike §8.6 name; the third column sets its scope |
| C4-j | Opening Approval bullet (`Approval by a person is still PENDING…`) | **Independent and declinable; not a consequence of O2.** In a revised C4 this bullet would keep stating a status that no longer holds. Proposed text: "**Approval.** The roles are those of spike §8.6. The values are proposed by the method author (this package, `[AGENT]`), checked by the independent reviewer and approved by a person. Approval by a person is recorded outside this record, each approval bound to the exact digest it approved. Nothing here authorizes Stage 1 or claims readiness, parity or any physical result." If it is declined, the bullet stays as it is |
| C4-k | Rows 1–9 and 11; N1–N7; the electronic-state rule | No change. N8 does not touch them |
| C4-l | The N2 normalization qualification; the N3 compiled-basis statement | No change. They belong to other items ([C4-PROPOSED-REVISION-01.md §3](C4-PROPOSED-REVISION-01.md#3-audit-of-the-affected-clauses), A7 and A8) |
| C4-m | §3, the revision sequence | No change. The application itself follows it |
| C4-n | Line 4, "the numerical-convergence protocol N1–N8" | No change. N8 still exists |

### 6.2 Other frozen definitions

| Ref | Record and locator | Current text | Disposition |
|---|---|---|---|
| B3-a | [B3 §3](B3-DRIVE-PROTOCOL.md#3-per-step-relaxation), row "Constraint projection" (line 50) | `Verified in Stage 1 by N8 (C4 §3)` | With O2, change. Under O2 both the scope and the cross-reference would be wrong: N8 is defined in C4 §2 and row 10, not §3, and it would verify the fixed-atom behaviour only. Proposed cell: "The fixed-atom checks of N8 (C4 §2 and row 10), on the constrained runs of C7 §2. That the constraint leaves the other components unchanged is source-defined behaviour and is not tested at run time" |
| B3-b | B3 opening status paragraph (lines 5–6) | `…goes through the revision sequence (C4 §4).` | **Independent and declinable; not a consequence of O2.** The revision sequence is C4 §3. Proposed: replace "(C4 §4)" with "(C4 §3)". It can be applied with or without any N8 revision |
| C2-a | [C2 §5](C2-COUPLING-ROUTE.md#5-what-the-official-documentation-does-not-establish), item 6 (lines 101–102) | `Correctness of the coupled energy and gradient, including link-atom chain-rule terms and constraint projection, is validated only by C6 in Stage 1.` | With O2, change. Left as it is, the sentence would claim run-time validation of the whole constraint projection, which O2 no longer provides. Proposed: "Correctness of the coupled energy and gradient, including link-atom chain-rule terms, is validated only by C6 in Stage 1. For the fixed-atom constraint, C6 checks through N8 that the fixed components print as zero and that the fixed coordinates print as their input values. That the constraint leaves every other component unchanged rests on version-matched source reading only (source resolution record, §7) and is not validated at run time." The remaining basis is thus stated in the record itself |
| C2-b | C2 §6, "Validation" bullet (line 106) | `Validating this route is Stage 1, under C6 and N5/N8 in C4, on the validation set in C7.` | No change. N8 stays part of C6 under O2, and C2-a states what it covers |
| C7-a | [C7 §2](C7-VALIDATION-SET.md#2-components-tested-by-the-finite-difference-checks), bullet "Constraint projection (N8)" (line 46) | `Constraint projection (N8). Tested on V1, V2 and V3 with the fixed sets H_M1 and H_T of B3 §1.` | With O2, change of title and scope wording only; configurations and fixed sets unchanged. Proposed: "**Fixed-atom checks (N8).** Tested on V1, V2 and V3 with the fixed sets H_M1 and H_T of B3 §1, in the constrained GEO_OPT runs that C4 row 10 names. Retained components are not compared." |
| B2-a | [B2 §8](B2-METHOD-DECLARATION.md#8-what-stays-open), prerequisite bullet (line 172) | `The printed representations that N8 compares (C4, row 10).` | No change to the line, which belongs to the dated list of what was required. With O2, a new dated annotation after the existing one, exactly: "*Dated annotation, [human-resolved: decision date].* A person approved a revision of C4 that defines N8 as fixed-atom checks on the records of row 10 ([human-resolved: approval record file name]). The N8 item of the list above is settled by that definition. N8 has not been run, and its Stage 1 observations are outstanding." |
| B2-b | B2 §8, annotation item 4 (lines 181–185) | `N8 representations. PARTIALLY ESTABLISHED. …N8 stays BLOCKED and has not been run.` | No change. It is a historical dated annotation, accurate on its date. B2-a supersedes it for current status |
| B2-c | B2 §8, Stage 2 gate (line 206) | `C6. Composite validation, including N5 and N8.` | No change. It stays true under O2 |

### 6.3 Package index and freeze record (both frozen)

| Ref | Record and locator | Kind | Disposition |
|---|---|---|---|
| IX-a | [Package index](README.md), "Open items", lines 63–74 | Current state, with a dated history | No rewrite of existing lines. With O2, a new dated sub-bullet after line 74, exactly: "*Updated [human-resolved: decision date]:* a person approved a revision of C4 that defines N8 as fixed-atom checks ([human-resolved: approval record file name]). N8 is no longer blocked by its definition. It has not been run, and its Stage 1 observations are outstanding. Whether this prerequisite holds depends on the other definitions listed here." |
| IX-b | Package index, lines 71–74 (the dated update of 2026-09-27) | Historical dated update | No change. IX-a supersedes it for current status |
| IX-c | Package index, line 82 (`C6, which needs N5 and N8.`) | Current state | No change. It stays true |
| IX-d | Package index, Records table | Navigation | With O2, one added row, exactly: "\| C4 approval, revision \| [human-resolved: approval record file name] \| The human approval of the revision of C4 that defines N8 as fixed-atom checks, bound to its own commit, path and SHA256 \|" |
| FR-a | [Freeze record](STAGE0-FREEZE-RECORD.md) §1: the review history (lines 14–51), the C4 approval paragraph (lines 52–65) and the source-resolution paragraph (lines 67–79) | Historical | No change. Each was accurate on its date |
| FR-b | Freeze record §1, C4 row of the disposition table (line 86) | Current state | With O2, appended at the end of the "What remains" cell, exactly: "*[human-resolved: decision date]:* a person approved a revision of C4 that defines N8 as fixed-atom checks ([human-resolved: approval record file name]); N8 is no longer blocked by its definition and has not been run." |
| FR-c | Freeze record §1, the Stage 0 closure paragraph ("C4 (N8 BLOCKED)", line 94) | Historical, as of the closure | No change to the paragraph. With O2, a new paragraph after the source-resolution paragraph, exactly: "**Revision of C4 ([human-resolved: decision date]).** A person approved a revision of C4 that defines N8 as fixed-atom checks, bound to commit [human-resolved: commit], path `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` and SHA256 [human-resolved: new digest] ([human-resolved: approval record file name]). It supersedes, for N8 only, the definition approved on 2026-09-27 at SHA256 `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`. That approval record is unchanged. N8 has not been run. The revision validates nothing physically, upgrades no evidence label and authorizes no Stage 1 work." |
| FR-d | Freeze record §1, readiness bullet on the five definitions (lines 106–110) | Current state | No rewrite. With O2, appended to the end of that sub-bullet, exactly: "*[human-resolved: decision date]:* the N8 representations are settled by the approved revision of C4 ([human-resolved: approval record file name]); this prerequisite holds only when the other definitions listed here are also settled." |
| FR-e | Freeze record §1, Stage 2 gates, "C6: composite validation, including N5 and N8" (line 122) | Current state | No change. It stays true |
| FR-f | Freeze record §2, bindings | Future freeze binding | Changes only after an approved revision. The C4 row would read: "\| C4 tolerances and convergence \| `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` \| [human-resolved: new digest] \| `[AGENT]` declarations; cited defaults `[LIT]`. Budgets are declarations, not validated uncertainties. Revised [human-resolved: decision date]; the digest approved on 2026-09-27 was `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d` \|". A row for the new approval record would be added as a process record. The rows of B3, C2, C7, B2 and the package index would be refreshed only for the records actually revised. Nothing in §2 changes before a person approves a revision |

### 6.4 Records that stay historical or are not frozen

| Ref | Record | Disposition |
|---|---|---|
| AP-a | [C4-HUMAN-APPROVAL.md](C4-HUMAN-APPROVAL.md) | **No change for this purpose, ever.** It is the historical approval of the exact bytes with digest `707c7f72…ffbb68d` at commit `bd3d16a5…`. It must never be rewritten to imply that a later candidate was approved under that digest. A person's choice of a revision needs a **new** decision record, for example `C4-HUMAN-APPROVAL-02.md`. That record binds the new commit, path and digest and states which approval it supersedes, and for what |
| SR-a | [SOURCE-RESOLUTION.md](SOURCE-RESOLUTION.md) | No change. It is a dated record of source facts, accurate on its date |
| PR-a | [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md) | No change. Its status table records the steps as of 2026-09-27, and a new decision record would state the later steps |
| ST-a | Status and navigation surfaces that are not frozen: the root README, `AGENTS.md`, `.agents/RESEARCH-STATE.md`, `docs/SOURCES.md` and the export manifest | Updated with the application, as status only, each change stated in the manifest |

## 7. The sequence a decision would follow

1. **Recorded reason (C4 §3, step 1).** Done in [C4-PROPOSED-REVISION-01.md §1](C4-PROPOSED-REVISION-01.md#1-recorded-reason-c4-3-step-1).
   This packet adds no new reason.
2. **Fresh approval by the same roles (step 2).**
   - The method author proposes exact revised bytes of C4, together with the consequential edits of Section 6 and
     any independent item the person wants.
   - The independent reviewer checks those exact bytes.
   - A person decides: APPROVE, REQUEST REVISION or DEFER.
   - An approval is recorded in a new approval record, bound to the commit, path and SHA256 of the revised C4. The
     approval of 2026-09-27 stays as it is.
3. **Revalidation (step 3).** Nothing that N8 governs has run, so nothing is repeated. The new record says so.
4. **Retention (step 4).** Not applicable, because no N8 result exists. The superseded C4 bytes stay identifiable
   by their digest.
5. **Freeze and status.** The bindings of FR-f are refreshed, and the surfaces of ST-a are updated.

Stage 1 would stay BLOCKED after this sequence, until a separate authorization is given and every other prerequisite
holds.

## 8. If a person chooses another option

| Option | Obligations that would follow |
|---|---|
| O0 | None now. N8 stays BLOCKED, and C6 cannot be met on the declared route. The prerequisite of row 10 stays unmet, so Stage 1 cannot start under the current prerequisites unless they change through C4 §3 |
| O1 | A declared allowance r, with its unit, its dependence on the `ES` exponent and its behaviour at an exponent boundary, and a stated justification that is not a source-defined rounding bound. The same iteration, identity, integrity and precedence declarations as candidate C4. A statement in C4 that the retained-component comparison compares renderings of one array. The Stage 1 observations of Section 5 |
| O3 | Settlement in Stage 1 of the link-atom force mapping and the numerical mixing derivative (C2 §5, items 1 and 3), and a declared record of the derivative values used. An allowance for two records and the reconstruction. No decision is possible before those Stage 1 results exist, so the Stage 1 prerequisite of row 10 would need its own revision |
| O4 | A separate proposal for an instrumented build: the exact code change, its review, its own authorization, the provenance of the changed source and build, and a prospective declaration of the projection. A departure from the stock CP2K 2026.2 route stated in B2 and C2 |

## 9. Limitations

- Every recommendation, candidate text and edit in this packet is `[AGENT]`. It is a proposal by the method author of
  this package and never evidence about physics.
- Every source statement reports software behaviour defined by the cited CP2K 2026.2 release source. None describes a
  build, a run or a printed output. No formatting behaviour of any compiled build has been observed.
- The Section 5 observations are required before any outcome.
- The candidate texts are exact as proposals. They have not had the independent review that step 2 of C4 §3
  requires for revised C4 bytes.
- Stage 1 remains BLOCKED and is not authorized.
