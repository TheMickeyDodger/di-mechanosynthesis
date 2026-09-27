# C3 provenance wiring: data-model review, frozen field set and one trivial AiiDA job

Status: MS-001 Stage 0, scope option B, item C3 (spike §8.3; closure §8). **Reviewed partial demonstration; readiness
BLOCKED** on the prerequisite blockers listed at the end of Section 5 (independent review).

This record is software wiring evidence only. The job that ran adds two integers in bash. It demonstrates nothing
about chemistry, energies, forces or gradients, and nothing about the readiness of any scientific method, engine or
coupling route. No quantum-chemistry, semi-empirical or force-field engine was installed or run.

Source identifiers `[S0-…]` are listed in Section 6 with their version and digest.

## 1. Environment

The environment is project-local and reversible. It is a virtual environment created from an existing CPython
3.12.14 interpreter, with package caches, temporary files and the AiiDA configuration kept under a git-ignored
project directory. Nothing was installed system-wide or per user.

Filesystem confinement was **not** flawless. D1, below, wrote a user-level folder, and a few Stage 0 working files
were written outside the permitted project directory. These are disclosed in the private record. An earlier
basis-comparison attempt was superseded, and its record is retained.

| Item | Value |
|---|---|
| Operating system | macOS 15.6 (Darwin 24.6.0), arm64 |
| Python | CPython 3.12.14 |
| ASE | 3.29.0 (wheel SHA256 `7b9dd103f007810339c24acfee2f6b677c0c48443b21d3c98e52959246cf4ebf`) |
| aiida-core | 2.9.2 (wheel SHA256 `72ec503b427936a00a5b5d81ae7224b40e42065373e95def2795ccecded77bdd`) |
| NumPy | 2.5.3 |
| Resolved set | 88 distributions, installed with pip `--require-hashes` from a local wheelhouse. The hash-locked requirements file has SHA256 `813b2d9adc6c986626f8a84373b91ae2be0bd9157d7547f9bc43d1a4a6ed80b8`; `pip check` reported no broken requirements |
| AiiDA profile | Created by `verdi presto --no-broker`: SQLite storage (`core.sqlite_dos`), no message broker, and a `localhost` computer with the `core.local` transport and `core.direct` scheduler [S0-aiida-quick] |

Two deviations occurred during setup and the job. Both are recorded privately with exact commands and output.

- **D1, user-level AiiDA folder.** The first import of `aiida` ran before `AIIDA_PATH` was set, and aiida-core
  created an AiiDA configuration folder under the user's home directory, which the task forbids. The folder held
  only five empty directories and was created in the same second as the import. It was removed with
  empty-directory-only `rmdir`, a cleanup the user authorized for exactly that tree. Every later AiiDA use set
  `AIIDA_PATH` to the project-local directory first. A fresh import and a `verdi` call then confirmed that the
  folder was not recreated, and it was still absent after the job.
- **D2, login shell during the job.** The local transport ran its commands through a login shell, which is the
  aiida-core 2.9.2 default (`use_login_shell` defaults to true [S0-aiida-src-transport]). That shell printed an
  error from a user shell start-up file, and AiiDA logged it as a warning. The job's own scheduler stdout and stderr
  are empty, and the job finished normally. The environment of the job nevertheless depended on user start-up files
  that AiiDA does not capture. No further AiiDA command that could invoke the local transport was run.

## 2. Data-model review (EVIDENCE-POLICY §6)

For each field of [EVIDENCE-POLICY §4](../ms-000/EVIDENCE-POLICY.md#4-provenance-requirements-for-any-eventual-result-or-figure),
this section records which data model already carries it: ASE 3.29.0, aiida-core 2.9.2, or `aiida-cp2k` 2.1.1, the
CP2K plugin named in the MS-000 dependency set.

The docs.ase-lib.org pages retrieved for this review describe features added in ASE 3.30.0, so they are not matched
to the installed version. The ASE facts below therefore cite the installed 3.29.0 source files. The AiiDA facts cite
the version-pinned 2.9.2 documentation or installed source. Where a claim was measured in the job, Section 4 says
so; everything else in this section is a documentation or source reading.

| §4 field | ASE 3.29.0 | aiida-core 2.9.2 | aiida-cp2k 2.1.1 |
|---|---|---|---|
| Code identity | Not carried | Each process node stores a `version` attribute holding the aiida-core and plugin versions (observed in the job: `core` 2.9.2, `plugin` 2.9.2). The commit and uncommitted diff of the driver scripts are not carried | Not carried beyond the plugin version |
| Configuration | Not carried | A calculation job stores the exact files it wrote for submission (input file, submit script and job description) in its node repository [S0-aiida-calc-usage; S0-aiida-repository]. Engine defaults the job relies on are not enumerated anywhere | The engine input is generated from a `parameters` Dict node plus optional `settings`, `file`, `basissets` and `pseudos` inputs [S0-aiida-cp2k-src, lines 62–131]. Defaults are not enumerated |
| Software version | Not carried | aiida-core and plugin versions, as above. Engine banners are captured only if the engine output is retrieved. Package digests are not carried | `aiida.out` is in the default retrieve list [lines 396–404]. The parser reads a version number from the `CP2K\| version string:` line [S0-aiida-cp2k-parser, lines 44–46]. Compiler, BLAS, LAPACK and MPI identities are not extracted |
| Input coordinates and atom identifiers | `Atoms` carries positions in Å, cell, periodic flags, symbols, tags, arbitrary per-atom arrays and an `info` dictionary. The extxyz writer always saves the periodic flags [S0-ase-src-extxyz, line 796]. `FixAtoms` and `FixCartesian` are written as a `move_mask` column and read back as constraints [lines 494–502, 805–819]. Units are not written; the program's files state them in a header key | `StructureData` stores cell, periodic flags and sites as kind names and positions, with Å as the default unit [S0-aiida-data-types, "StructureData"]. `set_ase` reads the cell, the periodic flags and each atom [S0-aiida-src-structure, lines 808–818], and an ASE tag becomes part of a kind name [lines 2025–2027]. The source contains no path that reads other per-atom arrays or constraints; see Section 4 for what was measured | The structure is written as XYZ from `StructureData.get_ase()`, with kind names formed from the symbol and the tag [S0-aiida-cp2k-src, lines 275–300, 431–436, 452–462]. Fixed atoms can only be given in the `parameters` Dict |
| Calculation performed | Not carried | Not carried as semantic fields. Only the stored input files and nodes record what was run | Method, partition, charge, spin, constraints and motion settings exist only inside the `parameters` Dict and the generated input. Drive bookkeeping (branch, step index, imposed z) is not carried |
| Random seed | Not carried | Not carried | Not carried (part of `parameters` if set) |
| Hardware and environment | Not carried | The Computer node records its label, host name, transport, scheduler and work directory. Job options record resources, environment variables and prepend text [S0-aiida-calc-usage, options list]. Operating system, CPU and memory are not recorded | As aiida-core |
| Outputs and hashes | Not carried | Retrieved files are stored in a `FolderData` node. The default repository backend keys every object by its SHA256 (`hash_type` default `sha256` [S0-aiida-src-container, line 310]; checked in [S0-aiida-src-dos, line 145]). Each node also gets a content hash computed from its attributes, package version, repository content and computer, plus the hashes of its inputs for process nodes [S0-aiida-caching, "How are nodes hashed"]. Extras are not in that list | `output_parameters` is a Dict that carries its own units convention (`energy_units: "a.u."` [S0-aiida-cp2k-parser, lines 24, 50]). Other outputs are optional nodes |
| Failure record | Not carried | A process records `exit_status` (zero for success) and `exit_message` [S0-aiida-processes-usage, exit codes], and log records are attached to the node. Stored nodes accept no modification [S0-aiida-data-types, BandsData note] | Defines its own exit codes |
| Review record | Not carried | Not carried. The review record belongs to the orchestration layer (EVIDENCE-POLICY §7) | Not carried |
| Retained per claim | `info` could hold labels | Extras can hold labels but lie outside the node hash | Not carried |

## 3. Frozen MS-001 provenance field set

The §4 fields are frozen for MS-001 as follows. A job whose record lacks any row is reported as incomplete, and the
`[COMP-PRED]` label is blocked (spike §8.5). The "Carrier" column reflects the review in Section 2. "Extension"
means that neither data model carries the field and the program must attach it. Every extension is a declared
requirement, not a demonstrated capability.

| # | Field | Frozen content | Carrier |
|---|---|---|---|
| F1 | Code identity | The repository commit. The **full tracked diff bytes** (`git diff --binary` against that commit), retained and resolvable, with their SHA256. The **full contents of every untracked source file** the job used, retained and resolvable, with each file's SHA256. The SHA256 of every driver script. The aiida-core and plugin versions. Hashes and byte counts alone do not satisfy F1 | Native for versions. Extension for the rest: the diff bytes and untracked-file contents must be retained as input nodes of each job, so that they resolve from the provenance store by digest |
| F2 | Configuration | Every file the engine consumed, by SHA256; the parameter nodes; an enumerated list of the engine and plugin defaults relied upon, for the exact versions | Native for files and nodes; extension for defaults |
| F3 | Software version | Name, version and build identity of every engine and library; the engine's printed banner; the SHA256 of the environment lock file | Native in part (plugin version, retrieved banner); extension for build identity and the lock digest |
| F4 | Input coordinates and atom identifiers | Coordinates with units; cell and periodicity; element symbols; the stable `atom_id` map; the fixed-atom set by `atom_id` | Native for coordinates, order, cell and periodicity. Extension, as a separate node that travels with every job and is checked site by site, for the identity map, the fixed-atom set and explicit units |
| F5 | Calculation performed | Method and levels; partition, embedding and link definition; charge; multiplicity; constraints; drive branch, step index and imposed z; optimizer and its settings | Engine input for most items; extension for the drive bookkeeping and the declared scheme |
| F6 | Random seed | The seed, or "none" | Extension |
| F7 | Hardware and environment | Host (private only); operating system; architecture; CPU; memory; environment variables that affect numerics; environment identity. The computer must be configured without a login shell and the environment declared explicitly (D2) | Native for the Computer and job options; extension for the rest |
| F8 | Outputs and hashes | Every output file by SHA256; extracted quantities with units; figures with their data files | Native for files; extension for units where the plugin does not state them |
| F9 | Failure record | Every failed, aborted or non-converged job, with exit status, message and logs, never deleted | Native |
| F10 | Review record | Reviewer role, reviewed file digests, canonical decision, round | Orchestration layer, linked by digest |
| F11 | Retained per claim | Units, atom identity, charge and spin, constraints, environment, tool state and evidence class | Extension |

Host names, local paths and user names are recorded only in the private record. Public records carry digests.

## 4. The job and its evidence

One calculation job ran: `core.arithmetic.add`, the integer-addition calculation that ships with aiida-core. It
used `/bin/bash` as its code on the `localhost` computer, with inputs `x = 2` and `y = 3`, and was driven by
[`tools/c3_provenance_wiring.py`](../../tools/c3_provenance_wiring.py) (SHA256
`d3d8b58e06f7ffff23934bec550b927586effad9c175e9a3451096bb8fbb3d17`).

- **Job options.** The job declared `OMP_NUM_THREADS=1`. Its prepend text wrote a context file and an "engine
  banner" file, and both were retrieved.
- **Context file contents.** The context file holds:
  - the repository commit and the diff and untracked-file digests, as values;
  - the software versions and the lock digest;
  - `random_seed=none`;
  - the operating system, CPU model, core count and memory size.
- **Surrogate data nodes.** Beside the job, three data nodes were stored, none of them an input of the job: the
  activated-tool extxyz file as a `SinglefileData`, a `StructureData` converted from it, and a `List` of its 48
  `atom_id` values.

Result: process state `finished`, exit status `0`, output `sum = 5`. At the time of the job the repository was at
commit `195a788022830559a5f63b3f83a61f630cd64789`, with an empty tracked diff and one untracked file, the driver
script. Node identifiers are kept in the private record. Public identification is by content:

| Node | AiiDA node hash | Repository files (SHA256; every storage key equals the file's SHA256) |
|---|---|---|
| Calculation job | `8f4f85c976a3918e74bbd9e2bd002e17e04c145bc3100a88bef98855c1786170` | `aiida.in` `27d98676e1756e773eaa59a4edb19e9d8d1364a893a7851d5bd048fdc5d0d622`; `_aiidasubmit.sh` `b7f501e15e7beea99c5905c9d958da833cb675b04e2331ae9fd9dc4e92302082`; `.aiida/calcinfo.json` `c68a4253ebf2f4c4701c645f2ddb916dfc206319e5efe8675b636aa7bd72e3eb`; `.aiida/job_tmpl.json` `f3f4114c99deddb5ab61e5961695895281cf8b037a2b83654addfa50b12abdb7` |
| Retrieved files | `7e48e3f0aecc108394907f29b71436a940a0681e6bd20886c8bcb54d26034df2` | `aiida.out` `f0b5c2c2211c8d67ed15e75e656c7862d086e9245420892a7de62cd9ec582a06`; `engine-banner.txt` `fc1e2d06772f7b7924bf684fb3a65d7b142cc31c965e927060e0733312e96788`; `provenance-context.txt` `3e2f68581e8b89b7cda263ae0a9ac759d18b8bac702423e145b1bc72bd907313`; scheduler stdout and stderr both empty, `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| Inputs `x`, `y`; output `sum` | `caf03818…d230b2`, `c4b85179…faed`, `f2fd5633…1f0a` | None |
| Code | `ada2406b75d96d29874ed6c2a8fdc26f703be7111710b51954c18cb7ae3117f8` | None |
| Surrogate `SinglefileData` | `161c4140ad2d10a483155ca842fe805cad26ed6fdaf5a4d5a4698255eedcf363` | The activated-tool file, `bb7ab3443a99fcdfe47df6a928a07cc45cdd531299051727a5b160493c9186e3` |
| Surrogate `List` of atom ids | `5bdc3cf8a80cf0b39f1deee532aad47baca1b06c1262f1a31f512ff7b48fa9ae` | None |
| Surrogate `StructureData` | `39138de55099f951c09ed2938e46f14796758987e6e8267b65a892cd8838b065` | None |

What the AiiDA `StructureData` round trip measured, and only this:

- The 48 sites kept their symbols, their order and their coordinates exactly (largest absolute position difference
  0.0 Å), and kept the non-periodic flags. That is a coordinates-and-order result only.
- The stable atom-identity map was not carried: the `atom_id` per-atom array was absent after the round trip.
  `StructureData` does not preserve atom identity.
- Whether `map_num` and `radical_electrons` survive the conversion was not inspected or recorded, so their survival
  through the AiiDA conversion is not measured `[GAP]`. No inference is made either way.

A separate test, not involving AiiDA, wrote the same activated-tool file with ASE 3.29.0 and read it back.
`atom_id`, `map_num`, `radical_electrons`, `positions` and `numbers` all survived with equal values, as did the
header keys and the periodic flags. This is an ASE file-I/O fact. It says nothing about AiiDA. (The private log has
SHA256 `9835fe3e57ae526b925dabb890374cc3c2bd3f11e461d76c967f14b24fa66fa8`.)

## 5. Coverage table

Each §4 field has exactly one disposition:

- **Demonstrated on the trivial job:** carried by the job's own nodes.
- **Demonstrated by surrogate:** attached by the driver, or carried by nodes that are not part of the job's
  provenance chain.
- **Not demonstrated:** with the reason, marked `[GAP]`.

"Unverified for a real engine job" lists what this test cannot establish.

| §4 field | Carrier | Disposition | Unverified for a real engine job |
|---|---|---|---|
| Code identity | The job's `version` attribute (aiida-core 2.9.2, plugin 2.9.2), plus the commit, diff and untracked-file digests and the driver SHA256, written into the retrieved, hashed `provenance-context.txt` and into job extras | Demonstrated by surrogate, as digests only. At the time of the job the tracked diff was empty (0 bytes), and the one untracked file was the driver, whose bytes are published with the same SHA256. The dirty state is therefore resolvable outside the job record, but the job record did not retain the bytes that the frozen F1 requires | `[GAP]` Retention of the full diff bytes and untracked source contents as job inputs; the identity of CP2K and xtb builds |
| Configuration | The job's repository: the exact input file and submit script, stored under SHA256 keys equal to their content digests | Demonstrated on the trivial job | `[GAP]` Enumeration of engine and plugin defaults; `aiida-cp2k` input generation from a `parameters` Dict is untested |
| Software version | `version` attribute; `engine-banner.txt` (the bash banner) retrieved and hashed; lock-file SHA256 in the context file | Demonstrated by surrogate | `[GAP]` The CP2K banner and build identity (compiler, BLAS, LAPACK, MPI) through `aiida-cp2k`; the GFN0 parameter provenance required by P1 |
| Input coordinates and atom identifiers | `StructureData` (coordinates and order only); separate `List` and `SinglefileData` nodes for identity | Demonstrated by surrogate, for identity only. `StructureData` preserved the symbols, order, coordinates and non-periodic flags of the 48 sites exactly, but not the `atom_id` map, which was absent after the round trip. Identity is carried only by the separate `List` and `SinglefileData` nodes, which are not inputs of the job and do not travel with `StructureData` through a calculation chain | `[GAP]`/`UNVERIFIED` Survival of the identity map across every step of a real job chain; survival of `map_num` and `radical_electrons` through the AiiDA conversion, which was not measured; carriage of the fixed-atom set. Closing these is a declared extension requirement (F4), not a demonstrated capability |
| Calculation performed | No method-bearing engine ran; the job's input file records only integer addition | Not demonstrated `[GAP]`: no method, partition, charge, spin, constraint or drive field exists in a trivial job, and running an engine is outside Stage 0 | Every F5 item through `aiida-cp2k`, the coupling route and the drive bookkeeping |
| Random seed | `random_seed=none` in the retrieved context file and in job extras | Demonstrated by surrogate | `[GAP]` Seeds of stochastic components, if any, in the real engines |
| Hardware and environment | Computer node (`localhost`, `core.local`, `core.direct`); job option `OMP_NUM_THREADS=1`; OS, architecture, CPU model, core count and memory size captured by the job into the retrieved context file | Demonstrated by surrogate | `[GAP]` The environment dependence on user login-shell files (D2) is not captured by AiiDA. F7 requires a computer configured without a login shell and an explicitly declared environment, which was not tested |
| Outputs and hashes | Retrieved `FolderData`; every repository key equals the file's SHA256 (independently recomputed); output node `sum` | Demonstrated on the trivial job | `[GAP]` Units of extracted quantities depend on plugin conventions (`aiida-cp2k` uses an `energy_units` key), untested |
| Failure record | `exit_status`, `exit_message`, process state and log records on the job node | Not demonstrated `[GAP]`: only one job ran and it succeeded (exit status 0), so preservation of a failed job was not shown. The documented carrier is cited in Section 2 | Preservation of failed and non-converged engine jobs |
| Review record | None in AiiDA | Not demonstrated `[GAP]`: outside AiiDA by design; held by the orchestration layer | Linking review decisions to job digests |
| Retained per claim | Job extras (evidence class, seed) | Not demonstrated `[GAP]`: no claim exists for a trivial job, and extras lie outside the node hash | The F11 record for every Stage 2 claim |

**Disposition counts:** 2 demonstrated on the trivial job, 5 demonstrated by surrogate, 4 not demonstrated.

**Disposition of C3 (independent review).** C3 is a **reviewed partial demonstration**. The wiring of one
trivial job is shown. Complete provenance readiness is not, and C3 readiness is **BLOCKED**. The review confirmed
that only `x`, `y` and `code` are inputs of the calculation; the structure, atom-identifier list and file surrogate
are not linked to it. The following blockers are prerequisites to starting Stage 1. Closing them needs a new
wiring test, and that needs its own authorization: this review authorizes no further AiiDA execution.
1. **Identity-chain survival (F4).** A stable atom-identity node must be an input of every job and must be checked
   site by site against each structure along a chain of jobs. This has not been demonstrated: `StructureData` lost
   `atom_id`, the surrogate nodes were not inputs, and survival of `map_num` and `radical_electrons` through the
   conversion was not measured `[GAP]`.
2. **Remaining provenance extensions.** These have not been demonstrated:
   - retention of full diff bytes and untracked source contents as job inputs (F1);
   - enumeration of relied-upon defaults (F2);
   - build identity and the lock-file digest as job inputs (F3);
   - drive bookkeeping (F5) and the seed as an input (F6);
   - units for extracted quantities (F8);
   - the retained-per-claim record (F11).
3. **Login-shell environment gap (F7, D2).** A computer configured without a login shell, with an explicitly
   declared environment, has not been tested.

Preservation of a failed job (F9) is native to AiiDA and is expected to be shown by the first failed Stage 1 job;
that is a dependency within Stage 1. The review record (F10) stays with the orchestration layer.

## 6. Sources used by this record

Retrieved on 2026-09-26. The Stage 0 source ledger gives URLs, locators and retrieved-byte digests. Installed
source files are identified by their own SHA256 and by the digest of the wheel or source archive that contains them.

| ID | Source | Version |
|---|---|---|
| S0-aiida-quick | AiiDA documentation, quick installation guide (`verdi presto`) | 2.9.2 (version-pinned URL) |
| S0-aiida-data-types | AiiDA documentation, Topics, Data types | 2.9.2 |
| S0-aiida-calc-usage | AiiDA documentation, Topics, Calculations, Usage | 2.9.2 |
| S0-aiida-processes-usage | AiiDA documentation, Topics, Processes, Usage | 2.9.2 |
| S0-aiida-repository | AiiDA documentation, Topics, Repository | 2.9.2 |
| S0-aiida-caching | AiiDA documentation, Topics, Provenance, Caching and hashing | 2.9.2 |
| S0-aiida-src-structure | `aiida/orm/nodes/data/structure.py`, SHA256 `6079686947454367ba41591a24f2f371652934edc68fbe5bc5c3285b218940a8` | aiida-core 2.9.2 wheel |
| S0-aiida-src-transport | `aiida/transports/transport.py`, SHA256 `8fbc221847c7d60d410bbc173ad89a925090047699eda36072bdbaa71d464faf` | aiida-core 2.9.2 wheel |
| S0-aiida-src-dos | `aiida/repository/backend/disk_object_store.py`, SHA256 `9b9ff39326cf2af5cb09c95fad28f908f41b421f0d57c0c3b6e7b03c72dfb618` | aiida-core 2.9.2 wheel |
| S0-aiida-src-container | `disk_objectstore/container.py`, SHA256 `e1c185805c5c672a94b971f2208a96d8a6f0241bea0fb7f60f6630b685b06234` | disk-objectstore 1.5.0 wheel |
| S0-ase-src-extxyz | `ase/io/extxyz.py`, SHA256 `bae127796d6f89f6144733ade5ba8c44920ee182b1b0dae2a7c85de9feef277e` | ASE 3.29.0 wheel |
| S0-aiida-cp2k-src | `aiida_cp2k/calculations/__init__.py`, SHA256 `f2fbdf6096ebef8217e60f139498adb6ff69973e9047c68cf00996214f7f9d9b` | `aiida-cp2k` 2.1.1 source archive, SHA256 `a5f9dfd520628d59be4bc4a193597889b88c84daddf563c5b909fba23afb9876`, equal to the digest published on PyPI |
| S0-aiida-cp2k-parser | `aiida_cp2k/utils/parser.py`, SHA256 `3acda03cc5361de51167d2ef843ef4a77f0916fb17ef82057c12d3888259d45d` | same archive |
