from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.views import View
# Create your views here.

def register(response):
    form = RegisterForm()
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
    return render(response, "main/register.html", {"form":form})





