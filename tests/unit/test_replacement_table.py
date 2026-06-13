from __future__ import annotations

import pytest

from masking_tool.models import ReplacementTableError
from masking_tool.replacement_table import load_replacement_table
from tests.fixtures.create_fixtures import (
    UNICODE_FULL_WIDTH_PHRASE,
    UNICODE_FULL_WIDTH_REPL,
    create_invalid_replacement_table,
    create_replacement_table,
)


def test_replacement_table_accepts_required_headers(tmp_path):
    path = create_replacement_table(tmp_path / "機密情報検出結果.xlsx")

    table = load_replacement_table(path)

    assert [rule.detected_phrase for rule in table.rules] == ["example@example.com", "山田太郎"]


def test_replacement_table_rejects_missing_headers(tmp_path):
    path = create_invalid_replacement_table(tmp_path / "bad.xlsx", ["No", "検出語句"])

    with pytest.raises(ReplacementTableError, match="列が必要"):
        load_replacement_table(path)


def test_replacement_table_rejects_blank_and_duplicate_rows(tmp_path):
    blank = create_replacement_table(tmp_path / "blank.xlsx", [(1, "", "<PERSON_001>")])
    duplicate = create_replacement_table(
        tmp_path / "duplicate.xlsx",
        [(1, "山田太郎", "<PERSON_001>"), (2, "山田太郎", "<PERSON_002>")],
    )

    with pytest.raises(ReplacementTableError):
        load_replacement_table(blank)
    with pytest.raises(ReplacementTableError):
        load_replacement_table(duplicate)


def test_replacement_table_preserves_unicode_width_values(tmp_path):
    path = create_replacement_table(
        tmp_path / "unicode.xlsx",
        [(1, UNICODE_FULL_WIDTH_PHRASE, UNICODE_FULL_WIDTH_REPL)],
    )

    table = load_replacement_table(path)

    assert table.rules[0].detected_phrase == UNICODE_FULL_WIDTH_PHRASE
    assert table.rules[0].replacement_proposal == UNICODE_FULL_WIDTH_REPL
