# Data Model: PDF Textbox Fit Preservation

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
- Replacement proposals must be written exactly as supplied when a replacement
  is performed.

## PDF Text Region

Represents a supported visible text area in a text-based PDF where replacement
is attempted.

Fields:
- `source_path`: source PDF path.
- `page_number`: one-based PDF page position.
- `region_bounds`: original visible text span or text-box region bounds.
- `original_text`: in-scope text contained in the region.
- `original_font_size`: font size observed in the source PDF region.
- `replacement_text`: text after applying matched replacement rules.

Validation rules:
- Only extractable text-layer PDF spans are PDF text regions for this feature.
- Image text, scanned PDFs, embedded objects, and OCR-dependent content are not
  PDF text regions for this feature.
- The original page region and original font size are the preferred boundaries
  for readable replacement.

## PDF Layout Attempt

Represents one attempt to place replacement text in a PDF text region.

Fields:
- `replacement_text`: label derived from matched replacement rules.
- `available_region`: original PDF text region bounds.
- `font_size`: original font size selected for replacement.
- `readable`: whether the replacement is expected to be readable in the region.
- `fits_page_region`: whether the replacement stays within the original page
  region at the original font size.

Validation rules:
- Layout attempts must not reintroduce original detected phrases.
- Layout attempts must preserve original font size before recording a warning.
- Layout attempts must not mark the entire file as failed when only a region
  needs review.
- Layout attempts must be deterministic for the same input and replacement
  table.

## Layout Warning

Represents a reportable condition that a PDF region may require manual review.

Fields:
- `relative_path`: processed PDF path relative to the selected input.
- `region_reference`: enough location detail for the user to find the problem,
  such as page number and region description.
- `reason`: readable explanation of why layout review is needed.

Validation rules:
- Warnings are recorded through existing result messages and
  `skipped_unsupported.txt`.
- Warnings must not claim unsupported or excluded content was successfully
  masked.
- Warnings do not allow original matched in-scope phrases to remain in output.

## Processed Output

Represents the written output PDF and result reporting.

Fields:
- `source_path`: original input path.
- `output_path`: output PDF path under the selected output folder.
- `replacement_count`: number of visible matched phrases replaced.
- `messages`: PDF layout warnings or safety notes.
- `status`: existing processing category such as replaced, no-match, skipped,
  or failed.

Validation rules:
- Original input files must not be overwritten.
- Original detected phrases must be absent from matched in-scope output text.
- Existing skip-report and unsupported-content behavior remains intact.

## State Transitions

```text
Supported Text-Layer PDF Discovered
  -> PDF Text Regions Identified
  -> Replacement Rules Applied Deterministically
  -> Original-Font Layout Attempt Made In Original Page Region
  -> Readable Output Saved OR Replacement Saved With Layout Warning
  -> Output/report messages available
```
