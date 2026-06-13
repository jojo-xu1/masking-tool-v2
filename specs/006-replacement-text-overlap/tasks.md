# Tasks: Replacement Text Overlap Prevention

**Input**: Design documents from `/specs/006-replacement-text-overlap/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/replacement-layout-contract.md, quickstart.md

**Tests**: Required. This feature changes Office replacement layout, visible masking behavior, and skip-report warning behavior.

**Organization**: Tasks are grouped by user story so each story can be implemented and tested independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches a different file and has no dependency on another task in the same phase
- **[Story]**: User story traceability for story phases only
- Every task includes an exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm the existing project structure and create the shared test skeletons for layout replacement work.

- [X] T001 Confirm existing Office replacement dependencies in `pyproject.toml` include `python-pptx`, `python-docx`, `openpyxl`, PyMuPDF, and pytest
- [X] T002 [P] Create the replacement layout contract test skeleton in `tests/contract/test_replacement_layout_contract.py`
- [X] T003 [P] Create the focused visual-layout integration test skeleton in `tests/integration/test_replacement_text_overlap.py`
- [X] T004 [P] Create generated `.pptx` layout fixture helper skeletons in `tests/fixtures/create_replacement_layout_samples.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build repeatable fixtures and shared layout primitives that all user stories depend on.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T005 Add shared fixture constants for detected phrases and replacement proposals in `tests/fixtures/create_replacement_layout_samples.py`
- [X] T006 Implement screenshot-style `.pptx` diagram fixture generation with close labels in `tests/fixtures/create_replacement_layout_samples.py`
- [X] T007 Implement `.pptx` text-box and table-cell fixture generation with constrained visual regions in `tests/fixtures/create_replacement_layout_samples.py`
- [X] T008 Implement unreadable overflow and mixed readable-plus-warning fixture generation in `tests/fixtures/create_replacement_layout_samples.py`
- [X] T009 [P] Add unit tests for PPTX visual region readability and layout warning helpers in `tests/unit/test_office_replacer.py`
- [X] T010 Add internal visual-region and layout-result helper structures in `src/masking_tool/office_replacer.py`
- [X] T011 Add deterministic region-reference and layout-warning message helper functions in `src/masking_tool/office_replacer.py`
- [X] T012 [P] Verify existing result-message reporting accepts layout warnings in `src/masking_tool/report.py`

**Checkpoint**: Fixture generation and shared layout primitives are ready; user story implementation can begin.

---

## Phase 3: User Story 1 - Readable replacements in diagram-like layouts (Priority: P1) MVP

**Goal**: Replacement labels in supported `.pptx` visual regions remain readable and do not overlap each other or nearby labels.

**Independent Test**: Process the screenshot-style diagram fixture and confirm the output contains all replacement proposals, contains no matched original phrases, and has distinct readable label regions.

### Tests for User Story 1

- [X] T013 [US1] Add contract assertions for screenshot-style non-overlapping replacement labels in `tests/contract/test_replacement_layout_contract.py`
- [X] T014 [US1] Add integration test for screenshot-style `.pptx` diagram replacement readability in `tests/integration/test_replacement_text_overlap.py`
- [X] T015 [US1] Add integration test for `.pptx` text-box and table-cell replacement readability in `tests/integration/test_replacement_text_overlap.py`

### Implementation for User Story 1

- [X] T016 [US1] Route `.pptx` shape text frames, text boxes, and table-cell text frames through layout-aware replacement in `src/masking_tool/office_replacer.py`
- [X] T017 [US1] Preserve the original visual region while applying readable in-region replacement layout in `src/masking_tool/office_replacer.py`
- [X] T018 [US1] Detect and prevent replacement-label overlap inside the same visual text region in `src/masking_tool/office_replacer.py`
- [X] T019 [US1] Preserve replacement counts and original-phrase absence after layout-aware replacement in `src/masking_tool/office_replacer.py`
- [X] T020 [US1] Complete unit coverage for successful visual-region layout helpers in `tests/unit/test_office_replacer.py`

**Checkpoint**: User Story 1 is functional and testable as the MVP.

---

## Phase 4: User Story 2 - Clear warning when readable layout cannot be guaranteed (Priority: P2)

**Goal**: Visual regions that cannot fit readable replacement labels record clear warnings without failing other readable regions.

**Independent Test**: Process an intentionally too-small visual region and confirm the result messages and `skipped_unsupported.txt` identify the affected file or region while readable regions remain successful.

### Tests for User Story 2

- [X] T021 [US2] Add contract assertions for overflow layout warnings in `tests/contract/test_replacement_layout_contract.py`
- [X] T022 [US2] Add integration test for unreadable overflow warning output in `tests/integration/test_replacement_text_overlap.py`
- [X] T023 [US2] Add integration test for mixed readable and warning regions in one `.pptx` in `tests/integration/test_replacement_text_overlap.py`
- [X] T024 [P] [US2] Add skip-report assertion for layout warnings in `tests/integration/test_folder_skip_report.py`

### Implementation for User Story 2

- [X] T025 [US2] Detect unreadable or overflowing replacement layout attempts in `src/masking_tool/office_replacer.py`
- [X] T026 [US2] Append layout warning messages with file, slide, and region context in `src/masking_tool/office_replacer.py`
- [X] T027 [US2] Keep readable regions successful when another region in the same file warns in `src/masking_tool/office_replacer.py`
- [X] T028 [US2] Ensure layout warning messages are written through existing skip-report generation in `src/masking_tool/report.py`
- [X] T029 [US2] Complete unit coverage for warning-region layout helpers in `tests/unit/test_office_replacer.py`

**Checkpoint**: User Stories 1 and 2 work independently and together.

---

## Phase 5: User Story 3 - Preserve existing masking safety boundaries (Priority: P3)

**Goal**: The layout fix does not weaken deterministic replacement, Unicode matching, split-run Office behavior, unsupported reporting, or excluded-content boundaries.

**Independent Test**: Run existing Unicode, split-run Office, deterministic rerun, folder skip-report, and excluded-scope tests after layout fixtures pass.

### Tests for User Story 3

- [X] T030 [P] [US3] Add or update Unicode/CJK replacement layout regression coverage in `tests/integration/test_unicode_normalization_replacement.py`
- [X] T031 [P] [US3] Add or update split-run Office replacement regression coverage in `tests/integration/test_office_split_run_replacement.py`
- [X] T032 [P] [US3] Add deterministic rerun assertions for layout outputs and warnings in `tests/integration/test_deterministic_rerun.py`
- [X] T033 [P] [US3] Add excluded content safety assertions for layout-adjacent Office content in `tests/integration/test_excluded_office_scope.py`

### Implementation for User Story 3

- [X] T034 [US3] Keep `plan_replacements` matching semantics unchanged in `src/masking_tool/text_replacer.py`
- [X] T035 [US3] Preserve embedded-object and unsupported-content notes while adding layout warnings in `src/masking_tool/office_replacer.py`
- [X] T036 [US3] Preserve existing file and folder orchestration behavior for processed outputs and messages in `src/masking_tool/app.py`

**Checkpoint**: All user stories are independently functional and existing safety guarantees remain intact.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, validation, and release-readiness checks across the feature.

- [X] T037 [P] Document the generated layout fixtures in `tests/fixtures/README.md`
- [X] T038 Update validation notes after implementation in `specs/006-replacement-text-overlap/quickstart.md`
- [X] T039 Run layout contract tests with `.venv\Scripts\python.exe -m pytest tests/contract/test_replacement_layout_contract.py`
- [X] T040 Run focused visual-layout integration tests with `.venv\Scripts\python.exe -m pytest tests/integration/test_replacement_text_overlap.py`
- [X] T041 Run affected regression tests with `.venv\Scripts\python.exe -m pytest tests/integration/test_office_split_run_replacement.py tests/integration/test_unicode_normalization_replacement.py tests/integration/test_deterministic_rerun.py tests/integration/test_folder_skip_report.py tests/integration/test_excluded_office_scope.py`
- [X] T042 Run the full test suite with `.venv\Scripts\python.exe -m pytest`
- [X] T043 Run whitespace validation with `git diff --check`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 Setup**: No dependencies; can start immediately
- **Phase 2 Foundational**: Depends on Phase 1; blocks all user stories
- **Phase 3 US1**: Depends on Phase 2; delivers the MVP overlap fix
- **Phase 4 US2**: Depends on Phase 2 and integrates with US1 warning-safe layout helpers
- **Phase 5 US3**: Depends on Phase 2 and can run alongside US1/US2 regression work after layout primitives exist
- **Phase 6 Polish**: Depends on the selected user stories being complete

### User Story Dependencies

- **US1 (P1)**: No dependency on other stories after Phase 2
- **US2 (P2)**: Can be tested independently with overflow fixtures after Phase 2; implementation reuses US1 layout helpers when available
- **US3 (P3)**: Can be tested independently by running existing regression suites after Phase 2

### Within Each User Story

- Write or update tests first and confirm they fail before implementation
- Implement `office_replacer.py` layout behavior before orchestration/report integration checks
- Complete each story checkpoint before relying on it for later validation

---

## Parallel Opportunities

- T002, T003, and T004 can run in parallel after T001 because they create different test helper files.
- T009 and T012 can run in parallel with fixture generation because they touch different files.
- T024 can run in parallel with T021-T023 because it updates a different integration test file.
- T030-T033 can run in parallel because each regression task touches a different test file.
- T037 can run in parallel with implementation cleanup because it only updates fixture documentation.

---

## Parallel Example: User Story 1

```powershell
# Contract and integration tests can be prepared by separate workers:
Task: "T013 [US1] Add contract assertions for screenshot-style non-overlapping replacement labels in tests/contract/test_replacement_layout_contract.py"
Task: "T014 [US1] Add integration test for screenshot-style .pptx diagram replacement readability in tests/integration/test_replacement_text_overlap.py"

# Implementation should then proceed in order in office_replacer.py:
Task: "T016 [US1] Route .pptx shape text frames, text boxes, and table-cell text frames through layout-aware replacement in src/masking_tool/office_replacer.py"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1 setup.
2. Complete Phase 2 foundational fixtures and layout helpers.
3. Complete Phase 3 User Story 1.
4. Validate with the contract and focused integration tests for the screenshot-style layout.

### Incremental Delivery

1. Deliver US1 to eliminate the reported overlap defect for readable `.pptx` regions.
2. Add US2 so unreadable layouts produce clear review warnings instead of silent overlap.
3. Add US3 regression protection to confirm Unicode, split-run Office, deterministic, and excluded-content behavior remain unchanged.
4. Run the quickstart validation commands and `git diff --check`.

### Validation Gates

- Contract tests pass for readable and warning layout cases.
- Focused `.pptx` visual-layout integration tests pass.
- Existing Unicode, split-run Office, deterministic, skip-report, and excluded-content regressions pass.
- Full pytest and `git diff --check` pass before commit.
