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

## Build Windows exe

Install the build extra, then run the packaging script from the repository root:

```powershell
python -m pip install -e .[test,build]
.\packaging\build_exe.ps1
```

Expected artifact:

```text
dist\MaskingTool.exe
```

Packaged smoke tests use two modes:
- normal test mode skips packaged checks when `dist\MaskingTool.exe` is absent
- distribution verification mode fails when `dist\MaskingTool.exe` is absent

Before distributing the exe, complete
`packaging\distribution-checklist.md`. The checklist records replacement-table
loading, file type detection, every supported extension, unsupported extensions,
no-match inputs, `skipped_unsupported.txt`, PDF Japanese readability, and UI/exe
timing measurements.

## Limitations

PDF handling is limited to files with an extractable text layer. Scanned PDFs,
image text, embedded objects, and OCR-dependent content are recorded as outside
first-version scope rather than treated as successfully masked.
