# api/models.py

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



class Question(models.Model):
    """ A model for storing YES/NO math questions
    """
    BOOLEAN = 0
    INTEGER = 1
    MULTIPLE_CHOICE = 2

    QUESTION_TYPES = (
        (BOOLEAN, 'Boolean'),
        (INTEGER, 'Integer'),
        (MULTIPLE_CHOICE, 'Multiple Choice')
    )

    question_type = models.PositiveSmallIntegerField(choices=QUESTION_TYPES)
    correct_answer = JSONField()
    question_data = JSONField()

    def save(self, *args, **kwargs):
        # TODO: generalize this to work with any type of question
        # self.correct_answer = self.compute_answer()
        super(BooleanQuestion, self).save(*args, **kwargs)


class ActiveQuestion(models.Model):
    """ A `User` may have up to one `ActiveQuestion` object at a time.
    The `ActiveQuestion` will be deleted when an answer is submitted.
    """
    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "question")

    def __str__(self):
        return "question for {} re: {}".format(
            self.student, self.question)


class Answer(models.Model):
    """ A `BooleanAnswer` is a `Student`-created response to a YES/NO question.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    answer = JSONField()
    was_correct = models.BooleanField()

    def save(self, *args, **kwargs):
        # retrieve the current `ActiveQuestion` for this `Student`
        active_q = ActiveQuestion.objects.filter(student=self.student).first()
        self.question = active_q.question
        # TODO: generalize answer validation
        self.was_correct = (self.answer == self.question.correct_answer)
        # TODO: generalize this to work with any type of question
        # active_q.question = BooleanQuestion.generate_question()
        # active_q.save()
        super(Answer, self).save(*args, **kwargs)

    def __str__(self):
        return "{} selected {}".format(self.student, self.raw_answer) 


@receiver(user_logged_in)
def populate_active_question(sender, user, request, **kwargs):
    if hasattr(user, 'student'):
        # check for an existing `ActiveQuestion`
        q = ActiveQuestion.objects.filter(student=user.student).first()
        if not q:
            # TODO: generalize this to work with any type of question
            #ActiveQuestion.objects.create(
            #   student=user.student, question=BooleanQuestion.generate_question())


# adds an authtoken to all new users
models.signals.post_save.connect(create_auth_token, sender=settings.AUTH_USER_MODEL)
