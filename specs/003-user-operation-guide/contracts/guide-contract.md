# Guide Contract: ユーザー向け操作手順書

## Artifacts

- Markdown source: `docs/user-guide.md`
- PDF distribution copy: `docs/user-guide.pdf`

## Required Markdown Sections

The guide must contain user-facing sections for:

1. Overview and safe-use purpose.
2. Before you start.
3. Supported files and excluded content.
4. Replacement table requirements.
5. Launching `MaskingTool.exe`.
6. Processing a single file.
7. Processing a folder.
8. Choosing output folder.
9. Reading results and `skipped_unsupported.txt`.
10. Troubleshooting.
11. Pre-use checklist.
12. Review questions and elapsed-time recording.

## Required Terms

The Markdown source and PDF must include:

- `MaskingTool.exe`
- `機密情報検出結果.xlsx`
- `No`
- `検出語句`
- `置換提案`
- `skipped_unsupported.txt`
- `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, `.pdf`
- image text, scanned PDFs, embedded objects, OCR as excluded scope
- under 10 minutes, under 15 minutes, and 90% review correctness

## Troubleshooting Coverage

Troubleshooting must cover:

- Missing replacement table, input target, or output folder.
- Invalid replacement table columns or rows.
- Unsupported files recorded in `skipped_unsupported.txt`.
- Files that fail during processing.
- `MaskingTool.exe` not launching.

## PDF Alignment

- The PDF must be generated from `docs/user-guide.md`.
- The PDF must contain the required terms from the Markdown source.
- The PDF must be readable as a standalone user distribution document.
- The PDF must contain the review questions and elapsed-time recording guidance.

## Review Validation

- The guide must provide a place to record sample single-file masking elapsed
  time.
- The guide must provide a place to record sample folder masking elapsed time.
- The guide must include review questions covering supported scope, excluded
  scope, replacement table, output files, and report interpretation.
- The guide must state the 90% correctness threshold for review questions.

## Non-Goals

- No developer build manual.
- No installer manual.
- No separate review checklist document.
- No online help site.
- No multilingual guide in this feature.
