from __future__ import annotations

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection, TraversalMode
from tests.fixtures.create_fixtures import create_replacement_table, create_text_file


def test_deterministic_rerun_outputs_and_reports(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    folder = tmp_path / "in"
    create_text_file(folder / "a.txt")
    (folder / "skip.bin").write_text("x", encoding="utf-8")

    first = process_selection(table, InputSelection(InputMode.FOLDER, folder, tmp_path / "out1", TraversalMode.DIRECT_CHILDREN))
    second = process_selection(table, InputSelection(InputMode.FOLDER, folder, tmp_path / "out2", TraversalMode.DIRECT_CHILDREN))

    assert (tmp_path / "out1" / "a.txt").read_text(encoding="utf-8") == (tmp_path / "out2" / "a.txt").read_text(encoding="utf-8")
    assert first.report_path.read_text(encoding="utf-8") == second.report_path.read_text(encoding="utf-8")
