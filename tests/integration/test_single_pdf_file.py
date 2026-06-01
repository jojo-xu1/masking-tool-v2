from __future__ import annotations

import fitz

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection
from tests.fixtures.create_fixtures import PHRASE_2, REPL_2, create_replacement_table, create_text_pdf


def test_single_text_based_pdf(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    source = create_text_pdf(tmp_path / "sample.pdf")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, tmp_path / "out"))

    output = fitz.open(tmp_path / "out" / "sample.pdf")
    text = "\n".join(page.get_text("text") for page in output)
    output.close()
    assert summary.replaced_count == 1
    assert PHRASE_2 not in text
    assert REPL_2 in text


def test_pdf_replacement_preserves_readable_japanese_text(tmp_path):
    table = create_replacement_table(
        tmp_path / "機密情報検出結果.xlsx",
        rows=[(1, "0125-74-2111", "電話番号_置換済み")],
    )
    source = create_text_pdf(tmp_path / "japanese.pdf", "連絡先 0125-74-2111")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, tmp_path / "out"))

    output = fitz.open(tmp_path / "out" / "japanese.pdf")
    text = "\n".join(page.get_text("text") for page in output)
    output.close()
    assert summary.replaced_count == 1
    assert "0125-74-2111" not in text
    assert "電話番号_置換済み" in text
    assert "�" not in text
