from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from constants import *
from datetime import *
from sys import maxint

class Log(models.Model):
    goal = models.OneToOneField('Goal')

    def parseEntriesByUser(self):
        entries = self.logentry_set.all()
        users = set(entry.participant for entry in entries)
        chart_days = ((datetime.today() if not self.goal.ending_date else self.goal.ending_date) - self.goal.date_created).days + 3
        total_days = ((datetime.today()) - self.goal.date_created).days + 1
        goal_created = self.goal.date_created
        goal_created = datetime(goal_created.year, goal_created.month, goal_created.day)

        response = {"users" : [], "errors" : [], "days" : [i for i in range(chart_days)]}

        for user in users:
            user_entries = list(entries.filter(participant=user).order_by("entry_date"))
            amounts = []
            for i in range(total_days):
                amount = amounts[i-1] if i > 0 else 0
                while user_entries and (user_entries[0].entry_date - (goal_created + timedelta(days=i))).days <= 0:
                    entry = user_entries.pop(0)
                    amount += entry.entry_amount
                amounts.append(amount)
            for j in range(total_days, chart_days):
                amounts.append("null");
            response["users"].append([user, amounts])


        return response



class LogEntry(models.Model):
    log = models.ForeignKey('Log')
    participant = models.ForeignKey('BeatMyGoalUser', related_name="logentries")
    entry_amount = models.IntegerField()
    entry_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=130)

    @classmethod
    def create(self, log, participant, amount, comment):
        errors = []
        logEntry = None

        amount = int(amount)
        if amount > maxint:
            errors.append(CODE_BAD_AMOUNT)
        if not log:
            errors.append(CODE_BAD_LOG)

        if not errors:
            logEntry = LogEntry(log=log, participant=BeatMyGoalUser.objects.get(username=participant), entry_amount=amount, comment=comment)
            logEntry.save()

        return {'errors':errors, 'logEntry' : logEntry}

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
    ending_value = models.CharField(max_length=MAX_LEN_UNIT, blank=True)
    unit = models.CharField(max_length=MAX_LEN_UNIT, blank=True)
    image = models.FileField(upload_to='image/')
    ending_date = models.DateTimeField(blank=True, null=True);



    def __str__(self):
        return str(self.title)


    @classmethod
    def create(self, title, description, creator, prize, private_setting, goal_type, ending_value, unit, ending_date):
        errors = []
        goal = None


        if not title or len(title)>self.MAX_LEN_TITLE:
            errors.append(CODE_BAD_TITLE)
        if not description or len(description)>self.MAX_LEN_DESC:
            errors.append(CODE_BAD_DESCRIPTION)
        if not goal_type or len(goal_type)>self.MAX_LEN_TYPE:
            errors.append(CODE_BAD_TYPE)
        if not prize or len(prize)>self.MAX_LEN_PRIZE:
            errors.append(CODE_BAD_PRIZE)
        creator_user = BeatMyGoalUser.getUserByName(creator)
        if creator_user < 0:
            errors.append(CODE_BAD_USERNAME)
            
        if ending_date:
            try:
                ending_date = datetime.strptime(ending_date,'%m/%d/%Y')
            except:
                errors.append(CODE_BAD_DEADLINE)
            if type(ending_date) != datetime or ending_date < datetime.now():
                errors.append(CODE_BAD_DEADLINE)


        if not errors:
            goal = Goal.objects.create(title=title, description=description, creator=BeatMyGoalUser.objects.get(username=creator), 
                prize=prize, private_setting=private_setting, goal_type=goal_type, progress_value=0.0, ending_value=ending_value, 
                unit=unit, ending_date=ending_date)
            goal.save()
            BeatMyGoalUser.joinGoal(goal.creator.username, goal.id)
            newLog = Log(goal=goal)
            newLog.save()
            
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

        if 'prize' in edits:
            goal.prize = edits['prize']

        if 'ending_value' in edits:
            goal.ending_value = edits['ending_value']

        if 'unit' in edits:
            goal.unit = edits['unit']



        errors = []
        if not goal.title or len(goal.title)>self.MAX_LEN_TITLE:
            errors.append(CODE_BAD_TITLE)
        if not goal.description or len(goal.description)>self.MAX_LEN_DESC:
            errors.append(CODE_BAD_DESCRIPTION)

        if not errors:
            goal.save()

        return {"errors" : errors}


    
class BeatMyGoalUser(AbstractUser):
    """
    A BeatMyGoal user extends from a django.auth.User and inherits the
    following properties:

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

    MAX_LEN_USERNAME = 30
    MAX_LEN_LASTNAME = 30
    MAX_LEN_FIRSTNAME = 30
    MAX_LEN_EMAIL = 30


    goals = models.ManyToManyField(Goal)
    favorite_goals = models.ManyToManyField(Goal, related_name="favorite_goals")
    image = models.FileField(upload_to='userimage/')
    
    
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
        from django.contrib.auth import login, authenticate

        errors = []

        if not self.valid_username(username):
            errors.append(CODE_BAD_USERNAME)

        if not self.valid_password(password):
            errors.append(CODE_BAD_PASSWORD)

        if (BeatMyGoalUser.objects.filter(username=username).count()) == 0:
            errors.append(CODE_BAD_USERNAME)
        
        user = authenticate(username=username, password=password)
        if user is None:
            errors.append(CODE_BAD_PASSWORD)
    
        return {"errors": errors, 'user' : user}

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
            user = BeatMyGoalUser(username=username, email=email)
            user.set_password(password)
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
    def addFavorite(self, username, goal_id):
        errors = []
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors.append(CODE_GOAL_DNE)
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            errors.append(CODE_BAD_USERNAME)


        if not goal in user.goals.all():
            errors.append(CODE_NOT_PARTICIPANT)
        if not errors:
            print user.favorite_goals
            user.favorite_goals.add(goal)
            user.save()


        return {"errors" : errors}

    
    @classmethod
    def leaveGoal(self, username, goal_id):     #add unit test here
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
            user.goals.get(id=goal_id)
            user.goals.remove(goal)
        except:
            errors.append(CODE_NOT_PARTICIPANT)

        if goal in user.favorite_goals.all():
            user.favorite_goals.remove(goal)

        if not errors:
            user.save()

        return { "errors" : errors }

    @classmethod
    def removeFavorite(self, username, goal_id):     
        errors = []
        try:
            goal = Goal.objects.get(id = goal_id)
        except:
            errors.append(CODE_GOAL_DNE)
        try:
            user = BeatMyGoalUser.objects.get(username = username)
        except:
            errors.append(CODE_BAD_USERNAME)
        if not goal in user.favorite_goals.all():
            errors.append(CODE_NOT_FAVORITE)
            
        try:
            user.favorite_goals.get(id=goal_id)
            user.favorite_goals.remove(goal)
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
