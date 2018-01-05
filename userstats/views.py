""" /mathstack/views.py
"""

from django.shortcuts import render
from .models import StudentStatistic
from django.views import generic
from api import models as api_models


# Create your views here.

class UserStatsCreateView(generic.CreateView):  
    """ 
    Class-based view to display user statistics.
    Has `context_data["statset"]` as the set of all data for all subjects the current student has studied.
    Has `context_data["user"]` as the current logged in user.
    """

    model = StudentStatistic
    template_name = "userstats/userstats_display.html"
    fields = ["num_correct"]

    def get_context_data(self, **kwargs):
        context_data = super(UserStatsCreateView, self).get_context_data()
        context_data["statset"] = StudentStatistic.objects.filter(student=self.request.user.student).all()
        context_data["user"] = self.request.user
        # context_data["subjects"] = StudentStatistic.objects.values_list('subject', flat=True).filter(user=self.request.user)
        return context_data