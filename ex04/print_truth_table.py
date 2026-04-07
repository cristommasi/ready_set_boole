import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../rsb_lib'))
from rsb_lib import COLOR, print_truth_table


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
