from django.shortcuts import render
from django.http import HttpResponse
from models import *
from django.template import RequestContext, loader, Context

from authomatic import Authomatic
from authomatic.adapters import DjangoAdapter
from config import CONFIG
from django.core.mail import send_mail, BadHeaderError, EmailMessage

authomatic = Authomatic(CONFIG, 'CSRF_TOKEN')

import requests

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

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
from helper import *

import cgi
import urllib

#venmo
from base64 import b64encode


def venmo(request):
    #Parsing 'code' from directed url
    code = request.GET.get('code')
    print 'code : ' + code
    print 'in view, user :' + str(request.user.username)
    
    #Post request to get 'real' access_code
    token_response = requests.post(
      'https://api.venmo.com/v1/oauth/access_token',
      data={
        'client_id':CONFIG['vm']['client_key'],
        'client_secret':CONFIG['vm']['client_secret'],
        'code': code,
        'grant_type': 'authorization_code',
      },
      headers={
        'Authorization': 'Basic {}'.format(
            b64encode('{}:{}'.format(CONFIG['vm']['client_key'], CONFIG['vm']['client_secret']))),
      })
    print 'status code : ' + str(token_response.status_code)
    #assert token_response.status_code == 200
    token_data = json.loads(token_response.content)
    #get venmo token
    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']
    access_token_lifetime_seconds = token_data['expires_in']

    print "token_data : "+ str(token_data)
    print "refresh_token : "+ str(refresh_token)
    print "access_token_lifetime_seconds : "+ str(access_token_lifetime_seconds)

    response = BeatMyGoalUser.set_vm_key(request.user, access_token, refresh_token, access_token_lifetime_seconds)

    response_data = {'data' : token_data, 'set_vm_key' : response }
    return render(request, 'venmo/venmo.html', response_data)

def venmo_login(request):
    user = BeatMyGoalUser.getUserByName(request.user)['user']
    userinfo_response = None
    if user.is_authentificated_venmo:
        user_vm_key = user.vm_key
        url = 'https://api.venmo.com/v1/me?access_token=' + user_vm_key
        userinfo_response = requests.get(url)
        assert userinfo_response.status_code == 200
    if userinfo_response != None:
        data = json.loads(userinfo_response.content)['data']
    else:
        data = None

    print(data)
    response = render(request, 'venmo/venmoLogin.html' ,  {'data' : data, 'is_authentificated_venmo' : user.is_authentificated_venmo})
    return response

def venmo_logout(request):
    errors = []
    print("logout??")
    user = BeatMyGoalUser.getUserByName(request.user)['user']
    user.vm_key = None
    user.vm_refresh_key = None
    user.vm_expire_date = None
    user.is_authentificated_venmo = False
    user.save()

    return HttpResponse(json.dumps({"errors" : errors}), content_type = "application/json")


#Test for making a payment
def venmo_make_payment(request):
    #make request
    data = json.loads(request.body)

    giver = data['giver']
    receiver = data['receiver']
    amount = data['amount']
    giver_vm_key = BeatMyGoalUser.get_vm_key(giver)['vm_key']
    print('giver venmo key : ' + giver_vm_key)
    receiver = BeatMyGoalUser.getUserByName(receiver)['user']
    receiver_email = receiver.email
    print('receiver_email : ' + receiver_email)
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
    print(json.loads(payment_response.content))
    data = json.loads(payment_response.content)['data']

    return HttpResponse(json.dumps({"data": data}), content_type = "application/json")





def send_email(request):
    subject = str(request.user) + " challenged you to beat his goal!"
    message = "This is a test email from BeatMyGoal"
    data = json.loads(request.body)
    to = data["to"].split(",")
    goal_id = data["goal_id"]
    goal = Goal.objects.get(id=int(goal_id))
    errors = []
    if data["to"]:
        # try:
            html_content = loader.get_template('email.html')
            html_content = html_content.render(Context({'from' : request.user.username, 'goal_id' : goal_id, 'goal' : goal }))
            email = EmailMessage(subject, html_content, to=to)
            email.content_subtype = "html"
            for email_address in to:
                pendinginvite = PendingInvite.create(email_address, goal_id)
            email.send()
        # except Exception as e:
        #     errors.append(-400)
    else:
        errors.append(-401)
    return HttpResponse(json.dumps({"errors" : errors, "redirect" : ""}), content_type = "application/json")

def email_preview(request):
    return render_to_response('email.html', {'from' : request.user.username.capitalize() })

def user_login_fb(request, mock=None):
    """
    Handles the login of a user from Facebook.
    If there is no BMG account for the user, one is created.
    """
    response = HttpResponseRedirect("/dashboard/")
    result = authomatic.login(DjangoAdapter(request, response), "fb") if not mock else mock

    if result:
        if result.error: pass #TODO
        elif result.user:
            # Get the info from the user
            if not (result.user.name and result.user.id):
                result.user.update()

            username, email= result.user.name, result.user.email

            if (BeatMyGoalUser.objects.filter(username=username).exists()):
                user = BeatMyGoalUser.objects.get(username=username)
                user.backend='django.contrib.auth.backends.ModelBackend'
                if not mock: login(request, user)
            else:
                password = BeatMyGoalUser.objects.make_random_password(8)
                user = BeatMyGoalUser.create(username, email, password)['user']
                user =  authenticate(username=username, password=password)
                user.social = result.user.id
                user.save()

                if not mock:
                    url = 'http://graph.facebook.com/{}/picture?width=200&height=200'.format(result.user.id)
                    temp=NamedTemporaryFile(delete=True)
                    temp.write(requests.get(url).content)
                    temp.flush()
                    user.image.save("faceimage" + str(result.user.id) + ".jpg",File(temp), save = True)               
                    login(request, user)
                response['Location'] = '/users/%s/?tutorial=true' % (user.id)

    return response

def user_login_twitter(request, mock=None):
    """
    Handles the login of a user from Facebook.
    If there is no BMG account for the user, one is created.
    """
    response = HttpResponseRedirect("/dashboard/")
    result = authomatic.login(DjangoAdapter(request, response), "tw") if not mock else mock

    if result:
        print result
        if result.error: pass #TODO
        elif result.user:
            # Get the info from the user
            if not (result.user.name and result.user.id):
                result.user.update()

            username, email= result.user.name, result.user.name + "2" + result.user.name + ".com"

            if (BeatMyGoalUser.objects.filter(username=username).exists()):
                user = BeatMyGoalUser.objects.get(username=username)
                user.backend='django.contrib.auth.backends.ModelBackend'
                if not mock: login(request, user)
            else:
                password = BeatMyGoalUser.objects.make_random_password(8)
                user = BeatMyGoalUser.create(username, email, password)['user']
                user =  authenticate(username=username, password=password)
                user.social = result.user.id
                user.save()

                if not mock:
                    url = 'http://graph.facebook.com/{}/picture?width=200&height=200'.format(result.user.id)
                    temp=NamedTemporaryFile(delete=True)
                    temp.write(requests.get(url).content)
                    temp.flush()
                    user.image.save("faceimage" + str(result.user.id) + ".jpg",File(temp), save = True)               
                    login(request, user)
                response['Location'] = '/users/%s/?tutorial=true' % (user.id)

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
        query = data["query"]
        filter_type = data["filter"]
        all_goals = Goal.objects.all()
        curr_user = request.user
        filtered_goals = dashboard_filter(filter_type, all_goals, curr_user)
        queried_goals = dashboard_search(query, filtered_goals)
        if (page*20+19 < len(queried_goals)):
            goals = queried_goals[page*20:page*20+19]
        else:
            goals = queried_goals[page*20:]
        serialized_goals = serializers.serialize('json', goals)
        json_data = json.dumps({'goals':serialized_goals})
        return HttpResponse(json_data, content_type="application/json")
    else:
        curr_user = request.user
        all_users = BeatMyGoalUser.objects.all()
        goals = Goal.objects.all()
        temp_goals = []
        if curr_user.is_authenticated():
            for goal in goals:
                if (len(goal.pendinginvite_set.filter(email=curr_user.email,goal=goal))>0 and (len(goal.beatmygoaluser_set.filter(username=curr_user))==0)):
                    temp_goals.append(goal)
            num_invites = len(temp_goals)
        else:
            num_invites = 0;
        return render(request, 'dashboard/dashboard_main.html', {
                'pending_invites': num_invites,
                'users': all_users
            })

def dashboard_search(query, goals):
    temp_goals = []
    for goal in goals:
        if query.lower() in goal.title.lower() or query in goal.description.lower():
            temp_goals.append(goal)
    return temp_goals

def dashboard_filter(filter_type, goals, curr_user):
    temp_goals = []
    if curr_user.is_authenticated():
        if filter_type == "mine":
            for goal in goals:
                if (len(goal.beatmygoaluser_set.filter(username=curr_user))>0):
                    temp_goals.append(goal)
        elif filter_type == "priv":
            for goal in goals:
                if goal.private_setting==1 and (len(goal.beatmygoaluser_set.filter(username=curr_user))>0):
                    temp_goals.append(goal)
        elif filter_type == "pend":
            for goal in goals:
                if (len(goal.pendinginvite_set.filter(email=curr_user.email,goal=goal))>0 and (len(goal.beatmygoaluser_set.filter(username=curr_user))==0)):
                    temp_goals.append(goal)
        else:
            for goal in goals:
                if goal.private_setting==0:
                    temp_goals.append(goal)
    else:
        if filter_type == "all":
            for goal in goals:
                if goal.private_setting==0:
                    temp_goals.append(goal)
        else:
            return []
    return temp_goals

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
            iscompetitive = int(data['iscompetitive']) if "iscompetitive" in data else 1
            is_pay_with_venmo = data.get('is_pay_with_venmo',False)

            if private_setting:

                response = Goal.create(title, description, creator, prize, 1, goal_type, ending_value, unit, ending_date, iscompetitive, is_pay_with_venmo)
            else:
                response = Goal.create(title, description, creator, prize, 0, goal_type, ending_value, unit, ending_date, iscompetitive, is_pay_with_venmo)

            if response['errors']:
                print(response['errors'])
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



def confirm(request):
    """
    Reauthenticates a user if they are about to make an important account change
    (e.g. change their password)
    """
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
    goal.checkDeadline()
    image = str(goal.image)
    isCreator = str(request.user) == str(goal.creator)
    isParticipant = len(goal.beatmygoaluser_set.filter(username=request.user)) > 0
    progress = goal.log.parseEntriesByUser()
    progress_ratio = goal.getProgressRatio(request.user)
    best_progress_ratio = goal.getBestProgressRatio()
    deadline_ratio = goal.getDeadlineRatio()
    leaders = goal.checkLeaders()
    print leaders
    print goal.winners
    try:
        isFavorite = goal in request.user.favorite_goals.all()
    except:
        isFavorite = False

    return render(request, 'goals/viewGoal.html', {"goal" : goal, "user" : request.user, 
        "isParticipant" : isParticipant, "isCreator" : isCreator, 
        "isFavorite" : isFavorite, "image" :image, "goal_id" : goal_id, "progress" : progress,
        "progressRatio" : progress_ratio, "deadlineRatio" : deadline_ratio, "bestprogressRatio" : best_progress_ratio, "leaders" : leaders})


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
            amount = data.get('amount', None)
            response = LogEntry.create(log=goal.log, participant=request.user, amount=amount, comment=data['comment'])
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
        redirect= data['redirect'] if 'redirect' in data else "/dashboard/"
        response = BeatMyGoalUser.login(username,password)
            
        if response['errors']:
            return HttpResponse(json.dumps(response), content_type = "application/json")
        else:
            user = response['user']
            login(request, user)
            return HttpResponse(json.dumps({"errors": response['errors'], 
                                            "redirect" : redirect}),
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
            redirect = "/users/%s/?tutorial=true" % (user.id)
            if "goal" in data:
                BeatMyGoalUser.joinGoal(user, data['goal'])
                redirect = "/goals/" + str(data['goal'])
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
            chart1_data = goal_to_numEntry(response['user'])
            chart2_data = date_to_numEntry(response['user'])
            streak = get_streaks(response['user'])
            return render(request, 'users/viewUser.html', {'streak': streak, 'chart2_data': chart2_data, 'chart1_data' : chart1_data, 'viewedUser' : response['user'], 'errors' : response['errors']} )

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

def user_logout(request):
    """
    De-authenticates the user and redirects to the homepage.
    """
    logout(request)
    return HttpResponseRedirect('/')



def goal_image_upload(request,goal_id):
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
            return HttpResponseRedirect('/goals/' + goal_id)
    else:
        image = ImageForm() #empty

        return HttpResponseRedirect('/goals/' + goal_id)

    

def user_image_upload(request,user_id):
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
    
    return HttpResponseRedirect(reverse('view_user', args=(user_id,)))
    

