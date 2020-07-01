from django.shortcuts import render, HttpResponse
from django.views import View
from homepage.models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class HomePage(View):
    # login_url = '/login/'
    def get(self, request):
        return render(request, '_CNPM/index.html')

class ChefPage(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, '_CNPM/order.html')

class AdminPage(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, '_CNPM/index.html')
