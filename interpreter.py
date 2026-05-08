"""
interpreter.py — Evaluation of the AST produced by the parser.

Walks the AST and computes the value of each expression, then
executes each assignment statement, maintaining a symbol table that
maps each variable name to a (value, is_let) pair.

Enforces two semantic rules:
  1. A variable used on the right-hand side must have been defined
     previously (otherwise NameError is raised).
  2. The right-hand side of a `let` declaration may only reference
     other `let`-defined variables (otherwise ValueError is raised
     with the message 'normal variables in let expression').

After all statements are executed, prints each variable's value in
the order it was first declared.

Author: Fiona Vladi
"""
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
    for name in order:
        value, _ = env[name]
        print(name + " = " + str(value))