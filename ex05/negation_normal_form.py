import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, negation_normal_form

def main():
	
	TEST_CASES = [
		"AB&!",    # A!B!|
		"AB|!",    # A!B!&
		"AB>",     # A!B|
		"AB=",     # AB&A!B!&|
		"AB=",     # A!B!&C!|
        "AB&!C!|", # A!B!|C!|
		"AB^"      # AB|A!B!|&
	]
	for formula in TEST_CASES:

		
		try:
			resultNNP = negation_normal_form(formula)

			print(f'\n{COLOR.WB}{formula}{COLOR.RST} --> {COLOR.B}{resultNNP}{COLOR.RST}\n')
		except ValueError as e:
			print(f'\n{COLOR.WB}"{formula}"{COLOR.RST}\n\n{COLOR.RB}{e}{COLOR.RST}\n')


if __name__ == "__main__":
   main()

