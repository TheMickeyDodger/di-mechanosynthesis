# H2-A-01 route-R2 run proposal 02 (enabling revision)

## 1. Status

**PROPOSED_NOT_AUTHORIZED.** This is a preparation-only `[AGENT]` proposal. It authorizes nothing and is not
readiness. It is a short delta to the route-R2 run proposal
[H2-A-R2-RUN-PROPOSAL.md](H2-A-R2-RUN-PROPOSAL.md) (SHA256
`d0239104596409d8f278449103f413843a225550cbfb91616d25d5b5143c2b2e`), which stays frozen and is not restated.

A person approved the method revision [H2-R2-METHOD-REVISION.md](H2-R2-METHOD-REVISION.md) (SHA256
`9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc`), with the approved decision packet
[H2-A-R2-DECISION-PACKET.md](H2-A-R2-DECISION-PACKET.md) as its context. The
[human approval record](H2-R2-METHOD-HUMAN-APPROVAL.md) (SHA256
`e4897a80869bc04d6ece9a8be75673085e18ddb1b07df1df5e71fd4b76f10d7c`) records that decision. It is not a run
authorization, and no run authorization exists. This proposal describes the enabling revision of step 3 of the method
revision §6. These bytes are submitted for independent review. Its decision and any Lead acceptance are recorded in
private task records, not in these bytes.

The frozen proposal's statements that approval is PENDING and that every launch is refused describe the state before
the approval. They are superseded by this proposal for the route-R2 driver, and they are not edited.

## 2. What changed

- **Approval record.** [H2-R2-METHOD-HUMAN-APPROVAL.md](H2-R2-METHOD-HUMAN-APPROVAL.md) is new. It binds the digests
  of the method revision and of the approved decision packet only.
- **The constant.** The route-R2 driver [h2_phase_a_r2_driver.py](h2_phase_a_r2_driver.py), SHA256
  `0b3172f8388b0f0c053a2b7a6945394e7e796aae8b14d0228447d7bc860af9b6`, sets `R2_METHOD_DECISION` to
  `method_revision_sha256` `9498019a…aecdc` and `approval_record_sha256` `e4897a80…10d7c`, in the existing two-key
  shape. These bytes replace the driver bytes `eadbde6b…318fe` that the approved packet records.
- **Approval-bytes binding.**
  - The approval record is a bound route-R2 file, under the key `method_revision_approval`. The driver hashes it at
    the first preflight, at the final preflight immediately before spawn and after the process ends.
  - The check `r2.method_revision_decision` passes only while the method revision and the approval record on disk
    have the constant's digests. It names an absent or unreadable record and a record with other bytes separately.
  - The authorization's `bound_sha256.method_revision_approval` must equal the record's digest on disk and the
    constant.
  - A change to the record during a run adds two reasons to the accepted classification: the failed post-run check
    `r2.method_revision_decision` and "bundle files changed during the run".
- **Unchanged.** The authorization schema and its sixteen keys, the eight code-provenance paths, the attempt-root
  entries, the profile parameters, the launched command, the run sequence, the post-run observations and groups, the
  pin of the accepted driver, the classification, one attempt and zero retries, and every scientific setting.

## 3. What refuses launch now

- **The method gate passes for the approved bytes.** It would refuse with `NETWORK_PREREQUISITE_UNRESOLVED` if
  `R2_METHOD_DECISION` were unset. The tests keep that path.
- **A launch requires an authorization file that satisfies every interlock check.** No run authorization exists.
  Without one, or with any mismatch, the driver refuses with BLOCK_LAUNCH and starts no process.
- **The interlock checks bytes, not people.** It compares bytes and fields only and cannot show that a person
  authorized anything.
- **The accepted Phase A driver** [../phase-a/h2_phase_a_driver.py](../phase-a/h2_phase_a_driver.py) is unchanged.
  It still refuses every launch with `NETWORK_PREREQUISITE_UNRESOLVED`. The method revision applies only to launches
  by the route-R2 driver.

## 4. Unchanged invocation, control and classification

The following are those of the frozen proposal §§4–9 and of R2-S in the approved method revision, unchanged:
- the three driver commands and the wrapped command that `run` would spawn;
- the bound profile and its write parameters;
- the platform checks of `sandbox-exec` and the OS build;
- the post-run observations;
- the classification: every reason is kept, FAILED takes precedence, a valid payload stop stays STOP_BEFORE_ENERGY,
  and otherwise the tier is QUARANTINE.

## 5. Bindings of a future run authorization

- **Sixteen keys, unchanged.** The interlock keys are those of the frozen proposal §9 and the approved packet §4.
  Their current values are listed in the run-decision packet
  [H2-A-R2-RUN-DECISION-PACKET.md](H2-A-R2-RUN-DECISION-PACKET.md).
- **Frozen context files stay bound.** `r2_run_proposal` stays the frozen `H2-A-R2-RUN-PROPOSAL.md`, and
  `r2_decision_packet` stays the approved `H2-A-R2-DECISION-PACKET.md`.
- **Documentary files.** This proposal and the run-decision packet are not interlock keys. A future run authorization
  must name both by SHA256 in its statement: this proposal's digest is in the run-decision packet, and the packet's
  digest is in the export manifest. The driver does not check that statement.

## 6. Code-provenance freshness

- The record must be written by the driver's `code-provenance` mode from the final reviewed bytes.
- It becomes stale after a commit, a change to any of the eight paths or a moved HEAD. The driver then refuses launch
  with `code provenance mismatch`, and a new record and a new authorization binding are needed.
- A fresh private record was written from these bytes. Only a run authorization binds its digest; no public file
  records it.

## 7. Machine binding

The private machine binding R2-01 (SHA256 `7a5ac67dd8c6f196955589e8d6e8c0f96240db10c42a01d043974d0feee884b0`) is
carried unchanged. Its operative fields are unchanged and still match the driver:
- interpreter, prefix and runs root;
- environment;
- the wrapped command.

Its status sentence, that the route-R2 driver refuses every launch until a person decides the method revision and a
reviewed revision sets `R2_METHOD_DECISION`, predates the approval and is superseded by this proposal. R2-01 also
records that the runs root did not exist when R2-01 was written and must be created empty before any authorized run.
Nothing here re-observes it.

## 8. Test evidence

The evidence is source [57]. Fake outputs are not chemistry evidence, and the fixture authorizations used are not
authorizations.
- **Route-R2 suite.** The 32 tests of [tests/](tests/) pass on these bytes. They cover:
  - the shipped constant, equal to the approved method digest and to the approval record's digest, with no digest
    of the driver, the tests or the new documents in the record;
  - the enabled path under a FIXTURE authorization: COMPLETED_PENDING_REVIEW through the real wrapper;
  - the approval record absent, unreadable, altered by one byte, replaced, or changed after authorization;
  - an authorization whose approval digest differs or whose key is missing;
  - a constant that differs from the files on disk, by FIXTURE patch, and a malformed constant;
  - the unset gate (`NETWORK_PREREQUISITE_UNRESOLVED`) and the accepted driver's refusal;
  - an authorization file that is absent, not JSON or not an object, and both templates;
  - every earlier binding negative, with the exact sixteen keys;
  - the approval record changed during a run, which gives QUARANTINE with both reasons;
  - the preserved behaviours, and real-sandbox prevention around fake processes against unsandboxed controls.

  Every refused launch spawned no process and wrote nothing to the runs root.
- **Accepted Phase A suite.** Its 37 tests pass unchanged.
- **Mutation check.** Ten single changes to the driver were run privately, together with one unmutated control. They
  cover each changed executable line and the comparison of the authorization's approval digest with the constant.
  Both runs are kept as recorded.
  - **First run, as recorded.** Three changes were killed by their intended assertion. Six were classified invalid
    under the run's strict rule, because some failures did not match its declared patterns, and in one case a test
    raised an error. The documentary change survived.
  - **Intended-assertion observation.** It reads the same first-run outputs with the patterns declared before that
    run. In eight runs, an intended test failed by assertion with the modelled defect visible. Three are the runs
    recorded as killed. The other five are runs recorded invalid. Their incidental failures, and in one of them a test
    error, remain part of the run, and their classification is unchanged. Eight is not a kill count.
  - **Second run.** It repaired only the classifier's patterns and used a test variant that was later withdrawn. It
    is not counted.

  Traced through the driver's paths, none of the ten changes was shown to permit a launch that the unmutated driver
  refuses:
  - five are fail-closed. They break the enabled path, so that every launch is refused, including legitimate ones;
  - four change no launch decision. Each changes only a message, the stage of a refusal or a post-run reason. They
    include the separate message for an absent record, and the constant comparison in the interlock, which is
    redundant and shows only in the exact reason string;
  - one changes descriptive text in the provenance record and survives.

  These are `[AGENT]` assessments. Their independent assessment belongs to review.

## 9. Remaining decision and open items

**Remaining decision.** A separate, bounded human run authorization of exactly one attempt, at the bytes listed in
the run-decision packet. Nothing in this proposal makes that decision.

**Open, and not accepted on anyone's behalf:**
- M1: engine memory is not an operating-system limit;
- E1: the engine interpreter's environment is unobserved;
- the Libint load-name risk;
- loaded identity;
- P4, the meaning of the reported total energy;
- source-to-binary correspondence;
- the engine's compatibility with the profile, which is unobserved;
- the gaps of R2-S item 5, as the person approved them.

**Phase B** is separate. It needs its own decision after an authorized Phase A run and an independent review of its
result.

**Gates.** H2 is NOT_RUN. W1 is STOPPED (S10). E-01 is technically BLOCKED and scientifically INDETERMINATE. C3
readiness, MS-001 Stage 1 and option A are BLOCKED.

Sources: [../../../SOURCES.md](../../../SOURCES.md) entries [55], [56] and [57].
