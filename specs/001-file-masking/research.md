# Research: 機密文字列ファイルマスキング

## Decision: Use a user-selected output folder

Rationale: The clarification flow was interrupted before the output destination
question was answered. A user-selected output folder is the safest planning
default because it avoids overwriting originals, keeps replaced files and
`skipped_unsupported.txt` together, and works for both single-file and folder
batch processing.

Alternatives considered:
- Same directory with suffix: simple, but easy to mix originals and outputs.
- Fixed subfolder under input folder: convenient for folders, awkward for
single-file inputs and read-only input locations.

## Decision: Use Tkinter for first-version screen operation

Rationale: Tkinter provides built-in local file/folder dialogs and simple forms
without adding UI packaging complexity. The first-version UX needs selection
controls, traversal mode, progress, and completion status rather than a complex
custom interface.

Alternatives considered:
- Web UI: heavier packaging and unnecessary server surface for a local tool.
- Rich desktop framework: better polish, but more setup before core masking
behavior is validated.

## Decision: Use structured format libraries per file type

Rationale: The constitution forbids raw string replacement for binary formats.
Use `openpyxl` for `.xlsx`, `python-docx` for `.docx`, `python-pptx` for
`.pptx`, and PyMuPDF for text-layer `.pdf`. Use standard text decoding paths for
`.txt`, `.csv`, and `.log`.

Alternatives considered:
- Raw byte replacement: rejected because it can corrupt Office/PDF files.
- Converting all files to text: rejected because output files must remain useful
in their original format.

## Decision: Detect and skip unsupported PDF cases

Rationale: Text-based PDFs are in scope, while scanned PDFs, image text, and OCR
are out of scope. If a PDF has no extractable text layer, or replacements cannot
be located through text search, record it in `skipped_unsupported.txt` instead
of reporting success.

Alternatives considered:
- OCR: explicitly out of first-version scope.
- Best-effort image analysis: rejected by constitution and not reproducible.

## Decision: Deterministic replacement ordering

Rationale: Detected phrases may overlap or contain one another. Replacement must
be reproducible, so rules are applied by descending `検出語句` length, then by
ascending `No`, then by original row order as a final tiebreaker.

Alternatives considered:
- Spreadsheet order only: can replace shorter phrases before longer matches.
- Arbitrary map iteration: not reproducible enough for audit expectations.

## Decision: Treat invalid replacement rows as validation errors

Rationale: Empty `検出語句`, empty `置換提案`, duplicate `検出語句`, or missing
required headers can cause ambiguous or unsafe replacement. The tool should stop
before processing any target files and show a validation error.

Alternatives considered:
- Skip invalid rows: could silently leave sensitive phrases unmasked.
- Use blank replacement values: makes output harder to audit and may hide
configuration mistakes.

## Decision: Preserve relative paths for recursive output

Rationale: When recursive mode is selected, output files should keep their
relative path under the selected output folder. This prevents filename
collisions and lets users compare input and output trees.

Alternatives considered:
- Flatten all outputs: simpler, but collisions and loss of context are likely.
- Mirror only successful files: accepted, with skipped entries carrying original
relative paths in the report.
