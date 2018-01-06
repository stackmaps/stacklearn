import random

from api import models as api_models
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver


class BooleanQuestion(models.Model):
    """ A model for storing YES/NO math questions
    """
    MODULUS = "MODULUS"
    OP_CHOICES = [(MODULUS, "%")]
    operand1 = models.IntegerField()
    operand2 = models.IntegerField()
    operator = models.CharField(choices=OP_CHOICES, max_length=20)
    correct_answer = models.BooleanField()

    def __str__(self):
        return "{} {} {} == 0".format(self.operand1, self.operator, self.operand2)

    def save(self, *args, **kwargs):
        self.correct_answer = self.compute_answer()
        super(BooleanQuestion, self).save(*args, **kwargs)

    def compute_answer(self):
        """ Method to ingest the raw text of a question, e.g., "10 % 2 == 0",
        and return the right answer.  Raises a `RuntimeError` if an unknown
        question format is encountered.
        Expected question types are divisibility and multiplication questions.
        """
        if self.operator == BooleanQuestion.MODULUS:
            return self.operand1 % self.operand2 == 0  # returns a Boolean
        else:
            raise RuntimeError("Unknown question operator '{}'.".format(self.operator))

    @staticmethod
    def get_divisor():
        DIVISORS = [2, 3, 4, 5, 6, 9]
        return random.choice(DIVISORS)

    @staticmethod
    def generate_question():
        """ Method to generate a random math question and update the ActiveQuestion accordingly.
        Presently generates divisibility questions only.
        """
        LOWER = 10
        UPPER = 5000
        op1 = random.randint(LOWER, UPPER)
        op2 = BooleanQuestion.get_divisor()
        q = BooleanQuestion.objects.create(operand1=op1, operand2=op2, operator=BooleanQuestion.MODULUS)
        return q


class ActiveQuestion(models.Model):
    """ A `User` may have up to one `ActiveQuestion` object at a time.
    The `ActiveQuestion` will be deleted when an answer is submitted.
    """
    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    question = models.ForeignKey(BooleanQuestion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "question")

    def __str__(self):
        return "question for {} re: {}".format(
            self.student, self.question)


class BooleanAnswer(models.Model):
    """ A `BooleanAnswer` is a `Student`-created response to a YES/NO question.
    """
    question = models.ForeignKey(BooleanQuestion, on_delete=models.CASCADE)
    student = models.ForeignKey(api_models.Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    raw_answer = models.BooleanField()
    was_correct = models.BooleanField()

    def save(self, *args, **kwargs):
        # retrieve the current `ActiveQuestion` for this `Student`
        active_q = ActiveQuestion.objects.filter(student=self.student).first()
        self.question = active_q.question
        self.was_correct = (self.raw_answer == self.question.correct_answer)
        active_q.question = BooleanQuestion.generate_question()
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
        return "{} selected {}".format(self.student.user.username, self.raw_answer)


@receiver(user_logged_in)
def populate_active_question(sender, user, request, **kwargs):
    if hasattr(user, 'student'):
        # check for an existing `ActiveQuestion`
        q = ActiveQuestion.objects.filter(student=user.student).first()
        if not q:
            ActiveQuestion.objects.create(
                student=user.student, question=BooleanQuestion.generate_question())
