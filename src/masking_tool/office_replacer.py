from __future__ import annotations

from pathlib import Path
from zipfile import BadZipFile, ZipFile

from docx import Document
from openpyxl import load_workbook
from pptx import Presentation

from .models import ReplacementRule
from .text_replacer import replace_text


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
    count = 0
    for run in paragraph.runs:
        replaced, replacements = replace_text(run.text, rules)
        if replacements:
            run.text = replaced
            count += replacements
    return count


def _replace_pptx_runs(paragraph, rules: tuple[ReplacementRule, ...]) -> int:
    count = 0
    for run in paragraph.runs:
        replaced, replacements = replace_text(run.text, rules)
        if replacements:
            run.text = replaced
            count += replacements
    return count
