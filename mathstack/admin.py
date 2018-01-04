from django.contrib import admin
from mathstack.models import (
	BooleanAnswer, IntegerAnswer
	)

admin.site.register(BooleanAnswer)
admin.site.register(IntegerAnswer)
