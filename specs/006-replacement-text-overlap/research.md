# Research: Replacement Text Overlap Prevention

## Decision: Prioritize `.pptx` visual containers for the first fix

Rationale: The reported screenshot shows a presentation-style diagram with text
inside a fixed blue box. Existing `.pptx` replacement already traverses text
frames and table-cell paragraphs, so this is the most direct path to reproduce
and fix the overlap without expanding scope.

Alternatives considered:
- Apply new layout behavior to all formats equally: rejected because flowing
  text formats do not have visual overlap concerns, and text-layer PDF layout
  has different redaction geometry constraints.
- Treat the screenshot as unsupported image text: rejected because the visible
  text appears to be normal in-scope shape/text-box text.

## Decision: Preserve the original visual region before warning

Rationale: Clarification selected fitting replacement labels within the original
visual region first. This preserves document structure and avoids moving or
resizing shapes in a way that could break diagrams. If a readable result cannot
be guaranteed, a warning is safer than silently producing overlapping output.

Alternatives considered:
- Always expand or move shapes: rejected because it can alter diagrams and
  create new overlaps with surrounding content.
- Always warn when replacement text is longer than the original: rejected
  because many labels can still be made readable by layout adjustments within
  the original region.

## Decision: Keep warning reporting in existing result messages

Rationale: Existing processing results already carry messages that are written
to `skipped_unsupported.txt` as `skipped_unsupported` entries even when the file
was otherwise processed. Reusing this reporting path keeps user visibility
consistent and avoids introducing a new report artifact.

Alternatives considered:
- Create a separate layout warning report: rejected because the constitution
  already anchors user review around processed files plus
  `skipped_unsupported.txt`.
- Mark the whole file as failed when one region needs layout review: rejected
  because the spec requires successfully readable regions to remain successful.

## Decision: Use fixture-based visual validation

Rationale: Visual overlap must be tested with a fixture that mirrors the
screenshot: multiple nearby phrases inside the same diagram/text-box area.
Programmatic validation can check that replacement labels are assigned distinct
readable regions and that warnings appear when the fixture is intentionally too
small.

Alternatives considered:
- Manual-only validation: rejected because this bug is user-visible and should
  have a repeatable regression test.
- Pixel-perfect visual diff: rejected for first pass because Office rendering
  can vary across environments; structural/readability assertions are more
  stable.

## Decision: Preserve existing replacement semantics

Rationale: The layout fix changes how replacement text is arranged inside a
visual region, not which phrases match. Deterministic ordering, Unicode width
matching, split-run replacement, original-phrase absence, and no reversible
mappings remain governed by existing shared replacement behavior.

Alternatives considered:
- Add layout-specific matching order: rejected because it risks diverging from
  supported format behavior and reintroducing inconsistent masking.
