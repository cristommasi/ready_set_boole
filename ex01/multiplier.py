from beartype import beartype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import numToBinStr, COLOR, MAX, adder




@beartype
def multiplier(a: int, b: int) -> int:
    
    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0 or a > MAX.U32 or b > MAX.U32:
        raise ValueError("Inputs must be 32bit unsigned integer and in range.")
    
    RES = 0
    while b != 0:

        if b & 1:
            RES = adder(RES, a)
            
        a = (a << 1) & MAX.U32
        b = b >> 1

    return RES & MAX.U32




def main():

    test_cases = [
        [25, 3], [0, 0], [15, 3], [1234, 5678], [1, 444], [7, 1], [15, 1], [255, 523], [234, 43], #regular expressions
        [MAX.U32, 0], [0, MAX.U32], [MAX.U32 - 1, 1], [MAX.U32, 2], #should work and wrap up if exceeds limit
        [MAX.U64, 0], [-1, 5], [5, -1], [-2, -3], #will throw error
        [65535, 65535], [65536, 65536],
        [244, 15]
    ]

    for a, b in test_cases:

        expected = (a * b) & MAX.U32
        try:

            result = multiplier(a, b)

            print(f'\n{COLOR.WB}TEST_CASE = [{a}, {b}]{COLOR.RST}\n')
            print(f'  {numToBinStr(a, 32)}')
            print(f'* {numToBinStr(b, 32)}')
            print("--------------------------------------------------------")
            print(f'{COLOR.B}  {numToBinStr(expected, 32)}{COLOR.RST} - a * b')
            print(f'{COLOR.G}  {numToBinStr(result, 32)}{COLOR.RST} - multiplier(a, b)\n')

            assert result == expected, f"multiplier({a},{b}) = {result}, expected {expected}"
            

        except ValueError as e:

            print(f"\n{COLOR.WB}TEST_CASE = [{a}, {b}] {COLOR.RST}\n\n{COLOR.RB}{e}{COLOR.RST}\n")

            

if __name__ == "__main__":
   main()
