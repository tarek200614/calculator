"""
app.py
======

Application bootstrap: creates the Tk root window, applies an icon if one
is available, builds the calculator UI, and starts the event loop.
"""

from __future__ import annotations

import tkinter as tk
from pathlib import Path

from .ui import CalculatorUI

ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"


def _apply_icon(root: tk.Tk) -> None:
    """Apply a window icon if a suitable file exists in ``assets/``.

    This is best-effort: if no icon file is present, or Tk cannot load it on
    the current platform, the application continues without an icon rather
    than crashing.
    """
    ico_path = ASSETS_DIR / "icon.ico"
    png_path = ASSETS_DIR / "icon.png"

    try:
        if ico_path.exists():
            root.iconbitmap(default=str(ico_path))
            return
        if png_path.exists():
            icon_image = tk.PhotoImage(file=str(png_path))
            root.iconphoto(True, icon_image)
            # Keep a reference so the image is not garbage-collected.
            root._icon_image = icon_image  # type: ignore[attr-defined]
    except tk.TclError:
        # Icon loading can fail depending on platform/format; ignore safely.
        pass


def main() -> None:
    """Create and run the calculator application."""
    root = tk.Tk()
    _apply_icon(root)
    CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
