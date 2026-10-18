# H2-A-01 human decision packet (Phase A)

## 1. What this packet is

This is a redacted, public preparation record for a person's decision about the first H2 single point, job
`H2-A-01`. It is **not an authorization** and authorizes nothing. The package is **not runnable** and not ready.

The bound driver refuses every launch with `NETWORK_PREREQUISITE_UNRESOLVED` (gate N1). A run would need, in this
order:
- a revision of the driver (and possibly a profile) under one of the routes in §4;
- a renewed independent review of those exact bytes;
- a person's separate decision on them.

This package contains none of these. The technical proposal is [H2-A-01-RUN-PROPOSAL.md](H2-A-01-RUN-PROPOSAL.md).

## 2. The bound files

Any authorization would bind these exact SHA256 digests; the driver checks them. The packet's own digest is recorded
in the export manifest and would be bound in the authorization file. The private machine binding holds the absolute
paths, the concrete command and the host facts. It is named here by digest only.

The authorization would also bind a detached, private code-provenance record (proposal §9). The record is written by
`h2_phase_a_driver.py code-provenance` after the final bytes. It covers the five code paths of a run against the
base commit. The driver re-derives it from read-only Git queries before launch and blocks if it is absent,
mismatched or unresolvable. Its digest is bound by the authorization and by the review inventory, not by this packet,
so no public file has to contain it.

<!-- BOUND-DIGESTS:BEGIN -->
| Binding key | File | SHA256 |
|---|---|---|
| `driver` | phase-a/h2_phase_a_driver.py | `6dcb4845e3b4b29f89dc4027274675e24c1152508828b1230857baac58b9aa7d` |
| `payload` | phase-a/h2_phase_a_payload.py | `7de1d53c70af7a4ff3a71fb5fbcd7cedfec24a7e3eb49d8b27f9d6bf6cc2f69b` |
| `input` | phase-a/h2-a-01-input.json | `3ca4753312b3f2cd50274d4c8f8dda48de422d691e34bf47784b1602670dc3d3` |
| `parameters` | h2-method-parameters.json (accepted, unchanged) | `2728b0efe2c6dae070346a3d0475857222f02864a6da63859edf4d4e334c156e` |
| `static_identity` | phase-a/h2-a-01-static-identity.json | `a45ee84d0d28e794ea7f56e7ff74130551fb326c36c7d8353467966ed2c025cc` |
| `run_proposal` | phase-a/H2-A-01-RUN-PROPOSAL.md | `d9bcb7e186a0ced226478d93470682c6ff84c78abab1f7546eb45bdac551225f` |
| `machine_binding` | private machine binding, revision 03 (not published) | `9a95bdebef27eea75a9aef72bce0d9b3f288ff4848fd92f24b18b7b17b17664e` |
| `decision_packet` | this file | recorded in the export manifest (a file cannot contain its own digest) |
| `code_provenance` | detached private code-provenance record (§2 above) | bound by the authorization and the review inventory, not recorded here |
<!-- BOUND-DIGESTS:END -->

Reviewed but not bound into the launch: the test files and fixtures under [tests/](tests/), with digests in the
export manifest.

## 3. What a person would be deciding, and what not

**In scope of an eventual authorization**, after N1 is resolved by revised and re-reviewed bytes:
- one attempt (`max_attempts 1`, zero retries);
- one engine process;
- the command, in placeholder form:

  ```
  <PREFIX>/bin/python3.14 -I -B <RUNS_ROOT>/H2-A-01/bundle/h2_phase_a_payload.py <RUNS_ROOT>/H2-A-01/bundle/h2-a-01-input.json <RUNS_ROOT>/H2-A-01
  ```

  launched only through `h2_phase_a_driver.py run` with the allow-list environment, 1 thread, an engine memory setting
  of 500 MiB, a 300 s wall bound and the accepted options (proposal §3).

**Never in scope:**
- Phase B;
- any second attempt or retry;
- any changed setting, fallback or other engine;
- installation, building or network access;
- any change to the accepted lesson, specification or parameter file;
- any MS-001, E-01 or W1 action, or any C3, Stage 1 or option A step;
- publication of results.

Any of these would need its own decision.

## 4. Conditional gates the person must resolve or accept

**N1, network and installation. A genuine blocker; the driver refuses launch.**
1. *Accepted language*, from [h2-method-parameters.json](../h2-method-parameters.json):
   - "any network access or installation attempt", with the rule "stop the sequence, keep all output, mark remaining
     points NOT_RUN, change no setting";
   - P5: "no network access".
2. *What is established* (proposal §8.5):
   - The driver applies no network control.
   - Before, immediately before and after the run, it compares the names of all `conda-meta/` entries, the full-file
     digests and declared fields of the two bound package records, and the five bound files and the bundle files. Any
     change, or any failed post-run identity check, is QUARANTINE.
   - Installed macOS documentation marks `sandbox-exec` deprecated and states that children inherit a sandbox. The SDK
     `sandbox.h` documents deprecated named profiles, for example "All sockets-based networking is prohibited".
   - A fixture under a candidate custom profile was refused AF_UNIX and `127.0.0.1` connections, with a grandchild
     inheriting the refusal, and was refused writes outside one directory [55].
3. *Remaining gap*:
   - no control is applied by the driver;
   - the custom-profile semantics are undocumented;
   - refusal is not detection;
   - other destinations and service-mediated traffic are untested;
   - the engine's behaviour under a profile is unobserved;
   - installation that touches only files outside the compared set is not detected: other package records' contents,
     other prefix files, anything outside the prefix, in-memory downloads, and changes reverted between samples.

Routes, each needing revised bytes, a renewed review and a further decision:
- **R1**, a bound `sandbox-exec` profile as prevention, plus a detection record with sourced semantics;
- **R2**, a method revision by a person accepting prevention without detection;
- **R3**, a driver-observed offline host state before and after, accepted as two instants only.

**M1, memory.** 500 MiB is an engine setting only. No operating-system memory limit is applied, and peak resident
memory of the direct child is merely observed. To be accepted or resolved.

**E1, environment.** If the engine process holds any environment name other than the allow-list and the declared
platform name `__CF_USER_TEXT_ENCODING`, it stops before energy, and that spends the single attempt. Whether the
candidate interpreter adds any such name has not been observed, because it was never run.

**Identity limits.**
- Static installed identity was observed on 2026-10-10 and must be re-checked at launch.
- Loaded identity is observed only inside a run, after the engine's import-time initialization.
- Which file the loader resolves for the core extension's `@rpath/libint2.dylib` dependency is not established. If it
  is not `<PREFIX>/lib/libint2.dylib`, the run stops at I1 and spends the attempt (proposal §6).
- The driver re-checks every gate-defining recorded value against its binding. The fields recorded only for review are
  listed with reasons in proposal §9a.
- Source-to-binary correspondence and the meaning of the reported total energy (P4) remain unproved.

## 5. Options

- **Choose a route for N1 (R1, R2 or R3).** This leads to a revised package and a renewed independent review, and
  only then to a decision on authorizing one attempt. This packet does not authorize anything on that route.
- **Decline.** Phase A stays NOT_RUN. Phase B stays CONDITIONAL_NOT_AUTHORIZED.
- **Request other changes.** Name them.
- *Authorizing these bytes as bound* would produce no run, because the bound driver refuses launch. It is listed only
  so that this is explicit.

## 6. Blank template, which is not an authorization

The schema value below is deliberately invalid, so the driver rejects this template as written. A real authorization
would use exact values, created by the person, only after a reviewed revision resolves N1.

```json
{
  "schema": "TEMPLATE-NOT-AN-AUTHORIZATION",
  "job_id": "H2-A-01",
  "max_attempts": 1,
  "authorized_by": "<NOT FILLED>",
  "authorized_utc": "<NOT FILLED>",
  "statement": "<NOT FILLED: this template authorizes nothing>",
  "bound_sha256": {
    "driver": "<NOT FILLED>", "payload": "<NOT FILLED>", "input": "<NOT FILLED>", "parameters": "<NOT FILLED>",
    "static_identity": "<NOT FILLED>", "run_proposal": "<NOT FILLED>", "decision_packet": "<NOT FILLED>",
    "machine_binding": "<NOT FILLED>", "code_provenance": "<NOT FILLED>"
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

## 7. Status of gates

All gates are unchanged:
- W1 STOPPED (S10).
- E-01 technically BLOCKED and scientifically INDETERMINATE.
- C3 readiness, MS-001 Stage 1 and option A BLOCKED.

H2 with `DIRECT` neither exercises nor diagnoses E-01's PK path. This packet is not readiness, parity, physical
evidence or a review decision.

Sources: [../../../SOURCES.md](../../../SOURCES.md) entries [31], [39], [48], [50], [52]–[55].
