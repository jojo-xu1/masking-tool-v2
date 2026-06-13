from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from docx import Document
from openpyxl import load_workbook
from pptx import Presentation

from .models import ReplacementRule
from .text_replacer import plan_replacements, replace_text


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

    visible_text = "".join(segment.text for segment in segments)
    matches = plan_replacements(visible_text, rules)
    if not matches:
        return 0

    next_segments: list[_TextSegment] = []
    cursor = 0
    for match in matches:
        next_segments.extend(_slice_segments(segments, cursor, match.start))
        first_run = _run_at(segments, match.start)
        next_segments.append(_TextSegment(match.replacement, first_run))
        cursor = match.end
    next_segments.extend(_slice_segments(segments, cursor, len(visible_text)))
    _write_segments(paragraph, next_segments)
    return len(matches)


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
