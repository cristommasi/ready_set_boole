
from adder import adder
from beartype import beartype

RESET   = "\033[0m"
RED     = "\033[31m"
GREEN   = "\033[32m"
BLUE    = "\033[34m"
WHITE   = "\033[1;37m"

U32_MAX = 4294967295
U64_MAX = 18446744073709551615

test_cases = [
    [25, 3], [0, 0], [15, 1], [1234, 5678], [1, 1], [7, 1], [15, 1], [255, 1], [65535, 1], #regular expressions with carry
    [U32_MAX, 0], [0, U32_MAX], [U32_MAX - 1, 1], [U32_MAX, 2], #should work and wrap up if exceeds limit
    [U64_MAX, 0], [-1, 5], [5, -1], [-2, -3], #will throw error
    [U32_MAX, 1]
]

@beartype
def numToBinary(num: int):

    binary = f"{num:032b}"
    grouped = " ".join(binary[i:i+8] for i in range(0, len(binary), 8))

    return f'{grouped} ({num})'


def main():


    for a, b in test_cases:

        expected = (a + b) & U32_MAX
        try:
            result = adder(a, b)

            print(f'\n{WHITE}TEST_CASE = [{a}, {b}]{RESET}\n')
            print(f'+ {numToBinary(a)}')
            print(f'  {numToBinary(b)}')
            print("--------------------------------------------------------")
            print(f'{BLUE}  {numToBinary(expected)}{RESET} - a + b')
            print(f'{GREEN}  {numToBinary(result)}{RESET} - adder(a, b)\n')

            assert result == expected, f"adder({a},{b}) = {result}, expected {expected}"
            

        except ValueError as e:

            print(f"{WHITE}TEST_CASE = [{a}, {b}] {RESET}\n\n{RED}{e}{RESET}\n")

            


if __name__ == "__main__":
   main()

