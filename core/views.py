from django.shortcuts import render
from django.http import HttpResponse
from models import Goal, BeatMyGoalUser, Log, LogEntry
from django.template import RequestContext, loader

from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter
from config import CONFIG

authomatic = Authomatic(CONFIG, 'CSRF_TOKEN')

# Create your views here

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core import serializers

from django.core.urlresolvers import reverse
from django.views.generic import FormView,DetailView
from .forms import ImageForm


def user_login_fb(request):
    """
    Handles the login of a user from Facebook.
    If there is no BMG account for the user, one is created.
    """
    #response = HttpResponse()
    response = HttpResponseRedirect("/dashboard/")
    result = authomatic.login(DjangoAdapter(request, response), "fb")
     

    if result:
        if result.error:
            #TODO - right now this is redirecting anyway
            pass
        elif result.user:
            # Get the info from the user
            if not (result.user.name and result.user.id):
                result.user.update()

            username, email= result.user.name, result.user.email

            if (BeatMyGoalUser.objects.filter(username=username).exists()):
                user = BeatMyGoalUser.objects.get(username=username)
                user.backend='django.contrib.auth.backends.ModelBackend'
                login(request, user)
            else:
                password = BeatMyGoalUser.objects.make_random_password(8)
                user = BeatMyGoalUser.create(username, email, password)['user']
                user =  authenticate(username=username, password=password)
                login(request, user)
                response['Location'] = '/users/profile'

    return response


def index(request):
    """
    Returns the homepage of the app.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect("/dashboard/")
    else:
        return render(request, 'index.html')


@csrf_exempt
def dashboard(request):
    """
    Returns the dashboard which contains all goals.
    """
    if request.is_ajax():
        data = json.loads(request.body)
        page = data["page"]
        all_goals = Goal.objects.all()
        if (page*20+19 < len(all_goals)):
            goals = all_goals[page*20:page*20+19]
        else:
            goals = all_goals[page*20:]
        serialized_goals = serializers.serialize('json', goals)
        json_data = json.dumps({'goals':serialized_goals})
        return HttpResponse(json_data, content_type="application/json")
    else:
        all_users = BeatMyGoalUser.objects.all()
        return render(request, 'dashboard/dashboard_main.html', {
                'users': all_users
            })

@csrf_exempt
def goal_create_goal(request):
    """
    Creates a goal if the user is authenticated.
    """
    if request.user.is_authenticated():
        if request.method == "GET":
            return render(request, 'goals/createGoal.html')
        if request.user.is_authenticated():

            data = json.loads(request.body)
            title = data['title']
            description = data['description']
            creator = request.user
            prize = data['prize']
            private_setting = data['private_setting']
            goal_type = data['goal_type']
            unit = data['unit']
            ending_value = data['ending_value']
            ending_date = data['ending_date']

            response = Goal.create(title, description, creator, prize, private_setting, goal_type, ending_value, unit, ending_date)

            if response['errors']:
                return HttpResponse(json.dumps(response), content_type = "application/json")
            else:
                goal = response['goal']
                redirect = "/goals/%s/" % (goal.id)
                return HttpResponse(json.dumps({"redirect" : redirect,
                    "errors" : response["errors"]}), content_type = "application/json")
        else:
            return HttpResponse("Invalid request", status=500)
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def goal_remove_goal(request):
    """
    Removes the goal if it belongs to the user.
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]

    user = request.user 
    response = Goal.remove(goal_id, user)

    if response['errors']:
            return HttpResponse(json.dumps(response), 
                                content_type = "application/json")  
    return HttpResponse(json.dumps({"redirect" : "/dashboard",
        "errors" : response["errors"]}), content_type = "application/json")


def goal_join_goal(request):        #add Functional test here
    """
    Adds a user as a participant of a goal.
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]
    user = request.user 
    response = BeatMyGoalUser.joinGoal(user, goal_id)
    redirect = "/goals/" + str(goal_id)
    if response['errors']:
            return HttpResponse(json.dumps(response), 
                                content_type = "application/json")
    return HttpResponse(json.dumps({"errors": response["errors"],
        "redirect" : redirect}), content_type = "application/json")

def goal_add_favorite(request):
    """
    Adds a goal as a favorite goal
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]
    user = request.user
    response = BeatMyGoalUser.addFavorite(user, goal_id)
    
    redirect = "/goals/" + str(goal_id)
    if response['errors']:
            return HttpResponse(json.dumps(response), 
                                content_type = "application/json")
    return HttpResponse(json.dumps({"errors": response["errors"],
        "redirect" : redirect}), content_type = "application/json")

def goal_leave_goal(request):       #add Functional test here
    """
    Removes a user as a participant of a goal.
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]
    user = request.user 
    response = BeatMyGoalUser.leaveGoal(user, goal_id)
    redirect = "/goals/" + str(goal_id)
    if response['errors']:
        return HttpResponse(json.dumps(response),content_type = "application/json")

    return HttpResponse(json.dumps({"errors": response["errors"],
        "redirect" : redirect}), content_type = "application/json")

def goal_remove_favorite(request):       
    """
    Removes a user as a participant of a goal.
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]
    user = request.user 
    response = BeatMyGoalUser.removeFavorite(user, goal_id)
    print response
    redirect = "/goals/" + str(goal_id)
    if response['errors']:
        return HttpResponse(json.dumps(response),content_type = "application/json")

    return HttpResponse(json.dumps({"errors": response["errors"],
        "redirect" : redirect}), content_type = "application/json")


@csrf_exempt
def goal_edit_goal(request, gid):
    """
    Edit the attributes of a goal if you are it's creator
    """
    gid = int(gid)
    goal = Goal.objects.get(id=gid)
    user = request.user
    goalTitle= str(goal.title)
    if ( user.is_authenticated() and goal.creator.id == user.id ):
        if request.method == "GET":
            return render(request, 'goals/editGoal.html', {"goal": goal })
        elif request.method == "POST":
            data = json.loads(request.body)
            
            title = data["title"]
            description = data["description"]
            prize = data["prize"]
            ending_value = data["ending_value"]
            unit =  data["unit"]

            
            edits = {'title': title, 'description': description, 'prize' : prize, 
                    'ending_value' : ending_value, 'unit' : unit}
        
            response = Goal.edit(goal, edits)
            if response['errors']:
                return HttpResponse(json.dumps(response), content_type = "application/json")
            else:
                return HttpResponse(json.dumps({"redirect":"/goals/" + str(gid),
                    "errors" : response["errors"]}), content_type = "application/json")
    else:
        return HttpResponse("Invalid request", status=500)            



def confirm(request):           #add Functional test here
    if request.method == "POST":
        data = json.loads(request.body)
        user = request.user;
        password = data["password"]
        response = BeatMyGoalUser.login(user.username, password)
        return HttpResponse(json.dumps({'errors':response['errors']}), content_type = "application/json")


def goal_view_goal(request, goal_id):
    """
    View the profile of a goal.
    """
    goal = Goal.objects.get(id=goal_id)
    image = str(goal.image)
    isCreator = str(request.user) == str(goal.creator)
    isParticipant = len(goal.beatmygoaluser_set.filter(username=request.user)) > 0
    isFavorite = goal in request.user.favorite_goals.all()
    return render(request, 'goals/viewGoal.html', {"goal" : goal, "user" : request.user, "isParticipant" : isParticipant, "isCreator" : isCreator, "isFavorite" : isFavorite, "image" :image, "goal_id" : goal_id})


def goal_log_progress(request, gid):       #add Functional test here
    """
    Allows users to log their progress for a goal
    """
    goal = Goal.objects.get(id=gid)
    if request.method == "GET":
        return render(request, 'goals/logGoal.html', {'goal' : goal})
    elif request.method == "POST":
        if request.user.is_authenticated() and len(goal.beatmygoaluser_set.filter(username=request.user)) > 0:
            data = json.loads(request.body)
            response = LogEntry.create(log=goal.log, participant=request.user, amount=data['amount'], comment=data['comment'])
            if response['errors']:
                return HttpResponse(json.dumps(response), content_type='application/json')
            else:
                return HttpResponse(json.dumps({
                        "redirect":"/goals/" + str(gid),
                        "errors" : response['errors']
                    }), content_type='application/json')
        else:
            return HttpResponse("Invalid request", status=500)


def user_login(request):
    """
    Authenticates the user credential, login if valid
    """
    # if request.method == "GET":
    #     return render(request, 'users/login.html')

    if request.method == "POST":
        data = json.loads(request.body)
        username= data["username"]
        password= data["password"]
        response = BeatMyGoalUser.login(username,password)
            
        if response['errors']:
            return HttpResponse(json.dumps(response), content_type = "application/json")
        else:
            user = response['user']
            login(request, user)
            return HttpResponse(json.dumps({"errors": response['errors'], 
                                            "redirect" : "/dashboard/"}),
                                content_type = "application/json")

@csrf_exempt
def profile(request):       #add Functional test here
    """
    Returns the profile of the authenticated user or else prompts them to login.
    """
    if request.user.is_authenticated():
        user = request.user
        uid = user.id
        user_url = "/users/"+str(uid)+"/"
        return HttpResponseRedirect(user_url)
    else:
        return HttpResponseRedirect('/users/create/')

@csrf_exempt
def create_user(request):
    """
    Creates a user and authenticates them, if credentials are valid.
    """

    if request.method == "GET":
            return render(request, 'index.html')
    elif request.method == "POST":
        data = json.loads(request.body)
        username, email, password = data["username"], data["email"], data["password"]
        response = BeatMyGoalUser.create(username, email, password)

        if response['errors']:
            return HttpResponse(json.dumps(response), 
                                content_type = "application/json")            
        else:
            # user = response['user']
            user =  authenticate(username=username, password=password)
            login(request, user)
            redirect = "/users/%s/" % (user.id)
            return HttpResponse(json.dumps({"redirect" : redirect,
                "errors" : response["errors"]
                }), content_type = "application/json")

    else:
        return HttpResponse("Invalid request", status=500)


def view_user(request, uid):
    """ 
    Returns the profile of the user with id, uid. 
    """
    if request.method == "GET":
        response = BeatMyGoalUser.getUserById(uid)
        if response['errors']:
            return render(request, 'users/viewUser.html', { "errors" : response["errors"] })
        else:
            return render(request, 'users/viewUser.html', {'viewedUser' : response['user'], 'errors' : response['errors']} )

#@csrf_exempt
def edit_user(request, uid):
    """ 
    Allows users to edit their profile if they are logged in.
    """
    uid = int(uid)
    user = request.user
    #user = BeatMyGoalUser.getUserById(uid)
    if (user.is_authenticated() and user.id == uid):
        if request.method == "GET":
            return render(request, 'users/editUser.html', {
                "username": user.username,
                "email":    user.email,
            })
        elif request.method == "POST":
            data = json.loads(request.body)
            username = data['username']
            email = data['email']
            password = data['password']

            loginResponse = BeatMyGoalUser.login(user.username, password)
            if loginResponse['errors']:
                return HttpResponse(json.dumps({"errors" : loginResponse["errors"]}), content_type = "application/json")


            response = BeatMyGoalUser.updateUser(user, username, email)



            if response['errors']:
                return HttpResponse(json.dumps({'errors': response['errors']}), content_type = "application/json")            
            else:
                redirect = "/users/" + str(uid)
                return HttpResponse(json.dumps({"redirect" : redirect,
                    "errors" : response['errors']
                    }), content_type = "application/json")
        #return HttpResponse(json.dumps(res), content_type = 'application/json', status=200)
    else:
        return HttpResponse("Invalid request", status=500)

@csrf_exempt
def delete_user(request, uid):
    """ 
    Allows users to delete their Userid if they are logged in.
    """
    uid = int(uid)
    if request.method == "POST":
        user = request.user;
        if (user.is_authenticated() and user.id == uid):
            response = BeatMyGoalUser.remove(uid)
            if len(response['errors']) == 0:
                return HttpResponse(json.dumps({"redirect": "/"}), content_type = "application/json")
            else:
                ttpResponse("Invalid request", status=500)
    return HttpResponse("Invalid request", status=500)

def user_logout(request):       #add Functional test here
    """
    De-authenticates the user and redirects to the homepage.
    """
    logout(request)
    return HttpResponseRedirect('/')



def goal_image_upload(request,goal_id):          #add Functional test here
    """
    Allows users to upload their goal's image
    """
    goal = Goal.objects.get(id=goal_id)
    isCreator = str(request.user) == str(goal.creator)
    isParticipant = len(goal.beatmygoaluser_set.filter(username=request.user)) > 0
    # Handle file upload
    if request.method == "POST":
        image = ImageForm(request.POST, request.FILES)
        if image.is_valid():
            goal.image = request.FILES['image']
            goal.save()

            #return HttpResponseRedirect(reverse('goal_view_goal', args=(goal_id,)))
            return HttpResponseRedirect('/goals/' + goal_id)
    else:
        image = ImageForm() #empty

        return HttpResponseRedirect('/goals/' + goal_id)
    #return render(request, 'goals/viewGoal.html', {'image': image, 'goal_id': goal_id, 'goal' : goal, 'user' : request.user, 'isParticipant' : isParticipant, 'isCreator' : isCreator})
    

def user_image_upload(request,user_id):          #add Functional test here
    """
        Allows users to upload their user's profile image
    """
    user = BeatMyGoalUser.objects.get(id = user_id)
    goal = user.goals
    # Handle file upload
    if request.method == "POST":
        image = ImageForm(request.POST, request.FILES)
        if image.is_valid():
            user.image = request.FILES['image']
            user.save()
            return HttpResponseRedirect(reverse('view_user', args=(user_id,)))
    else:
        image = ImageForm() #empty
    
    #return render(request, 'users/viewUser.html', {'image': image, 'user': user, 'goal':goal })
    return HttpResponseRedirect(reverse('view_user', args=(user_id,)))
    

