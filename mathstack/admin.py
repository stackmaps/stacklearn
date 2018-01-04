from django.contrib import admin
from mathstack.models import (
	Student, ActiveQuestion, BooleanAnswer, IntegerAnswer
	)

admin.site.register(Student)
admin.site.register(ActiveQuestion)
admin.site.register(BooleanAnswer)
admin.site.register(IntegerAnswer)
