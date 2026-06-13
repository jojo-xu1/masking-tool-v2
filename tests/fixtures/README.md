# Test Fixtures

Fixture helpers live in `tests/fixtures/create_fixtures.py`.

They generate:
- `機密情報検出結果.xlsx`
- `.txt`, `.csv`, `.log`
- `.docx`, `.xlsx`, `.pptx`
- split-run `.docx` and `.pptx` samples where `Technologies, Inc.` is stored
  across Office text runs
- Unicode width normalization samples where full-width ASCII-compatible
  `検出語句` values match half-width targets, and half-width `検出語句` values
  match full-width targets
- text-layer `.pdf`
- scanned-like `.pdf`
- unsupported files created directly inside tests

Use the helpers from tests instead of committing generated binary fixtures.

Generate manual split-run Office samples with:

```powershell
python -m tests.fixtures.create_split_run_samples
```

Generated split-run samples are written under
`tests/fixtures/inputs/split_run_samples/`, with replacement table
`tests/fixtures/replacement_tables/機密情報検出結果_split_run.xlsx`.

Generate manual Unicode width samples with:

```powershell
python -m tests.fixtures.create_unicode_normalization_samples
```

Generated Unicode samples are written under
`tests/fixtures/inputs/unicode_normalization_samples/`, with replacement table
`tests/fixtures/replacement_tables/機密情報検出結果_unicode_width.xlsx`.
