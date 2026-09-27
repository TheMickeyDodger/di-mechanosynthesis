# G4: proposed declaration of the dftd4 source

Date: 2026-09-27. MS-001 scope option B, before Stage 1. Status: **PROPOSAL under the C4 §3 revision sequence. Not
applied, not approved, and not a change of B2.**

The [source resolution record, §4](SOURCE-RESOLUTION.md#4-g4-gfn0-parameter-provenance-through-cp2k) left one piece of
G4 open. The GFN0 dispersion (D4) takes its reference data from the external dftd4 library, and the CP2K 2026.2 release
does not fix which dftd4 source a build uses. This record compares the two routes that the release's toolchain offers
and recommends one. It gives exact text that a person could approve. It builds nothing, links nothing and runs
nothing.

What this record is not:
- **Not a build or run claim.** Every statement below is about source text: archives, toolchain scripts, build files
  and CP2K source. None of it says what any build contains, links or computes, and none of it is physical evidence.
- **Not a change.** B2 and every other frozen record are unchanged. The declaration takes effect only if a person
  approves it through the C4 §3 sequence.
- **Not readiness.** The loaded parameter bytes, the linked library and the environment settings of a run remain P1
  observations within Stage 1 (B2 §8). Stage 1 remains BLOCKED and is not authorized.

## 1. Sources

All bytes were retrieved on 2026-09-27 from the location the CP2K 2026.2 toolchain itself downloads from, and each
matched the SHA256 that the release's toolchain pins. Identities, retrieval times, sizes and locators are in the
[pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md). No third-party bytes are published here.

| Archive | Pinned by | Size (bytes) | SHA256 |
|---|---|---:|---|
| `dftd4-4.2.0.tar.xz` | CP2K 2026.2 `tools/toolchain/scripts/stage8/install_dftd4.sh` lines 9–10 | 1 036 728 | `467e024071510ad82b862c66c383c2ebc164fc1140e15dfc79f48d2f999fd184` |
| `tblite-0.6.0.tar.xz` | CP2K 2026.2 `tools/toolchain/scripts/stage8/install_tblite.sh` lines 9–10 | 2 037 684 | `372281aedb89234168d00eb691addb303197a9462a9c55d145c835f2cf5e8b42` |

The two CP2K patch files are read from the CP2K 2026.2 release archive:
- `dftd4-4.2.0-gradient-fixes.patch`, SHA256 `5335cb7d02a8c3141f28967ef61418f425fb1e638d51fe75618b700321d9087a`;
- `simple-dftd3-1.4.0-gradient-fixes.patch`, SHA256 `6a20b4622821018954a204a33dcb2128ddfaec04a37f3b4a625a71058ba2a40b`.

**Upstream correspondence is not established.** The toolchain downloads by file name from the CP2K download site and
checks the pinned digest (`tools/toolchain/scripts/tool_kit.sh` 669–691). Whether those bytes equal an upstream
release asset of dftd4 or tblite was not examined.

## 2. What the archives contain

Both archives were unpacked as text, with every member checked first. Each file was hashed and compared by content;
nothing was configured or built. Findings:

- **The dftd4 source in both archives is the same.** tblite 0.6.0 bundles dftd4 under `subprojects/dftd4`, 166
  regular files. All 166 are byte-identical to the files at the same paths in the standalone `dftd4-4.2.0` archive.
  None differs, and the bundled copy has no file that the standalone archive lacks. Both declare version 4.2.0
  (`src/dftd4/version.f90` line 27, `meson.build` line 20, `fpm.toml` line 2, `CMakeLists.txt` line 22).
- **The archives provision dependencies differently.** The standalone archive has 547 further files, all under its
  own `subprojects/`, vendoring jonquil, mctc-lib, mstore, multicharge, test-drive and toml-f. tblite supplies these
  from its own top-level `subprojects/`:
  - jonquil 0.3.0, mctc-lib 0.5.1, mstore 0.3.0, multicharge 0.5.0 and test-drive 0.4.0 are byte-identical in both
    archives;
  - toml-f differs: 0.4.3 in the standalone archive and 0.5.0 in tblite;
  - tblite also bundles simple-dftd3 1.4.0.

  This difference is in how the archives provision dependencies. It is not a difference in the dftd4 source.
- **Both trees are in the same unpatched state for CP2K's patch.** The patch records a pre-image Git blob for each of
  the four files it changes:
  - `src/dftd4/cutoff.f90`, `86a856b`;
  - `src/dftd4/damping/atm.f90`, `c6162c9`;
  - `src/dftd4/damping/rational.f90`, `9d359c9`;
  - `src/dftd4/disp.f90`, `73253ce`.

  In both trees each file's blob begins with its pre-image identifier. A dry-run check (`patch --dry-run -l -p1`)
  reports that the patch would apply to both trees. The simple-dftd3 patch's eight pre-images likewise match tblite's
  bundled simple-dftd3. The dry run is a static check of applicability. Nothing was applied, and it is not evidence
  about any build.

## 3. What the two routes do with the same source

The asymmetry lies in the toolchain's install scripts, not in the archives.

| | Standalone route | tblite route |
|---|---|---|
| Script | `install_dftd4.sh` | `install_tblite.sh` |
| Archive | `dftd4-4.2.0.tar.xz` (lines 9–10, 33) | `tblite-0.6.0.tar.xz` (lines 9–10, 35) |
| Patch step | None: unpack, then configure and install (lines 36–46) | `simple-dftd3-1.4.0-gradient-fixes.patch` applied to `subprojects/s-dftd3`, and `dftd4-4.2.0-gradient-fixes.patch` applied to `subprojects/dftd4`, before configuration (lines 40–43) |
| Checksums the script records | The script only (line 48) | The script and both patch files (lines 55–57) |
| Toolchain default | Not used: `with_dftd4="__DONTUSE__"` (`install_cp2k_toolchain.sh` line 527) | Used: `with_tblite="__INSTALL__"` (line 528) |
| When both are requested | A standalone dftd4 is turned off whenever tblite is used (lines 1157–1164) | — |

**The precise claim.** The same dftd4 4.2.0 source files, byte-identical in the two CP2K-hosted archives, end up
patched on the tblite route and unpatched on the standalone route. That the patch is named "gradient fixes" is not
taken as evidence of what any difference would do. No gradient, energy or other result of either route has been
produced or compared.

**What the patch changes, by reading its hunks.**
- In `cutoff.f90`: it changes the default two-body smooth-cutoff width from 0 to 0.05, and it adds a reader for
  environment variables that override the widths.
- In `disp.f90`: the high-level routines apply that override to a copy of the cutoff.
- In `damping/rational.f90` and `damping/atm.f90`: it replaces per-thread accumulation arrays and a critical section
  with OpenMP reduction clauses.

The hunks read change no dispersion formula. A full hunk-by-hunk classification is not claimed.

## 4. Which dftd4 code CP2K's GFN0 path reaches

This section reads CP2K 2026.2 release source (file SHA256 in the ledger).
- **Selection.** `GFN_TYPE 0` without `VDW_POTENTIAL` selects D4 (`src/cp_control_utils.F` 1561–1571), with s6 = 1.00,
  s8 = 2.85, a1 = 0.80 and a2 = 4.60 (1606–1632).
- **Setup.** The xTB setup allocates the dispersion environment, sets `doabc` false and the D4 fields, and sets
  `ref_functional` to `"none"` (`src/qs_environment.F` 1904–1951).
- **Defaults of the two switches.** It does not set `d4_reference_code` or `d4_debug`. Both keep their type defaults,
  `.FALSE.` (`src/qs_dispersion_types.F` 61–62). The corresponding input keywords belong to the DFT dispersion
  section, which this path does not read (`src/input_cp2k_xc.F` 1011–1024).
- **The production branch.** With both switches false, `calculate_dispersion_d4_pairpot` takes its production branch
  (`src/qs_dispersion_d4.F` 348–620):
  - coordination numbers come from CP2K's own `cnumber_init` (381);
  - charges come from the dispersion environment or from CP2K's own `eeq_charges` (398–416);
  - the two-body energy and gradient come from CP2K's own `dispersion_2b` (441–444).
  - The three-body term is skipped because `doabc` is false (504).
- **What the branch takes from dftd4.** The D4 model constructor, with its reference data, and its weighting routine
  (231–242, 378, 429), and the reference-data fields passed to `dispersion_2b`.

**Where the patch's hunks lie.** By their hunk headers (patch file lines 1–574), they are in:
- the default two-body width of the cutoff type, and new routines that read the environment overrides
  (`cutoff.f90`);
- the high-level `get_dispersion` and `get_pairwise_dispersion` (`disp.f90`);
- the energy and derivative routines of the rational and three-body damping (`damping/rational.f90` and
  `damping/atm.f90`).

**Where CP2K reaches them.**
- It calls the damping routines only through `param%get_dispersion2` and `param%get_dispersion3`, and the high-level
  routine only as `get_dispersion`. Both occur only in the reference-code branch (315–347) and in the debug routine
  (645–761).
- The model code the production branch does call is `new_d4_model` and `weight_references`, in
  `src/dftd4/model/d4.f90` (lines 69–229 and 234–374 of dftd4 4.2.0). A search of every `use` statement under `src/`
  finds no import of the four patched modules in that file.
- The production branch uses the cutoff type only as a container. Its two-body width, the value that the patch
  changes, is set explicitly by CP2K (297–300).

*Project inference.* With its defaults, the GFN0 path reaches no patched routine. Both routes give it the same dftd4
source text for everything it calls: the model, the reference data and the weighting. This is a statement about
source. It is not a statement about any build.

## 5. Dependency resolution: a gap in both routes

Neither archive alone fixes which dependency sources a build uses.
- **The resolution order.** dftd4 4.2.0 resolves each dependency by trying, in order, an installed CMake package,
  then pkg-config, then its vendored `subprojects/`, then a network fetch of a pinned tag
  (`config/cmake/dftd4-utils.cmake` 28–106; `config/cmake/Findmulticharge.cmake` 17–33). tblite 0.6.0 does the same
  for dftd4 itself (`config/cmake/Finddftd4.cmake` 17–33):
  - The method list defaults to `cmake`, `pkgconf`, `subproject`, `fetch`, in that order (line 26). The last resort
    fetches `https://github.com/dftd4/dftd4` at `v4.2.0` (lines 19–20).
  - The global switch `tblite-dependency-method` is consulted only if the package-specific variable
    `DFTD4_FIND_METHOD` is not already defined (lines 22–24). A defined `DFTD4_FIND_METHOD` takes precedence.
  - Inside the lookup, a target of the package's name that already exists ends the lookup before any method is
    tried (`config/cmake/tblite-utils.cmake` 28–32).
  - Each method prints a status message when it resolves a package:
    - `Found installed package` (line 38);
    - `Found <package> via pkg-config` (line 47);
    - `Include <package> from subprojects` (line 68);
    - `Retrieving <package> from <url>` (line 87).

    A configure log therefore records which method resolved each package.
- **What this means.** Unless it is pinned, and unless the pin is actually honoured, a build may take dftd4 or one of
  its bundled dependencies from an installed package, from pkg-config, from a target defined earlier, or from a
  network fetch. On the tblite route that would replace the patched bundled copy. It would defeat the archive and
  patch identity that a declaration fixes. That is why the resolution has to be observed, not only switched.
- **Unpinned in the toolchain.** Neither toolchain script passes a switch that fixes the method
  (`install_dftd4.sh` 40–45; `install_tblite.sh` 46–53).
- **Why the pin is not enough on its own.** tblite looks up toml-f, mctc-lib, multicharge, dftd4 and simple-dftd3
  itself, in that order, before its sources are added (`CMakeLists.txt` 45–63). When the bundled dftd4 then looks up
  its own dependencies, it reuses a target that already exists (`dftd4-utils.cmake` 30–32). A tblite-level switch
  therefore reaches all five packages. It is bypassed, however, by:
  - a defined package-specific `*_FIND_METHOD` variable;
  - a target of the same name that exists before the lookup.

  *Project inference* from the cited lines.
- **The CP2K side.** CP2K's own build links `dftd4::dftd4` through the tblite target when tblite is used
  (`CMakeLists.txt` 911–918), and tblite's installed configuration then looks for a dftd4 package
  (`config/template.cmake` 37–39).

A declaration of the dftd4 source therefore has to say how its dependencies are resolved. Otherwise the archive
identity names a source that a build might not use.

## 6. Recommendation and candidate declaration

**Recommendation (`[AGENT]`): the tblite route, with dependency resolution pinned to the bundled sources.** The
reasons:
1. **It is the release toolchain's default.** It is also the only configuration in which the release's own scripts
   apply CP2K's dftd4 patch (Section 3). CP2K's D4 source aligns its explicit smooth width with that patch
   (`src/qs_dispersion_d4.F` 297–300).
2. **Identical text in the traced source subset.** The dftd4 routines and data that the GFN0 production path was
   traced to call (Section 4) have byte-identical text on both routes (Section 2). This is text identity of a traced
   subset of source. It is not functional equivalence of the two builds. Those would be patched differently,
   configured differently and resolve different dependency trees; toml-f, for example, is 0.4.3 on one route and
   0.5.0 on the other.
3. **It makes the resolution gap a checked condition.** Both routes have the gap (Section 5). The declaration below
   requires the actual resolution to be shown, not only switched.

The recommendation is a proposal. The alternative, with its consequences, is set out below. A person may choose it,
or neither.

**Candidate declaration (exact text for an annotation of B2 §3 after approval):**

> **Declared dftd4 source for G4 (approved [human-resolved: decision date]).** The dftd4 library of the declared CP2K 2026.2 route is built from the tblite 0.6.0 source archive `tblite-0.6.0.tar.xz`, SHA256 `372281aedb89234168d00eb691addb303197a9462a9c55d145c835f2cf5e8b42`, as pinned by the CP2K 2026.2 toolchain script `tools/toolchain/scripts/stage8/install_tblite.sh`. Its bundled `subprojects/dftd4` is dftd4 4.2.0, byte-identical in all 166 files to the corresponding files of `dftd4-4.2.0.tar.xz`, SHA256 `467e024071510ad82b862c66c383c2ebc164fc1140e15dfc79f48d2f999fd184`. Patch state: the CP2K 2026.2 patch `dftd4-4.2.0-gradient-fixes.patch`, SHA256 `5335cb7d02a8c3141f28967ef61418f425fb1e638d51fe75618b700321d9087a`, is applied to `subprojects/dftd4` with `patch -l -p1`, and `simple-dftd3-1.4.0-gradient-fixes.patch`, SHA256 `6a20b4622821018954a204a33dcb2128ddfaec04a37f3b4a625a71058ba2a40b`, to `subprojects/s-dftd3`, exactly as that script does. Dependencies: the five bundled library dependencies dftd4, mctc-lib, multicharge, toml-f and simple-dftd3 are resolved from tblite's bundled `subprojects/`, and from no installed package, pkg-config module, earlier target or network fetch. The build is configured in a fresh build directory with `-Dtblite-dependency-method=subproject`. No package-specific `*_FIND_METHOD` variable is set for any of the five, unless it is set to `subproject`. No target named for any of them exists before tblite's own lookup. The fail-closed condition is the build's own record, not the switch: the retained configure output must show `Include <package> from subprojects` for each of the five, and none of `Found installed package`, `Found <package> via pkg-config` or `Retrieving <package>` for any of them. Otherwise the build does not conform to this declaration. A P1 run record must also give the digests of the four patched dftd4 files after patching and the identity of the dftd4 library that CP2K links. This declaration covers only these five bundled libraries; it does not cover toolchain, compiler, BLAS, LAPACK or OpenMP dependencies. The archive identity, the patch identity and the dependency resolution are three separate parts of this declaration.

**The alternative: the standalone route.**
- **Archive.** `dftd4-4.2.0.tar.xz`, SHA256 `467e0240…d184`, unpatched, with its vendored dependencies (toml-f 0.4.3
  where tblite has 0.5.0).
- **Configuration.** It needs non-default toolchain options, tblite off and dftd4 on. It also needs a pin,
  `-Ddftd4-dependency-method=subproject`, with the same fail-closed resolution record as the candidate declaration,
  applied to dftd4's vendored dependencies.
- **Consequences.**
  - The four files that CP2K's patch changes stay in the state in which the CP2K-hosted archive carries them, the
    patch's pre-image.
  - GFN_TYPE `TBLITE` would not be available in that build; it is not declared.
  - The dftd4 source that the GFN0 production path was traced to call has the same text as on the recommended route
    (Section 4). This is text identity of a traced subset, not equivalence of the builds.

**Neither.** G4 stays `PARTIALLY ESTABLISHED`, and its P1 dependency stays open.

## 7. Disposition

- **G4, source-definition part: `PARTIALLY ESTABLISHED`, unchanged.** This record prepares the declaration that the
  source resolution named as the next step, but it does not make it. It adds three things:
  - the finding that both CP2K-hosted archives carry byte-identical dftd4 source files;
  - the location of the asymmetry, in the install scripts;
  - the dependency-resolution gap that a declaration must close.
- **After approval.** If a person approves a declaration, the source-definition part of G4 is settled by that
  declaration. P1 identity provenance remains within Stage 1.
- **Limits.** No build, linkage or runtime claim arises from this comparison. Upstream correspondence of the CP2K
  download-site bytes, the full hunk-by-hunk content of the patch, and the behaviour of any dftd4 routine at run time
  are not established.
- **Stage 1** remains BLOCKED and is not authorized.
