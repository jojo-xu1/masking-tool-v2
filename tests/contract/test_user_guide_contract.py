from __future__ import annotations

from pathlib import Path

import fitz

from masking_tool.docgen import (
    MARKDOWN_PATH,
    PDF_PATH,
    REQUIRED_SECTION_TITLES,
    REQUIRED_TERMS,
    REVIEW_VALIDATION_TERMS,
    TROUBLESHOOTING_TOPICS,
    generate_pdf,
)


ROOT = Path(__file__).resolve().parents[2]
GUIDE = ROOT / MARKDOWN_PATH
PDF = ROOT / PDF_PATH


def read_guide() -> str:
    return GUIDE.read_text(encoding="utf-8")


def read_pdf_text() -> str:
    with fitz.open(PDF) as document:
        return "\n".join(page.get_text() for page in document)


def test_required_artifacts_exist_and_pdf_is_generated_from_markdown():
    assert MARKDOWN_PATH == "docs/user-guide.md"
    assert PDF_PATH == "docs/user-guide.pdf"
    assert GUIDE.exists()
    generated = generate_pdf(GUIDE, PDF)
    assert generated == PDF.resolve()
    assert PDF.exists()
    assert PDF.stat().st_size > 0


def test_required_section_titles_are_present():
    guide = read_guide()
    for title in REQUIRED_SECTION_TITLES:
        assert title in guide


def test_required_terms_are_present_in_markdown():
    guide = read_guide()
    for term in REQUIRED_TERMS:
        assert term in guide


def test_basic_workflow_sections_cover_user_actions():
    guide = read_guide()
    for term in (
        "置換表を選択",
        "単一ファイル",
        "フォルダ",
        "サブフォルダ",
        "出力フォルダ",
        "処理開始",
        "結果を確認",
    ):
        assert term in guide


def test_result_terms_are_explained():
    guide = read_guide()
    for term in (
        "置換済み件数",
        "未検出件数",
        "対象外件数",
        "失敗件数",
        "レポートパス",
        "skipped_unsupported.txt",
    ):
        assert term in guide


def test_elapsed_time_recording_fields_are_present():
    guide = read_guide()
    for term in REVIEW_VALIDATION_TERMS:
        assert term in guide


def test_supported_extensions_are_documented():
    guide = read_guide()
    for extension in (".txt", ".csv", ".log", ".docx", ".xlsx", ".pptx", ".pdf"):
        assert extension in guide
    assert "テキスト型PDF" in guide


def test_excluded_scope_is_documented():
    guide = read_guide()
    for term in ("画像内文字", "スキャンPDF", "埋め込みオブジェクト", "OCR"):
        assert term in guide


def test_replacement_table_columns_are_documented():
    guide = read_guide()
    for header in ("No", "検出語句", "置換提案"):
        assert header in guide


def test_review_questions_and_threshold_are_present():
    guide = read_guide()
    for term in (
        "対応範囲",
        "対象外範囲",
        "置換表",
        "出力ファイル",
        "レポートの意味",
        "90%",
    ):
        assert term in guide


def test_troubleshooting_coverage_is_present():
    guide = read_guide()
    for topic in TROUBLESHOOTING_TOPICS:
        assert topic in guide


def test_pre_use_checklist_covers_safety_review():
    guide = read_guide()
    for term in (
        "処理前チェックリスト",
        "置換表",
        "入力対象",
        "出力フォルダ",
        "対応ファイル",
        "対象外",
        "skipped_unsupported.txt",
    ):
        assert term in guide


def test_normal_user_operation_does_not_require_developer_commands():
    guide = read_guide().lower()
    forbidden = ("python -m", "pip install", "pyinstaller", "build_exe.ps1")
    for command in forbidden:
        assert command not in guide


def test_pdf_contains_required_workflow_and_review_terms():
    generate_pdf(GUIDE, PDF)
    pdf_text = read_pdf_text()
    for term in (
        "MaskingTool.exe",
        "機密情報検出結果.xlsx",
        "skipped_unsupported.txt",
        "単一ファイル所要時間",
        "フォルダ処理所要時間",
        "90%",
    ):
        assert term in pdf_text


def test_pdf_contains_required_scope_terms():
    generate_pdf(GUIDE, PDF)
    pdf_text = read_pdf_text()
    for term in (".txt", ".csv", ".log", ".docx", ".xlsx", ".pptx", ".pdf", "OCR"):
        assert term in pdf_text
