"""  /mathstack/models.py
    Data models for the mathstack app.
"""

from django.conf import settings
from django.db import models
from django.urls import reverse

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


class BooleanAnswer(models.Model):
    """ A `BooleanAnswer` is a `Student`-created response to a YES/NO question.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_answer = models.BooleanField()
    right_answer = models.BooleanField()
    was_correct = models.BooleanField()
    question = models.CharField(max_length=50)

    def __str__(self):
        return "{} selected {}".format(self.student.username, self.raw_answer) 


class IntegerAnswer(models.Model):
    """ An `IntegerAnswer` is a `Student`-created response to a question.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_answer = models.IntegerField()
    right_answer = models.IntegerField()
    was_correct = models.BooleanField()
    question = models.CharField(max_length=50)

    def __str__(self):
        return "{} selected {}".format(self.student.username, self.raw_answer) 
