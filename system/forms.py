from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Customer


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField()
    class Meta:
        model = User
        fields = ["username", "password1", "password2",]


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]


class AvatarForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['avatar']