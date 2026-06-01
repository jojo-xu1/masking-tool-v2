from __future__ import annotations

import time

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection, TraversalMode
from tests.fixtures.create_fixtures import create_replacement_table, create_text_file


def test_batch_100_small_documents_completes_quickly(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    folder = tmp_path / "in"
    for index in range(100):
        create_text_file(folder / f"{index:03}.txt")

    start = time.perf_counter()
    summary = process_selection(table, InputSelection(InputMode.FOLDER, folder, tmp_path / "out", TraversalMode.DIRECT_CHILDREN))
    elapsed = time.perf_counter() - start

    assert summary.replaced_count == 100
    assert elapsed < 30
