# B3 drive protocol

Status: MS-001 Stage 0, scope option B. Every choice below is an `[AGENT]` declared deviation. The benchmark does
not state how its coordinate is imposed: the fixed atoms, step size, per-step relaxation and constraints are all
missing (spike §2.5, P4). The protocol is fixed before Stage 1, and a change after freezing goes through the
revision sequence (C4 §4).

A nudged elastic band (NEB) is never a substitute for this protocol (P4). NEB finds a zero-force path between fixed
endpoints, with no drive, no branches and no history. It may appear only as optional supporting analysis at a fixed
drive value, on results that are not quarantined (spike §3, M7).

## 1. Bodies, fixed sets and the drive

Atom identifiers and 1-based indices refer to the frozen files in
[structures/ms-001](../../structures/ms-001/README.md). Every combined file has the same atom order.

| Item | Declaration |
|---|---|
| Moving body | M1, the build site, which mirrors the moving probe chip of the experiment |
| Stationary body | The tool (M2). Its legs would rest on a sample surface, which is not modelled |
| M1 handle, H_M1 (135 atoms) | Every Si of layer 4 (`S-L4-*`, 45 atoms) and every H capping them (90 atoms). Indices 143–187 and 272–361 |
| Tool handle, H_T (6 atoms) | `D-O1`, `D-O2`, `D-O3`, `D-O1-H1`, `D-O2-H1` and `D-O3-H1`. Indices 369, 374, 380, 389, 396 and 405 |
| Free atoms (268) | Every other atom, relaxed at every step |
| Drive | At each step, H_M1 is rigidly translated along z by the step Δz, with no rotation; H_T does not move. Approach is +z, towards the tool, and retraction is −z |
| Drive coordinate | d, the cumulative imposed translation of H_M1 from the start, in Å. The separation D = z̄(H_T) − z̄(H_M1) is recorded at every step; it is 16.738 Å in the start file |
| z0 and z − z0 | z0 is the value of D at the first accepted approach step at which the **geometric trigger T_A** holds (Section 5). It is not tied to event E1, which also needs an energy criterion. If T_A never holds on an accepted approach step, z0 is undefined and D − z0 is not reported. z − z0 is reported as D − z0. This mirrors the benchmark's use of z − z0, where z is the distance between the two surfaces (spike §2.5). It is not the same coordinate, because this model has no sample surface |
| Alternative, untested | A stiffer tool handle that also fixes `D-L1b`, `D-L2b` and `D-L3b`. It is recorded for the model-geometry diagnostic (spike §8.8, item 3) |

## 2. Steps and branches

| Item | Declaration |
|---|---|
| Base step | Δz = 0.10 Å |
| Coarser and finer steps | 0.20 Å and 0.05 Å, used only in sensitivity segments (checkpoint S) |
| Step 0 | The frozen start file, relaxed with H_M1 and H_T fixed in place. Step 0 opens the approach branch |
| Approach branch A | Steps 1, 2, … each translate H_M1 by +0.10 Å from the previous accepted step. The branch ends at whichever comes first: (a) five accepted base steps after the first accepted step at which the geometric trigger T_A holds, which is 0.50 Å past that step; (b) a cumulative translation of 6.00 Å (step 60), whether or not T_A has held; (c) a step that is not accepted, including step 0 itself (Section 5, zero accepted steps). The stopping rule uses T_A only, never the energy part of event E1. Checkpoint windows for events near these ends are defined in Section 5 |
| Retraction branch R | Starts from the last accepted step of A, with its geometry and wavefunction, subject to the retraction-eligibility rule of Section 5. Steps translate H_M1 by −0.10 Å. The branch ends when d reaches −2.00 Å, that is 2.00 Å beyond the start separation, or at a step that is not accepted |
| Continuation | Each step starts from the relaxed geometry of the previous accepted step on the same branch, with H_M1 translated. The SCF of every sub-force_eval restarts from that step's converged wavefunction (`SCF_GUESS RESTART` [S0-cp2k-scf]). Branch results are therefore history-dependent by design |
| Unaccepted step | Recorded in full with its exit codes and logs, never overwritten (C3 F9). Propagation of the branch stops, and no retry with changed settings is made outside the revision sequence |

## 3. Per-step relaxation

| Item | Declaration and source |
|---|---|
| Energy and forces | The composite E = E1 − E2 + E3 of C2, evaluated by CP2K 2026.2 as one `MIXED` force_eval |
| Optimizer | CP2K `MOTION/GEO_OPT`, `TYPE MINIMIZATION`, `OPTIMIZER BFGS`. BFGS is the documented default [S0-cp2k-geo-opt] and is declared explicitly |
| Stopping criteria | The documented defaults for CP2K 2026.2 [S0-cp2k-geo-opt]: `MAX_FORCE 4.5e-4` hartree/bohr, `RMS_FORCE 3.0e-4` hartree/bohr, `MAX_DR 3.0e-3` bohr, `RMS_DR 1.5e-3` bohr and `MAX_ITER 200`. They are stopping criteria and not accuracy bounds (C4, row 1) |
| Constraints | `MOTION/CONSTRAINT/FIXED_ATOMS` with `LIST` giving the 141 indices of H_M1 and H_T, and `COMPONENTS_TO_FIX XYZ` (the default) [S0-cp2k-fixed-atoms] |
| Acceptance | A step is accepted only if GEO_OPT reports convergence within `MAX_ITER` and every SCF of every sub-force_eval converged to `EPS_SCF` within `MAX_SCF` (B2 §4; C4, row 2). The maximum residual force of every accepted step is reported and is never tuned (spike §8.5) |
| Constraint projection | The fixed-atom checks of N8 (C4 §2 and row 10), on the constrained runs of C7 §2. That the constraint leaves the other components unchanged is source-defined behaviour and is not tested at run time |

## 4. Branch bookkeeping

Every step, accepted or not, records the following, in addition to the C3 field set:
- branch (`A`, `R`, or a sensitivity segment `S-A-coarse`, `S-A-fine`, `S-R-coarse` or `S-R-fine`);
- step index; imposed Δz; cumulative d; measured D; parent step; restart source;
- GEO_OPT iteration count, convergence flags and maximum residual force; SCF convergence of each sub-force_eval;
- the digests of the input and output files;
- acceptance, and the checkpoint state (pending, released or quarantined).

Retraction steps record the approach step they started from.

## 5. Checkpoints (declared here, applied in Stage 2)

These are the selectors required by C7 and spike §8.5. Every selector below is deterministic: it is fixed before
Stage 1, and applying it needs only the recorded accepted steps and the cutoff rule of C4, row 4. The comparison made
at checkpoint S is not a selector: it compares the inherited events E1–E4 under their full criteria, and so also needs
N6 for E1.

**Geometric triggers.** Scan control and checkpoint selection use two geometric triggers and nothing else. Each is
judged from coordinates alone by the cutoff rule of C4, row 4, and holds at a step only if it holds at all three
multiples. Neither has an energy part. For the trigger step k_b and the stopping rule, a judgement that is
indeterminate at a step counts as not holding there. The triggers **select** configurations and segments only. They
are never what checkpoint S compares, and a match of trigger lists, or of any geometric part of an event, alone
**never releases** a segment or a branch.

| Trigger | Definition | Governs |
|---|---|---|
| T_A, geometric Si–C trigger | `D-Cb`, the distal C, bonded to `S-L1-07-05` or to `S-L1-09-05`, the site pair | z0 (Section 1), the approach stopping rule (Section 2), and the approach trigger step, anchor and window |
| T_R, geometric Ge–C trigger | `D-Ge1`–`D-Ca` non-bonded. This is only the Ge–C cleavage condition of event E2. The full event E2 also requires the Si–C bond to persist and the Si–Si bonds at the anchoring Si to stay intact | The retraction trigger step, anchor and window |

**Inherited events E1–E4.** These are the events of spike §8.4, each judged under its full criterion at every accepted
step of every run: the base scan and both sensitivity re-runs. They are reported, and they are what checkpoint S
compares (below). A criterion made of several geometric conditions is observed only if every condition holds at all
three multiples, not observed if some condition fails at all three multiples, and INDETERMINATE otherwise.

**Event E1.** Spike §8.4 defines E1 as a Si–C bond forming between the tool's distal C and one Si of the site pair,
"with a concurrent decrease in total energy at that step (sign only)". E1 is judged at each accepted step of every
approach run, where k − 1 is the predecessor defined under Comparison below. It never sets z0, the stopping rule or a
window, and T_A holding is never reported as E1.

| Part or case | Rule |
|---|---|
| Bond part, at step k ≥ 1 | T_A holds at k, and at k − 1 `D-Cb` is non-bonded to both site-pair Si at all three multiples |
| Energy part, at step k ≥ 1 | The composite ΔE = E(k) − E(k − 1) is negative, with its sign reported under N6 from direct envelopes at both configurations (C4, row 3 and §2). No constituent envelope, transferred envelope or budget is used |
| Observed at k | Both parts hold at k |
| Not observed at k | At k, `D-Cb` is non-bonded to both site-pair Si at all three multiples; or at k − 1, `D-Cb` is already bonded to a site-pair Si at all three multiples; or the bond part holds and N6 reports a positive sign |
| **Unavailable energy**, or any other case | INDETERMINATE at k. This covers an indeterminate cutoff judgement at k or k − 1, and a bond part that holds while either composite energy, or any N6 repeat or tighter-rung value at k − 1 or k, is missing or not converged, or while N6 cannot resolve the sign. A geometric result never replaces the missing energy criterion |
| **Step 0** | Step 0 has no predecessor, so no concurrent energy change exists. E1 is not observed at step 0 if `D-Cb` is non-bonded to both site-pair Si at all three multiples; otherwise it is INDETERMINATE at step 0. T_A is judged at step 0 like any other step: if it holds there, k_A = 0 and z0 = D(0) |
| On the branch | E1 is **observed** if it is observed at some accepted approach step; **not observed** if it is not observed at every accepted approach step, including step 0; otherwise **INDETERMINATE**. If A has no accepted step, E1 is INDETERMINATE |

**Events E2, E3 and E4.** Their criteria are geometric and are judged by the cutoff rule of C4, row 4, except where
another row is named.

| Event | Full criterion | Judged on |
|---|---|---|
| E2, Ge–C cleavage with the Si–C bond kept | All three conditions hold: the Ge–C bond is broken (T_R); the Si–C bond persists, meaning `D-Cb` is bonded to a site-pair Si (T_A), which is the **anchoring Si**; and every anchoring Si is still bonded to each of its three constructed Si neighbours in the start file ([geometry record](../../structures/ms-001/README.md), site-pair row). T_R alone is never reported as E2 | Retraction runs |
| E3, the pendent C2 over a finite range | The **pendent-state condition** at a step: all three conditions hold, namely `D-Ge1`–`D-Ca` is non-bonded (T_R); exactly one Si of M1 is bonded to `D-Ca` or `D-Cb`; and the proximity of claim (i) holds as C4, row 5 defines it. Spike §8.4 requires the pendent C2 to exist "over a finite z range", so E3 **occurs** only where this condition persists as the E3 persistence rules below declare. A single step never makes E3 occur. The compared E3 uses claim (i), proximity and connectivity, and nothing else. Claims (ii), radical character, and (iii), interaction and stabilization, are claims about that state: they are reported at each step under C4, rows 6 and 7, are never compared, and are never supported by proximity | Every run |
| E4, bridging | E4 has no energy part, so its full criterion is geometric: `S-L1-07-05` and `S-L1-09-05` are each bonded to `D-Ca` or `D-Cb`; no other Si is bonded to `D-Ca` or `D-Cb`; and every M1 hydrogen is bonded to the Si it caps in the start file | Every run |

E1 and E2 are judged only on the branch that spike §8.4 assigns them, the approach for E1 and the retraction for E2;
on the other branch they are absent from the compared lists, not INDETERMINATE. E5 and E6, and the E3 claims (ii) and
(iii), are reported under their own criteria (C4, rows 3–7) and are not compared at checkpoint S.

**E3 persistence.** These rules are an `[AGENT]` declaration fixed before Stage 1, with no calculation behind them.
They are applied identically in the base run and both re-runs. At checkpoint S they use only the accepted steps of
the compared interval [d(s_b), d(e_b)].

| Item | Rule |
|---|---|
| Declared minimum persistence | **Δd_min = 0.20 Å** of imposed d, the drive coordinate that all three runs share. A **qualifying span** is a sequence of consecutive accepted steps of one run, from step j to a later step j′ with \|d(j′) − d(j)\| ≥ 0.20 Å, at every one of which the pendent-state condition is observed. The value equals the coarsest declared step, so each run can establish it from at least two accepted steps. It is a declaration, not a physical threshold, and it says nothing about the width of the range in the benchmark |
| First occurrence | E3 first occurs at the **first step j of the first qualifying span** of the run and is placed at d(j). The step at which the span becomes complete is not used |
| Isolated hit | A step, or a set of consecutive steps, at which the condition is observed, followed inside the interval by a step at which it is determinately not observed before the span reaches Δd_min. It is **not** an occurrence of E3: E3 is **not observed** there, and the hit is reported only as a short pendent span. An isolated hit never enters the compared list and never contributes to a release |
| Span open at the start | Steps before d(s_b) are never used, because the re-runs have none. A span in which the condition is observed at d(s_b), which is the same configuration in all three runs, is taken to start at d(s_b) in each run |
| Span open at the end | A span that reaches Δd_min at or before d(e_b) qualifies, whatever follows it. If no qualifying span has occurred earlier in the run, and a span in which the condition is still observed at d(e_b) has not reached Δd_min, persistence cannot be established inside the interval. E3 is then **INDETERMINATE** in that run, which is blocking |
| Terminated re-run | A re-run that terminates, including inside a candidate span, makes checkpoint S INDETERMINATE under the re-run rule below |
| Indeterminate step | If the pendent-state condition is INDETERMINATE at any accepted step of the interval, E3 is INDETERMINATE in that run, as for every compared event |
| Outside checkpoint S | On a whole branch, the same rules apply to its accepted steps. A span still open when the branch ends, without reaching Δd_min and with no earlier qualifying span, makes E3 INDETERMINATE for that branch |

**Indexing.** On each branch b, the accepted base steps are indexed j = first_b, …, J_b:
- On A, first_A = 0 (step 0) and J_A is the last accepted approach step.
- On R, first_R = 1 (the first retraction step) and J_R is the last accepted retraction step. R's starting
  configuration is step J_A of A and is not an R step.

An unaccepted step is never indexed and never enters a window.

| Term | Definition |
|---|---|
| Trigger step k_b | On A: the first accepted base step at which T_A holds. On R: the first accepted base step at which T_R holds |
| Anchor a_b | k_b if the trigger holds at some accepted step of the branch. If it never does (**missing trigger**), J_b |
| Window W_b | If the trigger holds, the accepted steps with indices in [k_b − 3, k_b + 3], clipped to [first_b, J_b]. If the trigger is missing, the accepted steps with indices in [J_b − 6, J_b], clipped to [first_b, J_b]. Its first index is s_b, its last e_b, and its width is n_b = e_b − s_b base steps |
| **Early trigger** | If k_b − 3 < first_b, the window starts at first_b and is not extended to the right to compensate |
| **Late trigger, or a short or terminated branch** | If k_b + 3 > J_b, because the branch reached its limit or was stopped by an unaccepted step, the window ends at J_b and is not extended to the left to compensate |
| **Too short** | If n_b < 2, that is fewer than three accepted steps in the window, no sensitivity re-run is made. Checkpoint S for that branch is INDETERMINATE |
| **Zero accepted steps** | A branch with no accepted base step at all: on A, step 0 is not accepted; on R, the first retraction step is not accepted. J_b, k_b, a_b, s_b, e_b and W_b then **do not exist**. The branch check and checkpoint S for that branch are both recorded as **INDETERMINATE (blocking)**, and **no sensitivity re-run** is made. Every event and trigger that the branch would judge is INDETERMINATE. **No dependent branch starts**: if A has no accepted step, R is recorded as **not started (approach has no accepted step)**. No branch starts from R. A restart happens only through the revision sequence |

| Checkpoint | Rule |
|---|---|
| Branch check, approach and retraction | Performed at step a_b. When the trigger holds, propagation pauses on accepting k_b until the check is recorded. When the trigger is missing, the check is made after the branch has ended. With zero accepted steps there is no a_b, and the check is INDETERMINATE (blocking) as defined above |
| Sensitivity checkpoint S | Performed when the scan has accepted e_b; propagation pauses until the check is recorded. For a missing trigger it is made after the branch ends. With zero accepted steps there is no e_b and no re-run, and S is INDETERMINATE (blocking) |
| Sensitivity re-runs | Two re-runs start from the recorded relaxed configuration and wavefunction of base step s_b and cover the imposed-d interval [d(s_b), d(e_b)] in the branch's direction. The **fine** run takes 2·n_b steps of 0.05 Å. The **coarse** run takes steps of 0.20 Å; when n_b is odd, its last step is 0.10 Å, so that both runs **end exactly at d(e_b)**. Re-runs use the per-step relaxation, acceptance and restart rules of Sections 2 and 3. A re-run step that is not accepted terminates that re-run, and checkpoint S is INDETERMINATE |
| Comparison | For each of the base, coarse and fine runs, the ordered list of first occurrences of the **inherited events E1, E2, E3 and E4** within the interval is formed, each under its full criterion above: E1 with both its bond part and its N6-resolved energy decrease; E2 with the broken Ge–C bond, the persistent Si–C bond and the intact Si–Si bonds at the anchoring Si; E3 with its pendent-state condition persisting over Δd_min under the E3 persistence rules; and E4 with its bridging criterion. Within a run, the predecessor of a step is the previous accepted step of that run. The configuration at d(s_b) is base step s_b in all three runs, with base step s_b − 1 as its predecessor, and the step-0 rule of E1 applies when s_b = 0. Each event is placed at the d of the accepted step at which it is first observed; for E3 that is the first step of its first qualifying span, and an isolated E3 hit is never placed in the list. Events first observed at the same step are recorded as simultaneous. The order is **unchanged** only if the three lists are identical, including simultaneity and including the case where all are empty. Any difference means the order has **changed**. If any compared event is INDETERMINATE at any accepted step of any run in the interval, the outcome is **INDETERMINATE**. That includes an indeterminate cutoff judgement, a missing or unconverged composite energy or N6 value, an E1 sign that N6 cannot resolve, and an E3 whose persistence cannot be established inside the interval. A geometric result never replaces the missing energy criterion, and a match of trigger lists or of geometric parts alone never releases the segment |
| Quarantine | As spike §8.5. A changed or indeterminate S quarantines every accepted step of b from s_b onward and the checkpoint's own runs. A failed or indeterminate branch check quarantines the whole branch b. In both cases the quarantine also covers every later branch that starts from a quarantined step, and everything derived from these results. Steps before a quarantined span stay usable |
| Retraction eligibility | R starts only after both checkpoints of A are recorded, and only if step J_A is not quarantined. Otherwise R is recorded as **not started (quarantined start)**, and it can start only through the revision sequence. If A has no accepted step, R is recorded as **not started (approach has no accepted step)** |
| Restart | Only through the revision sequence (C4 §3). Re-running identical settings is never used to seek a different outcome |
