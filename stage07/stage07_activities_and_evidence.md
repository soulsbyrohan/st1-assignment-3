# Stage 7 Testing and Verification Record

Group/tutorial:  
Members/cohorts:  u3325731 
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.

Use the existing `project/` and preserve earlier tests and stage records.

## A Tutorial Activities

### Activity 1 Requirement to test

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | | | |
| FR-05 Prevent practitioner conflict | Book an available practitioner and confirm the appointment is scheduled. | Attempt to book the same practitioner at the same date and time as an existing scheduled appointment. | A valid booking is stored; a conflicting booking raises `ValueError` and leaves existing records unchanged. |
| FR-06 Cancel appointment | | | |
| FR-07 Retain cancelled history | | | |

### Activity 2 Strong or weak assertion

`assert True`  
Judgement:  
Why:  

`assert appointment is not None`  
Judgement:  
Why:  

`assert appointment.status == AppointmentStatus.CANCELLED`  
Judgement:  
Why:  

`assert len(results) > 0`  
Judgement:  
Why:  

`assert data_store.find_appointment('A1') is appointment`  
Judgement:  
Why:  

### Activity 3 Boundary thinking

For each input/state, expected result and supporting contract:

- **Same-time practitioner booking:** Two appointments with the same practitioner and exact date/time, with the first appointment `SCHEDULED`, must cause the second booking to raise `ValueError` (FR-05).
- **Different practitioner at the same time:** Both bookings are allowed because the conflict rule applies per practitioner (FR-05).
- **Same practitioner one minute later:** Both bookings are allowed under the exact-datetime conflict rule (FR-05).
- **Cancelled appointment:** The original appointment remains stored with `CANCELLED` status and its time slot may be booked again (FR-05 / FR-07).
- **Rejected conflict:** No new appointment is stored and the original appointment remains unchanged (FR-05).

### Activity 4 Critique GitHub Copilot tests

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

### Tutorial exit question


## B Requirement to Test Traceability Matrix

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-05 | | TEST-FR05-01 | Positive | `tests/test_services.py::test_fr05_available_practitioner_booking` | Available practitioner can be booked; appointment has correct participants, date/time and `SCHEDULED` status. | PASS | Student-authored |
| FR-05 | | TEST-FR05-02 | Negative | `tests/test_services.py::test_fr05_same_practitioner_same_time_rejected` | Same practitioner at the same date/time is rejected with `ValueError`; no second record is created. | PASS | Student-authored |
| FR-05 | | TEST-FR05-03 | Positive | `tests/test_services.py::test_fr05_different_practitioners_same_time_allowed` | Different practitioners may each have an appointment at the same date/time. | PASS | Student-authored |
| FR-05 | | TEST-FR05-04 | Boundary | `tests/test_services.py::test_fr05_same_practitioner_different_times_allowed` | Same practitioner can be booked at 09:00 and 09:01. | PASS | Student-authored |
| FR-05 / FR-07 | | TEST-FR05-05 | Positive / state transition | `tests/test_services.py::test_fr05_cancelled_slot_can_be_rebooked` | Cancelled appointment remains stored; a replacement booking at the same slot succeeds. | PASS | Student-authored |
| FR-05 | | TEST-FR05-06 | Negative / integrity | `tests/test_services.py::test_fr05_conflict_does_not_modify_existing_booking` | Rejected booking leaves original appointment fields and appointment collection unchanged. | PASS | Student-authored |

## C Test Design

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-FR05-01 | FR-05 | | Positive | Book a registered practitioner in an available slot. | Stored appointment is `SCHEDULED`, with correct patient, practitioner and date/time. | Establishes the successful booking baseline for conflict tests. |
| TEST-FR05-02 | FR-05 | | Negative | Book the same practitioner at the exact same time as an existing scheduled booking. | `ValueError`; original remains and attempted second booking is absent. | Explicitly verifies conflict rejection and no additional record. |
| TEST-FR05-03 | FR-05 | | Positive | Book two different practitioners at the same time. | Both appointments are `SCHEDULED`. | Confirms conflict checking is practitioner-specific. |
| TEST-FR05-04 | FR-05 | | Boundary | Book the same practitioner at 09:00 and 09:01. | Both bookings succeed. | Verifies the exact-datetime boundary, not duration overlap. |
| TEST-FR05-05 | FR-05 / FR-07 | | Positive / state transition | Cancel an appointment, then book its former slot. | Original remains `CANCELLED`; replacement is `SCHEDULED`; both records remain. | Checks that cancelled history does not block rebooking. |
| TEST-FR05-06 | FR-05 | | Negative / integrity | Attempt a conflicting booking and inspect the stored appointment. | Original appointment fields remain unchanged; collection contains only original. | Verifies preservation of state after rejection. |

## D Arrange Act Assert Record

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-FR05-01 | Fresh store; registered patient P1 and practitioner D1. | Book A1 at 09:00. | `SCHEDULED`; correct object references, date/time and lookup identity. | Checks the observable successful booking result. |
| TEST-FR05-02 | Fresh store; P1, P2, D1; A1 booked at 09:00. | Attempt A2 for D1 at 09:00. | `pytest.raises(ValueError)`; A1 unchanged, A2 absent, count 1. | Verifies rejection and absence of an unintended write. |
| TEST-FR05-03 | Fresh store; P1, P2, D1, D2. | Book A1 for D1 and A2 for D2 at 09:00. | Both `SCHEDULED`, correct practitioner IDs, count 2. | Demonstrates that a shared time is not globally blocked. |
| TEST-FR05-04 | Fresh store; P1, P2, D1. | Book A1 at 09:00 and A2 at 09:01 for D1. | Both `SCHEDULED`; times differ; count 2. | Exercises the one-minute boundary of exact-time matching. |
| TEST-FR05-05 | Fresh store; P1, P2, D1; A1 booked at 09:00. | Cancel A1 and book A2 in same slot. | A1 `CANCELLED`, A2 `SCHEDULED`, both retrievable, count 2. | Verifies cancellation releases the slot without erasing history. |
| TEST-FR05-06 | Fresh store; P1, P2, D1; A1 booked at 09:00. | Attempt conflicting A2. | `ValueError`; A1 ID, patient, practitioner, time and status unchanged; list equals `[original]`. | Checks that rejection does not mutate existing data. |

## E Domain Test Evidence

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| | | | |

## F Service Test Evidence

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-FR05-01 | Available practitioner booking | FR-05 | `tests/test_services.py::test_fr05_available_practitioner_booking` | PASS |
| TEST-FR05-02 | Reject exact-time double booking | FR-05 | `tests/test_services.py::test_fr05_same_practitioner_same_time_rejected` | PASS |
| TEST-FR05-03 | Allow different practitioners at same time | FR-05 | `tests/test_services.py::test_fr05_different_practitioners_same_time_allowed` | PASS |
| TEST-FR05-04 | Allow same practitioner at different times | FR-05 | `tests/test_services.py::test_fr05_same_practitioner_different_times_allowed` | PASS |
| TEST-FR05-05 | Rebook cancelled slot and retain history | FR-05 / FR-07 | `tests/test_services.py::test_fr05_cancelled_slot_can_be_rebooked` | PASS |
| TEST-FR05-06 | Preserve stored state after conflict rejection | FR-05 | `tests/test_services.py::test_fr05_conflict_does_not_modify_existing_booking` | PASS |

## G Negative and Boundary Cases

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Double-booking prevention | Same practitioner, exact same date/time, existing `SCHEDULED` appointment | `ValueError`; second appointment not stored. | TEST-FR05-02 |
| Practitioner-specific conflict check | Different practitioners, same date/time | Both bookings succeed. | TEST-FR05-03 |
| Exact-time boundary | Same practitioner, 09:00 versus 09:01 | Both bookings succeed. | TEST-FR05-04 |
| Cancelled-slot availability | Same practitioner and time after cancellation | Replacement succeeds; cancelled record retained. | TEST-FR05-05 |
| Rejection integrity | Conflicting appointment request | Original fields and stored appointment count unchanged. | TEST-FR05-06 |

## H GitHub Copilot Test Design

Requirement:  
Acceptance criterion:  
Behaviour to test:  
Human-first test idea/categories:  
Prompt and purpose:  

- Copilot test idea/candidate:  
- What it claims to verify:  
- Requirement trace:  
- Assertion quality:  
- Human critique:  
- Decision:  
- Reason:  
- Final test reference if accepted/modified:  
- Actual verification result:  

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak?  
Why was it weak?  
How did you strengthen it?  
Accepted / modified / rejected test decisions and evidence:  

## J Regression Run

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| `py -m pytest -v` | `project/` | | 33 | 0 | None observed | None observed | Full local regression suite passed after adding six FR-05 tests. |

Individual test runs and changed-order independence evidence: `py -m pytest tests/test_services.py -k "fr05" -v` — six FR-05 tests passed.  
Optional tutor-led demonstration notes:  
Requirement → test → failure/observation → diagnosis → change → verification: FR-05 → TEST-FR05-01 through TEST-FR05-06 → six passing tests; no failure or fix recorded.

## K What the Suite Still Does Not Prove

What does your test suite still not prove? The FR-05 tests verify exact-datetime conflicts in an in-memory store. They do not establish behaviour for overlapping appointment durations, simultaneous requests, persistent storage, or external notifications. Those behaviours are outside the verified FR-05 test scope.  
Coverage if used:  
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? These tests do not measure concurrency or persistence behaviour. Even high line coverage would not prove the correct conflict rule or adequate assertions; tests must check observable requirements.  
Optional fixtures/parametrisation used and why, if any: Not used in the six FR-05 tests; each test creates fresh store state explicitly.

## L Git and Review Evidence

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| FR-05 practitioner booking conflict tests | `feature/stage7-conflict-tests` | https://github.com/soulsbyrohan/st1-assignment-3/pull/7 | | | Six tests pushed; local regression 33 passed, 0 failed. |

## M Contribution Evidence

| Member | Actual contribution | Evidence link |
|---|---|---|
| u3325731 | Designed and implemented six FR-05 service tests covering successful booking, exact-time conflict rejection, different practitioners, different times, cancelled-slot reuse and unchanged state after rejection. Ran six focused tests and the full regression suite (33 passed, 0 failed). | https://github.com/soulsbyrohan/st1-assignment-3/pull/7 |

## N Formative Questions

1. What question does verification answer?  

2. What question does validation answer?  

3. What is a unit test?  

4. What is a pytest fixture?  

5. What is parametrisation in pytest?  

6. What is regression testing?  

7. What does code coverage tell us, and what does it not prove?  

8. What makes an assertion weak?  

9. What is the appropriate role of GitHub Copilot as a test assistant?  

10. What is the Stage 7 engineering rule?  

## O Stage Completion

Tested Stage 7 main SHA:  
Full-suite result:  
Unresolved defects and effect on baseline:  
Clean working tree and integration evidence:  
Stage 8 handover status:  
All tutorial/formative responses and traceability/Copilot decisions complete:  
