""" /mathstack/views.py
"""
from braces.views import LoginRequiredMixin
from django.shortcuts import reverse, Http404
from django.views import generic
from mathstack import models as mathstack_models


class StudentOnlyMixin(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = super(StudentOnlyMixin, self).get_context_data(**kwargs)

        #if not hasattr(self.request.user, "student") or self.request.user.student is None:
         #   raise Http404()
        return context


class BoolAnswerCreateView(StudentOnlyMixin, generic.CreateView):  
    """ Class-based view to create answers to YES/NO questions.
    """
    model = mathstack_models.BooleanAnswer
    fields = ["raw_answer"]
    template_name = "mathstack/bool_answer_create.html"

    def get_context_data(self, **kwargs):
        context_data = super(BoolAnswerCreateView, self).get_context_data(**kwargs)
        # retrieve the question from `ActiveQuestion` object
        active_q = mathstack_models.ActiveQuestion.objects.filter(
            student=self.request.user.student).first()
        context_data["operand1"] = active_q.question.operand1
        context_data["divisor"] = active_q.question.operand2
        return context_data

    def form_valid(self, form):
        form.instance.student = self.request.user.student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('bool_answer_create')

