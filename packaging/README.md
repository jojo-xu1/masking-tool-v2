# Packaging

This directory contains the repeatable Windows build flow for the desktop app.

## Build

```powershell
python -m pip install -e .[test,build]
.\packaging\build_exe.ps1
```

Expected artifact:

```text
dist\MaskingTool.exe
```

## Verification Modes

Normal automated test runs may skip packaged smoke checks when
`dist\MaskingTool.exe` does not exist. Distribution verification mode treats a
missing exe as a failure.

Use the release checklist in `packaging/distribution-checklist.md` before
sharing the executable.
