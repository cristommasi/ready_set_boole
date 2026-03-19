
from print_truth_table import print_truth_table

RESET   = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
WHITE   = "\033[1;37m"



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
    "AB> C&",    # (A ⇒ B) & C
    "ABC=>",     # (A & B) ⇒ C
    "AB^C^",     # A ^ B ^ C
    "AB!C&|",    # (A | (!B & C))
    "AB|C>!",    # !( (A | B) ⇒ C )
	"A",
	"AB!|",
	"AB&CDE!|^=F&",
	"ABCD|=>F|GH!^&",
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

def main():
	
	for formula in TEST_CASES:

		print(f'\n{WHITE}{formula}{RESET}\n')
		try:
			print_truth_table(formula)
		except ValueError as e:
			print(f'\n{WHITE}"{formula}"{RESET}\n\n{RED}{e}{RESET}\n')


if __name__ == "__main__":
   main()

