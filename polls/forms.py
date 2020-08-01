from django import forms
from system.models import Food, Owner, Vendor
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class HomeFood(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name', 'price', 'description', 'image', 'quantity', 'prepare')

    def clean_foodImage(self):
        temp = str(self.cleaned_data['foodImage'])
        if temp[-4::1] == '.png' or temp[-4::1] == '.jpg':
            return temp
        else:
            raise forms.ValidationError('Đây Không Phải Tệp Hình Ảnh')



class OwnerRegisterForm(forms.Form):
    store = forms.CharField(label='Tên Cửa Hàng', max_length=30, widget=forms.TextInput(attrs={'class': 'add_food'}))
    username = forms.CharField(label='Tài khoản', max_length=30, widget=forms.TextInput(attrs={'class': 'add_food'}))
    name = forms.CharField(label='Họ và Tên', max_length=20, widget=forms.TextInput(attrs={'class': 'add_food'}))
    phone = forms.CharField(label='Số Điện Thoại', max_length=13, widget=forms.TextInput(attrs={'class': 'add_food'}))
    password1 = forms.CharField(label='Mật Khẩu', widget=forms.TextInput(attrs={'class': 'add_food', 'type': 'password'}))
    password2 = forms.CharField(label='Nhập Lại Mật Khẩu', widget=forms.TextInput(attrs={'class': 'add_food', 'type': 'password'}))


    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError('mat khau khong hop le')

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except ObjectDoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("Tài khoản da ton tai")

    def clean_store(self):
        try:
            Owner.objects.get(store=self.cleaned_data['store'])
        except ObjectDoesNotExist:
            return self.cleaned_data['store']
        raise forms.ValidationError("Tên cửa hàng đã tồn tại")

    def save(self):
        owner_user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        owner_ob = Owner.objects.create(user=owner_user, name=self.cleaned_data['name'], phone=self.cleaned_data['phone'], store=self.cleaned_data['store'])
        Vendor.objects.create(name=self.cleaned_data['store'], owner=owner_ob)


