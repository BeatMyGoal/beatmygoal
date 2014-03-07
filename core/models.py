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
    private_setting = models.IntegerField()
     
    @classmethod
    def create(self, title, description, creator, prize, private_setting, goal_type):
        if not title or len(title)>self.MAX_LEN_TITLE:
            return self.CODE_BAD_TITLE
        if not description or len(description)>self.MAX_LEN_DESC:
            return self.CODE_BAD_DESCRIPTION
        if not creator or len(description)>self.MAX_LEN_DESC:
            return self.CODE_BAD_DESCRIPTION
        if not prize or len(prize)>self.MAX_LEN_PRIZE:
            return self.CODE_BAD_DESCRIPTION
        if not goal_type or len(goal_type)>self.MAX_LEN_TYPE:
            return self.CODE_BAD_DESCRIPTION
        try:
            creator_user = BeatMyGoalUser.objects.get(user=User.objects.get(username=creator))
            goal = Goal.objects.create(title=title, description=description, creator=User.objects.get(username=creator), prize=prize, private_setting=private_setting, goal_type=goal_type, progress_value=0.0 )
            goal.save()
            return self.CODE_SUCCESS 
        except:
            return self.CODE_BAD_USERNAME
    
class BeatMyGoalUser(User):
    """
    << User field >>
    * username,
    * email,
    * password,
    first_name,
    last_name,
    is_staff,
    is_active,
    is_superuser,
    last_login,
    date_joined


    << User method >>

    """
    CODE_SUCCESS = 1

    user = models.OneToOneField(User)
    goals = models.ManyToManyField(Goal)
    
    @classmethod
    def create(self, username, email, password):
        p = self.objects.create_user(username, email, password)
        p.save()
        return CODE_SUCCESS


    @classmethod
    def getUserById(self, uid):
        try:
            user = User.objects.get(id=uid)
            return user
        except:
            return -1 #TODO ERROR CODES
    @classmethod
    def getUserByName(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except Exception, e:
            return -1;
