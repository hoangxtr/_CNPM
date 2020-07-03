from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from homepage.models import *
# Create your views here.

def my_login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            print("Not remember me")
            request.session.set_expiry(0)
    return login(request, *args, **kwargs)

class Login(View):
    def get(self, request):
        return render(request, '_CNPM/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None: 
            return HttpResponse("Logined false")
        my_login(request, user=user)
        if Admin.objects.filter(user=user).exists():
            return redirect('/page/adminpage/')
        elif Chef.objects.filter(user=user).exists():
            return redirect('/page/chefpage/')
        elif Customer.objects.filter(user=user).exists():
            return redirect('/page/homepage/')
        return redirect('/admin/')

        
       