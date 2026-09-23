# Sources and references

This index maps every reference, tool, method source, structure-generation input and figure in this repository to
direct links, versions, locators, uses and limits. **It contains no computed values**; this project has produced
no quantum-chemistry results yet.

**How each entry was checked.** Link availability and scientific verification are kept separate.

| Label | Meaning |
|---|---|
| **Inspected** | The source, or a cached copy of it, was read in the current review at the locators given. |
| **Link-checked 2026-09-23** | The URL was opened successfully on 2026-09-23 to confirm that it is available and what it identifies. **This is not scientific verification**, not proof of an installed capability, and not proof of method equivalence. |
| **Recorded** | The URL and facts come from the project's retrieval records (retrieved 2026-09-16 unless stated otherwise) and were not re-inspected in the current review. |

Not every URL here was freshly opened. Each entry states its own basis.

**Kinds of content, kept distinct:**
- **Published data:** numbers reported by the cited authors.
- **Primary-source facts:** statements taken from documentation or source code.
- **Proposed choices:** thresholds, placements and geometries chosen by this project (`[AGENT]`), which are not
  physics.
- **Original conceptual design:** diagrams drawn for this repository.

---

## 1. Research literature

| Reference | Direct links | Version / date | Locators used | Used in | Basis | Limits |
|---|---|---|---|---|---|---|
| Cowie, M. *et al.*, "Atomically precise mechanosynthesis of carbon structures on hydrogenated Si(100) by inverted-mode STM" | [abstract](https://arxiv.org/abs/2605.27250) · [PDF v1](https://arxiv.org/pdf/2605.27250v1) · [HTML v1](https://arxiv.org/html/2605.27250v1) · [doi:10.48550/arXiv.2605.27250](https://doi.org/10.48550/arXiv.2605.27250) | arXiv v1, submitted 26 May 2026 | Abstract; sections "Mechanosynthetic C2 donation", "C2 donation mechanism" (Fig. 3) and "Positional and chemical control of mechanosynthetic donation" (Fig. 5 discussion) | [README](../README.md), [benchmark.md](benchmark.md), [donor-candidates.md](donor-candidates.md), figure `reported-outcomes.svg` | **Inspected** (cached listing and v1 PDF text) | Preprint; no peer-review status claimed. Supplementary Information "available upon request", **not obtained**. No text or figures copied. |
| Barrera, E. *et al.*, "Inverted-Mode Scanning Tunneling Microscopy for Atomically Precise Fabrication" | [abstract](https://arxiv.org/abs/2512.24431) · [PDF](https://arxiv.org/pdf/2512.24431) · [doi:10.48550/arXiv.2512.24431](https://doi.org/10.48550/arXiv.2512.24431) | arXiv v1, submitted 30 Dec 2025 | Abstract (inspected). Supplementary information p. 15 donor identity and spectra (**recorded** in the original reconstruction notes). | [README](../README.md), [benchmark.md](benchmark.md), [donor-candidates.md](donor-candidates.md), structure headers | Abstract **Inspected**; listing **Link-checked 2026-09-23** (reported by Root); SI content **Recorded** | Donor identity and coordinates derived from this source have not been re-verified in the current review. |
| Blue, B. *et al.*, "Towards Atom-by-Atom Fabrication: Mechanosynthetic donation and abstraction" | [abstract](https://arxiv.org/abs/2606.13876) · [doi:10.48550/arXiv.2606.13876](https://doi.org/10.48550/arXiv.2606.13876) | arXiv v1, submitted 11 Jun 2026 | Abstract (inspected). Fig. 1B/C connectivity and attachment scheme (**recorded** in the reconstruction notes). | [README](../README.md), [benchmark.md](benchmark.md), [donor-candidates.md](donor-candidates.md) | Abstract **Inspected**; listing **Link-checked 2026-09-23** (reported by Root); figure use **Recorded** | Supplementary Information "available upon request"; not obtained. |
| MacLean, O. *et al.*, "Electron-Induced Formation of C2 on Si(100) from Acetylene and Ethylene" | [abstract v1](https://arxiv.org/abs/2607.19488v1) · [doi:10.48550/arXiv.2607.19488](https://doi.org/10.48550/arXiv.2607.19488) | arXiv v1, submitted 21 Jul 2026 | Fig. S15 cluster and anchor convention (**recorded** in the reconstruction notes) | [donor-candidates.md](donor-candidates.md) §5 (surface comparator definition) | Identity **Link-checked 2026-09-23**; Fig. S15 details **Recorded** | The link check confirms bibliographic identity only; the figure details were not re-inspected. |
| Patent US11708384B2, "Systems and methods for mechanosynthesis" | [Google Patents record](https://patents.google.com/patent/US11708384B2/en) | publication US11708384B2 | FIG. 53 text description (**recorded** in the reconstruction notes) | [donor-candidates.md](donor-candidates.md) §4 | Record **Link-checked 2026-09-23**; FIG. 53 use **Recorded** | Confirms the public patent record only; no conclusion about donor identity, feasibility or patent law. |

## 2. Software and documentation

### 2.1 Selected or used

| Tool | Version | Direct links | What the source supports | Used for | Basis | Limits |
|---|---|---|---|---|---|---|
| **Psi4** (selected engine) | 1.11 (release tagged `v1.11`) | [github.com/psi4/psi4](https://github.com/psi4/psi4) · conda-forge record: [api.anaconda.org/package/conda-forge/psi4](https://api.anaconda.org/package/conda-forge/psi4) · licence text: [COPYING.LESSER](https://raw.githubusercontent.com/psi4/psi4/master/COPYING.LESSER) | Official repository. Version 1.11 exists as a tagged release and a conda-forge package; licence LGPL-3.0. | [e01-method-specification.md](e01-method-specification.md), [engine-capability-status.md](engine-capability-status.md) | Repository **Link-checked 2026-09-23**; release, package and licence facts **Recorded** | Not installed or validated here. |
| Psi4 development manual | pages carry `1.12a1.dev35` | [SCF](https://psicode.org/psi4manual/master/scf.html) · [one-electron properties](https://psicode.org/psi4manual/master/oeprop.html) · [basis sets](https://psicode.org/psi4manual/master/basissets.html) · [DFT by functional](https://psicode.org/psi4manual/master/dft_byfunctional.html) | See §3 and [engine-capability-status.md](engine-capability-status.md) | capability status | **Inspected** (cached copies; the sections listed there) | Development documentation cannot establish installed 1.11 behaviour. Version-pinned 1.11.0 manual pages returned 404 at retrieval (**recorded**). |
| Psi4 development manual (not inspected in the current review) | `master` | [DFT](https://psicode.org/psi4manual/master/dft.html) · [basis sets by element](https://psicode.org/psi4manual/master/basissets_byelement.html) | Capability notes; element coverage | open items in [engine-capability-status.md](engine-capability-status.md) | **Recorded** | Relevant to analytic gradients and basis coverage, which remain **UNVERIFIED**. |
| Psi4 `v1.11` source files | tag `v1.11` | [proc.py](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/proc.py) · [libxc_functionals.py](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/libxc_functionals.py) | `proc.py`: stability root-following restricted to UHF. `libxc_functionals.py`: the `wB97X-D3` declaration. Retrieved 2026-09-23: 13 425 bytes, Git blob `d1ed5e1a27b61b780e42449ab8f093718c9286e5`. | [engine-capability-status.md](engine-capability-status.md) | **Inspected** (the listed lines/entry only) | A source file is not proof of runtime behaviour or of an installed build; code is not copied. |
| **AiiDA** (selected provenance system) | page identifies 2.9.2 | [Introduction](https://aiida.readthedocs.io/projects/aiida-core/en/stable/intro/index.html) · [complete installation guide](https://aiida.readthedocs.io/projects/aiida-core/en/stable/installation/guide_complete.html) · licence: [LICENSE.txt](https://raw.githubusercontent.com/aiidateam/aiida-core/main/LICENSE.txt) | The introduction describes workflow and data-provenance features (the selected role). Installation options; MIT licence. | [README](../README.md) architecture | Introduction **Link-checked 2026-09-23**; installation and licence **Recorded** | The `stable` URL is mutable and is not proof of an installed version. Not integrated with an engine here. |
| **RDKit** (used for donor embeddings) | 2026.03.6 (file headers; the documentation page identifies 2026.03.6) | [RDKit Book — conformer generation](https://www.rdkit.org/docs/RDKit_Book.html#conformer-generation) | Documents the conformer-generation (ETKDG) algorithm used | [structures/](../structures/README.md), [donor-candidates.md](donor-candidates.md) | **Link-checked 2026-09-23** (reported by Root) | Algorithm documentation only. It is not evidence that the donor candidates match primary coordinates. |
| **ASE** (structure building and extxyz I/O) | 3.29.0 (headers and records) | [surface builders (`diamond100`)](https://docs.ase-lib.org/ase/build/surface.html) · [file format options](https://docs.ase-lib.org/ase/io/formatoptions.html) · [install](https://docs.ase-lib.org/install.html) · [constraints](https://docs.ase-lib.org/ase/constraints.html) · licence: [LICENSE](https://gitlab.com/ase/ase/-/raw/master/LICENSE) · PyPI record: [pypi.org/pypi/ase/json](https://pypi.org/pypi/ase/json) | `diamond100` builder used for the surface definitions; Python requirements; constraint classes; LGPL-2.1-or-later | [structures/](../structures/README.md), [donor-candidates.md](donor-candidates.md) §5 | Surface page **Link-checked 2026-09-23** (reported by Root). Format-options page: HTTP 200 on a HEAD request, 2026-09-23 (reported by Root). The rest **Recorded**. | Algorithm documentation only. For the format-options page only availability is established: its content, the extxyz section and the format behaviour are **unverified**. |

### 2.2 Candidates (documentation-evaluated only; none installed)

| Tool | Direct links | What the documentation states | Why it matters here | Basis | Limits |
|---|---|---|---|---|---|
| **xtb** | [setup and installation](https://xtb-docs.readthedocs.io/en/latest/setup.html) · [command line](https://xtb-docs.readthedocs.io/en/latest/commandline.html) · [GFN0 parameter file (main branch)](https://raw.githubusercontent.com/grimme-lab/xtb/main/param_gfn0-xtb.txt) · [README](https://raw.githubusercontent.com/grimme-lab/xtb/main/README.md) | The packaged parameter files include `param_gfn0-xtb.txt`; `--gfn` option (default 2) | GFN0-xTB is the benchmark's QM/MM partner method | Setup page **Link-checked 2026-09-23**; the rest **Recorded** | Documents the GFN0 route. Not local availability or benchmark equivalence; the parameter file above is main-branch, not a tagged release. |
| **CP2K** | [XTB section, 2026.2 branch](https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/QS/XTB.html) · [QMMM, 2026.2](https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/QMMM.html) · [XC functional, 2026.2](https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/XC_FUNCTIONAL.html) | `GFN_TYPE` 0 selects a CP2K-internal GFN0-xTB; QM/MM section; Libxc hybrid list including `WB97X_D3` | Possible periodic / QM/MM route with an internal GFN0 option | XTB section **Link-checked 2026-09-23**; the rest **Recorded** | Documentation only; not installation validation. |
| **tblite** | [built-in methods](https://tblite.readthedocs.io/en/stable/spec/methods.html) | Built-in methods: GFN1-xTB, GFN2-xTB, IPEA1-xTB; **no GFN0** | Listed to prevent confusion with the GFN0 route | **Link-checked 2026-09-23** | **Not** a substitute for the GFN0 route. |
| **QCFractal** | [github.com/MolSSI/QCFractal](https://github.com/MolSSI/QCFractal) · [QCArchive documentation](https://docs.qcarchive.molssi.org/) · [licence](https://raw.githubusercontent.com/MolSSI/QCFractal/main/LICENSE) | Official MolSSI repository; database and compute platform (README introduction); BSD-3-Clause | Alternative workflow store (deferred) | Repository **Link-checked 2026-09-23**; documentation and licence **Recorded** | No claim it ran here. |
| **OVITO** | [ovito.org](https://www.ovito.org/) · [licence information](https://www.ovito.org/manual/licenses/index.html) · [Python module installation](https://www.ovito.org/docs/current/python/introduction/installation.html) | Visualization and analysis of particle simulations; edition and licence statements; Python module | Rendering of computed coordinates | Homepage **Link-checked 2026-09-23**; the rest **Recorded** | Documentation only; nothing rendered yet. |

### 2.3 Functional-definition dependency

| Source | Direct link | What it states | Basis | Limits |
|---|---|---|---|---|
| Libxc functional list | [libxc.gitlab.io/functionals](https://libxc.gitlab.io/functionals/) | Lists `HYB_GGA_XC_WB97X_D3` (and `HYB_GGA_XC_WB97X_D`) | **Recorded** (2026-09-16) | The Libxc version linked into an installed Psi4 1.11 is unknown, and the definition was not inspected in the current review. Equivalence is not resolved here. |

## 3. Method-specification references ([e01-method-specification.md](e01-method-specification.md))

| Specification element | Kind | Source and locator | Basis |
|---|---|---|---|
| SCF convergence by energy change, RMS density change and maximum iterations | Primary-source fact (development manual) | [Psi4 SCF](https://psicode.org/psi4manual/master/scf.html), section "Initial Guess" (convergence paragraph) | **Inspected** |
| Numerical thresholds (10⁻⁸ / 10⁻¹⁰ Eh, gradient bounds, ⟨S²⟩ bands, 10⁻⁶ Eh degeneracy, 0.10 e, 0.50 / 0.80 e) | **Proposed choices** (prospective engineering choices, not physics) | Project method definition | — |
| ⟨S²⟩ deviation printed for UHF | Primary-source fact (development manual) | [Psi4 SCF](https://psicode.org/psi4manual/master/scf.html), UHF description | **Inspected** |
| Kohn–Sham stability: Davidson LDA-only; RHF→UHF external check; root-following restricted to UHF | Primary-source facts | [Psi4 SCF](https://psicode.org/psi4manual/master/scf.html), stability-analysis section; [`proc.py` @ v1.11](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/proc.py), SCF helper | **Inspected**; direct-inversion Kohn–Sham coverage unresolved |
| Per-label basis `assign`; ECP in the same block | Primary-source fact (development manual) | [Psi4 basis sets](https://psicode.org/psi4manual/master/basissets.html), basis-block and ECP sections | **Inspected** |
| Löwdin spin populations | Primary-source fact (development manual) | [Psi4 oeprop](https://psicode.org/psi4manual/master/oeprop.html), property list | **Inspected** |
| `wB97X-D3` declaration (Libxc ID, `d3zero2b` parameters) | Primary-source fact (version-tagged source) | [`libxc_functionals.py` @ v1.11](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/libxc_functionals.py), `wB97X-D3` entry | **Inspected** |
| Analytic gradients with ECP | Open | [Psi4 DFT](https://psicode.org/psi4manual/master/dft.html) capability notes | **Recorded**, not inspected; **UNVERIFIED** |
| Central finite-difference gradient check, guess set, localization rules | **Proposed choices** | Project method definition | — |

## 4. Structure generation ([structures/](../structures/README.md))

| Input | Kind | Source | Basis |
|---|---|---|---|
| Tool identity and description (EAOGe-C2I) | Published statement | [Cowie et al.](https://arxiv.org/abs/2605.27250), "Mechanosynthetic C2 donation" | **Inspected** |
| Systematic name, spectra consistency, mass-spectrometry mismatch | Historical claims | Supplementary information of [Barrera et al.](https://arxiv.org/abs/2512.24431), p. 15, as recorded in the original reconstruction notes | **Recorded**; not re-verified in the current review |
| Coordinates | **Proposed** (`[AGENT]`), unoptimized | RDKit 2026.03.6 ETKDGv3, seed 20260916 ([conformer generation](https://www.rdkit.org/docs/RDKit_Book.html#conformer-generation)); written with ASE 3.29.0 extxyz | Versions from the file headers; algorithm page link-checked |
| Generator script | Private | SHA256 `6c088a006e5cd401f0407cfcaedd956381d9aae9181fdcdba28e5364009b3bfd` (in the headers) | Not published (see the manifest) |
| Surface-model definitions (not published) | **Proposed** (`[AGENT]`) | ASE [`diamond100`](https://docs.ase-lib.org/ase/build/surface.html) lattice with geometric dimerization and capping; comparator convention after [MacLean et al.](https://arxiv.org/abs/2607.19488v1) Fig. S15 (recorded) | Builder page link-checked; construction details **Recorded** |

## 5. Figures (all five SVGs; editable sources in this repository)

| Figure | Kind | Content source | Limits |
|---|---|---|---|
| [`masthead.svg`](figures/masthead.svg) | Original conceptual design | None: abstract motif | Not a structure, geometry or result |
| [`reported-outcomes.svg`](figures/reported-outcomes.svg) | Original chart of **published data** | Counts and 95% intervals from [Cowie et al.](https://arxiv.org/abs/2605.27250), "Positional and chemical control of mechanosynthetic donation" (Fig. 5 discussion). The same values are tabulated in the [README](../README.md) and [benchmark.md](benchmark.md). | Authors' experimental counts; not this project's results; axis starts at 50%; not multipliable |
| [`evidence-classes.svg`](figures/evidence-classes.svg) | Original conceptual design | [evidence-policy.md](evidence-policy.md) | Summary only; the policy text governs |
| [`architecture.svg`](figures/architecture.svg) | Original conceptual design | Responsibilities table in the [README](../README.md); tool statuses from §2 | Not a deployment diagram; no tool validated |
| [`e01-validation-flow.svg`](figures/e01-validation-flow.svg) | Original conceptual design | [e01-method-specification.md](e01-method-specification.md) | Not run; contains no computed values |

## 6. Private or unavailable records

- **Unavailable to this project:** the benchmark's Supplementary Information and its coordinates, QM/MM
  partition and drive protocol. The authors state the SI is available on request; it has not been obtained.
- **Private, not linked:** the project's original working records. These include:
  - reconstruction notes, execution-route record and retrieval ledger
  - the cached copies of papers and documentation
  - logs, workflow-provenance tests and review records

  They are identified in the [export manifest](../provenance/EXPORT-MANIFEST.md) by description and SHA256 only.
