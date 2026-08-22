"""
calculator
==========

A small, dependency-free calculator engine and Tkinter GUI.

Public API:
    - Calculator: the calculation engine (usable without any GUI).
    - CalculatorError: base exception for calculator-related errors.
    - DivisionByZeroError, InvalidExpressionError: specific error types.
    - History: calculation history manager.
    - CalculatorApp: the Tkinter application (GUI).
"""

from .calculator import Calculator
from .evaluator import (
    CalculatorError,
    DivisionByZeroError,
    InvalidExpressionError,
)
from .history import History

__all__ = [
    "Calculator",
    "CalculatorError",
    "DivisionByZeroError",
    "InvalidExpressionError",
    "History",
]

__version__ = "1.0.0"
