from __future__ import annotations

from docx import Document
from docx.shared import Pt, RGBColor

from masking_tool.models import ReplacementRule
from masking_tool.office_replacer import _replace_paragraph_runs
from tests.fixtures.create_fixtures import SPLIT_PHRASE, SPLIT_REPL


def test_paragraph_helper_replaces_visible_split_phrase_with_first_run_format():
    document = Document()
    paragraph = document.add_paragraph()
    first = paragraph.add_run("Technologies")
    first.bold = True
    first.italic = True
    first.font.size = Pt(16)
    first.font.color.rgb = RGBColor(0x12, 0x34, 0x56)
    paragraph.add_run(", Inc.")

    count = _replace_paragraph_runs(paragraph, (_rule(),))

    assert count == 1
    assert paragraph.text == SPLIT_REPL
    assert paragraph.runs[0].bold is True
    assert paragraph.runs[0].italic is True
    assert paragraph.runs[0].font.size.pt == 16
    assert str(paragraph.runs[0].font.color.rgb) == "123456"


def test_paragraph_helper_does_not_count_internal_run_fragments():
    document = Document()
    paragraph = document.add_paragraph()
    paragraph.add_run("Technologies")
    paragraph.add_run(", Inc.")
    paragraph.add_run(" / Technologies")
    paragraph.add_run(", Inc.")

    count = _replace_paragraph_runs(paragraph, (_rule(),))

    assert count == 2
    assert paragraph.text.count(SPLIT_REPL) == 2


def _rule() -> ReplacementRule:
    return ReplacementRule(no="1", detected_phrase=SPLIT_PHRASE, replacement_proposal=SPLIT_REPL, row_index=2)
