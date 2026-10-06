# Ready Set Boole

Ready Set Boole is a collection of exercises around **Boolean algebra, bitwise operations, and logic formulas**.

The project started as a series of exercises, but I ended up building some of the logic from scratch to better understand what is happening underneath the higher-level operations.

## What is included

### Boolean Logic

The project includes a small formula engine capable of working with operators such as:

```text
!   NOT
&   AND
|   OR
^   XOR
>   IMPLIES
=   EQUIVALENCE
```

The input formulas use **Reverse Polish Notation (RPN)**.

For example:

```text
AB|
```

represents:

```text
A OR B
```

Formulas are parsed into an **AST (Abstract Syntax Tree)** and can then be evaluated with different variable assignments.

### Truth Tables

Given a Boolean formula, the project can generate its truth table by trying every possible combination of variable values.

```text
| A | B | = |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |
```

There is also a simple SAT check that evaluates all possible combinations to determine whether a formula can be satisfied.

## Normal Forms

The project implements transformations into:

* **NNF** — Negation Normal Form
* **CNF** — Conjunctive Normal Form
* **DNF** — Disjunctive Normal Form

It includes conversions such as:

* XOR → CNF / DNF
* Material implication → OR form
* Equivalence → conjunction of implications
* De Morgan's laws
* Double negation
* Distributivity

The transformations are performed directly on the AST rather than relying on an external library.

## Bitwise operations

There are also several exercises focused on working with integers at the bit level.

For example, addition and multiplication are implemented using bitwise operations rather than simply using `+` and `*`.

```python
def adder(a, b):
    while b != 0:
        carry = ((a & b) << 1)
        a = a ^ b
        b = carry

    return a
```

There is also an implementation of:

* Gray code
* Binary representation
* Bit manipulation
* 32-bit unsigned integer operations


## What I got from it

The main purpose of the project was to get more comfortable with **Boolean algebra and bit-level operations**, but the AST implementation also gave me a chance to work with parsing, recursive tree traversal, and transforming expressions programmatically.

It is a collection of exercises rather than a polished library, but it was a good way of getting a better understanding of how Boolean expressions and bits can be represented and manipulated programmatically.
