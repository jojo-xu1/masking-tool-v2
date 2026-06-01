from __future__ import annotations

from pathlib import Path

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection
from tests.fixtures.create_fixtures import PHRASE_1, REPL_1, create_replacement_table, create_text_file


def test_single_text_csv_log_and_no_match_files(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    for suffix in [".txt", ".csv", ".log"]:
        source = create_text_file(tmp_path / f"input{suffix}")
        out = tmp_path / f"out{suffix[1:]}"
        summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, out))

        output_text = (out / source.name).read_text(encoding="utf-8")
        assert PHRASE_1 not in output_text
        assert REPL_1 in output_text
        assert summary.replaced_count == 1
        assert source.read_text(encoding="utf-8").count(PHRASE_1) == 1

    no_match = create_text_file(tmp_path / "no_match.txt", "nothing here")
    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, no_match, tmp_path / "out-no-match"))

    assert summary.processed_no_matches_count == 1
    assert (tmp_path / "out-no-match" / "no_match.txt").read_text(encoding="utf-8") == "nothing here"
