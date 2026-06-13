# Data Model: Unicode Normalization Matching

## Replacement Rule

Represents one row from `機密情報検出結果.xlsx`.

Fields:
- `No`: row identifier from the replacement table.
- `検出語句`: raw detected phrase exactly as read from the replacement table.
- `置換提案`: irreversible replacement value exactly as read from the
  replacement table.
- `row_index`: physical row position used by existing deterministic ordering.

Validation rules:
- Required headers remain `No`, `検出語句`, and `置換提案`.
- Blank or duplicate raw detected phrases remain invalid according to existing
  replacement table validation.
- Raw replacement proposal values must not be normalized or rewritten.

## Width-Equivalent Match Key

Represents the comparison-only form of a string where ASCII-compatible
full-width and half-width differences are treated as equivalent.

Fields:
- `source_text`: original raw string.
- `comparison_text`: comparison-only string used for matching.
- `index_map`: relationship from comparison positions back to raw source spans.

Validation rules:
- CJK characters and unrelated visually similar Unicode characters remain
  distinct unless they are part of the ASCII-compatible width behavior.
- The key is never written to output files.
- The key must preserve enough span information to replace the original visible
  target text, not the comparison text.

## Match Candidate

Represents one possible rule application against an in-scope text segment.

Fields:
- `replacement_rule`: rule that produced the candidate.
- `match_type`: `exact_raw` or `width_equivalent`.
- `start_index`: raw visible target start position.
- `end_index`: raw visible target end position.
- `replacement_proposal`: exact value to write.
- `precedence`: exact raw matches first, then existing deterministic rule order.

Validation rules:
- Exact raw candidates always win over width-equivalent candidates for the same
  visible target span.
- If no exact raw candidate applies, existing deterministic rule ordering
  resolves width-equivalent overlaps and duplicates.
- One visible matched phrase increments replacement count by one.

## In-Scope Text Segment

Represents visible text where replacement is allowed.

Types:
- `.txt`, `.csv`, and `.log` file text.
- `.docx` paragraph and table-cell paragraph text.
- `.xlsx` string cell text.
- `.pptx` text-box paragraph and table-cell paragraph text.
- Text-layer `.pdf` page text that can be located for redaction/replacement.

Fields:
- `visible_text`: raw visible text for matching and output span replacement.
- `format`: source extension or text container family.
- `location`: file path plus format-specific location such as page, sheet,
  paragraph, table cell, or slide.

Validation rules:
- Matching must not expand into image text, scanned PDFs, embedded objects, or
  OCR-dependent content.
- Format-specific structure and existing replacement boundaries remain
  unchanged.

## Processed Output

Represents a generated output file and its result reporting.

Fields:
- `source_path`: original input path.
- `output_path`: output file path under the selected output folder.
- `replacement_count`: number of visible matched phrases replaced.
- `messages`: safety notes or processing messages.
- `status`: existing processing category such as replaced, no-match, skipped,
  or failed.

Validation rules:
- Original input files must not be overwritten.
- Output files must not contain the original visible sensitive text for matched
  in-scope spans.
- `skipped_unsupported.txt` continues to record unsupported or excluded content.

## State Transitions

```text
Replacement Table Loaded
  -> Replacement Rules Ordered Deterministically
  -> In-Scope Text Segment Identified
  -> Exact Raw Candidates Evaluated
  -> Width-Equivalent Candidates Evaluated If Needed
  -> Original Visible Spans Replaced With Exact Proposals
  -> Processed Output Saved and Reported
```
