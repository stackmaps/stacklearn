""" /mathstack/views.py
"""
from braces.views import LoginRequiredMixin
from django.shortcuts import render, reverse
from django.views import generic
from mathstack.helpers import (
    compute_answer, get_divisor, get_next_q, parse_question
    )
from mathstack import models as mathstack_models
import random


class StudentOnlyMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(StudentOnlyMixin, self).get_context_data(**kwargs)

        if not hasattr(self.request.user, "student") or self.request.user.student is None:
            raise Http404()
        return context


class BoolAnswerCreateView(StudentOnlyMixin, generic.CreateView):  
    """ Class-based view to create answers to YES/NO questions.
    """
    model = mathstack_models.BooleanAnswer
    fields = ["raw_answer"]
    template_name = "mathstack/bool_answer_create.html"
    #context_object_name

    def get_context_data(self, **kwargs):
        context_data = super(BoolAnswerCreateView, self).get_context_data(**kwargs)
        print("THE KEYS ARE:")
        print(context_data.keys())
        # retrieve the question from `ActiveQuestion` object
        active_q = mathstack_models.ActiveQuestion.objects.filter(
            student=self.request.user).first()
        q_text = active_q.q_text  # fails if no object found
        q_dict = parse_question(q_text)
        context_data["operand1"] = q_dict["operand1"]
        context_data["divisor"] = q_dict["divisor"]
        return context_data




