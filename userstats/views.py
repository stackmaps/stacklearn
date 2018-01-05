""" /mathstack/views.py
"""

from django.shortcuts import render
from django.views import generic
from api import models as api_models
from mathstack.models import IntegerAnswer
from mathstack.models import BooleanAnswer


# Create your views here.

class UserStatsCreateView(generic.CreateView):  
    """ 
    Class-based view to display user statistics.
    Has `context_data["statset"]` as the set of all data for all subjects the current student has studied.
    Has `context_data["user"]` as the current logged in user.
    """

    model = IntegerAnswer
    template_name = "userstats/userstats_display.html"
    fields = ["was_correct"]

    def get_context_data(self, **kwargs):
        context_data = super(UserStatsCreateView, self).get_context_data()
        context_data["user"] = self.request.user

        int_answers = IntegerAnswer.objects.filter(student=self.request.user.student)
        correct_ints = len(int_answers.filter(was_correct=True).all())
        incorrect_ints = len(int_answers.filter(was_correct=False).all())
        context_data["correct_ints"] = correct_ints
        context_data["incorrect_ints"] = incorrect_ints
        context_data["percentage"] = (correct_ints / (incorrect_ints + correct_ints)) * 100

        # context_data["subjects"] = StudentStatistic.objects.values_list('subject', flat=True).filter(user=self.request.user)
        return context_data