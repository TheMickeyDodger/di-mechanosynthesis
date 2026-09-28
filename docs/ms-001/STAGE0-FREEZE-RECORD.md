# MS-001 Stage 0 freeze record (scope option B)

This record binds every Stage 0 definition and machine-readable input of MS-001 scope option B by path, SHA256 and
evidence label, and gives the disposition of each Stage 0 item. It does not list its own digest; the export
manifest does.

Evidence labels follow the [evidence policy](../evidence-policy.md). `[AGENT]` marks a proposal of this project,
never physical evidence. `[LIT]` marks a fact taken from a cited source. `[SPEC]` marks a stated hypothesis.
`[GAP]` marks an input that is unavailable. No file here contains an energy, force, gradient, optimized structure
or any other physical result.

## 1. Disposition

**Review history.** The independent review of this package recorded the canonical decision REJECT, substantively
REVISE, with Stage 1 BLOCKED. C1 was accepted. C2, C3, C4, C7, B1, B2 and B3 were returned for correction, with C3
readiness BLOCKED and B1 needing documentation changes only. The corrections the review required are made in the
records bound below, with no calculation and no geometry regeneration.

A renewed independent review of the corrected package again recorded the canonical decision REJECT. It required five
further corrections: the Psi4 guess and fitting-basis treatment (B2, C4); the zero-accepted-step cases of the drive
(B3, C7, C4); the separation of the geometric Si–C trigger from event E1, which keeps its N6 energy criterion (B3,
C7, C4); a source-count wording in `docs/SOURCES.md`; and this record and the export manifest. They are made in the
records bound below, again with no calculation and no geometry regeneration.

A further independent review again recorded the canonical decision REJECT, for one remaining defect. It accepted C1;
C2, with its capability gaps disclosed and P3b unestablished; C3, as a reviewed partial demonstration with readiness
BLOCKED; B1, as an `[AGENT]` model definition with no physical validation; B2, with explicit prerequisite blockers and
no claim of method readiness; and the geometry and validation definitions of C7. It found no integrity regression. The
defect was that the checkpoint S comparison had been replaced by a match of geometric lists. The correction restored
the comparison of the inherited events E1–E4 under their full criteria, while checkpoint selection stays geometric
(B3 §5, C7 §4, C4 row 11).

A later independent review again recorded the canonical decision REJECT, for one semantic gap. It found the
inventory, the freeze bindings, the manifest and the protected bytes all matching, and it accepted the rest of the
checkpoint S definition. The gap was that E3 was defined at a single step, while spike §8.4 requires the pendent state
to exist over a finite z range, so a match of isolated E3 hits could have released a segment. The correction made
here declares the persistence prospectively, as an `[AGENT]` declaration: a minimum span Δd_min = 0.20 Å of imposed
d, the first step of the span as the occurrence, an isolated hit as not observed, and a span that cannot be
established inside the compared interval as INDETERMINATE (B3 §5, C7 §4, C4 rows 5 and 11).

The latest independent review, of the package as corrected for that gap, recorded the canonical decision APPROVE.
It accepted the corrected definitions of C1, C2, C3, C4, C7, B1, B2 and B3, with the qualifications given per item
below, and Lead acceptance is recorded. As of 2026-09-26, human approval of C4 was still PENDING, and Stage 0 was
not closed; the next paragraph records the approval. The acceptance is of definitions only. It validates nothing
physically: the minimum persistence Δd_min = 0.20 Å, for
example, remains an arbitrary `[AGENT]` declaration without physical validation. It changes no `[AGENT]`, `[SPEC]`,
`[GAP]` or `UNVERIFIED` label. A later status-only revision, recorded in the export manifest, changed status
sentences only: in this record and, among the artifacts bound in Section 2, in the package index, the geometry record
document and the opening Approval bullet of C4, whose digests there are refreshed. Every other byte of C4, and every
other bound artifact, is byte-identical to the reviewed version. The private review records are not published.

**Human approval of C4.** On 2026-09-27 a person approved C4 as the prospective numerical protocol of scope option B,
Stage 0, bound to commit `bd3d16a5173b19e3461817171487a106eea3173c`, path
`docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` and SHA256
`707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`, the digest bound in Section 2, which does not
change. The decision, its channel of record and its limits are recorded in the
[C4 human approval record](C4-HUMAN-APPROVAL.md). The approval adopts C4 with the records it references as they stood
at that commit, and any later change to C4 or to what it binds follows its binding revision sequence
([C4 §3](C4-TOLERANCES-AND-CONVERGENCE.md#3-revision-sequence-binding)). It validates nothing physically, upgrades no
evidence label, and authorizes no Stage 1, Stage 1a or Stage 1b work and no calculation, installation or engine run.
The one gate it satisfies is the human approval of
C4; no scientific or readiness gate changed. C4 itself is byte-identical, and its opening Approval bullet still states
that approval by a person is PENDING. That bullet is retained unchanged as the frozen text of the approved digest,
accurate at the bound commit, before the 2026-09-27 human decision, and it is superseded by the approval record. It
is not edited, because any edit would create bytes that no person approved.

**Source resolution (2026-09-27).** The five source definitions required before Stage 1 were read from
version-matched CP2K 2026.2 and Psi4 v1.11 source ([source resolution record](SOURCE-RESOLUTION.md#3-dispositions)).
- **`OMEGA` and the compiled Psi4 steps.** `ESTABLISHED FROM VERSION-MATCHED SOURCE`. The first covers CP2K's unit
  and conversion semantics only. The second covers the tagged-source behaviour only; the installed binary's build
  provenance and runtime conformance remain open.
- **G4, basis normalization and the N8 representations.** `PARTIALLY ESTABLISHED`.
- **N8.** It remains BLOCKED and has not been run. Options for a decision on its definition under C4 §3 are recorded
  as a proposal, not applied and not approved ([C4-PROPOSED-REVISION-01.md](C4-PROPOSED-REVISION-01.md)).
- **What changed.** Those two records are new and are not Stage 0 definitions, so they are not bound in Section 2.
  B2 received dated source annotations only, and its digest, with those of the source ledger and the package index,
  is refreshed in Section 2.
- **What did not change.** No declared value, label, gate or C4 byte changed, and Stage 1 remains BLOCKED and
  unauthorized.

**Revision of C4 (2026-09-28).** A person approved a revision of C4 that defines N8 as
fixed-atom checks, bound to path `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` and SHA256
`a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da` ([C4-HUMAN-APPROVAL-02.md](C4-HUMAN-APPROVAL-02.md)). The
approved bytes were prepared from commit `8ed54243a82f04363c7644c30c8584bca2a2d455` and were not committed when they were approved. The same
approval covers the consequential revisions of B3, C2 and C7, bound in Section 2. It supersedes, for N8 only, the
definition approved on 2026-09-27 at SHA256 `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`. That approval
record is unchanged. N8 has not been run. The revision validates nothing physically, upgrades no evidence label and
authorizes no Stage 1 work.

**Declaration of the dftd4 source for G4 (2026-09-28).** A person approved a revision of B2
that declares the dftd4 source of the declared CP2K 2026.2 route in B2 §3, bound to path
`docs/ms-001/B2-METHOD-DECLARATION.md` and SHA256 `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f`
([B2-G4-HUMAN-APPROVAL.md](B2-G4-HUMAN-APPROVAL.md)). The approved bytes were prepared from commit `8ed54243a82f04363c7644c30c8584bca2a2d455` and
were not committed when they were approved. It settles the source-definition part of G4. P1 identity provenance
remains within Stage 1, and the `[GAP]` of G4 for P1 stands. The revision establishes no build, linkage or runtime
property, validates nothing physically, upgrades no evidence label and authorizes no Stage 1 work.

| Item | Requirement (spike §8.3; closure §8) | Record | Disposition | What remains |
|---|---|---|---|---|
| C1 | Human authorization of a scope option, recorded separately from the MS-000 gate | [C1-AUTHORIZATION.md](C1-AUTHORIZATION.md) | **Accepted by the independent reviews.** Option B, Stage 0 only, 2026-09-26 | Nothing for C1. The authorization does not extend to Stage 1 |
| C2 | A coupling route selected from the reuse candidates and fully specified | [C2-COUPLING-ROUTE.md](C2-COUPLING-ROUTE.md) | **Accepted by independent review**, with its capability gaps disclosed and P3b unestablished. R-B, CP2K `MIXED`/`GENMIX`, is selected. Native-interface limitations, undocumented capabilities and demonstrated negatives (none) are now distinguished | P3b open. The five undocumented route capabilities are dependencies within Stage 1; C6 is a Stage 2 gate |
| C3 | Provenance capture tested on a trivial AiiDA job against the field set frozen after the data-model review | [C3-PROVENANCE-WIRING.md](C3-PROVENANCE-WIRING.md) | **Accepted by independent review as a reviewed partial demonstration; readiness BLOCKED.** One trivial non-chemistry job ran with exit status 0. F1 now requires retained full diff bytes and untracked source contents. Coverage: 2 fields on the job, 5 by surrogate (atom identity only as surrogate, with chain survival unverified), 4 not demonstrated | Prerequisites to starting Stage 1: identity-chain survival, the remaining provenance extensions and the login-shell environment gap. Closing them needs a new wiring test under its own authorization |
| C4 | Tolerances, budgets and the numerical-convergence protocol declared, approved and recorded | [C4-TOLERANCES-AND-CONVERGENCE.md](C4-TOLERANCES-AND-CONVERGENCE.md) | **Accepted by independent review**, including the E3 persistence correction made here, and **approved by a person on 2026-09-27** at the digest bound in Section 2 ([approval record](C4-HUMAN-APPROVAL.md)). The opening Approval bullet of C4, which still reads PENDING, is frozen text superseded by that record. The operational electronic-state rule is declared; E3(iii) is INDETERMINATE by declaration; **N8 is BLOCKED** pending the representations of both compared records and the combined formatting allowance r. Row 11 carries the zero-accepted-step case and requires the order comparison of the events E1–E4 under their full criteria at checkpoint S; row 5 declares E3's minimum persistence Δd_min = 0.20 Å for that comparison; row 3 keeps the N6 energy criterion of event E1 apart from the geometric trigger | Nothing further for human approval. Prerequisites to starting Stage 1: the N8 representations, with the combined formatting allowance r, and the compiled Psi4 fitting-basis steps. Dependency within Stage 1: engine grid acceptance. *2026-09-27:* the compiled Psi4 steps are established from the v1.11 tagged source. The N8 representations are partially established: no separate, direct record of the optimizer's gradient is written, the reading of row 10 is a definitional question, and r is not fixed by source ([source resolution](SOURCE-RESOLUTION.md#7-n8-the-two-compared-representations)). N8 remains BLOCKED. *2026-09-28:* a person approved a revision of C4 that defines N8 as fixed-atom checks ([C4-HUMAN-APPROVAL-02.md](C4-HUMAN-APPROVAL-02.md)); N8 is no longer blocked by its definition and has not been run. |
| C7 | Validation set, displaced atoms, P2 test molecule with identical model chemistry and isolated-molecule treatment, Stage 2 checkpoint selectors | [C7-VALIDATION-SET.md](C7-VALIDATION-SET.md); [structures/ms-001](../../structures/ms-001/README.md) | **Geometry, validation definitions and the corrected checkpoint comparison accepted by independent review**, including the E3 persistence correction made here. The selectors use B3 §5 unchanged and are geometric only, and a branch with zero accepted steps selects nothing and blocks. Checkpoint S compares the events E1–E4 under their full criteria. E3 counts only over its declared minimum persistence, and neither a match of geometric lists nor a match of isolated E3 hits ever releases a segment | Prerequisite to starting Stage 1: basis normalization. Dependencies within Stage 1: the remaining N2 checks and libxc identity. *2026-09-27:* basis normalization is partially established; the Libint2 version of the Psi4 build remains open ([source resolution](SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4)) |
| B1 | Models M1 and M2 frozen, hashed and labelled `[AGENT]` | [structures/ms-001](../../structures/ms-001/README.md) | **Accepted by independent review** as an `[AGENT]` model definition with no physical validation. The geometry is unchanged from attempt 3. The rigidity statement is limited to start, V1 and V2, and V3's intended change of about 1.50 Å is described | Not a model of the benchmark geometry and not compared with the authors' coordinates `[GAP]` |
| B2 | Scheme (partition, embedding, links, charge, spin) and the settings of both levels, as an `[AGENT]` deviation, approved by the reviewer | [B2-METHOD-DECLARATION.md](B2-METHOD-DECLARATION.md) | **Accepted by independent review**, with explicit prerequisite blockers and no claim of method readiness. The convergence controls and SCF algorithms of both engines are declared. For Psi4, `GUESS SAD`, `DF_SCF_GUESS false` and `SAD_SCF_TYPE DIRECT` are declared as explicit options, and the cited Python driver paths honor them (B2 §6). The fitting-basis behavior of the compiled SAD solver, double-hybrid test and gradient remains `UNVERIFIED` and blocks Stage 1. Nothing beyond the cited Python source is claimed about fitting bases. The dispersion-input contract is established from version-matched source | Prerequisites to starting Stage 1: G4 `[GAP]`, the unit of `OMEGA` and the compiled Psi4 fitting-basis steps. Dependencies within Stage 1: GAPW with exact exchange, GFN0 with `UKS`, and the s-dftd3 r⁻⁸ exponent. Stage 2 gate: the defining reference `[GAP]` for P2. D3 sr8 = 1.0 is a declared deviation. *2026-09-27:* `OMEGA`'s unit and conversion and the compiled Psi4 steps (tagged-source behaviour) are established from version-matched source. G4 is partially established, with the dftd4 source to be declared, and its `[GAP]` for P1 stands. B2 carries dated annotations only ([source resolution](SOURCE-RESOLUTION.md#3-dispositions)). *2026-09-28:* a person approved the declaration of the dftd4 source for G4 in B2 §3 ([B2-G4-HUMAN-APPROVAL.md](B2-G4-HUMAN-APPROVAL.md)); the source-definition part of G4 is settled by it, and its `[GAP]` for P1 stands |
| B3 | Drive protocol, including the sensitivity steps and segment rule, approved by the reviewer | [B3-DRIVE-PROTOCOL.md](B3-DRIVE-PROTOCOL.md) | **Accepted by independent review**, including the E3 persistence correction made here. The geometric triggers T_A and T_R govern z0, the approach stopping rule and the selection of checkpoint configurations and windows. Checkpoint S compares the order of the inherited events E1–E4 under their full criteria, including E1's N6-resolved energy decrease and E2's persistent Si–C bond and intact Si–Si bonds at the anchoring Si. E3 counts only where the pendent state persists over the declared minimum Δd_min = 0.20 Å of imposed d, and it is placed at the first step of that span. An isolated E3 hit is not observed, and a span that cannot be established inside the compared interval makes E3 INDETERMINATE. An INDETERMINATE event makes S INDETERMINATE, and a match of geometric lists alone never releases a segment. Event E1 needs the Si–C bond to form and an N6-resolved energy decrease at the same step. It is INDETERMINATE when an energy or sign is unavailable, and at step 0 unless the Si–C bond is absent there at all three multiples. A branch with zero accepted steps has no anchor or window, blocks both checkpoints, makes no sensitivity re-run and starts no dependent branch | Nothing further within Stage 0. The declared Δd_min = 0.20 Å remains an arbitrary `[AGENT]` declaration without physical validation |

**Stage 0 as a whole: closed as a set of frozen prospective definitions.** Every Stage 0 definition is recorded and
hashed below. The corrected definition package has independent review approval: C1, C2 (P3b unestablished), C3
(readiness BLOCKED), C4 (N8 BLOCKED), C7, B1, B2 and B3 are accepted as definitions. Lead acceptance is recorded, and a
person approved C4 on 2026-09-27 ([approval record](C4-HUMAN-APPROVAL.md)). The closure fixes these definitions
prospectively. It is not readiness, validates nothing physically, upgrades no evidence label, and authorizes no
Stage 1, Stage 1a or Stage 1b work and no calculation, installation or engine run.

**Readiness for Stage 1: BLOCKED.** The categories below are used across this package (B2 §8, the package index and
the research state).
- **Prerequisites to starting Stage 1.** All must hold before any Stage 1 calculation. Four are recorded: the Stage 0
  items are corrected or explicitly reviewed-blocked, independent review has approved them, Lead acceptance is
  recorded, and a person approved C4 on 2026-09-27. The others do not hold:
  - a separate human authorization of Stage 1;
  - the C3 blockers closed;
  - five definitions settled from version-matched source: G4, the unit of `OMEGA`, basis normalization, the N8
    representations (with them, the combined formatting allowance r of N8), and whether the compiled Psi4 SCF and
    gradient steps use any fitting basis under the declared settings. *2026-09-27:* two are established and three
    are partially established ([source resolution](SOURCE-RESOLUTION.md#3-dispositions)), so this prerequisite
    still does not hold.
    *2026-09-28:* the N8 representations are settled by the approved revision of C4
    ([C4-HUMAN-APPROVAL-02.md](C4-HUMAN-APPROVAL-02.md)); this prerequisite holds only when the other definitions listed
    here are also settled.
    *2026-09-28:* the dftd4 source for G4 is declared in B2 §3
    ([B2-G4-HUMAN-APPROVAL.md](B2-G4-HUMAN-APPROVAL.md)), which settles the source-definition part of G4; P1 identity
    provenance remains within Stage 1, and this prerequisite holds only when the other definitions listed here are
    also settled.

  None of these three holds, and Stage 1 has not started.
- **Dependencies within Stage 1.** These are settled only by Stage 1 work:
  - CP2K installation and build identity, including the libxc version it links;
  - the five undocumented route capabilities of C2 §5;
  - Mulliken spin populations for E1 inside `MIXED`;
  - the remaining N2 representation checks;
  - preservation of a failed job.
- **Stage 2 gates.**
  - C5: regimes, P1 identity with parameter provenance, P2 established including its check against the defining
    reference `[GAP]`, and complete provenance coverage.
  - C6: composite validation, including N5 and N8.
  - B4: parity unknown.

**Readiness for scope option A: BLOCKED**, unchanged. It is not authorized. The MS-000 gate stays PASS as a planning
judgement ([closure record](../ms-000/CLOSURE.md)) and implies none of the above. P1, P2, P3b, C5 and C6 are not
established.

## 2. Frozen artifacts

| Artifact | Path | SHA256 | Evidence label |
|---|---|---|---|
| C1 authorization record | `docs/ms-001/C1-AUTHORIZATION.md` | `21852d56daff3e648016f5dd7748b04bdf5c8fa00bb983159b117b54fba93d3a` | Process record; no evidence class |
| C2 coupling route | `docs/ms-001/C2-COUPLING-ROUTE.md` | `aa8425952187d9460a81034cbd98fc5c11108034a9bdda0afd0eb328c410459a` | `[AGENT]` selection over `[LIT]` documentation facts; `UNVERIFIED` items listed |
| B2 method declaration | `docs/ms-001/B2-METHOD-DECLARATION.md` | `aa24a45276d8cf89cdd47342c9ed27463be10562bdc794ae3e748160c9c2402f` | `[AGENT]` declared deviation over `[LIT]` defaults and parameters; `[GAP]` items listed. Revised 2026-09-28 to declare the dftd4 source for G4; the digest bound before was `022e4e8f10f8e2b29fafb1b6a38c6150760f0d5048923f6699192e5d9df77a1a` |
| B3 drive protocol | `docs/ms-001/B3-DRIVE-PROTOCOL.md` | `291754f60b49be52e349379c0f80dc0ed4782704e58f00a906997db8d842f955` | `[AGENT]` over `[LIT]` optimizer defaults |
| C4 tolerances and convergence | `docs/ms-001/C4-TOLERANCES-AND-CONVERGENCE.md` | `a51009089011d25860f5c6610186021e575a30e3bb38481db68345ee185158da` | `[AGENT]` declarations; cited defaults `[LIT]`. Budgets are declarations, not validated uncertainties. Revised 2026-09-28; the digest approved on 2026-09-27 was `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d` |
| C4 human approval record | `docs/ms-001/C4-HUMAN-APPROVAL.md` | `96975be965e2bd10eed45ab236282ec0c6d7d3751965eb98f2e216e5a925cffc` | Process record; no evidence class |
| C4 human approval record, revision of N8 | `docs/ms-001/C4-HUMAN-APPROVAL-02.md` | `d7e717bdd4be85e6355faf11f5b45e70c88fcc56dae86c419377bf73509db3fc` | Process record; no evidence class |
| B2 human approval record, G4 declaration | `docs/ms-001/B2-G4-HUMAN-APPROVAL.md` | `e489b9b9e982c42ee3d402eda3f33bbcdf36752a8fd31c327be47881ed8a6f69` | Process record; no evidence class |
| C7 validation set | `docs/ms-001/C7-VALIDATION-SET.md` | `301fc51755080e8f0e6126436a8e4ec45ba078ed01b81ce55aebabf34bd9a412` | `[AGENT]`. That the branches pass through the configurations is `[SPEC]` |
| C3 provenance wiring | `docs/ms-001/C3-PROVENANCE-WIRING.md` | `cd0ffcc37d40fbb82a0801a2685335c68fdde08e8f6fc6c6d31e3ff76fe2723d` | Software wiring evidence only, with no chemistry class. The field set is `[AGENT]`; coverage gaps are `[GAP]` |
| Failure record | `docs/ms-001/FAILURE-RECORD.md` | `3e5724c6786c0cb68bc7ee311608303945f4dbc95e4de2fae503b164c4151187` | The failure-record provenance field (evidence policy §4) |
| Source ledger | `docs/ms-001/SOURCE-LEDGER.md` | `4d46ff84ffe0767f5ded9d202b935836007cd9d4243647bc438353664f44142c` | `[LIT]` provenance record |
| Package index | `docs/ms-001/README.md` | `b3d536f59ad07bb3143d8abffd95501e4b31b4d738fe526f67ac8a90ecb8e147` | Navigation. Updated 2026-09-28 for recipe-audit status and links, previous digest `18f2ef3c0000addeaddd4d04dafaa0341943b6c81bb9602f44bc549390746335`; then updated 2026-09-28 for the status of the P2 build-declaration proposal and links only, previous digest `1288f41ab9bdcfdacede9fe433fe43842521f6202d6d4347ed8c511f5094bd94`. No definition, evidence label or gate changed |
| Geometry record (document) | `structures/ms-001/README.md` | `4cc6cc42660a0dd439f9d0c018aba0cbdea933b0d734fb163cec2442ac97aba6` | `[AGENT]` choices; `[GAP]` benchmark relation |
| Geometry record (machine-readable) | `structures/ms-001/geometry-record.json` | `43ef99bc795b600c834f9bf5a7590ee3dd6600bc8f1a65354f849120a5f55e74` | `[AGENT]`. Measured construction values establish internal consistency only |
| B1 model M1 | `structures/ms-001/M1-build-site.extxyz` | `c9374642d5e1cd4509b83cc9c48adbdbe1de1821df949f8700b55f53c0ff0aea` | `[AGENT]` |
| B1 model M2 (reused) | `structures/donor-activated-EAOGe-C2-radical.extxyz` | `bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3` | `[AGENT]`; unchanged, read by digest |
| Start of the approach branch | `structures/ms-001/start-combined.extxyz` | `f5e45282b638a6569b926c4aa1a402e5fa7c9e25e2db12820dbc3ef33b959ca5` | `[AGENT]` |
| C7 V1 | `structures/ms-001/V1-separated-bodies.extxyz` | `ea48cc26bb6102abcf4c0786861bbf3278d00911252fd41242cb81fe74e98cd2` | `[AGENT]` |
| C7 V2 | `structures/ms-001/V2-contact-GeC-intact.extxyz` | `f1a4e075cf4e239a4fac3805cc45e078e8fff362bacdd90d53c45d54222210be` | `[AGENT]`; the file name is nominal |
| C7 V3 | `structures/ms-001/V3-pendent-C2-GeC-broken.extxyz` | `6d722a44787cbfb7a25d87dc2f6b33ae79a5ff8b1c416d966f6cb7ddf78043c1` | `[AGENT]`; the file name is nominal |
| C7 P2 test molecule | `structures/ms-001/P2-test-molecule-H3GeCCSiH3.extxyz` | `25c7bceef076f2ed77987dbfabf89cce814490091e72ce911e08ed1ed6e2a702` | `[AGENT]` |
| Geometry generator (code identity of B1 and C7) | `tools/build_ms001_geometries.py` | `bb1b2a99b352bc773c3e858d4aac3cd0596597b5cf87dedbc1182f933ee9ab13` | Code. It produces `[AGENT]` files by geometric construction only |
| C3 driver (code identity of the wiring job) | `tools/c3_provenance_wiring.py` | `d3d8b58e06f7ffff23934bec550b927586effad9c175e9a3451096bb8fbb3d17` | Code; software wiring test |

## 3. Environment

The environment is project-local and reversible, and nothing was installed globally. It runs CPython 3.12.14 with
ASE 3.29.0, aiida-core 2.9.2 and NumPy 2.5.3. The 88 distributions were installed with `--require-hashes`; the lock
file has SHA256 `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8`. No chemistry engine was
installed or run.

Two deviations are recorded in [C3 §1](C3-PROVENANCE-WIRING.md#1-environment):
- **D1.** A first import created a user-level AiiDA folder. It was removed as an empty tree, and its
  non-recreation was verified.
- **D2.** The login-shell dependence of the local transport.

Filesystem confinement was **not** flawless. Besides D1, a few Stage 0 working files were written outside the
permitted project directory, and an earlier basis-comparison attempt was superseded. All are disclosed in the private
record.

## 4. Private evidence bound by digest

These records are kept privately because they contain local paths or host details. They are identified here by
SHA256 only.

| Record | SHA256 |
|---|---|
| Environment setup log (14 steps, each exit 0) | `8d391427e8df6ebf82c98949f64a98f404a2138bdd2e3833e4f105ac95c1b14b` |
| D1 incident log and addendum | `7003338310a566188b87642bf3f4cadb2732e30842184707b9a6051b2c3f0615` |
| D1 non-recreation check | `bd4843bf12bfc6c31b67c0dcecde0b9190c315586ec221e742af51527ed65287` |
| D2 note | `799602024945570eb8ea23f2fb76412333c238e449b4b895e94fbc2b4252ecf2` |
| C3 job evidence (node identifiers, hashes, retrieved context) | `959cb23a3862ada0d224b6cb6db0964c3f0fff9ba92c6b8604920f207e6130b2` |
| C3 run log | `f486fc45653a56a245137d2062d76ae8167574998247079bb2f7638a4de32558` |
| ASE-only per-atom array round trip | `9835fe3e57ae526b925dabb890374cc3c2bd3f11e461d76c967f14b24fa66fa8` |
| Geometry attempt 1 log (failed) | `4592247d4462cc61123bf616b9566909b55c3df38b0a75eab486755a202783ca` |
| Geometry attempt 2 log (superseded) | `db868255d9694b7a95870900eb375b8062624acfeefd5d518dd9745ecace5a44` |
| Attempt-2 generator bytes, reconstructed and hash-verified | `c7d14e03de21bdfbe68d805c63b0ce627a0fc7515952af17fafcdd4bd4e294ff` |
| Attempt-2 output digest list | `6d206f2e0b73adac9bc3bc3d42bd83aa2f4167d65c0830b3917e23b882692dce` |
| Geometry attempt 3 log | `1bd5ce11317315aa420176887531e97c1f7b708880af415bcda2a42063004533` |
| Attempt-2 validation log (unchanged; the erratum correcting its stated scope is appended to the separate angle-metadata finding record, not to this log) | `373ec20492a824d0553b6da523d17ceaad32b0ccca271659fe3a947b31c799c3` |
| Attempt-3 validation (120 checks, all passing) | `1082769f04a3890923d3c15faa4637099f7505053f5a4dd1c1138404fda50903` |
| Angle-metadata finding with its erratum | `f5ebbb6671f8408bcff89923325d47c1bd7aef651f40875b2e50c5185e62b0cb` |
| def2-TZVP text comparison between CP2K and Psi4 | `e96c77726491a9b9cbb312bcfe9b8976f3092818f3fb31b59b26a1fcdc24e5a5` |
| Partition derivation | `54c2b4e831281d86f26e3c722dbd31d9b9f31b4316ff9e86627db85d47a20de1` |
| Fixed-set derivation for B3 | `d98d3e39059bd8c91f6228a0d74a680401f86e98c4cea5e3815502067e99f421` |
| Retrieval manifest (73 retrievals, 71 obtained) | `0ea531877903d8f10992ee3a1fe6208f8e43c5fc2a9917551d318cd0d2cbac10` |
| Post-documentation geometry validation (120 assertions, all passing; the original validator is unchanged) | `8fc825603aec3fbb901f0ded43b102c88df93bd0f60bfe7ac4b830641292e65b` |
| Measure-then-assert check of the Pass B values against their sources, rerun on the corrected records (121 assertions, all passing; log of attempt 5, earlier logs retained) | `a0494accdb58b2195f7b46ff56ec06766c913c7f06ce6bf46b18d4fa37644b60` |
| Tool rigidity per combined file (start, V1 and V2 below 1.3e-8 Å; V3 at 1.500000 Å between its two groups) | `7c5ea7f65d2b88db7db86c184e9c8092821a177f2825dc388ab28760b8766d8e` |


## 5. Recipe audit status supplement, 2026-09-28

The [recipe metadata audit](RECIPE-METADATA-AUDIT.md) closes the unread-recipe gap with `[LIT]` software provenance
only. Normalization remains PARTIALLY ESTABLISHED; binary provenance and runtime conformance remain open. No P2
build is declared. Only the package-index navigation digest above is refreshed; every approved definition,
human-adopted reference and other artifact binding is unchanged. W1 remains unrun, C4-j and B3-b deferred, and
Stage 1/1a/1b and Stage 2 unauthorized. Scope option A remains BLOCKED.

## 6. P2 build-declaration proposal status supplement, 2026-09-28

The [P2 build-declaration decision packet](P2-PSI4-BUILD-DECISION-PACKET.md) and its
[source ledger](P2-PSI4-BUILD-SOURCE-LEDGER.md) prepare a person's decision on declaring the exact conda-forge
`osx-arm64` package `psi4-1.11-py314h53d0584_1`, with its exactly pinned Libint package, as the Psi4 build that P2
uses. They are proposals only and are not Stage 0 definitions, so they are not bound in Section 2. No build is
declared, and no option is chosen, approved or applied. B2 stays at the digest bound in Section 2, and C4, B3, C2, C7,
every approval record and every human-adopted reference are unchanged. Only the package-index navigation digest above
is refreshed. The packet records that an approved declaration would change B2's whole-file digest and would therefore
need a fresh adoption of the revised B2 by C4, B3, C2 and C7; nothing of that is applied here. Basis normalization
remains PARTIALLY ESTABLISHED. W1 remains unrun, C4-j and B3-b deferred, and Stage 1/1a/1b and Stage 2 unauthorized.
Scope option A remains BLOCKED.
