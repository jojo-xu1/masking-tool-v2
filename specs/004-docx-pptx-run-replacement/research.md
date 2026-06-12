# Research: DOCX/PPTX Split Text Replacement

## Decision: Match visible text at paragraph-level Office containers

Rationale: The defect occurs because a visible phrase such as
`Technologies, Inc.` can be stored across multiple Office runs. Matching each
run independently misses the phrase. Evaluating the visible text of one `.docx`
paragraph, one `.pptx` text-box paragraph, or one table-cell paragraph matches
the user-visible boundary clarified in the spec while avoiding replacement
across structural boundaries.

Alternatives considered:
- Run-only replacement: rejected because it is the current failing behavior.
- Whole-document replacement: rejected because it can cross paragraphs, cells,
  or text boxes and violates the clarified scope.
- Raw XML or binary replacement: rejected because the constitution requires
  format-specific structured APIs and format preservation.

## Decision: Reuse deterministic replacement rule ordering

Rationale: Existing text replacement already sorts and applies rules
deterministically for overlapping detected phrases. The Office split-run path
should reuse the same visible-text replacement semantics so `Technologies, Inc.`
and shorter overlapping phrases produce consistent results across formats.

Alternatives considered:
- Add Office-specific ordering: rejected because it risks diverging from text,
  PDF, and workbook behavior.
- Spreadsheet row order only: rejected because existing behavior already avoids
  shorter phrases corrupting longer matches.

## Decision: Use first matched visible portion formatting for replacement text

Rationale: The clarification selected the first visible portion's formatting.
This keeps replacement text legible, avoids trying to split a replacement label
across unrelated source styles, and provides concrete testable expectations for
`bold`, `italic`, font size, and color.

Alternatives considered:
- Preserve every source run's styling inside replacement text: rejected because
  replacement labels may not align with the source run boundaries and would make
  deterministic validation harder.
- Use default document or slide styling: rejected because it can visibly detach
  the replacement label from surrounding content.

## Decision: Count one visible split phrase as one replacement

Rationale: Users interpret replacement counts as matched visible phrases, not
internal Office run fragments. Counting one visible phrase as one replacement
keeps result reporting aligned with existing no-split text behavior.

Alternatives considered:
- Count each internal run fragment: rejected because a single visible phrase
  could inflate counts based on Office storage details.
- Exclude counts from this fix: rejected because result reporting is part of
  the existing user-visible contract.

## Decision: Record detectable out-of-scope Office content in skip report

Rationale: The feature fixes visible body text only. Detectable out-of-scope
Office content such as embedded objects or images must continue to warn users
that some content was not masked, even if visible split-run text in the same file
was successfully replaced.

Alternatives considered:
- Attempt embedded-object replacement: rejected as out of first-version scope.
- Suppress embedded-object notes when visible text succeeds: rejected because it
  would weaken safety reporting and conflict with the skip-report safety gate.
