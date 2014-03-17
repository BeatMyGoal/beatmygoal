from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    """
    Represents any Goal in the BeatMyGoal System.
    """
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
        errors = {}
        if not goal_id:
            errors['goal'] = self.CODE_GOAL_DNE
        try:
            BMGUser = BeatMyGoalUser.objects.get(username = user)
            goal = Goal.objects.get(id=goal_id)
            if BMGUser != goal.creator:
                errors['auth'] = self.CODE_BAD_AUTH
            
        except:
            errors['goal'] = self.CODE_GOAL_DNE
        if errors:
            return { "errors" : errors }
        else:   
            goal.delete()
            return { "success" : self.CODE_SUCCESS }
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
    INVALID_USERNAME = "Invalid Username"
    INVALID_EMAIL = "Invalid Email Address"
    INVALID_PASSWORD = "Invalid Password"
    INVALID_USERID = "Invalid UserID"
    NOT_A_PARTICIPANT = "You are not a participant of this goal"

    #user = models.OneToOneField(User)
    goals = models.ManyToManyField(Goal)
    favorites = models.ManyToManyField(Goal, blank=True, related_name='favorite_goals')


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
        errors = {}

        if not self.valid_username(username):
            errors['username'] = self.INVALID_USERNAME

        if not self.valid_password(password):
            errors['password'] = self.INVALID_PASSWORD

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

    @classmethod
    def create(self, username, email, password):
        from django.core.validators import validate_email
        errors = {}

        if not self.valid_email(email):
            errors['email'] = self.INVALID_EMAIL

        if not self.valid_username(username):
            errors['username'] = self.INVALID_USERNAME

        if not self.valid_password(password):
            errors['password'] = self.INVALID_PASSWORD
        
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
    def addFavorite(self, username, goal_id):
        errors = {}
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors['goal'] = Goal.CODE_GOAL_DNE
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            errors['user'] = self.INVALID_USERNAME

        if errors:
            return { "errors" : errors }
        user.favorites.add(goal)
        user.save()
        return { "success" : self.CODE_SUCCESS }

    @classmethod
    def removeFavorite(self, username, goal_id):
        errors = {}
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors['goal'] = Goal.CODE_GOAL_DNE
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            print(ex2)
            errors['user'] = self.INVALID_USERNAME
        try:
            user.favorites.remove(goal)
        except:
            errors['participant'] = self.NOT_A_PARTICIPANT

        if errors:
            print errors
            return { "errors" : errors }

        user.save()
        print "HMMMph"
        return { "success" : self.CODE_SUCCESS }


    @classmethod
    def joinGoal(self, username, goal_id):
        errors = {}
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors['goal'] = Goal.CODE_GOAL_DNE
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            print(ex2)
            errors['user'] = self.INVALID_USERNAME

        if errors:
            return { "errors" : errors }

        user.goals.add(goal)
        user.save()
        return { "success" : self.CODE_SUCCESS }

    
    @classmethod
    def leaveGoal(self, username, goal_id):
        errors = {}
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors['goal'] = Goal.CODE_GOAL_DNE
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            print(ex2)
            errors['user'] = self.INVALID_USERNAME
        try:
            user.goals.remove(goal)
        except:
            errors['participant'] = self.NOT_A_PARTICIPANT

        if errors:
            return { "errors" : errors }

        user.save()
        return { "success" : self.CODE_SUCCESS }

    @classmethod
    def remove(self, userid):
        errors = {}
        if not BeatMyGoalUser.objects.filter(id=userid).exists():
            errors['userid'] = self.INVALID_USERID
            return {'errors' : errors}
        user = BeatMyGoalUser.objects.get(id=userid)
        user.delete()
        returnValue = {"success" : self.CODE_SUCCESS }
        return returnValue

    @classmethod
    def getUserById(self, userid):
        errors = {}
        if not BeatMyGoalUser.objects.filter(id=userid).exists():
            errors['userid'] = self.INVALID_USERID
            return { 'errors' : errors }
        user = BeatMyGoalUser.objects.get(id=userid)
        returnValue = {"success" : self.CODE_SUCCESS, 'user' : user}
        return returnValue

    @classmethod
    def getUserByName(self, username):
        errors = {}
        if not BeatMyGoalUser.objects.filter(username=username).exists():
            errors['username'] = self.INVALID_USERNAME
            return {'errors' : errors}
        user = BeatMyGoalUser.objects.get(username=username)
        returnValue = {"success" : self.CODE_SUCCESS, 'user' : user}
        return returnValue


    @classmethod
    def updateUser(self, user, username=None, email=None, password=None):
        errors = {}

        if not BeatMyGoalUser.objects.filter(username=username).exists():
            user.username = user.username if username is None else username
        elif username and username != user.username:
            errors['username'] = self.CODE_BAD_USERNAME

        if not BeatMyGoalUser.objects.filter(email=email).exists():
            user.email = user.email if email is None else email
        elif email and email != user.email:
            errors['email'] = self.CODE_BAD_EMAIL

        user.password = user.password if password is None else password
        if errors:
            return {"errors" : errors}
        else:
            user.save()
            return {"success" : self.CODE_SUCCESS, "user" : user }
    
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

