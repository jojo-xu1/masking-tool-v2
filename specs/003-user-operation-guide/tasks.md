# Tasks: ユーザー向け操作手順書

**Input**: Design documents from `/specs/003-user-operation-guide/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: REQUIRED. The guide is safety-relevant documentation, so contract tests must verify required sections, required scope terms, troubleshooting coverage, review questions and elapsed-time recording, Markdown/PDF alignment, and the absence of normal-use developer-only instructions.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare guide output locations and PDF generation entry point.

- [x] T001 Create documentation directory structure for `docs/user-guide.md` and `docs/user-guide.pdf`
- [x] T002 [P] Confirm `docs/user-guide.pdf` is retained as a tracked distribution artifact by checking `.gitignore` and documenting the retention decision in `specs/003-user-operation-guide/quickstart.md`
- [x] T003 [P] Create PDF generation module skeleton in `src/masking_tool/docgen.py`
- [x] T004 [P] Create guide contract test file skeleton in `tests/contract/test_user_guide_contract.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define shared guide contract data before writing story-specific content.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T005 Define required guide section titles, required terms, troubleshooting topics, review validation terms, and artifact paths in `src/masking_tool/docgen.py`
- [x] T006 [P] Add contract tests for required artifact paths `docs/user-guide.md` and `docs/user-guide.pdf` in `tests/contract/test_user_guide_contract.py`
- [x] T007 [P] Add contract tests for required section titles from `specs/003-user-operation-guide/contracts/guide-contract.md`, including review questions and elapsed-time recording, in `tests/contract/test_user_guide_contract.py`
- [x] T008 [P] Add contract tests for required terms from `specs/003-user-operation-guide/contracts/guide-contract.md`, including under 10 minutes, under 15 minutes, and 90% review correctness, in `tests/contract/test_user_guide_contract.py`
- [x] T009 Implement Markdown-to-PDF generation behavior in `src/masking_tool/docgen.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - 初回利用者が手順書だけで基本操作できる (Priority: P1) - MVP

**Goal**: First-time users can follow the guide to launch the tool, select inputs, run masking, confirm outputs, and record sample run times without developer help.

**Independent Test**: A reader can use `docs/user-guide.md` to complete a sample single-file or folder run, record elapsed time, and explain where replaced files and `skipped_unsupported.txt` are located.

### Tests for User Story 1

- [x] T010 [P] [US1] Add guide contract tests for launch, replacement table selection, single-file flow, folder flow, output folder selection, execution, and result confirmation sections in `tests/contract/test_user_guide_contract.py`
- [x] T011 [P] [US1] Add guide contract tests for result terms replaced, no-match, skipped unsupported, failed, report path, and `skipped_unsupported.txt` in `tests/contract/test_user_guide_contract.py`
- [x] T012 [P] [US1] Add guide contract tests for elapsed-time recording fields for sample single-file and folder runs in `tests/contract/test_user_guide_contract.py`
- [x] T013 [P] [US1] Add PDF alignment test confirming generated PDF contains core basic workflow and elapsed-time terms in `tests/contract/test_user_guide_contract.py`

### Implementation for User Story 1

- [x] T014 [US1] Write the overview, before-you-start, launch, replacement table selection, and output folder sections in `docs/user-guide.md`
- [x] T015 [US1] Write the single-file processing and folder processing procedures, including traversal scope explanation, in `docs/user-guide.md`
- [x] T016 [US1] Write the result confirmation section covering replaced, no-match, skipped unsupported, failed, report path, and `skipped_unsupported.txt` in `docs/user-guide.md`
- [x] T017 [US1] Write elapsed-time recording guidance for under 10 minute single-file validation and under 15 minute folder validation in `docs/user-guide.md`
- [x] T018 [US1] Generate `docs/user-guide.pdf` from `docs/user-guide.md` with `python -m masking_tool.docgen docs/user-guide.md docs/user-guide.pdf`

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - 対象範囲と対象外範囲を理解できる (Priority: P2)

**Goal**: Users understand supported file types, excluded content, replacement table requirements, and why skipped files are not treated as masked.

**Independent Test**: A reader can correctly answer guide-body review questions about supported extensions, excluded content, required replacement table columns, and skip report meaning.

### Tests for User Story 2

- [x] T019 [P] [US2] Add guide contract tests for supported extensions `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf` in `tests/contract/test_user_guide_contract.py`
- [x] T020 [P] [US2] Add guide contract tests for excluded scope image text, scanned PDFs, embedded objects, and OCR-dependent content in `tests/contract/test_user_guide_contract.py`
- [x] T021 [P] [US2] Add guide contract tests for replacement table columns `No`, `検出語句`, and `置換提案` in `tests/contract/test_user_guide_contract.py`
- [x] T022 [P] [US2] Add guide contract tests for review questions covering supported scope, excluded scope, replacement table, output files, report interpretation, and 90% correctness threshold in `tests/contract/test_user_guide_contract.py`

### Implementation for User Story 2

- [x] T023 [US2] Write supported file and excluded content scope notes in `docs/user-guide.md`
- [x] T024 [US2] Write replacement table requirements and deterministic replacement explanation in `docs/user-guide.md`
- [x] T025 [US2] Write safety note explaining unsupported or unprocessable files are recorded and must be reviewed in `docs/user-guide.md`
- [x] T026 [US2] Write guide-body review questions and 90% correctness threshold in `docs/user-guide.md`
- [x] T027 [US2] Regenerate `docs/user-guide.pdf` from the updated `docs/user-guide.md`

**Checkpoint**: User Story 2 is independently testable through scope, replacement-table, and review-question validation.

---

## Phase 5: User Story 3 - エラーや想定外結果に対処できる (Priority: P3)

**Goal**: Users can use troubleshooting guidance to respond safely to common input, replacement table, skip report, processing, and exe launch problems.

**Independent Test**: A reader can map representative symptoms to likely causes and safe next actions using only the guide.

### Tests for User Story 3

- [x] T028 [P] [US3] Add guide contract tests for missing required input, invalid replacement table, unsupported files, processing failure, and exe launch failure troubleshooting entries in `tests/contract/test_user_guide_contract.py`
- [x] T029 [P] [US3] Add guide contract tests for the pre-use checklist covering replacement table, input target, output folder, supported scope, excluded scope, and result review in `tests/contract/test_user_guide_contract.py`
- [x] T030 [P] [US3] Add guide contract test that normal end-user operation does not require Python or build commands in `docs/user-guide.md` in `tests/contract/test_user_guide_contract.py`

### Implementation for User Story 3

- [x] T031 [US3] Write troubleshooting entries for missing inputs, invalid replacement table, unsupported files, processing failures, and exe launch failure in `docs/user-guide.md`
- [x] T032 [US3] Write the final pre-use checklist in `docs/user-guide.md`
- [x] T033 [US3] Add optional screenshot placeholder guidance without making screenshots required in `docs/user-guide.md`
- [x] T034 [US3] Regenerate `docs/user-guide.pdf` from the updated `docs/user-guide.md`

**Checkpoint**: All user stories are independently functional and ready for guide validation.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, PDF readability, review-measurement readiness, and documentation linkage.

- [x] T035 [P] Run `python -m pytest tests/contract/test_user_guide_contract.py` and record results in `specs/003-user-operation-guide/quickstart.md`
- [x] T036 Validate `docs/user-guide.pdf` exists, is tracked, and is readable as a standalone user distribution document
- [x] T037 [P] Add a link to `docs/user-guide.md` in `README.md`
- [x] T038 Review `docs/user-guide.md` for plain Japanese suitable for non-developer business users
- [x] T039 Review `docs/user-guide.md` and `docs/user-guide.pdf` for content alignment against `specs/003-user-operation-guide/contracts/guide-contract.md`
- [x] T040 Review `docs/user-guide.md` to confirm SC-001, SC-002, and SC-003 can be evaluated from the guide body without a separate review checklist document
- [x] T041 Run `git diff --check` and confirm no formatting errors across `docs/user-guide.md`, `src/masking_tool/docgen.py`, and `tests/contract/test_user_guide_contract.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - MVP
- **User Story 2 (Phase 4)**: Depends on Foundational and can be developed after or alongside US1, but PDF regeneration should follow Markdown updates
- **User Story 3 (Phase 5)**: Depends on Foundational and can be developed after or alongside US1/US2, but final checklist review depends on all guide content
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Start after Foundational; delivers a usable basic operation guide with timing fields
- **US2 (P2)**: Start after Foundational; scope notes and review questions integrate into the same guide
- **US3 (P3)**: Start after Foundational; troubleshooting and checklist integrate into the same guide

### Parallel Opportunities

- T002, T003, and T004 can run in parallel after T001.
- T006, T007, and T008 can run in parallel after T005.
- T010, T011, T012, and T013 can run in parallel before US1 guide content is finalized.
- T019, T020, T021, and T022 can run in parallel before US2 guide content is finalized.
- T028, T029, and T030 can run in parallel before US3 guide content is finalized.
- T035 and T037 can run in parallel after PDF generation and guide writing are complete.

---

## Parallel Example: User Story 1

```text
Task: "T010 [P] [US1] Add guide contract tests for basic workflow sections in tests/contract/test_user_guide_contract.py"
Task: "T011 [P] [US1] Add guide contract tests for result terms in tests/contract/test_user_guide_contract.py"
Task: "T012 [P] [US1] Add guide contract tests for elapsed-time recording fields in tests/contract/test_user_guide_contract.py"
Task: "T013 [P] [US1] Add PDF alignment test in tests/contract/test_user_guide_contract.py"
```

## Parallel Example: User Story 2

```text
Task: "T019 [P] [US2] Add guide contract tests for supported extensions in tests/contract/test_user_guide_contract.py"
Task: "T020 [P] [US2] Add guide contract tests for excluded scope in tests/contract/test_user_guide_contract.py"
Task: "T021 [P] [US2] Add guide contract tests for replacement table columns in tests/contract/test_user_guide_contract.py"
Task: "T022 [P] [US2] Add guide contract tests for review questions and 90% threshold in tests/contract/test_user_guide_contract.py"
```

## Parallel Example: User Story 3

```text
Task: "T028 [P] [US3] Add troubleshooting coverage tests in tests/contract/test_user_guide_contract.py"
Task: "T029 [P] [US3] Add pre-use checklist tests in tests/contract/test_user_guide_contract.py"
Task: "T030 [P] [US3] Add no-developer-commands test in tests/contract/test_user_guide_contract.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate: `docs/user-guide.md` and `docs/user-guide.pdf` explain the basic operation flow and provide elapsed-time fields

### Incremental Delivery

1. Setup + Foundational -> guide contract and PDF generation path ready
2. US1 -> basic operation guide MVP with timing fields
3. US2 -> safety scope, replacement table understanding, and review questions
4. US3 -> troubleshooting and pre-use checklist
5. Polish -> contract tests, PDF readability, README link, content alignment, and review-measurement readiness

### Format Validation

All tasks use the required checklist format: `- [ ] T### [P?] [US?] Description with file path`.
