from __future__ import annotations

from pathlib import Path

import fitz
from docx import Document
from openpyxl import Workbook
from pptx import Presentation

PHRASE_1 = "山田太郎"
PHRASE_2 = "example@example.com"
REPL_1 = "<PERSON_001>"
REPL_2 = "<EMAIL_001>"


def create_replacement_table(path: Path, rows: list[tuple[object, str, str]] | None = None) -> Path:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["No", "検出語句", "置換提案"])
    for row in rows or [(1, PHRASE_1, REPL_1), (2, PHRASE_2, REPL_2)]:
        sheet.append(list(row))
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    return path


def create_invalid_replacement_table(path: Path, headers: list[str]) -> Path:
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(headers)
    sheet.append([1, PHRASE_1])
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    return path


def create_text_file(path: Path, text: str | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text is not None else f"{PHRASE_1} / {PHRASE_2}", encoding="utf-8")
    return path


def create_docx(path: Path, text: str | None = None) -> Path:
    document = Document()
    document.add_paragraph(text if text is not None else f"担当者: {PHRASE_1}")
    table = document.add_table(rows=1, cols=1)
    table.cell(0, 0).text = PHRASE_2
    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(path)
    return path


def create_xlsx(path: Path, text: str | None = None) -> Path:
    workbook = Workbook()
    sheet = workbook.active
    sheet["A1"] = text if text is not None else PHRASE_1
    sheet["B1"] = PHRASE_2
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook.save(path)
    return path


def create_pptx(path: Path, text: str | None = None) -> Path:
    presentation = Presentation()
    slide = presentation.slides.add_slide(presentation.slide_layouts[5])
    box = slide.shapes.add_textbox(0, 0, 4000000, 1000000)
    box.text_frame.text = text if text is not None else f"{PHRASE_1} {PHRASE_2}"
    path.parent.mkdir(parents=True, exist_ok=True)
    presentation.save(path)
    return path


def create_text_pdf(path: Path, text: str | None = None) -> Path:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text if text is not None else PHRASE_2)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    doc.close()
    return path


def create_scanned_like_pdf(path: Path) -> Path:
    doc = fitz.open()
    doc.new_page()
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(path)
    doc.close()
    return path
