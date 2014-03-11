# TODO - let's have this script output JSON and use it like this
# https://docs.djangoproject.com/en/dev/howto/initial-data/

from core.models import *
import random

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
    ("Spend at least 2 hours outside everyday",)
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
    #print title
    t = "test"
    g = Goal(creator=creator, title=title, 
             description=t, prize=t, progress_value=1.0, goal_type=t, private_setting=1)
    g.save()
    #print "Creating goal: %s, %s, %s" % creator, title, prize
    goals.append(g)

# Add random users to random goals
for i in range(30):
    g = random.choice(goals)
    u = random.choice(goals)
    u.goals.add(g)
