from beartype import beartype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, AST


def sat(formula: str) -> bool:

    if not isinstance(formula, str):
        raise ValueError("Inputs must be string")
    
    ast_tree = AST("VARS", "ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)
    ast_tree.print_truth_table(formula)
    for i in range(2 ** ast_tree.formulaSetSize):

        ast_tree.assignValues(i)
        value = ast_tree.eval(ast_tree.root)
        if value == True:
              return True
    return False



def main():

    TEST_CASES = {

        "AB|":      True,
        "AB&":      True,
        "AA!&":     False,
        "AA^":      False,
        "A":        True,
        "A!":       True,
        "AA|":      True,
        "AA!|":     True,
        "AB|C|":    True,
        "AA!&BB!&|": False,
        "AB^":      True,
        "AB>":      True,
        "AB=":      True,
        "ABC&&":    True,
        "ABC||":    True,
        "ABC&|":    True,
        "A!!":      True,
        "A!!!":     True,
        "AB>BA>&":  True,
        "AB=!":     True,
    }

    for formula, expected in TEST_CASES.items():

        try:
            resultSAT = sat(formula)

            assert resultSAT == expected, f'\n{COLOR.WB}{formula}{COLOR.RST} --> {COLOR.RB}{resultSAT}{COLOR.RST}\n'


            print(f'\n{COLOR.WB}{formula}{COLOR.RST} --> {COLOR.GB}{resultSAT}{COLOR.RST}\n')

        except ValueError as e:
            print(f"\n{e}\n")



if __name__ == "__main__":
    main()
