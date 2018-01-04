from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from mathstack.helpers import compute_answer, get_next_q
from api import models as api_models

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
        print("LOGGING AN ANSWER OBJECT....")
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
        return "{} selected {}".format(self.student.username, self.raw_answer) 


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

@receiver(models.signals.post_save, sender=BooleanAnswer)
def update_active_question(sender, instance, created, **kwargs):
    if created:
        print("NOW UPDATING THE ACTIVE QUESTION....")
        active_q = ActiveQuestion.objects.filter(student=self.student).first()
        active_q.q_text = get_next_q()
        active_q.save()
