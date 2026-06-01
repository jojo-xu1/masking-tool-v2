from __future__ import annotations

from masking_tool.models import TraversalMode


def test_folder_ui_contract_values():
    assert TraversalMode.DIRECT_CHILDREN.value == "direct_children"
    assert TraversalMode.RECURSIVE.value == "recursive"
