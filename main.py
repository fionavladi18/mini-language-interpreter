"""
main.py — Main driver

Reads source code from `test1.txt`, then runs the three-stage pipeline:
    tokenize  →  parse  →  evaluate

Catches errors raised by any stage:
  - ValueError is reported with its message, matching the project 
    specification for sample 5.
  - All other errors (syntax errors, uninitialized variables, etc.)
    print the generic message 'error'.
"""

import tokenizer
import parser
import interpreter

# Read the source file
with open("test1.txt", "r") as f:
    source = f.read()
try:

    # Step 1: Tokenize
    tokens = tokenizer.tokenize(source)

    # Step 2: Hand the tokens to the parser 
    parser.tokens_list = tokens
    parser.pos = 0

    # Step 3: Parse to get the AST
    ast = parser.parse_program()

    # Step 4: Interpret (evaluate and print)
    interpreter.execute(ast)
    
except ValueError as e:
    print("error, " + str(e))
except Exception:
    print("error")