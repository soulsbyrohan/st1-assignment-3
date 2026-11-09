# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

| Statement | Classification | Reason |
|---|---|---|
| Appointment disappears after cancellation. | Symptom | It describes what happens to an appointment after it is cancelled.  |
| The data-store removal path is probably being called. | Hypothesis | A possible explanation that needs to be tested against the code. |
| The failing test shows `store.find_appointment('A1')` returns `None`. | Evidence | It is a concrete result that is observed during testing. |
| The service layer is badly designed. | Opinion | It is an opinion or judgement with no evidence or testable explanation.  |
| Traceback points to `smartcare/services.py` line 42 in the example. | Evidence | Identifies where the example failure occurred, but does not prove its root cause. |

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: 
Scenario: F8-02 Retained Appointment History

- Expected behaviour: FR-07 / AC-05.2 requires cancelled appointments to remain stored and retrievable by ID.
- Observed behaviour: Looking up cancelled appointment A1 raised `LookupError: Appointment not found`.
- Minimal reproduction: Register patient P1 and practitioner D1, book appointment A1, cancel A1, then attempt to retrieve A1.
- Initial hypothesis: The appointment lookup might be excluding cancelled appointments even though they remain stored.
- Evidence to inspect: The failing traceback, `SmartCareDataStore.find_appointment()`, `AppointmentService.find_appointment()` and `list_appointments()` after cancellation.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

A test that expects cancelled appointments to be deleted, but FR-07 says history 
must be retained is a test defect. The test should be changed to meet the 
requirement, as it is currently expecting something that is not what the requirement 
wants.  

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

| Unclear variable name | Rename `appt` to `appointment` | Refactoring | Improves readability. |
| Repeated conflict logic | Extract a repeated conflict helper | Refactoring | Reduces duplicate logic.. |
| Missing functionality | Add rescheduling | Feature | Add new functionality. |
| Incorrect cancellation history behaviour | Restore retained cancellation lookup | Repair | Corrects behaviour. |
| Magic status strings | Replace status strings with the existing enum | Refactoring | Improves maintainability |
| Direct collection manipulation | Use existing `SmartCareDataStore` methods | Refactoring | Keeps data management within the correct component. |
| Printing inside services | Move printing and messages to the console layer | Refactoring | Separates business logic from user interaction. |
| Repeated validation | Extract validation into a focused helper | Refactoring | Reduces duplication and simplifies maintenance. |
| Four nested conditionals | Simplify conditions using early returns | Refactoring | Reduces nesting and improves readability. |
| Overly long method | Split the method into smaller focused functions | Refactoring | Makes code easier to understand and test. |

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: 
Actual failure: F8-02 Retained-History Lookup

- Failing test: `test_fr07_cancelled_history_is_found_by_id_and_in_list`
- Requirement: FR-07 / AC-05.2 Cancelled appointments remain stored and retrievable.
- Expected behaviour: `find_appointment('A1')` returns the original cancelled appointment.
- Observed behaviour: `LookupError: Appointment not found`.
- Test line: [Insert actual failing test line number from traceback]
- Application failure location: `smartcare/services.py:138`, where the service raises `LookupError` after receiving `None` from the data store.
- Application call path: Retained-history test → `AppointmentService.cancel_appointment()` → `SmartCareDataStore.find_appointment()` → cancellation → `AppointmentService.find_appointment()` → `SmartCareDataStore.find_appointment()`.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: 
Changing code immediately after seeing a failure is a poor debugging strategy as going straight into code without understanding the cause of the issue might introduce new bugs to the system.


Classification responses (1–5, each with reason): See A.1.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: See A.2.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: See A.5.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline:
  `3774afb4ea6b86ff05ee99e43ef3a0769b300a9b` SmartCare Assignment 3 Requirements Baseline 2026, revision 2. This is the baseline Git SHA reported by the tutor.
- Baseline test command / working directory / observed result / evidence:
  `python -m pytest -v` from `project/`; 59 passed, 0 failed, as recorded in the Stage 7 testing and verification document.
- Clean preparation SHA if a record-only commit followed Stage 7:
  `3774afb4ea6b86ff05ee99e43ef3a0769b300a9b` — the clean baseline commit identified by the tutor before fault injection.
- Branch and preparer / how teammates obtained this branch:
  Tutor prepared `debug/stage08` and pushed it to the group's GitHub repository. Group members obtained the branch using `git fetch origin` and `git switch --track origin/debug/stage08`.
- Downloaded tool version, source SHA256 and --check outcome:
  Tutor staff used `prepare_debugging.py` version 1.1. The reported baseline SHA256 was `b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375`. The `--check` preflight passed, confirming that the original project was unchanged and both proposed fault signatures were verified in a temporary copy. The utility's source SHA256 was not supplied to the group.
- --apply and --verify output summaries / artefact references:
  The tutor applied two prepared faults: F8-01 (practitioner booking conflict) and F8-02 (retained-history lookup). The `--apply` output reported two expected failing tests: `test_f8_01_conflict` and `test_f8_02_history`. The `--verify` output confirmed exactly two approved fault signatures. Evidence was provided in the tutor's Stage 8 preparation email.
- Bounded diff inspected and recovery location (not committed):
  The introduced faults affected the practitioner ID comparison in `SmartCareDataStore.has_practitioner_conflict()` and the cancelled-appointment status restriction in `SmartCareDataStore.find_appointment()`. Both were identified during debugging. The tutor reported backup/hash metadata in `.stage8_faults`, which must remain excluded from Git and the final submission. No staff recovery utility was provided to the group.
- Prepared faulty-state commit SHA:
  `8991aa4f59e2b3023910790e399d0e4cb9f55bbf` tutor commit "Prepare stage 08 Debug" on `debug/stage08`, before the group's repairs.
- Preparation or recovery issues and resolution, if any:
  No preparation issues were reported by the tutor. The prepared branch was fetched successfully, and the expected fault symptoms were reproduced during local testing. No recovery operation was required.
- Initial prepared full-suite command / result / key failures:
  `python -m pytest -q` from `project/` on the debugging branch, 44 passed, 15 failed. Failures included the incorrect acceptance of same-practitioner bookings at the same time (F8-01), incorrect rejection of different-practitioner bookings at the same time (F8-01), and `LookupError: Appointment not found` during cancellation and retained-history operations (F8-02).

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: When running the FR-05 tests, the system incorrectly allowed two appointments for the same practitioner at the same time. It also rejected bookings for different practitioners at the same time. I ran python -m pytest tests/test_services.py -k fr05 -v from the project/ directory. The result was 3 failed, 3 passed, 29 deselected.
- Expected behaviour and requirement: FR-05 / AC-04.1 requires the system to reject a second scheduled appointment for the same practitioner at the exact same date and time. AC-04.2 allows different practitioners to have appointments at the same date and time. When a conflicting booking is rejected, the original appointment should remain unchanged and no additional appointment should be stored.
- Minimal synthetic reproduction steps: register patients P1 and P2 and practitioners D1 and D2. Book appointment called A1 with practitioner D1 at 9am. Attempt another booking, A2, with D1 at 9am. This should raise ValueError. Then in a new store, book A1 with D1 at 9am and A2 with D2 at 9am. Both bookings should succeed.
- Meaningful failing test path/name and exact relevant failure: 
`tests/test_services.py::test_fr05_same_practitioner_same_time_rejected` = Failed: DID NOT RAISE <class 'ValueError'>
`tests/test_services.py::test_fr05_different_practitioners_same_time_allowed` = ValueError: Practitioner already has a SCHEDULED appointment at this time
`tests/test_services.py::test_fr05_conflict_does_not_modify_existing_booking` = Failed: DID NOT RAISE <class 'ValueError'>
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: Inspection of SmartCareDataStore.has_practitioner_conflict() on the debugging branch shows that the practitioner ID comparison uses != rather than ==. This means the method can report a conflict when practitioners are different, while failing to identify a conflict when they are the same.
- Smallest justified fix / diff / why other behaviour is preserved: Change only the practitioner ID comparison in has_practitioner_conflict() from != to ==. This should restore the required conflict behaviour without changing appointment registration, cancellation, retained history or other validation rules.
- Repair SHA / focused verification result: Repaired the bug in data_store.py that was causing the errors. Both the focused tests (py -m pytest tests/test_services.py -k fr05 -v) and the full-suite tests succesfully passed. Repair SHA: 0876e19380ea03340ee090e75254c6e795b068c5

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: Looking up appointment A1 raises a `LookupError: Appointment not found` when the retained history tests expect the original appointment to still be retrivable.

- Expected behaviour and requirement: FR-07 / AC-05.2 requires cancelled appointments to still be stored and accessible by their IDs.  

- Minimal synthetic reproduction steps: Register patient P1 and practitioner D1, book appointment A1, cancel A1 and then retrieve A1.

- Meaningful failing test path/name and exact relevant failure: `tests/test_services.py::test_fr07_cancelled_history_is_found_by_id_and_in_list` - `LookupError: Appointment not found` at `smartcare/services.py:138`

- Human hypothesis and intended checks: see E, F8-02.

- Supported root cause and inspected code/runtime evidence: `SmartCareDataStore.find_appointment()` excludes appointments whose status is CANCELLED using the condition `appointment.status.value != "cancelled"`. This is resulting cancelled appointments to be unretrievable through ID, even when FR-07 / AC-05.2 requires retained appointments to remain accessible. The previous observed LookupError is consistent with this condition.

- Smallest justified fix / diff / why other behaviour is preserved: 
Removing the condition `appointment.status.value != "cancelled"` from `SmartCareDataStore.find_appointment()`. This will allows cancelled appointments to be retrievable by ID as is required by FR-07 / AC-05.2. The exisiting ID validation and lookup behaviour should remain unchanged.

- Repair SHA / focused verification result: Removed the incorrect CANCELLED status restriction from `SmartCareDataStore.find_appointment()`. The focused retain history test and FR-07 test suite passed after the repair. Repair commit SHA: f2634f68b07947c97d69f57406c9f4087aeecfed

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: Based on the three failed tests, I suspect the practitioner conflict check is comparing practitioner IDs incorrectly. The system allows bookings for the same practitioner at the same time, but rejects bookings for different practitioners at the same time.
Evidence intended to inspect / competing explanation / discriminating check: I will inspect SmartCareDataStore.has_practitioner_conflict() in data_store.py, especially how it compares practitioner IDs. Another possibility is that the appointment service passes the wrong practitioner ID to the conflict check. I can distinguish these causes by tracing the IDs passed into the method and comparing the result for matching and different practitioners.
Member and saved sequence/time or commit showing this preceded consultation: u3119457 | Commit SHA: ce03c985c33074a8f2048861a7a5bf64eae3d31e | This was committed before consulting with Copilot. 

### F8-02 human entry
Likely cause and why plausible:
The possible issuse I see is that appointment lookup could be excluding cancelled appointments because find_appointment() is not giving an appointment from the data store which is giving a LookupError

Evidence intended to inspect / competing explanation / discriminating check:
I intent to inspect SmartCareDataStore.find_appointment() to see if is filtering appointments by status. Another possibilty is that when appointments are cancelled, its just deleting the appointments from the data store. So checking list_appointment() after cancellation to see if A1 is still being stored.

Member and saved sequence/time or commit showing this preceded consultation: u3308969 - this hypothisis was recorded before consulting Copilot or touching any of the code. commit SHA: 681d5f9604ba48ef706199c52e3f926f9724cc60

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: u3119457 [Copilot review prompt](https://github.com/soulsbyrohan/st1-assignment-3/commit/72b47c3348093e7987b14d9f2799a3817423d8bc#commitcomment-208846290) [Copilot Response](https://github.com/soulsbyrohan/st1-assignment-3/commit/72b47c3348093e7987b14d9f2799a3817423d8bc#commitcomment-208846322)

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: 
- Suggestion: The practitioner ID comparison in SmartCareDataStore.has_practitioner_conflict() uses != when it should check for matching practitioner IDs.
- Evidence check: Inspect the comparison in smartcare/data_store.py and compare its behaviour with the failed FR-05 tests.
- Observed evidence: The faulty condition is appointment.practitioner.practitioner_id != practitioner_id. This checks whether IDs are different rather than equal. It explains why a second booking for D1 was allowed and a booking for D2 at the same time was rejected.
- Assessment: Correct.
- Decision: Accept. The incorrect comparison is the supported root cause. The smallest justified repair is changing != to ==.

2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
- Suggestion: AppointmentService.book_appointment() might be passing the wrong practitioner ID to the conflict check.
- Evidence check: Inspect how book_appointment() retrieves the registered practitioner and passes its ID to has_practitioner_conflict().
- Observed evidence: The service retrieves the practitioner using the supplied ID and passes practitioner.practitioner_id to the conflict check. The inspected code does not show an incorrect ID being passed. No separate runtime ID trace has been recorded.
- Assessment: Not supported as the cause of the observed failures.
- Decision: Reject as the root cause. The incorrect comparison in the data-store method explains the failures without requiring a problem in the service's ID handling.

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: 
- Suggestion: Another condition in the conflict check, such as appointment ID exclusion, datetime, status or the executed code version, might be causing the failures.
- Evidence check: Inspect the appointment IDs, scheduled status, datetime values and branch code used by the tests.
- Observed evidence: The tests use distinct appointment IDs, matching appointment times and scheduled appointments. The faulty practitioner ID comparison is present in the inspected debugging code. These other conditions do not explain why same-practitioner and different-practitioner bookings behave in the opposite way to the requirements.
- Assessment: Plausible as a general debugging possibility, but not supported as the cause of this defect.
- Decision: Reject as the root cause. No additional change to these conditions is justified by the available evidence.

Final human conclusion and comparison with initial hypothesis: Copilot's highest-ranked suggestion agreed with my original hypothesis that practitioner IDs were being compared incorrectly. Inspection of has_practitioner_conflict() and the failing FR-05 tests supports this explanation. The other two suggestions were considered but were less consistent with the code and observed behaviour. I accepted the first diagnosis and rejected the other two as explanations for F8-01. The repair should change only the incorrect practitioner ID comparison, preserving the existing booking, validation and cancellation behaviour.

### F8-02 Copilot review
Actual prompt / output reference and member: 
u3308969 [Copilot review prompt](https://github.com/soulsbyrohan/st1-assignment-3/commit/1d6c447fef2b3fba9496644bb10cebc8e957c41d#commitcomment-208850034) [Copilot Response](https://github.com/soulsbyrohan/st1-assignment-3/commit/1d6c447fef2b3fba9496644bb10cebc8e957c41d#commitcomment-208850172)

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
- Suggestion: Cancelled appointments are excluded from `SmartCareDataStore.find_appointment()`.
- Evidence check: Inspected the lookup condition in `smartcare/data_store.py` and compareed it with the failed FR-07 tests.
- Observed evidence: The faulty condition is `appointment.status.value != "cancelled"`. Its excludes cancelled appointments from lookup, causing the data store to return `None` and the service to raise `LookupError: Appointment not found`.
- Assessment: Correct.
- Decision: Accept. The status restriction explains the failure and violates FR-07 / AC-05.2. The smallest justified repair is removing the incorrect condition.

2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
- Suggestion: The lookup could be using a different or empty data store.
- Evidence check: Inspect how the test creates `SmartCareDataStore` and passes it to `AppointmentService`. Check whether the service uses the same store as the booking.
- Observed evidence: The test creates one data store and passes it to the appointment service. There is no indication that a different store is being used.
- Assessment: Not supported as the cause of the observed failure.
- Decision: Reject. The incorrect status restriction already explains why cancelled appointments cannot be retrieved.

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
- Suggestion: The requested appointment ID could be different from the stored appointment ID.
- Evidence check: Compare the appointment ID used during booking with the ID supplied to `find_appointment()`.
- Observed evidence: The test books appointment `A1` and later attempts to retrieve the same ID, `A1`. The IDs match, so this does not explain the failure.
- Assessment: Very unlikely based on the test inputs.
- Decision: Reject. No change to ID matching is justified by the available evidence.


Final human conclusion and comparison with initial hypothesis:
Copilot helped confirmed what I thought in my intitial hypothesis that cancelled appointments were being excluded from lookup. Inspection of `SmartCareDataStore.find_appointment()` identified the status restriction responsible for the failure. The other explanations were less consistent with the test setup and observed behaviour.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | 72b47c3348093e7987b14d9f2799a3817423d8bc | `python -m pytest tests/test_regressions.py -k f8_01 -v` directory: `project/`| FAILED tests/test_regressions.py::test_f8_01_same_practitioner_same_time_is_rejected - Failed: DID NOT RAISE <class 'ValueError'> |
| F8-01 after repair | 0876e19380ea03340ee090e75254c6e795b068c5 | `python -m pytest tests/test_regressions.py -k f8_01 -v` directory: `project/` | tests/test_regressions.py::test_f8_01_same_practitioner_same_time_is_rejected PASSED     |
| F8-02 before repair | 681d5f9604ba48ef706199c52e3f926f9724cc60 | `python -m pytest tests/test_services.py::test_fr07_cancelled_history_is_found_by_id_and_in_list -vv` from `project/` | Failed with `LookupError: Appointment not found` |
| F8-02 after repair | f2634f68b07947c97d69f57406c9f4087aeecfed | `python -m pytest tests/test_services.py::test_fr07_cancelled_history_is_found_by_id_and_in_list -v` from `project/` | Passed after removing the status restriciton; FR-7 tests also passed |
| Full suite after both repairs, before refactor | 0876e19380ea03340ee090e75254c6e795b068c5 | `python -m pytest -q` directory: `project/` | 60 passed in 0.31s https://github.com/soulsbyrohan/st1-assignment-3/commit/0876e19380ea03340ee090e75254c6e795b068c5#commitcomment-208847966 |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour:

The F8-01 regression test attempts to book A2 with the same practitioner at the same time as A1 and will require `ValueError`. It then checks that A1 is still the same SCHEDULED object, A2 was not stored and the appointment list still contains only A1. This detects the original F8-01 failure and also checks that rejection does not mutate existing records.

For F8-02, the retained-history tests should verify that cancelled appointments remain stored and accessible by ID. The faulty lookup caused a LookupError becaused cancelled appointments were excluded. After removing the incorrect condition, the tests passed, which confirms that cancelled appointments remain retrievable.

Unrelated failures investigated / resolution: [complete or not applicable with reason]

H. Refactoring decision and before/after verification

Smell and exact location:

In project/smartcare/services.py, the AppointmentService.book_appointment() method was handling both appointment creation and practitioner booking conflict validation. Having both responsibilities in one method made the code longer and harder to maintain.

Small proposed structural change / why justified:

I decided to move the practitioner conflict checking logic into a separate private helper method called _check_practitioner_conflict(). This makes the booking method easier to read and keeps the conflict validation separate from the main booking process.

External behaviour to preserve / relevant tests:

The refactoring needed to preserve FR-05 and its acceptance criteria. The system should reject bookings for the same practitioner at the same date and time, allow different practitioners to be booked at the same time, and leave existing appointments unchanged when a conflict occurs. The existing FR-05 tests and full regression suite were used to check this.

Before result:

Section G records that the full test suite passed after the defects were fixed and before refactoring, with 60 tests passing.

Actual change / diff / separate refactor SHA:

I extracted the conflict validation logic from book_appointment() into _check_practitioner_conflict(). The helper uses SmartCareDataStore.has_practitioner_conflict() and raises a ValueError if a conflict is found. The booking method now calls this helper instead of handling the conflict checking directly.

Branch: refactor/stage8-booking-conflict

Refactoring commit SHA: d5c50f4922f9eeb35e766c00af0ecc070d5a93cc

Focused and full after-refactor commands / working directory / results / evidence:

Working directory: project/

Full regression command: py -m pytest -q

Result: 61 passed in 0.12 seconds, 0 failed.

The FR-05 tests had also passed during the earlier verification. After completing the refactoring, I ran the full test suite again to check for any issues.

Result — accepted, revised or rejected / reason / behaviour-preservation conclusion:

I accepted the refactoring because it made the code more organised without changing the required functionality. All 61 tests passed after the changes, including the booking conflict tests. This gave me evidence that the existing functionality covered by the tests was still working correctly.

I. Git, human review and integration

Issues for both defects / refactor scope and owners:

F8-01 involved incorrect practitioner booking conflict detection, while F8-02 involved cancelled appointments not being retrievable. Both defects were fixed by the group.

My responsibility was refactoring the practitioner booking conflict validation in AppointmentService and verifying that the changes did not affect the existing functionality.

F8-01 was handled by u3119457, F8-02 by u3308969, and the refactoring was completed by me (u3325731).

Branch / prepared, repair and refactor checkpoints:

Prepared debugging branch: debug/stage08

F8-01 repair SHA: 0876e19380ea03340ee090e75254c6e795b068c5

F8-02 repair SHA: f2634f68b07947c97d69f57406c9f4087aeecfed

My refactoring branch: refactor/stage8-booking-conflict

Refactoring commit SHA: d5c50f4922f9eeb35e766c00af0ecc070d5a93cc

PR link and another member's reviewer identity:

PR #13: https://github.com/soulsbyrohan/st1-assignment-3/pull/13

The pull request was reviewed by EmilyNicLynh.

Key human feedback, difference from Copilot findings and response/outcome:

The reviewer checked my changes and commented that everything looked fine. They also reminded me to complete Sections H and J in the Stage 8 documentation.

Unlike Copilot's earlier suggestions, which focused on possible causes of the bugs, this review focused on the completed changes and documentation. No code changes were requested in the feedback shown.

Actual review approval / merge evidence:

PR #13 was reviewed by EmilyNicLynh and successfully merged into main by ThomasLongCrowley. The pull request is now closed.

The review comments and merge are visible on GitHub, although the screenshots do not show a formal GitHub approval.

Integrated code SHA and team pull/retest command / working directory / result:

After PR #13 was merged, I switched to main and ran git pull origin main to get the latest integrated changes.

I then ran py -m pytest -q from the project/ directory.

All 61 tests passed in 0.36 seconds, with no failures. This confirmed that the merged changes were working correctly with the rest of the project for the scenarios covered by the tests.

Integrated commit SHA: b2716a8112d112b8afee87479232bfd185758cc9

Evidence-only later SHA / explanation if different:

Documentation commit: 751d8d9 (Update Stage 8 documentation). This was made separately on my refactoring branch after PR #13 had been merged, so it is not the integrated main SHA recorded above.

Each member's substantive contribution and artefact:

u3119457 investigated and repaired F8-01, including the practitioner conflict comparison and its verification.

u3308969 investigated and repaired F8-02, including the cancelled appointment lookup and its verification.

u3325731 (me) refactored the practitioner conflict validation into _check_practitioner_conflict(), ran the regression tests, created PR #13 and verified the integrated code after merging.

The defect investigation, Copilot review and regression evidence are recorded in Sections C-G.

J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence?

Copilot suggested that the book_appointment() method might be sending the wrong practitioner ID when checking for conflicts. At first, this seemed reasonable because the system was allowing bookings that should have been rejected and rejecting ones that should have been allowed. But after looking through the code, we couldn't find anything wrong with how the ID was being passed. The actual issue was the != comparison in has_practitioner_conflict(), which should have been ==.

2. What evidence changed your group's view?

The failing tests were the main thing that helped us understand the problems. For F8-01, we noticed that the system was allowing two bookings for the same practitioner at the same time, which shouldn't happen. After checking the code, we found the incorrect comparison.

For F8-02, the tests were giving a LookupError when trying to find a cancelled appointment. We then found that find_appointment() was excluding cancelled appointments. So instead of just guessing what was wrong, we used the test results and code to confirm the actual issues.

3. How did regression tests protect the refactoring?

Before I started refactoring, the tests were already passing after the bugs had been fixed. My part was to move the practitioner conflict checking logic into a separate method called _check_practitioner_conflict() to make the code more organised and easier to understand.

After making the changes, I ran the full test suite again using py -m pytest -q, and all 61 tests passed. I also ran the tests after the changes were merged into main, and all 61 passed again. This helped me confirm that the refactoring hadn't affected the existing functionality covered by our tests and that the booking conflict checks were still working properly.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Before changing code in response to a failure an engineer should reproduce the error, assess the impact and identify the root clause. The root clause should always be investigated before making code changes. 

2. Where should expected behaviour come from during debugging?

Response: During debugging expected behaviour should come from a requirement or acceptance criteria rather than actual code or assumptions. 

3. What is a debugging hypothesis?

Response: A debugging hypothesis is a detailed explanation on how the current code produces a specific error or unexpected behaviour. 

4. What is a regression test and why is it retained?

Response: A regression test is a software test that reruns previously executed tests after the code has been modified, a bug has been fixed or a new feature has been added to ensure the changes haven’t negatively affected the existing functionality. 

5. What is meant by root cause?

Response: A root clause is the underlying cause of a problem. 

6. What is refactoring?

Response: Refactoring is when the internal structure of a program’s existing code while keeping its external behaviour in tact. 

7. What is a swallowed exception?

Response: A swallowed exception is when a program catches an error, or exception, and ignores it instead of logging or rethrowing it.

8. What is a code smell?

Response: A code smell is a surface-level warning that points to a deeper structural or design problem in your program.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: GitHub Copilot-generated debugged diagnoses should be treated as a baseline in debugging. GitHub Copilot should be an agent that assists in debugging, but you should not rely solely on it for debugging diagnoses.

10. What is the Stage 8 engineering rule?

Response: The Stage 8 engineering rule is to always observe and identify the root clause before fixing an issue. The root clause should always be investigated before making code changes. 

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
