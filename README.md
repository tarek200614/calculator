# 🧮 Python Calculator

<p align="center">
  <strong>A modern, secure, and lightweight desktop calculator built with Python.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/GUI-Tkinter-FF6F00?style=for-the-badge" alt="Tkinter">
  <img src="https://img.shields.io/badge/Dependencies-None-2EA44F?style=for-the-badge" alt="No Dependencies">
  <img src="https://img.shields.io/badge/Security-eval%28%29%20Free-DC2626?style=for-the-badge" alt="eval Free">
  <img src="https://img.shields.io/badge/License-MIT-6366F1?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  A clean desktop calculator featuring safe expression evaluation, correct
  operator precedence, keyboard support, calculation history, and a modern
  responsive interface — with <strong>zero third-party runtime dependencies</strong>.
</p>

---

## 📌 Overview

**Python Calculator** is a lightweight desktop application created to demonstrate clean Python application architecture, GUI development, expression parsing, software testing, and secure handling of user input.

The project separates the calculator engine from the graphical interface, allowing the calculation logic and history system to be reused independently of Tkinter.

The application requires **no third-party Python packages** for normal operation.

---

## ✨ Features

- ➕ Addition, subtraction, multiplication, and division
- 🔢 Decimal number support
- ➖ Negative number support
- `%` Percentage / modulo operator
- 🔢 Parentheses and correct operator precedence
- 🧹 Clear (`C`) functionality
- ⌫ Backspace support
- ⌨️ Full keyboard input
- ↵ Enter key for calculation
- ⎋ Escape key for clearing the calculator
- 📜 Calculation history panel
- 🔄 Click-to-reuse previous calculations
- 🗑️ Clear calculation history
- ⚠️ Friendly error messages
- 📐 Responsive interface when resizing the window
- 🌙 Modern dark-themed user interface
- 🛡️ Secure `eval()`-free expression evaluation
- 🧪 Automated unit tests
- 📦 Zero third-party runtime dependencies
- 🪟 Windows executable build instructions

---

## 🛠️ Technologies Used

### Programming Language

- **Python 3.11+**

### GUI

- **Tkinter**
- Python standard-library GUI components

### Expression Evaluation

- `ast`
- Custom expression parser
- Whitelisted arithmetic operators
- No direct use of `eval()`

### Testing

- Python `unittest`

### Development Tools

- Visual Studio Code
- Git
- GitHub
- Python standard library

---

## 🏗️ Architecture

The application follows a modular architecture that separates the user interface from the underlying calculator logic.

```text
User Input
    │
    ▼
┌──────────────────────┐
│      Tkinter UI      │
│       ui.py          │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Calculator Engine  │
│    calculator.py     │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Safe Expression     │
│     Evaluator        │
│    evaluator.py      │
└──────────┬───────────┘
           │
           ▼
      Mathematical
        Result
           │
           ▼
┌──────────────────────┐
│   History Manager    │
│     history.py       │
└──────────────────────┘

The core calculation components do not depend on Tkinter, making them usable independently in scripts, automated tests, or alternative front-ends.
```
## 📂 Project Structure
```text
python-calculator/
│
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── run.py                     # Application entry point
├── BUILD_WINDOWS.md           # Windows .exe build instructions
│
├── src/
│   └── calculator/
│       ├── __init__.py
│       ├── app.py             # Tkinter application bootstrap
│       ├── calculator.py      # GUI-independent calculator engine
│       ├── evaluator.py       # Safe expression parser/evaluator
│       ├── history.py         # Calculation history manager
│       └── ui.py              # Tkinter interface and event handling
│
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py     # Calculator engine tests
│   ├── test_evaluator.py      # Expression evaluator tests
│   └── test_history.py        # History manager tests
│
├── assets/
│   └── README.md              # Optional application icons
│
└── docs/
    └── DEVELOPMENT.md         # Architecture and development notes
```
## 🚀 Installation
1. Clone the repository

```text
git clone https://github.com/tarek200614/python-calculator.git
```

2. Navigate to the project

```text
cd python-calculator
```

3. Verify Python
Make sure Python 3.11 or newer is installed:

```text
python --version
```

4. Install dependencies
No third-party packages are required.

```text
pip install -r requirements.txt
```

Note: Tkinter is included with the standard Windows Python installation. On some Linux distributions, it may need to be installed separately.

## ▶️ Running the Application

From the project root directory:

```text
python run.py
```

On systems where Python 3 is exposed as python3:

```text
python3 run.py
```

The calculator window should open immediately.

## 🧪Running Tests

Run the complete test suite with:

```text
python -m unittest discover -s tests -v
```

The tests focus on the application's core logic and do not require the graphical interface to be opened.

The test suite covers:

Basic arithmetic
Operator precedence
Parentheses
Decimal numbers
Negative numbers
Division by zero
Invalid expressions
Expression parsing
History management
⌨️ Keyboard Shortcuts
Key	Action
0 – 9	Enter numbers
.	Decimal point
+	Addition
-	Subtraction
*	Multiplication
/	Division
%	Modulo / percentage operator
( )	Parentheses
Enter	Calculate
Escape	Clear calculator
Backspace	Delete last character
## 📸 Screenshots
Calculator Interface

Add a screenshot of the running application here.

assets/screenshot.png

Example:

![Python Calculator](assets/screenshot.png)
Calculation History

Add a screenshot showing the calculation history panel here.

assets/history.png
## 🛡️ Security

Security is an important part of the calculator's design.

The application never passes user input directly to Python's eval() function.

Instead, expressions are processed through several validation stages:

```text
User Expression
       │
       ▼
Character Validation
       │
       ▼
AST Parsing
       │
       ▼
Operator Whitelist
       │
       ▼
Custom Evaluation
       │
       ▼
Mathematical Result
```
The evaluator:

Restricts input to supported mathematical characters.
Parses the expression using Python's ast module.
Does not execute the generated AST.
Accepts only supported numeric literals and arithmetic operators.
Rejects unsupported constructs such as:
Function calls
Variables
Attribute access
Imports
Arbitrary Python expressions

This keeps the calculator focused exclusively on mathematical operations.

## ⚠️ Error Handling

The application converts technical calculation failures into user-friendly messages.

Situation	Application Response
Division by zero	Friendly division-by-zero message
Modulo by zero	Friendly calculation error
Invalid syntax	Invalid expression message
Missing parenthesis	Invalid expression message
Incomplete expression	Incomplete expression message
Unsupported operation	Invalid expression message

The application is designed to handle invalid input without crashing.

## 📋 Requirements
Python 3.11 or newer
Tkinter
Windows 10/11, Linux, or macOS
No third-party runtime dependencies

For Windows, Tkinter is normally included with the official Python installer.

For Debian/Ubuntu-based Linux distributions:

sudo apt install python3-tk
## 🪟 Building a Windows Executable

The project includes BUILD_WINDOWS.md with instructions for optionally packaging the calculator as a standalone Windows executable.

A typical PyInstaller workflow is:

pip install pyinstaller

Then:

```text
pyinstaller --onefile --windowed run.py
```

The resulting executable will be generated inside the dist/ directory.

PyInstaller is only required for creating an executable. It is not required to run the Python version of the calculator.

## 🔧 Troubleshooting
ModuleNotFoundError: No module named 'tkinter'

On Windows, reinstall Python using the official Python installer and ensure that Tcl/Tk and IDLE are included.

On Debian/Ubuntu:

```text
sudo apt install python3-tk
The calculator window does not appear
```

Make sure you are running the command from the project root:

```text
python run.py
Keyboard input does not work
```

Click the calculator window first to give it keyboard focus.

The interface looks too small

Resize the application window. The interface is designed to adapt to different window sizes.

Division by zero message appears

This is expected behavior. Division and modulo by zero are intentionally detected and reported instead of allowing the application to crash.

## 🎯 Learning Objectives

This project demonstrates practical experience with:

- 🐍 Python application development
- 🖥️ Desktop GUI development
- 🧩 Modular software architecture
- 🧮 Expression parsing and evaluation
- 🔐 Secure input handling
- 🧪 Unit testing
- ⌨️ Keyboard event handling
- 📜 State and history management
- ⚠️ Exception handling
- 📦 Python project organization
- 📝 Technical documentation
- 🪟 Windows application packaging
- 🔮 Future Improvements

Potential future versions could introduce:

- 🧮 Scientific calculator mode
- 📐 Trigonometric functions
- √ Square root and power operations
- 🌓 Light/Dark theme switching
- 💾 Persistent calculation history
- 📤 Export history to a file
- 📋 Copy/paste result support
- 🔢 Customizable number formatting
- 🎨 User-selectable themes
- 🖼️ Custom application icon
- 🪟 Standalone Windows .exe
- 🌍 Internationalization and multiple languages
- ♿ Improved accessibility support
- ⌨️ Fully customizable keyboard shortcuts
- 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Development workflow
Fork the repository.
Create a feature branch:
git checkout -b feature/my-improvement
Make your changes.
Run the test suite:
python -m unittest discover -s tests -v
Commit your changes:
git commit -m "Add calculator improvement"
Push your branch:
git push origin feature/my-improvement
Open a Pull Request.

When contributing, please keep the calculator engine independent from the GUI whenever possible and add tests for new functionality.

## 👨‍💻 Author

Abderrahmane Tarek MEGHARI

AI & Data Science Student
ECE Paris

- GitHub: https://github.com/tarek200614
- LinkedIn: https://www.linkedin.com/in/abderrahmane-tarek-meghari
- Email: meghariabderrhmanetarek@gmail.com

## 📄 License

This project is released under the MIT License.

See the LICENSE file for the complete license text.

You are free to use, modify, distribute, and learn from the project in accordance with the license.

## ⭐ Acknowledgments

This project was developed as a practical Python project to strengthen skills in:

Python programming
Desktop application development
GUI architecture
Secure expression evaluation
Automated testing
Software engineering principles

Special attention was given to keeping the project simple, dependency-free, secure, and maintainable while providing a polished desktop user experience.

If you find the project useful, consider giving the repository a ⭐ on GitHub.

<p align="center"> <strong>🧮 Simple to use. 🔐 Secure by design. 🐍 Built with Python.</strong> </p> ```
