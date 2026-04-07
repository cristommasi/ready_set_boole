import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../rsb_lib'))
from rsb_lib import numToBinStr, COLOR, MAX, graycode

def main():

    test_cases = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, MAX.U32, MAX.U32 - 1, MAX.U32 - 5, MAX.U32 + 1
    ]

    for n in test_cases:

        try:
            result = graycode(n)
            print(f'\n{COLOR.WB}TEST_CASE = G({n}){COLOR.RST}\n')
            print(f'{COLOR.B}n    = {numToBinStr(n, 32)}{COLOR.RST}')
            print(f'{COLOR.G}G(n) = {numToBinStr(result, 32)}{COLOR.RST}')

        except ValueError as e:

            print(f"\n{COLOR.WB}TEST_CASE = G({n}) {COLOR.RST}\n\n{COLOR.RB}{e}{COLOR.RST}\n")

            
if __name__ == "__main__":
   main()

