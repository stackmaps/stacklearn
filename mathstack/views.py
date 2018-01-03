from django.shortcuts import render, reverse
from django.views import generic
from mathstack import models as mathstack_models

class BoolAnswerCreateView(generic.CreateView):  
    """ Class-based view to create answers to YES/NO questions.
    """
    model = mathstack_models.BooleanAnswer
    fields = ["raw_answer"]
    template_name = "mathstack/bool_answer_create.html"
    #context_object_name

    def get_context_data(self, **kwargs):
    	context_data = super(BoolAnswerCreateView, self).get_context_data()
    	context_data["operand1"] = 10
    	return context_data
