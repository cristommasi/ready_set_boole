from beartype import beartype
import ast


def parse_formula(formula: str):

    stack = []
    allowed = "10!|&^>="

    for c in formula:

        if c not in allowed:
            raise ValueError(f'Error: Unknown Character: {c}')
        
        if c.isdigit():
            stack.append(ast.Constant(value=int(c)))

        elif c == '!':

            if not len(stack):
                raise ValueError(f'Error: Malformed formula: {formula}')
            right = stack.pop()
            node = ast.UnaryOp(op=ast.Not(), operand=right)
            stack.append(node)

        else:

            if len(stack) < 2:
                raise ValueError(f'Error: Malformed formula: {formula}')
            
            right = stack.pop()
            left = stack.pop()
            if c == '&':
                node = ast.BinOp(left=left, op=ast.BitAnd(), right=right)
            elif c == '|':
                node = ast.BinOp(left=left, op=ast.BitOr(), right=right)
            elif c == '^':
                node = ast.BinOp(left=left, op=ast.BitXor(), right=right)
            elif c == '>':
                node = ast.Compare(left=left, ops=[ast.LtE()], comparators=[right])
            elif c == '=':
                node = ast.Compare(left=left, ops=[ast.Eq()], comparators=[right])

            stack.append(node)
    if len(stack) > 1:
        raise ValueError(f"Malformed formula: leftover operands")
    return stack[0]


@beartype
def eval_formula(formula: str) -> bool:

    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")
    

    node = parse_formula(formula)
    tree = ast.Expression(body=node)
    ast.fix_missing_locations(tree)
    code = compile(tree, "<ast>", "eval")
    result = eval(code)
    return bool(result)
