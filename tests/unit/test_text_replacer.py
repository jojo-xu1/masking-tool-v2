from __future__ import annotations

from masking_tool.models import ReplacementRule
from masking_tool.replacement_table import sort_rules
from masking_tool.text_replacer import replace_text


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
