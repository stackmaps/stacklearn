""" test_views.py for the MATHSTACK app

    To run these tests, from an activated virtualenv run this command:

        python manage.py test --keepdb
"""

from django.shortcuts import reverse
from api.tests import factories as api_factories
import mathstack.tests.factories as mathstack_factories
from mathstack.tests.test_helpers import LoggedInStudentTestCase


class TestBoolAnswerCreateView(LoggedInStudentTestCase):

    def setUp(self):
        super(TestBoolAnswerCreateView, self).setUp()
        self.url = reverse("bool_answer_create")
        self.active_q = mathstack_factories.ActiveQuestionFactory()

    def test_bool_answer_create_get_not_student(self):
        user = api_factories.UserFactory()
        self.client.login(username=user.username, password=api_factories.PASSWORD)

        response = self.client.get(self.url)

        self.assertEqual(404, response.status_code)

    def test_bool_answer_create_get(self):
        response = self.client.get(self.url)

        self.assertContains(
            response, 
            "<h1>Math Practice Page</h1>")

    def test_bool_answer_create_post(self):
        data = {
        }

        original_active_question_id = self.student.activequestion_set.first().id
        num_answers_before = self.student.booleananswer_set.count()

        response = self.client.post(self.url, data=data, follow=True)

        self.assertEqual(200, response.status_code)
        self.assertEqual([('/math/div/', 302)], response.redirect_chain)

        updated_active_question = self.student.activequestion_set.first()
        num_answers_after = self.student.booleananswer_set.count()
        self.assertEqual(num_answers_after, num_answers_before + 1)
        self.assertNotEqual(original_active_question_id,
                            updated_active_question.question.id,
                            "Question should be updated when answer is submitted")

        self.assertContains(
            response,
            "<h1>Math Practice Page</h1>")
