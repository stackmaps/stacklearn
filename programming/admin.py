from django.contrib import admin
from programming.models import (ActivePuzzle, GamePuzzle, GameSolution)
# Register your models here.

admin.site.register(ActivePuzzle)
admin.site.register(GamePuzzle)
admin.site.register(GameSolution)
