# MS-001 source resolution record

Date: 2026-09-27. MS-001 scope option B, after the closure of Stage 0.

This record settles, as far as version-matched primary sources permit, the five source definitions that the Stage 0
package lists as prerequisites to starting Stage 1 ([B2 §8](B2-METHOD-DECLARATION.md#8-what-stays-open);
[freeze record §1](STAGE0-FREEZE-RECORD.md#1-disposition)). Each item receives exactly one disposition:
`ESTABLISHED FROM VERSION-MATCHED SOURCE`, `PARTIALLY ESTABLISHED` or `UNRESOLVED/BLOCKED`. Every source used here is
listed with its identity, retrieval record and digest in the dated 2026-09-27 section of the
[source ledger](SOURCE-LEDGER.md#source-resolution-retrievals-2026-09-27).

## 1. Scope and what this record is not

The five items are:
1. **G4.** GFN0 parameter provenance through the declared CP2K route (B2 §3).
2. **OMEGA.** The unit and conversion semantics of CP2K `FORCE_EVAL/DFT/XC/HF/INTERACTION_POTENTIAL/OMEGA` under
   `POTENTIAL_TYPE MIX_CL` (B2 §4).
3. **Basis normalization.** Whether CP2K and Psi4 normalize contracted functions, so that a non-unit coefficient of
   a single-primitive def2-TZVP shell is scaled away (B2 §6; N2 in [C4 §2](C4-TOLERANCES-AND-CONVERGENCE.md#2-numerical-convergence-protocol)).
4. **N8 representations.** The two records that N8 compares ([C4 row 10](C4-TOLERANCES-AND-CONVERGENCE.md#1-tolerance-table-spike-86-instantiated)):
   (i) the projected gradient that CP2K `GEO_OPT` uses and (ii) the printed analytic composite gradient after the
   constraints, with their format, units as printed and rounding, and whether a combined formatting allowance
   r = r_(i) + r_(ii) can be defined.
5. **Psi4 compiled steps.** Whether the compiled Psi4 v1.11 SAD atomic solver under `SAD_SCF_TYPE DIRECT`, the
   double-hybrid predicate `is_c_hybrid()` and `core.scfgrad` under `SCF_TYPE DIRECT` use any auxiliary or fitting
   basis under the declared settings (B2 §6).

What this record is not:
- **Not physical evidence.** Reading source establishes software behaviour as the source defines it. It is not
  physical evidence, method validation, parity, calculation evidence or a capability of any installed build. No
  engine, compiled code, renderer, geometry generator or retained source module was executed, and no calculation
  was run.
- **Not an upgrade of labels.** No `[AGENT]`, `[SPEC]`, `[GAP]` or `UNVERIFIED` label in B2, C4 or any other record
  changes. The findings below are recorded beside those labels, with their scope stated.
- **Not a change of frozen definitions or gates.** [C4](C4-TOLERANCES-AND-CONVERGENCE.md) is byte-identical at
  SHA256 `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`. No threshold, budget, parameter,
  partition, drive value, N-rule or gate changes, and no dependency moves between stages. Options for a C4 decision
  are set out separately in [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md), which is not applied and not
  approved.
- **Not readiness or authorization.** Stage 1 remains BLOCKED and is not authorized. This record cannot authorize
  it, and it authorizes no calculation, installation or engine run.

## 2. Method and source identity

**Standard.** Only version-matched primary sources are used: the CP2K 2026.2 release archive, the Psi4 v1.11
tagged source and the Libint source at the version that Psi4 v1.11 names. Search snippets, secondary summaries,
development-branch behaviour and the output of language models are not used as evidence. Third-party bytes are
cited and hashed, not copied. They are retained privately.

**How the sources were read.** Every source was read as text. Small scripts only hashed files, parsed retrieval
metadata, compared trees by Git blob SHA1, traced identifiers and asserted locators. A measure-then-assert check
confirms that each cited line range in this record contains the cited text: 211 locator assertions over 72 files
pass. A first run had 12 wrong line ranges; they were corrected, and the failing run is retained privately. Every
CP2K and Psi4 file cited here was checked to equal the blob of the tag-commit tree.

**Source statements and project inferences.** A statement with a file and line locator reports what that source
text says, with `[LIT]` provenance and no chemistry class. Where this record draws a conclusion that the source does
not state, the step is marked **Project inference**. It is this project's reading over the cited `[LIT]` text, and
it can be checked against those lines.

**Negative findings.** A statement that something does not occur rests on one of two stated methods:
- **Tracing.** The identifier is followed through every routine that receives it.
- **Search.** A search whose pattern and file set are given in the text.

A search covers only the files named. It does not cover code that another package supplies at run time, compiler
defaults or settings made outside the source.

**Four distinctions kept throughout.**
- **Timestamps.** A cached retrieval of 2026-09-26 keeps its original access time. The 2026-09-27 re-verification
  of its digest is recorded separately.
- **Identity kinds.** Tag-resolution metadata (which ref names which commit) is distinct from the content hash of a
  file.
- **Branch versus release.** The mutable `support/v2026.2` branch is distinct from the immutable release revision.
- **Source versus build.** Behaviour defined by source is distinct from the behaviour of any actual build.

**CP2K 2026.2.**

| Identity | Value | Source |
|---|---|---|
| Tag | `v2026.2`, an annotated tag object `09496e055e132aa3dba53a7751ebdf432b4ebb78`, unsigned (the tag record reports verification `unsigned`), tagged 2026-07-15T09:12:14Z | `SR-cp2k-ref-tag-v2026.2-api`, `SR-cp2k-tagobj-v2026.2-api` |
| Release revision | The commit the tag resolves to, `67b5da876dd6a76b8b021d5a04d1c81ba79a4c50`, "Cut release version 2026.2". It changes four files: `CMakeLists.txt`, `docs/changelog.md` and `src/cp2k_info.F`, and it adds `REVISION` | `SR-cp2k-commit-67b5da87-api` |
| Release archive | `cp2k-2026.2.tar.bz2`, 79 898 041 bytes, SHA256 `f9bd86f580f57a53a0768c0045d1417f9f9a1d66d851ed7f662f496200043373`, equal to the digest that the release record publishes for this asset | `SR-cp2k-2026.2-release-tarball`, `SR-cp2k-release-v2026.2-api` |
| Revision recorded inside the archive | The archive's `REVISION` file reads `git:c92cc08`. That is the parent of the release revision, `c92cc08b45378b85150447011b5a4bb552f5b797`. The release revision is the commit that adds this file with this content, so the archive's own revision string names the parent, not the tag commit | `SR-cp2k-commit-c92cc08-api` |
| Archive against release revision | All 8 985 regular files in the archive are byte-identical, by Git blob SHA1, to the tree of the release revision (8 999 blob entries). Fourteen tree paths have no regular-file match: 10 Git metadata files (`.gitignore` files, `.gitattributes`, `.git-blame-ignore-revs`) and `CODEOWNERS` are absent from the archive, and 3 symbolic links (`CONTRIBUTING.md`, `data/BASIS_MOLOPT_UZH`, `data/POTENTIAL_UZH`) are present in the archive as symbolic links and were not compared by content | `SR-cp2k-tree-67b5da87-api` |
| Branch | The head of `support/v2026.2` resolved to `67b5da87…` at 2026-09-27T14:38:17Z. This is tag-resolution metadata at that moment and says nothing about the branch at any other time | `SR-cp2k-ref-branch-support-v2026.2-api` |
| Stage 0 files cited from the branch | Six files retrieved from the branch on 2026-09-26 (`S0-cp2k-emsl-basis`, `S0-cp2k-all-basis`, `S0-cp2k-ecp`, `S0-cp2k-src-disp-pairpot`, `S0-cp2k-src-disp-utils` and `S0-cp2k-src-disp-d3`) match their ledger SHA256 and are byte-identical to the release-revision blobs. The 2026-09-26 listing of `data/` (`S0-cp2k-data-listing`, 68 entries) names, for every entry, the same Git object as the release revision | Source ledger |

Every CP2K locator in this record is at the release revision `67b5da87…`, read from the release archive, whose files
equal that tree. The identity of the six cached branch files with release-revision bytes establishes only that
those bytes are equal. It does not establish the state of the branch at any other time, and it does not extend to
the 2026.2-branch manual pages cited in Stage 0, which were not compared.

**Psi4 v1.11.** The tag `v1.11` is an annotated, unsigned tag object, `75fa0e14aa16a868a00eced50eaaa2f8658aa806`,
that resolves to commit `f16f4ea2ff2351cc2ab877d9b3887fcf81c2a670`. The release carries no source asset. The source
was read from the GitHub-generated archive of that commit (51 818 737 bytes, SHA256
`040e843efd4e70d286d8705e501bd2be5c7f1f855ec439eb8a27e6565af50266`). That archive is generated on request and is not
a published release asset, so its digest identifies the bytes read here and nothing more. All 9 821 of its files
equal the blobs of the commit's tree. The eight Psi4 files cached on 2026-09-26 match their ledger SHA256 and are
byte-identical to those blobs.

**Libint.** Three things are kept apart:
- **The library version read.** `include/libint2/shell.h` at Libint `v2.8.1`, a lightweight tag on commit
  `4482d01abc37732a24b24799d3efe1d1f89a2891`. It was retrieved by tag and by commit, with identical SHA256
  `c798162776893960c44fc119a69c00f201c28e164da0885522a5889f7c0e4f00`.
- **What Psi4 v1.11 states.**
  - `codedeps.yaml` names the Libint repository at `v2.8.1` with CMake constraint `2.8.1` and conda constraint
    `null`.
  - `psi4/CMakeLists.txt` line 189 calls `find_package(Libint2 2.8.1 CONFIG REQUIRED`. This states a minimum
    version, not the identity of the library in any build.
- **What the installed E-01 build linked.** The installed-build survey ([SOURCES [26]](../SOURCES.md)) records a
  dependency of the core extension library on a library named `libint2`. Its version is not recorded in the
  retained records.

(1) is the version that (2) names as its source pin and minimum. (2) does not bind any build to (1), and (3) is
unknown. Behaviour read at Libint v2.8.1 is therefore not established for any build (Section 6).

**libxc.** No libxc source was newly read. The libxc version that a CP2K 2026.2 build links remains `[GAP]`, and this
record does not close it.

## 3. Dispositions

**Disposition criterion.** The same test is applied to every item:
- **`ESTABLISHED FROM VERSION-MATCHED SOURCE`.** The question, as it concerns behaviour that software defines, is
  answered in full by version-matched source, including every component the answer depends on.
- **`PARTIALLY ESTABLISHED`.** Part of the answer depends on a component whose version the version-matched source
  does not fix, or the source gives no answer to part of the question as posed. An example of the first case is an
  external library that the release names only as a dependency, a reference build or a minimum.
- **`UNRESOLVED/BLOCKED`.** No part of the answer can be read from version-matched source.

What a particular build or run does is not part of a source-definition question: which bytes it loads, which binary
it is and what it prints. Those questions are recorded as open obligations in the stage where the frozen package
already places them, and they do not by themselves lower a disposition. A definitional ambiguity in a frozen record
is also not a source question. It is recorded as such (Section 7).

| # | Item | Disposition | What version-matched source establishes | Remaining question | Smallest next step | Needs Stage 1 authorization |
|---|---|---|---|---|---|---|
| 1 | G4 | `PARTIALLY ESTABLISHED` | The per-element parameter file (`data/xTB0_parameters`, with digest) and the global constants hard-coded in CP2K source, both at the release revision. Also: the file-resolution order; the D4 settings that CP2K source fixes; and what a run's output can and cannot state. The D4 reference data come from the external dftd4 library. The release's toolchain has two routes to dftd4, each with its own archive digest: a standalone dftd4 4.2.0 archive, and a tblite 0.6.0 archive whose bundled dftd4 subproject it patches. The identity of that bundled source was not examined. The release's CMake accepts any dftd4 version | Which dftd4 source (archive, digest and patch state) the declared route uses. This is a prospective definition that the release does not fix. Which bytes a run loads and which library a build links are P1 identity provenance within Stage 1 (B2 §8), not part of G4 | A declaration of the dftd4 source through the revision sequence. Either route of the release's toolchain is a candidate. No observation of a build is needed | No |
| 2 | OMEGA | `ESTABLISHED FROM VERSION-MATCHED SOURCE`, for CP2K's unit and conversion semantics of `OMEGA` only | `OMEGA` carries no unit and is not converted (read). The exchange kernels add ω² to a combination of Gaussian exponents in bohr⁻², so ω acts in bohr⁻¹ and `OMEGA 0.25` is 0.25 bohr⁻¹ (project inference from the cited expressions) | None for these semantics. Not touched by this record: agreement with the published functional stays `UNVERIFIED`, and the libxc version that a CP2K build links stays `[GAP]` | None for the definition. A Stage 1 output line `HFX_INFO\| Omega` would show the value consumed, not its unit | Only for that output observation |
| 3 | Basis normalization | `PARTIALLY ESTABLISHED` | CP2K normalizes primitives and contracted functions, so a positive single-primitive coefficient is scaled away (project inference from the cited formulas). In Psi4 v1.11 the DFT-grid coefficients are normalized by Psi4 source. The integral coefficients are normalized inside Libint2, read at Libint v2.8.1, a version that Psi4 names only as its source pin and minimum | The Libint2 version of the Psi4 build that P2 uses, and `Shell::renorm` at that version | A static read of that build's package record for Libint, and of `shell.h` at the version named | No calculation or Stage 1 work, but a read outside this repository needs its own authorization |
| 4 | N8 representations | `PARTIALLY ESTABLISHED` | The order of evaluation, constraint application and printing. The writers, formats and printed units of the constrained force records. And that CP2K writes no separate, direct record of the gradient `GEO_OPT` uses, traced through its call chain. In memory that gradient is the exact negation of the unformatted constrained force array that the force records render | How formatted output is rounded, which CP2K source leaves to the compiler and run-time library, and therefore any allowance r. Also a definitional ambiguity in C4 row 10, whether a force record can serve as record (i), which source cannot settle | A decision under C4 §3 on the reading of row 10 and on r. [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md) sets out the options, including no change. An instrumented build that records the optimizer vector and the composite forces before the constraint is a further option outside this task's scope | The decision does not. Observing records on a build does. Instrumentation would need its own authorization |
| 5 | Psi4 compiled steps | `ESTABLISHED FROM VERSION-MATCHED SOURCE`, for the behaviour the Psi4 v1.11 tagged source defines | Under the declared settings the SAD atomic solver, the SCF exchange builder and the analytic gradient construct and pass no auxiliary or fitting basis, and `is_c_hybrid()` is false | Two separate obligations stay open. **Build provenance:** whether the installed binary was built from this source, and with which changes. **Runtime conformance:** whether the binary takes these paths | For build provenance: a static read of the installed package's build record. For runtime conformance: the JK and JKGrad headers of a Stage 1 P2 run. These name the algorithm used, not the build's provenance | The static read does not, but needs its own authorization. The run does |

The prerequisite "five definitions settled from version-matched source" therefore does not yet hold: items 1, 3 and 4
are partial. N8 remains BLOCKED. It has not been run and has no outcome. Stage 1 remains BLOCKED and is not
authorized.

## 4. G4: GFN0 parameter provenance through CP2K

**Question.** B2 §3 requires G4 to be closed "from version-matched CP2K source (the file and revision that hold the
GFN0 parameters, with its digest)". Where do the GFN0 parameters of `GFN_TYPE 0` come from, and what can a run's
output state about them?

**What the source establishes** (CP2K 2026.2 release revision; file and lines):
- **Selector.** `GFN_TYPE` has the values `0`, `1` and `TBLITE`, with default `1`
  (`src/input_cp2k_tb.F` 181–193). It is read at `src/cp_control_utils.F` 1482. Value 0 dispatches to the
  GFN0 parameter reader `xtb0_parameters_init` (`src/xtb_parameters.F` 185–188).
- **Per-element parameters.**
  - When `PARAM_FILE_NAME` is not given, GFN0 uses the file name `xTB0_parameters`
    (`src/cp_control_utils.F` 1579–1594). The documented keyword default, `xTB_parameters`, is replaced in that
    case (`src/input_cp2k_tb.F` 434–438). `PARAM_FILE_PATH` defaults to an empty string (427–431).
  - The reader forms the file name as path followed by name (`src/xtb_parameters.F` 222–223). It acts only on
    records headed `$Z`, reading the one whose element number matches, and it aborts on an unknown key (294–297).
    If an element is absent it only warns and leaves that element undefined (330–335). The `$info` and `$globpar`
    blocks at the top of the file are not used by this routine.
- **The release data file.** `data/xTB0_parameters` at the release revision, SHA256
  `278461cabbf89b14379aedc78ef3e141c8cef1f911f3a3c72530aec7a52b6d34`. Its first records name `GFN0-xTB` and a
  preprint DOI (lines 1–4). The DOI was not retrieved and is a pointer only. The file holds `$Z` entries for H, C,
  O, Si and Ge at lines 29, 117, 155, 274 and 649.
- **Global constants hard-coded for GFN0.** When the corresponding keyword is not given
  (`src/cp_control_utils.F`):
  - dispersion scaling s6 = 1.00 and s8 = 2.85 (1606–1612), and a1 = 0.80 and a2 = 4.60 (1625–1632);
  - Hückel constants, among them kp = 2.4868 (1654–1662). When `HUCKEL_CONSTANTS` is given, ksp is recomputed from
    ks and kp (1651–1654);
  - electronegativity constants ksen = 0.006, kpen = −0.001 and kden = −0.002 (1714–1720);
  - `ENSCALE` −0.09 (1737–1740);
  - the six SRB parameters, read from their keyword (1820–1829), whose defaults are in `src/input_cp2k_tb.F`
    549–555.

  The documented default of `HUCKEL_CONSTANTS` is the GFN1 set (`src/input_cp2k_tb.F` 472–477). Hard-coded
  element tables (valence, electronegativity, occupation, covalent radii and charge limits) are at
  `src/xtb_parameters.F` 41–150, and a GFN0 pair factor at 763–779.
- **Basis.** The method's minimal basis is a contracted-Gaussian expansion of Slater functions
  (`src/xtb_parameters.F` 543–597), with 6 Gaussians per function and 4 for hydrogen by default
  (`src/input_cp2k_tb.F` 214–224, read at `src/cp_control_utils.F` 1574–1578).
- **Dispersion as fixed in CP2K source.**
  - For GFN0 without `VDW_POTENTIAL` the dispersion is D4 (`src/cp_control_utils.F` 1561–1571; keyword text at
    `src/input_cp2k_tb.F` 239–242).
  - In the D4 path the damping values s6, s8, a1 and a2 come from the constants above, over a rational-damping
    template obtained from the dftd4 library (`src/qs_dispersion_d4.F` 259–271).
  - When CP2K is built against dftd4 4.2 or later, it sets the two-body smooth-cutoff width to 0.05 and the
    three-body width to 0. Two pairs of environment variables can override these widths: `DFTD4_DISP2_SMOOTH_WIDTH`
    or its fallback `TBLITE_D4_DISP2_SMOOTH_WIDTH`, and the `DISP3` pair likewise (`src/qs_dispersion_d4.F`
    296–304; the reader at 88–112).
  - A build without the dftd4 library aborts (790).
- **Dispersion data supplied outside CP2K.** *Project inference:* the D4 reference data are supplied by the dftd4
  library linked into the build, because the D4 path calls that library and aborts without it. The library's own
  source was not read.

**The dftd4 dependency as the release defines it.**
- **The release's CMake.** It requires dftd4 with no version constraint and selects an interface by version:
  - below 4.0, the version 3 interface;
  - from 4.2, the 4.2 interface (`CMakeLists.txt` 871–884 and 886–889).
- **The release's toolchain**, its reference build scripts, has two routes to dftd4, each with its own archive:
  - **Standalone.** `install_dftd4.sh` fetches `dftd4-4.2.0.tar.xz` with SHA256
    `467e024071510ad82b862c66c383c2ebc164fc1140e15dfc79f48d2f999fd184`
    (`tools/toolchain/scripts/stage8/install_dftd4.sh` 9–10 and 33–36) and builds it without modification (33–46).
  - **Bundled in tblite.** `install_tblite.sh` fetches `tblite-0.6.0.tar.xz` with SHA256
    `372281aedb89234168d00eb691addb303197a9462a9c55d145c835f2cf5e8b42`
    (`tools/toolchain/scripts/stage8/install_tblite.sh` 9–12). It unpacks that archive and applies the CP2K-supplied
    patch `dftd4-4.2.0-gradient-fixes.patch` (SHA256
    `5335cb7d02a8c3141f28967ef61418f425fb1e638d51fe75618b700321d9087a`) to the dftd4 subproject bundled in it
    (35–43). The version string 4.2.0 on this route names the patch file (line 12). This route never fetches the
    standalone dftd4 archive. The patch changes, among other things, the library's default two-body smooth width
    from 0 to 0.05 (`tools/toolchain/scripts/stage8/dftd4-4.2.0-gradient-fixes.patch` 18–19).
  - **Not examined.** The identity of the dftd4 source bundled in the tblite archive, and its relation to the
    standalone dftd4 4.2.0 archive, were not examined. This record does not claim that they are the same.
- **Other sources of dftd4.** The toolchain can also take dftd4 from the system or from a user path
  (`tools/toolchain/scripts/stage8/install_dftd4.sh` 49–58).

The release's toolchain therefore specifies two different dftd4 sources, one of them bundled in another archive and
patched. The release does not fix the dftd4 that a build uses.

**What a run's output can and cannot state.**
- **Banner.** The xTB banner prints `GFN0-xTB` and `Version 1.1` (`src/header.F` 216–245). This names the method
  selected, not a parameter set.
- **Control parameters.** The DFT control-parameter printout prints at the default print level
  (`src/input_cp2k_print_dft.F` 818–820). Its `xTB| Parameter file` line gives the file name only, in 50
  characters (`src/cp_control_utils.F` 2712–2713), with no directory, resolved location or digest.
  - For D4 it prints `xTB| D4 Dispersion: Parameter file` with the `DISPERSION_PARAMETER_FILE` value, whose default
    is a D3 file name (2736–2738). This record did not trace whether the D4 path reads that file.
  - It prints `xTB| Electronegativity scaling` from the GFN1 constant (2753–2754) and does not print the GFN0
    electronegativity constants.
- **Per-element parameters.** These cannot be printed for GFN0. With `SUBSYS/PRINT/KINDS/POTENTIAL` switched on,
  GFN_TYPE 0 reaches an abort (`src/xtb_types.F` 380–391).
- **Build flags.** The program information lists `libdftd4` and a dftd4 interface marker when the library is compiled
  in (`src/cp2k_info.F` 226–234). It does not give a dftd4 version.

**Gate structure.** B2 §8 places CP2K installation and build identity within Stage 1, and P1's identity provenance,
including parameter provenance, among the Stage 2 gates. G4, the definition from source, is a prerequisite before
Stage 1. This record keeps that structure. It separates two things:
- **The prospective source definition (G4, before Stage 1).** For the CP2K-internal parameters this is settled
  above. For the dftd4-supplied part it is not fixed by the release. A declaration can fix it, without any build.
- **The run observations (P1, within Stage 1).** These are which parameter-file bytes a run loads (the resolution
  order below decides), which dftd4 a build links and the values of the smooth-width environment variables. B2 §8
  already places them in Stage 1, and this record does not move them before it.

The resolution order: the parser opens files through `discover_file` (`src/common/cp_files.F` 520–550). It tries
the name as given, relative to the working directory, first. It then tries the data directory: the environment
variable `CP2K_DATA_DIR` if set, otherwise the compiled-in directory (`src/common/cp_data_dir.c` 18–24), which the
build sets to the installation's data directory (`src/CMakeLists.txt` 1825–1836). A P1 run record therefore needs
the resolved file's path and digest, the linked dftd4 identity and the two smooth-width environment settings. The
output alone supplies none of them.

**Not established.**
- The dftd4 source that the declared route will use.
- That GFN0 accepts `UKS` and `MULTIPLICITY`, which remains a Stage 1 dependency.
- Any relation between these parameters and the published method, which was not examined.

**Disposition: `PARTIALLY ESTABLISHED`.**
- **Why partial.** Under the criterion of Section 3, part of the GFN0 parameter set, the D4 reference data, depends
  on a component whose version the release does not fix.
- **G4 stays `[GAP]` for P1.** Its source-definition part is now settled except for the dftd4 source.
- **Smallest next step.** A declaration of the dftd4 source (version, archive digest and patch state) through the
  revision sequence. Either route of the release's toolchain is a candidate, and choosing between them is part of the
  decision. This record does not make that declaration. The step needs no build, installation or Stage 1
  authorization.

## 5. OMEGA: unit and conversion in CP2K

**Question.** In what unit does CP2K use `OMEGA` in the declared exact-exchange path, and is any conversion
applied? This item concerns CP2K's unit and conversion semantics only.

**What the source states** (CP2K 2026.2 release revision):
- **Declaration.** `OMEGA` is declared in the `INTERACTION_POTENTIAL` section with default 0.0 and no unit string
  (`src/input_cp2k_hfx.F` 272–280). In the same section `CUTOFF_RADIUS` carries the unit string `angstrom`
  (303–311). `MIX_CL` is described as 1/r + erf(ωr)/r (253–266).
- **No conversion.** A keyword has no unit unless a unit string is given (`src/input/input_keyword_types.F` 202,
  407–409). A real value is converted only when the keyword has a unit (`src/input/input_parsing.F` 651–695, the
  test at 686–688). The number in the input is therefore the number stored.
- **Consumers.** The value is copied without transformation into the exchange potential parameters
  (`src/hfx_types.F` 719–720). In each consumer ω² is added to Rho = ζη/(ζ + η), formed from Gaussian exponents
  (`src/hfx_libint_interface.F` 97–105), and the Boys-function argument is scaled by ω²/(ω² + Rho). The consumers
  read are:
  - the `MIX_CL` four-centre kernel (`src/hfx_libint_interface.F` 167–179);
  - the `MIX_CL` screening estimates (`src/hfx_pair_list_methods.F` 332–345);
  - the two- and three-centre integrals (`src/libint_2c_3c.F` 372–375).
- **Internal units.** The internal length unit is the bohr. A bohr value is used as is, and an ångström value is
  multiplied by `bohr` = 1/`angstrom` (`src/common/cp_units.F` 720–733; `src/common/physcon.F` 147). Basis exponents
  are stored as read from the basis file (`src/aobasis/basis_set_types.F` 1375–1385 and 1410–1420), and these
  exponents enter the exchange code (`src/hfx_types.F` 1746–1761).
- **Printed value.** The exchange information block prints `HFX_INFO| Omega` as a bare number
  (`src/hfx_types.F` 2888–2892).

**Project inference.** Positions are in bohr and the exponents are stored as read. With the basis file's exponents
in bohr⁻², ω² is added to a quantity in bohr⁻², so ω acts in bohr⁻¹, and `OMEGA 0.25` is 0.25 bohr⁻¹. The source
attaches no unit label to `OMEGA`. The unit is this project's reading of the dimensional consistency of the cited
expressions, and it holds for every consumer read above.

**Outside this item.** B2 §4 records libxc's ω for ωB97X-D3 as 0.25 in bohr⁻¹ [S0-libxc-wb97, line 80]. Under that
recorded convention the value and the unit agree. This record does not touch:
- libxc's unit convention, which it did not read;
- the libxc version a CP2K 2026.2 build links, which stays `[GAP]`;
- agreement with the published functional, which stays `UNVERIFIED`, with its defining reference `[GAP]`.

That the GAPW exact-exchange route reaches these kernels is a Stage 1 dependency (C2 §5, item 5).

**Disposition: `ESTABLISHED FROM VERSION-MATCHED SOURCE`**, for CP2K's unit and conversion semantics of `OMEGA`
only. Nothing further is needed for the definition. A Stage 1 output line `HFX_INFO| Omega` would show the value
consumed, under Stage 1 authorization.

## 6. Basis normalization in CP2K and Psi4

**Question.** For the single-primitive def2-TZVP shells that carry a non-unit coefficient in CP2K's file and 1.0 in
Psi4's (B2 §6), does each engine normalize contracted functions so that the coefficient is scaled away?

**CP2K 2026.2.**
- **Reading.** The basis reader stores exponents and coefficients as read (`src/aobasis/basis_set_types.F`
  1375–1385 and 1410–1420). It opens the basis file through the same parser and file discovery as in Section 4
  (1269).
- **Normalization type.** A basis set starts with normalization type −1 (line 78). For every orbital basis, kind
  initialization sets it to 2 (`src/qs_kind_types.F` 1338–1345).
- **Type 2** (`src/aobasis/basis_set_types.F` 1137–1174):
  - First, each primitive's normalization factor is multiplied into its coefficient (1182–1202).
  - Then a contraction factor 1/√(prefactor × Σ c_i c_j …) is computed (1056–1098).
  - Both enter the transformation from primitives to contracted functions (843–859).
- **Project inference.** For one primitive with coefficient c, the contraction factor is proportional to 1/|c|. The
  contracted function is therefore sign(c) times the normalized primitive, and |c| is scaled away.
- **The def2-TZVP shells concerned.** The single-primitive coefficients in question are positive: for C they are
  0.46445822433 and 0.24955789874 (`data/EMSL_BASIS_SETS` 33982–34010). The retained text comparison of the two
  basis files, identified by SHA256 in the freeze record, lists positive values for O, Si and Ge. *Project
  inference:* after normalization these shells equal those with coefficient 1.0.
- **Other paths.** The GAPW soft basis inherits the normalization type (`src/aobasis/soft_basis_set.F` 292), and
  the exchange code uses the orbital basis transformation (`src/hfx_types.F` 1746–1761).

**Psi4 v1.11.** The coefficients are traced from the `.gbs` file to each consumer:
- **Parsing and construction.** The Python basis parser passes the original coefficients
  (`psi4/driver/qcdb/libmintsgshell.py` 338–346; `psi4/driver/p4util/python_helpers.py` 196). The C++ constructor
  builds every shell as `Unnormalized` (`psi4/src/export_mints.cc` 118–133).
- **Psi4's own normalization.** For an `Unnormalized` shell, `ShellInfo::normalize_shell` applies primitive and then
  contraction normalization to the working coefficients and keeps the file values as the original coefficients
  (`psi4/src/psi4/libmints/gshell.cc` 60–76, 78–84, 110–130 and 132–140).
- **Two arrays.** The basis set keeps both the normalized and the original coefficients
  (`psi4/src/psi4/libmints/basisset.cc` 649–651 and 801–803).
- **Consumer 1, the DFT grid.** Basis-function collocation uses `GaussianShell::coefs()`, the normalized
  coefficients (`psi4/src/psi4/libfock/points.cc` 748–754; `psi4/src/psi4/libmints/gshell.h` 287). This path is
  established in Psi4 source.
- **Consumer 2, integrals.**
  - `update_l2_shells` runs with its default `embed_normalization = true` (`psi4/src/psi4/libmints/basisset.cc`
    823–824; `psi4/src/psi4/libmints/basisset.h` 171). It builds the Libint2 shells from the original coefficients
    (`psi4/src/psi4/libmints/basisset.cc` 867–884).
  - The two-electron and one-electron integrals use these Libint2 shells (`psi4/src/psi4/libmints/eribase.cc`
    225–230; `psi4/src/psi4/libmints/onebody.cc` 351–352).
  - In Libint v2.8.1, the `Shell` constructor with embedding calls `renorm()` (`include/libint2/shell.h` 169–181).
    `renorm()` applies primitive normalization and then, while the static flag `do_enforce_unit_normalization()`
    holds its default true, normalizes the contraction to unity (294–303 and 359–401).
  - A word-bounded search for `do_enforce_unit_normalization` over all 9 821 files of the Psi4 v1.11 archive found
    no occurrence. Nothing in Psi4's own source changes the flag.
- **A path not taken.** A path without embedding exists for SAP potentials (`psi4/src/psi4/libmints/basisset.cc`
  1265–1285). It is reached from the SAP guess (`psi4/src/psi4/libscf_solver/hf.cc` 961), which is not declared.

In Psi4's `def2-tzvp.gbs` the shells concerned carry 1.0. The Psi4 question is therefore whether contractions are
normalized at all:
- **The grid path.** They are, by Psi4 v1.11 source.
- **The integral path.** They are, by Libint v2.8.1 source, which is not bound to any build (Section 2).

**Not established.**
- The Libint2 version of any Psi4 build, and so the integral-path normalization of the build that P2 uses.
- Whether a library or plugin loaded at run time changes Libint's normalization flag.
- Conventions beyond the radial normalization, such as the solid-harmonic normalization and phase of each engine,
  which were not examined.

Which basis-file bytes a CP2K run reads is a run observation for Stage 1, governed by the file resolution of Section
4.

**Disposition: `PARTIALLY ESTABLISHED`.**
- **Why partial.** Under the criterion of Section 3, the Psi4 integral path depends on Libint2, whose version the
  Psi4 v1.11 source fixes only as a minimum.
- **Established.** CP2K is established from version-matched source, and so is the Psi4 grid path.
- **Remaining.** The Libint2 version linked by the Psi4 build that P2 uses, and `Shell::renorm` at that version.

**Next step.** A static read of that build's package record for Libint, and of `shell.h` at the version it names.
It runs nothing and is not Stage 1 work, but it lies outside this repository and needs its own authorization. N2's
qualification "subject to the normalization item in B2 §6" therefore still applies.

## 7. N8: the two compared representations

**Question.** Which records carry (i) the projected gradient that `GEO_OPT` uses and (ii) the analytic composite
gradient after the constraints? What are their format, units as printed and rounding? Can r = r_(i) + r_(ii) be
defined?

**Order of operations in one `GEO_OPT` evaluation** (CP2K 2026.2 release revision):
1. **Evaluation call.** BFGS calls `cp_eval_at` (`src/motion/bfgs_optimizer.F` 290 and 409–410). That evaluates
   energy and forces of the top-level force environment, the `MIXED` force_eval (`src/motion/gopt_f77_methods.F`
   132–134).
2. **Sub-force_evals and mapping.**
   - The `MIXED` evaluation (`src/force_env_methods.F` 314) evaluates each sub-force_eval with the external controls
     skipped (1229–1231). The fixed-atom constraint is therefore not applied in any sub-force_eval.
   - `GENMIX` maps the sub-force_eval forces using a numerical derivative of the mixing function (1356–1385).
3. **Constraint.** Back in the top-level evaluation the controls run (361), and `fix_atom_control` runs first
   (366–369). For `COMPONENTS_TO_FIX XYZ` it sets the three force components of each fixed atom to exactly 0.0
   (`src/constraint_fxd.F` 220–223) and stores the result in the particle forces (230–240). Call the resulting
   in-memory array F_c. Restraints, virtual sites, an external potential and force rescaling follow; B3 §3 declares
   none of them.
4. **Force print.** `FORCE_EVAL/PRINT/FORCES` of the top-level force_eval writes a decimal rendering of F_c
   (`src/force_env_methods.F` 419–445).
5. **Optimizer gradient.** `cp_eval_at` packs the particle forces into the optimizer gradient with scale factor −1
   (`src/motion/gopt_f77_methods.F` 141–147; `src/subsys/cp_subsys_types.F` 518–521). The space-group option that
   would further modify it, `KEEP_SPACE_GROUP`, defaults to false (`src/start/input_cp2k_motion.F` 875–881) and is
   not declared. *Project inference:* multiplication by −1 is exact in IEEE binary floating-point arithmetic, so the
   in-memory optimizer gradient g equals −F_c exactly, element by element.
6. **Records of g.** The uses of g were traced through its call chain, not found by a text search for writers.
   - Within `geoopt_bfgs`, g is filled by `cp_eval_at` (`src/motion/bfgs_optimizer.F` 290 and 409–410).
   - It is passed to the space-group routine only when `KEEP_SPACE_GROUP` is set (294–297 and 414–417).
   - It forms the difference `dg` passed to `bfgs` (341–344), which reads it (653–694).
   - It is passed to `rat_fun_opt` and `geoopt_get_step` (386–388) and to `energy_predict` (405). They only read it
     (484–520, 765–813 and 871–892).
   - It is passed to `gopt_f_io` (427–428), which forwards it only to `check_converg` (`src/motion/gopt_f_methods.F`
     340–342, with the same call at 383, 387 and 411).
   - `check_converg` uses it only to form a maximum and an RMS value (660–666, with the RMS value completed at 669)
     that its write statements print (the maximum at 700–710, the RMS value at 717–720).
   - `cp_eval_at` only packs it (`src/motion/gopt_f77_methods.F` 141–147).
   - The BFGS routine otherwise writes messages and an unformatted Hessian restart file
     (`src/motion/bfgs_optimizer.F` 1000–1022).

   No routine in this chain writes a component of g. The `MAX_FORCE` and `RMS_FORCE` aggregates are convergence
   diagnostics, not a component-wise record. The trace covers the routines that receive g. The force writers listed
   below receive F_c, not g.

**Records of F_c** (n = `NDIGITS`, clamped to 1…20, default 8):

| Record | Switched on | Writer and format | Units as printed | Content |
|---|---|---|---|---|
| Top-level `FORCE_EVAL/PRINT/FORCES` to standard output, the default file name `__STD_OUT__` | High print level; must be switched on (`src/input_cp2k_force_eval.F` 321–343) | Three components and the norm in `ES(n+7).n`, which is ES15.8 by default (`src/force_env_utils.F` 482 and 486–490), after multiplication by the conversion factor of `FORCE_UNIT` (503) | `FORCE_UNIT`, default `hartree/bohr` (`src/input_cp2k_force_eval.F` 334–341), named in the header | A decimal rendering of the forces F_c |
| Top-level `FORCE_EVAL/PRINT/FORCES` to a named file | As above | Three components in `F(n+6).n`, which is F14.8 by default (`src/force_env_utils.F` 577–580), with no conversion; the writer is chosen at 430–436 | The header states "FORCES in [a.u.]" (591); `FORCE_UNIT` is not applied | A decimal rendering of F_c |
| `MOTION/PRINT/FORCES`, the optimizer trajectory | High print level (`src/input_cp2k_motion_print.F` 199–203) | Default format XMOL, in the branch for non-position print keys (361–367): three components in `F20.10` after unit conversion (`src/particle_methods.F` 303–309; `src/motion_utils.F` 380–382). Other formats were not examined | `UNIT`, default `hartree*bohr^-1` | A decimal rendering of F_c |

Each sub-force_eval's own `PRINT/FORCES` writes that constituent's unconstrained forces over its own atom set (step
2). Those are constituent records. They are not records of F_c and not records of the composite optimizer gradient,
and no sign relation to g holds for them.

The sign relation g = −F_c holds only for the top-level constrained array in memory. A record of F_c is a decimal
rendering of that array. The negation of a parsed record therefore approximates g, only as closely as the rendering
allows.

**Rounding.** The writers render values with `F` and `ES` editing. The number of printed digits is fixed by n. How a
value is rounded to those digits is not fixed by CP2K source. The basis for that statement:
- **Format templates.** The format templates of the three writers were read (`src/force_env_utils.F` 486–490 and
  577–580; `src/particle_methods.F` 303–309). None contains a rounding-mode edit descriptor.
- **`ROUND=` specifiers.** A case-insensitive, word-bounded search for a `ROUND=` specifier over all 1 546 files
  under `src/` found none. A search for rounding-mode edit descriptors in literal format strings also found none. A
  first run of the search, without a word boundary, matched only the identifier `background`; it is retained
  privately.
- **`OPEN` statements.** The two `OPEN` statements through which CP2K opens files (`src/common/cp_files.F` 447–466)
  carry no `ROUND=` specifier. Output to standard output goes to a preconnected unit.
- **Build files.** The CMake build files contain no rounding option. For Intel compilers they set `-fp-model
  consistent` (`cmake/CompilerConfiguration.cmake` 146–148). That is a floating-point model option, and its effect
  on formatted-output rounding is not established here.

These searches cannot exclude compiler defaults, compiler flags supplied outside the CMake files, or run-time
library settings. The rounding of formatted output is therefore left to the compiler and run-time library of a
build. Round-to-nearest is not established by CP2K source.

**Source fact and interpretation.**
- **The source fact** (established). Under the declared settings, CP2K 2026.2 writes no separate, direct record of
  the optimizer's gradient array g (step 6). In memory, g is the exact negation of F_c. The force records are decimal
  renderings of F_c.
- **The interpretation** (not settled by source). The question is whether a negated force record can serve as N8's
  record (i). C4 row 10 states that "N8 compares two recorded quantities: (i) the projected gradient that GEO_OPT
  uses, and (ii) the analytic composite gradient after the constraints are applied". The paragraph after C4's
  tolerance table adds: "Which CP2K output records the projected gradient used by GEO_OPT, and therefore the
  recorded values that N8 compares, is `UNVERIFIED`. If no such record exists, N8 is indeterminate and blocking."
  C4 does not state that the two records must be independent, or that record (i) must be written by the optimizer.

**Reading A: a force record can carry (i).**
- **The claim.** Because g = −F_c in memory, a negated rendering of F_c records the gradient `GEO_OPT` uses, to
  within the rendering. Records then exist for both (i) and (ii), and the condition "if no such record exists" does
  not apply.
- **The comparison would be empty.** Both records render the same array, so for the retained components their
  difference reflects formatting only, and it is zero by construction if one record serves for both. A fault in how
  the constraint acts on retained components would appear identically in both. The comparison could not detect it,
  and in that sense it would be a comparison of an array with itself.
- **r is still undefined.** r would have to bound the difference between two renderings. CP2K source fixes the
  digits but not the rounding, so r is not defined from version-matched source. Row 10 keeps N8 from being run until
  it is.

**Reading B: record (i) must be the optimizer's own record of g.**
- **The claim.** No such record exists (the source fact). The paragraph after C4's tolerance table then classes N8
  as indeterminate and blocking.
- **r.** r_(i) has nothing to bound.

**Under both readings.**
- N8 remains BLOCKED and has not been run.
- Source reading alone defines no r.
- A decision under C4 §3 is needed before N8 can have an outcome:
  - under reading A, at least to define r, a step that row 10 itself routes through the revision sequence, and to
    decide whether a comparison that cannot detect a projection error is wanted;
  - under reading B, to redefine record (i).

**Proposal (`[AGENT]`).** This record proposes that reading A be taken as the literal reading of C4's text, because
C4 states no independence requirement and the source establishes g = −F_c in memory. It further proposes that the
approval roles weigh that reading's consequence when they decide N8's definition: the retained-component comparison
would carry no information. This record does not decide between the readings. It leaves the ambiguity for a
separately reviewed decision, and it does not instantiate N8.

**r as a conditional allowance.** CP2K source fixes the number of printed digits of a record but not how values are
rounded to them. It gives no bound on the difference between a printed field and the value in memory. Any
per-record formatting allowance is therefore conditional and would have to be declared and justified.
- **A candidate.** One unit in the last printed place. Its unit, its dependence on the decimal exponent of an `ES`
  field and its behaviour at an exponent boundary would have to be defined explicitly. This is a proposal
  (`[AGENT]`), not a CP2K source result.
- **Its preconditions.** Any such allowance also requires that:
  - the record exists;
  - its unit label is present and known;
  - the force-to-gradient sign is applied;
  - every field is finite, parseable and not overflowed.

  The magnitude at which a field overflows depends on the field width, the number of digits, the sign of the value
  and rounding. No universal cutoff is stated here.

**Disposition: `PARTIALLY ESTABLISHED`.**
- **Why partial.** Under the criterion of Section 3, CP2K source gives no answer to the rounding part of the question,
  and so none to r. The reading of row 10 is a definitional ambiguity, not a source question. The disposition is the
  same under either reading.
- **Established.** The order of operations; the writers, formats and printed units of the records of F_c; and that
  no separate, direct record of g is written.

**Status, not outcome.** N8 has not been run and has no outcome. C4 row 10 states that N8 is not run while its
representations and r are undefined. N8's status is BLOCKED. Under reading B, the paragraph after C4's tolerance
table also classes it as indeterminate and blocking. That class is a status of the definition reached by source
reading, not the result of an executed N8.

**Options for the definition.** [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md) sets out the options for a
decision under C4 §3. A further option lies outside this task's scope: a separately authorized, instrumented CP2K
build that records the optimizer vector and the composite forces before the constraint, with full provenance of the
changed code. No instrumentation, code change or engine run is authorized here.

## 8. Psi4 compiled steps and fitting bases

**Question.** Under the declared settings (`GUESS SAD`, `SAD_SCF_TYPE DIRECT`, `DF_SCF_GUESS false`,
`SCF_TYPE DIRECT`, `BASIS_GUESS` false and a custom dictionary without a `c_mp2` block), does any of the three
compiled steps construct or use an auxiliary or fitting basis? Options that B2 does not declare keep their defaults.

A zero atomic-orbital placeholder, or a per-atom SAD basis built from the orbital basis, is not itself a fitting
basis. Non-use is traced at the dispatch and at the consumer.

**SAD atomic solver** (`psi4/src/psi4/libscf_solver/sad.cc`):
- **Fitting test.** `SAD_use_fitting` returns false for `DIRECT` (234–244).
- **Placeholder.** In the atomic loop the non-fitting branch passes a zero AO basis in the fitting argument
  (505–516).
- **Exchange builder.** Both atomic UHF solvers build `DirectJK` from the atomic orbital basis in the non-fitting
  branch and do not use that argument (705–719 and 969–983). The argument is used only in their `MemDFJK`
  branches. The second solver needs `SAD_ORBITAL_OPTIMIZER_PACKAGE OOO`. The default is `INTERNAL`
  (`psi4/src/read_options.cc` 1836–1843), and `OOO` is not declared.
- **Atomic bases.** The per-atom SAD bases are built from the orbital basis (`psi4/driver/procrouting/proc.py`
  1479–1484).

**SCF exchange builder under `SCF_TYPE DIRECT`:**
- **Initialization.** With `DF_SCF_GUESS` false, the SCF takes the plain initialization path
  (`psi4/driver/procrouting/scf_proc/scf_iterator.py` 62–80).
- **Auxiliary argument.** The JK builder receives the wavefunction's `DF_BASIS_SCF` (103–108), which the driver sets
  to the zero placeholder when no fitting is needed (`psi4/driver/procrouting/proc.py` 1468). A given auxiliary
  basis is kept, not rebuilt (`psi4/driver/p4util/python_helpers.py` 493–503).
- **Dispatch.** The C++ builder dispatches on `SCF_TYPE` (`psi4/src/psi4/libfock/jk.cc` 206–222). For `DIRECT` it
  constructs `DirectJK(primary, options)` (172–183), whose constructor takes no auxiliary basis
  (`psi4/src/psi4/libfock/DirectJK.cc` 79). The auxiliary argument is not passed on.
- **Accelerator path.** An optional BrianQC path exists only in builds compiled with it and only when
  `BRIANQC_ENABLE`, default false, is set (`psi4/src/read_options.cc` 167–170). It is not declared.

**Double-hybrid predicate:**
- **Definition.** `is_c_hybrid()` is `c_alpha_ != 0` (`psi4/src/psi4/libfunctional/superfunctional.h` 275).
- **Setting.** `c_alpha_` starts at 0 (`psi4/src/psi4/libfunctional/superfunctional.cc` 62) and is set only
  through `set_c_alpha` (390–392). `set_c_alpha` is exposed to Python at `psi4/src/export_functional.cc` 178. The
  only other assignment copies the existing value into the polarized copy that `build_polarized` makes (starting at
  115; the copy at 151). A copy carries the value it is given, so for the declared dictionary it introduces no
  nonzero value.
- **Callers.** A word-bounded search for `set_c_alpha` over all 9 821 files of the Psi4 v1.11 archive finds two
  calling routes:
  - the `c_mp2` branch of the functional builder (`psi4/driver/procrouting/dft/dft_builder.py` 370–383);
  - an option override in the functional factory, taken only when `DFT_ALPHA_C` has been changed
    (`psi4/driver/procrouting/dft/superfunctionals.py` 101–102). That option defaults to 0.0
    (`psi4/src/read_options.cc` 1854), and B2 does not declare it.
- **The declared dictionary.** It reaches the builder through the dictionary branch of the factory
  (`psi4/driver/procrouting/dft/superfunctionals.py` 66–67). It uses `xc_functionals`, and the builder rejects a
  dictionary that combines `xc_functionals` with `c_mp2` (`psi4/driver/procrouting/dft/dft_builder.py` 190–194).
  Neither route is taken under the declared settings. The predicate is therefore false, and `run_scf` builds no
  `DF_BASIS_MP2` (`psi4/driver/procrouting/proc.py` 2765–2776).
- **What the search covers.** It covers Psi4's own source. It does not cover a user script or plugin, and the
  declared input uses neither.

**Analytic gradient:**
- **Entry.** `run_scf_gradient` calls `core.scfgrad` (`psi4/driver/procrouting/proc.py` 2845–2869), which computes
  the gradient through `SCFDeriv` (`psi4/src/psi4/scfgrad/wrapper.cc` 41–50) and builds its exchange-gradient object
  (`psi4/src/psi4/scfgrad/scf_grad.cc` 226).
- **Dispatch.** The factory builds the density-fitted `DFJKGrad`, which uses `DF_BASIS_SCF`, only when `SCF_TYPE`
  contains `DF` (`psi4/src/psi4/scfgrad/jk_grad.cc` 83–84). For `DIRECT` it builds `DirectJKGrad` from the orbital
  basis alone (99–101).
- **Long-range exchange.** The long-range exchange derivatives use range-separated integrals of the same orbital
  basis (2318–2321).

**Conclusion.** Under the declared settings, the Psi4 v1.11 tagged source constructs no auxiliary or fitting basis
in these three steps and passes none to a consumer.

**Two obligations that stay open.**
- **Build provenance.** Whether the installed binary was built from the v1.11 tagged source, and with which changes.
  - Compiled code cannot be compared with source by hash.
  - SOURCES [20] records that the installed `libxc_functionals.py` differs from the tag at one entry, so the
    installed package is not byte-identical to the tag in every file.
  - An appropriate observation is static: a read of the installed package's build record, where the package
    records the source archive it was built from, that archive's digest and any patches applied. It executes
    nothing. It lies outside this repository and needs its own authorization.
- **Runtime conformance.** Whether the installed binary takes the paths traced above under the declared settings.
  The JK and JKGrad headers of a Stage 1 P2 run name the algorithm used and any auxiliary basis. They observe the
  algorithm, not the build's provenance, and a header naming the direct algorithm does not show that the binary
  corresponds to this source. That observation needs Stage 1 authorization.

The `UNVERIFIED` label of B2 §6 is retained as written. It referred to compiled code that had not been read, and what
the installed build does remains unverified.

**Disposition: `ESTABLISHED FROM VERSION-MATCHED SOURCE`**, for the behaviour defined by the Psi4 v1.11 tagged
source. Under the criterion of Section 3, every component of the answer is in that source. Build provenance and
runtime conformance are open obligations and are not settled here.

## 9. Effect on frozen definitions

- **C4.** Byte-identical. [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md) audits the clauses the findings
  touch:
  - row 10 and the paragraph that follows the tolerance table;
  - the N2 normalization qualification;
  - the N3 compiled-basis prerequisite;
  - N8 wherever it appears;
  - the revision sequence of §3.

  It records the definitional ambiguity of row 10 and sets out options for a decision under §3. No option is
  applied. N3's statement that the compiled steps are `UNVERIFIED` is a status statement in approved bytes, and
  Section 8 supersedes it for status only.
- **The C4 human approval record.** It is byte-identical and is not edited. It is the dated account of what a person
  approved on 2026-09-27. The passages below were accurate on that date, and this record does not say they were
  wrong. It supersedes them for current status only:
  - in [its §3](C4-HUMAN-APPROVAL.md#3-what-the-approval-does-and-does-not-do), the "Readiness" row of the table,
    which reads "C3 readiness and N8 remain BLOCKED, and the five source definitions of Section 4 are not settled";
  - in [its §4](C4-HUMAN-APPROVAL.md#4-limits-that-stand), the bullet headed "C3 readiness, N8 and scope option A",
    which states that "N8 is blocked pending the record that carries the projected gradient GEO_OPT uses";
  - in the same section, the bullet headed "Five definitions still to settle from version-matched source", which
    lists all five items as still to settle.

  The current status:
  - Two of the five definitions are established from version-matched source and three are partially established.
  - CP2K 2026.2 writes no separate, direct record of that gradient. Whether a force record can serve instead is a
    definitional question (Section 7).
  - N8 remains BLOCKED.
- **B2.** B2 receives dated source annotations only. Every declared choice, value and label is unchanged. The
  declaration of the dftd4 source that Section 4 names as G4's next step would be a change to B2 through the revision
  sequence. It is not made here.
- **Gates.** No gate or dependency moves between stages.
- **Stage 1.** BLOCKED and not authorized.

## 10. Incidental observations

These arose while tracing the five items. None changes a definition.
- **GFN0 keyword defaults.** For GFN_TYPE 0, CP2K does not read `COULOMB_INTERACTION`, `COULOMB_LR`,
  `TB3_INTERACTION` or `CHECK_ATOMIC_CHARGES`, and sets all four false (`src/cp_control_utils.F` 1777–1784). B2 §3
  lists `CHECK_ATOMIC_CHARGES T` and `COULOMB_INTERACTION T` as documented defaults. They are the documented keyword
  defaults, but the GFN0 path does not use them.
- **Kind printing with GFN0.** `SUBSYS/PRINT/KINDS/POTENTIAL` aborts with GFN_TYPE 0 (Section 4). A Stage 1 input
  must not enable that print key with GFN0.
- **Environment dependence of D4.** The D4 smooth-cutoff widths can be changed by environment variables (Section 4).
  The evidence policy's environment field (§4) therefore needs their values in a run record.
- **A cross-reference in B3.** B3 §3 refers constraint projection to "N8 (C4 §3)". N8 is defined in C4 §2, and §3 is
  the revision sequence. B3 is a frozen record; the reference is noted, not changed.

## 11. Limitations and evidence labels

- **Nature of the findings.** Every located statement reports software behaviour defined by the cited source, with
  `[LIT]` provenance and no chemistry class. Conclusions the source does not state are marked **Project inference**.
  The reading was done by a software agent. Mechanical locator assertions and independent review check it.
  Agreement between agents is not evidence.
- **Builds.** No statement here describes an installed or future build.
  - CP2K is not installed.
  - The Psi4 build of E-01 was not inspected in this task.
  - Library versions (Libint, dftd4 and libxc) are bound to builds only where Section 2 says so.
- **Formatted output.** This record establishes printed formats and digits from source. It establishes no rounding
  behaviour, no overflow threshold and no allowance r. No compiled formatting test was run.
- **Negative findings.** Each rests on the tracing or search method stated where it is made. A search does not cover
  code supplied at run time by another package, compiler defaults or settings outside the source.
- **The Psi4 archive.** It is a GitHub-generated archive, not a published asset. Its files were checked against the
  commit's tree by Git blob SHA1.
- **Labels.** No `[AGENT]`, `[SPEC]`, `[GAP]` or `UNVERIFIED` label is upgraded. Stage 1 remains BLOCKED and is not
  authorized, C3 readiness and N8 remain BLOCKED, and scope option A remains BLOCKED.
