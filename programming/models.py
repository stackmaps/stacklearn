from django.db import models
from api import models as api_models


# Create your models here.
class GamePuzzle (models.Model):
    """This object stores its difficulty, the least amount of steps that any user has been able to solve it in so far, and the puzzle itself as a string which can be parsed and rendered in a readable fashion on the client side.  The least amount of steps will be checked every time a solution for the puzzle is updated or added by the client.
    """
    difficulty = models.IntegerField()
    least_steps = models.IntegerField(default=2147483647)
    # TODO the vast majority of puzzles will be much smaller, but a few will be about this large (the most difficult ones).  We need to figure out if storing the small puzzles will take the same 5 mB (5000000 characters) as the large numbers (with most of that storage allocated but empty).  If that is the case then we need to figure out a better way to do this.
    puzzle_string = models.CharField(max_length=5000000)


class GameSolution (models.Model):
    """This object stores the number of steps it contains (the amount of blocks used by the user in its creation), wether or not it solves the puzzle it is meant to solve, the solution itself as a string, the user who created the solution, and the puzzle the solution refers to.  When the client creates or updates a GameSolution, the views.py will check if the solution solves the puzzle and if it has less steps than the current smallest solution.
    """
    num_of_steps = models.IntegerField()
    correct = models.BooleanField(default=False)
    solution_string = models.CharField(max_length=5000000)  # same TODO as line 11
    creator = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(GamePuzzle, on_delete=models.CASCADE)
