import sys, os
from beartype  import beartype
sys.path.append(os.path.join(os.path.dirname(__file__), '../rsb_lib'))
from rsb_lib import COLOR, MAX, numToBinStr, map


def main():

    TEST_CASES = [
        [0, 0],
        [MAX.U16, MAX.U16],
        [1, 0],
        [0, 1],
        [2, 3],
        [3, 2],
    ]

    for sets in TEST_CASES:

        x = sets[0]
        y = sets[1]
        print(f'{COLOR.WB}map({x}, {y}){COLOR.RST}\n')
        print(f'{numToBinStr(x, 32)} = x: u16')
        print(f'{numToBinStr(y, 32)} = y: u16')
        resSET = map(x, y)

        try:
            print('-----------------------------------------------------------------------')
            print(f'{numToBinStr(round(resSET * MAX.U32), 32)} = R: U32')
            print(f'{COLOR.BB}({resSET}) = R: F64{COLOR.RST}\n')
        except AssertionError as e:
            print(e)


if __name__ == "__main__":
    main()