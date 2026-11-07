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
| FR-01 Register patient | Register patient with valid ID | Register a patient with an existing ID | Patient can be found in data store from registered |
| FR-05 Prevent practitioner conflict | [response] | [response] | [response] |
| FR-06 Cancel appointment | [response] | [response] | [response] |
| FR-07 Retain cancelled history | [response] | [response] | [response] |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert appointment is not None`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert len(results) > 0`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

`assert data_store.find_appointment('A1') is appointment`
Judgement: [Strong for stated behaviour / Weak/unclear]  Why: [response]

### Activity 3 Boundary thinking

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
| FR-01 | AC-01.1 under FR-01 | Test-01-01 | Service | test_register_patient_valid_patient_unused_id_is_stored() in test_services.py | Patient data is successfully registered and stored in data store | Passed | Student-authored  |
| FR-01 | AC-01.2 under FR-01 | Test-01-02 | Service | test_duplicate_patient_id_is_rejected() in test_services.py | Duplicate patient ID is rejected at registration and raises ValueError | Passed | Student-authored  |
| FR-01 | Patient with name and ID is created | Test-01-03 | Domain | test_patient_valid_construction() in test_domain.py | Patient is created with the correct ID and name | Passed | Student-authored  |
| FR-01 | Blank ID is rejected | Test-01-04 | Domain | test_blank_patient_id_rejected() in test_domain.py | Patient ID is rejected and raises ValueError | Passed | Student-authored  |
| FR-01 | Whitespace characters as ID are rejected | Test-01-05 | Domain | test_whitespace_patient_id_rejected() in test_domain.py | Patient ID is rejected and raises ValueError | Passed | Student-authored  |
| FR-01 | Blank name is rejected | Test-01-06 | Domain | test_blank_patient_name_rejected() in test_domain.py | Patient name is rejected and raises ValueError | Passed | Student-authored  |
| FR-01 | Whitespace characters as name are rejected | Test-01-07 | Domain | test_whitespace_patient_name_rejected() in test_domain.py | Patient name is rejected and raises ValueError | Passed | Student-authored  |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| Test-01-01 | FR-01 | AC-01.1 under FR-01 | Positive | Verify that a patient with valid data can be registered and stored | Patient data is successfully registered and stored in data store | [complete] |
| Test-01-02 | FR-01 | AC-01.2 under FR-01 | Negative | Verify that duplicate patient IDs are rejected at registration | Duplicate patient ID is rejected at registration and raises ValueError | [complete] |
| Test-01-03 | FR-01 | Patient with name and ID is created | Positive | Patient is created and its ID and name match the supplied values | Patient is successfully created | [complete] |
| Test-01-04 | FR-01 | Blank ID is rejected | Negative | Verify blank patient IDs are rejected | Patient ID is rejected and raises ValueError | [complete] |
| Test-01-05 | FR-01 | Whitespace characters as ID are rejected | Boundary | Verify patient IDs with whitespace characters are rejected | Patient ID is rejected and raises ValueError | [complete] |
| Test-01-06 | FR-01 | Blank name is rejected | Negative | Verify blank patient names are rejected | Patient name is rejected and raises ValueError | [complete] |
| Test-01-07 | FR-01 | Whitespace characters as name are rejected | Boundary | Verify patient names with whitespace characters are rejected | Patient name is rejected and raises ValueError | [complete] |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| Test-01-01 | Create store for patient and PatientService | Register valid patient ID | Patient ID is found in datastore | Proves that a valid patient ID is stored (AC-01.1 under FR-01) |
| Test-01-02 | Create store for patient and PatientService | Register existing patient ID | ValueError is raised | Proves that duplicate patient IDs are rejected (AC-01.2 under FR-01) |
| Test-01-03 | Create patient object with ID and name | Construct patient object with ID and name | Patient object is created and its attributes are checked | Proves that patient construction works |
| Test-01-04 | Create blank ID and valid name | Construct with blank patient ID | ValueError is raised | Proves that blank patient IDs are rejected |
| Test-01-05 | Create ID with whitespace characters and valid name | Construct with patient ID with whitespace characters | ValueError is raised | Proves that patient IDs with whitespace characters are rejected |
| Test-01-06 | Create valid ID and blank name | Construct with blank patient name | ValueError is raised | Proves that blank patient names are rejected |
| Test-01-07 | Create valid ID and name with whitespace characters | Construct with patient name with whitespace characters | ValueError is raised | Proves that patient names with whitespace characters are rejected |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| Test-01-03 | Patient is successfully created | test_patient_valid_construction() in test_domain.py | Passed |
| Test-01-04 | Patient ID is rejected and raises ValueError | test_blank_patient_id_rejected() in test_domain.py | Passed |
| Test-01-05 | Patient ID is rejected and raises ValueError | test_whitespace_patient_id_rejected() in test_domain.py | Passed |
| Test-01-06 | Patient name is rejected and raises ValueError | test_blank_patient_name_rejected() in test_domain.py | Passed |
| Test-01-07 | Patient name is rejected and raises ValueError | test_whitespace_patient_name_rejected() in test_domain.py | Passed |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| Test-01-01 | Patient data is successfully registered and stored in data store | AC-01.1 under FR-01 | test_register_patient_valid_patient_unused_id_is_stored() in test_services.py | Passed |
| Test-01-02 | Duplicate patient ID is rejected at registration and raises ValueError | AC-01.2 under FR-01 | test_duplicate_patient_id_is_rejected() in test_service.py | Passed |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Patient register | Duplicate patient ID | ValueError is raised | Test-01-02 |
| Patient construction | Patient ID with whitespace characters | ValueError is raised | Test-01-05 |
| Patient construction | Patient name with whitespace characters | ValueError is raised | Test-01-07 |

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
| python -m pytest tests/test_domain.py -v | project/ | 8f436f3513d2dc62f6f3103990afe51aedc766f7 | 5 | 0 | None | None identified | All five FR-01 domain tests passed locally |

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
| Stage 7 — FR-01 Patient Tests | feature/stage7-patient-testing | [#9](https://github.com/soulsbyrohan/st1-assignment-3/pull/9) | u3308969 | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| u3306036 | Created Stage 7 FR-01 tests, 2 service tests for AC-01.1 and AC-01.2 under FR-01 and 5 domain tests for patient construction and required-field validation. Tested all tests locally and documented behaviours and results in sections A-G.| [complete] |

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

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
