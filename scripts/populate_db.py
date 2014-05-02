import environ
from core.models import *
import random
import datetime
from datetime import timedelta
from django.core.files import File

class FakeUser():
    def __init__(self, username, image=None):
        self.username = username
        self.email = "%s@example.com" % username
        if image != None:
            try:
                f = open('media/userimage/' + image)
                self.image = File(f)
            except IOError:
                pass
        else:
            self.image = None

dummy_users = [
    FakeUser("Nancy", "nancy.jpg"),
    FakeUser("Jimmy", "george.jpg"),
    FakeUser("Yuki", "yuki.jpg"),
    FakeUser("Kimbra", "kimbra.jpg"),
    FakeUser("Roger18", "roger.jpg"),
    FakeUser("blazer99", "blazer.jpg"),    
]

# """
# Jay
# Sol
# Arjun
# Kyle
# Chris
# Tim
# Mitchel  
# Nancie  
# Yuki  
# Garry  
# Kimbra  
# Ali  
# Evan  
# Laurena  
# Johnathan  
# Lela
# """

comments = [
    "This goal looks like so much fun!",
    "I hope I haven't joined too late?",
    "Keep up the good work everybody.",
    "We can do it!",
    "Always do your best. What you plant now, you will harvest later. - Og Mandino",
    "Believe in yourselves...",
    "Can't give up now!",
    "Even if you fall on your face, you're still moving forward. - Victor Kiam"
]

log_comments = [
    "Making good progress...",
    "I was tempted to quit, but now I can't!",
    "Catch me if you can!",
    "Sweet! :)",
    "Let's do this!",
    "Hell yeah!",
    "Let's get motivated!",        
]

class FakeGoal():
    def __init__(self, title, description="sample", prize="sample", 
                 ending_value="100", unit="unit", image=None):
        self.title = title
        self.description = description
        self.ending_value = ending_value
        self.unit = unit
        self.prize = prize
        
        if image != None:
            try:
                f = open('media/image/' + image)
                self.image = File(f)
            except IOError:
                pass
        else:
            self.image = None


    
# Tuple of the form (title, description, prize)
dummy_goals = [
    FakeGoal("Learn how to have a conversation in Japanese", 
             "Who wants to learn some simple Japanese with me?" , 
             "sushi dinner on me",
             "20",
             "sentences",
             image="japanese.jpg"),

    FakeGoal("Raise $500 for the American Red Cross", 
             "The American Red Cross supplies about 40 percent of the nation's blood supply in 2700 hospitals nation wide. We need your help!" , 
             "helping many others",
             "500",
             "dollars",
             image="redcross.jpg"),

    FakeGoal("Watch every episode of The Simpson in order", 
             "'nuff said. Who wants in?" , 
             "popcorn & company",
             "548",
             "episodes",
             image="simpsons.jpg"),

    FakeGoal("Commit the most lines of code to BeatMyGoal repo", 
             "I'm the biggest brogrammer out there" , 
             "$100 heroku credit",
             "50000",
             "lines of code",
             image="code.jpg"),

    FakeGoal("Complete the Fenton's Icecream challenge", 
             "it's a massive three-scoop, banana split with crushed pineapple, fudge, strawberry syrup, whip cream and a cherry on top!" , 
             "glory and calories",
             "3",
             "scoops",
             image="fentons.jpg"),

    FakeGoal("Meet 1 new person in each of our classes", 
             "Berkeley can feel like too big of a big school some times" , 
             "new friends",
             "10",
             "people",
             image="friends.jpg"),

    FakeGoal("Go swimming at the RSF every day for two weeks!", 
             "Swimming exercises every muscle in your body" , 
             "toned bod",
             "200",
             "laps",
             image="pool.jpg"),

    FakeGoal("Keep my apartment clean for a month", 
             "Cleanliness is next to godliness" , 
             "healthier, better environment",
             "30",
             "days",
             image="apartment.jpg"),





    # #("Go to the opera", None , "I'll buy us tickets."),
    # FakeGoal("Raise $500 for the Red Cross",
    # ),

    # FakeGoal("Watch every episode of The Simpsons in order", 
    #          "we can meet at my house!"),

    # #("Make authentic homemade quesadillas",),
    # ("Go running every day for a month",),
    # ("Learn how to play Chopticks on the piano",),
    # ("Program a web app in Erlang",),
    # #("Start writing poetry",),
    # #("Spend at least 2 hours outside everyday",),
    # ("Complete the Fenton's Icecream challenge",),
    # #("30 mile challenge",),
    # ("Commit the most lines of code to BeatMyGoal repo",),
    # ("Meet one new person in all of our classes",),
    # ("Keep my apartment clean for one month",),
    # ("Go swimming at the RSF every day this week!",),
    # #("Play soccer every day for a week",),
    # ("Get a lot of likes on a profile picture",),
]

users = []
goals = []

# Create the users
for u in dummy_users:
    b = BeatMyGoalUser.create(username=u.username, email=u.email, password=u.username)['user']
    print "Creating user: %s" % b
    users.append(b)

    if u.image != None:
        b.image = u.image
    b.save()


users = list(BeatMyGoalUser.objects.filter(id__gt=1))

# Create the goals
for g in dummy_goals:
    x = g
    creator = random.choice(users)

    goal_type = random.choice(['Time-based','Value-based'])

    if (goal_type == 'Time-based'):
       ending_date = datetime.date.today() + datetime.timedelta(days=random.randrange(1,31))
       ending_date = ending_date.strftime('%m/%d/%Y')
    else:
        ending_date =  None

    private_setting = 0

    result = Goal.create(g.title, g.description, creator, g.prize, private_setting, 
                    goal_type, g.ending_value, g.unit, ending_date)

    if result['errors']:
        print "errors", result, x.title
        continue
    else:
        g = result['goal']
    print "Creating goal: ", g

    g.date_created = datetime.datetime.today() - timedelta(days=14)
    
    if x.image != None:
        g.image = x.image
    g.save()
    

    # Add 5 random users, and have them log or comment
    for u in random.sample(users, 5):
        join = BeatMyGoalUser.joinGoal(u.username, g.id)
        
        if (random.randint(0, 1) == 0):
            # Create a log
            le = LogEntry.create(g.log, u.username, 
                                 random.randrange(1,int(g.ending_value)), 
                                 "<p>" + random.choice(log_comments)+ "</p>")['logEntry']

            le.entry_date = datetime.date.today() - datetime.timedelta(days=random.randrange(0,14))
            le.save()
        else:
            # Create a comment (because amount = None)
            le = LogEntry.create(g.log, u.username, 
                                 None, "<p>" + random.choice(comments) +"</p>")['logEntry']

            le.entry_date = datetime.date.today() - datetime.timedelta(days=random.randrange(0,14))
            le.save()

    goals.append(g)
