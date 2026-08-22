"""
evaluator.py
============

A safe arithmetic expression evaluator.

This module deliberately avoids Python's built-in ``eval()`` on user input.
Instead, it parses the expression into a Python Abstract Syntax Tree (AST)
using ``ast.parse`` and then walks that tree itself, only allowing a small,
explicit whitelist of node types (numbers, parentheses, +, -, *, /, %, and
unary +/-). Any other construct (function calls, names, attribute access,
subscripts, comparisons, string literals, etc.) is rejected before any
computation happens.

This means the evaluator can never execute arbitrary Python code, import
modules, or access the filesystem -- it can only do arithmetic.
"""

from __future__ import annotations

import ast
from typing import Union

Number = Union[int, float]


class CalculatorError(Exception):
    """Base class for all calculator-related errors."""


class InvalidExpressionError(CalculatorError):
    """Raised when the input expression cannot be parsed or is malformed."""


class DivisionByZeroError(CalculatorError):
    """Raised when a division (or modulo) by zero is attempted."""


# Node types that are allowed to appear in an expression's AST.
_ALLOWED_BINOPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)
_ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)

# Hard cap on expression length. This is generous for any real calculator
# input (typed or pasted) while keeping the AST shallow enough that our
# recursive evaluator can never exhaust the call stack -- see
# docs/DEVELOPMENT.md for the reasoning and the audit that uncovered this.
MAX_EXPRESSION_LENGTH = 200


def _validate_and_prepare(expression: str) -> str:
    """Perform lightweight normalisation and sanity checks before parsing.

    Raises:
        InvalidExpressionError: if the expression is empty or contains
            characters that are never valid in a supported expression.
    """
    if expression is None:
        raise InvalidExpressionError("The expression is empty.")

    cleaned = expression.strip()
    if not cleaned:
        raise InvalidExpressionError("The expression is empty.")

    if len(cleaned) > MAX_EXPRESSION_LENGTH:
        raise InvalidExpressionError(
            f"The expression is too long (max {MAX_EXPRESSION_LENGTH} characters)."
        )

    allowed_chars = set("0123456789.+-*/%() \t")
    invalid_chars = set(cleaned) - allowed_chars
    if invalid_chars:
        shown = ", ".join(sorted(invalid_chars))
        raise InvalidExpressionError(f"Unsupported character(s): {shown}")

    return cleaned


def _eval_node(node: ast.AST) -> Number:
    """Recursively evaluate a whitelisted AST node into a number."""
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)

    # Python >= 3.8 represents numeric literals as ast.Constant.
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise InvalidExpressionError("Only numbers are allowed in expressions.")

    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, _ALLOWED_BINOPS):
            raise InvalidExpressionError("Unsupported operator in expression.")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _apply_binop(node.op, left, right)

    if isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, _ALLOWED_UNARYOPS):
            raise InvalidExpressionError("Unsupported unary operator in expression.")
        operand = _eval_node(node.operand)
        return operand if isinstance(node.op, ast.UAdd) else -operand

    # Anything else (Call, Name, Attribute, Subscript, Compare, ...) is
    # rejected explicitly -- this is the core of the "safe" evaluator.
    raise InvalidExpressionError("Expression contains an unsupported element.")


def _apply_binop(op: ast.operator, left: Number, right: Number) -> Number:
    if isinstance(op, ast.Add):
        return left + right
    if isinstance(op, ast.Sub):
        return left - right
    if isinstance(op, ast.Mult):
        return left * right
    if isinstance(op, ast.Div):
        if right == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return left / right
    if isinstance(op, ast.Mod):
        if right == 0:
            raise DivisionByZeroError("Cannot perform modulo by zero.")
        return left % right
    raise InvalidExpressionError("Unsupported operator in expression.")  # pragma: no cover


def evaluate(expression: str) -> Number:
    """Safely evaluate a mathematical expression and return the result.

    Supports: + - * / % (modulo), parentheses, decimals, negative numbers,
    and standard operator precedence.

    Args:
        expression: The expression to evaluate, e.g. "(2 + 3) * 4".

    Returns:
        The numeric result, as an ``int`` or ``float``.

    Raises:
        InvalidExpressionError: if the expression is empty, malformed, or
            contains disallowed syntax.
        DivisionByZeroError: if the expression divides or takes modulo by
            zero.
    """
    cleaned = _validate_and_prepare(expression)

    try:
        tree = ast.parse(cleaned, mode="eval")
    except (SyntaxError, ValueError) as exc:
        raise InvalidExpressionError("The expression is not valid.") from exc

    try:
        result = _eval_node(tree)
    except ZeroDivisionError as exc:  # defensive; _apply_binop should catch this first
        raise DivisionByZeroError("Cannot divide by zero.") from exc
    except RecursionError as exc:
        # Defense-in-depth: MAX_EXPRESSION_LENGTH should already rule this
        # out, but never let an internal RecursionError escape the public
        # evaluate() contract (only CalculatorError subclasses should).
        raise InvalidExpressionError("The expression is too complex to evaluate.") from exc

    return result
