# Export manifest

This manifest lists every file in the initial public export, with its SHA256 and what it was derived from.

- **Sources are identified by description and SHA256 only.** The project's original working records are kept
  privately and are not part of this repository.
- **This manifest does not list or hash itself.** Its own digest is bound, together with every file below, in a
  separate private exact-tree inventory.

## Files

| Export path | SHA256 | Derivation |
|---|---|---|
| `.gitignore` | `371d515c4833af483145f145d7769ec3a2e9c51e010e46a70f1b26afe601a7e3` | New for this export. Ignores local orchestration state, Python environments and caches, environment files and OS/editor files. Scientific data and result logs are not ignored. |
| `README.md` | `5d27eb7069a6dab2f947069c6c4503afd558777a1dd54c77b4e1f6cccd664d9a` | New for this export. Cites and paraphrases the benchmark and related preprints; copies no source file. |
| `AGENTS.md` | `3e221c92057ed9493ccc78611d5e942e4f7d40beb1921550349115ea2b615c7e` | New for this export. Not copied from any private operating contract. |
| `.agents/RESEARCH-STATE.md` | `5c8544e3a7576100eaf7984b14a19d279431da410a5e35163c82c3bb3f2db07e` | New for this export. It summarizes the current qualified status from private assessment records, which are not published. |
| `docs/benchmark.md` | `78d8b29b5333ccbc4393e39f7af6995a30edc2368db3e80cd60bd794a0ae4ea6` | New. Paraphrases selected sections of the benchmark v1 PDF text (cached copy SHA256 `c77704adbe9d75c3fc11470a712822f1f1cf3b2d59b121d2cfc41c0d5eae139b`) and three arXiv listings. No paper text or figures copied. |
| `docs/evidence-policy.md` | `03789dd59494d2b872e0459a5fe8070de6beb531cb2ed2e539ed6abb02f506ed` | **Adapted** from the project's original evidence policy (SHA256 `93fb909f116797881c907c6495e65e0c6f67d62eb428d9916977cc8584438396`). Worked examples rewritten; internal cross-references, review-state lines and orchestration-layer detail removed; a rule on unverified capabilities added. |
| `docs/donor-candidates.md` | `f2a914c8c8961eb9dfd3eecd53466473fdec34b4a084be1b58d8ec1ef2764b2e` | **Adapted summary** of the reconstruction-inputs record (SHA256 `2f29e7dc39a342e32b4665c993e6b7600ed0107ed580c8c8f869d1e3ce58b206`). Internal paths, task identifiers, script and log references, cache file names, attachment-variant tables and electron counts of surface systems removed. Donor counts re-derived from the structure files. Historical identity and consistency claims are attributed to the original reconstruction notes and marked unverified. |
| `docs/e01-method-specification.md` | `5e9b2defd3285fd13b26e2b1f5cd0d826d3114b4e9fb6b009693710d50145971` | **Adapted** from the accepted method definition, sections 4–5 (lines 75–145) of the execution-route record (SHA256 `ce99f3b1968cb27e6bd452381ecdd98ad7b207532cf5e79ea080599624d8fa85`). See the omissions note below the table. |
| `docs/engine-capability-status.md` | `26006d42af4fb84ac3d39ba400285de06778eacfbc6f3c3ad4ead9a5b2ea2638` | New. See the source note below the table. No vendor text or code copied. |
| `docs/SOURCES.md` | `8738d16c11abd9c6fc4974c6f6d7ff53fd299bc5d50621cee02412c47e875787` | New source index. Compiled from the sources inspected in the current review, the project's retrieval records (cited by public URL only) and the link checks of 2026-09-23. Each entry states its basis: inspected, link-checked or recorded. Contains no computed values. |
| `docs/figures/architecture.svg` | `ab98975d49e50bce0d0af1a9173ec2e2a9b86e82abd9695a861edfc536e141ca` | New original diagram; conceptual. |
| `docs/figures/e01-validation-flow.svg` | `7492655a1a19d438278a7c5ba3c034b8a5e1baf2fa0460fa04fa8aac6618cfc0` | New original diagram; conceptual summary of the method specification. |
| `docs/figures/evidence-classes.svg` | `2a3ff687c8336214c72c5f6d25a54a1ce052c949c1063f18c2f07c76cfbb1d0a` | New original diagram; conceptual summary of the evidence policy. |
| `docs/figures/masthead.svg` | `a0b101bce37e7630c5929c62e25fda593a1e2758d387ba7bea58b03b837d0a9e` | New original illustration; conceptual. Not a structure, geometry or result. |
| `docs/figures/reported-outcomes.svg` | `09e1d62361297c778f73f660f9f5e4dac891043f5eee0ac140cab1d1dd0d8fe9` | New original chart. Its data are the four counts and intervals reported by the benchmark (Fig. 5 discussion), reproduced as a table in the README. No paper figure copied. |
| `structures/README.md` | `c4c62e2f5f02fe61a94a6ab2fb2ef1055fb6d970c7e9fc2114c9af151d0dc485` | New for this export. |
| `structures/donor-activated-EAOGe-C2-radical.extxyz` | `bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3` | **Adapted (header only)** from the original record, SHA256 `6ed11860b16290b698115c7a1638c494a5b72b2d296598c193671c4212e09a04`. See the header note below the table. |
| `structures/donor-precursor-EAOGe-C2I.extxyz` | `0556643368a2def37779d5150ab946e410aa1880e4170972bab55cc787fb8bb9` | **Adapted (header only)** from the original record, SHA256 `da63de5442e7f644cfb52ed55b10c668964235249d27e63f794711f8244340b2`. See the header note below the table. |

**Method specification omissions** (`docs/e01-method-specification.md`):
- Omitted: rows that apply only to later stages (optimization thresholds, constraint-output validation, basis,
  grid and proxy-size sensitivity, later-stage resource caps and preconditions), the worked witness table for the
  hypothesis rules, and the name-only next-experiment note.
- Rewritten: the Kohn–Sham stability statement, scoped to what the inspected sources show.
- Added: the clarifications from the current review.

**Capability-record sources** (`docs/engine-capability-status.md`). It summarizes inspection of these cached
sources:
- Psi4 development-manual texts, SHA256:
  - `scf` `4a624e8277c0679c6c054d94c0ea3263c3688dba3f62b8f5758e0e5415c2e7a8`
  - `oeprop` `7506acf7098966a1fd7ac7ed1df44e5a100c957c726eddf44779b79390de2888`
  - `dft_byfunctional` `546465d9a4695519600ecbe3404faf71b45493e6c042492b7fda177b929204ec`
  - `basissets` `531eb977c587798c22d7b323e4c13dff91bb662d10506bb4914cc7934cf0c8e7`
- Psi4 `v1.11` source files, SHA256:
  - `proc.py` `98ac648d84cc4587ec034b9207d3c6fbc3cd74df4c0409a85478e5467c0dd408`
  - `libxc_functionals.py` `e289d7d713e2ae9cecf8e37a22d80ed7fd9beed0c9febd0aa9282afd81c448fe`

**Structure header adaptation.** In both `.extxyz` files only line 2 changed:
- the internal task identifier was removed
- the private cache file names in the locator were replaced by "Barrera et al. arXiv:2512.24431 SI p15"
- `public_adaptation=` and `original_sha256=` were added

Line 1 and every atom line are byte-identical to the original.

## Redaction and adaptation policy

- **Never published:**
  - local file-system paths, user names and host names
  - internal session, task or runtime identifiers
  - names of the agent models or configurations used
  - credentials
  - orchestration-layer records (authorization, review, accounting and control records)
- **Excluded pending redistribution review:** third-party paper text, figures, supplementary material and vendor
  source code.
- **Adapted files say so.** An adapted file is labelled as adapted here, with its original's SHA256 and what was
  removed or changed. **It is not the original hash-bound record**, and its hash differs from the original's.
- **Facts from third-party sources are cited, not copied:** identifiers, reported counts and declared parameter
  values are cited with locators.

## Omitted from this export (retained privately)

| Material | Why omitted |
|---|---|
| Surface-model coordinate files and their constraint sidecars (three models) | Not inputs to the first experiment; they contain placeholder geometry that is easy to mistake for a benchmark model. The definitions are summarized in `docs/donor-candidates.md`. |
| Donor graph record, generator and checker scripts, and their logs | The generator reads locally cached third-party supplementary text, which is excluded pending redistribution review. The logs contain local paths. |
| Workflow-provenance test records and installation logs | Environment-specific and contain local paths; they are not chemistry evidence. |
| Earlier frozen documents (feasibility study, original architecture, tool landscape, source ledger, environment record) and the source addendum | Contain internal references, superseded status and milestone framing, and cache paths. The relevant facts are restated with attribution. |
| Cached third-party papers, supplementary material and vendor documentation or source | Excluded pending redistribution review. They are cited by identifier and hash. |
| Authorization, review, accounting, control and incident records; superseded attempt copies | Orchestration-layer and process records, not scientific content. |

This export is **not a complete archive** of the project's work.
