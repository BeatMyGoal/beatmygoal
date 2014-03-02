from django.shortcuts import render
from django.http import HttpResponse
from models import Goal, Participant


# Create your views here

from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.


def test(request):
    return render(request, 'index.html', {"foo": "bar"})


def edit_user(request):
	return render()


def edit_user(request):

    return render(request, 'base.html', {"foo": "bar"})

def logout(request):
    return None

def goal_delete_goal(request):
	try:
		req = json.loads(request.body)
		goal_id = req["goal_id"]
	except:
		return request.send_error(500)
	response = Goal().delete_goal(goal_id)
	return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")

def goal_remove_user(request):
	try:
		req = json.loads(request.body)
		goal_id = req["goal_id"]
		user_id = req["user_id"]
	except:
		return requeset.send_error(500)
	response = Goal().remove_user(goal_id, user_id)
	return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")



def logout(request):
    return None

>>>>>>> e998a153870639fba86293d5b48b1b4a2af4f95e
