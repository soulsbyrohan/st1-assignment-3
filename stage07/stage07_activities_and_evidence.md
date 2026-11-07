# Stage 7 Testing and Verification Record
Group/tutorial:  Wednesday (14:30-16:30)

Members/cohorts:  u3325731 

Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.

Use the existing `project/` and preserve earlier tests and stage records.

## A Tutorial Activities
### Activity 1 Requirement to test
| Requirement | Positive test | Negative test | Key assertion |

|---|---|---|---|

| FR-01 Register patient | Register patient with valid ID | Register a patient with an existing ID | Patient can be found in data store from registered |
| FR-05 Prevent practitioner conflict | Book an available practitioner and confirm the appointment is scheduled. | Attempt to book the same practitioner at the same date and time as an existing scheduled appointment. | A valid booking is stored; a conflicting booking raises `ValueError` and leaves existing records unchanged. |
| FR-06 Cancel appointment | [response] | [response] | [response] |
| FR-07 Retain cancelled history | [response] | [response] | [response] |

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

- ****Same-time practitioner booking:** Two appointments with the same practitioner and exact date/time, with the first appointment `SCHEDULED`, must cause the second booking to raise `ValueError` (FR-05).

- ****Different practitioner at the same time:** Both bookings are allowed because the conflict rule applies per practitioner (FR-05).

- ****Same practitioner one minute later:** Both bookings are allowed under the exact-datetime conflict rule (FR-05).

- ****Cancelled appointment:** The original appointment remains stored with `CANCELLED` status and its time slot may be booked again (FR-05 / FR-07).

- ****Rejected conflict:** No new appointment is stored and the original appointment remains unchanged (FR-05).
Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: 

| Candidate | Expected Result | Contract Supporting the Expectation |
|---|---|---|
| Patient ID = ‘’ | ValueError is raised | Blank patient IDs are rejected |
| Patient name = ‘   ’ | ValueError is raised | Whitespace-only names are rejected |
| Valid but unknown patient ID lookup | LookupError is raised | Known patient lookup succeeds; unknown patient lookup reports absence |
| Two appointments book the same practitioner at the same datetime | Second booking attempt is rejected and ValueError is raised | Same practitioner/exact time/SCHEDULED conflicts; another practitioner at the same time is allowed |
| Appointment status = CANCELLED and then appointment cancellation is attempted again | Status remains CANCELLED and ValueError is raised | Repeated cancellation is rejected |
| Appointment status = COMPLETED and then appointment cancellation is attempted | Status remains COMPLETED and ValueError is raised | Cancelling a SCHEDULED appointment changes it to CANCELLED; cancelling is only permitted when status is SCHEDULED |

### Activity 4 Critique GitHub Copilot tests

These are the five example test problems from the tutorial, not tests that Copilot generated for our project.

| Candidate | What's wrong with it | Better test idea |
|---|---|---|
| 1 — Only checks `is not None` | It only tells us a patient object exists. It doesn't check whether the details were saved correctly. | Register a patient, look them up by ID, and check that the ID and name match what was entered (FR-01). |
| 2 — Only checks a booking exists | A booking object existing doesn't tell us whether it was scheduled correctly or whether double booking is blocked. | Make a valid booking and check its status. Then try the same practitioner at the same time and check for `ValueError` and no extra booking (FR-05). |
| 3 — Uses `assert True` | This would pass every time, even if the program wasn't working. | Cancel a scheduled appointment and check that its status changes to `CANCELLED` (FR-06). |
| 4 — Expects an SMS after booking | SMS notifications aren't part of the behaviour we're testing, so this would be checking something outside the requirements. | Check that the booking is stored with the right practitioner, time and `SCHEDULED` status (FR-04/FR-05). |
| 5 — Expects an SMS after cancellation | Same problem as above. It assumes the system sends messages when that isn't in the stated contract. | Cancel the appointment, find it again, and check that it is still saved as `CANCELLED` (FR-06/FR-07). |

### Tutorial exit question
## B Requirement to Test Traceability Matrix
| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 | AC-01.1 under FR-01 | Test-01-01 | Service | test_register_patient_valid_patient_unused_id_is_stored() in test_services.py | Patient data is successfully registered and stored in data store | Passed | Student-authored  |
| FR-01 | AC-01.2 under FR-01 | Test-01-02 | Service | test_duplicate_patient_id_is_rejected() in test_services.py | Duplicate patient ID is rejected at registration and raises ValueError | Passed | Student-authored  |
| FR-01 | Patient with name and ID is created | Test-01-03 | Domain | test_patient_valid_construction() in test_domain.py | Patient is created with the correct ID and name | Passed | Student-authored  |
| FR-01 | Blank ID is rejected | Test-01-04 | Domain | test_blank_patient_id_rejected() in test_domain.py | Patient ID is rejected and raises ValueError | Passed | Student-authored  |
| FR-01 | Whitespace characters as ID are rejected | Test-01-05 | Domain | test_whitespace_patient_id_rejected() in test_domain.py | Patient ID is rejected and raises ValueError | Passed | Student-authored  |
| FR-01 | Blank name is rejected | Test-01-06 | Domain | test_blank_patient_name_rejected() in test_domain.py | Patient name is rejected and raises ValueError | Passed | Student-authored  |
| FR-01 | Whitespace characters as name are rejected | Test-01-07 | Domain | test_whitespace_patient_name_rejected() in test_domain.py | Patient name is rejected and raises ValueError | Passed | Student-authored  |

| FR-05 | | TEST-FR05-01 | Positive | `tests/test_services.py::test_fr05_available_practitioner_booking` | Available practitioner can be booked; appointment has correct participants, date/time and `SCHEDULED` status. | PASS | Student-authored |
| FR-05 | | TEST-FR05-02 | Negative | `tests/test_services.py::test_fr05_same_practitioner_same_time_rejected` | Same practitioner at the same date/time is rejected with `ValueError`; no second record is created. | PASS | Student-authored |
| FR-05 | | TEST-FR05-03 | Positive | `tests/test_services.py::test_fr05_different_practitioners_same_time_allowed` | Different practitioners may each have an appointment at the same date/time. | PASS | Student-authored |
| FR-05 | | TEST-FR05-04 | Boundary | `tests/test_services.py::test_fr05_same_practitioner_different_times_allowed` | Same practitioner can be booked at 09:00 and 09:01. | PASS | Student-authored |
| FR-05 / FR-07 | | TEST-FR05-05 | Positive / state transition | `tests/test_services.py::test_fr05_cancelled_slot_can_be_rebooked` | Cancelled appointment remains stored; a replacement booking at the same slot succeeds. | PASS | Student-authored |
| FR-05 | | TEST-FR05-06 | Negative / integrity | `tests/test_services.py::test_fr05_conflict_does_not_modify_existing_booking` | Rejected booking leaves original appointment fields and appointment collection unchanged. | PASS | Student-authored |

## C Test Design
| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |

|---|---|---|---|---|---|---|
| Test-01-01 | FR-01 | AC-01.1 under FR-01 | Positive | Verify that a patient with valid data can be registered and stored | Patient data is successfully registered and stored in data store | [complete] |
| Test-01-02 | FR-01 | AC-01.2 under FR-01 | Negative | Verify that duplicate patient IDs are rejected at registration | Duplicate patient ID is rejected at registration and raises ValueError | [complete] |
| Test-01-03 | FR-01 | Patient with name and ID is created | Positive | Patient is created and its ID and name match the supplied values | Patient is successfully created | [complete] |
| Test-01-04 | FR-01 | Blank ID is rejected | Negative | Verify blank patient IDs are rejected | Patient ID is rejected and raises ValueError | [complete] |
| Test-01-05 | FR-01 | Whitespace characters as ID are rejected | Boundary | Verify patient IDs with whitespace characters are rejected | Patient ID is rejected and raises ValueError | [complete] |
| Test-01-06 | FR-01 | Blank name is rejected | Negative | Verify blank patient names are rejected | Patient name is rejected and raises ValueError | [complete] |
| Test-01-07 | FR-01 | Whitespace characters as name are rejected | Boundary | Verify patient names with whitespace characters are rejected | Patient name is rejected and raises ValueError | [complete] |

| TEST-FR05-01 | FR-05 | | Positive | Book a registered practitioner in an available slot. | Stored appointment is `SCHEDULED`, with correct patient, practitioner and date/time. | Establishes the successful booking baseline for conflict tests. |
| TEST-FR05-02 | FR-05 | | Negative | Book the same practitioner at the exact same time as an existing scheduled booking. | `ValueError`; original remains and attempted second booking is absent. | Explicitly verifies conflict rejection and no additional record. |
| TEST-FR05-03 | FR-05 | | Positive | Book two different practitioners at the same time. | Both appointments are `SCHEDULED`. | Confirms conflict checking is practitioner-specific. |
| TEST-FR05-04 | FR-05 | | Boundary | Book the same practitioner at 09:00 and 09:01. | Both bookings succeed. | Verifies the exact-datetime boundary, not duration overlap. |
| TEST-FR05-05 | FR-05 / FR-07 | | Positive / state transition | Cancel an appointment, then book its former slot. | Original remains `CANCELLED`; replacement is `SCHEDULED`; both records remain. | Checks that cancelled history does not block rebooking. |
| TEST-FR05-06 | FR-05 | | Negative / integrity | Attempt a conflicting booking and inspect the stored appointment. | Original appointment fields remain unchanged; collection contains only original. | Verifies preservation of state after rejection. |

## D Arrange Act Assert Record
| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |

|---|---|---|---|---|
| Test-01-01 | Create store for patient and PatientService | Register valid patient ID | Patient ID is found in datastore | Proves that a valid patient ID is stored (AC-01.1 under FR-01) |
| Test-01-02 | Create store for patient and PatientService | Register existing patient ID | ValueError is raised | Proves that duplicate patient IDs are rejected (AC-01.2 under FR-01) |
| Test-01-03 | Create patient object with ID and name | Construct patient object with ID and name | Patient object is created and its attributes are checked | Proves that patient construction works |
| Test-01-04 | Create blank ID and valid name | Construct with blank patient ID | ValueError is raised | Proves that blank patient IDs are rejected |
| Test-01-05 | Create ID with whitespace characters and valid name | Construct with patient ID with whitespace characters | ValueError is raised | Proves that patient IDs with whitespace characters are rejected |
| Test-01-06 | Create valid ID and blank name | Construct with blank patient name | ValueError is raised | Proves that blank patient names are rejected |
| Test-01-07 | Create valid ID and name with whitespace characters | Construct with patient name with whitespace characters | ValueError is raised | Proves that patient names with whitespace characters are rejected |

| TEST-FR05-01 | Fresh store; registered patient P1 and practitioner D1. | Book A1 at 09:00. | `SCHEDULED`; correct object references, date/time and lookup identity. | Checks the observable successful booking result. |
| TEST-FR05-02 | Fresh store; P1, P2, D1; A1 booked at 09:00. | Attempt A2 for D1 at 09:00. | `pytest.raises(ValueError)`; A1 unchanged, A2 absent, count 1. | Verifies rejection and absence of an unintended write. |
| TEST-FR05-03 | Fresh store; P1, P2, D1, D2. | Book A1 for D1 and A2 for D2 at 09:00. | Both `SCHEDULED`, correct practitioner IDs, count 2. | Demonstrates that a shared time is not globally blocked. |
| TEST-FR05-04 | Fresh store; P1, P2, D1. | Book A1 at 09:00 and A2 at 09:01 for D1. | Both `SCHEDULED`; times differ; count 2. | Exercises the one-minute boundary of exact-time matching. |
| TEST-FR05-05 | Fresh store; P1, P2, D1; A1 booked at 09:00. | Cancel A1 and book A2 in same slot. | A1 `CANCELLED`, A2 `SCHEDULED`, both retrievable, count 2. | Verifies cancellation releases the slot without erasing history. |
| TEST-FR05-06 | Fresh store; P1, P2, D1; A1 booked at 09:00. | Attempt conflicting A2. | `ValueError`; A1 ID, patient, practitioner, time and status unchanged; list equals `[original]`. | Checks that rejection does not mutate existing data. |

## E Domain Test Evidence

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TEST-DOM-01 | Create a practitioner with valid details | `tests/test_domain.py::test_create_practitioner_with_valid_details` | PASS |
| TEST-DOM-02 | Reject an empty practitioner ID | `tests/test_domain.py::test_practitioner_empty_id` | PASS |
| TEST-DOM-03 | Reject an empty practitioner name | `tests/test_domain.py::test_practitioner_empty_name` | PASS |
| TEST-DOM-04 | Reject an empty specialty | `tests/test_domain.py::test_practitioner_empty_specialty` | PASS |
| TEST-DOM-05 | Reject a practitioner ID containing only spaces | `tests/test_domain.py::test_practitioner_id_with_only_spaces` | PASS |
| TEST-DOM-06 | Reject a practitioner name containing only spaces | `tests/test_domain.py::test_practitioner_name_with_only_spaces` | PASS |
| TEST-DOM-07 | Reject a specialty containing only spaces | `tests/test_domain.py::test_practitioner_specialty_with_only_spaces` | PASS |
| TEST-DOM-08 | Remove extra spaces from valid practitioner fields | `tests/test_domain.py::test_practitioner_removes_extra_spaces` | PASS |

| Test-01-03 | Patient is successfully created | test_patient_valid_construction() in test_domain.py | Passed |
| Test-01-04 | Patient ID is rejected and raises ValueError | test_blank_patient_id_rejected() in test_domain.py | Passed |
| Test-01-05 | Patient ID is rejected and raises ValueError | test_whitespace_patient_id_rejected() in test_domain.py | Passed |
| Test-01-06 | Patient name is rejected and raises ValueError | test_blank_patient_name_rejected() in test_domain.py | Passed |
| Test-01-07 | Patient name is rejected and raises ValueError | test_whitespace_patient_name_rejected() in test_domain.py | Passed |

All eight Practitioner domain tests passed locally. They check the required fields in `Practitioner` and the trimming done by `required_text()`.

## F Service Test Evidence
| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |

|---|---|---|---|---|
| Test-01-01 | Patient data is successfully registered and stored in data store | AC-01.1 under FR-01 | test_register_patient_valid_patient_unused_id_is_stored() in test_services.py | Passed |
| Test-01-02 | Duplicate patient ID is rejected at registration and raises ValueError | AC-01.2 under FR-01 | test_duplicate_patient_id_is_rejected() in test_services.py | Passed |

| TEST-FR05-01 | Available practitioner booking | FR-05 | `tests/test_services.py::test_fr05_available_practitioner_booking` | PASS |
| TEST-FR05-02 | Reject exact-time double booking | FR-05 | `tests/test_services.py::test_fr05_same_practitioner_same_time_rejected` | PASS |
| TEST-FR05-03 | Allow different practitioners at same time | FR-05 | `tests/test_services.py::test_fr05_different_practitioners_same_time_allowed` | PASS |
| TEST-FR05-04 | Allow same practitioner at different times | FR-05 | `tests/test_services.py::test_fr05_same_practitioner_different_times_allowed` | PASS |
| TEST-FR05-05 | Rebook cancelled slot and retain history | FR-05 / FR-07 | `tests/test_services.py::test_fr05_cancelled_slot_can_be_rebooked` | PASS |
| TEST-FR05-06 | Preserve stored state after conflict rejection | FR-05 | `tests/test_services.py::test_fr05_conflict_does_not_modify_existing_booking` | PASS |

## G Negative and Boundary Cases
| Behaviour | Boundary/invalid input | Expected result | Test ID |

|---|---|---|---|
| Patient register | Duplicate patient ID | ValueError is raised | Test-01-02 |
| Patient construction | Patient ID with whitespace characters | ValueError is raised | Test-01-05 |
| Patient construction | Patient name with whitespace characters | ValueError is raised | Test-01-07 |
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
| python -m pytest tests/test_domain.py -v | project/ | 8f436f3513d2dc62f6f3103990afe51aedc766f7 | 5 | 0 | None | None identified | All five FR-01 domain tests passed locally |
| `py -m pytest -v` | `project/` | Not recorded | 33 | 0 | None observed | None observed | Earlier run after adding the six FR-05 service tests. |
| `py -m pytest -v` | `project/` | Not recorded | 41 | 0 | None observed | None observed | Latest local run after adding eight Practitioner domain tests. |

Individual test runs: `py -m pytest tests/test_services.py -k "fr05" -v` — six FR-05 tests passed. The latest full run passed 41 tests in total. No separate changed-order run was recorded.  

Optional tutor-led demonstration notes:  

Requirement → test → failure/observation → diagnosis → change → verification: FR-05 → TEST-FR05-01 through TEST-FR05-06 → six passing tests; no failure or fix recorded.

## K What the Suite Still Does Not Prove
What does your test suite still not prove? The FR-05 tests verify exact-datetime conflicts in an in-memory store. They do not establish behaviour for overlapping appointment durations, simultaneous requests, persistent storage, or external notifications. Those behaviours are outside the verified FR-05 test scope.  

Coverage if used:  

Which uncovered areas matter, and why does coverage percentage alone not establish correctness? These tests do not measure concurrency or persistence behaviour. Even high line coverage would not prove the correct conflict rule or adequate assertions; tests must check observable requirements.  

Optional fixtures/parametrisation used and why, if any: I did not use fixtures or parametrisation in my six FR-05 tests or eight Practitioner tests. Each test sets up its own data, which makes it easy to follow.

## L Git and Review Evidence
| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| Stage 7 — FR-01 Patient Tests | feature/stage7-patient-testing | [#9](https://github.com/soulsbyrohan/st1-assignment-3/pull/9) | u3308969 | [complete] | [complete] |
| FR-05 practitioner booking conflict tests | `feature/stage7-conflict-tests` | [#7](https\://github.com/soulsbyrohan/st1-assignment-3/pull/7) | | | Six tests pushed; local regression 33 passed, 0 failed. |

## M Contribution Evidence
| Member | Actual contribution | Evidence link |

|---|---|---|

| u3325731 | Wrote six FR-05 service tests for booking conflicts and related cases. After the PR review, I also added eight Practitioner domain tests for valid details, empty fields, spaces-only fields and trimming extra spaces. The latest full test run passed all 41 tests. | [#7](https\://github.com/soulsbyrohan/st1-assignment-3/pull/7) |
| u3306036 | Created Stage 7 FR-01 tests, 2 service tests for AC-01.1 and AC-01.2 under FR-01 and 5 domain tests for patient construction and required-field validation. Tested all tests locally and documented behaviours and results in sections A-G.| [#9](https://github.com/soulsbyrohan/st1-assignment-3/pull/9) |

## N Formative Questions
1. What question does verification answer?  

Verification asks: ****Does the implemented software meet its specified requirements?**** Tests compare observed behaviour with the documented contract.

2. What question does validation answer?  

Validation asks: ****Does the software meet the users' intended needs?**** It checks whether the specified solution solves the right problem.

3. What is a unit test?  

A unit test checks one small part of the code, like a method or function. We give it an input and check whether the output or behaviour is correct.

4. What is a pytest fixture?  

A pytest fixture is a way to set up things that multiple tests need. For example, it can create a fresh object or test data so we do not have to repeat the same setup in every test.
 
5. What is parametrisation in pytest?
Parametrisation in pytest allows for single test functions to be run multiple times with different sets of arguments. 

6. What is regression testing?
Regression testing is a way of software testing that ensures recent changes to the code doesn't negatively impact existing functionality.

7. What does code coverage tell us, and what does it not prove?
Code coverage tells us to what extent the source code is executed during testing, but it does not prove that all requirements were met. 

8. What makes an assertion weak?
 A weak assertion is when it tests or checks very little about the code’s behaviour, for example assert True as it only checks whether a boolean condition is true or false. 

9. What is the appropriate role of GitHub Copilot as a test assistant?
Github Copilot as a test assistant can suggest scenarios, edge cases, assertions or code. However, the group must decide whether or not those suggestions match the requirements. 

10. What is the Stage 7 engineering rule?
The Stage 7 engineering rule is to use tests to gather evidence that your existing SmartCare application meets its requirements. We are to look at what required behaviour does these tests actually prove? In a group we are to write and review tests, interpret their results, and retain a traceable regression suite.

## O Stage Completion
Tested Stage 7 main SHA:  

Full-suite result:  

Unresolved defects and effect on baseline:  

Clean working tree and integration evidence:  

Stage 8 handover status:  

All tutorial/formative responses and traceability/Copilot decisions complete:
