from django.contrib import admin
from django.urls import path, include
from system.views import *
from django.contrib.auth import views as auth_views

app_name = "system"
urlpatterns = [
    # path('', Login.as_view(), name='login')
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/page/homepage/'), name='logout'),
]

