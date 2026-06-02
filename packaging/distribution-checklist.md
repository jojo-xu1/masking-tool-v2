# Distribution Verification Checklist

Record the result before distributing `dist\MaskingTool.exe`.

## Environment

- Date:
- 2026-06-02
- Windows version:
- Windows 11 10.0.22621
- Python version:
- Python 3.14.5
- Verification mode: distribution
- Notes:
- Automated build and regression checks completed. Manual visual timing and
  end-user GUI operation should be rechecked immediately before sharing the exe.

## Automated Regression Gate

- [x] Core tests passed (`python -m pytest`)
- [x] Replacement table loading verified
- [x] File type detection verified
- [x] Supported extensions verified: `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, text-layer `.pdf`
- [x] Unsupported extensions recorded without modification
- [x] No-match inputs verified
- [x] Skipped unsupported report (`skipped_unsupported.txt`) generation verified

## Executable Gate

- [x] `dist\MaskingTool.exe` exists
- [x] Missing exe fails distribution verification mode
- [x] Normal smoke mode skips packaged checks when exe is absent
- [x] Exe launches as a Windows process without a Python command
- [ ] Exe launch works outside the repository root

## Manual Sensitive Sample Gate

- Replacement table: `tests/fixtures/replacement_tables/機密情報検出結果_manual_sensitive.xlsx`
- Input folder: `tests/fixtures/inputs/manual_sensitive_samples/`

- [ ] Single-file sample processed from the packaged GUI
- [ ] Folder sample processed from the packaged GUI
- [ ] Replaced files written to the selected output folder from the packaged GUI
- [ ] `skipped_unsupported.txt` written to the selected output folder from the packaged GUI
- [ ] PDF Japanese readability verified from the packaged GUI

## Timing Gate

- [ ] UI recognition seconds: manual / threshold 30
- [ ] Sample single-file seconds: manual / threshold 300
- [ ] Development UI launch seconds: manual / threshold 5
- [x] Packaged exe launch seconds: <=5 / threshold 15
