from __future__ import annotations

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection
from masking_tool.office_replacer import embedded_object_notes
from tests.fixtures.create_fixtures import (
    SPLIT_PHRASE,
    SPLIT_REPL,
    create_docx,
    create_replacement_table,
    create_split_run_docx,
)


def test_office_embedded_object_notes_are_not_successful_mask_claims(tmp_path, monkeypatch):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    docx = create_docx(tmp_path / "sample.docx")
    monkeypatch.setattr("masking_tool.office_replacer.embedded_object_notes", lambda source: ["embedded objects are out of scope"])

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, docx, tmp_path / "out"))

    assert summary.replaced_count == 1
    assert any("embedded objects" in msg for result in summary.results for msg in result.messages)
    assert "embedded objects are out of scope" in summary.report_path.read_text(encoding="utf-8")
    assert embedded_object_notes(docx) == []


def test_split_run_office_with_embedded_object_records_skip_report_note(tmp_path, monkeypatch):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx", [(1, SPLIT_PHRASE, SPLIT_REPL)])
    docx = create_split_run_docx(tmp_path / "sample.docx")
    monkeypatch.setattr("masking_tool.office_replacer.embedded_object_notes", lambda source: ["embedded objects are out of scope"])

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, docx, tmp_path / "out"))

    report = summary.report_path.read_text(encoding="utf-8")
    assert summary.replaced_count == 1
    assert "sample.docx\tskipped_unsupported\tembedded objects are out of scope" in report
