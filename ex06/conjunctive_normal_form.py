import beartype from beartype
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))
from utils import COLOR, AST



def conjunctive_normal_form(formula: str) -> str:
