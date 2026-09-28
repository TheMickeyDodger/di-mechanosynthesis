# B2 human approval record: declaration of the dftd4 source for G4

Date of record: 2026-09-27, America/New_York. The person's answer was recorded on that date, on its receipt by the
separate orchestration system that governs this project. The time at which the person gave the answer was not
recorded, and this record states none.

A person directing this project approved a revision of [B2](B2-METHOD-DECLARATION.md) that declares the dftd4 source
of the declared CP2K 2026.2 route, the source-definition part of G4, in B2 §3. The declaration is the tblite route
recommended in the [G4 proposal](G4-DFTD4-DECLARATION-PROPOSAL.md#6-recommendation-and-candidate-declaration). In the
same decision the person approved the revision of N8 in C4, B3, C2 and C7, recorded in
[its own approval record](C4-HUMAN-APPROVAL-02.md). The approval is bound to the exact bytes
identified below. This is the public record of that decision for B2. It carries no energy, force, gradient,
structure or other physical result, and it adds no scientific claim.

## 1. The decision

| Element | Value |
|---|---|
| Decision | APPROVE, of one package covering C4, B3, C2, C7 and B2 together |
| Date of record | 2026-09-27, America/New_York: the date on which the answer was recorded on its receipt. The time at which the person gave it was not recorded |
| Approved record | `docs/ms-001/B2-METHOD-DECLARATION.md` ([B2](B2-METHOD-DECLARATION.md)). C4, B3, C2 and C7 are approved in the same decision and recorded separately |
| SHA256 of the approved record | `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` |
| Prepared from | Repository commit `8ed54243a82f04363c7644c30c8584bca2a2d455`, at which B2 had SHA256 `022e4e8f10f8e2b29fafb1b6a38c6150760f0d5048923f6699192e5d9df77a1a` |
| Commit of the approved bytes | None at the time of the decision. The approved bytes were prepared privately and were not committed when they were approved. They are identified by path and SHA256; a file at this path with any other digest does not carry the approved bytes |
| Scope | The declaration of the dftd4 source of the declared CP2K 2026.2 route, as a prospective Stage 0 definition of MS-001 scope option B. Every byte of B2 is covered |

**What was approved.** B2 as revised: a declaration of the dftd4 source and a paragraph on its provenance and scope,
added to B2 §3 after the dated source annotation of 2026-09-27 on G4. Every other byte of B2 equals its version at the
commit above.
- **The declaration** has three separate parts, the archive identity, the patch identity and the dependency
  resolution, and a fail-closed condition on the build's own configure record. Its text is the candidate declaration
  of the G4 proposal, §6, without that candidate's parenthesis for an approval date. The date on which the approval was
  recorded is stated here and not in B2, so that the approved bytes carry no date and no field to be filled in later.
- **The whole record.** The approval covers B2 as bound, including its four dated source annotations of 2026-09-27.
  Those annotations were added after the approval of C4 on 2026-09-27, which adopted B2 only as it stood at the
  commit that approval binds. They are not rewritten or re-dated.
- **Dated statements.** B2 §8 keeps its prerequisite list and its dated annotation of 2026-09-27, including the
  statement that the dftd4 source was then to be declared. They are dated records, accurate on their dates. The
  current status of G4 is carried by this record, the package index and the freeze record.

**References are read as bound.** B2 refers to other records. The approval adopts them at the digests below, which
are the digests in force once the one approved package is applied. It does not approve any later state of them and
does not separately approve them. Any later change to B2, or to what it binds, follows the binding revision sequence
of [C4 §3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding).

| Referenced record | Path | SHA256 adopted |
|---|---|---|
| C4 tolerances and convergence, as approved in the same decision | `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` | `a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da` |
| C2 coupling route, as approved in the same decision | `docs/ms-001/C2-COUPLING-ROUTE.md` | `aa8425952187d9460a81034cbd98fc5c11108034a9bdda0afd0eb328c410459a` |
| B3 drive protocol, as approved in the same decision | `docs/ms-001/B3-DRIVE-PROTOCOL.md` | `291754f60b49be52e349379c0f80dc0ed4782704e58f00a906997db8d842f955` |
| C3 provenance wiring | `docs/ms-001/C3-PROVENANCE-WIRING.md` | `cd0ffcc37d40fbb82a0801a2685335c68fdde08e8f6fc6c6d31e3ff76fe2723d` |
| Stage 0 source ledger | `docs/ms-001/SOURCE-LEDGER.md` | `4d46ff84ffe0767f5ded9d202b935836007cd9d4243647bc438353664f44142c` |
| Source resolution record | `docs/ms-001/SOURCE-RESOLUTION.md` | `cc07691b70383a220fd531d3e7476e7964bf862b34b7e33666fb58d4654c7e25` |
| G4 proposal | `docs/ms-001/G4-DFTD4-DECLARATION-PROPOSAL.md` | `1c7b9d4c76a6dea74d023b8e956beea948676e55a2f7c78b61b3712e0806bb83` |
| Pre-Stage-1 source ledger | `docs/ms-001/PRESTAGE1-SOURCE-LEDGER.md` | `9cec2c5b4e4f4c78ac5094dfec40731307ebe3a5d6657487b1943e6d1802be29` |
| Geometry record | `structures/ms-001/README.md` | `4cc6cc42660a0dd439f9d0c018aba0cbdea933b0d734fb163cec2442ac97aba6` |
| MS-000 compute spike | `docs/ms-000/MS-000-COMPUTE-SPIKE.md` | `e5e77015318e06af3338d1fdfaa9f266b040c343befd3d21859b43258ec727b6` |

The frozen geometry files are adopted at their digests in the freeze record §2. The freeze record, the package index,
the approval records, the export manifest and the status surfaces report or bind B2. They are not adopted as
definitions. B2 §8 cites the freeze record for its three categories of open items, and B2 cites entries [11] and [20]
to [22] of the source catalogue; this revision changes neither those categories nor those entries.

**One decision, two records.** The person approved one package: B2 and the four records of the N8 revision together.
C4, C2 and B3 are adopted here at the digests that the same decision approved. Each approval record covers its own
records only: this record does not approve C4, B3, C2 or C7, and the record of the N8 revision does not approve B2.
No part of the package was approved on its own. The approval of C4 of 2026-09-27, with its references as they stood
at commit `bd3d16a5173b19e3461817171487a106eea3173c`, is historical once the new C4 bytes are in force; this approval
does not update or extend it, and does not read it as having adopted this B2.

## 2. The revision sequence of C4 §3

| Step | State |
|---|---|
| 1. Recorded reason | The [source resolution record, §4](SOURCE-RESOLUTION.md#4-g4-gfn0-parameter-provenance-through-cp2k), of 2026-09-27, found that the CP2K 2026.2 release does not fix the dftd4 source a build uses, and B2 §3 recorded a declaration of that source as remaining. The G4 proposal of the same date compared the two routes |
| 2. Fresh approval by the same roles | The method author proposed the exact bytes above, the independent reviewer checked those bytes, and a person approved them in an answer recorded on 2026-09-27. This record is that approval |
| 3. Revalidation | Nothing that the dftd4 source governs has been built or run, so nothing is repeated |
| 4. Retention of superseded results | Not applicable: no result exists. The superseded B2 stays identifiable by its digest above |

## 3. Channel of record

The decision was given by the project's human operator, a person directing this project, through the separate
orchestration system that governs it. The person answered a decision question that offered three paths for the whole
package: approve the exact bytes of all five files, request a revision, or defer. No part of the package could be
approved on its own. The question was put after a private approval package had been prepared and independently
reviewed. The package bound the decision to the path and SHA256 above and of C4, B3, C2 and C7, stated every
adaptation of the proposal's and the packet's texts and what approval would and would not do. The person answered
with approval.

| Private record | SHA256 |
|---|---|
| Approval package for the revisions of N8 and G4, in its reviewed final form | `5b7e2bc3d0bc0a61284fc63268775d016a49fb4b5203d38fe39b708779ef13a5` |
| Canonical record of the independent review of that package | `107ff61a34ab90b8556e51a26ee929de716b4ec206ea42ec7b07743146249699` |

The private records are not published. This record carries no personal name and no task, session, reviewer or agent
identifier. Agreement between reviewers or agents is never physical evidence, and publishing this record authorizes
nothing further.

## 4. What the approval does and does not do

With this approval the source-definition part of G4 is settled by the declaration in B2 §3.

| It is not | Because |
|---|---|
| A build, linkage or runtime claim | The declaration names archives, patches and a dependency-resolution condition. Whether a build conforms is shown only by its own configure record, as the declaration requires. Nothing is built, linked or run |
| Equivalence of builds | The dftd4 source that CP2K's GFN0 path was traced to call has identical text on both toolchain routes. That is text identity of a traced source subset, not functional equivalence of differently patched, configured and resolved builds |
| P1 identity provenance | The loaded parameter bytes, the linked dftd4 library and the D4 environment settings of a run remain P1 observations within Stage 1. The `[GAP]` of G4 for P1 stands |
| An upgrade of evidence | No evidence label changes. The declaration is `[AGENT]`, over `[LIT]` archive, patch and toolchain identities ([evidence policy §3](../evidence-policy.md#3-language-model-output)) |
| Authorization of Stage 1, an installation, a build or an engine run | None is authorized. Stage 1, Stage 1a and Stage 1b remain BLOCKED and are not authorized |
| Readiness | The prerequisite of five definitions settled from version-matched source does not hold while basis normalization is partially established. C3 readiness remains BLOCKED |
| Upstream correspondence | Whether the CP2K-hosted archive bytes equal an upstream release asset of dftd4 or tblite was not examined |
