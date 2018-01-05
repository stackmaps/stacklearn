""" factories.py for the MATHSTACK app
"""
import factory

from api.tests import factories as api_factories
from mathstack import models as mathstack_models


PASSWORD = "W0W ultr@ super secure passw0rd!!!"


class BooleanQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = mathstack_models.BooleanQuestion

    operand1 = 1000
    operand2 = 5
    operator = mathstack_models.BooleanQuestion.MODULUS


class ActiveQuestionFactory(factory.DjangoModelFactory):
    class Meta:
        model = mathstack_models.ActiveQuestion

    question = factory.SubFactory(BooleanQuestionFactory)
    student = factory.SubFactory(api_factories.StudentFactory)


class BooleanAnswerFactory(factory.DjangoModelFactory):
    class Meta:
        model = mathstack_models.BooleanAnswer

    question = factory.SubFactory(BooleanQuestionFactory)
    student = factory.SubFactory(api_factories.StudentFactory)
    raw_answer = True
    was_correct = True

