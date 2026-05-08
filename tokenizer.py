"""
tokenizer.py — Lexical analysis for the language.

Reads raw source code (a string) and produces a list of tokens.
Each token is a tuple of the form (TYPE, VALUE), where TYPE is one of:
LET, IDENT, NUMBER, EQUALS, PLUS, MINUS, STAR, LPAREN, RPAREN, SEMI.

Whitespace is skipped. Multi-digit numbers with leading zeros
(e.g. '007') are rejected as syntax errors.
"""

def tokenize(source):
    tokens = []
    i = 0
    n = len(source)

    while i < n:
        c = source[i]
        if c == " " or c == "\t" or c == "\n" or c == "\r":
            i = i + 1
            continue

        if c.isdigit():
            start = i
            while i < n and source[i].isdigit():
                i = i + 1
            num_text = source[start:i]
            if len(num_text) > 1 and num_text[0] == "0":
                raise SyntaxError("Invalid number with leading zero: " + num_text)
            tokens.append(("NUMBER", int(num_text)))
            continue
        if c.isalpha() or c == "_":
            start = i
            while i < n and (source[i].isalnum() or source[i] == "_"):
                i = i + 1
            word = source[start:i]
            if word == "let":
                tokens.append(("LET", "let"))
            else:
                tokens.append(("IDENT", word))
            continue
        if c == "=":
            tokens.append(("EQUALS", "="))
            i = i + 1
            continue
        if c == "+":
            tokens.append(("PLUS", "+"))
            i = i + 1
            continue
        if c == "-":
            tokens.append(("MINUS", "-"))
            i = i + 1
            continue
        if c == "*":
            tokens.append(("STAR", "*"))
            i = i + 1
            continue
        if c == "(":
            tokens.append(("LPAREN", "("))
            i = i + 1
            continue
        if c == ")":
            tokens.append(("RPAREN", ")"))
            i = i + 1
            continue
        if c == ";":
            tokens.append(("SEMI", ";"))
            i = i + 1
            continue

        raise SyntaxError("Unexpected character: " + c)
    return tokens
