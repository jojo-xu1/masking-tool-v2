from __future__ import annotations

from pathlib import Path
from shutil import copy2
from typing import Callable

from .models import (
    InputSelection,
    ProcessingResult,
    ProcessingSummary,
    ResultStatus,
    SupportStatus,
)
from .office_replacer import replace_docx, replace_pptx, replace_xlsx
from .pdf_replacer import ExcludedPdfError, replace_pdf
from .replacement_table import load_replacement_table
from .report import write_skip_report
from .scanner import discover_targets
from .text_replacer import replace_text_file

ProgressCallback = Callable[[int, int, Path], None]
CancelCallback = Callable[[], bool]


def process_selection(
    replacement_table_path: str | Path,
    selection: InputSelection,
    progress: ProgressCallback | None = None,
    should_cancel: CancelCallback | None = None,
) -> ProcessingSummary:
    table = load_replacement_table(replacement_table_path)
    selection.output_directory.mkdir(parents=True, exist_ok=True)
    targets = discover_targets(selection)
    results: list[ProcessingResult] = []
    cancelled = False

    for index, target in enumerate(targets, start=1):
        if progress:
            progress(index, len(targets), target.relative_path)
        if should_cancel and should_cancel():
            cancelled = True
            break
        results.append(_process_target(target, selection.output_directory, table.rules))

    report_path = write_skip_report(selection.output_directory, results)
    return ProcessingSummary(results=results, report_path=report_path, cancelled=cancelled)


def _process_target(target, output_directory: Path, rules) -> ProcessingResult:
    if target.support_status != SupportStatus.SUPPORTED:
        return ProcessingResult(
            target=target,
            status=ResultStatus.SKIPPED_UNSUPPORTED,
            messages=[target.reason],
        )

    output_path = safe_output_path(output_directory, target)
    try:
        count, messages = _dispatch_replace(target.source_path, output_path, target.extension, rules)
        status = ResultStatus.REPLACED if count else ResultStatus.PROCESSED_NO_MATCHES
        return ProcessingResult(target, status, output_path, count, messages)
    except ExcludedPdfError as exc:
        return ProcessingResult(
            target=target,
            status=ResultStatus.SKIPPED_UNSUPPORTED,
            output_path=None,
            messages=[str(exc)],
        )
    except Exception as exc:
        return ProcessingResult(
            target=target,
            status=ResultStatus.FAILED,
            output_path=None,
            messages=[_safe_error(exc)],
        )


def safe_output_path(output_directory: Path, target) -> Path:
    output_path = output_directory / target.relative_path
    try:
        if output_path.resolve() == target.source_path.resolve():
            return output_path.with_name(f"{output_path.stem}_masked{output_path.suffix}")
    except FileNotFoundError:
        pass
    return output_path


def _dispatch_replace(source: Path, output: Path, extension: str, rules) -> tuple[int, list[str]]:
    if extension in {".txt", ".csv", ".log"}:
        return replace_text_file(source, output, rules), []
    if extension == ".docx":
        return replace_docx(source, output, rules)
    if extension == ".xlsx":
        return replace_xlsx(source, output, rules)
    if extension == ".pptx":
        return replace_pptx(source, output, rules)
    if extension == ".pdf":
        return replace_pdf(source, output, rules)
    return 0, [f"unsupported extension {extension}"]


def _safe_error(exc: Exception) -> str:
    message = str(exc).strip()
    return message or exc.__class__.__name__
