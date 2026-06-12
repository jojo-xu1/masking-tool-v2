from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from docx import Document
from openpyxl import load_workbook
from pptx import Presentation

from .models import ReplacementRule
from .text_replacer import replace_text


@dataclass(frozen=True)
class _TextSegment:
    text: str
    source_run: object


def replace_docx(source: str | Path, output: str | Path, rules: tuple[ReplacementRule, ...]) -> tuple[int, list[str]]:
    document = Document(str(source))
    count = 0
    for paragraph in document.paragraphs:
        count += _replace_paragraph_runs(paragraph, rules)
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    count += _replace_paragraph_runs(paragraph, rules)

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output_path))
    return count, embedded_object_notes(source)


def replace_xlsx(source: str | Path, output: str | Path, rules: tuple[ReplacementRule, ...]) -> tuple[int, list[str]]:
    workbook = load_workbook(source)
    count = 0
    for sheet in workbook.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                if isinstance(cell.value, str):
                    replaced, replacements = replace_text(cell.value, rules)
                    if replacements:
                        cell.value = replaced
                        count += replacements
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(output_path)
    return count, embedded_object_notes(source)


def replace_pptx(source: str | Path, output: str | Path, rules: tuple[ReplacementRule, ...]) -> tuple[int, list[str]]:
    presentation = Presentation(str(source))
    count = 0
    for slide in presentation.slides:
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False):
                for paragraph in shape.text_frame.paragraphs:
                    count += _replace_pptx_runs(paragraph, rules)
            if getattr(shape, "has_table", False):
                for row in shape.table.rows:
                    for cell in row.cells:
                        for paragraph in cell.text_frame.paragraphs:
                            count += _replace_pptx_runs(paragraph, rules)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    presentation.save(str(output_path))
    return count, embedded_object_notes(source)


def embedded_object_notes(source: str | Path) -> list[str]:
    try:
        with ZipFile(source) as archive:
            names = archive.namelist()
    except (BadZipFile, FileNotFoundError):
        return []
    indicators = ("/embeddings/", "embeddings/", "/oleObject", "oleObject")
    if any(any(indicator in name for indicator in indicators) for name in names):
        return ["embedded objects are out of scope and were not masked"]
    return []


def _replace_paragraph_runs(paragraph, rules: tuple[ReplacementRule, ...]) -> int:
    return _replace_visible_run_text(paragraph, rules)


def _replace_pptx_runs(paragraph, rules: tuple[ReplacementRule, ...]) -> int:
    return _replace_visible_run_text(paragraph, rules)


def _replace_visible_run_text(paragraph, rules: tuple[ReplacementRule, ...]) -> int:
    runs = list(paragraph.runs)
    segments = [_TextSegment(run.text, run) for run in runs if run.text]
    if not segments:
        return 0

    count = 0
    for rule in rules:
        segments, replacements = _replace_segments(segments, rule)
        count += replacements

    if count:
        _write_segments(paragraph, segments)
    return count


def _replace_segments(
    segments: list[_TextSegment],
    rule: ReplacementRule,
) -> tuple[list[_TextSegment], int]:
    visible_text = "".join(segment.text for segment in segments)
    phrase = rule.detected_phrase
    if phrase not in visible_text:
        return segments, 0

    next_segments: list[_TextSegment] = []
    count = 0
    cursor = 0
    while True:
        match_start = visible_text.find(phrase, cursor)
        if match_start == -1:
            next_segments.extend(_slice_segments(segments, cursor, len(visible_text)))
            break

        next_segments.extend(_slice_segments(segments, cursor, match_start))
        first_run = _run_at(segments, match_start)
        next_segments.append(_TextSegment(rule.replacement_proposal, first_run))
        cursor = match_start + len(phrase)
        count += 1

    return next_segments, count


def _slice_segments(segments: list[_TextSegment], start: int, end: int) -> list[_TextSegment]:
    if start >= end:
        return []

    sliced: list[_TextSegment] = []
    cursor = 0
    for segment in segments:
        segment_end = cursor + len(segment.text)
        overlap_start = max(start, cursor)
        overlap_end = min(end, segment_end)
        if overlap_start < overlap_end:
            local_start = overlap_start - cursor
            local_end = overlap_end - cursor
            sliced.append(_TextSegment(segment.text[local_start:local_end], segment.source_run))
        cursor = segment_end
    return sliced


def _run_at(segments: list[_TextSegment], index: int):
    cursor = 0
    for segment in segments:
        segment_end = cursor + len(segment.text)
        if cursor <= index < segment_end:
            return segment.source_run
        cursor = segment_end
    return segments[-1].source_run


def _write_segments(paragraph, segments: list[_TextSegment]) -> None:
    runs = list(paragraph.runs)
    while len(runs) < len(segments):
        runs.append(paragraph.add_run())

    for run, segment in zip(runs, segments):
        _copy_run_format(run, segment.source_run)
        run.text = segment.text

    for run in runs[len(segments) :]:
        run.text = ""


def _copy_run_format(target, source) -> None:
    if hasattr(target, "bold"):
        target.bold = getattr(source, "bold", None)
    if hasattr(target, "italic"):
        target.italic = getattr(source, "italic", None)

    if hasattr(target, "font") and hasattr(source, "font"):
        _copy_font_format(target.font, source.font)


def _copy_font_format(target_font, source_font) -> None:
    for attr in ("bold", "italic", "size"):
        if hasattr(target_font, attr) and hasattr(source_font, attr):
            setattr(target_font, attr, getattr(source_font, attr))

    try:
        source_rgb = source_font.color.rgb
    except AttributeError:
        source_rgb = None
    if source_rgb is not None:
        try:
            target_font.color.rgb = source_rgb
        except AttributeError:
            pass
