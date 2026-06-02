from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

import fitz


MARKDOWN_PATH = "docs/user-guide.md"
PDF_PATH = "docs/user-guide.pdf"

REQUIRED_SECTION_TITLES = (
    "概要と安全に使う目的",
    "始める前に",
    "対応ファイルと対象外",
    "置換表の準備",
    "MaskingTool.exe を起動する",
    "単一ファイルを処理する",
    "フォルダを処理する",
    "出力フォルダを選ぶ",
    "結果と skipped_unsupported.txt を確認する",
    "トラブルシュート",
    "処理前チェックリスト",
    "レビュー質問と所要時間記録",
)

REQUIRED_TERMS = (
    "MaskingTool.exe",
    "機密情報検出結果.xlsx",
    "No",
    "検出語句",
    "置換提案",
    "skipped_unsupported.txt",
    ".txt",
    ".csv",
    ".log",
    ".docx",
    ".xlsx",
    ".pptx",
    ".pdf",
    "画像内文字",
    "スキャンPDF",
    "埋め込みオブジェクト",
    "OCR",
    "10分以内",
    "15分以内",
    "90%",
)

TROUBLESHOOTING_TOPICS = (
    "置換表を選択していない",
    "入力対象を選択していない",
    "出力フォルダを選択していない",
    "置換表の列が不足している",
    "対象外ファイル",
    "処理失敗",
    "MaskingTool.exe が起動しない",
)

REVIEW_VALIDATION_TERMS = (
    "単一ファイル所要時間",
    "フォルダ処理所要時間",
    "10分以内",
    "15分以内",
    "90%",
    "レビュー質問",
)


def repository_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    return Path.cwd().resolve()


def markdown_to_plain_text(markdown: str) -> list[str]:
    lines: list[str] = []
    in_fence = False
    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            line = re.sub(r"^#{1,6}\s*", "", line)
            line = re.sub(r"^\s*-\s+", "- ", line)
            line = re.sub(r"^\s*\d+\.\s+", lambda match: match.group(0).strip() + " ", line)
            line = line.replace("**", "")
            line = line.replace("`", "")
        lines.append(line)
    return lines


def wrap_line(line: str, *, width: int = 52) -> list[str]:
    if not line:
        return [""]
    chunks: list[str] = []
    current = ""
    for char in line:
        current += char
        if len(current) >= width:
            chunks.append(current)
            current = ""
    if current:
        chunks.append(current)
    return chunks


def iter_pdf_lines(markdown: str) -> Iterable[str]:
    for line in markdown_to_plain_text(markdown):
        for chunk in wrap_line(line):
            yield chunk


def generate_pdf(markdown_path: Path, pdf_path: Path) -> Path:
    markdown_path = markdown_path.resolve()
    pdf_path = pdf_path.resolve()
    markdown = markdown_path.read_text(encoding="utf-8")

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    document = fitz.open()
    page = document.new_page(width=595, height=842)
    x = 48
    y = 54
    line_height = 15

    for line in iter_pdf_lines(markdown):
        if y > 800:
            page = document.new_page(width=595, height=842)
            y = 54
        fontsize = 11
        fontname = "japan"
        if line and not line.startswith(("- ", "1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.")):
            fontsize = 12 if len(line) < 35 else 11
        page.insert_text((x, y), line, fontsize=fontsize, fontname=fontname)
        y += line_height if line else 9

    document.save(pdf_path)
    document.close()
    return pdf_path


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 2:
        print("Usage: python -m masking_tool.docgen docs/user-guide.md docs/user-guide.pdf")
        return 2
    generate_pdf(Path(args[0]), Path(args[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "MARKDOWN_PATH",
    "PDF_PATH",
    "REQUIRED_SECTION_TITLES",
    "REQUIRED_TERMS",
    "REVIEW_VALIDATION_TERMS",
    "TROUBLESHOOTING_TOPICS",
    "generate_pdf",
    "markdown_to_plain_text",
    "repository_root",
]
