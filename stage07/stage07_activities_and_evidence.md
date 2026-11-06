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
| FR-07 Retain cancelled history | [response] | [response] | [response] |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: This assertion always passes True and doesn't check if the code actually produces the correct result. It doesn't show any required behaviour.

`assert appointment is not None`
Judgement: Weak/unclear  Why: This only checks if appoinment exists. It doesn't actually prove that it is the correct appointment has been returned or that the appointment's status is correct

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour  Why: This checks that the appointment is expected to have the CANCELLED status. But it still doesn't say if its the correct appointment was cancelled or the appointment is still stored. 

`assert len(results) > 0`
Judgement: Weak/unclear  Why: This only checks if the results contain at least one item. It doesn't actually verify the results returned are correct or that none are missing.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour  Why: This checks that the data is store is returning the exact same appointment object for ID A1. This proves the original object is still accessible but it doesn't check its status

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
| FR-06 | AC-05.1 | TEST-06-01 | Positive domain | test_domain_cancel_scheduled_appointment | Scheduled appointment changes to CANCELLED | Passed locally | Student-authored |
| FR-06 | AC-05.3 | TEST-06-02 | Negative domain | test_domain_cancel_already_cancelled | Repeated cancellation raises ValueError; status remains CANCELLED | Passed locally | Student-authored |
| FR-06 | Completed-state cancellation contract | TEST-06-03|Negative domain | test_domain_cancel_completed_appointment | Completed cancellation raises ValueError; status remains COMPLETED | Passed locally | Student-authored |
| FR-06 | AC-05.1 | TEST-06-04 | Positive service | test_cancel_scheduled_appointment | Service cancels a scheduled appointment, changes its status to CANCELLED and returns the original object | Previously passed locally | Student-authored |
| FR-06 | AC-05.3 | TEST-06-05 | Negative service | test_cancel_already_cancelled_appointment | Repeated cancellation raises ValueError and leaves the status unchanged | Previously passed locally | Student-authored |
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-06-01 | FR-06 | AC-05.1 | Positive | Check that a scheduled appointment can be cancelled using the domain method | Appointment status changes from SCHEDULED to CANCELLED | Independently verifies the Appointment object's cancellation behaviour |
| TEST-06-02 | FR-06| AC-05.3 | Negative | Check that an already cancelled appointment cannot be cancelled again | ValueError is raised and status remains CANCELLED | Verifies that repeated cancellation is rejected without changing the state |
| TEST-06-03 | FR-06 | Completed-state cancellation contract | Negative | Check that a completed appointment cannot be cancelled | ValueError is raised and status remains COMPLETED | Verifies that completed appointments are protected from invalid status changes |
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-06-01 | Create a patient, practitioner and SCHEDULED appointment | Call appointment.cancel() | Assert status is CANCELLED | Confirms the domain method successfully changes a scheduled appointment to CANCELLED |
| TEST-06-02 | Create a scheduled appointment and cancel it once | Call appointment.cancel() again | Assert ValueError is raised and status remains CANCELLED | Confirms repeated cancellation is rejected without changing the appointment's status |
| TEST-06-03 | Create an appointment with COMPLETED status | Call appointment.cancel() | Assert ValueError is raised and status remains COMPLETED | Confirms completed appointments cannot be cancelled and their status remains unchanged |
| [complete] | [complete] | [complete] | [complete] | [complete] |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
|TEST-06-01|Cancelling a scheduled appointment changes its status to CANCELLED| `test_domain.py::test_domain_cancel_scheduled_appointment` | Passed locally |
| TEST-06-02 | Repeated cancellation raises ValueError and leaves status unchanged | `test_domain.py::test_domain_cancel_already_cancelled` | Passed locally |
| TEST-06-03 | Cancelling a completed appointment raises ValueError and preserves COMPLETED status | `test_domain.py::test_domain_cancel_completed_appointment`| Passed locally |
| [complete] | [complete] | [complete] | [complete] |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-06-04 | Cancels a scheduled appointment and returns the original object | FR-06 / AC-05.1 | `test_services.py::test_cancel_scheduled_appointment` | Previously passed locally |
| TEST-06-05 | Rejects repeated cancellation and preserves CANCELLED status | FR-06 / AC-05.3 | `test_services.py::test_cancel_already_cancelled_appointment` | Previously passed locally |
| TEST-06-06 | Rejects cancellation of a completed appointment and preserves its status | FR-06 / Completed-state contract | `test_services.py::test_cancel_completed_appointment` | Previously passed locally |
| TEST-06-07 | Rejects cancellation of an unknown appointment ID with LookupError | FR-06 / Unknown-ID service contract | `test_services.py::test_cancel_unknown_appointment_id` | Previously passed locally |
| TEST-06-08 | Rejects a blank appointment ID with ValueError | FR-06 / Invalid-ID contract | `test_services.py::test_cancel_blank_appointment_id` | Previously passed locally |
| TEST-06-09 | Rejects a non-string appointment ID with ValueError | FR-06 / Invalid-ID contract | `test_services.py::test_cancel_invalid_appointment_id_type` | Previously passed locally |
| [complete] | [complete] | [complete] | [complete] | [complete] |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Repeated cancellation | Appointment already CANCELLED | ValueError raised; status remains CANCELLED | TEST-06-02 |
| Completed appointment cancellation | Appointment status is COMPLETED | ValueError raised; status remains COMPLETED | TEST-06-03 |
| Service rejects repeated cancellation | Attempt to cancel an already CANCELLED appointment | ValueError raised; status remains CANCELLED | TEST-06-05 |
| Service rejects completed cancellation | Attempt to cancel a COMPLETED appointment | ValueError raised; status remains COMPLETED | TEST-06-06 |
| Unknown appointment lookup during cancellation | Valid but unregistered appointment ID A1000 | LookupError raised | TEST-06-07 |
| Blank appointment ID | Empty string ('') | ValueError raised | TEST-06-08 |
| Invalid appointment ID type | None instead of a string | ValueError raised | TEST-06-09 |
| [complete] | [complete] | [complete] | [complete] |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-06 Appointment Cancellation
Acceptance criterion: AC-05.3 Repeated cancellation is rejected.
Behaviour to test: An appointment that has already been cancelled shouldn't be able to be cancelled again. The second cancellation should raise a ValueError and leave the appointment status unchanged.
Human-first test idea/categories: Created a scheduled appointment, cancelled it once, then tried cancelling it again. Check that a ValueError was raised and that the appointment status stays CANCELLED.
Prompt and purpose: Asked Github Copilot to suggest a postive, negative and boundary tests for FR-06 / AC-05.3 and explain what each verifies.

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: Repeated domain cancellation
- What it claims to verify: A second cancellation raises ValueError without changing status.
- Requirement trace: FR-06 / AC-05.3
- Assertion quality: It's strong, checks if the exception and unchanged status
- Human critique: Already done and covered by test_domain_cancel_already_cancelled().
- Decision: Accept
- Reason: It correctly verifies AC-05.3 and no additional test needed.
- Final test reference if accepted/modified: test_domain.py::test_domain_cancel_already_cancelled
- Actual verification result: Exisiting domain tested passed locally.

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: Third cancellation attempt
- What it claims to verify: Cancellation is still rejected after a previous failed attempt.
- Requirement trace: FR-06 / AC-05.3
- Assertion quality: It has valid checks but it has largely duplicate exisitng coverage.
- Human critique: The second cancellation test already proves rejection and unchanged status.
- Decision: Reject
- Reason: It duplicates the existing repeated-cancellation test without adding meaningful evidence.
- Final test reference if accepted/modified: Not retained.
- Actual verification result: Did not have a run, suggestion was rejected.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? 
Copilot suggested testing a third cancellation test which at first appeared to give additional coverage.
It repeats a lot of the behaviour already checked by the second cancellation test, including  ValueError and unchanged CANCELLED status.
How did you strengthen it? 
I Kept the exisitng repeated-cancellation test because its assertions already verify the required behaviour.. No additional test should be needed.
Accepted / modified / rejected test decisions and evidence: 
Accepted the repeated domain cancellation test idea as it is already covered by test_domain_cancel_already_cancelled() and rejected the third cancellation test as it wasn't needed because it pretty much duplicaiton of the accepted test. See explaination in Section H.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| python -m pytest tests/test_domain.py -k domain_cancel -v | project/ | 18c20a60a2d3100f082ec757f2994f3a19f5eec5 | 3 | 0 | None | None identified | All three FR-06 domain tests passed locally |
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

Individual test runs and changed-order independence evidence: 
- FR-06 domain tests: 3 passed, 0 failed.
- Original order (repeated then completed cancellation): 2 passed, 0 failed.
- Reversed order (completed then repeated cancellation): 2 passed, 0 failed.
- Both orders passed, supporting test independence.
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
| U3308969 | Created three FR-06 domain tests covering successful cancellation, repeated cancellation and rejection of completed appointments. Made sure all three tests passed locally and documented their requirement traceability, test design and negative cases in Sections B–G. | |
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
