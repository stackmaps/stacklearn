from django.db import models
from api import models as api_models
from .helpers import get_new_puzzle

#TODO Add __str__ functions for each model

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
    def save(self, *args, **kwargs):
        """Besides the regular save(), also runs logic for 'checking solution_string' to evaluate 'correct'
        Also,
        """
        active_puzzle = models.ActivePuzzle.objects.filter(student=self.student).first()
        print("Saving")
        #TODO complete condition
        if True: # if logic evals to True 'correct' should be True (its default is False)
            self.correct = True
        #TODO create parser for num_of_steps perhaps should go in helpers.py
        self.num_of_steps=1 #currently hardcoded to 1, should be changed to a parser
        #if Student solves in less steps than us, update the least_steps attr of the GamePuzzle
        if self.num_of_steps < active_puzzle.puzzle.least_steps:
            active_puzzle.puzzle.least_steps = num_of_steps
            active_puzzle.puzzle.save(force_update=True) #can we update an object pulled from an already pulled query?

        active_puzzle.puzzle = get_new_puzzle()
        active_puzzle.save()
        super(GameSolution,self).save(*args,**kwargs)

#sourced from stacklearn.api
class ActivePuzzle(models.Model):
    """ A `User` may have up to one `ActivePuzzle` object at a time.
    The `ActivePuzzle` will be deleted when an answer is submitted.
    """
    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(GamePuzzle, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "puzzle")

    def __str__(self):
        return "puzzle for {} re: ".format(
            self.student.username, self.puzzle.puzzle_string)

@receiver(models.signals.post_save, sender=GameSolution)
def update_puzzle(sender,instance, created,**kwargs):
   """Fetches and Updates ActivePuzzle Object for a Student with a new GamePuzzle"""
    if created:
        print("updating puzzle please wait")
        active_puzzle = models.ActivePuzzle.objects.filter(student=self.student).first()
        active_puzzle.puzzle = get_new_puzzle()
        active_puzzle.save(force_update=True)
