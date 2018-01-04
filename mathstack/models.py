from api import models as api_models
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from mathstack.helpers import compute_answer, get_next_q

import uuid


class Student(models.Model):
    """ A `Student` user can practice math skills.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return "{} (student)".format(self.user.username) 


class ActiveQuestion(models.Model):
    """ A `User` may have up to one `ActiveQuestion` object at a time.
    The `ActiveQuestion` will be deleted when an answer is submitted.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    q_text = models.CharField(max_length=50)  # post-processed by compute_answer()

    class Meta:
        unique_together = ("student", "q_text")

    def __str__(self):
        return "question for {} re: {}".format(
            self.student, self.q_text)


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
    # check for an existing `ActiveQuestion`
    q = ActiveQuestion.objects.filter(student__pk=request.user.student.pk).first()
    if not q:
        q = ActiveQuestion.objects.create(
            student_id=request.user.student.pk, q_text=get_next_q())
    else:
        q.q_text=get_next_q()
        q.save()

@receiver(models.signals.post_save, sender=BooleanAnswer)
def update_active_question(sender, instance, created, **kwargs):
    if created:
        active_q = ActiveQuestion.objects.filter(student=instance.student).first()
        active_q.q_text = get_next_q()
        active_q.save()
