from beartype import beartype

class COLOR:
    RST   = "\033[0m"
    R     = "\033[31m"
    RB    = "\033[1;31m"
    G     = "\033[32m"
    GB    = "\033[1;32m"
    B     = "\033[34m"
    BB    = "\033[1;34m"
    W     = "\033[37m"
    WB    = "\033[1;37m"


class MAX:
    U32: int = 4294967295
    U64: int = 18446744073709551615


class AST:
     
    class Node:
        pass
    
    class ValueNode(Node):

        def __init__(self, value):
            self.value = value

    class UnaryNode(Node):

        def __init__(self, op, right):
            self.op = op
            self.right = right

    class BinaryNode(Node):

        def __init__(self, op, left, right):
            self.op = op
            self.left = left
            self.right = right

    def __init__(self, mode: str, allowed: str, formula: str):

        self.mode = mode
        self.allowed = allowed
        self.root = self.create(formula)
        self.formulaSet = sorted({c for c in formula if c.isupper()})
        self.formulaSetSize = len(self.formulaSet)
        self.valuesDict = {}

    def create(self, formula: str):
        stack = []

        for c in formula:

            if c not in self.allowed:
                raise ValueError(f"Error: Unknown Character: {c}")

            if self.mode == 'VARS' and c.isupper():
                stack.append(self.ValueNode(c))

            elif self.mode == 'CONST' and c == '0' or c == '1':
                stack.append(self.ValueNode(int(c)))

            elif c == '!':
                if not stack:
                    raise ValueError(f"Error: Malformed formula: {formula}")
                right = stack.pop()
                stack.append(self.UnaryNode(c, right))

            else:
                if len(stack) < 2:
                    raise ValueError(f"Error: Malformed formula: {formula}")
                right = stack.pop()
                left = stack.pop()
                stack.append(self.BinaryNode(c, left, right))

        if len(stack) != 1:
            raise ValueError(f"Error: Malformed formula: {formula}")

        return stack[0]
    
    def assignValues(self, bValue: int):

        for i, c in enumerate(self.formulaSet):
            self.valuesDict[c] = (bValue >> (self.formulaSetSize - 1 - i)) & 1

    def eval(self, node = None):

        if isinstance(node, self.ValueNode):
            return self.valuesDict[node.value]

        if isinstance(node, self.UnaryNode):
            return int(not self.eval(node.right))

        if isinstance(node, self.BinaryNode):

            left = self.eval(node.left)
            right = self.eval(node.right)

            if node.op == '&': return left & right

            if node.op == '|': return left | right

            if node.op == '^': return left ^ right

            if node.op == '>': return int((not left) | right)

            if node.op == '=': return int(left == right)

        raise ValueError("Unknown node type")

    def toNNF(self, node = None):


        if node is None: node = self.root

        if isinstance(node, self.ValueNode): return node

        if node.op == '=': # Equivalence (A ⇔ B) ⇔ ((A ⇒ B) ∧ (B ⇒ A))


            left = self.toNNF(node.left)
            right = self.toNNF(node.right)
            new_node = self.BinaryNode('&', self.BinaryNode('>', left, right), self.BinaryNode('>', right, left))
            return self.toNNF(new_node)

        
        if node.op == '>': # Material Condition (A ⇒ B) ⇔ (¬A ∨ B)


            left = self.toNNF(node.left)
            right = self.toNNF(node.right)
            new_node = self.BinaryNode('|', self.UnaryNode('!', left), right)
            return self.toNNF(new_node)

        if node.op == '!':

            child = node.right

            if isinstance(child, self.ValueNode): return node
            
            
            if child.op == '!': # Elimination of double negation (¬¬A) ⇔ A 

                return self.toNNF(child.right)
            
            
            if child.op == '&': # De Morgan’s law  ¬(A ∧ B) ⇔ (¬A ∨ ¬B)

                new_structure = self.BinaryNode('|', self.UnaryNode('!', child.left), self.UnaryNode('!', child.right))
                return self.toNNF(new_structure)
            

            if child.op == '|': # De Morgan’s law ¬(A ∨ B) ⇔ (¬A ∧ ¬B)

                new_structure = self.BinaryNode('&', self.UnaryNode('!', child.left), self.UnaryNode('!', child.right))
                return self.toNNF(new_structure)
            

            return self.toNNF(self.UnaryNode('!', self.toNNF(child)))

        # Continue down
        if node.op == '|' or node.op == '&':

            return self.BinaryNode(node.op, self.toNNF(node.left), self.toNNF(node.right))
            
        
        raise ValueError("Unknown node type")

    def toRPN(self, node):

        if isinstance(node, self.ValueNode):
            return str(node.value)
        
        if isinstance(node, self.UnaryNode):
            return self.toRPN(node.right) + '!'
        
        if isinstance(node, self.BinaryNode):
            return self.toRPN(node.left) + self.toRPN(node.right) + node.op
        
        raise ValueError(f"Unknown node type in toRPN: {type(node)}")


    @beartype
    @staticmethod
    def print_truth_table(self, formula: str) -> None:

        if not isinstance(formula, str):
            raise ValueError("Inputs must be string")


        header = ' | '.join(self.formulaSet) + ' | ='
        separator = '|'.join(['---'] * (self.formulaSetSize + 1))
        print(f"| {header} |")
        print(f"|{separator}|")

        for i in range(2 ** self.formulaSetSize):

            self.assignValues(i)
            value = self.eval(self.root)
            row = ' | '.join(str(self.valuesDict[c]) for c in self.formulaSet)
            print(f"| {row} | {value} |")


@beartype
def numToBinStr(num: int, bytes: int) -> str:

    binary = f"{num:0{bytes}b}"
    grouped = " ".join(binary[i:i+8] for i in range(0, len(binary), 8))

    return f'{grouped} ({num})'


@beartype
def adder(a: int, b: int) -> int:

    if not isinstance(a, int) or not isinstance(b, int) or a < 0 or b < 0 or a > MAX.U32 or b > MAX.U32:
        raise ValueError("Inputs must be 32bit unsigned integer and in range.")
    
    while b != 0:
        carry = ((a & b) << 1) & MAX.U32
        a = (a ^ b) & MAX.U32
        b = carry
        
    return a & MAX.U32


