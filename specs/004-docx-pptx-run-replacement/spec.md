# Feature Specification: DOCX/PPTX Split Text Replacement

**Feature Branch**: `004-docx-pptx-run-replacement`

**Created**: 2026-06-11

**Status**: Draft

**Input**: User description: "docx-pptx-split-run-replacement.mdのissueベースで、.docx/.pptx本文のTechnologies, Inc.がOfficeテキストrun分割されても置換できるようにする"

## Clarifications

### Session 2026-06-12

- Q: 分割語句の対象範囲はどこまでにするか？ → A: 同一段落・同一テキストボックス・同一表セル内で連続表示される語句だけを対象にする。
- Q: 分割語句を置換した後のテキスト書式はどう扱うか？ → A: 置換後テキストは、分割語句の先頭部分の書式を使う。
- Q: 分割語句の置換件数はどう数えるか？ → A: 分割数に関係なく、1 つの可視語句を 1 件の置換として数える。
- Q: 先頭部分の書式として自動検証する属性は何か？ → A: `bold`, `italic`, font size, color を維持できれば合格とする。
- Q: split-run 置換に成功した Office ファイルの対象外内容はどう記録するか？ → A: embedded object や画像内文字など検出可能な対象外内容は `skipped_unsupported.txt` に記録する。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - DOCX本文の分割語句を確実に置換する (Priority: P1)

業務ユーザーは、Word 文書の同一段落または同一表セル内で `Technologies, Inc.` が画面上は連続した語句として見えている場合、書式や編集履歴によって内部的に分割されていても、置換表どおりにマスキングされた出力ファイルを受け取れる。

**Why this priority**: `.docx` は対応対象であり、見えている本文に会社名が残ると機密情報の残存につながるため、最小の価値提供として最優先で保証する。

**Independent Test**: `Technologies, Inc.` が内部的に分割された `.docx` を処理し、出力文書の本文から元語句が消え、対応する `置換提案` が確認できれば独立して検証できる。

**Acceptance Scenarios**:

1. **Given** `Technologies, Inc.` が同一段落内で連続表示されるが内部的に分割された `.docx` 本文があり、置換表で `Technologies, Inc.` が `会社名_置換済み` に対応している, **When** ユーザーが単一ファイルとして処理する, **Then** 出力 `.docx` の本文に `Technologies, Inc.` は残らず `会社名_置換済み` が含まれる
2. **Given** 同じ条件の `.docx` が表セル内にある, **When** ユーザーが処理する, **Then** 表セル内の見えている対象語句も同じ置換結果になり、置換後テキストは分割語句の先頭部分の `bold`, `italic`, font size, color で表示される

---

### User Story 2 - PPTX本文の分割語句を確実に置換する (Priority: P1)

業務ユーザーは、PowerPoint の同一テキストボックスまたは同一表セル内で `Technologies, Inc.` が画面上は連続した語句として見えている場合、書式差や編集操作により内部的に分割されていても、置換表どおりにマスキングされた出力ファイルを受け取れる。

**Why this priority**: `.pptx` も対応対象であり、提案資料や報告資料に会社名が残るリスクは `.docx` と同等に高いため、同じ優先度で扱う。

**Independent Test**: `Technologies, Inc.` が内部的に分割された `.pptx` を処理し、出力スライド本文から元語句が消え、対応する `置換提案` が確認できれば独立して検証できる。

**Acceptance Scenarios**:

1. **Given** `Technologies, Inc.` が同一テキストボックス内で連続表示されるが内部的に分割された `.pptx` テキストボックスがあり、置換表で `Technologies, Inc.` が `会社名_置換済み` に対応している, **When** ユーザーが単一ファイルとして処理する, **Then** 出力 `.pptx` のスライド本文に `Technologies, Inc.` は残らず `会社名_置換済み` が含まれる
2. **Given** 同じ条件の `.pptx` が表セル内にある, **When** ユーザーが処理する, **Then** 表セル内の見えている対象語句も同じ置換結果になり、置換後テキストは分割語句の先頭部分の `bold`, `italic`, font size, color で表示される

---

### User Story 3 - 既存の安全境界と結果確認を維持する (Priority: P2)

業務ユーザーは、今回の修正後も既存の対応範囲、対象外範囲、出力成果物、処理結果の見方が変わらないことを確認できる。

**Why this priority**: 置換漏れの修正によって、埋め込みオブジェクトや画像内文字など対象外範囲を誤って「置換済み」と扱うと、安全境界が曖昧になるため。

**Independent Test**: 既存の Office 文書処理、対象外内容の記録、置換件数表示を確認し、修正前から保証していた挙動が維持されていれば独立して検証できる。

**Acceptance Scenarios**:

1. **Given** `.docx` または `.pptx` に埋め込みオブジェクトや画像内文字など検出可能な対象外内容が含まれる, **When** ユーザーが処理する, **Then** それらは対象外として `skipped_unsupported.txt` に記録され、置換済み本文とは区別して確認できる
2. **Given** 分割されていない通常の `.docx` または `.pptx` 本文がある, **When** ユーザーが処理する, **Then** 従来どおり置換され、元ファイルは上書きされない

### Edge Cases

- 対象語句の一部だけに書式差があり、同一段落・同一テキストボックス・同一表セル内で `Technologies, Inc.` と連続して読める場合。
- 対象語句が段落、テキストボックス、表セルの境界をまたぐ場合は、この feature の分割語句保証の対象外とする。
- 対象語句の途中で書式が変わる場合、置換後テキストは分割語句の先頭部分の `bold`, `italic`, font size, color で表示される。
- 対象語句が内部的に複数部分へ分割されている場合でも、結果上は 1 つの可視語句を 1 件の置換として扱う。
- 対象語句と重複する短い語句が同じ置換表に含まれる場合。
- 対象語句が画像、埋め込みオブジェクト、または OCR が必要な内容にだけ存在する場合。
- split-run 置換対象の本文と、埋め込みオブジェクトや画像など検出可能な対象外内容が同じ Office ファイルに共存する場合。
- 対象語句を含まない `.docx` または `.pptx` を処理する場合。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST replace every visible in-scope `.docx` body occurrence of `Technologies, Inc.` with the corresponding `置換提案`, even when the visible phrase is internally split within the same paragraph by Office formatting or editing boundaries.
- **FR-002**: System MUST replace every visible in-scope `.pptx` slide-body occurrence of `Technologies, Inc.` with the corresponding `置換提案`, even when the visible phrase is internally split within the same text box by Office formatting or editing boundaries.
- **FR-003**: System MUST apply the same split-phrase guarantee to supported `.docx` and `.pptx` table-cell text when the visible phrase is internally split within the same table cell.
- **FR-004**: System MUST ensure output `.docx` and `.pptx` files do not retain `Technologies, Inc.` in visible in-scope body text after a matching replacement rule is provided.
- **FR-005**: System MUST display replacement text using the `bold`, `italic`, font size, and color of the first visible portion of the matched split phrase while preserving surrounding visible text as normal document or slide content.
- **FR-006**: System MUST report replacement results consistently with existing result categories, including successful replacement, no-match, skipped unsupported, failed, and report path.
- **FR-007**: System MUST count each matched visible split phrase as one replacement regardless of how many internal Office text portions formed that phrase.
- **FR-008**: System MUST preserve existing safety boundaries: image text, scanned PDFs, embedded objects, and OCR-dependent content remain out of scope and MUST NOT be treated as masked.
- **FR-009**: System MUST preserve original-file safety by writing processed files to the selected output location without overwriting the original input file.
- **FR-010**: System MUST preserve deterministic replacement behavior when overlapping replacement rules exist.
- **FR-011**: System MUST record detectable out-of-scope Office content, such as embedded objects or images, in `skipped_unsupported.txt` even when visible split-run body text in the same file is successfully replaced.
- **FR-MASK-001**: System MUST state which supported extensions are in scope for this feature: `.docx` and `.pptx` are directly changed by this feature; `.txt`, `.csv`, `.log`, `.xlsx`, and text-based `.pdf` remain supported but outside this fix's changed behavior.
- **FR-MASK-002**: System MUST use `機密情報検出結果.xlsx` as the replacement table and treat `No`, `検出語句`, and `置換提案` as required header columns.
- **FR-MASK-003**: System MUST replace each `検出語句` with its matching `置換提案` deterministically and without leaving reversible mappings in the produced files.
- **FR-MASK-004**: Users MUST be able to select either one input file or one folder by screen operation.
- **FR-MASK-005**: System MUST produce replaced files and `skipped_unsupported.txt`; unsupported, out-of-scope, or unprocessable files and detectable out-of-scope Office content MUST be recorded rather than silently ignored.
- **FR-MASK-006**: System MUST explicitly exclude image text, scanned PDFs, embedded objects, and OCR from first-version behavior unless a later constitution amendment changes scope.

### Key Entities

- **Replacement Rule**: A row from `機密情報検出結果.xlsx` containing `No`, `検出語句`, and `置換提案`.
- **Office Input File**: A selected `.docx` or `.pptx` file, or one discovered inside a selected folder, including visible body text, table-cell text, support status, and processing result.
- **Visible In-Scope Text**: Text that a user can inspect as normal document or slide body content, including text within the same paragraph, the same text box, or the same table cell, excluding image text, embedded objects, and text spanning structural boundaries.
- **Processed Output File**: The `.docx` or `.pptx` file created in the output location after replacement rules are applied.
- **Skip Report Entry**: A record written to `skipped_unsupported.txt` for unsupported extensions, excluded content types, or processing failures.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of test `.docx` files with `Technologies, Inc.` split within the same paragraph or table cell remove the original phrase from in-scope output text.
- **SC-002**: 100% of test `.pptx` files with `Technologies, Inc.` split within the same text box or table cell remove the original phrase from in-scope output text.
- **SC-003**: 100% of corresponding replacement proposals appear in the output locations where the split phrase was present.
- **SC-004**: 100% of split-phrase replacement samples display the replacement proposal using the first visible portion's `bold`, `italic`, font size, and color.
- **SC-005**: 100% of split-phrase replacement samples count each matched visible phrase as one replacement in result reporting.
- **SC-006**: Existing supported Office scenarios for normal, unsplit text continue to pass without new false failures.
- **SC-007**: Re-running the same replacement table against the same affected `.docx` or `.pptx` input produces the same visible replacement result.
- **SC-008**: 100% of split-run Office samples that also contain detectable out-of-scope Office content record that content in `skipped_unsupported.txt`.

## Assumptions

- Users continue to provide replacement rules through `機密情報検出結果.xlsx` with `No`, `検出語句`, and `置換提案`.
- The high-priority defect specifically concerns visible `.docx` and `.pptx` body text within the same paragraph, text box, or table cell.
- This feature does not expand scope to images, embedded objects, scanned PDFs, or OCR-dependent content.
- The exact sample phrase `Technologies, Inc.` is required for regression coverage because it represents the reported defect.
