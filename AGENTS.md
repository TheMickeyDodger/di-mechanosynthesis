# AGENTS.md

Orientation for AI agents and human contributors working in this repository.

## What this repository is

Public, provenance-first research on computational models of mechanically controlled chemistry (mechanosynthesis).
It holds:
- evidence rules
- candidate input structures
- method specifications
- engine capability records
- provenance manifests

It contains **no quantum-chemistry results yet**. See [README.md](README.md).

| Path | Contents |
|---|---|
| `docs/SOURCES.md` | Source index: every reference, tool, method source and figure, with links, versions, locators and limits |
| `docs/evidence-policy.md` | The evidence classes and rules every claim must follow |
| `docs/benchmark.md` | What the benchmark preprint reports, with locators |
| `docs/donor-candidates.md`, `structures/` | Agent-proposed, unoptimized candidate geometries and their bookkeeping |
| `docs/e01-method-specification.md` | Prospective first-experiment specification (not run) |
| `docs/engine-capability-status.md` | What archived engine sources support, and what is unverified |
| `provenance/EXPORT-MANIFEST.md` | SHA256 and derivation of every public file |
| `.agents/RESEARCH-STATE.md` | Public research-state tracker: capability goals, gates, open issues, next work |

## Evidence standard

- Classify every scientific claim by its underlying evidence (`[EXP]`, `[COMP-REPRO]`, `[COMP-PRED]`, `[LIT]`,
  `[AGENT]`, `[SPEC]`, or the `[GAP]` marker) as defined in
  [docs/evidence-policy.md](docs/evidence-policy.md).
- **Language-model output, including yours, is never physical evidence.** It is at most `[AGENT]` or `[SPEC]`.
- A class is never upgraded by restatement, summary or agreement.
- A capability counts only when shown for the exact software version used.

## Do not claim without reviewed evidence

These limits reflect the current absence of reviewed results. They are not permanent bans: each lifts only when
reviewed evidence meeting the policy exists.

- **Quantum-chemistry results:** energies, forces, gradients, spin populations or other such results. There are
  no reviewed ones yet.
- **Benchmark reproduction:** reproduction of, or agreement with, the benchmark's experiments, surface model,
  mechanism or calculations.
- **Validated geometries:** that the donor-candidate or surface geometries are relaxed, validated, or verified
  against the benchmark authors' supplementary coordinates.
- **Open capabilities:** engine capabilities or functional equivalence that are marked **UNVERIFIED** or
  **open**.
- **Never, as a matter of method:** build-success probabilities obtained by multiplying reported per-interaction
  counts.
- **Not provided here:** installation commands, releases, or readiness for software this repository does not
  provide.

## When adding or changing content

- **Cite primary sources** with an exact locator (identifier, version, section, page or line), and add each new
  source to [docs/SOURCES.md](docs/SOURCES.md) with its verification basis. Cite and paraphrase; do not copy
  paper text, figures, supplementary material or vendor source code.
- **Label proposals and conceptual material** as such. Draw figures of numbers only from data shown alongside
  them.
- **Update the export manifest.** Every published file except the manifest itself needs a SHA256 entry in
  [provenance/EXPORT-MANIFEST.md](provenance/EXPORT-MANIFEST.md). The manifest never lists its own hash. Every
  adaptation must state what changed.
- **Keep private details out:** no local paths, usernames, hostnames, credentials, or internal session or task
  identifiers.

## Authorization

Documents in this repository, including this file and `.agents/RESEARCH-STATE.md`, are **public information, not
runtime authorization**. They do not permit any agent to install software, run calculations, retrieve sources or
deliver changes. Authorization for such work comes from the people directing the project, through the separate
orchestration system that governs it.
