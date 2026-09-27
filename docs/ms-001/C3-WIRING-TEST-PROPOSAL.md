# C3 wiring test W1: proposed specification

Date: 2026-09-27. MS-001 scope option B, before Stage 1. Status: **PROPOSAL. Specification only. Nothing here has
been run, installed, registered or imported, and running it needs its own authorization.**

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
  only for files a wheel's `RECORD` lists with a hash. Cached bytecode is observed only. W1 does not establish the
  origin of the interpreter or of the shell (Section 3).
- **No authorization.** Nothing here authorizes Stage 1, a calculation or an installation.

## 1. Sources

The design rests on aiida-core 2.9.2 source, read from the retained wheel of the Stage 0 hash-locked installation
(SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`, C3 §1). Member digests are in the
[pre-Stage-1 source ledger](PRESTAGE1-SOURCE-LEDGER.md). Each statement reports what that source text defines.

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

## 2. Declared setup

| Item | Declaration |
|---|---|
| Python environment | The existing Stage 0 project-local environment: CPython 3.12.14, aiida-core 2.9.2, ASE 3.29.0, lock SHA256 `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8` (C3 §1). Nothing is installed |
| Profile and storage | A new AiiDA profile dedicated to W1, with `core.sqlite_dos` storage and no message broker, under a new project-local configuration directory in the git-ignored project area. The Stage 0 profile is not reused, so the W1 store holds only W1's nodes. The profile is created only under the future authorization |
| Computer | A new Computer labelled `w1-local-nologin`: transport `core.local` with `use_login_shell` false, scheduler `core.direct`, shebang `#!/bin/bash`, and its work directory inside the same project-local area |
| Code | An installed code labelled `w1-bash` on that computer, executable `/bin/bash`, command-line argument `w1_payload.sh` |
| Runner | In-process `run_get_node` of aiida-core in one interpreter, with no daemon. The interpreter is the Stage 0 environment's own, invoked by its exact resolved path, which is recorded privately and written publicly as the environment-relative `bin/python`. Before it imports anything outside the standard library, it records the F3 build identity and the host record of Section 3 and makes their checks. Its version must read back as CPython 3.12.14. The lock digest check establishes the lock file's bytes only; whether the installed environment corresponds to the lock is tested separately, per distribution (Section 3). It is never found through `PATH`: under the clean `PATH` of Section 5, a bare `python` would not select that environment. It is started as `<environment>/bin/python -E -s tools/w1_driver.py` from the repository root. `-I` is not used, because it would drop the driver's directory from the import path |
| Class and module | Class `W1Job` in the module file `tools/w1_job.py`. The driver puts `tools/` first on the import path and imports `w1_job`. The recorded process type must equal `w1_job.W1Job` (A9); any other value, such as one caused by an entry point of the same name, stops W1. Both files are tracked at the declared commit, and their bytes are also inputs of each job (Section 4) |
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
  payload record". A *recorded* value with no declared source and comparison is not allowed.

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
| `env_policy` (F7) | `allow_list`: exactly the five variables of Section 5. `absent`: `["BASH_ENV", "ENV", "HOME"]`. `use_login_shell`: false. `import_sys_environment`: true. `shell`: `/bin/bash` |

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

**The libraries actually used.** After job 2 the runner lists every module in `sys.modules`. For each module it
records two kinds of file in the run-end record, with the SHA256 of each:
- **the module file**, named by `__file__`: a source file, an extension module or another file the loader names;
- **the cached bytecode file**, named by `__cached__`, where that file exists.

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

**Cached bytecode files are observed only, in every class.** Their paths and SHA256 values are recorded. No `RECORD`
equality, and no other comparison, is required of them. That holds whether the installed `RECORD` lists them with a
hash or with an empty hash field, and whether they are not listed at all because they were written at import time.
Their correspondence to the locked wheel, or to the module's source, is not established.

**Limits of F3.**
- **The lock digest.** `lock_sha256` establishes the lock file's bytes only. It does not establish that the running
  environment corresponds to the lock. That correspondence is tested only by the per-distribution comparisons above.
  It is tested only for distributions whose status is `locked-verified`, and only for files that a wheel's `RECORD`
  lists with a non-empty hash. Bytecode cache files and `.data/scripts/` files are excepted.
- **Cached bytecode.** It is observed only, whether it was compiled at installation or at import time, and however
  a `RECORD` lists it. W1 does not establish that the bytecode the interpreter executed corresponds to the locked
  wheel or to the module's source.
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
| The `/usr/bin/env` output | The payload's exported environment | The names include `PATH`, `LC_ALL`, `AIIDA_PATH`, `TMPDIR`, `PYTHONNOUSERSITE` and `OMP_NUM_THREADS`, and lie within those six plus the shell-maintained `PWD`, `OLDPWD`, `SHLVL` and `_`. The first five values equal the parent's declared values, and `OMP_NUM_THREADS` is `1`. `BASH_ENV`, `ENV` and `HOME` are absent. A name outside that set, including one added by the platform or by aiida-core, fails the F7 criterion; it is retained as a finding and is not added to the set afterwards |

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
1. **Parent environment.** The runner is started from an empty environment containing exactly: `PATH=/usr/bin:/bin`,
   `LC_ALL=C`, `AIIDA_PATH` set to W1's project-local configuration directory, `TMPDIR` set to a project-local
   directory, and `PYTHONNOUSERSITE=1`. Nothing else is set. In particular `BASH_ENV`, `ENV` and `HOME` are absent,
   and `PATH` resolves `bash` to `/bin/bash`. A2 passes this environment on to every later shell. The runner records
   `os.environ` at start, and its names must equal `env_policy.allow_list` exactly.
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
- **For the declared environment.** The parent environment recorded at start, and the payload record's
  `/usr/bin/env` output, each compared as declared (item 1 above, and Section 3).

No file is written to any user startup file, and no user startup or history file is read.

## 6. F4: identity through the chain

**The sidecar.** It is built from the frozen file's text by a plain-text parser that does not use ASE. For each site
index i it holds six required fields:
- `atom_id`;
- the element symbol;
- the three position strings exactly as in the file;
- `map_num`;
- `radical_electrons`.

A missing required field, for any site, fails W1.

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
- **Native arrays present.** Where a native per-atom array (`atom_id`, `map_num`, `radical_electrons`) is present,
  its value at every site must equal the sidecar's. Any difference fails.
- **Native arrays absent.** Where one is absent, its non-survival is recorded as observed. This is permitted: Stage 0
  measured `atom_id` absent after a `StructureData` round trip. A value copied from the sidecar is never reported as
  native survival.
- **Sidecar carriage.** The sidecar bytes must be identical at every step: job 1's `identity`, job 1's
  `identity_out`, job 2's `identity` and job 2's `identity_out`. Agreement of element multisets, or mere presence of
  a field, is never taken as identity.
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
3. The F1 items resolve from the store as bytes, and their digests are unchanged between the start and the end of
   the run.
4. The F7 record shows, for both jobs, within the scope of Section 5 (the no-login setting and the declared
   environment only):
   - the Section 5 environment in the parent, and every payload-record comparison of Section 3;
   - `use_login_shell` false in the effective configuration;
   - a `presubmit` validation that passed;
   - the three-way byte binding of the submission files that Section 5 requires.

   No hardware property is part of this criterion.
5. The stored `defaults`, `build_identity`, `calc_performed`, `seed`, `units`, `per_claim`, `env_policy` and
   `host_record` inputs of **both** jobs satisfy the "Mandatory contents" declarations of Section 3 key by key. Each
   check is made against the declaration, not against another stored copy of the input. For a *recorded* value, the
   declaration is the source and comparison that Section 3 gives it. Any of the following fails W1:
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
   module file of the run-end record must pass its class check under "The libraries actually used". Cached bytecode
   files are observed only and are not checked.
6. Every repository object of every chain node has a key equal to its SHA256.

## 8. Stop conditions and failure handling

W1 stops, retains everything and repairs nothing on any of these:
- a user-level AiiDA configuration directory appears;
- any variable outside the Section 5 allow-list is present in the parent;
- `use_login_shell` reads back true;
- the `presubmit` validation raises, or the three copies of a submission file differ;
- the process type differs from `w1_job.W1Job`;
- a code capture changes during the run;
- a required link is missing;
- a job returns 310, 311 or 312;
- a provenance input fails its Section 3 "Mandatory contents" declaration;
- a comparison that Section 3 declares, and that applies, fails: for the build identity, the host record, the
  payload record or a loaded module file;
- a `distributions` entry fits none of the three statuses. A permitted status, and a cached bytecode file, never
  stop W1 by themselves;
- an F4 check fails;
- a negative case passes.

A stopped or failed W1 is retained as a failure record, as C3 F9 requires for any job. Nothing is deleted or rerun
silently.

## 9. Retained artifacts and ordering

**Private.** Kept privately, as for C3:
- node identifiers;
- the effective configuration record, with the parent environment recorded at start;
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
  - Cached bytecode is observed only.
  - The interpreter's origin, the shell's build origin and system libraries are not established.
- F7 is bounded to the no-login setting and the declared environment. W1 establishes no hardware property.
- Running W1 needs a separate authorization, and Stage 1 remains BLOCKED and is not authorized.
