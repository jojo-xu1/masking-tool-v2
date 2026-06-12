# Contract: Office Split Text Replacement

## Scope

This contract covers `.docx` and `.pptx` visible body text only.

In scope:
- `.docx` paragraphs.
- `.docx` table-cell paragraphs.
- `.pptx` text-box paragraphs.
- `.pptx` table-cell paragraphs.

Out of scope:
- Text spanning paragraph, text-box, or table-cell boundaries.
- Image text.
- Embedded objects.
- Scanned PDFs and OCR-dependent content.

Split-run matching MUST NOT cross paragraph, text-box, or table-cell boundaries.

## Replacement Input Contract

Given:
- A valid replacement table with headers `No`, `検出語句`, and `置換提案`.
- A rule where `検出語句` is `Technologies, Inc.`.
- A `.docx` or `.pptx` input where `Technologies, Inc.` appears as visible
  in-scope text but is internally split across Office text portions.

The system MUST:
- Match the visible phrase inside the same allowed Office Text Container.
- Replace it with the matching `置換提案`.
- Use deterministic rule ordering when overlapping detected phrases exist.

## Output Contract

For each matched visible split phrase:
- Output visible text MUST NOT contain `Technologies, Inc.` in that location.
- Output visible text MUST contain the replacement proposal in that location.
- Replacement text MUST use the `bold`, `italic`, font size, and color of the
  first visible portion of the matched phrase.
- Result reporting MUST count the visible matched phrase as one replacement,
  regardless of internal Office split count.

For non-matches:
- The file remains a successful processed output.
- Result reporting MUST NOT record a false replacement.

For excluded content:
- Embedded objects and image text remain out of scope.
- Detectable out-of-scope Office content is recorded in `skipped_unsupported.txt`
  even when visible split-run body text in the same file is successfully
  replaced.

## Required Verification Cases

- `.docx` paragraph: `Technologies` and `, Inc.` split across text portions.
- `.docx` table cell: `Technologies` and `, Inc.` split across text portions.
- `.pptx` text box: `Technologies` and `, Inc.` split across text portions.
- `.pptx` table cell: `Technologies` and `, Inc.` split across text portions.
- Formatting: replacement uses the first visible portion's `bold`, `italic`,
  font size, and color.
- Counting: one visible split phrase increments replacement count by one.
- Determinism: repeated processing with the same input and table produces the
  same visible output and count.
- Regression: existing unsplit Office replacement behavior remains valid.
