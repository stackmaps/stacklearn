from django.contrib import admin
from mathstack import models


admin.site.register(models.BooleanQuestion)
admin.site.register(models.ActiveQuestion)
admin.site.register(models.BooleanAnswer)
admin.site.register(models.IntegerAnswer)
