# Contract: Unicode Normalization Matching

## Scope

This contract covers replacement matching for these supported in-scope formats:

- `.txt`
- `.csv`
- `.log`
- `.docx`
- `.xlsx`
- `.pptx`
- Text-layer `.pdf`

Out of scope:

- Image text.
- Scanned PDFs.
- Embedded objects.
- OCR-dependent content.
- Any content already excluded by existing format boundaries.

## Replacement Input Contract

Given:
- A valid replacement table with headers `No`, `検出語句`, and `置換提案`.
- A `検出語句` that contains ASCII-compatible full-width or half-width
  letters, digits, spaces, or punctuation.
- A supported target file where visible in-scope text contains the
  width-equivalent form of that phrase.

The system MUST:
- Match full-width `検出語句` values to half-width target text.
- Match half-width `検出語句` values to full-width target text.
- Preserve CJK characters that are not part of an explicit match.
- Prefer exact raw matches over width-equivalent matches for the same visible
  target text.
- Use existing deterministic ordering when only width-equivalent candidates
  apply.

## Output Contract

For each matched visible phrase:
- Output visible text MUST contain the matching `置換提案` exactly as supplied
  in the replacement table.
- Output visible text MUST NOT contain the matched raw target phrase at that
  in-scope location.
- Output MUST NOT normalize unrelated visible text.
- Result reporting MUST count one visible matched phrase as one replacement.

For non-matches:
- The file remains a successful processed output when no other error occurs.
- Result reporting MUST NOT record a false replacement.

For excluded content:
- Unsupported or excluded content remains unprocessed.
- `skipped_unsupported.txt` continues to record unsupported or excluded content
  according to existing behavior.

## Required Verification Cases

- `.txt`: full-width `検出語句` masks half-width target text.
- `.csv`: half-width `検出語句` masks full-width target text.
- `.log`: mixed CJK and ASCII-compatible width forms mask only explicit matches.
- `.docx`: width-equivalent matching works in paragraph and table-cell text.
- `.xlsx`: width-equivalent matching works in string cells.
- `.pptx`: width-equivalent matching works in text-box and table-cell text.
- Text-layer `.pdf`: width-equivalent matching works for extractable page text.
- Exact precedence: an exact raw match wins over a width-equivalent-only match
  for the same visible target.
- Replacement preservation: full-width, half-width, punctuation, spacing, and
  CJK in `置換提案` are written exactly.
- CJK preservation: non-matched CJK text remains readable and unchanged.
- Determinism: repeated processing with the same input and table produces the
  same visible output and counts.
- Safety: scanned PDFs, image text, embedded objects, and unsupported files
  remain excluded and reportable.
