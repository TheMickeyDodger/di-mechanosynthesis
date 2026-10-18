# H2-A-01 route-R2 run authorization: human record

Date of record: 2026-10-10. Receipt time of the answer: 2026-10-10T22:02:47Z, the time at which the separate
orchestration system that governs this project recorded the answer on its receipt. It is not an independently measured
time of the answer, and the identity of the person was not independently established.

**Not exercised.** The run never started. It stopped as STOP_UNRUN before launch: the driver's `run` mode was invoked
zero times and no engine process existed. No launch permission remains in the task that held this authorization
([stop record](../../../../results/h2/H2-A-01/README.md)). This record is not a review decision.

## 1. The decision

| Element | Value |
|---|---|
| Decision | Authorize exactly one attempt |
| Answer, verbatim | "yes, authorized" |
| Question answered, verbatim | "Do you authorize exactly one H₂ RHF/STO-3G attempt at 1.4 bohr, bounded to 300 seconds, one thread, 50 SCF iterations and zero retries—and explicitly accept M1: 500 MiB is an engine setting, not an OS memory cap? Environment, loader or sandbox incompatibility may stop and consume that attempt, as packet §5 describes." |
| Context | The Operator's message immediately before the question bound both reviewed documentary files by SHA256 (§2) |
| Receipt time | 2026-10-10T22:02:47Z, a receipt time, not a measured time of the answer |
| Private reply record | SHA256 `bd67c57e82f0ca0199df434060def9ccd7c8e2c7e4a3c21bcd84d044c189abe3`. It is not published |

The question was put to a person directing this project, through the separate orchestration system, after the
independent review of the enabling revision. This record carries no personal name and no task, session or agent
identifier.

## 2. Bytes authorized

The authorization names these documentary files by SHA256:

| File | SHA256 | Role |
|---|---|---|
| [H2-A-R2-RUN-DECISION-PACKET.md](H2-A-R2-RUN-DECISION-PACKET.md) | `eea5cfaaf459adcb82373de1cd317493837431b8acbd327f7a09a6dee9d8edfe` | The run-decision packet |
| [H2-A-R2-RUN-PROPOSAL-02.md](H2-A-R2-RUN-PROPOSAL-02.md) | `a9c11ba494eb9384d348b180c8ddb7cb64cbb258ae040a411a16510628640408` | The current run proposal |

It binds the sixteen interlock keys of the packet's §3 at these values:

| Key | File, relative to `docs/learning/h2/` | SHA256 |
|---|---|---|
| `driver` | `phase-a/h2_phase_a_driver.py` | `6dcb4845e3b4b29f89dc4027274675e24c1152508828b1230857baac58b9aa7d` |
| `payload` | `phase-a/h2_phase_a_payload.py` | `7de1d53c70af7a4ff3a71fb5fbcd7cedfec24a7e3eb49d8b27f9d6bf6cc2f69b` |
| `input` | `phase-a/h2-a-01-input.json` | `3ca4753312b3f2cd50274d4c8f8dda48de422d691e34bf47784b1602670dc3d3` |
| `parameters` | `h2-method-parameters.json` | `2728b0efe2c6dae070346a3d0475857222f02864a6da63859edf4d4e334c156e` |
| `static_identity` | `phase-a/h2-a-01-static-identity.json` | `a45ee84d0d28e794ea7f56e7ff74130551fb326c36c7d8353467966ed2c025cc` |
| `run_proposal` | `phase-a/H2-A-01-RUN-PROPOSAL.md` | `d9bcb7e186a0ced226478d93470682c6ff84c78abab1f7546eb45bdac551225f` |
| `decision_packet` | `phase-a/H2-A-01-DECISION-PACKET.md` | `cfb4a9912114452211e19edadf115816e48359911e05f48d71c54672b72b55e5` |
| `r2_driver` | `phase-a-r2/h2_phase_a_r2_driver.py` | `0b3172f8388b0f0c053a2b7a6945394e7e796aae8b14d0228447d7bc860af9b6` |
| `r2_profile` | `phase-a-r2/h2-r2-sandbox.sb` | `0768725ab376312c4b22dc83f47b13eeaa67c62dc618dd350c9ab47a2f754d20` |
| `r2_platform_identity` | `phase-a-r2/h2-r2-platform-identity.json` | `822fbe69807184f8ac5c180caa74d23b0faca64e055ee4bc09a61c82019f2659` |
| `r2_method_revision` | `phase-a-r2/H2-R2-METHOD-REVISION.md` | `9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc` |
| `r2_run_proposal` | `phase-a-r2/H2-A-R2-RUN-PROPOSAL.md` | `d0239104596409d8f278449103f413843a225550cbfb91616d25d5b5143c2b2e` |
| `r2_decision_packet` | `phase-a-r2/H2-A-R2-DECISION-PACKET.md` | `5ce61f7c97be6db8e332d296d3f54335acb04552296d33eb230ce40cbd9c4083` |
| `method_revision_approval` | `phase-a-r2/H2-R2-METHOD-HUMAN-APPROVAL.md` | `e4897a80869bc04d6ece9a8be75673085e18ddb1b07df1df5e71fd4b76f10d7c` |
| `machine_binding` | private machine binding, revision R2-01; not published | `7a5ac67dd8c6f196955589e8d6e8c0f96240db10c42a01d043974d0feee884b0` |
| `code_provenance` | private code-provenance record written fresh from these bytes; not published | `b2ff2ad014ea284076ae9d56125b392947dcaa9200ae9e5e5ee9349744e924fc` |

Agents prepared a private driver-schema authorization record from the person's reply, with these sixteen bindings,
the interpreter, prefix and runs root of the machine binding, the static digests of the static identity record and
the allow-list environment. Its SHA256 is `d002c75ff69c7572152609be142bfba34b35e6117189417bc7516459215ab261`; it is not
published. It passed an independent check of every interlock condition, but it was never presented to the driver's
`run` mode. Such a record is checked by the driver by bytes and fields only and cannot show that a person authorized
anything; the authority is the person's reply in §1.

## 3. Scope

- Exactly one attempt of job H2-A-01, launched only through `h2_phase_a_r2_driver.py run`, with at most one engine
  process: `max_attempts` 1 and zero retries.
- The accepted settings, unchanged: RHF/STO-3G at 1.4 bohr, a 300 s wall bound, one thread, at most 50 SCF iterations
  and an engine memory setting of 500 MiB.
- **M1, accepted.** 500 MiB is an engine setting only. No operating-system memory limit is applied, and the peak
  resident memory of the direct child would merely be observed. M1 is accepted, not resolved.
- Independent assessment of the attempt's result or stop.

## 4. Exclusions

The authorization does not cover:
- Phase B;
- a second attempt or a retry;
- changed settings or a fallback engine;
- installation, building or retrieval of sources;
- external network access or system changes;
- any W1, AiiDA, MS-001, Stage 1 or option A action;
- staging, commit, push, merge, deployment or publication.

## 5. Limits that applied (packet §5)

- **E1.** Whether the engine interpreter adds an environment name outside the allow-list and the declared platform
  name was not observed.
- **Libint load-name risk.** Which file the loader resolves for `@rpath/libint2.dylib` was not established.
- **Engine under the profile.** Whether the engine is compatible with the sandbox profile was not observed.
- **No detection.** The driver detects no refused operation and writes no record of one.
- **The other gaps of R2-S item 5**, as the person approved them with the method revision.
- **Open identity and meaning.** Loaded identity, P4 (the meaning of the reported total energy) and source-to-binary
  correspondence are open.

None of these was observed or resolved, because no run took place. They all stay open.

## 6. What happened

[AGENT] summary of private records. Prerequisites were prepared and checked: a fresh code-provenance record, one
static preflight with every check passing, the driver-schema authorization record, which passed an independent
interlock check, and an empty runs root. A static preflight pass is not readiness, loaded identity or runtime identity.
The automatic permission check of the agent client that was delegating the run refused the command that would have
handed the run assignment to the executing agent. Its reason, verbatim: "Permission for this action was denied by the
Claude Code auto mode classifier. Reason: [Code from External]." The assignment was never delivered. The driver's `run`
mode was never invoked, no engine process existed and no attempt directory was created.

The disposition is STOP_UNRUN, an orchestration stop before launch. It is not a driver tier, an engine failure or
chemistry evidence. The single authorized invocation is numerically unspent, but the launch scope of the task that
held the authorization ended with this stop, and no launch permission remains in it. Nothing was retried, redelivered
or launched by another route, and no permission or setting was changed. This record does not carry the authorization
forward. Whether any future attempt is authorized is for the people directing the project.

## 7. What this record is not

- It is not a review decision, readiness, a run or a result.
- It does not decide E1 or any other open item, and it does not resolve M1.
- It does not authorize Phase B.
- It permits no installation, build, network access or system change.
- It is not physical evidence and changes no evidence label.

## 8. Gates

H2 has no result: no energies and no SCF data. Phase B is not authorized. W1 is STOPPED (S10). E-01 is technically
BLOCKED and scientifically INDETERMINATE. C3 readiness, MS-001 Stage 1 and option A are BLOCKED.

Sources: [../../../SOURCES.md](../../../SOURCES.md) entries [57] and [58].
