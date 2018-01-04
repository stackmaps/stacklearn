from django.conf import settings
from django.db import models
from django.dispatch import receiver

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
