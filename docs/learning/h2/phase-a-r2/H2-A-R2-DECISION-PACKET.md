# H2-A-01 route-R2 human decision packet

## 1. What this packet is

This is a redacted, public preparation record for a person's decision. It is **not an authorization** and
authorizes nothing. Human approval is **PENDING**. Nothing here is runnable: the route-R2 driver and the accepted
driver both refuse every launch with `NETWORK_PREREQUISITE_UNRESOLVED`.

The technical description is [H2-A-R2-RUN-PROPOSAL.md](H2-A-R2-RUN-PROPOSAL.md). The accepted Phase A packet,
[H2-A-01-DECISION-PACKET.md](../phase-a/H2-A-01-DECISION-PACKET.md), is unchanged; this packet follows its route R2.

## 2. What is decided now

Only one thing: **approve, decline or change the exact bytes of
[H2-R2-METHOD-REVISION.md](H2-R2-METHOD-REVISION.md)** (SHA256
`9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc`).

If approved, that text would replace, for job H2-A-01 launched by the route-R2 driver only, the accepted stop
condition "any network access or installation attempt" and the "no network" part of P5. The replacement is
prevention by a bound sandbox profile, inherited by descendants, with **no detection** of refused attempts. Every
other stop condition, every setting, the rule "stop the sequence, keep all output, mark remaining points NOT_RUN,
change no setting", one attempt and zero retries stay as accepted. Phase B is not affected.

The accepted classification is also unchanged. The post-run observations of the revision add reasons to it:
- every reason is kept;
- FAILED takes precedence;
- a valid payload stop stays STOP_BEFORE_ENERGY;
- otherwise the tier is QUARANTINE.

Not decided now:
- any run;
- the implementation revision that would set `R2_METHOD_DECISION`;
- M1;
- E1;
- Phase B;
- anything else.

## 3. Bound digests

These are the current bytes. Where a later step changes a row, the row says so.

<!-- BOUND-DIGESTS:BEGIN -->
| Binding key | File | SHA256 |
|---|---|---|
| `r2_method_revision` | phase-a-r2/H2-R2-METHOD-REVISION.md (the bytes decided now) | `9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc` |
| `r2_run_proposal` | phase-a-r2/H2-A-R2-RUN-PROPOSAL.md | `d0239104596409d8f278449103f413843a225550cbfb91616d25d5b5143c2b2e` |
| `r2_profile` | phase-a-r2/h2-r2-sandbox.sb | `0768725ab376312c4b22dc83f47b13eeaa67c62dc618dd350c9ab47a2f754d20` |
| `r2_platform_identity` | phase-a-r2/h2-r2-platform-identity.json | `822fbe69807184f8ac5c180caa74d23b0faca64e055ee4bc09a61c82019f2659` |
| `r2_driver` | phase-a-r2/h2_phase_a_r2_driver.py (current bytes; step 3 of the method revision §6 replaces them) | `eadbde6b5dd405f10c264a63135bafc1a8904a47a7a5c01bca162bf18cd318fe` |
| `driver` | phase-a/h2_phase_a_driver.py (accepted, unchanged) | `6dcb4845e3b4b29f89dc4027274675e24c1152508828b1230857baac58b9aa7d` |
| `payload` | phase-a/h2_phase_a_payload.py (accepted, unchanged) | `7de1d53c70af7a4ff3a71fb5fbcd7cedfec24a7e3eb49d8b27f9d6bf6cc2f69b` |
| `input` | phase-a/h2-a-01-input.json (accepted, unchanged) | `3ca4753312b3f2cd50274d4c8f8dda48de422d691e34bf47784b1602670dc3d3` |
| `parameters` | h2-method-parameters.json (accepted, unchanged) | `2728b0efe2c6dae070346a3d0475857222f02864a6da63859edf4d4e334c156e` |
| `static_identity` | phase-a/h2-a-01-static-identity.json (accepted, unchanged) | `a45ee84d0d28e794ea7f56e7ff74130551fb326c36c7d8353467966ed2c025cc` |
| `run_proposal` | phase-a/H2-A-01-RUN-PROPOSAL.md (accepted, unchanged) | `d9bcb7e186a0ced226478d93470682c6ff84c78abab1f7546eb45bdac551225f` |
| `decision_packet` | phase-a/H2-A-01-DECISION-PACKET.md (accepted, unchanged) | `cfb4a9912114452211e19edadf115816e48359911e05f48d71c54672b72b55e5` |
| `machine_binding` | private route-R2 machine binding, current revision R2-01 (not published; embeds no public-file digest) | `7a5ac67dd8c6f196955589e8d6e8c0f96240db10c42a01d043974d0feee884b0` |
| `r2_decision_packet` | this file | recorded in the export manifest (a file cannot contain its own digest) |
| `code_provenance` | private code-provenance record (proposal §9) | a fresh record, bound only by the run authorization; no public file records it |
| `method_revision_approval` | human approval record | does not exist; created only if a person approves (method revision §6, step 2) |
<!-- BOUND-DIGESTS:END -->

The tests and fixtures under [tests/](tests/) were reviewed but are not bound into a launch. Their digests are in the
export manifest.

## 4. What a later run authorization would bind

A later run authorization, which is not part of this decision, would bind:
- the sixteen keys above, with `r2_driver` at the bytes of the reviewed implementation revision and
  `machine_binding` at the machine-binding revision it uses;
- a fresh code-provenance record written after those bytes;
- the digest of the approval record.

Its scope would be one attempt (`max_attempts 1`, zero retries) and one engine process, launched only through
`h2_phase_a_r2_driver.py run`, with the wrapped command of proposal §4 and the accepted settings.

The following would never be in its scope:
- Phase B;
- a second attempt or a retry;
- any changed setting, fallback or other engine;
- installation, building or network access;
- any change to the accepted lesson, specification or parameter file;
- any MS-001, E-01 or W1 action;
- publication of results.

## 5. Options

- **Approve these method-revision bytes.** This leads, in order, to:
  1. a human approval record binding this file's digest and the revision's digest;
  2. a separately reviewed driver revision that sets `R2_METHOD_DECISION` to those digests;
  3. a separate, bounded human run authorization.

  Only then could one attempt run.
- **Decline.** N1 stays in force, Phase A stays NOT_RUN and Phase B stays CONDITIONAL_NOT_AUTHORIZED.
- **Request changes.** Name them. Changed bytes need a renewed independent review and a new decision.

What the person accepts by approving, and what remains open, is listed in item 5 of R2-S in the method revision:
- there is no detection;
- the profile semantics are undocumented and fixture-observed only;
- `sandbox-exec` is deprecated;
- service-mediated traffic is not covered;
- the engine's compatibility with the profile is unobserved, and a refusal that breaks the engine spends the single
  attempt;
- the compared-set gaps remain;
- the Libint load-name risk remains.

## 6. Template, deliberately invalid

The schema value below is deliberately invalid, so the driver rejects this template as written. It is not an
authorization.

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

## 7. Gates

These remain open and unchanged:
- M1: engine memory is not an operating-system limit;
- E1: the engine interpreter's environment is unobserved;
- the Libint load-name risk;
- loaded identity;
- P4, the meaning of the reported total energy;
- source-to-binary correspondence.

The project gates are unchanged:
- W1 STOPPED (S10);
- E-01 technically BLOCKED and scientifically INDETERMINATE;
- C3 readiness, MS-001 Stage 1 and option A BLOCKED.

This packet is not readiness, parity, physical evidence or a review decision.

Sources: [../../../SOURCES.md](../../../SOURCES.md) entries [55] and [56].
