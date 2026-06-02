# Feature Specification: ユーザー向け操作手順書

**Feature Branch**: `003-user-operation-guide`

**Created**: 2026-06-02

**Status**: Draft

**Input**: User description: "ユーザー向けの操作手順書を作ります。"

## Clarifications

### Session 2026-06-02

- Q: ユーザー向け操作手順書の成果物形式はどうするか？ → A: `docs/user-guide.md` と PDF の両方を作成する。
- Q: SC-001〜SC-003 の所要時間と90%正答レビューはどこで扱うか？ → A: レビュー質問と所要時間記録を `docs/user-guide.md` 本体に含める。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 初回利用者が手順書だけで基本操作できる (Priority: P1)

初めてマスキングツールを使うユーザーは、手順書を読んで、置換表、入力ファイルまたは
入力フォルダ、出力フォルダを選び、処理を開始し、置換済みファイルと
`skipped_unsupported.txt` を確認できる。

**Why this priority**: 操作手順書の最重要価値は、開発者の説明なしで安全に
基本操作を完了できることにある。

**Independent Test**: 手順書だけを渡されたユーザーが、サンプルデータで単一ファイル
またはフォルダ処理を完了し、出力結果とレポートの場所を説明できることを確認する。

**Acceptance Scenarios**:

1. **Given** ユーザーが `MaskingTool.exe` と置換表を持っている, **When** 手順書の基本操作に従う, **Then** アプリ起動、置換表選択、入力選択、出力フォルダ選択、開始、結果確認まで完了できる
2. **Given** ユーザーがフォルダを処理したい, **When** 手順書のフォルダ処理手順を読む, **Then** 直下のみ処理とサブフォルダ含む処理の違いを理解して選択できる
3. **Given** 処理が完了している, **When** ユーザーが手順書の結果確認手順を見る, **Then** 置換済み件数、未検出件数、対象外件数、失敗件数、`skipped_unsupported.txt` の意味を確認できる

---

### User Story 2 - 対象範囲と対象外範囲を理解できる (Priority: P2)

ユーザーは、処理できるファイル種別、処理できない内容、置換表の必要列を手順書で
確認し、対象外ファイルやスキャン PDF を誤って「処理済み」と判断しない。

**Why this priority**: 機密情報の取り残しを防ぐには、使い方だけでなく、
処理対象と対象外の境界を明確に理解できる必要がある。

**Independent Test**: ユーザーが手順書を読んで、対応拡張子、対象外内容、
置換表の必須列、対象外レポートの意味を正しく説明できることを確認する。

**Acceptance Scenarios**:

1. **Given** ユーザーが複数種類のファイルを処理したい, **When** 手順書の対象ファイル一覧を見る, **Then** `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, テキスト型 `.pdf` が対象であることを確認できる
2. **Given** ユーザーが画像内文字やスキャン PDF を処理したい, **When** 手順書の対象外説明を見る, **Then** 画像内文字、スキャン PDF、埋め込みオブジェクト、OCR が対象外であることを理解できる
3. **Given** ユーザーが置換表を準備する, **When** 手順書の置換表説明を見る, **Then** `No`, `検出語句`, `置換提案` の列が必要であることを確認できる

---

### User Story 3 - エラーや想定外結果に対処できる (Priority: P3)

ユーザーは、入力不足、置換表不備、対象外ファイル、処理失敗、ビルド済み exe が
起動しない場合などに、手順書のトラブルシュートを見て次に取る行動を判断できる。

**Why this priority**: 実務利用では、正常系だけでなく失敗時に安全に止まること、
結果を誤解しないことが重要である。

**Independent Test**: 代表的なエラー表示や対象外レポートを見せたユーザーが、
手順書を参照して原因候補と次の確認手順を説明できることを確認する。

**Acceptance Scenarios**:

1. **Given** 必須入力が不足している, **When** ユーザーが手順書のエラー対応を見る, **Then** 置換表、入力対象、出力フォルダのどれを確認すべきか判断できる
2. **Given** `skipped_unsupported.txt` に対象外ファイルが記録されている, **When** ユーザーが手順書を見る, **Then** 対象外ファイルは変更されていないことを理解できる
3. **Given** `MaskingTool.exe` が起動しない, **When** ユーザーが手順書のトラブルシュートを見る, **Then** 配布元への確認や再取得など、ユーザーが取れる安全な対応を判断できる

### Edge Cases

- ユーザーが Python や開発環境を知らず、`MaskingTool.exe` だけを受け取っている
- ファイルパスに日本語、空白、記号が含まれる
- 出力フォルダに同名ファイルが存在する、または元ファイルと同じ場所を指定する
- 置換表に必須列がない、検出語句が空欄、または重複している
- フォルダ内に対象外拡張子、スキャン PDF、画像内文字を含むファイルが混在している
- 処理結果に未検出、対象外、失敗が同時に含まれる
- 手順書の読者が業務担当者であり、開発者向け用語に慣れていない

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a user-facing operation guide that explains the complete basic workflow from launching the tool through confirming output files and `skipped_unsupported.txt`.
- **FR-002**: System MUST explain how to select a replacement table, one input file or one input folder, folder traversal scope, and output folder.
- **FR-003**: System MUST state the supported extensions: `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf`.
- **FR-004**: System MUST state that image text, scanned PDFs, embedded objects, and OCR-dependent content are out of scope.
- **FR-005**: System MUST explain that `機密情報検出結果.xlsx` requires `No`, `検出語句`, and `置換提案` columns.
- **FR-006**: System MUST explain that each `検出語句` is replaced with its matching `置換提案` and that original files are not intentionally overwritten.
- **FR-007**: System MUST explain how to interpret replaced, no-match, skipped unsupported, failed counts, and the report path.
- **FR-008**: System MUST include troubleshooting guidance for missing required inputs, invalid replacement tables, unsupported files, processing failures, and exe launch failure.
- **FR-009**: System MUST use plain Japanese suitable for non-developer business users.
- **FR-010**: System MUST include a final pre-use checklist that users can follow before processing confidential files.
- **FR-011**: System MUST provide the guide as both `docs/user-guide.md` and a PDF version suitable for user distribution.
- **FR-012**: System MUST include review questions and elapsed-time recording guidance in `docs/user-guide.md` so SC-001, SC-002, and SC-003 can be evaluated from the guide itself.

### Key Entities *(include if feature involves data)*

- **Operation Guide**: The user-facing document that describes safe operation, scope, result confirmation, and troubleshooting, provided as Markdown and PDF.
- **Procedure Section**: A step-by-step part of the guide such as launch, input selection, execution, result confirmation, or troubleshooting.
- **Scope Note**: A description of supported file types, excluded content, replacement table requirements, and output artifacts.
- **Troubleshooting Entry**: A symptom, likely cause, and recommended user action for common problems.
- **Pre-use Checklist**: A short confirmation list users complete before processing confidential files.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time user can complete a sample single-file masking run using only the guide in under 10 minutes.
- **SC-002**: A first-time user can complete a sample folder masking run using only the guide in under 15 minutes.
- **SC-003**: At least 90% of review checklist items for supported scope, excluded scope, replacement table, output files, and report interpretation are answered correctly by a reader after using the guide.
- **SC-004**: A user can identify the meaning of replaced, no-match, skipped unsupported, failed, and report path within 2 minutes of reading the results section.
- **SC-005**: The guide contains no unresolved developer-only instructions required for normal end-user operation.
- **SC-006**: The Markdown guide and PDF guide contain the same required operation, scope, result confirmation, troubleshooting, and pre-use checklist content.

## Assumptions

- The guide targets business users who receive `MaskingTool.exe` and do not need to build the application.
- The guide is written in Japanese.
- The Markdown guide is the source document, and the PDF is a distribution copy generated from the same content.
- The guide focuses on normal use, safe result confirmation, and troubleshooting; developer build instructions remain secondary or outside the end-user guide.
- The existing masking behavior and UI/exe packaging feature are the functional baseline for the guide.
- Review questions and elapsed-time recording are included in the guide body rather than managed as a separate review document.
