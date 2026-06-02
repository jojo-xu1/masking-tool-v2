# Packaging Contract: UI改善とexe配布

## Artifact

- Name: `MaskingTool.exe`
- Location: `dist/MaskingTool.exe`
- Mode: single-file executable
- Platform: Windows

## Build Command

The repository must expose a documented PowerShell build command that creates
`dist/MaskingTool.exe`.

The command must:
- Run from the repository root.
- Clean stale `dist/MaskingTool.exe` output before building.
- Use the application UI entry point.
- Return a non-zero exit code if the executable is not created.

## Verification

After building, verification must confirm:

- `dist/MaskingTool.exe` exists.
- Existing automated tests pass.
- Replacement-table loading is verified.
- File type detection is verified.
- All supported extensions are verified: `.txt`, `.csv`, `.log`, `.docx`,
  `.xlsx`, `.pptx`, and text-layer `.pdf`.
- Unsupported extensions are recorded without modification.
- No-match inputs are verified.
- The exe launches the UI without a Python command.
- Manual sensitive samples can be processed.
- `skipped_unsupported.txt` is created.
- PDF Japanese replacement remains readable.
- UI recognition, sample single-file processing, development UI launch, and
  packaged exe launch timings are measured and recorded.

## Smoke Test Modes

- Normal test mode may skip packaged smoke checks when `dist/MaskingTool.exe` is
  absent.
- Distribution verification mode must fail if `dist/MaskingTool.exe` is absent.

## Out of Scope

- Installer creation
- Code signing
- Auto-update
- macOS or Linux packaging
