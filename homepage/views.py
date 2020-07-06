from django.shortcuts import render, HttpResponse
from django.views import View
from homepage.models import *
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