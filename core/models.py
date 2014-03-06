from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    CODE_SUCCESS = 1
    CODE_BAD_USERNAME = -2
    CODE_BAD_TITLE = -3
    CODE_BAD_DESCRIPTION = -4
    CODE_USERNAME_DNE = -5
    CODE_BAD_PRIZE = -6

    MAX_LEN_DESC = 130
    MAX_LEN_TITLE = 50
    MAX_LEN_PRIZE = 50
    MAX_LEN_TYPE = 20

    creator = models.ForeignKey(User)
    title = models.CharField(max_length=MAX_LEN_TITLE)
    description = models.CharField(max_length=MAX_LEN_DESC)
    prize = models.TextField(max_length=MAX_LEN_PRIZE)
    date_created = models.DateTimeField(auto_now_add=True)
    progress_value = models.FloatField()
    goal_type = models.CharField(max_length=MAX_LEN_TYPE)

    @classmethod
    def create(title, description, creator, prize, private_setting, goal_type):
        if not title or len(title)>MAX_LEN_TITLE:
            return self.CODE_BAD_TITLE
        if not description or len(description)>MAX_LEN_DESC:
            return self.CODE_BAD_DESCRIPTION
        if not creator or len(description)>MAX_LEN_DESC:
            return self.CODE_BAD_DESCRIPTION
        if not prize or len(prize)>MAX_LEN_PRIZE:
            return self.CODE_BAD_DESCRIPTION
        if not goal_type or len(goal_type)>MAX_LEN_TYPE:
            return self.CODE_BAD_DESCRIPTION
        try:
            creator_user = BeatMyGoalUser.objects.get(username=creator)
            goal = Goal.create(title=title, description=description, creator=creator, prize=prize, private_setting=private_setting, goal_type=goal_type)
            goal.save()
            return CODE_SUCCESS 
        except:
            return CODE_BAD_USERNAME
    
class BeatMyGoalUser(models.Model):
    user = models.OneToOneField(User)
    goals = models.ManyToManyField(Goal)
