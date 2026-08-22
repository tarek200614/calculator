"""Tests for calculator.calculator (the Calculator engine)."""

import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from calculator.calculator import Calculator  # noqa: E402
from calculator.evaluator import DivisionByZeroError, InvalidExpressionError  # noqa: E402


class TestCalculatorEngine(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_basic_calculation(self):
        self.assertEqual(self.calc.calculate("2 + 2"), 4)

    def test_operator_precedence(self):
        self.assertEqual(self.calc.calculate("2 + 3 * 4"), 14)

    def test_parentheses(self):
        self.assertEqual(self.calc.calculate("(2 + 3) * 4"), 20)

    def test_calculation_recorded_in_history(self):
        self.calc.calculate("2 + 2")
        self.calc.calculate("10 - 3")
        entries = self.calc.history.all()
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].expression, "2 + 2")
        self.assertEqual(entries[0].result, 4)
        self.assertEqual(entries[1].expression, "10 - 3")
        self.assertEqual(entries[1].result, 7)

    def test_failed_calculation_not_recorded(self):
        with self.assertRaises(DivisionByZeroError):
            self.calc.calculate("5 / 0")
        self.assertEqual(len(self.calc.history), 0)

    def test_invalid_expression_not_recorded(self):
        with self.assertRaises(InvalidExpressionError):
            self.calc.calculate("2 +")
        self.assertEqual(len(self.calc.history), 0)

    def test_clear_history(self):
        self.calc.calculate("1 + 1")
        self.calc.clear_history()
        self.assertEqual(len(self.calc.history), 0)

    def test_engine_usable_without_gui(self):
        # Regression guard: importing/using Calculator must never require
        # tkinter or open any window.
        self.assertIsInstance(self.calc.calculate("3 * 3"), (int, float))


if __name__ == "__main__":
    unittest.main()
