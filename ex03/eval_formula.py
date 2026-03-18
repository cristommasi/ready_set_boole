from beartype import beartype


class AST:
     
    class Node:
        pass
    
    class ValueNode(Node):

        def __init__(self, value):
            self.value = value

    class UnaryNode(Node):

        def __init__(self, op, right):
            self.op = op
            self.right = right

    class BinaryNode(Node):

        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

    def __init__(self, allowed: str, formula: str):
        self.allowed = allowed
        self.root = self.create(formula)
    
    def create(self, formula: str):
        stack = []

        for c in formula:

            if c not in self.allowed:
                raise ValueError(f"Error: Unknown Character: {c}")

            if c == '0' or c == '1':
                stack.append(self.ValueNode(int(c)))

            elif c == '!':
                if not stack:
                    raise ValueError(f"Error: Malformed formula: {formula}")
                right = stack.pop()
                stack.append(self.UnaryNode(c, right))

            else:
                if len(stack) < 2:
                    raise ValueError(f"Error: Malformed formula: {formula}")
                right = stack.pop()
                left = stack.pop()
                stack.append(self.BinaryNode(c, left, right))

        if len(stack) != 1:
            raise ValueError(f"Error: Malformed formula: {formula}")

        return stack[0]

    def eval(self, node = None):
        if node is None:
            node = self.root

        if isinstance(node, self.ValueNode):
            return node.value

        if isinstance(node, self.UnaryNode):
            return int(not self.eval(node.right))

        if isinstance(node, self.BinaryNode):
            left = self.eval(node.left)
            right = self.eval(node.right)

            if node.op == '&':
                return left & right
            if node.op == '|':
                return left | right
            if node.op == '^':
                return left ^ right
            if node.op == '>':
                return int((not left) | right)
            if node.op == '=':
                return int(left == right)

        raise ValueError("Unknown node type")




@beartype
def eval_formula(formula: str) -> bool:

    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")
    

    ast_tree = AST("10!|&^>=", formula)

    return bool(ast_tree.eval())
