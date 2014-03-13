from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    CODE_SUCCESS = 1
    CODE_BAD_USERNAME = -2
    CODE_BAD_TITLE = -3
    CODE_BAD_DESCRIPTION = -4

    CODE_BAD_PRIZE = -6
    CODE_GOAL_DNE = -7
    CODE_BAD_AUTH = -8
    CODE_BAD_EDIT = -9

    MAX_LEN_DESC = 130
    MAX_LEN_TITLE = 50
    MAX_LEN_PRIZE = 50
    MAX_LEN_TYPE = 20

    creator = models.ForeignKey('BeatMyGoalUser')
    title = models.CharField(max_length=MAX_LEN_TITLE)
    description = models.CharField(max_length=MAX_LEN_DESC)
    prize = models.TextField(max_length=MAX_LEN_PRIZE)
    date_created = models.DateTimeField(auto_now_add=True)
    progress_value = models.FloatField()
    goal_type = models.CharField(max_length=MAX_LEN_TYPE)
    private_setting = models.IntegerField()
    
    def __str__(self):
        return str(self.title)


    @classmethod
    def create(self, title, description, creator, prize, private_setting, goal_type):
        errors = {}

        if not title or len(title)>self.MAX_LEN_TITLE:
            errors['title'] = self.CODE_BAD_TITLE
        if not description or len(description)>self.MAX_LEN_DESC or not goal_type or len(goal_type)>self.MAX_LEN_TYPE:
            errors['description'] = self.CODE_BAD_DESCRIPTION
        if not prize or len(prize)>self.MAX_LEN_PRIZE:
            errors['prize'] = self.CODE_BAD_PRIZE
        creator_user = BeatMyGoalUser.getUserByName(creator)
        if creator_user < 0:
            errors['user'] = self.CODE_BAD_USERNAME


        if errors:
            return { "errors" : errors }
        else:
            goal = Goal.objects.create(title=title, description=description, creator=BeatMyGoalUser.objects.get(username=creator), prize=prize, private_setting=private_setting, goal_type=goal_type, progress_value=0.0 )
            goal.save()
            return {"success" : self.CODE_SUCCESS, "goal" : goal }


    @classmethod
    def remove(self, goal_id, user):
        if not goal_id:
            return self.CODE_GOAL_DNE
        try:
            BMGUser = BeatMyGoalUser.objects.get(username = user)
            goal = Goal.objects.get(id=goal_id)
            if BMGUser != goal.creator:
                return self.CODE_BAD_AUTH
            goal.delete()
            return self.CODE_SUCCESS
        except:
            return self.CODE_GOAL_DNE
    #Goal.create(title="test_title", description="test_description", creator="test_usr", prize="test_prize", private_setting = 1.0, goal_type="teest_goaltype")




    @classmethod
    def edit(self, goal, edits = {}):

        if 'title' in edits:
            goal.title = edits['title']

        if 'description' in edits:
            goal.description = edits['description']




        errors = {}
        if not goal.title or len(goal.title)>self.MAX_LEN_TITLE:
            errors['title'] = self.CODE_BAD_TITLE
        if not goal.description or len(goal.description)>self.MAX_LEN_DESC:
            errors['description'] = self.CODE_BAD_DESCRIPTION

        if errors:
            return {'errors' : errors}
        else:
            goal.save()
            return {"success" : self.CODE_SUCCESS}


    
class BeatMyGoalUser(User):
    """
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
    CODE_SUCCESS = 1
    CODE_BAD_USERNAME = -2              #too long or no character
    CODE_BAD_EMAIL = -3                 #too long, no character, invalid email address
    CODE_BAD_PASSWORD = -4              #too long or no character
    CODE_FAIL_PASSWORD_CONFIRM = -5     #password does not match
    CODE_BAD_CREDENTIAL = -6            #Invalid username and password combination
    CODE_BAD_USERID = -7

    MAX_LEN_USERNAME = 30
    MAX_LEN_LASTNAME = 30
    MAX_LEN_FIRSTNAME = 30
    MAX_LEN_EMAIL = 30

    EXISTING_USERNAME = "An account with this username already exists."
    EXISTING_EMAIL = "An account with this email address already exists."


    #user = models.OneToOneField(User)
    goals = models.ManyToManyField(Goal)

    @classmethod
    def create(self, username, email, password):
        from django.core.validators import validate_email
        errors = {}
        
        if BeatMyGoalUser.objects.filter(username=username).exists():
            errors['username'] = self.EXISTING_USERNAME

        if BeatMyGoalUser.objects.filter(email=email).exists():
            errors['email'] = self.EXISTING_EMAIL

        if errors:
            return { "errors" : errors }
        else:
            user = BeatMyGoalUser(username=username, email=email, password=password)
            user.save()
            return {"success" : self.CODE_SUCCESS, "user" : user }

    @classmethod
    def joinGoal(self, username, goal_id):
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            print(ex1)
            return self.CODE_GOAL_DNE
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            print(ex2)
            return self.CODE_GOAL_DNE
        print(user.goals.all())
        user.goals.add(goal)
        user.save()
        print(user.goals.all())
        return self.CODE_SUCCESS

    @classmethod
    def delete(self, userid):
        try:
            user = User.objects.get(id=userid)
        except:
            return self.CODE_BAD_USERID
        user.delete()
        
        return self.CODE_SUCCESS

    @classmethod
    def getUserById(self, userid):
        try:
            user = BeatMyGoalUser.objects.get(id=userid)
            return user
        except:
            return self.CODE_BAD_USERID

    @classmethod
    def getUserByName(self, username):
        try:
            user = BeatMyGoalUser.objects.get(username=username)
            return user
        except Exception, e:
            return self.CODE_BAD_USERNAME

    @classmethod
    def updateUser(self, user, username=None, email=None, password=None):
        user.username = user.username if username is None else username
        user.email = user.email if email is None else email
        user.password = user.password if password is None else password
        user.save()
        return self.CODE_SUCCESS
    
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
