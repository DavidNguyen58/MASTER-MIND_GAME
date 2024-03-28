# Demonstrating how to use the predefined model
from logic import *

# Intializing all the symbols we need to use
A = Symbol("Red is the colour")
B = Symbol("Yellow is the colour")

# The knowledge will store all the information we know about the problem
knowledge = And()
knowledge.add(A)
knowledge.add(B)

# The model checking algorithm will check for entailment. In this case, KB ⊨ B, so it will print out in the terminal the message.
if model_check(knowledge, A):
    print(A)