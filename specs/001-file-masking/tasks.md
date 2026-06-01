# Tasks: 機密文字列ファイルマスキング

**Input**: Design documents from `/specs/001-file-masking/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/ui-contract.md, quickstart.md

**Tests**: Required for replacement behavior, file-format handling, folder processing, excluded scope, and skip-report generation.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently after foundational tasks are complete.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files and has no dependency on incomplete tasks
- **[Story]**: Which user story this task belongs to, used only in user story phases
- Each task includes exact file paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize a Python project layout matching the implementation plan.

- [X] T001 Create Python project metadata with dependencies in pyproject.toml
- [X] T002 Create package directories and empty module files under src/masking_tool/
- [X] T003 Create test directories under tests/unit/, tests/integration/, tests/contract/, and tests/fixtures/
- [X] T004 [P] Add pytest configuration and test path settings in pyproject.toml
- [X] T005 [P] Add application entry points in src/main.py and src/masking_tool/__main__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models, fixture generation, validation, scanning, and reporting required by all user stories.

**Critical**: No user story work can begin until this phase is complete.

- [X] T006 [P] Define dataclasses and enums for ReplacementRule, ReplacementTable, InputSelection, InputTarget, ProcessingResult, SkipReportEntry in src/masking_tool/models.py
- [X] T007 [P] Create fixture-generation helpers for replacement tables, text files, Office files, PDFs, scanned-like PDFs, and unsupported samples in tests/fixtures/create_fixtures.py
- [X] T008 [P] Create unit tests for replacement-table header validation and invalid rows in tests/unit/test_replacement_table.py
- [X] T009 Implement replacement-table loading, validation, duplicate detection, and deterministic rule ordering in src/masking_tool/replacement_table.py
- [X] T010 [P] Create unit tests for supported extension detection, direct-child scanning, recursive scanning, and relative paths in tests/unit/test_scanner.py
- [X] T011 Implement input target discovery and traversal mode handling in src/masking_tool/scanner.py
- [X] T012 [P] Create unit tests for skip report formatting, sorting, and empty report creation in tests/unit/test_report.py
- [X] T013 Implement UTF-8 skip report writing and summary count aggregation in src/masking_tool/report.py
- [X] T014 [P] Create unit tests for deterministic phrase replacement with overlapping phrases in tests/unit/test_text_replacer.py
- [X] T015 Implement shared deterministic text replacement helper in src/masking_tool/text_replacer.py
- [X] T016 Create orchestration skeleton for validating inputs and dispatching per-file processing in src/masking_tool/app.py

**Checkpoint**: Replacement rules, target discovery, deterministic text replacement, and skip-report generation are ready for story implementation.

---

## Phase 3: User Story 1 - 単一ファイルをマスキングする (Priority: P1) MVP

**Goal**: User selects a replacement table and one supported file, then receives a replaced output file without altering the original.

**Independent Test**: Process each supported fixture as a single file and verify detected phrases are absent, replacement proposals appear, and no-match files complete without false failure.

### Tests for User Story 1

- [X] T017 [P] [US1] Create `.txt`, `.csv`, `.log`, and no-match fixture tests in tests/integration/test_single_text_files.py
- [X] T018 [P] [US1] Create `.docx`, `.xlsx`, and `.pptx` fixture tests in tests/integration/test_single_office_files.py
- [X] T019 [P] [US1] Create text-based `.pdf` fixture test in tests/integration/test_single_pdf_file.py
- [X] T020 [P] [US1] Create UI contract test for single-file required controls and validation messages in tests/contract/test_ui_single_file_contract.py

### Implementation for User Story 1

- [X] T021 [P] [US1] Implement `.txt`, `.csv`, and `.log` file replacement in src/masking_tool/text_replacer.py
- [X] T022 [P] [US1] Implement `.docx` replacement preserving paragraphs and tables in src/masking_tool/office_replacer.py
- [X] T023 [P] [US1] Implement `.xlsx` replacement preserving workbook sheets and cell values in src/masking_tool/office_replacer.py
- [X] T024 [P] [US1] Implement `.pptx` replacement preserving slide text frames and table cells in src/masking_tool/office_replacer.py
- [X] T025 [P] [US1] Implement text-layer `.pdf` replacement and output creation in src/masking_tool/pdf_replacer.py
- [X] T026 [US1] Wire single-file processing dispatch and output path creation in src/masking_tool/app.py
- [X] T027 [US1] Implement Tkinter single-file flow with replacement table picker, input picker, output folder picker, validation messages, and start button in src/masking_tool/ui.py
- [X] T028 [US1] Add single-file command entry behavior that launches the UI in src/masking_tool/__main__.py

**Checkpoint**: User Story 1 is independently functional and testable as the MVP.

---

## Phase 4: User Story 2 - フォルダ内の対象ファイルを一括マスキングする (Priority: P2)

**Goal**: User selects a folder, chooses direct-child-only or recursive traversal, and batch-processes all supported targets while unsupported or failed files are reported.

**Independent Test**: Process a mixed folder containing supported files, unsupported files, nested files, and no-match files; verify traversal behavior, outputs, and `skipped_unsupported.txt`.

### Tests for User Story 2

- [X] T029 [P] [US2] Create mixed direct-child folder integration test in tests/integration/test_folder_direct_children.py
- [X] T030 [P] [US2] Create recursive folder integration test with nested relative-path outputs in tests/integration/test_folder_recursive.py
- [X] T031 [P] [US2] Create unsupported extension and failed-file report integration test in tests/integration/test_folder_skip_report.py
- [X] T032 [P] [US2] Create UI contract test for folder mode, traversal selector, progress, and completion counts in tests/contract/test_ui_folder_contract.py

### Implementation for User Story 2

- [X] T033 [US2] Extend app orchestration for folder processing, per-file continuation after failures, and summary counts in src/masking_tool/app.py
- [X] T034 [US2] Preserve input-relative subfolder paths for recursive output files in src/masking_tool/app.py
- [X] T035 [US2] Record unsupported extensions and processing failures through SkipReportEntry in src/masking_tool/report.py
- [X] T036 [US2] Implement Tkinter folder mode, traversal selector, progress updates, and completion summary in src/masking_tool/ui.py
- [X] T037 [US2] Add cancellation-safe batch processing state and user-visible cancelled summary in src/masking_tool/app.py

**Checkpoint**: User Stories 1 and 2 both work independently with shared foundations.

---

## Phase 5: User Story 3 - 第一版の対象外範囲を確認できる (Priority: P3)

**Goal**: User can distinguish first-version excluded content such as scanned PDFs, image text, embedded objects, and OCR-dependent content from successfully masked files.

**Independent Test**: Process excluded samples and verify they are not reported as successfully masked and are recorded with clear reasons.

### Tests for User Story 3

- [X] T038 [P] [US3] Create scanned or image-text-only PDF skip test in tests/integration/test_excluded_pdf_scope.py
- [X] T039 [P] [US3] Create Office embedded-object warning or skip-report test in tests/integration/test_excluded_office_scope.py
- [X] T040 [P] [US3] Create UI contract test for excluded-content completion summary in tests/contract/test_ui_excluded_scope_contract.py

### Implementation for User Story 3

- [X] T041 [US3] Add PDF text-layer detection and excluded-content reason mapping in src/masking_tool/pdf_replacer.py
- [X] T042 [US3] Add Office embedded-object detection notes without treating embedded content as masked in src/masking_tool/office_replacer.py
- [X] T043 [US3] Route excluded-content outcomes to `skipped_unsupported.txt` with status `skipped_unsupported` in src/masking_tool/app.py
- [X] T044 [US3] Display excluded-content counts and report location in src/masking_tool/ui.py

**Checkpoint**: All first-version exclusions are visible in processing results and not confused with successful masking.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, performance, packaging readiness, and final verification across stories.

- [X] T045 [P] Update quickstart usage notes with actual run and test commands in specs/001-file-masking/quickstart.md
- [X] T046 [P] Add README project overview and basic usage in README.md
- [X] T047 [P] Add end-to-end fixture generation documentation in tests/fixtures/README.md
- [X] T048 Add performance regression test for 100 mixed small documents in tests/integration/test_batch_performance.py
- [X] T049 Add deterministic rerun integration test comparing output content and skip-report entries in tests/integration/test_deterministic_rerun.py
- [X] T050 Add security/privacy regression test ensuring original detected phrases are not written to skip reports or summaries in tests/integration/test_no_reversible_mapping.py
- [X] T051 Run full pytest suite and fix failures in affected src/masking_tool/ and tests/ files
- [X] T052 Validate manual UI flow from quickstart and document any remaining limitations in README.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational and is the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational; can reuse US1 format handlers and app dispatch.
- **User Story 3 (Phase 5)**: Depends on Foundational; can proceed after PDF/Office handlers from US1 exist.
- **Polish (Phase 6)**: Depends on desired user stories being complete.

### User Story Dependencies

- **US1**: Required for MVP and establishes single-file format handlers.
- **US2**: Builds on scanning/reporting foundations and reuses US1 handlers for batch processing.
- **US3**: Builds on US1 PDF/Office handlers and shared reporting to expose excluded scope.

### Within Each User Story

- Tests are written before implementation.
- Format handlers are implemented before app orchestration is considered complete.
- UI work follows app orchestration so controls map to real processing inputs.
- A story is complete only when its independent tests pass.

---

## Parallel Opportunities

- Setup tasks T004 and T005 can run in parallel after T001.
- Foundational model, fixture, scanner-test, report-test, and text-helper-test tasks T006, T007, T008, T010, T012, and T014 can run in parallel.
- US1 test tasks T017 through T020 can run in parallel.
- US1 format handlers T021 through T025 can run in parallel after foundational helpers exist.
- US2 test tasks T029 through T032 can run in parallel.
- US3 test tasks T038 through T040 can run in parallel.
- Polish documentation tasks T045 through T047 can run in parallel.

## Parallel Example: User Story 1

```text
Task: T017 Create text fixture tests in tests/integration/test_single_text_files.py
Task: T018 Create Office fixture tests in tests/integration/test_single_office_files.py
Task: T019 Create PDF fixture test in tests/integration/test_single_pdf_file.py
Task: T020 Create UI contract test in tests/contract/test_ui_single_file_contract.py
```

```text
Task: T021 Implement text file replacement in src/masking_tool/text_replacer.py
Task: T022 Implement docx replacement in src/masking_tool/office_replacer.py
Task: T023 Implement xlsx replacement in src/masking_tool/office_replacer.py
Task: T024 Implement pptx replacement in src/masking_tool/office_replacer.py
Task: T025 Implement PDF replacement in src/masking_tool/pdf_replacer.py
```

## Parallel Example: User Story 2

```text
Task: T029 Create direct-child folder integration test in tests/integration/test_folder_direct_children.py
Task: T030 Create recursive folder integration test in tests/integration/test_folder_recursive.py
Task: T031 Create skip-report integration test in tests/integration/test_folder_skip_report.py
Task: T032 Create UI folder contract test in tests/contract/test_ui_folder_contract.py
```

## Parallel Example: User Story 3

```text
Task: T038 Create excluded PDF scope test in tests/integration/test_excluded_pdf_scope.py
Task: T039 Create excluded Office scope test in tests/integration/test_excluded_office_scope.py
Task: T040 Create excluded-content UI contract test in tests/contract/test_ui_excluded_scope_contract.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2.
2. Write and run US1 tests.
3. Implement single-file processing for all supported extensions.
4. Validate replacement-table errors, no-match files, and original-file preservation.
5. Demo single-file masking through the UI.

### Incremental Delivery

1. Deliver US1 as the smallest useful masking flow.
2. Add US2 folder batch traversal, skip reporting, and progress summary.
3. Add US3 excluded-scope reporting for scanned PDFs, image text, embedded objects, and OCR-dependent content.
4. Finish polish tasks and run the quickstart end-to-end.

### Validation Gates

- All supported extension fixtures must pass replacement assertions.
- `skipped_unsupported.txt` must be created for every run.
- Unsupported and excluded files must never be counted as successfully masked.
- Originals must remain unchanged across all stories.
