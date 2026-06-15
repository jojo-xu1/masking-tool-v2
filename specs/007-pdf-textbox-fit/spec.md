# Feature Specification: PDF Textbox Fit Preservation

**Feature Branch**: `007-pdf-textbox-fit`

**Created**: 2026-06-15

**Status**: Draft

**Input**: User description: "上記iussue内容を対応する: PDFを置換する際にテキストボックスの内容の文字が大きくなる、置換前は一ページで表示できますが、置換後ができない"

## Clarifications

### Session 2026-06-15

- Q: When PDF replacement text does not fit, what behavior should be prioritized? → A: Preserve the original font size first; warn when it cannot fit.
- Q: What should happen when a PDF region cannot fit the replacement at the original font size? → A: Still replace and remove the original phrase, then record a layout warning.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Preserve one-page PDF layout after replacement (Priority: P1)

A user masks a supported text-based PDF whose visible text fits inside a
constrained text box or fixed page region. After masking, the replacement text
remains readable and the content still fits within the original page region
instead of becoming larger, shrinking unexpectedly, or spilling beyond the
one-page layout.

**Why this priority**: This is the reported defect. If a PDF no longer fits in
the same page layout after masking, the output is difficult to review, print, or
deliver even when the sensitive text was removed.

**Independent Test**: Can be fully tested by processing a one-page text-based
PDF fixture with constrained visible text, then confirming the output still
fits on one page, the replacement text is readable, and the original detected
phrase is absent from in-scope text.

**Acceptance Scenarios**:

1. **Given** a one-page text-based PDF with a detected phrase inside a
   constrained visible text region, **When** the user runs masking, **Then** the
   output remains a one-page PDF with readable replacement text inside the
   original page region.
2. **Given** a replacement proposal that is longer than the original detected
   phrase but still can fit at the original font size in the original region,
   **When** the user runs masking, **Then** the output preserves that font size
   and does not break the original page fit.

---

### User Story 2 - Warn when PDF replacement cannot fit reliably (Priority: P2)

A user masks a text-based PDF whose available visible region is too small for a
readable replacement. The tool does not silently produce a broken layout; it
records a clear warning so the user knows the output needs manual review.

**Why this priority**: Some PDF text regions may be too constrained for longer
replacement labels. A warning is safer than silently creating a visually
unusable output.

**Independent Test**: Can be fully tested by processing an intentionally
constrained PDF fixture and confirming that the output records a layout warning
that identifies the affected file or page while still removing in-scope detected
text.

**Acceptance Scenarios**:

1. **Given** a supported text-based PDF region that cannot fit a readable
   replacement at the original font size inside the original page region,
   **When** the user runs masking, **Then** the original detected phrase is
   removed, replacement is applied, and the result includes a clear layout
   warning for manual review.
2. **Given** a PDF with both fit-safe and warning-required replacement regions,
   **When** masking completes, **Then** fit-safe regions remain usable and only
   the problematic regions are warned.

---

### User Story 3 - Preserve PDF masking safety boundaries (Priority: P3)

A user relies on existing PDF masking behavior for Japanese replacement text,
text-layer-only scope, deterministic replacement, and unsupported-content
reporting. The page-fit fix must not broaden unsupported scope or weaken those
guarantees.

**Why this priority**: The feature changes PDF layout handling, but it must not
create false confidence for scanned PDFs, image text, embedded objects, or
OCR-dependent content.

**Independent Test**: Can be fully tested by running existing PDF readable-text,
scanned-PDF exclusion, deterministic replacement, and skip-report checks after
the page-fit fixtures pass.

**Acceptance Scenarios**:

1. **Given** an existing text-based PDF with Japanese replacement text, **When**
   the user runs masking, **Then** the output replacement text remains readable
   and the original phrase is absent.
2. **Given** scanned PDFs, image text, embedded objects, or OCR-dependent
   content, **When** the user runs masking, **Then** those items remain excluded
   and reportable rather than silently treated as successfully masked.

### Edge Cases

- A replacement label is longer than the original visible phrase but can still
  fit at the original font size inside the original page region.
- A replacement label cannot be made readable inside a very narrow or short PDF
  text region without reducing the original font size.
- Multiple replacement regions appear on the same page, with one region fitting
  and another requiring a warning.
- Replacement text contains Japanese/CJK characters, full-width forms, or long
  classification labels.
- A selected folder contains both text-based PDFs and scanned/image-only PDFs.
- Existing source text fits exactly at the page boundary before masking.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST keep readable replacement text within the original
  page region for supported text-based PDF replacements whenever the region can
  fit the replacement at the original font size.
- **FR-002**: System MUST preserve the original PDF font size for replacement
  text before considering any layout warning.
- **FR-003**: System MUST keep original detected phrases absent from in-scope
  text-based PDF output after replacement.
- **FR-004**: System MUST record a clear layout warning when a readable
  replacement cannot be guaranteed within the original PDF page region while
  preserving the original font size.
- **FR-005**: System MUST still replace matched in-scope text and remove the
  original detected phrase when a PDF layout warning is recorded.
- **FR-006**: System MUST keep fit-safe replacement regions from being marked as
  failed only because another region in the same PDF requires a warning.
- **FR-007**: System MUST preserve existing readable Japanese replacement text
  behavior for text-based PDFs.
- **FR-008**: System MUST preserve deterministic replacement behavior and
  existing skip-report visibility for PDF replacement warnings.
- **FR-MASK-001**: System MUST state that supported extensions remain `.txt`,
  `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf`; this feature
  specifically changes page-fit behavior for supported text-based PDF
  replacement.
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
- **PDF Text Region**: A supported visible text area in a text-based PDF where
  a detected phrase appears and where page-fit behavior must be preserved.
- **PDF Layout Result**: The outcome for one PDF text region, including whether
  the replacement remains readable within the original page region or requires a
  warning.
- **Layout Warning**: A user-facing record that a PDF replacement region may
  require manual review because readability or page fit cannot be guaranteed.
- **Processed Output**: A generated output file where matched in-scope text has
  been replaced while unsupported or excluded content remains reportable.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of one-page constrained text-based PDF fixtures remain
  one-page outputs after masking when the replacement can fit at the original
  font size.
- **SC-002**: 100% of fit-safe PDF fixtures have readable replacement text
  within the original page region at the original font size.
- **SC-003**: 100% of PDF layout fixtures have original detected phrases absent
  from in-scope output text after masking.
- **SC-004**: 100% of PDF overflow fixtures record a clear layout warning
  and remove the original detected phrase instead of leaving sensitive text in
  the output.
- **SC-005**: Existing Japanese PDF replacement, scanned-PDF exclusion,
  deterministic replacement, and skip-report regression tests continue to pass.
- **SC-006**: Users can identify every PDF file or page region that needs layout
  review from output reporting without inspecting every processed file manually.

## Assumptions

- The reported PDF is a supported text-based PDF, not scanned or image-only
  content.
- The first deliverable focuses on preserving visible page fit for text-layer
  PDF replacements that the existing tool can already detect and replace.
- If a replacement cannot be kept readable inside the original page constraints
  while preserving the original font size, an explicit warning is acceptable and
  safer than silently producing a broken layout.
- The preferred behavior is to preserve the original PDF page region rather
  than expanding replacement text beyond that region.
- Normal flowing text files and Office files are not changed by this feature
  except for shared reporting behavior that remains compatible.
