# Implementation Plan: ユーザー向け操作手順書

**Branch**: `003-user-operation-guide` | **Date**: 2026-06-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/003-user-operation-guide/spec.md`

## Summary

Create a Japanese end-user operation guide for the masking tool that explains
launch, replacement table selection, file/folder input selection, execution,
result confirmation, supported and excluded scope, and troubleshooting. The
Markdown guide at `docs/user-guide.md` is the source of truth, and a distribution
PDF is generated from the same content and retained as a distributable artifact
so non-developer users can receive either format. The guide body also includes
review questions and elapsed-time recording guidance for validating the
measurable success criteria.

## Technical Context

**Language/Version**: Python 3.11+; current workspace uses Python 3.14.5

**Primary Dependencies**: Existing PyMuPDF dependency for PDF creation; pytest for
document contract checks

**Storage**: Local documentation files only: `docs/user-guide.md` and tracked
distribution artifact `docs/user-guide.pdf`

**Testing**: pytest contract tests for required guide sections, required scope
statements, troubleshooting coverage, review questions/elapsed-time guidance,
and Markdown/PDF content alignment

**Target Platform**: Windows desktop users receiving `MaskingTool.exe`

**Project Type**: Documentation deliverable within the existing Python desktop
utility repository

**Performance Goals**: A first-time user can complete sample single-file masking
from the guide in under 10 minutes and sample folder masking in under 15 minutes;
the guide provides the review questions and timing fields needed to record this
validation.

**Constraints**: Guide must be Japanese, business-user friendly, avoid requiring
Python/build knowledge for normal operation, clearly state supported and excluded
scope, and preserve the masking tool safety boundaries

**Scale/Scope**: One Markdown source guide, one tracked generated PDF, contract
tests, and a lightweight generation path; no separate review checklist document,
installer manual, online help site, or multi-language documentation in this
feature

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Guide must state supported extensions: `.txt`, `.csv`, `.log`, `.docx`,
  `.xlsx`, `.pptx`, and text-based `.pdf`.
- PASS: Guide must state excluded scope: image text, scanned PDFs, embedded
  objects, and OCR-dependent content.
- PASS: Guide must explain `機密情報検出結果.xlsx` and required headers `No`,
  `検出語句`, and `置換提案`.
- PASS: Guide must explain file/folder selection, output files, and
  `skipped_unsupported.txt`.
- PASS: Guide validation must check scope, output artifacts, troubleshooting,
  and result interpretation.
- PASS: Guide must include review questions and elapsed-time recording guidance
  in the user guide body so SC-001, SC-002, and SC-003 are directly verifiable.

## Project Structure

### Documentation (this feature)

```text
specs/003-user-operation-guide/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── guide-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
docs/
├── user-guide.md
└── user-guide.pdf

src/
└── masking_tool/
    └── docgen.py

tests/
└── contract/
    └── test_user_guide_contract.py
```

**Structure Decision**: Keep user-facing documentation under `docs/`. Add a
small Python generation helper only to produce `docs/user-guide.pdf` from the
Markdown source and keep the content aligned.

## Complexity Tracking

No constitution violations.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md), and
[contracts/guide-contract.md](./contracts/guide-contract.md).

## Post-Design Constitution Check

- PASS: Guide contract requires all constitutionally mandated scope statements.
- PASS: Data model includes operation, scope, troubleshooting, and pre-use
  checklist sections.
- PASS: Quickstart validates Markdown source, PDF generation, and guide content
  checks.
- PASS: Guide contract requires review questions and elapsed-time recording
  guidance in the Markdown and generated PDF.
- PASS: No supported/excluded file behavior is changed by this documentation
  feature.
