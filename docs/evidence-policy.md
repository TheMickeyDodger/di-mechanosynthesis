# Evidence policy

This policy governs how scientific claims in the repository are classified and what provenance a future result
must carry. It is adapted for public use from the project's original evidence policy, with the worked examples
rewritten and internal references removed.

## 1. Evidence classes

Each claim is assigned one of six classes, or the `[GAP]` marker, according to the rules in the table.

| Tag | Class | Assignment rule |
|---|---|---|
| `[EXP]` | Experimentally demonstrated | A physical observation made with an instrument, reported with its conditions by an identified party. The class applies to the observation, not to any interpretation of it. |
| `[COMP-REPRO]` | Computationally reproduced | A calculation performed by this project under full provenance (Section 4) and independently reviewed, which reproduces a previously stated computational result under a known, comparable setup. None exists. |
| `[COMP-PRED]` | Computationally predicted | The output of a calculation (energy, geometry, path or image) presented as a prediction, together with its method and provenance. It is not an observation. |
| `[LIT]` | Literature-derived | A statement taken from a published or official source, with a locator. This is a provenance label, and the underlying class is recorded alongside it. |
| `[AGENT]` | Agent-proposed | A model, protocol, threshold, geometry, mapping or ranking proposed by a person or software agent acting as a planner. It is a plan or hypothesis, never evidence about physics. |
| `[SPEC]` | Speculative | A possible explanation offered without supporting calculation or observation. |
| `[GAP]` | Marker, not a class | An input required for a claim that is not available. A gap blocks every classification that depends on it. |

In the benchmark, for example, the reported count of 184 IR-C2 outcomes in 197 interactions is `[LIT]` over
`[EXP]`, and the benchmark's QM/MM energy profile is `[LIT]` over `[COMP-PRED]`. The donor-candidate geometries in
this repository are `[AGENT]`. The record of the stopped E-01 attempt in `results/e01/` is a failure record of a
software run under Section 4; it carries no class about chemistry, because no converged electronic energy or
gradient of either donor was produced.

## 2. Rules of classification

The class of the underlying evidence is assigned first, and the provenance of the statement is recorded with it. A
class is never upgraded by restatement, summary, agreement between agents or repetition across documents. A
`[COMP-PRED]` claim in a paper therefore remains `[COMP-PRED]` when it is restated here, and an `[EXP]`
observation does not make any explanation of it `[EXP]`.

A calculation by this project qualifies as `[COMP-PRED]` only when the provenance of Section 4 is complete and the
result has been reviewed independently. It qualifies as `[COMP-REPRO]` only if, in addition, the setup it
reproduces is known and the comparison is stated. Missing provenance blocks the label.

When sources disagree, both are recorded with locators and the disagreement is stated, without silently preferring
either. A fact that cannot be established from primary sources is written `UNVERIFIED`, and the attempts are
listed. An engine capability that is unverified for the exact version used makes every criterion that depends on
it `INDETERMINATE`, never `PASS`.

## 3. Language-model output

Output from a language model or another generative agent is never evidence of stability, bonding, energies,
barriers, pathways, feasibility or product formation. At most it is `[AGENT]` or `[SPEC]`, however many agents
agree, however confident the wording, and whether or not the output was produced during review. In the same way,
import tests, file round trips and bookkeeping checks show that software and file formats behave as expected, but
they show nothing about chemistry.

## 4. Provenance required for a future result or figure

A result or figure is admissible only if every field below is present and resolvable. A missing field is recorded
as missing, and the result is labelled accordingly rather than upgraded.

| Field | Requirement |
|---|---|
| Code identity | Commit of every code path used; for uncommitted code, the full diff, hashed |
| Configuration | Exact engine input files and parameters, hashed, with every relied-upon default enumerated |
| Software version | Name, version and build identity of every engine and library, with the engine's printed banner captured |
| Input coordinates and atom identifiers | Coordinates with units, periodicity, element symbols and a stable atom-identity map that survives every step; which atoms are fixed |
| Calculation performed | Method, basis and effective core potentials, charge, spin multiplicity, constraints, protocol and optimizer settings |
| Random seed | Recorded wherever stochastic components exist, and recorded as "none" otherwise |
| Hardware and environment | Operating system, architecture, processors, memory and environment settings that affect numerics |
| Outputs and hashes | Every output file with its SHA256, extracted quantities with units, and figures with the data files they were drawn from |
| Failure record | Every failed, aborted or non-converged attempt, with exit codes and logs, preserved rather than overwritten |
| Review record | The digests of the reviewed files and the review decision |

## 5. Separate acceptances

Acceptance of documents, passage of a scientific gate and authorization of further work are distinct, and no one
of them implies another.

| Acceptance | Meaning | Does not imply |
|---|---|---|
| Document acceptance | A reviewer finds the documents internally consistent, sourced and candid about gaps | That the science is ready, or that anything may be run |
| Scientific gate | Evidence meets a declared criterion and has been checked independently | Permission to proceed |
| Authorization | A person permits a stated, bounded next step | That a scientific gate was passed on its merits |

Publishing a document in this repository is not an acceptance of any of these kinds, and it authorizes nothing.
