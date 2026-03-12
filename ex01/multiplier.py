from beartype import beartype

U32_MAX = 0xFFFFFFFF

@beartype
def multiplier(a: int, b: int) -> int:
    
    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0 or a > U32_MAX or b > U32_MAX:
        raise ValueError("Inputs must be 32bit unsigned integer and in range.")
    
    RES = 0
    while b != 0:

        if b & 1:
            RES = adder(RES, a)
            
        a = (a << 1) & U32_MAX
        b = b >> 1

    return RES & U32_MAX


@beartype
def adder(a: int, b: int) -> int:

    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0 or a > U32_MAX or b > U32_MAX:
        raise ValueError("Inputs must be 32bit unsigned integer and in range.")
    
    while b != 0:
        
        carry = ((a & b) << 1) & U32_MAX
        a = (a ^ b) & U32_MAX
        b = carry

    return a & U32_MAX

