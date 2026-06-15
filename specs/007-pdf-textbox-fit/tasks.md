# Tasks: PDF Textbox Fit Preservation

**Input**: Design documents from `/specs/007-pdf-textbox-fit/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/pdf-textbox-fit-contract.md, quickstart.md

**Tests**: Required. This feature changes PDF replacement layout, visible masking behavior, and skip-report warning behavior.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches a different file and has no dependency on another task in the same phase
- **[Story]**: User story traceability for story phases only
- Every task includes an exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the existing project structure and create the shared test skeletons for PDF page-fit work.

- [X] T001 Confirm existing PDF replacement dependencies in `pyproject.toml` include PyMuPDF, openpyxl, and pytest
- [X] T002 [P] Create the PDF textbox fit contract test skeleton in `tests/contract/test_pdf_textbox_fit_contract.py`
- [X] T003 [P] Create the focused PDF page-fit integration test skeleton in `tests/integration/test_pdf_textbox_fit.py`
- [X] T004 [P] Create generated text-layer PDF fixture helper skeletons in `tests/fixtures/create_pdf_textbox_fit_samples.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build repeatable PDF fixtures and shared PDF layout primitives that all user stories depend on.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T005 Add shared fixture constants for detected phrases, replacement proposals, page dimensions, and original font size in `tests/fixtures/create_pdf_textbox_fit_samples.py`
- [X] T006 Implement one-page constrained text-layer PDF fixture generation for original-font fit in `tests/fixtures/create_pdf_textbox_fit_samples.py`
- [X] T007 Implement longer-label text-layer PDF fixture generation that still fits at original font size in `tests/fixtures/create_pdf_textbox_fit_samples.py`
- [X] T008 Implement original-font overflow PDF fixture generation in `tests/fixtures/create_pdf_textbox_fit_samples.py`
- [X] T009 Implement mixed fit-safe plus warning-required PDF fixture generation in `tests/fixtures/create_pdf_textbox_fit_samples.py`
- [X] T010 [P] Add unit tests for PDF span metadata, original font size, and layout warning helper behavior in `tests/unit/test_pdf_replacer.py`
- [X] T011 Add internal PDF text-region and layout-attempt helper structures in `src/masking_tool/pdf_replacer.py`
- [X] T012 Add deterministic PDF layout-warning message helper functions in `src/masking_tool/pdf_replacer.py`
- [X] T013 [P] Verify existing result-message reporting accepts PDF layout warnings in `src/masking_tool/report.py`

**Checkpoint**: Fixture generation and shared PDF layout primitives are ready; user story implementation can begin.

---

## Phase 3: User Story 1 - Preserve one-page PDF layout after replacement (Priority: P1) MVP

**Goal**: Fit-safe text-layer PDF replacements remain readable at the original font size inside the original page region, and one-page inputs remain one-page outputs.

**Independent Test**: Process the one-page constrained PDF fixture and confirm the output remains one page, contains the replacement proposal, preserves original-font fit behavior, and omits the original detected phrase.

### Tests for User Story 1

- [X] T014 [US1] Add contract assertions for one-page original-font PDF fit behavior in `tests/contract/test_pdf_textbox_fit_contract.py`
- [X] T015 [US1] Add integration test for constrained one-page PDF replacement fit in `tests/integration/test_pdf_textbox_fit.py`
- [X] T016 [US1] Add integration test for longer replacement label that still fits at original font size in `tests/integration/test_pdf_textbox_fit.py`
- [X] T017 [US1] Add reusable PDF page count, extracted text, and font-size assertion helpers in `tests/integration/test_pdf_textbox_fit.py`

### Implementation for User Story 1

- [X] T018 [US1] Capture original PDF text span bounds and font size for replacement candidates in `src/masking_tool/pdf_replacer.py`
- [X] T019 [US1] Insert replacement text using the original font size when it fits inside the original PDF region in `src/masking_tool/pdf_replacer.py`
- [X] T020 [US1] Stop expanding PDF replacement rectangles beyond the original page region for fit-safe replacements in `src/masking_tool/pdf_replacer.py`
- [X] T021 [US1] Preserve replacement counts and original-phrase absence after original-font PDF replacement in `src/masking_tool/pdf_replacer.py`
- [X] T022 [US1] Complete unit coverage for fit-safe PDF layout helper behavior in `tests/unit/test_pdf_replacer.py`

**Checkpoint**: User Story 1 is functional and testable as the MVP.

---

## Phase 4: User Story 2 - Warn when PDF replacement cannot fit reliably (Priority: P2)

**Goal**: PDF regions that cannot fit at the original font size still remove matched sensitive text, apply the replacement, and record clear warnings without failing other fit-safe regions.

**Independent Test**: Process an intentionally too-small PDF text region and confirm the output omits the original phrase, includes the replacement, and records a layout warning in result messages and `skipped_unsupported.txt`.

### Tests for User Story 2

- [X] T023 [US2] Add contract assertions for original-font overflow warnings that still remove original phrases in `tests/contract/test_pdf_textbox_fit_contract.py`
- [X] T024 [US2] Add integration test for overflow PDF layout warning output in `tests/integration/test_pdf_textbox_fit.py`
- [X] T025 [US2] Add integration test for mixed fit-safe and warning-required PDF regions in `tests/integration/test_pdf_textbox_fit.py`
- [X] T026 [P] [US2] Add skip-report assertion for PDF layout warnings in `tests/integration/test_folder_skip_report.py`

### Implementation for User Story 2

- [X] T027 [US2] Detect replacement text that cannot fit at the original font size inside the original PDF region in `src/masking_tool/pdf_replacer.py`
- [X] T028 [US2] Still apply the replacement and remove the original detected phrase when a PDF layout warning is needed in `src/masking_tool/pdf_replacer.py`
- [X] T029 [US2] Append PDF layout warning messages with file, page, and region context in `src/masking_tool/pdf_replacer.py`
- [X] T030 [US2] Ensure PDF layout warning messages are written through existing skip-report generation in `src/masking_tool/report.py`
- [X] T031 [US2] Complete unit coverage for overflow and warning-region PDF layout helpers in `tests/unit/test_pdf_replacer.py`

**Checkpoint**: User Stories 1 and 2 work independently and together.

---

## Phase 5: User Story 3 - Preserve PDF masking safety boundaries (Priority: P3)

**Goal**: The page-fit fix does not weaken Japanese PDF replacement, text-layer-only scope, deterministic replacement, replacement-table semantics, or unsupported-content reporting.

**Independent Test**: Run existing PDF readable-text, scanned-PDF exclusion, deterministic rerun, replacement-table, no-reversible-mapping, and skip-report tests after page-fit fixtures pass.

### Tests for User Story 3

- [X] T032 [P] [US3] Add or update Japanese PDF replacement regression coverage in `tests/integration/test_single_pdf_file.py`
- [X] T033 [P] [US3] Add or update scanned-PDF exclusion regression coverage in `tests/integration/test_excluded_pdf_scope.py`
- [X] T034 [P] [US3] Add deterministic rerun assertions for PDF page-fit outputs and warnings in `tests/integration/test_deterministic_rerun.py`
- [X] T035 [P] [US3] Add replacement-table and no-reversible-mapping regression coverage for PDF page-fit replacements in `tests/integration/test_no_reversible_mapping.py`

### Implementation for User Story 3

- [X] T036 [US3] Verify `plan_replacements` matching semantics remain unchanged through `tests/unit/test_text_replacer.py`
- [X] T037 [US3] Preserve `ExcludedPdfError` and scanned-PDF exclusion behavior while adding PDF layout warnings in `src/masking_tool/pdf_replacer.py`
- [X] T038 [US3] Preserve existing file and folder orchestration behavior for PDF outputs and messages in `src/masking_tool/app.py`

**Checkpoint**: All user stories are independently functional and existing safety guarantees remain intact.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and release-readiness checks across the feature.

- [X] T039 [P] Document the generated PDF page-fit fixtures in `tests/fixtures/README.md`
- [X] T040 Update validation notes after implementation in `specs/007-pdf-textbox-fit/quickstart.md`
- [X] T041 Run PDF page-fit contract tests with `.venv\Scripts\python.exe -m pytest tests/contract/test_pdf_textbox_fit_contract.py`
- [X] T042 Run focused PDF page-fit integration tests with `.venv\Scripts\python.exe -m pytest tests/integration/test_pdf_textbox_fit.py`
- [X] T043 Run affected PDF and reporting regressions with `.venv\Scripts\python.exe -m pytest tests/integration/test_single_pdf_file.py tests/integration/test_excluded_pdf_scope.py tests/integration/test_deterministic_rerun.py tests/integration/test_folder_skip_report.py tests/integration/test_no_reversible_mapping.py tests/integration/test_batch_performance.py tests/unit/test_text_replacer.py`
- [X] T044 Run the full test suite with `.venv\Scripts\python.exe -m pytest`
- [X] T045 Run whitespace validation with `git diff --check`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; can start immediately
- **Phase 2 Foundational**: Depends on Phase 1; blocks all user stories
- **Phase 3 US1**: Depends on Phase 2; delivers the MVP page-fit fix
- **Phase 4 US2**: Depends on Phase 2 and integrates with US1 PDF layout helpers
- **Phase 5 US3**: Depends on Phase 2 and can run alongside US1/US2 regression work after PDF layout primitives exist
- **Phase 6 Polish**: Depends on the selected user stories being complete

### User Story Dependencies

- **US1 (P1)**: No dependency on other stories after Phase 2
- **US2 (P2)**: Can be tested independently with overflow PDF fixtures after Phase 2; implementation reuses US1 layout helpers when available
- **US3 (P3)**: Can be tested independently by running existing PDF and reporting regression suites after Phase 2

### Within Each User Story

- Write or update tests first and confirm they fail before implementation
- Implement `pdf_replacer.py` layout behavior before orchestration/report integration checks
- Complete each story checkpoint before relying on it for later validation

---

## Parallel Opportunities

- T002, T003, and T004 can run in parallel after T001 because they create different test helper files.
- T010 and T013 can run in parallel with fixture generation because they touch different files.
- T026 can run in parallel with T023-T025 because it updates a different integration test file.
- T032-T035 can run in parallel because each regression task touches a different test file.
- T039 can run in parallel with implementation cleanup because it only updates fixture documentation.

---

## Parallel Example: User Story 1

```powershell
# Contract and integration tests can be prepared by separate workers:
Task: "T014 [US1] Add contract assertions for one-page original-font PDF fit behavior in tests/contract/test_pdf_textbox_fit_contract.py"
Task: "T015 [US1] Add integration test for constrained one-page PDF replacement fit in tests/integration/test_pdf_textbox_fit.py"

# Implementation should then proceed in order in pdf_replacer.py:
Task: "T018 [US1] Capture original PDF text span bounds and font size for replacement candidates in src/masking_tool/pdf_replacer.py"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1 setup.
2. Complete Phase 2 foundational fixtures and PDF layout helpers.
3. Complete Phase 3 User Story 1.
4. Validate with the contract and focused integration tests for one-page original-font fit.

### Incremental Delivery

1. Deliver US1 to prevent fit-safe text-layer PDF replacements from enlarging or breaking one-page layout.
2. Add US2 so original-font overflow cases still remove sensitive text and produce clear review warnings.
3. Add US3 regression protection to confirm Japanese PDF, scanned-PDF exclusion, deterministic, replacement-table, and skip-report behavior remain unchanged.
4. Run the quickstart validation commands and `git diff --check`.

### Validation Gates

- Contract tests pass for original-font fit and warning cases.
- Focused PDF page-fit integration tests pass.
- Existing Japanese PDF, scanned-PDF exclusion, deterministic, replacement-table, no-reversible-mapping, and skip-report regressions pass.
- Full pytest and `git diff --check` pass before commit.
