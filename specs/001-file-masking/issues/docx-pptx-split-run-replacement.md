## Summary

High-priority `.docx` and `.pptx` masking defect: body text containing
`Technologies, Inc.` can remain unmasked when the phrase is split across Office
text runs.

## Reproduction

1. Create a `.docx` or `.pptx` file whose visible body text contains
   `Technologies, Inc.`.
2. Ensure Office formatting or editing history splits the visible phrase across
   multiple runs, for example `Technologies` in one run and `, Inc.` in another.
3. Use a replacement table where `検出語句` is `Technologies, Inc.` and
   `置換提案` is an irreversible masking value such as `会社名_置換済み`.
4. Run masking for the `.docx` or `.pptx` file.
5. Open or extract text from the output Office file.

## Expected

- Every visible in-scope occurrence of `Technologies, Inc.` is replaced in
  `.docx` and `.pptx` body text.
- The original phrase is absent from the output file.
- Replacement count reflects the performed replacement.
- Existing paragraph/table coverage and embedded-object out-of-scope behavior
  remain unchanged.

## Actual

`Technologies, Inc.` can remain in the output file. The current Office
replacement path applies `replace_text()` to each run independently, so a phrase
that spans multiple runs is never matched as a whole.

## Impact

This is high priority because `.docx` and `.pptx` are supported masking targets,
and an unreplaced company name in visible body text violates the requirement
that supported in-scope content must be masked deterministically.

## Fix

- Add regression fixtures for `.docx` and `.pptx` where `Technologies, Inc.` is
  split across runs.
- Update Office replacement to evaluate paragraph text across runs while
  preserving the document as safely as possible.
- Confirm table-cell text still receives the same treatment.
- Keep embedded objects and image text explicitly out of scope.

## Acceptance Criteria

- A `.docx` paragraph with `Technologies, Inc.` split across runs is masked.
- A `.pptx` text frame with `Technologies, Inc.` split across runs is masked.
- The output files do not contain `Technologies, Inc.` in visible body text.
- Existing Office integration tests still pass.
- Full replacement remains deterministic for overlapping replacement rules.
