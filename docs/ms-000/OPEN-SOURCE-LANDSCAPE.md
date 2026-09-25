# MS-000 Open-Source Landscape and Conditional Minimum Stack

Status: public adaptation of the MS-000 package assessment. The stack in
[Section 3](#3-conditional-minimum-stack-for-ms-001) is **CONDITIONAL** on the open parity gaps in
[MS-000-COMPUTE-SPIKE.md §4](MS-000-COMPUTE-SPIKE.md#4-parity-gaps-that-keep-the-stack-conditional), including the
coupling-route gap (P3b) recorded there and evaluated reuse-first in
[Section 4](#4-coupling-route-candidates-p3b-existing-tooling-evaluated-reuse-first) here.

Companion documents: [MS-000-COMPUTE-SPIKE.md](MS-000-COMPUTE-SPIKE.md), [ARCHITECTURE.md](ARCHITECTURE.md),
[EVIDENCE-POLICY.md](EVIDENCE-POLICY.md), [SOURCE-LEDGER.md](SOURCE-LEDGER.md),
[SMOKE-AND-ENVIRONMENT-RECORD.md](SMOKE-AND-ENVIRONMENT-RECORD.md).

## 0. Field schema and evidence classes

All eleven fields are mandatory for every tool. **Evidence class is per field, not per table:**

- Fields **(1) purpose, (2) license, (3) maintenance, (4) install feasibility, (5) macOS/arm64, (6) Python,
  (7) external binaries/services** are **`[LIT]` sourced facts** from official repositories, docs, package
  indexes and license files retrieved 2026-09-16 (`[S-…]` tags resolve in SOURCE-LEDGER.md), or `UNVERIFIED` with
  the attempts listed. "Feasibility" and "compatibility" are documented, not tested on this machine, except the
  single ASE import/IO smoke test, which is an environment fact and not chemistry evidence.
- Fields **(8) qualitative cost, (9) integration path, (10) overlap, (11) adopt/defer/reject** are **`[AGENT]`
  judgments** by this program. Cost statements are qualitative expectations, unmeasured; no Cowie wall-clock
  estimate exists and none is implied. Where a cost statement is structural (a library computes no energies), it
  is stated as such.

Nothing here was executed except the smoke test in SMOKE-AND-ENVIRONMENT-RECORD.md.

---

## 1. Required tools

### ASE (Atomic Simulation Environment)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Python library for building, manipulating, reading/writing atomic structures, constraints, optimizers, NEB, and calculator interfaces to engines; includes simple viewers | [S-gl-ase] description; [S-ase-neb]; [S-ase-constraints]; [S-ase-calculators] |
| 2 | License | `[LIT]` | LGPL-2.1-or-later | [S-gl-ase-license]; [S-ase-about]; [S-pypi-ase] |
| 3 | Maintenance | `[LIT]` | 3.29.0 on PyPI 2026-06-21; GitLab last activity 2026-09-15 | [S-pypi-ase]; [S-gl-ase] |
| 4 | Install | `[LIT]` | pip; pure-Python wheel; conda-forge noarch 3.29.0 (2026-06-22) | [S-ase-install]; [S-pypi-ase]; [S-conda-ase] |
| 5 | macOS/arm64 | `[LIT]` + smoke fact | Docs cover Mac Python via Homebrew and warn against the system Python. Imported and round-tripped extxyz on this arm64 host in smoke attempt 2 (`install_exit=0`, `smoke_exit=0`); attempt 1 failed at exit 127 before any install. Import/IO fact only | [S-ase-install]; SMOKE-AND-ENVIRONMENT-RECORD.md |
| 6 | Python | `[LIT]` (discrepancy) | Docs: 3.11 or newer; PyPI 3.29.0 metadata: `>=3.10`, classifiers 3.10–3.12. Both recorded; plan for ≥3.11 | [S-ase-install]; [S-pypi-ase] |
| 7 | External | `[LIT]` | NumPy, SciPy, Matplotlib; energies/forces require an external calculator | [S-ase-install] |
| 8 | Cost | `[AGENT]` | Structural: ASE computes no energies; cost is the attached engine's | Not applicable |
| 9 | Integration | `[AGENT]` | Structure/constraint/IO layer shared by engines and AiiDA plugins; `FixAtoms` etc. for the driven scan; `ase.mep.neb.NEB` for optional supporting NEB; `ase.calculators.cp2k.CP2K` shell interface | [S-ase-constraints]; [S-ase-neb]; [S-ase-cp2k] |
| 10 | Overlap | `[AGENT]` | pyiron/atomate2 wrap ASE; Sella/Pynta/autodE depend on ASE; ASE's viewer overlaps OVITO for basic rendering | Not applicable |
| 11 | Decision | `[AGENT]` | **ADOPT (required runtime).** Cited by Cowie (ref 50), LGPL, minimal | MS-000-COMPUTE-SPIKE.md §1.2 |

### Pynta (`zadorlab/pynta`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Automated workflow for thermochemistry and rate coefficients of reactions on **metallic surfaces**; GitHub description: reaction path exploration on metallic surfaces. Not the nanoparticle-tracking "PyNTA" on PyPI (`pynta` 0.1.4, 2019, Windows classifier) | [S-pynta-readme] para 1; [S-gh-pynta]; [S-pypi-pynta] |
| 2 | License | `[LIT]` | GPL-3.0 (LICENSE with Sandia header; README GPLv3 badge) | [S-pynta-license]; [S-pynta-readme] |
| 3 | Maintenance | `[LIT]` | Repo pushed 2026-09-13; latest tagged release v2.0.0 2023-05-26 | [S-gh-pynta] |
| 4 | Install | `[LIT]` | Source with conda env; docs list installing MongoDB and setting up Fireworks | [S-pynta-docs] |
| 5 | macOS/arm64 | `UNVERIFIED` | No platform statement in README or docs index retrieved | [S-pynta-docs]; [S-pynta-readme] |
| 6 | Python | `UNVERIFIED` | No `setup.py`/`pyproject.toml` at repo root (404 on master and main); `environment.yml` present but not retrieved | [S-pynta-contents] |
| 7 | External | `[LIT]` | Fireworks workflow engine and MongoDB; ASE; Sella; an electronic-structure engine | [S-pynta-readme]; [S-pynta-docs] |
| 8 | Cost | `[AGENT]` | Workflow overhead aside, it launches many engine calculations by design (README describes spawning large numbers of calculations) | [S-pynta-readme] para 2 |
| 9 | Integration | `[AGENT]` | Would sit as a workflow layer above ASE/Sella | Not applicable |
| 10 | Overlap | `[AGENT]` | Fireworks + MongoDB duplicate the workflow/provenance role assigned to AiiDA; Sella already separately available | Not applicable |
| 11 | Decision | `[AGENT]` | **REJECT for MS-001**, two locator-backed reasons: (a) target domain is metallic-surface heterogeneous catalysis ([S-pynta-readme] paras 1–2), not H:Si(100) mechanosynthesis with a driven tool; (b) it depends on a **second workflow engine**, Fireworks ([S-pynta-readme]), plus MongoDB ([S-pynta-docs]) | ARCHITECTURE.md §2 |

### SCINE Chemoton

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Automated exploration of chemical reaction networks with quantum chemical methods; calculations are dispatched through the back-end SCINE Puffin | [S-chemoton-readme] Introduction |
| 2 | License | `[LIT]` | BSD 3-Clause (ETH Zurich, Reiher group) | [S-chemoton-license]; [S-chemoton-readme] |
| 3 | Maintenance | `[LIT]` | Release 4.1.0 2025-10-09; repo pushed 2025-10-09 | [S-gh-chemoton]; [S-pypi-chemoton] |
| 4 | Install | `[LIT]` | pip from the cloned repo; requires `scine_utilities`, `scine_database`, `scine_molassember`; PyPI ships an sdist only | [S-chemoton-readme]; [S-pypi-chemoton] |
| 5 | macOS/arm64 | `UNVERIFIED` | No platform statement found for Chemoton itself | [S-chemoton-readme] |
| 6 | Python | `[LIT]` | PyPI `requires_python >=3.6` | [S-pypi-chemoton] |
| 7 | External | `[LIT]` | SCINE database (MongoDB, per Puffin's requirements) and SCINE C++ components; Puffin as calculation back-end | [S-chemoton-readme]; [S-puffin-readme] |
| 8 | Cost | `[AGENT]` | Exploration workflows generate many calculations; not needed for a single driven scan | Not applicable |
| 9 | Integration | `[AGENT]` | Not needed by MS-001, which is one driven-scan protocol (spike M4), not a network exploration | Not applicable |
| 10 | Overlap | `[AGENT]` | Its database/handler pair (Puffin + MongoDB) overlaps the job-execution/provenance role assigned to AiiDA for this program | Not applicable |
| 11 | Decision | `[AGENT]` | **DEFER**, scoped to this study: MS-001 has no network-exploration requirement. Re-evaluate at MS-004 (competing hypotheses), where exploration tooling may be relevant | ARCHITECTURE.md §3 |

### SCINE Puffin

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Calculation handler for SCINE Chemoton, bridging exploration jobs and quantum chemical calculations across supported programs and schedulers | [S-puffin-readme] Introduction |
| 2 | License | `[LIT]` | BSD 3-Clause (ETH Zurich, Reiher group) | [S-puffin-license] |
| 3 | Maintenance | `[LIT]` | Release 2.1.0 2025-10-09; repo pushed 2025-10-09 | [S-gh-puffin]; [S-pypi-puffin] |
| 4 | Install | `[LIT]` | pip or source; an instance bootstraps SCINE C++ components; needs CMake ≥3.12, Git, GCC ≥7 / Clang ≥6, Boost ≥1.64, MongoDB with C++ bindings; a containerized version is offered | [S-puffin-readme]; [S-scine-puffin-web] |
| 5 | macOS/arm64 | `[LIT]` (partial) | README: expected to run on Linux and possibly on OSX; Windows not specifically supported; arm64 not stated → `UNVERIFIED` for arm64 | [S-puffin-readme] |
| 6 | Python | `[LIT]` | PyPI `requires_python >=3.6` | [S-pypi-puffin] |
| 7 | External | `[LIT]` | MongoDB; SCINE database and other C++ components; the engines it wraps | [S-puffin-readme] |
| 8 | Cost | `[AGENT]` | Handler overhead only; engine cost dominates | Not applicable |
| 9 | Integration | `[AGENT]` | Designed as Chemoton's calculation handler; no MS-001 requirement for it | Not applicable |
| 10 | Overlap | `[AGENT]` | Job execution/provenance role already assigned to AiiDA for this program | Not applicable |
| 11 | Decision | `[AGENT]` | **DEFER**, scoped to this study (no stronger limitation is claimed) | Not applicable |

### xTB (`grimme-lab/xtb`, the engine)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Semiempirical extended tight-binding program package; GFN0-xTB, GFN1-xTB, GFN2-xTB, GFN-FF | [S-gh-xtb]; [S-xtb-setup] |
| 2 | License | `[LIT]` | LGPL-3.0-or-later (README License section; COPYING.LESSER; COPYING holds the GPLv3 text) | [S-xtb-readme]; [S-xtb-lgpl]; [S-xtb-gpl] |
| 3 | Maintenance | `[LIT]` | Repo pushed 2026-09-11; latest tagged release v6.7.1 2024-07-23; conda-forge 6.7.1 rebuilt 2026-06-10 | [S-gh-xtb]; [S-conda-xtb] |
| 4 | Install | `[LIT]` | conda-forge; Homebrew tap `grimme-lab/homebrew-qc`; or source (meson/CMake, gfortran, BLAS/LAPACK) | [S-xtb-readme] |
| 5 | macOS/arm64 | `[LIT]` | README: conda-forge packages for macOS x86_64 and arm64; Homebrew tap compiles arm64 on install; known issue listed for GCC-13 with macOS AArch64; README warns different BLAS libraries can give deviating results in rare cases on macOS builds; conda-forge lists osx-arm64 for 6.7.1 | [S-xtb-readme]; [S-conda-xtb] |
| 6 | Python | `[LIT]` | Not a Python package; Python access via xtb-python (deprecated) or tblite (no GFN0), see below | Not applicable |
| 7 | External | `[LIT]` | gfortran runtime, BLAS/LAPACK; parameter files located via `XTBPATH` | [S-xtb-setup] |
| 8 | Cost | `[AGENT]` | Semi-empirical tight-binding: expected cheaper per evaluation than hybrid DFT on the same atoms (qualitative, unmeasured) | Not applicable |
| 9 | Integration | `[AGENT]` | CLI `xtb --gfn 0` via a file wrapper from ASE; GFN0 must be selected explicitly each time because `--gfn INT` defaults to 2 ([S-xtb-cli]) | [S-xtb-cli] |
| 10 | Overlap | `[AGENT]` | CP2K-internal GFN0 (different implementation of the same named method; equivalence `UNVERIFIED`); tblite (no GFN0) | [S-cp2k-xtb] |
| 11 | Decision | `[AGENT]` | **ADOPT as a conditional reference/validation utility, not a runtime minimum:** an independent GFN0 implementation for cross-implementation comparison and parameter-file provenance (spike P1). If omitted, CP2K's internal GFN0 remains usable and identity provenance (selector/banner/version/parameters) is still possible; only the cross-implementation comparison is lost | MS-000-COMPUTE-SPIKE.md §4 P1 |

### xtb-python and tblite (Python routes to xTB; assessed because P1 depends on them)

| # | Field | xtb-python (`grimme-lab/xtb-python`) | tblite (`tblite/tblite`) |
|---|---|---|---|
| 1 | Purpose `[LIT]` | Python API for the xtb package incl. an ASE calculator [S-gh-xtbpy] | Light-weight tight-binding framework with Python/ASE API [S-gh-tblite] |
| 2 | License `[LIT]` | LGPL-3.0 [S-gh-xtbpy]; PyPI LGPL-3.0-or-later [S-pypi-xtb] | LGPL-3.0-or-later [S-gh-tblite]; [S-pypi-tblite]; [S-tblite-readme] |
| 3 | Maintenance `[LIT]` | README states the project is no longer in active development and recommends tblite [S-xtbpy-readme]; last release v22.1 2022-12-31; repo pushed 2024-09-03 [S-gh-xtbpy] | v0.7.0 2026-07-13; repo pushed 2026-09-02 [S-gh-tblite] |
| 4 | Install `[LIT]` | PyPI 22.1 wheels Linux x86_64 only [S-pypi-xtb]; conda-forge 22.1 (2024-11-27) [S-conda-xtb-python] | PyPI 0.7.0 wheels incl. macosx arm64 cp310–cp314 [S-pypi-tblite]; conda-forge 0.7.0 [S-conda-tblite] |
| 5 | macOS/arm64 `[LIT]` | conda-forge lists osx-arm64 builds of 22.1; PyPI wheels do not; untested here | PyPI and conda-forge list arm64; untested here |
| 6 | Python `[LIT]` | `>=3.7`, classifiers to 3.11 [S-pypi-xtb] | `>=3.7`, classifiers to 3.13 [S-pypi-tblite] |
| 7 | External `[LIT]` | Bundles the xtb API; GFN0 (`GFN0xTB = 3`) requires `param_gfn0-xtb.txt` via `XTBPATH` [S-xtbpy-api]; ASE calculator default method GFN2-xTB [S-xtbpy-ase] | BLAS; built-in methods GFN1-xTB, GFN2-xTB, IPEA1-xTB only [S-tblite-methods]; ASE calculator default GFN2-xTB [S-tblite-ase] |
| 8 | Cost `[AGENT]` | As xtb | As xtb |
| 9 | Integration `[AGENT]` | ASE calculator; GFN0 only with explicit method and `XTBPATH` | ASE calculator; cannot supply GFN0 |
| 10 | Overlap `[AGENT]` | Both wrap xTB-family methods; tblite is the upstream-recommended successor | Not applicable |
| 11 | Decision `[AGENT]` | **DEFER**: deprecated upstream, stale PyPI wheels; use the xtb CLI unless an arm64 compatibility test passes | **REJECT for GFN0** (method absent); acceptable only for non-GFN0 sanity checks |

### Sella

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Saddle-point optimization and minimization of atomic systems; ASE-based with a `Constraints` object | [S-gh-sella]; [S-sella-readme] |
| 2 | License | `[LIT]` | LGPL-3.0 (LICENSE with Sandia header; PyPI LGPL-3.0) | [S-sella-license]; [S-pypi-sella] |
| 3 | Maintenance | `[LIT]` | v2.6.0 GitHub 2026-09-09, PyPI 2026-09-02; repo pushed 2026-09-02 | [S-gh-sella]; [S-pypi-sella] |
| 4 | Install | `[LIT]` | pip (universal wheel); conda-forge noarch 2.6.0 | [S-pypi-sella]; [S-conda-sella] |
| 5 | macOS/arm64 | `[LIT]` | Pure-Python wheel; compiled numerics via NumPy/SciPy; untested here | [S-pypi-sella] |
| 6 | Python | `[LIT]` | `>=3.9`, classifiers 3.9–3.13 | [S-pypi-sella] |
| 7 | External | `[LIT]` | ASE, NumPy/SciPy; an ASE calculator for forces | [S-sella-readme] |
| 8 | Cost | `[AGENT]` | Repeated force evaluations; saddle searches need more evaluations than minimizations (qualitative) | Not applicable |
| 9 | Integration | `[AGENT]` | Constrained minimization per z step (alternative to ASE optimizers); optional saddle refinement for the P4 supporting analysis | Not applicable |
| 10 | Overlap | `[AGENT]` | ASE optimizers and NEB; CP2K internal optimizers | Not applicable |
| 11 | Decision | `[AGENT]` | **DEFER (optional).** Only if a specific saddle question is approved as supporting analysis | MS-000-COMPUTE-SPIKE.md §8.4 |

### ASE NEB (`ase.mep.neb`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Nudged elastic band over a chain of images between fixed endpoints; climbing-image option (cites Henkelman 2000, Cowie ref 54) | [S-ase-neb] |
| 2 | License | `[LIT]` | Part of ASE, LGPL-2.1-or-later | [S-gl-ase-license] |
| 3 | Maintenance | `[LIT]` | As ASE | [S-pypi-ase] |
| 4 | Install | `[LIT]` | Included in ASE | [S-ase-neb] |
| 5 | macOS/arm64 | `[LIT]` | As ASE | Not applicable |
| 6 | Python | `[LIT]` | As ASE | Not applicable |
| 7 | External | `[LIT]` | An engine per image | Not applicable |
| 8 | Cost | `[AGENT]` | Engine cost multiplied by the number of images (structural) | Not applicable |
| 9 | Integration | `[AGENT]` | **Supporting analysis only** at fixed large z | MS-000-COMPUTE-SPIKE.md §4 P4 |
| 10 | Overlap | `[AGENT]` | Sella saddle search; CP2K band methods (not evaluated) | Not applicable |
| 11 | Decision | `[AGENT]` | **ADOPT as optional supporting analysis; never a substitute for the driven trajectory** (no drive, no branches, no history) | MS-000-COMPUTE-SPIKE.md §4 P4 |

### CP2K

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Quantum chemistry and solid-state physics package: GPW DFT with libxc functionals, an HF exchange section, D3/D4 pair potentials, an internal xTB module (GFN0/GFN1/tblite), and a QM/MM section | [S-gh-cp2k]; [S-cp2k-xc]; [S-cp2k-hf]; [S-cp2k-vdw]; [S-cp2k-xtb]; [S-cp2k-qmmm] |
| 2 | License | `[LIT]` | GPL-2.0 (LICENSE; conda-forge GPL-2.0-only) | [S-cp2k-license]; [S-conda-cp2k] |
| 3 | Maintenance | `[LIT]` | v2026.2 released 2026-07-15; repo pushed 2026-09-16; download page names the `support/v2026.2` branch | [S-gh-cp2k]; [S-cp2k-download] |
| 4 | Install | `[LIT]` | Source toolchain, Spack, Homebrew; conda-forge 2026.2 for linux-64 only (osx-64 in older versions; no osx-arm64) | [S-cp2k-install]; [S-conda-cp2k] |
| 5 | macOS/arm64 | `[LIT]` | Installation page: macOS on Apple Silicon M1 is regularly tested, Spack/Homebrew recommended. Not installed on this host | [S-cp2k-install]; SMOKE-AND-ENVIRONMENT-RECORD.md §1 |
| 6 | Python | `[LIT]` | Not a Python package; driven via ASE's CP2K calculator (shell mode, default command `cp2k.psmp -s`) or `aiida-cp2k` 2.1.1 (`>=3.9`) | [S-ase-cp2k]; [S-pypi-aiida-cp2k] |
| 7 | External | `[LIT]` | Compiled Fortran binary with MPI/OpenMP and numerical libraries; basis and pseudopotential data files; optional `s-dftd3` library for D3 parameters | [S-ase-cp2k]; [S-cp2k-vdw] |
| 8 | Cost | `[AGENT]` | Hybrid DFT with exact exchange on a Ge/I-containing slab or cluster is expected to be the dominant cost of any MS-001 run; the GFN0 part is expected minor (qualitative, unmeasured) | Not applicable |
| 9 | Integration | `[AGENT]` over `[LIT]` facts | Feature inventory (facts): (a) `GFN_TYPE` enum default 1, values 0/1/TBLITE, 0 = internal GFN0-xTB [S-cp2k-xtb]; (b) `WB97X_D3` listed among libxc hybrid GGA entries, with hybrid parameters set in the HF section [S-cp2k-xc], [S-cp2k-hf]; (c) `PAIR_POTENTIAL TYPE` default DFTD3(BJ), reference-functional lookup [S-cp2k-vdw]; (d) QMMM `E_COUPL` default NONE with options for coupling a QM region to a **classical MM** region, and a LINK section [S-cp2k-qmmm]. **Judgment:** these are separate features; the inventory alone does not establish a two-level xTB/DFT coupling. CP2K's own `MIXED`/`GENMIX` section is one of the existing composition candidates evaluated in Section 4.2 (P3b) | Not applicable |
| 10 | Overlap | `[AGENT]` | xtb engine (GFN0), Psi4 (molecular hybrid DFT), ASE NEB/optimizers | Not applicable |
| 11 | Decision | `[AGENT]` | **ADOPT as the conditional required engine** for the DFT level and, if a supported route exists, the coupling. **CP2K availability is not proof of parity.** ASE's CP2K calculator defaults (`xc` LDA, `charge` 0, `basis_set` DZVP-MOLOPT-SR-GTH, `multiplicity` None per [S-ase-cp2k]) must never stand in an MS-001 input | MS-000-COMPUTE-SPIKE.md §4, §5 |

### AiiDA (`aiida-core`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Workflow and provenance engine for computational science | [S-gh-aiida] |
| 2 | License | `[LIT]` | MIT | [S-aiida-license]; [S-pypi-aiida] |
| 3 | Maintenance | `[LIT]` | v2.9.2 2026-09-03; repo pushed 2026-09-15 | [S-gh-aiida]; [S-pypi-aiida] |
| 4 | Install | `[LIT]` | pip; `verdi presto` creates a profile with SQLite and either the built-in ZeroMQ broker (new in 2.9) or no broker; PostgreSQL and a broker recommended for production | [S-aiida-quick]; [S-aiida-install] |
| 5 | macOS/arm64 | `[LIT]` | PyPI classifiers macOS and Linux; pure-Python wheel; conda-forge noarch; untested here | [S-pypi-aiida]; [S-conda-aiida] |
| 6 | Python | `[LIT]` | `>=3.10`, classifiers 3.10–3.14 | [S-pypi-aiida] |
| 7 | External | `[LIT]` | None for a small profile (SQLite + built-in ZeroMQ broker); PostgreSQL and RabbitMQ optional | [S-aiida-install] |
| 8 | Cost | `[AGENT]` | Bookkeeping overhead only (structural) | Not applicable |
| 9 | Integration | `[AGENT]` | Owns scientific job execution and provenance; `aiida-cp2k` 2.1.1 (MIT, 2025-02-04) is the CP2K plugin | [S-gh-aiida-cp2k]; [S-aiida-cp2k-readme] |
| 10 | Overlap | `[AGENT]` | QCFractal (alternative), Fireworks/jobflow (via Pynta/atomate2), pyiron | Not applicable |
| 11 | Decision | `[AGENT]` | **ADOPT (required runtime, conditional):** plugin compatibility with the eventual input is untested (`[GAP]`) | ARCHITECTURE.md §2 |

### QCFractal / QCArchive

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Distributed compute and database platform for quantum chemistry; documentation describes handling thousands to millions of computations with a server, client and compute workers | [S-gh-qcfractal]; [S-qcarchive-index] |
| 2 | License | `[LIT]` | BSD 3-Clause (MolSSI) | [S-qcfractal-license] |
| 3 | Maintenance | `[LIT]` | v0.70 2026-08-17; repo pushed 2026-09-14 | [S-gh-qcfractal]; [S-pypi-qcfractal] |
| 4 | Install | `[LIT]` | pip/conda; the server stores data in PostgreSQL (conda-installable; QCFractal can manage it) | [S-qcarchive-setup] |
| 5 | macOS/arm64 | `[LIT]` | PyPI classifiers macOS and Linux; pure-Python wheel; untested here | [S-pypi-qcfractal] |
| 6 | Python | `[LIT]` | `>=3.10` | [S-pypi-qcfractal] |
| 7 | External | `[LIT]` | PostgreSQL; compute managers/workers; QCEngine-wrapped engines | [S-qcarchive-setup]; [S-qcarchive-index] |
| 8 | Cost | `[AGENT]` | Bookkeeping overhead; built for scales beyond MS-001 | Not applicable |
| 9 | Integration | `[AGENT]` | Would replace AiiDA as job/provenance owner; molecule-centric data model | Not applicable |
| 10 | Overlap | `[AGENT]` | Full overlap with AiiDA's role | Not applicable |
| 11 | Decision | `[AGENT]` | **DEFER**: credible alternative; adopting both would duplicate workflow ownership; PostgreSQL required where AiiDA's small profile is not | Not applicable |

### OVITO

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Scientific visualization and analysis software for atomistic simulation models, with a Python module | [S-gl-ovito]; [S-ovito-readme] |
| 2 | License (edition-specific, each qualified separately) | `[LIT]` | Verified against the vendor's License information page in the OVITO User Manual 3.16.1 (HTTP 200), cross-checked with the repository license files: **(a) OVITO Basic, binary form:** published by OVITO GmbH under the MIT License. **(b) Source code (`stuko/ovito`):** available under GPL v3 and the MIT License (repository LICENSE.txt: every source file under GPL v3 or, at the user's option, MIT; LICENSE.MIT.txt copyright 2026 OVITO GmbH). **(c) OVITO Pro:** proprietary software of OVITO GmbH, licensed under the OVITO Pro End-User Licence Agreement; not open source. **(d) `ovito` Python module as distributed by OVITO GmbH on PyPI and Anaconda:** MIT License (PyPI metadata agrees: `license=MIT`). **(e) Packaging metadata that differs from the vendor statement, kept separate:** the community conda-forge package `ovito` 3.16.0 carries the label `GPL-3.0-or-later`; that is the channel's metadata for its own build, not the vendor's statement for its packages. Earlier failed attempts (`docs.ovito.org/licenses.html` HTTP 500; `ovito.org/docs/current/licenses.html` site 404 page) are retained in the ledger; the working path is `/manual/licenses/index.html` | [S-ovito-manual-licenses] first three paragraphs; [S-gl-ovito-license]; [S-gl-ovito-mit]; [S-ovito-readme]; [S-ovito-about]; [S-pypi-ovito]; [S-conda-ovito]; SOURCE-LEDGER.md failed rows |
| 3 | Maintenance | `[LIT]` | PyPI 3.16.1 2026-09-13; conda-forge 3.16.0 2026-08-21; GitLab last activity 2026-09-15 | [S-pypi-ovito]; [S-conda-ovito]; [S-gl-ovito] |
| 4 | Distribution | `[LIT]` | Python module on PyPI and Anaconda; Basic desktop distribution available. The documentation states that the module and conda package do not require a Pro licence | [S-ovito-pyinstall]; [S-ovito-about] |
| 5 | macOS/arm64 | `[LIT]` | PyPI wheels macosx arm64 for cp311–cp314; conda-forge osx-arm64 | [S-pypi-ovito]; [S-conda-ovito] |
| 6 | Python | `[LIT]` | `>=3.11` | [S-pypi-ovito] |
| 7 | External | `[LIT]` | Bundled Qt in the wheels | [S-ovito-pyinstall] |
| 8 | Cost | `[AGENT]` | Visualization only; no engine cost (structural) | Not applicable |
| 9 | Integration | `[AGENT]` | Render computed coordinates and run bond analysis on trajectories exported from ASE | ARCHITECTURE.md §5 |
| 10 | Overlap | `[AGENT]` | ASE's own viewer and `ase.io` image export cover basic rendering | Not applicable |
| 11 | Decision | `[AGENT]` | **OPTIONAL visualization, not a runtime minimum:** ASE renders computed coordinates; OVITO adds trajectory bond analysis and higher-quality rendering. Use the vendor-distributed Python module (MIT) or OVITO Basic (MIT binaries) only; Pro (proprietary EULA) not needed | Not applicable |

### OpenSCAD

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Script-based solid 3D CAD modeller with STL export | [S-gh-openscad]; [S-openscad-readme] |
| 2 | License | `[LIT]` | GPL-2.0 with a CGAL linking exception; GitHub license field NOASSERTION because of the exception text | [S-openscad-copying]; [S-gh-openscad] |
| 3 | Maintenance | `[LIT]` | Repo pushed 2026-09-12; latest tagged release 2021.01 (2021-02-07); development snapshots on the downloads page | [S-gh-openscad]; [S-openscad-downloads] |
| 4 | Install | `[LIT]` | Binaries for Linux/Windows/macOS; Homebrew (`openscad@snapshot`); MacPorts; source build | [S-openscad-downloads]; [S-openscad-readme] |
| 5 | macOS/arm64 | `[LIT]` (partial) | macOS builds listed; arm64 specifics not stated in retrieved text → `UNVERIFIED` | [S-openscad-downloads] |
| 6 | Python | `[LIT]` | Not a Python package; no PyPI or conda-forge package (both 404) | [S-pypi-openscad]; [S-conda-openscad] |
| 7 | External | `[LIT]` | CGAL and other C++ libraries (bundled in binaries) | [S-openscad-readme] |
| 8 | Cost | `[AGENT]` | CAD only; no scientific compute (structural) | Not applicable |
| 9 | Integration | `[AGENT]` | Conceptual factory/fixture geometry only; unrelated to atomic results | ARCHITECTURE.md §5 |
| 10 | Overlap | `[AGENT]` | None with the scientific stack | Not applicable |
| 11 | Decision | `[AGENT]` | **DEFER**: no MS-001 role; any geometry is conceptual unless tied to measured dimensions, and none exist | Not applicable |

## 2. Tools assessed for reducing custom work (full eleven fields each)

### autodE (`duartegroup/autodE`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Automated reaction-profile generation from SMILES; Python wrappers for electronic-structure codes; conformer/complex generation | [S-autode-readme]; [S-gh-autode] |
| 2 | License | `[LIT]` | MIT (LICENSE.md) | [S-autode-license]; [S-gh-autode] |
| 3 | Maintenance | `[LIT]` | v1.4.5 2025-06-06; repo pushed 2026-03-10 | [S-gh-autode] |
| 4 | Distribution | `[LIT]` | Available through conda-forge and from source; no PyPI project was found (HTTP 404) | [S-autode-readme]; [S-autode-install]; [S-pypi-autode] |
| 5 | macOS/arm64 | `[LIT]` | conda-forge 1.4.5 lists osx-arm64; install docs cover Mac OSX/Linux; untested here | [S-conda-autode]; [S-autode-install] |
| 6 | Python | `[LIT]` | README: Python > 3.7 | [S-autode-readme] |
| 7 | External | `[LIT]` | External electronic-structure codes (README lists ORCA, Gaussian09/16, XTB > 6.1 among others) | [S-autode-readme]; [S-autode-install] |
| 8 | Cost | `[AGENT]` | Engine-bound; profile generation launches many engine jobs | Not applicable |
| 9 | Integration | `[AGENT]` | Molecular, SMILES-driven profiles; no surface or driven-coordinate concept | Not applicable |
| 10 | Overlap | `[AGENT]` | TS search overlaps Sella/ASE NEB for molecules | Not applicable |
| 11 | Decision | `[AGENT]` | **Does not materially reduce custom work; REJECT for MS-001** (wrong problem shape) | Not applicable |

### KinBot (`zadorlab/KinBot`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Automated reaction pathway search for gas-phase organic molecules over multiwell potential energy surfaces | [S-kinbot-readme]; [S-gh-kinbot] |
| 2 | License | `[LIT]` | BSD 3-Clause (Sandia) | [S-kinbot-license] |
| 3 | Maintenance | `[LIT]` | 2.4.1 2026-09-11; repo pushed 2026-09-15 | [S-gh-kinbot]; [S-pypi-kinbot] |
| 4 | Install | `[LIT]` | PyPI and conda-forge (noarch) | [S-pypi-kinbot]; [S-conda-kinbot] |
| 5 | macOS/arm64 | `[LIT]` (partial) | Pure-Python noarch package; no explicit macOS statement found → platform support via its engines; `UNVERIFIED` for arm64 specifics | [S-conda-kinbot] |
| 6 | Python | `[LIT]` | `>=3.11`, classifiers 3.11–3.13 | [S-pypi-kinbot] |
| 7 | External | `[LIT]`/`UNVERIFIED` | External quantum-chemistry engines and a queue system are implied by its purpose; the exact list was not extracted from the retrieved README | [S-kinbot-readme] |
| 8 | Cost | `[AGENT]` | Engine-bound; launches many stationary-point searches | Not applicable |
| 9 | Integration | `[AGENT]` | Gas-phase PES exploration; no surface/driven-tool concept | Not applicable |
| 10 | Overlap | `[AGENT]` | Overlaps autodE (molecular pathway search) | Not applicable |
| 11 | Decision | `[AGENT]` | **Does not materially reduce custom work; REJECT for MS-001** (gas-phase only) | Not applicable |

### pyiron (`pyiron/pyiron`, `pyiron/pyiron_atomistics`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Integrated development environment for computational materials science; job management with its own database; `pyiron_atomistics` for atomistic simulation | [S-pyiron-readme]; [S-gh-pyiron]; [S-gh-pyiron-atomistics] |
| 2 | License | `[LIT]` | BSD 3-Clause (MPIE) for both packages | [S-pyiron-license]; [S-pyiron-atomistics-license] |
| 3 | Maintenance | `[LIT]` | `pyiron` meta-package 0.5.2 2024-01-12 (repo pushed 2025-10-13); `pyiron_atomistics` 0.8.12 2026-08-31 (repo pushed 2026-09-15) | [S-gh-pyiron]; [S-gh-pyiron-atomistics]; [S-pypi-pyiron-atomistics] |
| 4 | Install | `[LIT]` | pip/conda-forge (noarch) | [S-pypi-pyiron]; [S-conda-pyiron] |
| 5 | macOS/arm64 | `[LIT]` (partial) | Pure-Python noarch; platform support via engines; `UNVERIFIED` for arm64 specifics | [S-conda-pyiron] |
| 6 | Python | `[LIT]` | `pyiron_atomistics` `>=3.11,<3.14`; `pyiron` classifiers 3.9–3.11 | [S-pypi-pyiron-atomistics]; [S-pypi-pyiron] |
| 7 | External | `[LIT]`/`UNVERIFIED` | Wraps ASE and external engines; job database (SQL) per its purpose; exact service list not extracted | [S-pyiron-readme] |
| 8 | Cost | `[AGENT]` | Bookkeeping overhead; engine-bound | Not applicable |
| 9 | Integration | `[AGENT]` | Would provide job management and provenance | Not applicable |
| 10 | Overlap | `[AGENT]` | Full overlap with AiiDA's role | Not applicable |
| 11 | Decision | `[AGENT]` | **Does not reduce custom work for this program; DEFER** (second workflow owner) | Not applicable |

### atomate2 (`materialsproject/atomate2`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Library of computational materials-science workflows built on pymatgen, custodian, jobflow, and jobflow-remote or FireWorks; README examples are VASP workflows | [S-atomate2-readme]; [S-gh-atomate2] |
| 2 | License | `[LIT]` | Modified BSD (LBNL); PyPI `BSD-3-Clause-LBNL` | [S-atomate2-license]; [S-pypi-atomate2] |
| 3 | Maintenance | `[LIT]` | v0.1.5 2026-07-13; repo pushed 2026-09-15 | [S-gh-atomate2] |
| 4 | Install | `[LIT]` | pip/conda-forge (noarch) | [S-pypi-atomate2]; [S-conda-atomate2] |
| 5 | macOS/arm64 | `[LIT]` (partial) | Pure-Python noarch; platform support via engines; `UNVERIFIED` for arm64 specifics | [S-conda-atomate2] |
| 6 | Python | `[LIT]` | `>=3.11`, classifiers 3.11–3.13 | [S-pypi-atomate2] |
| 7 | External | `[LIT]` | jobflow (and jobflow-remote or FireWorks) as workflow engine; engines such as VASP per README; a database for jobflow results | [S-atomate2-readme] |
| 8 | Cost | `[AGENT]` | Bookkeeping overhead; engine-bound | Not applicable |
| 9 | Integration | `[AGENT]` | No workflow matching a driven-tool scan; would bring jobflow as a second workflow engine | Not applicable |
| 10 | Overlap | `[AGENT]` | Overlaps AiiDA's role | Not applicable |
| 11 | Decision | `[AGENT]` | **Does not reduce custom work; DEFER** | Not applicable |

### Psi4 (`psi4/psi4`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | Open-source molecular electronic-structure package in C++ driven by Python; DFT functional list includes `WB97X-D3`, `WB97X-D`, `WB97X-D3BJ` | [S-psi4-readme]; [S-psi4-dft] |
| 2 | License | `[LIT]` | LGPL-3.0 (COPYING.LESSER); conda-forge label LGPL-3.0-only AND BSD-3-Clause AND MIT | [S-psi4-license]; [S-conda-psi4] |
| 3 | Maintenance | `[LIT]` | v1.11 2026-06-30; repo pushed 2026-09-15; conda-forge 1.11 2026-08-08 | [S-gh-psi4]; [S-conda-psi4] |
| 4 | Install | `[LIT]` | conda-forge binary packages; not on PyPI (404) | [S-psi4-install]; [S-pypi-psi4] |
| 5 | macOS/arm64 | `[LIT]` | README platform badge lists MacOS Silicon; conda-forge lists osx-arm64; untested here | [S-psi4-readme]; [S-conda-psi4] |
| 6 | Python | `[LIT]` | 3.10–3.14 per README badge | [S-psi4-readme] |
| 7 | External | `[LIT]`/`UNVERIFIED` | conda-provided numerical libraries; ECP coverage for Ge/I in a def2 basis `UNVERIFIED` here | [S-psi4-install] |
| 8 | Cost | `[AGENT]` | Hybrid DFT on a small molecule: modest relative to any slab calculation (qualitative, unmeasured) | Not applicable |
| 9 | Integration | `[AGENT]` | Cross-engine **molecular** check for P2 (functional definition, D3 variant) and the ωB97X-D/def2-TZVPP proxy (spike M10). Not periodic; not a QM/MM host for the needed scheme | Not applicable |
| 10 | Overlap | `[AGENT]` | Any second engine implementing ωB97X-D3 could serve the P2 check; Psi4 is chosen because it lists the functional and ships arm64 conda packages | Not applicable |
| 11 | Decision | `[AGENT]` | **Reduces custom work narrowly; ADOPT as a conditional validation utility, not a runtime minimum.** The package is optional: another engine that implements ωB97X-D3 can serve instead. The capability is required: without a second implementation of ωB97X-D3 the P2 cross-engine check cannot run, spike §8.3 C5 is unmet, and Stage 2 may not begin | MS-000-COMPUTE-SPIKE.md §4 P2, §8.3 |

## 3. Conditional minimum stack for MS-001

`[AGENT]` judgment. Three tiers, so that "minimum" is not inflated by validation or visualization tools:

| Tier | Tools | Role | If omitted |
|---|---|---|---|
| **Required runtime (conditional)** | ASE 3.29.x; CP2K 2026.2; AiiDA 2.9.x with `aiida-cp2k` | Structure/constraints/IO; the DFT level and the GFN0 level; scientific job execution and provenance. The two-level coupling comes from one of the existing reuse candidates in Section 4 (ASE `SimpleQMMM` is inside ASE; CP2K `MIXED` is inside CP2K), **once a route is demonstrated (P3b)** | No MS-001 run is possible without a structure layer, an engine for both levels, and a provenance owner |
| **Conditional coupling-route candidate outside the required tier** | Py-ChemShell 25.0 (`NLayerSubtractive`) | Only if selected as the coupling route (Section 4.3); brings link-atom options | Not needed if route R-A or R-B is demonstrated |
| **Required validation capability (package optional)** | A second implementation of ωB97X-D3; candidate package Psi4 1.11 | P2 molecular cross-engine check, a Stage 1 method-validation calculation (spike §8.2) | Another engine implementing ωB97X-D3 may replace Psi4. With no second implementation the P2 check cannot run, spike §8.3 C5 is unmet, and Stage 2 may not begin |
| **Optional reference utility** | xtb CLI 6.7.x (GFN0 reference implementation and parameter-file provenance) | Cross-implementation GFN0 comparison in Stage 1 | CP2K-internal GFN0 remains usable and identity provenance is still possible; the cross-implementation comparison is lost; no stage is blocked. If the selected composition takes its GFN0 level from xtb, xtb is a required runtime tool instead |
| **Optional visualization** | OVITO Python module / Basic | Trajectory bond analysis and rendering | ASE renders computed coordinates; nothing in the gate depends on OVITO |
| **Supporting analysis only** | ASE NEB (part of ASE); Sella (optional) | Fixed-z barrier questions | Not required to observe E1–E6 |

Scope of the minimum claim: the required tier is minimal **for the proposed composition** (ASE for structure,
CP2K for both levels, AiiDA for provenance) **and for whichever coupling route is eventually selected**. It is not
an absolute minimum over all possible compositions: this document itself records alternatives that would change
the set, namely QCFractal or pyiron as a different workflow/provenance owner, Py-ChemShell as a coupling driver
with link-atom options (which would add a tool), another engine implementing ωB97X-D3 in place of Psi4 for the P2
check, and ASE's own viewer in place of OVITO. Those alternatives are retained as documented options; selecting
one re-opens the minimum set. Within the proposed composition, removing a required-tier tool removes a role the
composition needs. Removing Psi4 is possible only if another engine supplies the required cross-engine capability;
without that capability Stage 2 is blocked (spike §8.3 C5). Removing OVITO, or removing xtb where it does not
supply the GFN0 level, weakens a check or the rendering and blocks no stage. Where the selected composition takes
its GFN0 level from xtb, xtb is a required runtime tool, and removing it blocks Stage 1 onward.

**Rejected for MS-001, with reason:** Pynta (metallic-surface domain; Fireworks + MongoDB), tblite for GFN0 (no
GFN0), autodE and KinBot (molecular/gas-phase problem shape).

**Deferred, with reason:** SCINE Chemoton/Puffin (no network-exploration requirement in MS-001; re-evaluate at
MS-004), QCFractal (duplicates AiiDA; PostgreSQL), Sella (optional), xtb-python (deprecated upstream; stale
wheels), pyiron and atomate2 (second workflow owners; no matching workflow), OpenSCAD (no MS-001 role).

**The stack stays CONDITIONAL until these are resolved** (closing evidence in MS-000-COMPUTE-SPIKE.md §4):

1. **P1 GFN0 through the chosen adapter**: open. No route defaults to GFN0 (xtb CLI default 2; xtb-python ASE
   default GFN2-xTB; tblite has no GFN0; CP2K default `GFN_TYPE 1`). A silent GFN2 fallback is a correctness
   failure. Identity is established by selector, banner, version and parameter provenance, not by a numerical
   difference from GFN2.
2. **P2 hybrid exchange / dispersion / basis / ECP**: open. libxc supplies only the semilocal part; the caller
   supplies exact exchange and range separation; D3 variant/parameters, basis and Ge/I ECPs are unstated by Cowie.
3. **P3 QM/MM coupling scheme and partition**: open (unstated by Cowie), **and P3b coupling route**: open:
   three existing reuse candidates identified, none yet demonstrated for this system (Section 4).
4. **P4 driven constrained motion vs zero-force NEB**: open until a driven-scan protocol is approved.

**CP2K availability is not proof of parity.** An alternative engine or model is a **documented methodological
deviation** until equivalent implementation is verified, and the reference setup needed for that verification is
not available to this study.

## 4. Coupling route candidates (P3b): existing tooling, evaluated reuse-first

`[AGENT]` judgments over `[LIT]` facts. CP2K's QMMM section couples a QM region to a **classical MM** region
([S-cp2k-qmmm]) and is not, by itself, a two-level xTB/DFT scheme. Three **existing, maintained** components that
implement subtractive (ONIOM-like) composition of two levels were identified from official sources. Each is
evaluated below with the mandatory fields; components that are part of an already-evaluated tool inherit that
tool's license, maintenance, install, platform and Python fields by reference. **None of the three is shown to
compose a GFN0-xTB level with a ωB97X-D3 level for this system, and none proves Cowie parity, boundary placement
or link-atom suitability.** The coupling, coupled-force and boundary gaps therefore remain open; what changes is
that the route is a **reuse-first selection among existing components**, not custom driver work.

### 4.1 ASE `SimpleQMMM` (`ase.calculators.qmmm`)

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | ASE's native subtractive QM/MM calculator, described in the docs as similar to the original ONIOM model and usable between any two ASE calculators. Energy = QM(selected subset) − low-level(selected subset) + low-level(all atoms); forces combined the same way on the selected indices. The selected subsystem is made nonperiodic, with optional vacuum padding; `qmcalc`, `mmcalc1`, `mmcalc2` are arbitrary calculators | [S-ase-qmmm-docs] (subtractive section; class signature); [S-ase-qmmm-source]; [S-ase-qmmm-installed] (independently read, lines 15–94) |
| 2 | License | `[LIT]` | Part of ASE: LGPL-2.1-or-later | [S-gl-ase-license] |
| 3 | Maintenance | `[LIT]` | As ASE 3.29.0 (2026-06-21) | [S-pypi-ase] |
| 4 | Install | `[LIT]` | Included in ASE; present in the mission-local smoke venv (ASE 3.29.0) | [S-ase-qmmm-installed] |
| 5 | macOS/arm64 | `[LIT]` | As ASE (pure Python) | Not applicable |
| 6 | Python | `[LIT]` | As ASE | Not applicable |
| 7 | External | `[LIT]` | Two calculators for the two levels (e.g., an xtb-CLI wrapper or CP2K for GFN0 as `mmcalc1`/`mmcalc2`, CP2K for DFT as `qmcalc`); each must accept the subset geometry it is handed | [S-ase-qmmm-docs] |
| 8 | Cost | `[AGENT]` | Three engine evaluations per step (structural: high on subset, low on subset, low on all) | Not applicable |
| 9 | Integration | `[AGENT]` | Already in the required tier; composes with the ASE driven-scan constraints directly. **Limitations observed in the class:** the implementation passes the **complete** geometry to the full-system calculator (`mmcalc2`) and slices the selection for both subset terms (`qmcalc`, `mmcalc1`); it constructs no subsystem-only link atoms and has no host/link derivative mapping (zero mentions of link handling in lines 15–94 of the installed module); a selection that cuts covalent bonds hands dangling valences to both subset calculations; no electrostatic embedding (subtractive/mechanical only) | [S-ase-qmmm-installed] |
| 10 | Overlap | `[AGENT]` | CP2K `MIXED`/`GENMIX` (in-engine composition); Py-ChemShell `NLayerSubtractive` (external driver with link atoms) | Not applicable |
| 11 | Decision | `[AGENT]` | **Candidate route R-A (conditional).** Reuse candidate for the composition. **Boundary handling is an unresolved implementation requirement for this route:** because the class hands the full geometry to `mmcalc2`, adding capping atoms to the ASE geometry would change the full system for every term, so that is not a link-atom treatment. Two things must be kept distinct: (a) *model termination* (e.g., hydrogen termination at the edge of a cluster model), which is part of the physical model seen by all levels and is a modeling choice; (b) *subsystem link atoms* that exist only in the subset terms and carry host/link derivative mapping, which this class does not provide. Only a partition that cuts no covalent bond would avoid (b) entirely, and whether such a partition exists for this system is unverified. To be validated by the coupled-gradient check (spike §8.5) if selected. Not shown suitable for this system | MS-000-COMPUTE-SPIKE.md §4 P3b |

### 4.2 CP2K `FORCE_EVAL/MIXED` with `MIXING_TYPE GENMIX`, `GENERIC` and `MAPPING`

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | The MIXED section runs with a Hamiltonian defined by mixing several sub-force_evals. `MIXING_TYPE` values: `LINEAR_COMBINATION`, `MINIMUM`, `COUPLED`, `RESTRAINT` (each documented for two force_evals), `GENMIX` (user-driven generic coupling; unlimited number of force_evals), `MIXED_CDFT`. `GENERIC` takes a `MIXING_FUNCTION` written in the sub-force_eval energies with `VARIABLES`/`PARAMETERS`/`VALUES`/`UNITS`, and computes the derivative of the mixing function numerically by Ridders' method (`DX` default 0.1 bohr, `ERROR_LIMIT` default 1e-12 with a warning above it). `MAPPING` defines fragment-based atom mapping between each sub-force_eval and the mixed force_eval; the default is a 1-1 mapping in which all force_evals share the same structure; the section can be repeated and has `FORCE_EVAL` and `FORCE_EVAL_MIXED` subsections | [S-cp2k-mixed] (MIXING_TYPE values, NGROUPS, GROUP_PARTITION); [S-cp2k-mixed-generic]; [S-cp2k-mixed-mapping] |
| 2 | License | `[LIT]` | Part of CP2K: GPL-2.0 | [S-cp2k-license] |
| 3 | Maintenance | `[LIT]` | As CP2K 2026.2; MAPPING page last updated 2026-07-15 | [S-cp2k-mixed-mapping] footer |
| 4 | Install | `[LIT]` | As CP2K | [S-cp2k-install] |
| 5 | macOS/arm64 | `[LIT]` | As CP2K (Apple Silicon regularly tested per the installation page) | [S-cp2k-install] |
| 6 | Python | `[LIT]` | Not applicable; driven through CP2K input (ASE's CP2K calculator generates input from a template `inp`; whether it can express a MIXED force_eval is `UNVERIFIED`) | [S-ase-cp2k] |
| 7 | External | `[LIT]` | None beyond CP2K itself | Not applicable |
| 8 | Cost | `[AGENT]` | Multiple sub-force_evals per step, possibly in parallel groups (`NGROUPS`, `GROUP_PARTITION`) (structural) | [S-cp2k-mixed] |
| 9 | Integration | `[AGENT]` | An in-engine subtractive composition would be a `GENMIX` mixing function of the form E1 − E2 + E3 over three sub-force_evals with fragment `MAPPING` for the subset. **Not established from the retrieved pages:** whether sub-force_evals under one MIXED force_eval may use different `METHOD`s (QS xTB vs QS DFT); whether `MAPPING` fragments support the required subset geometry for the high level; how forces at mapped atoms are combined; any link-atom facility (none found on the three pages). These are `UNVERIFIED`, not negative findings | [S-cp2k-mixed-mapping] |
| 10 | Overlap | `[AGENT]` | ASE `SimpleQMMM`; Py-ChemShell | Not applicable |
| 11 | Decision | `[AGENT]` | **Candidate route R-B (conditional).** A bounded follow-up (manual pages for sub-force_eval METHOD mixing, an example input, or a regression test) would decide whether it applies; not shown suitable for this system | MS-000-COMPUTE-SPIKE.md §4 P3b |

### 4.3 Py-ChemShell 25.0 `NLayerSubtractive` / `Layer`

| # | Field | Class | Finding | Locator |
|---|---|---|---|---|
| 1 | Purpose | `[LIT]` | N-layer subtractive (ONIOM-like) QM/MM driver: `NLayerSubtractive(frag=…, layers=(inner…, outer…))` with `Layer(method, atom_indices, gradients_eval, link_atoms, link_atom_charges)`; embedding option `'mechanical'` (default), with electrostatic embedding stated as planned for a future release; `gradients_eval` `'analytic'` (default) or `'finitediff'`; `link_atoms` optional for QM layers (default hydrogen), required for MM layers | [S-pychemshell-subtractive] |
| 2 | License | `[LIT]` (partial) / `UNVERIFIED` | The availability page describes Py-ChemShell as open source and free of charge; **the specific license name is not stated on any retrieved page** (availability page, manual index, About, QM pages) → `UNVERIFIED`. (Tcl-ChemShell, the legacy version, is proprietary STFC-licensed; not relevant here) | [S-pychemshell-licence]; [S-pychemshell-about]; [S-pychemshell-index] |
| 3 | Maintenance | `[LIT]` | Latest release v25.0 (Py-ChemShell 2025) per the availability page and home page; manual copyright 2017–2025 | [S-pychemshell-licence]; [S-pychemshell-home] |
| 4 | Install | `[LIT]` | Source build via a `setup` script; Ubuntu-oriented package list; `--cp2k` links CP2K v2022 or later directly; optional GULP, NWChem, DL_POLY 5, CASTEP, FHI-aims, GAMESS-UK | [S-pychemshell-install] |
| 5 | macOS/arm64 | `UNVERIFIED` | The install page's platform section names Linux desktop (Ubuntu) and HPC modules; no macOS statement found | [S-pychemshell-install] |
| 6 | Python | `[LIT]` (partial) | Python 3 with numpy and tkinter per the install page; exact minimum version not extracted → `UNVERIFIED` | [S-pychemshell-install] |
| 7 | External | `[LIT]` | QM interfaces listed: CASTEP, CP2K, DFTB+, FHI-aims, GAMESS-UK, Gaussian, LSDalton, MNDO, Molpro, NWChem, ORCA, PySCF, Psi4, TURBOMOLE. **No xTB interface is listed**, so a GFN0 layer would have to come through CP2K's internal xTB (P1 route) or DFTB+ (a different method, not GFN0) | [S-pychemshell-qm]; [S-pychemshell-install] |
| 8 | Cost | `[AGENT]` | Driver overhead plus one evaluation per layer term (structural) | Not applicable |
| 9 | Integration | `[AGENT]` | A mature external driver that already carries link-atom options and per-layer gradient choice; would sit beside ASE (structure/IO) and would need its own provenance capture into AiiDA; both levels could be CP2K (DFT and internal GFN0) through its CP2K interface, subject to verification that the interface exposes xTB settings | Not applicable |
| 10 | Overlap | `[AGENT]` | ASE `SimpleQMMM`; CP2K `MIXED`; adds a second driver layer beside ASE | Not applicable |
| 11 | Decision | `[AGENT]` | **Candidate route R-C (conditional).** Strongest documented link-atom support of the three; open items: license name, macOS support, whether its CP2K interface can set `GFN_TYPE 0`, and mechanical-embedding-only. Not shown suitable for this system | MS-000-COMPUTE-SPIKE.md §4 P3b |

### 4.4 What remains open after this evaluation

| Gap | Status |
|---|---|
| A route demonstrated to compose GFN0-xTB and ωB97X-D3 for the declared partition | Open for all three candidates |
| Boundary placement and link-atom treatment suitable for a Si/Ge/C system with a cut through covalent bonds (or a partition that avoids cutting) | Open for every route; R-A provides no subsystem link construction or host/link derivative mapping (capping the full geometry is not a substitute); R-B not stated; R-C has options but unverified for this chemistry |
| Coupled energy/gradient correctness including link-atom chain-rule terms and constraint projection | Open; to be validated per MS-000-COMPUTE-SPIKE.md §8.5 whichever route is selected |
| Equivalence to the Cowie scheme | Unknowable without the Cowie setup (P3) |

## 5. What was not verified in this landscape (summary of `UNVERIFIED` fields)

Pynta macOS/Python; Chemoton macOS/arm64; Puffin arm64; KinBot/pyiron/atomate2 arm64 specifics and exact external
service lists; OpenSCAD macOS arm64 specifics; Psi4 ECP
coverage for Ge/I in a def2 basis; equivalence of CP2K-internal GFN0 to the xtb engine's GFN0; for the coupling
candidates (P3b): whether CP2K `MIXED` sub-force_evals may use different `METHOD`s and whether `MAPPING` supports
the needed subset, whether ASE's CP2K calculator can express a MIXED input, Py-ChemShell's license name, macOS
support, minimum Python version and whether its CP2K interface exposes `GFN_TYPE`; every "runs on arm64"
statement (documented, not tested here, except the ASE import/IO smoke test).
