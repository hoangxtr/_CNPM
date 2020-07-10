from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
<<<<<<< HEAD
from .models import Customer


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField()
    class Meta:
        model = User
        fields = ["username", "password1", "password2",]
=======

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2",]
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = ["username", "password"]


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['avatar']
=======
        fields = ["username", "password"]
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
