"""
calculator.py
=============

The core calculation engine. It is completely independent of any GUI code,
so it can be imported and used from scripts, tests, or other front-ends.
"""

from __future__ import annotations

from typing import Union

from .evaluator import CalculatorError, evaluate
from .history import History, format_number

Number = Union[int, float]

__all__ = ["Calculator", "CalculatorError", "format_number"]


class Calculator:
    """High-level calculator that evaluates expressions and records history."""

    def __init__(self, history_size: int = 100) -> None:
        self.history = History(max_entries=history_size)

    def calculate(self, expression: str) -> Number:
        """Evaluate ``expression`` and store it in history.

        Args:
            expression: A mathematical expression, e.g. "2 + 3 * 4".

        Returns:
            The numeric result of the expression.

        Raises:
            CalculatorError: (or one of its subclasses) if the expression is
                invalid or cannot be evaluated.
        """
        result = evaluate(expression)
        self.history.add(expression, result)
        return result

    def clear_history(self) -> None:
        """Clear all recorded calculation history."""
        self.history.clear()
