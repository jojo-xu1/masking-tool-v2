from __future__ import annotations

from pathlib import Path

from .create_fixtures import (
    UNICODE_FULL_WIDTH_PHRASE,
    UNICODE_FULL_WIDTH_REPL,
    UNICODE_HALF_WIDTH_PHRASE,
    UNICODE_REPL,
    create_docx,
    create_pptx,
    create_replacement_table,
    create_text_file,
    create_text_pdf,
    create_xlsx,
)

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "inputs" / "unicode_normalization_samples"
TABLE_DIR = ROOT / "replacement_tables"


def create_unicode_width_replacement_table() -> Path:
    return create_replacement_table(
        TABLE_DIR / "機密情報検出結果_unicode_width.xlsx",
        rows=[
            (1, UNICODE_FULL_WIDTH_PHRASE, UNICODE_REPL),
            (2, UNICODE_HALF_WIDTH_PHRASE, UNICODE_FULL_WIDTH_REPL),
        ],
    )


def create_unicode_width_inputs() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_text_file(INPUT_DIR / "full_rule_half_target.txt", f"取引先: {UNICODE_HALF_WIDTH_PHRASE}")
    create_text_file(INPUT_DIR / "half_rule_full_target.txt", f"取引先: {UNICODE_FULL_WIDTH_PHRASE}")
    create_text_file(INPUT_DIR / "mixed_cjk.log", f"東京本社 {UNICODE_HALF_WIDTH_PHRASE} 完了")
    create_docx(INPUT_DIR / "unicode_width.docx", f"取引先: {UNICODE_HALF_WIDTH_PHRASE}")
    create_xlsx(INPUT_DIR / "unicode_width.xlsx", f"取引先: {UNICODE_HALF_WIDTH_PHRASE}")
    create_pptx(INPUT_DIR / "unicode_width.pptx", f"取引先: {UNICODE_HALF_WIDTH_PHRASE}")
    create_text_pdf(INPUT_DIR / "unicode_width.pdf", f"取引先: {UNICODE_HALF_WIDTH_PHRASE}")


def main() -> None:
    create_unicode_width_replacement_table()
    create_unicode_width_inputs()


if __name__ == "__main__":
    main()
