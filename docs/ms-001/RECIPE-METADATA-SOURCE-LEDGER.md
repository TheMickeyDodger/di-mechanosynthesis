# Recipe metadata source ledger

Date: 2026-09-28. Companion to the [recipe metadata audit](RECIPE-METADATA-AUDIT.md).

This is a new ledger; the human-adopted [pre-Stage-1 ledger](PRESTAGE1-SOURCE-LEDGER.md) and
[source resolution](SOURCE-RESOLUTION.md) remain byte-identical. It records local observations of retained bytes,
not new retrievals. Third-party text is cited and paraphrased, not republished. `[LIT]` applies to metadata
statements as software provenance, with no chemistry evidence class. Locators below use archive/member names;
private storage locations, build-host paths and personal details are omitted.

## 1. Archive and member identities

The original retrievals occurred on 2026-09-27 at 17:54:40Z (Libint) and 17:54:41Z (Psi4), as recorded in the
prior ledger. The retrieval manifest is 1,802 bytes, SHA256
`556692211f3e144b0c45ce93b2017874ea8267d9ca3cf72861f7a9f95b793983`.
The following are new local hash observations; original retrieval timestamps are not reassigned.

| Archive URL | Observed UTC | Bytes | SHA256 | MD5 |
|---|---|---:|---|---|
| <https://conda.anaconda.org/conda-forge/osx-arm64/libint-2.13.1-h5a0831b_0.conda> | 2026-09-28T16:17:13.515239+00:00 | 65620333 | `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f` | `4bb40f31053b7c84626a6fcbe53a2cb4` |
| <https://conda.anaconda.org/conda-forge/osx-arm64/psi4-1.11-py314h53d0584_1.conda> | 2026-09-28T16:17:13.729638+00:00 | 28516421 | `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10` | `d2f223a4e61700800390b2fc95ed722b` |

| Package | Metadata object | Bytes | SHA256 |
|---|---|---:|---|
| `libint-2.13.1-h5a0831b_0` | ZIP `metadata.json` | 31 | `ffe74e3004bcb66df16fb0713bfeaed92b4256afab624fc1226641ed54b149ec` |
| `libint-2.13.1-h5a0831b_0` | `info-libint-2.13.1-h5a0831b_0.tar.zst` | 41865 | `c05ac158e20ecbd16f648badb3eb5e1dcfcbf67ff71c731c72f061e65909b3d1` |
| `libint-2.13.1-h5a0831b_0` | Decoded metadata tar | 235520 | `c02bc9c7ee1f5e2a2857f3a3e6b3e19e46ccde00299533bd0e5e1b319d3de461` |
| `psi4-1.11-py314h53d0584_1` | ZIP `metadata.json` | 31 | `ffe74e3004bcb66df16fb0713bfeaed92b4256afab624fc1226641ed54b149ec` |
| `psi4-1.11-py314h53d0584_1` | `info-psi4-1.11-py314h53d0584_1.tar.zst` | 274440 | `69b4a8390d9768f40222bdc7f35d4f15a1e8ca6125d3d680b6c43cae85ad8d2f` |
| `psi4-1.11-py314h53d0584_1` | Decoded metadata tar | 1853440 | `48797c00659c78d0722a386b9d476502b09550725cbdac7684e39aafb640347b` |

The compressed members equal the previously retained copies and published digests. The decoded tar hashes bind
all raw headers, PAX records, padding and regular-file contents. The ZIP payload member was listed but never
opened or decompressed; no payload-member digest is asserted separately from the whole-container digest.
ZIP member timestamps and tar timestamps are preserved in the private inventories as metadata fields, not asserted
as independently observed build times. Supplementary validation completed between
2026-09-28T16:40:16.261412Z and 2026-09-28T16:40:16.478867Z.

## 2. Complete regular-member inventory

These are the complete 24 Libint and 23 Psi4 regular-member sets of the decoded info tars. There are no links or
directories in these inventories. Every member was read and hashed for validation; only the records located in the
[audit](RECIPE-METADATA-AUDIT.md) supply interpretive claims. Test programs and build scripts were never executed.
Members are relative to their respective decoded metadata tar. File timestamps, offsets and modes are preserved
privately. Source URLs and digests inside recipes are declarations, distinct from these observed member digests.

### libint-2.13.1-h5a0831b_0

| Member | Bytes | SHA256 |
|---|---:|---|
| `info/about.json` | 8320 | `45fe2a3f09dcd451fc29b9f2787d4f91f123fa3678d6a6b6de6cb3585fb05238` |
| `info/files` | 6037 | `cdbc8498469bd714b1cce64ea816cd8e7dfcdd0d55321139774ff13275193615` |
| `info/git` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `info/has_prefix` | 585 | `9533a7ee156e045bf88724f9dcb4a82847093f4e556252db372d7235524507d8` |
| `info/hash_input.json` | 434 | `282e7120c4e3a877588877be7ee2feca3a383d87aad0b3d979f63c5654136ca3` |
| `info/index.json` | 330 | `dd4c4622543ed452053234be769d9a47abc58efef88b1e3f6ae016265dcf498d` |
| `info/paths.json` | 33979 | `18ab7ef1396d687ed7f89629f80eae614a9ddd184384fc5f8cfc48793830d9b9` |
| `info/recipe/conda_build_config.yaml` | 987 | `538181d39260b7c1e95b1f30d2bca4415bc75db84fe84a5e59c9f9555d0334c2` |
| `info/recipe/meta.yaml` | 4393 | `6cf388d2a06e5a7805e97dccdfaec7a4a1cdb6c64db365a1413d9e7c9a420dd0` |
| `info/recipe/parent/NOTES` | 6391 | `1c2bea113e6b7bc73434bdb59a2dfd0e584d47b86ee43903731ecaa58644f84d` |
| `info/recipe/parent/bld.bat` | 1240 | `25623d9ee64e18647c385a29ae6e6fd0c715cf0c5d6c3198bec3e8d18bbd8ac8` |
| `info/recipe/parent/build.sh` | 1343 | `bd45ca66356dcf7eaa79d2e457124c03bfbb92f953ae7533301c21ccbdd0d498` |
| `info/recipe/parent/conda_build_config.yaml` | 140 | `cb057f23d30771078f7a9de2c1062aefb4e483e889628efe5514f9af36116716` |
| `info/recipe/parent/meta.yaml` | 9482 | `70ae3ee7330936eb26a96934841b5b5cec614b59c7d06e366166db91f375ab43` |
| `info/recipe/parent/recipe-scripts-license.txt` | 1541 | `86dc4bc79c9fa4d5dc3ae5558441d5bb8b8736403e70997cf9ae8f671ab5d0ca` |
| `info/recipe/parent/tests/hartree-fock/CMakeLists.txt` | 710 | `98927f6f6c972d15f5c4103102c70f08faf876c7bb4345963993282c1282dfb7` |
| `info/run_exports.json` | 36 | `27fbcb61c1b892feafe94312d96ef0f499a6324e76cff90ab4cbdc1dd44d99f1` |
| `info/test/features` | 239 | `7edf970d26e6f101b1a4fc8fede6b74336b0612cee159d3899a093999845bc83` |
| `info/test/run_test.sh` | 638 | `3be14d78a5a5d4a55d46d93596427090d1a97d1d94e3235e35ccc54ca6161f40` |
| `info/test/test_time_dependencies.json` | 90 | `0bf6d09bd3f7472a1110438358cb2f307d80c79b063398371367141625a0ee6f` |
| `info/test/tests/hartree-fock/CMakeLists.txt` | 710 | `98927f6f6c972d15f5c4103102c70f08faf876c7bb4345963993282c1282dfb7` |
| `info/test/tests/hartree-fock/h2o_rotated.xyz` | 257 | `74a99a1243d3e654fda6e9a44aed97383156c30e68ec3abc694c829c68bac3ad` |
| `info/test/tests/hartree-fock/hartree-fock++-validate.py` | 11422 | `b40395b69cdb5bab88f396106a797125703e38ec28b5434188a216ff64570cae` |
| `info/test/tests/hartree-fock/hartree-fock++.cc` | 98029 | `b03d66653155973169d254142e299946b0d351115a133ade31ebd02a82c30eb4` |

### psi4-1.11-py314h53d0584_1

| Member | Bytes | SHA256 |
|---|---:|---|
| `info/about.json` | 9859 | `83a5d6ce5bfc6aa2e5b3c5c8ba2ecf6c390d2f290db5b922ef9b6cecead7125d` |
| `info/files` | 298826 | `836f297511ef8b5af5b8f0d6dcf1add4d5b942ee1e7afcc4cbe6840b3fd7d905` |
| `info/git` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `info/has_prefix` | 2289 | `0c1d31e28d9400316b8d31d1cdb012752088c7ff1191da6a704dc44dc69c052e` |
| `info/hash_input.json` | 546 | `621cbd1e73b679addb5a4e5a472d6af40a57ee6c72a9a60fad3c18b74f34ceb4` |
| `info/index.json` | 1515 | `f651f5c2b42316b60d66d470081c187d9ea927440fe46f3d3be830b3defef7c5` |
| `info/licenses/COPYING` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| `info/licenses/COPYING.LESSER` | 7651 | `da7eabb7bafdf7d3ae5e9f223aa5bdc1eece45ac569dc21b3b037520b4464768` |
| `info/licenses/THIRD-PARTY-LICENSES` | 21730 | `6c110e22202c17e8dafe3d0b1bc05c629fd05036431a2e7a89614bdebed390ce` |
| `info/paths.json` | 1389245 | `42dd9797ecb2c72a2f489de611afffaee0095a8786eca06c7a55112abc51ffd8` |
| `info/recipe/0001-rename-th-fl-for-libxc-7.1.patch` | 1454 | `660a47f03811fc89cc175212140658533157d10b6e375e98811cb747eb696e06` |
| `info/recipe/bld.bat` | 4343 | `64d4438ccc302a237d670908143e684b54f4a5b51a6df6f0645097deee484294` |
| `info/recipe/build.sh` | 5942 | `a5285ed70e8166b52cd5bce5829916fc1131dc8c5fd1999e6e71dde4e07f1c7f` |
| `info/recipe/conda_build_config.yaml` | 995 | `cc59d6a1e57a880117127af83d30a674dbcfcb8d08151983f89d6cef9241da21` |
| `info/recipe/meta.yaml` | 9867 | `4972399b6110873c71c656de71bc4671560aec4cfe9cb4a7d98be91258af8dd1` |
| `info/recipe/meta.yaml.template` | 16654 | `8b2a4de7fc59e9bee9d7fdf49628c1f458e44b8ed79f79510110ed0aabb4eac1` |
| `info/recipe/recipe-scripts-license.txt` | 1520 | `b76585ad68860b271fc4c5a346444e4a70cacd48a3fd688cb2e8dd18d5935cd1` |
| `info/recipe/src/psi4PluginCachelinux.cmake` | 1457 | `7d4b25d7768d5f99ef353755994bd03648c532e1cdef0c60820a1e5528966aa6` |
| `info/recipe/src/psi4PluginCacheosx.cmake` | 1478 | `63eedecc98e01607a71732a8d386d6f763cee3a10d591bcba1f82e8fdeb7c27e` |
| `info/run_exports.json` | 35 | `0fd7945b15de2239d4363a3752461a6fb489f27e657cc4e60fba906c452e043a` |
| `info/test/run_test.py` | 37 | `c28410faec8aac1ef3716ce9e12653c7246027c69caab6e21fa404f9d5509832` |
| `info/test/run_test.sh` | 1244 | `b696bd0f7eb438c3ba1eed937b5cc80f689863e6e4e52bc17f04f3547116d2e3` |
| `info/test/test_time_dependencies.json` | 244 | `dee3a2a34d32c458e1dea3a0dc5e7f98be1201c31feeb89f234dcab9678a8e9e` |

## 3. Retained installed records and comparisons

The prior complete Libint installed record, 67,513 bytes, has SHA256
`7cb2b345fecc86f890da13f971ec3cd1c03ee5d6aa8907d2326adefa2d4b634b`. Its exact fields and those in the
retained Psi4 field extract were compared with each archive's `info/index.json`: `name`, `version`, `build`,
`build_number`, `subdir` and the complete `depends` list are equal for both packages.

| Retained evidence | Bytes | SHA256 | Exact selector / limitation |
|---|---:|---|---|
| Libint installed package-field extract | 1465 | `dd1e76cd750891bd328543d4fe570784a9e4a441b77bbab2f98123362b6e5704` | `package_fields`; separate from the complete record |
| Installed-prefix identity report containing Psi4 fields | 3059 | `b1bd26221265c0f9706d3d0a7ecd9c4f51685e2cab1df47f85537a96760bfed6` | `rows[1].package_fields`; the full raw Psi4 record is not retained |
| Earlier full Psi4 installed record, identified by the prior audit | 2759029 | `853149d1b89fa4ca2ae2768de9a4e66220c0a93fab339f6520d51ea71fc1b4f2` | Prior observation only; no fresh full-record read or recomputation claimed here |

Libint `info/paths.json`, `paths[]` selected by `_path == include/libint2/shell.h`, has `sha256`
`e0aa1e87e7cccc05c84955c9cf496fdccee2caad92c8c3e3b7f41fedd9a99c9e`, equal to the prior installed-header
observation. Neither comparison is evidence about compiler inputs or runtime linkage.

## 4. Reproducibility, bounds and failures

The private scripts and reports below retain exact command arguments, input identities, observed UTC times,
exit statuses, limits, raw-header and parsed views, schema checks and per-member digests. The extraction profile
and numerical bounds are stated in [audit §1](RECIPE-METADATA-AUDIT.md#1-scope-identity-and-safe-reading).
The retained Zstandard CLI identifies itself as version 1.5.7. Its existing installation receipt records epoch
1783517208 (2026-07-08T13:26:48Z); this is receipt metadata, not a newly witnessed installation. No software was
installed for this audit.

| Private evidence or code (description only) | SHA256 |
|---|---|
| Initial archive/member/file inventory | `717b05dcd606343650a5c516511b78e56a607b769df578c8e15281135d6e7bb6` |
| Initial extraction command log | `8038be86d62131931d20989504af9d2468fe50670c0c1599a0ee0b640a3a505c` |
| Extraction driver | `d285d249fc87714e3de9b759d7a3b2f3f2be134b8d75cdd0f4ac000fb100a204` |
| Bounded metadata reader | `c9aff29ba5ca571c5ab9386260536db582d647d05f8ffc769c49ce9022b97249` |
| Supplementary validation driver | `c51c1359bd23037a21922cfc53410698ba6f26d4d9e2aeddeaec7eba4eb887b5` |
| Raw tar/PAX validator | `e947c6a09dbb6b2d91680b168fd6e9b2e6b9a67d42d531f4e66805a048848585` |
| Strict JSON validator | `a8b8fcfac415265a28b8e610659752016f68b26845e07b78caf659bc61f83d50` |
| Corrected supplementary report; COMPLETE | `1857a58c6f8906f64b5a5e908e79bb20bf86852ddbad8e5f5acf5e552ba8382b` |
| Corrected supplementary command log | `58d730c7791e83257bc851dbe2a988c946093e0e8f4187c264660cebd08888f4` |
| Stopped supplementary report; timestamp-rule false positive | `4e944c8fba0ba686d3881e323bca85092d6df30cfb1d300dce55f53046385dcb` |
| Stopped supplementary command log | `dfb1da535e830fce8bb03b1ba247a9070be40f4407d8dbedb1d99d5a3a2046ac` |
| Full 121-test run | `fdd0dc03bd69ea281abd5e4be820cabda1f30eb8d2775e2a96e2670e575a32e1` |
| 79-mutation diagnostic report | `7722ea913dd5b21144cc0105e9289c2533b0293e552451887d1f78c8e0e88e0d` |
| 79-mutation command and code-binding record | `fa7f3ae7cc482c5fe887aea7d37bc40b0d9e6ee5711e88fad8f2c81293cd275e` |
| Mutation harness with diagnostic classification | `fc8507f2576e5fd83daf950a03738c33f9b40cc664451bd73558e45637528310` |
| Withdrawn blanket-exception conversion note | `80388a7383f4f1fb1dfd6552bbe292170cd12a093832447088dc00b221086cbe` |
| Independent archive and 47-file hash comparison | `18e1bf8e62fafbc7f6ba372aef39e73d6ce19171257fe2780d58e39f3d3cb2a9` |
| Installed-record/index/header-digest comparison | `e6d03466a015ee7855c8b934fedc9cfc39cdf7a2080cf3da0f167f16cc88e3fe` |
| Existing decompressor executable | `d36baef4919b567feff3973ef2edc07e0373b8015495f0248b80e3646d383cee` |
| Existing decompressor installation receipt | `4f50e27fe4df17385b9d2da257e2258d8d3db3a6befacec513e7173a9937c23f` |

**Failure retention.** The earlier system-archive-tool zstd failure remains in the prior ledger and audit.
The first read used permissive JSON parsing and lacked raw PAX validation. Independent review exposed acceptance
of malformed/conflicting PAX fields in synthetic test fixtures; a supplement corrects that gap while retaining
the first scripts/report. The actual archives contain only single `mtime` PAX records, with no `path`, `size`
or duplicate keys. Separately, an initial supplementary run stopped because its floor-only timestamp consistency rule rejected rounded whole
seconds in the actual archives. The correction admits a zero placeholder or a difference below one second,
with finite/range checks, explicit regression cases and unchanged original timestamps in the inventories.
The stopped report is retained separately from the successful report.

Test history also retains deliberately failing initial stubs, a harness/import defect, insufficient mutation
anchors, a fixture defect and a withdrawn run that converted exceptions too broadly. The withdrawn run is not
relied on. The final tests use narrow assertions; the mutation report retains diagnostic traces and identifies
the mutated module. Original command logs and earlier results remain private, including failures that are not
sources of a final public claim. Review observations concern software provenance and the bounded parsing profile;
they establish no engine, method or chemistry result.
