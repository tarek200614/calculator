# Development Notes

## Architecture overview

The project keeps a strict separation between calculation logic and the
GUI, so the engine can be tested (and reused) without ever opening a
window:

```
src/calculator/
├── evaluator.py   # Safe expression parsing/evaluation (no eval()), uses ast
├── history.py     # In-memory calculation history, GUI-independent
├── calculator.py  # High-level Calculator class: evaluator + history
├── ui.py          # Tkinter widgets and event handling only
└── app.py         # Bootstraps the Tk root window and runs the app
```

`calculator.py` and everything it depends on (`evaluator.py`, `history.py`)
have **zero** dependency on `tkinter`. `ui.py` and `app.py` are the only
modules that import `tkinter`. This means:

- The engine can be imported and used in a headless environment (CI,
  scripts, other UIs) with no display required.
- Unit tests never need to open a GUI window.

## Why not `eval()`?

`eval()` on raw user input is a classic code-injection vector — a string
like `__import__('os').system('...')` would execute arbitrary code. Instead,
`evaluator.py`:

1. Rejects any character that isn't a digit, decimal point, whitespace, or
   one of `+ - * / % ( )`.
2. Parses the (already-restricted) string with `ast.parse(expr, mode="eval")`
   to get a syntax tree — this does not execute anything.
3. Walks that tree itself, only evaluating a small whitelist of node types
   (`Constant` numbers, `BinOp` with `+ - * / %`, `UnaryOp` with unary
   `+ -`). Anything else (`Call`, `Name`, `Attribute`, `Subscript`,
   `Compare`, ...) raises `InvalidExpressionError` before any computation
   happens.

This guarantees the evaluator can only ever perform arithmetic — it cannot
call functions, import modules, or access names/attributes.

## Adding a new operator

1. Add the new `ast` operator class to `_ALLOWED_BINOPS` (or
   `_ALLOWED_UNARYOPS`) in `evaluator.py`.
2. Add a branch for it in `_apply_binop` (or `_eval_node` for unary cases).
3. Add the operator's character(s) to the `allowed_chars` set in
   `_validate_and_prepare`.
4. Add the corresponding button to `BUTTON_ROWS` in `ui.py` if it should be
   exposed in the GUI.
5. Add tests to `tests/test_evaluator.py`.

## Running tests during development

```bash
python -m unittest discover -s tests -v
```

## Code style

- Type hints are used throughout for clarity.
- Each module has a single, clear responsibility (see architecture above).
- No hard-coded absolute paths; `pathlib.Path` is used with paths relative
  to `__file__` where the filesystem is touched (e.g. locating `assets/`).
