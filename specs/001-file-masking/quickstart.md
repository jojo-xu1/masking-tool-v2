# Quickstart: 機密文字列ファイルマスキング

## Prerequisites

- Python 3.11 or newer
- Local access to sample Office, text, and text-based PDF files

## Install

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install openpyxl python-docx python-pptx pymupdf pytest
```

## Prepare Fixtures

Create fixture inputs under `tests/fixtures/inputs/`:

- `sample.txt`
- `sample.csv`
- `sample.log`
- `sample.docx`
- `sample.xlsx`
- `sample.pptx`
- `sample.pdf` with extractable text
- `scanned.pdf` with no extractable text
- `unsupported.bin`
- `no_match.txt`

Create `tests/fixtures/replacement_tables/機密情報検出結果.xlsx` with headers:

```text
No	検出語句	置換提案
1	山田太郎	<PERSON_001>
2	example@example.com	<EMAIL_001>
```

Each supported fixture should contain at least one detected phrase. The no-match
fixture should contain none of the detected phrases.

## Run Manually

```powershell
python -m masking_tool
```

Manual validation:

1. Select the replacement table fixture.
2. Select single-file mode and process one supported fixture.
3. Confirm the output file is created in the selected output folder.
4. Confirm original detected phrases are absent from output content.
5. Confirm replacement proposals appear in output content.
6. Select folder mode.
7. Run direct-child-only mode.
8. Run recursive mode with a nested fixture folder.
9. Confirm `skipped_unsupported.txt` is created and records unsupported or
   excluded files.

## Run Tests

```powershell
python -m pytest
```

Required passing checks:

- Replacement table validation accepts required headers.
- Replacement table validation rejects missing headers, blank phrases, blank
  proposals, and duplicate detected phrases.
- `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf`
  fixtures replace every detected phrase.
- No-match supported files are processed without false failure.
- Unsupported extensions are recorded as `skipped_unsupported`.
- Scanned or image-text-only PDFs are recorded as `skipped_unsupported`.
- Recursive mode preserves relative subfolder paths in the output folder.
- Direct-child-only mode does not process subfolder files.
- Re-running the same input and replacement table produces equivalent output
  content and skip-report entries.
