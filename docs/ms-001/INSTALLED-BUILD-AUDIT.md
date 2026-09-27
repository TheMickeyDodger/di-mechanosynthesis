# Static audit of the installed Psi4 1.11 build: Libint2 and build provenance

Date: 2026-09-27. MS-001 scope option B, before Stage 1.

This record reports a bounded, read-only static audit of the project-local Psi4 1.11 environment in which E-01 ran,
called "the E-01 build" below. It asks two things. Which Libint2 package does that build carry? And what do its package
records establish about the source and build of Libint2 and Psi4? It relates the answer to the open item on
single-primitive basis normalization in the
[source resolution record, §6](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4).

What this audit is not:
- **Software provenance only.** It is not physical evidence, runtime conformance, method validation, parity or
  chemistry evidence.
- **Nothing executed.** Nothing from the environment was imported, loaded or executed. Files were read and hashed,
  and linkage was read only as the declarations in file headers.
- **Not about E-01's cause.** It says nothing about why E-01 stopped, and it does not exclude a contribution from disk
  capacity.
- **Not a declaration for P2.** Whether the E-01 build will be the Psi4 build that P2 uses is a prospective
  declaration, and this record does not make it.

## 1. Scope and method

- **Which environment.** It was identified from a retained private survey report of E-01's installation (SHA256
  `f3a0d09fdac5fa15c9c88e0f2870b18e67c7c6cde77afe329770149883153045`). That report gives the environment's location
  with its root elided. The root was reconstructed from the worktree root the same report names elsewhere. This is a
  reconstruction, not a newly observed path. The full path is kept privately, and no other location was read.
- **What was read.** Inside the environment, only package records (`conda-meta/`) and the exact installed files needed
  to identify Libint2 and Psi4. No directory tree was enumerated, and no symbolic link was followed out of the
  environment.
- **Fail-closed check first.** Before any other read, two identities from the retained survey were re-checked. A
  mismatch would have stopped the audit.
- **Two retrievals.** The official conda package archives named in the two installed records were retrieved from
  those records' URLs and checked against the records' digests, for static reading of their metadata only.
  Identities, times and sizes are in the [pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md).
- **Locators.** Paths below are relative to the environment root.

## 2. Identity check

| File | Observed (UTC) | Bytes | SHA256 | Result |
|---|---|---:|---|---|
| `lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so` | 2026-09-27T17:40:03Z | 37 500 848 | `0d12c8cda49e2cfe75cea563a2fe51889fa61b88c7b5234beb165b9b54805d99` | Equal to the retained survey |
| `conda-meta/psi4-1.11-py314h53d0584_1.json` | 2026-09-27T17:40:03Z | 2 759 029 | `853149d1b89fa4ca2ae2768de9a4e66220c0a93fab339f6520d51ea71fc1b4f2` | Size equal to the retained survey, which recorded no digest |

## 3. Installed package records

**Psi4.** The record gives:
- package `psi4`, version `1.11`, build `py314h53d0584_1`, build number 1;
- channel `conda-forge`, subdirectory `osx-arm64`;
- package archive `https://conda.anaconda.org/conda-forge/osx-arm64/psi4-1.11-py314h53d0584_1.conda`, SHA256
  `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10`.

Among its declared dependencies is the exact pin `libint 2.13.1 h5a0831b_0`.

**Libint2.** The record `conda-meta/libint-2.13.1-h5a0831b_0.json` was observed at 2026-09-27T17:42:42Z: 67 513 bytes,
SHA256 `7cb2b345fecc86f890da13f971ec3cd1c03ee5d6aa8907d2326adefa2d4b634b`. Its file name was taken from the Psi4
record's exact dependency pin, and its identity from the record's own fields:
- package `libint`, version `2.13.1`, build `h5a0831b_0`, build number 0;
- channel `conda-forge`, subdirectory `osx-arm64`, licence `LGPL-3.0-only`;
- declared dependencies `__osx >=11.0`, `libcxx >=19` and `llvm-openmp >=19.1.7`;
- package archive `https://conda.anaconda.org/conda-forge/osx-arm64/libint-2.13.1-h5a0831b_0.conda`, 65 620 333
  bytes, SHA256 `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f`.

The version is read from the record, not inferred from a file name or a dependency name. **Neither record carries a
source archive, a source digest, a patch list or build-host requirements.**

## 4. Installed Libint2 files against the record

The record lists a SHA256 for each installed file. Three files were read and hashed at 2026-09-27T17:43:35Z.

| File | Bytes | SHA256 | Equal to the record's digest |
|---|---:|---|---|
| `include/libint2/shell.h` | 53 810 | `e0aa1e87e7cccc05c84955c9cf496fdccee2caad92c8c3e3b7f41fedd9a99c9e` | Yes |
| `lib/cmake/libint2/libint2-config-version.cmake` | 1 862 | `66f2a118ffb88a1324ee577f4303735642b3c5ca09252467f9519b33525a8373` | Yes. Line 10 sets the package version to `2.13.1` |
| `lib/libint2.dylib` | 321 327 760 | `964aff2a18e0948684e62102389a31eb2d09b83ef60b7c4bcc62e959131aa367` | Yes |

**Linkage declarations,** read with the system `otool -L` at 2026-09-27T17:44:06Z:
- The Psi4 core library declares a dependency on `@rpath/libint2.dylib`.
- The Libint2 library declares the install name `@rpath/libint2.dylib`, with compatibility and current versions
  0.0.0.

The Mach-O version fields therefore carry no library version. Which file the dynamic loader resolves for that
dependency at run time is not established.

## 5. Package recipe and build metadata: unresolved

Both package archives were retrieved and matched the digests in the installed records. Each is a zip container whose
metadata sits in one `info-*.tar.zst` member. Those members were identified and hashed:

| Archive | Info member | Bytes | SHA256 |
|---|---|---:|---|
| `libint-2.13.1-h5a0831b_0.conda` | `info-libint-2.13.1-h5a0831b_0.tar.zst` | 41 865 | `c05ac158e20ecbd16f648badb3eb5e1dcfcbf67ff71c731c72f061e65909b3d1` |
| `psi4-1.11-py314h53d0584_1.conda` | `info-psi4-1.11-py314h53d0584_1.tar.zst` | 274 440 | `69b4a8390d9768f40222bdc7f35d4f15a1e8ca6125d3d680b6c43cae85ad8d2f` |

Their contents were **not read**. The system archive tool could not decompress the zstd member, and no other
decompressor was installed or used. So the recipe and build metadata that such a member would hold remain
unresolved: the source archive and its digest, any patches, and the host requirements at build time. This is the
exact missing record.

## 6. Dispositions

| Question | Disposition | Basis and limit |
|---|---|---|
| Libint2 package of the E-01 build | **Established by the installed package record:** libint 2.13.1, build `h5a0831b_0`, conda-forge `osx-arm64` | The record's own fields. Three installed files equal their recorded digests, and the Psi4 record pins exactly this build. Package provenance only |
| Libint2 source and build identity | **Unresolved** | The missing record is the recipe and build metadata inside `info-libint-2.13.1-h5a0831b_0.tar.zst` (Section 5) |
| Psi4 package identity | **Established by the installed package record:** psi4 1.11, build `py314h53d0584_1`, conda-forge `osx-arm64`, archive SHA256 `92d4aeb7…da10` | Package provenance only |
| Psi4 source, patches and build requirements | **Unresolved** | The missing record is the recipe and build metadata inside `info-psi4-1.11-py314h53d0584_1.tar.zst`. The build-provenance obligation of the [source resolution, §8](SOURCE-RESOLUTION.md#8-psi4-compiled-steps-and-fitting-bases) therefore stays open |
| Whether the Psi4 core was compiled against these Libint2 headers | **Not established** | A dependency pin is a run-time requirement in package metadata, not a record of compilation. The build requirements would be in the unread recipe |
| Which Libint2 file is loaded at run time | **Not established** | Only static declarations were read (Section 4) |

## 7. Relation to the normalization item

The [source resolution record, §6](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4) left one part open:
"the Libint2 version linked by the Psi4 build that P2 uses, and `Shell::renorm` at that version". It had read
`shell.h` only at Libint v2.8.1, the version Psi4 v1.11 names as its source pin and minimum.

**What the installed header states.** The installed header is Libint 2.13.1, SHA256 `e0aa1e87…9c9e`. It is cited,
not copied. It defines the same behaviour that was read at v2.8.1:
- the `Shell` constructor embeds normalization by default and then calls `renorm()` (lines 764–777);
- the static flag `do_enforce_unit_normalization()` defaults to true (891–902);
- `renorm()` multiplies each primitive's normalization factor into its coefficient. While the flag holds, it then
  scales the contraction to unit self-overlap (955–999).

*Project inference* from those lines: a single-primitive shell with a positive coefficient is scaled to the
normalized primitive, as the source resolution found at v2.8.1.

**What this closes, and what it does not.**
- **Closed, for the E-01 build.** The installed Libint2 version is 2.13.1, by package record, and the installed
  header defines the normalization above. **The Libint v2.8.1 pin in Psi4's source does not describe this build**;
  the build carries 2.13.1.
- **Open: compilation.** The normalization code is defined inline in the header, so it is compiled into the program
  that includes it. Whether the Psi4 core was compiled against these header bytes is not established (Section 6).
- **Open: run-time flag changes.** Whether any code loaded at run time changes the normalization flag is not
  established.
- **Open: P2's build.** Whether P2 will use the E-01 build is a declaration not made here.

**Disposition of the normalization item: still `PARTIALLY ESTABLISHED`, narrowed.** For the E-01 build, the package
version and the header-defined normalization are established from the installed package record and header text. The
remaining parts are:
- the Libint2 headers used when the Psi4 core was compiled, which is the missing recipe record of Section 5 and, beyond
  it, binary provenance;
- the declaration of the Psi4 build that P2 uses.

N2's qualification "subject to the normalization item in B2 §6" still applies.

## 8. Limits

- Every statement is a static observation of files, package metadata or linkage declarations, or a reading of
  installed header text. None concerns a run.
- The environment's path is a reconstruction from a retained report, and it is kept privately.
- Absence statements cover only the records named. No directory of the environment was enumerated.
- Stage 1 remains BLOCKED and is not authorized. This audit authorizes nothing.
