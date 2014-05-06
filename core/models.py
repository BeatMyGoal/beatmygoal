from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from constants import *
from datetime import *
from sys import maxint

import requests
import json
from config import CONFIG
from base64 import b64encode

class Log(models.Model):
    goal = models.OneToOneField('Goal')

    def __str__(self):
        return str("Log - " + str(self.goal))

    def parseEntriesByUser(self):
        """
        Gathers all log entries for this log and sorts
        by user for display in chart
        """
        entries = self.logentry_set.all()
        users = set(entry.participant for entry in entries) #get user set
        chart_days = ((datetime.today() if not self.goal.ending_date else self.goal.ending_date) - self.goal.date_created).days + 2 #how many days to display on chart, should display until end if time based else to today
        total_days = ((datetime.today()) - self.goal.date_created).days + 2 #how many days to calculate for each user
        goal_created = self.goal.date_created
        goal_created = datetime(goal_created.year, goal_created.month, goal_created.day)

        response = {"users" : [], "errors" : [], "days" : [i for i in range(chart_days)]}

        for user in users:
            user_entries = list(entries.filter(participant=user, entry_amount__isnull=False).order_by("entry_date"))
            amounts = []
            for i in range(total_days):
                amount = amounts[i-1] if i > 0 else 0 #amount for this day is equal to previous day
                while user_entries and (user_entries[0].entry_date - (goal_created + timedelta(days=i))).days < 1: #check if there are any more log entries for this day
                    entry = user_entries.pop(0)
                    amount += entry.entry_amount #if there are more entries, add them to today's total
                amounts.append(amount)
            for j in range(total_days, chart_days):
                amounts.append("null"); #or trailing days (if time deadline) insert null
            response["users"].append([user, amounts])


        return response

    def getUserTotal(self, user):
        errors = []
        usr_res = BeatMyGoalUser.getUserByName(user)
        user = usr_res['user'] if not usr_res['errors'] else None
        if not user:
            errors.append(CODE_BAD_USERID)
            return None
        else:
            total = 0
            logentries = list(self.logentry_set.filter(participant = user))
            for entry in logentries:
                total += entry.entry_amount if entry.entry_amount else 0
            return total
    
    def getGoalTotal(self):
        total = 0
        for entry in self.logentry_set.all():
            total += entry.entry_amount
        return total



class LogEntry(models.Model):
    log = models.ForeignKey('Log')
    participant = models.ForeignKey('BeatMyGoalUser', related_name="logentries")
    entry_amount = models.IntegerField(null=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    entry_date.editable=True
    comment = models.TextField()

    def __str__(self):
        return str(self.comment)

    @classmethod
    def create(self, log, participant, amount, comment):
        errors = []
        logEntry = None

        if log and log.goal.isEnded() and amount != None:
            errors.append(CODE_GOAL_ENDED)
            return {'errors': errors, 'logEntry': logEntry}

        if amount != None:
            try:
                amount = int(amount)
                if amount > maxint or amount < 0:
                    errors.append(CODE_BAD_AMOUNT)
            except Exception, e:
                errors.append(CODE_BAD_AMOUNT)
    
        if (not log) or ('script' in comment):
            errors.append(CODE_BAD_LOG)

        if not errors:
            if amount == None:
                # It is a comment
                logEntry = LogEntry(log=log, 
                                    participant=BeatMyGoalUser.objects.get(username=participant),
                                    comment=comment)
            else:
                logEntry = LogEntry(log=log,
                                    participant=BeatMyGoalUser.objects.get(username=participant),
                                    entry_amount=amount,
                                    comment=comment)
            logEntry.save()
            log.goal.checkWinner(participant)

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
    date_created.editable=True
    progress_value = models.FloatField()
    goal_type = models.CharField(max_length=MAX_LEN_TYPE)
    private_setting = models.IntegerField()
    ending_value = models.IntegerField()
    unit = models.CharField(max_length=MAX_LEN_UNIT, blank=True)
    image = models.FileField(upload_to='image/')
    ending_date = models.DateTimeField(blank=True, null=True);
    winning_date = models.DateTimeField(blank=True, null=True);
    winners = models.ManyToManyField('BeatMyGoalUser', blank=True, null=True, related_name='goalsWon')
    ended = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    iscompetitive = models.PositiveSmallIntegerField(default=1, blank=True)
    is_pay_with_venmo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title)

    @classmethod
    def create(self, title, description, creator, prize, private_setting, goal_type, ending_value, unit, ending_date, iscompetitive=1, is_pay_with_venmo=False):
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
        if not ending_value:
            errors.append(CODE_BAD_ENDING_VALUE)
        else:
            try:
                ending_value = float(ending_value)
            except:
                errors.append(CODE_BAD_ENDING_VALUE)

            if ending_value > maxint or ending_value <= 0:
                errors.append(CODE_BAD_ENDING_VALUE)
        if ending_date:
            try:
                ending_date = datetime.strptime(ending_date,'%m/%d/%Y')
            except:
                errors.append(CODE_BAD_DEADLINE)
            if type(ending_date) != datetime or ending_date < datetime.now():
                errors.append(CODE_BAD_DEADLINE)
        if is_pay_with_venmo:
            try:
                prize = float(prize)
                print(prize)
                if prize > 300.00 or prize <= 0:
                    errors.append(CODE_BAD_PRIZE_WITH_VENMO)
            except:
                errors.append(CODE_BAD_PRIZE_WITH_VENMO)

        if is_pay_with_venmo and not creator_user['user'].is_authentificated_venmo:
            errors.append(CODE_NOT_AUTHORIZED_WITH_VENMO)


        if not errors:
            goal = Goal.objects.create(title=title, description=description, creator=BeatMyGoalUser.objects.get(username=creator), 
                prize=prize, private_setting=private_setting, goal_type=goal_type, progress_value=0.0, ending_value=ending_value, 
                unit=unit, ending_date=ending_date, is_pay_with_venmo=is_pay_with_venmo, iscompetitive=int(iscompetitive))
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

        if not goal.ending_value:
            errors.append(CODE_BAD_ENDING_VALUE)
        else:
            try:
                goal.ending_value = float(goal.ending_value)
            except:
                errors.append(CODE_BAD_ENDING_VALUE)
        
        if not errors:
            goal.save()

        return {"errors" : errors}

    def checkWinner(self, user):
        if self.iscompetitive:
            userTotal = self.log.getUserTotal(user)
            if userTotal >= int(self.ending_value):
                self.endGoal(user)
        else:
            goalTotal = self.log.getGoalTotal()
            if goalTotal >= int(self.ending_value):
                self.endGoal([user.username for user in self.beatmygoaluser_set.all()])


    def checkLeaders(self):
        maxAmount = -1
        leaders = []
        for user in self.beatmygoaluser_set.all():
            userAmount = self.log.getUserTotal(user.username)
            if userAmount > maxAmount:
                maxAmount = userAmount
                leaders = [user]
            elif userAmount == maxAmount:
                leaders.append(user)
        return leaders

    def checkDeadline(self):
        if self.ending_date and (datetime.today() > self.ending_date): #if today is after the deadline
            if self.iscompetitive:
                winners = self.checkLeaders()
                self.endGoal(winners) #end goal, declaring the winner(s)
            else:
                self.endGoal() #end goal with no winners, no one met this goal


    def endGoal(self, winner=None):
        if not self.isEnded(): #if the goal hasn't ended yet, end it
            if winner:
                winner = winner if isinstance(winner, list) else [winner]
                for i in range(len(winner)):
                    self.winners.add(BeatMyGoalUser.objects.get(username=winner[i])) #add each winner to the goal
            self.ended = len(winner) if winner else 1 #set the ended value to be the amount of winners
            self.winning_date = datetime.now()
            super(Goal, self).save() #regular save method won't work now
            
            venmo_payment_error = {}
            if (self.is_pay_with_venmo):
                errors={}
                numWinner = len(self.winners.all())
                print 'numWinner : ' + str(numWinner)
                winnersList = self.winners.all()
                print 'winnersList : ' + str(winnersList)
                amount = round( float(self.prize) / numWinner)
                print 'amount : ' + str(amount)
                creator = self.creator
                for winner in winnersList:
                    response_vm_payment = Goal.venmo_make_payment(creator, winner, amount)
                    errors = dict(errors.items() + response_vm_payment.items())
                print("errors : " + str(errors))

    @classmethod
    def venmo_make_payment(self, giver, winner, amount):
        errors={}
        giver_vm_key = BeatMyGoalUser.get_vm_key(giver)['vm_key']
        print('Creator Venmo Key : ' + giver_vm_key)
        receiver = BeatMyGoalUser.getUserByName(winner)['user']
        receiver_email = receiver.email
        print('Receiver Email : ' + receiver_email)
        payment_response = requests.post(
          'https://api.venmo.com/v1/payments',
          data={
            'client_id': CONFIG['vm']['client_key'],
            'client_secret' : CONFIG['vm']['client_secret'],
            'access_token' : giver_vm_key,
            'email' : receiver_email,
            'note' : 'BeatMyGoal!',
            'amount' : amount,
          },
          headers={
            'Authorization': 'Basic {}'.format(
                b64encode('{}:{}'.format(CONFIG['vm']['client_key'], CONFIG['vm']['client_secret']))),
          })
        response = json.loads(payment_response.content)
        if 'error' in response:
            errors[receiver] = response['error']['message']
        return errors
        


    def isEnded(self):
        return self.ended

    def save(self, *args, **kwargs):
        if not self.isEnded():
            super(Goal, self).save(*args, **kwargs)

    def getProgressRatio(self,user):
        if not user in self.beatmygoaluser_set.all():
            return 0
        else:
            progress_ratio = (float(self.log.getUserTotal(user)) / int(self.ending_value)) * 100
        if progress_ratio > 100: progress_ratio=100
        return int(progress_ratio)

    def getDeadlineRatio(self):
        if self.ending_date:
            denom = self.ending_date - self.date_created
            numer = self.ending_date - datetime.today()
        else:
            return 0
        deadlineRatio = (float(numer.days)/(denom.days+1))*100
        return int(deadlineRatio)


    #pretty darn inefficient. come back and fix
    def getBestProgressRatio(self):
        best=0
        for user in self.beatmygoaluser_set.all():
            if self.getProgressRatio(user) > best:
                best = self.getProgressRatio(user)
        return best

    
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
    """

    MAX_LEN_USERNAME = 30
    MAX_LEN_LASTNAME = 30
    MAX_LEN_FIRSTNAME = 30
    MAX_LEN_EMAIL = 30


    goals = models.ManyToManyField(Goal)
    favorite_goals = models.ManyToManyField(Goal, related_name="favorite_goals")
    image = models.FileField(upload_to='userimage/')
    social = models.CharField(null=True, blank=True, max_length=20)
    
    #VENMO
    vm_key = models.CharField(null=True, blank=True, max_length=20)
    vm_refresh_key = models.CharField(null=True, blank=True, max_length=20)
    vm_expire_date = models.DateTimeField(blank=True, null=True);
    is_authentificated_venmo = models.BooleanField(default=False)


    @classmethod
    def set_vm_key(self, username, vm_key, vm_refresh_key, vm_lifetime_seconds):
        print 'in model, user :' + str(username)
        errors = []
        if not BeatMyGoalUser.objects.filter(username=username).exists():
            errors.append(CODE_BAD_USERID)
        user = BeatMyGoalUser.objects.get(username=username)
        user.vm_key = vm_key
        user.vm_refresh_key = vm_refresh_key
        user.vm_expire_date = datetime.now() + timedelta(seconds=vm_lifetime_seconds)
        user.is_authentificated_venmo = True
        user.save()
        return { 'user' : user, 'errors' : errors }

    @classmethod
    def get_vm_key(self, username):
        errors = []
        if not BeatMyGoalUser.objects.filter(username=username).exists():
            errors.append(CODE_BAD_USERID)
        user = BeatMyGoalUser.objects.get(username=username)
        vm_key = user.vm_key
        if vm_key == None:
            errors.append(CODE_NOT_VMCODE)
        return { 'user' : user, 'errors' : errors , 'vm_key' : vm_key }


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

# Admin Models

class GoalAdmin(admin.ModelAdmin):
    list_display  = ('title', 'creator', 'description', 'prize', 'date_created', 'progress_value')
    list_display += ('goal_type', 'private_setting', 'ending_value', 'unit', 'ending_date')


class LogEntryAdmin(admin.ModelAdmin):
    def get_goal_name(self, obj):
        return obj.log.goal
    get_goal_name.short_description = 'Goal'
    list_display = ('comment', 'get_goal_name', 'participant', 'entry_amount', 'entry_date')

class BeatMyGoalUserAdmin(admin.ModelAdmin):
    list_display  = ('username', 'email', 'date_joined')

# Pending Invited User 
class PendingInvite(models.Model):
    goal = models.ForeignKey('Goal')
    email = models.EmailField(null=True, max_length=20)
    @classmethod
    def create(self, email, goal_id):
        errors = []
        pendinginvite = None
        pendinginvite = PendingInvite(email=email, goal=Goal.objects.get(id=goal_id))
        pendinginvite.save()
        return {'errors':errors, 'pendinginvite' : pendinginvite}


