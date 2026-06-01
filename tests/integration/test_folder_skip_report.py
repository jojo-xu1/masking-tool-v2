from __future__ import annotations

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection, TraversalMode
from tests.fixtures.create_fixtures import create_replacement_table, create_text_file


def test_folder_records_unsupported_extensions(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    folder = tmp_path / "in"
    create_text_file(folder / "a.txt")
    (folder / "notes.bin").write_text("binary-ish", encoding="utf-8")

    summary = process_selection(
        table,
        InputSelection(InputMode.FOLDER, folder, tmp_path / "out", TraversalMode.DIRECT_CHILDREN),
    )

    report = summary.report_path.read_text(encoding="utf-8")
    assert summary.skipped_unsupported_count == 1
    assert "notes.bin\tskipped_unsupported\tunsupported extension .bin" in report
