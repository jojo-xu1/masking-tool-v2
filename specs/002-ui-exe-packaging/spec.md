# Feature Specification: UI改善とexe配布

**Feature Branch**: `002-ui-exe-packaging`

**Created**: 2026-06-02

**Status**: Draft

**Input**: User description: "UIを適度にデザインして、exeに作成する"

## Clarifications

### Session 2026-06-02

- Q: exe の配布形式はどうするか？ → A: 単一の `.exe` ファイルとして配布する。
- Q: exe ファイル名はどうするか？ → A: `MaskingTool.exe`。
- Q: UI の見た目の方向性はどうするか？ → A: 実務向けの落ち着いたデスクトップ UI。
- Q: 配布前ゲートに含める回帰確認範囲はどうするか？ → A: 置換表読み込み、ファイル種別判定、`.txt/.csv/.log/.docx/.xlsx/.pptx/.pdf`、対象外拡張子、未検出、skip レポートの全回帰確認を必須化する。
- Q: UI と exe の時間条件はどう検証するか？ → A: UI 30秒認識、単一ファイル5分、開発UI 5秒、exe 15秒は配布前チェックリストで実測して記録する。
- Q: packaged smoke test で exe が未作成の場合はどう扱うか？ → A: 通常は skip し、配布検証モードでは failure にする。
- Q: `build_exe.ps1` が `Expected executable was not created` だけを出す場合はどう扱うか？ → A: PyInstaller 未インストールと PyInstaller の非ゼロ終了を先に検出し、原因を明示して停止する。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 迷わず操作できるUIでマスキングを実行する (Priority: P1)

ユーザーは、既存のファイルマスキング機能を、整理された画面構成で操作できる。
置換表、入力ファイルまたはフォルダ、探索範囲、出力フォルダ、実行状態が
ひと目で分かり、入力不足や処理結果も画面上で確認できる。UI は実務向けの
落ち着いた配色、明確なセクション、読みやすい状態表示を優先する。

**Why this priority**: exe 化して配布しても、画面が分かりにくいとユーザーは
安全に処理対象や出力先を選べない。UI の基本品質が最初の価値になる。

**Independent Test**: ユーザーが画面だけで置換表、入力、出力先を選び、
処理を開始し、完了結果と `skipped_unsupported.txt` の場所を確認できることを
検証する。

**Acceptance Scenarios**:

1. **Given** アプリを起動している, **When** 画面を確認する, **Then** 置換表、入力種別、入力パス、出力フォルダ、処理開始、進捗、結果が区分されて表示される
2. **Given** 必須入力が不足している, **When** ユーザーが処理開始を押す, **Then** 不足項目が分かるメッセージが表示され、処理は開始されない
3. **Given** 有効な置換表と入力が指定されている, **When** ユーザーが処理を開始する, **Then** 進捗と完了サマリーが画面に表示される
4. **Given** 処理が完了した, **When** ユーザーが結果を確認する, **Then** 置換済み件数、未検出件数、対象外件数、失敗件数、レポート場所が確認できる

---

### User Story 2 - Pythonを意識せずexeから起動する (Priority: P2)

ユーザーは、Python やコマンドを意識せず、配布された Windows の単一
`MaskingTool.exe` ファイルをダブルクリックしてマスキングツールを起動できる。

**Why this priority**: 対象ユーザーが開発環境を持っていなくても利用できることが、
業務ツールとしての配布性を高める。

**Independent Test**: クリーンな Windows ユーザー環境を想定し、生成された exe を
起動して UI が表示され、基本フローを実行できることを確認する。

**Acceptance Scenarios**:

1. **Given** `MaskingTool.exe` が配布されている, **When** ユーザーが exe を起動する, **Then** マスキングツールの画面が表示される
2. **Given** exe からアプリを起動している, **When** ユーザーがサンプルファイルを処理する, **Then** Python コマンドを入力せずに置換済みファイルが作成される
3. **Given** exe の作成が完了している, **When** 開発者が成果物を確認する, **Then** 配布に必要な exe と利用手順が確認できる

---

### User Story 3 - 配布前にUIとexeを検証する (Priority: P3)

開発者は、exe 作成後に、画面操作、サンプル処理、対象外レポート、PDF 日本語置換の
主要確認をまとめて実施できる。

**Why this priority**: exe 化では実行環境差や同梱漏れが起きやすく、配布前の
検証手順がないとユーザー環境で動かないリスクがある。

**Independent Test**: 配布前チェックリストに従い、起動、単一ファイル処理、
フォルダ処理、対象外記録、PDF 日本語置換の確認が完了することを検証する。

**Acceptance Scenarios**:

1. **Given** exe が作成されている, **When** 配布前チェックを実行する, **Then** 起動、入力選択、出力選択、処理、レポート確認がすべて確認される
2. **Given** PDF 日本語置換サンプルがある, **When** exe から処理する, **Then** 置換後 PDF の日本語が文字化けしないことを確認できる

### Edge Cases

- 単一 exe が起動しない、または実行時に必要な同梱済みリソースを読み込めない
- 配布検証モードで `dist/MaskingTool.exe` が存在しない
- PyInstaller が未インストール、または PyInstaller のビルド処理が失敗して `dist/MaskingTool.exe` が作成されない
- exe 起動時に作業ディレクトリがプロジェクトルートではない
- ファイルパスに日本語、空白、記号が含まれる
- ユーザーが出力フォルダを指定しない
- 処理中にエラーが発生し、画面に結果サマリーを表示する必要がある
- 既存のマスキング機能は通るが、exe からだけ失敗する
- 画面サイズが小さく、主要操作が見切れる

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a calm work-oriented UI with distinct areas for replacement table selection, input target selection, output folder selection, execution controls, progress, and results.
- **FR-002**: System MUST preserve all existing masking capabilities from the file masking feature, including supported file types, folder traversal mode, output folder behavior, and `skipped_unsupported.txt`.
- **FR-003**: System MUST show validation messages before processing when required selections are missing or invalid.
- **FR-004**: System MUST show progress while processing multiple files.
- **FR-005**: System MUST show a completion summary with replaced, no-match, skipped, failed, and report-location information.
- **FR-006**: System MUST allow the user to launch the application from a single Windows `MaskingTool.exe` file without typing Python commands.
- **FR-007**: System MUST create a documented build output that identifies where `MaskingTool.exe` is located.
- **FR-008**: System MUST include a distribution verification procedure covering launch, single-file masking, folder masking, skipped unsupported files, and PDF Japanese replacement readability.
- **FR-009**: System MUST ensure paths containing Japanese characters, spaces, or symbols remain selectable and processable through the packaged application.
- **FR-010**: System MUST NOT remove or weaken first-version exclusions: image text, scanned PDFs, embedded objects, and OCR-dependent content remain out of scope.
- **FR-011**: System MUST require pre-distribution regression verification for replacement table loading, file type detection, all supported extensions (`.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`, text-layer `.pdf`), unsupported extensions, no-match inputs, and `skipped_unsupported.txt`.
- **FR-012**: System MUST require the distribution checklist to record measured results for UI selection recognition within 30 seconds, sample single-file processing within 5 minutes, development UI launch within 5 seconds, and packaged exe UI launch within 15 seconds.
- **FR-013**: System MUST allow packaged smoke tests to skip when `dist/MaskingTool.exe` is absent during normal test runs, but MUST fail when run in distribution verification mode and the executable is absent.
- **FR-014**: System MUST make the exe build script fail fast with an explicit message when PyInstaller is missing or when PyInstaller exits with a non-zero status, before falling back to the final `dist/MaskingTool.exe` existence check.

### Key Entities *(include if feature involves data)*

- **UI Session**: The user-visible state of replacement table path, input mode, input path, traversal mode, output folder, progress, and completion summary.
- **Executable Artifact**: The generated single Windows executable named `MaskingTool.exe` that starts the masking tool UI.
- **Distribution Package**: The single exe file produced for user distribution, with required runtime assets bundled inside it.
- **Distribution Verification Result**: A checklist-style record that launch and core masking flows were verified for the packaged executable.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can identify the required selections and start button within 30 seconds of opening the UI.
- **SC-002**: A user can complete a sample single-file masking run from the UI in under 5 minutes.
- **SC-003**: `MaskingTool.exe` launches the UI on a Windows machine without requiring a Python command.
- **SC-004**: Packaged execution successfully processes the manual sensitive sample set and creates `skipped_unsupported.txt`.
- **SC-005**: Packaged execution preserves readable Japanese replacement text in the PDF sample.
- **SC-006**: All existing automated tests for core masking behavior continue to pass after UI and packaging changes.
- **SC-007**: Pre-distribution verification explicitly records pass/fail results for replacement table loading, file type detection, every supported extension, unsupported extensions, no-match inputs, and skip-report generation.
- **SC-008**: Pre-distribution verification records measured times for UI recognition, sample single-file processing, development UI launch, and packaged exe launch against their stated thresholds.
- **SC-009**: Distribution verification mode fails if `dist/MaskingTool.exe` is missing, while normal automated test runs may skip packaged smoke checks before the exe is built.
- **SC-010**: When the exe build cannot run because PyInstaller is missing or fails, the build output identifies that cause rather than only reporting that `dist/MaskingTool.exe` was not created.

## Assumptions

- The first exe target is Windows.
- "適度にデザイン" means a calm work-oriented desktop UI: restrained colors, organized spacing, readable labels, clear grouping, and useful status feedback rather than a highly branded visual redesign.
- The executable is distributed as a single-file artifact.
- Packaging is built on top of the existing local desktop app and does not add a server or web UI.
- The existing masking feature from `001-file-masking` remains the functional baseline.
