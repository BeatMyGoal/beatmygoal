# TODO - let's have this script output JSON and use it like this
# https://docs.djangoproject.com/en/dev/howto/initial-data/

from core.models import *
import random
from random import randrange
import datetime
from datetime import timedelta

dummy_users = \
"""
Jay
Sol
Arjun
Kyle
Chris
Tim
Mitchel  
Nancie  
Yuki  
Garry  
Kimbra  
Ali  
Evan  
Laurena  
Johnathan  
Lela
"""

# Tuple of the form (title, description, prize)
dummy_goals = [
    ("Learn how to have a conversation in Japanese", None , "sushi dinner on me"),
    ("Go to the opera", None , "I'll buy us tickets."),
    ("Raise $500 for 'American Heart Association'",),
    ("Watch every episode of The Simpsons in order", "we can meet at my house!"),
    ("Make authentic homemade quesadillas",),
    ("Go running every day for a month",),
    ("Learn how to play Chopticks on the piano",),
    ("Program a web app in Erlang",),
    ("Start writing poetry",),
    ("Spend at least 2 hours outside everyday",),
    ("Complete the Fenton's Icecream challenge",),
    ("30 mile challenge",),
    ("Commit the most lines of code",),
    ("Meet one new person in all of my classes",),
    ("Keep my apartment clean for one month",),
    ("Go to the RSF everyday!",),
    ("Play soccer every day for a week",),
    ("Get the most likes on a profile picture",),
]

users = []
goals = []

# # Create the users
for user in dummy_users.split("\n"):
    if not user:
        continue
    user = user.strip()
    email = "%s@example.com" % user
    b = BeatMyGoalUser(username=user, email=email, password=user)
    b.save()
    print "Creating user: %s" % user
    users.append(b)

get = lambda x, y: x[y] if y < len(x) else ''
users = list(BeatMyGoalUser.objects.all())
# Create the goals
for g in dummy_goals:
    creator = random.choice(users)
    title = g[0]
    description = "This is a test Goal"
    prize = "$" + str(randrange(1,50) * 100)
    goal_type = random.choice(['Time-based','Value-based'])
    ending_value = str(randrange(1,6) * 100)
    #unit = random.choice(['dollar','pounds','kg','lines','km','times'])
    unit = "TEST_UNIT"
    if (goal_type == 'Time-based'):
        ending_date = datetime.date.today() + datetime.timedelta(days=randrange(1,31))
    else:
        ending_date =  None
    g = Goal(creator=creator, title=title, description=description, prize=prize, progress_value=1.0, goal_type=goal_type, private_setting=1, ending_value = ending_value, unit = unit, ending_date = ending_date)
    g.save()
    l = Log(goal=g)
    l.save()
    for u in users:
        join = BeatMyGoalUser.joinGoal(u.username, g.id)
        
        if (random.randint(0, 100) % 2 == 0):
            # Create a log entry
            for i in range(random.randint(0,10)):
                le = LogEntry.create(l, u.username, randrange(1,100), "<p>hello world</p>")['logEntry']
                le.entry_date = datetime.date.today() - datetime.timedelta(days=randrange(0,14), seconds=randrange(1,100))
                le.save()
        else:
            # Create a comment (because amount = None)
            for i in range(random.randint(0,10)):
                le = LogEntry.create(l, u.username, None, "<p>hello world</p>")['logEntry']
                le.entry_date = datetime.date.today() - datetime.timedelta(days=randrange(0,14), seconds=randrange(1,100))
                le.save()
    goals.append(g)

# Add random users to random goals
for i in range(30):
    g = random.choice(goals)
    u = random.choice(goals)
    u.goals.add(g)
