# W1 provenance wiring test: pre-run determination

Date: 2026-09-29. MS-001 scope option B. **Disposition: W1 BLOCKED before execution. W1 was not run.**

Every statement of status in this record is as of 2026-09-29, when the package inventory that the record's review
binds was frozen.

A person authorized W1, the non-chemistry AiiDA provenance wiring test specified in
[C3-WIRING-TEST-PROPOSAL.md](C3-WIRING-TEST-PROPOSAL.md), in an instruction recorded on 2026-09-29. The
authorization is held privately by the orchestration layer. It covered the preparation, implementation, execution,
review and verification of W1 within stated boundaries, including routine reversible preparation inside the
project-local environment. It did not cover any commit, push or other delivery, any chemistry or engine run, or any
Stage 1 work.

Before implementing anything, the project determined whether the specification can be executed as written within
that authorization. It cannot, for two independent reasons (Section 3):
- **W1-BLOCKER-E2.** The environment of the runner's interpreter holds a name outside the declared five-variable
  allow-list.
- **W1-BLOCKER-E1.** The specification declares that the two driver files are tracked at a commit, and no commit is
  authorized.

A third requirement, the capture of ignored or private source files, has no established conforming design and is
recorded as unresolved.

W1 was therefore not run. **No AiiDA profile, computer, code or job was created, and AiiDA was not imported.** No W1
driver or job class was written. No chemistry was done: no engine was run, nothing was calculated, nothing was
installed and nothing was retrieved over a network.

This record closes **none** of the C3 blockers (Section 7). C3 readiness remains BLOCKED. Stage 1 remains BLOCKED and
is not authorized.

## 1. What was done

A pre-run executability determination was made. It consisted of read-only inspection, hashing, and startup probes of
the Stage 0 interpreter:
- **Repository state.** HEAD, the index, the tracked files and the untracked-file listing were read. The listing was
  read both in the specification's five-variable environment and in an ordinary shell.
- **Interpreter startup.** The Stage 0 environment's `bin/python` was started as the specification requires, with
  `-E -s`, under an environment built with `env -i` that holds exactly the five declared variables. A small
  standard-library script recorded `os.environ`, the loaded modules and the interpreter flags, and spawned
  `/usr/bin/env` as a child. Controls repeated the startup with site processing disabled (`-S`) and ran `/bin/bash`
  without Python.
- **Shell chain.** A shell chain resembling the transport and scheduler invocations the specification cites was
  simulated without AiiDA.
- **Installed distributions.** Every installed distribution was compared with the Stage 0 lock and the retained
  wheels under the specification's applicability rule, using the standard library only.
- **Protected records.** Every tracked file was compared with HEAD, and the declared digests and the export manifest
  were checked.

None of these probes imported AiiDA, ASE or NumPy. Each command, with its exit code and output, is retained privately
and bound by digest (Section 10). Every observation in this record is a software or environment observation of this
project. It is not chemistry evidence, and no chemistry evidence class applies to it
([evidence policy §3](../evidence-policy.md#3-language-model-output)).

## 2. Disposition

**W1 BLOCKED before execution.** The disposition is BLOCKED, not INDETERMINATE: the blockers are unsatisfied
prerequisites that the retained evidence shows. The specification's own stop rule ([§8](C3-WIRING-TEST-PROPOSAL.md#8-stop-conditions-and-failure-handling))
governs a run that stops. It does not require starting a run in the face of a known blocker, and none was started.
This determination produced no executed W1 failure, and none is claimed.

## 3. The blockers

### 3.1 W1-BLOCKER-E2: the runner's environment

**Requirement.** [§5](C3-WIRING-TEST-PROPOSAL.md#5-f7-no-login-shell-anywhere-and-a-declared-environment), item 1:
"The runner records `os.environ` at start, and its names must equal `env_policy.allow_list` exactly." The allow-list
is the five variables `PATH`, `LC_ALL`, `AIIDA_PATH`, `TMPDIR` and `PYTHONNOUSERSITE`.
[§2](C3-WIRING-TEST-PROPOSAL.md#2-declared-setup) fixes the interpreter, the Stage 0 environment's own
`bin/python` ("Nothing is installed"), and the invocation, `-E -s`.

**Observations.** These are software observations of this project.

| Observation | Result |
|---|---|
| Environment handed to the interpreter by `env -i` | Exactly the five declared names |
| `os.environ` in the startup script, recorded after `import os` and `import sys` | Six names: the five, plus `__CF_USER_TEXT_ENCODING` |
| The same with site processing disabled (`-S`), recorded after `import os,sys` | The same six names |
| A child `/usr/bin/env`, started without a shell | Inherits the sixth name |
| A simulated shell chain, Python → `sh -c` → `bash` → `bash <script>` → `/usr/bin/env`, without AiiDA | The sixth name reaches the final `/usr/bin/env` |
| `/bin/bash --noprofile --norc` run under the same five names, without Python | No sixth name |
| Linkage of the interpreter binary that `bin/python` resolves to (SHA256 `bc56ea9cdc0fface1eb75712f871a454324f6cbfec4e30311b197f208a7f3d07`) | It links the CoreFoundation framework. `/bin/bash` and `/usr/bin/env` do not |

**What follows.** The runner's record of `os.environ` at start cannot equal the allow-list, so §5 item 1 and
[§7](C3-WIRING-TEST-PROPOSAL.md#7-acceptance-criteria) criterion 4 cannot hold. §8's stop condition "any variable
outside the Section 5 allow-list is present in the parent" would trigger at the runner's first record.

The simulation also indicates that the payload record's `/usr/bin/env` output would carry the name. [§3](C3-WIRING-TEST-PROPOSAL.md#3-node-boundary-the-w1-calcjob-class)
states that such a name "fails the F7 criterion; it is retained as a finding and is not added to the set
afterwards". No conforming implementation choice removes the name:
- adding it to the parent would add a sixth variable;
- deleting it inside the runner would falsify the record at start;
- allowing it would relax an acceptance rule that the specification expressly keeps;
- another interpreter would mean a different environment.

**Not established.**
- When the name first appears in the process, and why, are not traced.
- That CoreFoundation, loaded with the interpreter, sets the name is an `[AGENT]` inference from the controls and the
  linkage. The linkage is an observation, not an established cause.
- The blocker rests on the observed presence of the name, not on its cause.

### 3.2 W1-BLOCKER-E1: tracked drivers and the no-delivery boundary

**Requirement.** [§2](C3-WIRING-TEST-PROPOSAL.md#2-declared-setup), row "Class and module": "Both files are tracked
at the declared commit, and their bytes are also inputs of each job (Section 4)". The files are `tools/w1_driver.py`
and `tools/w1_job.py`.

**Observations.**
- Neither file exists at the authorized baseline commit `989e566b6009e9ca7c78c8b11a5e6efbe9f551fd`.
- The authorization permits no commit.
- Staging can make a file tracked in the index, but never "at the declared commit".

**What follows.** The declaration cannot be satisfied under the present specification together with the no-delivery
boundary. It is a declared requirement, so it is disposed as blocking, even though no §7 criterion and no §8 stop
condition repeats it. This blocker is independent of W1-BLOCKER-E2.

Capturing both drivers as untracked files under [§4](C3-WIRING-TEST-PROPOSAL.md#4-f1-the-code-that-ran-captured-once)
would keep their bytes. It would not make them tracked at a commit. It is recorded only as a proposed revision
(Section 8) and is not applied.

### 3.3 Unresolved requirement U-F1P: ignored or private source files

**Requirement.** [§4](C3-WIRING-TEST-PROPOSAL.md#4-f1-the-code-that-ran-captured-once): "the contents of every ignored
or private source file used are added explicitly. The list is built two ways, from the loaded modules whose files
lie in the repository and from a declared list. A difference between the two stops the test."

**Observation.** The Stage 0 environment lies inside the repository's working tree, under its git-ignored
private area. Every module file that a W1 runner loaded from the environment's `site-packages` would therefore be an
ignored file that lies in the repository. §4 states no exemption for it. The per-distribution check of §3 is a
separate obligation, and it does not discharge §4's capture.

**Not established.** No conforming capture design is established. The specification does not state:
- at what point in the run the loaded-module list is taken;
- how module files first loaded after the single capture are treated;
- whether compiled extension modules count as source.

No conforming capture design was established, and neither was the runner's actual import set, on which a declared
list could be based. None of this shows that such a capture is impossible. The requirement is recorded as unresolved
and would block a run until it is settled.

## 4. Other observations, which are not blockers

- **Installed distributions ([§3](C3-WIRING-TEST-PROPOSAL.md#3-node-boundary-the-w1-calcjob-class) applicability
  rule).** Software observations of this project.
  - 89 distributions are installed in the environment's `site-packages`.
  - 88 are `locked-verified`. For each, the retained wheel's SHA256 is among the lock hashes, and every file that the
    wheel's `RECORD` lists with a hash matches its installed file: 10 914 comparisons, with no mismatch and no missing
    file.
  - One, the installer pip 25.0.1, is `not-in-lock`. No entry fits no status.
  - Every installed `RECORD` check passes.
  - aiida-core 2.9.2 (wheel SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`) and ASE
    3.29.0 (wheel SHA256 `7b9dd103f007810339c24acfee2f6b677c0c48443b21d3c98e52959246cf4ebf`) are `locked-verified`
    at their declared digests.
  - NumPy 2.5.3 is `locked-verified`, with wheel SHA256
    `a72f874bc9e10e4b8f80426fb49716d5141f64442a0c8418065093ec8017fbb0` among its lock hashes.

  The lock digest establishes the lock's bytes only. These comparisons are the specification's per-distribution
  test, within its stated limits, and cached bytecode is observed only.
- **Interpreter startup.** Under `-E -s`, startup loaded no module from `site-packages`. No `.pth` file is at the top
  level of the environment's `site-packages`. Other locations were not searched for `.pth` files.
- **`PYTHONNOUSERSITE`.** With `-E`, the interpreter ignores `PYTHONNOUSERSITE`, and `-s` alone disables the user
  site directory. The variable nevertheless stays in `os.environ` and is inherited, so it still takes part in the
  allow-list comparison. This redundancy is recorded, and the invocation is not changed.
- **`HOME` absent.**
  - The interpreter starts normally without `HOME`.
  - Git then does not apply a user-level ignore rule, so one local tool-settings file that that rule normally hides is
    listed among the untracked files. A future run under §4 would capture it.
  - How AiiDA or its dependencies behave without `HOME` was not examined.
- **`bash` resolution.** `PATH=/usr/bin:/bin` resolves `bash` to `/bin/bash`.
- **Protected records.**
  - At the baseline commit, all 75 tracked files matched HEAD, including every file under `results/e01/` and every
    artifact bound in the [freeze record](STAGE0-FREEZE-RECORD.md#2-frozen-artifacts).
  - The frozen input `structures/donor-activated-EAOGe-C2-radical.extxyz` (SHA256
    `bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3`) and the Stage 0 lock (SHA256
    `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8`) equal their declarations.
  - The specification is unchanged at SHA256 `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158`.

## 5. Requirement dispositions

Every disposition in this section is a status at the freeze of the package inventory that the record's review
binds (2026-09-29). None predicts a later decision.

**Vocabulary.**
- **demonstrated:** retained evidence shows that the requirement holds. Where marked "before any run", this is a
  pre-run observation, not a W1 result.
- **unmet:** the requirement was evaluated in a W1 run and failed. No entry has this status, because no run occurred.
- **blocked:** pre-run evidence, or the no-delivery boundary of the authorization, shows that the requirement cannot
  be satisfied as specified. For a stop condition, it shows that the condition would be triggered.
- **not reached:** the requirement had not been evaluated at the inventory freeze. For W1's own requirements this is
  because W1 was not run. For T7 it is because the decision is taken outside this record.

The same dispositions, with the exact quoted text of each §8 stop condition, are in [w1-outcome.json](w1-outcome.json).

### 5.1 Declared setup and mandatory values (§2, §4, §5)

| Requirement | Disposition | Basis |
|---|---|---|
| §2 Python environment: the Stage 0 environment, aiida-core 2.9.2, ASE 3.29.0, lock SHA256 `813b2d9a…`, nothing installed | demonstrated before any run, for the lock digest and the aiida-core and ASE versions and statuses | Section 4. The runner's own read-back of CPython 3.12.14 is not reached |
| §2 Profile and storage (a new `core.sqlite_dos` profile with no broker) | not reached | No profile was created |
| §2 Computer `w1-local-nologin` | not reached | No computer was created |
| §2 Code `w1-bash` | not reached | No code was created |
| §2 Runner (`bin/python -E -s`, in-process, no daemon) | blocked | The invocation's environment conflicts with §5 item 1 (W1-BLOCKER-E2) |
| §2 Class and module: both drivers "tracked at the declared commit" | blocked | W1-BLOCKER-E1 |
| §2 Frozen input: SHA256 `bb7ab344…`, 48 atoms, per-atom `atom_id`, `map_num` and `radical_electrons` | demonstrated before any run | Digest equal; 48 atom lines; header declares the three per-atom fields |
| §2 Fixed-set fixture: six atoms by `atom_id` | demonstrated before any run, for presence | All six `atom_id` values are present in the frozen file. The fixture checks themselves are not reached |
| §4 Declared commit and diff | not reached | No capture was made. The authorized baseline is `989e566…` |
| §4 Untracked files | not reached | No capture was made |
| §4 Ignored and private files, with the two-way list | blocked (unresolved) | U-F1P |
| §4 One capture, and bytes rather than digests | not reached | No capture was made |
| §5 item 1: parent environment | blocked | W1-BLOCKER-E2. An exact five-name parent can be constructed, and `bash` resolves to `/bin/bash`, but `os.environ` at start holds a sixth name |
| §5 item 2: `use_login_shell` false, read back before any transport call | not reached | No computer was created |
| §5 item 3: job environment (`import_sys_environment` true, only `OMP_NUM_THREADS=1` added) | not reached | No job was created |
| §5 `presubmit` validation and three-way binding | not reached | No job was created |

### 5.2 Acceptance criteria (§7)

| # | Criterion (abridged) | Disposition | Basis |
|---|---|---|---|
| 1 | Exactly two CalcJob nodes, `w1-job1` and `w1-job2`, with exit status 0, process type `w1_job.W1Job`, and every §3 port an input of each | not reached | No job was created. W1-BLOCKER-E1 and W1-BLOCKER-E2 prevent a run |
| 2 | Every F4 check passes at every stage, and every negative case fails | not reached | No conversion sequence and no checker was run |
| 3 | The F1 items resolve from the store as bytes, with digests unchanged over the run | not reached | No capture and no store exist. W1-BLOCKER-E1 and U-F1P also bear on its preconditions |
| 4a | The Section 5 environment in the parent, and every payload-record comparison of Section 3 | blocked | W1-BLOCKER-E2 |
| 4b | `use_login_shell` false in the effective configuration | not reached | No computer was created |
| 4c | A `presubmit` validation that passed | not reached | No job was created |
| 4d | The three-way byte binding of the submission files | not reached | No job was created |
| 5 | The stored provenance inputs of both jobs satisfy "Mandatory contents" key by key, with the additional manifest and module-file checks | not reached | No input node was created. The pre-run distribution observations (Section 4) are consistent with the `aiida_core`, `ase` and `numpy` requirements but are not the run's check |
| 6 | Every repository object of every chain node has a key equal to its SHA256 | not reached | No node was created |

### 5.3 Stop conditions (§8)

| # | Stop condition | Disposition | Basis |
|---|---|---|---|
| 1 | A user-level AiiDA configuration directory appears | not reached | AiiDA was not imported. No such directory existed before or after the determination |
| 2 | Any variable outside the Section 5 allow-list is present in the parent | blocked: would trigger | W1-BLOCKER-E2 |
| 3 | `use_login_shell` reads back true | not reached | No computer was created |
| 4 | The `presubmit` validation raises, or the three copies of a submission file differ | not reached | No job was created |
| 5 | The process type differs from `w1_job.W1Job` | not reached | No job was created |
| 6 | A code capture changes during the run | not reached | No capture was made |
| 7 | A required link is missing | not reached | No job was created |
| 8 | A job returns 310, 311 or 312 | not reached | No job was created |
| 9 | A provenance input fails its "Mandatory contents" declaration | not reached | No input node was created |
| 10 | A declared, applicable Section 3 comparison fails (build identity, host record, payload record or a loaded module file) | blocked for the payload record: indicated to trigger. Not reached for the other comparisons | The simulated shell chain carries the sixth name to `/usr/bin/env` (W1-BLOCKER-E2). This is a simulation without AiiDA, not a run observation |
| 11 | A `distributions` entry fits none of the three statuses | not reached | All 89 entries fitted a status in the pre-run observation, which is not the run's check |
| 12 | An F4 check fails | not reached | No F4 check was run |
| 13 | A negative case passes | not reached | No negative case was run |

### 5.4 The task's own acceptance criteria

These are paraphrased from the private authorization of this task. They are process criteria, not evidence.

| # | Criterion (paraphrased) | Disposition | Basis |
|---|---|---|---|
| T1 | The implementation corresponds to the specification, and every declared requirement is exercised or disposed as unmet or blocking | demonstrated, by disposition, at the inventory freeze | No implementation was written. Every requirement above is disposed |
| T2 | The profile, computer, code and two-job chain are recorded without leaking local identifiers, and the checks are demonstrated or precisely failed | not reached, at the inventory freeze | Nothing was created. A precise pre-run blocker is recorded instead |
| T3 | Every public machine-readable artifact parses; every claim is classified and traceable; every relative link and anchor resolves | demonstrated for parsing and links, at the verifier run over the frozen package | Parsing and links were checked by a deterministic verifier over this package, recorded privately. Claim classification rests on the text of this record and its review, not on a mechanical check |
| T4 | The manifest covers every public file except itself with exact SHA256; protected paths are unchanged; no chemistry output | demonstrated, at the verifier run over the frozen package | As T3 |
| T5 | The configured repository check, W1-specific verification with negative controls, privacy scans and inventory and hash checks pass | demonstrated for the pre-run package, at the verifier run over the frozen package | The configured check exited 0. The W1-specific checks cover the pre-run evidence and this package only |
| T6 | Documentation states the disposition and its effect on C3 and preserves every blocker and boundary | demonstrated, at the inventory freeze, as this record's own statement | This record, and the navigation and state updates listed in the export manifest. Their review is held outside this record, as for T7 |
| T7 | Independent review approval and Lead acceptance | not reached, at the inventory freeze; the final decisions are held outside this record | This record states no review outcome. The review record, F10, is held by the orchestration layer and is never inside the inventory that the review binds, so the disposition of T7 is recorded there, not here. No outcome is asserted or predicted |
| T8 | The working tree is left uncommitted, and nothing is pushed | demonstrated, when the verifier ran | No commit or push was made |

## 6. What this establishes and what it does not

**Established.** These are software and environment observations of this project, with no chemistry class.
- W1, as specified, cannot be executed to a pass, for the two independent reasons of Section 3:
  - on this host, the interpreter's environment conflicts with §5 item 1 (W1-BLOCKER-E2);
  - under the authorization's no-delivery boundary, the tracked-driver declaration cannot be met (W1-BLOCKER-E1).
- The installed Stage 0 distributions correspond, per distribution, to the lock and the retained wheels, within the
  limits of F3 (Section 4).
- The protected records were unchanged when checked.

**Not established.**
- Anything about chemistry: no energy, force, gradient, structure, population or engine behaviour.
- Whether W1 would pass under a revised specification. That is untested.
- The cause of the environment name and when it first appears (an `[AGENT]` inference only).
- How aiida-core behaves on this host. AiiDA was not imported.
- The carriage of F1, F2, F3, F4, F5, F6, F8 or F11 through a job chain, and the no-login observation of F7.
- F9. No W1 job existed and none failed. This record is a pre-run determination, not the failure record of a run,
  and it demonstrates no preservation of a failed job.
- Readiness, parity, physical validation or any authorization.

## 7. Effect on C3 and on the remaining boundaries

- **C3 blockers closed: none.** Identity-chain survival (F4), the remaining provenance extensions (F1, F2, F3, F5, F6,
  F8, F11) and the login-shell environment gap (F7, D2) all stand, as listed at the end of
  [C3 §5](C3-PROVENANCE-WIRING.md#5-coverage-table). C3 readiness remains BLOCKED.
- **F9** remains a dependency within Stage 1. **F10**, the review record, remains with the orchestration layer.
  **F11** carries labels only.
- Basis normalization and Psi4 runtime conformance are outside W1 and unchanged: normalization remains PARTIALLY
  ESTABLISHED, and runtime conformance remains open.
- The specification [C3-WIRING-TEST-PROPOSAL.md](C3-WIRING-TEST-PROPOSAL.md) is unchanged. So is every frozen Stage 0
  definition, including C4 and its opening Approval bullet.
- Stage 1 remains BLOCKED and is not authorized. Stages 1a, 1b and 2 are not authorized. Scope option A remains
  BLOCKED.

## 8. Proposed revisions, for a person's decision

Each option below is an `[AGENT]` proposal. None is chosen, approved or applied, and the specification is unchanged.
A revised W1 would need its executability determined again before any run, under whatever authorization a person
gives.

| Blocker | Options |
|---|---|
| W1-BLOCKER-E2 | **O1.** Declare `__CF_USER_TEXT_ENCODING` as a recorded, platform-injected name, permitted in `os.environ` at start and in the payload record. Verify the five-name environment that the runner is started from with a separate launcher record. This changes an acceptance rule. **O2.** Require an interpreter that does not link CoreFoundation. That needs a different environment from the Stage 0 environment that the specification declares ("Nothing is installed") |
| W1-BLOCKER-E1 | **R-E1a.** Replace "tracked at the declared commit" with capture of both drivers as untracked files under §4, with their bytes retained as job inputs. **R-E1b.** A person decides, separately, to commit the two drivers before a run. That is a delivery decision |
| U-F1P | **R-P1.** Exempt environment sources explicitly from the §4 private capture, relying on the §3 wheel-`RECORD` check. **R-P2.** Specify the capture fully: the point at which the list is taken, the treatment of modules first loaded after the capture, and whether compiled extension modules count as source |

A revision should also define "the index state" of §4 and state git's behaviour under the declared environment,
including the user-level ignore rule that is not applied without `HOME`. It should also set a bytecode-write policy,
add a check for user-level side effects beyond `~/.aiida`, and declare the contents of the `code_identity`,
`fixture_diff` and sidecar inputs, which the specification leaves undeclared.

## 9. Limits of this record

- **Confinement.** Three writes fell outside the project's private working area, all outside this repository:
  - the agent runtime persisted one oversized command output in its own storage;
  - an agent wrote a memory note, and one index line for it, to the runtime's storage in the user's home area.

  These are confinement breaches. They are disclosed in the private record and, as directed, were not cleaned up:
  the task confines work to this repository.
- **Audit.** No complete filesystem confinement and no exhaustive audit of actions is claimed. The command record is
  complete for recorded commands. Earlier and auxiliary commands are reconstructed.
- **Model self-report.** The agent that made the determination reported its own model from its runtime context. It
  could not observe the model or the effort level independently.

## 10. Evidence bound by digest

The private records are not published. They contain local paths, host details and process identifiers, and they are
identified here by SHA256 only.

| Record | SHA256 |
|---|---|
| Private executability determination, revised after review, with every observation and its command reference | `2affa5eaa820851f26514d2f34fdd5178a4e7cfba74141e848a62c8621680df4` |
| Frozen digest list of the pre-run evidence: 30 command records with text, output, error and exit code, the probe scripts and outputs, and the recorder | `51d31f90d7e1d837e35189338972f9d0d48b2caac445014b4b192872a5b7a39e` |
| The W1 specification, unchanged | `92cdd0277316dec63992accd663fc9eba37662464f3e4217b459769158f22158` |
| The interpreter binary that the environment's `bin/python` resolves to | `bc56ea9cdc0fface1eb75712f871a454324f6cbfec4e30311b197f208a7f3d07` |
| The Stage 0 lock | `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8` |

This record cites no external source, and no source was retrieved for it. The software facts that the specification
cites, A1 to A11, are those of its own source ledger and are not restated here as observations.
