import itertools

from logic import *


def main() -> None:
    number_of_colours_to_use = int(
        input("Enter the the number of colours to use in the game: ")
    )

    colours = ["red", "blue", "yellow", "green"]
    colours = colours[0:number_of_colours_to_use]
    symbols = create_symbols(colours)

    KB = create_knowledge_base(colours)

    # Set up the goal for the game
    print("The order of the colour")
    goal = get_player_colour_input(colours)

    print("THE GAME STARTS NOW")
    print(
        f"You will need to correctly guess {len(colours)} of {colours}. Please put your guessing order in a line."
    )

    while True:
        print("Make your guess")
        guess = get_player_colour_input(colours)
        number_of_correct_guesses = get_number_of_correct_guesses(guess, goal)
        if number_of_correct_guesses == len(goal):
            result(goal, colours)
            print("That's the correct position")
            return
        else:
            # Update KnowledgeBase
            clauses = propositional_knowledege(guess, number_of_correct_guesses)
            KB = update_knowledge_base(KB, clauses, number_of_correct_guesses)
            for symbol in symbols:
                if model_check(KB, symbol):
                    print(symbol)


def create_symbols(colours: list[str]) -> list[Symbol]:
    # Create a symbol for each colour
    symbols = [Symbol(f"{c}{i}") for i, c in enumerate(colours)]
    return symbols


def get_player_colour_input(colours: list[str]) -> list[str]:
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


def get_number_of_correct_guesses(guess: list[str], goal: list[str]) -> int:
    # Take two lists of positions and compare them together
    number_of_correct_guesses = 0

    for i in range(len(guess)):
        if guess[i] != goal[i]:
            continue

        number_of_correct_guesses += 1

    return number_of_correct_guesses


def result(order: list[str], colours: list[str]) -> None:
    for i in range(len(colours)):
        print(f"{colours[i]}{order[i]} ", end="")
    print()


def create_knowledge_base(colours: list[str]) -> And:
    clauses_to_add = []

    for colour in colours:
        clauses_to_add += [
            Or(
                Symbol(f"{colour}0"),
                Symbol(f"{colour}1"),
                Symbol(f"{colour}2"),
                Symbol(f"{colour}3"),
            )
        ]

        # Each colour has only 1 position
        # e.g red1 -> not red0, not red2, not red3, ...
        clauses_to_add += [
            Implication(Symbol(f"{colour}{i}"), Not(Symbol(f"{colour}{j}")))
            for i in range(len(colours))
            for j in range(len(colours))
            if i != j
        ]

    # Each position has only 1 colour
    # red1 -> not yellow1, green1 and so on
    clauses_to_add += [
        Implication(Symbol(f"{c1}{i}"), Not(Symbol(f"{c2}{i}")))
        for i in range(len(colours))
        for c1 in colours
        for c2 in colours
        if c1 != c2
    ]

    KB = And(*clauses_to_add)
    return KB


def propositional_knowledege(guess: list[str], correct: int) -> list[list[str]]:
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


def update_knowledge_base(
    KB: And, clauses: list[list[str]], number_of_correct_guesses: int
) -> And:
    disjunction = Or()

    for clause in clauses:
        symbols = [
            Not(Symbol(var)) if i >= number_of_correct_guesses else Symbol(var)
            for i, var in enumerate(clause)
        ]
        conjunction = And(*symbols)
        disjunction.add(conjunction)

    KB.add(disjunction)

    return KB


if __name__ == "__main__":
    main()
