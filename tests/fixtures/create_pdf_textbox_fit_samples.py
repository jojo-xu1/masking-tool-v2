from __future__ import annotations

from pathlib import Path

import fitz

from .create_fixtures import create_replacement_table

PDF_FIT_PHRASE = "PDF-FIT-SOURCE"
PDF_FIT_REPL = "PDF-FIT-MASKED"
PDF_LONG_PHRASE = "PDF-LONG-SOURCE-PLACEHOLDER"
PDF_LONG_REPL = "PDF-LONG-MASKED-LABEL"
PDF_OVERFLOW_PHRASE = "PDF-OVERFLOW"
PDF_OVERFLOW_REPL = "MASKED-LABEL-NEEDS-MANUAL-REVIEW"
PDF_SCALED_PHRASE = "PDF-SCALED-SOURCE"
PDF_SCALED_REPL = "PDF-SCALED-MASKED"
PDF_JAPANESE_PHRASE = "03-1234-5678"
PDF_JAPANESE_REPL = "電話番号_置換済み"
PDF_FIT_FONT_SIZE = 6
PDF_PAGE_WIDTH = 300
PDF_PAGE_HEIGHT = 180

PDF_TEXTBOX_ROWS = [
    (1, PDF_FIT_PHRASE, PDF_FIT_REPL),
    (2, PDF_LONG_PHRASE, PDF_LONG_REPL),
    (3, PDF_OVERFLOW_PHRASE, PDF_OVERFLOW_REPL),
    (4, PDF_SCALED_PHRASE, PDF_SCALED_REPL),
    (5, PDF_JAPANESE_PHRASE, PDF_JAPANESE_REPL),
]

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "inputs" / "pdf_textbox_fit_samples"
TABLE_DIR = ROOT / "replacement_tables"


def create_pdf_textbox_fit_table(path: Path) -> Path:
    return create_replacement_table(path, PDF_TEXTBOX_ROWS)


def create_pdf_fit_sample(path: Path) -> Path:
    return _create_pdf(path, [(fitz.Point(42, 54), PDF_FIT_PHRASE, PDF_FIT_FONT_SIZE)])


def create_pdf_long_fit_sample(path: Path) -> Path:
    return _create_pdf(path, [(fitz.Point(42, 54), PDF_LONG_PHRASE, PDF_FIT_FONT_SIZE)])


def create_pdf_overflow_sample(path: Path) -> Path:
    return _create_pdf(path, [(fitz.Point(42, 54), PDF_OVERFLOW_PHRASE, PDF_FIT_FONT_SIZE)])


def create_pdf_scaled_sample(path: Path) -> Path:
    document = fitz.open()
    page = document.new_page(width=PDF_PAGE_WIDTH, height=PDF_PAGE_HEIGHT)
    point = fitz.Point(42, 54)
    page.insert_text(
        point,
        PDF_SCALED_PHRASE,
        fontname="japan",
        fontsize=PDF_FIT_FONT_SIZE * 2,
        morph=(point, fitz.Matrix(1, 0.5)),
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(path)
    document.close()
    return path


def create_pdf_mixed_sample(path: Path) -> Path:
    return _create_pdf(
        path,
        [
            (fitz.Point(42, 54), PDF_FIT_PHRASE, PDF_FIT_FONT_SIZE),
            (fitz.Point(42, 78), PDF_OVERFLOW_PHRASE, PDF_FIT_FONT_SIZE),
        ],
    )


def create_pdf_japanese_sample(path: Path) -> Path:
    return _create_pdf(path, [(fitz.Point(42, 54), f"連絡先 {PDF_JAPANESE_PHRASE}", PDF_FIT_FONT_SIZE)])


def _create_pdf(path: Path, items: list[tuple[fitz.Point, str, int]]) -> Path:
    document = fitz.open()
    page = document.new_page(width=PDF_PAGE_WIDTH, height=PDF_PAGE_HEIGHT)
    for point, text, size in items:
        page.insert_text(point, text, fontname="japan", fontsize=size)
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(path)
    document.close()
    return path


def create_pdf_textbox_fit_inputs() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_pdf_fit_sample(INPUT_DIR / "pdf_fit.pdf")
    create_pdf_long_fit_sample(INPUT_DIR / "pdf_long_fit.pdf")
    create_pdf_overflow_sample(INPUT_DIR / "pdf_overflow.pdf")
    create_pdf_scaled_sample(INPUT_DIR / "pdf_scaled.pdf")
    create_pdf_mixed_sample(INPUT_DIR / "pdf_mixed.pdf")
    create_pdf_japanese_sample(INPUT_DIR / "pdf_japanese.pdf")


def create_pdf_textbox_fit_replacement_table() -> Path:
    return create_pdf_textbox_fit_table(TABLE_DIR / "機密情報検出結果_pdf_textbox_fit.xlsx")


def main() -> None:
    create_pdf_textbox_fit_replacement_table()
    create_pdf_textbox_fit_inputs()


if __name__ == "__main__":
    main()
