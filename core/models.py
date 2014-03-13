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


INVALID_USERNAME = "Invalid Username"
INVALID_PASSWORD = "Invalid Password"

def login(self, username, password):
    errors = {}
    if (BeatMyGoalUser.objects.filter(username=username).count()) == 0:
        errors['username'] = self.INVALID_USERNAME
    users = list(BeatMyGoalUser.objects.filter(username=username))
    if len(users) > 0:
        user = users[0]
        if user.password != password:
            errors['password'] = self.INVALID_PASSWORD

    if errors:
        return {"errors": errors}

    else:
        return {"success" : self.CODE_SUCCESS}

