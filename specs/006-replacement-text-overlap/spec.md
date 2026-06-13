# Feature Specification: Replacement Text Overlap Prevention

**Feature Branch**: `006-replacement-text-overlap`

**Created**: 2026-06-13

**Status**: Draft

**Input**: User description: "iusse内容を改修する: 上記図通り置換する文字の内容を被っています"

## Clarifications

### Session 2026-06-13

- Q: When preventing replacement-text overlap, what behavior should be prioritized first? → A: Fit within the original visual region first; warn only if unreadable.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Readable replacements in diagram-like layouts (Priority: P1)

A user masks a supported file that contains several detected phrases close
together inside a fixed visual region, such as a PowerPoint diagram box,
shape, table cell, or text box. After masking, the replacement labels remain
readable and do not visually overlap each other or nearby labels.
The tool first tries to keep the readable replacement inside the original
visual region before using a layout warning.

**Why this priority**: This is the reported defect. If masked labels overlap,
the output is difficult to review or deliver even when the original sensitive
phrases were technically replaced.

**Independent Test**: Can be fully tested by processing a fixture matching the
attached screenshot style, then visually or programmatically confirming that
replacement labels have distinct readable regions and the original detected
phrases are absent from in-scope text.

**Acceptance Scenarios**:

1. **Given** a supported presentation file with multiple detected phrases in a
   small diagram box, **When** the user runs masking, **Then** each replacement
   label remains readable and does not overlap another replacement label.
2. **Given** a supported visual container with nearby non-sensitive labels,
   **When** the user runs masking, **Then** replacement labels do not obscure
   those nearby labels.

---

### User Story 2 - Clear warning when readable layout cannot be guaranteed (Priority: P2)

A user masks a supported visual layout whose available text region is too small
for the replacement proposal. The tool does not silently produce an unreadable
result; it records a clear warning so the user knows the output needs manual
review.

**Why this priority**: Some source layouts may not have enough visual space for
long replacement text. A warning is safer than silent overlap because it keeps
reviewers from trusting an unusable output.

**Independent Test**: Can be fully tested by processing a fixture with a very
small visual text area and long replacement proposal, then confirming the
result records a layout warning while still preserving existing masking and
skip-report behavior.

**Acceptance Scenarios**:

1. **Given** a supported visual container that cannot fit a readable
   replacement label, **When** the user runs masking, **Then** the result
   includes a warning that the replacement layout requires review.
2. **Given** a file containing both readable and unreadable replacement
   regions, **When** masking completes, **Then** readable regions remain
   readable and only the problematic regions are warned.

---

### User Story 3 - Preserve existing masking safety boundaries (Priority: P3)

A user relies on existing masking behavior for deterministic replacement,
Unicode matching, split-run Office text, unsupported content reporting, and
excluded content boundaries. The visual-overlap fix must not weaken those
guarantees.

**Why this priority**: The feature changes user-visible layout handling, but it
must not broaden unsupported scope or reintroduce sensitive-text leakage.

**Independent Test**: Can be fully tested by running existing deterministic,
Unicode, split-run Office, and unsupported-content tests after the layout
fixtures pass.

**Acceptance Scenarios**:

1. **Given** existing Unicode and split-run Office fixtures, **When** the user
   runs masking, **Then** the previous masking outcomes remain valid.
2. **Given** image text, scanned PDFs, embedded objects, or OCR-dependent
   content, **When** the user runs masking, **Then** those items remain
   excluded and reportable rather than silently treated as successfully masked.

### Edge Cases

- Multiple replacement labels fit individually but overlap because their source
  phrases are close together.
- A replacement label is longer than the original visible text region.
- A replacement label can be made readable within the original visual region by
  adjusting layout within that region.
- The source layout has a small shape, narrow table cell, or fixed-position
  text box.
- Replacement text contains Japanese/CJK characters, full-width forms, or long
  role/company labels.
- A file contains both readable replacement regions and regions that require a
  layout warning.
- Existing image text, scanned PDFs, embedded objects, and OCR-dependent
  content are present in the same selected file or folder.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST prevent replacement labels from visually overlapping
  each other in supported fixed-size visual text regions.
- **FR-002**: System MUST prevent replacement labels from obscuring nearby
  in-scope visible labels in the same supported visual region.
- **FR-003**: System MUST keep original detected phrases absent from in-scope
  output text after replacement.
- **FR-004**: System MUST record a clear layout warning when a readable
  replacement cannot be guaranteed for a supported visual region.
- **FR-005**: System MUST keep successfully readable replacement regions from
  being marked as failed only because another region in the same file requires
  a layout warning.
- **FR-006**: System MUST preserve deterministic replacement behavior,
  Unicode width matching behavior, split-run Office replacement behavior, and
  unsupported-content reporting.
- **FR-007**: System MUST attempt to keep replacement labels readable within the
  original visual region before recording a layout warning.
- **FR-MASK-001**: System MUST state that supported extensions remain `.txt`,
  `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf`; this
  feature specifically changes visual-readability behavior for supported
  fixed-size visual text regions, with `.pptx` visual containers as the primary
  reported path.
- **FR-MASK-002**: System MUST use `機密情報検出結果.xlsx` as the replacement
  table and treat `No`, `検出語句`, and `置換提案` as required header columns.
- **FR-MASK-003**: System MUST replace each matched `検出語句` with its matching
  `置換提案` deterministically and without leaving reversible mappings in the
  produced files.
- **FR-MASK-004**: Users MUST be able to select either one input file or one
  folder by screen operation.
- **FR-MASK-005**: System MUST produce replaced files and
  `skipped_unsupported.txt`; unsupported, unprocessable, excluded, or
  layout-warning conditions MUST be recorded rather than silently ignored.
- **FR-MASK-006**: System MUST explicitly exclude image text, scanned PDFs,
  embedded objects, and OCR from first-version behavior unless a later
  constitution amendment changes scope.

### Key Entities

- **Replacement Rule**: A row from `機密情報検出結果.xlsx` containing `No`,
  `検出語句`, and `置換提案`.
- **Visual Text Region**: A supported visible text area with fixed or constrained
  layout, such as a presentation shape, text box, table cell, or text-layer PDF
  replacement rectangle.
- **Replacement Layout Result**: The outcome for one visual text region,
  including whether the replacement is readable or requires a warning.
- **Layout Warning**: A user-facing record that a supported visual region was
  replaced or processed but the resulting layout may require manual review.
- **Processed Output**: A generated output file where matched in-scope text has
  been replaced while unsupported or excluded content remains reportable.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of screenshot-style visual layout fixtures produce
  replacement labels that do not overlap each other.
- **SC-002**: 100% of replacement-overflow fixtures record a clear layout
  warning instead of silently producing unreadable output.
- **SC-003**: 100% of layout fixtures have original detected phrases absent
  from in-scope output text after masking.
- **SC-004**: Existing Unicode matching, split-run Office, deterministic
  replacement, no-reversible-mapping, and unsupported-content tests continue to
  pass.
- **SC-005**: Users can identify every file or region that needs layout review
  from the output reporting without inspecting every processed file manually.

## Assumptions

- The reported screenshot represents a supported visual text region in a
  presentation-style file, most likely `.pptx`.
- The first deliverable focuses on readable output for in-scope text that the
  existing tool can already replace; it does not add OCR, image-text masking,
  embedded-object masking, or scanned-PDF masking.
- If the tool cannot guarantee readable replacement inside the existing visual
  constraints, an explicit warning is acceptable and safer than silent overlap.
- The preferred behavior is to preserve the original visual region rather than
  expanding or moving it, unless a later clarification changes that priority.
- Standard flowing text files such as `.txt`, `.csv`, `.log`, and normal
  workbook cells do not require visual-overlap layout handling beyond existing
  replacement behavior.
