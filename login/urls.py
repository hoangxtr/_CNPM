from django.contrib import admin
from django.urls import path
from login import views
from django.views import View
urlpatterns = [
    path('', views.Login.as_view(), name='login')
]
