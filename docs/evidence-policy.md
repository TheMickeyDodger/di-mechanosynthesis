# Evidence policy

This policy governs how scientific claims in this repository are classified and what provenance a future result
must carry. It is adapted for public use from the project's original evidence policy. The worked examples were
rewritten, and internal references were removed.

## 1. Evidence classes

| Tag | Class | Assignment rule |
|---|---|---|
| `[EXP]` | Experimentally demonstrated | A physical observation made with an instrument, reported with its conditions by an identified party. It applies to the observation, not to any interpretation of it. |
| `[COMP-REPRO]` | Computationally reproduced | A calculation performed **by this project** under full provenance (§4) and independently reviewed, which reproduces a previously stated computational result under a known, comparable setup. **None exist.** |
| `[COMP-PRED]` | Computationally predicted | A calculation's output (energy, geometry, path, image) presented as a prediction, with its method and provenance. Not an observation. |
| `[LIT]` | Literature-derived | A statement taken from a published or official source, with a locator. This is a *provenance* label; the underlying class is recorded alongside it. |
| `[AGENT]` | Agent-proposed | A model, protocol, threshold, geometry, mapping or ranking proposed by a person or software agent acting as a planner. It is a plan or hypothesis, never evidence about physics. |
| `[SPEC]` | Speculative | A possible explanation offered without supporting calculation or observation. |
| `[GAP]` | (marker, not a class) | An input required for a claim that is not available. A gap blocks every classification that depends on it. |

Examples, applied to the benchmark:
- The reported count of 184 IR-C2 outcomes in 197 interactions is `[LIT]` over `[EXP]`.
- The benchmark's QM/MM energy profile is `[LIT]` over `[COMP-PRED]`.
- This project's donor-candidate geometries are `[AGENT]`.

## 2. Rules

1. **Classify first, then attach provenance.** Assign the class of the underlying evidence first, then record
   where the statement came from.
2. **No upgrades by repetition.** A class is never upgraded by restatement, summary, agreement between agents,
   or repetition across documents. A `[COMP-PRED]` in a paper stays `[COMP-PRED]` when restated here.
3. **This project's calculations earn labels, never inherit them.** A calculation earns `[COMP-PRED]` only with
   §4 provenance complete and an independent review. It earns `[COMP-REPRO]` only if, in addition, the setup it
   reproduces is known and the comparison is stated. Missing provenance blocks the label.
4. **Observations do not transfer to explanations.** An `[EXP]` observation does not make any explanation of it
   `[EXP]`.
5. **Disagreements stay visible.** When sources disagree, record both with locators and state the disagreement.
   Never pick a winner silently.
6. **Unestablished is `UNVERIFIED`.** A fact that cannot be established from primary sources is written
   `UNVERIFIED`, and the attempts are listed.
7. **Missing capability means `INDETERMINATE`.** An engine capability that is unverified for the exact version
   used makes every criterion depending on it `INDETERMINATE`, never `PASS`.

## 3. Language-model output is never evidence

Output from a language model or other generative agent is **never** evidence of stability, bonding, energies,
barriers, pathways, feasibility or product formation. At most it is `[AGENT]` or `[SPEC]`. That holds regardless
of how many agents agree, how confident the wording is, or whether the output was produced during review.
Import tests, file round-trips and bookkeeping checks likewise show that software and file formats behave. They
show nothing about chemistry.

## 4. Provenance required for any future result or figure

A result or figure is admissible only if every field below is present and resolvable. Missing fields are recorded
as missing, and the result is labelled accordingly, never upgraded.

| Field | Requirement |
|---|---|
| Code identity | Commit of every code path used; for uncommitted code, the full diff, hashed |
| Configuration | Exact engine input files and parameters, hashed; every relied-upon default enumerated |
| Software version | Name, version and build identity of every engine and library; the engine's printed banner captured |
| Input coordinates and atom IDs | Coordinates with units, periodicity, element symbols and a stable atom-identity map that survives every step; which atoms are fixed |
| Calculation performed | Method, basis and effective core potentials, charge, spin multiplicity, constraints, protocol, optimizer settings |
| Random seed | Wherever stochastic components exist; "none" recorded explicitly otherwise |
| Hardware and environment | Operating system, architecture, processors, memory, and environment settings that affect numerics |
| Outputs and hashes | Every output file with SHA256; extracted quantities with units; figures with the data files they were drawn from |
| Failure record | Every failed, aborted or non-converged attempt, with exit codes and logs, preserved rather than overwritten |
| Review record | The reviewed file digests and the review decision |

## 5. Three separate acceptances

| Acceptance | Meaning | Does not imply |
|---|---|---|
| Document acceptance | A reviewer finds the documents internally consistent, sourced and honest about gaps | That the science is ready, or that anything may run |
| Scientific gate | Evidence meets a declared criterion, independently checked | Permission to proceed |
| Authorization | A person permits a stated, bounded next step | That a scientific gate was passed on merit |

Publishing a document in this repository is none of these. It authorizes nothing.
