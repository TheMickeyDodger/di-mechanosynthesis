# H2 fixed-separation RHF/STO-3G method specification

## Status

This is a prospective [AGENT] specification with status NOT_RUN: it authorizes nothing, it is not readiness, no proposed setting is a measured capability, and every engine-option statement is open until checked for the exact installed build.

## How to read the labels

The class of the underlying evidence is assigned first. A statement taken from a source's concept, with its locator, is [LIT]; proposals and the reasoning of this document itself are [AGENT]. Operational statuses and software failure records, such as the gates and the E-01 record, carry no chemistry class and do not acquire one from a source number.

## Purpose

This specification describes the first fixed-separation calculation that the lesson [lesson-01-fixed-separation-scf.md](lesson-01-fixed-separation-scf.md) prepares for. Its machine-readable parameterization is [h2-method-parameters.json](h2-method-parameters.json).

## System

The system is neutral H2 [AGENT]: charge 0, multiplicity 1, two electrons, with atom map H1 at (0, 0, -R/2) and H2 at (0, 0, +R/2) on the z axis. R is a fixed job parameter: the nuclei never move within a job, so no fixed-atom or optimizer settings apply.

## Units

Input coordinates are in bohr, so the nuclear repulsion V_NN = 1/R in hartree needs no unit conversion [AGENT]. Angstrom values, where given, are for orientation only, converted with the CODATA 2022 Bohr radius [51].

## Energy convention

E_elec excludes V_NN and includes the electron kinetic energy, and the Born-Oppenheimer energy is E_BO = E_elec + V_NN [AGENT]. The run records the engine's reported total energy and the reported nuclear repulsion separately; which energy the engine's total is stays open until shown for the exact build, and E_elec is derived only after that. V_NN is never added twice [AGENT].

## Electronic model

RHF with the STO-3G basis. [50] shows one contracted s function per H, so H2 has two basis functions and the variational space can be counted by hand [LIT]. This choice is made for transparent arithmetic; its limits are discussed in [lesson-01-fixed-separation-scf.md](lesson-01-fixed-separation-scf.md) [AGENT].

## Proposed engine options

Every line below is a proposal [AGENT]; version semantics are OPEN unless noted.

- `reference rhf` — single determinant for a closed-shell singlet.
- `basis sto-3g` — rationale in Electronic model [50] [LIT].
- `guess core` — set explicitly: core Hamiltonian start, no electron repulsion [48, Initial Guess] [LIT].
- `scf_type direct` with `df_scf_guess false` — exact integrals, no fitting basis. This pairing is PARTIAL: read from the version-matched v1.11 source for P2 in section 8 of [../../ms-001/SOURCE-RESOLUTION.md](../../ms-001/SOURCE-RESOLUTION.md) [31] and declared in section 6 of [../../ms-001/B2-METHOD-DECLARATION.md](../../ms-001/B2-METHOD-DECLARATION.md) [30, 39] [LIT].
- `e_convergence 1e-8` and `d_convergence 1e-8` — set explicitly because defaults depend on calculation type [48, Convergence and Algorithm Defaults] [LIT]. Which quantity the D_CONVERGENCE test measures is version-specific and OPEN: [48, Initial Guess] describes a root-mean-square density-matrix change, while the example output on the same page labels the column RMS |[F,P]|, a commutator residual [LIT]; it must be checked for the exact build (P2) [AGENT].
- `maxiter 50` — fixed iteration cap for every job.
- `fail_on_maxiter true` — non-convergence becomes a hard failure instead of a silent result.
- `molecule` with `units bohr`, `symmetry c1`, `no_reorient`, `no_com` — coordinates lie on the z axis, so no reorientation or centre-of-mass shift; the units choice is justified in Units.
- one thread and engine memory setting 500 MiB — see Resources.

## Relation to E-01

E-01 aborted during conventional (PK) integral setup and is closed as technically BLOCKED and scientifically INDETERMINATE [21, 27]. The H2 proposal uses `direct`, so an H2 run would neither exercise nor diagnose the PK path and must never be described as diagnosing E-01 [AGENT].

## Phase A

| Job | R (bohr) | Phase | Status |
|---|---|---|---|
| H2-A-01 | 1.4 | A | PROPOSED_NOT_AUTHORIZED |

1.4 bohr is a round value chosen for transparent arithmetic; it is not an equilibrium, a target, or an expected minimum [AGENT].

## Phase B

| Job | R (bohr) |
|---|---|
| H2-B-01 | 1.0 |
| H2-B-02 | 1.2 |
| H2-B-03 | 1.4 |
| H2-B-04 | 1.6 |
| H2-B-05 | 1.8 |
| H2-B-06 | 2.0 |
| H2-B-07 | 2.2 |
| H2-B-08 | 2.4 |
| H2-B-09 | 2.6 |

All nine jobs are CONDITIONAL_NOT_AUTHORIZED, run one at a time in table order, only after Phase A has been run under its own authorization and independently reviewed, and only with a person's separate authorization of Phase B; H2-B-03 repeats 1.4 bohr as a separate job; the lowest point of the scan is a grid minimum only, with no interpolation or fitting [AGENT].

## Exclusions

Excluded: geometry optimization, gradients, frequencies, UHF, basis comparison, correlated methods, points beyond 2.6 bohr, and stability analysis [AGENT]. [48, Stability Analysis] documents that RHF stability checks are placed on the PK algorithm [LIT]; adding a stability check here would be a separate reviewed change [AGENT].

## Resources

Phase A at most 1 job; Phase B at most 9, sequential; engine memory setting 500 MiB, not an operating-system limit; 0 automatic retries; per job: 1 thread, 300 s wall clock enforced by the driver, a fresh empty scratch directory, scratch free space sampled before and after, and output file sizes recorded [AGENT].

## Stop conditions

On any of these: nonzero exit; timeout; SCF not converged or iteration limit reached; nonfinite energy; any reported identity mismatch (engine version or build, method, reference, basis, charge, multiplicity, electron count, basis-function count, atom count, coordinates, units); missing reported nuclear repulsion; reported nuclear repulsion differing from 1/R by more than 1e-10 hartree (geometry and unit integrity check only); any missing provenance field; any network access or installation attempt; then stop the sequence, keep all output, mark remaining points NOT_RUN, and change no setting [AGENT].

## Provenance to record

An H2 run must record all ten fields of [../../evidence-policy.md](../../evidence-policy.md) section 4, mapped to this proposal as follows [AGENT]:

- Code identity: hashed driver commit or uncommitted diff, exact invocation (see P5); engine binary identity checked against P1
- Configuration: hashed engine input files and parameters, relied-upon defaults enumerated; see Proposed engine options, Resources, Stop conditions
- Software version: engine and library names, versions, build identity, printed banner; checked against P1
- Coordinates and atom map: coordinates in bohr, element symbols, atom-identity map, no atom moves within a job; see System, Units
- Calculation: method, basis, charge, multiplicity, electron count, protocol; see System, Electronic model
- Seed: none
- Hardware and environment: operating system, architecture, processor identity, physical memory, numerically relevant environment settings, plus the Resources controls
- Outputs and hashes: all output files with SHA256, reported total energy and reported nuclear repulsion with units; output sizes per Resources
- Failure record: every failed, aborted or non-converged attempt preserved — stop condition fired, exit status, iteration count, logs; see Stop conditions
- Review record: digests of reviewed files, review decision, human authorization record or its absence

## Unresolved prerequisites

None of these is satisfied by this document; each stays open until separately established and reviewed [AGENT]:

- P1 (OPEN): Exact engine build identity for H2 (candidate only: the Psi4 1.11 build declared for P2 in B2 section 6 [39]; not H2 identity or readiness)
- P2 (PARTIAL [31]): Version-matched semantics and defaults of every proposed option
- P3 (PARTIAL [31]): Installed STO-3G basis bytes, comparison with [50] and normalization
- P4 (OPEN): Meaning of the reported energies
- P5 (OPEN): Hashed driver, input and atom map, exact invocation, no network
- P6 (OPEN): Resource and environment controls
- P7 (OPEN): Provenance and failure record
- P8 (OPEN): Independent review of the concrete run package
- P9 (OPEN): A person's separate, bounded run authorization

## Next gate

The next gate is a concrete, version-bound run proposal — exact settings, resources, provenance and stop conditions — independently reviewed and presented for a person's decision; it covers Phase A only, and Phase B remains a separate later decision. This document is not that proposal [AGENT].

## Gates

As of this writing: W1 STOPPED (S10). E-01 technically BLOCKED and scientifically INDETERMINATE [21, 27]. C3 readiness, MS-001 Stage 1 and option A BLOCKED. The W1, C3, MS-001 and option A statuses are restated from the gates record in [../../../.agents/RESEARCH-STATE.md](../../../.agents/RESEARCH-STATE.md).

## References

Catalogued in [../../SOURCES.md](../../SOURCES.md); the numbers and locators this specification uses: [21]; [27]; [30] section 6; [31] section 8; [39] B2 section 6; [48] Theory, Initial Guess, Convergence and Algorithm Defaults, Spin/Symmetry Treatment, Stability Analysis; [50]; [51] (unit display only).
