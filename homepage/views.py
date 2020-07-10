from django.shortcuts import render, HttpResponse, redirect
from django.views import View
<<<<<<< HEAD
# from homepage.models import *
=======
from homepage.models import *
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
from system.models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.core import serializers
<<<<<<< HEAD
from system.forms import AvatarForm
=======
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
# Create your views here.

class HomePage(View):
    # login_url = '/login/'
    def get(self, request):
        username = str(request.user)
        if (username == 'AnonymousUser'):
            return render(request, '_CNPM/index.html')

<<<<<<< HEAD
        user = User.objects.get(username=username) 
        if Chef.objects.filter(user=user).exists():
            return HttpResponse("<h2 style='color: red'>Về bếp làm việc đi thằng khốn, mò qua đây làm gì =))</h2>")

        user = Customer.objects.get(user=user)        
        order, created = Order.objects.get_or_create(customer=user, complete=False)
        # orderItems = OrderI.orderitem_set.all()
        total = order.get_total_quantity    
=======
        user = User.objects.get(username=username)
        if Chef.objects.filter(user=user).exists():
            return redirect('/auth/login/')

        user = Customer.objects.get(user=user)        
        order, created = Order.objects.get_or_create(customer=user, is_completed=False)
        # orderItems = OrderI.orderitem_set.all()
        total = getTotalFood(order)
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
        context = {'total': total}            
        return render(request, '_CNPM/index.html', context)


<<<<<<< HEAD

class ChefPage(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        username = request.user
        user = User.objects.filter(username=username)
        if not Chef.objects.filter(user=user[0]).exists():
            return HttpResponse("<h2>You are not allowed to access this page</h2>")
        return render(request, '_CNPM/order.html')

# Phan them vo
=======
class AdminPage(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        return render(request, '_CNPM/index.html')

class Cart(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)      
        user = Customer.objects.get(user=user[0])       

        order, created = Order.objects.get_or_create(customer=user, is_completed=False)
        # orderItems = OrderI.orderitem_set.all()
        total = getTotalFood(order)
        total_bill = sum([item.get_total for item in order.orderitem_set.all()])
        context = {'total': total, 'order': order, 'total_bill': total_bill}
        return render(request, '_CNPM/Cart.html', context)

def updatedItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    print(productID)

    # get user object
    username = str(request.user)
    user = User.objects.filter(username=username)
    if (len(user) == 0):
        return render(request, '_CNPM/index.html')
        
    user = Customer.objects.get(user=user[0])
    #get food
    food = Food.objects.get(id=productID)
    order, created = Order.objects.get_or_create(customer=user, is_completed=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, food=food)
    
    
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    total = getTotalFood(order)
    food_id = orderItem.food.id
    food_quantity = orderItem.quantity

    total_bill = sum([item.get_total for item in order.orderitem_set.all()])
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


# Phan cua Khang


>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
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
<<<<<<< HEAD
        elif my_wallet.my_balance == 0:    
            return redirect('/page/wallet/login/')
        else:
            return render(request, '_CNPM/mywallet.html', {"wallet":my_wallet, "account":"none"})
=======
        else:    
            return redirect('/page/wallet/login/')
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4

    def post(self, request):
        if 'cash_in' in request.POST:
            money = float(str(request.POST.get("money")))
            username = str(request.user)
            user = User.objects.filter(username=username)
<<<<<<< HEAD
            customer = Customer.objects.get(user=user[0])
            if BankAccount.objects.filter(user=customer).exists():
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
            else:
                return redirect('/page/wallet/login/')
        if 'unlink' in request.POST:
            username = str(request.user)
            user = User.objects.filter(username=username)
            customer = Customer.objects.get(user=user[0]) 
            acc = BankAccount.objects.get(user=customer)
            acc.user = None
            acc.save()
=======
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
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
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
<<<<<<< HEAD
#Phan them vo           
 
=======
            

>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
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

<<<<<<< HEAD
class AdminPage(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request):
        return render(request, '_CNPM/index.html')
# Sua lai
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
        if 'pay' in request.POST:
            username = str(request.user)
            user = User.objects.filter(username=username)      
            user = Customer.objects.get(user=user[0])       
            order, created = Order.objects.get_or_create(customer=user, complete=False)
            total_bill = sum([item.get_total for item in order.orderitem_set.all()])
            if method == "dirty_coin":
                my_wallet, created = MyWallet.objects.get_or_create(user=user)
                if total_bill > my_wallet.my_balance:
                    return HttpResponse('Ko du tien')
                else:
                    my_wallet.my_balance =  my_wallet.my_balance - total_bill
                    my_wallet.save()
                    return HttpResponse('Ban da thanh toan thanh cong')
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



# def upload_pic(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = ExampleModel.objects.get(pk=course_id)
#             m.model_pic = form.cleaned_data['image']
#             m.save()
#             return HttpResponse('image upload success')
#     return HttpResponseForbidden('allowed only via POST')

class Profile(View):
    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)
        customer = Customer.objects.get(user=user[0])  
        avatar = AvatarForm()
        return render(request, '_CNPM/my_info.html', {"customer":customer, "avatar":avatar})
    
    def post(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username) 
        customer = Customer.objects.get(user=user[0]) 
        # Set name
        if 'name' in request.POST:
            name = request.POST["name"]
            customer.user.username = name
        # Set email
        if 'email' in request.POST:
            email = request.POST["email"]
            customer.email = email
        # Set phone
        if 'phone' in request.POST:
            phone = request.POST["phone"]
            customer.phone = phone
        # Set password
        if 'password' in request.POST:
            password = request.POST["password"]
            customer.user.set_password(password)
        # Set avatar
        # if 'ava' in request.POST:
        #     ava = request.FILES["ava"]
        #     customer.ava = ava
        avatar = AvatarForm(request.POST, request.FILES)
        if avatar.is_valid():
            customer.avatar = avatar.cleaned_data["avatar"]
        customer.user.save()  
        customer.save()
        return render(request, '_CNPM/my_info.html', {"customer":customer, "avatar":avatar})

=======
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
