# Sources and references

This catalogue lists every reference, tool, method source, structure-generation input and figure in the
repository, with direct links, versions, locators, uses and limitations. The numbering is shared by all documents
in the repository. The catalogue contains no computed values, because this project has not yet produced
quantum-chemistry results.

Each entry states its verification basis:
- **Inspected** means that the source, or a cached copy of it, was read in the current review at the locators
  given.
- **Link-checked 2026-09-23** means that the URL was opened successfully on that date to confirm its availability
  and what it identifies. A link check is not scientific verification, and it establishes neither an installed
  capability nor the equivalence of methods.
- **Recorded** means that the URL and the associated facts come from the project's retrieval records, retrieved on
  2026-09-16 unless stated otherwise, and were not re-inspected in the current review.

Not every URL was opened afresh; each entry states its own basis.

The catalogue also distinguishes four kinds of content:
- published data, meaning numbers reported by the cited authors
- primary-source facts, meaning statements taken from documentation or source code
- proposed choices, meaning thresholds, placements and geometries chosen by this project (`[AGENT]`), which are
  not physics
- original figures produced for this repository

## 1. Literature

**[1]** Cowie, M. *et al.* Atomically precise mechanosynthesis of carbon structures on hydrogenated Si(100) by
inverted-mode STM. arXiv:2605.27250v1 [cond-mat.mtrl-sci], submitted 26 May 2026.
- **Links:** [abstract](https://arxiv.org/abs/2605.27250); [PDF v1](https://arxiv.org/pdf/2605.27250v1);
  [HTML v1](https://arxiv.org/html/2605.27250v1);
  [doi:10.48550/arXiv.2605.27250](https://doi.org/10.48550/arXiv.2605.27250).
- **Locators used:** the abstract; the sections "Mechanosynthetic C2 donation", "C2 donation mechanism" (Fig. 3)
  and "Positional and chemical control of mechanosynthetic donation" (discussion of Fig. 5).
- **Used in:** the README, [benchmark.md](benchmark.md) and [donor-candidates.md](donor-candidates.md). The
  reported counts appear in the README and benchmark tables.
- **Basis:** inspected (cached listing and v1 PDF text).
- **Limitations:** the work is a preprint, and no peer-review status is claimed. The Supplementary Information is
  "available upon request" and has not been obtained. No text or figures are copied.

**[2]** Barrera, E. *et al.* Inverted-Mode Scanning Tunneling Microscopy for Atomically Precise Fabrication.
arXiv:2512.24431v1, submitted 30 December 2025.
- **Links:** [abstract](https://arxiv.org/abs/2512.24431); [PDF](https://arxiv.org/pdf/2512.24431);
  [doi:10.48550/arXiv.2512.24431](https://doi.org/10.48550/arXiv.2512.24431).
- **Locators used:** the abstract, which was inspected. The donor identity and spectra on p. 15 of the
  supplementary information are recorded in the original reconstruction notes.
- **Used in:** the README, [benchmark.md](benchmark.md), [donor-candidates.md](donor-candidates.md) and the
  structure headers.
- **Basis:** the abstract was inspected; the listing was link-checked on 2026-09-23 (reported by Root); the
  content of the supplementary information is recorded.
- **Limitations:** donor identity and coordinates derived from this source have not been re-verified in the
  current review.

**[3]** Blue, B. *et al.* Towards Atom-by-Atom Fabrication: Mechanosynthetic donation and abstraction.
arXiv:2606.13876v1, submitted 11 June 2026.
- **Links:** [abstract](https://arxiv.org/abs/2606.13876);
  [doi:10.48550/arXiv.2606.13876](https://doi.org/10.48550/arXiv.2606.13876).
- **Locators used:** the abstract, which was inspected. The connectivity and attachment scheme of Fig. 1B/C is
  recorded in the reconstruction notes.
- **Used in:** the README, [benchmark.md](benchmark.md) and [donor-candidates.md](donor-candidates.md).
- **Basis:** the abstract was inspected; the listing was link-checked on 2026-09-23 (reported by Root); the use of
  the figure is recorded.
- **Limitations:** the Supplementary Information is "available upon request" and has not been obtained.

**[4]** MacLean, O. *et al.* Electron-Induced Formation of C2 on Si(100) from Acetylene and Ethylene.
arXiv:2607.19488v1, submitted 21 July 2026.
- **Links:** [abstract v1](https://arxiv.org/abs/2607.19488v1);
  [doi:10.48550/arXiv.2607.19488](https://doi.org/10.48550/arXiv.2607.19488).
- **Locators used:** the cluster and anchor convention of Fig. S15, as recorded in the reconstruction notes.
- **Used in:** [donor-candidates.md](donor-candidates.md), for the definition of the surface comparator.
- **Basis:** the identity was link-checked on 2026-09-23; the details of Fig. S15 are recorded.
- **Limitations:** the link check confirms bibliographic identity only. The figure details were not re-inspected.

**[5]** Patent US11708384B2, "Systems and methods for mechanosynthesis".
- **Links:** [Google Patents record](https://patents.google.com/patent/US11708384B2/en).
- **Locators used:** the text description of FIG. 53, as recorded in the reconstruction notes.
- **Used in:** [donor-candidates.md](donor-candidates.md).
- **Basis:** the record was link-checked on 2026-09-23; the use of FIG. 53 is recorded.
- **Limitations:** the check confirms the public patent record only. No conclusion is drawn about donor identity,
  feasibility or patent law.

## 2. Software and documentation

### Selected or used

**[6]** Psi4, the selected electronic-structure engine, version 1.11 (release tagged `v1.11`).
- **Links:** repository [github.com/psi4/psi4](https://github.com/psi4/psi4); conda-forge record
  [api.anaconda.org/package/conda-forge/psi4](https://api.anaconda.org/package/conda-forge/psi4); licence text
  [COPYING.LESSER](https://raw.githubusercontent.com/psi4/psi4/master/COPYING.LESSER).
- **Content:** these sources identify the official repository and record that version 1.11 exists as a tagged
  release and a conda-forge package, under LGPL-3.0.
- **Basis:** the repository was link-checked on 2026-09-23; the release, package and licence facts are recorded.
- **Limitations:** Psi4 is not installed or validated here.

**[7]** Psi4 manual, development version (page headers carry `1.12a1.dev35`).
- **Links:** chapters on the [self-consistent field](https://psicode.org/psi4manual/master/scf.html),
  [one-electron properties](https://psicode.org/psi4manual/master/oeprop.html) and
  [basis sets](https://psicode.org/psi4manual/master/basissets.html), and the
  [table of functionals](https://psicode.org/psi4manual/master/dft_byfunctional.html).
- **Locators used:** see Section 3 and [engine-capability-status.md](engine-capability-status.md).
- **Basis:** inspected, from cached copies.
- **Limitations:** development documentation cannot establish the behaviour of an installed 1.11 release. The
  version-pinned `1.11.0` manual pages returned HTTP 404 at retrieval (recorded).

**[8]** Psi4 manual, development version, chapters not inspected in the current review.
- **Links:** [DFT](https://psicode.org/psi4manual/master/dft.html);
  [basis sets by element](https://psicode.org/psi4manual/master/basissets_byelement.html).
- **Content:** capability notes and element coverage.
- **Basis:** recorded.
- **Limitations:** these chapters bear on analytic gradients and basis coverage, which remain `UNVERIFIED`.

**[9]** Psi4 source file `proc.py` at tag `v1.11`.
- **Links:** [proc.py](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/proc.py).
- **Content:** in the SCF helper, stability root-following is restricted to UHF references.
- **Basis:** inspected (the relevant lines only).
- **Limitations:** a source file does not prove runtime behaviour or the content of an installed build. No code is
  copied.

**[10]** Psi4 source file `libxc_functionals.py` at tag `v1.11`.
- **Links:** [libxc_functionals.py](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/libxc_functionals.py).
- **Retrieval:** retrieved once on 2026-09-23 as 13 425 bytes, with Git blob
  `d1ed5e1a27b61b780e42449ab8f093718c9286e5` and SHA256
  `e289d7d713e2ae9cecf8e37a22d80ed7fd9beed0c9febd0aa9282afd81c448fe`, an exact match to the expected blob.
- **Content:** the file declares the `wB97X-D3` entry.
- **Basis:** inspected (that entry only).
- **Limitations:** the same as for [9].

**[11]** Libxc functional list.
- **Links:** [libxc.gitlab.io/functionals](https://libxc.gitlab.io/functionals/).
- **Content:** the list includes `HYB_GGA_XC_WB97X_D3` and `HYB_GGA_XC_WB97X_D`.
- **Basis:** recorded on 2026-09-16.
- **Limitations:** the Libxc version linked into an installed Psi4 1.11 is unknown, and the functional definition
  was not inspected in the current review. Equivalence is not resolved here.

**[12]** AiiDA, the selected provenance system (the documentation page identifies version 2.9.2).
- **Links:** [introduction](https://aiida.readthedocs.io/projects/aiida-core/en/stable/intro/index.html);
  [complete installation guide](https://aiida.readthedocs.io/projects/aiida-core/en/stable/installation/guide_complete.html);
  licence [LICENSE.txt](https://raw.githubusercontent.com/aiidateam/aiida-core/main/LICENSE.txt).
- **Content:** the introduction describes workflow and data-provenance features. The other pages give installation
  options and the MIT licence.
- **Basis:** the introduction was link-checked on 2026-09-23; installation and licence are recorded.
- **Limitations:** the `stable` URL is mutable and does not prove an installed version. AiiDA is not integrated
  with an engine here.

**[13]** RDKit, used for the donor embeddings (version 2026.03.6 in the file headers; the documentation page
identifies 2026.03.6).
- **Links:** [RDKit Book, conformer generation](https://www.rdkit.org/docs/RDKit_Book.html#conformer-generation).
- **Content:** documents the ETKDG conformer-generation algorithm used.
- **Basis:** link-checked on 2026-09-23 (reported by Root).
- **Limitations:** this is algorithm documentation only. It does not show that the donor candidates match any
  primary coordinates.

**[14]** ASE, used for structure building and extxyz input and output (version 3.29.0 in the headers and records).
- **Links:** [surface builders (`diamond100`)](https://docs.ase-lib.org/ase/build/surface.html);
  [file format options](https://docs.ase-lib.org/ase/io/formatoptions.html);
  [installation](https://docs.ase-lib.org/install.html);
  [constraints](https://docs.ase-lib.org/ase/constraints.html);
  licence [LICENSE](https://gitlab.com/ase/ase/-/raw/master/LICENSE);
  PyPI record [pypi.org/pypi/ase/json](https://pypi.org/pypi/ase/json).
- **Content:** the `diamond100` builder used for the surface definitions, Python requirements, constraint classes
  and the LGPL-2.1-or-later licence.
- **Basis:** the surface-builder page was link-checked on 2026-09-23 (reported by Root). The format-options page
  returned HTTP 200 to a HEAD request on 2026-09-23 (reported by Root). The remaining facts are recorded.
- **Limitations:** this is algorithm documentation only. For the format-options page only availability is
  established; its content, the extxyz section and the format behaviour are unverified.

### Candidates evaluated from documentation only

None of the following tools is installed.

**[15]** xtb.
- **Links:** [setup and installation](https://xtb-docs.readthedocs.io/en/latest/setup.html);
  [command line](https://xtb-docs.readthedocs.io/en/latest/commandline.html);
  [GFN0 parameter file (main branch)](https://raw.githubusercontent.com/grimme-lab/xtb/main/param_gfn0-xtb.txt);
  [README](https://raw.githubusercontent.com/grimme-lab/xtb/main/README.md).
- **Content:** the packaged parameter files include `param_gfn0-xtb.txt`, and the `--gfn` option defaults to 2.
  GFN0-xTB is the benchmark's QM/MM partner method.
- **Basis:** the setup page was link-checked on 2026-09-23; the remainder is recorded.
- **Limitations:** the documentation describes the GFN0 route but establishes neither local availability nor
  equivalence with the benchmark. The parameter file is from the main branch, not a tagged release.

**[16]** CP2K.
- **Links:** [XTB section, 2026.2 branch](https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/QS/XTB.html);
  [QMMM, 2026.2](https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/QMMM.html);
  [XC functional, 2026.2](https://manual.cp2k.org/cp2k-2026_2-branch/CP2K_INPUT/FORCE_EVAL/DFT/XC/XC_FUNCTIONAL.html).
- **Content:** `GFN_TYPE` 0 selects a CP2K-internal GFN0-xTB. The manual has a QM/MM section, and its Libxc hybrid
  list includes `WB97X_D3`. CP2K is a possible periodic and QM/MM route.
- **Basis:** the XTB section was link-checked on 2026-09-23; the remainder is recorded.
- **Limitations:** documentation only; this is not validation of an installation.

**[17]** tblite.
- **Links:** [built-in methods](https://tblite.readthedocs.io/en/stable/spec/methods.html).
- **Content:** the built-in methods are GFN1-xTB, GFN2-xTB and IPEA1-xTB, with no GFN0. tblite is listed only to
  prevent confusion with the GFN0 route.
- **Basis:** link-checked on 2026-09-23.
- **Limitations:** tblite is not a substitute for the GFN0 route.

**[18]** QCFractal.
- **Links:** [github.com/MolSSI/QCFractal](https://github.com/MolSSI/QCFractal);
  [QCArchive documentation](https://docs.qcarchive.molssi.org/);
  [licence](https://raw.githubusercontent.com/MolSSI/QCFractal/main/LICENSE).
- **Content:** the official MolSSI repository. Its README introduction describes a database and compute platform,
  under the BSD-3-Clause licence. It is an alternative workflow store, deferred.
- **Basis:** the repository was link-checked on 2026-09-23; the documentation and licence are recorded.
- **Limitations:** there is no claim that it ran here.

**[19]** OVITO.
- **Links:** [ovito.org](https://www.ovito.org/);
  [licence information](https://www.ovito.org/manual/licenses/index.html);
  [Python module installation](https://www.ovito.org/docs/current/python/introduction/installation.html).
- **Content:** OVITO provides visualization and analysis of particle simulations, with edition and licence
  statements and a Python module. It is a candidate for rendering computed coordinates.
- **Basis:** the homepage was link-checked on 2026-09-23; the remainder is recorded.
- **Limitations:** documentation only. It was not used for Figure 1.

## 3. Sources of the method specification

The following table maps each element of [e01-method-specification.md](e01-method-specification.md) to its
source.

| Specification element | Kind | Source and locator | Basis |
|---|---|---|---|
| SCF convergence by energy change, RMS density change and maximum iterations | Primary-source fact (development manual) | [7], [SCF chapter](https://psicode.org/psi4manual/master/scf.html), section "Initial Guess" (convergence paragraph) | Inspected |
| Numerical thresholds (10⁻⁸ and 10⁻¹⁰ Eh, gradient bounds, ⟨S²⟩ bands, 10⁻⁶ Eh degeneracy, 0.10 e, 0.50 and 0.80 e) | Proposed choices (prospective engineering choices, not physics) | Project method definition | Not applicable |
| ⟨S²⟩ deviation printed for UHF | Primary-source fact (development manual) | [7], [SCF chapter](https://psicode.org/psi4manual/master/scf.html), UHF description | Inspected |
| Kohn–Sham stability: Davidson limited to LDA; RHF→UHF external check; root-following restricted to UHF | Primary-source facts | [7], [SCF chapter](https://psicode.org/psi4manual/master/scf.html), stability-analysis section; [9], [`proc.py` at v1.11](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/proc.py), SCF helper | Inspected; direct-inversion Kohn–Sham coverage unresolved |
| Per-label basis `assign`; effective core potential in the same block | Primary-source fact (development manual) | [7], [basis-sets chapter](https://psicode.org/psi4manual/master/basissets.html), basis-block and ECP sections | Inspected |
| Löwdin spin populations | Primary-source fact (development manual) | [7], [oeprop chapter](https://psicode.org/psi4manual/master/oeprop.html), property list | Inspected |
| `wB97X-D3` declaration (Libxc identifier, `d3zero2b` parameters) | Primary-source fact (version-tagged source) | [10], [`libxc_functionals.py` at v1.11](https://raw.githubusercontent.com/psi4/psi4/v1.11/psi4/driver/procrouting/dft/libxc_functionals.py), `wB97X-D3` entry | Inspected |
| Analytic gradients with effective core potential | Open | [8], [DFT chapter](https://psicode.org/psi4manual/master/dft.html), capability notes | Recorded, not inspected; `UNVERIFIED` |
| Central finite-difference gradient check, guess set, localization rules | Proposed choices | Project method definition | Not applicable |

## 4. Structure-generation inputs

The inputs to [`../structures/`](../structures/README.md) fall into four groups.
- **Identity and description of the tool (EAOGe-C2I).** This is a published statement from [1], section
  "Mechanosynthetic C2 donation", and was inspected.
- **Systematic name, spectral consistency and the mass-spectrometry mismatch.** These are historical claims about
  the supplementary information of [2], p. 15, as recorded in the original reconstruction notes. They were not
  re-verified in the current review.
- **Coordinates.** These are proposed (`[AGENT]`) and unoptimized. They are RDKit 2026.03.6 ETKDGv3 embeddings
  with seed 20260916 [13], written with ASE 3.29.0 in extxyz format [14]; the versions are taken from the file
  headers. The generating script is private and is identified in the headers by its SHA256
  `6c088a006e5cd401f0407cfcaedd956381d9aae9181fdcdba28e5364009b3bfd`. It is not published, for the reason given in
  the export manifest.
- **Surface-model definitions (not published).** These are also proposed. They use the ASE
  [`diamond100`](https://docs.ase-lib.org/ase/build/surface.html) lattice with geometric dimerization and capping,
  and a comparator convention following Fig. S15 of [4] (recorded). The builder page was link-checked; the details
  of the construction are recorded.

## 5. Figures

The repository contains one figure, [`figures/activated-donor.svg`](figures/activated-donor.svg), which appears
as Figure 1 of the README.
- **Nature:** an original rendering, produced for this repository, of the heavy atoms of the proposed activated
  donor candidate.
- **Inputs:** the unchanged coordinates of
  [`../structures/donor-activated-EAOGe-C2-radical.extxyz`](../structures/donor-activated-EAOGe-C2-radical.extxyz)
  and the bond table [`../tools/activated-donor-bonds.tsv`](../tools/activated-donor-bonds.tsv). The bond table is
  transcribed from the atom-mapped SMILES in [donor-candidates.md](donor-candidates.md).
- **Method:** the deterministic standard-library script
  [`../tools/render_donor_plate.py`](../tools/render_donor_plate.py). Its projection, view selection, label mapping
  and validation checks are documented in [donor-candidates.md](donor-candidates.md), Section 4.
- **Limitations:** the figure depicts a proposed, unoptimized input. It is neither a validated structure nor the
  benchmark authors' coordinates. Hydrogen atoms are omitted, the atom-disc radii are graphic conventions rather
  than physical radii, and no computed quantity is shown.

The diagrams and the chart of reported outcomes in earlier versions of the repository have been retired. They are
recorded in the revision history of the export manifest. The reported outcomes remain tabulated in the README and
in [benchmark.md](benchmark.md).

## 6. Private and unavailable records

The benchmark's Supplementary Information, and its coordinates, QM/MM partition and drive protocol, are not
available to this project. The authors state that the Supplementary Information is available on request; it has
not been obtained.

The project's original working records are private and are not linked. They comprise:
- the reconstruction notes, the execution-route record and the retrieval ledger
- cached copies of papers and documentation
- logs, workflow-provenance tests and review records

They are identified in the [export manifest](../provenance/EXPORT-MANIFEST.md) by description and SHA256 only.
