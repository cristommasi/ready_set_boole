import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../rsb_lib'))
from rsb_lib import COLOR, AST, conjunctive_normal_form


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

