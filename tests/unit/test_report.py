from __future__ import annotations

from pathlib import Path

from masking_tool.models import InputTarget, ProcessingResult, ResultStatus, SupportStatus
from masking_tool.report import write_skip_report


def test_skip_report_format_sorting_and_empty_report(tmp_path):
    output = tmp_path / "out"
    report = write_skip_report(output, [])
    assert report.read_text(encoding="utf-8") == "relative_path\tstatus\treason\n"

    results = [
        ProcessingResult(
            InputTarget(tmp_path / "b.bin", Path("b.bin"), ".bin", SupportStatus.UNSUPPORTED_EXTENSION),
            ResultStatus.SKIPPED_UNSUPPORTED,
            messages=["unsupported extension .bin"],
        ),
        ProcessingResult(
            InputTarget(tmp_path / "a.pdf", Path("docs/a.pdf"), ".pdf", SupportStatus.SUPPORTED),
            ResultStatus.FAILED,
            messages=["could not open"],
        ),
    ]

    report = write_skip_report(output, results)
    lines = report.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "relative_path\tstatus\treason"
    assert lines[1].startswith("b.bin\tskipped_unsupported") or lines[1].startswith("docs/a.pdf\tfailed")
    assert sorted(lines[1:]) == lines[1:]
