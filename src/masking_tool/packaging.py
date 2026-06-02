from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Mapping

APP_TITLE = "Masking Tool"
APP_PURPOSE = "機密情報の検出語句を置換提案へ安全に置換します。"
EXECUTABLE_NAME = "MaskingTool.exe"
DIST_DIR_NAME = "dist"
ENTRY_POINT = "src/main.py"
SPEC_FILE = "packaging/MaskingTool.spec"
DISTRIBUTION_CHECKLIST = "packaging/distribution-checklist.md"
DISTRIBUTION_MODE_ENV = "MASKING_TOOL_DISTRIBUTION_VERIFY"

SUPPORTED_EXTENSION_CHECKS = (
    ".txt",
    ".csv",
    ".log",
    ".docx",
    ".xlsx",
    ".pptx",
    "text-layer .pdf",
)

REGRESSION_CHECK_FIELDS = (
    "replacement_table_checked",
    "file_type_detection_checked",
    "supported_extensions_checked",
    "unsupported_extension_checked",
    "no_match_checked",
    "skip_report_checked",
)

TIMING_FIELDS = (
    "ui_recognition_seconds",
    "sample_single_file_seconds",
    "development_ui_launch_seconds",
    "packaged_exe_launch_seconds",
)


class SmokeMode(str, Enum):
    NORMAL = "normal"
    DISTRIBUTION = "distribution"


class PackagedSmokeDecision(str, Enum):
    RUN = "run"
    SKIP = "skip"


@dataclass(frozen=True)
class DistributionVerificationResult:
    core_tests_passed: bool = False
    replacement_table_checked: bool = False
    file_type_detection_checked: bool = False
    supported_extensions_checked: bool = False
    unsupported_extension_checked: bool = False
    no_match_checked: bool = False
    exe_exists: bool = False
    exe_launch_checked: bool = False
    single_file_checked: bool = False
    folder_run_checked: bool = False
    skip_report_checked: bool = False
    pdf_japanese_checked: bool = False
    ui_recognition_seconds: float | None = None
    sample_single_file_seconds: float | None = None
    development_ui_launch_seconds: float | None = None
    packaged_exe_launch_seconds: float | None = None
    verification_mode: SmokeMode = SmokeMode.NORMAL
    notes: str = ""


def repository_root(start: Path | None = None) -> Path:
    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").exists():
            return candidate
    return Path.cwd().resolve()


def expected_executable_path(root: Path | None = None) -> Path:
    base = root if root is not None else repository_root()
    return base / DIST_DIR_NAME / EXECUTABLE_NAME


def is_distribution_verification_mode(env: Mapping[str, str] | None = None) -> bool:
    source = env if env is not None else os.environ
    return source.get(DISTRIBUTION_MODE_ENV, "").strip().lower() in {
        "1",
        "true",
        "yes",
        "distribution",
    }


def packaged_smoke_decision(
    exe_path: Path | None = None,
    *,
    distribution_mode: bool | None = None,
) -> PackagedSmokeDecision:
    path = exe_path if exe_path is not None else expected_executable_path()
    is_distribution = is_distribution_verification_mode() if distribution_mode is None else distribution_mode
    if path.exists() and path.is_file():
        return PackagedSmokeDecision.RUN
    if is_distribution:
        raise FileNotFoundError(f"{path} is required for distribution verification mode.")
    return PackagedSmokeDecision.SKIP


def required_checklist_labels() -> tuple[str, ...]:
    return (
        "Replacement table loading",
        "File type detection",
        "Supported extensions",
        "Unsupported extensions",
        "No-match inputs",
        "Skipped unsupported report",
        "PDF Japanese readability",
        "UI recognition seconds",
        "Sample single-file seconds",
        "Development UI launch seconds",
        "Packaged exe launch seconds",
    )
