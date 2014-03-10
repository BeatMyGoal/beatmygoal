from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Goal(models.Model):
    creator = models.ForeignKey(User)
    title = models.TextField()
    description = models.TextField()
    prize = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    progress_value = models.FloatField()
    
class Participant(models.Model):
    user = models.OneToOneField(User)
    goals = models.ManyToManyField(Goal)



