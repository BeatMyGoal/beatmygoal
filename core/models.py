from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    CODE_SUCCESS = 1
    CODE_BAD_USERNAME = -2
    CODE_BAD_TITLE = -3
    CODE_BAD_DESCRIPTION = -4
    CODE_USERNAME_DNE = -5
    CODE_BAD_PRIZE = -6
    CODE_GOAL_DNE = -7
    CODE_BAD_AUTH = -8
    CODE_BAD_EDIT = -9

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
            creator_user = BeatMyGoalUser.getUserByName(creator)
            goal = Goal.objects.create(title=title, description=description, creator=User.objects.get(username=creator), prize=prize, private_setting=private_setting, goal_type=goal_type, progress_value=0.0 )
            goal.save()
            return self.CODE_SUCCESS 
        except:
            return self.CODE_BAD_USERNAME


    @classmethod
    def remove(self, goal_id, user):
        if not goal_id:
            return self.CODE_GOAL_DNE

        try:
            goal = Goal.objects.get(id=goal_id)
            if not user or user != goal.creator:
                return CODE_BAD_AUTH
                
            goal.delete()
            return self.CODE_SUCCESS
        except:
            return self.CODE_GOAL_DNE
    #Goal.create(title="test_title", description="test_description", creator="test_usr", prize="test_prize", private_setting = 1.0, goal_type="teest_goaltype")

    @classmethod
    def edit(self, goal_id, user, edits):
        if not goal_id:
            return self.CODE_GOAL_DNE
        try:
            goal = Goal.objects.get(id=goal_id)
            if not user or user != goal.creator:
                return CODE_BAD_AUTH
        except:
            return self.CODE_GOAL_DNE


        try:
            if "title" in edits:
                goal.title = edits["title"]
            if "description" in edits:
                goal.description = edits["description"]
            if "private_setting" in edits:
                goal.private_setting = edits["private_setting"]
            goal.save()
            return self.CODE_SUCCESS
        except:
            return self.CODE_BAD_EDIT




    
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

    user = models.OneToOneField(User)
    goals = models.ManyToManyField(Goal)
    
    @classmethod
    def create(self, username, email, password):
        user = User.objects.create_user(username, email, password)
        user.save()
        return self.CODE_SUCCESS
    
    @classmethod
    def login(self, username, password):
        if ((User.objects.filter(username = username).count()) == 0):
            return self.CODE_BAD_CREDENTIAL
        else:
            userid = User.objects.get(username = username)
            if (userid.password != password):
                return self.CODE_BAD_CREDENTIAL
            else:
                return self.CODE_SUCCESS

    @classmethod
    def delete(self, username, email, password):
        
        return self.CODE_SUCCESS

    @classmethod
    def getUserById(self, userid):
        try:
            user = User.objects.get(id=userid)
            return user
        except:
            return User.CODE_BAD_USERID

    @classmethod
    def getUserByName(self, username):
        try:
            user = User.objects.get(username=username)
            return user
        except Exception, e:
            return User.CODE_BAD_USERNAME

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

    @classmethod
    def deleteUser(self, user_id):
    	try:
    		user = self.getUserById(user_id)
        except:
        	return self.CODE_BAD_USERID
        user.delete()
        return self.CODE_SUCCESS
