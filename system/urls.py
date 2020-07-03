from django.contrib import admin
from django.urls import path, include
from system.views import *

urlpatterns = [
    path('', Login.as_view(), name='login')
]

