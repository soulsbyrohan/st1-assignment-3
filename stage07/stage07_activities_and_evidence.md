# Stage 7 Testing and Verification Record

Group/tutorial: [complete]  Members/cohorts: [complete]
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | [response] | [response] | [response] |
| FR-05 Prevent practitioner conflict | [response] | [response] | [response] |
| FR-06 Cancel appointment | [response] | [response] | [response] |
| FR-07 Retain cancelled history | Cancel A1; retrieve the same record by ID and from `list_appointments()`. | Try cancelling A1 again or a missing ID; history must remain unchanged. | `assert service.find_appointment("A1") is original` and `assert original in store.list_appointments()`. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: It always passes and does not check any SmartCare requirement.

`assert appointment is not None`
Judgement: Weak/unclear  Why: It proves an object exists, not its identity, status, retention or correct appointment ID.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: It checks cancelled status but by itself cannot prove the same appointment remains in storage.

`assert len(results) > 0`
Judgement: Weak/unclear  Why: The list might contain the wrong record; it does not prove retained history for A1.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: It proves exact object identity in the store for A1, but status and full listing need separate checks.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract: [response]

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | [response] | [response] |
| 2 | [response] | [response] |
| 3 | [response] | [response] |
| 4 | [response] | [response] |
| 5 | [response] | [response] |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
[response]

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-07 | AC-05.2| TEST-FR07-01 | Positive / integration | test_fr07_cancelled_history_is_found_by_id_and_in_list | Cancelled A1 remains identical via service lookup, store lookup and listing | Passed locally | Student-authored|
| FR-07 | AC-05.2 | TEST-FR07-02 | Positive / integration |test_fr07_rebooking_does_not_erase_cancelled_history | Original cancelled and replacement bookings both remain stored | Passed locally | Student-authored |
| FR-07 | AC-05.2 | TEST-FR07-03 | Negative | test_fr07_repeated_cancellation_preserves_history | `ValueError`; status and stored list exactly unchanged |passed locally| Student-authored |
| FR-07 | AC-05.2 | TEST-FR07-04 | Negative | test_fr07_completed_cancel_rejection_retains_record | completed record remains in list and retrievable |passed locally | Student-authored |
| FR-07 | AC-05.2 | TEST-FR07-05 | Negative | test_fr07_unknown_cancellation_does_not_mutate_history | existing cancelled history unchanged | Passed locally | Student-authored |
| FR-07 | AC-05.2 | TEST-FR07-06 | Boundary | test_fr07_invalid_id_cannot_mutate_history | `ValueError` for `""`, spaces, `None`; existing history unchanged | Passed locally | Student-authored |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-FR07-01 | FR-07 | AC-05.2 — retained history | Positive | test_fr07_cancelled_history_is_found_by_id_and_in_list | Cancelled A1 remains identical via service lookup, store lookup and listing | Adds both retrieval paths and exact one-record list assertion beyond supplied domain check. |
| TEST-FR07-02 | FR-07 | AC-05.2 — retained history; FR-05 rebooking contract | Positive | test_fr07_rebooking_does_not_erase_cancelled_history | Original CANCELLED and replacement SCHEDULED bookings both remain stored | Checks two records coexist after rebooking the cancelled slot, beyond Stage 6 ID lookups. |
| TEST-FR07-03 | FR-07 | AC-05.2; AC-05.3 repeated cancellation | Negative | test_fr07_repeated_cancellation_preserves_history | `ValueError`; status and stored list exactly unchanged | Checks full history unchanged after rejected transition. |
| TEST-FR07-04 | FR-07 | AC-05.2; completed-state domain guard | Negative | test_fr07_completed_cancel_rejection_retains_record | `ValueError`; COMPLETED record remains in list and retrievable | Confirms illegal transition does not erase completed history. |
| TEST-FR07-05 | FR-07 | AC-05.2; service unknown-ID lookup contract | Negative | test_fr07_unknown_cancellation_does_not_mutate_history | `LookupError`; existing cancelled history unchanged | Checks absent ID does not mutate unrelated retained record. |
| TEST-FR07-06 | FR-07 | AC-05.2; `required_text()` invalid-ID validation | Boundary (3 inputs) | test_fr07_invalid_id_cannot_mutate_history | `ValueError` for `""`, spaces, `None`; existing history unchanged | Parametrised boundaries check that bad inputs do not mutate history. |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| SUP-04 | Stage 6 service cancellation and retained lookup | FR-06 / FR-07 | `tests/test_services.py::test_cancel_scheduled_appointment` | Group reported Stage 6 full regression 27 passed; not rerun on live Stage 7 |
| TEST-FR07-01 | Cancelled A1 remains identical via service lookup, store lookup and listing | FR-07 / AC-05.2 — retained history | `project/tests/test_fr07_history.py`::test_fr07_cancelled_history_is_found_by_id_and_in_list | Passed locally |
| TEST-FR07-02 | Original CANCELLED and replacement SCHEDULED bookings both remain stored | FR-07 / AC-05.2 — retained history; FR-05 rebooking contract | `project/tests/test_fr07_history.py`::test_fr07_rebooking_does_not_erase_cancelled_history | Passed locally |
| TEST-FR07-03 | `ValueError`; status and stored list exactly unchanged | FR-07 / AC-05.2; AC-05.3 repeated cancellation | `project/tests/test_fr07_history.py`::test_fr07_repeated_cancellation_preserves_history | Passed locally |
| TEST-FR07-04 | `ValueError`; COMPLETED record remains in list and retrievable | FR-07 / AC-05.2; completed-state domain guard | `project/tests/test_fr07_history.py`::test_fr07_completed_cancel_rejection_retains_record | Passed locally |
| TEST-FR07-05 | `LookupError`; existing cancelled history unchanged | FR-07 / AC-05.2; service unknown-ID lookup contract | `project/tests/test_fr07_history.py`::test_fr07_unknown_cancellation_does_not_mutate_history | Passed locally |
| TEST-FR07-06 | `ValueError` for `""`, spaces, `None`; existing history unchanged | FR-07 / AC-05.2; `required_text()` invalid-ID validation | `project/tests/test_fr07_history.py`::test_fr07_invalid_id_cannot_mutate_history | Passed locally |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Repeated cancellation | A1 is already CANCELLED | `ValueError`; same status and history list | TEST-FR07-03 |
| Completed cancellation | A1 is COMPLETED | `ValueError`; completed record still stored | TEST-FR07-04 |
| Unknown appointment ID | A999 valid text but never stored | `LookupError`; existing A1 unchanged | TEST-FR07-05 |
| Blank required ID | `""` | `ValueError`; existing records unchanged | TEST-FR07-06 |
| Whitespace-only required ID | `"   "` | `ValueError`; existing records unchanged | TEST-FR07-06 |
| Non-string required ID | `None` | `ValueError`; existing records unchanged | TEST-FR07-06 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: [complete]
Acceptance criterion: [quote]
Behaviour to test: [complete]
Human-first test idea/categories: [complete]
Prompt and purpose: [complete or link]

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: [complete]
- What it claims to verify: [complete]
- Requirement trace: [complete]
- Assertion quality: [complete]
- Human critique: [complete]
- Decision: [Accept / Modify / Reject]
- Reason: [complete]
- Final test reference if accepted/modified: [link or not retained]
- Actual verification result: [complete; do not claim an unrun test passed]

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? [response]
Why was it weak? [response]
How did you strengthen it? [response]
Accepted / modified / rejected test decisions and evidence: [link actual decisions in H]

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? [response]
Coverage if used: [result or not used]
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? [response]
Optional fixtures/parametrisation used and why, if any: [response or not used]

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

## N Formative Questions

1. What question does verification answer?
[response]

2. What question does validation answer?
[response]

3. What is a unit test?
[response]

4. What is a pytest fixture?
[response]

5. What is parametrisation in pytest?
[response]

6. What is regression testing?
[response]

7. What does code coverage tell us, and what does it not prove?
[response]

8. What makes an assertion weak?
[response]

9. What is the appropriate role of GitHub Copilot as a test assistant?
[response]

10. What is the Stage 7 engineering rule?
[response]

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
