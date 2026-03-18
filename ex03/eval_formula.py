from beartype import beartype

class Node(object):
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


def parse_formula(formula: str):

    stack = []
    allowed = "10!|&^>="

    for c in formula:

        if c not in allowed:
            raise ValueError(f'Error: Unknown Character: {c}')
        
        if c == '0' or c == '1':
            stack.append(ValueNode(int(c)))

        elif c == '!':

            if not stack:
                raise ValueError(f'Error: Malformed formula: {formula}')
            right = stack.pop()
            stack.append(UnaryNode(c, right))

        else:

            if len(stack) < 2:
                raise ValueError(f'Error: Malformed formula: {formula}')
            
            right = stack.pop()
            left = stack.pop()
            stack.append(BinaryNode(c, left, right))


    if len(stack) != 1:
        raise ValueError(f'Error: Malformed formula: {formula}')
    
    return stack[0]

def eval_ast(node):

    if isinstance(node, ValueNode):
        return node.value

    if isinstance(node, UnaryNode):
        return int(not eval_ast(node.right))

    if isinstance(node, BinaryNode):

        left = eval_ast(node.left)
        right = eval_ast(node.right)
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
    

    node = parse_formula(formula)
    return bool(eval_ast(node))
