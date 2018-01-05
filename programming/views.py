from django.shortcuts import render
from django.views import generic
from programming.helpers import (get_new_puzzle)
from programming import models as programming_models 

class GameSolutionCreateView(generic.CreateView):
    """ Class Based View to Handle Game to Database"""

    model = programming_models.GameSolution
    fields = ["solution_string"]
    template_name = "game_solution_template.html"

    def get_context_data(self, **kwargs):
        context = super(GameSolutionCreateView, self).get_context_data(**kwargs)
        # Retrieve the puzzle from ActivePuzzle object
        active_puzzle = models.ActivePuzzle.objects.filter(student=self.student).first()
        context["puzzle_string"] = active_puzzle.puzzle.puzzle_string
        context["difficulty"] = active_puzzle.puzzle.difficulty
        print(context["puzzle_string"])
        return context
