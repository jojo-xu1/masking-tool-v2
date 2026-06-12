# Tasks: DOCX/PPTX Split Text Replacement

**Input**: Design documents from `/specs/004-docx-pptx-run-replacement/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/office-replacement-contract.md, quickstart.md

**Tests**: Required. This feature changes supported Office replacement behavior and must include failing-first tests for split-run `.docx` and `.pptx` fixtures, formatting, replacement counts, determinism, and excluded-content safety.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently after shared fixture and helper foundations are complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files and has no dependency on incomplete tasks
- **[Story]**: Which user story this task belongs to, used only in user story phases
- Each task includes exact file paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the existing project has the required Office dependencies and create dedicated test locations for this bug fix.

- [X] T001 Confirm `python-docx`, `python-pptx`, and `pytest` dependencies remain available for this feature in `pyproject.toml`
- [X] T002 Create dedicated Office split-run integration test module in `tests/integration/test_office_split_run_replacement.py`
- [X] T003 [P] Create Office split-run contract test module for scope, formatting, and counting expectations in `tests/contract/test_office_split_run_contract.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared fixtures and Office text-container helper behavior required before any story implementation.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T004 Add shared constants for `Technologies, Inc.` and `会社名_置換済み` in `tests/fixtures/create_fixtures.py`
- [X] T005 Add split-run `.docx` fixture helpers for paragraph and table-cell cases in `tests/fixtures/create_fixtures.py`
- [X] T006 Add split-run `.pptx` fixture helpers for text-box and table-cell cases in `tests/fixtures/create_fixtures.py`
- [X] T007 Add replacement-table helper support for split-run Office rows in `tests/fixtures/create_fixtures.py`
- [X] T008 Add unit tests for Office visible-container replacement helpers, first-run formatting, and one-visible-phrase counting in `tests/unit/test_office_replacer.py`
- [X] T009 Implement shared paragraph-level split-run replacement helper in `src/masking_tool/office_replacer.py`
- [X] T010 Ensure split-run helper reuses deterministic replacement ordering from `src/masking_tool/text_replacer.py`

**Checkpoint**: Shared fixtures and Office split-run helper behavior are ready for story-specific `.docx` and `.pptx` implementation.

---

## Phase 3: User Story 1 - DOCX本文の分割語句を確実に置換する (Priority: P1) MVP

**Goal**: A `.docx` file with visible `Technologies, Inc.` split within the same paragraph or table cell is masked, uses the first visible portion's formatting, and counts each visible phrase as one replacement.

**Independent Test**: Process split-run `.docx` paragraph and table-cell fixtures and verify `Technologies, Inc.` is absent, `会社名_置換済み` appears, replacement formatting follows the first visible portion, and replacement count is one per visible phrase.

### Tests for User Story 1

- [X] T011 [US1] Add `.docx` split paragraph integration test in `tests/integration/test_office_split_run_replacement.py`
- [X] T012 [US1] Add `.docx` split table-cell integration test in `tests/integration/test_office_split_run_replacement.py`
- [X] T013 [US1] Add `.docx` first-run `bold`, `italic`, font size, and color assertions in `tests/integration/test_office_split_run_replacement.py`
- [X] T014 [US1] Add `.docx` one-visible-phrase replacement count assertion in `tests/integration/test_office_split_run_replacement.py`

### Implementation for User Story 1

- [X] T015 [US1] Route `.docx` paragraphs through the shared split-run replacement helper in `src/masking_tool/office_replacer.py`
- [X] T016 [US1] Route `.docx` table-cell paragraphs through the shared split-run replacement helper in `src/masking_tool/office_replacer.py`
- [X] T017 [US1] Preserve first matched run `bold`, `italic`, font size, and color for `.docx` replacement text in `src/masking_tool/office_replacer.py`
- [X] T018 [US1] Return one replacement count per matched visible `.docx` phrase in `src/masking_tool/office_replacer.py`

**Checkpoint**: User Story 1 is independently functional and testable as the MVP.

---

## Phase 4: User Story 2 - PPTX本文の分割語句を確実に置換する (Priority: P1)

**Goal**: A `.pptx` file with visible `Technologies, Inc.` split within the same text box or table cell is masked, uses the first visible portion's formatting, and counts each visible phrase as one replacement.

**Independent Test**: Process split-run `.pptx` text-box and table-cell fixtures and verify `Technologies, Inc.` is absent, `会社名_置換済み` appears, replacement formatting follows the first visible portion, and replacement count is one per visible phrase.

### Tests for User Story 2

- [X] T019 [US2] Add `.pptx` split text-box integration test in `tests/integration/test_office_split_run_replacement.py`
- [X] T020 [US2] Add `.pptx` split table-cell integration test in `tests/integration/test_office_split_run_replacement.py`
- [X] T021 [US2] Add `.pptx` first-run `bold`, `italic`, font size, and color assertions in `tests/integration/test_office_split_run_replacement.py`
- [X] T022 [US2] Add `.pptx` one-visible-phrase replacement count assertion in `tests/integration/test_office_split_run_replacement.py`

### Implementation for User Story 2

- [X] T023 [US2] Route `.pptx` text-frame paragraphs through the shared split-run replacement helper in `src/masking_tool/office_replacer.py`
- [X] T024 [US2] Route `.pptx` table-cell paragraphs through the shared split-run replacement helper in `src/masking_tool/office_replacer.py`
- [X] T025 [US2] Preserve first matched run `bold`, `italic`, font size, and color for `.pptx` replacement text in `src/masking_tool/office_replacer.py`
- [X] T026 [US2] Return one replacement count per matched visible `.pptx` phrase in `src/masking_tool/office_replacer.py`

**Checkpoint**: User Stories 1 and 2 both work independently for split-run Office body text.

---

## Phase 5: User Story 3 - 既存の安全境界と結果確認を維持する (Priority: P2)

**Goal**: The split-run fix does not weaken excluded-content reporting, no-match behavior, unsplit Office replacement, original-file safety, or deterministic rerun behavior.

**Independent Test**: Process excluded-content and regression Office samples and verify embedded objects and image text remain out of scope, no-match files do not falsely report replacement, unsplit Office text still works, and repeated runs produce identical visible results and counts.

### Tests for User Story 3

- [X] T027 [P] [US3] Add contract tests for in-scope and out-of-scope split-run boundaries in `tests/contract/test_office_split_run_contract.py`
- [X] T028 [P] [US3] Add embedded-object and `skipped_unsupported.txt` safety regression test for split-run Office files in `tests/integration/test_excluded_office_scope.py`
- [X] T029 [P] [US3] Add no-match `.docx` and `.pptx` split-run-adjacent regression tests in `tests/integration/test_office_split_run_replacement.py`
- [X] T030 [P] [US3] Add unsplit `.docx` and `.pptx` regression assertions in `tests/integration/test_single_office_files.py`
- [X] T031 [P] [US3] Add deterministic rerun coverage for split-run `.docx` and `.pptx` outputs and counts in `tests/integration/test_deterministic_rerun.py`

### Implementation for User Story 3

- [X] T032 [US3] Preserve embedded-object out-of-scope notes while replacing visible split-run text in `src/masking_tool/office_replacer.py`
- [X] T033 [US3] Ensure no-match `.docx` and `.pptx` files remain successful processed outputs in `src/masking_tool/app.py`
- [X] T034 [US3] Ensure original input files are not overwritten by split-run Office processing in `src/masking_tool/app.py`
- [X] T035 [US3] Ensure split-run Office processing does not alter `.txt`, `.csv`, `.log`, `.xlsx`, or text-layer `.pdf` dispatch behavior in `src/masking_tool/app.py`

**Checkpoint**: Safety boundaries and existing Office behavior remain intact after the split-run fix.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, quickstart alignment, and cleanup across all stories.

- [X] T036 [P] Update quickstart validation results for split-run Office scenarios in `specs/004-docx-pptx-run-replacement/quickstart.md`
- [X] T037 [P] Add fixture documentation for split-run Office samples in `tests/fixtures/README.md`
- [X] T038 Run `python -m pytest tests/integration/test_office_split_run_replacement.py` and fix failures in `src/masking_tool/office_replacer.py`
- [X] T039 Run `python -m pytest tests/integration/test_single_office_files.py tests/integration/test_excluded_office_scope.py tests/integration/test_deterministic_rerun.py` and fix regressions in affected `src/masking_tool/` files
- [X] T040 Run full `python -m pytest` and fix any remaining regressions in affected `src/masking_tool/` and `tests/` files
- [X] T041 Run `git diff --check` and resolve formatting issues in `specs/004-docx-pptx-run-replacement/tasks.md`, `src/masking_tool/office_replacer.py`, and affected `tests/` files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP
- **User Story 2 (Phase 4)**: Depends on Foundational and can proceed alongside US1 after shared helper behavior exists
- **User Story 3 (Phase 5)**: Depends on US1 and US2 behavior enough to validate safety and regression coverage
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational; delivers `.docx` split-run masking
- **US2 (P1)**: Can start after Foundational; delivers `.pptx` split-run masking
- **US3 (P2)**: Starts after split-run behavior exists for at least one Office format; final validation depends on US1 and US2

### Parallel Opportunities

- T003 can run in parallel with T002 after dependency confirmation.
- T011 through T014 should be authored sequentially because they share `tests/integration/test_office_split_run_replacement.py`.
- T019 through T022 should be authored sequentially because they share `tests/integration/test_office_split_run_replacement.py`.
- T027 through T031 can be authored in parallel because they touch distinct regression concerns.
- T036 and T037 can run in parallel after implementation is stable.

---

## Parallel Example: User Story 1

```text
US1 uses one focused integration test file and one implementation file, so its tasks should be executed sequentially:

Task: "T011 [US1] Add `.docx` split paragraph integration test in tests/integration/test_office_split_run_replacement.py"
Task: "T012 [US1] Add `.docx` split table-cell integration test in tests/integration/test_office_split_run_replacement.py"
Task: "T015 [US1] Route `.docx` paragraphs through the shared split-run replacement helper in src/masking_tool/office_replacer.py"
```

## Parallel Example: User Story 2

```text
US2 also shares the Office split-run test and implementation files, so its tasks should be executed sequentially:

Task: "T019 [US2] Add `.pptx` split text-box integration test in tests/integration/test_office_split_run_replacement.py"
Task: "T020 [US2] Add `.pptx` split table-cell integration test in tests/integration/test_office_split_run_replacement.py"
Task: "T023 [US2] Route `.pptx` text-frame paragraphs through the shared split-run replacement helper in src/masking_tool/office_replacer.py"
```

## Parallel Example: User Story 3

```text
Task: "T027 [P] [US3] Add contract tests for in-scope and out-of-scope split-run boundaries in tests/contract/test_office_split_run_contract.py"
Task: "T028 [P] [US3] Add embedded-object safety regression test for split-run Office files in tests/integration/test_excluded_office_scope.py"
Task: "T031 [P] [US3] Add deterministic rerun coverage for split-run `.docx` and `.pptx` outputs and counts in tests/integration/test_deterministic_rerun.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational shared fixture and helper tasks
3. Complete Phase 3: User Story 1 `.docx` split-run replacement
4. Stop and validate `.docx` paragraph/table-cell replacement, first-run formatting, and one-visible-phrase counting

### Incremental Delivery

1. Setup + Foundational -> split-run fixtures and shared Office helper ready
2. US1 -> `.docx` split-run replacement MVP
3. US2 -> `.pptx` split-run replacement using the same helper semantics
4. US3 -> safety boundary, no-match, unsplit Office, and deterministic rerun regression coverage
5. Polish -> quickstart, fixture docs, focused tests, full suite, and formatting checks

### Validation Gates

1. Tests for each story are written before implementation and fail for the current run-only behavior.
2. Each story reaches its checkpoint before moving to the next priority.
3. Full pytest and `git diff --check` pass before the feature is considered complete.
