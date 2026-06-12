# Quickstart: DOCX/PPTX Split Text Replacement

## Prerequisites

- Install project test dependencies in the existing development environment.
- Use a valid replacement table with `No`, `検出語句`, and `置換提案`.
- Include a row mapping `Technologies, Inc.` to an irreversible replacement
  value such as `会社名_置換済み`.

## Validation Steps

1. Add or update generated fixture helpers for:
   - `.docx` paragraph split across runs.
   - `.docx` table-cell paragraph split across runs.
   - `.pptx` text-box paragraph split across runs.
   - `.pptx` table-cell paragraph split across runs.
2. Run the Office integration tests:

   ```powershell
   python -m pytest tests/integration/test_single_office_files.py
   ```

3. Confirm each output Office file:
   - Does not contain `Technologies, Inc.` in visible in-scope body text.
   - Contains the replacement proposal.
   - Displays the replacement proposal using the first visible matched portion's
     `bold`, `italic`, font size, and color.
   - Counts each visible matched split phrase as one replacement.
4. Run deterministic rerun coverage for affected Office inputs:

   ```powershell
   python -m pytest tests/integration/test_deterministic_rerun.py
   ```

5. Run the full test suite before completion:

   ```powershell
   python -m pytest
   ```

## Manual Safety Check

1. Process a `.docx` or `.pptx` with an embedded object and a normal visible
   split phrase.
2. Confirm visible body text is masked.
3. Confirm embedded-object content is not treated as masked and existing safety
   notes remain visible through result reporting and `skipped_unsupported.txt`.

## Validation Results

- `python -m pytest tests/integration/test_office_split_run_replacement.py`
  passed.
- `python -m pytest tests/integration/test_single_office_files.py tests/integration/test_excluded_office_scope.py tests/integration/test_deterministic_rerun.py`
  passed.
- `python -m pytest` passed with 66 tests.

## Expected Result

The feature is complete when all required Office split-run cases pass, existing
Office replacement tests still pass, original input files are not overwritten,
and no excluded content is reported as successfully masked.
