import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../rsb_lib'))
from rsb_lib import COLOR, eval_formula


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
			("10&01|1111^!|&!>!|", True)
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
