"""
parser.py — Syntactic analysis for the language.

Implements a recursive-descent parser that consumes the token list
produced by the tokenizer and builds an abstract syntax tree (AST).
AST nodes are represented as nested tuples, e.g. ('Add', left, right).

The parser exposes a `parse_program` function that returns a list of
statement nodes. The token stream is held in module-level variables
`tokens_list` and `pos`, which the caller (main.py) sets before parsing.

Invalid syntax — a missing semicolon, a malformed expression,
unmatched parentheses, etc. — raises SyntaxError.
"""
tokens_list = []
pos = 0
def peek():
    if pos < len(tokens_list):
        return tokens_list[pos]
    return ("EOF", None)
def advance():
    global pos
    tok = peek()
    pos = pos + 1
    return tok
def expect(token_type):
    tok = peek()
    if tok[0] != token_type:
        raise SyntaxError("Expected " + token_type + " but got " + tok[0])
    return advance()
def parse_fact():
    tok = peek()
    if tok[0] == "LPAREN":
        advance()
        node = parse_exp()
        expect("RPAREN")
        return node
    if tok[0] == "MINUS":
        advance()
        child = parse_fact()
        return ("Neg", child)
    if tok[0] == "PLUS":
        advance()
        child = parse_fact()
        return child
    if tok[0] == "NUMBER":
        advance()
        return ("Number", tok[1])
    if tok[0] == "IDENT":
        advance()
        return ("Var", tok[1])
    raise SyntaxError("Unexpected token in factor: " + str(tok))
def parse_term():
    node = parse_fact()
    while peek()[0] == "STAR":
        advance()                     
        right = parse_fact()
        node = ("Mul", node, right)
    return node
def parse_exp():
    node = parse_term()
    while peek()[0] == "PLUS" or peek()[0] == "MINUS":
        op = advance()              
        right = parse_term()
        if op[0] == "PLUS":
            node = ("Add", node, right)
        else:
            node = ("Sub", node, right)
    return node
def parse_assignment():
    is_let = False
    if peek()[0] == "LET":
        advance()                      
        is_let = True
    name_tok = expect("IDENT")          
    name = name_tok[1]                   
    expect("EQUALS")                     
    expr = parse_exp()                  
    expect("SEMI")                     
    if is_let:
        return ("Let", name, expr)
    else:
        return ("Assign", name, expr)   
def parse_program():
    statements = []
    while peek()[0] != "EOF":
        stmt = parse_assignment()
        statements.append(stmt)
    return statements
