# Research state

This file is public, like the rest of the repository. It records the intended end state of the research, its
evidence gates, the current qualified status, the open issues and the next bounded work. It records scientific
status only. It is not authorization for any agent or person to act ([AGENTS.md](../AGENTS.md)). The intended
capabilities described in Section 1 are aims. They are neither accomplished capabilities nor permission to
execute. The file was last updated on 2026-09-23.

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
| Quantum-chemistry results | None. No reviewed energies, forces, gradients or populations exist in project evidence. |
| Donor candidates | Two agent-proposed, unoptimized ETKDG embeddings with stable atom identifiers. Counts and electron parity were re-derived from the files. Not compared with the benchmark authors' supplementary coordinates, which have not been obtained. The donor identity rests on literature statements as recorded in the original reconstruction notes and is unverified in the current review. |
| Surface models | Three definitions, built on an ASE lattice, unoptimized, with placeholders. Coordinate files are not published. |
| First calculation (E-01) | Prospective specification with open clarifications; not run. Project records show that an earlier preparation attempt ended blocked before engine installation. |
| Engine | Psi4 1.11 selected; not installed or validated in project evidence. |
| Engine capabilities | Mostly `UNVERIFIED` for 1.11 ([docs/engine-capability-status.md](../docs/engine-capability-status.md)). |
| Functional identity | Open. The v1.11 source declares the `wB97X-D3` entry; its dependencies and its equivalence to the literature functional are unresolved. |
| Compute-environment controls | A recorded process-containment "failure" was an intentional negative control: the expected detection of a descendant process, followed by cleanup. The accepted reassessment explains it, and no rerun is implied. Enforcement of resource limits at full workload scale remains unverified. |

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

## 5. Known unresolved issues

- **Engine capabilities.** Several capabilities are unverified for Psi4 1.11: analytic gradients with an effective
  core potential, ⟨S²⟩ reporting for unrestricted Kohn–Sham references, per-label basis and core-potential
  assignment, Löwdin spins and convergence controls. So are basis coverage, the iodine core-electron count and the
  direct-inversion coverage of Kohn–Sham stability analysis; no stability criterion is used.
- **Functional identity.** Four dependencies remain unresolved: the Libxc definition of `HYB_GGA_XC_WB97X_D3`, the
  Psi4 driver code that consumes the functional list, the implementation and availability of the `d3zero2b`
  dispersion, and the parameters given in the primary literature.
- **Method specification.** Four clarifications are open: whether the precursor also runs unrestricted and with
  which guess set, the exact atom and species sampled by the finite-difference check, whether the per-species
  budget suffices, and how to proceed if ⟨S²⟩ is unavailable.
- **Donor identity.** The original reconstruction notes record a mismatch between a printed mass-spectrometry
  formula in their cited source and the name-derived graph. The mismatch is recorded rather than corrected and is
  unverified in the current review.
- **Resource limits.** Enforcement of resource limits at workload scale is unverified.
- **Historical records.** Some earlier agent sessions in this project had a process-isolation problem, in which
  context from outside the project could have entered those sessions. Records from those sessions are treated as
  potentially influenced. They are used only as qualified data and are re-checked against primary sources where
  possible. No claim is made that they were unaffected.

## 6. Next bounded work

The following steps are ordered by dependency, not by date.

1. Version-matched evidence for Psi4 1.11 covering each capability listed above, from tagged source files or from
   the installed package's own documentation and basis files.
2. Resolution of the functional's identity against Libxc, the dispersion implementation and the primary
   literature, with any mismatch escalated as a decision about method.
3. Settlement of the open method clarifications through technical review.
4. Verification of resource-limit enforcement at workload scale.
5. Only after these steps, and only with authorization, a bounded engine installation and the E-01 run. The run is
   reported against the specification whatever its outcome, including a blocked or failed outcome.

## 7. Update policy

The file is updated whenever evidence, status or open issues change, and each update is logged below with its
date and a one-line summary. A status changes only on new evidence that meets the evidence policy, never on
restatement. Superseded statements are corrected in place and noted in the log rather than removed silently.

| Date | Change |
|---|---|
| 2026-09-23 | Initial public export of the research state |
| 2026-09-23 | Editorial revision into continuous prose; no change of scientific status, gates or open issues |
