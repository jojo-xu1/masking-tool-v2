from __future__ import annotations

from pathlib import Path

from masking_tool.packaging import (
    DISTRIBUTION_CHECKLIST,
    ENTRY_POINT,
    EXECUTABLE_NAME,
    REGRESSION_CHECK_FIELDS,
    SPEC_FILE,
    TIMING_FIELDS,
    SmokeMode,
    expected_executable_path,
    required_checklist_labels,
)


ROOT = Path(__file__).resolve().parents[2]


def test_packaging_contract_executable_identity_and_paths():
    assert EXECUTABLE_NAME == "MaskingTool.exe"
    assert ENTRY_POINT == "src/main.py"
    assert SPEC_FILE == "packaging/MaskingTool.spec"
    assert DISTRIBUTION_CHECKLIST == "packaging/distribution-checklist.md"
    assert expected_executable_path(ROOT) == ROOT / "dist" / "MaskingTool.exe"


def test_pyinstaller_spec_uses_onefile_ui_entry_point():
    spec_text = (ROOT / "packaging" / "MaskingTool.spec").read_text(encoding="utf-8")
    assert "src_dir / \"main.py\"" in spec_text
    assert "name=\"MaskingTool\"" in spec_text
    assert "console=False" in spec_text
    assert "COLLECT(" not in spec_text


def test_build_script_cleans_and_verifies_expected_exe():
    script = (ROOT / "packaging" / "build_exe.ps1").read_text(encoding="utf-8")
    assert "dist\\MaskingTool.exe" in script
    assert "Remove-Item" in script
    assert "python -m PyInstaller" in script
    assert "Expected executable was not created" in script


def test_distribution_checklist_contains_required_verification_fields():
    checklist = (ROOT / "packaging" / "distribution-checklist.md").read_text(encoding="utf-8")
    for label in required_checklist_labels():
        assert label in checklist
    assert "Missing exe fails distribution verification mode" in checklist
    assert "Normal smoke mode skips packaged checks" in checklist


def test_per_format_regression_gate_contract():
    checklist = (ROOT / "packaging" / "distribution-checklist.md").read_text(encoding="utf-8")
    for extension in [".txt", ".csv", ".log", ".docx", ".xlsx", ".pptx", "text-layer `.pdf`"]:
        assert extension in checklist
    assert REGRESSION_CHECK_FIELDS == (
        "replacement_table_checked",
        "file_type_detection_checked",
        "supported_extensions_checked",
        "unsupported_extension_checked",
        "no_match_checked",
        "skip_report_checked",
    )


def test_timing_fields_are_distribution_contract():
    assert TIMING_FIELDS == (
        "ui_recognition_seconds",
        "sample_single_file_seconds",
        "development_ui_launch_seconds",
        "packaged_exe_launch_seconds",
    )


def test_smoke_mode_values_are_stable():
    assert SmokeMode.NORMAL.value == "normal"
    assert SmokeMode.DISTRIBUTION.value == "distribution"
