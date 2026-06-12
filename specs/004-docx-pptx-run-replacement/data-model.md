# Data Model: DOCX/PPTX Split Text Replacement

## Replacement Rule

Represents one row from `機密情報検出結果.xlsx`.

Fields:
- `No`: row identifier from the replacement table.
- `検出語句`: detected phrase to match, including `Technologies, Inc.` for this
  regression.
- `置換提案`: irreversible replacement value, such as `会社名_置換済み`.

Validation rules:
- Required headers remain `No`, `検出語句`, and `置換提案`.
- Blank or duplicate detected phrases remain invalid according to existing
  replacement table validation.
- Rule application order remains deterministic for overlapping phrases.

## Office Text Container

Represents a visible in-scope text boundary where split-run matching is allowed.

Types:
- `.docx` paragraph.
- `.docx` table-cell paragraph.
- `.pptx` text-box paragraph.
- `.pptx` table-cell paragraph.

Fields:
- `visible_text`: concatenated visible text inside the same container.
- `text_portions`: ordered Office text portions that together form the visible
  text.
- `container_kind`: paragraph, text-box paragraph, or table-cell paragraph.
- `source_format_portion`: first visible portion of a matched phrase, used for
  replacement text `bold`, `italic`, font size, and color.

Validation rules:
- Matching MUST NOT cross paragraph, text-box, or table-cell boundaries.
- Image text, embedded objects, scanned PDFs, and OCR-dependent content are not
  Office Text Containers for this feature.

## Split-Run Match

Represents one matched visible phrase whose characters may span multiple Office
text portions.

Fields:
- `detected_phrase`: replacement rule phrase that matched visible text.
- `replacement_proposal`: replacement value to write.
- `start_index`: match start in the Office Text Container visible text.
- `end_index`: match end in the Office Text Container visible text.
- `covered_portions`: ordered text portions touched by the match.
- `replacement_count`: always `1` per visible matched phrase.

Validation rules:
- The output visible text MUST contain `replacement_proposal`.
- The output visible text MUST NOT contain the matched `detected_phrase`.
- The replacement text uses the first covered portion's `bold`, `italic`, font
  size, and color.

## Processed Office Output

Represents the written `.docx` or `.pptx` output file.

Fields:
- `source_path`: original Office input path.
- `output_path`: output file path under the selected output folder.
- `replacement_count`: sum of visible matched phrases.
- `notes`: safety notes such as embedded-object or image out-of-scope messages.
- `status`: existing processing category such as replaced, no-match, skipped,
  or failed.

Validation rules:
- Original input files MUST NOT be overwritten.
- Existing embedded-object notes remain present when applicable.
- Detectable out-of-scope Office content is recorded in `skipped_unsupported.txt`
  even when visible split-run body text is successfully replaced.
- Existing no-match behavior remains a successful processed output without a
  false replacement failure.

## State Transitions

```text
Discovered Office Input
  -> Valid Office Text Containers Identified
  -> Split-Run Matches Detected
  -> Replacement Text Written
  -> Processed Office Output Saved
  -> Result Summary and skip-report notes available
```
