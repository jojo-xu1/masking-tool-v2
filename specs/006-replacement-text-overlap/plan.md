# Implementation Plan: Replacement Text Overlap Prevention

**Branch**: `006-replacement-text-overlap` | **Date**: 2026-06-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/006-replacement-text-overlap/spec.md`

## Summary

Prevent replacement labels from visually overlapping in supported fixed-size
visual text regions, with `.pptx` shapes, text boxes, and table cells as the
primary reported path. The implementation will preserve the existing visual
region first, make replacement text readable within that region when possible,
record a layout warning when readability cannot be guaranteed, and keep existing
deterministic replacement, Unicode width matching, split-run Office replacement,
and unsupported-content reporting intact.

## Technical Context

**Language/Version**: Python 3.11+; current project metadata requires Python
3.11 or newer

**Primary Dependencies**: Existing `python-pptx` for `.pptx` visual text
regions, existing `python-docx` for `.docx`, existing `openpyxl` for replacement
tables and `.xlsx`, existing PyMuPDF for text-layer `.pdf`, existing shared
`text_replacer.plan_replacements` deterministic matching behavior, pytest for
automated tests

**Storage**: Local filesystem only; output files and `skipped_unsupported.txt`
continue to be written to the selected output folder

**Testing**: pytest integration and contract tests with generated `.pptx`
fixtures that reproduce tightly spaced diagram/text-box replacements,
replacement-overflow warnings, existing Unicode matching, split-run Office
behavior, deterministic reruns, and skip-report behavior

**Target Platform**: Windows-first local desktop utility, with path handling kept
platform-neutral through existing `pathlib` usage

**Project Type**: Single Python desktop utility with reusable file replacement
modules

**Performance Goals**: Process overlap-prevention fixtures with no user-visible
delay beyond existing Office processing; preserve the first-version folder run
goal of 100 mixed small documents within 5 minutes

**Constraints**: Must not overwrite originals; must not use raw byte/string
replacement for Office or PDF binaries; must not process image text, embedded
objects, scanned PDFs, or OCR-dependent content as masked; must preserve
deterministic replacement order; must keep replacement labels in the original
visual region before warning; must record layout warnings without treating
otherwise successful readable regions as failed

**Scale/Scope**: Targeted visual-readability bug fix for supported fixed-size
visual text regions, primarily `.pptx` shapes, text boxes, and table cells; no
change to supported extensions, UI selection flow, replacement-table schema, or
excluded content boundaries

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Scope keeps the first-version supported extensions: `.txt`, `.csv`,
  `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf`; image text, scanned
  PDFs, embedded objects, and OCR remain out of scope.
- PASS: Replacement source remains `機密情報検出結果.xlsx` with `No`,
  `検出語句`, and `置換提案`; replacement remains deterministic and no
  reversible mappings are written to output files.
- PASS: Existing file/folder selection flow, output files, and
  `skipped_unsupported.txt` behavior are preserved, with layout warnings
  recorded as reportable messages.
- PASS: Python and format-specific structured libraries are identified; Office
  files will continue to be handled through `python-pptx` and `python-docx`,
  not raw binary replacement.
- PASS: Test plan adds focused `.pptx` visual-overlap fixtures while preserving
  existing supported-extension and skip-report regression tests.

## Project Structure

### Documentation (this feature)

```text
specs/006-replacement-text-overlap/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── replacement-layout-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── masking_tool/
    ├── office_replacer.py
    ├── text_replacer.py
    ├── app.py
    ├── report.py
    └── models.py

tests/
├── contract/
├── fixtures/
├── integration/
└── unit/
```

**Structure Decision**: Keep the change inside the existing single Python
package. `office_replacer.py` owns `.pptx` shape/text-box/table-cell traversal
and is the primary implementation location. Existing orchestration in `app.py`
and skip-report formatting in `report.py` should continue to accept result
messages as reportable warnings. Add fixture helpers and integration coverage
rather than changing UI or file discovery modules.

## Complexity Tracking

No constitution violations.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md), and
[contracts/replacement-layout-contract.md](./contracts/replacement-layout-contract.md).

## Post-Design Constitution Check

- PASS: Data model defines visual text regions, layout attempts, layout
  warnings, and processed outputs without expanding supported file scope.
- PASS: Contract requires readable non-overlapping `.pptx` replacements,
  original-phrase absence, warning behavior for unreadable regions, and
  preservation of excluded scope.
- PASS: Quickstart validates screenshot-style fixtures, overflow-warning
  fixtures, existing Unicode/split-run/deterministic regressions, full suite,
  and `git diff --check`.
- PASS: Safety boundaries remain unchanged for image text, scanned PDFs,
  embedded objects, and OCR-dependent content.
