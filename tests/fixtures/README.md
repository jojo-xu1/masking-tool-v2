# Test Fixtures

Fixture helpers live in `tests/fixtures/create_fixtures.py`.

They generate:
- `機密情報検出結果.xlsx`
- `.txt`, `.csv`, `.log`
- `.docx`, `.xlsx`, `.pptx`
- text-layer `.pdf`
- scanned-like `.pdf`
- unsupported files created directly inside tests

Use the helpers from tests instead of committing generated binary fixtures.
