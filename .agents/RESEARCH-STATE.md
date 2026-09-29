# Research state

This file is public, like the rest of the repository. It records the intended end state of the research, its
evidence gates, the current qualified status, the open issues and the next bounded work. It records scientific
status only. It is not authorization for any agent or person to act ([AGENTS.md](../AGENTS.md)). The intended
capabilities described in Section 1 are aims. They are neither accomplished capabilities nor permission to
execute. The file was last updated on 2026-09-29 for the pre-run determination of the wiring test W1.

## 1. Intended end state

The research aims at a reviewed and reproducible computational capability for mechanically controlled chemistry,
built in stages.
- **Engine and method validation.** The first stage validates engines and methods on well-defined species, the
  first case being the benchmark's molecular tool in its iodinated and activated forms.
- **Validated primitive library.** Tool approach, contact and retraction are modelled along controlled
  coordinates, for example C2 donation to an inter-row dangling-bond pair on H:Si(100). Each validated event
  becomes a library primitive with explicit inputs, observables and limits of validity.
- **Pathway evaluation.** Reproducible evaluation covers energy landscapes along mechanical coordinates with
  complete provenance, and their sensitivity to approach depth, step size, lateral offset and tool conformation.
  It extends to multi-step targets, such as the extension of C2 to C4. Competing and off-target channels, such as
  hydrogen or silicon abstraction and alternative products, are each treated as separate hypotheses.
- **Build planning.** Beyond single events, the aims include:
  - compilation of a target structure into candidate build sequences, as a dependency graph of primitive
    operations
  - verification of each step, with modelling of failures, repair and yield, including correlated errors rather
    than an assumption of independence
  - parallel scheduling of operations under dependencies, mutual exclusions and resource limits
- **Manufacturing studies.** Industrial throughput and cost studies are treated strictly as research hypotheses
  until evidence supports them. Visualizations of manufacturing keep a firm distinction between renderings of
  computed atomic coordinates and conceptual illustrations.

A faithful reproduction of the benchmark would require the benchmark authors' coordinates, QM/MM partition, drive
protocol and supplementary material (`[GAP]`). The authors state that the supplementary material is available on
request; this project has not obtained it.

## 2. Acceptance and evidence gates

The pathway reproduction gates apply in the following order.

1. The IR-C2 pathway reproduction must be independently accepted before any extension from IR-C2 to IR-C4.
2. Both pathway reproductions, IR-C2 and the extension from IR-C2 to IR-C4, must be independently accepted before
   any study of mechanical perturbation (approach depth, step size, lateral offset or tool conformation).
3. The first novel-chemistry question, which is addressed only after those reproduction gates, is the reproducible
   off-target C2-donation outcome reported by Cowie et al., together with the competing mechanisms proposed for it.
4. Build-planning (compiler) and manufacturing studies require validated primitives.

The donor-only engine validation of E-01 checks an engine setup on free donor candidates. It is not a pathway
reproduction and satisfies none of these gates. Moving to a new research phase requires explicit human approval,
which is separate from every scientific gate; passing a scientific gate does not imply it.

Every result must also satisfy [docs/evidence-policy.md](../docs/evidence-policy.md), and missing provenance blocks
its label. The remaining gates are:
- **Capability gate.** Each engine feature requires version-matched primary evidence for the exact version used.
  Without it, dependent criteria are INDETERMINATE, never PASS.
- **Method gate.** Open questions in a specification are resolved by technical review before any run. Thresholds
  are preserved, and a change of method is decided explicitly rather than substituted.
- **Outcome rules.** The outcomes of E-01 follow
  [docs/e01-method-specification.md](../docs/e01-method-specification.md), with engine validation and the
  localization hypothesis reported separately.
- **Review.** Each result is reviewed independently and bound to exact file hashes. Document acceptance, a
  scientific gate and authorization are separate, and no one of them implies another.

## 3. Current qualified status

| Area | Status |
|---|---|
| Quantum-chemistry results | None converged. The only attempt, E-01, stopped before any SCF iteration was reported, and no converged electronic energies, forces, gradients or populations exist in project evidence. E-01 is closed as technically BLOCKED and scientifically INDETERMINATE, and every chemistry-dependent result remains INDETERMINATE. |
| Donor candidates | Two agent-proposed, unoptimized ETKDG embeddings with stable atom identifiers. Counts and electron parity were re-derived from the files. Not compared with the benchmark authors' supplementary coordinates, which have not been obtained. The donor identity rests on literature statements as recorded in the original reconstruction notes and is unverified in the current review. |
| Surface models | Three definitions, built on an ASE lattice, unoptimized, with placeholders. Coordinate files are not published. A separate MS-001 Stage 0 build-site cluster, M1, is published in [structures/ms-001](../structures/ms-001/README.md). It is geometric and unrelaxed, `[AGENT]`, and not a model of the benchmark geometry. |
| First calculation (E-01) | Executed once on 2026-09-24 under a reviewed configuration ([results/e01](../results/e01/README.md)). The precursor stopped at its first SCF job when Psi4 aborted during integral setup with `PSIO_ERROR: 17 (Incorrect block start address)`; every dependent criterion is INDETERMINATE. The activated donor is blocked and unrun. The cause is undiagnosed: a source-level postmortem and a bounded, read-only static survey of the installed build identified no cause, and no exact executable diagnostic could be specified from the evidence obtained ([results/e01/postmortem.md](../results/e01/postmortem.md)). The attempt is closed as technically BLOCKED and scientifically INDETERMINATE, a disposition that is terminal for the attempt as run. An earlier preparation attempt, which ended blocked before engine installation, remains part of the history. |
| Engine | Psi4 1.11 installed from conda-forge in a project-local environment. The installation and basis construction were checked and the configured dispersion route was exercised in a dispersion-only check; no SCF completed. |
| Engine capabilities | Partly established for the installed build: installation, basis construction with the iodine core potential and the functional composition as printed; the configured dispersion route was exercised in a dispersion-only check. SCF behaviour, analytic gradients, ⟨S²⟩ and Löwdin spins remain `UNVERIFIED` ([docs/engine-capability-status.md](../docs/engine-capability-status.md)). A static survey of the installed build recorded the availability of some input/output library names; that is name availability only, not ABI compatibility, initialization or callability, and the installed type widths remain unresolved. |
| Functional identity | Open. The installed build runs the `wB97X-D3` entry through Libxc 7.1.2; the installed `libxc_functionals.py` differs from the v1.11 tag at the TH-FL entry only. Equivalence to the literature and benchmark functional is unresolved. |
| Compute-environment controls | A recorded process-containment "failure" was an intentional negative control: the expected detection of a descendant process, followed by cleanup. The accepted reassessment explains it, and no rerun is implied. In E-01 the sampled resource and cleanup controls recorded the precursor job within the envelope with verified cleanup; these are sampled observations and cooperative limits, not hard containment. |
| Result records | The E-01 preparation and run records were stored with verified digests in the project's provenance system. This is record-keeping, not a scientific result. |
| MS-000 feasibility package | The complete public adaptation is versioned under [docs/ms-000](../docs/ms-000/README.md). It records the benchmark extraction, conditional minimum stack, open parity gaps, evidence policy, source ledger, and ASE smoke test. Its [closure record](../docs/ms-000/CLOSURE.md) disposes the six feasibility criteria that form the MS-000 gate: all six are met, including independent scientific review of the plan, and the gate is PASS. MS-001 faithful-reproduction readiness remains BLOCKED on missing source inputs and missing parity and coupling evidence. A person has since authorized scope option B for Stage 0 only (next row). |
| MS-001 Stage 0 (scope option B) | Authorized by a person for Stage 0 only, on 2026-09-26 ([C1](../docs/ms-001/C1-AUTHORIZATION.md)). Option A is not authorized and remains BLOCKED; parity is unknown for every item. The Stage 0 definitions are recorded in [docs/ms-001](../docs/ms-001/README.md). The independent review of this package recorded the canonical decision REJECT, substantively REVISE: C1 was accepted, and C2, C3, C4, C7, B1, B2 and B3 were returned for correction, with C3 readiness BLOCKED. A renewed review of the corrected package again recorded REJECT and required five further corrections. Further independent reviews each recorded REJECT for one remaining defect, first the checkpoint S comparison and then the persistence of E3, and each was corrected. The latest independent review recorded the canonical decision APPROVE for the corrected definition package, and Lead acceptance is recorded. On 2026-09-27 a person approved C4, the tolerances and numerical-convergence protocol, bound to its exact SHA256 ([approval record](../docs/ms-001/C4-HUMAN-APPROVAL.md)), and Stage 0 is closed as a set of frozen prospective definitions ([freeze record](../docs/ms-001/STAGE0-FREEZE-RECORD.md)). The acceptance and the approval cover definitions only and are neither readiness nor physical validation: C3 readiness remains BLOCKED, N8 has not been run, P1, P2, P3b, C5 and C6 remain unestablished, and every model, setting and threshold stays `[AGENT]`. Those definitions are: the provenance wiring test on one trivial non-chemistry job, which finished with exit status 0; the coupling-route selection, CP2K `MIXED`/`GENMIX`, with P3b open; the two-level declaration; the drive protocol; tolerances and the numerical-convergence protocol; and the validation set, with geometries built geometrically and unrelaxed. No chemistry calculation was run, and Stage 1 has not started, is BLOCKED and is not authorized. *Updated 2026-09-28:* in one decision a person approved a revision of C4 that defines N8 as fixed-atom checks, with consequential revisions of B3, C2 and C7, and the declaration of the dftd4 source for G4 in B2 §3 ([N8 approval record](../docs/ms-001/C4-HUMAN-APPROVAL-02.md); [G4 approval record](../docs/ms-001/B2-G4-HUMAN-APPROVAL.md)). N8 has not been run, and its Stage 1 observations are outstanding. The G4 declaration settles the source-definition part of G4, and P1 identity provenance remains within Stage 1. *P2 build approval, 2026-09-28:* a person approved a revision of B2 that declares, in B2 §6, the Psi4 build that P2 uses, and, in the same decision, C4, B3, C2 and C7 at their unchanged digests with the revised B2 adopted ([P2 build approval record](../docs/ms-001/B2-P2-BUILD-HUMAN-APPROVAL.md)). It settles the selection of the P2 build only; basis normalization remains partially established, and the build provenance and runtime conformance of the compiled Psi4 steps remain open. *W1, 2026-09-29:* a person authorized the wiring test W1, and a pre-run executability determination recorded it as W1 BLOCKED before execution ([W1 record](../docs/ms-001/W1-PRE-RUN-DETERMINATION.md)). There are two independent blockers: the Stage 0 interpreter's environment holds a name outside the declared allow-list, and the tracked-driver declaration conflicts with the no-delivery boundary. The capture of ignored or private sources is unresolved. W1 was not run; no AiiDA profile, computer, code or job was created, and no chemistry was done. No C3 blocker is closed, C3 readiness remains BLOCKED, and the specification is unchanged. |

## 4. Completed source inspection

The full catalogue, with links, locators and verification basis, is in [docs/SOURCES.md](../docs/SOURCES.md).
- **Benchmark preprint (v1).** The sections giving attribution, setup, reported counts and the proposed mechanism
  have been inspected ([docs/benchmark.md](../docs/benchmark.md)), together with the arXiv listings of two related
  preprints.
- **Psi4 development manual (`1.12a1.dev35`).** The inspected sections cover SCF reporting and convergence,
  stability analysis, Löwdin spins, basis assignment with effective core potentials, and the `WB97X-D3` row.
- **Psi4 `v1.11` source.** The stability root-following check in `proc.py` was inspected. The file
  `libxc_functionals.py` was retrieved once, verified against the expected Git blob, and inspected only for the
  `wB97X-D3` entry.
- **Installed build and E-01 run.** Package identities and selected installed files were hashed, and the engine
  output and error text of the E-01 attempt were preserved ([results/e01](../results/e01/README.md)).
- **Psi4 `v1.11` input/output and conventional-integral source (E-01 postmortem).** The input/output library
  files, the conventional (PK) integral manager and the Python binding of the input/output library were read at
  the `v1.11` tag, with the line locators recorded in the project's private capture records. The reading is
  source-conditional and does not establish the code of the installed binary
  ([results/e01/postmortem.md](../results/e01/postmortem.md)).
- **Installed build, statically surveyed.** A single bounded, read-only static inspection of the installed build
  captured four input/output library headers in full and recorded the export trie and symbol table of the core
  extension library. It read files and ran standard inspection utilities; it compiled nothing, linked nothing,
  loaded nothing from the build and executed nothing from it. Its absence statements are scoped to the 1 791 of
  6 260 package file names that it enumerated.

## 5. Known unresolved issues

- **E-01 engine abort.** The precursor's first SCF job aborted during conventional (PK) integral setup with
  `PSIO_ERROR: 17 (Incorrect block start address)`. The cause is undiagnosed, and the attempt is closed as
  technically BLOCKED and scientifically INDETERMINATE. The postmortem keeps three ranked hypotheses open: a block
  or entry inconsistency in the integral input/output path; a filesystem, capacity or operating-system
  input/output condition, which the inspected source text does not support as the direct source of code 17, while
  an indirect contribution is neither shown nor excluded; and a workload-dependent trigger, which overlaps the
  first. A conditional source-level pathway inside the first hypothesis is possible in the source but has not been
  shown to have occurred; it is not established as the cause and is neither established nor excluded. Disk capacity
  remains a live possible contributor, neither established nor excluded. The observed scratch allocation exceeded
  the pre-run estimate. The activated donor is unrun.
- **Installed-build interfaces.** Whether any diagnostic could link against and call the installed input/output
  code is unresolved. The entry points of the input/output handler class were not found among the exported names,
  the installed widths D = sizeof(double) and I = sizeof(int) are unresolved, and ABI compatibility, the standalone
  setup order and callability are not established. The ranked gaps are listed in
  [results/e01/postmortem.md](../results/e01/postmortem.md), Section 8.
- **Engine capabilities.** Several capabilities remain unverified for the installed Psi4 1.11, because no SCF
  completed: SCF convergence behaviour, analytic gradients with an effective core potential, ⟨S²⟩ reporting for
  unrestricted Kohn–Sham references and Löwdin spins. The direct-inversion coverage of Kohn–Sham stability analysis
  is also unresolved; no stability criterion is used. Basis construction, including the iodine core-electron count
  of 46, is established for the installed build.
- **Functional identity.** Three dependencies remain unresolved: the Libxc 7.1.2 definition of
  `HYB_GGA_XC_WB97X_D3`, the Psi4 driver code that consumes the functional list, and the parameters given in the
  primary literature. The `d3zero2b` dispersion route is configured through simple-dftd3 in the installed build and
  was exercised in a dispersion-only check.
- **MS-001 Stage 0 open items.** None is claimed. The corrected Stage 0 definitions have independent review approval
  and Lead acceptance, and C4 has human approval (2026-09-27); none of these settles any item below. The items are
  sorted by when they must be settled.
  - **Prerequisites to starting Stage 1.**
    - A separate Stage 1 authorization. Independent review approval and Lead acceptance of the corrected Stage 0
      items, and the human approval of C4 ([approval record](../docs/ms-001/C4-HUMAN-APPROVAL.md)), are recorded;
      they authorize nothing.
    - The C3 blockers. C3 is a reviewed partial demonstration. It showed two provenance fields on the trivial job
      and five by surrogate. Among the five, atom identity is surrogate coverage only: it is stored in separate nodes
      that are not inputs of the job, and its survival along a chain of jobs is unverified. It did not demonstrate
      four: calculation performed, failure record, review record and retained-per-claim. The prerequisite blockers
      are identity-chain survival, the remaining provenance extensions and the login-shell environment gap.
      *Updated 2026-09-27:* a proposed wiring test W1 that could close them is specified, awaiting its own
      authorization ([C3-WIRING-TEST-PROPOSAL.md](../docs/ms-001/C3-WIRING-TEST-PROPOSAL.md)). The blockers stand.
      *Updated 2026-09-29:* W1 was authorized by a person and was blocked before execution by a pre-run
      determination ([W1 record](../docs/ms-001/W1-PRE-RUN-DETERMINATION.md)), for two independent reasons with one
      further requirement unresolved. W1 was not run. It closes none of the blockers, which all stand.
    - Definitions still to settle from version-matched source: GFN0 parameter provenance through CP2K (G4); CP2K's
      unit for `OMEGA`; the normalization of single-primitive basis coefficients; the printed representations
      compared by N8, which stays BLOCKED until both compared representations and the combined formatting allowance
      r of C4 row 10 are defined; and whether the compiled Psi4 SCF and gradient steps use any fitting basis under
      the declared settings. *Updated 2026-09-27:* the
      [source resolution record](../docs/ms-001/SOURCE-RESOLUTION.md#3-dispositions) gives these dispositions.
      - `OMEGA` (CP2K's unit and conversion semantics only) and the compiled Psi4 steps (tagged-source behaviour
        only) are established from version-matched source.
      - G4, normalization and the N8 representations are partially established. The remaining pieces are the
        dftd4 source to be declared, the Libint2 version of the Psi4 build, and, for N8, the rounding of formatted
        output and a definitional question in C4 row 10.
      - Options for that question are recorded as a proposal, not applied
        ([C4-PROPOSED-REVISION-01.md](../docs/ms-001/C4-PROPOSED-REVISION-01.md)).
      - The installed Psi4 binary's build provenance and runtime conformance remain open.
      - This prerequisite still does not hold. N8 remains BLOCKED and has not been run.
      - *Updated 2026-09-27, pre-Stage-1 closure packet*
        ([PRESTAGE1-CLOSURE-PACKET.md](../docs/ms-001/PRESTAGE1-CLOSURE-PACKET.md)):
        - The installed Psi4 build of E-01 carries Libint2 2.13.1, by its package record, and the installed header
          defines the same normalization. The recipe records of both packages remain unread, so normalization stays
          partially established.
        - A declaration of the dftd4 source for G4 and a decision packet on N8, with option O2 recommended, are
          prepared as proposals. They are not applied and not approved.
        - This prerequisite still does not hold.
      - *Updated 2026-09-28:* in one decision a person approved a revision of C4 that defines
        N8 as fixed-atom checks and the declaration of the dftd4 source for G4 in B2 §3
        ([N8 approval record](../docs/ms-001/C4-HUMAN-APPROVAL-02.md);
        [G4 approval record](../docs/ms-001/B2-G4-HUMAN-APPROVAL.md)). N8 is no longer blocked
        by its definition; it has not been run, and its Stage 1 observations are outstanding. The source-definition
        part of G4 is settled; P1 identity provenance remains within Stage 1. Basis normalization remains partially
        established, so this prerequisite still does not hold.
      - *P2 build approval, 2026-09-28:* a person approved the declaration of the Psi4 build that P2 uses in B2 §6,
        with the fresh adoption of the revised B2 by C4, B3, C2 and C7
        ([P2 build approval record](../docs/ms-001/B2-P2-BUILD-HUMAN-APPROVAL.md)). It settles the selection of the
        build only. Basis normalization remains partially established, and the build provenance and runtime
        conformance of the compiled Psi4 steps remain open, so this prerequisite still does not hold.
  - **Dependencies within Stage 1.**
    - CP2K installation and build identity, including the libxc version it links.
    - The undocumented route capabilities: link atoms and mixed methods in CP2K `MIXED`, the numerical mixing
      derivative, GFN0 under open-shell settings and ωB97X-D3 exact exchange in GAPW.
    - Mulliken spin populations for E1 inside `MIXED`.
    - The remaining N2 representation checks.
  - **Stage 2 gates.**
    - C5, whose P2 part also needs the defining ωB97X-D3 reference, which was not obtained.
    - C6 (the coupling route, P3b; N5 and N8).
    - B4, parity unknown.
  - **Declared deviations and indeterminate claims.**
    - CP2K hard-codes the D3 zero-damping sr8 = 1.0, which the declaration uses as a declared deviation from the
      tabulated 1.094.
    - E3(iii) is INDETERMINATE by declaration, because no reference keeps both the imposed d and the reported D − z0
      fixed.
    - E3's minimum persistence, Δd_min = 0.20 Å of imposed d, is an arbitrary `[AGENT]` declaration without physical
      validation.

  Two environment deviations of Stage 0 are recorded ([C3 §1](../docs/ms-001/C3-PROVENANCE-WIRING.md#1-environment)).
- **Method specification.** The four clarifications that were open before the run were settled by review
  ([results/e01/method-config.json](../results/e01/method-config.json)).
- **Donor identity.** The original reconstruction notes record a mismatch between a printed mass-spectrometry
  formula in their cited source and the name-derived graph. The mismatch is recorded rather than corrected and is
  unverified in the current review.
- **Resource limits.** Resource limits are enforced by sampled observation and cooperative thread settings, not
  hard containment. One E-01 job exercised them at workload scale for 852 s.
- **Historical records.** Some earlier agent sessions in this project had a process-isolation problem, in which
  context from outside the project could have entered those sessions. Records from those sessions are treated as
  potentially influenced. They are used only as qualified data and are re-checked against primary sources where
  possible. No claim is made that they were unaffected.

## 6. Next bounded work

**W1 pre-run determination, 2026-09-29.** A person authorized the wiring test W1. A pre-run executability
determination found that W1 cannot be executed to a pass as specified within that authorization, and recorded
**W1 BLOCKED before execution** ([W1 record](../docs/ms-001/W1-PRE-RUN-DETERMINATION.md);
[outcome](../docs/ms-001/w1-outcome.json)).
- **W1-BLOCKER-E2.** Under the declared five-variable environment, the Stage 0 interpreter's `os.environ` holds a
  sixth name, `__CF_USER_TEXT_ENCODING`, observed in the startup probes and inherited by child processes. The cause
  is an `[AGENT]` inference.
- **W1-BLOCKER-E1.** The declaration that both drivers are tracked at a commit cannot be met without a commit, and
  none is authorized.
- **U-F1P.** The capture of ignored or private source files has no established conforming design, because the
  environment lies in the repository's ignored area.

W1 was not run. No AiiDA profile, computer, code or job was created, and no chemistry, engine run, calculation or
installation took place. The specification, C4 and every frozen definition are unchanged. No C3 blocker is closed.

The next bounded step is a proposal for a person's decision: a revision of the W1 specification, with the options
recorded in the W1 record, none applied. Its executability would then be determined again before any run, under
whatever authorization a person gives. F9 remains a dependency within Stage 1, F10 remains with the orchestration layer, and F11
carries labels only. Basis normalization remains PARTIALLY ESTABLISHED, and Psi4 runtime conformance remains open.
Stage 1 remains BLOCKED; Stages 1, 1a, 1b and 2 remain unauthorized, and option A stays BLOCKED. The paragraphs
below are historical where they state that W1 awaits or requires authorization. W1 remains unrun.

**P2 build declaration approved, 2026-09-28.** In one decision a person approved the declaration of the Psi4 build
that P2 uses in B2 §6, the exact conda-forge `osx-arm64` package `psi4-1.11-py314h53d0584_1` with its exactly
pinned Libint package, and C4, B3, C2 and C7 at their unchanged digests with the revised B2 adopted
([P2 build approval record](../docs/ms-001/B2-P2-BUILD-HUMAN-APPROVAL.md)). The approval settles the selection of
the build only. Basis normalization remains PARTIALLY ESTABLISHED; build provenance, runtime conformance and the P2
runtime identity observations remain open. W1 remains unrun and requires separate authorization; C4-j and B3-b
remain deferred. Stage 1 remains BLOCKED; Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized; option A
stays BLOCKED. The paragraph below on the decision packet is historical and is superseded for current status by
this update.

**P2 build-declaration decision packet, 2026-09-28 (proposal only).** The next documentary step named by the recipe
audit is prepared: a [decision packet](../docs/ms-001/P2-PSI4-BUILD-DECISION-PACKET.md), with its
[source ledger](../docs/ms-001/P2-PSI4-BUILD-SOURCE-LEDGER.md), for a person's decision on whether to declare the exact
conda-forge `osx-arm64` package `psi4-1.11-py314h53d0584_1`, with its exactly pinned Libint package, as the Psi4 build
that P2 uses. It recommends approval as an `[AGENT]` proposal. An approval would settle the selection of the build
only, would change B2's whole-file digest and would need a fresh adoption of the revised B2 by C4, B3, C2 and C7 under
C4 §3. No build is declared, and no option is chosen, approved or applied. Basis normalization remains PARTIALLY
ESTABLISHED; build provenance, runtime conformance and the P2 runtime identity observations remain open. W1 remains
unrun and requires separate authorization; C4-j and B3-b remain deferred. Stage 1, Stage 1a, Stage 1b and Stage 2
remain unauthorized; option A stays BLOCKED.

**Recipe audit update, 2026-09-28.** The [recipe metadata audit](../docs/ms-001/RECIPE-METADATA-AUDIT.md) closes
reading the two retained package recipes. `[LIT]` metadata establishes declared source/patch/build identities and
Psi4's exact Libint host and run pin. Normalization remains PARTIALLY ESTABLISHED; actual compilation/binary
provenance and runtime conformance remain open. The next bounded documentary step can be preparation of a separate
human P2 build-declaration decision package (`[AGENT]` recommendation), carrying those gaps rather than waiving them.
No P2 build is declared or approved here. W1 remains unrun and requires separate authorization; C4-j and B3-b remain
deferred. Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized; option A stays BLOCKED. Earlier dated recipe
work items below are historical and are superseded for current status by this update.

The MS-000 gate is PASS, with all six feasibility criteria met, including independent scientific review of the
plan ([closure record §2](../docs/ms-000/CLOSURE.md#2-gate-disposition)). The pass selects and authorizes nothing.
A person has since made the MS-001 scope decision:
- **Option B, Stage 0 only.** Scope option B, the declared-deviation study, is authorized for Stage 0 only
  ([C1](../docs/ms-001/C1-AUTHORIZATION.md)).
- **Option A.** Faithful reproduction is not authorized and remains blocked until the source coordinates and
  methods are obtained and parity evidence exists.

The Stage 0 definitions are recorded in [docs/ms-001](../docs/ms-001/README.md). Independent review approval and
Lead acceptance of the corrected Stage 0 items are recorded in the
[freeze record](../docs/ms-001/STAGE0-FREEZE-RECORD.md), and a person approved C4 on 2026-09-27
([approval record](../docs/ms-001/C4-HUMAN-APPROVAL.md)). Stage 0 is closed as a set of frozen prospective
definitions; the closure authorizes nothing. The next bounded work is:
1. Settling, from version-matched source, the definitions that are prerequisites to starting Stage 1: G4, the unit
   of `OMEGA`, basis normalization, the N8 representations, with them the combined formatting allowance r of N8, and
   the compiled Psi4 fitting-basis steps. Closing the C3 blockers, which needs a new wiring test under its own
   authorization. *Updated 2026-09-27:* the source reading is done as far as version-matched source permits
   ([source resolution record](../docs/ms-001/SOURCE-RESOLUTION.md)). What remains of this item:
   - a declaration of the dftd4 source for G4 through the revision sequence;
   - a static read, under its own authorization, of the Libint2 version and the build record of the installed
     Psi4;
   - a human decision under C4 §3 on N8's definition, from the options recorded as a proposal;
   - the C3 blockers.

   *Updated 2026-09-27:* the [pre-Stage-1 closure packet](../docs/ms-001/PRESTAGE1-CLOSURE-PACKET.md) takes these
   as far as static reading allows:
   - The static read of the installed build is done, except for its packages' recipe records.
   - The G4 declaration and the N8 decision are proposals awaiting a person's decision under C4 §3.
   - W1, the wiring test for the C3 blockers, is specified and awaits its own authorization.

   *Updated 2026-09-28:* the G4 declaration and the N8 decision are taken: in one decision a
   person approved both ([N8 approval record](../docs/ms-001/C4-HUMAN-APPROVAL-02.md);
   [G4 approval record](../docs/ms-001/B2-G4-HUMAN-APPROVAL.md)). N8 has not been run; its
   Stage 1 observations and the P1 identity provenance of G4 belong to Stage 1. The read of the installed build's
   recipe records and W1 remain.
2. Only after a separate authorization, Stage 1: installing CP2K and running the calibration and
   method-validation calculations of Stage 1a and 1b, including the demonstration of the coupling route.

Stage 1 has not started, and this update authorizes nothing.

The steps listed here earlier have been completed, closed or left as proposals, as follows. E-01 is closed, and
no step of it is pending.

1. The tabulation of what the existing E-01 records contain was completed in the postmortem. The records give no
   failing byte offset, no address representation and no mapping from the integral batch index to an address.
2. The optional filesystem-only probe was not performed and is not pending. It would inform only the storage path
   it tests and would not exercise the engine's integral or input/output code.
3. The source-informed diagnostic of the engine's input/output path was carried as far as the evidence allows. A
   source-level postmortem and a bounded, read-only static survey of the installed build were completed, and no
   exact executable diagnostic could be specified from the evidence obtained; this is a statement about the
   current evidence and does not assert that a diagnostic is impossible. A narrower replay through the exported
   low-level `PSIO::write` was declined, because it would exercise only the exported block-start guard and would not
   test the installed `AIOHandler` restart-versus-append behaviour, which is the mechanism at issue.
4. A revised configuration, for example a different SCF algorithm with a named auxiliary basis, or the same
   algorithm on storage verified for the required file sizes, remains a proposal. It would be a new calculation,
   reviewed before any run, rather than a continuation of E-01.
5. Resolution of the functional's identity against Libxc 7.1.2 and the primary literature, with any mismatch
   escalated as a decision about method, remains a proposal.

Any future attempt should sample scratch free space and file sizes through to termination and record the sampling
interval. The activated donor is not to be used as a diagnostic.

## 7. Update policy

The file is updated whenever evidence, status or open issues change, and each update is logged below with its
date and a one-line summary. A status changes only on new evidence that meets the evidence policy, never on
restatement. Superseded statements are corrected in place and noted in the log rather than removed silently.

| Date | Change |
|---|---|
| 2026-09-23 | Initial public export of the research state |
| 2026-09-23 | Editorial revision into continuous prose; no change of scientific status, gates or open issues |
| 2026-09-24 | E-01 executed once and stopped (engine abort during integral setup; activated donor unrun). Superseded in place: the statements that E-01 had not been run, that Psi4 was not installed and that the method clarifications were open. Capability, functional-identity, resource and next-work entries updated on the new evidence. |
| 2026-09-24 | E-01 closeout recorded. A source-level postmortem and a static survey of the installed build identified no cause, no exact executable diagnostic could be specified, a narrower guard-only replay was declined, and the attempt is closed as technically blocked and scientifically indeterminate. Superseded in place: next-work steps 1 to 3, now recorded as completed or closed. Status, source-inspection and open-issue entries updated on the closeout records. |
| 2026-09-24 | The complete public MS-000 feasibility package was added under `docs/ms-000/`; its PENDING scientific gate and the existing E-01 status are unchanged. |
| 2026-09-24 | MS-000 closure recorded in `docs/ms-000/CLOSURE.md`. Six feasibility criteria form the MS-000 gate. All six are met, including independent scientific review of the plan, and the gate is PASS. MS-001 faithful-reproduction readiness remains BLOCKED on missing source inputs and missing parity and coupling evidence. Human authorization of MS-001 is absent, and no scope option is selected. The compute spike's MS-001 protocol was corrected for forward dependencies and missing Stage 0 items. It gained a numerical-convergence protocol with a Stage 1a calibration, direct composite calibration, and defined Stage 2 checkpoints. The architecture's gate language was separated from authorization. Superseded in place: the MS-000 row, which now gives the disposition of each criterion, and the next-work paragraph. E-01 status unchanged. |
| 2026-09-26 | A person authorized MS-001 scope option B for Stage 0 only, and the Stage 0 package was recorded in `docs/ms-001/` and `structures/ms-001/`. It holds a provenance wiring test on one trivial non-chemistry job, a coupling-route selection with P3b open, a two-level declaration, a drive protocol, tolerances, a validation set and geometrically built unrelaxed geometries. Every definition is PENDING review and approval, and no chemistry calculation was run. Superseded in place: the statement in the MS-000 row that MS-001 authorization was absent and no scope option was selected, and the next-work paragraph. Option A remains BLOCKED, and E-01 status is unchanged. |
| 2026-09-26 | Independent review of the MS-001 Stage 0 package: canonical decision REJECT, substantively REVISE. C1 was accepted; C2, C3, C4, C7, B1, B2 and B3 were returned for correction, and C3 readiness is BLOCKED. The required corrections were made without any calculation or geometry regeneration. Among them: deterministic sensitivity windows; N8 BLOCKED pending its representation; an operational electronic-state rule; E3(iii) INDETERMINATE by declaration; frozen effective convergence controls; the dispersion-input contract read from source; and C3 recorded as a reviewed partial demonstration. Superseded in place: the MS-001 Stage 0 row, the open-items entry (atom identity is now classed as surrogate coverage) and the next-work list. Stage 1 stays BLOCKED and option A stays BLOCKED. |
| 2026-09-26 | Renewed independent review of the MS-001 Stage 0 package: canonical decision REJECT. Five further corrections were made without any calculation or geometry regeneration. The Psi4 guess and fitting-basis settings were declared from version-matched source, with the compiled steps `UNVERIFIED` and added as a prerequisite to starting Stage 1. The geometric Si–C trigger that controls the drive was separated from event E1, which keeps its N6 energy criterion. The zero-accepted-step case was defined as blocking. A source-count wording was corrected, and the freeze record and export manifest were rebound. Superseded in place: the MS-001 Stage 0 row, the open-items entry and the next-work list. Stage 1 stays BLOCKED and option A stays BLOCKED. |
| 2026-09-26 | Independent review approval of the corrected MS-001 Stage 0 definition package, and Lead acceptance recorded. Further independent reviews had recorded REJECT for the checkpoint S comparison and then for the persistence of E3; both were corrected without any calculation or geometry regeneration, and the latest independent review recorded the canonical decision APPROVE. Human approval of C4 remains PENDING, so Stage 0 is not closed. This update is status-only: no definition, evidence label or gate changed. Stage 1 stays BLOCKED and unauthorized, C3 readiness and N8 stay BLOCKED, option A stays BLOCKED and MS-000 remains a feasibility PASS only. P1, P2, P3b, C5 and C6 remain unestablished, and E3's minimum persistence Δd_min = 0.20 Å remains an arbitrary `[AGENT]` declaration without physical validation, as the declared-deviations list now states. Superseded in place: the MS-001 Stage 0 row, the open-items entry and the next-work list. |
| 2026-09-27 | A person approved C4, the tolerances and numerical-convergence protocol of MS-001 Stage 0, as the prospective numerical protocol of scope option B, Stage 0, bound to commit `bd3d16a5173b19e3461817171487a106eea3173c` and SHA256 `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`, with the records C4 references as they stood at that commit. The decision is recorded in `docs/ms-001/C4-HUMAN-APPROVAL.md`, and Stage 0 is closed as a set of frozen prospective definitions. C4 is byte-identical; its opening Approval bullet, which still reads PENDING, is retained as the frozen text of the approved bytes and superseded by the approval record. The one gate that changed is the human approval of C4. No scientific or readiness gate, definition or evidence label changed: Stage 1 stays BLOCKED and unauthorized, C3 readiness and N8 stay BLOCKED, option A stays BLOCKED and MS-000 remains a feasibility PASS only. P1, P2, P3b, C5 and C6 remain unestablished, and Δd_min = 0.20 Å remains an arbitrary `[AGENT]` declaration without physical validation. Superseded in place: the date line, the MS-001 Stage 0 row, the open-items entry and the next-work list, whose first item, the human approval of C4, is removed as completed. Earlier log rows are kept as written; their PENDING statements were accurate on their dates. |
| 2026-09-27 | Source resolution of the five definitions required before Stage 1, from version-matched CP2K 2026.2 release source, Psi4 v1.11 tagged source and Libint v2.8.1 (`docs/ms-001/SOURCE-RESOLUTION.md`). `OMEGA` (CP2K's unit and conversion semantics) and the compiled Psi4 steps (tagged-source behaviour) are established; G4, basis normalization and the N8 representations are partially established. CP2K writes no separate, direct record of the gradient `GEO_OPT` uses; whether a force record can serve as N8's record (i) is recorded as a definitional question, with options for a decision under C4 §3 in `docs/ms-001/C4-PROPOSED-REVISION-01.md`, not applied and not approved. C4 is byte-identical; B2 received dated annotations only; no value, label, gate or dependency changed. Stage 1 stays BLOCKED and unauthorized; N8 stays BLOCKED and has not been run. Superseded in place, with dates: the open-items entry on the five definitions and next-work item 1. |
| 2026-09-27 | Pre-Stage-1 closure packet (`docs/ms-001/PRESTAGE1-CLOSURE-PACKET.md` and five companion records). A static audit of the installed E-01 Psi4 build identifies Libint2 2.13.1 by package record, with the same header-defined normalization; the packages' recipe records could not be read, so normalization stays partially established. A proposed dftd4 declaration for G4 finds byte-identical dftd4 4.2.0 source files in the two CP2K-hosted archives, patched by one toolchain route and not the other, and a dependency-resolution gap. An N8 decision packet recommends option O2. A non-chemistry wiring test W1 for the C3 blockers is specified. Every proposal is unapplied and awaits a person's decision or a separate authorization; no frozen record, definition, label or gate changed. Stage 1 stays BLOCKED and unauthorized. Updated in place, with dates: the C3-blockers and five-definitions open items and next-work item 1. |
| 2026-09-28 | In one decision, in an answer recorded on 2026-09-27, a person approved a revision of C4 that defines N8 as fixed-atom checks, option O2 of the N8 decision packet, with the consequential revisions of B3, C2 and C7, and a revision of B2 that declares the dftd4 source for G4 in B2 §3: the tblite 0.6.0 archive with its bundled dftd4 4.2.0, the CP2K 2026.2 patches and dependency resolution from the bundled sources, with a fail-closed configure record. Each revision is bound to its exact SHA256 (`docs/ms-001/C4-HUMAN-APPROVAL-02.md`; `docs/ms-001/B2-G4-HUMAN-APPROVAL.md`). The six Stage 1 observations on which N8 depends are stated in C4. C4's opening Approval bullet is unchanged and still reads PENDING; the approval records supersede it for the status of human approval. N8 has not been run, and its Stage 1 observations are outstanding. The retained-component comparison and its budget B_P are no longer used by N8, a change of coverage and not a relaxation. The source-definition part of G4 is settled; P1 identity provenance, including the loaded parameter bytes and the linked dftd4 library, remains within Stage 1, and the `[GAP]` of G4 for P1 stands. Nothing was built, linked, installed or run. No evidence label, other definition or gate changed. Stage 1 stays BLOCKED and unauthorized, and C3 readiness and option A stay BLOCKED. Updated in place, with dates: the date line, the MS-001 Stage 0 row, the open item on the five definitions and next-work item 1. |
| 2026-09-28 | Installed recipe metadata audit completed as a static software-provenance supplement. Both retained archives and info members match prior digests; recipes identify declared source digests, patches, variants and requirements, including the exact Libint package in both Psi4 host and run requirements. Normalization remains PARTIALLY ESTABLISHED, compiled-binary provenance and runtime conformance remain open. A separate P2 build-declaration decision package can be prepared, but no declaration is made. New evidence is in companion records; human-adopted references and protocol bytes remain unchanged. W1 remains unrun, C4-j and B3-b deferred, all later stages unauthorized and option A BLOCKED. |
| 2026-09-28 | P2 Psi4 build-declaration decision packet and source ledger prepared as a proposal for a person's decision (`docs/ms-001/P2-PSI4-BUILD-DECISION-PACKET.md`). The candidate is the exact conda-forge `osx-arm64` package `psi4-1.11-py314h53d0584_1` with its exactly pinned Libint package `libint-2.13.1-h5a0831b_0`, each identified by archive SHA256; approval is recommended as an `[AGENT]` proposal, with exact candidate text for B2 §6 and a revision map that includes a fresh adoption of the revised B2 by C4, B3, C2 and C7. The E-01 stop in PK integral setup is recorded without inference about the declared DIRECT route in either direction. No build is declared and nothing is applied; B2, C4 and every approval record are unchanged. Basis normalization remains PARTIALLY ESTABLISHED. W1 remains unrun, C4-j and B3-b deferred, all later stages unauthorized and option A BLOCKED. |
| Approval recorded 2026-09-28 | In one decision, in an answer recorded on 2026-09-28, a person approved a revision of B2 that declares, in B2 §6, the Psi4 build that P2 uses: the exact conda-forge `osx-arm64` package `psi4-1.11-py314h53d0584_1` with its exactly pinned Libint package `libint-2.13.1-h5a0831b_0`, each identified by archive SHA256. In the same decision C4, B3, C2 and C7 were approved at their unchanged digests with the revised B2 adopted, each record bound to its exact SHA256 (`docs/ms-001/B2-P2-BUILD-HUMAN-APPROVAL.md`). The approval settles the selection of the P2 build only. C4, B3, C2 and C7 are byte-identical; C4's opening Approval bullet is unchanged and still reads PENDING, and C4-j and B3-b remain deferred. Basis normalization remains PARTIALLY ESTABLISHED; build provenance, runtime conformance and the P2 runtime identity observations remain open. E-01 remains technically BLOCKED and scientifically INDETERMINATE and is not evidence about P2 in either direction. Nothing was built, installed or run. No evidence label, other definition or gate changed. W1 remains unrun. Stage 1 stays BLOCKED and unauthorized, Stages 1a, 1b and 2 remain unauthorized, and C3 readiness and option A stay BLOCKED. The date in the first column is the date on which the approval was recorded. This update was made after that date and carries no date of its own. Updated in place: the date line, the MS-001 Stage 0 row, the open item on the five definitions and the next-work section. |
| 2026-09-29 | A person authorized the wiring test W1. A pre-run executability determination recorded it as W1 BLOCKED before execution (`docs/ms-001/W1-PRE-RUN-DETERMINATION.md`, with `docs/ms-001/w1-outcome.json`). There are two independent blockers: under the declared five-variable environment the Stage 0 interpreter's `os.environ` holds a sixth name, whose cause is an `[AGENT]` inference, and the declaration that both drivers are tracked at a commit conflicts with the no-delivery boundary. The capture of ignored or private sources is unresolved. W1 was not run: no AiiDA profile, computer, code or job was created, and nothing was calculated, installed or retrieved. The specification, C4 with its opening Approval bullet and every frozen definition are unchanged; proposed revisions are recorded for a person's decision and none is applied. No C3 blocker is closed, and C3 readiness remains BLOCKED. F9, F10 and F11, basis normalization and Psi4 runtime conformance are unchanged. Stage 1 stays BLOCKED and unauthorized, and option A stays BLOCKED. Updated in place: the date line, the MS-001 Stage 0 row, the C3-blockers open item and the head of Section 6. |
