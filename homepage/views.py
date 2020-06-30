from django.shortcuts import render, HttpResponse
from django.views import View
from homepage.models import *
from django.contrib.auth.models import User

# Create your views here.

class HomePage(View):
    def get(self, request):
        
        return render(request, '_CNPM/index.html')