# MS-000 Mechanosynthesis Research Architecture

Status: public adaptation of the MS-000 architecture record. It assigns responsibilities for research control,
scientific computation, workflow provenance, and visualization. It does not authorize a calculation.

Companion documents: [MS-000-COMPUTE-SPIKE.md](MS-000-COMPUTE-SPIKE.md), [EVIDENCE-POLICY.md](EVIDENCE-POLICY.md),
[OPEN-SOURCE-LANDSCAPE.md](OPEN-SOURCE-LANDSCAPE.md), [SOURCE-LEDGER.md](SOURCE-LEDGER.md).

## 1. What this program is

A human-gated research program whose first scientific target is the Cowie et al. 2026 IR-C2 donation model
(arXiv:2605.27250) as characterised in MS-000-COMPUTE-SPIKE.md. MS-000 is a feasibility spike: it produces
documents, a source ledger and one import/IO smoke test. It runs no chemistry.

## 2. Ownership boundaries

| Layer | Owns | Never owns |
|---|---|---|
| **Dodging Infinity** (research orchestration) | Mission identity and authorization; the milestone gates in Section 3; evidence classes and their non-upgrade rule; blockers; review orchestration; the human-authorization record; delivery receipts | Energies, forces, structures, physical conclusions; scientific job scheduling or provenance internals |
| **Scientific engines** (xtb, CP2K, Psi4; conditional) | Energies, forces, structures, populations, and every physical conclusion drawn from them | Mission state, evidence class assignment, review decisions |
| **Scientific workflow system** (AiiDA, conditional; QCFractal deferred as an alternative) | Scientific job execution, restarts, and the computational provenance graph (inputs, codes, outputs, hashes) | Authorization, evidence-class labeling, delivery |
| **Structure/analysis/rendering libraries** (ASE, OVITO) | Building, constraining, reading/writing and rendering **computed** coordinates; connectivity analysis | Physics (they have no energies without an engine) |
| **Humans** | Every milestone gate; scope decisions (e.g., faithful reproduction vs declared-deviation study); MS-001 authorization | Get replaced by an approval a machine minted |

Consequences for tool selection (OPEN-SOURCE-LANDSCAPE.md): a second workflow engine (Fireworks via Pynta or
atomate2; pyiron; Puffin/MongoDB) duplicates the workflow-system role and is deferred; DI does not implement a
chemistry engine, a compiler, a primitive library or a manufacturing simulation.

Research direction and authorization remain human decisions. Dodging Infinity records mission state and review;
AiiDA records calculation provenance and execution; the chemistry engines produce energies, forces, and
structures; ASE and OVITO handle structures, analysis, and rendering. No layer may substitute for evidence owned
by another.

## 3. Long-term human-gated milestone sequence (preserved as specified)

| Milestone | Content | Gate |
|---|---|---|
| **MS-000** | This spike: stack, gaps, evidence policy, prospective protocol | Independent document review; scientific gate PENDING (spike §8.1); separate human authorization required before MS-001 |
| **MS-001** | IR-C2 reproduction under a human-selected scope option (faithful reproduction is BLOCKED on missing inputs and parity evidence, with its own prerequisites in spike §8.3-A; a declared-deviation study is a possible option, not selected, with its own prerequisites in §8.3-B) | Human authorization; the option's prerequisites; Stage 0 → Stage 1 (method-validation calculations) → Stage 2 (trajectory), each Reviewer-checked (spike §8.2) |
| **MS-002** | IR-C2 → IR-C4 reproduction (Cowie Fig. 4 model) | Human authorization after MS-001 review |
| **MS-003** | Perturb mechanical variables (approach depth, step size, lateral offset, leg configuration), including the deeper-approach alternative pathway (spike M8) | **Only after both MS-001 and MS-002 pass**; human authorization |
| **MS-004** | Off-target and competing hypotheses (H abstraction, Si abstraction, the 2IR-C4 off-target product's two proposed pathways) | Requires review; this is the **first unanswered scientific question** in the program; human authorization |
| **MS-100+** | Anything beyond single validated primitives | Only after validated primitives exist; human authorization |

A milestone "passes" only when its declared observations are met with full provenance, an independent Reviewer
approves, and a human records authorization to proceed. A blocked or pending gate is a valid state.

## 4. Explicitly deferred

Not designed, not specified, not implemented in MS-000 or MS-001: a compiler; a build DAG; scheduling of build
operations; failure, retry, repair, repurpose, unknown-state and scrap handling; manufacturing simulation. Any
mention of these in this package is a placeholder name, not a design.

**Manufacturing hypotheses stay labeled as hypotheses.** Statements about throughput, latency, per-operation time,
yield under independence assumptions, or scale-up are `[AGENT]` or `[SPEC]` and are not evidence. The Cowie
yields are per-interaction counts with Wilson intervals (spike §2.7); no independence between events is assumed,
and no latency or throughput figure exists in the source.

## 5. Rendering

- **Atomic results** render **computed coordinates** only, via ASE (`ase.io`, `ase.visualize`) and the OVITO
  Python module or OVITO Basic. A rendered figure must trace to the data file it was rendered from
  (EVIDENCE-POLICY.md §4). Drawn, inferred or hand-placed geometries are not rendered as results.
- **OpenSCAD factory or fixture geometry is conceptual** unless every dimension is tied to a measured value with a
  source. No measured dimensions exist in this program today, so any OpenSCAD model is a concept sketch and is
  labeled as such.

## 6. Three separate acceptances

| Acceptance | Who | Meaning | Does not imply |
|---|---|---|---|
| **Document acceptance** | Independent reviewer | These documents are internally consistent, sourced, and honest about gaps | That the science is ready, or that anything may run |
| **Scientific gate** | Evidence against the milestone's declared criteria, independently checked | The milestone's prerequisites are met with evidence | Authorization to proceed |
| **Human authorization** | A person, recorded by DI | Permission to start the next milestone under a stated scope | That the gate was passed on merit (a human may authorize a bounded study while the gate stays pending, and must say so) |

The MS-000 scientific gate is **PENDING** for the reasons in spike §8.1: missing trajectory setup, missing parity
evidence, no public independent-review approval, and pending review of the tolerance procedure. This page conveys
no authorization for MS-001.

## 7. Repository boundary

This repository owns scientific definitions, inputs, workflows, results, and public provenance. Dodging Infinity
remains a separate orchestration system that owns mission state, authorization, and review records. Scientific
engines and workflow services remain replaceable components with no authority to change evidence classifications
or gates.
