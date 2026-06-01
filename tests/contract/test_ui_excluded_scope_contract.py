from __future__ import annotations

from masking_tool.models import ResultStatus


def test_excluded_content_is_not_success_status():
    assert ResultStatus.SKIPPED_UNSUPPORTED.value == "skipped_unsupported"
    assert ResultStatus.SKIPPED_UNSUPPORTED != ResultStatus.REPLACED
