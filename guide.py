from logic import *
# Demonstrating how to use the predefined model

# Intializing all the symbols we need to use
A = Symbol("Red is the colour")
B = Symbol("Yellow is the colour")

# Create a knowledge base. What we know to be True
# In this particular example, if we know that we have Red colour, and A implies B then surely we will have B.
knowledge = And(
    A,
    Implication(A, B)
)


knowledge.add(Implication(B, A))
# The model checking algorithm will check for entailment.
# In this case, KB ⊨ B, so it will print out in the terminal the message.
if model_check(knowledge, B):
    print(B)