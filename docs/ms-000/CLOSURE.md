# MS-000 closure record

Status: closure record of the MS-000 feasibility study, dated 2026-09-24. It audits the package in this directory
against the six gate criteria of the
[compute spike](MS-000-COMPUTE-SPIKE.md#81-ms-000-gate-criteria-and-current-status) and records the corrections
made to the package with it. It contains no calculation and no physical result, and it authorizes nothing.

Evidence tags are defined in [EVIDENCE-POLICY.md](EVIDENCE-POLICY.md). Tags such as [S-cp2k-vdw] resolve in the
[source ledger](SOURCE-LEDGER.md); entries cited as SOURCES.md [n] are in the repository catalogue
[docs/SOURCES.md](../SOURCES.md). Software facts are as retrieved on 2026-09-16 and were not re-checked for this
record, so later releases or revised documentation may exist. Everything this record adds is `[AGENT]` planning
content over those facts.

## 1. Verdict

| Question | Verdict | Basis |
|---|---|---|
| MS-000 gate: are its six feasibility criteria met? | **PASS** | Criteria 1–5 are met on the evidence cited in Section 2. An independent scientific review approved the plan and bound its decision to the reviewed file digests (criterion 6). The gate consists of these six criteria and nothing else. |
| MS-001 faithful-reproduction readiness (scope option A) | **BLOCKED** | It is blocked by missing source inputs and missing evidence. The inputs are the Cowie model geometry with atom identities, the partition, the embedding and link treatment, charge and spin, the basis, ECP and dispersion parameters, and the drive protocol (spike §1, §2.9). The evidence is parity for P1–P4 and a demonstrated coupling route, P3b (spike §4). It stays blocked whatever is authorized. It is a status of option A (Section 8), not an MS-000 criterion. |
| Human authorization of MS-001 | **Absent** | This is a separate prerequisite of either scope option (spike §8.3 C1). None is recorded or implied here, and neither option is selected. Its absence is not what blocks faithful reproduction, and obtaining it would not unblock faithful reproduction. |

The gate judges a plan. On the present record:
- A credible open-source stack is identified.
- Every major requirement of the Cowie IR-C2 model maps to an implementation or to an explicit gap.
- The dependency set is justified.
- The MS-001 acceptance criteria and tolerance procedure are prospective and, after the corrections in Section 3,
  have no forward dependency.
- No physical statement rests on language-model output.
- The plan received independent review (criterion 6).

The gate, whatever its disposition, does not establish any of the following:
- that any calculation will converge or reproduce the paper
- that any tool is equivalent to the unpublished setup
- that faithful reproduction is possible now
- that a scope option is chosen
- that anything may be installed or run

[evidence-policy.md §5](../evidence-policy.md#5-separate-acceptances) defines a scientific gate as evidence that
meets a declared criterion, checked independently, which does not imply permission to proceed. It defines
authorization as a person permitting a bounded next step. [ARCHITECTURE.md §6](ARCHITECTURE.md#6-three-separate-acceptances)
draws the same distinction. Two passages previously tied the person to gate passage. ARCHITECTURE.md §2 gave humans
"every milestone gate", and §3 counted a milestone as passed only once a person recorded authorization to
proceed. Both conflicted with §6 and were corrected with this record (finding F5). A person remains required for
authorization, and for nothing in the gate.

E-01 is unaffected. It remains technically BLOCKED and scientifically INDETERMINATE
([results/e01](../../results/e01/README.md)), and no MS-000 criterion depends on it.

## 2. Gate disposition

Each criterion is disposed on the package as revised with this record. "Kind" states whether satisfaction depends
on a future value, on a future decision procedure, or on neither.

| # | Criterion (spike §8.1) | Evidence relied on | Kind | Disposition |
|---|---|---|---|---|
| 1 | Credible stack identified | [Landscape §3](OPEN-SOURCE-LANDSCAPE.md#3-conditional-minimum-stack-for-ms-001): ASE, CP2K and AiiDA with `aiida-cp2k`. CP2K documents an internal GFN0-xTB (`GFN_TYPE 0`, default 1) [S-cp2k-xtb] and `WB97X_D3` through libxc with exact exchange set in its HF section [S-cp2k-xc], [S-cp2k-hf]. AiiDA runs a small profile without external services [S-aiida-install]. Three existing coupling routes are identified ([landscape §4](OPEN-SOURCE-LANDSCAPE.md#4-coupling-route-candidates-p3b-existing-tooling-evaluated-reuse-first)). | Neither. Identification is complete. How well the stack serves MS-001 depends on future values (P1, P2 and P3b in Stage 1; parity under option A), which this criterion does not require. | **MET.** The stack is conditional, and its conditions are named in spike §4. They are MS-001 stage preconditions (Section 8), not MS-000 criteria. |
| 2 | All major Cowie requirements mapped to implementations or explicit gaps | Spike §3 (M1–M13) and §4 (P1–P4, P3b); Section 6 here | Neither | **MET.** Every item has a named implementation or an explicit `[GAP]`. The review point of M1 is corrected (F4). |
| 3 | Justified minimum dependency set | Landscape §1–§2 (eleven fields per tool: `[LIT]` facts, `[AGENT]` decisions) and the §3 tiers, corrected for finding B and F6; Sections 4 and 5 here | Neither for the class rule. Two entries depend on the coupling route selected in Stage 0 (spike §8.3 C2), a procedure already fixed. | **MET** |
| 4 | Prospective MS-001 acceptance criteria | Spike §8.4 (E1–E6) and §8.5–§8.6 as corrected for findings A, C, F1, F7, F8 and F9; Section 7 here | Procedure. Every tolerance is a documented stopping criterion, a declared multiple, a declared acceptance budget applied through an explicit rule, or a declaration, and each is fixed before Stage 1. The calibration it needs runs in Stage 1a, before the Stage 1b checks that consume it. Every rule has pass, fail and indeterminate outcomes and a blocking disposition, and the Stage 2 checkpoints are defined. The numeric values are Stage 0 declarations or Stage 1a measurements by design. | **MET** |
| 5 | No LLM physics | Spike §2 gives every physical statement a paragraph or caption locator in [S2]/[S3]. Each is an experimental observation reported by the paper (`[EXP]`); a result of the paper's computational model (`[COMP-PRED]`, such as the Fig. 3 mechanism, which is admissible evidence of that kind and never upgraded); a possibility the paper offers without stated computational support (`[LIT]` over `[SPEC]`, such as its candidate failure routes for the 2IR-C4 off-target product, spike §2.7); or a `[GAP]`. The rules are in [EVIDENCE-POLICY.md §1–§3](EVIDENCE-POLICY.md#1-the-six-evidence-classes-never-conflated). Language-model output supplies no physical statement. This record's own content is `[AGENT]` planning and adds no physical statement. | Neither | **MET** |
| 6 | Independent scientific review approves the plan | The independent review recorded APPROVE for the scientific plan and bound the decision to the exact reviewed files through export-manifest SHA256 `50bd256010b680f708cc7a8455018d331f098724cba29ebe69c6cd3c5c7b7a33`. The private, non-published review record is kept separately from these public files. A final independent review also checks this status promotion against that decision. Review assesses a plan. It is neither physical evidence nor parity validation, and it validates no engine, method or result. | Digest-bound independent review of the plan | **MET** |
| | **MS-000 gate (criteria 1–6)** | Rows 1–6 | | **PASS.** All six criteria are met. |

Stage 1 evidence can reopen criteria 1 and 3. If no candidate route can compose the two levels, or no tool can
fill a required role, the stack and the dependency set must be revised and reviewed again.

## 3. Audit findings and corrections

**A. Forward dependency in tolerance freezing.**
- Defect: spike §8.6 required every tolerance to be frozen before Stage 1. Yet it based the force-convergence
  tolerance on the documented default "tightened only if the step-size sensitivity check shows event-order
  dependence", and that check needs the Stage 2 trajectory.
- Correction: the initial value is the documented default of the optimizer selected in Stage 0, cited from
  documentation for the exact version used. Under option A it is the source-stated per-step criterion where A1
  gives one.
- The sensitivity check can only trigger the revision sequence in Section 7; it never selects a value. Section 7
  also states how every tolerance is fixed before Stage 1.

**B. Psi4 as an optional package versus a required capability.**
- Defect: landscape §3 said that omitting Psi4 would leave P2 internal consistency open, and its Psi4 decision
  allowed P2 to be "left open". Spike §8.3 C5 requires P2 to be established before Stage 2.
- Correction: the package stays optional. Psi4 1.11 lists `WB97X-D3` [S-psi4-dft], and any engine that implements
  the same functional may replace it. The capability, a second implementation of ωB97X-D3 for the P2 cross-engine
  check, is a required validation dependency.
- Blocking consequence: without that capability, C5 is unmet and Stage 2 may not begin. Stages 0 and 1 are not
  blocked.
- Local records give a further reason to keep the package optional. The project's only Psi4 run, E-01, stopped
  before any SCF iteration. The equivalence of the installed build's `wB97X-D3` entry to the benchmark functional
  is open ([engine-capability-status.md](../engine-capability-status.md#functional-identity-of-wb97x-d3)). The
  package's fitness for this check is therefore unestablished.

**C. "One configuration per branch".**
- Defect: spike §8.5 specified the constituent-level finite-difference checks, which are Stage 1 work, on "one
  configuration per branch". Branches exist only once the Stage 2 driven scan has run.
- Assessment: representative pre-trajectory validation configurations must therefore be declared and frozen in
  Stage 0. Energy–force consistency is a property of a configuration and its electronic state, not of trajectory
  history. Configurations built geometrically from the frozen model and drive inputs therefore test the relation
  the scan relies on. They are built without calculation, are unrelaxed, and are `[AGENT]` inputs rather than
  results.
- Coverage: the set spans the bonding situations the branches should pass through (E1–E3):
  - the separated bodies
  - tool–surface contact with the Ge–C bond intact
  - a pendent C2 with the Ge–C bond broken
- A driven step can reach an electronic state that depends on its history. The same checks on one configuration
  visited on each branch therefore become a declared Stage 2 checkpoint. A failure quarantines that branch as
  Section 7 defines, and the check is not a precondition of Stage 2.
- The new prerequisite C7 freezes the set (spike §8.3).

The same test applied to every other Stage 1 input:
- The P1 identity run needs only the route (C2) and one frozen configuration, so it has no forward dependency.
- The P2 check lacked a declared test molecule; C7 now declares it.
- The composite and constraint-projection checks take the boundary and link-host atoms from the frozen partition
  (A3/B2) and the constraints from the frozen drive protocol, so they have no forward dependency once C7 exists.
- Option A's equivalence evidence had no prospective test (F2).

**Further findings.**
- **F1, incomplete procedure.** Spike §8.6 gave no tolerance for the constituent finite-difference check or the
  constraint-projection check, and no rule for deciding the sign-only energy criteria E1 and E5 within numerical
  noise. It also left the sensitivity segment and step sizes undeclared. These are now covered by the
  numerical-convergence protocol (F7) and by declarations made with the drive protocol.
- **F2, option A equivalence test.** A2 had no prospectively defined test, so equivalence would have been judged
  after the Stage 1 results existed. New prerequisite A5 (before Stage 1) fixes each test, or records in advance
  that an item cannot be established.
- **F3, change of scope without a decision.** A4 let an option-A run continue to Stage 2 as a deviation when
  parity was not established. Spike §5 allows a person only to authorize a different scope. Continuing now requires
  a new scope decision (C1).
- **F4, late or missing Stage 0 items.** Under option B, no Stage 0 item froze the settings that the Stage 1 P1
  and P2 checks consume: the GFN0 selector, exact exchange and range separation, D3 form and parameters, basis and
  core treatment per element, and engine settings. B2 now includes them. A3 now covers settings the source leaves
  unstated, which are declared and recorded as deviations. M1 placed the model review "before Stage 2", later than
  B1 requires; it is now before Stage 1.
- **F5, gate conflated with authorization.** This covers ARCHITECTURE.md §2 and §3 (Section 1). Spike §8.1 also
  held the MS-000 gate pending on the missing Cowie setup and parity evidence, which are not MS-000 criteria. Both
  are corrected; those inputs remain under MS-001 faithful-reproduction readiness.
- **F6, labels.** Landscape §3 listed Pynta, tblite, autodE and KinBot as deferred, although their tool decisions
  are REJECT. The list is now split. Its sentence on removing xtb now carries the exception for a composition that
  takes its GFN0 level from xtb.
- **F7, numerical error claims.** An SCF or optimizer threshold is a stopping criterion, not an accuracy bound, so
  no tolerance may be derived from it. The numerical-convergence protocol in Section 7 does three things:
  - It separates empirical stability envelopes, measured in a new Stage 1a before any check that consumes them,
    from declared acceptance budgets.
  - It claims no rigorous error bound.
  - It gives every check pass, fail and indeterminate rules and a blocking disposition.
- **F8, in-run stopping point.** The sensitivity rule said that Stage 2 "does not proceed", although the check runs
  inside Stage 2. Section 7 now defines the checkpoints, the quarantined results, what stops, and the conditions
  for restart, including the case of unchanged settings.
- **F9, composite calibration.** The first numerical-convergence revision defined envelopes for each constituent
  level but did not define the energy and mapped-gradient envelopes consumed by the composite check or the force
  envelope at a Stage 2 branch check. Section 7 now requires direct aligned-rung calibration of the actual coupled
  energy and mapped analytic gradient, including link-host and chain-rule terms, in Stage 1a and again at the
  declared branch checkpoint. N5 and N6 require the envelope for the exact quantity they assess.

## 4. Dependency set

A tool is classified by the role it fills, not by when it is invoked:
- It is a **minimum runtime dependency** only if the proposed composition needs a role that no other required tool
  can fill without it. The roles are structure and constraint handling, an engine for each level, the coupling,
  and execution with provenance.
- It is a **validation dependency** if a gate precondition (C5, C6 or A2) requires a capability that it provides
  and no runtime tool does.
- Otherwise it is **optional**, and it stays optional whenever it is used, including in Stage 2.

The class belongs to the capability. Replacing the package that supplies it leaves the class unchanged and reopens
only the version-matched capability evidence for the replacement.

| Class | Member (proposed composition) | If omitted | Stage blocked |
|---|---|---|---|
| Minimum runtime | ASE 3.29.x: structures, atom identity, constraints, IO and driven-scan control; route R-A is part of it | No model, validation configuration or driven scan can be defined | Stage 0 onward |
| Minimum runtime | CP2K 2026.2: the ωB97X-D3 level and, unless the composition takes it from xtb, the GFN0 level; route R-B is part of it | No engine for the levels | Stage 1 onward |
| Minimum runtime | AiiDA 2.9.x with `aiida-cp2k`: execution and provenance | The provenance of [EVIDENCE-POLICY.md §4](EVIDENCE-POLICY.md#4-provenance-requirements-for-any-eventual-result-or-figure) cannot be captured, so C3 is unmet | Stage 1 (C3) |
| Minimum runtime, by selection | The coupling component selected under C2: nothing further for R-A or R-B, Py-ChemShell 25.0 for R-C. The xtb engine joins this class only if the composition fills the GFN0 role with it. | No coupled energy or force (C2 or C6 unmet), or no GFN0 level | Stage 1 (C2); Stage 2 (C6) |
| Validation | A second implementation of ωB97X-D3 (package: Psi4 1.11 or another) | The P2 cross-engine check cannot run, so C5 is unmet | Stage 2 |
| Optional | xtb CLI 6.7.x when it does not fill the GFN0 role | The cross-implementation GFN0 comparison is lost; identity provenance through CP2K is unaffected, subject to G4 | None |
| Optional (supporting analysis) | ASE NEB; Sella | Supporting fixed-z analysis (M7) is lost; ASE's optimizers already fill the minimization role | None |
| Optional (visualization) | OVITO Python module or Basic | Trajectory bond analysis and higher-quality rendering are lost; ASE renders computed coordinates | None |

## 5. Tool dispositions

| Disposition | Tool | Reason (landscape section) |
|---|---|---|
| Accepted, runtime | ASE 3.29.x | Structure, constraint and IO layer; cited by Cowie (ref 50); LGPL (§1) |
| Accepted, runtime (conditional) | CP2K 2026.2 | Documents both levels in one engine; its availability is not proof of parity (§1) |
| Accepted, runtime (conditional) | AiiDA 2.9.x with `aiida-cp2k` 2.1.1 | Job execution and provenance owner; plugin compatibility untested (§1) |
| Accepted, validation (package optional) | Psi4 1.11 | Lists ωB97X-D3; molecular only; serves the P2 check (§2) |
| Accepted, optional | xtb CLI 6.7.x | Independent GFN0 implementation with a parameter file (§1) |
| Accepted, optional | ASE NEB | Supporting analysis at fixed z; never a substitute for the driven scan (§1) |
| Accepted, optional | OVITO module or Basic (MIT) | Bond analysis and rendering; Pro not needed (§1) |
| Candidates, one to be selected in Stage 0 | ASE `SimpleQMMM` (R-A); CP2K `MIXED`/`GENMIX` (R-B); Py-ChemShell `NLayerSubtractive` (R-C) | Reuse-first subtractive composition; none shown to compose GFN0 with ωB97X-D3 for this system (§4) |
| Deferred | Sella | Optional; only for an approved saddle question (§1) |
| Deferred | xtb-python | Deprecated upstream; PyPI wheels for Linux only (§1) |
| Deferred | SCINE Chemoton and Puffin | MS-001 has no network exploration; re-evaluate at MS-004 (§1) |
| Deferred | QCFractal | Duplicates AiiDA's role; requires PostgreSQL (§1) |
| Deferred | pyiron; atomate2 | Second workflow owners; no matching workflow (§2) |
| Deferred | OpenSCAD | No MS-001 role (§1) |
| Rejected | Pynta | Metallic-surface domain; brings Fireworks and MongoDB (§1) |
| Rejected | tblite for GFN0 | The method is absent; acceptable for non-GFN0 sanity checks only (§1) |
| Rejected | autodE; KinBot | Molecular or gas-phase problem shape (§2) |

## 6. Requirement mapping

The tables of spike §3 and §4 carry the locators. Every item maps to an implementation or to an explicit gap, and
the gap column names where it closes.

| Item | Implementation (conditional) | Gap, and where it closes |
|---|---|---|
| M1 H:Si(100)-2×1 apex with IR-DB pair | ASE builders, tags | Cowie geometry `[GAP]`: A1, or a B1 `[AGENT]` model reviewed before Stage 1 |
| M2 EAOGe-C2• with legs | ASE with the engines | Coordinates and leg configuration `[GAP]`: A1 or B1 |
| M3 two-level energetics | GFN0 via CP2K `GFN_TYPE 0` or `xtb --gfn 0`; ωB97X-D3 via CP2K libxc, HF and D3; coupling R-A, R-B or R-C | P1–P3 and P3b: Stage 0 declaration (C2; A3 or B2), Stage 1 validation (C5, C6), parity only under option A (A2) |
| M4 driven approach and retraction | ASE constraints with ASE optimizers or Sella | Drive definition, and whether the model is a static scan or dynamics, unstated (P4; spike §2.9 item 6): A1 or B3 |
| M5 event order | ASE neighbour lists or OVITO on computed coordinates | Cutoffs are `[AGENT]` choices under spike §8.6 |
| M6 energy profile | Per-step energies from M3 | Cowie profile not digitized: energy signs only (E1, E5) |
| M7 barrierless relaxation | ASE NEB (climbing image) or Sella | Optional supporting analysis after M4 |
| M8 deeper-approach pathway | As M4 | Deferred to MS-003 |
| M9 STM image simulation | None required; CP2K can write cube files | Method unstated `[GAP]`; deferred |
| M10 proxy bond energies | Psi4 or CP2K | Code and ECP unstated; optional, not a gate item |
| M11 yields | Evidence bookkeeping | Cited exactly; never combined with computed results |
| M12 provenance | AiiDA with `aiida-cp2k` | Plugin compatibility untested: C3 in Stage 0, coverage report in Stage 1 (G6) |
| M13 rendering | ASE; OVITO optional | None |
| P1 GFN0 identity | Selector, banner, version and parameter provenance through the chosen route | Stage 1 (C5); parameter provenance for the CP2K route unverified (G4) |
| P2 hybrid numerics | Frozen explicit input and a molecular cross-engine check | Stage 0 declarations (A3 or B2, C7), Stage 1 (C5); parity to Cowie only under A2 |
| P3 scheme and partition | None available | Source only (A1), or a declared deviation (B2) |
| P3b coupling route | R-A, R-B, R-C | Selection C2 (Stage 0), demonstration and validation C6 (Stage 1) |
| P4 driven motion | Driven-scan protocol; NEB as supporting analysis only | A1 or B3 |

## 7. Acceptance criteria and tolerance procedure

The criteria reproduce the event sequence of the Cowie model's Fig. 3 A–D and §3. They are `[COMP-PRED]` targets:
a reproduction must show the model's sequence, not an experimental observation. Each criterion is reported as
observed, not observed or indeterminate, against a criterion recorded before Stage 1, and "bonded" is judged by the
bond-cutoff rule below.

- **E1, approach branch.** A Si–C bond forms between the tool's distal C and one Si of the IR-DB pair, with a
  concurrent decrease in total energy at that step (sign only).
- **E2, retraction branch.** The Ge–C bond breaks while the Si–C bond persists, and the Si–Si bonds at the
  anchoring Si stay intact.
- **E3, pendent C2.** After Ge–C cleavage, a pendent C2 bound to one Si exists over a finite z range near the
  EAOGe• fragment. This comprises three distinct claims, each with its own evidence and its own prospective
  criterion:
  - (i) Proximity. A declared distance criterion supports only the claim that the fragments remain close.
  - (ii) Radical character. A declared spin-population localization criterion, from the engine's own population
    analysis at declared sites, supports only the claim that unpaired-electron density resides on the pendent C2,
    on the Ge site of EAOGe•, or on both.
  - (iii) Stabilization. A declared interaction-energy criterion is required before any claim that the contact
    stabilizes the pendent. The interaction energy is the energy of the pendent-plus-tool configuration minus that
    of the same fragments at a declared non-interacting separation, both computed within the same scheme at the
    same z, or an equivalent decomposition the scheme supports.

  Proximity never supports (ii) or (iii), and radical localization never supports (iii). Each claim is
  indeterminate wherever the chosen scheme cannot provide its evidence.
- **E4, bridging.** At larger z, the pendent C2 bridges the IR-DB pair across the trough. Both Si of the pair are
  bonded to the C2, no bond forms to a neighbouring dimer's Si, and no H is abstracted from the surface.
- **E5, net energy.** The net energy change from configuration A to configuration D is negative (sign only).
- **E6, atom identity.** The two C atoms of the final IR-C2 are the tool's C2 atoms, identified by tagged index.

A failed reproduction, in which any of E1–E6 is not observed, is a valid result, and parameters are never tuned
to obtain agreement (spike §8.8).

**Terms.**
- An SCF or optimizer convergence threshold is a *stopping criterion*. It ends an iteration and is not an accuracy
  bound on the converged energy or forces. For example, the Psi4 development manual defines SCF convergence by the
  change in energy and the root-mean-square change in density between iterations
  ([engine-capability-status.md](../engine-capability-status.md#scf-convergence-controls)).
- An *empirical stability envelope* is the observed spread of a quantity under frozen, declared perturbations. It
  shows stability under those perturbations only and is not a rigorous error bound. No rigorous error bound is
  claimed anywhere in this procedure.
- An *acceptance budget* is a declared tolerance, frozen before Stage 1 and reviewed. It is a proposal, not a
  validated numerical uncertainty, and results are reported against it.

Every tolerance in spike §8.6 is fixed before Stage 1:

| Class | Quantities | How it is fixed |
|---|---|---|
| Documented stopping criterion for the exact version selected in Stage 0; under option A, the source-stated value where A1 gives one | Force convergence per accepted step; SCF convergence | Read from documentation in Stage 0. These are not accuracy bounds. |
| A cited covalent-radius tabulation and a declared multiple, re-evaluated at a smaller and a larger multiple. An observation counts only if it holds at all three multiples; otherwise it is indeterminate. | Bond cutoffs (E1, E2, E4, E6); E3(i) proximity | Declared in Stage 0 |
| Declared acceptance budget, applied through N5, N7 or N8 against measured envelopes | Finite-difference budget `B` and regime interval; P2 budgets `B_E` and `B_F`; projection budget `B_P` | Declared in Stage 0; never set or adjusted from a result |
| Envelope rule, no budget | Energy signs (E1, E5) | N6 |
| Declaration only | E3(ii) spin-localization threshold, which must hold on every accepted step in the range; E3(iii) interaction-energy threshold and reference separation, which also require E3(i) | Declared in Stage 0 and reviewed. Claims resting on them are reported against the declared value and are never presented as physically justified. |
| Rule with a checkpoint | Step-size sensitivity: the order of the E1–E4 events within the declared segment is unchanged across three z steps | Steps and segment rule declared with the drive protocol; applied at checkpoint S below |

**Numerical-convergence protocol.** Every item is declared in Stage 0, which runs no calculation. The calibration
runs form Stage 1a, and the checks that consume their outputs (Stage 1b) start only once those outputs are
recorded.

- **N1, refinement ladder.** For each engine and level, at least three rungs run from the frozen production
  settings to tighter ones. Only numerical controls that the version-matched documentation defines are changed,
  for example SCF thresholds, integration grids or density cutoffs, and integral screening. The basis, core
  treatment, functional, dispersion form, geometry, charge and multiplicity never change along a ladder. The
  coupling route also has an aligned composite ladder: at composite rung k, every constituent evaluation uses its
  declared rung k and the frozen mapping, link-host and subtractive-composition rules produce the actual coupled
  energy and mapped analytic gradient. Constituent and composite values are both recorded; a constituent envelope
  is never substituted for a composite envelope.
- **N2, same representation.** Compared values use identical atoms and coordinates from the frozen files, and the
  same charge, multiplicity, basis, core treatment, functional parameters, dispersion form and parameters, and
  electronic state. The electronic state is judged by declared diagnostics: SCF convergence, the multiplicity and
  the declared population sites. A comparison that fails N2 is not used.
- **N3, energy calibration (Stage 1a).** On each validation configuration, every constituent energy and the actual
  composite coupled energy are computed at every applicable rung; the P2 test-molecule energy is computed at every
  rung in each engine. Each production rung is repeated a declared number of times, from independent initial
  guesses where the engine permits. For each recorded object X, its direct envelope `ε_X` is the largest absolute
  difference among its production-rung repeats and between its production rung and each tighter rung. A convergence
  regime is demonstrated for X when the magnitude of the difference between successive rungs does not increase
  along its ladder. Without a demonstrated regime, X is unusable: every check that consumes it is blocked, and C5
  or C6, as applicable, is unmet until a revision is revalidated.
- **N4, force calibration (Stage 1a).** The same direct procedure is applied to every analytic force component of
  each constituent and to every component of the actual composite mapped gradient, including link-host and
  chain-rule terms, giving an object-specific envelope `φ_X`. A component is stable when the same regime condition
  holds. A constituent force envelope is never used for the composite gradient.
- **N5, finite-difference checks (Stage 1b).** For a tested gradient component of object X,
  `D(s) = [E_X(x + s) - E_X(x - s)] / (2s)` is computed at three declared steps `s = h, h/2, h/4`, with every
  displaced point satisfying N2. A constituent check uses that constituent's direct `ε_X` and `φ_X`; the composite
  check uses the direct composite `ε_X` and mapped-gradient `φ_X` from N3–N4.
  - *Derivation.* Assume `E` is smooth along the displacement, at least five times differentiable, with the
    electronic state unchanged. Taylor expansion then gives `D(s) = g + a s^2 + O(s^4)`, where `g` is the exact
    derivative and `a` is one sixth of the third derivative. The Richardson estimate
    `R = [4 D(h/2) - D(h)] / 3` therefore equals `g + O(h^4)`. The truncation remaining in `D(h/2)` is estimated by
    `T = |D(h) - D(h/2)| / 3`, which in the asymptotic regime overstates the error of `R`.
  - *Noise.* If every computed energy lies within `ε` of the smooth function, which is the working assumption N3
    supports and not a bound, then noise shifts `D(s)` by at most `ε/s` and `R` by at most `N = 3ε/h`. Truncation
    falls as `s^2` while noise grows as `1/s`.
  - *Regime.* When the leading nonzero truncation term is the stated `a s^2` term, the asymptotic regime is indicated
    when `q = [D(h) - D(h/2)] / [D(h/2) - D(h/4)]` lies in the declared interval around 4, and
    `|D(h/2) - D(h/4)|` exceeds its own noise allowance `6ε/h`. If the leading `s^2` coefficient vanishes, the
    denominator is unresolved, or the ratio indicates a different leading order, this three-step test is
    INDETERMINATE rather than PASS.
  - *Rule.* Take the allowance `U = T + N + φ`, the analytic gradient component `G` (the negative of the force) and
    the declared budget `B`.
    - PASS: the regime is indicated and `|G - R| + U <= B`.
    - FAIL: the regime is indicated and `|G - R| - U > B`.
    - INDETERMINATE: every other case.

    C5 and C6 need PASS at every tested component of every validation configuration. A FAIL rejects the scheme
    and returns the route to Stage 0. An INDETERMINATE result is blocking until a revision, with other steps or
    tighter settings, is revalidated.
- **N6, energy signs (E1, E5).** Each actual Stage 2 configuration a or b used in an energy-sign claim receives
  direct composite-energy production-rung repeats and at least one tighter aligned composite rung. Its envelope
  `ε_a` or `ε_b` is calculated by N3 from those values. The sign of the composite `ΔE` is reported only if
  `|ΔE| > ε_a + ε_b`; otherwise it is indeterminate. No constituent envelope, validation-configuration transfer
  or acceptance budget is used.
- **N7, P2 agreement.** The model chemistry is identical in both engines (N2), and a periodic engine uses a
  declared isolated-molecule treatment from its version-matched documentation.
  - Rule for the production-rung energies, with difference `ΔE`, envelopes `ε_1` and `ε_2`, and budget `B_E`:
    - PASS: `|ΔE| + ε_1 + ε_2 <= B_E`.
    - FAIL: `|ΔE| - (ε_1 + ε_2) > B_E`.
    - INDETERMINATE: otherwise.
  - Each force component is judged the same way with `φ_1`, `φ_2` and `B_F`.
  - P2 is established only if every comparison passes. If a common representation or a regime in either engine
    cannot be demonstrated, P2 cannot be established, which is blocking (C5 unmet).
  - A pass establishes internal consistency only. Two engines that share a definitional error would still agree,
    which is why P2(a) checks each input against the primary definition.
- **N8, constraint projection.** Recorded values are compared. The output format and its rounding rule are declared
  before Stage 1; half a unit in the last recorded digit is used only for round-to-nearest. For truncation or
  another formatting rule, `r` is the full interval that rule permits.
  - Fixed-atom coordinates must be identical in the output before and after a constrained step, and the gradient
    components the constraints remove must be zero in the recorded projected gradient. Otherwise the check fails.
  - The retained components are compared with the analytic gradient after the constraints are applied, computed
    independently from the same recorded gradient. Let the difference be `Δ`, let `r` be the combined
    formatting-dependent allowance defined immediately above, and let `B_P` be the declared budget.
    - PASS: `|Δ| + r <= B_P`.
    - FAIL: `|Δ| - r > B_P`.
    - INDETERMINATE (blocking): otherwise.

Where a quantity cannot be resolved, the outcome is INDETERMINATE and blocking as stated, never a pass. This
covers a missing regime or common representation, a noise-limited difference and an unresolvable recorded
precision. The acceptance budgets, like the E3 thresholds, are declarations: results are reported against them,
and they are never presented as physically justified or as validated uncertainties. No tolerance, budget, ladder
or step is chosen or adjusted from a result of this program. The results that enter the rules, namely the Stage 1a
envelopes and the Stage 2 re-measurements, are measurements consumed by rules fixed in advance.

**Stage 2 checkpoints.** Each driven branch carries two checkpoints, whose configurations and segments are chosen
by rules declared in C7. At each one, propagation of that branch pauses until the check is complete and recorded.
- *Branch check.* A driven step can converge to an electronic state that depends on its history, so the
  constituent and composite checks (N5) are repeated at the declared visited configuration of each branch. Direct
  constituent and composite energy and force envelopes are re-measured there with the production-rung repeats and
  one tighter aligned rung (N3, N4); N5 uses the envelopes for the exact constituent or composite quantity it
  checks. Every actual Stage 2 configuration used in an E1 or E5 energy difference also receives the direct
  composite-energy measurements required by N6. PASS releases the branch.
- *Sensitivity check.* Checkpoint S is reached when the base-step scan of a branch has accepted the last step of
  its declared segment, for example the steps around the first event detected on that branch at the base step. The
  segment is re-run from the base-step configuration at its first step with the declared coarser and finer z
  steps, and the order of the E1–E4 events within it, judged by the cutoff rule, is compared across the three
  steps. An unchanged order releases the segment.
- *Quarantine.* A changed or indeterminate sensitivity result, or a failed or indeterminate branch check,
  quarantines results:
  - For a sensitivity result, every accepted step of the branch from the segment's first step onward.
  - For a branch check, the whole branch.
  - Every later branch that starts from a quarantined step. The retraction branch starts where the approach branch
    ends.
  - The checkpoint's own runs.
  - Everything derived from these results: E1–E6 determinations, energy signs, the M6 profile and M7 analyses.

  Steps before a quarantined span, and all Stage 1 results, are unaffected. Propagation of every quarantined branch
  stops, and no analysis uses quarantined results except to report them as quarantined.
- *Restart.* A quarantined branch restarts only through the revision sequence below. That means fresh approval of
  the changed settings or steps, the affected branches re-run from their first steps, and every checkpoint
  repeated. With settings unchanged there is no restart. Re-running identical settings cannot change a recorded
  outcome and is never used to seek a different one. The quarantined results remain as records, reported only as
  step-size-sensitive or as failing the branch check, and every E-criterion that depends on them is reported
  indeterminate on that ground. They are never released later; a revision produces new results beside them.

After freezing, a value or definition changes only through this revision sequence (spike §8.6):
1. A recorded reason that does not refer to agreement with the paper. A validation tolerance or budget is never
   relaxed to turn a recorded failure or indeterminate result into a pass. A demonstrated error in its recorded
   basis is corrected with the failure retained.
2. Fresh approval by the same roles as the original selection.
3. Revalidation of everything the old value governed. The driven scan is history-dependent, so a changed per-step
   criterion invalidates the rest of the branch. That branch is re-run from its first step, together with the
   sensitivity segments.
4. Retention of superseded results, with both outcomes reported.

A quarantine at a Stage 2 checkpoint is the declared trigger on which the force-convergence value, the production
settings or the z step may be tightened through this sequence. A frozen definition that fails in Stage 1, such as
a coupling route that fails its demonstration, returns to Stage 0 under the same sequence. Diagnostic runs under
spike §8.8 are additional runs and never replace a frozen-setup result.

## 8. Stage preconditions for scope options A and B

Neither option is selected. The identifiers are those of spike §8.3.

| Point | Both options | Option A: faithful reproduction | Option B: declared-deviation study |
|---|---|---|---|
| Before Stage 0 | C1: a person selects and authorizes the option, and the decision is recorded separately from the MS-000 gate and from document acceptance | A1: source inputs obtained through an authorized channel: model geometry with atom identities, partition, embedding and links, charge and spin, basis/ECP and dispersion parameters, drive protocol and per-step criteria, and software identities. None is available now (G1). | Nothing beyond C1 |
| Stage 0 work | No chemistry calculations. The only execution is the C3 provenance wiring test, which is a software check. | Freeze the source inputs; define the equivalence tests | Define the models, scheme, level settings and drive protocol |
| Before Stage 1 | C2: a coupling route selected and fully specified. C3: provenance capture tested on a trivial AiiDA job against the frozen §4 field set. C4: tolerances, acceptance budgets and the numerical-convergence protocol (N1–N8) declared and approved. C7: validation set, P2 test molecule and Stage 2 checkpoint rules frozen. Reviewer approval of every Stage 0 definition. | A3: inputs frozen and hashed as source-provided; any setting the source leaves unstated is declared and recorded as a deviation. A5: an equivalence test per P1–P4, approved in advance, or an advance record that the item cannot be established. | B1: models M1 and M2 frozen, hashed and labelled `[AGENT]`. B2: scheme and settings of both levels declared as an `[AGENT]` deviation, Reviewer-approved. B3: drive protocol, including the sensitivity steps and segment rule, Reviewer-approved. |
| Stage 1 work | Stage 1a: calibration ladders and repeats (N1–N4) on every validation configuration for every constituent evaluation and for the direct composite coupled energy and mapped gradient, and on the P2 test molecule in both engines. Stage 1b, using only recorded Stage 1a outputs: P1 identity; P2 check (N7); constituent and composite finite-difference checks (N5) and constraint projection (N8) on the validation set; provenance coverage. | The A5 tests (Stage 1b) | No parity test |
| Before Stage 2 | C5: a regime demonstrated in Stage 1a for every constituent, the direct composite, and the P2 test molecule in both engines; P1 identity captured; P2 established with a second ωB97X-D3 implementation and a common representation; and coverage complete. C6: composite coupled gradient validated. Stage 1 results reviewed, and every change since freezing made through the revision sequence. | A2: the result of each test recorded. A4: if any item is not established, the run is not a faithful reproduction, and continuing requires a new scope decision (C1). | B4: parity to Cowie recorded as unknown for every item and carried into every result |
| Stage 2 work | Driven scan (M4–M6) with the branch and sensitivity checkpoints (Section 7), then optional M7 on results that are not quarantined | A result can be `[COMP-REPRO]` only if every item is established and provenance and review are complete | A result is at most `[COMP-PRED]` under this program's setup |

## 9. Unresolved gaps

None of these gaps bears on the MS-000 gate. Each is an MS-001 precondition or a limitation of one.

- **G1. Cowie source inputs and Supplementary Information.** The paper states that the SI is provided on request
  [S1]. Only the authors can supply it, through an authorized channel. Option A needs it (A1).
- **G2. Parity for P1–P4.** Closed by the A5 tests run in Stage 1 on A1 inputs (A2). It cannot close without G1.
- **G3. Coupling route (P3b).** The `UNVERIFIED` items of
  [landscape §4.4 and §5](OPEN-SOURCE-LANDSCAPE.md#5-what-was-not-verified-in-this-landscape-summary-of-unverified-fields)
  are open. Closed by version-matched documentation for the selection (C2) and by the Stage 1 demonstration and
  composite validation (C6).
- **G4. GFN0 parameter provenance through CP2K.** The P1 evidence includes parameter provenance. Local records
  establish it for the xtb parameter file [S-xtb-param-gfn0] but not for CP2K's internal GFN0 [S-cp2k-xtb]. Closed
  by version-matched CP2K documentation or source in Stage 0. If CP2K exposes no parameter identity, either P1 for
  that route records the field as missing, which leaves C5 unmet, or the composition takes GFN0 from the xtb
  engine, which then becomes a runtime dependency.
- **G5. P2 comparability and functional definition.**
  - Whether the selected engines can evaluate the test molecule with an identical model chemistry (basis and core
    treatment) and, for a periodic engine, an isolated-molecule treatment is unverified. If this cannot be
    demonstrated, P2 cannot be established and Stage 2 is blocked (N7).
  - The engines' dispersion defaults differ: CP2K's pair-potential default is `DFTD3(BJ)` [S-cp2k-vdw], while the
    installed Psi4 build configures ωB97X-D3 through `d3zero2b` (SOURCES.md [22]). The frozen input must therefore
    declare the form and parameters rather than inherit either default.
  - The ωB97X-D3 definition paper (Cowie ref 47) has not been retrieved.
  - The Psi4 entry's equivalence to the benchmark functional is open.

  Closed by the Stage 0 declarations (C7; A3 or B2), drawn from version-matched documentation and the primary
  functional paper.
- **G6. Provenance path.** Compatibility of `aiida-cp2k` with the eventual input is untested (M12), and the §4
  field set is provisional ([EVIDENCE-POLICY.md §6](EVIDENCE-POLICY.md#6-the-schema-is-provisional)). The
  project's use of AiiDA 2.9.2 to store the E-01 records (SOURCES.md [12]) is record storage, not the C3 test.
  Closed by C3 in Stage 0 and the coverage report in Stage 1.
- **G7. Installation.** Of the required tier, only ASE has been installed for MS-000, and only for an import and
  file-round-trip test. The conda-forge record of CP2K 2026.2 lists no osx-arm64 build [S-conda-cp2k], while
  CP2K's installation page reports that Apple Silicon is regularly tested [S-cp2k-install]. Closed by an
  installation record with version-matched capability evidence, under an authorized scope option.
- **G8. Remaining landscape fields.** The other `UNVERIFIED` fields of landscape §5 are closed field by field from
  official sources. None is a gate item.

## 10. Basis of this record

This record was prepared from the package as published in the previous export, the E-01 records under
`results/e01/`, [engine-capability-status.md](../engine-capability-status.md) and [SOURCES.md](../SOURCES.md).

No source was retrieved for it. Retrieval was considered for two planning gaps:
- The documented optimizer and SCF defaults behind finding A. That gap is closed by a rule whose values must be
  cited from documentation for the version selected in Stage 0, so a retrieval now would bind the plan to a
  version not yet selected.
- The numerical method of finding F7. Its finite-difference and Richardson relations are derived in Section 7
  from a Taylor expansion under stated assumptions. The statement that a stopping criterion is not an accuracy
  bound rests on the repository's capability record. The engines' numerical controls must be cited for the
  version selected in Stage 0 (N1).

No calculation, installation or smoke test was run, and no remote link was re-checked.

The following were changed with this record:
- the compute spike: the status line, §3 (M1), §5 and §8.1 to §8.7
- the architecture record: §1, §2, §3 and §6
- the landscape: the Psi4 decision and §3
- the package index
- the repository README, AGENTS.md, the research state and the export manifest
