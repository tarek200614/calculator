"""
history.py
==========

A simple in-memory calculation history manager, kept separate from both the
calculation engine and the GUI so it can be tested and reused independently.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union

Number = Union[int, float]


@dataclass(frozen=True)
class HistoryEntry:
    """A single calculation history record."""

    expression: str
    result: Number

    def __str__(self) -> str:
        return f"{self.expression} = {format_number(self.result)}"


def format_number(value: Number) -> str:
    """Format a number for display, trimming trailing zeros on floats."""
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        # Avoid ugly floating point artifacts like 0.30000000000000004.
        text = f"{value:.10f}".rstrip("0").rstrip(".")
        return text if text else "0"
    return str(value)


class History:
    """Keeps track of past calculations in order (most recent last)."""

    def __init__(self, max_entries: int = 100) -> None:
        if max_entries <= 0:
            raise ValueError("max_entries must be a positive integer.")
        self._max_entries = max_entries
        self._entries: List[HistoryEntry] = []

    def add(self, expression: str, result: Number) -> HistoryEntry:
        """Add a new entry, evicting the oldest one if over capacity."""
        entry = HistoryEntry(expression=expression, result=result)
        self._entries.append(entry)
        if len(self._entries) > self._max_entries:
            self._entries.pop(0)
        return entry

    def clear(self) -> None:
        """Remove all history entries."""
        self._entries.clear()

    def all(self) -> List[HistoryEntry]:
        """Return a copy of all entries, oldest first."""
        return list(self._entries)

    def latest(self) -> HistoryEntry | None:
        """Return the most recent entry, or None if history is empty."""
        return self._entries[-1] if self._entries else None

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self._entries)
