## Summary

PDF replacement output can become mojibake when replacement proposals contain
Japanese text.

## Reproduction

1. Use a text-based PDF containing a detected phrase.
2. Use a replacement table where `置換提案` contains Japanese text, for example
   `電話番号_置換済み`.
3. Run PDF masking.
4. Open or extract text from the output PDF.

## Expected

- The detected phrase is removed from the output PDF.
- The Japanese replacement proposal remains readable.
- Extracted text does not contain mojibake replacement characters such as `�`.

## Actual

The previous PDF replacement path inserted replacement text through PyMuPDF
redaction annotation text, which can render Japanese replacement text
incorrectly depending on font handling.

## Fix

- Redact matched text with a white fill and no annotation replacement text.
- Insert replacement text after redaction using a CJK-capable font path.
- Add a regression test using Japanese replacement text.

## Acceptance Criteria

- `tests/integration/test_single_pdf_file.py::test_pdf_replacement_preserves_readable_japanese_text` passes.
- Full test suite passes.
- Scanned or image-text-only PDFs remain `skipped_unsupported`.
