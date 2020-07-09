from django.shortcuts import render, HttpResponse, redirect
from django.views import View
# from homepage.models import *
from system.models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.core import serializers
# Create your views here.

class HomePage(View):
    # login_url = '/login/'
    def get(self, request):
        username = str(request.user)
        if (username == 'AnonymousUser'):
            return render(request, '_CNPM/index.html')

        user = User.objects.get(username=username) 
        if Chef.objects.filter(user=user).exists():
            return HttpResponse("<h2 style='color: red'>Về bếp làm việc đi thằng khốn, mò qua đây làm gì =))</h2>")

        user = Customer.objects.get(user=user)        
        order, created = Order.objects.get_or_create(customer=user, complete=False)
        # orderItems = OrderI.orderitem_set.all()
        total = order.get_total_quantity    
        context = {'total': total}            
        return render(request, '_CNPM/index.html', context)



class ChefPage(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        username = request.user
        user = User.objects.filter(username=username)
        if not Chef.objects.filter(user=user[0]).exists():
            return HttpResponse("<h2>You are not allowed to access this page</h2>")
        return render(request, '_CNPM/order.html')

class Wallet(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)
        customer = Customer.objects.get(user=user[0]) 
        my_wallet, created = MyWallet.objects.get_or_create(user=customer)
        if BankAccount.objects.filter(user=customer).exists():
            acc = BankAccount.objects.filter(user=customer)[0]
            return render(request, '_CNPM/mywallet.html', {"wallet":my_wallet, "account":acc})
        else:    
            return redirect('/page/wallet/login/')

    def post(self, request):
        if 'cash_in' in request.POST:
            money = float(str(request.POST.get("money")))
            username = str(request.user)
            user = User.objects.filter(username=username)
            customer = Customer.objects.get(user=user[0]) 
            # Bank
            acc = BankAccount.objects.get(user=customer)
            if money > acc.balance:
                return HttpResponse("So tien con lai cua ban " + str(acc.balance) + " khong du de nap!")
            acc.balance -= money
            acc.save()
            # Wallet
            my_wallet, created = MyWallet.objects.get_or_create(user=customer)
            my_wallet.my_balance += money
            my_wallet.save()
        return redirect('/page/wallet/')



            
class WalletLogin(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        return render(request, '_CNPM/mywallet_login.html')
        
    def post(self, request):
        username = request.POST.get("name")
        password = request.POST.get("password")
        name = request.POST.get("bank_name")
        bank_account = BankAccount.objects.filter(username=username, password=password, name=name)
        if bank_account.exists():
            username = str(request.user)
            user = User.objects.filter(username=username)
            customer = Customer.objects.get(user=user[0])
            acc = bank_account[0]
            acc.user = customer
            acc.save() 
            return redirect('/page/wallet/')
        else:
            return HttpResponse("Tai khoan khong ton tai!")
            

class ChefPageOrder(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        username = request.user
        user = User.objects.filter(username=username)
        if not Chef.objects.filter(user=user[0]).exists():
            return redirect('/auth/login/')
        return render(request, '_CNPM/order.html', {"orderlist":Order.objects.all(), "foodlist":Food.objects.all()})
    def post(self, request):
        if 'notify' in request.POST:
            noti = Notification(content="Hoa don cua ban da hoan thanh", title="Thong bao")
            return HttpResponse("Thong bao cho khach")
        else:
            return HttpResponse("Toang")


class ChefPageFoodDrink(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        username = request.user
        user = User.objects.filter(username=username)
        if not Chef.objects.filter(user=user[0]).exists():
            return HttpResponse("<h2>You are not allowed to access this page</h2>")
        return render(request, '_CNPM/fooddrink.html', {"foodlist":Food.objects.all()})
    def post(self, request):
        if 'outoforder' in request.POST:
            food = Food.objects.get(pk=request.POST["outoforder"])
            food.quantity = 0
            food.save()
        return redirect('/page/chefpage/2/')

class AdminPage(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, '_CNPM/index.html')

class Cart(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)      
        user = Customer.objects.get(user=user[0])       

        order, created = Order.objects.get_or_create(customer=user, complete=False)
        # orderItems = OrderI.orderitem_set.all()
        total = getTotalFood(order)
        total_bill = sum([item.get_total for item in order.orderitem_set.all()])
        context = {'total': total, 'order': order, 'total_bill': total_bill}
        return render(request, '_CNPM/Cart.html', context)
    def post(self, request):
        method = request.POST['my_method']
        note = request.POST['customer_note']
        return HttpResponse("You are submited")

def updatedItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action'] 
    # print(productID)

    # get user object
    username = str(request.user)
    user = User.objects.filter(username=username)
    if (len(user) == 0):
        return render(request, '_CNPM/index.html')
        
    user = Customer.objects.get(user=user[0])
    #get food
    food = Food.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, food=food)
    
    
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    total = order.get_total_quantity
    food_id = orderItem.food.id
    food_quantity = orderItem.quantity

    total_bill = order.get_total_price
    res = {
        'total': total,
        'id': food_id,
        'quantity': food_quantity,
        'total_bill': total_bill
    }
    
    

    # print('name', orderItem.food.name)
    # print('quantity', orderItem.quantity)
    # print("total bill", total_bill)
    return JsonResponse(res, safe=False)

def getTotalFood(order):
    items = order.orderitem_set.all()
    total = sum([item.quantity for item in items])
    print('total', total)
    # print(items[0].quantity)
    return total