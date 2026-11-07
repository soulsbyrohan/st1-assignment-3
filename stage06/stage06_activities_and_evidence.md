# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Group 1 (Wednesday 2:30pm-4:30pm)
- Members, GitHub usernames and cohorts: Rohan Soulsby, soulsbyrohan | Ishraf Anas, Ishraf-Chy | Emily Nicole, EmilyNicLynh | Thomas Crowley, ThomasLongCrowley.
- Repository URL: https://github.com/soulsbyrohan/st1-assignment-3
- Starting SHA: 2e13f23faeb0f9b550bee18520295d350b6a5e42

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Implement Patient Search
- Context: The Patient class already has patient registration, but the search method was unfinished.
- Requirement: FR-02 Find a patient by patient ID.
- Acceptance criteria:
  - Registered patient can be found by their ID
  - Unknown ID raises LookupError
  - Blank ID raises ValueError
  - IDs are trimmed
  - IDs are case sensitive
- Scope: Implement 'find_patient()' in 'services.py' and add tests in 'test_services.py'.
- Definition of Done: Implementation and tests completed, starter tests passing, PR reviewed, feedback resolved and merged into main.
- Owner: u3306036
- Actual issue link: https://github.com/soulsbyrohan/st1-assignment-3/issues/6

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Implement Appointment Cancellation with Retained History
- Context: The Appointment class already supports cancellation, but the service method was unfinished.
- Requirement: FR-06 allows scheduled appointments to be cancelled. FR-07 requires cancelled records to remain stored.
- Acceptance criteria:
  - Scheduled appointments change to CANCELLED.
  - Completed and already cancelled appointments cannot be cancelled.
  - Invalid IDs raise ValueError; unknown IDs raise LookupError.
  - Successful cancellation returns the original stored appointment.
  - Cancelled records remain accessible.
  - Existing booking and conflict behaviour is preserved.
- Scope: Implement `cancel_appointment()` in `services.py` and add tests in `test_services.py`.
- Definition of Done: Implementation and tests completed, starter tests passing, PR reviewed, feedback resolved and merged into main.
- Owner: U3308969
- Actual issue link: https://github.com/soulsbyrohan/st1-assignment-3/issues/1

### Practitioner Lookup (Supporting FR-03)

- Title: Implement Practitioner Search
- Context: Practitioner lookup was unfinished in the service layer.
- Requirement: Find a registered practitioner using their practitioner ID. This supports FR-03, which concerns practitioner registration.
- Acceptance criteria:
  - Registered practitioner can be found by their ID.
  - Unknown practitioner ID raises LookupError.
  - Blank or invalid practitioner ID raises ValueError.
  - Leading and trailing whitespace in IDs is trimmed.
  - Practitioner IDs are case-sensitive.
- Scope: Implement `PractitionerService.find_practitioner()` in `project/smartcare/services.py` and add unit tests in `project/tests/test_services.py`.
- Definition of Done: Implementation and tests completed, PR reviewed and merged into main.
- Owner: [u3325731]
- Actual issue link: https://github.com/soulsbyrohan/st1-assignment-3/issues/3

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | Too vague. It does not explain what was changed or why. |
| final version | Weak | Does not identify the feature or improvement and gives no useful context. |
| Add patient search by ID | Strong | Clearly identifies the functionality implemented, making the commit easy to understand and trace. |
| fix stuff | Weak | Does not describe the problem or the specific fix, making review and future maintenance difficult. |
| Prevent cancellation of completed appointments | Strong | Describes a specific behavioural rule and the change made to enforce it. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR includes unrelated changes beyond appointment cancellation, making it harder to understand and review.
- Responsibility and architecture concerns: Renaming patient fields and restructuring unrelated code could affect other components and violate separation of responsibilities.
- Testing and review concerns: Unrelated changes increase the risk of regression and make it difficult to identify which changes caused a test failure.
- Changes to remove or separate, with reasons: Remove the unrelated patient field renaming, code restructuring and new dependency from this PR. These should be handled in separate issues and PRs so each change can be reviewed and tested independently.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: The review does not explain which files were examined, whether the implementation meets the acceptance criteria, or whether the tests cover positive, negative and boundary cases. Passing tests alone does not guarantee correct behaviour.
- Follow-up review question 1: Does the implementation satisfy all acceptance criteria for the assigned functional requirement?
- Follow-up review question 2: Are invalid inputs and unknown IDs handled using the correct exceptions?
- Follow-up review question 3: Do the tests contain meaningful assertions that verify actual behaviour rather than simply checking that an object exists?
- Follow-up review question 4: Does the PR introduce any unrelated changes or modify existing functionality unexpectedly?
- Follow-up review question 5: Were all existing tests and new tests executed successfully, and what evidence supports the results?
- Additional questions if useful: Does the implementation follow the existing architecture and reuse the appropriate service, domain and data-store methods?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Actual Stage 06 branches used: `feature/appointment_cancellation`, `feature/practitioner-search`, `feature/patient-search`|
| Commit message convention | Commits are intended to describe one change and its purpose; the repository includes focused commit messages and merge messages. |
| PR size | One feature and related tests per pull request; this was followed in intent, but an unrelated practitioner placeholder edit in PR #5 was identified and addressed during integration. |
| Another-member review requirement | All three PRs were reviewed by `soulsbyrohan`|
| Merge rule |Review the diff, resolve feedback, verify tests and merge to `main`.|
| Significant Copilot disclosure rule | Actual Copilot review outputs for PRs #2/#3/#5 are posted to their conversations|

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/soulsbyrohan/st1-assignment-3/issues/6 | FR-02 Patient search | EmilyNicLynh | Return same stored patient; error/trim/case checks in issue #6 | Closed issue #6; PR #5 merged 2026-11-04|
| https://github.com/soulsbyrohan/st1-assignment-3/issues/1 | FR-06/FR-07 cancellation/history | ThomasLongCrowley | Retain appointment and reject illegal cancellation in issue #1 | Closed issue #1; PR #2 merged 2026-11-04|
| https://github.com/soulsbyrohan/st1-assignment-3/issues/4 | Practitioner lookup (supporting operation under FR-03 registration) | Ishraf-Chy | Same stored object, invalid/missing IDs and whitespace in issue #4 | Closed issue #4; PR #3 merged 2026-11-04|

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.


- PR link and title: https://github.com/soulsbyrohan/st1-assignment-3/pull/2 — Stage 06: Implemented appointment cancellation (FR-06)
- Linked issue and requirement: https://github.com/soulsbyrohan/st1-assignment-3/issues/1 (FR-06/FR-07)
- Feature branch: `feature/appointment_cancellation`
- Changed behaviour: Scheduled appointments can be cancelled while retaining their records.
- Meaningful commits: [Original commit](https://github.com/soulsbyrohan/st1-assignment-3/commit/f96134d150f7fb767979177cfe334c2f6e665deb); [feedback changes](https://github.com/soulsbyrohan/st1-assignment-3/pull/2/changes/e7772122f69b893abd399029c95a94dd5acde6b7)
- Test command, directory and observed result: `python -m pytest -v` from `project/` — tests passed locally.
- Another-member reviewer: soulsbyrohan.
- Human observations recorded before Copilot: [Initial review](https://github.com/soulsbyrohan/st1-assignment-3/pull/2#pullrequestreview-5737687228), 2026-11-03 01:00 AEDT; predates [Copilot post](https://github.com/soulsbyrohan/st1-assignment-3/pull/2#issuecomment-6594723061), 14:30 AEDT.
- Requirement, responsibilities, test assertions and unrelated-scope checks: Reviewed domain-owned status, same-object identity, invalid/completed/repeated cancellation and rebooking. Cancellation tests verify record retrievability and final list-retention assertion.
- Key feedback: Add retained-history and whitespace-only ID assertions.
- Author response/change and verification: Added the retained-history assertion and whitespace-only ID test in commit e777212 - tests passed locally.
- Reviewer recheck and approval: Human (soulsbyrohan) review https://github.com/soulsbyrohan/st1-assignment-3/pull/2#pullrequestreview-5737687228 and later requested changes (2026-11-03 14:54 AEDT)
- Merge outcome and SHA: Merged on 2026-11-04 15:40 AEDT, merge commit `1dd1757abcb7faf3a5f28dc1b447356f5e03ac2d`.
- Significant Copilot assistance: [Copilot review](https://github.com/soulsbyrohan/st1-assignment-3/pull/2#issuecomment-6594723061) recommended direct history and whitespace-only ID assertions.
- Linked issue closure: [Issue #1](https://github.com/soulsbyrohan/st1-assignment-3/issues/1) closed 2026-11-04.
- Each member updated main: All group members pulled the latest main branch after the Stage 6 PRs were merged.
- Integrated verification after merge: Group-reported `python -m pytest -v` from `project/`: `27 passed, 0 failed`.

- PR link and title: [Stage 6: Implement Practitioner Search (FR-03)](https://github.com/soulsbyrohan/st1-assignment-3/pull/3)
- Linked issue and requirement: [Issue #4](https://github.com/soulsbyrohan/st1-assignment-3/issues/4) — Stage 06 practitioner lookup associated with FR-03.
- Feature branch: `feature/practitioner-search`
- Changed behaviour: Returns original stored practitioner; raises `LookupError` for missing ID; appoints ID validation to shared store.
- Meaningful commits: [PR commits](https://github.com/soulsbyrohan/st1-assignment-3/pull/3/commits), [merge](https://github.com/soulsbyrohan/st1-assignment-3/commit/84de8f21f50a40728b6faef160da971e2c2ce29e)
- Test command, directory and observed result: `python -m pytest -q` → `14 passed in 0.04s` ([test comment](https://github.com/soulsbyrohan/st1-assignment-3/pull/3#issuecomment-6594882188).
- Another-member reviewer: soulsbyrohan.
- Human observations recorded before Copilot: [Human review](https://github.com/soulsbyrohan/st1-assignment-3/pull/3#pullrequestreview-5746954138) and [readability observation](https://github.com/soulsbyrohan/st1-assignment-3/pull/3#pullrequestreview-5746963327).
- Requirement, responsibilities, test assertions and unrelated-scope checks: Six tests verify original object identity, unknown, blank, invalid type, trimmed and case-sensitive IDs. No cancellation logic changed.
- Key feedback: Human reviewer suggested clearer documentation; Copilot suggested an optional explicit empty-string ID test.
- Author response/change and verification: Six focused tests were included and 14 passing tests reported. Optional extra empty-string test was not required for correct implementation.
- Reviewer recheck and approval: Two reviews by soulsbyrohan and approved.
- Merge outcome and SHA: Merged 2026-11-04 15:17 AEDT; merge commit `84de8f21f50a40728b6faef160da971e2c2ce29e`.
- Significant Copilot assistance: [Copilot review](https://github.com/soulsbyrohan/st1-assignment-3/pull/3#issuecomment-6594873353): no important defect, optional empty-string test.
- Linked issue closure: [Issue #4](https://github.com/soulsbyrohan/st1-assignment-3/issues/4) closed 2026-11-04.
- Each member updated main: All group members pulled the latest main branch after the Stage 6 PRs were merged.
- Integrated verification after merge: Group-reported `python -m pytest -v` from `project/`: `27 passed, 0 failed`.

- PR link and title: [Stage 06: Implementation of Patient Lookup (FR-02)](https://github.com/soulsbyrohan/st1-assignment-3/pull/5)
- Linked issue and requirement: [Issue #6](https://github.com/soulsbyrohan/st1-assignment-3/issues/6) — FR-02 patient lookup.
- Feature branch: `feature/patient-search`
- Changed behaviour: Returns original stored patient; raises `LookupError` if missing; appoints invalid ID validation to store.
- Meaningful commits: [PR commits](https://github.com/soulsbyrohan/st1-assignment-3/pull/5/commits), [merge 0597b9e](https://github.com/soulsbyrohan/st1-assignment-3/commit/0597b9e6ff56e188742cf2cb1f20cf65f1356002)
- Test command, directory and observed result: Reviewer reported `python -m pytest -q` → `14 passed in 0.06s` ([test comment](https://github.com/soulsbyrohan/st1-assignment-3/pull/5#issuecomment-6595132227)); integrated group report: 27 passed.`.
- Another-member reviewer: soulsbyrohan.
- Human observations recorded before Copilot: [review](https://github.com/soulsbyrohan/st1-assignment-3/pull/5#pullrequestreview-5747028197), 2026-11-03 14:46 AEDT.
- Requirement, responsibilities, test assertions and unrelated-scope checks: Six tests cover identity, unknown, trimmed, blank, case-sensitive and invalid ID inputs. Early unrelated practitioner placeholder deletion identified and correct merged practitioner method preserved.
- Key feedback: Human and Copilot independently identified unrelated practitioner placeholder; optional whitespace-only patient-ID test suggested.
- Author response/change and verification: Merge conflict resolution retained the working practitioner lookup and incorporated patient lookup and tests; reviewer formally approved.
- Reviewer recheck and approval: [APPROVED by soulsbyrohan](https://github.com/soulsbyrohan/st1-assignment-3/pull/5#pullrequestreview-5763140111) 2026-11-04 15:17 AEDT, after a prior change request.
- Merge outcome and SHA: Merged 2026-11-04 15:32 AEDT; merge commit `0597b9e6ff56e188742cf2cb1f20cf65f1356002`.
- Significant Copilot assistance: [Copilot review](https://github.com/soulsbyrohan/st1-assignment-3/pull/5#issuecomment-6595122523) confirmed practitioner scope regression and optional whitespace-only patient test.
- Linked issue closure: [Issue #6](https://github.com/soulsbyrohan/st1-assignment-3/issues/6) closed 2026-11-04.
- Each member updated main: All group members pulled the latest main branch after the Stage 6 PRs were merged.
- Integrated verification after merge: Group-reported `python -m pytest -v` from `project/`: `27 passed, 0 failed`.

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: soulsbyrohan — Copilot-assisted review of PR #2, appointment cancellation with retained history (FR-06/FR-07).
- Prompt/purpose and relevant issue/diff: Review `https://github.com/soulsbyrohan/st1-assignment-3/pull/2` against issue #1.
- Summary of output: Copilot found the cancellation service correctly delegates to `Appointment.cancel()` and tests cover major cases. It recommended directly asserting `list_appointments()` retains the cancelled object and adding a whitespace-only ID test.
- Human check against actual code, requirements and tests: PR tests already assert same-object lookup after cancellation and unchanged status after invalid transitions; the two additional assertions would strengthen coverage without needing a code rewrite. Reviewer reported `python -m pytest -q`: `15 passed in 0.05s`.
- Decision — Accept / Modify / Reject: **Modify**: retain the service implementation and use stronger list-retention and whitespace-only ID tests.
- Reason: Copilot's new test suggestions are useful, but its description of retention as not verified is too strong: a test already asserts retrieval of the original cancelled object. The existing failed-transition tests also check unchanged state.
- Verification/evidence: Human-first review: https://github.com/soulsbyrohan/st1-assignment-3/pull/2#pullrequestreview-5737687228 (2026-11-03 01:00 AEDT); reviewer test report: https://github.com/soulsbyrohan/st1-assignment-3/pull/2#issuecomment-6594718565 (15 passed); Copilot output posted at https://github.com/soulsbyrohan/st1-assignment-3/pull/2#issuecomment-6594723061 (2026-11-03 14:30 AEDT)

- Member and task: soulsbyrohan — Copilot-assisted static review of PR #3, practitioner lookup (FR-03).
- Prompt/purpose and relevant issue/diff: Review https://github.com/soulsbyrohan/st1-assignment-3/pull/3 against issue #4, including identity, invalid/missing IDs, whitespace/case.
- Summary of output: Copilot reported no Critical/Important defects. It recommended an optional suggestion of an explicit empty-string test.
- Human check against actual code, requirements and tests: Human-first reviews confirmed original object identity, `LookupError` for absent practitioner and delegated `ValueError` validation. The supplied tests already cover whitespace-only input and `None`, so the empty-string test would be extra regression protection, not a fix. A human reviewer reported `14 passed in 0.04s`.
- Decision — Accept / Modify / Reject: **Reject**: existing shared validation rejects empty-string IDs.
- Reason: Empty string must fail via `required_text()`.
- Verification/evidence: Human-first reviews https://github.com/soulsbyrohan/st1-assignment-3/pull/3#pullrequestreview-5746954138 and https://github.com/soulsbyrohan/st1-assignment-3/pull/3#pullrequestreview-5746963327; Copilot posted https://github.com/soulsbyrohan/st1-assignment-3/pull/3#issuecomment-6594873353; reviewer-reported test result https://github.com/soulsbyrohan/st1-assignment-3/pull/3#issuecomment-6594882188 (`14 passed in 0.04s`).

- Member and task: soulsbyrohan — Copilot-assisted static review of PR #5, patient lookup (FR-02).
- Prompt/purpose and relevant issue/diff: Review https://github.com/soulsbyrohan/st1-assignment-3/pull/5 and issue #6 for patient-lookup behaviour, service/store boundaries, acceptance tests and unrelated changes.
- Summary of output: Copilot found an **Important scope regression**: PR #5 deletes the `find_practitioner()` `NotImplementedError` without implementing that unrelated method, potentially allowing it to return `None`. It also proposed an optional whitespace-only patient ID test.
- Human check against actual code, requirements and tests: Review identified the same practitioner-method regression before this Copilot output was supplied. Diff shows patient lookup returns the stored object via `SmartCareDataStore.find_patient()`, raising `LookupError` when missing.
- Decision — Accept / Modify / Reject: **Accept**
- Reason: The regression is real and breaches the PR's FR-02 scope.
- Verification/evidence: Human-first change request https://github.com/soulsbyrohan/st1-assignment-3/pull/5#pullrequestreview-5747028197 (2026-11-03 14:46 AEDT). Copilot review posted at https://github.com/soulsbyrohan/st1-assignment-3/pull/5#issuecomment-6595122523. Reviewer test report https://github.com/soulsbyrohan/st1-assignment-3/pull/5#issuecomment-6595132227 (`14 passed in 0.06s`).

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: PR #2: human review confirmed `Appointment.cancel()` delegation, same-object retention, invalid/repeated cancellation and rebooking. PR #3: two human reviews checked object identity, missing IDs, validation, case, readability and integration. PR #5: human review requested changes for the unrelated practitioner placeholder removal.
- Copilot noticed: PR #2: direct `list_appointments()` and whitespace-only ID test suggestions . PR #3: no critical defect; optional explicit empty-string practitioner-ID test . PR #5: independently confirmed the practitioner placeholder deletion was an Important scope regression and suggested an optional whitespace-only patient-ID test.
- Overlap: Human and Copilot agreed the feature methods should use the shared store, return original objects, check ID validation, and avoid unrelated code changes. Both specifically identified PR #5's unrelated practitioner-method regression.
- What did the human reviewer notice that Copilot did not: PR #3 human review requested clearer code documentation/readability and further integration testing; Copilot considered the implementation correct and treated additional empty-string coverage as optional. PR #2 human review highlighted slot rebooking, also mentioned in Copilot's test summary.
- What did Copilot identify that the human reviewer initially missed: explicit empty-string practitioner ID in PR #3; whitespace-only patient ID in PR #5.
- Unsupported or incorrect Copilot suggestion: PR #2 Copilot overstated absence of retention evidence: the existing test retrieves the exact same cancelled appointment by ID
- Human judgement accepted, modified or rejected, and why: PR #2 strengthened retention and whitespace-only tests while retaining correct cancellation.
- Which evidence justified merge approval: PR 5 was approved after correction.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: U3308969
- Implementation: Implemented `AppointmentService.cancel_appointment()` using existing lookup and domain cancellation methods. PR #2.
- Testing: Added tests for successful cancellation, repeated cancellation, completed appointments, invalid IDs and retained history. all tests passed locally.
- Review: Addressed reviewer feedback by adding retained-history and whitespace-only ID checks.
- Issue refinement: Created Issue #1 with FR-06/FR-07 acceptance criteria.
- Design and responsibility discussion: Used the existing `Appointment.cancel()` method instead of directly changing appointment status.
- Debugging or integration: Corrected an incorrect status assertion during testing.
- Documentation or team support: Completed FR-06/FR-07 requirement and did my parts in section A, F and G.

- Member: u3306036
- Implementation: Implemented `PatientService.find_patient()`. PR #5.
- Testing: Added tests for successful patient search. All tests passed locally. 
- Review: Corrected the placement of the patient search implementation in services.py
- Issue refinement: Created Issue #2 with FR-02 acceptance criteria.
- Design and responsibility discussion: Used the existing `find_patient()` method.
- Debugging or integration: Made sure the patient search tests passed
- Documentation or team support: Completed FR-02 requirement and did my parts in section A, F and G.

- Member: U3119457 (Rohan Soulsby)
- Implementation: NA
- Testing: Tested and confirmed all PRs in human reviews. 
- Review: PR #2 (https://github.com/soulsbyrohan/st1-assignment-3/pull/2#pullrequestreview-5737687228); PR #3 (https://github.com/soulsbyrohan/st1-assignment-3/pull/3#pullrequestreview-5746954138, https://github.com/soulsbyrohan/st1-assignment-3/pull/3#pullrequestreview-5746963327); PR #5 (https://github.com/soulsbyrohan/st1-assignment-3/pull/5#pullrequestreview-5747028197).
- Issue refinement: Confirmed issues #1, #4, #6 and their acceptance criteria
- Design and responsibility discussion: Identified correct domain-owned cancellation, existing data-store lookups, and unrelated practitioner deletion in PR #5.
- Debugging or integration: All issues in my reviews were resolved and tested. Final approvals given and merged to main.
- Documentation or team support: Commented reviews in PRs 02, 03, 05. Completed Stage 6 Activities and Evidence MD.

Member: u3325731
- Implementation: Implemented `PractitionerService.find_practitioner()` to search for registered practitioners using their ID. PR #3.
- Testing: Added six tests for successful practitioner search, unknown IDs, blank IDs, invalid inputs, whitespace handling and case sensitivity. All tests passed locally.
- Review: Received feedback on the tests and code readability, and checked the suggestions before finalising my work.
- Issue refinement: Worked on Issue #4 for practitioner lookup and its acceptance criteria.
- Design and responsibility discussion: Used the existing data store's `find_practitioner()` method instead of creating a separate search process.
- Debugging or integration: Checked that practitioner search worked correctly with the existing code and ran the full test suite after integration. 27 tests passed.
- Documentation or team support: Completed my practitioner lookup contribution and added the relevant testing and PR evidence to the Stage 6 Markdown file.

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

Commit count measures activity rather than quality. A small, well-tested fix or careful review may contribute more than numerous un-useful commits.

## L Stage 6 formative questions

1. What is version control?

Version control tracks changes to files so a team can collaborate, review history and restore earlier versions.

2. Why is a feature branch useful?

A feature branch isolates one change from stable main until it has been tested and reviewed.

3. What makes a commit a good engineering commit?

A good commit records a coherent change and has a message that clearly describes it.

4. What is a pull request?

A pull request proposes merging branch changes and provides a diff and discussion for review.

5. What is the purpose of code review?

Code review checks requirements, correctness, architecture, tests and unintended changes.

6. What does a Git diff show?

A Git diff shows lines added, removed and changed between versions.

7. What is a Definition of Done?

Definition of Done describes the evidence required for completed work, including tests, review, feedback and integration.

8. What is the appropriate role of GitHub Copilot in pull-request review?

Copilot is a second opinion after a human-first review; humans must verify its claims and make merge decisions.

9. Why should individual contribution not be judged only by commit count?

A large commit count can represent minor or low-quality edits; reviews, testing and integration may be substantial contributions with few commits.

10. What is the Stage 6 engineering rule?

Take each requirement through issue, focused branch, implementation, meaningful tests, independent review and integration.

## M Completion and handover

- Starting SHA: `2e13f23faeb0f9b550bee18520295d350b6a5e42`.
- Final Stage 6 code SHA: `65275cba8859f40bce27ad36f12d987c3150f2df`.
- Test command: `python -m pytest -v`
- Working directory: `project/`
- Observed result: **27 passed, 0 failed**.
- PR and another-member reviewer: [#2](https://github.com/soulsbyrohan/st1-assignment-3/pull/2) — soulsbyrohan COMMENTED/CHANGES_REQUESTED; [#3](https://github.com/soulsbyrohan/st1-assignment-3/pull/3) — soulsbyrohan COMMENTED; [#5](https://github.com/soulsbyrohan/st1-assignment-3/pull/5) — soulsbyrohan CHANGES_REQUESTED then [APPROVED](https://github.com/soulsbyrohan/st1-assignment-3/pull/5#pullrequestreview-5763140111).
- Unresolved issue or none: Issues #1, #4 and #6 are closed; all three PRs are merged and all three Stage 06 implementations are on `main`.
- Stage 7 handover status:
- Final submitted SHA if later than tested SHA: [`192f3a0`](https://github.com/soulsbyrohan/st1-assignment-3/commit/192f3a00fa7202d33a2f0f471280093bd4195734).

- [x] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [x] At least two focused issues link requirements and acceptance criteria.
- [x] Feature work reviewed by another member using the actual diff.
- [x] Human-first review and required Copilot comparison recorded.
- [x] Feedback resolved and approval recorded before merge.
- [x] Everyone pulled main and integrated checks passed.
- [x] Required activities, quiz responses and contribution notes completed.
- [x] Only synthetic data included; confidential peer material kept out.
- [x] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
