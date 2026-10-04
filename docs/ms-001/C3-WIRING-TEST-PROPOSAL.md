# C3 wiring test W1: proposed specification

Date: 2026-09-27. MS-001 scope option B, before Stage 1. Status: **PROPOSAL. Specification only. Nothing here has
been run, installed, registered or imported, and running it needs its own authorization.**

**Revision 01 (proposed 2026-10-04).** This text revises the specification of 2026-09-27 for the two blockers and the
unresolved requirement recorded by the [W1 pre-run determination](W1-PRE-RUN-DETERMINATION.md), W1-BLOCKER-E2,
W1-BLOCKER-E1 and U-F1P, and for seven gaps coupled to them. The options, reasons and rejected alternatives are in the
[revision decision packet](W1-REVISION-DECISION-PACKET.md). This revision is in force only after a person has approved
these exact bytes and the approval is recorded; until then the specification of 2026-09-27 is in force. Neither the
approval nor this revision authorizes a run of W1.

This record specifies the smallest future non-chemistry AiiDA wiring test, W1, that could close the C3 blockers
listed at the end of [C3 §5](C3-PROVENANCE-WIRING.md#5-coverage-table):
- identity-chain survival (F4);
- the remaining provenance extensions F1, F2, F3, F5, F6, F8 and F11;
- the login-shell environment requirement (F7, deviation D2).

W1 runs no chemistry engine and evaluates no energy, force or gradient. A pass would be software wiring evidence
only, as C3's trivial job was. Every value below is a declaration for a future run. None is an observation.

What W1 cannot establish, stated before its design:
- **F9.** It does not establish preservation of a failed engine job. That remains a dependency within Stage 1.
- **F10.** Review stays with the orchestration layer.
- **F11.** It establishes no validity of any scientific claim. It carries the F11 record with labels only.
- **F7 until observed.** The source facts below do not show that no login shell runs on the host. F7 stays unmet
  until an authorized W1 run observes it, and even then only the no-login setting and the declared environment are
  covered. W1 establishes no hardware property (Section 5).
- **F3 beyond its checks.** The lock digest establishes the lock file's bytes, not that the running environment
  corresponds to it. W1 tests that correspondence only per distribution, only where a retained wheel allows it, and
  only for files a wheel's `RECORD` lists with a hash. Cached bytecode is observed only: its correspondence to the
  wheel or to the source is not established, and Section 4 checks only that it does not change during the run. W1
  does not establish the origin of the interpreter or of the shell (Section 3).
- **F1 beyond its capture.** The capture of Section 4 retains the bytes of the project's files and of every file of
  the environment's `site-packages`, and two module listings record which of them the loaded modules name. Both are
  file inventories. They do not establish which code the interpreter executed.
- **The declared environment, as relaxed.** The interpreter and the payload may hold one platform-injected name
  beyond the five declared variables. It is recorded where it appears and is never part of the launcher's environment
  (Section 5).
- **No authorization.** Nothing here authorizes Stage 1, a calculation or an installation.

## 1. Sources

The design rests on aiida-core 2.9.2 source, read from the retained wheel of the Stage 0 hash-locked installation
(SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`, C3 §1). Member digests are in the
[pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md), and that of the member first cited by A12 is in the
[revision decision packet](W1-REVISION-DECISION-PACKET.md). Each statement reports what that source text defines.

| # | Fact | Locator (aiida-core 2.9.2) |
|---|---|---|
| A1 | The transport's login-shell setting defaults to true and selects `bash -l `; when false it selects `bash ` | `aiida/transports/transport.py` 114–124 |
| A2 | The local transport runs each command as that string with `-c`, through `subprocess.Popen` with `shell=True` and no explicit environment. The parent process's environment therefore reaches the outer system shell and the inner Bash | `aiida/transports/plugins/local.py` 770–791 |
| A3 | The direct scheduler submits a job as `(bash <script> > /dev/null 2>&1 & echo $!) &`. The script's shebang does not decide how it is invoked. Its script header contains output redirections, the optional `env --ignore-environment \` line, custom commands and an optional `OMP_NUM_THREADS` export, and no job name | `aiida/schedulers/plugins/direct.py` 126–174, 192–206 |
| A4 | The `env --ignore-environment \` line is written only when `import_sys_environment` is false. It is followed by custom scheduler commands, the optional export and an empty line | `aiida/schedulers/plugins/direct.py` 160–174 |
| A5 | The submission script is assembled in this order: shebang (`#!/bin/bash` when none is set), scheduler header, environment variables, prepend text, run line, append text | `aiida/schedulers/scheduler.py` 205–244 |
| A6 | `import_sys_environment` defaults to true. `environment_variables`, `prepend_text` and `metadata.dry_run` are options. The submission script's file name, `submit_script_filename`, defaults to `_aiidasubmit.sh`. The scheduler's output and error files default to `_scheduler-stdout.txt` and `_scheduler-stderr.txt`, and both are added to the retrieve list | `aiida/engine/processes/calcjobs/calcjob.py` 295–300, 320–324, 326–337, 398–432, 982–990 |
| A7 | A `parser_name` option must resolve through the plugin factory, that is through a registered entry point. `CalcJob.parse` calls `parse_retrieved_output`, uses its exit code when it returns one, and by default uses that parser | `aiida/engine/processes/calcjobs/calcjob.py` 211–223, 440–446, 775–823, 903–930 |
| A8 | The job-preparation record carries the node's UUID, and the job name carries its primary key | `aiida/engine/processes/calcjobs/calcjob.py` 965, 972 |
| A9 | A process's type is the registered entry-point string when one exists for its module and class. Otherwise it is the fully qualified `module.ClassName` | `aiida/engine/processes/process.py` 619–640 |
| A10 | A dry run constructs a default `LocalTransport()` directly, not the transport configured for the job's computer, and it still calls the upload step with that transport | `aiida/engine/processes/calcjobs/calcjob.py` 725–745 |
| A11 | In a real run the upload task requests the transport of the job's computer and authorization, calls `presubmit` to write the job folder, including the submission script, and only then uploads. An exception in `presubmit` is raised as a pre-submit failure, with no upload and no retry | `aiida/engine/processes/calcjobs/tasks.py` 84–111 |
| A12 | Importing the configuration-settings module calls `AiiDAConfigDir.set()`, which creates the configuration directory and its daemon, daemon-log, broker, log and access-control subdirectories. The directory comes from `AIIDA_PATH` when that variable is set, with `.aiida` appended unless the path already ends in it, and is otherwise `~/.aiida`. The default `~/.aiida` path is computed at import even when `AIIDA_PATH` is set | `aiida/manage/configuration/settings.py` 20–30, 35–60, 97–129, 132–168, 171–172 |
| A13 | Opening the local transport sets its internal directory to `os.path.expanduser('~')` | `aiida/transports/plugins/local.py` 58–70 |

*Project inferences:*
- **A4.** With no custom commands and no export, the `env --ignore-environment \` line continues onto an empty line.
  It then runs `env` on its own and does not change the payload's environment. W1 therefore keeps
  `import_sys_environment` at true and cleans the environment at the parent instead (Section 5).
- **A7.** A subclass that overrides `parse_retrieved_output` attaches its outputs without a registered parser.
- **A9.** An unregistered class is persisted with type `module.ClassName`. Loading the stored node later needs that
  module to be importable. A registered entry point with the same module and class would take precedence. The
  parser override does not settle how the process class is persisted or loaded; those are separate mechanisms.
- **A10.** By A1, that default transport has the login-shell setting true. A dry run therefore neither avoids a
  transport nor uses the configured no-login computer, and W1 does not use one.
- **A12, A13.** Without `HOME`, AiiDA still computes paths from `~`. How the interpreter expands `~` when `HOME` is
  absent is not defined by this source and was not observed. W1 sets `AIIDA_PATH` and observes user-level paths
  before and after the run (Section 5).

## 2. Declared setup

| Item | Declaration |
|---|---|
| Python environment | The existing Stage 0 project-local environment: CPython 3.12.14, aiida-core 2.9.2, ASE 3.29.0, lock SHA256 `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8` (C3 §1). Nothing is installed |
| Profile and storage | A new AiiDA profile dedicated to W1, with `core.sqlite_dos` storage and no message broker, under a new project-local configuration directory in the git-ignored project area. The Stage 0 profile is not reused, so the W1 store holds only W1's nodes. The profile is created only under the future authorization |
| Computer | A new Computer labelled `w1-local-nologin`: transport `core.local` with `use_login_shell` false, scheduler `core.direct`, shebang `#!/bin/bash`, and its work directory inside the same project-local area |
| Code | An installed code labelled `w1-bash` on that computer, executable `/bin/bash`, command-line argument `w1_payload.sh` |
| Runner | In-process `run_get_node` of aiida-core in one interpreter, with no daemon. The interpreter is the Stage 0 environment's own, invoked by its exact resolved path, which is recorded privately and written publicly as the environment-relative `bin/python`. Its version must read back as CPython 3.12.14. It is never found through `PATH`: under the clean `PATH` of Section 5, a bare `python` would not select that environment. The driver runs as two processes. The **launcher** is started by the operator as `<environment>/bin/python -E -s -B tools/w1_driver.py launch` from the repository root. It imports nothing outside the standard library, makes the launcher record and the first user-level observation of Section 5, starts the runner, waits for it to end and makes the second user-level observation. The **runner** is started by the launcher as `<environment>/bin/python -E -s -B tools/w1_driver.py run`, from an argument vector without a shell, with the repository root as working directory and with an environment that is exactly the launcher record. Before it imports anything outside the standard library, the runner makes the interpreter record of Section 5, records the F3 build identity and the host record of Section 3 and makes their checks. The lock digest check establishes the lock file's bytes only; whether the installed environment corresponds to the lock is tested separately, per distribution (Section 3). `-B` is the bytecode policy of Section 4. `-I` is not used, because it would drop the driver's directory from the import path |
| Class and module | Class `W1Job` in the module file `tools/w1_job.py`. The driver puts `tools/` first on the import path and imports `w1_job`. The recorded process type must equal `w1_job.W1Job` (A9); any other value, such as one caused by an entry point of the same name, stops W1. Both files are untracked at the declared commit and are not required to be tracked at any commit. Section 4 captures their bytes, with their SHA256 and Git blob identifiers, and those bytes are inputs of each job |
| Frozen input | `structures/donor-activated-EAOGe-C2-radical.extxyz`, SHA256 `bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3`, 48 atoms, with per-atom `atom_id`, `map_num` and `radical_electrons` |
| Fixed-set fixture | The six atoms `D-O1`, `D-O2`, `D-O3`, `D-O1-H1`, `D-O2-H1` and `D-O3-H1`, the tool handle of B3 §1. It is labelled a wiring fixture, not a scientific constraint |

## 3. Node boundary: the W1 CalcJob class

**The defect W1 must not repeat.** In C3 the trivial job ran stock `core.arithmetic.add` with only `x`, `y` and
`code` as inputs. The structure, identity and file nodes were stored beside it (C3 §4). W1 makes every node a real,
required input port of **each** of the two jobs:

| Port | Node type | Written into the job folder as | Field |
|---|---|---|---|
| `structure` | `StructureData` | `w1_structure_in.extxyz` | F4 |
| `identity` | `SinglefileData` | `w1_identity.json` | F4 |
| `fixed_set` | `List` | `w1_fixed_set.json` | F4 |
| `units` | `Dict` | `w1_units.json` | F4, F8 |
| `code_diff` | `SinglefileData` | `w1_inputs/code_diff.bin` | F1 |
| `code_untracked` | `FolderData` | `w1_inputs/code_untracked/` | F1 |
| `code_private` | `FolderData` | `w1_inputs/code_private/` | F1 |
| `code_identity` | `Dict` | `w1_inputs/code_identity.json` | F1 |
| `fixture_diff` | `SinglefileData` | `w1_inputs/fixture_diff.patch` | F1 |
| `defaults` | `Dict` | `w1_inputs/defaults.json` | F2 |
| `build_identity` | `Dict` | `w1_inputs/build_identity.json` | F3 |
| `lock` | `SinglefileData` | `w1_inputs/lock.txt` | F3 |
| `host_record` | `Dict` | `w1_inputs/host_record.json` | F7 |
| `calc_performed` | `Dict` | `w1_inputs/calc_performed.json` | F5 |
| `seed` | `Str` | `w1_inputs/seed.txt` | F6 |
| `per_claim` | `Dict` | `w1_inputs/per_claim.json` | F11 |
| `env_policy` | `Dict` | `w1_inputs/env_policy.json` | F7 |

**Mandatory contents of the provenance inputs.** Every key listed below is required, and no other key is allowed.
Each value is one of three kinds:
- an exact declared string;
- a member of a finite declared set;
- where marked *recorded*, a value read during the run. Its exact source and the exact comparison made against it
  are declared in the tables that follow this one, under "The F3 build identity", "The F7 host record" and "The
  payload record", and for `code_identity` under "The F1 code identity" (Section 4). A *recorded* value with no
  declared source and comparison is not allowed.

Where a value's kind depends on a condition, the table states the condition, and the value must be of the kind that
its condition selects.

N/A below stands for the exact string `not applicable: non-chemistry wiring test`. These labels record only that a
field was carried. They are not settings of a model chemistry, and they must never be read as an executed
calculation or as a physical claim.

| Port | Required keys and values |
|---|---|
| `defaults` (F2) | One entry per setting W1 relies on. Each entry is `{value, kind, defined_by}`: `kind` is `explicit` or `default relied upon`, and `defined_by` names the package, its version, the file and the lines. The entries are: `transport` (`core.local`, `use_login_shell` false, explicit, whose default is true by A1); `scheduler` (`core.direct`, with its submit-command form by A3); `shebang` (`#!/bin/bash`); `import_sys_environment` (true, default relied upon, with the reason in A4); `environment_variables` (`{"OMP_NUM_THREADS": "1"}`, explicit); `resources` (as in "Other settings", explicit); `withmpi` (false, explicit); `prepend_text`, `append_text` and `custom_scheduler_commands` (empty, explicit); `submit_script_filename` (`_aiidasubmit.sh`), `scheduler_stdout` (`_scheduler-stdout.txt`) and `scheduler_stderr` (`_scheduler-stderr.txt`), each a default relied upon (A6). No engine default is relied upon, so the key `engine_defaults` holds N/A |
| `build_identity` (F3) | Exactly the keys `python`, `distributions`, `aiida_core`, `ase`, `numpy`, `lock_sha256`, `bash`, `operating_system`, `engine`, `engine_banner` and `engine_build_identity`, with the values, sources and comparisons of "The F3 build identity" below. `engine`, `engine_banner` and `engine_build_identity` are each N/A |
| `host_record` (F7) | Exactly the keys `host_name`, `cpu_model`, `logical_cpu_count` and `memory_bytes`, with the values, sources and statuses of "The F7 host record" below |
| `calc_performed` (F5) | One key for every frozen F5 field: `method_and_levels`, `partition_embedding_and_links`, `charge`, `multiplicity`, `optimizer_and_settings`, `drive_branch`, `step_index` and `imposed_z`, each N/A. `constraints`: `{"fixed_set_fixture": ["D-O1", "D-O2", "D-O3", "D-O1-H1", "D-O2-H1", "D-O3-H1"], "label": "synthetic wiring fixture; not a scientific constraint"}`. `record_label`: `software wiring test; no model chemistry was executed` |
| `seed` (F6) | Exactly `none` |
| `units` (F4, F8) | `positions`: `angstrom`. `cell`: `angstrom; the structure is non-periodic`. `extracted_quantities`: `{"atom_count": "dimensionless count", "digests": "not applicable: identifiers, not quantities"}`. `energy`, `forces` and `gradient`: each `not applicable: none extracted` |
| `per_claim` (F11) | One key for every frozen F11 field: `units` (`see the units input of this job`); `atom_identity` (`see the identity and fixed_set inputs of this job`); `charge_and_spin` (N/A); `constraints` (`synthetic fixed-set fixture only; not a scientific constraint`); `environment` (`see the env_policy, build_identity and host_record inputs of this job`); `tool_state` (`not applicable: the frozen donor file is carried only as an identity fixture; no claim about the tool's state is made`); `evidence_class` (`software wiring test; not chemistry evidence; no chemistry evidence class applies`). `claim`: `none` |
| `env_policy` (F7) | `allow_list`: exactly the five variables of Section 5. `platform_injected`: exactly `["__CF_USER_TEXT_ENCODING"]`. `platform_injected_scope`: exactly `interpreter and payload records only; never the launcher record`. `absent`: `["BASH_ENV", "ENV", "HOME"]`. `use_login_shell`: false. `import_sys_environment`: true. `shell`: `/bin/bash` |
| `code_identity` (F1) | Exactly the keys of "The F1 code identity" (Section 4), with the values, sources and comparisons declared there |

**The F3 build identity.** The runner reads every value below before job 1, under the Section 5 environment, and
before it imports anything outside the standard library. It reads the same sources again after job 2, into the
run-end record of Section 9. "At run end" below means equality with that second reading.

| Key | Value | Source | Comparison made by the checker |
|---|---|---|---|
| `python.implementation`, `python.version` | Exactly `CPython` and `3.12.14` | `platform.python_implementation()` and `platform.python_version()` in the runner | Equal to the declared strings, and at run end |
| `python.build` | *recorded* | `platform.python_build()` and `platform.python_compiler()` | Equal at run end |
| `python.executable` | Exactly `bin/python` | `sys.executable`, written relative to `sys.prefix`. The resolved path is recorded privately | `sys.executable` equals `sys.prefix` joined with `bin/python`, and `sys.prefix` is the declared environment |
| `python.interpreter_sha256` | *recorded* | The SHA256 of the file at `os.path.realpath(sys.executable)`: the interpreter binary that the environment's `bin/python` resolves to | Equal at run end |
| `distributions` | One entry per distribution installed in the environment's `site-packages`, as enumerated by `importlib.metadata`. Each entry holds `name`, `version`, `in_lock`, `status`, `lock_hashes`, `wheel_sha256`, `wheel_record_match` and `installed_record_sha256` | The rows below | The rows below, subject to the applicability rule that follows the table |
| `distributions[*].name`, `.version` | *recorded* | The `Name` and `Version` fields of the installed `METADATA` | `in_lock` is true exactly when the normalized name and the version match one entry of the stored `lock` input |
| `distributions[*].status` | Exactly one of `locked-verified`, `locked-wheel-unavailable` and `not-in-lock` | Assigned by the applicability rule below | The entry's other fields satisfy that status as the rule defines it |
| `distributions[*].lock_hashes` | When `in_lock` is true, *recorded*. When `in_lock` is false, exactly the empty list | Every `--hash=sha256:` value of the matching lock entry | When `in_lock` is true: equal to the list the checker recomputes from the bytes of the stored `lock` input, and not empty. When `in_lock` is false, there is no lock entry to compare with: the checker confirms only that no entry matches |
| `distributions[*].wheel_sha256` | When `in_lock` is true and a retained Stage 0 wheel file exists for that name and version: *recorded*. When `in_lock` is true and none exists: exactly `not available`. When `in_lock` is false: exactly `not applicable: not in lock` | The SHA256 of that wheel file, whose location is recorded privately | Only when the value is *recorded*: it is a member of `lock_hashes`. The other two values are recorded, not tested |
| `distributions[*].wheel_record_match` | When `wheel_sha256` is *recorded*: exactly `true`. When it is `not available`: exactly `not established`. When `in_lock` is false: exactly `not applicable: not in lock` | The wheel's own `*.dist-info/RECORD` member, read from the archive without extraction. For every file it lists with a non-empty hash, other than a bytecode cache file or a `.data/scripts/` file, the SHA256 of the installed file at its installed path under the wheel-path rule below | Only when `wheel_sha256` is *recorded*: every such file exists and matches. A mismatch or a missing file is listed and stops W1. The other two values are recorded, not tested |
| `distributions[*].installed_record_sha256` | *recorded*, for entries of every status | The SHA256 of the installed `RECORD` file | For entries of every status: each entry of that installed `RECORD` that has a non-empty hash and is not a bytecode cache file matches its file. Entries with an empty hash field, and bytecode cache entries, are listed and not compared. The digest is equal at run end |
| `aiida_core` | Exactly `2.9.2`, wheel SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd` | The `distributions` entry of that name | Its `status` is `locked-verified`, and its version and `wheel_sha256` equal the declared strings. Any other status stops W1 |
| `ase` | Exactly `3.29.0`, wheel SHA256 `7b9dd103f007810339c24acfee2f6b677c0c48443b21d3c98e52959246cf4ebf` | The `distributions` entry of that name | As for `aiida_core` |
| `numpy` | Exactly `2.5.3`. Its wheel SHA256 is *recorded*: no public record states it, so it is checked by membership in `lock_hashes`, not against a declared string | The `distributions` entry of that name | Its `status` is `locked-verified`, which requires the recorded `wheel_sha256` to be a member of `lock_hashes` and `wheel_record_match` to be true. Its version equals the declared string. Any other status, `locked-wheel-unavailable` included, stops W1 |
| `lock_sha256` | Exactly `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8` | The SHA256 of the stored `lock` input's bytes | Equal to the declared string |
| `bash.path` | Exactly `/bin/bash` | Declared | Equal to the payload record's `bash_path` in each job |
| `bash.version` | *recorded* | The standard output of `/bin/bash --noprofile --norc -c 'printf %s "$BASH_VERSION"'`, run by the runner from an argument vector, without a shell, under the Section 5 environment | Exactly equal to the payload record's `bash_version` in each job |
| `bash.sha256` | *recorded* | The SHA256 of the file `/bin/bash` | Equal at run end |
| `operating_system.sysname`, `.release`, `.version`, `.machine` | *recorded* | The four fields of `os.uname()` in the runner | `sysname`, `release` and `machine` exactly equal to the payload record's `uname_s`, `uname_r` and `uname_m` in each job. All four equal at run end |
| `operating_system.product_name`, `.product_version`, `.product_build`, `.plist_sha256` | *recorded* | The keys `ProductName`, `ProductVersion` and `ProductBuildVersion` of `/System/Library/CoreServices/SystemVersion.plist`, read with `plistlib`, and that file's SHA256 | Equal at run end |

**The applicability rule for `distributions`.** Every entry has exactly one status. Each comparison of the table
applies only where the status says so. A permitted case in which a comparison does not apply is recorded as that
status, not tested and not failed.
- **`locked-verified`.** `in_lock` is true, `lock_hashes` is not empty, and `wheel_sha256` is *recorded* and a member
  of `lock_hashes`. `wheel_record_match` is true.
- **`locked-wheel-unavailable`.** `in_lock` is true, `lock_hashes` is not empty, `wheel_sha256` is `not available`
  and `wheel_record_match` is `not established`. No membership test and no wheel comparison is made.
- **`not-in-lock`.** `in_lock` is false. `lock_hashes` is the empty list. `wheel_sha256` and `wheel_record_match` are
  each `not applicable: not in lock`. No lock or wheel comparison is made.

The installed-`RECORD` check applies to entries of every status. An entry that fits none of the three statuses stops
W1. Examples are a recorded wheel digest outside `lock_hashes`, a failed wheel comparison, and an in-lock entry with
no hash.

**Definitions.**
- **Bytecode cache file.** A file with the suffix `.pyc` inside a `__pycache__` directory.
- **The wheel-path rule.** A path in a wheel's `RECORD` is compared with the installed file at the same path relative
  to `site-packages`, except under the wheel's `<name>-<version>.data/` directory. There, `purelib` and `platlib`
  paths map to `site-packages`, and `scripts`, `headers` and `data` paths map to the environment's corresponding
  installation directories.
- **`.data/scripts/` files.** These can be rewritten at installation, for example in their interpreter line. They
  are listed and not byte-compared with the wheel, and they are checked against the installed `RECORD` only.

**The libraries actually used.** The runner lists every module in `sys.modules` twice: at the input point of
Section 4, and after job 2. Each listing is taken from a copy of `sys.modules` made in one statement. For each module
it records, in the capture record and in the run-end record, with the SHA256 of each file:
- **the module file**, named by `__file__`: a source file, an extension module or another file the loader names;
- **the cached bytecode file**, named by `__cached__`, where that file exists;
- **the origin** named by the module's spec, where it has one, such as `built-in` or `frozen`.

Both listings are file inventories at two instants. Neither is a record of the code that executed (Section 4).

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

**Cached bytecode files are observed only for correspondence, in every class.** Their paths and SHA256 values are
recorded, and Section 4 retains the bytes of those under the environment's `site-packages` as part of its declared
superset. No correspondence comparison is required of them: no `RECORD` equality, and no comparison with the locked
wheel or with the module's source. That holds whether the installed `RECORD` lists them with a hash or with an empty
hash field, and whether they are not listed at all. Their correspondence to the locked wheel, or to the module's
source, is not established. Section 4 makes one other comparison, of stability only: under its bytecode policy no
bytecode file may be written, removed or changed between the capture point and the run end. Stability shows that the
same bytes were present at both readings. It is not correspondence.

**Limits of F3.**
- **The lock digest.** `lock_sha256` establishes the lock file's bytes only. It does not establish that the running
  environment corresponds to the lock. That correspondence is tested only by the per-distribution comparisons above.
  It is tested only for distributions whose status is `locked-verified`, and only for files that a wheel's `RECORD`
  lists with a non-empty hash. Bytecode cache files and `.data/scripts/` files are excepted.
- **Cached bytecode.** It is observed only, whether it was compiled at installation or at import time, and however
  a `RECORD` lists it. W1 does not establish that the bytecode the interpreter executed corresponds to the locked
  wheel or to the module's source. Section 4 checks only its stability between the capture point and the run end,
  which is not correspondence.
- **Unlisted files.** The runner enumerates the files in `site-packages` that no installed `RECORD` lists, such as
  path-configuration files, into the run-end record. They are not established.
- **Distributions outside the lock.** An installed distribution absent from the lock, such as the installer the
  environment was created with, has the status `not-in-lock`. It is recorded, not tested. If any of its module files
  is loaded, W1 stops.
- **Locked distributions without a retained wheel.** Such a distribution has the status `locked-wheel-unavailable`.
  Its correspondence to the lock is not established. If any of its module files is loaded, W1 stops.
- **The interpreter.** Its version, build and compiler strings and its binary digest are recorded. Its origin, its
  build recipe and any published artifact digest are not established. No reference digest exists for the binary or
  the standard-library files, so their digests identify bytes only.
- **Dynamic libraries.** Libraries loaded by the system's dynamic loader are not enumerated. A library installed from
  a wheel, such as one bundled with NumPy, is covered only as an installed file of its distribution; whether it was
  loaded is not recorded. System libraries are not identified.
- **The shell and the operating system.** The recorded values are those the system reports, with the digests of the
  files read. Their build origin is not established.

**The F7 host record.** Each key's value is an object `{value, source, status}`. The `status` is either `observed`
or `not observed`. A `not observed` entry carries a null value and its reason. It is never filled with a declared
or assumed value.

| Key | Source | Treatment |
|---|---|---|
| `host_name` | `os.uname().nodename` | Private only. It is never written to a public record |
| `cpu_model` | The standard output of `/usr/sbin/sysctl -n machdep.cpu.brand_string`, run from an argument vector without a shell | Descriptive |
| `logical_cpu_count` | `os.cpu_count()` | Descriptive |
| `memory_bytes` | The standard output of `/usr/sbin/sysctl -n hw.memsize`, run as above | Descriptive |

The only comparison is that each observed value is equal at run end. These are values the operating system reports.
W1 verifies them against no other source and establishes no hardware property. The architecture is carried by
`operating_system.machine`.

**The payload record.** `w1_env_record.txt` holds exactly eight key lines in the order below. They are followed by
the separator line `# /usr/bin/env follows` and then by the output of `/usr/bin/env`. The checker parses the file by
that structure, and any other structure fails.

| Line | Source in the payload | Comparison made by the checker, for each job |
|---|---|---|
| `dollar_zero=` | `$0` | Exactly `w1_payload.sh` |
| `shell_flags=` | `$-`, after `set -eu` | Contains `e` and `u`, and does not contain `i` |
| `login_shell=` | The guarded `shopt -q login_shell` test | Exactly `off`. `on` fails the F7 criterion |
| `bash_version=` | `$BASH_VERSION` | Exactly equal to `build_identity.bash.version` |
| `bash_path=` | `$BASH` | Exactly `/bin/bash` |
| `uname_s=`, `uname_r=`, `uname_m=` | `/usr/bin/uname -s`, `-r` and `-m` | Exactly equal to `build_identity.operating_system.sysname`, `.release` and `.machine` |
| The `/usr/bin/env` output | The payload's exported environment | The names include `PATH`, `LC_ALL`, `AIIDA_PATH`, `TMPDIR`, `PYTHONNOUSERSITE` and `OMP_NUM_THREADS`, and lie within those six, the shell-maintained `PWD`, `OLDPWD`, `SHLVL` and `_`, and the names of `env_policy.platform_injected`. The first five values equal the launcher record's values, and `OMP_NUM_THREADS` is `1`. A platform-injected name, where present, has the value it has in the interpreter record. `BASH_ENV`, `ENV` and `HOME` are absent. A name outside that set, including one added by the platform or by aiida-core, fails the F7 criterion; it is retained as a finding and is not added to the set afterwards. The one platform-injected name was declared before any run (Section 5) |

The payload's other record, `w1_input_manifest.sha256`, holds the `/usr/bin/shasum -a 256` digest of every input file
and of `w1_payload.sh`. Each digest must equal the SHA256 of the same file as stored for the submission in the job
node's repository (Section 5). The digest of `w1_payload.sh` must also equal that of the payload constant captured
under F1. A mismatch returns 312.

**The payload.**
- **The script.** `prepare_for_submission` writes `w1_payload.sh` from a constant in `w1_job.py`, so its bytes are
  part of the code identity. It runs the code `w1-bash` with that script as its only argument, and it does this
  under `set -eu`:
  1. It writes the payload record defined above to `w1_env_record.txt`, with exactly these lines:

     ```
     printf 'dollar_zero=%s\n' "$0" > w1_env_record.txt
     printf 'shell_flags=%s\n' "$-" >> w1_env_record.txt
     if shopt -q login_shell; then echo 'login_shell=on' >> w1_env_record.txt; else echo 'login_shell=off' >> w1_env_record.txt; fi
     printf 'bash_version=%s\n' "$BASH_VERSION" >> w1_env_record.txt
     printf 'bash_path=%s\n' "$BASH" >> w1_env_record.txt
     printf 'uname_s=%s\n' "$(/usr/bin/uname -s)" >> w1_env_record.txt
     printf 'uname_r=%s\n' "$(/usr/bin/uname -r)" >> w1_env_record.txt
     printf 'uname_m=%s\n' "$(/usr/bin/uname -m)" >> w1_env_record.txt
     echo '# /usr/bin/env follows' >> w1_env_record.txt
     /usr/bin/env >> w1_env_record.txt
     ```

     The login-shell test is guarded so that the expected state does not end the script under `set -e`.
     `login_shell=off` is the expected record, and `login_shell=on` fails the F7 criterion. Either way the payload
     continues and its record is retained. `BASH_VERSION` and `BASH` are always set by Bash, so `set -u` does not
     stop at them.
  2. It writes the `/usr/bin/shasum -a 256` of every input file listed above, and of `w1_payload.sh`, to
     `w1_input_manifest.sha256`.
  3. It copies `w1_structure_in.extxyz` to `w1_structure_out.extxyz` and `w1_identity.json` to
     `w1_identity_out.json` with `/bin/cp`.
- **The retrieve list** is exactly these four outputs. aiida-core adds the two scheduler files (A6).
- **Other settings.**
  - `environment_variables` is `{"OMP_NUM_THREADS": "1"}` and nothing else.
  - `resources` is `{"num_machines": 1, "num_mpiprocs_per_machine": 1}` with no cores-per-process value, so the
    scheduler header adds no export of its own (A3).
  - `prepend_text` and `append_text` are empty, `custom_scheduler_commands` is empty, and `withmpi` is false.

**Parsing and exit codes.** `W1Job` overrides `parse_retrieved_output` (A7). It declares four required output ports:

| Output port | Built from |
|---|---|
| `structure_out` | A `StructureData` built from `w1_structure_out.extxyz` through ASE (Section 6) |
| `identity_out` | A `SinglefileData` of `w1_identity_out.json` |
| `input_manifest` | A `Dict` of the manifest |
| `env_record` | A `SinglefileData` of `w1_env_record.txt` |

It returns a non-zero exit code and attaches no output when:

| Exit code | Name | Returned when |
|---|---|---|
| 310 | `ERROR_W1_MISSING_OUTPUT` | A retrieved file is missing |
| 311 | `ERROR_W1_MALFORMED_OUTPUT` | A file does not parse, or the structure's atom count differs from the sidecar |
| 312 | `ERROR_W1_MANIFEST_MISMATCH` | A manifest digest differs from the digest of the same file as stored for the submission |

**The chain.**
- **Job 1** is labelled `w1-job1`. Its `structure` is S1 and its `identity` is the sidecar built in Section 6.
- **Job 2** is labelled `w1-job2`. Its `structure` and `identity` are job 1's `structure_out` and `identity_out`.
  Every other port takes the same stored node as job 1.

## 4. F1: the code that ran, captured once

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

## 5. F7: no login shell anywhere, and a declared environment

**Scope.** W1's F7 result covers only two things: the no-login setting, and the declared environment. The host
record of Section 3 is carried with a source and a status for each value, but W1 establishes no hardware property.
A hardware value that was not observed is recorded as `not observed` and is never carried as established.

**The invocations F7 must cover.** A2, A3 and A5 give three places where a shell starts:
- the transport's `bash -c`, inside a system shell;
- the scheduler's `bash <script>`;
- the payload's own `bash`.

W1 adds a fourth: the runner's Bash version probe (Section 3). It is started from an argument vector with
`--noprofile --norc`, not through a shell. F7 must cover all four.

**Mandatory values.**
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
2. **Transport.** `use_login_shell` is false on `w1-local-nologin` (A1). The effective computer and authorization
   parameters are read back from the store and recorded before any transport call.
3. **Job environment.** `import_sys_environment` stays true, for the reason in A4. The job's only added variable is
   `OMP_NUM_THREADS=1`. The choice and its reason are recorded in `defaults`.

**The generated script, validated before upload and bound to what ran.** `metadata.dry_run` is not used (A10).
Instead, `W1Job` overrides `presubmit`:
1. It calls the base `presubmit`, which writes the job folder and `_aiidasubmit.sh` (A11).
2. It reads the generated `_aiidasubmit.sh` from that folder and checks it against A3 and A5. The script may contain
   no `-l`, no sourcing of any file and no `env --ignore-environment` line. Its run line must invoke `/bin/bash
   w1_payload.sh`, and its environment block may set only `OMP_NUM_THREADS=1`.
3. It computes the SHA256 of the script and of every file in the folder, and reports them to the job node's log.
4. It raises on any violation, so that nothing is uploaded or submitted (A11).

After the run the checker binds three copies of each file:
- the digests reported at `presubmit`;
- the files that aiida-core stores for the submission in the job node's repository;
- the files in the job's work directory, which is local, from which the script was run.

The three must be byte-identical. Any difference stops W1. Because the preparation records carry the node's
identifiers (A8), each job's files are compared within that job, never across the two jobs. The binding covers the
exact inputs, options and code:
- the input node UUIDs and option values recorded on the job node are compared with the declarations of Sections
  2 and 3;
- no other CalcJob node exists in the W1 profile, and the chain consists of exactly `w1-job1` and `w1-job2`.

The transport is requested and opened before `presubmit` runs (A11). Whether opening the local transport starts a
shell was not read. The configured no-login setting therefore has to be in effect before job 1 is launched
("Mandatory values", item 2).

**What counts as evidence.**
- **Primary.** The recorded configuration, the bound script and the source facts A1 to A5.
- **Secondary.** A command trace, retained where the transport logs one.
- **Corroboration only, for the no-login setting.** The payload record's `login_shell` and `shell_flags` lines. A
  clean scheduler stderr, or a shell flag printed by the payload, cannot show that no login shell ran.
- **For the declared environment.** The launcher record, the interpreter record at start and after job 2, and the
  payload record's `/usr/bin/env` output, each compared as declared (item 1 above, and Section 3).

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

## 6. F4: identity through the chain

**The sidecar.** It is built from the frozen file's text by a plain-text parser that does not use ASE. For each site
index i it holds six required fields:
- `atom_id`;
- the element symbol;
- the three position strings exactly as in the file;
- `map_num`;
- `radical_electrons`.

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

**The conversion sequence.**
1. **T0.** The frozen file is read with ASE 3.29.0 in `extxyz` format.
2. **S1.** A `StructureData` is built from T0. It is job 1's `structure`.
3. **Job 1's input file.** `prepare_for_submission` writes `w1_structure_in.extxyz` from S1 with its own writer: an
   `extxyz` header with `Properties=species:S:1:pos:R:3`, and each position formatted `%.8f`. The frozen positions
   have eight decimal places, so this reproduces their text (*project inference*).
4. **The payload** copies the file.
5. **T1 and S2.** `parse_retrieved_output` reads the copy with ASE (T1) and builds S2, job 1's `structure_out` and job
   2's `structure`.
6. **Job 2** repeats steps 3 to 5, ending with job 2's `structure_out`, S3.

**The checks at every stage** (T0, S1, job 1's input file, T1, S2, job 2's input file, and the structures of job 2
up to S3):
- **Site association.** Site i's element must equal the sidecar's, and its three coordinates must equal the sidecar's
  position strings, parsed exactly. An exchange of two atoms of the same element changes positions and fails.
- **Native arrays present.** Where a native `atom_id` array is present, each native string value must equal the
  corresponding sidecar string exactly. Where a native `map_num` or `radical_electrons` array is present, each native
  value must be an integer scalar, excluding Boolean and floating-point values, and must equal the base-10 integer
  represented by the corresponding sidecar string. That string must match `[+-]?[0-9]+` in its entirety; otherwise
  W1 fails. This conversion is for comparison only and does not change the sidecar bytes. Any type or value mismatch
  fails.
- **Native arrays absent.** Where one is absent, its non-survival is recorded as observed. This is permitted: Stage 0
  measured `atom_id` absent after a `StructureData` round trip. A value copied from the sidecar is never reported as
  native survival.
- **Sidecar carriage.** The sidecar bytes must be identical at every step, and equal to the checker's regeneration:
  job 1's `identity`, job 1's `identity_out`, job 2's `identity` and job 2's `identity_out`. Agreement of element
  multisets, or mere presence of a field, is never taken as identity.
- **Fixed-set fixture.** Each of the six fixture atoms is found by `atom_id` in the sidecar. At its index, every
  structure must carry the matching element and position.

**Negative cases.** These are run by the checker on local synthetic data, not as AiiDA jobs, and each must fail:
- exchanging `D-O1-H1` with `D-O2-H1`;
- a duplicate `atom_id`;
- a missing sidecar;
- a missing fixture member;
- one wrong `map_num` value in an otherwise complete sidecar;
- a permuted map that has been copied.

## 7. Acceptance criteria

W1 closes the C3 blockers only if every criterion holds:
1. Exactly two CalcJob nodes, `w1-job1` and `w1-job2`, finish with exit status 0 and process type `w1_job.W1Job`.
   Their link records show every port of Section 3 as an input of each, with job 2's `structure` and `identity`
   created by job 1.
2. Every F4 check of Section 6 passes at every stage, and every negative case fails.
3. The F1 items resolve from the store as bytes, each is an input of both jobs, and every comparison of Section 4
   between the capture point and the run end holds.
4. The F7 record shows, for both jobs, within the scope of Section 5 (the no-login setting and the declared
   environment only):
   - the launcher record and the interpreter records of Section 5, and every payload-record comparison of Section 3;
   - `use_login_shell` false in the effective configuration;
   - a `presubmit` validation that passed;
   - the three-way byte binding of the submission files that Section 5 requires.

   No hardware property is part of this criterion.
5. The stored `defaults`, `build_identity`, `calc_performed`, `seed`, `units`, `per_claim`, `env_policy`,
   `host_record` and `code_identity` inputs of **both** jobs satisfy the "Mandatory contents" declarations of Section
   3 key by key. Each check is made against the declaration, not against another stored copy of the input. For a
   *recorded* value, the declaration is the source and comparison that Section 3, or for `code_identity` Section 4,
   gives it. Any of the following fails W1:
   - an empty mapping;
   - a missing required key or an extra key;
   - a value that differs from its declared exact value, or lies outside its declared set;
   - a value that fails a comparison Section 3 declares for it, where that comparison applies, including its run-end
     comparison. For a `distributions` entry, only the comparisons its status makes applicable are made. A value
     recorded as `not available`, `not established` or `not applicable: not in lock` is not a failure in itself;
   - a `distributions` entry that fits none of the three statuses, or an `aiida_core`, `ase` or `numpy` entry whose
     status is not `locked-verified`;
   - a missing N/A or fixture label;
   - a host-record value marked `observed` without a value, or a `not observed` value with one.

   As additional checks, each job's `input_manifest` must match the digests of its stored submission files, and every
   module file of the capture record and of the run-end record must pass its class check under "The libraries
   actually used". Cached bytecode files are not checked for correspondence; their stability between the capture
   point and the run end is a comparison of Section 4, under criterion 3.
6. Every repository object of every chain node has a key equal to its SHA256.
7. The two user-level observations of Section 5 are equal, and the fixture diff passes its check of Section 4.

## 8. Stop conditions and failure handling

W1 stops, retains everything and repairs nothing on any of these:
- a user-level AiiDA configuration directory appears, or the two user-level observations of Section 5 differ;
- the launcher record differs from the Section 5 allow-list or its declared values, or an interpreter record holds a
  name outside the allow-list and the declared platform-injected name, lacks an allow-list name or differs from the
  launcher record in an allow-list value;
- `use_login_shell` reads back true;
- the `presubmit` validation raises, or the three copies of a submission file differ;
- the process type differs from `w1_job.W1Job`;
- a precondition of Section 4 fails, or a comparison of Section 4 between the capture point and the run end differs,
  a new, removed or changed bytecode file included;
- a required link is missing;
- a job returns 310, 311 or 312;
- a provenance input fails its Section 3 "Mandatory contents" declaration;
- a comparison that Section 3 declares, and that applies, fails: for the build identity, the host record, the
  payload record or a loaded module file;
- a `distributions` entry fits none of the three statuses. A permitted status never stops W1 by itself, and a cached
  bytecode file stops W1 only through the stability comparison of Section 4, never through its correspondence;
- an F4 check fails;
- a negative case passes;
- a project module file, or a module file outside the classes of Section 3, is first listed at the run end;
- the fixture diff fails its check of Section 4.

A stopped or failed W1 is retained as a failure record, as C3 F9 requires for any job. Nothing is deleted or rerun
silently.

## 9. Retained artifacts and ordering

**Private.** Kept privately, as for C3:
- node identifiers;
- the effective configuration record, with the launcher record and the interpreter records of Section 5;
- the two user-level observations of Section 5;
- the capture record of Section 4, with the module listings, the environment, `__pycache__` and runtime-data
  listings, and the run-end comparisons;
- the run-end record (Section 3):
  - the second reading of every build-identity and host-record source;
  - the loaded module files and cached bytecode files, with their digests;
  - the `site-packages` files that no installed `RECORD` lists;
- the `presubmit` validation reports, the stored submission files and the work-directory copies;
- the checker's output;
- a closure inventory: every node, link, repository object and digest of the chain.

**Public.** Content hashes, as for C3.

**Ordering.** The closure inventory is frozen first. Review then binds its digest, and the review record, F10, is held
by the orchestration layer and refers to the inventory. The review record is never inside the inventory, so no
digest refers to itself.

## 10. Limits

- W1 specifies a wiring test. It is not an engine or chemistry test.
- Success would show that the software carries the F-fields through a two-job chain on one computer configuration.
  It would establish nothing about chemistry, about engine behaviour or about F9.
- Every source statement in Section 1 reports aiida-core 2.9.2 source text. How it behaves on the host is what W1
  itself would observe.
- F3 is bounded by the "Limits of F3" in Section 3.
  - The lock digest establishes the lock's bytes only.
  - The correspondence of the environment to the lock is tested per distribution. It is tested only for distributions
    whose status is `locked-verified`, and only for files a wheel's `RECORD` lists with a non-empty hash.
  - Cached bytecode is observed only for correspondence; its stability within the run is checked (Section 4).
  - The interpreter's origin, the shell's build origin and system libraries are not established.
- F7 is bounded to the no-login setting and the declared environment. W1 establishes no hardware property.
- The declared environment admits one platform-injected name in the interpreter and payload records. Its cause is not
  established.
- F1 is a file inventory at two instants. W1 claims no guarantee about the code that executed (Section 4).
- The two driver files are identified by their bytes, SHA256 and Git blob identifiers, not by a commit.
- The user-level observation covers the paths that Section 5 names, and only the names of their direct entries.
- Running W1 needs a separate authorization, and Stage 1 remains BLOCKED and is not authorized.
