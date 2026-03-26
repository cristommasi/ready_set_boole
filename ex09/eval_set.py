import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, eval_set


def main():

    TEST_CASES = [
        ("AB&", [{0, 1, 2}, {0, 3, 4}]),                          # {0}
        ("AB|", [{0, 1, 2}, {3, 4, 5}]),                          # {0, 1, 2, 3, 4, 5}
        ("A!",  [{0, 1, 2}]),                                     # {}
        ("AB^", [{1, 2, 3}, {2, 3, 4}]),                          # {1, 4}
        ("AB>", [{1, 2, 3}, {2, 3, 4}]),                          # {2,3,4}
        ("AB=", [{1, 2, 3}, {1, 2, 3}]),                          # {1, 2, 3}
        ("AB|C&", [{0, 1, 2}, {3, 4, 5}, {1, 3}]),                # {1,3}
        ("AB&C|", [{0, 1, 2}, {0, 3, 4}, {5, 6}]),                # {0, 5, 6}
        ("ABC||", [{0, 1}, {2, 3}, {4, 5}]),                      # {0,1,2,3,4,5}
        ("AB!&", [{0, 1, 2}, {0, 1, 2}]),                         # {}
        ("AB!&", [{0, 1, 2, 3}, {2, 3}]),                         # {0,1}
        ("AB&CD&|", [{0,1,2}, {1,2,3}, {4,5}, {5,6}]),            # {1,2,5}
    ]
    RES_CASES = [
        {0},
        {0, 1, 2, 3, 4, 5},
        set(),
        {1, 4},
        {2,3,4},
        {1, 2, 3},
        {1,3},
        {0, 5, 6},
        {0,1,2,3,4,5},
        set(),
        {0,1},
        {1,2,5}
    ]
    i = 0
    for formula, sets in TEST_CASES:

        
        print(f'\n{COLOR.WB}{sets} - {COLOR.RST}{COLOR.WB}{formula}{COLOR.RST}', end="")
        resSET = eval_set(formula, sets)

        try:
            assert resSET == RES_CASES[i], f' -> {COLOR.R}{resSET}{COLOR.RST}{COLOR.B} <-- Expected {RES_CASES[i]}{COLOR.RST}\n'
            print(f' -> {COLOR.BB}{resSET}{COLOR.RST}\n')
        except AssertionError as e:
            print(e)
        i += 1


if __name__ == "__main__":
    main()