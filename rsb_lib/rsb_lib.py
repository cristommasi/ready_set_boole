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
	U16: int = 65535
	U32: int = 4294967295
	U64: int = 18446744073709551615


@beartype
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

	def __init__(self, allowed: str, formula: str):

		self.allowed = allowed
		self.root = self.create(formula)
		self.formulaSet = sorted({c for c in formula if c.isupper() or c == '1' or c == '0'})
		self.formulaSetSize = len(self.formulaSet)
		self.valuesDict = {}
		self.universalSet: set[int] = set()

	def create(self, formula: str) -> Node:
		stack = []

		for c in formula:

			if c not in self.allowed:
				raise ValueError(f"Error: Unknown Character: {c}")

			if c.isupper() or c == '0' or c == '1':
				stack.append(self.ValueNode(c))

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
	
	def assignValues(self, bValue: int) -> None:

		for i, c in enumerate(self.formulaSet):
			self.valuesDict[c] = (bValue >> (self.formulaSetSize - 1 - i)) & 1

	def eval(self, node: Node = None) -> int:

		if node is None: node = self.root

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

	def equivalence(self, left: Node, right: Node) -> Node: 

		new_left = self.BinaryNode('>', left, right)
		new_right = self.BinaryNode('>', right, left)
		return self.BinaryNode('&', new_left, new_right)
	
	def xorDecompositionCNF(self, left: Node, right: Node) -> Node: 

		new_left = self.BinaryNode('|', left, right)
		new_right = self.BinaryNode('|', self.UnaryNode('!', left), self.UnaryNode('!', right))
		return self.BinaryNode('&', new_left, new_right)

	def xorDecompositionDNF(self, left: Node, right: Node) -> Node: 

		new_left = self.BinaryNode('&', self.UnaryNode('!', left), right)
		new_right = self.BinaryNode('&', left, self.UnaryNode('!', right))
		return self.BinaryNode('|', new_left, new_right)

	def materialCondition(self, left: Node, right: Node) -> Node: 

		new_left = self.UnaryNode('!', left)
		return self.BinaryNode('|', new_left, right)
	
	def deMorgansDNF(self, left: Node, right: Node) -> Node:
		
		new_left = self.UnaryNode('!', left)
		new_right = self.UnaryNode('!', right)
		return self.BinaryNode('|', new_left, new_right)

	def deMorgansCNF(self, left: Node, right: Node) -> Node:

		new_left = self.UnaryNode('!', left)
		new_right = self.UnaryNode('!', right)
		return self.BinaryNode('&', new_left, new_right)

	def distributivity(self, left: Node, right: Node) -> Node:

		if isinstance(left, self.BinaryNode) and left.op == '&': # (A & B) | C  →  (A | C) & (B | C)

			return self.BinaryNode('&', self.distributivity(left.left, right), self.distributivity(left.right, right))

		if isinstance(right, self.BinaryNode) and right.op == '&': # A | (B & C)  →  (A | B) & (A | C)

			return self.BinaryNode('&', self.distributivity(left, right.left), self.distributivity(left, right.right))

		return self.BinaryNode('|', left, right)
	
	def toRPN(self, node: Node = None) -> str:

		if node is None: node = self.root

		if isinstance(node, self.ValueNode):
			return str(node.value)
		
		if isinstance(node, self.UnaryNode):
			return self.toRPN(node.right) + '!'
		
		if isinstance(node, self.BinaryNode):
			return self.toRPN(node.left) + self.toRPN(node.right) + node.op
		
		raise ValueError(f"Unknown node type in toRPN: {type(node)}")

	def flatten(self, node: Node, op: str) -> list[Node]:
	
		if isinstance(node, AST.BinaryNode) and node.op == op:
			return self.flatten(node.left, op) + self.flatten(node.right, op)
	
		return [node]
	
	def CNFtoRPN(self, node: Node = None) -> str:
	
		if node is None: node = self.root

		if isinstance(node, AST.ValueNode):
			return str(node.value)
	
		if isinstance(node, AST.UnaryNode):
			return self.CNFtoRPN(node.right) + '!'
	
		if isinstance(node, AST.BinaryNode):
		
			leaves = self.flatten(node, node.op)
			result = ''.join(self.CNFtoRPN(leaf) for leaf in leaves)
			result += node.op * (len(leaves) - 1)
			return result
	
		raise ValueError(f"Unknown node type in toRPNFlatten: {type(node)}")

	def toNNF(self, node: Node = None) -> Node:

		if node is None: node = self.root

		if isinstance(node, self.ValueNode): return node

		if node.op == '^': # Exclusive Disjunction Decomposition CNF (A ⊕ B) ⇔ (A ∨ B) ∧ (¬A ∨ ¬B)

			return self.toNNF(self.xorDecompositionCNF(self.toNNF(node.left), self.toNNF(node.right)))


		if node.op == '=': # Equivalence (A ⇔ B) ⇔ ((A ⇒ B) ∧ (B ⇒ A))

			return self.toNNF(self.equivalence(self.toNNF(node.left), self.toNNF(node.right)))

		
		if node.op == '>': # Material Condition (A ⇒ B) ⇔ (¬A ∨ B)

			return self.toNNF(self.materialCondition(self.toNNF(node.left), self.toNNF(node.right)))

		if node.op == '!':

			child = node.right

			if isinstance(child, self.ValueNode): return node
			
			
			if child.op == '!': # Elimination of double negation (¬¬A) ⇔ A 

				return self.toNNF(child.right)
			
			
			if child.op == '&': # De Morgan’s law  ¬(A ∧ B) ⇔ (¬A ∨ ¬B)

				return self.toNNF(self.deMorgansDNF(child.left, child.right))
			

			if child.op == '|': # De Morgan’s law ¬(A ∨ B) ⇔ (¬A ∧ ¬B)

				return self.toNNF(self.deMorgansCNF(child.left, child.right))
			

			return self.toNNF(self.UnaryNode('!', self.toNNF(child)))

		# Continue down
		if node.op == '|' or node.op == '&':

			return self.BinaryNode(node.op, self.toNNF(node.left), self.toNNF(node.right))
			
		
		raise ValueError("Unknown node type")

	def toCNF(self, node: Node = None) -> Node:

		if node is None: node = self.root

		if isinstance(node, self.ValueNode): return node

		if isinstance(node, self.UnaryNode): return node

		if node.op == '&':

			return self.BinaryNode('&', self.toCNF(node.left), self.toCNF(node.right))

		if node.op == '|':

			left  = self.toCNF(node.left)
			right = self.toCNF(node.right)
			return self.distributivity(left, right)

		raise ValueError(f"Unexpected operand in toCNF: {node.op}")

	def assignSetValues(self, sets: list[set[int]]):

		if len(sets) != self.formulaSetSize:
			raise ValueError(f'Malformed sets')
		
		for i, s in enumerate(self.formulaSet):
			self.valuesDict[s] = sets[i]
	
	def assignUniversalSet(self, sets: list[set[int]]):

		for s in sets:
			for elem in s:
				self.universalSet.add(elem)

	def evalS(self, node: Node = None) -> set[int]:
		
		if node is None: node = self.root

		if isinstance(node, self.ValueNode):
			return self.valuesDict[node.value]

		if isinstance(node, self.UnaryNode):
			return self.universalSet - self.evalS(node.right)

		if isinstance(node, self.BinaryNode):

			leftSet = self.evalS(node.left)
			rightSet = self.evalS(node.right)

			if node.op == '|': 
				return leftSet | rightSet

			if node.op == '&':
				return leftSet & rightSet
			
			if node.op == '^':
				return (leftSet - rightSet) | (rightSet - leftSet)
			
			
		raise ValueError("Unknown node type")


@beartype
def numToBinStr(num: int, bytes: int) -> str:

	binary = f"{num:0{bytes}b}"
	grouped = " ".join(binary[i:i+8] for i in range(0, len(binary), 8))

	return f'{grouped} ({num})'

@beartype
def adder(a: int, b: int) -> int:

	if a < 0 or b < 0 or a > MAX.U32 or b > MAX.U32:
		raise ValueError("Inputs must be 32bit unsigned integer and in range.")
	
	while b != 0:
		carry = ((a & b) << 1) & MAX.U32
		a = (a ^ b) & MAX.U32
		b = carry
		
	return a & MAX.U32

@beartype
def multiplier(a: int, b: int) -> int:
	
	if a < 0 or b < 0 or a > MAX.U32 or b > MAX.U32:
		raise ValueError("Inputs must be 32bit unsigned integer and in range.")
	
	RES = 0
	while b != 0:

		if b & 1:
			RES = adder(RES, a)
			
		a = (a << 1) & MAX.U32
		b = b >> 1

	return RES & MAX.U32

@beartype
def graycode(n: int) -> int:

	if n < 0 or n > MAX.U32:
		raise ValueError("Inputs must be 32bit unsigned integer and in range.")
	
	return (n ^(n >> 1)) & MAX.U32

@beartype
def eval_formula(formula: str) -> bool:

	if not formula:
		raise ValueError("Formula cannot be empty")

	ast_tree = AST("01!|&^>=", formula)
	ast_tree.valuesDict = {"0": 0, "1": 1}
			
	return bool(ast_tree.eval(ast_tree.root))

@beartype
def print_truth_table(formula: str) -> None:

	if not isinstance(formula, str):
		raise ValueError("Inputs must be string")
	
	ast_tree = AST("ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)

	header = ' | '.join(ast_tree.formulaSet) + ' | ='
	separator = '|'.join(['---'] * (ast_tree.formulaSetSize + 1))
	print(f"| {header} |")
	print(f"|{separator}|")

	for i in range(2 ** ast_tree.formulaSetSize):
		
		ast_tree.assignValues(i)
		value = ast_tree.eval(ast_tree.root)
		row = ' | '.join(str(ast_tree.valuesDict[c]) for c in ast_tree.formulaSet)
		print(f"| {row} | {value} |")

@beartype
def negation_normal_form(formula: str) -> str:

	if not formula:
		raise ValueError("Formula cannot be empty")
	
	
	ast_tree = AST("ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)
	ast_tree.root = ast_tree.toNNF(ast_tree.root)
	return ast_tree.toRPN(ast_tree.root)

@beartype
def conjunctive_normal_form(formula: str) -> str:

	if not formula:
		raise ValueError("Formula cannot be empty")
	
	ast_tree = AST("ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)
	ast_tree.root = ast_tree.toNNF(ast_tree.root)
	ast_tree.root = ast_tree.toCNF(ast_tree.root)
	return ast_tree.CNFtoRPN(ast_tree.root)

@beartype
def sat(formula: str) -> bool:

	if not formula:
		raise ValueError("Formula cannot be empty")
	
	ast_tree = AST("ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)
	for i in range(2 ** ast_tree.formulaSetSize):

		ast_tree.assignValues(i)
		value = ast_tree.eval(ast_tree.root)
		if value == True:
			return True
	return False

@beartype
def powerset(s: set[int]) -> list[set[int]]:

	s = list(s)

	for c in s:
		if c < 0 or c > MAX.U32:
			raise ValueError("Inputs in sets must be 32bit unsigned integer and in range.")
	
	cardinal = len(s)
	powersets: list[set[int]] = []

	for bit in range(1 << cardinal):

		new_set: set[int] = set()
		for j in range(cardinal):

			if (bit >> j) & 1:
				new_set.add(s[j])
				
		powersets.append(new_set)

	return powersets

@beartype
def eval_set(formula: str, sets: list[set[int]]) -> set[int]:

	if not formula:
		raise ValueError("Formula cannot be empty")
	if not sets:
		raise ValueError("Sets cannot be empty")

	
	ast_tree = AST("ABCDEFGHIJKLMNOPQRSTUVWXYZ!|&^>=", formula)
	ast_tree.root = ast_tree.toNNF(ast_tree.root)
	ast_tree.root = ast_tree.toCNF(ast_tree.root)
	ast_tree.assignSetValues(sets)
	ast_tree.assignUniversalSet(sets)
	return ast_tree.evalS(ast_tree.root)

@beartype
def map(x: int, y: int) -> float:

	if x < 0 or x > MAX.U16 or y < 0 or y > MAX.U16:
		raise ValueError("Inputs must be in 16bit unsigned integer range.")
	
	combined = 0
	for i in range(16):
		combined |= (((x >> i) & 1) << (2 * i))
		combined |= ((y >> i) & 1) << (2 * i + 1)

	return combined / MAX.U32

@beartype
def reverse_map(n: float) -> tuple[int, int]:

	converted: int = int(n * MAX.U32)

	x = 0
	y = 0
	for i in range(16):
		x |= ((converted >> (2 * i)) & 1) << i
		y |= ((converted >> (2 * i + 1)) & 1) << i

	return (x, y)

