from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class InputMode(str, Enum):
    SINGLE_FILE = "single_file"
    FOLDER = "folder"


class TraversalMode(str, Enum):
    DIRECT_CHILDREN = "direct_children"
    RECURSIVE = "recursive"


class SupportStatus(str, Enum):
    SUPPORTED = "supported"
    UNSUPPORTED_EXTENSION = "unsupported_extension"
    EXCLUDED_CONTENT = "excluded_content"
    UNPROCESSABLE = "unprocessable"


class ResultStatus(str, Enum):
    REPLACED = "replaced"
    PROCESSED_NO_MATCHES = "processed_no_matches"
    SKIPPED_UNSUPPORTED = "skipped_unsupported"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ReplacementTableError(ValueError):
    """Raised when the replacement spreadsheet is invalid."""


@dataclass(frozen=True)
class ReplacementRule:
    no: str
    detected_phrase: str
    replacement_proposal: str
    row_index: int


@dataclass(frozen=True)
class ReplacementTable:
    path: Path
    rules: tuple[ReplacementRule, ...]
    source_headers: tuple[str, ...]


@dataclass(frozen=True)
class InputSelection:
    mode: InputMode
    input_path: Path
    output_directory: Path
    traversal_mode: TraversalMode = TraversalMode.DIRECT_CHILDREN


@dataclass(frozen=True)
class InputTarget:
    source_path: Path
    relative_path: Path
    extension: str
    support_status: SupportStatus
    reason: str = ""


@dataclass
class ProcessingResult:
    target: InputTarget
    status: ResultStatus
    output_path: Path | None = None
    replacement_count: int = 0
    messages: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SkipReportEntry:
    relative_path: str
    status: str
    reason: str


@dataclass
class ProcessingSummary:
    results: list[ProcessingResult]
    report_path: Path
    cancelled: bool = False

    @property
    def replaced_count(self) -> int:
        return sum(1 for r in self.results if r.status == ResultStatus.REPLACED)

    @property
    def processed_no_matches_count(self) -> int:
        return sum(1 for r in self.results if r.status == ResultStatus.PROCESSED_NO_MATCHES)

    @property
    def skipped_unsupported_count(self) -> int:
        return sum(1 for r in self.results if r.status == ResultStatus.SKIPPED_UNSUPPORTED)

    @property
    def failed_count(self) -> int:
        return sum(1 for r in self.results if r.status == ResultStatus.FAILED)
