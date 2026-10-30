# H2-A-01 (run 01): one authorized attempt ran once; one recorded single-point RHF/STO-3G value

## 1. Summary

**Status: COMPLETED_PENDING_REVIEW**, the route-R2 driver's own tier for one attempt that ran to its end with no reason
recorded. The label is immutable and was not rewritten after review. It is not a statement about chemistry.

- **Authorization.** One bounded attempt of job H2-A-01 was authorized by the project owner on 2026-10-29
  (recorded on receipt at 20:19:15Z; that is the time the orchestration system recorded the decision, not an independently
  measured time of the decision, and the identity of the person was not independently established). M1 stays accepted but
  not resolved: the 500 MiB engine memory setting is not an operating-system limit. It is a separate authorization from
  the one of 2026-10-10, which stays unexercised ([stop record](../H2-A-01/README.md)) and is not carried forward.
- **Prerequisites.** Earlier on 2026-10-29 the driver wrote a fresh code-provenance record over the eight covered
  repository files (the full-diff digest is that of empty input, so no uncommitted change was recorded) and one static
  preflight passed. A driver-schema authorization record was prepared from the decision and passed an itemized check
  (141 of 141 items) before the run.
- **The run.** The driver's `run` mode was invoked once. Inside that invocation the driver repeated its preflight before
  launch (34 of 34 checks passed, then 35 of 35 in the final block, which replaces the attempt-absent check by a
  fresh-attempt check and adds `r2.attempt.bundle_fresh`) and ran its checks again after the engine exited (33 of 33,
  with neither attempt check). The engine ran under a bound sandbox profile with one thread and a 300 s bound.
  It exited 0 after 8.903699540998787 s, was not timed out and left no process in the group.
- **The result as recorded.** The engine, Psi4 1.11, reported a total energy of **-1.11671432506257 hartree** and a nuclear
  repulsion of 0.7142857142857143 hartree for the hydrogen molecule at one fixed, input separation of **1.4 bohr**
  (RHF/STO-3G, two electrons, singlet), converged in 2 SCF iterations. The independent review derived an electronic energy
  of -1.8310000393482843 hartree under the convention that the reported total includes the nuclear repulsion; the engine did
  not print it. These are **recorded values of one run**.
- **What this is not.** It is a single point at one fixed separation. It is not a dissociation curve, not an optimized or
  predicted equilibrium bond length (the 1.4 bohr separation is the fixed input internuclear distance, not a result), not
  readiness for any further work, not parity with any other calculation, and not a reproduction of, or agreement with, the
  benchmark study. It validates no donor, surface or pathway and does not explain the stopped E-01 attempt.
- **Review.** An independent review of the run result recorded the canonical decision APPROVE with eight non-blocking findings
  and no blocker, and Lead acceptance of the narrow result is recorded (private task records). A later independent review of
  the material that supports the post-run host summary recorded **REJECT** with one blocker, because two claims of that material
  were not supported by the retained raw capture; that REJECT stays on the record, and the Lead did not accept that candidate. A
  documentary erratum, with no new capture and no probe, relabelled those two claims supplied and unverified; a further
  independent review recorded APPROVE with eight non-blocking findings, and the Lead accepted the correction. That acceptance
  covers the correction only: it closes no open item and grants no evidence class. A final independent review recorded APPROVE
  with eight non-blocking findings, and the Lead's disposition (see below) records two outcomes.
- **Classification.** The values are actual software output, recorded as such. The class `[COMP-PRED]` is **not granted**: the
  [evidence policy](../../../docs/evidence-policy.md) section 4 requires complete provenance, and the remaining gap is the
  engine's source-code identity (section 4 below and section 8 of the report). The classification belongs to the independent
  review and Lead acceptance, which are recorded privately, and this record does not change it.

This report is an `[AGENT]` summary of private task records and of a recorded software output. The private originals are
identified by SHA256 and neutral description in [provenance.json](provenance.json). The machine-readable form is
[outcome.json](outcome.json). The full report, with figures, is
[H2-A-01-RESULT-REPORT.md](../../../docs/learning/h2/H2-A-01-RESULT-REPORT.md).

## 2. Timeline (UTC, 2026-10-29)

| Time | Event |
|---|---|
| 20:19:15 | The owner's decision was recorded on receipt |
| 20:39:48.98 | The driver's initial preflight inside the run invocation: 34 of 34 checks passed |
| 20:39:49.31 | Launch record written; the engine process started at 20:39:49.31 under the sandbox profile |
| 20:39:49.97 | Record taken before the engine was imported (the list of engine modules loaded before import is empty) |
| 20:39:58.11 | Engine identity record taken inside the engine process, then the configuration and basis records |
| 20:39:58.12 | The energy call began; it returned at 20:39:58.15 |
| 20:39:58.21 | The engine process ended (exit 0) |
| 20:39:58.34 | Post-run checks (33 of 33) and the driver outcome, tier COMPLETED_PENDING_REVIEW |
| 21:37:21 | A read-only host capture, about 57 min 32 s after the launch record's time (section 4) |

## 3. What was done and what was not

**Done:**
- one invocation of the driver's `run` mode, one engine process, one attempt directory, all output kept;
- the recorded values, the two engine streams, the engine's text output and log, and the identity, configuration and
  basis records, as listed in section 6;
- the review and acceptance steps described in section 1.

**Not done:**
- no second invocation, retry, redelivery, changed setting or fallback engine; the runs root holds only this attempt;
- no Phase B point; no other driver mode and no further preflight after the run;
- no installation, build or source retrieval was part of the run, and none was authorized; network traffic was not
  measured, and no claim about it is made (the sandbox profile prevents, and does not detect);
- no calculation of any other separation, method or basis;
- nothing was staged, committed, published or delivered.

## 4. Open items and residuals

All of the following stay open or unexplained. None was resolved by the run or by its review.
- **OMP Warning #179.** The engine's error stream holds one line, `OMP: Warning #179: Function Can't set size of /tmp file
  failed:`. Its cause and numerical impact are unknown (INDETERMINATE) and its harmlessness is unproved. Convergence does
  not prove it harmless.
- **The `CURRENT ENERGY` alias is a `[GAP]`.** The payload's recorded source text for the returned value is a string literal
  (`docs/learning/h2/phase-a/h2_phase_a_payload.py`, line 445 at the base commit), not a read-back. The returned value, the printed final
  energy and the printed total agree (`psi4-output.dat` lines 177 and 184, `psi4-output.log` line 3), but the label itself
  is not independently proved.
- **`network.prerequisite` FAIL retained.** The base check that the approved route-R2 revision replaces is retained, as a
  FAIL with detail `NETWORK_PREREQUISITE_UNRESOLVED`, in all three embedded check blocks. It is not relabelled.
- **A platform-added environment name.** The launch record lists `__CF_USER_TEXT_ENCODING` as added by the platform
  outside the allowed list. It is recorded, not interpreted (E1 stays open).
- **Host summary, taken after the run.** A read-only capture about 57 min 32 s after launch gives: arm64, Apple M5 Pro, 18 CPUs
  (two core levels of 6 and 12; which is performance and which is efficiency is an inference), 68719476736 bytes of memory,
  model Mac17,9, macOS 27.0.1 build 26A434, last boot 2026-10-06T01:53:17Z. It was not captured by the driver during the
  run. Supported by the retained capture: the OS product and build equal the launch record's, the last boot precedes the
  launch, and the host name agrees with the engine's own output. **Same host is supported but not unique:** no serial
  number or hardware UUID was captured, and the hardware numbers match the host after the run only. **Supplied
  and unverified:** that the recorded `sandbox-exec` digest equals the installed program's digest at capture time, and that
  the recorded absolute paths existed then; the retained capture contains no hash or path check. Exclusivity of the capture is
  indeterminate. **Load, thermal state and memory pressure at run time are UNOBSERVED.**
- **Engine source-code identity, UNESTABLISHED.** The engine is the conda-forge psi4 1.11 build `py314h53d0584_1` (archive
  SHA256 `92d4aeb73fe7027bd239a656cf353461490420d76096ae762bd9f1c29ed4da10`). Its printed revision is the build's placeholder,
  `Git: Rev {} zzzzzzz` (`redacted/psi4-output.dat` line 6), and the code-provenance record excludes the engine environment.
  Two anomalies are explained by **supplied** evidence, a read-only observation of the external engine environment made outside
  this project's boundary and not read by this project: the installed core extension differs from its archive path record
  because conda applied its declared prefix replacement and re-signed it ad hoc, matching conda's own install-time record; and
  the banner revision is the placeholder that the shipped version metadata defines. This shows no tampering or different build,
  which is an absence of evidence and not a proved negative; the patch and re-signing were not reproduced byte for byte.
  Source-to-binary correspondence is not established, and the repository's own catalogue records that the material the project
  holds cannot establish it. The recorded core-extension digest matches the one in E-01's `method-config.json`: one digest
  agreeing between two records, which does not establish the same build or equivalent runtimes.
- **Loaded identity.** The identity record lists 468 loaded images, including `libint2.dylib` and `libxc.15.dylib` under the
  engine prefix, a runtime observation made during the run. A path is not a build identity, and the load name encodes no
  version, so the loaded build, version and source linkage stay unresolved. Also open: P1; the Libint load-name question; E1;
  compatibility with the sandbox profile.
- **The Lead's disposition.** The orchestration system's own run-record requirement for this attempt is recorded as **met on a
  retained supplied-source basis only**: the authorization, Mission, revision, proposal and workspace identifiers match, and the
  result and its full review are bound and durable, but the external files and whole-store digests were supplied and are not
  independently checked or authenticated as to current state. The result has not been ingested into that system, the approved
  text does not require it, and this record does not claim it. The reviewed-calculation requirement is recorded as **not met**:
  its provenance clause stays open on the engine's source-code identity, and no `[COMP-PRED]` is granted.
- **M1** is accepted but not resolved: 500 MiB is an engine setting, not an operating-system memory limit.
- **Retention and execution completeness** are INDETERMINATE.

## 5. Gates

Phase B is NOT_RUN and has no authorization. The gates are unchanged: W1 STOPPED (S10); E-01 technically BLOCKED,
scientifically INDETERMINATE and unexplained; C3 readiness, MS-001 Stage 1 and option A BLOCKED. No evidence label changed.

## 6. Files

| File | Contents |
|---|---|
| [README.md](README.md) | This record |
| [outcome.json](outcome.json) | Machine-readable outcome: tier, settings, process, check counts, recorded values, classification statement, host summary, residuals |
| [provenance.json](provenance.json) | Bound digests, the hashed inventory of all sixteen original files with their public derivatives, private records by SHA256 and neutral description, and the redaction rules with replacement counts |
| [raw/](raw/) | Byte-identical copies: `result.json`, `psi4-output.log`, `engine.stdout`, `engine.stderr` |
| [redacted/](redacted/) | Redacted copies, with local paths, host name and process id replaced by tokens: `psi4-output.dat`, `i1-identity.json` (engine identity and loaded images), `i2-configuration.json`, `i3-basis-geometry.json`, `pre-import.json`, `launch-record.json`, `driver-outcome.json`, `timer.dat` |
| [derived/code-provenance-summary.json](derived/code-provenance-summary.json) | Summary of the code-provenance record: base commit, coverage statement and per-file digests |

All sixteen original files stay private and unedited. The three bundle copies (input, sandbox profile, payload) are
byte-identical to public repository files and are identified in `provenance.json` instead of being copied again. The
report, the figures with their source tables and renderers, and the PDF are in
[docs/learning/h2/](../../../docs/learning/h2/README.md) and [docs/figures/](../../../docs/figures/), and are listed with their
digests in [provenance/EXPORT-MANIFEST.md](../../../provenance/EXPORT-MANIFEST.md).

Sources: [../../../docs/SOURCES.md](../../../docs/SOURCES.md) entries [60] to [62].
