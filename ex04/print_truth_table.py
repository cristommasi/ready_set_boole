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
        self.formulaSet = sorted({c for c in formula if c.isupper()})
        self.formulaSetSize = len(self.formulaSet)
        self.valuesDict = {}
    
    def assignValues(self, bValue: int):

        for i, c in enumerate(self.formulaSet):
            self.valuesDict[c] = (bValue >> (self.formulaSetSize - 1 - i)) & 1

    def create(self, formula: str):
        stack = []

        for c in formula:

            if c not in self.allowed:
                raise ValueError(f"Error: Unknown Character: {c}")

            if c.isupper():
                stack.append(self.ValueNode(c))

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

        if isinstance(node, self.ValueNode):
            return self.valuesDict[node.value]

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
def print_truth_table(formula: str) -> None:

    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")
    
    ast_tree = AST("ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)

    header = ' | '.join(ast_tree.formulaSet) + ' | ='
    separator = '|'.join(['---'] * (ast_tree.formulaSetSize + 1))
    print(f"| {header} |")
    print(f"|{separator}|")

    for i in range(2 ** ast_tree.formulaSetSize):
        ast_tree.assignValues(i)
        value = ast_tree.eval(ast_tree.root)
        row = ' | '.join(str(ast_tree.valuesDict[c]) for c in ast_tree.formulaSet)
        print(f"| {row} | {value} |")

