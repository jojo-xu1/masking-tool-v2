from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import unicodedata

from .models import ReplacementRule

TEXT_EXTENSIONS = {".txt", ".csv", ".log"}


@dataclass(frozen=True)
class ReplacementMatch:
    start: int
    end: int
    replacement: str


@dataclass(frozen=True)
class _Candidate:
    start: int
    end: int
    rule: ReplacementRule
    rule_order: int
    exact: bool


def replace_text(text: str, rules: tuple[ReplacementRule, ...] | list[ReplacementRule]) -> tuple[str, int]:
    matches = plan_replacements(text, rules)
    if not matches:
        return text, 0

    result: list[str] = []
    cursor = 0
    for match in matches:
        result.append(text[cursor : match.start])
        result.append(match.replacement)
        cursor = match.end
    result.append(text[cursor:])
    return "".join(result), len(matches)


def plan_replacements(
    text: str,
    rules: tuple[ReplacementRule, ...] | list[ReplacementRule],
) -> list[ReplacementMatch]:
    candidates = _find_candidates(text, tuple(rules))
    selected: list[_Candidate] = []
    occupied: list[tuple[int, int]] = []
    exact_spans = {(candidate.start, candidate.end) for candidate in candidates if candidate.exact}

    for candidate in sorted(candidates, key=lambda item: (item.rule_order, item.start, item.end)):
        if not candidate.exact and (candidate.start, candidate.end) in exact_spans:
            continue
        if any(_overlaps(candidate.start, candidate.end, start, end) for start, end in occupied):
            continue
        selected.append(candidate)
        occupied.append((candidate.start, candidate.end))

    return [
        ReplacementMatch(candidate.start, candidate.end, candidate.rule.replacement_proposal)
        for candidate in sorted(selected, key=lambda item: item.start)
    ]


def width_equivalent_key(text: str) -> str:
    return "".join(_fold_ascii_width(character) for character in text)


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


def _find_candidates(text: str, rules: tuple[ReplacementRule, ...]) -> list[_Candidate]:
    text_key, index_map = _width_key_with_index_map(text)
    candidates: list[_Candidate] = []
    for rule_order, rule in enumerate(rules):
        candidates.extend(_find_exact_candidates(text, rule, rule_order))
        candidates.extend(_find_width_candidates(text, text_key, index_map, rule, rule_order))
    return candidates


def _find_exact_candidates(text: str, rule: ReplacementRule, rule_order: int) -> list[_Candidate]:
    candidates: list[_Candidate] = []
    cursor = 0
    while rule.detected_phrase:
        start = text.find(rule.detected_phrase, cursor)
        if start == -1:
            break
        end = start + len(rule.detected_phrase)
        candidates.append(_Candidate(start, end, rule, rule_order, exact=True))
        cursor = end
    return candidates


def _find_width_candidates(
    text: str,
    text_key: str,
    index_map: list[tuple[int, int]],
    rule: ReplacementRule,
    rule_order: int,
) -> list[_Candidate]:
    phrase_key = width_equivalent_key(rule.detected_phrase)
    if not phrase_key:
        return []

    candidates: list[_Candidate] = []
    cursor = 0
    while True:
        key_start = text_key.find(phrase_key, cursor)
        if key_start == -1:
            break
        key_end = key_start + len(phrase_key)
        raw_start = index_map[key_start][0]
        raw_end = index_map[key_end - 1][1]
        if text[raw_start:raw_end] != rule.detected_phrase:
            candidates.append(_Candidate(raw_start, raw_end, rule, rule_order, exact=False))
        cursor = key_end
    return candidates


def _width_key_with_index_map(text: str) -> tuple[str, list[tuple[int, int]]]:
    key_parts: list[str] = []
    index_map: list[tuple[int, int]] = []
    for index, character in enumerate(text):
        folded = _fold_ascii_width(character)
        key_parts.append(folded)
        index_map.extend((index, index + 1) for _ in folded)
    return "".join(key_parts), index_map


def _fold_ascii_width(character: str) -> str:
    folded = unicodedata.normalize("NFKC", character)
    if folded and all(ord(item) < 128 for item in folded):
        return folded
    return character


def _overlaps(left_start: int, left_end: int, right_start: int, right_end: int) -> bool:
    return left_start < right_end and right_start < left_end
