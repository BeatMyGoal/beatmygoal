from django.shortcuts import render
from django.http import HttpResponse
from models import Goal, BeatMyGoalUser
from django.template import RequestContext, loader

# Create your views here

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core import serializers


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
        print("page")
        print(page)
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
            response = Goal.create(title, description, creator, prize, private_setting, goal_type)

            if "errors" in response:
                return HttpResponse(json.dumps(response), content_type = "application/json")
            else:
                goal = response['goal']
                redirect = "/goals/%s/" % (goal.id)
                return HttpResponse(json.dumps({"redirect" : redirect,
                    "success" : response["success"]}), content_type = "application/json")
        else:
            return HttpResponse("Invalid request", status=500)
    else:
        return render(request, 'users/login.html', {
            "message": "You must be logged in to create a goal"
        })


@csrf_exempt
def goal_remove_goal(request):
    """
    Removes the goal if it belongs to the user.
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]

    user = request.user 
    response = Goal.remove(goal_id, user)

    if "errors" in response:
            return HttpResponse(json.dumps(response), 
                                content_type = "application/json")  
    return HttpResponse(json.dumps({"redirect" : "/dashboard",
        "success" : response["success"]}), content_type = "application/json")

def goal_join_goal(request):
    """
    Adds a user as a participant of a goal.
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]
    user = request.user 
    response = BeatMyGoalUser.joinGoal(user, goal_id)
    redirect = "/goals/" + str(goal_id)
    if "errors" in response:
            return HttpResponse(json.dumps(response), 
                                content_type = "application/json")

    return HttpResponse(json.dumps({"success": response["success"],
        "redirect" : redirect}), content_type = "application/json")

def goal_leave_goal(request):
    """
    Removes a user as a participant of a goal.
    """
    data = json.loads(request.body)
    goal_id = data["goal_id"]
    user = request.user 
    response = BeatMyGoalUser.leaveGoal(user, goal_id)
    redirect = "/goals/" + str(goal_id)
    if "errors" in response:

        return HttpResponse(json.dumps(response),content_type = "application/json")

    return HttpResponse(json.dumps({"success": response["success"],
        "redirect" : redirect}), content_type = "application/json")


@csrf_exempt
def goal_edit_goal(request, gid):
    """
    Edit the attributes of a goal if you are it's creator
    """
    gid = int(gid)
    goal = Goal.objects.get(id=gid)
    user = request.user
    if ( user.is_authenticated() and goal.creator.id == user.id ):
        if request.method == "GET":
            return render(request, 'goals/editGoal.html', {"title": goal.title, "description": goal.description })
        elif request.method == "POST":
            data = json.loads(request.body)
            title = data["title"]
            description = data["description"]
            edits = {'title': title, 'description': description}
     
            response = Goal.edit(goal, edits)
            if 'errors' in response:
                return HttpResponse(json.dumps(response), content_type = "application/json")
            else:
                return HttpResponse(json.dumps({"redirect":"/goals/" + str(gid),
                    "success" : response["success"]}), content_type = "application/json")
    else:
        return HttpResponse("Invalid request", status=500)            



def goal_view_goal(request, goal_id):
    """
    View the profile of a goal.
    """
    goal = Goal.objects.get(id=goal_id)

    isCreator = str(request.user) == str(goal.creator)
    isParticipant = len(goal.beatmygoaluser_set.filter(username=request.user)) > 0

    return render(request, 'goals/viewGoal.html', {"goal" : goal, "user" : request.user, "isParticipant" : isParticipant, "isCreator" : isCreator})


#def goal_remove_user(request):
#    try:
#        req = json.loads(request.body)
#        goal_id = req["goal_id"]
#        user_id = req["user_id"]
#    except:
#        return requeset.send_error(500)
#    response = Goal().remove_user(goal_id, user_id)
#    return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")


def user_login(request):
    """
    Authenticates the user credential, login if valid 
    """
    #if request.method == "GET":
    #    return render(request, 'users/login.html')
    
    #elif request.method == "POST":
    data = json.loads(request.body)
    username= data["username"]
    password= data["password"]
    #user = authenticate(username=username, password=password)
    response = BeatMyGoalUser.login(username,password)
    users = list(BeatMyGoalUser.objects.filter(username=username))
        
    if "errors" in response:
        return HttpResponse(json.dumps(response), content_type = "application/json")
        
    if len(users) > 0:
        u = users[0]
        if u.password == password:
            u.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, u)
            return HttpResponse(json.dumps({"success": 1, "redirect" : "/dashboard/"}),
                                    content_type = "application/json")

@csrf_exempt
def profile(request):
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
            return render(request, 'users/createUser.html', {
            })
    elif request.method == "POST":
        data = json.loads(request.body)
        username, email, password = data["username"], data["email"], data["password"]
        response = BeatMyGoalUser.create(username, email, password)

        if "errors" in response:
            return HttpResponse(json.dumps(response), 
                                content_type = "application/json")            
        else:
            user = response['user']
            #TODO
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            # authenticate(username=username, password=password)
            login(request, user)
            redirect = "/users/%s/" % (user.id)
            return HttpResponse(json.dumps({"redirect" : redirect,
                "success" : response["success"]
                }), content_type = "application/json")

    else:
        return HttpResponse("Invalid request", status=500)

def view_user(request, uid):
    """ 
    Returns the profile of the user with id, uid. 
    """
    if request.method == "GET":
        response = BeatMyGoalUser.getUserById(uid)
        if "errors" in response:
            return render(request, 'users/viewUser.html', { "errors" : response["errors"] })
        else:
            user = response['user']
            return render(request, 'users/viewUser.html', {
                'username' : user.username,
                'email' : user.email,
                'userid' : user.id,
                })

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
            response = BeatMyGoalUser.updateUser(user, username, email)

            if "errors" in response:
                return HttpResponse(json.dumps(response), content_type = "application/json")            
            else:
                redirect = "/users/" + str(uid)
                return HttpResponse(json.dumps({"redirect" : redirect,
                "success" : response["success"]
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
            return HttpResponse(json.dumps({"redirect": "/"}), content_type = "application/json")
    return HttpResponse("Invalid request", status=500)

def user_logout(request):
    """
    De-authenticates the user and redirects to the homepage.
    """
    logout(request)
    return HttpResponseRedirect('/')


