#!/usr/bin/env python3
"""
run.py
======

Entry point for the Python Calculator application.

Usage:
    python run.py
"""

import sys
from pathlib import Path

# Allow running directly from the project root without installing the
# package: add ``src/`` to sys.path so ``import calculator`` works.
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from calculator.app import main  # noqa: E402  (import after sys.path tweak)

if __name__ == "__main__":
    main()
