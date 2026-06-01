from __future__ import annotations

from docx import Document
from openpyxl import load_workbook
from pptx import Presentation

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection
from tests.fixtures.create_fixtures import (
    PHRASE_1,
    REPL_1,
    create_docx,
    create_pptx,
    create_replacement_table,
    create_xlsx,
)


def test_single_docx_xlsx_pptx_files(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")

    docx = create_docx(tmp_path / "sample.docx")
    process_selection(table, InputSelection(InputMode.SINGLE_FILE, docx, tmp_path / "out-docx"))
    doc = Document(str(tmp_path / "out-docx" / "sample.docx"))
    assert PHRASE_1 not in "\n".join(p.text for p in doc.paragraphs)
    assert REPL_1 in "\n".join(p.text for p in doc.paragraphs)

    xlsx = create_xlsx(tmp_path / "sample.xlsx")
    process_selection(table, InputSelection(InputMode.SINGLE_FILE, xlsx, tmp_path / "out-xlsx"))
    workbook = load_workbook(tmp_path / "out-xlsx" / "sample.xlsx")
    assert workbook.active["A1"].value == REPL_1

    pptx = create_pptx(tmp_path / "sample.pptx")
    process_selection(table, InputSelection(InputMode.SINGLE_FILE, pptx, tmp_path / "out-pptx"))
    prs = Presentation(str(tmp_path / "out-pptx" / "sample.pptx"))
    text = "\n".join(shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text"))
    assert PHRASE_1 not in text
    assert REPL_1 in text
