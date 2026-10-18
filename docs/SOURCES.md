# Sources and references

This catalogue lists the references, method sources, structure-generation inputs and figures used by the main
repository narrative, with direct links, versions, locators, uses and limitations. The full MS-000 software
assessment uses a larger retrieval set, catalogued separately in the
[MS-000 source ledger](ms-000/SOURCE-LEDGER.md); the MS-001 Stage 0 retrievals are catalogued in the
[MS-001 Stage 0 source ledger](ms-001/SOURCE-LEDGER.md) and summarized in Section 9 (entries [28] to [31]). The
sources of the MS-001 pre-Stage-1 closure packet are catalogued in the
[pre-Stage-1 source ledger](ms-001/PRESTAGE1-SOURCE-LEDGER.md) and summarized in Section 10 (entries [32] to [35]).
Revisions of the Stage 0 definitions approved by a person since then are listed in Sections 11 and 14 (entries [36] and [39]).
The pre-run determination of the wiring test W1, which cites no external source, is listed in Section 15 (entry [40]).
The decision packet on revision 01 of the W1 specification is listed in Section 16 (entry [41]). The approval and
application of that revision are listed in Section 17 (entry [42]), and the second W1 pre-run determination, under the
revised text, in Section 18 (entry [43]). The one run of W1, which stopped under §8 condition S10, is listed in
Section 19 (entry [44]). The sources of the H2 learning package are listed in Section 20 (entries [45] to [51]), and
those of its Phase A run proposal in Section 21 (entries [52] to [55]); the fixture assessment of its route-R2
method-revision proposal is listed in Section 22 (entry [56]), and the test record of the enabling revision that
binds the approved method revision is listed in Section 23 (entry [57]). The records of the one authorized attempt of
job H2-A-01, which stopped before launch, are listed in Section 24 (entry [58]), and those of its continuation, which
stopped before any driver invocation, in Section 25 (entry [59]). The
numbering here is shared by the main documents in the
repository. The catalogue contains no converged quantum-chemistry values. The project's only
quantum-chemistry attempt, E-01, stopped before any SCF iteration was reported and is closed as technically
blocked and scientifically indeterminate. Its records are entries [20] and [21], and the dispersion library it
used is [22]. The `v1.11` source files read for its postmortem are entries [23] and [24], and the project's
postmortem, installed-build survey and closure records are entries [25] to [27]. Its public report is
[results/e01](../results/e01/README.md), and its postmortem is
[results/e01/postmortem.md](../results/e01/postmortem.md).

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
  reported counts appear in Figure 2 of the README, in the table in benchmark.md and in the chart input
  [`../tools/benchmark-reported-outcomes.tsv`](../tools/benchmark-reported-outcomes.tsv).
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
- **Basis:** the abstract was inspected; the listing was link-checked on 2026-09-23 (reported in the project's
  link-check record); the content of the supplementary information is recorded.
- **Limitations:** donor identity and coordinates derived from this source have not been re-verified in the
  current review.

**[3]** Blue, B. *et al.* Towards Atom-by-Atom Fabrication: Mechanosynthetic donation and abstraction.
arXiv:2606.13876v1, submitted 11 June 2026.
- **Links:** [abstract](https://arxiv.org/abs/2606.13876);
  [doi:10.48550/arXiv.2606.13876](https://doi.org/10.48550/arXiv.2606.13876).
- **Locators used:** the abstract, which was inspected. The connectivity and attachment scheme of Fig. 1B/C is
  recorded in the reconstruction notes.
- **Used in:** the README, [benchmark.md](benchmark.md) and [donor-candidates.md](donor-candidates.md).
- **Basis:** the abstract was inspected; the listing was link-checked on 2026-09-23 (reported in the project's
  link-check record); the use of the figure is recorded.
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
- **Limitations:** Psi4 1.11 was installed from conda-forge in a project-local environment [20]. The installation
  and basis construction were checked for that build, the configured dispersion route was exercised in a
  dispersion-only check, and the E-01 precursor SCF aborted during integral setup [21]. SCF behaviour, analytic
  gradients and spin properties of this build remain unverified. A postmortem of the `v1.11` input/output and
  conventional-integral source [23, 24] and a bounded, read-only static survey of the installed build [26]
  identified no cause of the abort. The survey records the availability of some input/output library names in the
  installed build; that is not ABI compatibility, initialization or callability.

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
- **Limitations:** the installed Psi4 1.11 build printed Libxc version 7.1.2 at runtime [21]. The functional
  definition in Libxc was not inspected in the current review, and equivalence is not resolved here.

**[12]** AiiDA, the selected provenance system (the documentation page identifies version 2.9.2).
- **Links:** [introduction](https://aiida.readthedocs.io/projects/aiida-core/en/stable/intro/index.html);
  [complete installation guide](https://aiida.readthedocs.io/projects/aiida-core/en/stable/installation/guide_complete.html);
  licence [LICENSE.txt](https://raw.githubusercontent.com/aiidateam/aiida-core/main/LICENSE.txt).
- **Content:** the introduction describes workflow and data-provenance features. The other pages give installation
  options and the MIT licence.
- **Basis:** the introduction was link-checked on 2026-09-23; installation and licence are recorded.
- **Limitations:** the `stable` URL is mutable and does not prove an installed version. The project used an
  installed AiiDA 2.9.2 only to store hashed records of the E-01 preparation and run [21]; it was not used to
  execute calculations, and storage of records is not evidence of a scientific result. In MS-001 Stage 0, a separate
  project-local AiiDA 2.9.2 profile ran one trivial non-chemistry job, integer addition in bash, as the provenance
  wiring test [30]; that job is software evidence only.

**[13]** RDKit, used for the donor embeddings (version 2026.03.6 in the file headers; the documentation page
identifies 2026.03.6).
- **Links:** [RDKit Book, conformer generation](https://www.rdkit.org/docs/RDKit_Book.html#conformer-generation).
- **Content:** documents the ETKDG conformer-generation algorithm used.
- **Basis:** link-checked on 2026-09-23 (reported in the project's link-check record).
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
- **Basis:** the surface-builder page was link-checked on 2026-09-23 (reported in the project's link-check
  record). The format-options page returned HTTP 200 to a HEAD request on 2026-09-23 (reported in the project's
  link-check record). The remaining facts are recorded.
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

The repository contains two figures. The first, [`figures/activated-donor.svg`](figures/activated-donor.svg),
appears as Figure 1 of the README.
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

The second figure, [`figures/benchmark-outcomes.svg`](figures/benchmark-outcomes.svg), appears as Figure 2 of the
README.
- **Nature:** an original point-and-interval chart of published data, namely the per-interaction target-formation
  percentages, reported 95% confidence intervals and counts of [1]. It is not a copy of a figure from the paper.
- **Input:** [`../tools/benchmark-reported-outcomes.tsv`](../tools/benchmark-reported-outcomes.tsv). The values are
  transcribed as reported in the section "Positional and chemical control of mechanosynthetic donation" of [1]
  (discussion of Fig. 5), and they match the table in [benchmark.md](benchmark.md).
- **Method:** the deterministic standard-library script
  [`../tools/render_outcomes_chart.py`](../tools/render_outcomes_chart.py). It draws the reported values on a 0 to
  100 percent axis. It does not recompute percentages or confidence intervals from the counts.
- **Limitations:** the values are the authors' experimental per-interaction outcomes. They are neither results of
  this project nor independent full-build yields, and they are not multiplied into a build-success probability.

The diagrams and the earlier chart of reported outcomes in previous versions of the repository have been retired.
They are recorded in the revision history of the export manifest.

## 6. Private and unavailable records

The benchmark's Supplementary Information, and its coordinates, QM/MM partition and drive protocol, are not
available to this project. The authors state that the Supplementary Information is available on request; it has
not been obtained.

The project's original working records are private and are not linked. They comprise:
- the reconstruction notes, the execution-route record and the retrieval ledger
- cached copies of papers and documentation
- logs, workflow-provenance tests and review records

They are identified in the [export manifest](../provenance/EXPORT-MANIFEST.md) by description and SHA256 only.
The original E-01 run records [21] are also private; the public derivatives in
[`../results/e01/`](../results/e01/README.md) state their sources and redactions. The postmortem, survey and
closure records [25] to [27], the source captures and raw survey captures that they bind, and the project's
orchestration records are private as well. The ten postmortem, survey and closure records are identified by
description and SHA256 in [postmortem.md](../results/e01/postmortem.md).

## 7. Installed environment and E-01 records

**[20]** Project installation record of the Psi4 1.11 environment.
- **Content:** 94 conda-forge packages (platforms `osx-arm64` and `noarch`), each with name, version, build,
  channel, URL, MD5 and SHA256, including psi4 1.11, Python 3.14.7, libxc-c 7.1.2, qcengine 0.51.0,
  qcelemental 0.51.2, simple-dftd3 1.6.0 and dftd3-python 1.6.0. The installation receipt has SHA256
  `4e080247aaed75c151b029564673c1d5c8204e110ec239a233fadc3265eb8b59`.
- **Used in:** the README, [engine-capability-status.md](engine-capability-status.md) and
  [`../results/e01/method-config.json`](../results/e01/method-config.json), which lists the hashes of the selected
  installed files.
- **Basis:** recorded; the package identities were checked against the installed package records before the run.
- **Limitations:** package records identify packages, not the integrity of every installed file; file bytes were
  checked only for the selected files. The installed `libxc_functionals.py` differs from the `v1.11` tag [10] at
  the TH-FL entry only, and no functional equivalence is claimed. No installation instructions are given.

**[21]** Project records of the E-01 run, 2026-09-24.
- **Content:** the reviewed configuration, the runner's gate checks, job inputs, engine output and error text, the
  classification, the resource ledger and scratch observations, bound by an as-run evidence manifest of 45 files
  (SHA256 `6e7050b3fe02c237a9572b55e2f8a987517a14ffa8bae15db1992628c8cfdadc`) and a preparation manifest of 33 files
  (SHA256 `0d5d018df63b88ec4a00d1d4f0aaa9366324bcdf789978e66d3cd59293d5d10a`).
- **Used in:** [`../results/e01/`](../results/e01/README.md), including
  [postmortem.md](../results/e01/postmortem.md), the README and
  [engine-capability-status.md](engine-capability-status.md).
- **Basis:** the public derivatives were produced from these records, with their SHA256 values and redactions stated
  in the export manifest.
- **Limitations:** the records document a stopped software run. They contain no converged electronic energy or
  gradient of either donor and no statement about chemistry, and the cause of the abort is undiagnosed. The
  postmortem and the installed-build survey [25, 26] did not diagnose it, and the attempt is closed as technically
  blocked and scientifically indeterminate [27].

**[22]** simple-dftd3 and dftd3-python, version 1.6.0, installed with Psi4 [20].
- **Links:** conda-forge packages as recorded in the installation receipt,
  [simple-dftd3 1.6.0](https://conda.anaconda.org/conda-forge/osx-arm64/simple-dftd3-1.6.0-gfortran_h643d65c_0.conda)
  and
  [dftd3-python 1.6.0](https://conda.anaconda.org/conda-forge/osx-arm64/dftd3-python-1.6.0-py314hcd3153d_1.conda).
- **Content:** the D3 dispersion implementation through which the Psi4 route for ωB97X-D3 is configured
  (`d3zero2b`, three-body term off). The parameters printed by the engine at E-01 setup are s6 = 1.0, s8 = 1.0,
  sr6 = 1.281, sr8 = 1.094 and alpha6 = 14.0 [21].
- **Basis:** recorded (installation receipt and engine output), not newly inspected; the dispersion route was
  exercised in a dispersion-only check without SCF.
- **Limitations:** the check covers the dispersion term only. E-01 completed no dispersion-corrected energy.

## 8. E-01 postmortem sources and closeout records

**[23]** Psi4 source files of the input/output library at tag `v1.11`, with its Python binding.
- **Links:** the [`v1.11` tag tree](https://github.com/psi4/psi4/tree/v1.11). The files are cited by name and line
  locator; no per-file link is given.
- **Files and locators used:** `config.h`, recorded as `libpsio/config.h` (lines 42 to 84); `get_address.cc`
  (lines 44 to 55); `get_global_address.cc` (lines 48 to 53); `rw.cc` (lines 94, 105, 128, 140, 160 and 172);
  `volseek.cc` (lines 50 to 75); `read.cc` (lines 71 to 78); `write.cc` (lines 57 to 58 and 103 to 124);
  `aio_handler.cc` (lines 89 to 116 and 209 to 480); and the Python binding `export_psio.cc` (lines 41 to 70).
- **Content:** the error constants, including code 17 for an incorrect block start address and code 18 for a block
  end, and the page length of 65 536; the relative and global address arithmetic; the block-start and extension
  checks on the write path, and the explanatory message printed on the read path; the codes raised for failed
  operating-system reads, writes and seeks; the asynchronous input/output handler, with its single worker thread,
  its zero-fill and integral-write jobs and its lack of an exception handler; and the input/output functions
  exposed to Python.
- **Used in:** [postmortem.md](../results/e01/postmortem.md), Sections 2 to 4 and 7.
- **Basis:** recorded. The files were read at the `v1.11` tag for the project's postmortem, and the locators above
  are those given in its private capture records [25]. They were not re-inspected in the current review. The
  tag-tree link shares the base of the repository link of [6], which was link-checked; the tag-tree URL itself was
  not opened in the current review.
- **Limitations:** source text is conditional evidence. It does not establish the code of the installed binary,
  and a type declared in the source is not a measured width in the installed build. The installed `config.h` has
  the same SHA256 as the capture of this file [26]; no other file was compared with the installed build. The
  binding file is one of fifteen such export files, and only it was inspected. No source text is copied.

**[24]** Psi4 source files of the conventional (PK) integral manager at tag `v1.11`.
- **Links:** the [`v1.11` tag tree](https://github.com/psi4/psi4/tree/v1.11). The files are cited by name and line
  locator; no per-file link is given.
- **Files and locators used:** `PKmanagers.cc` (lines 946 to 947, 950 and 957 to 980); `PK_workers.cc` (lines 818
  to 819 and 951 to 996); `PK_workers.h` (lines 189 to 193).
- **Content:** the assignment of units 92 and 93 to the two supermatrix scratch files; the pre-striping arithmetic,
  in which the divisor, row count and remainder are computed before the divisor is clamped, the first zero-fill is
  conditional on a positive row count and the second is unconditional; and the asynchronous bucket writes with a
  shared running position.
- **Used in:** [postmortem.md](../results/e01/postmortem.md), Sections 2 and 3.
- **Basis:** recorded, on the same terms as [23].
- **Limitations:** the same as for [23]. The engine memory value, the workload size and the other operands of E-01
  cannot be obtained from these files.

**[25]** Project postmortem records of E-01, 2026-09-24.
- **Content:** a source-level assessment of the E-01 abort, which is the controlling record (SHA256
  `629601e688b5f22379ca408f2eb43bfa112ff67ee106c1bb8a7a077095bf0d37`), and an independent review of that assessment
  (SHA256 `4ce5f8469639733d4b6c90b3e8e9e94326eec9bf130c119c316cba62f49e2532`). The assessment binds the source
  captures of [23] and [24] by SHA256 and records the conditional source-level pathway, the ranked hypotheses, a
  conditional design for a fixed-position test and the ranked gaps.
- **Used in:** [postmortem.md](../results/e01/postmortem.md), [`../results/e01/`](../results/e01/README.md),
  [engine-capability-status.md](engine-capability-status.md) and
  [RESEARCH-STATE.md](../.agents/RESEARCH-STATE.md).
- **Basis:** inspected. Both records were read in full in the current review, and their SHA256 values were
  recomputed and matched. The source captures and other records that they bind are private, are not present in this
  repository and were not re-inspected.
- **Limitations:** the records assess source text and run records; they are not a diagnosis. The pathway they record
  is a hypothesis, which is not established as the cause of E-01 and is neither established nor excluded. Text
  produced by language models is never physical evidence.

**[26]** Project records of the installed-build survey, 2026-09-24.
- **Content:** the survey observations (SHA256 `f3a0d09fdac5fa15c9c88e0f2870b18e67c7c6cde77afe329770149883153045`),
  the diagnostic-feasibility determination (SHA256
  `adb4a6eee85de8b450d04db55b1809e482500dccdd1ce4c532a37624e0ecc3d3`), the evidence manifest of 76 bindings, which
  excludes itself (SHA256 `e99807c15ba01b76b9d43181a10d6512f5297ecac385bef7cfd7c30d5fb954d7`), the independent review
  of the survey result (SHA256 `37c77fe100f9df814d57b912e0b8f7b861c2aafcf432e379d0dc3842ba68a546`), the acceptance
  record of the survey result, with supplemental findings (SHA256
  `6b28b3a9e2157cc60ac13d2c3cdf84b22c346cc5f17c87cb19faddb200165dc8`), and the survey result status record (SHA256
  `2230695b2dcef3f49cef380b4707447cd467b989547829b2b43ac13c618485c6`).
- **Used in:** [postmortem.md](../results/e01/postmortem.md),
  [engine-capability-status.md](engine-capability-status.md),
  [`../results/e01/outcome.json`](../results/e01/outcome.json) and
  [RESEARCH-STATE.md](../.agents/RESEARCH-STATE.md).
- **Basis:** inspected. The six records were read in full in the current review, and their SHA256 values were
  recomputed and matched. The raw survey captures and run evidence that they bind are private, are not present in
  this repository and were not inspected. The verification of all 76 manifest bindings that these records report is
  historical and was not repeated.
- **Limitations:** the survey provides static evidence about software artifacts only. Its enumeration of package
  file names covered 1 791 of 6 260 names, and the installed widths D = sizeof(double) and I = sizeof(int) are
  unresolved. The supplemental findings of the acceptance record were recorded after the independent review and are
  not covered by it. Nothing in these records establishes callability, a cause of E-01 or any chemical fact.

**[27]** Project closeout records of E-01, 2026-09-24.
- **Content:** the terminal disposition of the diagnostic route (SHA256
  `fb958eefbe078bc7a2bc8cedbe7b0bc7a3ff7495ad5fd0a60259f149f29e49cc`), which records that the narrower guard-only
  replay was declined and that the attempt is technically blocked and scientifically indeterminate, and the closure
  record of the attempt (SHA256 `9261fa1903901f7b4eb660be56e0e612ba4f93b9062bc9c5782bc6114df15a87`).
- **Used in:** [postmortem.md](../results/e01/postmortem.md), [`../results/e01/`](../results/e01/README.md), the
  README and [RESEARCH-STATE.md](../.agents/RESEARCH-STATE.md).
- **Basis:** inspected. Both records were read in full in the current review, and their SHA256 values were
  recomputed and matched.
- **Limitations:** the records close the attempt as run. They establish no cause of the abort, no chemical result,
  no exclusion of disk capacity and no demonstration of the source-level pathway.

## 9. MS-001 Stage 0 sources

The exhaustive Stage 0 retrieval record is the [MS-001 Stage 0 source ledger](ms-001/SOURCE-LEDGER.md). It gives
the URL, version, locator, access time, HTTP result and retrieved-byte SHA256 of each item. The entries below
summarize it for the narrative catalogue.

**[28]** Stage 0 documentation and source retrievals, 2026-09-26: 73 retrievals, 71 obtained and 2 not.
- **Links and versions:**
  - AiiDA documentation at the version-pinned URL for 2.9.2;
  - the CP2K 2026.2-branch manual, and CP2K data and source files from the `support/v2026.2` branch;
  - the Py-ChemShell 25.0 manual;
  - Psi4 source files at tag `v1.11`; simple-dftd3 files at tag `v1.6.0`; qcengine files at tag `v0.51.0`, which
    are byte-identical to those installed with the project's Psi4 build; and libxc source at tag `7.0.0`;
  - the `aiida-cp2k` 2.1.1 PyPI record and source archive;
  - docs.ase-lib.org pages, which were found not to match ASE 3.29.0.

  Each item is listed in the [ledger](ms-001/SOURCE-LEDGER.md).
- **Content:** the facts used to review the ASE and AiiDA data models, compare the three coupling routes, declare
  both method levels and their numerical settings, and declare the drive, tolerances and validation set. Among them:
  - CP2K's GFN0 selector (`GFN_TYPE 0`, default 1);
  - the libxc ωB97X-D3 parameters, 1.0, −0.804272 and 0.25;
  - CP2K's hard-coded D3 zero-damping sr8 = 1.0, against rs8 = 1.094 in the simple-dftd3 table;
  - the def2-TZVP basis entries in both engines;
  - the dispersion-input contract from Psi4 through qcengine to simple-dftd3, and the Psi4 driver rule on SCF
    convergence defaults;
  - the documented optimizer and SCF defaults.
- **Used in:** [docs/ms-001](ms-001/README.md).
- **Basis:** inspected at the locators given in the ledger.
- **Limitations:** the defining ωB97X-D3 paper (doi:10.1021/ct300715s) was not obtained (HTTP 403), and one
  Py-ChemShell page returned 404. Documentation establishes documented behaviour only. Nothing here demonstrates
  that a route or setting works on this system, and nothing here is a parity claim.

**[29]** Installed source files read locally for Stage 0.
- **Content:** twelve source-ID rows covering thirteen files from the project-local ASE 3.29.0, aiida-core 2.9.2
  and disk-objectstore 1.5.0 installations and from the `aiida-cp2k` 2.1.1 source archive. They cover extxyz I/O,
  the covalent-radius and lattice tables, the `diamond100` builder, `SimpleQMMM`, `StructureData`, the transport
  login-shell default, repository hashing and the `aiida-cp2k` input and parser code. One row, `S0-aiida-src-add`,
  covers two files: the arithmetic calculation and its parser. Each file is identified by its own SHA256 and its
  archive's SHA256 in the [ledger](ms-001/SOURCE-LEDGER.md).
- **Used in:** [C3](ms-001/C3-PROVENANCE-WIRING.md), [C2](ms-001/C2-COUPLING-ROUTE.md),
  [C4](ms-001/C4-TOLERANCES-AND-CONVERGENCE.md) and the [geometry record](../structures/ms-001/README.md).
- **Basis:** inspected. The files were read and their digests were recorded.
- **Limitations:** source reading establishes what the code states, not runtime behaviour, except where the C3 job
  measured it.

**[30]** Project records of MS-001 Stage 0 (scope option B), 2026-09-26, with the C4 human approval record of
2026-09-27.
- **Content:** the Stage 0 package in [docs/ms-001](ms-001/README.md):
  - the authorization record;
  - the provenance wiring test on one trivial non-chemistry AiiDA job, which finished with exit status 0;
  - the coupling-route selection, the two-level declaration, the drive protocol, the tolerances and
    numerical-convergence protocol, and the validation set;
  - the failure record and the freeze record;
  - the [C4 human approval record](ms-001/C4-HUMAN-APPROVAL.md) of 2026-09-27, which binds the approval of C4 to its
    exact path, commit and SHA256 and identifies the private decision records by SHA256 only.

  With it go the geometries in [structures/ms-001](../structures/ms-001/README.md), built by
  [`tools/build_ms001_geometries.py`](../tools/build_ms001_geometries.py), and the wiring driver
  [`tools/c3_provenance_wiring.py`](../tools/c3_provenance_wiring.py).
- **Basis:** new records of this project, identified by SHA256 in the freeze record and the export manifest.
- **Limitations:** every model, setting and threshold is `[AGENT]`, a declared deviation. The records contain no
  energy, force, gradient or optimized structure. Parity with the benchmark is unknown. The definitions have
  independent review approval and Lead acceptance, and a person approved C4 on 2026-09-27 as the prospective Stage 0
  numerical protocol, so Stage 0 is closed as a set of frozen prospective definitions. The approval validates nothing
  physically and changes no evidence label, and Stage 1 is not authorized.

**[31]** Source-resolution sources, 2026-09-27: 16 retrievals, all obtained, and the reuse of 15 retrievals of
2026-09-26.
- **Links and versions.** Each item is listed in the dated section of the
  [ledger](ms-001/SOURCE-LEDGER.md#source-resolution-retrievals-2026-09-27):
  - **CP2K.** The 2026.2 release archive `cp2k-2026.2.tar.bz2` (SHA256 `f9bd86f5…`). Its release revision is
    `67b5da876dd6a76b8b021d5a04d1c81ba79a4c50`, to which tag `v2026.2` resolves, and the archive's own `REVISION`
    file names the parent `c92cc08`. The tag, commit and tree records were retrieved with it.
  - **Psi4.** The source archive of commit `f16f4ea2ff2351cc2ab877d9b3887fcf81c2a670`, to which tag `v1.11`
    resolves, with the tag and tree records.
  - **Libint.** `include/libint2/shell.h` at Libint `v2.8.1`, the version that Psi4 v1.11 names as its source pin and
    minimum.
- **Content.** The source facts behind the [source resolution record](ms-001/SOURCE-RESOLUTION.md):
  - GFN0 parameter provenance in CP2K: the data file `xTB0_parameters`, constants hard-coded in source, the
    file-resolution order and the dftd4 dependency;
  - the unit and conversion of `OMEGA` in CP2K's exact exchange;
  - basis normalization in CP2K and Psi4;
  - the order and formats of CP2K's force records under `GEO_OPT`;
  - the non-use of fitting bases by Psi4's compiled SCF and gradient steps under the declared settings.
- **Used in.** [SOURCE-RESOLUTION.md](ms-001/SOURCE-RESOLUTION.md), the proposed
  [C4 revision options](ms-001/C4-PROPOSED-REVISION-01.md), and the dated annotations of
  [B2](ms-001/B2-METHOD-DECLARATION.md).
- **Basis.** Inspected. 211 locator assertions over 72 files pass. Every cited CP2K and Psi4 file equals the blob of
  its tag-commit tree. The 15 reused retrievals of 2026-09-26 match their ledger digests and equal the corresponding
  release-revision or tag-commit bytes.
- **Limitations.**
  - Source text establishes software behaviour defined by that source, not the behaviour of any installed or future
    build.
  - The Psi4 archive is generated by GitHub and is not a published release asset.
  - Libint v2.8.1 is not shown to be the version of any build.
  - The dftd4 source that the declared route uses, the rounding of formatted output and the Libint2 version of the
    Psi4 build remain open. So do C4's definitional question on N8 and the build provenance of the installed Psi4.
  - *2026-09-28:* the dftd4 source that the declared route uses is declared in B2 §3, and C4's
    definitional question on N8 is settled by a revision of C4, both approved by a person in one decision
    ([N8 approval record](ms-001/C4-HUMAN-APPROVAL-02.md);
    [G4 approval record](ms-001/B2-G4-HUMAN-APPROVAL.md)). The rounding of formatted output
    is still not fixed by source, and the P1 identity provenance of G4 remains within Stage 1.
  - Nothing here is physical evidence or parity, upgrades an evidence label, or authorizes Stage 1.

## 10. MS-001 pre-Stage-1 closure sources

The exhaustive record of these sources is the [pre-Stage-1 source ledger](ms-001/PRESTAGE1-SOURCE-LEDGER.md). It
gives identity, retrieval or observation time, byte count, SHA256, locators and limits for each. The entries below
summarize it.

**[32]** Installed E-01 Psi4 environment and its package archives, 2026-09-27.
- **Links and versions:**
  - the installed package records of psi4 1.11 (`py314h53d0584_1`) and libint 2.13.1 (`h5a0831b_0`), both
    conda-forge `osx-arm64`;
  - three installed Libint2 files and the Psi4 core library;
  - the two package archives named by those records,
    <https://conda.anaconda.org/conda-forge/osx-arm64/libint-2.13.1-h5a0831b_0.conda> and
    <https://conda.anaconda.org/conda-forge/osx-arm64/psi4-1.11-py314h53d0584_1.conda>.
- **Content.** The installed Libint2 package version, 2.13.1. The agreement of three installed files with the
  record's digests. The normalization code of the installed `shell.h`. The static linkage declarations.
- **Used in.** [INSTALLED-BUILD-AUDIT.md](ms-001/INSTALLED-BUILD-AUDIT.md).
- **Basis.** Inspected. Read-only static observation of the named files, with hashes. Each archive matched the
  SHA256 and MD5 in its installed record.
- **Limitations.**
  - Package provenance only, not runtime conformance.
  - The recipe and build metadata inside both archives' `info` members were not read, because the system archive
    tool lacks zstd support. Libint2 and Psi4 source and build identity remain unresolved.
  - Runtime linkage is not established.

**[33]** The dftd4 4.2.0 and tblite 0.6.0 source archives from the CP2K download site, 2026-09-27, with the CP2K
2026.2 toolchain files that pin them.
- **Links and versions.**
  - <https://www.cp2k.org/static/downloads/dftd4-4.2.0.tar.xz> and
    <https://www.cp2k.org/static/downloads/tblite-0.6.0.tar.xz>, each matching the SHA256 pinned by the CP2K 2026.2
    toolchain.
  - The toolchain scripts, patches and CP2K source files read inside the retained release archive [31].
- **Content.**
  - Both archives carry byte-identical dftd4 4.2.0 source files. The tblite route patches them and the standalone
    route does not.
  - By source tracing, CP2K's GFN0 D4 path with its defaults reaches none of the patched routines.
  - Dependency resolution depends on switches that neither toolchain script sets.
- **Used in.** [G4-DFTD4-DECLARATION-PROPOSAL.md](ms-001/G4-DFTD4-DECLARATION-PROPOSAL.md), and, since
  2026-09-28, the declaration of the dftd4 source in
  [B2 §3](ms-001/B2-METHOD-DECLARATION.md#3-gfn0-xtb-level-sub-force_evals-e2-and-e3).
- **Basis.** Inspected. Every member was checked before unpacking, and both trees were compared file by file with
  SHA256 and Git blob SHA1. Patch applicability was checked by dry run only.
- **Limitations.**
  - Correspondence with any upstream release asset was not examined.
  - Nothing was built. No build, linkage or runtime claim follows.

**[34]** aiida-core 2.9.2 source members of the retained Stage 0 wheel, 2026-09-27.
- **Links and versions.** The wheel of the Stage 0 hash-locked installation (SHA256 `72ec503b…7bdd`). Its members
  for the transport, the direct scheduler, the script assembly, the CalcJob class, the upload task and the process
  type are identified in the ledger.
- **Content.** Login-shell default and command form. Environment inheritance by transport shells. The direct
  scheduler's invocation and header. The dry-run transport. The order of `presubmit` and upload. The persistence of
  an unregistered process class.
- **Used in.** [C3-WIRING-TEST-PROPOSAL.md](ms-001/C3-WIRING-TEST-PROPOSAL.md) and the
  [N8 decision packet](ms-001/N8-DECISION-PACKET.md).
- **Basis.** Inspected. The members were read from the retained wheel without installation or import.
- **Limitations.** Source text only. How aiida-core behaves on the host is a run observation, which only an
  authorized wiring test could make.

**[35]** Project records of the MS-001 pre-Stage-1 closure packet, 2026-09-27.
- **Content.**
  - the [closure packet](ms-001/PRESTAGE1-CLOSURE-PACKET.md), with its consolidated readiness table;
  - the installed-build audit;
  - the proposed G4 dftd4 declaration;
  - the N8 decision packet;
  - the proposed C3 wiring test W1;
  - the [pre-Stage-1 source ledger](ms-001/PRESTAGE1-SOURCE-LEDGER.md).
- **Basis.** New records of this project, identified by SHA256 in the export manifest.
- **Limitations.**
  - Every recommendation, candidate text and specification is `[AGENT]`, and none is applied or approved.
  - *2026-09-28:* the proposed G4 declaration and option O2 of the N8 decision packet were
    approved by a person in one decision and applied, to B2 §3 and to C4, B3, C2 and C7
    ([N8 approval record](ms-001/C4-HUMAN-APPROVAL-02.md);
    [G4 approval record](ms-001/B2-G4-HUMAN-APPROVAL.md)). The packet's records themselves
    are unchanged.
  - *2026-10-04:* revision 01 of the proposed C3 wiring test W1 was approved by a person and applied to the W1
    specification itself (entry [42]). That record therefore no longer holds its text of 2026-09-27, which stays
    identifiable by SHA256 `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158`.
  - The frozen Stage 0 records, including C4 and its approval record, are byte-identical.
  - Nothing here is physical evidence or upgrades an evidence label.
  - Stage 1 remains BLOCKED and is not authorized.

## 11. MS-001 revisions approved by a person

**[36]** Project records of the revisions of MS-001 Stage 0 definitions approved by a person in one decision, in an answer
recorded on 2026-09-27.
- **Records.**
  - The revision of C4 that defines N8 as fixed-atom checks, with the consequential revisions of B3, C2 and C7, and
    its [approval record](ms-001/C4-HUMAN-APPROVAL-02.md).
  - The revision of B2 that declares the dftd4 source for G4 in B2 §3, and its
    [approval record](ms-001/B2-G4-HUMAN-APPROVAL.md).
- **Basis.** New records of this project, identified by SHA256 in the export manifest and bound in the
  [freeze record](ms-001/STAGE0-FREEZE-RECORD.md#2-frozen-artifacts).
- **Limitations.**
  - Each approval binds exact bytes by path and SHA256. It validates nothing physically and upgrades no evidence
    label.
  - Stage 1 remains BLOCKED and is not authorized.


## 12. Installed recipe metadata audit

**[37]** Exact retained conda-forge Psi4 1.11 `py314h53d0584_1` and Libint 2.13.1 `h5a0831b_0`
package metadata, locally reverified and read on 2026-09-28.
- **Identity and locators.** The [new companion ledger](ms-001/RECIPE-METADATA-SOURCE-LEDGER.md) records archive URLs,
  exact sizes/digests, both compressed and decoded metadata identities, all 47 regular members, private validation
  code/report digests, observed times and retained failures. Exact claim locators are in the
  [audit](ms-001/RECIPE-METADATA-AUDIT.md).
- **Verification basis.** Existing archive digests and prior copies match; bounded local decoding, raw-tar/PAX
  checks, strict JSON, file hashes and independent read-only safety rechecks pass. No source was retrieved.
- **What it supports.** `[LIT]` software provenance: recipe source URLs/digests, patch contents, declared
  build/host/run requirements, variants and metadata discrepancies. The P2 preparation recommendation is `[AGENT]`.
- **Limitations.** Declared upstream source archives were not independently read or compared here. Recipes and test
  instructions are not execution records. Compiler inputs, actual build/source correspondence and runtime conformance
  remain open; normalization stays PARTIALLY ESTABLISHED. No physical validity, parity or readiness is established,
  no P2 build is declared, no evidence label is upgraded and no later stage is authorized. The human-adopted source
  resolution and earlier source ledger are unchanged; this is a separate supplement.

## 13. P2 build-declaration decision packet

**[38]** Project records of the P2 Psi4 build-declaration decision packet, 2026-09-28.
- **Records.** The [decision packet](ms-001/P2-PSI4-BUILD-DECISION-PACKET.md) and its
  [source ledger](ms-001/P2-PSI4-BUILD-SOURCE-LEDGER.md).
- **Content.** A decision prepared for a person: whether to declare the exact conda-forge `osx-arm64` package
  `psi4-1.11-py314h53d0584_1`, archive SHA256 `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10`,
  with its exactly pinned Libint package `libint-2.13.1-h5a0831b_0`, archive SHA256
  `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f`, as the Psi4 build that P2 uses. It gives the
  evidence for and against, the options, one `[AGENT]` recommendation, exact candidate text for B2 §6, validity
  conditions and a map of every record that a later approval would change, including a fresh adoption of the revised
  B2 by C4, B3, C2 and C7.
- **Basis.** New records of this project, identified by SHA256 in the export manifest. Every claim is located in
  records already committed, chiefly [32] and [37] and the E-01 records [20] and [21]. No installed file, archive,
  installation or engine was newly read, retrieved, installed or run; committed public records were the only inputs.
- **Limitations.**
  - A proposal only. No build is declared, and no option is chosen, approved or applied. B2, C4 and every approval
    record are unchanged.
  - In an answer recorded on 2026-09-28, a person approved the declaration. It is applied to B2 §6, with the fresh
    adoption of the revised B2 by C4, B3, C2 and C7 ([approval record](ms-001/B2-P2-BUILD-HUMAN-APPROVAL.md); entry
    [39]). The packet's records themselves are unchanged.
  - Package identity is not proof of compiler inputs, source-to-binary correspondence, linkage, runtime conformance,
    numerical agreement, readiness, parity or physical validity. Basis normalization remains PARTIALLY ESTABLISHED.
  - The E-01 stop is recorded without inference about P2 in either direction.
  - No evidence label is upgraded. Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized, and Stage 1 remains
    BLOCKED.

## 14. MS-001 P2 build revision approved by a person

**[39]** Project records of the revision of B2 that declares the Psi4 build for P2, approved by a person in one
decision with C4, B3, C2 and C7 at their unchanged digests, in an answer recorded on 2026-09-28.
- **Records.**
  - The revision of B2 that declares, in
    [B2 §6](ms-001/B2-METHOD-DECLARATION.md#6-second-implementation-for-the-p2-check), the Psi4 build that P2 uses.
  - Its [approval record](ms-001/B2-P2-BUILD-HUMAN-APPROVAL.md), which also records the approval of C4, B3, C2 and
    C7 at their unchanged digests with the revised B2 adopted.
- **Basis.** New records of this project, identified by SHA256 in the export manifest and bound in the
  [freeze record](ms-001/STAGE0-FREEZE-RECORD.md#2-frozen-artifacts).
- **Limitations.**
  - The approval binds exact bytes by path and SHA256. It settles the selection of the P2 build only, validates
    nothing physically and upgrades no evidence label.
  - Package identity is not proof of compiler inputs, source-to-binary correspondence, linkage, runtime conformance,
    numerical agreement, readiness, parity or physical validity. Basis normalization remains PARTIALLY ESTABLISHED.
  - Stage 1 remains BLOCKED and is not authorized.

## 15. MS-001 W1 pre-run determination

**[40]** Project records of the pre-run executability determination of the wiring test W1, 2026-09-29.
- **Records.**
  - The [W1 record](ms-001/W1-PRE-RUN-DETERMINATION.md), whose disposition is W1 BLOCKED before execution.
  - Its [machine-readable outcome](ms-001/w1-outcome.json).
- **Content.**
  - Two independent blockers: the runner's interpreter environment against the declared allow-list, and the
    tracked-driver declaration against the no-delivery boundary.
  - One unresolved requirement: the capture of ignored or private sources.
  - The disposition of every acceptance criterion and stop condition of the
    [W1 specification](ms-001/C3-WIRING-TEST-PROPOSAL.md).
  - Proposed revisions, none applied.
- **Basis.** New records of this project, identified by SHA256 in the export manifest. They are written from private
  command and probe records of read-only inspection, hashing and interpreter-startup probes of the installed Stage 0
  environment on the project host. Those records are bound by SHA256 in the W1 record. No external source was
  retrieved or cited.
- **Limitations.**
  - W1 was not run. No AiiDA profile, computer, code or job was created, and AiiDA was not imported.
  - The observations are software and environment observations only. They show nothing about chemistry, and no
    chemistry evidence class applies.
  - The cause of the environment name that blocks W1 is an `[AGENT]` inference, not an established fact.
  - None of the C3 blockers is closed. Stage 1 remains BLOCKED and is not authorized.
  - *2026-10-04:* these records are the result under the specification of 2026-09-27 and are unchanged. The
    specification was revised afterwards (entry [42]), and the determination under the revised text is entry [43].

## 16. MS-001 W1 specification revision decision packet

**[41]** Project record of the decision packet on revision 01 of the W1 specification, 2026-10-04.
- **Records.** The [decision packet](ms-001/W1-REVISION-DECISION-PACKET.md).
- **Content.**
  - Options, an `[AGENT]` recommendation and rejection reasons for W1-BLOCKER-E2, W1-BLOCKER-E1, U-F1P and seven
    coupled gaps of the [W1 specification](ms-001/C3-WIRING-TEST-PROPOSAL.md).
  - Exact replacement text, marked UNAPPLIED, with a declared rule that reconstructs the revised bytes from the packet
    and the base file.
  - The SHA256 and byte sizes of the base, of the prospective revised specification and of the patch between them,
    which are retained privately, and the decision a person can take on those bytes.
- **Basis.** A new record of this project, identified by SHA256 in the export manifest. Two members of the
  aiida-core 2.9.2 wheel of entry [34] were read as text, without extraction, installation or import:
  `aiida/manage/configuration/settings.py`, a member not cited before, and `aiida/transports/plugins/local.py`.
  Their member digests are given in the packet. The other inputs are read-only inspections of this repository's Git
  index and configuration under declared environments, a commit-free measurement on temporary index files, file
  counts of the Stage 0 environment and a read of the frozen input file, all bound privately by SHA256. No source was
  retrieved.
- **Limitations.**
  - A proposal only. Nothing is chosen, approved or applied, and the specification is unchanged.
  - The source facts describe aiida-core source text, not its behaviour on the host. AiiDA was not imported.
  - The observations are software and environment observations. No chemistry evidence class applies.
  - W1 remains BLOCKED before execution and unrun, and none of the C3 blockers is closed. Stage 1 remains BLOCKED and
    is not authorized.
  - *2026-10-04:* the revision was approved by a person and applied afterwards (entry [42]). The packet is unchanged,
    and its statements are accurate as of its preparation.

## 17. MS-001 W1 specification revision 01 approved by a person

**[42]** Project records of revision 01 of the W1 specification, approved by a person in an answer recorded on
2026-10-04, and of its application.
- **Records.**
  - The [W1 specification](ms-001/C3-WIRING-TEST-PROPOSAL.md), revision 01, SHA256
    `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347`.
  - Its [approval record](ms-001/W1-REVISION-01-HUMAN-APPROVAL.md), which binds the base, revised and patch digests
    and records the fail-closed application of the approved bytes.
- **Basis.** New records of this project, identified by SHA256 in the export manifest. The revised bytes are those
  bound by the decision packet (entry [41]). The patch is retained privately. No source was retrieved.
- **Limitations.**
  - The approval binds exact bytes by path and SHA256. It settles the text of the W1 specification only, validates
    nothing physically and upgrades no evidence label.
  - It authorizes no W1 run, no writing of the W1 drivers, no AiiDA profile or job, no installation and no commit.
  - W1 remains unrun, and none of the C3 blockers is closed. Stage 1 remains BLOCKED and is not authorized.

## 18. MS-001 W1 pre-run determination 02, under revision 01

**[43]** Project records of the second pre-run executability determination of the wiring test W1, under revision 01
of its specification, 2026-10-04.
- **Records.**
  - The [second W1 record](ms-001/W1-PRE-RUN-DETERMINATION-02.md), whose disposition is INDETERMINATE before
    execution.
  - Its [machine-readable outcome](ms-001/w1-outcome-02.json).
- **Content.**
  - The earlier blockers W1-BLOCKER-E2 and W1-BLOCKER-E1 and the requirement U-F1P, disposed under the revised text.
  - The prerequisites of the decision packet's §10.2, item 3, each verified at the probed state or named as an
    untested requirement, the carriage of the declared superset through the job machinery among the latter.
  - The disposition of every acceptance criterion and stop condition of the revised specification.
- **Basis.** New records of this project, identified by SHA256 in the export manifest. They are written from private
  command and probe records of read-only inspection, hashing, interpreter-startup probes, a shell-chain simulation
  without AiiDA and the declared read-only Git invocations, on the project host. Three source files of the installed
  aiida-core 2.9.2, the distribution of entry [34], were read as text, without import. Their SHA256 values match their
  installed `RECORD` entries and are given in the record. The private records are bound by SHA256 in the record. No
  external source was retrieved.
- **Limitations.**
  - W1 was not run. No AiiDA profile, computer, code or job was created, and AiiDA, ASE and NumPy were not imported.
  - The observations are software and environment observations only. They show nothing about chemistry, and no
    chemistry evidence class applies. The statements about job carriage are `[AGENT]` inferences from source text.
  - INDETERMINATE is not readiness and predicts no pass. None of the C3 blockers is closed. Stage 1 remains BLOCKED
    and is not authorized.

## 19. MS-001 W1 run, stopped under §8 condition S10

**[44]** Project records of the one run of the wiring test W1, under revision 01 of its specification, 2026-10-04.
- **Records.**
  - The [W1 run record](ms-001/W1-RUN-RECORD.md), whose outcome is STOPPED under §8 condition S10.
  - Its [machine-readable outcome](ms-001/w1-run-outcome.json).
- **Content.**
  - The phases the run executed and the stop at the input point's module classification, repeated at the run end.
  - What was created, absent because never created, empty as observed and not queried.
  - The state of every acceptance criterion and stop condition, and F1 to F11 coverage.
  - The null closure inventory, and the separately labelled post-stop retained-evidence inventory bound by SHA256.
- **Basis.** New records of this project, identified by SHA256 in the export manifest. They are written from the
  run's own private records and the post-stop retained-evidence inventory, both bound by SHA256 in the record. The run
  used the installed aiida-core 2.9.2, the distribution of entry [34], in the Stage 0 environment. No external source
  was retrieved.
- **Limitations.**
  - The run stopped at the input point. No computer, code, input node or job was created, and no submission, payload,
    retrieval, F4 sequence or negative case was run.
  - The observations are software and environment observations only. They show nothing about chemistry, and no
    chemistry evidence class applies.
  - The stop is not readiness, and W1 did not pass. None of the C3 blockers is closed. Stage 1 remains BLOCKED and is
    not authorized.

## 20. H2 learning package sources

This section lists the sources of the H2 learning package in [learning/h2/](learning/h2/README.md), which are
conceptual educational, documentation and reference sources retrieved read-only on 2026-10-10, none of which is
evidence about the installed Psi4 1.11 build or its options or gives any H2 result for this project.

**[45]** MIT OpenCourseWare, 8.06 Quantum Physics III, Spring 2018, transcript of the video lecture "L18.1
Born-Oppenheimer approximation: Hamiltonian and electronic states" (PDF).
- **Links:** [transcript PDF](https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/b0a9e8628c1ff147e137527946219dfd_UOoKUdjVP78.pdf).
- **Locators used:** PDF pp. 2–3, the total Hamiltonian separated into nuclear kinetic, nucleus–nucleus and
  electronic parts; p. 3, nuclei are not, in principle, classical particles at fixed positions; pp. 4–5, electronic
  states solved at fixed nuclear positions, with energies that depend parametrically on those positions.
- **Used in:** [learning/h2/lesson-01-fixed-separation-scf.md](learning/h2/lesson-01-fixed-separation-scf.md).
- **Basis:** retrieved read-only on 2026-10-10 and inspected from a cached copy, SHA256
  `58bcbc736129c874515b7879f4eb0acaf85203db80efa59a660954da802d64eb`. The cached copy is private and is not
  redistributed.
- **Limitations:** a conceptual educational source, not evidence about the installed Psi4 1.11 build or its options.
  It gives no H2 result for this project.

**[46]** MIT OpenCourseWare, 8.06 Quantum Physics III, Spring 2018, transcript of the video lecture "L18.2 Effective
nuclear Hamiltonian. Electronic Berry connection" (PDF).
- **Links:** [transcript PDF](https://ocw.mit.edu/courses/8-06-quantum-physics-iii-spring-2018/bcd2e076c24614afc4853fd3825338a1_aY8iTiAfRzs.pdf).
- **Locators used:** p. 1, the variational principle; pp. 2–4 and p. 4, the effective nuclear Hamiltonian obtained
  by integrating out the electrons, in its lowest-order form; pp. 3–4, the Berry-connection and further derivative
  terms that the lowest-order form drops, which make it an approximation.
- **Used in:** [learning/h2/lesson-01-fixed-separation-scf.md](learning/h2/lesson-01-fixed-separation-scf.md).
- **Basis:** retrieved read-only on 2026-10-10 and inspected from a cached copy, SHA256
  `a9919ab3dc54d5a25562e22c746dc44e98082ad7a4a2e480d47c00621dd02828`. The cached copy is private and is not
  redistributed.
- **Limitations:** a conceptual educational source, not evidence about the installed Psi4 1.11 build or its options.
  It gives no H2 result for this project.

**[47]** MIT OpenCourseWare, 5.61 Physical Chemistry, Fall 2017, "Lecture 28 and 29 Notes: Modern Electronic
Structure Guided Notes" (PDF).
- **Links:** [lecture notes PDF](https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/0d07e780a9ba9181bb949c7618d3c99e_MIT5_61F17_lec28_29_notes.pdf).
- **Locators used:** p. 1, the electronic Schrödinger equation at fixed nuclear coordinates and the resulting energy
  surfaces; pp. 2 and 9, basis and method shown as separate choices; p. 4, the complete-basis-set limit; p. 7, the
  difference between the Hartree–Fock and exact energies, and the correlation energy.
- **Used in:** [learning/h2/lesson-01-fixed-separation-scf.md](learning/h2/lesson-01-fixed-separation-scf.md).
- **Basis:** retrieved read-only on 2026-10-10 and inspected from a cached copy, SHA256
  `216d7309ceeb542179f7f59726d567f2edb95a502ae842b084d2f3d472ffad94`. The cached copy is private and is not
  redistributed.
- **Limitations:** a conceptual educational source, not evidence about the installed Psi4 1.11 build or its options.
  These are guided notes with blanks: only their printed text is cited, and they do not say whether their electronic
  energy includes nuclear repulsion. They give no H2 result for this project.

**[48]** Psi4 manual, development version, chapter "HF: Hartree–Fock Theory" (page header `1.12a1.dev41`).
- **Links:** [psicode.org/psi4manual/master/scf.html](https://psicode.org/psi4manual/master/scf.html).
- **Locators used:** section Theory, the molecular-orbital coefficients as constrained variational parameters of a
  single Slater determinant, the density-dependent Fock matrix and the iteration to self-consistency, and the
  generalized eigenproblem with the overlap matrix; section Spin/Symmetry Treatment, the restricted treatment of
  closed-shell singlets and the unrestricted alternative; section Initial Guess, the convergence quantities with
  `E_CONVERGENCE`, `D_CONVERGENCE` and `MAXITER`, and the `CORE` and `SAD` guesses; section Stability Analysis, a
  converged SCF as a stationary point and the check for instabilities; section Convergence and Algorithm Defaults,
  defaults that depend on the type of calculation.
- **Used in:** [learning/h2/lesson-01-fixed-separation-scf.md](learning/h2/lesson-01-fixed-separation-scf.md),
  [learning/h2/h2-method-specification.md](learning/h2/h2-method-specification.md) and
  [learning/h2/h2-method-parameters.json](learning/h2/h2-method-parameters.json).
- **Basis:** retrieved read-only on 2026-10-10 and inspected from a cached copy, SHA256
  `c6e7d01da0538901b3bed1e19bbcdbc905360bb27ddb0d4e96bb5dbf8e06c63c`; identical bytes were served at psicode.org and
  at psi4.github.io. The cached copy is private and is not redistributed.
- **Limitations:** a documentation source, not evidence about the installed Psi4 1.11 build or its options, and it
  gives no H2 result for this project. It is a mutable development manual, used only for broad concepts and option
  names; the option names are not confirmed for the installed build, and its displayed equations are not cited as
  validated. The cached copy shows apparent issues, recorded here as `[AGENT]` readings. In Theory, the displayed
  Fock matrix adds the exchange term K although the Slater-rule energy shown just before it subtracts exchange, and
  the density-matrix energy expression has no factor one half for the density matrix defined there. In Initial
  Guess, the prose names the root-mean-square change in the density matrix as the second convergence quantity,
  while the example iteration output near the top of the page labels that column `RMS |[F,P]|`, a commutator
  residual, which is a different quantity. What `D_CONVERGENCE` tests in any installed build therefore remains
  unresolved, and nothing about the engine follows from these issues.

**[49]** Hehre, W. J.; Stewart, R. F.; Pople, J. A. Self-Consistent Molecular-Orbital Methods. I. Use of Gaussian
Expansions of Slater-Type Atomic Orbitals. J. Chem. Phys. 51, 2657–2664 (1969).
- **Links:** DOI [10.1063/1.1672392](https://doi.org/10.1063/1.1672392).
- **Locators used:** none inside the paper; it is cited only as the STO-3G reference that [50] names for hydrogen.
- **Used in:** [learning/h2/lesson-01-fixed-separation-scf.md](learning/h2/lesson-01-fixed-separation-scf.md).
- **Basis:** link-checked read-only on 2026-10-10; the DOI resolved to the publisher's article page. The paper was
  not inspected.
- **Limitations:** a literature reference, not evidence about the installed Psi4 1.11 build or its options, and it
  gives no H2 result for this project. Because the paper was not inspected, this catalogue makes no claim about its
  content.

**[50]** Basis Set Exchange, STO-3G basis set, element H, version 1, exported in Psi4 format through the BSE API on
2026-10-10 (export header version 0.12).
- **Links:** [basissetexchange.org export](https://www.basissetexchange.org/basis/sto-3g/format/psi4/?version=1&elements=1).
- **Locators used:** the hydrogen entry of the export, with its contracted s function, the Gaussian primitives of
  that function and its reference key.
- **Used in:** [learning/h2/lesson-01-fixed-separation-scf.md](learning/h2/lesson-01-fixed-separation-scf.md),
  [learning/h2/h2-method-specification.md](learning/h2/h2-method-specification.md) and
  [learning/h2/h2-method-parameters.json](learning/h2/h2-method-parameters.json).
- **Basis:** retrieved read-only on 2026-10-10 from the BSE API and inspected: basis export SHA256
  `29e91651bf30b0c4ec847384a2fe03157a47886ce3ef5faa669de70d73402779`; reference list SHA256
  `792c6b3290d11bf1946e8b494f511d5a60bf1703ceb6d13b05ea0db751515ea7`, which names the key hehre1969a, entry [49],
  for H. The cached copies are private and are not redistributed.
- **Limitations:** a reference data source, not evidence about the installed Psi4 1.11 build or its options. It
  says nothing about any installed basis file and gives no H2 result for this project.

**[51]** National Institute of Standards and Technology (NIST), CODATA 2022 recommended value of the Bohr radius.
- **Links:** [physics.nist.gov value page](https://physics.nist.gov/cgi-bin/cuu/Value?bohrrada0).
- **Locators used:** the recommended value, used only to convert displayed lengths between bohr and ångström.
- **Used in:** [learning/h2/lesson-01-fixed-separation-scf.md](learning/h2/lesson-01-fixed-separation-scf.md),
  [learning/h2/h2-method-specification.md](learning/h2/h2-method-specification.md) and
  [learning/h2/h2-method-parameters.json](learning/h2/h2-method-parameters.json).
- **Basis:** retrieved read-only on 2026-10-10 and inspected from a cached copy of the NIST page, SHA256
  `3da07839ac51e1d5197350488d08d6b54d1670001133a7ad775d19e3f87fc0af`. The cached copy is private and is not
  redistributed.
- **Limitations:** a reference data source, not evidence about the installed Psi4 1.11 build or its options. It
  says nothing about the constant that any engine uses internally and gives no H2 result for this project.

## 21. H2 Phase A run proposal sources

This section lists the sources of the Phase A run proposal in
[learning/h2/phase-a/](learning/h2/phase-a/H2-A-01-RUN-PROPOSAL.md). No engine was imported, initialized or run for
them, no installed file was executed, and none gives an H2 result.

**[52]** Psi4 v1.11 tagged-source files read for the Phase A run proposal.
- **Links and versions:** the GitHub-generated source archive of commit `f16f4ea2ff2351cc2ab877d9b3887fcf81c2a670`, to
  which tag `v1.11` resolves, SHA256 `040e843efd4e70d286d8705e501bd2be5c7f1f855ec439eb8a27e6565af50266`, the archive
  of [31]; <https://github.com/psi4/psi4/tree/v1.11>.
- **Locators used:** the file and line locators of
  [H2-A-01-RUN-PROPOSAL.md](learning/h2/phase-a/H2-A-01-RUN-PROPOSAL.md) §§3, 4, 6 and 7 and of the payload and
  driver comments, in 27 files:
  - `psi4/__init__.py`, `psi4/extras.py`, `psi4/header.py`;
  - `psi4/driver/driver.py`, `driver_util.py`, `molutil.py`;
  - `psi4/driver/p4util/util.py` and `python_helpers.py`;
  - `psi4/driver/qcdb/libmintsbasisset.py`, `psiutil.py` and `molecule.py`;
  - `psi4/driver/procrouting/proc.py` and `proc_util.py`;
  - `psi4/driver/procrouting/scf_proc/scf_iterator.py` and `subclass_methods.py`;
  - `psi4/src/read_options.cc`, `core.cc`, `export_mints.cc`;
  - `psi4/src/psi4/libscf_solver/rhf.cc` and `hf.cc`; `psi4/src/psi4/libmints/wavefunction.h` and `molecule.h`;
  - `psi4/src/psi4/liboptions/liboptions.cc`, `psi4/src/psi4/libpsi4util/process.cc`,
    `psi4/src/psi4/libpsio/filemanager.cc`, `psi4/src/psi4/libqt/timer.cc`;
  - `psi4/include/psi4/masses.h`.
- **Used in:** [H2-A-01-RUN-PROPOSAL.md](learning/h2/phase-a/H2-A-01-RUN-PROPOSAL.md),
  [h2_phase_a_payload.py](learning/h2/phase-a/h2_phase_a_payload.py) and
  [h2-a-01-input.json](learning/h2/phase-a/h2-a-01-input.json).
- **Basis:** inspected on 2026-10-10 from the retained private extract of the archive.
  - The archive digest was recomputed and matched.
  - Each of the 27 files equals its member in the archive.
  - A measure-then-assert check of 116 cited line ranges passed. Its private record has SHA256
    `ec1d92a111f0ebeb91c6a518443a31f073aabc89d7ffdfcc7aaf27f84f1a0723`. Earlier runs of the first 100, 104 and 107
    ranges also passed (`fc7e820de0b611c30756e402811c28b51e5b57faee79e2bce7b124758dbbd2c8`,
    `4d819ed662d095b8b2eb4e1fbeef76bc46754cbd1434f778816c0e403f1e96c4`,
    `a5fe0f6d13941357dd7e712252183680773a17d8fa48180f1c3cc12a68b90671`).
  - Third-party bytes are cited, not copied.
- **Limitations:** source text defines the behaviour of that source, not of any installed or future build.
  - `psi4/__init__.py` and `psi4/extras.py` are CMake templates whose installed copies are configured.
  - Compiled code cannot be compared with source by hash.
  - Nothing here establishes runtime conformance, source-to-binary correspondence or the meaning of any reported
    energy for a build.

**[53]** Path records of the declared Psi4 and Libint package archives.
- **Links and versions:** `info/paths.json` inside the `info` members of
  <https://conda.anaconda.org/conda-forge/osx-arm64/psi4-1.11-py314h53d0584_1.conda> (archive SHA256 `92d4aeb7…da10`)
  and <https://conda.anaconda.org/conda-forge/osx-arm64/libint-2.13.1-h5a0831b_0.conda> (`ca18cdfd…cb6f`), the archives
  declared in [B2 §6](ms-001/B2-METHOD-DECLARATION.md#6-second-implementation-for-the-p2-check) [39].
- **Locators used:** the records whose `_path` is `share/psi4/basis/sto-3g.gbs`,
  `lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so` (Psi4), `include/libint2/shell.h` and
  `lib/libint2.dylib` (Libint).
- **Used in:** [h2-a-01-static-identity.json](learning/h2/phase-a/h2-a-01-static-identity.json) and
  [H2-A-01-RUN-PROPOSAL.md](learning/h2/phase-a/H2-A-01-RUN-PROPOSAL.md) §6.
- **Basis:** inspected on 2026-10-10 from the retained, decoded metadata of [37].
  - `paths.json` SHA256 `42dd9797ecb2c72a2f489de611afffaee0095a8786eca06c7a55112abc51ffd8` (Psi4) and
    `18ab7ef1396d687ed7f89629f80eae614a9ddd184384fc5f8cfc48793830d9b9` (Libint), equal to the ledger rows of
    [RECIPE-METADATA-SOURCE-LEDGER.md](ms-001/RECIPE-METADATA-SOURCE-LEDGER.md).
  - The retained `info` members match their recorded SHA256. No archive was retrieved again.
- **Limitations:** a path record states what a package archive declares for a file. It does not show what any
  installation contains, what a binary was compiled from, or what it does.

**[54]** Static observation of the installed candidate Psi4 1.11 environment, 2026-10-10.
- **Content:**
  - a names-only listing of `conda-meta/`;
  - the package records of psi4, libint, python 3.14.7, qcelemental 0.51.2 and qcengine 0.51.0, and the installation
    history file;
  - the bytes and SHA256 of `share/psi4/basis/sto-3g.gbs`, `include/libint2/shell.h`, `lib/libint2.dylib`, the core
    extension and `bin/python3.14` (with its two links);
  - sixteen installed Psi4 Python files, byte-compared with [52].
- **Used in:** [h2-a-01-static-identity.json](learning/h2/phase-a/h2-a-01-static-identity.json), which gives
  prefix-relative paths, digests, sizes and package fields; [H2-A-01-RUN-PROPOSAL.md](learning/h2/phase-a/H2-A-01-RUN-PROPOSAL.md)
  §§6–7 and 11; and the driver's preflight expectations.
- **Basis:** read-only static inspection on 2026-10-10 under a person's bounded authorization of that day.
  - The permitted operations were lstat, readlink, reading and hashing.
  - Every path was resolved inside the environment, and nothing in it was executed, imported or loaded.
  - Private raw records: SHA256 `d62f2af23d9e81854ad55182da9b5ccb8cf6f2702cb0a13f66c825e78e9034ed` and
    `e715e89022b8656f2da6c24521315f1bc8cd1a61d681f87335c02eb0551f75eb`.
  - The environment's location is private.
- **Limitations:** static installed bytes at one instant. They are not loaded or runtime identity, not
  source-to-binary correspondence, and not a capability or readiness.
  - The installed `psi4/header.py` was not compared.
  - The core extension differs from its archive path record [53]. The reason is not established.

**[55]** Installed macOS sandbox documentation and a bounded fixture containment assessment, 2026-10-10.
- **Links and versions:** installed on macOS 27.0.1 (build 26A434):
  - the manual page sandbox-exec(1), SHA256 `0d264f72dc6a8e0db5474840f33b512542c469beb109ed146c17055da287336b`;
  - the manual page sandbox(7), `9043d9296715714f95b4de6c5f88a5436c5cc3b83b62641327212078c5c69b04`;
  - the manual page sandboxd(8), `88177c5ed67c8e43f35cd9995e5724526bc656e8b996a9cb8084cd5780bc6698`;
  - the Command Line Tools SDK header `usr/include/sandbox.h`,
    `5baa98c212110d6323f7d73f4b42b0072a4c66a826a46c8bfd8fb850305f9416`;
  - the `sandbox-exec` binary, `58839ef01b4eef8aac0d2aa8f9d1c074ae45aafe3533965b030672450064acc8`.
- **Locators used:**
  - sandbox-exec(1) NAME and DESCRIPTION: deprecation and options;
  - sandbox(7) DESCRIPTION: inheritance by new processes, and enforcement on acquisition of resources;
  - `sandbox.h` lines 6–10, 22–54 and 60–85: deprecated `sandbox_init` and its named profiles with their stated
    intents.
- **Used in:** [H2-A-01-RUN-PROPOSAL.md](learning/h2/phase-a/H2-A-01-RUN-PROPOSAL.md) §§8.5–8.6 and §10;
  [H2-A-01-DECISION-PACKET.md](learning/h2/phase-a/H2-A-01-DECISION-PACKET.md) §4; and, for route R2,
  [H2-R2-METHOD-REVISION.md](learning/h2/phase-a-r2/H2-R2-METHOD-REVISION.md),
  [H2-A-R2-RUN-PROPOSAL.md](learning/h2/phase-a-r2/H2-A-R2-RUN-PROPOSAL.md) §§7–8,
  [H2-A-R2-DECISION-PACKET.md](learning/h2/phase-a-r2/H2-A-R2-DECISION-PACKET.md) and
  [h2-r2-platform-identity.json](learning/h2/phase-a-r2/h2-r2-platform-identity.json).
- **Basis:** inspected on 2026-10-10.
  - A fixture assessment, private record SHA256 `91e4abae76d1b5d16a89b8af4779519500e9a83b59217cc80dfbe6c6b6cb9fff`
    with raw results `fb3a29387e4270e82d9d3bfd55dc8b2557c2b837656c9707204e6456b62832d4`, ran `sandbox-exec` around a
    fake non-engine client only.
  - Its only network destinations were an AF_UNIX socket and the literal address `127.0.0.1`, both owned by the
    assessment, with unsandboxed controls.
- **Limitations:**
  - The documentation marks the facility deprecated and does not describe the custom-profile language.
  - The fixture observations cover the tested operation classes on this OS build only. They establish no coverage of
    other destinations, of traffic mediated by system services, or of the engine's behaviour.
  - They do not satisfy the accepted no-network stop condition, and they authorize nothing.

## 22. H2 route-R2 preparation sources

This section lists the evidence for the route-R2 method-revision proposal in
[learning/h2/phase-a-r2/](learning/h2/phase-a-r2/H2-R2-METHOD-REVISION.md). No engine was imported, initialized or run
for it, nothing in the candidate environment was executed, and it gives no H2 result.

**[56]** Route-R2 fixture assessment: static platform observation and sandbox tests around fake processes,
2026-10-10.
- **Links and versions:** installed on macOS 27.0.1 (build 26A434), as read from `SystemVersion.plist` with
  `plistlib`:
  - `/usr/bin/sandbox-exec`, 135 136 bytes, SHA256
    `58839ef01b4eef8aac0d2aa8f9d1c074ae45aafe3533965b030672450064acc8`, the binary of [55];
  - the four documentation digests of [55], re-checked and unchanged.
- **Content:**
  - a static observation of those two platform facts, by reading and hashing files only;
  - design probes of the candidate profile around a fake Python child. Without a `/dev/null` allowance, opening
    `/dev/null` for writing and Python's `subprocess.DEVNULL` were refused. A UDP send to `127.0.0.1` was refused. The
    environment names were unchanged by `sandbox-exec`. A nested `sandbox-exec` exited 71 with
    `sandbox_apply: Operation not permitted`. Without its `-D` parameters the profile was rejected (exit 65);
  - the route-R2 test suite (28 tests) on the final bytes, and the accepted Phase A suite (37 tests), unchanged;
  - targeted mutation checks classified by the intended assertion. On the final driver, 18 defects were killed and
    two earlier unfaithful mutants were kept and labelled invalid.
- **Used in:** [H2-R2-METHOD-REVISION.md](learning/h2/phase-a-r2/H2-R2-METHOD-REVISION.md) (R2-S),
  [H2-A-R2-RUN-PROPOSAL.md](learning/h2/phase-a-r2/H2-A-R2-RUN-PROPOSAL.md) §§4–8 and 10,
  [H2-A-R2-DECISION-PACKET.md](learning/h2/phase-a-r2/H2-A-R2-DECISION-PACKET.md),
  [h2-r2-sandbox.sb](learning/h2/phase-a-r2/h2-r2-sandbox.sb) (comments) and
  [h2-r2-platform-identity.json](learning/h2/phase-a-r2/h2-r2-platform-identity.json).
- **Basis:** inspected on 2026-10-10.
  - The assessment's private record has SHA256 `2c47551118750cd30d65d683c686e0ab01cd33c625687275b61bf1211e2f5527`.
  - Its raw records are kept with it: the platform observation
    `46dcd6ed79d1cbb9daa29e34dcb59e7e110d09a407ad1c3241f80a4366d55d18`, the final suite output
    `073d021c2b13e608bd2fb247c16a8bfaabed340719adacb22249fb280fec2909` and the final mutation summary
    `2e85a55f7f0e3f55b3cad54a32a965e202163fa3d0da35ea8ca408c9c2d10f95`.
  - `sandbox-exec` was run only around fake, non-engine processes. The only network destinations were AF_UNIX sockets
    and the literal address `127.0.0.1`, owned by the tests, with unsandboxed controls.
  - Nothing was installed and no system setting was changed.
- **Limitations:**
  - The observations cover the tested operation classes on this OS build with this `sandbox-exec` digest only:
    AF_UNIX connect and bind, TCP connect and UDP send to `127.0.0.1`, and file creation and append outside the two
    write directories. They establish no coverage of other destinations, socket types or system-call paths, of
    traffic mediated by system services, or of the engine's behaviour under the profile.
  - The profile semantics are undocumented, and `sandbox-exec` is deprecated.
  - Refusal is not detection.
  - Fake outputs are not chemistry evidence.
  - They do not satisfy the accepted no-network stop condition unless a person approves the method revision, and they
    authorize nothing.

## 23. H2 route-R2 enabling revision

This section lists the test record of the enabling revision of the route-R2 driver in
[learning/h2/phase-a-r2/](learning/h2/phase-a-r2/H2-A-R2-RUN-PROPOSAL-02.md). The revision binds the method revision
that a person approved and the [human approval record](learning/h2/phase-a-r2/H2-R2-METHOD-HUMAN-APPROVAL.md). No
engine was imported, initialized or run for it, no driver mode was run against the real prefix, interpreter or runs
root, and it gives no H2 result.

**[57]** Route-R2 enabling-revision test record: engine-free tests and targeted mutation checks of the route-R2
driver that binds the approved method revision, 2026-10-10.
- **Links and versions:**
  - the route-R2 driver, SHA256 `0b3172f8388b0f0c053a2b7a6945394e7e796aae8b14d0228447d7bc860af9b6`, and its test
    module, SHA256 `01e2c631690e31423891f198e727391c86029d6ae50013c88e91316ec3c14da8`;
  - the accepted Phase A suite, unchanged;
  - run on macOS 27.0.1 (build 26A434), with `/usr/bin/sandbox-exec` of 135 136 bytes and SHA256
    `58839ef01b4eef8aac0d2aa8f9d1c074ae45aafe3533965b030672450064acc8`, as read statically with `plistlib` and by
    hashing, equal to the platform identity record.
- **Content:**
  - the route-R2 suite (32 tests) on the final bytes and the accepted Phase A suite (37 tests), both passing;
  - the cases the route-R2 suite covers:
    - the shipped constant, equal to the approved method revision's digest and to the approval record's digest;
    - the enabled path under a FIXTURE authorization, which gives COMPLETED_PENDING_REVIEW through the real wrapper;
    - the approval record absent, unreadable, altered, replaced or changed during a run;
    - authorization, approval and provenance mismatches;
    - the unset gate;
    - the preserved behaviours and real-sandbox prevention around fake processes.

    Every refused launch spawned no process and wrote nothing to the runs root.
  - a targeted mutation check. It changed each changed executable line and the redundant comparison of the
    authorization's approval digest with the constant, ten single changes in all, with one unmutated control. Its
    two runs are kept as recorded:
    - in the first run, three changes were killed by their intended assertion and six were classified invalid under
      that run's strict rule, and the documentary change survived;
    - read with the patterns declared before that run, an intended assertion failure that shows the modelled defect
      was observed in eight runs. Three are the runs recorded killed. Five are runs recorded invalid, whose incidental
      failures and errors remain and whose classification is unchanged. Eight is not a kill count;
    - the second run repaired only the classifier's patterns, used a test variant that was later withdrawn, and is not
      counted.

    Traced through the driver's paths, five of the changes are fail-closed: they break the enabled path, so that every
    launch is refused. Four change no launch decision, only a message, the stage of a refusal or a post-run reason;
    one of them is the redundant comparison. None of the ten was shown to permit a launch that the unmutated driver
    refuses. These are `[AGENT]` assessments;
  - a check that the enabled driver rejects a private, deliberately invalid authorization proposal on exactly its
    three invalid fields. The check ran in-process, with a synthetic report and no process spawned.
- **Used in:** [H2-A-R2-RUN-PROPOSAL-02.md](learning/h2/phase-a-r2/H2-A-R2-RUN-PROPOSAL-02.md) §8 and
  [H2-A-R2-RUN-DECISION-PACKET.md](learning/h2/phase-a-r2/H2-A-R2-RUN-DECISION-PACKET.md).
- **Basis:** inspected on 2026-10-10.
  - The private test record has SHA256 `127ca3f147cf98b2ea14aa25b507857e620dd8106d2dd9fecd43e0dd7a447af3`.
  - Its raw records are kept with it:
    - the final route-R2 suite output, `fbb1283c9b4fcdd69799aa653c05cc331057a52a052f7e7820b1bced6499278b`;
    - the accepted suite output, `773989df068dc9f805d925772f136cc82441d083aac07c520268f7534c549ef8`;
    - the mutation summaries of the two runs, `c61b5a5a675924c8a73244b9df3fcf817686cd4340bb8bcc5158bc6e65b45aa4` and
      `7120aaebdb201fabacc18e43935251bdd1701eae28edf86cc2fbc15f29ab4d6f`;
    - the assessment of recorded classes, intended-assertion observations and launch effects,
      `e888694ac9849a8a38573490f7ef1582d471cdb9f483bf83de5a129758d77298`.
  - `sandbox-exec` was run only around fake, non-engine processes. The only network destinations were AF_UNIX sockets
    and the literal address `127.0.0.1`, owned by the tests. Nothing was installed and no system setting was changed.
- **Limitations:**
  - Fake outputs are not chemistry evidence, and the FIXTURE authorizations used are not authorizations.
  - The tests show that the driver checks bytes and fields; they cannot show that a person authorized anything.
  - The limitations of [56] apply unchanged, including the absence of detection and the unobserved behaviour of the
    engine under the profile.
  - The mutation assessments are `[AGENT]` assessments; their independent assessment belongs to review.
  - The record authorizes nothing.

## 24. H2-A-01 authorized attempt, stopped before launch

This section lists the records of the one attempt of job H2-A-01 that a person authorized through the route-R2 driver.
The attempt was not exercised. The driver's `run` mode was never invoked, no engine was imported, initialized or run,
and it gives no H2 result.

**[58]** Project records of the run authorization of H2-A-01 and of its stop as STOP_UNRUN before launch, 2026-10-10.
- **Records.**
  - The [run authorization record](learning/h2/phase-a-r2/H2-A-01-HUMAN-RUN-AUTHORIZATION.md).
  - The [stop record](../results/h2/H2-A-01/README.md), with its
    [machine-readable outcome](../results/h2/H2-A-01/outcome.json) and its
    [provenance record](../results/h2/H2-A-01/provenance.json).
- **Content.**
  - The person's answer "yes, authorized" and the question it answered, verbatim, with the receipt time of the answer,
    the run-decision packet and the current run proposal by SHA256, M1 accepted, the scope, the exclusions and the
    limits of the packet's §5.
  - The prerequisites prepared and checked: a fresh code-provenance record, one static preflight with every check
    passing, a driver-schema authorization record that passed an independent interlock check, and an empty runs root.
  - The stop: the automatic permission check of the agent client that was delegating the run refused delivery of the
    run assignment, with its reason quoted verbatim. Zero run invocations, no engine process and no attempt
    directory. The disposition STOP_UNRUN, with what was and was not done, the open items and the gates.
- **Basis.** New records of this project, identified by SHA256 in the export manifest. They are written from private
  task records, cited by description and SHA256 only:
  - the person's reply as recorded on receipt, `bd67c57e82f0ca0199df434060def9ccd7c8e2c7e4a3c21bcd84d044c189abe3`;
  - the driver-schema authorization record, `d002c75ff69c7572152609be142bfba34b35e6117189417bc7516459215ab261`;
  - the stop disposition, `a982114308eb90e1679a5564423dc291eb44ea3ed6925d52d701a381b5ea1782`, and the disclosure that
    records a later overwrite of it at the same private location and the recovery of its exact bytes,
    `4e9ff394e5aa425e9ba43f0f95c5e700cb284d18f388c3e14dccd8e5e9d43fb2`;
  - the record of the permission refusal, `4f5c47c9b7bdbe70a7c393e974a6fbbbe7ba1a7e4e1a2caae400c7c6f3dc61d1`;
  - the prerequisite report, `c49108238943fe54ac49616202d1f9d37742f8f4d4f867639501429c2557009a`, and the independent
    readiness verification, `3ce908f684fb08ed99cc2c98697d21cf1d6acc7dafb6f32c7073638a012c2de0`.

  The remaining private records are listed in the provenance record. Nothing was installed, built or retrieved, and
  no system setting was changed. Network activity was not observed, and no claim about it is made.
- **Limitations.**
  - No run took place. Nothing about the engine, the sandbox profile or the engine environment was observed: E1, the
    Libint load-name risk, compatibility with the profile, loaded identity, P4 and source-to-binary correspondence stay
    open, and M1 is accepted but not resolved.
  - A static preflight pass is not readiness, loaded identity or runtime identity.
  - The driver-schema authorization record is checked by the driver by bytes and fields only and cannot show that a
    person authorized anything.
  - STOP_UNRUN is an orchestration stop before launch. It is not a driver tier, an engine failure or chemistry
    evidence, and no chemistry evidence class applies.
  - No launch permission remains in the task that held the authorization. The records do not carry it forward and
    authorize nothing.

## 25. H2-A-01 continuation, stopped before any driver invocation

This section lists the records of the continuation of the one authorized attempt of job H2-A-01, which a person
directed on 2026-10-11. The continuation stopped during preparation. The driver was not invoked in any mode, no
engine was imported, initialized or run, and it gives no H2 result.

**[59]** Project records of the continuation of H2-A-01 and of its stop as STOP_UNRUN before any driver invocation,
2026-10-11.
- **Records.**
  - The [continuation stop record](../results/h2/H2-A-01-continuation-01/README.md), with its
    [machine-readable outcome](../results/h2/H2-A-01-continuation-01/outcome.json) and its
    [provenance record](../results/h2/H2-A-01-continuation-01/provenance.json).
- **Content.**
  - The person's reply "approved. Keep going." with its receipt time and its qualifier, recorded as direction to
    continue the same unchanged single attempt in a new task through one exact temporary permission rule for the
    delegation command; the terms of the earlier authorization and its acceptance of M1 unchanged.
  - Two defects in the private preparation instructions and how each was handled. The driver's own runs-root checks
    were not run.
  - O1, the executing agent's command `echo verify`, displayed as "Placeholder to check nothing", with its purpose not
    established.
  - The stop: the safeguard notice displayed by the executing agent's client, quoted verbatim; the executing agent's
    statement; the missing account and the unknown cause, kept distinct. The disposition STOP_UNRUN; zero driver
    invocations in any mode, no engine process and no attempt directory; what was not reached, the open items and the
    gates.
- **Basis.** New records of this project, identified by SHA256 in the export manifest. They are written from private
  task records, cited by description and SHA256 only:
  - the person's reply as recorded on receipt, `907909171d2053faac283aba229982d63a0fb1734164c870eeb652d165ec513a`;
  - the operator handoff that sets out the permission route, `39df6564283ea73e7d78cf64564f05b0d597c7372d0d82e2341123da1fd13d05`;
  - the terminal disposition, `8f92edd4b3f997ca6aace859fe8b470b0c0d703e520d419ce30157462cbb5e88`, and the observed
    state after the stop, `e6a6e6774d96e39ff53dbb39f149940e5b78a6230946327df3c924bc28f4f1c4`;
  - the terminal capture of the safeguard notice, `07d93aa31f8283e358b8bb8f7bf0c9d14a092d95e003bf0c92670d61782c41c5`;
  - the coordinating agent's record of O1 and of the stop,
    `e1a08f197fa3ab7fccf2b4d8ad49c02e2d118811451fcb6cd9099386f3c7500c`, and its clarification, which withdraws that
    record's statements about any recovery of session records,
    `181fcff0d96da3ef0a8a1a7919c0898b46bcf105c50a2d3de52861c9d947c5aa`.

  The remaining private records are listed in the provenance record. Nothing was installed or built, and no system
  setting was changed.
- **Documentation consulted.** The operative official documentation of the supported permission-resolution route,
  read by the supervising agent through its web tool, accessed 2026-10-11. Basis: recorded. All three pages are named
  in the supervising agent's persisted statement of the three documentation URLs and the access date,
  `855fc60651d0ad2841a3a77f3da1f6c03c92584117a4972ee15e90b6587c402b`. That statement is not the original web-tool
  transcript or captured page content, nothing is claimed about the pages beyond what it says, and the pages were not
  re-opened for this entry. The permissions and settings pages are also named in the supervising agent's earlier
  documentation record, `e68367a6f3e69f175c88f06e56223d32e01be2e37cfd62d81f9dd089ad5e5f86`.
  - Permissions, https://code.claude.com/docs/en/permissions (permission rule syntax, Bash rules, managing
    permissions).
  - Settings, https://code.claude.com/docs/en/settings (the project-local settings source and its root resolution).
  - Interactive mode, https://code.claude.com/docs/en/interactive-mode (the `/status` command).

  The documents were used to map the client's displayed settings-source class to the repository-local settings file.
  They do not show that the installed client behaves exactly as documented. They are not a scientific source and
  change no evidence label. No chemistry source was retrieved. Network traffic of the host and of the agent clients
  was not measured, and no claim about it is made. The engine was never executed.
- **Limitations.**
  - No run took place. Nothing about the engine, the sandbox profile or the engine environment was observed: E1, the
    Libint load-name risk, compatibility with the profile, loaded identity, P4 and source-to-binary correspondence stay
    open, and M1 is accepted but not resolved.
  - The missing account of O1, the unestablished purpose of O1 and the unknown cause of the safeguard stop are
    permanent limits of these records.
  - STOP_UNRUN is an orchestration stop before any driver invocation. It is not a driver tier, an engine failure or
    chemistry evidence, and no chemistry evidence class applies.
  - No launch permission remains. The records do not carry any authorization forward and authorize nothing.
