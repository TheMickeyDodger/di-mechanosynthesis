# Research state

This file is public, like the rest of the repository. It records the intended end state of the research, its
evidence gates, the current qualified status, the open issues and the next bounded work. It records scientific
status only. It is not authorization for any agent or person to act ([AGENTS.md](../AGENTS.md)). The intended
capabilities described in Section 1 are aims. They are neither accomplished capabilities nor permission to
execute. The file was last updated on 2026-09-24.

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
| Quantum-chemistry results | None converged. The only attempt, E-01, stopped before any SCF iteration was reported, and no converged electronic energies, forces, gradients or populations exist in project evidence. |
| Donor candidates | Two agent-proposed, unoptimized ETKDG embeddings with stable atom identifiers. Counts and electron parity were re-derived from the files. Not compared with the benchmark authors' supplementary coordinates, which have not been obtained. The donor identity rests on literature statements as recorded in the original reconstruction notes and is unverified in the current review. |
| Surface models | Three definitions, built on an ASE lattice, unoptimized, with placeholders. Coordinate files are not published. |
| First calculation (E-01) | Executed once on 2026-09-24 under a reviewed configuration ([results/e01](../results/e01/README.md)). The precursor stopped at its first SCF job when Psi4 aborted during integral setup with `PSIO_ERROR: 17 (Incorrect block start address)`; every dependent criterion is INDETERMINATE. The activated donor is blocked and unrun. The cause is undiagnosed. An earlier preparation attempt, which ended blocked before engine installation, remains part of the history. |
| Engine | Psi4 1.11 installed from conda-forge in a project-local environment. The installation and basis construction were checked and the configured dispersion route was exercised in a dispersion-only check; no SCF completed. |
| Engine capabilities | Partly established for the installed build: installation, basis construction with the iodine core potential and the functional composition as printed; the configured dispersion route was exercised in a dispersion-only check. SCF behaviour, analytic gradients, ⟨S²⟩ and Löwdin spins remain `UNVERIFIED` ([docs/engine-capability-status.md](../docs/engine-capability-status.md)). |
| Functional identity | Open. The installed build runs the `wB97X-D3` entry through Libxc 7.1.2; the installed `libxc_functionals.py` differs from the v1.11 tag at the TH-FL entry only. Equivalence to the literature and benchmark functional is unresolved. |
| Compute-environment controls | A recorded process-containment "failure" was an intentional negative control: the expected detection of a descendant process, followed by cleanup. The accepted reassessment explains it, and no rerun is implied. In E-01 the sampled resource and cleanup controls recorded the precursor job within the envelope with verified cleanup; these are sampled observations and cooperative limits, not hard containment. |
| Result records | The E-01 preparation and run records were stored with verified digests in the project's provenance system. This is record-keeping, not a scientific result. |

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

## 5. Known unresolved issues

- **E-01 engine abort.** The precursor's first SCF job aborted during conventional (PK) integral setup with
  `PSIO_ERROR: 17 (Incorrect block start address)`. The cause is undiagnosed. The ranked, untested hypotheses are
  a large-file or block-address failure in the PK input/output path, a scratch capacity or other filesystem
  condition, and a trigger specific to the precursor. The observed scratch allocation exceeded the pre-run
  estimate, and disk exhaustion at the abort is neither established nor excluded. The activated donor is unrun.
- **Engine capabilities.** Several capabilities remain unverified for the installed Psi4 1.11, because no SCF
  completed: SCF convergence behaviour, analytic gradients with an effective core potential, ⟨S²⟩ reporting for
  unrestricted Kohn–Sham references and Löwdin spins. The direct-inversion coverage of Kohn–Sham stability analysis
  is also unresolved; no stability criterion is used. Basis construction, including the iodine core-electron count
  of 46, is established for the installed build.
- **Functional identity.** Three dependencies remain unresolved: the Libxc 7.1.2 definition of
  `HYB_GGA_XC_WB97X_D3`, the Psi4 driver code that consumes the functional list, and the parameters given in the
  primary literature. The `d3zero2b` dispersion route is configured through simple-dftd3 in the installed build and
  was exercised in a dispersion-only check.
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

The following steps are ordered by dependency, not by date. They are proposals; none has been executed or
authorized.

1. Tabulate what the existing E-01 records contain and state explicitly what they lack: no failing byte offset, no
   address representation and no mapping from the integral batch index to an address.
2. Optionally, a single filesystem-only probe on the same storage within stated limits on size, free space and
   time. It would not exercise the engine's integral or input/output code, so it cannot resolve the engine-specific
   question.
3. A separately authorized, source-informed diagnostic of the engine's own PK input/output path. Completing steps 1
   and 2, even with a successful probe, does not resolve the shared risk.
4. Only afterwards, a revised configuration proposal, for example a different SCF algorithm with a named auxiliary
   basis, or the same algorithm on storage verified for the required file sizes, each reviewed before any run.
5. Resolution of the functional's identity against Libxc 7.1.2 and the primary literature, with any mismatch
   escalated as a decision about method.

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
