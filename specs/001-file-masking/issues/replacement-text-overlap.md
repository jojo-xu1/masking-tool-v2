## Summary

Visual replacement layout defect: replacement output text can overlap nearby
or original content in diagram-like Office/PDF layouts, making the masked result
hard to read and potentially leaving the user unsure whether masking succeeded.

## Reproduction

1. Prepare a supported target file containing a diagram, shape, text box, or
   other fixed-size visual layout.
2. Include multiple detected phrases close together inside the same visual
   region, such as several `担当者...` values and a company label inside a
   PowerPoint-like box.
3. Use `機密情報検出結果.xlsx` with `検出語句` rows for those visible phrases and
   replacement proposals such as role labels or company labels.
4. Run masking.
5. Open the replaced output file and inspect the visual layout.

## Expected

- Replaced text remains readable in the output file.
- Replacement proposals do not overlap each other, the original text, or nearby
  visible labels inside the same shape/diagram region.
- Masking still removes the original detected phrase from in-scope text.
- Existing unsupported/excluded content reporting remains unchanged.

## Actual

As shown in the attached screenshot, replacement strings can be drawn on top of
nearby text inside the same blue diagram/shape area. Several replacement labels
appear to occupy the same visual line and overlap, so the output is difficult to
read even though text replacement may have been applied.

## Impact

This is high priority for user-facing document quality. Even when sensitive
text is technically replaced, overlapped replacement labels make the output
unusable for review or delivery and may cause users to suspect that masking was
incomplete.

## Fix

- Add a regression fixture that reproduces tightly spaced diagram or shape text
  where multiple replacement labels are close together.
- Define expected layout behavior for replaced text in fixed-size visual
  containers: for example, clear the original text region fully, preserve text
  inside the original bounds when possible, shrink replacement font, wrap text,
  or record an explicit layout warning when a readable replacement cannot be
  guaranteed.
- Verify the behavior for `.pptx` text boxes/shapes first, and evaluate whether
  the same visual-overlap risk exists for `.docx` text boxes or text-layer
  `.pdf` replacements.
- Keep image text, embedded objects, scanned PDFs, and OCR-dependent content out
  of scope unless a later feature changes the supported scope.

## Acceptance Criteria

- A fixture matching the screenshot-style diagram/text-box layout is added.
- Replacing multiple close text items does not produce overlapping visible
  replacement labels in the supported in-scope output.
- Original detected phrases are absent from in-scope output text.
- If a readable layout cannot be guaranteed for a supported visual container,
  the result records a clear warning rather than silently producing unusable
  output.
- Existing deterministic replacement, Unicode matching, split-run Office, and
  unsupported-content tests still pass.
