
from eval_formula import eval_formula

RESET   = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
WHITE   = "\033[1;37m"


false = [
	"0" #false
]

true = [
	"1" #true
]

negation = [
	"1!", #false
	"0!" #true
]

conjunction = [
	"00&", #false
	"01&", #false
	"10&", #false
	"11&" #true
]

disjunction = [
	"00|", #false
	"01|", #true
	"10|", #true
	"11|" #true
]

exclusive_disjunction = [
	"00^", #false
	"01^", #true
	"10^", #true
	"11^" #false  
]

material_condition = [
	"00>", #true
	"01>", #true
	"10>", #false
	"11>" #true
]

logical_equivalence = [
	"00=", #true
	"01=", #false
	"10=", #false
	"11=" #true
]

subject_test_cases = [
	"10&", #false
	"10|", #true
	"11>", #true
	"10=", #false
	"1011||=", #true
]

longer_test_cases = [
	"10&01|1111^!|&!>!|", #true
	"11&11|1001^!&&!>!^",
	"1011|=>1|00!^&"
]


TEST_CASES = {
	"false (⊥)": false, 
	"true (⊤)": true, 
	"Negation (¬)": negation, 
	"Conjunction (∧)": conjunction, 
	"Disjunction (∨)": disjunction, 
	"Exclusive disjunction (⊕)": exclusive_disjunction, 
	"Material condition (⇒)": material_condition,
	"Logical equivalence (⇔)": logical_equivalence,
	"Subject testcases": subject_test_cases, 
	"Longer testcases": longer_test_cases,

}


def main():
	
	for title, tests in TEST_CASES.items():

		print(f'\n{WHITE}{title}{RESET}')
		for test in tests:
			try:
				result = eval_formula(test)
				print(f'\n"{test}" {GREEN if result else RED}{result}{RESET}')

			except ValueError as e:
				print(f'\n{WHITE}"{test}"{RESET}\n\n{RED}{e}{RESET}\n')


if __name__ == "__main__":
   main()

