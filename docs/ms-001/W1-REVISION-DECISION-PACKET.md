# W1 specification revision 01: decision packet

Date: 2026-10-04. MS-001 scope option B, before Stage 1. Status: **decision support for a person. One revision is
recommended as an `[AGENT]` proposal and bound to exact bytes. Nothing is chosen, approved or applied.**

This packet prepares a person's decision on revising [C3-WIRING-TEST-PROPOSAL.md](C3-WIRING-TEST-PROPOSAL.md), the
specification of the non-chemistry wiring test W1, so that the two blockers and the unresolved requirement recorded by
the [W1 pre-run determination](W1-PRE-RUN-DETERMINATION.md) are resolved or explicitly disposed:
- **W1-BLOCKER-E2.** The Stage 0 interpreter's `os.environ` holds `__CF_USER_TEXT_ENCODING`, a name outside the
  five-variable allow-list.
- **W1-BLOCKER-E1.** The specification declares both driver files "tracked at the declared commit", and no commit is
  authorized.
- **U-F1P.** The capture of ignored or private source files has no conforming design.

It also disposes the seven gaps coupled to them (Section 4). It compares the options, recommends one combination,
gives the exact replacement text, marked **UNAPPLIED**, binds the resulting whole-file bytes by SHA256 (Section 9),
and ends with the decision a person can take on those bytes (Section 11).

What this packet is not:
- **Not the decision.** Only a person decides. Reviewing, accepting or publishing this packet is not that decision.
- **Not a change.** The specification stays byte-identical at SHA256
  `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158`. Frozen Stage 0 definitions, human decision
  records and the other artifacts bound in the [freeze record](STAGE0-FREEZE-RECORD.md#2-frozen-artifacts) remain
  unchanged, while the package-index navigation binding is refreshed: the bound package index changed, for
  navigation only.
- **Not a run.** W1 was not run. No AiiDA profile, computer, code or job was created, AiiDA, ASE and NumPy were not
  imported, and no chemistry engine ran. Nothing was installed or retrieved.
- **Not a prediction.** A revised W1 is not predicted to pass.
- **Not authorization.** Nothing here authorizes a run of W1, Stage 1, Stage 1a, Stage 1b or Stage 2.

## 1. Evidence and labels

Labels follow the [evidence policy](../evidence-policy.md). No chemistry evidence class applies to anything here.
- **Source facts** are `[LIT]` software provenance: statements of what a cited source text defines, with file and line
  locators. They describe no run on the host.
- **Observations** are software or environment observations of this project, made by read-only inspection and
  hashing. Their commands, outputs and exit codes are retained privately and bound by digest (Section 1.3).
- **Everything else** (options, recommendations, replacement text, inferences) is `[AGENT]`. Where a statement rests
  on neither a source locator nor an observation, it is marked `[AGENT]` and, where it matters, *not established*.

### 1.1 Source facts

Read from the retained wheel of the Stage 0 hash-locked installation, aiida-core 2.9.2, SHA256
`72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd` ([SOURCES.md](../SOURCES.md), entry [34]),
as text, without extraction, installation or import.

| # | Fact `[LIT]` | Locator (aiida-core 2.9.2) | Member SHA256, bytes |
|---|---|---|---|
| A12 | Importing the configuration-settings module calls `AiiDAConfigDir.set()`, which creates the configuration directory and its daemon, daemon-log, broker, log and access-control subdirectories. The directory comes from `AIIDA_PATH` when that variable is set, with `.aiida` appended unless the path already ends in it, and is otherwise `~/.aiida`. The default `~/.aiida` path is computed at import even when `AIIDA_PATH` is set | `aiida/manage/configuration/settings.py` 20–30, 35–60, 97–129, 132–168, 171–172 | `b9b75a9e4c7e020893813386268d618f24281a52eb4ac1c93ab546abe76ed4dc`, 6 931 |
| A13 | Opening the local transport sets its internal directory to `os.path.expanduser('~')` | `aiida/transports/plugins/local.py` 58–70 | `e34aaebbe13930d15d17eba2244091ae543b2fd692afd12a3af6d26f25cc8561`, 39 702 (also in the [pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md)) |

The facts A1 to A11 of the specification are used as the specification states them and are not restated.

### 1.2 Observations

Each row is a software or environment observation of this project. "The declared Git environment" is the one the
revision proposes: exactly `PATH=/usr/bin:/bin`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`
and `GIT_OPTIONAL_LOCKS=0`, with no `HOME`. Every statement about which files are untracked or ignored holds only for
the environment named with it. Each result holds at the probed state, before this packet's own documentary changes.

| Ref | What was done | Result |
|---|---|---|
| G1 | Read this repository's index under the declared Git environment | 77 entries, every mode `100644`, so no symbolic link and no submodule entry; no `.gitmodules`; every `ls-files -v` tag `H`; no staged and no unstaged change; object format `sha1`; index version 2; no split-index file; Git 2.39.5 (Apple Git-154) |
| G2 | Listed untracked files with `ls-files --others --exclude-standard`, and the configuration sources Git reads, in three environments | **Operator's ordinary environment, with `GIT_OPTIONAL_LOCKS=0`:** no untracked file; configuration read from the repository, from a toolchain-level file and from the user's own file. **The five declared W1 variables with `GIT_OPTIONAL_LOCKS=0`, no `HOME`:** exactly one untracked file, a local tool-settings file that a user-level ignore file hides in the ordinary environment; configuration read from the repository and the toolchain-level file; `git config --global` fails with `$HOME not set`. **The declared Git environment:** the same one untracked file; configuration read from the repository only |
| G3 | Searched the working tree for symbolic links | None outside the repository's git-ignored private area, and none in the Stage 0 environment's `site-packages` |
| G4 | Commit-free measurement on separate temporary index files, each populated from the tree of the baseline commit, which leaves their file-system metadata unset. Each command ran once against its own temporary index; the raw bytes of that index and its `ls-files --stage -z` output were hashed before and after | Porcelain `git diff --binary <commit>` rewrote the temporary index both with `--no-optional-locks` and with `GIT_OPTIONAL_LOCKS=0`. `git status` rewrote it only without the lock policy. `diff-index -p --binary <commit>`, `diff-files -p --binary` and `ls-files --others` did not rewrite it. The `ls-files --stage -z` output never changed and equalled that of the repository's own index, whose raw bytes stayed unchanged. **Not established by G4:** behaviour on the repository's own index, on an index with only some stale entries, or with options other than those listed |
| G5 | Read this repository's index flags and listing under the declared Git environment | Every `flags:` field printed by `ls-files --debug` is `0` (77 of 77); every entry has stage `0`; raw index bytes unchanged before and after |
| G6 | Ran, read-only, the exact Git invocations that the revision declares (`--version`; `rev-parse --show-object-format`, `--git-path index` and `--verify HEAD^{commit}`; `ls-files --stage -z`, `--debug` and `--others --exclude-standard -z`; `diff-index -p --binary --no-color --no-ext-diff --no-textconv --no-renames --src-prefix=a/ --dst-prefix=b/ <commit>`) under the declared Git environment | Each produced its output with no error output; the code diff of the clean tree was empty; one untracked file was listed; raw index bytes unchanged before and after. The exit status of `diff-index` itself was not captured |
| G7 | Read, under the declared Git environment, the origin and name of every effective configuration entry, and searched for attribute and exclude files | Every entry comes from the repository's own `.git/config`, 12 keys. None is an include or includeIf key, `core.excludesFile`, `core.attributesFile`, `core.fsmonitor`, `core.untrackedCache`, `core.splitIndex`, `core.worktree`, `core.hooksPath`, or a `filter.*`, `diff.*`, `index.*` or `extensions.*` key. No `.gitattributes` file is tracked, and the only `.gitattributes` files in the working tree lie in one git-ignored directory that holds no tracked or listed untracked path. No `.git/info/attributes` exists. `.git/info/exclude` holds one rule. The raw index bytes were unchanged before and after |
| S2 | Counted the files of the Stage 0 environment's `site-packages` | 18 448 files, 374 182 654 bytes: 6 834 `.py` files, 6 834 `.pyc` files, 180 `.so` extension modules, 33 dynamic libraries and 4 567 other files; no top-level `.pth` file |
| S3 | Read the frozen input file (SHA256 `bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3`) as text | 48 atom lines of 7 fields each, header `Properties=species:S:1:pos:R:3:atom_id:S:1:map_num:I:1:radical_electrons:I:1`; no field holds a character outside printable ASCII, a `"` or a `\` |
| W1 | The observations of the [W1 pre-run determination](W1-PRE-RUN-DETERMINATION.md), Sections 3 and 4 | Used as recorded there, including the six-name `os.environ` under `-E -s`, the inheritance by `/usr/bin/env` and a simulated shell chain, the absence of the name under `/bin/bash` alone, and that startup under `-E -s` loads no module from `site-packages` |

No observation used here depends on creating a new commit or on either P04 scratch commit. P04 names two earlier
probes made while this packet was prepared, each in a throwaway repository with a commit of its own; none of their
results is used here. G4 and G6 read the pre-existing baseline commit.

### 1.3 Private evidence bound by digest

The commands, outputs and exit codes of G1 to G7, S2 and S3, and the source reads of A12 and A13, are retained
privately because they contain local paths and host details. They are identified here by SHA256 only.

| Record | SHA256 |
|---|---|
| Digest list of the private evidence of this packet | `8acf945403fd49f506e9597bf08270f2fb20ee7bd2c7afa19a87f67aa4d099c7` |

## 2. The evidentiary contract and what each blocker touches

| Item | Clause of the specification | Criterion and stop condition it governs |
|---|---|---|
| W1-BLOCKER-E2 | §5 item 1; §3 payload record, `/usr/bin/env` row; `env_policy` | §7 criterion 4, first bullet; §8 stop conditions 2 and 10 (payload record) |
| W1-BLOCKER-E1 | §2, "Class and module" | None repeats it; it is a declared requirement (W1 record §3.2) |
| U-F1P | §4, "Ignored and private files" and "One capture" | §7 criterion 3; §8 stop condition 6 |

A **relaxation** below means a change that lets W1 pass where the current text would make it fail or stop. A
**change of coverage** means a change of what is checked, stated as gained or given up. Neither is applied to a
recorded result: no W1 result exists.

## 3. Options and recommendations for the blockers

### 3.1 W1-BLOCKER-E2: the platform-injected name

| Option | What changes | Testable on this host | Effect on the evidentiary contract |
|---|---|---|---|
| E2-O0. No change | Nothing | No: §8 stop condition 2 triggers at the runner's first record (W1 record §3.1) | Keeps the strict rule; W1 cannot pass with the Stage 0 interpreter on this host |
| E2-O1. Three records with one declared platform-injected name (W1 record option O1, refined) | A **launcher record** keeps the five-name rule exactly. The **interpreter record** may also hold the declared name `__CF_USER_TEXT_ENCODING`. The **payload record** may hold it too, with the interpreter's value | Yes: the launcher builds and records its mapping; the name's presence in the interpreter and its inheritance are already observed (W1 record §3.1) | **Relaxation**, prospective and for one named name only: §5 item 1 and the §3 payload rule admit it in the interpreter and payload records. Kept: the five-name launcher environment, the allow-list values everywhere, and failure on any other name. Given up: the claim that every shell ran in exactly the five declared variables plus the job's own |
| E2-O2. A different interpreter without CoreFoundation (W1 record option O2) | §2's environment and possibly the lock | Not now: needs an installation that "Nothing is installed" excludes, and a new environment | Keeps the strict rule, at the cost of a different, unverified environment and its own determination |
| E2-O3. Record, then remove | The runner records `os.environ`, then deletes the name before any import or child | Not established: whether removal propagates to every child and whether the name reappears was not observed, because no new probe was permitted | Keeps the payload rule strict, but makes F7 describe an environment the runner altered. The observed propagation would no longer be visible in the payload |
| E2-O4. Widen the allow-list to six | `allow_list` gains the name | Yes | **Relaxation** that also admits the name in the launcher environment, where it was not observed, and so erases the distinction the observation shows |
| E2-O5. Declare the name in the launcher | The launcher sets it to a fixed value | Yes | Masks whether the platform injects it, and makes a platform value a declared one |

**Recommendation `[AGENT]`: E2-O1.**
1. It is the only option testable now that neither erases nor masks the observation. The name is recorded where it was
   observed, in the interpreter and its children, and its absence from the launcher's mapping stays checked.
2. The five-name rule survives where it was always meant to hold: the environment the runner is started with.
3. The relaxation is explicit, prospective and limited to one named name with a checked value. Any other name still
   fails, and a later addition "afterwards" is still forbidden.
4. E2-O0 leaves W1 unexecutable with the declared interpreter. E2-O2 needs an installation outside the current
   boundary. E2-O3 rests on unobserved behaviour and alters what F7 describes. E2-O4 and E2-O5 hide where the name
   comes from.

The cause of the name is not established. That CoreFoundation, which the interpreter binary links, sets it remains an
`[AGENT]` inference (W1 record §3.1). The recommendation does not depend on the cause.

### 3.2 W1-BLOCKER-E1: tracked drivers

| Option | What changes | Provenance it gives | Limitation in provenance terms |
|---|---|---|---|
| E1-O0. No change | Nothing | Commit identity, if a commit is ever made | W1 cannot run without a delivery decision, which a test authorization does not include |
| E1-R-E1a. Untracked capture (W1 record option R-E1a, refined) | The drivers are untracked; §4 captures their bytes with SHA256 and Git blob identifiers, as inputs of each job | Content identity: the exact bytes, retained in the provenance store and resolvable by digest; the blob identifiers let a later commit be matched to the bytes that ran | No position in a commit history, no author or time from Git, and no public reference until the bytes are published. Identity is by content in a private store |
| E1-R-E1b. Commit before the run (W1 record option R-E1b) | A person separately decides to commit the drivers | Commit identity in the history, publicly referable once pushed | Couples a delivery decision to a test. A commit still says nothing about what ran unless F1 shows no difference |
| E1-O3. Stage the drivers | `git add` | None beyond R-E1a | Changes the index without authorization and still is not "at the declared commit" (W1 record §3.2) |

**Recommendation `[AGENT]`: R-E1a.**
1. The evidence policy requires, as code identity, the "Commit of every code path used; for uncommitted code, the
   full diff, hashed" ([evidence policy §4](../evidence-policy.md#4-provenance-required-for-a-future-result-or-figure)).
   For tracked code, the code diff against the declared commit is that diff. The two drivers are new, untracked files,
   which a diff against the commit does not contain. The proposal's treatment of such new code is R-E1a: their full
   bytes, hashed, with Git blob identifiers, retained in the store as inputs of each job.
2. It keeps delivery and testing as separate decisions.
3. The blob identifiers make a later, separately authorized commit checkable against the bytes that ran, without
   making the commit a precondition.
4. E1-O0 and R-E1b both make W1 wait for a delivery decision. E1-O3 is a delivery-adjacent mutation and does not meet
   the declaration either.

### 3.3 U-F1P: ignored and private files

The environment lies in the repository's ignored area (W1 record §3.3), so every module file loaded from it is an
"ignored or private source file used". The base text's node boundary (§3) makes every F1 item a required input of
each of the two jobs. The import set of a run is unknown: AiiDA has not been imported here, and the W1 record found
no observed import set on which a declared list could be based.

| Option | What changes | Effect on the evidentiary contract |
|---|---|---|
| U-O0. No change | Nothing | U-F1P stays unresolved; W1 stays blocked |
| U-R-P1. Exempt the environment, rely on `RECORD` (W1 record option R-P1) | Environment files are left out of §4 | **Relaxation**: the `RECORD` comparison would stand in for byte retention. It retains nothing, covers only hashed `RECORD` entries, and its bytes resolve only from the retained wheels outside the store |
| U-R-P2. Capture only what was loaded, with late loads captured after job 2 into a separate node (W1 record option R-P2, made concrete one way) | `code_private` holds the environment module files listed at the input point; files first loaded later are captured after job 2 into a folder node that neither job links | **Reduction**: late-loaded environment files would not be required inputs of either job, contrary to the base node boundary, and would be captured after use. The C3 coverage of F1 for those files would stay unestablished |
| U-R-P2s. Capture only what was loaded; any later first load stops W1 | The late-load rule | Keeps every captured file input-linked, but W1 would stop unless the import set were known in advance, and it is not known |
| U-R-P3. Declared superset plus observed subset (W1 record option R-P2, made concrete another way) | `code_private` holds every regular file of the environment's `site-packages`, captured before any import outside the standard library and linked as a required input of each job. Two module listings, at the input point and after job 2, record separately which files the loaded modules name | **Change of coverage**, with the obligations kept apart: §3 tests correspondence to the wheels, and §4 retains bytes. Gained: every environment file, data files, bundled libraries and cached bytecode included, is retained before any of it loads, as an input of both jobs; "what was available" and "what was observed loaded" stay separate records. Given up, and named: an executed-code guarantee, which neither obligation gives |
| U-R-P4. As U-R-P3, but the superset stored outside the job inputs | A separate node | Retains everything but links none of it to the jobs |

**Recommendation `[AGENT]`: U-R-P3.**
1. It keeps the base node boundary: every F1 item, every environment file included, is a required input of each
   job. Nothing is captured after use, and no unlinked node is needed.
2. It does not need the import set in advance. The superset is declared by location, the observed subset is recorded
   separately, and the two stay distinguishable.
3. It keeps §3's `RECORD` test and §4's byte retention as two obligations, and states what each covers and what
   neither covers (Section 4.7).
4. Its costs are stated:
   - **Size.** At the probed state `site-packages` held 18 448 files and 374 182 654 bytes (S2). The size at a run
     is recorded, not assumed.
   - **Volume through each job.** By the base text's own rules, each job folder receives these files under
     `w1_inputs/code_private/` (§3 ports table), the payload's input manifest digests each of them (§3), and the
     three-way binding covers each of them (§5).
   - **Feasibility.** Whether aiida-core's upload and storage handle that volume is unobserved, because AiiDA was not
     imported. The re-determination must establish it.
   - **Unloaded code.** `[AGENT]` judgement, with no measured ratio: the superset includes code that will not be
     loaded. The listings, not the capture, say what was loaded.
5. U-R-P1 lets a test stand in for retention. U-R-P2 makes late-loaded environment files not required inputs of
   either job, against the base node boundary, and leaves the C3 coverage of F1 for them unestablished. U-R-P2s
   depends on an import set no one has observed. U-R-P4 links nothing.

None of these options closes a C3 blocker. C3 readiness remains BLOCKED.

## 4. The seven coupled gaps

Each gap gets a disposition: **exact text** (in the replacement blocks of Section 8), **bounded limitation**, or
**contingent**. None is waived.

### 4.1 G-1. The index state

| Option | Definition | Assessment |
|---|---|---|
| IX-raw | SHA256 of the raw bytes of `.git/index` | Rejected. G4 shows a porcelain `git diff --binary <commit>` rewriting the raw bytes of a temporary index even with optional locks disabled, while its entries stayed unchanged. `[AGENT]` By that observation, the current text's own diff could stop W1 under a raw-byte definition, and so could any process refreshing the index |
| IX-sem | SHA256 of the exact output of `ls-files --stage -z`: mode, object name, stage and path of every entry | **Recommended.** G4 shows this output unchanged across those rewrites and equal between a rewritten index and the repository's own |

**Disposition: exact text.** The revision declares:
- **The invocation.** Every Git command is `/usr/bin/git --no-optional-locks <subcommand>`, started without a shell
  in the declared Git environment, with the repository root as working directory. System and user-level
  configuration files are not read, by `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null` and the absence of
  `HOME` (G2). The no-optional-locks policy is set twice, by option and by variable.
- **The repository's own configuration, bounded.** Excluding the system and user files does not by itself exclude
  what the repository's configuration can reach. The revision therefore states conditions, checked at both
  instants, that every configuration entry comes from `.git/config`. It also requires that no include or includeIf
  key, `core.excludesFile`, `core.attributesFile`, `core.fsmonitor`, `core.untrackedCache`, `core.splitIndex`,
  `core.worktree`, `core.hooksPath`, `filter.*`, `diff.*`, `index.*` or `extensions.*` key is set. No
  `.git/info/attributes` may exist, and no `.gitattributes` file may lie in the root or in any directory above a
  tracked or listed path. The digests of the configuration listing and of `.git/info/exclude` are recorded and
  compared. All of these hold at the probed state (G7). Git's compiled-in defaults and the program behind
  `/usr/bin/git` are not bounded; they are recorded only through the Git version.
- **No index writes by W1.** Only `config`, `rev-parse`, `ls-files`, `diff-index` and `--version` are used. G6 ran all
  of them except `config --list --show-origin -z`; G7 read the same keys and origins with `--name-only` in place of
  `-z`. `ls-files` and `diff-index`
  did not rewrite an index in G4. The porcelain `git diff` is replaced by `diff-index` with explicit options.
- **The raw index** is recorded at both instants and observed only.
- **Under the declared environment no user-level ignore rule applies.** In that environment, at the probed state, the
  untracked listing included one local tool-settings file that the ordinary environment hides (G2). The capture is
  therefore wider than in the ordinary environment, never narrower: that file is captured as bytes, and any change
  to it during the run stops W1. Its content is a local file of the account. It stays in the private store and is
  never published.
- **Symbolic links, submodules and flagged entries.** None occur at the probed state: every mode is `100644` (G1),
  and no symbolic link lies outside the ignored area or in `site-packages` (G3). The revision makes their later
  appearance a stop: a symbolic link or directory among the tracked or listed paths, a symbolic link in
  `site-packages`, an entry with mode `160000` or a non-zero stage, or any non-zero `flags:` field of `ls-files
  --debug`. Which markings set which flag bits is *not established* here
  `[AGENT]`; the rule is conservative and stops on any non-zero field. Every field is `0` now (G5).
- **Unstaged modifications** can occur, for example from uncommitted documentation. They are captured by the code
  diff against the declared commit, staged and unstaged together, and the index state records the staged state.
  Tracked-file digests are recorded independently of Git's change detection.

**Bounded limitations.** That `diff-index` with the added options never rewrites the repository's own index rests on
G4 and G6 together, not on an observation of every case. Whether a refresh of the repository's index by another
process during a run could change the `ls-files --stage -z` output is not established; it would not change any entry
by G4, and any change of that output stops W1.

### 4.2 G-2. The bytecode policy

| Option | Assessment |
|---|---|
| BC-0. No change | Rejected. `-E -s` alone sets no policy, so bytecode files could be written into the repository or the environment between the capture and the run end, and whether that "changes" F1 is left undefined |
| BC-1. `-B` on both interpreter invocations, a recorded `sys.flags.dont_write_bytecode` that must be `1`, and a listing of every `__pycache__` file at both instants, any change stopping W1 | **Recommended.** It changes the §2 invocation to `-E -s -B` and makes "no bytecode is written" a checked fact of the run rather than an assumption |
| BC-2. Writes permitted and observed only | Rejected. It leaves F1's "any change stops the test" in conflict with expected writes |
| BC-3. BC-1 plus a separate, empty bytecode-cache prefix, so that existing cached bytecode is not read | Not recommended now. Its effect on this interpreter was not observed, because no new probe was permitted. It may be proposed after the re-determination |

**Disposition: exact text (BC-1).** `[AGENT]` that `PYTHONDONTWRITEBYTECODE` is ignored under `-E` is not
established by an observation here. BC-1 does not rely on it, because it uses the flag and checks
`sys.flags.dont_write_bytecode`. **Interaction with F1 and F3:** with no bytecode written, a bytecode change is
always a stop, never an expected side effect. Existing cached bytecode, 6 834 `.pyc` files beside 6 834 `.py`
files in `site-packages` (S2), stays observed only for correspondence (F3); `[AGENT]` that the interpreter reads it as
usual under `-B` is not established here. Its bytes are now also retained for project and environment modules (G-7).

**Stability and correspondence are kept apart.** The `__pycache__` comparison is a stability check: the same bytes
at the capture point and at the run end. It is not a correspondence check, so it never claims that cached bytecode
matches the locked wheel or the module's source. The revised text says so in each place where the base text said
that cached bytecode is "observed only": the opening limits (R02a), Section 3 (R12, R12a), criterion 5 (R22a), stop
condition 11 (R26a) and Section 10 (R29a). Correspondence stays unestablished everywhere. Stability is required
under criterion 3 and stop condition 6.

**One byte serialization.** The environment listing, the bytecode listing and the listings of declared runtime data
share one exact serialization, "Listings" in the revised §4. It fixes the UTF-8 encoding, three fields (a root-tagged
relative path, the decimal size and the lowercase hexadecimal SHA256), one TAB between fields, one LF after every
line including the last, byte order of the path field, and a stop for a path that cannot be serialized. Two
independent implementations therefore produce the same bytes and the same digest.

### 4.3 G-3. User-level side effects beyond `~/.aiida`

**Disposition: exact text.** A12 and A13 show AiiDA computing paths from `~` even when `AIIDA_PATH` is set. How the
interpreter expands `~` without `HOME` is *not established* here `[AGENT]`; the absence of `HOME` is therefore not
treated as protection. The launcher observes, before the runner starts and after it ends, a declared set of paths
relative to the account's home directory as the password database gives it: the home directory itself, `.aiida`,
`.ase`, `.cache`, `.config`, `.local`, `.local/share`, `Library/Caches`, `Library/Application Support`,
`Library/Preferences` and `Library/Logs`. For each it records existence, type and the names and types of its direct
entries. Any difference stops W1. The resolved home directory is private.

**Bounded limitations.** A change deeper in an existing directory, or elsewhere, is not detected. Another process
can cause a stop.

### 4.4 G-4. `code_identity`

**Disposition: exact text.** Eighteen keys, each with value kind, source and comparison, in a table under "The F1
code identity" in §4, and a `code_identity` row in §3's "Mandatory contents", with the rule for *recorded* values
extended to name that table. They include the digests of the bounded Git configuration and of `.git/info/exclude`.
Criterion 5 now checks `code_identity` key by key.

### 4.5 G-5. `fixture_diff`

**Disposition: exact text.** Its bytes are a declared 94-byte constant in `w1_job.py`, with SHA256
`f3a3deb5cd0693c76b9bff397e811bff75eb253cb5f42265fe68e6582fdea609`. They are written from that constant, so they
are deterministic. The checker compares them with the constant in the captured `w1_job.py` and with their store key,
and resolves them through the same function as `code_diff`. The fixture never stands for the code state. Criterion 7
and a stop condition cover its failure.

### 4.6 G-6. The sidecar's bytes

**Disposition: exact text.** The sidecar is one JSON object, serialized as Python's `json.dumps` writes it with
`ensure_ascii=True` and `separators=(",", ":")`, followed by one LF. Its keys and their order are declared. Every
value except the site index and `position` is a JSON string holding the exact text of its field in the frozen file,
and `position` is an array of the three coordinate strings. S3 shows that no field needs an escape. Because the
frozen header declares `map_num` and `radical_electrons` as integer-typed (S3), a native array of either is compared
with the sidecar's string through a declared base-10 reading, for comparison only; a native `atom_id` array is
compared as strings (R18a). The checker regenerates the sidecar from the frozen file and compares it byte for byte with job 1's
`identity`, which gives "identical at every step" a declared referent.

### 4.7 G-7. Capture timing, late loads, extension modules and the two obligations

**Disposition: exact text, with bounded limitations.**
- **Timing.** The capture point comes after the interpreter record and the first F3 reading, and before any import
  outside the standard library. Startup under `-E -s` loads no module from `site-packages` (W1 record §4), so the
  environment is captured before any of it loads. The first module listing is taken at the input point, after
  `w1_job` is imported and the profile loaded and before any input node is created. The second is taken after job
  2. Each comes from a one-statement copy of `sys.modules`, and each is a file inventory.
- **Late loads.** A module first listed at the run end is checked like any other:
  - an environment module file must be in `code_private` with an equal SHA256 and pass its `RECORD` check, so its
    bytes were captured before it loaded and are inputs of both jobs;
  - a project module file first listed at the run end stops W1;
  - a standard-library module file is recorded by digest;
  - any other module file stops W1.
- **Extension modules.** Extension modules count as module files. Their bytes are compared with `RECORD` and captured
  as bytes. They are machine code, not readable source. Libraries bundled in `site-packages` are captured with the
  superset. Libraries that the dynamic loader loads from elsewhere are neither captured nor enumerated.
- **Two obligations.** The `RECORD` comparison covers every file that a `locked-verified` wheel's `RECORD` lists with
  a non-empty hash, loaded or not, except bytecode cache and `.data/scripts/` files. It retains nothing and is the
  only correspondence test. The F1 capture retains every file of `site-packages`,
  with the project's code, as inputs of each job, and tests no correspondence. Neither covers the standard library's
  bytes, the interpreter binary, `/bin/bash`, the declared runtime data, libraries loaded from outside
  `site-packages`, or frozen modules.
- **Source and data apart.** The capture is about code. The run's declared runtime data are listed as data, not
  source:
  - the W1 configuration directory and `TMPDIR`, listed at both instants and observed only;
  - the profile's storage, covered by the closure inventory;
  - the work directory, whose submission files are bound by Section 5.

  A module file elsewhere in the ignored area stops W1.
- **File inventory, not executed code.** Every check supports a file inventory. None supports an executed-code
  guarantee, for the reasons the revised §4 lists, and W1 claims none.

**Bounded limitations.** A module loaded and removed between the two listings is in neither. That the bytes a module
loaded equal the captured bytes rests on the capture-point and run-end readings, not on an observation at load time.
The volume of the capture at a run, and how the job machinery handles it, are unknown until the re-determination.

## 5. Answers to the four questions

**1. Which E2 treatment is testable on this host and honest about a platform-injected variable?** E2-O1, with three
separate records:
- **Launcher record.** The explicit mapping the launcher passes to the runner. It must be exactly the five declared
  names and values. The injected name must not be in it.
- **Interpreter record.** `os.environ` right after `import os` in the runner, and again after job 2. It must hold every
  allow-list name with the launcher's values, may hold the declared injected name, and may hold nothing else. The
  injected name is recorded with its value where it appears, and its absence is recorded too.
- **Payload record.** The `/usr/bin/env` output. It may hold the declared injected name, with the interpreter's
  value.

The observation is not erased, the five-name environment stays verifiable at the launcher, and the allow-list is not
widened: the injected name is a separate, declared key of `env_policy`.

**2. Should E1 keep commit identity through a delivery gate, or can untracked byte capture suffice?** For a
software-wiring test, untracked byte capture gives equivalent content identity, the same bytes under the same digests.
The evidence policy asks, for uncommitted code, for "the full diff, hashed". The code diff gives that for tracked files;
for new, untracked files the proposal captures their full bytes, hashed, as its treatment of new code. It does not
give equivalent
provenance. It has no place in a commit history, no Git authorship or time, and no public reference until the bytes
are published. A commit through a separate delivery gate would give those, at the cost of coupling delivery to
testing. The blob identifiers let a later commit be checked against the bytes that ran. Recommended: R-E1a.

**3. What is the minimum coherent F1 private-source capture contract, and how does it interact with `RECORD`?** The
contract of G-7 has these parts:
- a capture point before any import outside the standard library;
- the bytes of the project's code and of every file of the environment's `site-packages`, a declared superset,
  retained as required inputs of each job;
- two module listings, at the input point and after job 2, that record separately which files were observed loaded;
- four classes plus "no file", with a late project load stopping W1;
- a `-B` bytecode policy whose check is stability, not correspondence;
- the run's runtime data declared as data, not source.

It is the smallest contract found here that keeps the base node boundary without knowing the import set. A
loaded-only capture either stops W1 on any late load or leaves late-loaded files unlinked (Section 3.3). `RECORD`
verification and byte retention are separate obligations. The first tests correspondence to the locked wheels for
every file that a `RECORD` lists with a non-empty hash, loaded or not, except bytecode cache and `.data/scripts/`
files. The second retains bytes. Neither discharges the other, and neither gives an
executed-code guarantee.

**4. Which coupled omissions need exact text, and which may stay bounded limitations?** All seven need exact text
before W1 is executable. Within them, these stay bounded limitations, each named in the revised text:
- that the bytes a module loaded equal the captured bytes, which rests on two readings;
- the volume of the superset at a run, and how the job machinery handles it;
- modules loaded and removed between the listings;
- Git influences beyond the bounded configuration, recorded only through the Git version;
- deeper user-level changes;
- the reach of G4 to the repository's own index;
- the cause of the injected name.

## 6. Recommended combination

E2-O1, R-E1a and U-R-P3, with exact text for all seven coupled gaps: the semantic index state with a bounded Git
configuration, the `-B` policy, the user-level observation, and declared `code_identity`, `fixture_diff` and sidecar
bytes. One relaxation is made, for a single named, platform-injected environment name, before any run. Two changes
of coverage are named:
- byte retention of every file of the environment's `site-packages`, as inputs of each job, beside separate listings
  of what was observed loaded;
- the absence of any executed-code guarantee.

The node boundary of the base text is kept: every F1 item is a required input of each job. The rest of the
specification is unchanged. No C3 blocker is closed, and C3 readiness remains BLOCKED.

## 7. Consequential effects

| Specification element | Effect of the recommended revision |
|---|---|
| §2 invocation | Becomes a launcher and a runner, each `-E -s -B`; the runner's environment is exactly the launcher record |
| §7 criterion 3 | Requires every F1 item to be an input of both jobs, and every comparison of the revised §4 to hold |
| §7 criterion 4, first bullet | The launcher record and the interpreter records replace the single parent-environment record |
| §7 criterion 5 | Adds `code_identity` to the inputs checked key by key, and checks the module files of both listings |
| §7 criterion 7 | New: equal user-level observations, and the fixture-diff check |
| §7 criteria 1, 2, 4b–4d, 6 | Unchanged |
| §8 stop condition 1 | Adds a difference between the user-level observations |
| §8 stop condition 2 | Becomes the three-record rule |
| §8 stop condition 6 | Becomes "a precondition or comparison of §4 fails", bytecode stability and the bounded Git configuration included |
| §8 stop condition 11 | A cached bytecode file stops W1 only through the stability comparison, never through correspondence |
| §8 stop conditions 14 and 15 | New: a late project or unclassified module file, and a failed fixture-diff check |
| §8 stop conditions 3–5, 7–10, 12, 13 | Unchanged in text; condition 10 now applies to the payload rule as revised |
| §9 private artifacts | Add the launcher and interpreter records, both user-level observations, and the capture record with the module listings, the environment, `__pycache__` and runtime-data listings and the run-end comparisons |
| §10 limits | Add the platform-injected name, the file-inventory limit, the drivers' content identity, and the scope of the user-level observation; cached bytecode is "observed only for correspondence" |
| §6 "Native arrays present" | Compares native `atom_id` values as strings, and native `map_num` and `radical_electrons` values as integers against a declared base-10 reading of the sidecar's strings |
| §1 | Adds source facts A12 and A13 and a project inference |
| Section headings | Unchanged, so existing links into the specification keep resolving |

## 8. Exact replacement text, UNAPPLIED

**Every block in this section is UNAPPLIED.** The specification is unchanged. A block takes effect only if a person
approves the whole bound revision of Section 9 and it is then applied under that authority.

### 8.1 Reconstruction rule

The blocks below are the exact payload of the revision. Given the bytes of this packet and the base file
`docs/ms-001/C3-WIRING-TEST-PROPOSAL.md` with SHA256 `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158`,
the revised file is produced as follows. The bytes of this file are authoritative, not its rendering.
1. **Lines.** Read this packet as UTF-8 and split it into lines at each LF byte. Neither file contains a CR byte.
2. **Blocks.** A payload block opens at a line that is exactly four tildes, a space, `w1r01`, a space, the word
   `current` or `proposed`, a space and the block identifier, for example `R01`, with nothing else on the line. It
   closes at the next line that is exactly four tildes. Its payload is the lines strictly between the two, each
   followed by one LF. A block with no line between has the empty payload. Whitespace is taken exactly as it is: no
   trimming, no tab expansion, no Unicode normalization.
3. **Pairs.** Each identifier has exactly one `current` block and one `proposed` block, the `current` block first.
4. **Location.** Each `current` payload occurs exactly once in the base file's bytes. The located spans do not overlap.
5. **Replacement.** Every located span is replaced by its `proposed` payload, all at once against the base file, so a
   replacement never searches inside another's result. Every other byte is kept.
6. **Result.** The result is the revised file. It must have the SHA256 and size bound in Section 9.

Every `current` payload starts at the beginning of a line and ends with an LF, so line structure is kept. The base
file ends with an LF and contains no line of four tildes.

### 8.2 Header

**R01. Opening status lines**, replaced to add a revision note after them.

~~~~ w1r01 current R01
Date: 2026-09-27. MS-001 scope option B, before Stage 1. Status: **PROPOSAL. Specification only. Nothing here has
been run, installed, registered or imported, and running it needs its own authorization.**
~~~~

~~~~ w1r01 proposed R01
Date: 2026-09-27. MS-001 scope option B, before Stage 1. Status: **PROPOSAL. Specification only. Nothing here has
been run, installed, registered or imported, and running it needs its own authorization.**

**Revision 01 (proposed 2026-10-04).** This text revises the specification of 2026-09-27 for the two blockers and the
unresolved requirement recorded by the [W1 pre-run determination](W1-PRE-RUN-DETERMINATION.md), W1-BLOCKER-E2,
W1-BLOCKER-E1 and U-F1P, and for seven gaps coupled to them. The options, reasons and rejected alternatives are in the
[revision decision packet](W1-REVISION-DECISION-PACKET.md). This revision is in force only after a person has approved
these exact bytes and the approval is recorded; until then the specification of 2026-09-27 is in force. Neither the
approval nor this revision authorizes a run of W1.
~~~~

Effect: none on §7–§9.

**R02. "What W1 cannot establish", before the bullet "No authorization"**, adding two bullets.

~~~~ w1r01 current R02
- **No authorization.** Nothing here authorizes Stage 1, a calculation or an installation.
~~~~

~~~~ w1r01 proposed R02
- **F1 beyond its capture.** The capture of Section 4 retains the bytes of the project's files and of every file of
  the environment's `site-packages`, and two module listings record which of them the loaded modules name. Both are
  file inventories. They do not establish which code the interpreter executed.
- **The declared environment, as relaxed.** The interpreter and the payload may hold one platform-injected name
  beyond the five declared variables. It is recorded where it appears and is never part of the launcher's environment
  (Section 5).
- **No authorization.** Nothing here authorizes Stage 1, a calculation or an installation.
~~~~

Effect: none on §7–§9; states limits that §10 repeats.

**R02a. "What W1 cannot establish", the bullet "F3 beyond its checks"** (G-2), separating stability from
correspondence.

~~~~ w1r01 current R02a
- **F3 beyond its checks.** The lock digest establishes the lock file's bytes, not that the running environment
  corresponds to it. W1 tests that correspondence only per distribution, only where a retained wheel allows it, and
  only for files a wheel's `RECORD` lists with a hash. Cached bytecode is observed only. W1 does not establish the
  origin of the interpreter or of the shell (Section 3).
~~~~

~~~~ w1r01 proposed R02a
- **F3 beyond its checks.** The lock digest establishes the lock file's bytes, not that the running environment
  corresponds to it. W1 tests that correspondence only per distribution, only where a retained wheel allows it, and
  only for files a wheel's `RECORD` lists with a hash. Cached bytecode is observed only: its correspondence to the
  wheel or to the source is not established, and Section 4 checks only that it does not change during the run. W1
  does not establish the origin of the interpreter or of the shell (Section 3).
~~~~

### 8.3 Section 1, sources

**R03. The sentence on member digests.**

~~~~ w1r01 current R03
(SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`, C3 §1). Member digests are in the
[pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md). Each statement reports what that source text defines.
~~~~

~~~~ w1r01 proposed R03
(SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`, C3 §1). Member digests are in the
[pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md), and that of the member first cited by A12 is in the
[revision decision packet](W1-REVISION-DECISION-PACKET.md). Each statement reports what that source text defines.
~~~~

**R04. Source table, after row A11**, adding A12 and A13.

~~~~ w1r01 current R04
| A11 | In a real run the upload task requests the transport of the job's computer and authorization, calls `presubmit` to write the job folder, including the submission script, and only then uploads. An exception in `presubmit` is raised as a pre-submit failure, with no upload and no retry | `aiida/engine/processes/calcjobs/tasks.py` 84–111 |
~~~~

~~~~ w1r01 proposed R04
| A11 | In a real run the upload task requests the transport of the job's computer and authorization, calls `presubmit` to write the job folder, including the submission script, and only then uploads. An exception in `presubmit` is raised as a pre-submit failure, with no upload and no retry | `aiida/engine/processes/calcjobs/tasks.py` 84–111 |
| A12 | Importing the configuration-settings module calls `AiiDAConfigDir.set()`, which creates the configuration directory and its daemon, daemon-log, broker, log and access-control subdirectories. The directory comes from `AIIDA_PATH` when that variable is set, with `.aiida` appended unless the path already ends in it, and is otherwise `~/.aiida`. The default `~/.aiida` path is computed at import even when `AIIDA_PATH` is set | `aiida/manage/configuration/settings.py` 20–30, 35–60, 97–129, 132–168, 171–172 |
| A13 | Opening the local transport sets its internal directory to `os.path.expanduser('~')` | `aiida/transports/plugins/local.py` 58–70 |
~~~~

**R05. Project inferences, after A10**, adding one inference.

~~~~ w1r01 current R05
- **A10.** By A1, that default transport has the login-shell setting true. A dry run therefore neither avoids a
  transport nor uses the configured no-login computer, and W1 does not use one.
~~~~

~~~~ w1r01 proposed R05
- **A10.** By A1, that default transport has the login-shell setting true. A dry run therefore neither avoids a
  transport nor uses the configured no-login computer, and W1 does not use one.
- **A12, A13.** Without `HOME`, AiiDA still computes paths from `~`. How the interpreter expands `~` when `HOME` is
  absent is not defined by this source and was not observed. W1 sets `AIIDA_PATH` and observes user-level paths
  before and after the run (Section 5).
~~~~

Effect: R03 to R05 add sources for §5's user-level observation; none on §7–§9 directly.

### 8.4 Section 2, declared setup

**R06. Row "Runner"** (E2, G-2).

~~~~ w1r01 current R06
| Runner | In-process `run_get_node` of aiida-core in one interpreter, with no daemon. The interpreter is the Stage 0 environment's own, invoked by its exact resolved path, which is recorded privately and written publicly as the environment-relative `bin/python`. Before it imports anything outside the standard library, it records the F3 build identity and the host record of Section 3 and makes their checks. Its version must read back as CPython 3.12.14. The lock digest check establishes the lock file's bytes only; whether the installed environment corresponds to the lock is tested separately, per distribution (Section 3). It is never found through `PATH`: under the clean `PATH` of Section 5, a bare `python` would not select that environment. It is started as `<environment>/bin/python -E -s tools/w1_driver.py` from the repository root. `-I` is not used, because it would drop the driver's directory from the import path |
~~~~

~~~~ w1r01 proposed R06
| Runner | In-process `run_get_node` of aiida-core in one interpreter, with no daemon. The interpreter is the Stage 0 environment's own, invoked by its exact resolved path, which is recorded privately and written publicly as the environment-relative `bin/python`. Its version must read back as CPython 3.12.14. It is never found through `PATH`: under the clean `PATH` of Section 5, a bare `python` would not select that environment. The driver runs as two processes. The **launcher** is started by the operator as `<environment>/bin/python -E -s -B tools/w1_driver.py launch` from the repository root. It imports nothing outside the standard library, makes the launcher record and the first user-level observation of Section 5, starts the runner, waits for it to end and makes the second user-level observation. The **runner** is started by the launcher as `<environment>/bin/python -E -s -B tools/w1_driver.py run`, from an argument vector without a shell, with the repository root as working directory and with an environment that is exactly the launcher record. Before it imports anything outside the standard library, the runner makes the interpreter record of Section 5, records the F3 build identity and the host record of Section 3 and makes their checks. The lock digest check establishes the lock file's bytes only; whether the installed environment corresponds to the lock is tested separately, per distribution (Section 3). `-B` is the bytecode policy of Section 4. `-I` is not used, because it would drop the driver's directory from the import path |
~~~~

Effect: §7 criterion 4 (first bullet) and §8 stop condition 2 now refer to the launcher and interpreter records;
§9 retains them.

**R07. Row "Class and module"** (E1).

~~~~ w1r01 current R07
| Class and module | Class `W1Job` in the module file `tools/w1_job.py`. The driver puts `tools/` first on the import path and imports `w1_job`. The recorded process type must equal `w1_job.W1Job` (A9); any other value, such as one caused by an entry point of the same name, stops W1. Both files are tracked at the declared commit, and their bytes are also inputs of each job (Section 4) |
~~~~

~~~~ w1r01 proposed R07
| Class and module | Class `W1Job` in the module file `tools/w1_job.py`. The driver puts `tools/` first on the import path and imports `w1_job`. The recorded process type must equal `w1_job.W1Job` (A9); any other value, such as one caused by an entry point of the same name, stops W1. Both files are untracked at the declared commit and are not required to be tracked at any commit. Section 4 captures their bytes, with their SHA256 and Git blob identifiers, and those bytes are inputs of each job |
~~~~

Effect: removes the requirement disposed as W1-BLOCKER-E1. No §7 criterion or §8 stop condition repeated it; §7
criterion 3 and §8 stop condition 6 now cover the drivers through the untracked capture.

### 8.5 Section 3, node boundary

**R08. The rule for *recorded* values** (G-4).

~~~~ w1r01 current R08
- where marked *recorded*, a value read during the run. Its exact source and the exact comparison made against it
  are declared in the tables that follow this one, under "The F3 build identity", "The F7 host record" and "The
  payload record". A *recorded* value with no declared source and comparison is not allowed.
~~~~

~~~~ w1r01 proposed R08
- where marked *recorded*, a value read during the run. Its exact source and the exact comparison made against it
  are declared in the tables that follow this one, under "The F3 build identity", "The F7 host record" and "The
  payload record", and for `code_identity` under "The F1 code identity" (Section 4). A *recorded* value with no
  declared source and comparison is not allowed.
~~~~

**R09. "Mandatory contents", row `env_policy`, and a new row `code_identity`** (E2, G-4).

~~~~ w1r01 current R09
| `env_policy` (F7) | `allow_list`: exactly the five variables of Section 5. `absent`: `["BASH_ENV", "ENV", "HOME"]`. `use_login_shell`: false. `import_sys_environment`: true. `shell`: `/bin/bash` |
~~~~

~~~~ w1r01 proposed R09
| `env_policy` (F7) | `allow_list`: exactly the five variables of Section 5. `platform_injected`: exactly `["__CF_USER_TEXT_ENCODING"]`. `platform_injected_scope`: exactly `interpreter and payload records only; never the launcher record`. `absent`: `["BASH_ENV", "ENV", "HOME"]`. `use_login_shell`: false. `import_sys_environment`: true. `shell`: `/bin/bash` |
| `code_identity` (F1) | Exactly the keys of "The F1 code identity" (Section 4), with the values, sources and comparisons declared there |
~~~~

Effect: §7 criterion 5 checks both rows key by key (R22); §8 stop condition 9 applies to them.

**R10. "The libraries actually used"** (G-7).

~~~~ w1r01 current R10
**The libraries actually used.** After job 2 the runner lists every module in `sys.modules`. For each module it
records two kinds of file in the run-end record, with the SHA256 of each:
- **the module file**, named by `__file__`: a source file, an extension module or another file the loader names;
- **the cached bytecode file**, named by `__cached__`, where that file exists.
~~~~

~~~~ w1r01 proposed R10
**The libraries actually used.** The runner lists every module in `sys.modules` twice: at the input point of
Section 4, and after job 2. Each listing is taken from a copy of `sys.modules` made in one statement. For each module
it records, in the capture record and in the run-end record, with the SHA256 of each file:
- **the module file**, named by `__file__`: a source file, an extension module or another file the loader names;
- **the cached bytecode file**, named by `__cached__`, where that file exists;
- **the origin** named by the module's spec, where it has one, such as `built-in` or `frozen`.

Both listings are file inventories at two instants. Neither is a record of the code that executed (Section 4).
~~~~

**R11. "Module files"** (G-7, U-F1P).

~~~~ w1r01 current R11
**Module files.** The checker assigns every module file to exactly one class:
- **Environment packages.** A module file under the environment's `site-packages` must be listed with a non-empty hash,
  under the wheel-path rule, in the wheel's own `RECORD` of a distribution whose status is `locked-verified`. Its
  SHA256 must equal that hash.
- **Standard library.** A module file under the base interpreter's prefix has its SHA256 recorded. See the limits
  below.
- **Repository.** A module file of the repository must equal its F1 capture (Section 4).
- **No file.** A built-in, frozen or namespace module, which has no module file, is recorded by name.

A module file in any other location, or one that fails its class's check, stops W1. That includes a module file of a
distribution whose status is `locked-wheel-unavailable` or `not-in-lock`.
~~~~

~~~~ w1r01 proposed R11
**Module files.** The checker assigns every module of both listings to exactly one class, in this order:
- **No file.** A module whose spec origin is `built-in` or `frozen`, or a namespace module, is recorded by name. A
  `__file__` that such a module carries is recorded and is not taken as the code it executed.
- **Environment packages.** A module file under the environment's `site-packages` must be a regular file, not a
  symbolic link, and must be listed with a non-empty hash, under the wheel-path rule, in the wheel's own `RECORD` of a
  distribution whose status is `locked-verified`. Its SHA256 must equal that hash, and it must be a file of the
  `code_private` capture of Section 4 with the same SHA256. An extension module is a module file like any other: its
  bytes are compared and captured as bytes, and they are machine code, not readable source.
- **Standard library.** A module file under the base interpreter's prefix has its SHA256 recorded. See the limits
  below.
- **Project.** A module file under the repository root and outside the environment must be one of the project files
  of Section 4 and must equal its F1 capture.

A module file in any other location, or one that fails its class's check, stops W1. That includes a module file of a
distribution whose status is `locked-wheel-unavailable` or `not-in-lock`, a module file in the repository's ignored
area outside the environment's `site-packages`, and a project module file first listed at the run end.
~~~~

**R12. "Cached bytecode files are observed only"** (G-2).

~~~~ w1r01 current R12
**Cached bytecode files are observed only, in every class.** Their paths and SHA256 values are recorded. No `RECORD`
equality, and no other comparison, is required of them. That holds whether the installed `RECORD` lists them with a
hash or with an empty hash field, and whether they are not listed at all because they were written at import time.
Their correspondence to the locked wheel, or to the module's source, is not established.
~~~~

~~~~ w1r01 proposed R12
**Cached bytecode files are observed only for correspondence, in every class.** Their paths and SHA256 values are
recorded, and Section 4 retains the bytes of those under the environment's `site-packages` as part of its declared
superset. No correspondence comparison is required of them: no `RECORD` equality, and no comparison with the locked
wheel or with the module's source. That holds whether the installed `RECORD` lists them with a hash or with an empty
hash field, and whether they are not listed at all. Their correspondence to the locked wheel, or to the module's
source, is not established. Section 4 makes one other comparison, of stability only: under its bytecode policy no
bytecode file may be written, removed or changed between the capture point and the run end. Stability shows that the
same bytes were present at both readings. It is not correspondence.
~~~~

**R12a. "Limits of F3", the bullet on cached bytecode** (G-2).

~~~~ w1r01 current R12a
- **Cached bytecode.** It is observed only, whether it was compiled at installation or at import time, and however
  a `RECORD` lists it. W1 does not establish that the bytecode the interpreter executed corresponds to the locked
  wheel or to the module's source.
~~~~

~~~~ w1r01 proposed R12a
- **Cached bytecode.** It is observed only, whether it was compiled at installation or at import time, and however
  a `RECORD` lists it. W1 does not establish that the bytecode the interpreter executed corresponds to the locked
  wheel or to the module's source. Section 4 checks only its stability between the capture point and the run end,
  which is not correspondence.
~~~~

Effect of R10 to R12a: §7 criterion 5's module-file check covers both listings; §8 stop conditions 6 and 10 apply;
§9 retains both listings. Cached bytecode is checked for stability under criterion 3 and stop condition 6, and never
for correspondence.

**R13. The payload record, row of the `/usr/bin/env` output** (E2).

~~~~ w1r01 current R13
| The `/usr/bin/env` output | The payload's exported environment | The names include `PATH`, `LC_ALL`, `AIIDA_PATH`, `TMPDIR`, `PYTHONNOUSERSITE` and `OMP_NUM_THREADS`, and lie within those six plus the shell-maintained `PWD`, `OLDPWD`, `SHLVL` and `_`. The first five values equal the parent's declared values, and `OMP_NUM_THREADS` is `1`. `BASH_ENV`, `ENV` and `HOME` are absent. A name outside that set, including one added by the platform or by aiida-core, fails the F7 criterion; it is retained as a finding and is not added to the set afterwards |
~~~~

~~~~ w1r01 proposed R13
| The `/usr/bin/env` output | The payload's exported environment | The names include `PATH`, `LC_ALL`, `AIIDA_PATH`, `TMPDIR`, `PYTHONNOUSERSITE` and `OMP_NUM_THREADS`, and lie within those six, the shell-maintained `PWD`, `OLDPWD`, `SHLVL` and `_`, and the names of `env_policy.platform_injected`. The first five values equal the launcher record's values, and `OMP_NUM_THREADS` is `1`. A platform-injected name, where present, has the value it has in the interpreter record. `BASH_ENV`, `ENV` and `HOME` are absent. A name outside that set, including one added by the platform or by aiida-core, fails the F7 criterion; it is retained as a finding and is not added to the set afterwards. The one platform-injected name was declared before any run (Section 5) |
~~~~

Effect: §7 criterion 4 (first bullet) and §8 stop condition 10 apply to the revised rule. This is the relaxation of
E2-O1 for the payload.

### 8.6 Section 4, F1

**R14. The body of Section 4**, from "Declared commit" to "Digests alone do not satisfy F1." The heading is kept.

~~~~ w1r01 current R14
- **Declared commit.** `git diff --binary <declared commit>` of the working tree. It includes staged and unstaged
  changes.
- **Untracked files.** The contents of every file listed by `git ls-files --others --exclude-standard`.
- **Ignored and private files.** That listing omits ignored paths such as private task directories. So the contents
  of every ignored or private source file used are added explicitly. The list is built two ways, from the loaded
  modules whose files lie in the repository and from a declared list. A difference between the two stops the test.
- **One capture.** All of this is captured once, at the run boundary, before the first job. At the end the commit,
  the index state and every digest are read again. Any change stops the test and marks it failed.
- **The fixture diff.** The labelled fixture diff guards only against a vacuous empty-diff pass. It never stands for
  the code state.
- **Bytes, not only digests.** Every item is retained as bytes that resolve from the provenance store by digest.
  Digests alone do not satisfy F1.
~~~~

~~~~ w1r01 proposed R14
**Scope.** F1 retains, as required inputs of each job, the bytes of the project's code and of every file of the
environment's `site-packages`, captured before the runner imports anything outside the standard library. Separately,
two module listings record which of those files the loaded modules name. The capture says what was available; the
listings say what was observed loaded. Both are file inventories. Neither is a record of the code that executed (see
"File inventory, not executed code" below).

**Git.** Every Git command of W1 is `/usr/bin/git --no-optional-locks` followed by one of the subcommands named in
this section. The runner starts it from an argument vector without a shell, with the repository root as working
directory and with an environment that is exactly `PATH=/usr/bin:/bin`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`,
`GIT_CONFIG_GLOBAL=/dev/null` and `GIT_OPTIONAL_LOCKS=0`. `HOME` is absent, so no system-level or user-level
configuration file and no user-level ignore file is read. The untracked listing below can therefore be wider than in
an ordinary shell of the same account, and every file it lists is captured. W1 uses only the subcommands `config`,
`rev-parse`, `ls-files` and `diff-index`, and the option `--version`. It does not use the porcelain `git diff`, which
can rewrite an index file even with optional locks disabled (observation G4 of the
[revision decision packet](W1-REVISION-DECISION-PACKET.md)).

**Bounded repository configuration and rules.** The repository's own configuration could reach further, so it is
bounded by these conditions:
- every entry printed by `config --list --show-origin -z` has the origin `file:.git/config`;
- no key printed by it is `include.path`, starts with `includeif.`, `filter.`, `diff.`, `index.` or `extensions.`, or
  is `core.excludesfile`, `core.attributesfile`, `core.fsmonitor`, `core.untrackedcache`, `core.splitindex`,
  `core.worktree` or `core.hookspath`;
- no file `.git/info/attributes` exists, and no file named `.gitattributes` lies in the repository root or in any
  directory that contains, at any depth, a path of the index or of the untracked listing;
- the ignore rules that apply are those of the repository's `.gitignore` files, which are tracked files, and of
  `.git/info/exclude`, whose SHA256 is recorded.

Influences on Git that these conditions do not bound, such as its compiled-in defaults and the program that
`/usr/bin/git` runs, are recorded only through `git_version`.

**Preconditions.** At the capture point and at the run end, each of these must hold, or W1 stops:
- every condition of "Bounded repository configuration and rules";
- `rev-parse --show-object-format` prints `sha1`, and `rev-parse --git-path index` prints `.git/index`;
- every entry printed by `ls-files --stage -z` has stage `0` and a mode other than `160000`;
- every `flags:` field printed by `ls-files --debug` is `0`;
- every path of the index and every path of the untracked listing names a regular file, not a symbolic link or a
  directory;
- the environment's `site-packages` holds no symbolic link.

**The capture point.** The runner reaches it after it has made the interpreter record of Section 5 and the first
reading of the F3 build identity, and before it imports anything outside the standard library, `w1_job` included.
Everything in this section that is "captured" or "recorded at the capture point" is read there, once. The F1 input
nodes are created later from these captured bytes, before job 1, and each must equal what was captured.

**The input point.** The runner reaches it after it has imported `w1_job`, with everything that module imports, and
loaded the W1 profile, and before it creates any input node of job 1. The first module listing of Section 3 is taken
here, and the second after job 2.

**The declared commit.** `rev-parse --verify HEAD^{commit}` at the capture point. It must be the same at the run end.

**The index state.** The exact standard output of `ls-files --stage -z`, which gives each entry's mode, object name,
stage and path. Its SHA256 is recorded at the capture point and must be equal at the run end. The raw bytes of
`.git/index` are not the index state, because some Git commands rewrite them without changing any entry (observation
G4 of the decision packet). Their SHA256 is recorded at both instants and is observed only.

**Tracked files.** For every path of the index, the SHA256 and size of the file in the working tree are recorded at
the capture point and must be equal at the run end. This comparison does not depend on Git's own change detection.

**The code diff.** The standard output of `diff-index -p --binary --no-color --no-ext-diff --no-textconv --no-renames
--src-prefix=a/ --dst-prefix=b/ <declared commit>`: the difference between the working tree and the declared commit,
staged and unstaged changes together. It is the `code_diff` input. It is produced again at the run end and must be
byte-identical.

**Untracked files.** `ls-files --others --exclude-standard -z` lists them. Each is captured as bytes in
`code_untracked`, with its path, size, SHA256 and Git blob identifier: the SHA-1 of the ASCII text `blob`, a space,
the size in decimal and a NUL byte, followed by the file's bytes. The listing and every digest are taken again at the
run end and must be equal. The two driver files are among these files (Section 2).

**Project files.** Exactly `tools/w1_driver.py` and `tools/w1_job.py`. Neither may have a cached bytecode file at the
capture point. In each module listing the module files of the Project class of Section 3 must be exactly these two
files, and each must equal its captured bytes. A project module file first listed at the run end stops W1.

**The environment, as a declared superset.** At the capture point every regular file under the environment's
`site-packages` is captured as bytes in `code_private`, under its path relative to `site-packages`: module files,
extension modules, cached bytecode, bundled libraries, data files and files that no `RECORD` lists. Its listing, in
the serialization of "Listings" below, is recorded at the capture point and taken again at the run end, and the two
must be equal. In each module listing, every module file of the Environment packages class of Section 3 must be a
file of `code_private` with an equal SHA256. A module first listed at the run end is therefore covered by bytes
captured before it was loaded. That the bytes it loaded equal them rests on the capture-point and run-end readings,
not on an observation at load time. No other ignored or private file is captured or used as code: a module file
anywhere else in the repository's ignored area stops W1 (Section 3).

**Declared runtime data, not source.** The run also reads and writes files that are data, not code. They are not part
of the F1 capture, and nothing in them is taken as code:
- the W1 configuration directory under `AIIDA_PATH` (A12), with the profile's configuration;
- the profile's storage, which is the provenance store itself and is covered by the closure inventory (Section 9);
- the computer's work directory, whose submission files are bound by Section 5;
- the project-local `TMPDIR`.

For the configuration directory and for `TMPDIR`, the runner records a listing at the capture point and at the run
end, in the serialization of "Listings" below. These listings are retained privately and are observed only, because
the run is expected to write there.

**The bytecode policy.** The launcher and the runner run with `-B`. The runner records `sys.flags.dont_write_bytecode`,
which must be `1`. At the capture point and at the run end it lists every file in every `__pycache__` directory under
`tools/`, under the environment's `site-packages` and under the base interpreter's prefix, in the serialization of
"Listings" below. The listing is private. A new, removed or changed file stops W1. This is a stability check: it shows
that the same bytes were present at both readings. It is not a correspondence check, and the correspondence of cached
bytecode to the wheel or to the module's source stays unestablished (Section 3). Cached bytecode that already exists
can be read by the interpreter.

**Listings.** A listing is a sequence of lines encoded as UTF-8. Each line holds three fields separated by one TAB
byte and ends with one LF byte, the last line included; an empty listing has no bytes. The fields are: the path,
written as a root tag, `/` and the path relative to that root with `/` as separator; the size in bytes, in decimal
without leading zeros; and the SHA256 of the file, as 64 lowercase hexadecimal characters. The root tags are `tools`,
`site-packages`, `base-prefix`, `aiida-config` and `tmpdir`, for `tools/`, the environment's `site-packages`, the base
interpreter's prefix, the W1 configuration directory and `TMPDIR`. Only regular files are listed. Lines are sorted by
the bytes of the path field. A path that contains a TAB or LF byte, or that is not valid UTF-8, stops W1.

**The fixture diff.** `fixture_diff` holds exactly the bytes of the constant `W1_FIXTURE_DIFF` in `w1_job.py`: the
ASCII text below, with LF line endings and a final LF, 94 bytes, SHA256
`f3a3deb5cd0693c76b9bff397e811bff75eb253cb5f42265fe68e6582fdea609`.

```
--- a/w1_fixture.txt
+++ b/w1_fixture.txt
@@ -1 +1,2 @@
 w1 fixture line 1
+w1 fixture line 2
```

The checker confirms that the stored bytes are not empty, that they equal the constant in the captured `w1_job.py`,
and that they resolve from the store by their digest through the same function that resolves `code_diff`. The
fixture diff guards only against a vacuous empty-diff pass. It never stands for the code state.

**The F1 code identity.** `code_identity` holds exactly these keys. Paths are relative to the repository root and are
written with `/`. Lists are sorted by the bytes of their paths.

| Key | Value | Source | Comparison made by the checker |
|---|---|---|---|
| `commit` | *recorded* | `rev-parse --verify HEAD^{commit}` | Equal at run end |
| `object_format` | Exactly `sha1` | `rev-parse --show-object-format` | Equal to the declared string at both instants |
| `git_version` | *recorded* | The standard output of `--version` | Equal at run end |
| `git_environment` | Exactly the five names and values of "Git" above | Declared | Equal to the declaration |
| `git_config_sha256` | *recorded* | The SHA256 of the standard output of `config --list --show-origin -z` | Equal at run end |
| `info_exclude_sha256` | *recorded* | The SHA256 of the bytes of `.git/info/exclude` | Equal at run end |
| `index_state_sha256` | *recorded* | The SHA256 of the standard output of `ls-files --stage -z` | Equal at run end |
| `raw_index_sha256` | *recorded* | The SHA256 of the bytes of `.git/index` | None. Observed only, at both instants |
| `tracked_files` | *recorded*: one entry `{path, bytes, sha256}` per path of the index | The working-tree files | Equal at run end |
| `code_diff_sha256` | *recorded* | The SHA256 of the code diff | Equal to the SHA256 of the stored `code_diff`, and to that of the diff produced again at run end |
| `untracked_files` | *recorded*: one entry `{path, bytes, sha256, git_blob}` per listed path | The untracked listing and the files | Equal to the contents of the stored `code_untracked`, and equal at run end |
| `project_files` | Exactly `["tools/w1_driver.py", "tools/w1_job.py"]` | Declared | Equal to the Project module files of each module listing |
| `environment_listing_sha256` | *recorded* | The SHA256 of the listing of "The environment, as a declared superset", in the serialization of "Listings" | Equal to the SHA256 of the same listing made from the stored `code_private`, and equal at run end |
| `pycache_listing_sha256` | *recorded* | The SHA256 of the bytecode listing of "The bytecode policy", in the serialization of "Listings" | Equal at run end. A stability comparison, not a correspondence check |
| `dont_write_bytecode` | Exactly `1` | `sys.flags.dont_write_bytecode` in the runner | Equal to the declared value |
| `payload_sha256` | *recorded* | The SHA256 of the payload constant in `w1_job.py` | Equal to the digest of `w1_payload.sh` in each job's input manifest |
| `fixture_diff_sha256` | Exactly `f3a3deb5cd0693c76b9bff397e811bff75eb253cb5f42265fe68e6582fdea609` | The SHA256 of the stored `fixture_diff` | Equal to the declared string |
| `capture_point` | Exactly `after the interpreter record and the first F3 reading; before any import outside the standard library` | Declared | Equal to the declared string |

**File inventory, not executed code.** Two obligations are kept apart. Neither discharges the other.
- **The `RECORD` comparisons of Section 3** test that installed files equal the bytes of the locked wheels. They cover
  every file that a `locked-verified` wheel's `RECORD` lists with a non-empty hash, loaded or not, except bytecode
  cache and `.data/scripts/` files, at a reading before job 1 and a reading after job 2. They retain no bytes, and
  they are the only correspondence test.
- **The F1 capture of this section** retains bytes in the provenance store, as required inputs of each job: the code
  diff, the untracked files and every file of the environment's `site-packages`. It tests no correspondence: a file
  that no `RECORD` lists, or a cached bytecode file, is retained without being established.

Covered by neither: the bytes of standard-library files, of the interpreter binary and of `/bin/bash`, which are
recorded by digest only; the bytes of the declared runtime data; libraries that the system's dynamic loader loads
from outside `site-packages`; and frozen modules, whose code is part of the interpreter binary.

Every check of this section and of Section 3 supports a file inventory: which files, with which bytes, were present
when they were read, and which of them the loaded modules named. None of them supports a guarantee about executed
code. The interpreter can execute cached bytecode whose correspondence to its source is not established, frozen code,
or code generated at run time; a file can change and change back between two readings; and a module can be loaded
and removed between the two listings. W1 claims no executed-code guarantee.

**Bytes, not only digests.** Every item is retained as bytes that resolve from the provenance store by digest.
Digests alone do not satisfy F1.

**The run end.** After job 2 every comparison of this section is made. Any difference stops W1 and marks it failed.
~~~~

Effect: §7 criterion 3 is restated (R20); §7 criterion 5 checks `code_identity` (R22); §7 criterion 7 covers the
fixture diff (R23); §8 stop condition 6 is restated (R26) and stop conditions 14 and 15 are added (R27); §9 retains
the capture record (R28). This block resolves U-F1P and gaps G-1, G-2, G-4, G-5 and G-7.

### 8.7 Section 5, F7

**R15. Mandatory value 1, the parent environment** (E2).

~~~~ w1r01 current R15
1. **Parent environment.** The runner is started from an empty environment containing exactly: `PATH=/usr/bin:/bin`,
   `LC_ALL=C`, `AIIDA_PATH` set to W1's project-local configuration directory, `TMPDIR` set to a project-local
   directory, and `PYTHONNOUSERSITE=1`. Nothing else is set. In particular `BASH_ENV`, `ENV` and `HOME` are absent,
   and `PATH` resolves `bash` to `/bin/bash`. A2 passes this environment on to every later shell. The runner records
   `os.environ` at start, and its names must equal `env_policy.allow_list` exactly.
~~~~

~~~~ w1r01 proposed R15
1. **Parent environment, in three records.** The runner is started from an empty environment containing exactly:
   `PATH=/usr/bin:/bin`, `LC_ALL=C`, `AIIDA_PATH` set to W1's project-local configuration directory, `TMPDIR` set to a
   project-local directory, and `PYTHONNOUSERSITE=1`. Nothing else is set. In particular `BASH_ENV`, `ENV` and `HOME`
   are absent, and `PATH` resolves `bash` to `/bin/bash`. Three records are kept apart:
   - **The launcher record.** The launcher builds this environment as an explicit mapping, not from its own
     environment, records it and passes exactly it to the runner. Its names must equal `env_policy.allow_list`, and
     its values must equal the declared values. A platform-injected name in it stops W1.
   - **The interpreter record.** The runner records `os.environ` immediately after `import os`, before any other
     import, and again after job 2. Its names must include every name of `env_policy.allow_list` and lie within
     `env_policy.allow_list` and `env_policy.platform_injected`. Each allow-list value must equal the launcher
     record's value. A platform-injected name is recorded with its value where it appears, and its absence is
     recorded too.
   - **The payload record.** The payload's `/usr/bin/env` output, compared as Section 3 declares.

   `__CF_USER_TEXT_ENCODING` was observed in the interpreter's environment on the project host, with exactly the five
   declared variables handed to the interpreter and without that name among them
   ([W1 pre-run determination](W1-PRE-RUN-DETERMINATION.md), §3.1). Its cause is not established. It is declared as
   platform-injected before any run, for this one name only. This relaxes the earlier rule that the names recorded
   at start equal the allow-list exactly; the launcher record keeps that rule. The runner does not remove the name.
   A2 passes the runner's environment, with any platform-injected name, on to every later shell. The runner's own
   child processes, the Bash version probe, the `sysctl` commands and the Git commands, are started with an explicit
   environment: the launcher record, or for Git the environment of Section 4.
~~~~

Effect: §7 criterion 4 (first bullet) is restated (R21) and §8 stop condition 2 is restated (R25). This is the
relaxation of E2-O1 at the interpreter.

**R16. "What counts as evidence", the bullet on the declared environment** (E2).

~~~~ w1r01 current R16
- **For the declared environment.** The parent environment recorded at start, and the payload record's
  `/usr/bin/env` output, each compared as declared (item 1 above, and Section 3).
~~~~

~~~~ w1r01 proposed R16
- **For the declared environment.** The launcher record, the interpreter record at start and after job 2, and the
  payload record's `/usr/bin/env` output, each compared as declared (item 1 above, and Section 3).
~~~~

**R17. After the sentence on user startup files**, adding the user-level observation (G-3).

~~~~ w1r01 current R17
No file is written to any user startup file, and no user startup or history file is read.
~~~~

~~~~ w1r01 proposed R17
No file is written to any user startup file, and no user startup or history file is read.

**User-level side effects.** The absence of `HOME` does not by itself keep a process away from the user's home
directory: AiiDA computes paths from `~` even when `AIIDA_PATH` is set (A12, A13), and how `~` is expanded without
`HOME` is interpreter behaviour that this source does not define. The launcher therefore observes user-level paths
before it starts the runner and after the runner has ended. The home directory is the one that the password database
gives for the account running W1. It is recorded privately and is never written to a public record. The observed
paths, relative to it, are: the home directory itself, `.aiida`, `.ase`, `.cache`, `.config`, `.local`,
`.local/share`, `Library/Caches`, `Library/Application Support`, `Library/Preferences` and `Library/Logs`. For each,
the launcher records whether it exists and its type, and for a directory the sorted names and types of its entries,
without descending further. Any difference between the two observations stops W1, whatever its cause, another
process included. A change deeper inside an existing directory, or at any other path, is not detected.
~~~~

Effect: §7 criterion 7 (R23) and §8 stop condition 1 (R24); §9 retains both observations (R28).

### 8.8 Section 6, F4

**R18. After the sentence on missing fields**, declaring the sidecar's bytes (G-6).

~~~~ w1r01 current R18
A missing required field, for any site, fails W1.
~~~~

~~~~ w1r01 proposed R18
A missing required field, for any site, fails W1.

**The sidecar's bytes.** The sidecar file `w1_identity.json` holds one JSON object, written as Python's `json.dumps`
writes it with `ensure_ascii=True` and `separators=(",", ":")`, followed by one LF byte and nothing else. The object
has exactly these keys, in this order:
- `format`: the string `w1-identity-sidecar-1`;
- `source_sha256`: the SHA256 of the frozen file, as 64 lowercase hexadecimal characters;
- `sites`: a list with one object per site, in file order. Each has exactly the keys `index` (the site index i, an
  integer counted from 0), `atom_id`, `element`, `position` (a list of the three position strings), `map_num` and
  `radical_electrons`, in this order. Every value except `index` and `position` is a JSON string holding the exact
  text of its field in the frozen file's atom line. `position` is a JSON array of exactly three JSON strings, each
  holding the corresponding coordinate field's exact text, in file order.

The checker builds the sidecar again from the frozen file by this rule and compares the result byte for byte with job
1's `identity`. That regeneration is the referent of "the sidecar bytes" below.
~~~~

**R18a. "Native arrays present"** (G-6), defining the comparison of native arrays with the sidecar's strings.

~~~~ w1r01 current R18a
- **Native arrays present.** Where a native per-atom array (`atom_id`, `map_num`, `radical_electrons`) is present,
  its value at every site must equal the sidecar's. Any difference fails.
~~~~

~~~~ w1r01 proposed R18a
- **Native arrays present.** Where a native `atom_id` array is present, each native string value must equal the
  corresponding sidecar string exactly. Where a native `map_num` or `radical_electrons` array is present, each native
  value must be an integer scalar, excluding Boolean and floating-point values, and must equal the base-10 integer
  represented by the corresponding sidecar string. That string must match `[+-]?[0-9]+` in its entirety; otherwise
  W1 fails. This conversion is for comparison only and does not change the sidecar bytes. Any type or value mismatch
  fails.
~~~~

Effect: §7 criterion 2 and §8 stop condition 12 apply the comparison as defined. The frozen file's header declares
`map_num` and `radical_electrons` as integer-typed (S3), while the sidecar holds their exact text as strings (R18).

**R19. "Sidecar carriage"** (G-6).

~~~~ w1r01 current R19
- **Sidecar carriage.** The sidecar bytes must be identical at every step: job 1's `identity`, job 1's
  `identity_out`, job 2's `identity` and job 2's `identity_out`. Agreement of element multisets, or mere presence of
  a field, is never taken as identity.
~~~~

~~~~ w1r01 proposed R19
- **Sidecar carriage.** The sidecar bytes must be identical at every step, and equal to the checker's regeneration:
  job 1's `identity`, job 1's `identity_out`, job 2's `identity` and job 2's `identity_out`. Agreement of element
  multisets, or mere presence of a field, is never taken as identity.
~~~~

Effect: §7 criterion 2 and §8 stop condition 12 now have a declared byte referent; neither text changes.

### 8.9 Section 7, acceptance criteria

**R20. Criterion 3.**

~~~~ w1r01 current R20
3. The F1 items resolve from the store as bytes, and their digests are unchanged between the start and the end of
   the run.
~~~~

~~~~ w1r01 proposed R20
3. The F1 items resolve from the store as bytes, each is an input of both jobs, and every comparison of Section 4
   between the capture point and the run end holds.
~~~~

**R21. Criterion 4, first bullet.**

~~~~ w1r01 current R21
   - the Section 5 environment in the parent, and every payload-record comparison of Section 3;
~~~~

~~~~ w1r01 proposed R21
   - the launcher record and the interpreter records of Section 5, and every payload-record comparison of Section 3;
~~~~

**R22. Criterion 5, opening.**

~~~~ w1r01 current R22
5. The stored `defaults`, `build_identity`, `calc_performed`, `seed`, `units`, `per_claim`, `env_policy` and
   `host_record` inputs of **both** jobs satisfy the "Mandatory contents" declarations of Section 3 key by key. Each
   check is made against the declaration, not against another stored copy of the input. For a *recorded* value, the
   declaration is the source and comparison that Section 3 gives it. Any of the following fails W1:
~~~~

~~~~ w1r01 proposed R22
5. The stored `defaults`, `build_identity`, `calc_performed`, `seed`, `units`, `per_claim`, `env_policy`,
   `host_record` and `code_identity` inputs of **both** jobs satisfy the "Mandatory contents" declarations of Section
   3 key by key. Each check is made against the declaration, not against another stored copy of the input. For a
   *recorded* value, the declaration is the source and comparison that Section 3, or for `code_identity` Section 4,
   gives it. Any of the following fails W1:
~~~~

**R22a. Criterion 5, the additional checks.**

~~~~ w1r01 current R22a
   As additional checks, each job's `input_manifest` must match the digests of its stored submission files, and every
   module file of the run-end record must pass its class check under "The libraries actually used". Cached bytecode
   files are observed only and are not checked.
~~~~

~~~~ w1r01 proposed R22a
   As additional checks, each job's `input_manifest` must match the digests of its stored submission files, and every
   module file of the capture record and of the run-end record must pass its class check under "The libraries
   actually used". Cached bytecode files are not checked for correspondence; their stability between the capture
   point and the run end is a comparison of Section 4, under criterion 3.
~~~~

**R23. After criterion 6**, adding criterion 7.

~~~~ w1r01 current R23
6. Every repository object of every chain node has a key equal to its SHA256.
~~~~

~~~~ w1r01 proposed R23
6. Every repository object of every chain node has a key equal to its SHA256.
7. The two user-level observations of Section 5 are equal, and the fixture diff passes its check of Section 4.
~~~~

### 8.10 Section 8, stop conditions

**R24. Stop condition 1.**

~~~~ w1r01 current R24
- a user-level AiiDA configuration directory appears;
~~~~

~~~~ w1r01 proposed R24
- a user-level AiiDA configuration directory appears, or the two user-level observations of Section 5 differ;
~~~~

**R25. Stop condition 2.**

~~~~ w1r01 current R25
- any variable outside the Section 5 allow-list is present in the parent;
~~~~

~~~~ w1r01 proposed R25
- the launcher record differs from the Section 5 allow-list or its declared values, or an interpreter record holds a
  name outside the allow-list and the declared platform-injected name, lacks an allow-list name or differs from the
  launcher record in an allow-list value;
~~~~

**R26. Stop condition 6.**

~~~~ w1r01 current R26
- a code capture changes during the run;
~~~~

~~~~ w1r01 proposed R26
- a precondition of Section 4 fails, or a comparison of Section 4 between the capture point and the run end differs,
  a new, removed or changed bytecode file included;
~~~~

**R26a. Stop condition 11**, aligned with the bytecode stability check (G-2).

~~~~ w1r01 current R26a
- a `distributions` entry fits none of the three statuses. A permitted status, and a cached bytecode file, never
  stop W1 by themselves;
~~~~

~~~~ w1r01 proposed R26a
- a `distributions` entry fits none of the three statuses. A permitted status never stops W1 by itself, and a cached
  bytecode file stops W1 only through the stability comparison of Section 4, never through its correspondence;
~~~~

**R27. After the last stop condition**, adding stop conditions 14 and 15.

~~~~ w1r01 current R27
- a negative case passes.
~~~~

~~~~ w1r01 proposed R27
- a negative case passes;
- a project module file, or a module file outside the classes of Section 3, is first listed at the run end;
- the fixture diff fails its check of Section 4.
~~~~

### 8.11 Section 9, retained artifacts

**R28. The private item on the effective configuration record.**

~~~~ w1r01 current R28
- the effective configuration record, with the parent environment recorded at start;
~~~~

~~~~ w1r01 proposed R28
- the effective configuration record, with the launcher record and the interpreter records of Section 5;
- the two user-level observations of Section 5;
- the capture record of Section 4, with the module listings, the environment, `__pycache__` and runtime-data
  listings, and the run-end comparisons;
~~~~

### 8.12 Section 10, limits

**R29. After the F7 limit**, adding four limits.

~~~~ w1r01 current R29
- F7 is bounded to the no-login setting and the declared environment. W1 establishes no hardware property.
~~~~

~~~~ w1r01 proposed R29
- F7 is bounded to the no-login setting and the declared environment. W1 establishes no hardware property.
- The declared environment admits one platform-injected name in the interpreter and payload records. Its cause is not
  established.
- F1 is a file inventory at two instants. W1 claims no guarantee about the code that executed (Section 4).
- The two driver files are identified by their bytes, SHA256 and Git blob identifiers, not by a commit.
- The user-level observation covers the paths that Section 5 names, and only the names of their direct entries.
~~~~

**R29a. The F3 sub-limit on cached bytecode** (G-2).

~~~~ w1r01 current R29a
  - Cached bytecode is observed only.
~~~~

~~~~ w1r01 proposed R29a
  - Cached bytecode is observed only for correspondence; its stability within the run is checked (Section 4).
~~~~

## 9. Bound bytes and the application proof

| Artifact | SHA256 | Bytes |
|---|---|---|
| Base: `docs/ms-001/C3-WIRING-TEST-PROPOSAL.md`, unchanged | `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158` | 45 998 |
| Prospective revised specification, revision 01, not applied | `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347` | 70 753 |
| Patch carrying the base to the revised bytes, a unified diff | `ed8a0dfd9891709c65c24eb4ec28ea80dff0fd4a54d94d0be6813b9ca3b450a7` | 52 085 |

These are digests of three separate artifacts. The revised file and the patch are retained privately and are not
published as files; this packet does not list its own digest.

**Two independent routes to the same bytes.** Both were carried out on private copies, never on the specification,
and both gave the revised SHA256 above.
1. **By the blocks of Section 8**, under the rule of Section 8.1, from the bytes of this packet and the base file.
2. **By the patch.** In an empty directory holding a copy of the base file named `base.md` and the patch named
   `revision-01.patch`, the invocation `/usr/bin/patch -o revised.md base.md revision-01.patch` (Apple `patch`
   2.0-12u11) exits 0, and `revised.md` has the revised SHA256. The patch was generated by
   `/usr/bin/diff -u --label a/docs/ms-001/C3-WIRING-TEST-PROPOSAL.md --label b/docs/ms-001/C3-WIRING-TEST-PROPOSAL.md`
   applied to the base and the revised file (Apple `diff`, exit 1 because the files differ). Its paths are
   repository-relative, and it carries no time stamps.

An independent party who holds the base file and this packet can repeat route 1 without any private material. Route
2 needs the patch, whose bytes are bound above.

## 10. Residual risks, prerequisites and what does not change

### 10.1 Residual risks and uncertainties

- **The injected name.** Its cause and its first appearance in the process are not established. That CoreFoundation
  sets it remains an `[AGENT]` inference. A different or second injected name on another host or interpreter would
  still fail W1.
- **AiiDA on this host.** Unobserved: AiiDA was not imported. How it behaves without `HOME`, which modules it loads
  late, and how large the capture will be are unknown until a run.
- **Git.** That `diff-index` with the declared options never rewrites the repository's own index rests on G4 and G6,
  not on every case. The meaning of individual index flag bits is not established. The rule that stops on any
  non-zero flag does not depend on it.
- **Interpreter behaviour assumed only through run-time checks.** That `-B` stops bytecode writes, and that existing
  cached bytecode is read, were not observed here. The revision checks the first at run time
  (`dont_write_bytecode`, the `__pycache__` listings) and states the second as observed only.
- **The wider untracked capture.** Under the declared Git environment a local tool-settings file of the account is
  captured into the private store. If anything changes it during the run, W1 stops.
- **The user-level observation** can stop W1 for a change made by another process, and it does not see deeper changes.
- **No executed-code guarantee.** The F1 capture and the `RECORD` checks give a file inventory only.
- **Load-time bytes.** That the bytes a module loaded equal the captured bytes rests on the capture-point and run-end
  readings, not on an observation at load time.
- **Capture volume.** The superset was 18 448 files and 374 182 654 bytes at the probed state (S2). Its size at a run,
  and whether the job machinery carries it through each job's folder, manifest and binding, are unobserved.
- **Determination still needed.** The revised text has had no executability determination. A revised W1 is not
  predicted to pass.

### 10.2 Prerequisites

1. A person's decision on the bound revision (Section 11).
2. If approved: the application of exactly the bound bytes, recorded under that authority.
3. Then a renewed executability determination under the revised text, by the project under whatever authorization a
   person gives. It covers at least the launcher and interpreter records under `-E -s -B`,
   `sys.flags.dont_write_bytecode`, the declared Git invocations and configuration bounds, the user-level
   observation paths, and whether the job machinery carries the declared superset through each job's folder,
   input manifest and binding.
4. Only then, a separately authorized W1 run, which needs the two driver files to be written under that authorization.

### 10.3 What this packet does not change

- C3 readiness remains BLOCKED. No C3 blocker is closed.
- Stage 1 remains BLOCKED and is not authorized. Stages 1a, 1b and 2 are not authorized. Scope option A remains
  BLOCKED.
- Basis normalization remains PARTIALLY ESTABLISHED. E-01 remains technically BLOCKED and scientifically
  INDETERMINATE.
- W1 remains unrun. C4-j and B3-b remain deferred.
- The specification, C4 with its opening Approval bullet, every approval record and every frozen Stage 0 definition
  are byte-identical.
- No evidence label is upgraded.

## 11. Decision

**The bytes for decision.**

| Artifact | SHA256 | Bytes |
|---|---|---|
| Base specification (in force) | `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158` | 45 998 |
| Revised specification, revision 01 | `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347` | 70 753 |
| Patch from base to revised | `ed8a0dfd9891709c65c24eb4ec28ea80dff0fd4a54d94d0be6813b9ca3b450a7` | 52 085 |

**What approving these bytes would mean.** A person would approve the revised bytes as the text of
`docs/ms-001/C3-WIRING-TEST-PROPOSAL.md`, to replace the base bytes. That includes the relaxation for one
platform-injected name, the untracked-capture identity of the drivers, the F1 capture contract with its stated
limits, and the seven coupled declarations.

**What it would not mean.** It would not mean:
- readiness, parity or physical validation;
- authorization of Stage 1, 1a, 1b or 2;
- authorization to run W1, to implement its drivers, to install anything or to commit anything;
- an upgrade of any evidence label;
- the closure of any C3 blocker.

C3 readiness would remain BLOCKED.

**Response form.** One line, in exactly one of these forms:
- `W1-REVISION-01 APPROVE <revised SHA256>`: approves exactly the revised bytes bound above. The digest must match.
- `W1-REVISION-01 REJECT`, optionally followed by free text: the base specification stays in force, and W1 stays
  BLOCKED.
- `W1-REVISION-01 REQUEST-CHANGES: <free text>`: names the clauses or options to change. A changed revision would
  have new bytes and would need its own decision.

No response is not a decision: the base specification stays in force.

**After an approval, in this order.**
1. The approved bytes are applied to the specification and recorded under that authority, bound to the base, revised
   and patch digests.
2. Executability is determined again under the revised text.
3. Only then is a separately authorized W1 run sought.

No step of this sequence is reached by this packet, and no W1 pass is predicted.
