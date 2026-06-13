# Tasks: Unicode Normalization Matching

**Input**: Design documents from `/specs/005-unicode-normalization-matching/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/unicode-normalization-contract.md, quickstart.md

**Tests**: Required. This feature changes supported replacement behavior and must include failing-first tests for width-equivalent matching, exact raw match precedence, exact replacement proposal preservation, CJK preservation, deterministic reruns, supported format coverage, and excluded-content safety.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently after shared matching and fixture foundations are complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files and has no dependency on incomplete tasks
- **[Story]**: Which user story this task belongs to, used only in user story phases
- Each task includes exact file paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm current dependencies and create dedicated test locations for Unicode width matching.

- [X] T001 Confirm Python 3.11+, `openpyxl`, `python-docx`, `python-pptx`, PyMuPDF, and pytest dependencies remain available for this feature in `pyproject.toml`
- [X] T002 Create Unicode normalization contract test module in `tests/contract/test_unicode_normalization_contract.py`
- [X] T003 [P] Create Unicode normalization integration test module in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T004 [P] Create Unicode normalization fixture generator in `tests/fixtures/create_unicode_normalization_samples.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared fixtures and matching behavior required before any user story can be implemented.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T005 Add full-width and half-width sample constants for `Technologies, Inc.` and `Ｔｅｃｈｎｏｌｏｇｉｅｓ， Ｉｎｃ．` in `tests/fixtures/create_fixtures.py`
- [X] T006 Add replacement proposal constants that preserve full-width, half-width, punctuation, spacing, and CJK characters in `tests/fixtures/create_fixtures.py`
- [X] T007 Add generated replacement table fixture for Unicode width rows in `tests/fixtures/create_unicode_normalization_samples.py`
- [X] T008 Add generated `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-layer `.pdf` Unicode width fixtures in `tests/fixtures/create_unicode_normalization_samples.py`
- [X] T009 [P] Add unit tests for comparison-only width key behavior in `tests/unit/test_text_replacer.py`
- [X] T010 [P] Add unit tests for exact raw match precedence over width-equivalent candidates in `tests/unit/test_text_replacer.py`
- [X] T011 Implement shared width-equivalent match helpers with raw span preservation in `src/masking_tool/text_replacer.py`
- [X] T012 Implement deterministic candidate selection with exact raw match precedence in `src/masking_tool/text_replacer.py`
- [X] T013 Ensure replacement-table loading keeps raw `検出語句` and `置換提案` values unchanged in `src/masking_tool/replacement_table.py`

**Checkpoint**: Shared Unicode width fixtures and matching semantics are ready for story-specific implementation.

---

## Phase 3: User Story 1 - Full-width Excel phrase masks half-width document text (Priority: P1) MVP

**Goal**: A replacement table row with full-width ASCII-compatible `検出語句` masks half-width visible target text across supported in-scope formats.

**Independent Test**: Process fixtures where `検出語句` is `Ｔｅｃｈｎｏｌｏｇｉｅｓ， Ｉｎｃ．` and target text is `Technologies, Inc.`, then confirm the output contains the replacement proposal and no visible half-width target remains in in-scope text.

### Tests for User Story 1

- [X] T014 [P] [US1] Add contract assertions for full-width `検出語句` matching half-width targets in `tests/contract/test_unicode_normalization_contract.py`
- [X] T015 [US1] Add text format integration tests for `.txt`, `.csv`, and `.log` full-width-to-half-width matching in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T016 [US1] Add Office and workbook integration tests for `.docx`, `.xlsx`, and `.pptx` full-width-to-half-width matching in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T017 [US1] Add text-layer `.pdf` integration test for full-width-to-half-width matching in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T018 [P] [US1] Add no reversible mapping assertion for full-width-to-half-width outputs in `tests/integration/test_no_reversible_mapping.py`

### Implementation for User Story 1

- [X] T019 [US1] Route `.txt`, `.csv`, and `.log` replacement through width-equivalent matching in `src/masking_tool/text_replacer.py`
- [X] T020 [US1] Route `.docx` paragraph and table-cell visible text through width-equivalent matching in `src/masking_tool/office_replacer.py`
- [X] T021 [US1] Route `.xlsx` string cell replacement through width-equivalent matching in `src/masking_tool/office_replacer.py`
- [X] T022 [US1] Route `.pptx` text-box and table-cell visible text through width-equivalent matching in `src/masking_tool/office_replacer.py`
- [X] T023 [US1] Route text-layer `.pdf` replacement through width-equivalent span matching in `src/masking_tool/pdf_replacer.py`
- [X] T024 [US1] Preserve one visible replacement count per full-width-to-half-width match in `src/masking_tool/text_replacer.py`

**Checkpoint**: User Story 1 is independently functional and testable as the MVP.

---

## Phase 4: User Story 2 - Half-width Excel phrase masks full-width document text (Priority: P1)

**Goal**: A replacement table row with half-width ASCII `検出語句` masks full-width visible target text across supported in-scope formats.

**Independent Test**: Process fixtures where `検出語句` is `Technologies, Inc.` and target text is `Ｔｅｃｈｎｏｌｏｇｉｅｓ， Ｉｎｃ．`, then confirm the output contains the replacement proposal and no visible full-width target remains in in-scope text.

### Tests for User Story 2

- [X] T025 [P] [US2] Add contract assertions for half-width `検出語句` matching full-width targets in `tests/contract/test_unicode_normalization_contract.py`
- [X] T026 [US2] Add text format integration tests for `.txt`, `.csv`, and `.log` half-width-to-full-width matching in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T027 [US2] Add Office and workbook integration tests for `.docx`, `.xlsx`, and `.pptx` half-width-to-full-width matching in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T028 [US2] Add text-layer `.pdf` integration test for half-width-to-full-width matching in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T029 [US2] Add exact raw match precedence integration test for width-equivalent duplicate rows in `tests/integration/test_unicode_normalization_replacement.py`

### Implementation for User Story 2

- [X] T030 [US2] Ensure shared width-equivalent matching detects half-width `検出語句` against full-width visible spans in `src/masking_tool/text_replacer.py`
- [X] T031 [US2] Ensure Office split-run visible text uses raw target spans after half-width-to-full-width matching in `src/masking_tool/office_replacer.py`
- [X] T032 [US2] Ensure workbook cell values use exact replacement proposals after half-width-to-full-width matching in `src/masking_tool/office_replacer.py`
- [X] T033 [US2] Ensure PDF redaction and insertion use full-width source spans for half-width-to-full-width matches in `src/masking_tool/pdf_replacer.py`
- [X] T034 [US2] Ensure exact raw match precedence is applied before width-equivalent candidate selection in `src/masking_tool/text_replacer.py`

**Checkpoint**: User Stories 1 and 2 both work independently for bidirectional width-equivalent matching.

---

## Phase 5: User Story 3 - CJK text and replacement values remain intact (Priority: P2)

**Goal**: CJK text that is not explicitly matched remains unchanged, and `置換提案` values are written exactly as supplied while excluded content stays reportable.

**Independent Test**: Process mixed-language fixtures containing CJK text, width-equivalent ASCII-compatible phrases, exact replacement proposals, unsupported files, scanned PDFs, and Office embedded objects; verify only explicit matches change and existing safety reporting remains intact.

### Tests for User Story 3

- [X] T035 [P] [US3] Add CJK preservation contract assertions in `tests/contract/test_unicode_normalization_contract.py`
- [X] T036 [P] [US3] Add exact replacement proposal preservation assertions in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T037 [P] [US3] Add visually similar non-width-equivalent negative test in `tests/unit/test_text_replacer.py`
- [X] T038 [P] [US3] Add deterministic rerun coverage for Unicode width outputs and counts in `tests/integration/test_deterministic_rerun.py`
- [X] T039 [P] [US3] Add folder skip-report regression coverage with Unicode width fixtures and unsupported files in `tests/integration/test_folder_skip_report.py`
- [X] T040 [P] [US3] Add excluded PDF and Office safety regression coverage for Unicode width fixtures in `tests/integration/test_excluded_pdf_scope.py` and `tests/integration/test_excluded_office_scope.py`

### Implementation for User Story 3

- [X] T041 [US3] Prevent normalization of unrelated visible text and CJK-only text in `src/masking_tool/text_replacer.py`
- [X] T042 [US3] Preserve exact `置換提案` values for text, Office, workbook, and PDF outputs in `src/masking_tool/text_replacer.py`
- [X] T043 [US3] Preserve existing unsupported and excluded content reporting while processing Unicode width matches in `src/masking_tool/app.py`
- [X] T044 [US3] Preserve scanned PDF and embedded-object exclusion behavior while adding Unicode width matching in `src/masking_tool/pdf_replacer.py` and `src/masking_tool/office_replacer.py`

**Checkpoint**: Safety boundaries, CJK preservation, exact output value preservation, and deterministic behavior remain intact.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, fixture documentation, and cleanup across all stories.

- [X] T045 [P] Update Unicode normalization fixture documentation in `tests/fixtures/README.md`
- [X] T046 [P] Update quickstart validation results after implementation in `specs/005-unicode-normalization-matching/quickstart.md`
- [X] T047 Run `python -m pytest tests/contract/test_unicode_normalization_contract.py` and fix failures in affected `src/masking_tool/` and `tests/` files
- [X] T048 Run `python -m pytest tests/integration/test_unicode_normalization_replacement.py tests/unit/test_text_replacer.py` and fix failures in affected `src/masking_tool/` and `tests/` files
- [X] T049 Run `python -m pytest tests/integration/test_deterministic_rerun.py tests/integration/test_no_reversible_mapping.py tests/integration/test_folder_skip_report.py tests/integration/test_excluded_pdf_scope.py tests/integration/test_excluded_office_scope.py` and fix regressions in affected `src/masking_tool/` and `tests/` files
- [X] T050 Run `python -m pytest tests/contract/test_ui_single_file_contract.py tests/contract/test_ui_folder_contract.py` and confirm file/folder screen selection contracts remain valid
- [X] T051 Run full `python -m pytest` and fix regressions in affected `src/masking_tool/` and `tests/` files
- [X] T052 Run `git diff --check` and resolve formatting issues in `specs/005-unicode-normalization-matching/tasks.md`, affected `src/masking_tool/`, and affected `tests/` files

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP
- **User Story 2 (Phase 4)**: Depends on Foundational and can proceed alongside US1 after shared matching behavior exists
- **User Story 3 (Phase 5)**: Depends on enough US1/US2 behavior to validate preservation and safety outcomes
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational; delivers full-width replacement-table values matching half-width document text
- **US2 (P1)**: Can start after Foundational; delivers half-width replacement-table values matching full-width document text
- **US3 (P2)**: Starts after width-equivalent behavior exists; final validation depends on US1 and US2

### Parallel Opportunities

- T003 and T004 can run in parallel after T001.
- T009 and T010 can be authored in parallel because they cover separate unit expectations.
- T014 and T018 can be authored in parallel with the sequential integration tests because they touch different files.
- T025 can be authored in parallel with the sequential integration tests because it touches a different file.
- T035 through T040 can be authored in parallel because they touch distinct safety and regression checks.
- T045 and T046 can run in parallel after implementation is stable.

---

## Parallel Example: User Story 1

```text
Task: "T014 [P] [US1] Add contract assertions for full-width `検出語句` matching half-width targets in tests/contract/test_unicode_normalization_contract.py"
Task: "T015 [US1] Add text format integration tests for `.txt`, `.csv`, and `.log` full-width-to-half-width matching in tests/integration/test_unicode_normalization_replacement.py"
Task: "T018 [P] [US1] Add no reversible mapping assertion for full-width-to-half-width outputs in tests/integration/test_no_reversible_mapping.py"
```

## Parallel Example: User Story 2

```text
Task: "T025 [P] [US2] Add contract assertions for half-width `検出語句` matching full-width targets in tests/contract/test_unicode_normalization_contract.py"
Task: "T026 [US2] Add text format integration tests for `.txt`, `.csv`, and `.log` half-width-to-full-width matching in tests/integration/test_unicode_normalization_replacement.py"
Task: "T029 [US2] Add exact raw match precedence integration test for width-equivalent duplicate rows in tests/integration/test_unicode_normalization_replacement.py"
```

## Parallel Example: User Story 3

```text
Task: "T035 [P] [US3] Add CJK preservation contract assertions in tests/contract/test_unicode_normalization_contract.py"
Task: "T038 [P] [US3] Add deterministic rerun coverage for Unicode width outputs and counts in tests/integration/test_deterministic_rerun.py"
Task: "T040 [P] [US3] Add excluded PDF and Office safety regression coverage for Unicode width fixtures in tests/integration/test_excluded_pdf_scope.py and tests/integration/test_excluded_office_scope.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational shared fixture and matching tasks
3. Complete Phase 3: User Story 1 full-width-to-half-width replacement
4. Stop and validate full-width replacement-table phrases mask half-width target text across supported in-scope formats

### Incremental Delivery

1. Setup + Foundational -> Unicode width fixtures and shared matching semantics ready
2. US1 -> full-width `検出語句` masks half-width target text MVP
3. US2 -> half-width `検出語句` masks full-width target text and exact raw match precedence
4. US3 -> CJK preservation, exact replacement proposal preservation, deterministic reruns, and excluded-content safety
5. Polish -> fixture docs, quickstart validation, focused tests, full suite, and formatting checks

### Validation Gates

1. Tests for each story are written before implementation and fail for the current raw-string-only behavior.
2. Each story reaches its checkpoint before moving to the next priority.
3. Full pytest and `git diff --check` pass before the feature is considered complete.
