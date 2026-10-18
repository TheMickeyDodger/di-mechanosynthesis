# H2-A-01 route-R2 run-decision packet

## 1. What this packet is

This is a redacted, public preparation record for a person's decision. It is **not an authorization** and
authorizes nothing. A person approved the method revision
([approval record](H2-R2-METHOD-HUMAN-APPROVAL.md)), and the route-R2 driver now binds that approval. No run
authorization exists, and without one the driver refuses every launch.

The technical description is the frozen [H2-A-R2-RUN-PROPOSAL.md](H2-A-R2-RUN-PROPOSAL.md), with its delta
[H2-A-R2-RUN-PROPOSAL-02.md](H2-A-R2-RUN-PROPOSAL-02.md). The approved decision packet
[H2-A-R2-DECISION-PACKET.md](H2-A-R2-DECISION-PACKET.md) is unchanged. Its §3 lists the values at its own bytes; this
packet lists the current values.

## 2. What is decided next

Only one thing: **authorize, decline or change exactly one attempt of job H2-A-01 through
`h2_phase_a_r2_driver.py run` at the exact bytes bound in §3.** Nothing is authorized by this packet.

Not decided by this packet:
- Phase B;
- a second attempt or a retry;
- anything else.

## 3. Bound digests

These are the current values of the sixteen interlock keys.

<!-- BOUND-DIGESTS:BEGIN -->
| Binding key | File | SHA256 |
|---|---|---|
| `r2_driver` | phase-a-r2/h2_phase_a_r2_driver.py (the enabled driver, step 3 of the method revision §6) | `0b3172f8388b0f0c053a2b7a6945394e7e796aae8b14d0228447d7bc860af9b6` |
| `r2_profile` | phase-a-r2/h2-r2-sandbox.sb (unchanged) | `0768725ab376312c4b22dc83f47b13eeaa67c62dc618dd350c9ab47a2f754d20` |
| `r2_platform_identity` | phase-a-r2/h2-r2-platform-identity.json (unchanged) | `822fbe69807184f8ac5c180caa74d23b0faca64e055ee4bc09a61c82019f2659` |
| `r2_method_revision` | phase-a-r2/H2-R2-METHOD-REVISION.md (approved, frozen) | `9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc` |
| `r2_run_proposal` | phase-a-r2/H2-A-R2-RUN-PROPOSAL.md (approved context, frozen) | `d0239104596409d8f278449103f413843a225550cbfb91616d25d5b5143c2b2e` |
| `r2_decision_packet` | phase-a-r2/H2-A-R2-DECISION-PACKET.md (approved context, frozen) | `5ce61f7c97be6db8e332d296d3f54335acb04552296d33eb230ce40cbd9c4083` |
| `method_revision_approval` | phase-a-r2/H2-R2-METHOD-HUMAN-APPROVAL.md (the human approval record) | `e4897a80869bc04d6ece9a8be75673085e18ddb1b07df1df5e71fd4b76f10d7c` |
| `driver` | phase-a/h2_phase_a_driver.py (accepted, unchanged) | `6dcb4845e3b4b29f89dc4027274675e24c1152508828b1230857baac58b9aa7d` |
| `payload` | phase-a/h2_phase_a_payload.py (accepted, unchanged) | `7de1d53c70af7a4ff3a71fb5fbcd7cedfec24a7e3eb49d8b27f9d6bf6cc2f69b` |
| `input` | phase-a/h2-a-01-input.json (accepted, unchanged) | `3ca4753312b3f2cd50274d4c8f8dda48de422d691e34bf47784b1602670dc3d3` |
| `parameters` | h2-method-parameters.json (accepted, unchanged) | `2728b0efe2c6dae070346a3d0475857222f02864a6da63859edf4d4e334c156e` |
| `static_identity` | phase-a/h2-a-01-static-identity.json (accepted, unchanged) | `a45ee84d0d28e794ea7f56e7ff74130551fb326c36c7d8353467966ed2c025cc` |
| `run_proposal` | phase-a/H2-A-01-RUN-PROPOSAL.md (accepted, unchanged) | `d9bcb7e186a0ced226478d93470682c6ff84c78abab1f7546eb45bdac551225f` |
| `decision_packet` | phase-a/H2-A-01-DECISION-PACKET.md (accepted, unchanged) | `cfb4a9912114452211e19edadf115816e48359911e05f48d71c54672b72b55e5` |
| `machine_binding` | private route-R2 machine binding, revision R2-01, carried unchanged (not published; embeds no public-file digest) | `7a5ac67dd8c6f196955589e8d6e8c0f96240db10c42a01d043974d0feee884b0` |
| `code_provenance` | private code-provenance record, written fresh from these bytes | bound only by the run authorization; no public file records it |
<!-- BOUND-DIGESTS:END -->

Documentary files, which are not interlock keys:

| File | SHA256 |
|---|---|
| [H2-A-R2-RUN-PROPOSAL-02.md](H2-A-R2-RUN-PROPOSAL-02.md), the current run proposal | `a9c11ba494eb9384d348b180c8ddb7cb64cbb258ae040a411a16510628640408` |
| This packet | recorded in the export manifest (a file cannot contain its own digest) |

A run authorization must name both by SHA256 in its statement. The driver does not check the statement: it checks
bytes and fields only and cannot show that a person authorized anything. The tests under [tests/](tests/) are not
bound into a launch; their digests are in the export manifest.

## 4. What a run authorization would bind

A run authorization, which is not part of this packet, would bind:
- the sixteen keys of §3 at the values given there, with `code_provenance` at a fresh private record written from
  these bytes by the driver's `code-provenance` mode;
- the private paths of the machine binding and of that code-provenance record, the interpreter, prefix and runs root
  of the machine binding, the static digests of the static identity record and the exact allow-list environment;
- a statement that names this packet and the current run proposal by SHA256 and records the person's acceptance or
  resolution of M1.

Its scope would be one attempt (`max_attempts 1`, zero retries) and one engine process, launched only through
`h2_phase_a_r2_driver.py run`, with the wrapped command of the frozen proposal §4 and the accepted settings.

The following would never be in its scope:
- Phase B;
- a second attempt or a retry;
- any changed setting, fallback or other engine;
- installation, building or network access;
- any change to the accepted lesson, specification or parameter file;
- any MS-001, E-01 or W1 action;
- publication of results.

## 5. Items a person must decide, not accepted on anyone's behalf

- **M1, memory.** 500 MiB is an engine setting only. No operating-system memory limit is applied, and the peak
  resident memory of the direct child is merely observed. A run authorization must record that the person accepts or
  resolves M1 (accepted proposal P6).
- **E1, environment.** If the engine process holds any environment name other than the allow-list and the declared
  platform name `__CF_USER_TEXT_ENCODING`, it stops before energy, and that spends the single attempt. Whether the
  engine interpreter adds such a name has not been observed.
- **Libint load-name risk.** Which file the loader resolves for the core extension's `@rpath/libint2.dylib`
  dependency is not established. If it is not the bound `libint2.dylib`, the run stops at I1 and spends the attempt.
- **Engine under the profile.** Whether the engine is compatible with the profile is unobserved. A refusal that
  breaks the engine spends the single attempt.
- **No detection.** The driver detects no refused attempt and writes no record of one.
- **The other gaps of R2-S item 5**, as the person approved them: the tested coverage, the undocumented profile
  semantics and deprecated `sandbox-exec`, what is not prevented, service-mediated traffic, platform dependence and
  the compared set.
- **Open identity and meaning.** Loaded identity, P4 (the meaning of the reported total energy) and source-to-binary
  correspondence remain open. A completed run would be `COMPLETED_PENDING_REVIEW` and would need an independent
  review. It would not be physical evidence.

## 6. Options

- **Authorize exactly one attempt** at the bytes of §3, with a run authorization as in §4.
- **Decline.** Phase A stays NOT_RUN and Phase B stays CONDITIONAL_NOT_AUTHORIZED.
- **Request changes.** Name them. Changed bytes need a renewed independent review and a new decision.

## 7. Template, deliberately invalid

The schema value below is deliberately invalid, so the driver rejects this template as written. It is not an
authorization.

```json
{
  "schema": "TEMPLATE-NOT-AN-AUTHORIZATION",
  "job_id": "H2-A-01",
  "max_attempts": 1,
  "authorized_by": "<NOT FILLED>",
  "authorized_utc": "<NOT FILLED>",
  "statement": "<NOT FILLED: must name this packet and the current run proposal by SHA256 and record M1; this template authorizes nothing>",
  "bound_sha256": {
    "driver": "<NOT FILLED>", "payload": "<NOT FILLED>", "input": "<NOT FILLED>", "parameters": "<NOT FILLED>",
    "static_identity": "<NOT FILLED>", "run_proposal": "<NOT FILLED>", "decision_packet": "<NOT FILLED>",
    "r2_driver": "<NOT FILLED>", "r2_profile": "<NOT FILLED>", "r2_platform_identity": "<NOT FILLED>",
    "r2_method_revision": "<NOT FILLED>", "r2_run_proposal": "<NOT FILLED>", "r2_decision_packet": "<NOT FILLED>",
    "machine_binding": "<NOT FILLED>", "code_provenance": "<NOT FILLED>", "method_revision_approval": "<NOT FILLED>"
  },
  "machine_binding_path": "<NOT FILLED>",
  "code_provenance_path": "<NOT FILLED>",
  "interpreter": "<NOT FILLED>",
  "prefix": "<NOT FILLED>",
  "runs_root": "<NOT FILLED>",
  "expected_static_sha256": {"<NOT FILLED>": "<NOT FILLED>"},
  "environment": {"<NOT FILLED>": "<NOT FILLED>"}
}
```

## 8. Gates

H2 is NOT_RUN, and Phase B is not authorized. The project gates are unchanged:
- W1 STOPPED (S10);
- E-01 technically BLOCKED and scientifically INDETERMINATE;
- C3 readiness, MS-001 Stage 1 and option A BLOCKED.

This packet is not readiness, parity, physical evidence or a review decision.

Sources: [../../../SOURCES.md](../../../SOURCES.md) entries [55], [56] and [57].
