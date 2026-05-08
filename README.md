# Mini Language Interpreter

An interpreter for a simple assignment-based language, written in Python.
Built as a project for the Programming Languages and Paradigms course.

## The language

The language supports two kinds of statements:

- Normal assignments: `x = expr;`
- Single-assignment (constant) declarations: `let x = expr;`

Expressions support `+`, `-`, `*`, parentheses, unary `+`/`-`, integer literals, and identifiers.

## What the interpreter detects

1. **Syntax errors** — invalid tokens, missing semicolons, malformed expressions, leading-zero numbers, etc.
2. **Uninitialized variables** — using a variable on the right-hand side that was never assigned.
3. **Let-purity violations** — a `let` expression that references a normal (mutable) variable.
4. **Successful programs** — prints all variable values after execution.

## How it works

The interpreter is structured in three logical components, all in `interpreter.py`:

1. **Tokenizer** — turns source code into a list of tokens.
2. **Parser** — recursive-descent parser that builds an abstract syntax tree (AST).
3. **Evaluator** — walks the AST, maintains a symbol table, enforces semantic rules, and prints results.

## How to run

Requires Python 3.10 or later.

1. Put your source code in `test1.txt`.
2. Run: python interpreter.py
3. The interpreter prints the variable values, or `error` (with an explanation for let-violations).