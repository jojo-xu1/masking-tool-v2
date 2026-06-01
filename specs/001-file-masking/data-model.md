# Data Model: 機密文字列ファイルマスキング

## ReplacementTable

Represents the user-selected spreadsheet that defines all masking rules.

Fields:
- `path`: Absolute path to the selected spreadsheet.
- `rules`: Ordered list of validated `ReplacementRule` records.
- `source_headers`: Headers found in the first row.

Validation:
- Must contain `No`, `検出語句`, and `置換提案`.
- Must contain at least one valid replacement rule.
- Invalid rows stop processing before any target file is changed or copied.

## ReplacementRule

Represents one row from `機密情報検出結果.xlsx`.

Fields:
- `no`: Value from `No`, used for traceability and deterministic ordering.
- `detected_phrase`: Value from `検出語句`.
- `replacement_proposal`: Value from `置換提案`.
- `row_index`: Original spreadsheet row number.

Validation:
- `detected_phrase` must not be blank.
- `replacement_proposal` must not be blank.
- Duplicate `detected_phrase` values are invalid.

Ordering:
- Sort by descending `detected_phrase` length.
- Then sort by ascending `no` when comparable.
- Then sort by ascending `row_index`.

## InputSelection

Represents the target chosen by the user.

Fields:
- `mode`: `single_file` or `folder`.
- `input_path`: Absolute selected file or folder path.
- `traversal_mode`: `direct_children` or `recursive`; required for folder mode.
- `output_directory`: Absolute output folder path selected by the user.

Validation:
- `input_path` must exist and be readable.
- `output_directory` must be writable or creatable.
- `traversal_mode` is ignored for single-file mode.

## InputTarget

Represents one file considered for processing.

Fields:
- `source_path`: Absolute file path.
- `relative_path`: Path relative to selected input root.
- `extension`: Lowercase file extension.
- `support_status`: `supported`, `unsupported_extension`, `excluded_content`,
  or `unprocessable`.
- `reason`: Human-readable reason for skipped or failed files.

Validation:
- Supported extensions are `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`,
  and `.pdf`.
- `.pdf` also requires a text layer and searchable replacement locations.

## ProcessingResult

Represents the outcome for one `InputTarget`.

Fields:
- `target`: Associated input target.
- `status`: `replaced`, `processed_no_matches`, `skipped_unsupported`, or
  `failed`.
- `output_path`: Path to the produced file when status is `replaced` or
  `processed_no_matches`.
- `replacement_count`: Number of replacements applied.
- `messages`: List of warnings or notes for the user.

State transitions:
- `discovered` -> `supported` -> `replaced`
- `discovered` -> `supported` -> `processed_no_matches`
- `discovered` -> `unsupported_extension` -> `skipped_unsupported`
- `discovered` -> `excluded_content` -> `skipped_unsupported`
- `discovered` -> `supported` -> `failed`

## SkipReport

Represents `skipped_unsupported.txt`.

Fields:
- `output_path`: Path to the report in the output directory.
- `entries`: Ordered list of `SkipReportEntry`.

Validation:
- Report must be created for every run.
- Entries must be stable across identical input and replacement-table runs.

## SkipReportEntry

Represents one line in `skipped_unsupported.txt`.

Fields:
- `relative_path`: Input-relative file path.
- `status`: `skipped_unsupported` or `failed`.
- `reason`: Unsupported extension, excluded content, or processing failure.

Validation:
- Unsupported extensions must use status `skipped_unsupported`.
- Scanned PDFs, image-text-only PDFs, and OCR-dependent content must use status
  `skipped_unsupported`.
