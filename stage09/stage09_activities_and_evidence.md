# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Session/Domain | Must identify the patient throughout the session in order to ensure that appointments are linked to the correct patient. |
| Appointment history | Session/Domain | All appointments, scheduled, completed or cancelled, must be available for lookup. |
| Temporary menu choice | Transient | Only needed when the user is making a selection. |
| Practitioner specialty | Session/Domain | Is part of practitioner information and is required when making appointments. |
| Debug print output | Transient | Used only for temporary debugging. |
| Appointment status | Session/Domain | Required to track whether an appointment is scheduled, completed or cancelled. |

What is intentionally lost on exit? Temporary data, such as menu choices and debugging outputs, is intentionally lost on exit.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.
| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] | Returning ordering key | Uses appointment appointment_id and date_time |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus, None = None | list[Appointment] | Filter and sort appointments and return new sorted list | Practitioner ID must match the appointment’s practitioner ID. |
| Service listing | practitioner_id: str, status: AppointmentStatus or None | list[Appointment] | Checks that the practitioner exists and the status filter is valid. Gets appointments from the data store and passes them to the pure query function for filtering and sorting. | Uses registered practitioners and appointments in SmartCareDataStore. Must preserve stored appointments and cancelled history. |
| Console | | | | |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: 
patient ID/name: Patient ID is uniquely identified with registered patient name,
practitioner ID/name/specialty: Practitioner ID is uniquely identified with registered practitioner name and speciality,
appointment ID/actual participants/date_time/status: Appointment ID is uniquely identified with appointment information 

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | It is handling user input, which it should not be | The console should read the user’s input and then call Appointment.cancel |
| Service prints/reads the menu | Service is doing menu interaction when it only do service operations | Console should display menu and handle menu interaction, service manages service operations |
| Query sorts its source in place | Query is modifying the original appointment, breaking purity | Query should return a sorted copy of the original list, leaving the original list in tact |
| Store prints Appointment saved | Store is doing presentation | Console start display save message, store should only |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: 

appointments.sort(key=appointment_sort_key)
<br>Source order: Modified (the original is sorted)
<br>Return Value: None
<br>Result identity: The original list is modified, no new list is returned

<br>result = sorted(appointments, key=appointment_sort_key)
<br>Source order: Unchanged
<br>Return Value: New sorted list
<br>Result identity: Different list

Score-example prediction and explanation of passing the named key: Appointment_sort_key separates sorting logic from query logic and ensures appointments are sorted by date_time and appointment_id is used to differentiate appointments at the same date and time.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancelling an appointment changes its status from SCHEDULLED to CANCELLED without deleting the original appointment. The cancelled appointment remains retrievable by ID and appears in an all-status listings, but, it is excluded when filtering for SCHEDULED appointments. These behaviours can be verified through lookup, listing and cancellation tests.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-04 | Registered practitioner D1 with no appointments | Service listing | Return an empty list `[]` | `test_listing_known_practitioner_with_no_appointments` |
| QRY-04 | Unknown practitioner D999 | Service validation | Raise `LookupError` | `test_listing_unknown_practitioner_raises_lookup_error` |
| QRY-04 | Blank, whitespace or non-text practitioner ID | Service validation | Raise `ValueError` | `test_listing_invalid_practitioner_id_raises_value_error` |
| QRY-04 | Non-enum status such as `"scheduled"` | Service validation | Raise `ValueError` | `test_listing_invalid_status_raises_value_error` |


Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-04 — known empty | `test_services.py` | Registered D1 with no appointments should return `[]`. | FAILED — `NotImplementedError: Stage 9: pure query` | [PR #16](https://github.com/soulsbyrohan/st1-assignment-3/pull/16) |
| QRY-04 — unknown ID | `test_services.py` | Unknown D999 must raise `LookupError`. | PASSED | [PR #16](https://github.com/soulsbyrohan/st1-assignment-3/pull/16) |
| QRY-04 — invalid ID | `test_services.py` | Empty, whitespace, `None` and numeric IDs must raise `ValueError`. | PASSED — four parameterised cases | [PR #16](https://github.com/soulsbyrohan/st1-assignment-3/pull/16) |
| QRY-04 — invalid status | `test_services.py` | Strings and other non-enum status values must raise `ValueError`. | PASSED — four parameterised cases | [PR #16](https://github.com/soulsbyrohan/st1-assignment-3/pull/16) |


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

1. What makes select_appointments pure, and what side effect breaks purity? select_appointments is pure because it only uses its own inputs to calculate a result, it doesn't perform input/output and it doesn't modify any existing lists or objects, therefore it has no side effects. A side effect that would break purity is modifying an appointment object or printing an output.
2. Which explicit inputs are needed, and why avoid a global store? As select_appointment requires appointments lists, practitioner ID and status filter, the explicit inputs makes the function testable and reusable. Avoiding a global store ensures that the results only depend on the given inputs.
3. How can a new list reuse Appointment objects safely? A new list can reuse Appointment objects safely as long as the new list doesn't modify objects in Appointment class. 
4. Why use a named key, and what breaks equal-time ties? A named key allows for sorting to be customised or improved without modifying the exisiting objects. Additionally, appointment IDs break equal-time ties when appointments have the same time.
5. How do default and explicit status filters differ? In this SmartCare system, when status is None that means that the appointment status is optional, which is default status. Explicit status is where a status is specified, when a specific status is supplied, only appointments with that status are included in the result.
6. How do empty, unknown practitioner and invalid filter cases differ? An empty result means no appointment matching the criteria. An unknown practitioner mean the provided practitioner ID shouldn't match the registered practitioner. Invalid filter means the practitioner ID or appointment status isn't the correct type or format.
7. Which console errors recover, and how is unchanged state checked? Invalid dates, unknown IDs, booking conflicts and repeated cancellations display an error without terminating the console. Tests will check that any rejected operations do not change any existing appointment records.
8. What is data integrity for registered participants, conflicts and history? Data integrity means appointments reference registered patients and practitioners, conflicting bookings are rejected and cancelled appointments remain accessible and stored without deleting them.
9. What is Copilot's review role, and who verifies findings? Copilt can act as in assistant in reviewing, as it is able to identify smells, improvements and issues. However, all suggestions and observations made by Copilot must be verified and checked by the student.
10. How do pure functions and OOP responsibilities work together? Pure functions and OOP responsibilities work together by separating duties. OOP organises data and information into objects, and pure functions use thos objects to perform tasks. 

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
