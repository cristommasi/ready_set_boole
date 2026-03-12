
from graycode import graycode
from beartype import beartype

RESET   = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
WHITE   = "\033[1;37m"

U32_MAX = 4294967295

test_cases = [
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, -1, U32_MAX, U32_MAX - 1, U32_MAX - 5, U32_MAX + 1
]

@beartype
def numToBinary(num: int):

    binary = f"{num:032b}"
    grouped = " ".join(binary[i:i+8] for i in range(0, len(binary), 8))

    return f'{grouped} ({num})'


def main():


    for n in test_cases:

        try:
            result = graycode(n)
            print(f'\n{WHITE}TEST_CASE = G({n}){RESET}\n')
            print(f'{BLUE}n    = {numToBinary(n)}{RESET}')
            print(f'{GREEN}G(n) = {numToBinary(result)}{RESET}')

            

        except ValueError as e:

            print(f"\n{WHITE}TEST_CASE = G({n}) {RESET}\n\n{RED}{e}{RESET}\n")

            


if __name__ == "__main__":
   main()

