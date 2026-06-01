from __future__ import annotations

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection, TraversalMode
from tests.fixtures.create_fixtures import REPL_1, create_replacement_table, create_text_file


def test_folder_recursive_preserves_relative_paths(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    folder = tmp_path / "in"
    create_text_file(folder / "nested" / "b.txt")

    summary = process_selection(
        table,
        InputSelection(InputMode.FOLDER, folder, tmp_path / "out", TraversalMode.RECURSIVE),
    )

    assert summary.replaced_count == 1
    assert (tmp_path / "out" / "nested" / "b.txt").read_text(encoding="utf-8").count(REPL_1) == 1
