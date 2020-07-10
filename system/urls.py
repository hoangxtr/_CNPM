from django.contrib import admin
from django.urls import path, include
from system.views import *

app_name = "system"
urlpatterns = [
    # path('', Login.as_view(), name='login')
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
]

