# Tasks: UI改善とexe配布

**Input**: Design documents from `/specs/002-ui-exe-packaging/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: REQUIRED. This feature changes the desktop workflow and packaging path, and the specification requires UI contract tests, packaging contract tests, packaged smoke behavior, per-format regression verification, timing records, and existing masking regression tests.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare build dependencies, generated-output rules, and packaging folders.

- [x] T001 Add a `build` optional dependency group with `pyinstaller` in pyproject.toml
- [x] T002 Add package metadata for the executable name and app title in pyproject.toml
- [x] T003 [P] Update generated artifact ignore rules for `dist/`, `build/`, and local PyInstaller cache output in .gitignore
- [x] T004 [P] Create packaging workspace files `packaging/README.md`, `packaging/build_exe.ps1`, `packaging/MaskingTool.spec`, and `packaging/distribution-checklist.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared UI and packaging contracts before story work begins.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T005 [P] Define app/package constants for `MaskingTool.exe`, app title, expected dist path, smoke verification mode, and entry point in src/masking_tool/packaging.py
- [x] T006 Normalize development entry points so `python -m masking_tool` and `python src/main.py` launch the same UI in src/masking_tool/__main__.py and src/main.py
- [x] T007 Add stable UI state and summary keys for paths, mode, traversal, progress, counts, status, and report path in src/masking_tool/ui.py
- [x] T008 [P] Add distribution verification helper fields for per-format checks, timing values, and notes in src/masking_tool/packaging.py

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - 迷わず操作できるUIでマスキングを実行する (Priority: P1) - MVP

**Goal**: Users can identify inputs, choose processing options, run masking, and see progress/results from a calm work-oriented UI.

**Independent Test**: Launch the development UI, select a replacement table, input target, and output folder, then confirm validation, progress, completion counts, timing checklist fields, and `skipped_unsupported.txt` location are visible.

### Tests for User Story 1

- [x] T009 [P] [US1] Add UI layout contract tests for required grouped sections and stable state keys in tests/contract/test_ui_layout_contract.py
- [x] T010 [P] [US1] Add UI validation contract tests for missing replacement table, input path, and output folder messages in tests/contract/test_ui_layout_contract.py
- [x] T011 [P] [US1] Add UI completion summary contract tests for replaced, no-match, skipped, failed, and report path values in tests/contract/test_ui_layout_contract.py
- [x] T012 [P] [US1] Add Japanese/space/symbol path handling coverage for UI-selected paths in tests/contract/test_ui_layout_contract.py
- [x] T013 [P] [US1] Add UI usability contract checks for `900x620` minimum size and timing checklist field names in tests/contract/test_ui_layout_contract.py

### Implementation for User Story 1

- [x] T014 [US1] Rebuild the main window into header, input, execution, and results sections in src/masking_tool/ui.py
- [x] T015 [US1] Add work-oriented ttk styling, spacing, stable minimum size `900x620`, and non-overlapping responsive grid behavior in src/masking_tool/ui.py
- [x] T016 [US1] Implement required input validation and user-visible status messages before processing in src/masking_tool/ui.py
- [x] T017 [US1] Add progress updates for single-file and folder processing without hiding the current status line in src/masking_tool/ui.py
- [x] T018 [US1] Render completion counts and `skipped_unsupported.txt` report path after every run in src/masking_tool/ui.py

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Pythonを意識せずexeから起動する (Priority: P2)

**Goal**: Users can launch the tool from a single Windows executable named `MaskingTool.exe` without typing Python commands.

**Independent Test**: Build `dist/MaskingTool.exe`, launch it from outside the repository root, and confirm the UI opens and can process a sample file.

### Tests for User Story 2

- [x] T019 [P] [US2] Add packaging contract tests for exe name, one-file mode, output path, and entry point in tests/contract/test_packaging_contract.py
- [x] T020 [P] [US2] Add packaging script contract tests for cleaning stale output and failing when `dist/MaskingTool.exe` is missing after build in tests/contract/test_packaging_contract.py
- [x] T021 [P] [US2] Add normal smoke-mode test that skips packaged checks when `dist/MaskingTool.exe` is absent in tests/integration/test_packaged_app_smoke.py
- [x] T022 [P] [US2] Add distribution verification smoke-mode test that fails when `dist/MaskingTool.exe` is absent in tests/integration/test_packaged_app_smoke.py
- [x] T023 [P] [US2] Add packaged launch readiness test for an existing `dist/MaskingTool.exe` in tests/integration/test_packaged_app_smoke.py

### Implementation for User Story 2

- [x] T024 [US2] Implement the PyInstaller one-file spec for the UI entry point and bundled runtime needs in packaging/MaskingTool.spec
- [x] T025 [US2] Implement `packaging/build_exe.ps1` to run from repository root, clean stale exe output, build one-file mode, and verify `dist/MaskingTool.exe`
- [x] T026 [US2] Implement normal and distribution verification smoke-mode helpers in src/masking_tool/packaging.py
- [x] T027 [US2] Ensure packaged execution resolves resources and output paths correctly when launched outside the repository root in src/masking_tool/packaging.py
- [x] T028 [US2] Update build instructions for `python -m pip install -e .[test,build]`, `packaging/build_exe.ps1`, and `dist/MaskingTool.exe` in README.md and packaging/README.md

**Checkpoint**: User Story 2 is functional and testable independently after the MVP UI.

---

## Phase 5: User Story 3 - 配布前にUIとexeを検証する (Priority: P3)

**Goal**: Developers can complete a repeatable distribution verification covering launch, per-format regression checks, sample processing, unsupported skip reporting, readable Japanese PDF replacement, timing records, and missing-exe behavior.

**Independent Test**: Follow the distribution verification procedure against the built exe and confirm every required pass/fail and timing field is recorded.

### Tests for User Story 3

- [x] T029 [P] [US3] Add verification checklist contract tests for launch, single-file, folder, skip-report, PDF Japanese, and timing fields in tests/contract/test_packaging_contract.py
- [x] T030 [P] [US3] Add per-format regression gate contract tests for replacement-table loading, file type detection, `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, text-layer `.pdf`, unsupported extensions, and no-match inputs in tests/contract/test_packaging_contract.py
- [x] T031 [P] [US3] Add packaged manual sample smoke coverage for `tests/fixtures/inputs/manual_sensitive_samples/` in tests/integration/test_packaged_app_smoke.py
- [x] T032 [P] [US3] Add distribution verification mode coverage for missing `dist/MaskingTool.exe` failure in tests/integration/test_packaged_app_smoke.py

### Implementation for User Story 3

- [x] T033 [US3] Create a distribution verification checklist template with pass/fail fields, timing fields, verification mode, and notes in packaging/distribution-checklist.md
- [x] T034 [US3] Document replacement-table loading and file type detection verification in packaging/distribution-checklist.md
- [x] T035 [US3] Document per-format verification for `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, text-layer `.pdf`, unsupported extensions, and no-match inputs in packaging/distribution-checklist.md
- [x] T036 [US3] Document manual sensitive sample verification using `tests/fixtures/replacement_tables/機密情報検出結果_manual_sensitive.xlsx` in packaging/distribution-checklist.md
- [x] T037 [US3] Document PDF Japanese readability verification and `skipped_unsupported.txt` verification for the packaged exe in packaging/distribution-checklist.md
- [x] T038 [US3] Link the distribution checklist and verification-mode instructions from README.md and specs/002-ui-exe-packaging/quickstart.md

**Checkpoint**: All user stories are independently functional and ready for release validation.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final regression checks, documentation alignment, and cleanup.

- [x] T039 [P] Run and record `python -m pytest tests/unit/test_replacement_table.py tests/unit/test_scanner.py tests/unit/test_report.py` results in specs/002-ui-exe-packaging/quickstart.md
- [x] T040 [P] Run and record supported-extension regression results for `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and `.pdf` tests in specs/002-ui-exe-packaging/quickstart.md
- [x] T041 [P] Run and record unsupported-extension, no-match, folder traversal, and `skipped_unsupported.txt` regression results in specs/002-ui-exe-packaging/quickstart.md
- [x] T042 Build `dist/MaskingTool.exe` with `packaging/build_exe.ps1` and record the result in specs/002-ui-exe-packaging/quickstart.md
- [x] T043 Run packaged smoke tests in normal and distribution verification modes and record results in specs/002-ui-exe-packaging/quickstart.md
- [x] T044 Execute the distribution checklist, including timing measurements and environment notes, in packaging/distribution-checklist.md
- [x] T045 Review README.md, specs/002-ui-exe-packaging/quickstart.md, and packaging/README.md for consistent command names, verification modes, and artifact paths

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP
- **User Story 2 (Phase 4)**: Depends on Foundational and should be validated after US1 UI exists
- **User Story 3 (Phase 5)**: Depends on US1 and US2 because it verifies the built executable and UI flow
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Start after Foundational; no dependency on US2 or US3
- **US2 (P2)**: Start after Foundational; packaging smoke is meaningful after US1 UI changes land
- **US3 (P3)**: Start after US1 and US2; verifies the distributable result and per-format release gate

### Parallel Opportunities

- T003 and T004 can run in parallel after T001/T002 are understood.
- T005 and T008 can run in parallel because both target packaging constants/helpers.
- T009, T010, T011, T012, and T013 can be written in parallel before US1 implementation.
- T019, T020, T021, T022, and T023 can be written in parallel before packaging implementation.
- T029, T030, T031, and T032 can be written in parallel before checklist documentation.
- T039, T040, and T041 can run in parallel after all story implementation tasks are complete.

---

## Parallel Example: User Story 1

```text
Task: "T009 [P] [US1] Add UI layout contract tests in tests/contract/test_ui_layout_contract.py"
Task: "T010 [P] [US1] Add UI validation contract tests in tests/contract/test_ui_layout_contract.py"
Task: "T011 [P] [US1] Add UI completion summary contract tests in tests/contract/test_ui_layout_contract.py"
Task: "T012 [P] [US1] Add Japanese/space/symbol path handling coverage in tests/contract/test_ui_layout_contract.py"
Task: "T013 [P] [US1] Add UI usability contract checks in tests/contract/test_ui_layout_contract.py"
```

## Parallel Example: User Story 2

```text
Task: "T019 [P] [US2] Add packaging contract tests in tests/contract/test_packaging_contract.py"
Task: "T020 [P] [US2] Add packaging script contract tests in tests/contract/test_packaging_contract.py"
Task: "T021 [P] [US2] Add normal smoke-mode test in tests/integration/test_packaged_app_smoke.py"
Task: "T022 [P] [US2] Add distribution verification smoke-mode test in tests/integration/test_packaged_app_smoke.py"
```

## Parallel Example: User Story 3

```text
Task: "T029 [P] [US3] Add verification checklist contract tests in tests/contract/test_packaging_contract.py"
Task: "T030 [P] [US3] Add per-format regression gate contract tests in tests/contract/test_packaging_contract.py"
Task: "T031 [P] [US3] Add packaged manual sample smoke coverage in tests/integration/test_packaged_app_smoke.py"
Task: "T032 [P] [US3] Add distribution verification missing-exe coverage in tests/integration/test_packaged_app_smoke.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate: development UI can run a sample masking flow and show results

### Incremental Delivery

1. Setup + Foundational -> shared contracts ready
2. US1 -> usable redesigned UI MVP
3. US2 -> single-file `MaskingTool.exe` with normal/distribution smoke modes
4. US3 -> documented distribution verification with per-format and timing gates
5. Polish -> full test/build/checklist validation

### Format Validation

All tasks use the required checklist format: `- [ ] T### [P?] [US?] Description with file path`.
