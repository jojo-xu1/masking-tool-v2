# Implementation Plan: 機密文字列ファイルマスキング

**Branch**: `001-file-masking` | **Date**: 2026-06-01 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-file-masking/spec.md`

## Summary

Build a local Python desktop tool that lets the user select a replacement table,
an input file or folder, an output folder, and folder traversal mode. The tool
loads `機密情報検出結果.xlsx`, validates `No`, `検出語句`, and `置換提案`, then
applies deterministic replacements to supported text, Office, and text-based PDF
files. Unsupported, excluded, or failed files are left unchanged and recorded in
`skipped_unsupported.txt`.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: Tkinter for local file/folder selection UI; openpyxl for
`.xlsx` replacement table and workbook processing; python-docx for `.docx`;
python-pptx for `.pptx`; PyMuPDF for text-layer PDF detection and replacement;
pytest for automated tests

**Storage**: Local filesystem only; no database

**Testing**: pytest with generated fixture files for `.txt`, `.csv`, `.log`,
`.docx`, `.xlsx`, `.pptx`, text-based `.pdf`, unsupported extensions, no-match
inputs, invalid replacement table, and skipped/failed reports

**Target Platform**: Local desktop execution on Windows-first filesystem paths,
with implementation avoiding platform-specific path logic where practical

**Project Type**: Single Python desktop utility with reusable service modules and
a small UI entry point

**Performance Goals**: Process a folder of 100 mixed small documents within 5
minutes on a typical local workstation; keep UI responsive by showing progress
between files

**Constraints**: Must not overwrite originals; must not use OCR; must not treat
scanned PDFs or embedded objects as successfully masked; must keep replacements
deterministic; must preserve file format and structure as far as supported by
format libraries

**Scale/Scope**: First-version local batch tool for user-selected file sets;
direct-child-only and recursive folder traversal are user-selectable

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Scope is limited to `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`,
  and text-based `.pdf`; OCR, scanned PDFs, image text, and embedded objects are
  excluded and reported.
- PASS: Replacement source is `機密情報検出結果.xlsx` with `No`, `検出語句`, and
  `置換提案`; no reversible mapping is written to outputs.
- PASS: UI flow includes replacement table, input target, output folder, and
  folder traversal mode; unsupported/failed files are reported in
  `skipped_unsupported.txt`.
- PASS: Python and format-specific libraries are identified; binary Office/PDF
  files are handled through structured libraries, not raw byte replacement.
- PASS: Test plan covers all supported extensions, unsupported extensions,
  no-match inputs, invalid replacement table, and skip-report validation.

## Project Structure

### Documentation (this feature)

```text
specs/001-file-masking/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── ui-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── masking_tool/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── replacement_table.py
│   ├── scanner.py
│   ├── report.py
│   ├── text_replacer.py
│   ├── office_replacer.py
│   ├── pdf_replacer.py
│   └── ui.py
└── main.py

tests/
├── fixtures/
│   ├── replacement_tables/
│   ├── inputs/
│   └── expected/
├── integration/
├── unit/
└── contract/
```

**Structure Decision**: Use a single Python package because this is a local
desktop utility with no server boundary. Keep UI orchestration separate from
replacement services so format handlers can be tested independently.

## Complexity Tracking

No constitution violations.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md), and
[contracts/ui-contract.md](./contracts/ui-contract.md).

## Post-Design Constitution Check

- PASS: Data model includes replacement table rows, input targets, processing
  results, output files, and skip-report entries.
- PASS: UI contract covers file/folder selection, output folder selection,
  traversal mode, progress, completion, and validation failures.
- PASS: Quickstart requires fixture validation for every supported extension and
  `skipped_unsupported.txt`.
- PASS: PDF constraints remain explicit: only text-layer PDFs are processed;
  scanned/OCR-dependent PDFs are skipped.
