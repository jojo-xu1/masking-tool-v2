# Implementation Plan: Unicode Normalization Matching

**Branch**: `005-unicode-normalization-matching` | **Date**: 2026-06-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/005-unicode-normalization-matching/spec.md`

## Summary

Fix Unicode width matching so detected phrases imported through Japanese Excel
workflows match in-scope target text even when one side uses full-width
ASCII-compatible characters and the other uses half-width ASCII. The
implementation will define one shared width-equivalent matching behavior,
preserve `置換提案` exactly as provided, prefer exact raw matches over
width-equivalent matches, reuse existing deterministic ordering when no exact
raw match applies, and apply the behavior consistently to supported text,
Office, workbook, and text-layer PDF replacement paths.

## Technical Context

**Language/Version**: Python 3.11+; current project metadata requires Python
3.11 or newer

**Primary Dependencies**: Python standard Unicode support for width-equivalent
comparison, existing `openpyxl` for replacement tables and `.xlsx`, existing
`python-docx` for `.docx`, existing `python-pptx` for `.pptx`, existing PyMuPDF
for text-layer `.pdf`, existing pytest test suite

**Storage**: Local filesystem only; output files and `skipped_unsupported.txt`
continue to be written to the selected output folder

**Testing**: pytest unit, integration, and contract tests with generated
fixtures covering full-width `検出語句` to half-width targets, half-width
`検出語句` to full-width targets, exact raw match precedence, unchanged CJK
text, exact replacement proposal preservation, deterministic reruns, and
unsupported-content reporting

**Target Platform**: Windows-first local desktop utility, with path handling kept
platform-neutral through existing `pathlib` usage

**Project Type**: Single Python desktop utility with reusable file replacement
modules

**Performance Goals**: Keep width-equivalent matching within the existing folder
run goal of processing 100 mixed small documents within 5 minutes; avoid
user-visible delay for small text, Office, workbook, and text-layer PDF samples

**Constraints**: Must not overwrite originals; must not use raw byte replacement
for Office or PDF binaries; must not process image text, scanned PDFs, embedded
objects, or OCR-dependent content as masked; must preserve deterministic
replacement order; must write replacement proposals exactly as supplied; must
prefer exact raw matches before width-equivalent matches

**Scale/Scope**: Targeted matching semantics fix for `.txt`, `.csv`, `.log`,
`.docx`, `.xlsx`, `.pptx`, and text-layer `.pdf`; no change to supported
extensions, UI selection flow, or excluded content boundaries

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Scope keeps the first-version supported extensions: `.txt`, `.csv`,
  `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf`; image text, scanned
  PDFs, embedded objects, and OCR remain out of scope.
- PASS: Replacement source remains `機密情報検出結果.xlsx` with `No`,
  `検出語句`, and `置換提案`; replacement remains deterministic and no
  reversible mappings are written to output files.
- PASS: Existing file/folder selection flow, output files, and
  `skipped_unsupported.txt` behavior are preserved.
- PASS: Python and format-specific structured libraries are identified; Office
  and PDF files will continue to use structured APIs rather than raw binary
  replacement.
- PASS: Test plan adds fixtures for supported extensions, width-equivalent
  directions, raw-match precedence, CJK preservation, exact replacement proposal
  preservation, deterministic reruns, and skip-report behavior.

## Project Structure

### Documentation (this feature)

```text
specs/005-unicode-normalization-matching/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── unicode-normalization-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── masking_tool/
    ├── text_replacer.py
    ├── office_replacer.py
    ├── pdf_replacer.py
    ├── replacement_table.py
    └── models.py

tests/
├── contract/
├── fixtures/
├── integration/
└── unit/
```

**Structure Decision**: Keep the change inside the existing single Python
package. The shared matching semantics should be available to text, Office,
workbook, and PDF replacement paths. Add focused fixture generation plus unit,
contract, and integration coverage rather than changing orchestration, UI, or
file discovery modules.

## Complexity Tracking

No constitution violations.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md), and
[contracts/unicode-normalization-contract.md](./contracts/unicode-normalization-contract.md).

## Post-Design Constitution Check

- PASS: Data model defines replacement rules, width-equivalent keys, match
  candidates, in-scope text segments, and processed outputs without expanding
  supported file scope.
- PASS: Contract requires exact raw match precedence, bidirectional
  full-width/half-width matching, exact replacement proposal preservation, CJK
  preservation, and deterministic behavior.
- PASS: Quickstart validates all supported extension families, raw-match
  precedence, CJK preservation, no reversible mappings, and skip-report
  behavior.
- PASS: Safety boundaries remain unchanged for image text, scanned PDFs,
  embedded objects, and OCR-dependent content.
