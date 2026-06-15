## Summary

High-priority text-layer PDF masking defect: replacement text inserted into a
PDF text box can become visually larger or occupy more space than the original
text, so content that fit on one page before masking no longer fits or becomes
hard to review after masking.

## Reproduction

1. Prepare a text-based PDF where visible text is laid out inside a constrained
   text box or fixed page region.
2. Ensure the source page displays correctly on one page before masking.
3. Use `機密情報検出結果.xlsx` with a `検出語句` in that PDF region and a
   `置換提案` value that should replace it.
4. Run masking for the PDF.
5. Open the output PDF and compare the same page with the source PDF.

## Expected

- The detected phrase is removed from the text-layer PDF output.
- The replacement proposal remains readable inside the original page region
  when possible.
- The replacement step does not enlarge text or consume extra layout space in a
  way that pushes formerly one-page content out of the page.
- If the replacement cannot be kept readable inside the original PDF text
  region, the result records a clear layout warning instead of silently
  producing an unusable PDF.
- Scanned PDFs, image text, embedded objects, and OCR-dependent content remain
  out of scope and reportable.

## Actual

When replacing text in a PDF, the replacement output can appear larger than the
original text-box content. A source PDF that was readable and contained on one
page can become visually overflowing or no longer fit cleanly after masking.

The current PDF replacement path redacts matched text and reinserts replacement
text into a derived rectangle. That insertion may not preserve the original
font size, text box constraints, or page-fit behavior closely enough for fixed
PDF layouts.

## Impact

This is high priority because text-based PDF is a supported masking target.
Even if sensitive text is technically removed, a PDF that no longer fits in its
original page layout is difficult to review, print, or deliver. The user may
also lose confidence that masking preserved the document safely.

## Fix

- Add a regression fixture for a text-layer PDF with constrained text-box style
  layout that fits on one page before masking.
- Update PDF replacement to attempt in-region fitting before warning, using a
  font size and insertion rectangle that preserves the original page layout as
  much as possible.
- Avoid expanding the replacement rectangle in a way that causes visible
  overflow beyond the original page region unless a warning is recorded.
- Record a clear layout warning through existing result messages and
  `skipped_unsupported.txt` when a readable in-region PDF replacement cannot be
  guaranteed.
- Keep scanned PDFs, image text, embedded objects, and OCR-dependent content out
  of scope.

## Acceptance Criteria

- A constrained text-layer PDF fixture that fits on one page before masking is
  added.
- Replacing text in that fixture keeps the replacement readable and within the
  original page region when possible.
- The output PDF does not contain the original detected phrase in in-scope text.
- Overflow or unreadable PDF replacement regions produce a clear layout warning
  instead of silently producing a visually broken output.
- Existing PDF Japanese-text, scanned-PDF exclusion, deterministic replacement,
  and skip-report tests still pass.
