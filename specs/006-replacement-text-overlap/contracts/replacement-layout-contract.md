# Contract: Replacement Layout Readability

## Scope

This contract covers readable replacement layout for supported fixed-size visual
text regions, primarily:

- `.pptx` shape text frames.
- `.pptx` text boxes.
- `.pptx` table-cell text frames.

Out of scope:

- Image text.
- Scanned PDFs.
- Embedded objects.
- OCR-dependent content.
- Moving or expanding unrelated visual objects outside the original visual
  region.

## Replacement Input Contract

Given:
- A valid replacement table with headers `No`, `検出語句`, and `置換提案`.
- A supported `.pptx` input containing multiple nearby detected phrases inside
  the same diagram-like visual region.
- Replacement proposals that must remain exact and irreversible.

The system MUST:
- Replace matched in-scope visible phrases.
- Attempt to keep replacement labels readable inside the original visual region.
- Prevent replacement labels from overlapping each other when the fixture has
  enough visual room.
- Preserve deterministic matching and replacement count behavior.

## Output Contract

For readable layout regions:
- Output visible text MUST contain the replacement proposals.
- Output visible text MUST NOT contain the original detected phrases for the
  matched in-scope locations.
- Replacement labels MUST remain readable and non-overlapping.
- The file remains a successful processed output.

For regions that cannot be made readable:
- The result MUST record a layout warning that identifies the file and region.
- Other readable regions in the same file MUST remain successful.
- The warning MUST be visible through existing output reporting and
  `skipped_unsupported.txt`.

For excluded content:
- Unsupported or excluded content remains unprocessed.
- Image text, scanned PDFs, embedded objects, and OCR-dependent content remain
  reportable according to existing behavior.

## Required Verification Cases

- Screenshot-style `.pptx` diagram box with multiple close replacement labels.
- `.pptx` text box where a replacement label is longer than the original text.
- `.pptx` table cell with constrained width.
- Overflow case that records a layout warning.
- Mixed case where one region is readable and another region requires warning.
- Regression: existing Unicode width matching still passes.
- Regression: existing split-run Office replacement still passes.
- Regression: deterministic rerun outputs and counts remain stable.
- Regression: unsupported and excluded content remains reportable.
