# Data Model: UI改善とexe配布

## UISession

Represents the current user-visible UI state.

Fields:
- `replacement_table_path`: Selected replacement table path.
- `input_mode`: `single_file` or `folder`.
- `input_path`: Selected file or folder path.
- `traversal_mode`: `direct_children` or `recursive`.
- `output_folder`: Selected output folder path.
- `progress_current`: Current processed file count.
- `progress_total`: Total discovered file count.
- `status_message`: Current status or validation message.
- `summary_counts`: Replaced, no-match, skipped, failed counts.
- `report_path`: Path to `skipped_unsupported.txt` after completion.

Validation:
- Required paths must be present before start.
- Folder traversal controls are active only for folder input.
- Summary values must match the processing result returned by the existing app
  service.

## ExecutableArtifact

Represents the generated executable.

Fields:
- `name`: Must be `MaskingTool.exe`.
- `path`: Expected build output path, `dist/MaskingTool.exe`.
- `build_mode`: Must be `onefile`.
- `entry_point`: Application entry point used to start the UI.

Validation:
- Artifact must exist after a successful build.
- Artifact must be a file, not a distribution folder.
- Artifact must launch the UI without requiring a Python command.

## DistributionVerificationResult

Represents pre-distribution validation.

Fields:
- `core_tests_passed`: Whether automated masking tests passed before packaging.
- `replacement_table_checked`: Whether replacement-table loading was verified.
- `file_type_detection_checked`: Whether file type detection was verified.
- `supported_extensions_checked`: Whether `.txt`, `.csv`, `.log`, `.docx`,
  `.xlsx`, `.pptx`, and text-layer `.pdf` were verified.
- `unsupported_extension_checked`: Whether unsupported extension handling was
  verified.
- `no_match_checked`: Whether an input with no detected terms was verified.
- `exe_exists`: Whether `dist/MaskingTool.exe` exists.
- `exe_launch_checked`: Whether the exe launch was verified.
- `single_file_checked`: Whether a single-file sample run was verified.
- `folder_run_checked`: Whether folder mode was verified.
- `skip_report_checked`: Whether skipped unsupported reporting was verified.
- `pdf_japanese_checked`: Whether Japanese PDF replacement readability was verified.
- `ui_recognition_seconds`: Measured time for identifying required selections
  and start button.
- `sample_single_file_seconds`: Measured time for sample single-file processing.
- `development_ui_launch_seconds`: Measured development UI launch time.
- `packaged_exe_launch_seconds`: Measured packaged exe launch time.
- `verification_mode`: `normal` or `distribution`.
- `notes`: Any limitations or environment details.

Validation:
- All check fields must be true before a distribution is considered ready.
- Distribution verification mode must fail if `dist/MaskingTool.exe` is absent.
- Normal test runs may skip packaged smoke checks when `dist/MaskingTool.exe` is
  absent.
- Timing fields must be recorded against the thresholds in the feature spec.
- Notes must record failures or skipped checks.
