from models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Goal, GoalAdmin)
admin.site.register(BeatMyGoalUser, BeatMyGoalUserAdmin)
admin.site.register(Log)
admin.site.register(LogEntry, LogEntryAdmin)
