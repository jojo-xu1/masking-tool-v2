from __future__ import annotations

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection, TraversalMode
from tests.fixtures.create_fixtures import PHRASE_1, PHRASE_2, create_replacement_table, create_text_file
from tests.fixtures.create_fixtures import UNICODE_FULL_WIDTH_PHRASE, UNICODE_HALF_WIDTH_PHRASE, UNICODE_REPL


def test_original_detected_phrases_not_written_to_reports_or_summaries(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    folder = tmp_path / "in"
    create_text_file(folder / "a.txt")
    (folder / "skip.bin").write_text("x", encoding="utf-8")

    summary = process_selection(table, InputSelection(InputMode.FOLDER, folder, tmp_path / "out", TraversalMode.DIRECT_CHILDREN))
    report = summary.report_path.read_text(encoding="utf-8")
    summary_text = f"{summary.replaced_count} {summary.skipped_unsupported_count} {summary.failed_count}"

    assert PHRASE_1 not in report
    assert PHRASE_2 not in report
    assert PHRASE_1 not in summary_text
    assert PHRASE_2 not in summary_text


def test_unicode_width_outputs_do_not_leave_original_visible_phrase(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx", [(1, UNICODE_FULL_WIDTH_PHRASE, UNICODE_REPL)])
    source = create_text_file(tmp_path / "unicode.txt", f"取引先: {UNICODE_HALF_WIDTH_PHRASE}")

    process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, tmp_path / "out"))

    output_text = (tmp_path / "out" / "unicode.txt").read_text(encoding="utf-8")
    assert UNICODE_HALF_WIDTH_PHRASE not in output_text
    assert UNICODE_REPL in output_text
