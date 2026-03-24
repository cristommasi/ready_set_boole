from beartype import beartype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, AST



def distribute(left, right):

    
    if isinstance(left, AST.BinaryNode) and left.op == '&': # (A & B) | C  →  (A | C) & (B | C)

        return AST.BinaryNode('&', distribute(left.left, right), distribute(left.right, right))
    
    if isinstance(right, AST.BinaryNode) and right.op == '&': # A | (B & C)  →  (A | B) & (A | C)

        return AST.BinaryNode('&', distribute(left, right.left), distribute(left, right.right))
    

    return AST.BinaryNode('|', left, right)

def toCNF(node):

    if isinstance(node, AST.ValueNode): return node

    if isinstance(node, AST.UnaryNode): return node

    if node.op == '&':

        return AST.BinaryNode('&', toCNF(node.left), toCNF(node.right))
    
    if node.op == '|':

        left  = toCNF(node.left)
        right = toCNF(node.right)
        return distribute(left, right)
    
    raise ValueError(f"Unexpected operand in toCNF: {node.op}")


def flatten(node, op):

    if isinstance(node, AST.BinaryNode) and node.op == op:
        return flatten(node.left, op) + flatten(node.right, op)
    
    return [node]


def toRPNFlatten(node):

    if isinstance(node, AST.ValueNode):
        return str(node.value)
    
    if isinstance(node, AST.UnaryNode):
        return toRPNFlatten(node.right) + '!'
    
    if isinstance(node, AST.BinaryNode):

        leaves = flatten(node, node.op)
        result = ''.join(toRPNFlatten(leaf) for leaf in leaves)
        result += node.op * (len(leaves) - 1)
        return result
    
    raise ValueError(f"Unknown node type in toRPNFlatten: {type(node)}")


def conjunctive_normal_form(formula: str) -> str:

    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")
    
    ast_tree = AST("VARS", "ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)
    nnf = ast_tree.toNNF(ast_tree.root)
    cnf = toCNF(nnf)
    return toRPNFlatten(cnf)


def main():
	
	TEST_CASES = [
		"AB&!",    # A!B!|
		"AB|!",    # A!B!&
		"AB|C&",   # AB|C&
		"AB|C|D|", # ABCD|||
		"AB&C&D&", # ABCD&&&
        "AB&!C!|", # A!B!C!||
        "AB|!C!&",  # A!B!C!&&
        "AB|!C!D&E|&"
	]
	for formula in TEST_CASES:

		
		try:
			resultCNF = conjunctive_normal_form(formula)

			print(f'\n{COLOR.WB}{formula}{COLOR.RST} --> {COLOR.B}{resultCNF}{COLOR.RST}\n')
		except ValueError as e:
			print(f'\n{COLOR.WB}"{formula}"{COLOR.RST}\n\n{COLOR.RB}{e}{COLOR.RST}\n')


if __name__ == "__main__":
   main()

