# Implementation Plan: UI改善とexe配布

**Branch**: `002-ui-exe-packaging` | **Date**: 2026-06-02 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-ui-exe-packaging/spec.md`

## Summary

Improve the existing Tkinter desktop UI into a calm work-oriented tool surface
with clear sections, progress, and completion status, then package the app as a
single Windows executable named `MaskingTool.exe`. Preserve the existing masking
behavior and verification coverage while adding package build, distribution
checks, explicit per-format regression gates, measured timing checks, and a
strict distribution verification mode for the executable path.

## Technical Context

**Language/Version**: Python 3.11+; current workspace uses Python 3.14.5

**Primary Dependencies**: Tkinter/ttk for UI; existing openpyxl, python-docx,
python-pptx, PyMuPDF dependencies for masking; PyInstaller for Windows one-file
exe packaging; pytest for automated tests

**Storage**: Local filesystem only; generated executable in `dist/MaskingTool.exe`;
build intermediates under `build/`

**Testing**: pytest for core and UI contract tests; explicit regression checks
for replacement-table loading, file-type detection, every supported extension,
unsupported extensions, no-match inputs, and skip-report generation; subprocess
smoke test for packaging command where available; normal smoke tests may skip
when `dist/MaskingTool.exe` is absent, while distribution verification mode must
fail if the executable is absent; manual verification checklist for the built exe

**Target Platform**: Windows desktop

**Project Type**: Single Python desktop utility with packaged executable output

**Performance Goals**: UI launches within 5 seconds in development mode; packaged
exe displays the main window within 15 seconds on a typical Windows workstation;
sample single-file run completes within 5 minutes; a user can identify required
selections and the start button within 30 seconds. These timings are measured
and recorded in the distribution checklist.

**Constraints**: Must create a single `MaskingTool.exe`; must not weaken the
file masking exclusions or supported-format behavior; must work when launched
outside the repository root; must keep Japanese paths selectable; must preserve
readable Japanese PDF replacement output; distribution verification mode must
fail when `dist/MaskingTool.exe` is missing.

**Scale/Scope**: UI polish and packaging on top of the existing local masking
feature; no web server, installer, auto-update, or code signing in this feature

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- PASS: Existing supported extensions and excluded content scope remain unchanged.
- PASS: Replacement source and irreversible deterministic replacement behavior
  remain unchanged.
- PASS: UI keeps file/folder selection, output folder, traversal mode, progress,
  and `skipped_unsupported.txt` result visibility.
- PASS: Python remains the implementation language; packaging uses Python build
  tooling without changing file-format handlers.
- PASS: Tests and distribution verification cover supported samples, skipped
  unsupported files, and PDF Japanese replacement readability.
- PASS: Distribution verification now explicitly covers replacement-table
  loading, file-type detection, all supported extensions, unsupported extensions,
  no-match inputs, skip-report generation, timing measurements, and missing-exe
  failure behavior.

## Project Structure

### Documentation (this feature)

```text
specs/002-ui-exe-packaging/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── ui-contract.md
│   └── packaging-contract.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── main.py
└── masking_tool/
    ├── __main__.py
    ├── ui.py
    └── packaging.py

packaging/
├── MaskingTool.spec
├── README.md
├── build_exe.ps1
└── distribution-checklist.md

tests/
├── contract/
│   ├── test_ui_layout_contract.py
│   └── test_packaging_contract.py
├── integration/
│   └── test_packaged_app_smoke.py
└── fixtures/
```

**Structure Decision**: Keep the existing Python desktop package. Add packaging
scripts/specs under `packaging/` so executable creation is repeatable and separate
from masking logic.

## Complexity Tracking

No constitution violations.

## Phase 0: Research

See [research.md](./research.md).

## Phase 1: Design & Contracts

See [data-model.md](./data-model.md), [quickstart.md](./quickstart.md),
[contracts/ui-contract.md](./contracts/ui-contract.md), and
[contracts/packaging-contract.md](./contracts/packaging-contract.md).

## Post-Design Constitution Check

- PASS: UI and packaging contracts preserve the existing masking workflow and
  `skipped_unsupported.txt` visibility.
- PASS: Packaging contract requires `MaskingTool.exe` single-file output and a
  verification path.
- PASS: Quickstart includes core tests before packaging, explicit per-format
  regression checks, measured timing checks, and manual exe validation after
  packaging.
- PASS: No first-version exclusions are removed or weakened.
