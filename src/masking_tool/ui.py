from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .app import process_selection
from .models import InputMode, InputSelection, TraversalMode

VALIDATION_MESSAGES = {
    "missing_replacement_table": "置換表を選択してください。",
    "invalid_replacement_table_headers": "`No`, `検出語句`, `置換提案` 列が必要です。",
    "invalid_replacement_row": "置換表に空欄または重複した検出語句があります。",
    "missing_input_target": "処理対象のファイルまたはフォルダを選択してください。",
    "missing_output_folder": "出力フォルダを選択してください。",
    "no_supported_files": "対象フォルダに対応ファイルがありません。",
}


class MaskingToolUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Masking Tool")
        self.replacement_table = tk.StringVar()
        self.input_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.input_mode = tk.StringVar(value=InputMode.SINGLE_FILE.value)
        self.traversal_mode = tk.StringVar(value=TraversalMode.DIRECT_CHILDREN.value)
        self.status = tk.StringVar(value="")
        self.progress = tk.StringVar(value="")
        self._cancel_requested = False
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.grid(sticky="nsew")
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="置換表").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.replacement_table, width=60).grid(row=0, column=1, sticky="ew")
        ttk.Button(frame, text="選択", command=self.pick_replacement_table).grid(row=0, column=2)

        ttk.Label(frame, text="入力種別").grid(row=1, column=0, sticky="w")
        mode_frame = ttk.Frame(frame)
        mode_frame.grid(row=1, column=1, sticky="w")
        ttk.Radiobutton(mode_frame, text="ファイル", variable=self.input_mode, value=InputMode.SINGLE_FILE.value).grid(row=0, column=0)
        ttk.Radiobutton(mode_frame, text="フォルダ", variable=self.input_mode, value=InputMode.FOLDER.value).grid(row=0, column=1)

        ttk.Label(frame, text="処理対象").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.input_path, width=60).grid(row=2, column=1, sticky="ew")
        ttk.Button(frame, text="選択", command=self.pick_input).grid(row=2, column=2)

        ttk.Label(frame, text="フォルダ範囲").grid(row=3, column=0, sticky="w")
        traversal = ttk.Frame(frame)
        traversal.grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(traversal, text="直下のみ", variable=self.traversal_mode, value=TraversalMode.DIRECT_CHILDREN.value).grid(row=0, column=0)
        ttk.Radiobutton(traversal, text="サブフォルダ含む", variable=self.traversal_mode, value=TraversalMode.RECURSIVE.value).grid(row=0, column=1)

        ttk.Label(frame, text="出力フォルダ").grid(row=4, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.output_folder, width=60).grid(row=4, column=1, sticky="ew")
        ttk.Button(frame, text="選択", command=self.pick_output).grid(row=4, column=2)

        buttons = ttk.Frame(frame)
        buttons.grid(row=5, column=1, sticky="w")
        self.start_button = ttk.Button(buttons, text="開始", command=self.start)
        self.start_button.grid(row=0, column=0)
        ttk.Button(buttons, text="キャンセル", command=self.cancel).grid(row=0, column=1)

        ttk.Label(frame, textvariable=self.progress).grid(row=6, column=0, columnspan=3, sticky="w")
        ttk.Label(frame, textvariable=self.status).grid(row=7, column=0, columnspan=3, sticky="w")

    def pick_replacement_table(self) -> None:
        value = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if value:
            self.replacement_table.set(value)

    def pick_input(self) -> None:
        if self.input_mode.get() == InputMode.FOLDER.value:
            value = filedialog.askdirectory()
        else:
            value = filedialog.askopenfilename()
        if value:
            self.input_path.set(value)

    def pick_output(self) -> None:
        value = filedialog.askdirectory()
        if value:
            self.output_folder.set(value)

    def validate(self) -> str | None:
        if not self.replacement_table.get():
            return VALIDATION_MESSAGES["missing_replacement_table"]
        if not self.input_path.get():
            return VALIDATION_MESSAGES["missing_input_target"]
        if not self.output_folder.get():
            return VALIDATION_MESSAGES["missing_output_folder"]
        return None

    def start(self) -> None:
        error = self.validate()
        if error:
            messagebox.showerror("入力エラー", error)
            return
        self.start_button.configure(state="disabled")
        self._cancel_requested = False
        thread = threading.Thread(target=self._run_processing, daemon=True)
        thread.start()

    def cancel(self) -> None:
        self._cancel_requested = True

    def _run_processing(self) -> None:
        try:
            selection = InputSelection(
                mode=InputMode(self.input_mode.get()),
                input_path=Path(self.input_path.get()),
                output_directory=Path(self.output_folder.get()),
                traversal_mode=TraversalMode(self.traversal_mode.get()),
            )
            summary = process_selection(
                self.replacement_table.get(),
                selection,
                progress=lambda current, total, path: self._set_progress(current, total, path),
                should_cancel=lambda: self._cancel_requested,
            )
            self.root.after(0, lambda: self._complete(summary))
        except Exception as exc:
            self.root.after(0, lambda: self._fail(exc))

    def _set_progress(self, current: int, total: int, path: Path) -> None:
        self.root.after(0, lambda: self.progress.set(f"{current}/{total}: {path.as_posix()}"))

    def _complete(self, summary) -> None:
        self.start_button.configure(state="normal")
        cancelled = "キャンセル済み " if summary.cancelled else ""
        self.status.set(
            f"{cancelled}置換:{summary.replaced_count} 未検出:{summary.processed_no_matches_count} "
            f"対象外:{summary.skipped_unsupported_count} 失敗:{summary.failed_count} "
            f"レポート:{summary.report_path}"
        )

    def _fail(self, exc: Exception) -> None:
        self.start_button.configure(state="normal")
        messagebox.showerror("処理エラー", str(exc))


def main() -> None:
    root = tk.Tk()
    MaskingToolUI(root)
    root.mainloop()
