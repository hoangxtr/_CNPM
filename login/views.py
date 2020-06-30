from django.shortcuts import render, HttpResponse
from django.views import View
from django.contrib.auth import authenticate
from login.models import *
# Create your views here.
class Login(View):
    def get(self, request):
        return render(request, '_CNPM/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username)
        # print(password)

        kind = request.POST['kind']
        people = None
        if kind == 'Customer':
            people = Customer.objects.filter(username=username)
        elif kind == 'Admin':
            people = Admin.objects.filter(username=username)
        else:
            people = Chef.objects.filter(username=username)
        if not people.exists():
            return HttpResponse("Your login is false")
        
        return HttpResponse("You are logined")