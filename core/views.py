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


def index(request):
    return render(request, 'index.html')


@csrf_exempt
def dashboard(request):
	all_goals = Goal.objects.all()
	print(all_goals)
	goals = all_goals[0:10]
	print(goals)
	return render(request, 'dashboard/dashboard_main.html', {
		"goals": goals
	})




@csrf_exempt
def goal_create_goal(request):
    if request.user.is_authenticated():
    	if request.method == "GET":
    		return render(request, 'goals/createGoal.html')

    	if request.user.is_authenticated():
    		print "here"
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
	data = json.loads(request.body)
	goal_id = data["goal_id"]
	user = request.user 
	response = Goal.remove(goal_id, user)
	return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")

def goal_join_goal(request):
    data = json.loads(request.body)
    goal_id = data["goal_id"]
    user = request.user 
    response = BeatMyGoalUser.joinGoal(user, goal_id)
    return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")

@csrf_exempt
def goal_edit_goal(request, gid):
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
            print edits
            response = Goal.edit(goal, edits)
            print response
            if 'errors' in response:
                return HttpResponse(json.dumps(response), content_type = "application/json")
            else:
                return HttpResponse(json.dumps({"redirect":"/goals/" + str(gid),
                    "success" : response["success"]}), content_type = "application/json")
    else:
        return HttpResponse("Invalid request", status=500)            






def goal_view_goal(request, goal_id):
	goal = Goal.objects.get(id=goal_id)
	return render(request, 'goals/viewGoal.html', {"goal" : goal})


#def goal_remove_user(request):
#	try:
#		req = json.loads(request.body)
#		goal_id = req["goal_id"]
#		user_id = req["user_id"]
#	except:
#		return requeset.send_error(500)
#	response = Goal().remove_user(goal_id, user_id)
#	return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")


def user_login(request):
    errors = {}
    if request.method == "GET":
        return render(request, 'users/login.html')
    
    elif request.method == "POST":
        data = json.loads(request.body)
        username= data["username"]
        password= data["password"]
        #user = authenticate(username=username, password=password)
        users = list(BeatMyGoalUser.objects.filter(username=username))
        if len(users) > 0:
            u = users[0]
            if u.password == password:
                u.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, u)
                return HttpResponse(json.dumps({"errCode": 1, "redirect" : "/dashboard/"}), 
                                    content_type = "application/json")

            else:
                errors['password'] = "Invalid password"
                return HttpResponse(json.dumps({"errCode": -1}), content_type = "application/json")
        else:
            errors['username'] = "Invalid username"
            return HttpResponse(json.dumps({"errCode": -1}), content_type = "application/json")

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
    print request.method
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
        user = BeatMyGoalUser.getUserById(uid)
        return render(request, 'users/viewUser.html', {
            "user_profile" : user
        })
		
#@csrf_exempt
def edit_user(request, uid):
	uid = int(uid)
	user = request.user
	#user = BeatMyGoalUser.getUserById(uid)
	if (user.is_authenticated() and user.id == uid):
		if request.method == "GET":
			return render(request, 'users/editUser.html', {
				"username": user.username,
				"email":	user.email,
			})
		elif request.method == "POST":
			data = json.loads(request.body)
			print data
			username = data['username']
			email = data['email']
			response = BeatMyGoalUser.updateUser(user, username, email)
			res = {
				"errCode" : response,
				"redirect": "/users/" + str(uid)
			}
			print "test"
			return HttpResponse(json.dumps(res), content_type = 'application/json', status=200)
	else:
		return HttpResponse("Invalid request", status=500)

@csrf_exempt
def delete_user(request, uid):
	uid = int(uid)
	if request.method == "POST":
		user = request.user;
		if (user.is_authenticated() and user.id == uid):
			response = BeatMyGoalUser.delete(uid)
			return HttpResponse(json.dumps({"errCode": response, "redirect": "/"}), content_type = "application/json")
		else:
			return HttpResponse("Invalid request", status=500)
	else:
		return HttpResponse("Invalid request", status=500)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

