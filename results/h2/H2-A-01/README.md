# H2-A-01: authorized attempt stopped before launch (STOP_UNRUN)

## 1. Summary

**Status: STOP_UNRUN.** The run never started. There is no result: no energies and no SCF data.

- **Authorization.** A person authorized exactly one attempt of job H2-A-01 through the route-R2 driver: RHF/STO-3G at
  1.4 bohr, 300 s, one thread, at most 50 SCF iterations and zero retries. The person also accepted M1. The
  authorization names the [run-decision packet](../../../docs/learning/h2/phase-a-r2/H2-A-R2-RUN-DECISION-PACKET.md)
  and the [current run proposal](../../../docs/learning/h2/phase-a-r2/H2-A-R2-RUN-PROPOSAL-02.md) by SHA256
  ([authorization record](../../../docs/learning/h2/phase-a-r2/H2-A-01-HUMAN-RUN-AUTHORIZATION.md)).
- **Prerequisites.** They were prepared and checked: a fresh code-provenance record, one static preflight with every
  check passing, a driver-schema authorization record that passed an independent interlock check, and an empty runs
  root. A static preflight pass is not readiness, loaded identity or runtime identity. No engine process was started
  at any time.
- **The stop.** The automatic permission check of the agent client that was delegating the run refused the command
  that would have handed the run assignment to the executing agent. Its reason, verbatim: "Permission for this action
  was denied by the Claude Code auto mode classifier. Reason: [Code from External]." The assignment was never
  delivered. The driver's `run` mode was never invoked, no engine process existed and no attempt directory was
  created.
- **Disposition.** STOP_UNRUN is an orchestration stop before launch. It is not a driver tier (not BLOCK_LAUNCH,
  STOP_BEFORE_ENERGY, FAILED, QUARANTINE or COMPLETED_PENDING_REVIEW), not an engine failure and not chemistry
  evidence.
- **The authorization.** The single authorized invocation is numerically unspent, but no launch permission remains in
  the task that held the authorization: its launch scope ended with this stop. Nothing was retried, redelivered or
  launched by another route, and no permission or setting was changed. These records do not carry the authorization
  forward. Whether any future attempt is authorized is for the people directing the project.

This report is an `[AGENT]` summary of private task records, which are identified by SHA256 in
[provenance.json](provenance.json). Its independent review is pending. The machine-readable form is
[outcome.json](outcome.json).

## 2. Timeline (UTC, 2026-10-10)

| Time | Event |
|---|---|
| 22:02:47 | The person's reply "yes, authorized" was recorded on receipt (a receipt time, not a measured time of the answer) |
| 22:12:10 | The empty runs root was created |
| 22:12:35 | The driver's `code-provenance` mode wrote a fresh code-provenance record over the eight covered paths; it starts no engine process and runs read-only Git queries as child processes |
| 22:12:57 | One static preflight by the driver: every check passed (34 of 34); it started no engine process |
| 22:14:13 | The driver-schema authorization record was prepared from the reply (the file's modification time; no time is recorded inside the record) |
| 22:15:25 | A static recomputation of every interlock condition against that record passed |
| 22:18:42 | Independent readiness verification, including an in-process evaluation of the driver's interlock checks against the recorded preflight report, without a run: every check passed (56 of 56) |
| 22:19:41 | The readiness record was written |
| 22:20:15 | Coordination release of the single invocation; this was not new human authority |
| between 22:20:15 and 22:22:57 | The client's permission check refused the command that would have delivered the run assignment; its exact time was not exposed |
| 22:22:57 | Stop disposition: STOP_UNRUN; the task's launch scope ended |

## 3. What was done and what was not

**Done:**
- the runs root was created empty, and it is still empty;
- one fresh code-provenance record was written by the driver's `code-provenance` mode, which starts no engine process
  and runs read-only Git queries as child processes;
- one static preflight was run by the driver; it reads and hashes files and started no engine process. By reading the
  exact driver code, its preflight path contains no process-creation call; this is a source-level statement, not an
  observation of the processes that ran;
- a driver-schema authorization record was prepared and checked statically;
- the readiness was verified independently and the single invocation was released for coordination.

**Not done:**
- the run assignment was not delivered;
- the driver's `run` mode was not invoked; zero invocations;
- no engine process was started, and the engine interpreter was never executed;
- no attempt directory was created, and no engine output exists;
- nothing was retried, reworded, redelivered or routed another way;
- no permission, setting, policy or configuration was changed;
- no person was asked to reconfirm the authorization;
- nothing was installed, built or retrieved, and no system setting was changed. Network activity was not observed,
  and no claim about it is made.

## 4. Open items

Nothing about the following was observed, because no run took place. All stay open:
- **E1**, the engine interpreter's environment;
- the **Libint load-name risk**;
- the engine's **compatibility with the sandbox profile**;
- **loaded identity**;
- **P4**, the meaning of the reported total energy;
- **source-to-binary correspondence**.

**M1** stays accepted by the person, but not resolved: 500 MiB is an engine setting, not an operating-system memory
limit.

## 5. Gates

H2 has no result. Phase B is not authorized. The gates are unchanged:
- W1 STOPPED (S10);
- E-01 technically BLOCKED and scientifically INDETERMINATE;
- C3 readiness, MS-001 Stage 1 and option A BLOCKED.

## 6. Files

| File | Contents |
|---|---|
| [README.md](README.md) | This stop report |
| [outcome.json](outcome.json) | Machine-readable outcome of the stop |
| [provenance.json](provenance.json) | Bound digests, private source records by SHA256, preflight check identifiers and statuses, derivation and redaction rules, and the integration files changed |

No raw directory exists: no run output exists to publish.

Sources: [../../../docs/SOURCES.md](../../../docs/SOURCES.md) entry [58].
