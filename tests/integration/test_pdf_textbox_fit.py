from __future__ import annotations

import fitz

from masking_tool.app import process_selection
from masking_tool.models import InputMode, InputSelection, TraversalMode
from masking_tool.pdf_replacer import PDF_LAYOUT_WARNING_PREFIX
from tests.fixtures.create_pdf_textbox_fit_samples import (
    PDF_FIT_FONT_SIZE,
    PDF_FIT_PHRASE,
    PDF_FIT_REPL,
    PDF_LONG_PHRASE,
    PDF_LONG_REPL,
    PDF_OVERFLOW_PHRASE,
    PDF_OVERFLOW_REPL,
    create_pdf_fit_sample,
    create_pdf_long_fit_sample,
    create_pdf_mixed_sample,
    create_pdf_overflow_sample,
    create_pdf_textbox_fit_table,
)


def test_constrained_pdf_replacement_preserves_one_page_original_font_fit(tmp_path):
    table = create_pdf_textbox_fit_table(tmp_path / "機密情報検出結果.xlsx")
    source = create_pdf_fit_sample(tmp_path / "fit.pdf")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, tmp_path / "out"))

    output = tmp_path / "out" / "fit.pdf"
    assert summary.replaced_count == 1
    assert summary.results[0].replacement_count == 1
    assert summary.results[0].messages == []
    assert _page_count(output) == 1
    assert PDF_FIT_PHRASE not in _pdf_text(output)
    assert PDF_FIT_REPL in _pdf_text(output)
    assert _span_size_for(output, PDF_FIT_REPL) == PDF_FIT_FONT_SIZE


def test_longer_pdf_replacement_preserves_original_font_size_when_it_fits(tmp_path):
    table = create_pdf_textbox_fit_table(tmp_path / "機密情報検出結果.xlsx")
    source = create_pdf_long_fit_sample(tmp_path / "long-fit.pdf")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, tmp_path / "out"))

    output = tmp_path / "out" / "long-fit.pdf"
    assert summary.results[0].replacement_count == 1
    assert not summary.results[0].messages
    assert PDF_LONG_PHRASE not in _pdf_text(output)
    assert PDF_LONG_REPL in _pdf_text(output)
    assert _span_size_for(output, PDF_LONG_REPL) == PDF_FIT_FONT_SIZE


def test_overflow_pdf_replacement_applies_replacement_and_records_warning(tmp_path):
    table = create_pdf_textbox_fit_table(tmp_path / "機密情報検出結果.xlsx")
    source = create_pdf_overflow_sample(tmp_path / "overflow.pdf")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, tmp_path / "out"))

    output = tmp_path / "out" / "overflow.pdf"
    report = summary.report_path.read_text(encoding="utf-8")
    assert summary.replaced_count == 1
    assert summary.results[0].replacement_count == 1
    assert any(message.startswith(PDF_LAYOUT_WARNING_PREFIX) for message in summary.results[0].messages)
    assert PDF_OVERFLOW_PHRASE not in _pdf_text(output)
    assert PDF_OVERFLOW_REPL in _pdf_text(output)
    assert "overflow.pdf\tskipped_unsupported\tpdf layout warning:" in report


def test_mixed_pdf_regions_keep_fit_safe_replacement_successful_when_another_region_warns(tmp_path):
    table = create_pdf_textbox_fit_table(tmp_path / "機密情報検出結果.xlsx")
    source = create_pdf_mixed_sample(tmp_path / "mixed.pdf")

    summary = process_selection(table, InputSelection(InputMode.SINGLE_FILE, source, tmp_path / "out"))

    output = tmp_path / "out" / "mixed.pdf"
    text = _pdf_text(output)
    assert summary.replaced_count == 1
    assert summary.results[0].replacement_count == 2
    assert any(message.startswith(PDF_LAYOUT_WARNING_PREFIX) for message in summary.results[0].messages)
    assert PDF_FIT_PHRASE not in text
    assert PDF_OVERFLOW_PHRASE not in text
    assert PDF_FIT_REPL in text
    assert PDF_OVERFLOW_REPL in text
    assert _span_size_for(output, PDF_FIT_REPL) == PDF_FIT_FONT_SIZE


def test_folder_skip_report_records_pdf_layout_warning(tmp_path):
    table = create_pdf_textbox_fit_table(tmp_path / "機密情報検出結果.xlsx")
    folder = tmp_path / "in"
    create_pdf_overflow_sample(folder / "overflow.pdf")

    summary = process_selection(
        table,
        InputSelection(InputMode.FOLDER, folder, tmp_path / "out", TraversalMode.DIRECT_CHILDREN),
    )

    report = summary.report_path.read_text(encoding="utf-8")
    assert summary.replaced_count == 1
    assert "overflow.pdf\tskipped_unsupported\tpdf layout warning:" in report


def _page_count(path):
    document = fitz.open(path)
    try:
        return document.page_count
    finally:
        document.close()


def _pdf_text(path):
    document = fitz.open(path)
    try:
        return "\n".join(page.get_text("text") for page in document)
    finally:
        document.close()


def _span_size_for(path, expected_text):
    document = fitz.open(path)
    try:
        for page in document:
            for block in page.get_text("dict").get("blocks", []):
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if expected_text in span.get("text", ""):
                            return round(span["size"])
    finally:
        document.close()
    raise AssertionError(f"span not found for {expected_text!r}")
