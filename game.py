# FRONT_END 

colours = ["red", "blue", "green", "yellow"]
# Player 1 can set a goal
def main():
    # Prompt the user 1 to put colour order for player 2 to guess
    player_1 = colour_order()
    start()

def colour_order():
    # Prompt the player 1 to insert a correct order of the colours
    # The function should return a list of object in the form of color{position}. e.g red0
    raise NotImplementedError

def start():
    # Generate a title showing that the game is starting now and prompt the second player to play
    raise NotImplementedError

# Player 2 will need to find out the correct order in the minimum of move with the support of A.I
