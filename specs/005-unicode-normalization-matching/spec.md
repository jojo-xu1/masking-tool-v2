# Feature Specification: Unicode Normalization Matching

**Feature Branch**: `005-unicode-normalization-matching`

**Created**: 2026-06-13

**Status**: Draft

**Input**: User description: "新しいissueを修正する: Unicodeがマッチングできない。日本語入力方法（インポート方法）を使用してExcelに日本語文字をインポートする場合、全角文字/CJK文字は生成されますが、ASCII半角文字は生成されません。"

## Clarifications

### Session 2026-06-13

- Q: When raw and width-equivalent replacement rules could both match the same visible text, which rule should win? → A: Exact raw match wins; otherwise use existing deterministic order.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full-width Excel phrase masks half-width document text (Priority: P1)

A user prepares `機密情報検出結果.xlsx` through Japanese Excel input or import, and the `検出語句` contains full-width ASCII-compatible characters such as company names, codes, punctuation, or spaces. When the selected target file contains the same visible phrase in half-width ASCII form, the tool still treats the phrase as covered by the replacement table and masks it.

**Why this priority**: This is the reported high-priority leak path. Users can reasonably believe a phrase is protected because it appears in the replacement table, while the supported output still contains an unmasked half-width equivalent.

**Independent Test**: Can be fully tested by preparing a replacement table with a full-width ASCII-compatible `検出語句`, running masking against a supported file that contains the half-width equivalent, and confirming the visible text is replaced.

**Acceptance Scenarios**:

1. **Given** a replacement table row where `検出語句` is `Ｔｅｃｈｎｏｌｏｇｉｅｓ， Ｉｎｃ．` and `置換提案` is `Company A`, **When** the user masks a supported file containing `Technologies, Inc.`, **Then** the output contains `Company A` and no visible `Technologies, Inc.` remains in in-scope text.
2. **Given** a replacement table row where `検出語句` contains full-width ASCII-compatible digits or punctuation, **When** the user masks a supported file containing the half-width equivalent, **Then** the equivalent target text is replaced once for each visible occurrence according to the existing deterministic replacement behavior.

---

### User Story 2 - Half-width Excel phrase masks full-width document text (Priority: P1)

A user has a replacement table where `検出語句` uses ordinary half-width ASCII characters, while the supported target file contains the visually equivalent full-width form. The tool recognizes the width-equivalent phrase and applies the expected replacement.

**Why this priority**: The issue can happen in both directions depending on how the replacement table and source documents were produced. Bidirectional coverage prevents users from needing to manually create duplicate full-width and half-width rows.

**Independent Test**: Can be fully tested by preparing a replacement table with a half-width `検出語句`, running masking against a supported file that contains the full-width equivalent, and confirming the visible text is replaced.

**Acceptance Scenarios**:

1. **Given** a replacement table row where `検出語句` is `Technologies, Inc.` and `置換提案` is `Company A`, **When** the user masks a supported file containing `Ｔｅｃｈｎｏｌｏｇｉｅｓ， Ｉｎｃ．`, **Then** the output contains `Company A` and no visible full-width equivalent remains in in-scope text.
2. **Given** multiple replacement rows that remain distinct after width-equivalent comparison, **When** the user masks a supported file containing both width forms, **Then** each occurrence receives the replacement proposal for its matching row without exposing reversible mappings.

---

### User Story 3 - CJK text and replacement values remain intact (Priority: P2)

A user masks Japanese, Chinese, or mixed-language documents and expects CJK characters and replacement proposals to remain exactly readable. Width-equivalent matching must not corrupt non-target text or rewrite replacement proposals.

**Why this priority**: The fix exists to support Japanese Excel workflows. It must not introduce broader text corruption or unexpected output changes.

**Independent Test**: Can be fully tested by running masking on supported files containing Japanese/CJK text, width-equivalent ASCII-compatible phrases, and replacement proposals with exact punctuation and spacing, then comparing the resulting visible text.

**Acceptance Scenarios**:

1. **Given** a supported file containing CJK text that is not part of any matching `検出語句`, **When** the user runs masking, **Then** that CJK text remains unchanged in the output.
2. **Given** a replacement table row where `置換提案` contains intentionally full-width or half-width characters, **When** a width-equivalent match is found, **Then** the output uses `置換提案` exactly as provided in the replacement table.

### Edge Cases

- A `検出語句` contains a mixture of CJK characters, ASCII-compatible letters, digits, punctuation, and spaces.
- Two replacement rows differ in raw text but become equivalent for matching after width differences are ignored.
- The same visible target could match one replacement row by exact raw text and another row only by width-equivalent comparison.
- A target contains adjacent or overlapping detected phrases where existing deterministic precedence decides which phrase is replaced.
- A target contains visually similar characters that are not width equivalents and should not be treated as a match.
- The selected input includes unsupported files, scanned PDFs, image text, embedded objects, or other excluded content.
- A replacement proposal intentionally uses full-width forms, half-width forms, or CJK characters.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST match `検出語句` against in-scope visible text when the only difference is full-width versus half-width ASCII-compatible character width.
- **FR-002**: System MUST support the reverse direction: half-width `検出語句` values match full-width target text when the characters are width-equivalent.
- **FR-003**: System MUST preserve `置換提案` exactly as supplied in the replacement table when writing output, including width, punctuation, spacing, and CJK characters.
- **FR-004**: System MUST NOT change unrelated visible text merely because it has a width-equivalent form; only text selected by a matching replacement rule may change.
- **FR-005**: System MUST keep existing deterministic replacement behavior for repeated, adjacent, or overlapping detected phrases.
- **FR-006**: System MUST produce processed outputs that do not leave reversible mappings for text replaced by this feature.
- **FR-007**: System MUST identify and report unsupported or excluded content consistently with existing masking behavior instead of silently ignoring it.
- **FR-008**: System MUST prefer an exact raw text match over a width-equivalent match when both could apply to the same visible target text; if no exact raw match applies, existing deterministic rule ordering decides among width-equivalent matches.
- **FR-MASK-001**: System MUST state that supported extensions in scope for this feature are `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf`.
- **FR-MASK-002**: System MUST use `機密情報検出結果.xlsx` as the replacement table and treat `No`, `検出語句`, and `置換提案` as required header columns.
- **FR-MASK-003**: System MUST replace each matched `検出語句` with its matching `置換提案` deterministically and without leaving reversible mappings in the produced files.
- **FR-MASK-004**: Users MUST be able to select either one input file or one folder by screen operation.
- **FR-MASK-005**: System MUST produce replaced files and `skipped_unsupported.txt`; unsupported or unprocessable files MUST be recorded rather than silently ignored.
- **FR-MASK-006**: System MUST explicitly exclude image text, scanned PDFs, embedded objects, and OCR from first-version behavior unless a later constitution amendment changes scope.

### Key Entities

- **Replacement Rule**: A row from `機密情報検出結果.xlsx` containing `No`, `検出語句`, and `置換提案`.
- **Width-Equivalent Match**: A comparison result where two visible strings are treated as the same for matching because they differ only by full-width and half-width ASCII-compatible forms.
- **In-Scope Text Segment**: Visible text inside a supported file type where the existing masking tool is allowed to search and replace text.
- **Processed Output**: A generated output file where matched text has been replaced and unrelated text remains unchanged.
- **Skip Report Entry**: A record written to `skipped_unsupported.txt` for unsupported extensions, excluded content types, or processing failures.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of validation samples where a full-width ASCII-compatible `検出語句` corresponds to half-width target text are masked in all in-scope supported formats represented by the sample set.
- **SC-002**: 100% of validation samples where a half-width `検出語句` corresponds to full-width target text are masked in all in-scope supported formats represented by the sample set.
- **SC-003**: 100% of replacement proposals in width-equivalent match samples appear in output exactly as supplied in `置換提案`.
- **SC-004**: 100% of CJK-only text samples that are not explicitly matched remain readable and unchanged after masking.
- **SC-005**: Existing deterministic replacement and unsupported-content reporting checks continue to pass after this feature is added.

## Assumptions

- Width-equivalent matching is intended only for ASCII-compatible full-width and half-width forms, not for every visually similar Unicode character.
- The matching behavior applies to text already considered in scope by the masking tool; image text, scanned PDFs, embedded objects, and OCR-dependent content remain excluded.
- If two replacement rows conflict after width-equivalent comparison and neither is an exact raw match for the visible target text, the existing deterministic rule ordering and overlap behavior remains the source of truth.
- Replacement table values are trusted user-provided masking output and must not be normalized or rewritten.
