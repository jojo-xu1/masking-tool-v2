from __future__ import annotations

from pathlib import Path

from .models import InputMode, InputSelection, InputTarget, SupportStatus, TraversalMode

SUPPORTED_EXTENSIONS = {".txt", ".csv", ".log", ".docx", ".xlsx", ".pptx", ".pdf"}


def is_supported_extension(path: str | Path) -> bool:
    return Path(path).suffix.lower() in SUPPORTED_EXTENSIONS


def discover_targets(selection: InputSelection) -> list[InputTarget]:
    input_path = selection.input_path
    if not input_path.exists():
        raise FileNotFoundError(f"Input path not found: {input_path}")

    if selection.mode == InputMode.SINGLE_FILE:
        if not input_path.is_file():
            raise ValueError("Single-file mode requires a file path.")
        return [_target_for(input_path, Path(input_path.name))]

    if not input_path.is_dir():
        raise ValueError("Folder mode requires a folder path.")

    if selection.traversal_mode == TraversalMode.RECURSIVE:
        files = [p for p in input_path.rglob("*") if p.is_file()]
    else:
        files = [p for p in input_path.iterdir() if p.is_file()]

    return [_target_for(path, path.relative_to(input_path)) for path in sorted(files)]


def _target_for(path: Path, relative_path: Path) -> InputTarget:
    extension = path.suffix.lower()
    if extension in SUPPORTED_EXTENSIONS:
        return InputTarget(path, relative_path, extension, SupportStatus.SUPPORTED)
    return InputTarget(
        path,
        relative_path,
        extension,
        SupportStatus.UNSUPPORTED_EXTENSION,
        f"unsupported extension {extension or '<none>'}",
    )
