# UI Contract: UI改善とexe配布

## Layout

The main window must use calm work-oriented grouping:

1. Header area with app name and one-line purpose.
2. Input section:
   - Replacement table selector
   - Input mode selector
   - Input path selector
   - Folder traversal selector
   - Output folder selector
3. Execution section:
   - Start button
   - Cancel button
   - Progress bar
   - Current file/status line
4. Results section:
   - Replaced count
   - No-match count
   - Skipped count
   - Failed count
   - Report path

## Interaction Rules

- Start is disabled or blocked until required selections are present.
- Folder traversal selection is visible and meaningful only for folder mode.
- Processing must not block status/progress updates.
- Completion summary must remain visible after processing.
- Error messages must identify the missing or invalid input.
- Paths with Japanese characters, spaces, and symbols must remain visible without
  truncating the important filename.

## Visual Rules

- Use restrained colors suitable for an operational tool.
- Keep labels short and stable.
- Use grouped sections rather than one long list of controls.
- The main window must be usable at 900x620 or larger.
- Text must not overlap controls.

## Contract Test Expectations

- UI exposes stable state keys for required inputs and summary values.
- UI validation messages remain compatible with existing tests.
- UI launch does not require a repository-relative working directory.
