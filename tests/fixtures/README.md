# Test Fixtures

Fixture helpers live in `tests/fixtures/create_fixtures.py`.

They generate:
- `機密情報検出結果.xlsx`
- `.txt`, `.csv`, `.log`
- `.docx`, `.xlsx`, `.pptx`
- split-run `.docx` and `.pptx` samples where `Technologies, Inc.` is stored
  across Office text runs
- replacement-layout `.pptx` samples with screenshot-style diagram text,
  constrained text boxes, table cells, overflow warning regions, and mixed
  readable-plus-warning regions
- Unicode width normalization samples where full-width ASCII-compatible
  `検出語句` values match half-width targets, and half-width `検出語句` values
  match full-width targets
- PDF textbox-fit samples with constrained text-layer spans, original-font
  replacements, overflow warning regions, mixed regions, and Japanese text
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

Replacement layout tests use in-test generated fixtures from:

```powershell
python -m tests.fixtures.create_replacement_layout_samples
```

The helper module exposes fixture builders for readable diagram/text-box/table
cell cases and intentionally unreadable overflow cases. Tests create these
files under their temporary directories instead of committing generated binary
fixtures.

Generate manual PDF textbox-fit samples with:

```powershell
python -m tests.fixtures.create_pdf_textbox_fit_samples
```

Generated PDF textbox-fit samples are written under
`tests/fixtures/inputs/pdf_textbox_fit_samples/`, with replacement table
`tests/fixtures/replacement_tables/機密情報検出結果_pdf_textbox_fit.xlsx`.
Tests usually create these files under temporary directories instead of
committing generated binary fixtures.
