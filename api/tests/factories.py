""" factories.py for the MATHSTACK app
"""

import datetime
import factory
import pytz

from django.contrib.auth import get_user_model

from api import models as api_models

PASSWORD = "W0W ultr@ super secure passw0rd!!!"


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = "SampleUser"
    username = factory.Sequence(lambda n: "user_%d" % n)
    email = factory.Sequence(lambda n: "user_%d@example.com" % n)
    password = factory.PostGenerationMethodCall("set_password", PASSWORD)
    last_login = pytz.utc.localize(datetime.datetime(2017, 3, 1))


class StudentFactory(factory.DjangoModelFactory):
    class Meta:
        model = api_models.Student

    user = factory.SubFactory(UserFactory)  # has a ForeignKey!
