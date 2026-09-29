# B2 human approval record: declaration of the Psi4 build for P2

Date of record: 2026-09-28, America/New_York: the date on which a person's answer is recorded
on its receipt by the separate orchestration system that governs this project. This record states that date only. It
states no time of the answer.

This record concerns one package, for a decision by a person directing this project under the revision sequence of [C4
§3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding): a revision of [B2](B2-METHOD-DECLARATION.md) that
declares, in B2 §6, the Psi4 build that P2 uses, together with the fresh adoption of the revised B2 by
[C4](C4-TOLERANCES-AND-CONVERGENCE.md), [B3](B3-DRIVE-PROTOCOL.md), [C2](C2-COUPLING-ROUTE.md) and
[C7](C7-VALIDATION-SET.md) at their unchanged whole-file digests. The declaration is the candidate text of the [P2
build-declaration decision packet, §6](P2-PSI4-BUILD-DECISION-PACKET.md#6-candidate-declaration-unapplied), which the
packet recommends as its option A, an `[AGENT]` proposal. Section 1 gives the outcome and the date of record. The
package is bound to the exact bytes identified below. This record carries no energy, force, gradient, structure or
other physical result, and it adds no scientific claim.

## 1. The decision

| Element | Value |
|---|---|
| Decision | APPROVE, of one package covering B2, C4, B3, C2 and C7 together |
| Date of record | 2026-09-28, America/New_York: the date on which the answer is recorded on its receipt. This record states no time of the answer |
| Records bound | The five records of the next table, each at the SHA256 given there. One record covers the whole package; there is no second record |
| Prepared from | Repository commit `9332b08c5c6c16a69094361000156b848fa6cddc`, at which B2 had SHA256 `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` and C4, B3, C2 and C7 had the SHA256 given below |
| Commit of the bytes put to the decision | The revised B2: none. Its bytes were prepared privately from the commit above and are in no commit at preparation, and writing them into the repository follows only an approval, as for the two approvals recorded on 2026-09-27, whose approved bytes were not committed when they were approved. C4, B3, C2 and C7: committed at the commit above, unchanged. Each record is identified by path and SHA256; a file at one of these paths with any other digest does not carry the bytes bound here |
| Scope | The declaration of the Psi4 build that P2 uses, as a prospective Stage 0 definition of MS-001 scope option B, and the fresh adoption of the revised B2 by the four records that adopted B2 at `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`. Every byte of B2 is covered. No byte of C4, B3, C2 or C7 changes |
| Supersedes | For B2 only, once the revised bytes are in force: the bytes approved at SHA256 `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` ([approval record of the G4 declaration](B2-G4-HUMAN-APPROVAL.md)). The earlier approval records are never changed |

| Record | Path | SHA256 bound | At the commit above |
|---|---|---|---|
| B2 | `docs/ms-001/B2-METHOD-DECLARATION.md` | `6cf0bceb932e53c6395b1c170bd2319beb246108991c2715abf635f223add1e0` (34 036 bytes) | `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` (28 830 bytes), superseded for B2 once the revised bytes are in force |
| C4 | `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` | `a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da` | The same digest. No byte changes; freshly adopted with the revised B2 |
| B3 | `docs/ms-001/B3-DRIVE-PROTOCOL.md` | `291754f60b49be52e349379c0f80dc0ed4782704e58f00a906997db8d842f955` | The same digest. No byte changes; freshly adopted with the revised B2 |
| C2 | `docs/ms-001/C2-COUPLING-ROUTE.md` | `aa8425952187d9460a81034cbd98fc5c11108034a9bdda0afd0eb328c410459a` | The same digest. No byte changes; freshly adopted with the revised B2 |
| C7 | `docs/ms-001/C7-VALIDATION-SET.md` | `301fc51755080e8f0e6126436a8e4ec45ba078ed01b81ce55aebabf34bd9a412` | The same digest. No byte changes; freshly adopted with the revised B2 |

**What an approval in this decision covers.**
- **B2.** B2 as revised: the declaration of the Psi4 build that P2 uses (paragraph D1) and a paragraph on its
  provenance and scope (paragraph D2), added to B2 §6 after the dated source annotation of 2026-09-27 on normalization
  and compiled steps and before §7, each preceded by one blank line. Every other byte of B2 equals its version at the
  commit above. The two paragraphs are the candidate text of the packet, §6, whose exact bytes the
  [packet's source ledger, §4](P2-PSI4-BUILD-SOURCE-LEDGER.md#4-exact-byte-binding-of-the-candidate-text) binds: D1,
  2625 bytes, SHA256 `da52ca797f5cc1831ab9275fdab60749658d74d40716800fc509f0a6773ccfca`; D2, 2579 bytes, SHA256
  `2e74db033dc2364e03f94a2fc4111b215c762e6092d04c1f529d0c3e89ef324c`. They carry no date and no field to be filled in
  later. The date of record is stated here and not in B2.
- **Unchanged in B2.** The §6 opening sentence, which names Psi4 1.11 as the build installed for E-01; the §6 table;
  the basis-identity paragraph with its `UNVERIFIED` normalization statement; the dated source annotation of
  2026-09-27 on normalization and compiled steps; §3, with the declaration of the dftd4 source for G4 approved at
  `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`; and every other section.
- **Dated statements.** B2 §8 keeps its prerequisite list and its dated annotation of 2026-09-27, including item 3,
  "The Libint2 version of the Psi4 build remains open." They are dated records, accurate on their date. The current
  status of the selection of the P2 build is carried by this record, the package index and the freeze record.
- **C4, B3, C2 and C7.** Each is bound at its unchanged whole-file digest, with the revised B2 adopted in place of B2
  at `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`. Without that fresh adoption the four records
  would keep adopting B2 at that digest while the revised B2 is in force, and their references to B2 would not be read
  as bound. Their text still reads correctly. C4's N2 ("subject to the normalization item in B2 §6") and N3 ("B2 §6
  and §8") refer to an item that remains partially established, and C7 §3's "Psi4 1.11 (B2 §6)" then refers to the
  declared build. B3 and C2 cite other sections of B2, none of which changes.
- **Unchanged frozen text.** C4's opening Approval bullet, which still reads that approval by a person is PENDING, and
  B3's opening reference to the revision sequence as "C4 §4" are unchanged. Their proposed corrections, C4-j and B3-b,
  stay deferred and are not part of this decision.

**References are read as bound.** The five records refer to other records. An approval in this decision adopts them at
the digests below. Every digest below is the digest of the committed file at the commit above, except that of the
revised B2, which C4, B3, C2 and C7 adopt at the digest bound in Section 1. Applying the package changes no adopted
record other than B2. An approval does not approve any later state of them and does not separately approve them. Any
later change to the five records, or to what they bind, follows the binding revision sequence of [C4
§3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding).

Adopted by B2:

| Referenced record | Path | SHA256 adopted |
|---|---|---|
| C4 tolerances and convergence, bound in Section 1 of this record | `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` | `a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da` |
| C2 coupling route, bound in Section 1 of this record | `docs/ms-001/C2-COUPLING-ROUTE.md` | `aa8425952187d9460a81034cbd98fc5c11108034a9bdda0afd0eb328c410459a` |
| B3 drive protocol, bound in Section 1 of this record | `docs/ms-001/B3-DRIVE-PROTOCOL.md` | `291754f60b49be52e349379c0f80dc0ed4782704e58f00a906997db8d842f955` |
| C3 provenance wiring | `docs/ms-001/C3-PROVENANCE-WIRING.md` | `cd0ffcc37d40fbb82a0801a2685335c68fdde08e8f6fc6c6d31e3ff76fe2723d` |
| Stage 0 source ledger | `docs/ms-001/SOURCE-LEDGER.md` | `4d46ff84ffe0767f5ded9d202b935836007cd9d4243647bc438353664f44142c` |
| Source resolution record | `docs/ms-001/SOURCE-RESOLUTION.md` | `cc07691b70383a220fd531d3e7476e7964bf862b34b7e33666fb58d4654c7e25` |
| G4 proposal | `docs/ms-001/G4-DFTD4-DECLARATION-PROPOSAL.md` | `1c7b9d4c76a6dea74d023b8e956beea948676e55a2f7c78b61b3712e0806bb83` |
| Pre-Stage-1 source ledger | `docs/ms-001/PRESTAGE1-SOURCE-LEDGER.md` | `9cec2c5b4e4f4c78ac5094dfec40731307ebe3a5d6657487b1943e6d1802be29` |
| Geometry record | `structures/ms-001/README.md` | `4cc6cc42660a0dd439f9d0c018aba0cbdea933b0d734fb163cec2442ac97aba6` |
| MS-000 compute spike | `docs/ms-000/MS-000-COMPUTE-SPIKE.md` | `e5e77015318e06af3338d1fdfaa9f266b040c343befd3d21859b43258ec727b6` |
| P2 build-declaration decision packet | `docs/ms-001/P2-PSI4-BUILD-DECISION-PACKET.md` | `08e5d64f2a8390492692edb3c49c94cbb59135108ad02ca7770cbb55d9ae66bc` |
| P2 build-declaration source ledger | `docs/ms-001/P2-PSI4-BUILD-SOURCE-LEDGER.md` | `bc4cef5438ecce950facea46efe6dff69f43704344327622fa840588f4266a86` |
| Installed-build audit | `docs/ms-001/INSTALLED-BUILD-AUDIT.md` | `43d75ce277099f67c8cc6b682e2e3a7192a6c0305d140a2693f8dcafd3ff9e3f` |
| Recipe metadata audit | `docs/ms-001/RECIPE-METADATA-AUDIT.md` | `cc05c86c032b392205dbe78bef2c5dbc514149e1775394e25a89d2bf5f063789` |
| Recipe metadata source ledger | `docs/ms-001/RECIPE-METADATA-SOURCE-LEDGER.md` | `96015d4669e57f60d09efd46647934ba44ed310d163192b5e4eb6f9ad5bd99eb` |

The first ten rows are the records that B2 adopted at `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`
([approval record of the G4 declaration, §1](B2-G4-HUMAN-APPROVAL.md#1-the-decision)), each at an unchanged digest. The
last five are the records that paragraph D2 newly cites or names: the packet, its source ledger, the installed-build
audit, and the recipe metadata audit with its source ledger. The installed-build audit's own ledger is the pre-Stage-1
source ledger, adopted above.

Adopted by C4, B3, C2 and C7:

| Referenced record | Path | SHA256 adopted |
|---|---|---|
| B2 method declaration, as revised and bound in Section 1 of this record | `docs/ms-001/B2-METHOD-DECLARATION.md` | `6cf0bceb932e53c6395b1c170bd2319beb246108991c2715abf635f223add1e0` |
| C3 provenance wiring | `docs/ms-001/C3-PROVENANCE-WIRING.md` | `cd0ffcc37d40fbb82a0801a2685335c68fdde08e8f6fc6c6d31e3ff76fe2723d` |
| Stage 0 source ledger | `docs/ms-001/SOURCE-LEDGER.md` | `4d46ff84ffe0767f5ded9d202b935836007cd9d4243647bc438353664f44142c` |
| Source resolution record | `docs/ms-001/SOURCE-RESOLUTION.md` | `cc07691b70383a220fd531d3e7476e7964bf862b34b7e33666fb58d4654c7e25` |
| N8 decision packet | `docs/ms-001/N8-DECISION-PACKET.md` | `f726b5bb49c1458b504b7fd0a7e400cf75d36bbd78c2bf9945583414ae42ca92` |
| Geometry record | `structures/ms-001/README.md` | `4cc6cc42660a0dd439f9d0c018aba0cbdea933b0d734fb163cec2442ac97aba6` |
| MS-000 compute spike | `docs/ms-000/MS-000-COMPUTE-SPIKE.md` | `e5e77015318e06af3338d1fdfaa9f266b040c343befd3d21859b43258ec727b6` |

These are the records that C4, B3, C2 and C7 adopted
([record of the N8 revision, §1](C4-HUMAN-APPROVAL-02.md#1-the-decision)), with B2 at its revised digest in place of
`aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`. Every other row is at an unchanged digest.

The frozen geometry files are adopted at their digests in the freeze record §2. The freeze record, the package index,
the approval records, the export manifest and the status surfaces report or bind these records. They are not adopted
as definitions. Where one of the five records cites the freeze record, as C7 §1 does for the digests of the validation
configurations and B2 §8 does for its three categories of open items, the cited rows and categories are not changed by
this revision. B2 cites entries [11] and [20] to [22] of the source catalogue; this revision changes neither those
entries nor B2's citation of them.

**One decision, one record.** The package is put to one decision on B2 and the four records together, and this one
record covers it. No part of the package can be approved on its own. The
[record of the N8 revision](C4-HUMAN-APPROVAL-02.md) and the
[record of the G4 declaration](B2-G4-HUMAN-APPROVAL.md) are unchanged, and this record does not update or extend them.
Their reference environment, in which B2 is adopted and approved at
`aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`, is historical for B2 once the revised bytes are in
force. The environment of the [approval of C4 of 2026-09-27](C4-HUMAN-APPROVAL.md) is already historical
([record of the N8 revision, §1](C4-HUMAN-APPROVAL-02.md#1-the-decision), "The environment of 2026-09-27 is
historical"). This record does not read any earlier approval as having adopted the revised B2.

## 2. The revision sequence of C4 §3

| Step | State |
|---|---|
| 1. Recorded reason | The [source resolution record, §6](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4), of 2026-09-27, leaves open the Libint2 version linked by the Psi4 build that P2 uses. The [installed-build audit, §7](INSTALLED-BUILD-AUDIT.md#7-relation-to-the-normalization-item), records that whether P2 will use the E-01 build is a declaration not made there, and lists the declaration of the Psi4 build that P2 uses as open. The [recipe metadata audit, §5](RECIPE-METADATA-AUDIT.md#5-dispositions-and-prospective-p2-decision), found that a separate prospective P2 build-declaration package could be prepared. The reason does not refer to agreement with the paper. The P2 build-declaration decision packet adds no new reason |
| 2. Fresh approval by the same roles | Roles: the method author proposes the exact bytes above; the independent reviewer checks those bytes, including that the inserted paragraphs equal their bound digests and that every other byte of B2 is unchanged; a person decides. The question is put to the person only after that review. Recorded answer: APPROVE, on 2026-09-28 |
| 3. Revalidation | Nothing that the P2 build governs has run, so nothing is repeated. E-01 is not a P2 run, and it is neither repeated nor reinterpreted |
| 4. Retention of superseded results | Not applicable: no P2 result exists. The superseded B2 stays identifiable by its digest, `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` |

## 3. Channel of record

The question is put to the project's human operator, a person directing this project, through the separate
orchestration system that governs it. It offers four answers for the whole package: approve the exact bytes of B2 and
the fresh adoption of C4, B3, C2 and C7, request a revision, decline, or defer. No part of the package can be approved
on its own. The question is put only after a private approval package has been prepared and independently reviewed.
That package binds the decision to the paths and SHA256 above, states every adaptation of the packet's text and of the
earlier approval records, and states what an approval would and would not do. Recorded answer: APPROVE.

The private approval package and the record of its independent review are not published. This record carries no
personal name and no task, session, reviewer or agent identifier. Agreement between reviewers or agents is never
physical evidence, and publishing this record authorizes nothing further.

## 4. What an approval does and does not do

With an approval, the selection of the Psi4 build that P2 uses is settled by the declaration in B2 §6. Nothing else is
settled.

| It is not | Because |
|---|---|
| A build, linkage, loaded-file or runtime claim | The declaration selects two package archives by digest and sets a conformance condition on a P2 run record. Nothing is installed, built, linked, loaded or run. Which Libint library file a run loads, and whether code loaded at run time changes Libint's normalization flag, are not established |
| Equivalence of builds | A package with another archive digest, another subdirectory or platform, another build string or build number, or a rebuild under the same name, version and build string is a different build. The declaration applies to `osx-arm64` only and claims no reproducibility on another platform |
| Source-to-binary correspondence | The recipe's source archive and patch are metadata of the declared artifact, not a declaration of its compiled source. The compiler, its inputs and the Libint headers used when the Psi4 core was compiled are not recorded. The digest of the E-01 installation's core library is an observation of one installation, never compared with the archive's contents |
| P1 identity provenance or P2 runtime identity | P1 identity provenance, of the GFN0 parameters through CP2K, is untouched and remains within Stage 1. The installed package records, installed-file digests and loaded Libint library of a P2 run are run-record observations within Stage 1 |
| An upgrade of evidence | No evidence label changes. The declaration is `[AGENT]`, over `[LIT]` package identities and recipe metadata ([evidence policy §3](../evidence-policy.md#3-language-model-output)) |
| A conclusion from E-01 | E-01, run in an installation of this build, stopped during conventional (PK) integral setup, before any SCF iteration was printed. Its cause is undiagnosed, and it is closed as technically BLOCKED and scientifically INDETERMINATE. P2 declares the DIRECT algorithm and does not use PK. E-01 is not evidence that P2's DIRECT route will fail on this build, and it is not evidence that it will succeed |
| Authorization | Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized, and Stage 1 remains BLOCKED. No installation, build, engine run or calculation is authorized |
| Readiness | Basis normalization remains `PARTIALLY ESTABLISHED`, so the prerequisite of five definitions settled from version-matched source does not hold. The build provenance and runtime conformance of the compiled Psi4 steps remain open. C3 readiness and scope option A remain BLOCKED |
