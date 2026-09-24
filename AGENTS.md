# Conventions for contributors and automated agents

This repository contains public, provenance-first research material on computational models of mechanically
controlled chemistry. It holds an evidence policy, candidate input structures, a method specification, an engine
capability record, figure renderers, provenance manifests and the record of one stopped engine-validation attempt
(`results/e01/`), with its postmortem and installed-build survey. That attempt is closed as technically blocked
and scientifically indeterminate. The repository contains no converged quantum-chemistry results. The
[README](README.md) describes the scientific scope. This document sets out the conventions that contributors, and
automated agents in particular, are expected to follow.

## Organization of the repository

| Path | Contents |
|---|---|
| `docs/SOURCES.md` | Numbered catalogue of every reference, tool, method source and figure, with links, versions, locators and limitations |
| `docs/evidence-policy.md` | Evidence classes and the rules every claim must follow |
| `docs/benchmark.md` | What the benchmark preprint reports, with locators |
| `docs/donor-candidates.md`, `structures/` | Agent-proposed, unoptimized candidate geometries, their bookkeeping and the Figure 1 method |
| `docs/e01-method-specification.md` | Prospective specification of the first calculation, kept as the preparation record |
| `docs/engine-capability-status.md` | What archived engine sources and the installed build establish, and what remains unverified |
| `results/e01/` | The stopped and closed E-01 attempt: report, postmortem and installed-build survey, machine-readable outcome, configuration used and redacted engine output |
| `tools/` | Deterministic renderers of Figures 1 and 2, with their input tables |
| `provenance/EXPORT-MANIFEST.md` | SHA256 and derivation of every public file |
| `.agents/RESEARCH-STATE.md` | Research-state record: intended end state, gates, status, open issues and next work |

## Division of responsibilities

The project separates responsibilities so that no layer can supply evidence on behalf of another.

| Layer | Responsible for | Not responsible for |
|---|---|---|
| People | Research direction, decisions on scope, authorization of consequential work | Not applicable |
| Dodging Infinity, a separate orchestration project | Bounded task orchestration, independent review, tracking of evidence status, authorization and delivery records | Calculated energies, forces or structures |
| This repository | Scientific definitions, candidate inputs, method specifications, capability records, provenance and export manifests | Authorization; publishing a document here authorizes nothing |
| Scientific toolchain | Computational evidence: calculated energies, forces, structures and populations, with their raw outputs | Evidence classification and review decisions |

## Evidence standard

Every scientific claim is classified by its underlying evidence using the classes `[EXP]`, `[COMP-REPRO]`,
`[COMP-PRED]`, `[LIT]`, `[AGENT]` and `[SPEC]`, or the marker `[GAP]`, as defined in
[docs/evidence-policy.md](docs/evidence-policy.md). Output from language models, including the output of any agent
working in this repository, is never physical evidence and is at most `[AGENT]` or `[SPEC]`. A classification is
never upgraded by restatement, summary or agreement. An engine capability counts only when it is shown for the exact
software version used.

## Claims that require reviewed evidence

The following restrictions reflect the present absence of reviewed results rather than permanent prohibitions, and
each lifts only when reviewed evidence that meets the evidence policy exists. Energies, forces, gradients, spin
populations and other quantum-chemistry results are not claimed, because no converged results exist; the only
attempt, E-01, stopped during integral setup and is closed as technically blocked and scientifically
indeterminate, and a source-level postmortem and a static survey of the installed build did not diagnose its
cause. The conditional source-level pathway recorded in the postmortem is not claimed as the cause of E-01; it is
neither established nor excluded, and disk capacity is likewise neither established nor excluded. Neither
reproduction of the benchmark's experiments, surface model, mechanism or calculations, nor agreement with them, is
claimed. The donor-candidate and surface geometries are not described as relaxed or validated, nor as verified
against the benchmark authors' supplementary coordinates. Engine capabilities and functional equivalence that are
marked `UNVERIFIED` or open are not claimed.

Three further restrictions are matters of method or scope rather than of missing evidence. Reported
per-interaction counts are never multiplied into build-success probabilities. Installation commands, releases or
claims of readiness are not given for software that this repository does not provide. Name availability in an
installed build, whether a header declaration, a symbol-table definition or a dynamic export, is not claimed as
ABI compatibility, initialization or callability.

## Adding or changing content

Primary sources are cited with an exact locator (identifier, version and section, page or line), and each new
source is added to [docs/SOURCES.md](docs/SOURCES.md) with its verification basis. Paper text, figures,
supplementary material and vendor source code are cited and paraphrased rather than copied. Proposals are labelled
as proposals, and figures of numerical data are drawn only from data given alongside them.

Every published file except the manifest itself requires a SHA256 entry in
[provenance/EXPORT-MANIFEST.md](provenance/EXPORT-MANIFEST.md), since the manifest never lists its own hash. Every
adaptation must state what changed. Local paths, user names, host names, credentials and internal session or task
identifiers do not belong in public files.

## Authorization

The documents in this repository, including this file and `.agents/RESEARCH-STATE.md`, are public information and
do not constitute runtime authorization. They do not permit any agent to install software, run calculations,
retrieve sources or deliver changes. Authorization for such work comes from the people directing the project,
through the separate orchestration system that governs it.
