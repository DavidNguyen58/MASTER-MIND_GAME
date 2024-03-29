import itertools

from logic import *


def main():
    number_of_colours_to_use = int(
        input("Enter the the number of colours to use in the game: ")
    )

    colours = ["red", "blue", "yellow", "green"]
    colours = colours[0:number_of_colours_to_use]
    symbols = create_symbols(colours)

    KB = knowledge_base(colours)

    goal = player_1(colours)

    print("THE GAME STARTS NOW")
    print(
        f"You will need to correctly guess {len(colours)} of {colours}. Please put your guessing order in a line."
    )

    while True:
        guess = player_2(colours)
        r = compare_guess(guess, goal)
        if r == len(goal):
            result(goal, colours)
            print("That's the correct position")
            return
        else:
            # Update KnowledgeBase
            clauses = propositional_knowledege(guess, r)
            KB = update_knowledge_base(KB, clauses, r)
            for symbol in symbols:
                if model_check(KB, symbol):
                    print(symbol)


def create_symbols(colours):
    # Create a symbol for each colour
    symbols = [Symbol(f"{c}{i}") for i, c in enumerate(colours)]
    return symbols


def player_1(colours):
    # Set up the goal for the game
    print("The order of the colour")
    t = dict()
    for c in colours:
        t[c] = None
    n = len(colours)
    for i in range(n):
        x = input(f"{i} position: ")
        t[x] = f"{i}"
    a = []
    for key in t:
        tmp = key + t[key]
        a.append(tmp)
    return a


def player_2(colours):
    print("Make your guess")
    t = dict()
    for c in colours:
        t[c] = None
    n = len(colours)
    for i in range(n):
        x = input(f"{i} position: ")
        t[x] = f"{i}"
    a = []
    for key in t:
        tmp = key + t[key]
        a.append(tmp)
    return a


def compare_guess(guess, goal):
    # Take two lists of positions and compare it together
    counter = 0
    for i in range(len(guess)):
        if guess[i] == goal[i]:
            counter += 1
    return counter


def result(order, colours):
    for i in range(len(colours)):
        print(f"{colours[i]}{order[i]} ", end="")
    print()


def knowledge_base(colours):
    KB = And()
    for color in colours:
        KB.add(
            Or(
                Symbol(f"{color}0"),
                Symbol(f"{color}1"),
                Symbol(f"{color}2"),
                Symbol(f"{color}3"),
            )
        )
    # A colour only has 1 position
    for colour in colours:
        for i in range(len(colours)):
            for j in range(len(colours)):
                if i != j:
                    # e.g red1 -> not red0, not red2, not red3, ...
                    KB.add(
                        Implication(Symbol(f"{colour}{i}"), Not(Symbol(f"{colour}{j}")))
                    )

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


def propositional_knowledege(guess, correct):
    if correct == 0:
        return [guess]
    p = list(itertools.combinations(guess, correct))
    # Return the full set
    result = []
    for i in p:
        x = list(i)
        for j in guess:
            if j not in x:
                x.append(j)
        result.append(x)
    return result


def update_knowledge_base(KB, clauses, correct):
    if correct == 0:
        for var in clauses[0]:
            KB.add(Not(Symbol(var)))
        return KB
    new = Or()
    for clause in clauses:
        a = And()
        i = 0
        for var in clause:
            if i >= correct:
                a.add(Not(Symbol(var)))
            else:
                a.add(Symbol(var))
            i += 1
        new.add(a)
    KB.add(new)
    return KB


if __name__ == "__main__":
    main()
