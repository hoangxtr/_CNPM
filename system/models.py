from django.db import models
<<<<<<< HEAD
# from homepage.models import Customer
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=25, unique=False)
    email = models.EmailField(max_length=254, default='')
    phone = models.CharField(max_length=10, default='')
    avatar = models.ImageField(upload_to="uploads/", blank=True, null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customers"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')
    name = models.CharField(max_length=25, unique=False)
    isManage = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Admins"

class Chef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='chef')
    name = models.CharField(max_length=25, unique=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Chefs"

=======
from homepage.models import Customer
# Create your models here.

>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
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
<<<<<<< HEAD
	complete = models.BooleanField(default=False) # true when order is completed
	to_chef = models.BooleanField(default=False) # true when customer completes the order and this order send to chef
	is_shipping = models.BooleanField(default=False)    # true when chef confirm the order and notify customer of getting food 
	note = models.CharField(max_length=255, default='')
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
	@property
	def get_total_price(self):
		"""
			This function use for get total money of order
		"""
		return sum([item.get_total for item in self.orderitem_set.all()])
	@property
	def get_total_quantity(self):
		"""
			This function use for get total quantity of order
		"""
		return sum([item.quantity for item in self.orderitem_set.all()])

		

=======
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
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4

class OrderItem(models.Model):
	food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)

	def __str__(self):
<<<<<<< HEAD
		return str(self.food.name)

	@property
	def get_total(self):
		"""
			get total money of order item
		"""
=======
		return str(self.order.id)

	@property
	def get_total(self):
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
		total = self.food.price * self.quantity
		return total


<<<<<<< HEAD

=======
# Phan cua Khang 
 
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
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
<<<<<<< HEAD
    my_balance = models.FloatField(default=0)


=======
    my_balance = models.FloatField(default=0)
>>>>>>> 33099c2c05e6664c9b0ac30281128c00d2ff97b4
