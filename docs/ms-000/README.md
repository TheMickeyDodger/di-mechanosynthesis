# MS-000 computational feasibility study

MS-000 asks whether a minimum open-source stack can represent and test the IR-C2 pathway proposed by Cowie et al.
It is a planning and source-analysis record. It contains no quantum-chemistry result and does not reproduce the
paper's pathway.

The study found a technically credible conditional stack built around ASE, CP2K, and AiiDA. A second
implementation of ωB97X-D3 is a required validation capability, with Psi4 as the optional candidate package; the
xtb engine is an optional GFN0 cross-check. Sella and OVITO are optional for later pathway analysis and
visualization. The stack is conditional because the public paper does not provide the model coordinates, QM/MM
partition, boundary treatment, basis and ECP choices, coupling scheme, or complete driven-coordinate protocol. No
open-source implementation has yet been shown equivalent to the unpublished setup.

## Records

| Document | Purpose |
|---|---|
| [Closure record](CLOSURE.md) | Disposes the six gate criteria and gives the bounded verdict, the dependency classes, tool dispositions, requirement mapping, tolerance procedure, unresolved gaps and the stage preconditions of both MS-001 scope options |
| [Compute spike](MS-000-COMPUTE-SPIKE.md) | Extracts the benchmark method, separates experimental and computational evidence, maps requirements to tools, records parity gaps, and defines prospective acceptance criteria |
| [Architecture](ARCHITECTURE.md) | Assigns responsibility among research orchestration, workflow provenance, scientific engines, structure tools, and human review |
| [Evidence policy](EVIDENCE-POLICY.md) | Defines evidence classes and the provenance required before a calculation may support a scientific claim |
| [Open-source landscape](OPEN-SOURCE-LANDSCAPE.md) | Evaluates candidate packages by purpose, licence, maintenance, platform support, dependencies, cost, integration, overlap, and MS-001 relevance |
| [Source ledger](SOURCE-LEDGER.md) | Gives direct links, access status, versions, locators, and SHA256 values for the literature and software sources used |
| [ASE smoke record](SMOKE-AND-ENVIRONMENT-RECORD.md) | Records a bounded ASE 3.29.0 import and extxyz round-trip test, its environment, results, limits, and private raw-record digests |

## Current conclusion

The MS-000 gate is the six feasibility criteria of the compute spike (§8.1). All six are met, including independent
scientific review of the plan, and the gate is **PASS**
([closure record §2](CLOSURE.md#2-gate-disposition)). The gate judges a plan. MS-001 faithful reproduction remains
**blocked**. It needs the missing trajectory inputs and the method-parity and coupling evidence, and authorization
alone would not supply either. A declared-deviation study could test whether the reported qualitative event order
appears under a fully specified open-source setup, but that would be a new computational prediction rather than a
reproduction of the Cowie calculation. Neither scope option is selected, human authorization of MS-001 is absent,
and this package authorizes no calculation.

The central mapping is:

| Cowie method element | Required capability | Candidate implementation | Unresolved issue |
|---|---|---|---|
| H:Si(100)-2x1 substrate and IR dangling-bond pair | Stable atom identities, surfaces, constraints | ASE | Source geometry and termination are unavailable |
| EAOGe-C2 radical tool | Molecular structure and constrained placement | ASE with a chemistry engine | Source coordinates and leg-binding configuration are unavailable |
| GFN0/DFT two-level calculation | GFN0-xTB, omega-B97X-D3, coupled energies and forces | CP2K, with a second omega-B97X-D3 implementation (Psi4 or another engine) required for validation and xTB optional | Partition, embedding, link treatment, basis, ECP, and coupling scheme are unavailable or unvalidated |
| Controlled approach and retraction | History-preserving constrained optimization | ASE constraints and optimizers; Sella optional | The paper's exact drive definition is unavailable; ordinary NEB is not a substitute |
| Scientific execution and provenance | Versioned inputs, calculations, outputs, failures, and restarts | AiiDA with `aiida-cp2k` | Integration remains to be tested before a scientific run |
| Atomic visualization | Rendering from computed coordinates | ASE and optional OVITO | No computed pathway coordinates exist yet |

All package conclusions are bounded by the source status in the [ledger](SOURCE-LEDGER.md). The benchmark
Supplementary Information was not obtained for MS-000, and every conclusion that depends on it remains marked as
a gap.
