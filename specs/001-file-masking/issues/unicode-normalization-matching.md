## Summary

Unicode matching defect: replacement can fail when detected phrases imported
from Excel contain Japanese IME/full-width forms while the target document uses
ASCII half-width forms, or the reverse.

## Reproduction

1. Prepare `機密情報検出結果.xlsx` using Japanese input/import behavior in Excel.
2. Enter or import a detected phrase that contains ASCII-looking characters,
   such as an English company name, code, email-like token, or phone-like token.
3. Confirm Excel stores some characters as full-width/CJK-compatible forms
   instead of ASCII half-width forms.
4. Prepare a supported target file where the visible text uses the other Unicode
   form, for example half-width `Technologies, Inc.` versus full-width
   `Ｔｅｃｈｎｏｌｏｇｉｅｓ， Ｉｎｃ．`.
5. Run masking with the replacement table.

## Expected

- Matching behavior is Unicode-aware for in-scope text.
- Semantically equivalent full-width and half-width forms can be matched when
  they differ only by Unicode compatibility width.
- The detected phrase is replaced with the corresponding `置換提案`.
- CJK characters remain intact and are not corrupted by normalization.
- Replacement remains deterministic and does not create reversible mappings.

## Actual

The phrase can remain unmasked because matching currently compares raw string
forms. If Excel stores full-width ASCII-compatible characters but the document
contains half-width ASCII, or vice versa, the raw strings do not match even
though they are visually/semantically equivalent for the user.

## Impact

This is high priority because Japanese Excel workflows can introduce full-width
ASCII-compatible characters during input or import. A user may believe a phrase
is covered by the replacement table, while supported output files still contain
the unmasked half-width or full-width variant.

## Fix

- Define a Unicode normalization strategy for matching, likely compatibility
  width normalization for comparison.
- Preserve output replacement values exactly as provided in `置換提案`.
- Avoid corrupting CJK-only text or changing unrelated output content.
- Add regression fixtures covering Excel-imported/full-width forms and
  half-width document forms.
- Confirm behavior across supported text and Office formats at minimum.

## Acceptance Criteria

- A replacement table detected phrase containing full-width ASCII-compatible
  characters matches a target file containing the half-width equivalent.
- A replacement table detected phrase containing half-width ASCII matches a
  target file containing the full-width equivalent.
- Japanese/CJK characters remain readable and unchanged except where explicitly
  replaced by a matching rule.
- Replacement proposals are written exactly as provided in `置換提案`.
- Existing deterministic overlap behavior still passes.
- Full test suite passes.
