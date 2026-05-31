<!--
Sync Impact Report
Version change: template -> 1.0.0
Modified principles:
- PRINCIPLE_1_NAME placeholder -> I. 明示された対応範囲と除外範囲
- PRINCIPLE_2_NAME placeholder -> II. 不可逆かつ再現可能な置換
- PRINCIPLE_3_NAME placeholder -> III. 安全なファイル選択とバッチ処理
- PRINCIPLE_4_NAME placeholder -> IV. Python 優先と形式保持
- PRINCIPLE_5_NAME placeholder -> V. 形式別テストの必須化
Added sections:
- Product Scope and Inputs
- Development Workflow and Quality Gates
Removed sections:
- Placeholder-only template sections
Templates requiring updates:
- ✅ updated: .specify/templates/plan-template.md
- ✅ updated: .specify/templates/spec-template.md
- ✅ updated: .specify/templates/tasks-template.md
Follow-up TODOs:
- None
-->
# Masking Tool Constitution

## Core Principles

### I. 明示された対応範囲と除外範囲

第一版の対象ファイルは `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`, `.pptx`,
`.pdf` に限定する。PDF はテキスト型 PDF のみを対象とする。画像内文字、
スキャン PDF、埋め込みオブジェクト、OCR を必要とする入力は対象外とする。
対象外の拡張子や未対応の内容は処理せず、必ず `skipped_unsupported` として
レポートに記録する。

Rationale: 機密文字列の置換は安全性を優先するため、処理できる範囲と
できない範囲を明示して誤った安心感を避ける。

### II. 不可逆かつ再現可能な置換

置換ルールは `機密情報検出結果.xlsx` の `検出語句` と `置換提案` を正とする。
ツールは各 `検出語句` を対応する `置換提案` に置換しなければならない。
置換後の値から元の機密文字列を復元できる仕組みを出力ファイルへ残しては
ならない。同一の入力ファイル群と同一の置換表からは、同一の置換結果を
生成しなければならない。

Rationale: 監査可能な再現性と、出力ファイル単体で元情報を復元できない
不可逆性を両立する。

### III. 安全なファイル選択とバッチ処理

ユーザーは画面操作で単一ファイルまたはフォルダを指定できなければならない。
フォルダ指定時は、指定フォルダ内の対象ファイルすべてに同じ置換ルールを
適用しなければならない。対象外ファイルは変更せず、処理対象外として記録する。
処理中に失敗したファイルがあっても、他ファイルの処理結果と失敗情報を
判別できる成果物を残さなければならない。

Rationale: ユーザーが安全に範囲指定でき、バッチ処理後に何が処理され何が
処理されなかったかを確認できる必要がある。

### IV. Python 優先と形式保持

実装言語は Python とする。Office、Excel 置換表、PDF、テキスト系ファイルは、
各形式に適したライブラリまたは構造化 API で読み書きしなければならない。
バイナリ形式を文字列として直接置換してはならない。置換後ファイルは、可能な
限り元のファイル形式、シート、スライド、段落、表などの構造を保持する。

Rationale: ファイル破損と形式崩れを避けるため、形式ごとの安全な処理経路を
使う。

### V. 形式別テストの必須化

対応拡張子ごとにテスト用ファイルを用意し、置換表に基づく置換結果を検証
しなければならない。少なくとも `.txt`, `.csv`, `.log`, `.docx`, `.xlsx`,
`.pptx`, テキスト型 `.pdf`、対象外拡張子、空または該当語句なしの入力を
テストする。新しい対応形式を追加する場合は、その形式の正常系、未検出系、
失敗系のテストを同時に追加しなければならない。

Rationale: 機密情報の残存は重大な欠陥であるため、形式ごとの回帰テストを
開発の標準ゲートにする。

## Product Scope and Inputs

このプロジェクトは、機密文字列を分類ラベル付きの不可逆な値へ置換する
デスクトップまたはローカル実行ツールを提供する。必須入力は
`機密情報検出結果.xlsx` であり、先頭行をタイトルとして `No`, `検出語句`,
`置換提案` の列を含まなければならない。

成果物は、置換したファイルと `skipped_unsupported.txt` を含まなければ
ならない。`skipped_unsupported.txt` は、対象外拡張子、対象外内容、処理不能
ファイルをユーザーが追跡できる形式で記録する。

## Development Workflow and Quality Gates

すべての機能仕様は、対応ファイル種別、対象外範囲、入力 Excel レイアウト、
出力成果物、失敗時の記録方法を明記しなければならない。実装計画は Python の
バージョン、使用ライブラリ、ファイル形式ごとの処理方針、テスト方針を
明記しなければならない。

タスク分解では、置換表読み込み、ファイル種別判定、形式別置換、skip レポート、
画面操作、形式別テストを追跡可能なタスクとして分けなければならない。
実装完了前に、全対応拡張子のテストファイルで置換結果と skip レポートを
検証しなければならない。

## Governance

この憲章は、仕様書、実装計画、タスク、テスト判断に優先する。憲章と矛盾する
提案や実装は、憲章改定または明示的な例外記録なしに採用してはならない。

憲章の改定は、変更理由、影響を受ける原則、テンプレート更新の有無、必要な
移行作業を記録して行う。バージョンは semantic versioning に従う。原則の削除
または互換性のない再定義は MAJOR、原則や必須ゲートの追加は MINOR、文言修正
または明確化は PATCH とする。

レビューでは、対象範囲の逸脱、不可逆性、再現性、ファイル形式保持、
`skipped_unsupported.txt` の完全性、形式別テストの有無を確認しなければ
ならない。

**Version**: 1.0.0 | **Ratified**: 2026-06-01 | **Last Amended**: 2026-06-01
