# MS-000 Evidence Policy

Status: public adaptation of the MS-000 evidence policy. The provenance schema in Section 4 is **provisional**
(Section 6).

Companion documents: [MS-000-COMPUTE-SPIKE.md](MS-000-COMPUTE-SPIKE.md), [ARCHITECTURE.md](ARCHITECTURE.md),
[OPEN-SOURCE-LANDSCAPE.md](OPEN-SOURCE-LANDSCAPE.md), [SOURCE-LEDGER.md](SOURCE-LEDGER.md),
[SMOKE-AND-ENVIRONMENT-RECORD.md](SMOKE-AND-ENVIRONMENT-RECORD.md).

## 1. The six evidence classes, never conflated

| Tag | Class | Assignment rule | Worked example from this spike |
|---|---|---|---|
| `[EXP]` | Experimentally demonstrated | A physical observation made with an instrument, reported with its conditions, by an identified party. Applies to the observation, not to any interpretation of it. | Cowie reports IR-C2 yield 93% (184/197, Wilson 95% CI 89–96%) from IM-STM outcomes at 4 K (MS-000-COMPUTE-SPIKE.md §2.7). The **assignment** of the imaged feature to IR-C2 is an interpretation supported by several lines, one of which is `[COMP-PRED]`. |
| `[COMP-REPRO]` | Computationally reproduced | A calculation performed **by this program** under full provenance (Section 4), Reviewer-checked, that reproduces a previously stated computational result under a stated, comparable setup. Requires the comparison setup to be known. | **None exist.** No calculation was run in MS-000. Because the Cowie setup is unavailable, nothing can be labeled `[COMP-REPRO]` against Cowie until the parity gaps close; a Stage 2 result under a declared deviation could at most be `[COMP-PRED]` under this program's setup. |
| `[COMP-PRED]` | Computationally predicted | A calculation's output (energy, geometry, path, image) presented as a prediction, with its method and provenance. Not an observation. | Cowie's Fig. 3 mechanism and E(z−z0) profile; the STM image simulation for IR-C2; the proxy Ge–C vs Si–C energies (5.200 vs 5.139 eV at ωB97X-D/Def2-TZVPP) (spike §2.6–2.7). Barrera's H-abstraction surface (spike §1.4). |
| `[LIT]` | Literature-derived | A statement taken from a published or official source, with a locator. This is a **provenance** label; the underlying evidence type is recorded alongside it (Section 2). | tblite's built-in method list (GFN1, GFN2, IPEA1; no GFN0) from its official docs; CP2K `GFN_TYPE` default 1 from its manual (OPEN-SOURCE-LANDSCAPE.md). |
| `[AGENT]` | Agent-proposed | A model, protocol, threshold procedure, geometry, mapping or ranking proposed by a research agent or an LLM. It is a plan or hypothesis, never evidence about physics. | The M1/M2 candidate geometries, the driven-scan protocol, the diagnostic priority order in spike §8.8, the tolerance-selection procedure in §8.6. |
| `[SPEC]` | Speculative | A possible explanation offered without supporting calculation or observation, by the paper or by this program. | Cowie's list of possible contributors to off-target H abstraction, including hydrogen tunneling, and its pair of candidate failure routes for the 2IR-C4 off-target product, which the paper leaves undiscriminated (spike §2.7 third table, §2.9 item 9): literature provenance over speculative evidence. |
| `[GAP]` | (Not a class; a marker) | An input required for a claim that is not available to this study. A `[GAP]` blocks any class assignment that depends on it. | The QM/MM partition; basis/ECP; the drive protocol; all SI-only content. |

**Rules for assigning and moving between classes**

1. Assign the class of the **underlying evidence** first, then attach the provenance (Section 2).
2. A class is never upgraded by restatement, summary, agreement between agents, or repetition across documents. A
   `[COMP-PRED]` in Cowie stays `[COMP-PRED]` when this program restates it.
3. A calculation by this program earns `[COMP-PRED]` only with the Section 4 provenance complete and a Reviewer
   check; it earns `[COMP-REPRO]` only when, in addition, the setup it reproduces is known and the comparison is
   stated. Missing provenance fields block the label.
4. An `[EXP]` claim in a paper does not make any explanation of it `[EXP]`. Explanations are `[COMP-PRED]`,
   `[LIT]`, `[AGENT]` or `[SPEC]` as their own evidence warrants.
5. When two sources disagree (e.g., ASE docs vs PyPI metadata on Python version), both are recorded with locators
   and the disagreement is stated; the program does not pick a winner silently.
6. A field that cannot be established from official sources is written `UNVERIFIED` with the attempts listed.

## 2. LLM output is never evidence

LLM output, including every sentence in these documents that is not a locator-backed restatement of a source, is
**never evidence** of stability, bonding, energies, barriers, pathways, feasibility, or product formation. It is at
most `[AGENT]` or `[SPEC]`. This holds regardless of how many agents agree, how confident the wording is, or
whether the output was produced during review. The same applies to import/IO smoke tests (Section 5).

## 3. Literature provenance vs underlying evidence type

"Provenance" answers *where the statement came from*; "evidence type" answers *what kind of thing it is*. A paper
reporting a calculation is **literature-derived provenance over computationally-predicted evidence**. Every claim
in this package therefore carries both when they differ:

| Statement | Provenance | Underlying evidence type |
|---|---|---|
| Cowie reports 2IR-C2 at 97% (71/73) | `[LIT]` (Cowie section 6, para 1) | `[EXP]` |
| Cowie's model describes the pendent-to-IR relaxation as barrierless at large z | `[LIT]` (Cowie section 3, para 1) | `[COMP-PRED]` |
| CP2K lists `WB97X_D3` among libxc hybrid GGA functionals | `[LIT]` (CP2K 2026.2 manual) | Software documentation fact (neither `[EXP]` nor `[COMP-PRED]`; it says nothing about parity) |
| The stack in OPEN-SOURCE-LANDSCAPE.md §3 is the minimum | `[AGENT]` | Proposal |
| ASE 3.29.0 imports and round-trips extxyz on this host | First-party smoke record | Environment fact only (Section 5) |

## 4. Provenance requirements for any eventual result or figure

A result or figure produced by this program is admissible only if each field below is present and resolvable.
Missing fields are recorded as missing, and the result is labeled accordingly (not upgraded).

| Field | Requirement |
|---|---|
| Code identity | Git commit of every code path used (this repository and any driver scripts); if uncommitted, the full dirty diff, hashed |
| Configuration | The exact input files/parameters as consumed by each engine, hashed; all engine defaults that were relied upon, enumerated (e.g., ASE's CP2K calculator defaults must be listed if not overridden) |
| Software version | Name, version, build identity (compiler, BLAS/LAPACK, MPI) for each engine and library; package digests where available; the engine's own printed banner captured |
| Input coordinates and atom IDs | Coordinates with **units**, cell/periodicity, and a stable atom identity map (tags/indices) that survives every step; element symbols; which atoms are fixed |
| Calculation performed | Method, level(s), partition/embedding/link definition, charge, spin multiplicity, constraints, drive protocol (branch, step index, imposed z), optimizer and its settings |
| Random seed | Wherever stochastic components exist (initial guesses, sampling); "none" recorded explicitly otherwise |
| Hardware/environment | Host, OS, architecture, CPU/GPU, memory, environment variables that affect numerics (e.g., `XTBPATH`, thread counts), container/venv identity |
| Outputs and hashes | Every output file with sha256; extracted quantities with units; figures with the data files they were rendered from |
| Failure record | Every failed, aborted or non-converged attempt, with exit codes and logs, preserved rather than overwritten (the smoke record's attempt 1 is the model for this) |
| Review record | Reviewer identity/role, the reviewed file digests, the canonical decision, and the round |
| Retained per claim | Coordinate units, atom identity, charge/spin, constraints, environment, tool state (e.g., iodinated or de-iodinated; which leg configuration), and the evidence class |

## 5. Smoke and IO evidence does not reproduce chemistry

An import or read/write round-trip demonstrates that a library loads and that a file format preserves the fields
tested. It demonstrates **nothing** about energies, forces, bonding, stability, pathways, feasibility, product
formation, or agreement with any paper. The ASE smoke test in
[SMOKE-AND-ENVIRONMENT-RECORD.md](SMOKE-AND-ENVIRONMENT-RECORD.md) is labeled accordingly, and any sentence in this
package implying otherwise is a defect to be corrected.

## 6. The schema is provisional

Section 4 is provisional pending (a) the Cowie SI or author-provided setup, should it become available through an
authorized channel, and (b) a review of the ASE and AiiDA scientific data models (ASE `Atoms`/`info`/constraints
and `ase.io` formats; AiiDA node types and the `aiida-cp2k` plugin's data model) to decide which fields those
models already carry and which need extension. **No custom primitive schema or generator is finalized now**, and
none is to be implemented in MS-000.

## 7. What the evidence layer belongs to

DI records mission, evidence class, blockers, review and authorization. The scientific workflow system (AiiDA,
conditional) records job execution and computational provenance. Scientific engines produce energies, forces,
structures and physical conclusions. This policy governs how those records are labeled and combined; it does not
move authority between layers (ARCHITECTURE.md §2).
