# C4 human approval record: MS-001 scope option B, Stage 0 numerical protocol

Date of decision: 2026-09-27.

A person directing this project approved [C4](C4-TOLERANCES-AND-CONVERGENCE.md), the tolerances, acceptance budgets
and numerical-convergence protocol of the MS-001 Stage 0 package under scope option B, as the prospective numerical
protocol of Stage 0. The approval is bound to the exact bytes identified below. This is the public record of that
decision. It carries no energy, force, gradient, structure or other physical result, and it adds no scientific claim.

## 1. The decision

| Element | Value |
|---|---|
| Decision | APPROVE |
| Date | 2026-09-27 |
| Approved record | `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` ([C4](C4-TOLERANCES-AND-CONVERGENCE.md)) |
| Repository commit | `bd3d16a5173b19e3461817171487a106eea3173c` |
| SHA256 of the approved record | `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d` |
| Scope | The prospective numerical protocol of MS-001 scope option B, Stage 0 |
| Limits | Every limit stated in the reviewed decision packet, as listed in Sections 3 and 4 of this record |

The approval covers the whole of C4 as bound: the terms of its opening section; the tolerance table of §1, rows 1 to
11, and the note after it; the numerical-convergence protocol of §2, N1 to N8, including the electronic-state
comparison rule and the frozen but BLOCKED N8 rule with its budget B_P; and the binding revision sequence of §3. The
adopted protocol therefore includes, as written in C4, the requirement that event E1 carry an N6-resolved energy
decrease at the same accepted step as its Si–C bond part (row 3), the blocking treatment of a branch with zero
accepted steps (row 11), and the comparison at checkpoint S of the events E1–E4 under their full criteria (row 11).

**References are read as they stand at the bound commit.** C4 refers to other records, among them B2, B3 and C7 of
this package, the MS-000 compute spike and the Stage 0 source ledger. The approval adopts C4 together with those
references as the referenced records stand at commit `bd3d16a5173b19e3461817171487a106eea3173c`. It does not approve
any later state of a referenced record, and it does not separately approve B2, B3 or C7. Any later change to C4, or to
what it binds, follows the binding revision sequence of
[C4 §3, "Revision sequence (binding)"](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding), which includes
fresh approval by the same roles as the original selection.

## 2. Channel of record

The decision was given by the project's human operator, a person directing this project, through the separate
orchestration system that governs it. The person answered a decision question that offered three paths: approve the
exact bound C4 bytes, request a revision, or defer. The question was put after a private decision packet had been
prepared and independently reviewed. The packet bound the decision to the commit, path and SHA256 above, summarized
the values, rules and open items of C4 with their locators and evidence status, and stated what approval would and
would not do. The person answered with approval.

The private records are not published. As in the [freeze record](STAGE0-FREEZE-RECORD.md) and the
[export manifest](../../provenance/EXPORT-MANIFEST.md), they are identified here by description and SHA256 only.

| Private record | SHA256 |
|---|---|
| Decision packet for the human approval of C4, in its reviewed final form | `2d9db4fb92d9d81ea5f7fc70f6f7d31059a27ca849da713105a7205a7d645810` |
| Canonical record of the independent review of that packet | `de26ce185ce3c957acac70e2c13dcd737312c3f56b93a480d0fda1397735074e` |

The independent review approved the packet as decision support. It assessed the packet against C4 and did not make
or imply the decision, and agreement between reviewers or agents is never physical evidence. This record carries no
personal name and no task, session, reviewer or agent identifier. Publishing it authorizes nothing further.

## 3. What the approval does and does not do

The approval adopts the exact bound C4 definition set as the prospective numerical protocol of scope option B,
Stage 0. With it, Stage 0 is closed as a set of frozen prospective definitions, bound by path and SHA256 in the
[freeze record](STAGE0-FREEZE-RECORD.md). The closure fixes those definitions before any calculation. It is not
readiness for Stage 1, and it gives no authority for Stage 1, Stage 1a or Stage 1b, or for any calculation,
installation or engine run.

The one gate that this decision satisfies is the human approval of C4 (spike §8.3, item C4). No scientific or
readiness gate changed.

| It is not | Because |
|---|---|
| Physical validation | No threshold, budget, structure, pathway, force, energy, stability or feasibility is validated. A stopping criterion is not an accuracy bound, and an acceptance budget is a declaration, not a validated uncertainty (C4, opening section) |
| An upgrade of evidence | No evidence label changes. Every model, setting and threshold stays `[AGENT]`, and every `[SPEC]`, `[GAP]` and `UNVERIFIED` item keeps its label. Output from language models and agreement between agents are never physical evidence ([evidence policy §3](../evidence-policy.md#3-language-model-output)) |
| Authorization of Stage 1, a calculation, an installation or an engine run | The approval authorizes no calculation of any kind, no Stage 1a or Stage 1b work, no installation and no engine run. Stage 1 remains BLOCKED and is not authorized. It needs a separate human authorization together with the prerequisites listed in Section 4 |
| Readiness | C3 readiness and N8 remain BLOCKED, and the five source definitions of Section 4 are not settled |
| Coupling or parity | No coupling route has been demonstrated, and P3b is open. Parity with the benchmark is unknown for every item (B4). Scope option A remains BLOCKED and is not authorized |
| A Stage 2 gate | P1, P2, P3b, C5 and C6 are not established |
| Document acceptance or a scientific gate | Document acceptance, a scientific gate and authorization are separate, and none implies another ([evidence policy §5](../evidence-policy.md#5-separate-acceptances)) |

## 4. Limits that stand

- **Stage 1.** BLOCKED and not authorized, including Stage 1a and Stage 1b. It needs a separate human
  authorization, the closure of the C3 blockers and the five source definitions below. No calculation, installation
  or engine run is authorized.
- **C3 readiness, N8 and scope option A.** Each remains BLOCKED. N8 is blocked pending the record that carries the
  projected gradient GEO_OPT uses, the printed representation of the analytic composite gradient, and the combined
  formatting allowance r = r_(i) + r_(ii), which cannot be defined until both representations are (C4 row 10).
- **Stage 2 gates.** P1, P2, P3b, C5 and C6 are unestablished.
- **Five definitions still to settle from version-matched source.** GFN0 parameter provenance through CP2K (G4);
  CP2K's unit for `OMEGA`; the normalization of single-primitive basis coefficients; the printed representations that
  N8 compares; and whether the compiled Psi4 SCF and gradient steps use any fitting basis under the declared settings.
- **E3 persistence.** The minimum persistence Δd_min = 0.20 Å of imposed d remains an arbitrary `[AGENT]` declaration
  without physical validation (C4 rows 5 and 11).
- **E3(iii).** It remains INDETERMINATE by declaration (C4 row 7).
- **D3 sr8.** CP2K's hard-coded D3 zero-damping sr8 = 1.0 remains a declared deviation (C4 §2, N2; B2).
- **Geometries.** The Stage 0 geometries remain unrelaxed `[AGENT]` models. They are not a model of the benchmark
  geometry and have not been compared with the benchmark authors' coordinates `[GAP]`.
- **Labels and coupling.** Every model, setting and threshold stays `[AGENT]`. No coupling route has been
  demonstrated.

## 5. The frozen opening bullet of C4

The opening Approval bullet of C4 still states that approval by a person is PENDING and that no value in C4 is
approved by a person yet. That bullet is retained unchanged. It is the frozen text of C4 as of the approved digest, and
it was accurate at the bound commit, before the 2026-09-27 human decision.

C4 is not edited, because the approval is bound to its digest
`707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`. Any edit, including a status edit, would produce
bytes that no person approved. For the status of human approval, this record supersedes that bullet. The rest of the
bullet stands: nothing in C4 authorizes Stage 1 or claims readiness, parity or any physical result. The
[freeze record](STAGE0-FREEZE-RECORD.md) and the [export manifest](../../provenance/EXPORT-MANIFEST.md) state the same
qualification.
