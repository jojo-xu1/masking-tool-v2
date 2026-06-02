# Research: ユーザー向け操作手順書

## Decision: Use `docs/user-guide.md` as the source of truth

Rationale: Markdown is easy to edit, review in GitHub, test with plain text
contract checks, and keep close to the repository. It is also suitable as a
source for generated distribution formats.

Alternatives considered:
- README-only instructions: rejected because the README already serves mixed
  installation, development, and project overview needs.
- PDF-only guide: rejected because PDF is harder to review and maintain as the
  canonical source.

## Decision: Generate `docs/user-guide.pdf` from the Markdown source

Rationale: The user requested both Markdown and PDF. Generating the PDF from the
same source avoids drift and gives business users a distributable document. The
PDF is retained in the repository as a tracked distribution artifact because the
feature requires both guide formats as deliverables.

Alternatives considered:
- Manually maintain Markdown and PDF separately: rejected because content can
  diverge.
- Require external document tools: rejected because the project already uses
  Python and has PyMuPDF available.

## Decision: Include review questions and elapsed-time recording in the guide body

Rationale: The user selected the guide body as the place to handle the
SC-001/SC-002 timing checks and SC-003 90% review correctness check. Keeping the
review questions in `docs/user-guide.md` makes the Markdown and PDF both usable
for validation without a separate review document.

Alternatives considered:
- Separate `docs/user-guide-review-checklist.md`: rejected by clarification.
- Contract tests only: rejected because the success criteria require reader
  comprehension and elapsed-time validation, not only document structure.

## Decision: Keep the guide text-first and screenshot-optional

Rationale: The screenshot requirement was not finalized before planning. The
guide must remain complete without screenshots; screenshots can be added later
without changing the core workflow or acceptance criteria.

Alternatives considered:
- Require screenshots now: rejected because it would add a capture workflow and
  potentially block delivery.
- Avoid visual references entirely: rejected because the structure should allow
  screenshots if they become available.

## Decision: Validate the guide with contract tests

Rationale: The guide is safety-relevant documentation. Tests should confirm that
required scope, output, troubleshooting, and checklist content remains present
in the Markdown source and generated PDF.

Alternatives considered:
- Manual review only: rejected because key safety statements could be removed
  accidentally.
- Full usability testing automation: rejected because user task completion is
  better handled by checklist review and manual validation.
