# H2-A-01 run proposal (Phase A, one job)

## 1. Status

**PROPOSED_NOT_AUTHORIZED.** This is a preparation-only `[AGENT]` proposal for a calculation that has not been run.
It authorizes nothing and is not readiness. Accepting it as a document would not be a scientific gate or an
authorization ([evidence policy §5](../../../evidence-policy.md)).

**The shipped driver cannot launch the engine.** It is not runnable, not ready, and does not need only a person's run
authorization. Every launch is refused with `NETWORK_PREREQUISITE_UNRESOLVED` (§8.5, gate N1). Resolving N1 needs
revised driver (and possibly profile) bytes under one of the routes R1–R3, a renewed independent review of those
bytes, and then a person's separate decision on them. This package includes none of these.

Labels follow [h2-method-specification.md](../h2-method-specification.md):
- a statement taken from source text with a file and line locator is `[LIT]` provenance about software behaviour
  defined by that source, with no chemistry class;
- choices and controls of this package are `[AGENT]`;
- static installed bytes are observations of files, not of what a build does.

## 2. Files of the package

| File | Role |
|---|---|
| [h2_phase_a_driver.py](h2_phase_a_driver.py) | Control driver, standard library only. Static preflight, code-provenance record and its re-derivation, authorization interlock, launch of at most one engine process, independent classification that compares every gate-defining recorded value with the launch or input binding (§9a) |
| [h2_phase_a_payload.py](h2_phase_a_payload.py) | Future engine-side script, run only by the bound interpreter inside an authorized run |
| [h2-a-01-input.json](h2-a-01-input.json) | Prospective input. The driver checks it against the accepted parameter file |
| [h2-a-01-static-identity.json](h2-a-01-static-identity.json) | Static identity record: package records, file digests, source comparison, preflight expectations |
| [tests/](tests/) | Fixture and fake-process tests. No engine is imported or run |
| [H2-A-01-DECISION-PACKET.md](H2-A-01-DECISION-PACKET.md) | What a person would decide, with bound digests and a blank template that is not an authorization |

The accepted inputs are unchanged: [h2-method-parameters.json](../h2-method-parameters.json),
[h2-method-specification.md](../h2-method-specification.md) and
[lesson-01-fixed-separation-scf.md](../lesson-01-fixed-separation-scf.md).

## 3. Prospective invocation

There is one job (`H2-A-01`, R = 1.4 bohr), one engine process and zero retries. Placeholders: `<PREFIX>` is the
candidate Psi4 environment, `<RUNS_ROOT>` is an existing, empty private directory, and `<AUTH>` is the person's
authorization file. The driver runs under a standard-library Python that is not the engine interpreter.

```
python3 -I docs/learning/h2/phase-a/h2_phase_a_driver.py preflight --interpreter <PREFIX>/bin/python3.14 --prefix <PREFIX> --runs-root <RUNS_ROOT>
python3 -I docs/learning/h2/phase-a/h2_phase_a_driver.py code-provenance --out <PROVENANCE>
python3 -I docs/learning/h2/phase-a/h2_phase_a_driver.py run --interpreter <PREFIX>/bin/python3.14 --prefix <PREFIX> --runs-root <RUNS_ROOT> --authorization <AUTH>
```

`<PROVENANCE>` is a detached, private code-provenance record (§9), written after the final bytes and bound by SHA256
in the authorization. The `code-provenance` and `run` modes spawn read-only Git queries (`rev-parse`, `ls-tree`,
`cat-file`, with `--no-optional-locks`). `preflight` spawns no process.

The driver would then launch exactly:

```
<PREFIX>/bin/python3.14 -I -B <RUNS_ROOT>/H2-A-01/bundle/h2_phase_a_payload.py <RUNS_ROOT>/H2-A-01/bundle/h2-a-01-input.json <RUNS_ROOT>/H2-A-01
```

The launch conditions are:
- **Working directory:** `cwd` = `<RUNS_ROOT>/H2-A-01/scratch`, created empty by the driver.
- **Process:** a new session and process group; stdin closed; stdout and stderr to files created exclusively.
- **Environment:** exactly the allow-list of §4.
- **Wall clock:** 300 s.

`-B` is added to `-I` so that the interpreter writes no bytecode and the prefix stays unmodified (§8.5). The semantics
of both flags are CPython's and are not located in a cached source here (§10).

**Settings and where they come from.** Each setting is taken from the accepted parameter file. Where the driver
derives a value itself, it says so.

| Setting | Value | Source |
|---|---|---|
| Molecule | H2, charge 0, multiplicity 1, 2 electrons; H1 (0, 0, −0.7), H2 (0, 0, +0.7) bohr | `system`, `phases.A.job_sequence`; positions derived by the driver from `(0, 0, ∓R/2)` |
| Method and basis | RHF, STO-3G (2 basis functions expected) | `electronic_model` |
| Engine options | `reference rhf`, `basis sto-3g`, `guess core`, `scf_type direct`, `df_scf_guess false`, `e_convergence 1e-8`, `d_convergence 1e-8`, `maxiter 50`, `fail_on_maxiter true` | `proposed_engine_options.*.value` |
| Molecule options | `units bohr`, `symmetry c1`, `no_reorient`, `no_com` | same |
| Threads | 1 | `proposed_engine_options.threads`, `resource_bounds.threads` |
| Engine memory | `500 MiB` (524 288 000 bytes) | `proposed_engine_options.memory`, `resource_bounds.engine_memory_mib` |
| Wall bound, jobs, retries | 300 s, 1 job, 0 retries | `resource_bounds` |
| Nuclear-repulsion check | \|V_NN − 1/R\| ≤ 1e-10 hartree | `stop_conditions`, parsed by the driver |

Further `[AGENT]` values are not in the accepted file: the atomic mass `1.00782503223` (v1.11
`psi4/include/psi4/masses.h` 80), needed only to construct the molecule record, the read-back tolerances in the input
and the free-space floor (§5, §8.7). They are not method settings. The driver's preflight fails if the input differs from these derived
values (`input.matches_parameters`).

## 4. Environment

The driver builds the engine's environment from an allow-list and inherits nothing:

| Name | Value | Reason |
|---|---|---|
| `PATH` | `<PREFIX>/bin:/usr/bin:/bin` | Minimal search path. v1.11 uses `PATH` only for optional add-on executables (`psi4/extras.py` 121–140) |
| `TMPDIR` | `<RUNS_ROOT>/H2-A-01/scratch` | Keeps temporary files of Python and libraries in the fresh scratch |
| `PSI_SCRATCH` | same | Sets the engine's scratch path at import (`psi4/__init__.py` 76–80). Without it, the default is `/tmp` (`psi4/src/psi4/libpsio/filemanager.cc` 41–53) |
| `OMP_NUM_THREADS` | `1` | `[AGENT]` single OpenMP thread from start-up. The engine also sets threads explicitly (§7). The conda record names an OpenMP OpenBLAS build. Its use of this variable is not verified here |
| `LC_ALL` | `C` | `[AGENT]` fixed locale for formatted output |

These names are kept absent on purpose:
- `PSIDATADIR` replaces the data directory (`psi4/__init__.py` 59–68).
- `PSIPATH` is searched before the library basis directory (`psi4/driver/qcdb/libmintsbasisset.py` 803–805) and for
  add-ons (`psi4/extras.py` 139–140).
- `BRIANQC_ENABLE` and `BRIANQC_ENABLE_DFT` are read by `psi4/src/core.cc` 1134 and 1146.
- `TEMP` and `TMP` are read only on Windows (`filemanager.cc` 44–47).
- `PYTHONPATH`, `PYTHONHOME`, the `DYLD_*` loader variables, proxies and `HOME` are excluded too. `-I` ignores
  `PYTHON*` variables, but that is CPython behaviour, not located here.

An authorization whose declared environment contains any other name, or any other value, blocks launch.

**Platform-injected name.** On this host a CoreFoundation-linked interpreter's `os.environ` holds
`__CF_USER_TEXT_ENCODING` even when it is started with an explicit environment, and child processes inherit it. The
evidence is [W1-PRE-RUN-DETERMINATION.md](../../../ms-001/W1-PRE-RUN-DETERMINATION.md) (observation table, line 77,
and option O1, line 304), [W1-PRE-RUN-DETERMINATION-02.md](../../../ms-001/W1-PRE-RUN-DETERMINATION-02.md),
[w1-outcome.json](../../../ms-001/w1-outcome.json) and [w1-outcome-02.json](../../../ms-001/w1-outcome-02.json).
Those records concern a different interpreter.
- The driver never puts this name in the launcher environment.
- The payload records the full observed environment before import and accepts this one declared name.
- Any other undeclared name stops before energy and spends the attempt.
- The payload never scrubs a name.

## 5. Stop tiers

The rule for every row is: stop, keep all output, mark remaining points NOT_RUN, change no setting. Phase A has no
remaining point. Phase B stays NOT_RUN under a separate decision.

The tiers are:
- **BLOCK_LAUNCH:** no engine process exists.
- **STOP_BEFORE_ENERGY:** the engine process stops itself before the energy call.
- **FAILED:** the run failed and is recorded.
- **QUARANTINE:** output is kept, but it is not admissible until reviewed.

Every row maps to exactly one tier. A run reaching none of them is `COMPLETED_PENDING_REVIEW`, which is not a result
class (§9).

| Condition (accepted ones quoted; others `[AGENT]`) | Detected by | Tier |
|---|---|---|
| "nonzero exit" (also termination by a signal, or a spawn failure) | driver | FAILED |
| "timeout" (300 s) | driver | FAILED |
| "SCF not converged or iteration limit reached" (engine convergence error; `converged` not true; the recorded integer count ≥ 50; or, failing closed, a finite raw reported count ≥ 50 whatever the recorded count). The limit is evaluated independently of the raw-consistency check, and a raw mismatch is kept as an additional reason | payload record, driver | FAILED |
| "nonfinite energy" | driver, from result record | FAILED |
| Identity mismatch found statically before launch: package records, bound file digests, interpreter, input against parameters | driver preflight | BLOCK_LAUNCH |
| Identity mismatch at P0: re-hashed prefix files, interpreter flags or path, prefix | payload P0 | STOP_BEFORE_ENERGY |
| Identity mismatch at I1: engine version, module or extension path, loaded Libint or core library, data directory | payload I1 | STOP_BEFORE_ENERGY |
| Identity mismatch at I2: method, reference, options, threads, memory, charge, multiplicity, electron count, atom count, atom labels, coordinates, units, frame settings, printed banner | payload I2 | STOP_BEFORE_ENERGY |
| Identity mismatch at I3: basis file or digest, basis-function count | payload I3 | STOP_BEFORE_ENERGY |
| Identity mismatch after the energy call: version, reference, basis-function count, electrons, atoms, coordinates, options, banner not preserved | driver, from result record | QUARANTINE |
| "missing reported nuclear repulsion" (after energy) | driver | QUARANTINE |
| "reported nuclear repulsion differing from 1/R by more than 1e-10 hartree", or nonfinite (after energy) | driver | QUARANTINE |
| Molecule nuclear repulsion before energy missing, nonfinite or off 1/R | payload I3 | STOP_BEFORE_ENERGY |
| "any missing provenance field": a binding the driver cannot record before launch | driver | BLOCK_LAUNCH |
| Code provenance absent, its digest different from the authorization, its re-derivation from Git and the current bytes different (base commit, base blob ids, diffs, current bytes), or unresolvable (Git query failing, base blob not matching its id) | driver | BLOCK_LAUNCH |
| "any missing provenance field": a stage or result record absent, malformed, of the wrong shape or type, or not a passed gate; a gate-defining value differing from its launch or input binding (§9a); `scf_iterations` not a positive integer or not equal to the raw reported value; energy call and return times missing or out of order; an expected output (including the engine output and `.log` files) absent after exit 0 | driver | QUARANTINE |
| A malformed result record, even if it also reports failure (FAILED applies only to a well-formed result) | driver | QUARANTINE |
| Classification error of any kind (classification never raises) | driver | QUARANTINE |
| "any network access or installation attempt": prerequisite unresolved | driver preflight | BLOCK_LAUNCH (`NETWORK_PREREQUISITE_UNRESOLVED`) |
| "any network access or installation attempt": in the compared set (§8.6), a record name added or removed, a bound package record's content changed, a bound file changed, or any post-run identity check failing | driver, before against after | QUARANTINE |
| Authorization absent or any binding mismatch; existing attempt record; runs root misplaced; free space below 2 GiB; prefix or interpreter path not canonical or leaving the prefix | driver | BLOCK_LAUNCH |
| Failure after the attempt directory is created but before spawn | driver | BLOCK_LAUNCH; the attempt record still blocks any relaunch |
| Undeclared environment name in the engine process; engine module loaded before import; import failure | payload P0 or import | STOP_BEFORE_ENERGY |
| Process-group members left after the engine process ends | driver | QUARANTINE |
| Payload stop exit without a valid stop record, or with one inconsistent with the stage records (unknown stage, an earlier stage not passed, the stopping stage's problems differing, or a later stage record present) | driver | FAILED |

When several conditions occur, FAILED outranks QUARANTINE. Every reason is kept in `outcome.json`.

## 6. Identity layers and ordering

There are three layers, kept apart:
1. **Pre-launch static identity.** Statically observed on 2026-10-10 under a person's bounded authorization, and
   recorded in [h2-a-01-static-identity.json](h2-a-01-static-identity.json):
   - the installed psi4 and libint package records equal every B2 §6 declared field
     ([B2 §6](../../../ms-001/B2-METHOD-DECLARATION.md#6-second-implementation-for-the-p2-check)) [39];
   - `include/libint2/shell.h` equals `e0aa1e87…`;
   - `lib/libint2.dylib` is a regular file equal to the declared archive's path record;
   - `share/psi4/basis/sto-3g.gbs` equals the archive record, the v1.11 tagged source and `b472adfb…`;
   - `core.cpython-314-darwin.so` (`0d12c8cd…`, 37 500 848 bytes) differs from the archive's record (`08879420…`,
     37 483 872 bytes, a binary file with a prefix placeholder) and equals the installed record's own in-prefix
     digest. Correspondence between the two is not shown;
   - the interpreter `bin/python3.14` (`5bac0535…`) is outside the B2 declaration. Its package record is python 3.14.7
     `h0ae1c2c_106_cp314`.

   The driver re-checks all of these at preflight, again immediately before launch, and after the process ends. The
   payload re-hashes the prefix files before import (P0).
2. **Post-import loaded identity.** A future authorized substep; nothing was performed now. At I1 the payload records
   and checks:
   - `psi4.__version__` against `1.11`;
   - `psi4.__file__` and `psi4.core.__file__` inside `<PREFIX>`;
   - the data directory (`core.get_datadir`, `psi4/src/core.cc` 1256–1257; set at import, `psi4/__init__.py` 82);
   - the loaded-image list with on-disk digests of loaded files under `<PREFIX>`. Every image named `libint2*` must
     be `<PREFIX>/lib/libint2.dylib` with the bound digest, and the core extension must carry its bound digest.

   The list comes from the dyld image API through `ctypes`. That is an operating-system interface, not engine
   source, and its documentation is not cached here (§10).

   **Known launch risk (Libint load name).** The installed-build audit recorded that the core extension declares a
   dependency on `@rpath/libint2.dylib` and that Libint's install name is the same
   ([INSTALLED-BUILD-AUDIT §4](../../../ms-001/INSTALLED-BUILD-AUDIT.md#4-installed-libint2-files-against-the-record)).
   Which file the loader resolves for it is not established. If the loaded image's realpath is not
   `<PREFIX>/lib/libint2.dylib`, the run stops at I1 and the single attempt is spent.
3. **Source-to-binary correspondence.** Unproved. A byte-equal Python file shows only that those bytes are equal.
   Compiled code cannot be compared with source by hash ([SOURCE-RESOLUTION §8](../../../ms-001/SOURCE-RESOLUTION.md#8-psi4-compiled-steps-and-fitting-bases)).

**What the ordering establishes.**
- Static bound files are checked by the driver before launch and re-hashed by the payload before `import psi4`.
- Loaded observations are validated after import and before the payload's explicit settings, molecule, basis,
  nuclear-repulsion and energy API calls: version string, module and extension paths, and loaded-image paths with
  on-disk digests of those files.
- Not proved: what the import and start-up of the engine and its native libraries do. `import psi4` loads the
  extension and its linked libraries and runs `core.initialize()`, `core.set_datadir`, the scratch set-up, `atexit`
  registrations, plugin imports and `set_num_threads(1)` (`psi4/__init__.py` 71–96), and those native side effects are
  not observed. Also not proved: the correspondence between in-memory code and on-disk bytes, and source-to-binary
  correspondence.

**Payload stages.** Each stage writes its own record. A failed gate writes a stop record, and no later stage runs.
- P0 (pre-import record): environment, interpreter, static re-hash.
- import.
- I1 (`i1-identity.json`).
- I2 (`i2-configuration.json`): threads, memory, output file with the banner requested explicitly, options, molecule
  from `core.Molecule.from_dict`, read-back.
- I3 (`i3-basis-geometry.json`): basis file resolved and hashed, `nbf = 2`, molecule nuclear repulsion against 1/R.
- The single `psi4.energy('scf', molecule=…, return_wfn=True)`.

The ordering is exercised by a test with a fixture stand-in confined to a test subprocess. It is not exercised against
the engine.

## 7. Option, default, energy and convergence semantics in the v1.11 tagged source

These are `[LIT]` statements about the Psi4 v1.11 tagged source (commit `f16f4ea2…`, archive `040e843e…`) [31, 52].
They describe behaviour defined by that source, not by any build (P2, P4). Of the sixteen installed Python files read
statically, thirteen are byte-identical to the tag. `psi4/__init__.py`, `psi4/metadata.py` and `psi4/extras.py` differ
only in build-configured lines [54].

- **Reference.** `REFERENCE` defaults to `RHF` (`psi4/src/read_options.cc` 1464). `scf_set_reference_local` changes
  RHF to RKS only when the functional needs exchange-correlation; for Hartree–Fock it leaves the reference unchanged
  (`psi4/driver/procrouting/proc_util.py` 40–64). Whether the `scf` functional entry needs exchange-correlation is
  not traced here, and the post-energy read-back of the wavefunction class checks it. The factory builds `core.RHF`
  for `RHF` (`proc.py` 1437–1438).
- **Options are set as globals** by `set_options` (`psi4/driver/p4util/python_helpers.py` 582–606).
  `core.get_option('SCF', key)` returns the global value when the local one is unchanged
  (`psi4/src/psi4/liboptions/liboptions.cc` 772–800; `psi4/src/core.cc` 992–1012). `has_option_changed` reports a
  changed global the same way (`core.cc` 873–880). `BASIS` and `SCF_TYPE` are read by the driver as globals.
- **Basis lookup.** The search path is the working directory, then `PSIPATH`, then `<datadir>/basis`
  (`psi4/driver/qcdb/libmintsbasisset.py` 792–805). The first match is loaded (`libmintsbasisset.py` 916–925;
  `psi4/driver/qcdb/psiutil.py` 76–91). `<datadir>` is `PSIDATADIR` if set, otherwise the installed `share/psi4`
  (`psi4/__init__.py` 59–68). The fresh empty scratch and the absent `PSIPATH` and `PSIDATADIR` leave only
  `<PREFIX>/share/psi4/basis`, and I3 checks the resolved path and digest.
- **Guess.** `GUESS` defaults to `AUTO` (`read_options.cc` 1505), which becomes `SAD` for more than one atom
  (`proc.py` 1884–1888). The explicit `CORE` avoids that rule.
- **`scf_type direct` with `df_scf_guess false`.**
  - The global `SCF_TYPE` default is `PK` (`read_options.cc` 194), and `run_scf` switches an unchanged one to `DF`
    (`proc.py` 2756–2758); the explicit `DIRECT` avoids both.
  - `DF_SCF_GUESS` defaults to true (`read_options.cc` 1481). With `DIRECT` it runs DF pre-iterations
    (`psi4/driver/procrouting/scf_proc/scf_iterator.py` 62–80) and builds a JKFIT basis (`proc.py` 1452–1466).
  - With `false`, the wavefunction gets a zero auxiliary basis (`proc.py` 1468). Under `DIRECT` the JK builder
    passes no auxiliary basis ([SOURCE-RESOLUTION §8](../../../ms-001/SOURCE-RESOLUTION.md#8-psi4-compiled-steps-and-fitting-bases)).
- **Convergence.**
  - `E_CONVERGENCE` and `D_CONVERGENCE` default to 1e-6 (`read_options.cc` 1544, 1551). Explicit values are kept,
    because `negotiate_convergence_criterion` changes only unchanged options (`psi4/driver/driver_util.py` 40, 75–83).
  - Convergence requires \|ΔE\| < `E_CONVERGENCE` and `Dnorm` < `D_CONVERGENCE` (`scf_iterator.py` 929–935).
  - For RHF, `Dnorm` is the RMS, when `DIIS_RMS_ERROR` is true (its default, `read_options.cc` 1573), otherwise the
    maximum absolute value, of `FDS − SDF` transformed by the orthogonalizer
    (`psi4/driver/procrouting/scf_proc/subclass_methods.py` 24–46; `psi4/src/psi4/libscf_solver/hf.cc` 1412–1422).
    The option text says the same (`read_options.cc` 1545–1550), and the iteration header prints `RMS |[F,P]|`
    (`scf_iterator.py` 255–261).
  - So in v1.11 source `D_CONVERGENCE` tests the orbital gradient, a commutator residual, not a density-matrix change.
- **Iteration limit.**
  - `MAXITER` defaults to 100 in the SCF module (`read_options.cc` 1538); the explicit 50 replaces it.
  - The convergence check precedes the limit check, and `iteration_ ≥ MAXITER` raises `SCFConvergenceError`
    (`scf_iterator.py` 581–609). With `FAIL_ON_MAXITER` true (default, `read_options.cc` 1540) the error propagates
    (`scf_iterator.py` 85–97).
  - The driver classifies a recorded count of 50 or more as FAILED even when converged. Failing closed, it does the same
    for a finite raw reported count of 50 or more, independently of whether the recorded count matches the raw value.
- **Molecule.**
  - The payload builds the molecule with `core.Molecule.from_dict` (`psi4/src/export_mints.cc` 228–328): units `Bohr`
    (246–251), frame settings from `fix_com`, `fix_orientation` and `fix_symmetry` (254–256), labels as upper-case
    element plus label suffix (292–300).
  - This avoids `geometry()` and `from_arrays`, which parse through qcelemental (`psi4/driver/molutil.py` 157, 285).
    Basis construction still passes the molecule through `Molecule.to_dict` (`psi4/driver/p4util/python_helpers.py`
    169; bound at `psi4/driver/molutil.py` 250), which calls qcelemental (`psi4/driver/qcdb/molecule.py` 1662, 1711).
    I3 checks the effect of that call: the resolved basis file, its digest and `nbf = 2`.
  - `energy()` calls `molecule.update_geometry()` (`psi4/driver/driver.py` 445–446).
  - Read-backs: `natom`, `multiplicity`, `x/y/z` in bohr (`export_mints.cc` 885–910), `symbol`, `label` (933–944),
    `molecular_charge` (947), `nuclear_repulsion_energy` (1002–1003), `schoenflies_symbol` (1023), `units`
    (1058–1064), `com_fixed` and `orientation_fixed` (878–879).
  - Types, a source-level reading (the runtime type is not observed): `molecular_charge` and `multiplicity` are `int`
    (`psi4/src/psi4/libmints/molecule.h` 128, 644, 646, 650; `export_mints.cc` 230, 887, 947), while `Z` is a double
    (`molecule.h` 260; `export_mints.cc` 904). The payload's electron count, `round(ΣZ) − charge`, is therefore an
    integer, and the driver requires exact integers for these three fields.
- **Threads.** `set_num_threads` sets the engine thread count and calls `omp_set_num_threads` when compiled with
  OpenMP; otherwise it forces 1 (`psi4/src/core.cc` 1029–1044; `psi4/src/psi4/libpsi4util/process.cc` 64–67). Import
  sets 1 (`psi4/__init__.py` 96).
- **Memory.**
  - `set_memory('500 MiB')` parses binary units to 524 288 000 bytes and stores them as the engine setting only
    (`psi4/driver/p4util/util.py` 185–210, 220; `core.cc` 1019–1025).
  - The code minimum is 262 144 000 bytes (250 MiB) (`util.py` 212–217), while the docstring says "<500MiB"
    (`util.py` 144). The two disagree, and 500 MiB satisfies both.
- **Reported energies.**
  - `RHF::compute_E` adds `nuclearrep_` into the total, alongside the one- and two-electron terms
    (`psi4/src/psi4/libscf_solver/rhf.cc` 308–366).
  - `scf_print_energies` sets `NUCLEAR REPULSION ENERGY` and `SCF ITERATIONS` on the wavefunction (`scf_iterator.py`
    851, 878). Scalar variables are stored and returned as doubles (`psi4/driver/p4util/python_helpers.py` 1330;
    `psi4/src/psi4/libmints/wavefunction.h` 246, 666). The payload keeps the raw value and records the count as an
    integer only when that double is finite and integral, otherwise as null, which the driver quarantines.
  - `scf_helper` sets `SCF TOTAL ENERGY` and `CURRENT ENERGY` to the SCF energy (`proc.py` 2047–2051), and `energy()`
    returns `CURRENT ENERGY` (`driver.py` 553–555).
  - In v1.11 source the returned total therefore includes nuclear repulsion. Whether the installed build does so stays
    OPEN (P4), and the payload derives no `E_elec`.
- **Banner.**
  - `set_output_file(…, print_header=True)` prints the header and an `Addons:` line (`psi4/extras.py` 310–314) and
    attaches a `.log` handler (289, 305–306).
  - The header carries the version and release, start time, process ID, host name (`socket.gethostname()`),
    `PSIDATADIR`, memory and threads (`psi4/header.py` 89–140).
  - `core.print_out` flushes on every call (`core.cc` 558–564), so I2 reads the banner back at once. The banner is
    private raw evidence.
  - The installed `header.py` was not statically compared (§10).
- **Files written.**
  - In `<RUNS_ROOT>/H2-A-01/payload/`: the output file, its `.log`, and the stage and result records.
  - In the scratch, which is also the working directory: `timer.dat` (`psi4/src/psi4/libqt/timer.cc` 1025–1027),
    `psi.<pid>.clean` (`filemanager.cc` 174, removed at 232), and scratch files named `psi.<pid>.<namespace>.<unit>`
    (`filemanager.cc` 88), removed by `core.clean` at exit (`psi4/__init__.py` 87–90).
  - The driver inventories every file in the attempt directory with its size and SHA256.
- **Relied-upon defaults** (`read_options.cc`): `PUREAM` true (138); `INTS_TOLERANCE` 1e-12 (1502);
  `S_ORTHOGONALIZATION` `AUTO` (1495); `S_TOLERANCE` 1e-7 (1497); `DIIS` true (1582); `DIIS_START` 1 (1575);
  `DIIS_MAX_VECS` 10 (1580); `SCF_INITIAL_ACCELERATOR` `ADIIS` (1632); `DAMPING_PERCENTAGE` 0 (1557);
  `LEVEL_SHIFT` 0 (1584); `MOM_START` 0 (1588); `STABILITY_ANALYSIS` `NONE` (1620); `BASIS_GUESS` false (1566);
  `SCF_SUBTYPE` `AUTO` (1489); `ORBITAL_OPTIMIZER_PACKAGE` `INTERNAL` (197–200).
  - `[AGENT]` reading: `PUREAM` and the basis file's `spherical` header do not change two s functions. I3 checks
    `nbf = 2`.
  - The SCF also runs one-electron properties after the energy by default (`proc.py` 2054–2056).

**Development manual [48].** It is not authoritative for the installed build. Two caveats are preserved:
- its displayed Fock matrix adds exchange while the energy subtracts it, and its density-matrix energy has no factor
  one half;
- its prose names a density-matrix change for `D_CONVERGENCE` while its output column reads `RMS |[F,P]|`.

The v1.11 source above resolves the second point for the tagged source only.

## 8. Enforcement and limits

1. **Memory.**
   - The engine setting (524 288 000 bytes) is read back at I2. No operating-system memory limit is applied.
   - Whether such a limit is enforceable on this platform is not established here.
   - The driver records the direct child's `ru_maxrss` from `wait4` as an observation. Its unit is platform-defined,
     and it does not include descendants that the child did not wait for.
   - This is conditional gate **M1**.
2. **Threads.** One engine thread is set and read back, and `OMP_NUM_THREADS=1`. Threads of other libraries (BLAS)
   are not verified.
3. **Wall clock.**
   - The bound is 300 s by the monotonic clock. At expiry: SIGTERM to the process group, 5 s grace, SIGKILL.
   - The driver then verifies that no group member remains, recording it in `outcome.json`.
   - Tested with a child and a grandchild that both ignore SIGTERM.
4. **Process cleanup.**
   - Group signals reach only processes still in the group. A process that calls `setsid` or `setpgid` escapes them
     and is neither detected nor killed.
   - Members left after a normal exit are killed and the run is quarantined.
5. **Network and installation: conditional gate N1, unresolved.**
   - **(1) Accepted language,** quoted from [h2-method-parameters.json](../h2-method-parameters.json):
     - `stop_conditions`: "any network access or installation attempt";
     - the rule "stop the sequence, keep all output, mark remaining points NOT_RUN, change no setting";
     - P5: "no network access".
   - **(2) What is established.**
     - *Driver.* It applies no network control. `network.prerequisite` fails with `NETWORK_PREREQUISITE_UNRESOLVED`
       unless reviewed driver code supplies an observer function (`NETWORK_OBSERVER`, `network_gate()`). A field in
       the authorization cannot satisfy it. Tests cover the gate's decisions with injected observers.
     - *Installation half.* `-B` asks for no bytecode writes. The driver compares the set of §8.6 before and after
       the run and re-runs every identity check after it (QUARANTINE on any change or failure). This is tested with a
       fixture that adds a record and with one that changes `build_number` inside the existing Psi4 record without
       renaming it.
     - *Installed primary documentation* [55]:
       - sandbox-exec(1) marks `sandbox-exec` DEPRECATED and documents only its options.
       - sandbox(7) states that "New processes inherit the sandbox of their parent" and that restrictions apply when
         resources are acquired, so open descriptors stay usable.
       - The SDK `sandbox.h` (lines 22–85) documents the deprecated `sandbox_init` API, "No longer supported" from
         macOS 10.8, with named profiles whose stated intents include "All sockets-based networking is prohibited"
         (65) and "File system writes are prohibited" (70).
     - *Fixture demonstrations* [55], around a fake non-engine client only. Under a candidate custom profile, with the
       same operations succeeding in unsandboxed controls:
       - AF_UNIX connect and bind and a TCP connect to `127.0.0.1` were refused with EPERM, by the client and by its
         grandchild;
       - a write bound refused file creation outside one directory.
   - **(3) Remaining gap,** stated concretely.
     - The driver applies no control, so nothing prevents or detects network access during a run.
     - The candidate profile's operation semantics, which `sandbox-exec -p`/`-f` would use, are not documented in any
       installed source.
     - Refusal is not detection, so the run would not "stop" on an attempt.
     - Traffic to other destinations, other socket types and traffic mediated by system services outside the
       sandboxed process were not tested.
     - The engine binary's behaviour under a profile is unobserved.
     - Installation attempts outside the compared prefix set are not detected.
     - Two endpoint samples of host state would show two instants only, never continuous behaviour.
   - **Resolution paths, none included in this package.** Each needs revised driver (and profile) bytes, a renewed
     independent review and then a person's decision on the exact revised bytes:
     - **R1:** apply a bound `sandbox-exec` profile as prevention, and add a detection record whose semantics are
       established from a citable source.
     - **R2:** a person decides, as a method revision, that prevention by a bound profile without detection is
       accepted in place of the quoted stop condition.
     - **R3:** a driver-observed offline host state before launch and after the end, accepted by a person as a
       two-instant observation.

     None of these relaxes the accepted method unless a person decides it (R2, R3).
6. **Installation detection: the compared set and its limits.**
   - **Compared** before launch, immediately before launch and after the process ends:
     - the names of all `conda-meta/` entries;
     - the full-file SHA256 of the two bound package records, `psi4-1.11-py314h53d0584_1.json` and
       `libint-2.13.1-h5a0831b_0.json`, and their declared fields;
     - the SHA256 of the five bound files (interpreter, core extension, `libint2.dylib`, `shell.h`, `sto-3g.gbs`);
     - the SHA256 of the bundle files in the repository.
   - **Not compared:**
     - the content of any other package record (names only);
     - any other file in `<PREFIX>`;
     - anything outside `<PREFIX>` and the bundle;
     - downloads held in memory;
     - changes made and reverted between two samples.

     An installation attempt that touches only those is not detected. The `sandbox-exec` write bound is not applied
     (N1).
7. **Disk.**
   - Launch requires at least 2 GiB free on the runs-root file system, an `[AGENT]` floor. Free space is recorded
     before and after.
   - Output size is not bounded, only measured. The runs root must lie outside `<PREFIX>`, and inside the repository
     only under the ignored `.herd/` tree.
8. **Interlock.** The authorization check compares bytes and fields. It cannot show that a person authorized
   anything.

## 9. Provenance (evidence policy §4)

| Field | Recorded by | Missing → tier |
|---|---|---|
| Code identity | A detached code-provenance record written by `code-provenance` after the final bytes. It carries the repository base commit (HEAD) and, for each code path the run uses (driver, payload, input, parameter file, static identity record), the base presence and Git blob id, the full unified diff from the base to the current bytes with its SHA256, and the current bytes themselves; it states its coverage and what it does not cover. The authorization binds its SHA256. Before launch the driver re-derives the record with read-only Git queries and blocks unless it is identical, which checks base blob ids, diffs and current bytes mechanically. The record is copied into the attempt (`code-provenance.json`) and summarized in the launch record. The proposal, decision packet and machine binding are bound by SHA256 in the authorization. No public file embeds the record's digest, so there is no digest cycle | BLOCK_LAUNCH when absent, mismatched or unresolvable; QUARANTINE if the preserved copy is missing after a run |
| Configuration | input file, I2 option read-backs, relied-upon defaults (§7), launch record | STOP_BEFORE_ENERGY / QUARANTINE |
| Software version | static identity record, preflight digests, I1 version and loaded images, banner bytes and SHA256 (private) | BLOCK_LAUNCH / STOP_BEFORE_ENERGY / QUARANTINE |
| Coordinates and atom identifiers | input atom map; I2 and post-energy read-backs in bohr; nuclei fixed | STOP_BEFORE_ENERGY / QUARANTINE |
| Calculation performed | method, basis, charge, multiplicity, electrons at I2 and I3; wavefunction class after energy | STOP_BEFORE_ENERGY / QUARANTINE |
| Random seed | none: no stochastic component is configured | — |
| Hardware and environment | private machine binding (OS, architecture, processor, memory); launch environment; P0 observed environment | BLOCK_LAUNCH / STOP_BEFORE_ENERGY |
| Outputs and hashes | `outcome.json` inventory of every attempt file (size, SHA256); reported total energy, reported nuclear repulsion, iterations and convergence, each separately | QUARANTINE |
| Failure record | exit or signal, timeout, cleanup, stop or failure records, free space; nothing overwritten | FAILED / QUARANTINE |
| Review record | independent review of the result with file digests; this package's review record | result not admissible until present |

A completed run is `COMPLETED_PENDING_REVIEW`. Its values would be `[COMP-PRED]` only after complete provenance and
independent review (evidence policy §2).

## 9a. Driver re-checks of the payload's records

The driver re-checks each gate-defining value the payload records against the launch record (bound environment,
command, interpreter and prefix realpaths, scratch, static digests) or the input and parameter file. Fields that are
recorded but not re-checked are listed with the reason.

| Record | Re-checked against a binding | Recorded only (reason) |
|---|---|---|
| P0 `pre-import` | `environ`: exactly the bound environment's names and values, plus at most the declared platform name; `argv` equals the bound command's payload arguments; `executable_realpath` and `prefix_realpath` equal the bound realpaths; `cwd` equals the bound scratch; `isolated` and `dont_write_bytecode` are 1; `engine_modules_loaded_before_import` empty; `static_sha256` has exactly the five re-hashed files, each equal to its bound digest | `sys_path`, `sys_executable`, `sys_version`, `pid`: interpreter descriptors and a process id that cannot be bound in advance; the interpreter's identity is checked through its realpath and static digest |
| I1 `i1-identity` | `version` equals 1.11; `module_file`, `core_file` and `datadir_realpath` equal `<PREFIX>/lib/python3.14/site-packages/psi4/__init__.py`, the core extension path and `<PREFIX>/share/psi4`; `loaded_images` non-empty, every entry well-formed; the core extension present at its bound path with its bound digest; every `libint2*` image at `<PREFIX>/lib/libint2.dylib` with its bound digest | loaded images outside `<PREFIX>`, by name only: operating-system libraries are not bound |
| I2 `i2-configuration` | options; every option marked as changed; threads; memory set and read back; banner digest and byte length; banner program line, version line, `PSIDATADIR` inside `<PREFIX>`, thread and memory lines; charge 0, multiplicity 1, electrons 2 and atom count 2 as exact integers; units `Bohr`; point group `c1`; centre of mass and orientation fixed; atom labels, symbols and coordinates within tolerance | the other banner lines (start time, process id, host name): not bindable, and private |
| I3 `i3-basis-geometry` | the basis file path equals `<PREFIX>/share/psi4/basis/sto-3g.gbs`, with its bound digest; no `.gbs` file in the working directory; two basis functions; nuclear repulsion within 1e-10 of 1/R | `basis_message`: the engine's text from which the path was parsed; the parsed path and the file digest are checked |
| `result` | job, stage and energy call; engine version; converged; finite total energy; reported nuclear repulsion against 1/R; `scf_iterations` a positive integer equal to `scf_iterations_raw`; the limit of 50 checked on the integer count and on the raw value independently of that equality; energy call time not after return time; post-energy read-back (wavefunction class `RHF`, two basis functions, `nalpha = nbeta`, two electrons, two atoms with labels and coordinates, options); banner preserved; output and `.log` files listed and present | `reported_total_energy_source`, `converged_basis`: descriptive strings; `post_energy_error`: its presence gives QUARANTINE |
| stop record | known stage; earlier stages passed; the stopping stage's record, if written, carries the same problems; no later stage record | — |

What no record can show remains outside these checks: the engine's in-memory state, and native side effects of import
and start-up (§6).

## 10. Gaps and missing sources

The following are not established in this package:
- CPython documentation for `-I`, `-B` and `sys.flags` (not cached).
- The dyld image API, through `ctypes`, used for the loaded-image list (not cached).
- The `sandbox-exec` custom-profile language. Installed sources document only the deprecated named profiles of
  `sandbox_init` (SDK `sandbox.h`) [55].
- The installed `psi4/header.py` and `psi4/driver/qcdb/molecule.py`, which are not byte-compared with the tag. They
  were not on the authorized static-read list. The banner is checked from its output, and the effect of
  `Molecule.to_dict` at I3.
- qcelemental source (0.51.2 by the installed record [54]). It is not cached. It is not used to construct the
  molecule, but the basis-construction path calls it through `Molecule.to_dict` (§7). I3 checks its effect, while
  its semantics are not established here.
- Whether import-time code or plugins change Libint's normalization flag (P3).

None of these is filled by inference. A retrieval would need its own authorization.

## 11. Prerequisites P1–P9

| Id | Accepted status (unchanged) | What this package adds | What remains | Gate |
|---|---|---|---|---|
| P1 | OPEN | Static identity of the installed candidate equal to B2 §6 [54]; preflight re-check; I1 checks specified | Loaded identity at run time; source-to-binary correspondence | Run-time check (I1); correspondence unproved |
| P2 | PARTIAL | v1.11 source semantics and defaults of every option (§7) [52] | Behaviour of the installed build | Run-time read-back (I2, I3) |
| P3 | PARTIAL | Installed STO-3G bytes equal to the archive record and tagged source; H entry equal to [50] at 8 decimal places [54] | Normalization stays PARTIALLY ESTABLISHED ([SOURCE-RESOLUTION §6](../../../ms-001/SOURCE-RESOLUTION.md#6-basis-normalization-in-cp2k-and-psi4)) | Not settled by this package |
| P4 | OPEN | v1.11 source sums nuclear repulsion into the total (§7) | Meaning for the installed build | Shown only by an authorized run and its review |
| P5 | OPEN | Hashed driver, payload, input and atom map; exact invocation (§3); network gate; detached code-provenance record re-derived from Git before launch (§9) | No-network condition unresolved | **N1 blocks launch** |
| P6 | OPEN | Allow-list environment, thread and memory read-backs, wall bound, cleanup, free-space floor | No OS memory limit (M1) | Person accepts or resolves M1 |
| P7 | OPEN | Ten-field mapping (§9); exclusive records; stage and stop records; tests; gate-defining stage and result values compared with the bindings (§9a) and expected outputs required; post-run identity checks propagated | Records exist only after a run | Run |
| P8 | OPEN | — | This package's independent review is pending | Review |
| P9 | OPEN | Decision packet and blank template | No authorization exists | Person |

## 12. Gates

All gates are unchanged:
- W1 STOPPED (S10).
- E-01 technically BLOCKED and scientifically INDETERMINATE [21, 27].
- C3 readiness, MS-001 Stage 1 and option A BLOCKED.

H2 with `DIRECT` neither exercises nor diagnoses E-01's PK path. Phase B remains CONDITIONAL_NOT_AUTHORIZED: a
separate later decision, after an authorized Phase A run and independent review of its result.

## 13. References

Catalogued in [../../../SOURCES.md](../../../SOURCES.md):
- [21] and [27]: E-01 records.
- [31]: the Psi4 v1.11 archive.
- [39]: the B2 §6 declaration.
- [48]: the development manual.
- [50]: the BSE STO-3G hydrogen entry.
- [52]: the v1.11 tagged-source files cited here.
- [53]: the declared-archive path records.
- [54]: the installed static observation of 2026-10-10.
- [55]: the installed macOS sandbox documentation.
