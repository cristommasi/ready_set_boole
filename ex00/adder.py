from beartype import beartype

U32_MAX = 4294967295

@beartype
def adder(a: int, b: int) -> int:

    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0 or a > U32_MAX or b > U32_MAX:
        raise ValueError("Inputs must be 32bit unsigned integer and in range.")
    
    while b != 0:
        carry = ((a & b) << 1) & U32_MAX
        a = (a ^ b) & U32_MAX
        b = carry
    return a

def main():

    test = [127, 1]
    x = adder(test[0], test[1])
    y = test[0] + test[1]
    print(f'a + b       = {x}\nadder(a, b) = {x}')


if __name__ == "__main__":
    main()