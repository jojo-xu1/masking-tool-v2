# Implementation Plan: DOCX/PPTX Split Text Replacement

**Branch**: `004-docx-pptx-run-replacement` | **Date**: 2026-06-12 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/004-docx-pptx-run-replacement/spec.md`

## Summary

Fix the supported Office replacement path so visible `.docx` and `.pptx` body
text containing `Technologies, Inc.` is replaced even when Office stores the
phrase across multiple text runs. The implementation will keep the existing
Python Office libraries, evaluate replacement candidates at the paragraph,
text-box paragraph, and table-cell paragraph level, write the replacement using
the first visible matched portion's `bold`, `italic`, font size, and color,
count each visible matched phrase as one replacement, and record detectable
out-of-scope Office content in `skipped_unsupported.txt`.

## Technical Context

**Language/Version**: Python 3.11+; current project metadata requires Python
3.11 or newer

**Primary Dependencies**: Existing `python-docx` for `.docx`,
`python-pptx` for `.pptx`, `openpyxl` for replacement tables and existing
`.xlsx` support, existing shared `text_replacer.replace_text` deterministic
rule behavior, pytest for automated tests

**Storage**: Local filesystem only; output Office files and
`skipped_unsupported.txt` continue to be written to the selected output folder

**Testing**: pytest integration and unit tests with generated `.docx` and
`.pptx` fixtures containing split-run `Technologies, Inc.` in paragraphs,
text boxes, and table cells

**Target Platform**: Windows-first local desktop utility, with path handling kept
platform-neutral through existing `pathlib` usage

**Project Type**: Single Python desktop utility with reusable file replacement
modules

**Performance Goals**: Process split-run Office fixtures with no user-visible
delay beyond existing Office processing; preserve first-version folder run goal
of 100 mixed small documents within 5 minutes

**Constraints**: Must not overwrite originals; must not use raw byte/string
replacement for Office binaries; must not process images, embedded objects, or
OCR-dependent content as masked; must preserve deterministic replacement order;
must count one visible split phrase as one replacement regardless of internal run
count; must record detectable out-of-scope Office content even when visible body
text in the same file is successfully replaced

**Scale/Scope**: Targeted Office bug fix for `.docx` and `.pptx` visible body
text inside the same paragraph, text box, or table cell; no change to `.txt`,
`.csv`, `.log`, `.xlsx`, or text-layer `.pdf` behavior

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Scope keeps the first-version supported extensions and directly changes
  only `.docx` and `.pptx`; image text, scanned PDFs, embedded objects, and OCR
  remain out of scope.
- PASS: Replacement source remains `機密情報検出結果.xlsx` with `No`,
  `検出語句`, and `置換提案`; replacement remains deterministic and no
  reversible mappings are written to output files.
- PASS: Existing file/folder selection flow, output files, and
  `skipped_unsupported.txt` behavior are preserved.
- PASS: Python and format-specific structured libraries are identified;
  Office files will continue to be handled through `python-docx` and
  `python-pptx`, not raw binary replacement.
- PASS: Test plan adds focused `.docx` and `.pptx` split-run fixtures while
  preserving existing supported-extension and skip-report tests.

## Project Structure

### Documentation (this feature)

```text
specs/004-docx-pptx-run-replacement/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── office-replacement-contract.md
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
    └── models.py

tests/
├── fixtures/
│   └── create_fixtures.py
└── integration/
    ├── test_single_office_files.py
    └── test_deterministic_rerun.py
```

**Structure Decision**: Keep the change inside the existing single Python
package. `office_replacer.py` owns Office traversal and replacement, while
existing orchestration in `app.py`, replacement table parsing, scanning, and UI
remain unchanged. Add fixture helpers and integration coverage rather than a new
module unless implementation complexity requires extracting a small internal
run-mapping helper.

## Complexity Tracking

No constitution violations.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md), and
[contracts/office-replacement-contract.md](./contracts/office-replacement-contract.md).

## Post-Design Constitution Check

- PASS: Data model defines visible in-scope Office text, split-run matches,
  processed outputs, and result counting.
- PASS: Contract explicitly limits split-run replacement to the same paragraph,
  text box, or table cell, and excludes structural-boundary spanning text.
- PASS: Quickstart validates `.docx` and `.pptx` split-run paragraph/text-box
  and table-cell cases, first-run formatting, one-visible-phrase counting,
  no-match behavior, and existing Office regression tests.
- PASS: Safety boundaries remain unchanged for embedded objects, image text,
  scanned PDFs, and OCR-dependent content; detectable out-of-scope Office
  content remains recorded in `skipped_unsupported.txt`.
