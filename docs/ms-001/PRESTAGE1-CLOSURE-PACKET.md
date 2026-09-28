# MS-001 pre-Stage-1 closure packet

Date: 2026-09-27. MS-001 scope option B, after the closure of Stage 0 and the source resolution.

**Dated status supplement, 2026-09-28.** The packet below retains its historical dispositions and proposals.
The human-approved G4 and N8 revisions are recorded in the [package index](README.md). The newly completed
[recipe metadata audit](RECIPE-METADATA-AUDIT.md) closes the unread-metadata gap, identifies declared source,
patch and build requirements, and confirms the exact Libint package as both a Psi4 host requirement and a run pin
(`[LIT]` software provenance). Basis normalization remains PARTIALLY ESTABLISHED; actual binary provenance and
runtime conformance remain open. A separate prospective P2 build-declaration decision package can now be prepared
(`[AGENT]`), but no declaration is made or approved here. W1 remains unrun; C4-j and B3-b remain deferred.
Stage 1, Stage 1a, Stage 1b and Stage 2 remain unauthorized, and option A remains BLOCKED. New sources are in a
[new companion ledger](RECIPE-METADATA-SOURCE-LEDGER.md); the human-adopted earlier ledger is unchanged.

This packet takes the remaining prerequisites to starting Stage 1 as far as they can go without running scientific
software, changing a frozen definition or starting the C3 wiring test. It prepares the decisions that remain for a
person. It also specifies, on exact terms, a proposed next non-chemistry wiring test, which would need its own
separate authorization. It authorizes nothing.

## 1. Records

| Part | Record | What it provides |
|---|---|---|
| 1 | [INSTALLED-BUILD-AUDIT.md](INSTALLED-BUILD-AUDIT.md) | A static audit of the installed Psi4 1.11 build of E-01: its Libint2 package and what its package records establish about Libint2 and Psi4 source and build, with dispositions |
| 2 | [G4-DFTD4-DECLARATION-PROPOSAL.md](G4-DFTD4-DECLARATION-PROPOSAL.md) | A comparison of the two dftd4 routes of the CP2K 2026.2 toolchain, one recommendation, an exact candidate declaration and the alternative |
| 3 | [N8-DECISION-PACKET.md](N8-DECISION-PACKET.md) | A human decision packet on N8: one recommended option, what it gains and loses, exact candidate text, and a map of every consequential frozen-record edit |
| 4 | [C3-WIRING-TEST-PROPOSAL.md](C3-WIRING-TEST-PROPOSAL.md) | A specification of W1, the smallest future non-chemistry AiiDA wiring test that could close the C3 blockers |
| Sources | [PRESTAGE1-SOURCE-LEDGER.md](PRESTAGE1-SOURCE-LEDGER.md) | Every external byte newly inspected for this packet, with identity, time, size, SHA256, locators and limits |

## 2. What this packet is not

- **Nothing executed or installed.**
  - No scientific software, engine, AiiDA command, generator or renderer was run, imported or installed.
  - No calculation, geometry work, C3 wiring execution, Stage 1a or Stage 1b work took place.
  - No dependency or environment was changed.
- **Frozen records unchanged.** C4 is byte-identical at SHA256
  `707c7f72564e6bd2bae2a8a0e5acf2c13dd86e048ca624858d147514cffbb68d`, and the
  [C4 human approval record](C4-HUMAN-APPROVAL.md) is unchanged. Every artifact bound in the
  [freeze record](STAGE0-FREEZE-RECORD.md#2-frozen-artifacts), and the freeze record itself, is byte-identical. That
  includes the package index and the Stage 0 source ledger. The records of this packet are therefore not listed in
  the package index; they are linked from the repository's README, catalogue and research state instead.
- **Nothing applied or approved.** No N8 option, formatting allowance, G4 declaration or other method change is
  applied. Every proposal is separate, exact and unapplied.
- **Not evidence.** Source reading and static inspection of installed files are software provenance. They are not
  physical evidence, runtime conformance, method validation or parity, and they upgrade no evidence label. Every
  recommendation is `[AGENT]`.
- **Not readiness.** Stage 1 remains BLOCKED and is not authorized.

## 3. Decisions a person can take independently

Each item can be accepted, declined or deferred without the others.

| Decision | Record | Path it would follow |
|---|---|---|
| Declare the dftd4 source for G4, as recommended or as the alternative | [G4 proposal §6](G4-DFTD4-DECLARATION-PROPOSAL.md#6-recommendation-and-candidate-declaration) | C4 §3: fresh approval by the roles of the original selection, then a dated annotation of B2 |
| Choose an N8 option, O2 recommended | [N8 packet §2 and §4](N8-DECISION-PACKET.md#2-options-and-recommendation) | C4 §3, with a new approval record bound to the revised C4 digest |
| Rewrite C4's opening Approval bullet (C4-j) | [N8 packet §6.1](N8-DECISION-PACKET.md#61-c4-docsms-001c4-tolerances-and-convergencemd) | C4 §3. Independent of any N8 option |
| Correct B3's cross-reference to the revision sequence (B3-b) | [N8 packet §6.2](N8-DECISION-PACKET.md#62-other-frozen-definitions) | The same sequence for B3. Independent of any N8 option |
| Authorize W1 | [C3 wiring test proposal](C3-WIRING-TEST-PROPOSAL.md) | A separate human authorization of a non-chemistry AiiDA run |
| Declare the Psi4 build that P2 uses | [Installed-build audit §7](INSTALLED-BUILD-AUDIT.md#7-relation-to-the-normalization-item) | A prospective declaration under the same sequence; not proposed here |

## 4. Changes since the source resolution

- **Libint2 of the E-01 build.** The installed Psi4 build carries Libint2 2.13.1, by its package record, not the
  v2.8.1 that Psi4's source names as a pin. The installed header defines the same normalization. The recipe and
  build metadata of both packages remain unread.
- **G4.** The two CP2K-hosted archives carry byte-identical dftd4 4.2.0 source files. The asymmetry is in the
  toolchain's install scripts: the tblite route patches those files and the standalone route does not.
  - By source tracing, CP2K's GFN0 path reaches none of the patched routines with its defaults. That is text identity
    of a traced subset, not equivalence of two builds.
  - Neither route fixes how dependencies are resolved. A declaration must require the actual resolution to be shown.
- **N8.** GEO_OPT writes no trajectory frame for its starting geometry. A fixed-coordinate check therefore needs the
  run's input as its reference.
- **C3.** Under aiida-core 2.9.2:
  - the direct scheduler invokes Bash itself, whatever the script's shebang;
  - the local transport passes its parent's environment to every shell it starts;
  - a dry run uses a default local transport rather than the configured computer's.

  The W1 specification therefore cleans the environment at the parent and validates its own submission script
  before upload.

## 5. Consolidated readiness

This table follows the categories of the [freeze record](STAGE0-FREEZE-RECORD.md#1-disposition).
- **"Closed here"** means established by this packet.
- **"Human decision"** means a step that only a person can take.
- **"Authorized test"** means the W1 wiring test, or a static read, under its own authorization.
- **"Stage 1"** means a dependency within Stage 1.

| Item | Before this packet | After this packet | Closed here | Human decision | Authorized test or static read | Stage 1 |
|---|---|---|---|---|---|---|
| Separate authorization of Stage 1 | Not given | Not given | — | Required | — | — |
| C3 blockers: F4 identity chain, F1, F2, F3, F5, F6, F8, F11, F7 | BLOCKED | BLOCKED; the closing test W1 is specified | Specification of W1 only | Authorizing W1 | W1 | — |
| G4, GFN0 parameter provenance: dftd4 source | `PARTIALLY ESTABLISHED`; dftd4 source to be declared | `PARTIALLY ESTABLISHED`; declaration prepared, routes compared, dependency-resolution gap found | Route comparison | Approving a declaration | — | P1 identity: loaded files, linked dftd4, D4 environment settings |
| `OMEGA` unit and conversion | `ESTABLISHED FROM VERSION-MATCHED SOURCE` | Unchanged | — | — | — | Printed `HFX_INFO\| Omega` only |
| Basis normalization | `PARTIALLY ESTABLISHED`; Libint2 of the P2 build open | `PARTIALLY ESTABLISHED`, narrowed: E-01 build carries Libint2 2.13.1, whose header defines the same normalization | Installed Libint2 version of the E-01 build | Declaring the P2 build | A static read of the packages' recipe metadata (tool able to read zstd) | Remaining N2 checks |
| N8 representations and definition | `PARTIALLY ESTABLISHED`; N8 BLOCKED | Unchanged; options turned into an exact decision packet, O2 recommended | Decision packet only | Choosing an option under C4 §3 | — | Formatting and correspondence observations of the N8 packet §5 |
| Compiled Psi4 steps | Tagged-source behaviour established; build provenance and runtime conformance open | Package identity of the build established; source and patch identity unresolved; runtime conformance open | Package identity | — | The same recipe read | P2 JK and JKGrad headers |
| CP2K installation and build identity, libxc version | Stage 1 dependency | Unchanged | — | — | — | Yes |
| Route capabilities of C2 §5, items 1–5 | Stage 1 dependencies | Unchanged | — | — | — | Yes |
| Mulliken spin populations for E1 inside `MIXED` | Stage 1 dependency | Unchanged | — | — | — | Yes |
| Preservation of a failed job (F9) | Stage 1 dependency | Unchanged; W1 does not establish it | — | — | — | Yes |
| P1, P2, P3b, C5, C6, B4 | Stage 2 gates, unestablished | Unchanged | — | — | — | — |

**The prerequisite "five definitions settled from version-matched source" still does not hold.** G4, basis
normalization and the N8 representations are still partial. The C3 blockers still stand, and Stage 1 has no
authorization. **Stage 1 remains BLOCKED and is not authorized.** Scope option A remains BLOCKED. MS-000 remains a
feasibility PASS only.

## 6. Process record

This packet was prepared under the project's separate orchestration system. Private records hold every command, the
retrieval manifests, the run logs of the read-only inspection scripts, the failed attempts and the review. They are
identified by SHA256 in the [source ledger](PRESTAGE1-SOURCE-LEDGER.md) where they back a public statement, and they
are not published.

Two process limits are recorded:
- One planned observation, free space before and after the retrievals, was not made, because the executed retrieval
  script did not include it. It is recorded as not made.
- The attempt to read the conda metadata stopped because the system archive tool lacked zstd support. That stop is
  retained as a failure, not repaired.
