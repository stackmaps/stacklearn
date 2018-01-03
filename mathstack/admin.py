from django.contrib import admin
from mathstack.models import (
	Student, BooleanAnswer, IntegerAnswer
	)

admin.site.register(Student)
admin.site.register(BooleanAnswer)
admin.site.register(IntegerAnswer)
