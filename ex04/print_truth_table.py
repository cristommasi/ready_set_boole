from beartype import beartype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, MAX, AST



@beartype
def print_truth_table(formula: str) -> None:

    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")
    
    ast_tree = AST("VARS", "ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)

    header = ' | '.join(ast_tree.formulaSet) + ' | ='
    separator = '|'.join(['---'] * (ast_tree.formulaSetSize + 1))
    print(f"| {header} |")
    print(f"|{separator}|")

    for i in range(2 ** ast_tree.formulaSetSize):
        
        ast_tree.assignValues(i)
        value = ast_tree.eval(ast_tree.root)
        row = ' | '.join(str(ast_tree.valuesDict[c]) for c in ast_tree.formulaSet)
        print(f"| {row} | {value} |")




def main():
	
	TEST_CASES = [
	    "AB&C|",     # (A & B) | C
	    "AB&C^",     # (A & B) ^ C
	    "A!",        # !A
	    "AB|C&",     # (A | B) & C
	    "ABC&&",     # A & B & C
	    "AB|C|",     # A | B | C
	    "AB>!",      # !(A ⇒ B)
	    "AB=!",      # !(A ⇔ B)
	    "ABC|^",     # A ^ (B | C)
	    "AB!&",      # A & !B
	    "AB!|",      # A | !B
	    "AB>C&",    # (A ⇒ B) & C
	    "ABC=>",     # (A & B) ⇒ C
	    "AB^C^",     # A ^ B ^ C
	    "AB!C&|",    # (A | (!B & C))
	    "AB|C>!",    # !( (A | B) ⇒ C )
		"A",
		"AB!|",
		"AB&!",
		"AB>",
		"AB=",
		"A!B|B!A|&",
		"AB&A!B!&|",
		"AB^",
		"AB&",
		"AB|",
		"AB&!",
		"AB^!",
		"A!B|"
	]
	for formula in TEST_CASES:

		print(f'\n{COLOR.WB}{formula}{COLOR.RST}\n')
		try:
			print_truth_table(formula)
		except ValueError as e:
			print(f'\n{COLOR.WB}"{formula}"{COLOR.RST}\n\n{COLOR.RB}{e}{COLOR.RST}\n')


if __name__ == "__main__":
   main()
