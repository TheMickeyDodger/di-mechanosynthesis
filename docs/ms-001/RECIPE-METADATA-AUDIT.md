# Installed Psi4 and Libint recipe metadata audit

Date: 2026-09-28. MS-001 scope option B, before Stage 1.

The exact retained conda archives now yield their recipe metadata. The unread-metadata gap of the
[installed-build audit §5](INSTALLED-BUILD-AUDIT.md#5-package-recipe-and-build-metadata-unresolved) is closed.
Psi4's rendered recipe declares `libint 2.13.1 h5a0831b_0` in **both host and run requirements**. Source URLs,
declared source digests, recipe patches and build settings are now identifiable. Actual compiler inputs, binary
provenance and runtime conformance remain unestablished. Basis normalization stays **PARTIALLY ESTABLISHED**.

**Evidence convention.** Statements about upstream package metadata below are `[LIT]` software provenance,
with no chemistry evidence class. Observations of hashes and validation are local software-provenance records.
Interpretations and recommendations are explicitly `[AGENT]`; missing evidence is `[GAP]`. Every member locator
is relative to the named archive's metadata tar. The [companion ledger](RECIPE-METADATA-SOURCE-LEDGER.md) binds
all inspected regular members, the private evidence and the exact archive URLs. No evidence label in an approved
definition changes.

## 1. Scope, identity and safe reading

Only the previously retained archives were used. Their sizes, SHA256 and MD5 match the earlier retrieval manifest
and the digests recorded from the installed-package records. The original retrieval times remain 2026-09-27;
the new local observations are dated separately in the companion ledger. No replacement was retrieved.

| Package | Archive SHA256 | Exact metadata member | Member SHA256 |
|---|---|---|---|
| `libint-2.13.1-h5a0831b_0` | `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f` | `info-libint-2.13.1-h5a0831b_0.tar.zst` | `c05ac158e20ecbd16f648badb3eb5e1dcfcbf67ff71c731c72f061e65909b3d1` |
| `psi4-1.11-py314h53d0584_1` | `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10` | `info-psi4-1.11-py314h53d0584_1.tar.zst` | `69b4a8390d9768f40222bdc7f35d4f15a1e8ca6125d3d680b6c43cae85ad8d2f` |

The existing Zstandard CLI 1.5.7 decoded the members. Its executable identity and pre-existing installation receipt
are recorded privately; nothing was installed. The prior failed system-archive-tool attempt is retained as a
historical failure. The availability of a different existing tool does not turn that attempt into a success.

The ZIP reader admitted exactly `metadata.json`, the expected info member and the expected payload member.
The payload member was listed but never opened or decompressed. Whole-container hashing necessarily covers its
compressed bytes. Metadata was read into a new private extraction area; no archived script was executed.

Bounds were 16 MiB per compressed info member, 64 MiB decoded tar, 32 MiB per regular file, 20,000 members,
64 KiB per PAX header, the decoder's 128 MB memory-window setting and a 60-second decoder timeout. Outer JSON
was capped at 64 KiB; the supplementary strict JSON parser uses a 16 MiB default input limit and depth 64.
Raw tar/PAX checks precede the archive library's interpretation. They reject malformed numeric fields, nonfinite
timestamps, duplicate PAX keys and conflicting records. The hostile PAX cases were synthetic test fixtures;
the actual archives contain only single `mtime` PAX records, with no `path`, `size` or duplicate keys.
Paths, exact/case/Unicode collisions, file/directory conflicts, unsupported types, truncation, trailing nonzero
data and limit violations fail closed. The original reader would record safe links without creating them and
reject escaping links; the final raw validator rejects all link types. Neither actual metadata tar contains a link.

Libint yielded 24 regular files in 235,520 decoded bytes; Psi4 yielded 23 in 1,853,440 bytes. All 47 extracted-file
hashes were checked. Fourteen metadata JSON records passed strict parsing and the applicable field/type checks.
YAML and Jinja templates were read as text with line locators, not executed or represented as a fully evaluated
recipe. The retained installed Libint record and the retained package-field extracts were also strictly checked.
The full raw installed Psi4 record was not retained in the earlier work; its prior file digest and retained field
extract remain distinct evidence objects. This audit does not claim a fresh read of that full installed record.

An independent read-only check revalidated the 47 files and 14 metadata JSON records and reran 82 parser tests
that require no filesystem writes. The recorded full suite has 121 passing tests, including decoder bounds;
79 mutation checks retain diagnostics and distinguish failures in the tested functions from unrelated harness
errors. These checks concern this bounded parsing profile, not arbitrary archives or scientific software behavior.

## 2. Source identity and patches

| Item | What the retained text declares | Locator and limitation |
|---|---|---|
| Psi4 source | `https://github.com/psi4/psi4/archive/v1.11.tar.gz`; SHA256 `b6b5a4d397ba551d7f3516e5dc0da64bcc5778e3dca7898504293792d1b02bac` | Psi4 `info/recipe/meta.yaml` 6–13. This is a tag URL and declared archive digest, not a verified source archive in this audit |
| Psi4 patch | `0001-rename-th-fl-for-libxc-7.1.patch`, SHA256 `660a47f03811fc89cc175212140658533157d10b6e375e98811cb747eb696e06` | Recipe 12–13; patch 7–21. One Python functional-table entry changes the TH-FL identifier from `GGA_XC_TH_FL` to `LDA_XC_TH_FL`. The patch text touches no compiled routine traced in the source resolution. Application to the actual build is not observed |
| Libint source | `https://github.com/loriab/libint/releases/download/v0.1/libint-2.13.1-7-6-3-7-7-4_mm10f12ob2_0.tgz`; SHA256 `324b578f795d1f406f37a1d936f04ea51a85eae1b2ea37b5cf773afb4e25ab14` | Libint `info/recipe/meta.yaml` 4–9. Declared generated-source archive; not retrieved or independently verified here |
| Libint lineage | Parent recipe calls the tarballs generated library source with configurations different from upstream release artifacts. Its notes name tag `v2.13.1` for the selected “bells” archive and list generator options | Libint `info/recipe/parent/meta.yaml` 9–11, 31–44; `parent/NOTES` 110–126. This is a recorded generation claim, not a verified generator revision or execution record |
| Libint patches | No source-patch stanza in the rendered recipe and no patch file in the 24-member inventory | Libint rendered recipe 7–10 and complete ledger inventory. This bounded absence does not prove that the generated archive or binary has no changes; the notes also discuss historical source changes |
| Feedstock revisions | Psi4 `eedc9c313751c25cee58136474afd7b12fb85ef7`; Libint `f7d3fc73f3a766933c247ea1fed7e7c5fe1a7b45` | Respective `info/about.json`, `extra.remote_url` and `extra.sha`; rendered recipes 300–301 and 129–130. These identify declared feedstock revisions, not upstream engine commits. Both `info/git` members are empty |

The [source resolution §2](SOURCE-RESOLUTION.md#2-method-and-source-identity) previously resolved Psi4's `v1.11`
tag to `f16f4ea2ff2351cc2ab877d9b3887fcf81c2a670` and read a commit-addressed archive with digest
`040e843efd4e70d286d8705e501bd2be5c7f1f855ec439eb8a27e6565af50266`. The recipe declares a different URL and digest.
**[AGENT] interpretation:** unequal archive digests alone neither establish unequal source trees nor prove their
equality. No comparison of those two source archives was made. The recipe's `PSI4_PRETEND_VERSIONLONG=1.11+zzzzzzz`
(rendered recipe 16–17; template 1–9, 28) is a version placeholder, not an upstream commit identifier.

## 3. Build, host and variant records

The complete resolved lists are located in the hashed rendered recipes: Psi4 build 23–74, host 75–164 and run
165–198; Libint build 16–68, host 69–73 and run 74–77. The following are the directly relevant entries.

| Aspect | Psi4 | Libint | Limit |
|---|---|---|---|
| Package tuple | 1.11, build `py314h53d0584_1`, number 1 | 2.13.1, build `h5a0831b_0`, number 0 | `info/index.json` keys `name`, `version`, `build`, `build_number`, `subdir`; both `osx-arm64`. Package identity, not binary execution |
| Recipe writer | conda-build 26.7.0 | conda-build 26.1.0 | Rendered recipe line 1; metadata claim |
| Build tools | Clang/Clang++ 19.1.7, CMake 4.4.2, Ninja 1.13.2 | Clang/Clang++ 19.1.7, CMake 4.2.3, Ninja 1.13.2 | Rendered build lists above; not compiler invocation logs |
| Relevant host entries | Exact Libint 2.13.1 `h5a0831b_0`; Libxc-C 7.1.2 `cpu_h337c2d1_1`; Python 3.14.6; Eigen 5.0.1; Boost headers 1.88.0; LLVM OpenMP 19.1.7; gau2grid 2.0.9; libecpint 1.0.7; OpenOrbitalOptimizer 0.3.0 | Eigen 3.4.0; Boost headers 1.88.0; libcxx 21.1.8; LLVM OpenMP 19.1.7 | Psi4 host 85–150; Libint host 69–73. Host declarations, not proof of consumed headers/libraries |
| Target and variants | Target `osx-arm64`; Python `3.14.* *_cp314`, pybind11 ABI 11, NumPy 2, Clang/Clang++ 19 | Build platform `osx-64`, target `osx-arm64`, Clang/Clang++ 19, gfortran 14 in variant configuration | Respective `info/hash_input.json`; `info/recipe/conda_build_config.yaml` 1–48 and 1–45. Variant keys are not proof every setting affected an output |
| Exact Libint dependency | `requirements.host` line 115 **and** `requirements.run` line 178; template host 111 and exact run pin 141 | Not applicable | It is a declared host dependency as well as a runtime pin; it is absent from Psi4's separate `requirements.build` list. Actual compilation remains `[GAP]` |

**Differences and tensions retained.** Psi4's template 79 says native ARM runners became available and the recipe
switched to them, while `build.sh` 132–134 still comments that tests do not run for “this cross-compile”. Psi4's
hash-input record does not contain `build_platform`; Libint's explicitly says `osx-64`. These support a distinction
between the recorded build arrangements; neither a comment nor a variant proves actual build execution or tests.

Libint's parent recipe 46–66 requests Fortran for Unix and its variant configuration names gfortran 14. The
rendered **libint output** has no Fortran compiler in its own build requirements. Its parent is a split-output
recipe (68 onward). These are different metadata levels; the absence in one output's list does not establish
that the parent build omitted Fortran. Both packages' variant records name SDK/deployment version 11.0 while
their resolved build lists include an SDK-root environment package version 26.0. The active SDK and effective
configure arguments are not recovered from these fields alone.

## 4. What the build scripts request

Psi4 `info/recipe/build.sh` 58–99 requests a Release build, external Libint2 discovery, `MAX_AM_ERI=5`, OpenMP,
and several external dependencies. It sets `psi4_SKIP_ENABLE_Fortran=ON`, enables DKH, ECPInt, PCMSolver,
and GauXC, and disables XHOST and GENERIC. Lines 20–26 assign the Einsums and OpenOrbitalOptimizer variables
consumed by lines 58–99: both are ON for `osx-arm64`; `linux-aarch64` instead sets Einsums OFF while keeping
OpenOrbitalOptimizer ON. Lines
40–44 select BLAS/LAPACK library paths for `osx-arm64`; 110 requests build/install. Lines 112–130 edit installed
CMake configuration files. Environment variables such as `CMAKE_ARGS`, compiler flags and prefixes are inputs
to these commands; their effective values and successful execution are not recorded here.

Libint `info/recipe/parent/build.sh` 13–35 requests Release, a shared library, OpenMP compiler flags,
`LIBINT2_REQUIRE_CXX_API=ON`, `LIBINT2_REQUIRE_CXX_API_COMPILED=OFF`, Python disabled and Fortran selected
through an environment variable, then build/install. The comments at 37–43 name default generator ordering
settings; the selected generation options are recorded separately in `parent/NOTES` 110–126. No generated source
or configure/build log was examined. In particular, the C++ API option is not proof about which inline header
bytes Psi4 consumed.

Recipe test sections and retained `info/test/` files are instructions, not results. No listed package test was
run here. No configure trace, compiler command, dependency file, loaded-file record or successful chemistry
result is supplied by this audit.

## 5. Dispositions and prospective P2 decision

| Question | Disposition | What remains |
|---|---|---|
| Reading the exact metadata members | **Established; unread-recipe gap closed** | Archive/member/file identities and declared contents only; earlier failure retained |
| Source locators, declared digests, recipe patch and requirement identities | **Established as metadata declarations** | Declared upstream archives were not fetched; upstream tree identity, generator execution and actual patch application remain `[GAP]` |
| Exact Libint package as a Psi4 build dependency | **Established as a host requirement, as well as a run pin** | Not in the separate build-tool list; no actual header-consumption or linkage proof |
| Single-primitive basis normalization | **PARTIALLY ESTABLISHED, narrowed; not closed** | The prior installed header defines normalization; its digest agrees with the Libint package path record. The exact declared host package is now known. Actual compiler header inputs and the P2 build declaration remain open; runtime flag changes are not excluded |
| Compiled Psi4 fitting-basis steps | **Tagged-source conclusion retained; installed-build provenance narrowed, not closed** | Recipe source and patch declarations do not prove correspondence of the installed binary to the previously traced source. Runtime conformance remains a Stage 1 dependency, including P2 JK/JKGrad observations |
| Can a separate prospective P2 build-declaration package be prepared? | **Yes, as an `[AGENT]` recommendation for a separate human decision** | It can name the exact E-01 package candidate and its evidence/gaps. No P2 declaration is made, drafted for approval or approved here; preparation or approval does not discharge the remaining prerequisites or authorize a run |

The normalization comparison uses the earlier header observation, not a new header read:
`include/libint2/shell.h`, SHA256 `e0aa1e87e7cccc05c84955c9cf496fdccee2caad92c8c3e3b7f41fedd9a99c9e`,
and its normalization locators in [installed-build audit §7](INSTALLED-BUILD-AUDIT.md#7-relation-to-the-normalization-item).
Libint `info/paths.json`, `paths[]` entry for that path, records the same digest. That agreement is package
provenance, not a compiler observation. N2's normalization qualification still applies.

## 6. Integration and limits

This is an additive documentary update. It supplements the approved, unchanged source resolution and pre-Stage-1
source ledger; their exact adopted bytes remain in place. The installed-build audit and closure packet retain
their historical text with dated pointers to this audit. Current navigation, research state and manifest are
updated. No frozen method or protocol definition changes.

The public record is a paraphrase and digest inventory of privately retained metadata; upstream recipe text,
build-host paths, personal details and private storage locations are omitted. Commands, tool identities,
observed timestamps, all failures and machine-readable inventories remain privately retained, identified in the
companion ledger. A permissive first JSON parse, the raw-PAX defect, a timestamp-validator false positive and
weak/withdrawn mutation-test runs are preserved; the corrected supplementary run is the validation basis.

Option B remains at closed Stage 0 definitions. C4-j and B3-b remain deferred; W1 remains unrun and outside this
audit. Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized. C3 readiness and option A remain BLOCKED;
MS-000 is a feasibility PASS only. No installation, network access, source retrieval, package build, engine
import/execution or calculation occurred. E-01 remains closed as technically blocked and scientifically
indeterminate; this audit establishes no cause, readiness, parity, functional equivalence or physical validity.
