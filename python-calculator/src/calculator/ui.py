"""
ui.py
=====

The Tkinter graphical user interface for the calculator.

This module only handles presentation and user interaction; all actual
calculation logic lives in ``calculator.py`` / ``evaluator.py`` so the engine
can be tested and reused without ever opening a window.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from typing import Callable, List, Tuple

from .calculator import Calculator
from .evaluator import CalculatorError
from .history import format_number

# ---------------------------------------------------------------------------
# Colours & fonts -- kept in one place for a clean, modern, consistent look.
# ---------------------------------------------------------------------------
COLOR_BG = "#1e1f26"
COLOR_DISPLAY_BG = "#26272f"
COLOR_DISPLAY_FG = "#ffffff"
COLOR_HISTORY_BG = "#26272f"
COLOR_HISTORY_FG = "#9aa0ab"
COLOR_NUMBER_BG = "#31333d"
COLOR_NUMBER_FG = "#ffffff"
COLOR_NUMBER_ACTIVE = "#3d3f4b"
COLOR_OPERATOR_BG = "#3a6ff7"
COLOR_OPERATOR_FG = "#ffffff"
COLOR_OPERATOR_ACTIVE = "#5583ff"
COLOR_FUNCTION_BG = "#4a4d5a"
COLOR_FUNCTION_FG = "#ffffff"
COLOR_FUNCTION_ACTIVE = "#5a5d6c"
COLOR_EQUALS_BG = "#f7943a"
COLOR_EQUALS_FG = "#ffffff"
COLOR_EQUALS_ACTIVE = "#ff9f4d"
COLOR_ERROR_FG = "#ff6b6b"

# Button layout: each tuple is (label, kind) where kind controls styling and
# behaviour. "num" digits/decimal point, "op" arithmetic operators, "func"
# clear/backspace/parentheses/percent, "eq" the equals button.
BUTTON_ROWS: List[List[Tuple[str, str]]] = [
    [("C", "func"), ("(", "func"), (")", "func"), ("⌫", "func")],
    [("7", "num"), ("8", "num"), ("9", "num"), ("/", "op")],
    [("4", "num"), ("5", "num"), ("6", "num"), ("*", "op")],
    [("1", "num"), ("2", "num"), ("3", "num"), ("-", "op")],
    [("0", "num"), (".", "num"), ("%", "op"), ("+", "op")],
    [("=", "eq")],
]

_STYLE_MAP = {
    "num": (COLOR_NUMBER_BG, COLOR_NUMBER_FG, COLOR_NUMBER_ACTIVE),
    "op": (COLOR_OPERATOR_BG, COLOR_OPERATOR_FG, COLOR_OPERATOR_ACTIVE),
    "func": (COLOR_FUNCTION_BG, COLOR_FUNCTION_FG, COLOR_FUNCTION_ACTIVE),
    "eq": (COLOR_EQUALS_BG, COLOR_EQUALS_FG, COLOR_EQUALS_ACTIVE),
}


class CalculatorUI:
    """Builds and wires up the calculator's Tkinter widgets."""

    def __init__(self, root: tk.Tk, calculator: Calculator | None = None) -> None:
        self.root = root
        self.calculator = calculator or Calculator()
        self.expression = ""
        self._error_active = False

        self._configure_root()
        self._build_fonts()
        self._build_layout()
        self._bind_keyboard()

    # -- setup -------------------------------------------------------------

    def _configure_root(self) -> None:
        self.root.title("Python Calculator")
        self.root.configure(bg=COLOR_BG)
        self.root.minsize(360, 520)
        self.root.geometry("380x600")

    def _build_fonts(self) -> None:
        self.display_font = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        self.history_font = tkfont.Font(family="Segoe UI", size=10)
        self.button_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")

    def _build_layout(self) -> None:
        # Root grid: history panel, display, then a resizable button grid.
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self._build_history_panel()
        self._build_display()
        self._build_button_grid()

    def _build_history_panel(self) -> None:
        container = tk.Frame(self.root, bg=COLOR_HISTORY_BG)
        container.grid(row=0, column=0, sticky="nsew", padx=8, pady=(8, 0))
        container.grid_columnconfigure(0, weight=1)

        header = tk.Frame(container, bg=COLOR_HISTORY_BG)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        tk.Label(
            header,
            text="History",
            bg=COLOR_HISTORY_BG,
            fg=COLOR_HISTORY_FG,
            font=self.history_font,
            anchor="w",
        ).grid(row=0, column=0, sticky="w")

        clear_history_btn = tk.Button(
            header,
            text="Clear history",
            bg=COLOR_HISTORY_BG,
            fg=COLOR_HISTORY_FG,
            activebackground=COLOR_HISTORY_BG,
            activeforeground=COLOR_ERROR_FG,
            bd=0,
            font=self.history_font,
            cursor="hand2",
            command=self.on_clear_history,
        )
        clear_history_btn.grid(row=0, column=1, sticky="e")

        self.history_listbox = tk.Listbox(
            container,
            bg=COLOR_HISTORY_BG,
            fg=COLOR_HISTORY_FG,
            bd=0,
            highlightthickness=0,
            font=self.history_font,
            height=4,
            activestyle="none",
            selectbackground=COLOR_NUMBER_ACTIVE,
        )
        self.history_listbox.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(4, 8))
        self.history_listbox.bind("<<ListboxSelect>>", self._on_history_select)

    def _build_display(self) -> None:
        display_frame = tk.Frame(self.root, bg=COLOR_DISPLAY_BG)
        display_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        display_frame.grid_columnconfigure(0, weight=1)

        self.display_var = tk.StringVar(value="0")
        self.display_label = tk.Label(
            display_frame,
            textvariable=self.display_var,
            bg=COLOR_DISPLAY_BG,
            fg=COLOR_DISPLAY_FG,
            font=self.display_font,
            anchor="e",
            padx=16,
            pady=24,
        )
        self.display_label.grid(row=0, column=0, sticky="nsew")

    def _build_button_grid(self) -> None:
        grid_frame = tk.Frame(self.root, bg=COLOR_BG)
        grid_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))

        num_cols = max(len(row) for row in BUTTON_ROWS)
        for col in range(num_cols):
            grid_frame.grid_columnconfigure(col, weight=1)
        for row_index in range(len(BUTTON_ROWS)):
            grid_frame.grid_rowconfigure(row_index, weight=1)

        for row_index, row in enumerate(BUTTON_ROWS):
            span = num_cols if len(row) == 1 else 1
            for col_index, (label, kind) in enumerate(row):
                bg, fg, active_bg = _STYLE_MAP[kind]
                button = tk.Button(
                    grid_frame,
                    text=label,
                    bg=bg,
                    fg=fg,
                    activebackground=active_bg,
                    activeforeground=fg,
                    bd=0,
                    relief="flat",
                    font=self.button_font,
                    cursor="hand2",
                    command=lambda l=label: self.on_button_press(l),
                )
                col_span = span if len(row) == 1 else 1
                button.grid(
                    row=row_index,
                    column=col_index,
                    columnspan=col_span,
                    sticky="nsew",
                    padx=4,
                    pady=4,
                    ipady=8,
                )

    def _bind_keyboard(self) -> None:
        self.root.bind("<Key>", self._on_key_press)
        self.root.bind("<Return>", lambda _e: self.on_equals())
        self.root.bind("<KP_Enter>", lambda _e: self.on_equals())
        self.root.bind("<Escape>", lambda _e: self.on_clear())
        self.root.bind("<BackSpace>", lambda _e: self.on_backspace())

    # -- event handlers ------------------------------------------------------

    def _on_key_press(self, event: tk.Event) -> None:
        char = event.char
        if char and char in "0123456789.+-*/%()":
            self.on_button_press(char)

    def on_button_press(self, label: str) -> None:
        if label == "C":
            self.on_clear()
        elif label == "⌫":
            self.on_backspace()
        elif label == "=":
            self.on_equals()
        else:
            self.on_input(label)

    def on_input(self, char: str) -> None:
        if self._error_active:
            # Start fresh after an error instead of appending to the message.
            self.expression = ""
            self._error_active = False
        self.expression += char
        self._refresh_display()

    def on_clear(self) -> None:
        self.expression = ""
        self._error_active = False
        self._refresh_display()

    def on_backspace(self) -> None:
        if self._error_active:
            self.expression = ""
            self._error_active = False
        else:
            self.expression = self.expression[:-1]
        self._refresh_display()

    def on_equals(self) -> None:
        if not self.expression.strip():
            return
        try:
            result = self.calculator.calculate(self.expression)
        except CalculatorError as exc:
            self._show_error(str(exc))
            return
        except Exception as exc:  # noqa: BLE001 - last line of defence for the GUI
            self._show_error(f"Something went wrong: {exc}")
            return

        formatted = format_number(result)
        self.expression = formatted
        self._error_active = False
        self._refresh_display()
        self._refresh_history()

    def on_clear_history(self) -> None:
        self.calculator.clear_history()
        self._refresh_history()

    def _on_history_select(self, _event: tk.Event) -> None:
        selection = self.history_listbox.curselection()
        if not selection:
            return
        entries = self.calculator.history.all()
        index = selection[0]
        if 0 <= index < len(entries):
            self.expression = format_number(entries[index].result)
            self._error_active = False
            self._refresh_display()

    # -- rendering helpers ---------------------------------------------------

    def _refresh_display(self) -> None:
        self.display_var.set(self.expression if self.expression else "0")
        self.display_label.configure(fg=COLOR_DISPLAY_FG)

    def _show_error(self, message: str) -> None:
        self._error_active = True
        self.display_var.set(message)
        self.display_label.configure(fg=COLOR_ERROR_FG)

    def _refresh_history(self) -> None:
        self.history_listbox.delete(0, tk.END)
        for entry in reversed(self.calculator.history.all()):
            self.history_listbox.insert(tk.END, str(entry))
