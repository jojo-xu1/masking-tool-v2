# Quickstart: Replacement Text Overlap Prevention

## Prerequisites

- Install project test dependencies in the existing development environment.
- Use a valid replacement table with `No`, `検出語句`, and `置換提案`.
- Include `.pptx` visual fixtures with multiple nearby detected phrases inside
  diagram-like shapes, text boxes, and table cells.

## Validation Steps

1. Add or update generated fixture helpers for:
   - Screenshot-style `.pptx` diagram box with close labels.
   - `.pptx` text box where replacement labels can fit in the original region.
   - `.pptx` table cell with constrained width.
   - Overflow case that cannot guarantee readable layout and must warn.
2. Run the layout contract tests:

   ```powershell
   .venv\Scripts\python.exe -m pytest tests/contract/test_replacement_layout_contract.py
   ```

3. Run focused visual-layout integration tests:

   ```powershell
   .venv\Scripts\python.exe -m pytest tests/integration/test_replacement_text_overlap.py
   ```

4. Run affected Office and reporting regressions:

   ```powershell
   .venv\Scripts\python.exe -m pytest tests/integration/test_office_split_run_replacement.py tests/integration/test_unicode_normalization_replacement.py tests/integration/test_deterministic_rerun.py tests/integration/test_folder_skip_report.py tests/integration/test_excluded_office_scope.py
   ```

5. Run the full test suite before completion:

   ```powershell
   .venv\Scripts\python.exe -m pytest
   ```

6. Run formatting validation:

   ```powershell
   git diff --check
   ```

## Manual Safety Check

1. Process a `.pptx` matching the screenshot-style layout.
2. Confirm replacement labels are readable and do not overlap inside the visual
   region.
3. Process an intentionally too-small visual region.
4. Confirm `skipped_unsupported.txt` records a layout warning that points to the
   affected file or region.
5. Confirm image text, scanned PDFs, embedded objects, and OCR-dependent content
   remain excluded and reportable.

## Expected Result

The feature is complete when screenshot-style replacement labels are readable,
overflow cases produce clear layout warnings, original detected phrases are
absent from in-scope output text, existing Unicode and split-run Office behavior
still passes, and full pytest plus `git diff --check` pass.

## Implementation Validation Notes

- Added generated `.pptx` layout fixtures for diagram, text-box/table-cell,
  overflow warning, and mixed readable-plus-warning cases.
- Layout warnings use existing result messages so `skipped_unsupported.txt`
  records the affected file, slide, and region without failing readable
  replacements in the same file.
- The first focused validation passed with:

  ```powershell
  .venv\Scripts\python.exe -m pytest --basetemp=.tmp\pytest tests/contract/test_replacement_layout_contract.py tests/integration/test_replacement_text_overlap.py tests/unit/test_office_replacer.py
  ```

- Affected Office/reporting regressions passed with:

  ```powershell
  .venv\Scripts\python.exe -m pytest --basetemp=.tmp\pytest tests/integration/test_office_split_run_replacement.py tests/integration/test_unicode_normalization_replacement.py tests/integration/test_deterministic_rerun.py tests/integration/test_folder_skip_report.py tests/integration/test_excluded_office_scope.py tests/integration/test_replacement_text_overlap.py tests/contract/test_replacement_layout_contract.py tests/unit/test_office_replacer.py
  ```
