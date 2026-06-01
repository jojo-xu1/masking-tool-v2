# Masking Tool v2

Local desktop utility for replacing detected confidential phrases in supported
files with irreversible replacement proposals from `機密情報検出結果.xlsx`.

Supported first-version targets:
- `.txt`
- `.csv`
- `.log`
- `.docx`
- `.xlsx`
- `.pptx`
- text-based `.pdf`

Out of scope for the first version:
- image text
- scanned PDFs
- embedded objects
- OCR-dependent content

## Install

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .[test]
```

## Run

```powershell
python -m masking_tool
```

The UI asks for:
1. replacement table
2. input file or folder
3. folder traversal mode when folder input is selected
4. output folder

Original files are not overwritten. Replaced files and
`skipped_unsupported.txt` are written to the selected output folder.

## Test

```powershell
python -m pytest
```

## Limitations

PDF handling is limited to files with an extractable text layer. Scanned PDFs,
image text, embedded objects, and OCR-dependent content are recorded as outside
first-version scope rather than treated as successfully masked.
