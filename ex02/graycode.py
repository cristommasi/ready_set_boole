from beartype import beartype

U32_MAX = 0xFFFFFFFF

@beartype
def graycode(n: int) -> int:

    if not isinstance(n, int) or n < 0 or n > U32_MAX:
        raise ValueError("Inputs must be 32bit unsigned integer and in range.")
    
    return (n ^(n >> 1)) & U32_MAX