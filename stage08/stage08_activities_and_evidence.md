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

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
- Baseline test command / working directory / observed result / evidence: [complete]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: [complete]
- Downloaded tool version, source SHA256 and --check outcome: [complete]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete]
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete]
- Initial prepared full-suite command / result / key failures: [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete]
- Expected behaviour and requirement: [complete]
- Minimal synthetic reproduction steps: [complete]
- Meaningful failing test path/name and exact relevant failure: [complete]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

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
Member and saved sequence/time or commit showing this preceded consultation: u3119457 |

### F8-02 human entry
Likely cause and why plausible:
The possible issuse I see is that appointment lookup could be excluding cancelled appointments because find_appointment() is not giving an appointment from the data store which is giving a LookupError

Evidence intended to inspect / competing explanation / discriminating check:
I intent to inspect SmartCareDataStore.find_appointment() to see if is filtering appointments by status. Another possibilty is that when appointments are cancelled, its just deleting the appointments from the data store. So checking list_appointment() after cancellation to see if A1 is still being stored.

Member and saved sequence/time or commit showing this preceded consultation: u3308969 - this hypothisis was recorded before consulting Copilot or touching any of the code. commit SHA: 681d5f9604ba48ef706199c52e3f926f9724cc60

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: 
u3308969 - Asked Copilot to investigate the F8-02 retained-history lookup error and suggest three possible causes. Copilot's response was reviewed against the existing code. No files were modified by Copilot.

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
- Suggestion: Cancelled appointments is explicitly filtered out
- Evidence: `data_store.py` checks `appointment.status.value != "cancelled"`.
- Assesment: Correct
- Decision: Accept. This explains well why the data store is returning None for cancelled appointments

2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
- Suggestion: The lookup could use a different or empty store
- Evidence: The test creates the service using the same store where the appointment is first registered.
- Assesment: Doesn't seem likely based on the tests setup
- Decision: Reject, I don't see it being the cause of this failure.

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason:
Suggestion: The requested ID could differ from the stored ID
- Evidence: The test should book and retrieve appointment A1 using the same ID
- Assesment: Very unlikely
- Decision: Reject, I don't see it being the cause of this failure.

Final human conclusion and comparison with initial hypothesis:
Copilot helped confirmed what I thought in my intitial hypothesis that cancelled appointments were being excluded from lookup. Inspection of `SmartCareDataStore.find_appointment()` identified the status restriction responsible for the failure. The other explanations were less consistent with the test setup and observed behaviour.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | 681d5f9604ba48ef706199c52e3f926f9724cc60 | `python -m pytest tests/test_services.py::test_fr07_cancelled_history_is_found_by_id_and_in_list -vv` from `project/` | Failed with `LookupError: Appointment not found` |
| F8-02 after repair | f2634f68b07947c97d69f57406c9f4087aeecfed | `python -m pytest tests/test_services.py::test_fr07_cancelled_history_is_found_by_id_and_in_list -v` from `project/` | Passed after removing the status restriciton; FR-7 tests also passed |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour:

For F8-02, the retained-history tests should verify that cancelled appointments remain stored and accessible by ID. The faulty lookup caused a LookupError becaused cancelled appointments were excluded. After removing the incorrect condition, the tests passed, which confirms that cancelled appointments remain retrievable.

Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

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
