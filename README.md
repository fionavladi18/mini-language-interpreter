# PLP Project — Language Interpreter

An interpreter for a simple assignment-based language. Built in Python as a
project for the Programming Languages course.

## About the language

The language has two kinds of statements:

- **Normal assignments** — `x = expr;` — the variable can be reassigned later.
- **Single-assignment declarations** — `let x = expr;` — the variable is a constant,
  and its right-hand side may only reference literals or other `let`-defined variables.

Expressions support `+`, `-`, `*`, parentheses, unary `+`/`-`, integer literals,
and identifiers. Identifiers start with a letter or underscore; numbers
cannot have leading zeros (so `007` is a syntax error, but `0` is fine).

The full grammar was provided in the project specification.

## What the interpreter does

For any input program, the interpreter detects:

1. **Syntax errors** — invalid tokens, missing semicolons, malformed expressions.
2. **Uninitialized variables** — using a variable that was never assigned.
3. **Let-purity violations** — a `let` declaration whose right-hand side
   references a normal (mutable) variable.

If no errors are found, it executes the program and prints all variables
with their final values, in the order they were first declared.

## Project structure

The code is split into four files, each responsible for one stage of the pipeline:

```
tokenizer.py  →  parser.py  →  interpreter.py
                                     ↑
                                  main.py  (entry point)
```


- `tokenizer.py` — turns the source text into a list of tokens.
- `parser.py` — recursive-descent parser; builds an AST from the tokens.
- `interpreter.py` — walks the AST, evaluates expressions, prints results.
- `main.py` — wires the three stages together and handles errors.

## How to run

Requires Python 3.10 or later.

1. Place the program you want to run in `test1.txt`.
2. From the project folder, run:
```
   python main.py
```
3. The interpreter prints each variable's final value, or `error`.

## Sample input/output

Input (`test1.txt`):
```
let x = 1;
y = 2;
z = ---(x+y)*(x+-y);
```

Output:
```
x = 1
y = 2
z = 3
```

## What I learned from this project
The AST finally printing was the moment I understood what was going on. Before that, it felt like random functions calling each other.

The precedence thing was confusing because I kept thinking I forgot some rule, but it turned out the precedence comes from the parser structure itself.

I had worked with Python a bit before this, so it was rough at first, but it got easier as I went.