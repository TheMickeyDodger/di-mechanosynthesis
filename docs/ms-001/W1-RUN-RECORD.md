# W1 provenance wiring test: the one run, stopped under §8 condition S10

Date: 2026-10-04 (UTC−04:00). MS-001 scope option B. **Outcome: STOPPED under §8 condition S10. W1 ran once; the
one attempt is spent and is not repeated.**

W1 is the non-chemistry AiiDA wiring test specified in [C3-WIRING-TEST-PROPOSAL.md](C3-WIRING-TEST-PROPOSAL.md),
revision 01, SHA256 `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347`. This is a software wiring
observation only. It runs no chemistry engine, evaluates no energy, force or gradient, and no chemistry evidence class
applies to it. Its machine-readable outcome is [w1-run-outcome.json](w1-run-outcome.json).

**This record supersedes nothing.** The first pre-run determination ([record](W1-PRE-RUN-DETERMINATION.md);
[outcome](w1-outcome.json)) and determination 02 ([record](W1-PRE-RUN-DETERMINATION-02.md);
[outcome](w1-outcome-02.json)) keep their bytes. They describe the position before the run, under the specification
text in force when each was made. The specification, its [approval record](W1-REVISION-01-HUMAN-APPROVAL.md), every
other approval record and every frozen Stage 0 definition are unchanged.

**Authorization.** A person authorized one strict attempt of W1 and its possible early stop. That authorization is held
privately by the orchestration layer and covered this attempt only; it is spent. Before the launch, an independent
review approved the exact bytes of the two driver files, and the orchestration layer ran its own checks on them. That
approval and those checks are pre-run checks, not W1 evidence, and neither is readiness.

## 1. What ran

**The drivers, as run.** `tools/w1_driver.py`, SHA256
`ea3b7e40aec2e64373cde7002de0344d16d3624ebd3d33eff5d12b8470d35c3a` (214 951 bytes), and `tools/w1_job.py`, SHA256
`41622c64e074b2a23e404e6bc5a8f6ea2f31de55132a3b6736451c1b0ce9bc88` (28 290 bytes). The person's authorization for
this task covered writing them, and they are the authorized implementation. They are **published as run** at those
paths, entered with their SHA256 in the export manifest. They are untracked, as §2 of the specification permits, and
frozen: their bytes are exactly the bytes that ran. The run's own capture holds copies with the same SHA256, bound in
the post-stop retained-evidence inventory (Section 13). The drivers contain no local path, user name, host name,
credential or session identifier. Their one account string is a synthetic placeholder on the reserved `.invalid`
top-level domain, used as the profile's default user, and their work-area names are portable paths relative to the
repository.

**The launch.** The launcher started from the repository root as
`<environment>/bin/python -E -s -B tools/w1_driver.py launch`. It started the runner as a separate process with
exactly the five-variable environment of §5. The run began at 22:08:18 and ended at 22:08:31 (UTC−04:00). No
wall-clock ceiling was reached, and the runner was not interrupted.

**Background execution is established; session detachment is not.**
- **Background execution.** The launcher was started through the agent tool's background mode, as the retained launch
  command and the tool's response show. That is established.
- **Session detachment.** The launcher record notes `launcher_session` as a recorded detachment error: the
  launcher's call to `os.setsid()` raised `PermissionError`. Successful OS session detachment is therefore not
  established. The recorded error establishes only that this call raised. It does not establish whether the launcher
  already had a session of its own, since `os.setsid()` also raises in states that were not observed here, and it
  does not establish that the launcher was not detached.
- **No effect on the outcome.** The run's outcome, the empty list of operational events and every criterion and
  stop-condition state are as recorded (Sections 2, 6 and 7).

**The phases the run executed.** The run executed every phase it reached, and the records show each one:
1. the launcher record and the first user-level observation;
2. the interpreter record at the runner's start;
3. the first F3 build-identity reading and the host record;
4. the §4 capture, with its declared Git invocations, the copy of the `site-packages` superset and the project files,
   and all four listings;
5. the import of `w1_job`, the import of aiida-core, and the creation and loading of the W1 profile;
6. the module listing at the input point and its classification, **where S10 fired and the job sequence stopped**;
7. the run-end readings, which §8 retains after a stop: the second module listing and its classification, the
   interpreter record at the end, the second build-identity and host-record readings, the run-end §4 comparisons
   with their Git invocations and listings, and the check of the user-level AiiDA directory;
8. the second user-level observation, made by the launcher, and the result record.

Items 7 and 8 ran **after** the stop, as §8 requires the run-end readings to be retained. They are not credited toward
any criterion and establish no condition as not holding (Sections 6 and 7). What the stop ended was the **job
sequence**. None of the following ran (Section 5):
- no computer, code or input node was created;
- no submission script was written;
- there was no `presubmit` validation, upload, payload execution, retrieval or parsing;
- the F4 conversion sequence and the negative cases did not run;
- there was no three-way binding and no closure inventory.

## 2. The outcome

From the result record, format `w1-result-4`:

| Field | Value |
|---|---|
| Outcome | `STOPPED: Section 8 condition(s) S10` |
| Conditions fired | S10 only |
| First stop | S10 at the check `modules.input_point`, phase `input point`, sequence 7, not after another stop |
| Second stop | S10 at the check `modules.run_end`, phase `run end`, sequence 13, after the first stop |
| Phase reached by the runner | `input point`; it ended with "Section 8 stop: module classes at the input point" |
| Runner exit status | 1 |
| Interrupted | no |
| Operational events | none |
| Wall-clock ceiling | not reached |
| Source of the result | the runner's own result record. The durable journal held 39 entries with no error and no unreadable line; nothing was merged from it, nothing was reconstructed and no runner record was unusable |
| Criteria | criterion 5 unmet; criteria 1, 2, 3, 4, 6 and 7 not reached |
| Checks recorded as not reached, with reasons | 18 |
| `closure_inventory_sha256` | **null**. The driver produced no closure inventory, because no chain of jobs was built (Section 5). No value is substituted for it |

## 3. What fired S10

At the input point, after `w1_job` and aiida-core were imported and the W1 profile was loaded, and before any computer,
code, input node or job existed, the runner listed **1 690** entries of `sys.modules` and assigned each to one class of
§3, "The libraries actually used":

| Class | Entries |
|---|---|
| Environment packages | 1 385 |
| No file (built-in, frozen or namespace) | 93 |
| Standard library | 199 |
| Project | 2, exactly `tools/w1_driver.py` and `tools/w1_job.py` |
| **Unassigned** | **11** |

No entry was unestablished. An unassigned entry fits no declared class, and an unassigned entry fails its class
check (interpretation I-2 of the reviewed plan), which fires S10. The 11 entries, with the classifier's reason:

| Entry | Classifier's reason |
|---|---|
| `typing.io`, `typing.re` | a non-module object (`typing._DeprecatedType`) with no module file that is not built-in, frozen or a namespace module |
| `pyexpat.errors`, `pyexpat.model`, `xml.parsers.expat.errors`, `xml.parsers.expat.model` | a module with no module file that is not built-in, frozen or a namespace module |
| `_cython_3_1_4`, `_cython_3_2_9`, `_cython_3_2_9limited_fastcallnofinalize`, `_cython_3_3_0`, `cython_runtime` | a module with no module file that is not built-in, frozen or a namespace module |

The two `typing` entries were a known pre-run probe finding, disclosed in the reviewed plan before the run; no
exemption was made for them or for any other entry. The run-end classification lists the same 11 entries with the
same reasons, and its record is byte-identical to the input point's. No entry was first listed at the run end, so S14
did not fire. This record states the classifier's reasons only. Why these entries carry no module file is not
established here.

## 4. The four kinds of ending, kept apart

| Kind | In this run |
|---|---|
| §8 specification stops | S10 at `modules.input_point` (the first stop) and S10 at `modules.run_end` (after it). No other condition fired |
| §7 criterion failures | Criterion 5 is unmet: `modules.input_point` and `modules.run_end` failed |
| Not reached | Criteria 1, 2, 3, 4, 6 and 7. Every check after the input point's stop that needs a computer, code, input node or job was never made. Checks passed after the first stop are retained and **not credited** (Section 6) |
| Operational stops | None |

## 5. Created, absent, empty and not queried

These four states are kept apart throughout.

**Created.** The W1 AiiDA profile was created and loaded: name `w1`, storage backend `core.sqlite_dos`, no
process-control backend, under a new configuration directory in the project's git-ignored private area. Each item is
classified on what it is:
- The profile's UUID, the absolute path of the configuration directory, its access process-identifier file, the host
  name and the resolved interpreter path are private identifiers. They live in the private run records, not in the
  drivers, and they are not published.
- The default user's address is the synthetic placeholder on the reserved `.invalid` domain that the published driver
  declares. It identifies no person and no machine.

The configuration directory's listing holds 0 entries at the capture point and 9 at the run end; the increase is the
profile.

**Absent because never created.** The computer `w1-local-nologin`, the code `w1-bash`, the 17 input nodes and the two
CalcJob nodes `w1-job1` and `w1-job2` were never created. The stop was raised at the input point, before the code that
creates them. No record of any of them exists.

**Empty as observed.** After the run, the run's job work-directory area and its temporary directory each held 0
files. This is an observation of the filesystem.

**Not queried.** The number of nodes, CalcJob nodes or other objects in the profile's store was not queried. The check
`chain.calcjob_nodes` is among the 18 not-reached checks, so the driver made no such query, and none was made
afterwards. That number is unknown: no count is asserted, zero included, and none is inferred from the store's files.

**Steps never performed.** No submission script was written. There was no `presubmit` validation, no upload, no
payload execution, no retrieval and no parsing. The F4 conversion sequence and the negative cases were not run. There
was no three-way submission binding and no closure inventory. The capture was made before the stop. The run-end
readings and the second user-level observation **were** made after it, and they are not credited (Section 1).

**The empty code diff is not a verified F1 result.** The captured code diff is 0 bytes: the tracked diff was empty.
The check `fixture_diff` is the §4 guard against a vacuous pass on an empty diff, and it is among the 18 not-reached
checks. That guard was never exercised.

## 6. The seven acceptance criteria (§7)

Each criterion's checks fall into three groups:
- checks made **before the first stop**;
- checks made **after the first stop**, which are retained observations, recorded as such, and earn **no acceptance
  credit** toward any criterion;
- checks **never made**.

The states:
- **unmet**: a check of the criterion was made before any other stop had fired, and it failed;
- **not reached**: no check of the criterion failed before the first stop, and at least one was not made before it.
  A pass before the stop is recorded and does not make the criterion demonstrated. A pass after the stop earns no
  credit, and a failure after the stop remains recorded as an observation.

No criterion is demonstrated.

| # | Criterion (abridged) | State | Before the first stop | After the first stop (retained; no acceptance credit) | Never made |
|---|---|---|---|---|---|
| 1 | Two CalcJob nodes with exit status 0, process type `w1_job.W1Job`, required links, the chain | not reached | none | none | all eight: `finished_ok`, `process_type` and `links` of both jobs; `chain.calcjob_nodes`; `chain.job2_from_job1` |
| 2 | Every F4 check passes; every negative case fails | not reached | `capture.frozen_input` passed | none | `f4.sidecar_built`, `f4.T0`, `f4.S1`, `job1.f4`, `job2.f4`, `f4.sidecar_carriage`, `negative_cases` |
| 3 | The F1 items resolve as bytes, are inputs of both jobs, and every §4 comparison holds | not reached | `interpreter.dont_write_bytecode` and `capture.preconditions` passed | `runend.section4` held | `inputs.f1_equal_capture`, `f1.resolve_bytes`, `f1.inputs_of_both_jobs` |
| 4 | Launcher, interpreter and payload records; no-login setting; `presubmit` validation; three-way binding | not reached | `launcher.record` and `interpreter.record_start` passed | `interpreter.record_end` passed | the computer read-back and declared configuration; `presubmit`, binding, submission inventory, options and payload record of both jobs (12 checks) |
| 5 | Stored provenance inputs satisfy "Mandatory contents"; every module file passes its class check | **unmet** | `f3.first_reading` passed; **`modules.input_point` failed (S10, the first stop)** | `runend.build_identity` and `runend.host_record` passed; `modules.run_end` failed (S10) | the four mandatory-contents checks and the two input-manifest checks |
| 6 | Every repository object's key equals its SHA256 | not reached | none | none | `repository_keys` |
| 7 | Equal user-level observations; the fixture-diff check | not reached | `user_level.aiida_dir_after_import` passed | `user_level.aiida_dir_at_run_end` passed; `user_level`, the comparison of the two observations, found them equal | `fixture_diff` |

## 7. The fifteen stop conditions (§8)

Each condition's checks fall into the same three groups as in Section 6, by the audited mapping of checks to
conditions. The states:
- **fired**: it fired at a check made before any other stop. That check was the first stop.
- **did not fire before the stop; incomplete**: at least one check that can fire it was made before the first stop,
  and every such check passed. At least one other check that can fire it was made only after the stop, or never.
- **not evaluated before the stop**: no check that can fire it was made before the first stop. Checks made after the
  stop are listed as retained observations.
- **never evaluated**: no check that can fire it was made at all.

No state here says that a condition did not hold. "Never evaluated" is not "did not hold". A check made after the
first stop is a retained observation, recorded as such:
- it earns no acceptance credit toward any §7 criterion;
- a pass after the stop does not turn incomplete coverage of a condition into a finding that the condition did not
  hold;
- a failure observed after the stop remains recorded. The second S10, at the run-end module classification, is such
  a failure, and it is recorded as a fired condition.

No condition had every one of its checks made before the stop, so a state of "evaluated before the stop, did not
fire" applies to none.

| # | Stop condition (abridged) | State | Before the first stop | After the first stop (retained; no acceptance credit) | Never made |
|---|---|---|---|---|---|
| S01 | A user-level AiiDA directory appears, or the user-level observations differ | did not fire before the stop; incomplete | the directory check after the import passed | the run-end directory check passed; the two user-level observations were equal | none |
| S02 | The launcher or interpreter records break the §5 rule | did not fire before the stop; incomplete | the launcher record and the interpreter record at start passed | the interpreter record at end passed | none |
| S03 | `use_login_shell` reads back true | never evaluated | none | none | the computer read-back |
| S04 | `presubmit` raises, or the three copies of a submission file differ | never evaluated | none | none | `presubmit`, binding and job-end checks of both jobs |
| S05 | The process type differs from `w1_job.W1Job` | never evaluated | none | none | the process-type checks of both jobs |
| S06 | A §4 precondition fails, or a §4 comparison differs | did not fire before the stop; incomplete | the capture preconditions passed | the run-end §4 comparisons held | the input nodes against the capture |
| S07 | A required link is missing | never evaluated | none | none | the link checks of both jobs; the chain check |
| S08 | A job returns 310, 311 or 312 | never evaluated | none | none | the job-end checks of both jobs |
| S09 | A provenance input fails "Mandatory contents" | never evaluated | none | none | the four mandatory-contents checks |
| S10 | A declared §3 comparison fails (build identity, host record, payload record, loaded module file) | **fired** | the first build-identity reading passed; **the input-point module classification failed: the first stop** | the run-end build-identity and host-record readings passed; the run-end module classification failed again | the payload records of both jobs |
| S11 | A `distributions` entry fits no status | did not fire before the stop; incomplete | the first build-identity reading passed | the run-end build-identity reading passed | none |
| S12 | An F4 check fails | did not fire before the stop; incomplete | the frozen-input check passed | none | the sidecar, its two stages, the F4 checks of both jobs, the carriage check |
| S13 | A negative case passes | never evaluated | none | none | the negative cases |
| S14 | A project or outside-class module file is first listed at the run end | not evaluated before the stop | none | the run-end module classification found no entry first listed at the run end | none |
| S15 | The fixture diff fails its check | never evaluated | none | none | the fixture-diff check |

## 8. F1 to F11 coverage

The fields and their standing blockers are those of [C3 §5](C3-PROVENANCE-WIRING.md#5-coverage-table). The
dispositions:
- **demonstrated**: shown by this run's credited evidence;
- **unmet**: evaluated before the stop and failed;
- **blocked**: shown impossible as specified;
- **not reached**: not evaluated before the stop;
- **standing limit**: outside what W1 can establish.

No field is demonstrated, and no field is blocked.

| Field | What W1 carries | This run | Disposition | Residual blocker |
|---|---|---|---|---|
| F1 Code identity with full bytes | The captured diff, untracked files and `site-packages` superset as inputs of both jobs | The capture was made before the stop and is retained privately: a 0-byte code diff (the tracked diff was empty), three untracked files and an 18 448-file superset. The empty diff is **not** a verified F1 result: `fixture_diff`, the §4 guard against a vacuous pass on an empty diff, was never exercised. No input node was made. The §3 module-class requirement, checked on the module listings at the input point and the run end, is unmet (S10) | not reached | C3 blocker 2 (F1) stands |
| F2 Relied-upon defaults | The options and defaults recorded with each job | No job, computer or code | not reached | C3 blocker 2 (F2) stands |
| F3 Build identity and lock digest as inputs | The F3 build-identity input, compared at the run end | The first reading passed its checks before the stop: 89 distributions, 88 `locked-verified` and 1 `not-in-lock`; aiida-core 2.9.2, ASE 3.29.0 and NumPy 2.5.3 at their declared values; the lock digest as declared. No input node was made. The run-end reading equalled the first, after the stop, and is not credited. The §3 module-class requirement is unmet (S10) | not reached | C3 blocker 2 (F3) stands |
| F4 Identity-chain survival | The sidecar and its checks along the chain of two jobs | The frozen input matched its digest at the capture. No sidecar, conversion stage, job or negative case existed | not reached | C3 blocker 1 (F4) stands |
| F5 Drive bookkeeping | Labelled not-applicable fields of the inputs | No input node | not reached | C3 blocker 2 (F5) stands |
| F6 Seed as input | The seed input | No input node | not reached | C3 blocker 2 (F6) stands |
| F7 No login shell; declared environment | The computer's no-login setting read back; the launcher, interpreter and payload records | Before the stop, the launcher record and the interpreter record at start conformed: the five declared names, plus the platform-injected name that §5 permits in the interpreter record. The interpreter record at end conformed after the stop, not credited. No computer existed, so the no-login setting was never read back, and no payload ran | not reached | C3 blocker 3 (F7, D2) stands |
| F8 Units | The units input | No input node | not reached | C3 blocker 2 (F8) stands |
| F9 Failed-job preservation | Not established by W1 (§10) | No job existed, and none failed. This stop is the driver's, before any job, and is not an F9 demonstration | standing limit | Remains a dependency within Stage 1 |
| F10 Review record | Not held in AiiDA | Unchanged | standing limit | Remains with the orchestration layer |
| F11 Retained per claim | Labels only (§10) | No input node | not reached; standing limit on scientific validity | C3 blocker 2 (F11) stands |

## 9. Other observations of this run

These are software and environment observations of this project, retained in the run's private records. Each is
marked as made before or after the first stop. They are not conditions, and none is credited to a criterion beyond
what Section 6 states. Nothing made after the stop is credited.
- **§4 preconditions, before the stop.** All 14 preconditions held at the capture point. These include the bounded
  Git configuration, the index state, no `.gitattributes` on the listed paths, the untracked project files, no cached
  bytecode of the project files, and no symbolic link in `site-packages`. The untracked listing was exactly the two
  driver files and the local tool-settings file.
- **Run-end comparisons, after the stop and not credited.** Every comparison held:
  - the commit, Git version, configuration, exclude rules and index state;
  - the tracked and untracked files;
  - the code diff, byte for byte;
  - the `site-packages` and bytecode listings, field by field.

  The capture-time and run-end listings of `site-packages` (18 448 entries) and of the bytecode files (7 216 entries)
  are byte-identical.
- **Interpreter.** CPython 3.12.14 at the environment-relative `bin/python`, under `-E -s -B`, with bytecode writing
  disabled, read before the stop. The platform-injected name of §5 was present in the interpreter record at start,
  and in the record at end, after the stop. Its value is private.
- **Host record.** All four values were observed at the first reading, before the stop. The run-end reading equalled
  it, after the stop, not credited. Their values are private.
- **User-level observation.** All 11 paths were observable at the launcher's first observation and at its second,
  after the stop. The second equalled the first, a comparison made after the stop and not credited. The user-level
  AiiDA directory was absent at both instants.
- **The local tool-settings file**, which the capture includes, had the same SHA256 immediately before the launch and
  after the run. This is the implementing agent's observation outside the run's checks, not a W1 check.

## 10. What this establishes and what it does not

**Established**, as software observations of one run of this project, with no chemistry class:
- run as specified, W1 stops at the input point on module entries that fit no declared class, before creating any
  computer, code, input node or job;
- the stop, the retained run-end readings and the result record are as described in Sections 2 to 7.

**Not established.**
- That W1 can be executed to a pass. W1 did not pass, and no prediction is made.
- Any F1 to F8 or F11 carriage through a job chain, the no-login observation of F7, or any F4 identity check.
- F9. No job existed and none failed.
- That any stop condition did not hold. A pass made only after the stop, or no check at all, does not show that a
  condition did not hold (Section 7).
- That the empty code diff is a verified F1 result. Its guard, `fixture_diff`, was never exercised (Section 5).
- Why the 11 unassigned entries carry no module file.
- The number of objects in the profile's store (not queried).
- Anything about chemistry. This record is not readiness, parity, physical validation or authorization, and it
  upgrades no evidence label.

## 11. Effect on C3 and on the remaining boundaries

- **C3 blockers closed: none.** Identity-chain survival (F4), the remaining provenance extensions (F1, F2, F3, F5, F6,
  F8, F11) and the login-shell environment gap (F7, D2) all stand, as listed at the end of
  [C3 §5](C3-PROVENANCE-WIRING.md#5-coverage-table). C3 readiness remains **BLOCKED**.
- **F9** remains a dependency within Stage 1. **F10** remains with the orchestration layer. **F11** carries labels
  only.
- The authorization covered this one attempt only and is spent. W1 is not rerun, and nothing was repaired, adjusted,
  waived or exempted. An exemption of unclassifiable entries, or a revision of the specification, would need a
  person's decision. None is sought here.
- Basis normalization remains PARTIALLY ESTABLISHED, and Psi4 runtime conformance remains open. E-01 remains
  technically BLOCKED and scientifically INDETERMINATE. C4-j and B3-b remain deferred.
- **Stage 1 remains BLOCKED** and is not authorized. Stages 1a, 1b and 2 are not authorized. Scope option A remains
  **BLOCKED**.

## 12. Limits of this record

- **The pre-run checks are not W1 evidence.** The static verifier, the synthetic harness and the mutation check were
  run by the implementing agent and by the orchestration layer. With the repository checks, they ran on extracted
  copies of the driver functions with synthetic inputs and synthetic fixtures. Their coverage of the full phase
  routines, and of a real `SIGKILL`, was structural and call-site only. The run itself executed every phase it reached
  (Section 1). It needed no `SIGKILL`.
- **Process incidents during this task, retained and unresolved.** All are process matters, separate from §8 and
  giving no W1 or scientific evidence:
  - The orchestration layer's coordinating agent kept scratch outside this repository and ran a recursive deletion
    and a pattern-matched process termination there, of unestablished scope.
  - It appended to the reviewer's charter during an active review.
  - It wrote a fabricated digest whose original value is unrecoverable.
  - It made a stale parent binding, with a second hand-written digest; both values are retained.
  - It dispatched a packet containing one sentence that was false as written; the packet was not mutated.
  - The implementing agent deleted an undelivered draft result. It is not reconstructed and is excluded from
    established evidence.
  - After a guard refused one of its edit commands, the implementing agent wrote two helper scripts outside this
    repository and ran each once, as a workaround. This was not runtime logging, and why the guard matched is
    inferred, not established.
  - How many times two later helper scripts inside this repository were run cannot be settled by repository-local
    evidence. It remains open.
- **Model self-report.** Each agent's model is known from configuration and its own report. Neither is an
  attestation.
- **Confinement.** No complete filesystem confinement and no exhaustive audit of actions is claimed.

## 13. Evidence bound by digest

The run's records are private: they contain local paths, host details, process identifiers and private identifiers
of the profile. They are identified here by SHA256 only.

| Record | SHA256 |
|---|---|
| The post-stop retained-evidence inventory, version 02. It is **not** the §9 closure inventory and **not** a value for the null `closure_inventory_sha256`. It covers four categories: the bytes inventoried directly (the 52 run records, the captured diff, the lock and the three captured untracked files); the bytes bound through a listing (the `site-packages` superset, the bytecode files and the configuration directory); the mutable and runtime-owned files excluded, each with its reason; and the empty, not-queried and never-created states | `959d87ddc4687d843c50379d8aba0738da366c15c5deae09c082f3fb1e1059c0` |
| Its version 01, which listed the 52 run records only. Retained unchanged and superseded by version 02 as the inventory to bind | `a0d8fe6f485e1fde30de0ff19bcc2446e45ae34af41b830846406e4afa6876ad` |
| The result record (`closure_inventory_sha256` null) | `d7f0bb37088323abf2b8da6d2ca985f4ad0566b524e975df8da79ea10e5b844a` |
| The runner's own result record | `340f3fca5064eeaf2a89023b6929a9c5c0c316a8c837361fecaaac7e11113ae4` |
| The runner's durable journal, 39 entries | `6673ae619bea9702315f50c2ebd494b1057e8b3a198db425fcf45aaf507d259b` |
| The module classification at the input point, and the byte-identical one at the run end | `1779c111f6a2557848e36318cb2d049c2af274a7dea13e8d186fee7173ee31f5` |
| The `site-packages` listing, at the capture point and at the run end (identical) | `0934e6deb864c2aa9d56117486348ef183d85d00080d381d8fbde04d4032d497` |
| The bytecode listing, at the capture point and at the run end (identical) | `9cdbd1ded667ad803f5783a769bb6fe1ff951d21d37a062eb640faf804869a1a` |
| The interpreter binary that the environment's `bin/python` resolves to | `bc56ea9cdc0fface1eb75712f871a454324f6cbfec4e30311b197f208a7f3d07` |
| The captured lock file, equal to the declared lock digest | `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8` |
| The W1 specification in force, revision 01 | `29c71ff6d89d9f26bc1ef997ed80719d975f1f986226330e54a28af760b9a347` |

This record cites no external source, and no source was retrieved for it. The installed aiida-core 2.9.2 is the
distribution of entry [34] of the [sources catalogue](../SOURCES.md). This record is entry [44].
