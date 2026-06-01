from __future__ import annotations

from pathlib import Path

from .models import ReplacementRule

TEXT_EXTENSIONS = {".txt", ".csv", ".log"}


def replace_text(text: str, rules: tuple[ReplacementRule, ...] | list[ReplacementRule]) -> tuple[str, int]:
    total = 0
    result = text
    for rule in rules:
        count = result.count(rule.detected_phrase)
        if count:
            result = result.replace(rule.detected_phrase, rule.replacement_proposal)
            total += count
    return result, total


def replace_text_file(source: str | Path, output: str | Path, rules: tuple[ReplacementRule, ...]) -> int:
    source_path = Path(source)
    output_path = Path(output)
    text = _read_text(source_path)
    replaced, count = replace_text(text, rules)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(replaced, encoding="utf-8")
    return count


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp932")
