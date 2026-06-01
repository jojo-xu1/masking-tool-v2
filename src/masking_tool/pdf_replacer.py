from __future__ import annotations

from pathlib import Path

import fitz

from .models import ReplacementRule


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
            for rule in rules:
                matches = page.search_for(rule.detected_phrase)
                for rect in matches:
                    page.add_redact_annot(rect, fill=(1, 1, 1), cross_out=False)
                    insertions.append((rect, rule.replacement_proposal))
                total += len(matches)
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
