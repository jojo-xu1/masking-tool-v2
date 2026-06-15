# Implementation Plan: PDF Textbox Fit Preservation

**Branch**: `007-pdf-textbox-fit` | **Date**: 2026-06-15 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/007-pdf-textbox-fit/spec.md`

## Summary

Preserve one-page text-layer PDF layout when replacing detected phrases inside
constrained PDF text regions. The implementation will keep replacement text at
the original PDF font size whenever it fits inside the original page region,
avoid expanding replacement regions in a way that breaks page fit, still remove
the original detected phrase when layout cannot be guaranteed, and record a
clear layout warning through existing result messages and
`skipped_unsupported.txt`.

## Technical Context

**Language/Version**: Python 3.11+; current project metadata requires Python
3.11 or newer

**Primary Dependencies**: Existing PyMuPDF dependency for text-layer PDF
inspection, redaction, and replacement text insertion; existing
`text_replacer.plan_replacements` deterministic matching behavior; existing
`openpyxl` replacement-table loading; pytest for automated tests

**Storage**: Local filesystem only; output PDF files and
`skipped_unsupported.txt` continue to be written to the selected output folder

**Testing**: pytest integration and contract tests with generated text-layer PDF
fixtures that reproduce one-page constrained text regions, original-font fit
cases, original-font overflow warning cases, Japanese replacement text,
scanned-PDF exclusion, deterministic reruns, and skip-report visibility

**Target Platform**: Windows-first local desktop utility, with path handling kept
platform-neutral through existing `pathlib` usage

**Project Type**: Single Python desktop utility with reusable file replacement
modules

**Performance Goals**: Process focused PDF page-fit fixtures with no
user-visible delay beyond existing PDF processing; preserve the first-version
folder run goal of 100 mixed small documents within 5 minutes

**Constraints**: Must not overwrite originals; must not use raw byte/string
replacement for PDF binaries; must not process image text, scanned PDFs,
embedded objects, or OCR-dependent content as masked; must preserve deterministic
replacement order; must preserve original PDF font size before warning; must
still remove matched in-scope detected phrases when a layout warning is recorded

**Scale/Scope**: Targeted text-layer PDF page-fit bug fix; no change to
supported extensions, UI selection flow, replacement-table schema, Office
replacement behavior, or excluded content boundaries

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Scope keeps the first-version supported extensions and changes only
  text-based `.pdf`; image text, scanned PDFs, embedded objects, and OCR remain
  out of scope and reportable.
- PASS: Replacement source remains `機密情報検出結果.xlsx` with `No`,
  `検出語句`, and `置換提案`; replacement remains deterministic and no
  reversible mappings are written to output files.
- PASS: Existing file/folder selection flow, output files, and
  `skipped_unsupported.txt` behavior are preserved, with PDF layout warnings
  recorded as reportable messages.
- PASS: Python and PyMuPDF are identified for structured PDF handling; PDF
  binaries will not be modified through raw byte/string replacement.
- PASS: Test plan adds focused text-layer PDF page-fit fixtures while
  preserving existing supported-extension and skip-report regression tests.

## Project Structure

### Documentation (this feature)

```text
specs/007-pdf-textbox-fit/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── pdf-textbox-fit-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── masking_tool/
    ├── pdf_replacer.py
    ├── app.py
    ├── report.py
    ├── text_replacer.py
    └── models.py

tests/
├── contract/
├── fixtures/
├── integration/
└── unit/
```

**Structure Decision**: Keep the change inside the existing single Python
package. `pdf_replacer.py` owns text-layer PDF span discovery, redaction, and
replacement insertion, so it is the primary implementation location. Existing
orchestration in `app.py` and skip-report formatting in `report.py` should
continue to accept result messages as reportable layout warnings. Add generated
PDF fixture helpers, contract tests, and integration coverage rather than
changing UI or file discovery modules.

## Complexity Tracking

No constitution violations.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md), and
[contracts/pdf-textbox-fit-contract.md](./contracts/pdf-textbox-fit-contract.md).

## Post-Design Constitution Check

- PASS: Data model defines PDF text regions, layout attempts, layout warnings,
  and processed outputs without expanding supported file scope.
- PASS: Contract requires original-font-size fit behavior, original-phrase
  absence, warning behavior for unreadable regions, and preservation of excluded
  scope.
- PASS: Quickstart validates one-page constrained PDF fixtures, overflow-warning
  fixtures, existing Japanese/scanned/deterministic/skip-report regressions,
  full suite, and `git diff --check`.
- PASS: Safety boundaries remain unchanged for image text, scanned PDFs,
  embedded objects, and OCR-dependent content.
