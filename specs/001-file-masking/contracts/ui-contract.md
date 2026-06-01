# UI Contract: 機密文字列ファイルマスキング

## Primary Flow

1. User selects a replacement table spreadsheet.
2. User selects input mode: single file or folder.
3. User selects the input file or folder.
4. If folder mode is selected, user chooses traversal mode:
   - Direct children only
   - Include subfolders
5. User selects an output folder.
6. User starts processing.
7. UI shows progress by file and final summary.
8. UI exposes the output folder location and skip report location.

## Required Controls

- Replacement table picker accepting `.xlsx`.
- Input mode selector: `single_file` or `folder`.
- Input path picker matching the selected input mode.
- Folder traversal selector shown only for folder mode.
- Output folder picker.
- Start button disabled until required selections are valid.
- Progress indicator showing current file and completed/total count.
- Completion summary showing replaced, no-match, skipped, and failed counts.

## Validation Messages

- Missing replacement table: "置換表を選択してください。"
- Invalid replacement table headers: "`No`, `検出語句`, `置換提案` 列が必要です。"
- Invalid replacement row: "置換表に空欄または重複した検出語句があります。"
- Missing input target: "処理対象のファイルまたはフォルダを選択してください。"
- Missing output folder: "出力フォルダを選択してください。"
- No supported files: "対象フォルダに対応ファイルがありません。"

## Processing Contract

Inputs:
- `replacement_table_path`
- `input_mode`
- `input_path`
- `traversal_mode`
- `output_directory`

Outputs:
- Replaced files in the selected output directory.
- `skipped_unsupported.txt` in the selected output directory.
- Summary counts:
  - `replaced_count`
  - `processed_no_matches_count`
  - `skipped_unsupported_count`
  - `failed_count`

Rules:
- Originals are never overwritten.
- Recursive outputs preserve input-relative subfolder paths.
- Direct-child mode ignores subfolder contents.
- Unsupported files are not copied as successful outputs.
- The skip report is created even when it has no entries.

## Skip Report Format

`skipped_unsupported.txt` is UTF-8 text with one entry per line after a header.

```text
relative_path	status	reason
docs/image.pdf	skipped_unsupported	no extractable text layer
notes.bin	skipped_unsupported	unsupported extension .bin
deck.pptx	failed	could not open presentation
```

Ordering:
- Sort entries by normalized relative path.
- Use `/` as the separator in report paths for stable comparison.

## Error Handling Contract

- Replacement table validation errors stop the run before target processing.
- Per-file failures do not stop the batch unless the user cancels.
- Failed files are recorded in the skip report with status `failed`.
- User cancellation leaves already produced outputs in place and shows a
  cancelled summary.
