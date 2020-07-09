import uuid
from urllib import request
import urllib.parse
from urllib.parse import urlsplit, parse_qs
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from homepage.models import *
from system.models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpRequest
from django.views.generic.base import RedirectView
from django.http import HttpResponse, HttpResponseRedirect
import json

# import for handle MoMo
from django.urls import reverse
import urllib.request
import uuid
import hmac
import hashlib
import requests

import webbrowser
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
        return HttpResponse(note)


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
    # get food
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

    total_bill = order.get_total_amount
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


# --------------------------------------Pay by MoMo wallet-------------------------
def result(request):
    url = request.get_full_path()
    query = urlsplit(url).query
    query = urllib.parse.parse_qs(query)
    query = json.dumps(query)
    query = str(json.loads(query)['localMessage'])
    query = query.replace("['", '')
    query = query.replace("']", '')

    context = {'result': query}

    return render(request, '_CNPM/resultPayment.html', context)


class payByMoMo(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        username = str(request.user)
        user = User.objects.filter(username=username)
        user = Customer.objects.get(user=user[0])

        order, created = Order.objects.get_or_create(customer=user, complete=False)
        # orderItems = OrderI.orderitem_set.all()
        total = getTotalFood(order)
        total_bill = sum([item.get_total for item in order.orderitem_set.all()])
        # -----------------------UPDATE AMOUNT-------------------
        total_bill = round(total_bill) * 1000
        endpoint = "https://test-payment.momo.vn/gw_payment/transactionProcessor"
        partnerCode = "MOMO"
        accessKey = "F8BBA842ECF85"
        serectkey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
        orderInfo = "pay with MoMo"
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
        url = json.loads(response)['payUrl']

        # response = urllib.request.urlopen(url)
        # open url return by MoMo
        # webbrowser.open(url)
        print("notifyURL")

        return redirect(url)


# --------------------------------HistoryOrder--------------------
def MyOrder(request):
    username = str(request.user)
    user = User.objects.filter(username=username)
    user = Customer.objects.get(user=user[0])

    context = {'orders': Order.objects.get_or_create(customer=user, complete=True)}
    return render(request, '_CNPM/MyOrder.html', context)
