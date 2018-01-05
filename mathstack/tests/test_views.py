""" test_views.py for the MATHSTACK app

    To run these tests, from an activated virtualenv run this command:

        python manage.py test --keepdb
"""

from django.shortcuts import reverse
import mathstack.tests.factories as mathstack_factories
from mathstack.tests.test_helpers import LoggedInStudentTestCase


class TestBoolAnswerCreateView(LoggedInStudentTestCase):

    def setUp(self):
        super(TestBoolAnswerCreateView, self).setUp()
        self.url = reverse("bool_answer_create")
        self.active_q = mathstack_factories.ActiveQuestionFactory()

    def test_bool_answer_create_get(self):
        response = self.client.get(self.url)

        self.assertContains(
            response, 
            "<h1>Math Practice Page</h1>")
