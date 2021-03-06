from django.shortcuts import render, HttpResponse, redirect
from django.views import View
# from homepage.models import *
from system.models import *
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
import json
from django.core import serializers
from system.forms import AvatarForm
# Create your views here.

#khue
import uuid
from urllib import request
import urllib.parse
from urllib.parse import urlsplit, parse_qs

from django.urls import reverse
# import urllib.request
import uuid
import hmac
import hashlib

import webbrowser

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
class HomePage(View):
    # login_url = '/login/'
    def get(self, request):
        import math
        username = str(request.user)
        if (username == 'AnonymousUser'):
            string = ""
            food = Food.objects.all()
            num = math.ceil(food.count()/12)
            for i in range(num):
                string = string + str(i)
            context = {'vendor': Vendor.objects.all(), 'food': food, 'num': string}
            return render(request, '_CNPM/index.html', context)

        user = User.objects.get(username=username)

        if not Customer.objects.filter(user=user).exists():
            return redirect('/auth/login/')
        customer = Customer.objects.get(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        # orderItems = OrderI.orderitem_set.all()
        total = order.get_total_quantity
        string = ""
        food = Food.objects.all()
        num = math.ceil(food.count() / 12)
        for i in range(num):
            string = string + str(i)
        context = {'total': total, 'vendor': Vendor.objects.all(), 'food': food, 'num': string, 'customer':customer}
        return render(request, '_CNPM/index.html', context)

    def post(self, request):
        import math
        if request.POST['vendors'] == 'all':
            name = ""
            if request.POST['s_value'] == '':
                food = Food.objects.all()
            else:
                food = Food.objects.filter(name__icontains=request.POST['s_value'])
        else:
            name = request.POST['vendors']
            if request.POST['s_value'] == '':
                food = Food.objects.filter(vendor__name=request.POST['vendors'])
            else:
                food = Food.objects.filter(vendor__name=request.POST['vendors'], name__icontains=request.POST['s_value'])
        num = math.ceil(food.count() / 12)
        string = ""
        for i in range(num):
            string = string + str(i)
        username = str(request.user)
        user = User.objects.filter(username=username)
        if not user.exists():
            context = {'vendor': Vendor.objects.all(), 'food': food, 'num': string, 'select': name}
        else:
            if not Customer.objects.filter(user=user[0]).exists():
            # if not Customer.objects.filter(user=request.user[0]).exists():

                return redirect('/auth/login/')
            customer = Customer.objects.get(user=request.user)
            order, created = Order.objects.get_or_create(customer=customer, status=0)
            # orderItems = OrderI.orderitem_set.all()
            total = order.get_total_quantity
            context = {'total': total, 'vendor': Vendor.objects.all(), 'food': food, 'num': string, 'select': name, 'customer':customer}
        return render(request, '_CNPM/index.html', context)



class Wallet(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)
        customer = Customer.objects.get(user=user[0]) 
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        # orderItems = OrderI.orderitem_set.all()
        total = order.get_total_quantity  
        my_wallet, created = MyWallet.objects.get_or_create(user=customer)
        my_wallet.my_account_number = 9999999*my_wallet.id - 12345678
        if BankAccount.objects.filter(user=customer).exists():
            acc = BankAccount.objects.filter(user=customer)[0]
            return render(request, '_CNPM/mywallet.html', {"wallet":my_wallet, "account":acc, "customer":customer,"total":total})
        elif my_wallet.my_balance == 0:    
            return redirect('/page/wallet/login/')
        else:
            return render(request, '_CNPM/mywallet.html', {"wallet":my_wallet, "account":"none","customer":customer,"total":total})

    def post(self, request):
        if 'cash_in' in request.POST:
            money = float(str(request.POST.get("money")))
            username = str(request.user)
            user = User.objects.filter(username=username)
            customer = Customer.objects.get(user=user[0])
            if BankAccount.objects.filter(user=customer).exists():
            # Bank
                acc = BankAccount.objects.get(user=customer)
                order, created = Order.objects.get_or_create(customer=customer, status=0)
                total = order.get_total_quantity
                if money > acc.balance:
                    return render(request, '_CNPM/resultPayment.html', {'result':'199', 'customer':user, 'total':total})
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
        return redirect('/page/wallet/')



            
class WalletLogin(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)
        customer = Customer.objects.get(user=user[0])
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        # orderItems = OrderI.orderitem_set.all()
        total = order.get_total_quantity  
        return render(request, '_CNPM/mywallet_login.html', {'customer':customer,'total':total})
        
    def post(self, request):
        bank_account_name = request.POST.get("name")
        bank_account_password = request.POST.get("password")
        bank_name = request.POST.get("bank_name")
        username = str(request.user)
        user = User.objects.filter(username=username)
        customer = Customer.objects.get(user=user[0])
        for account in BankAccount.objects.filter(user=customer):
            account.user = None
            account.save()
        bank_account = BankAccount.objects.filter(username=bank_account_name, password=bank_account_password, name=bank_name)
        if bank_account.exists():
            acc = bank_account[0]
            acc.user = customer
            acc.save() 
            return redirect('/page/wallet/')
        else:
            return HttpResponse("Please check your username and password again!")
            

class ChefPageOrder(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        username = request.user
        user = User.objects.filter(username=username)
        if not Chef.objects.filter(user=user[0]).exists():
            return redirect('/auth/login/')
        chef = Chef.objects.filter(user=user[0])[0]
        context = {
            "orders_to_chef":Order.objects.filter(status=1, vendor=chef.vendor), 
            "foodlist":Food.objects.all(),
            "orders_notify":Order.objects.filter(status=2, vendor=chef.vendor), 
        }
        return render(request, '_CNPM/order.html', context)

    def post(self, request):
        if 'notify' in request.POST:
            order = Order.objects.filter(pk = request.POST['notify'])[0]
            order.status = 2
            order.save()
        if 'complete' in request.POST:
            order = Order.objects.filter(pk = request.POST['complete'])[0]
            order.status = 3
            order.save()
        return redirect('/page/chefpage/')



class ChefPageFoodDrink(LoginRequiredMixin, View):
    login_url = '/auth/login/'
    def get(self, request):
        username = request.user
        user = User.objects.filter(username=username)
        if not Chef.objects.filter(user=user[0]).exists():
            return redirect('/auth/login/')
        chef = Chef.objects.filter(user=user[0])[0]
        return render(request, '_CNPM/fooddrink.html', {"foodlist":Food.objects.filter(vendor=chef.vendor)})
    def post(self, request):
        if 'outoforder' in request.POST:
            food = Food.objects.get(pk=request.POST["outoforder"])
            food.quantity = 0
            food.save()
        return redirect('/page/chefpage/2/')


class Cart(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)      
        customer = Customer.objects.get(user=user[0])       

        order, created = Order.objects.get_or_create(customer=customer, status=0)
        # orderItems = OrderI.orderitem_set.all()
        total = getTotalFood(order)
        total_bill = sum([item.get_total for item in order.orderitem_set.all()])
        context = {'total': total, 'order': order, 'total_bill': total_bill,'customer':customer}
        return render(request, '_CNPM/Cart.html', context)
    
    def post(self, request):
        method = request.POST['my_method']
        note = request.POST['customer_note']
        username = str(request.user)
        user = User.objects.filter(username=username)      
        user = Customer.objects.get(user=user[0])       
        order, created = Order.objects.get_or_create(customer=user, status=0)
        total = order.get_total_quantity
        if total == 0:
            return redirect('/page/cart/')
        total_bill = order.get_total_price
        channel_layer = get_channel_layer()
        if method == "dirty_coin":
            my_wallet, created = MyWallet.objects.get_or_create(user=user)
            if total_bill > my_wallet.my_balance:
                return render(request, '_CNPM/resultPayment.html', {'result':'99','customer':usser, 'total':total})
            else:
                my_wallet.my_balance = my_wallet.my_balance - total_bill
                my_wallet.save()
                for vendor in Vendor.objects.all(): 
                    if order.orderitem_set.filter(vendor=vendor).exists():
                        order_vendor = Order.objects.create(customer=user, status=1, vendor=vendor, note=note)
                        for item in order.orderitem_set.filter(vendor=vendor):
                            item.order = order_vendor
                            item.save()
                        order_vendor.vendor = vendor
                        order_vendor.save()
                async_to_sync(channel_layer.group_send)(
                    "users", 
                    {
                        'type': 'chat.message',
                        "command": 'to_chef'
                    }
                )        
                return render(request, '_CNPM/resultPayment.html', {'result':'0','customer':user,'total':0})
        elif method == "Momo":
            return redirect('/page/payByMoMo/')
        return render(request, '_CNPM/resultPayment.html', {'result':'49', 'customer':user, 'total':total})

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
    order, created = Order.objects.get_or_create(customer=user, status=0)
    orderItem, created = OrderItem.objects.get_or_create(order=order, food=food, vendor=food.vendor)
    
    
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



#khue
def result(request):
    url = request.get_full_path()
    query = urlsplit(url).query
    query = urllib.parse.parse_qs(query)
    query = json.dumps(query)
    query = str(json.loads(query)['errorCode'])
    query = query.replace("['", '')
    query = query.replace("']", '')

    # Change status of Order after paying
    username = str(request.user)
    user = User.objects.filter(username=username)
    user = Customer.objects.get(user=user[0])
    channel_layer = get_channel_layer()
    order, created = Order.objects.get_or_create(customer=user, status=0)
    if query == '0':  # Having successful payment
        order.status = 1
        order.save()
        async_to_sync(channel_layer.group_send)(
            "users", 
            {
                'type': 'chat.message',
                "command": 'to_chef'
            }
        )
        

    #  return result for customer
    context = {'result': query, 'total':0}
    return render(request, '_CNPM/resultPayment.html', context)


class payByMoMo(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)
        user = Customer.objects.get(user=user[0])

        order, created = Order.objects.get_or_create(customer=user, status=0)
        # orderItems = OrderI.orderitem_set.all()
        total = getTotalFood(order)
        total_bill = sum([item.get_total for item in order.orderitem_set.all()])
        # -----------------------UPDATE AMOUNT-------------------
        total_bill = round(total_bill)
        endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
        partnerCode = "MOMOLKP820200711"
        accessKey = "ngh9wZuFqjzXqXSd"
        serectkey = "pC5hHhAgkg2AwHydTnP7kBvpBruhSlK5"
        orderInfo = "Pay by MoMo"
        returnUrl = "http://127.0.0.1:8000/page/result"
        notifyurl = "http://127.0.0.1:8000/page/result"
        amount = str(total_bill)
        orderId = str(uuid.uuid4())
        requestId = str(uuid.uuid4())
        requestType = "captureMoMoWallet"
        # pass empty value if your merchant does not have stores else merchantName=[storeName]; merchantId=[storeId] to identify a transaction map with a physical store
        extraData = "merchantName=;merchantId="

        # before sign HMAC SHA256 with format
        # partnerCode=$partnerCode&accessKey=$accessKey&requestId=$requestId&amount=$amount&orderId=$oderId&orderInfo=$orderInfo&returnUrl=$returnUrl&notifyUrl=$notifyUrl&extraData=$extraData
        rawSignature = "partnerCode=" + partnerCode + "&accessKey=" + accessKey + "&requestId=" + requestId + "&amount=" \
                       + amount + \
                       "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&returnUrl=" + \
                       returnUrl + "&notifyUrl=" + notifyurl + "&extraData=" + extraData

        # puts raw signature
        print("--------------------RAW SIGNATURE----------------")
        print(rawSignature)
        # signature
        # h=hmac.new(b'serectkey', data.encode('utf-8'), hashlib.sha256).hexdigest()
        # h = hmac.new(b'serectkey', rawSignature.encode('utf-8'), hashlib.sha256)
        h = hmac.new(serectkey.encode('utf-8'), rawSignature.encode('utf-8'), hashlib.sha256)

        signature = h.hexdigest()
        print("--------------------SIGNATURE----------------")
        print(signature)

        # json object send to MoMo endpoint

        data = {
            'partnerCode': partnerCode,
            'accessKey': accessKey,
            'requestId': requestId,
            'amount': amount,
            'orderId': orderId,
            'orderInfo': orderInfo,
            'returnUrl': returnUrl,
            'notifyUrl': notifyurl,
            'extraData': extraData,
            'requestType': requestType,
            'signature': signature
        }
        print("--------------------JSON REQUEST----------------\n")

        # from obj in python to string by json.dumps then convert to binary
        data = str.encode(json.dumps(data))
        clen = len(data)
        req = urllib.request.Request(endpoint, data, {'Content-Type': 'application/json', 'Content-Length': clen})
        f = urllib.request.urlopen(req)
        response = f.read()
        f.close()
        try:
            url = json.loads(response)['payUrl']

            # response = urllib.request.urlopen(url)
            # open url return by MoMo
            # webbrowser.open(url)
            print("notifyURL")

            return redirect(url)
        except:
            print("################### Loi so tien khong hop le ##############")


# --------------------------------HistoryOrder--------------------
def MyOrder(request):
    username = str(request.user)
    user = User.objects.filter(username=username)
    customer = Customer.objects.get(user=user[0])
    order, created = Order.objects.get_or_create(customer=customer, status=0)
        # orderItems = OrderI.orderitem_set.all()
    total = order.get_total_quantity    
    context = {'orders': Order.objects.filter(customer=customer), 'total': total, 'customer':customer}
    return render(request, '_CNPM/MyOrder.html', context)


class Profile(View):
    def get(self, request):
        username = str(request.user)
        user = User.objects.get(username=username)
        customer = Customer.objects.get(user=user)
        order, created = Order.objects.get_or_create(customer=customer, status=0)
        # orderItems = OrderI.orderitem_set.all()
        total = order.get_total_quantity  
        avatar = AvatarForm()
        return render(request, '_CNPM/my_info.html', {"customer":customer, "avatar":avatar, "total":total})
    
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
            customer.user.email = email
        # Set phone
        if 'phone' in request.POST:
            phone = request.POST["phone"]
            customer.phone = phone
        # Set password
        if 'password' in request.POST:
            password = request.POST["password"]
            customer.user.set_password(password)
            customer.user.save()
            login(request, user=user[0])
        # Set avatar
        # if 'ava' in request.POST:
        #     ava = request.FILES["ava"]
        #     customer.ava = ava
        if 'ava' in request.POST:
            avatar = AvatarForm(request.POST, request.FILES)
            if avatar.is_valid():
                customer.avatar = avatar.cleaned_data["avatar"]
        customer.user.save()
        customer.save()
        return redirect('/page/profile/')


def result(request):
    # hanle response json from momo
    url = request.get_full_path()
    query = urlsplit(url).query
    query = urllib.parse.parse_qs(query)
    query = json.dumps(query)
    query = str(json.loads(query)['errorCode'])
    query = query.replace("['", '')
    query = query.replace("']", '')

    # Change status of Order after paying
    username = str(request.user)
    user = User.objects.filter(username=username)
    user = Customer.objects.get(user=user[0])

    order, created = Order.objects.get_or_create(customer=user, status=0)
    if query == '0':  # Having successful payment
        order.status = 1
    else:
        order.status = 0

    #  return result for customer
    context = {'result': query}
    return render(request, '_CNPM/resultPayment.html', context)
