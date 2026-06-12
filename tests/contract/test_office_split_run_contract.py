from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = ROOT / "specs" / "004-docx-pptx-run-replacement" / "spec.md"
CONTRACT = ROOT / "specs" / "004-docx-pptx-run-replacement" / "contracts" / "office-replacement-contract.md"


def test_split_run_scope_is_limited_to_single_visible_container():
    text = SPEC.read_text(encoding="utf-8") + CONTRACT.read_text(encoding="utf-8")

    for term in ("same paragraph", "same text box", "same table cell"):
        assert term in text
    assert "MUST NOT cross paragraph, text-box, or table-cell boundaries" in text


def test_split_run_formatting_and_count_contract_are_explicit():
    text = SPEC.read_text(encoding="utf-8")

    for term in ("bold", "italic", "font size", "color"):
        assert term in text
    assert "1 つの可視語句を 1 件" in text


def test_detectable_out_of_scope_office_content_must_be_reported():
    text = SPEC.read_text(encoding="utf-8")

    assert "skipped_unsupported.txt" in text
    assert "detectable out-of-scope Office content" in text
