from beartype import beartype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, AST


def toNNF(node, root=None):

    if node is None: return node

    if isinstance(node, AST.ValueNode): return node

    if node.op == '=': # Equivalence (A ⇔ B) ⇔ ((A ⇒ B) ∧ (B ⇒ A))

        left = toNNF(node.left)
        right = toNNF(node.right)
        new_node = AST.BinaryNode('&', AST.BinaryNode('>', left, right), AST.BinaryNode('>', right, left))
        return toNNF(new_node)
    
    if node.op == '>': # Material Condition (A ⇒ B) ⇔ (¬A ∨ B)

        left = toNNF(node.left)
        right = toNNF(node.right)
        new_node = AST.BinaryNode('|', AST.UnaryNode('!', left), right)
        return toNNF(new_node)
    
    if node.op == '!':

        child = node.right
        if isinstance(child, AST.ValueNode): return node
        
        
        if child.op == '!': # Elimination of double negation (¬¬A) ⇔ A 
            return toNNF(child.right)
        
        
        if child.op == '&': # De Morgan’s law  ¬(A ∧ B) ⇔ (¬A ∨ ¬B)

            new_structure = AST.BinaryNode('|', AST.UnaryNode('!', child.left), AST.UnaryNode('!', child.right))
            return toNNF(new_structure)
        
        if child.op == '|': # De Morgan’s law ¬(A ∨ B) ⇔ (¬A ∧ ¬B)

            new_structure = AST.BinaryNode('&', AST.UnaryNode('!', child.left), AST.UnaryNode('!', child.right))
            return toNNF(new_structure)
        
        return toNNF(AST.UnaryNode('!', toNNF(child)))
    
    # Continue down
    if node.op == '|' or node.op == '&':
        return AST.BinaryNode(node.op, toNNF(node.left), toNNF(node.right))
        
    raise ValueError("Unknown node type")


def toRPN(node):

    if isinstance(node, AST.ValueNode):
        return str(node.value)
    
    if isinstance(node, AST.UnaryNode):
        return toRPN(node.right) + '!'
    
    if isinstance(node, AST.BinaryNode):
        return toRPN(node.left) + toRPN(node.right) + node.op
    
    raise ValueError(f"Unknown node type in toRPN: {type(node)}")



@beartype
def negation_normal_form(formula: str) -> str:


    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")
    
    
    ast_tree = AST("VARS", "ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)
    nnf_root = toNNF(ast_tree.root)
    return toRPN(nnf_root)




def main():
	
	TEST_CASES = [
		"AB&!", # A!B!|
		"AB|!", # A!B!&
		"AB>",  # A!B|
		"AB=",  # AB&A!B!&|
		"AB="   # A!B!&C!|
	]
	for formula in TEST_CASES:

		
		try:
			resultNNP = negation_normal_form(formula)

			print(f'\n{COLOR.WB}{formula}{COLOR.RST} --> {COLOR.B}{resultNNP}{COLOR.RST}\n')
		except ValueError as e:
			print(f'\n{COLOR.WB}"{formula}"{COLOR.RST}\n\n{COLOR.RB}{e}{COLOR.RST}\n')


if __name__ == "__main__":
   main()

