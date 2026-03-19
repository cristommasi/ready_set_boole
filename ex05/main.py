
from negation_normal_form import negation_normal_form
from negation_normal_form import print_truth_table

import importlib.util
mod = importlib.util.spec_from_file_location("ex00", "../ex04/print_truth_table.py")
ex04 = importlib.util.module_from_spec(mod)
mod.loader.exec_module(ex04)



RESET   = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
WHITE   = "\033[1;37m"


TEST_CASES = [
	"AB&!", # A!B!|
	"AB|!", # A!B!&
	"AB>",  # A!B|
	"AB=",  # AB&A!B!&|
	"AB="   # A!B!&C!|
]

def main():
	
	for formula in TEST_CASES:

		
		try:
			resultNNP = negation_normal_form(formula)
			print_truth_table(formula)
			print(' ')
			print_truth_table(resultNNP)

			print(f'\n{WHITE}{formula}{RESET} --> {BLUE}{resultNNP}{RESET}\n')
		except ValueError as e:
			print(f'\n{WHITE}"{formula}"{RESET}\n\n{RED}{e}{RESET}\n')


if __name__ == "__main__":
   main()

