from __future__ import annotations

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection
from tests.fixtures.create_fixtures import UNICODE_FULL_WIDTH_PHRASE, UNICODE_REPL, create_replacement_table, create_scanned_like_pdf


def test_scanned_pdf_is_skipped_not_successful(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")
    pdf = create_scanned_like_pdf(tmp_path / "scanned.pdf")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, pdf, tmp_path / "out"))

    assert summary.skipped_unsupported_count == 1
    assert summary.replaced_count == 0
    assert "scanned.pdf\tskipped_unsupported\tno extractable text layer" in summary.report_path.read_text(encoding="utf-8")


def test_scanned_pdf_stays_excluded_with_unicode_width_rule(tmp_path):
    table = create_replacement_table(tmp_path / "機密情報検出結果.xlsx", [(1, UNICODE_FULL_WIDTH_PHRASE, UNICODE_REPL)])
    pdf = create_scanned_like_pdf(tmp_path / "scanned.pdf")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, pdf, tmp_path / "out"))

    assert summary.skipped_unsupported_count == 1
    assert summary.replaced_count == 0
    assert "scanned.pdf\tskipped_unsupported\tno extractable text layer" in summary.report_path.read_text(encoding="utf-8")
