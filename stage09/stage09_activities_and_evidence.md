# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->

Members and responsibilities: u3325731 — console and workflow integration; u3119457 — service-level listing and validation; u3308969 — date/time and booking/cancellation console review. Confirm the full group allocation before submission.

Stage 8 integrated SHA, command, working directory and actual result: `b2716a8112d112b8afee87479232bfd185758cc9` (earlier confirmed Stage 8 main checkpoint); `py -m pytest -q` from `project/`: 61 passed. Verify whether a later Stage 8 documentation commit changed the final baseline.

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

What is intentionally lost on exit? Temporary menu choices and debugging output are lost. Since the application uses in-memory, session-only storage, patient, practitioner and appointment records are also lost when the program exits.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] | Returning ordering key | Uses appointment appointment_id and date_time |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus, None = None | list[Appointment] | Filter and sort appointments and return new sorted list | Practitioner ID must match the appointment’s practitioner ID. |
| Service listing | practitioner_id: str, status: AppointmentStatus or None | list[Appointment] | Checks that the practitioner exists and the status filter is valid. Gets appointments from the data store and passes them to the pure query function for filtering and sorting. | Uses registered practitioners and appointments in SmartCareDataStore. Must preserve stored appointments and cancelled history. |
| Console | Menu choice and user-entered IDs, names, specialty, date/time and optional status text | Printed results or recoverable error messages | Read input, convert date/time and status, call existing services, repeat until exit | Uses one session data store; services retain validation and business rules |

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

\Source order: Modified (the original is sorted)

\Return Value: None

\Result identity: The original list is modified, no new list is returned

\result = sorted(appointments, key=appointment_sort_key)

\Source order: Unchanged

\Return Value: New sorted list

\Result identity: Different list

Score-example prediction and explanation of passing the named key: Appointment_sort_key separates sorting logic from query logic and ensures appointments are sorted by date_time and appointment_id is used to differentiate appointments at the same date and time.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancelling an appointment changes its status from SCHEDULLED to CANCELLED without deleting the original appointment. The cancelled appointment remains retrievable by ID and appears in an all-status listings, but, it is excluded when filtering for SCHEDULED appointments. These behaviours can be verified through lookup, listing and cancellation tests.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: <!-- response -->

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| FR-04 / UI-01 | Appointment ID, patient ID, practitioner ID and date/time | Console collects input and calls `AppointmentService.book_appointment()` | Valid booking creates a SCHEDULED appointment; invalid inputs or booking conflicts are rejected without altering existing records | |
| FR-06 / UI-01-02 | Appointment ID | Console calls `AppointmentService.cancel_appointment()` | Valid cancellation changes appointment status to CANCELLED and retains the record; repeated cancellation or invalid IDs display an error without terminating the console | |
| QRY-04 | Registered practitioner D1 with no appointments | Service listing | Return an empty list `[]` | `test_listing_known_practitioner_with_no_appointments` |
| QRY-04 | Unknown practitioner D999 | Service validation | Raise `LookupError` | `test_listing_unknown_practitioner_raises_lookup_error` |
| QRY-04 | Blank, whitespace or non-text practitioner ID | Service validation | Raise `ValueError` | `test_listing_invalid_practitioner_id_raises_value_error` |
| QRY-04 | Non-enum status such as `"scheduled"` | Service validation | Raise `ValueError` | `test_listing_invalid_status_raises_value_error` |

u3119457 (human design): For the service-level appointment listing, I decided to keep validation in AppointmentService rather than putting it in the query function.

The service checks that the status filter is a valid AppointmentStatus value or None, and that the practitioner is registered. An invalid ID or filter raises ValueError, while an unknown practitioner raises LookupError.

A valid practitioner with no matching appointments should receive an empty list, not an error. The service then passes the appointments to select_appointments(), which handles the filtering and sorting.

This keeps the responsibilities separate and avoids changing the original appointments or losing cancelled history.

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

### Console and workflow design — u3325731

For my part, I focused on how the console handles user interactions and connects with the existing SmartCare services. The console should use the same data store throughout the session so that registered patients, practitioners and appointments remain available until the user exits.

The console handles user input and displays results, while the services handle validation, bookings and cancellations. Invalid inputs should display an error without crashing the program or changing existing records.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| UI-01 | Patient, practitioner and appointment details | Console uses the existing services | Users can register, find, book, cancel and list appointments through the menu | `project/tests/test_workflows.py` and manual menu run |
| UI-02 | Invalid IDs, dates, statuses and menu choices | Console handles invalid inputs | Errors are displayed, the menu continues running and existing data remains unchanged | `project/tests/test_workflows.py`; manual checks (status filtering still needs confirmation) |

**Additional design decisions:**

The console should convert status text into the correct `AppointmentStatus` enum before passing it to the service. Leaving the status blank should return appointments of all statuses.

Cancelling an appointment should update its status rather than delete it. This allows the appointment to be found again and included in the all-status listing, while excluding it from a scheduled-only listing.

The workflow tests check that invalid operations do not affect existing records and that the user can continue using the menu afterward.

For FR-04 and FR-06, the console collects user input and calls the existing AppointmentService methods. The separate date and time inputs are combined and converted into a datetime object using parse_date_time().

Invalid inputs, unknown IDs, booking conflicts and repeated cancellations are handled by displaying an error without terminating the console. Invalid inputs include incorrect date formats or missing values, while unknown IDs refer to records that do not exist.

Successful cancellation retains the original appointment object and changes its status to CANCELLED. Rejected operations leave existing appointment records unchanged.

My implementation files were `project/smartcare/console.py` and `project/tests/test_workflows.py`; the console is launched through `project/main.py --interactive`.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-04 — known empty | `test_services.py` | Registered D1 with no appointments should return `[]`. | FAILED — `NotImplementedError: Stage 9: pure query` | [PR #16](https\://github.com/soulsbyrohan/st1-assignment-3/pull/16) |
| QRY-04 — unknown ID | `test_services.py` | Unknown D999 must raise `LookupError`. | PASSED | [PR #16](https\://github.com/soulsbyrohan/st1-assignment-3/pull/16) |
| QRY-04 — invalid ID | `test_services.py` | Empty, whitespace, `None` and numeric IDs must raise `ValueError`. | PASSED — four parameterised cases | [PR #16](https\://github.com/soulsbyrohan/st1-assignment-3/pull/16) |
| QRY-04 — invalid status | `test_services.py` | Strings and other non-enum status values must raise `ValueError`. | PASSED — four parameterised cases | [PR #16](https\://github.com/soulsbyrohan/st1-assignment-3/pull/16) |

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
| Automated service workflow | Run `python -m pytest tests/test_workflows.py -v` and `python -m pytest -q` from `project/`. | New workflow tests and existing regression tests pass. | 12 workflow tests passed. At the earlier checkpoint, the full regression suite had 73 passing tests. A later integrated run reported 97 passing tests (see the contribution note below). | Test output screenshot to be linked |

### Console and workflow integration — u3325731

I worked on the interactive SmartCare console in `project/smartcare/console.py` and the workflow tests in `project/tests/test_workflows.py`.

The console provides a repeating menu with options to register and find patients, register and find practitioners, book appointments, cancel appointments, find appointments and list a practitioner's appointments. Option 0 exits the program.

The menu uses one shared data store for the session and calls the existing services instead of implementing the business rules itself.

The workflow tests were added to check how the console handles user actions and expected errors. The important cases include successful bookings and cancellations, invalid input handling and continuing to use the menu after an error.

**Regression testing**

- Working directory: `project/`

- Command: `py -m pytest -q`

- Reported result: ****97 passed****

- No failing tests were reported in the completed run.

This result covers the integrated test suite, not just my console tests. The latest 97-pass result was reported from the local working tree; the final merged commit and its test output still need to be linked.

**Files involved in my contribution:**

- `project/smartcare/console.py`

- `project/main.py`

- `project/tests/test_workflows.py`

- `stage09/stage09_activities_and_evidence.md`

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->

Actual prompt/context supplied: <!-- paste or accessible reference -->

u3308969: [Copilot Prompt](https\://github.com/soulsbyrohan/st1-assignment-3/commit/d3b59a07db4db20ec82106827324e75aec99258f#commitcomment-208920251)

u3119457: [Copilot Prompt](https\://github.com/soulsbyrohan/st1-assignment-3/pull/16#issuecomment-6739338286)

Actual response: <!-- accessible reference -->

u3308969: [Copilot Response](https\://github.com/soulsbyrohan/st1-assignment-3/commit/d3b59a07db4db20ec82106827324e75aec99258f#commitcomment-208920279)

u3119457: [Copilot Response](https\://github.com/soulsbyrohan/st1-assignment-3/pull/16#issuecomment-6739433255)

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| u3308969: Date/time validation correct | `parse_date_time()` and `test_console.py` | None | Accept — validation meets requirements | No change | 40 focused tests passed |
| u3308969: Booking and cancellation rules preserved | `AppointmentService` and `test_services.py` | None | Accept — existing business rules are preserved | No change | 40 focused tests passed |
| u3308969: Uncaught `EOFError` | Console booking and cancellation helpers | Low | Modify/defer — better handled at menu level | No change to helpers | No EOF-specific test performed |
| u3119457: Service validation and query coordination correct | `services.py`, `data_store.py` and `queries.py` | Optional | Accept — the service correctly validates inputs and uses the query for listing | No change | 11 focused tests passed; 85 full-suite tests passed |
| u3119457: Successful listing and status filtering not tested | `make_appointments()` and `test_services.py` | Important | Modify — agreed more testing was needed, but one combined test covers the main requirements without adding unnecessary separate tests | Added `test_listing_with_existing_appointments()` to test successful listing, filtering, ordering and cancelled history | 11 tests passsed locally |
| u3119457: New list and original object identity not verified | `test_services.py` and `test_queries.py` | Important | Modify — included checks in the same combined test rather than creating another test | Added assertions for a new list and original appointment objects | PASSED — test_listing_with_existing_appointments |
| u3119457: Failed requests not tested with existing appointments | `test_services.py` previously checked invalid inputs using an empty store | Important | Modify — included an invalid-status request with existing appointments in the combined test | Added checks that stored appointment order and statuses remain unchanged after rejection | PASSED — test_listing_with_existing_appointments |
| u3119457: Console listing not implemented | `run_menu()` in `console.py` | Important | Accept/defer — console integration is required for Stage 9 but is assigned to another group member | No change to my service code; console integration to be completed by the group | Console verification to be finished |
| u3119457: Missing type annotations in test helpers | `listing_setup()` and `make_appointments()` | Optional | Reject — annotations are not necessary for the required functionality and the existing helpers are readable | No change | No functional defect identified |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

u3119457: The domain classes maintain valid appointment data and cancellation rules. The data store keeps the registered patients, practitioners and appointments. The service validates practitioner IDs and status filters, while the query filters and sorts the appointments without changing the stored records. Keeping these responsibilities separate makes the application easier to understand and test

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->

u3308969: Making sure that the console used the existing `AppointmentService` methods rather than implementing booking and cancellation rules itself. The console handles user input and errors, while the service manages appointment operations and the domain controls status changes.

2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->

u3308969:  Copilot suggested handling `EOFError` when console input closes. I chose not to add this to my booking and cancellation helpers because it was outside their main responsibility. This could be handled at the main menu level if needed.

3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

u3308969: I used pytest assertions to verify that cancelling an appointment changes its status to `CANCELLED` while retaining the original appointment object. The existing service and regression tests also check that cancelled appointments can still be found by ID and included in appointment listings.

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

### Console and workflow handover — u3325731

My Stage 9 work covers the interactive console and workflow tests on `feature/stage9-console`. The menu reuses the existing services and a single in-memory store throughout the session. The console accepts user input, displays results and handles expected errors without ending the session.

The most recent local full-suite test result I reported was `py -m pytest -q` from `project/`: **97 passed**. This result should be rechecked and linked after the current merge is completed. Manual testing previously verified registration, lookup, booking, conflict rejection, cancellation, retained cancelled history and recovery from several invalid inputs. Different-practitioner booking, Option 8 listing/filtering and invalid status filtering were not confirmed in the earlier manual evidence and should be checked before marking the checklist complete.

The system is session-only: records are not saved after exit. Final PR/reviewer links, merged SHA and README evidence remain to be recorded by the group.

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
