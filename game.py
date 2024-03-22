import sys
import itertools
from logic import *

def main():
    if len(sys.argv) != 2:
        print("Usage: python game.py [N]")
        return 0
    
    try:
        val = int(sys.argv[1])
        if val < 4  or val > 6:
            print("Please enter an integer between 4 and 8")
    except:
        print("Please enter an integer")
        return
    
    colours = ["red", "blue", "green", "yellow", "black"]
    colours = tuple(colours[0: int(sys.argv[1])])
    order = player_1(colours)
    KB = knowledge_base(colours)
    print("THE GAME STARTS NOW")
    print(f"You will need to guess {val} colours. Please put your guessing order in a line")
    while True:
        guess = player_2()
        check = compare_guess(guess, order)
        if check == len(order):
            result(order, colours)
            print("That's the correct position")
            return
        else:
            # Update KnowledgeBase
            print(check)
            KB = update_KB(KB, guess, check)



def player_1():
    # Set up the goal for the game
    goal = input("Enter the order: ")
    goal = goal.strip().split()
    return goal


def knowledge_base(colours):
    # Create symbol for each colour
    symbols = []
    # Each colour has a position
    for i in range(len(colours)):
        for colour in colours:
            symbols.append(Symbol(f"{colour}{i}"))
    KB = And()
    # A colour only has 1 position
    for colour in colours:
        for i in range(len(colours)):
            for j in range(len(colours)):
                if i != j:
                    # e.g red1 -> not red0, red2, red3, ...
                    KB.add(Implication(Symbol(f"{colour}{i}"), Not(Symbol(f"{colour}{j}"))))

    # A position only has 1 colour
    for i in range(len(colours)):
        for c1 in colours:
            for c2 in colours:
                if c1 != c2:
                    # red1 -> not yellow1, green1 and so on
                    x = Symbol(f"{c1}{i}")
                    y = Not(Symbol(f"{c2}{i}"))
                    KB.add(Implication(x, y))
    return KB


def player_2():
    guess = input("Your guess: ")
    guess = guess.strip().split()
    return guess


def compare_guess(guess, order):
    # Take two lists of positions and compare it together
    counter = 0
    for i in range(len(guess)):
        if guess[i] == order[i]:
            counter += 1
    return counter
    

def result(order, colours):
    for i in range(len(colours)):
        print(f"{colours[i]}{order[i]} ", end="")
    print()


def update_KB(KB, guess, colours, check):
    # Update the knowledge_base
    ...

if __name__ == "__main__":
    main()