# MS-001 pre-Stage-1 source ledger

This ledger records every external byte newly inspected for the
[pre-Stage-1 closure packet](PRESTAGE1-CLOSURE-PACKET.md) of 2026-09-27. For each item it gives:
- the source identity;
- the retrieval or local-observation time in UTC;
- the byte count and SHA256;
- the exact locators cited;
- a stated limitation.

It supplements the [Stage 0 source ledger](SOURCE-LEDGER.md), which is a frozen record and is not changed.

**Conventions.**
- **Private bytes.** Retrieved and observed bytes are retained privately. Third-party documentation, source and
  package contents are cited and hashed here, never copied.
- **Sanitized locations.** Local paths are not published. Installed files are located relative to the root of the
  E-01 environment, and archive members relative to the archive's top directory.
- **Identity kinds.** Content hashes (SHA256) are kept apart from Git blob identifiers (SHA1 of the Git blob
  encoding), which are used to compare files with trees and patch pre-images.
- **What the entries establish.** Every entry establishes the identity of bytes and what their text states. None
  establishes the behaviour of a build or a run.

## 1. Retrievals

All four were made on 2026-09-27, each once, with HTTPS only and no retry under another name. Each returned HTTP 200
with curl exit 0, and each matched its expected SHA256; the expected MD5 also matched where one was recorded. The
private retrieval manifest has SHA256 `556692211f3e144b0c45ce93b2017874ea8267d9ca3cf72861f7a9f95b793983`.

| ID | URL | Accessed (UTC) | Bytes | SHA256 | Expected digest taken from |
|---|---|---|---:|---|---|
| `PS-conda-libint-2.13.1-h5a0831b_0` | <https://conda.anaconda.org/conda-forge/osx-arm64/libint-2.13.1-h5a0831b_0.conda> | 2026-09-27T17:54:40Z | 65 620 333 | `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f` | The installed record `conda-meta/libint-2.13.1-h5a0831b_0.json`, keys `sha256` and `md5` (MD5 `4bb40f31053b7c84626a6fcbe53a2cb4`) |
| `PS-conda-psi4-1.11-py314h53d0584_1` | <https://conda.anaconda.org/conda-forge/osx-arm64/psi4-1.11-py314h53d0584_1.conda> | 2026-09-27T17:54:41Z | 28 516 421 | `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10` | The installed record `conda-meta/psi4-1.11-py314h53d0584_1.json`, keys `sha256` and `md5` (MD5 `d2f223a4e61700800390b2fc95ed722b`), as extracted into a private evidence record. The full raw Psi4 record is not retained; the record file is bound by its SHA256 in Section 2 |
| `PS-cp2kdl-dftd4-4.2.0` | <https://www.cp2k.org/static/downloads/dftd4-4.2.0.tar.xz> | 2026-09-27T17:54:42Z | 1 036 728 | `467e024071510ad82b862c66c383c2ebc164fc1140e15dfc79f48d2f999fd184` | CP2K 2026.2 `tools/toolchain/scripts/stage8/install_dftd4.sh`, lines 9–10 |
| `PS-cp2kdl-tblite-0.6.0` | <https://www.cp2k.org/static/downloads/tblite-0.6.0.tar.xz> | 2026-09-27T17:54:43Z | 2 037 684 | `372281aedb89234168d00eb691addb303197a9462a9c55d145c835f2cf5e8b42` | CP2K 2026.2 `tools/toolchain/scripts/stage8/install_tblite.sh`, lines 9–10 |

**Basis for each retrieval.** This is recorded retrospectively: the retrieval script that was executed did not
write a basis file.
- **The two conda archives.** They were needed for their static recipe metadata, because the installed records carry
  no source or recipe field. They were not retained in the repository.
- **The two CP2K download-site archives.** They were needed to compare the two dftd4 routes. The source resolution
  had not examined them.

**Not observed.** Free space before and after the retrievals was planned but not observed.

**Limits.**
- The conda archives' origin is the conda-forge channel. How those packages were built is not established.
- The download-site archives are the bytes that the CP2K toolchain pins. Their correspondence to an upstream release
  asset of dftd4 or tblite was not examined.

## 2. Installed files observed in the E-01 environment

These are static local observations of 2026-09-27, made by read and hash only. The environment's location is a
reconstruction from a retained survey report (SHA256
`f3a0d09fdac5fa15c9c88e0f2870b18e67c7c6cde77afe329770149883153045`) and is kept privately.

| File (relative to the environment root) | Observed (UTC) | Bytes | SHA256 | Locator and use |
|---|---|---:|---|---|
| `lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so` | 17:40:03Z | 37 500 848 | `0d12c8cda49e2cfe75cea563a2fe51889fa61b88c7b5234beb165b9b54805d99` | Identity check against the retained survey |
| `conda-meta/psi4-1.11-py314h53d0584_1.json` | 17:40:03Z | 2 759 029 | `853149d1b89fa4ca2ae2768de9a4e66220c0a93fab339f6520d51ea71fc1b4f2` | Keys `name`, `version`, `build`, `build_number`, `channel`, `subdir`, `url`, `sha256`, `md5`, `depends` |
| `conda-meta/libint-2.13.1-h5a0831b_0.json` | 17:42:42Z | 67 513 | `7cb2b345fecc86f890da13f971ec3cd1c03ee5d6aa8907d2326adefa2d4b634b` | The same keys, plus `license`, `size` and the per-file `paths_data` digests |
| `include/libint2/shell.h` | 17:43:35Z | 53 810 | `e0aa1e87e7cccc05c84955c9cf496fdccee2caad92c8c3e3b7f41fedd9a99c9e` | Lines 764–777 (constructor), 891–902 (unit-normalization flag), 955–999 (`renorm`). Git blob `48d94583f1743753708fc46311a5451c792709c0`. Equal to the record's digest |
| `lib/cmake/libint2/libint2-config-version.cmake` | 17:43:35Z | 1 862 | `66f2a118ffb88a1324ee577f4303735642b3c5ca09252467f9519b33525a8373` | Line 10 (package version). Equal to the record's digest |
| `lib/libint2.dylib` | 17:43:35Z | 321 327 760 | `964aff2a18e0948684e62102389a31eb2d09b83ef60b7c4bcc62e959131aa367` | Equal to the record's digest |

**Linkage declarations.** These were read with the system `otool -L` at 17:44:06Z, from the core library and from
`lib/libint2.dylib`. The captured outputs have SHA256
`d010cb786972cd252da8e1f453357a1ec264a59187555ad332efa4972fcdb941` (core) and
`5679d872d91a2bad26ab6e8ba1416b05938cc897954d800177d1c6b454b5ba40` (Libint2).

**Limits.**
- These are static observations of files and declarations only. Nothing was loaded or executed.
- Runtime linkage is not established.

## 3. Archive members identified but not read

| Archive | Member | Bytes | SHA256 | Status |
|---|---|---:|---|---|
| `PS-conda-libint-2.13.1-h5a0831b_0` | `info-libint-2.13.1-h5a0831b_0.tar.zst` | 41 865 | `c05ac158e20ecbd16f648badb3eb5e1dcfcbf67ff71c731c72f061e65909b3d1` | Not read: the system archive tool lacks zstd support, and no decompressor was installed |
| `PS-conda-psi4-1.11-py314h53d0584_1` | `info-psi4-1.11-py314h53d0584_1.tar.zst` | 274 440 | `69b4a8390d9768f40222bdc7f35d4f15a1e8ca6125d3d680b6c43cae85ad8d2f` | Not read, as above |

The package payload members were neither extracted nor read.

## 4. Files read inside retained or retrieved archives

Every file was read as text; no build was configured. The digests were computed on 2026-09-27 by a read-only script.
Its private digest table has SHA256 `951aa0d01947d7eb3511f404c4d413c33948700ed346e67c2b2c78c259d3aad1`. A separate private verification record of 2026-09-27T18:12:48Z asserts
that all 54 rows of that table matched a recomputation. That record does not contain the digests it compared, so it
is an asserted check, not a re-verifiable binding, and this ledger does not rely on it. The final verification of
this packet recomputes every row below from the retained bytes.

**CP2K 2026.2 release archive** (`SR-cp2k-2026.2-release-tarball` of the [Stage 0 ledger](SOURCE-LEDGER.md#source-resolution-retrievals-2026-09-27),
SHA256 `f9bd86f5…3373`). The source resolution established that every regular file of this archive equals the
blob of the release revision `67b5da87…`.

| File | Bytes | SHA256 | Git blob SHA1 | Lines cited |
|---|---:|---|---|---|
| `CMakeLists.txt` | 47 269 | `147aaf86596e26e39ce857b62b357f241b59b894b02c5f2dc47476ba58c860b5` | `075f91973c0813684ee791ecba2a95967b4a464d` | 886–889, 911–918 |
| `src/qs_dispersion_d4.F` | 60 370 | `3699c01defd8dd4c13cb57542a04eda0c832a2276af2e5d75e31115de4038097` | `dcf321e4f0bf84151f25431ba353cf3b4fba3d1d` | 231–242, 297–300, 315–347, 348–620, 378, 381, 398–416, 429, 441–444, 504, 645–761 |
| `src/qs_dispersion_types.F` | 11 459 | `6f4ef085eefa5208a15d2ebca592825392d3497b4a23192182d7602c02d5d10c` | `ef623cb95ab34ad2a5713dba54f4dd5285c122a4` | 61–62 |
| `src/qs_environment.F` | 132 266 | `51acf59832239e5610dcb8b3c7117d1311f42d5eb5beb39400591b724ed5e777` | `bf7ae4766d93830f69d35594c8d863224cd55a43` | 1904–1951 |
| `src/cp_control_utils.F` | 194 866 | `da04a34bb800c6ccc9314a9e434abca7b0f1482a250f1672bb0cd27adff6aa39` | `3a2478e19e0bc67c8fad09fd00736d0b3ef3f960` | 1561–1571, 1606–1632 |
| `src/input_cp2k_xc.F` | 112 577 | `332cda33e1d90c5e3002fcc1e965633d009f28caadbc98c188474cd26e314e3b` | `7f93bfe65760fd46fea2e3f1824243dc2043db8b` | 1011–1024 |
| `src/force_env_methods.F` | 123 339 | `82b08e7e477c1fe2f1f0ce82b80202dd93863b0b3ab420fa9ba5fe1f35851ada` | `28cbe7e2acafffa9ff01df4dc0c5380bd19a0c1f` | 260, 361–369, 410–442 (411–413, 439) |
| `src/force_env_utils.F` | 30 729 | `67279322d29605b85e5f7c39210b004d58ccfe8a9144a5ba8690a232d6f2fdc5` | `699045290f6f972f8eb8e7c8ffdf5eca27a20d9e` | 482–490, 503–506, 509–513, 574–582, 590–606 |
| `src/constraint_fxd.F` | 23 753 | `99e1a032cb2b64cfbc77eda42aba30dbfc38b6b97cd269eae4d5c8cb3745ead1` | `225416d12d4b3b36253f115916d32409d5a43837` | 130–147, 221–225, 232–242 |
| `src/particle_methods.F` | 70 633 | `eba3978a2a8336b48dbeea33efc3f08e79da51b40ddc6f305ca83fc404b10389` | `e7336c66ad4f47a4c353dd85b989bfbd19450372` | 269–295 |
| `src/motion_utils.F` | 33 002 | `478a5431bcb3f6ccc6af02f7d8ec6312ed618d1128317b08117bb81a29731001` | `d83916a8e33606be6ca2b286b667cfaa86a9db84` | 380–382, 419–423 |
| `src/input_cp2k_force_eval.F` | 23 053 | `966515458634db9fb5355423781bc69e28ffa4bb65689c10b7ccef7e06413c0f` | `cea88f47605a5c9bc49646e0127bc427f0320b7e` | 322–335 |
| `src/input_cp2k_motion_print.F` | 24 795 | `33b63bf95fe3062f1865d3c6cb9ef54b174a8effe7dd196b897fcbe3ccb2b138` | `f37d1b4c39cd7399d187376b15297fc8e86d2bd0` | 73–75, 319–323 |
| `src/input/cp_output_handling.F` | 59 048 | `b834ae06db0e41a5a78384b553bac91776e8def275bd7bc7d4f9428364e2e01d` | `8abac352bf11c9c35ab10e908b6cf195b465fcf8` | 221, 262, 292–294, 766–772 |
| `src/motion/gopt_f_methods.F` | 54 117 | `af0a983bd5d43b4843f7394e90ef001e0bbcd0800703ff47798456404cbdc8b2` | `65682a68caa69a6eb002f6ebfa6828b5c5a9d6bd` | 176–250, 321–336, 482–486, 769–774, 894–905 (899–900, 902–903, 904), 920–941, 1048–1088 |
| `src/motion/gopt_f77_methods.F` | 13 238 | `aed5caa7ad3d134df229ffd0a2d472de67aa49c12ec3fab8e3e0b0a0d026b972` | `8d5b6727fd4db34b5eaab2fa8a13215cdb017345` | 131–135 |
| `src/motion/bfgs_optimizer.F` | 52 153 | `10f3c8588f863d672ef8757babc949591b65e37c3f8616e15d2b59532d039dea` | `ef6ae345ea076f404cb3df84b09568f690e0c3c8` | 290, 304, 409–410, 427–428 |
| `tools/toolchain/install_cp2k_toolchain.sh` | 62 500 | `ea853395f73ddb4cff11bd8ef4cae85bf64627f7d9fb2847412f5a0e4897ddde` | `1459a6ec7b9b23f33a3583f4927a413c4e2916e3` | 527–528, 1157–1164 |
| `tools/toolchain/scripts/tool_kit.sh` | 23 187 | `997e30310169ea6f565a1cfe7707655763fc66104e9e5b1bf20920afeb807868` | `359faad536a5f7f892df91d3410680a4dc8244a1` | 669–691 |
| `tools/toolchain/scripts/stage8/install_dftd4.sh` | 2 782 | `d58c9d5b642fe424798c4b2ac0bbc80d7e6d8b3b179f5111e711e99f741950b6` | `1bed51b389f63136b7fc395632a7c0025f68a8c6` | 9–10, 33–48 |
| `tools/toolchain/scripts/stage8/install_tblite.sh` | 3 522 | `b36e31c9c83d679ee45e7b09573575c739291f4ba3e2ecaf579ea939d0396a03` | `9c9654af8fe8e0d785aa9f08109cc223105ca2c6` | 9–12, 35–57 |
| `tools/toolchain/scripts/stage8/dftd4-4.2.0-gradient-fixes.patch` | 24 723 | `5335cb7d02a8c3141f28967ef61418f425fb1e638d51fe75618b700321d9087a` | `e467cf852e1d1d824bd770f5226d45ab3d38e2a2` | 1–574 (hunk headers; pre-image identifiers on lines 2, 71, 234, 469) |
| `tools/toolchain/scripts/stage8/simple-dftd3-1.4.0-gradient-fixes.patch` | 50 886 | `6a20b4622821018954a204a33dcb2128ddfaec04a37f3b4a625a71058ba2a40b` | `05fa3542f923ee7919dbb2f09dcbe5c2b0d7f188` | Pre-image identifiers of its eight files |

**dftd4 4.2.0** (`PS-cp2kdl-dftd4-4.2.0`; paths below the top directory `dftd4-4.2.0/`).

| File | Bytes | SHA256 | Git blob SHA1 | Lines cited |
|---|---:|---|---|---|
| `CMakeLists.txt` | 3 838 | `bfcbaf91758f60cddc40b2ba8537f0893151d4081ad2ced68e6d17483740fc71` | `3db54423ebfe6b55c613ecf65f94ad576db85f15` | 22 |
| `meson.build` | 3 130 | `2801af8f34d4413087cbfe8c5e8d420eea042599503ac2227007c7ae748b466c` | `7de7d61f66cff66df3bab2e32393623b3e447326` | 20 |
| `fpm.toml` | 770 | `95ed0ebdaaf670ce28364674a67838c8e4f84783b7ea1ce6e80ada3b44f59c53` | `4cdb69da56658bcd76994e1f3ced889c75674365` | 2 |
| `src/dftd4/version.f90` | 2 042 | `a03de344af6da26c1dd20253ca3a4fb146fc144683323ea8f2cbc98486b883b7` | `b029e0e6e92f78a54c514672c91fd5d163de0c3c` | 27 |
| `config/cmake/dftd4-utils.cmake` | 3 700 | `7937fe3930e573b7f6c2039f18caf998f828de8592dd36eb614f99ebed595be8` | `db4336e32a62f808717110e8083d16e753255fc0` | 28–106 |
| `config/cmake/Findmulticharge.cmake` | 1 399 | `8d789959147ea6c8efad009c81568334db97685445bd5487255a6eec5132d38b` | `6e1441d8653209e89b0df491fb9459b47d58c7b2` | 17–33 |
| `src/dftd4/cutoff.f90` | 7 156 | `e9e4b2b6d0cfdb138ff304cf109e59a9549998d2b9008821b4c53a5361c01e1a` | `86a856b5e738f6c43bde5b0597f05987c9502de5` | Whole file; equals the patch pre-image `86a856b` |
| `src/dftd4/damping/atm.f90` | 17 918 | `7f7e718bfa0892bd48591258b00430e3f7327693275f757fa6e3b27947b4f252` | `c6162c97a380362a0bf4059bad7c24d7434f8d4d` | Whole file; equals the patch pre-image `c6162c9` |
| `src/dftd4/damping/rational.f90` | 21 519 | `449c052716272c1bb35ad0f41bb23b9a0df019de45c43eb308267c568724d396` | `9d359c95d2b67365b9e61ec33ad663b564e53334` | Whole file; equals the patch pre-image `9d359c9` |
| `src/dftd4/disp.f90` | 8 589 | `e83b1b3cdf1bb2caa56d4ec5b7014b02eb41f362a160dba7e3adbf82dabe2cad` | `73253cee0288803eedcea29f9704b6b9b2bbf4ce` | Whole file; equals the patch pre-image `73253ce` |
| `src/dftd4/model/d4.f90` | 17 241 | `dc421a2ccf76227ae028f45ad84efd1683505b803f926dfda24be1b5d223b220` | `33ed0ea918a81bc88a22110cc856d7988b18f956` | 69–229 (`new_d4_model`), 234–374 (`weight_references`) |

**tblite 0.6.0** (`PS-cp2kdl-tblite-0.6.0`; paths below the top directory `tblite-0.6.0/`).

| File | Bytes | SHA256 | Git blob SHA1 | Lines cited |
|---|---:|---|---|---|
| `CMakeLists.txt` | 3 925 | `81a4bb41da8a86ad8265cb06fdfe1e7501b668006122b58511281d3de902a3ad` | `f7681fe3d7b7316c60abb3b67600fab74b856f3a` | 45–63 |
| `config/template.cmake` | 984 | `e44c4c98776a10f04d2b28c133c308e0d3dd1825c2f1163f8a05776008350229` | `738b22cd192cdd7e599dd6566014a49c6973786a` | 37–39 |
| `config/cmake/Finddftd4.cmake` | 1 382 | `45105f9491b3c057b6fc1004073d3cd6cc6a7c2c9e1126323d22d1779d904451` | `0369209499fcbc1d59e2f843fd6298f05e518332` | 17–33 (method list 26; `DFTD4_FIND_METHOD` precedence 22–24; fetch URL and revision 19–20) |
| `config/cmake/tblite-utils.cmake` | 3 690 | `c8f36b08ed177ea2b15454c0bffcd9cd04ad9dc05de2c4e46211e21169f42f32` | `be656717e2e7cf9e9583b5addbf2dc4ffaa352fc` | 28–32, 38, 47, 68, 87 |
| `subprojects/dftd4/src/dftd4/version.f90` | 2 042 | `a03de344af6da26c1dd20253ca3a4fb146fc144683323ea8f2cbc98486b883b7` | `b029e0e6e92f78a54c514672c91fd5d163de0c3c` | 27; identical to the standalone file |
| `subprojects/dftd4/src/dftd4/cutoff.f90` | 7 156 | `e9e4b2b6d0cfdb138ff304cf109e59a9549998d2b9008821b4c53a5361c01e1a` | `86a856b5e738f6c43bde5b0597f05987c9502de5` | Whole file; identical to the standalone file |
| `subprojects/toml-f/meson.build` | 2 040 | `9a5067efe6d3abb29c64f2b65317809b34394a8ae5f481c875bffd3d62070b58` | `bcea3b3cb910303b0309b76076e814dda5a81aa6` | 17 (version 0.5.0) |
| `subprojects/s-dftd3/meson.build` | 3 174 | `adb78e7469a615d0daf79e78b36a9db3f4cbc2899dedae07873c013ffd946044` | `b0551898b5cc734de12c2b3f36309337a2547fdb` | 20 (version 1.4.0) |

**Whole-tree comparison.** A read-only comparison of the two unpacked trees, by SHA256 and Git blob SHA1 of every
regular file, gave these results. The private comparison report has SHA256 `7a463200f830ac702a17c347e545f4eb94e470a3a82c389a4be4173f6bb4609b`, and its
summary `05cb309d62cba3bc185da40742540eedf5a10668687de481b5d56f4354d8ac1d`.
- The tblite archive holds 166 regular files under `subprojects/dftd4`. All 166 are identical to the standalone
  files at the same paths. None differs, and none is present only in the bundled copy.
- The standalone archive has 547 further files, all under its `subprojects/`.
- Of the shared subprojects:
  - jonquil (35 files), mctc-lib (156), mstore (46), multicharge (67) and test-drive (24) are identical;
  - toml-f differs in 30 files and has 3 files present only in tblite.
- A dry-run check (`patch --dry-run -l -p1`) of CP2K's dftd4 patch succeeded on both trees, and that of its
  simple-dftd3 patch on tblite's bundled copy. Nothing was applied.

**aiida-core 2.9.2 wheel.** This is the retained wheel of the Stage 0 hash-locked installation, 1 500 351 bytes,
SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`, verified at 2026-09-27T18:00:06Z. Its
members were read without installation or import.

| Member | Bytes | SHA256 | Git blob SHA1 | Lines cited |
|---|---:|---|---|---|
| `aiida/transports/transport.py` | 83 969 | `8fbc221847c7d60d410bbc173ad89a925090047699eda36072bdbaa71d464faf` | `0ae3fd5a8af58d4cfba6fc4010d9ad27a08addce` | 114–124 |
| `aiida/transports/plugins/local.py` | 39 702 | `e34aaebbe13930d15d17eba2244091ae543b2fd692afd12a3af6d26f25cc8561` | `e5ffcd7a863fe00e32c0be2bde48a13993aa13d2` | 770–791 |
| `aiida/schedulers/plugins/direct.py` | 16 852 | `324561c821f53c42c9665dbf689b04ce41b8defb2a2a6928de8b7b7a9e25ba3a` | `36e87e548e1d178c8f8c3fa8c3d1999e268f88db` | 126–174, 192–206 |
| `aiida/schedulers/scheduler.py` | 17 479 | `27f9351d314a197e061cdec91760810f869bcee2da23006078e9b03bb3a1e2ae` | `a7bc4d96e6167271eee1a27ec18a7f5e33e24500` | 205–244 |
| `aiida/engine/processes/calcjobs/calcjob.py` | 55 833 | `7ebd9157f19d7e04144d88cf18ce631d675dcecdde0c413b7a2a909616efbe2e` | `8821149d6bb5675923ede5d751684b8364e00a34` | 211–223, 295–300, 320–324, 326–337, 398–432, 440–446, 725–745, 775–823, 903–930, 965, 972, 982–990 |
| `aiida/engine/processes/calcjobs/tasks.py` | 36 171 | `389b78414b4cd04312aa59fcd2280e70a2e2653266e73f8011f5bb12d041c6ef` | `1ec2628a51557d88ef02d38ffd166f92a021e890` | 84–111 |
| `aiida/engine/processes/process.py` | 45 586 | `b1f458b05e0546d7adddae8bf89811e3d2347671abe54624e521e88266995b80` | `add65a2852cbc5abb39d57516699fa73046e6fea` | 619–640 |

**Limits.**
- Every row establishes the identity of bytes and what their text states at the cited lines.
- No row establishes the behaviour of a build, an installation or a run.
- Project inferences drawn from these lines are marked as such in the records that make them.
