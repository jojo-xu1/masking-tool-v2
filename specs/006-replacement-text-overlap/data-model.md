# Data Model: Replacement Text Overlap Prevention

## Replacement Rule

Represents one row from `機密情報検出結果.xlsx`.

Fields:
- `No`: row identifier from the replacement table.
- `検出語句`: detected phrase to match.
- `置換提案`: irreversible replacement label to write.
- `row_index`: physical row position used by deterministic ordering.

Validation rules:
- Required headers remain `No`, `検出語句`, and `置換提案`.
- Existing validation for blank or duplicate detected phrases remains unchanged.
- Replacement proposals must be written exactly as supplied.

## Visual Text Region

Represents a supported visible text area with fixed or constrained layout.

Types:
- `.pptx` shape text frame.
- `.pptx` text box.
- `.pptx` table-cell text frame.
- Future evaluated regions such as `.docx` text boxes or text-layer `.pdf`
  rectangles, if they are confirmed in scope during implementation.

Fields:
- `source_path`: source file path.
- `slide_index`: presentation slide position when applicable.
- `region_kind`: shape, text box, or table cell.
- `region_bounds`: visual area available for replacement labels.
- `visible_text`: in-scope text contained in the region.

Validation rules:
- Image text, embedded objects, scanned PDFs, and OCR-dependent content are not
  visual text regions for this feature.
- The original visual region is preserved as the preferred boundary for
  readability attempts.

## Layout Attempt

Represents one attempt to arrange replacement labels inside the original visual
region.

Fields:
- `replacement_labels`: labels derived from matched replacement rules.
- `available_region`: original visual region bounds.
- `layout_strategy`: the selected in-region adjustment, such as preserving
  existing placement, wrapping, fitting, or reducing text size.
- `readable`: whether labels are expected to be readable and non-overlapping.

Validation rules:
- Layout attempts must not reintroduce original detected phrases.
- Layout attempts must not mark the entire file as failed when only a region
  needs review.
- Layout attempts must be deterministic for the same input and replacement
  table.

## Layout Warning

Represents a reportable condition that a visual region may require manual
review.

Fields:
- `relative_path`: processed file path relative to the selected input.
- `region_reference`: enough location detail for the user to find the problem,
  such as slide number and shape/table-cell description.
- `reason`: readable explanation of why layout review is needed.

Validation rules:
- Warnings are recorded through existing result messages and
  `skipped_unsupported.txt`.
- Warnings must not claim unsupported content was successfully masked.

## Processed Output

Represents the written output file and result reporting.

Fields:
- `source_path`: original input path.
- `output_path`: output file path under the selected output folder.
- `replacement_count`: number of visible matched phrases replaced.
- `messages`: layout warnings or safety notes.
- `status`: existing processing category such as replaced, no-match, skipped,
  or failed.

Validation rules:
- Original input files must not be overwritten.
- Original detected phrases must be absent from matched in-scope output text.
- Existing skip-report and unsupported-content behavior remains intact.

## State Transitions

```text
Supported Visual Input Discovered
  -> Visual Text Regions Identified
  -> Replacement Rules Applied Deterministically
  -> Layout Attempt Made Within Original Region
  -> Readable Output Saved OR Layout Warning Recorded
  -> Processed Output and skip-report messages available
```
