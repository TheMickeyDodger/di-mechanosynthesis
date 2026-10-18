# H2-A-01 route-R2 run proposal (delta to the accepted Phase A proposal)

## 1. Status

**PROPOSED_NOT_AUTHORIZED.** This is a preparation-only `[AGENT]` proposal. It authorizes nothing and is not
readiness. It is a delta to the accepted [H2-A-01-RUN-PROPOSAL.md](../phase-a/H2-A-01-RUN-PROPOSAL.md) (SHA256
`d9bcb7e186a0ced226478d93470682c6ff84c78abab1f7546eb45bdac551225f`), which is unchanged, and it does not restate it.
It describes how job H2-A-01 would run if a person approved the method revision
[H2-R2-METHOD-REVISION.md](H2-R2-METHOD-REVISION.md). That approval is PENDING.

**Every launch is refused.**
- The route-R2 driver fails its check `r2.method_revision_decision` with `NETWORK_PREREQUISITE_UNRESOLVED` while
  `R2_METHOD_DECISION` is unset, and no field of an authorization file can satisfy that check.
- The accepted driver still fails `network.prerequisite` in the same way.

The steps that would lift the gate are listed in §10.

## 2. Files

| File | Role |
|---|---|
| [H2-R2-METHOD-REVISION.md](H2-R2-METHOD-REVISION.md) | The exact text a person would decide on |
| [h2_phase_a_r2_driver.py](h2_phase_a_r2_driver.py) | Route-R2 driver, standard library only. It composes the accepted driver's pinned bytes and adds the method-revision gate, the launch wrapper, the platform checks and the post-run observations |
| [h2-r2-sandbox.sb](h2-r2-sandbox.sb) | Sandbox profile, `[AGENT]`, machine-independent |
| [h2-r2-platform-identity.json](h2-r2-platform-identity.json) | Bound `sandbox-exec` digest and OS build |
| [tests/](tests/) | Fixture and fake-process tests, including real-sandbox tests around fake processes; no engine |
| [H2-A-R2-DECISION-PACKET.md](H2-A-R2-DECISION-PACKET.md) | What a person decides now, with bound digests |

## 3. What applies unchanged

The accepted proposal applies to route R2 unchanged, apart from six kinds of exception:
- the invocation of §4 here;
- the two N1 rows of its §5;
- its §8.5, replaced by §§5–8 here;
- its §8.6, which applies as extended by §8 here. Its final sentence, that the `sandbox-exec` write bound is not
  applied, is replaced for route R2 by §§5 and 8 here;
- its §9, which applies as extended by §9 here: code identity over eight paths, with the route-R2 authorization
  schema and its sixteen bound keys;
- the P5 row of its §11.

It applies unchanged in particular to:
- §3, settings and launch conditions: working directory, new session and process group, closed stdin, exclusive
  output files, allow-list environment and 300 s wall bound;
- §4, the environment;
- §5, the other stop tiers and FAILED precedence;
- §6, identity layers and ordering;
- §7, v1.11 source semantics;
- §8.1–8.4, §8.7 and §8.8, other limits;
- §9a, the driver's re-checks of the payload's records;
- §10, gaps;
- §12, gates.

The payload, input, static identity record, parameter file and accepted driver are executed or read as their
accepted bytes.

## 4. Changed invocation

There are three driver commands. The first two run no engine process:

```
python3 -I -B docs/learning/h2/phase-a-r2/h2_phase_a_r2_driver.py preflight --interpreter <PREFIX>/bin/python3.14 --prefix <PREFIX> --runs-root <RUNS_ROOT>
python3 -I -B docs/learning/h2/phase-a-r2/h2_phase_a_r2_driver.py code-provenance --out <PROVENANCE>
python3 -I -B docs/learning/h2/phase-a-r2/h2_phase_a_r2_driver.py run --interpreter <PREFIX>/bin/python3.14 --prefix <PREFIX> --runs-root <RUNS_ROOT> --authorization <AUTH>
```

`run` would spawn exactly:

```
/usr/bin/sandbox-exec -f <RUNS_ROOT>/H2-A-01/bundle/h2-r2-sandbox.sb -D H2_PAYLOAD_DIR=<RUNS_ROOT>/H2-A-01/payload -D H2_SCRATCH_DIR=<RUNS_ROOT>/H2-A-01/scratch <PREFIX>/bin/python3.14 -I -B <RUNS_ROOT>/H2-A-01/bundle/h2_phase_a_payload.py <RUNS_ROOT>/H2-A-01/bundle/h2-a-01-input.json <RUNS_ROOT>/H2-A-01
```

Everything after the `-D` options is the accepted engine command.

**Composition, not a copy.** The route-R2 driver pins the accepted driver's SHA256 `6dcb4845…9aa7d`. It reads
`../phase-a/h2_phase_a_driver.py` once as bytes and checks that digest. Only then does it execute exactly those bytes
into a fresh module object whose `__file__` is the accepted path. It reuses the accepted functions unchanged:
- the static preflight;
- input derivation;
- environment and command;
- `launch`, process-group cleanup, inventory and classification;
- the read-only Git functions.

On a digest mismatch or read failure it refuses (exit 2) without executing the bytes. It never sets the accepted
`NETWORK_OBSERVER`.

**Launch record.** The `command` field is the engine command, exactly as before, so the accepted P0 argv check and
the payload are unchanged. The record adds:
- `sandbox_wrapper`, `launched_argv` and `launched_shell_form`;
- the profile and platform identity digests;
- the observed `sandbox-exec` digest and OS version and build;
- `R2_METHOD_DECISION`.

The machine binding's `command` must equal `launched_shell_form`.

**Environment.** The environment is the allow-list of accepted §4, unchanged. In fixtures, fake processes started
through the wrapper saw the same environment names as unsandboxed controls:
- `LC_ALL`, `OMP_NUM_THREADS`, `PATH`, `PSI_SCRATCH` and `TMPDIR`;
- the declared platform name `__CF_USER_TEXT_ENCODING`.

So `sandbox-exec` added no name to a fake process [56]. This is not an observation of the engine interpreter, and E1
stays open.

## 5. The control

- **Profile.** `(version 1)`, `(allow default)`, `(deny network*)`, `(deny file-write*)`. It then allows
  `file-write*` only under `(subpath (param "H2_PAYLOAD_DIR"))` and `(subpath (param "H2_SCRATCH_DIR"))`, and for
  `(literal "/dev/null")`.
  - **Why `/dev/null`.** Without it, opening `/dev/null` for writing was refused. That made Python's
    `subprocess.DEVNULL` fail in a fixture, while writes there persist nothing [56]. Whether the engine needs it is
    unobserved.
  - **Missing parameters.** Without the `-D` parameters, `sandbox-exec` rejected the profile before the command
    started (exit 65) [56].
- **Write parameters.** The driver passes the attempt's canonical `payload/` and `scratch/` paths. The attempt root,
  `bundle/`, `launch-record.json`, `code-provenance.json`, the runs root, the prefix and the repository are therefore
  outside the write allowance.
- **Bound copy.** The profile is copied into `<attempt>/bundle/` by exclusive creation, and its digest is checked
  against the authorization, as for the payload and input.
- **Platform checks.** Before launch, immediately before spawn and after the process ends, the driver checks
  `/usr/bin/sandbox-exec` (regular file, not a link, executable, size and SHA256) and the OS `ProductVersion` and
  `ProductBuildVersion` against [h2-r2-platform-identity.json](h2-r2-platform-identity.json). The OS version is read
  from `SystemVersion.plist` with `plistlib`.
- **Method-revision gate.** The check `r2.method_revision_decision` replaces the accepted check
  `network.prerequisite`, which is kept verbatim in each report under `replaced_base_checks`. Every other accepted
  check is kept and must pass.

## 6. Prevention, observation and detection

| What | Kind | Result | Basis |
|---|---|---|---|
| AF_UNIX connect and bind; TCP connect and UDP send to `127.0.0.1`, by the process and its descendants | Prevention (refusal, EPERM) | Operation fails in the process; no driver detection or event record | Fixture-observed [56] |
| File creation or append outside `payload/` and `scratch/` (existing and new prefix files, new `conda-meta` record, attempt root, `bundle/`, runs root, repository tree) | Prevention (refusal, EPERM) | Operation fails in the process; no driver detection or event record | Fixture-observed [56] |
| Bound prefix files, `conda-meta/` names and bound package records, bundle and route-R2 files, `sandbox-exec`, OS build | Observation at three instants | BLOCK_LAUNCH before spawn; after the end, a reason added to the accepted classification | Driver checks; tests |
| Entries in the attempt root or `bundle/` that the driver did not create; attempt copies of payload, input, profile, code provenance and launch record | Observation after the end | A reason added to the accepted classification | Driver checks; tests |
| A refused attempt | Detection | **None** | — |
| A refusal that makes the engine fail | Existing stop conditions, unchanged | FAILED (nonzero exit other than a valid payload stop, signal, timeout, energy failure) or STOP_BEFORE_ENERGY (valid payload stop) | Fixture: a fake whose prefix write was refused exited 1 and was FAILED [56] |

Both kinds of observation report state at instants. Neither detects attempts. No system log is read. The engine's
stdout, stderr and output files are kept and inventoried but not analysed for refusals, and their silence does not
show that no attempt was made.

**How post-run reasons are classified.** The reasons are added to the accepted classification, which is applied
unchanged:
- every reason is kept;
- the tier is FAILED whenever the accepted rules give FAILED, which takes precedence;
- a valid payload stop stays STOP_BEFORE_ENERGY;
- otherwise the tier is QUARANTINE.

Item 3 of R2-S in the method revision lists exactly which post-run checks and observations add a reason. The
runs-root, attempt and free-space checks are kept in the outcome but add none.

## 7. Inheritance

- **Source.** sandbox(7) states that new processes inherit the sandbox of their parent [55].
- **Fixtures.** Refusals were observed in four kinds of process [56]:
  - the launched process;
  - its child;
  - a grandchild in the same process group;
  - a grandchild that left the session and process group with `setsid`.
- **Nested sandbox.** A nested `sandbox-exec -p '(version 1)(allow default)'` started inside the sandbox exited 71
  with `sandbox_apply: Operation not permitted`, and its command did not run. The process that tried it was still
  refused afterwards. This is recorded as observed.
- **Process groups.** The accepted §8.4 limit is unchanged: a process that leaves the process group escapes the
  group signals of the wall-clock bound, although it stays sandboxed.

## 8. Write, installation and compared-set coverage

**Prevented, for the tested operations:** writes and file creation outside `payload/` and `scratch/`. This includes
bytecode caches and package files in `<PREFIX>`, a new `conda-meta` record, and anything in the attempt root,
`bundle/`, the runs root or the repository.

**Not prevented:**
- writes and local installation inside `payload/` and `scratch/`;
- activity in memory, including downloads held in memory;
- operations outside the profile's `file-write*` and `network*` classes as fixture-observed;
- use of descriptors opened before the sandbox: stdin, stdout and stderr are opened by the driver, as sandbox(7)
  allows;
- traffic sent by system services on the process's behalf, which was not tested. No claim is made about any specific
  service;
- the behaviour, under the profile, of import-time and native side effects of the engine, which now occur inside the
  sandbox. This is unobserved.

**Compared set.** It is the accepted §8.6 set plus:
- the route-R2 files;
- the `sandbox-exec` digest and OS build;
- the attempt-root and `bundle/` entries;
- the attempt copies.

The accepted gaps remain: other package records' contents, other prefix files, anything outside the prefix and bundle
that the profile does not protect, in-memory downloads, and changes reverted between samples.

## 9. Provenance and authorization bindings

**Code provenance.** The driver's `code-provenance` mode writes a record over eight paths, with the accepted read-only
Git functions:
- the route-R2 driver and the accepted driver;
- the payload, input, parameter file and static identity record;
- the profile and the platform identity record.

`run` re-derives the record before launch and blocks when it is absent, mismatched, stale or unresolvable. The record
is preserved in the attempt.

**Authorization.** The schema is `di-mechanosynthesis/h2-phase-a-r2-authorization/1`, with sixteen `bound_sha256`
keys:
- the seven accepted bundle keys (the accepted bytes);
- `r2_driver`, `r2_profile`, `r2_platform_identity`, `r2_method_revision`, `r2_run_proposal` and
  `r2_decision_packet`;
- `machine_binding`, `code_provenance` and `method_revision_approval`.

When `R2_METHOD_DECISION` is set, `r2_method_revision` and `method_revision_approval` must equal its values. Every
accepted interlock rule carries over:
- one job, with `max_attempts` 1;
- the exact environment;
- the static digests;
- the interpreter, prefix and runs root equal to the machine binding.

The check compares bytes and fields only. It cannot show that a person authorized anything.

## 10. Test evidence and remaining gates

**Tests** [56]. The route-R2 suite ([tests/](tests/)) has 28 tests, which pass. The accepted Phase A suite (37 tests)
passes unchanged. The route-R2 suite covers:
- the shipped refusal, and the rejection of the decision packet's template;
- the pin, with proof that altered accepted bytes were not executed;
- each binding negative, with nothing spawned;
- a structured refusal, before any attempt exists, for a wrong-shaped `SystemVersion.plist` and for an unexpected
  preflight error;
- real-sandbox prevention against unsandboxed controls;
- the preserved accepted behaviours through the wrapper: completion, no relaunch, process-group timeout, leftover
  member, a prefix change made outside the sandbox, the iteration limit with both reasons, a malformed record, a stop
  before energy;
- the post-run observations;
- code-provenance coverage;
- the absence of repository writes, bytecode and leftover processes.

A private mutation check killed each of eighteen targeted defects with its intended assertion. Two earlier mutants
that did not model their defect faithfully are kept and labelled invalid. Fake outputs are not chemistry evidence.

**Remaining gates, in order:**
1. A person's decision on the method revision (PENDING).
2. A human approval record.
3. A separately reviewed driver revision that sets `R2_METHOD_DECISION`.
4. A separate, bounded human run authorization.

**Unchanged and open:**
- M1 (engine memory is not an operating-system limit);
- E1 (the engine interpreter's environment is unobserved);
- the Libint load-name risk;
- loaded identity;
- P4 (the meaning of the reported total energy);
- source-to-binary correspondence;
- the engine's compatibility with the profile.

**P5.** It would read as in R2-S and R2-P5 of the method revision for this job only. Phase B remains separately
gated.

**Other gates.** W1 is STOPPED (S10). E-01 is technically BLOCKED and scientifically INDETERMINATE. C3 readiness,
MS-001 Stage 1 and option A are BLOCKED.

Sources: [../../../SOURCES.md](../../../SOURCES.md) entries [55] and [56].
