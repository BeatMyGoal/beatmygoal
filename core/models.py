from django.db import models
from django.contrib.auth.models import User
from django.core.validators import validate_email
from constants import *

class Goal(models.Model):
    """
    Represents any Goal in the BeatMyGoal System.
    """

    MAX_LEN_DESC = 130
    MAX_LEN_TITLE = 50
    MAX_LEN_PRIZE = 50
    MAX_LEN_TYPE = 20
    MAX_LEN_UNIT = 20

    creator = models.ForeignKey('BeatMyGoalUser')
    title = models.CharField(max_length=MAX_LEN_TITLE)
    description = models.CharField(max_length=MAX_LEN_DESC)
    prize = models.TextField(max_length=MAX_LEN_PRIZE)
    date_created = models.DateTimeField(auto_now_add=True)
    progress_value = models.FloatField()
    goal_type = models.CharField(max_length=MAX_LEN_TYPE)
    private_setting = models.IntegerField()
    unit = models.CharField(max_length=MAX_LEN_UNIT, blank=True)

    def __str__(self):
        return str(self.title)


    @classmethod
    def create(self, title, description, creator, prize, private_setting, goal_type):
        errors = []
        goal = None

        if not title or len(title)>self.MAX_LEN_TITLE:
            errors.append(CODE_BAD_TITLE)
        if not description or len(description)>self.MAX_LEN_DESC or not goal_type or len(goal_type)>self.MAX_LEN_TYPE:
            errors.append(CODE_BAD_DESCRIPTION)
        if not prize or len(prize)>self.MAX_LEN_PRIZE:
            errors.append(CODE_BAD_PRIZE)
        creator_user = BeatMyGoalUser.getUserByName(creator)
        if creator_user < 0:
            errors.append(CODE_BAD_USERNAME)

        if not errors:
            goal = Goal.objects.create(title=title, description=description, creator=BeatMyGoalUser.objects.get(username=creator), prize=prize, private_setting=private_setting, goal_type=goal_type, progress_value=0.0, unit=unit )
            goal.save()
            
        return {"errors" : errors, "goal" : goal }


    @classmethod
    def remove(self, goal_id, user):
        errors = []
        if not goal_id:
            errors.append(CODE_GOAL_DNE)
        try:
            BMGUser = BeatMyGoalUser.objects.get(username = user)
            goal = Goal.objects.get(id=goal_id)
            if not BMGUser or BMGUser != goal.creator:
                errors.append(CODE_BAD_AUTH)
            
        except:
            errors.append(CODE_GOAL_DNE)

        if not errors: 
            goal.delete()
        return { "errors" : errors }




    @classmethod
    def edit(self, goal, edits = {}):
        if 'title' in edits:
            goal.title = edits['title']

        if 'description' in edits:
            goal.description = edits['description']

        errors = []
        if not goal.title or len(goal.title)>self.MAX_LEN_TITLE:
            errors.append(CODE_BAD_TITLE)
        if not goal.description or len(goal.description)>self.MAX_LEN_DESC:
            errors.append(CODE_BAD_DESCRIPTION)

        if not errors:
            goal.save()

        return {"errors" : errors}


    
class BeatMyGoalUser(User):
    """
    A BeatMyGoal user extends from a django.auth.User and inherits the
    following properties:

    << User field >>
    * username,
    * email,
    * password,
    * first_name,
    * last_name,
    is_staff,
    is_active,
    is_superuser,
    last_login,
    date_joined


    << User method >>

    """

    MAX_LEN_USERNAME = 30
    MAX_LEN_LASTNAME = 30
    MAX_LEN_FIRSTNAME = 30
    MAX_LEN_EMAIL = 30

    #user = models.OneToOneField(User)
    goals = models.ManyToManyField(Goal)
    
    @classmethod
    def valid_email(self, e):
        return 0 < len(e)

    @classmethod
    def valid_password(self, p):
        return 0 < len(p)

    @classmethod
    def valid_username(self, u):
        return 0 < len(u)

    @classmethod
    def login(self, username, password):
        errors = []

        if not self.valid_username(username):
            errors.append(CODE_BAD_USERNAME)

        if not self.valid_password(password):
            errors.append(CODE_BAD_PASSWORD)

        if (BeatMyGoalUser.objects.filter(username=username).count()) == 0:
            errors.append(CODE_BAD_USERNAME)
        
        users = list(BeatMyGoalUser.objects.filter(username=username))

        if len(users) > 0:
            user = users[0]
            if user.password != password:
                errors.append(CODE_BAD_PASSWORD)
    
        return {"errors": errors}

    @classmethod
    def create(self, username, email, password):
        errors = []
        user = None

        if not self.valid_email(email):
            errors.append(CODE_BAD_EMAIL)

        if not self.valid_username(username):
            errors.append(CODE_BAD_USERNAME)

        if not self.valid_password(password):
            errors.append(CODE_BAD_PASSWORD)
        
        if BeatMyGoalUser.objects.filter(username=username).exists():
            errors.append(CODE_DUPLICATE_USERNAME)

        if BeatMyGoalUser.objects.filter(email=email).exists():
            errors.append(CODE_DUPLICATE_EMAIL)

        if not errors:
            user = BeatMyGoalUser(username=username, email=email, password=password)
            user.save()

        return {"errors" : errors, "user" : user }


    @classmethod
    def joinGoal(self, username, goal_id):
        errors = []
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors.append(CODE_GOAL_DNE)
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            errors.append(CODE_BAD_USERNAME)

        if not errors:
            user.goals.add(goal)
            user.save()

        return { "errors" : errors }

    
    @classmethod
    def leaveGoal(self, username, goal_id):
        errors = []
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors.append(CODE_GOAL_DNE)
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            errors.append(CODE_BAD_USERNAME)
        try:
            user.goals.remove(goal)
        except:
            errors.append(CODE_NOT_PARTICIPANT)

        if not errors:
            user.save()

        return { "errors" : errors }

    @classmethod
    def remove(self, userid):
        errors = []
        if not BeatMyGoalUser.objects.filter(id=userid).exists():
            errors.append(CODE_BAD_USERID)
            return {'errors' : errors}
        user = BeatMyGoalUser.objects.get(id=userid)
        user.delete()
        return {"errors" : errors }

    @classmethod
    def getUserById(self, userid):
        errors = []
        if not BeatMyGoalUser.objects.filter(id=userid).exists():
            errors.append(CODE_BAD_USERID)
            return { 'errors' : errors }
        user = BeatMyGoalUser.objects.get(id=userid)
        return {"errors" : errors, 'user' : user}

    @classmethod
    def getUserByName(self, username):
        errors = []
        user = None
        if not BeatMyGoalUser.objects.filter(username=username).exists():
            errors.append(CODE_BAD_USERNAME)
            return {'errors' : errors}
        user = BeatMyGoalUser.objects.get(username=username)
        return {'errors' : errors, 'user' : user}


    @classmethod
    def updateUser(self, user, username=None, email=None, password=None):
        errors = []
        
        if not BeatMyGoalUser.objects.filter(username=username).exists():
            user.username = user.username if username is None else username
        elif username and username != user.username:
            errors.append(CODE_DUPLICATE_USERNAME)
        if not BeatMyGoalUser.objects.filter(email=email).exists():
            user.email = user.email if email is None else email
        elif email and email != user.email:
            errors.append(CODE_DUPLICATE_EMAIL)
        user.password = user.password if password is None else password

        if not errors:
            user.save()

        return {"errors" : errors, "user" : user }
    
    @classmethod
    def updateUser2(self, user_id, user_name, user_firstName, user_lastName, user_email):
    	try:
    		user = self.getUserById(user_id)
        except:
        	return self.CODE_BAD_USERID
        user.username = user_name
        user.first_name = user_firstName
        user.last_name = user_lastName
        user.email = user_email
        user.save()
    	return self.CODE_SUCCESS
