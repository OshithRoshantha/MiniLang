# MiniLang Compiler

A simple compiler for the MiniLang programming language.

---

## Project Overview

This project implements a simple compiler for MiniLang, a custom-designed programming language supporting:

- Variable declarations
- Assignments
- Arithmetic expressions
- Conditional statements (`if`/`else`)
- Loops (`while`)
- Print statements

The compiler is implemented in Python and covers all major phases:
- **Lexical Analysis** ([`lexer.py`](lexer.py))
- **Parsing** ([`parser.py`](parser.py))
- **Semantic Analysis** ([`semanticAnalyzer.py`](semanticAnalyzer.py))
- **Intermediate Code Generation** ([`intermediateCode.py`](intermediateCode.py))

---

## Project Structure

```
MiniLang/
├── compiler.py
├── intermediateCode.py
├── lexer.py
├── parser.py
├── semanticAnalyzer.py
├── symbolTable.py
├── examples/
│   ├── arithmetic.mini
│   ├── fibonacci.mini
│   └── nestedIf.mini
├── __pycache__/
├── .gitignore
└── README.md
```

- **`compiler.py`**: Main driver script that runs all compilation phases.
- **`lexer.py`**: Tokenizes MiniLang source code.
- **`parser.py`**: Builds an Abstract Syntax Tree (AST) from tokens.
- **`semanticAnalyzer.py`**: Checks for semantic errors (e.g., undeclared variables).
- **`intermediateCode.py`**: Generates intermediate code from the AST.
- **`symbolTable.py`**: Implements a symbol table for variable scope management.
- **`examples/`**: Sample MiniLang programs.

---

## Requirements

- Python 3.6 or higher

---

## How to Run

1. Make sure you have Python installed on your system.
2. Open a terminal and navigate to the project directory.

### Compile a MiniLang Program

```bash
python3 compiler.py examples/arithmetic.mini
```

### Run Individual Phases

- **Lexer:**
  ```bash
  python3 lexer.py examples/arithmetic.mini
  ```

- **Parser:**
  ```bash
  python3 parser.py examples/arithmetic.mini
  ```

- **Semantic Analyzer:**
  ```bash
  python3 semanticAnalyzer.py examples/arithmetic.mini
  ```

- **Intermediate Code Generator:**
  ```bash
  python3 intermediateCode.py examples/arithmetic.mini
  ```

---

## Example MiniLang Programs

See the [`examples/`](examples/) directory for sample programs:

- [`arithmetic.mini`](examples/arithmetic.mini): Demonstrates arithmetic operations and print statements.
- [`fibonacci.mini`](examples/fibonacci.mini): Computes Fibonacci numbers using a loop.
- [`nestedIf.mini`](examples/nestedIf.mini): Shows nested conditional statements.

---

## Notes

- The compiler reports lexical, syntax, and semantic errors with line numbers.
- Intermediate code is printed in a simple three-address code format.
- The project is for educational purposes and can be extended with more language features.

---