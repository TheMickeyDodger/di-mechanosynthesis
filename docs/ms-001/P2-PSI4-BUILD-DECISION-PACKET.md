# P2 Psi4 build-declaration decision packet

Date: 2026-09-28. MS-001 scope option B, before Stage 1. Status: **decision support for a person. One option is
recommended as an `[AGENT]` proposal. No option is chosen, approved or applied, and no build is declared.**

This packet prepares one decision: whether the exact conda-forge Psi4 package build of the E-01 environment should be
declared prospectively as the Psi4 build that P2 uses, the second implementation of ωB97X-D3 in
[B2 §6](B2-METHOD-DECLARATION.md#6-second-implementation-for-the-p2-check). It states the object, the evidence for and
against, what the stopped E-01 attempt does and does not show, the options with their consequences, exact candidate
text, what approval would and would not settle, and every record that a later, approved application would change.
Its sources, claim locators and exact-byte bindings are in the
[companion source ledger](P2-PSI4-BUILD-SOURCE-LEDGER.md).

What this packet is not:
- **Not the decision.** A declaration changes B2 and is reserved to the roles of the original selection under
  [C4 §3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding): the method author proposes, the independent
  reviewer checks, and a person decides. Reviewing, accepting or publishing this packet is not that decision.
- **Not a change of any definition or approval.** No frozen definition, no adopted scientific reference and no
  approval record changes: B2, C4, B3, C2, C7 and every approval record are byte-identical. The package index, the
  [freeze record](STAGE0-FREEZE-RECORD.md#2-frozen-artifacts) (its package-index digest and a status supplement), the
  root README, the research state, the source catalogue, the pre-Stage-1 closure packet and the export manifest receive
  status, navigation and digest-refresh edits only, disclosed in the export manifest. No candidate text below is
  applied.
- **Not a build, installation or runtime claim.** Nothing was installed, built, retrieved, imported or run for this
  packet, and no calculation was made. It reads committed public records only.
- **Not authorization or readiness.** Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized. Stage 1 remains
  BLOCKED.

## 1. The question

**Should the exact package artifact identified in Section 2 be declared prospectively, under the revision sequence of
C4 §3, as the Psi4 build that P2 uses?**

B2 §6 already reads: "The declared second engine is **Psi4 1.11**, the build installed for E-01 (SOURCES [20])"
(B2 lines 143–144). That sentence names the engine version and points to an installation. It does not state a build
string, a platform, a package archive or its digest, or the Libint package, so it does not by itself pin a package
artifact that a later installation could be checked against. The later records accordingly leave the declaration of
the build open:
- the [source resolution record, §6](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4) leaves open "the
  Libint2 version linked by the Psi4 build that P2 uses" (line 379);
- the [installed-build audit, §7](INSTALLED-BUILD-AUDIT.md#7-relation-to-the-normalization-item) records that "Whether
  P2 will use the E-01 build is a declaration not made here" (line 142);
- the [recipe metadata audit, §5](RECIPE-METADATA-AUDIT.md#5-dispositions-and-prospective-p2-decision) keeps "the P2
  build declaration" open under basis normalization (line 132) and supports preparing this separate package as an
  `[AGENT]` recommendation (line 134).

A declaration would add the exact **package artifact identity** that the phrase "the build installed for E-01" does
not pin. It would not correct B2 §6, whose sentence stays accurate, and it would not mean that any build was approved
before. No Psi4 build has been declared or approved by a person for P2.

## 2. The object under decision

Three kinds of identity are kept apart. Only the first would be declared.

| Kind | What it identifies | Status in this repository |
|---|---|---|
| **Package artifact identity** | The conda package archives and their index fields | Established by the installed package records and by the archives' own `info/index.json`; archive digests re-observed on 2026-09-28 |
| **Installed-file observations** | Bytes of particular files in the one installation of E-01 | Observations of that installation only. They are not properties of the archive |
| **Runtime identity** | Which files a P2 run actually loads and which code paths it takes | Not observed. It exists only in Stage 1 run records |

**Package artifact identity (the object).**

| Field | Psi4 | Libint | Public locator |
|---|---|---|---|
| Package, version | `psi4` `1.11` | `libint` `2.13.1` | [Installed-build audit §3](INSTALLED-BUILD-AUDIT.md#3-installed-package-records), lines 55 and 65; [recipe audit §3](RECIPE-METADATA-AUDIT.md#3-build-host-and-variant-records), line 84 |
| Build string, build number | `py314h53d0584_1`, 1 | `h5a0831b_0`, 0 | The same |
| Channel, subdirectory | `conda-forge`, `osx-arm64` | `conda-forge`, `osx-arm64` | Installed-build audit §3, lines 56 and 66; recipe audit §3, lines 84 and 88 |
| Archive | `psi4-1.11-py314h53d0584_1.conda`, 28 516 421 bytes | `libint-2.13.1-h5a0831b_0.conda`, 65 620 333 bytes | [Recipe ledger §1](RECIPE-METADATA-SOURCE-LEDGER.md#1-archive-and-member-identities), lines 20–21 |
| Archive SHA256 | `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10` | `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f` | Installed-build audit §3, lines 57–58 and 68–69; [recipe audit §1](RECIPE-METADATA-AUDIT.md#1-scope-identity-and-safe-reading), lines 26–27 |
| Relation | Its rendered recipe pins `libint 2.13.1 h5a0831b_0` in both `requirements.host` (line 115) and `requirements.run` (line 178) | The pinned package | Recipe audit §3, line 89; installed-build audit §3, line 60 |

**Recipe metadata of the Psi4 artifact** (`[LIT]` software provenance; declarations, not observations):
- source `https://github.com/psi4/psi4/archive/v1.11.tar.gz`, declared SHA256
  `b6b5a4d397ba551d7f3516e5dc0da64bcc5778e3dca7898504293792d1b02bac` (recipe audit §2, line 63);
- patch `0001-rename-th-fl-for-libxc-7.1.patch`, SHA256
  `660a47f03811fc89cc175212140658533157d10b6e375e98811cb747eb696e06`, which changes one Python functional-table entry,
  TH-FL, from `GGA_XC_TH_FL` to `LDA_XC_TH_FL` (recipe audit §2, line 64).

The source archive was not retrieved or verified, and application of the patch to the build was not observed.

**Installed-file observations of the E-01 installation.**

| File | SHA256 | Compared with | Locator |
|---|---|---|---|
| `lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so` (37 500 848 bytes) | `0d12c8cda49e2cfe75cea563a2fe51889fa61b88c7b5234beb165b9b54805d99` | The retained survey of E-01 only. **Not compared with the package payload or with a package path record:** the payload member of the archive was never opened | [Installed-build audit §2](INSTALLED-BUILD-AUDIT.md#2-identity-check), line 49; [pre-Stage-1 ledger](PRESTAGE1-SOURCE-LEDGER.md), line 58; recipe audit §1, lines 33–35 |
| `include/libint2/shell.h` (53 810 bytes) | `e0aa1e87e7cccc05c84955c9cf496fdccee2caad92c8c3e3b7f41fedd9a99c9e` | The installed Libint record, and the path record `info/paths.json` inside the Libint archive; equal to both | [Installed-build audit §4](INSTALLED-BUILD-AUDIT.md#4-installed-libint2-files-against-the-record), line 80; [recipe ledger §3](RECIPE-METADATA-SOURCE-LEDGER.md#3-retained-installed-records-and-comparisons), lines 117–119 |

Whether installation changes the bytes of a packaged file is neither established nor excluded here, and nothing in
this packet relies on either. The installed core library's digest is a fact about one installation. The archive's
payload member was never opened, so no digest of the core library inside the archive is known here, and the E-01
digest was never compared with one.

## 3. Evidence for and against selection

**What favours selecting this artifact.**
1. **A complete, public identity chain.** The installed Psi4 record names the archive and its digest. The re-observed
   archive has that digest. The archive's own index gives the same tuple. Its rendered recipe pins the exact Libint
   package in host and run requirements. The installed Libint record, the Libint archive's path record and the
   observed installed header agree on the header digest. Every link has a public locator (Section 2).
2. **The package-level audits concern this artifact.** The installed-build audit and the recipe audit describe this
   exact package and its Libint package. Three separate objects agree in what they define, and none is a reading of
   the compiled binary:
   - the source resolution's reading of Libint v2.8.1, the version that Psi4 names as its source pin and minimum and
     not the version of any build
     ([source resolution §6](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4));
   - the installed Libint 2.13.1 header of the E-01 installation, which defines the same single-primitive
     normalization (installed-build audit §7, lines 124–132);
   - the recipe's exact pin of the 2.13.1 package (recipe audit §3, line 89).

   None shows which header bytes the Psi4 core was compiled against.
3. **It can be checked.** Two archive digests identify it, and a later installation's package records can be checked
   against them without executing anything. The correspondence of its installed binaries to the archives is a further
   check that the candidate requires (Section 8).
4. **It is consistent with the text B2 §6 already carries.** It is the package of the installation that B2 §6
   names, so a declaration narrows that text to an artifact rather than changing it.
5. **The recorded patch touches no traced compiled routine.** The recipe audit states that the patch text changes one
   Python table entry and touches no compiled routine traced in the source resolution (recipe audit §2, line 64).
   `[AGENT]` observation: the only difference from the tag that E-01's configuration records for the installed
   `libxc_functionals.py` is that same TH-FL entry (`results/e01/method-config.json`,
   `engine.installed_file_deviation`).
   This is consistency between two records, not an observation that the patch was applied.

**What counsels against, or remains uncertain.**
1. **No source-to-binary correspondence.** The recipe's source URL and declared digest are metadata. The declared
   archive digest differs from the digest of the commit archive that the source resolution read; unequal archive
   digests neither establish unequal source trees nor prove equality, and no comparison was made (recipe audit §2,
   lines 70–75).
2. **No compiler record.** No configure trace, compiler command, dependency file or loaded-file record exists in the
   metadata (recipe audit §4, lines 121–123). Whether the Psi4 core was compiled against the pinned Libint headers is
   not established; a host requirement is not proof of consumed headers (recipe audit §3, line 87).
3. **Build-arrangement tensions.** The Psi4 template records a switch to native ARM runners while `build.sh` still
   comments on a cross-compile; Libint's variant record names build platform `osx-64`; SDK versions differ between
   variant records and resolved build lists (recipe audit §3, lines 91–101). None is resolved from metadata alone.
4. **A generated Libint source.** Libint's declared source is a generated-library archive that the parent recipe
   describes as configured differently from upstream release artifacts; its generator revision and execution are not
   verified (recipe audit §2, lines 65–67).
5. **Runtime behaviour unobserved.** Which Libint library file the loader resolves is not established; only the
   declaration `@rpath/libint2.dylib` was read (installed-build audit §4, lines 84–90). Whether code loaded at run
   time changes Libint's normalization flag is not established.
6. **Platform-bound.** The artifact is `osx-arm64` only. Reproduction on another platform, or from a rebuilt package,
   would need a separately identified build.
7. **A narrow scope.** The candidate declares two packages. The E-01 environment had 94 packages, including Python
   3.14.7, libxc-c 7.1.2, qcengine 0.51.0 and simple-dftd3 1.6.0 (`results/e01/method-config.json`,
   `engine.distribution`, `engine.recorded_versions` and `engine.integrity_scope`), and its file integrity was checked
   only for selected files. B2 §6's dispersion-input contract was established against qcengine
   files byte-identical to the installed ones (B2 line 149). The candidate does not declare those packages.

## 4. E-01 and P2

**What E-01 recorded.** E-01 ran this Psi4 environment on the donor precursor with the conventional (PK) SCF
algorithm, 6-31G(d,p) with LANL2DZ and its effective core potential on iodine, Cartesian functions, 4 threads and
2 GB of engine memory (`results/e01/method-config.json`, `method`), and a basis of 478 functions
(`results/e01/outcome.json`, `species.precursor.gates_before_first_scf.basis_construction.nbf`). Its first SCF job,
P-RKS-core, stopped during conventional (PK) integral setup with `PSIO_ERROR: 17 (Incorrect block start address)` on
unit 92, after 852 s and before any SCF iteration was printed (`results/e01/outcome.json`, `summary` and
`species.precursor.jobs`; [results/e01 §2](../../results/e01/README.md#2-what-happened)). No converged electronic
energy and no gradient of either donor was produced, every dependent criterion is INDETERMINATE, and the activated
donor was not run (`outcome.json`, `summary` and `disposition`).

**Its disposition.** The cause is undiagnosed. The conditional source-level pathway recorded in the postmortem is
neither established nor excluded, and so is a contribution from disk capacity. The attempt is closed as technically
BLOCKED and scientifically INDETERMINATE (`outcome.json`, `disposition` and `not_claimed`).

**What P2 declares.** B2 §6 declares `SCF_TYPE DIRECT`, `DF_SCF_GUESS false` and `SAD_SCF_TYPE DIRECT` for P2, with
`GUESS SAD`, `REFERENCE RKS` and def2-TZVP, and states: "The disk-based `PK` algorithm is not used; E-01 aborted during
its setup" (B2 line 153).

**The difference.** E-01's stop occurred in the PK algorithm. P2 declares the DIRECT algorithm. The two configurations
also differ in molecule, basis set and core treatment.

This packet draws no inference from that difference, in either direction. E-01 is not evidence that the P2 DIRECT
route will fail on this build, and it is not evidence that it will succeed. E-01 is not counted for or against
selecting this artifact. No P2 run and no P2 result is recorded in this project, and no converged quantum-chemistry
result exists in it.

## 5. Options and recommendation

| Option | What happens | Practical consequences |
|---|---|---|
| **A. Approve** the candidate of Section 6 | Through C4 §3, the candidate is inserted into B2 §6, and the revised whole-file B2 and its reference environment are freshly approved (Section 9) | The selection part of the P2 build is settled. A P2 run must show the declared package records, or it is not a P2 result under the declaration, and an unexplained binary difference blocks use of the installation until reviewed. Basis normalization stays `PARTIALLY ESTABLISHED`, and every item of Section 7 stays open. New B2 bytes and a new approval record are created; old records are unchanged |
| **B. Decline** | No declaration of this artifact. B2 stays as it is | B2 §6 keeps "the build installed for E-01" without an artifact identity, and the declaration of the P2 build stays open under basis normalization. Any P2 run would first need a build declared through C4 §3. Another candidate would need its own identity work from its package records and recipe; a source build would also need an authorized installation and its own build records |
| **C. Defer** | Nothing changes now | The item stays open, and the candidate stays available while its validity conditions hold (Section 8). Deferral produces no evidence by itself. The missing compiler records are absent from the package metadata, and runtime identity can be observed only in authorized Stage 1 runs on an identified build |

A person may also request a revision, for example different wording or a declaration that covers more of the
environment. That would be a new proposal.

**Recommendation (`[AGENT]`): A, approve.** The reasons, none of which is scientific evidence:
1. **It settles an open selection with the one candidate that has a public identity chain.** Every link in the chain
   has a locator (Section 3, item 1). No other candidate has been identified or audited in this repository.
2. **It is narrow, and it can be checked.** It declares two archives by digest and one conformance condition on the
   run record. It declares nothing that the evidence does not support, and its text says what it does not establish.
3. **Waiting does not close the gaps.** The gaps that count against it (Section 3) are either absent from package
   metadata by its nature or observable only at run time. Runtime observations presuppose an identified build.
4. **Another build would not remove them now.** Another conda build would need this audit repeated from its own
   package records and recipe, with no recorded reason to expect the compiler record that this one lacks. A source
   build would add installation and build work under its own authorization. This is a judgement about effort, not
   evidence about any build.
5. **E-01 bears on neither side** (Section 4).

What approval costs: a revision of B2, a fresh adoption of the revised B2 by the four records of the N8 revision, a
new approval record, and status updates (Section 9). A reader could mistake the declaration for more than a
selection; the candidate text states its limits for that reason.

## 6. Candidate declaration (unapplied)

The two paragraphs below are the exact candidate text. They would be added to B2 §6, after the dated source annotation
of 2026-09-27 on normalization and compiled steps and before §7, only if a person approves option A and the rest of the
C4 §3 sequence is completed. They are **not applied**.

Following the [G4 precedent](B2-G4-HUMAN-APPROVAL.md#1-the-decision), the candidate text carries **no date and no field
to be filled in later**. The decision date would be recorded in the new approval record, not in B2. The exact bytes of
each paragraph are bound by SHA256 in the
[source ledger, §4](P2-PSI4-BUILD-SOURCE-LEDGER.md#4-exact-byte-binding-of-the-candidate-text).

**Candidate paragraph D1 (the declaration):**

> **Declared Psi4 build for P2.** The Psi4 build that P2 uses is the conda-forge package `psi4`, version `1.11`, build string `py314h53d0584_1`, build number 1, subdirectory `osx-arm64`, whose package archive `psi4-1.11-py314h53d0584_1.conda` has SHA256 `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10`. Its Libint is the package that this archive's rendered recipe pins exactly, in both its host and its run requirements: the conda-forge package `libint`, version `2.13.1`, build string `h5a0831b_0`, build number 0, subdirectory `osx-arm64`, whose package archive `libint-2.13.1-h5a0831b_0.conda` has SHA256 `ca18cdfd0b0271e059a214d4d2786dfe88f0bc317b014e6abe1747b6d782cb6f`. The two archive digests are the identity of this build. A package with another archive digest, for another subdirectory, or rebuilt under the same name, version and build string is not this build. The declaration applies to `osx-arm64` only. A P2 run conforms to this declaration only if its run record shows installed package records of both packages whose name, version, build string, build number, channel, subdirectory and archive SHA256 equal the values above, and an installed `include/libint2/shell.h` with SHA256 `e0aa1e87e7cccc05c84955c9cf496fdccee2caad92c8c3e3b7f41fedd9a99c9e`, the digest that the Libint package's path record gives for that file. Otherwise the run does not conform, and it is not a P2 result under this declaration. Matching package records are not sufficient for the binaries. The run record must also give the SHA256 of the installed `lib/python3.14/site-packages/psi4/core.cpython-314-darwin.so` and `lib/libint2.dylib`, their relation to the corresponding files of the declared archives, and the identity of the Libint library file that the run loads. Any difference between those installed bytes and the corresponding files of the declared archives that is not identified and explained, or any correspondence that cannot be shown, must be identified and reviewed before that installation is used for P2; a difference that indicates a different artifact, such as a rebuilt, patched or replaced binary, requires a revision of this declaration through the revision sequence of C4 §3. This declaration neither assumes nor excludes that installation changes these files. It covers these two packages only. It does not declare the Python interpreter, libxc, the dispersion packages or any other package of the environment, the source from which either binary was compiled, the headers or libraries used at compilation, the compiler or its settings, which files a run loads, or what the build computes.

**Candidate paragraph D2 (provenance and scope):**

> **Provenance and scope of the declaration above.** It declares the Psi4 build that P2 uses, which the [source resolution record, §6](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4) and the [installed-build audit, §7](INSTALLED-BUILD-AUDIT.md#7-relation-to-the-normalization-item) left open. It adds the package artifact identity of the build installed for E-01, named above, and changes no other statement of this section. Its text is the candidate declaration of the [P2 build-declaration decision packet, §6](P2-PSI4-BUILD-DECISION-PACKET.md#6-candidate-declaration-unapplied). The identities it names are recorded, with their locators, in the installed-build audit, the [recipe metadata audit](RECIPE-METADATA-AUDIT.md) and their source ledgers. The declaration is `[AGENT]`, over `[LIT]` package identities and recipe metadata. It selects package artifacts; it does not establish what either binary contains, was compiled from or does. The recipe's source archive `https://github.com/psi4/psi4/archive/v1.11.tar.gz`, declared SHA256 `b6b5a4d397ba551d7f3516e5dc0da64bcc5778e3dca7898504293792d1b02bac`, and its patch `0001-rename-th-fl-for-libxc-7.1.patch`, SHA256 `660a47f03811fc89cc175212140658533157d10b6e375e98811cb747eb696e06`, are metadata of the declared artifact, not a declaration of its compiled source. The installed files of the E-01 environment are observations of one installation of this build; the digest of its core library, `0d12c8cda49e2cfe75cea563a2fe51889fa61b88c7b5234beb165b9b54805d99`, was not compared with the package's contents and is not part of the declared identity. Basis normalization remains `PARTIALLY ESTABLISHED`: the declaration selects the Libint package of the P2 build, but the Libint headers used when the Psi4 core was compiled, and whether code loaded at run time changes Libint's normalization flag, remain open. The build provenance and runtime conformance of the compiled Psi4 steps remain open, and the runtime identity observations of P2 remain within Stage 1. The E-01 attempt, run in an installation of this build, stopped during conventional (PK) integral setup, and this section declares the DIRECT algorithm for P2 and does not use PK; the cause of that stop is undiagnosed, and it is not evidence about P2 in either direction. The declaration takes effect only through the revision sequence of C4 §3. Whether and when a person approved it is recorded outside this record, in an approval record bound to the exact digest of this record, and not here. It authorizes nothing and is not readiness for Stage 1.

How the candidate answers the questions this decision raises:

| Question | Where the candidate answers it |
|---|---|
| Exact object, platform and digests | D1: both tuples, `osx-arm64`, both archive SHA256 |
| Package identity versus installed files versus runtime | D1 declares archives; the E-01 core digest is an observation outside the identity (D2); installed digests and the loaded Libint library are run-record observations (D1) |
| No false claim of compiler inputs, source correspondence, linkage or conformance | D1, last sentence; D2 |
| What happens to normalization | D2: selection only; `PARTIALLY ESTABLISHED` stays |
| E-01 | D2: stated without inference in either direction |
| Invalidation, including a changed binary | D1: another archive digest, subdirectory or rebuild is not this build; an unexplained binary difference blocks use of the installation until it is identified and reviewed, and one that indicates a different artifact requires a revision |

## 7. What approval would settle and what stays open

Approval would settle one thing: **the selection of the Psi4 build that P2 uses**, the item that the installed-build
audit lists as the declaration of the P2 build (§7, line 149). It closes no whole prerequisite.

| Item | After approval | Still open |
|---|---|---|
| Selection of the P2 Psi4 build and its Libint package | Settled, by package artifact identity | — |
| Basis normalization (a prerequisite to starting Stage 1) | `PARTIALLY ESTABLISHED`, unchanged; narrowed to the declared Libint package | The Libint headers used at compilation; run-time changes to the normalization flag; conventions beyond radial normalization, not examined ([source resolution §6](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4), lines 366–371). N2's qualification "subject to the normalization item in B2 §6" still applies |
| Compiled Psi4 steps | Tagged-source behaviour stays established; the artifact whose provenance is at issue is fixed | Build provenance (source-to-binary correspondence); runtime conformance of the SAD atomic solver, `is_c_hybrid()` and `core.scfgrad`, including the P2 JK and JKGrad observations ([source resolution §8](SOURCE-RESOLUTION.md#8-psi4-compiled-steps-and-fitting-bases), lines 603–620) |
| The prerequisite "five definitions settled from version-matched source" | Still does not hold | Basis normalization |
| P2 runtime identity | Stage 1 dependency | Installed package records, installed-file digests and the loaded Libint library (D1); the printed Psi4 version and Libxc version; the correspondence of installed binaries to the declared archives |
| N2 representation checks | Stage 1 dependency | The s-dftd3 r⁻⁸ exponent and the D3 cutoff treatments; the electronic-state rule items for P2 |
| Other packages of the P2 environment | Not declared | Python, libxc-c, qcengine, simple-dftd3, dftd3-python and the rest, recorded in the run record |
| libxc alignment between the engines | `[GAP]` | Psi4 printed Libxc 7.1.2 at E-01; the CP2K build's libxc is a Stage 1 dependency |
| CP2K installation and build identity | Stage 1 dependency | Unchanged |
| Convergence and P2 agreement | Unchanged, as C4 defines them | N1 refinement ladders, N3 energy calibration and N4 force envelopes (Stage 1a) for P2 in both engines; N7 P2 agreement, with budgets B_E = 1.0e-4 hartree and B_F = 1.0e-4 hartree/bohr per force component, under which P2 is established only if every comparison passes (C4 row 8 and N7). Each comparison is subject to N2's same-state and representation rule, and a missing required diagnostic makes every check that consumes it, N3 to N7, INDETERMINATE and blocking (C4 N2, "Missing diagnostic"). No tolerance or rule is changed |
| Defining ωB97X-D3 reference | `[GAP]`, a Stage 2 gate (C5) | Lin et al., doi:10.1021/ct300715s, not obtained (HTTP 403) |
| C4-j and B3-b | Deferred | Unchanged; neither is a consequence of this decision |
| W1 | Unrun | Needs its own authorization |
| Stage 1, 1a, 1b and 2 | Unauthorized | Stage 1 remains BLOCKED |
| C3 readiness; scope option A | BLOCKED | Unchanged. MS-000 remains a feasibility PASS only |

## 8. Validity conditions

A decision on this packet concerns the object of Section 2 only.
- **Invalidating changes.** A different archive SHA256 of either package; a different subdirectory or platform; a
  different build string or build number; or a rebuilt package under the same name, version and build string. Any of
  these is a different build. Its use for P2 would need its own identification and declaration through C4 §3.
- **A changed binary.** Matching package records are not enough. If the installed Psi4 core library or Libint library
  differs from the corresponding file of the declared archive, and the difference is not identified and explained,
  or if their correspondence cannot be shown, that installation is not used for P2 until the difference is identified
  and reviewed. A difference that indicates a different artifact, such as a rebuilt, patched or replaced binary,
  requires a revision through C4 §3 (candidate D1). Whether installation changes these files is neither assumed nor
  excluded here.
- **The E-01 core digest is historical.** `0d12c8cda49e2cfe75cea563a2fe51889fa61b88c7b5234beb165b9b54805d99` is an
  observation of the E-01 installation. It is neither the declared identity nor a conformance reference, and it was
  never compared with the archive's contents, whose payload member was never opened.
- **The Libint header.** Its installed digest must equal the digest that the Libint package's own path record gives
  (candidate D1).
- **Changed evidence.** If a later record shows that a locator of Section 2 is wrong, the decision's basis must be
  re-examined before it is relied on.
- **Scope.** The declaration is prospective and `osx-arm64` only. It is not a claim of reproducibility on any other
  platform.

## 9. Future revision map

This map lists every record that a future, approved application of option A would change, or explicitly would not.
**No edit in this map is applied in this task.** Where this task changes a record that the map names, the package index
and the freeze record, the change is a status, navigation or digest-refresh edit outside the clauses that the map
addresses.

Three things are kept apart:
- **The candidate bytes.** The two paragraphs of Section 6, bound by SHA256 in the source ledger.
- **The whole-file revision of B2.** The exact revised B2 is not prepared in this task; preparing it is outside this
  task's scope. It would be prepared from the B2 then in force, in the proposal step of C4 §3, and its digest would
  exist before any approval. No digest is asserted for it here.
- **The adopted-reference inventory.** The records that adopt B2 by its whole-file digest (Section 9.2).

Approving the candidate text is not approving a whole file. An approval binds whole files by path and SHA256, and it
cannot cover bytes that no one has seen.

**Placeholders.** Two kinds appear, only in this map and never in the candidate text:
- `[prepared before approval: …]` marks the new B2 digest, the commit from which the revised B2 is prepared, and the
  file name of the new approval record. They are outputs of the proposal step that precedes approval. A person approves
  exact bytes bound to an exact SHA256, as the approvals of C4, N8 and G4 did, so these values must exist before the
  decision. They are absent here only because that step is outside this task.
- `[human-resolved: decision date]` marks genuine post-decision metadata. The decision date, the channel of record and
  the outcome can exist only after a person decides, and they are recorded in the new approval record.

### 9.1 B2 (`docs/ms-001/B2-METHOD-DECLARATION.md`)

| Ref | Clause | Disposition |
|---|---|---|
| B2-a | §6, after the dated source annotation of 2026-09-27 on normalization and compiled steps, before §7 | With option A: insert candidate paragraphs D1 and D2, each preceded by one blank line, and change no other byte |
| B2-b | §6 opening, lines 143–144 (`The declared second engine is Psi4 1.11, the build installed for E-01 (SOURCES [20])`) | No change. It stays accurate; D1 adds the artifact identity and D2 says so |
| B2-c | §6 table, the basis-identity paragraph and its `UNVERIFIED` normalization statement | No change. As with the 2026-09-27 annotation, the `UNVERIFIED` wording stays |
| B2-d | §6 source annotation of 2026-09-27 | No change. It is a dated record |
| B2-e | §8 prerequisite list and its dated annotation, item 3 (`The Libint2 version of the Psi4 build remains open.`) | No change. They are dated records, accurate on their date, as the G4 and N8 approvals left them. Current status is carried by the new approval record, the package index and the freeze record |
| B2-f | §3, including the declared dftd4 source for G4; every other section | No change. The G4 declaration approved at `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` is carried unchanged |

### 9.2 Adopted-reference inventory

An additive annotation of B2 §6 changes B2's whole-file digest. **It therefore breaks every binding that adopts B2
at `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`.** Existing approvals cannot follow new bytes.

| Ref | Record that binds B2 at `aa24a452…` | Kind of binding | Locator | Disposition |
|---|---|---|---|---|
| AR-a | [C4-HUMAN-APPROVAL-02.md](C4-HUMAN-APPROVAL-02.md) | Adoption: C4, B3, C2 and C7 were approved with B2 adopted at this whole-file digest ("References are read as bound") | Lines 48–62; the B2 row is line 55 | The record is not changed, ever. Under option A the same decision must freshly approve C4, B3, C2 and C7 at their unchanged digests with the revised B2 adopted at [prepared before approval: new B2 digest], recorded in the new approval record. Without that, the four records would keep adopting B2 at `aa24a452…` while the revised B2 is in force, and their references to B2 would not be read as bound |
| AR-b | [B2-G4-HUMAN-APPROVAL.md](B2-G4-HUMAN-APPROVAL.md) | Approval of the whole of B2 at this digest ("Every byte of B2 is covered") | Lines 25–45 | The record is not changed, ever. It stays the approval of the G4 declaration. The revised B2 carries that declaration unchanged, but the whole revised file needs its own approval |
| AR-c | [C4-HUMAN-APPROVAL.md](C4-HUMAN-APPROVAL.md) | Adoption of references as they stood at commit `bd3d16a5173b19e3461817171487a106eea3173c` | Line 31 | No change. That environment is already historical ([C4-HUMAN-APPROVAL-02.md](C4-HUMAN-APPROVAL-02.md), "The environment of 2026-09-27 is historical") |
| AR-d | [Freeze record §2](STAGE0-FREEZE-RECORD.md#2-frozen-artifacts), B2 row | Freeze binding, not an adoption | §2 | Refreshed only after approval (FR-e) |
| AR-e | [Export manifest](../../provenance/EXPORT-MANIFEST.md), B2 row | Published-file digest, not an adoption | B2 row | Refreshed with the application |

**How the references of the four records stand.** None of C4, B3, C2 or C7 would change a byte. C4 cites B2 §6 in N2
("subject to the normalization item in B2 §6", line 67) and N3 ("B2 §6 and §8", line 99). C7 §3 names "Psi4 1.11
(B2 §6)" (line 57). B3 and C2 cite B2 §3, §4 and §5 only. After a fresh adoption, the text of each still reads
correctly: the normalization item remains partial, and "Psi4 1.11 (B2 §6)" then refers to the declared build.

**The new approval record** ([prepared before approval: approval record file name]). It follows the pattern of the
two approval records of 2026-09-27 and binds:
- B2 at [prepared before approval: new B2 digest], prepared from [prepared before approval: commit] at which B2 had
  SHA256 `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`, and whether those bytes were committed
  when approved;
- C4, B3, C2 and C7 at their unchanged digests,
  `a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da`,
  `291754f60b49be52e349379c0f80dc0ed4782704e58f00a906997db8d842f955`,
  `aa8425952187d9460a81034cbd98fc5c11108034a9bdda0afd0eb328c410459a` and
  `301fc51755080e8f0e6126436a8e4ec45ba078ed01b81ce55aebabf34bd9a412`, if they are still in force at the decision,
  with the revised B2 adopted;
- a table of the records each approved record adopts, at the digests in force at the decision. For B2 these include
  the records the G4 approval adopted and, newly, this packet, its source ledger, the installed-build audit and the
  recipe metadata audit with its ledger;
- the decision date, the channel of record, the C4 §3 steps, and what the approval does and does not do.

It states that [C4-HUMAN-APPROVAL-02.md](C4-HUMAN-APPROVAL-02.md) and [B2-G4-HUMAN-APPROVAL.md](B2-G4-HUMAN-APPROVAL.md)
are unchanged, that their reference environment is historical for B2 once the revised bytes are in force, and that it
does not update or extend them. The decision may equally be recorded in two records, one for B2 and one for the four
records, as the decision of 2026-09-27 was; the bound digests are the same either way.

### 9.3 Package index and freeze record

| Ref | Record and locator | Kind | Disposition |
|---|---|---|---|
| IX-a | [Package index](README.md), "Open items", five-definitions item | Current state, with dated history | No rewrite of existing lines. With option A, a new dated sub-bullet after the last one, exactly: "*Updated [human-resolved: decision date]:* a person approved a revision of B2 that declares the Psi4 build for P2 in B2 §6 ([prepared before approval: approval record file name]): the conda-forge `osx-arm64` package `psi4-1.11-py314h53d0584_1` with its exactly pinned Libint package `libint-2.13.1-h5a0831b_0`, each identified by archive SHA256. It settles the selection of the P2 build only. Basis normalization remains `PARTIALLY ESTABLISHED`, and the build provenance and runtime conformance of the compiled Psi4 steps remain open. Whether this prerequisite holds depends on the other definitions listed here." |
| IX-b | Package index, Records table | Navigation | With option A, one added row, exactly: "\| B2 approval, P2 build \| [prepared before approval: approval record file name] \| The human approval of the revision of B2 that declares the Psi4 build for P2, with the fresh adoption of the revised B2 by C4, B3, C2 and C7, bound to their paths and SHA256 \|" |
| IX-c | Package index, existing dated paragraphs and sub-bullets | Historical | No change |
| FR-a | [Freeze record](STAGE0-FREEZE-RECORD.md) §1, existing history and approval paragraphs | Historical | No change |
| FR-b | Freeze record §1, a new paragraph after the paragraph on the dftd4 source for G4 | Current state | With option A, exactly: "**Declaration of the Psi4 build for P2 ([human-resolved: decision date]).** A person approved a revision of B2 that declares the Psi4 build for P2 in B2 §6, bound to path `docs/ms-001/B2-METHOD-DECLARATION.md` and SHA256 [prepared before approval: new B2 digest], and, in the same decision, C4, B3, C2 and C7 at their unchanged digests with that B2 adopted ([prepared before approval: approval record file name]). It supersedes, for B2, the bytes approved at SHA256 `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`; the earlier approval records are unchanged. It settles the selection of the P2 build only. Basis normalization remains `PARTIALLY ESTABLISHED`; build provenance, runtime conformance and the P2 runtime identity observations remain open. The revision validates nothing physically, upgrades no evidence label and authorizes no Stage 1 work." |
| FR-c | Freeze record §1, disposition table, B2 and C7 rows, "What remains" | Current state | With option A, appended to the B2 cell: "*[human-resolved: decision date]:* a person approved the declaration of the Psi4 build for P2 in B2 §6 ([prepared before approval: approval record file name]); it settles the selection of the build only, and basis normalization remains partially established." Appended to the C7 cell: "*[human-resolved: decision date]:* the Psi4 build for P2 is declared in B2 §6 ([prepared before approval: approval record file name]); basis normalization remains partially established." |
| FR-d | Freeze record §1, readiness bullet on the five definitions | Current state | With option A, appended after its last dated line: "*[human-resolved: decision date]:* the Psi4 build that P2 uses is declared in B2 §6 ([prepared before approval: approval record file name]); this settles its selection only, basis normalization remains partially established, and this prerequisite does not hold." |
| FR-e | Freeze record §2, bindings | Future freeze binding | Changes only after approval. The B2 row would read: "\| B2 method declaration \| `docs/ms-001/B2-METHOD-DECLARATION.md` \| [prepared before approval: new B2 digest] \| `[AGENT]` declared deviation over `[LIT]` defaults and parameters; `[GAP]` items listed. Revised [human-resolved: decision date] to declare the Psi4 build for P2; the digest bound before was `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` \|". A row for the new approval record is added as a process record, and the package index row is refreshed. The C4, B3, C2 and C7 rows keep their digests, because no byte of those four records changes; their fresh adoption of the revised B2 is recorded in the new approval record, not in their bytes |
| FR-f | Freeze record §5 and §6 (status supplements) | Historical | No change |

### 9.4 Records that stay historical or are not frozen

| Ref | Record | Disposition |
|---|---|---|
| HI-a | [C4](C4-TOLERANCES-AND-CONVERGENCE.md), including its opening Approval bullet that still reads PENDING | No byte changes. The frozen bullet stays as it is; its proposed rewrite, C4-j, stays deferred and is not part of this decision |
| HI-b | [B3](B3-DRIVE-PROTOCOL.md), including its opening reference to "C4 §4" | No byte changes. Its correction, B3-b, stays deferred and is not part of this decision |
| HI-c | The installed-build audit, the recipe metadata audit, their ledgers, the source resolution, the pre-Stage-1 packet and ledger, the G4 proposal, the N8 packet, this packet and its ledger | No change. They are dated records |
| HI-d | `results/e01/` | No change. E-01 stays closed as technically BLOCKED and scientifically INDETERMINATE |
| ST-a | Status surfaces that are not frozen: the root README, `AGENTS.md`, `.agents/RESEARCH-STATE.md`, `docs/SOURCES.md` and the export manifest | Updated with the application as status only, each change stated in the manifest |

## 10. The sequence a decision would follow

1. **Recorded reason (C4 §3, step 1).** The source resolution (§6, line 379) and the installed-build audit (§7,
   lines 142 and 149) record the declaration of the Psi4 build that P2 uses as remaining, and the recipe audit (§5,
   line 134) found that a separate decision package can be prepared. The reason does not refer to agreement with the
   paper. This packet adds no new reason.
2. **Fresh approval by the same roles (step 2).**
   - The method author prepares the exact whole-file bytes of the revised B2, inserting D1 and D2 and nothing else,
     and the bindings of the new approval record, including the adopted-reference inventory of Section 9.2. The new
     B2 digest, the commit and the approval record's file name are fixed at this step, before the person decides.
   - The independent reviewer checks those exact bytes, including that the inserted paragraphs equal the candidate
     digests of the source ledger and that every other byte of B2 is unchanged.
   - A person decides: APPROVE, REQUEST REVISION, DECLINE or DEFER. An approval is recorded in a new approval record;
     every earlier approval record stays as it is.
3. **Revalidation (step 3).** Nothing that the P2 build governs has run, so nothing is repeated. E-01 is not a P2 run
   and is not repeated or reinterpreted.
4. **Retention (step 4).** No P2 result exists, so nothing is retained. The superseded B2 bytes stay identifiable by
   their digest, `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`.
5. **Freeze and status.** The bindings of FR-e are refreshed, and the surfaces of ST-a are updated.

Stage 1 would stay BLOCKED after this sequence, until a separate authorization is given and every other prerequisite
holds.

## 11. Sources and limitations

Every claim above is located in committed public records. The [source ledger](P2-PSI4-BUILD-SOURCE-LEDGER.md)
lists each record with its SHA256 at the baseline commit, the claim locators, and the exact-byte binding of the
candidate text.

- Every recommendation, candidate text, edit and inference in this packet is `[AGENT]`. It is a proposal by the method
  author of this package and never evidence about physics.
- Package and recipe statements are `[LIT]` software provenance, with no chemistry evidence class. Missing evidence is
  `[GAP]`. No evidence label changes.
- Recipe metadata is not proof of compiler inputs, header consumption, source-to-binary correspondence, linkage,
  successful package tests, callability, runtime conformance, numerical agreement, readiness, parity or physical
  validity.
- No installed file, archive, installation or engine was newly read, retrieved, installed or run for this packet.
  Committed public records were its only inputs.
- The candidate text is exact as a proposal. It has not had the independent review that step 2 of C4 §3 requires for
  revised B2 bytes, and no whole-file revision of B2 exists.
- Stage 1 remains BLOCKED and is not authorized.
