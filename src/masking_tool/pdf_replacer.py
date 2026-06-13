from __future__ import annotations

from pathlib import Path

import fitz

from .models import ReplacementRule
from .text_replacer import plan_replacements


class ExcludedPdfError(RuntimeError):
    """Raised when a PDF is outside first-version supported scope."""


def replace_pdf(source: str | Path, output: str | Path, rules: tuple[ReplacementRule, ...]) -> int:
    source_path = Path(source)
    output_path = Path(output)
    document = fitz.open(source_path)
    try:
        if not _has_text_layer(document):
            raise ExcludedPdfError("no extractable text layer")

        total = 0
        for page in document:
            insertions: list[tuple[fitz.Rect, str]] = []
            for rect, replacement_text, count in _page_replacements(page, rules):
                page.add_redact_annot(rect, fill=(1, 1, 1), cross_out=False)
                insertions.append((rect, replacement_text))
                total += count
            if page.first_annot:
                page.apply_redactions()
            for rect, text in insertions:
                _insert_replacement_text(page, rect, text)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        document.save(output_path)
        return total
    finally:
        document.close()


def _has_text_layer(document) -> bool:
    return any(page.get_text("text").strip() for page in document)


def _page_replacements(page, rules: tuple[ReplacementRule, ...]) -> list[tuple[fitz.Rect, str, int]]:
    replacements: list[tuple[fitz.Rect, str, int]] = []
    for span in _text_spans(page):
        replaced_text, count = _replace_span_text(span["text"], rules)
        if count:
            replacements.append((fitz.Rect(span["bbox"]), replaced_text, count))
    return replacements


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


def _insert_replacement_text(page, rect: fitz.Rect, text: str) -> None:
    target = fitz.Rect(rect)
    target.x1 = max(target.x1, target.x0 + 120)
    target.y1 = max(target.y1, target.y0 + 16)
    fonts = ("japan", "china-s", "helv")
    for fontname in fonts:
        for fontsize in (10, 9, 8, 7, 6):
            try:
                remaining = page.insert_textbox(
                    target,
                    text,
                    fontname=fontname,
                    fontsize=fontsize,
                    color=(0, 0, 0),
                    overlay=True,
                )
            except Exception:
                continue
            if remaining >= 0:
                return
    page.insert_text(target.tl, text, fontname="japan", fontsize=8, color=(0, 0, 0), overlay=True)
