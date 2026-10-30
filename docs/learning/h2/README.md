# H2 learning track

This folder is a learning track on what a fixed-nuclei electronic calculation does, using the hydrogen molecule held
at a fixed internuclear separation. Its purpose is to make the steps of a self-consistent field (SCF) calculation
clear before any reconstruction of tool-tip geometries is attempted. The track is separate from MS-001: it is not
part of the MS-001 Stage 0 package and does not revise any of its definitions.

**Status.** The lesson, the method specification and the proposals in this folder are `[AGENT]` documents. No calculation was run for them, they contain
no computed values, they authorize nothing, and they make no claim of learner mastery. The Phase A run proposal in
[phase-a/](phase-a/H2-A-01-RUN-PROPOSAL.md) is PROPOSED_NOT_AUTHORIZED. Its independent review recorded the canonical
decision APPROVE for its exact bytes, and Lead acceptance is recorded; both are private task records. This approves a
preparation package only. It is not an authorization, readiness or a run. The proposal's P8 row, which reads that the
package's independent review is pending, is kept unchanged as the frozen text of the reviewed bytes and is superseded
by this status. It is not runnable: its driver refuses every launch while the network and installation prerequisite
(gate N1) is unresolved, and resolving that needs revised bytes, a renewed review and a person's decision. The
route-R2 method revision in [phase-a-r2/](phase-a-r2/H2-R2-METHOD-REVISION.md) states that, for job H2-A-01 launched
by the route-R2 driver only, prevention by a bound sandbox profile, without detection, takes the place of the accepted
no-network stop condition. A person approved its exact bytes on 2026-10-10
([approval record](phase-a-r2/H2-R2-METHOD-HUMAN-APPROVAL.md)). That approval is not a run authorization. The
route-R2 driver now binds the approved revision and the approval record. It still refuses every launch that lacks an
authorization satisfying every interlock check. On the [run-decision packet](phase-a-r2/H2-A-R2-RUN-DECISION-PACKET.md),
a person authorized exactly one attempt of H2-A-01 on 2026-10-10 and accepted M1
([authorization record](phase-a-r2/H2-A-01-HUMAN-RUN-AUTHORIZATION.md)). It was not exercised: the run stopped as
STOP_UNRUN before launch, with no run invocation and no engine process
([stop record](../../../results/h2/H2-A-01/README.md)). No launch permission remains in the task that held the
authorization, and there is no result. On 2026-10-11 a person directed a continuation of the same unchanged attempt in
a new task. It stopped as STOP_UNRUN during preparation, before the driver was invoked in any mode, with no engine
process ([continuation stop record](../../../results/h2/H2-A-01-continuation-01/README.md)). No launch permission
remains. The accepted Phase A driver still refuses every launch. A separate bounded authorization of 2026-10-29 covered one attempt of
H2-A-01 through the route-R2 driver, which ran once. Its [result report](H2-A-01-RESULT-REPORT.md), with a
[PDF summary](H2-A-01-RESULT-REPORT.pdf), and its [record](../../../results/h2/H2-A-01-run-01/README.md) give one recorded RHF/STO-3G
single point at a fixed 1.4 bohr separation. It is not a dissociation curve, an optimized or predicted equilibrium bond length,
readiness, parity or a reproduction of the benchmark; `[COMP-PRED]` is not granted, and the engine's source-code identity is
unestablished.

## Files

| File | Contents |
|---|---|
| [lesson-01-fixed-separation-scf.md](lesson-01-fixed-separation-scf.md) | Lesson on the SCF calculation of the hydrogen molecule at a fixed separation |
| [h2-method-specification.md](h2-method-specification.md) | Prospective method specification for that calculation, written as a proposal |
| [h2-method-parameters.json](h2-method-parameters.json) | Machine-readable parameters of the method specification |
| [phase-a/H2-A-01-RUN-PROPOSAL.md](phase-a/H2-A-01-RUN-PROPOSAL.md) | Concrete Phase A run proposal for job H2-A-01: invocation, environment, stop tiers, identity layers, v1.11 source semantics, enforcement limits, provenance and prerequisites |
| [phase-a/H2-A-01-DECISION-PACKET.md](phase-a/H2-A-01-DECISION-PACKET.md) | Redacted decision packet for a person, with bound digests, conditional gates and a blank template that is not an authorization |
| [phase-a/h2_phase_a_driver.py](phase-a/h2_phase_a_driver.py), [phase-a/h2_phase_a_payload.py](phase-a/h2_phase_a_payload.py), [phase-a/h2-a-01-input.json](phase-a/h2-a-01-input.json) | Control driver (standard library, refuses launch while N1 is unresolved), future engine-side payload and prospective input |
| [phase-a/h2-a-01-static-identity.json](phase-a/h2-a-01-static-identity.json) | Redacted static identity record of the candidate engine environment and version-matched source comparison; not runtime identity |
| [phase-a/tests/](phase-a/tests/) | Fixture and fake-process tests of the driver and payload; no engine is imported or run |
| [phase-a-r2/H2-R2-METHOD-REVISION.md](phase-a-r2/H2-R2-METHOD-REVISION.md) | Route-R2 method revision for job H2-A-01, with the quoted accepted texts it supersedes for that job; approved by a person (its frozen status text still reads PENDING) |
| [phase-a-r2/H2-R2-METHOD-HUMAN-APPROVAL.md](phase-a-r2/H2-R2-METHOD-HUMAN-APPROVAL.md) | Redacted record of the person's approval of the method revision, binding the revision and its decision packet; not a run authorization |
| [phase-a-r2/H2-A-R2-RUN-PROPOSAL.md](phase-a-r2/H2-A-R2-RUN-PROPOSAL.md), [phase-a-r2/H2-A-R2-DECISION-PACKET.md](phase-a-r2/H2-A-R2-DECISION-PACKET.md) | Route-R2 run proposal, a delta to the Phase A proposal, and the decision packet the person approved, with bound digests; both frozen |
| [phase-a-r2/H2-A-R2-RUN-PROPOSAL-02.md](phase-a-r2/H2-A-R2-RUN-PROPOSAL-02.md), [phase-a-r2/H2-A-R2-RUN-DECISION-PACKET.md](phase-a-r2/H2-A-R2-RUN-DECISION-PACKET.md) | Current run proposal, a delta for the enabling revision, and the run-decision packet for a person, with the sixteen bound digests and a deliberately invalid template |
| [phase-a-r2/h2_phase_a_r2_driver.py](phase-a-r2/h2_phase_a_r2_driver.py), [phase-a-r2/h2-r2-sandbox.sb](phase-a-r2/h2-r2-sandbox.sb), [phase-a-r2/h2-r2-platform-identity.json](phase-a-r2/h2-r2-platform-identity.json) | Route-R2 driver composing the pinned Phase A driver (binds the approved method revision and approval record; refuses every launch without an authorization that satisfies every interlock check), sandbox profile and platform identity record |
| [phase-a-r2/tests/](phase-a-r2/tests/) | Fixture and fake-process tests of the route-R2 driver, including sandbox tests around fake processes; no engine is imported or run |
| [phase-a-r2/H2-A-01-HUMAN-RUN-AUTHORIZATION.md](phase-a-r2/H2-A-01-HUMAN-RUN-AUTHORIZATION.md) | Redacted record of the person's authorization of exactly one attempt of H2-A-01, binding the run-decision packet and the current run proposal; not exercised (STOP_UNRUN before launch) and not a review decision |
| [../../../results/h2/H2-A-01/README.md](../../../results/h2/H2-A-01/README.md) | Stop record of that attempt: STOP_UNRUN before launch, with zero run invocations and no engine process, its machine-readable outcome and provenance; no results |
| [../../../results/h2/H2-A-01-continuation-01/README.md](../../../results/h2/H2-A-01-continuation-01/README.md) | Stop record of the continuation of that attempt (2026-10-11): STOP_UNRUN during preparation, before any driver invocation, with no engine process, its machine-readable outcome and provenance; no results |
| [H2-A-01-RESULT-REPORT.md](H2-A-01-RESULT-REPORT.md), [H2-A-01-RESULT-REPORT.pdf](H2-A-01-RESULT-REPORT.pdf) | Sourced report of the H2-A-01 run of 2026-10-29: one recorded RHF/STO-3G single point at a fixed 1.4 bohr separation, Figures 3 to 5 with their source tables, the energy convention, residuals, the engine source-code identity gap and one conceptual question; the PDF is a derived summary |
| [../../../results/h2/H2-A-01-run-01/README.md](../../../results/h2/H2-A-01-run-01/README.md) | Record of that run: machine-readable outcome, provenance with a hashed inventory of the sixteen original files and the redaction rules, verbatim and redacted engine records |
| [../../figures/](../../figures/) and [../../../tools/](../../../tools/) | Figures 3 to 5 (SVG and PNG), their source tables, deterministic renderers, the PNG exporter and the PDF builder |

## Reading order

Read the lesson first, then the method specification, and consult the parameter file alongside the specification.
Then read the Phase A run proposal, its decision packet, and the driver, payload, input and static identity record it
describes. For route R2, read the method revision, its run proposal and decision packet, then the approval record,
the current run proposal and the run-decision packet, and finally the run authorization record and the stop record. The report of the run of 2026-10-29 follows the stop records.

## Gates

The gates are unchanged: W1 is STOPPED (S10); E-01 is technically BLOCKED and scientifically INDETERMINATE; and C3
readiness, MS-001 Stage 1 and option A are BLOCKED.

## Related documents

- [Repository README](../../../README.md)
- [Source catalogue](../../SOURCES.md), Section 20
- [Evidence policy](../../evidence-policy.md)
