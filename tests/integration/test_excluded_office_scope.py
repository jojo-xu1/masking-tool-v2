from __future__ import annotations

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection
from masking_tool.office_replacer import embedded_object_notes
from tests.fixtures.create_fixtures import create_docx, create_replacement_table


def test_office_embedded_object_notes_are_not_successful_mask_claims(tmp_path, monkeypatch):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    docx = create_docx(tmp_path / "sample.docx")
    monkeypatch.setattr("masking_tool.office_replacer.embedded_object_notes", lambda source: ["embedded objects are out of scope"])

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, docx, tmp_path / "out"))

    assert summary.replaced_count == 1
    assert any("embedded objects" in msg for result in summary.results for msg in result.messages)
    assert embedded_object_notes(docx) == []
