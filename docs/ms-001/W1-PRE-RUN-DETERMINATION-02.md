# W1 provenance wiring test: pre-run determination 02, under specification revision 01

Date: 2026-10-04. MS-001 scope option B. **Disposition: INDETERMINATE before execution. W1 was not run.**

Every statement of status in this record is as of 2026-10-04, at the probed state described in Section 1.

A person approved revision 01 of the W1 specification, [C3-WIRING-TEST-PROPOSAL.md](C3-WIRING-TEST-PROPOSAL.md), in
an answer recorded on 2026-10-04, and the approved bytes were applied
([approval record](W1-REVISION-01-HUMAN-APPROVAL.md)). The specification in force has SHA256
`29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347`. The
[revision decision packet, §10.2](W1-REVISION-DECISION-PACKET.md#102-prerequisites) and its §11 require that
executability then be determined again under the revised text, before any W1 run is sought. This record is that
renewed determination. It was made under the instruction that authorized the application. That instruction is held
privately by the orchestration layer. It permits only small read-only probes needed for this determination. It does
not permit a W1 run, the writing of the W1 drivers, an AiiDA import, profile or job, an installation, any chemistry or
any commit.

**Order.** This determination postdates the application. The base bytes of the specification, SHA256
`92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158` (45 998 bytes), were replaced by the approved
revision 01, SHA256 `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347` (70 753 bytes), and the
specification read back with the revised digest, before the first probe of Section 1 began. Every requirement
disposed below is a requirement of the revised bytes.

**Relation to the first determination.** The [first W1 pre-run determination](W1-PRE-RUN-DETERMINATION.md),
`docs/ms-001/W1-PRE-RUN-DETERMINATION.md` at SHA256
`a808f51f4593e4556174b67b91f1fb865d010a724d2ee1cd4d53463d73488809`, of 2026-09-29, and its
[machine-readable outcome](w1-outcome.json), `docs/ms-001/w1-outcome.json` at SHA256
`63e47e2fab6306c62218b33663cb48221e41012366fdc0fc6367121e9f34400d`, are the result of a determination under the base
specification of 2026-09-27, which revision 01 supersedes. They keep their bytes and are not rewritten, so they carry
no note of the supersession themselves. This record, the [package index](README.md#records) and the export manifest
state it. Their disposition, W1 BLOCKED before execution, stands as the result under the base text. This record is a
new determination under revision 01. It replaces nothing in the first record.

The disposition is INDETERMINATE, for two reasons together (Section 2):
- **No probed prerequisite blocks.** Under the revised text, the earlier blockers W1-BLOCKER-E2 and W1-BLOCKER-E1 and
  the unresolved requirement U-F1P no longer block as specified (Section 3). Every prerequisite of the packet's §10.2
  item 3 that can be observed without AiiDA was observed to hold at the probed state (Section 4).
- **Untested requirements remain.** Several requirements cannot be observed without importing AiiDA or running W1.
  The chief one is whether the job machinery carries the declared superset of about 18 000 files through each job's
  folder, input manifest and binding. They stay untested (Section 4.6 and Section 5).

W1 was therefore not run. **No AiiDA profile, computer, code or job was created, and AiiDA, ASE and NumPy were not
imported.** No W1 driver or job class was written. No chemistry was done: no engine was run, nothing was calculated,
nothing was installed and nothing was retrieved over a network. A W1 run still needs a separate authorization by a
person, which must cover writing the two driver files (Section 8).

This record closes **none** of the C3 blockers (Section 7). C3 readiness remains BLOCKED. Stage 1 remains BLOCKED and
is not authorized.

## 1. What was done

After the application, a pre-run executability determination was made by read-only inspection, hashing and startup
probes of the Stage 0 interpreter. Each probe imports the standard library only:
- **Application checks.** The base, revised and patch digests and sizes were verified before the application, and the
  live specification after it (approval record, Section 2).
- **Launcher and runner.** The Stage 0 environment's `bin/python` was started, by its exact path, as
  `-E -s -B <probe> launch` from the repository root. That launcher built the five-variable environment as an
  explicit mapping, recorded it, made the first user-level observation and started a runner as
  `bin/python -E -s -B <probe> run`, from an argument vector without a shell, with exactly that mapping as its
  environment. The runner recorded `os.environ` immediately after `import os` and again at its end, together with the
  interpreter flags, version, executable, import path and loaded modules. It started its children with the launcher
  record as their explicit environment: the Bash version probe of §3, `/usr/bin/env`, and the two `sysctl` commands of
  the host record. It also read `SystemVersion.plist`. The launcher made the second user-level observation after the
  runner had ended.
- **Shell-chain simulation.** The runner also simulated the shell chain of the specification's source facts A2, A3
  and A5, without AiiDA: a system shell running `bash -c`, which runs a submission script, which runs
  `/bin/bash w1_payload.sh`. The submission script held header redirections, the one export `OMP_NUM_THREADS=1` and the
  run line. The payload held exactly the payload-record lines of
  [§3](C3-WIRING-TEST-PROPOSAL.md#3-node-boundary-the-w1-calcjob-class), and the runner applied the payload-record
  comparisons of §3 to its output.
- **Git.** The declared Git invocations of
  [§4](C3-WIRING-TEST-PROPOSAL.md#4-f1-the-code-that-ran-captured-once) were run twice under the declared Git
  environment, and every precondition of §4 was evaluated. The raw bytes of `.git/index` were hashed before and after.
- **The superset.** Every regular file of the environment's `site-packages` was listed in the serialization of §4
  "Listings", and the path rules, path-configuration files and free space were read.
- **Bytecode.** Every file in every `__pycache__` directory under `tools/`, the environment's `site-packages` and the
  base interpreter's prefix was listed before the interpreter probes and again after them. A further probe classified
  every module loaded by the same imports by whether it had a cached bytecode file, and the listing was taken once
  more after it.
- **Static source reading.** Three installed aiida-core 2.9.2 source files were read as text and bound to their
  installed `RECORD` hashes. They were not imported.

The probes differ from a W1 run in four deliberate ways. The probe file is not `tools/w1_driver.py`, so the script
directory on the import path is the probe's directory, not `tools/`. The shell chain is a simulation without AiiDA,
without the transport and without the scheduler's backgrounding. No F1 capture, no F3 distribution reading and no job
was made. And no AiiDA configuration directory was created: the probe's `AIIDA_PATH` named a project-local directory
that does not exist.

Every observation in this record is a software or environment observation of this project. It is not chemistry
evidence, and no chemistry evidence class applies to it
([evidence policy §3](../evidence-policy.md#3-language-model-output)). Each command, with its exit code and output, is
retained privately and bound by digest (Section 10). **The probed state** is the working tree after the application
and before this record and the other documentary files of the application were written: HEAD
`af7a8983a7a4c3d52c882ff9a2f63923823e85f6`, with seven tracked files changed from HEAD by documentary edits and two
untracked files (Section 4.4).

## 2. Disposition

**INDETERMINATE before execution.** The disposition is not BLOCKED: no retained observation shows that a requirement
of the revised text cannot be satisfied. It is not a pass, and it is not readiness: the requirements of Section 4.6 and
the run-time checks of Section 5 can only be observed in a run, and none was started. The specification's stop rule
([§8](C3-WIRING-TEST-PROPOSAL.md#8-stop-conditions-and-failure-handling)) governs a run that stops. No run was started,
and no executed W1 failure or pass is claimed.

## 3. The earlier blockers under the revised text

### 3.1 W1-BLOCKER-E2: the runner's environment

**Revised requirement.** [§5](C3-WIRING-TEST-PROPOSAL.md#5-f7-no-login-shell-anywhere-and-a-declared-environment)
item 1 keeps three records apart. The launcher record must equal the five-variable allow-list and its declared values,
and a platform-injected name in it stops W1. The interpreter record must include every allow-list name and lie within
the allow-list and `env_policy.platform_injected`, which is exactly `["__CF_USER_TEXT_ENCODING"]`. The payload record
is compared as §3 declares.

**Observations.** These are software observations of this project, under `-E -s -B`.

| Observation | Result |
|---|---|
| Launcher record | Exactly `AIIDA_PATH`, `LC_ALL`, `PATH`, `PYTHONNOUSERSITE` and `TMPDIR`, with the declared values; no platform-injected name; `BASH_ENV`, `ENV` and `HOME` absent |
| Interpreter record, immediately after `import os` | The five names plus `__CF_USER_TEXT_ENCODING`. Each allow-list value equals the launcher record's value. `BASH_ENV`, `ENV` and `HOME` absent |
| Interpreter record at the runner's end | Identical to the record at start |
| `/usr/bin/env` started with the launcher record as its explicit environment | Exactly the five names |
| `/usr/bin/env` started with the runner's own environment | The five names plus `__CF_USER_TEXT_ENCODING` |
| Simulated payload record's `/usr/bin/env` output | `AIIDA_PATH`, `LC_ALL`, `OMP_NUM_THREADS`, `PATH`, `PWD`, `PYTHONNOUSERSITE`, `SHLVL`, `TMPDIR`, `_` and `__CF_USER_TEXT_ENCODING`: within the permitted set of §3. The five values equal the launcher record's, `OMP_NUM_THREADS` is `1`, and the injected name has the interpreter record's value |
| The other simulated payload-record lines | `dollar_zero=w1_payload.sh`; flags contain `e` and `u` and not `i`; `login_shell=off`; `bash_version` equal to the Bash version probe; `bash_path=/bin/bash`; the three `uname` values equal to the runner's `os.uname()` |

**Disposition.** W1-BLOCKER-E2 no longer blocks as specified. The pre-run records conform to the revised rule. The
run's own records are not reached, and the payload result is a simulation without AiiDA, not a run observation.

**Not established.** The cause of the injected name and when it first appears are not established. That
CoreFoundation sets it remains an `[AGENT]` inference. A different or second injected name, on another host or
interpreter or at another time, would still stop W1.

### 3.2 W1-BLOCKER-E1: the drivers

**Revised requirement.** [§2](C3-WIRING-TEST-PROPOSAL.md#2-declared-setup), row "Class and module": both driver files
are untracked at the declared commit and are not required to be tracked at any commit. §4 captures their bytes, with
their SHA256 and Git blob identifiers, as inputs of each job.

**Observations.** Neither `tools/w1_driver.py` nor `tools/w1_job.py` exists. There is no `tools/__pycache__`
directory, so neither file has a cached bytecode file.

**Disposition.** W1-BLOCKER-E1 no longer blocks as specified: the declaration no longer conflicts with a boundary that
permits no commit. The drivers still have to be written before a run. That is a prerequisite of a run, not a defect of
the text, and it needs the separate authorization of the
[packet, §10.2](W1-REVISION-DECISION-PACKET.md#102-prerequisites), item 4. It is not satisfied now.

### 3.3 U-F1P: ignored and private source files

**Revised requirement.** §4 fixes the capture point, before any import outside the standard library. It captures
every regular file of the environment's `site-packages` as bytes in `code_private`. It takes two module listings, at
the input point and after job 2, and counts extension modules as module files. A module file anywhere else in the
repository's ignored area stops W1.

**Observations.**
- The superset is 18 448 regular files, 374 182 654 bytes: 6 834 `.py`, 6 834 cached bytecode files, 180 `.so`
  extension modules, 33 dynamic libraries and 4 567 other files. This equals the packet's observation S2.
- Every path is valid UTF-8 and holds no TAB or LF byte. There is no symbolic link and no other non-regular file.
- No `.pth` file exists at any depth, and no editable-install finder or `.egg-link` file exists.
- 89 `*.dist-info` directories are present.
- Under `-E -s -B`, startup loaded no module from `site-packages`.
- The import path held the probe's directory, three entries under the base interpreter's prefix and the
  environment's `site-packages`, and nothing else. The probe's directory lies in the repository's git-ignored
  private area, outside `site-packages`. It was on the path only because the probe ran from there; a W1 run would put
  the driver's directory, `tools/`, there instead. Apart from the probe's directory, no entry pointed into the
  repository's ignored area outside `site-packages`.
- The only loaded module whose file lay outside the base prefix was the probe itself, as `__main__`.

**Disposition.** U-F1P no longer blocks as specified: a capture design is now declared. The pre-run preconditions that
can be measured hold. Whether every module that AiiDA loads falls into a permitted class is untested, because AiiDA
was not imported. Two examples are a module file of the one `not-in-lock` distribution, or a file listed with an empty
hash.

## 4. The prerequisites of the packet's §10.2, item 3

Each row states whether the item was **verified at the probed state** by a retained observation, or remains an
**untested requirement**.

### 4.1 Launcher and interpreter records under `-E -s -B`

Verified at the probed state, as Section 3.1 shows. In addition:
- the interpreter reads back as CPython 3.12.14;
- `sys.executable` equals `sys.prefix` joined with `bin/python`, and `sys.prefix` is the declared environment;
- the binary it resolves to has SHA256 `bc56ea9cdc0fface1eb75712f871a454324f6cbfec4e30311b197f208a7f3d07`, the same as
  in the first determination;
- the flags read `ignore_environment` 1 and `no_user_site` 1.

### 4.2 `sys.flags.dont_write_bytecode` and the bytecode policy

- **Verified:** `sys.flags.dont_write_bytecode` reads `1` in the runner.
- **Bytecode stability:** the listing of §4 "The bytecode policy" held 7 216 files, 6 834 under `site-packages`, 382
  under the base prefix and none under `tools/`. It was byte-identical before the interpreter probes, after them, and
  after the classification probe.
- **Not shown:** that `-B` prevents a write. Of the modules loaded by the probes' imports, all 40 loaded from source
  files already had a cached bytecode file. The others were built in (33) or frozen (17), or were the probe itself or
  submodule objects without a file of their own. No import of a source module without a cached bytecode file was
  tested, so the equal listings do not demonstrate that bytecode writing was suppressed. The revised text checks `-B`
  only at run time, through the flag and the stability comparison.

### 4.3 The declared Git invocations and configuration bounds

Verified at the probed state. Every declared invocation exited 0 with no error output. All outputs were identical
between the two rounds, the code diff included. The raw `.git/index` was unchanged across all of them, with SHA256
`8e12f22521a8d144f4a31d3547340959a90766e62a978099204bcaf950f688f9`.

| §4 precondition | Result |
|---|---|
| Every configuration entry has the origin `file:.git/config` | Holds: 12 entries |
| No forbidden configuration key | Holds |
| No `.git/info/attributes`; no `.gitattributes` in the root or in a directory that contains an index or untracked path | Holds. Three directories hold a `.gitattributes` file, all in the git-ignored area, none containing such a path |
| `.git/info/exclude` | One rule; its SHA256 is recorded privately |
| Object format `sha1`; index path `.git/index` | Holds |
| Every index entry has stage `0` and no mode `160000` | Holds: 77 entries |
| Every `flags:` field of `ls-files --debug` is `0` | Holds: 77 of 77, in both rounds |
| Every index and untracked path is a regular file | Holds |
| `site-packages` holds no symbolic link | Holds |
| Git version | `git version 2.39.5 (Apple Git-154)` |

One probe defect is disclosed. The Git probe first reported the flags condition as failing. It had tested for lines
beginning with `flags:`, while Git prints the field after `size:` on the same line, so it counted no field at all. A
re-parse of the retained outputs, which ran no Git command, found the 77 fields above, all `0`. Both results are
retained.

### 4.4 The untracked listing and the code diff at the probed state

- **Untracked listing.** Under the declared Git environment, the listing held two files: a local tool-settings file of
  the account, which a user-level ignore rule hides in an ordinary shell, and the decision packet. Both would be
  captured into the private store.
- **New documentary files.** The files of this application that are new were written after the probes. Until they
  are delivered they would join the listing too.
- **Code diff.** It covered seven tracked files: the six documentary files changed by the proposal task, and the
  applied specification.

Any change to a captured file between the capture point and the run end stops W1. The tool-settings file can be
written by tools that the account runs. This is an operational risk for a run, not a blocker of the text.

### 4.5 The user-level observation paths

Verified at the probed state, over a window of seconds:
- All eleven paths of §5 could be observed without error.
- `.aiida` and `.ase` are absent. The home directory and the other eight paths are directories whose top-level entries
  could be listed.
- The two observations around the runner were equal.
- Without `HOME`, the runner's `os.path.expanduser('~')` returned the home directory given by the password database.
  Paths that AiiDA derives from `~` (A12, A13) would therefore point into the account's home directory.
- The base interpreter's prefix lies below the top level of one observed directory, where the observation does not
  look. Its cached bytecode is covered by the bytecode listing instead.

**Untested:** stability over the length of a run. Another process can add or remove a top-level entry, for example in
a cache directory, and that stops W1, as §5 states.

### 4.6 Carriage of the declared superset through each job: untested requirement

Whether the job machinery carries the declared superset through each job's folder, input manifest and binding is an
**untested requirement**. It cannot be observed without importing AiiDA and running a job, and neither was done.

**Static source reading.** Three files of the installed aiida-core 2.9.2 were read as text. Their SHA256 values match
their entries in the installed `RECORD`.

| File | SHA256 | What the text defines |
|---|---|---|
| `aiida/engine/daemon/execmanager.py` | `92c2b1d96b96c2594bd03673f1b3af72714209097bd3c5b2d0ebeff220a12dbd` | The upload step copies the sandbox folder to the work directory (lines 393–400). It copies each `local_copy_list` item from its input node's repository to the work directory only (lines 335–392). It stores in the job node's repository every file of the sandbox folder that `provenance_exclude_list` does not exclude, and nothing else (lines 245–273) |
| `aiida/engine/processes/calcjobs/calcjob.py` | `7ebd9157f19d7e04144d88cf18ce631d675dcecdde0c413b7a2a909616efbe2e` | `presubmit` receives the sandbox folder in which the input files and the submission script are written (lines 932–935) |
| `aiida/common/folders.py` | `5a707f11cd24a3f07cf7e43d9444d63ba202bda61cd3ff1a4f8c8b5dd44132c9` | A sandbox folder is created by `tempfile.mkdtemp`, in a configured sandbox directory when one is given (lines 403–415) |

*Project inferences (`[AGENT]`), not observations:*
- §3 compares each job's input manifest with the files "as stored for the submission in the job node's repository".
  To meet that, `W1Job` would have to write every F1 input, the 18 448 files of `code_private` included, into the
  sandbox folder itself. Items carried by `local_copy_list` would not be stored in the job node's repository.
- Each job would then hold the superset in its sandbox folder, under the project-local `TMPDIR` unless a sandbox
  directory is configured, in its node repository and in its work directory, beside the `code_private` input node.
- The `presubmit` digests, the three-way binding of §5 and the payload's `shasum` would each cover about 18 000 files.

**Untested:** whether aiida-core carries these files through `presubmit`, the node repository, the work directory and
the payload within a practical time; whether the store deduplicates the copies; and the run's total size. The file
system that holds the repository had 554 070 908 928 bytes free at the probe, about 1 480 times the superset's size.
That ratio does not show that a run fits.

### 4.7 Other untested requirements

- **AiiDA without `HOME`.** How aiida-core behaves without `HOME`, which modules it loads late, and whether any lies
  outside the permitted classes of §3, are unobserved.
- **Per-distribution checks.** The per-distribution `RECORD` checks of §3 were not repeated. The first determination
  observed them on 2026-09-29. The superset's file count and size are unchanged since the packet's S2.
- **Run-time records.** Every record that only a run makes is untested: the profile, the computer read-back, the
  `presubmit` validation, the payload record of a real job and the run-end comparisons.

## 5. Requirement dispositions

The vocabulary is that of the first determination: **demonstrated** (retained evidence shows the requirement holds;
"before any run" marks a pre-run observation, not a W1 result), **unmet** (evaluated in a run and failed; unused),
**blocked** (pre-run evidence shows it cannot be satisfied; unused here), and **not reached** (not evaluated, because
W1 was not run). The same dispositions are in [w1-outcome-02.json](w1-outcome-02.json).

### 5.1 Declared setup and mandatory values (§2, §4, §5)

| Requirement | Disposition | Basis |
|---|---|---|
| §2 Python environment | demonstrated before any run, for the interpreter's read-back, executable and prefix | Section 4.1. The per-distribution checks are not repeated |
| §2 Profile and storage, Computer, Code | not reached | Nothing was created |
| §2 Runner: launcher and runner, each `-E -s -B` | demonstrated before any run, for the invocation and the three environment records | Sections 3.1 and 4.1, with a probe file in place of the driver |
| §2 Class and module: untracked drivers | not reached | The drivers do not exist. Writing them needs separate authorization (Section 3.2) |
| §2 Frozen input and fixed-set fixture | not re-examined | Unchanged since the first determination: the frozen input is bound by digest in the freeze record |
| §4 Git and its bounded configuration and preconditions | demonstrated before any run, at the probed state | Section 4.3 |
| §4 Capture point, superset, listings and bytes | not reached, except the measurable preconditions | No capture was made. Superset and path rules: Section 3.3 |
| §4 Bytecode policy | demonstrated before any run, for the flag and the stability of the listing | Section 4.2. Not a demonstration that `-B` prevents a write |
| §5 item 1: three environment records | demonstrated before any run | Section 3.1 |
| §5 items 2 and 3: transport and job environment | not reached | No computer or job was created |
| §5 user-level observation | demonstrated before any run, for observability and equality over seconds | Section 4.5 |
| §5 `presubmit` validation and three-way binding | not reached | Untested (Section 4.6) |

### 5.2 Acceptance criteria (§7)

| # | Criterion (abridged) | Disposition | Basis |
|---|---|---|---|
| 1 | Two CalcJob nodes with exit status 0, process type `w1_job.W1Job`, every port an input of each | not reached | No job was created |
| 2 | Every F4 check passes; every negative case fails | not reached | No checker was run |
| 3 | The F1 items resolve as bytes, are inputs of both jobs, and every §4 comparison holds | not reached | No capture; carriage untested (Section 4.6) |
| 4 | Launcher and interpreter records, payload record, no-login setting, `presubmit` validation, three-way binding | not reached | The pre-run records conform (Section 3.1), but the criterion concerns the run's records |
| 5 | The stored provenance inputs satisfy "Mandatory contents" key by key | not reached | No input node was created |
| 6 | Every repository object's key equals its SHA256 | not reached | No node was created |
| 7 | Equal user-level observations; the fixture-diff check | not reached | Pre-run observations were equal (Section 4.5) |

### 5.3 Stop conditions (§8)

| # | Stop condition (abridged) | Disposition | Basis |
|---|---|---|---|
| 1 | A user-level AiiDA directory appears, or the user-level observations differ | not reached | `.aiida` absent; pre-run observations equal |
| 2 | The three-record environment rule fails | not reached; not indicated | Pre-run records conform (Section 3.1) |
| 3 | `use_login_shell` reads back true | not reached | No computer was created |
| 4 | `presubmit` raises, or the three copies differ | not reached | Untested (Section 4.6) |
| 5 | Process type differs from `w1_job.W1Job` | not reached | No job was created |
| 6 | A §4 precondition fails, or a §4 comparison differs, bytecode included | not reached; preconditions hold at the probed state | Sections 4.2 to 4.4 |
| 7 | A required link is missing | not reached | No job was created |
| 8 | A job returns 310, 311 or 312 | not reached | No job was created |
| 9 | A provenance input fails "Mandatory contents" | not reached | No input node was created |
| 10 | A declared §3 comparison fails (build identity, host record, payload record, loaded module file) | not reached; not indicated for the payload record | The simulated payload record conforms. This is a simulation without AiiDA |
| 11 | A `distributions` entry fits no status | not reached | Not re-examined |
| 12 | An F4 check fails | not reached | No F4 check was run |
| 13 | A negative case passes | not reached | No negative case was run |
| 14 | A project or unclassified module file is first listed at the run end | not reached | AiiDA was not imported |
| 15 | The fixture diff fails its check | not reached | `w1_job.py` does not exist |

## 6. What this establishes and what it does not

**Established.** These are software and environment observations of this project at the probed state, with no
chemistry class:
- the earlier blockers E2 and E1 and the requirement U-F1P no longer block under the revised text;
- the launcher and interpreter records, the bytecode flag, the declared Git invocations and bounds, the superset's
  measurable preconditions and the user-level observation paths conform to the revised text;
- the specification in force is byte-identical to the approved revision 01.

**Not established.**
- That W1 can be executed to a pass under the revised text. That is untested.
- The carriage of the superset through the job machinery, and the run's size and duration (Section 4.6).
- How aiida-core behaves on this host. AiiDA was not imported.
- That `-B` prevents bytecode writes (Section 4.2).
- The cause of the injected environment name (an `[AGENT]` inference only).
- The carriage of F1, F2, F3, F4, F5, F6, F8 or F11 through a job chain, and the no-login observation of F7.
- F9. No W1 job existed and none failed. This record demonstrates no preservation of a failed job.
- Anything about chemistry, and any readiness, parity, physical validation or authorization.

## 7. Effect on C3 and on the remaining boundaries

- **C3 blockers closed: none.** Identity-chain survival (F4), the remaining provenance extensions (F1, F2, F3, F5, F6,
  F8, F11) and the login-shell environment gap (F7, D2) all stand, as listed at the end of
  [C3 §5](C3-PROVENANCE-WIRING.md#5-coverage-table). C3 readiness remains BLOCKED.
- **F9** remains a dependency within Stage 1. **F10**, the review record, remains with the orchestration layer.
  **F11** carries labels only.
- Basis normalization remains PARTIALLY ESTABLISHED, and Psi4 runtime conformance remains open. E-01 remains
  technically BLOCKED and scientifically INDETERMINATE.
- The specification is revision 01, applied under the recorded approval. C4, including its opening Approval bullet,
  every approval record and every frozen Stage 0 definition are unchanged. C4-j and B3-b remain deferred.
- Stage 1 remains BLOCKED and is not authorized. Stages 1a, 1b and 2 are not authorized. Scope option A remains
  BLOCKED.

## 8. What a W1 run would still need

1. **A separate authorization by a person** for a W1 run. It must cover writing `tools/w1_driver.py` and
   `tools/w1_job.py` and creating the W1 profile, computer and code
   ([packet, §10.2](W1-REVISION-DECISION-PACKET.md#102-prerequisites), item 4). None is held.
2. **The run itself** is the only way to test the requirements of Sections 4.6 and 4.7, and its outcome is not
   predicted.
3. **A quiet account and working tree during the run.** Every captured file must stay unchanged, the local
   tool-settings file included (Section 4.4). The top-level entries of the eleven user-level paths must stay
   unchanged too (Section 4.5). Otherwise W1 stops, as the specification intends.

## 9. Limits of this record

- **Confinement.** Intentional outputs and temporary files of this determination were kept in the project's
  git-ignored private area. Three matters are disclosed privately:
  - two helper invocations of the operating system's own Python interpreter ran before bytecode writing was
    disabled for them, and that interpreter keeps its bytecode cache in the account's cache directory, outside this
    repository; whether any file was written there is not established;
  - the agent runtime may have kept its own records outside this repository, which were not inspected;
  - during the orchestration layer's startup for this task, an attempted cleanup of a previous orchestration
    workspace failed, and one local orchestration metadata file was lost. A minimal replacement mapping was built
    later from current observations. It is new metadata, not a recovery: the original file's exact bytes are
    irrecoverable.

  This determination cleaned up nothing: neither contents outside this repository nor the evidence of earlier
  incidents. No complete filesystem confinement, no absence of cleanup attempts by any party and no exhaustive audit
  of actions is claimed.
- **Probe defect.** Section 4.3 discloses one parsing defect and its correction.
- **Model self-report.** The agent that made the determination was configured as one model, and it reported a model
  from its own runtime context. Neither is an attestation: the running model and its effort level could not be
  observed independently.

## 10. Evidence bound by digest

The private records are not published. They contain local paths, host details and process identifiers, and they are
identified here by SHA256 only.

| Record | SHA256 |
|---|---|
| Frozen digest list of the private evidence of this determination, version 02: the command records with argument vector, exit code, output and error output, the probe scripts, their outputs and the recorder, 102 files. It supersedes version 01, which listed 92 of them before the classification probe and is retained | `83d1f7db02e883e8f47ea0efcb8293d9758934cecdd3016ea839ac79047c976f` |
| The W1 specification in force, revision 01 | `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347` |
| The interpreter binary that the environment's `bin/python` resolves to | `bc56ea9cdc0fface1eb75712f871a454324f6cbfec4e30311b197f208a7f3d07` |
| The `site-packages` listing, in the serialization of §4 "Listings" | `0934e6deb864c2aa9d56117486348ef183d85d00080d381d8fbde04d4032d497` |
| The bytecode listing, before and after the interpreter probes and after the classification probe | `9cdbd1ded667ad803f5783a769bb6fe1ff951d21d37a062eb640faf804869a1a` |
| The raw `.git/index`, before and after the Git probe | `8e12f22521a8d144f4a31d3547340959a90766e62a978099204bcaf950f688f9` |

This record cites no external source, and no source was retrieved for it. The three aiida-core files of Section 4.6
were read from the installed Stage 0 environment, whose wheel is entry [34] of the
[sources catalogue](../SOURCES.md). The software facts that the specification cites, A1 to A13, are those of its own
sources and are not restated here as observations.
