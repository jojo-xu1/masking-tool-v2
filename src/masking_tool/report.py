from __future__ import annotations

from pathlib import Path

from .models import ProcessingResult, ResultStatus, SkipReportEntry

REPORT_NAME = "skipped_unsupported.txt"


def entries_from_results(results: list[ProcessingResult]) -> list[SkipReportEntry]:
    entries: list[SkipReportEntry] = []
    for result in results:
        if result.status in {ResultStatus.SKIPPED_UNSUPPORTED, ResultStatus.FAILED}:
            reason = "; ".join(result.messages) or result.target.reason or result.status.value
            status = result.status.value
        elif result.messages:
            reason = "; ".join(result.messages)
            status = ResultStatus.SKIPPED_UNSUPPORTED.value
        else:
            continue
        entries.append(
            SkipReportEntry(
                relative_path=_stable_path(result.target.relative_path),
                status=status,
                reason=reason,
            )
        )
    return sorted(entries, key=lambda entry: entry.relative_path)


def write_skip_report(output_dir: str | Path, results: list[ProcessingResult]) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    report_path = output_path / REPORT_NAME
    entries = entries_from_results(results)
    lines = ["relative_path\tstatus\treason"]
    for entry in entries:
        lines.append(f"{entry.relative_path}\t{entry.status}\t{entry.reason}")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def _stable_path(path: Path) -> str:
    return path.as_posix()
