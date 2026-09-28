# P2 Psi4 build-declaration source ledger

Date: 2026-09-28. Companion to the [P2 build-declaration decision packet](P2-PSI4-BUILD-DECISION-PACKET.md).

This ledger records the public evidence on which the packet rests. **No installed file, archive, installation or
engine was newly read, retrieved, installed or run for it; committed public records were its only inputs.** Every
claim of the packet is taken from records committed at repository commit
`066241a4f902f14e10203e776bdc6afec61f362b`, which are identified below by the SHA256 of their bytes at that commit.
Where a cited record has changed since, the export manifest gives its current digest. No archive, installed
environment, engine or private record is a source of any public claim here. Third-party text is cited and
paraphrased, not republished.

Evidence treatment follows the [evidence policy](../evidence-policy.md). Package and recipe statements are `[LIT]`
software provenance, with no chemistry evidence class. The packet's recommendation, candidate text and inferences are
`[AGENT]`. Missing evidence is `[GAP]`.

## 1. Cited records

| Record | SHA256 at commit `066241a4…` | Used for |
|---|---|---|
| [INSTALLED-BUILD-AUDIT.md](INSTALLED-BUILD-AUDIT.md) | `43d75ce277099f67c8cc6b682e2e3a7192a6c0305d140a2693f8dcafd3ff9e3f` | Installed package records of both packages; installed-file observations; linkage declarations; the open declaration of the P2 build |
| [RECIPE-METADATA-AUDIT.md](RECIPE-METADATA-AUDIT.md) | `cc05c86c032b392205dbe78bef2c5dbc514149e1775394e25a89d2bf5f063789` | Archive index tuples; recipe source, patch, requirements, variants and tensions; dispositions |
| [RECIPE-METADATA-SOURCE-LEDGER.md](RECIPE-METADATA-SOURCE-LEDGER.md) | `96015d4669e57f60d09efd46647934ba44ed310d163192b5e4eb6f9ad5bd99eb` | Archive sizes and digests re-observed 2026-09-28; member inventory; header path-record digest |
| [PRESTAGE1-SOURCE-LEDGER.md](PRESTAGE1-SOURCE-LEDGER.md) | `9cec2c5b4e4f4c78ac5094dfec40731307ebe3a5d6657487b1943e6d1802be29` | What the installed core library was compared with |
| [SOURCE-RESOLUTION.md](SOURCE-RESOLUTION.md) | `cc07691b70383a220fd531d3e7476e7964bf862b34b7e33666fb58d4654c7e25` | Normalization and compiled-step dispositions and their open items |
| [B2-METHOD-DECLARATION.md](B2-METHOD-DECLARATION.md) | `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` | B2 §6 as it stands; the declared P2 settings; §8 |
| [C4-TOLERANCES-AND-CONVERGENCE.md](C4-TOLERANCES-AND-CONVERGENCE.md) | `a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da` | References to B2 §6; the revision sequence of §3 |
| [C7-VALIDATION-SET.md](C7-VALIDATION-SET.md) | `301fc51755080e8f0e6126436a8e4ec45ba078ed01b81ce55aebabf34bd9a412` | Reference to B2 §6 |
| [B3-DRIVE-PROTOCOL.md](B3-DRIVE-PROTOCOL.md) | `291754f60b49be52e349379c0f80dc0ed4782704e58f00a906997db8d842f955` | Its references to B2 sections |
| [C2-COUPLING-ROUTE.md](C2-COUPLING-ROUTE.md) | `aa8425952187d9460a81034cbd98fc5c11108034a9bdda0afd0eb328c410459a` | Its references to B2 sections |
| [C4-HUMAN-APPROVAL.md](C4-HUMAN-APPROVAL.md) | `96975be965e2bd10eed45ab236282ec0c6d7d3751965eb98f2e216e5a925cffc` | Adoption of references at commit `bd3d16a5…` |
| [C4-HUMAN-APPROVAL-02.md](C4-HUMAN-APPROVAL-02.md) | `d7e717bdd4be85e6355faf11f5b45e70c88fcc56dae86c419377bf73509db3fc` | Whole-file adoption of B2 by C4, B3, C2 and C7; record pattern |
| [B2-G4-HUMAN-APPROVAL.md](B2-G4-HUMAN-APPROVAL.md) | `e489b9b9e982c42ee3d402eda3f33bbcdf36752a8fd31c327be47881ed8a6f69` | Whole-file approval of B2; the precedent of candidate bytes without a date |
| [G4-DFTD4-DECLARATION-PROPOSAL.md](G4-DFTD4-DECLARATION-PROPOSAL.md) | `1c7b9d4c76a6dea74d023b8e956beea948676e55a2f7c78b61b3712e0806bb83` | Pattern of the candidate declaration |
| [N8-DECISION-PACKET.md](N8-DECISION-PACKET.md) | `f726b5bb49c1458b504b7fd0a7e400cf75d36bbd78c2bf9945583414ae42ca92` | Pattern of the decision packet and edit map |
| [STAGE0-FREEZE-RECORD.md](STAGE0-FREEZE-RECORD.md) | `07e17b1c7b9e7c4b3607d85895be1419953b3c1056ebf03affa3e973710b519a` | Frozen bindings; dispositions of B2 and C7 |
| [Package index](README.md) | `1288f41ab9bdcfdacede9fe433fe43842521f6202d6d4347ed8c511f5094bd94` | Open items |
| [results/e01/README.md](../../results/e01/README.md) | `382b1f3abf3f54db39fbbfb5f56afb8c7779d3a2db4cae1c2adeb7468eab90d8` | The account of the E-01 stop |
| [results/e01/outcome.json](../../results/e01/outcome.json) | `7150b3420c414eab06114cfbc94e28b582875cc0c7df589712de794a5a729370` | E-01 summary, job record, disposition and non-claims |
| [results/e01/method-config.json](../../results/e01/method-config.json) | `cf06bedef08fbc1e3d0d36508360b4a2d0318d692bc2c093f92ffe2d58afd8aa` | E-01 method, environment versions, selected installed-file digests and the TH-FL deviation |
| [results/e01/postmortem.md](../../results/e01/postmortem.md) | `645b421eb858fd0359b9c4d0aaa7ce089f4fb4625769400c46ce9f5a0abf71b9` | Status of the conditional pathway and of disk capacity |
| [Evidence policy](../evidence-policy.md) | `32c88d9a0c4c516a4588cd4340f2af50198d30a0b9dcddac4b51d82dc7338720` | Evidence classes |

## 2. Candidate identity: each field and its locator

Each field was confirmed from the records above, independently of any summary. No field is unconfirmed.

| Field | Value | Confirming locator | Corroborating locator | Kind |
|---|---|---|---|---|
| Psi4 package tuple | `psi4` `1.11`, build `py314h53d0584_1`, build number 1 | Installed-build audit §3, line 55 | Recipe audit §3, line 84 (`info/index.json`) | Package identity |
| Channel, subdirectory | `conda-forge`, `osx-arm64` | Installed-build audit §3, line 56 | Recipe audit §3, lines 84 and 88 | Package identity |
| Psi4 archive SHA256 | `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10` | Installed-build audit §3, lines 57–58 | Recipe audit §1, line 27; recipe ledger §1, line 21 (28 516 421 bytes) | Package identity |
| Installed core library | `lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so`, 37 500 848 bytes, `0d12c8cda49e2cfe75cea563a2fe51889fa61b88c7b5234beb165b9b54805d99` | Installed-build audit §2, line 49 | Pre-Stage-1 ledger, line 58 (compared with the retained survey only); `method-config.json`, `engine.selected_installed_file_sha256` | Observation of the E-01 installation; not compared with the package payload, which was never opened (recipe audit §1, lines 33–35) |
| Recipe source | `https://github.com/psi4/psi4/archive/v1.11.tar.gz`, declared `b6b5a4d397ba551d7f3516e5dc0da64bcc5778e3dca7898504293792d1b02bac` | Recipe audit §2, line 63 | — | Recipe declaration; not retrieved or verified |
| Recipe patch | `0001-rename-th-fl-for-libxc-7.1.patch`, `660a47f03811fc89cc175212140658533157d10b6e375e98811cb747eb696e06` | Recipe audit §2, line 64 | Recipe ledger §2, line 90 (1 454 bytes) | Recipe declaration; application not observed |
| Exact Libint pin | `libint 2.13.1 h5a0831b_0`, host (recipe line 115) and run (line 178) | Recipe audit §3, line 89 | Recipe audit, line 7; installed-build audit §3, line 60 | Recipe and installed-record declaration |
| Libint package tuple | `libint` `2.13.1`, build `h5a0831b_0`, build number 0, `conda-forge` `osx-arm64` | Installed-build audit §3, lines 65–66 | Recipe audit §3, line 84 | Package identity |
| Libint archive SHA256 | `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f`, 65 620 333 bytes | Installed-build audit §3, lines 68–69 | Recipe audit §1, line 26; recipe ledger §1, line 20 | Package identity |
| Installed Libint header | `include/libint2/shell.h`, 53 810 bytes, `e0aa1e87e7cccc05c84955c9cf496fdccee2caad92c8c3e3b7f41fedd9a99c9e` | Installed-build audit §4, line 80 | Recipe ledger §3, lines 117–119 (the Libint archive's `info/paths.json` gives the same digest) | Observation that agrees with the package path record; not a compiler observation |

## 3. Claim locators

| Packet section | Claim | Record and locator |
|---|---|---|
| §1 | B2 §6 names Psi4 1.11, "the build installed for E-01 (SOURCES [20])" | B2 lines 143–144 |
| §1 | The declaration of the Psi4 build that P2 uses is open | Source resolution §6, lines 367 and 379; installed-build audit §7, lines 142 and 149; recipe audit §5, line 132 |
| §1 | Preparing a separate P2 package is supportable, as an `[AGENT]` recommendation | Recipe audit §5, line 134 |
| §3 | The installed 2.13.1 header defines the normalization that the source resolution read at v2.8.1, a version that is Psi4's source pin and minimum and not that of any build | Installed-build audit §7, lines 124–132; source resolution §6, lines 376–379, and §2 (Libint) |
| §3 | The patch touches no traced compiled routine | Recipe audit §2, line 64 |
| §3 | The only installed deviation from the tag recorded for `libxc_functionals.py` is the TH-FL entry | `method-config.json`, `engine.installed_file_deviation` |
| §3 | Recipe and source-resolution archive digests differ; no comparison made | Recipe audit §2, lines 70–75 |
| §3 | No configure trace, compiler command or loaded-file record | Recipe audit §4, lines 121–123 |
| §3 | Host declarations are not proof of consumed headers | Recipe audit §3, line 87 |
| §3 | Native-runner versus cross-compile, build platform and SDK tensions | Recipe audit §3, lines 91–101 |
| §3 | Libint's generated-library source and its lineage | Recipe audit §2, lines 65–67 |
| §3 | Only the linkage declaration `@rpath/libint2.dylib` was read | Installed-build audit §4, lines 84–90 |
| §3 | The E-01 environment's 94 packages, recorded versions and file-integrity scope | `method-config.json`, `engine.distribution`, `engine.recorded_versions` and `engine.integrity_scope` |
| §3 | The dispersion-input contract relies on installed qcengine files | B2 line 149 |
| §4 | E-01 configuration: PK, basis, Cartesian functions, threads and engine memory | `method-config.json`, `method` |
| §4 | E-01 precursor basis of 478 functions | `outcome.json`, `species.precursor.gates_before_first_scf.basis_construction.nbf` |
| §4 | E-01 stopped in PK integral setup, `PSIO_ERROR` 17 on unit 92, before any SCF iteration | `outcome.json`, `summary` and `species.precursor.jobs`; results/e01 README §2, lines 42–47 |
| §4 | Cause undiagnosed; pathway and disk capacity neither established nor excluded; technically BLOCKED, scientifically INDETERMINATE | `outcome.json`, `disposition`, `hypotheses` and `not_claimed` |
| §4 | No converged electronic energy and no gradient of either donor; every dependent criterion INDETERMINATE; the activated donor not run | `outcome.json`, `summary` and `disposition` |
| §4 | P2 settings, and that the disk-based PK algorithm is not used | B2 line 153 |
| §7 | Normalization items not established | Source resolution §6, lines 366–371 |
| §7 | Build provenance and runtime conformance of the compiled steps | Source resolution §8, lines 603–620 |
| §7 | N7 P2 agreement, budgets B_E and B_F, P2 established only if every comparison passes | C4 row 8, line 34; N7, lines 132–138 |
| §7 | N4 force calibration in Stage 1a | C4 line 108 |
| §7 | N2 same representation; a missing diagnostic makes N3 to N7 INDETERMINATE and blocking | C4 lines 64–89 |
| §7 | Libxc 7.1.2 printed at E-01; CP2K libxc `[GAP]` | B2 line 155 |
| §7 | The defining reference was not obtained (HTTP 403) | B2 line 112 |
| §9.2 | C4, B3, C2 and C7 adopt B2 at `aa24a452…` | C4-HUMAN-APPROVAL-02.md lines 48–62, B2 row line 55 |
| §9.2 | The G4 approval covers every byte of B2 at `aa24a452…`; the approval date is kept out of B2 | B2-G4-HUMAN-APPROVAL.md lines 25–45 |
| §9.2 | C4's references to B2 §6 | C4 lines 67 and 99 |
| §9.2 | C7's reference to B2 §6 | C7 line 57 |
| §10 | The revision sequence | C4 §3, lines 199–216 |

Line numbers refer to the bytes identified in Section 1.

## 4. Exact-byte binding of the candidate text

The packet's candidate text, [§6](P2-PSI4-BUILD-DECISION-PACKET.md#6-candidate-declaration-unapplied), is two
paragraphs, each a single blockquote line. **Convention:** the bytes of a paragraph are that line without its leading
`> ` (greater-than sign and one space), encoded in UTF-8, followed by one line feed. These are the bytes that option A
would insert into B2 §6, each after one blank line.

| Paragraph | Opening words | Bytes | SHA256 |
|---|---|---:|---|
| D1 | **Declared Psi4 build for P2.** | 2625 | `da52ca797f5cc1831ab9275fdab60749658d74d40716800fc509f0a6773ccfca` |
| D2 | **Provenance and scope of the declaration above.** | 2579 | `2e74db033dc2364e03f94a2fc4111b215c762e6092d04c1f529d0c3e89ef324c` |

Neither paragraph contains a date or a field to be filled in later. These digests bind candidate text only. They do
not bind or predict a whole-file revision of B2, which does not exist and would be approved only by its own digest.

## 5. Limits

- The packet is a paraphrase and locator index of committed records. It adds no observation.
- Recipe and package statements carry the limits of the records cited: declared sources were not retrieved, patch
  application and compiler inputs were not observed, and no package test or engine was run.
- The installed-file observations concern the one installation of E-01 and were made on 2026-09-27; nothing was
  re-observed for this ledger.
- Stage 1 remains BLOCKED and is not authorized. This ledger authorizes nothing.
