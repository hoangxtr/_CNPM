from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth import login, authenticate
# from homepage.models import *
from system.models import Customer, Chef
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
# Create your views here.

import datetime
import time
from django.http import StreamingHttpResponse

def stream(request):
    return render(request, '_CNPM/test.html')

def my_login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            print("Not remember me")
            request.session.set_expiry(0)
    return login(request, *args, **kwargs)


class Register(View):
    def get(self, request):
        rform = RegisterForm()
        return render(request, "_CNPM/register.html", {"form":rform})
    def post(self, request):
        rform = RegisterForm(request.POST)
        if rform.is_valid():
            username = rform.cleaned_data["username"]
            email = rform.cleaned_data["email"]
            password = rform.cleaned_data["password1"]
            user = User.objects.create_user(username=username, email=email, password=password)
            customer = Customer.objects.create(user=user, name=username)
            return redirect('../login/')
        else:
            rform = RegisterForm()
            return render(request, "_CNPM/register.html", {"form":rform})


class Login(View):
    def get(self, request):
        return render(request, '_CNPM/login.html', {'form': LoginForm()})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None: 
            return HttpResponse("Logined false")
        my_login(request, user=user)
        if Chef.objects.filter(user=user).exists():
            return redirect('/page/chefpage/')
        elif Customer.objects.filter(user=user).exists():
            print('Customer')
            return redirect('/page/homepage/')
        return redirect('/admin/')
