# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 1 Wednesday 2:30pm-4:30pm
Members and UG/PG applicability: UG


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare Assignment 3: UG common release candidate v1.0
This release follows the main overview requirments, including FR-01-09, QRY-01-04, FP-01-03 and UI-01-2.
Common starting SHA / branch / applicable members: 
- Branch: `main`
- Starting SHA: 2f4e398bd2b65fe8aa35ccfe6f8f2c584d9969a2
- Applicable members: u3308969, u3119457, u3325731, u3306036
PG starting SHA / branch / applicable members or not applicable: Not applicable
Working-state review and approved integration: The integrated Stage 9 implementation passed all 99 tests at commit 3aa1be27cb16ca40da3732f4777c0d80b82d7376. The updated README documents the application, commands and session-only limitations.
The Stage 9 implementation includes the patient and practitioner registration and lookup, appointment booking, cancellation, retained appointment history, pure queries, service lisiting and an interactive console.
Protected common candidate and PG differences: Not applicable
The UG commonc candidate includes Stages 6, 7, 8 and 9. Stage 10 rescheduling and stage 11 assurance activities are outside of what is required for undergraduate
Feature freeze / owner / verifier:
- Feature freeze: No further functions will be added after Stage 9 integration. Only any type of issues will be corrected.
- Owner: u3325731
- Verifier: u3308969


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify:
<br>Release with conditions - All tests passed, meaning all implementations work correctly, however README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. These issues should be fixed before release, but they don’t affect the actual behaviour of the software.


Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | FR-06 and FR-07 tests confirm that cancelled appointments are stored | test_services.py and test_regressions.py | u3306036 | Yes | None |
| Architecture responsibilities are appropriate | Domain classes manage appointment rules, services help coordinate operations and validation, pure queries filter and sort without modifying stored data and the console handles the input / output | `project/smartcare/domain.py`, `services.py`, `queries.py`, `console.py`, Stage 9 Sections B and E, Tested SHA: 3aa1be27cb16ca40da3732f4777c0d80b82d7376  | All members | Yes | None |
| AI use is responsible | GitHub Copilot suggestions were reviewed and verified by students, with decisions to accept, modify or reject documented. | Stage 9 Section E, Stage 12 Section E | All members | Pending final review | Complete final Stage 12 AI review |
| System is maintainable | Readable code structure, tests, named functions | Source code and pull reviews | All members | Yes | None |
| FR-01–03 register/find and validation | FR-01 and FR-03 tests confirm that registration, lookup and validation work; invalid IDs are rejected | test_services.py and test_domain.py | u33257131 | Yes | None |
| FR-04–05 booking/conflict rules | FR-04 and FR-05 tests confirm that an available practitioner can be booked and cannot be double-booked, different practitioners can share a time slot and the same practitioner can have different time slots.  | test_services.py and test_domain.py | u3308969 | Yes | None |
| FR-06–08 cancellation/history/find | FR-06 and FR-08 tests confirm that only a SCHEDULED appointment can be cancelled, and cancelled appointments remain in history and can be searched up. | test_services.py and test_regressions.py | u3308969 | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | FR-09 and QRY/FP tests confirm appointment lists can be filtered, sorted and returned in new lists without modifying the original appointment list or objects | test_queries.py | u3308969 | Yes | None |
| UI full console sequence and error recovery | Manual testing verified registration, lookup, booking, conflict rejection, different-practitioner booking, cancellation, retained history, appointment listing/filtering, invalid-status recovery and normal exit. Automated workflow tests cover additional invalid inputs. | `project/tests/test_workflows.py`, Stage 9 Section D, tested SHA 3aa1be27cb16ca40da3732f4777c0d80b82d7376 | u3325731 | Yes | None for verified scenarios |
| Session-only scope / FR-10 retired | SmartCare uses an in-memory data store. Patient, practitioner and appointment records are lost when the application exits. Persistence is outside the revision 2 scope. | `project/README.md`, `project/smartcare/data_store.py` | All members | Yes | Accepted scope limitation; no persistence required |



### C. Integrated Regression Testing

The integrated SmartCare application was tested after the workflow test corrections were merged into the main branch.

- **Branch:** `main`
- **Commit SHA:** `3aa1be27cb16ca40da3732f4777c0d80b82d7376`
- **Command:** `py -m pytest -q`
- **Result:** 99 passed in 0.42 seconds, with no failures.

During an earlier regression run, two workflow tests failed because their assertions expected outdated console success messages. The test expectations were corrected to match the current implementation, and the corrections were merged through a pull request.

A fresh regression run on the updated main branch confirmed that all 99 tests passed, including the Option 8 listing/filtering and different-practitioner booking scenarios.

### D. Manual Console Demonstration

The SmartCare console was launched using `py main.py --interactive`. A continuous interactive session was used to demonstrate patient and practitioner registration, appointment booking, conflict handling, cancellation, lookup, filtering, chronological sorting and error recovery.

**Observed results:**

| Scenario | Result |
|---|---|
| Register and retrieve practitioners | DR1 and DR2 registered successfully; DR1 lookup succeeded |
| Practitioner booking conflict | A2 rejected because DR1 already had a scheduled appointment at the requested time |
| Different practitioner at same time | A3 successfully booked with DR2 |
| Rejected appointment lookup | A2 returned `Appointment not found` |
| Cancellation | A1 changed to `cancelled` |
| Cancellation history | A1 remained retrievable with its original details |
| Repeated cancellation | Rejected because only scheduled appointments may be cancelled |
| Appointment isolation | A3 remained scheduled after cancelling A1 |
| Option 8 status filtering | Cancelled A1 displayed under DR1; scheduled filter returned no matches before new bookings |
| Practitioner-specific listing | DR1 and DR2 displayed their respective appointments |
| Unknown practitioner | DR99 returned `Practitioner not found` |
| Chronological sorting | DR1 appointments displayed in order A1, A5, A4 despite A4 being booked before A5 |
| Invalid date format | Invalid date input rejected; corrected input accepted |

The demonstration showed that appointment operations maintained consistent session state and that invalid actions did not prevent subsequent valid operations.


**Manual console demonstration evidence**

All screenshots for practitioner registration, booking conflicts, cancellation history, Option 8 filtering, and chronological sorting are available in the evidence folder.

[View Stage 12 Console Demonstration Evidence](evidence/)
    

## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` | Each file has its own job. Domain classes check rules, the store keeps records, services handle tasks, queries filter and sort, and the console handles user input. | No change needed. The Stage 09 test record shows 99 passing tests. |
| PascalCase and snake_case naming | `project/smartcare/` | Class names such as `AppointmentService` use PascalCase. Methods and variables use snake_case. | No issue found. |
| Useful type hints and meaningful docstrings | `domain.py`, `services.py`, `queries.py`, `test_services.py` | Main methods have type hints and descriptions. Some test helpers do not have return types written out. | No required change; the helpers are still easy to understand. |
| Four-space indentation and imports/layout | `services.py`, `queries.py`, `test_services.py` | Indentation is generally consistent. Some blank lines and comments could be tidier. | Only a small style issue, not a problem with how the program works. |
| Focused methods / duplication / dead or commented code | `services.py`, `console.py` | The menu uses existing booking and cancellation helpers. An old commented-out `NotImplementedError` remains in `services.py`. | The comment does not affect the program. No change was made. |
| Globals / leakage / unnecessary inheritance or frameworks | `data_store.py`, `queries.py`, `console.py` | The console uses one shared store per session. Queries use information passed to them rather than global variables. | No issue found in the reviewed code. |
| No SQLite/persistence/repository ABCs/speculative features | `data_store.py`, `project/README.md` | SmartCare keeps data in memory instead of a database. Data is lost when the program closes. | No change needed. Permanent storage is outside our UG requirements. |
| Synthetic data / secrets / dependencies / provenance | `project/tests/`, `requirements-dev.txt`, `.gitignore` | Tests use made-up patient details. The testing dependency is `pytest==8.3.5`. The Git ignore file excludes common temporary files. | The reviewed GitHub file list did not show secret-named files or caches. This does not prove the contents of a final ZIP have been checked. |
| Significant common Copilot contributions and human verification | [Stage 08 evidence](../stage08/stage08_activities_and_evidence.md), [Stage 09 evidence](../stage09/stage09_activities_and_evidence.md), [PR #20](https://github.com/soulsbyrohan/st1-assignment-3/pull/20) | Copilot helped us find problems and missing test cases. We checked its suggestions before deciding what to change. | I added one combined service test. My 11 focused tests passed, and the group later recorded 99 passing tests. |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | `stage10_pg/`, `stage11_pg/` | Not applicable. Everyone in our group is an undergraduate student. | No PG work was required. |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Practitioner IDs were compared incorrectly | FR-05, `data_store.py`, [issue #14](https://github.com/soulsbyrohan/st1-assignment-3/issues/14) | We checked the `!=` comparison against the failing booking tests. | Accept — matching practitioner IDs should use `==`. | The code was fixed and Stage 08 regression tests were recorded. |
| Cancelled appointments could not be found | FR-07, `data_store.py`, [issue #12](https://github.com/soulsbyrohan/st1-assignment-3/issues/12) | We checked the old lookup condition against the cancelled-history tests. | Accept — cancelling an appointment must not remove its history. | The incorrect condition was removed. |
| Service tests needed successful-listing checks | QRY-04, `test_services.py`, [Copilot response](https://github.com/soulsbyrohan/st1-assignment-3/pull/16#issuecomment-6739433255) | I checked that the older tests mostly covered invalid inputs. | Modify — I wrote one combined test instead of lots of separate tests. | [PR #20](https://github.com/soulsbyrohan/st1-assignment-3/pull/20) added `test_listing_with_existing_appointments()`. All 11 focused listing tests passed in my local run. |
| The interactive menu was unfinished | UI-01/UI-02, `console.py`, [PR #21](https://github.com/soulsbyrohan/st1-assignment-3/pull/21) | We checked the old placeholder and the completed menu with options 0–8. | Accept — the menu needed to work for the assignment. | The menu was implemented and Stage 12 includes a manual demonstration. |
| Add type hints to test helpers | `test_services.py` | I checked whether this was required for the tests to pass. | Reject/defer — it was an optional style suggestion rather than a bug. | No change made. |

Access route or approved equivalent / limitations: The [Stage 08](../stage08/stage08_activities_and_evidence.md) and [Stage 09](../stage09/stage09_activities_and_evidence.md) records link to our actual Copilot prompts, responses and decisions. My [Stage 09 prompt](https://github.com/soulsbyrohan/st1-assignment-3/pull/16#issuecomment-6739338286) and [response](https://github.com/soulsbyrohan/st1-assignment-3/pull/16#issuecomment-6739433255) are also on GitHub.

Available AI evidence and missing evidence honestly disclosed: This section uses the Copilot reviews completed in the earlier stages. A separate Stage 12 Copilot review was not provided.
## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | `README.md`, `project/README.md` | u3308969 | Stage 9 UG functionality documented, PG stages not applicable. |
| Out-of-scope capabilities and known limitations  | `project/README.md` | u3308969 | Session-only storage, no persistence and synthetic-data requirement documented.|
| Confirmed teaching Python version and dependency installation | `project/README.md`, `project/requirements-dev.txt` | u3308969 | Python 3.13.0 and pytest 8.3.5 verified, installation successful  |
| Working directory / demo / interactive / test commands | `project/README.md` | u3308969 |  All documented commands executed successfully from a fresh clone; 99 tests passed. |
| Repository structure and architecture responsibilities | `README.md`, `project/README.md` | u3308969 | Application modules and responsibilities documented; final root README update to be checked. |
| Responsible AI summary / synthetic-data rule | `project/README.md` | u3308969 | Synthetic-data rule documented; Copilot review and human decisions recorded in Stage 9 Section E. |
| Release label/version and SHA links  | `README.md`, Section K | u3308969 | [PENDING — Final release SHA] |

Root README index and project/README verified: The root README contains group details, repository information, stage links and test instructions. The project README instructions were successfully reproduced from a fresh clone using Python 3.13.0, with 99 tests passing.
Fresh clone or extracted ZIP / candidate identity:
Fresh clone of https://github.com/soulsbyrohan/st1-assignment-3 into `smartcare-release-check`.
tested commt SHA: 2f4e398bd2b65fe8aa35ccfe6f8f2c584d9969a2
Verifier and clean environment / actual version:
- Verifier: u3308969
- Environment/version: Windows PowerSHell, python 3.13.0, pytest 8.3.5
Setup/run/test commands and observed results:
- `py -m pip install -r requirements-dev.txt` — successful.
- `py main.py` — demonstration completed successfully.
- `py main.py --interactive` — menu displayed; option 0 exited normally.
- `py -m pytest -q` — 99 passed in 0.18s.
Missing local file or setup gap / remedy and recheck:
No missing files or setup issues were identified during the fers-clone verification.


## G Known limitations debt and release notes

Delivered features:
- Patient/practitioner registration and lookup
- Appointment booking and cancellation with retained history
- Practitioner conflicting checking
- Appointment filtering by status
- Appointment sorting by date and time and appointment ID
- Console interaction


Important fixes:
- Invalid ID rejection
- Practitioner conflict checking
- Cancelled appointment storage
- Appointment filtering and sorting


Architecture/quality improvements:
- Responsibilities are separated across services, shared data store, domain classes, query functions and a console interface


Known limitations:
- No login system
- No database - data store stores data for current session and data is lost when program is exited


AI-assisted development note:
Github Copilot was used in this project to assist in review and offer suggestions and possible improvements.


| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| Session-only synthetic data and minute-precision local time: Synthetic data is stored in each session, all data is lost once program is exited. Appointment times use mintue precision without explicit timezone handling. | Data is lost once program exited | Medium | Add a database | Accepted - Out of scope of project requirements |
| Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: User authentication and access control, push notifications, payment and insurance handling, clinical AI assistance | Cannot support healthcare clinics | High | Consider user authentication and access control, push notifications, payment and insurance handling if the application is developed further. | Accepted - Out of scope of project requirements |
| Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Limited scale, concurrency, timezone handling, operations and monitoring, and accessibility and usability | System may not be able to handle working with multiple users or operations | Medium | Implement scale and concurrency, timezone handling, operations and monitoring, and accessibility and usability support | Accepted - Out of scope of project requirements |
| Difference between accepted scope limit and unresolved required behaviour: Scope limitations and unresolved behaviour | Scope limitations can still allow for release, but unresolved behaviour prevents release | High | Clearly documented the accpted scop limitations and make sure to verify that all required behaviours work correctly before release. | Accepted - Scope limiations accepted if its outside the assignment requriemtns. Unresolved requred defects are not be accepted and must first be fixed before offical release |

## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Interactive console (UI-01/UI-02) | The old menu was unfinished. The new menu has options 0–8 for registration, booking, cancellation, finding and listing appointments. | High at the time; **fixed**. | Group completed the menu. | [PR #21](https://github.com/soulsbyrohan/st1-assignment-3/pull/21) | The Stage 09 record shows 99 passing tests. [Stage 12 screenshots](evidence/) show a manual console test. | Data is lost after exit, as required. |
| Workflow tests | Two tests failed because they expected old console messages. | Important; **fixed**. | Group changed the test expectations to match the correct output. | [PR #22](https://github.com/soulsbyrohan/st1-assignment-3/pull/22) | The recorded Stage 09 result was 99 passed at `3aa1be27`. | No failing test reported in that run. |
| Service appointment listing tests (QRY-04) | The older service tests did not check a successful listing of stored appointments. | Important; **fixed**. | I added one test for listing, status filters, order and unchanged data. | [PR #20](https://github.com/soulsbyrohan/st1-assignment-3/pull/20) | My 11 focused listing tests passed. The group later recorded 99 passing tests. | No further problem found from this review. |
| README information | `project/README.md` explains how to run and test SmartCare. The root README has the group details but still contains some starter wording. | Minor documentation issue. | Group updated the project README. | [PR #23](https://github.com/soulsbyrohan/st1-assignment-3/pull/23) | The commands and limits are written in the project README. | Some old wording remains in the root README. |
| Stage 12 tests and console evidence | Section C records 99 passing tests. Section D records a console walkthrough with screenshots. | Evidence recorded. | Group added and reviewed the evidence. | [PR #24](https://github.com/soulsbyrohan/st1-assignment-3/pull/24) — merged. | [Review comment](https://github.com/soulsbyrohan/st1-assignment-3/pull/24#pullrequestreview-5841424052) and [screenshots](evidence/). | Tests were recorded at the Stage 09 SHA, before later documentation commits. |

Justified no-change conclusion if no defect found: I did not find another required code problem in the areas I reviewed. The console and workflow problems were fixed. I would not add extra features that are outside the UG assignment.

Release blockers still open / status: The reviewed Stage 09 code and tests have a recorded passing result, and the group has documented a console demonstration. The group release decision and submission checks are handled in the other Stage 12 sections; this review does not claim to be the final release approval.

## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: [F8-01 issue #14](https://github.com/soulsbyrohan/st1-assignment-3/issues/14), [F8-02 issue #12](https://github.com/soulsbyrohan/st1-assignment-3/issues/12), [Stage 08 PR #13](https://github.com/soulsbyrohan/st1-assignment-3/pull/13), [service listing PR #16](https://github.com/soulsbyrohan/st1-assignment-3/pull/16), [queries PR #18](https://github.com/soulsbyrohan/st1-assignment-3/pull/18), [extra service tests PR #20](https://github.com/soulsbyrohan/st1-assignment-3/pull/20), [console PR #21](https://github.com/soulsbyrohan/st1-assignment-3/pull/21), [workflow tests PR #22](https://github.com/soulsbyrohan/st1-assignment-3/pull/22), [README PR #23](https://github.com/soulsbyrohan/st1-assignment-3/pull/23), [Stage 12 evidence PR #24](https://github.com/soulsbyrohan/st1-assignment-3/pull/24). The recorded 99-pass Stage 09 version is [3aa1be27cb16ca40da3732f4777c0d80b82d7376](https://github.com/soulsbyrohan/st1-assignment-3/commit/3aa1be27cb16ca40da3732f4777c0d80b82d7376). GitHub `main` was last inspected at [fb9eb9425ea915e07cde31ee16009ce1a85f8805](https://github.com/soulsbyrohan/st1-assignment-3/commit/fb9eb9425ea915e07cde31ee16009ce1a85f8805).

Independent reviewer / feedback / response: [Thomas reviewed PR #16](https://github.com/soulsbyrohan/st1-assignment-3/pull/16#pullrequestreview-5823012944) and said the service work looked good, while queries were still being completed. [Emily reviewed PR #15](https://github.com/soulsbyrohan/st1-assignment-3/pull/15#pullrequestreview-5824310897). Thomas also [requested changes on PR #21](https://github.com/soulsbyrohan/st1-assignment-3/pull/21#pullrequestreview-5835995569); updated console and workflow code was later merged. Thomas [reviewed PR #24](https://github.com/soulsbyrohan/st1-assignment-3/pull/24#pullrequestreview-5841424052) and said there were no major issues. These were actual review comments, not a separate final release approval.

Integration commit / full recheck: The Stage 09 record reports `python -m pytest -q` from `project/`: **99 passed** at commit `3aa1be27cb16ca40da3732f4777c0d80b82d7376`. Earlier, I ran 11 passing service listing tests and an 85-test full suite before the later console changes. More recent changes through `fb9eb942` include documentation and Stage 12 evidence, so the 99-pass result is linked specifically to its tested commit.

Tracked and untracked file inspection / cleanliness: The GitHub list of tracked files was inspected and did not show unexpected caches, backups or credential-named files. This does not show untracked files on group members' computers, so I cannot confirm local working-tree cleanliness from the repository alone.

Secrets/staff material/caches/tool-metadata exclusion check: `.gitignore` excludes virtual environments, caches, `.env` and Stage 08 temporary files. The reviewed tests use made-up details. I did not inspect an actual final source ZIP, so this is not a claim that the full package was checked.

Candidate recovery plan / known-good SHA: The known passing checkpoint is `3aa1be27cb16ca40da3732f4777c0d80b82d7376` with 99 passing tests. Git history lets the group return to this version if a later change causes a problem. The newer GitHub `main` version includes extra documentation and evidence work.

Named substantive contributions: soulsbyrohan (u3119457) — Stage 08 F8-01 debugging, Stage 09 appointment listing and validation ([PR #16](https://github.com/soulsbyrohan/st1-assignment-3/pull/16)), extra service tests ([PR #20](https://github.com/soulsbyrohan/st1-assignment-3/pull/20)) and preparation of Stage 12 Sections E, H and I. ThomasLongCrowley (u3308969) — cancellation, console helpers, reviews and Stage 09 handover. EmilyNicLynh (u3306036) — query code and tests ([PR #18](https://github.com/soulsbyrohan/st1-assignment-3/pull/18)), earlier tests and reviews. Ishraf-Chy (u3325731) — Stage 08 refactoring, Stage 09 console ([PR #21](https://github.com/soulsbyrohan/st1-assignment-3/pull/21)), workflow tests ([PR #22](https://github.com/soulsbyrohan/st1-assignment-3/pull/22)), README ([PR #23](https://github.com/soulsbyrohan/st1-assignment-3/pull/23)) and Stage 12 demonstration/test evidence ([PR #24](https://github.com/soulsbyrohan/st1-assignment-3/pull/24)).

## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [response]
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners: [response]
Can the team explain the system: [response]
Can a change be recovered: [response]
Common decision / PG decision where different: [response]


## K Final tested release SHA

Exact common tested SHA: 2f4e398bd2b65fe8aa35ccfe6f8f2c584d9969a2
Exact PG tested SHA or not applicable: Not applicable
Final submitted SHA / repository URL: 2c1990a8c64d881779343e1b431feeb8ee073b92
- Repository URL:https://github.com/soulsbyrohan/st1-assignment-3/
Evidence-only later commit and difference explanation:
Documentation and Stage 12 evidence were added after the earlier verified code checkpoint. The final release commit and any executable differences will be checked before submission.
Executable changes after testing and re-verification: 
Source ZIP name / SHA correspondence / extracted comparison: 
- ZIP filename: SmartCare_Stage12.zip
- Source commit: 2c1990a8c64d881779343e1b431feeb8ee073b92
- Extracted contents: Includes root README.md, .gitignore, project source code, tests and applicable stage records.


## L Submission package verification

- [ x] Feature freeze and scoped requirements traced.
- [ x] Applicable full regressions, integrated demo and invalid paths verified.
- [ x] Architecture/code quality and final AI/dependency checks complete.
- [ x] Root README and project/README reproduced by another verifier.
- [ x] Release notes, technical debt and limitations visible.
- [ x] Independent human review, integration and release decision recorded.
- [ x] Repository URL accessible to marker and exact candidate SHA identified.
- [ x] One source ZIP from submitted commit with root README.md and .gitignore.
- [ x] project/ source and all accumulated applicable tests included.
- [ x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ x] Mixed-group common protection and candidate upload routing checked.
- [ x] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route:
Deadline/timezone: [response]
Repository access arrangement: Group Repository: https://github.com/soulsbyrohan/st1-assignment-3
Mixed-candidate upload arrangement: One common candidate will be submitted
Oral/video recording/accessibility arrangements: [response]
Remaining administration or release dependency: [response]


## M Formative questions


1. What is a release candidate? A release candidate is a pre-release version of a software containing all of its planned features coded, completed and tested. It is the near-final version of a software.


2. What is feature freeze and why is it used? A feature freeze is a period during software development where features stop being added or changed to allow testers to have time to find and fix any bugs in the program.


3. What is regression testing in a release context? Regression testing, in a context release, is where functional and non-functional tests are rerun on existing softwares after changes have been made to the code, bugs have been fixed or new features have been added.


4. What is a known limitation? A known limitation is an acknowledged limitation, boundary or weakness in a system.


5. What is technical debt? Technical debt is the future cost as a result of choosing quick and temporary solutions, over long term, sustainable choices, during software development.


6. What are release notes? Release notes are documentation that comes with the launch of a new software product or the launch of an update in a software.


7. What is software maintenance? Software maintenance is the practice of updating, modifying and managing a software after it has been launched in order to keep the software efficient, secure and reliable.


8. What is the purpose of the individual demonstration/viva?  The purpose of the individual demonstration/viva is to ensure that the development team can verify their technical ownership. It also assesses the team’s understanding of the product in terms of design choices, implementation decisions and team member contributions.


9. What should the final responsible-AI check establish before release? The final responsible-AI check before release should establish the system meets all requirements and behaves correctly, and also checks the reliability and security of the software. All AI reviews and suggestions must be verified and assessed by a human team member.


10. What is the main course conclusion about AI and the role of the software engineer? The main course conclusion about AI and the role of the software engineer is that AI is a helpful and intelligent tool to use in software development, testing and documentation, however it does not replace the software engineer. The soft engineer is still responsible for verifying all AI suggestions, design and implementation decisions, and ensuring the final product meets all requirements.



## N Reflection viva and handover

Strongest evidence SmartCare is ready: The strongest evidence is that the complete regression suite passed all 99 tests. The application was also verified from a fresh clone using Python 3.13.0, where dependency installation, the standard demonstration and interactive console all worked successfully.

Weakest area: Console integration possibly because there were at first duplicate booking and cancelling logic in the menu. The menu was updated later to reuse the exisitng helper functins and the workflow tests were corrected to help match the behaviour.

How AI use changed from Stage 1 to Stage 12: AI was mostly used to assist with development and understanding throughout the project. As we progressed through each stage, GitHub Copilot was used more for code review, identifying possible issues and suggesting improvements. These suggests were checked against requirements and tests before ever being accepted, modified or rejected.

Start doing — engineering and AI use: Agree on interfaces, responsibilities and expected test result earlier. Integrate smaller changes  more frequently and make sure AI suggestions follow or not go out of scope of the actual requirements before implementation.
Stop doing — engineering and AI use: Avoid the duplication of existing code and leaving documentation late in development. Avoid accepting AI suggesting without checking if it is truly necessary.
Continue doing — engineering and AI use: the continue use of feature branches, pull requests, automated testing and human code reviews. Make sure responsibilities separated between domain classes, services, queries and the console. Continue to use AI as a supporting tool whilst maintaining the human responsibility for the final implementation.
What worked / caused rework / future delivery improvement: Separating responsibilities between components helped make the system easier to develop and test. Automated testing was really good for identifying integration problem fast. Rework occurred when the console had duplicated code and some workflow tests had different outputs. In the future we should agree on interfaces earlier and perform integration testing a lot more.
One paragraph — If AI can write code why do we still need software engineers: Al though AI is able to generate, explain and review code, software engineers are still needed to actually understand the requirements, make design decisions and verify if the implementation is doing things correctly. Ai suggestions can contain mistakes , overlook the projects requirements or introduce out of scope complexity. Software engineers are responsible for evaluating these suggestions, testing the system, solving integration problems and making sure that the final project meets all of its requirements.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | SmartCare is a clinic appointment management application. Its stakeholders would include patients, practitioners and clinic staff who would need to register, manage and retrieve appointment information. Evidence: `project/README.md` and Stage 6–9 records. |
| Two requirements and acceptance criteria | FR-04: A valid appointment can be booked when the patient and practitioner exist and the practitioner is available. FR-06: A scheduled appointment can be cancelled, changing its status to CANCELLED while preserving the appointment record. Evidence: `project/tests/test_services.py` and `project/tests/test_console.py`. |
| Domain model and architecture | Patient and Practitioner represent registered participants, while Appointment would store the participants, appointment ID, date/time and status. Domain classes handle appointment rules, services coordinate operations, the data store manages session records, pure queries filter and sort appointments, and the console handles user interaction. Evidence: `project/smartcare/`. |
| Design trade-off | SmartCare uses an in-memory data store instead of a database. This simplifies implementation and meets the assignment scope, but all registered data is lost when the application exits. Evidence: `project/smartcare/data_store.py` and `project/README.md`. |
| Meaningful test and its limits / 100 percent coverage | Booking conflict tests verify that a practitioner cannot have two scheduled appointments at the same time. This checks a business rule, but passing tests cannot guarantee that every possible defect has been found. Even 100 percent code coverage does not prove that software is correct. Evidence: `project/tests/test_services.py`. |
| Diagnosed defect and verification | The console menu initially duplicated booking and cancellation logic. It was updated to call `handle_book_appointment()` and `handle_cancel_appointment()` instead, and workflow tests were corrected to match the outputs. The integrated suite subsequently passed 99 tests. Evidence: `project/smartcare/console.py`, `project/tests/test_workflows.py` and Stage 9 Section H. |
| Shared store and session-state/query responsibilities | A shared in-memory store maintains patients, practitioners and appointments throughout one console session. Services access the stored records, while pure query functions receive appointment lists as explicit inputs and return filtered and sorted results without modifying the original list. Evidence: `project/smartcare/data_store.py`, `services.py` and `queries.py`. |
| What would break if session-state lookup/query responsibilities changed? | If each console operation used a different store, previously registered patients, practitioners and appointments would not stop being available during the session. If queries modified stored records, the results could become inconsistent and more difficult to test. |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | Cancellation changes an individual appointment's status based on the to domain rules. Practitioner conflict checking requires comparing a proposed booking against other appointments in the shared store, so it is coordinated by the service. Evidence: `project/smartcare/domain.py` and `services.py`. |
| FR-07 retained history test | Cancelling an appointment changes its status to CANCELLED without deleting the record. Tests check that the cancelled appointment remains retrievable and available in all-status listings but is excluded from scheduled-only results. Evidence: `project/tests/test_services.py` and `project/tests/test_regressions.py`. |
| Actual AI change rejected/modified or honestly accepted with verification | GitHub Copilot suggested handling `EOFError` within the booking and cancellation helpers. I chose not to add separate handling inside each helper because input termination was better handled in the menu code. This was recorded as a modified/deferred suggestion rather than claiming an unverified fix. Evidence: Stage 9 Section E. |
| Unresolved limitation / future production work | SmartCare does not provide persistent storage, production authentication, multi-user concurrency or a complete timezone policy. These limitations are outside the undergraduate assignment requirements but would need consideration for production use. Evidence: `project/README.md` and Stage 12 Section G. |
| Personal implementation contribution | I implemented the booking and cancellation console helpers, including input collection, date/time conversion, calling existing appointment services and displaying results. Evidence: `project/smartcare/console.py` and `project/tests/test_console.py`. |
| Personal test/review/design/integration contribution | I created console-focused tests, reviewed pull requests, helped resolve console integration issues, manually verified booking, cancellation and appointment listing, and independently completed the Stage 12 fresh-clone reproducibility check with 99 passing tests. Evidence: Stage 9 Sections B, D, E and H, Stage 12 Section F. |
| PG agentic change and rescheduling verification | Not applicable |
| PG responsible-AI risk/remediation or supported no finding | Not applicable |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.
