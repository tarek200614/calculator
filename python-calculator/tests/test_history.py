"""Tests for calculator.history (the History manager)."""

import sys
import unittest
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from calculator.history import History, format_number  # noqa: E402


class TestHistory(unittest.TestCase):
    def setUp(self):
        self.history = History()

    def test_add_entry(self):
        entry = self.history.add("2 + 2", 4)
        self.assertEqual(entry.expression, "2 + 2")
        self.assertEqual(entry.result, 4)
        self.assertEqual(len(self.history), 1)

    def test_multiple_entries_preserve_order(self):
        self.history.add("1 + 1", 2)
        self.history.add("2 + 2", 4)
        entries = self.history.all()
        self.assertEqual([e.result for e in entries], [2, 4])

    def test_clear(self):
        self.history.add("1 + 1", 2)
        self.history.clear()
        self.assertEqual(len(self.history), 0)
        self.assertIsNone(self.history.latest())

    def test_latest(self):
        self.history.add("1 + 1", 2)
        self.history.add("3 + 3", 6)
        self.assertEqual(self.history.latest().result, 6)

    def test_max_entries_eviction(self):
        history = History(max_entries=2)
        history.add("1 + 1", 2)
        history.add("2 + 2", 4)
        history.add("3 + 3", 6)
        entries = history.all()
        self.assertEqual(len(entries), 2)
        self.assertEqual([e.result for e in entries], [4, 6])

    def test_invalid_max_entries_rejected(self):
        with self.assertRaises(ValueError):
            History(max_entries=0)


class TestFormatNumber(unittest.TestCase):
    def test_integer_float_formatted_without_decimal(self):
        self.assertEqual(format_number(4.0), "4")

    def test_decimal_float_preserved(self):
        self.assertEqual(format_number(2.5), "2.5")

    def test_plain_int(self):
        self.assertEqual(format_number(7), "7")

    def test_floating_point_artifact_trimmed(self):
        self.assertEqual(format_number(0.1 + 0.2), "0.3")


if __name__ == "__main__":
    unittest.main()
