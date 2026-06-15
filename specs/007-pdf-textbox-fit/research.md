# Research: PDF Textbox Fit Preservation

## Decision: Target text-layer PDF replacements only

Rationale: The reported defect occurs during supported text-based PDF
replacement. The constitution limits first-version PDF support to text-layer
PDFs, while image text, scanned PDFs, embedded objects, and OCR-dependent
content remain excluded and reportable.

Alternatives considered:
- Add OCR/image-text support: rejected because it expands the supported scope
  and conflicts with the current constitution.
- Treat all PDFs as unsupported when layout is constrained: rejected because
  text-layer PDF replacement is already supported and should remain useful.

## Decision: Preserve original PDF font size before warning

Rationale: Clarification selected preserving original font size as the first
priority. This directly addresses the user-visible problem where replacement
text appears larger or consumes extra page space after masking.

Alternatives considered:
- Shrink replacement text to force fit: rejected because the user selected font
  size preservation over automatic shrink.
- Expand the replacement region to fit longer text: rejected because it can
  break one-page layout and create new visual overflow.

## Decision: Replace sensitive text even when warning is needed

Rationale: Clarification selected removing the original detected phrase even
when the replacement cannot be guaranteed to fit at the original font size. This
preserves masking safety while surfacing layout review needs.

Alternatives considered:
- Leave the original text in place and warn: rejected because it leaves
  sensitive text in supported in-scope output.
- Fail the whole PDF and produce no output: rejected because fit-safe regions in
  the same file should remain useful and reportable.

## Decision: Reuse existing result messages for PDF layout warnings

Rationale: Existing processing results already carry messages that are written
to `skipped_unsupported.txt` as reportable entries even when the file was
otherwise processed. Reusing this path keeps user visibility consistent and
avoids a new report artifact.

Alternatives considered:
- Create a separate PDF layout warning report: rejected because users already
  review `skipped_unsupported.txt` for unsupported, excluded, and warning
  conditions.
- Mark the whole file as failed when one region needs layout review: rejected
  because the spec requires fit-safe regions to remain successful.

## Decision: Use fixture-based page-fit validation

Rationale: PDF page-fit regressions need repeatable text-layer fixtures that
fit before masking and can be inspected after masking. Programmatic validation
can check page count, extracted text, replacement presence, original phrase
absence, and warning messages.

Alternatives considered:
- Manual-only PDF inspection: rejected because the bug is user-visible and
  should have repeatable regression coverage.
- Pixel-perfect PDF rendering diff: rejected for the first pass because PDF
  rendering can vary across environments; structural and page-fit assertions
  are more stable.

## Decision: Preserve existing replacement semantics

Rationale: The page-fit fix changes how replacement text is inserted into PDF
regions, not which phrases match. Deterministic ordering, Unicode matching,
replacement-table validation, no reversible mappings, and unsupported reporting
remain governed by existing shared behavior.

Alternatives considered:
- Add PDF-specific matching order: rejected because it risks diverging from
  supported format behavior and reintroducing inconsistent masking.
