# di-mechanosynthesis

This project investigates computational models of mechanically controlled carbon transfer on hydrogenated
Si(100). The initial reference is the IR-C2 donation pathway reported by Cowie et al. [1]. In that pathway, a
germanium-based molecular tool transfers a C2 unit to a pair of dangling bonds on a hydrogen-passivated silicon
surface under inverted-mode scanning tunnelling microscopy. The present work defines candidate structures for the
tool and an electronic-structure validation protocol, which are prerequisites for modelling the coupled
tool–surface system. The repository is an active research record that is revised as sources are examined and
calculations are specified. It does not yet contain quantum-chemistry results, and it does not reproduce any
experiment, model or calculation from the benchmark study.

<p align="center">
  <img src="docs/figures/activated-donor.svg" width="720"
       alt="Heavy-atom ball-and-stick rendering of the proposed activated donor candidate EAOGe-C2 radical, an unoptimized input geometry; hydrogen atoms omitted.">
</p>

Figure 1. Heavy atoms of the proposed activated donor candidate EAOGe-C2• (C17H27GeO3), drawn from the unchanged
coordinates in
[`structures/donor-activated-EAOGe-C2-radical.extxyz`](structures/donor-activated-EAOGe-C2-radical.extxyz). The
geometry is an unoptimized RDKit ETKDGv3 embedding proposed as a calculation input. It is neither a validated
structure nor the benchmark authors' coordinate set. Hydrogen atoms are omitted, and Cα and Cβ denote atoms `D-Ca`
and `D-Cb`. Rendering details are given in [docs/donor-candidates.md](docs/donor-candidates.md).

## Background

Inverted-mode scanning tunnelling microscopy (IM-STM) was introduced by Barrera et al. as a means of performing
mechanically controlled chemical reactions for atomically precise fabrication [2]. Tall molecules deposited
sparsely on a Si(100) sample image the apex of a flat silicon probe chip [1, 2]. Because the same molecules can react with
that apex, the two sides of the tunnel junction act as reagents positioned with sub-ångström precision. Blue et al.
subsequently reported positionally controlled donation of carbon and abstraction of silicon on atomically clean
Si(100) [3].

The molecular tool used by Cowie et al., EAOGe-C2I, is a germanium-substituted adamantane. It carries a C2 group
capped by iodine and three OH-terminated legs that anchor the molecule to the silicon sample [1]. The build site
is the hydrogen-passivated Si(100) apex of the probe chip, which is pre-patterned with reactive dangling-bond
sites. In the reaction considered here, the de-iodinated tool is positioned with its distal carbon atom beneath an
inter-row dangling-bond (IR-DB) pair, and it transfers its C2 unit to the build site.

## The benchmark study

Cowie et al. report atomically precise mechanosynthesis of carbon structures on hydrogenated Si(100) by IM-STM at
4 K [1]. The work is a preprint (arXiv:2605.27250v1, submitted 26 May 2026), and no peer-review status is claimed
for it here. The authors state that Supplementary Information is available upon request, but this project has not
obtained it. The authors report per-interaction target formation for four build targets in the section "Positional
and chemical control of mechanosynthetic donation".

| Target | Reported outcome | Reported percentage | Reported 95% CI |
|---|---|---|---|
| IR-C2 | 184 / 197 | 93% | 89–96% |
| 2IR-C2 | 71 / 73 | 97% | 91–99% |
| IR-C2/C4 | 45 / 49 | 92% | 81–97% |
| 2IR-C4 | 27 / 32 | 84% | 68–93% |

These are separate interaction counts reported by the authors, not results of this project. They do not describe
independent full-build events or throughput, and they are not multiplied here into a build-success probability.

The same paper proposes a mechanism for IR-C2 formation based on a QM/MM model that combines xTB (GFN0) with DFT
(ωB97X-D3) [1, Fig. 3]. The mechanism proceeds in three steps:

1. The de-iodinated tool is positioned beneath an IR-DB pair.
2. A first C–Si bond forms as the tool approaches.
3. The Ge–C bond cleaves on retraction, transferring the C2 unit.

The authors present the configuration shown as one representative leg-binding arrangement among several. The
mechanism is a computational proposal, distinct from the experimental counts, and it has not been reproduced here.
A fuller account with locators is given in [docs/benchmark.md](docs/benchmark.md).

## Research aims

The longer-term objective is a reviewed and reproducible computational description of mechanically controlled
reactions. Tool approach, contact and retraction would be described along controlled mechanical coordinates.
Individual donation and abstraction events would be characterized as reaction primitives with defined inputs,
observables and limits of validity. Energy landscapes along these coordinates would then be evaluated
reproducibly, including competing and off-target channels and the dependence of outcomes on approach depth, step
size, lateral offset and tool conformation. Once primitives have been validated, the same framework could be used
to study how they might be sequenced into larger atomically precise structures. Questions of throughput, error
handling and repair are treated as hypotheses until evidence addresses them. These capabilities do not yet exist.

## Present scope

Two candidate geometries represent the benchmark tool in its iodinated (precursor) and de-iodinated (activated)
forms.

| Candidate | Atoms | Formula | Charge / multiplicity |
|---|---|---|---|
| Precursor | 49 | C17H27GeIO3 | 0 / 1 |
| Activated | 48 | C17H27GeO3 | 0 / 2 |

Both geometries are RDKit ETKDGv3 distance-geometry embeddings with seed 20260916 [13], obtained without a force
field, quantum-chemical step or relaxation. Every atom carries a stable identifier, and the all-electron counts of
238 and 185 have the parity expected for a singlet and a doublet respectively. The identity of the donor rests on
literature statements recorded in the project's original reconstruction notes. The coordinates have not been
compared with the benchmark authors' supplementary coordinates. The atom-mapped SMILES, the identifier table and
the Figure 1 rendering method are given in [docs/donor-candidates.md](docs/donor-candidates.md), and the
coordinate files are described in [structures/README.md](structures/README.md).

The reconstruction also defined three unoptimized silicon surface models. The first is a periodic H:Si(100)-(2×1)
slab with one IR-DB pair; the second is a finite cluster built with the same pair rule; the third is a clean
Si(100)-(2×1) comparator cluster with a C2 placeholder. They were constructed on an ASE `diamond100` lattice [14]
with geometric dimer formation and hydrogen capping. Their coordinate files are not published, because they are
not inputs to the first calculation and they contain placeholder geometry.

The first calculation, designated E-01, is specified prospectively in
[docs/e01-method-specification.md](docs/e01-method-specification.md) and has not been run. It asks whether the
selected engine setup runs correctly on the two free donor candidates at fixed geometry. The setup is Psi4 1.11
with the ωB97X-D3 functional, 6-31G(d,p) on all atoms except iodine, and LANL2DZ with its effective core potential
on iodine [6, 7]. The criteria cover SCF convergence from several initial guesses, agreement between analytic and
finite-difference gradients, spin contamination and run-to-run reproducibility. A radical-localization hypothesis
for the activated donor is reported separately, and several clarifications of the specification remain open.

Whether Psi4 1.11 provides each capability the calculation requires is examined in
[docs/engine-capability-status.md](docs/engine-capability-status.md). The inspected documentation is the
development manual (version string `1.12a1.dev35`) [7], together with two source files from the `v1.11` tag
[9, 10]. As a result, most capabilities remain unverified for an installed 1.11 build. The v1.11 source declares a
`wB97X-D3` entry built from the Libxc identifier `HYB_GGA_XC_WB97X_D3` with a `d3zero2b` dispersion term [10].
Whether this entry is equivalent to the functional used in the benchmark calculations has not been established.

## Evidence classification and provenance

Scientific claims are classified by their underlying evidence as experimentally demonstrated (`[EXP]`),
computationally reproduced by this project (`[COMP-REPRO]`), computationally predicted (`[COMP-PRED]`),
literature-derived (`[LIT]`), agent-proposed (`[AGENT]`) or speculative (`[SPEC]`). The literature-derived label
records provenance alongside the underlying class. An unavailable input is marked `[GAP]` and blocks the claims
that depend on it. Classifications are not upgraded by restatement, summary or agreement between agents, and
output from language models is never treated as physical evidence. The rules are set out in
[docs/evidence-policy.md](docs/evidence-policy.md).

Every public file is listed with its SHA256 in [provenance/EXPORT-MANIFEST.md](provenance/EXPORT-MANIFEST.md),
which excludes itself from its own table. Where a file was adapted from a private working record, the manifest
states the change and gives the hash of the original. Figure 1 is drawn directly from repository data by the
included script. A software capability is accepted only when it is shown for the exact version used.

The work is coordinated through a separate orchestration and review system, Dodging Infinity. That system
authorizes bounded tasks, conducts independent review and records evidence status. This repository holds the
scientific content, and none of its documents authorizes computation. Conventions for contributors and automated
agents are given in [AGENTS.md](AGENTS.md).

## Computational tools

The table lists each tool with its current status in the project. Numbers refer to the catalogue in
[docs/SOURCES.md](docs/SOURCES.md).

| Tool | Status here | Role |
|---|---|---|
| RDKit [13]; ASE [14] | Used in preparation, without quantum chemistry | Donor-candidate embeddings; structure building and extxyz input and output |
| Psi4 1.11 [6] | Selected; not installed or validated here | Electronic-structure engine for the first calculation |
| AiiDA [12] | Selected provenance system | Scientific job execution and computational provenance |
| xtb [15] | Candidate, documentation only | GFN0-xTB, the benchmark's QM/MM partner method; the xtb documentation describes a GFN0 parameter file |
| CP2K [16] | Candidate, documentation only | Periodic and QM/MM engine whose manual documents an internal GFN0-xTB option |
| tblite [17] | Candidate, documentation only | Tight-binding library whose documentation lists GFN1-xTB, GFN2-xTB and IPEA1-xTB but not GFN0; not a substitute for the GFN0 route |
| QCFractal [18]; OVITO [19] | Candidates, documentation only | Alternative workflow store (deferred); rendering of computed coordinates |

## Repository contents

The public export covers the donor candidates and their documentation. The surface-model coordinate files and the
project's private working records are omitted, and the manifest lists each omission with its reason.

| Path | Contents |
|---|---|
| [docs/SOURCES.md](docs/SOURCES.md) | Numbered catalogue of literature, software documentation, method sources and figure inputs |
| [docs/benchmark.md](docs/benchmark.md) | Attribution, reported observations and proposed mechanism of the benchmark study |
| [docs/evidence-policy.md](docs/evidence-policy.md) | Evidence classes, classification rules and provenance requirements |
| [docs/donor-candidates.md](docs/donor-candidates.md) | Donor identity, molecular graph, atom identifiers, electron bookkeeping, surface models and Figure 1 method |
| [docs/e01-method-specification.md](docs/e01-method-specification.md) | Prospective specification of the first calculation |
| [docs/engine-capability-status.md](docs/engine-capability-status.md) | Capabilities of Psi4 1.11 as established, or not, by archived primary sources |
| [docs/figures/activated-donor.svg](docs/figures/activated-donor.svg) | Figure 1 |
| [tools/](tools/render_donor_plate.py) | Figure 1 renderer and its bond table |
| [structures/](structures/README.md) | Donor-candidate coordinate files |
| [AGENTS.md](AGENTS.md) | Conventions for contributors and automated agents |
| [provenance/EXPORT-MANIFEST.md](provenance/EXPORT-MANIFEST.md) | Per-file SHA256, derivation and redaction statements |

## Contributing and licence

Corrections are welcome, particularly those that bring a primary source to bear on a statement marked unverified.
An issue should identify the source exactly, by identifier, version and page, section or line, and should name the
statement it supports or contradicts. Claims without a checkable source are recorded as proposals rather than
evidence.

No licence has been selected for this repository, and no licence is therefore granted. Third-party works are cited
rather than included. Paper text, figures, supplementary material and vendor source code were excluded from this
export pending redistribution review. Work that builds on the benchmark should cite the original preprint [1].

## References

1. Cowie, M. *et al.* Atomically precise mechanosynthesis of carbon structures on hydrogenated Si(100) by
   inverted-mode STM. arXiv:2605.27250v1 (2026). <https://doi.org/10.48550/arXiv.2605.27250>
2. Barrera, E. *et al.* Inverted-Mode Scanning Tunneling Microscopy for Atomically Precise Fabrication.
   arXiv:2512.24431 (2025). <https://doi.org/10.48550/arXiv.2512.24431>
3. Blue, B. *et al.* Towards Atom-by-Atom Fabrication: Mechanosynthetic donation and abstraction.
   arXiv:2606.13876 (2026). <https://doi.org/10.48550/arXiv.2606.13876>

References [4] to [19], covering further literature and software documentation, are catalogued with versions,
locators, verification basis and limitations in [docs/SOURCES.md](docs/SOURCES.md), which uses the same numbering.
