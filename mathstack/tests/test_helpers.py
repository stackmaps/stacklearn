"""  mathstack/tests/test_helpers.py 
     --> helper functions for testing the MATHSTACK app.
"""

from django.test import Client, TestCase
from mathstack.tests.factories import PASSWORD, StudentFactory, UserFactory


class LoggedInUserTestCase(TestCase):  # the base class -- contains no tests

    def setUp(self):
        self.user = UserFactory()
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)


class LoggedInStudentTestCase(TestCase):  # the base class -- contains no tests

    def setUp(self):
        self.user = UserFactory()
        self.teacher = StudentFactory(user=self.user)
        self.client = Client()
        self.client.login(username=self.user.username, password=PASSWORD)
