# Research state

This file is **public** like the rest of the repository. It tracks the program's intended end state, its evidence
gates, the current qualified status, open issues and the next bounded work.
- **It records scientific status only.** It is not authorization for any agent or person to act (see
  [AGENTS.md](../AGENTS.md)).
- **Aims are not accomplishments.** Everything in §1 is an aim, not an existing capability and not permission to
  execute.
- **Currency:** last updated 2026-09-23, initial public export.

## 1. Full intended end state (research aims)

1. **Engine and method validation** on well-defined species. The first case is the benchmark's molecular tool in
   its iodinated and activated forms.
2. **Mechanical trajectories and a validated primitive library.** Model tool approach, contact and retraction
   along controlled coordinates, for example C2 donation to an inter-row dangling-bond pair on H:Si(100). Each
   validated event becomes a library primitive with explicit inputs, observables and validity limits.
3. **Reproducible pathway evaluation.**
   - Energy landscapes along mechanical coordinates, with complete provenance.
   - Sensitivity to approach depth, step size, lateral offset and tool conformation.
   - Multi-step targets, such as extending C2 to C4.
   - Competing and off-target channels (hydrogen or silicon abstraction, alternative products), each as its own
     hypothesis.
4. **From target structure to build plan.** Compile a target structure into candidate build sequences
   (a dependency graph of primitive operations).
5. **Verification, failure and repair.** Detect and verify each step; model failures, repair and yield; and
   account for correlated errors instead of assuming independence.
6. **Parallel scheduling.** Schedule operations under dependencies, mutual exclusions and resource limits.
7. **Industrial throughput and cost studies.** Treated strictly as research hypotheses until supported by
   evidence.
8. **Manufacturing visualization.** Keep a hard line between renderings of computed atomic coordinates and
   conceptual illustrations.

Faithful reproduction of the benchmark would require the benchmark authors' coordinates, QM/MM partition, drive
protocol and supplementary material (`[GAP]`). The authors state the supplementary material is available on
request; this project has not obtained it.

## 2. Acceptance and evidence gates

- **Pathway reproduction gates, in order:**
  1. The **IR-C2 pathway reproduction** must be independently accepted before any IR-C2 → IR-C4 extension.
  2. **Both** pathway reproductions (IR-C2, and IR-C2 → IR-C4) must be independently accepted before any
     mechanical perturbation study (approach depth, step size, lateral offset, tool conformation).
  3. **The first novel-chemistry question,** only after those reproduction gates: the reproducible **off-target
     C2-donation outcome** reported by Cowie et al., and the competing mechanisms proposed for it.
  4. **Build-planning (compiler) and manufacturing studies** require validated primitives.
- **E-01 does not satisfy these gates.** The donor-only E-01 engine validation checks an engine setup on free
  donor candidates. It is **not** a pathway reproduction and satisfies none of the gates above.
- **Human approval of each phase.** Moving to a new research phase requires explicit human approval, separate
  from every scientific gate. A passed scientific gate does not imply it.
- **Evidence classes and provenance fields.** Every result must meet [docs/evidence-policy.md](../docs/evidence-policy.md).
  Missing provenance blocks the label.
- **Capability gate.** Each engine feature needs version-matched primary evidence for the exact version used.
  Without it, dependent criteria are INDETERMINATE, never PASS.
- **Method gate.** Open specification questions are resolved by technical review before any run. Thresholds are
  preserved, and a method change is decided explicitly, never substituted.
- **Outcome rules.** E-01 outcomes follow [docs/e01-method-specification.md](../docs/e01-method-specification.md).
  Engine validation and the localization hypothesis are reported separately.
- **Independent review.** Every result is independently reviewed and bound to exact file hashes. Document
  acceptance, a scientific gate and authorization are separate, and no one of them implies another.

## 3. Current qualified status

| Area | Status |
|---|---|
| Quantum-chemistry results | **None.** No reviewed energies, forces, gradients or populations exist in project evidence. |
| Donor candidates | Two agent-proposed, unoptimized ETKDG embeddings with stable atom IDs. Counts and electron parity were re-derived from the files. Not compared with the benchmark authors' supplementary coordinates, which have not been obtained. Donor identity rests on literature statements as recorded in the original reconstruction notes; unverified in the current review. |
| Surface models | Three definitions: ASE-lattice construction, unoptimized, with placeholders. Coordinate files are not published. |
| First experiment (E-01) | Prospective specification with open clarifications; **not run**. Project records show an earlier preparation attempt ended blocked before engine installation. |
| Engine | Psi4 1.11 selected; **not installed or validated** in project evidence. |
| Engine capabilities | Mostly **UNVERIFIED** for 1.11 (see [docs/engine-capability-status.md](../docs/engine-capability-status.md)). |
| Functional identity | **Open.** The v1.11 source declares the `wB97X-D3` entry; its dependencies and literature equivalence are unresolved. |
| Compute-environment controls | A recorded process-containment "failure" was an intentional negative control: the expected detection of a descendant process, followed by cleanup. The accepted reassessment explains it, and no rerun is implied. Enforcement of resource limits at full workload scale remains **unverified**. |

## 4. Completed source inspection

The full index, with links, locators and verification basis, is in [docs/SOURCES.md](../docs/SOURCES.md).

- **Benchmark preprint (v1):** attribution, setup, reported counts and the proposed-mechanism sections (see
  [docs/benchmark.md](../docs/benchmark.md)). Also the arXiv listings of two related preprints.
- **Psi4 development manual (`1.12a1.dev35`):** sections on SCF reporting and convergence, stability analysis,
  Löwdin spins, basis assignment with effective core potentials, and the `WB97X-D3` row.
- **Psi4 `v1.11` source:**
  - the stability root-following check in `proc.py`
  - `libxc_functionals.py`, retrieved once and verified to the expected Git blob, inspected only for the
    `wB97X-D3` entry

## 5. Known unresolved issues

- **Engine capabilities:** analytic gradients with an effective core potential, unrestricted Kohn–Sham ⟨S²⟩,
  per-label basis/ECP assignment, Löwdin spins and convergence controls are unverified for 1.11. So are basis
  coverage, the iodine core-electron count, and direct-inversion Kohn–Sham stability coverage (no stability
  criterion is used).
- **Functional dependencies:**
  - the Libxc `HYB_GGA_XC_WB97X_D3` definition
  - the Psi4 driver consumer of the functional list
  - the `d3zero2b` dispersion implementation and its availability
  - the primary literature parameters
- **Method clarifications:**
  - whether the precursor also runs unrestricted, and its guess set
  - the exact finite-difference atom and species
  - whether the per-species budget suffices
  - how to proceed if ⟨S²⟩ is unavailable
- **Donor identity:** the original reconstruction notes record a mismatch between a printed mass-spectrometry
  formula in their cited source and the name-derived graph. The mismatch is recorded, not corrected, and it is
  unverified in the current review.
- **Workload-scale enforcement:** resource-limit enforcement at workload scale is unverified.
- **Qualified historical records:** some earlier agent sessions in this project had a process-isolation problem,
  in which context from outside the project could have entered those sessions. Records from those sessions are
  treated as potentially influenced. They are used only as qualified data and re-checked against primary sources
  where possible. No claim is made that they were unaffected.

## 6. Next bounded work

These are ordered by dependency, not by date.

1. **Version-matched evidence for Psi4 1.11,** covering each capability above: tagged source files, or the
   installed package's own documentation and basis files.
2. **Functional identity,** resolved against Libxc, the dispersion implementation and primary literature, with
   any mismatch escalated as a method decision.
3. **Method clarifications** above, settled through technical review.
4. **Workload-scale enforcement** of resource limits, verified.
5. **Only then, and only with authorization:** a bounded engine installation and the E-01 run, reported against
   the specification whatever the outcome, including blocked or failed.

## 7. Update policy

- **When to update:** whenever evidence, status or open issues change, with the date and a one-line summary
  below.
- **Status only moves with evidence:** it changes only on new evidence meeting the policy, never on restatement.
- **Keep the history:** superseded statements are corrected in place and noted here, not silently removed.

| Date | Change |
|---|---|
| 2026-09-23 | Initial public export of the research state |
