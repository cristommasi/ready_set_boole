import sys, os
from beartype  import beartype
sys.path.append(os.path.join(os.path.dirname(__file__), '../rsb_lib'))
from rsb_lib import COLOR, MAX, numToBinStr, map, reverse_map


def main():

	TEST_CASES = [
		[0, 0],
		[MAX.U16, MAX.U16],
		[1, 0],
		[0, 1],
		[2, 3],
		[3, 2]
	]

	for sets in TEST_CASES:


		try:
			x = sets[0]
			y = sets[1]
			resMAP = map(x, y)
			RESREVMAP = reverse_map(resMAP)
			print(f'{COLOR.WB}reverse_map({COLOR.RST}{COLOR.BB}map({x}, {y}) -> {resMAP}{COLOR.RST})\n')
			print(f'{COLOR.GB}{numToBinStr(RESREVMAP[0], 32)}{COLOR.RST}')
			print(f'{COLOR.GB}{numToBinStr(RESREVMAP[1], 32)}{COLOR.RST}\n')
			assert x == RESREVMAP[0] and y == RESREVMAP[1], f'{COLOR.RB} <-- expected [{x}, {y}]{COLOR.RST}'

		except AssertionError as e:
			
			print(e)


if __name__ == "__main__":
	main()