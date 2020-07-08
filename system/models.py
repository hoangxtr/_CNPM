from django.db import models
from homepage.models import Customer
# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
	    return self.name

class Food(models.Model):
    name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to="uploads/")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	is_completed = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
	note = models.CharField(max_length=255, default='')
	def __str__(self):
		return str(self.id)

	@property
	def get_total_price(self):
		return sum([item.get_total for item in self.orderitem_set.all()])
	@property
	def get_total_quantity(self):
		return sum([item.quantity for item in order.orderitem_set.all()])

class OrderItem(models.Model):
	food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
		return str(self.order.id)

	@property
	def get_total(self):
		total = self.food.price * self.quantity
		return total


# Phan cua Khang 
 
class BankAccount(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255, default='')
    image = models.ImageField(upload_to="uploads/")
    account_number = models.IntegerField(default=0)
    balance = models.FloatField(default=0)


class MyWallet(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    my_account_number = models.IntegerField(default=0)
    my_balance = models.FloatField(default=0)