# Building a Windows .exe (optional)

The calculator runs fine with just `python run.py` — you do **not** need
this guide to use the application. This is only for turning it into a
standalone `.exe` that can be shared with people who don't have Python
installed.

`PyInstaller` is **not** a runtime dependency of the calculator; it is only
needed on the machine that *builds* the `.exe`.

## 1. Install PyInstaller (build machine only)

```bash
pip install pyinstaller
```

## 2. Build the executable

From the project root (the folder containing `run.py`):

```bash
pyinstaller --noconsole --onefile --name PythonCalculator run.py
```

- `--noconsole` — don't open a background terminal window (this is a GUI app).
- `--onefile` — bundle everything into a single `.exe`.
- `--name PythonCalculator` — sets the output file name.

If you've added an icon at `assets/icon.ico`, include it in the build too:

```bash
pyinstaller --noconsole --onefile --name PythonCalculator --icon assets/icon.ico run.py
```

## 3. Find the result

PyInstaller creates a few folders. The executable you want is at:

```text
dist\PythonCalculator.exe
```

You can copy `PythonCalculator.exe` anywhere and double-click it to run the
calculator — no Python installation needed on the target machine.

## 4. Clean up (optional)

PyInstaller also creates `build/` and a `PythonCalculator.spec` file. These
are safe to delete after a successful build; re-running the command above
will regenerate them. (Both are already excluded via `.gitignore`.)

## Troubleshooting

| Problem | Fix |
|---|---|
| `pyinstaller` not recognized | Make sure `pip install pyinstaller` completed successfully and that your Python `Scripts` folder is on `PATH`. |
| Antivirus flags the `.exe` | This is a common false positive with PyInstaller-built executables; it's caused by the bundling technique, not the calculator's code. |
| Window looks tiny/huge on a high-DPI screen | This is a Windows display-scaling behavior with Tk; try running the `.exe` with "Disable display scaling on high DPI settings" (right-click the `.exe` → Properties → Compatibility) if it looks off. |
