# Quickstart: Unicode Normalization Matching

## Prerequisites

- Install project test dependencies in the existing development environment.
- Use a valid replacement table with `No`, `検出語句`, and `置換提案`.
- Include fixtures where `検出語句` and target text differ only by
  ASCII-compatible full-width and half-width forms.

## Validation Steps

1. Add or update generated fixture helpers for:
   - Full-width `検出語句` with half-width target text.
   - Half-width `検出語句` with full-width target text.
   - Mixed CJK plus ASCII-compatible width differences.
   - Exact raw match precedence over width-equivalent matches.
   - Replacement proposals that intentionally contain full-width, half-width,
     punctuation, spacing, and CJK characters.
2. Run focused unit tests for replacement ordering and matching behavior:

   ```powershell
   python -m pytest tests/unit/test_text_replacer.py tests/unit/test_replacement_table.py
   ```

3. Run supported-format integration coverage:

   ```powershell
   python -m pytest tests/integration/test_single_text_files.py tests/integration/test_single_office_files.py tests/integration/test_single_pdf_file.py
   ```

4. Run deterministic and safety coverage:

   ```powershell
   python -m pytest tests/integration/test_deterministic_rerun.py tests/integration/test_no_reversible_mapping.py tests/integration/test_folder_skip_report.py tests/integration/test_excluded_pdf_scope.py tests/integration/test_excluded_office_scope.py
   ```

5. Run the Unicode normalization contract tests:

   ```powershell
   python -m pytest tests/contract/test_unicode_normalization_contract.py
   ```

6. Run the full test suite before completion:

   ```powershell
   python -m pytest
   ```

## Validation Results

- `.venv\Scripts\python.exe -m pytest tests/contract/test_unicode_normalization_contract.py tests/unit/test_text_replacer.py tests/integration/test_unicode_normalization_replacement.py`
  passed with 16 tests.
- `.venv\Scripts\python.exe -m pytest tests/unit/test_replacement_table.py tests/integration/test_deterministic_rerun.py tests/integration/test_no_reversible_mapping.py tests/integration/test_folder_skip_report.py tests/integration/test_excluded_pdf_scope.py tests/integration/test_excluded_office_scope.py tests/contract/test_ui_single_file_contract.py tests/contract/test_ui_folder_contract.py`
  passed with 18 tests.
- `.venv\Scripts\python.exe -m pytest tests/integration/test_single_text_files.py tests/integration/test_single_office_files.py tests/integration/test_single_pdf_file.py tests/integration/test_office_split_run_replacement.py tests/unit/test_office_replacer.py`
  passed with 11 tests.
- `.venv\Scripts\python.exe -m pytest` passed with 87 tests.
- `git diff --check` passed with CRLF conversion warnings only.

## Manual Safety Check

1. Process a folder containing supported Unicode width fixtures, an unsupported
   file, a scanned PDF, and Office files with detectable embedded objects.
2. Confirm supported visible text is masked in both full-width-to-half-width and
   half-width-to-full-width directions.
3. Confirm replacement proposals are written exactly as supplied.
4. Confirm non-matched CJK text remains unchanged.
5. Confirm excluded content is still recorded through result reporting and
   `skipped_unsupported.txt`.

## Expected Result

The feature is complete when all required width-equivalent matching cases pass,
exact raw match precedence is verified, existing deterministic behavior remains
valid, original input files are not overwritten, replacement proposals are
preserved exactly, and no excluded content is reported as successfully masked.
