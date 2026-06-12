from __future__ import annotations

from pathlib import Path

from .create_fixtures import (
    SPLIT_PHRASE,
    SPLIT_REPL,
    create_replacement_table,
    create_split_run_docx,
    create_split_run_pptx,
)

ROOT = Path(__file__).resolve().parent
INPUT_DIR = ROOT / "inputs" / "split_run_samples"
TABLE_DIR = ROOT / "replacement_tables"


def create_split_run_replacement_table() -> Path:
    return create_replacement_table(
        TABLE_DIR / "機密情報検出結果_split_run.xlsx",
        rows=[(1, SPLIT_PHRASE, SPLIT_REPL)],
    )


def create_split_run_inputs() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    create_split_run_docx(INPUT_DIR / "split_run_paragraph.docx")
    create_split_run_docx(INPUT_DIR / "split_run_table.docx", in_table=True)
    create_split_run_pptx(INPUT_DIR / "split_run_textbox.pptx")
    create_split_run_pptx(INPUT_DIR / "split_run_table.pptx", in_table=True)


def main() -> None:
    create_split_run_replacement_table()
    create_split_run_inputs()


if __name__ == "__main__":
    main()
