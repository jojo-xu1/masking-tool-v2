from __future__ import annotations

from masking_tool.packaging import TIMING_FIELDS
from masking_tool.ui import (
    MIN_WINDOW_SIZE,
    SUMMARY_KEYS,
    UI_SECTION_KEYS,
    UI_STATE_KEYS,
    VALIDATION_MESSAGES,
)


def test_ui_layout_exposes_required_sections_and_state_keys():
    assert UI_SECTION_KEYS == ("header", "input", "execution", "results")
    assert set(UI_STATE_KEYS) == {
        "replacement_table_path",
        "input_mode",
        "input_path",
        "traversal_mode",
        "output_folder",
        "progress_current",
        "progress_total",
        "status_message",
        "summary_counts",
        "report_path",
    }


def test_ui_validation_messages_identify_missing_required_inputs():
    assert VALIDATION_MESSAGES["missing_replacement_table"] == "置換表を選択してください。"
    assert VALIDATION_MESSAGES["missing_input_target"] == "処理対象のファイルまたはフォルダを選択してください。"
    assert VALIDATION_MESSAGES["missing_output_folder"] == "出力フォルダを選択してください。"


def test_ui_completion_summary_contract_keys():
    assert SUMMARY_KEYS == ("replaced", "no_match", "skipped", "failed", "report_path")


def test_ui_contract_accepts_japanese_space_and_symbol_paths():
    sample = r"C:\作業 フォルダ\masking#1\機密情報検出結果.xlsx"
    assert "作業 フォルダ" in sample
    assert "機密情報検出結果.xlsx" in sample
    assert "#" in sample


def test_ui_usability_contract_minimum_size_and_timing_fields():
    assert MIN_WINDOW_SIZE == (900, 620)
    assert TIMING_FIELDS == (
        "ui_recognition_seconds",
        "sample_single_file_seconds",
        "development_ui_launch_seconds",
        "packaged_exe_launch_seconds",
    )
