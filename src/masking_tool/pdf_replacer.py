from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import fitz

from .models import ReplacementRule
from .text_replacer import plan_replacements

PDF_LAYOUT_WARNING_PREFIX = "pdf layout warning:"
_DEFAULT_PDF_FONT_SIZE = 10.0
_MIN_PDF_FONT_SIZE = 3.0
_MIN_REGION_WIDTH = 1.0
_MIN_FONT_METRIC_SPAN = 0.1
_TEXT_WIDTH_TOLERANCE = 1.02
_TEXT_FIT_PADDING = 0.96
_FONT_CANDIDATES = ("japan", "china-s", "helv")


class ExcludedPdfError(RuntimeError):
    """Raised when a PDF is outside first-version supported scope."""


@dataclass(frozen=True)
class _PdfTextRegion:
    bounds: fitz.Rect
    original_text: str
    replacement_text: str
    font_size: float
    fontname: str
    replacement_count: int


def replace_pdf(source: str | Path, output: str | Path, rules: tuple[ReplacementRule, ...]) -> tuple[int, list[str]]:
    source_path = Path(source)
    output_path = Path(output)
    document = fitz.open(source_path)
    try:
        if not _has_text_layer(document):
            raise ExcludedPdfError("no extractable text layer")

        total = 0
        messages: list[str] = []
        for page_index, page in enumerate(document, start=1):
            insertions: list[tuple[_PdfTextRegion, float]] = []
            for region in _text_regions(page, rules):
                fits = _replacement_fits(region)
                if not fits:
                    messages.append(_layout_warning(source_path.name, page_index, region.bounds))
                page.add_redact_annot(region.bounds, fill=(1, 1, 1), cross_out=False)
                insertions.append((region, _replacement_font_size(region)))
                total += region.replacement_count
            if page.first_annot:
                page.apply_redactions()
            for region, font_size in insertions:
                _insert_replacement_text(page, region, font_size)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        document.save(output_path)
        return total, messages
    finally:
        document.close()


def _has_text_layer(document) -> bool:
    return any(page.get_text("text").strip() for page in document)


def _text_regions(page, rules: tuple[ReplacementRule, ...]) -> list[_PdfTextRegion]:
    regions: list[_PdfTextRegion] = []
    for span in _text_spans(page):
        replaced_text, count = _replace_span_text(span["text"], rules)
        if count:
            regions.append(
                _PdfTextRegion(
                    bounds=fitz.Rect(span["bbox"]),
                    original_text=span["text"],
                    replacement_text=replaced_text,
                    font_size=_visible_font_size(span),
                    fontname=str(span.get("font") or ""),
                    replacement_count=count,
                )
            )
    return regions


def _text_spans(page) -> list[dict]:
    spans: list[dict] = []
    page_dict = page.get_text("dict")
    for block in page_dict.get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "")
                if text:
                    spans.append(span)
    return spans


def _visible_font_size(span: dict) -> float:
    nominal_size = float(span.get("size") or _DEFAULT_PDF_FONT_SIZE)
    bounds = fitz.Rect(span["bbox"])
    metric_span = max(
        _MIN_FONT_METRIC_SPAN,
        float(span.get("ascender", 1.0)) - float(span.get("descender", -0.2)),
    )
    visible_size = bounds.height / metric_span
    return min(nominal_size, visible_size)


def _replace_span_text(text: str, rules: tuple[ReplacementRule, ...]) -> tuple[str, int]:
    matches = plan_replacements(text, rules)
    if not matches:
        return text, 0

    parts: list[str] = []
    cursor = 0
    for match in matches:
        parts.append(text[cursor : match.start])
        parts.append(match.replacement)
        cursor = match.end
    parts.append(text[cursor:])
    return "".join(parts), len(matches)


def _replacement_fits(region: _PdfTextRegion) -> bool:
    width = max(_MIN_REGION_WIDTH, region.bounds.width)
    return _replacement_width(region.replacement_text, region.font_size) <= width * _TEXT_WIDTH_TOLERANCE


def _replacement_font_size(region: _PdfTextRegion) -> float:
    width = max(_MIN_REGION_WIDTH, region.bounds.width)
    text_width = _replacement_width(region.replacement_text, region.font_size)
    if text_width <= width * _TEXT_WIDTH_TOLERANCE:
        return region.font_size
    scaled_size = region.font_size * width / max(_MIN_REGION_WIDTH, text_width) * _TEXT_FIT_PADDING
    return max(_MIN_PDF_FONT_SIZE, min(region.font_size, scaled_size))


def _replacement_width(text: str, font_size: float) -> float:
    for fontname in _FONT_CANDIDATES:
        try:
            return float(fitz.get_text_length(text, fontname=fontname, fontsize=font_size))
        except Exception:
            continue
    return len(text) * font_size


def _layout_warning(source_name: str, page_number: int, bounds: fitz.Rect) -> str:
    region = ",".join(f"{value:.1f}" for value in (bounds.x0, bounds.y0, bounds.x1, bounds.y1))
    return (
        f"{PDF_LAYOUT_WARNING_PREFIX} {source_name} page {page_number} region {region} "
        "may need manual review because replacement text cannot fit at the original font size"
    )


def _insert_replacement_text(page, region: _PdfTextRegion, font_size: float) -> None:
    target = fitz.Rect(region.bounds)
    for fontname in _FONT_CANDIDATES:
        try:
            remaining = page.insert_textbox(
                target,
                region.replacement_text,
                fontname=fontname,
                fontsize=font_size,
                color=(0, 0, 0),
                overlay=True,
            )
        except Exception:
            continue
        if remaining >= 0:
            return
    for fontname in _FONT_CANDIDATES:
        try:
            page.insert_text(
                target.bl,
                region.replacement_text,
                fontname=fontname,
                fontsize=font_size,
                color=(0, 0, 0),
                overlay=True,
            )
            return
        except Exception:
            continue
