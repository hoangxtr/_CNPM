import os
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils import timezone
from system.models import*
from .forms import*
from django.contrib.auth import authenticate, login, decorators, logout
from django.contrib.auth.models import User

# Create your views here.


def Log_out(request):
    logout(request)
    return redirect('owner')


def manLogin(request):
    if request.method == "POST":
        nameInput = request.POST['username']
        passInput = request.POST['password']
        try:
            user = User.objects.get(username=nameInput)
            if user.is_superuser:
                user = authenticate(username=nameInput, password=passInput)
                if user is not None:
                    login(request, user)
                    return redirect('manager')
                return render(request, 'polls/manlogin.html', {'wrong_mess': "Mật khẩu không trùng khớp"})
            return render(request, 'polls/manlogin.html', {'none_mess': "Bạn không phải quản lý của hệ thống."})
        except Exception as e:
            return render(request, 'polls/manlogin.html', {'none_mess': "Tài khoản không tồn tại."})
    return render(request, 'polls/manlogin.html')


@decorators.login_required(login_url='login/')
def man_homepage(request):
    food = Food.objects.all()
    ven = Vendor.objects.all()
    if not request.user.is_superuser:
        return HttpResponse('khong phai manager')
    form = OwnerRegisterForm()
    owner = Owner.objects.all()
    if request.method == "POST":
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'polls/manhomepage.html', {'form': form, 'owner': owner, 'food': food, 'vendor': ven, 'user': User.objects.all()})
    return render(request, 'polls/manhomepage.html', {'form':form, 'owner':owner, 'food': food, 'vendor': ven, 'user': User.objects.all()})


def delOwner(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    ven = get_object_or_404(Vendor, owner=owner)
    if request.method == "POST":
        try:
            for path in os.listdir('media/' + str(owner.store)):
                full_path = os.path.join('media/' + str(owner.store), path)
                if os.path.isfile(full_path):
                    os.remove(full_path)
            os.rmdir('media/' + str(owner.store))
            owner.user.delete()
            ven.delete()
        except Exception as e:
            owner.user.delete()
            ven.delete()
            return HttpResponseRedirect('../manager/')
        return HttpResponseRedirect('../manager/')
    return HttpResponse('Error')


def editOwner(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    if request.method == "POST":
        ownerVendor = Vendor.objects.get(owner=owner)
        if owner.store != request.POST['store']:
            print(os.getcwd())
            print('____________________')
            os.rename('media/' + owner.store, 'media/' + request.POST['store'])
            foodlist = Food.objects.filter(vendor__owner=owner)
            owner.store = request.POST['store']
            for food in foodlist:
                temp_1 = str(food.image).rfind('/')
                temp_2 = str(food.image)[temp_1::1]
                food.image = request.POST['store'] + temp_2
                food.save()
        owner.name = request.POST['name']
        owner.phone = request.POST['phone']
        if request.POST['password'] != "":
            owner.save()
            owner.user.set_password(request.POST['password'])
            owner.user.save()
            ownerVendor.name = owner.store
            ownerVendor.save()
        else:
            owner.save()
            ownerVendor.name = owner.store
            ownerVendor.save()
    return HttpResponseRedirect('../manager/')


class owner_homepage(LoginRequiredMixin, View):
    login_url = './login/'
    def get(self, request):
        try:
            owner = Owner.objects.get(user=request.user)
        except Exception as e:
           return HttpResponse('khong phai owner')
        chief = Chef.objects.filter(vendor__owner=owner)
        foodreal = Food.objects.filter(vendor__owner=owner)
        if request.method == "GET":
            searchValue = request.GET.get('search_value')
            if searchValue != "" and searchValue != None:
                foodreal = foodreal.filter(name__icontains=searchValue)
        context = {'foodreal': foodreal, 'staff': chief, 'store': owner.store}
        return render(request, "polls/ownerhomepage.html", context)

    def post(self, request):
        owner = Owner.objects.get(user=request.user)
        if owner is None:
            return HttpResponse('<h1 align="center"> KHÔNG PHẢI CHỦ CỬA HÀNG </h1>')
        d = HomeFood(request.POST, request.FILES)
        if not d.is_valid():
            print(request.FILES['image'])
            return HttpResponse('<h1 align="center"> FORM KHÔNG CHÍNH XÁC </h1>')
        else:
            data = Food()
            data.vendor = Vendor.objects.get(owner=owner)
            data.name = d.cleaned_data['name']
            data.price = d.cleaned_data['price']
            data.description = d.cleaned_data['description']
            data.image = request.FILES['image']
            data.quantity = d.cleaned_data['quantity']
            data.prepare = d.cleaned_data['prepare']
            data.save()
            return HttpResponseRedirect('./')



def OwnerLogin(request):
    if request.method == "POST":
        nameInput = request.POST['username']
        passInput = request.POST['password']
        try:
            user = User.objects.get(username=nameInput)
            try:
                own = Owner.objects.get(user=user)
                user = authenticate(username=nameInput, password=passInput)
                if user is not None:
                    login(request, user)
                    return redirect('owner')
                return render(request, 'polls/ownlogin.html', {'wrong_mess': "Mật khẩu không trùng khớp"})
            except Exception as e:
                return render(request, 'polls/ownlogin.html', {'none_mess': "Bạn không phải chủ cửa hàng."})
        except Exception as e:
            return render(request, 'polls/ownlogin.html', {'none_mess': "Tài khoản không tồn tại."})
    return render(request, 'polls/ownlogin.html')


def delFood(request, pk):
    ploc = get_object_or_404(Food ,pk=pk)
    if request.method == "POST":
        if os.path.exists('media/' + str(ploc.image)):
            os.remove('media/' + str(ploc.image))
        ploc.delete()
        return HttpResponseRedirect('../owner/')
    return HttpResponse('error')


def editMenu(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == "POST":
        if bool(request.FILES):
            os.remove('media/' + str(food.image))
            food.image = request.FILES['foodImage']
        Food.objects.create(
            vendor = food.vendor , prepare = request.POST['foodPrepare'],
            name = request.POST['foodName'], image = food.image,
            price = request.POST['foodPrice'], quantity = request.POST['foodQuantity'],
            description = request.POST['foodDescription']
        )
        food.delete()
    return HttpResponseRedirect('../owner/')


def AddStaff(request):
    username = request.POST['username']
    email = request.POST['email']
    name = request.POST['name']
    pass1 = request.POST['password1']
    pass2 = request.POST['password2']
    phone = request.POST['phone']
    if not pass1 == pass2:
        return HttpResponse('<h1> MẬT KHẨU KHÔNG TRÙNG KHỚP </h1>')
    try:
        User.objects.get(username=username)
    except ObjectDoesNotExist:
        newUser = User.objects.create_user(username=username, password=pass1, email=email)
        owner = Owner.objects.get(user=request.user)
        storeTemp = Vendor.objects.get(owner=owner)
        Chef.objects.create(user=newUser, name=name, vendor=storeTemp, phone=phone)
        return redirect('../owner')
    return HttpResponse('<h1> TÀI KHOẢN ĐÃ TỒN TẠI </h1>')


def EditStaff(request, pk):
    username = request.POST['username']
    email = request.POST['email']
    name = request.POST['name']
    password = request.POST['password']
    phone = request.POST['phone']
    chief = Chef.objects.get(pk=pk)
    if password != "":
        storeTemp = chief.vendor
        user = chief.user
        user.delete()
        newUser = User.objects.create_user(username=username, password=password, email=email)
        Chef.objects.create(user=newUser, name=name, vendor=storeTemp, phone=phone)
    else:
        chief.user.username = username
        chief.user.email = email
        chief.name = name
        chief.phone = phone
        chief.save()
    return HttpResponseRedirect('../owner/')


def delStaff(request, pk):
    chief = Chef.objects.get(pk=pk)
    user = chief.user
    user.delete()
    return HttpResponseRedirect('../owner')


class report:
    @decorators.login_required(login_url='owner/login/')
    def makeManReport(request):
        if not request.user.is_superuser:
           return HttpResponse('<h1 style="color: red" align="center> CÓ CL HACK ĐƯỢC KAO </h1>')
        else:
            from .write import writeManReport
            ven = Vendor.objects.all()
            writeManReport(ven)
            response = report.loadReport(str(timezone.now().month) + '-' + str(timezone.now().year) + '_report.xls', str(timezone.now().month) + '-' + str(timezone.now().year) + '_report.xls')
            return response


    def loadReport(reportPath, name):
        with open(reportPath, 'rb') as xlsx:
            response = HttpResponse(xlsx.read())
            response['content_type'] = 'application/xls'
            fileName = 'attachment; filename=' + name
            response['Content-Disposition'] = fileName
            xlsx.close()
            return response


    @decorators.login_required(login_url='owner/login/')
    def makeOwnerReport(request):
        owner = Owner.objects.get(user=request.user)
        if owner is None:
           return HttpResponse('<h1 style="color: red" align="center> CÓ CL HACK ĐƯỢC KAO </h1>')
        else:
            from .write import writeOwnerReport
            list_order_history = Order.objects.filter(vendor__owner=owner)
            time = writeOwnerReport(list_order_history, owner.store)
            response = report.loadReport('./media/' + owner.store + '/' + time + '_report.xls', time + '_report.xls')
            return response
