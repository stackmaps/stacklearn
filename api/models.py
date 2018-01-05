# api/models.py

from django.conf import settings
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

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


def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# adds an authtoken to all new users
models.signals.post_save.connect(create_auth_token, sender=settings.AUTH_USER_MODEL)
