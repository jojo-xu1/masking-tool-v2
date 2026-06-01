from __future__ import annotations

from pathlib import Path

from masking_tool.models import InputMode, InputSelection, SupportStatus, TraversalMode
from masking_tool.scanner import discover_targets, is_supported_extension


def test_supported_extensions():
    assert is_supported_extension("a.txt")
    assert is_supported_extension("a.PDF")
    assert not is_supported_extension("a.bin")


def test_direct_children_scanning(tmp_path):
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "b.txt").write_text("x", encoding="utf-8")
    selection = InputSelection(InputMode.FOLDER, tmp_path, tmp_path / "out", TraversalMode.DIRECT_CHILDREN)

    targets = discover_targets(selection)

    assert [target.relative_path for target in targets] == [Path("a.txt")]


def test_recursive_scanning_and_unsupported_status(tmp_path):
    (tmp_path / "a.bin").write_text("x", encoding="utf-8")
    (tmp_path / "nested").mkdir()
    (tmp_path / "nested" / "b.txt").write_text("x", encoding="utf-8")
    selection = InputSelection(InputMode.FOLDER, tmp_path, tmp_path / "out", TraversalMode.RECURSIVE)

    targets = discover_targets(selection)

    by_path = {target.relative_path.as_posix(): target for target in targets}
    assert by_path["a.bin"].support_status == SupportStatus.UNSUPPORTED_EXTENSION
    assert by_path["nested/b.txt"].support_status == SupportStatus.SUPPORTED
