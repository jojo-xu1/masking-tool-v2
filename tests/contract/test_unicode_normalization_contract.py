from __future__ import annotations

from masking_tool.models import ReplacementRule
from masking_tool.replacement_table import sort_rules
from masking_tool.text_replacer import replace_text, width_equivalent_key
from tests.fixtures.create_fixtures import (
    UNICODE_FULL_WIDTH_PHRASE,
    UNICODE_FULL_WIDTH_REPL,
    UNICODE_HALF_WIDTH_PHRASE,
    UNICODE_REPL,
)


def test_full_width_detected_phrase_matches_half_width_target_contract():
    rules = sort_rules([ReplacementRule("1", UNICODE_FULL_WIDTH_PHRASE, UNICODE_REPL, 2)])

    result, count = replace_text(f"取引先: {UNICODE_HALF_WIDTH_PHRASE}", rules)

    assert count == 1
    assert UNICODE_HALF_WIDTH_PHRASE not in result
    assert UNICODE_REPL in result


def test_half_width_detected_phrase_matches_full_width_target_contract():
    rules = sort_rules([ReplacementRule("1", UNICODE_HALF_WIDTH_PHRASE, UNICODE_REPL, 2)])

    result, count = replace_text(f"取引先: {UNICODE_FULL_WIDTH_PHRASE}", rules)

    assert count == 1
    assert UNICODE_FULL_WIDTH_PHRASE not in result
    assert UNICODE_REPL in result


def test_exact_raw_match_wins_over_width_equivalent_match_contract():
    rules = sort_rules(
        [
            ReplacementRule("1", UNICODE_FULL_WIDTH_PHRASE, "WIDTH_EQUIVALENT", 2),
            ReplacementRule("2", UNICODE_HALF_WIDTH_PHRASE, "EXACT_RAW", 3),
        ]
    )

    result, count = replace_text(UNICODE_HALF_WIDTH_PHRASE, rules)

    assert count == 1
    assert result == "EXACT_RAW"


def test_cjk_and_replacement_proposal_preservation_contract():
    rules = sort_rules([ReplacementRule("1", UNICODE_HALF_WIDTH_PHRASE, UNICODE_FULL_WIDTH_REPL, 2)])

    result, count = replace_text(f"東京本社 {UNICODE_FULL_WIDTH_PHRASE} 完了", rules)

    assert count == 1
    assert result == f"東京本社 {UNICODE_FULL_WIDTH_REPL} 完了"
    assert "東京本社" in result
    assert "完了" in result


def test_width_key_does_not_fold_unrelated_cjk_characters_contract():
    assert width_equivalent_key("東京ＡＢＣ") == "東京ABC"
    assert width_equivalent_key("東京株式会社") == "東京株式会社"
