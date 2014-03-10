from django.shortcuts import render
from django.contrib.auth import authenticate, login
# Create your views here.

def test(request):
    return render(request, 'index.html', {"foo": "bar"})


def user_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    
    elif request.method == "POST":
        data = json.loads(request.body)
        username= data["username"]
        password= data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            response = -6
            return HttpResponse(json.dumps({"errCode": response}), content_type = "application/json")
