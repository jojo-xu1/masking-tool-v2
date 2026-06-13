from __future__ import annotations

from masking_tool.models import ReplacementRule
from masking_tool.replacement_table import sort_rules
from masking_tool.text_replacer import replace_text, width_equivalent_key
from tests.fixtures.create_fixtures import UNICODE_FULL_WIDTH_PHRASE, UNICODE_HALF_WIDTH_PHRASE, UNICODE_REPL


def test_deterministic_phrase_replacement_with_overlaps():
    rules = sort_rules(
        [
            ReplacementRule("2", "山田", "<LAST>", 3),
            ReplacementRule("1", "山田太郎", "<PERSON>", 2),
        ]
    )

    result, count = replace_text("山田太郎 と 山田", rules)

    assert result == "<PERSON> と <LAST>"
    assert count == 2


def test_width_equivalent_key_folds_only_ascii_compatible_width():
    assert width_equivalent_key(UNICODE_FULL_WIDTH_PHRASE) == UNICODE_HALF_WIDTH_PHRASE
    assert width_equivalent_key("東京ＡＢＣ") == "東京ABC"
    assert width_equivalent_key("東京株式会社") == "東京株式会社"


def test_exact_raw_match_precedence_over_width_equivalent_candidate():
    rules = sort_rules(
        [
            ReplacementRule("1", UNICODE_FULL_WIDTH_PHRASE, "WIDTH_EQUIVALENT", 2),
            ReplacementRule("2", UNICODE_HALF_WIDTH_PHRASE, "EXACT_RAW", 3),
        ]
    )

    result, count = replace_text(UNICODE_HALF_WIDTH_PHRASE, rules)

    assert result == "EXACT_RAW"
    assert count == 1


def test_visually_similar_non_width_equivalent_characters_do_not_match():
    rules = sort_rules([ReplacementRule("1", "A", UNICODE_REPL, 2)])

    result, count = replace_text("Α", rules)

    assert result == "Α"
    assert count == 0
