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
| FR-04 / UI-01 | Appointment ID, patient ID, practitioner ID and date/time | Console collects input and calls `AppointmentService.book_appointment()` | Valid booking creates a SCHEDULED appointment; invalid inputs or booking conflicts are rejected without altering existing records | |
| FR-06 / UI-01-02 | Appointment ID | Console calls `AppointmentService.cancel_appointment()` | Valid cancellation changes appointment status to CANCELLED and retains the record; repeated cancellation or invalid IDs display an error without terminating the console | |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: <!-- response -->

For FR-04 and FR-06, the console collects user input and calls the existing AppointmentService methods. The separate date and time inputs are combined and converted into a datetime object using parse_date_time().

Invalid inputs, unknown IDs, booking conflicts and repeated cancellations are handled by displaying an error without terminating the console. Invalid inputs include incorrect date formats or missing values, while unknown IDs refer to records that do not exist.

Successful cancellation retains the original appointment object and changes its status to CANCELLED. Rejected operations leave existing appointment records unchanged.

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

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
u3308969: [Copilot Prompt](https://github.com/soulsbyrohan/st1-assignment-3/commit/d3b59a07db4db20ec82106827324e75aec99258f#commitcomment-208920251)
Actual response: <!-- accessible reference -->
u3308969: [Copilot Response](https://github.com/soulsbyrohan/st1-assignment-3/commit/d3b59a07db4db20ec82106827324e75aec99258f#commitcomment-208920279)

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| u3308969: Date/time validation correct | `parse_date_time()` and `test_console.py` | None | Accept — validation meets requirements | No change | 40 focused tests passed |
| u3308969: Booking and cancellation rules preserved | `AppointmentService` and `test_services.py` | None | Accept — existing business rules are preserved | No change | 40 focused tests passed |
| u3308969: Uncaught `EOFError` | Console booking and cancellation helpers | Low | Modify/defer — better handled at menu level | No change to helpers | No EOF-specific test performed |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
u3308969: Making sure that the console used the existing `AppointmentService` methods rather than implementing booking and cancellation rules itself. The console handles user input and errors, while the service manages appointment operations and the domain controls status changes.
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
u3308969:  Copilot suggested handling `EOFError` when console input closes. I chose not to add this to my booking and cancellation helpers because it was outside their main responsibility. This could be handled at the main menu level if needed.
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->
u3308969: I used pytest assertions to verify that cancelling an appointment changes its status to `CANCELLED` while retaining the original appointment object. The existing service and regression tests also check that cancelled appointments can still be found by ID and included in appointment listings.

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
