import random

def get_new_puzzle():
    """fetches a new puzzle from the GamePuzzle Model, returns a puzzle object"""
    #currently hardcoded with a primary key between 0 and 10, will change to be scalable in the future
    puzzle = GamePuzzle.objects.get(id=ceil(random(0, 10)))

    return puzzle
