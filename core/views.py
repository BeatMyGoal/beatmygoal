from django.shortcuts import render
from django.http import HttpResponse
from models import Goal, BeatMyGoalUser
from django.template import RequestContext, loader

# Create your views here

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


def test(request):
    return render(request, 'index.html', {"foo": "bar"})

def edit_user(request, uid):
	user = BeatMyGoalUser.getUserById(uid)
	print user.email
	if request.method == "GET":
		return render(request, 'editUser.html', {
			"username": user.username,
			"email":	user.email,
			})
	elif request.method == "POST":
		data = json.loads(request.body)
		user.username = data['username']
		user.email = data['email']
		return

def logout(request):
    return None


@csrf_exempt
def goal_create_goal(request):
	data = json.loads(request.body)
	title = data['title']
	description = data['description']
	creator = data['creator']
	prize = data['prize']
	private_setting = data['private_setting']
	goal_type = data['goal_type']
	response = Goal.create(title, description, creator, prize, private_setting, goal_type)
	return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")

def goal_delete_goal(request):
	data = json.loads(request.body)
	goal_id = data["goal_id"]
	response = Goal.delete(goal_id)
	return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")

#def goal_remove_user(request):
#	try:
#		req = json.loads(request.body)
#		goal_id = req["goal_id"]
#		user_id = req["user_id"]
#	except:
#		return requeset.send_error(500)
#	response = Goal().remove_user(goal_id, user_id)
#	return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")



def view_user(request):
	try:
		date = json.loads(request.body)
		user_id = date["user_id"]
	except:
		return request.send_error(500)

	user = getUserById(user_id)
	user_name = user.username
	user_firstName = user_firstName
	user_lastName = user.last_name
	user_email = user_email

	response = 1 		   #errCode
	return HttpResponse(json.dumps({"errCode": response, "username" : username,"firstName" : user_firstName, 
									"lastName" : user_lastName, "email" : email}), content_type = "application/json")


def edit_user(request):
	try:
		date = json.loads(request.body)
		user_id = date["user_id"]
		user_name = date["user_name"]
		user_firstName = date["user_firstName"]
		user_lastName = date["user_lastName"]
		user_email = date["user_email"]
	except:
		return request.send_error(500)


	response = BeatMyGoalUser.editUser(user_id, user_name, user_firstName, user_lastName, user_email)


	return HttpResponse(json.dumps({"errCode": response, "username" : username,"firstName" : user_firstName, 
									"lastName" : user_lastName, "email" : email}), content_type = "application/json")


	
def test_user(request):
	return render(request, 'testUserView.html', {"foo": "bar"})


def delete_user(request):
	try:
		req = json.loads(request.body)
		user_id = req["user_id"]
	except:
		return request.send_error(500)
		
		return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")


def logout(request):
    return None
