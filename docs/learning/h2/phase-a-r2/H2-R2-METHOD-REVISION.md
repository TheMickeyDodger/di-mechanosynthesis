# H2 method revision R2: prevention in place of detection for job H2-A-01

## 1. Status

**PROPOSED. Human approval PENDING.** This is an `[AGENT]` proposal for a person's decision on these exact bytes. It
authorizes nothing, changes no accepted file and is not readiness. The accepted
[method specification](../h2-method-specification.md), [parameter file](../h2-method-parameters.json) and
[lesson](../lesson-01-fixed-separation-scf.md), and every file under [../phase-a/](../phase-a/), stay byte-identical
whatever is decided. Until a person approves these bytes and the later steps of §6 are completed, gate N1 stays in
force, and both the accepted driver and the route-R2 driver refuse every launch with `NETWORK_PREREQUISITE_UNRESOLVED`.

Route R2 is the route named in the accepted proposal ([H2-A-01-RUN-PROPOSAL.md §8.5](../phase-a/H2-A-01-RUN-PROPOSAL.md#8-enforcement-and-limits)):
a person decides, as a method revision, whether prevention by a bound profile, without detection, is accepted in
place of the quoted stop condition.

## 2. Scope

- **Applies to** Phase A job `H2-A-01` only, and only when it is launched by
  [h2_phase_a_r2_driver.py](h2_phase_a_r2_driver.py) `run`.
- **Does not apply to** Phase B (jobs `H2-B-01` to `H2-B-09`), to any other driver, to any other job, or to any
  attempt after the first. For all of these the accepted texts of §3 remain in force unchanged.
- **Unchanged for H2-A-01 as well:**
  - the rule "stop the sequence, keep all output, mark remaining points NOT_RUN, change no setting";
  - every other stop condition;
  - every setting of the parameter file;
  - one attempt and zero retries.

## 3. Accepted texts this revision would supersede for H2-A-01

| Id | File (SHA256) | Locator | Accepted text |
|---|---|---|---|
| A1 | [h2-method-parameters.json](../h2-method-parameters.json) (`2728b0efe2c6dae070346a3d0475857222f02864a6da63859edf4d4e334c156e`) | `stop_conditions`, ninth entry (line 219) | "any network access or installation attempt" |
| A2 | [h2-method-specification.md](../h2-method-specification.md) (`a8cb407a99d1a534dcb199c941888236e19af15b5f407edf761a6bdc1810001d`) | Stop conditions paragraph (line 83), the clause before "then stop the sequence" | "any network access or installation attempt" |
| A3 | h2-method-parameters.json (as A1) | `prerequisites`, P5 `title` (line 261) and `note` (line 263) | "Hashed driver, input and atom map, exact invocation, no network"; "[AGENT] hashes of driver, input and atom map and the exact invocation must be recorded; no network access" |
| A4 | h2-method-specification.md (as A2) | Unresolved prerequisites, P5 (line 108) | "P5 (OPEN): Hashed driver, input and atom map, exact invocation, no network" |

Only the network and installation part of A3 and A4 would be superseded. The hashing and invocation requirements of
P5 are unchanged.

## 4. Proposed replacement text

The following text, and nothing else, would take the place of A1 and A2 for H2-A-01 launched by the route-R2 driver.

> **R2-S. Network and installation: prevention, not detection.**
>
> 1. **Prevention control.** The engine process is started as
>    `/usr/bin/sandbox-exec -f <attempt>/bundle/h2-r2-sandbox.sb -D H2_PAYLOAD_DIR=<attempt>/payload -D H2_SCRATCH_DIR=<attempt>/scratch`
>    followed by the accepted engine command. The bound items are:
>    - the profile [h2-r2-sandbox.sb](h2-r2-sandbox.sb), SHA256
>      `0768725ab376312c4b22dc83f47b13eeaa67c62dc618dd350c9ab47a2f754d20`;
>    - the program `/usr/bin/sandbox-exec`, 135 136 bytes, SHA256
>      `58839ef01b4eef8aac0d2aa8f9d1c074ae45aafe3533965b030672450064acc8`;
>    - the operating system, macOS 27.0.1 (build 26A434).
>
>    The last two are recorded in [h2-r2-platform-identity.json](h2-r2-platform-identity.json), SHA256
>    `822fbe69807184f8ac5c180caa74d23b0faca64e055ee4bc09a61c82019f2659`. The profile denies the operations it names
>    `network*` and every write it names `file-write*`, except writes under the attempt's `payload/` and `scratch/`
>    directories and to `/dev/null`. New processes inherit the sandbox of their parent (sandbox(7)), so the control
>    applies to the engine's descendants.
> 2. **Refusal is not detection.** The driver does not detect a refused operation, writes no event record of it and
>    reads no system log, and an attempt does not by itself stop the run.
>    - A refusal that makes the engine fail is recorded through the existing stop conditions, applied unchanged:
>      FAILED when the engine process exits nonzero other than through a valid payload stop, is killed by a signal,
>      times out or reports an energy failure; STOP_BEFORE_ENERGY when the payload stops at one of its gates with a
>      valid stop record.
>    - A refusal that the engine tolerates produces no driver record. The engine's stdout, stderr and output files are
>      kept and inventoried and might contain an incidental trace, such as an error message. They are not analysed
>      for refusals, and their silence does not show that no attempt was made.
>    - Either way the single attempt is spent.
> 3. **Retained observations, added as reasons to the accepted classification.** The driver compares the following
>    before launch and immediately before spawn, where a difference blocks launch (item 4), and again after the
>    process ends:
>    - the names of the `conda-meta/` entries;
>    - the full-file digests and declared fields of the two bound package records;
>    - the five bound prefix files;
>    - the bundle and route-R2 files;
>    - the `sandbox-exec` digest and the operating-system build.
>
>    After the process ends, each of the following adds a reason to the outcome:
>    - a failed post-run check in the groups `bundle`, `input`, `prefix`, `interpreter`, `package`, `sha256` or `r2`
>      (the route-R2 checks: the accepted-driver pin, the route-R2 file digests, the platform identity record,
>      `sandbox-exec`, the OS build and the method decision). The runs-root, attempt and free-space checks are kept in
>      the outcome but add no reason, and the accepted network check is replaced;
>    - a changed set of `conda-meta/` names, or a changed digest of a bound package record or bound prefix file;
>    - a changed digest of a bundle or route-R2 file;
>    - a changed `sandbox-exec` or OS observation;
>    - an entry in the attempt root or `bundle/` that the driver did not create;
>    - an attempt copy of the payload, input, profile, code-provenance record or launch record that is missing or
>      differs from its recorded digest;
>    - a failure to complete the post-run checks, the attempt observation or the output inventory.
>
>    The accepted classification is applied to these reasons unchanged:
>    - every reason is kept;
>    - the tier is FAILED whenever the accepted rules give FAILED, which takes precedence;
>    - a valid payload stop stays STOP_BEFORE_ENERGY;
>    - otherwise the tier is QUARANTINE.
>
>    These are observations of state at those instants. They do not detect attempts.
> 4. **Launch prerequisites.** Each of the following is required, and any mismatch is BLOCK_LAUNCH with no engine
>    process:
>    - the exact bytes and digests bound by the run authorization;
>    - a regular, executable, non-link `sandbox-exec` at the bound path, with the bound size and digest;
>    - the bound ProductVersion and ProductBuildVersion;
>    - the profile copied into the attempt, with its digest checked;
>    - the launched command equal to the bound command.
> 5. **Accepted gaps.**
>    - **Detection.** The driver detects no refused attempt and writes no event record of one, and no system log is
>      read. Retained engine output is not analysed for refusals.
>    - **Tested coverage.** Prevention was observed only in fixtures and only for these operation classes: AF_UNIX
>      connect and bind, TCP connect and UDP send to `127.0.0.1`, file creation and append outside `payload/` and
>      `scratch/`. Other destinations, socket types and system-call paths were not tested.
>    - **Profile semantics.** The custom-profile language is undocumented in installed sources: what `network*`,
>      `file-write*`, `subpath`, `literal` and `param` cover is fixture-observed only. `sandbox-exec` and `sandbox_init`
>      are deprecated.
>    - **Not prevented:**
>      - writes and local installation inside `payload/` and `scratch/`;
>      - activity in memory;
>      - operations outside the profile's `file-write*` and `network*` classes;
>      - use of descriptors opened before the sandbox.
>    - **Service-mediated traffic.** Traffic sent by system services on the process's behalf is not covered and was
>      not tested. No claim is made about any specific service.
>    - **Engine under the profile.** The engine's import-time and native side effects take place inside the sandbox,
>      but how they behave there is unobserved. Whether the engine is compatible with the profile at all is
>      unobserved, and a refusal that breaks the engine spends the single attempt.
>    - **Platform dependence.** The control depends on the bound `sandbox-exec` digest and the bound OS build.
>      Either can change, or the facility can disappear.
>    - **Compared set.** The gaps of the accepted proposal §8.6 remain:
>      - other package records' contents;
>      - other prefix files;
>      - anything outside the prefix and bundle that the profile does not protect;
>      - downloads held in memory;
>      - changes reverted between samples.
>    - **Other open items.** M1, E1, the Libint load-name risk, loaded identity, the meaning of the reported total
>      energy and source-to-binary correspondence remain open.

The following text would take the place of the network part of A3 and A4 for H2-A-01 launched by the route-R2 driver:

> **R2-P5.** No network access is permitted to the engine process or its descendants. This requirement is addressed
> only by R2-S, which prevents the covered operation classes and detects nothing; the gaps listed in R2-S item 5
> apply.

## 5. What approval would and would not do

**Approval of these exact bytes would:**
- record a person's decision that, for H2-A-01 launched by the route-R2 driver, R2-S and R2-P5 take the place of A1
  to A4;
- allow the later steps of §6 to begin.

**It would not:**
- authorize a run or any engine command, import or initialization;
- change any accepted file or the accepted Phase A package;
- change Phase B;
- resolve M1, E1, the Libint load-name risk, loaded identity, P4 or source-to-binary correspondence;
- show that the engine runs under the profile;
- turn prevention into detection;
- upgrade any evidence label.

Declining keeps N1 in force and Phase A NOT_RUN. A requested change produces new bytes, a renewed independent review
and a new decision.

## 6. Decision sequence and digest graph

1. **Now.** This package is independently reviewed, and a person decides on these bytes: approve, decline or change.
2. **If approved.** A human approval record binds this file's SHA256 and the SHA256 of the decision packet.
3. **Implementation revision.** A separately reviewed revision of the route-R2 driver sets `R2_METHOD_DECISION` to
   the digests of this file and of the approval record. This changes the driver's bytes, so their digest changes and
   is reviewed again.
4. **Run authorization.** A separate, bounded human run authorization binds:
   - the reviewed bytes;
   - the private machine-binding revision it uses;
   - a fresh code-provenance record;
   - the approval record.
5. **Run.** Only then could one attempt run. Phase B needs its own decision, after independent review of the Phase A
   result.

**Digest graph.** There are no cycles:
- **Leaves:** the profile, the platform identity record and the accepted files. This file embeds the digests of
  these only.
- **This file** is bound by the decision packet and described by the run proposal.
- **The route-R2 driver** pins only the accepted driver's digest. After step 3 it would also hold this file's digest
  and the approval record's digest. Neither of those files embeds the driver's digest.
- **The export manifest** lists every public file and never lists itself.
- **The machine binding** is private. The decision packet records the digest of its current revision, and the binding
  embeds no digest of a public file, so no cycle arises. A future run authorization binds whichever machine-binding
  revision it uses.
- **The code-provenance record** is private. A fresh one is written for a run, and only the run authorization binds
  its digest; no public file records it.
- **The decision packet** records the current route-R2 driver bytes, which the reviewed implementation revision of
  step 3 replaces.

## 7. Leaf digests

| File | SHA256 |
|---|---|
| [h2-r2-sandbox.sb](h2-r2-sandbox.sb) | `0768725ab376312c4b22dc83f47b13eeaa67c62dc618dd350c9ab47a2f754d20` |
| [h2-r2-platform-identity.json](h2-r2-platform-identity.json) | `822fbe69807184f8ac5c180caa74d23b0faca64e055ee4bc09a61c82019f2659` |
| [../h2-method-parameters.json](../h2-method-parameters.json) | `2728b0efe2c6dae070346a3d0475857222f02864a6da63859edf4d4e334c156e` |
| [../h2-method-specification.md](../h2-method-specification.md) | `a8cb407a99d1a534dcb199c941888236e19af15b5f407edf761a6bdc1810001d` |
| [../phase-a/h2_phase_a_driver.py](../phase-a/h2_phase_a_driver.py) | `6dcb4845e3b4b29f89dc4027274675e24c1152508828b1230857baac58b9aa7d` |
| [../phase-a/h2_phase_a_payload.py](../phase-a/h2_phase_a_payload.py) | `7de1d53c70af7a4ff3a71fb5fbcd7cedfec24a7e3eb49d8b27f9d6bf6cc2f69b` |
| [../phase-a/h2-a-01-input.json](../phase-a/h2-a-01-input.json) | `3ca4753312b3f2cd50274d4c8f8dda48de422d691e34bf47784b1602670dc3d3` |
| [../phase-a/h2-a-01-static-identity.json](../phase-a/h2-a-01-static-identity.json) | `a45ee84d0d28e794ea7f56e7ff74130551fb326c36c7d8353467966ed2c025cc` |

## 8. Gates

All gates are unchanged:
- W1 STOPPED (S10).
- E-01 technically BLOCKED and scientifically INDETERMINATE.
- C3 readiness, MS-001 Stage 1 and option A BLOCKED.

Sources: [../../../SOURCES.md](../../../SOURCES.md) entries [55] (installed sandbox documentation) and [56] (route-R2
fixture assessment).
