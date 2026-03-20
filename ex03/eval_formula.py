from beartype import beartype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import numToBinStr, COLOR, MAX, AST



def evalAST(node, root=None):

    if node is None: 
        node = root

    if isinstance(node, AST.ValueNode):
        return node.value
    
    if isinstance(node, AST.UnaryNode):
        return int(not evalAST(node.right))
    
    if isinstance(node, AST.BinaryNode):

        left = evalAST(node.left)
        right = evalAST(node.right)

        if node.op == '&': return left & right

        if node.op == '|': return left | right

        if node.op == '^': return left ^ right

        if node.op == '>': return int((not left) | right)

        if node.op == '=': return int(left == right)
        
    raise ValueError("Unknown node type")



@beartype
def eval_formula(formula: str) -> bool:

    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")

    ast_tree = AST("CONST", "10!|&^>=", formula)

    return bool(evalAST(ast_tree.root))



def main():
	
	TEST_CASES = {
		"false (⊥)": [
			("0", False),
		],
		"true (⊤)": [
			("1", True),
		],
		"Negation (¬)": [
			("1!", False),
			("0!", True),
		],
		"Conjunction (∧)": [
			("00&", False),
			("01&", False),
			("10&", False),
			("11&", True),
		],
		"Disjunction (∨)": [
			("00|", False),
			("01|", True),
			("10|", True),
			("11|", True),
		],
		"Exclusive disjunction (⊕)": [
			("00^", False),
			("01^", True),
			("10^", True),
			("11^", False),
		],
		"Material condition (⇒)": [
			("00>", True),
			("01>", True),
			("10>", False),
			("11>", True),
		],
		"Logical equivalence (⇔)": [
			("00=", True),
			("01=", False),
			("10=", False),
			("11=", True),
		],
		"Subject testcases": [
			("10&",       False),
			("10|",       True),
			("11>",       True),
			("10=",       False),
			("1011||=",   True),
		],
		"Longer testcases": [
			("10&01|1111^!|&!>!|", True),
			("11&11|1001^!&&!>!^", None),  # unknown expected
			("1011|=>1|00!^&",     None),  # unknown expected
		],
	}
	 
	for title, tests in TEST_CASES.items():
		
		print(f'\n{COLOR.WB}{title}{COLOR.RST}')
		
		for formula, expected in tests:
			
			try:
                        
				result = eval_formula(formula)
				correct = expected is None or result == expected
                        
				status = COLOR.G if correct else COLOR.RB
                        
				print(f'"{formula}" {status}{result}{COLOR.RST}', end='')
                        
				if expected is not None and not correct:
					print(f'  ← expected {expected}', end='')
				print()
				
			except ValueError as e:
				print(f'\n{COLOR.WB}"{formula}"{COLOR.RST}\n\n{COLOR.RB}{e}{COLOR.RST}\n')
				
if __name__ == "__main__":
   main()
