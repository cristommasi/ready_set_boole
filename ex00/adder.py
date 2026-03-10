from beartype import beartype

U32_MAX = 4294967295

@beartype
def adder(a: int, b: int) -> int:

    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0 or a > U32_MAX or b > U32_MAX:
        raise ValueError("Inputs must be 32bit unsigned integer and in range.")

    while b != 0:
        temp = a ^ b
        carry = (a & b) << 1
        a = temp & U32_MAX
        b = carry & U32_MAX
    return a

def main():


    x = adder(3, 3)

    b = f"{x:032b}"

    grouped = " ".join(b[i:i+8] for i in range(0, len(b), 8))

    print(f'{grouped} ({x})')


if __name__ == "__main__":
    main()