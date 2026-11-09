# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | | |
| Appointment history | | |
| Temporary menu choice | | |
| Practitioner specialty | | |
| Debug print output | | |
| Appointment status | | |

What is intentionally lost on exit? <!-- response -->

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | | | | |
| select_appointments | | | | |
| Service listing | | | | |
| Console | | | | |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: <!-- response -->

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | | |
| Service prints/reads the menu | | |
| Query sorts its source in place | | |
| Store prints Appointment saved | | |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: <!-- response -->

Score-example prediction and explanation of passing the named key: <!-- response -->

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: <!-- response -->

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| | | | | |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->


**Console and workflow design — u3325731**

For my part, I will focus on how the console should handle user interactions and connect with the existing SmartCare services. The console should use the same data store throughout the session so that registered patients, practitioners and appointments remain available until the user exits.

The console will handle user input and display results, while the services will handle validation, bookings and cancellations. Invalid inputs should display an error without crashing the program or changing existing records.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| UI-01 | Patient, practitioner and appointment details | Console uses the existing services | Users can register, find, book, cancel and list appointments through the menu | Test a complete menu workflow |
| UI-02 | Invalid IDs, dates, statuses and menu choices | Console handles invalid inputs | Errors are displayed, the menu continues running and existing data remains unchanged | Test invalid inputs followed by valid actions |

**Additional design decisions:**

The console should convert status text into the correct `AppointmentStatus` enum before passing it to the service. Leaving the status blank should return appointments of all statuses.

Cancelling an appointment should update its status rather than delete it. This allows the appointment to be found again and included in the all-status listing, while excluding it from a scheduled-only listing.

I will also check that invalid operations do not affect existing records and that the user can continue using the menu afterward.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| | | | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | Run `python main.py --interactive` from `project/`. Register P1 and DR1, book A1, attempt a conflicting booking, cancel A1, retrieve A1 and book A2 in the freed slot. | Valid operations succeed, conflicts are rejected and cancelled appointments remain retrievable. | Registration, lookup, booking and cancellation worked as expected. The conflicting booking was rejected without affecting A1. After cancellation, A1 remained retrievable and A2 could use the freed time slot. Different-practitioner booking and Option 8 listing/filtering still need verification. | Terminal screenshots to be linked |
| UI-02 invalid-input recovery | Test invalid menu choices, blank/duplicate IDs, unknown records, malformed/impossible dates and repeated cancellation, followed by valid operations. | Invalid inputs produce appropriate errors without crashing or changing existing records. | All tested invalid inputs were rejected. The menu continued running, the original patient remained unchanged, and a valid appointment could still be booked afterward. Invalid status filtering remains unverified until Option 8 is available. | Terminal screenshots to be linked |
| Automated service workflow | Run `python -m pytest tests/test_workflows.py -v` and `python -m pytest -q` from `project/`. | New workflow tests and existing regression tests pass. | 12 workflow tests passed. Full regression suite: 73 passed, with no reported failures. | Test output screenshot to be linked |

**Pending verification:** Option 8 requires the Stage 9 practitioner appointment listing service to be completed. Once integrated, we still need to test all-status listing, status filtering, invalid status handling and the remaining workflow scenarios.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
