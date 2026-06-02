# Quickstart: UI改善とexe配布

## Prerequisites

- Windows
- Python 3.11 or newer
- Existing masking tests pass

## Install Build Dependencies

```powershell
python -m pip install -e .[test,build]
```

## Run Development UI

```powershell
python -m masking_tool
```

Verify:

1. The UI shows grouped sections for inputs, execution, and results.
2. Required selections are easy to identify.
3. Missing inputs show validation messages.
4. A sample file can be processed.
5. Completion counts and report path remain visible.
6. Record development UI launch time and UI selection recognition time in
   `packaging/distribution-checklist.md` when preparing a release.

## Build Single exe

```powershell
.\packaging\build_exe.ps1
```

Expected output:

```text
dist\MaskingTool.exe
```

## Verify Distribution

1. Run all automated tests:

   ```powershell
   python -m pytest
   ```

2. Confirm the automated and manual regression gate covers replacement-table
   loading, file type detection, `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`,
   `.pptx`, text-layer `.pdf`, unsupported extensions, no-match inputs, and
   `skipped_unsupported.txt`.

3. Launch the exe:

   ```powershell
   .\dist\MaskingTool.exe
   ```

4. For normal test runs, packaged smoke checks may skip when
   `dist\MaskingTool.exe` is absent. For distribution verification mode, absence
   of `dist\MaskingTool.exe` is a failure.
5. Select `tests/fixtures/replacement_tables/機密情報検出結果_manual_sensitive.xlsx`.
6. Process `tests/fixtures/inputs/manual_sensitive_samples/`.
7. Confirm replaced files and `skipped_unsupported.txt` are written to the output folder.
8. Confirm the PDF sample has readable Japanese replacement text.
9. Record UI recognition, sample single-file processing, development UI launch,
   and packaged exe launch timings in `packaging/distribution-checklist.md`.

## Implementation Validation Record

- Replacement table, scanner, and skip report tests: `7 passed`
- Supported-extension regression tests: `4 passed`
- Unsupported/no-match/folder/skip-report regression tests: `5 passed`
- Full regression suite: `39 passed`
- Exe build result: `dist\MaskingTool.exe` created
- Exe artifact size: `45,835,666` bytes
- Packaged smoke mode result: `4 passed`
- Packaged process launch check: process started and was stopped after 5 seconds
- Manual visual timing checks: record final release values in `packaging/distribution-checklist.md`

## Known Non-Goals

- No installer.
- No code signing.
- No auto-update.
- No packaging for macOS or Linux.
