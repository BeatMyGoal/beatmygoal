from django.shortcuts import render

# Create your views here.

def test(request):
    return render(request, 'index.html', {"foo": "bar"})

def edit_user(request):
	return render()
