"""Tests for calculator.evaluator (the safe expression evaluator)."""

import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from calculator.evaluator import (  # noqa: E402
    DivisionByZeroError,
    InvalidExpressionError,
    evaluate,
)


class TestBasicArithmetic(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(evaluate("2 + 2"), 4)

    def test_subtraction(self):
        self.assertEqual(evaluate("10 - 3"), 7)

    def test_multiplication(self):
        self.assertEqual(evaluate("5 * 6"), 30)

    def test_division(self):
        self.assertEqual(evaluate("20 / 4"), 5)

    def test_modulo_percentage_operator(self):
        self.assertEqual(evaluate("10 % 2"), 0)
        self.assertEqual(evaluate("10 % 3"), 1)


class TestPrecedenceAndParentheses(unittest.TestCase):
    def test_operator_precedence(self):
        self.assertEqual(evaluate("2 + 3 * 4"), 14)

    def test_parentheses_override_precedence(self):
        self.assertEqual(evaluate("(2 + 3) * 4"), 20)

    def test_nested_parentheses(self):
        self.assertEqual(evaluate("((1 + 2) * (3 + 4))"), 21)


class TestNegativeAndDecimalNumbers(unittest.TestCase):
    def test_negative_numbers(self):
        self.assertEqual(evaluate("-5 + 3"), -2)
        self.assertEqual(evaluate("5 + -3"), 2)
        self.assertEqual(evaluate("-(5 + 3)"), -8)

    def test_decimal_numbers(self):
        self.assertAlmostEqual(evaluate("2.5 + 2.5"), 5.0)
        self.assertAlmostEqual(evaluate("0.1 + 0.2"), 0.3)


class TestErrorHandling(unittest.TestCase):
    def test_division_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            evaluate("5 / 0")

    def test_modulo_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            evaluate("5 % 0")

    def test_empty_expression(self):
        with self.assertRaises(InvalidExpressionError):
            evaluate("")

    def test_whitespace_only_expression(self):
        with self.assertRaises(InvalidExpressionError):
            evaluate("   ")

    def test_incomplete_expression(self):
        with self.assertRaises(InvalidExpressionError):
            evaluate("2 +")

    def test_unbalanced_parentheses(self):
        with self.assertRaises(InvalidExpressionError):
            evaluate("(2 + 3")

    def test_invalid_characters_rejected(self):
        with self.assertRaises(InvalidExpressionError):
            evaluate("__import__('os')")

    def test_no_code_execution_via_names(self):
        with self.assertRaises(InvalidExpressionError):
            evaluate("2 + x")

    def test_overly_long_expression_rejected_cleanly(self):
        # Regression test: a very long chain of operators used to blow the
        # recursive evaluator's call stack with an uncaught RecursionError
        # instead of a friendly, documented error. See docs/DEVELOPMENT.md.
        pathological = "+".join(["1"] * 1000)
        with self.assertRaises(InvalidExpressionError):
            evaluate(pathological)

    def test_expression_at_length_limit_still_works(self):
        # A reasonably long, but legitimate, expression must still work.
        expression = "+".join(["1"] * 50)
        self.assertEqual(evaluate(expression), 50)


if __name__ == "__main__":
    unittest.main()
