import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../rsb_lib'))
from rsb_lib import COLOR, MAX, powerset


def main():

    TEST_CASES = [
        {1, 2, 3},
        {2, 3}
    ]

    for test_case in TEST_CASES:

        print(f'\n{COLOR.WB}TEST_CASE = {test_case}{COLOR.RST}\n')
        powersetLIST = powerset(test_case)
        for each_set in powersetLIST:

            print('{', end="")
            each_set = list(each_set)
            cardinal = len(each_set)
            for i in range(cardinal):
                print(f'{each_set[i]}', end="")
                if i + 1 != cardinal:
                    print(",", end="")
            else:
                if cardinal == 0:
                    print(' ', end="")

            print('}')

        

if __name__ == "__main__":
    main()