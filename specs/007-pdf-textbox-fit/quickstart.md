# Quickstart: PDF Textbox Fit Preservation

## Prerequisites

- Install project test dependencies in the existing development environment.
- Use a valid replacement table with `No`, `検出語句`, and `置換提案`.
- Include text-layer PDF fixtures with constrained visible text regions that
  fit on one page before masking.

## Validation Steps

1. Add or update generated fixture helpers for:
   - One-page constrained text-layer PDF that can fit replacement at the
     original font size.
   - Longer replacement label that still fits at the original font size.
   - Overflow case that cannot fit at the original font size and must warn.
   - Mixed case with one fit-safe region and one warning-required region.
2. Run the PDF page-fit contract tests:

   ```powershell
   .venv\Scripts\python.exe -m pytest tests/contract/test_pdf_textbox_fit_contract.py
   ```

3. Run focused PDF integration tests:

   ```powershell
   .venv\Scripts\python.exe -m pytest tests/integration/test_pdf_textbox_fit.py
   ```

4. Run affected PDF and reporting regressions:

   ```powershell
   .venv\Scripts\python.exe -m pytest tests/integration/test_single_pdf_file.py tests/integration/test_excluded_pdf_scope.py tests/integration/test_deterministic_rerun.py tests/integration/test_folder_skip_report.py tests/integration/test_no_reversible_mapping.py tests/integration/test_batch_performance.py
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

1. Process a text-layer PDF that fits on one page before masking.
2. Confirm the output remains one page and the replacement text is readable in
   the original page region at the original font size.
3. Process an intentionally too-small PDF text region.
4. Confirm the original detected phrase is absent and `skipped_unsupported.txt`
   records a layout warning that points to the affected PDF page or region.
5. Confirm scanned PDFs, image text, embedded objects, and OCR-dependent content
   remain excluded and reportable.

## Expected Result

The feature is complete when fit-safe text-layer PDF replacements preserve the
one-page layout and original font size, overflow cases still remove original
detected phrases while producing clear layout warnings, existing Japanese PDF
and scanned-PDF behavior still passes, and full pytest plus `git diff --check`
pass.
