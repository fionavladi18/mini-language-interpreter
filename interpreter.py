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

# ---------- Parser ----------

# Global state for the parser.
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

# ---------- Interpreter ----------

def eval_expr(node, env, inside_let):
    kind = node[0]

    if kind == "Number":
        return node[1]

    if kind == "Var":
        name = node[1]
        if name not in env:
            raise NameError("Uninitialized variable: " + name)
        value, is_let_var = env[name]
        if inside_let and not is_let_var:
            raise ValueError("normal variables in let expression")
        return value

    if kind == "Neg":
        return -eval_expr(node[1], env, inside_let)

    if kind == "Add":
        return eval_expr(node[1], env, inside_let) + eval_expr(node[2], env, inside_let)

    if kind == "Sub":
        return eval_expr(node[1], env, inside_let) - eval_expr(node[2], env, inside_let)

    if kind == "Mul":
        return eval_expr(node[1], env, inside_let) * eval_expr(node[2], env, inside_let)

    raise Exception("Unknown node kind: " + kind)

def execute(ast):
    env = {}
    order = [] 

    for stmt in ast:
        kind = stmt[0]
        name = stmt[1]
        expr = stmt[2]

        if kind == "Let":
            value = eval_expr(expr, env, inside_let=True)
            env[name] = (value, True)
        else:  # "Assign"
            value = eval_expr(expr, env, inside_let=False)
            env[name] = (value, False)

        if name not in order:
            order.append(name)

    # Print all variables in declaration order
    for name in order:
        value, _ = env[name]
        print(name + " = " + str(value))

with open("test1.txt", "r") as f:
    source = f.read()

try:
    tokens_list = tokenize(source)
    pos = 0
    ast = parse_program()
    execute(ast)
except ValueError as e:
    print("error, " + str(e))
except Exception:
    print("error")


