# Research: UI改善とexe配布

## Decision: Keep Tkinter/ttk and redesign within the existing desktop stack

Rationale: The existing app already uses Tkinter and the feature asks for a
moderate, practical design improvement rather than a full UI rewrite. ttk
supports grouped frames, labels, progress bars, status labels, and buttons
without adding a new runtime that complicates packaging.

Alternatives considered:
- Web UI: rejected because the feature explicitly targets exe distribution and
  no server should be introduced.
- New desktop framework: rejected because it increases packaging risk before
  user value improves.

## Decision: Use a calm work-oriented layout

Rationale: The app handles confidential files, so the UI should prioritize
clarity, scanability, and status visibility. Grouped sections for inputs,
options, execution, and results reduce user mistakes.

Alternatives considered:
- Decorative modern UI: can look better but adds little value for a repeated
  operational workflow.
- Minimal spacing-only cleanup: too small to satisfy the design improvement
  request.

## Decision: Use PyInstaller one-file build for `MaskingTool.exe`

Rationale: The user clarified single exe distribution. PyInstaller is the most
common packaging route for Python desktop utilities and supports one-file
Windows executables.

Alternatives considered:
- Folder distribution: safer for debugging, but rejected by clarification.
- Installer package: outside the requested scope.
- Nuitka: powerful but heavier for this first packaging workflow.

## Decision: Add a packaging script and checked-in build spec

Rationale: Packaging should be repeatable. A script can create or reuse the
PyInstaller spec, clean stale build output, and place the expected artifact at
`dist/MaskingTool.exe`.

Alternatives considered:
- Manual command in README only: easy to drift and hard to test.
- Commit built exe: rejected because binary build outputs should not be versioned
  in the source repo.

## Decision: Validate packaged behavior with smoke and manual checks

Rationale: Automated tests can verify contract and build configuration, but GUI
exe launch behavior often depends on Windows shell/session constraints. Use an
automated packaging smoke test when possible and a required distribution
verification checklist for the actual exe.

Alternatives considered:
- Fully automated GUI testing: disproportionate for the first packaging pass.
- No exe validation: too risky because packaging failures are common.

## Decision: Use separate normal and distribution verification smoke modes

Rationale: Normal development test runs should remain useful before the exe is
built, so packaged smoke checks may skip when `dist/MaskingTool.exe` is absent.
Distribution verification is the release gate, so it must fail if the executable
is missing.

Alternatives considered:
- Always fail when the exe is absent: rejected because it makes routine test runs
  fail before packaging work is complete.
- Always skip when the exe is absent: rejected because it weakens the release
  gate and can hide a missing artifact.

## Decision: Treat per-format regression and timing checks as distribution gates

Rationale: The constitution requires format-specific test coverage and skip
report verification. The UI/exe timing criteria depend on the Windows desktop
session and are best recorded in a distribution checklist rather than enforced
by fragile GUI timing tests.

Alternatives considered:
- Only run `python -m pytest`: rejected because the release record would not show
  which constitutional checks were verified.
- Enforce every timing criterion in automated tests: rejected because GUI launch
  timing is environment-sensitive and would be noisy on developer machines.

## Decision: Preserve existing masking tests as regression gate

Rationale: UI and packaging changes must not weaken confidential data handling.
The existing test suite remains the baseline gate before packaging, and the
distribution checklist records the required per-format confirmations.

Alternatives considered:
- Only test packaging: rejected because packaging changes can accidentally break
  imports, resources, or runtime behavior.
