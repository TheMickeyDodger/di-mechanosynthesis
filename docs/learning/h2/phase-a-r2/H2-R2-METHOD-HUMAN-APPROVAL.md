# H2 route-R2 method revision: human approval record

Date of record: 2026-10-10. This is the date on which a person's answer was recorded on its receipt by the separate
orchestration system that governs this project. It is not an independently measured time of the answer, and this
record states no time.

## 1. The decision

| Element | Value |
|---|---|
| Decision | APPROVE |
| Answer, verbatim | "approve" |
| Question answered, verbatim | "Do you approve those exact revision bytes? This would permit preparing the reviewed enabling change; a calculation still needs separate run authorization." |
| Date of record | 2026-10-10, the date of receipt of the answer |
| Private reply record | SHA256 `fa7b367f793b39c3197c2b4ab639d61ac2e1bb8b5056a8776f9385f973bb7fbb`. It is not published |

The question was put to a person directing this project, through the separate orchestration system, after the
independent review of the route-R2 preparation package. This record carries no personal name and no task, session or
agent identifier.

## 2. Bytes approved

| File | SHA256 | Role |
|---|---|---|
| [H2-R2-METHOD-REVISION.md](H2-R2-METHOD-REVISION.md) | `9498019a23a8fa1542788b17126b91e3fff93ada49639856f6599e3afc8aecdc` | The method revision decided |
| [H2-A-R2-DECISION-PACKET.md](H2-A-R2-DECISION-PACKET.md) | `5ce61f7c97be6db8e332d296d3f54335acb04552296d33eb230ce40cbd9c4083` | The accompanying decision context |

A file at either path with any other digest does not carry the approved bytes.

## 3. Scope

- The approval applies to job H2-A-01 launched by the route-R2 driver, `h2_phase_a_r2_driver.py run`, only. For that
  job, R2-S and R2-P5 take the place of the accepted texts A1 to A4
  ([method revision §§3–4](H2-R2-METHOD-REVISION.md#3-accepted-texts-this-revision-would-supersede-for-h2-a-01)).
- The person accepted the prevention coverage and detection gaps exactly as listed in item 5 of R2-S in the approved
  bytes, and no others.
- Preparation of the separately reviewed enabling revision of
  [method revision §6](H2-R2-METHOD-REVISION.md#6-decision-sequence-and-digest-graph), step 3, is permitted.

## 4. What this record is not

- It is not a run authorization. It permits no engine command, import or initialization and no calculation.
- It is not a decision on M1, E1 or any other open item: the Libint load-name risk, loaded identity, P4 and
  source-to-binary correspondence stay open.
- It is not a decision on Phase B.
- It permits no installation, build or system change.
- It permits no W1 action, AiiDA action, MS-001 Stage 1 work or option A work.
- It authorizes no commit or publication.
- It is not readiness or physical evidence, and it changes no evidence label.

## 5. Frozen status texts

The approved method revision (§1, "Human approval PENDING") and the approved decision packet (§1, "Human approval is
PENDING") still state that approval is pending. These are the frozen bytes the person approved. They are
superseded by this record and are not edited, because an edit would create bytes that no person approved.

## 6. Digest graph

This record binds the two approved files only. A later file may bind this record's digest, as step 3 of the method
revision §6 does for the route-R2 driver. This record binds no later file, so no digest cycle arises.

## 7. Gates

All gates are unchanged. W1 is STOPPED (S10). E-01 is technically BLOCKED and scientifically INDETERMINATE. C3
readiness, MS-001 Stage 1 and option A are BLOCKED. H2 is NOT_RUN, and Phase B is not authorized.
