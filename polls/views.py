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
import os
# Create your views here.


def Log_out(request):
    logout(request)
    return redirect('owner')


def manLogin(request):
    if request.method == "POST":
        nameInput = request.POST['username']
        passInput = request.POST['password']
        user = authenticate(username=nameInput, password=passInput)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('manager')
            return HttpResponse('<h1 style="color:red; text-align:center;"> BẠN KHÔNG PHẢI QUẢN LÝ CỦA HỆ THỐNG NÀY </h1>')
        return HttpResponse('pha cc')
    return render(request, 'polls/manlogin.html')


@decorators.login_required(login_url='login/')
def man_homepage(request):
    food = Food.objects.all()
    ven = vendor.objects.all()
    if not request.user.is_superuser:
        return HttpResponse('khong phai manager')
    form = OwnerRegisterForm()
    owner = Owner.objects.all()
    if request.method == "POST":
        form = OwnerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            form = OwnerRegisterForm()
            return render(request, 'polls/manhomepage.html', {'form': form, 'owner': owner, 'mess': "Thêm Cửa Hàng Thành Công", 'food': food, 'vendor': ven})
    return render(request, 'polls/manhomepage.html', {'form':form, 'owner':owner, 'food': food, 'vendor': ven})


def delOwner(request, pk):
    owner = get_object_or_404(Owner, pk=pk)
    ven = get_object_or_404(vendor, owner=owner)
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
        ownerVendor = vendor.objects.get(owner=owner)
        if owner.store != request.POST['store']:
            os.rename('media/' + owner.store, 'media/' + request.POST['store'])
            foodlist = Food.objects.filter(store__owner=owner)
            owner.store = request.POST['store']
            for food in foodlist:
                temp_1 = str(food.foodImage).rfind('/')
                temp_2 = str(food.foodImage)[temp_1::1]
                food.foodImage = request.POST['store'] + temp_2
                food.save()
        owner.user.username = request.POST['email']
        owner.name = request.POST['name']
        owner.phone = request.POST['phone']
        if request.POST['password'] != "":
            owner.user.delete()
            newUser = User.objects.create_user(username = request.POST['email'], password = request.POST['password'])
            newOwner = Owner.objects.create(phone=request.POST['phone'], name=request.POST['name'], store=request.POST['store'], user=newUser)
            owner.user = newUser
            ownerVendor.name = owner.store
            ownerVendor.owner = newOwner
            ownerVendor.save()
        else:
            owner.save()
            ownerVendor.name = owner.store
            ownerVendor.save()
    return HttpResponseRedirect('../manager/')


@decorators.login_required(login_url='owner/login/')
def makeManReport(request):
    if not request.user.is_superuser:
       return HttpResponse('<h1 style="color: red" align="center> CÓ CL HACK ĐƯỢC KAO </h1>')
    else:
        import xlwt
        from xlwt import Workbook
        wb = Workbook()
        sheet1 = wb.add_sheet('Sheet 1')
        row = 0
        col = 0
        sum_total = 0
        ven = vendor.objects.all()
        border_center = xlwt.easyxf(
            'borders: top_color black, left_color black, bottom_color black, right_color black, '
            ' top thin, left thin, bottom thin, right thin; align: vert centre, horiz centre')
        border = xlwt.easyxf('borders: top_color black, left_color black, bottom_color black, right_color black, '
                             ' top thin, left thin, bottom thin, right thin')
        border_top_bot = xlwt.easyxf('borders: top_color black, bottom_color black, top thin, bottom thin')
        sheet1.write(row, col, 'Báo Cáo Tháng: ' + str(timezone.now().month) + ' năm ' + str(timezone.now().year))
        sheet1.merge(row, row, col, col + 2)
        row = 2
        col = 2
        for store in ven:
            write = True
            sumStore = 0
            list_order = Order.objects.filter(store=store)
            for order in list_order:
                if order.date_ordered.month == timezone.now().month and order.date_ordered.year == timezone.now().year and order.status == 3:
                    quantity = 0
                    sum = 0;
                    list_order_item = OrderItem.objects.filter(order=order)
                    if write:
                        sheet1.write(row, col - 1, str(order.store.name) + ':', border_top_bot)
                        sheet1.merge(row, row, col - 1, col + 2, border_top_bot)
                        row = row + 2;
                        sheet1.write(row, col, 'Ngày', border_center)
                        sheet1.write(row, col + 1, 'Số Lượng Đơn Hàng', border_center)
                        sheet1.write(row, col + 2, 'Doanh Thu (VND)', border_center)
                        write = False
                        row = row + 1
                    for orderItem in list_order_item:
                        sum = sum + orderItem.get_total
                        quantity = quantity + 1
                    sumStore = sumStore + sum
                    sheet1.write(row, col, str(order.date_ordered.day), border_center)
                    sheet1.write(row, col + 1, quantity, border)
                    sheet1.write(row, col + 2, sum, border)
                    row = row + 1
            sheet1.write(row + 1, col - 1, 'Tổng Doanh Thu Tháng', border_top_bot)
            sheet1.merge(row + 1, row + 1, col - 1, col, border_top_bot)
            sheet1.write(row + 1, col + 1, '', border_top_bot)
            sheet1.write(row + 1, col + 2, sumStore, border_top_bot)
            row = row + 4
            sum_total = sum_total + sumStore
        sheet1.write(row, col - 2, 'Doanh Thu Tháng Food Court: ' + str(sum_total) + ' VND')
        sheet1.merge(row, row, col - 2, col + 1)
        wb.save(str(timezone.now().month) + '-' + str(timezone.now().year) + '_report.xls')
        response = loadReport(str(timezone.now().month) + '-' + str(timezone.now().year) + '_report.xls', str(timezone.now().month) + '-' + str(timezone.now().year) + '_report.xls')
        return response



class owner_homepage(LoginRequiredMixin, View):
    login_url = './login/'
    def get(self, request):
        try:
            owner = Owner.objects.get(user=request.user)
        except Exception as e:
           return HttpResponse('khong phai owner')
        chief = Chef.objects.filter(store__owner=owner)
        foodreal = Food.objects.filter(store__owner=owner)
        if request.method == "GET":
            searchValue = request.GET.get('search_value')
            if searchValue != "" and searchValue != None:
                foodreal = foodreal.filter(foodName__icontains=searchValue)
        context = {'foodreal': foodreal, 'staff': chief, 'store': owner.store}
        return render(request, "polls/ownerhomepage.html", context)

    def post(self, request):
        owner = Owner.objects.get(user=request.user)
        if owner is None:
            return HttpResponse('<h1 align="center"> KHÔNG PHẢI CHỦ CỬA HÀNG </h1>')
        d = HomeFood(request.POST, request.FILES)
        if not d.is_valid():
            return HttpResponse('<h1 align="center"> FORM KHÔNG CHÍNH XÁC </h1?')
        else:
            data = Food()
            data.store = vendor.objects.get(owner=owner)
            data.foodName = d.cleaned_data['foodName']
            data.foodPrice = d.cleaned_data['foodPrice']
            data.foodDescription = d.cleaned_data['foodDescription']
            data.foodImage = request.FILES['foodImage']
            data.foodQuantity = d.cleaned_data['foodQuantity']
            data.foodPrepare = d.cleaned_data['foodPrepare']
            data.foodState = True
            data.save()
            return HttpResponseRedirect('./')



def OwnerLogin(request):
    if request.method == "POST":
        nameInput = request.POST['username']
        passInput = request.POST['password']
        user = authenticate(username=nameInput, password=passInput)
        if user is not None:
            login(request, user)
            return redirect('owner')
            return HttpResponse('<h1 style="color:red; text-align:center;"> BẠN KHÔNG PHẢI QUẢN LÝ CỦA HỆ THỐNG NÀY </h1>')
        return HttpResponse('pha cc')
    return render(request, 'polls/ownlogin.html')


def delFood(request, pk):
    ploc = get_object_or_404(Food ,pk=pk)
    if request.method == "POST":
        if os.path.exists('media/' + str(ploc.foodImage)):
            os.remove('media/' + str(ploc.foodImage))
        ploc.delete()
        return HttpResponseRedirect('../owner/')
    return HttpResponse('error')


def editMenu(request, pk):
    food = get_object_or_404(Food, pk=pk)
    if request.method == "POST":
        if bool(request.FILES):
            os.remove('media/' + str(food.foodImage))
            food.foodImage = request.FILES['foodImage']
        Food.objects.create(
            store = food.store , foodPrepare = request.POST['foodPrepare'],
            foodName = request.POST['foodName'], foodImage = food.foodImage,
            foodPrice = request.POST['foodPrice'], foodQuantity = request.POST['foodQuantity'],
            foodDescription = request.POST['foodDescription'], foodState = True
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
        storeTemp = vendor.objects.get(owner=owner)
        Chef.objects.create(user=newUser, name=name, store=storeTemp, phone=phone)
        return redirect('../owner')
    return HttpResponse('<h1> TÀI KHOẢN ĐÃ TỒN TẠI </h1>')

def EditStaff(request, pk):
    username = request.POST['username']
    email = request.POST['email']
    name = request.POST['name']
    password = request.POST['password']
    phone = request.POST['phone']
    chief = Chef.objects.get(pk=pk)
    storeTemp = chief.store
    user = chief.user
    user.delete()
    newUser = User.objects.create_user(username=username, password=password, email=email)
    Chef.objects.create(user=newUser, name=name, store=storeTemp, phone=phone)
    return HttpResponseRedirect('../owner/')


def delStaff(request, pk):
    chief = Chef.objects.get(pk=pk)
    user = chief.user
    user.delete()
    return HttpResponseRedirect('../owner')


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
        import xlwt
        from xlwt import Workbook

        wb = Workbook()
        sheet1 = wb.add_sheet('Sheet 1')
        row = 0
        col = 0
        sum_total = 0
        list_order_history = Order.objects.filter(store__owner=owner)
        border_center = xlwt.easyxf('borders: top_color black, left_color black, bottom_color black, right_color black, '
                                    ' top thin, left thin, bottom thin, right thin; align: vert centre, horiz centre')
        border = xlwt.easyxf('borders: top_color black, left_color black, bottom_color black, right_color black, '
                                    ' top thin, left thin, bottom thin, right thin')
        border_top_bot = xlwt.easyxf('borders: top_color black, bottom_color black, top thin, bottom thin')
        time = str(timezone.now().day) + '-' + str(timezone.now().month) + '-' + str(timezone.now().year)
        sheet1.write(row, col, 'Báo Cáo Ngày: ' + time)
        sheet1.merge(row, row, col, col + 2)
        row = row + 2
        col = col + 2
        for orderHistory in list_order_history:
            if orderHistory.date_ordered.year == timezone.now().year and orderHistory.date_ordered.month == timezone.now().month and orderHistory.date_ordered.day == timezone.now().day and orderHistory.status == 3:
                list_order_item = OrderItem.objects.filter(order=orderHistory)
                sheet1.write(row, col, 'Mã Giao Dịch: ' + str(orderHistory.transaction_id), border_top_bot)
                sheet1.merge(row, row, col, col + 1, border_top_bot)
                sheet1.write(row, col + 2, '', border_top_bot)
                sheet1.write(row, col + 3, '', border_top_bot)
                sheet1.write(row, col + 4, '', border_top_bot)
                row = row + 2
                col = col + 1
                sheet1.write(row, col, 'Tên Món Ăn', border_center)
                sheet1.write(row, col + 1, 'Số Lượng', border_center)
                sheet1.write(row, col + 2, 'Giá Tiền (VND)', border_center)
                sheet1.write(row, col + 3, 'Thành Tiền (VND)', border_center)
                sum = 0
                for orderDetail in list_order_item:
                    sheet1.write(row + 1, col, str(orderDetail.food.foodName), border_center)
                    sheet1.write(row + 1, col + 1, orderDetail.quantity, border)
                    sheet1.write(row + 1, col + 2, orderDetail.food.foodPrice, border)
                    sheet1.write(row + 1, col + 3, orderDetail.get_total, border)
                    sum = sum + orderDetail.get_total
                    row = row + 1
                sheet1.write(row + 2, col - 1, 'Tổng Tiền', border_top_bot)
                sheet1.write(row + 2, col + 3, sum, border_top_bot)
                sheet1.write(row + 2, col, '', border_top_bot)
                sheet1.write(row + 2, col + 1, '', border_top_bot)
                sheet1.write(row + 2, col + 2, '', border_top_bot)
                sum_total = sum_total + sum
                row = row + 5
                col = 2
        sheet1.write(row, 0, 'Doanh Thu Ngày: ' + str(sum_total) + ' VND')
        sheet1.merge(row, row, 0, 2)
        wb.save('./media/' + owner.store + '/' + time + '_report.xls')
        response = loadReport('./media/' + owner.store + '/' + time + '_report.xls', time + '_report.xls')
        return response
