# build_exe.ps1 reports only "Expected executable was not created"

## Summary

`packaging/build_exe.ps1` could report only:

```text
Expected executable was not created: E:\work\AI\masking-tool-v2\dist\MaskingTool.exe
```

This hides the real cause when PyInstaller is missing or when PyInstaller exits
with a non-zero status before creating `dist\MaskingTool.exe`.

## Expected Behavior

- If PyInstaller is not installed, the script should tell the user to run:

  ```powershell
  python -m pip install -e .[test,build]
  ```

- If PyInstaller fails, the script should stop immediately and report the
  PyInstaller exit code.
- The final `dist\MaskingTool.exe` existence check should remain as a last
  safeguard.

## Local Fix Applied

- Added a PyInstaller import check to `packaging/build_exe.ps1`.
- Added `$LASTEXITCODE` handling after `python -m PyInstaller`.
- Re-ran the build successfully and generated `dist\MaskingTool.exe`.
- Re-ran packaging contract and smoke tests successfully.

## Spec Reflection

Updated `specs/002-ui-exe-packaging/spec.md`:

- Clarification added for build failure handling.
- Edge case added for missing PyInstaller or PyInstaller build failure.
- Added `FR-014` requiring fail-fast build-script behavior.
- Added `SC-010` requiring build output to identify the real cause.

## Verification

```text
.\packaging\build_exe.ps1
Created E:\work\AI\masking-tool-v2\dist\MaskingTool.exe

python -m pytest tests\contract\test_packaging_contract.py tests\integration\test_packaged_app_smoke.py
11 passed
```
