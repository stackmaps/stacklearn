from api import models as api_models
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from mathstack.helpers import compute_answer, get_next_q

import uuid


class BooleanQuestion(models.Model):
    """ A model for storing YES/NO math questions
    """
    OP_CHOICES = [("MODULUS", "%")]
    operand1 = models.IntegerField()
    operand2 = models.IntegerField()
    operator = models.CharField(choices=OP_CHOICES, max_length=2)
    correct_answer = models.BooleanField()

    def __str__(self):
        return "{} {} {} == 0".format(operand1, operator, operand2)


class BooleanAnswer(models.Model):
    """ A `BooleanAnswer` is a `Student`-created response to a YES/NO question.
    """
    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_answer = models.BooleanField()
    right_answer = models.BooleanField()
    was_correct = models.BooleanField()
    question = models.CharField(max_length=50)  # example: "10 % 2 == 0"

    def save(self, *args, **kwargs):
        # retrieve the current `ActiveQuestion` for this `Student`
        active_q = api_models.ActiveQuestion.objects.filter(student=self.student).first()
        q_text = active_q.q_text
        answer = compute_answer(q_text)
        if type(answer) is bool:
            self.right_answer = answer
        else:
            raise TypeError("Question-Answer type mismatch")
        self.question = q_text
        self.was_correct = (self.raw_answer == self.right_answer)
        active_q.question = get_next_q()
        active_q.save()
        super(BooleanAnswer, self).save(*args, **kwargs)

    def __str__(self):
        return "{} selected {}".format(self.student, self.raw_answer) 


class IntegerAnswer(models.Model):
    """ An `IntegerAnswer` is a `Student`-created response to a question.
    """
    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_answer = models.IntegerField()
    right_answer = models.IntegerField()
    was_correct = models.BooleanField()
    question = models.CharField(max_length=50)  # example: "4 * 8 =="

    def __str__(self):
        return "{} selected {}".format(self.student.username, self.raw_answer) 


@receiver(user_logged_in)
def populate_active_question(sender, user, request, **kwargs):
    next_q = get_next_q()
    # check for an existing `ActiveQuestion`
    try:
        q = api_models.ActiveQuestion.objects.filter(student=user.student).first()
    except ObjectDoesNotExist:
        # this is like an admin user, so we will do nothing
        is_student = False
    if is_student:
        if not q:
            q = api_models.ActiveQuestion.objects.create(
                student=user.student, q_text=next_q)
        else:
            q.q_text=next_q
            q.save()

@receiver(models.signals.post_save, sender=BooleanAnswer)
def update_active_question(sender, instance, created, **kwargs):
    if created:
        active_q = api_models.ActiveQuestion.objects.filter(student=instance.student).first()
        active_q.q_text = get_next_q()
        active_q.save()
