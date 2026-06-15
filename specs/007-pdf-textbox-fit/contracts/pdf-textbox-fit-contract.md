# Contract: PDF Textbox Fit Preservation

## Scope

This contract covers page-fit preservation for supported text-layer PDF
replacement regions.

In scope:
- Text-based `.pdf` files with extractable visible text.
- PDF regions whose detected phrases can be matched by replacement rules.
- One-page constrained PDF layouts that fit before masking.
- Layout warnings for regions that cannot fit replacement text at the original
  font size.

Out of scope:
- Image text.
- Scanned PDFs.
- Embedded objects.
- OCR-dependent content.
- Expanding replacement text beyond the original page region to force fit.

## Replacement Input Contract

Given:
- A valid replacement table with headers `No`, `検出語句`, and `置換提案`.
- A supported text-layer PDF containing a detected phrase in a constrained page
  region.
- Replacement proposals that must remain exact and irreversible.

The system MUST:
- Replace matched in-scope visible phrases.
- Preserve the original font size for replacement text when it fits inside the
  original page region.
- Keep the output page count stable for fit-safe one-page fixtures.
- Preserve deterministic matching and replacement count behavior.
- Record a layout warning when replacement cannot be guaranteed to fit at the
  original font size.

## Output Contract

For fit-safe PDF regions:
- Output extracted text MUST contain the replacement proposal.
- Output extracted text MUST NOT contain the original detected phrase for the
  matched in-scope location.
- Replacement text MUST remain readable within the original page region at the
  original font size.
- A one-page fit-safe input remains a one-page output.
- The file remains a successful processed output.

For regions that cannot fit at the original font size:
- The matched original detected phrase MUST be removed from in-scope output.
- The replacement proposal MUST be applied.
- The result MUST record a layout warning that identifies the file and page or
  region.
- Other fit-safe regions in the same file MUST remain successful.
- The warning MUST be visible through existing output reporting and
  `skipped_unsupported.txt`.

For excluded content:
- Unsupported or excluded content remains unprocessed.
- Image text, scanned PDFs, embedded objects, and OCR-dependent content remain
  reportable according to existing behavior.

## Required Verification Cases

- One-page text-layer PDF with a constrained text region that fits before and
  after masking at original font size.
- Longer replacement label that still fits at original font size.
- Overflow case that records a layout warning while removing the original
  detected phrase.
- Mixed case where one PDF region is fit-safe and another requires warning.
- Regression: Japanese PDF replacement text remains readable.
- Regression: scanned or image-only PDF remains excluded.
- Regression: deterministic rerun outputs and counts remain stable.
- Regression: skip-report entries include PDF layout warnings.
