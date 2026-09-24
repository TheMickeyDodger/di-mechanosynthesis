# Export manifest

This manifest lists every file in the public repository with its SHA256 and its derivation. The project's
original working records are private and are identified here only by description and SHA256. The manifest does
not list or hash itself; its own digest is bound, together with every file below, in a separate private
exact-tree inventory.

## Files

| Export path | SHA256 | Derivation |
|---|---|---|
| `.agents/RESEARCH-STATE.md` | `0dde86b001a5f4794609e68e38e644ceda15ab0e4866d565b981b3f160717ae8` | New for the public export and revised editorially. It summarizes the current qualified status from private assessment records, which are not published. Revised 2026-09-24 for the stopped E-01 attempt: status, capabilities, open issues and next work updated, superseded statements noted in its log. |
| `.gitignore` | `371d515c4833af483145f145d7769ec3a2e9c51e010e46a70f1b26afe601a7e3` | New for the public export. It ignores local orchestration state, Python environments and caches, environment files and operating-system and editor files. Scientific data and result logs are not ignored. |
| `AGENTS.md` | `6e611ccf33aa03d999c220ce8175798c406703b017c3e70e4f49fcaa42a697d9` | New for the public export. It is not copied from any private operating contract. Revised 2026-09-24: the repository description, the organization table (the `results/e01/` row) and the statement on quantum-chemistry results now reflect the stopped E-01 attempt. |
| `README.md` | `9ef573d9102aeb3e6410b5145401508c92b0db86ccf7b98700ebaac153861a70` | New for the public export. It cites and paraphrases the benchmark and related preprints and copies no source file. Revised 2026-09-24: the introduction, the E-01 and capability paragraphs, the tool table and the contents table report the stopped E-01 attempt and the installed build; figures and captions are unchanged. |
| `docs/SOURCES.md` | `477ee9ecb674881a95aa58eb6b155e455ce95ad6f72aa29de14e105b9ccc8116` | New source catalogue compiled from the sources inspected in the current review, the project's retrieval records (cited by public URL only) and the link checks of 2026-09-23. Each entry states whether it was inspected, link-checked or recorded. Revised 2026-09-24: entries [6], [11] and [12] updated on installed-build evidence, Section 6 extended, and Section 7 added with entries [20] to [22] for the installation record, the E-01 records and the dispersion library. It contains no converged quantum-chemistry values. |
| `docs/benchmark.md` | `6c48750df8d8754ff7421111d4ddaf94b032266a5c33561d4ddb2151260ae649` | New. It paraphrases selected sections of the benchmark v1 PDF text (cached copy SHA256 `c77704adbe9d75c3fc11470a712822f1f1cf3b2d59b121d2cfc41c0d5eae139b`) and three arXiv listings. No paper text or figures are copied. |
| `docs/evidence-policy.md` | `32c88d9a0c4c516a4588cd4340f2af50198d30a0b9dcddac4b51d82dc7338720` | Adapted from the project's original evidence policy (SHA256 `93fb909f116797881c907c6495e65e0c6f67d62eb428d9916977cc8584438396`). The worked examples were rewritten, internal cross-references, review-state lines and detail of the orchestration layer were removed, and a rule on unverified capabilities was added. Revised 2026-09-24: one sentence classifying the E-01 record as a failure record of a software run. |
| `docs/donor-candidates.md` | `0cdde737d20727323925e2631ec26a92717597f08ace210caca0e4a0df3c77ab` | Adapted summary of the reconstruction-inputs record (SHA256 `2f29e7dc39a342e32b4665c993e6b7600ed0107ed580c8c8f869d1e3ce58b206`). Removed: internal paths, task identifiers, script and log references, cache file names, attachment-variant tables and electron counts of surface systems. Donor counts were re-derived from the structure files, and historical identity and consistency claims are attributed to the original reconstruction notes and marked unverified. A section documenting the Figure 1 rendering method was added. Revised 2026-09-24: the iodine core-electron count (46) and explicit electron count (192) reported by the installed engine's basis construction replace the earlier `UNVERIFIED` statement. |
| `docs/e01-method-specification.md` | `ab7e366879190519a8ac01b9cedc638ee0c9c4927414d66e3f3c8e710667891c` | Adapted from sections 4 and 5 (lines 75 to 145) of the execution-route record (SHA256 `ce99f3b1968cb27e6bd452381ecdd98ad7b207532cf5e79ea080599624d8fa85`), as described below. Revised 2026-09-24: a dated status note marks it as the preparation record, and Section 5 records how the open clarifications were settled; the specification text is otherwise kept as written. |
| `docs/engine-capability-status.md` | `845b008d11a8fb66f23f6f374451c0e5dabe1cf50fc63816650b09ec54c56f8f` | New, from the sources described below. No vendor text or code is copied. Revised 2026-09-24: a section on evidence from the installed build was added; the earlier sections are kept as written. |
| `docs/figures/benchmark-outcomes.svg` | `80fbd902eb8d7479ce733f6d2be060aff240532f7efe3973e787fd9f8e4e2fb3` | New original chart (Figure 2) of published data. It was generated by `tools/render_outcomes_chart.py` from `tools/benchmark-reported-outcomes.tsv` and shows the reported percentages, 95% confidence intervals and counts of the benchmark without recomputation. It is not a copied paper figure. |
| `docs/figures/activated-donor.svg` | `efc535f01867f6d62e42ff74be33662184b261cdaf313a91552ec4604bea7fca` | New original figure (Figure 1). It was generated by `tools/render_donor_plate.py` from the unchanged activated-donor structure file and `tools/activated-donor-bonds.tsv`. It shows heavy atoms only and no computed quantity. |
| `results/e01/README.md` | `69663988ea2f977a0781ec9648a20f556fff089858b0198c0a04324dc225ba18` | New (2026-09-24). A public report of the stopped E-01 attempt, written from the project's reviewed outcome report (private, SHA256 `5563fbdfb08d2ab7dafa1a1fa281d0748c17c5f56c5b312550785511f1802442`) and the run records. No review, authorization or accounting record is copied. |
| `results/e01/outcome.json` | `95d34b2ca1729b56e46553255b612d5e4e6ffd494a1db856104d0b37d354e16c` | New (2026-09-24). Machine-readable outcome; every value is transcribed without change from the private records listed in its `sources` field, each identified by SHA256. Internal identifiers and accounting documents are not copied. |
| `results/e01/method-config.json` | `cf06bedef08fbc1e3d0d36508360b4a2d0318d692bc2c093f92ffe2d58afd8aa` | New (2026-09-24). Derived from the reviewed E-01 configuration (private, SHA256 `813a28c7f658d5414401c6ec44abf80f87166071a35e92557d33fc1657961da8`), the installation receipt (SHA256 `4e080247aaed75c151b029564673c1d5c8204e110ec239a233fadc3265eb8b59`) and the installed-file hash set (SHA256 `45170652a4579319085a42cf9f1109b11ea52e0beb982439c4ac64eceb617d2a`). Internal status annotations, review references and local paths were removed; installed-file paths are relative to the environment prefix; values are unchanged. |
| `results/e01/raw/FEASIBILITY.psi4.out` | `288011863c70b5631da029a2d15cc767185c440f59d984ead2ba459c42cbe1b9` | Redacted copy of the engine output of the construction-only job (original SHA256 `8c49a5044c741d6150245899d4d14e0890a0535e2f795bd05f800f2307af1f71`, 1278 bytes). Five occurrences of the absolute installation path were replaced by `<psi4-prefix>/`; nothing else changed. |
| `results/e01/raw/FEASIBILITY.result.json` | `c4f479c535304ed23fed8dd5ac9592f3ccaf334861eecee5af32a764d8554bee` | Exact copy of the construction-only job result; identical to the original record. |
| `results/e01/raw/P-RKS-core.psi4.out` | `29a4f45ae784e8903dfcb2fc905003d1385dfffb2ea41c52f60cd53707ce6029` | Redacted copy of the engine output of the first precursor SCF job (original SHA256 `2a302836dadb33099cf209079731baa33f5dd793112238b197443ba7c67c4821`, 14 284 bytes). Replaced: five occurrences of the absolute installation path by `<psi4-prefix>/`, the absolute scratch directory by `<job-scratch>` and the host name by `<host>`; nothing else changed. |
| `results/e01/raw/P-RKS-core.spec.json` | `a47234303c7ffc868f07f794f8702a6df59d6a515e67b01d26b2fee5d1039d4d` | Redacted copy of the job input of the first precursor SCF job (original SHA256 `d88703ee7ad6908217736414cdb132430a4596d2d557c6301649a484db37f45f`, 6035 bytes). The absolute output-file path and scratch directory were replaced by `<job-dir>/psi4.out` and `<job-scratch>`; nothing else changed. |
| `results/e01/raw/P-RKS-core.stderr.txt` | `b4aee644c1f6763f077dbb61df71e9e816bb7681613b9d37a1e4de0236e5eb17` | Redacted copy of the engine error output of the first precursor SCF job (original SHA256 `2a90c4795b42b3a605fc9c8ff8408349456e504e63f802fa6edf3aa20264afc0`, 1045 bytes). The absolute build-tree prefix embedded in the conda-forge binary was replaced by `<conda-forge-build-tree>/`; the error text is otherwise unchanged. |
| `results/e01/raw/precursor-classification.json` | `0f4b0a2b9c8ee3468083af07e0e49d33773835078b2320bab38663a410539757` | Exact copy of the runner's classification of the precursor; identical to the original record. |
| `structures/README.md` | `74c8ceefb5adba69d1a37e511059662a5b081f38d05f5254d7d0d23eebc960a0` | New for the public export. |
| `structures/donor-activated-EAOGe-C2-radical.extxyz` | `bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3` | Adapted in its header only from the original record, SHA256 `6ed11860b16290b698115c7a1638c494a5b72b2d296598c193671c4212e09a04`, as described below. |
| `structures/donor-precursor-EAOGe-C2I.extxyz` | `0556643368a2def37779d5150ab946e410aa1880e4170972bab55cc787fb8bb9` | Adapted in its header only from the original record, SHA256 `da63de5442e7f644cfb52ed55b10c668964235249d27e63f794711f8244340b2`, as described below. |
| `tools/activated-donor-bonds.tsv` | `e8e4efcb1d019f6c8ce9c9c37ecf3047a552f3f30771de37a2f61949e4ff3fee` | New. It transcribes the 23 heavy-atom bonds of the activated donor from the atom-mapped SMILES in `docs/donor-candidates.md`, with atom-map numbers. |
| `tools/benchmark-reported-outcomes.tsv` | `ddf0f0a850397c559fe8f709dcdc0a23dd4bdf97ecad7a4e98b19c1e91852f73` | New. Machine-readable transcription of the four reported percentages, 95% confidence intervals and counts from the benchmark (section "Positional and chemical control of mechanosynthetic donation"); the values are identical to the table in `docs/benchmark.md`. |
| `tools/render_outcomes_chart.py` | `458e13c1c5cd0d789bac1c99068db250dc51978de297e61ae3d2e89a1bc4b265` | New. A deterministic standard-library renderer for Figure 2 on a 0 to 100 percent axis; it does not recompute values. |
| `tools/render_donor_plate.py` | `b452c4a53825b43b7c76e6f3d4bb665c0c0461e29458f159a1a1dd071458cabc` | New. A deterministic standard-library renderer for Figure 1; it reads, and never modifies, the structure file. |

## Notes on adapted and derived files

The method specification omits the rows that apply only to later stages: optimization thresholds, validation of
constraint output, basis, grid and proxy-size sensitivity, and later-stage resource caps and preconditions. It also
omits the worked witness table for the hypothesis rules and the name-only note on the next experiment. The
statement on Kohn–Sham stability was rewritten to match the scope of the inspected sources. Clarifications from
the current review were added, and the gradient floor, the energy-tie rule and the assignment *p* = *p*<sub>L</sub>
follow the original record.

The capability record summarizes inspection of cached sources. These are the Psi4 development-manual texts, with
SHA256 `4a624e8277c0679c6c054d94c0ea3263c3688dba3f62b8f5758e0e5415c2e7a8` (`scf`),
`7506acf7098966a1fd7ac7ed1df44e5a100c957c726eddf44779b79390de2888` (`oeprop`),
`546465d9a4695519600ecbe3404faf71b45493e6c042492b7fda177b929204ec` (`dft_byfunctional`) and
`531eb977c587798c22d7b323e4c13dff91bb662d10506bb4914cc7934cf0c8e7` (`basissets`). They also include the Psi4
`v1.11` source files `proc.py` (SHA256 `98ac648d84cc4587ec034b9207d3c6fbc3cd74df4c0409a85478e5467c0dd408`) and
`libxc_functionals.py` (SHA256 `e289d7d713e2ae9cecf8e37a22d80ed7fd9beed0c9febd0aa9282afd81c448fe`).

The E-01 files under `results/e01/raw/` were produced mechanically from the private run records by fixed literal
replacements only. Each redacted copy was checked for the absence of local paths, user names and host names, and
each JSON file was checked to parse. The job standard output of both jobs was empty (0 bytes) and is not published.
The E-01 run records were selected from the project's reviewed as-run evidence manifest of 45 files (SHA256
`6e7050b3fe02c237a9572b55e2f8a987517a14ffa8bae15db1992628c8cfdadc`) and preparation manifest of 33 files (SHA256
`0d5d018df63b88ec4a00d1d4f0aaa9366324bcdf789978e66d3cd59293d5d10a`).

In both structure files only the second line, the header, was changed. The internal task identifier was removed.
The private cache file names in the literature locator were replaced by "Barrera et al. arXiv:2512.24431 SI p15",
and the keys `public_adaptation=` and `original_sha256=` were added. The atom-count line and every atom line are
byte-identical to the original records.

## Redaction and adaptation policy

The public files never contain local file-system paths, user names or host names. Nor do they contain internal
session, task or runtime identifiers, the names of agent models or configurations, credentials, or
orchestration-layer records such as authorization, review, accounting and control records. Third-party paper text,
figures, supplementary material and vendor source code were excluded from this export pending redistribution
review; facts from these sources, such as identifiers, reported counts and declared parameter values, are cited
with locators rather than copied. An adapted file is labelled as adapted, with the SHA256 of its original and a
statement of what was removed or changed. It is not the original hash-bound record, and its hash differs from the
original's.

## Material omitted from this export

The following material is retained privately.

| Material | Reason for omission |
|---|---|
| Surface-model coordinate files and their constraint sidecars (three models) | They are not inputs to the first calculation, and their placeholder geometry could be mistaken for a benchmark model. The definitions are summarized in `docs/donor-candidates.md`. |
| Donor graph record, generator and checker scripts, and their logs | The generator reads locally cached third-party supplementary text, which is excluded pending redistribution review. The logs contain local paths. |
| Workflow-provenance test records and installation logs | They are specific to the environment, contain local paths and are not chemistry evidence. |
| Earlier frozen documents (feasibility study, original architecture, tool landscape, source ledger, environment record) and the source addendum | They contain internal references, superseded status and milestone framing, and cache paths. The relevant facts are restated with attribution. |
| Cached third-party papers, supplementary material and vendor documentation or source | Excluded pending redistribution review. They are cited by identifier and hash. |
| Authorization, review, accounting, control and incident records; superseded attempt copies | They are orchestration-layer and process records, not scientific content. |
| E-01 runner, classifier, resource-control and job scripts; gate, ledger, journal, launcher and scratch-observation records; provenance receipts and the provenance-system store | They are orchestration-layer records or contain local paths and internal identifiers. Their values relevant to the result are transcribed in `results/e01/outcome.json` with source SHA256 values. |
| E-01 job scratch files | They were removed after the job, as recorded, and were never retained. |

This export is not a complete archive of the project's work.

## Revision history

The initial public export contained 19 files. The editorial revision rewrote every explanatory document as
continuous prose without changing the scientific content. It also replaced the earlier figures with Figure 1 and
added the Figure 1 renderer and bond table. Five figures were retired; their final SHA256 values were:
- `docs/figures/masthead.svg`: `a0b101bce37e7630c5929c62e25fda593a1e2758d387ba7bea58b03b837d0a9e`
- `docs/figures/architecture.svg`: `ab98975d49e50bce0d0af1a9173ec2e2a9b86e82abd9695a861edfc536e141ca`
- `docs/figures/evidence-classes.svg`: `2a3ff687c8336214c72c5f6d25a54a1ce052c949c1063f18c2f07c76cfbb1d0a`
- `docs/figures/e01-validation-flow.svg`: `7492655a1a19d438278a7c5ba3c034b8a5e1baf2fa0460fa04fa8aac6618cfc0`
- `docs/figures/reported-outcomes.svg`: `9272328a658d57816e3a6cbe99191d4daf1ddf37ad96ac29b41a5937ab4a6c51`

A later revision added Figure 2, an original point-and-interval chart of the reported outcomes, with its renderer
and input table. It replaces the duplicate table in the README; the exact values remain tabulated in
`docs/benchmark.md`.

The revision of 2026-09-24 added the E-01 result under `results/e01/` (nine files) and revised `README.md`,
`AGENTS.md`, `.agents/RESEARCH-STATE.md`, `docs/SOURCES.md`, `docs/evidence-policy.md`, `docs/donor-candidates.md`,
`docs/e01-method-specification.md` and `docs/engine-capability-status.md` to report the stopped attempt. Both
figures, both structure files, both renderers and their input tables are byte-identical to the previous export.
