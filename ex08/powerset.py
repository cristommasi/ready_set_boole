from beartype import beartype
from beartype.typing import List, Set
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, MAX


@beartype
def powerset(s: Set[int]) -> List[Set[int]]:

    s = List(s)

    for c in s:
        if c < 0 or c > MAX.U32:
            raise ValueError("Inputs in sets must be 32bit unsigned integer and in range.")
    
    cardinal = len(s)
    powersets: List[Set[int]] = []

    for bit in range(1 << cardinal):

        new_set: Set[int] = set()
        for j in range(cardinal):

            if (bit >> j) & 1:
                new_set.add(s[j])
                
        powersets.append(new_set)

    return powersets


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