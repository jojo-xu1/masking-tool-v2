from __future__ import annotations

import pytest

from masking_tool.packaging import PackagedSmokeDecision, packaged_smoke_decision


def test_normal_smoke_mode_skips_when_exe_is_absent(tmp_path):
    missing_exe = tmp_path / "dist" / "MaskingTool.exe"

    decision = packaged_smoke_decision(missing_exe, distribution_mode=False)

    assert decision == PackagedSmokeDecision.SKIP


def test_distribution_verification_mode_fails_when_exe_is_absent(tmp_path):
    missing_exe = tmp_path / "dist" / "MaskingTool.exe"

    with pytest.raises(FileNotFoundError):
        packaged_smoke_decision(missing_exe, distribution_mode=True)


def test_packaged_launch_readiness_when_exe_exists(tmp_path):
    exe = tmp_path / "dist" / "MaskingTool.exe"
    exe.parent.mkdir(parents=True)
    exe.write_bytes(b"MZ")

    decision = packaged_smoke_decision(exe, distribution_mode=True)

    assert decision == PackagedSmokeDecision.RUN


def test_packaged_manual_sample_paths_are_available():
    replacement_table = "tests/fixtures/replacement_tables/機密情報検出結果_manual_sensitive.xlsx"
    manual_samples = "tests/fixtures/inputs/manual_sensitive_samples/"

    assert replacement_table.endswith("機密情報検出結果_manual_sensitive.xlsx")
    assert manual_samples.endswith("manual_sensitive_samples/")
