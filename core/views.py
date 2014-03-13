from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
# Create your views here.

def user_login(request):
    if request.method == "GET":
        return render(request, 'users/login.html')
    
    elif request.method == "POST":
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
                return HttpResponse(json.dumps({"errCode": 1, "redirect" : "/dashboard/"}),
                                    content_type = "application/json")


