from __future__ import annotations

import fitz

from masking_tool.models import ReplacementRule
from masking_tool.pdf_replacer import (
    PDF_LAYOUT_WARNING_PREFIX,
    _visible_font_size,
    _layout_warning,
    _replacement_fits,
    _replacement_font_size,
    _text_regions,
)
from tests.fixtures.create_pdf_textbox_fit_samples import (
    PDF_FIT_FONT_SIZE,
    PDF_FIT_PHRASE,
    PDF_FIT_REPL,
    create_pdf_fit_sample,
)


def test_text_regions_capture_original_span_bounds_and_font_size(tmp_path):
    source = create_pdf_fit_sample(tmp_path / "fit.pdf")
    document = fitz.open(source)
    try:
        regions = _text_regions(document[0], (_rule(),))
    finally:
        document.close()

    assert len(regions) == 1
    assert regions[0].original_text == PDF_FIT_PHRASE
    assert regions[0].replacement_text == PDF_FIT_REPL
    assert round(regions[0].font_size) == PDF_FIT_FONT_SIZE
    assert regions[0].replacement_count == 1
    assert regions[0].bounds.width > 0


def test_replacement_fits_uses_original_font_size_and_region_width(tmp_path):
    source = create_pdf_fit_sample(tmp_path / "fit.pdf")
    document = fitz.open(source)
    try:
        region = _text_regions(document[0], (_rule(),))[0]
        assert _replacement_fits(region) is True
        too_long = region.__class__(
            bounds=region.bounds,
            original_text=region.original_text,
            replacement_text="X" * 200,
            font_size=region.font_size,
            fontname=region.fontname,
            replacement_count=region.replacement_count,
        )
        assert _replacement_fits(too_long) is False
    finally:
        document.close()


def test_replacement_font_size_shrinks_when_text_cannot_fit_original_region(tmp_path):
    source = create_pdf_fit_sample(tmp_path / "fit.pdf")
    document = fitz.open(source)
    try:
        region = _text_regions(document[0], (_rule(),))[0]
        too_long = region.__class__(
            bounds=region.bounds,
            original_text=region.original_text,
            replacement_text="MASKED-LABEL-NEEDS-MANUAL-REVIEW",
            font_size=region.font_size,
            fontname=region.fontname,
            replacement_count=region.replacement_count,
        )
        assert _replacement_font_size(too_long) < region.font_size
    finally:
        document.close()


def test_visible_font_size_is_capped_by_extracted_bbox_height():
    span = {
        "size": 12.0,
        "ascender": 1.0,
        "descender": -0.2,
        "bbox": (10.0, 20.0, 80.0, 27.2),
    }

    assert round(_visible_font_size(span), 2) == 6.0


def test_layout_warning_includes_file_page_and_region_context():
    message = _layout_warning("sample.pdf", 2, fitz.Rect(10, 20, 30, 40))

    assert message.startswith(PDF_LAYOUT_WARNING_PREFIX)
    assert "sample.pdf" in message
    assert "page 2" in message
    assert "10.0,20.0,30.0,40.0" in message


def _rule() -> ReplacementRule:
    return ReplacementRule(no="1", detected_phrase=PDF_FIT_PHRASE, replacement_proposal=PDF_FIT_REPL, row_index=2)
