import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import numToBinStr, COLOR, MAX, adder


def main():

    test_cases = [
        [25, 3], [0, 0], [15, 1], [1234, 5678], [1, 1], [7, 1], [15, 1], [255, 1], [65535, 1], #regular expressions with carry
        [MAX.U32, 0], [0, MAX.U32], [MAX.U32 - 1, 1], [MAX.U32, 2], #should work and wrap up if exceeds limit
        [MAX.U64, 0], [-1, 5], [5, -1], [-2, -3], #will throw error
        [MAX.U32, 1]
    ]
    for a, b in test_cases:

        expected = (a + b) & MAX.U32
        try:
            result = adder(a, b)

            print(f'\n{COLOR.WB}TEST_CASE = [{a}, {b}]{COLOR.RST}\n')
            print(f'  {numToBinStr(a, 32)}')
            print(f'+ {numToBinStr(b, 32)}')
            print("--------------------------------------------------------")
            print(f'{COLOR.B}  {numToBinStr(expected, 32)}{COLOR.RST} - a + b')
            print(f'{COLOR.G}  {numToBinStr(result, 32)}{COLOR.RST} - adder(a, b)\n')

            assert result == expected, f"adder({a},{b}) = {result}, expected {expected}"
            

        except ValueError as e:

            print(f"\n{COLOR.WB}TEST_CASE = [{a}, {b}] {COLOR.RST}\n\n{COLOR.R}{e}{COLOR.RST}\n")

            


if __name__ == "__main__":
   main()