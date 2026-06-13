# Research: Unicode Normalization Matching

## Decision: Centralize width-equivalent matching semantics

Rationale: The same replacement table drives `.txt`, `.csv`, `.log`, `.docx`,
`.xlsx`, `.pptx`, and text-layer `.pdf` processing. A shared matching behavior
keeps raw-match precedence, width-equivalent matching, replacement counts, and
overlap handling consistent across formats.

Alternatives considered:
- Format-specific normalization in each replacer: rejected because it can
  diverge and create inconsistent masking results for the same input text.
- Replacement-table-only normalization: rejected because output proposals must
  remain exact and target text still needs raw span information for replacement.

## Decision: Fold only ASCII-compatible width differences for comparison

Rationale: The reported defect concerns Japanese Excel workflows that generate
full-width ASCII-compatible letters, digits, punctuation, and spaces. Matching
should treat those as equivalent to half-width ASCII while leaving CJK text and
unrelated visually similar Unicode characters unchanged.

Alternatives considered:
- Normalize all text broadly before replacement: rejected because it risks
  changing the meaning of non-target text and violating CJK preservation.
- Require users to duplicate full-width and half-width rows: rejected because it
  leaves a high-priority leak path in normal Japanese Excel workflows.

## Decision: Preserve original target spans and replacement proposal values

Rationale: The matcher needs comparison keys to find equivalent text, but the
writer must replace the original visible span and write `置換提案` exactly as
provided. This allows full-width table values to match half-width targets while
keeping output labels intentionally full-width, half-width, or CJK.

Alternatives considered:
- Write normalized replacement proposals: rejected because users own the
  replacement output and exact value preservation is a functional requirement.
- Normalize non-matched output text: rejected because unrelated text must remain
  unchanged.

## Decision: Exact raw matches win before width-equivalent matches

Rationale: Clarification selected exact raw match precedence. If a visible
target can match one row exactly and another row only after width folding, the
raw match better represents the user's explicit rule. If no raw match applies,
existing deterministic rule ordering resolves width-equivalent candidates.

Alternatives considered:
- Always use first normalized candidate: rejected because it can ignore a more
  explicit exact match.
- Treat width-equivalent duplicate rules as a hard error: rejected because the
  existing replacement table currently accepts raw-distinct detected phrases.

## Decision: Keep PDF support limited to text-layer matches with source text spans

Rationale: Text-layer PDFs are already in scope, while scanned PDFs, image text,
and OCR-dependent content are excluded. Width-equivalent PDF replacement should
operate only on extractable text-layer strings and should continue to report
excluded PDFs through existing behavior.

Alternatives considered:
- Add OCR or image-text matching: rejected by the constitution and feature
  scope.
- Skip PDF width-equivalent matching: rejected because the spec requires
  consistency across supported in-scope formats.
