# Python Calculator

A modern, desktop calculator built with **Python 3.11+** and **Tkinter**
(no third-party GUI frameworks). It supports standard arithmetic with
correct operator precedence, parentheses, decimals, negative numbers,
keyboard input, and a calculation history panel — all backed by a
dependency-free, `eval()`-free expression evaluator.

## Features

- Basic arithmetic: addition, subtraction, multiplication, division
- Decimal numbers and negative numbers
- Percentage / modulo operator (`%`)
- Parentheses with correct operator precedence
- Clear (`C`) and backspace (`⌫`) buttons
- Equals button and full keyboard support (numbers, `+ - * / % ( )`,
  <kbd>Enter</kbd>, <kbd>Escape</kbd>, <kbd>Backspace</kbd>)
- Calculation history panel with a "Clear history" button, and click-to-reuse
  a past result
- Friendly, non-technical error messages (division by zero, invalid
  expressions, incomplete expressions)
- Responsive layout that behaves correctly when the window is resized
- Clean, modern dark-themed appearance
- Safe by design: user input is **never** passed to `eval()`

## Screenshots

_(Add screenshots of the running application here, e.g. `assets/screenshot.png`.)_

## Requirements

- Python **3.11 or newer**
- Tkinter (included with the standard Windows Python installer; on Linux
  you may need your distribution's `python3-tk` package)
- No third-party packages — see [`requirements.txt`](requirements.txt)

## Installation

1. Make sure Python 3.11+ is installed:
   ```bash
   python --version
   ```
2. Extract this ZIP file / clone the repository.
3. That's it — there is nothing to `pip install`.

## Running the application

From the project's root folder (the one containing `run.py`):

```bash
python run.py
```

On some systems the Python 3 interpreter is called `python3`:

```bash
python3 run.py
```

## Running tests

```bash
python -m unittest discover -s tests -v
```

The test suite covers the calculation engine and history manager directly
and does **not** require opening the GUI.

## Keyboard shortcuts

| Key | Action |
|---|---|
| `0`–`9` | Enter digits |
| `.` | Decimal point |
| `+` `-` `*` `/` `%` | Operators |
| `(` `)` | Parentheses |
| `Enter` | Evaluate (`=`) |
| `Escape` | Clear (`C`) |
| `Backspace` | Delete last character |

## Project structure

```text
python-calculator/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── run.py                     # Entry point: python run.py
├── BUILD_WINDOWS.md           # Optional: package as a Windows .exe
│
├── src/
│   └── calculator/
│       ├── __init__.py
│       ├── app.py             # Tk root window bootstrap
│       ├── calculator.py      # Calculator engine (GUI-independent)
│       ├── evaluator.py       # Safe expression parser/evaluator (no eval())
│       ├── history.py         # Calculation history manager
│       └── ui.py              # Tkinter widgets and event handling
│
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   ├── test_evaluator.py
│   └── test_history.py
│
├── assets/
│   └── README.md              # Optional icon.ico / icon.png go here
│
└── docs/
    └── DEVELOPMENT.md         # Architecture notes for contributors
```

The calculation engine (`calculator.py`, `evaluator.py`, `history.py`) has
no dependency on Tkinter and can be imported and used entirely without a
GUI — for example in scripts or other front-ends.

## Security notes

This calculator **never calls Python's `eval()` on user input**. Expressions
are:

1. Restricted to a whitelist of characters (digits, `. + - * / % ( )`, and
   whitespace).
2. Parsed into a Python `ast` (Abstract Syntax Tree) using `ast.parse(...,
   mode="eval")`, which only *parses* — it does not execute anything.
3. Walked by a custom evaluator that only recognizes number literals and a
   whitelist of arithmetic operators. Any other construct (function calls,
   variable names, attribute access, imports, etc.) is rejected with an
   `InvalidExpressionError` before any computation occurs.

This design means the calculator can perform arithmetic and nothing else —
it cannot execute arbitrary code, regardless of what is typed into it.

Expressions are also capped at 200 characters. This is far more than any
real calculation needs, and it keeps the evaluator's internal recursive
tree-walk safely within Python's call-stack limits (an earlier version
could be crashed by an extremely long, otherwise harmless-looking chain of
operators, e.g. `1+1+1+...`; this is now rejected with a friendly "too
long" message instead — see `docs/DEVELOPMENT.md` for details).

## Troubleshooting

| Problem | Likely cause / fix |
|---|---|
| `ModuleNotFoundError: No module named 'tkinter'` | Tkinter isn't installed. On Windows, reinstall Python from python.org and make sure "tcl/tk and IDLE" is checked. On Debian/Ubuntu Linux, run `sudo apt install python3-tk`. |
| Window opens but looks blank or tiny | Try resizing the window; the layout is responsive and will re-flow. |
| "Cannot divide by zero" message | Expected behavior — division and modulo by zero are caught and reported as a friendly error, not a crash. |
| "The expression is not valid." message | The typed expression has mismatched parentheses, a trailing operator, or another syntax issue. Correct the expression and press `=` again. |
| Nothing happens when pressing keyboard keys | Click on the calculator window first so it has keyboard focus. |

## License

Released under the [MIT License](LICENSE).
