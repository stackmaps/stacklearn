""" test_models.py for the MATHSTACK app

    To run these tests, from an activated virtualenv run this command:

        python manage.py test --keepdb
"""

from django.test import TestCase

from mathstack import models as mathstack_models
import mathstack.tests.factories as mathstack_factories


class TestBooleanQuestion(TestCase):

    def setUp(self):
        super(TestBooleanQuestion, self).setUp()
        self.question = mathstack_factories.BooleanQuestionFactory()

    def test_str(self):
        self.assertEqual('1000 % 5 == 0', str(self.question))

    def test_compute_answer(self):
        answer = self.question.compute_answer()
        self.assertTrue(answer, '{} should be True'.format(self.question))

    def test_compute_answer_invalid_operator(self):
        question = mathstack_factories.BooleanQuestionFactory()
        question.operator = '/'

        try:
            question.compute_answer()
            self.fail('Should not be able to compute answer for invalid operator')
        except RuntimeError as e:
            self.assertEqual("Unknown question operator '/'.", str(e))

    def test_get_divisor(self):
        divisor = mathstack_models.BooleanQuestion.get_divisor()
        self.assertIn(divisor, mathstack_models.BooleanQuestion.DIVISORS)

    def test_generate_question(self):
        question = mathstack_models.BooleanQuestion.generate_question()
        self.assertGreaterEqual(question.operand1, mathstack_models.BooleanQuestion.LOWER)
        self.assertLess(question.operand1, mathstack_models.BooleanQuestion.UPPER)
        self.assertEqual(question.operator, mathstack_models.BooleanQuestion.MODULUS)
        self.assertIn(question.operand2, mathstack_models.BooleanQuestion.DIVISORS)
