from django.db import models
from django.conf import settings
from api import models as api_models
import uuid
import api.models as api_models

# Create your models here.

class StudentStatistic(models.Model):
    MATH = "Mathematics"
    PROGRAMMING = "Programming"
    SUBJECTS = (
        (MATH, 'Math'),
        (PROGRAMMING, 'Programming')
    )

    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    subject = models.CharField(choices=SUBJECTS, max_length=30)
    num_correct = models.IntegerField(default=uuid.uuid4)
    num_incorrect = models.IntegerField(default=uuid.uuid4)

    def percent_correct(self):
        return str(float(self.num_correct) / max([self.num_correct + self.num_incorrect, 1]) * 100) + "%"