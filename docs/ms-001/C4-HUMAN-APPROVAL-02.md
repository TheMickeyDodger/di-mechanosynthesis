# C4 human approval record: revision of N8

Date of record: 2026-09-27, America/New_York. The person's answer was recorded on that date, on its receipt by the
separate orchestration system that governs this project. The time at which the person gave the answer was not
recorded, and this record states none.

A person directing this project approved a revision of [C4](C4-TOLERANCES-AND-CONVERGENCE.md) that defines N8 as
fixed-atom checks on the records of C4 row 10, option O2 of the [N8 decision packet](N8-DECISION-PACKET.md),
together with the consequential revisions of [B3](B3-DRIVE-PROTOCOL.md), [C2](C2-COUPLING-ROUTE.md) and
[C7](C7-VALIDATION-SET.md) that the packet maps. In the same decision the person approved the declaration of the
dftd4 source for G4 in [B2](B2-METHOD-DECLARATION.md), recorded in
[its own approval record](B2-G4-HUMAN-APPROVAL.md). The approval is bound to the exact bytes
identified below. This is the public record of that decision for the four records named here. It carries no energy,
force, gradient, structure or other physical result, and it adds no scientific claim.

## 1. The decision

| Element | Value |
|---|---|
| Decision | APPROVE, of one package covering C4, B3, C2, C7 and B2 together |
| Date of record | 2026-09-27, America/New_York: the date on which the answer was recorded on its receipt. The time at which the person gave it was not recorded |
| Approved records | The four records of the next table, each at its approved SHA256. B2 is approved in the same decision and recorded separately |
| Prepared from | Repository commit `8ed54243a82f04363c7644c30c8584bca2a2d455`, at which each record had its superseded SHA256 |
| Commit of the approved bytes | None at the time of the decision. The approved bytes were prepared privately and were not committed when they were approved. They are identified by path and SHA256; a file at one of these paths with any other digest does not carry the approved bytes |
| Scope | The definition of N8 in C4, and the clauses of B3, C2 and C7 that depend on it, as prospective Stage 0 definitions of MS-001 scope option B. Every byte of the four files is covered; the clauses of C4 other than N8 are unchanged from the bytes approved on 2026-09-27 |
| Supersedes | For N8 only, the definition approved on 2026-09-27 at SHA256 `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d` ([approval record](C4-HUMAN-APPROVAL.md)). That record is unchanged |

| Record | Path | Approved SHA256 | Superseded SHA256 |
|---|---|---|---|
| C4 | `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` | `a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da` | `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d` |
| B3 | `docs/ms-001/B3-DRIVE-PROTOCOL.md` | `291754f60b49be52e349379c0f80dc0ed4782704e58f00a906997db8d842f955` | `79aceedc391afd949660271aed23e2f48da7da8078b288427f3db5219dccea7a` |
| C2 | `docs/ms-001/C2-COUPLING-ROUTE.md` | `aa8425952187d9460a81034cbd98fc5c11108034a9bdda0afd0eb328c410459a` | `45401c8f45bfbb82798765bfdf7628640a160c2b1129f7afcdc1d2ee587b4c8e` |
| C7 | `docs/ms-001/C7-VALIDATION-SET.md` | `301fc51755080e8f0e6126436a8e4ec45ba078ed01b81ce55aebabf34bd9a412` | `05c8e75215b2233ae77f239f42297d83e9a7129c87b0419f9abdccab728400a4` |

**What was approved.**
- **C4.** Row 10, third and fourth columns; the paragraph after the tolerance table; and N8 in §2, whose
  retained-component comparison is removed. Their text is candidates C1 to C4 of the N8 decision packet, §4, not the
  earlier candidate text of [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md), §5. A paragraph after the N8
  rule states the six Stage 1 observations of the packet's §5, which are required before any N8 outcome, and the
  consequence if one fails or cannot be made.
- **B3, C2 and C7.** B3 §3, row "Constraint projection"; C2 §5, item 6; and C7 §2, the N8 bullet, as the packet's
  edit map gives them (§6.2).
- **Unchanged.** Every other byte of the four records equals its superseded version. C4's opening Approval bullet,
  which still states that approval by a person is PENDING, is unchanged; for the status of human approval this record
  and the record of 2026-09-27 supersede it. Its proposed rewrite is unresolved. B3's opening reference to the
  revision sequence as "C4 §4" is unchanged; its proposed correction to "C4 §3" is unresolved.

**References are read as bound.** The four records refer to other records. The approval adopts them at the digests
below, which are the digests in force once the one approved package is applied. It does not approve any later state
of them and does not separately approve them. Any later change to the four records, or to what they bind, follows the
binding revision sequence of [C4 §3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding).

| Referenced record | Path | SHA256 adopted |
|---|---|---|
| B2 method declaration, as approved in the same decision | `docs/ms-001/B2-METHOD-DECLARATION.md` | `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` |
| C3 provenance wiring | `docs/ms-001/C3-PROVENANCE-WIRING.md` | `cd0ffcc37d40fbb82a0801a2685335c68fdde08e8f6fc6c6d31e3ff76fe2723d` |
| Stage 0 source ledger | `docs/ms-001/SOURCE-LEDGER.md` | `4d46ff84ffe0767f5ded9d202b935836007cd9d4243647bc438353664f44142c` |
| Source resolution record | `docs/ms-001/SOURCE-RESOLUTION.md` | `cc07691b70383a220fd531d3e7476e7964bf862b34b7e33666fb58d4654c7e25` |
| N8 decision packet | `docs/ms-001/N8-DECISION-PACKET.md` | `f726b5bb49c1458b504b7fd0a7e400cf75d36bbd78c2bf9945583414ae42ca92` |
| Geometry record | `structures/ms-001/README.md` | `4cc6cc42660a0dd439f9d0c018aba0cbdea933b0d734fb163cec2442ac97aba6` |
| MS-000 compute spike | `docs/ms-000/MS-000-COMPUTE-SPIKE.md` | `e5e77015318e06af3338d1fdfaa9f266b040c343befd3d21859b43258ec727b6` |

The frozen geometry files are adopted at their digests in the freeze record §2. The freeze record, the package index,
the approval records, the export manifest and the status surfaces report or bind these records. They are not adopted
as definitions. Where an approved record cites the freeze record, as C7 §1 does for the digests of the validation
configurations, the cited rows are not changed by this revision.

**One decision, two records.** The person approved one package: these four records and B2 together. B2 is adopted
here at the digest that the same decision approved. Each approval record covers its own records only: this record does
not approve B2, and the record of B2 does not approve the four records above. No part of the package was approved on
its own.

**The environment of 2026-09-27 is historical.** The [C4 human approval record, §1](C4-HUMAN-APPROVAL.md#1-the-decision)
approved C4 at SHA256 `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`, with its references "as the referenced
records stand at" commit `bd3d16a5173b19e3461817171487a106eea3173c`, and states that it "does not approve any later
state of a referenced record". That approval, and its environment, are historical once these bytes are in force. This
approval does not update or extend that environment, and it does not read the earlier approval as having adopted any
reference adopted here. Two of those references had already changed before this decision: B2 and the Stage 0 source
ledger. This approval adopts their current states in its own right.

## 2. The revision sequence of C4 §3

| Step | State |
|---|---|
| 1. Recorded reason | Recorded on 2026-09-27 in [C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md), §1. The N8 decision packet adds no new reason |
| 2. Fresh approval by the same roles | The method author proposed the exact bytes above, the independent reviewer checked those bytes, and a person approved them in an answer recorded on 2026-09-27. This record is that approval |
| 3. Revalidation | Nothing that N8 governs has run, so nothing is repeated |
| 4. Retention of superseded results | Not applicable: no N8 result exists. The superseded records stay identifiable by the digests above |

## 3. Channel of record

The decision was given by the project's human operator, a person directing this project, through the separate
orchestration system that governs it. The person answered a decision question that offered three paths for the whole
package: approve the exact bytes of all five files, request a revision, or defer. No part of the package could be
approved on its own. The question was put after a private approval package had been prepared and independently
reviewed. The package bound the decision to the paths and SHA256 above and of B2, stated every adaptation of the
packet's and the proposal's texts and what approval would and would not do. The person answered with approval.

| Private record | SHA256 |
|---|---|
| Approval package for the revisions of N8 and G4, in its reviewed final form | `5b7e2bc3d0bc0a61284fc63268775d016a49fb4b5203d38fe39b708779ef13a5` |
| Canonical record of the independent review of that package | `107ff61a34ab90b8556e51a26ee929de716b4ec206ea42ec7b07743146249699` |

The private records are not published. This record carries no personal name and no task, session, reviewer or agent
identifier. Agreement between reviewers or agents is never physical evidence, and publishing this record authorizes
nothing further.

## 4. What the approval does and does not do

The approval adopts the exact bytes above as the prospective definition of N8 of scope option B, Stage 0, with its
consequential clauses. N8 has not been run and has no outcome.

| It is not | Because |
|---|---|
| Physical validation | No threshold, budget, structure, force, energy or pathway is validated. The fixed-atom checks test printed values: a zero significand shows that a component printed as zero, and identical ten-decimal strings show equality at printed precision, never in memory |
| An upgrade of evidence | No evidence label changes. Every model, setting and threshold stays `[AGENT]`, and every `[SPEC]`, `[GAP]` and `UNVERIFIED` item keeps its label ([evidence policy §3](../evidence-policy.md#3-language-model-output)) |
| A relaxation | The retained-component comparison and its budget B_P = 1.0e-6 hartree/bohr are no longer used by N8. No N8 result exists and N8 governs nothing that has run, so this is a change of coverage, not a relaxation. That the constraint leaves the retained components unchanged rests on version-matched source reading alone and is not tested at run time |
| An outcome | The six Stage 1 observations of C4 are outstanding. If one fails or cannot be made, N8 is INDETERMINATE on that build until the definition is revised through C4 §3 |
| Authorization of Stage 1, a calculation, an installation or an engine run | None is authorized. Stage 1, Stage 1a and Stage 1b remain BLOCKED and are not authorized |
| Readiness | C3 readiness remains BLOCKED. The prerequisite of five definitions settled from version-matched source does not hold while basis normalization is partially established |
| Coupling or parity | No coupling route has been demonstrated, P3b is open and parity with the benchmark is unknown. Scope option A remains BLOCKED |

## 5. B2 is not edited for this revision

The N8 item of the prerequisite list of [B2 §8](B2-METHOD-DECLARATION.md#8-what-stays-open), "The printed
representations that N8 compares (C4, row 10)", is settled by the definition approved here. B2 is not edited for that
purpose. Its §8 list and its dated annotation of 2026-09-27 are dated records, accurate on their dates, and they stay
as they are. The current status of N8 is carried by this record, the package index and the freeze record. N8 has not
been run, and its Stage 1 observations are outstanding.
