# Feature Specification: 機密文字列ファイルマスキング

**Feature Branch**: `001-file-masking`

**Created**: 2026-06-01

**Status**: Draft

**Input**: User description: "Office ファイル、テキスト系ファイル、テキスト型 PDF に含まれる機密文字列を、分類ラベル付きの不可逆な値へ置換するツール。画面操作によりインプットファイル指定あるいはフォルダ指定。フォルダ指定の場合、フォルダ内すべての対象ファイルの置き換え処理が必要。第一版では安全性と再現性を優先し、画像内文字、スキャン PDF、埋め込みオブジェクト、OCR は対象外。対応拡張子は .txt, .csv, .log, .docx, .xlsx, .pptx, .pdf。機密情報検出結果.xlsx の 検出語句 を 置換提案 に置き換える。成果物は置換したファイルと skipped_unsupported.txt。各種類のテスト用ファイルを作成する。"

## Clarifications

### Session 2026-06-01

- Q: フォルダ指定時の探索範囲はどうするか？ → A: 画面で「直下のみ / サブフォルダ含む」を選べるようにする。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 単一ファイルをマスキングする (Priority: P1)

ユーザーは画面上で `機密情報検出結果.xlsx` と処理対象の単一ファイルを指定し、
ファイル内の検出語句が置換提案へ置換されたファイルを取得する。

**Why this priority**: 単一ファイル処理は最小の価値提供単位であり、置換表の読み込み、
対象拡張子判定、置換、成果物作成の中核動作を検証できる。

**Independent Test**: 各対応拡張子のテストファイルを 1 つずつ指定し、出力ファイルに
検出語句が残らず、対応する置換提案が含まれることを確認する。

**Acceptance Scenarios**:

1. **Given** 有効な置換表と `.txt` ファイルが指定されている, **When** ユーザーが処理を開始する, **Then** 検出語句は置換提案へ置換され、置換後ファイルが作成される
2. **Given** 有効な置換表と該当語句を含まない対応ファイルが指定されている, **When** ユーザーが処理を開始する, **Then** ファイルは処理済み成果物として作成され、不要な置換は行われない
3. **Given** 必須列が不足した置換表が指定されている, **When** ユーザーが処理を開始する, **Then** 処理は開始されず、置換表の不備がユーザーに通知される
4. **Given** 出力フォルダが指定されている, **When** ユーザーが処理を開始する, **Then** 元ファイルは上書きされず、置換後ファイルと `skipped_unsupported.txt` は出力フォルダに作成される

---

### User Story 2 - フォルダ内の対象ファイルを一括マスキングする (Priority: P2)

ユーザーは画面上でフォルダを指定し、選択した探索範囲内にある対応拡張子の
ファイルすべてへ同じ置換表を適用する。フォルダ指定時、ユーザーは直下ファイル
のみを処理するか、サブフォルダを含めて処理するかを画面で選択できる。

**Why this priority**: 実利用では複数ファイルをまとめて処理する需要が高く、対象外
ファイルの扱いと処理結果の追跡が重要になる。

**Independent Test**: 対応ファイル、対象外拡張子、該当語句なしファイルを含む
テストフォルダを指定し、対応ファイルのみが置換され、対象外ファイルが
`skipped_unsupported.txt` に記録されることを確認する。

**Acceptance Scenarios**:

1. **Given** 対応拡張子の複数ファイルを含むフォルダが指定されている, **When** ユーザーが処理を開始する, **Then** フォルダ内の対象ファイルすべてに置換表が適用される
2. **Given** 対象外拡張子のファイルを含むフォルダが指定されている, **When** ユーザーが処理を開始する, **Then** 対象外ファイルは変更されず `skipped_unsupported.txt` に `skipped_unsupported` として記録される
3. **Given** 一部の対象ファイルが処理不能である, **When** ユーザーが処理を開始する, **Then** 処理可能なファイルは成果物化され、処理不能ファイルはレポートに記録される

---

### User Story 3 - 第一版の対象外範囲を確認できる (Priority: P3)

ユーザーは、画像内文字、スキャン PDF、埋め込みオブジェクト、OCR が必要な内容が
第一版の対象外であることを処理結果から確認できる。

**Why this priority**: 機密情報の残存リスクを避けるには、処理できなかった内容を
ユーザーが明確に把握できる必要がある。

**Independent Test**: スキャン PDF または画像文字を含むサンプルを指定し、対象外として
記録され、処理済みとして誤認されないことを確認する。

**Acceptance Scenarios**:

1. **Given** スキャン PDF が指定されている, **When** ユーザーが処理を開始する, **Then** そのファイルは対象外として記録され、置換済み成果物として扱われない
2. **Given** Office ファイル内に埋め込みオブジェクトが含まれている, **When** ユーザーが処理を開始する, **Then** 通常本文の処理結果と埋め込みオブジェクト対象外の記録をユーザーが区別できる

### Edge Cases

- 置換表に `No`, `検出語句`, `置換提案` のいずれかの列が存在しない
- 置換表に空の `検出語句`、空の `置換提案`、または重複した `検出語句` が含まれる
- 入力ファイルまたはフォルダが存在しない、読み取り不可、または処理中に削除される
- 入力フォルダに対応ファイルが 1 件も存在しない
- 対応拡張子だが内容が対象外である PDF または破損ファイルが含まれる
- ファイル内に同じ検出語句が複数回出現する
- 検出語句同士が包含関係にある
- ファイル名やフォルダ名に日本語、空白、記号が含まれる

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow the user to select one replacement table file named or equivalent to `機密情報検出結果.xlsx`.
- **FR-002**: System MUST validate that the replacement table contains header columns `No`, `検出語句`, and `置換提案`.
- **FR-003**: System MUST allow the user to select either a single input file or a single input folder through screen operation.
- **FR-003a**: When a folder is selected, System MUST allow the user to choose direct-child-only processing or recursive processing including subfolders.
- **FR-003b**: System MUST allow the user to select an output folder and MUST write replaced files and `skipped_unsupported.txt` there without overwriting originals.
- **FR-004**: System MUST treat `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, and text-based `.pdf` as supported target files for the first version.
- **FR-005**: System MUST replace every occurrence of each `検出語句` with its corresponding `置換提案` in supported file content that is in scope.
- **FR-006**: System MUST produce replaced files as the primary output for successfully processed supported inputs.
- **FR-007**: System MUST produce `skipped_unsupported.txt` for files that are unsupported, out of first-version scope, or unprocessable.
- **FR-008**: System MUST record unsupported extensions in `skipped_unsupported.txt` with status `skipped_unsupported`.
- **FR-009**: System MUST NOT process image text, scanned PDFs, embedded objects, or OCR-dependent content in the first version.
- **FR-010**: System MUST make processing results distinguishable by file, including successful replacement, skipped unsupported files, and processing failures.
- **FR-011**: System MUST avoid including any reversible mapping from replacement proposal back to original detected phrase in produced files.
- **FR-012**: System MUST produce the same replacement result when the same inputs and replacement table are processed again.
- **FR-013**: System MUST handle inputs with no matching detected phrase without reporting a false replacement failure.
- **FR-014**: System MUST create test fixture files for all supported extensions and at least one unsupported extension.
- **FR-015**: System MUST verify through tests that supported fixtures are replaced correctly and unsupported fixtures are recorded in `skipped_unsupported.txt`.
- **FR-016**: System MUST preserve readable replacement text in output PDFs,
  including Japanese replacement proposals, without mojibake.

### Key Entities *(include if feature involves data)*

- **Replacement Table**: The user-provided spreadsheet containing replacement rules with `No`, `検出語句`, and `置換提案` headers.
- **Replacement Rule**: One row from the replacement table mapping a detected phrase to a replacement proposal.
- **Input Target**: A selected file or a file discovered inside a selected folder, including path, extension, support status, and processing result.
- **Processed Output File**: A file created from a supported input after applying all applicable replacement rules.
- **Skip Report Entry**: A record written to `skipped_unsupported.txt` for unsupported extensions, excluded content types, or processing failures.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For each supported extension fixture, 100% of detected phrases listed in the replacement table are absent from the produced output file.
- **SC-002**: For each supported extension fixture, 100% of corresponding replacement proposals appear where the detected phrases were present.
- **SC-003**: When a folder contains supported and unsupported files, 100% of unsupported files are listed in `skipped_unsupported.txt`.
- **SC-004**: A user can complete selection of replacement table, input file or folder, and processing start within 5 minutes without command-line operation.
- **SC-005**: Re-running the same replacement table against the same input set produces identical replacement content and equivalent skip-report entries.
- **SC-006**: First-version excluded inputs such as scanned PDFs are not reported as successfully masked.
- **SC-007**: A text-based PDF fixture with Japanese replacement proposals is
  readable after masking and contains no mojibake in extracted text.

## Assumptions

- The first version runs locally and is used by a user who can access the files through the operating system file picker.
- Folder processing scope is selected by the user as either direct-child-only or recursive including subfolders.
- Output files are created separately from originals so users can compare or retain source files.
- The replacement table may be named `機密情報検出結果.xlsx`, and equivalent user-selected spreadsheets must still follow the required header layout.
- For overlapping detected phrases, the system uses a deterministic ordering that prevents shorter phrases from corrupting longer phrase replacements.
