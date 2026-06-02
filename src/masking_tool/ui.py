from __future__ import annotations

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .app import process_selection
from .models import InputMode, InputSelection, TraversalMode
from .packaging import APP_PURPOSE, APP_TITLE, TIMING_FIELDS

MIN_WINDOW_SIZE = (900, 620)

UI_SECTION_KEYS = (
    "header",
    "input",
    "execution",
    "results",
)

UI_STATE_KEYS = (
    "replacement_table_path",
    "input_mode",
    "input_path",
    "traversal_mode",
    "output_folder",
    "progress_current",
    "progress_total",
    "status_message",
    "summary_counts",
    "report_path",
)

SUMMARY_KEYS = (
    "replaced",
    "no_match",
    "skipped",
    "failed",
    "report_path",
)

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
        self.root.title(APP_TITLE)
        self.root.minsize(*MIN_WINDOW_SIZE)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.replacement_table = tk.StringVar()
        self.input_path = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.input_mode = tk.StringVar(value=InputMode.SINGLE_FILE.value)
        self.traversal_mode = tk.StringVar(value=TraversalMode.DIRECT_CHILDREN.value)
        self.status = tk.StringVar(value="待機中")
        self.progress_text = tk.StringVar(value="0/0")
        self.progress_value = tk.IntVar(value=0)
        self.summary_vars = {key: tk.StringVar(value="-") for key in SUMMARY_KEYS}
        self._cancel_requested = False
        self._traversal_widgets: list[ttk.Radiobutton] = []
        self._build()

    def _build(self) -> None:
        self._configure_style()

        frame = ttk.Frame(self.root, padding=18, style="App.TFrame")
        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        self._build_header(frame)
        self._build_input_section(frame)
        self._build_execution_section(frame)
        self._build_results_section(frame)
        self._sync_traversal_state()
        self.input_mode.trace_add("write", lambda *_: self._sync_traversal_state())

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("App.TFrame", background="#f6f7f9")
        style.configure("Header.TLabel", font=("Yu Gothic UI", 16, "bold"), background="#f6f7f9")
        style.configure("Subtle.TLabel", foreground="#4b5563", background="#f6f7f9")
        style.configure("Section.TLabelframe", padding=12)
        style.configure("Section.TLabelframe.Label", font=("Yu Gothic UI", 10, "bold"))
        style.configure("Summary.TLabel", font=("Yu Gothic UI", 10))

    def _build_header(self, parent: ttk.Frame) -> None:
        header = ttk.Frame(parent, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=APP_TITLE, style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text=APP_PURPOSE, style="Subtle.TLabel").grid(row=1, column=0, sticky="w")

    def _build_input_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="入力", style="Section.TLabelframe")
        section.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        section.columnconfigure(1, weight=1)

        ttk.Label(section, text="置換表").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(section, textvariable=self.replacement_table).grid(row=0, column=1, sticky="ew", pady=5)
        ttk.Button(section, text="選択", command=self.pick_replacement_table).grid(row=0, column=2, padx=(8, 0), pady=5)

        ttk.Label(section, text="入力種別").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=5)
        mode_frame = ttk.Frame(section)
        mode_frame.grid(row=1, column=1, sticky="w", pady=5)
        ttk.Radiobutton(mode_frame, text="ファイル", variable=self.input_mode, value=InputMode.SINGLE_FILE.value).grid(row=0, column=0, padx=(0, 12))
        ttk.Radiobutton(mode_frame, text="フォルダ", variable=self.input_mode, value=InputMode.FOLDER.value).grid(row=0, column=1)

        ttk.Label(section, text="処理対象").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(section, textvariable=self.input_path).grid(row=2, column=1, sticky="ew", pady=5)
        ttk.Button(section, text="選択", command=self.pick_input).grid(row=2, column=2, padx=(8, 0), pady=5)

        ttk.Label(section, text="フォルダ範囲").grid(row=3, column=0, sticky="w", padx=(0, 8), pady=5)
        traversal = ttk.Frame(section)
        traversal.grid(row=3, column=1, sticky="w", pady=5)
        direct = ttk.Radiobutton(traversal, text="直下のみ", variable=self.traversal_mode, value=TraversalMode.DIRECT_CHILDREN.value)
        recursive = ttk.Radiobutton(traversal, text="サブフォルダ含む", variable=self.traversal_mode, value=TraversalMode.RECURSIVE.value)
        direct.grid(row=0, column=0, padx=(0, 12))
        recursive.grid(row=0, column=1)
        self._traversal_widgets = [direct, recursive]

        ttk.Label(section, text="出力フォルダ").grid(row=4, column=0, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(section, textvariable=self.output_folder).grid(row=4, column=1, sticky="ew", pady=5)
        ttk.Button(section, text="選択", command=self.pick_output).grid(row=4, column=2, padx=(8, 0), pady=5)

    def _build_execution_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="実行", style="Section.TLabelframe")
        section.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        section.columnconfigure(1, weight=1)

        buttons = ttk.Frame(section)
        buttons.grid(row=0, column=0, sticky="w", padx=(0, 12))
        self.start_button = ttk.Button(buttons, text="開始", command=self.start)
        self.start_button.grid(row=0, column=0, padx=(0, 8))
        self.cancel_button = ttk.Button(buttons, text="キャンセル", command=self.cancel, state="disabled")
        self.cancel_button.grid(row=0, column=1)

        progress = ttk.Progressbar(section, variable=self.progress_value, maximum=100)
        progress.grid(row=0, column=1, sticky="ew")
        ttk.Label(section, textvariable=self.progress_text, style="Subtle.TLabel").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Label(section, textvariable=self.status, style="Subtle.TLabel").grid(row=1, column=1, sticky="ew", pady=(8, 0))

    def _build_results_section(self, parent: ttk.Frame) -> None:
        section = ttk.LabelFrame(parent, text="結果", style="Section.TLabelframe")
        section.grid(row=3, column=0, sticky="ew")
        for index in range(5):
            section.columnconfigure(index, weight=1)

        labels = {
            "replaced": "置換済み",
            "no_match": "未検出",
            "skipped": "対象外",
            "failed": "失敗",
            "report_path": "レポート",
        }
        for column, key in enumerate(SUMMARY_KEYS):
            ttk.Label(section, text=labels[key], style="Subtle.TLabel").grid(row=0, column=column, sticky="w")
            ttk.Label(section, textvariable=self.summary_vars[key], style="Summary.TLabel").grid(row=1, column=column, sticky="ew", padx=(0, 12))

    def _sync_traversal_state(self) -> None:
        state = "normal" if self.input_mode.get() == InputMode.FOLDER.value else "disabled"
        for widget in self._traversal_widgets:
            widget.configure(state=state)

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

    def state_keys(self) -> tuple[str, ...]:
        return UI_STATE_KEYS

    def timing_fields(self) -> tuple[str, ...]:
        return TIMING_FIELDS

    def start(self) -> None:
        error = self.validate()
        if error:
            self.status.set(error)
            messagebox.showerror("入力エラー", error)
            return
        self.start_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.progress_value.set(0)
        self.progress_text.set("0/0")
        self.status.set("処理中")
        self._cancel_requested = False
        thread = threading.Thread(target=self._run_processing, daemon=True)
        thread.start()

    def cancel(self) -> None:
        self._cancel_requested = True
        self.status.set("キャンセル要求中")

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
        percent = int((current / total) * 100) if total else 0
        self.root.after(
            0,
            lambda: (
                self.progress_value.set(percent),
                self.progress_text.set(f"{current}/{total}"),
                self.status.set(path.as_posix()),
            ),
        )

    def _complete(self, summary) -> None:
        self.start_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        cancelled = "キャンセル済み " if summary.cancelled else ""
        self.summary_vars["replaced"].set(str(summary.replaced_count))
        self.summary_vars["no_match"].set(str(summary.processed_no_matches_count))
        self.summary_vars["skipped"].set(str(summary.skipped_unsupported_count))
        self.summary_vars["failed"].set(str(summary.failed_count))
        self.summary_vars["report_path"].set(str(summary.report_path))
        self.status.set(f"{cancelled}完了")

    def _fail(self, exc: Exception) -> None:
        self.start_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self.status.set(str(exc))
        messagebox.showerror("処理エラー", str(exc))


def main() -> None:
    root = tk.Tk()
    MaskingToolUI(root)
    root.mainloop()
