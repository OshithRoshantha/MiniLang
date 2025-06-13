# MiniLang Compiler

A simple compiler for the MiniLang programming language.

## Project Overview

This project implements a simple compiler for MiniLang, a custom-designed programming language supporting:

- Variable declarations
- Assignments
- Arithmetic expressions
- Conditional statements (`if`/`else`)
- Loops (`while`)
- Print statements

The compiler is implemented in Python and covers all major phases: lexical analysis, parsing, semantic analysis, and intermediate code generation.

---

## Requirements
- Python 3.6+

## How to Run

1. Make sure you have Python installed on your system.
2. Open a terminal and navigate to the project directory.
3. To compile a MiniLang program:
   ```bash
   python3 compiler.py examples/example1.mini
   ```
4. To run the lexer separately:
   ```bash
   python3 lexer.py examples/example1.mini
   ```
5. To run the parser separately:
   ```bash
   python3 parser.py examples/example1.mini
   ```
6. To run the semantic analyzer:
   ```bash
   python3 semantic_analyzer.py examples/example1.mini
   ```
7. To generate intermediate code:
   ```bash
   python3 intermediate_code.py examples/example1.mini
   ```