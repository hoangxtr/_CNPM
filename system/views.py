from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth import login, authenticate
<<<<<<< HEAD
# from homepage.models import *
from system.models import Customer, Admin, Chef
=======
from homepage.models import *
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
# Create your views here.

<<<<<<< HEAD
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


=======
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
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
<<<<<<< HEAD
            phone = rform.cleaned_data["phone"]
            user = User.objects.create_user(username=username, password=password)
            customer = Customer.objects.create(user=user, name=username, email=email, phone=phone)
=======
            user = User.objects.create_user(username=username, email=email, password=password)
            customer = Customer.objects.create(user=user, name=username)
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
            return redirect('../login/')
        else:
            rform = RegisterForm()
            return render(request, "_CNPM/register.html", {"form":rform})
<<<<<<< HEAD


class Login(View):
    def get(self, request):
        return render(request, '_CNPM/login.html', {'form': LoginForm()})
=======
        

def my_login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            print("Not remember me")
            request.session.set_expiry(0)
    return login(request, *args, **kwargs)

class Login(View):
    def get(self, request):
        lform = LoginForm()
        return render(request, "_CNPM/login.html", {"form":lform})
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4

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
<<<<<<< HEAD
            print('Customer')
=======
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
            return redirect('/page/homepage/')
        return redirect('/admin/')


<<<<<<< HEAD

=======
        
       
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
