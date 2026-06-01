from __future__ import annotations

from masking_tool.ui import VALIDATION_MESSAGES


def test_single_file_ui_contract_messages_and_controls():
    assert VALIDATION_MESSAGES["missing_replacement_table"] == "置換表を選択してください。"
    assert VALIDATION_MESSAGES["missing_input_target"] == "処理対象のファイルまたはフォルダを選択してください。"
    assert VALIDATION_MESSAGES["missing_output_folder"] == "出力フォルダを選択してください。"
