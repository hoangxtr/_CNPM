from django.contrib import admin
from django.urls import path, include
from system.views import *
<<<<<<< HEAD

app_name = "system"
urlpatterns = [
    # path('', Login.as_view(), name='login')
=======
app_name = "system"
urlpatterns = [
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
]

