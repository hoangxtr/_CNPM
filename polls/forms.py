from django import forms
from system.models import Food, Owner, Vendor
import re
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User


class HomeFood(forms.ModelForm):
    class Meta:
        model = Food
        fields = ('name', 'price', 'description', 'image', 'quantity', 'prepare')

    def clean_image(self):
        temp = str(self.cleaned_data['image'])
        if temp[-4::1] == '.png' or temp[-4::1] == '.jpg':
            return temp
        else:
            raise forms.ValidationError('Đây Không Phải Tệp Hình Ảnh')



class OwnerRegisterForm(forms.Form):
    store = forms.CharField(label='Tên Cửa Hàng', max_length=30, widget=forms.TextInput(attrs={'class': 'add_food', 'id': 'newStore'}))
    username = forms.CharField(label='Tài khoản', max_length=30, widget=forms.TextInput(attrs={'class': 'add_food', 'id': 'newUsername'}))
    name = forms.CharField(label='Họ và Tên', max_length=20, widget=forms.TextInput(attrs={'class': 'add_food', 'id': 'newName'}))
    phone = forms.CharField(label='Số Điện Thoại', max_length=13, widget=forms.TextInput(attrs={'class': 'add_food', 'id': 'newPhone'}))
    password1 = forms.CharField(label='Mật Khẩu', widget=forms.TextInput(attrs={'class': 'add_food', 'type': 'password', 'id': 'newPass1'}))
    password2 = forms.CharField(label='Nhập Lại Mật Khẩu', widget=forms.TextInput(attrs={'class': 'add_food', 'type': 'password', 'id': 'newPass2'}))

    def save(self):
        owner_user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        owner_ob = Owner.objects.create(user=owner_user, name=self.cleaned_data['name'], phone=self.cleaned_data['phone'], store=self.cleaned_data['store'])
        Vendor.objects.create(name=self.cleaned_data['store'], owner=owner_ob)


