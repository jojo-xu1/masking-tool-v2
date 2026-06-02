# Data Model: ユーザー向け操作手順書

## OperationGuide

Represents the complete user-facing guide.

Fields:
- `markdown_path`: Must be `docs/user-guide.md`.
- `pdf_path`: Must be `docs/user-guide.pdf`.
- `language`: Must be Japanese.
- `audience`: Business users who receive `MaskingTool.exe`.
- `sections`: Ordered list of guide sections.
- `source_is_markdown`: Must be true.
- `review_questions`: Questions embedded in the guide body for reader
  comprehension validation.
- `elapsed_time_fields`: Timing fields embedded in the guide body for
  single-file and folder sample runs.

Validation:
- Markdown and PDF artifacts must both exist for distribution.
- The PDF must be generated from the Markdown source.
- The PDF must be tracked as a distribution artifact.
- The guide must not require Python or build knowledge for normal operation.
- Review questions and elapsed-time fields must be present in the guide body.

## ProcedureSection

Represents one step-by-step guide section.

Fields:
- `title`: User-facing section title.
- `purpose`: What the user accomplishes in the section.
- `steps`: Ordered user actions.
- `expected_result`: What the user should see or confirm.

Required sections:
- Launch the tool.
- Select replacement table.
- Select a single file.
- Select a folder and traversal scope.
- Select output folder.
- Run masking.
- Confirm results.

## ScopeNote

Represents safety and scope statements.

Fields:
- `supported_extensions`: `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`,
  text-based `.pdf`.
- `excluded_content`: image text, scanned PDFs, embedded objects, OCR-dependent
  content.
- `replacement_table_headers`: `No`, `検出語句`, `置換提案`.
- `output_artifacts`: replaced files and `skipped_unsupported.txt`.

Validation:
- Supported and excluded scope must be explicit.
- The guide must explain that unsupported or unprocessable files are recorded,
  not silently treated as masked.

## TroubleshootingEntry

Represents one common problem and user action.

Fields:
- `symptom`: What the user sees.
- `likely_causes`: One or more likely causes.
- `user_action`: Safe next action for non-developer users.

Required entries:
- Missing required input.
- Invalid replacement table.
- Unsupported files or skipped entries.
- Processing failure.
- `MaskingTool.exe` launch failure.

## PreUseChecklist

Represents the final checklist before processing confidential files.

Fields:
- `items`: Confirmation items covering replacement table, input target, output
  folder, supported scope, excluded scope, and result review.

Validation:
- Checklist must be short enough for users to complete before each run.
- Checklist must include a reminder to review `skipped_unsupported.txt`.

## ReviewValidationSection

Represents the guide-body validation area for measurable outcomes.

Fields:
- `single_file_elapsed_time`: Field for recording sample single-file run time.
- `folder_elapsed_time`: Field for recording sample folder run time.
- `review_questions`: Questions covering supported scope, excluded scope,
  replacement table, output files, and report interpretation.
- `passing_threshold`: Must state that at least 90% of review questions should
  be answered correctly.

Validation:
- Timing guidance must make SC-001 and SC-002 measurable from the guide.
- Review questions must make SC-003 measurable from the guide.
