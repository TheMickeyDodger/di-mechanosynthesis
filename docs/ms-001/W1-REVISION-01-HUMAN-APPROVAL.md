# W1 human approval record: specification revision 01

Date of record: 2026-10-04: the date on which a person's answer is recorded on its receipt by the separate
orchestration system that governs this project. This record states that date only. It states no time of the answer.

This record concerns one decision by a person directing this project: revision 01 of
[C3-WIRING-TEST-PROPOSAL.md](C3-WIRING-TEST-PROPOSAL.md), the specification of the non-chemistry provenance wiring test
W1. The revision is the one prepared and bound to exact bytes by the
[W1 revision decision packet](W1-REVISION-DECISION-PACKET.md), whose recommended combination is an `[AGENT]`
proposal. Section 1 gives the outcome and the date of record, and Section 2 records how the approved bytes were
applied. This record carries no energy, force, gradient, structure or other physical result, and it adds no
scientific claim. It is a process record, and no evidence class applies to it.

## 1. The decision

The recorded answer is this one line:

```
W1-REVISION-01 APPROVE 29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347
```

It has the APPROVE form of the [packet, §11](W1-REVISION-DECISION-PACKET.md#11-decision), and its digest equals the
revised SHA256 bound in the packet's [§9](W1-REVISION-DECISION-PACKET.md#9-bound-bytes-and-the-application-proof) and
§11.

| Element | Value |
|---|---|
| Decision | APPROVE, of revision 01 of the W1 specification as one whole file |
| Date of record | 2026-10-04: the date on which the answer is recorded on its receipt. This record states no time of the answer |
| Record bound | `docs/ms-001/C3-WIRING-TEST-PROPOSAL.md`, at the revised SHA256 of the next table. One record covers the decision; there is no second record |
| Prepared from | Repository commit `af7a8983a7a4c3d52c882ff9a2f63923823e85f6`, at which the specification had the base SHA256 of the next table |
| Commit of the approved bytes | None. The revised bytes were prepared privately from the commit above and were in no commit when they were approved. Writing them into the repository followed only the approval (Section 2). A file at this path with any other digest does not carry the bytes bound here |
| Scope | The text of the W1 specification. Every byte of the file is covered |
| Supersedes | The specification of 2026-09-27, at the base SHA256 below, as the specification in force. The base bytes stay identifiable by that digest |

| Artifact | SHA256 | Bytes |
|---|---|---|
| Base specification, in force until this approval | `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158` | 45 998 |
| Revised specification, revision 01, approved | `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347` | 70 753 |
| Patch from base to revised, a unified diff | `ed8a0dfd9891709c65c24eb4ec28ea80dff0fd4a54d94d0be6813b9ca3b450a7` | 52 085 |

The patch is retained privately, as the packet states, and is not published as a file.

**What the approval covers.** Following the packet's §11, the person approved the revised bytes as the text of
`docs/ms-001/C3-WIRING-TEST-PROPOSAL.md`, replacing the base bytes. That includes:
- the relaxation for one platform-injected environment name, `__CF_USER_TEXT_ENCODING`, declared before any run and
  permitted in the interpreter and payload records only, never in the launcher record;
- the identity of the two driver files as untracked files captured by content, with no requirement that they be
  tracked at any commit;
- the F1 capture contract, with its stated limits, including the absence of any executed-code guarantee;
- the seven coupled declarations: the index state with a bounded Git configuration, the `-B` bytecode policy, the
  user-level observation, and the declared `code_identity`, `fixture_diff` and sidecar contents.

**The revision's own header.** The approved bytes describe revision 01 as "proposed 2026-10-04" and state that it is
in force only after a person has approved those exact bytes and the approval is recorded. This record is that
recording, so from it revision 01 is the specification in force. The header is not edited, because an edit would
create bytes that no person approved.

## 2. Application

The approved bytes were applied on 2026-10-04 under this approval, as the first step of the packet's §11 sequence.
The application was fail-closed. Before anything was written, each of these was checked, and each held:
- the live specification had the base SHA256 and size above;
- the privately retained revised file had the revised SHA256 and size above;
- the privately retained patch had the patch SHA256 and size above;
- the decision packet was unchanged;
- the base bytes with the patch applied reproduced the revised SHA256 and size, byte for byte equal to the retained
  revised file.

The retained revised file was then written over the specification as one whole file. Read back, the specification
has the revised SHA256 and 70 753 bytes, and it is byte-identical to the retained revised file. No byte was changed
by editing: the text in force is exactly the approved text. The check records are retained privately.

The application changed no other record of the decision:
- The [decision packet](W1-REVISION-DECISION-PACKET.md) is unchanged. Its statements that nothing is chosen, approved
  or applied, and its replacement text marked UNAPPLIED, are accurate as of its date, 2026-10-04, before this
  decision.
- The [first W1 pre-run determination](W1-PRE-RUN-DETERMINATION.md) and its
  [machine-readable outcome](w1-outcome.json) are unchanged. They remain the result of a determination under the base
  specification of 2026-09-27, and they are not rewritten to describe the revised text.
- C4, including its opening Approval bullet, every earlier approval record and every frozen Stage 0 definition are
  unchanged.

Nothing was committed or pushed. The applied specification is a change of the working tree only.

## 3. Channel of record

The question was put to the project's human operator, a person directing this project, through the separate
orchestration system that governs it, after the packet had been independently reviewed. The packet offers three
answers in a fixed one-line form: approve the exact revised bytes by their digest, reject, or request changes, and it
states that no response is not a decision. Recorded answer: APPROVE, in the line quoted in Section 1.

The private records of the question, of its review and of the application are not published. This record carries no
personal name and no task, session, reviewer or agent identifier. Agreement between reviewers or agents is never
physical evidence, and publishing this record authorizes nothing further.

## 4. What the approval does and does not do

With the approval, the text of the W1 specification is settled as revision 01. Nothing else is settled.

| It is not | Because |
|---|---|
| Readiness, parity or physical validation | W1 is a non-chemistry software wiring test, and it has not run. A pass would be software wiring evidence only |
| A determination that W1 can be executed | The revised text had had no executability determination when it was approved ([packet, §10.1](W1-REVISION-DECISION-PACKET.md#101-residual-risks-and-uncertainties)). A renewed determination is a separate step, recorded in the [second W1 pre-run determination](W1-PRE-RUN-DETERMINATION-02.md) |
| A prediction | A revised W1 is not predicted to pass |
| Authorization to run W1 | A run, the writing of its two driver files, the creation of an AiiDA profile, computer, code or job, any installation and any commit each need a separate authorization by a person |
| Authorization of any stage | Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized, and Stage 1 remains BLOCKED. Scope option A remains BLOCKED |
| Closure of a C3 blocker | No C3 blocker is closed. C3 readiness remains BLOCKED |
| An upgrade of evidence | No evidence label changes. The revision is `[AGENT]` text over `[LIT]` aiida-core source facts and the project's software observations ([evidence policy §3](../evidence-policy.md#3-language-model-output)) |
| A change elsewhere | Basis normalization remains PARTIALLY ESTABLISHED. E-01 remains technically BLOCKED and scientifically INDETERMINATE. C4-j and B3-b remain deferred |

## 5. What follows

The packet's §11 sets the order after an approval:
1. The approved bytes are applied and recorded under that authority. This record and Section 2 complete this step.
2. Executability is determined again under the revised text. The
   [second W1 pre-run determination](W1-PRE-RUN-DETERMINATION-02.md) does this. It reaches no W1 run.
3. Only then is a separately authorized W1 run sought. This record does not seek or grant it.
